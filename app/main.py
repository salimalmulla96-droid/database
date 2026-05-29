import csv
import json
import re
import shutil
import urllib.error
import urllib.request
import zipfile
from datetime import datetime
from difflib import SequenceMatcher
from pathlib import Path
from uuid import uuid4

from fastapi import Depends, FastAPI, File, Form, Request, UploadFile
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import inspect, or_, text
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from .models import (
    AppearanceSetting,
    BackupLog,
    DuplicateRecord,
    Education,
    ExportLog,
    ExtractedItem,
    Note,
    Organization,
    OrganizationRelationship,
    Person,
    Position,
    Relationship,
    SettingOption,
    Source,
)


BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"
TEMPLATES_DIR = BASE_DIR / "templates"
UPLOAD_DIR = STATIC_DIR / "uploads"
SOURCE_UPLOAD_DIR = UPLOAD_DIR / "sources"
EXPORT_DIR = BASE_DIR / "exports"
BACKUP_DIR = BASE_DIR / "backups"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
SOURCE_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
EXPORT_DIR.mkdir(parents=True, exist_ok=True)
BACKUP_DIR.mkdir(parents=True, exist_ok=True)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Smart Database")
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))
templates.env.cache = None


@app.get("/health")
def health():
    return {"status": "ok"}

PERSON_GENDERS = ["Male", "Female", "Unknown"]
NATIONALITIES = [
    "UAE",
    "Saudi Arabia",
    "Kuwait",
    "Qatar",
    "Bahrain",
    "Oman",
    "Egypt",
    "Jordan",
    "Lebanon",
    "Syria",
    "Palestine",
    "Iraq",
    "Yemen",
    "India",
    "Pakistan",
    "United Kingdom",
    "United States",
    "Other",
    "Unknown",
]
PERSON_STATUSES = ["Alive", "Deceased", "Unknown"]
PERSON_CATEGORIES = [
    "Government Figure",
    "Royal Family",
    "Business Figure",
    "Family Member",
    "Friend",
    "University Friend",
    "Classmate",
    "Colleague",
    "Historical Figure",
    "Ministry Employee",
    "Company Employee",
    "Public Figure",
    "Private Contact",
    "Other",
]
ORGANIZATION_TYPES = [
    "Ministry",
    "Government Authority",
    "Government Department",
    "Council",
    "Company",
    "Holding Company",
    "University",
    "School",
    "Hospital",
    "Bank",
    "Family Business",
    "Royal Office",
    "Charity",
    "Foundation",
    "Committee",
    "Other",
]
ORGANIZATION_STATUSES = ["Active", "Inactive", "Merged", "Renamed", "Unknown"]
EMIRATES = [
    "Abu Dhabi",
    "Dubai",
    "Sharjah",
    "Ajman",
    "Umm Al Quwain",
    "Ras Al Khaimah",
    "Fujairah",
    "Federal",
    "GCC",
    "International",
    "Unknown",
]
RELATIONSHIP_TYPES = [
    "Father",
    "Mother",
    "Son",
    "Daughter",
    "Brother",
    "Sister",
    "Husband",
    "Wife",
    "Grandfather",
    "Grandmother",
    "Grandson",
    "Granddaughter",
    "Uncle",
    "Aunt",
    "Cousin",
    "Nephew",
    "Niece",
    "Friend",
    "Classmate",
    "Colleague",
    "Business Partner",
    "Mentor",
    "Student",
    "Connected To",
    "Other",
]
NOTE_TYPES = [
    "General Note",
    "Personal Note",
    "Family Note",
    "Education Note",
    "Career Note",
    "Government Note",
    "Business Note",
    "Historical Note",
    "Source Note",
    "Meeting Note",
    "Important Fact",
    "Warning / Unverified",
    "Other",
]
ORGANIZATION_RELATIONSHIP_TYPES = [
    "Parent Organization",
    "Subsidiary",
    "Partner",
    "Government Owner",
    "Regulator",
    "Managed By",
    "Related Entity",
    "Replaced By",
    "Former Name Of",
    "Merged With",
    "Other",
]
SOURCE_TYPES = ["Link", "Image", "File", "Text Reference", "Screenshot", "Other"]
ROLE_TYPES = [
    "Government Role",
    "Business Role",
    "Academic Role",
    "Board Member",
    "Founder",
    "Chairman",
    "CEO",
    "Minister",
    "Director",
    "Employee",
    "Advisor",
    "Other",
]

HEX_COLOR_RE = re.compile(r"^#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})$")
FONT_FAMILIES = [
    "System Default",
    "Arial",
    "Segoe UI",
    "Tahoma",
    "Verdana",
    "Georgia",
    "Times New Roman",
    "Cairo",
    "Noto Sans Arabic",
]
FONT_WEIGHTS = ["400", "500", "600", "700", "800", "900"]
COLOR_FIELDS = [
    ("primary_color", "Primary color", "اللون الأساسي", "Used for main buttons, active menu items, and important highlights.", "يستخدم للأزرار الرئيسية وعناصر القائمة النشطة والتمييز المهم."),
    ("secondary_color", "Secondary color", "اللون الثانوي", "Used for secondary actions, quiet highlights, and supporting UI elements.", "يستخدم للإجراءات الثانوية والتمييز الهادئ والعناصر المساندة."),
    ("accent_color", "Accent color", "لون التمييز", "Used for links, focus rings, and small emphasis details.", "يستخدم للروابط وإطارات التركيز والتفاصيل البارزة الصغيرة."),
    ("background_color", "Background color", "لون الخلفية", "Used for the main page background.", "يستخدم لخلفية صفحات الموقع."),
    ("surface_color", "Surface/card color", "لون البطاقات", "Used for cards, panels, modals, and table surfaces.", "يستخدم للبطاقات واللوحات والنوافذ والجداول."),
    ("sidebar_bg", "Sidebar background", "خلفية الشريط الجانبي", "Used for the left navigation menu background.", "يستخدم لخلفية قائمة التنقل الجانبية."),
    ("sidebar_text", "Sidebar text color", "لون نص الشريط الجانبي", "Used for sidebar links, labels, and the app title.", "يستخدم لروابط الشريط الجانبي وتسمياته واسم التطبيق."),
    ("heading_color", "Heading color", "لون العناوين", "Used for page titles, section titles, and card headings.", "يستخدم لعناوين الصفحات والأقسام والبطاقات."),
    ("body_text_color", "Body text color", "لون النص الأساسي", "Used for normal text, records, descriptions, and form text.", "يستخدم للنصوص العادية والسجلات والوصف ونص النماذج."),
    ("muted_text_color", "Muted text color", "لون النص الهادئ", "Used for helper text, metadata, subtitles, and secondary labels.", "يستخدم للنصوص المساعدة والبيانات الفرعية والعناوين الصغيرة."),
    ("border_color", "Border color", "لون الحدود", "Used for card, input, table, and panel borders.", "يستخدم لحدود البطاقات والحقول والجداول واللوحات."),
    ("success_color", "Success color", "لون النجاح", "Used for success badges, positive states, and completed indicators.", "يستخدم لشارات النجاح والحالات الإيجابية ومؤشرات الاكتمال."),
    ("warning_color", "Warning color", "لون التحذير", "Used for warning boxes, unverified badges, and caution states.", "يستخدم لصناديق التحذير والشارات غير المؤكدة وحالات التنبيه."),
    ("danger_color", "Danger color", "لون الخطر", "Used for delete buttons, warning icons, and danger badges.", "يستخدم لأزرار الحذف وأيقونات التحذير وشارات الخطر."),
]
TEXT_GROUPS = [
    ("global", "Global Font", "الخط العام", "Affects most text in the website.", "يؤثر على معظم النصوص في الموقع."),
    ("sidebar", "Sidebar Menu Font", "خط القائمة الجانبية", "This controls the font of the left main menu items, such as Dashboard, People, Organizations, Smart Add, and Settings.", "يتحكم بخط عناصر القائمة الرئيسية مثل لوحة التحكم والأشخاص والجهات والإضافة الذكية والإعدادات."),
    ("heading", "Page Heading Font", "خط عناوين الصفحات", "Affects page titles like People, Organizations, and Settings.", "يؤثر على عناوين الصفحات مثل الأشخاص والجهات والإعدادات."),
    ("card_title", "Card Title Font", "خط عناوين البطاقات", "This controls person names, organization names, profile titles, and card headings.", "يتحكم بأسماء الأشخاص والجهات وعناوين الملفات والبطاقات."),
    ("body", "Body Text Font", "خط النص العادي", "This controls notes, descriptions, explanations, and normal paragraph text.", "يتحكم بالملاحظات والوصف والشرح والنصوص العادية."),
    ("button", "Button Font", "خط الأزرار", "This controls all button text, including Add, Save, Delete, Edit, Filter, and Cancel.", "يتحكم بنصوص الأزرار مثل إضافة وحفظ وحذف وتعديل وتصفية وإلغاء."),
    ("form", "Form Font", "خط النماذج", "This controls form labels, dropdown options, input text, and placeholders.", "يتحكم بتسميات النماذج وخيارات القوائم ونص الحقول والنصوص الإرشادية."),
    ("badge", "Badge Font", "خط الشارات", "This controls badges like nationality, category, status, and confidence.", "يتحكم بالشارات مثل الجنسية والفئة والحالة والثقة."),
]
DEFAULT_APPEARANCE_SETTINGS = {
    "primary_color": "#1F6FEB",
    "secondary_color": "#0F9F8F",
    "accent_color": "#2563EB",
    "background_color": "#F4F7FB",
    "surface_color": "#FFFFFF",
    "sidebar_bg": "#071526",
    "sidebar_text": "#CDD7E6",
    "heading_color": "#071526",
    "body_text_color": "#172235",
    "muted_text_color": "#6B778B",
    "border_color": "#DCE4EF",
    "success_color": "#16A34A",
    "warning_color": "#B54708",
    "danger_color": "#B42318",
    "card_radius": "8",
    "button_radius": "8",
    "sidebar_width": "270",
}
for group, *_ in TEXT_GROUPS:
    DEFAULT_APPEARANCE_SETTINGS[f"{group}_font_family"] = "System Default"
    DEFAULT_APPEARANCE_SETTINGS[f"{group}_font_size"] = {
        "global": "16",
        "sidebar": "15",
        "heading": "34",
        "card_title": "18",
        "body": "16",
        "button": "14",
        "form": "15",
        "badge": "13",
    }[group]
    DEFAULT_APPEARANCE_SETTINGS[f"{group}_font_weight"] = {
        "global": "500",
        "sidebar": "700",
        "heading": "800",
        "card_title": "800",
        "body": "500",
        "button": "800",
        "form": "500",
        "badge": "700",
    }[group]
    DEFAULT_APPEARANCE_SETTINGS[f"{group}_letter_spacing"] = "0"

SETTINGS_SECTIONS = {
    "overview": {
        "label": "Overview",
        "label_ar": "نظرة عامة",
        "icon": "fa-table-cells-large",
        "description": "Review setting health, quick actions, and live previews.",
        "description_ar": "راجع حالة الإعدادات والإجراءات السريعة والمعاينات.",
        "categories": [],
    },
    "people": {
        "label": "People Settings",
        "label_ar": "الأشخاص",
        "icon": "fa-users",
        "description": "Manage dropdowns and badges used when adding or filtering people.",
        "description_ar": "إدارة القوائم والشارات المستخدمة في الأشخاص.",
        "categories": ["gender", "nationality", "person_status", "person_category", "tag_suggestion"],
    },
    "organizations": {
        "label": "Organization Settings",
        "label_ar": "الجهات",
        "icon": "fa-building",
        "description": "Manage organization types, statuses, emirates, and entity links.",
        "description_ar": "إدارة أنواع الجهات والحالات والإمارات والعلاقات.",
        "categories": ["organization_type", "organization_status", "emirate", "organization_relationship_type"],
    },
    "career": {
        "label": "Career & Position Settings",
        "label_ar": "المسار المهني والمناصب",
        "icon": "fa-briefcase",
        "description": "Manage role types, position suggestions, and current role display rules.",
        "description_ar": "إدارة أنواع المناصب واقتراحات المسميات وقواعد المناصب الحالية.",
        "categories": ["role_type", "position_title_suggestion", "department_suggestion"],
    },
    "relationships": {
        "label": "Relationships",
        "label_ar": "العلاقات",
        "icon": "fa-link",
        "description": "Manage relationship labels, reverse meanings, and relationship groups.",
        "description_ar": "إدارة مسميات العلاقات والمعاني العكسية والمجموعات.",
        "categories": ["relationship_type"],
    },
    "education": {
        "label": "Education",
        "label_ar": "التعليم",
        "icon": "fa-graduation-cap",
        "description": "Manage education degrees, countries, and institution suggestions.",
        "description_ar": "إدارة الدرجات التعليمية والدول واقتراحات المؤسسات.",
        "categories": ["education_degree", "country", "institution_type"],
    },
    "notes": {
        "label": "Notes & Sources Settings",
        "label_ar": "الملاحظات والمصادر",
        "icon": "fa-note-sticky",
        "description": "Manage note categories, source types, and file source behavior.",
        "description_ar": "إدارة أنواع الملاحظات والمصادر وسلوك الملفات.",
        "categories": ["note_type", "source_type"],
    },
    "interface": {
        "label": "Interface & Language",
        "label_ar": "الواجهة واللغة",
        "icon": "fa-language",
        "description": "Preview language, RTL, sidebar style, density, and theme behavior.",
        "description_ar": "معاينة اللغة واتجاه الواجهة والشريط والكثافة والثيم.",
        "categories": ["interface_language", "card_density", "theme"],
    },
    "appearance": {
        "label": "Appearance & Design",
        "label_ar": "إعدادات المظهر والتصميم",
        "icon": "fa-palette",
        "description": "Customize website colors, fonts, cards, buttons, sidebar, and preview changes before applying.",
        "description_ar": "تخصيص ألوان الموقع والخطوط والبطاقات والأزرار والشريط الجانبي مع معاينة التغييرات قبل التطبيق.",
        "categories": [],
    },
    "data": {
        "label": "Data Management",
        "label_ar": "إدارة البيانات",
        "icon": "fa-database",
        "description": "Export, backup, reset defaults, and review dangerous actions.",
        "description_ar": "التصدير والنسخ الاحتياطي وإعادة الضبط والإجراءات الحساسة.",
        "categories": [],
    },
}

COLOR_FIELDS = [
    ("primary_color", "Primary Color", "اللون الأساسي", "Used for main buttons, active menu items, important highlights.", "يستخدم للأزرار الرئيسية وعناصر القائمة النشطة والتمييز المهم.", "Brand Colors"),
    ("secondary_color", "Secondary Color", "اللون الثانوي", "Used for secondary buttons and subtle accents.", "يستخدم للأزرار الثانوية واللمسات الهادئة.", "Brand Colors"),
    ("accent_color", "Accent Color", "لون التمييز", "Used for highlights, focus states, and small visual accents.", "يستخدم للتمييز وحالات التركيز واللمسات الصغيرة.", "Brand Colors"),
    ("app_background", "App Background", "خلفية التطبيق", "Used for the main page background.", "تستخدم لخلفية صفحات الموقع.", "Layout Colors"),
    ("card_background", "Card Background", "خلفية البطاقات", "Used for cards, panels, forms, modals.", "تستخدم للبطاقات واللوحات والنماذج والنوافذ.", "Layout Colors"),
    ("sidebar_background", "Sidebar Background", "خلفية الشريط الجانبي", "Used for the left main menu.", "تستخدم للشريط الجانبي الرئيسي.", "Layout Colors"),
    ("sidebar_text", "Sidebar Text", "نص الشريط الجانبي", "Used for sidebar links and menu labels.", "يستخدم لروابط وتسميات الشريط الجانبي.", "Layout Colors"),
    ("sidebar_active", "Sidebar Active Item", "عنصر الشريط النشط", "Used for selected sidebar item.", "يستخدم لعنصر الشريط الجانبي المحدد.", "Layout Colors"),
    ("heading_text", "Heading Text", "نص العناوين", "Used for page titles and section headings.", "يستخدم لعناوين الصفحات والأقسام.", "Text Colors"),
    ("body_text", "Body Text", "النص الأساسي", "Used for normal text.", "يستخدم للنصوص العادية.", "Text Colors"),
    ("muted_text", "Muted Text", "النص الهادئ", "Used for helper text, subtitles, placeholders.", "يستخدم للنصوص المساعدة والعناوين الفرعية والنصوص الإرشادية.", "Text Colors"),
    ("border_color", "Border Color", "لون الحدود", "Used for card borders, input borders, dividers.", "يستخدم لحدود البطاقات والحقول والفواصل.", "Layout Colors"),
    ("success_color", "Success Color", "لون النجاح", "Used for success badges and confirm actions.", "يستخدم لشارات النجاح وإجراءات التأكيد.", "State Colors"),
    ("warning_color", "Warning Color", "لون التحذير", "Used for warnings and unverified data.", "يستخدم للتحذيرات والبيانات غير المؤكدة.", "State Colors"),
    ("danger_color", "Danger Color", "لون الخطر", "Used for delete buttons and dangerous actions.", "يستخدم لأزرار الحذف والإجراءات الخطرة.", "State Colors"),
]

TEXT_GROUPS = [
    ("global", "Global Font", "الخط العام", "Controls most text across the website.", "يتحكم بمعظم النصوص في الموقع."),
    ("sidebar", "Sidebar Menu Font", "خط القائمة الجانبية", "Controls Dashboard, People, Organizations, Smart Add, Settings, and all left menu labels.", "يتحكم بلوحة التحكم والأشخاص والجهات والإضافة الذكية والإعدادات وكل عناصر القائمة الجانبية."),
    ("heading", "Page Heading Font", "خط عناوين الصفحات", "Controls People page title, Organization page title, Settings title, and profile page titles.", "يتحكم بعناوين صفحات الأشخاص والجهات والإعدادات وعناوين الملفات."),
    ("record_name", "Record Name Font", "خط أسماء السجلات", "Controls person names, organization names, profile names, and search result names.", "يتحكم بأسماء الأشخاص والجهات وأسماء الملفات ونتائج البحث."),
    ("card_title", "Card Title Font", "خط عناوين البطاقات", "Controls card headings, section titles inside profile pages, and note titles.", "يتحكم بعناوين البطاقات وعناوين أقسام الملفات وعناوين الملاحظات."),
    ("body", "Body Text Font", "خط النص العادي", "Controls descriptions, notes, explanations, and paragraphs.", "يتحكم بالوصف والملاحظات والشرح والفقرات."),
    ("form", "Form Font", "خط النماذج", "Controls labels, input text, dropdown text, and placeholders.", "يتحكم بالتسميات ونص الحقول والقوائم والنصوص الإرشادية."),
    ("button", "Button Font", "خط الأزرار", "Controls Add Person, Save, Delete, Filter, Cancel, and Apply Changes.", "يتحكم بأزرار إضافة شخص وحفظ وحذف وتصفية وإلغاء وتطبيق التغييرات."),
    ("badge", "Badge Font", "خط الشارات", "Controls status, category, nationality, and confidence badges.", "يتحكم بشارات الحالة والفئة والجنسية والثقة."),
]

DEFAULT_APPEARANCE_SETTINGS = {
    "primary_color": "#2563EB",
    "secondary_color": "#64748B",
    "accent_color": "#0EA5E9",
    "app_background": "#F4F7FB",
    "card_background": "#FFFFFF",
    "sidebar_background": "#071B33",
    "sidebar_text": "#EAF2FF",
    "sidebar_active": "#0F2D50",
    "heading_text": "#0F172A",
    "body_text": "#334155",
    "muted_text": "#64748B",
    "border_color": "#E2E8F0",
    "success_color": "#16A34A",
    "warning_color": "#F59E0B",
    "danger_color": "#DC2626",
    "card_radius": "8",
    "button_radius": "10",
    "sidebar_width": "270",
}
for group, *_ in TEXT_GROUPS:
    DEFAULT_APPEARANCE_SETTINGS[f"{group}_font_family"] = "System Default"
    DEFAULT_APPEARANCE_SETTINGS[f"{group}_font_size"] = {
        "global": "16",
        "sidebar": "15",
        "heading": "34",
        "record_name": "18",
        "card_title": "18",
        "body": "16",
        "form": "15",
        "button": "14",
        "badge": "13",
    }[group]
    DEFAULT_APPEARANCE_SETTINGS[f"{group}_font_weight"] = {
        "global": "500",
        "sidebar": "700",
        "heading": "800",
        "record_name": "800",
        "card_title": "800",
        "body": "500",
        "form": "500",
        "button": "800",
        "badge": "700",
    }[group]
    DEFAULT_APPEARANCE_SETTINGS[f"{group}_letter_spacing"] = "0"

SETTINGS_SECTIONS = {
    "overview": {"label": "Overview", "icon": "fa-table-cells-large", "description": "Choose a settings area to manage.", "categories": []},
    "people": {"label": "People", "icon": "fa-users", "description": "Manage people dropdowns, labels, icons, and colors.", "categories": ["gender", "nationality", "person_status", "person_category", "tag_suggestion"]},
    "organizations": {"label": "Organizations", "icon": "fa-building", "description": "Manage organization types, statuses, locations, and relationship labels.", "categories": ["organization_type", "organization_status", "emirate", "organization_relationship_type"]},
    "career": {"label": "Career & Positions", "icon": "fa-briefcase", "description": "Manage role types, position titles, and department suggestions.", "categories": ["role_type", "position_title_suggestion", "department_suggestion"]},
    "relationships": {"label": "Relationships", "icon": "fa-link", "description": "Manage person and organization relationship labels.", "categories": ["relationship_type", "organization_relationship_type"]},
    "notes": {"label": "Notes & Sources", "icon": "fa-note-sticky", "description": "Manage note categories and source types.", "categories": ["note_type", "source_type"]},
    "appearance": {"label": "Appearance Studio", "icon": "fa-palette", "description": "Control colors, fonts, text groups, buttons, cards, and sidebar style with a live preview.", "categories": []},
    "data": {"label": "Data & Backup", "icon": "fa-database", "description": "Export, backup, reset defaults, and review data actions.", "categories": []},
}

DEFAULT_SETTING_OPTIONS = {
    "gender": [
        ("Male", "Male", "ذكر", "fa-mars", "#2563eb"),
        ("Female", "Female", "أنثى", "fa-venus", "#db2777"),
        ("Unknown", "Unknown", "غير معروف", "fa-circle-question", "#64748b"),
    ],
    "person_status": [
        ("Alive", "Alive", "على قيد الحياة", "fa-heart-pulse", "#16a34a"),
        ("Deceased", "Deceased", "متوفى", "fa-dove", "#475569"),
        ("Unknown", "Unknown", "غير معروف", "fa-circle-question", "#64748b"),
    ],
    "nationality": [(item, item, ar, "fa-flag", "#0f766e") for item, ar in [
        ("UAE", "الإمارات العربية المتحدة"), ("Saudi Arabia", "السعودية"), ("Kuwait", "الكويت"),
        ("Qatar", "قطر"), ("Bahrain", "البحرين"), ("Oman", "عُمان"), ("Egypt", "مصر"),
        ("Jordan", "الأردن"), ("Lebanon", "لبنان"), ("Syria", "سوريا"), ("Palestine", "فلسطين"),
        ("Iraq", "العراق"), ("Yemen", "اليمن"), ("India", "الهند"), ("Pakistan", "باكستان"),
        ("United Kingdom", "المملكة المتحدة"), ("United States", "الولايات المتحدة"),
        ("Other", "أخرى"), ("Unknown", "غير معروف"),
    ]],
    "person_category": [(item, item, ar, "fa-user-tag", "#1d4ed8") for item, ar in [
        ("Government Figure", "شخصية حكومية"), ("Royal Family", "الأسرة الحاكمة"),
        ("Business Figure", "شخصية أعمال"), ("Family Member", "فرد من العائلة"), ("Friend", "صديق"),
        ("University Friend", "صديق جامعي"), ("Classmate", "زميل دراسة"), ("Colleague", "زميل عمل"),
        ("Historical Figure", "شخصية تاريخية"), ("Ministry Employee", "موظف وزارة"),
        ("Company Employee", "موظف شركة"), ("Public Figure", "شخصية عامة"),
        ("Private Contact", "جهة اتصال خاصة"), ("Other", "أخرى"),
    ]],
    "organization_type": [(item, item, ar, "fa-building", "#334155") for item, ar in [
        ("Ministry", "وزارة"), ("Government Authority", "هيئة حكومية"),
        ("Government Department", "دائرة حكومية"), ("Council", "مجلس"), ("Company", "شركة"),
        ("Holding Company", "شركة قابضة"), ("University", "جامعة"), ("School", "مدرسة"),
        ("Hospital", "مستشفى"), ("Bank", "بنك"), ("Family Business", "شركة عائلية"),
        ("Royal Office", "مكتب رسمي"), ("Charity", "جمعية خيرية"), ("Foundation", "مؤسسة"),
        ("Committee", "لجنة"), ("Other", "أخرى"),
    ]],
    "organization_status": [(item, item, ar, "fa-toggle-on", "#0f766e") for item, ar in [
        ("Active", "نشطة"), ("Inactive", "غير نشطة"), ("Merged", "مدمجة"),
        ("Renamed", "تغير اسمها"), ("Unknown", "غير معروف"),
    ]],
    "emirate": [(item, item, ar, "fa-location-dot", "#0369a1") for item, ar in [
        ("Abu Dhabi", "أبوظبي"), ("Dubai", "دبي"), ("Sharjah", "الشارقة"),
        ("Ajman", "عجمان"), ("Umm Al Quwain", "أم القيوين"), ("Ras Al Khaimah", "رأس الخيمة"),
        ("Fujairah", "الفجيرة"), ("Federal", "اتحادي"), ("GCC", "خليجي"),
        ("International", "دولي"), ("Unknown", "غير معروف"),
    ]],
    "role_type": [(item, item, ar, "fa-briefcase", "#7c3aed") for item, ar in [
        ("Government Role", "منصب حكومي"), ("Business Role", "منصب تجاري"),
        ("Academic Role", "منصب أكاديمي"), ("Board Member", "عضو مجلس إدارة"), ("Founder", "مؤسس"),
        ("Chairman", "رئيس مجلس إدارة"), ("CEO", "رئيس تنفيذي"), ("Minister", "وزير"),
        ("Director", "مدير"), ("Employee", "موظف"), ("Advisor", "مستشار"), ("Other", "أخرى"),
    ]],
    "position_title_suggestion": [(item, item, ar, "fa-id-badge", "#7c3aed") for item, ar in [
        ("President", "رئيس"), ("Vice President", "نائب رئيس"), ("Prime Minister", "رئيس مجلس الوزراء"),
        ("Deputy Prime Minister", "نائب رئيس مجلس الوزراء"), ("Minister", "وزير"),
        ("Chairman", "رئيس مجلس إدارة"), ("Vice Chairman", "نائب رئيس مجلس إدارة"),
        ("CEO", "رئيس تنفيذي"), ("Director General", "مدير عام"), ("Executive Director", "مدير تنفيذي"),
        ("Board Member", "عضو مجلس إدارة"), ("Founder", "مؤسس"), ("Co-Founder", "شريك مؤسس"),
        ("Advisor", "مستشار"), ("Manager", "مدير"), ("Employee", "موظف"), ("Other", "أخرى"),
    ]],
    "relationship_type": [(item, item, ar, "fa-link", "#0891b2") for item, ar in [
        ("Father", "أب"), ("Mother", "أم"), ("Son", "ابن"), ("Daughter", "ابنة"),
        ("Brother", "أخ"), ("Sister", "أخت"), ("Husband", "زوج"), ("Wife", "زوجة"),
        ("Grandfather", "جد"), ("Grandmother", "جدة"), ("Grandson", "حفيد"), ("Granddaughter", "حفيدة"),
        ("Uncle", "عم / خال"), ("Aunt", "عمة / خالة"), ("Cousin", "ابن/بنت عم أو خال"),
        ("Nephew", "ابن الأخ/الأخت"), ("Niece", "بنت الأخ/الأخت"), ("Friend", "صديق"),
        ("Classmate", "زميل دراسة"), ("Colleague", "زميل عمل"), ("Business Partner", "شريك عمل"),
        ("Mentor", "موجّه"), ("Student", "طالب"), ("Connected To", "مرتبط بـ"), ("Other", "أخرى"),
    ]],
    "organization_relationship_type": [(item, item, ar, "fa-network-wired", "#0f766e") for item, ar in [
        ("Parent Organization", "جهة أم"), ("Subsidiary", "شركة تابعة"), ("Partner", "شريك"),
        ("Government Owner", "مالك حكومي"), ("Regulator", "جهة تنظيمية"), ("Managed By", "تُدار بواسطة"),
        ("Related Entity", "جهة مرتبطة"), ("Replaced By", "استُبدلت بـ"),
        ("Former Name Of", "الاسم السابق لـ"), ("Merged With", "اندمجت مع"), ("Other", "أخرى"),
    ]],
    "note_type": [(item, item, ar, "fa-note-sticky", "#ca8a04") for item, ar in [
        ("General Note", "ملاحظة عامة"), ("Personal Note", "ملاحظة شخصية"), ("Family Note", "ملاحظة عائلية"),
        ("Education Note", "ملاحظة تعليمية"), ("Career Note", "ملاحظة مهنية"), ("Government Note", "ملاحظة حكومية"),
        ("Business Note", "ملاحظة تجارية"), ("Historical Note", "ملاحظة تاريخية"), ("Source Note", "ملاحظة مصدر"),
        ("Meeting Note", "ملاحظة مقابلة"), ("Important Fact", "معلومة مهمة"),
        ("Warning / Unverified", "تحذير / غير مؤكد"), ("Other", "أخرى"),
    ]],
    "source_type": [(item, item, ar, "fa-paperclip", "#475569") for item, ar in [
        ("Link", "رابط"), ("Image", "صورة"), ("File", "ملف"), ("Text Reference", "مرجع نصي"),
        ("Screenshot", "لقطة شاشة"), ("Other", "أخرى"),
    ]],
    "education_degree": [(item, item, ar, "fa-graduation-cap", "#2563eb") for item, ar in [
        ("High School", "الثانوية العامة"), ("Diploma", "دبلوم"), ("Bachelor", "بكالوريوس"),
        ("Master", "ماجستير"), ("PhD", "دكتوراه"), ("Fellowship", "زمالة"),
        ("Certificate", "شهادة"), ("Other", "أخرى"),
    ]],
    "country": [(item, item, ar, "fa-earth-asia", "#0f766e") for item, ar in [
        ("UAE", "الإمارات العربية المتحدة"), ("Saudi Arabia", "السعودية"),
        ("United Kingdom", "المملكة المتحدة"), ("United States", "الولايات المتحدة"),
        ("Other", "أخرى"), ("Unknown", "غير معروف"),
    ]],
    "tag_suggestion": [(item, item, ar, "fa-tag", "#64748b") for item, ar in [
        ("Government", "حكومي"), ("Business", "أعمال"), ("Family", "عائلة"), ("Education", "تعليم"),
    ]],
    "department_suggestion": [(item, item, ar, "fa-sitemap", "#7c3aed") for item, ar in [
        ("Executive Office", "المكتب التنفيذي"), ("Board Office", "مكتب مجلس الإدارة"), ("Strategy", "الاستراتيجية"),
    ]],
    "institution_type": [(item, item, ar, "fa-school", "#2563eb") for item, ar in [
        ("University", "جامعة"), ("School", "مدرسة"), ("Institute", "معهد"), ("Other", "أخرى"),
    ]],
    "interface_language": [(item, item, ar, "fa-language", "#0f766e") for item, ar in [
        ("English", "الإنجليزية"), ("Arabic", "العربية"), ("Both", "الاثنان"),
    ]],
    "card_density": [(item, item, ar, "fa-table-cells", "#334155") for item, ar in [
        ("Comfortable", "مريح"), ("Compact", "مدمج"),
    ]],
    "theme": [(item, item, ar, "fa-palette", "#1f6feb") for item, ar in [
        ("Light", "فاتح"), ("Dark Navy", "كحلي داكن"), ("System", "حسب النظام"),
    ]],
    "confidence": [(item, item, ar, icon, color) for item, ar, icon, color in [
        ("Confirmed", "مؤكد", "fa-circle-check", "#16a34a"),
        ("Likely", "غالباً صحيح", "fa-thumbs-up", "#2563eb"),
        ("Unverified", "غير مؤكد", "fa-triangle-exclamation", "#b45309"),
        ("Private", "خاص", "fa-lock", "#7c3aed"),
        ("Outdated", "قديم", "fa-clock", "#64748b"),
        ("Unknown", "غير معروف", "fa-circle-question", "#64748b"),
    ]],
    "privacy_level": [(item, item, ar, icon, color) for item, ar, icon, color in [
        ("Public Fact", "معلومة عامة", "fa-globe", "#16a34a"),
        ("Private Note", "ملاحظة خاصة", "fa-lock", "#7c3aed"),
        ("Sensitive / Do Not Export", "حساس / لا يتم تصديره", "fa-shield-halved", "#b91c1c"),
    ]],
    "input_type": [(item, item, ar, "fa-wand-magic-sparkles", "#1f6feb") for item, ar in [
        ("Person", "شخص"), ("Organization", "جهة"), ("Career / Position", "مسار مهني / منصب"),
        ("Education", "تعليم"), ("Relationship", "علاقة"), ("Note", "ملاحظة"), ("Source", "مصدر"),
        ("Mixed Information", "معلومات مختلطة"), ("Unknown / Auto Detect", "غير معروف / اكتشاف تلقائي"),
    ]],
    "review_status": [(item, item, ar, "fa-list-check", "#334155") for item, ar in [
        ("Pending Review", "بانتظار المراجعة"), ("Approved", "معتمد"), ("Rejected", "مرفوض"),
        ("Merged", "مدمج"), ("Saved as Note", "حفظ كملاحظة"),
    ]],
    "intake_source_type": [(item, item, ar, "fa-paperclip", "#475569") for item, ar in [
        ("Personal Knowledge", "معرفة شخصية"), ("Official Website", "موقع رسمي"),
        ("News Article", "خبر صحفي"), ("Government Website", "موقع حكومي"),
        ("Company Website", "موقع شركة"), ("Document", "وثيقة"), ("Screenshot", "لقطة شاشة"),
        ("Social Media", "وسائل التواصل"), ("Other", "أخرى"),
    ]],
}
RELATIONSHIP_GROUPS = {
    "Family": {
        "Father",
        "Mother",
        "Son",
        "Daughter",
        "Brother",
        "Sister",
        "Husband",
        "Wife",
        "Grandfather",
        "Grandmother",
        "Grandson",
        "Granddaughter",
        "Uncle",
        "Aunt",
        "Cousin",
        "Nephew",
        "Niece",
    },
    "Work / Professional": {"Colleague", "Business Partner", "Mentor", "Student"},
    "Social": {"Friend", "Classmate"},
}


def migrate_database():
    additions = {
        "people": {
            "fourth_name": "VARCHAR",
            "image_path": "VARCHAR",
            "education": "VARCHAR",
            "university": "VARCHAR",
            "major": "VARCHAR",
            "graduation_year": "INTEGER",
            "current_role": "VARCHAR",
            "main_field": "VARCHAR",
            "known_for": "TEXT",
            "achievements": "TEXT",
            "public_summary": "TEXT",
            "tags": "VARCHAR",
            "created_at": "DATETIME",
            "updated_at": "DATETIME",
        },
        "organizations": {
            "name": "VARCHAR",
            "alternative_name": "VARCHAR",
            "image_path": "VARCHAR",
            "status": "VARCHAR",
            "emirate": "VARCHAR",
            "founder": "VARCHAR",
            "headquarters": "VARCHAR",
            "tags": "VARCHAR",
            "created_at": "DATETIME",
            "updated_at": "DATETIME",
        },
        "positions": {
            "department": "VARCHAR",
            "role_type": "VARCHAR",
            "source_type": "VARCHAR",
            "source_title": "VARCHAR",
            "source_url": "VARCHAR",
            "confidence": "VARCHAR",
            "privacy_level": "VARCHAR",
            "created_at": "DATETIME",
            "updated_at": "DATETIME",
        },
        "relationships": {
            "source_type": "VARCHAR",
            "source_title": "VARCHAR",
            "source_url": "VARCHAR",
            "confidence": "VARCHAR",
            "privacy_level": "VARCHAR",
            "created_at": "DATETIME",
        },
        "notes": {
            "source_type": "VARCHAR",
            "source_title": "VARCHAR",
            "source_url": "VARCHAR",
            "confidence": "VARCHAR",
            "privacy_level": "VARCHAR",
            "updated_at": "DATETIME",
        },
        "organization_relationships": {
            "source_type": "VARCHAR",
            "source_title": "VARCHAR",
            "source_url": "VARCHAR",
            "confidence": "VARCHAR",
            "privacy_level": "VARCHAR",
        },
        "sources": {},
        "education": {
            "source_type": "VARCHAR",
            "source_title": "VARCHAR",
            "source_url": "VARCHAR",
            "confidence": "VARCHAR",
            "privacy_level": "VARCHAR",
        },
        "setting_options": {
            "category": "VARCHAR",
            "key": "VARCHAR",
            "label_en": "VARCHAR",
            "label_ar": "VARCHAR",
            "icon": "VARCHAR",
            "color": "VARCHAR",
            "sort_order": "INTEGER",
            "is_active": "BOOLEAN",
            "is_system": "BOOLEAN",
            "created_at": "DATETIME",
            "updated_at": "DATETIME",
        },
    }
    now = datetime.utcnow().isoformat(sep=" ", timespec="seconds")
    with engine.begin() as connection:
        inspector = inspect(connection)
        for table, columns in additions.items():
            if table not in inspector.get_table_names():
                continue
            existing = {column["name"] for column in inspector.get_columns(table)}
            for column, column_type in columns.items():
                if column not in existing:
                    connection.execute(text(f"ALTER TABLE {table} ADD COLUMN {column} {column_type}"))

        inspector = inspect(connection)
        if "organizations" in inspector.get_table_names():
            existing = {column["name"] for column in inspector.get_columns("organizations")}
            if {"name", "name_english"}.issubset(existing):
                connection.execute(
                    text("UPDATE organizations SET name = COALESCE(name, name_english) WHERE name IS NULL")
                )
            if {"alternative_name", "name_arabic"}.issubset(existing):
                connection.execute(
                    text(
                        "UPDATE organizations SET alternative_name = COALESCE(alternative_name, name_arabic) "
                        "WHERE alternative_name IS NULL"
                    )
                )
        for table in ["people", "organizations", "positions", "relationships", "notes", "organization_relationships", "sources", "education"]:
            if table not in inspector.get_table_names():
                continue
            existing = {column["name"] for column in inspector.get_columns(table)}
            if "created_at" in existing:
                connection.execute(
                    text(f"UPDATE {table} SET created_at = :now WHERE created_at IS NULL"),
                    {"now": now},
                )
            if "updated_at" in existing:
                connection.execute(
                    text(f"UPDATE {table} SET updated_at = :now WHERE updated_at IS NULL"),
                    {"now": now},
                )


migrate_database()


def seed_setting_options(reset=False):
    from .database import SessionLocal

    db = SessionLocal()
    try:
        if reset:
            db.query(SettingOption).delete()
            db.commit()
        existing = {
            (option.category, option.key): option
            for option in db.query(SettingOption).all()
        }
        for category, options in DEFAULT_SETTING_OPTIONS.items():
            for index, (key, label_en, label_ar, icon, color) in enumerate(options, start=1):
                current = existing.get((category, key))
                if current:
                    if current.is_system:
                        current.label_en = label_en
                        current.label_ar = label_ar
                        current.icon = current.icon or icon
                        current.color = current.color or color
                        current.sort_order = current.sort_order or index
                        current.updated_at = datetime.utcnow()
                    continue
                db.add(
                    SettingOption(
                        category=category,
                        key=key,
                        label_en=label_en,
                        label_ar=label_ar,
                        icon=icon,
                        color=color,
                        sort_order=index,
                        is_active=True,
                        is_system=True,
                    )
                )
        db.commit()
    finally:
        db.close()


seed_setting_options()


def appearance_settings(db):
    saved = {item.key: item.value for item in db.query(AppearanceSetting).all()}
    return {**DEFAULT_APPEARANCE_SETTINGS, **saved}


def font_stack(font_family):
    if not font_family or font_family == "System Default":
        return '"Segoe UI", "Tahoma", "Arial", sans-serif'
    escaped = font_family.replace('"', "")
    return f'"{escaped}", "Segoe UI", "Tahoma", "Arial", sans-serif'


def appearance_css_variables(settings):
    aliases = {
        "primary_color": ["--primary-color", "--accent"],
        "secondary_color": ["--secondary-color", "--accent-2"],
        "accent_color": ["--accent-color", "--focus-color"],
        "app_background": ["--app-bg", "--background-color", "--soft"],
        "card_background": ["--surface-color", "--white"],
        "sidebar_background": ["--sidebar-bg", "--navy"],
        "sidebar_text": ["--sidebar-text"],
        "sidebar_active": ["--sidebar-active"],
        "heading_text": ["--heading-color", "--navy-2"],
        "body_text": ["--body-text", "--body-text-color", "--ink"],
        "muted_text": ["--muted-text", "--muted-text-color", "--muted"],
        "border_color": ["--border-color", "--line"],
        "success_color": ["--success-color"],
        "warning_color": ["--warning-color"],
        "danger_color": ["--danger-color", "--danger"],
    }
    lines = []
    for key, variables in aliases.items():
        for variable in variables:
            lines.append(f"{variable}: {settings.get(key, DEFAULT_APPEARANCE_SETTINGS[key])};")
    lines.extend(
        [
            f"--card-radius: {settings.get('card_radius', '8')}px;",
            f"--button-radius: {settings.get('button_radius', '8')}px;",
            f"--sidebar-width: {settings.get('sidebar_width', '270')}px;",
        ]
    )
    for group, *_ in TEXT_GROUPS:
        lines.append(f"--{group}-font: {font_stack(settings.get(f'{group}_font_family'))};")
        lines.append(f"--{group}-font-size: {settings.get(f'{group}_font_size', '16')}px;")
        lines.append(f"--{group}-font-weight: {settings.get(f'{group}_font_weight', '500')};")
        lines.append(f"--{group}-letter-spacing: {settings.get(f'{group}_letter_spacing', '0')}px;")
    return ":root {\n  " + "\n  ".join(lines) + "\n}"


def validate_appearance_value(key, value):
    value = (value or "").strip()
    color_keys = {field[0] for field in COLOR_FIELDS}
    if key in color_keys:
        if not HEX_COLOR_RE.match(value):
            return None
        return value.upper()
    if key.endswith("_font_family"):
        return value if value in FONT_FAMILIES else DEFAULT_APPEARANCE_SETTINGS.get(key, "System Default")
    if key.endswith("_font_weight"):
        return value if value in FONT_WEIGHTS else DEFAULT_APPEARANCE_SETTINGS.get(key, "500")
    if key.endswith("_font_size") or key.endswith("_letter_spacing") or key in {"card_radius", "button_radius", "sidebar_width"}:
        try:
            number = float(value)
        except ValueError:
            return DEFAULT_APPEARANCE_SETTINGS.get(key, "0")
        limits = {
            "font_size": (10, 48),
            "letter_spacing": (-1, 3),
            "card_radius": (0, 20),
            "button_radius": (0, 20),
            "sidebar_width": (220, 340),
        }
        limit_key = next((name for name in limits if key.endswith(name) or key == name), "font_size")
        low, high = limits[limit_key]
        number = max(low, min(high, number))
        return str(int(number) if number.is_integer() else number)
    return value


def parse_date(value):
    if not value:
        return None
    return datetime.strptime(value, "%Y-%m-%d").date()


def parse_int(value):
    if value in (None, ""):
        return None
    return int(value)


def save_upload(upload: UploadFile | None):
    if not upload or not upload.filename:
        return None
    suffix = Path(upload.filename).suffix.lower()
    if suffix not in {".jpg", ".jpeg", ".png", ".webp"}:
        return None
    filename = f"{uuid4().hex}{suffix}"
    destination = UPLOAD_DIR / filename
    with destination.open("wb") as buffer:
        buffer.write(upload.file.read())
    return f"/static/uploads/{filename}"


def save_source_file(upload: UploadFile | None):
    if not upload or not upload.filename:
        return None
    suffix = Path(upload.filename).suffix.lower()
    allowed = {
        ".jpg",
        ".jpeg",
        ".png",
        ".webp",
        ".pdf",
        ".doc",
        ".docx",
        ".xlsx",
        ".pptx",
        ".txt",
    }
    if suffix not in allowed:
        return None
    filename = f"{uuid4().hex}{suffix}"
    destination = SOURCE_UPLOAD_DIR / filename
    with destination.open("wb") as buffer:
        buffer.write(upload.file.read())
    return f"/static/uploads/sources/{filename}"


def add_sources(
    db,
    note,
    source_types,
    source_titles,
    source_urls,
    source_texts,
    source_notes,
    source_files,
):
    for index, source_type in enumerate(source_types or []):
        if not source_type:
            continue
        source = Source(
            note_id=note.id,
            entity_type=note.entity_type,
            entity_id=note.entity_id,
            source_type=source_type,
            title=(source_titles[index] if index < len(source_titles) else ""),
            url=(source_urls[index] if index < len(source_urls) else ""),
            text_reference=(source_texts[index] if index < len(source_texts) else ""),
            notes=(source_notes[index] if index < len(source_notes) else ""),
            file_path=save_source_file(source_files[index]) if index < len(source_files) else None,
        )
        if source.title or source.url or source.text_reference or source.notes or source.file_path:
            db.add(source)


INPUT_TYPES = [
    "One Person",
    "One Organization",
    "Mixed Information",
    "Note Only",
    "Career / Position Only",
    "Education Only",
    "Relationship Only",
    "Person",
    "Organization",
    "Source",
    "Unknown / Auto Detect",
]
INTAKE_SOURCE_TYPES = [
    "Personal Knowledge",
    "Official Website",
    "News Article",
    "Government Website",
    "Company Website",
    "Document",
    "Screenshot",
    "Social Media",
    "Other",
]
CONFIDENCE_OPTIONS = ["Confirmed", "Likely", "Unverified", "Private", "Outdated", "Unknown"]
PRIVACY_OPTIONS = ["Public Fact", "Private Note", "Sensitive / Do Not Export"]
REVIEW_STATUSES = ["Pending Review", "Approved", "Rejected", "Merged", "Saved as Note"]


def timestamp_slug():
    return datetime.utcnow().strftime("%Y-%m-%d_%H%M")


def safe_filename(name):
    cleaned = re.sub(r"[^A-Za-z0-9_.-]+", "_", name or "file").strip("._")
    return cleaned or "file"


def smart_options(db, category, fallback):
    return get_option_keys(db, category, fallback)


PERSON_TITLE_BLOCKLIST = {
    "Crown Prince",
    "Deputy Crown Prince",
    "President",
    "Chairman",
    "Minister",
    "Director",
    "Armed Forces",
    "Executive Council",
    "Education Council",
    "Bureau",
    "Company",
    "Council",
    "Ministry",
    "Department",
    "Authority",
    "Program",
    "Government",
    "University",
    "School",
    "Office",
}
POSITION_KEYWORDS = [
    "Deputy Supreme Commander",
    "Deputy Crown Prince",
    "Crown Prince",
    "Board Member",
    "Supreme Commander",
    "Chairman",
    "President",
    "Founder",
    "Minister",
    "Director",
    "Advisor",
    "Ruler",
    "CEO",
]
ORGANIZATION_KEYWORDS = [
    "Council",
    "Bureau",
    "Company",
    "Ministry",
    "Department",
    "Authority",
    "Armed Forces",
    "University",
    "School",
    "Foundation",
    "Office",
    "Program",
    "Corporation",
    "Government",
]
MONTHS = {
    "january": 1,
    "february": 2,
    "march": 3,
    "april": 4,
    "may": 5,
    "june": 6,
    "july": 7,
    "august": 8,
    "september": 9,
    "october": 10,
    "november": 11,
    "december": 12,
}


def normalize_input_type(input_type):
    mapping = {
        "Person": "One Person",
        "Organization": "One Organization",
        "Career / Position": "Career / Position Only",
        "Education": "Education Only",
        "Relationship": "Relationship Only",
        "Note": "Note Only",
        "Unknown / Auto Detect": "One Person",
    }
    return mapping.get(input_type or "", input_type or "One Person")


def extract_with_ollama(raw_text, input_type):
    normalized_type = normalize_input_type(input_type)
    if normalized_type in {"One Person", "One Organization"}:
        return None
    payload = {
        "model": "llama3",
        "prompt": (
            "Extract Smart Database intake information as compact JSON with keys people, "
            "organizations, positions, relationships, education, notes, sources, tags, confidence. "
            "For One Person return at most one person and never treat job titles or organizations as people. "
            "Do not invent missing facts. Text:\n" + raw_text
        ),
        "stream": False,
    }
    try:
        request = urllib.request.Request(
            "http://127.0.0.1:11434/api/generate",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=4) as response:
            data = json.loads(response.read().decode("utf-8"))
        match = re.search(r"\{.*\}", data.get("response", ""), re.S)
        return json.loads(match.group(0)) if match else None
    except (urllib.error.URLError, TimeoutError, ValueError, json.JSONDecodeError):
        return None


def split_possible_names(raw_text):
    candidates = re.findall(r"\b[A-Z][a-z]+(?:\s+(?:bin|bint|Al|Al-|[A-Z][a-z]+)){1,4}\b", raw_text)
    blocked = {"United Arab Emirates", "Abu Dhabi", "Ras Al Khaimah", *PERSON_TITLE_BLOCKLIST}
    return list(dict.fromkeys(item.strip() for item in candidates if not is_non_person_phrase(item, blocked)))[:10]


def is_non_person_phrase(value, blocked=None):
    text_value = (value or "").strip()
    if not text_value:
        return True
    lowered = text_value.lower()
    blocked = blocked or PERSON_TITLE_BLOCKLIST
    return any(term.lower() in lowered for term in blocked | set(ORGANIZATION_KEYWORDS))


def parse_textual_date(value):
    if not value:
        return None
    day_month_year = re.search(r"\b(\d{1,2})\s+([A-Z][a-z]+)\s+((?:18|19|20)\d{2})\b", value)
    if day_month_year:
        month = MONTHS.get(day_month_year.group(2).lower())
        if month:
            return f"{day_month_year.group(3)}-{month:02d}-{int(day_month_year.group(1)):02d}"
    month_year = re.search(r"\b([A-Z][a-z]+)\s+((?:18|19|20)\d{2})\b", value)
    if month_year:
        month = MONTHS.get(month_year.group(1).lower())
        if month:
            return f"{month_year.group(2)}-{month:02d}-01"
    return None


def extract_year(value):
    match = re.search(r"\b(?:18|19|20)\d{2}\b", value or "")
    return int(match.group(0)) if match else None


def organization_type_for_name(name):
    lowered = (name or "").lower()
    if "ministry" in lowered:
        return "Ministry"
    if "company" in lowered or "mubadala" in lowered:
        return "Company"
    if "university" in lowered:
        return "University"
    if "school" in lowered:
        return "School"
    if "council" in lowered:
        return "Council"
    if "authority" in lowered:
        return "Government Authority"
    if "department" in lowered:
        return "Government Department"
    if "foundation" in lowered:
        return "Foundation"
    return "Other"


def extract_career_sentence(sentence):
    cleaned = sentence.strip(" .")
    position_pattern = "|".join(re.escape(item) for item in POSITION_KEYWORDS)
    match = re.search(
        rf"\b(?:Became|Appointed|Named|Served as|Was)\s+(?:the\s+)?(?P<title>{position_pattern})\s+(?:of|at|for)\s+(?P<org>.+?)(?:\s+in\s+(?P<date>\d{{1,2}}\s+[A-Z][a-z]+\s+\d{{4}}|[A-Z][a-z]+\s+\d{{4}}|\d{{4}}))?$",
        cleaned,
        re.I,
    )
    if not match:
        return None
    org = re.sub(r"^(the)\s+", "", match.group("org").strip(), flags=re.I)
    org = re.sub(r"\s+on\s+\d{1,2}\s+[A-Z][a-z]+\s+\d{4}$", "", org).strip()
    org = org.strip(" .")
    date_text = match.group("date") or cleaned
    title = " ".join(part.capitalize() if part.lower() not in {"of", "and"} else part.lower() for part in match.group("title").split())
    year = extract_year(date_text)
    return {
        "organization": org,
        "position_title": title,
        "department": "",
        "start_year": year,
        "end_year": "",
        "is_current": True,
        "role_type": title if title in ROLE_TYPES else "Government Role",
        "notes": cleaned,
    }


def extract_organizations_from_text(raw_text, positions):
    names = [position.get("organization", "") for position in positions if position.get("organization")]
    renamed = re.findall(r"renamed as ([A-Z][A-Za-z]*(?:\s+[A-Z][A-Za-z]*){1,6})", raw_text, re.I)
    names.extend(renamed)
    for match in re.finditer(r"\b([A-Z][A-Za-z]*(?:\s+[A-Z][A-Za-z]*){0,6}\s+(?:Council|Bureau|Company|Ministry|Department|Authority|Armed Forces|University|School|Foundation|Office|Program|Corporation|Government))\b", raw_text):
        names.append(match.group(1).strip())
    organizations = []
    seen = set()
    generic_names = {keyword.lower() for keyword in ORGANIZATION_KEYWORDS} | {"the bureau", "the council", "the company"}
    for name in names:
        cleaned = re.sub(r"^the\s+", "", (name or "").strip(" ."), flags=re.I)
        if not cleaned or cleaned.lower() in seen or cleaned.lower() in generic_names:
            continue
        seen.add(cleaned.lower())
        organizations.append({"name": cleaned, "organization_type": organization_type_for_name(cleaned), "emirate": "Federal" if cleaned == "UAE" else "", "notes": ""})
    return organizations


def extract_one_person(raw_text):
    birth_date = ""
    born_match = re.search(r"\bBorn\s+(?:on\s+)?([^.;]+)", raw_text, re.I)
    if born_match:
        birth_date = parse_textual_date(born_match.group(1)) or ""
    explicit_name = re.search(r"(?:^|\b)(?:Sheikh|H\.?H\.?|His Highness|Her Highness)\s+([A-Z][A-Za-z]+(?:\s+[A-Z][A-Za-z]+){1,5})", raw_text)
    name_parts = []
    if explicit_name:
        candidate = explicit_name.group(1)
        if not is_non_person_phrase(candidate):
            name_parts = candidate.split()[:5]
    sentences = [part.strip() for part in re.split(r"(?<=[.;])\s+", raw_text) if part.strip()]
    positions = [entry for entry in (extract_career_sentence(sentence) for sentence in sentences) if entry]
    organizations = extract_organizations_from_text(raw_text, positions)
    person = {
        "first_name": name_parts[0] if len(name_parts) > 0 else "",
        "second_name": name_parts[1] if len(name_parts) > 1 else "",
        "third_name": name_parts[2] if len(name_parts) > 2 else "",
        "fourth_name": name_parts[3] if len(name_parts) > 3 else "",
        "family_name": " ".join(name_parts[4:]) if len(name_parts) > 4 else "",
        "tribe_name": "",
        "gender": "Unknown",
        "nationality": "UAE" if re.search(r"\bUAE\b|United Arab Emirates", raw_text) else "Unknown",
        "status": "Unknown",
        "category": "Government Figure" if positions else "Other",
        "birth_date": birth_date,
        "birth_place": "",
        "tags": ", ".join(tag for tag in ["UAE", "Abu Dhabi", "Government"] if tag.lower() in raw_text.lower()),
    }
    return {
        "people": [person],
        "main_person": person,
        "organizations": organizations,
        "positions": positions,
        "relationships": [],
        "education": [],
        "notes": [{"note_type": "Source Note", "title": "Imported paragraph", "content": raw_text}],
        "sources": [],
        "tags": [tag.strip() for tag in person["tags"].split(",") if tag.strip()],
        "confidence": "Likely" if birth_date or positions else "Unverified",
    }


def extract_one_organization(raw_text):
    organizations = extract_organizations_from_text(raw_text, [])
    organization = organizations[0] if organizations else {"name": "", "organization_type": "Other", "emirate": "", "notes": raw_text[:240]}
    return {
        "people": [],
        "organizations": [organization],
        "main_organization": organization,
        "positions": [],
        "relationships": [],
        "education": [],
        "notes": [{"note_type": "Source Note", "title": "Imported paragraph", "content": raw_text}],
        "sources": [],
        "tags": [],
        "confidence": "Likely" if organization.get("name") else "Unverified",
    }


def extract_information(raw_text, input_type):
    normalized_type = normalize_input_type(input_type)
    if normalized_type == "One Person":
        return extract_one_person(raw_text)
    if normalized_type == "One Organization":
        return extract_one_organization(raw_text)
    if normalized_type == "Note Only":
        return {"people": [], "organizations": [], "positions": [], "relationships": [], "education": [], "notes": [{"note_type": "Source Note", "title": "Imported paragraph", "content": raw_text}], "sources": [], "tags": [], "confidence": "Unknown"}
    ollama = extract_with_ollama(raw_text, input_type)
    if isinstance(ollama, dict):
        if normalized_type == "Mixed Information":
            people = [person for person in ollama.get("people", []) if not is_non_person_phrase(person.get("full_name") or person.get("name") or "")]
        else:
            people = []
        return {
            "people": people,
            "organizations": ollama.get("organizations", []),
            "positions": ollama.get("positions", []),
            "relationships": ollama.get("relationships", []),
            "education": ollama.get("education", []),
            "notes": ollama.get("notes", []),
            "sources": ollama.get("sources", []),
            "tags": ollama.get("tags", []),
            "confidence": ollama.get("confidence", "Unknown"),
        }

    lower = raw_text.lower()
    years = re.findall(r"\b(?:18|19|20)\d{2}\b", raw_text)
    tags = [tag for tag in ["Dubai", "Abu Dhabi", "Sharjah", "government", "ministry", "business", "economy"] if tag.lower() in lower]
    people = [{"full_name": name} for name in split_possible_names(raw_text)] if normalized_type == "Mixed Information" else []
    organization_words = ["ministry", "authority", "department", "council", "company", "holding", "university", "school", "bank", "office"]
    organizations = []
    for sentence in re.split(r"[\n.;]", raw_text):
        if any(word in sentence.lower() for word in organization_words):
            name = sentence.strip(" -:")
            if 3 < len(name) <= 120:
                organizations.append({"name": name})
    role_words = ["founder", "chairman", "ceo", "minister", "director", "board member", "advisor", "president"]
    positions = [{"position_title": word.title(), "years": years[:2]} for word in role_words if word in lower]
    education_words = ["university", "bachelor", "master", "phd", "school", "diploma", "degree"]
    education = [{"text": raw_text[:240], "years": years}] if any(word in lower for word in education_words) else []
    relationship_words = ["father", "mother", "brother", "sister", "wife", "husband", "son", "daughter"]
    relationships = [{"relationship_type": word.title()} for word in relationship_words if word in lower]
    return {
        "people": people,
        "organizations": organizations[:8],
        "positions": positions[:8],
        "relationships": relationships[:8],
        "education": education,
        "notes": [{"content": raw_text[:1000]}] if raw_text.strip() else [],
        "sources": [],
        "tags": tags,
        "confidence": "Unknown",
    }


def extracted_payload(item):
    try:
        return json.loads(item.extracted_json or "{}")
    except json.JSONDecodeError:
        return {}


def profile_name_similarity(left, right):
    return int(SequenceMatcher(None, (left or "").lower(), (right or "").lower()).ratio() * 100)


def find_duplicate_people(db, limit=50):
    people = db.query(Person).order_by(Person.id).all()
    records = []
    for index, left in enumerate(people):
        for right in people[index + 1 :]:
            score = profile_name_similarity(left.display_name, right.display_name)
            matches = []
            if left.family_name and left.family_name == right.family_name:
                score += 8
                matches.append("family name")
            if left.nationality and left.nationality == right.nationality:
                score += 4
                matches.append("nationality")
            if score >= 68:
                records.append({"type": "person", "left": left, "right": right, "score": min(score, 100), "reason": ", ".join(matches) or "similar name"})
    return sorted(records, key=lambda item: item["score"], reverse=True)[:limit]


def find_duplicate_organizations(db, limit=50):
    organizations = db.query(Organization).order_by(Organization.id).all()
    records = []
    for index, left in enumerate(organizations):
        for right in organizations[index + 1 :]:
            names = [left.name, left.alternative_name, right.name, right.alternative_name]
            score = max(profile_name_similarity(names[0], names[2]), profile_name_similarity(names[1], names[2]), profile_name_similarity(names[0], names[3]))
            matches = []
            if left.organization_type and left.organization_type == right.organization_type:
                score += 5
                matches.append("type")
            if left.emirate and left.emirate == right.emirate:
                score += 5
                matches.append("emirate")
            if score >= 68:
                records.append({"type": "organization", "left": left, "right": right, "score": min(score, 100), "reason": ", ".join(matches) or "similar name"})
    return sorted(records, key=lambda item: item["score"], reverse=True)[:limit]


def duplicate_label(score):
    if score >= 85:
        return "High match"
    if score >= 74:
        return "Medium match"
    return "Low match"


def table_rows(db, model, columns):
    rows = []
    for item in db.query(model).all():
        rows.append({column: getattr(item, column, None) for column in columns})
    return rows


def write_csv(path, rows, columns):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in columns})
    return path


def create_backup_zip(db):
    stamp = timestamp_slug()
    backup_path = BACKUP_DIR / f"smart_database_backup_{stamp}.zip"
    counts = {
        "people": db.query(Person).count(),
        "organizations": db.query(Organization).count(),
        "positions": db.query(Position).count(),
        "relationships": db.query(Relationship).count(),
        "education_entries": db.query(Education).count(),
        "notes": db.query(Note).count(),
        "sources": db.query(Source).count(),
        "setting_options": db.query(SettingOption).count(),
    }
    temp_dir = BACKUP_DIR / f"_backup_{stamp}"
    temp_dir.mkdir(parents=True, exist_ok=True)
    csv_specs = {
        "people.csv": (Person, ["id", "first_name", "second_name", "third_name", "fourth_name", "family_name", "tribe_name", "gender", "nationality", "status", "category", "tags"]),
        "organizations.csv": (Organization, ["id", "name", "alternative_name", "organization_type", "status", "emirate", "tags"]),
        "positions.csv": (Position, ["id", "person_id", "organization_id", "position_title", "department", "start_year", "end_year", "is_current", "role_type"]),
        "relationships.csv": (Relationship, ["id", "from_person_id", "to_person_id", "relationship_type", "notes"]),
        "education.csv": (Education, ["id", "person_id", "institution", "degree", "major", "start_year", "end_year", "graduation_year", "country"]),
        "notes.csv": (Note, ["id", "entity_type", "entity_id", "note_type", "title", "content", "date_text", "is_private", "confidence", "privacy_level"]),
        "sources.csv": (Source, ["id", "note_id", "entity_type", "entity_id", "source_type", "title", "url", "file_path"]),
    }
    for filename, (model, columns) in csv_specs.items():
        write_csv(temp_dir / filename, table_rows(db, model, columns), columns)
    (temp_dir / "settings_export.json").write_text(json.dumps(export_settings_payload(db), ensure_ascii=False, indent=2), encoding="utf-8")
    (temp_dir / "backup_info.json").write_text(json.dumps({"backup_date": datetime.utcnow().isoformat(), "app_name": "Smart Database", "counts": counts}, ensure_ascii=False, indent=2), encoding="utf-8")
    if Path("smart_database.db").exists():
        shutil.copy2("smart_database.db", temp_dir / "smart_database.db")
    with zipfile.ZipFile(backup_path, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in temp_dir.rglob("*"):
            archive.write(path, path.relative_to(temp_dir))
        for path in UPLOAD_DIR.rglob("*"):
            if path.is_file():
                archive.write(path, Path("static/uploads") / path.relative_to(UPLOAD_DIR))
    shutil.rmtree(temp_dir, ignore_errors=True)
    db.add(BackupLog(file_path=str(backup_path), backup_type="Full", people_count=counts["people"], organization_count=counts["organizations"], notes_count=counts["notes"]))
    db.commit()
    return backup_path


def export_settings_payload(db):
    return {
        "appearance": appearance_settings(db),
        "options": [
            {
                "category": option.category,
                "key": option.key,
                "label_en": option.label_en,
                "label_ar": option.label_ar,
                "icon": option.icon,
                "color": option.color,
                "sort_order": option.sort_order,
                "is_active": option.is_active,
                "is_system": option.is_system,
            }
            for option in db.query(SettingOption).order_by(SettingOption.category, SettingOption.sort_order).all()
        ]
    }


def get_setting_options(db, category, active_only=True):
    query = db.query(SettingOption).filter(SettingOption.category == category)
    if active_only:
        query = query.filter(SettingOption.is_active == True)
    return query.order_by(SettingOption.sort_order, SettingOption.id).all()


def get_option_keys(db, category, fallback):
    options = get_setting_options(db, category)
    return [option.key for option in options] or fallback


def setting_label_maps(db):
    options = db.query(SettingOption).order_by(SettingOption.sort_order, SettingOption.id).all()
    return {
        "en": {option.key: option.label_en or option.key for option in options},
        "ar": {option.key: option.label_ar or option.label_en or option.key for option in options},
    }


def setting_option_lists(db):
    options = (
        db.query(SettingOption)
        .filter(SettingOption.is_active == True)
        .order_by(SettingOption.sort_order, SettingOption.id)
        .all()
    )
    grouped = {}
    for option in options:
        grouped.setdefault(option.category, []).append(option.key)
    return grouped


def settings_options_by_category(db):
    options = db.query(SettingOption).order_by(SettingOption.sort_order, SettingOption.id).all()
    grouped = {}
    for option in options:
        grouped.setdefault(option.category, []).append(option)
    return grouped


def select_options(db):
    return {
        "genders": get_option_keys(db, "gender", PERSON_GENDERS),
        "nationalities": get_option_keys(db, "nationality", NATIONALITIES),
        "person_statuses": get_option_keys(db, "person_status", PERSON_STATUSES),
        "person_categories": get_option_keys(db, "person_category", PERSON_CATEGORIES),
        "organization_types": get_option_keys(db, "organization_type", ORGANIZATION_TYPES),
        "organization_statuses": get_option_keys(db, "organization_status", ORGANIZATION_STATUSES),
        "emirates": get_option_keys(db, "emirate", EMIRATES),
        "relationship_types": get_option_keys(db, "relationship_type", RELATIONSHIP_TYPES),
        "note_types": get_option_keys(db, "note_type", NOTE_TYPES),
        "organization_relationship_types": get_option_keys(db, "organization_relationship_type", ORGANIZATION_RELATIONSHIP_TYPES),
        "source_types": get_option_keys(db, "source_type", SOURCE_TYPES),
        "role_types": get_option_keys(db, "role_type", ROLE_TYPES),
        "position_title_suggestions": get_option_keys(db, "position_title_suggestion", []),
        "education_degrees": get_option_keys(db, "education_degree", []),
        "countries": get_option_keys(db, "country", []),
        "input_types": smart_options(db, "input_type", INPUT_TYPES),
        "intake_source_types": smart_options(db, "intake_source_type", INTAKE_SOURCE_TYPES),
        "confidence_options": smart_options(db, "confidence", CONFIDENCE_OPTIONS),
        "privacy_options": smart_options(db, "privacy_level", PRIVACY_OPTIONS),
        "review_statuses": smart_options(db, "review_status", REVIEW_STATUSES),
    }


def context(active_page, db=None, **extra):
    data = {"active_page": active_page}
    if db:
        data.update(select_options(db))
        data["setting_labels"] = setting_label_maps(db)
        data["setting_option_lists"] = setting_option_lists(db)
        appearance = appearance_settings(db)
        data["appearance_settings"] = appearance
        data["appearance_css"] = appearance_css_variables(appearance)
    else:
        data.update({
            "genders": PERSON_GENDERS,
            "nationalities": NATIONALITIES,
            "person_statuses": PERSON_STATUSES,
            "person_categories": PERSON_CATEGORIES,
            "organization_types": ORGANIZATION_TYPES,
            "organization_statuses": ORGANIZATION_STATUSES,
            "emirates": EMIRATES,
            "relationship_types": RELATIONSHIP_TYPES,
            "note_types": NOTE_TYPES,
            "organization_relationship_types": ORGANIZATION_RELATIONSHIP_TYPES,
            "source_types": SOURCE_TYPES,
            "role_types": ROLE_TYPES,
            "position_title_suggestions": [],
            "education_degrees": [],
            "countries": [],
            "setting_labels": {"en": {}, "ar": {}},
            "setting_option_lists": {},
            "appearance_settings": DEFAULT_APPEARANCE_SETTINGS,
            "appearance_css": appearance_css_variables(DEFAULT_APPEARANCE_SETTINGS),
        })
    data.update(extra)
    return data


def relationship_group(relationship_type):
    for group, values in RELATIONSHIP_GROUPS.items():
        if relationship_type in values:
            return group
    return "Other"


def gender_label(person, male_label, female_label, unknown_label):
    if person and person.gender == "Male":
        return male_label
    if person and person.gender == "Female":
        return female_label
    return unknown_label


def reverse_relationship_label(relationship, current_person):
    relation = relationship.relationship_type
    if relation in {"Father", "Mother"}:
        return gender_label(current_person, "Son", "Daughter", "Child")
    if relation in {"Son", "Daughter"}:
        return gender_label(current_person, "Father", "Mother", "Parent")
    if relation in {"Brother", "Sister"}:
        return gender_label(current_person, "Brother", "Sister", "Sibling")
    if relation == "Husband":
        return "Wife"
    if relation == "Wife":
        return "Husband"
    symmetric = {
        "Friend",
        "Classmate",
        "Colleague",
        "Business Partner",
        "Cousin",
        "Connected To",
        "Other",
    }
    if relation in symmetric:
        return relation
    reverse = {
        "Grandfather": "Grandson/Granddaughter",
        "Grandmother": "Grandson/Granddaughter",
        "Grandson": "Grandfather/Grandmother",
        "Granddaughter": "Grandfather/Grandmother",
        "Uncle": "Nephew/Niece",
        "Aunt": "Nephew/Niece",
        "Nephew": "Uncle/Aunt",
        "Niece": "Uncle/Aunt",
        "Mentor": "Student",
        "Student": "Mentor",
    }
    return reverse.get(relation, "Connected To")


def person_relationships(person):
    grouped = {"Family": [], "Work / Professional": [], "Social": [], "Other": []}
    for relationship in person.relationships_from:
        grouped[relationship_group(relationship.relationship_type)].append(
            {
                "person": relationship.to_person,
                "id": relationship.id,
                "type": relationship.relationship_type,
                "notes": relationship.notes,
            }
        )
    for relationship in person.relationships_to:
        grouped[relationship_group(relationship.relationship_type)].append(
            {
                "person": relationship.from_person,
                "id": relationship.id,
                "type": reverse_relationship_label(relationship, person),
                "notes": relationship.notes,
            }
        )
    return grouped


def grouped_notes(notes):
    grouped = {}
    for note in notes:
        grouped.setdefault(note.note_type or "General Note", []).append(note)
    return grouped


def organization_relationships(organization):
    items = []
    for relationship in organization.relationships_from:
        items.append(
            {
                "organization": relationship.to_organization,
                "id": relationship.id,
                "type": relationship.relationship_type,
                "notes": relationship.notes,
            }
        )
    reverse_labels = {
        "Parent Organization": "Subsidiary",
        "Subsidiary": "Parent Organization",
        "Replaced By": "Former Name Of",
        "Former Name Of": "Replaced By",
        "Managed By": "Managed By",
        "Partner": "Partner",
        "Merged With": "Merged With",
        "Related Entity": "Related Entity",
        "Government Owner": "Government Owner",
        "Regulator": "Regulator",
        "Other": "Other",
    }
    for relationship in organization.relationships_to:
        items.append(
            {
                "organization": relationship.from_organization,
                "id": relationship.id,
                "type": reverse_labels.get(relationship.relationship_type, "Related Entity"),
                "notes": relationship.notes,
            }
        )
    return items


@app.get("/")
def dashboard(request: Request, db: Session = Depends(get_db)):
    stats = {
        "people": db.query(Person).count(),
        "organizations": db.query(Organization).count(),
        "positions": db.query(Position).count(),
        "relationships": db.query(Relationship).count(),
        "notes": db.query(Note).count(),
        "government_figures": db.query(Person).filter(Person.category == "Government Figure").count(),
        "business_figures": db.query(Person).filter(Person.category == "Business Figure").count(),
        "active_organizations": db.query(Organization).filter(Organization.status == "Active").count(),
    }
    return templates.TemplateResponse(
        request,
        "index.html",
        context(
            "dashboard",
            db=db,
            stats=stats,
            recent_people=db.query(Person).order_by(Person.id.desc()).limit(5).all(),
            recent_organizations=db.query(Organization).order_by(Organization.id.desc()).limit(5).all(),
        ),
    )


@app.get("/people")
def people(
    request: Request,
    gender: str = "",
    nationality: str = "",
    status: str = "",
    category: str = "",
    tribe: str = "",
    family_name: str = "",
    db: Session = Depends(get_db),
):
    query = db.query(Person)
    if gender:
        query = query.filter(Person.gender == gender)
    if nationality:
        query = query.filter(Person.nationality == nationality)
    if status:
        query = query.filter(Person.status == status)
    if category:
        query = query.filter(Person.category == category)
    if tribe:
        query = query.filter(Person.tribe_name.ilike(f"%{tribe}%"))
    if family_name:
        query = query.filter(Person.family_name.ilike(f"%{family_name}%"))
    return templates.TemplateResponse(
        request,
        "people.html",
        context(
            "people",
            db=db,
            people=query.order_by(Person.id.desc()).all(),
            filters={
                "gender": gender,
                "nationality": nationality,
                "status": status,
                "category": category,
                "tribe": tribe,
                "family_name": family_name,
            },
        ),
    )


@app.get("/people/add")
def add_person_page(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse(request, "add_person.html", context("add_person", db=db))


@app.post("/people/add")
def add_person(
    first_name: str = Form(...),
    second_name: str = Form(""),
    third_name: str = Form(""),
    fourth_name: str = Form(""),
    family_name: str = Form(""),
    tribe_name: str = Form(""),
    gender: str = Form("Unknown"),
    nationality: str = Form("Unknown"),
    status: str = Form("Unknown"),
    category: str = Form("Other"),
    birth_date: str = Form(""),
    birth_place: str = Form(""),
    education: str = Form(""),
    university: str = Form(""),
    major: str = Form(""),
    graduation_year: str = Form(""),
    current_role: str = Form(""),
    main_field: str = Form(""),
    tags: str = Form(""),
    image: UploadFile = File(None),
    db: Session = Depends(get_db),
):
    person = Person(
        first_name=first_name,
        second_name=second_name,
        third_name=third_name,
        fourth_name=fourth_name,
        family_name=family_name,
        tribe_name=tribe_name,
        image_path=save_upload(image),
        gender=gender,
        nationality=nationality,
        status=status,
        category=category,
        birth_date=parse_date(birth_date),
        birth_place=birth_place,
        education=education,
        university=university,
        major=major,
        graduation_year=parse_int(graduation_year),
        current_role=current_role,
        main_field=main_field,
        tags=tags,
    )
    db.add(person)
    db.commit()
    db.refresh(person)
    return RedirectResponse(url=f"/people/{person.id}", status_code=303)


@app.get("/people/{person_id}")
def person_detail(person_id: int, request: Request, db: Session = Depends(get_db)):
    person = db.query(Person).filter(Person.id == person_id).first()
    if not person:
        return RedirectResponse(url="/people", status_code=303)
    positions = sorted(
        person.positions,
        key=lambda position: (position.start_year or 0, position.id or 0),
        reverse=True,
    )
    current_positions = [position for position in positions if position.is_current or not position.end_year]
    previous_positions = [position for position in positions if position not in current_positions]
    linked_organizations = []
    seen = set()
    for position in positions:
        if position.organization_id not in seen:
            linked_organizations.append(position.organization)
            seen.add(position.organization_id)
    return templates.TemplateResponse(
        request,
        "person_detail.html",
        context(
            "people",
            db=db,
            person=person,
            people=db.query(Person).order_by(Person.first_name, Person.family_name).all(),
            organizations=db.query(Organization).order_by(Organization.name).all(),
            relationships=person_relationships(person),
            positions=positions,
            current_positions=current_positions,
            previous_positions=previous_positions,
            linked_organizations=linked_organizations,
            education_entries=db.query(Education)
            .filter(Education.person_id == person.id)
            .order_by(Education.start_year.desc(), Education.id.desc())
            .all(),
            notes=grouped_notes(
                db.query(Note)
                .filter(Note.entity_type == "person", Note.entity_id == person.id)
                .order_by(Note.id.desc())
                .all()
            ),
        ),
    )


@app.get("/people/{person_id}/edit")
def edit_person_page(person_id: int, request: Request, db: Session = Depends(get_db)):
    person = db.query(Person).filter(Person.id == person_id).first()
    if not person:
        return RedirectResponse(url="/people", status_code=303)
    return templates.TemplateResponse(
        request, "edit_person.html", context("people", db=db, person=person)
    )


@app.post("/people/{person_id}/edit")
def edit_person(
    person_id: int,
    first_name: str = Form(...),
    second_name: str = Form(""),
    third_name: str = Form(""),
    fourth_name: str = Form(""),
    family_name: str = Form(""),
    tribe_name: str = Form(""),
    gender: str = Form("Unknown"),
    nationality: str = Form("Unknown"),
    status: str = Form("Unknown"),
    category: str = Form("Other"),
    birth_date: str = Form(""),
    birth_place: str = Form(""),
    tags: str = Form(""),
    image: UploadFile = File(None),
    db: Session = Depends(get_db),
):
    person = db.query(Person).filter(Person.id == person_id).first()
    if not person:
        return RedirectResponse(url="/people", status_code=303)
    person.first_name = first_name
    person.second_name = second_name
    person.third_name = third_name
    person.fourth_name = fourth_name
    person.family_name = family_name
    person.tribe_name = tribe_name
    person.gender = gender
    person.nationality = nationality
    person.status = status
    person.category = category
    person.birth_date = parse_date(birth_date)
    person.birth_place = birth_place
    person.tags = tags
    new_image = save_upload(image)
    if new_image:
        person.image_path = new_image
    person.updated_at = datetime.utcnow()
    db.commit()
    return RedirectResponse(url=f"/people/{person.id}", status_code=303)


@app.post("/people/{person_id}/delete")
def delete_person(person_id: int, db: Session = Depends(get_db)):
    person = db.query(Person).filter(Person.id == person_id).first()
    if not person:
        return RedirectResponse(url="/people", status_code=303)
    try:
        for source in db.query(Source).filter(Source.entity_type == "person", Source.entity_id == person.id).all():
            db.delete(source)
        for note in db.query(Note).filter(Note.entity_type == "person", Note.entity_id == person.id).all():
            for source in list(note.sources):
                db.delete(source)
            db.delete(note)
        if Education:
            db.query(Education).filter(Education.person_id == person.id).delete(synchronize_session=False)
        if Position:
            db.query(Position).filter(Position.person_id == person.id).delete(synchronize_session=False)
        if Relationship:
            db.query(Relationship).filter(
                or_(Relationship.from_person_id == person.id, Relationship.to_person_id == person.id)
            ).delete(synchronize_session=False)
        db.delete(person)
        db.commit()
    except Exception:
        db.rollback()
    return RedirectResponse(url="/people", status_code=303)


@app.get("/organizations")
def organizations(
    request: Request,
    organization_type: str = "",
    status: str = "",
    emirate: str = "",
    db: Session = Depends(get_db),
):
    query = db.query(Organization)
    if organization_type:
        query = query.filter(Organization.organization_type == organization_type)
    if status:
        query = query.filter(Organization.status == status)
    if emirate:
        query = query.filter(Organization.emirate == emirate)
    return templates.TemplateResponse(
        request,
        "organizations.html",
        context(
            "organizations",
            db=db,
            organizations=query.order_by(Organization.id.desc()).all(),
            filters={"organization_type": organization_type, "status": status, "emirate": emirate},
        ),
    )


@app.get("/organizations/add")
def add_organization_page(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse(request, "add_organization.html", context("add_organization", db=db))


@app.post("/organizations/add")
def add_organization(
    name: str = Form(...),
    alternative_name: str = Form(""),
    organization_type: str = Form("Other"),
    status: str = Form("Unknown"),
    emirate: str = Form("Unknown"),
    founded_year: str = Form(""),
    founder: str = Form(""),
    headquarters: str = Form(""),
    description: str = Form(""),
    tags: str = Form(""),
    image: UploadFile = File(None),
    db: Session = Depends(get_db),
):
    organization = Organization(
        name=name,
        alternative_name=alternative_name,
        image_path=save_upload(image),
        organization_type=organization_type,
        status=status,
        emirate=emirate,
        founded_year=parse_int(founded_year),
        founder=founder,
        headquarters=headquarters,
        description=description,
        tags=tags,
    )
    db.add(organization)
    db.commit()
    db.refresh(organization)
    return RedirectResponse(url=f"/organizations/{organization.id}", status_code=303)


@app.get("/organizations/{organization_id}")
def organization_detail(organization_id: int, request: Request, db: Session = Depends(get_db)):
    organization = db.query(Organization).filter(Organization.id == organization_id).first()
    if not organization:
        return RedirectResponse(url="/organizations", status_code=303)
    positions = sorted(
        organization.positions,
        key=lambda position: (position.start_year or 0, position.id or 0),
        reverse=True,
    )
    return templates.TemplateResponse(
        request,
        "organization_detail.html",
        context(
            "organizations",
            db=db,
            organization=organization,
            people=db.query(Person).order_by(Person.first_name, Person.family_name).all(),
            organizations=db.query(Organization).order_by(Organization.name).all(),
            current_positions=[position for position in positions if position.is_current or not position.end_year],
            previous_positions=[position for position in positions if not (position.is_current or not position.end_year)],
            positions=positions,
            notes=grouped_notes(
                db.query(Note)
                .filter(Note.entity_type == "organization", Note.entity_id == organization.id)
                .order_by(Note.id.desc())
                .all()
            ),
            organization_relationships=organization_relationships(organization),
        ),
    )


@app.get("/organizations/{organization_id}/edit")
def edit_organization_page(
    organization_id: int, request: Request, db: Session = Depends(get_db)
):
    organization = db.query(Organization).filter(Organization.id == organization_id).first()
    if not organization:
        return RedirectResponse(url="/organizations", status_code=303)
    return templates.TemplateResponse(
        request, "edit_organization.html", context("organizations", db=db, organization=organization)
    )


@app.post("/organizations/{organization_id}/edit")
def edit_organization(
    organization_id: int,
    name: str = Form(...),
    alternative_name: str = Form(""),
    organization_type: str = Form("Other"),
    status: str = Form("Unknown"),
    emirate: str = Form("Unknown"),
    founded_year: str = Form(""),
    founder: str = Form(""),
    headquarters: str = Form(""),
    description: str = Form(""),
    tags: str = Form(""),
    image: UploadFile = File(None),
    db: Session = Depends(get_db),
):
    organization = db.query(Organization).filter(Organization.id == organization_id).first()
    if not organization:
        return RedirectResponse(url="/organizations", status_code=303)
    organization.name = name
    organization.alternative_name = alternative_name
    organization.organization_type = organization_type
    organization.status = status
    organization.emirate = emirate
    organization.founded_year = parse_int(founded_year)
    organization.founder = founder
    organization.headquarters = headquarters
    organization.description = description
    organization.tags = tags
    new_image = save_upload(image)
    if new_image:
        organization.image_path = new_image
    organization.updated_at = datetime.utcnow()
    db.commit()
    return RedirectResponse(url=f"/organizations/{organization.id}", status_code=303)


@app.post("/organizations/{organization_id}/delete")
def delete_organization(organization_id: int, db: Session = Depends(get_db)):
    organization = db.query(Organization).filter(Organization.id == organization_id).first()
    if not organization:
        return RedirectResponse(url="/organizations", status_code=303)
    try:
        for source in db.query(Source).filter(Source.entity_type == "organization", Source.entity_id == organization.id).all():
            db.delete(source)
        for note in db.query(Note).filter(Note.entity_type == "organization", Note.entity_id == organization.id).all():
            for source in list(note.sources):
                db.delete(source)
            db.delete(note)
        if Position:
            db.query(Position).filter(Position.organization_id == organization.id).delete(synchronize_session=False)
        if OrganizationRelationship:
            db.query(OrganizationRelationship).filter(
                or_(
                    OrganizationRelationship.from_organization_id == organization.id,
                    OrganizationRelationship.to_organization_id == organization.id,
                )
            ).delete(synchronize_session=False)
        db.delete(organization)
        db.commit()
    except Exception:
        db.rollback()
    return RedirectResponse(url="/organizations", status_code=303)


@app.post("/relationships/add")
def add_relationship(
    from_person_id: int = Form(...),
    relationship_type: str = Form(...),
    to_person_id: int = Form(...),
    notes: str = Form(""),
    return_to: str = Form("/people"),
    db: Session = Depends(get_db),
):
    if from_person_id != to_person_id:
        db.add(
            Relationship(
                from_person_id=from_person_id,
                to_person_id=to_person_id,
                relationship_type=relationship_type,
                notes=notes,
            )
        )
        db.commit()
    return RedirectResponse(url=return_to, status_code=303)


@app.post("/people/{person_id}/relationships/add")
def add_person_relationship(
    person_id: int,
    to_person_id: int = Form(...),
    relationship_type: str = Form(...),
    notes: str = Form(""),
    db: Session = Depends(get_db),
):
    if person_id != to_person_id:
        db.add(
            Relationship(
                from_person_id=person_id,
                to_person_id=to_person_id,
                relationship_type=relationship_type,
                notes=notes,
            )
        )
        db.commit()
    return RedirectResponse(url=f"/people/{person_id}", status_code=303)


@app.post("/positions/add")
def add_position(
    person_id: int = Form(...),
    organization_id: int = Form(...),
    position_title: str = Form(...),
    department: str = Form(""),
    start_year: str = Form(""),
    end_year: str = Form(""),
    is_current: str = Form(""),
    role_type: str = Form("Other"),
    notes: str = Form(""),
    return_to: str = Form("/people"),
    db: Session = Depends(get_db),
):
    db.add(
        Position(
            person_id=person_id,
            organization_id=organization_id,
            position_title=position_title,
            department=department,
            start_year=parse_int(start_year),
            end_year=parse_int(end_year),
            is_current=is_current == "yes",
            role_type=role_type,
            notes=notes,
        )
    )
    db.commit()
    return RedirectResponse(url=return_to, status_code=303)


@app.post("/people/{person_id}/positions/add")
def add_person_position(
    person_id: int,
    organization_id: int = Form(...),
    position_title: str = Form(...),
    department: str = Form(""),
    start_year: str = Form(""),
    end_year: str = Form(""),
    is_current: str = Form(""),
    role_type: str = Form("Other"),
    notes: str = Form(""),
    db: Session = Depends(get_db),
):
    db.add(
        Position(
            person_id=person_id,
            organization_id=organization_id,
            position_title=position_title,
            department=department,
            start_year=parse_int(start_year),
            end_year=parse_int(end_year),
            is_current=is_current == "yes",
            role_type=role_type,
            notes=notes,
        )
    )
    db.commit()
    return RedirectResponse(url=f"/people/{person_id}", status_code=303)


@app.post("/people/{person_id}/education/add")
def add_person_education(
    person_id: int,
    institution: str = Form(...),
    degree: str = Form(""),
    major: str = Form(""),
    start_year: str = Form(""),
    end_year: str = Form(""),
    graduation_year: str = Form(""),
    country: str = Form(""),
    notes: str = Form(""),
    db: Session = Depends(get_db),
):
    db.add(
        Education(
            person_id=person_id,
            institution=institution,
            degree=degree,
            major=major,
            start_year=parse_int(start_year),
            end_year=parse_int(end_year),
            graduation_year=parse_int(graduation_year),
            country=country,
            notes=notes,
        )
    )
    db.commit()
    return RedirectResponse(url=f"/people/{person_id}", status_code=303)


@app.post("/organizations/{organization_id}/positions/add")
def add_organization_position(
    organization_id: int,
    person_id: int = Form(...),
    position_title: str = Form(...),
    department: str = Form(""),
    start_year: str = Form(""),
    end_year: str = Form(""),
    is_current: str = Form(""),
    role_type: str = Form("Other"),
    notes: str = Form(""),
    db: Session = Depends(get_db),
):
    db.add(
        Position(
            person_id=person_id,
            organization_id=organization_id,
            position_title=position_title,
            department=department,
            start_year=parse_int(start_year),
            end_year=parse_int(end_year),
            is_current=is_current == "yes",
            role_type=role_type,
            notes=notes,
        )
    )
    db.commit()
    return RedirectResponse(url=f"/organizations/{organization_id}", status_code=303)


@app.post("/people/{person_id}/notes/add")
def add_person_note(
    person_id: int,
    note_type: str = Form("General Note"),
    title: str = Form(""),
    content: str = Form(...),
    date_text: str = Form(""),
    is_private: str = Form(""),
    source_type: list[str] = Form([]),
    source_title: list[str] = Form([]),
    source_url: list[str] = Form([]),
    source_text_reference: list[str] = Form([]),
    source_notes: list[str] = Form([]),
    source_file: list[UploadFile] = File([]),
    db: Session = Depends(get_db),
):
    note = Note(
        entity_type="person",
        entity_id=person_id,
        note_type=note_type,
        title=title,
        content=content,
        date_text=date_text,
        is_private=is_private == "yes",
    )
    db.add(note)
    db.flush()
    add_sources(db, note, source_type, source_title, source_url, source_text_reference, source_notes, source_file)
    db.commit()
    return RedirectResponse(url=f"/people/{person_id}", status_code=303)


@app.post("/organizations/{organization_id}/notes/add")
def add_organization_note(
    organization_id: int,
    note_type: str = Form("General Note"),
    title: str = Form(""),
    content: str = Form(...),
    date_text: str = Form(""),
    is_private: str = Form(""),
    source_type: list[str] = Form([]),
    source_title: list[str] = Form([]),
    source_url: list[str] = Form([]),
    source_text_reference: list[str] = Form([]),
    source_notes: list[str] = Form([]),
    source_file: list[UploadFile] = File([]),
    db: Session = Depends(get_db),
):
    note = Note(
        entity_type="organization",
        entity_id=organization_id,
        note_type=note_type,
        title=title,
        content=content,
        date_text=date_text,
        is_private=is_private == "yes",
    )
    db.add(note)
    db.flush()
    add_sources(db, note, source_type, source_title, source_url, source_text_reference, source_notes, source_file)
    db.commit()
    return RedirectResponse(url=f"/organizations/{organization_id}", status_code=303)


@app.post("/organizations/{organization_id}/relationships/add")
def add_organization_relationship(
    organization_id: int,
    to_organization_id: int = Form(...),
    relationship_type: str = Form(...),
    notes: str = Form(""),
    db: Session = Depends(get_db),
):
    if organization_id != to_organization_id:
        db.add(
            OrganizationRelationship(
                from_organization_id=organization_id,
                to_organization_id=to_organization_id,
                relationship_type=relationship_type,
                notes=notes,
            )
        )
        db.commit()
    return RedirectResponse(url=f"/organizations/{organization_id}", status_code=303)


@app.post("/notes/{note_id}/delete")
def delete_note(note_id: int, return_to: str = Form("/"), db: Session = Depends(get_db)):
    note = db.query(Note).filter(Note.id == note_id).first()
    if note:
        for source in db.query(Source).filter(Source.note_id == note.id).all():
            db.delete(source)
        db.delete(note)
        db.commit()
    return RedirectResponse(url=return_to, status_code=303)


@app.post("/sources/{source_id}/delete")
def delete_source(source_id: int, return_to: str = Form("/"), db: Session = Depends(get_db)):
    source = db.query(Source).filter(Source.id == source_id).first()
    if source:
        db.delete(source)
        db.commit()
    return RedirectResponse(url=return_to, status_code=303)


@app.post("/relationships/{relationship_id}/delete")
def delete_relationship(
    relationship_id: int, return_to: str = Form("/"), db: Session = Depends(get_db)
):
    relationship = db.query(Relationship).filter(Relationship.id == relationship_id).first()
    if relationship:
        db.delete(relationship)
        db.commit()
    return RedirectResponse(url=return_to, status_code=303)


@app.post("/positions/{position_id}/delete")
def delete_position(position_id: int, return_to: str = Form("/"), db: Session = Depends(get_db)):
    position = db.query(Position).filter(Position.id == position_id).first()
    if position:
        db.delete(position)
        db.commit()
    return RedirectResponse(url=return_to, status_code=303)


@app.post("/education/{education_id}/delete")
def delete_education(
    education_id: int, return_to: str = Form("/"), db: Session = Depends(get_db)
):
    education = db.query(Education).filter(Education.id == education_id).first()
    if education:
        db.delete(education)
        db.commit()
    return RedirectResponse(url=return_to, status_code=303)


@app.post("/organization-relationships/{relationship_id}/delete")
def delete_organization_relationship(
    relationship_id: int, return_to: str = Form("/"), db: Session = Depends(get_db)
):
    relationship = (
        db.query(OrganizationRelationship)
        .filter(OrganizationRelationship.id == relationship_id)
        .first()
    )
    if relationship:
        db.delete(relationship)
        db.commit()
    return RedirectResponse(url=return_to, status_code=303)


@app.get("/smart-add")
def smart_add_page(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse(request, "smart_add.html", context("smart_add", db=db))


@app.post("/smart-add/analyze")
def smart_add_analyze(
    raw_text: str = Form(...),
    input_type: str = Form("Unknown / Auto Detect"),
    source_type: str = Form("Personal Knowledge"),
    source_title: str = Form(""),
    source_url: str = Form(""),
    confidence: str = Form("Unknown"),
    privacy_level: str = Form("Public Fact"),
    db: Session = Depends(get_db),
):
    extracted = extract_information(raw_text, input_type)
    extracted["confidence"] = confidence or extracted.get("confidence") or "Unknown"
    item = ExtractedItem(
        raw_text=raw_text,
        input_type=input_type,
        extracted_json=json.dumps(extracted, ensure_ascii=False),
        source_type=source_type,
        source_title=source_title,
        source_url=source_url,
        confidence=confidence,
        privacy_level=privacy_level,
        status="Pending Review",
        duplicate_status="Not Checked",
    )
    db.add(item)
    db.commit()
    return RedirectResponse(url=f"/review/{item.id}", status_code=303)


@app.get("/review")
def review_queue(request: Request, db: Session = Depends(get_db)):
    items = db.query(ExtractedItem).order_by(ExtractedItem.created_at.desc()).all()
    grouped = {status: [] for status in REVIEW_STATUSES}
    for item in items:
        grouped.setdefault(item.status or "Pending Review", []).append(item)
    return templates.TemplateResponse(
        request,
        "review.html",
        context("review", db=db, grouped_items=grouped, extracted_payload=extracted_payload),
    )


@app.get("/review/{item_id}")
def review_detail(item_id: int, request: Request, db: Session = Depends(get_db)):
    item = db.query(ExtractedItem).filter(ExtractedItem.id == item_id).first()
    if not item:
        return RedirectResponse(url="/review", status_code=303)
    possible_people = find_duplicate_people(db, 8)
    possible_organizations = find_duplicate_organizations(db, 8)
    return templates.TemplateResponse(
        request,
        "review_detail.html",
        context(
            "review",
            db=db,
            item=item,
            payload=extracted_payload(item),
            possible_people=possible_people,
            possible_organizations=possible_organizations,
            duplicate_label=duplicate_label,
        ),
    )


@app.post("/review/{item_id}/approve")
async def approve_extracted_item(item_id: int, request: Request, db: Session = Depends(get_db)):
    item = db.query(ExtractedItem).filter(ExtractedItem.id == item_id).first()
    if not item:
        return RedirectResponse(url="/review", status_code=303)
    form = await request.form()
    payload = extracted_payload(item)
    normalized_type = normalize_input_type(item.input_type)

    if normalized_type == "One Organization":
        organization = Organization(
            name=(form.get("organization_name") or "").strip(),
            organization_type=form.get("organization_type") or "Other",
            status="Unknown",
            emirate=form.get("organization_emirate") or "Unknown",
            notes=form.get("organization_notes") or "",
        )
        if organization.name:
            db.add(organization)
            db.flush()
            note = Note(
                entity_type="organization",
                entity_id=organization.id,
                note_type=form.get("note_type") or "Source Note",
                title=form.get("note_title") or "Imported paragraph",
                content=form.get("note_content") or item.raw_text,
                source_type=form.get("source_type") or item.source_type,
                source_title=form.get("source_title") or item.source_title,
                source_url=form.get("source_url") or item.source_url,
                confidence=form.get("note_confidence") or item.confidence,
                privacy_level=form.get("privacy_level") or item.privacy_level,
                is_private=(form.get("privacy_level") or item.privacy_level) != "Public Fact",
            )
            db.add(note)
        item.status = "Approved"
        item.reviewed_at = datetime.utcnow()
        db.commit()
        return RedirectResponse(url=f"/review/{item.id}", status_code=303)

    if normalized_type == "Mixed Information":
        for index, person_data in enumerate(payload.get("people", [])):
            if form.get(f"create_person_{index}") != "yes":
                continue
            name = (person_data.get("full_name") or person_data.get("name") or "").strip()
            if not name or is_non_person_phrase(name):
                continue
            parts = name.split()
            db.add(Person(first_name=parts[0], second_name=parts[1] if len(parts) > 1 else "", third_name=parts[2] if len(parts) > 2 else "", family_name=" ".join(parts[3:]) if len(parts) > 3 else "", category="Other", status="Unknown"))
        for index, org_data in enumerate(payload.get("organizations", [])):
            if form.get(f"create_organization_{index}") != "yes":
                continue
            name = (org_data.get("name") or "").strip()
            if name:
                db.add(Organization(name=name, organization_type=org_data.get("organization_type") or "Other", status="Unknown", emirate=org_data.get("emirate") or "Unknown"))
        item.status = "Approved"
        item.reviewed_at = datetime.utcnow()
        db.commit()
        return RedirectResponse(url=f"/review/{item.id}", status_code=303)

    person = Person(
        first_name=(form.get("first_name") or "").strip(),
        second_name=(form.get("second_name") or "").strip(),
        third_name=(form.get("third_name") or "").strip(),
        fourth_name=(form.get("fourth_name") or "").strip(),
        family_name=(form.get("family_name") or "").strip(),
        tribe_name=(form.get("tribe_name") or "").strip(),
        gender=form.get("gender") or "Unknown",
        nationality=form.get("nationality") or "Unknown",
        status=form.get("status") or "Unknown",
        category=form.get("category") or "Other",
        birth_date=parse_date(form.get("birth_date") or ""),
        birth_place=form.get("birth_place") or "",
        tags=form.get("tags") or "",
    )
    if person.first_name or person.family_name:
        db.add(person)
        db.flush()
        orgs_by_index = {}
        for index, _org_data in enumerate(payload.get("organizations", [])):
            action = form.get(f"organization_action_{index}") or "ignore"
            org_name = (form.get(f"organization_name_{index}") or "").strip()
            if action == "existing":
                existing_id = parse_int(form.get(f"organization_existing_id_{index}") or "")
                existing = db.query(Organization).filter(Organization.id == existing_id).first() if existing_id else None
                if existing:
                    orgs_by_index[index] = existing
            elif action == "create" and org_name:
                existing = db.query(Organization).filter(Organization.name.ilike(org_name)).first()
                if existing:
                    orgs_by_index[index] = existing
                else:
                    org = Organization(
                        name=org_name,
                        organization_type=form.get(f"organization_type_{index}") or "Other",
                        status="Unknown",
                        emirate=form.get(f"organization_emirate_{index}") or "Unknown",
                        notes=form.get(f"organization_notes_{index}") or "",
                    )
                    db.add(org)
                    db.flush()
                    orgs_by_index[index] = org
        for index, position_data in enumerate(payload.get("positions", [])):
            if form.get(f"position_create_{index}") != "yes":
                continue
            org_name = (form.get(f"position_organization_{index}") or position_data.get("organization") or "").strip()
            organization = next((org for org in orgs_by_index.values() if org.display_name.lower() == org_name.lower()), None)
            if not organization and org_name:
                organization = db.query(Organization).filter(Organization.name.ilike(org_name)).first()
            if not organization and org_name:
                organization = Organization(name=org_name, organization_type=organization_type_for_name(org_name), status="Unknown", emirate="Unknown")
                db.add(organization)
                db.flush()
            if organization and (form.get(f"position_title_{index}") or "").strip():
                db.add(Position(
                    person_id=person.id,
                    organization_id=organization.id,
                    position_title=(form.get(f"position_title_{index}") or "").strip(),
                    department=form.get(f"position_department_{index}") or "",
                    start_year=parse_int(form.get(f"position_start_year_{index}") or ""),
                    end_year=parse_int(form.get(f"position_end_year_{index}") or ""),
                    is_current=form.get(f"position_is_current_{index}") == "yes",
                    role_type=form.get(f"position_role_type_{index}") or "Other",
                    notes=form.get(f"position_notes_{index}") or "",
                    source_type=form.get("source_type") or item.source_type,
                    source_title=form.get("source_title") or item.source_title,
                    source_url=form.get("source_url") or item.source_url,
                    confidence=form.get("note_confidence") or item.confidence,
                    privacy_level=form.get("privacy_level") or item.privacy_level,
                ))
        for index, _education_data in enumerate(payload.get("education", [])):
            if form.get(f"education_create_{index}") != "yes":
                continue
            institution = (form.get(f"education_institution_{index}") or "").strip()
            if institution:
                db.add(Education(
                    person_id=person.id,
                    institution=institution,
                    degree=form.get(f"education_degree_{index}") or "",
                    major=form.get(f"education_major_{index}") or "",
                    start_year=parse_int(form.get(f"education_start_year_{index}") or ""),
                    end_year=parse_int(form.get(f"education_end_year_{index}") or ""),
                    graduation_year=parse_int(form.get(f"education_graduation_year_{index}") or ""),
                    country=form.get(f"education_country_{index}") or "",
                    notes=form.get(f"education_notes_{index}") or "",
                    confidence=form.get("note_confidence") or item.confidence,
                    privacy_level=form.get("privacy_level") or item.privacy_level,
                ))
        note = Note(
            entity_type="person",
            entity_id=person.id,
            note_type=form.get("note_type") or "Source Note",
            title=form.get("note_title") or "Imported paragraph",
            content=form.get("note_content") or item.raw_text,
            source_type=form.get("source_type") or item.source_type,
            source_title=form.get("source_title") or item.source_title,
            source_url=form.get("source_url") or item.source_url,
            confidence=form.get("note_confidence") or item.confidence,
            privacy_level=form.get("privacy_level") or item.privacy_level,
            is_private=(form.get("privacy_level") or item.privacy_level) != "Public Fact",
        )
        db.add(note)
    item.status = "Approved"
    item.reviewed_at = datetime.utcnow()
    db.commit()
    return RedirectResponse(url=f"/review/{item.id}", status_code=303)


@app.post("/review/{item_id}/reject")
def reject_extracted_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(ExtractedItem).filter(ExtractedItem.id == item_id).first()
    if item:
        item.status = "Rejected"
        item.reviewed_at = datetime.utcnow()
        db.commit()
    return RedirectResponse(url="/review", status_code=303)


@app.post("/review/{item_id}/save-note")
def save_extracted_as_note(item_id: int, db: Session = Depends(get_db)):
    item = db.query(ExtractedItem).filter(ExtractedItem.id == item_id).first()
    if item:
        db.add(Note(entity_type="extracted_item", entity_id=item.id, note_type="Source Note", title=item.source_title or "Extracted intake", content=item.raw_text, source_type=item.source_type, source_title=item.source_title, source_url=item.source_url, confidence=item.confidence, privacy_level=item.privacy_level, is_private=item.privacy_level != "Public Fact"))
        item.status = "Saved as Note"
        item.reviewed_at = datetime.utcnow()
        db.commit()
    return RedirectResponse(url=f"/review/{item_id}", status_code=303)


@app.post("/review/{item_id}/delete")
def delete_extracted_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(ExtractedItem).filter(ExtractedItem.id == item_id).first()
    if item:
        db.delete(item)
        db.commit()
    return RedirectResponse(url="/review", status_code=303)


@app.post("/review/{item_id}/check-duplicates")
def check_extracted_duplicates(item_id: int, db: Session = Depends(get_db)):
    item = db.query(ExtractedItem).filter(ExtractedItem.id == item_id).first()
    if item:
        item.duplicate_status = "Possible Duplicate" if find_duplicate_people(db, 1) or find_duplicate_organizations(db, 1) else "No Duplicate"
        db.commit()
    return RedirectResponse(url=f"/review/{item_id}", status_code=303)


@app.post("/review/{item_id}/merge")
def merge_extracted_placeholder(item_id: int, db: Session = Depends(get_db)):
    item = db.query(ExtractedItem).filter(ExtractedItem.id == item_id).first()
    if item:
        item.status = "Merged"
        item.duplicate_status = "Merged"
        item.reviewed_at = datetime.utcnow()
        db.commit()
    return RedirectResponse(url=f"/review/{item_id}", status_code=303)


@app.get("/duplicates")
def duplicate_center(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse(
        request,
        "duplicates.html",
        context("duplicates", db=db, people_duplicates=find_duplicate_people(db), organization_duplicates=find_duplicate_organizations(db), duplicate_label=duplicate_label),
    )


@app.post("/duplicates/check")
def duplicates_check(db: Session = Depends(get_db)):
    db.query(DuplicateRecord).delete()
    for record in find_duplicate_people(db):
        db.add(DuplicateRecord(entity_type="person", entity_id_1=record["left"].id, entity_id_2=record["right"].id, similarity_score=record["score"], match_reason=record["reason"]))
    for record in find_duplicate_organizations(db):
        db.add(DuplicateRecord(entity_type="organization", entity_id_1=record["left"].id, entity_id_2=record["right"].id, similarity_score=record["score"], match_reason=record["reason"]))
    db.commit()
    return RedirectResponse(url="/duplicates", status_code=303)


@app.get("/duplicates/people/{person_id}")
def duplicates_for_person(person_id: int):
    return RedirectResponse(url=f"/people/{person_id}", status_code=303)


@app.post("/duplicates/merge-people")
def merge_people_placeholder(primary_id: int = Form(...), duplicate_id: int = Form(...), db: Session = Depends(get_db)):
    db.add(DuplicateRecord(entity_type="person", entity_id_1=primary_id, entity_id_2=duplicate_id, similarity_score=100, match_reason="Merge preview required", status="Pending Merge Preview"))
    db.commit()
    return RedirectResponse(url="/duplicates", status_code=303)


@app.post("/duplicates/merge-organizations")
def merge_organizations_placeholder(primary_id: int = Form(...), duplicate_id: int = Form(...), db: Session = Depends(get_db)):
    db.add(DuplicateRecord(entity_type="organization", entity_id_1=primary_id, entity_id_2=duplicate_id, similarity_score=100, match_reason="Merge preview required", status="Pending Merge Preview"))
    db.commit()
    return RedirectResponse(url="/duplicates", status_code=303)


@app.post("/duplicates/mark-not-duplicate")
def mark_not_duplicate(entity_type: str = Form(...), entity_id_1: int = Form(...), entity_id_2: int = Form(...), db: Session = Depends(get_db)):
    db.add(DuplicateRecord(entity_type=entity_type, entity_id_1=entity_id_1, entity_id_2=entity_id_2, similarity_score=0, match_reason="User marked not duplicate", status="Not Duplicate", resolved_at=datetime.utcnow()))
    db.commit()
    return RedirectResponse(url="/duplicates", status_code=303)


@app.get("/smart-import")
def smart_import_page(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse(request, "smart_import.html", context("smart_import", db=db, preview_rows=[], columns=[]))


@app.post("/smart-import/upload")
def smart_import_upload(request: Request, import_file: UploadFile = File(...), db: Session = Depends(get_db)):
    content = import_file.file.read().decode("utf-8-sig", errors="ignore")
    rows = list(csv.DictReader(content.splitlines()))
    return templates.TemplateResponse(request, "smart_import.html", context("smart_import", db=db, preview_rows=rows[:50], columns=list(rows[0].keys()) if rows else [], raw_csv=content))


@app.post("/smart-import/confirm")
def smart_import_confirm(raw_csv: str = Form(""), db: Session = Depends(get_db)):
    rows = list(csv.DictReader(raw_csv.splitlines())) if raw_csv else []
    for row in rows:
        text = "; ".join(f"{key}: {value}" for key, value in row.items() if value)
        extracted = {
            "people": [{"full_name": " ".join(row.get(key, "") for key in ["first_name", "second_name", "third_name", "fourth_name", "family_name"]).strip()}] if row.get("first_name") else [],
            "organizations": [{"name": row.get("organization", "")}] if row.get("organization") else [],
            "positions": [{"position_title": row.get("position_title", ""), "start_year": row.get("start_year", ""), "end_year": row.get("end_year", "")}] if row.get("position_title") else [],
            "notes": [{"content": row.get("notes", text)}],
            "sources": [{"url": row.get("source_url", "")}] if row.get("source_url") else [],
            "tags": [row.get("tags", "")] if row.get("tags") else [],
            "confidence": "Unknown",
            "relationships": [],
            "education": [],
        }
        db.add(ExtractedItem(raw_text=text, input_type="CSV Import", extracted_json=json.dumps(extracted, ensure_ascii=False), source_type="Document", source_url=row.get("source_url", ""), confidence="Unknown", privacy_level="Public Fact", status="Pending Review", duplicate_status="Not Checked"))
    db.commit()
    return RedirectResponse(url="/review", status_code=303)


@app.get("/export")
def export_center(request: Request, db: Session = Depends(get_db)):
    people = db.query(Person).order_by(Person.display_name if False else Person.id).all()
    organizations = db.query(Organization).order_by(Organization.id).all()
    logs = db.query(ExportLog).order_by(ExportLog.id.desc()).limit(20).all()
    return templates.TemplateResponse(request, "export_center.html", context("export", db=db, people=people, organizations=organizations, logs=logs))


@app.post("/export/people/csv")
def export_people_csv(include_private: str = Form(""), include_sensitive: str = Form(""), db: Session = Depends(get_db)):
    path = EXPORT_DIR / f"people_export_{timestamp_slug()}.csv"
    columns = ["id", "first_name", "second_name", "third_name", "fourth_name", "family_name", "tribe_name", "gender", "nationality", "status", "category", "tags"]
    write_csv(path, table_rows(db, Person, columns), columns)
    db.add(ExportLog(export_type="people_csv", file_path=str(path), include_private=include_private == "yes", include_sensitive=include_sensitive == "yes"))
    db.commit()
    return FileResponse(path, filename=path.name)


@app.post("/export/organizations/csv")
def export_organizations_csv(include_private: str = Form(""), include_sensitive: str = Form(""), db: Session = Depends(get_db)):
    path = EXPORT_DIR / f"organizations_export_{timestamp_slug()}.csv"
    columns = ["id", "name", "alternative_name", "organization_type", "status", "emirate", "founded_year", "founder", "headquarters", "tags"]
    write_csv(path, table_rows(db, Organization, columns), columns)
    db.add(ExportLog(export_type="organizations_csv", file_path=str(path), include_private=include_private == "yes", include_sensitive=include_sensitive == "yes"))
    db.commit()
    return FileResponse(path, filename=path.name)


@app.post("/export/full/json")
def export_full_json(include_private: str = Form(""), include_sensitive: str = Form(""), db: Session = Depends(get_db)):
    path = EXPORT_DIR / f"full_database_export_{timestamp_slug()}.json"
    payload = {
        "people": table_rows(db, Person, ["id", "first_name", "second_name", "third_name", "fourth_name", "family_name", "tribe_name", "gender", "nationality", "status", "category", "tags"]),
        "organizations": table_rows(db, Organization, ["id", "name", "alternative_name", "organization_type", "status", "emirate", "tags"]),
        "positions": table_rows(db, Position, ["id", "person_id", "organization_id", "position_title", "department", "start_year", "end_year", "is_current", "role_type"]),
        "relationships": table_rows(db, Relationship, ["id", "from_person_id", "to_person_id", "relationship_type", "notes"]),
        "education": table_rows(db, Education, ["id", "person_id", "institution", "degree", "major", "country"]),
        "notes": [row for row in table_rows(db, Note, ["id", "entity_type", "entity_id", "note_type", "title", "content", "is_private", "confidence", "privacy_level"]) if include_private == "yes" or not row.get("is_private")],
        "sources": table_rows(db, Source, ["id", "note_id", "entity_type", "entity_id", "source_type", "title", "url", "file_path"]),
        "settings": export_settings_payload(db),
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    db.add(ExportLog(export_type="full_json", file_path=str(path), include_private=include_private == "yes", include_sensitive=include_sensitive == "yes"))
    db.commit()
    return FileResponse(path, filename=path.name)


@app.post("/export/backup/zip")
def export_backup_zip(db: Session = Depends(get_db)):
    path = create_backup_zip(db)
    return FileResponse(path, filename=path.name)


@app.get("/backup")
def backup_center(request: Request, db: Session = Depends(get_db)):
    backups = sorted(BACKUP_DIR.glob("*.zip"), key=lambda path: path.stat().st_mtime, reverse=True)
    logs = db.query(BackupLog).order_by(BackupLog.id.desc()).limit(50).all()
    return templates.TemplateResponse(request, "backup.html", context("backup", db=db, backups=backups, logs=logs))


@app.post("/backup/create")
def backup_create(db: Session = Depends(get_db)):
    create_backup_zip(db)
    return RedirectResponse(url="/backup", status_code=303)


@app.get("/backup/download/{filename}")
def backup_download(filename: str):
    path = BACKUP_DIR / safe_filename(filename)
    if not path.exists() or path.suffix != ".zip":
        return RedirectResponse(url="/backup", status_code=303)
    return FileResponse(path, filename=path.name)


@app.post("/backup/delete/{filename}")
def backup_delete(filename: str):
    path = BACKUP_DIR / safe_filename(filename)
    if path.exists() and path.suffix == ".zip":
        path.unlink()
    return RedirectResponse(url="/backup", status_code=303)


@app.post("/backup/restore-placeholder")
def backup_restore_placeholder():
    return RedirectResponse(url="/backup", status_code=303)


@app.get("/settings")
def settings_home(request: Request, db: Session = Depends(get_db)):
    return settings_section("overview", request, db)


@app.get("/settings/{section}")
def settings_section(section: str, request: Request, db: Session = Depends(get_db)):
    if section == "export":
        return export_settings(db)
    if section not in SETTINGS_SECTIONS:
        section = "overview"
    all_options = db.query(SettingOption).order_by(SettingOption.updated_at.desc()).all()
    stats = {
        "total": len(all_options),
        "active": sum(1 for option in all_options if option.is_active),
        "inactive": sum(1 for option in all_options if not option.is_active),
        "system": sum(1 for option in all_options if option.is_system),
        "custom": sum(1 for option in all_options if not option.is_system),
        "last_updated": all_options[0] if all_options else None,
    }
    return templates.TemplateResponse(
        request,
        "settings.html",
        context(
            "settings",
            db=db,
            section=section,
            settings_sections=SETTINGS_SECTIONS,
            current_section=SETTINGS_SECTIONS[section],
            options_by_category=settings_options_by_category(db),
            stats=stats,
            color_fields=COLOR_FIELDS,
            text_groups=TEXT_GROUPS,
            font_families=FONT_FAMILIES,
            font_weights=FONT_WEIGHTS,
            default_appearance=DEFAULT_APPEARANCE_SETTINGS,
        ),
    )


@app.post("/settings/options/add")
def add_setting_option(
    category: str = Form(...),
    key: str = Form(...),
    label_en: str = Form(...),
    label_ar: str = Form(""),
    icon: str = Form("fa-circle"),
    color: str = Form("#64748b"),
    section: str = Form("overview"),
    db: Session = Depends(get_db),
):
    max_order = (
        db.query(SettingOption)
        .filter(SettingOption.category == category)
        .order_by(SettingOption.sort_order.desc())
        .first()
    )
    existing = (
        db.query(SettingOption)
        .filter(SettingOption.category == category, SettingOption.key == key)
        .first()
    )
    if not existing:
        db.add(
            SettingOption(
                category=category,
                key=key,
                label_en=label_en,
                label_ar=label_ar,
                icon=icon,
                color=color,
                sort_order=(max_order.sort_order + 1) if max_order else 1,
                is_active=True,
                is_system=False,
            )
        )
        db.commit()
    return RedirectResponse(url=f"/settings/{section}", status_code=303)


@app.post("/settings/options/{option_id}/edit")
def edit_setting_option(
    option_id: int,
    label_en: str = Form(...),
    label_ar: str = Form(""),
    icon: str = Form("fa-circle"),
    color: str = Form("#64748b"),
    section: str = Form("overview"),
    db: Session = Depends(get_db),
):
    option = db.query(SettingOption).filter(SettingOption.id == option_id).first()
    if option:
        option.label_en = label_en
        option.label_ar = label_ar
        option.icon = icon
        option.color = color
        option.updated_at = datetime.utcnow()
        db.commit()
    return RedirectResponse(url=f"/settings/{section}", status_code=303)


@app.post("/settings/options/{option_id}/toggle")
def toggle_setting_option(
    option_id: int, section: str = Form("overview"), db: Session = Depends(get_db)
):
    option = db.query(SettingOption).filter(SettingOption.id == option_id).first()
    if option:
        option.is_active = not option.is_active
        option.updated_at = datetime.utcnow()
        db.commit()
    return RedirectResponse(url=f"/settings/{section}", status_code=303)


@app.post("/settings/options/{option_id}/delete")
def delete_setting_option(
    option_id: int, section: str = Form("overview"), db: Session = Depends(get_db)
):
    option = db.query(SettingOption).filter(SettingOption.id == option_id).first()
    if option:
        db.delete(option)
        db.commit()
    return RedirectResponse(url=f"/settings/{section}", status_code=303)


def move_setting_option(db, option_id, direction):
    option = db.query(SettingOption).filter(SettingOption.id == option_id).first()
    if not option:
        return
    comparator = SettingOption.sort_order < option.sort_order if direction == "up" else SettingOption.sort_order > option.sort_order
    order = SettingOption.sort_order.desc() if direction == "up" else SettingOption.sort_order.asc()
    neighbor = (
        db.query(SettingOption)
        .filter(SettingOption.category == option.category, comparator)
        .order_by(order)
        .first()
    )
    if neighbor:
        option.sort_order, neighbor.sort_order = neighbor.sort_order, option.sort_order
        option.updated_at = datetime.utcnow()
        neighbor.updated_at = datetime.utcnow()
        db.commit()


@app.post("/settings/options/{option_id}/move-up")
def move_setting_option_up(
    option_id: int, section: str = Form("overview"), db: Session = Depends(get_db)
):
    move_setting_option(db, option_id, "up")
    return RedirectResponse(url=f"/settings/{section}", status_code=303)


@app.post("/settings/options/{option_id}/move-down")
def move_setting_option_down(
    option_id: int, section: str = Form("overview"), db: Session = Depends(get_db)
):
    move_setting_option(db, option_id, "down")
    return RedirectResponse(url=f"/settings/{section}", status_code=303)


@app.post("/settings/reset-defaults")
def reset_settings(section: str = Form("overview")):
    seed_setting_options(reset=True)
    return RedirectResponse(url=f"/settings/{section}", status_code=303)


@app.post("/settings/appearance/apply")
async def apply_appearance_settings(request: Request, db: Session = Depends(get_db)):
    form = await request.form()
    for key, default_value in DEFAULT_APPEARANCE_SETTINGS.items():
        raw_value = form.get(key, default_value)
        value = validate_appearance_value(key, raw_value)
        if value is None:
            return RedirectResponse(url="/settings/appearance?appearance_error=invalid_hex", status_code=303)
        setting = db.query(AppearanceSetting).filter(AppearanceSetting.key == key).first()
        if setting:
            setting.value = value
            setting.updated_at = datetime.utcnow()
        else:
            db.add(AppearanceSetting(key=key, value=value))
    db.commit()
    return RedirectResponse(url="/settings/appearance", status_code=303)


@app.post("/settings/appearance/reset")
def reset_appearance_settings(db: Session = Depends(get_db)):
    db.query(AppearanceSetting).delete()
    db.commit()
    return RedirectResponse(url="/settings/appearance", status_code=303)


@app.get("/settings/export")
def export_settings(db: Session = Depends(get_db)):
    return export_settings_payload(db)


@app.get("/search")
def search(request: Request, q: str = "", db: Session = Depends(get_db)):
    people_results = []
    organization_results = []
    position_results = []
    note_results = []
    query = q.strip()
    if query:
        pattern = f"%{query}%"
        people_results = (
            db.query(Person)
            .filter(
                or_(
                    Person.first_name.ilike(pattern),
                    Person.second_name.ilike(pattern),
                    Person.third_name.ilike(pattern),
                    Person.fourth_name.ilike(pattern),
                    Person.family_name.ilike(pattern),
                    Person.tribe_name.ilike(pattern),
                    Person.tags.ilike(pattern),
                    Person.private_notes.ilike(pattern),
                    Person.achievements.ilike(pattern),
                )
            )
            .order_by(Person.id.desc())
            .all()
        )
        organization_results = (
            db.query(Organization)
            .filter(
                or_(
                    Organization.name.ilike(pattern),
                    Organization.alternative_name.ilike(pattern),
                    Organization.organization_type.ilike(pattern),
                    Organization.tags.ilike(pattern),
                    Organization.description.ilike(pattern),
                    Organization.notes.ilike(pattern),
                )
            )
            .order_by(Organization.id.desc())
            .all()
        )
        position_results = (
            db.query(Position)
            .join(Person)
            .join(Organization)
            .filter(
                or_(
                    Position.position_title.ilike(pattern),
                    Position.notes.ilike(pattern),
                    Person.first_name.ilike(pattern),
                    Person.family_name.ilike(pattern),
                    Organization.name.ilike(pattern),
                    Organization.alternative_name.ilike(pattern),
                )
            )
            .order_by(Position.id.desc())
            .all()
        )
        note_results = (
            db.query(Note)
            .filter(
                or_(
                    Note.title.ilike(pattern),
                    Note.content.ilike(pattern),
                    Note.note_type.ilike(pattern),
                    Note.source.ilike(pattern),
                    Note.date_text.ilike(pattern),
                )
            )
            .order_by(Note.id.desc())
            .all()
        )
    return templates.TemplateResponse(
        request,
        "search.html",
        context(
            "search",
            db=db,
            q=q,
            people=people_results,
            organizations=organization_results,
            positions=position_results,
            notes=note_results,
        ),
    )

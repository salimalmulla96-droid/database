const translations = {
  en: {
    brand: "Smart Database",
    language_button: "العربية",
    nav_dashboard: "Dashboard",
    nav_people: "People",
    nav_add_person: "Add Person",
    nav_organizations: "Organizations",
    nav_add_organization: "Add Organization",
    nav_search: "Search",
    nav_settings: "Settings",
    nav_smart_add: "Smart Add",
    nav_smart_import: "Smart Import",
    nav_review: "Review Queue",
    nav_duplicates: "Duplicate Center",
    nav_export: "Export Center",
    nav_backup: "Backup Center",
    smart_intake: "Smart Information Intake",
    smart_add: "Smart Add",
    smart_import: "Smart Import",
    review_queue: "Review Queue",
    duplicate_center: "Duplicate Center",
    export_center: "Export Center",
    backup_center: "Backup Center",
    paste_information: "Paste information",
    smart_add_hint: "Paste messy notes, biography text, source snippets, or mixed profile information. Nothing is saved to profiles until review.",
    analyze_information: "Analyze Information",
    classify_source: "Classify source",
    input_type: "What type of information is this?",
    confidence: "Confidence",
    privacy_level: "Privacy",
    review_safety: "Extracted information always goes to Review Queue first.",
    review: "Review",
    reject: "Reject",
    approve: "Approve",
    save_as_note: "Save as Note",
    check_duplicates: "Check Duplicates",
    merge: "Merge",
    review_item: "Review Item",
    original_text: "Original pasted text",
    possible_duplicates: "Possible Duplicates",
    editable_data: "Editable extracted data",
    approve_safety: "Approve creates new records only for clear extracted people and organizations. It never overwrites existing records.",
    empty_queue: "No items in this status.",
    no_duplicates: "No possible duplicates found.",
    run_duplicate_check: "Run Duplicate Check",
    people_duplicates: "People Duplicates",
    organization_duplicates: "Organization Duplicates",
    keep_separate: "Keep Separate",
    import_hint: "CSV is supported in this first version. Excel/PDF/Word/Image import are placeholders.",
    import_to_review: "Import selected to Review Queue",
    include_private: "Include private notes",
    include_sensitive: "Include sensitive items",
    include_files: "Include source files",
    include_images: "Include uploaded images",
    include_unverified: "Include unverified information",
    export_warning: "Private and sensitive data are excluded unless checked.",
    download: "Download",
    create_backup: "Create Full Backup Now",
    existing_backups: "Existing Backups",
    restore_placeholder: "Restore Placeholder",
    restore_warning: "Restoring will replace current data. Create a backup before restoring.",
    no_backups: "No backups yet.",
    settings_center: "Smart Settings Center",
    settings: "Settings",
    add_option: "Add Option",
    export_settings: "Export Settings",
    total_options: "Total options",
    active_options: "Active options",
    inactive_options: "Inactive options",
    system_options: "System-protected",
    custom_options: "Custom options",
    last_updated: "Last updated",
    open_preview: "Open Preview",
    sample_profile: "Sample profile badge",
    settings_overview: "Overview",
    settings_people: "People",
    settings_organizations: "Organizations",
    settings_career: "Career & Positions",
    settings_relationships: "Relationships",
    settings_education: "Education",
    settings_notes: "Notes & Sources",
    settings_interface: "Interface & Language",
    settings_data: "Data Management",
    settings_overview_desc: "Review setting health, quick actions, and live previews.",
    settings_people_desc: "Manage dropdowns and badges used when adding or filtering people.",
    settings_organizations_desc: "Manage organization types, statuses, emirates, and entity links.",
    settings_career_desc: "Manage role types, position suggestions, and current role display rules.",
    settings_relationships_desc: "Manage relationship labels, reverse meanings, and relationship groups.",
    settings_education_desc: "Manage education degrees, countries, and institution suggestions.",
    settings_notes_desc: "Manage note categories, source types, and file source behavior.",
    settings_interface_desc: "Preview language, RTL, sidebar style, density, and theme behavior.",
    settings_data_desc: "Export, backup, reset defaults, and review dangerous actions.",
    inactive_helper: "Inactive options are hidden from new forms but remain visible on old records.",
    system_helper: "System options are protected to prevent accidental deletion.",
    key_helper: "English key values are stored internally to keep search and filters stable.",
    name_helper: "Arabic labels only affect display and do not translate saved names.",
    no_options: "No options in this category yet.",
    interface_preview: "Interface Preview",
    interface_hint: "Use the language button in the sidebar to preview RTL and LTR behavior.",
    data_management: "Data Management",
    danger_helper: "Review dangerous actions carefully before using them.",
    reset_defaults: "Reset Defaults",
    import_placeholder: "Import data placeholder",
    backup_placeholder: "Backup database placeholder",
    preview: "Preview",
    sample_dropdown: "Sample dropdown",
    sample_card: "Sample card",
    preview_helper: "Click an option row to preview how it looks.",
    manage_option: "Manage Option",
    key: "Key",
    label_en: "English Label",
    label_ar: "Arabic Label",
    icon: "Icon",
    color: "Color",
    dashboard: "Dashboard",
    dashboard_eyebrow: "Private intelligence database",
    total_people: "Total people",
    total_organizations: "Total organizations",
    total_relationships: "Total relationships",
    total_positions: "Total positions",
    total_notes: "Total notes",
    government_figures: "Government figures",
    business_figures: "Business figures",
    active_organizations: "Active organizations",
    recent_people: "Recently added people",
    recent_organizations: "Recently added organizations",
    view_all: "View all",
    records: "Records",
    people: "People",
    organizations: "Organizations",
    add_person: "Add Person",
    add_organization: "Add Organization",
    add_note: "Add Note",
    add_relationship: "Add Relationship",
    filter_gender: "Gender",
    filter_nationality: "Nationality",
    filter_status: "Status",
    filter_category: "Category",
    filter_type: "Type",
    filter_emirate: "Emirate",
    filter: "Filter",
    clear: "Clear",
    new_record: "New record",
    edit: "Edit",
    edit_person: "Edit Person",
    edit_organization: "Edit Organization",
    save_changes: "Save Changes",
    save: "Save",
    main_photo: "Main Photo",
    photo_hint: "Upload a profile image or keep the default avatar.",
    logo_hint: "Upload a logo or keep the default organization icon.",
    name_information: "Name Information",
    basic_information: "Basic Information",
    basic_info_card: "Basic Info",
    identity: "Identity",
    education_career: "Education / Career",
    first_name: "First Name",
    second_name: "Second Name",
    third_name: "Third Name",
    fourth_name: "Fourth Name",
    family_name: "Family Name",
    tribe_name: "Tribe Name",
    gender: "Gender",
    nationality: "Nationality",
    status: "Status",
    category: "Category",
    birth_date: "Birth Date",
    birth_place: "Birth Place",
    education: "Education",
    add_education: "Add Education",
    education_history: "Education History",
    institution: "Institution",
    degree: "Degree / Level",
    country: "Country",
    no_education: "No education added yet.",
    university: "University",
    major: "Major",
    graduation_year: "Graduation Year",
    current_role: "Current Role",
    main_field: "Main Field",
    note: "Note",
    private_notes: "Private Notes",
    tags: "Tags",
    tags_placeholder: "Dubai, Government, Emaar, University, Medicine",
    organization_tags_placeholder: "Dubai, Government, Ministry, Holding, Finance",
    person_image: "Person Image",
    organization_image: "Organization Logo/Image",
    cancel: "Cancel",
    save_person: "Save Person",
    save_organization: "Save Organization",
    save_note: "Save Note",
    save_relationship: "Save Relationship",
    save_position: "Save Position",
    logo_image: "Logo/Image",
    name: "Name",
    alternative_name: "Alternative Name",
    organization_type: "Organization Type",
    emirate: "Emirate",
    history: "History",
    history_location: "History and Location",
    founded_year: "Founded Year",
    founder: "Founder",
    headquarters: "Headquarters",
    description_notes: "Description and Notes",
    description: "Description",
    notes: "Notes",
    smart_notes: "Smart Notes",
    note_type: "Note Type",
    title: "Title",
    content: "Content",
    date_text: "Date / Year",
    source: "Source",
    sources: "Sources",
    add_source: "Add Source",
    source_type: "Source Type",
    source_title: "Source Title",
    source_url: "URL",
    source_file: "Upload File",
    text_reference: "Text Reference",
    private: "Private",
    private_note: "Private note",
    delete: "Delete",
    no_notes: "No notes added yet.",
    person_profile: "Person profile",
    organization_profile: "Organization profile",
    back: "Back",
    name_family_card: "Name / Family / Tribe",
    career_timeline: "Career Timeline",
    current_positions: "Current Positions",
    current_roles: "Current Roles",
    no_current_role: "No current role added yet.",
    previous_positions: "Previous Positions",
    linked_organizations: "Linked Organizations",
    no_linked_organizations: "No linked organizations.",
    present: "Present",
    no_current_positions: "No current positions added.",
    no_previous_positions: "No previous positions added.",
    no_position_history: "No position history added.",
    relationships: "Relationships",
    organization_relationships: "Organization Relationships",
    no_organization_relationships: "No organization relationships added.",
    none: "None",
    from_person: "From Person",
    to_person: "To Person",
    from_organization: "From Organization",
    to_organization: "To Organization",
    relationship_type: "Relationship Type",
    another_person: "Another Person",
    organization_position: "Organization / Work Position",
    another_organization: "Another Organization",
    person_position: "Person / Position",
    add_position: "Add Position / Work History",
    add_career_position: "Add Career / Position",
    add_person_position: "Add Person / Position Link",
    organization: "Organization",
    person: "Person",
    position_title: "Position Title",
    department: "Department",
    role_type: "Role Type",
    start_year: "Start Year",
    end_year: "End Year",
    current_role_checkbox: "Current role",
    current_people: "Current People",
    previous_people: "Previous People",
    position_timeline: "Position Timeline",
    no_current_people: "No current people added.",
    no_previous_people: "No previous people added.",
    group_family: "Family",
    group_work_professional: "Work / Professional",
    group_social: "Social",
    group_other: "Other",
    find_records: "Find records",
    search: "Search",
    search_placeholder: "Search names, tribes, tags, notes, organizations, and positions",
    people_results: "People results",
    organization_results: "Organization results",
    position_results: "Position results",
    note_results: "Note results",
    no_people_match: "No people matched your search.",
    no_organizations_match: "No organizations matched your search.",
    no_positions_match: "No positions matched your search.",
    no_notes_match: "No notes matched your search.",
    enter_search: "Enter a search term to begin.",
    search_org_hint: "Search by organization name, tags, type, or notes.",
    search_position_hint: "Position matches will appear here.",
    search_note_hint: "Note matches will appear here.",
    no_people_yet: "No people added yet.",
    no_organizations_yet: "No organizations added yet.",
    no_people_found: "No people found. Add your first person record.",
    no_organizations_found: "No organizations found. Add your first organization record.",
    what_are_you_adding: "What are you adding?",
    back_to_smart_add: "Back to Smart Add",
    extracted_person: "Extracted Person",
    extracted_organization: "Extracted Organization",
    current_role_career: "Current Role / Career",
    add_career_entry: "Add another career entry",
    create_position: "Create position",
    create_education: "Create education",
    remove: "Remove",
    organizations_detected: "Organizations Detected",
    create_organization: "Create organization",
    link_existing: "Link existing",
    ignore: "Ignore",
    existing_organization: "Existing Organization",
    note_from_original_paragraph: "Note From Original Paragraph",
    create_new: "Create new",
    merge_existing: "Merge with existing",
    update_existing: "Update existing",
    advanced_raw_data: "Advanced: View raw extracted data",
    approve_create_profile: "Approve & Create Profile",
    save_as_note_only: "Save as Note Only",
    mixed_detected_items: "Mixed Detected Items",
    delete_extracted_item: "Delete extracted item",
    delete_person: "Delete Person",
    delete_organization: "Delete Organization"
  },
  ar: {
    brand: "قاعدة البيانات الذكية",
    language_button: "English",
    nav_dashboard: "لوحة التحكم",
    nav_people: "الأشخاص",
    nav_add_person: "إضافة شخص",
    nav_organizations: "الجهات",
    nav_add_organization: "إضافة جهة",
    nav_search: "البحث",
    nav_settings: "الإعدادات",
    nav_smart_add: "الإضافة الذكية",
    nav_smart_import: "الاستيراد الذكي",
    nav_review: "قائمة المراجعة",
    nav_duplicates: "مركز التكرارات",
    nav_export: "مركز التصدير",
    nav_backup: "مركز النسخ الاحتياطي",
    smart_intake: "إدخال المعلومات الذكي",
    smart_add: "الإضافة الذكية",
    smart_import: "الاستيراد الذكي",
    review_queue: "قائمة المراجعة",
    duplicate_center: "مركز التكرارات",
    export_center: "مركز التصدير",
    backup_center: "مركز النسخ الاحتياطي",
    paste_information: "لصق المعلومات",
    smart_add_hint: "الصق ملاحظات غير مرتبة أو نص سيرة أو مقتطفات مصادر أو معلومات مختلطة. لا يتم حفظ شيء في الملفات قبل المراجعة.",
    analyze_information: "تحليل المعلومات",
    classify_source: "تصنيف المصدر",
    input_type: "ما نوع هذه المعلومات؟",
    confidence: "درجة الثقة",
    privacy_level: "الخصوصية",
    review_safety: "المعلومات المستخرجة تنتقل دائماً إلى قائمة المراجعة أولاً.",
    review: "مراجعة",
    reject: "رفض",
    approve: "اعتماد",
    save_as_note: "حفظ كملاحظة",
    check_duplicates: "فحص التكرارات",
    merge: "دمج",
    review_item: "مراجعة عنصر",
    original_text: "النص الأصلي",
    possible_duplicates: "تكرارات محتملة",
    editable_data: "البيانات المستخرجة القابلة للتعديل",
    approve_safety: "الاعتماد ينشئ سجلات جديدة فقط للأشخاص والجهات الواضحة ولا يستبدل السجلات الحالية.",
    empty_queue: "لا توجد عناصر بهذه الحالة.",
    no_duplicates: "لا توجد تكرارات محتملة.",
    run_duplicate_check: "تشغيل فحص التكرارات",
    people_duplicates: "تكرارات الأشخاص",
    organization_duplicates: "تكرارات الجهات",
    keep_separate: "إبقاء منفصل",
    import_hint: "يدعم الإصدار الأول CSV. استيراد Excel/PDF/Word/Image متاح كخانة مستقبلية.",
    import_to_review: "استيراد المحدد إلى قائمة المراجعة",
    include_private: "تضمين الملاحظات الخاصة",
    include_sensitive: "تضمين العناصر الحساسة",
    include_files: "تضمين ملفات المصادر",
    include_images: "تضمين الصور المرفوعة",
    include_unverified: "تضمين المعلومات غير المؤكدة",
    export_warning: "يتم استبعاد البيانات الخاصة والحساسة ما لم يتم اختيارها.",
    download: "تنزيل",
    create_backup: "إنشاء نسخة احتياطية كاملة الآن",
    existing_backups: "النسخ الاحتياطية الموجودة",
    restore_placeholder: "استعادة لاحقاً",
    restore_warning: "الاستعادة ستستبدل البيانات الحالية. أنشئ نسخة احتياطية قبل الاستعادة.",
    no_backups: "لا توجد نسخ احتياطية بعد.",
    settings_center: "مركز الإعدادات الذكي",
    settings: "الإعدادات",
    add_option: "إضافة خيار",
    export_settings: "تصدير الإعدادات",
    total_options: "إجمالي الخيارات",
    active_options: "الخيارات النشطة",
    inactive_options: "الخيارات غير النشطة",
    system_options: "خيارات محمية",
    custom_options: "خيارات مخصصة",
    last_updated: "آخر تحديث",
    open_preview: "فتح المعاينة",
    sample_profile: "شارة ملف تجريبية",
    settings_overview: "نظرة عامة",
    settings_people: "الأشخاص",
    settings_organizations: "الجهات",
    settings_career: "المسار المهني والمناصب",
    settings_relationships: "العلاقات",
    settings_education: "التعليم",
    settings_notes: "الملاحظات والمصادر",
    settings_interface: "الواجهة واللغة",
    settings_data: "إدارة البيانات",
    settings_overview_desc: "راجع حالة الإعدادات والإجراءات السريعة والمعاينات.",
    settings_people_desc: "إدارة القوائم والشارات المستخدمة في الأشخاص.",
    settings_organizations_desc: "إدارة أنواع الجهات والحالات والإمارات والعلاقات.",
    settings_career_desc: "إدارة أنواع المناصب واقتراحات المسميات وقواعد المناصب الحالية.",
    settings_relationships_desc: "إدارة مسميات العلاقات والمعاني العكسية والمجموعات.",
    settings_education_desc: "إدارة الدرجات التعليمية والدول واقتراحات المؤسسات.",
    settings_notes_desc: "إدارة أنواع الملاحظات والمصادر وسلوك الملفات.",
    settings_interface_desc: "معاينة اللغة واتجاه الواجهة والشريط والكثافة والثيم.",
    settings_data_desc: "التصدير والنسخ الاحتياطي وإعادة الضبط والإجراءات الحساسة.",
    inactive_helper: "الخيارات غير النشطة تختفي من النماذج الجديدة وتبقى ظاهرة في السجلات القديمة.",
    system_helper: "خيارات النظام محمية لمنع الحذف غير المقصود.",
    key_helper: "القيم الإنجليزية الداخلية تحفظ ثبات البحث والفلاتر.",
    name_helper: "التسميات العربية للعرض فقط ولا تترجم الأسماء المحفوظة.",
    no_options: "لا توجد خيارات في هذه الفئة بعد.",
    interface_preview: "معاينة الواجهة",
    interface_hint: "استخدم زر اللغة في الشريط الجانبي لمعاينة RTL و LTR.",
    data_management: "إدارة البيانات",
    danger_helper: "راجع الإجراءات الحساسة بعناية قبل استخدامها.",
    reset_defaults: "إعادة الإعدادات الافتراضية",
    import_placeholder: "استيراد البيانات لاحقا",
    backup_placeholder: "نسخ احتياطي لاحقا",
    preview: "المعاينة",
    sample_dropdown: "قائمة تجريبية",
    sample_card: "بطاقة تجريبية",
    preview_helper: "اضغط على خيار لمعاينة شكله.",
    manage_option: "إدارة الخيار",
    key: "المفتاح",
    label_en: "التسمية الإنجليزية",
    label_ar: "التسمية العربية",
    icon: "الأيقونة",
    color: "اللون",
    dashboard: "لوحة التحكم",
    dashboard_eyebrow: "قاعدة معلومات خاصة",
    total_people: "إجمالي الأشخاص",
    total_organizations: "إجمالي الجهات",
    total_relationships: "إجمالي العلاقات",
    total_positions: "إجمالي المناصب",
    total_notes: "إجمالي الملاحظات",
    government_figures: "الشخصيات الحكومية",
    business_figures: "الشخصيات التجارية",
    active_organizations: "الجهات النشطة",
    recent_people: "أحدث الأشخاص",
    recent_organizations: "أحدث الجهات",
    view_all: "عرض الكل",
    records: "السجلات",
    people: "الأشخاص",
    organizations: "الجهات",
    add_person: "إضافة شخص",
    add_organization: "إضافة جهة",
    add_note: "إضافة ملاحظة",
    add_relationship: "إضافة علاقة",
    filter_gender: "الجنس",
    filter_nationality: "الجنسية",
    filter_status: "الحالة",
    filter_category: "الفئة",
    filter_type: "النوع",
    filter_emirate: "الإمارة",
    filter: "تصفية",
    clear: "مسح",
    new_record: "سجل جديد",
    edit: "تعديل",
    edit_person: "تعديل الشخص",
    edit_organization: "تعديل الجهة",
    save_changes: "حفظ التغييرات",
    save: "حفظ",
    main_photo: "الصورة الرئيسية",
    photo_hint: "ارفع صورة شخصية أو اترك الصورة الافتراضية.",
    logo_hint: "ارفع شعارا أو اترك الأيقونة الافتراضية.",
    name_information: "معلومات الاسم",
    basic_information: "المعلومات الأساسية",
    basic_info_card: "معلومات أساسية",
    identity: "الهوية",
    education_career: "التعليم / المسار المهني",
    first_name: "الاسم الأول",
    second_name: "الاسم الثاني",
    third_name: "الاسم الثالث",
    fourth_name: "الاسم الرابع",
    family_name: "اسم العائلة",
    tribe_name: "اسم القبيلة",
    gender: "الجنس",
    nationality: "الجنسية",
    status: "الحالة",
    category: "الفئة",
    birth_date: "تاريخ الميلاد",
    birth_place: "مكان الميلاد",
    education: "التعليم",
    add_education: "إضافة تعليم",
    education_history: "تاريخ التعليم",
    institution: "المؤسسة التعليمية",
    degree: "الدرجة / المستوى",
    country: "الدولة",
    no_education: "لم تتم إضافة تعليم بعد.",
    university: "الجامعة",
    major: "التخصص",
    graduation_year: "سنة التخرج",
    current_role: "الدور الحالي",
    main_field: "المجال الرئيسي",
    note: "ملاحظة",
    private_notes: "ملاحظات خاصة",
    tags: "الوسوم",
    tags_placeholder: "دبي، حكومة، إعمار، جامعة، طب",
    organization_tags_placeholder: "دبي، حكومة، وزارة، شركة قابضة، مالية",
    person_image: "صورة الشخص",
    organization_image: "شعار أو صورة الجهة",
    cancel: "إلغاء",
    save_person: "حفظ الشخص",
    save_organization: "حفظ الجهة",
    save_note: "حفظ الملاحظة",
    save_relationship: "حفظ العلاقة",
    save_position: "حفظ المنصب",
    logo_image: "الشعار / الصورة",
    name: "الاسم",
    alternative_name: "اسم بديل",
    organization_type: "نوع الجهة",
    emirate: "الإمارة",
    history: "التاريخ",
    history_location: "التاريخ والموقع",
    founded_year: "سنة التأسيس",
    founder: "المؤسس",
    headquarters: "المقر الرئيسي",
    description_notes: "الوصف والملاحظات",
    description: "الوصف",
    notes: "الملاحظات",
    smart_notes: "ملاحظات ذكية",
    note_type: "نوع الملاحظة",
    title: "العنوان",
    content: "المحتوى",
    date_text: "التاريخ / السنة",
    source: "المصدر",
    sources: "المصادر",
    add_source: "إضافة مصدر",
    source_type: "نوع المصدر",
    source_title: "عنوان المصدر",
    source_url: "الرابط",
    source_file: "رفع ملف",
    text_reference: "مرجع نصي",
    private: "خاص",
    private_note: "ملاحظة خاصة",
    delete: "حذف",
    no_notes: "لا توجد ملاحظات بعد.",
    person_profile: "ملف شخصي",
    organization_profile: "ملف جهة",
    back: "رجوع",
    name_family_card: "الاسم / العائلة / القبيلة",
    career_timeline: "الخط الزمني المهني",
    current_positions: "المناصب الحالية",
    current_roles: "المناصب الحالية",
    no_current_role: "لم تتم إضافة مناصب حالية بعد",
    previous_positions: "المناصب السابقة",
    linked_organizations: "الجهات المرتبطة",
    no_linked_organizations: "لا توجد جهات مرتبطة.",
    present: "حالي",
    no_current_positions: "لا توجد مناصب حالية.",
    no_previous_positions: "لا توجد مناصب سابقة.",
    no_position_history: "لا يوجد تاريخ مناصب.",
    relationships: "العلاقات",
    organization_relationships: "علاقات الجهات",
    no_organization_relationships: "لا توجد علاقات جهات.",
    none: "لا يوجد",
    from_person: "من شخص",
    to_person: "إلى شخص",
    from_organization: "من جهة",
    to_organization: "إلى جهة",
    relationship_type: "نوع العلاقة",
    another_person: "شخص آخر",
    organization_position: "جهة / منصب عمل",
    another_organization: "جهة أخرى",
    person_position: "شخص / منصب",
    add_position: "إضافة منصب / تاريخ عمل",
    add_career_position: "إضافة مسار مهني / منصب",
    add_person_position: "إضافة شخص / منصب",
    organization: "الجهة",
    person: "الشخص",
    position_title: "المسمى الوظيفي",
    department: "القسم",
    role_type: "نوع الدور",
    start_year: "سنة البداية",
    end_year: "سنة النهاية",
    current_role_checkbox: "منصب حالي",
    current_people: "الأشخاص الحاليون",
    previous_people: "الأشخاص السابقون",
    position_timeline: "الخط الزمني للمناصب",
    no_current_people: "لا يوجد أشخاص حاليون.",
    no_previous_people: "لا يوجد أشخاص سابقون.",
    group_family: "العائلة",
    group_work_professional: "العمل / المهني",
    group_social: "اجتماعي",
    group_other: "أخرى",
    find_records: "البحث في السجلات",
    search: "بحث",
    search_placeholder: "ابحث في الأسماء، القبائل، الوسوم، الملاحظات، الجهات، والمناصب",
    people_results: "نتائج الأشخاص",
    organization_results: "نتائج الجهات",
    position_results: "نتائج المناصب",
    note_results: "نتائج الملاحظات",
    no_people_match: "لا يوجد أشخاص مطابقون.",
    no_organizations_match: "لا توجد جهات مطابقة.",
    no_positions_match: "لا توجد مناصب مطابقة.",
    no_notes_match: "لا توجد ملاحظات مطابقة.",
    enter_search: "أدخل كلمة بحث للبدء.",
    search_org_hint: "ابحث باسم الجهة أو الوسوم أو النوع أو الملاحظات.",
    search_position_hint: "ستظهر نتائج المناصب هنا.",
    search_note_hint: "ستظهر نتائج الملاحظات هنا.",
    no_people_yet: "لم تتم إضافة أشخاص بعد.",
    no_organizations_yet: "لم تتم إضافة جهات بعد.",
    no_people_found: "لا توجد نتائج. أضف أول سجل شخص.",
    no_organizations_found: "لا توجد نتائج. أضف أول سجل جهة.",
    what_are_you_adding: "ما الذي تضيفه؟",
    back_to_smart_add: "العودة إلى الإضافة الذكية",
    extracted_person: "الشخص المستخرج",
    extracted_organization: "الجهة المستخرجة",
    current_role_career: "الدور الحالي / المسار المهني",
    add_career_entry: "إضافة منصب آخر",
    create_position: "إنشاء منصب",
    create_education: "إنشاء تعليم",
    remove: "إزالة",
    organizations_detected: "الجهات المكتشفة",
    create_organization: "إنشاء جهة",
    link_existing: "ربط بجهة موجودة",
    ignore: "تجاهل",
    existing_organization: "جهة موجودة",
    note_from_original_paragraph: "ملاحظة من الفقرة الأصلية",
    create_new: "إنشاء جديد",
    merge_existing: "دمج مع موجود",
    update_existing: "تحديث موجود",
    advanced_raw_data: "متقدم: عرض البيانات الخام",
    approve_create_profile: "اعتماد وإنشاء ملف",
    save_as_note_only: "حفظ كملاحظة فقط",
    mixed_detected_items: "العناصر المختلطة المكتشفة",
    delete_extracted_item: "حذف عنصر المراجعة",
    delete_person: "حذف الشخص",
    delete_organization: "حذف الجهة"
  }
};

const valueLabels = {
  ar: {
    "Male": "ذكر",
    "Female": "أنثى",
    "Unknown": "غير معروف",
    "Alive": "على قيد الحياة",
    "Deceased": "متوفى",
    "UAE": "الإمارات العربية المتحدة",
    "Saudi Arabia": "السعودية",
    "Kuwait": "الكويت",
    "Qatar": "قطر",
    "Bahrain": "البحرين",
    "Oman": "عُمان",
    "Egypt": "مصر",
    "Jordan": "الأردن",
    "Lebanon": "لبنان",
    "Syria": "سوريا",
    "Palestine": "فلسطين",
    "Iraq": "العراق",
    "Yemen": "اليمن",
    "India": "الهند",
    "Pakistan": "باكستان",
    "United Kingdom": "المملكة المتحدة",
    "United States": "الولايات المتحدة",
    "Other": "أخرى",
    "Government Figure": "شخصية حكومية",
    "Royal Family": "الأسرة الحاكمة",
    "Business Figure": "شخصية أعمال",
    "Family Member": "فرد من العائلة",
    "Friend": "صديق",
    "University Friend": "صديق جامعي",
    "Classmate": "زميل دراسة",
    "Colleague": "زميل عمل",
    "Historical Figure": "شخصية تاريخية",
    "Ministry Employee": "موظف وزارة",
    "Company Employee": "موظف شركة",
    "Public Figure": "شخصية عامة",
    "Private Contact": "جهة اتصال خاصة",
    "Ministry": "وزارة",
    "Government Authority": "هيئة حكومية",
    "Government Department": "دائرة حكومية",
    "Council": "مجلس",
    "Company": "شركة",
    "Holding Company": "شركة قابضة",
    "University": "جامعة",
    "School": "مدرسة",
    "Hospital": "مستشفى",
    "Bank": "بنك",
    "Family Business": "شركة عائلية",
    "Royal Office": "مكتب رسمي",
    "Charity": "جمعية خيرية",
    "Foundation": "مؤسسة",
    "Committee": "لجنة",
    "Active": "نشطة",
    "Inactive": "غير نشطة",
    "Merged": "مدمجة",
    "Renamed": "تغير اسمها",
    "Abu Dhabi": "أبوظبي",
    "Dubai": "دبي",
    "Sharjah": "الشارقة",
    "Ajman": "عجمان",
    "Umm Al Quwain": "أم القيوين",
    "Ras Al Khaimah": "رأس الخيمة",
    "Fujairah": "الفجيرة",
    "Federal": "اتحادي",
    "GCC": "خليجي",
    "International": "دولي",
    "Father": "أب",
    "Mother": "أم",
    "Son": "ابن",
    "Daughter": "ابنة",
    "Brother": "أخ",
    "Sister": "أخت",
    "Husband": "زوج",
    "Wife": "زوجة",
    "Grandfather": "جد",
    "Grandmother": "جدة",
    "Grandson": "حفيد",
    "Granddaughter": "حفيدة",
    "Uncle": "عم / خال",
    "Aunt": "عمة / خالة",
    "Cousin": "ابن/بنت عم أو خال",
    "Nephew": "ابن الأخ/الأخت",
    "Niece": "بنت الأخ/الأخت",
    "Business Partner": "شريك عمل",
    "Mentor": "موجّه",
    "Student": "طالب",
    "Connected To": "مرتبط بـ",
    "Child": "ابن/ابنة",
    "Parent": "والد/والدة",
    "Sibling": "أخ/أخت",
    "Grandson/Granddaughter": "حفيد/حفيدة",
    "Grandfather/Grandmother": "جد/جدة",
    "Nephew/Niece": "ابن/بنت الأخ أو الأخت",
    "Uncle/Aunt": "عم/خال أو عمة/خالة",
    "General Note": "ملاحظة عامة",
    "Personal Note": "ملاحظة شخصية",
    "Family Note": "ملاحظة عائلية",
    "Education Note": "ملاحظة تعليمية",
    "Career Note": "ملاحظة مهنية",
    "Government Note": "ملاحظة حكومية",
    "Business Note": "ملاحظة تجارية",
    "Historical Note": "ملاحظة تاريخية",
    "Source Note": "ملاحظة مصدر",
    "Meeting Note": "ملاحظة مقابلة",
    "Important Fact": "معلومة مهمة",
    "Warning / Unverified": "تحذير / غير مؤكد",
    "Parent Organization": "جهة أم",
    "Subsidiary": "شركة تابعة",
    "Partner": "شريك",
    "Government Owner": "مالك حكومي",
    "Regulator": "جهة تنظيمية",
    "Managed By": "تُدار بواسطة",
    "Related Entity": "جهة مرتبطة",
    "Replaced By": "استُبدلت بـ",
    "Former Name Of": "الاسم السابق لـ",
    "Merged With": "اندمجت مع"
    ,
    "Link": "رابط",
    "Image": "صورة",
    "File": "ملف",
    "Text Reference": "مرجع نصي",
    "Screenshot": "لقطة شاشة",
    "Government Role": "منصب حكومي",
    "Business Role": "منصب تجاري",
    "Academic Role": "منصب أكاديمي",
    "Board Member": "عضو مجلس إدارة",
    "Chairman": "رئيس مجلس إدارة",
    "CEO": "رئيس تنفيذي",
    "Minister": "وزير",
    "Director": "مدير",
    "Employee": "موظف",
    "Advisor": "مستشار"
  }
};

Object.assign(translations.en, {
  settings_people: "People Settings",
  settings_organizations: "Organization Settings",
  settings_career: "Career & Position Settings",
  settings_notes: "Notes & Sources Settings",
  settings_appearance: "Appearance & Design",
  settings_appearance_desc: "Customize website colors, fonts, cards, buttons, sidebar, and preview changes before applying.",
  color_system: "Color System",
  color_system_desc: "Enter hex color codes and use the picker for live preview before applying.",
  font_system: "Font System",
  text_groups: "Text Groups",
  component_preview: "Component Preview",
  apply_reset: "Apply / Reset",
  preview_changes: "Preview Changes",
  apply_changes: "Apply Changes",
  reset_to_default: "Reset to Default",
  invalid_hex_warning: "Invalid color code. Use #RGB or #RRGGBB, for example #0A2342.",
  hex_format_hint: "Use #RGB or #RRGGBB.",
  font_family: "Font family",
  font_size: "Font size",
  font_weight: "Font weight",
  letter_spacing: "Letter spacing",
  component_style: "Component Style",
  card_style: "Card radius",
  button_style: "Button radius",
  sidebar_style: "Sidebar width",
  preview_language: "Preview Language"
  ,confirm_delete: "Confirm Delete"
});

Object.assign(translations.ar, {
  settings_people: "إعدادات الأشخاص",
  settings_organizations: "إعدادات الجهات",
  settings_career: "إعدادات المسار المهني والمناصب",
  settings_notes: "إعدادات الملاحظات والمصادر",
  settings_appearance: "إعدادات المظهر والتصميم",
  settings_appearance_desc: "تخصيص ألوان الموقع والخطوط والبطاقات والأزرار والشريط الجانبي مع معاينة التغييرات قبل التطبيق.",
  color_system: "نظام الألوان",
  color_system_desc: "أدخل رموز الألوان بنظام hex واستخدم منتقي اللون للمعاينة المباشرة قبل التطبيق.",
  font_system: "نظام الخطوط",
  text_groups: "مجموعات النص",
  component_preview: "معاينة المكونات",
  apply_reset: "تطبيق / إعادة ضبط",
  preview_changes: "معاينة التغييرات",
  apply_changes: "تطبيق التغييرات",
  reset_to_default: "إعادة للوضع الافتراضي",
  invalid_hex_warning: "رمز اللون غير صحيح. استخدم #RGB أو #RRGGBB مثل #0A2342.",
  hex_format_hint: "استخدم #RGB أو #RRGGBB.",
  font_family: "نوع الخط",
  font_size: "حجم الخط",
  font_weight: "سماكة الخط",
  letter_spacing: "تباعد الحروف",
  component_style: "نمط المكونات",
  card_style: "استدارة البطاقات",
  button_style: "استدارة الأزرار",
  sidebar_style: "عرض الشريط الجانبي",
  preview_language: "لغة المعاينة"
  ,confirm_delete: "تأكيد الحذف"
});

function displayValue(value, language) {
  if (!value) return value;
  const dynamic = window.settingOptionLabels?.[language]?.[value];
  if (dynamic) return dynamic;
  return language === "ar" ? (valueLabels.ar[value] || value) : value;
}

function applyLanguage(language) {
  const dictionary = translations[language] || translations.en;
  document.documentElement.lang = language;
  document.documentElement.dir = language === "ar" ? "rtl" : "ltr";
  localStorage.setItem("smartDatabaseLanguage", language);

  document.querySelectorAll("[data-i18n]").forEach((element) => {
    const key = element.dataset.i18n;
    if (dictionary[key]) element.textContent = dictionary[key];
  });

  document.querySelectorAll("[data-i18n-placeholder]").forEach((element) => {
    const key = element.dataset.i18nPlaceholder;
    if (dictionary[key]) element.placeholder = dictionary[key];
  });

  document.querySelectorAll("[data-option-label]").forEach((option) => {
    option.textContent = displayValue(option.dataset.optionLabel, language);
  });

  document.querySelectorAll("[data-value-label]").forEach((element) => {
    const value = element.dataset.valueLabel;
    if (value && value !== "None") element.textContent = displayValue(value, language);
  });

  document.querySelectorAll("[data-bilingual-en]").forEach((element) => {
    element.textContent = language === "ar" ? (element.dataset.bilingualAr || element.dataset.bilingualEn) : element.dataset.bilingualEn;
  });
}

function setupImagePreview() {
  document.querySelectorAll("[data-preview-input]").forEach((input) => {
    input.addEventListener("change", () => {
      const file = input.files?.[0];
      const wrapper = input.closest(".upload-preview");
      const preview = wrapper?.querySelector("[data-image-preview]");
      const fallback = wrapper?.querySelector("[data-image-fallback]");
      if (!file || !preview || !fallback) return;
      preview.src = URL.createObjectURL(file);
      preview.classList.remove("hidden");
      fallback.classList.add("hidden");
    });
  });
}

function setupModals() {
  const closeModal = (modal) => {
    modal.classList.remove("open");
    modal.setAttribute("aria-hidden", "true");
  };
  document.querySelectorAll("[data-modal-open]").forEach((button) => {
    button.addEventListener("click", () => {
      const parentModal = button.closest(".modal");
      if (parentModal) closeModal(parentModal);
      const modal = document.getElementById(button.dataset.modalOpen);
      if (!modal) return;
      modal.classList.add("open");
      modal.setAttribute("aria-hidden", "false");
    });
  });
  document.querySelectorAll("[data-modal-close]").forEach((button) => {
    button.addEventListener("click", () => closeModal(button.closest(".modal")));
  });
  document.querySelectorAll(".modal").forEach((modal) => {
    modal.addEventListener("click", (event) => {
      if (event.target === modal) closeModal(modal);
    });
  });
  document.querySelectorAll("[data-modal-choice]").forEach((button) => {
    button.addEventListener("click", () => {
      const dialog = button.closest(".modal-dialog");
      const choice = button.dataset.modalChoice;
      dialog.querySelectorAll("[data-modal-choice]").forEach((item) => item.classList.toggle("active", item === button));
      dialog.querySelectorAll("[data-choice-panel]").forEach((panel) => {
        panel.classList.toggle("hidden", panel.dataset.choicePanel !== choice);
      });
    });
  });
}

function sourceRowTemplate() {
  const sourceTypes = window.settingOptionLists?.source_type?.length
    ? window.settingOptionLists.source_type
    : ["Link", "Image", "File", "Text Reference", "Screenshot", "Other"];
  return `
    <div class="source-row">
      <label><span data-i18n="source_type">Source Type</span>
        <select name="source_type">
          ${sourceTypes.map((item) => `<option value="${item}" data-option-label="${item}">${displayValue(item, document.documentElement.lang)}</option>`).join("")}
        </select>
      </label>
      <label><span data-i18n="source_title">Source Title</span><input name="source_title"></label>
      <label><span data-i18n="source_url">URL</span><input name="source_url" type="url"></label>
      <label><span data-i18n="source_file">Upload File</span><input name="source_file" type="file" accept=".jpg,.jpeg,.png,.webp,.pdf,.doc,.docx,.xlsx,.pptx,.txt"></label>
      <label class="full-span"><span data-i18n="text_reference">Text Reference</span><textarea name="source_text_reference" rows="2"></textarea></label>
      <label class="full-span"><span data-i18n="notes">Notes</span><input name="source_notes"></label>
      <button class="text-danger" type="button" data-remove-source><i class="fa-solid fa-trash"></i> <span data-i18n="delete">Delete</span></button>
    </div>
  `;
}

function setupSources() {
  document.querySelectorAll("[data-add-source]").forEach((button) => {
    button.addEventListener("click", () => {
      const builder = button.closest("[data-source-builder]");
      const list = builder?.querySelector("[data-source-list]");
      if (!list) return;
      list.insertAdjacentHTML("beforeend", sourceRowTemplate());
      applyLanguage(document.documentElement.lang || "en");
    });
  });
  document.addEventListener("click", (event) => {
    const remove = event.target.closest("[data-remove-source]");
    if (remove) remove.closest(".source-row")?.remove();
  });
}

function setupSettingsPreview() {
  const select = document.querySelector("[data-preview-select]");
  const badge = document.querySelector("[data-preview-badge]");
  const badgeCopies = document.querySelectorAll("[data-preview-badge-copy]");
  const rows = document.querySelectorAll("[data-preview-option]");
  const form = document.querySelector("[data-option-form]");
  if (!select || !badge) return;

  const render = (row) => {
    const language = document.documentElement.lang || "en";
    const label = language === "ar" ? (row.dataset.labelAr || row.dataset.labelEn) : row.dataset.labelEn;
    const icon = row.dataset.icon || "fa-circle";
    const color = row.dataset.color || "#64748b";
    select.innerHTML = `<option>${label}</option>`;
    badge.innerHTML = `<i class="fa-solid ${icon}"></i> ${label}`;
    badge.style.background = `${color}22`;
    badge.style.color = color;
    badgeCopies.forEach((copy) => {
      copy.innerHTML = badge.innerHTML;
      copy.style.background = badge.style.background;
      copy.style.color = badge.style.color;
    });
  };

  rows.forEach((row) => row.addEventListener("click", () => render(row)));
  if (rows[0]) render(rows[0]);

  const renderDraft = () => {
    if (!form) return;
    const draft = {
      dataset: {
        labelEn: form.querySelector('[name="label_en"]')?.value || "Preview option",
        labelAr: form.querySelector('[name="label_ar"]')?.value || form.querySelector('[name="label_en"]')?.value || "Preview option",
        icon: form.querySelector('[name="icon"]')?.value || "fa-circle",
        color: form.querySelector('[name="color"]')?.value || "#64748b",
      },
    };
    render(draft);
  };

  form?.querySelectorAll('[name="label_en"], [name="label_ar"], [name="icon"], [name="color"]').forEach((input) => {
    input.addEventListener("input", renderDraft);
  });

  document.querySelectorAll("[data-category-prefill]").forEach((button) => {
    button.addEventListener("click", () => {
      document.querySelector("[data-option-category]").value = button.dataset.categoryPrefill;
    });
  });

  document.querySelectorAll("[data-edit-option]").forEach((button) => {
    button.addEventListener("click", () => {
      const modal = document.getElementById("option-modal");
      if (!form || !modal) return;
      form.action = `/settings/options/${button.dataset.id}/edit`;
      form.querySelector('[name="category"]').closest("label").classList.add("hidden");
      form.querySelector('[name="key"]').closest("label").classList.add("hidden");
      form.querySelector('[name="label_en"]').value = button.dataset.labelEn || "";
      form.querySelector('[name="label_ar"]').value = button.dataset.labelAr || "";
      form.querySelector('[name="icon"]').value = button.dataset.icon || "";
      form.querySelector('[name="color"]').value = button.dataset.color || "#64748b";
      renderDraft();
      modal.classList.add("open");
      modal.setAttribute("aria-hidden", "false");
    });
  });

  document.querySelectorAll('[data-modal-open="option-modal"]').forEach((button) => {
    button.addEventListener("click", () => {
      const form = document.querySelector("[data-option-form]");
      if (!form) return;
      form.action = "/settings/options/add";
      form.querySelector('[name="category"]').closest("label").classList.remove("hidden");
      form.querySelector('[name="key"]').closest("label").classList.remove("hidden");
      form.reset();
      if (button.dataset.categoryPrefill) {
        form.querySelector('[name="category"]').value = button.dataset.categoryPrefill;
      }
      renderDraft();
    });
  });
}

function setupConfirmations() {
  const modal = document.getElementById("confirm-delete-modal");
  const message = modal?.querySelector("[data-confirm-modal-message]");
  const accept = modal?.querySelector("[data-confirm-accept]");
  const cancel = modal?.querySelector("[data-confirm-cancel]");
  let pendingForm = null;

  const close = () => {
    modal?.classList.remove("open");
    modal?.setAttribute("aria-hidden", "true");
    pendingForm = null;
  };

  accept?.addEventListener("click", () => {
    if (!pendingForm) return;
    pendingForm.dataset.confirmed = "true";
    const form = pendingForm;
    close();
    form.requestSubmit();
  });
  cancel?.addEventListener("click", close);
  modal?.addEventListener("click", (event) => {
    if (event.target === modal) close();
  });

  document.querySelectorAll("[data-confirm-message]").forEach((form) => {
    form.addEventListener("submit", (event) => {
      if (form.dataset.confirmed === "true") {
        delete form.dataset.confirmed;
        return;
      }
      event.preventDefault();
      if (!modal || !message) {
        if (window.confirm(form.dataset.confirmMessage || "Are you sure?")) {
          form.dataset.confirmed = "true";
          form.requestSubmit();
        }
        return;
      }
      pendingForm = form;
      message.textContent = form.dataset.confirmMessage || "Are you sure?";
      modal.classList.add("open");
      modal.setAttribute("aria-hidden", "false");
    });
  });
}

function confirmPersonDelete() {
  return window.confirm(
    "Are you sure you want to delete this person? This may also remove related relationships, positions, notes, and sources.\n\n" +
      "هل أنت متأكد أنك تريد حذف هذا الشخص؟ قد يؤدي ذلك أيضاً إلى حذف العلاقات والمناصب والملاحظات والمصادر المرتبطة به."
  );
}

function confirmOrganizationDelete() {
  return window.confirm(
    "Are you sure you want to delete this organization? This may also remove related positions, notes, sources, and organization relationships.\n\n" +
      "هل أنت متأكد أنك تريد حذف هذه الجهة؟ قد يؤدي ذلك أيضاً إلى حذف المناصب والملاحظات والمصادر والعلاقات المرتبطة بها."
  );
}

window.confirmPersonDelete = confirmPersonDelete;
window.confirmOrganizationDelete = confirmOrganizationDelete;

function setupAppearanceSettings() {
  const form = document.querySelector("[data-appearance-form]");
  const preview = document.querySelector("[data-appearance-preview-surface]");
  if (!form || !preview) return;

  const cssNames = {
    primary_color: ["--primary-color", "--accent"],
    secondary_color: ["--secondary-color", "--accent-2"],
    accent_color: ["--accent-color", "--focus-color"],
    app_background: ["--app-bg", "--background-color", "--soft"],
    card_background: ["--surface-color", "--white"],
    sidebar_background: ["--sidebar-bg", "--navy"],
    sidebar_text: ["--sidebar-text"],
    sidebar_active: ["--sidebar-active"],
    heading_text: ["--heading-color", "--navy-2"],
    body_text: ["--body-text", "--body-text-color", "--ink"],
    muted_text: ["--muted-text", "--muted-text-color", "--muted"],
    border_color: ["--border-color", "--line"],
    success_color: ["--success-color"],
    warning_color: ["--warning-color"],
    danger_color: ["--danger-color", "--danger"],
    card_radius: ["--card-radius"],
    button_radius: ["--button-radius"],
    sidebar_width: ["--sidebar-width"]
  };
  const hexPattern = /^#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})$/;
  const fontStack = (font) => !font || font === "System Default"
    ? '"Segoe UI", "Tahoma", "Arial", sans-serif'
    : `"${font.replace(/"/g, "")}", "Segoe UI", "Tahoma", "Arial", sans-serif`;

  const setVars = () => {
    form.querySelectorAll("[data-appearance-input]").forEach((input) => {
      const name = input.name;
      let value = input.value.trim();
      const field = input.closest("[data-color-field]");
      if (field) {
        const valid = hexPattern.test(value);
        field.classList.toggle("invalid", !valid);
        if (!valid) return;
      }
      if (name.endsWith("_font_family")) {
        preview.style.setProperty(`--${name.replace("_font_family", "")}-font`, fontStack(value));
        return;
      }
      if (name.endsWith("_font_size")) {
        preview.style.setProperty(`--${name.replace("_font_size", "")}-font-size`, `${value}px`);
        return;
      }
      if (name.endsWith("_font_weight")) {
        preview.style.setProperty(`--${name.replace("_font_weight", "")}-font-weight`, value);
        return;
      }
      if (name.endsWith("_letter_spacing")) {
        preview.style.setProperty(`--${name.replace("_letter_spacing", "")}-letter-spacing`, `${value}px`);
        return;
      }
      (cssNames[name] || []).forEach((cssName) => {
        const needsPx = ["card_radius", "button_radius", "sidebar_width"].includes(name);
        preview.style.setProperty(cssName, needsPx ? `${value}px` : value);
      });
    });
  };

  form.querySelectorAll("[data-color-field]").forEach((field) => {
    const hex = field.querySelector(".hex-input");
    const picker = field.querySelector("[data-color-picker]");
    const reset = field.querySelector("[data-reset-color]");
    if (!hex || !picker) return;
    hex.addEventListener("input", () => {
      if (hexPattern.test(hex.value.trim())) picker.value = hex.value.trim();
      setVars();
    });
    picker.addEventListener("input", () => {
      hex.value = picker.value.toUpperCase();
      setVars();
    });
    reset?.addEventListener("click", () => {
      const defaultColor = field.dataset.defaultColor || "#FFFFFF";
      hex.value = defaultColor;
      picker.value = defaultColor;
      setVars();
    });
  });

  form.querySelectorAll("[data-appearance-input]").forEach((input) => {
    input.addEventListener("input", setVars);
    input.addEventListener("change", setVars);
  });

  document.querySelector("[data-appearance-preview]")?.addEventListener("click", setVars);

  document.querySelector("[data-preview-language]")?.addEventListener("change", (event) => {
    const language = event.target.value;
    preview.dir = language === "ar" ? "rtl" : "ltr";
    preview.querySelectorAll("[data-preview-copy-en]").forEach((element) => {
      element.textContent = language === "ar" ? element.dataset.previewCopyAr : element.dataset.previewCopyEn;
    });
  });

  form.addEventListener("submit", (event) => {
    const invalid = [...form.querySelectorAll("[data-color-field] .hex-input")].some((input) => !hexPattern.test(input.value.trim()));
    if (invalid) {
      event.preventDefault();
      setVars();
    }
  });

  setVars();
}

function setupSettingsSearch() {
  const input = document.querySelector("[data-settings-search]");
  if (!input) return;
  input.addEventListener("input", () => {
    const query = input.value.trim().toLowerCase();
    document.querySelectorAll("[data-settings-row]").forEach((row) => {
      row.classList.toggle("hidden", query && !row.dataset.searchText.includes(query));
    });
  });
}

function setupReviewEditor() {
  let reviewIndex = 1000;
  document.addEventListener("click", (event) => {
    const remove = event.target.closest("[data-remove-review-card]");
    if (remove) {
      const list = remove.closest(".editable-card-list");
      remove.closest("[data-review-card]")?.remove();
      list?.querySelector(".empty")?.remove();
      return;
    }

    const add = event.target.closest("[data-add-review-card]");
    if (!add) return;
    const type = add.dataset.addReviewCard;
    const list = document.querySelector(`[data-review-list="${type}"]`);
    if (!list) return;
    list.querySelector(".empty")?.remove();
    const index = reviewIndex++;
    const html = type === "education" ? `
      <article class="editable-card" data-review-card>
        <label class="checkbox"><input type="checkbox" name="education_create_${index}" value="yes" checked><span data-i18n="create_education">Create education</span></label>
        <div class="form-grid">
          <label><span data-i18n="institution">Institution</span><input name="education_institution_${index}"></label>
          <label><span data-i18n="degree">Degree</span><input name="education_degree_${index}"></label>
          <label><span data-i18n="major">Major</span><input name="education_major_${index}"></label>
          <label><span data-i18n="start_year">Start Year</span><input type="number" name="education_start_year_${index}"></label>
          <label><span data-i18n="end_year">End Year</span><input type="number" name="education_end_year_${index}"></label>
          <label><span data-i18n="graduation_year">Graduation Year</span><input type="number" name="education_graduation_year_${index}"></label>
          <label><span data-i18n="country">Country</span><input name="education_country_${index}"></label>
          <label class="full-span"><span data-i18n="notes">Notes</span><textarea name="education_notes_${index}" rows="2"></textarea></label>
        </div>
        <button class="text-danger" type="button" data-remove-review-card><i class="fa-solid fa-trash"></i> <span data-i18n="remove">Remove</span></button>
      </article>
    ` : `
      <article class="editable-card" data-review-card>
        <label class="checkbox"><input type="checkbox" name="position_create_${index}" value="yes" checked><span data-i18n="create_position">Create position</span></label>
        <div class="form-grid">
          <label><span data-i18n="organization">Organization</span><input name="position_organization_${index}"></label>
          <label><span data-i18n="position_title">Position Title</span><input name="position_title_${index}"></label>
          <label><span data-i18n="department">Department</span><input name="position_department_${index}"></label>
          <label><span data-i18n="start_year">Start Year</span><input type="number" name="position_start_year_${index}"></label>
          <label><span data-i18n="end_year">End Year</span><input type="number" name="position_end_year_${index}"></label>
          <label><span data-i18n="role_type">Role Type</span><input name="position_role_type_${index}" value="Other"></label>
          <label class="checkbox"><input type="checkbox" name="position_is_current_${index}" value="yes" checked><span data-i18n="current_role_checkbox">Current role</span></label>
          <label class="full-span"><span data-i18n="notes">Notes</span><textarea name="position_notes_${index}" rows="2"></textarea></label>
        </div>
        <button class="text-danger" type="button" data-remove-review-card><i class="fa-solid fa-trash"></i> <span data-i18n="remove">Remove</span></button>
      </article>
    `;
    list.insertAdjacentHTML("beforeend", html);
    applyLanguage(document.documentElement.lang || "en");
  });
}

document.addEventListener("DOMContentLoaded", () => {
  applyLanguage(localStorage.getItem("smartDatabaseLanguage") || "en");

  document.querySelector("[data-language-toggle]")?.addEventListener("click", () => {
    applyLanguage(document.documentElement.lang === "ar" ? "en" : "ar");
  });

  document.querySelectorAll("textarea").forEach((textarea) => {
    const resize = () => {
      textarea.style.height = "auto";
      textarea.style.height = `${textarea.scrollHeight}px`;
    };
    textarea.addEventListener("input", resize);
    resize();
  });

  setupImagePreview();
  setupModals();
  setupSources();
  setupSettingsPreview();
  setupAppearanceSettings();
  setupSettingsSearch();
  setupConfirmations();
  setupReviewEditor();
  document.querySelectorAll("[data-confirm-delete]").forEach((form) => {
    form.addEventListener("submit", (event) => {
      if (!window.confirm("Delete this backup?")) event.preventDefault();
    });
  });
});

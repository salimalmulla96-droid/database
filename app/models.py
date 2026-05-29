from datetime import datetime

from sqlalchemy import Boolean, Column, Date, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from .database import Base


class Person(Base):
    __tablename__ = "people"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    second_name = Column(String, nullable=True)
    third_name = Column(String, nullable=True)
    fourth_name = Column(String, nullable=True)
    family_name = Column(String, index=True, nullable=True)
    tribe_name = Column(String, index=True, nullable=True)
    image_path = Column(String, nullable=True)
    gender = Column(String, nullable=True)
    nationality = Column(String, index=True, nullable=True)
    status = Column(String, index=True, nullable=True)
    category = Column(String, index=True, nullable=True)
    birth_date = Column(Date, nullable=True)
    birth_place = Column(String, nullable=True)
    education = Column(String, nullable=True)
    university = Column(String, nullable=True)
    major = Column(String, nullable=True)
    graduation_year = Column(Integer, nullable=True)
    current_role = Column(String, nullable=True)
    main_field = Column(String, nullable=True)
    known_for = Column(Text, nullable=True)
    achievements = Column(Text, nullable=True)
    public_summary = Column(Text, nullable=True)
    biography = Column(Text, nullable=True)
    private_notes = Column(Text, nullable=True)
    tags = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    positions = relationship("Position", back_populates="person")
    relationships_from = relationship(
        "Relationship",
        foreign_keys="Relationship.from_person_id",
        back_populates="from_person",
    )
    relationships_to = relationship(
        "Relationship",
        foreign_keys="Relationship.to_person_id",
        back_populates="to_person",
    )

    @property
    def display_name(self):
        return (
            " ".join(
                part
                for part in [
                    self.first_name,
                    self.second_name,
                    self.third_name,
                    self.fourth_name,
                    self.family_name,
                ]
                if part
            )
            or "Unnamed Person"
        )


class Organization(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    alternative_name = Column(String, index=True, nullable=True)
    image_path = Column(String, nullable=True)
    organization_type = Column(String, index=True, nullable=True)
    status = Column(String, index=True, nullable=True)
    emirate = Column(String, index=True, nullable=True)
    founded_year = Column(Integer, nullable=True)
    founder = Column(String, nullable=True)
    headquarters = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    tags = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    positions = relationship("Position", back_populates="organization")
    relationships_from = relationship(
        "OrganizationRelationship",
        foreign_keys="OrganizationRelationship.from_organization_id",
        back_populates="from_organization",
    )
    relationships_to = relationship(
        "OrganizationRelationship",
        foreign_keys="OrganizationRelationship.to_organization_id",
        back_populates="to_organization",
    )

    @property
    def display_name(self):
        return self.name or self.alternative_name or "Unnamed Organization"


class Position(Base):
    __tablename__ = "positions"

    id = Column(Integer, primary_key=True, index=True)
    person_id = Column(Integer, ForeignKey("people.id"), nullable=False)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    position_title = Column(String, nullable=False)
    department = Column(String, nullable=True)
    start_year = Column(Integer, nullable=True)
    end_year = Column(Integer, nullable=True)
    is_current = Column(Boolean, default=False)
    role_type = Column(String, nullable=True)
    notes = Column(Text, nullable=True)
    source_type = Column(String, nullable=True)
    source_title = Column(String, nullable=True)
    source_url = Column(String, nullable=True)
    confidence = Column(String, nullable=True)
    privacy_level = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    person = relationship("Person", back_populates="positions")
    organization = relationship("Organization", back_populates="positions")


class Relationship(Base):
    __tablename__ = "relationships"

    id = Column(Integer, primary_key=True, index=True)
    from_person_id = Column(Integer, ForeignKey("people.id"), nullable=False)
    to_person_id = Column(Integer, ForeignKey("people.id"), nullable=False)
    relationship_type = Column(String, nullable=False)
    notes = Column(Text, nullable=True)
    source_type = Column(String, nullable=True)
    source_title = Column(String, nullable=True)
    source_url = Column(String, nullable=True)
    confidence = Column(String, nullable=True)
    privacy_level = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    from_person = relationship(
        "Person", foreign_keys=[from_person_id], back_populates="relationships_from"
    )
    to_person = relationship(
        "Person", foreign_keys=[to_person_id], back_populates="relationships_to"
    )


class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    entity_type = Column(String, index=True, nullable=False)
    entity_id = Column(Integer, index=True, nullable=False)
    note_type = Column(String, index=True, nullable=False)
    title = Column(String, nullable=True)
    content = Column(Text, nullable=False)
    date_text = Column(String, nullable=True)
    source = Column(String, nullable=True)
    is_private = Column(Boolean, default=False)
    source_type = Column(String, nullable=True)
    source_title = Column(String, nullable=True)
    source_url = Column(String, nullable=True)
    confidence = Column(String, nullable=True)
    privacy_level = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    sources = relationship("Source")


class OrganizationRelationship(Base):
    __tablename__ = "organization_relationships"

    id = Column(Integer, primary_key=True, index=True)
    from_organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    to_organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    relationship_type = Column(String, nullable=False)
    notes = Column(Text, nullable=True)
    source_type = Column(String, nullable=True)
    source_title = Column(String, nullable=True)
    source_url = Column(String, nullable=True)
    confidence = Column(String, nullable=True)
    privacy_level = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    from_organization = relationship(
        "Organization",
        foreign_keys=[from_organization_id],
        back_populates="relationships_from",
    )
    to_organization = relationship(
        "Organization",
        foreign_keys=[to_organization_id],
        back_populates="relationships_to",
    )


class Source(Base):
    __tablename__ = "sources"

    id = Column(Integer, primary_key=True, index=True)
    note_id = Column(Integer, ForeignKey("notes.id"), nullable=True)
    entity_type = Column(String, index=True, nullable=False)
    entity_id = Column(Integer, index=True, nullable=False)
    source_type = Column(String, index=True, nullable=False)
    title = Column(String, nullable=True)
    url = Column(String, nullable=True)
    file_path = Column(String, nullable=True)
    text_reference = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class Education(Base):
    __tablename__ = "education"

    id = Column(Integer, primary_key=True, index=True)
    person_id = Column(Integer, ForeignKey("people.id"), nullable=False)
    institution = Column(String, nullable=False)
    degree = Column(String, nullable=True)
    major = Column(String, nullable=True)
    start_year = Column(Integer, nullable=True)
    end_year = Column(Integer, nullable=True)
    graduation_year = Column(Integer, nullable=True)
    country = Column(String, nullable=True)
    notes = Column(Text, nullable=True)
    source_type = Column(String, nullable=True)
    source_title = Column(String, nullable=True)
    source_url = Column(String, nullable=True)
    confidence = Column(String, nullable=True)
    privacy_level = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    person = relationship("Person")


class SettingOption(Base):
    __tablename__ = "setting_options"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String, index=True, nullable=False)
    key = Column(String, index=True, nullable=False)
    label_en = Column(String, nullable=False)
    label_ar = Column(String, nullable=True)
    icon = Column(String, nullable=True)
    color = Column(String, nullable=True)
    sort_order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    is_system = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class AppearanceSetting(Base):
    __tablename__ = "appearance_settings"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, index=True, nullable=False, unique=True)
    value = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ExtractedItem(Base):
    __tablename__ = "extracted_items"

    id = Column(Integer, primary_key=True, index=True)
    raw_text = Column(Text, nullable=False)
    input_type = Column(String, index=True, nullable=True)
    extracted_json = Column(Text, nullable=True)
    source_type = Column(String, nullable=True)
    source_title = Column(String, nullable=True)
    source_url = Column(String, nullable=True)
    confidence = Column(String, nullable=True)
    privacy_level = Column(String, nullable=True)
    status = Column(String, index=True, default="Pending Review")
    duplicate_status = Column(String, index=True, default="Not Checked")
    created_at = Column(DateTime, default=datetime.utcnow)
    reviewed_at = Column(DateTime, nullable=True)
    notes = Column(Text, nullable=True)


class DuplicateRecord(Base):
    __tablename__ = "duplicate_records"

    id = Column(Integer, primary_key=True, index=True)
    entity_type = Column(String, index=True, nullable=False)
    entity_id_1 = Column(Integer, index=True, nullable=False)
    entity_id_2 = Column(Integer, index=True, nullable=False)
    similarity_score = Column(Integer, default=0)
    match_reason = Column(Text, nullable=True)
    status = Column(String, index=True, default="Possible Duplicate")
    created_at = Column(DateTime, default=datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)


class ExportLog(Base):
    __tablename__ = "export_logs"

    id = Column(Integer, primary_key=True, index=True)
    export_type = Column(String, index=True, nullable=False)
    file_path = Column(String, nullable=False)
    include_private = Column(Boolean, default=False)
    include_sensitive = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    notes = Column(Text, nullable=True)


class BackupLog(Base):
    __tablename__ = "backup_logs"

    id = Column(Integer, primary_key=True, index=True)
    file_path = Column(String, nullable=False)
    backup_type = Column(String, default="Full")
    people_count = Column(Integer, default=0)
    organization_count = Column(Integer, default=0)
    notes_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

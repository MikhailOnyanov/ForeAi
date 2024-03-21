from __future__ import annotations

# импортируем классы, используемые для определения атрибутов модели
from sqlalchemy import ForeignKey

# импортируем объекты для создания отношения между объектами
from sqlalchemy.orm import Mapped
from Curs2024.db import Base
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from typing import List, ClassVar


# relation between works and mistakes
class WorksMistakes(Base):
    __tablename__ = "works_mistakes"
    record_id: Mapped[int] = mapped_column(primary_key=True)
    work_code: Mapped[int] = mapped_column(ForeignKey("works.work_code"))
    mistake_code: Mapped[int] = mapped_column(ForeignKey("mistakes_codes.mistake_code"))
    mistake_code_raw: ClassVar[str]
    mistakes_count: Mapped[int] = mapped_column()
    editable_attributes: ClassVar = ['record_id', 'work_code', 'mistake_code', 'mistakes_count']

    def to_dict(self):
        return {
            "record_id": self.record_id,
            "work_code": self.work_code,
            "mistake_code": self.mistake_code,
            "mistakes_count": self.mistakes_count
        }

    def __repr__(self) -> str:
        return f"WorksMistakes(" \
               f"record_id={self.record_id!r}, " \
               f"work_code={self.work_code}, " \
               f"mistake_code={self.mistake_code!r}, " \
               f"mistake_code_raw={self.mistake_code_raw!r}, " \
               f"mistakes_count={self.mistakes_count!r}" \
               f")"


# parent for MistakesCodes
class MistakesTypes(Base):
    __tablename__ = "mistakes_types"
    mistake_type_id: Mapped[int] = mapped_column(primary_key=True)
    mistake_type_transcript: Mapped[str] = mapped_column(nullable=False)
    # refers to mistakes_codes table, sets up a collection of codes for each type
    mistakes_codes: Mapped[List["MistakesCodes"]] = relationship(back_populates="mistake_type")
    editable_attributes: ClassVar = ['mistake_type_transcript']

    def to_dict(self):
        return {
            "mistake_type_id": self.mistake_type_id,
            "mistake_type_transcript": self.mistake_type_transcript
        }

    def __repr__(self) -> str:
        return f"MistakesTypes(" \
               f"mistake_type_id={self.mistake_type_id!r}," \
               f" mistake_type_transcript={self.mistake_type_transcript!r}" \
               f")"


# children for MistakesTypes
class MistakesCodes(Base):
    __tablename__ = "mistakes_codes"
    # "06.02", "07.12" ...
    mistake_code: Mapped[str] = mapped_column(primary_key=True)
    # lexical, syn, sem, pos
    mistake_type_id: Mapped[int] = mapped_column(ForeignKey("mistakes_types.mistake_type_id"))
    # description for mistake
    mistake_code_transcript: Mapped[str] = mapped_column(nullable=False)
    # children refers to parent
    mistake_type: Mapped["MistakesTypes"] = relationship(back_populates="mistakes_codes")
    editable_attributes: ClassVar = ['mistake_type_id', 'mistake_code_transcript']

    def to_dict(self):
        return {
            "mistake_code": self.mistake_code,
            "mistake_type_id": self.mistake_type_id,
            "mistake_code_transcript": self.mistake_code_transcript
        }

    def __repr__(self) -> str:
        return f"MistakesCode(" \
               f"mistake_code={self.mistake_code!r}," \
               f" mistake_code_transcript={self.mistake_code_transcript!r}," \
               f" mistake_type_id={self.mistake_type_id!r}" \
               f")"


class EducationProfile(Base):
    __tablename__ = "education_profiles"
    education_profile_number: Mapped[str] = mapped_column(primary_key=True)
    grade_of_education: Mapped[str] = mapped_column(nullable=True)
    form_of_education: Mapped[str] = mapped_column(nullable=True)
    discipline_title: Mapped[str] = mapped_column(nullable=True)
    course: Mapped[int] = mapped_column()
    # refers to Works table, sets up a collection of Works for each type
    related_works: Mapped[List["Works"]] = relationship(back_populates="education_profile")
    editable_attributes: ClassVar = ['education_profile_number', 'grade_of_education', 'form_of_education',
                                     'discipline_title', 'course', 'record_id']

    def to_dict(self):
        return {
            "education_profile_number": self.education_profile_number,
            "grade_of_education": self.grade_of_education,
            "form_of_education": self.form_of_education,
            "discipline_title": self.discipline_title,
            "course": self.course
        }

    def __repr__(self) -> str:
        return f"EducationProfile(" \
               f"education_profile_number={self.year!r}," \
               f"grade_of_education={self.grade_of_education!r}," \
               f"form_of_education={self.form_of_education!r}," \
               f"discipline_title={self.discipline_title!r}," \
               f"course={self.course})"


class Works(Base):
    __tablename__ = "works"
    work_code: Mapped[int] = mapped_column(primary_key=True)
    year: Mapped[str] = mapped_column(nullable=False)
    mistakes: Mapped[List["WorksMistakes"]] = relationship()
    education_profile_number: Mapped["str"] = mapped_column(ForeignKey("education_profiles.education_profile_number"),
                                                            nullable=True)
    # children refers to parent
    education_profile: Mapped["EducationProfile"] = relationship(back_populates="related_works")
    editable_attributes: ClassVar = ['work_code', 'year', 'education_profile_number']

    def to_dict(self):
        return {
            "work_code": self.work_code,
            "year": self.year,
            "education_profile_number": self.education_profile_number
        }

    def __repr__(self) -> str:
        return f"Works(" \
               f"year={self.year!r}," \
               f"work_code={self.work_code!r}," \
               f"education_profile_number={self.education_profile_number})"

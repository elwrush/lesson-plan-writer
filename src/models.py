"""
Pydantic models for Lesson Plan Writer 3.

Replaces manual REQUIRED_FIELDS validation in three scripts:
  - build_lesson_pdf.py
  - json_to_markdown.py
  - json_to_pdf.py
"""

import re
from typing import Literal

from pydantic import BaseModel, Field, field_validator

CEFR_LEVEL = Literal["A1", "A2", "B1", "B2", "C1", "C2"]
INTERACTION = Literal["T-Ss", "Ss-Ss", "S-S", "S-Ss", "T-S", "Group", "Individual"]
SHAPE = Literal[
    "ESA",
    "PPP",
    "TBL",
    "Test-Teach-Test",
    "Guided Discovery",
    "Receptive Skills",
    "Productive Skills",
    "Text-based Presentation",
    "Language Practice",
]


class Material(BaseModel):
    name: str
    type: str
    page: str | None = None


class Stage(BaseModel):
    stage_number: int
    stage: str
    stage_aim: str
    procedure: str
    time: str
    interaction: INTERACTION

    @field_validator("stage_number")
    @classmethod
    def positive_stage(cls, v: int) -> int:
        if v < 1:
            raise ValueError(f"Stage number must be >= 1, got {v}")
        return v

    @field_validator("time")
    @classmethod
    def time_format(cls, v: str) -> str:
        if not re.match(r"^\d+(?:-\d+)?\s*min\.?$", v, re.IGNORECASE):
            raise ValueError(f"Time must match 'N min.' format, got '{v}'")
        return v


class LessonPlanMeta(BaseModel):
    shape: SHAPE
    shape_name: str
    cefr_level: CEFR_LEVEL
    class_name: str = Field(alias="class")
    stages: list[Stage]

    @field_validator("stages")
    @classmethod
    def non_empty_stages(cls, v: list[Stage]) -> list[Stage]:
        if not v:
            raise ValueError("stages must be a non-empty array")
        return v


class LessonPlanFrontmatter(BaseModel):
    """Flat frontmatter model for YAML in lesson.md files.

    Unlike LessonPlan (which nests meta under lesson_plan.),
    build_lesson_pdf.py reads a flat YAML frontmatter.
    """

    topic: str
    teacher: str
    formatted_date: str
    duration: str
    cefr_level: CEFR_LEVEL
    class_name: str = Field(alias="class")
    shape: SHAPE
    shape_name: str


class LessonPlan(BaseModel):
    teacher: str
    duration: str
    date: str
    topic: str
    materials: list[Material] = Field(default_factory=list)
    lesson_plan: LessonPlanMeta

    @field_validator("date")
    @classmethod
    def validate_date(cls, v: str) -> str:
        patterns = [
            r"^\d{1,2}/\d{1,2}/\d{2,4}$",
            r"^\d{1,2}\s+\w+\s+\d{4}$",
            r"^\d{6}$",
        ]
        if not any(re.match(p, v) for p in patterns):
            raise ValueError(f"Date '{v}' must match dd/mm/yy, d Month YYYY, or ddmmyy")
        return v

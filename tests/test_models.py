"""
test_models.py — Red-green tests for Pydantic lesson plan models.

Phases:
  Red:   Run tests → confirm FAIL (models don't exist yet)
  Green: Write models → run tests → confirm PASS
"""

import json
import sys
from pathlib import Path

import pytest
from pydantic import ValidationError

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.models import LessonPlan, Material, Stage  # noqa: E402

# ── Fixtures ─────────────────────────────────────────────────────────────


@pytest.fixture
def valid_stage_data():
    return {
        "stage_number": 1,
        "stage": "Lead-in",
        "stage_aim": "To activate interest",
        "procedure": "Show pictures and ask questions",
        "time": "5 min.",
        "interaction": "T-Ss",
    }


@pytest.fixture
def valid_lesson_plan_data(valid_stage_data):
    return {
        "teacher": "E. L. Wrus",
        "duration": "50 min.",
        "date": "050726",
        "topic": "What Connects Us",
        "materials": [
            {"name": "Coursebook p.45", "type": "coursebook"},
        ],
        "lesson_plan": {
            "shape": "ESA",
            "shape_name": "Engage-Study-Activate",
            "cefr_level": "B1",
            "class": "M3",
            "stages": [valid_stage_data],
        },
    }


# ── Stage tests ──────────────────────────────────────────────────────────


class TestStage:
    def test_valid_stage(self, valid_stage_data):
        stage = Stage.model_validate(valid_stage_data)
        assert stage.stage_number == 1
        assert stage.interaction == "T-Ss"

    def test_zero_stage_number(self, valid_stage_data):
        data = dict(valid_stage_data, stage_number=0)
        with pytest.raises(ValidationError):
            Stage.model_validate(data)

    def test_negative_stage_number(self, valid_stage_data):
        data = dict(valid_stage_data, stage_number=-1)
        with pytest.raises(ValidationError):
            Stage.model_validate(data)

    def test_invalid_time_format(self, valid_stage_data):
        data = dict(valid_stage_data, time="5 minutes")
        with pytest.raises(ValidationError):
            Stage.model_validate(data)

    def test_invalid_interaction(self, valid_stage_data):
        data = dict(valid_stage_data, interaction="Invalid")
        with pytest.raises(ValidationError):
            Stage.model_validate(data)

    def test_missing_stage_field(self, valid_stage_data):
        data = dict(valid_stage_data)
        del data["stage"]
        with pytest.raises(ValidationError):
            Stage.model_validate(data)


# ── LessonPlan tests ─────────────────────────────────────────────────────


class TestLessonPlan:
    def test_valid_lesson_plan(self, valid_lesson_plan_data):
        plan = LessonPlan.model_validate(valid_lesson_plan_data)
        assert plan.teacher == "E. L. Wrus"
        assert plan.lesson_plan.shape == "ESA"
        assert len(plan.lesson_plan.stages) == 1
        assert plan.lesson_plan.class_name == "M3"

    def test_class_alias(self, valid_lesson_plan_data):
        """'class' field is aliased to class_name."""
        plan = LessonPlan.model_validate(valid_lesson_plan_data)
        assert plan.lesson_plan.class_name == "M3"
        # Serialize back and check 'class' key is present
        dumped = plan.lesson_plan.model_dump(by_alias=True)
        assert "class" in dumped
        assert dumped["class"] == "M3"

    def test_invalid_date(self, valid_lesson_plan_data):
        data = dict(valid_lesson_plan_data, date="not-a-date")
        with pytest.raises(ValidationError):
            LessonPlan.model_validate(data)

    def test_invalid_cefr_level(self, valid_lesson_plan_data):
        data = dict(valid_lesson_plan_data)
        data["lesson_plan"]["cefr_level"] = "D3"
        with pytest.raises(ValidationError):
            LessonPlan.model_validate(data)

    def test_invalid_shape(self, valid_lesson_plan_data):
        data = dict(valid_lesson_plan_data)
        data["lesson_plan"]["shape"] = "Unknown"
        with pytest.raises(ValidationError):
            LessonPlan.model_validate(data)

    def test_missing_top_level_field(self, valid_lesson_plan_data):
        data = dict(valid_lesson_plan_data)
        del data["teacher"]
        with pytest.raises(ValidationError):
            LessonPlan.model_validate(data)

    def test_empty_stages_rejected(self, valid_lesson_plan_data):
        """Empty stages list is rejected — every lesson plan needs at least one stage."""
        data = dict(valid_lesson_plan_data)
        data["lesson_plan"]["stages"] = []
        with pytest.raises(ValidationError):
            LessonPlan.model_validate(data)

    def test_round_trip_json(self, valid_lesson_plan_data):
        plan = LessonPlan.model_validate(valid_lesson_plan_data)
        serialized = json.loads(plan.model_dump_json(by_alias=True))
        restored = LessonPlan.model_validate(serialized)
        assert restored.teacher == plan.teacher
        assert restored.lesson_plan.shape == plan.lesson_plan.shape
        assert restored.lesson_plan.class_name == plan.lesson_plan.class_name

    def test_empty_materials(self, valid_lesson_plan_data):
        data = dict(valid_lesson_plan_data)
        data["materials"] = []
        plan = LessonPlan.model_validate(data)
        assert plan.materials == []

    def test_missing_materials_default(self, valid_lesson_plan_data):
        """materials should default to empty list when missing."""
        data = dict(valid_lesson_plan_data)
        del data["materials"]
        plan = LessonPlan.model_validate(data)
        assert plan.materials == []


# ── Material tests ───────────────────────────────────────────────────────


class TestMaterial:
    def test_valid_material(self):
        mat = Material(name="Audio Track 1", type="audio")
        assert mat.name == "Audio Track 1"

    def test_material_with_page(self):
        mat = Material(name="Handout 1", type="handout", page="3")
        assert mat.page == "3"

    def test_material_missing_required(self):
        with pytest.raises(ValidationError):
            Material.model_validate({"name": "Test"})

    def test_material_default_page_none(self):
        mat = Material(name="Video", type="video")
        assert mat.page is None

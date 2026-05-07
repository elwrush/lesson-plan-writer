"""
test_json_to_pdf.py - Tests for json_to_pdf conversion script
"""

import json
import os
import copy
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from json_to_pdf import (
    validate_json,
    normalize_topic,
    get_output_path,
    render_template,
    convert_json_to_pdf,
    PROJECT_ROOT,
)

# Sample valid lesson plan data for testing
VALID_LESSON_PLAN = {
    "teacher": "Test Teacher",
    "duration": "45 minutes",
    "date": "050726",
    "topic": "Test Topic",
    "objective": "Test objective",
    "materials": "Test materials",
    "lesson_plan": {
        "shape": "A",
        "shape_name": "Text-based Presentation",
        "cefr_level": "B1",
        "class": "M3",
        "stages": [
            {
                "stage_number": 1,
                "stage": "Lead-in",
                "stage_aim": "To lead-in",
                "procedure": "- Step 1\n- Step 2",
                "time": 5,
                "interaction": "T-Ss",
            }
        ],
    },
    "transcript": "none",
    "answer-key": "none",
}


class TestValidateJson:
    """Tests for JSON validation."""

    def test_valid_json_passes(self):
        """TC-01 style: Valid JSON should pass validation."""
        errors = validate_json(VALID_LESSON_PLAN)
        assert len(errors) == 0

    def test_missing_teacher_fails(self):
        """TC-03 style: Missing required field should fail."""
        data = copy.deepcopy(VALID_LESSON_PLAN)
        del data["teacher"]
        errors = validate_json(data)
        assert len(errors) > 0
        assert any("teacher" in e for e in errors)

    def test_missing_lesson_plan_fails(self):
        """Missing lesson_plan should fail."""
        data = copy.deepcopy(VALID_LESSON_PLAN)
        del data["lesson_plan"]
        errors = validate_json(data)
        assert len(errors) > 0

    def test_missing_stages_fails(self):
        """Missing stages should fail."""
        data = copy.deepcopy(VALID_LESSON_PLAN)
        del data["lesson_plan"]["stages"]
        errors = validate_json(data)
        assert len(errors) > 0

    def test_empty_stages_fails(self):
        """Empty stages array should fail."""
        data = copy.deepcopy(VALID_LESSON_PLAN)
        data["lesson_plan"]["stages"] = []
        errors = validate_json(data)
        assert len(errors) > 0

    def test_missing_stage_field_fails(self):
        """Missing stage field should fail."""
        data = copy.deepcopy(VALID_LESSON_PLAN)
        del data["lesson_plan"]["stages"][0]["stage"]
        errors = validate_json(data)
        assert len(errors) > 0


class TestNormalizeTopic:
    """Tests for topic normalization."""

    def test_lowercase(self):
        assert normalize_topic("Test Topic") == "test-topic"

    def test_spaces_to_hyphens(self):
        assert normalize_topic("What Connects Us") == "what-connects-us"

    def test_slashes_to_hyphens(self):
        assert normalize_topic("Test/Topic") == "test-topic"


class TestRenderTemplate:
    """Tests for template rendering."""

    def test_template_renders_with_valid_data(self):
        """Template should render without errors with valid data."""
        result = render_template(VALID_LESSON_PLAN)
        assert "Test Teacher" in result
        assert "Test Topic" in result
        assert "LEAD-IN" in result

    def test_template_handles_missing_optional_fields(self):
        """TC-02 style: Template should handle missing optional fields."""
        data = copy.deepcopy(VALID_LESSON_PLAN)
        del data["transcript"]
        del data["answer-key"]
        result = render_template(data)
        # When transcript/answer-key are "none", sections are hidden
        assert "## Transcript" not in result
        assert "## Answer Key" not in result


class TestConvertJsonToPdf:
    """Tests for the main conversion function."""

    @patch("json_to_pdf.render_typst")
    def test_valid_json_creates_pdf(self, mock_render_typst, tmp_path):
        """TC-01 style: Valid JSON should create PDF."""
        mock_render_typst.return_value = True

        json_file = tmp_path / "test-lesson.json"
        json_file.write_text(json.dumps(copy.deepcopy(VALID_LESSON_PLAN)))

        success = convert_json_to_pdf(str(json_file), str(tmp_path))
        assert success is True
        mock_render_typst.assert_called_once()

    @patch("json_to_pdf.render_typst")
    def test_missing_optional_fields_creates_pdf(self, mock_render_typst, tmp_path):
        """TC-02 style: Missing optional fields should still create PDF."""
        mock_render_typst.return_value = True

        data = copy.deepcopy(VALID_LESSON_PLAN)
        del data["transcript"]
        del data["answer-key"]

        json_file = tmp_path / "test-lesson.json"
        json_file.write_text(json.dumps(data))

        success = convert_json_to_pdf(str(json_file), str(tmp_path))
        assert success is True

    def test_missing_required_field_fails(self, tmp_path):
        """TC-03 style: Missing required field should fail."""
        data = copy.deepcopy(VALID_LESSON_PLAN)
        del data["teacher"]

        json_file = tmp_path / "test-lesson.json"
        json_file.write_text(json.dumps(data))

        success = convert_json_to_pdf(str(json_file), str(tmp_path))
        assert success is False

    def test_invalid_json_fails(self, tmp_path):
        """Invalid JSON should fail."""
        json_file = tmp_path / "test-lesson.json"
        json_file.write_text("not valid json")

        success = convert_json_to_pdf(str(json_file), str(tmp_path))
        assert success is False

    @patch("json_to_pdf.subprocess.run")
    def test_quarto_not_installed_fails(self, mock_run, tmp_path):
        """TC-05 style: Missing Quarto should fail."""
        mock_run.side_effect = FileNotFoundError()

        json_file = tmp_path / "test-lesson.json"
        json_file.write_text(json.dumps(copy.deepcopy(VALID_LESSON_PLAN)))

        success = convert_json_to_pdf(str(json_file), str(tmp_path))
        assert success is False

    @patch("json_to_pdf.subprocess.run")
    def test_quarto_render_failure_fails(self, mock_run, tmp_path):
        """TC-08 style: Quarto render failure should fail."""
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stderr = "Render error"
        mock_run.return_value = mock_result

        json_file = tmp_path / "test-lesson.json"
        json_file.write_text(json.dumps(copy.deepcopy(VALID_LESSON_PLAN)))

        success = convert_json_to_pdf(str(json_file), str(tmp_path))
        assert success is False

    def test_file_not_found_fails(self):
        """TC-04 style: Non-existent file should fail."""
        success = convert_json_to_pdf("/nonexistent/path/file.json")
        assert success is False

    def test_invalid_json_fails(self, tmp_path):
        """Invalid JSON should fail."""
        json_file = tmp_path / "test-lesson.json"
        json_file.write_text("not valid json")

        success = convert_json_to_pdf(str(json_file), str(tmp_path))
        assert success is False

    @patch("json_to_pdf.subprocess.run")
    def test_quarto_not_installed_fails(self, mock_run, tmp_path):
        """TC-05 style: Missing Quarto should fail."""
        mock_run.side_effect = FileNotFoundError()

        json_file = tmp_path / "test-lesson.json"
        json_file.write_text(json.dumps(VALID_LESSON_PLAN))

        success = convert_json_to_pdf(str(json_file), str(tmp_path))
        assert success is False

    @patch("json_to_pdf.subprocess.run")
    def test_quarto_render_failure_fails(self, mock_run, tmp_path):
        """TC-08 style: Quarto render failure should fail."""
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stderr = "Render error"
        mock_run.return_value = mock_result

        json_file = tmp_path / "test-lesson.json"
        json_file.write_text(json.dumps(VALID_LESSON_PLAN))

        success = convert_json_to_pdf(str(json_file), str(tmp_path))
        assert success is False

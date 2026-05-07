"""
test_json_to_markdown.py - Tests for json_to_markdown conversion script
"""

import json
import os
import copy
import pytest
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from json_to_markdown import (
    validate_json,
    humanize_stage_aim,
    format_date,
    generate_title_slide,
    generate_markdown,
    convert_json_to_markdown,
    OUTPUT_DIR,
)

VALID_LESSON_PLAN = {
    "teacher": "Test Teacher",
    "duration": "45 minutes",
    "date": "050726",
    "topic": "Test Topic",
    "objective": "By the end, learners will have practiced reading.",
    "materials": "Student Book, pp 10-12",
    "lesson_plan": {
        "shape": "E",
        "shape_name": "Receptive Skills (Traditional)",
        "cefr_level": "B2",
        "class": "M3",
        "stages": [
            {
                "stage_number": 1,
                "stage": "Lead-in",
                "stage_aim": "To activate interest in the theme",
                "procedure": "- Discuss photos.\n- Share ideas.",
                "time": 5,
                "interaction": "Ss-Ss",
            },
            {
                "stage_number": 2,
                "stage": "Reading for gist",
                "stage_aim": "To get the general idea of the article",
                "procedure": "- Read quickly.\n- Discuss main idea.",
                "time": 5,
                "interaction": "Ss-Ss",
            },
        ],
    },
    "transcript": "none",
    "answer_key": "none",
}


class TestValidateJson:
    def test_valid_json_passes(self):
        errors = validate_json(VALID_LESSON_PLAN)
        assert len(errors) == 0

    def test_missing_teacher_fails(self):
        data = copy.deepcopy(VALID_LESSON_PLAN)
        del data["teacher"]
        errors = validate_json(data)
        assert len(errors) > 0
        assert any("teacher" in e for e in errors)

    def test_missing_lesson_plan_fails(self):
        data = copy.deepcopy(VALID_LESSON_PLAN)
        del data["lesson_plan"]
        errors = validate_json(data)
        assert len(errors) > 0

    def test_missing_stages_fails(self):
        data = copy.deepcopy(VALID_LESSON_PLAN)
        del data["lesson_plan"]["stages"]
        errors = validate_json(data)
        assert len(errors) > 0

    def test_empty_stages_fails(self):
        data = copy.deepcopy(VALID_LESSON_PLAN)
        data["lesson_plan"]["stages"] = []
        errors = validate_json(data)
        assert len(errors) > 0


class TestHumanizeStageAim:
    def test_lead_in_humanized(self):
        result = humanize_stage_aim("To lead-in to the topic of food")
        assert "activate interest" in result.lower()

    def test_reading_for_gist_humanized(self):
        result = humanize_stage_aim("To reading for gist")
        assert "general idea" in result.lower()

    def test_preserves_good_aim(self):
        result = humanize_stage_aim("To activate interest in the theme of travel")
        assert result == "To activate interest in the theme of travel"


class TestFormatDate:
    def test_ddmmyy_to_long(self):
        result = format_date("050726")
        assert result == "5 July, 2026"

    def test_non_numeric_passthrough(self):
        result = format_date("unknown")
        assert result == "unknown"


class TestGenerateTitleSlide:
    def test_contains_cefr_badge(self):
        slide = generate_title_slide(VALID_LESSON_PLAN)
        assert '<span class="cefr-badge B2">B2</span>' in slide

    def test_contains_topic(self):
        slide = generate_title_slide(VALID_LESSON_PLAN)
        assert "# Test Topic" in slide

    def test_contains_teacher(self):
        slide = generate_title_slide(VALID_LESSON_PLAN)
        assert "Test Teacher" in slide

    def test_contains_materials(self):
        slide = generate_title_slide(VALID_LESSON_PLAN)
        assert "Student Book" in slide


class TestGenerateMarkdown:
    def test_separators_used(self):
        md = generate_markdown(VALID_LESSON_PLAN)
        assert "---" in md

    def test_fragments_only_on_answer_slides(self):
        """Fragments should only appear on answer slides, not on expository content."""
        # Valid plan has no answer_key, so markdown should NOT contain fragments
        md = generate_markdown(VALID_LESSON_PLAN)
        assert 'class="fragment"' not in md

    def test_fragments_appear_with_answer_key(self):
        """Fragments should appear when answer_key content is provided."""
        data = copy.deepcopy(VALID_LESSON_PLAN)
        data["answer_key"] = "none"
        md = generate_markdown(data)
        assert 'class="fragment"' not in md

    def test_notes_included(self):
        md = generate_markdown(VALID_LESSON_PLAN)
        assert "Notes:" in md

    def test_stage_aims_included(self):
        md = generate_markdown(VALID_LESSON_PLAN)
        assert "Lead-in" in md
        assert "Reading for gist" in md

    def test_no_banned_patterns(self):
        """Ensure no banned patterns (----, ***, ___) are used as separators."""
        md = generate_markdown(VALID_LESSON_PLAN)
        lines = md.split("\n")
        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped in ("----", "***", "___"):
                pytest.fail(f"Banned separator '{stripped}' found at line {i+1}")


class TestConvertJsonToMarkdown:
    def test_valid_json_creates_markdown(self, tmp_path):
        json_path = tmp_path / "050726-test-lesson-plan.json"
        with open(json_path, "w") as f:
            json.dump(VALID_LESSON_PLAN, f)

        import scripts.json_to_markdown as j2m
        original_output_dir = j2m.OUTPUT_DIR
        j2m.OUTPUT_DIR = tmp_path / "output"
        try:
            result = convert_json_to_markdown(json_path)
            assert result is not None
            assert result.exists()
            content = result.read_text(encoding="utf-8")
            assert "# Test Topic" in content
            assert "---" in content
        finally:
            j2m.OUTPUT_DIR = original_output_dir

    def test_missing_file_returns_none(self):
        result = convert_json_to_markdown("nonexistent_file.json")
        assert result is None

    def test_invalid_json_returns_none(self, tmp_path):
        bad_json = tmp_path / "bad.json"
        bad_json.write_text("not json", encoding="utf-8")
        result = convert_json_to_markdown(bad_json)
        assert result is None
"""
test_build_lesson_pdf.py — Red-green tests for the Markdown → Pandoc → Typst → PDF pipeline.

Catches regressions in validation, path derivation, and end-to-end compilation.
Uses the same pytest conventions as the existing 56-test suite.
"""

import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from build_lesson_pdf import (
    get_output_pdf_path,
    lint_markdown,
    parse_frontmatter,
    validate_metadata,
)

# ── Helper: minimal valid lesson.md ──


def _make_md(content, topic="Test Topic"):
    """Write a .md temp file and return its Path."""
    header = f"""---
topic: "{topic}"
teacher: "Ed Rush"
formatted_date: "15 June, 2026"
duration: "46 minutes"
cefr_level: "B2"
class: "M3"
shape: "G"
shape_name: "Task-Based Learning"
materials:
  - "Textbook"
---
"""
    combined = header + content
    tf = tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False, encoding="utf-8")
    tf.write(combined)
    tf.close()
    return Path(tf.name)


MINIMAL_STAGES = """
## Stage 1: Lead-in

**Time:** 5 min  |  **Interaction:** T-Ss

**Aim:** To activate interest

- Discussion question
- Pair share

## Stage 2: Practice

**Time:** 41 min  |  **Interaction:** Ss-Ss

**Aim:** To apply the skill

- Complete exercise
- Peer feedback
"""


# ══════════════════════════════════════════════════════════════════════════
# UNIT TESTS — validation logic (no Pandoc/Typst needed)
# ══════════════════════════════════════════════════════════════════════════


class TestParseFrontmatter:
    """YAML frontmatter parsing."""

    def test_valid_frontmatter_returns_meta_and_body(self):
        path = _make_md(MINIMAL_STAGES)
        try:
            meta, body = parse_frontmatter(path)
            assert meta["topic"] == "Test Topic"
            assert "## Stage 1: Lead-in" in body
        finally:
            path.unlink()

    def test_missing_frontmatter_exits(self):
        import pytest

        path = _make_md("Just text, no --- markers\n", topic="")
        path.write_text("Just text, no YAML frontmatter\n", encoding="utf-8")
        try:
            with pytest.raises(SystemExit):
                parse_frontmatter(path)
        finally:
            path.unlink()


class TestValidateMetadata:
    """Required YAML field checks."""

    def test_all_fields_present_no_warnings(self):
        meta = {
            "topic": "T",
            "teacher": "T",
            "formatted_date": "D",
            "duration": "46",
            "cefr_level": "B2",
            "class": "M3",
            "shape": "G",
            "shape_name": "TBL",
        }
        warnings = validate_metadata(meta)
        assert len(warnings) == 0

    def test_missing_topic_produces_warning(self):
        meta = {
            "teacher": "T",
            "formatted_date": "D",
            "duration": "46",
            "cefr_level": "B2",
            "class": "M3",
            "shape": "G",
            "shape_name": "TBL",
        }
        warnings = validate_metadata(meta)
        assert any("topic" in w for w in warnings)


class TestLintMarkdown:
    """Body-stage validation."""

    def test_valid_body_passes(self):
        path = _make_md(MINIMAL_STAGES)
        try:
            assert lint_markdown(path) is True
        finally:
            path.unlink()

    def test_missing_stage_headings_fails(self):
        path = _make_md("## Materials\n\n- Textbook\n", topic="No Stages")
        try:
            assert lint_markdown(path) is False
        finally:
            path.unlink()

    def test_mismatched_time_warns_but_passes(self):
        body = """
## Stage 1: Intro

**Time:** 5 min  |  **Interaction:** T-Ss

**Aim:** To activate

- Item
"""
        path = _make_md(body, topic="Time Mismatch")
        try:
            assert lint_markdown(path) is True  # WARNING, not FATAL
        finally:
            path.unlink()


class TestOutputPath:
    """PDF output path derivation."""

    def test_output_in_subfolder_matches_convention(self):
        md = Path("output/M3-SPEAKING-TBL/150626-gender-lesson-plan.md")
        pdf = get_output_pdf_path(md, {"topic": "Gender Stereotypes and Gen Z"})
        assert "PDF" in str(pdf)
        assert str(pdf).endswith(".pdf")
        assert "M3-SPEAKING-TBL" in str(pdf)


# ══════════════════════════════════════════════════════════════════════════
# INTEGRATION TESTS — requires Pandoc + Typst on PATH
# ══════════════════════════════════════════════════════════════════════════


def _has_pandoc():
    return subprocess.run(["pandoc", "--version"], capture_output=True).returncode == 0


def _has_typst():
    return subprocess.run(["typst", "--version"], capture_output=True).returncode == 0


class TestPandocTypstIntegration:
    """End-to-end: Markdown → Pandoc → Typst → PDF."""

    def test_pandoc_to_typst_succeeds(self):
        if not _has_pandoc():
            pytest.skip("Pandoc not installed")
        from build_lesson_pdf import pandoc_to_typst

        path = _make_md(MINIMAL_STAGES)
        try:
            typst_source = pandoc_to_typst(path)
            assert "Lesson Information" in typst_source
            assert "STAGE 1" in typst_source
            assert "STAGE 2" in typst_source
        finally:
            path.unlink()

    def test_full_pipeline_produces_pdf(self):
        if not _has_pandoc() or not _has_typst():
            pytest.skip("Pandoc or Typst not installed")
        from build_lesson_pdf import compile_typst, pandoc_to_typst

        path = _make_md(MINIMAL_STAGES)
        pdf_path = path.parent / "test_output.pdf"
        try:
            typst_source = pandoc_to_typst(path)
            assert compile_typst(typst_source, pdf_path) is True
            assert pdf_path.exists()
            assert pdf_path.stat().st_size > 1000  # non-empty PDF
        finally:
            path.unlink()
            if pdf_path.exists():
                pdf_path.unlink()

    def test_invalid_md_is_rejected_before_typst(self):
        """Red: a .md with no stages should fail validation, not reach Typst."""
        if not _has_pandoc():
            pytest.skip("Pandoc not installed")
        path = _make_md("No stage headings here\n", topic="Empty")
        try:
            assert lint_markdown(path) is False
        finally:
            path.unlink()

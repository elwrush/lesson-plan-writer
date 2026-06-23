"""
test_validate_slides.py — Red-green tests for the pre-build validation script.

Tests:
  - Known-good slides.md passes validation
  - Known-bad patterns are flagged
  - Edge cases (empty slides, unbalanced divs, missing files, raw HTML)
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from scripts.validate_slides import (
    check_fenced_div_balance,
    check_horizontal_rules,
    check_inline_css,
    check_missing_files,
    check_raw_html,
    check_speaker_notes,
    check_unauthorized_assets,
    check_youtube_ids,
    parse_slides,
)

# ── Fixtures ─────────────────────────────────────────────────────────────


@pytest.fixture
def good_slides_md():
    return """\
#  {data-background-image="assets/bg.jpg" data-background-size="cover"}

#  {data-background-image="assets/bg.jpg" data-background-size="cover"}

![](assets/logo.png){.title-logo}

::: {.title-row}
[**Test Title**]{.slide-title}
:::

::: {.shield}
Subtitle
:::

::: notes
Welcome. Time: 1 min. T-Ss.
:::

# Objectives

I can do this.

I can do that.

::: notes
Read through. Time: 1 min.
:::

# Content Slide

Some body content here.

- Item 1
- Item 2

::: {.fragment .answer-reveal}
Hidden answer.
:::

::: notes
Discuss. Time: 2 min. T-Ss.
:::

#  {data-background-color="#2c3e50"}

**Topic** **B2**

::: notes
Thank students. Time: 1 min.
:::"""


@pytest.fixture
def good_md_parsed(good_slides_md):
    return parse_slides(good_slides_md)


# ── parse_slides ─────────────────────────────────────────────────────────


class TestParseSlides:
    def test_parses_correct_number_of_slides(self, good_md_parsed):
        # Splash(empty) + Title(empty) + Objectives + Content Slide + End(empty) = 5
        assert len(good_md_parsed) == 5

    def test_splash_heading_detected_empty(self, good_md_parsed):
        splash = good_md_parsed[0]
        assert splash["heading_text"] == "", (
            f"Expected empty heading text, got '{splash['heading_text']}'"
        )
        assert "data-background-image" in splash["heading_attrs"]

    def test_title_heading_empty_with_attrs(self, good_md_parsed):
        # Title slide heading is empty (text is in .title-row), only has attributes
        title = good_md_parsed[1]
        assert title["heading_text"] == "", (
            f"Title heading should be empty, got '{title['heading_text']}'"
        )
        assert "data-background-image" in title["heading_attrs"]

    def test_speaker_notes_detected(self, good_md_parsed):
        for slide in good_md_parsed:
            if slide["heading_text"] == "Objectives":
                assert slide["has_speaker_notes"] is True
                break
        else:
            pytest.fail("Objectives slide not found")

    def test_fenced_divs_balanced(self, good_md_parsed):
        for slide in good_md_parsed:
            assert slide["fenced_divs"] == 0, (
                f"Slide '{slide['heading_text']}' has "
                f"unbalanced fenced divs ({slide['fenced_divs']})"
            )


# ── check_speaker_notes ──────────────────────────────────────────────────


class TestCheckSpeakerNotes:
    def test_good_slides_pass(self, good_md_parsed):
        errors = check_speaker_notes(good_md_parsed)
        assert len(errors) == 0

    def test_missing_notes_reported(self, good_md_parsed):
        # Remove notes from one slide
        good_md_parsed[2]["has_speaker_notes"] = False
        errors = check_speaker_notes(good_md_parsed)
        assert len(errors) >= 1
        assert "missing speaker notes" in errors[0]

    def test_empty_heading_skipped(self, good_md_parsed):
        # Splash (slide 0) has empty heading — should be skipped even without notes
        splash = good_md_parsed[0]
        assert splash["heading_text"] == ""
        splash["has_speaker_notes"] = False
        errors = check_speaker_notes(good_md_parsed)
        splash_errors = [e for e in errors if "slide 1" in e.lower()]
        assert len(splash_errors) == 0, f"Splash slide should skip notes check: {splash_errors}"


# ── check_raw_html ───────────────────────────────────────────────────────


class TestCheckRawHtml:
    def test_pure_markdown_passes(self, good_md_parsed):
        errors = check_raw_html(good_md_parsed)
        assert len(errors) == 0

    def test_raw_html_tag_reported(self, good_md_parsed):
        good_md_parsed[2]["body_lines"].append("<div>raw html</div>")
        errors = check_raw_html(good_md_parsed)
        assert len(errors) >= 1

    def test_bracketed_span_not_reported(self, good_md_parsed):
        good_md_parsed[2]["body_lines"].append("[text]{.class}")
        errors = check_raw_html(good_md_parsed)
        html_errors = [e for e in errors if "raw HTML" in e]
        assert len(html_errors) == 0


# ── check_fenced_div_balance ─────────────────────────────────────────────


class TestCheckFencedDivBalance:
    def test_balanced_passes(self, good_md_parsed):
        errors = check_fenced_div_balance(good_md_parsed)
        assert len(errors) == 0

    def test_unbalanced_reported(self, good_md_parsed):
        good_md_parsed[1]["fenced_divs"] = 2
        errors = check_fenced_div_balance(good_md_parsed)
        assert len(errors) >= 1
        assert "unbalanced" in errors[0]


# ── check_missing_files ──────────────────────────────────────────────────


class TestCheckMissingFiles:
    def test_nonexistent_file_reported(self, tmp_path, good_md_parsed):
        md_path = tmp_path / "slides.md"
        md_path.touch()
        # Add reference to non-existent file
        good_md_parsed[0]["heading_attrs"] = 'data-background-image="assets/missing.jpg"'
        errors = check_missing_files(md_path, good_md_parsed)
        assert len(errors) >= 1
        assert "missing.jpg" in errors[0]

    def test_existing_file_passes(self, tmp_path, good_md_parsed):
        md_path = tmp_path / "slides.md"
        md_path.touch()
        # Create the referenced file
        assets_dir = tmp_path / "assets"
        assets_dir.mkdir()
        (assets_dir / "bg.jpg").touch()
        good_md_parsed[0]["heading_attrs"] = 'data-background-image="assets/bg.jpg"'
        errors = check_missing_files(md_path, good_md_parsed)
        file_errors = [e for e in errors if "assets/bg.jpg" in e]
        assert len(file_errors) == 0


# ── check_horizontal_rules ───────────────────────────────────────────────


class TestCheckHorizontalRules:
    def test_no_rules_passes(self):
        md = "# Slide 1\n\nContent\n\n# Slide 2\n\nContent\n"
        warnings = check_horizontal_rules(md)
        assert len(warnings) == 0

    def test_separator_warns(self):
        md = "# Slide 1\n\nContent\n\n---\n\n# Slide 2\n\nContent\n"
        warnings = check_horizontal_rules(md)
        assert len(warnings) >= 1
        assert "---" in warnings[0]

    def test_yaml_frontmatter_not_flagged(self):
        md = "---\ntitle: Test\n---\n\n# Slide 1\n\nContent\n"
        warnings = check_horizontal_rules(md)
        # The YAML frontmatter has --- at lines 1 and 3, should not be flagged
        [w for w in warnings if "frontmatter" not in w.lower()]
        # Check that we're not flagging YAML delimiters as slide breaks
        assert len(warnings) == 0


# ── check_youtube_ids ────────────────────────────────────────────────────


class TestCheckYoutubeIds:
    def test_valid_youtube_id_passes(self):
        slides = [
            {
                "line_start": 5,
                "body_lines": [
                    "::: {.youtube}",
                    "dQw4w9WgXcQ",
                    ":::",
                ],
            }
        ]
        errors = check_youtube_ids(slides)
        assert len(errors) == 0

    def test_invalid_youtube_id_reported(self):
        slides = [
            {
                "line_start": 10,
                "body_lines": [
                    "::: {.youtube}",
                    "not-a-real-id-thats-way-too-long-123456789",
                    ":::",
                ],
            }
        ]
        errors = check_youtube_ids(slides)
        assert len(errors) >= 1
        assert "suspicious" in errors[0].lower()

    def test_no_youtube_no_error(self):
        slides = [{"line_start": 1, "body_lines": ["Just text."]}]
        errors = check_youtube_ids(slides)
        assert len(errors) == 0


# ── Edge cases ────────────────────────────────────────────────────────────


class TestEdgeCases:
    def test_empty_file(self):
        slides = parse_slides("")
        assert len(slides) == 0

    def test_no_headings(self):
        slides = parse_slides("Just some text\n\nMore text\n")
        assert len(slides) == 0

    def test_headings_without_body(self):
        md = "# Slide 1\n\n# Slide 2\n\n# Slide 3\n"
        slides = parse_slides(md)
        assert len(slides) == 3
        for slide in slides:
            assert slide["heading_text"] in ("Slide 1", "Slide 2", "Slide 3")

    def test_notes_syntax_variants(self):
        md = """\
# Slide 1

::: notes
Note content
:::

# Slide 2

::: notes
Another note
:::
"""
        slides = parse_slides(md)
        assert slides[0]["has_speaker_notes"] is True
        assert slides[1]["has_speaker_notes"] is True


# ── Inline CSS guard (red-green for agent's own writing) ──────────────────


class TestCheckInlineCss:
    """The agent writes pure Pandoc Markdown — no inline CSS.

    If the agent writes `style=` in slides.md, the build must fail.
    All styling must go through Lua filters or the shared CSS file.
    """

    def test_clean_md_passes(self):
        """Pure Pandoc Markdown with no style attributes passes."""
        md = """\
#  {#splash data-background-image="assets/bg.jpg"}

# Title

::: {.shield}
Subtitle
:::

::: notes
Test.
:::
"""
        errors = check_inline_css(md)
        assert len(errors) == 0

    def test_inline_css_is_detected(self):
        """Any `style=` in Markdown body is flagged."""
        md = """\
# Slide
<div style="color: red;">
Bad
</div>
"""
        errors = check_inline_css(md)
        assert len(errors) >= 1
        assert "style=" in errors[0]

    def test_style_in_fenced_div_attrs_is_detected(self):
        """Even style in fenced div attributes is forbidden — use Lua filter."""
        md = """\
# Slide

::: {.shield style="padding: 0;"}
Text
:::
"""
        errors = check_inline_css(md)
        assert len(errors) >= 1

    def test_style_in_bracketed_span_is_detected(self):
        """Even style in bracketed spans is forbidden — use Lua filter."""
        md = """\
# Slide

[text]{style="color: red;"}
"""
        errors = check_inline_css(md)
        assert len(errors) >= 1

    def test_data_attributes_not_flagged(self):
        """data-background-image and similar are NOT style attributes."""
        md = """\
#  {#splash data-background-image="assets/bg.jpg" data-background-size="cover"}
"""
        errors = check_inline_css(md)
        assert len(errors) == 0

    def test_heading_attrs_no_style_not_flagged(self):
        """Heading attributes without style= pass."""
        md = """\
# Slide {#my-id .custom-class}
"""
        errors = check_inline_css(md)
        assert len(errors) == 0

    def test_unauthorized_css_reported(self, tmp_path):
        """Unauthorized .css file in slides directory is flagged."""
        md = tmp_path / "slides.md"
        md.write_text("# Slide\ncontent\n")
        css = tmp_path / "custom.css"
        css.write_text("body { color: red; }")
        errors = check_unauthorized_assets(md)
        assert len(errors) == 1
        assert "Unauthorized" in errors[0]

    def test_unauthorized_html_reported(self, tmp_path):
        """Unauthorized .html file in slides directory is flagged."""
        md = tmp_path / "slides.md"
        md.write_text("# Slide\ncontent\n")
        html = tmp_path / "custom.html"
        html.write_text("<div></div>")
        errors = check_unauthorized_assets(md)
        assert len(errors) == 1
        assert "Unauthorized" in errors[0]

    def test_allowed_assets_pass(self, tmp_path):
        """slides-pandoc.css and slides-header.html are allowed."""
        md = tmp_path / "slides.md"
        md.write_text("# Slide\ncontent\n")
        css = tmp_path / "slides-pandoc.css"
        css.write_text("/* hash-locked */")
        html = tmp_path / "slides-header.html"
        html.write_text("<!-- header -->")
        errors = check_unauthorized_assets(md)
        assert len(errors) == 0

    def test_no_assets_no_errors(self, tmp_path):
        """No CSS/HTML files at all means no errors."""
        md = tmp_path / "slides.md"
        md.write_text("# Slide\ncontent\n")
        errors = check_unauthorized_assets(md)
        assert len(errors) == 0

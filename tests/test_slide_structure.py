"""
test_slide_structure.py — Red-green test suite for slide HTML structural invariants.

Tests run against ALL output/*/slides/index.html files by default, ensuring
no slideshow is left with broken HTML structure after agent manipulation.

Usage:
    python -m pytest tests/test_slide_structure.py -v --tb=short
    python -m pytest tests/test_slide_structure.py --slideshow-html "path/to/index.html" -v
    python -m pytest tests/test_slide_structure.py::TestSlideCount -v
"""

import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

# Override set by conftest.py when --slideshow-html CLI argument is provided
_CLI_HTML_OVERRIDE = None


def _resolve_slideshow_paths():
    """Return list of (subfolder_name, Path) for every slideshow to test.

    Respects _CLI_HTML_OVERRIDE set by the --slideshow-html CLI argument.
    Otherwise returns all output/*/slides/index.html sorted by mtime (newest first).
    """
    if _CLI_HTML_OVERRIDE:
        p = Path(_CLI_HTML_OVERRIDE)
        if not p.exists():
            raise FileNotFoundError(
                f"Specified --slideshow-html path does not exist: {_CLI_HTML_OVERRIDE}"
            )
        return [(_CLI_HTML_OVERRIDE, p)]

    matches = sorted(
        Path("output").rglob("slides/index.html"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    if not matches:
        pytest.exit("No output/*/slides/index.html files found", returncode=1)
    return [(str(p), p) for p in matches]


# Resolve paths once at module load time
SLIDESHOW_PATHS = _resolve_slideshow_paths()


@pytest.fixture(params=SLIDESHOW_PATHS, ids=[name for name, _ in SLIDESHOW_PATHS])
def slideshow(request):
    """Fixture yielding (content, path) for each slideshow to test."""
    _name, path = request.param
    if not path.exists():
        pytest.fail(f"Slideshow file not found: {path}")
    content = path.read_text(encoding="utf-8")
    return content, path


class TestSlideCount:
    """At least one <section> must exist, and every section must have a stable id."""

    def test_sections_exist(self, slideshow):
        content, path = slideshow
        opens = len(re.findall(r"<section[\s>]", content))
        assert opens > 0, (
            f"No <section> elements found in {path.name} "
            f"(subfolder: {path.parent.parent.name}). "
            "The slide splice may have produced an empty output."
        )

    def test_all_sections_have_ids(self, slideshow):
        content, path = slideshow
        sections = re.findall(r"<section[\s>]", content)
        ids = re.findall(r"<section[^>]*\sid=\"([^\"]+)\"", content)

        # Pre-convention slideshows (no IDs at all) are accepted without change
        if len(ids) == 0:
            return

        # Once IDs are in use, every section must have one
        missing = len(sections) - len(ids)
        assert missing == 0, (
            f"{missing} <section> element(s) in {path.parent.parent.name}/ "
            f"are missing an id attribute. {len(sections)} sections total, "
            f"but only {len(ids)} have one."
        )
        duplicates = {i for i in ids if ids.count(i) > 1}
        assert not duplicates, (
            f"Duplicate section id(s) in {path.parent.parent.name}/: {sorted(duplicates)}"
        )


class TestHtmlWellFormed:
    """Basic HTML tag matching within the slides container."""

    def test_section_tags_balanced(self, slideshow):
        content, path = slideshow
        opens = len(re.findall(r"<section[\s>]", content))
        closes = content.count("</section>")
        assert opens == closes, (
            f"Mismatched <section> tags in {path.parent.parent.name}/: "
            f"{opens} opens, {closes} closes"
        )

    def test_span_tags_balanced(self, slideshow):
        content, path = slideshow
        opens = len(re.findall(r"<span[\s>]", content))
        closes = content.count("</span>")
        assert opens == closes, (
            f"Mismatched <span> tags in {path.parent.parent.name}/: {opens} opens, {closes} closes"
        )


class TestBareCommentClosers:
    """No bare '-->' text nodes — orphaned comment closers render as visible text."""

    def test_html_comment_balance(self, slideshow):
        content, path = slideshow
        opens = content.count("<!--")
        closes = content.count("-->")
        assert opens == closes, (
            f"Unbalanced HTML comments in {path.parent.parent.name}/: "
            f"{opens} opens, {closes} closes. "
            "A bare '-->' may be rendering as visible text on every slide."
        )

    def test_no_bare_dash_dash_gt_outside_comments(self, slideshow):
        content, path = slideshow
        stripped = re.sub(r"<!--.*?-->", "", content, flags=re.DOTALL)
        remaining = stripped.count("-->")
        assert remaining == 0, (
            f"{remaining} orphaned '-->' found outside HTML comments in "
            f"{path.parent.parent.name}/. "
            "These render as visible text on slides."
        )
        remaining_opens = stripped.count("<!--")
        assert remaining_opens == 0, (
            f"{remaining_opens} orphaned '<!--' found outside HTML comments in "
            f"{path.parent.parent.name}/."
        )


class TestAutoAnimatePairs:
    """Every data-auto-animate-id value must appear exactly twice (entry + reveal)."""

    def test_auto_animate_ids_are_paired(self, slideshow):
        content, path = slideshow
        ids = re.findall(r'data-auto-animate-id="([^"]+)"', content)
        counts = {}
        for aid in ids:
            counts[aid] = counts.get(aid, 0) + 1
        unpaired = {aid: c for aid, c in counts.items() if c < 2}
        assert not unpaired, (
            f"Unpaired auto-animate IDs in {path.parent.parent.name}/: "
            + ", ".join(f"'{k}' appears {v} times" for k, v in sorted(unpaired.items()))
        )


class TestFragmentClasses:
    """Fragment classes should not conflict with reveal.js built-in highlight classes.

    The highlight-* classes set opacity:1 and visibility:inherit at all times,
    making them unusable for hide/reveal fragment patterns.
    """

    CONFLICTING_CLASSES = {
        "highlight-green",
        "highlight-red",
        "highlight-blue",
    }

    def test_no_highlight_fragments(self, slideshow):
        content, path = slideshow
        for cls in self.CONFLICTING_CLASSES:
            pattern = rf'class="[^"]*\bfragment\b[^"]*\b{cls}\b'
            matches = re.findall(pattern, content)
            pattern2 = rf'class="[^"]*\b{cls}\b[^"]*\bfragment\b[^"]*'
            matches += re.findall(pattern2, content)
            assert not matches, (
                f"Found {len(matches)} element(s) combining 'fragment' and '{cls}' "
                f"in {path.parent.parent.name}/. "
                f"reveal.js keeps '{cls}' at opacity:1 — fragments never hide."
            )

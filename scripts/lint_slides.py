"""
lint_slides.py — Design rule checker for reveal.js slide HTML.

Run BEFORE revealjs-validator to catch color, layout, and content
violations that the validator doesn't check.

Usage:
    python scripts/lint_slides.py --project output/<subfolder>/slides/

Exit codes:
    0 — all checks pass
    1 — warnings only
    2 — errors found
"""

import argparse
import re
import sys
from pathlib import Path

# Known good values
PEDAGOGICAL_BG = "#1a237e"
ANSWER_BG = "#052e0d"
TRANSITION_BG = "#c0392b"
DARK_BG = "#1a1a2e"
END_BG = "#2c3e50"
YELLOW = "#ffdd00"
WHITE = "#fff"

# Colors that should NEVER appear in slide HTML (except CEFR badge CSS)
BANNED_COLORS = [
    ("#0d4a3d", "old pedagogical teal"),
    ("#0d5e1a", "old answer green"),
    ("#4fc3f7", "blue accent"),
    ("#ff8a65", "orange accent"),
    ("#4caf50", "green (except CEFR badge A1 CSS)"),
    ("#ff5252", "red accent"),
]

# CEFR badge CSS lines that are exempt from banned-color checks
CEFR_EXEMPT_LINES = [
    "cefr-badge.A1 { background: #4caf50",
    "cefr-badge.A2 { background: #8bc34a",
    "cefr-badge.A2 { background: #2196f3",
    "cefr-badge.A1 { background: #8bc34a",
    "cefr-badge.B1 { background: #2196f3",
    "cefr-badge.B2 { background: #2a76dd",
    "cefr-badge.C1 { background: #9c27b0",
    "cefr-badge.C2 { background: #f44336",
]


def check_banned_colors(content, filepath):
    """Check for colors that violate the design rules."""
    errors = []
    lines = content.split("\n")
    for i, line in enumerate(lines, 1):
        for color, desc in BANNED_COLORS:
            if color in line:
                # Skip CEFR badge CSS
                is_cefr = any(ex in line for ex in CEFR_EXEMPT_LINES)
                if is_cefr:
                    continue
                errors.append(f"  Line {i}: Found {desc} ({color})")
    return errors


def check_rgba_text_color(content, filepath):
    """Check for rgba(255,255,255,X) with X < 1 used as text color."""
    warnings = []
    lines = content.split("\n")
    for i, line in enumerate(lines, 1):
        # Match color: rgba(255,255,255,0.X) patterns
        matches = re.findall(r"color:\s*rgba\(255,\s*255,\s*255,\s*0\.\d+\)", line, re.IGNORECASE)
        for m in matches:
            warnings.append(f"  Line {i}: rgba text color with alpha < 1: {m}")
    return warnings


def check_text_shadow(content, filepath):
    """Check for text-shadow CSS declarations."""
    warnings = []
    lines = content.split("\n")
    for i, line in enumerate(lines, 1):
        if "text-shadow" in line and "text-shadow: none" not in line:
            warnings.append(f"  Line {i}: text-shadow declaration found")
    return warnings


def check_box_shadow(content, filepath):
    """Check for box-shadow (banned on all slides except title)."""
    warnings = []
    lines = content.split("\n")
    for i, line in enumerate(lines, 1):
        if "box-shadow" in line.lower():
            # Allow in timer-plugin.css (not index.html)
            warnings.append(f"  Line {i}: box-shadow found")
    return warnings


def check_answer_slides(content, filepath):
    """Check answer slides for structural issues."""
    errors = []
    warnings = []

    # Find all answer-slide sections
    pattern = r'<section[^>]*class="[^"]*answer-slide[^"]*"[^>]*>'
    sections = list(re.finditer(pattern, content))

    for match in sections:
        section_start = match.start()
        section_end = content.find("</section>", section_start) + len("</section>")
        section_html = content[section_start:section_end]

        # Count a-rows
        row_count = section_html.count('<div class="a-row')
        if row_count > 1:
            errors.append(f"  {match.group()[:80]}: Found {row_count} a-rows (should be 1)")

        # Check for a-num
        if 'class="a-num"' in section_html:
            warnings.append(f"  {match.group()[:80]}: Contains a-num span (redundant with h2)")

        # Check for original sentence <p> above answer-list
        has_p_before = bool(
            re.search(r"</h2>\n\s*<p[^>]*>.*</p>\n\s*<div class=\"answer-list\">", section_html)
        )
        if not has_p_before:
            # Check if the <p> is missing entirely (not just different spacing)
            section_after_h2 = section_html[section_html.find("</h2>") :]
            if '<div class="answer-list">' in section_after_h2:
                warnings.append(
                    f"  {match.group()[:80]}: May be missing original-sentence <p> above answer-list"
                )

        # Check for fragment on a-row (not per-span)
        if (
            'class="a-row fragment fade-up"' not in section_html
            and 'class="a-row fragment' not in section_html
        ):
            # Check if fragments exist on spans inside
            if "fragment fade-up a-ans" in section_html:
                warnings.append(
                    f"  {match.group()[:80]}: Fragments on individual spans instead of a-row div"
                )

        # Check for background color
        if ANSWER_BG not in section_html:
            errors.append(f"  {match.group()[:80]}: Missing data-background-color={ANSWER_BG}")

    return errors, warnings


def check_cefr_consistency(content, filepath):
    """Check that all CEFR badges use the same level."""
    badges = re.findall(r"cefr-badge\s+([AB]\d)", content)
    if len(badges) >= 2:
        unique = set(badges)
        if len(unique) > 1:
            return [f"  Inconsistent CEFR badges: {badges}"]
    return []


def main():
    parser = argparse.ArgumentParser(description="Lint reveal.js slide HTML for design rules.")
    parser.add_argument("--project", required=True, help="Path to slides directory")
    args = parser.parse_args()

    project_path = Path(args.project)
    html_path = project_path / "index.html"

    if not html_path.exists():
        print(f"ERROR: {html_path} not found")
        sys.exit(2)

    with open(html_path, encoding="utf-8") as f:
        content = f.read()

    all_errors = []
    all_warnings = []

    print(f"Checking: {html_path}")
    print()

    # Run checks
    errors = check_banned_colors(content, html_path)
    all_errors.extend(errors)
    for e in errors:
        print(f"  ERROR: {e}")

    warnings = check_rgba_text_color(content, html_path)
    all_warnings.extend(warnings)
    for w in warnings:
        print(f"  WARN: {w}")

    warnings = check_text_shadow(content, html_path)
    all_warnings.extend(warnings)
    for w in warnings:
        print(f"  WARN: {w}")

    warnings = check_box_shadow(content, html_path)
    all_warnings.extend(warnings)
    for w in warnings:
        print(f"  WARN: {w}")

    ans_errors, ans_warnings = check_answer_slides(content, html_path)
    all_errors.extend(ans_errors)
    all_warnings.extend(ans_warnings)
    for e in ans_errors:
        print(f"  ERROR: {e}")
    for w in ans_warnings:
        print(f"  WARN: {w}")

    cefr_errors = check_cefr_consistency(content, html_path)
    all_errors.extend(cefr_errors)
    for e in cefr_errors:
        print(f"  ERROR: {e}")

    # Authorial voice check
    import importlib.util

    _av_path = str(Path(__file__).parent / "check_authorial_voice.py")
    _av_spec = importlib.util.spec_from_file_location("check_authorial_voice", _av_path)
    _av_mod = importlib.util.module_from_spec(_av_spec)
    _av_spec.loader.exec_module(_av_mod)
    av_exit = _av_mod.check_authorial_voice(html_path)
    if av_exit != 0:
        all_warnings.append(
            "Authorial voice violations found -- run check_authorial_voice.py for details"
        )

    # Structural integrity check
    import re

    sec_opens = content.count("<section")
    sec_closes = content.count("</section>")
    div_opens = content.count("<div")
    div_closes = content.count("</div>")

    print(f"  STRUCTURAL: {sec_opens} <section> opens, {sec_closes} closes")
    print(f"             {div_opens} <div> opens, {div_closes} closes")

    if sec_opens != sec_closes:
        all_errors.append(
            f"STRUCTURAL: {sec_opens} <section> opens but {sec_closes} </section> closes — DOM corruption will cause slides to be cut off"
        )
    if div_opens != div_closes:
        all_errors.append(
            f"STRUCTURAL: {div_opens} <div> opens but {div_closes} </div> closes — DOM corruption will cause content to be cut off or slides to malfunction"
        )

    # Per-section div balance check
    sections = re.findall(r"(<section\b.*?</section>)", content, re.DOTALL)
    bad_slides = 0
    for sec in sections:
        aid = re.search(r'id="([^"]*)"', sec)
        sid = aid.group(1) if aid else "unknown"
        s_div_o = sec.count("<div")
        s_div_c = sec.count("</div>")
        if s_div_o != s_div_c:
            all_errors.append(
                f"STRUCTURAL: Slide '{sid}' has {s_div_o} <div> opens and {s_div_c} </div> closes — will cause slides after it to be cut off"
            )
            bad_slides += 1
    if bad_slides == 0:
        print(f"             {len(sections)} sections, all with balanced divs")

    # Unicode escape check — literal \\u... in HTML breaks rendering
    import re as _re

    unicode_escapes = _re.findall(r"\\u[0-9a-fA-F]{4}", content)
    if unicode_escapes:
        for ue in unicode_escapes[:5]:
            all_errors.append(
                f"UNICODE: Literal '{ue}' found — should be actual Unicode character, not escape sequence"
            )
        if len(unicode_escapes) > 5:
            all_errors.append(f"UNICODE: ... and {len(unicode_escapes) - 5} more literal escapes")

    # Summary
    print()
    if not all_errors and not all_warnings:
        print("All checks passed.")
        sys.exit(0)
    elif all_errors:
        print(f"FAILED: {len(all_errors)} error(s), {len(all_warnings)} warning(s)")
        sys.exit(2)
    else:
        print(f"WARNINGS ONLY: {len(all_warnings)} warning(s)")
        sys.exit(1)


if __name__ == "__main__":
    main()

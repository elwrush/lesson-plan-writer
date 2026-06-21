#!/usr/bin/env python3
"""
validate_slides.py — Pre-build validation for slides.md

Scans a Pandoc Markdown slides file for common errors before building:
  - Speaker notes missing on slides
  - Audio/image files referenced but not found
  - Raw HTML tags (forbidden — use Pandoc Markdown only)
  - Unbalanced fenced divs (:::[space]...[space]:::)
  - `---` separators that may cause spurious slide breaks
  - Slide count statistics

Usage:
    python scripts/validate_slides.py output/{subfolder}/slides/slides.md

Exit codes:
    0 — all checks pass
    1 — warnings only (non-blocking — still OK to build)
    2 — errors found (build should not proceed)
"""

import hashlib
import re
import sys
from pathlib import Path

# ── helpers ──────────────────────────────────────────────────────────────


def warn(msg: str) -> None:
    print(f"  ⚠  WARN: {msg}")


def err(msg: str) -> None:
    print(f"  ✖  ERROR: {msg}")


def ok(msg: str) -> None:
    print(f"  ✔  {msg}")


# ── checks ───────────────────────────────────────────────────────────────


def parse_slides(md: str) -> list[dict]:
    """Split the file into slides by `# ` headings.

    Returns a list of dicts: {heading, lines, speaker_notes, body, line_start, line_end}.
    """
    lines = md.split("\n")
    slides: list[dict] = []
    current_slide: dict | None = None

    for i, line in enumerate(lines, start=1):
        stripped = line.strip()

        # A `# ` heading begins a new slide
        if stripped.startswith("# "):
            if current_slide is not None:
                slides.append(current_slide)
            heading_text = stripped[2:].strip()
            # Remove attributes in braces { ... } — may be attached or spaced
            heading_attrs = ""
            attr_match = re.search(r"\{([^}]*)\}\s*$", heading_text)
            if attr_match:
                heading_text = heading_text[: attr_match.start()].strip()
                heading_attrs = attr_match.group(1)
            current_slide = {
                "heading_text": heading_text,
                "heading_attrs": heading_attrs,
                "has_speaker_notes": False,
                "speaker_notes_lines": [],
                "body_lines": [],
                "line_start": i,
                "line_end": i,
                "fenced_divs": 0,  # nesting count of opened ::: blocks
            }
            continue

        if current_slide is None:
            continue  # content before first heading (metadata etc.)

        current_slide["line_end"] = i

        # Track fenced div nesting
        if stripped.startswith(":::") and not stripped.startswith("::::"):
            remainder = stripped[3:].strip()
            if remainder:
                # Opening: `::: {.class}`, `::: notes`, `::: fragment`, etc.
                current_slide["fenced_divs"] += 1
            else:
                # Closing: bare `:::`
                current_slide["fenced_divs"] -= 1

        # Detect speaker notes
        if stripped == "::: notes":
            current_slide["has_speaker_notes"] = True
            continue

        if current_slide["has_speaker_notes"]:
            current_slide["speaker_notes_lines"].append(line)
            continue

        current_slide["body_lines"].append(line)

    if current_slide is not None:
        slides.append(current_slide)

    return slides


def check_speaker_notes(slides: list[dict]) -> list[str]:
    """Check every slide has speaker notes (except splash/end with only attrs)."""
    errors = []
    for slide in slides:
        # Allow empty-heading slides (splash, end) to skip notes
        heading = slide["heading_text"]
        if heading == "":
            continue
        # Allow "Common Errors" heading (auto-animate pair, notes before AA slides)
        if heading == "Common Errors":
            continue

        if not slide["has_speaker_notes"]:
            body_preview = " ".join(slide["body_lines"][:3])[:80].strip()
            preview = f" ({body_preview}...)" if body_preview else ""
            errors.append(
                f'Slide {slide["line_start"]}: heading "{heading}"{preview} '
                f"— missing speaker notes (`::: notes`)"
            )
    return errors


def check_raw_html(slides: list[dict]) -> list[str]:
    """Check for raw HTML tags (forbidden in pure Pandoc Markdown)."""
    html_pattern = re.compile(r"<[a-zA-Z/][^>]*>")
    errors = []
    for slide in slides:
        all_text = "\n".join(slide["body_lines"])
        # Allow known Pandoc-generated spans and divs: fenced divs, bracketed spans
        # Filter out valid constructs
        stripped = re.sub(r":::\s*\{[^}]*\}", "", all_text)
        stripped = re.sub(r"\[([^\]]*)\]\{[^}]*\}", r"\1", stripped)
        # Filter inline bold/italic markers (they use *, not HTML)
        matches = html_pattern.findall(stripped)
        if matches:
            # Filter common allowed patterns
            allowed_prefixes = (
                "</div",
                "<div ",
                "<section",
                "</section",
                "<aside",
                "</aside",
                "<i ",
                "</i",
            )
            real_matches = [m for m in matches if not m.startswith(allowed_prefixes)]
            if real_matches:
                errors.append(
                    f"Slide {slide['line_start']}: raw HTML tags found: "
                    f"{', '.join(real_matches[:5])}. "
                    f"Use Pandoc Markdown instead."
                )
    return errors


def check_fenced_div_balance(slides: list[dict]) -> list[str]:
    """Check each slide has balanced fenced divs."""
    errors = []
    for slide in slides:
        if slide["fenced_divs"] != 0:
            errors.append(
                f"Slide {slide['line_start']}: unbalanced fenced divs "
                f"({slide['fenced_divs']} more openings than closings)"
            )
    return errors


def check_missing_files(md_path: Path, slides: list[dict]) -> list[str]:
    """Check referenced audio/image files exist relative to slides dir."""
    slides_dir = md_path.parent
    errors = []

    # Collect all file references from heading attrs and body
    all_text = ""
    for slide in slides:
        all_text += slide["heading_attrs"] + "\n"
        all_text += "\n".join(slide["body_lines"]) + "\n"

    # data-audio-src="assets/file.mp3"
    audio_refs = re.findall(r'data-audio-src="([^"]+)"', all_text)
    # data-background-image="assets/file.jpg"
    bg_refs = re.findall(r'data-background-image="([^"]+)"', all_text)
    # ![](assets/file.png)
    img_refs = re.findall(r"!\[\]\(([^)]+)\)", all_text)

    for ref in audio_refs + bg_refs + img_refs:
        ref_path = slides_dir / ref
        if not ref_path.exists():
            errors.append(f"Referenced file not found: {ref}")

    return errors


def check_horizontal_rules(md: str) -> list[str]:
    """Warn about `---` separators that may cause unintended slide breaks.

    Detects YAML frontmatter (--- at line 1 and its closing ---) and skips both.
    """
    warnings = []
    lines = md.split("\n")
    in_yaml = False
    for i, line in enumerate(lines, start=1):
        stripped = line.strip()
        if stripped == "---":
            if i == 1:
                # YAML frontmatter start — skip this and find the closing
                in_yaml = True
                continue
            if in_yaml:
                # YAML frontmatter end — skip and exit YAML mode
                in_yaml = False
                continue
        else:
            if in_yaml:
                continue  # still inside YAML frontmatter

        if stripped == "---":
            warnings.append(
                f"Line {i}: `---` horizontal rule found. "
                f"In Pandoc slide mode this creates a slide break. "
                f"Use only `# ` headings for slide breaks."
            )
    return warnings


def check_inline_css(md: str) -> list[str]:
    """Check for forbidden inline CSS (`style=` attributes) in slides.md.

    The agent writes PURE Pandoc Markdown only — no inline CSS. All styling
    must come from:
      - slides-pandoc.css (shared CSS file)
      - Lua filters (shield-block.lua, etc.)
      - Pandoc Markdown constructs (fenced divs, bracketed spans with classes)

    If custom styling is needed, add it to the Lua filter, not to Markdown.
    """
    errors = []
    for i, line in enumerate(md.split("\n"), start=1):
        if re.search(r"style\s*=", line):
            errors.append(
                f"Line {i}: inline CSS found (`style=`). "
                f"Do NOT write style attributes in Markdown — use a Lua filter."
            )
    return errors


def check_youtube_ids(slides: list[dict]) -> list[str]:
    """Check YouTube fenced divs have valid video IDs."""
    errors = []
    youtube_pattern = re.compile(r"::: \{\.youtube\}")
    for slide in slides:
        body = "\n".join(slide["body_lines"])
        if youtube_pattern.search(body):
            # Extract the video ID from the next non-blank line
            lines = body.split("\n")
            for i, line in enumerate(lines):
                if "::: {.youtube}" in line.strip():
                    # Look at subsequent lines for the ID
                    for j in range(i + 1, len(lines)):
                        candidate = lines[j].strip()
                        if candidate == ":::":
                            break  # closing without content
                        if candidate and not candidate.startswith(":::"):
                            # Check it's a valid 11-char YouTube ID
                            if not re.match(r"^[a-zA-Z0-9_-]{8,15}$", candidate):
                                errors.append(
                                    f"Slide {slide['line_start']}: suspicious YouTube ID "
                                    f"'{candidate}'"
                                )
                            break
    return errors


def check_css_hash() -> list[str]:
    """Check slides-pandoc.css hash hasn't been modified.

    The canonical CSS file at scripts/slides-pandoc.css is hash-locked.
    Any modification (even whitespace) will be caught here.
    Visual fixes must go through Pandoc Markdown or Lua filters — never CSS.
    """
    errors = []
    scripts_dir = Path(__file__).resolve().parent
    css_path = scripts_dir / "slides-pandoc.css"
    hash_path = css_path.with_suffix(".css.sha256")

    if not hash_path.exists():
        errors.append(f"Hash file not found: {hash_path}. Run the hash-lock setup to generate it.")
        return errors

    stored_hash = hash_path.read_text(encoding="utf-8").strip()
    current_hash = hashlib.sha256(css_path.read_bytes()).hexdigest()

    if stored_hash != current_hash:
        errors.append(
            f"slides-pandoc.css has been modified (hash mismatch).\n"
            f"  This file is hash-locked. Do NOT edit CSS.\n"
            f"  Visual fixes go through Pandoc Markdown attributes or Lua filters.\n"
            f"  If intentional, regenerate the hash: update {hash_path.name}"
        )
    return errors


def count_slides(slides: list[dict]) -> dict:
    """Produce slide statistics."""
    total = len(slides)
    with_notes = sum(1 for s in slides if s["has_speaker_notes"] or s["heading_text"] == "")
    with_content = sum(1 for s in slides if len(" ".join(s["body_lines"]).strip()) > 0)
    return {
        "total": total,
        "with_notes": with_notes,
        "with_content": with_content,
        "empty": total - with_content,
    }


# ── main ─────────────────────────────────────────────────────────────────


def main():
    if len(sys.argv) < 2:
        print(f"Usage: python {sys.argv[0]} path/to/slides.md")
        sys.exit(2)

    md_path = Path(sys.argv[1])
    if not md_path.exists():
        print(f"Error: file not found: {md_path}")
        sys.exit(2)

    print(f"\n── Validating: {md_path} ──\n")

    md = md_path.read_text(encoding="utf-8")
    slides = parse_slides(md)

    # ── slide count ──
    stats = count_slides(slides)
    print(f"   Slides: {stats['total']} total")
    print(f"   With speaker notes: {stats['with_notes']}")
    print(f"   With body content: {stats['with_content']}")
    print(f"   Empty (splash/end): {stats['empty']}\n")

    error_count = 0
    warn_count = 0

    # ── checks that produce errors (blocking) ──

    # 0. CSS hash-lock — ensure slides-pandoc.css hasn't been edited
    css_hash_errors = check_css_hash()
    for msg in css_hash_errors:
        err(msg)
        error_count += 1

    # 1. Inline CSS — agent writes Pandoc Markdown only
    css_errors = check_inline_css(md)
    for msg in css_errors:
        err(msg)
        error_count += 1

    # 1. Speaker notes
    notes_errors = check_speaker_notes(slides)
    for msg in notes_errors:
        err(msg)
        error_count += 1

    # 2. Raw HTML
    html_errors = check_raw_html(slides)
    for msg in html_errors:
        err(msg)
        error_count += 1

    # 3. Fenced div balance
    div_errors = check_fenced_div_balance(slides)
    for msg in div_errors:
        err(msg)
        error_count += 1

    # 4. Missing files
    file_errors = check_missing_files(md_path, slides)
    for msg in file_errors:
        err(msg)
        error_count += 1

    # 5. YouTube IDs
    yt_errors = check_youtube_ids(slides)
    for msg in yt_errors:
        err(msg)
        error_count += 1

    # ── checks that produce warnings (non-blocking) ──

    # 6. `---` horizontal rules
    hr_warnings = check_horizontal_rules(md)
    for msg in hr_warnings:
        warn(msg)
        warn_count += 1

    # ── summary ──
    print()
    if error_count == 0 and warn_count == 0:
        ok("All checks passed — ready to build.")
        sys.exit(0)
    elif error_count == 0:
        print(f"   {warn_count} warning(s) — build OK but review suggestions above.")
        sys.exit(1)
    else:
        print(f"   {error_count} error(s), {warn_count} warning(s) — fix errors before building.")
        sys.exit(2)


if __name__ == "__main__":
    main()

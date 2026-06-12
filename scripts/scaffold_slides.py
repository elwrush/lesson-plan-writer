"""
scaffold_slides.py — Generate reveal.js HTML skeleton with guaranteed valid structure.

Usage:
    python scripts/scaffold_slides.py --count 37 --output output/subfolder/slides/index.html

The script copies the base template, creates the assets directory, copies SFX
files and the institution logo, and inserts N empty <section> elements with
stable IDs between <div class="slides"> and </div>. The agent then fills each
section one at a time using the Edit tool.

Exit codes:
    0 — success
    1 — template not found
    2 — output path invalid
"""

import argparse
import shutil
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
TEMPLATES_DIR = PROJECT_ROOT / "templates"
SFX_DIR = Path(r"C:\PROJECTS\SFX")
LOGO_FILE = TEMPLATES_DIR / "Image_20260324_141022.png"
BASE_TEMPLATE = TEMPLATES_DIR / "base-slides-template.html"

SLIDES_DIV_OPEN = '<div class="slides">'
SLIDES_DIV_CLOSE = "</div>"


def scaffold(count: int, output_path: Path) -> int:
    """Generate slide scaffold with count empty <section> elements."""
    # Sanity checks
    if not BASE_TEMPLATE.exists():
        print(f"error: base template not found at {BASE_TEMPLATE}", file=sys.stderr)
        return 1

    output_path = output_path.resolve()
    assets_dir = output_path.parent / "assets"

    # Create output directory and assets directory
    output_path.parent.mkdir(parents=True, exist_ok=True)
    assets_dir.mkdir(parents=True, exist_ok=True)

    # Read base template
    html = BASE_TEMPLATE.read_text(encoding="utf-8")

    # Find the slides div opening boundary
    div_start = html.find(SLIDES_DIV_OPEN)
    if div_start == -1:
        print('error: could not find <div class="slides"> in template', file=sys.stderr)
        return 1

    # Find the closing </div> that matches the slides div.
    # The template structure is:
    #   <div class="slides">
    #     ...content...
    #             </div>        ← slides div close (line 640, 12-space indent)
    #         </div>            ← reveal div close (line 641, 8-space indent)
    #
    #     <!-- Mark.js (CDN) + mark plugin (local) -->
    # We search for the unique closing pattern.
    slides_close_marker = "\n            </div>\n        </div>"
    div_end = html.find(slides_close_marker, div_start)
    if div_end == -1:
        print("error: could not find slides div closing pattern in template", file=sys.stderr)
        return 1

    # div_end points to the start of "\n            </div>..."
    # Everything from here onwards is the closing + post-slides boilerplate
    after_slides = html[div_end:]

    # Build section elements
    sections = []
    for i in range(count):
        sections.append(
            f"        <!-- Slide {i} -->\n"
            f'        <section id="slide-{i}">\n'
            f"          <!-- TODO: Fill slide {i} content here -->\n"
            f"        </section>"
        )
    sections_html = "\n\n".join(sections)

    # Reassemble: header up to and including slides open + new sections + closing boilerplate
    before_slides = html[: div_start + len(SLIDES_DIV_OPEN)]
    new_html = before_slides + "\n\n" + sections_html + "\n" + after_slides

    # Write
    output_path.write_text(new_html, encoding="utf-8")

    # Copy SFX files (optional — warn if missing)
    sfx_files = ["blip.mp3", "BELL.mp3"]
    sfx_ok = True
    for sfx in sfx_files:
        src = SFX_DIR / sfx
        if src.exists():
            shutil.copy2(src, assets_dir / sfx)
        else:
            print(
                f"warning: SFX file not found at {src} (timer will run silently)", file=sys.stderr
            )
            sfx_ok = False

    # Copy timer plugin files (needed for reveal.js to initialize)
    timer_files = ["timer-plugin.js", "timer-plugin.css"]
    for tf in timer_files:
        src = TEMPLATES_DIR / tf
        if src.exists():
            shutil.copy2(src, output_path.parent / tf)

    # Copy logo (optional — warn if missing)
    if LOGO_FILE.exists():
        shutil.copy2(LOGO_FILE, assets_dir / LOGO_FILE.name)
    else:
        print(f"warning: logo file not found at {LOGO_FILE}", file=sys.stderr)

    print(f"scaffold: {count} slides -> {output_path}")
    print(f"scaffold: assets directory -> {assets_dir}")
    if sfx_ok:
        print("scaffold: SFX files copied")
    print("scaffold: done. Use Edit tool to fill each slide by its id.")

    return 0


def main():
    parser = argparse.ArgumentParser(
        description="Generate reveal.js slide scaffold with guaranteed valid structure."
    )
    parser.add_argument(
        "--count",
        type=int,
        required=True,
        help="Number of slides to scaffold",
    )
    parser.add_argument(
        "--output",
        type=str,
        required=True,
        help="Output path for index.html (e.g., output/subfolder/slides/index.html)",
    )

    args = parser.parse_args()

    if args.count < 1:
        print("error: --count must be >= 1", file=sys.stderr)
        sys.exit(2)

    output_path = Path(args.output)
    if output_path.suffix != ".html":
        print(f"error: output path must end with .html, got: {output_path.suffix}", file=sys.stderr)
        sys.exit(2)

    sys.exit(scaffold(args.count, output_path))


if __name__ == "__main__":
    main()

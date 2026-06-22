"""rebuild_slides.py — Rebuild index.html from slides.md for a slideshow.

Usage:
    python scripts/rebuild_slides.py output/<subfolder>/slides [--force]

Discovers all .lua files in the slides directory (excluding utility modules
like slide-helper.lua) and runs pandoc with the standard reveal.js
configuration. Rebuilds only if slides.md is newer than index.html,
or always if --force is passed.

Run FROM the project root so that relative asset paths resolve correctly.
"""

import pathlib
import subprocess
import sys


def rebuild(slides_dir: str, force: bool = False) -> int:
    slides = pathlib.Path(slides_dir).resolve()
    if not slides.is_dir():
        print(f"Error: {slides_dir} is not a directory")
        return 1

    slides_md = slides / "slides.md"
    index_html = slides / "index.html"

    if not slides_md.exists():
        print(f"Error: No slides.md found in {slides_dir}")
        return 1

    if not force and index_html.exists():
        slides_mtime = slides_md.stat().st_mtime
        html_mtime = index_html.stat().st_mtime
        if html_mtime >= slides_mtime:
            print("index.html is up to date — skipping rebuild")
            return 0

    # Discover Lua filters — all .lua files except slide-helper.lua
    lua_filters = []
    for f in sorted(slides.glob("*.lua")):
        if f.name == "slide-helper.lua":
            continue  # utility library, not a standalone filter
        lua_filters.append(str(f))

    # Build pandoc command
    #   --include-in-header and --css are relative to the slides directory
    #   but pandoc resolves them from its working directory, so we set cwd
    cmd = [
        "pandoc",
        str(slides_md),
        "-t",
        "revealjs",
        "-s",
        "--slide-level=1",
        "-o",
        str(index_html),
        "-V",
        "revealjs-url=https://cdn.jsdelivr.net/npm/reveal.js@5.1.0",
        "-V",
        "theme=black",
        "-V",
        "width=1280",
        "-V",
        "height=720",
        "-V",
        "margin=0.04",
        "--css=slides-pandoc.css",
        "--include-in-header=slides-header.html",
    ]
    for lf in lua_filters:
        cmd.extend(["--lua-filter", lf])

    filter_names = [pathlib.Path(f).name for f in lua_filters]
    print(f"Rebuilding {slides_dir} ...")
    print(f"  Filters: {filter_names}")

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=120,
        cwd=str(slides),  # run from slides dir so relative paths resolve
    )
    if result.returncode != 0:
        print("Pandoc failed:")
        print(result.stderr)
        return result.returncode

    if result.stderr.strip():
        for line in result.stderr.strip().split("\n"):
            if "warning" in line.lower():
                print(f"  Warning: {line.strip()}")

    print("  Done — index.html rebuilt")
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/rebuild_slides.py <slides-dir> [--force]")
        sys.exit(1)

    slides_dir = sys.argv[1]
    force = "--force" in sys.argv
    sys.exit(rebuild(slides_dir, force))

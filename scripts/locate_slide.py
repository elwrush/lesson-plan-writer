#!/usr/bin/env python3
"""
locate_slide.py - Map reveal.js slide index to markdown section

Usage:
    python scripts/locate_slide.py "file:///path/to/index.html#/7"
    python scripts/locate_slide.py 7 --slides-dir path/to/slides/
    python scripts/locate_slide.py 7 --md path/to/slides.md
"""

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse, unquote


def find_markdown_from_url(url):
    """Find markdown file from a file:// URL."""
    from urllib.parse import unquote
    url = url.strip()
    if "#" in url:
        url = url.split("#")[0]
    url = url.replace("file:///", "")
    url = url.replace("file://", "")
    url = unquote(url)
    url = url.replace("/", "\\")
    path = Path(url)
    if path.name == "index.html":
        md_files = list(path.parent.glob("*-slides.md"))
        if md_files:
            return md_files[0]
        return None
    else:
        md_path = Path(str(path).replace(".html", ".md"))
        if md_path.exists():
            return md_path
    return None


def find_markdown_from_slides_dir(slides_dir):
    """Find markdown file from a slides directory."""
    slides_dir = Path(slides_dir)
    md_files = list(slides_dir.glob("*-slides.md"))
    if md_files:
        return md_files[0]
    return None


def parse_slide_indices(md_path):
    """Parse markdown to build slide_index -> (section, start_line, end_line) mapping."""
    content = md_path.read_text(encoding="utf-8")
    lines = content.split("\n")

    slide_map = {}
    current_slide_index = None
    current_section = None
    start_line = None

    slide_pattern = re.compile(r"<!--\s*slide:\s*(\d+)\s*-->")
    section_pattern = re.compile(r"<!--\s*slide-section:\s*(\S+)\s*-->")

    for i, line in enumerate(lines, start=1):
        slide_match = slide_pattern.match(line.strip())
        if slide_match:
            current_slide_index = int(slide_match.group(1))
            start_line = i
            continue

        section_match = section_pattern.match(line.strip())
        if section_match and current_slide_index is not None:
            current_section = section_match.group(1)

        if line.strip() == "---" and current_slide_index is not None:
            slide_map[current_slide_index] = {
                "section": current_section,
                "start_line": start_line,
                "end_line": i - 1,
            }
            current_slide_index = None
            current_section = None
            start_line = None

    if current_slide_index is not None and start_line is not None:
        slide_map[current_slide_index] = {
            "section": current_section,
            "start_line": start_line,
            "end_line": len(lines),
        }

    return slide_map


def get_section_content(md_path, start_line, end_line):
    """Extract the raw content of a section."""
    content = md_path.read_text(encoding="utf-8")
    lines = content.split("\n")
    return "\n".join(lines[start_line - 1 : end_line])


def get_heading(md_path, start_line, end_line):
    """Extract the main heading from a section."""
    content = md_path.read_text(encoding="utf-8")
    lines = content.split("\n")

    for i in range(start_line - 1, min(end_line, len(lines))):
        line = lines[i].strip()
        if line.startswith("## "):
            return line[3:].strip()
    return None


def locate_slide(index, md_path):
    """Locate slide info by index."""
    slide_map = parse_slide_indices(md_path)

    if index not in slide_map:
        return None

    info = slide_map[index]
    heading = get_heading(md_path, info["start_line"], info["end_line"])
    content = get_section_content(md_path, info["start_line"], info["end_line"])

    return {
        "slide_index": index,
        "section": info["section"],
        "heading": heading,
        "slide_comment_line": f"<!-- slide: {index} -->",
        "lines": {"start": info["start_line"], "end": info["end_line"]},
        "content": content,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Map reveal.js slide index to markdown section"
    )
    parser.add_argument(
        "input",
        nargs="?",
        help="URL (file://path/index.html#/N) or slide index (N)",
    )
    parser.add_argument(
        "--slides-dir",
        help="Path to slides directory (if input is just an index)",
    )
    parser.add_argument(
        "--md",
        help="Path to markdown file",
    )
    parser.add_argument(
        "--json", action="store_true", help="Output JSON (default)"
    )
    parser.add_argument(
        "--text", action="store_true", help="Output human-readable text"
    )

    args = parser.parse_args()

    if not args.input and args.input != 0:
        parser.print_help()
        return 1

    slide_index = None
    md_path = None

    # Extract slide index from URL or use directly
    if args.input.startswith("file://") or args.input.startswith("http"):
        url = args.input
        parsed = urlparse(url)
        path = unquote(parsed.path)
        hash_part = parsed.fragment or ""
        if hash_part.startswith("/"):
            hash_part = hash_part[1:]
        if hash_part.isdigit():
            slide_index = int(hash_part)
        md_path = find_markdown_from_url(url)
    elif args.input.isdigit():
        slide_index = int(args.input)
        if args.md:
            md_path = Path(args.md)
        elif args.slides_dir:
            md_path = find_markdown_from_slides_dir(args.slides_dir)
        else:
            print("Error: Need --md or --slides-dir", file=sys.stderr)
            return 1
    else:
        print("Error: Invalid input", file=sys.stderr)
        return 1

    if md_path is None or not md_path.exists():
        print(f"Error: Markdown file not found", file=sys.stderr)
        return 1

    result = locate_slide(slide_index, md_path)

    if result is None:
        print(f"Error: Slide {slide_index} not found", file=sys.stderr)
        return 1

    if args.text:
        print(f"Slide {result['slide_index']}")
        print(f"Section: {result['section']}")
        print(f"Heading: {result['heading']}")
        print(f"Lines: {result['lines']['start']}-{result['lines']['end']}")
        print()
        print(result["content"])
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))

    return 0


if __name__ == "__main__":
    sys.exit(main())
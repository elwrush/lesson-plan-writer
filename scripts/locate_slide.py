#!/usr/bin/env python3
"""
locate_slide.py - Map reveal.js slide index to its HTML section or markdown section.

Supports two modes:
  1. HTML mode (primary) — parses raw <section> elements in index.html
  2. Markdown mode (legacy) — parses <!-- slide: N --> comments in *-slides.md

Usage:
    python scripts/locate_slide.py "file:///path/to/index.html#/7"
    python scripts/locate_slide.py 7 --slides-dir path/to/slides/
    python scripts/locate_slide.py 7 --html path/to/slides/index.html
    python scripts/locate_slide.py 7 --md path/to/slides.md
"""

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlparse


# ── URL and file resolution ────────────────────────────────────────────

def resolve_index_html_from_url(url):
    """Find raw-HTML index.html from a file:// URL.
    
    Skips markdown-based HTML files (uses is_markdown_based_html check).
    Falls back to index2.html if index.html is markdown-based.
    """
    url = url.strip()
    if "#" in url:
        url = url.split("#")[0]
    url = url.replace("file:///", "")
    url = url.replace("file://", "")
    url = unquote(url)
    url = url.replace("/", "\\")
    path = Path(url)
    
    if path.suffix == ".html" and path.exists():
        if not is_markdown_based_html(path):
            return path
        # Markdown-based — try index2.html in same directory
        alt = path.parent / "index2.html"
        if alt.exists():
            return alt
        return path  # fallback to original
    
    # If the URL points to a directory or missing file, look for index.html
    if path.is_dir():
        return find_index_html_in_slides_dir(path)
    elif path.parent.name:
        return find_index_html_in_slides_dir(path.parent)
    
    return None


def is_markdown_based_html(html_path):
    """Check if the HTML file uses the markdown plugin (old style)."""
    content = html_path.read_text(encoding="utf-8")
    return '<textarea data-template>' in content or 'data-markdown' in content[:2000]


def find_index_html_in_slides_dir(slides_dir):
    """Find a raw-HTML index.html in a slides directory.
    
    Prefers index.html first, falls back to index2.html.
    Skips markdown-based index.html files.
    """
    slides_dir = Path(slides_dir)
    
    # Try index.html
    html = slides_dir / "index.html"
    if html.exists() and not is_markdown_based_html(html):
        return html
    
    # Fall back to index2.html
    html2 = slides_dir / "index2.html"
    if html2.exists():
        return html2
    
    # Last resort: markdown-based index.html (for backward compat)
    if html.exists():
        return html
    
    return None


# ── HTML mode (primary) ────────────────────────────────────────────────

def parse_html_sections(html_path):
    """Parse index.html to build slide_index -> (heading, start_line, end_line) mapping.
    
    Counts <section> elements directly inside <div class="slides">.
    Returns list of dicts, index 0 = first slide.
    """
    content = html_path.read_text(encoding="utf-8")
    lines = content.split("\n")

    # Find the <div class="slides"> region
    slides_start = None
    slides_end = None
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith('<div class="slides"'):
            slides_start = i
        elif stripped == '</div>' and slides_start is not None and slides_end is None:
            # Find the closing </div> that corresponds to the slides container
            # We count depth to find the right one
            depth = 0
            for j in range(slides_start, len(lines)):
                tag = lines[j].strip()
                if tag.startswith('<div'):
                    depth += 1
                elif tag.startswith('</div>'):
                    depth -= 1
                    if depth == 0:
                        slides_end = j
                        break
            break

    if slides_start is None or slides_end is None:
        # Fall back: if no slides div found, parse all <section> elements
        slides_start = 0
        slides_end = len(lines)

    sections = []
    in_section = False
    section_start = None
    depth = 0

    for i in range(slides_start, min(slides_end, len(lines))):
        stripped = lines[i].strip()
        
        if stripped.startswith('<section') and not in_section:
            in_section = True
            section_start = i
            depth = 0
        
        if in_section:
            # Count nested tags
            if stripped.startswith('<section'):
                depth += 1
            if stripped.startswith('</section>'):
                depth -= 1
            if depth == 0:
                # Extract heading
                heading = None
                for j in range(section_start, i + 1):
                    h_match = re.search(r'<h[1-4][^>]*>(.*?)</h[1-4]>', lines[j])
                    if h_match:
                        # Strip HTML tags from heading text
                        heading = re.sub(r'<[^>]+>', '', h_match.group(1)).strip()
                        break
                
                section_name = heading or f"slide_{len(sections)}"
                
                sections.append({
                    "slide_index": len(sections),
                    "section": section_name,
                    "heading": heading,
                    "lines": {"start": section_start + 1, "end": i + 1},
                })
                in_section = False
    
    return sections


def get_html_section_content(html_path, start_line, end_line):
    """Extract the raw content of an HTML section."""
    content = html_path.read_text(encoding="utf-8")
    lines = content.split("\n")
    return "\n".join(lines[start_line - 1 : end_line])


# ── Markdown mode (legacy) ─────────────────────────────────────────────

def find_markdown_from_url(url):
    """Find markdown file from a file:// URL (legacy)."""
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
    """Find markdown file from a slides directory (legacy)."""
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


def get_md_section_content(md_path, start_line, end_line):
    """Extract the raw content of a markdown section."""
    content = md_path.read_text(encoding="utf-8")
    lines = content.split("\n")
    return "\n".join(lines[start_line - 1 : end_line])


def get_md_heading(md_path, start_line, end_line):
    """Extract the main heading from a markdown section."""
    content = md_path.read_text(encoding="utf-8")
    lines = content.split("\n")
    for i in range(start_line - 1, min(end_line, len(lines))):
        line = lines[i].strip()
        if line.startswith("## "):
            return line[3:].strip()
    return None


def locate_slide_md(index, md_path):
    """Locate slide info by index in markdown (legacy)."""
    slide_map = parse_slide_indices(md_path)
    if index not in slide_map:
        return None
    info = slide_map[index]
    heading = get_md_heading(md_path, info["start_line"], info["end_line"])
    content = get_md_section_content(md_path, info["start_line"], info["end_line"])
    return {
        "slide_index": index,
        "section": info["section"],
        "heading": heading,
        "lines": {"start": info["start_line"], "end": info["end_line"]},
        "content": content,
    }


def locate_slide_html(index, html_path):
    """Locate slide info by index in HTML (primary mode)."""
    sections = parse_html_sections(html_path)
    if index >= len(sections):
        return None
    info = sections[index]
    content = get_html_section_content(html_path, info["lines"]["start"], info["lines"]["end"])
    return {
        "slide_index": info["slide_index"],
        "section": info["section"],
        "heading": info["heading"],
        "lines": info["lines"],
        "content": content,
    }


# ── Main ───────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Map reveal.js slide index to HTML section (primary) or markdown section (legacy)"
    )
    parser.add_argument(
        "input", nargs="?", help="URL (file://path/index.html#/N) or slide index (N)"
    )
    parser.add_argument("--slides-dir", help="Path to slides directory")
    parser.add_argument("--html", help="Path to index.html file")
    parser.add_argument("--md", help="Path to markdown file (legacy)")
    parser.add_argument("--text", action="store_true", help="Output human-readable text")

    args = parser.parse_args()

    if not args.input and args.input != 0:
        parser.print_help()
        return 1

    slide_index = None
    html_path = None
    md_path = None

    # Extract slide index from URL or use directly
    if args.input.startswith("file://") or args.input.startswith("http"):
        url = args.input
        parsed = urlparse(url)
        hash_part = parsed.fragment or ""
        if hash_part.startswith("/"):
            hash_part = hash_part[1:]
        if hash_part.isdigit():
            slide_index = int(hash_part)
        elif hash_part.lstrip('/').isdigit():
            slide_index = int(hash_part.lstrip('/'))
        
        # Try HTML first
        html_path = resolve_index_html_from_url(url)
        if not html_path:
            md_path = find_markdown_from_url(url)

    elif args.input.isdigit():
        slide_index = int(args.input)
        if args.html:
            html_path = Path(args.html)
        elif args.md:
            md_path = Path(args.md)
        elif args.slides_dir:
            html_path = find_index_html_in_slides_dir(args.slides_dir)
            if not html_path:
                md_path = find_markdown_from_slides_dir(args.slides_dir)
        else:
            print("Error: Need --html, --md, or --slides-dir", file=sys.stderr)
            return 1
    else:
        print("Error: Invalid input", file=sys.stderr)
        return 1

    if slide_index is None:
        print("Error: Could not determine slide index", file=sys.stderr)
        return 1

    # Primary: HTML mode
    if html_path and html_path.exists():
        result = locate_slide_html(slide_index, html_path)
        if result:
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

    # Fallback: Markdown mode (legacy)
    if md_path and md_path.exists():
        result = locate_slide_md(slide_index, md_path)
        if result:
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

    print(f"Error: Slide {slide_index} not found in HTML or markdown", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
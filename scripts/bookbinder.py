#!/usr/bin/env python3
"""bookbinder.py — Convert texts to A5 booklet PDFs with gloss footnotes.

Usage:
    python scripts/bookbinder.py <input_path> [options]

Input formats: .epub, .pdf, .txt, .md

Options:
    --title <str>          Book title (default: auto-detect from filename)
    --author <str>         Author name (default: none)
    --gloss <word=def,...> Comma-separated gloss entries (e.g., "lone=to be alone,reckon=think")
    --outdir <dir>         Output directory (default: PDF/<subfolder>/)
    --font <name>          Serif font name (default: RobotoSerif)
    --font-size <pt>       Body font size in pt (default: 11)
    --leading <em>       Line leading in em (default: 0.65)
    --margin-inside <mm>   Inner margin in mm (default: 16)
    --margin-outside <mm>  Outer margin in mm (default: 11)
    --margin-top <mm>      Top margin in mm (default: 14)
    --margin-bottom <mm>   Bottom margin in mm (default: 14)
"""

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# ─── Font path for RobotoSerif (Typst needs it) ──────────────────────────
FONT_PATH = (
    Path(os.environ.get("APPDATA", ""))
    / "TinyTeX"
    / "texmf-dist"
    / "fonts"
    / "opentype"
    / "google"
    / "roboto"
)
if not FONT_PATH.exists():
    FONT_PATH = (
        Path(os.environ.get("LOCALAPPDATA", ""))
        / "TinyTeX"
        / "texmf-dist"
        / "fonts"
        / "opentype"
        / "google"
        / "roboto"
    )

TEMP_DIR = Path(os.environ.get("TEMP", "C:\\Users\\elwru\\AppData\\Local\\Temp")) / "kilo"
TEMP_DIR.mkdir(parents=True, exist_ok=True)


# ─── Text extraction ─────────────────────────────────────────────────────


def extract_text_from_epub(path: Path) -> str:
    """Extract plain text from an EPUB file using ebooklib."""
    try:
        from ebooklib import epub
    except ImportError:
        print("Error: ebooklib not installed. Run: pip install ebooklib")
        sys.exit(1)
    from html.parser import HTMLParser

    class TextStripper(HTMLParser):
        def __init__(self):
            super().__init__()
            self._parts = []
            self._skip = False

        def handle_starttag(self, tag, attrs):
            t = tag.lower()
            if t in ("script", "style"):
                self._skip = True
            elif t in ("p", "div", "br", "h1", "h2", "h3", "li", "tr"):
                if self._parts and not self._parts[-1].endswith("\n"):
                    self._parts.append("\n")

        def handle_endtag(self, tag):
            t = tag.lower()
            if t in ("script", "style"):
                self._skip = False
            if t in ("p", "h1", "h2", "h3", "li", "tr", "div"):
                if self._parts and not self._parts[-1].endswith("\n"):
                    self._parts.append("\n")

        def handle_data(self, data):
            if not self._skip:
                self._parts.append(data)

        def handle_entityref(self, name):
            m = {
                "amp": "&",
                "lt": "<",
                "gt": ">",
                "quot": '"',
                "apos": "'",
                "mdash": "\u2014",
                "ndash": "\u2013",
                "lsquo": "\u2018",
                "rsquo": "\u2019",
                "ldquo": "\u201c",
                "rdquo": "\u201d",
            }
            self._parts.append(m.get(name, f"&{name};"))

        def handle_charref(self, name):
            try:
                self._parts.append(
                    chr(int(name[1:], 16)) if name.startswith("x") else chr(int(name))
                )
            except ValueError:
                pass

        def get_text(self):
            import re as _re

            t = "".join(self._parts)
            t = _re.sub(r"\n{3,}", "\n\n", t)
            t = _re.sub(r"[ \t]+", " ", t)
            return t.strip()

    book = epub.read_epub(str(path))
    texts = []
    for item in book.get_items():
        if item.get_type() == 9:  # DOCUMENT
            html = item.get_content().decode("utf-8", errors="replace")
            stripper = TextStripper()
            stripper.feed(html)
            t = stripper.get_text()
            if t:
                texts.append(t)
    return "\n\n".join(texts)


def extract_text_from_pdf(path: Path) -> str:
    """Extract plain text from a PDF using PyMuPDF."""
    try:
        import fitz
    except ImportError:
        print("Error: pymupdf not installed. Run: pip install pymupdf")
        sys.exit(1)
    doc = fitz.open(str(path))
    texts = []
    for page in doc:
        t = page.get_text("text")
        if t.strip():
            texts.append(t.strip())
    doc.close()
    return "\n\n".join(texts)


def extract_text(path: Path) -> str:
    """Detect format and extract plain text."""
    ext = path.suffix.lower()
    if ext == ".epub":
        return extract_text_from_epub(path)
    elif ext == ".pdf":
        return extract_text_from_pdf(path)
    elif ext in (".txt", ".md"):
        return path.read_text(encoding="utf-8", errors="replace")
    else:
        print(f"Error: unsupported format '{ext}'. Supported: .epub, .pdf, .txt, .md")
        sys.exit(1)


# ─── Gloss footnote injection ────────────────────────────────────────────


def parse_gloss_string(s: str) -> list:
    """Parse 'word=definition;word2=def2' into list of (regex_pattern, word, definition).
    Uses semicolons as entry separators so definitions can contain commas.
    """
    entries = []
    for part in s.split(";"):
        part = part.strip()
        if not part:
            continue
        if "=" in part:
            word, defn = part.split("=", 1)
            word, defn = word.strip(), defn.strip()
            if not word or not defn:
                print(f"  Warning: ignoring '{part}' — empty word or definition")
                continue
            # Build the regex pattern with word boundaries
            if word == "lone":
                # Special case: match "lone" and "loned" but not "lonesome"
                pat = r"\blone(?:d)?\b"
            else:
                pat = r"\b" + re.escape(word) + r"\b"
            entries.append((pat, word, defn))
        else:
            print(f"  Warning: ignoring '{part}' — expected word=definition format")
    return entries


def inject_glosses(text: str, gloss_entries: list) -> str:
    """Add #footnote[] calls on first occurrence of each gloss word."""
    if not gloss_entries:
        return text

    paragraphs = re.split(r"\n\s*\n", text)
    already_glossed = set()
    patterns = [pat for pat, _, _ in gloss_entries]
    combined = "(" + ")|(".join(patterns) + ")"
    gloss_re = re.compile(combined)

    def _root_key(word: str) -> str:
        return word.replace(r"\b", "").replace(r"(?:d)?", "").replace(r"(?:", "").replace(r")?", "")

    def replace_fn(match):
        nonlocal already_glossed
        matched = match.group(0)
        for i, (pat, w, defn) in enumerate(gloss_entries):
            if match.group(i + 1) is not None:
                key = _root_key(w)
                if key in already_glossed:
                    return matched
                already_glossed.add(key)
                return f"{matched}#footnote[{defn}]"
        return matched

    result_paras = []
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
        result_paras.append(gloss_re.sub(replace_fn, para))
    return "\n\n".join(result_paras)


# ─── Typst document builder ──────────────────────────────────────────────


def strip_leading_heading(text: str) -> str:
    """Strip the first line if it looks like a chapter/heading line
    (e.g. 'Chapter 1', 'CHAPTER 2', 'Chapter 1: The Beginning').
    The title page already communicates the chapter — no need to repeat it in body text.
    """
    lines = text.split("\n", 1)
    if len(lines) > 0:
        first = lines[0].strip()
        if re.match(
            r"^(Chapter|CHAPTER|Ch\.|CH\.)\s*(\d+|[IVXLCDM]+|[A-Z])([:\s].*)?$",
            first,
        ):
            return lines[1].strip() if len(lines) > 1 else ""
    return text


def build_typ_document(
    body_text: str,
    title: str = "",
    author: str = "",
    font: str = "RobotoSerif",
    font_size: int = 11,
    leading: float = 0.65,
    margin_inside: int = 16,
    margin_outside: int = 11,
    margin_top: int = 14,
    margin_bottom: int = 14,
) -> str:
    """Generate a complete A5 booklet Typst document."""
    body_text = strip_leading_heading(body_text)
    title_block = ""
    if title:
        title_block = f"""
#align(center)[
  #text(size: {font_size + 5}pt, weight: "bold")[{title}]
"""
        if author:
            title_block += f"""  #v(0.1em)
  #text(size: {font_size - 2}pt, fill: luma(100))[{author}]
"""
        title_block += """  #v(0.3em)
  #line(length: 35%, stroke: 0.4pt)
]

"""

    return f"""#set text(font: "{font}", size: {font_size}pt)
#set page(
  paper: "a5",
  margin: (
    inside: {margin_inside}mm,
    outside: {margin_outside}mm,
    top: {margin_top}mm,
    bottom: {margin_bottom}mm,
  ),
  numbering: "1",
)
#set par(leading: {leading}em, justify: true)

#set footnote.entry(
  separator: [  #h(0pt)],
  clearance: 0.3em,
  gap: 0.15em,
)

{title_block}#set par(first-line-indent: 1.5em)

{body_text}
"""


# ─── Compilation ─────────────────────────────────────────────────────────


def compile_pdf(typ_src: str, output_pdf: Path) -> bool:
    """Write .typ to temp file and compile to PDF via typst CLI."""
    typ_path = TEMP_DIR / "bookbinder_temp.typ"
    typ_path.write_text(typ_src, encoding="utf-8")
    cmd = ["typst", "compile", str(typ_path), str(output_pdf)]
    if FONT_PATH.exists():
        cmd.extend(["--font-path", str(FONT_PATH)])
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    if result.returncode != 0:
        print(f"Typst compile error:\n{result.stderr}")
        return False
    return True


# ─── Main ────────────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(description="Bind a text into an A5 booklet PDF")
    parser.add_argument("input", help="Input file (.epub, .pdf, .txt, .md)")
    parser.add_argument("--title", help="Book title (auto from filename if omitted)")
    parser.add_argument("--author", default="", help="Author name")
    parser.add_argument("--gloss", help="Gloss entries: word=def,word2=def2,...")
    parser.add_argument("--outdir", help="Output directory (default: PDF/<subfolder>)")
    parser.add_argument("--font", default="RobotoSerif", help="Serif font name")
    parser.add_argument("--font-size", type=int, default=11, help="Body font size in pt")
    parser.add_argument(
        "--leading",
        type=float,
        default=0.65,
        help="Line leading in em (Typst default: 0.65; increase for more line spacing)",
    )
    parser.add_argument("--margin-inside", type=int, default=16, help="Inner margin mm")
    parser.add_argument("--margin-outside", type=int, default=11, help="Outer margin mm")
    parser.add_argument("--margin-top", type=int, default=14, help="Top margin mm")
    parser.add_argument("--margin-bottom", type=int, default=14, help="Bottom margin mm")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: input file not found: {input_path}")
        sys.exit(1)

    # Determine output path
    outdir = args.outdir
    if not outdir:
        subfolder = input_path.parent.name if input_path.parent.name != "inputs" else "output"
        outdir = str(Path("PDF") / subfolder)
    out_path = Path(outdir)
    out_path.mkdir(parents=True, exist_ok=True)

    stem = input_path.stem.replace(" ", "_")
    output_pdf = out_path / f"{stem}_A5_booklet.pdf"

    # Extract text
    print(f"Extracting text from {input_path.name} ...")
    raw_text = extract_text(input_path)
    print(f"  Extracted {len(raw_text)} chars")

    # Determine title
    title = args.title if args.title else stem.replace("_", " ")

    # Inject gloss footnotes
    gloss_entries = parse_gloss_string(args.gloss) if args.gloss else []
    if gloss_entries:
        print(f"  Adding {len(gloss_entries)} gloss entries (first occurrence only)")
        body_text = inject_glosses(raw_text, gloss_entries)
    else:
        body_text = raw_text

    # Build Typst document
    print("  Building Typst document ...")
    typ_src = build_typ_document(
        body_text,
        title=title,
        author=args.author,
        font=args.font,
        font_size=args.font_size,
        leading=args.leading,
        margin_inside=args.margin_inside,
        margin_outside=args.margin_outside,
        margin_top=args.margin_top,
        margin_bottom=args.margin_bottom,
    )

    # Count footnotes
    fn_count = typ_src.count("#footnote[")
    print(f"  {fn_count} footnote(s) inserted")

    # Compile
    print("  Compiling to PDF ...")
    if not compile_pdf(typ_src, output_pdf):
        sys.exit(1)

    print(f"\nBooklet created: {output_pdf}")
    print(f"  Format: A5, {args.font} {args.font_size}pt, leading {args.leading}em")


if __name__ == "__main__":
    main()

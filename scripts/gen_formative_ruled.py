"""Generate formative ruled paper booklets for a class.

Takes student data from Supabase classlists table,
generates individual ruled paper PDFs per student,
interleaves: St1, St2, blank, blank, St3, St4, blank, blank...
"""

import os
import subprocess
import sys
import uuid
from pathlib import Path

import fitz  # PyMuPDF

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PROJECT_ROOT = Path(r"C:\PROJECTS\LESSON-PLAN-WRITER-3")
FONT_PATH = (
    Path(os.environ.get("APPDATA") or "C:\\Users\\elwru\\AppData\\Roaming")
    / "TinyTeX"
    / "texmf-dist"
    / "fonts"
    / "opentype"
    / "google"
    / "roboto"
)

# Resolve tool paths — Windows Winget install locations
_PANDOC_CANDIDATES = [
    r"C:\Users\elwru\AppData\Local\Microsoft\WinGet\Packages\JohnMacFarlane.Pandoc_Microsoft.Winget.Source_8wekyb3d8bbwe\pandoc.exe",
    r"C:\Program Files\Pandoc\pandoc.exe",
    r"C:\Users\elwru\AppData\Local\Pandoc\pandoc.exe",
]
PANDOC_EXE = None
for c in _PANDOC_CANDIDATES:
    if Path(c).exists():
        PANDOC_EXE = c
        break
if not PANDOC_EXE:
    # Fallback: try PATH
    import shutil
    PANDOC_EXE = shutil.which("pandoc")

_TYPST_CANDIDATES = [
    r"C:\Users\elwru\AppData\Local\Programs\typst\typst.exe",
]
TYPST_EXE = None
for c in _TYPST_CANDIDATES:
    if Path(c).exists():
        TYPST_EXE = c
        break
if not TYPST_EXE:
    import shutil
    TYPST_EXE = shutil.which("typst")

for tool, name in [(PANDOC_EXE, "pandoc"), (TYPST_EXE, "typst")]:
    if not tool:
        print(f"FATAL: {name} not found")
        sys.exit(1)
    print(f"  {name}: {tool}")
OUT_DIR = PROJECT_ROOT / "PDF" / "FORMATIVE-RULED"
TEMP_DIR = PROJECT_ROOT / "tmp" / "ruled-paper"

LUA_FILTER = PROJECT_ROOT / "scripts" / "ruled-paper.lua"


def query_supabase(class_filter):
    """Query Supabase classlists table for students."""
    r = subprocess.run(
        [
            "supabase", "db", "query", "--linked", "-o", "json",
            f"SELECT student_id, name, class FROM classlists WHERE class = '{class_filter}' ORDER BY name;"
        ],
        capture_output=True, text=True, encoding="utf-8", timeout=30,
    )
    if r.returncode != 0:
        print(f"Supabase error: {r.stderr[:500]}")
        sys.exit(1)

    import json
    return json.loads(r.stdout)


def make_student_md(student, tmp_dir):
    """Write a Markdown file with YAML frontmatter for one student."""
    content = (
        "---\n"
        f'class: "{student["class"]}"\n'
        f'student_id: "{student["student_id"]}"\n'
        f'name: "{student["name"]}"\n'
        "---\n"
    )
    safe_name = student["name"].replace(" ", "_").replace("(", "").replace(")", "")
    path = tmp_dir / f"{student['student_id']}-{safe_name}.md"
    path.write_text(content, encoding="utf-8")
    return path


def make_blank_md(tmp_dir):
    """Write a Markdown file for blank ruled paper (no demographics)."""
    content = "---\nblank: true\n---\n"
    path = tmp_dir / "_blank.md"
    path.write_text(content, encoding="utf-8")
    return path


def compile_student(md_path, pdf_path):
    """Run Pandoc + Typst to produce a PDF from a Markdown file."""
    typ_path = md_path.with_suffix(".typ")

    r1 = subprocess.run(
        [
            PANDOC_EXE,
            str(md_path),
            "-t", "typst",
            "--lua-filter", str(LUA_FILTER),
            "-o", str(typ_path),
            "--wrap=none",
        ],
        capture_output=True, text=True, timeout=30,
    )
    if r1.returncode != 0:
        print(f"  Pandoc error: {r1.stderr[:300]}")
        return False

    r2 = subprocess.run(
        [
            TYPST_EXE, "compile",
            "--root", str(PROJECT_ROOT),
            "--font-path", str(FONT_PATH),
            str(typ_path),
            str(pdf_path),
        ],
        capture_output=True, text=True, timeout=60,
    )
    if r2.returncode != 0:
        print(f"  Typst error: {r2.stderr[:300]}")
        return False

    typ_path.unlink(missing_ok=True)
    return True


def interleave_booklet(student_pdfs, blank_pdf, output_path):
    """Interleave: St1p1, St2p1, blank, blank, St3p1, St4p1, blank, blank..."""
    book = fitz.open()
    blank_doc = fitz.open(str(blank_pdf))
    blank_page = blank_doc[0]  # single blank page, used twice per pair

    # Pair students
    pairs = [(student_pdfs[i], student_pdfs[i+1]) for i in range(0, len(student_pdfs) - 1, 2)]
    if len(student_pdfs) % 2 == 1:
        # Odd student out: pair with themselves
        pairs.append((student_pdfs[-1], student_pdfs[-1]))

    for st_a, st_b in pairs:
        # Student A page 1
        doc_a = fitz.open(str(st_a))
        book.insert_pdf(doc_a, from_page=0, to_page=0)
        doc_a.close()

        # Student B page 1
        doc_b = fitz.open(str(st_b))
        book.insert_pdf(doc_b, from_page=0, to_page=0)
        doc_b.close()

        # Two blank ruled pages
        book.insert_pdf(blank_doc, from_page=0, to_page=0)
        book.insert_pdf(blank_doc, from_page=0, to_page=0)

    blank_doc.close()
    total = len(book)
    book.save(str(output_path))
    book.close()
    return total


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--class", dest="class_filter", default="M2-4A",
                        help="Class to generate (e.g. M3-5A)")
    args = parser.parse_args()
    class_filter = args.class_filter

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Querying Supabase for {class_filter}...")
    students = query_supabase(class_filter)
    print(f"  Found {len(students)} students")

    # Generate blank ruled paper once
    print("Generating blank ruled paper...")
    blank_md = make_blank_md(TEMP_DIR)
    blank_pdf = TEMP_DIR / "_blank.pdf"
    if not compile_student(blank_md, blank_pdf):
        print("FATAL: blank PDF generation failed")
        sys.exit(1)
    print(f"  Blank PDF: {blank_pdf}")

    # Generate per-student PDFs
    student_pdfs = []
    for s in students:
        safe = s["name"].replace(" ", "_").replace("(", "").replace(")", "")
        md_path = make_student_md(s, TEMP_DIR)
        pdf_path = TEMP_DIR / f"{s['student_id']}-{safe}.pdf"
        print(f"  {s['class']} {s['student_id']}-{s['name']}... ", end="")
        ok = compile_student(md_path, pdf_path)
        if ok:
            student_pdfs.append(pdf_path)
            print("OK")
        else:
            print("FAIL")

    # Interleave
    output_path = OUT_DIR / f"{class_filter}-ruled-booklet.pdf"
    print(f"\nInterleaving {len(student_pdfs)} students...")
    total_pages = interleave_booklet(student_pdfs, blank_pdf, output_path)
    print(f"  Output: {output_path} ({total_pages} pages)")
    print(f"  Sheets: {total_pages // 4} (4-page blocks)")


if __name__ == "__main__":
    main()

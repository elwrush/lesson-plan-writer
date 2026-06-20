"""Generate formal ruled paper for a class — straight A4 duplex, no interleaving.

Same format as formative ruled paper, but outputs a simple concatenated PDF
(St1-p1, St1-p2, St2-p1, St2-p2, ...) for 2-sided A4 printing.
"""

import argparse
import json
import os
import subprocess
import sys
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

OUT_DIR = PROJECT_ROOT / "PDF" / "FORMAL-RULED"
TEMP_DIR = PROJECT_ROOT / "tmp" / "formal-ruled"
LUA_FILTER = PROJECT_ROOT / "scripts" / "ruled-paper.lua"


def query_supabase(class_filter):
    result = subprocess.run(
        [
            "supabase",
            "db",
            "query",
            "--linked",
            "-o",
            "json",
            f"SELECT student_id, name, class FROM classlists WHERE class = '{class_filter}' ORDER BY name;",
        ],
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=30,
    )
    if result.returncode != 0:
        print(f"Supabase error: {result.stderr[:500]}")
        sys.exit(1)
    return json.loads(result.stdout)


def make_student_md(student, tmp_dir):
    content = (
        "---\n"
        f'class: "{student["class"]}"\n'
        f'student_id: "{student["student_id"]}"\n'
        f'name: "{student["name"]}"\n'
        "---\n"
    )
    safe = student["name"].replace(" ", "_").replace("(", "").replace(")", "")
    path = tmp_dir / f"{student['student_id']}-{safe}.md"
    path.write_text(content, encoding="utf-8")
    return path


def compile_student(md_path, pdf_path):
    typ_path = md_path.with_suffix(".typ")

    r1 = subprocess.run(
        [
            PANDOC_EXE,
            str(md_path),
            "-t",
            "typst",
            "--lua-filter",
            str(LUA_FILTER),
            "-o",
            str(typ_path),
            "--wrap=none",
        ],
        capture_output=True,
        text=True,
        timeout=30,
    )
    if r1.returncode != 0:
        print(f"  Pandoc error: {r1.stderr[:300]}")
        return False

    r2 = subprocess.run(
        [
            TYPST_EXE,
            "compile",
            "--root",
            str(PROJECT_ROOT),
            "--font-path",
            str(FONT_PATH),
            str(typ_path),
            str(pdf_path),
        ],
        capture_output=True,
        text=True,
        timeout=60,
    )
    if r2.returncode != 0:
        print(f"  Typst error: {r2.stderr[:300]}")
        return False

    typ_path.unlink(missing_ok=True)
    return True


def main():
    parser = argparse.ArgumentParser(description="Generate formal ruled paper (A4 duplex)")
    parser.add_argument(
        "--class", dest="class_filter", default=None, help="Class to generate (e.g. M3-5A)"
    )
    parser.add_argument(
        "--blank", action="store_true", help="Generate blank ruled paper only (no demographics)"
    )
    args = parser.parse_args()

    if args.blank:
        OUT_DIR.mkdir(parents=True, exist_ok=True)
        TEMP_DIR.mkdir(parents=True, exist_ok=True)
        content = "---\nblank: true\n---\n"
        md_path = TEMP_DIR / "_blank.md"
        md_path.write_text(content, encoding="utf-8")
        pdf_path = OUT_DIR / "blank-ruled.pdf"
        if compile_student(md_path, pdf_path):
            print(f"Blank ruled paper: {pdf_path}")
        else:
            print("FATAL: blank PDF generation failed")
            sys.exit(1)
        return

    if not args.class_filter:
        print("Specify --class M3-5A or --blank")
        sys.exit(1)

    class_filter = args.class_filter
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    TEMP_DIR.mkdir(parents=True, exist_ok=True)

    print(f"Querying Supabase for {class_filter}...")
    students = query_supabase(class_filter)
    print(f"  Found {len(students)} students")

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

    print(f"\nMerging {len(student_pdfs)} PDFs sequentially...")
    merged = fitz.open()
    for p in student_pdfs:
        doc = fitz.open(str(p))
        merged.insert_pdf(doc)
        doc.close()

    output_path = OUT_DIR / f"{class_filter}-formal-ruled.pdf"
    merged.save(str(output_path))
    page_count = len(merged)
    merged.close()
    print(f"  Output: {output_path} ({page_count} pages)")
    print(f"  Students: {len(student_pdfs)}, Pages per student: 2")
    print("  Print 2-sided (duplex) on A4.")


if __name__ == "__main__":
    main()

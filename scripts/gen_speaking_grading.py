"""Generate speaking grading sheet booklets for classes.

Takes student data from Supabase classlists table,
generates individual grading sheet PDFs per student,
combines into per-class booklets.
"""

import os
import subprocess
import sys
from pathlib import Path

import fitz  # PyMuPDF

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PROJECT_ROOT = Path(r"C:\PROJECTS\LESSON-PLAN-WRITER-3")
OUT_DIR = PROJECT_ROOT / "PDF" / "PRONUNCIATION-MARKING-SHEETS"
TEMP_DIR = PROJECT_ROOT / "tmp" / "speaking-grading"
FONT_PATH = (
    Path(os.environ.get("APPDATA") or "C:\\Users\\elwru\\AppData\\Roaming")
    / "TinyTeX"
    / "texmf-dist"
    / "fonts"
    / "opentype"
    / "google"
    / "roboto"
)
TEMPLATE = PROJECT_ROOT / "templates" / "speaking-grading.typ"
LUA_FILTER = PROJECT_ROOT / "scripts" / "speaking-grading-sheet.lua"

# Resolve tool paths
_PANDOC_CANDIDATES = [
    r"C:\Program Files\Pandoc\pandoc.exe",
    r"C:\Users\elwru\AppData\Local\Microsoft\WinGet\Packages\JohnMacFarlane.Pandoc_Microsoft.Winget.Source_8wekyb3d8bbwe\pandoc.exe",
]
PANDOC_EXE = next((c for c in _PANDOC_CANDIDATES if Path(c).exists()), None)

_TYPST_CANDIDATES = [
    r"C:\Users\elwru\AppData\Local\Microsoft\WinGet\Packages\Typst.Typst_Microsoft.Winget.Source_8wekyb3d8bbwe\typst-x86_64-pc-windows-msvc\typst.EXE",
    r"C:\Users\elwru\AppData\Local\Programs\typst\typst.exe",
]
TYPST_EXE = next((c for c in _TYPST_CANDIDATES if Path(c).exists()), None)

if not PANDOC_EXE:
    print("FATAL: pandoc not found")
    sys.exit(1)
if not TYPST_EXE:
    print("FATAL: typst not found")
    sys.exit(1)

print(f"  pandoc: {PANDOC_EXE}")
print(f"  typst: {TYPST_EXE}")


def query_supabase(class_filter):
    """Query Supabase classlists table for students (JSON output)."""
    r = subprocess.run(
        [
            "supabase", "db", "query", "--linked", "-o", "json",
            f"SELECT student_id, name, class FROM classlists WHERE class = '{class_filter}' ORDER BY name;"
        ],
        capture_output=True, text=True, encoding="utf-8", timeout=30,
    )
    if r.returncode != 0:
        print(f"  Supabase error: {r.stderr[:300]}")
        return None
    import json
    return json.loads(r.stdout)


def compile_student(md_content, pdf_path):
    """Run Markdown through Pandoc + Lua filter + Typst to produce a single-page PDF."""
    md_path = pdf_path.with_suffix(".md")
    typ_path = pdf_path.with_suffix(".typ")
    md_path.write_text(md_content, encoding="utf-8")

    r = subprocess.run(
        [PANDOC_EXE, str(md_path), "-t", "typst",
         "--template", str(TEMPLATE),
         "--lua-filter", str(LUA_FILTER),
         "-o", str(typ_path), "--wrap=none"],
        capture_output=True, text=True, timeout=30,
    )
    if r.returncode != 0:
        print(f"  Pandoc error: {r.stderr[:200]}")
        return False

    r = subprocess.run(
        [TYPST_EXE, "compile", "--root", str(PROJECT_ROOT),
         "--font-path", str(FONT_PATH),
         str(typ_path), str(pdf_path)],
        capture_output=True, text=True, timeout=60,
    )
    if r.returncode != 0:
        print(f"  Typst error: {r.stderr[:200]}")
        return False

    # Cleanup temp files
    md_path.unlink(missing_ok=True)
    typ_path.unlink(missing_ok=True)
    return True


def make_student_md(student):
    """Build Markdown content with YAML frontmatter for one student."""
    return (
        "---\n"
        f'class: "{student["class"]}"\n'
        f'student_id: "{student["student_id"]}"\n'
        f'name: "{student["name"]}"\n'
        "---\n"
        "\n"
        "::: {.score}\n"
        ":::\n"
        "\n"
        "# Speaking Grading Sheet \u2014 Pronunciation\n"
        "\n"
        "| Band | Intonation | Intelligibility | Sentence and Word Stress | Individual Sounds |\n"
        "|------|-----------|----------------|------------------------|--------------------|\n"
        "| 5 | Intonation is natural and appropriate. | Always clear. | Stress is natural and accurate. | Sounds are clear. |\n"
        "| 4 | Between 5 and 3. | Between 5 and 3. | Between 5 and 3. | Between 5 and 3. |\n"
        "| 3 | Intonation OK in patches. | Mostly clear. | Stress OK in patches. | Some sounds muddled. |\n"
        "| 2 | Between 3 and 1. | Between 3 and 1. | Between 3 and 1. | Between 3 and 1. |\n"
        "| 1 | Intonation defects constant and obvious. | Often unclear or hard to follow. | Stress errors constant and obvious. | Many sounds unclear or distorted. |\n"
        "\n"
        "::: {.observations}\n"
        "**Special Observations**\n"
        ":::\n"
    )


def main():
    classes = ["M2-4A", "M2-5A", "M3-3A", "M3-4A", "M3-5A"]
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    for class_filter in classes:
        print(f"\n=== {class_filter} ===")
        students = query_supabase(class_filter)
        if students is None or len(students) == 0:
            print(f"  No students found for {class_filter}")
            continue
        print(f"  {len(students)} students")

        student_pdfs = []
        for s in students:
            safe = s["name"].replace(" ", "_").replace("(", "").replace(")", "")
            pdf_path = TEMP_DIR / f"{s['student_id']}-{safe}.pdf"
            md_content = make_student_md(s)

            print(f"  {s['student_id']}-{s['name']}... ", end="", flush=True)
            ok = compile_student(md_content, pdf_path)
            if ok:
                student_pdfs.append(pdf_path)
                print("OK")
            else:
                print("FAIL")

        # Combine all student PDFs into single class booklet
        booklet_path = OUT_DIR / f"{class_filter}-speaking-grading.pdf"
        book = fitz.open()
        for sp in student_pdfs:
            doc = fitz.open(str(sp))
            book.insert_pdf(doc, from_page=0, to_page=0)
            doc.close()
        book.save(str(booklet_path))
        total = len(book)
        book.close()
        print(f"  Output: {booklet_path.name} ({total} pages)")


if __name__ == "__main__":
    main()

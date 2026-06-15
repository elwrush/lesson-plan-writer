"""
linter_pdf_content.py — Validate lesson plan PDF content.

Checks:
  - PDF file is non-empty and readable
  - Has ≥ 2 pages
  - Contains expected text (masthead, lesson topic, teacher)
  - No Unicode replacement characters (encoding corruption)

Usage:
    python scripts/linter_pdf_content.py PDF/{subfolder}/{file}.pdf [expected_text...]

All PDF parsing uses PyPDF2 library. No inline python -c needed.
"""

import re
import sys
from pathlib import Path


def lint_pdf(pdf_path, expected_texts=None):
    """Validate a lesson plan PDF. Returns list of warning strings (empty = clean)."""
    try:
        from PyPDF2 import PdfReader
    except ImportError:
        return ["LINT: PyPDF2 not installed — install with: pip install PyPDF2"]

    warnings = []

    if not pdf_path.exists():
        return [f"FATAL: File not found: {pdf_path}"]
    if pdf_path.stat().st_size == 0:
        return [f"FATAL: File is empty: {pdf_path}"]

    reader = PdfReader(str(pdf_path))
    pages = len(reader.pages)

    if pages == 0:
        return ["FATAL: PDF has 0 pages"]
    if pages < 2:
        warnings.append(f"WARNING: PDF has {pages} page — expected ≥ 2")

    # Check page 1 for headings
    if pages > 0:
        p1 = reader.pages[0].extract_text() or ""
        if "Lesson Plan" not in p1:
            warnings.append("WARNING: 'Lesson Plan' heading not found on page 1")
        if "Lesson Stages" not in p1:
            warnings.append("WARNING: 'Lesson Stages' heading not found on page 1")

    # Extract all text once, check expected content and mojibake
    all_text = " ".join((p.extract_text() or "") for p in reader.pages)
    normalized_all = re.sub(r"\s+", "", all_text)
    if expected_texts:
        for t in expected_texts:
            if t:
                normalized_t = re.sub(r"\s+", "", t)
                if normalized_t not in normalized_all:
                    warnings.append(f"WARNING: Expected '{t}' not found in PDF")

    if "\ufffd" in all_text:
        warnings.append("WARNING: Unicode replacement characters found (encoding corruption)")

    return warnings


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if len(sys.argv) < 2:
        print("Usage: python scripts/linter_pdf_content.py <lesson.pdf> [expected_text...]")
        sys.exit(1)

    pdf_path = Path(sys.argv[1])
    expected = sys.argv[2:] if len(sys.argv) > 2 else None

    if not pdf_path.exists():
        print(f"FATAL: File not found: {pdf_path}")
        sys.exit(1)

    print(f"Linting PDF: {pdf_path.name}")

    warnings = lint_pdf(pdf_path, expected)
    if warnings:
        for w in warnings:
            print(f"  {w}")
        sys.exit(1 if any(w.startswith("FATAL") for w in warnings) else 0)
    else:
        print("  Clean — all checks passed")
        sys.exit(0)


if __name__ == "__main__":
    main()

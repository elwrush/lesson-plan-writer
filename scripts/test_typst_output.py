"""
Red-Green test harness for Typst document output.

Usage:
    python scripts/test_typst_output.py ^
        --typ-file typst/code/May-13-2026-handbook/index.typ ^
        --pdf-output typst/PDF/May-13-2026-handbook/index.pdf ^
        --expect-text "Mathayom Program" ^
        --expect-text "Chapter 1" ^
        --expect-page-count 2 ^
        --forbid-text "TODO" ^
        --expect-title "Mathayom Program"

Exits with code 0 (all GREEN) or 1 (one or more RED).
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

import fitz

RED = "\033[91m"
GREEN = "\033[92m"
RESET = "\033[0m"


def red(s):
    return f"{RED}{s}{RESET}"


def green(s):
    return f"{GREEN}{s}{RESET}"


def compile_typst(typ_file: Path, pdf_output: Path) -> list[str]:
    pdf_output.parent.mkdir(parents=True, exist_ok=True)
    result = subprocess.run(
        ["typst", "compile", "--root", ".", str(typ_file), str(pdf_output)],
        capture_output=True,
        text=True,
    )
    errors = []
    if result.returncode != 0:
        errors.append(result.stderr.strip())
    return errors


def extract_text(pdf_path: Path) -> str:
    doc = fitz.open(pdf_path)
    text_pages = []
    for page in doc:
        text_pages.append(page.get_text())
    doc.close()
    return "\n".join(text_pages)


def count_pages(pdf_path: Path) -> int:
    doc = fitz.open(pdf_path)
    count = doc.page_count
    doc.close()
    return count


def extract_headings(text: str) -> list[str]:
    return re.findall(r"^([A-Z][A-Za-z\s]{2,80})$", text, re.MULTILINE)


def run_tests(typ_file: Path, pdf_output: Path, args) -> tuple[bool, list[str]]:
    all_passed = True
    results = []

    # --- COMPILE TEST ---
    print(f"\n  [COMPILE] {typ_file.name} -> {pdf_output.name}")
    compile_errors = compile_typst(typ_file, pdf_output)
    if compile_errors:
        for err in compile_errors:
            print(f"    {red('RED')}  Compilation failed: {err}")
        all_passed = False
        return all_passed, ["Compilation failed — cannot proceed to PDF tests"]

    size = pdf_output.stat().st_size
    if size == 0:
        print(f"    {red('RED')}  PDF is empty (0 bytes)")
        all_passed = False
        results.append("PDF is empty")
    else:
        print(f"    {green('GREEN')} PDF created ({size:,} bytes)")

    text = extract_text(pdf_output)
    page_count = count_pages(pdf_output)

    # --- TEXT PRESENCE TESTS ---
    for expected in args.expect_text:
        if expected in text:
            print(f'    {green("GREEN")} Text present: "{expected}"')
        else:
            print(f'    {red("RED")}  Text missing: "{expected}"')
            all_passed = False
            results.append(f'Expected text not found: "{expected}"')

    # --- FORBIDDEN TEXT TESTS ---
    for forbidden in args.forbid_text:
        if forbidden not in text:
            print(f'    {green("GREEN")} Forbidden text absent: "{forbidden}"')
        else:
            print(f'    {red("RED")}  Forbidden text found: "{forbidden}"')
            all_passed = False
            results.append(f'Forbidden text found: "{forbidden}"')

    # --- PAGE COUNT TEST ---
    if args.expect_page_count is not None:
        if page_count == args.expect_page_count:
            print(
                f"    {green('GREEN')} Page count: {page_count} (expected {args.expect_page_count})"
            )
        else:
            print(f"    {red('RED')}  Page count: {page_count} (expected {args.expect_page_count})")
            all_passed = False
            results.append(f"Expected {args.expect_page_count} pages, got {page_count}")

    return all_passed, results


def main():
    parser = argparse.ArgumentParser(description="Red-Green test Typst output")
    parser.add_argument("--typ-file", required=True, type=Path, help="Path to .typ source file")
    parser.add_argument("--pdf-output", required=True, type=Path, help="Path for compiled PDF")
    parser.add_argument("--expect-text", action="append", default=[], help="Required text string")
    parser.add_argument("--forbid-text", action="append", default=[], help="Forbidden text string")
    parser.add_argument(
        "--expect-page-count", type=int, default=None, help="Expected number of pages"
    )
    args = parser.parse_args()

    typ_file = args.typ_file
    if not typ_file.exists():
        print(f"\n{red('ERROR')} .typ file not found: {typ_file}")
        sys.exit(1)

    pdf_output = args.pdf_output

    print(f"\n{'=' * 60}")
    print(f"  Red-Green Test: {typ_file.name}")
    print(f"{'=' * 60}")
    print(f"  Source:  {typ_file}")
    print(f"  PDF:     {pdf_output}")
    print(
        f"  Tests:   {len(args.expect_text)} content + {len(args.forbid_text)} forbidden + "
        f"{'page count' if args.expect_page_count is not None else 'no page count'}"
    )

    passed, failures = run_tests(typ_file, pdf_output, args)

    print(f"\n{'=' * 60}")
    if passed:
        print(f"  {green('ALL GREEN')} — all tests passed")
        sys.exit(0)
    else:
        print(f"  {red(f'{len(failures)} RED')} — some tests failed")
        for f in failures:
            print(f"    - {f}")
        sys.exit(1)


if __name__ == "__main__":
    main()

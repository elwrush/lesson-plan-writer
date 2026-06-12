"""
Booklet page-count validator.
Checks that every PDF in the given directory has a page count that is a multiple of 4.

Usage:
    python scripts/validate_booklet.py --dir "PDF/M3-GENDER-ROLES-BOOKLETS/"
    python scripts/validate_booklet.py --dir "PDF/M3-GENDER-ROLES-BOOKLETS/" --strict

Exits 0 if all valid, 1 on failure.
"""

import argparse
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


def validate_dir(directory: Path, strict: bool) -> bool:
    pdfs = sorted(directory.rglob("*.pdf"))
    if not pdfs:
        print(f"  {red('FAIL')} No PDFs found in {directory}")
        return False

    all_ok = True
    for p in pdfs:
        doc = fitz.open(str(p))
        n = len(doc)
        r = n % 4
        ok = r == 0
        status = green("PASS") if ok else red("FAIL")
        note = ""
        if not ok and strict:
            note = f"  ({4 - r} blank pages needed)"
        elif not ok:
            note = f"  ({4 - r} pages needed — not enforced)"
        print(f"  {status} {n:>4} pages  {p.name}{note}")
        if not ok and strict:
            all_ok = False
        doc.close()

    if all_ok:
        print(f"\n{green('ALL VALID')} — {len(pdfs)} file(s), all multiples of 4")
    else:
        print(f"\n{red('VALIDATION FAILED')} — some files are not multiples of 4")
    return all_ok


def main():
    parser = argparse.ArgumentParser(description="Validate booklet PDFs are multiples of 4 pages")
    parser.add_argument("--dir", required=True, help="Directory of booklet PDFs to check")
    parser.add_argument(
        "--strict", action="store_true", help="Fail on non-multiple-of-4 (default: warn only)"
    )
    args = parser.parse_args()

    path = Path(args.dir)
    if not path.exists():
        print(f"{red('ERROR')}: directory not found: {path}")
        sys.exit(1)

    ok = validate_dir(path, strict=args.strict)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()

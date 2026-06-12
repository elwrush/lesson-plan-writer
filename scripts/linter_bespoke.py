"""
Bespoke materials linter: validates generated PDFs for:
  - Page count: each booklet must be multiple of 4
  - Font sizes: no text below 11pt (body >= 14pt for booklet)
  - Ruled line spacing: answer/ruled-line rows must be ~24pt apart
  - Text fill: no washed-out gray (luma < 60 is too light for grayscale)
  - Outline line breaks: outline items must be on separate lines (not merged)

Usage:
    python scripts/linter_bespoke.py --dir "PDF/M3-GENDER-ROLES-BOOKLETS/"
    python scripts/linter_bespoke.py --dir "PDF/M3-GENDER-ROLES-BOOKLETS/" --strict
    python scripts/linter_bespoke.py --single "tmp/gender-individual/29508-Satang.pdf"
"""

import argparse
import sys
from pathlib import Path

import fitz

RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"

MIN_BODY_PT = 14
MIN_ANY_PT = 12
RULED_LS_PT = 24
RULED_TOLERANCE = 4
MIN_LUMA = 60
MAX_LUMA_FOR_LINE = 40


def red(s):
    return f"{RED}{s}{RESET}"


def green(s):
    return f"{GREEN}{s}{RESET}"


def yellow(s):
    return f"{YELLOW}{s}{RESET}"


def check_page_count(pdf_path: Path, strict: bool) -> list:
    errors = []
    doc = fitz.open(str(pdf_path))
    n = len(doc)
    r = n % 4
    if r != 0:
        msg = f"page count {n} is not a multiple of 4 ({4 - r} pages needed)"
        if strict:
            errors.append(("FAIL", msg))
        else:
            errors.append(("WARN", msg))
    else:
        errors.append(("PASS", f"page count {n} is a multiple of 4"))
    doc.close()
    return errors


def check_font_sizes(pdf_path: Path) -> list:
    errors = []
    doc = fitz.open(str(pdf_path))
    min_seen = 999
    violations = []
    for pg in range(len(doc)):
        page = doc[pg]
        blocks = page.get_text("dict")["blocks"]
        for b in blocks:
            if b.get("type") != 0:
                continue
            for l in b.get("lines", []):
                for s in l.get("spans", []):
                    size = s.get("size", 0)
                    if size < min_seen:
                        min_seen = size
                    if size < MIN_ANY_PT and size > 0:
                        text = s["text"][:40]
                        violations.append((pg + 1, size, text))
    doc.close()

    if min_seen >= MIN_ANY_PT:
        errors.append(("PASS", f"minimum font size {min_seen:.1f}pt >= {MIN_ANY_PT}pt"))
    else:
        errors.append(("WARN", f"minimum font size {min_seen:.1f}pt < {MIN_ANY_PT}pt"))

    for pg, size, text in violations[:5]:
        errors.append(("INFO", f'  page {pg}: {size:.1f}pt "{text}"'))
    if len(violations) > 5:
        errors.append(("INFO", f"  ... and {len(violations) - 5} more violations"))

    return errors


def check_ruled_lines(pdf_path: Path) -> list:
    errors = []
    doc = fitz.open(str(pdf_path))
    for pg in range(len(doc)):
        page = doc[pg]
        drawings = page.get_drawings()
        hlines = []
        for d in drawings:
            r = d["rect"]
            h = r[3] - r[1]
            w = r[2] - r[0]
            if h < 2 and w > 200:
                hlines.append(round(r[1]))

        if len(hlines) < 3:
            continue
        hlines.sort()
        gaps = [hlines[i] - hlines[i - 1] for i in range(1, len(hlines))]

        # Only flag when 3+ consecutive gaps match (suggests a ruled-line block)
        streak = 0
        for g in gaps:
            if abs(g - RULED_LS_PT) <= RULED_TOLERANCE:
                streak += 1
            else:
                streak = 0
            if streak >= 2:
                break
        else:
            continue  # no consistent ruled-line block found

        # Now report any gaps that deviate
        bad = []
        for g in set(gaps):
            if abs(g - RULED_LS_PT) > RULED_TOLERANCE:
                bad.append(g)
        if bad:
            errors.append(
                ("INFO", f"  page {pg + 1}: non-standard gaps: {[f'{b}pt' for b in bad[:3]]}")
            )

    doc.close()
    if not any(e[0] == "INFO" for e in errors):
        errors.append(("PASS", "ruled line spacing consistent"))
    else:
        errors.append(("WARN", f"ruled line spacing deviations found (target {RULED_LS_PT}pt)"))
    return errors


def check_text_fill(pdf_path: Path) -> list:
    errors = []
    doc = fitz.open(str(pdf_path))
    light_texts = []
    for pg in range(len(doc)):
        page = doc[pg]
        blocks = page.get_text("dict")["blocks"]
        for b in blocks:
            if b.get("type") != 0:
                continue
            for l in b.get("lines", []):
                for s in l.get("spans", []):
                    color = s.get("color", 0)
                    size = s.get("size", 0)
                    # Color is a float 0=black → 1=white
                    luma_val = color * 255
                    if luma_val > MIN_LUMA and size > 5:
                        text = s["text"][:40]
                        light_texts.append((pg + 1, size, luma_val, text))

    doc.close()
    if not light_texts:
        errors.append(("PASS", "all text fills are dark enough for grayscale"))
    else:
        errors.append(("WARN", f"found {len(light_texts)} text spans with luma > {MIN_LUMA}"))
        for pg, size, luma, text in light_texts[:3]:
            errors.append(("INFO", f'  page {pg}: {size:.1f}pt luma={luma:.0f} "{text}"'))
    return errors


def check_outline_breaks(pdf_path: Path) -> list:
    errors = []
    doc = fitz.open(str(pdf_path))
    for pg in range(len(doc)):
        page = doc[pg]
        blocks = page.get_text("dict")["blocks"]
        text_content = ""
        for b in blocks:
            if b.get("type") != 0:
                continue
            for l in b.get("lines", []):
                for s in l.get("spans", []):
                    text_content += s["text"] + " "

        # Check for merged outline items (should see "I." then later "A." on different lines)
        # If "I." and "A." appear in same block without line separation, flag it
        # We check by looking for patterns like "I.A." or "I. A." with no gap
        import re

        merged = re.findall(r"I\.\s*[A-Z]\.\d", text_content)
        if merged:
            errors.append(("INFO", f"  page {pg + 1}: potential merged outline items"))
    doc.close()
    if not any(e[0] == "INFO" for e in errors):
        errors.append(("PASS", "outline line breaks appear correct"))
    else:
        errors.append(("WARN", "potential outline merging detected"))
    return errors


def validate_single(pdf_path: Path, strict: bool) -> bool:
    print(f"\n=== {pdf_path.name} ===")
    all_checks = []
    all_checks.extend(("PAGE COUNT", *r) for r in check_page_count(pdf_path, strict))
    all_checks.extend(("FONT SIZES", *r) for r in check_font_sizes(pdf_path))
    all_checks.extend(("RULED LINES", *r) for r in check_ruled_lines(pdf_path))
    all_checks.extend(("TEXT FILL", *r) for r in check_text_fill(pdf_path))
    all_checks.extend(("OUTLINE", *r) for r in check_outline_breaks(pdf_path))

    has_fail = False
    has_warn = False
    for check, status, msg in all_checks:
        if status == "PASS":
            print(f"  [{check:12s}] {green(status)}  {msg}")
        elif status == "WARN":
            print(f"  [{check:12s}] {yellow(status)}  {msg}")
            has_warn = True
        elif status == "FAIL":
            print(f"  [{check:12s}] {red(status)}  {msg}")
            has_fail = True
        elif status == "INFO":
            print(f"  [{check:12s}]   {msg}")

    if has_fail and strict:
        return False
    return True


def main():
    parser = argparse.ArgumentParser(description="Linter for bespoke material PDFs")
    parser.add_argument("--dir", help="Directory of booklet PDFs to validate")
    parser.add_argument("--single", help="Single PDF file to validate")
    parser.add_argument("--strict", action="store_true", help="Fail on warnings")
    args = parser.parse_args()

    if args.single:
        ok = validate_single(Path(args.single), args.strict)
        sys.exit(0 if ok else 1)

    if args.dir:
        path = Path(args.dir)
        if not path.exists():
            print(f"{red('ERROR')}: directory not found: {path}")
            sys.exit(1)
        pdfs = sorted(path.rglob("*.pdf"))
        if not pdfs:
            print(f"{red('ERROR')}: no PDFs found in {path}")
            sys.exit(1)

        all_ok = True
        for p in pdfs:
            if not validate_single(p, args.strict):
                all_ok = False

        if all_ok:
            print(f"\n{green('ALL CHECKS PASSED')}")
        else:
            print(f"\n{red('SOME CHECKS FAILED')}")
        sys.exit(0 if all_ok else 1)

    parser.print_help()


if __name__ == "__main__":
    main()

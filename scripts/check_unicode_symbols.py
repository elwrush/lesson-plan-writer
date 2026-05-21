"""
check_unicode_symbols.py — Scan .html files for raw Unicode check/cross symbols.

Finds raw Unicode characters U+2713 (CHECK MARK ✓) and U+2717 (BALLOT X ✗)
in HTML files. These should be replaced with Font Awesome icons:
  <i class="fa-solid fa-check">  (replaces ✓)
  <i class="fa-solid fa-times"> (replaces ✗)

Usage:
    python scripts/check_unicode_symbols.py
        Scans all .html files in the project tree.
        Exits 0 if clean, 1 if any violations found.

    python scripts/check_unicode_symbols.py --fix
        Scans and replaces all occurrences in place.
"""

import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

VIOLATIONS = {
    0x2713: 'CHECK MARK (U+2713) → use <i class="fa-solid fa-check">',
    0x2717: 'BALLOT X (U+2717) → use <i class="fa-solid fa-times">',
}

REPLACEMENTS = {
    chr(0x2713): '<i class="fa-solid fa-check"></i>',
    chr(0x2717): '<i class="fa-solid fa-times"></i>',
}


def scan_file(path: Path):
    """Return list of (line_number, char_code) violations in a file."""
    text = path.read_text(encoding="utf-8", errors="replace")
    violations = []
    for i, line in enumerate(text.split("\n"), 1):
        for ch in line:
            if ord(ch) in VIOLATIONS:
                violations.append((i, ord(ch)))
    return violations, text


def main():
    fix = "--fix" in sys.argv
    project_root = Path(__file__).resolve().parent.parent
    html_files = sorted(project_root.rglob("*.html"))

    any_violations = False
    for path in html_files:
        violations, text = scan_file(path)
        if not violations:
            continue

        any_violations = True
        rel = path.relative_to(project_root)
        for line_no, code in violations:
            print(
                f"{rel}:{line_no}: raw Unicode {VIOLATIONS[code]}",
                file=sys.stderr,
            )

        if fix:
            for old, new in REPLACEMENTS.items():
                text = text.replace(old, new)
            path.write_text(text, encoding="utf-8")
            print(f"  \u2192 Fixed: {rel}", file=sys.stderr)

    if any_violations and not fix:
        print(
            "FAILED: raw Unicode check/cross symbols found. Run with --fix to auto-replace.",
            file=sys.stderr,
        )
        return 1

    if fix and any_violations:
        print("FIXED: all raw Unicode check/cross symbols replaced.", file=sys.stderr)
    else:
        print("OK: no raw Unicode check/cross symbols found.", file=sys.stderr)

    return 0


if __name__ == "__main__":
    sys.exit(main())

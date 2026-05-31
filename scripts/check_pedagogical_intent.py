"""
check_pedagogical_intent.py — Verify every slide has pedagogical intent annotations.

Scans the output HTML file and checks that every non-exempt <section> is
preceded by the three mandatory annotation comments (PEDAGOGICAL INTENT,
WHY THIS FEATURE, COGNITIVE PRINCIPLE).

Usage:
    python scripts/check_pedagogical_intent.py output/<subfolder>/slides/index.html
        Exit 0 if all slides annotated, 1 if any violations found.

    python scripts/check_pedagogical_intent.py --project output/<subfolder>/slides/
        Same, scans index.html inside the project directory.
"""

import os
import re
import sys

# Slide ID prefixes that are exempt from pedagogical intent (orientation/structural)
EXEMPT_PREFIXES = (
    "slide-transition-",
    "slide-end",
    "slide-title",
    "slide-objective",
)

ALLOWED_FEATURES = [
    "auto-animate",
    "fragments",
    "sibling slides",
    "data-line-numbers",
    "data-mark",
    "data-transition",
    "data-background-gradient",
    "vertical slides",
    "audio",
    "autoslide",
    "code blocks",
    "lightbox",
    "r-fit-text",
    "static",
]


def check_file(path: str) -> int:
    with open(path, encoding="utf-8") as f:
        content = f.read()

    # Find all <section> elements with their positions
    pattern = re.compile(
        '<section\\s+id="(?P<id>slide-[^"]+)"[^>]*>',
    )

    violations = []

    for match in pattern.finditer(content):
        section_id = match.group("id")

        # Skip exempt slides
        if section_id.startswith(EXEMPT_PREFIXES):
            continue

        # Look at the 1000 characters immediately before this <section> tag
        preceding_start = max(0, match.start() - 1000)
        preceding = content[preceding_start : match.start()]

        # Check that the last comment block before this section contains both annotations
        has_intent = "PEDAGOGICAL INTENT:" in preceding
        has_feature = "WHY THIS FEATURE:" in preceding
        has_principle = "COGNITIVE PRINCIPLE:" in preceding

        if not has_intent or not has_feature or not has_principle:
            line_num = content[: match.start()].count("\n") + 1
            missing = []
            if not has_intent:
                missing.append("PEDAGOGICAL INTENT")
            if not has_feature:
                missing.append("WHY THIS FEATURE")
            if not has_principle:
                missing.append("COGNITIVE PRINCIPLE")
            violations.append((line_num, section_id, missing))

    if violations:
        print("PEDAGOGICAL INTENT CHECK FAILED:", file=sys.stderr)
        for line, sid, missing in violations:
            print(
                f"  {path}:{line}: {sid} — missing {', '.join(missing)}",
                file=sys.stderr,
            )
        print(
            "Every non-exempt slide must have all three:",
            file=sys.stderr,
        )
        print(
            "  <!-- PEDAGOGICAL INTENT: [what the student must SEE happen] -->",
            file=sys.stderr,
        )
        print(
            "  <!-- WHY THIS FEATURE: [reveal.js feature + why alternatives fail] -->",
            file=sys.stderr,
        )
        return 1

    print("OK: all slides have pedagogical intent annotations.", file=sys.stderr)
    return 0


def main():
    args = sys.argv[1:]

    if not args:
        print("Usage: check_pedagogical_intent.py <path-to-index.html>", file=sys.stderr)
        print("   or: check_pedagogical_intent.py --project <slides-dir>", file=sys.stderr)
        return 1

    if args[0] == "--project" and len(args) >= 2:
        path = os.path.join(args[1], "index.html")
    else:
        path = args[0]

    if not os.path.exists(path):
        print(f"File not found: {path}", file=sys.stderr)
        return 1

    return check_file(path)


if __name__ == "__main__":
    sys.exit(main())

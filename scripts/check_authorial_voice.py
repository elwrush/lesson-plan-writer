"""Check pedagogical annotations for Authorial Voice compliance.

Returns non-zero exit code if any violations found. Reports:
- "Same as" / "Same pattern" lazy cross-references
- WHY THIS FEATURE lines that are too brief (<25 chars after label)
- DESIGN MECHANISM lines that mention HTML/CSS/reveal.js technical details
  without a teaching rationale
- Identical annotation blocks used on multiple consecutive slides (non-answer)
"""

import re
import sys


def check_authorial_voice(html_path: str) -> int:
    exit_code = 0

    with open(html_path, encoding="utf-8") as f:
        content = f.read()

    pattern = re.compile(
        r"<!-- PEDAGOGICAL INTENT:(.*?)-->"
        r"\s*<!-- WHY THIS FEATURE:(.*?)-->"
        r"\s*<!-- COGNITIVE PRINCIPLE:(.*?)-->"
        r"\s*<!-- DESIGN MECHANISM:(.*?)-->",
        re.DOTALL,
    )

    blocks = list(pattern.findall(content))
    prev_text = None
    identical_count = 0
    violations = []

    for i, (pi, wtf, cp, dm) in enumerate(blocks):
        slide_num = i + 1
        pi = pi.strip().rstrip(" --")
        wtf = wtf.strip().rstrip(" --")
        cp = cp.strip().rstrip(" --")
        dm = dm.strip().rstrip(" --")

        # Check 1: "Same as", "Same pattern", "Identical structure"
        lazy_patterns = ["same as", "same pattern", "identical struct", "identical pattern"]
        for field_name, field_val in [
            ("PEDAGOGICAL INTENT", pi),
            ("WHY THIS FEATURE", wtf),
            ("COGNITIVE PRINCIPLE", cp),
            ("DESIGN MECHANISM", dm),
        ]:
            lower = field_val.lower()
            for lp in lazy_patterns:
                if lp in lower:
                    violations.append(
                        {
                            "slide": slide_num,
                            "field": field_name,
                            "issue": f"lazy-reference: contains '{lp}'",
                            "text": field_val[:80],
                            "severity": "error"
                            if "pedagogical" in field_name.lower()
                            else "warning",
                        }
                    )

        # Check 2: WHY THIS FEATURE too thin (<25 substantive chars)
        wtf_stripped = (
            wtf.replace("static", "")
            .replace("fragment fade-up", "")
            .replace("fragment", "")
            .strip()
        )
        if len(wtf_stripped) < 25 and slide_num != 1:
            violations.append(
                {
                    "slide": slide_num,
                    "field": "WHY THIS FEATURE",
                    "issue": "too-thin: no rationale for feature choice",
                    "text": wtf[:60],
                    "severity": "warning",
                }
            )

        # Check 3: DESIGN MECHANISM mentions implementation without teaching impact
        dm_has_technical = any(
            t in dm.lower()
            for t in [
                "html",
                "css",
                "flex layout",
                "data-background",
                "data-audio-src",
                "data-autoplay",
                "reveal.js's",
                "data-vocab-audio",
                "javascript",
                "a-why class",
                "call startembeddedcontent",
                "queryselector",
            ]
        )
        dm_has_rationale = any(
            t in dm.lower()
            for t in [
                "without",
                "if removed",
                "so the student",
                "so the learner",
                "the teacher can",
                "students can",
                "so that the",
            ]
        )
        if dm_has_technical and not dm_has_rationale:
            violations.append(
                {
                    "slide": slide_num,
                    "field": "DESIGN MECHANISM",
                    "issue": "technical-only: describes implementation without teaching rationale",
                    "text": dm[:80],
                    "severity": "warning",
                }
            )

        # Track identical blocks
        block_text = pi + "|" + wtf + "|" + cp + "|" + dm

        # Check 4: Identical blocks on consecutive slides -- exempt answer slides
        is_answer = any(
            t in pi.lower()
            for t in ["answer", "a-row", "badge", "correction", "comprehension question"]
        )
        if is_answer:
            identical_count = 0
            prev_text = None
        elif block_text == prev_text:
            identical_count += 1
            if identical_count >= 3:
                violations.append(
                    {
                        "slide": slide_num,
                        "field": "all",
                        "issue": f"identical-annotation: same block repeated {identical_count + 1} times",
                        "text": pi[:60],
                        "severity": "error",
                    }
                )
        else:
            identical_count = 0
        prev_text = block_text

    if violations:
        print(f"\nAuthorial Voice Check -- {len(violations)} violation(s)\n")
        for v in violations:
            icon = "ERROR" if v["severity"] == "error" else "WARN"
            print(f"  [{icon}] Slide {v['slide']} {v['field']}: {v['issue']}")
            print(f'         Text: "{v["text"]}"')
            print()
        if any(v["severity"] == "error" for v in violations):
            exit_code = 1
    else:
        print("\nAuthorial Voice Check -- all annotations pass")

    return exit_code


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True, help="Path to slides directory")
    args = parser.parse_args()
    import os

    html_path = os.path.join(args.project, "index.html")
    sys.exit(check_authorial_voice(html_path))

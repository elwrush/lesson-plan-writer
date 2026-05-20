"""
audit_slides.py — Cross-reference slide content against lesson plan JSON.

Usage:
    python scripts/audit_slides.py --plan output/.../lesson-plan.json --html output/.../slides/index.html
    python scripts/audit_slides.py --plan output/.../lesson-plan.json --html output/.../slides/index.html --verbose
"""

import argparse
import json
import re
import sys
from pathlib import Path


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def load_html(path):
    return path.read_text(encoding="utf-8")


def extract_exercise_refs(text):
    """Extract exercise references and page numbers from text."""
    refs = []
    # Exercise names: Practice N, Practice NA, Practice NB
    for m in re.finditer(r"Practice\s+(\d+[A-Z]?)(?:\s*[—–-]\s*([^,.]+))?", text):
        num = m.group(1)
        title = m.group(2).strip() if m.group(2) else ""
        refs.append(("exercise", f"Practice {num}", title))

    # Page numbers: p. N or pp. N-N
    for m in re.finditer(r"p[p]?\.\s*(\d+(?:[–—\u2013\u2014-]\d+)?)", text):
        refs.append(("page", m.group(1), ""))

    return refs


def extract_stage_info(plan):
    """Extract exercise references from each stage in the lesson plan."""
    stages = []
    for stage in plan.get("lesson_plan", {}).get("stages", []):
        num = stage.get("stage_number")
        name = stage.get("stage", "")
        procedure = stage.get("procedure", "")
        refs = extract_exercise_refs(procedure)
        stages.append(
            {
                "number": num,
                "name": name,
                "refs": refs,
            }
        )
    return stages


def extract_slide_info(html):
    """Extract exercise/page references from each slide's visible content."""
    slides = []
    # Split by slide comments
    parts = re.split(r"<!-- SLIDE \d+:.*?-->", html)
    comments = re.findall(r"<!-- SLIDE \d+:.*?-->", html)

    for i, (comment, content) in enumerate(zip(comments, parts[1:])):
        title_match = re.search(r"SLIDE \d+: (.*?)\s*-->", comment)
        title = title_match.group(1).strip() if title_match else f"slide_{i}"

        # Extract refs from visible HTML (not in aside.notes)
        visible = re.sub(r"<aside class=\"notes\">.*?</aside>", "", content, flags=re.DOTALL)
        refs = extract_exercise_refs(visible)

        slides.append(
            {
                "index": i,
                "title": title,
                "refs": refs,
            }
        )
    return slides


def safe_print(text):
    """Print with non-ASCII characters replaced for Windows console."""
    safe = "".join(ch if ord(ch) < 128 else "?" for ch in text)
    print(safe)


def audit(plan_path, html_path, verbose=False):
    """Run the audit and return (pass_count, fail_count, issues)."""
    plan = load_json(plan_path)
    html = load_html(html_path)

    stages = extract_stage_info(plan)
    slides = extract_slide_info(html)

    issues = []
    passes = 0

    def check(condition, msg):
        nonlocal passes
        if condition:
            passes += 1
            if verbose:
                safe_print(f"  PASS: {msg}")
        else:
            issues.append(msg)
            safe_print(f"  FAIL: {msg}")

    safe_print(f"\n--- Audit: {plan_path.name} vs {html_path.name} ---\n")

    # 1. Stage coverage
    safe_print("Stage coverage:")
    for stage in stages:
        stage_num = stage["number"]
        stage_name = stage["name"]
        matching = [
            s
            for s in slides
            if stage_name.lower() in s["title"].lower()
            or f"stage {stage_num}" in s["title"].lower()
            or stage_name.split("?")[0].strip().lower() in s["title"].lower()
        ]
        if not matching:
            keywords = stage_name.lower().replace("?", "").split()
            keywords = [k for k in keywords if len(k) > 3]
            matching = [s for s in slides if any(k in s["title"].lower() for k in keywords)]
        check(
            len(matching) > 0,
            f'Stage {stage_num} "{stage_name}" has {len(matching)} matching slide(s)',
        )
        if verbose and matching:
            for s in matching:
                safe_print(f"    -> Slide {s['index']}: {s['title'][:55]}")

    # 2. Exercise name consistency
    safe_print("\nExercise references:")
    plan_exercises = set()
    for stage in stages:
        for ref_type, ref_name, ref_title in stage["refs"]:
            if ref_type == "exercise":
                plan_exercises.add(ref_name)

    slide_exercises = set()
    for slide in slides:
        for ref_type, ref_name, ref_title in slide["refs"]:
            if ref_type == "exercise":
                slide_exercises.add(ref_name)

    for ex in sorted(plan_exercises):
        found = any(
            ex.lower() in s["title"].lower() or ex.lower() in str(s["refs"]).lower() for s in slides
        )
        if not found and ("Test" in ex or "Diagnostic" in ex):
            # Bespoke diagnostics legitimately replace textbook exercises
            passes += 1
            if verbose:
                safe_print(
                    f'  PASS: Exercise "{ex}" (lesson plan) — bespoke diagnostic replaces this'
                )
        else:
            check(found, f'Exercise "{ex}" (lesson plan) is referenced on slides')

    for ex in sorted(slide_exercises):
        found = ex in plan_exercises
        if not found:
            if "Test" in ex or "Quick" in ex:
                passes += 1
                if verbose:
                    safe_print(f'  PASS: Exercise "{ex}" is bespoke (diagnostic/test)')
            else:
                issues.append(f'Exercise "{ex}" appears in slides but not in lesson plan')
                safe_print(f'  FAIL: Exercise "{ex}" appears in slides but not in lesson plan')

    # 3. Page number consistency
    safe_print("\nPage references:")
    plan_pages = set()
    for stage in stages:
        for ref_type, ref_val, _ in stage["refs"]:
            if ref_type == "page":
                plan_pages.add(ref_val)

    slide_pages = set()
    for slide in slides:
        for ref_type, ref_val, _ in slide["refs"]:
            if ref_type == "page":
                slide_pages.add(ref_val)

    for pg in sorted(plan_pages):
        found = any(pg in str(s["refs"]) or pg in s["title"] for s in slides)
        check(found, f'Page "{pg}" (from lesson plan) appears in slides')

    for pg in sorted(slide_pages):
        check(pg in plan_pages, f'Page "{pg}" appears in slides but not in lesson plan')

    # 4. Content quality checks
    safe_print("\nContent quality:")
    # Only check inside <div class="slides">...</div> (exclude script configs, header, footer)
    slides_match = re.search(r'<div\s+class="slides"[^>]*>(.*?)</div>\s*</div>', html, re.DOTALL)
    slides_content = slides_match.group(1) if slides_match else html
    visible = re.sub(r"<aside class=\"notes\">.*?</aside>", "", slides_content, flags=re.DOTALL)
    full_text_no_tags = re.sub(r"<[^>]+>", " ", visible)

    banned_patterns = ["Source: First Steps", "Teacher:", "Duration:"]
    for pattern in banned_patterns:
        check(pattern not in full_text_no_tags, f'No banned text "{pattern}" on slides')

    safe_print(f"\n{'=' * 50}")
    total_checks = passes + len(issues)
    safe_print(f"Audit complete: {passes}/{total_checks} passed, {len(issues)} issue(s)")
    if issues:
        safe_print("Issues:")
        for i in issues:
            safe_print(f"  ? {i}")

    return passes, issues


def main():
    parser = argparse.ArgumentParser(
        description="Cross-reference slide content against lesson plan JSON"
    )
    parser.add_argument("--plan", required=True, help="Path to lesson plan JSON")
    parser.add_argument("--html", required=True, help="Path to slides index.html")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show passes too")
    args = parser.parse_args()

    plan_path = Path(args.plan)
    html_path = Path(args.html)

    if not plan_path.exists():
        print(f"Error: Lesson plan not found: {plan_path}", file=sys.stderr)
        return 1
    if not html_path.exists():
        print(f"Error: Slides HTML not found: {html_path}", file=sys.stderr)
        return 1

    passes, issues = audit(plan_path, html_path, verbose=args.verbose)
    return 1 if issues else 0


if __name__ == "__main__":
    sys.exit(main())

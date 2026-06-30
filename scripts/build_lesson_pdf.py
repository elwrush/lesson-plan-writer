"""
build_lesson_pdf.py — Markdown → Pandoc → Typst → PDF

Three-layer architecture:
  1. Static Typst template (templates/lesson-plan.typ) — locked, hash-verified
  2. Pandoc — converts Markdown YAML frontmatter + stages to Typst via template
  3. This script — validates input, runs Pandoc + Typst, lints output

Usage:
    python scripts/build_lesson_pdf.py path/to/lesson.md

The agent writes a single .md file with YAML frontmatter for metadata
and Markdown body for stages. A Lua filter transforms stages into a Typst table.

No inline python -c, no PowerShell quoting issues.
All Python code lives in .py files.
"""

import hashlib
import io
import json
import os
import re
import subprocess
import sys
import uuid
from datetime import datetime
from pathlib import Path

from pydantic import ValidationError

# ── Paths ──
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.models import LessonPlanFrontmatter  # noqa: E402

TEMPLATES_DIR = PROJECT_ROOT / "templates"
TEMPLATE = TEMPLATES_DIR / "lesson-plan.typ"
LUA_FILTER = PROJECT_ROOT / "scripts" / "lesson-tables.lua"
TEMPLATE_LOCK = PROJECT_ROOT / ".template-lock.json"
PDF_OUTPUT_DIR = PROJECT_ROOT / "PDF"

# Roboto font directory (TinyTeX bundled)
ROBOTO_FONT_DIR = Path(
    os.path.expandvars(r"%APPDATA%\TinyTeX\texmf-dist\fonts\opentype\google\roboto")
)

# ══════════════════════════════════════════════════════════════════════════
# TEMPLATE VERIFICATION
# ══════════════════════════════════════════════════════════════════════════


def verify_template():
    """Check template exists and hash matches lock file."""
    if not TEMPLATE.exists():
        print(f"FATAL: Template not found: {TEMPLATE}", file=sys.stderr)
        sys.exit(1)

    if not TEMPLATE_LOCK.exists():
        actual = hashlib.sha256(TEMPLATE.read_bytes()).hexdigest().upper()
        TEMPLATE_LOCK.write_text(
            json.dumps({"lesson-plan.typ": {"sha256": actual}}, indent=2),
            encoding="utf-8",
        )
        print(f"  Created template lock: {TEMPLATE_LOCK.name}")
        return

    lock = json.loads(TEMPLATE_LOCK.read_text(encoding="utf-8"))
    expected = lock.get("lesson-plan.typ", {}).get("sha256", "")
    actual = hashlib.sha256(TEMPLATE.read_bytes()).hexdigest().upper()

    if expected and actual != expected:
        print(
            f"FATAL: Template hash mismatch!\n"
            f"  Expected: {expected}\n"
            f"  Actual:   {actual}\n\n"
            f"The template has changed since it was locked.\n"
            f"Delete {TEMPLATE_LOCK} to acknowledge the change and re-lock.",
            file=sys.stderr,
        )
        sys.exit(1)


# ══════════════════════════════════════════════════════════════════════════
# MARKDOWN VALIDATION (lint step)
# ══════════════════════════════════════════════════════════════════════════


def parse_frontmatter(md_path):
    """Parse YAML frontmatter from a Markdown file.

    Returns (metadata_dict, body_text) or exits on fatal error.
    Uses pyyaml — no inline python -c needed.
    """
    import yaml

    text = md_path.read_text(encoding="utf-8")

    # Extract between --- markers
    m = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if not m:
        print(f"FATAL: No YAML frontmatter (--- ... ---) found in {md_path.name}", file=sys.stderr)
        sys.exit(1)

    frontmatter = m.group(1)
    body = text[m.end() :].strip()

    try:
        meta = yaml.safe_load(frontmatter)
    except yaml.YAMLError as e:
        print(f"FATAL: YAML parse error in {md_path.name}:\n  {e}", file=sys.stderr)
        sys.exit(1)

    if not isinstance(meta, dict):
        print("FATAL: YAML frontmatter must be a key: value mapping", file=sys.stderr)
        sys.exit(1)

    return meta, body


def validate_metadata(meta):
    """Check required metadata fields via Pydantic model. Returns list of warning strings."""
    warnings = []
    try:
        LessonPlanFrontmatter.model_validate(meta)
    except ValidationError as e:
        for err in e.errors():
            field = ".".join(str(p) for p in err["loc"])
            warnings.append(f"MISSING/INVALID: '{field}' in YAML frontmatter — {err['msg']}")
    return warnings


def lint_markdown(md_path):
    """Full Markdown validation. Returns True if passable (warnings ok)."""
    meta, body = parse_frontmatter(md_path)
    warnings = []

    # Metadata checks
    warnings.extend(validate_metadata(meta))

    # Check stage headings in Markdown body
    stage_headings = re.findall(r"^##\s+Stage\s+(\d+):", body, re.MULTILINE)
    if not stage_headings:
        warnings.append("FATAL: No '## Stage N:' headings found in body")
    else:
        stage_nums = [int(n) for n in stage_headings]
        expected = list(range(1, len(stage_nums) + 1))
        if stage_nums != expected:
            warnings.append(f"WARNING: Non-sequential stage numbers: {stage_nums}")

        time_matches = re.findall(r"\*\*Time:\*\*\s+(\d+)", body)
        if time_matches:
            total_time = sum(int(t) for t in time_matches)
            duration_str = str(meta.get("duration", ""))
            dur_match = re.search(r"(\d+)", duration_str)
            if dur_match:
                duration_minutes = int(dur_match.group(1))
                if total_time != duration_minutes:
                    warnings.append(
                        f"WARNING: Stage total ({total_time} min) != duration ({duration_minutes} min)"
                    )

    # Report
    issues = [w for w in warnings if w.startswith("FATAL")]
    for w in warnings:
        print(f"  {w}")

    return len(issues) == 0


# ══════════════════════════════════════════════════════════════════════════
# PANDOC → TYPST → PDF
# ══════════════════════════════════════════════════════════════════════════


def pandoc_to_typst(md_path):
    """Run Pandoc to convert Markdown → Typst via template.

    Returns Typst source string, or exits on error.
    Captures Pandoc stderr separately from stdout.
    """
    proc = None
    cmd = [
        "pandoc",
        "--from",
        "markdown+yaml_metadata_block",
        "--template",
        str(TEMPLATE),
        "--lua-filter",
        "scripts/table-content-fit.lua",
        "--lua-filter",
        str(LUA_FILTER),
        "--lua-filter",
        "scripts/pagebreak.lua",
        "--to",
        "typst",
        "--wrap",
        "none",
        "--eol",
        "lf",
        str(md_path),
    ]

    try:
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stdout, stderr = proc.communicate(timeout=30)
    except subprocess.TimeoutExpired:
        if proc:
            proc.kill()
        print("FATAL: Pandoc timed out (30s)", file=sys.stderr)
        sys.exit(1)

    except FileNotFoundError:
        print("FATAL: Pandoc not found. Install from https://pandoc.org", file=sys.stderr)
        sys.exit(1)

    if proc.returncode != 0:
        err_text = stderr.decode("utf-8", errors="replace")[:500] if stderr else "(no stderr)"
        print(f"FATAL: Pandoc error (exit {proc.returncode})", file=sys.stderr)
        print(f"  {err_text}", file=sys.stderr)
        sys.exit(1)

    if stderr:
        stderr_text = stderr.decode("utf-8", errors="replace").strip()
        if stderr_text:
            print(f"  Pandoc stderr: {stderr_text[:300]}")

    return stdout.decode("utf-8")


def compile_typst(typst_source, output_pdf):
    """Compile Typst source to PDF.

    Writes Pandoc output as a temp .typ file in the project root
    so template-relative image paths resolve correctly.
    Always cleans up the temp file — errors print to stderr but do NOT leave
    orphaned temp files in the project root."""
    # Write temp .typ in the project root for template-relative paths like templates/cambridge.png
    temp_typ = PROJECT_ROOT / f"_temp_lesson_{uuid.uuid4().hex[:8]}.typ"
    temp_typ.write_text(typst_source, encoding="utf-8")

    proc = None
    typst_cmd = ["typst", "compile"]
    if ROBOTO_FONT_DIR.exists():
        typst_cmd += ["--font-path", str(ROBOTO_FONT_DIR)]
    typst_cmd += [str(temp_typ), str(output_pdf)]

    try:
        proc = subprocess.Popen(
            typst_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        _, stderr = proc.communicate(timeout=60)
    except subprocess.TimeoutExpired:
        if proc:
            proc.kill()
        temp_typ.unlink(missing_ok=True)
        print("FATAL: Typst timed out (60s)", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        temp_typ.unlink(missing_ok=True)
        print(
            "FATAL: Typst CLI not found. Install from https://github.com/typst/typst",
            file=sys.stderr,
        )
        sys.exit(1)

    if proc.returncode != 0:
        err_text = stderr.decode("utf-8", errors="replace")[:1000] if stderr else "(no stderr)"
        temp_typ.unlink(missing_ok=True)
        print(f"FATAL: Typst compile failed (exit {proc.returncode})", file=sys.stderr)
        print(f"  {err_text}", file=sys.stderr)
        sys.exit(1)

    temp_typ.unlink(missing_ok=True)
    return True


# ══════════════════════════════════════════════════════════════════════════
# PDF LINTING
# ══════════════════════════════════════════════════════════════════════════


def lint_pdf(pdf_path, expected_texts=None):
    """Validate the generated PDF using PyPDF2.

    Checks:
    - File exists and is non-empty
    - PDF has ≥ 2 pages
    - Contains expected text (lesson topic, teacher, stages)
    - No replacement characters (encoding corruption)

    Returns list of warnings (empty = clean).
    """
    try:
        from PyPDF2 import PdfReader
    except ImportError:
        print("  LINT: PyPDF2 not installed — skipping PDF checks")
        return []

    warnings = []

    if not pdf_path.exists() or pdf_path.stat().st_size == 0:
        return ["FATAL: PDF file is empty or missing"]

    reader = PdfReader(str(pdf_path))
    pages = len(reader.pages)

    if pages == 0:
        return ["FATAL: PDF has 0 pages"]
    if pages < 2:
        warnings.append(f"WARNING: PDF has only {pages} page — expected ≥ 2")

    # Check first page for masthead
    page1 = reader.pages[0].extract_text() or ""
    if "Lesson Plan" not in page1:
        warnings.append("WARNING: 'Lesson Plan' heading not found on page 1")

    # Check all pages for expected text and mojibake
    # PyPDF2 extracts with spacing artifacts (e.g. "T eacher"), so normalize
    all_text = " ".join((p.extract_text() or "") for p in reader.pages)
    normalized_all = re.sub(r"\s+", "", all_text)

    if expected_texts:
        for text in expected_texts:
            if text:
                normalized_text = re.sub(r"\s+", "", text)
                if normalized_text not in normalized_all:
                    warnings.append(f"WARNING: Expected text '{text}' not found in PDF")

    if "\ufffd" in all_text:
        warnings.append("WARNING: Unicode replacement characters found — encoding corruption")

    return warnings


# ══════════════════════════════════════════════════════════════════════════
# OUTPUT PATH
# ══════════════════════════════════════════════════════════════════════════


def get_output_pdf_path(md_path, meta):
    """Determine output PDF path.

    Convention:
    - If .md is in output/{subfolder}/, PDF goes to PDF/{subfolder}/
    - Otherwise, PDF goes alongside the .md file
    """
    topic = meta.get("topic", "untitled")
    today = datetime.now().strftime("%m%d%y")

    # Normalize topic for filename
    topic_file = (
        topic.lower()
        .replace(" ", "-")
        .replace("/", "-")
        .replace(":", "")
        .replace("?", "")
        .replace('"', "")
        .replace("|", "")
        .replace("<", "")
        .replace(">", "")
        .replace("*", "")
    )
    # Collapse consecutive hyphens (e.g. "a -- b" -> "a-b")
    while "--" in topic_file:
        topic_file = topic_file.replace("--", "-")

    filename = f"{today}-{topic_file}-lesson-plan.pdf"

    # Check if input is under output/
    try:
        parts = md_path.resolve().parts
        output_idx = parts.index("output")
        subfolder = parts[output_idx + 1]
        pdf_dir = PDF_OUTPUT_DIR / subfolder
    except (ValueError, IndexError):
        pdf_dir = md_path.parent

    pdf_dir.mkdir(parents=True, exist_ok=True)
    return pdf_dir / filename


# ══════════════════════════════════════════════════════════════════════════
# APPENDIX RESOLUTION
# ══════════════════════════════════════════════════════════════════════════


def resolve_appendix(path_str, base_dir):
    """Resolve an appendix file path relative to base_dir. Returns None if not found."""
    if not path_str or path_str == "none":
        return None
    p = Path(path_str)
    if not p.is_absolute():
        p = (base_dir / path_str).resolve()
    return p if p.exists() else None


def read_appendix_content(path):
    """Read a .typ appendix file, stripping page setup lines the template provides."""
    if not path or not path.exists() or path.suffix != ".typ":
        return None
    try:
        content = path.read_text(encoding="utf-8")
        # Strip set page / set text / set par commands (template provides these)
        content = re.sub(
            r"^#set\s+(page|text|par)\s*\([^)]*\)\s*(\n|$)+",
            "",
            content,
            flags=re.MULTILINE,
        )
        content = re.sub(
            r"^#show:\s*doc\s*=>\s*\{[^}]*\set\s+page[^}]*\}",
            "",
            content,
            flags=re.MULTILINE | re.DOTALL,
        )
        return content.strip()
    except Exception as e:
        print(f"  WARNING: Could not read {path.name}: {e}")
        return None


# ══════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════


def main():
    # Enable UTF-8 for console output
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    print("build_lesson_pdf.py — Markdown → Pandoc → Typst → PDF\n")

    verify_template()

    if len(sys.argv) < 2:
        print("Usage: python scripts/build_lesson_pdf.py <lesson.md>", file=sys.stderr)
        sys.exit(1)

    md_path = Path(sys.argv[1])
    if not md_path.exists():
        print(f"FATAL: File not found: {md_path}", file=sys.stderr)
        sys.exit(1)
    if md_path.suffix.lower() not in (".md", ".markdown"):
        print(f"FATAL: Input must be a .md file: {md_path}", file=sys.stderr)
        sys.exit(1)

    print(f"  Input: {md_path.name}")

    # ── Step 1: Parse & Validate Markdown ──
    meta, body = parse_frontmatter(md_path)
    print(f"  Topic: {meta.get('topic', '?')}")
    print(f"  Teacher: {meta.get('teacher', '?')}")
    stage_count = len(re.findall(r"^##\s+Stage\s+\d+:", body, re.MULTILINE))
    print(f"  Stages: {stage_count}")

    ok = lint_markdown(md_path)
    if not ok:
        print("\nFATAL: Markdown validation failed. Fix errors and retry.", file=sys.stderr)
        sys.exit(1)

    # ── Step 2: Determine output path ──
    output_pdf = get_output_pdf_path(md_path, meta)
    print(f"  Output: {output_pdf}")

    # ── Step 3: Pandoc → Typst ──
    print("  Running Pandoc...", end=" ")
    typst_source = pandoc_to_typst(md_path)
    print("OK")

    # ── Step 4: Append answer key and transcript ──
    ak_path_str = meta.get("answer_key", "")
    tr_path_str = meta.get("transcript", "")
    # Resolve paths from project root, not from .md file's directory
    ak_path = resolve_appendix(ak_path_str, PROJECT_ROOT)
    tr_path = resolve_appendix(tr_path_str, PROJECT_ROOT)

    if ak_path:
        ak_content = read_appendix_content(ak_path)
        if ak_content:
            typst_source += "\n\n= Answer Key\n\n" + ak_content
            print(f"  Answer key appended: {ak_path.name}")

    if tr_path:
        tr_content = read_appendix_content(tr_path)
        if tr_content:
            typst_source += "\n\n= Transcript\n\n" + tr_content
            print(f"  Transcript appended: {tr_path.name}")

    # ── Step 5: Typst → PDF ──
    print("  Running Typst compile...", end=" ")
    compile_typst(typst_source, output_pdf)
    file_size = output_pdf.stat().st_size
    print(f"OK ({file_size // 1024}KB)")

    # ── Step 6: Validate PDF content ──
    expected_texts = [
        meta.get("topic", ""),
        meta.get("teacher", ""),
        "Lesson Stages",
    ]
    pdf_warnings = lint_pdf(output_pdf, expected_texts)
    if pdf_warnings:
        for w in pdf_warnings:
            print(f"  PDF CHECK: {w}")
    else:
        print("  PDF linter: clean")

    print(f"\nDone. PDF: {output_pdf}")


if __name__ == "__main__":
    main()

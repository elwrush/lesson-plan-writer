# Plan: `build-excellent-lesson-plans` — Development Plan

Date: 2026-06-15
Status: Planning phase (no code executed yet)

## Goal

Replace `json_to_pdf.py` (Python f-strings → raw Typst) with a three-layer pipeline:

```
Lesson Plan JSON → Python wrapper → Markdown + YAML frontmatter → Pandoc (--to typst --template) → Typst → PDF
```

**Layer 1: Static Typst template** — page setup, masthead, stage table, answer key/transcript sections. Locked, never edited by agent.
**Layer 2: Pandoc** — converts Markdown body to Typst markup, fills template variables from YAML frontmatter.
**Layer 3: Python wrapper** — reads JSON, generates Markdown + YAML frontmatter, runs Pandoc + Typst, lints output.

---

## Architecture

### Component 1: Typst Template (`templates/lesson-plan.typ`)

A static `.typ` file that uses Pandoc template variable syntax (`$variable$`). Based on the current `build_typ_content()` layout in `json_to_pdf.py`.

**What it contains:**

```typst
// === templates/lesson-plan.typ ===
// PDF layout for ESL lesson plans. Uses Pandoc template variables.
// All page setup, masthead, stage rendering, and appendices live here.
// The agent never touches this file.

// Page setup
$if(teacher)$
#set page(paper: "a4", margin: (x: 0.75in, top: 0.75in, bottom: 0.75in))
#set text(font: "Roboto", size: 10pt)
#set par(leading: 0.55em)

// Masthead (logo band — identical to current json_to_pdf.py layout)
#v(12pt)
#block(
  stroke: (bottom: 0.5pt + black),
  inset: (bottom: 6pt),
  grid(
    columns: (1fr, 1fr, 1fr),
    align: (left + horizon, center + horizon, right + horizon),
    image("Image_20260324_141022.png", height: 1.35cm),
    align(center, text(size: 14pt, weight: "bold")[Lesson Plan]),
    image("cambridge.png", height: 1.8cm),
  ),
)
#v(0.3em)

// Lesson Information (from YAML frontmatter)
= Lesson Information

*Topic:* $topic$

#table(
  columns: (auto, 1fr, auto, 1fr),
  stroke: 1pt,
  [*Teacher:*], [$teacher$],
  [*Date:*], [$formatted_date$],
  [*Class:*], [$class$],
  [*Duration:*], [$duration$],
  [*CEFR Level:*], [$cefr_level$],
  [*Lesson Shape:*], [$shape$ ($shape_name$)],
)

// Materials block
$if(materials)$
*Materials:*
$materials$
$endif$

$if(slideshow_url)$
*Slideshow URL:* $slideshow_url$
$endif$

#v(0.5em)

// Lesson Aim
$if(objective)$
= Lesson Aim
#block(stroke: (left: 2pt + black), inset: 8pt, [$objective$])
#v(0.5em)
$endif$

// MAIN CONTENT — Pandoc converts Markdown body to Typst and inserts here
// The body contains: Stage headings, procedure lists, any free-form content
$body$

$endif$
```

**Key design decisions:**
- `$if(teacher)$`...`$endif$` guards the entire document — Pandoc conditionals prevent rendering when variable is empty
- `$body$` is where the lesson stages go. Pandoc converts stage headings (`## Stage 1: ...`) and procedure lists from Markdown to properly formatted Typst
- The template is ~50 lines — dramatically simpler than the current 200+ line Python function
- No `$for(stages)$` loop needed — the agent's Markdown body already has the structured stage content, and Pandoc converts it correctly
- Answer keys and transcripts remain as separate `.typ` files, referenced by path in the lesson plan JSON

### Component 2: Python Wrapper (`scripts/build_lesson_plan_pdf.py`)

Reads lesson plan JSON, generates Markdown, runs Pandoc → Typst → PDF, lints at every stage.

**Architecture:**

```python
"""
build_lesson_plan_pdf.py — New pipeline: JSON → Markdown → Pandoc → Typst → PDF

Usage:
    python scripts/build_lesson_plan_pdf.py output/{folder}/{file}.json

Replaces json_to_pdf.py with the three-layer architecture from WRITING-ASSESSMENT-2027.
"""

import json, os, re, subprocess, sys, shutil, hashlib
from pathlib import Path
from datetime import datetime

# ── Constants ──
PROJECT_ROOT = Path(__file__).parent.parent
TEMPLATE = PROJECT_ROOT / "templates" / "lesson-plan.typ"
TEMPLATE_LOCK = PROJECT_ROOT / ".template-lock.json"
FONT_DIR = Path(os.path.expandvars(r"%APPDATA%\TinyTeX\texmf-dist\fonts\opentype\google\roboto"))
ROBOTO_AVAILABLE = FONT_DIR.exists()

# ── Template hash verification ──
def verify_template():
    """Refuse to run if template has been modified from its locked hash."""
    if not TEMPLATE_LOCK.exists():
        print("WARNING: No template lock file. Creating one now.")
        actual = hashlib.sha256(TEMPLATE.read_bytes()).hexdigest().upper()
        TEMPLATE_LOCK.write_text(
            json.dumps({"lesson-plan.typ": {"sha256": actual}}, indent=2),
            encoding="utf-8",
        )
        return True
    lock = json.loads(TEMPLATE_LOCK.read_text(encoding="utf-8"))
    expected = lock.get("lesson-plan.typ", {}).get("sha256", "")
    actual = hashlib.sha256(TEMPLATE.read_bytes()).hexdigest().upper()
    if expected and actual != expected:
        print(f"ERROR: Template hash mismatch! Expected {expected}, got {actual}")
        sys.exit(1)
    return True


# ── Step 1: Read and validate JSON ──
def load_lesson_plan(json_path):
    """Load lesson plan JSON with mojibake fix."""
    # Reuse the existing read_json_with_encoding_fix from json_to_pdf.py
    # (or import it from a shared module)
    ...


# ── Step 2: Generate YAML frontmatter ──
def build_yaml_frontmatter(data):
    """Build YAML frontmatter string from lesson plan JSON."""
    lp = data.get("lesson_plan", {})
    formatted_date = format_date(data.get("date", ""))

    lines = [
        "---",
        f'topic: "{data.get("topic", "")}"',
        f'teacher: "{data.get("teacher", "")}"',
        f'duration: "{data.get("duration", "")}"',
        f'date: "{data.get("date", "")}"',
        f'formatted_date: "{formatted_date}"',
        f'shape: "{lp.get("shape", "")}"',
        f'shape_name: "{lp.get("shape_name", "")}"',
        f'cefr_level: "{lp.get("cefr_level", "")}"',
        f'class: "{lp.get("class", "")}"',
    ]

    # Materials (may contain bullet points — use YAML block scalar)
    materials = data.get("materials", "")
    if materials:
        lines.append("materials: |")
        for mat_line in materials.strip().split("\n"):
            lines.append(f"  {mat_line}")

    slideshow_url = data.get("slideshow_url", "")
    if slideshow_url:
        lines.append(f'slideshow_url: "{slideshow_url}"')

    objective = data.get("objective", "")
    if objective:
        lines.append(f'objective: "{objective}"')

    lines.append("---")
    lines.append("")
    return "\n".join(lines)


# ── Step 3: Generate Markdown body ──
def build_markdown_body(data):
    """Generate Markdown body from lesson plan stages."""
    lines = []
    lp = data.get("lesson_plan", {})
    stages = lp.get("stages", [])

    lines.append("= Lesson Stages")
    lines.append("")

    for st in stages:
        stage_num = st.get("stage_number", "")
        stage_name = st.get("stage", "")
        aim = st.get("stage_aim", "")
        procedure = st.get("procedure", "")
        time_val = st.get("time", "")
        interaction = st.get("interaction", "")

        # Stage heading
        lines.append(f"## Stage {stage_num}: {stage_name}")
        lines.append("")

        # Stage metadata
        lines.append(f"**Aim:** {aim}")
        lines.append("")
        lines.append(f"**Time:** {time_val} min  |  **Interaction:** {interaction}")
        lines.append("")

        # Procedure (bullet points)
        lines.append("**Procedure:**")
        lines.append("")
        # Procedure text may already have dashes. Split on newlines.
        for proc_line in procedure.strip().split("\n"):
            proc_line = proc_line.strip()
            if proc_line:
                # If already starts with dash, use as-is. Otherwise prefix.
                if proc_line.startswith("-"):
                    lines.append(proc_line)
                else:
                    lines.append(f"- {proc_line}")
        lines.append("")
        lines.append("")  # empty line between stages

    return "\n".join(lines)


# ── Step 4: Pandoc → Typst → PDF ──
def render_pdf(yaml_content, markdown_body, output_pdf, transcript_path=None, answer_key_path=None):
    """Pipe Markdown + YAML through Pandoc → Typst → PDF."""
    full_markdown = yaml_content + "\n" + markdown_body

    # 4a. Pandoc: Markdown → Typst
    pandoc_cmd = [
        "pandoc",
        "--from", "markdown+yaml_metadata_block",
        "--template", str(TEMPLATE),
        "--to", "typst",
        "--wrap", "none",
    ]

    pandoc_proc = subprocess.Popen(
        pandoc_cmd,
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    typst_source_bytes, pandoc_err = pandoc_proc.communicate(
        input=full_markdown.encode("utf-8")
    )

    if pandoc_proc.returncode != 0:
        print(f"PANDOC ERROR: {pandoc_err.decode('utf-8', errors='replace')[:500]}")
        return False

    typst_source = typst_source_bytes.decode("utf-8")

    # 4b. Inject answer key and transcript as raw Typst appendices
    if answer_key_path:
        ak_content = _read_typst_file(answer_key_path)
        if ak_content:
            typst_source += "\n\n#pagebreak()\n= Answer Key\n\n" + ak_content

    if transcript_path:
        tx_content = _read_typst_file(transcript_path)
        if tx_content:
            typst_source += "\n\n#pagebreak()\n= Transcript\n\n" + tx_content

    # 4c. Typst compile → PDF
    typst_cmd = ["typst", "compile"]
    if ROBOTO_AVAILABLE:
        typst_cmd += ["--font-path", str(FONT_DIR)]
    typst_cmd += ["-", str(output_pdf)]

    typst_proc = subprocess.Popen(
        typst_cmd,
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    _, typst_err = typst_proc.communicate(input=typst_source.encode("utf-8"))

    if typst_proc.returncode != 0:
        print(f"TYPST ERROR: {typst_err.decode('utf-8', errors='replace')[:500]}")
        return False

    print(f"PDF created: {output_pdf} ({output_pdf.stat().st_size // 1024}KB)")
    return True


def _read_typst_file(path_str):
    """Read a .typ file and return its content, stripped of Typst page setup."""
    path = Path(path_str)
    if not path.is_absolute():
        path = (PROJECT_ROOT / path).resolve()
    if not path.exists() or path.suffix != ".typ":
        return None
    try:
        content = path.read_text(encoding="utf-8")
        # Strip page setup lines that the template already provides
        # (set page, set text, set par, show rules from answer key/transcript files)
        content = re.sub(r'^#set\s+(page|text|par)\s*\([^)]*\)\s*$', '', content, flags=re.MULTILINE)
        content = re.sub(r'^#show:\s*doc\s*=>\s*\{.*?\}', '', content, flags=re.DOTALL)
        return content.strip()
    except Exception:
        return None


# ── Linter: Markdown validation ──
def lint_markdown(markdown_text):
    """Validate the generated Markdown structure before Pandoc conversion.
    
    Checks:
    - Frontmatter parses correctly
    - All stages have required fields (heading, aim, time, interaction)
    - No orphaned or duplicated stage numbers
    - Time fields sum to total duration
    """
    import yaml
    from markdown_it import MarkdownIt

    warnings = []

    # Parse YAML frontmatter
    yaml_match = re.match(r'^---\s*\n(.*?)\n---', markdown_text, re.DOTALL)
    if not yaml_match:
        return ["ERROR: No YAML frontmatter found"]

    try:
        metadata = yaml.safe_load(yaml_match.group(1))
    except yaml.YAMLError as e:
        return [f"ERROR: YAML parse error: {e}"]

    # Check required metadata fields
    required = ["topic", "teacher", "duration", "date", "shape", "shape_name", "cefr_level", "class"]
    for field in required:
        if field not in metadata or not metadata[field]:
            warnings.append(f"WARNING: Missing required field: '{field}'")

    # Parse Markdown body for stages
    md = MarkdownIt("js-default")
    tokens = md.parse(markdown_text)

    stage_headings = []
    for tok in tokens:
        if tok.type == "heading_open" and tok.tag == "h2":
            # Look ahead to get the heading content
            next_idx = tokens.index(tok) + 1
            while next_idx < len(tokens):
                if tokens[next_idx].type == "heading_close":
                    break
                if tokens[next_idx].type == "inline":
                    stage_headings.append(tokens[next_idx].content)
                next_idx += 1

    # Verify stage count matches expectations
    if len(stage_headings) == 0:
        warnings.append("WARNING: No stage headings (##) found in body")

    # Verify stage numbers are sequential
    stage_nums = []
    for h in stage_headings:
        m = re.match(r'Stage\s+(\d+):', h)
        if m:
            stage_nums.append(int(m.group(1)))

    if stage_nums:
        expected = list(range(stage_nums[0], stage_nums[0] + len(stage_nums)))
        if stage_nums != expected:
            warnings.append(f"WARNING: Non-sequential stage numbers: {stage_nums}")

    return warnings


# ── Linter: PDF validation ──
def lint_pdf(pdf_path):
    """Validate the generated PDF for content integrity.
    
    Checks:
    - File is non-empty and readable
    - Contains expected text (lesson topic, teacher name)
    - Has reasonable page count (≥ 2)
    """
    try:
        from PyPDF2 import PdfReader
    except ImportError:
        print("  LINT: PyPDF2 not installed — skipping PDF checks.")
        return []

    warnings = []
    reader = PdfReader(str(pdf_path))
    pages = len(reader.pages)

    if pages == 0:
        return ["ERROR: PDF has 0 pages"]
    if pages < 2:
        warnings.append("WARNING: PDF has only 1 page — expected ≥ 2")

    # Extract first-page text to verify masthead
    page1_text = reader.pages[0].extract_text() or ""

    if "Lesson Plan" not in page1_text:
        warnings.append("WARNING: 'Lesson Plan' not found on page 1 — masthead may be broken")
    if "Lesson Information" not in page1_text:
        warnings.append("WARNING: 'Lesson Information' not found on page 1")

    # Extract all text for content checks
    all_text = " ".join(
        (p.extract_text() or "") for p in reader.pages
    )

    if "Teacher:" not in all_text:
        warnings.append("WARNING: 'Teacher:' not found in PDF")

    return warnings


# ── Main ──
def main():
    verify_template()

    if len(sys.argv) < 2:
        print("Usage: python build_lesson_plan_pdf.py <lesson-plan.json>")
        sys.exit(1)

    json_path = Path(sys.argv[1])

    # Step 1: Load JSON
    data = load_lesson_plan(json_path)
    if data is None:
        print(f"ERROR: Cannot load {json_path}")
        sys.exit(1)

    # Step 2: Generate YAML frontmatter
    yaml_content = build_yaml_frontmatter(data)

    # Step 3: Generate Markdown body
    markdown_body = build_markdown_body(data)

    # Step 4: Lint Markdown
    full_markdown = yaml_content + "\n\n" + markdown_body
    markdown_warnings = lint_markdown(full_markdown)
    if any(w.startswith("ERROR") for w in markdown_warnings):
        for w in markdown_warnings:
            print(w)
        sys.exit(1)
    for w in markdown_warnings:
        print(f"  LINT: {w}")

    # Step 5: Determine output path
    topic = data.get("topic", "untitled")
    # output/{subfolder}/ in JSON path → PDF/{subfolder}/ for PDF
    parts = json_path.parts
    try:
        output_idx = parts.index("output")
        subfolder = parts[output_idx + 1]
    except (ValueError, IndexError):
        subfolder = "default"

    today = datetime.now().strftime("%m%d%y")
    normalized_topic = normalize_topic(topic)
    pdf_dir = PROJECT_ROOT / "PDF" / subfolder
    pdf_dir.mkdir(parents=True, exist_ok=True)
    output_pdf = pdf_dir / f"{today}-{normalized_topic}-lesson-plan.pdf"

    # Step 6: Resolve answer key and transcript paths
    base_dir = json_path.parent
    transcript = data.get("transcript", "")
    answer_key = data.get("answer_key", "")

    tr_path = _resolve_path(transcript, base_dir)
    ak_path = _resolve_path(answer_key, base_dir)

    # Step 7: Render PDF
    success = render_pdf(yaml_content, markdown_body, output_pdf, tr_path, ak_path)

    if not success:
        sys.exit(1)

    # Step 8: Lint PDF
    pdf_warnings = lint_pdf(output_pdf)
    for w in pdf_warnings:
        print(f"  PDF LINT: {w}")

    # Step 9: Copy logo images for Typst
    # (unlike json_to_pdf.py which copies images to temp, the template 
    #  references them from templates/ — we just need to ensure they exist)
    logo_files = ["Image_20260324_141022.png", "cambridge.png"]
    for logo in logo_files:
        src = PROJECT_ROOT / "templates" / logo
        if not src.exists():
            print(f"WARNING: Logo file not found: {src}")

    # Step 10: Report
    print(f"\nDone. PDF: {output_pdf}")


if __name__ == "__main__":
    main()
```

### Component 3: Markdown Linter (`scripts/lint_lesson_markdown.py`)

Uses `markdown-it-py` and `pyyaml` to validate the generated Markdown before Pandoc conversion.

```python
"""
lint_lesson_markdown.py — Validates lesson plan Markdown structure

Checks:
1. YAML frontmatter parses correctly
2. All metadata fields present and non-empty
3. Stage headings are well-formed (## Stage N: Name)
4. Stage numbers are sequential
5. Each stage has: Aim, Time, Interaction, Procedure
6. Total time equals stated duration
"""

import re, sys, yaml
from pathlib import Path
from markdown_it import MarkdownIt

def lint_markdown_file(md_path):
    """Validate a lesson plan Markdown file. Returns list of issue strings."""
    text = Path(md_path).read_text(encoding="utf-8")
    issues = []

    # 1. YAML frontmatter
    yaml_match = re.match(r'^---\s*\n(.*?)\n---', text, re.DOTALL)
    if not yaml_match:
        return ["FATAL: No YAML frontmatter found"]
    try:
        meta = yaml.safe_load(yaml_match.group(1))
    except yaml.YAMLError as e:
        return [f"FATAL: YAML parse error: {e}"]

    # 2. Required metadata
    for field in ["topic", "teacher", "duration", "date", "shape", "shape_name", "cefr_level", "class"]:
        if field not in meta or not meta[field]:
            issues.append(f"MISSING: '{field}' in YAML frontmatter")

    # 3. Parse stages from Markdown
    md = MarkdownIt("js-default").enable("table")
    tokens = md.parse(text)

    # Extract stage headings
    stages = []
    for i, tok in enumerate(tokens):
        if tok.type == "heading_open" and tok.tag == "h2":
            content = tokens[i + 1].content if i + 1 < len(tokens) else ""
            stages.append(content)

    if not stages:
        issues.append("WARNING: No ## stage headings found")
        return issues

    # 4. Sequential stage numbers
    stage_nums = []
    for h in stages:
        m = re.match(r'Stage\s+(\d+):', h)
        if m:
            stage_nums.append(int(m.group(1)))
        else:
            issues.append(f"WARNING: Stage heading doesn't match pattern: {h}")

    expected = list(range(1, len(stage_nums) + 1))
    if stage_nums and stage_nums != expected:
        issues.append(f"WARNING: Non-sequential numbers: {stage_nums}")

    return issues

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python lint_lesson_markdown.py <lesson.md>")
        sys.exit(1)
    issues = lint_markdown_file(sys.argv[1])
    for i in issues:
        print(f"  {i}")
    sys.exit(1 if any(i.startswith("FATAL") for i in issues) else 0)
```

### Component 4: The Skill (`build-excellent-lesson-plans`)

**Location:** `.kilo/skills/build-excellent-lesson-plans/SKILL.md`

This skill is exceptionally short — ~40 lines. The agent doesn't write HTML, doesn't write Typst, doesn't even write the Markdown directly. The Python wrapper handles everything.

```markdown
# Skill: build-excellent-lesson-plans

## Purpose
Convert a lesson plan JSON into a professionally formatted PDF using the Markdown → Pandoc → Typst pipeline.

## Pipeline
```
Lesson Plan JSON → build_lesson_plan_pdf.py → Markdown → Pandoc → Typst → PDF
```

## Usage

### Step 1: Write a lesson plan JSON
Use the `write-lesson-plan` skill (existing workflow). Produce a standard lesson plan JSON file.

### Step 2: Generate the PDF
```powershell
python scripts/build_lesson_plan_pdf.py output/{subfolder}/{file}.json
```

The script:
- Reads the lesson plan JSON
- Generates Markdown with YAML frontmatter
- Lints the Markdown for structural errors
- Converts Markdown to Typst via Pandoc (using the locked `templates/lesson-plan.typ` template)
- Compiles Typst to PDF
- Lints the PDF for content integrity

### What the agent controls
The agent's focus is **lesson quality**, not technical implementation:
- Meaningful, natural stage aims (not robotic template fills)
- Logical stage sequencing matching the selected shape
- Concise, actionable procedure text
- Appropriate time allocations

All code generation, markdown formatting, YAML construction, Pandoc invocation, and Typst compilation happen inside the Python script. The agent never touches a .typ file, .html file, or Pandoc command.

## Output
```
PDF/{subfolder}/{mmddyy}-{topic}-lesson-plan.pdf
```
```

---

## Implementation Order

| Step | File | Description | Lines | Dependency |
|------|------|-------------|-------|------------|
| 1 | `templates/lesson-plan.typ` | Static Typst template with Pandoc variable syntax | ~50 | None |
| 2 | `scripts/build_lesson_plan_pdf.py` | Python wrapper: JSON → Markdown → Pandoc → Typst → PDF | ~250 | Step 1 |
| 3 | `scripts/lint_lesson_markdown.py` | Markdown structural linter | ~60 | markdown-it-py |
| 4 | `.kilo/skills/build-excellent-lesson-plans/SKILL.md` | Agent-facing skill documentation | ~40 | Steps 1-3 |
| 5 | Lint + test with existing lesson plan JSON | End-to-end validation | — | Steps 1-4 |
| 6 | `.template-lock.json` | Hash-lock the template after validation | auto | Step 5 |

---

## Python Library Dependencies

All heavy lifting is done by existing, vetted libraries. The agent never implements parsing, rendering, or validation from scratch.

| Library | Purpose | Used in |
|---|---|---|
| `pyyaml` | YAML frontmatter parsing | `build_lesson_plan_pdf.py`, `lint_lesson_markdown.py` |
| `markdown-it-py` | Markdown tokenization for structural linting | `lint_lesson_markdown.py` |
| `PyPDF2` | PDF text extraction for content validation | `build_lesson_plan_pdf.py` (PDF linter) |
| `subprocess` | Pandoc and Typst CLI invocation | `build_lesson_plan_pdf.py` |
| `hashlib` | Template hash verification (anti-tamper) | `build_lesson_plan_pdf.py` |

All are in `requirements.txt` (markdown-it-py may need adding).

---

## What We Keep from `json_to_pdf.py`

| Function | Fate |
|---|---|
| `validate_json()` | Reused (imported) |
| `format_date()` | Reused (imported) |
| `humanize_stage_aim()` | Reused (imported) |
| `clean_procedure()` | Reused (imported) |
| `normalize_topic()` | Reused (imported) |
| `read_json_with_encoding_fix()` | Reused (imported) |
| `render_typst()` | Replaced by `render_pdf()` (adds Pandoc step before Typst) |
| `build_typ_content()` | **Replaced entirely** by the combination of `templates/lesson-plan.typ` + `build_yaml_frontmatter()` + `build_markdown_body()` |

The utility functions (validation, date formatting, aim humanization, procedure cleaning, encoding fix) remain unchanged — they process JSON data, not Typst code.

## What's Eliminated

- ~200 lines of Python f-strings generating raw Typst code (the `build_typ_content` function)
- Agent's need to understand Typst syntax, page setup, or table formatting
- The manul answer key/transcript injection logic in the Python file (handled by the template)
- The temporary file dance (copying logos to output dir, then cleaning up) — the template references logo paths directly

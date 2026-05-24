---
name: create-pdf-lesson-file
description: Converts a lesson plan JSON file to a formatted PDF using Typst CLI. Data is rendered into .typ markup by build_typ_content() in Python (no Jinja2), then compiled to PDF with typst compile.
---

# Skill: Create PDF Lesson File

## Purpose
Convert lesson plan JSON files to professionally formatted PDFs using Typst CLI with Roboto font, logo header, and structured lesson information.

## Workflow

### Step 1: Validate Input
- Check that the JSON file exists
- Parse and validate against required schema:
- **Auto-fix for mojibake**: `json_to_pdf.py` auto-detects and reconstructs UTF-8 characters corrupted by PowerShell encoding (em dashes, curly quotes, IPA symbols). The fix uses Latin-1 round-trip decoding. No manual intervention needed.
  - `teacher`, `duration`, `date`, `topic`, `materials`
  - `lesson_plan.shape`, `lesson_plan.shape_name`, `lesson_plan.cefr_level`, `lesson_plan.class`, `lesson_plan.stages`
  - Each stage must have: `stage_number`, `stage`, `stage_aim`, `procedure`, `time`, `interaction`
- Halt on first validation error with descriptive message

### Step 2: Process Content
- If `answer_key` is a file path, it must point to a `.typ` file (read raw — no conversion). `.md` files are NOT accepted — the markdown intermediary has been removed from the pipeline.
- If `transcript` is a file path, it must point to a `.typ` file. `.md`/`.txt` files are NOT accepted.
- Format date from `DDMMYY` or `YYMMDD` to `D Month, YYYY`
- Humanize robotic stage aims (e.g., "To reading for gist" → "To get the general idea of the text")
- Strip minute indicators from procedure text (e.g., "3 min.", "2 min.")

### Step 3: Build .typ Content
- Call `build_typ_content(data)` in `scripts/json_to_pdf.py` to generate .typ markup as a Python string (f-strings, no Jinja2)
- The generated .typ content produces:
  - Page 1 header with Cambridge and ACT logos, title "Lesson Plan"
  - Lesson Information: Topic line, then table (Teacher, Date, Class, Duration, CEFR, Shape, Materials, Slideshow URL)
  - Lesson Aim box with left border
  - Lesson Stages table (Time, Goal, Procedure, Interaction)
  - Answer Key and Transcript sections on page breaks

### Step 4: Render PDF with Typst
- Copy logo images to temp directory alongside the `.typ` file
- Run: `typst compile <temp.typ> <output.pdf> --font-path <roboto_dir>`
- Output path: `PDF/{input_subfolder}/{mmddyy}-{topic}-lesson-plan.pdf`
- Clean up temporary `.typ` file and copied images after rendering

### Step 5: Confirm Output
- Report success with output file path
- Report any errors with details

## File Locations
- **Script:** `C:\PROJECTS\LESSON PLAN WRITER 3\scripts\json_to_pdf.py` (contains `build_typ_content()` which generates .typ markup inline)
- **Reference template:** `C:\PROJECTS\LESSON PLAN WRITER 3\templates\lesson-plan-template.typ` (kept for reference, not used by pipeline)
- **Logos:** `C:\PROJECTS\LESSON PLAN WRITER 3\templates\Image_20260324_141022.png` (ACT), `cambridge.png` (Cambridge)
- **Roboto fonts:** `%APPDATA%\TinyTeX\texmf-dist\fonts\opentype\google\roboto\`
- **Output:** `C:\PROJECTS\LESSON PLAN WRITER 3\PDF\{subfolder}\{mmddyy}-{topic}-lesson-plan.pdf`

## Usage
```bash
python scripts/json_to_pdf.py <json_file_path> [--output-dir <dir>]
```

## Dependencies
- Python 3.x
- Typst CLI (v0.13+)
- Roboto OTF fonts (in TinyTeX or system)
- pytest (`pip install pytest`) for running tests

## Testing
Run tests with:
```bash
cd C:\PROJECTS\LESSON PLAN WRITER 3
python -m pytest tests/test_json_to_pdf.py -v
```

## Notes
- Black and white formatting only
- Logos appear only on page 1 header
- Roboto font used throughout
- Topic names normalized for filenames: lowercase, spaces to hyphens
- Date format in filename: mmddyy (no hyphens)
- Filename suffix: `-lesson-plan` (e.g. `051226-what-connects-us-lesson-plan.pdf`)
- Fails fast on any error - does not continue on validation failure

## Typst Syntax — Avoid Hallucination

**Typst evolves fast. Agent training data almost always predates the current release. Never guess or rely on training data for Typst syntax.**

When modifying `build_typ_content()` in `scripts/json_to_pdf.py` or debugging Typst compile errors, consult these sources in order:

1. **Remote Typst source code on GitHub** via `gh search code` or `gh api` — this is the only authoritative, up-to-date source:
   ```powershell
   gh search code "pub fn table" --repo typst/typst --limit 5
   gh api repos/typst/typst/contents/crates/typst-library/src/foundations/eval.rs
   ```
2. **Local `typst-author` skill docs** (`.kilo/skills/typst-author/docs/`) — bundled snapshot, useful offline but may be stale. Cross-reference against the remote repo.
3. **Local packed repo** (`knowledge-base/typst-packed.json`) — a repomix snapshot that predates this session. It is the **stale-est** source. Use only when offline.
4. **Never guess or rely on training data.** Every function call, parameter name, set rule, and show rule must be confirmed against one of the sources above.
5. **Follow read-edit-compile-check**: make a change, run `python scripts/json_to_pdf.py ...`, read errors, fix.

Key pitfalls:
- `#set par(leading: Xem)` is **additional** spacing, not a line-height multiplier
- `#set text(font: "Roboto")` requires `--font-path` pointing to actual OTF files
- `context { if counter(page).get().first() == 1 { ... } }` for conditional page-1 headers
- `table.cell(colspan: N)` merges N columns, consuming only one cell position in the row

## Answer Key File Format — CRITICAL

**Answer key files MUST use `.typ` extension. The pipeline does NOT accept `.md` files.** The `md_to_typst()` markdown intermediary was removed from `json_to_pdf.py` in May 2026. Any `.md` answer key will be silently ignored — the PDF will contain no answer key section.

The `write-lesson-plan` skill enforces this — even if the user asks for `.md`, the agent must write `.typ` instead.

### Answer Key Path Resolution

**Always use an absolute file path for the `answer_key` field in the lesson plan JSON** (e.g., `"answer_key": "C:\\PROJECTS\\LESSON-PLAN-WRITER-3\\inputs\\{subfolder}\\answer_key.typ"`). Relative paths like `"answer_key": "answer_key.typ"` are resolved from the project root directory, NOT from the JSON file's directory, and will silently fail — the PDF will contain no answer key section.

If relative paths are used, `json_to_pdf.py` now resolves them against the JSON file's parent directory (as of May 2026 fix), but for clarity and predictability, absolute paths are preferred.

### Answer Key Typst Syntax — Common Errors

Answer key `.typ` files contain `#table()` calls with column headers and data rows. The most common compile-error causes are:

1. **`#` inside bold markup** — `[*#*]` is INVALID because `#` starts a code expression inside any content block `[...]`. Always write `[*\#*]` instead. This applies to all `table.header[*#*]` calls.

2. **Missing curly braces in Unicode escapes** — the Typst `\\u{XXXX}` syntax (with curly braces) differs from Python/JavaScript `\\uXXXX`. Better yet, paste the actual Unicode character directly (em dash `—`, check `✓`, cross `✗`).

3. **Bold spanning word boundaries** — `*M*y` fails because Typst bold syntax requires word boundaries. Use `#strong[M]y` for mid-word bold.

**Checklist before writing any answer key `.typ` file:**
- [ ] All `[*#*]` in table headers changed to `[*\#*]`
- [ ] No markdown pipe tables (`| header |`) — use `#table()` only
- [ ] Unicode characters pasted directly, not as escape sequences
- [ ] Cross-check all three Typst Pitfall rules (#2 `#` escape, #1 mid-word bold, #6 Unicode escapes) in the section below

## Typst Pitfalls — Compile Errors and Fixes

### 1. Bold only works at word boundaries

`*bold*` syntax is Typst markup for strong emphasis, but it **only works when the enclosed text is surrounded by word boundaries** (spaces, punctuation, or line start/end). It does NOT work for bolding part of a word.

| Intended | Typst syntax | Result |
|----------|-------------|--------|
| Bold letter M in "My" | `*M*y` | ❌ Compile error: "unclosed delimiter" |
| Bold letter M in "My" | `#strong[M]y` | ✅ Renders bold M + "y" |

**Error pattern:** `*M*y`, `*N*elson`, `*I*n` — any `*X*y` where X is a single letter followed immediately by another letter.

**Fix:** Use `#strong[letter]word_rest` for mid-word bold. For whole words at word boundaries, `*bold*` works fine (e.g., `*I*` at word boundaries works, `*bold*` text works).

### 2. `#` character inside content blocks must be escaped

In Typst, `#` starts a code expression. Inside a content block `[...]`, `#` is still interpreted as starting code. To include a literal `#` inside a content block, escape it with `\#`.

| Intended | Typst syntax | Result |
|----------|-------------|--------|
| Bold # symbol in table header | `[*#*]` | ❌ Compile error: "expected expression" |
| Bold # symbol in table header | `[*\#*]` | ✅ Renders bold # |

**Error pattern:** Any `[*#*]`, `[#]`, or other `[...]` content blocks containing a bare `#`.

**Fix:** In answer key `.typ` files inside `#table(...)` calls, write `[*\#*]` instead of `[*#*]`.

### 3. Raw blocks (` ``` `) are markup, not function arguments

Triple backtick raw blocks exist ONLY in Typst **markup mode**. They cannot be used as arguments inside a function call.

| Intended | Typst syntax | Result |
|----------|-------------|--------|
| Raw block inside function | `#raw(lang: "none", ```...```)` | ❌ Compile error: "expected string, found content" |
| Raw block in markup | `` ```text ... ``` `` | ✅ Works |

**Error pattern:** `#raw(... , ``` ... ```)` — backticks inside function call arguments.

**Fix:** Use triple backticks directly in markup mode (no `#raw()` wrapper). Or pass a string to `#raw()`: `#raw("text")`.

### 4. `#raw()` takes a string, not content

When using `#raw()` as a function (e.g., inside a code block), it expects a **string** argument, not a content block. In markup mode, backticks create a raw block directly — no `#raw()` needed.

| Correct usage | Context |
|---------------|---------|
| `` ```text ... ``` `` | Markup mode (within content block or bare text) |
| `#raw("...")` | Code mode (inside function arguments, show rules) |

### 5. No markdown pipe tables — use Typst `#table()`

Markdown pipe table syntax (`| Header | Header |`) is NOT valid Typst. All tables in `.typ` files must use Typst's `#table()` function directly:
```typst
#table(
  columns: 3,
  table.header[*Header 1*][*Header 2*][*Header 3*],
  [Cell 1], [Cell 2], [Cell 3],
)
```

### 6. Unicode escapes require curly braces (`\u{NNNN}`, not `\uNNNN`)

Typst uses `\u{NNNN}` syntax for Unicode escape sequences — with **curly braces** around the hex value. Without braces, the escape is NOT recognized and the literal text `uNNNN` appears in the output.

| Intended character | Correct Typst | Wrong (renders as text) |
|---|---|---|
| Em dash `—` (U+2014) | `\u{2014}` or paste `—` directly | `\u2014` → shows `u2014` |
| Ellipsis `…` (U+2026) | `\u{2026}` or paste `…` directly | `\u2026` → shows `u2026` |
| Smiley `😀` (U+1F600) | `\u{1f600}` or paste `😀` directly | `\u1f600` → compile error |

**Root cause:** The `\uNNNN` syntax (without braces) comes from Python, JavaScript, and Markdown. When answer keys are converted from `.md` to `.typ`, these escapes are copied verbatim and do NOT work in Typst.

**Best practice:** Paste the actual Unicode character directly (em dash `—`, ellipsis `…`, etc.) instead of using escape sequences. This avoids the issue entirely and is more readable. Typst has first-class Unicode support — all UTF-8 characters work in content mode without escaping.

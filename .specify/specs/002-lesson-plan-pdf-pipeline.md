# Feature: Lesson Plan PDF Pipeline

## Feature Summary

Generate professional lesson plan PDFs from Markdown using the three-layer Markdown → Pandoc → Typst → PDF pipeline. The agent writes a single `.md` file with YAML frontmatter (topic, teacher, date, CEFR level, stage details). A Lua filter converts stage headings to a Typst table. `build_lesson_pdf.py` orchestrates: frontmatter validation, Pandoc invocation, Typst compilation, and output linting.

## User Scenarios

### User Story 1 — Build PDF from lesson.md (P1)
Run `python scripts/build_lesson_pdf.py output/subfolder/lesson.md` → validates frontmatter, runs Pandoc with Lua filter to generate `.typ`, runs Typst to compile `.pdf`, lint checks output.

**Why this priority:** Core output format for the lesson plan workflow.

### User Story 2 — Template integrity (P2)
Template `.typ` file is hash-verified via `.template-lock.json`. Any modification (even whitespace) produces a hash mismatch warning. Changes require explicit lock file update.

**Why this priority:** Agents sometimes edit template files; hash lock prevents silent drift.

### User Story 3 — PDF content is verifiable after build (P1)
After any `build_lesson_pdf.py` run, the output PDF must be machine-readable. Extracted text is checked against expected content from the lesson plan source. Missing or silently-dropped content (e.g. vocabulary lists, stage aims) produces a build warning or failure.

**Why this priority:** Lua filters can silently drop paragraphs (paragraphs not matching `Time:` or `Aim:` patterns vanish with no error). Without post-build text extraction, agents cannot detect content loss.

### User Story 4 — Cross-platform path resolution (P1)
Build scripts must resolve `%USERPROFILE%`, `%APPDATA%`, `%LOCALAPPDATA%` with fallback to `$HOME` or `/usr/share/fonts` on Linux. No hardcoded Windows-only paths.

**Why this priority:** The agent runs on Linux; the build must work identically on Windows and Linux without environment-specific edits.

## Technical Approach

`build_lesson_pdf.py` reads a Markdown file with YAML frontmatter, validates REQUIRED_META keys (eventually via `LessonPlan.model_validate()`), pipes through Pandoc with `lesson-tables.lua` to convert stage sections to Typst table syntax, compiles the Typst via CLI, and lints the PDF for structural issues.

After compilation, the PDF text is extracted via PyPDF2 or PyMuPDF and checked for content presence. This catches cases where the Lua filter silently drops paragraphs (non-`Time:`/`Aim:` `Para` blocks).

Files: `scripts/build_lesson_pdf.py`, `templates/lesson-plan.typ` (hash-locked), `scripts/lesson-tables.lua`, `.template-lock.json`.

## Validation Rules

| Module | Check | Rule |
|--------|-------|------|
| Frontmatter | REQUIRED_META keys | All present, non-empty |
| Frontmatter | shape_name duplication | `shape_name` must not contain `shape` as a substring (template renders `$shape$ ($shape_name$)` — nested repetition produces "Receptive Skills (Receptive Skills)") |
| Template | Slideshow URL row always present | The Slideshow URL row in `templates/lesson-plan.typ` must NOT be wrapped in `$if(slideshow_url)$ ... $endif$`. The row renders unconditionally with an empty gray-shaded cell. The cell content is `$if(slideshow_url)$$slideshow_url$$endif$` so the value only appears after deployment. |
| Template | .template-lock.json hash | SHA256 matches current file |
| Pandoc | Compilation | Exit code 0 |
| Pandoc | Para capture | All `Para` blocks in stage sections are captured — no silent drops for non-`Time:`/non-`Aim:` text |
| Typst | Compilation | Exit code 0 |
| Output | Lint (PyPDF2) | Page count, expected text, no forbidden text |
| Output | Vocab rendering | If `**Vocabulary:**` is present in lesson.md body, each listed word must appear in extracted PDF text |
| Output | Stage aims | Each stage aim phrase must appear in extracted PDF text |
| Cross-platform | Template path | `%USERPROFILE%` → `$HOME` fallback; `%APPDATA%` → `/usr/share/fonts` fallback |
| Cross-platform | Font path | Must resolve on both Windows (%APPDATA%/TinyTeX) and Linux (system fonts or explicit path) |

### Markdown structure rules (pre-build check)

| Check | Rule | Severity |
|-------|------|----------|
| Blank line before bullet list | A bullet list (`- item`) directly after a `**Heading:**` line without an intervening blank line will be parsed as a single paragraph with hyphens, not as a list. Every line beginning `- ` must be preceded by a blank line when it follows a `Para`. | ERROR |
| Stage heading format | Must match `^## Stage \\d+: .+$` | ERROR |
| Procedure has content | Every stage must have at least one bullet point in procedure | WARNING |
| Timing sums | Sum of stage `**Time:**` values must match `duration` in YAML frontmatter | WARNING |

## Test Coverage

`tests/test_build_lesson_pdf.py`: Frontmatter parsing, markdown linting, Pandoc/Typst integration test. (Some tests require Pandoc/Typst on PATH.)

Additional tests required:
- `tests/test_lesson_tables_lua.py`: Verify all `Para` types in stage content are captured (Time, Aim, Vocabulary, Notes, etc.). Test with a `**Vocabulary:**` followed by a bullet list with blank line, and without blank line (expect error).
- `tests/test_pdf_content_extraction.py`: Build a known-good lesson.md, compile, extract PDF text, verify all expected strings appear (stage names, aims, vocab words).

## Acceptance Criteria

| ID | Criterion | Validation Method |
|----|-----------|-------------------|
| AC1 | Valid lesson.md produces .pdf | File exists, non-empty |
| AC2 | Missing frontmatter field rejected | SystemExit |
| AC3 | Modified template caught | Hash mismatch error |
| AC4 | PDF text contains expected stage names, aims, and vocab | PyPDF2 text extraction |
| AC5 | Non-Time/Aim Para in stage content appears in output | PyPDF2 text extraction |
| AC6 | Bullet list without preceding blank line produces ERROR | Pre-build markdown lint |
| AC7 | SHAPE Literal in model covers all shapes in skill doc | `src/models.py` vs skill shape reference audit |
| AC8 | Build succeeds on Linux without Windows env vars | Cross-platform path resolution test |

## Constraints

- Pandoc >= 3.1 required (Typst writer)
- Typst CLI >= 0.12 required
- Roboto OTF fonts in TinyTeX font directory or system fonts
- PyPDF2 or PyMuPDF required for post-build content verification
- `lesson-tables.lua` MUST capture all `Para` block types in stage sections — not just `Time:` and `Aim:`. Any `Para` that doesn't match known patterns must be inserted into the procedure list (not silently dropped).

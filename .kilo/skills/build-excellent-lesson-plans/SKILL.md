---
name: build-excellent-lesson-plans
description: Generate professional lesson plan PDFs from Markdown using the three-layer Markdown → Pandoc → Typst → PDF pipeline.
---

# Skill: build-excellent-lesson-plans

## Purpose
Generate professional lesson plan PDFs from Markdown using the three-layer Markdown → Pandoc → Typst → PDF pipeline.

## Pipeline
```
Agent writes lesson.md → build_lesson_pdf.py (validates + Pandoc + Lua filter + Typst + lint) → PDF
```

## Architecture

| Layer | What | Who writes |
|---|---|---|
| `templates/lesson-plan.typ` | Typst page setup, masthead, info table, aim block. `$body$` for content. | Developer, once, hash-locked |
| `scripts/lesson-tables.lua` | Pandoc Lua filter — reads `## Stage N:` headings from the body and generates a Typst `#table()` with colored headers. | Developer, once |
| `scripts/build_lesson_pdf.py` | Validates Markdown, runs Pandoc with template + Lua filter, compiles Typst, lints PDF, appends answer key/transcript if present. | Developer, once |
| `lesson.md` | YAML frontmatter (metadata) + Markdown body (stages, materials). **No Typst code, no HTML, no JSON.** | Agent, every lesson |

## Key conventions

- **Duration:** Standard lesson is 46 minutes. Total stage times must always match stated duration.
- **Stage numbering:** Sequential from 1. No gaps.
- **Output location:** Input `.md` in `output/{subfolder}/` → PDF in `PDF/{subfolder}/`.
- **Stages in Markdown body, not YAML.** YAML frontmatter is for simple metadata strings only. The Lua filter reads `## Stage N:` headings and builds the stage table.

## When to Use

Use this skill when:
- A teacher needs a professional lesson plan PDF generated from Markdown
- Stages need to be formatted as a colored table with timing and interaction columns
- Optional answer key or transcript appendices are needed

Do NOT use this skill when:
- Raw Typst output is needed (use `typst-author` skill instead)
- The lesson plan is already in a different format that needs conversion first

**Trigger:** `/build-excellent-lesson-plans` command or when the user asks to generate a lesson plan PDF.


## Workflow

### Step 1: Write a lesson plan in Markdown

Create a `.md` file in `output/{subfolder}/` with YAML frontmatter for metadata and Markdown body for stages.

**YAML frontmatter fields:**

```yaml
---
topic: "Gender Stereotypes and Gen Z"
teacher: "Ed Rush"
formatted_date: "15 June, 2026"
duration: "46 minutes"
cefr_level: "B2"
class: "M3"
shape: "G"
shape_name: "Task-Based Learning"
materials:
  - "BTN video (Episode 15)"
  - "YouTube clip: Andrew Tate (https://www.youtube.com/watch?v=...)"
  - "Slide deck"
slideshow_url: "https://elwrush.github.io/lesson-plan-writer/SUBFOLDER/index.html"
main_aim: "By the end of the lesson, learners will have..."
subsidiary_aim: "Learners will also have practiced..."
transcript: "output/.../transcript_tate.typ"
---

= Lesson Stages

## Stage 1: Stage Name

**Time:** 5 min  |  **Interaction:** T-Ss

**Aim:** Natural English aim description

- Bullet point each step
- Keep procedures concise
- No blank lines between bullet items

## Stage 2: Next Stage
...
```

**Optional YAML fields:**
- `transcript` — path to a `.typ` transcript file. If present, appended to the PDF after the stages.
- `answer_key` — path to a `.typ` answer key file. Only include when the lesson actually has an answer key. If absent, no answer key header appears.
- `slideshow_url` — URL of the lesson slideshow. Renders as a gray-shaded row in the info table. **Compute from git remote:** run `git remote get-url origin`, extract `{owner}` and `{repo}`, then use `https://{owner}.github.io/{repo}/{subfolder}/index.html` where `{subfolder}` matches the output directory name. Do NOT guess or hardcode. The `/git-pages` command also auto-updates this field after deployment for both JSON and Markdown lesson plan files.

**Stage aim style:** Write aims in natural English. Vary sentence openers. Avoid robotic templates like "To lead-in" or "To reading for gist".

**Procedure style:** One dash per action step. No blank lines between bullets. Keep concise — the teacher has the lesson plan, they don't need full exercise instructions reproduced.

### Step 2: Generate the PDF

```powershell
python scripts/build_lesson_pdf.py output/{subfolder}/lesson.md
```

This validates the Markdown, runs Pandoc with `templates/lesson-plan.typ` and `scripts/lesson-tables.lua`, compiles via Typst, appends any answer key or transcript, and lints the PDF.

Output: `PDF/{subfolder}/{mmddyy}-{topic}-lesson-plan.pdf`

### Step 3: Review

Open the PDF and check:
- Masthead (Cambridge logo · C·E·L Mathayom · ACT logo)
- Info table: teacher, date, class, duration, CEFR, shape, materials, slideshow URL (gray-shaded)
- Lesson aims with left accent bar (main aim bold, subsidiary aim bold)
- Stage table with colored headers (luma(230) fill) and four columns: Time, Goal, Procedure, Int
- Total timing matches duration
- Aims are natural English
- Bullet points render correctly throughout
## Examples

### Example 1: Full lesson with answer key

**Request:** "Generate lesson plan for Gender Stereotypes lesson"

**Action taken:** Write `output/m3-gender/lesson.md` with YAML frontmatter and stage Markdown, run `python scripts/build_lesson_pdf.py output/m3-gender/lesson.md`, append answer key from `answer-key.typ`.

**Output:** `PDF/m3-gender/lesson-plan.pdf`

### Example 2: Lesson with transcript appendix

**Request:** "Lesson plan with video transcript appended"

**Action taken:** Add `transcript: output/m3-gender/transcript.typ` to YAML frontmatter, run the build script.

**Output:** PDF with transcript appended after stages table.

### Example 3: Minimal no-frills lesson

**Request:** "Quick lesson plan, no extras"

**Action taken:** Write minimal YAML + stages, run build script without `transcript` or `answer_key` fields.

**Output:** Clean PDF with only the lesson plan content.



## Key principles

- **Agent writes Markdown** — no Typst, no HTML, no JSON. Pandoc + Lua filter handle the conversion.
- **Lua filter builds the table** — `scripts/lesson-tables.lua` scans `## Stage N:` headings and generates the Typst `#table()`. No YAML `stages` arrays needed.
- **Template is locked** — `templates/lesson-plan.typ` is hash-verified. Changes require deleting `.template-lock.json`.
- **Optional appendices** — answer key and transcript are only appended when the corresponding YAML field is present. Headers appear inline, not on separate pages.
- **No inline `python -c`** — all operations use permanent `.py` files in `scripts/`.

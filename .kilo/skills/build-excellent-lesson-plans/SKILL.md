---
name: build-excellent-lesson-plans
description: Generate professional lesson plan PDFs from Markdown using the three-layer Markdown → Pandoc → Typst → PDF pipeline.
license: MIT
metadata: author=Ed Rush (C·E·L Mathayom / ACT)
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
- **Stage table columns:** The Lua filter (`lesson-tables.lua`) generates a 5-column table: Time | Stage | Goal | Procedure | Int. The narrow "Stage" column between Time and Goal shows the stage number (1, 2, 3…) for quick visual reference. Headers are bold; stage name rows have a light gray (`luma(230)`) background spanning all 5 columns.
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

The workflow asks exactly **one question per turn**. Questions alternate between two input methods:

| Input method | When to use | How |
|---|---|---|
| **`question` tool with predefined options** | Only for fields with a known closed set: shape (A–G) and CEFR level (A1–C2) | Call `question` with `options` array. User clicks an option to select. |
| **Chat message** | All other fields: teacher, duration, topic, class, materials, subfolder name, answer key path, transcript path | Write the question directly in your response text. The user types the answer in the normal message input. |

**Critical rules:**
- If using the `question` tool and the user types a custom answer (rather than picking a predefined option), **use their answer literally**. Do NOT map it back to one of the predefined options.
- Never use the `question` tool for anything other than shape or CEFR level.
- After each answer, do a brief visible action (read a file, confirm the value) before asking the next question.

### Step 1: Greet the User
```
Welcome to the Lesson Plan Writer!
I'll help you create a structured lesson plan.
```

### Step 2: Read Creative Techniques

Read `references/CREATIVE_TECHNIQUES.md` before picking a shape. Ask the 7 questions from that document — the objective and creative approach should choose the shape, not the other way around.

### Step 3: Shape (question tool with options)
Display the shapes in your response text, then call `question` with options A–G:

| Shape | Name |
|-------|------|
| A | Text-based Presentation of Language |
| B | Language Practice |
| C | Test-Teach-Test |
| D | Situational Presentation (PPP) |
| E | Receptive Skills (Traditional) |
| F | Productive Skills (Traditional) |
| G | Task-Based Learning/TBL |

After the user answers, read the corresponding shape template from `knowledge-base/lesson plan shapes/json/shape-{letter}.json`. Report back: "Loaded Shape {letter} — {shape name}." Use the template's stage structure, `main_aim_format`, and `pedagogical_justification` to guide the stage design.

### Step 3: Teacher name (chat)
Default: "Ed Rush". Confirm with the teacher: "Teacher name: Ed Rush — is that still correct?" If they say no, ask for the new name.

### Step 4: Lesson length (chat)
Default: 46 minutes. Confirm with the teacher: "Lesson length: 46 minutes — is that still correct?" If they say no, ask for the new duration.

### Step 5: CEFR level (question tool with options)
Call `question` with options: A1, A2, B1, B2, C1, C2. Each with appropriate description.

### Step 6: Topic (chat)
Write: "What's the lesson topic?" in your response text. Wait for the user's chat reply.

### Step 7: Class (chat)
Write: "What's the class name or identifier?" in your response text. Wait for the user's chat reply.

### Step 8: Materials (chat)
Write: "What materials will you use? (e.g., coursebook unit and pages, video links, handouts)" in your response text. Wait for the user's chat reply.

### Step 9: Output subfolder (chat)
Write: "What subfolder should I use under `output/`?" in your response text. Wait for the user's chat reply.

After receiving the name:
1. Check if `output/{subfolder}/` exists. If not, create it.
2. List the folder contents.
3. Scan for any existing materials files, answer keys, or transcripts.

### Step 10: Resolve answer key and transcript (chat only)
Only ask if not already present in the subfolder:
- "Do you have an answer key? If so, what path?"
- "Do you have a transcript? If so, what path?"

### Step 11: Write the lesson plan

Create `output/{subfolder}/lesson.md` with:

**YAML frontmatter:**

```yaml
---
topic: "[User-provided topic]"
teacher: "[User-provided name]"
formatted_date: "[Today's date, e.g. 21 June, 2026]"
duration: "[Duration]"
cefr_level: "[CEFR level]"
class: "[Class]"
shape: "[Shape letter]"
shape_name: "[Shape name]"
materials:
  - "Material 1"
  - "Material 2"
main_aim: "By the end of the lesson, learners will have..."
subsidiary_aim: "Learners will also have practiced..."
---
```

Optional YAML fields (only include if provided):
- `transcript: "output/{subfolder}/transcript.typ"` — path to transcript file
- `answer_key: "output/{subfolder}/answer-key.typ"` — path to answer key file
- `slideshow_url` — computed from git remote after slideshow deployment (not during initial lesson plan creation)

**Body format:**

```
= Lesson Stages

## Stage 1: Stage Name

**Time:** 5 min  |  **Interaction:** T-Ss

**Aim:** Natural English aim description (see writing style below)

- Bullet point each step
- Keep procedures concise
- No blank lines between bullet items

## Stage 2: Next Stage
...
```

Use the shape template's stage structure from Step 2 as a guide for the number and type of stages, but write original stage names, aims, and procedures specific to the user's topic and materials.

**Stage aim style:** Write aims in natural English. Vary sentence openers. Avoid robotic templates like "To lead-in" or "To reading for gist".

**Procedure style:** One dash per action step. No blank lines between bullets. Keep concise — the teacher has the lesson plan, they don't need full exercise instructions reproduced.

### Step 12: Generate the PDF

```powershell
python scripts/build_lesson_pdf.py output/{subfolder}/lesson.md
```

This validates the Markdown, runs Pandoc with `templates/lesson-plan.typ` and `scripts/lesson-tables.lua`, compiles via Typst, appends any answer key or transcript, and lints the PDF.

Output: `PDF/{subfolder}/{mmddyy}-{topic}-lesson-plan.pdf`

### Step 13: Review

Open the PDF and check:
- Masthead (Cambridge logo · C·E·L Mathayom · ACT logo)
- Info table: teacher, date, class, duration, CEFR, shape, materials, slideshow URL (gray-shaded)
- Lesson aims with left accent bar (main aim bold, subsidiary aim bold)
- Stage table with colored headers (luma(230) fill) and four columns: Time, Goal, Procedure, Int
- Total timing matches duration
- Aims are natural English
- Bullet points render correctly throughout

### Step 14: Confirm
Inform the user where the PDF was saved.

## Writing Style

### Stage Aim Quality

Stage aims must be written in natural, idiomatic English — never in the deterministic style of a template. Vary phrasing across stages.

**UNACCEPTABLE (robotic/deterministic)**:
- "To lead-in to the topic of..."
- "To reading for gist"
- "To reading for detail and specific information"
- "To post-reading speaking task"
- "To wrap-up and reflection"

**ACCEPTABLE (natural/probabilistic)**:
- "To activate learners' interest in the theme of..."
- "To get the general idea of the text"
- "To identify key facts and supporting details"
- "To discuss ideas from the reading and share personal responses"
- "To reflect on key takeaways and consolidate learning"

### Writing Principles

1. **Vary sentence openers** — do not start every aim with "To" followed by a verbatim stage name
2. **Use natural collocations** — e.g., "get the gist", "activate interest", "draw out", "build on", "set the scene"
3. **Write aims as meaningful teaching intentions** — not mechanical labels
4. **Adapt language to CEFR level** — simpler phrasing for A1/A2, more sophisticated for B2/C1

## Shape Templates

Lesson plan shape templates are stored at:
```
knowledge-base/lesson plan shapes/json/
```

Available templates:
- `shape-a.json` — Text-based Presentation of Language
- `shape-b.json` — Language Practice
- `shape-c.json` — Test-Teach-Test
- `shape-d.json` — Situational Presentation (PPP)
- `shape-e.json` — Receptive Skills (Traditional)
- `shape-f.json` — Productive Skills (Traditional)
- `shape-g.json` — Task-Based Learning/TBL

Each contains stage structure, `main_aim_format`, and `pedagogical_justification` to guide lesson design.

## Key principles

- **Agent writes Markdown** — no Typst, no HTML, no JSON. Pandoc + Lua filter handle the conversion.
- **Lua filter builds the table** — `scripts/lesson-tables.lua` scans `## Stage N:` headings and generates the Typst `#table()`. No YAML `stages` arrays needed.
- **Template is locked** — `templates/lesson-plan.typ` is hash-verified. Changes require deleting `.template-lock.json`.
- **Optional appendices** — answer key and transcript are only appended when the corresponding YAML field is present. Headers appear inline, not on separate pages.
- **No inline `python -c`** — all operations use permanent `.py` files in `scripts/`.

## Examples

### Example 1: Receptive skills listening lesson

**Request:** "Create a lesson plan for the M3 listening lesson based on the transcript."

**Action taken:** Greeted user, loaded shape E (Receptive Skills), collected metadata (teacher, duration, CEFR, topic, class, materials, subfolder). Wrote `output/{subfolder}/lesson.md` with YAML frontmatter and body stages matching shape E. Ran `python scripts/build_lesson_pdf.py output/{subfolder}/lesson.md` to generate PDF. Verified masthead, info table, aim block, and stage table matched the template.

**Output:** `PDF/M3_Lesson01_Listening/050726-listening-lesson-plan.pdf`

### Example 2: Productive skills with answer key appendix

**Request:** "Lesson plan for M2 writing CA feedback — 46 min, B1."

**Action taken:** Loaded shape F (Productive Skills). Collected metadata. Wrote lesson.md with writing CA feedback stage structure. Added `answer_key: "output/{subfolder}/answer-key.typ"` to YAML frontmatter. Ran build script which appended the answer key as an appendix section. Verified PDF included both lesson stages and appendix.

**Output:** `PDF/M2-WRITING-CA-FEEDBACK/050726-ca-feedback-lesson-plan.pdf`

---

## Error Handling

| Symptom | Likely cause | Fix |
|---------|-------------|-----|
| `build_lesson_pdf.py` exits with code 1 | Markdown validation failed (missing frontmatter, stage headings) | Check `lesson.md` for required YAML fields and `## Stage N:` heading format |
| Typst compilation fails with "unknown font family" | Font path not set or Roboto not installed | Verify TinyTeX Roboto OTFs in `--font-path` |
| Stage table renders with wrong column headers | Stage headings use wrong format | Ensure headings match `## Stage N:` exactly (with colon) |
| Output PDF is empty or missing body | Pandoc or Typst pipeline error | Run `build_lesson_pdf.py --verbose` to see intermediate output |
| "Template hash mismatch" error | `templates/lesson-plan.typ` was modified | Delete `.template-lock.json` and re-run, or restore original template |

---

## Reference

The build pipeline uses these files:

- `templates/lesson-plan.typ` — Typst page setup, masthead, info table, aim block
- `scripts/lesson-tables.lua` — Pandoc Lua filter that reads `## Stage N:` headings and generates Typst `#table()` with colored headers
- `scripts/table-align.lua` — Pandoc Lua filter that catches `Table` AST elements and replaces `align(center)` with `align(left)` before the Typst writer runs
- `scripts/pagebreak.lua` — Pandoc Lua filter that converts `---` to `#pagebreak()` in Typst output and adds a pagebreak before the appendix header
- `scripts/build_lesson_pdf.py` — Entry point: validates Markdown, runs Pandoc + Lua filter, compiles Typst, lints PDF
- `knowledge-base/lesson plan shapes/json/shape-{letter}.json` — Shape templates defining stage structure per lesson type
- `references/CREATIVE_TECHNIQUES.md` — Creative techniques to explore BEFORE picking a shape (problem-first, comparative input, persona-based, drama, McKinsey-style)

See also `.kilo/skills/build-excellent-lesson-plans/SKILL.md` (this document) for full workflow details.

## Scripts

- `scripts/build_lesson_pdf.py` — Main build script: validates markdown, runs Pandoc → Typst pipeline, lints output PDF, appends answer key/transcript
- `scripts/lesson-tables.lua` — Pandoc Lua filter for stage table generation
- `scripts/table-align.lua` — Pandoc Lua filter that replaces `align(center)` with `align(left)` for all pipe tables in Typst output
- `scripts/pagebreak.lua` — Pandoc Lua filter: converts `---` to `#pagebreak()`, ensures appendix starts on a new page
- `scripts/linter_pdf_content.py` — Post-build PDF content linting


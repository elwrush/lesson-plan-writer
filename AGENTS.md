# AGENTS.md — Lesson Plan Writer 3

## Environment

- **OS:** Windows AMD64 (win32 sys.platform)
- **Shell:** PowerShell
- **Python:** 3.x
- **PowerShell quoting trap:** Inline `python -c "..."` with complex quoting (regex, nested quotes, f-strings with backslashes) ALWAYS hits PowerShell escaping issues. **Never use inline `python -c` for complex code.** Instead: write the Python script to `C:\Users\elwru\AppData\Local\Temp\kilo\*.py` via the Write tool, then execute via `python "C:\Users\elwru\AppData\Local\Temp\kilo\*.py"`. This avoids all quoting problems.

## Golden Rule: Pattern-first, not guess-first

Before writing any HTML, CSS, Typst, slide markup, or configuration, **read the template or an existing file that already does what you need**. The correct pattern is always in the codebase already — guessing or generating from training data wastes time and causes errors. Specifically:
- Slide attributes: check `templates/base-slides-template.html` for the exact attribute pattern
- Typst syntax: check `.kilo/skills/create-pdf-lesson-file/SKILL.md` (Typst Pitfalls section)
- Slide structure: check the most recently built `output/*/slides/index.html`
- Reveal.js bugs: check `docs/revealjs-known-issues.md` before debugging audio, fragment, or plugin issues

## Two pipelines

### PDF (2-stage)
1. **`write-lesson-plan` skill** → `output/{subfolder}/{mmddyy}-{topic}-lesson-plan.json`
2. **`create-pdf-lesson-file` skill** → converts JSON → `PDF/{subfolder}/{mmddyy}-{topic}-lesson-plan.pdf`

### Slides (template-based)
1. **`write-lesson-plan` skill** → JSON (same as above)
2. **`lesson-plan-to-reveal` skill** → copies `templates/base-slides-template.html` → hand-builds `index.html` with raw HTML `<section>` elements in `output/{subfolder}/slides/`
3. **`/git-pages` command** (or `publish-to-github-pages` skill in `.kilo/skills/`) → deploys all slideshows in `output/` to gh-pages

**Markdown pipeline is permanently abandoned.** All slides are raw HTML `<section>` elements. `scripts/json_to_markdown.py` is deprecated — do not use for new presentations. Auto-animate requires sibling `<section data-auto-animate>` elements, which cannot be produced from the markdown plugin.

## Key commands

```bash
# Kilo CLI commands
# /git-backup — Stage all, auto-generate commit message, commit+push to main
# /git-pages — Deploy slides subfolder to gh-pages with landing page
# /lint — Run ruff check --fix and ruff format

# PDF (from project root)
python scripts/json_to_pdf.py output/<subfolder>/<file>.json

# Slides — copy base template + hand-build sections
cp "templates/base-slides-template.html" "output/<subfolder>/slides/index.html"

# Slide validation (runs 66 reveal.js rule checks)
npx revealjs-validator --project "output/<subfolder>/slides/"
# Then open index.html in browser + check console (F12) for errors

# Pixabay image download (for slide backgrounds)
python scripts/pixabay_download.py --query "topic" --type image --count 3

# Tests (56 total, all pass)
python -m pytest tests/ -v
python -m pytest tests/test_json_to_pdf.py -v          # 18 tests
python -m pytest tests/test_json_to_markdown.py -v      # 26 tests
python -m pytest tests/test_git_pages_safety.py -v      # 12 tests — red-green safety guard for /git-pages

# Locate slide by reveal.js index (deterministic editing)
python scripts/locate_slide.py "file:///path/to/index.html#/7"
python scripts/locate_slide.py 7 --slides-dir path/to/slides/
```

## Linting & Quality

ruff is installed globally via pip. **Pre-commit hook is permanently uninstalled** (caused git lock contention). Use the `/lint` command instead — it runs encoding checks, then ruff on demand with no background processes.

**Windows UTF-8 trap:** Python on Windows defaults to cp1252 for file I/O and console output. Always use `encoding="utf-8"` when opening project files (`open(path, "r", encoding="utf-8")`). For scripts that print Unicode to the console, add:
```python
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
```
The `check_encoding.py` script (run as part of `/lint`) scans all text files for encoding issues and fixes cp1252→UTF-8.

To avoid cp1252 issues in interactive Python sessions, set `$env:PYTHONUTF8=1` in PowerShell before running Python commands that handle project files. This makes Python default to UTF-8 for all file I/O on Windows.

```bash
# Lint + fix (all files) — replaces pre-commit hook
python -m ruff check --fix .

# Format all Python files
python -m ruff format .

# Both in sequence
python -m ruff check --fix . ; python -m ruff format .

# Run pre-commit checks on all files (without hook, without committing)
python -m pre_commit run --all-files
```

A lint command is defined at `.kilo/command/lint.md` — invoke via Kilo CLI.

## JSON schema

- Top-level: `teacher`, `duration`, `date` (DDMMYY), `topic`, `materials`, `lesson_plan`
- `lesson_plan` keys: `shape`, `shape_name`, `cefr_level`, `class`, `stages[]`
- Each stage: `stage_number`, `stage`, `stage_aim`, `procedure`, `time`, `interaction`
- Optional top-level: `transcript`, `answer_key`, `cefr_level`, `class`, `objective`
- `answer_key` value: `"none"`, or a file path to `.typ` markup (`.md` files are NOT accepted — the markdown intermediary was removed)
- **`lesson_plan` and `answer_key` use underscore** (not hyphen). The test fixture has a bug — uses `answer-key` — ignore it; production JSON always uses `answer_key`.
- Shape templates (A–G) at `knowledge-base/lesson plan shapes/json/shape-{letter}.json`

## PDF rendering (Typst)

- Renderer: `typst compile` (NOT Quarto — abandoned, it ignored `format: typst`)
- Template: `.typ` content generated by `build_typ_content()` in `scripts/json_to_pdf.py` (Python f-strings, compiled with `typst compile`)
- Font: Roboto OTF from `%APPDATA%\TinyTeX\texmf-dist\fonts\opentype\google\roboto\` via `--font-path`
- Logos: `templates/Image_20260324_141022.png` (ACT), `templates/cambridge.png` (Cambridge) — page-1 content only, not a page header
- Logo band is rendered as page-1 content (a `#block` + `#grid`), not as a page header. Margins are uniform at 0.75in.
- Line spacing: `#set par(leading: 0.55em)` — leading is **additional** space, not a multiplier

## Typst Error Reference

When Typst compilation fails, the most common causes are documented in the `create-pdf-lesson-file` skill at: `.kilo/skills/create-pdf-lesson-file/SKILL.md` (section: **Typst Pitfalls — Compile Errors and Fixes**).

Five known error patterns covered:
1. **Bold only at word boundaries** — `*M*y` fails; use `#strong[M]y`
2. **`#` inside content blocks** — `[*#*]` fails; use `[*\#*]`
3. **Raw blocks are markup, not function arguments** — `#raw(```)``` invalid; use `` ``` `` directly
4. **`#raw()` takes a string** — no backtick syntax inside function calls
5. **No markdown pipe tables** — use `#table(columns: N, ...)` instead

**Before modifying any `.typ` file or `json_to_pdf.py`, read the Categorised Typst Pitfalls section in that skill first.** Do not guess Typst syntax from training data.

## Content transforms (in json_to_pdf.py build_typ_content)

- Date: `050726` → `7 May, 2026`
- Stage aims: robotic templates humanized (e.g. "To reading for gist" → "To understand the general idea of the text")
- Procedure: minute indicators stripped (`3 min.` → ``)
- Windows paths: `\` → `/` for Typst

## Language quality

Stage aims must read as natural English, not template fills. Unacceptable:
- "To lead-in to the topic of..."
- "To reading for gist"
- "To post-reading speaking task"

Acceptable: "To activate interest in...", "To get the general idea of the text", "To discuss ideas from the reading"

## Slide design reference

`docs/slide-design-reference.md` defines slide types (vocabulary, task, answer, transition), fragment policy, auto-animate rules, and Pixabay image strategy. The `json_to_markdown.py` script reads this doc at generation time.

### V1 Slide Flow (Actual)

```
SLIDESHOW FLOW — index2.html
────────────────────────────────────────────
 0  Title (Pixabay background, CEFR badge)
 1  Objective (4 bullets)
 2  Lead-in (Pixabay bg, discussion Q)
 3  Vocab 1 (generation gap) — h2 on first only
 4  Vocab 2 (frustration)
 5  Vocab 3 (redefine)
 6  Vocab 4 (workplace)
  7  Transition → What's the main idea? (red bg)
  8  Transition → Finding details (red bg)
  ─────── T/F Strategy Block (4 steps) ───────
  9  T/F Header + Step 1 + tip text
 10  T/F Step 2 (sub-questions + rule)
 11  T/F Step 3 (evidence + keywords)
 12  T/F Step 4 (answer with paragraph quotes)
 13  Exercise 2 Timer (60s)
 14  Exercise 2 Answers (answer-table, tick/cross, Why column)
  ─────── Paragraph Matching Block (4 steps) ───────
 15  Transition → Matching ideas (red bg)
 16  Para Matching Header + Step 1
 17  Para Matching Step 2 (keywords list)
 18  Para Matching Step 3 (scan paragraphs)
 19  Para Matching Step 4 (confirm match + answer)
 20  Exercise 3 Timer (180s)
 21  Exercise 3 Answers (1–2) (answer-table, Why column)
 22  Exercise 3 Answers (3–4)
 23  Exercise 3 Answers (5–6)
  ─────── Multiple Choice Strategy Block (5 steps) ───────
 24  Transition → Making conclusions (red bg)
 25  MC Header + Step 1 (demo Q + options)
 26  MC Step 2a (auto-animate entry, transparent borders)
 27  MC Step 2b (auto-animate reveal, white borders)
 28  MC Step 3 (scan + photo/headline tip)
 29  MC Step 4 (fragment strike table, a/b eliminated)
 30  MC Step 5 (answer-table wrap, answer + citations)
 31  Exercise 4 Timer (240s)
 32  Exercise 4 Answer (answer-table wrap, tick/cross, Why)
  ─────── Discussion — Review — Summary ───────
 33  Transition → Let's Discuss (red bg)
 34  Task → Let's Discuss (420s, 3 Qs)
 35  Transition → Let's Review (red bg)
 36  Summary (✓ bullets)
────────────────────────────────────────────
```

### Mandatory Pre-Write Ritual (for agent)

Complete these steps IN ORDER before writing ANY slide HTML.

**Phase 0: Design Blueprint (MANDATORY — before ANY HTML)**

After reading the lesson plan JSON and the reference templates, create a design blueprint document that maps every stage to its slides and specifies the pedagogical mechanism for each slide. This forces intentionality before implementation.

**Blueprint sections:**

1. **Stage-to-slide mapping** — list every `lesson_plan.stages[]` entry, what slide type(s) it produces, and which template pattern to copy from (e.g., "Type 4: Lead-in Error" from `reference-slideshow.html`).

2. **Per-slide design table:**

   | Slide ID | Stage | Type | Intent | Feature | Principle | Mechanism | Template Ref |
   |----------|-------|------|--------|---------|-----------|-----------|--------------|

   The Mechanism column must answer the litmus-test question for the named principle (see Mechanism Rubric in `docs/pedagogical-design-dictionary.md`).

3. **Auto-animate pair check** — list every `data-auto-animate-id`, its slide count (must be ≥2), verify previous slide has NO auto-animate, verify same background on all siblings.

4. **Answer slide sizing** — per exercise: item count → slide count → slide IDs. Flag >3 items.

5. **Fragment verification** — list every fragment slide, verify no fragments on objectives/transitions/summaries.

6. **Color/font audit** — verify backgrounds match slide type, verify no font-size below minimums.

The blueprint is a planning document — no HTML at this stage. Reference template patterns by type name only. Write the blueprint to `.kilo/plans/` as a plan file before proceeding to Phase 1.

**Phase 1: Pre-generation**
1. **Open `templates/reference-slideshow.html`** — scroll through EVERY slide type. This is a complete working slideshow with verified patterns. Identify which types you need, guided by the blueprint.
2. **Open `templates/base-slides-template.html`** — copy the `<head>` and `<script>` blocks exactly. Do not modify.
3. **Verify colors**: answer green = `#052e0d`, pedagogical teal = `#1a237e`. Never use `#1e7e34` or `#1a6b5a`.
4. **Verify font sizes**: body text ≥1em, labels ≥0.9em, title h2=2.2em, logo=120px, subheader=1em. Never use 0.7em.
5. **Plan the slide count**: ensure no answer slide has >3 items. Split if needed.

**Phase 2: Generation rules**
6. **Copy, don't invent** — use reference examples. Change content only, not structure.
7. **Title slides**: must use `data-background-color` + `data-background-image` + `style="justify-content: center;"`. Logo 120px, h2 2.2em, CEFR badge inline in h2.
8. **Auto-animate**: use only for structural transformations (simple→compound, error→correction). Entry = transparent borders on changed elements. Reveal = white `#fff` or yellow `#ffdd00`. Both need matching `data-auto-animate-id`.
9. **Answer slides**: One item per slide. Show the original sentence as a `<p>` above the `answer-list`. Use `class="a-row fragment fade-up"` so the entire row reveals on one click. Include `a-q` (classification label), `a-ans` (corrected sentence, yellow `#ffdd00`), and `a-why` (explanation, white). No `a-num` span — item number goes in the `<h2>`.
10. **DESIGN MECHANISM annotation** — Every pedagogical annotation block must now include a fourth line: `<!-- DESIGN MECHANISM: [specific design choice that makes the principle manifest — must pass the litmus test: "if I remove this mechanism, would the slide need to change?"] -->`. See `docs/pedagogical-design-dictionary.md` for the full Mechanism Rubric with principle-specific questions.
11. **Fragments on answers only**: objectives, summaries, transitions, and strategy steps stay static.

**Phase 3: Post-generation validation**
11. **Run `npx revealjs-validator --project "output/{subfolder}/slides/"`** and fix ALL errors.
12. **Visual check**: open in browser. Inspect title (full screen, centered, readable), answers (reveals work, S/V underlines visible), auto-animate pairs (transitions smooth), font sizes (minimums met), colors (green = #052e0d, teal = #1a237e).
13. **No push until user gives all-clear**. Commit locally only.

If any rule is unclear, ask. Do not guess.

### Key Design Rules

- **One step per slide** — enforced across all three pedagogy blocks
- **Step label format**: `<p><u><strong>Step N:</strong> description</u></p>`
- **Auto-animate**: only between adjacent slides with matching `data-id` on elements; previous slide must NOT have `data-auto-animate`
- **Fragment strike**: `class="fragment strike"` on td/p elements. Built-in CSS provides `opacity: 1` (always visible) and `text-decoration: line-through` only when `.visible` class is added on click
- **Answer tables**: `<table class="answer-table">` with 3 columns (Statement/Answer/Why?). Add `wrap` class for tables with long text. Right column uses `white-space: normal`
- **Table tick/cross**: middle column with `data-fragment-index` matching explanation cell for simultaneous reveal
- **Lightbulb removed** from all answer slides (saves screen real estate)
- **Color rule — ALL slides**: Only `#fff` (white) and `#ffdd00` (yellow) are permitted for ALL visible CSS properties — font color, borders, underlines, highlights. Never use `rgba(255,255,255,X)` with X < 1 — semi-transparent white creates invisible gray text at projection distance. No colored underlines, no blue/orange/green annotation colors — differentiate via style (solid vs dashed), font size, or symbols (❌/✅) instead. This applies to every slide background (#1a1a2e, #052e0d, #1a237e, #c0392b). The template's `.aim-label` uses gray `#888` by default and must be overridden with `#fff` on all slides. **No `box-shadow` on any slide except title slides** (where text-shield uses it, but only as an implementation detail — avoid explicit box-shadow in inline styles). Use `border-bottom: 4px solid #fff` or `4px solid #ffdd00` for emphasis instead.
- **Pedagogical background**: `data-background-color="#1a237e"` + `class="pedagogical"` + `data-background-transition="none"`
- **One item per answer slide** — When each answer has a Why explanation, use exactly one `a-row` per slide. The item number goes in the `<h2>` heading. Do not use `a-num` spans. The entire row (label + answer + why) reveals on one click via `class="a-row fragment fade-up"`.
- **Question/statement visible on slide entry, answers revealed** — On answer slides, the question or statement must be visible immediately when the slide enters. The answer (verdict, explanation, correction, source) must be inside a `<div class="fragment fade-up">` so the teacher can discuss the question first before revealing the answer.
- **Inline S/V/O annotations** — for grammar identification exercises (subjects, verbs, objects), decorate words directly on the sentence rather than using a separate answer column. Use `class="fragment custom svo-s"`, `svo-v`, `svo-o` on `<span>` elements with CSS controlling border/color changes on `.visible`. Superscript labels (`<sup>S</sup>`, `<sup>V</sup>`, `<sup>O</sup>`) use `opacity: 0` → `opacity: 1` with CSS transitions. Use `data-fragment-index` to group each sentence's decorations and confirmation note for per-click reveal.
- **Custom fragments** — use `class="fragment custom"` when you need an element to stay fully visible but change specific CSS properties (border, color, opacity) on click. The `custom` keyword prevents reveal.js from applying default `opacity: 0; visibility: hidden`. All styling is controlled via CSS rules on `.fragment.custom.*` (default state) and `.fragment.custom.*.visible` (revealed state). Common use: annotations that animate in without hiding the underlying text.
- **Title slide layout** — Use TWO slides: a splash slide (full-screen image only, no text) followed by the title slide (logo + h2 + badge + strap line + lesson type CTA). The splash slide primes the topic visually before any information appears.
   * **Splash slide**: `data-background-image` + `data-background-color` only. No content. No notes. Text-shield NOT needed (no text).
   * **Title slide**: Full-screen Pixabay background image using `data-background-image` with `data-background-color="#1a1a2e"` as fallback. Logo at `120px` (not 78px — too small on 1280x720). h2 at `2.2em` (not default ~1.6em). CEFR badge inline inside h2 with `vertical-align: middle`. Subheader at `1em` (not 0.7em) containing a **topic tagline or strap line** (e.g., "Are You a Super Recognizer?"), NOT teacher name, duration, or class identifier — those are presentation metadata, not student-facing content. Add a **second subtitle line** hinting at the lesson type (e.g., "Let's Read and Find Out" for reading, "Let's Listen and Find Out" for listening, "Let's Write" for writing, "Let's Learn" for grammar/vocab). This second line should be at 0.9em in bold white (`#fff`, `font-weight: bold`) with a **crimson text-shield** (`background: rgba(180, 0, 0, 0.65)`) so it visually pops as a call-to-action. **ALL title text (h2, subtitle lines) MUST use `class="text-shield"`** for readability against the image — this applies a semi-transparent dark background behind the text instead of dimming the entire image. No `data-background-opacity` needed (image stays at full brightness). **CRITICAL:** Must add `style="justify-content: center;"` to the section — reveal.js defaults to `flex-start`, pushing content to the top of the slide. Both `data-background-color` AND `data-background-image` are required (background-color shows while image loads). Do NOT use `r-stack` for title slides — it creates a letterbox effect.
- **Font size minimums for readability** — On 1280x720 slides: main sentence text `1.2em`, labels/annotations `0.9em`, faded "before" comparison text `1em`. Never go below `0.85em` for any text. The default reveal.js base sizes assume desktop presentation — ESL students at projection distance need larger. Differentiate faded "before" text via font size or a ❌ mark, never via opacity.
- **Why column on every answer row** — Every answer slide must include `class="a-why"` with a short explanation text (coordinator meaning, grammar rule, error type). The `a-why` class is defined in the base template CSS. Use `class="a-row fragment fade-up"` on the row div so the entire row (label, answer, why) reveals on one click — NOT per-span fragments.
- **Paragraph numbers on reading answers** — Every reading comprehension answer (summary, T/F, open questions) must include the paragraph number where the evidence is found, appended as `— Para N` at the end of the `a-why` text. This enables the teacher to direct students to the exact location for justification. Example: `"Term first used by Richard Russell in 2009 — Para 2"`.
- **Demo slide before freer practice** — Before any freer practice task (e.g. Practice 2C, 10A), include a pedagogical demo slide. The teacher walks through ONE item step by step (Step 1: identify relationship, Step 2: choose coordinator, Step 3: combine) so students see the reasoning chain before attempting independently.
- **Pedagogical slide before every exercise type** — In reading and listening lessons, include a pedagogical slide before EVERY distinct exercise type (gist summary, T/F, comprehension questions, matching, etc.). Use ONE item from the exercise as a worked example. Model the skill using auto-animate across 2-3 slides or fragments on a single slide. Do NOT put the pedagogical slide only before the first exercise — every exercise type needs its own modelled example. The demo must always use the **first question or item** from the following exercise, not a made-up example.
- **Opinion question structure** — For open-ended opinion exercises (e.g. "Do you think you are a super recogniser?"), teach a three-part response structure: **Opinion → Reason → Detail/Example**. Provide sentence starters for each part and a model answer that uses all three, so B1 learners have a concrete template to follow.
- **Lead-in error slides** — Each error gets a 2-slide auto-animate pair: Entry shows the error with transparent borders on problem words. Reveal shows the original (at a smaller font size or with ❌ mark) and the corrected version in `#ffdd00` yellow with white underlines on fix words. Label line tells what type of error it is. Do NOT use opacity < 1 on the original text — it creates invisible gray text. Differentiate via font size or a visible ❌ mark instead. All borders/underlines must be white (`#fff`) — use style (dashed vs solid) for differentiation if needed.
- **Diagnostic tests max 3 items per slide** — Split diagnostic tests across multiple slides (e.g. `slide-diagnostic-1-3`, `slide-diagnostic-4-6`). Add answer fragments below the questions with the correct coordinator and a Why explanation. Timer on each slide.
- **Formula reveals: 2-slide auto-animate pair** — When demonstrating a structural transformation (simple→compound, wrong→right): Entry shows both versions with transparent borders on CHANGED elements. Reveal changes borders to `#fff` white `border-bottom: 4px solid #fff` for a thick underline effect. Both need `data-auto-animate` with matching `data-auto-animate-id`. Key elements need matching `data-id` on both slides.
- **Vocabulary context sentences** — Context sentences for vocabulary words must make the meaning completely obvious from context alone. Use a two-sentence pattern: the first sentence uses the target word in natural context; the second sentence rephrases or demonstrates the meaning with simpler language. The sentences do NOT need to connect to the lesson's reading or listening text.
  ✅ Good: "Her job is to **recruit** new employees. Last week she gave jobs to five new people."
  ❌ Bad: "The police use special tests to **recruit** super recognizers." (does not make the meaning obvious)
- **Vocabulary word display** — On vocabulary slides: the English word is followed by a part-of-speech marker in smaller gray text, e.g. `remarkable (adjective)`. The target word in the context sentence must be wrapped in `<span class="vocab-word">` so it renders in yellow. The phonemic script must use `font-family: 'Times New Roman', Times, serif;` for reliable IPA character rendering.

## Pedagogical Strategy Slides — Design Principles

Strategy slides teach a test-taking or reading skill explicitly. The design follows a **modelled whole-task approach** consistent with Strategy-Based Instruction (SBI) in EFL/ESL reading pedagogy.

### Core Pattern: One Consistent Worked Example

Pick one real exam question and carry it through every step of the strategy. Never mix examples mid-flow. The student sees the complete process on a single item before attempting it alone.

Example: A True/False statement about the "generation gap" article runs through Steps 1–4. A Multiple Choice question runs through its own 3 steps. Do not switch between different exam items within the same strategy block.

### Step Structure

| Step | Cognitive function | What goes on the slide |
|---|---|---|
| 1 | Decode | Read the statement carefully. Note each separate claim. |
| 2 | Analyse | Break into Yes/No sub-questions. State the decision rule (Yes→TRUE / No→FALSE). |
| 3 | Locate | Identify which paragraph(s) contain the evidence. Name them explicitly. |
| 4 | Confirm | Show the original question in yellow. Quote the text that confirms each sub-answer. Conclude. |

### Slide Layout Rules

- **One step per slide** — each `<section>` covers a single step. This lets the teacher pause and check understanding at each decision point.
- **Header on first slide only** — `True/False Strategy` heading on Slide 1 of the block. Remaining slides show only the step label.
- **Original question in yellow** on first and last slides — `<p style="color:#ffdd00;"><em>"Statement text"</em></p>`
- **Underline step labels** — `<u><strong>Step N:</strong> ...</u>`
- **Real quotes on Step 4** — actual text excerpts from the article, in italics with the relevant phrase highlighted
- **Rule embedded at Step 2** — not a separate slide. Include it: "If you answer Yes to all → TRUE. If you answer No to even one → FALSE."
- **Auto-animate for keyword underlines** — use `data-auto-animate` on a pair of adjacent slides to animate keyword underlines appearing. See pattern below.
- **Teal background** — `data-background-color="#1a237e"` + `class="pedagogical"` on all strategy slides.
- **Top alignment** — use `padding-top: 30px` on `.reveal .slides > section.pedagogical` in CSS. Do NOT use negative margins (they clip content off-screen). Inline `style="top: 0;"` on the section element if needed.

### Auto-Animate for Underline Reveal

When a pedagogical slide needs to show key words being underlined (e.g. Step 2 of a strategy: "Underline key words"), use TWO successive `<section>` elements with matching `data-auto-animate`. The first shows the text with transparent borders; the second shows white borders. The transition is triggered by advancing through slides (click/right arrow), NOT by fragments.

**DO NOT use `class="fragment"`** for this purpose. Fragments hide text (`opacity: 0`) which produces blank spaces. Auto-animate between two slides is the correct approach.

Pattern (both sections need `data-auto-animate`):

```html
<!-- Enter state: plain sentence, borders invisible -->
<section class="pedagogical" data-background-color="#1a237e" data-background-transition="none" data-auto-animate data-auto-animate-id="underline-demo">
        <div style="overflow: hidden;">
            <p><u><strong>Step 2:</strong> Underline key words</u></p>
            <p data-id="mcq" style="color:#ffdd00;">
                <em>"What is the <span data-id="w1" style="border-bottom: 2px solid transparent;">main message</span>
                of this <span data-id="w2" style="border-bottom: 2px solid transparent;">article</span>?"</em>
            </p>
        </div>
    </section>
    <!-- After click: borders become visible, animate via auto-animate -->
    <section class="pedagogical" data-background-color="#1a237e" data-background-transition="none" data-auto-animate data-auto-animate-id="underline-demo">
    <div style="overflow: hidden;">
        <p><u><strong>Step 2:</strong> Underline key words</u></p>
        <p data-id="mcq" style="color:#ffdd00;">
            <em>"What is the <span data-id="w1" style="border-bottom: 2px solid white;">main message</span>
            of this <span data-id="w2" style="border-bottom: 2px solid white;">article</span>?"</em>
        </p>
    </div>
</section>
```

Requirements:
- Both `<section>` elements MUST have `data-auto-animate`
- The `<p>` wrapping the question MUST have a `data-id` attribute (same value on both)
- Each `<span>` wrapping a keyword MUST have a `data-id` attribute (same on both)
- Slide 1 uses `transparent` border color so the text appears plain but the border space is reserved
- Slide 2 uses `white` border color - auto-animate animates the color transition during slide advance
- The previous slide (e.g. Step 1) should NOT have `data-auto-animate` — this prevents unwanted animation between unrelated slides
- Use `data-background-transition="none"` to keep background from animating (teacher controls pacing)

### Auto-Animate for S/V/O Annotation Demonstration

For grammar lead-in slides where you want to demonstrate subjects (S), verbs (V), and objects (O) on a single sentence, use the same two-slide auto-animate pattern but with THREE simultaneous annotations:

- **Subject**: `border-bottom: 2px solid #fff` (white solid underline) + `<sup style="opacity:0">S </sup>` → `opacity:1; color:#ffdd00`
- **Verb**: `border-bottom: 4px solid #ffdd00` (yellow, thick) + `<sup>V </sup>`
- **Object**: `border: 2px solid #fff` (white box) + `<sup>O </sup>`

Pattern:

```html
<!-- Slide 1 (entry): plain sentence, transparent annotations -->
<section data-auto-animate data-auto-animate-id="svo-demo" data-background-color="#1a1a2e">
    <h2 data-id="title">What's inside a sentence?</h2>
    <p>
        <span data-id="subject" style="border-bottom: 2px solid transparent;">
            <sup style="opacity:0;">S </sup>My roommate
        </span>
        <span data-id="verb" style="border-bottom: 2px solid transparent;">
            <sup style="opacity:0;">V </sup>lost
        </span>
        <span data-id="object" style="border: 2px solid transparent;">
            <sup style="opacity:0;">O </sup>his keys
        </span>
    </p>
</section>
<!-- Slide 2 (annotated): decorations appear via auto-animate CSS transition -->
<section data-auto-animate data-auto-animate-id="svo-demo" data-background-color="#1a1a2e">
    <h2 data-id="title">What's inside a sentence?</h2>
    <p>
        <span data-id="subject" style="border-bottom: 2px solid #fff;">
            <sup style="color:#ffdd00;">S </sup>My roommate
        </span>
        <span data-id="verb" style="border-bottom: 4px solid #ffdd00;">
            <sup style="color:#fff;">V </sup>lost
        </span>
        <span data-id="object" style="border: 2px solid #fff; padding: 0 4px; border-radius: 4px;">
            <sup style="color:#fff;">O </sup>his keys
        </span>
    </p>
</section>
```

This is used for the **lead-in demonstration only** (one sentence). For multi-item practice exercises, use the inline S/V/O annotation with custom fragments (see Key Design Rules) instead — auto-animate would require 2 slides per item, which is impractical.

### Vertical Alignment Fix

Reveal.js `.slides` is a flex container that defaults to vertically centering its section children. To top-align pedagogical slides:

```css
.reveal .slides > section.pedagogical {
    align-self: flex-start;
    margin-top: 0;
    padding-top: 30px;
}
```

Do not use `margin-top: -X%` — it pushes content off-screen. A small positive `padding-top` on the section or its CSS parent is more reliable.

## Slide Icons

Decorative slide icons (`.slide-icon`, `.transition-icon`, `.pedagogical-icon`, `.objective-icon`) have been removed from all slide templates and the base template — they wasted screen real estate. Do not add decorative icons to any slide.

**Font Awesome IS still used for functional answer markers** — `<i class="fa-solid fa-check">` for correct answers and `<i class="fa-solid fa-times">` for incorrect answers on answer slides. These are functional indicators, not decorative icons. Never use raw Unicode check/cross characters (U+2713/U+2717), arrows (U+2192), bullets, or any other typographic symbols — Font Awesome renders reliably across all browsers and projection systems while Unicode symbols do not.

## Hard Rules (from real failures)

These rules exist because they were violated in production and cost hours to debug. Do not bypass them.

### Audio playback on vocabulary slides
- Audio must be placed **inside the word's `<p class="fragment fade-up">`** with `data-autoplay`. It fires on fragment reveal, NOT on slide entry.
- Remove `RevealAudioSlideshow` from the plugins array when using vocab TTS — its `fragmentshown`/`fragmenthidden` handlers interfere with native `<audio>` playback.
- Never use both `autoplay` (native HTML5) and `data-autoplay` (reveal.js) on the same element — they both fire independently, causing double-play.
- Hide audio via `position: absolute; width: 0; height: 0; overflow: hidden` (not `display:none`) so the browser loads audio data.

### DOM integrity after scripted edits
Every Python script that does `content.replace()` on raw HTML is a risk. After any such script, verify:
```python
opens = html.count('<section')
closes = html.count('</section>')
assert opens == closes, f"Mismatch: {opens} opens, {closes} closes"
```
revealjs-validator does NOT catch unbalanced tags or orphaned elements — only a tag-count check does.

### Strategy demonstrations
- Use **auto-animate across separate slides** (one per step), not fragments on a single slide.
- Fragments stack text vertically, creating a wall of text that overwhelms B1 learners.
- The key element (question, sentence, etc.) should have `data-id` across all slides so auto-animate keeps it stationary while step content changes.

### Timer + audio/video exclusion
Never put `data-timer` on a slide that plays any audio or video, regardless of mechanism:
- `data-audio-src` (plugin)
- Native `<audio data-autoplay>`
- `<video>` elements
- YouTube iframes or `data-background-iframe`

## Dependencies

- Python 3.x, Pillow, requests
- Typst CLI (NOT Quarto-embedded version)
- Roboto OTF fonts (TinyTeX or system)
- `@kilocode/plugin` in `.kilo/` and `.kilocode/` (tool internal, not for edits)
- reveal.js 5.x via CDN (loaded from `templates/base-slides-template.html`, no npm needed)

## Image replacement workflow (frequent task)

When asked to replace a slide background image with a Pixabay URL:

1. **Extract image ID** from the URL — e.g. `1407880` from `https://pixabay.com/photos/men-smoke-grill-picnic-forest-1407880/`
2. **Construct CDN URL** — `https://cdn.pixabay.com/photo/{year}/{month}/{day}/{id}_1280.jpg`  
   (Use the `_1280` variant for good resolution with reasonable size)
3. **Download + compress** using `compress_image()` from `scripts/pixabay_download.py`:
   ```python
   python -c "
   import sys; sys.path.insert(0, 'scripts')
   from pixabay_download import compress_image
   from pathlib import Path
   compress_image('CDN_URL', Path('output/SUBFOLDER/slides/assets/FILENAME.jpg'), ID, 1)
   "
   ```
4. **Place output** in `output/{subfolder}/slides/assets/` (the new pipeline output)
5. **Update HTML** — change the `data-background-image` attribute on the target slide to `assets/FILENAME.jpg`
6. **If no `assets/` dir exists**, create it first

The `compress_image` function applies: resize to 1920px max edge, JPEG quality=80, optimize=True (Pillow).

## Config dirs

- `.kilo/` — session plans, package.json (Kilo internal), and `.kilo/command/` for Kilo CLI commands (e.g., `lint.md`). Skills also live in `.kilo/skills/` (tracked by git).
- `.kilocode/` — legacy skills, node_modules (Kilo internal). **Now gitignored** — switching branches won't delete it anymore
- Skills at `.kilo/skills/<name>/SKILL.md` — new skills require Kilo restart
- Commands at `.kilo/command/<name>.md` — no restart needed

## Windows Path Handling

When processing `file://` URLs containing Windows paths with forward slashes (e.g., `file:///C:/PROJECTS/...`), the `/C:/` is misinterpreted. Use this pattern in Python:

```python
from pathlib import Path
url = url.strip()
if "#" in url:
    url = url.split("#")[0]
url = url.replace("file:///", "")
url = url.replace("file://", "")
path = Path(url)
if not path.exists():
    path = Path(url.replace("/", "\\"))  # Fix forward slashes for Windows
```

Alternatively, convert forward slashes to backslashes:
```python
windows_path = url.replace("/", "\\")
path = Path(windows_path)
```

### Pre-build Linter

Before running `revealjs-validator`, run the design-rule linter:

```bash
python scripts/lint_slides.py --project "output/<subfolder>/slides/"
```

This checks for banned colors (old teal/green/blue/orange), `text-shadow` CSS, `box-shadow`, and answer-slide structural violations (bundled items, missing original sentence, per-span fragments). Fix any errors before running the validator.

# Slide Editing Workflow

## Authorial Voice for Slide Design

When designing or editing slides, you are an **experienced ESL teacher with training in instructional design and materials writing**, not a software engineer. See the `lesson-plan-to-reveal` skill's **Authorial Voice** section for detailed guidance on how to phrase pedagogical annotations, context sentences, and design rationale in teaching terms, not engineering terms.

When the user asks to edit a slide at a reveal.js URL (e.g., `index.html#/7`):

1. **Run `scripts/locate_slide.py`** to determine the slide section:
   ```bash
   python scripts/locate_slide.py "file:///path/to/index.html#/7"
   # OR
   python scripts/locate_slide.py 7 --slides-dir path/to/slides/
   ```
2. The script outputs JSON with slide index, section name, heading, and line numbers
3. Edit `index.html` directly using the line numbers from the output — the slide is a raw HTML `<section>` element
4. No regeneration needed — just reload the browser
5. **When adding a new slide**, insert a new `<section>` element at the correct position in `<div class="slides">`. All subsequent slide indices shift by +1.

### Stable slide IDs — preferred method

**To avoid index confusion**, every `<section>` should have a stable `id` attribute (e.g., `id="slide-title"`, `id="slide-lead-in"`). Unlike numerical indices, IDs don't shift when slides are added or removed.

To locate a slide by its stable ID:
```bash
python scripts/locate_slide.py --id slide-objective --html path/to/slides/index.html
```

The script returns the line numbers and content for that slide regardless of its position in the sequence.

**Naming convention:** Use kebab-case prefixes matching the lesson stage:
- `slide-title`, `slide-objective`
- `slide-lead-in`, `slide-diagnosis-reveal`
- `slide-pet-scale-1`, `slide-pet-scale-2`
- `slide-test1-{range}` (e.g., `slide-test1-1-3`)
- `slide-test2-entry`, `slide-test2-reveal`
- `slide-transition-{target}` (e.g., `slide-transition-learn`)
- `slide-teach-{topic}` (e.g., `slide-teach-sentence-def`, `slide-teach-commands`)
- `slide-quick-check`
- `slide-transition-{topic}` (e.g., `slide-transition-capitals`)
- `slide-cap-rules-1-3`, `slide-cap-rules-4-6`
- `slide-did-you-know`
- `slide-p2b-task`, `slide-p2b-answers-{range}`
- `slide-p7-task`, `slide-p7-corrected-{range}`
- `slide-summary`, `slide-end`

## reveal.js Codebase

When making changes to reveal.js code (e.g., custom themes, configuration, or plugin modifications), **always query the live GitHub repository first**. Do not rely on static snapshots — the live codebase is the source of truth.

### Query Live reveal.js via Git

Use `gh` (GitHub CLI) to fetch individual files from the live repository. This is faster than cloning and always returns the current version.

```bash
# Get a specific file from the latest version
gh api repos/hakimel/reveal.js/contents/css/reveal.scss --jq '.content' | base64 -d

# Get the compiled CSS
gh api repos/hakimel/reveal.js/contents/dist/reveal.css --jq '.content' | base64 -d

# Get the main JS source
gh api repos/hakimel/reveal.js/contents/js/reveal.js --jq '.content' | base64 -d | head -200

# List the top-level directory structure
gh api repos/hakimel/reveal.js/contents/ --jq '.[].name'

# Search the codebase for a specific pattern (uses GitHub code search)
gh search code "data-auto-animate" --repo hakimel/reveal.js --limit 10

# Get a file from a specific tag/version
gh api repos/hakimel/reveal.js/contents/css/reveal.scss?ref=5.1.0 --jq '.content' | base64 -d
```

To see how a specific feature works (e.g., `autoAnimateUnmatched`), search the JS source:
```bash
gh api repos/hakimel/reveal.js/contents/js/reveal.js --jq '.content' | base64 -d | Select-String -Pattern "autoAnimateUnmatched" -Context 0,5
```

## Known CSS Conflicts with reveal.js

### Fragment `highlight-*` classes set `opacity: 1`

**Problem:** reveal.js built-in CSS forces `opacity: 1; visibility: inherit` on `.highlight-green`, `.highlight-red`, and `.highlight-blue` at all times. These classes are designed for color-change-on-reveal, not hide-reveal. Using `class="fragment highlight-green"` will NOT hide the element — it stays visible, only changing color when `.visible` is added.

**Evidence from compiled `reveal.css`:**
```css
.reveal .fragment.highlight-green{opacity:1;visibility:inherit}
.reveal .fragment.highlight-red{opacity:1;visibility:inherit}
/* .visible only changes color, not opacity: */
.reveal .fragment.highlight-green.visible{color:#17ff2e}
```

**Solution:** Use custom CSS classes that only apply on `.visible`:
```css
.reveal .fragment.answer-correct.visible {
    background: rgba(0, 120, 0, 0.5);
    padding: 0.3em 0.5em;
    border-radius: 4px;
}
.reveal .fragment.answer-incorrect.visible {
    background: rgba(120, 0, 0, 0.5);
    padding: 0.3em 0.5em;
    border-radius: 4px;
}
```
Then use `class="fragment answer-correct"` — the element starts hidden (default fragment behavior) and only gains background on click.

**To verify:** Check the compiled `reveal.css` from CDN for fragment CSS rules:
```bash
Invoke-WebRequest -Uri "https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/reveal.css" -OutFile "$env:TEMP\reveal.css"
Select-String -Path "$env:TEMP\reveal.css" -Pattern "fragment" -SimpleMatch
```

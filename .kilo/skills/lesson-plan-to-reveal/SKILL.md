---
name: lesson-plan-to-reveal
description: Converts a lesson plan JSON into a reveal.js presentation using raw HTML sections. All slides are hand-crafted <section> elements inside the base template. Markdown pipeline is permanently abandoned — auto-animate and pedagogical slides require native HTML.
---
# Skill: Lesson Plan to reveal.js Presentation

## Purpose
Convert a lesson plan JSON into a reveal.js slideshow for ESL classroom delivery. The teacher controls all slides — students never interact directly. **Slides support the teacher's narration, not replace it.** Student-facing content appears on screen; teacher procedure text goes in speaker notes only.

## Authorial Voice

When designing slides, adopt the voice of an **experienced ESL teacher with training in instructional design and materials writing**. All pedagogical annotations, context sentences, and design decisions must be articulated from this perspective. The technical implementation (HTML, CSS, reveal.js) is *how* you achieve the pedagogical goals, but the reasoning should always be expressed in teaching terms, not engineering terms.

- **PEDAGOGICAL INTENT** annotations should sound like a veteran teacher justifying a classroom decision to a colleague ("Students need to see the contrast at a glance, not read two paragraphs"), not an engineer documenting code ("The section uses a two-column flex layout with a vertical divider").
- **DESIGN MECHANISM** annotations should name the concrete design choice and what happens if it's removed, in teaching language ("If both columns were on separate slides, the comparison would be lost — students can't hold one in memory while they look at the other").
- **Context sentences** for vocabulary should be written as a teacher would model the word's meaning: clear, natural, immediately understandable from context.
- **Exercise instructions** on task slides should read as teacher-to-learner cues, not documentation.

When in doubt about phrasing, ask: "Would a teacher in the staffroom explain it this way?" If the answer is no, rewrite it.

**Pipeline**: JSON → hand-built `index.html` with raw HTML `<section>` elements → open directly in browser (no server needed).

**Markdown is permanently abandoned** for slide generation. The reveal.js auto-animate feature requires sibling `<section data-auto-animate>` elements, which cannot be produced from a single `<section data-markdown>` container. All new presentations start from `templates/base-slides-template.html`.

**Slide design authority**: `docs/slide-design-reference.md` defines all slide types, fragment policies, text limits, vocabulary rules, and auto-animate patterns.

## ⚠ CRITICAL — Tier-1 Reference Hierarchy

**Pre-generation ritual — mandatory before Step 0:**

1. Open `templates/reference-slideshow.html` in a browser and scroll through EVERY slide type. This is a complete working slideshow with verified HTML patterns for every slide type (title, lead-in, diagnostic, teach, auto-animate pairs, strategy, task, answer with S/V annotations, summary, end). Identify which types you need for the current lesson. Copy the pattern, change only the content.

2. **Cross-lesson dedup check**: Read `lesson_plan.stages[].procedure` for every stage. For any exercise referenced by name (e.g., "Practice 2D"), search the `output/` directory for OTHER lesson plan JSONs that reference the same exercise. If the exercise was already assigned in a prior lesson, flag it to the user — do NOT build duplicate slides unless the user explicitly confirms.

**The lesson plan JSON is the SOLE AUTHORITY for WHAT to teach. Everything else is HOW to present it.**

Design slides using this **four-tier priority hierarchy** (after the pre-generation ritual above). Each tier overrides everything below it:

1. **👑 Tier 1 — The lesson plan JSON** (`output/{subfolder}/{mmddyy}-{topic}-lesson-plan.json`)
   - `lesson_plan.stages[]` defines EXACTLY what slides to build, in what order, with what timing
   - Every `stage_number` MUST produce ≥ 1 slide
   - No slide may introduce content not referenced in the lesson plan
   - The procedure text, stage names, and exercise references in the JSON determine what goes on screen
   - If the JSON says Exercise 1-3, the slides cover Exercise 1-3 — never add Exercise 4

2. **📘 Tier 2 — This skill document** — the authoritative rules and patterns below
   - Defines HOW to build each slide type (layout, background color, fragment policy, notes format)
   - Use the Stage-to-Slide Mapping table to determine which slide types each stage produces

3. **📄 Tier 3 — `templates/base-slides-template.html`** — the boilerplate, CSS, Reveal.initialize() config
   - Copy this verbatim; never edit the `<head>`, `<style>`, or `<script>` config unless adding a plugin

4. **📖 Tier 4 — `docs/slide-design-reference.md`** — slide type definitions, fragment policy, text limits, backgrounds
   - Consult for fine-grained design rules when Tier 2 is ambiguous

**NEVER read, copy, or consult any existing slideshow in `output/*/slides/` as a design reference.** Every existing slideshow was built by a different process, may use legacy patterns (e.g., `<table class="answer-table">`, `answer-correct`/`answer-incorrect`, broken CSS, missing ids), and is NOT a valid reference for new presentations.

**If the user points to an existing slideshow as an example, do NOT replicate its HTML patterns.** Instead, tell the user the slideshow is legacy and may contain broken patterns. Design the new slides using only the four-tier hierarchy above.

**If you are tempted to run `read` on any file under `output/*/slides/` for design guidance, stop and read the lesson plan JSON instead.** The lesson plan is the source of truth for what should be on screen.

## When to Use This Skill

Use `lesson-plan-to-reveal` when converting a lesson plan JSON to slides. The skill:
1. **Parses the lesson plan JSON** — reads `lesson_plan.stages[]` to enumerate every stage and map each to slide types
2. **Determines pedagogical intent** — for each slide block, states what the student must *see happen* on screen and which reveal.js feature achieves that (consulting the Feature Lookup Table in `docs/slide-design-reference.md`)
3. **Reads source materials** — extracts exercise content from the source PDF and answer content from the answer key `.typ` file
4. Copies the institution logo into `output/{subfolder}/slides/assets/`
5. Copies `templates/base-slides-template.html` to `output/{subfolder}/slides/index.html`
6. Builds slides one by one as raw HTML `<section>` elements, each preceded by a mandatory pedagogical intent annotation
7. **Verifies every stage has at least one corresponding slide** — flags any stage that would be skipped
8. Reports the output path

## Workflow

### Step 0: Create the slides directory

```powershell
mkdir "output/{subfolder}/slides/assets"
```

### Step 1: Copy the base template

```powershell
cp "templates/base-slides-template.html" "output/{subfolder}/slides/index.html"
```

All slide `<section>` elements go between `<div class="slides">` and `</div>` in `index.html`. The `<head>`, `<style>`, `<body>`, `<script>` boilerplate is already complete — never edit it unless adding a new reveal.js plugin.

**Note:** The base template already includes the [audio-slideshow](https://github.com/rajgoel/reveal.js-plugins/tree/master/audio-slideshow) plugin (CDN-loaded) and the `TimerPlugin` in `Reveal.initialize()`. To add audio to a slide, use `data-audio-src="assets/file.mp3"` on the `<section>` element. Audio files go in `slides/assets/`. The plugin is configured with `advance: -1` (no auto-advance) — teacher controls playback via hover controls or `A` key. See the `audio:` config block in `Reveal.initialize()` for details.

**Known limitation — audio on multiple slides**: The audio-slideshow plugin does NOT reliably play the same audio file on more than one slide. If two or more slides need the same audio, copy the file to a distinct filename for each slide (e.g., `podcast_listen1.mp3` and `podcast_listen2.mp3`). Each `data-audio-src` value must be unique across the presentation.

### Vocabulary TTS Audio Pattern

When a lesson plan includes pre-teach vocabulary, generate TTS audio clips and embed them in the vocabulary slides so the word is spoken aloud when the English word fragment is revealed.

**Prerequisites:**
1. Run `scripts/design_tts_voice.py` (one-time per voice) to design and publish a bespoke voice.
2. Run `scripts/generate_vocab_audio.py` to create MP3 clips for each vocabulary word.

**Slide structure:** Place the `<audio>` element INSIDE the English word's `<p class="fragment fade-up">`, NOT at the `<section>` level. Use `data-autoplay` so reveal.js plays it when that fragment becomes visible.

```html
<section id="slide-vocab-1" class="vocab-slide" data-background-color="#1a1a2e" data-background-transition="none">
    <div style="text-align: center; padding: 60px 40px;">
        <p style="font-size: 1.8em; color: #ffdd00; letter-spacing: 0.05em;">
            /fəˈnetɪk/
        </p>
        <p class="fragment fade-up" style="font-size: 2.2em; color: #fff; font-weight: bold; margin-top: 0.5em;">
            <!-- Audio inside the word fragment — plays when this fragment is revealed -->
            <audio data-autoplay preload="auto" style="position: absolute; width: 0; height: 0; overflow: hidden;"
                   src="assets/vocab-word.mp3"></audio>
            <span class="vocab-word">word</span> <span style="color: #888; font-size: 0.5em;">(noun)</span>
        </p>
        <p class="fragment fade-up" style="font-size: 1.2em; color: #fff; margin-top: 1em;">
            Context sentence with <span class="vocab-word">word</span> highlighted.
        </p>
    </div>
</section>
```

**Key rules:**
- Audio fires on the **first fragment reveal** (English word), NOT on slide entry (phonemic script)
- Use `data-autoplay` (not native HTML5 `autoplay`) — reveal.js's `startEmbeddedContent(el)` plays it when the fragment becomes `.visible`
- Remove `RevealAudioSlideshow` from the plugins array — its `fragmentshown`/`fragmenthidden` handlers interfere with reliable single-playback
- Do NOT use a custom `slidechanged` handler — let reveal.js manage playback via `data-autoplay` inside the fragment
- Hide via `position: absolute; width: 0; height: 0; overflow: hidden` (not `display:none`) so the browser loads audio data
- Add part-of-speech marker after the English word in smaller gray text: `word (noun)`
- The phonemic script must use `font-family: 'Times New Roman', Times, serif;` for reliable IPA rendering

### Step 2: Copy supporting files (timer plugin, logo)

```powershell
cp "templates/timer-plugin.js" "output/{subfolder}/slides/timer-plugin.js"
cp "templates/timer-plugin.css" "output/{subfolder}/slides/timer-plugin.css"
cp "templates/ACT.png" "output/{subfolder}/slides/assets/logo.png"
```

**Note:** The logo is available in `assets/logo.png` and IS displayed on the title slide (centered at top, height: 78px). See Step 3 for title slide layout patterns.

### ⚠ Step 2b: Inline style block for answer-list CSS (ANSWER-LIST STYLE OVERRIDES)

The template's base answer-list CSS provides structural layout (flex, alignment). The inline block below adds color overrides and S/V annotation classes for green-background answer slides where the black theme's defaults are invisible. Add this `<style>` block inside the slides, immediately after the vocab task slide or before the first answer slide:

```html
<style>
    .reveal .answer-list { width: 100%; font-size: 0.95em; }
    .reveal .a-row { display: flex; align-items: baseline; padding: 0.5em 0; border-bottom: 1px solid #fff; gap: 0.5em; }
    .reveal .a-row:last-child { border-bottom: none; }
    .reveal .a-num { flex: 0 0 1.5em; text-align: left; color: #fff; font-size: 0.95em; }
    .reveal .a-q { flex: 0 0 auto; min-width: 0; color: #ffdd00; font-size: 0.9em; }
    .reveal .a-ans { flex: 1 1 auto; min-width: 0; text-align: left; padding: 0.1em 0.3em; border-radius: 4px; color: #ffdd00; font-size: 0.9em; line-height: 1.5; }
    .reveal .a-ans.a-cor.visible { background: rgba(76, 175, 80, 0.3); }
    .reveal .a-why { flex: 1 1 auto; min-width: 0; text-align: left; color: #fff; font-size: 0.9em; line-height: 1.5; }
    .reveal .a-s { border-bottom: 2px solid #fff; }
    .reveal .a-v { border-bottom: 3px solid #ffdd00; }
    .reveal .a-ls { color: #ffdd00; font-size: 0.75em; font-style: italic; margin-right: 1px; }
    .reveal .a-lv { color: #fff; font-size: 0.75em; font-style: italic; margin-right: 1px; }
    .reveal .aim-label { color: #fff; }
</style>
```

**Do NOT skip this.** Without it, answer rows may use wrong font sizes, borders, and missing S/V annotation classes.

### Step 3: Layout and Backgrounds

**Title slides: use `data-background-image` with `data-background-color` (NOT `r-stack`).** The `r-stack` approach creates a letterbox effect (content compressed into the middle). Use both background attributes plus `style="justify-content: center;"` to vertically center content:

```html
<section id="slide-title" data-background-color="#1a1a2e" data-background-image="assets/photo.jpg" data-background-size="cover" style="justify-content: center;">
    <img src="assets/logo.png" style="height: 120px; margin: 0 auto 0.5em; display: block;" alt="ACT" />
    <h2 style="font-size: 2.2em;"><span class="text-shield">Topic Title <span class="cefr-badge B1" style="font-size: 0.6em; padding: 4px 14px; vertical-align: middle;">B1</span></span></h2>
    <p style="font-size: 1em; margin-top: 0.5em;"><span class="text-shield">Subheader</span></p>
</section>
```

**Other image slides** (vocabulary, lead-in with photo): Use `data-background-image` with `text-shield` classes on all text elements.

**When to use each approach:**

| Scenario | Approach | Why |
|---|---|---|
| Title slide with full-bleed image | `data-background-image` + `data-background-color` + `text-shield` + `justify-content: center` | Full edge-to-edge image; no letterbox; text-shield keeps image at full opacity |
| Vocabulary/lead-in with image | `data-background-image` + `text-shield` | Image fills slide edge-to-edge; text needs shield for readability |
| Image fills remaining space after title | `r-stretch` on `<img>` | Responsive; title stays at top, image fills middle, caption at bottom |
| Stacking elements on top of each other | `r-stack` + fragments | Reveal images one at a time, or layer text over image |
| Framing an image/link | `r-frame` on element | Subtle border, hover effect on links |

**Do NOT auto-download Pixabay or any other images.** If the teacher provides a background image URL or file path, you may use it. Never fetch images independently.

Default background color reference (solid colors — no shielding needed):
| Slide type | Default background |
|---|---|
| Title, lead-in, general content | `#1a1a2e` (dark navy/black) |
| Transition (forward to next stage) | `#c0392b` (red) |
| Pedagogical/strategy blocks, grammar rules | `#1a237e` (teal) |
| Answer tables | `#052e0d` (green) |
| Summary | white (default) — **WARNING: white background + black theme = invisible white text.** Use `#1a1a2e` for summary slides unless text color is explicitly overridden. |
| End | `#2c3e50` (dark blue-gray) |

Background types available in reveal.js:
- **Solid color**: `data-background-color="#1a1a2e"` — default for most slides; no text-shield needed. Use `data-background-color`, NOT `data-background` (the bare `data-background` attribute is not recognized by reveal.js 5.x).
- **Gradient**: `data-background-gradient="linear-gradient(to bottom, #283b95, #17b2c3)"` — use for phase transitions or emphasis; no text-shield needed
- **Image**: `data-background-image="assets/filename.jpg" data-background-opacity="1.0"` — ONLY when teacher provides the file; ALL text on the slide MUST use `text-shield` or `text-shield-light`
- **Video**: `data-background-video="assets/clip.mp4" data-background-video-muted` — for lesson hooks, only with teacher-provided files; ALL text MUST use `text-shield`
- **Iframe**: `data-background-iframe="https://..." data-background-interactive` — for live web content as backdrop; text may need `text-shield` depending on the iframe content

**Rule summary:**
| Background type | `data-background-opacity` | Text-shield required? |
|---|---|---|
| Solid color | not applicable | No |
| Gradient | not applicable | No |
| **Image via `data-background-image`** | **`1.0`** | **Yes — ALL text must use text-shield or text-shield-light** |
| **Image via `r-stack`** | not applicable (use CSS opacity on `<img>`) | **No** — image is a normal element, text is separate |
| Video | `1.0` (implied) | Yes |
| Iframe | not applicable | Case-by-case |

See the [Reveal.js Backgrounds documentation](https://revealjs.com/backgrounds/) for full details on all available options and attributes.

### Step 4A: Parse the lesson plan — enumerate stages and map to slides

**CRITICAL — TIER-1 SOURCE: The lesson plan JSON is the sole determinant of slide content, slide count, and slide order.** Read ONLY `lesson_plan.stages[]` from the JSON to determine what slides to build. NEVER derive slide content from any other source (not from memory, not from the answer key, not from source PDFs that aren't referenced in the JSON).

**Rule of thumb:** If a piece of content is NOT mentioned in `lesson_plan.stages[].procedure` or `lesson_plan.stages[].stage`, it does NOT belong in the slides. The JSON is the contract — slides that depart from it are wrong.

Enforcement rules:
- Every `lesson_plan.stages[].stage_number` MUST produce at least one `<section>` slide
- Slide order MUST follow `stage_number` ascending (1, 2, 3, ...) — never reorder
- Do NOT use the old "Slide ordering convention" below — that was an artifact that caused missing stages

For each stage in `lesson_plan.stages[]`:
1. Read the stage name, aim, procedure, time, and interaction from the JSON.
2. Determine which slide type(s) this stage maps to, using the Stage-to-Slide Mapping table below.
3. For any exercise referenced in the procedure (e.g., "Practice 2B"), **read the source PDF** to understand what the exercise asks — but do NOT print the exercise text on screen. Students have the workbook. The task slide should show only the exercise number and a brief student-facing instruction.
4. For any answer key referenced in the JSON, **read the answer key file** (.typ) manually and re-express its content as HTML table rows. Do NOT attempt to parse Typst markup programmatically — `#table(...)` calls and `*bold*` syntax are not reliably machine-readable. Read the file, understand the answers, then hand-build the HTML.
5. For any bespoke (teacher-written) exercise that has no PDF source, **source content from the lesson plan JSON's procedure text** or from the user's specified item list. Do NOT assume all exercise content lives in a PDF.
6. Create the appropriate `<section>` elements.

**Stage-to-Slide Mapping** (use this to determine how many slides each stage needs)

**Content source rule:** Every column in the row below that says "Stage procedure" or "Lesson plan JSON" is **tier-1** and takes priority. Source PDFs and answer key files are **tier-2** — only consult them AFTER verifying the lesson plan references that exercise. If the lesson plan says "Practice 2B" but the PDF contains "Practice 2A", the lesson plan's exercise numbering is authoritative; update accordingly.

### Four-Slide Exercise Block Pattern

Every distinct exercise type MUST follow this four-slide sequence. This is the canonical pattern for all listening, reading, and language exercises:

| Step | Slide type | Background | Content | Audio/Timer |
|------|-----------|------------|---------|-------------|
| 1 | **Transition** | `#c0392b` (red) | Heading only — signals phase change to students | Neither |
| 2 | **Pedagogical** | `#1a237e` (teal), `class="pedagogical"` | Strategy instruction for the skill (e.g., how to listen for gist). May use auto-animate for keyword underline reveals. Differentiation challenge (`🏁 Want a challenge?`) shown here. | **No audio** — audio goes on the task slide |
| 3 | **Task** | `#1a1a2e` (dark) | Exercise number + brief student-facing instruction. **Do NOT print full exercise text** — students have the workbook. | `data-audio-src` for listening exercises; `data-timer` for written exercises. **Never both** on the same slide. Also never put a timer on a slide with any audio (native `<audio autoplay>`, `<video>`, or embedded YouTube). |
| 4 | **Answers** | `#052e0d` (green) | For simple reveals (T/F, MC): answer-list flex layout, max 3 items per slide. For error-correction with two fix methods: **both-methods pattern** (one item per slide, both M1 + M2). See "Answer Slides: Both-Methods Pattern" below. | Neither |

**Key rules:**
- Audio always goes on the **task slide**, never the pedagogical slide
- The pedagogical slide explains the *strategy*; the task slide tells students *what to do*
- Exercise content is in the workbook — the task slide shows only the exercise number and a one-line instruction
- WHY lines for listening comprehension answers use **direct transcript quotes**, not paraphrases
- WHY lines for language exercises use grammatical rule explanations
- Differentiation challenge text must be **student-facing** ("Want a challenge?…"), not teacher-facing ("Stronger Ss…")
- The checkered flag icon (`🏁` in HTML as `<i class="fa-solid fa-flag-checkered">`) marks challenge options

| Stage type (from name/purpose) | Slide(s) to create | Content source |
|---|---|---|
| Lead-in — discussion / prediction | 1 slide with open question, dark `#1a1a2e` background | Stage procedure + user's context (from JSON) |
| Lead-in — error analysis with auto-animate | 2-3 auto-animate slides: error sentences (transparent borders) → corrected sentences (visible borders) | Bespoke error sentences written in lesson plan JSON procedure text |
| Diagnostic test (Test 1 in TTT) | 1 slide with all test items on screen, dark `#1a1a2e` background | Lesson plan JSON procedure text (bespoke items) — NOT source PDF |
| Teach / Clarifying | 1-2 slides per concept taught (not per sub-rule); group related rules together | Stage procedure from JSON first; source PDF only for example sentences mentioned in that procedure |
| Controlled Practice / Practice X | 1 task slide (student-facing instructions + timer) + 1+ answer slides (see answer table sizing rules below) | EXERCISE: JSON procedure text (e.g., "Ss complete Practice 2B"). ANSWERS: answer key `.typ` file |
| Freer Practice / Practice X | 1 task slide + 1+ answer slides (see answer table sizing rules below) | EXERCISE: JSON procedure text. ANSWERS: answer key `.typ` file |
| Wrap-up | 1 summary slide | Stage procedure + learning objectives from JSON |
| Vocabulary (if pre-teach stage exists) | 1 slide per word (max 5) | Stage 11 pre-teach vocabulary selection (from the write-lesson-plan workflow) |

**Slide order**: Follow stage_number order from the JSON. Insert Title (slide 0) and Objective (slide 1) BEFORE stage 1. Insert End slide AFTER the last stage.

**CRITICAL — Stable id attributes**: Every `<section>` MUST have a unique `id` attribute following the `slide-{kebab-name}` convention (e.g., `id="slide-title"`, `id="slide-lead-in"`, `id="slide-vocab-task"`, `id="slide-predict-entry"`). This prevents index confusion when slides are added or removed later. Locate by `id` via `scripts/locate_slide.py --id slide-name --html path/to/index.html`.

**Speaker notes**: All slides EXCEPT transition slides and end slides must include `<aside class="notes">` containing:
- Stage aim from the JSON (`stage_aim`)
- Timing (`time` field in minutes)
- Interaction pattern (`interaction` field)
- The full procedure text from the JSON
- Do NOT put procedure text on screen — only student-facing task instructions

| Slide type | Notes required? | Content |
|---|---|---|
| Title | Yes | Lesson overview, teacher cues |
| Objective | Yes | Elicitation script, connection to prior learning |
| Lead-in | Yes | Activation script, timing, expected responses |
| Diagnostic test | Yes | Stage aim, timing, monitoring instructions |
| Teach / Clarifying | Yes | Key points to elicit, board plan cues |
| Task instruction | Yes | Full procedure, timing, interaction pattern |
| Answer table | Yes | Discussion prompts, expected student reactions |
| Transition | No | (Teacher's spoken introduction bridges the gap) |
| Summary | Yes | Elicitation script, connection to objective |
| End | No | — |

**Materials**: For any exercise referenced in the procedure by name (e.g., "Practice 2B", "Practice 7"), read the source PDF file from the `inputs/` folder to get the exercise text. Build screen content from the PDF, not from your own paraphrasing. The exercise must look exactly as it does in the textbook (same items, same numbering).

**Materials — reference rule**: The `materials` field in the lesson plan JSON must only reference **videos** (YouTube, etc.) and **printed material** (books, PDFs, handouts). Never reference supplied images (Pixabay, Wikimedia, user-provided photos, character composites, etc.) — those are slide assets managed separately and are not materials the teacher needs to prepare.

**Answers**: For any exercise that has an answer in the answer key, read the answer key `.typ` file and build answer slides using the **flex answer-list layout**, NOT `<table class="answer-table">`. Use `<div class="answer-list">` with flex rows:

```
<div class="answer-list">
    <div class="a-row">
        <span class="a-num">1.</span>
        <span class="a-q">Statement text</span>
        <span class="fragment fade-up a-ans a-cor"><i class="fa-solid fa-check"></i> Answer</span>
    </div>
</div>
```

- `a-cor` for correct answers (green background on reveal via CSS `.a-cor.visible`)
- `a-inc` for incorrect answers (red background on reveal via CSS `.a-inc.visible`)
- `fragment fade-up` animates each answer sliding up while fading in
- `fa-check` / `fa-times` for check/cross icons (never raw Unicode U+2713/U+2717)

**CRITICAL — CSS values for left-alignment.** These exact CSS values are required for the layout to read left-to-right naturally. Do NOT guess or change them:

```
.a-num { flex: 0 0 1.5em; text-align: left; }       ← MUST be left (not right)
.a-q   { flex: 0 0 auto; min-width: 0; }             ← MUST take only needed width
.a-ans { flex: 1 1 auto; min-width: 0; }             ← MUST fill remaining space, NOT min-width:160px
```

If `.a-num` is `text-align: right`, the number floats right and breaks the visual flow. If `.a-q` is `flex: 1 1 auto`, it fills all space and pins the answer to the far right. If `.a-ans` is `flex: 0 0 auto; min-width: 160px`, the answer hangs on the right with large gaps.


**CRITICAL — Add the inline style block from Step 2b before any answer slide.** Without it, the flex layout breaks on green backgrounds because the template's CSS is corrupted by a missing `}` in `.cefr-badge`.

### Answer Slides: Both-Methods Pattern (one per item)

For error-correction exercises where students need to see **both fix methods** (e.g., Method 1: period, Method 2: comma + coordinator) with an explanation, use the **one-item-per-slide pattern** with stacked vertical layout:

**When to use:**
- Error-correction exercises (run-ons, comma splices, fragment fixes)
- Any exercise where the answer key lists alternative correction methods
- Exercises where showing both correct alternatives is pedagogically important

**Do NOT use this pattern for:**
- Simple answer reveals (T/F, MC, comprehension Qs) — use the `answer-list` row layout instead
- Exercises with >1 item needing a quick overview (no space for 10+ slides)

**CRITICAL RULES:**
- **One item per slide** — never bundle multiple items
- Fragment sequence: error badge → Method 1 → Method 2 → Why
- Correct items (no fix needed): fewer fragments — badge → "No fix needed" → Why
- Use `class="answer-slide"` on the `<section>` tag — this removes text-shadow for a clean look on green
- Use `.p11-answer`, `.p11-badge`, `.p11-original`, `.p11-method`, `.p11-fix`, `.p11-why` classes (CSS is in the base template; no inline `<style>` block needed for the base styles)
- **Underlines on changes**: use `<span class="cor-add">` around added/changed text — renders as yellow (`#ffdd00`) text with a thick white (`3px solid #fff`) underline
- **No text shadows** — `.answer-slide` strips them via `text-shadow: none !important`
- **No gray text** — only `#fff` and `#ffdd00`

**Pattern for error items:**

```html
<section id="slide-practice-answers-N" class="answer-slide" data-background-color="#052e0d" data-background-transition="none">
    <h2>Practice N — Item N</h2>
    <div class="p11-answer">
        <p class="fragment fade-up p11-badge" data-fragment-index="1">error type</p>
        <p class="p11-original">"Original sentence with the error."</p>
        <div class="p11-method fragment fade-up" data-fragment-index="2">
            <p><u><strong>Method 1:</strong> Add a period</u></p>
            <p class="p11-fix">&rarr; "Fixed sentence<span class="cor-add">.</span>"</p>
        </div>
        <div class="p11-method fragment fade-up" data-fragment-index="3">
            <p><u><strong>Method 2:</strong> Add a comma + coordinator</u></p>
            <p class="p11-fix">&rarr; "Fixed sentence, <span class="cor-add">and</span> ..."</p>
        </div>
        <p class="p11-why fragment fade-up" data-fragment-index="4">Why: Explanation of the error and why both fixes work.</p>
    </div>
</section>
```

**Pattern for correct items (no error):**

```html
<section id="slide-practice-answers-N" class="answer-slide" data-background-color="#052e0d" data-background-transition="none">
    <h2>Practice N — Item N</h2>
    <div class="p11-answer">
        <p class="fragment fade-up p11-badge" data-fragment-index="1" style="color: #fff;">OK &mdash; Correct</p>
        <p class="p11-original">"Correct sentence."</p>
        <div class="p11-method fragment fade-up" data-fragment-index="2">
            <p>Both methods: <strong>No fix needed</strong> &mdash; correct compound sentence.</p>
        </div>
        <p class="p11-why fragment fade-up" data-fragment-index="3">Why: Already has comma + coordinator. &#10003;</p>
    </div>
</section>
```

**Key CSS classes** (defined in `base-slides-template.html`):
| Class | Purpose |
|-------|---------|
| `.answer-slide` | Strips text-shadow from all text inside the slide |
| `.p11-answer` | Flex container, 0.9em, left-aligned |
| `.p11-badge` | Inline error-type label (e.g., "comma splice", "run-on") |
| `.p11-original` | Yellow italic original sentence, bottom-bordered |
| `.p11-method` | Wrapper for one correction method |
| `.p11-fix` | White fix text, indented |
| `.cor-add` | **Yellow text + thick white underline** — marks added/changed text |
| `.p11-why` | Explanation box with yellow left border, dark background |

**Design rules for `.cor-add`:**
- Use on added punctuation, capitalized letters, added coordinators
- Always wraps ONLY the text that changed
- Use multiple `<span class="cor-add">` per fix if multiple changes (period + capitalized letter):  
  `"...strangers<span class="cor-add">.</span> <span class="cor-add">T</span>hey..."`

### Step 4A-bis: Design Blueprint (MANDATORY — Design Gate)

**⚠ THIS IS A DESIGN GATE. NO HTML IS WRITTEN UNTIL THE BLUEPRINT IS COMPLETE. ⚠**

Before writing any `<section>` tags, create a design blueprint that enumerates every planned slide and specifies exactly how each one achieves its pedagogical goal. The blueprint is a planning document that validates design choices against the existing templates and cognitive principles.

**Blueprint format** (write to `.kilo/plans/` as a plan file):

```
## Design Blueprint — [Lesson Topic]

### Stage-to-Slide Mapping
| Stage # | Stage Name | Slide Type(s) | Template Pattern | Slide IDs |
|---------|-----------|---------------|------------------|-----------|
| 1       | Lead-in   | Auto-animate error pair (×2) | Type 4: reference-slideshow.html | slide-leadin1-entry, slide-leadin1-reveal, ... |

### Per-Slide Design
| Slide ID | Intent | Feature | Principle | Mechanism | Template Ref |
|----------|--------|---------|-----------|-----------|--------------|

### Auto-Animate Pairs
| data-auto-animate-id | Slide count | Slide IDs | Same bg? | Prev slide no AA? |
|---------------------|-------------|-----------|----------|-------------------|

### Answer Slide Sizing
| Exercise | Total items | Slides needed | Slide IDs | All ≤3 items? |
|----------|------------|---------------|-----------|---------------|

### Fragment Verification
| Slide ID | Fragment usage | On allowed slide type? | Notes |
|----------|---------------|----------------------|-------|

### Color & Font Audit
| Slide ID | Background | Correct for type? | Font-size check | Notes |
|----------|------------|------------------|-----------------|-------|
```

**Reference rule:** When filling in "Template Pattern," reference the exact type number from `templates/reference-slideshow.html` (e.g., "Type 4: Lead-in Error Auto-animate Pair") or `templates/base-slides-template.html`. Do not describe the pattern in prose — point to the existing verified example.

**Mechanism litmus test:** For every row in the Per-Slide Design table, the Mechanism column must answer the rubric question for the named principle. If the mechanism is generic ("the teacher clicks to advance"), stop and rethink until you can name a design choice unique to this slide.

**After the blueprint is complete**, advance to Step 4A-ter.

### Step 4A-ter: Human-Readable Pedagogical Narrative (MANDATORY — Design Gate)

**⚠ THIS IS A HUMAN GATE. THE NARRATIVE IS SHOWN TO THE USER FOR APPROVAL BEFORE ANY CODE IS WRITTEN. ⚠**

Before writing any `<section>` tags, write a plain-English narrative of the entire slideshow that explains:
- What each stage does
- Why it is designed this way (pedagogical justification)
- What design choices were made (fragments, timers, auto-animate, audio, answer reveals)
- How the learner experiences each stage

The narrative should be written in an instructional voice — as if explaining the lesson to a fellow teacher. It must walk through every stage in order.

**Narrative format:**

```
The slideshow is organised like this.

We begin with [stage/activity]. This [explain purpose]. It is pedagogically useful because [explain why]. I have included [specific features — questions, fragments, timers, auto-animate, audio, answer reveals] so the learner can [explain what the learner gains].

[Repeat for every stage of the lesson. Be specific about design choices:
- "I have included fragment clickthroughs so the learner can see how we add commas and coordinators to form compound sentences."
- "There is one slide for each coordinator type."
- "Each vocabulary word has an autoplay audio file embedded in the word fragment. The audio fires when the English word fragment is revealed, not when the slide enters — so students attempt to decode the phonemic script first, then hear the word as they see the spelling."
- "Answers are split across multiple slides (one per item) so the teacher can pause and discuss each answer before revealing the next."
]

We end with [summary/end].
```

**⚠ THIS IS A DESIGN GATE. THE NARRATIVE IS NOT SHOWN UNTIL THE LINTER PASSES. ⚠**

Before showing the narrative to the user, run both lint checks and fix all violations:

```bash
python scripts/lint_slides.py --project "output/{subfolder}/slides/"
python scripts/check_authorial_voice.py --project "output/{subfolder}/slides/"
```

If **either** check produces violations (errors or warnings about authorial voice, lazy references, technical-only mechanisms, or identical annotations), **fix the HTML annotations first**, then re-run the checks. Only proceed to the user when both checks pass cleanly with 0 authorial voice violations.

**Only then** present the narrative to the user for approval. No HTML is written until the user gives approval.

**After the user approves the narrative**, advance to Step 4B and write the HTML, using both the narrative and the blueprint as guides.

### Step 4B: Build slides (new build)

**⚠ THIS IS A DESIGN GATE. WRITE THE ANNOTATIONS FIRST, THEN THE HTML. DO NOT REVERSE THIS ORDER. ⚠**

Before writing a single `<section>` tag, you must write **FOUR** comment lines for every slide:

```html
<!-- PEDAGOGICAL INTENT: [what the student must SEE happen on screen] -->
<!-- WHY THIS FEATURE: [reveal.js feature + why alternatives fail] -->
<!-- COGNITIVE PRINCIPLE: [Mayer's 12 principle. If none fits, state "none — assessment task"] -->
<!-- DESIGN MECHANISM: [specific design choice that makes the principle manifest — must pass the litmus test: "if I remove this mechanism, would the slide need to change?"] -->
```

**These four lines are a design gate.** If you cannot fill in all four convincingly, you do not understand what the student needs to learn from this slide. Redesign the slide until you can. Do NOT write the `<section>` HTML until the annotations are complete.

The DESIGN MECHANISM is the most important line — it bridges the abstract principle to the concrete implementation. See the **Mechanism Rubric** in `docs/pedagogical-design-dictionary.md` for principle-specific questions.

How it works:
1. Iterate through the Design Blueprint from Step 4A-bis
2. For each planned slide, write the four annotation lines
3. Then write the `<section>` HTML
4. Advance to the next blueprint row and repeat

If you catch yourself writing annotation lines that are identical across multiple slides in a row (same intent, same feature, same principle, same mechanism, same justification), you are NOT designing each slide intentionally. Stop and reconsider each slide's unique purpose.

**Four-line format (exactly these, no additions):**

| Line | Purpose | Example |
|------|---------|---------|
| `PEDAGOGICAL INTENT` | What the student MUST SEE HAPPEN on screen | `Student sees the error sentence transform into a correct one. The added comma+coordinator animates in with a blue border.` |
| `WHY THIS FEATURE` | Which reveal.js feature + why alternatives fail | `Auto-animate morphs WRONG to RIGHT across two slides; fragments would hide the original, losing the comparison.` |
| `COGNITIVE PRINCIPLE` | Name from Mayer's 12 (Signaling, Segmenting, Spatial Contiguity, Coherence, Temporal Contiguity, Modality) or explain why none applies | `Temporal Contiguity — both versions visible simultaneously; the animated border signals exactly what changed.` |
| `DESIGN MECHANISM` | Concrete design choice that operationalizes the principle on THIS specific slide | `The period between sentences is wrapped in a transparent-border span that reserves layout space. On reveal, it morphs to comma+coordinator with a thick yellow underline (`4px solid #ffdd00`). Without the reserved space, the morph would cause line jump, breaking contiguity.` |

For the feature choice in `WHY THIS FEATURE`, pick from: `auto-animate`, `fragments`, `sibling slides`, `data-line-numbers`, `data-mark`, `data-transition`, `data-background-gradient`, `vertical slides`, `audio`, `autoslide`, `code blocks`, `lightbox`, `r-fit-text`, `r-stack`, `r-stretch`, `custom-fragment`, `nested-fragment`, or `static — [reason]`.

**These annotations are enforced by `check_pedagogical_intent.py`** — every non-exempt slide must have all four lines, or the script exits with code 1. Exempt slides (transitions, end, title, objective) are hard-coded in the script and should not be expanded.

### Option A: Component builder (preferred for answer slides, transitions, tasks, auto-animate pairs)

Import `scripts.slides_builder` and call helper functions instead of hand-writing repetitive HTML. This produces correct HTML with verified fragment indices, icon classes, flex layout, and auto-animate attributes.

```python
from scripts.slides_builder import (
    answer_row, answer_slide,
    transition_slide,
    task_slide,
    pedagogical_slide,
    intent_comment, aside_notes,
    title_slide, objective_slide, end_slide,
    auto_animate_underline_pair,
    auto_animate_highlight_pair,
    auto_animate_svo_pair,
    svo_annotation_span,
)
```

Functions output HTML strings only — no file I/O, no side effects. Compose them into the splice file as shown in the usage examples below.

### Option B: Hand-written HTML (for bespoke content)

Use only for slides that don't fit a builder function (e.g. grammar diagrams, bespoke visual layouts, custom structures). Every slide must still pass the pedagogical intent and structural tests.

Write slide sections to a temp file, then splice them into the template. **Do NOT attempt to write the entire `index.html` in a single Write tool call** — at 600+ lines with Unicode content, the Write tool may reject or mangle the file. Do NOT copy the template and then incrementally replace sections with Edit tool calls — this is slow, fragile, and causes timeouts.

Instead, use the **splice approach**:

1. **Compose all `<section>` elements** in a temp file at `C:\Users\elwru\AppData\Local\Temp\kilo\slides_sections.html` using the Write tool.
2. **Copy the template** to the output directory via PowerShell:
   ```powershell
   cp "templates/base-slides-template.html" "output/{subfolder}/slides/index.html"
   ```
3. **Run a Python splice script** that finds the `<div class="slides">` boundary in the template and inserts the sections, then updates the `<title>`:
    ```python
    import re
    template_path = r"output/{subfolder}/slides/index.html"
    sections_path = r"C:\Users\elwru\AppData\Local\Temp\kilo\slides_sections.html"
    
    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()
    with open(sections_path, "r", encoding="utf-8") as f:
        sections = f.read()
    
    # Find the slides div boundary RELIABLY using the <!-- Mark.js anchor.
    # DO NOT use template.find("</div>") — the sections themselves contain
    # </div> inside answer-list flex rows, which causes silent truncation.
    start_marker = '<div class="slides">'
    start_idx = template.find(start_marker)
    
    # Anchor on <!-- Mark.js (unique in template) then rfind backwards
    mark_js = template.find('<!-- Mark.js')
    first_div = template.rfind('</div>', 0, mark_js)    # closes reveal div
    second_div = template.rfind('</div>', 0, first_div)  # closes slides div
    
    result = template[:start_idx + len(start_marker)] + "\n\n" + sections + "\n" + template[second_div:]
    result = result.replace("<!-- TOPIC -->", lesson_title)
    
    with open(template_path, "w", encoding="utf-8") as f:
        f.write(result)
    ```
4. **Update the `<title>`** by replacing `<!-- TOPIC -->` with the lesson topic.
5. Then verify the output (Step 5).

**Why this works:**
- The Write tool call writes to the allowed `C:\Users\elwru\AppData\Local\Temp\kilo\` directory (no permission issues)
**CRITICAL — PowerShell `-replace` destroyes UTF-8.** PowerShell `-replace` on HTML files with non-ASCII characters (em dashes —, curly quotes "", apostrophes ', accented letters) silently corrupts them. The mismatch between .NET's UTF-16 and the file's UTF-8 produces bytes like `0x97` that break Python decoders. **Never use PowerShell `-replace` for HTML content modifications.** Write a Python script to `C:\Users\elwru\AppData\Local\Temp\kilo\` and execute it instead — Python handles UTF-8 natively and its `re.sub()` matches exactly what the HTML contains.
- The splice is deterministic — finds `<div class="slides">` then anchors on `<!-- Mark.js` to locate the correct closing `</div>`. Never uses `template.find("</div>")` directly — the sections themselves contain `</div>` in answer-list flex rows (`<div class="a-row">...</div>`), and naive `</div>` search causes silent truncation to ~6 slides.
- No size limit concerns — sections and template are written separately

The boilerplate (everything before `<div class="slides">` and everything after the closing `</div>` of the slides div) is always the same. Only the `<section>` elements inside `<!-- SLIDE N -->` comments change per lesson.

#### C. Editing an existing slideshow

**Editing an existing slideshow is fundamentally different from building one from scratch.** Existing slideshows may contain legacy patterns (old color schemes, stale CSS, bundled answer slides, incorrect annotations) that must be audited before any changes are made.

##### Phase 1: Pre-edit audit (MANDATORY)

Before touching any HTML, run this audit checklist:

1. **Read the lesson plan JSON** — this is the SOLE authority for what content should exist. Identify every stage and exercise.
2. **Count slides** — use `grep '<section ' index.html` to get the total. Verify against expected count from stage mapping.
3. **Scan for legacy colors** — `#4fc3f7` (blue), `#ff8a65` (orange), `#0d4a3d` (old teal), `#0d5e1a` (old green), `#4caf50` (green checkmark) are all deprecated. If any exist, note them for a batch color fix pass.
4. **Check answer slide sizing** — count `a-row` items per answer slide. Any slide with >1 `a-row` violates the one-per-item rule.
5. **Check for box-shadow** — `grep "box-shadow"` on the file. Except title slides, all must be removed.
6. **Check for text-shadow** — `grep "text-shadow"` on the CSS. Must be none.
7. **Scan auto-animate IDs** — ensure each `data-auto-animate-id` appears exactly twice (entry + reveal) and pairs are adjacent siblings.

Create a task list from the audit findings before proceeding to Phase 2.

##### Phase 2: Edit strategy

1. **Git safety first** — run `git status` to check for uncommitted changes. If the working tree is dirty, either commit or `git stash` before editing. This gives you a clean rollback point via `git checkout -- <file>` without losing unrelated work.
2. **Batch edits by type** — never mix edit types. Process in this order:
   - Global color replacements (CSS, background colors, badge levels)
   - Structural changes (adding/removing slides, splitting bundles, replacing auto-animate patterns)
   - Content corrections (answer text, Why columns, original sentences)
   - Comment updates (stale slide numbers, DESIGN MECHANISM annotations)
3. **Use Python for bulk changes** — for any change that affects more than 3 locations, write a Python script to `C:\Users\elwru\AppData\Local\Temp\kilo\` and execute it. Do NOT use PowerShell `-replace` — it corrupts Unicode.
4. **Verify after each batch** — run `npx revealjs-validator --project "output/{subfolder}/slides/"` after each batch. If it fails, the last batch introduced an error — fix before proceeding.

##### Phase 3: Targeted edits

When the user asks to modify a specific slide:
1. Use `scripts/locate_slide.py` to find the exact line numbers by slide ID.
2. Use the `Edit` tool for targeted changes — ideally one edit per slide.
3. **Never use large replace-all when a targeted edit will do.** Large oldString replacements are fragile: whitespace differences, encoding mismatches, or partial matches can leave orphan content in the file.

**Rule**: Every slide is a raw `<section>` element inside `<div class="slides">`.

### Step 5: Verify output

**Prefer revealjs-validator over bespoke scripts.** The project includes `revealjs-validator` (npm dev dependency) which checks 66 rules derived from the official Reveal.js docs. Run it in project mode for cross-file validation:

```bash
npx revealjs-validator --project "output/{subfolder}/slides/"
```

You can also target a single slideshow for faster iteration using the `--slideshow-html` CLI argument:
```bash
python -m pytest tests/test_slide_structure.py --slideshow-html "output/{subfolder}/slides/index.html" -v --tb=short
```

This catches broken auto-animate pairs, invalid fragment classes, missing assets, CSS misuse, and more. **However, the validator only checks static HTML structure — it CANNOT detect runtime errors that cause a blank page.** A presentation can pass all 66 rules and still show a blank screen due to a JavaScript error during `Reveal.initialize()`.

**CRITICAL — Browser test every build:** After the validator passes, open the slides in a browser and check the JavaScript console (`F12` → Console tab):
- Verify the page shows content (not blank/white)
- Verify NO red errors appear in the console
- Common runtime errors: undefined plugin references, CDN failures, plugin `init()` crashes
- If the page is blank, remove recently added plugins from the `plugins` array first, then debug

For the specific checks the validator doesn't cover (e.g., lesson plan stage coverage, answer table sizing, speaking notes on every slide), write a focused Python verification script to `C:\Users\elwru\AppData\Local\Temp\kilo\` that uses `in` operator checks.

If a check fails, do NOT trust what the terminal displays (Unicode renders inconsistently). Instead:
```python
idx = content.find(check_words[0])  # search for first word
if idx >= 0:
    print(repr(content[idx:idx+80]))  # show exact bytes
    print(content[idx:idx+80].encode("utf-8").hex())  # show hex
```

**Checklist:**
- **CRITICAL — Stage coverage check**: Count the number of `<section>` slides created (excluding Title + End). Verify this matches the number of `lesson_plan.stages[]` items. Each stage must have ≥ 1 corresponding `<section>` slide. If a stage has no slides, flag it immediately.
- **CRITICAL — Section count integrity**: Use `<!-- Mark.js` anchor to extract the slides region, NOT `re.search(r'<div class="slides">(.*?)</div>')` (which stops at the first `</div>` inside answer-list rows). Use this pattern:
  ```python
  start = content.find('<div class="slides">')
  mark_js = content.find('<!-- Mark.js')
  first_div = content.rfind('</div>', 0, mark_js)
  second_div = content.rfind('</div>', 0, first_div)
  slides_content = content[start:second_div]
  ```
  Then count sections via `slides_content.count('</section>')` or `len(re.findall(r'<section[\s>]', slides_content))`. If the count is wrong, the splice script's boundary detection failed — check that it uses `<!-- Mark.js` anchor, not `template.find("</div>")`.
- Check `index.html` exists in the slides directory
- Check `timer-plugin.js` and `timer-plugin.css` exist in the slides directory
- Check every `<section>` has a stable `id` attribute (`id="slide-..."`) — extract via `re.findall(r'id="(slide-[^"]*)"', slides_content)` and confirm count matches section count.
- Verify `TimerPlugin` is in the `plugins` array of `Reveal.initialize()`
- Verify answer slides use `a-cor`/`a-inc` (NOT `answer-correct`/`answer-incorrect`, NOT `highlight-green`/`highlight-red`)
- Verify answer slides use `fragment fade-up` (not bare `fragment`) on answer spans
- Verify answer slides use `<div class="answer-list">` flex layout, not `<table class="answer-table">`
- **Answer list sizing**: Count item rows per answer-list. Max 3 items per answer slide. **However, when each item has a Why explanation (full sentence or grammatical rule), use ONE item per slide** — the combination of sentence text + answer (+ S/V annotation where applicable) + Why explanation is too much for more than one item. Split exercises with >3 items across multiple slides (e.g., `slide-ex2-answers-1-3`, `slide-ex2-answers-4-5`), and use one-per-item for any exercise where answers include explanations.
- **Both-methods answer slides**: Verify each slide uses `class="answer-slide"` on `<section>` — without it, global text-shadow creates a blurry look on green backgrounds.
- **Both-methods answer slides**: Verify `.cor-add` spans exist on added/changed text — without them, students can't see what was modified. Check `border-bottom: 3px solid #fff` in the CSS.
- **Both-methods answer slides**: Verify each error-type slide has BOTH `.p11-method` blocks (M1 + M2), and correct-item slides have exactly one "No fix needed" block.
- Verify no instructional text like "Click to reveal" appears on slides — answer reveal behavior is self-evident.
- Verify fragment usage: only on answer reveal slides and strategy demonstrations, not on expository content
- Verify procedure text is in `<aside class="notes">`, not on screen
- Verify vocabulary words use `<span class="vocab-word">word</span>`
- Verify title slide has strap subheader (not date/teacher/materials)
- Verify `autoAnimateUnmatched: true` is in `Reveal.initialize()`
- Verify every slide with `data-auto-animate` also has `data-auto-animate-id` — without it, `null === null` causes all auto-animate slides to animate into each other.
- Verify transition slides use `data-background-color="#c0392b"` (use `data-background-color` for solid colors, NOT `data-background` — `data-background` is not recognized by reveal.js 5.x)
- Verify pedagogical strategy slides use `data-background-color="#1a237e"` and `class="pedagogical"`
- Verify listening task slides that need audio have `data-audio-src="assets/filename.mp3"`
- **Verify no `<section>` has both `data-timer` AND any audio or video** — never place a timer pill on a slide that plays audio or video (whether via `data-audio-src`, native `<audio autoplay>`, `<video>` elements, or embedded YouTube/iframe content). Timers and audio/video are mutually exclusive across ALL mechanisms, not just the audio-slideshow plugin.
- **Verify no raw Unicode check/cross characters**: Scan for U+2713 (✓) and U+2717 (✗) in the output HTML. If found, replace with `<i class="fa-solid fa-check">` and `<i class="fa-solid fa-times">` respectively. Font Awesome renders reliably; Unicode glyphs do not.
- **PEDAGOGICAL INTENT CHECK**: Run `python scripts/check_pedagogical_intent.py --project <slides-dir>` — verifies every non-exempt slide has mandatory `PEDAGOGICAL INTENT`, `WHY THIS FEATURE`, `COGNITIVE PRINCIPLE`, and `DESIGN MECHANISM` annotations. If missing, the slide was built without intentional design and must be fixed. Do NOT ship slides that fail this check.
- **Regression check on slide moves**: When moving a slide from one position to another, insert the slide at the new location FIRST, then remove it from the old location. Removing first and forgetting to re-insert causes silent slide loss. After any move, verify total section count matches expected count.

### Step 6: Publish and write URL to lesson plan JSON

After slides are verified, publish to GitHub Pages and write the deployment URL into the lesson plan JSON as `slideshow_url`. This feeds into the PDF template's gray-shaded Slideshow URL cell.

**Prerequisites:** `gh` CLI installed and authenticated. See `publish-to-github-pages` skill for details.

```powershell
# Extract owner and repo from git remote
$remoteUrl = git remote get-url origin
$owner, $repo = if ($remoteUrl -match 'github\.com[:\/](.+?)\/(.+?)\.git') { $matches[1], $matches[2] }
$url = "https://${owner}.github.io/${repo}/"

# Write URL to the lesson plan JSON
$jsonPath = "output/{subfolder}/{mmddyy}-{topic}-lesson-plan.json"
$json = Get-Content $jsonPath -Raw | ConvertFrom-Json
$json | Add-Member -MemberType NoteProperty -Name "slideshow_url" -Value $url -Force
$json | ConvertTo-Json -Depth 10 | Set-Content $jsonPath

Write-Host "Slideshow URL written to $jsonPath : $url"
```

## Fragment Policy

| Use fragments for | DO NOT use fragments for |
|---|---|
| Revealing answers (`a-cor`/`a-inc` with `fragment fade-up`) | Task instructions, vocabulary lists |
| Eliminating wrong MC options (`fragment strike`) | Objectives/outcomes, discussion questions |
| Strategy step reveals (on pedagogical slides) | Lead-in images and prompts, transitions |
| Directional emphasis (`fade-up`, `fade-down`, etc.) | Any expository or static content |

**Class quick reference:** `fragment fade-up a-ans a-cor` for correct reveals, `fragment strike` for elimination, `fragment grow` for single-word emphasis. NEVER use `highlight-green`/`highlight-red` (they force `opacity: 1` — never hide).

For custom CSS fragments, nested fragments, `highlight-current-*`, `fade-in-then-out`, and `current-visible`, see `docs/pedagogical-design-dictionary.md`. Copy verified fragment patterns from `templates/reference-slideshow.html` — do not invent new class combinations.

## Pedagogical Design Principles

Before building any slide, you MUST answer these **FOUR** questions for every student-facing element:

1. **What must the student *see* happen?** The student needs to witness a visual transformation — a word changing color, an answer appearing, a wrong option being eliminated. Slides are not documents; they are moments of revealed understanding.
2. **Which reveal.js feature achieves that?** Consult the **Decision Framework** and **Feature Lookup Table** in `docs/pedagogical-design-dictionary.md`. The table maps every reveal.js feature to a specific pedagogical use case. Do not guess from training data.
3. **Which cognitive principle does this serve?** Every design choice must be justified against established multimedia learning theory (Mayer, Sweller). See `docs/pedagogical-design-dictionary.md` for the complete Mayer's 12 Principles reference table and Decision Framework. If you cannot name the principle, the design may be cosmetic rather than pedagogical.
4. **What specific design mechanism makes this principle manifest on this particular slide?** Name the exact visual/interactive/structural choice that would be absent if the principle were ignored. See the **Mechanism Rubric** in `docs/pedagogical-design-dictionary.md` for principle-specific questions.

For the feature choice question (#2), consult the **Decision Framework** and **Feature Lookup Table** in `docs/pedagogical-design-dictionary.md` — they map every reveal.js feature to a specific pedagogical use case. Do not guess from training data.
### Pedagogical Intent Annotation

Every slide block must be preceded by a FOUR-line comment block explaining the pedagogical goal. This is **mandatory** — it forces intentionality before writing code:

```html
<!-- PEDAGOGICAL INTENT: Student sees the subject word transform from white to yellow. -->
<!-- WHY THIS FEATURE: Auto-animate transforms appearance; fragments only reveal/hide. -->
<!-- COGNITIVE PRINCIPLE: Signaling + Temporal Contiguity — highlighting essential material while the label appears simultaneously improves transfer. -->
<!-- DESIGN MECHANISM: The subject word has a transparent underline on entry (reserving layout space). On reveal, the underline becomes #ffdd00 yellow with a thick underline (`4px solid #ffdd00`) — the eye tracks the color transition, which IS the subject identification. Without the transparent pre-reserved space, the underline would appear abruptly, causing layout shift. -->
```

The annotation must state:
- **What visual transformation the student witnesses** (not what the slide *says*, but what *happens* on screen)
- **Why this feature was chosen** (and implicitly, why alternatives would fail)
- **Which cognitive principle it serves** (from the Mayer's 12 reference table above)
- **What specific design mechanism operationalizes this principle on THIS slide** (named a choice that would be absent if the principle were ignored)

If you cannot write all four, you do not understand what the student needs to learn from this slide. Stop and reconsider the slide design.

### Common Anti-Patterns (DO NOT DO)

See `docs/pedagogical-design-dictionary.md` for the full anti-patterns table. Key ones to avoid:
- `highlight-green`/`highlight-red` — use `a-cor`/`a-inc` with `fragment fade-up` instead
- Putting the answer in the slide title — use a separate answer slide after the task slide
- Instructional text like "Click to check" on auto-animate reveals — the visual transformation IS the answer, no instruction needed
- **Guessing the slide pattern instead of reading the reference** — if you are tempted to write a `<section>` without first reading the closest matching pattern in `templates/reference-slideshow.html` or `templates/base-slides-template.html`, stop. The correct pattern already exists. Reading it takes 30 seconds. Guessing and redoing takes 30 minutes.
- **Editing without auditing first** — modifying an existing slideshow without running the pre-edit audit (see Section C, Phase 1) guarantees missed legacy patterns and duplicated work.

## Slide Type Templates

Full HTML patterns with pedagogical intent annotations live in `templates/base-slides-template.html` as HTML comments. **Copy the pattern, paste it into `<div class="slides">`, and adapt the content.** Do not invent new patterns — use only variants documented there.

Every slide must be preceded by this mandatory FOUR-line comment block:

```html
<!-- PEDAGOGICAL INTENT: [what the student must SEE happen on screen] -->
<!-- WHY THIS FEATURE: [reveal.js feature + why alternatives fail] -->
<!-- COGNITIVE PRINCIPLE: [name the principle from Mayer's 12, or state why it doesn't apply] -->
<!-- DESIGN MECHANISM: [specific design choice that makes the principle manifest — see Mechanism Rubric in pedagogical-design-dictionary.md] -->
```

Quick reference of slide types and their pedagogical intent:

| Slide type | Background | Student sees | Feature |
|---|---|---|---|
| Title | `#1a1a2e` | Topic + CEFR + strap | Static — orientation |
| Objective | default | 3 outcomes (full visibility) | Static — orientation |
| Vocabulary | `#1a1a2e` | IPA visible first; English word + context reveal on click | Fragment — reveal |
| Lead-in | `#1a1a2e` | One open question | Static — activation |
| Transition | `#c0392b` | Heading only, phase signal | Static — rest |
| Teach (sentence/grammar) | `#1a237e` | Word/part transforms (color, border, highlight) | Auto-animate — transformation |
| Teach (rules/reference) | `#1a237e` | Rules in 2-column table (Rule | Example) | Static — reference |
| Strategy (step-by-step) | `#1a237e` | Each step is one slide | Sibling slides — discrete teaching |
| Task instruction | dark + timer | Instructions full-visible | Static — orientation |
| Answer (T/F, MC) | `#052e0d` | Statements visible; answers reveal per-row | Fragment on `<span>` inside `<td>` |
| Summary | default | "I can..." checkmarks | Static — consolidation |
| End | `#2c3e50` | Topic + CEFR | Static — exit |

**CRITICAL — Answer list sizing**: Max 3 items per answer-list slide. If an exercise has more than 3 items, split across multiple answer-list slides (e.g., `slide-ex2-answers-1-3`, `slide-ex2-answers-4-5`). Use `data-fragment-index` for per-row reveal coordination if needed.

## Slide Indexing System

When the user provides a reveal.js URL like `file:///.../index.html#/N`, use `scripts/locate_slide.py` to map the slide index to its HTML section.

```bash
python scripts/locate_slide.py "file:///path/to/index.html#/7"
python scripts/locate_slide.py 7 --slides-dir path/to/slides/
```

The script reads `index.html` directly (not a markdown file). The slide index equals the 0-based position of the `<section>` element within `<div class="slides">`.

Mapping:
- URL `index.html#/` or `index.html#/0` → first `<section>` (title)
- URL `index.html#/1` → second `<section>` (objective)
- URL `index.html#/7` → eighth `<section>`
- And so on...

### Slide Editing Workflow (HTML)

When asked to edit a slide at a reveal.js URL:

1. **Run `scripts/locate_slide.py`** to determine the section index and line numbers:
   ```bash
   python scripts/locate_slide.py "file:///path/to/index.html#/7"
   ```
2. The script outputs JSON with slide index, heading text, and line numbers
3. **Edit `index.html` directly** using the line numbers from the output — no intermediate markdown file
4. **No regeneration needed** — the HTML is already complete. Just reload the browser.
5. **When adding a new slide**, insert a new `<section>` element at the correct position in `<div class="slides">`.

**Stable slide IDs (preferred):** Every `<section>` should have a stable `id` attribute to prevent index confusion when slides are added or removed:
```html
<section id="slide-lead-in" data-background-color="#1a1a2e">
```
To locate a slide by its stable ID:
```bash
python scripts/locate_slide.py --id slide-objective --html path/to/slides/index.html
```
Use kebab-case names matching the slide function (e.g., `slide-title`, `slide-objective`, `slide-lead-in`, `slide-test1-1-3`, `slide-p7-corrected-1-3`, `slide-summary`).

## Key Design Rules

Rules 0–15 covering colors, layout, backgrounds, fragments, annotations, and file output. See `references/key-design-rules.md` for the complete reference. Critical rules to remember:

- **Rule 0 — No gray text.** Only `#fff` and `#ffdd00` on all backgrounds. No green, blue, red, or gray text.
- **Rule 7 — Answer slides**: Use one `a-row` per slide (NEVER bundle multiple items). Show the original sentence as a `<p>` above the `answer-list`. No `<span class="a-num">` — the item number goes in the `<h2>`. Use `class="a-row fragment fade-up"` on the row div so the entire row (label + answer + why) appears on one click. `a-ans` text must be yellow `#ffdd00` (both text and FA icon). `a-why` remains white `#fff`. Never use `highlight-green`/`highlight-red`.
- **Rule 9 — Backgrounds**: dark `#1a1a2e` (title/lead-in), red `#c0392b` (transitions), teal `#1a237e` (pedagogical), green `#052e0d` (answers), `#2c3e50` (end).
- **Rule 10 — Title slides**: `justify-content: center;`, logo 120px, h2 2.2em, CEFR badge inline. When using `data-background-image`, do NOT use `data-background-opacity` — add `class="text-shield"` to all text elements instead.
- **Rule 15 — Symbols**: Font Awesome only (`<i class="fa-solid fa-check">` / `<i class="fa-solid fa-times">`). Never raw Unicode U+2713/U+2717.
- **Rule 16 — One per item**: When each answer has a Why explanation, use exactly one `a-row` per slide. Do not bundle multiple items even if the max-3 limit permits it. The heading must say "Practice N — Item N", not "Practice N — Answers (1-3)".
- **Rule 17 — Answer text verbatim**: Every corrected sentence in an answer slide must exactly match the answer key. No truncation, no paraphrasing. Read the `.typ` file and copy the corrected text character by character.
- **Rule 18 — Whole-row fragment**: Use `class="a-row fragment fade-up"` on the `<div class="a-row">`, not on individual spans. The entire row (label + answer + explanation) appears on one click.
- **Rule 19 — Original sentence on answer slides**: Always show the original (uncorrected) sentence as `<p style="font-size: 0.8em; color: #fff; margin-bottom: 0.5em;">` above the answer-list. Students need to compare original vs corrected.
- **Rule 20 — No text-shadow**: The global `text-shadow` CSS block is removed from the template. Do not add `text-shadow` to any CSS rule or inline style. Use `class="answer-slide"` on answer sections to strip any remaining shadows.

Read the full rule list from `references/key-design-rules.md` when you encounter an unfamiliar slide type or when a rule check fails.
## Authorial Voice & Audience

B1 default (Mathayom 2-3). See `references/authorial-voice.md` for the complete vocabulary ceiling, sentence complexity limits, and B2 adaptation rules. Core rules:

- **Person Rule**: Direct "you" imperatives on screen. Third-person ("Students read...") is banned.
- **Vocabulary Ceiling**: No words above CEFR B1 without inline definition (e.g., "identify" → "find", "infer" → "understand what the writer means").
- **Sentence Complexity**: Max 15 words, no semicolons, no passive voice on screen.
- **Summary**: "I can..." statements only.

Read the full file from `references/authorial-voice.md` during the Design Blueprint phase to check language against the B1 word list.

## reveal.js Feature Lookup

See the complete Decision Framework, Feature Lookup Table, Mayer's 12 Principles, and Common Anti-Patterns in `docs/pedagogical-design-dictionary.md`.

**Key decision rule**: Auto-animate for transformations — color changes, border reveals, word replacement, and element repositioning (items reordering within a container to show correct matching). Fragments for reveals — answers appearing, options being eliminated. Sibling slides for discrete teaching moments — each step is its own slide where the teacher pauses.

## Pedagogical Strategy Slides

See AGENTS.md (`Pedagogical Strategy Slides — Design Principles`) for the full SBI design framework. Key rules for this project:
- **One consistent worked example** per strategy block — carry one exam item through all steps
- **One step per slide — STRICTLY ENFORCED. NEVER cram multiple steps onto one pedagogical or strategy slide.** Each `<section>` covers exactly one step so the teacher can pause at each decision point. If your strategy has steps labelled Step 1, Step 2, Step 3, and Step 4, you need FOUR consecutive `<section>` slides (not one slide with four bullet points). Use sibling slides (static, or chained with `data-auto-animate` for step-build-up effects). This rule applies to ALL pedagogical teaching slides — skimming strategy, T/F/NG strategy, critical thinking frames, error correction demos, and any slide that walks through a sequence. A single pedagogical slide with 4 step-labels is a design violation. Test: if any student-facing text on a pedagogical slide contains more than one `<u><strong>Step N:</strong>` element, the slide is violating this rule and must be split.
- **Step label format**: `<u><strong>Step N:</strong> description</u>`
- **Header on first slide only**, remaining slides show only the step label
- **Auto-animate for keyword underlines**: use `<span data-id="...">` with transparent→visible border transitions across consecutive `<section data-auto-animate>` siblings
- **Teal background**: `data-background-color="#1a237e"` + `class="pedagogical"` on all strategy slides
- **Top alignment**: CSS `.reveal .slides > section.pedagogical { align-self: flex-start; padding-top: 30px; }`

## Common Pitfalls

Debug reference for when builds fail or layouts break. See `references/common-pitfalls.md` for the complete guide covering:

- **Plugin safety protocol** — blank page on init failure, add plugins one at a time
- **Temp file workflow** — write to temp dir, splice with Python, never write large files directly
- **Answer-list CSS traps** — `.a-num: text-align: left`, `.a-q: flex: 0 0 auto`, `.a-ans: flex: 1 1 auto`
- **Gray text ban** — template traps in `.aim-label`, `.source-cite`, `.material-ref`, `.a-num`

Consult `references/common-pitfalls.md` only when: verification fails, answer-list layout breaks, or the slides appear blank/empty in browser.

## Files

| File / Directory | Purpose |
|---|---|
| `docs/slide-design-reference.md` | Slide design rules (authoritative) — consult before building |
| `docs/pedagogical-design-dictionary.md` | Decision Framework, Feature Lookup Table, Mayer's 12 Principles, Anti-Patterns |
| `templates/base-slides-template.html` | Base template for ALL new presentations |
| `scripts/locate_slide.py` | Map reveal.js URL index to HTML section |
| `scripts/pixabay_download.py` | Pixabay image downloader |
| `templates/ACT.png` | Institution logo — copy to `assets/logo.png` |
| `references/key-design-rules.md` | Complete design rules (15+ rules) |
| `references/authorial-voice.md` | B1 authorial voice rules, vocabulary ceiling, sentence complexity |
| `references/common-pitfalls.md` | Plugin safety, CSS traps, gray text fixes |

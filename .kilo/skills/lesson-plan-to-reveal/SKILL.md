---
name: lesson-plan-to-reveal
description: Converts a lesson plan JSON into a reveal.js presentation using raw HTML sections. All slides are hand-crafted <section> elements inside the base template. Markdown pipeline is permanently abandoned — auto-animate and pedagogical slides require native HTML.
---
# Skill: Lesson Plan to reveal.js Presentation

## Purpose
Convert a lesson plan JSON into a reveal.js slideshow for ESL classroom delivery. The teacher controls all slides — students never interact directly. **Slides support the teacher's narration, not replace it.** Student-facing content appears on screen; teacher procedure text goes in speaker notes only.

**Pipeline**: JSON → hand-built `index.html` with raw HTML `<section>` elements → open directly in browser (no server needed).

**Markdown is permanently abandoned** for slide generation. The reveal.js auto-animate feature requires sibling `<section data-auto-animate>` elements, which cannot be produced from a single `<section data-markdown>` container. All new presentations start from `templates/base-slides-template.html`.

**Slide design authority**: `docs/slide-design-reference.md` defines all slide types, fragment policies, text limits, vocabulary rules, and auto-animate patterns.

## ⚠ CRITICAL — No Outside Reference

**Design new slides using ONLY these three sources, in this order of priority:**
1. **This skill document** — the authoritative rules and patterns below
2. **`templates/base-slides-template.html`** — the boilerplate, CSS, and Reveal.initialize() config
3. **`docs/slide-design-reference.md`** — slide type definitions, fragment policy, text limits, backgrounds

**NEVER read, copy, or consult any existing slideshow in `output/*/slides/` as a design reference.** Every existing slideshow was built by a different process, may use legacy patterns (e.g., `<table class="answer-table">`, `answer-correct`/`answer-incorrect`, broken CSS, missing ids), and is NOT a valid reference for new presentations.

**If the user points to an existing slideshow as an example, do NOT replicate its HTML patterns.** Instead, tell the user the slideshow is legacy and may contain broken patterns. Design the new slides using only this skill document's patterns and the base template.

**If you are tempted to run `read` on any file under `output/*/slides/` for design guidance, stop and read this skill instead.** The patterns you need are documented here.

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

### Step 2: Copy supporting files (timer plugin, logo)

```powershell
cp "templates/timer-plugin.js" "output/{subfolder}/slides/timer-plugin.js"
cp "templates/timer-plugin.css" "output/{subfolder}/slides/timer-plugin.css"
cp "templates/ACT.png" "output/{subfolder}/slides/assets/logo.png"
```

**Note:** The logo is available in `assets/logo.png` for potential use but is NOT displayed on the title slide. Title slides now use `r-stack` layout with a Pixabay image. See Step 3 for layout patterns.

### ⚠ Step 2b: Inline style block for answer-list CSS (FIX BROKEN TEMPLATE)

The base template has a CSS syntax error in `.cefr-badge` (missing closing `}`) that can break `.answer-list` and `.a-row` rules. Add this `<style>` block inside the slides, immediately after the vocab task slide or before the first answer slide:

```html
<style>
    .reveal .answer-list { width: 100%; font-size: 0.85em; }
    .reveal .a-row { display: flex; align-items: baseline; padding: 0.4em 0; border-bottom: 1px solid rgba(255,255,255,0.1); gap: 0.5em; }
    .reveal .a-row:last-child { border-bottom: none; }
    .reveal .a-num { flex: 0 0 1.5em; text-align: left; color: rgba(255,255,255,0.5); font-size: 0.85em; }
    .reveal .a-q { flex: 0 0 auto; min-width: 0; margin-right: 0.5em; }
    .reveal .a-ans { flex: 1 1 auto; min-width: 0; text-align: left; padding: 0.1em 0.3em; border-radius: 4px; }
    .reveal .a-ans.a-cor { color: #fff; }
    .reveal .a-ans.a-cor.visible { background: rgba(76, 175, 80, 0.3); }
    .reveal .a-ans.a-inc { color: #fff; }
    .reveal .a-ans.a-inc.visible { background: rgba(244, 67, 54, 0.3); }
    /* Override template's gray #888 aim-label — invisible on green #1e7e34 */
    .reveal .aim-label { color: rgba(255,255,255,0.7); }
</style>
```

**Do NOT skip this.** Without it, the answer-list flex layout may not render correctly due to the template CSS bug.

### Step 3: Layout and Backgrounds

**Prefer `r-stack` over `data-background-image` for image+text slides.** Instead of using a full background image (which forces text-shield on every element), use `r-stack` to layer a slide-level image with text positioned over it:

```html
<section>
  <div class="r-stack" style="height: 100%;">
    <img class="r-stretch" src="assets/photo.jpg" style="object-fit: cover; opacity: 0.85;" />
    <h2 style="position: relative; z-index: 1; align-self: center;">Title over image</h2>
  </div>
</section>
```

This avoids the text-shield entirely: the image is a normal `<img>` element you can style, dim, or position independently of the text.

**When to use each approach:**

| Scenario | Approach | Why |
|---|---|---|
| Text overlaid on image | `r-stack` + `<img>` + positioned text | No text-shield needed; image is a normal element you can dim, crop, or position |
| Full-bleed background image | `data-background-image` | When image must fill entire slide edge-to-edge; requires text-shield |
| Image fills remaining space after title | `r-stretch` on `<img>` | Responsive; title stays at top, image fills middle, caption at bottom |
| Stacking elements on top of each other | `r-stack` + fragments | Reveal images one at a time, or layer text over image |
| Framing an image/link | `r-frame` on element | Subtle border, hover effect on links |

**Do NOT auto-download Pixabay or any other images.** If the teacher provides a background image URL or file path, you may use it. Never fetch images independently.

Default background color reference (solid colors — no shielding needed):
| Slide type | Default background |
|---|---|
| Title, lead-in, general content | `#1a1a2e` (dark navy/black) |
| Transition (forward to next stage) | `#c0392b` (red) |
| Pedagogical/strategy blocks, grammar rules | `#1a6b5a` (teal) |
| Answer tables | `#1e7e34` (green) |
| Summary | white (default) |
| End | `#2c3e50` (dark blue-gray) |

Background types available in reveal.js:
- **Solid color**: `data-background="#1a1a2e"` — default for most slides; no text-shield needed
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

**CRITICAL: The lesson plan JSON is the primary authority for slide content.** Read `lesson_plan.stages[]` from the JSON. Every stage MUST produce at least one slide. Do NOT use the generic "Slide ordering convention" below — that was an old artifact and caused missing stages. Derive slide order from stage order.

For each stage in `lesson_plan.stages[]`:
1. Read the stage name, aim, procedure, time, and interaction from the JSON.
2. Determine which slide type(s) this stage maps to, using the Stage-to-Slide Mapping table below.
3. For any exercise referenced in the procedure (e.g., "Practice 2B"), **read the source PDF** to get the actual exercise content that students will see on screen.
4. For any answer key referenced in the JSON, **read the answer key file** (.typ) manually and re-express its content as HTML table rows. Do NOT attempt to parse Typst markup programmatically — `#table(...)` calls and `*bold*` syntax are not reliably machine-readable. Read the file, understand the answers, then hand-build the HTML.
5. For any bespoke (teacher-written) exercise that has no PDF source, **source content from the lesson plan JSON's procedure text** or from the user's specified item list. Do NOT assume all exercise content lives in a PDF.
6. Create the appropriate `<section>` elements.

**Stage-to-Slide Mapping** (use this to determine how many slides each stage needs):

| Stage type (from name/purpose) | Slide(s) to create | Content source |
|---|---|---|
| Lead-in — discussion / prediction | 1 slide with open question, dark `#1a1a2e` background | Stage procedure + user's context |
| Lead-in — error analysis with auto-animate | 2-3 auto-animate slides: error sentences (transparent borders) → corrected sentences (visible borders) | Bespoke error sentences from lesson plan |
| Diagnostic test (Test 1 in TTT) | 1 slide with all test items on screen, dark `#1a1a2e` background | Lesson plan JSON procedure text (bespoke items) |
| Teach / Clarifying | 1-2 slides per concept taught (not per sub-rule); group related rules together | Source PDF definitions + examples + rule statements |
| Controlled Practice / Practice X | 1 task slide (student-facing instructions + timer) + 1+ answer slides (see answer table sizing rules below) | Source PDF exercise content + answer key file |
| Freer Practice / Practice X | 1 task slide + 1+ answer slides (see answer table sizing rules below) | Source PDF exercise content + answer key file |
| Wrap-up | 1 summary slide | Stage procedure + learning objectives from JSON |
| Vocabulary (if pre-teach stage exists) | 1 slide per word (max 5) | Stage 11 pre-teach vocabulary selection |

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

### Step 4B: Build slides (new build)

**PEDAGOGICAL PRE-CHECK — mandatory before writing any slide:**

For each slide block you are about to build, write a pedagogical intent comment before the HTML:

```html
<!-- PEDAGOGICAL INTENT: [what the student must SEE happen on screen] -->
<!-- WHY THIS FEATURE: [reveal.js feature + why alternatives fail] -->
<!-- FEATURE CHECK: Must pick from [auto-animate | fragments | sibling slides | data-line-numbers | data-mark | data-transition | data-background-gradient | vertical slides | audio | autoslide | code blocks | lightbox | r-fit-text | r-stack | r-stretch | custom-fragment | nested-fragment]. If none fit, state "static — [reason]" -->
<!-- COGNITIVE PRINCIPLE: Must name the principle from Mayer's 12 (e.g. Signaling, Segmenting, Spatial Contiguity, Coherence, Temporal Contiguity, Modality). If none fit, state "none — [explain why]" -->
```

The `FEATURE CHECK` and `COGNITIVE PRINCIPLE` lines are mandatory. They force you to:
1. Explicitly choose a reveal.js feature from the list
2. Justify it against established learning theory

If you keep choosing the same 2-3 features, or cannot name a cognitive principle for a teaching slide, reconsider the design.

**For the full feature lookup table with pedagogical sweet spots, see `docs/pedagogical-design-dictionary.md`.** If you cannot pick a specific feature from that list AND justify why the others don't fit, you have not thought enough about the slide's design. Reconsider.

If you cannot write all three comments, you do not understand what the student needs to learn from this slide. Reconsider the design until you can.

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
- Python handles UTF-8 cleanly (no BOM, no PowerShell encoding corruption)
- The splice is deterministic — finds `<div class="slides">` then anchors on `<!-- Mark.js` to locate the correct closing `</div>`. Never uses `template.find("</div>")` directly — the sections themselves contain `</div>` in answer-list flex rows (`<div class="a-row">...</div>`), and naive `</div>` search causes silent truncation to ~6 slides.
- No size limit concerns — sections and template are written separately

The boilerplate (everything before `<div class="slides">` and everything after the closing `</div>` of the slides div) is always the same. Only the `<section>` elements inside `<!-- SLIDE N -->` comments change per lesson.

#### C. Editing an existing slideshow

When the user asks to modify an already-built slideshow (e.g., "change slide 7" or "add a new slide after the vocabulary"):
1. Read the current `index.html`.
2. Use the `Edit` tool for targeted incremental changes.
3. Use `scripts/locate_slide.py` to find the exact line numbers.

**Rule**: Every slide is a raw `<section>` element inside `<div class="slides">`.

### Step 5: Verify output

**Prefer revealjs-validator over bespoke scripts.** The project includes `revealjs-validator` (npm dev dependency) which checks 66 rules derived from the official Reveal.js docs. Run it in project mode for cross-file validation:

```bash
npx revealjs-validator --project "output/{subfolder}/slides/"
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
- **Answer list sizing**: Count item rows per answer-list. Max 5 items per answer slide. Flag any slide with >5.
- Verify no instructional text like "Click to reveal" appears on slides — answer reveal behavior is self-evident.
- Verify fragment usage: only on answer reveal slides and strategy demonstrations, not on expository content
- Verify procedure text is in `<aside class="notes">`, not on screen
- Verify vocabulary words use `<span class="vocab-word">word</span>`
- Verify title slide has strap subheader (not date/teacher/materials)
- Verify `autoAnimateUnmatched: true` is in `Reveal.initialize()`
- Verify every slide with `data-auto-animate` also has `data-auto-animate-id` — without it, `null === null` causes all auto-animate slides to animate into each other.
- Verify transition slides use `data-background="#c0392b"`
- Verify pedagogical strategy slides use `data-background="#1a6b5a"` and `class="pedagogical"`
- Verify listening task slides that need audio have `data-audio-src="assets/filename.mp3"`
- **Verify no `<section>` has both `data-timer` AND `data-audio-src`** — never place a timer pill on a slide that plays audio or video
- **Verify no raw Unicode check/cross characters**: Scan for U+2713 (✓) and U+2717 (✗) in the output HTML. If found, replace with `<i class="fa-solid fa-check">` and `<i class="fa-solid fa-times">` respectively. Font Awesome renders reliably; Unicode glyphs do not.
- **PEDAGOGICAL INTENT CHECK**: Run `python scripts/check_pedagogical_intent.py --project "output/{subfolder}/slides/"` — verifies every non-exempt slide has mandatory `<!-- PEDAGOGICAL INTENT: -->` and `<!-- WHY THIS FEATURE: -->` annotations. If missing, the slide was built without intentional design and must be fixed.

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
|---|---|---|
| Revealing answers (`a-cor`) | Task instructions |
| Highlighting wrong answers (`a-inc`) | Vocabulary lists |
| Strategy step reveals (on pedagogical slides) | Objectives/outcomes |
| Eliminating wrong MC options (`strike`) | Discussion questions |
| Key vocabulary emphasis (`grow`) | Lead-in images and prompts |
| Temporary hints (`fade-in-then-out`, `current-visible`) | Material references |
| Progressive word focus (custom CSS: blur, rotate, scale) | Any expository content |
| Directional emphasis (`fade-up`, `fade-down`, `fade-left`, `fade-right`) | — |

Fragment classes — available but constrained:

| Class | Behavior | When to use |
|---|---|---|
| `fragment` (bare) | Hidden until click, fades in | Generic answer reveal |
| `fragment fade-up a-ans a-cor` | Hidden until click, slides up + green background on reveal | Correct answer rows (preferred over answer-correct) |
| `fragment fade-up a-ans a-inc` | Hidden until click, slides up + red background on reveal | Incorrect answer rows (preferred over answer-incorrect) |
| `fragment strike` | Always visible, strikethrough on click | Eliminating wrong MC options |
| `fragment grow` | Scales up on click | Emphasizing a single vocabulary word |
| `fragment shrink` | Scales down on click | De-emphasizing a distractor |
| `fragment fade-up / fade-down / fade-left / fade-right` | Slides in from direction while fading | Directional emphasis — draws eye to specific location |
| `fragment fade-in-then-out` | Fades in, then fades out on NEXT click | Temporary scaffolding — hint appears, then disappears |
| `fragment current-visible` | Same as fade-in-then-out | Scaffolding that should vanish |
| `fragment fade-in-then-semi-out` | Fades in, then to 50% opacity | Keeping reference visible without distraction |
| `fragment semi-fade-out` | Fades to 50% opacity | Partially hiding a completed item |
| `fragment highlight-current-red/green/blue` | Temporarily changes color, reverts on NEXT click | Word emphasis without permanent change — SAFE to use |
| `fragment highlight-red/green/blue` | Permanently changes color, forces `opacity: 1` | **AVOID** — cannot hide, content always visible |

**Custom CSS fragments**: Define your own effects. Elements with `class="fragment custom blur"` get no default reveal.js styles — you control everything:

```css
.fragment.blur { filter: blur(5px); }
.fragment.blur.visible { filter: none; }
```

Replace `visible` with `current-fragment` to blur all EXCEPT the current step:

```css
.fragment.blur.current-fragment { filter: none; }
```

**Nested fragments**: Multiple sequential effects on the same element:
```html
<span class="fragment fade-in">
  <span class="fragment highlight-red">
    <span class="fragment fade-out">Fade in → Turn red → Fade out</span>
  </span>
</span>
```


## Pedagogical Design Principles

Before building any slide, you MUST answer these three questions for every student-facing element:

1. **What must the student *see* happen?** The student needs to witness a visual transformation — a word changing color, an answer appearing, a wrong option being eliminated. Slides are not documents; they are moments of revealed understanding.
2. **Which reveal.js feature achieves that?** Consult the **Decision Framework** and **Feature Lookup Table** in `docs/pedagogical-design-dictionary.md`. The table maps every reveal.js feature to a specific pedagogical use case. Do not guess from training data.
3. **Which cognitive principle does this serve?** Every design choice must be justified against established multimedia learning theory (Mayer, Sweller). See `docs/pedagogical-design-dictionary.md` for the complete Mayer's 12 Principles reference table and Decision Framework. If you cannot name the principle, the design may be cosmetic rather than pedagogical.
What must the student see happen?
│
├─ A word/part changes appearance (color, border, strikethrough)?
│   → AUTO-ANIMATE (two consecutive <section> with matching data-id)
│   Example: Subject word turns yellow → student sees WHERE the subject is
│
├─ Content reveals on click (answer appears, step builds)?
│   → FRAGMENTS on a single <section>
│   Example: Answer column appears row by row
│
├─ Each step is a discrete teaching moment (teacher pauses)?
│   → SIBLING SLIDES (one <section> per step, no auto-animate)
│   Example: Strategy demonstration — one slide per step
│
├─ Text needs progressive highlighting within a block?
│   → CODE + DATA-LINE-NUMBERS on <pre><code>
│   Example: Reading passage — highlight key sentence, then details
│
├─ A wrong option gets visually eliminated?
│   → FRAGMENT STRIKE (class="fragment strike")
│   Example: Multiple choice — strike out eliminated answers
│
├─ Items on one side need to reposition to show correct matching?
│   → AUTO-ANIMATE (matching data-id on sibling elements within a shared container)
│   Example: Letters A–F on the left, paragraph numbers on the right. The right-side
│   elements have data-id="p1"…"p8". On the reveal slide they reorder to match the
│   correct letter → paragraph pairing. Auto-animate animates each item sliding to
│   its new position. The transformation IS the answer — no fragments needed.
│   Design rule: do NOT add instructional text ("Click to check", "Click to reveal").
│   The visual rearrangement is self-evident. Unmatched items dim and sink to the bottom.
│
└─ A word needs temporary emphasis (grow, color)?
    → FRAGMENT GROW or FRAGMENT HIGHLIGHT-CURRENT-*
    Example: Key vocabulary word on click
```

### Pedagogical Intent Annotation

Every slide block must be preceded by a comment block explaining the pedagogical goal. This is **mandatory** — it forces intentionality before writing code:

```html
<!-- PEDAGOGICAL INTENT: Student sees the subject word transform from white to yellow. -->
<!-- WHY THIS FEATURE: Auto-animate transforms appearance; fragments only reveal/hide. -->
<!-- COGNITIVE PRINCIPLE: Signaling + Temporal Contiguity —
     highlighting essential material while the label appears simultaneously improves transfer. -->
```

The annotation must state:
- **What visual transformation the student witnesses** (not what the slide *says*, but what *happens* on screen)
- **Why this feature was chosen** (and implicitly, why alternatives would fail)
- **Which cognitive principle it serves** (from the Mayer’s 12 reference table above)

If you cannot write all three, you do not understand what the student needs to learn from this slide. Stop and reconsider the slide design.

### Common Anti-Patterns (DO NOT DO)

See `docs/pedagogical-design-dictionary.md` for the full anti-patterns table. Key ones to avoid:
- `highlight-green`/`highlight-red` — use `a-cor`/`a-inc` with `fragment fade-up` instead
- Putting the answer in the slide title — use a separate answer slide after the task slide
- Instructional text like "Click to check" on auto-animate reveals — the visual transformation IS the answer, no instruction needed

## Slide Type Templates

Full HTML patterns with pedagogical intent annotations live in `templates/base-slides-template.html` as HTML comments. **Copy the pattern, paste it into `<div class="slides">`, and adapt the content.** Do not invent new patterns — use only variants documented there.

Every slide must be preceded by this mandatory comment block:

```html
<!-- PEDAGOGICAL INTENT: [what the student must SEE happen on screen] -->
<!-- WHY THIS FEATURE: [reveal.js feature + why alternatives fail] -->
<!-- COGNITIVE PRINCIPLE: [name the principle from Mayer's 12, or state why it doesn't apply] -->
```

Quick reference of slide types and their pedagogical intent:

| Slide type | Background | Student sees | Feature |
|---|---|---|---|
| Title | `#1a1a2e` | Topic + CEFR + strap | Static — orientation |
| Objective | default | 3 outcomes (full visibility) | Static — orientation |
| Vocabulary | `#1a1a2e` | One word + IPA + context | Static — focus |
| Lead-in | `#1a1a2e` | One open question | Static — activation |
| Transition | `#c0392b` | Heading only, phase signal | Static — rest |
| Teach (sentence/grammar) | `#1a6b5a` | Word/part transforms (color, border, highlight) | Auto-animate — transformation |
| Teach (rules/reference) | `#1a6b5a` | Rules in 2-column table (Rule | Example) | Static — reference |
| Strategy (step-by-step) | `#1a6b5a` | Each step is one slide | Sibling slides — discrete teaching |
| Task instruction | dark + timer | Instructions full-visible | Static — orientation |
| Answer (T/F, MC) | `#1e7e34` | Statements visible; answers reveal per-row | Fragment on `<span>` inside `<td>` |
| Summary | default | "I can..." checkmarks | Static — consolidation |
| End | `#2c3e50` | Topic + CEFR | Static — exit |

**CRITICAL — Answer list sizing**: Max 5 items per answer-list slide. If an exercise has more than 5 items, split across multiple answer-list slides. Use `data-fragment-index` for per-row reveal coordination if needed. Fragment classes go on `<span class="a-ans">`, never on the `<div class="a-row">` itself.

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
<section id="slide-lead-in" data-background="#1a1a2e">
```
To locate a slide by its stable ID:
```bash
python scripts/locate_slide.py --id slide-objective --html path/to/slides/index.html
```
Use kebab-case names matching the slide function (e.g., `slide-title`, `slide-objective`, `slide-lead-in`, `slide-test1-1-3`, `slide-p7-corrected-1-3`, `slide-summary`).

## Key Design Rules

1. **Student-facing content on screen only** — task instructions, questions, vocabulary, answers. Teacher procedure text goes in `<aside class="notes">`. "Ss" is never used on screen.
2. **Objective slide uses accessible language** — avoid complex words like "identify", "distinguish", "inference". Use simple phrases. Tie outcomes to PET reading test.
3. **Title slide: topic + CEFR badge + strap subheader** — NO date, teacher name, duration, or materials.
4. **Task slides: brief student instructions** — extract task description from procedure, skip teacher-only instructions. Max 3 task lines on screen.
5. **Stage names: student-friendly language** — "Lead-in" → "Let's get Started", "Reading for gist" → "What's the main idea?", "Reading for detail" → "Finding details", "Reading for inference" → "Making conclusions", "Post-reading" → "Let's Discuss", "Wrap-up" → "Let's Review"
6. **Vocabulary slides** — generated AFTER lead-in stage. One word per slide with dark navy background. "Important Words" title on first slide only. Yellow bold (#ffdd00) via `<span class="vocab-word">`.
7. **Answer slides** — use `<div class="answer-list">` flex layout (NOT `<table class="answer-table">`). Green background `#1e7e34`. Statements visible on entry. Structure each row as:
    ```html
    <div class="a-row">
        <span class="a-num">#</span>
        <span class="a-q">Statement text</span>
        <span class="fragment fade-up a-ans a-cor"><i class="fa-solid fa-check"></i> Answer</span>
    </div>
    ```
    - `a-cor` for correct answers, `a-inc` for incorrect (not `answer-correct`/`answer-incorrect`)
    - `fragment fade-up` for animated reveal (not bare `fragment`)
    - Font Awesome `fa-check`/`fa-times` for icons (never raw Unicode U+2713/U+2717)
    - **Do NOT use `highlight-green`/`highlight-red`** (reveal.js keeps them at `opacity: 1`; they never hide)
    - **CRITICAL — Green slide text: only white `#fff` or yellow `#ffdd00` allowed.** Gray, blue, or any muted color is invisible at projection distance. Never use any other color on `#1e7e34` slides.
8. **Transition slides: heading only (no subheader text).** The red background + icon + heading is sufficient — the teacher's spoken introduction bridges the gap. Remove all `<p>` elements from transition slides.
9. **Backgrounds**: dark navy `#1a1a2e` (title, lead-in, vocabulary), red `#c0392b` (transitions), teal `#1a6b5a` (pedagogical/strategy), green `#1e7e34` (answer tables), dark `#2c3e50` (end)
10. **Title slide visuals**: Use `r-stack` layout with a themed Pixabay image. No logo on title slides. See Step 3 for layout patterns.
11. **Text highlighting**: white text, dark text-shadow, pedagogical sections use white-on-teal
12. **Vocabulary words**: yellow boldface (`#ffdd00`) via `<span class="vocab-word">` — in both the word heading AND context sentence
13. **Timer pill vs audio**: Never add `data-timer` to a slide that also has `data-audio-src`. Slides with audio playback should not have a timer pill — the two controls conflict visually and functionally.
14. **Proper HTML lists for letters/numbers**: Never use manual lettering or numbering in `<p>` tags (e.g., `<p><strong>A</strong> Option text</p>`). Use semantically correct HTML lists instead: `<ol type="A">` for lettered options, `<ol>` for numbered items, `<ul>` for bullet points. Each item gets its own `<li>` element. This ensures proper alignment and accessibility.
15. **Check/cross symbols: Font Awesome only, never Unicode**: Check marks (✓) and cross marks (✗) must use Font Awesome icons `<i class="fa-solid fa-check">` and `<i class="fa-solid fa-times">` — never raw Unicode characters U+2713 and U+2717. These Unicode characters do not render reliably across all browser/system font combinations. Font Awesome is loaded in the base template via CDN and renders consistently in every browser. Use `style="color:#4caf50;"` on check marks and `style="color:#ff5252;"` on cross marks for dark/teal/white backgrounds. On green `#1e7e34` answer slides, use `style="color:#fff;"` for both (only white or yellow allowed on green backgrounds per rule 7).
## Authorial Voice & Audience

This skill generates slides for **Thai secondary students (CEFR A2–B2)**. The default voice targets **B1** (Mathayom 2-3). All student-facing text on screen MUST follow these rules, with level-appropriate relaxations noted.

### Baseline (Applies to all CEFR levels)

#### 1. Person Rule
All on-screen student-facing text MUST use **direct "you" imperatives**, never third person:

| Wrong | Correct |
|-------|---------|
| "Students read the article again..." | "Read the article again." |
| "They must correct the false statements." | "Correct the false statements." |
| "Ss complete the task individually." | "Complete the task on your own." |

**`<aside class="notes">` remains unrestricted** — teacher procedure can use full professional vocabulary.

#### 2. Person Rule
- Collective framing: "We can see...", "Our class can think about..."
- Positive, concrete questions — avoid abstract philosophical prompts
- Group participation questions, not individual introspection

#### 3. No Automatic Image Downloads
When regenerating slides, **do not auto-download images**. Start with solid theme colors. Use gradients, images, or videos only when the teacher provides assets or when they serve a clear pedagogical purpose. Never fetch images independently.

### B1 Default (Mathayom 2-3)

#### Vocabulary Ceiling
No words above CEFR B1 on screen without inline definition:
- "identify" → use "find"
- "predict" → use "guess"
- "convincing" → use "makes sense"
- "distinguish" → use "tell the difference"
- "evaluate" → use "decide"
- "analyze" → use "look at carefully"
- "infer" → use "understand what the writer means"

#### Sentence Complexity
- Max 15 words per sentence on screen
- No semicolons — break into two sentences
- One clause preferred, two max
- No passive voice on screen

#### Summary: "I Can" Statements
| Wrong | Correct |
|-------|---------|
| "Identify the main purpose" | "I can find the main idea" |
| "Find key facts" | "I can find important facts" |
| "Express opinions" | "I can share my ideas" |

### B2 Adaptation (for higher-level classes)

When the lesson targets B2 learners, relax the B1 rules as follows:

- **Vocabulary ceiling**: academic words (identify, evaluate, analyze) may appear but must be defined or exemplified on screen
- **Sentence complexity**: max 20 words per sentence; semicolons OK for contrast
- **Summary**: may use slightly more specific outcomes (e.g., "I can use correct subject-verb agreement when a prepositional phrase separates subject and verb")
- **All other rules remain** (person rule, no auto-download, collective framing)

## reveal.js Feature Lookup

See the complete Decision Framework, Feature Lookup Table, Mayer's 12 Principles, and Common Anti-Patterns in `docs/pedagogical-design-dictionary.md`.

**Key decision rule**: Auto-animate for transformations — color changes, border reveals, word replacement, and element repositioning (items reordering within a container to show correct matching). Fragments for reveals — answers appearing, options being eliminated. Sibling slides for discrete teaching moments — each step is its own slide where the teacher pauses.

## Pedagogical Strategy Slides

See AGENTS.md (`Pedagogical Strategy Slides — Design Principles`) for the full SBI design framework. Key rules for this project:
- **One consistent worked example** per strategy block — carry one exam item through all steps
- **One step per slide** — each `<section>` covers a single step so the teacher can pause
- **Step label format**: `<u><strong>Step N:</strong> description</u>`
- **Header on first slide only**, remaining slides show only the step label
- **Auto-animate for keyword underlines**: use `<span data-id="...">` with transparent→visible border transitions across consecutive `<section data-auto-animate>` siblings
- **Teal background**: `data-background="#1a6b5a"` + `class="pedagogical"` on all strategy slides
- **Top alignment**: CSS `.reveal .slides > section.pedagogical { align-self: flex-start; padding-top: 30px; }`

## Common Pitfalls

### Plugin safety protocol

Adding a plugin to the base template's `plugins` array can cause a silent blank page if the plugin's `init()` fails. Protocol:
1. **Add to the `plugins` array LAST** — build and test WITHOUT the new plugin first
2. **Add one plugin at a time** — never add multiple untested plugins simultaneously
3. **Test in browser** — open slides, `F12` → Console tab. Verify: page shows content, zero red errors, navigation works
4. **Isolate on failure** — if page is blank, remove ALL recently added plugins, re-add one at a time

### Temp file workflow (proven pattern)

The ONLY reliable approach given Windows tooling constraints:
1. **Write slide sections** to `C:\Users\elwru\AppData\Local\Temp\kilo\slides_sections.html` via the Write tool
2. **Copy template** to output dir via PowerShell `cp`
3. **Write splice script** to `C:\Users\elwru\AppData\Local\Temp\kilo\splice_slides.py`
4. **Run splice script** via `python ...\splice_slides.py`
5. **Write verification script** to `C:\Users\elwru\AppData\Local\Temp\kilo\verify_slides.py`
6. **Clean up** temp files only after verification passes

**Do NOT:** Write large files (>300 lines) directly via Write tool to `output/` — may hit permission blocks. Use PowerShell `>`, `Out-File`, or `Set-Content` for files with Unicode — they add BOM or corrupt codepoints.

### Answer-list CSS alignment traps

The answer-list flex layout has three CSS properties that, if set incorrectly, break left-alignment. All three must be set correctly in the inline `<style>` block (Step 2b):

| Element | Correct value | Wrong value | What breaks |
|---------|--------------|-------------|-------------|
| `.a-num` | `text-align: left` | `text-align: right` | Number pushes away from text |
| `.a-q` | `flex: 0 0 auto` | `flex: 1 1 auto` | Question fills all space, answer pinned to far right |
| `.a-ans` | `flex: 1 1 auto; min-width: 0` | `flex: 0 0 auto; min-width: 160px` | Answer pinned to far right with fixed width |

**Rule of thumb:** The answer-list should read left-to-right naturally, like a sentence: `[1] [anxious →] [d — worried because...]`. If any column looks separated or floating on the right, check these three CSS values.

**Also verify the inline `<style>` block is present** — if the template CSS bug (missing `}` in `.cefr-badge`) broke the cascade, the flex rules may not apply at all, causing the browser to fall back to default inline layout (which looks broken). Step 2b is mandatory, not optional.

### Gray text on green `#1e7e34` answer slides

The base template defines `.reveal .aim-label { color: #888; }`. Gray `#888` text is **invisible at projection distance** on `#1e7e34` green backgrounds. The skill rule allows only white `#fff` or yellow `#ffdd00` on green slides.

The inline `<style>` block from Step 2b MUST include this override:
```css
.reveal .aim-label { color: rgba(255,255,255,0.7); }
```

Without it, every `class="aim-label"` on an answer slide renders as unreadable gray text. This applies to ALL text on green slides — not just `.aim-label`. If you add any other text elements (paragraphs, spans, etc.) on a `#1e7e34` slide, they must also use white or yellow. Gray, blue, or muted colors fail at projector brightness.

## Files

| File | Purpose |
|---|---|
| `docs/slide-design-reference.md` | Slide design rules (authoritative) — consult before building |
| `docs/pedagogical-design-dictionary.md` | Decision Framework, Feature Lookup Table, Mayer's 12 Principles, Anti-Patterns |
| `templates/base-slides-template.html` | Base template for ALL new presentations |
| `scripts/locate_slide.py` | Map reveal.js URL index to HTML section |
| `scripts/pixabay_download.py` | Pixabay image downloader |
| `templates/ACT.png` | Institution logo — copy to `assets/logo.png` |

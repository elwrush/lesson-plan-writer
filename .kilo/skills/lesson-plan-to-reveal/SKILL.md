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

## When to Use This Skill

Use `lesson-plan-to-reveal` when converting a lesson plan JSON to slides. The skill:
1. Copies the institution logo into `output/{subfolder}/slides/assets/`
2. Copies `templates/base-slides-template.html` to `output/{subfolder}/slides/index.html`
3. Builds slides one by one as raw HTML `<section>` elements, inserting them between `<div class="slides">` and `</div>`
4. Reports the output path

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

### Step 2: Copy supporting files (timer plugin, logo)

```powershell
cp "templates/timer-plugin.js" "output/{subfolder}/slides/timer-plugin.js"
cp "templates/timer-plugin.css" "output/{subfolder}/slides/timer-plugin.css"
cp "templates/ACT.png" "output/{subfolder}/slides/assets/logo.png"
```

### Step 3: Background images

**Do NOT download Pixabay images.** The user adds custom screenshot backgrounds manually after the slides are produced. All slide backgrounds use solid theme colors only.

Background color reference:
| Slide type | Background |
|---|---|
| Title, lead-in, general content | `#1a1a2e` (dark navy/black) |
| Transition (forward to next stage) | `#c0392b` (red) |
| Pedagogical/strategy blocks | `#1a6b5a` (teal) |
| Answer tables | `#1e7e34` (green) |
| Summary | white (default) |
| End | `#2c3e50` (dark blue-gray) |

Pixabay background images (`data-background-image`, `data-background-opacity`) are NEVER used in generated output. All backgrounds use `data-background="<color>"`.

### Step 4: Build slides

There are two distinct workflows depending on the situation:

#### A. New build (first generation from JSON)

**Always write the entire `index.html` in a single Write tool call.** Do NOT copy the template and then incrementally replace sections with Edit tool calls — this is slow, fragile, and causes timeouts.

Instead:
1. Read `templates/base-slides-template.html` once to get the `<head>`, `<style>`, `<body>`, and `<script>` boilerplate.
2. Compose all `<section>` elements in memory.
3. Write the complete file in one `Write` call to `output/{subfolder}/slides/index.html`.
4. Then verify the output (Step 5).

The boilerplate (lines 1-136 and lines 358-390 of the template) is always the same. Only the `<section>` elements inside `<div class="slides">` change per lesson.

#### B. Editing an existing slideshow

When the user asks to modify an already-built slideshow (e.g., "change slide 7" or "add a new slide after the vocabulary"):
1. Read the current `index.html`.
2. Use the `Edit` tool for targeted incremental changes.
3. Use `scripts/locate_slide.py` to find the exact line numbers.

**Rule**: Every slide is a raw `<section>` element inside `<div class="slides">`.

**Slide ordering convention**:
1. Title (with logo)
2. Objective (3 outcomes, all visible)
3. Lead-in (open question)
4. Vocabulary (one slide per word, AFTER lead-in)
5. Transition (red background, directive + foreshadow)
6. Strategy block (auto-animate or pedagogical, if applicable)
7. Task instruction (with timer)
8. Answer slides (fragment reveals)
9. (Repeat 5-8 for each reading stage)
10. Transition → Post-reading discussion
11. Transition → Wrap-up
12. Summary ("What you can do now")
13. End slide

### Step 5: Verify output
- Check `index.html` exists in the slides directory
- Check `timer-plugin.js` and `timer-plugin.css` exist in the slides directory
- Verify title slide contains `<img src="assets/logo.png" class="title-logo" />`
- Verify `TimerPlugin` is in the `plugins` array of `Reveal.initialize()`
- Verify `answer-correct` / `answer-incorrect` are used for answer fragments (NOT `highlight-green`/`highlight-red`)
- Verify fragment usage: only on answer reveal slides and strategy demonstrations, not on expository content
- Verify procedure text is in `<aside class="notes">`, not on screen
- Verify vocabulary words use `<span class="vocab-word">word</span>`
- Verify title slide has strap subheader (not date/teacher/materials)
- Verify `autoAnimateUnmatched: true` is in `Reveal.initialize()`
- Verify transition slides use `data-background="#c0392b"`
- Verify pedagogical strategy slides use `data-background="#1a6b5a"` and `class="pedagogical"`
- Verify listening task slides that need audio have `data-audio-src="assets/filename.mp3"`
- **Verify no `<section>` has both `data-timer` AND `data-audio-src`** — never place a timer pill on a slide that plays audio or video

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
| Revealing answers (`answer-correct`) | Task instructions |
| Highlighting wrong answers (`answer-incorrect`) | Vocabulary lists |
| Strategy step reveals (on pedagogical slides) | Objectives/outcomes |
| Eliminating wrong MC options (`strike`) | Discussion questions |
| Key vocabulary emphasis (`grow`, single word) | Lead-in images and prompts |
| | Material references |
| | Any expository content |

Fragment classes:
- `fragment answer-correct` — correct answer revealed (hidden until click, green background on reveal)
- `fragment answer-incorrect` — incorrect answer revealed (hidden until click, red background on reveal)
- `fragment highlight-green` — **DO NOT USE** (reveal.js built-in forces `opacity: 1`, prevents hiding)
- `fragment highlight-red` — **DO NOT USE** (same reason as above)
- `fragment strike` — eliminated wrong answer (always visible, strikethrough on click)
- `fragment grow` — emphasize single vocabulary word
- `fragment` (bare) — generic reveal

## Slide Icons — Font Awesome 6

Every slide type gets a **function-icon** that signals its role (not its topic). Icons are centered at the top, above the heading, using Font Awesome 6 via CDN. The CDN is already in `templates/base-slides-template.html`.

**Icon CSS** (in template):
```css
.slide-icon {
    font-size: 2.5em;
    margin-bottom: 0.3em;
    display: block;
    text-align: center;
}
.transition-icon  { color: rgba(255,255,255,0.85); }  /* #c0392b slides */
.pedagogical-icon { color: rgba(255,255,255,0.9);  }  /* #1a6b5a slides */
.objective-icon   { color: rgba(255,221,0,0.85);    }  /* white slides    */
```

**Icon mapping** — one icon on the first slide of each block, before the `<h2>`:

| Slide / Block | Icon | CSS class | Background |
|---|---|---|---|
| Objective | `fa-seedling` | `objective-icon` | white |
| Lead-in | `fa-eye` | inherit | `#1a1a2e` |
| Vocabulary (first word) | `fa-spell-check` | inherit | `#1a1a2e` |
| Transition | `fa-forward` | `transition-icon` | `#c0392b` |
| Strategy block header | `fa-list-check` | `pedagogical-icon` | `#1a6b5a` |
| Strategy step slides | `fa-chess` | `pedagogical-icon` | `#1a6b5a` |
| Task instruction | `fa-pencil` | inherit | white |
| Discussion | `fa-comments` | `transition-icon` | `#c0392b` |
| Summary | `fa-flag-checkered` | inherit | white |
| End | `fa-star` | inherit | `#2c3e50` |

**Example — Objective slide:**
```html
<section>
    <i class="fa-solid fa-seedling slide-icon objective-icon"></i>
    <h2>Here's what you'll be able to do</h2>
    ...
</section>
```

**Example — Transition slide:**
```html
<section data-background="#c0392b">
    <i class="fa-solid fa-forward slide-icon transition-icon"></i>
    <h2>Finding details</h2>
    ...
</section>
```

**Example — Strategy block header:**
```html
<section class="pedagogical" data-background="#1a6b5a" data-background-transition="none" style="top: 0;">
    <i class="fa-solid fa-list-check slide-icon pedagogical-icon"></i>
    <h2>True/False Strategy</h2>
    ...
</section>
```

Only the **first slide** of a strategy block gets the icon. Steps 2–4 do not repeat it — the teacher and students see the icon once as the block begins.

## Slide Type Templates (Raw HTML)

All patterns live in `templates/base-slides-template.html` as HTML comments. **Copy the pattern, paste it into `<div class="slides">`, and adapt the content.** Do not invent new patterns — only use variants of the ones documented here.

### 1. Title Slide
```html
<section data-background="#1a1a2e">
    <img src="assets/logo.png" class="title-logo" alt="Logo" />
    <h1>Topic Title <span class="cefr-badge B1">B1</span></h1>
    <p><em>Strap subheader — derived from lesson objective</em></p>
</section>
```
- CEFR badge colors: A1=green, A2=light green, B1=blue, B2=dark blue, C1=purple, C2=red
- Strap is derived from the lesson objective using natural teacher voice
- NO date, teacher name, duration, or materials on title slide
- Logo: `assets/logo.png`, max-height 100px (set in CSS)

### 2. Objective Slide
```html
<section>
    <h2>Here's what you'll be able to do</h2>
    <ul>
        <li>Understand what the article is mainly about</li>
        <li>Find the most important facts and mistakes</li>
        <li>Share your ideas with a partner</li>
    </ul>
    <p><em>These are the same skills you need for the PET reading test!</em></p>
</section>
```
- 3 outcomes max, each ≤10 words
- NO fragments — students see this as orientation
- Tie to PET reading test where applicable

### 3. Vocabulary Slides (one word per slide)
```html
<!-- First word (with header) -->
<section class="vocab-slide" data-background="#1a1a2e">
    <h2>Important Words</h2>
    <p><span class="vocab-word">generation gap</span></p>
    <p><em>/ˌdʒenəˈreɪʃn ɡæp/</em></p>
    <p><em>There is a big <span class="vocab-word">generation gap</span> between old people and young people.</em></p>
</section>

<!-- Subsequent words (no header) -->
<section class="vocab-slide" data-background="#1a1a2e">
    <p><span class="vocab-word">frustration</span></p>
    <p><em>/frʌˈstreɪʃn/</em></p>
    <p><em>I felt <span class="vocab-word">frustration</span> when my phone died.</em></p>
</section>
```
- **One word per slide** — max 5 words total
- `<span class="vocab-word">` renders yellow (#ffdd00) bold
- Word + phonemic script (IPA) + context sentence with word highlighted
- **Sentence must imply meaning, NOT define** — e.g., "There's such a **generation gap** between them" (GOOD) vs "generation gap — the difference between groups" (BAD)
- Background: `#1a1a2e`
- Class: `vocab-slide`

### 4. Lead-in Slide
```html
<section data-background="#1a1a2e">
    <h2>Let's get Started</h2>
    <h3>What do these two people have in common?</h3>
    <aside class="notes">
        Display the photo. Give students 20 seconds to look silently.
        Then ask the question. Elicit 3-4 responses.
        Connect responses to today's topic.
    </aside>
</section>
```
- One open question only
- Speaker notes in `<aside class="notes">`

### 5. Transition Slide (red background)
```html
<section data-background="#c0392b">
    <i class="fa-solid fa-forward slide-icon transition-icon"></i>
    <h2>Finding details</h2>
</section>
```
- Red background `#c0392b`
- **Heading only** — no subheader text or descriptive paragraphs. The teacher's spoken introduction bridges the gap. All `<p>` elements removed.
- Icon: `fa-forward` (or `fa-comments` for discussion transitions)

### 6. Auto-Animate Strategy Block
```html
<section data-auto-animate data-auto-animate-id="tf-strategy" class="pedagogical" data-background="#1a6b5a">
    <h2>True/False Strategy</h2>
    <p><strong>Step 1:</strong> Read the statement carefully</p>
    <p><em>Statement text goes here.</em></p>
</section>
<section data-auto-animate data-auto-animate-id="tf-strategy" class="pedagogical" data-background="#1a6b5a">
    <h2>True/False Strategy</h2>
    <p><strong>Step 1:</strong> Read the statement carefully</p>
    <p><em>Statement text goes here.</em></p>
    <p><strong>Step 2:</strong> Find the keywords</p>
    <p>"keyword1" · "keyword2" · "keyword3"</p>
</section>
<!-- ... up to 5 slides, each adding one more step ... -->
<section data-auto-animate data-auto-animate-id="tf-strategy" class="pedagogical" data-background="#1a6b5a">
    <h2>True/False Strategy</h2>
    <!-- ... all previous steps ... -->
    <p class="fragment highlight-green">TRUE — Explanation of why it's true.</p>
</section>
```
**Critical rules for auto-animate:**
- All sections in one auto-animate block MUST be **consecutive siblings** in `<div class="slides">` — no other sections between them
- `data-auto-animate-id` MUST match across all sections in the block (e.g., `"tf-strategy"`)
- Each section builds on the previous one by adding new elements
- Use `data-auto-animate` (not `data-auto-animate-unmatched`) — `autoAnimateUnmatched: true` in Reveal.initialize handles unmatched elements
- All sections in the block share `class="pedagogical"` and `data-background="#1a6b5a"`
- The final section may include a `fragment highlight-green` for the answer reveal
- Auto-animate sections CANNOT be placed inside `<section data-markdown>` — this is the core reason markdown was abandoned

### 7. Task Instruction Slide
```html
<section data-timer="960">
    <h2>Finding details</h2>
    <ul>
        <li>Read the article again and complete the true/false task.</li>
        <li>Complete the paragraph matching task.</li>
    </ul>
    <aside class="notes">
        Stage 3 · 16 min · Ss-Ss
        Goal: To identify key facts and supporting details
        Materials: Student Book, pp 5-6
    </aside>
</section>
```
- `data-timer="seconds"` — time in seconds (minutes × 60)
- Brief student-facing instructions (max 3 bullet points)
- Full procedure, timing, and materials in `<aside class="notes">`
- **Listening task slides** that play an audio track should also add `data-audio-src="assets/filename.mp3"` on the `<section>` element
- **Never combine `data-timer` and `data-audio-src` on the same `<section>`** — timer pills conflict with audio playback. Use one or the other, not both.

### YouTube / Iframe Embedding

YouTube requires a valid `HTTP Referer` header for embedded players. Without it, YouTube returns Error 153. Use `referrerpolicy="strict-origin-when-cross-origin"` on the iframe to ensure the browser sends the referrer.

```html
<section data-background="#1a1a2e">
    <h2>Video Title</h2>
    <iframe
        width="760" height="430"
        src="https://www.youtube.com/embed/VIDEO_ID"
        frameborder="0"
        allowfullscreen
        referrerpolicy="strict-origin-when-cross-origin"
        style="border: none; display: block; margin: 0 auto;">
    </iframe>
    <p><em>Discussion prompt below the video.</em></p>
</section>
```

**Rules:**
- Use `src` directly (not `data-src`) — the iframe loads immediately. Reveal.js will auto-detect the YouTube URL and manage pause-on-navigate-away via postMessage.
- `referrerpolicy="strict-origin-when-cross-origin"` — REQUIRED. Without this, YouTube blocks the embed when the page is served from `file://` or any context without a default referrer.
- Also add `<meta name="referrer" content="strict-origin-when-cross-origin" />` inside `<head>` as a page-wide fallback for any other embedded resources that need a referrer.
- `allowfullscreen` enables the YouTube fullscreen button.
- Do NOT add `data-timer` to a slide that has a YouTube iframe.
- Background: `#1a1a2e` (dark navy).

### Diagnostic Talk Structure Slide

For teaching students how to structure a short talk (thesis → reasons → example):

```html
<section class="pedagogical structure-talk" data-background="#1a6b5a" data-background-transition="none" style="top: 0;">
    <h2>Structure Your Talk</h2>
    <p class="structure-step"><u><strong>Thesis:</strong> Say your main idea</u></p>
    <p class="structure-step"><u><strong>Reasons:</strong> Give 1-2 reasons</u></p>
    <p class="structure-step"><u><strong>Example:</strong> Share an example you know</u></p>
    <p class="transition-words">First... &nbsp; Also... &nbsp; For example...</p>
</section>
```

- Teal background `#1a6b5a`, `class="pedagogical structure-talk"`
- Three underlined steps teaching basic argument structure
- Yellow transition word box at bottom: First / Also / For example

### 8. Pedagogical Strategy Slide (non-auto-animate)
```html
<section class="pedagogical" data-background="#1a6b5a">
    <h2>Multiple Choice Strategy</h2>
    <p><strong>Step 1: Read all options first</strong> <span class="fragment"> — look at all three choices</span></p>
    <ul class="fragment">
        <li>a) Option A text</li>
        <li>b) Option B text</li>
        <li>c) Option C text</li>
    </ul>
    <p class="fragment"><strong>Step 2: Eliminate wrong answers</strong></p>
    <p class="fragment strike">a) Reason. <strong>Eliminate.</strong></p>
    <p class="fragment strike">b) Reason. <strong>Eliminate.</strong></p>
    <p class="fragment"><strong>Step 3: Confirm the answer</strong></p>
    <p class="fragment answer-correct">c) Explanation. ✓ <strong>c is correct!</strong></p>
</section>
```
- Teal background `#1a6b5a` via `data-background`
- `class="pedagogical"` for white text styling
- Fragments used for step-by-step reveal of strategy

### 9. Answer Slide (True/False)

Use the same `answer-table` pattern with green background and fragment reveals:

```html
<section data-background="#1e7e34">
    <h2>Exercise N — Answers</h2>
    <p class="aim-label">True/False</p>
    <table class="answer-table">
        <thead><tr><th>Statement</th><th>Answer</th></tr></thead>
        <tbody>
            <tr><td>Statement text here.</td><td class="fragment answer-correct">✓ <strong>True</strong></td></tr>
            <tr><td>Another statement.</td><td class="fragment answer-incorrect">✗ <strong>False</strong></td></tr>
            <tr><td>Corrected statement.</td><td class="fragment answer-correct">✓ <em>Explanation</em></td></tr>
        </tbody>
    </table>
</section>
```
- **Statements visible at slide entry** — teacher and students see all questions immediately
- **Answer column uses `class="fragment answer-correct"` or `class="fragment answer-incorrect"`** — revealed one row at a time
- `answer-correct` = green background on reveal, `answer-incorrect` = red background on reveal
- **Do NOT use `highlight-green`/`highlight-red`** — reveal.js built-in classes force `opacity: 1`, preventing fragment hiding
- For 3-column tables with explanations, add a `Why?` column (see Answer Table Patterns below)

### 10. Answer Slide (Multiple Choice / Matching)

```html
<section data-background="#1e7e34">
    <h2>Exercise N — Answers</h2>
    <p class="aim-label">Multiple Choice</p>
    <table class="answer-table">
        <thead><tr><th>Question</th><th>Answer</th><th>Why?</th></tr></thead>
        <tbody>
            <tr><td>Question text</td><td class="fragment answer-correct">✓ <strong>c) Option C</strong></td><td class="fragment">citation from text</td></tr>
        </tbody>
    </table>
</section>
```
- **Questions/options visible at slide entry** — students see all choices
- **Answer and Why columns are fragments** — revealed one row at a time via clickthrough

### 11. Summary Slide
```html
<section>
    <h2>What you can do now</h2>
    <ul>
        <li>✓ I can find the main idea</li>
        <li>✓ I can find important facts</li>
        <li>✓ I can share my ideas</li>
    </ul>
    <aside class="notes">
        Elicit from students: What did you learn today?
        Connect back to their predictions from the beginning.
        Praise effort, mention one thing to improve.
    </aside>
</section>
```
- 3 "I can..." outcomes with checkmarks
- Speaker notes: elicitation script

### 12. End Slide
```html
<section data-background="#2c3e50">
    <h2>Thank you</h2>
    <p><em>Topic Name</em> | B2</p>
</section>
```
- Dark background `#2c3e50`

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
5. **When adding a new slide**, insert a new `<section>` element at the correct position in `<div class="slides">`. Shift all subsequent slide indices by +1.

## Key Design Rules

1. **Student-facing content on screen only** — task instructions, questions, vocabulary, answers. Teacher procedure text goes in `<aside class="notes">`. "Ss" is never used on screen.
2. **Objective slide uses accessible language** — avoid complex words like "identify", "distinguish", "inference". Use simple phrases. Tie outcomes to PET reading test.
3. **Title slide: topic + CEFR badge + strap subheader** — NO date, teacher name, duration, or materials.
4. **Task slides: brief student instructions** — extract task description from procedure, skip teacher-only instructions. Max 3 task lines on screen.
5. **Stage names: student-friendly language** — "Lead-in" → "Let's get Started", "Reading for gist" → "What's the main idea?", "Reading for detail" → "Finding details", "Reading for inference" → "Making conclusions", "Post-reading" → "Let's Discuss", "Wrap-up" → "Let's Review"
6. **Vocabulary slides** — generated AFTER lead-in stage. One word per slide with dark navy background. "Important Words" title on first slide only. Yellow bold (#ffdd00) via `<span class="vocab-word">`.
7. **Answer slides** — use `<table class="answer-table">` with green background `#1e7e34`. Statements visible on entry; answers use `class="fragment answer-correct"` or `class="fragment answer-incorrect"` for clickthrough reveal. **Do NOT use `highlight-green`/`highlight-red`** (reveal.js keeps them at `opacity: 1`; they never hide).
8. **Transition slides: heading only (no subheader text).** The red background + icon + heading is sufficient — the teacher's spoken introduction bridges the gap. Remove all `<p>` elements from transition slides.
9. **Backgrounds**: dark navy `#1a1a2e` (title, lead-in, vocabulary), red `#c0392b` (transitions), teal `#1a6b5a` (pedagogical/strategy), green `#1e7e34` (answer tables), dark `#2c3e50` (end)
10. **Logo**: `assets/logo.png`, transparent RGBA PNG, max-height 100px, centered
11. **Text highlighting**: white text, dark text-shadow, pedagogical sections use white-on-teal
12. **Vocabulary words**: yellow boldface (`#ffdd00`) via `<span class="vocab-word">` — in both the word heading AND context sentence
13. **Timer pill vs audio**: Never add `data-timer` to a slide that also has `data-audio-src`. Slides with audio playback should not have a timer pill — the two controls conflict visually and functionally.
14. **Proper HTML lists for letters/numbers**: Never use manual lettering or numbering in `<p>` tags (e.g., `<p><strong>A</strong> Option text</p>`). Use semantically correct HTML lists instead: `<ol type="A">` for lettered options, `<ol>` for numbered items, `<ul>` for bullet points. Each item gets its own `<li>` element. This ensures proper alignment and accessibility.
## Authorial Voice & Audience

This skill generates slides for **Mathayom 2-3 Thai students (CEFR B1)**. All student-facing text on screen MUST follow these rules:

### 1. Person Rule
All on-screen student-facing text MUST use **direct "you" imperatives**, never third person:

| Wrong | Correct |
|-------|---------|
| "Students read the article again..." | "Read the article again." |
| "They must correct the false statements." | "Correct the false statements." |
| "Ss complete the task individually." | "Complete the task on your own." |

**`<aside class="notes">` remains unrestricted** — teacher procedure can use full professional vocabulary.

### 2. B1 Vocabulary Ceiling
No words above CEFR B1 on screen without inline definition:
- "identify" → use "find"
- "predict" → use "guess"
- "convincing" → use "makes sense"
- "distinguish" → use "tell the difference"
- "evaluate" → use "decide"
- "analyze" → use "look at carefully"
- "infer" → use "understand what the writer means"

### 3. Sentence Complexity
- Max 15 words per sentence on screen
- No semicolons — break into two sentences
- One clause preferred, two max
- No passive voice on screen

### 4. Thai L1 Considerations
- Collective framing: "We can see...", "Our class can think about..."
- Positive, concrete questions — avoid abstract philosophical prompts
- Group participation questions, not individual introspection

### 5. Summary: "I Can" Statements
| Wrong | Correct |
|-------|---------|
| "Identify the main purpose" | "I can find the main idea" |
| "Find key facts" | "I can find important facts" |
| "Express opinions" | "I can share my ideas" |

### 6. Transition Slides: Directive + Foreshadow + Engagement
| Old (reflective) | New (directive + foreshadow + engage) |
|-------------------|---------------------------------------|
| "What's the idea?" | "WHAT'S THE MAIN IDEA? Look at the main reading. What do you think the text is about?" |
| "What did you learn?" | "We're now going to read in more detail. Let's start with True/False questions. They may look easy, but they can have some surprises!" |

### 7. No Automatic Image Downloads
When regenerating slides, **do not download images**. All backgrounds use solid theme colors only.

## Auto-Animate vs. Simple Slides for Strategy Blocks

**For step-by-step strategy teaching (SBI), prefer simple slides without auto-animate.**

Use separate `<section>` elements with `data-background-transition="none"` — one step per slide. Teacher advances manually, pausing at each decision point. This is more effective than auto-animate for pedagogical slides because:

1. Each step is a discrete teaching moment
2. Teacher controls pacing, not the animation
3. No content disappears mid-step (avoids negative-margin clipping issues)

Use auto-animate only when the strategy block is a quick demonstration, not explicit instruction.

**Rules for simple (non-auto-animate) pedagogical slides:**
- Each step = one `<section>` with `class="pedagogical"` and `data-background="#1a6b5a"`
- All sections: `data-background-transition="none"` (prevents flash of color on entry)
- Inline `style="top: 0;"` on each section to prevent vertical centering issues
- Step label underlined: `<u><strong>Step N:</strong> ...</u>`
- Rule (if applicable) embedded in Step 2, not a separate slide
- Real quotes from the article on Step 4, in italics
- Original question in yellow (`#ffdd00`) on first and last slides

**Why markdown was abandoned**: reveal.js auto-animate requires consecutive sibling `<section data-auto-animate>` elements in `<div class="slides">`. The markdown plugin wraps all content in a single `<section data-markdown>`, making auto-animate impossible.

**Rules for auto-animate blocks:**
1. All sections in one block must be **consecutive siblings** — no other sections between them
2. `data-auto-animate-id` must match across all sections in the block
3. Each section adds content to what was shown in the previous section
4. `autoAnimateUnmatched: true` in `Reveal.initialize()` handles elements that appear/disappear between slides
5. All sections share `class="pedagogical"` and `data-background="#1a6b5a"` for visual consistency
6. The final section may use `fragment highlight-green` for answer reveal
7. Use for: strategy demonstrations (True/False, Multiple Choice), step-by-step language analysis, grammar transformations

**When NOT to use auto-animate:**
- Answer reveal slides (use fragments instead)
- General slide transitions (use regular slide changes)
- Vocabulary lists (all visible at once)
- Expository content (no animation)

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
- **No auto-animate** — use `data-background-transition="none"` on all pedagogical sections. Teacher controls pacing.
- **Teal background** — `data-background="#1a6b5a"` + `class="pedagogical"` on all strategy slides.
- **Top alignment** — CSS: `align-self: flex-start; margin-top: 0; padding-top: 30px` on `.reveal .slides > section.pedagogical`. Do NOT use negative margins (they clip content off-screen). Add `style="top: 0;"` inline on each section if needed.

### Vertical Alignment Fix

Reveal.js `.slides` is a flex container that defaults to vertically centering its section children. The correct fix is positive padding, not negative margin:

```css
.reveal .slides > section.pedagogical {
    align-self: flex-start;
    margin-top: 0;
    padding-top: 30px;
}
```

Using `margin-top: -2.5%` pushes content off-screen top. A small positive `padding-top` on the section is reliable.

### Vertical Alignment for Pedagogical Slides

```html
<section class="pedagogical" data-background="#1a6b5a" data-background-transition="none" style="top: 0;">
    <h2>True/False Strategy</h2>
    ...
</section>
```

### Example: True/False Strategy (4 slides + worked example)

```html
<!-- Slide 1: Header + Step 1 + yellow question + tip -->
<section class="pedagogical" data-background="#1a6b5a" data-background-transition="none" style="top: 0;">
    <h2>True/False Strategy</h2>
    <p style="color:#ffdd00;"><em>"The author wrote the text to explore the generation gap and problems it can cause, and to suggest a possible solution."</em></p>
    <p><u><strong>Step 1:</strong> Read the statement carefully</u></p>
    <p>Sometimes there is more than one question to think about — note each part separately.</p>
</section>

<!-- Slide 2: Step 2 + sub-questions + rule -->
<section class="pedagogical" data-background="#1a6b5a" data-background-transition="none" style="top: 0;">
    <p><u><strong>Step 2:</strong> Work out what the question is asking you</u></p>
    <ul>
        <li>Did the author write about the generation gap? <em>(Yes/No)</em></li>
        <li>Did the author write about the problems it can cause? <em>(Yes/No)</em></li>
        <li>Did the author suggest a possible solution? <em>(Yes/No)</em></li>
    </ul>
    <p><strong>Rule:</strong> If you answer "Yes" to all → it's TRUE.<br />If you answer "No" to even one → it's FALSE.</p>
</section>

<!-- Slide 3: Step 3 + paragraph names -->
<section class="pedagogical" data-background="#1a6b5a" data-background-transition="none" style="top: 0;">
    <p><u><strong>Step 3:</strong> Find the evidence</u></p>
    <p>Keywords like "author" and "solution" are found in <strong>paragraphs A and F</strong>. Now we can answer each question from Step 2.</p>
</section>

<!-- Slide 4: Step 4 + yellow question + real quotes + answer -->
<section class="pedagogical" data-background="#1a6b5a" data-background-transition="none" style="top: 0;">
    <p><u><strong>Step 4:</strong> Answer the question</u></p>
    <p style="color:#ffdd00;"><em>"The author wrote the text to explore the generation gap..."</em></p>
    <p>You can see that the author:</p>
    <ul>
        <li>talks about the generation gap → <em>"There is a growing generation gap between people..."</em></li>
        <li>writes about the problems → <em>"This can cause serious problems in families and workplaces..."</em></li>
        <li>offers solutions → <em>"The only way to close the gap is through empathy..."</em></li>
    </ul>
    <p><strong>So the answer is: TRUE.</strong></p>
</section>
```

### Example: Multiple Choice Strategy (5 steps + auto-animate + table answers)

```html
<!-- Step 1: Header + demo question + options -->
<section class="pedagogical" data-background="#1a6b5a" data-background-transition="none" style="top: 0;">
    <span style="font-size: 2.5em; color: rgba(255,255,255,0.9);"><i class="fa-solid fa-chess"></i></span>
    <div style="overflow: hidden;">
    <h2>Multiple Choice Strategy</h2>
    <p>Now let's learn how to answer MC questions with an example.</p>
    <p style="color:#ffdd00;"><em>"What is the main message of this article?"</em></p>
    <ul>
        <li><strong>a)</strong> option text</li>
        <li><strong>b)</strong> option text</li>
        <li><strong>c)</strong> option text</li>
    </ul>
    <p><u><strong>Step 1:</strong> Read the question — Is it asking for detail or main idea?</u></p>
    </div>
</section>

<!-- Step 2a: Auto-animate entry — borders invisible -->
<section class="pedagogical" data-background="#1a6b5a" data-background-transition="none" data-auto-animate>
    <div style="overflow: hidden;">
    <p><u><strong>Step 2:</strong> Underline key words</u></p>
    <p data-id="mcq" style="color:#ffdd00;"><em>"What is the <span data-id="w1" style="border-bottom: 2px solid transparent;">keyword</span> of this <span data-id="w2" style="border-bottom: 2px solid transparent;">word</span>?"</em></p>
    </div>
</section>

<!-- Step 2b: Auto-animate reveal — borders turn white -->
<section class="pedagogical" data-background="#1a6b5a" data-background-transition="none" data-auto-animate>
    <div style="overflow: hidden;">
    <p><u><strong>Step 2:</strong> Underline key words</u></p>
    <p data-id="mcq" style="color:#ffdd00;"><em>"What is the <span data-id="w1" style="border-bottom: 2px solid white;">keyword</span> of this <span data-id="w2" style="border-bottom: 2px solid white;">word</span>?"</em></p>
    </div>
</section>

<!-- Step 3: Scan text -->
<section class="pedagogical" data-background="#1a6b5a" data-background-transition="none">
    <div style="overflow: hidden;">
    <p><u><strong>Step 3:</strong> Scan the text</u></p>
    <ul>
        <li>Detail questions: answer follows the order of the text</li>
        <li>Main idea: think about what the whole text is about</li>
    </ul>
    </div>
</section>

<!-- Step 4: Eliminate wrong answers — fragment strike table -->
<section class="pedagogical" data-background="#1a6b5a" data-background-transition="none">
    <div style="overflow: hidden;">
    <p><u><strong>Step 4:</strong> Eliminate wrong answers</u></p>
    <table class="answer-table">
        <thead><tr><th>Option</th><th>Why?</th></tr></thead>
        <tbody>
            <tr><td class="fragment strike" data-fragment-index="0"><strong>a)</strong> wrong option text</td><td class="fragment" data-fragment-index="0">Reason why wrong</td></tr>
            <tr><td class="fragment strike" data-fragment-index="1"><strong>b)</strong> wrong option text</td><td class="fragment" data-fragment-index="1">Reason why wrong</td></tr>
        </tbody>
    </table>
    </div>
</section>

<!-- Step 5: Confirm correct answer — table with citations -->
<section class="pedagogical" data-background="#1a6b5a" data-background-transition="none">
    <div style="overflow: hidden;">
    <p><u><strong>Step 5:</strong> Confirm your answer</u></p>
    <table class="answer-table wrap">
        <thead><tr><th>Answer</th><th>Why?</th></tr></thead>
        <tbody>
            <tr><td><strong>c)</strong> correct option text</td><td>Matches the article: <em>"quote from text"</em> (para X)</td></tr>
        </tbody>
    </table>
    </div>
</section>
```

### Answer Table Patterns (V1)

All answer slides use `answer-table` class with green background `#1e7e34`. The answer column and optionally the explanation column use fragments for clickthrough reveal.

**2-column table (True/False, simple answers):**

```html
<section data-background="#1e7e34">
    <h2>Exercise N — Answers</h2>
    <table class="answer-table">
        <thead><tr><th>Statement</th><th>Answer</th></tr></thead>
        <tbody>
            <tr>
                <td>statement text</td>
                <td class="fragment answer-correct">✓ Correct</td>
            </tr>
            <tr>
                <td>another statement</td>
                <td class="fragment answer-incorrect">✗ Incorrect</td>
            </tr>
        </tbody>
    </table>
</section>
```

**3-column table (with explanation):**

```html
<section data-background="#1e7e34">
    <h2>Exercise N — Answers</h2>
    <table class="answer-table">
        <thead><tr><th>Statement</th><th>Answer</th><th>Why?</th></tr></thead>
        <tbody>
            <tr>
                <td>statement text</td>
                <td class="fragment answer-correct">✓ Correct</td>
                <td class="fragment">explanation with paragraph reference</td>
            </tr>
            <tr>
                <td>another statement</td>
                <td class="fragment answer-incorrect">✗ Incorrect</td>
                <td class="fragment">explanation with paragraph reference</td>
            </tr>
        </tbody>
    </table>
</section>
```

For answer tables with long explanation text that must wrap, add class `wrap`:
```html
<table class="answer-table wrap">
```

### Fragment Strike Confirmed Behavior

Per `knowledge-base\revealjs-packed.json` (line 127-134):
```css
.reveal .fragment.strike { opacity: 1; visibility: inherit; }
.reveal .fragment.strike.visible { text-decoration: line-through; }
```
**Do NOT override this CSS** in the `<style>` block. Text is always visible; strikethrough appears on click only. Any custom `.reveal .fragment.strike` CSS in the page will break this behavior.

## reveal.js Codebase

When making changes to reveal.js code (e.g., custom themes, configuration, or plugin modifications), **always consult the stored reveal.js codebase first**. Do not attempt to write reveal.js API code from memory.

The packed reveal.js codebase is stored at: `knowledge-base\revealjs-packed.json`

```bash
# Load and query the packed JSON
$json = Get-Content "knowledge-base\revealjs-packed.json" | ConvertFrom-Json

# List all files
$json.files.PSObject.Properties.Name | Sort-Object

# Get specific file content
$json.files.'js/reveal.js'
$json.files.'css/reveal.scss'
$json.files.'css/theme/white.scss'

# Search for specific code
$json.files.PSObject.Properties | Where-Object { $_.Value -match "transition" }

# View the auto-animate example (canonical pattern reference)
$json.files.'examples/auto-animate.html'
```

### Update reveal.js Pack

To update the stored codebase when reveal.js releases a new version:

```bash
repomix --remote https://github.com/hakimel/reveal.js --style json --output knowledge-base\revealjs-packed.json --top-files-len 15
```

### Global Repomix Skill

See: `C:\Users\elwru\.kilo\skills\repomix-codebase-search\SKILL.md`

## Files

| File | Purpose |
|---|---|
| `docs/slide-design-reference.md` | Slide design rules (authoritative) |
| `templates/base-slides-template.html` | **Base template for ALL new presentations** |
| `templates/slides-template.html` | **DEPRECATED** — markdown-based (kept for backward compat) |
| `scripts/json_to_markdown.py` | **DEPRECATED** — markdown generator (not for new work) |
| `scripts/pixabay_download.py` | Pixabay image downloader (first-gen only) |
| `scripts/locate_slide.py` | Map reveal.js URL index to HTML section |
| `templates/ACT.png` | Institution logo (ACT) — copy to `assets/logo.png` |
| `templates/ACT.png` | Institution logo (ACT) — copy to `assets/logo.png` |

## Dependencies
- Python 3.x + Pillow
- reveal.js 5.1.0 via CDN (no npm needed)
- `templates/base-slides-template.html` (copied to `output/{subfolder}/slides/index.html`)

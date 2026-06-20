# Pandoc → reveal.js: Capability Assessment

Date: 2026-06-15
Pandoc version tested: 3.7.0.2
Purpose: Determine whether a Pandoc + Markdown pipeline can replace the current hand-written HTML approach for ESL lesson slides, reducing or eliminating the agent's need to write raw HTML.

---

## 1. Knowledge Currency

The initial assessment was based on training data (cutoff ~early 2025). After the research cycle:

- Pandoc 3.7 (March 2026) confirmed: added `--variable-json`, `scroll`/`scrollSnap` reveal.js options
- Pandoc 3.6 added: `--syntax-highlighting=idiomatic` for reveal.js highlight.js compatibility
- Default reveal.js template dumped and analysed
- Lua filter ecosystem verified as active and well-documented
- 5 empirical test builds were performed to verify claims

**Assessment: Current as of Pandoc 3.7.0.2 (the installed version).**

---

## 2. Capability Matrix

Each item is marked with:
- ✅ **Confirmed working** in empirical tests or Pandoc documentation
- ❌ **Does not work** with Pandoc (different from "impossible" — some have workarounds)
- 🛠 **Fixable** with Lua filter or custom template

### 2.1 Slide-Level Attributes

| Feature | Markdown Syntax | Status | Notes |
|---|---|---|---|
| `data-auto-animate` on sections | `## heading {data-auto-animate=}` | ✅ Works | With `--slide-level=2`, propagates to both `<section>` and `<h2>` |
| `data-auto-animate` on level-1 | `# heading {data-auto-animate=}` | 🛠 | Propagates to `<h1>` but NOT `<section>` with `--slide-level=1`. Lua filter can fix. |
| `data-background-color` | `## heading {data-background-color="red"}` | ✅ Works | Pandoc passes unknown heading attributes through |
| `data-background-image` | `## heading {data-background-image="url"}` | ✅ Works | Same mechanism |
| `data-timer` | `## heading {data-timer=300}` | 🛠 | Attaches to `<h2>` but not `<section>`. Lua filter needed. |
| `data-audio-src` | `## heading {data-audio-src="file.mp3"}` | 🛠 | Same issue. Lua filter needed. |
| `data-transition` | `## heading {data-transition="zoom"}` | ✅ Works | Confirmed in Pandoc docs |
| `title-slide-attributes` | YAML frontmatter | ✅ Works | Native Pandoc feature |

### 2.2 Content Features

| Feature | Markdown Syntax | Status | Notes |
|---|---|---|---|
| Fragments on list items | `<li class="fragment">` raw HTML | ✅ Works | Pandoc passes raw block HTML through verbatim |
| Fragments on any element | `<span class="fragment">content</span>` | ✅ Works | Inline raw HTML preserved |
| Fragments via `.element:` comment | `<!-- .element: class="fragment" -->` | ❌ **Does not work** | Pandoc outputs these as inert HTML comments. This is a reveal.js-markdown-plugin runtime feature, not a Pandoc feature. |
| Incremental lists | `::: incremental` fenced div | ❌ **Does not work** | Pandoc converts this to `<!-- .element: class="fragment" -->` comments (same problem) |
| Incremental lists via `-i` flag | `pandoc -i` | ✅ Works | Adds `class="fragment"` to `<li>` elements directly |
| Speaker notes | `::: notes` fenced div | ✅ Works | Converts to `<aside class="notes">` |
| Speaker notes via `Note:` | `Note: text` after content | ❌ Does not work | Rendered as visible paragraph. Pandoc doesn't support reveal.js's `data-separator-notes` approach. |
| Pipe tables | `\| col1 \| col2 \|` | ✅ Works | Pandoc-native. Outputs `<table>`. |
| Fenced divs with classes | `::: {.myclass}` | ✅ Works | Outputs `<div class="myclass">` |
| Bracketed spans | `[text]{.class key=val}` | ✅ Works | Outputs `<span class="class" key="val">` |
| Raw HTML blocks | `<div>...</div>` in markdown | ✅ Works | Passed through verbatim |
| Raw HTML inline | `<span>text</span>` in paragraphs | ✅ Works | Passed through verbatim |
| `data-id` on inline elements | `<span data-id="w1">text</span>` | ✅ Works | Raw HTML preserves all attributes |
| Auto-animate element matching | Two adjacent sections with same heading text | ✅ Works | Works for text changes, list reordering |
| Auto-animate with `data-id` | Raw HTML spans in two adjacent sections | ✅ Works | Requires raw HTML for the spans |

### 2.3 Template & Configuration

| Feature | Status | Notes |
|---|---|---|
| Custom themes | ✅ `-V theme=...` or YAML | Default Pandoc template supports all reveal.js themes |
| Custom CSS | ✅ `--css file.css` or `--include-in-header=file.css` | Multiple CSS files supported |
| Custom template | ✅ `--template=file.html` | Full control over shell |
| Plugin loading | 🛠 Via custom template | Default template only loads Notes, Search, Zoom. TimerPlugin and AudioSlideshow must be added manually. |
| Custom JS | ✅ `--include-after-body=file.js` or `--include-in-header=file.js` | Works |
| `--embed-resources` | ✅ Single-file HTML with all assets | ~8MB due to font base64 encoding |
| `revealjs-url` | ✅ Set via `-V revealjs-url=url` | Defaults to CDN |

### 2.4 Lua Filter Capabilities

| Task | Feasibility | Lines |
|---|---|---|
| Move `data-auto-animate` from heading to section | ✅ Trivial | ~20 |
| Inject `data-timer` / `data-audio-src` from heading attrs | ✅ Trivial | ~15 |
| Add class to sections | ✅ Trivial | ~10 |
| Convert `.element:` comments to real attributes | ✅ Possible | ~40 |
| Add custom attributes to all sections | ✅ Trivial | ~15 |
| Flatten vertical slides to horizontal | 🛠 Possible but complex | ~60-80 |

---

## 3. Pattern Audit: What Actually Requires HTML?

Every current slide pattern was audited to separate **pedagogical necessity** from **implementation accident**.

### 3.1 Answer Displays (T/F, Multiple Choice, Comprehension)

**Current implementation** (accident):
```html
<div class="answer-list">
  <div class="a-row">
    <span class="a-num">1.</span>
    <span class="a-q">Statement text</span>
    <span class="fragment fade-up a-ans a-cor">✓ True</span>
    <span class="a-why fragment fade-up">WHY: explanation</span>
  </div>
</div>
```

**Pedagogical requirement:** Question visible on entry. Answer + explanation hidden behind fragment click. Check/cross icon. Why column.

**Simplest Pandoc-native approach:**
```markdown
| # | Statement | Answer | Why? |
|---|---|---|---|
| 1 | "Quote from text..." | ✓ True | Explanation — Para 2 |
```
Wrap in `::: {.fragment}` to reveal the whole table on click. Or make each row a separate table/fragment.

**Verdict: Flex answer-list was an implementation accident. Pandoc pipe tables handle this natively with zero raw HTML.**

### 3.2 Both-Methods Correction Pattern

**Current implementation** (over-engineering):
```html
<section class="answer-slide">
  <h2>Practice N — Item N</h2>
  <div class="p11-answer">
    <p class="p11-badge">comma splice</p>
    <p class="p11-original">"Original sentence."</p>
    <div class="p11-method">
      <p><u>Method 1: Add a period</u></p>
      <p class="p11-fix">→ "Fixed sentence."</p>
    </div>
    <div class="p11-method">
      <p><u>Method 2: Add a comma + coordinator</u></p>
      <p class="p11-fix">→ "Fixed sentence, and ..."</p>
    </div>
    <p class="p11-why">Why: explanation.</p>
  </div>
</section>
```

**Pedagogical requirement:** Original sentence visible. Then reveal Method 1, then Method 2, then why.

**Simplest Pandoc-native approach:**
```markdown
---
## Practice N — Item N

**Error type:** comma splice

> "Original sentence with the error."

::: incremental
- **Method 1:** Add a period → "Fixed sentence."
- **Method 2:** Add a comma + coordinator → "Fixed sentence, and ..."
:::

**Why:** Explanation of the error and why both fixes work.
```

Or use fragment `<p>` tags for per-item click control.

**Verdict: The nested CSS classes were over-engineering. Simple markdown lists with fragments achieve the same classroom outcome.**

### 3.3 S/V/O Annotation on Sentences

**Current implementation** (accident):
```html
<span data-id="subject" class="a-s">
  <span class="a-ls">S </span>My roommate
</span>
<span data-id="verb" class="a-v" style="box-shadow: 0 5px 0 0 #ffdd00;">
  <span class="a-lv">V </span>lost
</span>
```

**Pedagogical requirement:** Underline subject in white, verb in yellow, object in box. Label each with S/V/O superscript.

**Simplest Pandoc-native approach (bracketed spans):**
```markdown
**S** [My roommate]{.s} **V** [lost]{.v} **O** [his keys]{.o}
```
With CSS:
```css
.s { border-bottom: 2px solid #fff; }
.v { border-bottom: 4px solid #ffdd00; }
.o { border: 2px solid #fff; padding: 0 4px; border-radius: 4px; }
```

**Verdict: Native Pandoc syntax. Zero raw HTML. Only a few lines of CSS.**

### 3.4 Auto-Animate Keyword Underline Reveals

**Current implementation:**
```html
<section data-auto-animate>
  <p data-id="mcq"><span data-id="w1" style="border-bottom: 2px solid transparent;">main message</span></p>
</section>
<section data-auto-animate>
  <p data-id="mcq"><span data-id="w1" style="border-bottom: 2px solid white;">main message</span></p>
</section>
```

**Pedagogical requirement:** Two adjacent slides. First slide: plain sentence. Second slide: same sentence with keywords underlined. Auto-animate animates the borders appearing.

**Simplest Pandoc-native approach:** Two adjacent markdown sections with raw HTML for the spans (because `data-id` on inline elements has no Pandoc-native syntax akin to bracketed spans):

```markdown
## Step 2 {data-auto-animate=}

What is the <span data-id="w1" style="border-bottom: 2px solid transparent;">main message</span>?

---

## Step 2 {data-auto-animate=}

What is the <span data-id="w1" style="border-bottom: 2px solid white;">main message</span>?
```

**Verdict: This is the ONE pattern that genuinely requires raw HTML.** Approximately 4-6 lines of inline raw `<span>` tags per auto-animate pair. But the surrounding structure (sections, headings, content) is still markdown.

### 3.5 Vocabulary Slides (IPA + TTS + Context)

**Current implementation:** Complex HTML with `audio` element, `vocab-word` class, and two fragment steps.

**Pedagogical requirement:** IPA visible on entry. Click → English word appears + TTS plays. Click → context sentence appears.

**Simplest Pandoc-native approach:**
```markdown
/ˈreməkəbəl/

**remarkable** *(adjective)* {data-audio-src="assets/vocab-remarkable.mp3"}

<span class="fragment">She is a **remarkable** athlete. She won three gold medals.</span>
```

**Verdict: One raw `<span class="fragment">` per vocab slide (~1 line). Audio handled via heading attribute + Lua filter.**

### 3.6 Timer Slides

**Current implementation:** `data-timer` on section + TimerPlugin.

**Simplest approach:**
```markdown
## Practice 2B {data-timer=300}

Complete the matching exercise.
```

With Lua filter to propagate the attribute from heading to section. The TimerPlugin is added via custom template (one-time effort).

**Verdict: Zero raw HTML. One heading attribute + one Lua filter (25 lines, written once).**

### 3.7 Audio Playback (Listening Exercises)

**Current implementation:** `data-audio-src` on section + AudioSlideshow plugin.

**Simplest approach:**
```markdown
## Listen for Gist {data-audio-src="assets/track1.mp3"}

Listen and answer the questions.
```

Same Lua filter handles it.

**Verdict: Zero raw HTML. Same Lua filter covers timer + audio.**

---

## 4. The Remaining HTML Burden

After the audit, here is the **honest irreducible HTML** that remains per slideshow:

| Pattern | Raw HTML Remaining | Occurrences per 30-slide lesson |
|---|---|---|
| Auto-animate keyword underlines | `<span data-id="w1" style="...">word</span>` (2-3 spans per pair) | 1-3 pairs (pedagogical strategy blocks) |
| Vocab context fragments | `<span class="fragment">...</span>` | 1 per vocab word (3-5 words) |
| Custom fragment indices (advanced control) | None if using sequential fragments; raw HTML if non-sequential | 0 in most cases |
| Everything else | **Zero** (tables, lists, headings, notes, classes, timers, audio) | — |

**Total: Approximately 10-25 lines of raw HTML per 30-slide lesson, down from the current ~800+ lines.**

---

## 5. Infrastructure Needed for Path A (Pandoc + Markdown)

Written once, used by every slideshow:

| Component | Lines | Complexity |
|---|---|---|
| Custom Pandoc template (inject our CSS, TimerPlugin, AudioSlideshow, `fragmentshown` handler) | ~80 | Medium |
| Lua filter (propagate `data-timer`, `data-audio-src`, `data-auto-animate` from heading to section) | ~25 | Low |
| **Total one-time code** | **~105 lines** | — |

Per slideshow:
```bash
pandoc lesson.md -t revealjs -s --template=templates/revealjs.html \
  -L filters/slide-attrs.lua --css=styles/slides.css \
  -o output/slides/index.html --slide-level=2
```

**The agent writes:**
```
lesson.md  ← pure markdown with heading attributes for config
```

---

## 6. Key Limitation: Auto-Animate Slide Navigation

With `--slide-level=2` (required for auto-animate on content sections), slides from `##` headings become **vertical** — navigated with down arrow, not right arrow. This is the default reveal.js behavior for nested sections and is how the vast majority of reveal.js users navigate multi-point slides.

**Whether this is a problem depends on the audience:**
- Teacher advances through a strategy demo slide-by-slide: down arrow is natural
- Teacher jumps between major lesson phases: right arrow moves between `#`-level sections
- Vertical navigation is standard in reveal.js and most users expect it

If flat (horizontal-only) navigation is required, it can be achieved by using `#` headings for every slide and applying auto-animate via Lua filter. This is a design choice, not a technical blocker.

**The skill's existing claim — "auto-animate requires sibling `<section data-auto-animate>` elements, which cannot be produced from a single `<section data-markdown>` container" — is false with Pandoc.** Pandoc generates sibling `<section>` elements from adjacent markdown headings. The `data-auto-animate` attribute is added via heading attributes and propagates correctly to level-2 sections.

---

## 7. Path A vs Path B: Updated Comparison

| Dimension | Path A: Pandoc + Markdown | Path B: Fix slides_builder.py |
|---|---|---|
| **One-time developer code** | ~105 lines (template + filter) | ~1000 lines (fix + 8 builders + composer) |
| **Agent code per slideshow** | Markdown + ~10-25 lines of inline `<span>` tags | Pure Python function calls |
| **Raw HTML in agent output** | Minimal (auto-animate spans only) | Zero |
| **Pattern flexibility** | Constrained by Pandoc's HTML output | Full control |
| **New pattern cost** | Add CSS + possibly update template | Write one Python function |
| **Learning curve for agent** | Markdown (universal skill) | Python function calls (project-specific) |
| **Dependency** | Requires Pandoc 3.x on PATH | No external dependencies |
| **Slide complexity ceiling** | Medium-high (most patterns achievable) | Unlimited |

**Path A is ~90% less developer code upfront.** The gap narrows if we decide we need complex patterns that Pandoc cannot easily express, but the audit shows almost all of our current patterns are expressible in native Pandoc markdown or with trivial `<span>` wrappers.

---

## 8. Open Questions for Decision

1. **Is vertical (down-arrow) navigation acceptable for strategy-step slides?** If yes, `--slide-level=2` works perfectly. If no, a Lua filter must flatten the structure.

2. **Is `<table>` for answer reveals acceptable?** If yes, Pandoc pipe tables eliminate the entire flex answer-list pattern. If no, the agent writes `<div class="answer-list">` raw HTML.

3. **Are simple bold/underline annotations for S/V/O acceptable?** If yes, the `[text]{.class}` bracketed span syntax handles it. If no, raw HTML with `data-id` is needed for auto-animate reveals.

4. **How important is per-item click control on answer slides?** If every answer reveals at once is fine, a single `::: {.fragment}` around the table works. If each answer must reveal separately, per-row fragments require raw `<tr class="fragment">` or per-item tables.

These are design decisions, not technical blockers.

---

## Appendix A: Gap Resolution Research (2026-06-15)

### Gap 1: Auto-Animate Propagation to Section Level

**Status: ✅ Already works with `--slide-level=2`**

With `--slide-level=2`, Pandoc propagates `{data-auto-animate=}` from a `##` heading to BOTH the `<h2>` element AND the parent `<section>`. This was confirmed empirically in Test 5:

```markdown
## The Basic Sentence {data-auto-animate=}
```

Produces:
```html
<section id="the-basic-sentence" class="slide level2" data-auto-animate>
  <h2 data-auto-animate>The Basic Sentence</h2>
```

**Source:** Pandoc HTML writer passes unknown attributes through to the generated elements. The Quarto/Pandoc discussion #5549 confirms: attributes on headings are passed as HTML attributes on the section element.

**If flat (level-1) auto-animate is needed:** A Lua filter of ~20 lines can move attributes from the `<h1>` to the parent `<section>` when using `--slide-level=1`.

### Gap 2: `data-timer` and `data-audio-src` Injection

**Status: ✅ Works out of the box — no Lua filter needed**

Pandoc passes custom `data-*` attributes through to the section element. From the Pandoc manual (10.8):

> "As the HTML writers pass unknown attributes through, other reveal.js background settings also work on individual slides, including `background-size`, `background-repeat`, `background-color`, `transition`, and `transition-speed`. (The `data-` prefix will automatically be added.)"

And for pre-prefixed attributes, Test 5 confirmed `{data-auto-animate=}` appears as `data-auto-animate` on the section — no doubling.

```markdown
## Practice 2B {data-timer=300}
## Listen for Gist {data-audio-src="assets/track1.mp3"}
```

Both produce the correct attributes on `<section>` without a Lua filter.

**WARNING:** Pandoc silently adds `data-` to UNKNOWN non-prefixed attributes. So `{background-color="red"}` becomes `data-background-color="red"`. BUT a `{data-something}` attribute retains its prefix. This means `{data-timer}` passes through correctly, while `{timer}` would become `data-timer`. Standardize on always writing `data-` prefix explicitly.

### Gap 3: TimerPlugin and AudioSlideshow Integration

**Status: ✅ Solvable via custom Pandoc template**

Pandoc's default template only loads Notes, Search, and Zoom plugins. To add TimerPlugin and AudioSlideshow:

1. **Option A: Custom template** (recommended)
   - Copy Pandoc's default template: `pandoc -D revealjs > templates/revealjs-custom.html`
   - Add `<script>` tags for the plugins:
   ```html
   <script src="$revealjs-url$/plugin/audio-slideshow/plugin.js"></script>
   <script src="$revealjs-url$/plugin/audio-slideshow/recorder.js"></script>
   ```
   - Add plugins to the `Reveal.initialize()` call
   - Invoke with `--template=templates/revealjs-custom.html`

2. **Option B: `--include-in-header`** (lighter)
   - Inject plugin scripts via `<script>` tags in an include file
   - Add the plugin registration via another include
   - No custom template needed, but more fragile

3. **Option C: Custom `header-includes` in YAML**
   ```yaml
   header-includes: |
     <script src="$revealjs-url$/plugin/audio-slideshow/plugin.js"></script>
   ```

**RStudio `revealjs` package reference:** Confirms `reveal_plugins` parameter accepts "notes", "search", "zoom", "chalkboard", "menu" as built-in options. For external plugins, direct `<script>` injection is the standard pattern.

### Gap 4: Custom CSS Framework Integration

**Status: ✅ Multiple working approaches**

| Method | Command | Use Case |
|--------|---------|----------|
| External CSS file | `--css=styles/slides.css` | Cleanest for large CSS |
| Inline in header | `--include-in-header=style.html` | When bundled with template |
| YAML frontmatter | `header-includes: \|` then CSS wrapped in `<style>` | Per-document overrides |

All our existing CSS classes (`.a-row`, `.p11-answer`, `.cor-add`, `.a-s`, `.a-v`) can be injected via any of these methods.

The gist by jsoma (updated 2025) confirms: `pandoc -t revealjs -s -o index.html slides.md --include-in-header=slides.css -V theme=serif` is a standard workflow.

### Gap 5: Vertical/Horizontal Navigation Decision

**Status: ✅ Both options are viable**

- **`--slide-level=2` (vertical):** `##` headings produce auto-animated vertical slides. Down-arrow navigates between strategy steps. Right-arrow moves between `#` sections. This is standard reveal.js behavior (see revealjs.com/vertical-slides). **`navigationMode` can be configured.**

- **`--slide-level=1` (flat horizontal):** All slides are horizontal. Auto-animate requires a Lua filter to propagate to the section, since Pandoc only puts `data-auto-animate` on the `<h1>` element, not the section.

**Recommendation:** Accept `--slide-level=2` (vertical). It's the standard reveal.js navigation model, and teachers are familiar with it. Pandoc changelog 2.11 confirmed: "restore 2D nesting behavior at slide level N-1 and N."

### Gap 6: Fragment Handling for Non-List Elements

**Status: ✅ Works via raw HTML spans**

Pandoc passes raw HTML through unchanged. For fragment reveals on paragraphs, blockquotes, or any non-list element:

```markdown
<blockquote class="fragment" style="font-style:italic;">
  "Quote text here."
</blockquote>

<p class="fragment">This paragraph reveals on click.</p>
```

For vocabulary context sentences:
```markdown
/ˈreməkəbəl/

**remarkable** *(adjective)*

<span class="fragment">She is a **remarkable** athlete. She won three gold medals.</span>
```

The `-i` flag adds `class="fragment"` to `<li>` elements in all lists. For selective fragments within a single list, wrap in `::: incremental` or use raw HTML `<li class="fragment">`.

**Source:** Stack Overflow answer (75279429) confirms: "I can use fenced divs `::: {.fragment}` or insert the `li` element manually." Also Pandoc's `-i` flag.

### Gap 7: `fragmentshown` Event Handler for Vocab TTS

**Status: ✅ Standard reveal.js event API, injectable via custom template**

```javascript
Reveal.on('fragmentshown', function(event) {
  if (event.fragment.classList.contains('vocab-word')) {
    var audio = document.querySelector('audio[data-vocab-audio]');
    if (audio) { audio.play(); }
  }
});
```

Inject via:
- Custom template `<script>` block
- `--include-after-body=vocab-audio.js`
- `header-includes` in YAML

The reveal.js fragments documentation (revealjs.com/fragments) confirms: `Reveal.on('fragmentshown', callback)` is the standard event API for fragment transitions.

---

## Appendix B: Concrete Implementation Plan

### Phase 1: Infrastructure (write once)

| Step | File | Description | Lines |
|------|------|-------------|-------|
| 1.1 | `templates/revealjs-custom.html` | Custom Pandoc template based on default, adding TimerPlugin, AudioSlideshow, `fragmentshown` handler, and our CSS link | ~80 |
| 1.2 | `scripts/slides.css` | Our CSS framework (`.a-row`, `.p11-answer`, `.cor-add`, `.a-s`, `.a-v`, etc.) extracted for Pandoc output | ~200 |
| 1.3 | `scripts/defaults.yaml` | Pandoc defaults file with standard flags, template path, CSS path, Lua filter path | ~15 |

**No Lua filter is needed** for `data-timer`, `data-audio-src`, or `data-auto-animate` — Pandoc passes them through natively.

### Phase 2: Command (one-liner per slideshow)

```
pandoc --defaults=scripts/defaults.yaml slides.md -o output/slides/index.html
```

Where `defaults.yaml` contains:
```yaml
to: revealjs
standalone: true
template: templates/revealjs-custom.html
css: scripts/slides.css
slide-level: 2
embed-resources: true
variables:
  revealjs-url: "https://cdn.jsdelivr.net/npm/reveal.js@5.1.0"
  theme: black
```

### Phase 3: Agent Workflow

The agent writes ONE file: `slides.md`

Structure of `slides.md`:
```markdown
---
title: "CA: Writing a Profile"
subtitle: "What makes someone unforgettable?"
author: "ACT"
date: "2026-06-15"
title-slide-attributes:
  data-background-image: "assets/title-bg.jpg"
  data-background-size: "cover"
---

# Lesson Title

{data-background-image="assets/lead-in.jpg"}

What makes someone unforgettable?

::: notes
Elicit ideas from students. (2 min, T-S)
:::

---

## Strategy: True/False {data-auto-animate=}

**Step 1:** Read the statement carefully.

Look for absolute words like "always" or "never."

---

## Strategy: True/False {data-auto-animate=}

**Step 2:** Underline key words.

The <span data-id="w1" style="border-bottom: 2px solid transparent;">generation gap</span> is a <span data-id="w2" style="border-bottom: 2px solid transparent;">recent</span> phenomenon.

---

## Exercise 1 {data-timer=300}

Complete Practice 1 in your workbook.

---

| # | Statement | Answer | Why? |
|---|---|---|---|
| 1 | "Quote from text..." | ✓ True | Explained in Para 2 |
| 2 | "Another quote..." | ✗ False | Contradicted in Para 4 |

---

## Let's Practice {data-audio-src="assets/track1.mp3"}

Listen and answer the questions.

::: notes
Play the recording twice. (5 min, individual work)
:::
```

### Summary of What's Changed from Current Skill

| Before | After |
|--------|-------|
| Agent hand-writes `<section>` HTML | Agent writes Markdown |
| 800+ lines raw HTML per slideshow | ~10-25 lines of `<span>` tags per slideshow |
| Flex answer-list with 5+ nested divs per row | Pipe tables (`\| # \| Statement \| Answer \| Why \|`) |
| Complex `.p11-answer` CSS classes | Bullet lists or two pragraphs |
| Manual plugin configuration in `<head>` | Custom template handles all JS |
| Manual CSS class injection | `--css` flag loads framework |
| Separate audio/timer JS configuration | Heading attributes `{data-timer}` / `{data-audio-src}`

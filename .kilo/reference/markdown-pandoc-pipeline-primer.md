# Markdown → Pandoc → Typst/HTML — Pipeline Primer

## Why Not Raw Typst?

Agents should **never write raw Typst** for document generation. The Markdown → Pandoc → Typst pipeline exists because:

| Raw Typst | Markdown → Pandoc → Typst |
|-----------|---------------------------|
| `#`/no-`#` context errors inside `[...]` | Zero syntax errors — Pandoc generates correct Typst |
| `#strong[M]y` required for mid-word bold | `**M**y` works as expected |
| `[*#*]` must be escaped as `[*\#*]` | `#` is just text |
| No markdown pipe tables — must use `#table(columns: N, ...)` | Pipe tables `| A \| B \|` work natively |
| Raw blocks can't be function arguments | Pandoc handles code blocks |
| Unicode invisible chars crash compiler | Markdown strips them naturally |
| Zero-width space U+200B crashes Typst | Never introduced by Pandoc |

## The Three-Layer Architecture

```
┌─────────────────────────────────────────────────────┐
│                     Layer 1: Markdown                │
│  Agent writes: content.md with YAML frontmatter      │
│  - Pure Pandoc Markdown (no Typst, no HTML)          │
│  - YAML metadata for variables (title, date, etc.)   │
│  - Fenced divs for structure (::: {.class})          │
│  - Bracketed spans for inline styling [text]{.class} │
└──────────────────────┬──────────────────────────────┘
                       │ pandoc -f markdown
                       ▼
┌─────────────────────────────────────────────────────┐
│                 Layer 2: Pandoc + Lua Filters         │
│  Transforms the AST before writing output            │
│                                                       │
│  Lua filters can:                                     │
│  - Read metadata from headings (data-audio-src, etc.)│
│  - Transform divs into different output elements      │
│  - Inject raw output blocks (HTML, Typst, etc.)       │
│  - Pass through untouched content                     │
│  - Access the full document AST                       │
└──────────────────────┬──────────────────────────────┘
                       │ pandoc -t typst | -t revealjs
                       ▼
┌─────────────────────────────────────────────────────┐
│         Layer 3: Typst compile (PDF)                  │
│         OR: Reveal.js (HTML slides)                   │
│                                                       │
│  Typst: Static template + generated .typ → PDF       │
│  Reveal.js: Generated .html served directly           │
└─────────────────────────────────────────────────────┘
```

## Why Lua Filters?

Lua filters are the **secret weapon** that makes this pipeline practical. They operate on Pandoc's Abstract Syntax Tree (AST) — the parsed document — before it's written to the target format. This means:

### What Lua Filters Can Do

1. **Read metadata from headings** — e.g., `{data-audio-src="file.mp3"}` on a heading gets transformed into `<audio data-autoplay>` in HTML.

2. **Transform structural elements** — e.g., convert `## Stage N:` headings into a Typst `#table()` with colored headers (see `scripts/lesson-tables.lua`).

3. **Inject raw output** — add HTML iframes, Typst blocks, or any format-specific content that Markdown can't express.

4. **Filter/transform content** — modify text, rearrange elements, add wrapping divs.

5. **Combine with CSS** — generate clean semantic HTML that a companion CSS file styles.

### Concrete Examples from This Project

#### `scripts/audio-autoplay.lua` (Slides pipeline)

```lua
-- Reads data-audio-src from headings, injects <audio data-autoplay>
function Header(el)
  local src = el.attributes['data-audio-src']
  if src then
    local audio = '<audio data-autoplay src="' .. src .. '"></audio>'
    -- Add raw HTML audio element after the heading
    return {el, pandoc.RawBlock('html', audio)}
  end
end
```

This is 20 lines of Lua. The equivalent raw HTML would need to be hand-written for every slide, error-prone, and impossible to maintain across 30+ slides.

#### `scripts/youtube-embed.lua` (Slides pipeline)

```lua
-- Converts ::: {.youtube} VIDEO_ID ::: to responsive iframe
function Div(el)
  if el.classes:includes('youtube') then
    local id = el.content[1].text  -- extract video ID
    local iframe = '<div class="iframe-container">'
      .. '<iframe src="https://www.youtube.com/embed/' .. id .. '" ...>'
      .. '</iframe></div>'
    return pandoc.RawBlock('html', iframe)
  end
end
```

#### `scripts/lesson-tables.lua` (PDF pipeline)

```lua
-- Converts ## Stage N: headings into a Typst #table() with colored headers
function Header(el)
  if el.level == 2 and el.content[1].text:match('^Stage ') then
    -- ... generates Typst table rows from the heading + following content
    return pandoc.RawBlock('typst', generated_table_code)
  end
end
```

## The Two Pipelines in Detail

### Pipeline A: PDF (Markdown → Pandoc → Typst → PDF)

```
lesson.md (YAML + Markdown stages)
    │
    ▼
pandoc --template=templates/lesson-plan.typ \
       --lua-filter=scripts/lesson-tables.lua \
       -f markdown -t typst
    │
    ▼
output.typ (Pandoc-generated, never hand-edited)
    │
    ▼
typst compile --font-path=... output.typ lesson-plan.pdf
```

**Agent writes:** Pure Pandoc Markdown with YAML frontmatter. The YAML contains metadata like `topic`, `teacher`, `duration`, `cefr_level`, `class`, `shape`, `main_aim`, `materials`, etc.

**What the Lua filter does:** Reads `## Stage N:` headings and the following structured content (time, aim, procedure), then generates a correctly-formatted Typst `#table()` with colored header rows, time columns, and bullet-point procedures.

**Why agents must NOT write Typst:** Every time an agent tried to write the table markup directly, it hit Typst's `#`/no-`#` context rules (different inside `[...]` vs `(...)` vs `#` blocks). The Lua filter generates correct Typst by construction.

### Pipeline B: Slides (Markdown → Pandoc → Reveal.js HTML)

```
slides.md (Pandoc Markdown with fenced divs)
    │
    ▼
pandoc -t revealjs -s --slide-level=1 \
       --lua-filter=scripts/audio-autoplay.lua \
       --lua-filter=scripts/youtube-embed.lua \
       --css=slides-pandoc.css
    │
    ▼
index.html (self-contained reveal.js presentation)
```

**Agent writes:** Pure Pandoc Markdown with `#` headings (each = one slide), fenced divs for fragments/shields, and `data-*` attributes on headings for audio/settings.

**What the Lua filters do:**
- `audio-autoplay.lua` — reads `{data-audio-src="file.mp3"}` from headings, injects `<audio data-autoplay>` for automatic playback when the slide enters.
- `youtube-embed.lua` — converts `::: {.youtube} VIDEO_ID :::` fenced divs into responsive `<iframe>` embeds.

## When to Use Each Approach

| Task | Approach | Why |
|------|----------|-----|
| **Lesson plan as PDF** | MD → Pandoc → Typst | Structured stages table, consistent layout, no Typst debugging |
| **Classroom slides** | MD → Pandoc → Reveal.js | Auto-animate, fragments, audio, YouTube, CSS-controlled styling |
| **Worksheets/ handouts** | Raw Typst (if you must) | Highly custom layout (ruled lines, boxes, etc.) — but see SKILL.md first |
| **Bespoke materials** | MD → Pandoc → Typst (preferred) | Even for worksheets, start with Markdown and use Pandoc to get correct Typst. Only drop to raw Typst for pixel-level layout that Pandoc can't express. See `C:\PROJECTS\CONSUMABLES\.kilo\skills\create-formal-ruled-paper\SKILL.md` or `create-formative-ruled-paper\SKILL.md`. |

**Rule of thumb:** If the output has a repeating structure (stages, questions, items), use Pandoc + Lua. The filter handles the repetition. If the output requires absolute positioning, ruled lines at exact spacing, or multi-column layouts that Pandoc doesn't support, you may need raw Typst — but only after consulting the skill document.

## How to Write Lua Filters

Lua filters are functions that Pandoc calls for each element type in the AST:

```lua
-- Filter function names match Pandoc element types
function Header(el)   -- called for each heading
function Para(el)     -- called for each paragraph
function Div(el)      -- called for each fenced div
function Span(el)     -- called for each bracketed span
function Str(el)      -- called for each text string
function Meta(m)      -- called for the document metadata
```

Each function receives the element and must return either:
- The modified element
- A new element (or list of elements) to replace it
- `nil` to delete it
- Nothing to leave it unchanged

### Pattern: Read attribute, wrap in output

```lua
function Div(el)
  if el.classes:includes('my-class') then
    local content = pandoc.utils.stringify(el.content)
    return pandoc.RawBlock('typst', '#block(stroke: blue)[' .. content .. ']')
  end
end
```

### Pattern: Inject raw format blocks

```lua
function Header(el)
  if el.attributes['data-custom'] then
    return {el, pandoc.RawBlock('html', '<div class="custom-annotation">...</div>')}
  end
end
```

### Pattern: Pass-through with modifications

```lua
function Div(el)
  if el.classes:includes('wrap') then
    el.attributes['data-wrapped'] = 'true'
  end
  return el  -- no change, but allows other filters to see the modification
end
```

## Key Constraints & Gotchas

### Markdown Constraints

1. **Lists inside fenced divs need blank lines.** Pandoc requires a blank line before `1.` or `-` items inside `::: {.class}` blocks, otherwise they render as inline text.

2. **Fenced divs must be properly closed.** `:::` opens and `:::` closes. Missing closers break the AST.

3. **Bracketed spans need explicit class.** `[text]{.class}` works, `[text]()` does not (creates a link).

4. **Pipe tables need header separators.** `| A | B |\n|--|--|` — the separator row must have at least 3 dashes per column.

### Lua Filter Traps

1. **`pandoc.utils.stringify()` drops formatting.** Use it only for extracting text, not for preserving content.

2. **Returning `nil` deletes the element.** Return `{}` (empty table) for an empty block.

3. **Multiple filters run in order.** First filter listed runs first. Order matters when filters modify the same elements.

4. **`pandoc.RawBlock` is format-specific.** `pandoc.RawBlock('html', ...)` only appears in HTML output. Use `'typst'` for Typst output, `'latex'` for LaTeX.

### Typst-Specific Issues (Avoided by Pipeline)

| Issue | Raw Typst | Markdown → Pandoc |
|-------|-----------|-------------------|
| `*M*y` mid-word bold | Error | `**M**y` works |
| `#` inside `[...]` | `[\#]` required | Just type `#` |
| `#table()` syntax | Complex, easy to break | Pipe tables |
| `#set text()` position | Must be at top | YAML frontmatter |

## Pandoc 3.10 — New Improvements

Upgraded from 3.7 to 3.10 (2026-06-03). Key improvements relevant to this project:

### Typst Writer Improvements (3.8 → 3.10)

| Version | Improvement |
|---------|-------------|
| 3.10 | `--typst-input` CLI option — pass `sys.inputs` to Typst (like `--input` for direct `typst`) |
| 3.10 | Newline after `#set text` directive — fixes list parsing after font changes |
| 3.10 | Zero-width space before Span labels — prevents Typst errors on empty labels |
| 3.9 | Escape hyphens when needed |
| 3.9 | Fix escaping of quotes |
| 3.9 | Include alt attributes on images |
| 3.9 | Handle `data:` URIs in images (uses `bytes` object instead of SVG workaround) |
| 3.9 | Typst reader supports `#bibliography` — enables `--citeproc` with Typst |
| 3.8 | Fix smart quotes regression for Typst PDF output |
| 3.8 | Template fixes for Typst 0.14 (font, columns, bibliography syntax) |

### Reveal.js Writer Improvements (3.8 → 3.10)

| Version | Improvement |
|---------|-------------|
| 3.10 | (No reveal.js-specific changes in 3.10; general fixes apply) |
| 3.9 | Default `scrollProgress` to `auto` |
| 3.9 | Fix type rendering of scroll-view options in template |
| 3.9 | Idiomatic highlight.js support — `--syntax-highlighting=idiomatic` now generates `<pre><code class="language-X">` format compatible with reveal.js's built-in highlight.js plugin |
| 3.8 | `. . .` pause marker works in nested blocks (fragments inside nested content) |
| 3.8 | New `scroll` and `scrollSnap` options for scrollable slides |

### General Improvements (3.8 → 3.10)

- **3.9:** Defaults files can be JSON or YAML.
- **3.9:** WASM build — Pandoc runs in browser (not relevant to this project).
- **3.8:** New input formats: AsciiDoc, XLSX, PPTX.
- **3.8:** New output format: BBCode.
- **3.8:** `--extract-media` can create a `.zip` archive.

## Tooling Versions

```
pandoc 3.10     (upgraded 2026-06-16 from 3.7.0.2)
typst  0.14.2
Lua    5.4      (Pandoc built-in scripting engine)
```

## Quick Reference: File Locations

| File | Purpose |
|------|---------|
| `scripts/build_lesson_pdf.py` | Orchestrates the PDF pipeline (Markdown → Pandoc → Typst) |
| `scripts/lesson-tables.lua` | Lua filter: transforms `## Stage N:` into Typst tables |
| `scripts/audio-autoplay.lua` | Lua filter: reads `data-audio-src` → injects `<audio data-autoplay>` |
| `scripts/youtube-embed.lua` | Lua filter: `::: {.youtube} id :::` → iframe |
| `scripts/slides-pandoc.css` | CSS for reveal.js slides (yellow headers, shields, fragments) |
| `templates/lesson-plan.typ` | Static Typst template for lesson plan PDFs (never agent-edited) |
| `.kilo/reference/` | This primer and other reference documents |

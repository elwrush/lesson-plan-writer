# Skill: Create Beautiful Slideshows

**Pipeline:** Markdown → Pandoc → reveal.js  
**Author writes:** Pure Markdown only — no HTML, no Typst, no CSS  
**Pandoc handles:** HTML generation, slide structure, attribute propagation  
**Lua filters handle:** Audio autoplay, YouTube embeds  
**CSS handles:** Styling, text shields, fragment colors, responsive sizing

---

## Architecture

The agent writes a single `slides.md` file. Pandoc converts it to reveal.js HTML using `--slide-level=1` (all horizontal slides). Two Lua filters inject native reveal.js features (audio, YouTube) via `pandoc.RawBlock()`. A CSS file handles styling.

**Key principle:** The agent writes ONLY Markdown. Pandoc, Lua filters, and CSS handle everything else.

### Files

| File | Purpose | Location |
|------|---------|----------|
| `slides.md` | The presentation source | `output/{subfolder}/slides/` |
| `index.html` | Generated slideshow (do not hand-edit) | `output/{subfolder}/slides/` |
| `slides-pandoc.css` | Custom styles | `scripts/slides-pandoc.css` |
| `audio-autoplay.lua` | Injects `<audio data-autoplay>` from heading attrs | `scripts/audio-autoplay.lua` |
| `youtube-embed.lua` | Converts `::: {.youtube}` to iframe | `scripts/youtube-embed.lua` |
| `slides-header.html` | `<meta referrer>` for YouTube embeds | `output/{subfolder}/slides/` |
| `assets/` | Images, logos, audio clips | `output/{subfolder}/slides/assets/` |

### Build Command

```bash
# From the slides/ directory:
pandoc slides.md -t revealjs -s --slide-level=1 -o index.html \
  -V revealjs-url="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0" \
  -V theme=black \
  -V margin=0.125 \
  --css="slides-pandoc.css" \
  --include-in-header="slides-header.html" \
  --lua-filter="youtube-embed.lua" \
  --lua-filter="audio-autoplay.lua"
```

### Serve Locally

```bash
python -m http.server 8000
# Open http://localhost:8000/
```

YouTube iframes require HTTP (not `file://`) due to YouTube's referrer policy.

---

## Pandoc Markdown Conventions

### Slide breaks

Every `#` heading creates a horizontal slide. No vertical nesting.

```markdown
# Slide Title

Content here.

# Next Slide

More content.
```

### Heading attributes (slide-level config)

Attributes on `#` headings propagate to the `<section>` element:

```markdown
# Slide Title {data-background-color="#1a1a2e"}

# Splash {data-background-image="assets/img.jpg" data-background-size="cover" data-background-color="#1a1a2e"}
```

Known attributes: `data-background-color`, `data-background-image`, `data-background-size`, `data-background-iframe`, `data-background-interactive`, `data-timer`, `data-audio-src`, `data-transition`.

### Empty headings (splash/end slides)

Use `# ` with only attributes — the empty `<h1>` is hidden by CSS:

```markdown
#  {data-background-image="assets/bg.jpg" data-background-size="cover"}
```

### Fenced divs (classed containers)

`::: {.class}` creates a `<div class="class">`. Used for shields, YouTube embeds, fragments:

```markdown
::: {.title-row}
[**Title text**]{.slide-title}
:::
```

### Bracketed spans (inline classes)

`[text]{.class}` creates `<span class="class">text</span>`. Used for text styling:

```markdown
[**Bold text**]{.cta-text}
```

### Fragments (clickthrough reveals)

```markdown
::: {.fragment .answer-reveal}
Answer content that is hidden until clicked.
:::
```

### Speaker notes

```markdown
::: notes
Hidden notes visible in presenter view (press S).
Time: 2 min. Interaction: T-Ss.
:::
```

### Line breaks within paragraphs

Two trailing spaces force a line break (use for phrase lists):

```markdown
"Phrase one..."  
"Phrase two..."  
"Phrase three..."
```

---

## Slide Patterns

### Title slide (image background with shielded text)

```markdown
#  {data-background-image="assets/bg.jpg" data-background-size="cover" data-background-color="#1a1a2e"}

![](assets/logo.png){.title-logo}

::: {.title-row}
[**Presentation Title**]{.slide-title}
:::

::: {.shield}
Subtitle text
:::

::: {.shield}
[**Call to action**]{.cta-text}
:::
```

### Fragment answer slide (CCQ, comprehension)

```markdown
# Question text here

::: {.fragment .answer-reveal}
**Answer** — source or explanation
:::
```

### YouTube embed (responsive, non-fullscreen)

```markdown
# Video Slide Title

::: {.youtube}
VIDEO_ID_HERE
:::
```

Produces a responsive 16:9 iframe using `youtube.com/embed/`. Requires `youtube-embed.lua`.

### Audio autoplay slide

```markdown
# Slide Title {data-audio-src="assets/audio.mp3"}

Content visible on the slide.
```

The `audio-autoplay.lua` filter injects `<audio data-autoplay src="...">`. Reveal.js plays it when the slide enters, pauses when it leaves.

### Quote + analysis (model answer)

```markdown
# Analysis Title {data-audio-src="assets/clip.mp3"}

> "The quote text here."

::: {.fragment .answer-reveal}
**Evidence:** Type of evidence used.

**Feature:** Linguistic feature description.
:::
```

---

## CSS Classes Reference

| Class | Usage | Effect |
|-------|-------|--------|
| `.title-logo` | Image with `{.title-logo}` | Max-height 108px, centered, block |
| `.title-row` | Fenced div `::: {.title-row}` | Dark shield background, white-space nowrap. **Image backgrounds only.** |
| `.slide-title` | Span `[text]{.slide-title}` | 1.8em bold white |
| `.shield` | Fenced div `::: {.shield}` | Dark semi-transparent background for text on images. **Image backgrounds only.** |
| `.cta-text` | Span `[text]{.cta-text}` | Yellow bold |
| `.cefr-badge` | Span `[B2]{.cefr-badge}` | Blue badge (currently unused) |
| `.answer-reveal` | Fenced div `::: {.fragment .answer-reveal}` | Hidden until clicked, then yellow bold. **Answer keys and CCQs only.** For generic reveals (template blanks, content steps), use plain `::: {.fragment}` to avoid random yellow text. |
| `.iframe-container` | Generated by `youtube-embed.lua` | Responsive 16:9 YouTube iframe |

---

## Design Rules

1. **All slides horizontal** — `--slide-level=1` produces flat `<section>` elements
2. **No fake section labels** — every `#` heading must be student-facing content
3. **Minimal text per slide** — keep headings short, avoid cramming
4. **Yellow headers** — `h1` is `#ffdd00` at 1.3em (CSS handles this)
5. **Text shields on image backgrounds ONLY** — use `::: {.shield}` or `::: {.title-row}` ONLY when the slide has a `data-background-image`. These classes add a dark semi-transparent overlay (`rgba(0,0,0,0.55)`) for text readability against images. On slides with solid background colors or the default black theme, white/yellow text is already readable — do NOT use `.shield` or `.title-row`. Plain markdown is sufficient.
6. **Fragment answers** — use `::: {.fragment .answer-reveal}` for clickthrough reveals
7. **Speaker notes** — every slide should have `::: notes` with timing and interaction
8. **Blockquotes at 0.85em** — CSS handles this for model answer quotes
9. **B2-level discourse markers** — use "It seems to me that...", "Furthermore...", "All things considered..." not "I think..."
10. **Statistics sourced from transcript** — use real data from the BTN video, never invent numbers

---

## What NOT to Do

- **Do not write raw HTML** — use Pandoc Markdown only
- **Do not use `--slide-level=2`** — creates vertical slides (nested sections)
- **Do not use `data-background-iframe`** for YouTube — goes fullscreen, causes Error 153 from file://
- **Do not use `##` headings for slide breaks** — use `#` headings only
- **Do not invent statistics** — source from the BTN transcript or lesson plan
- **Do not use `<!-- .element: class="fragment" -->`** — Pandoc outputs inert HTML comments, not reveal.js directives
- **Do not put the CSS `opacity: 1` on fragment base classes** — breaks reveal.js default hidden→visible behavior

---

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| Vertical slides (down arrow) | Use `--slide-level=1`, not `--slide-level=2` |
| YouTube Error 153 | Serve from HTTP server, not file://. Ensure `slides-header.html` has referrer meta tag |
| Fragment answer always visible | Check CSS doesn't set `opacity: 1` on `.fragment.answer-reveal` (only on `.visible`) |
| Text too wide/narrow | Adjust `margin` in build command: `-V margin=0.125` = 75% content width |
| Blockquote too large | CSS sets `blockquote { font-size: 0.85em }` — check slides-pandoc.css |
| Empty heading showing space | CSS `.reveal h1:empty { display: none }` handles this |
| Audio doesn't play | Check `data-audio-src` is on the `#` heading, not a `##` heading |
| YouTube embed not showing | Ensure `youtube-embed.lua` is in `--lua-filter` and `::: {.youtube}` fenced div is correct |

---

## Workflow (Step by Step)

1. **Read the lesson plan** (JSON or Markdown) for content, stages, timing
2. **Read the BTN transcript** for real statistics (if applicable)
3. **Plan slide order** — splash → title → objectives → content → task → summary → end
4. **Write `slides.md`** in pure Pandoc Markdown
5. **Copy assets** — images, logos, audio files to `assets/`
6. **Copy infrastructure** — CSS, Lua filters, header to the slides directory
7. **Build** — run the pandoc command from the slides directory
8. **Serve locally** — `python -m http.server 8000` from the slides directory
9. **Test** — open http://localhost:8000/, check all slides, fragments, audio, video
10. **Deploy to GitHub Pages** — `/git-pages {subfolder}` (e.g., `/git-pages M3-SPEAKING-TBL-GENDER-ROLES`)
11. **Write URL to lesson plan** — update `slideshow_url` in the lesson plan `.md` file with the GitHub Pages URL
12. **Iterate** — edit slides.md, rebuild, test, redeploy

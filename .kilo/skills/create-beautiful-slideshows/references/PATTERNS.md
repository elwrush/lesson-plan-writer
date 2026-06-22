# Slide Markdown Patterns

Canonical Markdown patterns for every slide type. Read this file BEFORE writing `slides.md`. Do not guess patterns.

---

## Splash slide (first slide, background image only)

A full-bleed background image with no text. Shows before the title slide. Requires:
1. A `title` metadata block at the top of slides.md so Pandoc generates a meaningful `<title>` for the landing page card grid
2. Pedagogical intent annotations injected via `--include-in-header` because the splash is the first section in the HTML and inline comments can't be found by the test lookback

```markdown
---
title: "Voice and Character -- Introduction to Dramatic Reading"
---

#  {#slide-splash data-background-image="assets/splash.jpg" data-background-size="cover"}
```

Create a companion `splash-annotations.html` in the slides directory:

```html
<!-- PEDAGOGICAL INTENT: Students SEE the image before any text -->
<!-- WHY THIS FEATURE: full-bleed data-background-image with zero text -->
<!-- COGNITIVE PRINCIPLE: Multimedia (Mayer) -->
```

Include it in the build command: `--include-in-header="splash-annotations.html"`

---

## Title slide

Single slide — no splash/title split. Background image, logo, rhetorical question in one `.shield`, answer/CTA in another `.shield`. No `.title-row`, no `.slide-title`.

```markdown
#  {#slide-title data-background-image="assets/splash.jpg" data-background-size="cover"}

![](assets/logo.png){.title-logo width=120}

::: {.shield}
Rhetorical question here.
:::

::: {.shield}
[**Answer / call to action here.**]{.cta-text}
:::
```

- Logo: `{width=120}` (bare integer, no `px` unit)
- `.cta-text` uses plain text, NOT bold markers: `[text]{.cta-text}` not `[**text**]{.cta-text}`
- Two `.shield` divs, each holding one line. `shield-block.lua` gives `margin: 0.6em auto` between them.

---

## Single-column grid table (objectives, numbered lists)

```markdown
+------------------------------------------------------------------+
| **1.** Item one that can span multiple lines of text here         |
+------------------------------------------------------------------+
| **2.** Item two                                                  |
+------------------------------------------------------------------+
| **3.** Item three                                                |
+------------------------------------------------------------------+
```

Grid tables have NO header row (no `<th>` yellow styling). All rows are body rows.

---

## Two-column pipe table with Answer column

Leverages `reading-feedback.lua` for white row lines and auto-animate data-ids:

```markdown
| Statement | Answer |
|-----------|--------|
| 1a. Columbus was an Italian explorer. | [**Fact**]{.fragment .answer-reveal} |
| 1b. Columbus was a brave explorer. | [**Opinion**]{.fragment .answer-reveal} |
```

---

## Three-column click-through table (definition + example pairs)

Wrap in `::: {.click-table}` div. Uses `click-table.lua` filter. Each row appears on click.

```markdown
::: {.click-table}
|  |  |  |
|---|---|---|
| **Fact** | can be proven | **FACT:** Columbus sailed from Spain in 1492. |
| **Opinion** | what someone thinks | **OPINION:** Columbus was a brave explorer. |
:::
```

---

## Shield usage rule

- **Image background** → `::: {.shield} / content / :::` (semi-transparent backdrop ensures readability)
- **Plain dark background** → plain paragraphs (the slide background is already dark enough)
- Never use `.shield` on a slide without `data-background-image`

---

## Three-tier differentiation

**Plain dark slide — no shields:**
```markdown
<i class="fa-solid fa-book-open"></i> **Standard** — Full scaffolding, questions visible.

<i class="fa-solid fa-pencil"></i> **Advanced** — Partial scaffolding, notes allowed.

<i class="fa-solid fa-star"></i> **Elite** — Minimal scaffolding, from memory.
```

**Image-background slide — wrap each tier in `.shield`:**
```markdown
::: {.shield}
<i class="fa-solid fa-book-open"></i> **Standard** — Full scaffolding, questions visible.
:::

::: {.shield}
<i class="fa-solid fa-pencil"></i> **Advanced** — Partial scaffolding, notes allowed.
:::

::: {.shield}
<i class="fa-solid fa-star"></i> **Elite** — Minimal scaffolding, from memory.
:::
```

---

## Exercise cycle (transition → skill → task+timer → answers)

Each exercise gets its own four-slide cycle:

```markdown
# Exercise N {#transition-exN data-background-color="#c0392b"}

# Skill for Exercise N {#skill-exN}
**Skill:** Skill name
Pedagogical advice here.

# Exercise N {#task-exN data-timer="300"}
Instructions here.

# Check Your Answers {#answer-exN}
[Answer 1.]{.fragment .answer-reveal}
[Answer 2.]{.fragment .answer-reveal}
```

Lower-order exercises: bare answers (short fragments).
Higher-order exercises: answer + explanation + evidence, one per slide.

---

## Answer slides with paragraph references (higher-order)

```markdown
::: {.split-list}
|  |  |
|---|---|
| **Question** | N — Paragraph X (Author) |
| **[Answer]{.highlight}** | Brief answer here. |
| **[Reason]{.highlight}** | Why this is the answer. |
| **[Evidence]{.highlight}** | *"Direct quote from source text."* |
:::
```

---

## Fragment rule

- Wrap ENTIRE cell content inside `[...]{.fragment .XXX}` — hidden fragment text that takes up space causes unwanted indentation
- **Answers** use `.answer-reveal` (yellow bold on reveal): `[**Fact**]{.fragment .answer-reveal}`
- **Non-answer reveals** use `.white-reveal` (white on reveal): `[flat voice]{.fragment .white-reveal}`
- Requires `white-reveal.lua` filter in the build command to inject the white-reveal CSS

---

## Timer on task slides

```markdown
# Task slide {#task-id data-timer="300"}
```

Read by `timer-inject.lua`. Value in seconds.

---

## Font Awesome icons — yellow

All `<i class="fa-solid fa-...">` tags are colored yellow by `fa-yellow.lua`. Use `[text]{.highlight}` for yellow text on inline content.

---

## YouTube embeds

The video ID must be on its OWN LINE inside the fenced div — never on the opening `::: {.youtube}` line.

```markdown
# Slide heading {#slide-youtube}

::: {.youtube}
VIDEO_ID
:::
```

- Optional start time: append `?start=NNN` to the video ID (e.g. `CvyYEWSK1-w?start=1148` to start at 19:08).
- Requires `youtube-embed.lua` filter and `slide-helper.lua` in the same directory.
- Requires the HTTP server to serve the page (YouTube blocks embeds on `file://`).

---

## Vocabulary slides (phonemic script → word+audio → context)

```markdown
#  {#vocab-navigator}

/ˈnævɪɡeɪtə/

[**navigator**]{.fragment .answer-reveal data-audio-src="assets/vocab-navigator.mp3"}

[Context sentence here.]{.fragment .answer-reveal}
```

Audio plays on FRAGMENT reveal (not slide entry) via `vocab-audio-fragment.lua`.

# Solved Patterns — Body Technology Reading Lesson

## Slide Patterns

### Auto-advance text sequence (replaces autocue)

Use `data-autoslide="2500" data-transition="slide-in slide-out"` on headings. The last slide in the sequence omits `data-autoslide` so the gist question stops and waits.

```markdown
#  {#slide-auto-1 data-autoslide="2500" data-transition="slide-in slide-out"}

**Exoskeletons** help people lift heavy things — up to 20 times their own weight.

#  {#slide-gist}

**What is body technology?**

[**Answer text.**]{.fragment .answer-reveal}
```

### Audio with scrubber (controls)

The `audio-autoplay.lua` filter generates `<audio data-autoplay src="...">` without `controls`. To add a scrubber, use raw HTML directly:

```markdown
# Listen and Read {#slide-listen-read}

<audio data-autoplay controls src="assets/filename.mp3"></audio>
```

### Auto-slide → listen → answer → self-assess sequence

Multi-slide task cycle:
1. Pre-teach vocab slides (one word per slide)
2. Listen-and-read slide (audio + prompt, no questions shown)
3. Answer slide (`data-timer="300"` for 5-min countdown)
4. Gallery-walk instructions (self-assessment)

### Differentiation tiers on plain dark slides

Use three paragraphs with FA icons, no `.shield` wrapper:

```markdown
**Standard** <i class="fa-solid fa-book-open"></i>
Visible prompts. Full scaffolding.

**Advanced** <i class="fa-solid fa-pencil"></i>
Partial scaffolding. Notes only.

**Elite** <i class="fa-solid fa-star"></i>
Memory only. No re-reading.
```

---

## Lesson Plan Patterns

### Template editing

The build script uses `templates/lesson-plan.typ` (project root), NOT `.kilo/skills/build-excellent-lesson-plans/templates/lesson-plan.typ`. Always edit the project-root copy.

### Slideshow URL row always present

Remove the `$if(slideshow_url)$` guard from `templates/lesson-plan.typ`. The row renders unconditionally with an empty gray-shaded cell:

```typst
[*Slideshow URL:*], table.cell(colspan: 3, fill: luma(190))[$if(slideshow_url)$$slideshow_url$$endif$],
```

After template edit, update `.template-lock.json` with the new SHA256.

### SHAPE Literal in models

`src/models.py` SHAPE Literal must cover all lesson plan shapes. Current valid values:
- "ESA", "PPP", "TBL", "Test-Teach-Test", "Guided Discovery"
- "Receptive Skills", "Productive Skills", "Text-based Presentation", "Language Practice"

`shape_name` in YAML must NOT contain `shape` as a substring (avoids "Receptive Skills (Receptive Skills)").

### Vocabulary in lesson plan

`lesson-tables.lua` only captured `Time:` and `Aim:` from `Para` blocks. Any other `Para` (e.g. `**Vocabulary:**`) was silently dropped. Fix: add an `else` branch in the `Para` handler to insert non-matching text into the procedure list.

Blank line required between `**Vocabulary:**` and `- exoskeleton` — without it, Pandoc parses the `-` as a literal hyphen, not a bullet marker.

---

## Typst Patterns

### Page break in Typst output

`\newpage` is ignored by Pandoc's Typst writer. Use raw Typst inline:

```markdown
`#pagebreak()`{=typst}
```

### Vertical centering on page

`#v(1fr)` before and after content pushes it to the vertical center. Must be outside containers.

```markdown
`#v(1fr)`{=typst}

# Question N

Content...

`#v(1fr)`{=typst}

`#pagebreak()`{=typst}
```

---

## PDF Verification

PyPDF2 or PyMuPDF (`fitz`) is required for post-build content extraction. Verify:
- Stage names appear in extracted PDF text
- Stage aims appear
- Vocabulary words appear (if `**Vocabulary:**` present in source)
- No blank-line-before-bullet-list errors (checked via Pandoc AST or pre-build lint)

---

## Build Command (Consolidated)

Use `presentation-defaults.lua` instead of 4 separate presentational filters:

```bash
pandoc slides.md -t revealjs -s --slide-level=1 -o index.html \
  -V revealjs-url="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0" \
  -V theme=black -V width=1280 -V height=720 -V margin=0.04 \
  -V autoSlide=999999 \
   --css="slides-pandoc.css" \
   --include-in-header="slides-header.html" \
   --lua-filter="./presentation-defaults.lua" \
   --lua-filter="./reading-feedback.lua" \
   --lua-filter="./box-keywords.lua" \
   --lua-filter="./shield-block.lua" \
   --lua-filter="./youtube-embed.lua" \
   --lua-filter="./audio-autoplay.lua" \
   --lua-filter="./timer-inject.lua"
```

- `-V autoSlide=999999` required for `data-autoslide` to work
- 6 filters (down from 9) — old `slide-font-size.lua`, `fa-yellow.lua`, `white-reveal.lua`, `vocab-size.lua` consolidated into `presentation-defaults.lua`
- Timer requires `timer-plugin.js`, `timer-plugin.css`, `assets/blip.mp3`, `assets/BELL.mp3`
- Re-copy `slide-helper.lua` after any edit (timer-inject.lua loads it via `dofile`)

## Common Traps

| Trap | Symptom | Fix |
|------|---------|-----|
| `$if(slideshow_url)$` guard | Slideshow URL row missing from PDF | Remove `$if` guard, always render row |
| Wrong template file | Template edits have no effect | Edit `templates/lesson-plan.typ` (project root), NOT `.kilo/skills/...` |
| Missing blank line before bullet list | Markdown items parse as a single paragraph | Insert blank line before `- item` after any `**Heading:**` para |
| lesson-tables.lua drops Para | Vocab/notes disappear from PDF | Add `else` clause in Para handler for non-Time/Aim text |
| `\newpage` in Typst | Page break ignored | Use `` `#pagebreak()`{=typst} `` |
| `#v(1fr)` inside block | "pagebreaks are not allowed inside of containers" error | Place `#v(1fr)` outside any `#block{...}` or `#show: it => block(...)` wrapper |
| `data-audio-src` without controls | No scrubber/seek bar | Use raw `<audio data-autoplay controls src="...">` instead |
| Autocue on GitHub Pages | Teleprompter fails silently due to JS race condition | Use auto-advance slides instead (`data-autoslide` + `data-transition`) |
| `slideshow_url: " "` whitespace-only | Row still hidden (Pandoc treats whitespace as falsy) | Remove conditional guard from template instead |

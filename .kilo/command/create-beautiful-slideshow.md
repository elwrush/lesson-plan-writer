# /create-beautiful-slideshow

## Purpose

Generate a reveal.js slideshow from an existing lesson plan using the Markdown → Pandoc → reveal.js pipeline. All slides are pure Markdown — no HTML.

## Prerequisites

- Pandoc 3.7+ installed
- `scripts/slides-pandoc.css` — custom CSS
- `scripts/audio-autoplay.lua` — audio autoplay Lua filter
- `scripts/youtube-embed.lua` — YouTube embed Lua filter

## Workflow

1. Read the lesson plan (JSON or Markdown) for content, stages, timing
2. Read the BTN transcript for real statistics (if applicable)
3. Plan slide order — splash → title → objectives → content → task → summary → end
4. Write `slides.md` in pure Pandoc Markdown (see skill for conventions)
5. Copy assets (images, logos, audio) to `output/{subfolder}/slides/assets/`
6. Copy infrastructure (CSS, Lua filters, header) to `output/{subfolder}/slides/`
7. Build: `pandoc slides.md -t revealjs -s --slide-level=1 -o index.html -V revealjs-url="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0" -V theme=black -V margin=0.125 --css="slides-pandoc.css" --include-in-header="slides-header.html" --lua-filter="youtube-embed.lua" --lua-filter="audio-autoplay.lua"`
8. Serve: `python -m http.server 8000`
9. Test at http://localhost:8000/

## Notes

- See `.kilo/skills/create-beautiful-slideshows/SKILL.md` for full conventions
- All slides are horizontal (`--slide-level=1`) — no vertical nesting
- Audio uses `data-audio-src` heading attribute (Lua filter injects `<audio data-autoplay>`)
- YouTube uses `::: {.youtube} video-id :::` fenced div (Lua filter converts to iframe)
- Fragments use `::: {.fragment .answer-reveal}` for clickthrough reveals

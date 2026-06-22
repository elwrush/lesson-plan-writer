# Slideshow Architecture

Pipeline, files, build commands, test/serve/deploy procedures. Read this WHEN setting up the `slides/` directory and when building.

---

## Code Libraries (Reusable Lua Module)

All custom Lua filters in `scripts/` share a common library at `scripts/slide-helper.lua`. Loaded at Pandoc compile time via `dofile()`. Never hand-edit during slide generation.

| Function | Purpose | Used by |
|----------|---------|---------|
| `slide.youtube_iframe(id)` | Generates responsive YouTube embed HTML | `youtube-embed.lua` |
| `slide.audio_tag(src)` | Generates `<audio data-autoplay>` HTML | `audio-autoplay.lua` |
| `slide.timer_div(seconds)` | Generates countdown timer overlay | (reserved) |
| `slide.get_attr(elem, key)` | Safely reads an attribute from a Pandoc element | All filters |
| `slide.set_background(header, img, color)` | Sets background-image/color on heading | (reserved) |
| `slide.set_auto_animate(header, id)` | Sets data-auto-animate attributes | (reserved) |

---

## Pandoc Version

This project uses **Pandoc 3.10** (released June 2026). Key features:

| Feature | Since | How to use |
|---------|-------|-----------|
| `--syntax-highlighting=idiomatic` for reveal.js | 3.9 | Adds native highlight.js support |
| Scroll/scrollSnap options | 3.8.3 | `-V scroll=true` enables scroll-based navigation |
| Pause syntax `. . .` in nested blocks | 3.9 | Works in block quotes, lists |

Search GitHub topic `pandoc-filter` for 200+ available community filters.

---

## Files

| File | Purpose | Source |
|------|---------|--------|
| `slides.md` | Presentation source (agent writes this) | Agent writes to `output/{subfolder}/slides/` |
| `index.html` | Generated slideshow (never hand-edit) | Pandoc generates |
| `slides-pandoc.css` | Custom styles (shields, fragments, etc.) | Copy from `scripts/slides-pandoc.css` |
| `slide-helper.lua` | Shared Lua library | Copy from skill's `scripts/slide-helper.lua` |
| `shield-block.lua` | Forces `.shield` to stack vertically | Copy from skill's `scripts/shield-block.lua` |
| `audio-autoplay.lua` | Injects `<audio data-autoplay>` | Copy from skill's `scripts/audio-autoplay.lua` |
| `youtube-embed.lua` | Converts `::: {.youtube}` to iframe | Copy from skill's `scripts/youtube-embed.lua` |
| `box-keywords.lua` | Yellow-bordered boxes | Copy from skill's `scripts/box-keywords.lua` |
| `reading-feedback.lua` | White row lines + auto-animate | Copy from skill's `scripts/reading-feedback.lua` |
| `autocue.lua` | Scrolling teleprompter | Copy from skill's `scripts/autocue.lua` |
| `slides-header.html` | `<meta referrer>` for embeds | Copy from `scripts/slides-header.html` (project root, not skill) |
| `assets/logo.png` | Institution logo | Copy from skill's `templates/ACT.png` |
| `assets/splash.*` | Background image | Pixabay or input folder |

---

## Infrastructure Copy (from skill to slides directory)

```powershell
# Logo
Copy-Item ".kilo/skills/create-beautiful-slideshows/templates/ACT.png" "output/{subfolder}/slides/assets/logo.png"

# Core infrastructure
$skillScripts = ".kilo/skills/create-beautiful-slideshows/scripts"
Copy-Item "$skillScripts/youtube-embed.lua","$skillScripts/audio-autoplay.lua","$skillScripts/slide-helper.lua","$skillScripts/shield-block.lua","$skillScripts/box-keywords.lua","$skillScripts/reading-feedback.lua","$skillScripts/autocue.lua" -Destination "output/{subfolder}/slides/"

# Shared project infrastructure (not in skill)
Copy-Item "scripts/slides-pandoc.css","scripts/slides-header.html" "output/{subfolder}/slides/"
```

**If any `scripts/*.lua` was edited during the session, re-copy with `-Force`.**

---

## Build Command

Run from the `slides/` directory:

```powershell
pandoc slides.md -t revealjs -s --slide-level=1 -o index.html `
  -V revealjs-url="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0" `
  -V theme=black -V width=1280 -V height=720 -V margin=0.04 `
   --css="slides-pandoc.css" `
   --include-in-header="slides-header.html" `
   --lua-filter="./autocue.lua" `
   --lua-filter="./reading-feedback.lua" `
   --lua-filter="./box-keywords.lua" `
   --lua-filter="./shield-block.lua" `
   --lua-filter="./youtube-embed.lua" `
   --lua-filter="./audio-autoplay.lua"
```

Use `./` not `$slidesDir\` to avoid PowerShell path issues.

---

## Validate Before Build

```powershell
python scripts/validate_slides.py output/{subfolder}/slides/slides.md
```

---

## Test After Build

```powershell
python -m pytest tests/test_slide_structure.py --slideshow-html "output/{subfolder}/slides/index.html" -v --tb=short
```

Validates: section IDs, balanced tags, auto-animate pairs, no bare comment closers, pedagogical intent annotations.

---

## Serve (YouTube requires HTTP server — file:// is blocked)

```powershell
background_process start --command "python -m http.server 8000" --workdir "output/{subfolder}/slides/"
```

### Review Checklist

- Title slide (background image, logo, question + CTA in shields)
- All slides navigate with right arrow
- Fragments reveal on click
- Audio autoplays on entry
- YouTube embeds load correctly (requires HTTP server)
- Shields on image backgrounds only
- Speaker notes in presenter view (press S)
- Differentiation tiers on every main task slide

---

## Deploy

```powershell
/git-pages {subfolder}
```

Update `slideshow_url` in the lesson plan `.md` file after deployment.

---

## Before Editing Any .lua File

1. Search via Context7 for the relevant Pandoc Lua filter API function
2. If Context7 is down, fall back to Tavily: `pandoc lua filter <topic>`
3. Cite the search result in the edit rationale

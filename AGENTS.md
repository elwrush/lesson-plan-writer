# AGENTS.md — Lesson Plan Writer 3

## Environment

- **OS:** Windows AMD64 (win32 sys.platform)
- **Shell:** PowerShell
- **Python:** 3.x
- **PowerShell quoting trap:** Inline `python -c "..."` with complex quoting (regex, nested quotes, f-strings with backslashes) ALWAYS hits PowerShell escaping issues. **Never use inline `python -c` for complex code.** Instead: write the Python script to `C:\Users\elwru\AppData\Local\Temp\kilo\*.py` via the Write tool, then execute via `python "C:\Users\elwru\AppData\Local\Temp\kilo\*.py"`. This avoids all quoting problems.

## Golden Rule: Pattern-first, not guess-first

Before writing any Markdown, slide markup, or configuration, **read the template or an existing file that already does what you need**. The correct pattern is always in the codebase already — guessing or generating from training data wastes time and causes errors. Specifically:
- Slide attributes: check `.kilo/skills/create-beautiful-slideshows/SKILL.md` (Pandoc Markdown pipeline)
- Slide structure: check the most recently built `output/*/slides/slides.md`

## Key commands

```bash
# Kilo CLI commands
# /git-backup — Stage all, auto-generate commit message, commit+push to main
# /git-pages — Deploy slides subfolder to gh-pages with landing page
# /lint — Run ruff check --fix and ruff format

# PDF
python scripts/build_lesson_pdf.py output/<subfolder>/<file>.md

# Slides (from slides/ directory)
pandoc slides.md -t revealjs -s --slide-level=1 -o index.html \
  -V revealjs-url="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0" \
  -V theme=black -V width=1280 -V height=720 -V margin=0.04 \
  --css="slides-pandoc.css" \
  --include-in-header="slides-header.html" \
  --lua-filter="youtube-embed.lua" \
  --lua-filter="audio-autoplay.lua"

# Slides — serve locally (required for YouTube embeds)
python -m http.server 8000

# Pixabay image download
python scripts/pixabay_download.py --query "topic" --type image --count 3

# Tests
python -m pytest tests/ -v --tb=short

# Locate slide by reveal.js index (deterministic editing)
python scripts/locate_slide.py "file:///path/to/index.html#/7"
python scripts/locate_slide.py 7 --slides-dir path/to/slides/
```

## Linting & Quality

ruff is installed globally via pip. **Pre-commit hook is permanently uninstalled** (caused git lock contention). Use the `/lint` command instead — it runs encoding checks, then ruff on demand with no background processes.

**Windows UTF-8 trap:** Python on Windows defaults to cp1252 for file I/O and console output. Always use `encoding="utf-8"` when opening project files (`open(path, "r", encoding="utf-8")`). For scripts that print Unicode to the console, add:
```python
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
```
The `check_encoding.py` script (run as part of `/lint`) scans all text files for encoding issues and fixes cp1252→UTF-8.

To avoid cp1252 issues in interactive Python sessions, set `$env:PYTHONUTF8=1` in PowerShell before running Python commands that handle project files. This makes Python default to UTF-8 for all file I/O on Windows.

```bash
# Lint + fix (all files) — replaces pre-commit hook
python -m ruff check --fix .

# Format all Python files
python -m ruff format .

# Both in sequence
python -m ruff check --fix . ; python -m ruff format .

# Run pre-commit checks on all files (without hook, without committing)
python -m pre_commit run --all-files
```

A lint command is defined at `.kilo/command/lint.md` — invoke via Kilo CLI.

## PDF pipeline (Markdown → Pandoc → Typst → PDF)

- **Skill:** `build-excellent-lesson-plans` — writes `lesson.md` with YAML frontmatter + Markdown body
- **Build:** `python scripts/build_lesson_pdf.py output/{subfolder}/lesson.md`
- **Template:** `templates/lesson-plan.typ` (hash-locked, never agent-edited)
- **Lua filter:** `scripts/lesson-tables.lua` — converts `## Stage N:` headings to Typst `#table()`
- **Output:** `PDF/{subfolder}/lesson-plan.pdf`
- **Font:** Roboto OTF via `--font-path`
- Reference: `.kilo/skills/build-excellent-lesson-plans/SKILL.md`

## Slides pipeline (Markdown → Pandoc → reveal.js)

- **Skill:** `create-beautiful-slideshows` — writes `slides.md` in pure Pandoc Markdown
- **Workflow:**
  1. Write `output/{subfolder}/slides/slides.md` in Pandoc Markdown
  2. Copy assets (images, logos, audio) to `output/{subfolder}/slides/assets/`
  3. Copy infrastructure files to `output/{subfolder}/slides/`:
     - `scripts/slides-pandoc.css` → `slides-pandoc.css`
     - `scripts/youtube-embed.lua` → `youtube-embed.lua`
     - `scripts/audio-autoplay.lua` → `audio-autoplay.lua`
      - **Copy** `scripts/slides-header.html` (shared, never write HTML by hand)
  4. Build from the `slides/` directory:
     ```bash
     pandoc slides.md -t revealjs -s --slide-level=1 -o index.html \
       -V revealjs-url="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0" \
       -V theme=black -V width=1280 -V height=720 -V margin=0.04 \
       --css="slides-pandoc.css" \
       --include-in-header="slides-header.html" \
       --lua-filter="youtube-embed.lua" \
       --lua-filter="audio-autoplay.lua"
     ```
  5. Serve locally: `python -m http.server 8000`
- **Lua filters:** `audio-autoplay.lua` (audio from heading attrs), `youtube-embed.lua` (YouTube to iframe)
- **CSS:** `scripts/slides-pandoc.css` — shields, fragments, title row, CEFR badges
- **`slides-header.html`:** shared file at `scripts/slides-header.html` — copy to each slides directory (never write HTML by hand)
- Reference: `.kilo/skills/create-beautiful-slideshows/SKILL.md` (full conventions, slide patterns, CSS reference)

## Content transforms

The agent writes stage aims and dates directly in final form. No Python-level transforms needed.
- Date: `050726` → `7 May, 2026`
- Stage aims: natural English (e.g. "To understand the general idea of the text", not "To reading for gist")
- Procedure: minute indicators stripped (`3 min.` → ``)
- Windows paths: `\` → `/` when needed

## Language quality

Stage aims must read as natural English, not template fills. Unacceptable:
- "To lead-in to the topic of..."
- "To reading for gist"
- "To post-reading speaking task"

Acceptable: "To activate interest in...", "To get the general idea of the text", "To discuss ideas from the reading"

## Slide editing workflow

When editing a slide at a reveal.js URL (e.g., `index.html#/7`):
1. Run `python scripts/locate_slide.py "file:///path/to/index.html#/7"` to find the corresponding `#` heading
2. Edit the `slides.md` file — never edit `index.html` directly
3. Rebuild with `pandoc slides.md -t revealjs ...` (see build command above)
4. Reload the browser

**Always edit `slides.md`, never `index.html`.** The HTML is regenerated from Markdown.

## Research — Pandoc/Lua only

The only output formats are Markdown. Pandoc + Lua filters handle all HTML/Typst generation. If you don't know how to do something:
- **Pandoc Markdown syntax** → search via Tavily or use Context7 for the Pandoc docs
- **Lua filter patterns** → search the Pandoc Lua filter documentation via Context7 or Tavily
- **No raw HTML** — use Pandoc Markdown fenced divs `::: {.class}`, bracketed spans `[text]{.class}`, and heading attributes `{data-key=value}`
- **No raw Typst** — the `build-excellent-lesson-plans` skill's Lua filter handles all Typst table generation

## Image replacement workflow

When asked to replace a slide background image with a Pixabay URL:

1. **Extract image ID** from the URL — e.g. `1407880` from `https://pixabay.com/photos/men-smoke-grill-picnic-forest-1407880/`
2. **Construct CDN URL** — `https://cdn.pixabay.com/photo/{year}/{month}/{day}/{id}_1280.jpg`  
   (Use the `_1280` variant for good resolution with reasonable size)
3. **Download + compress** — write a Python script to `$TEMP\kilo\` and run it (never inline `-c`):
   ```python
   from pixabay_download import compress_image
   from pathlib import Path
   compress_image('CDN_URL', Path('output/SUBFOLDER/slides/assets/FILENAME.jpg'), ID, 1)
   ```
4. **Place output** in `output/{subfolder}/slides/assets/`
5. **Update `data-background-image`** in `slides.md` heading attribute
6. **Rebuild with pandoc**

The `compress_image` function: resize to 1920px max edge, JPEG quality=80, optimize=True (Pillow).

## Consumables — moved to separate project

Ruled paper, bookbinding, and PDF template insertion have moved to `C:\PROJECTS\CONSUMABLES` (https://github.com/elwrush/consumables). Run consumable workflows from that project, not here.

## Codebase audit

Run the full audit pipeline from any project root:
```powershell
python "C:\Users\elwru\.config\kilo\skills\audit-codebase\scripts\find_dead_code.py" --root .
python "C:\Users\elwru\.config\kilo\skills\audit-codebase\scripts\map_redundancy.py" --root .
python "C:\Users\elwru\.config\kilo\skills\audit-codebase\scripts\check_doc_alignment.py" --root .
python "C:\Users\elwru\.config\kilo\skills\audit-codebase\scripts\find_hallucinations.py" --root . --skip-urls
```
All four scripts are stdlib-only. Reports write to `audit-*.md` at the project root.

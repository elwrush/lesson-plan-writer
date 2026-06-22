# AGENTS.md — Lesson Plan Writer 3

## Self-Improvement Loop

At session start, read `C:\Users\elwru\.kilo\learnings.md` and apply any relevant lessons tagged `[lesson-plan-writer]`. After completing a fix or discovering a better approach, append an entry to that file with date, context, fix, and pattern.

## Pre-session Checklist (Run BEFORE any work)

1. **Load learnings** — `read("C:/Users/elwru/.kilo/learnings.md")` for `[lesson-plan-writer]` entries
2. **Load the skill** — `skill("create-beautiful-slideshows")`
 3. **Read Proven Markdown Patterns** in `.kilo/skills/create-beautiful-slideshows/SKILL.md`. The skill is the canonical reference — not the most recently built slides.md, which may use outdated patterns. Read the full Title slide, Objectives, and Fragment sections before writing slides.md.
4. **Audit existing work** — if resuming a session, run `git status` and `git diff --name-only` to see what changed

## Skill Authoring Rule

**Every SKILL.md must follow `.kilo/skills/_TEMPLATE.md`.** Before creating or editing any skill, read the template verbatim. The template defines the required sections and their order:

1. YAML frontmatter (`name`, `description`)
2. `## Purpose` with Output line
3. `## When to Use` with conditions, Trigger, and anti-patterns
4. `## Workflow (N Steps)` — numbered steps, each a coherent action
5. `## Examples` — at least 2 real scenarios
6. `## Error Handling` — symptom/cause/fix table
7. `## Reference` — files in `reference/` subdirectory
8. `## Scripts` — automation scripts shipped with the skill

If you find a skill that doesn't match this structure, restructure it. Ignorance of the template is not an excuse — agents are expected to find and apply it.

## Execution Gates (MANDATORY — violations cause 2-hour sessions)

### Gate 1: Blueprint Approval Gate
**Before any slides.md is written, the blueprint must be reviewed and approved by the user.**
- Write the blueprint at `.kilo/plans/{lesson}-blueprint.md`
- Present it for review
- **Wait for explicit approval** — do NOT write slides.md until told "approved"
- If the blueprint is rejected, fix it and re-present. Do not proceed until approval is received.
- The blueprint must include exact Markdown patterns, not descriptions. Every slide gets a code block showing the precise syntax.

### Gate 2: One-Issue → Full-Audit Rule
**When the user reports ONE problem, do NOT fix just that problem.** Immediately read the ENTIRE slides.md against the SKILL.md and blueprint. Find and list ALL deviations. Fix them in ONE pass. Present the full list before editing.

### Gate 3: Skill Re-load Rule
**After any rejection or failure, re-load the relevant SKILL.md** to refresh the pedagogical principles before making the next edit. The patterns are documented there — reading them eliminates guesswork.

### Gate 4: Research Before Syntax
**Never write Pandoc syntax you haven't verified.** Before ANY table, grid, pipe, or complex Markdown:
1. Search Context7 for "pandoc markdown grid table" or equivalent
2. Check the MOST RECENT slides.md for the pattern
3. Only then write Markdown

### Gate 5: No Shared Lua Edits
**Never modify scripts/*.lua files** that are shared infrastructure. `reading-feedback.lua`, `slide-helper.lua`, `shield-block.lua`, `box-keywords.lua`, `audio-autoplay.lua`, `youtube-embed.lua` are shared across ALL projects. Create new standalone filters in `scripts/` with unique names. If a shared filter needs a behavioral change, ask the user first.

### Gate 6: Hallucination Guard
**After writing any answer slide, verify every stat and fact against the source transcription.** If the source doesn't contain a specific number, date, or location, do not include it. "The Pacific is the largest ocean" (source says this) is fine. "63 million square miles" (not in source) is a hallucination.

## Workflow: Blueprint-first, then slides

**Never write slides.md directly.** The blueprint is the design document; slides.md is a mechanical translation.

### Phase 1: Write the Blueprint

File: `.kilo/plans/{lesson}-blueprint.md`

Write a per-slide design table. For EVERY slide, answer:

| Slide ID | Intent (what teacher says) | Feature | Principle | Mechanism | Content |
|----------|---------------------------|---------|-----------|-----------|---------|
| unique-id | Teacher script / purpose | Which feature(s) used | Why this feature here | How it's implemented | Approx word count |

Feature choices (from existing Lua filters, not bespoke code):
- **auto-animate** — jumbled→correct table pairs for visual process demonstration. ALL non-moving elements must get stable `data-id`.
- **boxed text** — `[keyword]{.box}` via `box-keywords.lua`. Use ONLY for critical vocabulary, signal phrases, grammar targets. Never box answers.
- **fragments** — `[**answer**]{.fragment .answer-reveal}` for click-through reveals (video answers, vocab answers).
- **tables** — Pandoc pipe tables for structured data. `reading-feedback.lua` adds white row lines and auto-animate data-ids to tables with an "Answer" column.
- **red transitions** — `data-background-color="#c0392b"` on section headings for cognitive phase breaks.
- **challenge tiers** — FA icons (`fa-book-open`, `fa-pencil`, `fa-star`) with bold labels. Full descriptions first time, icons-only thereafter.

Blueprint must be reviewed and approved before any slides.md writing begins.

### Phase 2: Write slides.md

Translate the blueprint into Pandoc Markdown. No pedagogical decisions at this stage — pure mechanical conversion.

```markdown
# Slide Heading {#slide-id data-feature="value"}

::: {.feature-class}
Content
:::
```

### Phase 3: Build and test

```powershell
$slidesDir = Resolve-Path "."
pandoc slides.md ... (see build command below)
python -m pytest tests/ -v --tb=short -k "{lesson-slug}"
```

After tests pass, run the audit-codebase pipeline to catch structural issues before committing:

```powershell
python "C:\Users\elwru\.config\kilo\skills\audit-codebase\scripts\find_dead_code.py" --root .
python "C:\Users\elwru\.config\kilo\skills\audit-codebase\scripts\map_redundancy.py" --root .
python "C:\Users\elwru\.config\kilo\skills\audit-codebase\scripts\check_doc_alignment.py" --root .
python "C:\Users\elwru\.config\kilo\skills\audit-codebase\scripts\find_hallucinations.py" --root . --skip-urls
```

Review `audit-*.md` reports for any BLOCKER findings and fix before committing.

### Slide sequence template

```
1. title           — background image, logo, rhetorical question + CTA in two `.shield` divs
2. objectives      — table: left column numbers, right column objectives
3. transition      — red background if major phase shift
4. strategy        — pedagogical advice (auto-animate or plain list)
5. task+timer      — instruction + timer pill
6. answers         — lower order: bare answers. Higher order: answer + explanation + evidence, one per slide
```

## Environment

- **OS:** Windows AMD64 (win32 sys.platform)
- **Shell:** PowerShell
- **Python:** 3.x
- **PowerShell quoting trap:** Inline `python -c "..."` with complex quoting (regex, nested quotes, f-strings with backslashes) ALWAYS hits PowerShell escaping issues. **Never use inline `python -c` for complex code.** Instead: write the Python script to `C:\Users\elwru\AppData\Local\Temp\kilo\*.py` via the Write tool, then execute via `python "C:\Users\elwru\AppData\Local\Temp\kilo\*.py"`. This avoids all quoting problems.

## Codebase search

Choosing the right search method:

| You want to... | Use | Why |
|---|---|---|
| Find a literal string (no regex) | `rg -F "text"` via bash | Fastest, no escaping needed |
| Match a pattern (word, prefix, structure) | `grep` tool with `include="*.py"` | RegExp with scoping; built-in tool |
| Find files by name pattern | `glob` tool with `pattern="**/*.py"` | Globbing, not regex |
| Search across specific file types | `grep` tool with `include="*.{py,md}"` | Scoped, no noise |
| Multi-line / structural pattern | `rg -U -z` via bash, or `task` explorer agent | Regex can't do multi-line well; an agent can read + reason |
| Find where a feature/concept is implemented | `task(..., subagent_type="explore")` with a prompt describing what it does | Matches intent, not just text |
| Search all code history | `git log -p -S "pattern" -- "*.py"` via bash | Searches commits, not just working tree |

Tools available: `rg` (ripgrep), `Select-String` (PowerShell), built-in `grep`/`glob` tools.

## Golden Rule: Pattern-first, not guess-first

Before writing any Markdown, slide markup, or configuration, **read a template or reference section in the relevant SKILL.md**. The SKILL.md's templates are the sole canonical reference — not the most recently built slides.md, which may use outdated or rejected patterns. Specifically:
- Slide attributes: check `.kilo/skills/create-beautiful-slideshows/SKILL.md` (Pandoc Markdown pipeline)
- Slide structure: check the SKILL.md's Proven Markdown Patterns section (the template patterns, not past builds)
- Lua filter patterns: check an existing `scripts/*.lua` file
- **Do NOT read .css, .html, or .htm files** — these are generated output or shared styling, not patterns to follow
- **Do NOT read previous slides.md files** — they may reflect inferior past knowledge, bias new work, and hinder learning. The SKILL.md is the authority.

## Key commands

```bash
# Kilo CLI commands
# /git-backup — Stage all, auto-generate commit message, commit+push to main
# /git-pages — Deploy slides subfolder to gh-pages with landing page
# /lint — Run ruff check --fix and ruff format

# PDF
python scripts/build_lesson_pdf.py output/<subfolder>/<file>.md

# Slides (from slides/ directory)
$slidesDir = Resolve-Path "."
pandoc slides.md -t revealjs -s --slide-level=1 -o index.html \
  -V revealjs-url="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0" \
  -V theme=black -V width=1280 -V height=720 -V margin=0.04 \
   --css="slides-pandoc.css" \
   --include-in-header="slides-header.html" \
   --lua-filter="$slidesDir\autocue.lua" \
   --lua-filter="$slidesDir\reading-feedback.lua" \
   --lua-filter="$slidesDir\split-list.lua" \
   --lua-filter="$slidesDir\click-table.lua" \
   --lua-filter="$slidesDir\left-table.lua" \
   --lua-filter="$slidesDir\fa-yellow.lua" \
   --lua-filter="$slidesDir\vocab-audio-fragment.lua" \
   --lua-filter="$slidesDir\timer-inject.lua" \
   --lua-filter="$slidesDir\box-keywords.lua" \
   --lua-filter="$slidesDir\shield-block.lua" \
   --lua-filter="$slidesDir\youtube-embed.lua" \
   --lua-filter="$slidesDir\audio-autoplay.lua"

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

## Lua Filter Quality — Static Type Checking

Lua filters use **Lua Language Server (LuaLS)** with `rnwst/pandoc-lua-types` for static type checking and autocompletion.

**Setup is already in place:**
- `lua-language-server` — installed via Scoop at `C:\Users\elwru\scoop\shims\lua-language-server.exe`
- `.luarc.json` — project root config, points `workspace.library` to `.lua/`
- `.lua/` — upstream `rnwst/pandoc-lua-types` type definitions for pandoc's Lua API

**Before writing any Lua filter, run static analysis:**
```powershell
lua-language-server --check="scripts/my-filter.lua" --config=".luarc.json"
```

This catches: undefined fields, type mismatches, wrong return types, and missing pandoc API functions — all before pandoc runs. Use this as the pre-write gate, analogous to `typst-check` for `.typ` files.

If `lua-language-server` reports a type error for a pandoc function you're calling, check that the function exists in `pandoc.org/lua-filters.html` for your pandoc version. The type defs track the upstream API; a mismatch usually means the API changed between versions.

**To update type definitions** (when pandoc updates):
```powershell
Remove-Item -Recurse -LiteralPath ".lua" -Force
git clone --depth 1 https://github.com/rnwst/pandoc-lua-types.git .lua
Remove-Item -Recurse -LiteralPath ".lua/.git" -Force
Remove-Item -LiteralPath ".lua/.gitmodules", ".lua/README.md", ".lua/COPYING", ".lua/lua-reader-writer-options.ods" -ErrorAction SilentlyContinue
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
      - `scripts/slide-helper.lua` → `slide-helper.lua` (required by both Lua filters)
      - `scripts/shield-block.lua` → `shield-block.lua` (forces adjacent `.shield` divs to stack vertically)
      - `scripts/youtube-embed.lua` → `youtube-embed.lua`
      - `scripts/audio-autoplay.lua` → `audio-autoplay.lua`
      - `scripts/box-keywords.lua` → `box-keywords.lua` (yellow-bordered boxes for key terms)
      - `scripts/reading-feedback.lua` → `reading-feedback.lua` (auto-animate table feedback)
      - `scripts/autocue.lua` → `autocue.lua` (teleprompter scrolling text)
      - **Copy** `scripts/slides-header.html` (shared, never write HTML by hand)
      - **Note:** If any `scripts/*.lua` was edited during the session, re-copy it with `-Force` to ensure the slides directory has the latest version.
  4. Build from the `slides/` directory:
     ```bash
     pandoc slides.md -t revealjs -s --slide-level=1 -o index.html \
       -V revealjs-url="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0" \
       -V theme=black -V width=1280 -V height=720 -V margin=0.04 \
        --css="slides-pandoc.css" \
        --include-in-header="slides-header.html" \
        --lua-filter="./autocue.lua" \
       --lua-filter="./reading-feedback.lua" \
       --lua-filter="./split-list.lua" \
       --lua-filter="./click-table.lua" \
       --lua-filter="./left-table.lua" \
       --lua-filter="./fa-yellow.lua" \
       --lua-filter="./vocab-audio-fragment.lua" \
       --lua-filter="./timer-inject.lua" \
       --lua-filter="./box-keywords.lua" \
       --lua-filter="./shield-block.lua" \
       --lua-filter="./youtube-embed.lua" \
       --lua-filter="./audio-autoplay.lua"
     ```
     Note: Use `./` not `$slidesDir\` to avoid PowerShell path resolution issues. The `autocue.lua` and other shared filters require `slide-helper.lua` in the same directory — this is set up in the copy step above.
  5. Serve locally: `python -m http.server 8000`
- **Lua filters:** `audio-autoplay.lua` (audio from heading attrs), `youtube-embed.lua` (YouTube to iframe)
- **CSS:** `scripts/slides-pandoc.css` — shields, fragments, title row, CEFR badges
- **`slides-header.html`:** shared file at `scripts/slides-header.html` — copy to each slides directory (never write HTML by hand)
- Reference: `.kilo/skills/create-beautiful-slideshows/SKILL.md` (full conventions, slide patterns, CSS reference)

## Differentiation (Tiered Challenges)

Every main task slide must offer **three-tier differentiation** (Standard / Advanced / Elite) to accommodate the wide ability range in class:

- **Standard:** Full scaffolding — task prompts visible during input/activity
- **Advanced:** Partial scaffolding — students take notes, then answer from notes
- **Elite:** Minimal scaffolding — students complete from memory and understanding alone

**Display pattern:**
- **Plain dark slides (no image background):** Three paragraphs with bold tier labels and Font Awesome icons — no `.shield` wrapper
- **Image-background slides:** Three stacked `.shield` divs (dark backdrop ensures readability over the image)

Font Awesome icons (`fa-solid`) are loaded via `slides-header.html`. Use `fa-book-open` for Standard, `fa-pencil` for Advanced, `fa-star` for Elite.

This applies to reading, listening, speaking, and writing task slides. See `.kilo/skills/create-beautiful-slideshows/SKILL.md#pedagogical-requirements` for the full framework and examples.

Non-task slides (lead-in, transition, summary, title) are exempt.

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

## CSS/HTML FILES ARE FORBIDDEN

- Do NOT read any .css, .html, or .htm file
- Do NOT edit any .css, .html, or .htm file
- slides-pandoc.css is **hash-locked** — `validate_slides.py` fails the build if it has been modified (even whitespace)
- slides-header.html is **copy-only** — its source is at `scripts/slides-header.html`; never write HTML by hand
- If a visual problem exists, the fix is ALWAYS in Pandoc Markdown or a Lua filter — NEVER in CSS
- The `style=` attribute is forbidden in slides.md — use Pandoc fenced divs, bracketed spans, or Lua filters

## Research — Pandoc/Lua only

The only output formats are Markdown. Pandoc + Lua filters handle all HTML/Typst generation. If you don't know how to do something:
- **Pandoc Markdown syntax** → Context7 first (faster, authoritative). Fall back to Tavily: "pandoc markdown \<topic\>"
- **Lua filter patterns** → Context7 first for the Pandoc Lua filter API. Fall back to Tavily: "pandoc lua filter \<topic\>"
- **Before ANY edit to a .lua file** (shield-block.lua, youtube-embed.lua, etc.):
  1. Search via Context7 for the relevant Pandoc Lua filter API function
  2. If Context7 is down or doesn't have the answer, fall back to Tavily web search: `pandoc lua filter <topic>`
  3. Cite the search result in the edit rationale
- **No raw HTML** — use Pandoc Markdown fenced divs `::: {.class}`, bracketed spans `[text]{.class}`, and heading attributes `{data-key=value}`
- **No inline CSS (`style=`) in slides.md** — all styling goes through shared CSS files or Lua filters. The validation script (`validate_slides.py`) will fail the build if `style=` is found in Markdown. The test suite (`tests/test_validate_slides.py::TestCheckInlineCss`) enforces this as red-green.
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

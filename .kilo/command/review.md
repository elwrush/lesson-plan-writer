---
description: Run lint, tests, and comprehensive quality review of uncommitted changes against all project conventions in AGENTS.md. Invoke before /git-backup.
---

# Command: Review

## What it does
1. Runs lint (ruff check + ruff format)
2. Runs all tests (pytest)
3. Shows uncommitted changes (git diff)
4. Reviews changed files against EVERY project-specific quality rule from AGENTS.md
5. Reports pass/fail with specific violations

## Workflow

### Phase 1: Automated Checks

Run lint first:

```powershell
python -m ruff check --fix . ; python -m ruff format .
```

Run all tests:

```powershell
python -m pytest tests/ -v
```

If either fails, **stop and report the failure**. Do not proceed to Phase 2.

### Phase 2: Uncommitted Changes Audit

Show what changed:

```powershell
git diff --stat
```

If nothing to review ("nothing to commit, working tree clean"), report "No uncommitted changes — review complete" and exit.

Show the full diff:

```powershell
git diff
```

### Phase 3: Quality Review

For each changed file, check the file type and evaluate ALL applicable rules below. Report ANY violation found.

---

#### HTML Slides (`output/*/slides/index.html`)

1. **Icon placement**: Icons in pedagogical strategy headers must be inline `<span style="font-size: 2.5em;">` left of `<h2>` inside an `overflow: hidden` div. NOT centered block.
2. **Icon mapping** correct per slide type: transition = `fa-forward red #c0392b`, strategy = `fa-list-check`/`fa-chess` teal `#1a6b5a`, task = `fa-pencil`, discussion = `fa-comments` red, objective = `fa-seedling`, vocabulary = `fa-spell-check`, summary = `fa-flag-checkered`.
3. **Transition icons**: use `fa-forward`, red `data-background-color="#c0392b"`, `class="transition-icon"`. NOT any other icon or color.
4. **Answer slides**: lightbulb icons removed. No `fa-lightbulb` anywhere in answer `<section>`s.
5. **Answer tables**: `<table class="answer-table">` with exactly 3 columns (Statement/Answer/Why?). Add `wrap` class for long text. Right column uses `white-space: normal`.
6. **Table tick/cross**: middle column uses `data-fragment-index` matching the explanation cell for simultaneous reveal.
7. **Fragment strike**: `class="fragment strike"` on td/p elements. NOT `class="fragment highlight-green"` or any `highlight-*` class (those force `opacity: 1` and never hide).
8. **Custom fragment CSS**: `answer-correct`/`answer-incorrect` classes used instead of `highlight-green`/`highlight-red` for background reveals.
9. **Auto-animate**: only between adjacent slides with matching `data-id` on elements. The previous slide must NOT have `data-auto-animate`.
10. **Pedagogical**: `data-background-color="#1a6b5a"` + `class="pedagogical"` + `data-background-transition="none"` on all strategy slides.
11. **Pedagogical alignment**: `padding-top: 30px` via CSS (NOT negative margin-top). Inline `style="top: 0;"` on the `<section>` if needed.
12. **Step labels**: format `<p><u><strong>Step N:</strong> description</u></p>`.
13. **One step per slide**: each strategy step is its own `<section>`. No two steps in one slide.
14. **Header on first slide only**: strategy block heading only on Slide 1. Remaining slides show only step label.
15. **Original question in yellow**: `<p style="color:#ffdd00;"><em>"..."</em></p>` on first and last strategy slide of each block.
16. **Real quotes on Step 4**: actual article text excerpts in italics with highlighted phrase.
17. **Rule embedded at Step 2**: "If you answer Yes to all → TRUE. If you answer No to even one → FALSE." Not a separate slide.
18. **Auto-animate underline reveal**: uses two `<section data-auto-animate>` with transparent → white border transition. NOT `class="fragment"` for keywords (fragments cause blank space with `opacity: 0`).
19. **Background transition**: `data-background-transition="none"` on all pedagogical slides.
20. **Pixabay backgrounds**: NOT used in generated output. All backgrounds are solid colors via `data-background-color="<color>"`.
21. **One consistent example**: same exam question carried through all steps of a strategy block. No mid-flow example switching.
22. **No `data-markdown`**: all slides are raw HTML `<section>`. Markdown pipeline is permanently abandoned.
23. **Answer slides not used for strategy steps**: strategy steps have teal background; answer/confirmation slides have green `#0d5e1a` background.
24. **Summary background**: white (default). End slide: `data-background-color="#2c3e50"`.

---

#### JSON (`output/*/*.json`, `knowledge-base/lesson plan shapes/json/*.json`)

1. **Underscore keys**: `lesson_plan`, `answer_key`. NOT `answer-key` or `lesson-plan`.
2. **Required top-level**: `teacher`, `lesson_plan`. `lesson_plan` must contain `stages`.
3. **Each stage**: `stage_number`, `stage`, `stage_aim`, `procedure`, `time`, `interaction`.
4. **`answer_key` value**: `"none"` or a valid path string to `.typ` markup.
5. **Shape templates**: at `knowledge-base/lesson plan shapes/json/shape-{letter}.json`.

---

#### Python (`scripts/*.py`)

1. **Language quality transforms active**: `humanize_stage_aim` removes banned template fills. Banned: "To lead-in to...", "To reading for gist", "To post-reading speaking task".
2. **Date formatting**: `format_date()` converts `DDMMYY` → "D Month, YYYY" (e.g. `050726` → `7 May, 2026`).
3. **Minute indicators stripped**: `strip_minute_indicators()` removes `"3 min."` etc from procedure text.
4. **Answer key**: `.typ` files read directly — no markdown conversion.
5. **Windows paths**: `\` converted to `/` for Typst.
6. **No deprecated `json_to_markdown.py`** usage for new presentations.
7. **No new `data-markdown`** usage — markdown pipeline abandoned.
8. **No hardcoded secrets/tokens** — all credentials externalized.
9. **No hallucinated imports** — imports must match known project deps (Pillow, requests, etc).
10. **No unused imports** — ruff will catch these.
11. **Error handling** for external tools (typst compile, subprocess calls).

---

#### Typst (any `.typ` files or generated Typst content in Python strings)

1. **Font**: Roboto OTF from `%APPDATA%\TinyTeX\texmf-dist\fonts\opentype\google\roboto\` via `--font-path`.
2. **Leading**: `#set par(leading: 0.55em)` — leading is **additional** space, NOT a multiplier.
3. **Top margin**: 1.25in (prevents logo clipping on print).
4. **Logos**: page 1 only via `context { if counter(page).get().first() == 1 { ... } }`.
5. **Logo files**: `templates/Image_20260324_141022.png` (ACT), `templates/cambridge.png` (Cambridge).

---

#### General code quality (all changed files)

1. **No hardcoded secrets, API keys, or tokens** in any file.
2. **No hallucinated dependencies** — check imports/packages against known project dependencies.
3. **No commented-out dead code** without a clear purpose comment.
4. **No TODO/FIXME left in production code** without tracking.
5. **Consistent project conventions** — match surrounding code style in the same file.

---

### Phase 4: Report

Build a structured summary:

```powershell
Write-Host "`n=== REVIEW REPORT ==="
Write-Host "`n--- Phase 1: Automated Checks ---"
# Report lint exit code
# Report test results (passed/failed count)
Write-Host "`n--- Phase 2: Changed Files ---"
# List files changed
Write-Host "`n--- Phase 3: Quality Violations ---"
# List each violation found, with file path and rule reference
# If none found: "None — all rules pass"
Write-Host "`n=== CONCLUSION ==="
```

- If ALL checks pass: "✅ Review passed — ready for /git-backup"
- If ANY violation found: "❌ Review failed — fix the issues listed above before committing"

## Edge cases

- **No uncommitted changes**: report and exit cleanly (not an error)
- **Lint fails**: stop — do not proceed to quality review (code must be clean first)
- **Tests fail**: stop — do not proceed to quality review
- **New file types not covered by checklist**: report "unreviewed file type" so rules can be added

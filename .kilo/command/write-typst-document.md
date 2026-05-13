---
description: Create or edit Typst (.typ) documents. Loads the typst-document-creator skill for the full pipeline — source consultation, syntax verification against the packed repo, code generation, formatting, compilation, and integrity checking.
---

# Command: Write Typst Document

## Usage
`/write-typst-document <path/to/file.typ>`

Create or edit a `.typ` file for a lesson plan template, PDF component, or standalone document.

## What it does
1. Loads the `typst-document-creator` skill (which internally loads `typst-author` for syntax reference)
2. Creates or opens a `.typ` file at the specified path, OR creates a new document in `typst/code/{subfolder}/`
3. Verifies all Typst syntax against `knowledge-base/typst-packed.json` before writing
4. For new documents: follows the full pipeline (source → header → format → generate → RED→GREEN tests → compile → integrity check)
5. For existing files: reads first, edits, formats, compiles, reports
6. Validates with `typst compile` to catch errors
7. Reports results

## Prerequisites
- Typst CLI installed (`typst compile`)
- `typstyle` installed for formatting (optional — skip checks if missing)
- `knowledge-base/typst-packed.json` — **MANDATORY**. Every function call, parameter, set rule, and show rule must be verified against this file before writing.

## Workflow

### Step 1: Load the skill
```
skill typst-document-creator
```

This loads the document creation pipeline, syntax reference (via the bundled `typst-author` dependency), troubleshooting guide, and the full docs tree.

### Step 2: Determine mode
- If `<path/to/file.typ>` is provided: **edit mode** — read existing file, edit, format, compile, report
- If no path is provided: **create mode** — follow the `typst-document-creator` workflow (source → header → format → generate → compile → integrity check)

### Step 3: Consult the packed repo for syntax — MANDATORY
**Never guess Typst syntax from training data.** Every function call must be confirmed against the packed repo first. Follow the concrete query protocol in the typst-document-creator skill (Step 4, section 3). Secondary sources:
- `.kilo/skills/typst-author/docs/reference/syntax.md` — syntax fundamentals
- `.kilo/skills/typst-author/docs/reference/styling.md` — set/show rules and themes
- `.kilo/skills/typst-author/docs/guides/page-setup.md` and `.kilo/skills/typst-author/docs/guides/tables.md` — page layout and tables
- `knowledge-base/typst-packed.json` — full Typst codebase reference
- `.kilo/skills/typst-author/docs/reference/<category>/` — specific function reference

### Step 4: Create or edit the .typ file
- **Edit mode**: Write the file following idiomatic Typst patterns from the skill's quick-start example and reference docs
- **Create mode**: Follow typst-document-creator Steps 1–4b (source → header → format → generate → RED→GREEN tests)

### Step 5: Run post-edit formatting checks
```powershell
# Check if typstyle is available
$hasTypstyle = (Get-Command typstyle -ErrorAction SilentlyContinue) -ne $null

if ($hasTypstyle) {
    # Check formatting
    typstyle --check <file>
    # If fails, inspect diff before formatting
    if ($LASTEXITCODE -ne 0) {
        typstyle --diff <file>
    }
}
```

Only auto-format (`typstyle -i <file>`) when changes are limited to a newly created file or to code you just edited. If the diff touches untouched pre-existing code, ask the user.

### Step 6: Compile and validate
```powershell
typst compile --root "." <file.typ>
```

For new documents created via the typst-document-creator workflow, compile to both the specified path and to `typst/PDF/{subfolder}/`.

On error, read the error message and consult the skill's troubleshooting section or relevant docs.

### Step 7: Report
Summarize what was created/edited, any formatting applied, compilation result, and integrity check result (if applicable).

## Edge cases
- **No file path**: Enter **create mode** — launch the typst-document-creator workflow
- **typstyle not available**: Skip formatting checks (not required for valid output)
- **Compilation error**: Show the error with line number and suggested fix from docs
- **Missing font**: "Font warning — document compiles with fallback fonts"
- **Document already exists**: Read first, then edit — never overwrite without reading
- **Integrity check fails**: Warn and continue (never halt)

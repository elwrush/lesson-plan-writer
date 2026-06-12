---
description: Creates bespoke teaching materials with headed ruled-paper formatting — Mathayom header, student demographics (from Supabase or blank), ruled writing lines at 24pt spacing. Booklet mode: A4 pages, 14pt body, 4-page signatures, combined by class.
---

# Command: Create Bespoke Materials

## Usage
`/create-bespoke-materials`

No arguments. Fully interactive flow.

## What it does
1. Loads the `create-bespoke-materials` skill (all rules/patterns there)
2. Loads the `insert-pdf-to-template` skill (for PDF/image injection)
3. Interactively gathers: input type, description, level, demographics (Supabase classlist or blank fields), format (booklet/standard), transcript preference
4. Generates A4 PDFs at 14pt body (printer booklet function handles A5 folding)
5. Pads each student to 4-page multiple; combines by class
6. Runs linter post-generation (font sizes, page counts, text fill, outline breaks)
7. Reports output paths

## Workflow
1. `skill create-bespoke-materials`
2. Follow interactive Q&A (6 questions — see skill for exact wording)
3. Run linter: `python scripts/linter_bespoke.py --dir "PDF/{topic}-BOOKLETS"`
4. Report output path(s) and linter results

## Critical rules (read the skill before running)
- A4 pages, 14pt body — NOT A5
- `box(stroke: bottom)` for blanks — NOT `underline(h(...))`
- `line()` in loop for ruled lines — NOT `table.hlines()` or `tiling()`
- `black` strokes only — NOT `luma()` grays
- `.typ` files inside project root — NOT in temp dir
- `1\.` at line start — NOT `1.` (prevents list detection)

## Prerequisites
- `typst compile` CLI available
- `pymupdf` (fitz) installed
- Roboto OTF fonts: `%APPDATA%\TinyTeX\texmf-dist\fonts\opentype\google\roboto\`
- `supabase` CLI logged in: `supabase login --token $env:SUPABASE_ACCESS_TOKEN`
- Tinymist LSP: `tinymist compile` for pre-check

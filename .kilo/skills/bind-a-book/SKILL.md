---
name: bind-a-book
description: Converts text files (epub, pdf, txt, md) into A5 booklet PDFs with serif typography, book-standard margins, optional gloss footnotes, and a title page.
---

# Skill: Bind a Book

## Purpose
Take a source text file and produce a print-ready A5 booklet PDF with:
- Serif font (RobotoSerif) at 11pt
- Book-standard margins (16mm inside / 11mm outside / 14mm top/bottom)
- ~1.3 line spacing
- Title page with book title, author, and decorative rule
- Optional gloss footnotes (superscript numbers with definitions at page bottom)
- Automatic page numbering

## Workflow

### Step 1: Greet and gather input
Welcome the user and ask:
1. **Source file** — "Which file should I bind into a booklet? (epub, pdf, txt, or md)"
   - Accept absolute paths or project-relative paths
   - Resolve relative paths against project root: `C:\PROJECTS\LESSON-PLAN-WRITER-3`
   - Validate the file exists; abort with error if not
   - Supported formats: `.epub`, `.pdf`, `.txt`, `.md`

2. **Book title** — "What's the book title?" (default: auto-detect from filename)

3. **Author name** — "Who's the author?" (default: none, skip author line)

4. **Gloss words** — "Any words to gloss as footnotes? Provide as `word=definition;word2=def2` or 'none'"
   - Example: `lone=to go or be alone;reckon=think or suppose`
   - Semicolons separate entries, commas are allowed inside definitions
   - Each word gets glossed only on its FIRST occurrence
   - The word `lone` has special handling to also match `loned`

5. **Output location** — "Where should the PDF go?" (default: `PDF/{input_subfolder}/`)
   - If the input is in `inputs/`, output goes to `PDF/{subfolder}/`

### Step 2: Run bookbinder.py
```powershell
python scripts/bookbinder.py "<input_path>" --title "<title>" --author "<author>" --gloss "<gloss_string>" --outdir "<output_dir>"
```

Omit `--gloss` if none. Omit `--author` if not provided.

### Step 3: Override any defaults (optional)
The user can request changes to:
- Font (default: RobotoSerif)
- Font size (default: 11pt)
- Margins (default: inside 16mm, outside 11mm, top 14mm, bottom 14mm)
- Line spacing (default: 0.3em leading)

For each override, re-run with the appropriate `--font`, `--font-size`, `--margin-*`, or `--leading` flags.

### Step 4: Report output
Inform the user where the PDF was saved and how to print:
```
Booklet created at: PDF/{subfolder}/{filename}_A5_booklet.pdf
Format: A5, {font} {size}pt, leading {leading}em

To print: Open PDF → Ctrl+P → Booklet mode → A4 paper
```

## File locations
- **Script:** `C:\PROJECTS\LESSON-PLAN-WRITER-3\scripts\bookbinder.py`
- **Font path:** `%APPDATA%\TinyTeX\texmf-dist\fonts\opentype\google\roboto\` (or `%LOCALAPPDATA%` for Local install)

## Edge cases
- **File not found**: "Error: input file not found at {path}"
- **Unsupported format**: "Error: unsupported format '.xyz'. Supported: .epub, .pdf, .txt, .md"
- **Missing ebooklib for EPUB**: Print install hint and abort
- **Missing pymupdf for PDF**: Print install hint and abort
- **Typst compile failure**: Print full stderr from the compiler
- **Gloss word not found in text**: No error — the word simply won't appear in the output

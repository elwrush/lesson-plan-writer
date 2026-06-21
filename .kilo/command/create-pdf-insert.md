# Command: Create PDF Insert

## Usage
`/create-pdf-insert <path/to/source.pdf> <pages>`

Automatically inserts selected PDF pages into a template with Mathayom header (ACT + Cambridge logos) on page 1. Subsequent pages are full-page, no header.

## Arguments
- `<path/to/source.pdf>` — Path relative to project root (e.g., `inputs/M2-5A BUSINESS/some.pdf`)
- `<pages>` — Page range, e.g. `2-6`, `3,5,7`, or `all` for all pages

## What it does
1. Loads the `insert-pdf-to-template` skill
2. Validates the source file exists
3. If pages is `all`: auto-detects page count via `fitz`
4. Derives output path automatically:
   - Source `inputs/M2-5A BUSINESS/X.pdf` → `PDF/M2-5A BUSINESS/X_with_header.pdf`
5. Writes and runs the insert script to `$TEMP\kilo\insert_pdf_to_template.py`
6. Reports the output path

## Template assets
- `templates/ACT.png` — left logo
- `templates/cambridge.png` — right logo
- Falls back to text-only header if logos missing

## Output
PDF saved to `PDF/{subfolder}/{stem}_with_header.pdf`

## Example
```
/create-pdf-insert inputs/M2-5A BUSINESS/B1-Reading Extract[43-49].pdf 2-6
/create-pdf-insert inputs/M2-5A BUSINESS/B1-Reading Extract[43-49].pdf all
```

# Command: Insert PDF to Template

## Usage
`/insert-pdf-to-template`

No arguments. Interactive flow.

## Workflow
1. Load skill `insert-pdf-to-template`
2. Agent asks: which PDF file and which pages to insert
3. If pages is "all": auto-detect page count via `python -c "import fitz; d=fitz.open(PATH); print(len(d)); d.close()"` before running the script
4. Agent runs the Python script to produce the output
5. Agent reports output path

**CRITICAL**: If the source PDF was just regenerated (e.g., by bookbinder.py), always re-derive the page count. Do not reuse a cached value.

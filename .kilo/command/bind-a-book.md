---
description: Converts epub/pdf/txt/md files into A5 booklet PDFs with serif typography, book margins, and optional gloss footnotes.
---

# Command: Bind a Book

## Usage
`/bind-a-book`

No arguments. Fully interactive flow.

## What it does
1. Loads the `bind-a-book` skill
2. Asks interactively: source file, title, author, gloss words, output location
3. Runs `scripts/bookbinder.py` to produce an A5 booklet PDF
4. Reports the output path and print instructions

## Workflow
1. `skill bind-a-book`
2. Follow the skill's interactive workflow (Step 1–4)
3. Report the output path

## Prerequisites
- `pip install ebooklib` (for EPUB input)
- `pip install pymupdf` (for PDF input)
- Typst CLI installed
- RobotoSerif OTF fonts in TinyTeX

---
name: bind-a-book
description: Converts text files (epub, pdf, txt, md) into A5 booklet PDFs with serif typography, book-standard margins, optional gloss footnotes, and a title page.
---

# Skill: Bind a Book

## Purpose
Take a source text file and produce a print-ready A5 booklet PDF with:
- Serif font (RobotoSerif) at 11pt
- Book-standard margins (16mm inside / 11mm outside / 14mm top/bottom)
- ~1.6 line spacing
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

2. **Chapter/page range** — "Which chapters or pages should I bind? (e.g., `1-5`, `3,4`, or `all`)"
   - For EPUB: maps to chapter HTML files in the manifest (e.g., `c03_r1.htm` = Chapter 3)
   - For PDF: maps to page ranges (requires pymupdf)
   - For TXT/MD: no range support (always `all`)
   - Default: `all` (bind the entire file)
   - When a range is specified, only extract content from those chapters/pages

3. **Book title** — "What's the book title?" (default: auto-detect from filename)

4. **Author name** — "Who's the author?" (default: none, skip author line)

5. **Gloss words** — "Any words to gloss as footnotes? Provide as `word=definition;word2=def2` or 'none'"
   - Example: `lone=to go or be alone;reckon=think or suppose`
   - Semicolons separate entries, commas are allowed inside definitions
   - Each word gets glossed only on its FIRST occurrence
   - The word `lone` has special handling to also match `loned`

6. **Output location** — "Where should the PDF go?" (default: `PDF/{input_subfolder}/`)
   - If the input is in `inputs/`, output goes to `PDF/{subfolder}/`

### Step 2: Handle chapter/page range (if specified)

**For EPUB source:**
1. List the EPUB's chapter files by examining `namelist()` for patterns like `*c03*.htm` (Chapter 3)
2. Map numeric chapter numbers to their internal filenames
3. Extract text only from the selected chapter files using `ebooklib` (filter by item index or filename pattern)
4. **Inject chapter headings and title block into body text as Typst markup** — since the bookbinder places body text raw into a Typst block, you can prepend markup directly:
   - Prepend a compact title block (title + author + horizontal rule) to the body text
   - Before each chapter's text, inject a centered chapter heading: `#align(center)[*CHAPTER N*]`
   - Between chapters, inject a decorative ornament divider: `#v(0.8em)\n#align(center)[— · — · — · — · —]\n#v(0.4em)`
   - See the "Chapter divider design" section below for exact patterns
5. Write the extracted text (with Typst markup) to a temporary `.txt` file in `%TEMP%\kilo\`
6. Use this `.txt` file as the input to bookbinder.py instead of the original EPUB

**For PDF source:**
- Use PyMuPDF to extract only the specified page range (e.g., `doc[2:5]` for pages 3-5)
- Write extracted text to a temporary `.txt` file

**For TXT/MD source:**
- Chapter ranges are not supported; warn the user and proceed with the full file.

### Step 3: Run bookbinder.py

**Important:** To ensure the first chapter starts on page 1 (no separate title page), pass spaces for title/author so the bookbinder's built-in title block is invisible:
```powershell
python scripts/bookbinder.py "<input_path>" --title " " --author " " --gloss "<gloss_string>" --outdir "<output_dir>"
```

Instead, inject the title, author, and chapter headings directly into the body text as Typst markup (see Step 2 for the pattern).

If the user does NOT plan to use `insert-pdf-to-template` and wants a standalone booklet with a proper title page, use the full title/author:
```powershell
python scripts/bookbinder.py "<input_path>" --title "<title>" --author "<author>" --gloss "<gloss_string>" --outdir "<output_dir>"
```

Omit `--gloss` if none. Omit `--author` if not provided.

**After compilation, rename the output file** from the temp-text derived name to a meaningful name like `{Title}_Ch{range}_A5_booklet.pdf`.

### Step 4: Override any defaults (optional)
The user can request changes to:
- Font (default: RobotoSerif)
- Font size (default: 11pt)
- Margins (default: inside 16mm, outside 11mm, top 14mm, bottom 14mm)
- Line spacing (default: 0.65em leading — Typst's built-in default)

For each override, re-run with the appropriate `--font`, `--font-size`, `--margin-*`, or `--leading` flags.

**CRITICAL — preserve all flags on regeneration**: When re-running bookbinder.py after a user override, carry forward ALL previously used flags (especially `--gloss`). Omitting `--gloss` on a rebuild will silently drop all gloss footnotes from the output. Always re-read the previous command's arguments before regenerating.

**Page count changes**: Adding glosses increases the page count (footnotes push content to new pages). When passing the output to `insert-pdf-to-template`, always re-derive the page count — do not reuse a previously cached count.

### Step 5: Report output
Inform the user where the PDF was saved and how to print:
```
Booklet created at: PDF/{subfolder}/{filename}_A5_booklet.pdf
Format: A5, {font} {size}pt, leading {leading}em

To print: Open PDF → Ctrl+P → Booklet mode → A4 paper
```

### Default workflow: insert-pdf-to-template

By default, the A5 booklet PDF is generated **without a separate title page** so the first chapter content starts on page 1. The title and author are set to spaces (`--title " " --author " "`) to suppress the bookbinder's built-in title block. Instead, the proper title, author, and chapter headings are injected directly into the body text as Typst markup. The booklet is then inserted into the school header template via the `insert-pdf-to-template` skill.

To run this step:
1. Load the `insert-pdf-to-template` skill
2. Follow its interactive workflow
3. The template adds a narrow school header band (logos + horizontal rule) on page 1 only

**Page count**: The source PDF page count (excluding the template's own first page) is `{page_count}`. After insertion into the template, the final PDF has `{page_count + 1}` pages (template = 1 + booklet = N). Always re-derive page counts — do not reuse cached counts from previous runs.

## File locations
- **Script:** `C:\PROJECTS\LESSON-PLAN-WRITER-3\scripts\bookbinder.py`
- **Font path:** `%APPDATA%\TinyTeX\texmf-dist\fonts\opentype\google\roboto\` (or `%LOCALAPPDATA%` for Local install)

## Text extraction rules (critical)

The bookbinder places extracted text directly into a Typst code block. The text file must be clean and correctly formatted **before** running the bookbinder. Follow these rules:

### 1. Paragraph breaks
Convert `</p>`, `</h1>`–`</h6>`, and `</div>` to `\n\n` **BEFORE** stripping HTML tags.
```python
# CORRECT: closing tags → newlines, then strip remaining tags
html = html.replace('</p>', '\n\n')
html = html.replace('</h1>', '\n\n')
html = html.replace('</h2>', '\n\n')
# ... after all replacements:
html = re.sub(r'<[^>]+>', '', html)
```
**Wrong**: stripping tags first destroys `</p>` so subsequent `.replace('</p>', '\n\n')` does nothing, producing a single wall of text.

### 2. Strip `<title>` content
The HTML `<title>...</title>` tag leaks into body text. Remove it explicitly:
```python
html = re.sub(r'<title[^>]*>.*?</title>', '', html, flags=re.IGNORECASE | re.DOTALL)
```

### 3. Strip redundant chapter headings
The title page already communicates the book title. Strip the first line if it matches the chapter heading:
```python
while lines and lines[0].strip() in ('A MONSTER CALLS', 'BREAKFAST', ''):
    lines.pop(0)
```
The bookbinder's `strip_leading_heading()` only handles patterns like `"Chapter 1"`, `"CHAPTER 2"` — it does NOT strip custom headings like `"A MONSTER CALLS"` or `"BREAKFAST"`. You must strip these manually.

### 4. Verify the text file before running bookbinder
Always read the `.txt` output file **first** and check:
- No title duplication at the start
- Paragraph breaks look correct (blank lines between paragraphs, not one continuous line)
- Chapter transitions have visible markers
- Reflection questions (if any) are present

## Injecting Typst markup into body text

Since the bookbinder places body text raw into a `{body_text}` Typst block, you can inject Typst commands directly into the text file. The gloss injector passes them through untouched as long as they don't match any gloss word regex.

### Available Typst commands for bookbinder text

| Purpose | Typst code | Notes |
|---------|-----------|-------|
| Page break | `#pagebreak()` | Use before reflection questions to put them on a separate page |
| Vertical space | `#v(1em)` | Adds space. Multiple consecutive uses work. |
| Centered align | `#align(center)[text]` | Wraps content in a centered block |
| Bold | `[*text*]` | Inside align or standalone |
| Italic | `*text*` | Works in markup context |
| Horizontal rule | `#line(length: 30%, stroke: 0.4pt)` | **Avoid for chapter dividers** — stubby line looks unprofessional |

### Chapter divider design

**Do NOT use `#line()` for chapter breaks.** A short horizontal rule looks amateurish. Instead use a centered typographic ornament spanning the full visual width:

```
#v(0.8em)
#align(center)[— · — · — · — · —]
#v(0.4em)

#align(center)[*CHAPTER 2*]
```

This pattern (em-dashes alternating with mid-dots) is a classic fleuron-style divider used in book typography since the Renaissance. It works for both:
- **Chapter breaks** (between chapters in the text)
- **Section headings** (e.g., `Reflection Questions` on a new page)

For reflection questions, combine with `#pagebreak()`:
```
#pagebreak()

#v(1.2em)
#align(center)[— · — · — · — · —]
#v(0.6em)

#align(center)[*Reflection Questions*]
```

### Gloss words vs pre-taught vocabulary

When the booklet accompanies a lesson plan, ensure gloss words do **not** overlap with vocabulary already pre-taught in the lesson slides. Example:
- **Pre-taught slide vocab**: `yew, nightmare, ancient, untamed, compost`
- **Booklet gloss words**: `groggily, billowing, fortnightly, teetering, gaping`

Learners should encounter each word once — either in the lesson or in the booklet, not both.

### Reflection questions

Follow the pattern: **specific text quote/reference + analytical question + personal response**. This matches the established style in the Every Day booklet.

```
1. Conor tells the monster, "I've seen worse," and later says he is afraid "Not of you, anyway."
   What do you think the real source of fear in Conor's life is? What clues has the story given us so far?

2. Conor's mother says, "I wish you didn't have to be quite so good."
   Does keeping secrets from his mother protect Conor, or does it make his life harder?
   What would you do if you were in his situation?
```

Format: italicized (`*text*` in Typst), with `#v(0.4em)` spacing between questions.

## Source EPUB hygiene

**Check for Chinese ad/spam pages** before extracting. Some Chinese ebook sites insert `ad_chapter*.xhtml` files between chapters with promotional content (e.g., "公众号：古德猫宁李", "沉金书屋 https://www.chenjin5.com"). These appear in the EPUB manifest as separate items.

Mitigation:
1. List EPUB contents with `zipfile.ZipFile.namelist()` and inspect for `ad_chapter*.xhtml` or `ad_*.xhtml`
2. If present, **replace the EPUB with a clean edition** — do not attempt to filter them out (the manifest structure may still reference them)
3. Verify the publisher: legitimate editions show the actual publisher (e.g., "Walker Books") in the OPF metadata

## Common pitfalls

| Symptom | Cause | Fix |
|---------|-------|-----|
| Entire text is one continuous paragraph | Tags stripped before `</p>` → `\n\n` conversion | Reorder: replace `</p>` first, then strip tags |
| Title appears twice ("A Monster Calls A MONSTER CALLS") | `<title>` tag content not stripped | Add `re.sub(r'<title>.*?</title>', ...)` to extraction |
| Chapter heading missing between sections | Heading stripped by `strip_leading_heading()` or manually | Insert a `CHAPTER N` heading with ornament divider in the combined text |
| First chapter heading missing when using range | Only chapters after the first get ornament dividers; first chapter has no label | Always inject `#align(center)[*CHAPTER N*]` before the first chapter's text, not just between chapters |
| Reflection questions run directly into story text | No page break or separator | Add `#pagebreak()` + ornament divider before questions |
| Gloss words also taught in lesson slides | Overlap between pre-taught vocab and gloss list | Audit both lists before running bookbinder |
| Line is a short stub, not decorative | Using `#line(length: 30%)` | Replace with centered `#align(center)[— · — · — · — · —]` |
| EPUB has Chinese ads between chapters | Source is from chenjin5.com or similar | Replace with clean publisher edition |

## Edge cases
- **File not found**: "Error: input file not found at {path}"
- **Unsupported format**: "Error: unsupported format '.xyz'. Supported: .epub, .pdf, .txt, .md"
- **Missing ebooklib for EPUB**: Print install hint and abort
- **Missing pymupdf for PDF**: Print install hint and abort
- **Typst compile failure**: Print full stderr from the compiler
- **Gloss word not found in text**: No error — the word simply won't appear in the output
- **Chapter heading in source text**: The script automatically strips the first line of body text if it matches a chapter heading pattern (e.g., "Chapter 1", "CHAPTER 2", "Ch. 3") since the title page already communicates the chapter. No manual action needed.
- **Gloss words on regeneration**: Always re-supply `--gloss` on regeneration. The script does not cache previous gloss entries — omitting `--gloss` produces an unglossed booklet.

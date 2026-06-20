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

## When to Use

Use this skill when:
- The user provides or requests conversion of an EPUB, PDF, TXT, or MD file into a print-ready booklet
- A5 format with book-standard margins is needed
- Optional gloss footnotes are needed (non-gloss footnotes are discarded)
- The output is intended for printing and binding

Do NOT use this skill when:
- The output needs to remain editable (use Pandoc to PDF instead)
- Standard binding is not needed (A4 single-page output is preferred)

**Trigger:** `/bind-a-book` command or when the user asks to convert a file into a booklet PDF.

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
## Examples

### Example 1: Convert EPUB to booklet

**Request:** "Bind moby-dick.epub into a booklet"

**Action taken:** Extract text via `ebooklib`, parse chapters, pipe through Pandoc + Typst, compile to A5 PDF with gloss footnotes.

**Output:** `PDF/BOOKLETS/moby-dick-booklet.pdf`

### Example 2: Convert text with gloss words

**Request:** "Bind story.txt with gloss for: sailor, whale"

**Action taken:** Read text, insert gloss footnote markers, compile to A5 PDF.

**Output:** `PDF/BOOKLETS/story-booklet.pdf`

### Example 3: PDF chapter range

**Request:** "Bind chapters 3-5 from this PDF"

**Action taken:** Extract pages via pymupdf, compile to A5 booklet.

**Output:** `PDF/BOOKLETS/excerpt-booklet.pdf`



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

## Preferred source: Standard Ebooks

For public-domain short stories and novels, **Standard Ebooks** (standardebooks.org) is strongly preferred over PDF extraction. Their XHTML is cleanly structured with proper `<p>` tags, no inline ads, no page-break artifacts, and no website navigation garbage.

**Workflow:**
1. Fetch the XHTML page via `requests` or `webfetch`
2. Parse with BeautifulSoup
3. Find the `<article>` or `<section>` containing the story
4. Extract text from each `<p>` tag: `[p.get_text(strip=True) for p in article.find_all("p")]`
5. Join with `\n\n` to preserve paragraph breaks
6. Use this as the body text instead of PDF-extracted text

**Why not American Literature (americanliterature.com):** Mediavine inline ads create artificial paragraph breaks. The site also requires Cloudflare-bypassing tools.

**Why not plain PDF extraction:** PDF page boundaries create artificial paragraph breaks at sentence mid-points (e.g., "shoot off afresh\n\nunder" instead of "shoot off afresh under"). Character encoding (mojibake) is also a recurring issue.

## PDF extraction (when web source unavailable)

### Author/intro image extraction
When the first page of a PDF contains a photo (e.g., author portrait), it can be extracted with PyMuPDF:
```python
page = doc[0]
images = page.get_images()
xref = images[0][0]
base_image = doc.extract_image(xref)
# save base_image["image"] to file
```

If the extracted image is low quality or unavailable, search Wikimedia Commons for a public-domain alternative (e.g., author portrait from Nadar).

### Intelligent page joining (critical)
When joining extracted PDF pages, **detect mid-sentence page breaks** to avoid artificial paragraph breaks:
```python
sentence_endings = {".", "!", "?", "\"", "'", "\u201d", "\u2019", "\u00bb", "\u2014"}
prev_last = last_non_empty_line_of(prev_page)
last_char = prev_last[-1] if prev_last else ""
if last_char in sentence_endings:
    join_with = "\n\n"  # natural paragraph break
else:
    join_with = "\n"    # sentence continues across page
```

### Website garbage stripping
When extracting from web-sourced PDFs (americanliterature.com etc.), strip these patterns:
- `"Copy Link"`, `"Rate:"`, `"Save to Library"`, `"FEATURED"`, `"COLLECTIONS"`, `"Share"`
- `"Short Story of the Day"`, `"100 Great"`, `"Halloween"`, `"Christmas"`
- `"SUBSCRIBE"`, `"Privacy Policy"`, `"YouTube"`, `"Pierrot"`
- Date/time stamps matching `\d+/\d+/\d+,\s+\d+:\d+\s+(AM|PM)`
- URL lines containing `americanliterature.com`
- Page numbers matching `N/22` pattern
- `"Paul's Mistress by Guy de Maupassant | Full Text"` (or any `" | Full Text"` variant)

**Robust ending detection:** Find the story's last sentence and trim everything after it:
```python
story_end = "and she went off slowly"
if story_end in body:
    idx = body.rfind(story_end) + len(story_end)
    eol = body.find("\n", idx)
    body = body[:eol] if eol >= 0 else body[:idx]
```

## Adding a critical thinking question page (PyMuPDF)

A question page can be appended to the final PDF using PyMuPDF. The page uses the same font as the booklet body (RobotoSerif 11pt).

### Font registration and measurement
**CRITICAL — do NOT guess font widths.** Use `fitz.Font.text_length()` for exact measurement:
```python
import fitz
font_reg = fitz.Font(fontfile="path/to/RobotoSerif-Regular.otf")

# Word-wrap using actual font metrics
MAX_W = available_width - 5  # small buffer
words = text.split()
line = ""
for word in words:
    test = (line + " " + word).strip()
    if font_reg.text_length(test, fontsize=11) > MAX_W and line:
        page.insert_text(point, line, fontname="RoboReg", fontsize=11, ...)
        y += line_height
        line = word
    else:
        line = test
```
- `fitz.get_text_length()` does NOT support custom fonts (base 14 only). Use `Font.text_length()` instead.
- `page.insert_textbox()` with custom fonts may return incorrect position values. Manual word-wrap with `Font.text_length()` is more reliable.
- Always register the font with `page.insert_font(fontname="RoboReg", fontfile=path)` before `insert_text`.

### A4 page layout for question page
- A4 dimensions: 595 x 842 pt
- Standard margins: 72pt (1 inch) all sides
- Usable width: 595 - 144 = 451pt
- RobotoSerif 11pt average char width: ~5.7pt → ~79 chars per line at max
- Line height: 17pt (11pt × ~1.5 leading)
- Ruled line spacing: 30pt for handwriting

### Ruled lines
Draw full-width horizontal lines at 30pt intervals:
```python
for i in range(15):
    ly = y_start + i * 30
    page.draw_line(fitz.Point(ML, ly), fitz.Point(PW - MR, ly), color=(0, 0, 0), width=0.5)
```
- 15 lines require ~450pt vertical space
- Starting at Y≈160 gives a well-centered layout on A4

### Inference question design
B2-level critical thinking questions should test **inference** (reading between the lines), not literal recall. Pattern:
- Reference two connected scenes/events in the story
- Ask why the author placed them together
- Ask what a metaphor/object reveals about a character's self-perception

## Common pitfalls

| Symptom | Cause | Fix |
|---------|-------|-----|
| Entire text is one continuous paragraph | Tags stripped before `</p>` → `\n\n` conversion | Reorder: replace `</p>` first, then strip tags |
| Title appears twice ("A Monster Calls A MONSTER CALLS") | `<title>` tag content not stripped | Add `re.sub(r'<title>.*?</title>', ...)` to extraction |
| Chapter heading missing between sections | Heading stripped by `strip_leading_heading()` or manually | Insert `CHAPTER N` heading with ornament divider |
| Sentences split across pages ("afresh / under") | PDF pages joined with `\n\n` | Use intelligent page joining — detect mid-sentence breaks |
| Text overflows A4 question page margins | Char-count-based wrap with wrong font metrics | Use `fitz.Font.text_length()` with actual font file |
| Custom font text width wrong in PyMuPDF | Using `fitz.get_text_length()` (built-in fonts only) | Use `fitz.Font(fontfile=...).text_length(text, fontsize=N)` |
| Website footer garbage in extracted text | Stripping only exact line matches | Add pattern-based detection: date regex, URL patterns, "Full Text", "Pierrot" |
| Ruled lines off bottom of A4 page | `insert_textbox()` return value wrong for custom fonts | Manual word-wrap with `Font.text_length()` instead |
| Intro paragraph has footnote markers | Gloss injector footnotes first occurrence | Italicise intro with `_..._` to visually separate, or accept as intentional |
| Inline ads break paragraph flow in American Literature | Mediavine ads injected as `<div>` elements | Extract via `<p>` tags only, or switch to Standard Ebooks |

## Edge cases
- **File not found**: "Error: input file not found at {path}"
- **Unsupported format**: "Error: unsupported format '.xyz'. Supported: .epub, .pdf, .txt, .md"
- **Missing ebooklib for EPUB**: Print install hint and abort
- **Missing pymupdf for PDF**: Print install hint and abort
- **Typst compile failure**: Print full stderr from the compiler
- **Gloss word not found in text**: No error — the word simply won't appear in the output
- **Chapter heading in source text**: The script automatically strips the first line of body text if it matches a chapter heading pattern (e.g., "Chapter 1", "CHAPTER 2", "Ch. 3") since the title page already communicates the chapter. No manual action needed.
- **Gloss words on regeneration**: Always re-supply `--gloss` on regeneration. The script does not cache previous gloss entries — omitting `--gloss` produces an unglossed booklet.
- **Cloudflare-blocked source**: americanliterature.com blocks direct requests. Use `webfetch` tool or switch to Standard Ebooks.
- **Custom font text measurement**: `fitz.get_text_length()` does NOT work with custom fonts. Always use `fitz.Font(fontfile=...).text_length()`.
- **Mid-sentence page break**: Detect via last non-whitespace character of the page; if not sentence-ending punctuation (.!?"'»—), join with `\n` instead of `\n\n`.
- **Question page Y alignment**: With 15 ruled lines at 30pt spacing, start ruled lines at Y≈160 for centered layout on A4 (842pt page).
- **Gloss semicolon trap**: Do NOT use semicolons inside gloss definitions — they are entry separators. Use commas instead.
- **Typst emphasis vs story underscores**: Story text containing `_` (e.g. song lyrics) conflicts with Typst's `_..._` emphasis syntax. Use `#emph[...]` for preface italicisation instead of `_..._`, or escape underscores with `\_` in the body text.
- **`typst compile` cp1252 crash on Windows**: `subprocess.run(text=True)` on stderr crashes on non-cp1252 output. Use `encoding="utf-8", errors="replace"` instead.
- **EPUB extraction**: Use `ebooklib` to open `.epub` files, iterate items, find the target XHTML file by pattern (e.g. `06.xhtml`), parse with BeautifulSoup, extract `<p>` tag text. Skip heading-only paragraphs (`<h1>`, chapter titles) by filtering them out.
- **Cover image**: Extracted images should be resized to max 1920px wide, saved as JPEG quality 85. Place in the body text as `#image("filename.jpg", height: 5.5cm)` centred. 1280×720 images work well at this height.
- **EPUB paragraph extraction**: Use `p.get_text(separator=" ", strip=False).strip()` NOT `p.get_text(strip=True)`. The `strip=True` argument strips ALL internal whitespace, merging words across inline tags (e.g. `the <em>third</em> voyage` becomes `thethirdvoyage`). Always pass `separator=" "` to ensure spaces between inline elements, then call `.strip()` externally.
- **Plain-text italics markers in EPUBs**: Some EPUBs use `_text_` as a plain-text convention for italics (not `<em>` tags), especially in song lyrics. After text extraction, do a targeted string replacement to convert these to Typst `#emph[...]`:
  ```python
  story_text = story_text.replace(
      "\u201c_Oh, give me a June night\n\nThe moonlight and you_ ... \u201d",
      "#emph[Oh, give me a June night\n\nThe moonlight and you]"
  )
  ```
  Strip the `_` markers and wrapping curly quotes, keep the rest intact.
- **Typst emphasis vs literal underscores**: If story text contains literal `_` characters (song lyrics, old-style italics markers), they conflict with Typst's `_..._` emphasis syntax. Two strategies:
  - For intentional italics: use `#emph[...]` instead of `_..._` markers
  - For literal underscores: escape as `\_` with `body.replace("_", "\\_")`
  - Apply the underscore escape AFTER `#emph[...]` conversion so emphasized text renders correctly
- **Header text variation**: Different detention groups use different labels (M2, M3, etc.). Set `HEADER_TEXT` dynamically per assignment. Don't hardcode in skill scripts.
- **Page count in print statements**: Never hardcode page counts. Use `fitz.open()` to re-read the final PDF and get the actual page count.

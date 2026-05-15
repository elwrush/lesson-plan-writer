# Skill: Insert PDF to Template

## Purpose
Insert selected pages from a source PDF into a template PDF with a narrow school header appearing only on page 1. Remaining inserted pages fill the entire page.

## Workflow

### Step 1: Gather Input
Ask the user **three things** interactively, one per turn:

1. **Source PDF path** — "Where is the original PDF file? Provide the full path."
   - Accept absolute paths like `C:\path\to\file.pdf` or project-relative like `inputs\REX-LESSON-01\Question+Reading.pdf`
   - Resolve relative paths against the project root: `C:\PROJECTS\LESSON-PLAN-WRITER-3`
   - Validate the file exists. If not found under the relative path, try the absolute path as given.

2. **Pages to insert** — "Which pages do you want to insert? (e.g., 2-4, or 3,5,7)"
   - Accept hyphenated ranges and comma-separated lists
   - Validate each page number is within the source PDF's page count

3. **Output path** — Always save to `PDF/{input-folder-name}/{meaningful-name}.pdf`
   - Derive automatically from the source PDF path:
     - Source: `inputs/REX-LESSON-01/Question+Reading.pdf`
     - Subfolder name = last directory in the source path (e.g., `REX-LESSON-01`)
     - Stem = source filename minus extension (e.g., `Question+Reading`)
     - Output: `PDF/REX-LESSON-01/Question+Reading_with_header.pdf`
   - Create the output directory if it doesn't exist
   - Ask the user to confirm or suggest a different stem name if desired

### Step 2: Parse pages and validate input
- Check the PDF file exists
- Parse the page range string (e.g., "2-4", "3,5,7")
- Validate each page number is within the source PDF's page count
- If logo file is missing, fall back to text-only header

### Step 3: Write and run the script

Write the Python script to `C:\Users\elwru\AppData\Local\Temp\kilo\insert_pdf_to_template.py` and run it.

### Step 4: Report
Inform user of the output PDF path.

## Python Script

Uses `fitz.paper_rect("a4")` for precise A4 dimensions (595.276 x 841.890 pt). The `show_pdf_page` call renders source content as vector, preserving full resolution — print output will use the device's native DPI. No pixel-based resampling occurs.

**Layout**: The first inserted source page is placed on page 1 below the header band. Remaining inserted pages fill full pages (no header).

Write the script at `C:\Users\elwru\AppData\Local\Temp\kilo\insert_pdf_to_template.py` with this content:

```python
import fitz
import sys, os

LOGO_LEFT = r"C:\PROJECTS\LESSON-PLAN-WRITER-3\templates\ACT.png"
LOGO_RIGHT = r"C:\PROJECTS\LESSON-PLAN-WRITER-3\templates\1135082720.png"
HEADER_TEXT = "Mathayom Program"

A4 = fitz.paper_rect("a4")
PW, PH = A4.width, A4.height

LOGO_W = 60

# Right ear needs a wider rect because its image is landscape
# For Cambridge (800x371) to match ACT (1396x1732) visible height at 44pt:
#   right_w = 44 * (800/371) = 95pt
RIGHT_W = 95

def create_header_page(doc, first_src_page=None):
    page = doc.new_page(width=PW, height=PH)
    page.draw_rect(fitz.Rect(0, 0, PW, PH), color=None, fill=(1, 1, 1))
    page.draw_rect(fitz.Rect(0, 0, PW, HEADER_HEIGHT), color=None, fill=(1, 1, 1))

    # Left ear (ACT logo) — portrait, fills 44pt height naturally
    if os.path.exists(LOGO_LEFT):
        try:
            logo_l = fitz.Rect(15, 8, 15 + LOGO_W, 8 + 44)
            page.insert_image(logo_l, filename=LOGO_LEFT, keep_proportion=True)
        except Exception:
            pass

    # Right ear (Cambridge logo) — landscape, needs wider rect for same visible size
    if os.path.exists(LOGO_RIGHT):
        try:
            logo_r = fitz.Rect(PW - 15 - RIGHT_W, 8, PW - 15, 8 + 44)
            page.insert_image(logo_r, filename=LOGO_RIGHT, keep_proportion=True)
        except Exception:
            pass

    if os.path.exists(LOGO_RIGHT):
        try:
            logo_r = fitz.Rect(PW - 90, 8, PW - 15, HEADER_HEIGHT - 8)
            page.insert_image(logo_r, filename=LOGO_RIGHT, keep_proportion=True)
        except Exception:
            pass

    tw = fitz.get_text_length(HEADER_TEXT, fontname="helv", fontsize=13)
    x_center = (PW - tw) / 2
    page.insert_text(
        fitz.Point(x_center, HEADER_HEIGHT / 2 + 5),
        HEADER_TEXT,
        fontname="helv",
        fontsize=13,
        color=(0, 0, 0),
    )

    # Full-width horizontal line under the header
    page.draw_line(fitz.Point(0, HEADER_HEIGHT), fitz.Point(PW, HEADER_HEIGHT),
                   color=(0, 0, 0), width=0.5)

    if first_src_page is not None:
        doc_src, src_idx = first_src_page
        body_rect = fitz.Rect(0, HEADER_HEIGHT, PW, PH)
        page.show_pdf_page(body_rect, doc_src, src_idx)
    return page

def parse_pages(pages_str, max_page):
    parts = [p.strip() for p in pages_str.split(",")]
    pages = []
    for p in parts:
        if "-" in p:
            s, e = p.split("-")
            pages.extend(range(int(s), int(e) + 1))
        else:
            pages.append(int(p))
    for p in pages:
        if p < 1 or p > max_page:
            raise ValueError(f"Page {p} not in range [1, {max_page}]")
    return pages

def main():
    source_pdf = sys.argv[1]
    pages_str = sys.argv[2]
    output_pdf = sys.argv[3]

    if not os.path.exists(source_pdf):
        print(f"Error: source PDF not found at {source_pdf}")
        sys.exit(1)

    doc_src = fitz.open(source_pdf)
    pages = parse_pages(pages_str, len(doc_src))

    doc_out = fitz.open()
    first = pages[0]
    create_header_page(doc_out, first_src_page=(doc_src, first - 1))
    for p in pages[1:]:
        page_out = doc_out.new_page(width=PW, height=PH)
        page_out.show_pdf_page(page_out.rect, doc_src, p - 1)

    doc_out.save(output_pdf)
    doc_out.close()
    doc_src.close()
    print(f"Created {output_pdf} ({len(pages)} pages inserted)")

if __name__ == "__main__":
    main()
```

### Running the script

Derive the output path from the source PDF location before running:

```
Source:  inputs/REX-LESSON-01/Question+Reading.pdf
Subfolder: REX-LESSON-01
Stem:     Question+Reading
Output:   PDF/REX-LESSON-01/Question+Reading_with_header.pdf
```

```powershell
python C:\Users\elwru\AppData\Local\Temp\kilo\insert_pdf_to_template.py "inputs/REX-LESSON-01/Question+Reading.pdf" "2-4" "PDF/REX-LESSON-01/Question+Reading_with_header.pdf"
```

## Dependencies
- `pymupdf` (imported as `fitz`)
- `templates/ACT.png` — school logo for page 1 header

## Edge Cases
- **Invalid page numbers**: Report error "Page X not in range [1, N]"
- **PDF not found**: Check file exists, abort with descriptive error
- **Logo missing**: Fall back to text-only header (no crash)
- **Output path**: Default to `output/inserted_{source_stem}.pdf` if not specified

Base directory for this skill: file:///C:/PROJECTS/LESSON-PLAN-WRITER-3/.kilo/skills/insert-pdf-to-template

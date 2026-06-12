---
name: create-bespoke-materials
description: Creates bespoke teaching materials with headed ruled-paper formatting — Mathayom header on page 1, centered student demographics (from Supabase), ruled writing lines at 24pt spacing, and booklet mode (4-page signatures on A4).
---

# Skill: Create Bespoke Materials

## Hard-Won Lessons (from 2026-06-11)

Do NOT bypass these rules. Each cost hours of debugging.

### Page format
- **PDF pages are A4** (not A5). The printer's booklet function handles 2-up scaling to A5.
- **Do NOT use `set page(header: ...)`** — header (logos + Mathayom Program) is regular content on page 1 only.
- Pages after page 1: **no header**, just the 1.5cm top margin as padding.
- **No explicit `#pagebreak()` between Parts 1-3** — let them flow continuously. Only pagebreak before Discussion (Part 4) and before Transcript.

### Font sizes (14pt body for booklet)
| Element | Size | Rationale |
|---------|------|-----------|
| Body text | 14pt | 70.7% scale → ~9.9pt readable at A5 |
| Title | 18pt | Bold, centered |
| Subtitle | 15pt | |
| Instructions | 13pt | |
| Labels / metadata | 12pt | **Absolute minimum for ANY text** |
| Transcript | 12pt | Reference material |
| Structure hint | 12pt | Think-Pair-Share scaffolding |

### Fill-in blanks — NEVER use `#underline(h(...))`
`#underline(h(3cm))` produces NO visible line. Two correct approaches:
1. **`#box(stroke: bottom)`** for inline blanks:
```typst
#let fl = box(width: 3cm, stroke: (bottom: 0.5pt + black))
#h(3em) 1\. Women shown as the #fl \\
```
2. **`#ul(N)` helper (underscores)** — simpler, text-level, never breaks indentation:
```typst
#let ul(n) = str("_") * n
#h(3em) 1\. Women shown as the #ul(15) \\
```

### Pre-Output Typst Validation (MANDATORY)

Before writing any `.typ` file, validate it through `scripts/typst_check.py`:

```powershell
python scripts/typst_check.py path/to/file.typ
# or for inline content:
echo "$typstContent" | python scripts/typst_check.py -
```

Do NOT write the file until validation passes (exit code 0). The tool catches: mid-word bold, hash-in-content, hash-in-code-mode, unclosed blocks, and all other compile errors catalogued in the Typst Pitfalls section above.

### Ruled lines — the only correct pattern
```typst
#let ls = 24pt
#let ruled-lines(n) = {
  for i in range(n) {
    if i == 0 { v(1.2em) } else { v(ls / 2) }
    line(length: 100%, stroke: 0.4pt + black)
    v(ls / 2)
  }
}
```
- DO NOT use `tiling()`, `table()`, `table.hlines()`, `grid()`, `block(stroke: bottom)` (empty blocks don't render), or `rect()`.
- First line gets `v(1.2em)` clearance (not `v(ls/2)` = 12pt which is too close to text).

### Academic outline format — use manual `#h()` + `\\`
Do NOT use `+` list syntax:
- `+` adds excessive block spacing that can't be fully eliminated
- `set enum(spacing: 0em)` DESTROYS line breaks (collapses items into same paragraph)
- `start:` parameter conflicts with nested list numbering
- Manual `\\` with `#h()` indentation is **predictable, compact, and always works**

```typst
I. Section Title \\
  #h(1.5em) A. Sub-section \\
    #h(3em) 1\. Fill-in #ul(15) \\
    #h(3em) 2\. Another fill-in #ul(15) \\
  #h(1.5em) B. Next sub-section \\
    #h(3em) 1\. #ul(6) of people believe...
```

### Line breaks in Typst markup
- Consecutive lines (no blank line) = same paragraph (joined by spaces)
- `\\ ` at end of line = explicit line break within same paragraph
- Blank line = paragraph break

### Escaping list markers
`1.` at line start triggers Typst list detection. Use `1\.` to render as plain text. This applies to `#h()` indented items as well — `#h(3em) 1\. text` renders correctly.

### Color for grayscale printing
Use `black` for all lines and strokes. Do NOT use `luma()` — luma values wash out. For subtle text (metadata), `luma(20)` is the maximum acceptable.

### Demographics — centered with gaps
Use `#align(center)` with `#h(2em)` gaps between fields:
```typst
#align(center, text(size: 14pt)[
  *CLASS:* CLASS_PLACEHOLDER #h(2em)
  *ID:* ID_PLACEHOLDER #h(2em)
  *NAME:* NAME_PLACEHOLDER
])
```
Do NOT use `#grid()` with `1fr` columns for demographics — `1fr` makes the grid full-width, defeating centering. Do NOT use `#` prefix before placeholders (e.g. `#CLASS_PLACEHOLDER` becomes `#M3-5A` which Typst interprets as a variable name).

### 4-page signatures
Each student's booklet MUST be padded to the next multiple of 4 pages. Use PyMuPDF after compilation:
```python
blank = fitz.open()
blank.new_page(width=595, height=842)  # A4 in points
for _ in range(4 - (n % 4)):
    doc.insert_pdf(blank)
```

### Supabase integration
```powershell
supabase login --token $env:SUPABASE_ACCESS_TOKEN
supabase link --project-ref hdpwaqprrgnndkgzmnan --password "Per3843235!"
supabase db query --linked "SELECT student_id, name, class FROM classlists WHERE class LIKE 'M2-%' ORDER BY class, name;"
```
Project ref: `hdpwaqprrgnndkgzmnan`

### `.typ` files must be inside project root
With `--root "."`, Typst requires source files within `C:\PROJECTS\LESSON-PLAN-WRITER-3\`. Write temp files to `tmp/` subdirectory.

### Comprehension questions — inferential, not recall
Do NOT write questions that simply repeat the outline gaps. Questions should require synthesis, analysis, or evaluation. For example:
- ❌ "What did the Kings College study find?" (recall from outline)
- ✅ "Why might Gen Z hold stronger traditional beliefs despite living in a more progressive era?" (inference)

### Transcript — include at 12pt minimum
Transcript goes on the final page after `#pagebreak()`. Set `12pt` minimum font with `leading: 0.4em` and `spacing: 0.8em` for double line breaks between paragraphs.

### Linting (mandatory post-generation)
```bash
python scripts/validate_booklet.py --dir "PDF/{topic}-BOOKLETS" --strict
```

## References
- **`scripts/gen_gender_booklets.py`** — M3 gender roles: full working example (58 students)
- **`scripts/gen_m2_booklets.py`** — M2 diphtheria: second working example (39 students)
- **`scripts/linter_bespoke.py`** — font sizes, page counts, text fill, outline breaks
- **`scripts/validate_booklet.py`** — page-count validator (multiples of 4)
- **`templates/mathayom-header.typ`** — reusable Typst header component
- **`C:\Users\elwru\.kilo\skills\insert-pdf-to-template\SKILL.md`** — for injecting existing PDF/JPEG pages

## Interactive Questions (agent asks in order)

### Q1: Input type
"What are you working with?"
- `Supabase classlist` — generate from student data (e.g. M2-4A, M3-5A)
- `Typst content` — create from existing `.typ` source
- `PDF` — inject existing PDF pages into template
- `Image` — inject JPEG/PNG

### Q2: Description
"What is being produced? (e.g., 'M2 Listening — Diphtheria Worksheet')"

### Q3: Level / class
"Which level or class? (e.g., M2, M3, M3-5A)"
If Supabase: query the classlist table with the appropriate filter.

### Q4: Demographics
"Should each document include student demographic data?"
- `Yes, from Supabase` — query classlist, generate one PDF per student (ask for class filter)
- `Yes, blank fields` — show blank CLASS, ID, NAME on each page
- `No` — skip demographics

### Q5: Transcript
"Should the transcript be included?"
- `No` (default) — saves ~2 pages per student
- `Yes` — included on final page after pagebreak

### Q6: Format
"Booklet or standard A4?"
- `Booklet` — A4 pages, 14pt, pad each student to 4-page multiple, combine by class

## Output directory structure
```
PDF/{topic}-BOOKLETS/
├── {CLASS1}-{topic}-booklet.pdf    # Combined by class
├── {CLASS2}-{topic}-booklet.pdf
└── ALL-{topic}-booklet.pdf         # Mega combined
```

---
name: typst-document-creator
description: Creates new Typst documents from scratch or transforms existing lesson materials. Manages full pipeline — user consultation, code generation, PDF compilation, and integrity verification.
---

# Skill: Typst Document Creator

## Purpose
Create Typst documents from scratch or by transforming existing lesson materials (JSON, markdown, text). Uses the official Mathayom Program header, handles print format consultation, compiles to PDF, and runs a deterministic integrity check to ensure no text was truncated or altered.

## Output directories
- Source `.typ` files: `typst/code/{date-prefix}-{topic}/`
- Compiled PDFs: `typst/PDF/{date-prefix}-{topic}/`

## Dependencies
- Loads `typst-author` skill for Typst syntax reference
- `typst compile` for PDF generation
- `typstyle` (optional) for formatting
- `python` with `difflib` for integrity checks
- Remote Typst source code on GitHub (via `gh search code` / `gh api`) — **primary syntax authority.** Every function call, argument, set rule, and show rule must be confirmed against this before writing. The packed repo at `knowledge-base/typst-packed.json` is a stale fallback snapshot. **Never guess or rely on training data — Typst evolves fast.**

## Workflow

### STRICT RULE: NO HALLUCINATED SYNTAX
**Training data is forbidden as a Typst syntax reference — it is always stale and inaccurate.** For every function call, parameter name, set rule, and show rule, consult sources in this priority:

1. **Remote Typst source code on GitHub** (`github.com/typst/typst`) via `gh search code` or `gh api` — the only authoritative, up-to-date source.
2. **Local `typst-author` skill bundled docs** (`.kilo/skills/typst-author/docs/`) — a snapshot that may be stale. Cross-reference against the remote repo when possible.
3. **Local packed repo** (`knowledge-base/typst-packed.json`) — a repomix snapshot that predates this session. Stale-est source. Use only when offline.
4. **If none of the above contain the function you need, do not use it** — find an alternative syntax you CAN confirm.

### Step 0: Load Prerequisites
1. Load `typst-author` skill: `skill typst-author`
2. Verify `typst compile` is available; warn if not, but continue (syntax-only mode)
3. **Primary authority**: Remote Typst GitHub repo via `gh search code` / `gh api`. The local packed repo at `knowledge-base/typst-packed.json` is a stale snapshot — do NOT treat it as mandatory. If the packed repo is missing, proceed using the remote repo; it is not a blocker.

### Step 1: Source Consultation
Ask user:
- **Source**: "Create from scratch" or "Transform existing lesson materials"?
  - If "Transform": ask for file path(s) to existing materials (JSON, .md, .txt, .typ)
  - If "Create from scratch": ask for document purpose, topic, and content outline

### Step 2: Header Selection
Ask user:
- **Header style**: "Official school header" or "Custom/None"?
  - **Official**: Use `templates/mathayom-header.typ` — left ear ACT.png, right ear 1135082720.png, centered "Mathayom Program", rule line below
  - **Custom/None**: Ask for details, or skip header

### Step 3: Print Format
Ask user:
- **Print format**: "Single A4 sheet" or "Booklet (A5 pages, folded)"?
  - **A4**: 11pt body font, `#set page(paper: "a4")`
  - **Booklet (A5)**: 14pt body font, `#set page(paper: "a5")`
    - Inform user: A5 booklet printed 2-up on A4; 14pt body ensures readable ~10pt effective after scaling

### Step 4: Generate Typst Code

**ALL CODE IS AI-GENERATED. NEVER GUESS SYNTAX.** The remote Typst GitHub repo is the primary syntax reference. The local packed repo (`knowledge-base/typst-packed.json`) is a snapshot that may be stale. For every function call you write, you must first run a concrete query against one of these sources — prefer the remote repo.

1. Determine subfolder name: `{date-prefix}-{topic}` (e.g., `May-13-2026-mathayom-handbook`)
2. Create output directory: `typst/code/{subfolder}/`
3. **MANDATORY — concrete syntax verification protocol**. For **every** Typst function you write (`image`, `grid`, `table`, `text`, `set page`, `block`, `align`, `figure`, `circle`, `line`, `highlight`, etc.), you **must**:

   a. **Search the remote Typst GitHub repo** — primary authority:
   ```powershell
   # Search for function definition across the repo
   gh search code "pub fn image" --repo typst/typst --limit 5

   # Get a specific source file
   gh api repos/typst/typst/contents/crates/typst-library/src/visualize/image/mod.rs

   # Search test files for usage examples
   gh search code "#image(" --repo typst/typst --limit 10
   ```
   If GitHub CLI is unavailable, fall back to the local packed repo:
   ```powershell
   $json = Get-Content "knowledge-base/typst-packed.json" -Raw | ConvertFrom-Json
   $json.files.'crates/typst-library/src/visualize/image/mod.rs'
   ```

   b. **Extract and confirm the parameter signature**. Look for `#[elem]` annotation followed by `pub struct` with field comments — these define the Typst function's parameters.

   c. **Only after confirming the exact function name, parameter names, and types** may you write that function call in the `.typ` file.

   d. **If neither the remote repo nor the packed repo contain the function you need**, consult `.kilo/skills/typst-author/docs/reference/` as a third fallback. If still no match, **do not use that function** — use an alternative you can confirm.

   e. **Repeat for every single function call** — there are no shortcuts.

4. Generate `typst/code/{subfolder}/index.typ` with:
   - `#import "../../../templates/mathayom-header.typ": mathayom-header` (if official header — path is 3 levels up from `typst/code/{subfolder}/`)
   - Page setup (`set page` with correct paper and margins)
   - Font size via `set text(size: Npt)`
   - Document content
   - If transforming existing materials: embed content `#include` or inline text

**Structural template reference (syntax within must still be verified against remote GitHub repo or local docs):**
```typst
#import "../../../templates/mathayom-header.typ": mathayom-header

#set text(font: "Roboto", size: 11pt)
#set page(paper: "a4", margin: (x: 0.75in, top: 1in, bottom: 0.75in))

#mathayom-header()

= Heading

Content goes here.
```

### Step 4b: Red-Green Test Phase (RED first, then GREEN)

**RED**: Before finalizing the `.typ` code, write test assertions as a Python command. These define what the output PDF MUST contain.

**GREEN**: Run the test against the compiled PDF. If any assertion fails (RED), fix the `.typ` code and re-compile. Repeat until ALL GREEN.

#### Step 4b-i: Write test assertions (RED phase)

Based on user requirements, construct a `test_typst_output.py` command that captures every critical requirement:

```powershell
python scripts/test_typst_output.py `
    --typ-file "typst/code/{subfolder}/index.typ" `
    --pdf-output "typst/PDF/{subfolder}/index.pdf" `
    --expect-text "Mathayom Program" `
    --expect-text "Chapter 1" `
    --forbid-text "TODO" `
    --expect-page-count 2
```

Rules for writing assertions:
- `--expect-text` for EVERY critical string that must appear (header title, all headings, key content phrases)
- `--forbid-text` for every placeholder or draft marker that must be gone ("TODO", "FIXME", "lorem", placeholder text)
- `--expect-page-count` for the expected number of pages (determined from user requirements)
- When transforming existing materials: add `--expect-text` for EVERY distinct content item from the source

#### Step 4b-ii: Run tests (GREEN phase)

```powershell
python scripts/test_typst_output.py `
    --typ-file "typst/code/{subfolder}/index.typ" `
    --pdf-output "typst/PDF/{subfolder}/index.pdf" `
    --expect-text "..." `
    --forbid-text "..."
```

- Exit code 0 = ALL GREEN — proceed
- Exit code 1 = one or more RED — must fix `.typ` code and recompile until green
- **Never proceed past Step 4b with any RED test**

#### Step 4b-iii: Iterate until all green

```powershell
$tries = 0
do {
    $tries++
    Write-Host "Attempt $tries..."
    python scripts/test_typst_output.py <args>
    $passed = $LASTEXITCODE -eq 0
    if (-not $passed) { <fix .typ code and recompile> }
} while (-not $passed -and $tries -lt 10)

if (-not $passed) { Write-Host "FAILED after 10 attempts"; exit 1 }
```

Max 10 attempts. If the test never goes green, report the specific RED assertions to the user and offer to debug.

#### When this step is mandatory

- **Transform mode**: ALWAYS — every piece of source content must be tested
- **Scratch mode**: ALWAYS — at minimum test header title, page count, and heading presence

### Step 5: Compile PDF (production compile)
The PDF was already compiled during the GREEN phase (Step 4b). This step ensures the final PDF is in the correct output location.

```powershell
$subfolder = "May-13-2026-mathayom-handbook"
$source = "typst/code/$subfolder/index.typ"
$output = "typst/PDF/$subfolder/index.pdf"

typst compile --root "." $source $output
```
On success: `"PDF written to typst/PDF/$subfolder/index.pdf"`
On error: show line number and recommended fix from typst-author docs

### Step 6: Formatting
- `typstyle --check "typst/code/$subfolder/index.typ"`
- Apply `typstyle -i` only if changes are limited to newly created code

### Step 7: Integrity Check
Run **only when transforming existing material**. Compares original source text to generated output text character-by-character.

```powershell
python -c "
import sys, difflib
source_path = r'SOURCE_PATH'
typst_path = r'typst/code/SUBFOLDER/index.typ'

with open(source_path, encoding='utf-8') as f:
    source_text = f.read()
with open(typst_path, encoding='utf-8') as f:
    typst_text = f.read()

# Extract only content from .typ file (text between [])
import re
typst_content = ' '.join(re.findall(r'\[([^\]]*)\]', typst_text))

matcher = difflib.SequenceMatcher(None, source_text, typst_content)
diffs = []
for tag, i1, i2, j1, j2 in matcher.get_opcodes():
    if tag != 'equal':
        diffs.append(f'{tag}: src[{i1}:{i2}]={source_text[i1:i2]!r} -> typ[{j1}:{j2}]={typst_content[j1:j2]!r}')

if diffs:
    print(f'INTEGRITY WARNING: {len(diffs)} difference(s) found')
    for d in diffs[:10]:
        print(f'  {d}')
    if len(diffs) > 10:
        print(f'  ... and {len(diffs) - 10} more')
else:
    print('INTEGRITY PASSED: 0 differences found')
"
```

Report result to user. Always **warn and continue** — never halt.

### Step 8: Report
Summarize:
- **Source .typ**: `typst/code/{subfolder}/index.typ`
- **Output PDF**: `typst/PDF/{subfolder}/index.pdf`
- **Formatting applied**: Yes/No
- **Compilation**: Success / Error (with details)
- **Integrity**: Passed / Warning (N diffs)

## New Document Checklist
- [x] User consulted on source (scratch vs transform)
- [x] Header style selected
- [x] Print format selected (font size set accordingly)
- [x] Typst code generated in `typst/code/`
- [x] Red-Green tests: ALL GREEN (no RED)
- [x] PDF compiled to `typst/PDF/`
- [x] Formatting checked
- [x] Integrity verified (if transforming existing material)
---
name: slideshow-to-pptx
description: Converts a reveal.js HTML slideshow to a full-visual-fidelity PowerPoint .pptx file. Uses Decktape to render each slide as a PDF page via Chrome headless, then extracts pages as high-resolution images and assembles them into a PPTX using PyMuPDF and python-pptx.
---

# Skill: Slideshow to PPTX

## Purpose

Convert a reveal.js HTML slideshow (`index.html` with `assets/`) into a Microsoft PowerPoint `.pptx` file that preserves the **full visual appearance** of the original presentation. Each slide is rendered via Chrome headless and placed as a full-slide rasterized image in the PPTX.

**Pipeline position:** After `lesson-plan-to-reveal` (which generates the HTML slideshow).

**Why not Pandoc?** Pandoc's `-f html -t pptx` strips all visual styling — backgrounds, Font Awesome icons, vocabulary highlighting, colors, and layout are all lost. Decktape renders each slide exactly as it appears in the browser, preserving everything.

**Trade-off:** The PPTX slides are rasterized images. Text is NOT editable in PowerPoint. The output is a visual reproduction suitable for projection, printing, or distribution.

## When to Use This Skill

Use `slideshow-to-pptx` when:
- A teacher requests a PowerPoint version of an existing reveal.js slideshow
- The slideshow `index.html` already exists in `output/{subfolder}/slides/`
- **Visual fidelity matters** — background images, colors, icons, fonts must be preserved
- The PPTX is for projection, printing, or distribution (not text editing)

Do NOT use this skill when:
- The PPTX must have editable text
- First-time slide generation is needed (use `lesson-plan-to-reveal` first)

## Prerequisites

- **Node.js 18+** (for Decktape). Verify:
  ```powershell
  node --version
  ```
- **Decktape** installed globally:
  ```powershell
  npm install -g decktape
  ```
- **Python 3.x** packages:
  ```powershell
  pip install PyMuPDF python-pptx Pillow
  ```
- The slideshow must exist at `output/{subfolder}/slides/index.html` with all assets in `output/{subfolder}/slides/assets/`

## Workflow

### Step 0: Verify dependencies

```powershell
node --version
decktape --version
python -c "import fitz; import pptx; from PIL import Image; print('OK')"
```

### Step 1: Create output directory

```powershell
New-Item -ItemType Directory -Path "output/{subfolder}/pptx" -Force
```

### Step 2: Generate PDF with Decktape

Decktape uses Chrome headless (via Puppeteer) to open the reveal.js slideshow, render each slide via the reveal.js API, and capture it as a PDF page. This handles all reveal.js features — backgrounds, fragments (in their final visible state), auto-animate, and Font Awesome icons.

```powershell
# Work in the pptx directory so output paths stay flat
Push-Location "output/{subfolder}/pptx"

decktape reveal `
  "file:///ABSOLUTE/PATH/TO/output/{subfolder}/slides/index.html" `
  "slides.pdf" `
  --load-pause 2000 `
  --chrome-arg=--allow-file-access-from-files

Pop-Location
```

**Critical flags:**

| Flag | Purpose |
|---|---|
| `reveal` | Uses the reveal.js plugin (reads slide state via reveal.js API) |
| `--load-pause 2000` | 2s pause after page load for fonts/images to render |
| `--chrome-arg=--allow-file-access-from-files` | Required for `file://` URLs that reference local assets |

**Note about `file://` URLs:** The `slides/index.html` references local asset files (images in `assets/`). These must be accessed via `file://` with the `--allow-file-access-from-files` flag. Convert an absolute Windows path to URL format:
- Path: `C:\PROJECTS\...\slides\index.html`
- URL: `file:///C:/PROJECTS/.../slides/index.html`

**Why `Push-Location`:** Decktape expects simple filenames for output. Running from within the pptx directory keeps paths flat and avoids issues with nested directory structures.

**Output:** `output/{subfolder}/pptx/slides.pdf`

### Step 3: Build PPTX from PDF

```powershell
python scripts/pdf_to_pptx.py `
  "output/{subfolder}/pptx/slides.pdf" `
  "output/{subfolder}/pptx/{topic}-lesson-plan.pptx"
```

The script (`scripts/pdf_to_pptx.py`):
1. Opens the PDF with PyMuPDF
2. Determines page dimensions and computes zoom to reach 1920px on the long edge
3. Renders each page as a high-resolution PNG (in-memory, no temp files)
4. Creates a 1920×1080 PPTX (proportional to page aspect ratio)
5. Places each rendered page as a full-slide picture
6. Saves the PPTX

**Output:** `output/{subfolder}/pptx/{topic}-lesson-plan.pptx`

### Step 4: Verify the output

```powershell
$pptx = Get-Item "output/{subfolder}/pptx/{topic}-lesson-plan.pptx"
$pdf = Get-Item "output/{subfolder}/pptx/slides.pdf"
Write-Host "PDF: $([math]::Round($pdf.Length/1KB)) KB"
Write-Host "PPTX: $([math]::Round($pptx.Length/1KB)) KB"
```

A typical lesson plan with 37 slides produces a ~14.5MB PPTX.

### Step 5 (optional): Clean up intermediate PDF

```powershell
Remove-Item "output/{subfolder}/pptx/slides.pdf"
```

## What Survives (Everything Visual)

| Feature | Preserved? | Notes |
|---|---|---|
| Slide backgrounds (images, colors, gradients) | Yes | Rasterized from PDF page |
| Vocabulary word highlighting (`#ffdd00`) | Yes | Rendered by browser, captured in PDF |
| Font Awesome icons | Yes | Rendered by browser, captured in PDF |
| Fragment states | Yes | Captured in final visible state on slide advance |
| Auto-animate final state | Yes | Final animated state is captured |
| Background opacity | Yes | Rendered by browser |
| Speaker notes | No | In `<aside class="notes">`, not rendered on screen |
| Text content (for editing) | No | Text is rasterized — not selectable or editable |
| Hyperlinks | No | Links are rasterized as text |
| Slide transitions | No | PPTX has its own transition system |

## Known Limitations

- **Text is not editable.** Each slide is a single rasterized image.
- **Speaker notes are lost.** They exist in `<aside class="notes">` in the HTML but are not rendered on screen.
- **Hyperlinks are not clickable.** They are rasterized as text in the image.
- **Audio/video is not captured.** Media elements are not rendered in the PDF export.
- **Fragment stepping is lost.** Only the final visible state of each slide (with all fragments revealed) is captured.
- **File size is larger** than a text-based PPTX (~14.5MB vs ~30KB for 37 slides).

## Files

| File | Purpose |
|---|---|
| `output/{subfolder}/slides/index.html` | Input: reveal.js slideshow |
| `output/{subfolder}/slides/assets/` | Input: images and media |
| `output/{subfolder}/pptx/slides.pdf` | Intermediate: Decktape PDF (can be deleted) |
| `output/{subfolder}/pptx/{topic}-lesson-plan.pptx` | **Output: PowerPoint file** |
| `scripts/pdf_to_pptx.py` | Build script — renders PDF pages and assembles PPTX |

## Dependencies

- Node.js 18+ (for Decktape via `npm install -g decktape`)
- Python 3.x packages: `PyMuPDF`, `python-pptx`, `Pillow`
- Chrome/Chromium (bundled with Puppeteer inside Decktape — no separate install)
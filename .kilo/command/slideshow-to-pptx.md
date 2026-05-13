---
description: Converts a reveal.js HTML slideshow to a full-visual-fidelity PowerPoint .pptx file using Decktape (Chrome headless → PDF) and PyMuPDF (PDF pages → PPTX slides). Each slide becomes a rasterized full-slide image preserving all visual styling.
---

# Command: Slideshow to PPTX

## Usage
`/slideshow-to-pptx <subfolder> [topic-name]`

Converts `output/{subfolder}/slides/index.html` to `output/{subfolder}/pptx/{topic}-lesson-plan.pptx`.

## What it does
1. Loads the `slideshow-to-pptx` skill
2. Verifies all dependencies (Node.js, Decktape, Python packages)
3. Creates `pptx/` output directory
4. Renders the slideshow to PDF via Decktape (Chrome headless)
5. Converts each PDF page to a high-res PNG and assembles into PPTX
6. Reports the output path and file sizes

## Prerequisites
- Node.js 18+ (for Decktape)
- Decktape installed globally: `npm install -g decktape`
- Python packages: `PyMuPDF`, `python-pptx`, `Pillow`
- Slideshow must exist at `output/{subfolder}/slides/index.html`

## Workflow

### Step 1: Load the skill
`skill slideshow-to-pptx`

This loads the full pipeline details including Decktape flags and script paths.

### Step 2: Verify dependencies
```powershell
node --version
decktape --version
python -c "import fitz; import pptx; from PIL import Image; print('OK')"
```

If any check fails, abort with installation instructions.

### Step 3: Create output directory
```powershell
New-Item -ItemType Directory -Path "output/{subfolder}/pptx" -Force
```

### Step 4: Determine the topic name
If `<topic-name>` argument provided, use it. Otherwise extract from the slideshow:
```powershell
$content = Get-Content "output/{subfolder}/slides/index.html" -Raw
if ($content -match '<h1>(.*?)<') { $topic = $matches[1] } else { $topic = $subfolder }
```

### Step 5: Render PDF with Decktape
```powershell
Push-Location "output/{subfolder}/pptx"

$absPath = (Resolve-Path "../slides/index.html").Path
$url = "file:///$($absPath.Replace('\','/'))"

decktape reveal $url "slides.pdf" --load-pause 2000 --chrome-arg=--allow-file-access-from-files

Pop-Location
```

### Step 6: Build PPTX from PDF
```powershell
python scripts/pdf_to_pptx.py "output/{subfolder}/pptx/slides.pdf" "output/{subfolder}/pptx/$topic-lesson-plan.pptx"
```

### Step 7: Verify and report
```powershell
$pptx = Get-Item "output/{subfolder}/pptx/$topic-lesson-plan.pptx"
$pdf = Get-Item "output/{subfolder}/pptx/slides.pdf"
Write-Host "PDF: $([math]::Round($pdf.Length/1KB)) KB"
Write-Host "PPTX: $([math]::Round($pptx.Length/1KB)) KB"
Write-Host "Output: $($pptx.FullName)"
```

### Step 8 (optional): Clean up intermediate PDF
```powershell
Remove-Item "output/{subfolder}/pptx/slides.pdf" -Force
```

## Known Limitations
- **Text is NOT editable** — each slide is a rasterized image
- **Fragment/auto-animate**: only the final visible state is captured
- **Speaker notes**: not included
- **Hyperlinks**: rasterized, not clickable

## Edge cases
- **No arguments**: "Error: subfolder name required — usage: /slideshow-to-pptx <subfolder> [topic-name]"
- **Slideshow not found**: "Error: output/{subfolder}/slides/index.html does not exist"
- **Decktape not installed**: "Install Decktape: npm install -g decktape"
- **Node.js not found**: "Install Node.js 18+ from https://nodejs.org"
- **Decktape fails**: Print error output; check that Chrome can access file:// URLs
- **Push-Location fails**: The pptx directory may not exist — create it first

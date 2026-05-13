---
description: Auto-detect all slideshows in output/ and deploy each to its own subfolder on gh-pages. Updates the landing page card grid, commits, and pushes.
---
# Command: Git Pages

## Usage
`/git-pages`

No arguments needed. The command scans `output/` for all subdirectories containing `slides/index.html` and deploys every one.

## What it does
1. Scans `output/` for all subdirectories with `slides/index.html`
2. Warns if none found and stops
3. Runs `/lint`
4. Detects remote owner/repo from `git remote get-url origin`
5. Copies each slideshow to a temp directory (preserves source files)
6. Fetches or creates the gh-pages branch
7. Copies each slideshow into its own subfolder
8. Generates/updates root `index.html` (card grid landing page for ALL presentations)
9. Commits, pushes, returns to `main`
10. Prints the landing page URL

## Prerequisites
- `gh` CLI installed and authenticated (`gh auth status`)
- At least one subfolder in `output/` containing `slides/index.html`
- Remote `origin` is a GitHub repo

## Workflow

### Step 0: Auto-detect all slideshows in output/
```powershell
$presentations = @()
Get-ChildItem -Path "output" -Directory | ForEach-Object {
    $slidesHtml = Join-Path $_.FullName "slides\index.html"
    if (Test-Path $slidesHtml) {
        $presentations += @{ subfolder = $_.Name }
    }
}

if ($presentations.Count -eq 0) {
    Write-Error "No slideshows found — no output/*/slides/index.html exists"
    exit 1
}

Write-Host "Detected $($presentations.Count) slideshow(s):"
$presentations | ForEach-Object { Write-Host "  - $($_.subfolder)" }
```

### Step 1: Check prerequisites
```powershell
if (-not (gh auth status 2>&1 | Select-String "Logged in")) {
    Write-Error "gh CLI not authenticated — run 'gh auth login' first"
    exit 1
}
```

### Step 2: Detect remote
```powershell
$remoteUrl = git remote get-url origin
if ($remoteUrl -match "github\.com[:\/](.+)/(.+)\.git") {
    $owner = $matches[1]
    $repo = $matches[2]
} else {
    Write-Error "Remote origin is not a GitHub repo"
    exit 1
}
```

### Step 3: Lint
```powershell
python -m ruff check --fix . ; python -m ruff format .
```

### Step 4: Save current branch and copy ALL slideshows to temp
```powershell
$originalBranch = git rev-parse --abbrev-ref HEAD
$tmp = "$env:TEMP\gh-pages-deploy"
if (Test-Path $tmp) { Remove-Item -Recurse -Force $tmp }
New-Item -ItemType Directory -Force -Path $tmp | Out-Null

foreach ($p in $presentations) {
    $src = "output/$($p.subfolder)/slides"
    $dst = Join-Path $tmp $p.subfolder
    New-Item -ItemType Directory -Force -Path $dst | Out-Null
    Copy-Item -Recurse -Force "$src\*" $dst
    Write-Host "  Copied $($p.subfolder) to temp"
}
```

### Step 5a: Fetch gh-pages and check if it exists
```powershell
git fetch origin gh-pages 2>$null
$ghPagesExists = $LASTEXITCODE -eq 0
```

### Step 5b: Switch to gh-pages branch
```powershell
if ($ghPagesExists) {
    git checkout gh-pages
} else {
    # First deploy — create orphan branch
    git checkout --orphan gh-pages
    git rm -rf .
    git clean -fd
}
```

### Step 6: Copy ALL slideshows into their subfolders
```powershell
Get-ChildItem -Path $tmp -Directory | ForEach-Object {
    $subfolder = $_.Name
    New-Item -ItemType Directory -Force -Path $subfolder | Out-Null
    Copy-Item -Recurse -Force "$($_.FullName)\*" "$subfolder/"
    Write-Host "  Deployed $subfolder to gh-pages"
}
```

### Step 7: Generate/update root landing page (card grid)
```powershell
# Find all subdirectories containing index.html
$allPresentations = @()
git ls-tree --name-only HEAD | Where-Object { $_ -ne "index.html" } | ForEach-Object {
    $dir = $_
    $htmlPath = "$dir/index.html"
    $title = "Presentation"
    if (Test-Path $htmlPath) {
        $content = Get-Content $htmlPath -Raw
        if ($content -match '<title>(.*?)</title>') {
            $title = $matches[1]
        }
    }
    $allPresentations += @{ dir = $dir; title = $title }
}

# Generate landing page HTML
$cardsHtml = ""
foreach ($p in $allPresentations) {
    $cardsHtml += @"
            <a href="$($p.dir)/" class="card">
                <div class="card-title">$($p.title)</div>
                <div class="card-dir">$($p.dir)</div>
            </a>

"@
}

$landingPage = @"
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Lesson Plan Slides</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
            background: #f0f2f5;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 60px 20px;
        }
        h1 {
            font-size: 2.2em;
            color: #1a1a2e;
            margin-bottom: 40px;
            text-align: center;
        }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 20px;
            max-width: 960px;
            width: 100%;
        }
        .card {
            background: white;
            border-radius: 12px;
            padding: 28px 24px;
            text-decoration: none;
            color: #333;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            transition: transform 0.2s, box-shadow 0.2s;
            display: flex;
            flex-direction: column;
            gap: 8px;
        }
        .card:hover {
            transform: translateY(-4px);
            box-shadow: 0 8px 24px rgba(0,0,0,0.12);
        }
        .card-title {
            font-size: 1.15em;
            font-weight: 600;
            color: #1a1a2e;
        }
        .card-dir {
            font-size: 0.85em;
            color: #888;
            font-family: 'Consolas', monospace;
        }
        footer {
            margin-top: 50px;
            font-size: 0.85em;
            color: #aaa;
        }
    </style>
</head>
<body>
    <h1>Lesson Plan Slides</h1>
    <div class="grid">
$cardsHtml    </div>
    <footer>Lesson Plan Writer 3</footer>
</body>
</html>
"@

Set-Content -Path "index.html" -Value $landingPage -NoNewline
```

### Step 8: Commit and push
```powershell
$date = Get-Date -Format "ddMMyy"
$count = $presentations.Count
git add -A
git commit -m "Deploy $count slideshow(s) ($date)"
git push origin gh-pages
```

### Step 9: Return to original branch
```powershell
git checkout $originalBranch
```

### Step 10: Print URLs
```powershell
Write-Host ""
Write-Host "Deployed $count slideshow(s):"
foreach ($p in $presentations) {
    Write-Host "  https://$owner.github.io/$repo/$($p.subfolder)/"
}
Write-Host ""
Write-Host "Landing page: https://$owner.github.io/$repo/"
```

## Edge cases
- **First deploy**: creates orphan gh-pages branch automatically
- **No slides found**: aborts with clear error before any git operations
- **gh not authenticated**: aborts with instruction to run `gh auth login`
- **Push fails**: stays on gh-pages branch for debugging; error is printed
- **Landing page**: regenerated each time, listing ALL presentations on gh-pages
- **Existing subfolders on gh-pages**: preserved — only updated if source was copied
---
description: Deploy a single slideshow from output/ to its subfolder on gh-pages. Updates the landing page card grid, commits, and pushes.
---
# Command: Git Pages

## Usage
`/git-pages [subfolder]`

If `subfolder` is provided, only that slideshow is deployed. If omitted, you will be prompted for one.

Examples:
```
/git-pages M2_Lesson01_Listening
/git-pages M3_Lesson01_Listening
```

## What it does
1. Scans `output/` for the requested slideshow
2. Warns if none found and stops
3. Runs `/lint`
4. Copies the slideshow to a temp staging directory
5. Creates/updates a git worktree for the gh-pages branch in a **separate** temp directory
6. Copies the slideshow into its own subfolder inside the worktree
7. Regenerates the root `index.html` (card grid listing ALL presentations on gh-pages)
8. Commits and pushes from the worktree
9. Removes the worktree — `main` is never switched away from
10. Prints the URL

## Safety
**This command NEVER switches branches in the main working tree.** All gh-pages operations happen inside a `git worktree` — a separate directory that acts as an independent checkout. If anything fails, the main project directory is completely untouched. No stashing, no `git clean`, no `Remove-Item` on project files.

All worktree git commands use `git -C $worktreeDir` explicitly. No `Push-Location` / `Pop-Location` is used — those do not survive across separate command executions.

## Regression Guard
A red-green safety test at `tests/test_git_pages_safety.py` (12 tests) scans this command file for forbidden patterns. It FAILS if any of these are re-introduced:
- `git checkout gh-pages` — direct branch switch in the working tree
- `git rm -rf .` — destroys tracked files
- `git clean -fd` — destroys untracked files globally
- Missing `git worktree add` or `git -C $worktreeDir` — worktree isolation not in use

Run: `python -m pytest tests/test_git_pages_safety.py -v`

## Prerequisites
- `gh` CLI installed and authenticated (`gh auth status`)
- At least one subfolder in `output/` containing `slides/index.html`
- Remote `origin` is a GitHub repo

## Workflow

### Step 0: Detect the target slideshow
```powershell
$targetSubfolder = $args[0]
if (-not $targetSubfolder) {
    $targetSubfolder = Read-Host "Enter the subfolder to deploy (e.g. M2_Lesson01_Listening)"
}

$slidesHtml = "output/$targetSubfolder/slides/index.html"
if (-not (Test-Path $slidesHtml)) {
    Write-Error "No slideshow found at output/$targetSubfolder/slides/index.html"
    Write-Host "Available slideshows:"
    Get-ChildItem "output" -Directory | ForEach-Object {
        $testPath = Join-Path $_.FullName "slides\index.html"
        if (Test-Path $testPath) { Write-Host "  - $($_.Name)" }
    }
    exit 1
}

$presentations = @(@{ subfolder = $targetSubfolder })
Write-Host "Deploying: $targetSubfolder"
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

### Step 4: Copy slideshows to a staging temp directory
```powershell
$staging = "$env:TEMP\gh-pages-staging"
if (Test-Path $staging) { Remove-Item -Recurse -Force -Path $staging }
New-Item -ItemType Directory -Force -Path $staging | Out-Null

foreach ($p in $presentations) {
    $src = "output/$($p.subfolder)/slides"
    $dst = Join-Path $staging $p.subfolder
    New-Item -ItemType Directory -Force -Path $dst | Out-Null
    Copy-Item -Recurse -Force "$src\*" $dst
    Write-Host "  Copied $($p.subfolder) to staging"
}
```

### Step 5: Create/update the gh-pages worktree
```powershell
$worktreeDir = "$env:TEMP\gh-pages-worktree"

# Remove any leftover worktree from a previous run
git worktree remove $worktreeDir 2>$null
if (Test-Path $worktreeDir) { Remove-Item -Recurse -Force -Path $worktreeDir }

# Fetch the remote gh-pages branch
git fetch origin gh-pages 2>$null
$ghPagesExists = $LASTEXITCODE -eq 0

if ($ghPagesExists) {
    Write-Host "Adding worktree for existing gh-pages branch..."
    git worktree add $worktreeDir gh-pages 2>$null
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Failed to create worktree. Exiting — no project files touched."
        exit 1
    }
} else {
    # First deploy: push empty commit to gh-pages from isolated temp repo
    # NEVER touches the main working tree — no checkout, no git rm, no clean
    Write-Host "Creating gh-pages branch for first deploy..."
    $bootstrapDir = "$env:TEMP\gh-pages-bootstrap"
    if (Test-Path $bootstrapDir) { Remove-Item -Recurse -Force $bootstrapDir }
    New-Item -ItemType Directory -Force -Path $bootstrapDir | Out-Null
    Push-Location $bootstrapDir
    git init
    git remote add origin $remoteUrl
    New-Item -ItemType File -Name ".gitkeep" -Value "" | Out-Null
    git add -A
    git commit -m "Initial empty gh-pages"
    git push origin HEAD:gh-pages
    Pop-Location
    Remove-Item -Recurse -Force $bootstrapDir

    # Now add the worktree
    git worktree add $worktreeDir gh-pages
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Failed to create worktree after first deploy. Exiting."
        exit 1
    }
}

Write-Host "Worktree ready at $worktreeDir"
```

### Step 6: Copy all slideshows into the worktree
```powershell
Get-ChildItem -Path $staging -Directory | ForEach-Object {
    $subfolder = $_.Name
    $destDir = Join-Path $worktreeDir $subfolder
    New-Item -ItemType Directory -Force -Path $destDir | Out-Null
    Copy-Item -Recurse -Force "$($_.FullName)\*" "$destDir/"
    Write-Host "  Deployed $subfolder"
}
```

### Step 7: Generate/update root landing page (card grid)
```powershell
# All path/file operations target $worktreeDir explicitly.
# All git commands use git -C $worktreeDir.
# No Push-Location — it doesn't survive across separate command executions.
$allPresentations = @()
git -C $worktreeDir ls-tree --name-only HEAD | Where-Object { $_ -ne "index.html" } | ForEach-Object {
    $dir = $_
    $htmlPath = Join-Path $worktreeDir "$dir/index.html"
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

Set-Content -Path (Join-Path $worktreeDir "index.html") -Value $landingPage -NoNewline
```

### Step 8: Commit and push from worktree
```powershell
$date = Get-Date -Format "ddMMyy"
git -C $worktreeDir add -A
git -C $worktreeDir commit -m "Deploy $($presentations[0].subfolder) ($date)"
git -C $worktreeDir push origin gh-pages
```

### Step 9: Clean up worktree and return to main
```powershell
git worktree remove $worktreeDir
Write-Host "Worktree removed. Still on main."
```

### Step 10: Print URL
```powershell
$subfolder = $presentations[0].subfolder
Write-Host ""
Write-Host "Deployed: $subfolder"
Write-Host "  https://$owner.github.io/$repo/$subfolder/"
Write-Host ""
Write-Host "Landing page: https://$owner.github.io/$repo/"
```

### Step 10a: Write URL to lesson plan JSON
```powershell
$lessonPlanJson = Get-ChildItem -Path "output/$subfolder" -Filter "*-lesson-plan.json" | Select-Object -First 1
if ($lessonPlanJson) {
    $jsonContent = Get-Content $lessonPlanJson.FullName -Raw | ConvertFrom-Json
    $url = "https://$owner.github.io/$repo/$subfolder/"
    if ($jsonContent.slideshow_url -ne $url) {
        $jsonContent | Add-Member -MemberType NoteProperty -Name "slideshow_url" -Value $url -Force
        $jsonContent | ConvertTo-Json -Depth 10 | Set-Content $lessonPlanJson.FullName
        Write-Host "  Wrote URL to $($lessonPlanJson.Name)"
    } else {
        Write-Host "  URL already up to date in $($lessonPlanJson.Name)"
    }
} else {
    Write-Warning "  No lesson plan JSON found in output/$subfolder/"
}
```

## Edge cases
- **No argument**: prompts interactively for the subfolder name
- **Not found**: lists available slideshows and exits
- **First deploy**: pushes an empty commit from an isolated `git init` in %TEMP% — never touches the working tree
- **gh not authenticated**: aborts with instruction to run `gh auth login`
- **Worktree add fails**: exits with error; main directory untouched; stale worktree cleaned up
- **Push fails**: worktree is left on disk for manual recovery; error is printed
- **Landing page**: regenerated each time, listing ALL presentations on gh-pages
- **Existing subfolders on gh-pages**: preserved — only updated if source was copied

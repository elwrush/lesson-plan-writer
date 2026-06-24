---
description: Deploy or update a single slideshow on gh-pages. Detects whether the subfolder already exists and acts accordingly.
---
# Command: Git Pages

## Usage
`/git-pages [subfolder]`

If `subfolder` is provided, only that slideshow is deployed/updated. If omitted, you will be prompted for one.

**New deploy** = the slideshow subfolder does NOT exist on gh-pages yet. Creates the gh-pages branch if needed and pushes the slideshow for the first time.

**Update** = the slideshow subfolder ALREADY exists on gh-pages. Overwrites the existing files, regenerates the landing page, and pushes.

**Do NOT ask the user whether to deploy or update — detect it automatically.** Check if `git ls-tree --name-only origin/gh-pages 2>$null` lists the subfolder. If yes → update. If no → new deploy.

Examples:
```
/git-pages M2-WRITING-COMPOUND-SENTENCES-L2
/git-pages M2_Lesson01_Listening
```

## What it does
1. Scans `output/` for the requested slideshow
2. Warns if none found and stops
3. **Detects** whether this is a new deploy or an update (by checking gh-pages branch for the subfolder)
4. Runs `/lint`
5. **Rebuilds `index.html` from `slides.md`** using pandoc with auto-discovered Lua filters (prevents stale-HTML deploys)
6. Copies the slideshow to a temp staging directory
7. Creates/updates a git worktree for the gh-pages branch in a **separate** temp directory
8. Copies the slideshow into its own subfolder inside the worktree (overwrites if updating)
9. Regenerates the root `index.html` (card grid listing ALL presentations on gh-pages)
10. Commits and pushes from the worktree
11. Removes the worktree — `main` is never switched away from
12. Prints the URL

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

### Step 0: Detect the target slideshow and determine deploy vs update
```powershell
$targetSubfolder = $args[0]
if (-not $targetSubfolder) {
    $targetSubfolder = Read-Host "Enter the subfolder to deploy (e.g. M2_WRITING_COMPOUND_SENTENCES_L2)"
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

# Detect whether this is a new deploy or an update
git fetch origin gh-pages 2>$null
$subfolderExists = git ls-tree --name-only origin/gh-pages 2>$null | Select-String "^$([regex]::Escape($targetSubfolder))$" -Quiet
if ($subfolderExists) {
    Write-Host "UPDATE: $targetSubfolder (already exists on gh-pages, overwriting files)"
} else {
    Write-Host "NEW DEPLOY: $targetSubfolder (first time on gh-pages)"
}
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

### Step 4: Rebuild index.html from slides.md (prevents stale-HTML deploys)
This step runs pandoc to regenerate `index.html` from `slides.md` using the Lua filters
present in the slides directory. If `index.html` is already newer than `slides.md`,
rebuild is skipped (use `--force` to override).

```powershell
$slidesDir = Resolve-Path "output/$targetSubfolder/slides"
python scripts/rebuild_slides.py $slidesDir
if ($LASTEXITCODE -ne 0) {
    Write-Error "Rebuild failed — fix the error and try again"
    exit 1
}
```

### Step 5: Copy slideshows to a staging temp directory
```powershell
$staging = "$env:TEMP\gh-pages-staging"
if (Test-Path $staging) { Remove-Item -Recurse -Force -Path $staging }
New-Item -ItemType Directory -Force -Path $staging | Out-Null

foreach ($p in $presentations) {
    $src = "output/$($p.subfolder)/slides"
    $dst = Join-Path $staging $p.subfolder
    New-Item -ItemType Directory -Force -Path $dst | Out-Null
    robocopy "$src" "$dst" /E /IS /NFL /NDL /NJH /NJS /NP
    Write-Host "  Copied $($p.subfolder) to staging"
}
```

### Step 6: Add the gh-pages worktree (shared by both new deploy and update)

**PowerShell trap:** Never append `2>&1` to a multi-line command — it gets parsed as a separate command name. Use `2>$null` for stderr suppression and check `$?` instead of `$LASTEXITCODE` after redirects.

```powershell
$worktreeDir = "$env:TEMP\gh-pages-worktree"

# Remove any leftover worktree from a previous run
git worktree remove $worktreeDir 2>$null
if (Test-Path $worktreeDir) { Remove-Item -Recurse -Force -Path $worktreeDir }

# Fetch the remote gh-pages branch
git fetch origin gh-pages 2>$null
$ghPagesExists = $?
```

### Step 7: Copy all slideshows into the worktree
```powershell
Get-ChildItem -Path $staging -Directory | ForEach-Object {
    $subfolder = $_.Name
    $destDir = Join-Path $worktreeDir $subfolder
    New-Item -ItemType Directory -Force -Path $destDir | Out-Null
    Copy-Item -Recurse -Force "$($_.FullName)\*" "$destDir/"
    Write-Host "  Deployed $subfolder"
}
```

### Step 8: Generate/update root landing page (card grid)

**Do NOT build the landing page inline in PowerShell here-strings.** PowerShell's `@""@` syntax breaks on CSS curly braces, and `2>&1` at the end of multi-line blocks is parsed as a separate command. Use a Python script written to `$env:TEMP\kilo\gen_landing.py` instead.

```powershell
@"
import subprocess, os, re, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

worktree = r'$env:TEMP\gh-pages-worktree'

result = subprocess.run(['git', '-C', worktree, 'ls-tree', '--name-only', 'HEAD'],
                       capture_output=True, text=True, timeout=30)
dirs = [d.strip() for d in result.stdout.splitlines() if d.strip() and d.strip() != 'index.html']

presentations = []
for d in dirs:
    html_path = os.path.join(worktree, d, 'index.html')
    if os.path.exists(html_path):
        with open(html_path, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read(5000)
        if '<div class=\"slides\">' in content:
            title_match = re.search(r'<title>(.*?)</title>', content)
            title = title_match.group(1) if title_match else 'Presentation'
            presentations.append({'dir': d, 'title': title})

presentations.sort(key=lambda p: p['dir'])

cards = []
for p in presentations:
    cards.append(f'            <a href=\"{p[\"dir\"]}/\" class=\"card\">')
    cards.append(f'                <div class=\"card-title\">{p[\"title\"]}</div>')
    cards.append(f'                <div class=\"card-dir\">{p[\"dir\"]}</div>')
    cards.append(f'            </a>')
cards_html = chr(10).join(cards)

landing = '''<!DOCTYPE html>
<html lang=\"en\">
<head>
    <meta charset=\"utf-8\" />
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
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
        h1 { font-size: 2.2em; color: #1a1a2e; margin-bottom: 40px; text-align: center; }
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
        .card:hover { transform: translateY(-4px); box-shadow: 0 8px 24px rgba(0,0,0,0.12); }
        .card-title { font-size: 1.15em; font-weight: 600; color: #1a1a2e; }
        .card-dir { font-size: 0.85em; color: #888; font-family: 'Consolas', monospace; }
        footer { margin-top: 50px; font-size: 0.85em; color: #aaa; }
    </style>
</head>
<body>
    <h1>Lesson Plan Slides</h1>
    <div class=\"grid\">
''' + cards_html + '''
    </div>
    <footer>Lesson Plan Writer 3</footer>
</body>
</html>'''

with open(os.path.join(worktree, 'index.html'), 'w', encoding='utf-8') as f:
    f.write(landing)

print(f'Landing page generated -- {len(presentations)} presentations')
"@ | Set-Content -LiteralPath "$env:TEMP\kilo\gen_landing.py" -Encoding UTF8

# Execute the landing page generator
python "$env:TEMP\kilo\gen_landing.py"
if ($LASTEXITCODE -ne 0) {
    Write-Error "Landing page generation failed"
    exit 1
}
```

### Step 9: Commit and push from worktree
```powershell
$date = Get-Date -Format "ddMMyy"
git -C $worktreeDir add -A
git -C $worktreeDir commit -m "Deploy $($presentations[0].subfolder) ($date)"
git -C $worktreeDir push origin gh-pages
```

### Step 10: Clean up worktree and return to main
```powershell
git worktree remove $worktreeDir
Write-Host "Worktree removed. Still on main."
```

### Step 11: Print URL
```powershell
$subfolder = $presentations[0].subfolder
Write-Host ""
Write-Host "Deployed: $subfolder"
Write-Host "  https://$owner.github.io/$repo/$subfolder/index.html"
Write-Host ""
Write-Host "Landing page: https://$owner.github.io/$repo/"
```

### Step 11a: Write URL to lesson plan file (JSON or Markdown)
```powershell
$url = "https://$owner.github.io/$repo/$([System.Uri]::EscapeUriString("$subfolder/"))index.html"

# Try JSON first
$lessonPlanJson = Get-ChildItem -Path "output/$subfolder" -Filter "*-lesson-plan.json" | Select-Object -First 1
if ($lessonPlanJson) {
    $jsonContent = Get-Content $lessonPlanJson.FullName -Raw | ConvertFrom-Json
    if ($jsonContent.slideshow_url -ne $url) {
        $jsonContent | Add-Member -MemberType NoteProperty -Name "slideshow_url" -Value $url -Force
        $jsonContent | ConvertTo-Json -Depth 10 | Set-Content $lessonPlanJson.FullName
        Write-Host "  Wrote URL to $($lessonPlanJson.Name)"
    } else {
        Write-Host "  URL already up to date in $($lessonPlanJson.Name)"
    }
} else {
    # Fall back to Markdown lesson plan file (YAML frontmatter)
    $lessonPlanMd = Get-ChildItem -Path "output/$subfolder" -Filter "*-lesson-plan.md" | Select-Object -First 1
    if (-not $lessonPlanMd) {
        $lessonPlanMd = Get-ChildItem -Path "output/$subfolder" -Filter "*.md" | Where-Object {
            (Get-Content $_.FullName -TotalCount 1) -eq "---"
        } | Select-Object -First 1
    }
    if ($lessonPlanMd) {
        $content = Get-Content $lessonPlanMd.FullName -Raw
        if ($content -match '(?<=slideshow_url:\s*")[^"]+(?=")') {
            $currentUrl = $matches[0]
            if ($currentUrl -ne $url) {
                $content = $content -replace '(slideshow_url:\s*")[^"]+(")', "`$1$url`$2"
                Set-Content -Path $lessonPlanMd.FullName -Value $content
                Write-Host "  Wrote URL to $($lessonPlanMd.Name)"
            } else {
                Write-Host "  URL already up to date in $($lessonPlanMd.Name)"
            }
        } else {
            # No slideshow_url field yet — add it after the shape_name line
            $content = $content -replace '(shape_name: "[^"]+")', "`$1`nslideshow_url: `"$url`""
            Set-Content -Path $lessonPlanMd.FullName -Value $content
            Write-Host "  Added slideshow_url to $($lessonPlanMd.Name)"
        }
    } else {
        Write-Warning "  No lesson plan file found in output/$subfolder/"
    }
}
```

### Step 11b: Republish PDF with updated slideshow URL
If the lesson plan JSON was updated in step 10a, regenerate the PDF so the Slideshow URL cell reflects the deployment URL.
```powershell
if ($lessonPlanJson -and $jsonContent.slideshow_url -eq $url) {
    $pdfScript = "scripts/json_to_pdf.py"
    if (Test-Path $pdfScript) {
        python $pdfScript $lessonPlanJson.FullName
    }
}
```

## Edge cases
- **No argument**: prompts interactively for the subfolder name
- **Not found**: lists available slideshows and exits
- **New deploy vs update**: detected automatically in Step 0 by checking `git ls-tree --name-only origin/gh-pages`. Do NOT ask the user.
- **First deploy (gh-pages branch doesn't exist)**: pushes an empty commit from an isolated `git init` in %TEMP% (via `git -C`, never Push-Location). Then proceeds with the normal worktree flow.
- **Update (subfolder already exists)**: files are simply overwritten in Step 6. The old files are replaced; the landing page is regenerated with all presentations.
- **gh not authenticated**: aborts with instruction to run `gh auth login`
- **Worktree add fails**: exits with error; main directory untouched; stale worktree cleaned up
- **Push fails**: worktree is left on disk for manual recovery; error is printed
- **Landing page**: regenerated each time, listing ALL presentations on gh-pages
- **PowerShell `2>&1` trap**: Never append `2>&1` to a multi-line PowerShell command — it gets parsed as a separate command name (e.g., `The term '2>&1' is not recognized`). Use `2>$null` for stderr suppression and check `if ($?)` for exit code. For getting stdout+stderr combined, redirect to a file instead. This applies to ALL PowerShell commands in this file, not just git commands.

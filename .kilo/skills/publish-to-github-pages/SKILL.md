---
name: publish-to-github-pages
description: Publishes a reveal.js slide site to GitHub Pages. Pushes the slides directory to the gh-pages branch and returns the live URL.
---
# Skill: Publish to GitHub Pages

## Purpose
Publish a generated `slides/` directory to GitHub Pages so the presentation is accessible via a public URL.

## Prerequisites
- `gh` CLI must be installed and authenticated (`gh auth status`)
- Repository must be on GitHub
- `slides/` directory must exist with `index.html` (or `index2.html` — see Step 1)

## Workflow

### Step 1: Verify inputs
- Check that `slides/` directory exists with `index.html` or `index2.html`
- If only `index2.html` exists (no `index.html`), rename it to `index.html` in the source:
  ```powershell
  if (Test-Path "output/{subfolder}/slides/index2.html") {
      Remove-Item "output/{subfolder}/slides/index.html" -ErrorAction SilentlyContinue
      Rename-Item "output/{subfolder}/slides/index2.html" "index.html"
  }
  ```
- Detect GitHub remote URL: `git remote get-url origin`
- Extract owner and repo from remote URL (format: `https://github.com/{owner}/{repo}.git`)
- Save current branch name: `$originalBranch = git rev-parse --abbrev-ref HEAD`

### Step 2: Publish to gh-pages branch

**CRITICAL**: The `git checkout --orphan` + `git rm -rf .` workflow destroys ALL tracked files in the working tree, including the source `output/{subfolder}/slides/` directory. **Always copy slides to a temp directory BEFORE switching branches.**

```powershell
# --- 2a. Copy slides to temp directory (preserves source files) ---
$tmp = "$env:TEMP\gh-pages-deploy"
if (Test-Path $tmp) { Remove-Item -Recurse -Force $tmp }
New-Item -ItemType Directory -Force -Path $tmp | Out-Null
Copy-Item -Recurse -Force "output/{subfolder}/slides/*" $tmp
```

**If gh-pages branch does NOT exist (first deploy):**
```powershell
# --- 2b. Create orphan gh-pages branch ---
git checkout --orphan gh-pages

# --- 2c. Remove all tracked files PLUS untracked junk ---
git rm -rf .
git clean -fd

# --- 2d. Copy slides from temp to branch root ---
Copy-Item -Recurse -Force "$tmp\*" .

# --- 2e. Verify index.html exists at root ---
if (-not (Test-Path "index.html")) {
    Write-Error "index.html not found at branch root — aborting"
    git checkout $originalBranch
    exit 1
}

# --- 2f. Commit and force-push (orphan has no history) ---
git add -A
git commit -m "Deploy slides: {topic} ({date})"
git push origin gh-pages --force

# --- 2g. Return to original branch ---
git checkout $originalBranch
```

**If gh-pages branch ALREADY exists (update existing deploy):**
```powershell
# --- 2b. Switch to gh-pages ---
git checkout gh-pages

# --- 2c. Clean existing content (single-site root deploy) ---
git rm -rf .
git clean -fd

# --- 2d. Copy slides from temp to branch root ---
Copy-Item -Recurse -Force "$tmp\*" .

# --- 2e. Verify index.html exists at root ---
if (-not (Test-Path "index.html")) {
    Write-Error "index.html not found at branch root — aborting"
    git checkout $originalBranch
    exit 1
}

# --- 2f. Commit and push ---
git add -A
git commit -m "Update slides: {topic} ({date})"
git push origin gh-pages

# --- 2g. Return to original branch ---
git checkout $originalBranch
```

### Step 3: Enable GitHub Pages (if needed)
```powershell
gh api repos/{owner}/{repo}/pages --method POST -f "source[branch]=gh-pages" -f "source[path]=/"
```
This is idempotent — safe to run even if already enabled. Run AFTER the push so the branch exists.

If GitHub Pages is already enabled, the API returns HTTP 409 — this is expected and safe to ignore.

### Step 4: Return the URL
- Single-site deploy: `https://{owner}.github.io/{repo}/`
- Multi-presentation subfolder: `https://{owner}.github.io/{repo}/{presentation}/`
- Note: GitHub Pages may take 1–2 minutes to build after the push

## Publishing Subfolder (Multiple Presentations)
To publish each presentation to its own subdirectory:
```powershell
# Temp copy as usual first
$tmp = "$env:TEMP\gh-pages-deploy"
Copy-Item -Recurse -Force "output/{subfolder}/slides/*" $tmp

# Switch to gh-pages and add subfolder
git checkout gh-pages
New-Item -ItemType Directory -Force -Path "{presentation}" | Out-Null
Copy-Item -Recurse -Force "$tmp\*" "{presentation}/"
git add -A
git commit -m "Add slides: {presentation}"
git push origin gh-pages
git checkout $originalBranch
```
URL: `https://{owner}.github.io/{repo}/{presentation}/`

## Constraints
- Must NOT destroy existing gh-pages content for other presentations
- Must preserve index.html for other presentations (use subfolder approach for multi-site)
- Must work with already-authenticated gh CLI
- Must return to the original branch after push
- Force-push to gh-pages for first-time orphan branch deploy is acceptable (it's a deployment artifact, not source)
- Source `output/{subfolder}/slides/` directory must remain intact after deployment

## Troubleshooting

### gh CLI not found after install
After `winget install GitHub.cli`, the current PowerShell session may not have `gh` in PATH. Either:
- Start a fresh PowerShell session, or
- Use full path: `"$env:ProgramFiles\GitHub CLI\gh.exe"` or `"$env:LOCALAPPDATA\GitHubCLI\gh.exe"`
- Check with: `where.exe gh` or iterate known install paths

### Source files destroyed by git rm
If the agent accidentally runs `git rm -rf .` before copying to temp:
1. `git checkout $originalBranch` — git will restore all tracked files
2. Any untracked files (e.g. user-renamed `index.html`) will be lost — redo renames manually

### GitHub Pages not building
- Verify `index.html` is at the root of the gh-pages branch: `git ls-tree gh-pages --name-only`
- Check build status: `gh api repos/{owner}/{repo}/pages/builds`
- Common issue: force-push didn't trigger build — push an empty commit to trigger: `git commit --allow-empty -m "trigger build"`

## Error Handling
- If gh CLI not installed: instruct user to install (`winget install GitHub.cli` or `scoop install gh`)
- If gh not authenticated: instruct user to run `gh auth login`
- If push fails (no permission): report the error and suggest checking repo permissions
- If GitHub Pages not enabled: the API call in Step 3 enables it; if it fails, suggest enabling in repo settings
- If `index.html` missing from temp copy: abort before commit, return to original branch

## Usage
When asked to publish, run all git commands in the project root:
```
C:\PROJECTS\LESSON PLAN WRITER 3
```

# Command: Git Backup

## Usage
`/git-backup`

Stages all changes, bumps VERSION, generates a categorised commit message, commits to main, and pushes to origin. All changes are committed — no prompting for individual files.

## Prerequisites
- `gh` CLI authenticated
- Git remote `origin` configured
- Reviews / tests can run via the review step

## Safety
**This command pushes directly to `origin/main`.** The agent must present the commit message to the user for confirmation before pushing. If the user rejects, unstage everything and stop.

## Workflow

### Step 0: Run review (optional)
```powershell
python -m ruff check --fix . ; python -m ruff format .
```

If lint fails, ask the user whether to continue or abort. If tests are available, prompt: "Run tests before committing? (Y/n)"

### Step 1: Check working tree
```powershell
git status
```
If "nothing to commit, working tree clean" — stop.

### Step 2: Stage everything
```powershell
git add -A
```

### Step 3: Show staged diff summary
```powershell
git diff --cached --stat
```

### Step 4: Read and bump VERSION
```powershell
$oldVer = (Get-Content "VERSION").Trim()
$bump = Read-Host "$oldVer — major, minor, or patch? [minor]"
if (-not $bump) { $bump = "minor" }
$parts = $oldVer.Split(".")
switch ($bump) {
    "major" { $newVer = "$([int]$parts[0]+1).0.0" }
    "minor" { $newVer = "$($parts[0]).$([int]$parts[1]+1).0" }
    default { $newVer = "$($parts[0]).$($parts[1]).$([int]$parts[2]+1)" }
}
$newVer | Set-Content "VERSION" -NoNewline
Write-Host "$oldVer → $newVer ($bump)"
```

### Step 5: Build commit message
Categorise changed files from `git diff --cached --name-status` into:
- **Skills/commands** — `.kilo/skills/`, `.kilo/command/`
- **Scripts** — `scripts/`
- **Configuration** — `AGENTS.md`, `pyproject.toml`, `.gitignore`
- **Tests** — `tests/`
- **Templates** — `templates/`
- **Lesson content** — `output/`, `PDF/` (if any)

Subject line: `v{N.m.p} — {brief description}`

### Step 6: Confirm with user
Display the message. Ask `Commit v{ver} with this message? (Y/n)`:
- **Y** or empty — commit via `-F` temp file
- **N** — prompt for custom message; empty = abort

### Step 7: Push
```powershell
git push origin main
```

### Step 8: Report
```powershell
$ver = (Get-Content "VERSION").Trim()
Write-Host "Pushed v$ver to origin/main"
```

## Edge cases
- **Nothing to commit** — stop before staging
- **Review failures** — ask user; they can continue or abort
- **Push rejected** — print error; local commit is preserved
- **Custom message** — user writes their own; empty = abort

## Examples

### Full backup
```
/git-backup
```
Stages, bumps VERSION, generates message, confirms, commits, pushes.

### Review only (planned, not implemented yet)
Run `git status` and `git diff --cached --stat` manually, then abort.

---
name: git-backup
description: Stages all changes, auto-generates a categorised multi-line commit message, commits to main, and pushes to origin. Runs review (lint + tests + quality checks) first.
---

# Skill: Git Backup

## Purpose
Stage all working-tree changes, increment the semantic version from `VERSION` (`v{M}.{m}.{p}`), generate a structured commit message categorised by file type (skills/commands/scripts/lessons), confirm with the user, commit to main, and push to origin.

**Output:** Git commit pushed to `origin/main` with updated `VERSION` file.

## Prerequisites
- `gh` CLI authenticated
- Git remote `origin` configured
- `/review` command available for pre-commit lint/tests

## When to Use

Use this skill when:
- The user asks to commit, back up, or save all current work to git
- The review-only mode is requested (`/git-backup --review`)
- Significant changes have been made across multiple file categories

Do NOT use this skill when:
- Only a small, experimental change needs a quick commit (consider manual `git commit`)
- No changes have been made yet (run `git status` first to verify)

**Trigger:** `/git-backup` command or when the user asks to commit and push changes.


## Workflow

### Step 0: Run review
Invoke `/review` (lint + tests + quality checks against AGENTS.md rules). If review fails, ask the user whether to continue or abort. If they abort, stop.

### Step 1: Check working tree
```powershell
git status
```
If "nothing to commit, working tree clean" — stop here.

### Step 2: Stage everything
```powershell
git add -A
```

### Step 3: Show staged diff summary
```powershell
git diff --cached --stat
```

### Step 4: Derive version and build categorised commit message

**Version bump:** Read `VERSION` from project root, then auto-detect the bump type by scanning staged file paths:
```powershell
$oldVer = (Get-Content "VERSION").Trim()
$changed = git diff --cached --name-only

# Heuristics: core infrastructure changes → major, new content → minor, fixes → patch
$majorPatterns = @('templates/', 'AGENTS.md', '.kilo/skills/', '.kilo/command/', 'scripts/', 'pyproject.toml')
$minorPatterns = @('output/', 'inputs/', 'docs/', 'knowledge-base/')

$hasMajor = ($changed | Where-Object { $_ -match ($majorPatterns -join '|') }).Count -gt 0
$hasMinor = ($changed | Where-Object { $_ -match ($minorPatterns -join '|') }).Count -gt 0

if ($hasMajor -and $hasMinor) {
    # Both core infra AND new content changed → likely a significant release
    $bump = Read-Host "Major, minor, or patch? (auto-detected: major+minor, suggest major) [minor]"
    if (-not $bump) { $bump = "minor" }
} elseif ($hasMajor) {
    $bump = Read-Host "Major, minor, or patch? (auto-detected: major) [major]"
    if (-not $bump) { $bump = "major" }
} elseif ($hasMinor) {
    $bump = Read-Host "Major, minor, or patch? (auto-detected: minor) [minor]"
    if (-not $bump) { $bump = "minor" }
} else {
    $bump = Read-Host "Major, minor, or patch? (auto-detected: patch) [patch]"
    if (-not $bump) { $bump = "patch" }
}

$parts = $oldVer.Split(".")
switch ($bump) {
    "major" { $newVer = "$([int]$parts[0]+1).0.0" }
    "minor" { $newVer = "$($parts[0]).$([int]$parts[1]+1).0" }
    default { $newVer = "$($parts[0]).$($parts[1]).$([int]$parts[2]+1)" }  # patch
}
Write-Host "$oldVer → $newVer ($bump)"
```
Write the new version back to `VERSION`:
```powershell
$newVer | Set-Content "VERSION" -NoNewline
```

**Body categories:** Parse `git diff --cached --name-status` into categories: skills, commands, scripts, lesson content (inputs/output/PDF), plans, and other.

**Subject line format:** `v{M.m.p} — {brief description}` (e.g., `v1.0.1 — Update colors, answer layouts, and templates`)

**Full message structure:**
```
v{M.m.p} — {description}

Skills/commands:
- ...

Configuration:
- ...

Lessons:
- ...

Templates:
- ...

Scripts:
- ...
```

### Step 5: Confirm with user
Display the generated message (with version number in the subject line). Ask `Commit v{N} with this message? (Y/n)`:
- **Y** or empty — commit with the generated message (via `-F` temp file)
- **N** — prompt for custom message; empty = abort

### Step 6: Push
```powershell
git push origin main
```

### Step 7: Report
Read the final version from `VERSION` and show commit status:
```powershell
$ver = (Get-Content "VERSION").Trim()
$ahead = [int](git rev-list --count origin/main..HEAD)
Write-Host "Committed v$ver (${ahead} ahead of origin)"
```

### Step 8: Capture learnings
If the session involved a bug fix, pattern change, or new approach worth remembering, append an entry to the global learnings file at `C:\Users\elwru\.kilo\learnings.md`. Use this format:

```markdown
## YYYY-MM-DD: [lesson-plan-writer] Brief description

**Context:** What was being done
**Fix:** What was done to fix it
**Pattern:** The general principle to apply next time
**Files:** path/to/file.py
```

Ask the user: "Add a learnings entry for this session? (Y/n)" — if Y, prompt for the description and append.


## Reference

- `VERSION` — Project root file storing the current semantic version (`v{M}.{m}.{p}`)
- `AGENTS.md` — Workflow rules and execution gates that the review step validates against
- `.kilo/command/git-backup.md` — Kilo CLI command definition for `/git-backup`

## Scripts

This skill does not ship standalone scripts. It uses standard git commands (`git add`, `git commit`, `git push`) and the `/review` command for pre-commit quality checks. The workflow is implemented directly in the skill steps, not in external scripts.


## Error Handling

| Symptom | Likely cause | Fix |
|---------|-------------|-----|
| Review fails | Lint or test suite failed | Ask user whether to continue or abort |
| Nothing to commit | Working tree is clean | Stop before staging; no action needed |
| Push fails | Remote unreachable or rejected | Error is printed; local commit is preserved |
| Custom message rejected | User entered empty message | Abort the operation |
| Filename too long for git | Large `.epub` files with long metadata filenames | Rename the offending file to a shorter path, or add a gitignore entry for the file type/pattern, then re-run `git add -A` |

## Examples

### Example 1: Full backup

**Request:** "Back up my work"

**Action taken:** Stage all changes, run lint + tests, bump VERSION, generate categorised commit message, present to user for confirmation, commit to main, push.

### Example 2: Review only

**Request:** "Show me what would be committed"

**Action taken:** Run `/git-backup --review` — stages everything, runs quality checks, prints the commit message, then un-stages without committing.

### Example 3: After slides build

**Request:** "Save the slides I just built"

**Action taken:** Stage new slides output + assets, generate commit message categorised under `lessons/slides`, commit, push.


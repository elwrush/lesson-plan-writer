---
name: git-backup
description: Stages all changes, auto-generates a categorised multi-line commit message, commits to main, and pushes to origin. Runs review (lint + tests + quality checks) first.
---

# Skill: Git Backup

## Purpose
Stage all working-tree changes, derive the next version number (`v{N}` from total commit count), generate a structured commit message categorised by file type (skills/commands/scripts/lessons), confirm with the user, commit to main, and push to origin.

## Prerequisites
- `gh` CLI authenticated
- Git remote `origin` configured
- `/review` command available for pre-commit lint/tests

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

**Version number:** Count total commits on main that will exist AFTER this commit:
```powershell
$version = (git rev-list --count HEAD) + 1
```
Format as `v{N}` (e.g., `v101`, `v102`). Every commit gets a unique incrementing version.

**Body categories:** Parse `git diff --cached --name-status` into categories: skills, commands, scripts, lesson content (inputs/output/PDF), plans, and other.

**Subject line format:** `v{N} — {brief description}` (e.g., `v101 — Update colors, answer layouts, and templates`)

**Full message structure:**
```
v{N} — {description}

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
Show the new version number and commit count ahead:
```powershell
$newCount = git rev-list --count HEAD
$ahead = git rev-list --count origin/main..HEAD
Write-Host "Committed v$newCount (${ahead} ahead of origin)"
```

## Edge cases
- **Review fails**: ask user whether to continue or abort
- **Nothing to commit**: stop before staging
- **Push fails**: error is printed; local commit is preserved
- **Custom message rejected**: empty message aborts the operation
- **Filename too long for git**: If `git add -A` fails with "Filename too long" or "unable to index file", identify the offending file and either:
  - Rename it to a shorter path, or
  - Add a gitignore entry for the file type/pattern, then re-run `git add -A`
  - The most common cause is large `.epub` files from archives with very long metadata filenames — these should be gitignored globally via `*.epub`

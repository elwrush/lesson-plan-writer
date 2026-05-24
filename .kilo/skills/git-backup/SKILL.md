---
name: git-backup
description: Stages all changes, auto-generates a categorised multi-line commit message, commits to main, and pushes to origin. Runs review (lint + tests + quality checks) first.
---

# Skill: Git Backup

## Purpose
Stage all working-tree changes, generate a structured commit message categorised by file type (skills/commands/scripts/lessons), confirm with the user, commit to main, and push to origin.

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

### Step 4: Build categorised commit message
Parse `git diff --cached --name-status` into categories: skills, commands, scripts, lesson content (inputs/output/PDF), plans, and other. Build a subject line ("Update (N files)" or "Add/Remove/Update path") and body grouped by category.

### Step 5: Confirm with user
Display the generated message. Ask `Commit with this message? (Y/n)`:
- **Y** or empty — commit with the generated message (via `-F` temp file)
- **N** — prompt for custom message; empty = abort

### Step 6: Push
```powershell
git push origin main
```

### Step 7: Report
```powershell
git rev-list --count origin/main..HEAD
```

## Edge cases
- **Review fails**: ask user whether to continue or abort
- **Nothing to commit**: stop before staging
- **Push fails**: error is printed; local commit is preserved
- **Custom message rejected**: empty message aborts the operation

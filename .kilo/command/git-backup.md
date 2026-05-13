---
description: Stage all changes, show a diff summary, auto-generate a commit message, commit to main, and push to origin. Runs lint first.
---
# Command: Git Backup

## What it does
1. Runs `/lint` (ruff check + format)
2. Shows `git status` overview
3. Stages all changes (`git add -A`)
4. Shows `git diff --cached --stat` summary
5. Auto-generates commit message from changed filenames
6. Asks for confirmation before committing
7. Commits and pushes to `origin main`

## Workflow

### Step 1: Lint
```powershell
python -m ruff check --fix . ; python -m ruff format .
```

### Step 2: Check working tree
```powershell
git status
```

If status shows "nothing to commit, working tree clean" — stop here.

### Step 3: Stage everything
```powershell
git add -A
```

### Step 4: Show staged diff summary
```powershell
$stagedStat = git diff --cached --stat
Write-Host "`n--- STAGED CHANGES ---"
$stagedStat
```

### Step 5: Auto-generate commit message from file list
```powershell
# Get staged files categorized
$added = @()
$modified = @()
$deleted = @()

git diff --cached --name-status | ForEach-Object {
    $parts = $_ -split "`t"
    $status = $parts[0]
    $file = $parts[1]
    if ($file) {
        switch ($status) {
            "A" { $added += $file }
            "M" { $modified += $file }
            "D" { $deleted += $file }
        }
    }
}

$allFiles = @($added) + @($modified)
$count = $allFiles.Count

if ($count -eq 0) {
    if ($deleted.Count -eq 1) {
        $message = "Remove $($deleted[0])"
    } elseif ($deleted.Count -le 4) {
        $message = "Remove $($deleted -join ', ')"
    } else {
        $message = "Remove multiple: $($deleted[0]) and $($deleted.Count - 1) more files"
    }
} elseif ($count -eq 1) {
    if ($added.Count -gt 0 -and $modified.Count -eq 0) {
        $message = "Add $($allFiles[0])"
    } else {
        $message = "Update $($allFiles[0])"
    }
} elseif ($count -le 4) {
    if ($added.Count -eq $count) {
        $message = "Add $($allFiles -join ', ')"
    } else {
        $message = "Update $($allFiles -join ', ')"
    }
} else {
    $message = "Update multiple: $($allFiles[0]) and $($count - 1) more files"
}

Write-Host "`n--- AUTO-GENERATED COMMIT MESSAGE ---"
Write-Host $message
```

### Step 6: Confirm
```powershell
$choice = Read-Host "`nCommit with this message? (Y/n)"
if ($choice -eq '' -or $choice -eq 'y' -or $choice -eq 'Y') {
    git commit -m $message
} else {
    $custom = Read-Host "Enter custom commit message"
    if ($custom -eq '') { Write-Error "Empty message — aborting"; exit 1 }
    git commit -m $custom
}
```

### Step 7: Push
```powershell
git push origin main
```

### Step 8: Report
```powershell
$ahead = git rev-list --count origin/main..HEAD
Write-Host "Backup complete. main is $ahead commit(s) ahead of origin/main."
```

## Edge cases
- **Nothing to commit**: stop before staging
- **Push fails**: error is printed; the local commit is preserved
- **Custom message rejected**: empty message aborts the operation
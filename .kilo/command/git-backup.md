---
description: Stage all changes, show a diff summary, auto-generate a verbose multiline commit message (categorised by skills/commands/scripts/lessons), commit to main, and push to origin. Runs lint first.
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

### Step 5: Auto-generate verbose commit message

Build a structured multiline commit message with a subject line and body sections. The message summarises what changed and why, not just which files.

```powershell
# --- Categorise files by type ---
$skills = @(); $commands = @(); $scripts = @(); $lessons = @(); $plans = @(); $other = @()

git diff --cached --name-status | ForEach-Object {
    $status, $file = $_ -split "`t"
    $label = if ($status -eq 'A') { 'Add' } elseif ($status -eq 'D') { 'Remove' } else { 'Update' }
    if ($file -match '^\.kilo/skills/')    { $skills += "  $label $file" }
    elseif ($file -match '^\.kilo/command/') { $commands += "  $label $file" }
    elseif ($file -match '^scripts/')       { $scripts += "  $label $file" }
    elseif ($file -match '^\.kilo/plans/')  { $plans += "  $label $file" }
    elseif ($file -match '^(inputs|output|PDF)/') { $lessons += "  $label $file" }
    else                                    { $other += "  $label $file" }
}

# --- Build subject line ---
$total = @($skills) + @($commands) + @($scripts) + @($plans) + @($lessons) + @($other)
$count = $total.Count
$subject = if    ($count -eq 0) { "No changes" }
           elseif ($count -eq 1) { $total[0] }
           else                  { "Update ($count files)" }

# --- Build message body ---
$body = @()
if ($skills.Count -gt 0)    { $body += "`nSkills:"; $body += $skills }
if ($commands.Count -gt 0)  { $body += "`nCommands:"; $body += $commands }
if ($scripts.Count -gt 0)   { $body += "`nScripts:"; $body += $scripts }
if ($lessons.Count -gt 0)   { $body += "`nLesson content:"; $body += $lessons }
if ($plans.Count -gt 0)     { $body += "`nPlans:"; $body += $plans }
if ($other.Count -gt 0)     { $body += "`nOther:"; $body += $other }

$message = "$subject`n$($body -join "`n")"

Write-Host "`n--- COMMIT MESSAGE ---"
Write-Host $message
```

### Step 6: Confirm
```powershell
Write-Host "`n$message"
$choice = Read-Host "`nCommit with this message? (Y/n)"
if ($choice -eq '' -or $choice -eq 'y' -or $choice -eq 'Y') {
    $msg = $message -split "`n", 2
    $body = if ($msg.Count -eq 2) { $msg[1] } else { "" }
    Set-Content -Path "$env:TEMP\commit_msg.txt" -Value "$msg[0]`n`n$body"
    git commit -F "$env:TEMP\commit_msg.txt"
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
---
name: skill-name-here
description: One-line summary — what does this skill do? 15–20 words, no more.
---

# Skill: Human-Readable Name

## Purpose

2–3 sentences answering: what problem does this skill solve, and what does the final output look like? The agent reads this to decide if the skill fits the task.

**Output:** path or format of the deliverable (e.g. `output/{subfolder}/index.html`)

## When to Use

Use this skill when:
- Condition 1 — specific task, tool, or file type
- Condition 2 — the user mentions X or asks for Y
- Condition 3 — never use for Z (anti-pattern to avoid)

**Trigger:** `/command-name` command or when the user asks to [one-sentence paraphrase].

**Non-verbose:** (optional) If the skill runs silently, say so here.

## Workflow (N Steps)

---

### Step 1 — Step Name

What the agent does first. Ask questions, read files, gather input.

- Bullet each action
- Keep commands in `inline code`
- Reference scripts by relative path: `python scripts/validate_slides.py`

### Step 2 — Step Name

Continue with numbered steps. Each step should be a single coherent action.

```powershell
# Show real commands the agent can run
pandoc slides.md -t revealjs -s --slide-level=1 -o index.html
```

### Step N — Output

Describe the final deliverable and how to verify it.

---

## Examples

### Example 1: Short description of the scenario

**Request:** "Paraphrase of what the user says"

**Action taken:** 2–3 sentence summary of what the skill does

**Output:** Path or format of the result

### Example 2: Another scenario

**Request:** "..."

**Action taken:** ...

### Example 3: Edge case scenario

**Request:** "..."

**Action taken:** ...

---

## Error Handling

| Symptom | Likely cause | Fix |
|---------|-------------|-----|
| Error message A | Cause X | Solution Y |
| Output is empty | Cause Z | Solution W |

---

## Reference

If the skill has depth material (checklists, configuration reference, API details), store them in `reference/` files and link them here:

- `reference/CHECKLIST.md` — step-by-step verification list
- `reference/CONFIG.md` — configuration options

## Scripts

If the skill ships automation scripts, keep them in `scripts/` (stdlib-only Python, no pip installs):

- `scripts/validate.py` — what it checks
- `scripts/build.py` — what it builds

# Plan: Create Global Repomix Skill

## Objective
Create a global Kilo skill for using repomix to:
1. Grab a codebase from GitHub (clone + pack remote repo)
2. Search/pack the codebase for AI analysis

## Analysis

**Repomix** (`yamadashy/repomix`) is an npm CLI tool that packs an entire repository into a single AI-friendly file (XML, Markdown, JSON, or Plain Text). Key capabilities:

- `repomix --remote <github-url>` — clones and packs any public GitHub repo
- `repomix --stdout` — outputs to stdout for piping
- `repomix --style json` — JSON output for jq searching
- `repomix --token-count-tree` — shows token distribution
- `repomix --include` / `--ignore` — filter files by glob patterns

## Implementation Steps

### Step 1: Add repomix to bash permissions
Add to `C:\Users\elwru\.config\kilo\kilo.jsonc`:
```json
"repomix *": "allow"
```

### Step 2: Create global skill file
Location: `C:\Users\elwru\.kilo\skills\repomix-codebase-search\SKILL.md`

The skill will include:
- **Workflow 1**: Grab a remote repo from GitHub using `repomix --remote <url>`
- **Workflow 2**: Search the packed output using grep/Select-String or JSON+jq
- **Workflow 3**: Get token count tree for a repo

## Deliverable
Global skill file ready to use.
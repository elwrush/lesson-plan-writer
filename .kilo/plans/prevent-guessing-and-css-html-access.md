# Plan: Prevent Agent Guessing and CSS/HTML Access

## Problem

The agent repeatedly violates two core rules:

1. **Guessing Lua/Pandoc syntax instead of researching.** When a visual or structural issue arises, the agent writes Lua filter code or Pandoc attributes from training data rather than searching Context7, Tavily, or the Pandoc documentation. This produces wrong code, wastes tokens on fix cycles, and violates the "pattern-first, not guess-first" rule.

2. **Reading and editing CSS/HTML files.** The agent defaults to reading `slides-pandoc.css` and `shield-block.lua` (to see inline styles) when it doesn't know how to achieve a visual effect. It then writes CSS or HTML-level changes instead of staying at the Pandoc Markdown/Lua filter layer. This is explicitly forbidden: the build pipeline requires `--css` (a shared file), not per-slideshow CSS tweaks.

## Root cause

The existing rules are **permissive suggestions**, not hard blocks:

| Current rule | Why it fails |
|---|---|
| "Search via Tavily or Context7" (AGENTS.md §Research) | The agent treats this as optional. When under pressure to fix something quickly, it skips research and guesses. |
| "No raw HTML / No inline CSS" (What NOT to Do) | These rules only forbid *writing* HTML/CSS, not *reading* them. The agent reads `slides-pandoc.css` to "figure out what class to use" — then writes CSS changes anyway. |
| "Golden Rule: read existing examples before writing" | The agent reads `.css` and `.html` files as "examples", then writes in the same domain. This loophole needs closing: the only "examples" that are allowed are `.md` and `.lua` files. |
| "CSS handles: Styling" (SKILL.md header) | States a fact but doesn't enforce it. No mechanical check prevents CSS edits. |

## What to change

### 1. Hard prohibition on CSS/HTML file access

**Files:** `AGENTS.md`, `SKILL.md`

Add an explicit, unmissable block at the top of the Research section and What NOT to Do:

```
# CSS/HTML FILES ARE FORBIDDEN
- Do NOT read any .css, .html, or .htm file
- Do NOT edit any .css, .html, or .htm file
- slides-pandoc.css is hash-locked — the build fails if it has been modified
- slides-header.html is copy-only — its source is at scripts/slides-header.html
- If a visual problem exists, the fix is ALWAYS in Pandoc Markdown or a Lua filter — NEVER in CSS
```

This replaces the current weak "Do not write raw HTML" with "Do not read or write CSS/HTML at all."

### 2. Research gate before Lua filter edits

**Files:** `AGENTS.md`, `SKILL.md`

Before ANY edit to a `.lua` file (including `shield-block.lua`, `youtube-embed.lua`, etc.):

1. Load the `context7-docs` skill and search for the relevant Pandoc Lua filter API
2. If Context7 is down or doesn't have the answer, fall back to Tavily: `pandoc lua filter <topic>`
3. Cite the search result in the edit rationale

Add this as a numbered checklist in the Workflow Summary and as a blocker in What NOT to Do:

```
- Do not edit any .lua file without first running a Context7 search for the Pandoc Lua filter API function you intend to use
```

### 3. CSS hash-lock (automated enforcement)

**Files:** `scripts/validate_slides.py` (new check), `scripts/slides-pandoc.css.sha256` (new)

Add a SHA256 hash of `slides-pandoc.css` stored in a companion file. The validation script checks this hash before every build. If the CSS has been modified (even whitespace), the build is blocked with a clear message:

```
ERROR: slides-pandoc.css has been modified.
This file is hash-locked. Do NOT edit CSS.
Visual fixes go through Pandoc Markdown attributes or Lua filters.
```

This provides mechanical enforcement independent of agent discipline.

### 4. Visual-issue decision tree (replaces CSS guessing)

**Files:** `SKILL.md` (new Troubleshooting reference)

Add a lookup table mapping common visual problems to Pandoc/Lua solutions, so the agent doesn't default to reading CSS:

| Visual problem | Correct approach | Pandoc Markdown / Lua filter |
|---|---|---|
| Text needs to be yellow | Use `.cta-text` bracketed span | `[text]{.cta-text}` |
| Text needs dark background (image-bg slide) | Use `.shield` fenced div | `::: {.shield} ... :::` |
| Element needs positioning (logo, overlay) | Heading attr → section, Lua Div wrapper | `# {#id style="position:relative"}` + shield-block.lua |
| Text needs to be larger | Use heading level (h1 for slides, ### for sub) | `### heading` |
| Element needs centering | shield-block.lua flexbox (shields) or heading attr | `{data-}` attrs on heading |
| Columns needed | Pandoc pipe table or ???shield stack | `\| col1 \| col2 \|` or three stacked `.shield` divs |

This table should live in the Troubleshooting reference (`reference/TROUBLESHOOTING.md`) and be loaded when visual issues arise. The table's structure forces the agent to stay in Markdown/Lua territory.

### 5. Stale "read CSS" loophole — close it

**Files:** `AGENTS.md`, `SKILL.md`

The Golden Rule says "read existing examples before writing code." The agent exploits this to read `.css` files as "examples" of what to write. Fix:

```
## Golden Rule: Pattern-first, not guess-first

Before writing any Markdown, slide markup, or configuration, read a **Markdown or Lua file** that already does what you need. 
- Slide attributes: check an existing `output/*/slides/slides.md`
- Lua filter patterns: check an existing `scripts/*.lua` file
- Do NOT read .css, .html, or .htm files — these are generated output, not patterns to follow
```

## Implementation order

1. **hash-lock** `scripts/slides-pandoc.css` → create `.sha256` file → add validation check
2. **Update AGENTS.md** §Research and What NOT to Do with hard CSS/HTML prohibition + research gate
3. **Update SKILL.md** §Architecture and What NOT to Do with same prohibitions
4. **Add visual-issue decision table** to `reference/TROUBLESHOOTING.md`
5. **Update Golden Rule** to exclude CSS/HTML from "examples"
6. **Run lint + tests** to verify nothing is broken

# Research Report: Reducing Friction for Complex Reveal.js & Typst Documents

**Date:** 12 June 2026  
**Method:** 5 Tavily searches → deep-dive on 4 key repositories

---

## Executive Summary

Three distinct friction-reduction strategies have emerged in the community:

1. **Runtime validation loops** (Typst MCP server) — agent tests code against compiler before output
2. **Scaffold-then-edit workflows** (revealjs-skill) — generate structure first, fill content incrementally
3. **Design rule enforcement via agent skills** (writing-revealjs-presentations) — strict CSS/typography/fragment rules loaded as skill instructions

All three are complementary, not mutually exclusive, and all three already have partial equivalents in this project. The question is whether the community versions offer enough additional value to adopt.

---

## 1. Typst MCP Server — `johannesbrandenburger/typst-mcp`

**Stars:** 159 | **Forks:** 15 | **License:** MIT | **Language:** Python

### What it provides

| Tool | Function | Equivalent in this project |
|---|---|---|
| `list_docs_chapters()` | List all Typst documentation chapters | `typst-author` skill (100+ doc files) |
| `get_docs_chapter(route)` | Fetch specific doc chapter content | Same as above, but indexed by topic |
| `latex_snippet_to_typst(latex)` | LaTeX → Typst via Pandoc | Not needed (no math) |
| `check_if_snippet_is_valid_typst_syntax(snippet)` | Compile-check Typst code | **`typst_check.py` (built today)** |
| `typst_to_image(snippet)` | Render Typst to PNG | Not needed |

### How it works internally

The server runs `typst compile` against actual Typst CLI. It requires a cloned Typst source repo for documentation generation (`cargo run --package typst-docs`). The documentation is pre-built into a JSON file that the server loads at startup.

### Key insight: The docs tool reads from a pre-built JSON, not live web

The Typst documentation is statically compiled from the Typst source into `main.json` using `cargo run --package typst-docs`. This means the documentation is version-locked to a specific Typst release — if the docs change upstream, the JSON must be regenerated. This is more reliable than web scraping but requires maintenance when Typst updates.

### Kilo MCP integration

The `opencode.json` config format shown in the typst-mcp README is structurally identical to Kilo's MCP config format:

```jsonc
// Kilo: kilo.json or .kilo/kilo.json
{
  "mcp": {
    "typst": {
      "type": "local",
      "command": ["python", "/path/to/typst-mcp/server.py"],
      "enabled": true
    }
  }
}
```

This means the Typst MCP server can be integrated with Kilo with zero code changes — just config.

### Assessment

The `check_if_snippet_is_valid_typst_syntax` tool is functionally equivalent to `typst_check.py`. The documentation tools (`list_docs_chapters` / `get_docs_chapter`) are an MCP-based alternative to the `typst-author` skill. The advantage of MCP over skill docs is that the agent can query docs on-demand (lower token burn than loading all docs upfront) and gets exactly the chapter it needs.

**Value for this project: MEDIUM.** The compile-check is already solved. The docs-as-tools pattern could replace loading the full `typst-author` skill for every session, but the docs are version-locked to the Typst source snapshot at build time and may be stale.

---

## 2. revealjs-skill — `ryanbbrown/revealjs-skill`

**Stars:** 340 | **Forks:** 35 | **License:** MIT

### Architecture: Scaffold-then-edit (not generate-all-at-once)

This is the most significant architectural insight from the research. The skill uses a fundamentally different approach from this project:

| Phase | This project | revealjs-skill |
|---|---|---|
| 1. Plan | Design blueprint (`.kilo/plans/`) | Plan slide structure from user's content |
| 2. Scaffold | Copy `base-slides-template.html` | Run `create-presentation.js --structure 1,1,d,3` |
| 3. Fill | Generate ALL `<section>` elements at once via Write tool | Edit each slide ONE AT A TIME via Edit tool |
| 4. Validate | `lint_slides.py` + `revealjs-validator` + authorial voice + pedagogical intent | `check-overflow.js` (Playwright) + `decktape` screenshots |
| 5. Polish | Manual browser review | Browser text editor (`edit-html.js`) |

### The scaffold-first advantage

```bash
# Generates HTML with placeholder text and guaranteed valid structure
node scripts/create-presentation.js --structure 1,1,1,d,3,d,1 --title "My Presentation"
```

This produces:
```html
<section id="slide-1"><h2>Slide 1 Title</h2><div class="content"><p>Slide 1 content here</p></div></section>
<section id="slide-2"><h2>Slide 2 Title</h2><div class="content"><p>Slide 2 content here</p></div></section>
<section id="slide-3" class="section-divider"><h1>Divider Title</h1></section>
...
```

Then each slide is filled with the Edit tool — small, targeted edits that preserve structure. This eliminates the section-tag mismatch problem entirely (the scaffold guarantees balance).

### Overflow detection via Playwright

```bash
node scripts/check-overflow.js presentation.html
```

Uses Puppeteer (not Playwright — the README lists Puppeteer as dependency) to render each slide and check for content beyond slide boundaries. This catches visual bugs the validator can't.

### Visual review via Decktape screenshots

```bash
npx decktape reveal "presentation.html?export" output.pdf --screenshots --screenshots-directory screenshots/
```

Captures a PNG screenshot of every slide for visual inspection. This is more thorough than manual browser review.

### What it does NOT provide (relevant to this project)

- ❌ No pedagogical slide types (vocabulary, lead-in error, S/V/O annotation, strategy steps)
- ❌ No answer slide structure (`a-row`, `a-q`, `a-ans`, `a-why`)
- ❌ No British Council IPA
- ❌ No audio/TTS integration
- ❌ No timer plugin
- ❌ No fragment→audio trigger (`data-vocab-trigger` + `fragmentshown`)
- ❌ No design principle enforcement beyond visual overflow
- ❌ No mechanism rubric or pedagogical intent annotations

### Assessment

**Value for this project: MODERATE.** The scaffold-first approach is architecturally superior for preventing structural errors, but it cannot handle auto-animate (requires matching `data-id` across slides that must be generated together) or any pedagogical slide type. The overflow detection and screenshot review are real additions you don't have.

The most valuable takeaway is the **scaffold-then-edit pattern** — could be adapted to generate a blueprint-aware scaffold that preserves your pedagogical slide types.

---

## 3. writing-revealjs-presentations — `ZempTime/.dotfiles`

**Platform:** Smithery (supports Kilo Code, Claude Code, Cursor, etc.)

### Core philosophy: Tailwind-first, semantic colors, strict typography

This is a developer conference talk skill. Its rules:

- All styling via Tailwind CSS (`class="text-6xl font-bold text-slate-100"`)
- Strict typography scale with code >= body text (non-negotiable)
- Mandatory speaker notes with timing markers on every slide
- Fragment discipline ("build complexity, not click fatigue")
- Semantic colors (green=good, red=bad, yellow=warning)
- `data-auto-animate` for structural transformations only
- Pre-flight refactoring check (no inline styles, no `.slide1` classes)

### Conflict with this project

| Rule | This project | writing-revealjs-presentations |
|---|---|---|
| Styling | Custom CSS via base template `<style>` block | Tailwind CDN |
| Font sizing | `em` units (1em, 0.9em, 1.2em) | Tailwind `text-*` (px-based) |
| Slide types | 7+ pedagogical patterns | Developer talk patterns |
| Answer slides | `a-row`/`a-q`/`a-ans`/`a-why` classes | Not supported |
| Color palette | `#fff`/`#ffdd00` only (2-color rule) | Tailwind semantic colors (5+ colors) |
| Auto-animate | S/V/O annotations, keyword underlines, error→correction | Box morphing, size changes |
| Fragments | Custom `fragment custom svo-s` with CSS transitions | Standard `fragment fade-in` |
| Speaker notes | Teacher procedure in `<aside class="notes">` | Timing markers + presenter guidance |
| Backgrounds | `data-background-color` + `data-background-image` | `data-background-color` only |

### Assessment

**Value for this project: LOW.** It enforces a Tailwind-first approach that conflicts with your existing CSS infrastructure and pedagogical slide types. The speaker notes discipline (timing markers, 3-5x detail ratio) is philosophically aligned with your existing practice but uses a different format. The "no click fatigue" fragment rule is weaker than your fragment policy (which reserves fragments for answers only, not objectives/summaries/transitions).

---

## 4. Cross-Cutting Patterns — What the Community is Converging On

### Pattern A: Runtime validation (universal)

Both the Typst MCP server and revealjs-skill enforce a **validate-before-presenting** step. The agent doesn't just generate and hope — it runs actual tools (typst compile, Playwright overflow check, Decktape screenshots) to verify correctness. This is the single biggest gap your project still has for Typst (now partially addressed by `typst_check.py`).

### Pattern B: Scaffold-then-edit (reveal.js-specific)

The scaffold-first approach prevents the most common error class: structural HTML corruption (unbalanced tags, misplaced sections). Your current approach (generate all sections at once with Write) is vulnerable to this, mitigated only by post-hoc section-count checks.

### Pattern C: Design rules as skill content (universal)

All three skills embed design rules directly in the skill file. No external config, no separate documentation — the instructions ARE the rules. Your project already does this extensively (AGENTS.md, skill SKILL.md files, design reference docs).

### Pattern D: Platform portability (skill ecosystem)

Smithery lists Kilo Code as a supported platform. Skills written for Claude Code can be adapted to Kilo. The MCP config format is identical between OpenCode and Kilo. This means the community tooling ecosystem is accessible — you don't need to build everything from scratch.

---

## 5. Specific Recommendations (ranked by ROI)

### Already done: `typst_check.py`
Built and tested (11/11). Closes the Typst validation loop gap. Run before presenting Typst output to user.

### High ROI: Scaffold script for pedagogical slide types
Build a `create-pedagogical-slides.py` that generates the HTML skeleton with:
- Correct section count and structure
- Pre-set `data-background-color` per slide type
- Pre-set `data-auto-animate-id` on auto-animate pairs
- Pre-set fragment placements on answer slides
- Guaranteed balanced tags

Then fill content via Edit tool slide-by-slide. This eliminates structural errors at generation time.

### Medium ROI: Overflow detection for reveal.js slides
Adapt the Playwright/Puppeteer approach from revealjs-skill to check your slides for content overflow. Your existing lint_slides.py catches design rule violations but NOT visual overflow. This would catch text running off the bottom of slides.

### Medium ROI: Typst MCP server for documentation-on-demand
Replace the `typst-author` skill (100+ files loaded at session start) with the MCP server's `get_docs_chapter` tool (loads only the chapter needed). Reduces context bloat in Typst-heavy sessions.

### Low ROI: Adopt Tailwind or Marp
These would require rebuilding your CSS infrastructure and conflict with pedagogical slide types. Not recommended.

### No ROI: reveal-js-slides-generator (MCPMarket)
General-purpose developer talk generator. Zero pedagogical awareness. Evaluated and rejected.

---

## 6. What You've Already Solved (recognition)

These are problems the community is still struggling with that you've already addressed:

| Problem | Community status | Your solution |
|---|---|---|
| Auto-animate for language teaching | Most skills ignore it | S/V/O annotations, keyword underlines, error→correction morphs — all documented with HTML patterns |
| Fragment-audio synchronization | GitHub Issue #724 still open | Custom `fragmentshown` handler with `data-vocab-trigger` |
| Answer slide structure | Not addressed by any skill | `a-row`/`a-q`/`a-ans`/`a-why` pattern with per-row fragment |
| British Council IPA | Not addressed by any skill | Phonemic chart reference + Times New Roman IPA rendering |
| Pedagogical intent annotation | Not addressed by any skill | DESIGN MECHANISM annotations with Mechanism Rubric |
| 2-color projection rule (#fff/#ffdd00) | Most skills use 5+ Tailwind colors | Enforced by lint_slides.py |
| Design blueprint before generation | Most skills "plan" but don't blueprint | Phase 0 mandatory pre-write ritual |

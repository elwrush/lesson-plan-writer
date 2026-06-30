# Feature: Consolidated Presentation Defaults Lua Filter

## Feature Summary

Create a single `presentation-defaults.lua` Pandoc Lua filter that replaces four separate filters (`slide-font-size.lua`, `fa-yellow.lua`, `white-reveal.lua`, `vocab-size.lua`). The consolidated filter injects all presentation-level CSS (base font size, yellow highlight colour, white reveal colour, vocab slide enlargement) in one pass.

This is purely a **consolidation** — the visual output must be identical to the current 4-filter setup. No new features.

## User Scenarios

### User Story 1 — Single filter replaces four (P1)
Build command changes from 9 filters to 6. Instead of copying and ordering `slide-font-size.lua`, `fa-yellow.lua`, `white-reveal.lua`, and `vocab-size.lua`, only `presentation-defaults.lua` is needed.

**Why this priority:** Every build command currently needs 9 Lua filters in a specific order. Missing any one silently degrades styling (no error, just wrong colours/sizes).

### User Story 2 — Font and colour rules in one place (P2)
All presentation defaults (base font 48px, vocab +15%, yellow `.highlight`, white `.white-reveal`) are defined in one file. Changing a size or colour requires editing one file, not four.

**Why this priority:** Reduces maintenance surface. A single source of truth for visual defaults.

## Technical Approach

`presentation-defaults.lua` wraps the functionality of all four existing filters into a single `Pandoc` function that:

1. Injects `<style>.reveal { font-size: 48px; } [id^="slide-vocab-"] { font-size: 1.15em; }</style>` (from `slide-font-size.lua` + `vocab-size.lua`)
2. Processes `Span` elements with class `highlight` → `color: #ffd700` (from `fa-yellow.lua`)
3. Injects `<style>.fragment.white-reveal.visible { color: white !important; }</style>` (from `white-reveal.lua`)

Filter order in build command is irrelevant — the single filter handles all presentational CSS.

## Validation Rules

| Module | Check | Rule |
|--------|-------|------|
| Input | Existing filters removed | Build command must NOT include `slide-font-size.lua`, `fa-yellow.lua`, `white-reveal.lua`, or `vocab-size.lua` |
| Output | Base font size | `.reveal { font-size: 48px }` present in generated HTML |
| Output | Vocab slide size | `[id^="slide-vocab-"] { font-size: 1.15em }` present in generated HTML |
| Output | Yellow highlight | `.highlight` spans render with `color: #ffd700` |
| Output | White reveal | `.fragment.white-reveal.visible` renders with `color: white !important` |
| Output | Visual parity | All existing slides render identically to pre-consolidation build |
| Count | Filter count | Build command has exactly 6 filters (down from 9) |

## Test Coverage

`tests/test_presentation_defaults_lua.py`:
- Build a known-good slides.md with `presentation-defaults.lua` only (no other presentational filters)
- Compile to HTML
- Verify CSS injection: base font size, vocab size, yellow `.highlight`, white `.white-reveal`
- Verify no change to slide structure (section IDs, headings, fragments unchanged)

## Acceptance Criteria

| ID | Criterion | Validation Method |
|----|-----------|-------------------|
| AC1 | `presentation-defaults.lua` exists in `scripts/` | File exists |
| AC2 | Single filter replaces 4 old filters | Build with new filter only, verify CSS injected |
| AC3 | Visual output unchanged | Pixel comparison or CSS rule coverage match |
| AC4 | Build command reduced from 9 to 6 filters | `--lua-filter` count in build command |
| AC5 | Old filters removable | No slide depends on old 4 filters for correct rendering |

## Constraints

- Must not modify any existing `.md`, `.css`, `.html`, or other `.lua` files
- Old 4 filters must remain in `scripts/` (backward compatibility for other projects)
- The filter must work for ALL reveal.js slides, not just this lesson
- CSS hash-lock unchanged (`slides-pandoc.css` not modified)

## Source Files

- `scripts/presentation-defaults.lua` (consolidated filter)

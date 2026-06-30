# Plan: Slide Validation Gate

## Phase 1 — Slide parsing
- Split slides.md by `# ` headings into per-slide dicts
- Track fenced div nesting, speaker notes blocks, line numbers

## Phase 2 — Checks (blocking: exit 2)
- Speaker notes presence
- Raw HTML detection
- Fenced div balance
- Missing asset files
- YouTube ID format
- Inline CSS (style=)
- Unauthorized .css/.html files
- CSS hash-lock

## Phase 3 — Checks (non-blocking: exit 1)
- Horizontal rule `---` detection

## Phase 4 — Statistics + exit
- Count total/with-notes/with-content/empty slides
- Exit 0 (pass), 1 (warnings), 2 (errors)

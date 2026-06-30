# Plan: Consolidated Presentation Defaults Filter

## Phase 1 — Write presentation-defaults.lua
- Read all 4 existing filters (slide-font-size.lua, fa-yellow.lua, white-reveal.lua, vocab-size.lua)
- Combine CSS injection into a single Pandoc function
- Combine Span processing for `.highlight` into the same filter
- Ensure format check `FORMAT:match('revealjs')` wraps all reveal-specific logic

## Phase 2 — Verify against current output
- Build slides with old 4-filter setup → capture HTML as reference
- Build slides with new single filter (remove old 4)
- Compare CSS injections: base font, vocab size, yellow colour, white colour
- Compare slide structure: section IDs, headings, fragments unchanged

## Phase 3 — Update spec 003
- Reduce filter count from 9 to 6 in the Validation Rules and Constraints
- Remove references to the 4 old filters
- Point to `presentation-defaults.lua` as the single source for visual defaults

## Phase 4 — Remove old filters from slide build
- Update the build command in the reference patterns file
- Remove old 4 filter copy steps from the infrastructure checklist

# Plan: Lesson Plan PDF Pipeline

## Phase 1 — Frontmatter parsing
- `parse_frontmatter()` in build_lesson_pdf.py reads YAML frontmatter
- REQUIRED_META list validates keys present
- SHAPE Literal in src/models.py must include all shapes from lesson-plan-skill doc

## Phase 2 — Template hash-verification
- `.template-lock.json` stores SHA256 of `templates/lesson-plan.typ`
- Template changes caught by hash mismatch

## Phase 3 — Pandoc + Typst invocation
- Pandoc with `lesson-tables.lua` filter converts .md → .typ
- ALL `Para` block types in stage content MUST be captured (not just Time/Aim)
- Typst CLI compiles .typ → .pdf
- Linter verifies output quality

## Phase 4 — Pre-build Markdown structure check
- Blank line before bullet lists: verify every `- ` line after a `Para` has a blank line preceding it
- Stage heading format: `## Stage \d+: .+$`
- Timing sum matches YAML duration

## Phase 5 — Post-build PDF content verification
- Extract PDF text via PyPDF2 or PyMuPDF
- Verify stage names appear in extracted text
- Verify stage aims appear in extracted text
- Verify listed vocabulary words appear (if `**Vocabulary:**` present)
- Cross-platform path resolution: test on both Windows and Linux

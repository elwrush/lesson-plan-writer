# Feature: Slide Validation Gate

## Feature Summary

Pre-build validation for `slides.md` files. `validate_slides.py` scans Pandoc Markdown for common errors before reveal.js HTML generation: missing speaker notes, raw HTML tags, unbalanced fenced divs, broken asset references, invalid YouTube IDs, inline CSS, unauthorized CSS/HTML files, and CSS hash-lock violations. Exits 0 (pass), 1 (warnings), or 2 (blocking errors).

## User Scenarios

### User Story 1 — Block invalid slides before build (P1)
Run `python scripts/validate_slides.py output/subfolder/slides/slides.md` before the pandoc build command. If it exits 2, the build pipeline stops — saving time and preventing broken HTML.

**Why this priority:** Catch errors early, before HTML generation.

### User Story 2 — CSS hash-lock integrity (P1)
If `slides-pandoc.css` has been modified (even whitespace), the validation fails. Visual changes must go through Pandoc Markdown or Lua filters — never CSS.

**Why this priority:** CSS files are hash-locked to prevent agent-driven style changes that bypass the established design system.

### User Story 3 — Ban inline CSS in Markdown (P1)
Any `style=` attribute in `slides.md` triggers a blocking error. All styling must come from `slides-pandoc.css`, Lua filters, or Pandoc Markdown constructs (fenced divs, bracketed spans with classes).

**Why this priority:** Inline CSS circumvents the CSS hash-lock and breaks the separation of content and presentation.

## Technical Approach

`validate_slides.py` parses the Markdown file by `# ` headings, producing a list of slide dicts. Each slide is checked independently: speaker notes presence, raw HTML via regex `<[a-zA-Z/][^>]*>`, fenced div balance via opening/closing `:::` count, asset file existence (audio/background/image references), YouTube ID format validation, inline CSS via `style=` regex, unauthorized `.css`/`.html` files in the slides directory, and SHA256 hash of `slides-pandoc.css` against `.slides-pandoc.css.sha256`.

## Validation Rules

| Check | Rule | Severity |
|-------|------|----------|
| Speaker notes | Every slide (except empty/splash) has `::: notes` | ERROR |
| Raw HTML | No `<tag>` patterns unless Pandoc-generated | ERROR |
| Fenced div balance | Opening `:::` count == closing `:::` count | ERROR |
| Asset files | Referenced audio/bg/image exists on disk | ERROR |
| YouTube IDs | Video IDs match `[a-zA-Z0-9_-]{8,15}` | ERROR |
| Inline CSS | No `style=` in Markdown | ERROR |
| Unauthorized assets | No `.css`/`.html` except allowlist | ERROR |
| CSS hash | SHA256 matches `.slides-pandoc.css.sha256` | ERROR |
| `---` rules | No bare `---` that create unintended slide breaks | WARNING |

## Test Coverage

`tests/test_validate_slides.py`: 432-line test suite covering known-good slides, known-bad patterns, edge cases (empty slides, unbalanced divs, missing files, raw HTML, inline CSS, YouTube IDs, CSS hash, unauthorized files, horizontal rules).

## Acceptance Criteria

| ID | Criterion | Validation Method |
|----|-----------|-------------------|
| AC1 | Valid slides.md exits 0 | Shell exit code |
| AC2 | Missing speaker notes exits 2 | Exit code check |
| AC3 | Raw HTML exits 2 | Exit code check |
| AC4 | `style=` inline CSS exits 2 | Exit code check |
| AC5 | Unbalanced fenced divs exits 2 | Exit code check |
| AC6 | CSS file modification produces hash error | pytest with modified hash |

## Constraints

- Only checks Markdown structure, not pedagogical content
- CSS hash file (`.slides-pandoc.css.sha256`) must exist alongside CSS file
- Pattern matching is regex-based, not semantic (no AST parsing)

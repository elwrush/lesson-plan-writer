# Markdown → Pandoc → Typst → PDF: Research Findings

Date: 2026-06-15
Research method: 10+ Tavily searches across 60+ results including GitHub repos, blog posts, Typst docs, HN threads, Pandoc issues

## The Standard Pipeline

The established approach used by thousands is:

```bash
pandoc input.md -o output.pdf --pdf-engine=typst --template=custom-template.typ
```

**Sources:**
- `andyburri/pandoc-typst-template` — complete pipeline, 300+ stars
- `alexmodrono/typst-pandoc` — book publishing pipeline
- `neilzone.co.uk` — custom logo template blog post
- `slhck.info` — "Typst with Pandoc: A Modern Alternative" (Oct 2025)
- `bobek.cz` — "Beautiful two-column PDFs with Markdown, Pandoc and Typst"

## How Pandoc's Typst Writer Handles Lists

From the [Typst list docs](https://typst.app/docs/reference/model/list):

> In markup mode, the value of [`tight`] is determined based on whether items are separated with a blank line. If items directly follow each other, this is set to `true`; if items are separated by a blank line, this is set to `false`.

**Empirically verified**: Pandoc converts compact Markdown lists (no blank lines between items) to compact Typst lists with `\n` separators only. No `\n\n` blank lines appear. The body content (`$body$`) processes through Pandoc's Markdown parser → AST → Typst writer correctly.

## What Works and What Doesn't

### ✅ Works: Stages in Markdown body

```markdown
---
metadata: values
---

## Stage 1: Name

**Time:** 5 min | **Interaction:** T-Ss

- Bullet item one
- Bullet item two
- No blank lines between bullets above
```

Pandoc converts this to tight Typst lists in `$body$`. Lists are compact. This is the proven pattern from every existing template.

### ❌ Problematic: Stages in YAML frontmatter with `$for(stages)$`

```yaml
stages:
  - procedure: |
      - Item one
      - Item two
```

Multi-line YAML block scalars (`|` or `|-`) when substituted as `$stages.procedure$` in a Typst content block `[...]` cause inconsistent indentation. On Windows, Pandoc's template engine produces `\r\r\n` line endings (doubled CR from native CRLF normalization), which Typst interprets as blank lines between list items.

**Verdict**: Avoid `$for(stages)$` with multi-line variable substitution for procedure text. Use `$body$` instead.

## Recommended Architecture

### Template (`lesson-plan.typ`)

- Page setup (margins, font, leading)
- Masthead with logos (from YAML variables)
- Metadata table (teacher, date, class, etc. — from YAML variables)
- `$body$` for all lesson content (stages, procedures, aims — written as Markdown)
- Appendices (answer key, transcript) appended by Python build script after Pandoc conversion

### Markdown Input (`lesson.md`)

- YAML frontmatter for metadata (topic, teacher, date, class, materials, aims)
- Markdown body for all stage content
- Each stage as `## Stage N: Name` heading
- Time, interaction, aim as bold-marked metadata within each stage
- Bullet lists for procedures (no blank lines between items)

### Build Script (`build_lesson_pdf.py`)

- Reads `.md` file
- Validates Markdown structure (headings exist, time totals match)
- Runs Pandoc: `--to=typst --template=lesson-plan.typ --eol=lf`
- Appends answer key `.typ` and transcript `.typ` as appendices
- Runs `typst compile` to produce PDF
- Lints output PDF (page count, expected text, no mojibake)

## Templates to Reference

| Repository | URL | Notes |
|---|---|---|
| andyburri/pandoc-typst-template | github.com/andyburri/pandoc-typst-template | Full shell script pipeline |
| alexmodrono/typst-pandoc | github.com/alexmodrono/typst-pandoc | Book publishing, multi-chapter |
| iandol/dotpandoc | github.com/iandol/dotpandoc | Lua filters + templates, comprehensive |
| neilzone blog | neilzone.co.uk/2025/01/... | Logo template, simple and clean |
| slhck blog | slhck.info/software/2025/10/... | Tutorial-style, has migration guide |

## Key Lessons

1. **Don't fight Pandoc's template system.** Multi-line YAML block scalars in template variables don't work reliably inside Typst content blocks. Use `$body$` instead.

2. **Lists in `$body$` are correct.** Pandoc's Typst writer produces tight lists for compact Markdown. The issue was exclusively with YAML variable substitution, not with body content.

3. **The `--eol=lf` flag** helps with line ending consistency on Windows.

4. **Existing templates exist — use them as reference.** The `andyburri` and `iandol` repositories are the most complete.

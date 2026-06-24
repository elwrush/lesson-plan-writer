# Fix Handout Attachment — Lesson Plan PDF

**Source file:** `output/M3-LESSON02-DRAMA/lesson.md`  
**Pipeline:** `Markdown → Pandoc 3.10 → Typst → PDF`  
**Date:** 24 June, 2026  
**Research:** Context7 API lookups for Pandoc Lua filter (see §Research Citations)

---

## Research Citations (Context7-verified APIs)

All Lua filter code below is backed by Context7 lookups against `/websites/pandoc`:

| API | Verified behavior | Source |
|-----|------------------|--------|
| `pandoc.write(pandoc.Pandoc{tbl}, 'typst')` | Returns string; Pandoc 3.10 wraps tables in `#figure(align(center)[#table(…)], kind: table)` | Diagnostic smoke test + Context7 `pandoc.write` docs |
| `tbl.colspecs:map(fn)` | Returns new List; callback receives `{align, width}` ColSpec pair; `width` is a number (page-width fraction, 0=auto) | Context7 "Remove Table Column Widths" snippet |
| `TableBody.body` | Field contains `List of Rows`; NOT `.rows` | Context7 "Table Components" / TableBody docs |
| `TableHead.rows` / `TableFoot.rows` | Header and footer accessors | Context7 "Table Components" / Row docs |
| `pandoc.RawBlock('typst', str)` | Injects raw Typst into output | Context7 "Raw Content with Attributes" snippet |
| `pandoc.utils.stringify(inlines)` | Converts inline list to plain string | Pandoc Lua filter docs (stdlib) |

---

## Diagnostic Findings

### Pandoc 3.10 Typst writer table output

A diagnostic smoke test (pipe table → `pandoc -t typst`) reveals:

```typst
#figure(
  align(center)[#table(
    columns: (31.43%, 40%, 28.57%),
    align: (left,left,left,),
    table.header([Character], [Voice notes], [Key line],),
    table.hline(),
    [#strong[Cherry]], [Thoughtful, questioning...], ["He looked at me."],
    [#strong[Marcia]], [Playful, warm, loyal.], ["We're not so different after all."],
  )]
  , kind: table
  )
```

**Three critical observations:**

1. **`#figure(…, kind: table)` wrapper is new in Pandoc 3.x.** Before 3.6, tables were wrapped in plain `#align(center)[#table(…)]`. Now they are `#figure(align(center)[#table(…)], kind: table)`. The `kind: table` makes Typst treat it as a **floating figure** — the table can drift to the next page, separating from its heading.

2. **`table-align.lua` correctly replaces `align(center)` → `align(left)`** — the gsub matches the substring within `#figure(align(center)[…], kind: table)`. The filter works. But the `#figure()` wrapper still introduces float behavior.

3. **Pandoc 3.10 already calculates content-aware column widths** — `columns: (31.43%, 40%, 28.57%)` reflects actual content lengths. Users may still perceive short-name columns as too wide because their content doesn't fill the allocated percentage.

---

## Problem Analysis and Fix Strategy

### Problem 1: Table center-aligned under Word Count Target

**Root cause:** Despite `table-align.lua` working correctly, the `#figure()` wrapper's `align(center)` parameter AND Typst's figure float behavior combine to center the table on whatever page it lands on.

**Fix:** The new `table-content-fit.lua` filter will **strip the `#figure()` wrapper entirely**, replacing it with plain `#align(left)[#table(…)]`. This eliminates floating and forces left alignment unconditionally. We use a surgical regex on the `pandoc.write()` output:

```lua
-- Replace: #figure(\n  align(...)[#table(\n    ...\n  )]\n  , kind: table\n  )
-- With:    #align(left)[#table(\n    ...\n  )]
```

### Problem 2: Page break between Teacher Demo Model header and table

**Root cause:** The `#figure(kind: table)` wrapper makes the table a floating element in Typst. Typst's figure placement algorithm may push the table to the next page if it doesn't fit after the heading, while the heading stays on the current page. Additionally, there is no `#block(breakable: false)` keeping them together.

**Fix:** Two-pronged:
1. **Stripping `#figure()` wrapper** (same as Problem 1 fix) — removes floating behavior, so table stays in document flow
2. **New Lua filter `header-table-keeper.lua`** — detects any heading directly followed by a small table (≤8 rows) and wraps both in `#block(breakable: false, […)` to prevent Typst from splitting them across pages

### Problem 3: "Hypothesis" too advanced for B2

**Root cause:** Content — the word appears 5 times in the handout.

**Fix:** Replace in `lesson.md`:
- `**Hypothesis prompt:** When [character] tells this story, they will focus on ____ and the tone will be ____.`
- → `**Before you write — focus question:** What matters most to your character in this scene? What mood will their version have?  
  Focus: _______________  
  Tone: _______________`

### Problem 4: Table column widths not content-aware enough

**Root cause:** Pandoc 3.10's percentage calculation is proportional to total character count. For tables with extreme asymmetry (e.g., `Character` column = 6 chars, `Voice notes` column = 200 chars), the short column still gets ~3% which can look too wide because short text doesn't fill it, or too narrow because the header "Character" is 9 chars.

**Fix:** The `table-content-fit.lua` filter recalculates column widths using a capped-proportional algorithm:
- Measure each column's max text length (split multi-line cells, take the longest line)
- Calculate proportions
- Apply a **minimum 12%** floor so short columns don't collapse below header text
- Convert to `fr` units (cleaner than percentage strings)
- Write into the Typst `columns:` spec

### Problem 5: Walls of text

**Root cause:** Content — Scene arc descriptions and intro paragraphs are monolithic blocks.

**Fix:** Break into bulleted lists and shorter paragraphs in `lesson.md`.

---

## Implementation Plan

### Workstream 1: New Lua filter — `table-content-fit.lua`

**Purpose:** Single filter that handles left-alignment AND content-aware column widths. Replaces `table-align.lua` in the pipeline.

**File:** `C:\PROJECTS\LESSON-PLAN-WRITER-3\scripts\table-content-fit.lua`

**Algorithm (Context7-verified):**
1. Collect cell content from `tbl.head.rows`, `tbl.bodies[*].body` (Context7: `TableBody.body` is `List of Rows`), `tbl.foot.rows`
2. Measure max line length per column via `pandoc.utils.stringify(inlines)` (Context7: stdlib)
3. Calculate capped-proportional widths with 12% minimum floor
4. Set widths via `tbl.colspecs:map()` (Context7: ColSpec = `{align, width}` pair)
5. Call `pandoc.write(pandoc.Pandoc{tbl}, 'typst')` (Context7: returns string)
6. Extract `#table(...)` from `#figure()` wrapper via **balanced-parenthesis counting** (no regex — reliable with nested parens)
7. Wrap in `#align(left)[...]`
8. Fallback: if extraction fails, apply proven `align(center)` → `align(left)` gsub
9. Return as `pandoc.RawBlock('typst', ...)` (Context7: verified)

```lua
-- table-content-fit.lua
-- Left-alignment + content-aware column widths for Typst PDF output.
-- Replaces table-align.lua. Handles Pandoc 3.10's #figure(kind: table) wrapper.
-- All API calls verified against Context7 /websites/pandoc.

if FORMAT:match('typst') then

  -- Measure max line width in a list of inline content (Context7: pandoc.utils.stringify)
  local function measure_cell(inlines)
    local text = pandoc.utils.stringify(inlines)
    local longest = 0
    for line in text:gmatch("[^\n]+") do
      longest = math.max(longest, #line)
    end
    return math.max(longest, 1)
  end

  function Table(tbl)
    -- Context7: #colspecs = number of columns
    local num_cols = #tbl.colspecs

    -- Collect cell content per column
    local col_texts = {}
    for i = 1, num_cols do
      col_texts[i] = {}
    end

    -- Header (Context7: TableHead.rows, Row.cells)
    if tbl.head and tbl.head.rows then
      for _, row in ipairs(tbl.head.rows) do
        for i, cell in ipairs(row.cells) do
          if i <= num_cols then
            table.insert(col_texts[i], cell.contents)
          end
        end
      end
    end

    -- Bodies (Context7: TableBody.body = List of Rows)
    for _, body_section in ipairs(tbl.bodies) do
      for _, row in ipairs(body_section.body) do
        for i, cell in ipairs(row.cells) do
          if i <= num_cols then
            table.insert(col_texts[i], cell.contents)
          end
        end
      end
    end

    -- Foot (Context7: TableFoot.rows)
    if tbl.foot and tbl.foot.rows then
      for _, row in ipairs(tbl.foot.rows) do
        for i, cell in ipairs(row.cells) do
          if i <= num_cols then
            table.insert(col_texts[i], cell.contents)
          end
        end
      end
    end

    -- Calculate per-column max character width
    local char_widths = {}
    local total_chars = 0
    for i = 1, num_cols do
      local max_w = 0
      for _, contents in ipairs(col_texts[i]) do
        max_w = math.max(max_w, measure_cell(contents))
      end
      char_widths[i] = max_w
      total_chars = total_chars + max_w
    end

    -- Calculate fractions with 12% minimum floor (prevents collapse of narrow columns)
    local MIN_FR = 0.12
    local fractions = {}
    local fr_total = 0
    for i = 1, num_cols do
      local raw = char_widths[i] / math.max(total_chars, 1)
      fractions[i] = math.max(raw, MIN_FR)
      fr_total = fr_total + fractions[i]
    end

    -- Normalize to sum to 1.0 (page-width fractions)
    for i = 1, num_cols do
      fractions[i] = fractions[i] / fr_total
    end

    -- Context7: Set widths in AST via colspecs:map()
    -- ColSpec = {align, width} where width is a page-width fraction (number)
    local idx = 0
    tbl.colspecs = tbl.colspecs:map(function(colspec)
      idx = idx + 1
      local align = colspec[1]
      local width = fractions[idx]
      return {align, width}
    end)

    -- Context7: Convert modified table to Typst string
    -- Pandoc's Typst writer now uses our custom widths in the columns: spec
    local typst = pandoc.write(pandoc.Pandoc{tbl}, 'typst')

    -- Extract #table(...) from Pandoc 3.10's #figure(align(center)[#table(...)], kind: table) wrapper
    -- Uses balanced-parenthesis counting — reliable with nested parens, no regex fragility
    local table_start = typst:find('#table%(', 1, true)
    if table_start then
      local depth = 0
      local table_end = table_start
      for j = table_start, #typst do
        local c = typst:sub(j, j)
        if c == '(' then
          depth = depth + 1
        elseif c == ')' then
          depth = depth - 1
          if depth == 0 then
            table_end = j
            break
          end
        end
      end
      -- Wrap extracted #table(...) in left-aligned block
      local table_body = typst:sub(table_start, table_end)
      typst = '#align(left)[' .. table_body .. ']'
    else
      -- Fallback: #table not found — fix alignment in whatever output we got
      typst = typst:gsub('align%(center%)', 'align(left)')
    end

    -- Context7: Return as raw Typst block (pandoc.RawBlock format = 'typst')
    return pandoc.RawBlock('typst', typst)
  end
end
```

**Pipeline integration:** In `build_lesson_pdf.py` line 195, replace:
```python
"--lua-filter", "scripts/table-align.lua",
```
with:
```python
"--lua-filter", "scripts/table-content-fit.lua",
```

---

### Workstream 2: Modified Lua filter — `pagebreak.lua`

**Purpose:** Detect headings followed by small tables and wrap them in `#block(breakable: false)` to prevent page-break separation.

**File:** `C:\PROJECTS\LESSON-PLAN-WRITER-3\scripts\pagebreak.lua`

**Modification:** Add header+table keeper logic to the existing `Pandoc(doc)` function. Uses a numeric `while` loop to look ahead at adjacent blocks. No `goto` — avoids any possibility of unsupported syntax in Pandoc's embedded Lua.

```lua
-- pagebreak.lua — modified to keep headers + small tables together
-- All API calls verified against Context7 /websites/pandoc

if FORMAT:match('typst') then

  -- Context7: Count rows via tbl.head.rows (TableHead), body.body (TableBody), tbl.foot.rows
  local function count_table_rows(tbl)
    local n = 0
    if tbl.head and tbl.head.rows then
      n = n + #tbl.head.rows
    end
    for _, body_section in ipairs(tbl.bodies) do
      n = n + #body_section.body  -- Context7: TableBody.body = List of Rows
    end
    if tbl.foot and tbl.foot.rows then
      n = n + #tbl.foot.rows
    end
    return n
  end

  function Pandoc(doc)
    local new_blocks = {}
    local i = 1
    while i <= #doc.blocks do
      local blk = doc.blocks[i]
      local consumed = false  -- set true when we wrap multiple blocks into one

      -- ── Detect heading + short-intro + small-table pattern ──
      if blk.t == 'Header' then
        local group = {blk}
        local next_idx = i + 1

        -- Optional: consume a short introductory paragraph (< 250 chars)
        if next_idx <= #doc.blocks and doc.blocks[next_idx].t == 'Para' then
          local para_text = pandoc.utils.stringify(doc.blocks[next_idx].content)
          if #para_text < 250 then
            table.insert(group, doc.blocks[next_idx])
            next_idx = next_idx + 1
          end
        end

        -- Check if next block is a small table (≤ 8 rows)
        if next_idx <= #doc.blocks and doc.blocks[next_idx].t == 'Table' then
          local tbl = doc.blocks[next_idx]
          if count_table_rows(tbl) <= 8 then
            table.insert(group, doc.blocks[next_idx])
            next_idx = next_idx + 1

            -- Context7: pandoc.write() to Typst, then wrap in unbreakable block
            local inner_typst = pandoc.write(pandoc.Pandoc(group), 'typst')
            table.insert(new_blocks,
              pandoc.RawBlock('typst',
                '#block(breakable: false, [\n' .. inner_typst .. '\n])'))
            i = next_idx
            consumed = true
          end
        end
      end

      if not consumed then
        -- ── Existing pagebreak logic (unchanged) ──
        -- Add pagebreak before "## Appendix" heading
        if blk.t == 'Header' and blk.level == 2 then
          local text = ''
          for _, inline in ipairs(blk.content) do
            if inline.t == 'Str' then text = text .. inline.text end
            if inline.t == 'Space' then text = text .. ' ' end
          end
          if text:match('^Appendix') then
            table.insert(new_blocks, pandoc.RawBlock('typst', '#pagebreak()'))
          end
        end

        -- Replace horizontal rules with page breaks
        if blk.t == 'HorizontalRule' then
          table.insert(new_blocks, pandoc.RawBlock('typst', '#pagebreak()'))
        else
          table.insert(new_blocks, blk)
        end

        i = i + 1
      end
    end
    doc.blocks = new_blocks
    return doc
  end
end
```

---

### Workstream 3: Content edits to `lesson.md`

#### 3a. Replace "Hypothesis" (Problem 3)

Search for all 5 instances of:
```
**Hypothesis prompt:** When [character] tells this story, they will focus on ____ and the tone will be ____.
```

Replace each with:
```
**Before you write — focus question:**
What matters most to your character in this scene? What mood will their version of the story have?

Focus: _______________
Tone: _______________
```

**Affected sections:** Group 1 (line 182), Group 2 (line 206), Group 3 (line 230), Group 4 (line 254), Group 5 (line 278)

#### 3b. Break walls of text (Problem 5)

**Scene arc sections** — break single-line descriptions into sub-bullets:

Before (Group 1 example):
```
- **Opening:** Dally storms in, furious. He's embarrassed — Cherry humiliated him in front of everyone. He expects sympathy. He doesn't get it.
- **Middle:** Tim Shepard doesn't back down. He challenges Dally's reaction. Johnny quietly says something that surprises everyone — he defends Cherry. Dally turns on him.
- **Resolution:** Someone has to give. Dally either walks away or stays silent. Johnny proves he's no longer afraid. The power dynamic shifts.
```

After:
```
- **Opening** — Dally storms in, furious and embarrassed.
  - Cherry humiliated him in front of everyone.
  - He expects sympathy from the gang. He doesn't get it.
- **Middle** — The confrontation.
  - Tim Shepard doesn't back down. He challenges Dally's reaction.
  - Johnny quietly defends Cherry — and surprises everyone.
  - Dally turns on Johnny. The tension sharpens.
- **Resolution** — Someone has to give.
  - Dally walks away or stays silent.
  - Johnny proves he is no longer afraid.
  - The power dynamic has shifted.
```

Apply the same sub-bullet pattern to all 5 Group scene arcs.

**Scene Structure Guide intro paragraph** — break into bullets:
```
Every scene needs three parts. Use this shape -- but write your own words.
```
→ Add a bulleted checklist:
```
Every scene needs three parts. Use this shape:

- **Opening** — set the mood. A character reveals how they feel.
- **Middle** — conflict builds. Characters clash or reveal something unexpected.
- **Resolution** — something shifts. The characters are not the same as when the scene started.

Write your own words — don't copy the demo.
```

**Word Count Target trailing paragraph** — leave as-is (it's one short sentence).

---

### Workstream 4: Pipeline updates

#### 4a. Edit `build_lesson_pdf.py`

Line 195 — change filter reference:
```python
# Before:
"--lua-filter", "scripts/table-align.lua",

# After:
"--lua-filter", "scripts/table-content-fit.lua",
```

#### 4b. Copy filters to skill directory

```powershell
Copy-Item -LiteralPath "scripts\table-content-fit.lua" -Destination ".kilo\skills\build-excellent-lesson-plans\scripts\table-content-fit.lua"
Copy-Item -LiteralPath "scripts\pagebreak.lua" -Destination ".kilo\skills\build-excellent-lesson-plans\scripts\pagebreak.lua" -Force
```

---

### Workstream 5: Validate and rebuild

```powershell
# 1. LuaLS static type check on both filters
lua-language-server --check="scripts/table-content-fit.lua" --config=".luarc.json"
lua-language-server --check="scripts/pagebreak.lua" --config=".luarc.json"

# 2. Red-green TDD on table-content-fit.lua (per write-a-lua skill)
pandoc "$env:TEMP\kilo\diagnostic-table.md" -t typst --lua-filter="scripts/table-content-fit.lua"

# 3. Full build
$env:PYTHONUTF8=1; python scripts/build_lesson_pdf.py output/M3-LESSON02-DRAMA/lesson.md

# 4. PDF lint
python scripts/linter_pdf_content.py PDF/M3-LESSON02-DRAMA/062326-scene-creation-the-outsiders-from-another-perspective-lesson-plan.pdf

# 5. Open the PDF for visual inspection
```

---

## Execution Order

| Step | Workstream | Description | Estimated time |
|------|-----------|-------------|----------------|
| 1 | 3a | Replace "Hypothesis" in lesson.md | 5 min |
| 2 | 3b | Break walls of text in lesson.md | 10 min |
| 3 | 1 | Write `table-content-fit.lua` (new filter) | 20 min |
| 4 | 2 | Modify `pagebreak.lua` (add header+table keeper) | 10 min |
| 5 | 4a | Update `build_lesson_pdf.py` | 2 min |
| 6 | 5 | LuaLS validate both filters | 3 min |
| 7 | 5 | Red-green TDD on table-content-fit.lua | 5 min |
| 8 | 5 | Full build + lint | 5 min |
| **Total** | | | ~60 min |

---

## Risk Register

| Risk | Likelihood | Mitigation |
|------|-----------|------------|
| Balanced-parenthesis counting fails on malformed Typst output from Pandoc | Very Low | Fallback: `gsub('align%(center%)', 'align(left)')` applied if `#table(` not found. Pandoc emits well-formed output. |
| `tbl.colspecs:map()` callback index tracking (closure `idx`) misaligns with actual column count | Low | `idx` resets per call; `fractions` array built from same `num_cols`. Invariant: `idx == num_cols` at loop end. |
| Stripping `#figure()` wrapper breaks tables that genuinely need floating (e.g., multi-page tables) | Medium | Unwrapping from `#figure()` removes float behavior — tables stay in document flow. Large tables (≥20 rows) will naturally paginate. Typst's `#block(breakable: false)` from `pagebreak.lua` only wraps small (≤8 row) tables. |
| Content edits break Markdown syntax (mismatched bold/italics) | Low | Run through Pandoc as dry-run before full build |
| `pandoc.write()` on each Table triggers full Typst writer re-invocation — slow for documents with many tables | Low | This document has ~10 tables total. Overhead is < 100ms per table. |

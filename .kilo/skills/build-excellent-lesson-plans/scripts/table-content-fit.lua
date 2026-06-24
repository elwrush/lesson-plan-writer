-- table-content-fit.lua
-- Left-alignment + content-aware column widths for Typst PDF output.
-- Replaces table-align.lua. Handles Pandoc 3.10's #figure(kind: table) wrapper.
-- All API calls verified against Context7 /websites/pandoc.

if FORMAT:match('typst') then

  local function measure_cell(inlines)
    local text = pandoc.utils.stringify(inlines)
    local longest = 0
    for line in text:gmatch("[^\n]+") do
      longest = math.max(longest, #line)
    end
    return math.max(longest, 1)
  end

  function Table(tbl)
    local num_cols = #tbl.colspecs

    local col_texts = {}
    for i = 1, num_cols do
      col_texts[i] = {}
    end

    if tbl.head and tbl.head.rows then
      for _, row in ipairs(tbl.head.rows) do
        for i, cell in ipairs(row.cells) do
          if i <= num_cols then
            table.insert(col_texts[i], cell.contents)
          end
        end
      end
    end

    for _, body_section in ipairs(tbl.bodies) do
      for _, row in ipairs(body_section.body) do
        for i, cell in ipairs(row.cells) do
          if i <= num_cols then
            table.insert(col_texts[i], cell.contents)
          end
        end
      end
    end

    if tbl.foot and tbl.foot.rows then
      for _, row in ipairs(tbl.foot.rows) do
        for i, cell in ipairs(row.cells) do
          if i <= num_cols then
            table.insert(col_texts[i], cell.contents)
          end
        end
      end
    end

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

    local MIN_FR = 0.15
    local fractions = {}
    local fr_total = 0
    for i = 1, num_cols do
      local raw = char_widths[i] / math.max(total_chars, 1)
      fractions[i] = math.max(raw, MIN_FR)
      fr_total = fr_total + fractions[i]
    end

    for i = 1, num_cols do
      fractions[i] = fractions[i] / fr_total
    end

    local idx = 0
    tbl.colspecs = tbl.colspecs:map(function(colspec)
      idx = idx + 1
      local align = colspec[1]
      local width = fractions[idx]
      return {align, width}
    end)

    local typst = pandoc.write(pandoc.Pandoc{tbl}, 'typst')

    local table_start = typst:find('#table(', 1, true)
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
      local table_body = typst:sub(table_start, table_end)
      table_body = table_body:gsub('table.header%([^)]*%)', function(header_call)
        return header_call:gsub('(%b[])', function(cell_content)
          return 'table.cell(fill: luma(230))' .. cell_content
        end)
      end)
      typst = '#align(left)[' .. table_body .. ']'
    else
      typst = typst:gsub('align%(center%)', 'align(left)')
    end

    return pandoc.RawBlock('typst', typst)
  end
end

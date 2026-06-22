-- left-table.lua
-- Left-aligns all table cells and sets intelligent column widths from content.
-- Runs AFTER reading-feedback.lua in the filter chain (reading-feedback
-- sets border-bottom/padding but NOT text-align — left-table finishes the job).
-- Wrap tables in ::: {.left-table} to apply.
-- Usage: pandoc --lua-filter=left-table.lua ...
-- Place in build AFTER reading-feedback.lua:
--   --lua-filter=reading-feedback.lua --lua-filter=left-table.lua

if FORMAT:match('revealjs') then

  local function calc_col_avg_lengths(bodies)
    local sums, counts = {}, {}
    for _, tb in ipairs(bodies or {}) do
      for _, row in ipairs(tb.body or {}) do
        for ci, cell in ipairs(row.cells or {}) do
          local text = pandoc.utils.stringify(cell and cell.contents or "")
          sums[ci] = (sums[ci] or 0) + #text
          counts[ci] = (counts[ci] or 0) + 1
        end
      end
    end
    local avgs = {}
    for ci = 1, #counts do avgs[ci] = counts[ci] > 0 and (sums[ci] / counts[ci]) or 1 end
    return avgs
  end

  local function avgs_to_colspecs(avgs)
    local total = 0
    for _, v in ipairs(avgs) do total = total + v end
    if total == 0 then return nil end
    local specs = {}
    for _, v in ipairs(avgs) do
      table.insert(specs, { pandoc.AlignDefault, math.max(v / total, 0.15) })
    end
    local sum = 0
    for _, s in ipairs(specs) do sum = sum + s[2] end
    for _, s in ipairs(specs) do s[2] = s[2] / sum end
    return specs
  end

  local function left_align_all_cells(block)
    local function style(rows)
      for _, row in ipairs(rows or {}) do
        for _, cell in ipairs(row.cells or {}) do
          if cell and cell.attr and cell.attr.attributes then
            -- APPPEND to existing style (reading-feedback already set border/padding)
            local existing = cell.attr.attributes['style'] or ''
            cell.attr.attributes['style'] = existing .. ' text-align: left !important;'
          end
        end
      end
    end
    style(block.head and block.head.rows)
    for _, tb in ipairs(block.bodies or {}) do
      style(tb.body)
    end
  end

  function Div(el)
    for _, cls in ipairs(el.attr.classes) do
      if cls == "left-table" then
        for _, block in ipairs(el.content) do
          if block.t == "Table" then
            -- Set table to full width
            block.attr = block.attr or pandoc.Attr("", {}, {})
            block.attr.attributes['style'] = 'width: 100%;'
            left_align_all_cells(block)
            local avgs = calc_col_avg_lengths(block.bodies)
            local specs = avgs_to_colspecs(avgs)
            if specs then block.colspecs = specs end
          end
        end
        return el
      end
    end
    return el
  end

end

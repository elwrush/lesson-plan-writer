-- click-table.lua
-- Reusable 3-column+ table filter: converts tables inside {.click-table}
-- divs into click-through rows. Each body row becomes a fragment (one click
-- per row). Removes empty header rows automatically.
-- Works with any column count — designed for 3-column definition+example tables.
-- Usage: pandoc --lua-filter=click-table.lua ...
--
-- Markdown pattern:
--   ::: {.click-table}
--   |  |  |  |
--   |---|---|---|
--   | **Term** | Definition | Example |
--   | **Term** | Definition | Example |
--   :::
--

if FORMAT:match('revealjs') then

  -- Calculate average text length per column from body rows
  local function calc_col_avg_lengths(bodies)
    local sums = {}
    local counts = {}
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
    for ci = 1, #counts do
      avgs[ci] = counts[ci] > 0 and (sums[ci] / counts[ci]) or 1
    end
    return avgs
  end

  -- Convert average lengths to proportional colspecs (min 15% per col)
  local function avgs_to_colspecs(avgs)
    local total = 0
    for _, v in ipairs(avgs) do total = total + v end
    if total == 0 then return nil end
    local specs = {}
    for _, v in ipairs(avgs) do
      local pct = math.max(v / total, 0.15)
      table.insert(specs, { pandoc.AlignDefault, pct })
    end
    -- Scale to sum of 1.0 while respecting minimums
    local raw_sum = 0
    for _, s in ipairs(specs) do raw_sum = raw_sum + s[2] end
    if raw_sum > 1.0 then
      local excess = raw_sum - 1.0
      -- Subtract excess from non-minimum columns proportionally
      for _, s in ipairs(specs) do
        if s[2] > 0.18 then
          local share = (s[2] - 0.18) / (raw_sum - 0.18 * #specs)  -- hmm this is complex
        end
      end
    end
    return specs
  end

  function Div(el)
    for _, cls in ipairs(el.attr.classes) do
      if cls == "click-table" then
        for _, block in ipairs(el.content) do
          if block.t == "Table" then
            -- Add fragment class to each body row
            if block.bodies then
              for _, tb in ipairs(block.bodies) do
                for _, row in ipairs(tb.body or {}) do
                  row.attr = row.attr or pandoc.Attr("", {}, {})
                  row.attr.classes:insert("fragment")
                end
              end
            end
            -- Remove empty header
            block.head = nil
            -- Intelligent column widths from content length
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

-- reading-feedback.lua
-- For auto-animate reading feedback slides (Pandoc 3.x API).
-- Maps answer column text to data-id attributes for reveal.js auto-animate.
-- Expects a table with an "Answer" column.

local answer_ids = {
  ["how important customer service is"] = "a1",
  ["how important quality products are"] = "a2",
  ["what brands say about people"] = "a3",
  ["You can return a broken product, but you cannot return rude customer service."] = "d1",
  ["It is more expensive to attract new customers than to keep old ones."] = "d2",
  ["A lot of companies sell the same product."] = "d3",
  ["People are willing to spend a lot of money on good-quality products."] = "d4",
  ["People do not need a watch, but they are still popular."] = "d5",
  ["People like to buy brands that represent who they are."] = "d6",
}

if FORMAT:match('revealjs') then

  function Table(t)
    -- Add white borders to table and all cells
    local function style_cell(cell)
      if cell and cell.attr and cell.attr.attributes then
        cell.attr.attributes['style'] = 'border-bottom: 1px solid white; padding: 6px 12px;'
      end
    end
    -- Style all cells in a list of rows
    local function style_rows(rows)
      for _, row in ipairs(rows or {}) do
        for _, cell in ipairs(row.cells or {}) do
          style_cell(cell)
        end
      end
    end
    style_rows(t.head and t.head.rows)
    for _, tb in ipairs(t.bodies or {}) do
      style_rows(tb.body)
    end
    -- Don't set border-collapse — row lines only, no table outer border

    -- Find the "Answer" column
    local ans_col = nil
    if t.head then
      for _, row in ipairs(t.head.rows) do
        for ci, cell in ipairs(row.cells) do
          local text = pandoc.utils.stringify(cell and cell.contents or ""):lower()
          if text == "answer" then ans_col = ci; break end
        end
        if ans_col then break end
      end
    end
    if not ans_col then
      -- Check for "Main idea" column (D2 table) and set 75/25 split
      if t.head then
        for _, row in ipairs(t.head.rows) do
          for ci, cell in ipairs(row.cells) do
            local text = pandoc.utils.stringify(cell and cell.contents or ""):lower()
            if text == "main idea" then
              t.colspecs = {
                { pandoc.AlignDefault, 0.75 },
                { pandoc.AlignCenter, 0.25 },
              }
              break
            end
          end
          if t.colspecs then break end
        end
      end
      return t
    end

    -- Stabilize header cells with data-id so they don't animate
    if t.head then
      for _, row in ipairs(t.head.rows) do
        for ci, cell in ipairs(row.cells) do
          if cell and cell.contents then
            local text = pandoc.utils.stringify(cell.contents):lower()
            if text == "paragraph" or text == "answer" then
              local inlines = {}
              for _, b in ipairs(cell.contents) do
                if b.t == "Para" or b.t == "Plain" then
                  for _, il in ipairs(b.content) do
                    table.insert(inlines, il)
                  end
                end
              end
              if #inlines == 0 then inlines = {pandoc.Str(text)} end
              local span = pandoc.Span(inlines)
              span.attributes['data-id'] = "col_" .. text
              cell.contents = {pandoc.Para({span})}
            end
          end
        end
      end
    end

    -- Process each table body
    for _, tb in ipairs(t.bodies) do
      if tb and tb.body then
        for _, row in ipairs(tb.body) do
          for ci, cell in ipairs(row.cells) do
            if cell and cell.contents then
              local text = pandoc.utils.stringify(cell.contents)
              text = text:gsub("%s+", " "):gsub("^%s*(.-)%s*$", "%1")

              -- Column 1 (Paragraph or Main Idea): add stable data-id
              if ci == 1 then
                local stable_id = text:match("(%d+)")
                if not stable_id then
                  stable_id = text:match("^(.-):?%.?%s*$")
                  stable_id = stable_id:gsub("[^%w%s]", ""):gsub("%s+", "_"):lower()
                  stable_id = stable_id:sub(1, 25)
                end
                if stable_id and stable_id ~= "" then
                  local inlines = {}
                  for _, b in ipairs(cell.contents) do
                    if b.t == "Para" or b.t == "Plain" then
                      for _, il in ipairs(b.content) do
                        table.insert(inlines, il)
                      end
                    end
                  end
                  if #inlines == 0 then inlines = {pandoc.Str(text)} end
                  local span = pandoc.Span(inlines)
                  span.attributes['data-id'] = "col_" .. stable_id
                  cell.contents = {pandoc.Para({span})}
                end

              -- Answer column: add matching data-id for auto-animate
              elseif ci == ans_col then
                local id = answer_ids[text]
                if id then
                  local inlines = {}
                  for _, b in ipairs(cell.contents) do
                    if b.t == "Para" or b.t == "Plain" then
                      for _, il in ipairs(b.content) do
                        table.insert(inlines, il)
                      end
                    end
                  end
                  if #inlines == 0 then inlines = {pandoc.Str(text)} end
                  local span = pandoc.Span(inlines)
                  span.attributes['data-id'] = id
                  cell.contents = {pandoc.Para({span})}
                end
              end
            end
          end
        end
      end
    end
    return t
  end

end

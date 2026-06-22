-- split-list.lua
-- Transforms 2-column tables inside a {.split-list} div:
--   First column → 15% width, centered, vertically middle-aligned
--   Second column → 85% width, left-aligned
-- Designed for FA icon lists and numbered lists on differentiation slides.
-- Usage: pandoc --lua-filter=split-list.lua ...
-- Reuse: wrap any 2-column grid/pipe table in ::: {.split-list} to apply.

if FORMAT:match('revealjs') then

  function Div(el)
    for _, cls in ipairs(el.attr.classes) do
      if cls == "split-list" then
        for _, block in ipairs(el.content) do
          if block.t == "Table" then
            -- Set column widths
            block.colspecs = {
              { pandoc.AlignCenter, 0.15 },
              { pandoc.AlignDefault, 0.85 },
            }
            -- Vertical-align first column cells to middle
            local function style_cells(rows)
              for _, row in ipairs(rows or {}) do
                for ci, cell in ipairs(row.cells or {}) do
                  if ci == 1 then
                    cell.attr = cell.attr or pandoc.Attr("", {}, {})
                    cell.attr.attributes['style'] = (cell.attr.attributes['style'] or '') .. ' text-align: center; vertical-align: middle;'
                  end
                end
              end
            end
            style_cells(block.head and block.head.rows)
            for _, tb in ipairs(block.bodies or {}) do
              style_cells(tb.body)
            end
          end
        end
        return el
      end
    end
    return el
  end

end

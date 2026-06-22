-- speaking-grading-sheet.lua

local function cell_text(cell)
  if cell and cell.content then
    return pandoc.utils.stringify(cell.content)
  end
  return pandoc.utils.stringify(cell or "")
end

local function table_to_typst(el)
  local rows = {}
  local cr = "luma(220)"

  -- Header row
  local hr = el.head and el.head.rows
  if not hr and el.head then
    hr = el.head[1]
  end
  if hr and #hr > 0 then
    local hdr = {}
    local cells = hr[1].cells or hr[1]
    for _, cell in ipairs(cells) do
      table.insert(hdr, "table.cell(fill: " .. cr .. ")[*" .. cell_text(cell) .. "*]")
    end
    if #hdr > 0 then
      table.insert(rows, "  " .. table.concat(hdr, ",\n  "))
    end
  end

  -- Body rows
  if el.bodies and #el.bodies > 0 then
    local b = el.bodies[1]
    local br = b.rows or b[1] or b[2] or b[3] or b[4] or b.body or {}
    -- Try to find rows by checking which field is a list of tables with 'cells' field
    for _, v in ipairs(b) do
      if type(v) == "table" and #v > 0 and v[1] and type(v[1]) == "table" and (v[1].cells or v[1][1]) then
        br = v
        break
      end
    end
    for i, row in ipairs(br) do
      local cells = row.cells or row
      local has_fill = (i == 2 or i == 4)
      local rcells = {}
      for j, cell in ipairs(cells) do
        local txt = cell_text(cell)
        if j == 1 then
          if has_fill then
            table.insert(rcells, "table.cell(fill: " .. cr .. ", align: center + horizon)[*" .. txt .. "*]")
          else
            table.insert(rcells, "table.cell(align: center + horizon)[*" .. txt .. "*]")
          end
        else
          if has_fill then
            table.insert(rcells, "table.cell(fill: " .. cr .. ")[" .. txt .. "]")
          else
            table.insert(rcells, "[" .. txt .. "]")
          end
        end
      end
      if #rcells > 0 then
        table.insert(rows, "  " .. table.concat(rcells, ",\n  "))
      end
    end
  end

  return [[#table(
  columns: (auto, 1fr, 1fr, 1fr, 1fr),
  align: (left + top, left + top, left + top, left + top, left + top),
  stroke: 0.5pt + black,
  inset: 5pt,
]] .. table.concat(rows, ",\n") .. "\n)"
end

function Header(el)
  if el.level == 1 then
    local txt = pandoc.utils.stringify(el)
    return {
      pandoc.RawBlock("typst", "#v(0.5em)"),
      pandoc.RawBlock("typst", "#align(center)[*" .. txt .. "*]"),
      pandoc.RawBlock("typst", "#v(0.5em)"),
    }
  end
end

function Table(el)
  return pandoc.RawBlock("typst", table_to_typst(el))
end

function Div(el)
  if el.classes:includes("observations") then
    return {
      pandoc.RawBlock("typst", "#v(1em)"),
      pandoc.RawBlock("typst", [[#block(
  width: 100%,
  height: 1fr,
  stroke: 0.5pt + black,
  inset: 8pt,
)[
  #text(size: 14pt, weight: "bold")[Special Observations]
]
]]),
    }
  end
  if el.classes:includes("score") then
    return pandoc.RawBlock("typst", [[#table(
  columns: (6em, 6em),
  stroke: 0.5pt + black,
  inset: 10pt,
  align: center,
  table.cell(fill: luma(220))[*SCORE*],
  table.cell(fill: white)[],
)
]])
  end
  return nil
end

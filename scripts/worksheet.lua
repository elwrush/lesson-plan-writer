local function escape_typst(s)
  s = s:gsub("\\", "\\\\")
  s = s:gsub('"', '\\"')
  return s
end

local function render_checkboxes()
  local cb = '#box(stroke: 1.5pt + black, width: 0.9em, height: 0.9em)'
  return cb .. ' Correct  '
      .. '#h(3em)'
      .. cb .. ' Half correct  '
      .. '#h(3em)'
      .. cb .. ' Wrong'
end

function Div(el)
  if el.classes:find("cefr-box") then
    local content = pandoc.utils.stringify(el.content)
    content = escape_typst(content)
    return pandoc.RawBlock("typst", "#block(stroke: 2pt + black, width: 55%, grid(\n  columns: (auto, 1fr),\n  align: (left + horizon, left + horizon),\n  block(inset: (x: 12pt, y: 14pt), text(18pt, weight: \"bold\")[" .. content .. "]),\n  block(inset: (x: 12pt, y: 14pt))[]\n))")
  end
  if el.classes:find("question") then
    local content = pandoc.utils.stringify(el.content)
    content = escape_typst(content)
    local lines = "#line(length: 100%, stroke: 0.5pt + black)\n#v(1.2em)\n#line(length: 100%, stroke: 0.5pt + black)"
    local checkboxes = render_checkboxes()
    local spacer = "#v(1.5em)"
    return pandoc.RawBlock("typst", content .. "\n\n" .. spacer .. "\n" .. lines .. "\n\n" .. checkboxes .. "\n\n#v(2em)")
  end
  return nil
end

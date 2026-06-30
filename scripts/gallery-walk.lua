local function escape_typst(s)
  s = s:gsub("\\", "\\\\")
  s = s:gsub('"', '\\"')
  return s
end

function Div(el)
  if el.classes:find("answer-box") then
    local content = pandoc.utils.stringify(el.content)
    content = escape_typst(content)
    return pandoc.RawBlock("typst", "#block(stroke: 1.5pt + black, inset: 12pt, width: 100%, text(11pt)[\n" .. content .. "\n])")
  end
  if el.classes:find("cefr-box") then
    local content = pandoc.utils.stringify(el.content)
    content = escape_typst(content)
    return pandoc.RawBlock("typst", "#block(stroke: 1.5pt + black, inset: 8pt, width: 100%, text(12pt)[\n" .. content .. " #line(length: 60%, stroke: 0.5pt + black)\n])")
  end
  return nil
end

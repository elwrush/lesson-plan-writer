-- ruled-paper.lua
-- Generates ruled writing paper with Mathayom header + student demographics.
-- Normal mode (default): header + demographics + ruled lines (2 pages)
-- Blank mode (blank: true in YAML): ruled lines only, full page (1 page)

local function make_typ(class, sid, name, blank)
  if blank then
    -- Blank mode: ruled lines only, full page, no header/demographics
    return [[#set text(font: "Roboto", size: 14pt)
#set par(leading: 0.65em, spacing: 0.3em)
#show: doc => {
  set page(paper: "a4", margin: (x: 0.75in, top: 0.75in, bottom: 0.75in))
  doc
}

#let ls = 24pt

#block(height: 1fr, layout(size => {
  let n = int(size.height / ls)
  for i in range(n) {
    v(ls / 2)
    line(length: 100%, stroke: 0.4pt + black)
    v(ls / 2)
  }
}))]]
  end

  -- Normal mode: header + demographics + ruled lines (2 pages)
  local t = [[#set text(font: "Roboto", size: 14pt)
#set par(leading: 0.65em, spacing: 0.3em)
#show: doc => {
  set page(paper: "a4", margin: (x: 0.75in, top: 0.75in, bottom: 0.75in))
  doc
}

#let ls = 24pt

// Masthead — matches lesson-plan.typ layout
#block(
  stroke: (bottom: 0.5pt + black),
  inset: (bottom: 6pt, top: 12pt),
  grid(
    columns: (1fr, 1fr, 1fr),
    align: (left + horizon, center + horizon, right + horizon),
    image("/templates/cambridge.png", height: 1.8cm),
    align(center, text(size: 14pt, weight: "bold")[C\u{00b7}E\u{00b7}L Mathayom]),
    image("/templates/Image_20260324_141022.png", height: 1.35cm),
  ),
)
#v(0.3em)

// Student demographics
#align(center, text(size: 14pt)[
  *CLASS:* __CLASS__ #h(4em) *ID:* __ID__ #h(4em) *NAME:* __NAME__
])
#v(2.5em)

// Fill remaining page with ruled lines
#block(height: 1fr, layout(size => {
  let n = int(size.height / ls)
  for i in range(n) {
    v(ls / 2)
    line(length: 100%, stroke: 0.4pt + black)
    v(ls / 2)
  }
}))

// Page 2: ruled lines only (no header, no demographics)
#pagebreak()
#block(height: 1fr, layout(size => {
  let n = int(size.height / ls)
  for i in range(n) {
    v(ls / 2)
    line(length: 100%, stroke: 0.4pt + black)
    v(ls / 2)
  }
}))]]
  t = t:gsub("__CLASS__", class)
  t = t:gsub("__ID__", sid)
  t = t:gsub("__NAME__", name)
  return t
end

function Pandoc(doc)
  local function mv(key)
    local v = doc.meta[key]
    if v == nil then return "" end
    return pandoc.utils.stringify(v)
  end
  local blank = mv("blank") == "true"
  local cls  = mv("class")
  local sid  = mv("student_id")
  local name = mv("name")
  if cls == "" then cls = "-" end
  if sid == "" then sid = "-" end
  if name == "" then name = "-" end
  local typ = make_typ(cls, sid, name, blank)
  return pandoc.Pandoc({pandoc.RawBlock("typst", typ)}, doc.meta)
end

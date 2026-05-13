#set text(
  font: "Roboto",
  size: 11pt
)
#set page(
  paper: "a4",
  margin: 2cm,
)

#let writing-lines(spacing: 12mm) = {
  layout(size => {
    let line-tile = tiling(
      size: (size.width, spacing),
      place(bottom, line(length: size.width, stroke: 0.5pt + black))
    )
    rect(
      width: 100%,
      height: 100%,
      fill: line-tile,
      stroke: none,
    )
  })
}

#block(
  stroke: (bottom: 0.5pt + black),
  inset: (bottom: 6pt),
  grid(
    columns: (1fr, 2fr, 1fr),
    align: (left + horizon, center + horizon, right + horizon),
    image("../../templates/ACT.png", height: 1.2cm),
    text(size: 16pt, weight: "bold")[Mathayom Program],
    image("../../templates/1135082720.png", height: 1.6cm),
  )
)
#v(24pt)
#grid(
  columns: (auto, auto, 50%),
  rows: (auto, auto),
  row-gutter: 24pt,
  column-gutter: 4pt,
  align: bottom,
  [*CLASS:*], [], line(length: 100%, stroke: 0.5pt + black),
  [*ID:*],    [], line(length: 100%, stroke: 0.5pt + black),
)
#v(24pt)
#block(width: 100%, height: 1fr, writing-lines())
#pagebreak()
#block(width: 100%, height: 1fr, writing-lines())
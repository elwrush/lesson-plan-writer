#let mathayom-header(
  title: "Mathayom Program",
  logo-left: "ACT.png",
  logo-right: "1135082720.png",
  left-height: 1.2cm,
  right-height: 1.6cm,
  rule: true,
) = {
  let content = grid(
    columns: (1fr, 2fr, 1fr),
    align: (left + horizon, center + horizon, right + horizon),
    image(logo-left, height: left-height),
    text(size: 16pt, weight: "bold")[#title],
    image(logo-right, height: right-height),
  )
  if rule {
    block(
      stroke: (bottom: 0.5pt + black),
      inset: (bottom: 6pt),
      content,
    )
  } else {
    block(inset: (bottom: 6pt), content)
  }
}
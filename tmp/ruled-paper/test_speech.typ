#set text(font: "Roboto", size: 14pt)
#set par(leading: 0.65em, spacing: 0.3em)
#show: doc => {
  set page(paper: "a4", margin: (x: 0.75in, top: 0.75in, bottom: 0.75in))
  doc
}

// Masthead
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
  *CLASS:* M2-4A #h(3em) *ID:* 30321 #h(3em) *NAME:* Alin
])
#v(1cm)

#set par(leading: 0.25em)

#table(
  columns: (6em, 6em),
  stroke: 0.5pt + black,
  inset: 10pt,
  align: center,
  table.cell(fill: luma(220))[*SCORE*],
  table.cell(fill: white)[],
)
#v(0.5em)
#align(center)[*Speaking Grading Sheet — Pronunciation*]
#v(0.5em)
#table(
  columns: (auto, 1fr, 1fr, 1fr, 1fr),
  align: (left + top, left + top, left + top, left + top, left + top),
  stroke: 0.5pt + black,
  inset: 5pt,
  table.cell(fill: luma(220))[*Band*],
  table.cell(fill: luma(220))[*Intonation*],
  table.cell(fill: luma(220))[*Intelligibility*],
  table.cell(fill: luma(220))[*Sentence and Word Stress*],
  table.cell(fill: luma(220))[*Individual Sounds*],
  table.cell(align: center + horizon)[*5*],
  [Intonation is natural and appropriate.],
  [Always clear.],
  [Stress is natural and accurate.],
  [Sounds are clear.],
  table.cell(fill: luma(220), align: center + horizon)[*4*],
  table.cell(fill: luma(220))[Between 5 and 3.],
  table.cell(fill: luma(220))[Between 5 and 3.],
  table.cell(fill: luma(220))[Between 5 and 3.],
  table.cell(fill: luma(220))[Between 5 and 3.],
  table.cell(align: center + horizon)[*3*],
  [Intonation OK in patches.],
  [Mostly clear.],
  [Stress OK in patches.],
  [Some sounds muddled.],
  table.cell(fill: luma(220), align: center + horizon)[*2*],
  table.cell(fill: luma(220))[Between 3 and 1.],
  table.cell(fill: luma(220))[Between 3 and 1.],
  table.cell(fill: luma(220))[Between 3 and 1.],
  table.cell(fill: luma(220))[Between 3 and 1.],
  table.cell(align: center + horizon)[*1*],
  [Intonation defects constant and obvious.],
  [Often unclear or hard to follow.],
  [Stress errors constant and obvious.],
  [Many sounds unclear or distorted.]
)
#v(1em)
#block(
  width: 100%,
  height: 1fr,
  stroke: 0.5pt + black,
  inset: 8pt,
)[
  #text(size: 14pt, weight: "bold")[Special Observations]
]

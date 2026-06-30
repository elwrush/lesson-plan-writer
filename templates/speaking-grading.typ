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
  *CLASS:* $class$ #h(3em) *ID:* $student_id$ #h(3em) *NAME:* $name$
])
#v(1cm)

#set par(leading: 0.25em)

$body$

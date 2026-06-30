$if(topic)$
#set page(paper: "a4", margin: (x: 0.75in, top: 0.75in, bottom: 0.75in))
#set text(font: "Roboto", size: 11pt)
#set par(leading: 0.55em)

// Masthead
#block(
  stroke: (bottom: 0.5pt + black),
  inset: (bottom: 6pt, top: 12pt),
  grid(
    columns: (1fr, 1fr, 1fr),
    align: (left + horizon, center + horizon, right + horizon),
    image("templates/cambridge.png", height: 1.8cm),
    align(center, text(size: 14pt, weight: "bold")[C\u{00b7}E\u{00b7}L Mathayom]),
    image("templates/Image_20260324_141022.png", height: 1.35cm),
  ),
)
#v(0.3em)

= Lesson Plan
*Topic:* $topic$

#table(
  columns: (auto, 1fr, auto, 1fr),
  stroke: 1pt,
  [*Teacher:*], [$teacher$],
  [*Date:*], [$formatted_date$],
  [*Class:*], [$class$],
  [*Duration:*], [$duration$],
  [*CEFR Level:*], [$cefr_level$],
  [*Lesson Shape:*], [$shape$ ($shape_name$)],
$if(materials)$  [*Materials:*], table.cell(colspan: 3)[$for(materials)$- $materials$
$endfor$],
$endif$  [*Slideshow URL:*], table.cell(colspan: 3, fill: luma(220))[$if(slideshow_url)$$slideshow_url$$endif$],
)

$if(main_aim)$#v(0.5em)
= Lesson Aim
#block(stroke: (left: 2pt + black), inset: 8pt)[
  *Main aim:* $main_aim$
  #v(0.3em)
  *Subsidiary aim:* $subsidiary_aim$
]
#v(0.5em)$endif$

$body$
$endif$

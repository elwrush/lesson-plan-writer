#set page(paper: "a4", margin: 2cm)
#set text(font: "Roboto", size: 14pt)

1.  Question text here
#block(inset: (left: 2em))[
  #line(length: 100%, stroke: 0.4pt + black)
  #line(length: 100%, stroke: 0.4pt + black)
]

2.  Another question
#block(inset: (left: 2em))[
  #for i in range(2) {
    v(12pt)
    line(length: 100%, stroke: 0.4pt + black)
    v(12pt)
  }
]

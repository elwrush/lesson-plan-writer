#import "mathayom-header.typ": mathayom-header

#let show-demographics = sys.inputs.at("demographics", default: "false") == "true"
#let doc-title = sys.inputs.at("title", default: "")
#let doc-level = sys.inputs.at("level", default: "")

// Use box(stroke: bottom) for inline blanks — underline(h()) is invisible
#let fl = box(width: 3cm, stroke: (bottom: 0.5pt + black))
#let fls = box(width: 1.2cm, stroke: (bottom: 0.5pt + black))
#let fll = box(width: 4cm, stroke: (bottom: 0.5pt + black))

#set text(font: "Roboto", size: 11pt)
#set par(leading: 0.65em)

#show: doc => {
  set page(paper: "a4", margin: (x: 0.75in, top: 1in, bottom: 0.75in))
  doc
}

#mathayom-header(title: "Mathayom Program")
#v(0.3em)

#if show-demographics [
  #grid(
    columns: (auto, 1fr, auto, 1fr, auto, 1fr),
    column-gutter: 0.5em,
    align: bottom + left,
    [*CLASS:*], [#h(3em, weak: true)],
    [*ID:*], [#h(3em, weak: true)],
    [*NAME:*], [#h(4em, weak: true)],
  )
  #v(0.2em)
  #line(length: 100%, stroke: 0.5pt + luma(180))
  #v(0.5em)
] else [
  #v(0.3em)
]

#if doc-title != "" [
  #align(center, text(size: 14pt, weight: "bold")[#doc-title])
  #v(0.1em)
]

#if doc-level != "" [
  #align(center, text(size: 11pt, fill: luma(80))[Level: #doc-level])
  #v(0.4em)
]

#let body-path = sys.inputs.at("body", default: "none")
#if body-path != "none" [
  #let body-content = read(body-path)
  #eval(body-content, mode: "markup")
]

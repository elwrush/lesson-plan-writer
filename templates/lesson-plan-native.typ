#let data = json(sys.inputs.json_path)

#set text(font: "Roboto", size: 10pt)
#set par(leading: 0.55em)

#show: doc => {
  set page(
    header: context {
      if counter(page).get().first() == 1 {
        block(
          stroke: (bottom: 0.5pt + black),
          inset: (bottom: 6pt, top: 12pt),
          grid(
            columns: (1fr, 1fr, 1fr),
            align: (left + horizon, center + horizon, right + horizon),
            image("Image_20260324_141022.png", height: 1.35cm),
            align(center, text(size: 14pt, weight: "bold")[Lesson Plan]),
            image("1135082720.png", height: 1.8cm),
          ),
        )
      }
    },
    margin: (x: 0.75in, top: 1.25in, bottom: 0.75in),
  )
  doc
}

#let format-date(d) = {
  let months = ("January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December")
  if d.len() == 6 {
    let mm = int(d.slice(0, 2))
    let dd = int(d.slice(2, 4))
    let yy = int(d.slice(4, 6))
    if mm >= 1 and mm <= 12 {
      [#dd #months.at(mm - 1), 20#yy]
    } else { d }
  } else { d }
}

#let humanize-aim(aim) = {
  let result = aim
  let mappings = (
    ("To lead-in", "To activate interest"),
    ("To lead in", "To activate interest"),
    ("To reading for gist", "To understand the general idea of the text"),
    ("To reading for detail and specific information",
      "To identify key facts and details in the text"),
    ("To reading for inference and conclusion",
      "To draw inferences and conclusions from the text"),
    ("To post-reading", "To discuss and apply ideas"),
    ("To wrap-up and reflection",
      "To reflect on what was learned and consolidate understanding"),
    ("To wrap-up", "To reflect on what was learned"),
    ("To reading for", "To practise reading for"),
  )
  for (pat, rep) in mappings {
    if result.starts-with(pat) {
      result = rep + result.slice(pat.len())
      break
    }
  }
  result
}

#let clean-procedure(proc) = {
  let p = proc
  p = p.replace(regex(`,\s*\d+\s*min\.?\s*$`.text), "")
  p = p.replace(regex(`,\s*\d+\s*min\.`.text), ".")
  p = p.replace(regex(`\s*\d+\s*min\.?\s*$`.text), "")
  p.trim()
}

#let teacher = data.at("teacher", default: "")
#let raw-date = data.at("date", default: "")
#let topic = data.at("topic", default: "")
#let duration = data.at("duration", default: "")
#let materials = data.at("materials", default: "")
#let objective = data.at("objective", default: "")
#let slideshow-url = data.at("slideshow_url", default: "")

#let lp = data.at("lesson_plan", default: (:))
#let cefr = lp.at("cefr_level", default: "")
#let class-name = lp.at("class", default: "")
#let shape = lp.at("shape", default: "")
#let shape-name = lp.at("shape_name", default: "")
#let stages = lp.at("stages", default: ())

#let formatted-date = format-date(raw-date)

= Lesson Information

*Topic:* #topic

#table(
  columns: (auto, 1fr, auto, 1fr),
  stroke: 1pt,
  [*Teacher:*], [#teacher],
  [*Date:*], [#formatted-date],
  [*Class:*], [#class-name],
  [*Duration:*], [#duration],
  [*CEFR Level:*], [#cefr],
  [*Lesson Shape:*], [#shape (#shape-name)],
  [*Materials:*], table.cell(colspan: 3)[#materials],
  [*Slideshow URL:*], table.cell(colspan: 3, fill: luma(220))[#slideshow-url],
)

#v(0.5em)

= Lesson Aim

#block(stroke: (left: 2pt + black), inset: 8pt, [#objective])

#v(0.5em)

= Lesson Stages

#{
  table(
    columns: (auto, 1fr, 2fr, auto),
    stroke: 1pt,
    table.header([*Time*], [*Goal*], [*Procedure*], [*Int*]),
    ..stages.map(st => {
      let aim = humanize-aim(st.stage_aim)
      let proc = clean-procedure(st.procedure)
      (
        table.cell(colspan: 4, fill: luma(230))[
          *STAGE #st.stage_number: #upper(st.stage)*
        ],
        [#st.time min],
        [#aim],
        [#proc],
        [#st.interaction],
      )
    }).flatten(),
  )
}

#let t-rel = sys.inputs.at("transcript_rel_path", default: "none")

#if t-rel != "none" [
  #pagebreak()
  = Transcript
  #let t-content = read(t-rel)
  #eval(t-content, mode: "markup")
]

#let ak-rel = sys.inputs.at("answer_key_rel_path", default: "none")

#if ak-rel != "none" [
  #pagebreak()
  = Answer Key
  #let ak-content = read(ak-rel)
  #eval(ak-content, mode: "markup")
]

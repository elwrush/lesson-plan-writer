#set text(font: "Roboto", size: 10pt)
#set par(leading: 0.55em)

#let logo-left = "Image_20260324_141022.png"
#let logo-right = "1135082720.png"

#show: it => {
  set page(
    header: context {
      if counter(page).get().first() == 1 {
        block(
          stroke: (bottom: 0.5pt + black),
          inset: (bottom: 6pt, top: 12pt),
          grid(
            columns: (1fr, 1fr, 1fr),
            align: (left + horizon, center + horizon, right + horizon),
            image(logo-left, height: 1.35cm),
            align(center, text(size: 14pt, weight: "bold")[Lesson Plan]),
            image(logo-right, height: 1.8cm),
          ),
        )
      }
    },
    margin: (x: 0.75in, top: 1.25in, bottom: 0.75in),
  )
  it
}

= Lesson Information

*Topic:* {{ topic }}

#table(
  columns: (auto, 1fr, auto, 1fr),
  stroke: 1pt,
  [*Teacher:*], [{{ teacher }}], [*Date:*], [{{ date }}],
  [*Class:*], [{{ class }}], [*Duration:*], [{{ duration }}],
  [*CEFR Level:*], [{{ cefr_level }}], [*Lesson Shape:*], [{{ shape }} ({{ shape_name }})],
  [*Materials:*], table.cell(colspan: 3)[{{ materials }}],
  [*Slideshow URL:*], table.cell(colspan: 3, fill: luma(220))[{{ slideshow_url }}],
)

#v(0.5em)

= Lesson Aim

#block(
  stroke: (left: 2pt + black),
  inset: 8pt,
  [{{ objective }}]
)

#v(0.5em)

= Lesson Stages

#table(
  columns: (auto, 1fr, 2fr, auto),
  stroke: 1pt,
  table.header([*Time*], [*Goal*], [*Procedure*], [*Int*]),
{% for stage in stages %}
  table.cell(fill: luma(230), colspan: 4)[*STAGE {{ stage.stage_number }}: {{ stage.stage | upper }}*],
  [{{ stage.time }} min], [{{ stage.stage_aim }}], [{{ stage.procedure }}], [{{ stage.interaction }}],
{% endfor %}
)

{% if transcript and transcript != "none" %}
#pagebreak()

= Transcript

{{ transcript }}
{% endif %}

{% if answer_key and answer_key != "none" %}
#pagebreak()

= Answer Key

{{ answer_key }}
{% endif %}
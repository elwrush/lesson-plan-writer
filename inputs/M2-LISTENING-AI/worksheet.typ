#set text(font: "Roboto", size: 11pt)
#set par(leading: 0.65em)

#show: doc => {
  set page(paper: "a4", margin: (x: 0.75in, top: 1in, bottom: 0.75in))
  doc
}

#let writing-lines(spacing: 12mm) = {
  layout(size => {
    let line-tile = tiling(
      size: (size.width, spacing),
      place(bottom, line(length: size.width, stroke: 0.5pt + luma(180)))
    )
    rect(width: 100%, height: 100%, fill: line-tile, stroke: none)
  })
}

#block(
  stroke: (bottom: 0.5pt + black),
  inset: (bottom: 6pt),
  grid(
    columns: (1fr, 2fr, 1fr),
    align: (left + horizon, center + horizon, right + horizon),
    image("/templates/ACT.png", height: 1.2cm),
    text(size: 16pt, weight: "bold")[Mathayom Program],
    image("/templates/cambridge.png", height: 1.6cm),
  )
)
#v(12pt)
#grid(
  columns: (auto, 1fr, auto, 1fr, auto, 1fr),
  column-gutter: 0.5em,
  align: bottom + left,
  [*CLASS:*], [#h(3em, weak: true)],
  [*ID:*], [#h(3em, weak: true)],
  [*NAME:*], [#h(4em, weak: true)],
)
#v(6pt)
#line(length: 100%, stroke: 0.5pt + luma(180))
#v(12pt)

#align(center, text(size: 16pt, weight: "bold")[BTN Classroom - Listening Worksheet])
#align(center, text(size: 14pt)[Diphtheria])
#align(center, text(size: 10pt, fill: luma(80))[4 June 2026])

#v(0.4em)

#block(
  stroke: (left: 3pt + black),
  inset: 8pt,
  [
    *Instructions for Students*

    You will watch the BTN Diphtheria video three times. Each time, focus on a different part of the outline below. Each gap is no more than *three words*. After each part, your teacher will pause the video so you can answer the comprehension questions.

    The transcript is at the end of this worksheet to help you check your answers.
  ]
)

#v(0.6em)

= Part 1: History of Diphtheria

#v(0.3em)

I. History of Diphtheria

#let fl = box(width: 3.5cm, stroke: (bottom: 0.5pt + black))
#let fls = box(width: 1.5cm, stroke: (bottom: 0.5pt + black))

  #h(2em) A. About the disease

    #h(4em) 1. First described by #fl

    #h(4em) 2. Greek name means #fl

  #h(2em) B. Medical breakthrough (1890s)

    #h(4em) 1. Scientists developed #fl therapy

    #h(4em) 2. Won the first Nobel Prize in #fls

  #h(2em) C. Safer vaccine (1923)

    #h(4em) 1. A #fl vaccine was made

#v(0.5em)

*Comprehension Questions — Part 1*

#v(0.2em)

1. Who first described diphtheria, and when?

   #line(length: 100%)
   #line(length: 100%)

2. How did Kitasato and von Behring develop serum therapy?

   #line(length: 100%)
   #line(length: 100%)

3. When was a safer vaccine made, and by whom?

   #line(length: 100%)

#pagebreak()

= Part 2: Vaccines and Outbreak

#v(0.3em)

II. Vaccines and Outbreak in Australia

  #h(2em) A. Vaccination in Australia

    #h(4em) 1. #fls% of 5-year-olds are vaccinated

    #h(4em) 2. A #fl is given at ages 11-13

  #h(2em) B. Current outbreak

    #h(4em) 1. More than #fls cases

    #h(4em) 2. Many cases in #fl communities

#v(0.5em)

*Comprehension Questions — Part 2*

#v(0.2em)

1. What percentage of Australian 5-year-olds are vaccinated against diphtheria?

   #line(length: 100%)

2. What booster option is available for children aged 11-13?

   #line(length: 100%)

3. Where have most of the current cases been found? Who are they affecting?

   #line(length: 100%)
   #line(length: 100%)

#pagebreak()

= Part 3: Government Response

#v(0.3em)

III. Government Response

  #h(2em) A. Communication problems

    #h(4em) 1. Over #fls Aboriginal languages

    #h(4em) 2. Need to fight #fl

  #h(2em) B. Response so far

    #h(4em) 1. Over #fl vaccinated in the NT

    #h(4em) 2. New cases are going #fl

#v(0.5em)

*Comprehension Questions — Part 3*

#v(0.2em)

1. What did Minister McCarthy say about communication in Aboriginal communities?

   #line(length: 100%)
   #line(length: 100%)

2. What did Minister Butler say about the return of diseases like diphtheria?

   #line(length: 100%)
   #line(length: 100%)

3. How has the outbreak changed in the Northern Territory recently?

   #line(length: 100%)
   #line(length: 100%)

#pagebreak()

= Part 4: Discussion

#v(0.2em)

== Discussion Techniques

When sharing your ideas in class, try using these phrases to introduce your own views and to respond to others.

#v(0.2em)

*Introducing your point of view:*

- "I think that ... because ..."
- "In my opinion, ..."
- "It seems to me that ..."
- "One thing I noticed was ..."

#v(0.2em)

*Acknowledging someone else's point of view:*

- "That's a good point. I'd add that ..."
- "I see what you mean. However, ..."
- "I hadn't thought of it that way. I think ..."
- "That's interesting. But what about ...?"

#v(0.4em)

== Think-Pair-Share

#v(0.2em)

*Question 1 (Use the structure below to help you)*

Should vaccination be compulsory for everyone? Use at least one piece of evidence from the video.

#v(0.2em)

*Suggested structure:*

1. Say what you think: "I think (vaccination should / should not) be compulsory because ..."
2. Give evidence from the video: "The video showed that ..."
3. Summarise: "This means that ..."

#v(0.2em)

*Your notes:*

#block(width: 100%, height: 210pt, writing-lines())

#v(0.4em)

*Question 2 (Respond in your own way — no set structure)*

How can governments make sure everyone has access to vaccines, especially in remote communities?

#v(0.2em)

*Your notes:*

#block(width: 100%, height: 210pt, writing-lines())

#pagebreak()

= Transcript

#v(0.3em)

#set text(size: 10pt)
#set par(leading: 0.35em)

https://www.youtube.com/watch?v=tiluGfZ_AtU

#v(0.2em)

*Tatenda:* This was a film that once played in movie theatres, warning people about a dangerous disease that affected thousands of children.

PSA: Stop this needless death!

*Tatenda:* Diphtheria is a contagious disease caused by toxin-producing bacteria, and it can infect the nose, throat, airways or skin. The disease was first described in 4th or 5th century BCE by Greek physician and philosopher Hippocrates, AKA the father of medicine, and, in the 1800s, it was given the name diphtheria, which translates to 'leather' in Greek, because that's kind of what it looked like in the throat.

In the 1890s, there was a breakthrough. Scientists Kitasato Shibasaburo and Emil von Behring developed serum therapy. It involved injecting animals with diphtheria toxins to produce antibodies, which are proteins made by the immune system to fight off disease. They found that by giving those antibodies to other animals and eventually humans, they could stop them from getting sick. The discovery won Emil von Behring the first Nobel Prize in Physiology or Medicine in 1901. In 1923, a French researcher found a way to make a safer diphtheria vaccine, and countries around the world pushed to protect their populations.

And it worked. This graph shows just how much diphtheria cases have fallen since the vaccine became widespread. Today, most Aussies get vaccinated when they're little. In fact, 93% of five-year-olds have had all their recommended doses of the diphtheria vaccine. 11-to-13-year-olds can also get a booster shot through school programs. But there are still gaps. And, recently, we've seen an outbreak of diphtheria.

More than 230 people have tested positive for the disease in parts of Queensland, Western Australia, South Australia and the Northern Territory. Many of those cases are adults living in Indigenous communities, where authorities say there can be barriers to accessing vaccines.

*Malarndirri McCarthy, Minister for Indigenous Australians:* We know that we've got over 100 Aboriginal languages. We need to ensure that the communication is there, not misinformation.

*Mark Butler, Minister for Health and Aged Care:* Some of these diseases, which we thought had been largely consigned to the dustbin of history, like diphtheria, like measles, are showing a re-emergence not just here in Australia, but in a number of other countries where particularly childhood immunisation rates are dropping.

In the last few weeks, more than 10,000 people in the NT alone have had a diphtheria vaccine. Authorities say the outbreak isn't over yet, but the number of new cases has gone down, and hopefully, soon, diphtheria will once again be a thing of the past.

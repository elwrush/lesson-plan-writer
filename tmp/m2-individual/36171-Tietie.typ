#set text(font: "Roboto", size: 14pt)
#set par(leading: 0.65em, spacing: 0.3em)
#show: doc => {
  set page(paper: "a4", margin: (x: 1.5cm, top: 1.5cm, bottom: 1.5cm))
  doc
}

#let ls = 24pt
#let ul(n) = str("_") * n
#let ruled-lines(n) = {
  for i in range(n) {
    if i == 0 { v(1.2em) } else { v(ls / 2) }
    line(length: 100%, stroke: 0.4pt + black)
    v(ls / 2)
  }
}

#block(
  stroke: (bottom: 0.5pt + black),
  inset: (bottom: 4pt),
  grid(
    columns: (1fr, 2fr, 1fr),
    align: (left + horizon, center + horizon, right + horizon),
    image("/templates/ACT.png", height: 1.2cm),
    text(size: 14pt, weight: "bold")[Mathayom Program],
    image("/templates/cambridge.png", height: 1.6cm),
  )
)
#v(8pt)
#align(center, text(size: 14pt)[*CLASS:* M2-5A #h(2em) *ID:* 36171 #h(2em) *NAME:* Tietie])
#v(4pt)
#line(length: 100%, stroke: 0.4pt + black)
#v(10pt)
#align(center, text(size: 18pt, weight: "bold")[BTN Classroom - Listening Worksheet])
#align(center, text(size: 15pt)[Diphtheria])
#align(center, text(size: 12pt)[4 June 2026])
#v(0.3em)

#block(
  stroke: (left: 2pt + black),
  inset: 6pt,
  text(size: 12pt)[
    *Instructions:* You will watch the video three times. Each time, focus on a different part of the outline. Each gap is no more than *three words*.
  ]
)
#v(0.4em)

= Part 1: History of Diphtheria
#v(0.1em)

I. History of Diphtheria \
  #h(1.5em) A. About the disease \
    #h(3em) 1\. First described by #ul(15) \
    #h(3em) 2\. Greek name means #ul(15) \
  #h(1.5em) B. Medical breakthrough (1890s) \
    #h(3em) 1\. Scientists developed #ul(15) therapy \
    #h(3em) 2\. Won the first Nobel Prize in #ul(10) \
  #h(1.5em) C. Safer vaccine (1923) \
    #h(3em) 1\. A #ul(15) vaccine was made

#v(0.6em)
*Comprehension Questions*
#v(0.1em)
The disease was first described 2,400 years ago, but the vaccine took until 1923. What does this timeline tell us about how medical science develops?
#ruled-lines(2)

How did using animals to produce antibodies help scientists develop a treatment before they had a vaccine?
#ruled-lines(2)

= Part 2: Vaccines and Outbreak
#v(0.1em)

II. Vaccines and Outbreak in Australia \
  #h(1.5em) A. Vaccination in Australia \
    #h(3em) 1\. #ul(6)% of 5-year-olds are vaccinated \
    #h(3em) 2\. A #ul(15) is given at ages 11-13 \
  #h(1.5em) B. Current outbreak \
    #h(3em) 1\. More than #ul(6) cases \
    #h(3em) 2\. Many cases in #ul(15) communities

#v(0.6em)
*Comprehension Questions*
#v(0.1em)
93% of 5-year-olds are vaccinated, but there is still an outbreak. Why does this gap in vaccination matter for protecting the whole community?
#ruled-lines(2)

The outbreak is mostly in Indigenous communities. What barriers might make it harder for people in remote areas to access vaccines?
#ruled-lines(2)

= Part 3: Government Response
#v(0.1em)

III. Government Response \
  #h(1.5em) A. Communication problems \
    #h(3em) 1\. Over #ul(6) Aboriginal languages \
    #h(3em) 2\. Need to fight #ul(15) \
  #h(1.5em) B. Response so far \
    #h(3em) 1\. Over #ul(10) vaccinated in the NT \
    #h(3em) 2\. New cases are going #ul(15)

#v(0.6em)
*Comprehension Questions*
#v(0.1em)
Minister McCarthy says the government needs to communicate in over 100 languages. Why is language access important for public health campaigns?
#ruled-lines(2)

Minister Butler says diseases like diphtheria are re-emerging where vaccination rates drop. What does this tell us about the importance of maintaining vaccination programs?
#ruled-lines(2)

#pagebreak()
= Part 4: Discussion
#v(0.1em)

== Discussion Techniques

Use these phrases to introduce your views and respond to others.

*Introducing your point of view:*
- "I think that ... because ..."
- "In my opinion, ..."
- "It seems to me that ..."
- "One thing I noticed was ..."

*Acknowledging someone else's point of view:*
- "That's a good point. I'd add that ..."
- "I see what you mean. However, ..."
- "I hadn't thought of it that way. I think ..."
- "That's interesting. But what about ...?"

#v(0.3em)
== Think-Pair-Share

1\. Should vaccination be compulsory for everyone? Use at least one piece of evidence from the video.

#text(size: 12pt)[*Structure:* Say what you think \ " Give evidence from the video \ " Summarise]

#ruled-lines(4)

2\. How can governments make sure everyone has access to vaccines, especially in remote communities?

#ruled-lines(4)

#pagebreak()
= Transcript

#set text(size: 12pt)
#set par(leading: 0.4em, spacing: 0.8em)

https://www.youtube.com/watch?v=tiluGfZ_AtU

#v(0.1em)

*Tatenda:* This was a film that once played in movie theatres, warning people about a dangerous disease that affected thousands of children.

PSA: Stop this needless death!

*Tatenda:* Diphtheria is a contagious disease caused by toxin-producing bacteria, and it can infect the nose, throat, airways or skin. The disease was first described in 4th or 5th century BCE by Greek physician and philosopher Hippocrates, AKA the father of medicine, and, in the 1800s, it was given the name diphtheria, which translates to 'leather' in Greek, because that's kind of what it looked like in the throat.

In the 1890s, there was a breakthrough. Scientists Kitasato Shibasaburo and Emil von Behring developed serum therapy. It involved injecting animals with diphtheria toxins to produce antibodies, which are proteins made by the immune system to fight off disease. They found that by giving those antibodies to other animals and eventually humans, they could stop them from getting sick. The discovery won Emil von Behring the first Nobel Prize in Physiology or Medicine in 1901. In 1923, a French researcher found a way to make a safer diphtheria vaccine, and countries around the world pushed to protect their populations.

And it worked. This graph shows just how much diphtheria cases have fallen since the vaccine became widespread. Today, most Aussies get vaccinated when they're little. In fact, 93% of five-year-olds have had all their recommended doses of the diphtheria vaccine. 11-to-13-year-olds can also get a booster shot through school programs. But there are still gaps. And, recently, we've seen an outbreak of diphtheria.

More than 230 people have tested positive for the disease in parts of Queensland, Western Australia, South Australia and the Northern Territory. Many of those cases are adults living in Indigenous communities, where authorities say there can be barriers to accessing vaccines.

*Malarndirri McCarthy, Minister for Indigenous Australians:* We know that we've got over 100 Aboriginal languages. We need to ensure that the communication is there, not misinformation.

*Mark Butler, Minister for Health and Aged Care:* Some of these diseases, which we thought had been largely consigned to the dustbin of history, like diphtheria, like measles, are showing a re-emergence not just here in Australia, but in a number of other countries where particularly childhood immunisation rates are dropping.

In the last few weeks, more than 10,000 people in the NT alone have had a diphtheria vaccine. Authorities say the outbreak isn't over yet, but the number of new cases has gone down, and hopefully, soon, diphtheria will once again be a thing of the past.

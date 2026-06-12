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
#align(center, text(size: 14pt)[*CLASS:* M3-5A #h(2em) *ID:* 34933 #h(2em) *NAME:* Grace])
#v(4pt)
#line(length: 100%, stroke: 0.4pt + black)
#v(10pt)
#align(center, text(size: 18pt, weight: "bold")[BTN High - Listening Worksheet])
#align(center, text(size: 15pt)[Gen Z Gender Roles])
#align(center, text(size: 12pt)[Episode 15 - 25 March 2026])
#v(0.3em)

#block(
  stroke: (left: 2pt + black),
  inset: 6pt,
  text(size: 13pt)[
    *Instructions:* Emerging (B1): complete the outline (max 3 words per gap). Established (B2): take your own notes, then answer comprehension questions after each section.
  ]
)
#v(0.4em)

= Part 1: Traditional Gender Roles
#v(0.1em)

I. Traditional Gender Roles in Society \
  #h(1.5em) A. 1950s TV shows portrayed clear gender roles \
    #h(3em) 1\. Women shown as the #ul(15) \
    #h(3em) 2\. Men shown as the #ul(15) \
  #h(1.5em) B. Kings College study \ " 23,000 people from 29 countries \
    #h(3em) 1\. Gen Z holds the #ul(15) traditional beliefs \
    #h(3em) 2\. #ul(3) of Gen Z men believe a wife should obey her husband \
    #h(3em) 3\. #ul(3) of Gen Z men say a husband should have the final word \
  #h(1.5em) C. Attitudes beyond the home \
    #h(3em) 1\. #ul(3) of Gen Z men say enough has been done for gender equality \
    #h(3em) 2\. #ul(3) of Gen Z men feel men are now discriminated against

#v(0.3em)
*Comprehension Questions*
#v(0.1em)
Why might Gen Z hold stronger traditional beliefs than older generations, despite living in a more progressive era?
#ruled-lines(2)

The study found 61% of Gen Z men feel enough has been done for gender equality, while 57% feel men are discriminated against. What does this gap suggest?
#ruled-lines(2)

Why is the response gap between Gen Z men and women on every question, and what does it imply about how they experience society differently?
#ruled-lines(2)

= Part 2: The Role of Social Media
#v(0.1em)

II. The Role of Social Media \
  #h(1.5em) A. Josh Glover \ " facilitator at #ul(15) \
    #h(3em) 1\. His organisation tackles #ul(15) in schools \
    #h(3em) 2\. Social media helps bring back #ul(15) gender norms \
  #h(1.5em) B. How social media algorithms work \
    #h(3em) 1\. Algorithms create #ul(15) where users hear agreeing voices \
    #h(3em) 2\. No one presents #ul(15) opinions \
    #h(3em) 3\. Users only see opinions that get debunked or #ul(15) \
  #h(1.5em) C. The definition problem \
    #h(3em) 1\. Teenage boys\' definition of #ul(15) differs from the intended meaning \
    #h(3em) 2\. This results from algorithms and lack of #ul(15) with people who hold different views

#v(0.3em)
*Comprehension Questions*
#v(0.1em)
Josh says algorithms create echo chambers where "no one presents another opinion." How does this explain why extreme gender stereotypes spread without being challenged?
#ruled-lines(2)

The video suggests manosphere content fills a void of purpose for some young men. What social changes might make young men receptive to these messages?
#ruled-lines(2)

Josh says teenage boys' and feminists' definitions of feminism are "two completely different things." Why does this disconnect matter?
#ruled-lines(2)

= Part 3: Tradwives and Solutions
#v(0.1em)

III. Tradwives and Solutions \
  #h(1.5em) A. "Tradwife" influencers \
    #h(3em) 1\. Glamorise #ul(15) lifestyles \
    #h(3em) 2\. Create content about cooking, cleaning, and #ul(15) roles \
  #h(1.5em) B. Effects on young people \
    #h(3em) 1\. University of Melbourne study of 2,300 adults and 1,100 young people \
    #h(3em) 2\. Support for violence to resist feminism was highest among #ul(15) \
    #h(3em) 3\. Around #ul(3) of boys aged 13-17 agree women lie about domestic and sexual violence \
  #h(1.5em) C. Josh\'s perspective on solutions \
    #h(3em) 1\. Two parts needed: #ul(15) and problem-solving \
    #h(3em) 2\. Need for #ul(15) conversations where people are not judged \
    #h(3em) 3\. Importance of #ul(15) \ " older generations investing in younger people

#v(0.3em)
*Comprehension Questions*
#v(0.1em)
Josh says tradwife influencers "don't care about what the best expression of being a woman is \ " they care about making money." Why is this distinction important for evaluating online media?
#ruled-lines(2)

The Melbourne study found 40% of boys aged 13-17 agree women lie about domestic violence, partly from social media. How can online content shape beliefs that contradict evidence?
#ruled-lines(2)

Josh says solving this needs both awareness and "safe conversations." Why is awareness alone insufficient, and what makes a conversation safe?
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
- "One piece of evidence that supports this is ..."

*Acknowledging someone else's point of view:*
- "That's an interesting point. I'd add that ..."
- "I see what you mean. However, ..."
- "I hadn't thought of it that way. I think ..."
- "You make a good point about ... but have you considered ...?"

#v(0.3em)
== Think-Pair-Share

1\. To what extent do you agree Gen Z holds the strongest traditional beliefs? Use at least two pieces of evidence from the video.

#text(size: 12pt)[*Structure:* State position \ " Evidence 1 \ " Evidence 2 \ " Conclude]

#ruled-lines(4)

2\. How can young people critically evaluate social media content about gender roles?

#ruled-lines(4)

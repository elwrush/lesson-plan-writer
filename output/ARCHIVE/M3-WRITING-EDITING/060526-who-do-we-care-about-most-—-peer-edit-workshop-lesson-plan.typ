#set text(font: "Roboto", size: 10pt)
#set par(leading: 0.55em)

#show: it => {
  set page(margin: (x: 0.75in, top: 0.75in, bottom: 0.75in))
  it
}

#block(
  stroke: (bottom: 0.5pt + black),
  inset: (bottom: 6pt, top: 12pt),
  grid(
    columns: (1fr, 1fr, 1fr),
    align: (left + horizon, center + horizon, right + horizon),
    image("Image_20260324_141022.png", height: 1.35cm),
    align(center, text(size: 14pt, weight: "bold")[Lesson Plan]),
    image("cambridge.png", height: 1.8cm),
  ),
)
#v(0.3em)

= Lesson Information

*Topic:* Who do we care about most? — Peer Edit Workshop

#table(
  columns: (auto, 1fr, auto, 1fr),
  stroke: 1pt,
  [*Teacher:*], [Ed Rush],
  [*Date:*], [6 May, 2026],
  [*Class:*], [M3],
  [*Duration:*], [46 minutes],
  [*CEFR Level:*], [B2],
  [*Lesson Shape:*], [F (Productive Skills (Traditional))],
  [*Materials:*], table.cell(colspan: 3)[- Students' first drafts from the previous lesson
- Projector (for comparison paragraphs and model edit)
- Timer visible to the class
- Optional: printed 3-point checklist bookmark (half-sheet per pair)
- Coloured pens / pencils if available (one colour per check for clarity)],
  [*Slideshow URL:*], table.cell(colspan: 3, fill: luma(220))[],
)

#v(0.5em)

= Lesson Aim

#block(stroke: (left: 2pt + black), inset: 8pt, [By the end of the lesson, learners will have given and received peer feedback on their PET-style article drafts using a 3-point checklist (capitalisation, compound sentences, the hook) and produced a revised version incorporating that feedback.])

#v(0.5em)

= Lesson Stages

#{
  table(
    columns: (auto, 1fr, 2fr, auto),
    stroke: 1pt,
    table.header([*Time*], [*Goal*], [*Procedure*], [*Int*]),
    ..(
      table.cell(colspan: 4, fill: luma(230))[
        *STAGE 1: LEAD-IN — THREE THINGS WE HAVE BEEN WORKING ON*
      ],
      [6 min],
      [To reactivate prior knowledge of capitalisation, compound sentences, and the hook, and to show students how these three areas make the difference between a weak first draft and a strong final article.],
      [- Project two versions of the opening of an article about a completely different topic (learning to play the piano). The content must be unrelated to the students' own essay so they focus on the editing criteria, not the topic.
  • Version A (weak opening): "i remember the First time i touched a Piano. my fingers felt clumsy. i didnt know where to put them. My Teacher was very patient she showed me where to put my hands."
  • Version B (strong opening): "Have you ever sat down at a piano, placed your hands on the keys, and realised you had no idea what to do? I remember that moment well, and I can still feel the frustration. But my teacher told me that every expert was once a beginner, and those words kept me going."
- Ask: "What is better about Version B? What mistakes can you spot in Version A?" Pairs discuss for 1 minute.
- Elicit answers. Guide students to name the three areas they have been practising: (1) capitalisation — every sentence starts with a capital letter, names are capitalised, 'I' is always capitalised, no random capitals in the middle of words; (2) compound sentences — Version B uses 'and' to connect ideas instead of short choppy sentences; (3) the hook — Version B starts with a question that creates a vivid mental image and makes you want to keep reading.
- Frame the lesson: "Today you will swap drafts with a partner and check each other's work for exactly these three things. The examples I just showed are about learning piano — your article is about close friendships. We are practising the skills, not copying the content."
- Briefly recap each area (30 seconds each):
  • Capitalisation: sentence starts, proper nouns (names, nationalities, languages, specific places), pronoun 'I', no random capitals on common nouns. Correct 'didnt' → 'didn't' (apostrophe in contractions).
  • Compound sentences: two S-V pairs joined by a comma + coordinator (and, but, so, or). If you have only simple sentences, find two related ideas and combine them.
  • The hook: the first sentence should grab attention — a question, a surprising statement, a vivid image, or a bold opinion. It should also make the topic clear.],
      [T-Ss],
      table.cell(colspan: 4, fill: luma(230))[
        *STAGE 2: MODEL EDIT — WATCH ME CHECK A DRAFT*
      ],
      [7 min],
      [To demonstrate exactly how to check for capitalisation, compound sentences, and the hook using a think-aloud on a parallel topic, so students know what to look for and how to mark it without seeing a model they could copy.],
      [- Project a sample paragraph about a different topic again (reaching the summit of a mountain for the first time) — not about piano, and certainly not about close friendships. The paragraph has clear problems in all three areas:
  • Sample: "i will never forget the first time i reached the Summit of a Mountain. the view was breathtaking. i could see for Miles. my legs were aching, i felt truly alive. my Friends were cheering. i felt very Proud."
  • Weak hook: just a personal memory, no image, no question.
  • Capitalisation errors: 'i' not capitalised (three times), 'Summit', 'Mountain', 'Miles', 'Friends', 'Proud' — all common nouns with unnecessary capitals.
  • Comma splice: 'my legs were aching, i felt truly alive' — two S-V pairs joined by only a comma.
- Teacher thinks aloud through all three checks, marking directly on the projected text:
  **Capitalisation:** "First I'm checking capital letters. I read from the beginning. 'i' at the start of a sentence — needs a capital. I'll circle it and write 'C' above. 'the Summit of a Mountain' — these are common nouns, not proper names. 'Summit' and 'Mountain' don't need capitals. I'll cross them out. 'Miles' — same thing, it's just a distance. Cross it out. 'my Friends' — 'friends' is a common noun. Cross out the capital. 'Proud' — cross it out. Now I'm also checking for missing apostrophes. 'didnt' — should be 'didn't'. I'll write the apostrophe in."
  **Compound sentences:** "Now I'm looking for compound sentences. 'my legs were aching, i felt truly alive' — I see two S-V pairs here: 'my legs were aching' and 'i felt truly alive'. They are joined by only a comma. This is a comma splice. I'll underline the comma and write '+coord' above it. That tells the writer to add a word like 'and' or 'but'."
  **The hook:** "Now I read the first sentence. 'i will never forget the first time i reached the Summit of a Mountain.' Does this grab my attention? Not really — it's just telling me a memory. There's no question, no vivid sensory detail, no surprise. I'll write 'hook?' in the margin and a suggestion: 'Try opening with a question or a strong image — what did the air feel like? What did you see?'"
- Ask students: "What marks did I make?" Quick recap: C circles, crossed-out capitals, '+coord' underlines, 'hook?' in the margin.
- Clarify: "These marks are for your partner. You are not fixing their draft — you are showing them where to look. They decide what to change."],
      [T-Ss],
      table.cell(colspan: 4, fill: luma(230))[
        *STAGE 3: PEER EDIT — TWO PASSES*
      ],
      [20 min],
      [To give each student a reader's perspective on their draft through two focused passes — first for overall understanding, then for the three criteria they have been practising in class — so they can see both what works and what needs attention.],
      [- Students swap drafts with a partner. Each pair works together at their desk. Start the timer.

**Pass 1 — Read for understanding (7 minutes)**
- "Read your partner's draft silently from beginning to end. Your job is to understand what they are saying. Make only two kinds of marks:
  • Put a small checkmark ✓ next to parts that are clear and easy to follow.
  • Put a ? next to anything that confuses you or is hard to follow."
- Teacher circulates and prompts: "If you had to explain this part to someone else, would you be able to? That's how you know if it's clear."
- When the timer sounds, students finish their last mark.

**Pass 2 — Three-check edit (13 minutes)**
- "Now read your partner's draft again. This time you are looking for three things we have practised in class. Mark them clearly:"
  • **Capitalisation:** Read sentence by sentence. Circle the first letter of each sentence — is it a capital? If not, write 'C' above it. Check proper nouns (names, nationalities, languages, specific places) — do they have capitals? Check the pronoun 'I' — is it always capitalised? Cross out any unnecessary capitals on common nouns (e.g., 'School', 'Mother', 'Teacher', 'Friend', 'Family') by drawing a line through the capital letter. Check for missing apostrophes in contractions (dont → don't, didnt → didn't, im → I'm).
  • **Compound sentences:** Find every coordinator (and, but, so, or) and draw a box around it. If you find two S-V pairs joined by only a comma (comma splice), underline the comma and write '+coord' above. If you see two short simple sentences next to each other that could be combined, draw a curved line connecting them and write 'combine?' nearby.
  • **The hook:** Read the first sentence again. Does it grab your attention? Put a star ★ in the margin if it is a strong hook (a question that creates curiosity, a vivid image, a surprising statement, a bold opinion). If the hook is weak — 'I think...', 'My article is about...', 'I will talk about...', or just a plain statement — write 'hook?' in the margin. Optional: add a brief suggestion like 'try a question' or 'try a vivid image'.
- Demo the marks briefly on the board: C, crossed-out capital, boxed coordinator, '+coord', 'combine?', star, 'hook?' — so students have a visual reference.
- Teacher circulates. If students ask 'is this right?', redirect: 'What do you think? You are the reader. Does this word need a capital letter?'
- 2-minute warning, then the timer sounds. Students return the draft to its owner.],
      [Ss-Ss],
      table.cell(colspan: 4, fill: luma(230))[
        *STAGE 4: FINAL POLISH — YOUR TURN TO REVISE*
      ],
      [13 min],
      [To give students time to read their partner's feedback and produce a clean final version of their article, deciding for themselves which changes to make.],
      [- Students look at their own draft with their partner's marks. "You now have a reader's feedback. Some marks will make sense immediately. Others you might disagree with — and that is okay. It is your article and you decide what to change."
- Students write or type the final version of their article. Three things to check in their revision:
  • **Capitalisation:** Fix every circled letter and crossed-out capital. Read the first word of every sentence to make sure it starts with a capital. Check proper nouns. Check that 'I' is always capitalised. Add apostrophes to contractions if needed.
  • **Compound sentences:** Look at every '+coord' and 'combine?' mark. Decide whether to add a coordinator, fix a comma splice, or combine two simple sentences into one compound sentence. Aim for at least 2 compound sentences in the final version.
  • **The hook:** Look at the 'hook?' mark if there is one. Revise the first sentence. Read it aloud: does it make you want to keep reading? Compare it to the hooks we looked at earlier — questions, vivid images, surprising statements. Your hook can be about your own experience, but it must make the reader curious.
- Teacher circulates and prompts with questions: "Your partner put a ? here — what do you think they found confusing?", "You have both a C and a crossed-out capital here. Can you see why your partner marked both?", "Only one compound sentence? Where could you add another one?
- 2-minute warning, then timer sounds.
- Collect both the marked-up first draft (with partner's marks visible) and the final version for teacher assessment.],
      [S],
    ),
  )
}

# M2-5A Final Syllable Stress — Three-Product Plan

## Lesson Identity

| Field | Value |
|-------|-------|
| **Class** | M2-5A |
| **Topic** | Thai overstressing of final syllables in English pronunciation |
| **Duration** | 30 minutes |
| **Shape** | B (Language Practice) |
| **CEFR** | A2/B1 |
| **Teacher** | Ed Rush |

## Linguistic Background (Research-Sourced)

- **Cause:** Thai is a fixed-stress language — primary stress always falls on the LAST syllable of polysyllabic words (ERC EJ1225869). This is the opposite of English, where stress is variable (e.g., `TEACHer`, not `teachER`; `ANswer`, not `ansWER`).
- **Mechanism:** Thai is syllable-timed (every syllable has equal weight), while English is stress-timed (unstressed syllables are reduced to schwa). When Thai speakers transfer L1 syllable-timing to English, every syllable sounds equally prominent — unstressed English syllables don't get the vowel reduction they need.
- **Mita's data:** Her pronunciation feedback explicitly calls out overstressed final syllables: `teacher /ˈtiːtʃə/`, `answer /ˈɑːnsə/`, `another /əˈnʌðə/`, `story /ˈstɔːri/` — "your voice is too strong at the end of these words."
- **British Council method:** The O o (big circle / small circle) system marks stressed syllables with a big circle and unstressed with a small circle. Recommended for classroom use because it's visual, intuitive, and requires no IPA knowledge.

---

## Product 1: Bespoke Worksheet (Typst PDF)

### Content Structure

**Header:** M2-5A Pronunciation — Final Syllable Stress | Name: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**Section A — Listen and Underline (5 min)**
- Instruction: "Listen to Mita's recording TWICE. First time — just listen. Second time — underline the words that sound 'too strong' at the end."
- Mita's transcript printed with line spacing for underlining:

> One thing that really stressing me out is math subject. The first reason is that difficult and boring, and the second reason is that hard to understand. For example, last week at your school, my teacher teach me about math, like how to divide, how to find the answer, but I don't understand anything about math because my teacher speak so fast, so I don't understand what she need to explain to me.
>
> And let me tell you another story. One time I want to sleep because the lesson is so boring. That's it.

**Section B — Why Does This Happen? (3 min)**
- Brief explanation in student-friendly language:
  - In Thai, the last syllable of a word is always strong → students carry this habit into English
  - In English, stress can be on ANY syllable → need to learn word-by-word
  - Example: `teacher` = TEACHer (NOT teachER), `answer` = ANSwer (NOT ansWER)

**Section C — Mark the Stress (O o) — 5 Sentences (7 min)**
- Instruction: "For each sentence, use the O o method to mark the stress."
- Example: O o | O | o O | O o | O
  (map to: teacher / gave / us a / boring / lesson)
  Actually better to use the word-level approach:

Example shown on worksheet:
```
teacher → O o     (TEACH-er, not teach-ER)  
answer  → O o     (ANS-wer, not ans-WER)
boring  → O o     (BOR-ing, not bor-ING)
```

Sentences for students to mark:
1. My teacher gave us a boring lesson.
2. I don't understand the answer.
3. Another student told me a story.
4. My favourite subject is history.
5. Please explain the problem carefully.

(Students write O o patterns above each multi-syllable word)

**Section D — Write Your Own — 3 Sentences (5 min)**
- Prompts:
  1. Write about a subject you like or don't like at school. ("I really like English because...")
  2. Write about something a teacher said to you yesterday. ("My teacher told me...")
  3. Write about a hobby you have. ("In my free time, I...")
- After writing: "Circle the multi-syllable words. Mark the stress using O o. Practice reading your sentences aloud."

**Section E — Compare with a London Speaker (3 min)**
- Instruction: "Listen to a 16-year-old student from London read similar sentences. How is her stress different from Mita's? Write one difference:"

---

## Product 2: Lesson Plan (lesson.md → Typst PDF)

### Shape B (Language Practice) — 30 min

| Stage | Time | Activity | Interaction |
|-------|------|----------|-------------|
| 1 — Lead-in: Problem-First Listening | 4 min | Play Mita's audio. "What do you notice about how she pronounces the end of words?" Elicit: sounds too strong, like pushing. Give worksheet Section A. Listen again — students individually underline words that feel overstressed. Pair-check. Class feedback. | T-Ss → Ss-Ss → T-Ss |
| 2 — Explanation: The Thai Rule | 4 min | Board Mita's words: teacher, answer, another, story, boring. Ask: "Which syllable is she stressing?" (the LAST one). Elicit why — in Thai, the last syllable is always strong. Board the Thai rule: word in Thai = ... STRONG. English = unpredictable. Connect to students' own pronunciation. | T-Ss |
| 3 — Controlled Practice: O o Markers | 8 min | Introduce BC O o method. Demo on board: teacher → O o, understand → o o O. Section C of worksheet — students mark stress in 5 sentences. Teacher circulates, checks. Board answers for self-correction. Choral drilling of corrected sentences. | T-Ss → S (indiv) → T-Ss |
| 4 — Freer Practice: Write + Mark + Say | 8 min | Section D — students write 3 sentences from prompts, then mark their own stress, then practice in pairs. Teacher monitors and takes notes for delayed error correction. Pair read-aloud: each student reads their sentences to a partner. | S (indiv) → Ss-Ss |
| 5 — Wrap-up: Model Comparison | 6 min | Play London model audio (16yo female). "Same sentences, but listen to where she puts the stress." Compare to Mita's version. Elicit one takeaway. Collect worksheets for review. | T-Ss |

### Materials
- Bespoke worksheet (Product 1)
- Mita.mp3 audio file
- London model audio file (generated via build-a-monolog skill)
- Whiteboard + markers

### Main aim
By the end of the lesson, learners will have had an opportunity to practise word stress in English and will be better able to avoid overstressing the final syllable of common English words.

### Subsidiary aim
Learners will have developed awareness of L1 transfer from Thai (fixed final-syllable stress) to English (variable word stress).

---

## Product 3: Slides (slides.md → reveal.js HTML)

### Slide Sequence

| # | Slide ID | Title | Feature | Content |
|---|----------|-------|---------|---------|
| 1 | title | Do you sound like this? | background image + shield blocks | Title question + Mita's audio autoplay |
| 2 | objectives | Lesson Objectives | table | 3 objectives: identify, understand, practise |
| 3 | transition | Let's Listen | red background | Cognitive shift to listening |
| 4 | listen-mita | Mita's Recording | audio-autoplay + fragment reveal | Play Mita.mp3. Instructions on screen. |
| 5 | underline-task | Underline the Overstressed Words | fragment reveal | Show transcript. Underline instruction. |
| 6 | answer-check | What Did You Find? | click-table / fragment | Reveal the overstressed words |
| 7 | transition | Why Does This Happen? | red background | Shift to explanation |
| 8 | thai-rule | The Thai Stress Rule | boxed keywords | Board the rule: last syllable in Thai = STRONG |
| 9 | compare | Thai vs English | auto-animate table | Side-by-side comparison |
| 10 | transition | Let's Practise | red background | Shift to practice |
| 11 | bc-method | British Council Stress Markers | boxed keywords | O o method explanation + demo |
| 12 | controlled-practice | Mark the Stress | timer-inject + fragment | 5 sentences from worksheet on screen |
| 13 | controlled-answers | Check Your Answers | click-table | Show O o patterns for each sentence |
| 14 | free-practice | Write Your Own Sentences | timer-inject | 3 prompts on screen |
| 15 | pair-practice | Read to Your Partner | fragment | Pair practice instructions + timer |
| 16 | london-model | Listen to a London Speaker | audio-autoplay | Model audio + reflection question |
| 17 | wrap-up | One Takeaway | fragment | Students write one thing they learned |

### Technical notes for slides
- Audio files (Mita.mp3, london-model.mp3) go in `slides/assets/`
- Background image for title slide: Pixabay search "pronunciation" or "speaking" or "mouth"
- Use `audio-autoplay.lua` filter for autoplay slides
- Timer for practice slides via `timer-inject.lua`

---

## Production Order

1. **Generate London model audio** — build-a-monolog skill (16yo female, London, reading the 5 controlled-practice sentences + 3 sample sentences)
2. **Build bespoke worksheet** — Typst PDF via typst-author or insert-pdf-to-template
3. **Write lesson plan** — lesson.md → build_lesson_pdf.py → PDF
4. **Write slides** — slides.md → pandoc → reveal.js HTML
5. **Copy assets** (audio, images) and build slides

---

## Before You Proceed

Please review and approve this plan (or request changes). Once approved, I'll implement in this order:
1. First — generate the London model audio via build-a-monolog
2. Second — create the bespoke worksheet PDF
3. Third — write the lesson plan Markdown + build PDF
4. Fourth — write the slides Markdown + build HTML

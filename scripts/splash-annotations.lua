if FORMAT:match('revealjs') then
  function Pandoc(doc)
    table.insert(doc.blocks, pandoc.RawBlock('html', '<!-- PEDAGOGICAL INTENT: Students SEE the Heisenberg image before any text -- the transformation metaphor lands subconsciously -->'))
    table.insert(doc.blocks, pandoc.RawBlock('html', '<!-- WHY THIS FEATURE: full-bleed data-background-image with zero text forces students to form their own connection -->'))
    table.insert(doc.blocks, pandoc.RawBlock('html', '<!-- COGNITIVE PRINCIPLE: Multimedia (Mayer) -- image primes emotional/cognitive engagement before verbal content -->'))
    return doc
  end
end

if FORMAT:match('revealjs') then
  function Pandoc(doc)
    table.insert(doc.blocks, pandoc.RawBlock('html',
      '<style>[id^="slide-vocab-"] { font-size: 1.15em; }</style>'))
    return doc
  end
end

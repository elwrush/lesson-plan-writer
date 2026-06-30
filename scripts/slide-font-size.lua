if FORMAT:match('revealjs') then
  function Pandoc(doc)
    table.insert(doc.blocks, pandoc.RawBlock('html',
      '<style>.reveal { font-size: 48px; } .reveal h1 { font-size: 1.4em; } .reveal h2 { font-size: 1.2em; } .reveal p { font-size: 1em; }</style>'))
    return doc
  end
end

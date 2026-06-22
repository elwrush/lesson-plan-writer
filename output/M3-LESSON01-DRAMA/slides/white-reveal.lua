if FORMAT:match('revealjs') then
  function Pandoc(doc)
    table.insert(doc.blocks, pandoc.RawBlock('html', '<style>.fragment.white-reveal.visible { color: white !important; }</style>'))
    return doc
  end
end

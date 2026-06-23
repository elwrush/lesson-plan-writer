if FORMAT:match('typst') then
  function Table(tbl)
    -- Convert Table AST element to a Typst raw block with align(left).
    -- Pandoc's default Typst writer wraps tables in align(center).
    -- This bypasses that by using pandoc.write() to generate the Typst,
    -- then replacing align(center) with align(left).
    local typst = pandoc.write(pandoc.Pandoc{tbl}, 'typst')
    typst = typst:gsub('align%(center%)', 'align(left)')
    return pandoc.RawBlock('typst', typst)
  end
end

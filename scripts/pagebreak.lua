-- pagebreak.lua
-- Converts horizontal rules (---) to #pagebreak() in Typst.
-- Adds a pagebreak before ## Appendix headings.
-- Runs before table-content-fit.lua in the pipeline — no Table dependency.

if FORMAT:match('typst') then
  function Pandoc(doc)
    local new_blocks = {}
    for _, block in ipairs(doc.blocks) do
      if block.t == 'Header' and block.level == 2 then
        local text = ''
        for _, inline in ipairs(block.content) do
          if inline.t == 'Str' then text = text .. inline.text end
          if inline.t == 'Space' then text = text .. ' ' end
        end
        if text:match('^Appendix') then
          table.insert(new_blocks, pandoc.RawBlock('typst', '#pagebreak()'))
        end
      end
      if block.t == 'HorizontalRule' then
        table.insert(new_blocks, pandoc.RawBlock('typst', '#pagebreak()'))
      else
        table.insert(new_blocks, block)
      end
    end
    doc.blocks = new_blocks
    return doc
  end
end

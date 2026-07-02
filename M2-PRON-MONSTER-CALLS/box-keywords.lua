-- box-keywords.lua
-- Adds a visible border to spans with class 'box'
-- Usage in Markdown: [text]{.box}  or  [**text**]{.box}
-- Also handles [text]{.y} for bold yellow text
if FORMAT:match('revealjs') then
  function Span(el)
    if el.classes:includes('box') then
      el.attributes['style'] = 'border: 2px solid #ffdd00; border-radius: 4px; padding: 1px 7px; display: inline-block;'
      return el
    end
    if el.classes:includes('y') then
      el.attributes['style'] = 'color: #ffdd00; font-weight: bold;'
      return el
    end
  end
end

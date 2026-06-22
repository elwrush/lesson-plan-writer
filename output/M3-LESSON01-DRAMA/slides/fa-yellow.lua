-- fa-yellow.lua
-- Makes Font Awesome icons (#fa-) render in yellow (#ffd700) in reveal.js output.
-- Also makes Spans with class "highlight" render in yellow.
-- Usage: pandoc --lua-filter=fa-yellow.lua ...

if FORMAT:match('revealjs') then
  function RawInline(el)
    if el.text:match('fa%-') then
      el.text = el.text:gsub('class="', 'style="color: #ffd700; " class="')
    end
    return el
  end

  function Span(el)
    for _, cls in ipairs(el.attr.classes) do
      if cls == "highlight" or cls == "label" then
        el.attributes['style'] = 'color: #ffd700;'
        return el
      end
    end
    return el
  end
end

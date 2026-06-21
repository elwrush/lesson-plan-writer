-- vocab-animate.lua
-- Two jobs:
-- 1) Injects data-auto-animate into all slide-level headers
-- 2) Adds display: inline-block to any fenced div with a data-id attribute,
--    so auto-animate can animate position changes on inline-flow content.
-- Usage: pandoc --lua-filter=vocab-animate.lua ...
if FORMAT:match('revealjs') then

  function Header(el)
    el.attributes['data-auto-animate'] = ''
    return el
  end

  function Div(el)
    if el.attributes['data-id'] then
      el.attributes['style'] = 'display: inline-block;'
    end
    return el
  end

end

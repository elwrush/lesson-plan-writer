-- auto-animate.lua
-- Injects data-auto-animate into all slide-level headers
-- so reveal.js auto-animate can be triggered without manual
-- {data-auto-animate=""} on every heading.
-- Usage: pandoc --lua-filter=auto-animate.lua ...
if FORMAT:match('revealjs') then
  function Header(el)
    el.attributes['data-auto-animate'] = ''
    return el
  end
end

-- presentation-defaults.lua
-- Consolidated presentation defaults for reveal.js slides.
-- Replaces: slide-font-size.lua, fa-yellow.lua, white-reveal.lua, vocab-size.lua
-- Usage: pandoc --lua-filter=presentation-defaults.lua ...

if FORMAT:match('revealjs') then

  -- ── Inject all CSS in one Pandoc pass ──
  function Pandoc(doc)
    table.insert(doc.blocks, pandoc.RawBlock('html', [[
<style>
.reveal { font-size: 48px; }
.reveal h1 { font-size: 1.4em; }
.reveal h2 { font-size: 1.2em; }
.reveal p { font-size: 1em; }
[id^="slide-vocab-"] { font-size: 1.15em; }
.fragment.white-reveal.visible { color: white !important; }
</style>
]]))
    return doc
  end

  -- ── Yellow highlight spans (replaces fa-yellow.lua Span handler) ──
  function Span(el)
    for _, cls in ipairs(el.attr.classes) do
      if cls == "highlight" or cls == "label" then
        el.attributes['style'] = 'color: #ffd700;'
        return el
      end
    end
    return el
  end

  -- ── Yellow Font Awesome icons (replaces fa-yellow.lua RawInline handler) ──
  function RawInline(el)
    if el.text:match('fa%-') then
      el.text = el.text:gsub('class="', 'style="color: #ffd700; " class="')
    end
    return el
  end

end

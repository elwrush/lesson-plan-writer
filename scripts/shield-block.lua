-- shield-block.lua
-- Processes heading, paragraph, and div elements for reveal.js slides.
-- Uses Pandoc's attribute transfer mechanism: heading attributes on
-- slide-level headings propagate to the <section> element in HTML output.
if FORMAT:match('revealjs') then

--- @param h pandoc_header
--- @return pandoc_header|nil
function Header(h)
  if h.identifier == 'title' then
    h.attributes['style'] = 'position: relative;'
    return h
  end
end

--- Position the logo absolutely within the title slide by wrapping
--- it in a Div with absolute positioning. The nearest positioned
--- ancestor is the <section> (via Header position:relative transfer).
--- @param p pandoc_para
--- @return pandoc_div|nil
function Para(p)
  for _, il in ipairs(p.content) do
    if il.t == 'Image' then
      --- @cast il pandoc_image
      if il.classes:includes('title-logo') then
        return pandoc.Div(
          {pandoc.Plain(p.content)},
          {style = 'position: absolute; top: 30px; left: 30px; margin: 0;'}
        )
      end
    end
  end
end

--- @param d pandoc_div
--- @return pandoc_div|nil
function Div(d)
  if d.classes:includes('shield') then
    d.attributes['style'] = 'display: flex; align-items: center; width: fit-content; margin: 0.3em auto; padding: 0.1em 0.4em; color: #ffdd00;'
    for i, block in ipairs(d.content) do
      if block.t == 'Para' then
        --- @cast block pandoc_para
        d.content[i] = pandoc.Plain(block.content)
      end
    end
    return d
  end
  if d.classes:includes('title-row') then
    d.attributes['style'] = 'padding: 0.1em 0.4em;'
    return d
  end
end

end

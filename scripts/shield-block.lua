-- shield-block.lua
-- Processes heading, paragraph, and div elements for reveal.js slides.
-- Uses Pandoc's attribute transfer mechanism: heading attributes on
-- slide-level headings propagate to the <section> element in HTML output.
if FORMAT:match('revealjs') then

--- Override reveal.js vertical centering on every slide
--- so content starts at the top instead of being centered.
--- @param h pandoc_header
--- @return pandoc_header|nil
function Header(h)
  -- Skip headings with data-auto-animate (even empty value):
  -- justify-content interferes with reveal.js auto-animate
  if h.attributes['data-auto-animate'] ~= nil then return h end
  h.attributes['style'] = 'justify-content: flex-start !important;'
  return h
end

--- Center the logo at the top of the title slide in normal content flow.
--- The image width is controlled by the Markdown `width=` attribute.
--- @param p pandoc_para
--- @return pandoc_div|nil
function Para(p)
  for _, il in ipairs(p.content) do
    if il.t == 'Image' then
      --- @cast il pandoc_image
      if il.classes:includes('title-logo') then
        return pandoc.Div(
          {pandoc.Plain(p.content)},
          {style = 'text-align: center; margin: 10px 0 0 0;'}
        )
      end
    end
  end
end

--- @param d pandoc_div
--- @return pandoc_div|nil
function Div(d)
  if d.classes:includes('shield') then
    d.attributes['style'] = 'display: flex; align-items: center; width: fit-content; margin: 0.1em auto; padding: 0.1em 0.4em; background: rgba(0, 0, 0, 0.55); border-radius: 4px; text-shadow: none; line-height: 1.3;'
    for i, block in ipairs(d.content) do
      if block.t == 'Para' then
        --- @cast block pandoc_para
        d.content[i] = pandoc.Plain(block.content)
      end
    end
    return d
  end
  if d.classes:includes('title-row') then
    for i, block in ipairs(d.content) do
      if block.t == 'Para' then
        --- @cast block pandoc_para
        d.content[i] = pandoc.Plain(block.content)
      end
    end
    d.attributes['style'] = 'padding: 0.1em 0.4em; background: rgba(0, 0, 0, 0.55); border-radius: 4px; display: inline-block; white-space: nowrap; text-shadow: none; margin-bottom: 0.3em;'
    return d
  end
end

end

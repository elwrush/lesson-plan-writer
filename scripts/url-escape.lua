-- url-escape.lua
-- Escape metadata URL values for safe rendering inside Typst [...] content blocks.
-- Typst interprets // as a line comment inside [...] so URLs need #text("...")
-- wrapping to avoid comment parsing.
local URL_META_KEYS = {
  slideshow_url = true,
}

function Meta(meta)
  for key, _ in pairs(URL_META_KEYS) do
    local val = meta[key]
    if val then
      local url = pandoc.utils.stringify(val)
      url = url:gsub('"', '\\"')
      meta[key] = '#text("' .. url .. '")'
    end
  end
  return meta
end

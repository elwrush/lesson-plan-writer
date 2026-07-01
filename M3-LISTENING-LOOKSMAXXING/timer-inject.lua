-- timer-inject.lua
-- Reads data-timer (seconds) from headings and injects a countdown timer pill.
-- Uses slide-helper.lua for timer_div().
-- Usage: pandoc --lua-filter=timer-inject.lua ...

if FORMAT:match('revealjs') then
  local source = debug.getinfo(1).source:gsub('^@', '')
  local script_dir = source:match("(.*[/\\])")
  local slide = dofile(script_dir .. 'slide-helper.lua')

  function Header(h)
    local seconds = h.attributes['data-timer']
    if seconds then
      local sec_num = tonumber(seconds)
      if sec_num and sec_num > 0 then
        return { h, slide.timer_div(sec_num) }
      end
    end
    return h
  end
end

-- autocue.lua
-- Self-contained scrolling teleprompter for reveal.js slides.
-- No external CSS/HTML files needed.
-- Usage:
--   ::: {.autocue .a2}
--   Text at A2 speed
--   :::
-- Speeds: .a2 (80 wpm), .b1 (130 wpm default), .b2 (180 wpm)
-- Duration is calculated from word count + reading speed.

if FORMAT:match('revealjs') then

  local has_autocue = false

  local function count_words(blocks)
    local text = pandoc.utils.stringify(blocks)
    local n = 0
    for _ in text:gmatch("%S+") do n = n + 1 end
    return n
  end

  local function build_autocue(el, speed)
    local wpm = 130
    if speed == "a2" then wpm = 80 end
    if speed == "b2" then wpm = 180 end

    local word_count = count_words(el.content)
    local seconds = math.max(8, math.ceil(word_count / wpm * 60))
    local duration = tostring(seconds) .. "s"

    -- Calculate start offset so some text is visible immediately
    -- Est. text height ~ word_count * 4px. Want ~60% hidden below, 40% visible.
    local start_pct = math.min(80, math.max(20, math.floor(word_count * 0.35)))

    -- Scoped CSS inside the slide
    local css = pandoc.RawBlock('html', [[
<style>
@keyframes autocue-scroll {
  0% { transform: translateY(]] .. start_pct .. [[%); }
  100% { transform: translateY(-100%); }
}
.autocue-outer {
  height: 320px; overflow: hidden; position: relative;
  border: 1px solid rgba(255,255,255,0.2); border-radius: 8px;
  padding: 0 16px; background: rgba(0,0,0,0.3); text-align: left;
}
.autocue-inner {
  position: absolute; width: calc(100% - 32px);
  font-size: 1.1em; line-height: 1.6; text-align: left;
  animation: autocue-scroll linear forwards;
  animation-duration: ]] .. duration .. [[;
}
.autocue-badge {
  position: absolute; bottom: 8px; right: 12px;
  display: inline-block; padding: 2px 10px;
  border-radius: 4px; font-size: 0.7em; font-weight: bold;
  text-transform: uppercase; z-index: 2;
}
.autocue-speed-a2 .autocue-badge { background: #27ae60; color: #fff; }
.autocue-speed-b1 .autocue-badge { background: #f39c12; color: #fff; }
.autocue-speed-b2 .autocue-badge { background: #e74c3c; color: #fff; }
.autocue-toggle {
  position: absolute; top: 8px; right: 12px; z-index: 2;
  background: rgba(255,255,255,0.15); border: 1px solid rgba(255,255,255,0.3);
  color: #fff; border-radius: 4px; padding: 2px 10px;
  font-size: 1em; cursor: pointer; line-height: 1.4;
}
.autocue-toggle:hover { background: rgba(255,255,255,0.3); }
</style>
]])

    -- Toggle button + badge
    local html = pandoc.RawBlock('html',
      '<button class="autocue-toggle">⏸</button>' ..
      '<span class="autocue-badge">' .. speed:upper() .. '</span>')

    -- Inner scrolling content
    local inner = pandoc.Div(el.content, {class = 'autocue-inner'})

    return pandoc.Div(
      {css, html, inner},
      {class = 'autocue-outer autocue-speed-' .. speed}
    )
  end

  function Div(el)
    if el.classes:includes('autocue') then
      has_autocue = true
      local speed = "b1"
      if el.classes:includes('a2') then speed = "a2" end
      if el.classes:includes('b2') then speed = "b2" end
      return build_autocue(el, speed)
    end
  end

  function Pandoc(doc)
    if has_autocue then
      table.insert(doc.blocks, pandoc.RawBlock('html', [[
<section id="autocue-global-script" style="display:none">
<script>
(function() {
  if (typeof Reveal === 'undefined') return;
  Reveal.on('slidechanged', function(event) {
    var containers = event.currentSlide.querySelectorAll('.autocue-outer');
    for (var i = 0; i < containers.length; i++) {
      var inner = containers[i].querySelector('.autocue-inner');
      if (!inner) continue;
      inner.style.animation = 'none';
      void inner.offsetHeight;
      inner.style.animation = '';
    }
    var buttons = event.currentSlide.querySelectorAll('.autocue-toggle');
    for (var j = 0; j < buttons.length; j++) {
      buttons[j].onclick = function() {
        var inner = this.parentElement.querySelector('.autocue-inner');
        if (!inner) return;
        if (inner.style.animationPlayState === 'paused') {
          inner.style.animationPlayState = 'running';
          this.textContent = '⏸';
        } else {
          inner.style.animationPlayState = 'paused';
          this.textContent = '▶';
        }
      };
    }
  });
})();
</script>
</section>
]]))
    end
    return doc
  end

end

/* captions-plugin.js — Large high-contrast captions UNDER the audio player.
 *
 * For every slide with `.caption-video` + `.caption-overlay`, this plugin:
 *   1. FETCHES the .vtt file directly (robust — not dependent on <track>
 *      activeCues timing) and parses it into a cue list.
 *   2. On `timeupdate`, finds the active cue and renders it large + high-contrast
 *      in the overlay BELOW the player.
 *   3. Sizes it for room readability.
 *
 * Injected by post-process.py.
 */
(function () {
  "use strict";

  // ── Browser check ──────────────────────────────────────────────────
  // Captions rely on native <video>/WebVTT which is reliable in Chrome.
  // If a different browser is detected, show a persistent badge.
  var isChrome = /Chrome\//.test(navigator.userAgent) && !/Edg\//.test(navigator.userAgent) && !/OPR\//.test(navigator.userAgent);
  if (!isChrome) {
    var badge = document.createElement("div");
    badge.className = "browser-badge";
    badge.textContent = "⚠ Best in Chrome — captions/audio may not display correctly";
    badge.title = "This deck is designed for Google Chrome.";
    document.documentElement.appendChild(badge);
  }

  function parseVtt(raw) {
    var cues = [];
    var lines = raw.split(/\r?\n/);
    var i = 0;
    while (i < lines.length) {
      var line = lines[i].trim();
      // "HH:MM:SS.mmm --> HH:MM:SS.mmm" (allow HH:MM:SS, MM:SS.mmm, etc.)
      var m = line.match(
        /^(\d{1,2}:)?(\d{1,2}):(\d{1,2})\.(\d{1,3})\s*-->\s*(\d{1,2}:)?(\d{1,2}):(\d{1,2})\.(\d{1,3})/
      );
      if (m && m.index === 0) {
        var start = toSec(m[1], m[2], m[3], m[4]);
        var end = toSec(m[5], m[6], m[7], m[8]);
        var text = [];
        i++;
        while (i < lines.length && lines[i].trim() !== "") {
          text.push(lines[i].trim());
          i++;
        }
        cues.push({ start: start, end: end, text: text.join(" ") });
      } else {
        i++;
      }
    }
    return cues;
  }

  function toSec(hhGroup, mm, ss, mmm) {
    var sec = parseFloat(mm) * 60 + parseFloat(ss) + (parseFloat(mmm) || 0) / 1000;
    if (hhGroup) {
      var hh = parseFloat(hhGroup.replace(":", "")) || 0;
      sec += hh * 3600;
    }
    return sec;
  }

  function initCaptions() {
    var vids = document.querySelectorAll("section .caption-video");
    if (!vids.length) return;

    vids.forEach(function (video) {
      var wrap = video.closest(".captions-wrap");
      var overlay = wrap ? wrap.querySelector(".caption-overlay") : null;
      if (!overlay) return;

      var track = video.querySelector('track[kind="captions"]');
      var cues = [];

      function update() {
        if (!cues.length) return;
        var t = video.currentTime;
        var active = null;
        for (var k = 0; k < cues.length; k++) {
          if (t >= cues[k].start && t < cues[k].end) { active = cues[k].text; break; }
        }
        overlay.textContent = active || "";
        overlay.classList.toggle("caption-on", !!active);
      }

      function loadVtt() {
        if (!track) return;
        fetch(track.getAttribute("src"))
          .then(function (r) { return r.text(); })
          .then(function (raw) { cues = parseVtt(raw); update(); })
          .catch(function () {});
      }

      video.addEventListener("timeupdate", update);
      video.addEventListener("loadedmetadata", loadVtt);
      // VTT may load async — attempt early and on canplay too.
      if (document.readyState === "complete") loadVtt();
      else window.addEventListener("load", loadVtt);
      video.addEventListener("canplay", loadVtt);
    });
  }

  Reveal.addEventListener("ready", initCaptions);
  Reveal.addEventListener("slidechanged", initCaptions);
})();

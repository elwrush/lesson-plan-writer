(function () {
    var BLIP_AUDIO_SRC = "assets/blip.mp3";
    var BELL_AUDIO_SRC = "assets/BELL.mp3";
    var WARNING_THRESHOLD = 10;

    var pillEl = null;
    var displayEl = null;
    var startBtn = null;
    var pauseBtn = null;
    var resetBtn = null;
    var blipAudio = null;
    var bellAudio = null;

    var totalSeconds = 0;
    var secondsLeft = 0;
    var intervalId = null;
    var warned = false;    // true after first bell warning played (at &le;10s)
    var finished = false;  // true once timer hit 0 and final bell played
    var lastMinute = -1;   // track minute for blip-at-every-minute

    function createPill() {
        if (pillEl) return;

        pillEl = document.createElement("div");
        pillEl.className = "timer-pill";

        startBtn = document.createElement("button");
        startBtn.className = "timer-pill__btn";
        startBtn.innerHTML = "&#9654;";  // ⏵ play
        startBtn.title = "Start timer";

        pauseBtn = document.createElement("button");
        pauseBtn.className = "timer-pill__btn timer-pill__btn--hidden";
        pauseBtn.innerHTML = "\u23F8";  // ⏸ pause
        pauseBtn.title = "Pause timer";

        resetBtn = document.createElement("button");
        resetBtn.className = "timer-pill__btn";
        resetBtn.innerHTML = "&#8634;";  // ↺ reset
        resetBtn.title = "Reset timer";

        displayEl = document.createElement("span");
        displayEl.className = "timer-pill__display";

        pillEl.appendChild(startBtn);
        pillEl.appendChild(pauseBtn);
        pillEl.appendChild(resetBtn);
        pillEl.appendChild(displayEl);

        document.body.appendChild(pillEl);

        startBtn.addEventListener("click", function () {
            playBlip();
            onStart();
        });
        pauseBtn.addEventListener("click", function () {
            playBlip();
            onPause();
        });
        resetBtn.addEventListener("click", function () {
            playBlip();
            onReset();
        });
    }

    function formatTime(seconds) {
        var m = Math.floor(seconds / 60);
        var s = seconds % 60;
        return (m < 10 ? "0" : "") + m + ":" + (s < 10 ? "0" : "") + s;
    }

    function showPill() {
        pillEl.classList.add("timer-pill--visible");
    }

    function hidePill() {
        clearInterval(intervalId);
        intervalId = null;
        pillEl.classList.remove("timer-pill--visible");
    }

    function onStart() {
        if (finished) return; // timer expired, must reset first
        startBtn.classList.add("timer-pill__btn--hidden");
        pauseBtn.classList.remove("timer-pill__btn--hidden");
        playBlip(); // blip on start (also for autostart)
        // Record current minute for minute-blip tracking
        lastMinute = Math.floor(secondsLeft / 60);
        intervalId = setInterval(tick, 1000);
        tick(); // update display immediately
    }

    function onPause() {
        clearInterval(intervalId);
        intervalId = null;
        startBtn.classList.remove("timer-pill__btn--hidden");
        pauseBtn.classList.add("timer-pill__btn--hidden");
    }

    function onReset() {
        clearInterval(intervalId);
        intervalId = null;
        secondsLeft = totalSeconds;
        warned = false;
        finished = false;
        lastMinute = -1;
        startBtn.classList.remove("timer-pill__btn--hidden");
        pauseBtn.classList.add("timer-pill__btn--hidden");
        pillEl.classList.remove("timer-pill--warning");
        pillEl.classList.remove("timer-pill--expired");
        displayEl.textContent = formatTime(secondsLeft);
    }

    function tick() {
        if (secondsLeft <= 0) {
            clearInterval(intervalId);
            intervalId = null;
            finished = true;
            startBtn.classList.add("timer-pill__btn--hidden");
            pauseBtn.classList.add("timer-pill__btn--hidden");
            pillEl.classList.add("timer-pill--expired");
            displayEl.textContent = "00:00";
            playBell();
            return;
        }

        secondsLeft--;
        displayEl.textContent = formatTime(secondsLeft);

        // Last 10 seconds: blip every second
        if (secondsLeft <= WARNING_THRESHOLD) {
            pillEl.classList.add("timer-pill--warning");
            playBlip();
        } else {
            // Blip at every minute boundary
            var currentMinute = Math.floor(secondsLeft / 60);
            if (lastMinute !== -1 && currentMinute !== lastMinute) {
                playBlip();
            }
            lastMinute = currentMinute;
        }
    }

    function playBlip() {
        if (blipAudio) {
            blipAudio.currentTime = 0;
            blipAudio.play().catch(function () {});
        }
    }

    function playBell() {
        if (bellAudio) {
            bellAudio.currentTime = 0;
            bellAudio.play().catch(function () {});
        }
    }

    function loadSlideTimer(deck) {
        hidePill();
        lastMinute = -1;

        var slide = deck.getCurrentSlide();
        if (!slide) return;

        var timerVal = slide.getAttribute("data-timer");
        if (!timerVal) return;

        var parsed = parseInt(timerVal, 10);
        if (isNaN(parsed) || parsed <= 0) return;

        totalSeconds = parsed;
        secondsLeft = totalSeconds;
        warned = false;
        finished = false;

        pillEl.classList.remove("timer-pill--warning");
        pillEl.classList.remove("timer-pill--expired");
        startBtn.classList.remove("timer-pill__btn--hidden");
        pauseBtn.classList.add("timer-pill__btn--hidden");

        displayEl.textContent = formatTime(secondsLeft);
        showPill();
        // Autostart timer on slide entry
        onStart();
    }

    var TimerPlugin = {
        id: "timer-pill",
        init: function (deck) {
            createPill();

            // Preload blip and bell audio
            blipAudio = new Audio(BLIP_AUDIO_SRC);
            blipAudio.preload = "auto";
            bellAudio = new Audio(BELL_AUDIO_SRC);
            bellAudio.preload = "auto";

            // When slide changes, load or hide timer
            deck.on("slidechanged", function () {
                loadSlideTimer(deck);
            });

            // When reveal.js pauses, pause the timer
            deck.on("paused", function () {
                if (intervalId !== null) {
                    onPause();
                }
            });
        },
    };

    // Expose globally so slides-template.html can register it
    window.TimerPlugin = TimerPlugin;

    // Auto-init: poll for reveal.js, then bind directly
    (function autoInit() {
        var check = setInterval(function() {
            if (typeof Reveal !== 'undefined') {
                clearInterval(check);
                var readyCheck = setInterval(function() {
                    if (Reveal.isReady()) {
                        clearInterval(readyCheck);
                        createPill();
                        blipAudio = new Audio(BLIP_AUDIO_SRC);
                        blipAudio.preload = "auto";
                        bellAudio = new Audio(BELL_AUDIO_SRC);
                        bellAudio.preload = "auto";
                        Reveal.on('slidechanged', function() {
                            loadSlideTimer(Reveal);
                        });
                        Reveal.on('paused', function() {
                            if (intervalId !== null) onPause();
                        });
                        loadSlideTimer(Reveal);
                    }
                }, 50);
            }
        }, 50);
    })();
})();

// Auto-init: poll for reveal.js, then bind directly (not a registered plugin)
(function autoInit() {
    var check = setInterval(function() {
        if (typeof Reveal !== 'undefined') {
            clearInterval(check);
            var readyCheck = setInterval(function() {
                if (Reveal.isReady()) {
                    clearInterval(readyCheck);
                    createPill();
                    blipAudio = new Audio(BLIP_AUDIO_SRC);
                    blipAudio.preload = "auto";
                    bellAudio = new Audio(BELL_AUDIO_SRC);
                    bellAudio.preload = "auto";
                    Reveal.on('slidechanged', function() {
                        loadSlideTimer(Reveal);
                    });
                    Reveal.on('paused', function() {
                        if (intervalId !== null) onPause();
                    });
                    loadSlideTimer(Reveal);
                }
            }, 50);
        }
    }, 50);
})();

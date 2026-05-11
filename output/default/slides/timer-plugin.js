(function () {
    var CHIME_AUDIO_SRC = "assets/chime.mp3";
    var WARNING_THRESHOLD = 10;

    var pillEl = null;
    var displayEl = null;
    var startBtn = null;
    var pauseBtn = null;
    var resetBtn = null;
    var chimeAudio = null;

    var totalSeconds = 0;
    var secondsLeft = 0;
    var intervalId = null;
    var warned = false;    // true after first chime played (at ≤10s)
    var finished = false;  // true once timer hit 0 and final chime played

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
        pauseBtn.innerHTML = "&#9646;&#9646;";  // ⏸ pause
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

        startBtn.addEventListener("click", onStart);
        pauseBtn.addEventListener("click", onPause);
        resetBtn.addEventListener("click", onReset);
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
            playChime();
            return;
        }

        secondsLeft--;
        displayEl.textContent = formatTime(secondsLeft);

        if (secondsLeft <= WARNING_THRESHOLD && !warned) {
            warned = true;
            pillEl.classList.add("timer-pill--warning");
            playChime();
        }
    }

    function playChime() {
        if (chimeAudio) {
            chimeAudio.currentTime = 0;
            chimeAudio.play().catch(function () {});
        }
    }

    function loadSlideTimer(deck) {
        hidePill();

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
    }

    var TimerPlugin = {
        id: "timer-pill",
        init: function (deck) {
            createPill();

            // Preload chime audio
            chimeAudio = new Audio(CHIME_AUDIO_SRC);
            chimeAudio.preload = "auto";

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

            // On resize or layout change, no special action needed
        },
    };

    // Expose globally so slides-template.html can register it
    window.TimerPlugin = TimerPlugin;
})();
(function () {
    var BLIP_SRC = "assets/blip.mp3";
    var BELL_SRC = "assets/BELL.mp3";
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
    var finished = false;
    var lastMinute = -1;

    function createPill() {
        if (pillEl) return;

        pillEl = document.createElement("div");
        pillEl.className = "timer-pill";

        startBtn = document.createElement("button");
        startBtn.className = "timer-pill__btn";
        startBtn.innerHTML = "&#9654;";
        startBtn.title = "Start timer";

        pauseBtn = document.createElement("button");
        pauseBtn.className = "timer-pill__btn timer-pill__btn--hidden";
        pauseBtn.innerHTML = "\u23F8";
        pauseBtn.title = "Pause timer";

        resetBtn = document.createElement("button");
        resetBtn.className = "timer-pill__btn";
        resetBtn.innerHTML = "&#8634;";
        resetBtn.title = "Reset timer";

        displayEl = document.createElement("span");
        displayEl.className = "timer-pill__display";

        pillEl.appendChild(startBtn);
        pillEl.appendChild(pauseBtn);
        pillEl.appendChild(resetBtn);
        pillEl.appendChild(displayEl);

        document.body.appendChild(pillEl);

        startBtn.addEventListener("click", function(){ playBlip(); onStart(); });
        pauseBtn.addEventListener("click", function(){ playBlip(); onPause(); });
        resetBtn.addEventListener("click", function(){ playBlip(); onReset(); });
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
        pillEl.classList.remove("timer-pill--visible");
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

    function onStart() {
        if (finished) return;
        startBtn.classList.add("timer-pill__btn--hidden");
        pauseBtn.classList.remove("timer-pill__btn--hidden");
        lastMinute = Math.floor(secondsLeft / 60);
        intervalId = setInterval(tick, 1000);
        tick();
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
        finished = false;
        lastMinute = Math.floor(secondsLeft / 60);
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

        // Blip every second in last 10 seconds
        if (secondsLeft <= WARNING_THRESHOLD) {
            pillEl.classList.add("timer-pill--warning");
            playBlip();
        }

        // Beep every minute (on the minute mark)
        var currentMinute = Math.floor(secondsLeft / 60);
        if (currentMinute < lastMinute) {
            lastMinute = currentMinute;
            playBell();
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
        finished = false;
        lastMinute = Math.floor(secondsLeft / 60);

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

            blipAudio = new Audio(BLIP_SRC);
            blipAudio.preload = "auto";
            bellAudio = new Audio(BELL_SRC);
            bellAudio.preload = "auto";

            deck.on("slidechanged", function () {
                loadSlideTimer(deck);
            });

            deck.on("paused", function () {
                if (intervalId !== null) {
                    onPause();
                }
            });
        },
    };

    window.TimerPlugin = TimerPlugin;
})();

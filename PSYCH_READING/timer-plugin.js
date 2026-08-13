(function () {
    var BLIP_SRC = "assets/blip.mp3";
    var BELL_SRC = "assets/BELL.mp3";
    var WARNING_THRESHOLD = 10;

    var pillEl = null, displayEl = null, startBtn = null, pauseBtn = null, resetBtn = null;
    var blipAudio = null, bellAudio = null;
    var totalSeconds = 0, secondsLeft = 0, intervalId = null, finished = false, lastMinute = -1;

    function createPill() {
        if (pillEl) return;
        pillEl = document.createElement("div"); pillEl.className = "timer-pill";
        startBtn = document.createElement("button"); startBtn.className = "timer-pill__btn"; startBtn.innerHTML = "\u25B6"; startBtn.title = "Start timer";
        pauseBtn = document.createElement("button"); pauseBtn.className = "timer-pill__btn timer-pill__btn--hidden"; pauseBtn.innerHTML = "\u23F8"; pauseBtn.title = "Pause timer";
        resetBtn = document.createElement("button"); resetBtn.className = "timer-pill__btn"; resetBtn.innerHTML = "\u21B4"; resetBtn.title = "Reset timer";
        displayEl = document.createElement("span"); displayEl.className = "timer-pill__display";
        [startBtn, pauseBtn, resetBtn, displayEl].forEach(function(el){ pillEl.appendChild(el); });
        document.querySelector('.reveal').appendChild(pillEl);
        startBtn.addEventListener("click", function(){ playBlip(); onStart(); });
        pauseBtn.addEventListener("click", function(){ playBlip(); onPause(); });
        resetBtn.addEventListener("click", function(){ playBlip(); onReset(); });
    }

    function fmt(s){ var m=Math.floor(s/60); var n=s%60; return (m<10?"0":"")+m+":"+(n<10?"0":"")+n; }

    function showPill(){ pillEl.classList.add("timer-pill--visible"); }
    function hidePill(){ pillEl.classList.remove("timer-pill--visible"); }
    function playBlip(){ if(blipAudio){ blipAudio.currentTime=0; blipAudio.play().catch(function(){}); }}
    function playBell(){ if(bellAudio){ bellAudio.currentTime=0; bellAudio.play().catch(function(){}); }}

    function onStart(){
        if(finished)return; if(intervalId!==null){clearInterval(intervalId);} startBtn.classList.add("timer-pill__btn--hidden"); pauseBtn.classList.remove("timer-pill__btn--hidden");
        lastMinute=Math.floor(secondsLeft/60); intervalId=setInterval(tick,1000); tick();
    }

    function onPause(){ clearInterval(intervalId);intervalId=null;startBtn.classList.remove("timer-pill__btn--hidden");pauseBtn.classList.add("timer-pill__btn--hidden");}
    function onReset(){ clearInterval(intervalId);intervalId=null;secondsLeft=totalSeconds;finished=false;lastMinute=Math.floor(secondsLeft/60);startBtn.classList.remove("timer-pill__btn--hidden");pauseBtn.classList.add("timer-pill__btn--hidden");pillEl.classList.remove("timer-pill--warning");pillEl.classList.remove("timer-pill--expired");displayEl.textContent=fmt(secondsLeft);}

    function tick(){
        if(secondsLeft<=0){clearInterval(intervalId);intervalId=null;finished=true;startBtn.classList.add("timer-pill__btn--hidden");pauseBtn.classList.add("timer-pill__btn--hidden");pillEl.classList.add("timer-pill--expired");displayEl.textContent="00:00";playBell();return;}
        secondsLeft--;displayEl.textContent=fmt(secondsLeft);
        if(secondsLeft<=WARNING_THRESHOLD){pillEl.classList.add("timer-pill--warning");playBlip();}
        var cm=Math.floor(secondsLeft/60);if(cm<lastMinute){lastMinute=cm;playBell();}
    }

    function loadSlideTimer(deck){
        if(intervalId!==null){clearInterval(intervalId);intervalId=null;} hidePill();var slide=deck.getCurrentSlide();if(!slide)return;
        var tv=slide.getAttribute("data-timer");if(!tv)return;
        var p=parseInt(tv,10);if(isNaN(p)||p<=0)return;
        totalSeconds=p;secondsLeft=totalSeconds;finished=false;lastMinute=Math.floor(secondsLeft/60);
        pillEl.classList.remove("timer-pill--warning");pillEl.classList.remove("timer-pill--expired");
        startBtn.classList.remove("timer-pill__btn--hidden");pauseBtn.classList.add("timer-pill__btn--hidden");
        displayEl.textContent=fmt(secondsLeft);showPill();
        if(slide.getAttribute("data-timer-autostart")==="true"){onStart();}
    }

    window.TimerPlugin = { id: "timer-pill", init: function(deck){
        createPill();
        blipAudio=new Audio(BLIP_SRC);blipAudio.preload="auto";
        bellAudio=new Audio(BELL_SRC);bellAudio.preload="auto";
        deck.on("slidechanged",function(){loadSlideTimer(deck);});
        deck.on("paused",function(){if(intervalId!==null)onPause();});
    }};
})();

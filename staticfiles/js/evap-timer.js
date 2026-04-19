// =========================
// EVAP GLOBAL TIMER (PERSISTENT ACROSS PAGES)
// =========================

const EvapTimer = {

  mode: "stopwatch",
  running: false,

  startTime: null,
  elapsed: 0,
  duration: 0,

  interval: null,
  widget: null,

  // -------------------------
  // INIT
  // -------------------------
  init() {
    this.load();
    this.createWidget();
    this.loop();

    // IMPORTANT: restore display immediately
    this.updateUI(this.getTime());
  },

  // -------------------------
  // STORAGE
  // -------------------------
  save() {
    localStorage.setItem("evap_timer", JSON.stringify({
      mode: this.mode,
      running: this.running,
      startTime: this.startTime,
      elapsed: this.elapsed,
      duration: this.duration
    }));
  },

  load() {
    const data = JSON.parse(localStorage.getItem("evap_timer"));
    if (!data) return;

    this.mode = data.mode || "stopwatch";
    this.running = data.running || false;
    this.startTime = data.startTime || null;
    this.elapsed = data.elapsed || 0;
    this.duration = data.duration || 0;
  },

  // -------------------------
  // TIME LOGIC
  // -------------------------
  getTime() {
    if (!this.running) return this.elapsed;

    if (this.mode === "stopwatch") {
      return Date.now() - this.startTime;
    }

    if (this.mode === "countdown") {
      return this.duration - (Date.now() - this.startTime);
    }
  },

  // -------------------------
  // LOOP
  // -------------------------
  loop() {
    this.interval = setInterval(() => {

      if (!this.running) return;

      let t = this.getTime();

      if (this.mode === "countdown" && t <= 0) {
        this.reset();
        t = 0;
      }

      this.updateUI(t);
      this.save();

    }, 250);
  },

  // -------------------------
  // FORMAT
  // -------------------------
  format(ms) {
    const total = Math.max(0, Math.floor(ms / 1000));

    const h = String(Math.floor(total / 3600)).padStart(2, "0");
    const m = String(Math.floor((total % 3600) / 60)).padStart(2, "0");
    const s = String(total % 60).padStart(2, "0");

    return `${h}:${m}:${s}`;
  },

  // -------------------------
  // UI
  // -------------------------
  createWidget() {

    if (document.getElementById("evap-mini-timer")) return;

    const el = document.createElement("div");
    el.id = "evap-mini-timer";

    el.style.cssText = `
      position: fixed;
      bottom: 20px;
      right: 20px;
      background: rgba(255,255,255,0.95);
      border: 1px solid #F472B6;
      color: #EC4899;
      padding: 10px 14px;
      border-radius: 14px;
      font-weight: 600;
      font-family: Poppins, sans-serif;
      z-index: 999999;
      cursor: pointer;
      backdrop-filter: blur(10px);
      display: none;
    `;

    el.onclick = () => {
      this.pause();
    };

    document.body.appendChild(el);
    this.widget = el;
  },

  updateUI(ms) {
    if (!this.widget) return;

    const txt = this.format(ms);
    this.widget.innerText = txt;

    // visible si actif OU si temps existe
    const shouldShow = this.running || this.elapsed > 0;

    this.widget.style.display = shouldShow ? "block" : "none";
  },

  // -------------------------
  // CONTROLS (OPTIONAL HOOKS)
  // -------------------------
  startStopwatch() {
    this.mode = "stopwatch";
    this.running = true;
    this.startTime = Date.now() - this.elapsed;
    this.save();
  },

  pause() {
    if (!this.running) return;

    this.elapsed = this.getTime();
    this.running = false;

    this.save();
  },

  reset() {
    this.running = false;
    this.startTime = null;
    this.elapsed = 0;
    this.duration = 0;

    this.save();
    this.updateUI(0);
  }
};

// =========================
// AUTO START EVERY PAGE
// =========================
window.addEventListener("load", () => {
  EvapTimer.init();
});
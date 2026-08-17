// =========================
// EVAP GLOBAL TIMER (persistant entre les pages)
// Source unique de vérité : la page /timer/ et le mini-widget flottant
// pilotent tous les deux cet objet plutôt que d'avoir chacun leur propre
// horloge (c'était le cas avant et ça pouvait désynchroniser l'affichage).
// =========================

const EvapTimer = {

  mode: "stopwatch",
  running: false,

  startTime: null,
  elapsed: 0,
  duration: 0,

  interval: null,
  widget: null,
  listeners: [],

  // -------------------------
  // INIT
  // -------------------------
  init() {
    this.load();
    this.createWidget();
    this.loop();
    this.updateUI(this.getTime());
  },

  // -------------------------
  // SUBSCRIBE (used by the /timer/ page to sync its own display/buttons)
  // -------------------------
  subscribe(fn) {
    this.listeners.push(fn);
    fn(this.getTime());
    return () => {
      this.listeners = this.listeners.filter(l => l !== fn);
    };
  },

  notify(ms) {
    this.listeners.forEach(fn => fn(ms));
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

    return this.elapsed;
  },

  // -------------------------
  // LOOP
  // -------------------------
  loop() {
    this.interval = setInterval(() => {
      let t = this.getTime();

      if (this.running && this.mode === "countdown" && t <= 0) {
        this.reset();
        t = 0;
      }

      this.updateUI(t);
      this.notify(t);

      if (this.running) this.save();

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
  // CONTROLS
  // -------------------------
  setMode(mode) {
    this.reset();
    this.mode = mode;
    this.save();
  },

  start(countdownSeconds) {
    if (this.running) return;
    this.running = true;

    if (this.mode === "countdown") {
      if (typeof countdownSeconds === "number") {
        this.duration = countdownSeconds * 1000;
      } else {
        // Reprise après pause (aucune durée fournie) : "elapsed" contient le
        // temps RESTANT au moment de la pause (cf. pause() plus bas) - il
        // devient la nouvelle durée à décompter à partir de maintenant.
        // Sans ce cas, une reprise repartait de la durée totale d'origine.
        this.duration = this.elapsed;
      }
      this.startTime = Date.now();
    } else {
      this.startTime = Date.now() - this.elapsed;
    }

    this.save();
    this.updateUI(this.getTime());
  },

  pause() {
    if (!this.running) return;

    this.elapsed = this.getTime();
    this.running = false;

    this.save();
    this.updateUI(this.elapsed);
  },

  reset() {
    this.running = false;
    this.startTime = null;
    this.elapsed = 0;
    this.duration = 0;

    this.save();
    this.updateUI(0);
    this.notify(0);
  },

  // -------------------------
  // MINI WIDGET UI
  // -------------------------
  createWidget() {
    if (document.getElementById("evap-mini-timer")) {
      this.widget = document.getElementById("evap-mini-timer");
      return;
    }

    const el = document.createElement("div");
    el.id = "evap-mini-timer";
    el.title = "Cliquer pour mettre en pause";

    el.onclick = () => this.pause();

    document.body.appendChild(el);
    this.widget = el;
  },

  updateUI(ms) {
    if (!this.widget) return;

    const txt = this.format(ms);
    this.widget.innerText = txt;

    const shouldShow = this.running || this.elapsed > 0;
    this.widget.style.display = shouldShow ? "block" : "none";
  }
};

// =========================
// AUTO START EVERY PAGE
// This script tag is placed at the end of <body> (before page-specific
// scripts), so the DOM is already ready - no need to wait for "load".
// Running synchronously means EvapTimer's persisted state (mode/running/...)
// is available immediately to any script that loads after this one.
// =========================
EvapTimer.init();

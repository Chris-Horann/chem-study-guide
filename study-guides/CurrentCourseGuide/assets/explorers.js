/* Interactive explorers for the CurrentCourseGuide study guide.
   Classic script: window.Explorers = { calc, mount }. In node, module.exports gives the pure calc functions
   (tested by verification/CurrentCourseGuide/test_explorers.js). Every plotted value is computed from the
   course constants in data.js; nothing is hand-placed. */
(function (root, factory) {
  if (typeof module === "object" && module.exports) module.exports = factory();
  else root.Explorers = factory();
})(typeof self !== "undefined" ? self : this, function () {
  "use strict";

  /* ================================================================ constants (course values) */
  var K = { c: 2.998e8, h: 6.626e-34, bohr: 2.178e-18, coul: 2.31e-19, balmer: 364.56, NA: 6.022e23, kB: 1.380649e-23, me: 9.109e-31 };
  function useData(D) {
    if (!D || !D.constants) return;
    K.c = D.constants.c.value; K.h = D.constants.h.value; K.bohr = D.constants.bohr.value;
    K.coul = D.constants.coulomb.value; K.balmer = D.constants.balmer.value; K.NA = D.constants.NA.value;
    K.kB = D.constants.kB.value; K.me = D.constants.me.value;
  }

  /* ================================================================ pure calculations */
  var calc = {
    photonFromNm: function (nm) { var lam = nm * 1e-9; return { E: K.h * K.c / lam, nu: K.c / lam }; },
    nmFromE: function (E) { return K.h * K.c / E * 1e9; },
    bohrE: function (n) { return n === Infinity ? 0 : -K.bohr / (n * n); },
    bohrDE: function (ni, nf) {
      var inv = function (n) { return n === Infinity ? 0 : 1 / (n * n); };
      return -K.bohr * (inv(nf) - inv(ni));
    },
    deBroglie: function (m, u) { return K.h / (m * u); },
    eel: function (q1, q2, dnm) { return K.coul * q1 * q2 / dnm; },
    planck: function (lam, T) { // spectral radiance, W sr^-1 m^-3 (BACKGROUND: Planck's law)
      var a = 2 * K.h * K.c * K.c / Math.pow(lam, 5), x = K.h * K.c / (lam * K.kB * T);
      return x > 700 ? 0 : a / (Math.exp(x) - 1);
    },
    rayleighJeans: function (lam, T) { return 2 * K.c * K.kB * T / Math.pow(lam, 4); },
    planckPeakNm: function (T) { return K.h * K.c / (4.965114231744276 * K.kB * T) * 1e9; }, // exact maximum of Planck's law
    planckPeakNumeric: function (T) { // brute-force check used by the node tests
      var best = 0, bestL = 0;
      for (var nm = 50; nm <= 20000; nm += 0.25) { var v = calc.planck(nm * 1e-9, T); if (v > best) { best = v; bestL = nm; } }
      return bestL;
    },
    region: function (lam) { // approximate boundaries (BACKGROUND), meters
      if (lam < 1e-11) return "gamma rays";
      if (lam < 1e-8) return "X-rays";
      if (lam < 4.0e-7) return "ultraviolet";
      if (lam <= 7.5e-7) return "visible";
      if (lam < 1e-3) return "infrared";
      if (lam < 1) return "microwave";
      return "radio";
    },
    colorName: function (nm) {
      if (nm < 400 || nm > 750) return "";
      if (nm < 450) return "violet"; if (nm < 495) return "blue"; if (nm < 570) return "green";
      if (nm < 590) return "yellow"; if (nm < 620) return "orange"; return "red";
    },
    seriesName: function (nf) { return nf === 1 ? "Lyman" : nf === 2 ? "Balmer" : nf === 3 ? "Paschen" : ""; },
    balmerNm: function (n) { return K.balmer * n * n / (n * n - 4); },
    unpaired: function (cfg) {
      var cap = { s: 2, p: 6, d: 10, f: 14 }, t = 0;
      cfg.forEach(function (x) { var orb = cap[x[0].slice(-1)] / 2, k = x[1]; t += k <= orb ? k : 2 * orb - k; });
      return t;
    },
    gcd: function (a, b) { return b ? calc.gcd(b, a % b) : a; }
  };

  /* ================================================================ formatting */
  var MINUS = "−";
  function sci(x, sf) {
    sf = sf || 3;
    if (!isFinite(x)) return "—";
    if (x === 0) return "0";
    var e = Math.floor(Math.log10(Math.abs(x))), m = x / Math.pow(10, e), mr = +m.toFixed(sf - 1);
    if (Math.abs(mr) >= 10) { e += 1; mr = +(x / Math.pow(10, e)).toFixed(sf - 1); }
    var s = (x < 0 ? MINUS : "") + Math.abs(mr).toFixed(sf - 1);
    return e === 0 ? s : s + " × 10<sup>" + (e < 0 ? MINUS + (-e) : e) + "</sup>";
  }
  function num(x, sf) {
    sf = sf || 3;
    if (!isFinite(x)) return "—";
    if (x === 0) return "0";
    var e = Math.floor(Math.log10(Math.abs(x))), dec = Math.max(0, sf - 1 - e);
    var r = +x.toPrecision(sf);
    var s = Math.abs(r).toLocaleString("en-US", { minimumFractionDigits: dec, maximumFractionDigits: dec });
    return (r < 0 ? MINUS : "") + s;
  }
  function fix(x, d) { return (x < 0 ? MINUS : "") + Math.abs(x).toFixed(d); }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  // plain-text notation for places that can't hold markup (<option> labels, title tooltips)
  var SUPS = { "0": "⁰", "1": "¹", "2": "²", "3": "³", "4": "⁴", "5": "⁵", "6": "⁶", "7": "⁷", "8": "⁸", "9": "⁹", "+": "⁺", "−": "⁻", "-": "⁻" };
  var SUBS = { "0": "₀", "1": "₁", "2": "₂", "3": "₃", "4": "₄", "5": "₅", "6": "₆", "7": "₇", "8": "₈", "9": "₉" };
  function uniSup(s) { return String(s).replace(/[0-9+\-−]/g, function (c) { return SUPS[c]; }); }
  function formulaText(f) { return String(f).replace(/([A-Za-z)])(\d+)/g, function (_, a, d) { return a + d.replace(/\d/g, function (c) { return SUBS[c]; }); }); }
  function ionText(sym, q) { var a = Math.abs(q); return q ? sym + uniSup((a === 1 ? "" : a) + (q > 0 ? "+" : "−")) : sym; }
  function signed(x) { return x < 0 ? MINUS + (-x) : String(x); }
  function ion(sym, q) { // HTML ion notation, magnitude then sign
    if (!q) return sym;
    var a = Math.abs(q);
    return sym + "<sup>" + (a === 1 ? "" : a) + (q > 0 ? "+" : MINUS) + "</sup>";
  }
  function formulaHTML(parts) { // [[sym, count], ...]
    return parts.map(function (p) { return p[0] + (p[1] > 1 ? "<sub>" + p[1] + "</sub>" : ""); }).join("");
  }
  function sciSVG(x, sf, unit) { // superscripts as tspans for SVG text
    var h = sci(x, sf), m = h.match(/^(.*) × 10<sup>(.*)<\/sup>$/);
    if (!m) return h + (unit ? " " + unit : "");
    return m[1] + " × 10<tspan class='sup' dy='-6'>" + m[2] + "</tspan><tspan dy='6'>" + (unit ? " " + unit : "\u200b") + "</tspan>";
  }
  function ionSVG(sym, q) {
    if (!q) return sym;
    var a = Math.abs(q);
    return sym + "<tspan class='sup' dy='-6'>" + (a === 1 ? "" : a) + (q > 0 ? "+" : MINUS) + "</tspan><tspan dy='6'>\u200b</tspan>";
  }
  function cfgHTML(cfg) { return cfg.map(function (x) { return x[0] + "<sup>" + x[1] + "</sup>"; }).join(""); }
  function wavelengthColor(nm) {
    var r = 0, g = 0, b = 0;
    if (nm < 380 || nm > 780) return "#9aa3ad";
    if (nm < 440) { r = -(nm - 440) / 60; b = 1; }
    else if (nm < 490) { g = (nm - 440) / 50; b = 1; }
    else if (nm < 510) { g = 1; b = -(nm - 510) / 20; }
    else if (nm < 580) { r = (nm - 510) / 70; g = 1; }
    else if (nm < 645) { r = 1; g = -(nm - 645) / 65; }
    else { r = 1; }
    var f = nm < 420 ? 0.3 + 0.7 * (nm - 380) / 40 : nm > 700 ? 0.3 + 0.7 * (780 - nm) / 80 : 1;
    function c(x) { return Math.round(255 * Math.pow(Math.max(0, x) * f, 0.8)); }
    return "rgb(" + c(r) + "," + c(g) + "," + c(b) + ")";
  }
  var SERIES = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300"]; // validated categorical order (dataviz)
  var RAMP = ["#cde2fb", "#b7d3f6", "#9ec5f4", "#86b6ef", "#6da7ec", "#5598e7", "#3987e5", "#2a78d6", "#256abf", "#1c5cab", "#184f95", "#104281", "#0d366b"];
  var DIV_NEG = ["#0d366b", "#184f95", "#256abf", "#3987e5", "#6da7ec", "#9ec5f4", "#cde2fb"]; // strong negative -> weak
  var DIV_MID = "#f0efec";
  var DIV_POS = ["#f7d4cf", "#eaa39a", "#d9665c"];
  function rampColor(t) { t = Math.max(0, Math.min(1, t)); return RAMP[Math.round(t * (RAMP.length - 1))]; }
  function inkOn(hex) {
    var m = hex.match(/^#(..)(..)(..)$/); if (!m) return "#17212E";
    var l = [m[1], m[2], m[3]].map(function (x) { var v = parseInt(x, 16) / 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); });
    var L = 0.2126 * l[0] + 0.7152 * l[1] + 0.0722 * l[2];
    return L > 0.35 ? "#17212E" : "#FFFFFF";
  }
  var reduceMotion = typeof window !== "undefined" && window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ================================================================ DOM helpers (browser only) */
  function el(tag, attrs, html) {
    var e = document.createElement(tag);
    if (attrs) for (var k in attrs) {
      if (attrs[k] === null || attrs[k] === undefined || attrs[k] === false) continue;
      if (k === "class") e.className = attrs[k]; else e.setAttribute(k, attrs[k] === true ? "" : attrs[k]);
    }
    if (html !== undefined) e.innerHTML = html;
    return e;
  }
  function shell(host, opts) {
    host.innerHTML = "";
    host.classList.add("xp");
    var title = el("h3", { class: "xp-title" }, opts.title);
    var intro = opts.intro ? el("p", { class: "xp-intro" }, opts.intro) : null;
    var controls = el("div", { class: "xp-controls" });
    var presets = el("div", { class: "xp-presets", role: "group", "aria-label": "Presets" });
    var view = el("div", { class: "xp-view" });
    var readout = el("p", { class: "xp-readout", "aria-live": "polite" });
    var kv = el("dl", { class: "xp-kv" });
    var table = el("details", { class: "xp-table" }, "<summary>Show the values as a table</summary><div class='table-wrap'></div>");
    var src = el("p", { class: "source" }, opts.source || "");
    host.appendChild(title);
    if (intro) host.appendChild(intro);
    var grid = el("div", { class: "xp-grid" });
    var side = el("div", { class: "xp-side" });
    side.appendChild(controls); side.appendChild(presets);
    grid.appendChild(side); grid.appendChild(view);
    host.appendChild(grid);
    host.appendChild(readout); host.appendChild(kv); host.appendChild(table); host.appendChild(src);
    return { host: host, controls: controls, presets: presets, view: view, readout: readout, kv: kv, table: table.querySelector(".table-wrap"), details: table };
  }
  function slider(parent, o) {
    var id = "sl-" + o.testid;
    var wrap = el("div", { class: "ctl ctl-slider" });
    var lab = el("label", { for: id }, o.label + " <output class='ctl-val' id='" + id + "-out'></output>");
    var inp = el("input", { type: "range", id: id, min: o.min, max: o.max, step: o.step, value: o.value, "data-testid": "slider-" + o.testid });
    wrap.appendChild(lab); wrap.appendChild(inp);
    parent.appendChild(wrap);
    var out = lab.querySelector("output");
    // show(v): label the exact value a preset or typed entry set, not the slider's step-rounded position
    function show(v) { var x = v === undefined ? parseFloat(inp.value) : v; out.innerHTML = o.format ? o.format(x) : String(x); inp.setAttribute("aria-valuetext", out.textContent); }
    inp.addEventListener("input", function () { show(); o.onInput(parseFloat(inp.value)); });
    show(o.value);
    return { input: inp, set: function (v) { inp.value = v; show(v); }, get: function () { return parseFloat(inp.value); } };
  }
  function select(parent, o) {
    var id = "se-" + o.testid;
    var wrap = el("div", { class: "ctl ctl-select" });
    wrap.appendChild(el("label", { for: id }, o.label));
    var s = el("select", { id: id, "data-testid": "select-" + o.testid });
    o.options.forEach(function (op) { var x = el("option", { value: op[0] }); x.textContent = op[1]; s.appendChild(x); });
    s.value = o.value;
    s.addEventListener("change", function () { o.onChange(s.value); });
    wrap.appendChild(s); parent.appendChild(wrap);
    return s;
  }
  function checkbox(parent, o) {
    var id = "cb-" + o.testid;
    var wrap = el("div", { class: "ctl ctl-check" });
    var c = el("input", { type: "checkbox", id: id, "data-testid": "toggle-" + o.testid });
    c.checked = !!o.value;
    c.addEventListener("change", function () { o.onChange(c.checked); });
    wrap.appendChild(c); wrap.appendChild(el("label", { for: id }, o.label));
    parent.appendChild(wrap);
    return c;
  }
  function radios(parent, o) {
    var fs = el("fieldset", { class: "ctl ctl-radios" });
    fs.appendChild(el("legend", null, o.label));
    var name = "rg-" + o.testid;
    o.options.forEach(function (op, i) {
      var id = name + "-" + i;
      var r = el("input", { type: "radio", name: name, id: id, value: op[0], "data-testid": "radio-" + o.testid + "-" + op[0] });
      if (op[0] === o.value) r.checked = true;
      r.addEventListener("change", function () { if (r.checked) o.onChange(op[0]); });
      var lab = el("label", { for: id, class: "radio" });
      lab.appendChild(r); lab.appendChild(document.createTextNode(" "));
      lab.appendChild(el("span", null, op[1]));
      fs.appendChild(lab);
    });
    parent.appendChild(fs);
    return { set: function (v) { var x = fs.querySelector("input[value='" + v + "']"); if (x) x.checked = true; } };
  }
  function button(parent, label, testid, onClick, cls) {
    var b = el("button", { type: "button", class: "btn " + (cls || "btn-small"), "data-testid": testid }, label);
    b.addEventListener("click", onClick);
    parent.appendChild(b);
    return b;
  }
  function presetButtons(ui, name, list, apply) {
    if (!list.length) return;
    ui.presets.appendChild(el("p", { class: "xp-presets-label" }, "Try"));
    list.forEach(function (p, i) { button(ui.presets, p[0], "preset-" + name + "-" + i, function () { apply(p[1]); }); });
  }
  function kvSet(dl, rows) {
    dl.innerHTML = rows.map(function (r) { return "<div><dt>" + r[0] + "</dt><dd>" + r[1] + "</dd></div>"; }).join("");
  }
  function tableHTML(head, rows) {
    return "<table><thead><tr>" + head.map(function (x) { return "<th scope='col'>" + x + "</th>"; }).join("") + "</tr></thead><tbody>" +
      rows.map(function (r) { return "<tr>" + r.map(function (x) { return "<td>" + x + "</td>"; }).join("") + "</tr>"; }).join("") + "</tbody></table>";
  }
  function svgWrap(w, hgt, label, inner) {
    return "<svg viewBox='0 0 " + w + " " + hgt + "' role='img' aria-label='" + esc(label) + "' preserveAspectRatio='xMidYMid meet'>" + inner + "</svg>";
  }
  function linePath(pts) {
    return pts.map(function (p, i) { return (i ? "L" : "M") + p[0].toFixed(1) + " " + p[1].toFixed(1); }).join("");
  }
  /* chart frame: returns scale functions and axis markup */
  function frame(o) {
    var W = o.w, Hh = o.h, m = o.m || { l: 56, r: 16, t: 14, b: 40 };
    var pw = W - m.l - m.r, ph = Hh - m.t - m.b;
    var xs = o.xlog ? function (v) { return m.l + (Math.log10(v) - Math.log10(o.x0)) / (Math.log10(o.x1) - Math.log10(o.x0)) * pw; }
      : function (v) { return m.l + (v - o.x0) / (o.x1 - o.x0) * pw; };
    var ys = o.ylog ? function (v) { return m.t + ph - (Math.log10(v) - Math.log10(o.y0)) / (Math.log10(o.y1) - Math.log10(o.y0)) * ph; }
      : function (v) { return m.t + ph - (v - o.y0) / (o.y1 - o.y0) * ph; };
    var g = "<g class='axis'>";
    (o.yticks || []).forEach(function (t) {
      var y = ys(t[0]);
      g += "<line class='grid' x1='" + m.l + "' x2='" + (m.l + pw) + "' y1='" + y + "' y2='" + y + "'/>" +
        "<text class='tick' x='" + (m.l - 6) + "' y='" + (y + 4) + "' text-anchor='end'>" + t[1] + "</text>";
    });
    (o.xticks || []).forEach(function (t) {
      var x = xs(t[0]);
      g += "<line class='tickmark' x1='" + x + "' x2='" + x + "' y1='" + (m.t + ph) + "' y2='" + (m.t + ph + 4) + "'/>" +
        "<text class='tick' x='" + x + "' y='" + (m.t + ph + 17) + "' text-anchor='middle'>" + t[1] + "</text>";
    });
    g += "<line class='baseline' x1='" + m.l + "' x2='" + (m.l + pw) + "' y1='" + (m.t + ph) + "' y2='" + (m.t + ph) + "'/>";
    if (o.xlabel) g += "<text class='axis-label' x='" + (m.l + pw / 2) + "' y='" + (Hh - 4) + "' text-anchor='middle'>" + o.xlabel + "</text>";
    if (o.ylabel) g += "<text class='axis-label' transform='translate(12 " + (m.t + ph / 2) + ") rotate(-90)' text-anchor='middle'>" + o.ylabel + "</text>";
    g += "</g>";
    return { xs: xs, ys: ys, axes: g, m: m, pw: pw, ph: ph, W: W, H: Hh };
  }
  /* hover layer: crosshair + tooltip, driven by a function that returns HTML for an x position */
  function hoverLayer(container, svg, f, invX, htmlAt) {
    var tip = el("div", { class: "xp-tip", hidden: true, role: "presentation" });
    container.style.position = "relative";
    container.appendChild(tip);
    var ns = "http://www.w3.org/2000/svg";
    var cross = document.createElementNS(ns, "line");
    cross.setAttribute("class", "crosshair"); cross.setAttribute("y1", f.m.t); cross.setAttribute("y2", f.m.t + f.ph);
    cross.style.display = "none";
    svg.appendChild(cross);
    function move(clientX, clientY) {
      var rect = svg.getBoundingClientRect();
      var sx = (clientX - rect.left) / rect.width * f.W;
      if (sx < f.m.l || sx > f.m.l + f.pw) { hide(); return; }
      var xv = invX(sx), html = htmlAt(xv);
      if (!html) { hide(); return; }
      cross.setAttribute("x1", sx); cross.setAttribute("x2", sx); cross.style.display = "";
      tip.innerHTML = html; tip.hidden = false;
      var left = (clientX - rect.left) + 14, top = (clientY - rect.top) - 10;
      if (left + 200 > rect.width) left = (clientX - rect.left) - 200;
      tip.style.left = Math.max(0, left) + "px"; tip.style.top = Math.max(0, top) + "px";
    }
    function hide() { tip.hidden = true; cross.style.display = "none"; }
    svg.addEventListener("pointermove", function (e) { move(e.clientX, e.clientY); });
    svg.addEventListener("pointerleave", hide);
    return { hide: hide };
  }
  function invLinear(f, x0, x1) { return function (sx) { return x0 + (sx - f.m.l) / f.pw * (x1 - x0); }; }

  var mount = {};

  /* ================================================================ m1: multiple proportions */
  mount.massRatios = function (host, D) {
    useData(D);
    var SETS = { // fm = mass of the fixed element in one formula unit; o = mass of O in one unit (same mass scale)
      water: { label: "Water and hydrogen peroxide (Day 1 p.13)", fixed: "H", other: "O", cmpds: [
        { f: [["H", 2], ["O", 1]], name: "water", fm: 2.02, o: 16.00 }, { f: [["H", 2], ["O", 2]], name: "hydrogen peroxide", fm: 2.02, o: 32.00 }], src: "Day 1 p.11, p.13" },
      carbon: { label: "Two oxides of carbon (background)", fixed: "C", other: "O", cmpds: [
        { f: [["C", 1], ["O", 1]], name: "", fm: 12.01, o: 16.00 }, { f: [["C", 1], ["O", 2]], name: "", fm: 12.01, o: 32.00 }], src: "Background (atomic masses C 12.01, O 16.00)" },
      sulfur: { label: "Two oxides of sulfur (textbook §1.1)", fixed: "S", other: "O", cmpds: [
        { f: [["S", 1], ["O", 2]], name: "", fm: 32.07, o: 32.00 }, { f: [["S", 1], ["O", 3]], name: "", fm: 32.07, o: 48.00 }], src: "textbook §1.1, PDF p.41; atomic masses are background values" },
      nitrogen: { label: "Three oxides of nitrogen (background)", fixed: "N", other: "O", cmpds: [
        { f: [["N", 2], ["O", 1]], name: "", fm: 28.02, o: 16.00 }, { f: [["N", 1], ["O", 1]], name: "", fm: 14.01, o: 16.00 },
        { f: [["N", 1], ["O", 2]], name: "", fm: 14.01, o: 32.00 }], src: "Background (atomic masses N 14.01, O 16.00)" }
    };
    var st = { set: "water", mass: 1.01 };
    var ui = shell(host, { title: "Explorer: fix one element's mass, compare the other",
      intro: "Choose a pair of compounds made of the same two elements, then change the sample size. Watch which number changes and which never does.",
      source: "Source: Day 1 p.11–14. Atomic masses for the non-lecture sets are background values." });
    select(ui.controls, { label: "Compounds", testid: "ratio-set", value: st.set, options: Object.keys(SETS).map(function (k) { return [k, SETS[k].label]; }),
      onChange: function (v) { st.set = v; st.mass = SETS[v].fixed === "H" ? 1.01 : 1.00; sl.set(st.mass); draw(); } });
    var sl = slider(ui.controls, { label: "Mass of the fixed element", testid: "ratio-mass", min: 0.1, max: 10, step: 0.01, value: st.mass,
      format: function (v) { return v.toFixed(2) + " g " + SETS[st.set].fixed; }, onInput: function (v) { st.mass = v; draw(); } });
    function draw() {
      var S = SETS[st.set], W = 560, Hh = 230;
      var masses = S.cmpds.map(function (c) { return c.o / c.fm * st.mass; });
      var maxM = Math.max.apply(null, masses) * 1.15;
      var bw = 24, gap = (W - 180) / S.cmpds.length;
      var svg = "", x0 = 150;
      svg += "<text class='tick' x='8' y='20'>Mass of " + S.other + " combined with " + st.mass.toFixed(2) + " g " + S.fixed + "</text>";
      S.cmpds.forEach(function (c, i) {
        var x = x0 + i * gap + gap / 2 - bw / 2, hgt = masses[i] / maxM * 150, y = 190 - hgt;
        svg += "<path class='bar' d='M" + x + " 190 V" + (y + 4) + " q0 -4 4 -4 h" + (bw - 8) + " q4 0 4 4 V190 Z' fill='" + SERIES[0] + "'/>";
        svg += "<text class='val' x='" + (x + bw / 2) + "' y='" + (y - 6) + "' text-anchor='middle'>" + masses[i].toFixed(2) + " g</text>";
        svg += "<text class='tick' x='" + (x + bw / 2) + "' y='208' text-anchor='middle'>" + formulaSVG(c.f) + "</text>";
        if (c.name) svg += "<text class='tick muted' x='" + (x + bw / 2) + "' y='224' text-anchor='middle'>" + c.name + "</text>";
        // particle picture: one formula unit
        var px = 20, py = 50 + i * 55;
        svg += "<text class='tick' x='" + px + "' y='" + (py - 10) + "'>" + formulaSVG(c.f) + "</text>";
        var k = 0;
        c.f.forEach(function (part) {
          for (var j = 0; j < part[1]; j++) {
            var isFixed = part[0] === S.fixed, r = isFixed ? 8 : 10;
            svg += "<circle cx='" + (px + 10 + k * 19) + "' cy='" + (py + 6) + "' r='" + r + "' class='" + (isFixed ? "atom-a" : "atom-b") + "'/>" +
              "<text class='atom-label' x='" + (px + 10 + k * 19) + "' y='" + (py + 10) + "' text-anchor='middle'>" + part[0] + "</text>";
            k++;
          }
        });
      });
      svg += "<line class='baseline' x1='140' x2='" + (W - 10) + "' y1='190' y2='190'/>";
      ui.view.innerHTML = svgWrap(W, Hh, "Bar chart of oxygen mass per fixed mass of " + S.fixed + " for each compound, with one formula unit drawn for each.", svg);
      var base = masses[0], ratios = masses.map(function (m) { return (m / base).toFixed(2); });
      ui.readout.innerHTML = "With " + st.mass.toFixed(2) + " g of " + S.fixed + ": " + S.cmpds.map(function (c, i) { return (c.name || formulaHTML(c.f)) + " holds " + masses[i].toFixed(2) + " g " + S.other; }).join("; ") +
        ". Ratio " + ratios.join(" : ") + ", the same for every sample size, because every unit of each compound carries a whole number of " + S.other + " atoms.";
      kvSet(ui.kv, [["Fixed element", st.mass.toFixed(2) + " g " + S.fixed], ["Mass ratio", ratios.join(" : ")], ["Data", S.src]]);
      ui.table.innerHTML = tableHTML(["Compound", "g " + S.other + " per " + st.mass.toFixed(2) + " g " + S.fixed, "Ratio to the first"],
        S.cmpds.map(function (c, i) { return [formulaHTML(c.f) + (c.name ? " (" + c.name + ")" : ""), masses[i].toFixed(3), ratios[i]]; }));
    }
    draw();
  };
  function formulaSVG(f) { return f.map(function (p) { return p[0] + (p[1] > 1 ? "<tspan class='sub' dy='3'>" + p[1] + "</tspan><tspan dy='-3'>​</tspan>" : ""); }).join(""); }

  /* ================================================================ m2: alpha scattering */
  mount.alphaScatter = function (host) {
    var st = { model: "nuclear", fired: [], counts: { straight: 0, deflected: 0, back: 0 } };
    var ui = shell(host, { title: "Explorer: fire α particles at gold foil",
      intro: "Pick a model of the atom, then fire α particles. Compare what each model predicts with what Geiger and Marsden saw (Day 2 p.15–18).",
      source: "Source: Day 2 p.14–19. Schematic: the nuclei are drawn far larger than scale so you can see them, and the rate of large deflections is exaggerated." });
    radios(ui.controls, { label: "Model of the atom", testid: "alpha-model", value: st.model,
      options: [["pudding", "Plum pudding (Day 2 p.16)"], ["nuclear", "Nuclear atom (Day 2 p.17)"]],
      onChange: function (v) { st.model = v; clear(); } });
    var btns = el("div", { class: "ctl-row" });
    ui.controls.appendChild(btns);
    button(btns, "Fire 40 α particles", "fire-alpha", function () { fire(40); }, "primary");
    button(btns, "Clear", "btn-alpha-clear", function () { clear(); });
    var W = 600, Hh = 280, foilX = 300;
    function atomsSVG() {
      var s = "<rect x='" + (foilX - 16) + "' y='10' width='32' height='" + (Hh - 20) + "' class='foil'/>";
      for (var i = 0; i < 7; i++) {
        var cy = 30 + i * 37;
        if (st.model === "pudding") {
          s += "<circle cx='" + foilX + "' cy='" + cy + "' r='17' class='pudding'/>";
          for (var k = 0; k < 4; k++) s += "<text class='atom-label' x='" + (foilX - 9 + (k % 2) * 16) + "' y='" + (cy - 3 + Math.floor(k / 2) * 11) + "' text-anchor='middle'>−</text>";
        } else {
          s += "<circle cx='" + foilX + "' cy='" + cy + "' r='17' class='cloud'/><circle cx='" + foilX + "' cy='" + cy + "' r='3' class='nucleus'/>";
        }
      }
      return s;
    }
    function deflection() {
      if (st.model === "pudding") return (Math.random() - 0.5) * 2 * (Math.PI / 180); // below 1 degree
      // Schematic, not Rutherford's formula: the deflection falls off steeply with the distance b from a
      // nucleus, so roughly 90% pass nearly straight, about 9% deflect, and about 1% come back.
      var b = Math.random();                          // impact parameter as a fraction of the atom's radius
      var th = Math.PI * Math.exp(-b / 0.02);
      return (Math.random() < 0.5 ? -1 : 1) * th;
    }
    function fire(n) {
      for (var i = 0; i < n; i++) {
        var y = 20 + Math.random() * (Hh - 40), th = deflection(), a = Math.abs(th) * 180 / Math.PI;
        var cls = a < 2 ? "straight" : a < 90 ? "deflected" : "back";
        st.counts[cls]++;
        st.fired.push({ y: y, th: th, cls: cls });
      }
      if (st.fired.length > 400) st.fired = st.fired.slice(-400);
      draw(true);
    }
    function clear() { st.fired = []; st.counts = { straight: 0, deflected: 0, back: 0 }; draw(false); }
    function draw(animate) {
      var paths = st.fired.map(function (f, i) {
        var len = 320, ex = foilX + Math.cos(f.th) * len, ey = f.y - Math.sin(f.th) * len;
        var d = "M10 " + f.y.toFixed(1) + " L" + foilX + " " + f.y.toFixed(1) + " L" + ex.toFixed(1) + " " + ey.toFixed(1);
        return "<path class='alpha alpha-" + f.cls + (animate && !reduceMotion && i >= st.fired.length - 40 ? " draw" : "") + "' d='" + d + "'/>";
      }).join("");
      var legend = "<g class='legend'><text x='10' y='" + (Hh - 6) + "' class='tick'>α source (left) → foil → screen</text></g>";
      ui.view.innerHTML = svgWrap(W, Hh, "Paths of alpha particles through gold foil under the " + (st.model === "pudding" ? "plum-pudding" : "nuclear") + " model.",
        "<defs><clipPath id='alpha-clip'><rect x='0' y='0' width='" + W + "' height='" + Hh + "'/></clipPath></defs>" + atomsSVG() + "<g clip-path='url(#alpha-clip)'>" + paths + "</g>" + legend);
      var c = st.counts, n = c.straight + c.deflected + c.back;
      ui.readout.innerHTML = n ? (st.model === "pudding" ? "Plum pudding: " : "Nuclear atom: ") + c.straight + " of " + n + " went nearly straight, " + c.deflected + " were deflected, and " + c.back +
        " bounced back. " + (st.model === "pudding" ? "Spread-out positive charge can't turn a heavy α particle around." : "Only the rare α particle aimed almost straight at a tiny nucleus comes back.") :
        "Nothing fired yet.";
      kvSet(ui.kv, [["Nearly straight (under 2°)", String(c.straight)], ["Deflected (2° to 90°)", String(c.deflected)], ["Bounced back (over 90°)", String(c.back)]]);
      ui.table.innerHTML = tableHTML(["Outcome", "Count", "What it means"], [
        ["Nearly straight", c.straight, "mostly empty space"], ["Deflected", c.deflected, "passed near a concentrated charge"], ["Bounced back", c.back, "nearly head-on with a tiny, massive, positive nucleus"]]);
    }
    draw(false);
  };

  /* ================================================================ m3: EM spectrum */
  mount.emSpectrum = function (host, D) {
    useData(D);
    var st = { logl: Math.log10(530e-9) };
    var ui = shell(host, { title: "Explorer: wavelength, frequency, and photon energy",
      intro: "Drag the wavelength across the whole spectrum. λν = c ties wavelength to frequency; E = hν = hc/λ gives the energy of one photon.",
      source: "Source: Day 2 p.29–30; Day 3 p.17; Day 4 p.10. Region boundaries are approximate (background). The wave drawing is schematic, not to scale." });
    var sl = slider(ui.controls, { label: "Wavelength", testid: "em-wavelength", min: -12, max: 1, step: 0.005, value: st.logl,
      format: function (v) { return fmtLen(Math.pow(10, v)); }, onInput: function (v) { st.logl = v; draw(); } });
    var nmIn = el("div", { class: "ctl ctl-num" }, "<label for='em-nm'>Or type λ in nm</label><input id='em-nm' type='text' inputmode='decimal' data-testid='input-em-nm' placeholder='e.g., 486'>");
    ui.controls.appendChild(nmIn);
    nmIn.querySelector("input").addEventListener("change", function (e) {
      var v = parseFloat(String(e.target.value).replace(/,/g, ""));
      if (v > 0) { st.logl = Math.log10(v * 1e-9); sl.set(st.logl); draw(); }
    });
    presetButtons(ui, "em", [["Green, 530 nm", 530e-9], ["Red, 700 nm", 700e-9], ["UV, 250 nm", 250e-9], ["X-ray, 0.10 nm", 1.0e-10],
      ["Microwave oven, 2.45 GHz", K.c / 2.45e9], ["FM radio, 98.5 MHz", K.c / 98.5e6]], function (lam) { st.logl = Math.log10(lam); sl.set(st.logl); draw(); });
    function fmtLen(l) {
      if (l < 1e-9) return num(l * 1e12, 3) + " pm";
      if (l < 1e-6) return num(l * 1e9, 3) + " nm";
      if (l < 1e-3) return num(l * 1e6, 3) + " μm";
      if (l < 1) return num(l * 100, 3) + " cm";
      return num(l, 3) + " m";
    }
    var REG = [["gamma rays", 1e-13, 1e-11], ["X-rays", 1e-11, 1e-8], ["ultraviolet", 1e-8, 4e-7], ["visible", 4e-7, 7.5e-7], ["infrared", 7.5e-7, 1e-3], ["microwave", 1e-3, 1], ["radio", 1, 10]];
    function draw() {
      var lam = Math.pow(10, st.logl), nu = K.c / lam, E = K.h * nu, nm = lam * 1e9, W = 600, Hh = 220;
      var x0 = 20, x1 = 580, lx = function (l) { return x0 + (Math.log10(l) + 13) / 14 * (x1 - x0); };
      var s = "<defs><linearGradient id='vis-grad' x1='0' x2='1'>";
      for (var w = 400; w <= 750; w += 25) s += "<stop offset='" + ((w - 400) / 350).toFixed(3) + "' stop-color='" + wavelengthColor(w) + "'/>";
      s += "</linearGradient></defs>";
      REG.forEach(function (r, i) {
        var a = lx(r[1]), b = lx(r[2]);
        s += "<rect x='" + a + "' y='30' width='" + (b - a) + "' height='34' class='band-reg" + (i % 2 ? " alt" : "") + "'" + (r[0] === "visible" ? " style='fill:url(#vis-grad)'" : "") + "/>";
        if (r[0] !== "visible") s += "<text class='tick' x='" + ((a + b) / 2) + "' y='52' text-anchor='middle'>" + (r[0] === "gamma rays" ? "γ" : r[0] === "ultraviolet" ? "UV" : r[0] === "infrared" ? "IR" : r[0] === "X-rays" ? "X-ray" : r[0]) + "</text>";
      });
      for (var e = -12; e <= 0; e += 2) s += "<text class='tick' x='" + lx(Math.pow(10, e)) + "' y='80' text-anchor='middle'>10<tspan dy='-5' class='sup'>" + (e < 0 ? "−" + (-e) : e) + "</tspan></text>";
      s += "<text class='tick muted' x='20' y='22'>wavelength, m (log scale): shortest, highest energy</text><text class='tick muted' x='580' y='22' text-anchor='end'>longest, lowest energy</text>";
      var mx = lx(lam);
      s += "<line class='marker' x1='" + mx + "' x2='" + mx + "' y1='26' y2='68'/><path class='marker-head' d='M" + (mx - 6) + " 24 h12 l-6 8 z'/>";
      // schematic wave: displayed wavelength grows with log(lambda)
      var disp = 10 + (st.logl + 12) / 13 * 150, pts = [];
      for (var x = 20; x <= 580; x += 2) pts.push([x, 150 + 32 * Math.sin(2 * Math.PI * (x - 20) / disp)]);
      var col = nm >= 380 && nm <= 780 ? wavelengthColor(nm) : "#475467";
      s += "<path d='" + linePath(pts) + "' class='wave' stroke='" + col + "'/>";
      s += "<text class='tick muted' x='20' y='208'>schematic wave: longer λ, fewer crests per second</text>";
      ui.view.innerHTML = svgWrap(W, Hh, "Electromagnetic spectrum with a marker at " + fmtLen(lam) + " in the " + calc.region(lam) + " region.", s);
      var reg = calc.region(lam), cn = calc.colorName(nm);
      ui.readout.innerHTML = "λ = " + fmtLen(lam) + (reg === "visible" ? " (" + cn + " light)" : " (" + reg + ")") + ": ν = c/λ = " + sci(nu) + " s<sup>−1</sup>, and one photon carries E = hν = " + sci(E) + " J." +
        (st.logl > -3 ? " Very low energy per photon." : st.logl < -8 ? " Enough energy per photon to break bonds and ionize atoms." : "");
      kvSet(ui.kv, [["λ", sci(lam) + " m"], ["ν = c/λ", sci(nu) + " s<sup>−1</sup>"], ["E = hν", sci(E) + " J per photon"],
        ["E per mole of photons (uses N<sub>A</sub>, background)", num(E * K.NA / 1000, 3) + " kJ/mol"], ["Region", reg + (cn ? ", " + cn : "")]]);
      ui.table.innerHTML = tableHTML(["Example", "λ", "ν (s<sup>−1</sup>)", "E per photon (J)"],
        [["Green light", "530 nm", sci(K.c / 530e-9), sci(K.h * K.c / 530e-9)], ["UV", "250 nm", sci(K.c / 250e-9), sci(K.h * K.c / 250e-9)],
          ["X-ray", "0.10 nm", sci(K.c / 1e-10), sci(K.h * K.c / 1e-10)], ["Microwave oven", sci(K.c / 2.45e9) + " m", sci(2.45e9), sci(K.h * 2.45e9)],
          ["FM radio", num(K.c / 98.5e6, 3) + " m", sci(98.5e6), sci(K.h * 98.5e6)], ["Current setting", fmtLen(lam), sci(nu), sci(E)]]);
    }
    draw();
  };

  /* ================================================================ m4: line spectra */
  mount.lineSpectrum = function (host, D) {
    useData(D);
    var lines = [3, 4, 5, 6].map(function (n) { return { n: n, nm: calc.balmerNm(n) }; });
    var st = { mode: "emission", labels: true, bohr: false };
    var ui = shell(host, { title: "Explorer: emission, absorption, and continuous spectra",
      intro: "Switch between the three kinds of spectrum. Watch where hydrogen's lines sit in emission and in absorption.",
      source: "Source: Day 2 p.31; Day 3 p.8–10. Line positions are computed from Balmer's formula, λ = 364.56 nm × n²/(n² − 4) (Day 3 p.21)." });
    radios(ui.controls, { label: "What you are looking at", testid: "spectrum-mode", value: st.mode,
      options: [["emission", "Hot hydrogen gas (emission)"], ["absorption", "White light through cold hydrogen (absorption)"], ["continuous", "Glowing hot solid (continuous)"]],
      onChange: function (v) { st.mode = v; draw(); } });
    checkbox(ui.controls, { label: "Label the wavelengths", testid: "spectrum-labels", value: st.labels, onChange: function (v) { st.labels = v; draw(); } });
    checkbox(ui.controls, { label: "Show which drop makes each line (Module 6)", testid: "spectrum-bohr", value: st.bohr, onChange: function (v) { st.bohr = v; draw(); } });
    function draw() {
      var W = 600, Hh = 170, x0 = 20, x1 = 580, lx = function (nm) { return x0 + (nm - 380) / (750 - 380) * (x1 - x0); };
      var s = "<defs><linearGradient id='rainbow' x1='0' x2='1'>";
      for (var w = 380; w <= 750; w += 10) s += "<stop offset='" + ((w - 380) / 370).toFixed(3) + "' stop-color='" + wavelengthColor(w) + "'/>";
      s += "</linearGradient></defs>";
      if (st.mode === "emission") s += "<rect x='" + x0 + "' y='20' width='" + (x1 - x0) + "' height='70' fill='#0E1320'/>";
      else s += "<rect x='" + x0 + "' y='20' width='" + (x1 - x0) + "' height='70' fill='url(#rainbow)'/>";
      if (st.mode !== "continuous") lines.forEach(function (L) {
        var x = lx(L.nm);
        s += st.mode === "emission" ? "<rect x='" + (x - 2) + "' y='20' width='4' height='70' fill='" + wavelengthColor(L.nm) + "'/><rect x='" + (x - 0.75) + "' y='20' width='1.5' height='70' fill='#ffffff' opacity='0.7'/>"
          : "<rect x='" + (x - 2) + "' y='20' width='4' height='70' fill='#0E1320'/>";
        if (st.labels) s += "<text class='tick' x='" + x + "' y='108' text-anchor='middle'>" + L.nm.toFixed(1) + "</text>";
        if (st.bohr) s += "<text class='tick muted' x='" + x + "' y='124' text-anchor='middle'>" + L.n + " → 2</text>";
      });
      [400, 500, 600, 700].forEach(function (t) { s += "<line class='tickmark' x1='" + lx(t) + "' x2='" + lx(t) + "' y1='90' y2='95'/><text class='tick' x='" + lx(t) + "' y='146' text-anchor='middle'>" + t + " nm</text>"; });
      ui.view.innerHTML = svgWrap(W, Hh, st.mode + " spectrum of hydrogen from 380 to 750 nm", s);
      var list = lines.map(function (L) { return L.nm.toFixed(1); }).reverse().join(", ");
      ui.readout.innerHTML = st.mode === "emission" ? "Emission: bright lines on black at " + list + " nm. The atoms give off only these wavelengths." :
        st.mode === "absorption" ? "Absorption: a rainbow with dark gaps at " + list + " nm, exactly where the emission lines were. Cold hydrogen absorbs the same wavelengths hot hydrogen emits (Day 3 p.10)." :
          "Continuous: every visible wavelength is present, with no lines at all, like the glowing metal on Day 3 p.12.";
      kvSet(ui.kv, [["Mode", st.mode], ["Lines shown", st.mode === "continuous" ? "none" : "4 (visible hydrogen lines)"]]);
      ui.table.innerHTML = tableHTML(["Level the electron drops from (to n = 2)", "λ from Balmer's formula (nm)", "Color"],
        lines.map(function (L) { return [L.n, L.nm.toFixed(1), calc.colorName(L.nm)]; }));
    }
    draw();
  };

  /* ================================================================ m5: photoelectric effect */
  mount.photoelectric = function (host, D) {
    useData(D);
    var WF = D.workFunctionE19, metals = ["Cs", "K", "Ca", "Mg", "Hg"], names = { Cs: "cesium", K: "potassium", Ca: "calcium", Mg: "magnesium", Hg: "mercury" };
    var st = { metal: "K", nm: 400, inten: 5 };
    var ui = shell(host, { title: "Explorer: the photoelectric effect",
      intro: "Choose a metal, then change the light's wavelength and brightness. Find the threshold, and test whether brightness can beat it.",
      source: "Source: Day 3 p.18–19 (KE = hν − φ; the five metals and their order). Work-function values are approximate literature values (background); the lecture graph gives only their order." });
    select(ui.controls, { label: "Metal", testid: "pe-metal", value: st.metal, options: metals.map(function (m) { return [m, names[m] + " (φ ≈ " + WF[m].toFixed(2) + " × 10⁻¹⁹ J)"]; }),
      onChange: function (v) { st.metal = v; draw(); } });
    var sl = slider(ui.controls, { label: "Wavelength of the light", testid: "pe-wavelength", min: 100, max: 800, step: 1, value: st.nm,
      format: function (v) { return v + " nm"; }, onInput: function (v) { st.nm = v; draw(); } });
    slider(ui.controls, { label: "Brightness (photons per second, relative)", testid: "pe-intensity", min: 1, max: 10, step: 1, value: st.inten,
      format: function (v) { return v + "×"; }, onInput: function (v) { st.inten = v; draw(); } });
    presetButtons(ui, "pe", [["Violet light on K", ["K", 400]], ["Dim red on K", ["K", 700]], ["UV on Hg", ["Hg", 220]], ["Green on Cs", ["Cs", 530]]],
      function (p) { st.metal = p[0]; st.nm = p[1]; ui.controls.querySelector("select").value = p[0]; sl.set(p[1]); draw(); });
    var tube = el("div", { class: "xp-sub" }), graph = el("div", { class: "xp-sub" });
    ui.view.appendChild(tube); ui.view.appendChild(graph);
    function draw() {
      var ph = calc.photonFromNm(st.nm), phi = WF[st.metal] * 1e-19, KE = ph.E - phi, on = KE > 0;
      var col = st.nm >= 380 && st.nm <= 780 ? wavelengthColor(st.nm) : "#8a7fd1";
      // phototube
      var t = "<rect x='10' y='20' width='280' height='130' rx='60' class='tube'/><rect x='40' y='45' width='14' height='80' class='plate'/>" +
        "<text class='tick' x='47' y='142' text-anchor='middle'>metal (−)</text><rect x='250' y='60' width='8' height='50' class='plate'/><text class='tick' x='254' y='124' text-anchor='middle'>+</text>";
      for (var i = 0; i < st.inten; i++) t += "<line x1='" + (150 + i * 4) + "' y1='0' x2='" + (56) + "' y2='" + (60 + i * 5) + "' class='ray' stroke='" + col + "'/>";
      if (on) {
        var sp = Math.min(1, Math.sqrt(KE / 8e-19));
        for (var j = 0; j < st.inten; j++) {
          var y = 55 + j * 7, len = 40 + 140 * sp;
          t += "<line x1='58' y1='" + y + "' x2='" + (58 + len) + "' y2='" + y + "' class='e-path'/><circle cx='" + (58 + len) + "' cy='" + y + "' r='3.5' class='electron'/>";
        }
      }
      t += "<text class='tick' x='150' y='172' text-anchor='middle'>" + (on ? "current flows" : "no current") + "</text>";
      tube.innerHTML = svgWrap(300, 180, "Phototube: " + (on ? "electrons are ejected" : "no electrons are ejected"), t);
      // KE vs frequency
      var f = frame({ w: 360, h: 230, x0: 0, x1: 2.0e15, y0: 0, y1: 8, m: { l: 44, r: 44, t: 12, b: 40 },
        xticks: [[0, "0"], [5e14, "0.5"], [1e15, "1.0"], [1.5e15, "1.5"], [2e15, "2.0"]], yticks: [[0, "0"], [2, "2"], [4, "4"], [6, "6"], [8, "8"]],
        xlabel: "frequency ν (10¹⁵ s⁻¹)", ylabel: "max KE (10⁻¹⁹ J)" });
      var g = f.axes;
      metals.forEach(function (m) {
        var nu0 = WF[m] * 1e-19 / K.h, nu1 = 2.0e15, k1 = (K.h * nu1 - WF[m] * 1e-19) / 1e-19;
        var sel = m === st.metal;
        g += "<line x1='" + f.xs(nu0) + "' y1='" + f.ys(0) + "' x2='" + f.xs(nu1) + "' y2='" + f.ys(Math.min(8, k1)) + "' class='" + (sel ? "series-line" : "series-muted") + "'" + (sel ? " stroke='" + SERIES[0] + "'" : "") + "/>";
        var nuTop = (8e-19 + WF[m] * 1e-19) / K.h;
        var lx = Math.min(f.xs(nuTop), f.xs(nu1)), ly = f.ys(Math.min(8, k1));
        g += "<text class='direct-label" + (sel ? " strong" : "") + "' x='" + (lx + 3) + "' y='" + (ly + (nuTop < nu1 ? 10 : 4)) + "'>" + m + "</text>";
      });
      var nu = ph.nu;
      if (nu <= 2e15) {
        g += "<line class='marker' x1='" + f.xs(nu) + "' x2='" + f.xs(nu) + "' y1='" + f.ys(0) + "' y2='" + f.ys(8) + "'/>";
        if (on) g += "<circle cx='" + f.xs(nu) + "' cy='" + f.ys(Math.min(8, KE / 1e-19)) + "' r='5' class='dot' fill='" + SERIES[0] + "'/>";
      }
      graph.innerHTML = svgWrap(360, 230, "Maximum kinetic energy versus frequency: five parallel lines, one per metal; the selected metal is " + names[st.metal] + ".", g);
      var svg = graph.querySelector("svg");
      hoverLayer(graph, svg, f, invLinear(f, 0, 2e15), function (x) {
        var k = (K.h * x - phi) / 1e-19;
        return "ν = " + sci(x) + " s<sup>−1</sup><br>" + names[st.metal] + ": " + (k > 0 ? "KE = " + k.toFixed(2) + " × 10<sup>−19</sup> J" : "below threshold, no electrons");
      });
      var nu0 = phi / K.h, lam0 = K.c / nu0 * 1e9;
      ui.readout.innerHTML = "Each " + st.nm + " nm photon carries " + sci(ph.E) + " J; " + names[st.metal] + "'s threshold is φ ≈ " + sci(phi) + " J. " +
        (on ? "So electrons leave with KE up to " + sci(KE) + " J. Doubling the brightness doubles the number of electrons, not their energy."
          : "That's below threshold: no electrons, however bright the light. Wavelengths shorter than " + num(lam0, 3) + " nm are needed.");
      kvSet(ui.kv, [["Photon energy hν", sci(ph.E) + " J"], ["Work function φ (background value)", sci(phi) + " J"], ["KE = hν − φ", on ? sci(KE) + " J" : "none: hν < φ"],
        ["Threshold ν₀ = φ/h", sci(nu0) + " s<sup>−1</sup> (λ₀ = " + num(lam0, 3) + " nm)"], ["Electrons per second (relative)", on ? String(st.inten) : "0"]]);
      ui.table.innerHTML = tableHTML(["Metal", "φ (10<sup>−19</sup> J, background)", "ν₀ (s<sup>−1</sup>)", "Longest λ that works (nm)"],
        metals.map(function (m) { var n0 = WF[m] * 1e-19 / K.h; return [names[m], WF[m].toFixed(2), sci(n0), num(K.c / n0 * 1e9, 3)]; }));
    }
    draw();
  };

  /* ================================================================ m5: blackbody */
  mount.blackbody = function (host, D) {
    useData(D);
    var st = { T: 5000, compare: true, classical: false };
    var ui = shell(host, { title: "Explorer: blackbody radiation",
      intro: "Heat the object and watch the curve. Where is the peak? What happens to the total brightness?",
      source: "Source: Day 3 p.12–16 (curves for 3000, 4000, 5000 K; the classical curve). Curves computed from Planck's law and the classical formula (background equations, not given in lecture)." });
    var sl = slider(ui.controls, { label: "Temperature", testid: "bb-temperature", min: 1500, max: 7000, step: 50, value: st.T,
      format: function (v) { return v + " K"; }, onInput: function (v) { st.T = v; draw(); } });
    checkbox(ui.controls, { label: "Show the lecture's 3000, 4000, 5000 K curves", testid: "bb-compare", value: st.compare, onChange: function (v) { st.compare = v; draw(); } });
    checkbox(ui.controls, { label: "Show the classical prediction at this temperature", testid: "bb-classical", value: st.classical, onChange: function (v) { st.classical = v; draw(); } });
    presetButtons(ui, "bb", [["Red hot, 1500 K", 1500], ["3000 K", 3000], ["5000 K", 5000], ["White hot, 6000 K", 6000]], function (T) { st.T = T; sl.set(T); draw(); });
    function curve(T) { var pts = []; for (var um = 0.05; um <= 3.0001; um += 0.01) pts.push([um, calc.planck(um * 1e-6, T)]); return pts; }
    function draw() {
      var ref = [3000, 4000, 5000], all = [st.T].concat(st.compare ? ref : []);
      var ymax = Math.max.apply(null, all.map(function (T) { return calc.planck(calc.planckPeakNm(T) * 1e-9, T); })) * 1.12;
      var f = frame({ w: 600, h: 280, x0: 0, x1: 3, y0: 0, y1: ymax, xticks: [[0, "0"], [0.5, "0.5"], [1, "1.0"], [1.5, "1.5"], [2, "2.0"], [2.5, "2.5"], [3, "3.0"]],
        yticks: [[0, "0"], [ymax / 2.24, ""], [ymax / 1.12, ""]], xlabel: "wavelength (μm)", ylabel: "spectral radiance (relative)" });
      var g = "<defs><linearGradient id='bb-vis' x1='0' x2='1'>";
      for (var w = 400; w <= 750; w += 25) g += "<stop offset='" + ((w - 400) / 350).toFixed(3) + "' stop-color='" + wavelengthColor(w) + "'/>";
      g += "</linearGradient></defs><rect x='" + f.xs(0.4) + "' y='" + f.m.t + "' width='" + (f.xs(0.75) - f.xs(0.4)) + "' height='" + f.ph + "' fill='url(#bb-vis)' opacity='0.18'/>" +
        "<text class='tick muted' x='" + f.xs(0.575) + "' y='" + (f.m.t + 12) + "' text-anchor='middle'>visible</text>" + f.axes;
      if (st.compare) ref.forEach(function (T) {
        var pts = curve(T).map(function (p) { return [f.xs(p[0]), f.ys(p[1])]; });
        g += "<path d='" + linePath(pts) + "' class='series-muted'/>";
        var pk = calc.planckPeakNm(T) / 1000;
        g += "<text class='direct-label' x='" + (f.xs(pk) + 4) + "' y='" + (f.ys(calc.planck(pk * 1e-6, T)) - 4) + "'>" + T + " K</text>";
      });
      if (st.classical) {
        var cp = []; for (var um = 0.3; um <= 3; um += 0.01) { var v = calc.rayleighJeans(um * 1e-6, st.T); cp.push([f.xs(um), f.ys(Math.min(v, ymax * 1.5))]); }
        g += "<path d='" + linePath(cp) + "' class='series-line' stroke='" + SERIES[1] + "'/><text class='direct-label' x='" + f.xs(0.9) + "' y='" + (f.m.t + 26) + "'>classical prediction (" + st.T + " K)</text>";
      }
      var main = curve(st.T).map(function (p) { return [f.xs(p[0]), f.ys(Math.min(p[1], ymax * 1.5))]; });
      g += "<path d='" + linePath(main) + "' class='series-line' stroke='" + SERIES[0] + "'/>";
      var peak = calc.planckPeakNm(st.T);
      g += "<circle cx='" + f.xs(peak / 1000) + "' cy='" + f.ys(calc.planck(peak * 1e-9, st.T)) + "' r='5' class='dot' fill='" + SERIES[0] + "'/>" +
        "<text class='direct-label strong' x='" + (f.xs(peak / 1000) + 8) + "' y='" + (f.ys(calc.planck(peak * 1e-9, st.T)) + 4) + "'>" + st.T + " K, peak " + num(peak, 3) + " nm</text>";
      g = "<defs><clipPath id='bb-clip'><rect x='" + f.m.l + "' y='" + f.m.t + "' width='" + f.pw + "' height='" + f.ph + "'/></clipPath></defs>" +
        g.replace(/(<path d='M[^']*' class='series-(?:line|muted)'[^>]*\/>)/g, "<g clip-path='url(#bb-clip)'>$1</g>");
      ui.view.innerHTML = svgWrap(600, 280, "Blackbody curve at " + st.T + " kelvin peaking at " + num(peak, 3) + " nanometers.", g);
      var svg = ui.view.querySelector("svg");
      hoverLayer(ui.view, svg, f, invLinear(f, 0, 3), function (x) {
        if (x <= 0.05) return "";
        var v = calc.planck(x * 1e-6, st.T) / ymax * 1.12;
        return "λ = " + num(x * 1000, 3) + " nm<br>relative radiance at " + st.T + " K: " + v.toFixed(2);
      });
      var region = peak < 400 ? "ultraviolet" : peak <= 750 ? "visible (" + calc.colorName(peak) + ")" : "infrared";
      ui.readout.innerHTML = "At " + st.T + " K the curve peaks near " + num(peak, 3) + " nm, in the " + region + ". Hotter objects peak at shorter wavelengths and are brighter at every wavelength." +
        (st.classical ? " The classical prediction keeps rising at short wavelengths; that failure is what Planck's quanta fixed (Day 3 p.15–17)." : "");
      kvSet(ui.kv, [["Temperature", st.T + " K"], ["Peak wavelength", num(peak, 3) + " nm"], ["Peak region", region]]);
      ui.table.innerHTML = tableHTML(["T (K)", "Peak λ (nm)", "Peak region"], [1500, 3000, 4000, 5000, 6000, 7000].map(function (T) {
        var p = calc.planckPeakNm(T); return [T, num(p, 3), p < 400 ? "UV" : p <= 750 ? "visible" : "infrared"]; }));
    }
    draw();
  };

  /* ================================================================ m6: Bohr energy levels */
  mount.bohr = function (host, D) {
    useData(D);
    var st = { ni: 4, nf: 2 };
    var ui = shell(host, { title: "Explorer: hydrogen's energy levels",
      intro: "Pick a starting and an ending level. The arrow's length is ΔE; the photon carries |ΔE|.",
      source: "Source: Day 4 p.10. ΔE = −2.178 × 10⁻¹⁸ J (1/n_final² − 1/n_initial²); λ = hc/|ΔE|." });
    var opts = [1, 2, 3, 4, 5, 6, 7].map(function (n) { return [String(n), "n = " + n]; });
    var sI = select(ui.controls, { label: "Starting level, n<sub>initial</sub>", testid: "bohr-ni", value: "4", options: opts, onChange: function (v) { st.ni = +v; draw(); } });
    var sF = select(ui.controls, { label: "Ending level, n<sub>final</sub>", testid: "bohr-nf", value: "2", options: opts.concat([["inf", "n = ∞ (ionized)"]]),
      onChange: function (v) { st.nf = v === "inf" ? Infinity : +v; draw(); } });
    presetButtons(ui, "bohr", [["4 → 2 (visible)", [4, 2]], ["3 → 2 (red)", [3, 2]], ["2 → 1 (UV)", [2, 1]], ["4 → 3 (IR)", [4, 3]], ["1 → ∞ (ionize)", [1, Infinity]], ["2 → 5 (absorb)", [2, 5]]],
      function (p) { st.ni = p[0]; st.nf = p[1]; sI.value = String(p[0]); sF.value = p[1] === Infinity ? "inf" : String(p[1]); draw(); });
    function draw() {
      var W = 600, Hh = 330, top = 20, bot = 300, Emin = -2.3e-18;
      var y = function (E) { return top + (E / Emin) * (bot - top); };
      var s = "", levels = [1, 2, 3, 4, 5, 6, 7];
      s += "<line class='baseline' x1='70' x2='70' y1='" + top + "' y2='" + bot + "'/>";
      levels.forEach(function (n) {
        var E = calc.bohrE(n), yy = y(E);
        s += "<line class='level' x1='80' x2='360' y1='" + yy + "' y2='" + yy + "'/>";
        if (n <= 4) s += "<text class='tick' x='366' y='" + (yy + 4) + "'>n = " + n + "   " + fix(E / 1e-18, 3) + " × 10⁻¹⁸ J</text>";
        else if (n === 5) s += "<text class='tick' x='366' y='" + (yy + 10) + "'>n = 5, 6, 7 … crowd together</text>";
      });
      s += "<line class='level ion' x1='80' x2='360' y1='" + y(0) + "' y2='" + y(0) + "'/><text class='tick' x='366' y='" + (y(0) + 4) + "'>n = ∞   0 J (electron removed)</text>";
      s += "<text class='axis-label' transform='translate(40 " + ((top + bot) / 2) + ") rotate(-90)' text-anchor='middle'>energy of the electron (higher is up)</text>";
      var Ei = calc.bohrE(st.ni), Ef = calc.bohrE(st.nf), dE = calc.bohrDE(st.ni, st.nf);
      var nm = dE !== 0 ? calc.nmFromE(Math.abs(dE)) : NaN;
      if (st.ni !== st.nf) {
        var col = nm >= 380 && nm <= 780 ? wavelengthColor(nm) : "#475467", x = 220, y1 = y(Ei), y2 = y(Ef);
        s += "<line x1='" + x + "' x2='" + x + "' y1='" + y1 + "' y2='" + (y2 + (dE < 0 ? -7 : 7)) + "' class='transition' stroke='" + col + "'/>" +
          "<path d='M" + (x - 6) + " " + (y2 + (dE < 0 ? -9 : 9)) + " L" + x + " " + y2 + " L" + (x + 6) + " " + (y2 + (dE < 0 ? -9 : 9)) + "' class='transition-head' stroke='" + col + "'/>";
        var pts = []; for (var t = 0; t <= 60; t++) pts.push([x + 14 + t, (y1 + y2) / 2 + 5 * Math.sin(t / 3)]);
        s += "<path d='" + linePath(pts) + "' class='photon' stroke='" + col + "'/><text class='tick' x='" + (x + 80) + "' y='" + ((y1 + y2) / 2 + 4) + "'>" + (dE < 0 ? "photon out" : "photon in") + "</text>";
      }
      ui.view.innerHTML = svgWrap(W, Hh, "Hydrogen energy-level diagram with an arrow from n = " + st.ni + " to n = " + (st.nf === Infinity ? "infinity" : st.nf) + ".", s);
      var nfTxt = st.nf === Infinity ? "∞" : st.nf;
      if (st.ni === st.nf) { ui.readout.innerHTML = "Same level: no transition, no photon."; kvSet(ui.kv, []); }
      else {
        var reg = calc.region(nm * 1e-9), series = dE < 0 ? calc.seriesName(st.nf) : "";
        ui.readout.innerHTML = "n = " + st.ni + " → " + nfTxt + ": ΔE = " + sci(dE, 4) + " J. " +
          (dE < 0 ? "Negative: the atom loses energy and emits a photon" : "Positive: the atom must absorb a photon") +
          (st.nf === Infinity ? " (this removes the electron: ionization)" : "") + " with λ = hc/|ΔE| = " + num(nm, 4) + " nm (" + reg + (reg === "visible" ? ", " + calc.colorName(nm) : "") + ")" +
          (series ? ", in the " + series + " series" : "") + ".";
        kvSet(ui.kv, [["E(initial)", sci(Ei, 4) + " J"], ["E(final)", st.nf === Infinity ? "0 J" : sci(Ef, 4) + " J"], ["ΔE", sci(dE, 4) + " J"], ["λ", num(nm, 4) + " nm"],
          ["Per mole (× N<sub>A</sub>, background)", num(dE * K.NA / 1000, 4) + " kJ/mol"]]);
      }
      var nfT = st.nf === Infinity ? 2 : st.nf, rows = [];
      for (var n = nfT + 1; n <= 7; n++) { var d = calc.bohrDE(n, nfT), l = calc.nmFromE(-d); rows.push([n + " → " + nfT, sci(d, 4), num(l, 4), calc.region(l * 1e-9)]); }
      ui.table.innerHTML = "<p class='table-note'>Emission lines ending on n = " + nfT + "</p>" + tableHTML(["Transition", "ΔE (J)", "λ (nm)", "Region"], rows);
    }
    draw();
  };

  /* ================================================================ m7: de Broglie + standing waves */
  mount.deBroglie = function (host, D) {
    useData(D);
    var P = { electron: [K.me, "electron"], proton: [1.673e-27, "proton"], neutron: [1.675e-27, "neutron"], alpha: [6.645e-27, "α particle (background mass)"],
      tennis: [0.0570, "tennis ball, 57.0 g"], baseball: [0.142, "baseball, 142 g (Day 4 p.14)"] };
    var st = { p: "electron", logu: Math.log10(4.05e6), n: 3 };
    var ui = shell(host, { title: "Explorer: matter waves",
      intro: "Choose a particle and a speed. Where does its wavelength land compared with the size of an atom?",
      source: "Source: Day 4 p.11–16. λ = h/(mu); landmark sizes from Day 2 p.20 (nucleus ~0.01 pm, gold atom ~288 pm)." });
    var sP = select(ui.controls, { label: "Particle", testid: "db-particle", value: st.p, options: Object.keys(P).map(function (k) { return [k, P[k][1]]; }), onChange: function (v) { st.p = v; draw(); } });
    var sl = slider(ui.controls, { label: "Speed u", testid: "db-speed", min: 0, max: 7.5, step: 0.01, value: st.logu, format: function (v) { return sci(Math.pow(10, v)) + " m/s"; }, onInput: function (v) { st.logu = v; draw(); } });
    presetButtons(ui, "db", [["Electron, 4.05 × 10⁶ m/s (Day 4 p.12)", ["electron", 4.05e6]], ["Baseball, 44.0 m/s (Day 4 p.14)", ["baseball", 44.0]], ["Neutron, 2.20 × 10³ m/s", ["neutron", 2.20e3]]],
      function (p) { st.p = p[0]; st.logu = Math.log10(p[1]); sP.value = p[0]; sl.set(st.logu); draw(); });
    var scale = el("div", { class: "xp-sub" }), ring = el("div", { class: "xp-sub" });
    ui.view.appendChild(scale); ui.view.appendChild(ring);
    var ringCtl = el("div", { class: "xp-ringctl" });
    ui.view.appendChild(ringCtl);
    slider(ringCtl, { label: "Wavelengths around one orbit", testid: "db-ring", min: 1, max: 6, step: 0.25, value: st.n, format: function (v) { return String(v); }, onInput: function (v) { st.n = v; drawRing(); } });
    function draw() {
      var m = P[st.p][0], u = Math.pow(10, st.logu), lam = calc.deBroglie(m, u);
      var marks = [[1e-14, "nucleus ~10⁻¹⁴ m"], [2.88e-10, "gold atom ~288 pm"], [5e-7, "visible light ~500 nm"], [7.4e-2, "baseball ~7 cm"]];
      var x = function (l) { return 30 + (Math.log10(l) + 36) / 36 * 540; };
      var s = "<line class='baseline' x1='30' x2='570' y1='60' y2='60'/>";
      for (var e = -36; e <= 0; e += 6) s += "<line class='tickmark' x1='" + x(Math.pow(10, e)) + "' x2='" + x(Math.pow(10, e)) + "' y1='60' y2='66'/><text class='tick' x='" + x(Math.pow(10, e)) + "' y='80' text-anchor='middle'>10<tspan dy='-5' class='sup'>" + (e < 0 ? "−" + (-e) : e) + "</tspan></text>";
      marks.forEach(function (mk, i) { s += "<line class='landmark' x1='" + x(mk[0]) + "' x2='" + x(mk[0]) + "' y1='40' y2='60'/><text class='tick muted' x='" + x(mk[0]) + "' y='" + (34 - (i % 2) * 12) + "' text-anchor='middle'>" + mk[1] + "</text>"; });
      var lx = Math.max(30, Math.min(570, x(lam)));
      s += "<path class='marker-head' d='M" + (lx - 7) + " 100 h14 l-7 -10 z'/><text class='tick strong' x='" + Math.min(470, Math.max(90, lx)) + "' y='118' text-anchor='middle'>λ = " + sciSVG(lam, 3, "m") + "</text>";
      s += "<text class='tick muted' x='30' y='136'>length, m (log scale)</text>";
      scale.innerHTML = svgWrap(600, 140, "Log scale of lengths with the particle's de Broglie wavelength marked at " + lam.toExponential(2) + " meters.", s);
      var cmp = lam > 1e-11 && lam < 1e-8 ? "about the size of an atom, so this particle behaves as a wave when it meets atoms" :
        lam >= 1e-8 ? "larger than an atom: strongly wavelike on the atomic scale" : lam > 1e-16 ? "smaller than an atom but not by an absurd factor" :
          "unimaginably smaller than the object itself, so its wave nature never shows";
      var pname = P[st.p][1].split(",")[0].replace(/ \(.*/, "");
      ui.readout.innerHTML = (/^[aeiouα]/i.test(pname) ? "An " : "A ") + pname + " at " + sci(u) + " m/s has λ = h/(mu) = " + sci(lam) + " m: " + cmp + ".";
      kvSet(ui.kv, [["m", sci(m, 4) + " kg"], ["u", sci(u) + " m/s"], ["mu (momentum)", sci(m * u) + " kg·m/s"], ["λ = h/(mu)", sci(lam) + " m"]]);
      ui.table.innerHTML = tableHTML(["Example", "m (kg)", "u (m/s)", "λ (m)"], [["Electron (Day 4 p.12)", sci(K.me, 4), sci(4.05e6), sci(calc.deBroglie(K.me, 4.05e6))],
        ["Baseball (Day 4 p.14)", "0.142", "44.0", sci(calc.deBroglie(0.142, 44.0))], ["Thermal neutron", sci(1.675e-27, 4), sci(2.2e3), sci(calc.deBroglie(1.675e-27, 2.2e3))],
        ["Current setting", sci(m, 4), sci(u), sci(lam)]]);
    }
    function drawRing() {
      var R = 70, A = 12, cx = 110, cy = 100, pts = [], n = st.n, whole = Math.abs(n - Math.round(n)) < 1e-9;
      for (var t = 0; t <= 720; t++) { var th = t / 720 * 2 * Math.PI, r = R + A * Math.sin(n * th); pts.push([cx + r * Math.cos(th), cy - r * Math.sin(th)]); }
      var s = "<circle cx='" + cx + "' cy='" + cy + "' r='" + R + "' class='orbit'/><circle cx='" + cx + "' cy='" + cy + "' r='4' class='nucleus'/>" +
        "<path d='" + linePath(pts) + "' class='series-line' stroke='" + (whole ? SERIES[2] : SERIES[1]) + "'/>";
      if (!whole) {
        var endR = R + A * Math.sin(n * 2 * Math.PI);
        s += "<line x1='" + (cx + R) + "' y1='" + cy + "' x2='" + (cx + endR) + "' y2='" + cy + "' class='mismatch'/>";
      }
      s += "<text class='tick strong' x='230' y='80'>" + (whole ? "✓ closes on itself" : "✗ doesn't close") + "</text><text class='tick' x='230' y='100'>" +
        (whole ? "a standing wave: allowed orbit, n = " + n : n + " wavelengths: the wave would cancel itself") + "</text>";
      ring.innerHTML = svgWrap(600, 200, (whole ? "Allowed" : "Forbidden") + " orbit with " + n + " wavelengths around the circumference.", s);
    }
    draw(); drawRing();
  };

  /* ================================================================ m8: quantum numbers */
  mount.quantumNumbers = function (host) {
    var st = { n: 3, l: 2, ml: -2, ms: 0.5 };
    var ui = shell(host, { title: "Explorer: build a set of quantum numbers",
      intro: "Choose any four values, including impossible ones, and see which rule each set passes or breaks.",
      source: "Source: Day 5 p.10–16 (rules and the Top Hat sets); Day 5 p.13 (Table 3.1)." });
    var r = function (a, b) { var o = []; for (var i = a; i <= b; i++) o.push([String(i), String(i).replace("-", "−")]); return o; };
    var sN = select(ui.controls, { label: "n", testid: "qn-n", value: "3", options: r(-3, 5), onChange: function (v) { st.n = +v; draw(); } });
    var sL = select(ui.controls, { label: "ℓ", testid: "qn-l", value: "2", options: r(-2, 5), onChange: function (v) { st.l = +v; draw(); } });
    var sM = select(ui.controls, { label: "m<sub>ℓ</sub>", testid: "qn-ml", value: "-2", options: r(-4, 4), onChange: function (v) { st.ml = +v; draw(); } });
    var sS = select(ui.controls, { label: "m<sub>s</sub>", testid: "qn-ms", value: "0.5", options: [["-1", "−1"], ["-0.5", "−½"], ["0", "0"], ["0.5", "+½"], ["1", "+1"]], onChange: function (v) { st.ms = +v; draw(); } });
    var TOP = [["a (1, 0, −1, +½)", [1, 0, -1, 0.5]], ["b (3, 2, −2, +½)", [3, 2, -2, 0.5]], ["c (2, 2, 0, 0)", [2, 2, 0, 0]], ["d (2, 0, 1, −½)", [2, 0, 1, -0.5]], ["e (−3, −2, −1, −½)", [-3, -2, -1, -0.5]]];
    presetButtons(ui, "qn", TOP.map(function (t) { return ["Top Hat " + t[0], t[1]]; }), function (v) {
      st.n = v[0]; st.l = v[1]; st.ml = v[2]; st.ms = v[3]; sN.value = String(v[0]); sL.value = String(v[1]); sM.value = String(v[2]); sS.value = String(v[3]); draw(); });
    function draw() {
      var rules = [
        [st.n >= 1, "n is a positive integer (1, 2, 3, …)"],
        [st.l >= 0 && st.l <= st.n - 1, "ℓ is between 0 and n − 1" + (st.n >= 1 ? " (here 0 to " + (st.n - 1) + ")" : "")],
        [Math.abs(st.ml) <= st.l && st.l >= 0, "m<sub>ℓ</sub> is between −ℓ and +ℓ" + (st.l >= 0 ? " (here −" + st.l + " to +" + st.l + ")" : "")],
        [Math.abs(st.ms) === 0.5, "m<sub>s</sub> is +½ or −½"]];
      var okAll = rules.every(function (x) { return x[0]; });
      var letter = "spdfgh"[st.l] || "?";
      var html = "<ul class='rules'>" + rules.map(function (x) { return "<li class='" + (x[0] ? "rule-ok" : "rule-no") + "'><span class='rule-icon' aria-hidden='true'>" + (x[0] ? "✓" : "✗") + "</span> " + (x[0] ? "" : "<strong>Breaks:</strong> ") + x[1] + "</li>"; }).join("") + "</ul>";
      if (st.n >= 1 && st.n <= 5) {
        html += "<p class='xp-caption'>The n = " + st.n + " shell (Day 5 p.12–13)</p><div class='shell-rows'>";
        for (var l = 0; l < st.n; l++) {
          html += "<div class='shell-row'><span class='sub-label'>" + st.n + "spdf"[l] + "</span>";
          for (var m = -l; m <= l; m++) {
            var hit = okAll && l === st.l && m === st.ml;
            html += "<span class='obox" + (hit ? " hit" : "") + "' title='mₗ = " + signed(m) + "'>" + (hit ? (st.ms > 0 ? "↑" : "↓") : "") + "<span class='sr-only'>m<sub>ℓ</sub> = " + signed(m) + (hit ? ", this electron" : "") + "</span></span>";
          }
          html += "<span class='sub-count'>" + (2 * l + 1) + " orbital" + (l ? "s" : "") + ", " + 2 * (2 * l + 1) + " e<sup>−</sup></span></div>";
        }
        html += "</div><p class='xp-caption'>Shell total: " + st.n * st.n + " orbitals, " + 2 * st.n * st.n + " electrons.</p>";
      }
      ui.view.innerHTML = html;
      var fmtMs = st.ms === 0.5 ? "+½" : st.ms === -0.5 ? "−½" : String(st.ms).replace("-", "−");
      ui.readout.innerHTML = "(" + [st.n, st.l, st.ml].map(function (v) { return String(v).replace("-", "−"); }).join(", ") + ", " + fmtMs + "): " +
        (okAll ? "allowed. This is a " + st.n + letter + " electron: n = " + st.n + " sets size and energy, ℓ = " + st.l + " gives a " + letter + " shape, and m<sub>ℓ</sub> = " + String(st.ml).replace("-", "−") + " picks one orientation."
          : "not allowed. " + rules.filter(function (x) { return !x[0]; }).length + " rule(s) broken.");
      kvSet(ui.kv, [["Verdict", okAll ? "allowed" : "not allowed"], ["Subshell", okAll ? st.n + letter : "—"]]);
      ui.table.innerHTML = tableHTML(["n", "ℓ values (letters)", "Orbitals in the shell", "Electrons"], [1, 2, 3, 4].map(function (n) {
        var ls = []; for (var l2 = 0; l2 < n; l2++) ls.push(l2 + " (" + "spdf"[l2] + ")"); return [n, ls.join(", "), n * n, 2 * n * n]; }));
    }
    draw();
  };

  /* ================================================================ m9: radial distributions */
  mount.radial = function (host, D) {
    var R = D.radial, names = ["1s", "2s", "2p", "3s", "3p", "3d"];
    var st = { on: { "1s": true, "2s": true, "3s": true }, density: false, rc: 100, rmax: 1000 };
    var ui = shell(host, { title: "Explorer: where is the electron likely to be?",
      intro: "Turn orbitals on and off. Zeros are where the probability vanishes. Move the cutoff radius to measure penetration: how much of each orbital lies close to the nucleus.",
      source: "Source: Day 5 p.17–18; Day 6 p.12, p.18. Curves computed from the exact hydrogen radial functions (background math; a₀ = 52.918 pm). In many-electron atoms the shapes are similar." });
    var boxes = el("fieldset", { class: "ctl ctl-checks" }, "<legend>Orbitals</legend>");
    ui.controls.appendChild(boxes);
    var cbs = {};
    names.forEach(function (nm) { cbs[nm] = checkbox(boxes, { label: nm, testid: "rad-" + nm, value: !!st.on[nm], onChange: function (v) { st.on[nm] = v; draw(); } }); });
    checkbox(ui.controls, { label: "Also show 1s density ψ<sup>2</sup> (Day 5 p.17a, rescaled)", testid: "rad-density", value: false, onChange: function (v) { st.density = v; draw(); } });
    var sl = slider(ui.controls, { label: "Cutoff radius for penetration", testid: "rad-cutoff", min: 10, max: 600, step: 5, value: st.rc, format: function (v) { return v + " pm"; }, onInput: function (v) { st.rc = v; draw(); } });
    function setOn(list) { names.forEach(function (n) { st.on[n] = list.indexOf(n) >= 0; cbs[n].checked = st.on[n]; }); }
    presetButtons(ui, "rad", [["Day 5 p.17: 1s density vs. distribution", "a"], ["Day 5 p.18: 1s, 2s, 3s", "b"], ["Day 6 p.12: 2s vs. 2p", "c"], ["Day 6 p.18: 3s, 3p, 3d", "d"]],
      function (k) {
        st.density = k === "a"; host.querySelector("[data-testid='toggle-rad-density']").checked = st.density;
        setOn(k === "a" ? ["1s"] : k === "b" ? ["1s", "2s", "3s"] : k === "c" ? ["2s", "2p"] : ["3s", "3p", "3d"]);
        st.rc = k === "c" ? 100 : k === "d" ? 200 : 100; sl.set(st.rc); draw();
      });
    function cum(nm, rc) { var ys = R.curves[nm], s = 0, n = Math.min(ys.length - 1, Math.round(rc / R.step)); for (var i = 1; i <= n; i++) s += (ys[i] + ys[i - 1]) / 2 * R.step; return s; }
    function draw() {
      var shown = names.filter(function (n) { return st.on[n]; });
      var rmax = shown.some(function (n) { return n[0] === "3"; }) ? 1000 : shown.some(function (n) { return n[0] === "2"; }) ? 600 : 400;
      var ymax = 0;
      shown.forEach(function (n) { R.curves[n].forEach(function (v, i) { if (i * R.step <= rmax && v > ymax) ymax = v; }); });
      if (!ymax) ymax = 0.012;
      ymax *= 1.15;
      var xt = []; for (var t = 0; t <= rmax; t += rmax > 600 ? 200 : 100) xt.push([t, String(t)]);
      var f = frame({ w: 600, h: 300, x0: 0, x1: rmax, y0: 0, y1: ymax, xticks: xt, yticks: [[0, "0"]], xlabel: "distance from the nucleus, r (pm)", ylabel: "4πr²ψ² (probability per pm)" });
      var g = "<rect x='" + f.m.l + "' y='" + f.m.t + "' width='" + (f.xs(Math.min(st.rc, rmax)) - f.m.l) + "' height='" + f.ph + "' class='cutoff-zone'/>" + f.axes;
      g += "<line class='cutoff' x1='" + f.xs(Math.min(st.rc, rmax)) + "' x2='" + f.xs(Math.min(st.rc, rmax)) + "' y1='" + f.m.t + "' y2='" + (f.m.t + f.ph) + "'/>" +
        "<text class='tick' x='" + (f.xs(Math.min(st.rc, rmax)) + 4) + "' y='" + (f.m.t + 12) + "'>cutoff " + st.rc + " pm</text>";
      if (st.density) {
        var dens = R.curves["1s_density_rel"], dp = [];
        dens.forEach(function (v, i) { var r = i * R.step; if (r <= rmax) dp.push([f.xs(r), f.ys(v * ymax / 1.15)]); });
        g += "<path d='" + linePath(dp) + "' class='series-muted'/><text class='direct-label' x='" + (f.xs(0) + 6) + "' y='" + (f.ys(ymax / 1.15) + 14) + "'>1s density ψ² (rescaled)</text>";
      }
      var legend = [];
      shown.forEach(function (n) {
        var k = names.indexOf(n), col = SERIES[k], pts = [];
        R.curves[n].forEach(function (v, i) { var r = i * R.step; if (r <= rmax) pts.push([f.xs(r), f.ys(v)]); });
        g += "<path d='" + linePath(pts) + "' class='series-line' stroke='" + col + "'/>";
        var ft = R.features[n];
        ft.nodes.forEach(function (r) { if (r <= rmax) g += "<line class='node-line' x1='" + f.xs(r) + "' x2='" + f.xs(r) + "' y1='" + f.ys(0) + "' y2='" + (f.ys(0) - 28) + "'/><circle cx='" + f.xs(r) + "' cy='" + f.ys(0) + "' r='4' class='node-dot' stroke='" + col + "'/>" +
          "<text class='direct-label' x='" + (f.xs(r) + 3) + "' y='" + (f.ys(0) - 31) + "'>" + n + " zero, " + Math.round(r) + " pm</text>"; });
        var pk = ft.peaks[ft.peaks.length - 1], pv = R.curves[n][Math.round(pk / R.step)];
        if (pk <= rmax) g += "<circle cx='" + f.xs(pk) + "' cy='" + f.ys(pv) + "' r='4.5' class='dot' fill='" + col + "'/><text class='direct-label strong' x='" + (f.xs(pk) + 7) + "' y='" + (f.ys(pv) - 6) + "'>" + n + ", " + Math.round(pk) + " pm</text>";
        legend.push("<span class='lg'><span class='lg-sw' style='background:" + col + "'></span>" + n + "</span>");
      });
      ui.view.innerHTML = (shown.length > 1 ? "<div class='legend-row'>" + legend.join("") + "</div>" : "") +
        svgWrap(600, 300, "Radial probability curves for " + (shown.join(", ") || "no orbitals") + ".", g);
      var svg = ui.view.querySelector("svg");
      hoverLayer(ui.view, svg, f, invLinear(f, 0, rmax), function (x) {
        if (!shown.length || x < 0) return "";
        var i = Math.round(x / R.step);
        return "r = " + Math.round(x) + " pm<br>" + shown.map(function (n) { return n + ": " + (R.curves[n][i] * 1000).toFixed(2) + " × 10⁻³ per pm"; }).join("<br>");
      });
      var inside = shown.map(function (n) { return [n, cum(n, st.rc)]; });
      ui.readout.innerHTML = shown.length ? "Probability of finding the electron within " + st.rc + " pm of the nucleus: " +
        inside.map(function (x) { return x[0] + " " + (x[1] * 100).toFixed(1) + "%"; }).join(", ") + ". A bigger share close in means more penetration." : "Turn on at least one orbital.";
      kvSet(ui.kv, shown.map(function (n) { var ft = R.features[n]; return [n, "most probable r ≈ " + Math.round(ft.peaks[ft.peaks.length - 1]) + " pm; zeros: " + (ft.nodes.length ? ft.nodes.map(function (r) { return Math.round(r) + " pm"; }).join(", ") : "none")]; }));
      ui.table.innerHTML = tableHTML(["Orbital", "Peaks (pm)", "Zeros (pm)", "Inside " + st.rc + " pm"], names.map(function (n) {
        var ft = R.features[n]; return [n, ft.peaks.map(function (p) { return Math.round(p); }).join(", "), ft.nodes.map(function (p) { return Math.round(p); }).join(", ") || "none", (cum(n, st.rc) * 100).toFixed(1) + "%"]; }));
    }
    draw();
  };

  /* ================================================================ m10/m11: configuration builder */
  var CORES = [["He", 2, [["1s", 2]]], ["Ne", 10, [["1s", 2], ["2s", 2], ["2p", 6]]], ["Ar", 18, [["1s", 2], ["2s", 2], ["2p", 6], ["3s", 2], ["3p", 6]]],
    ["Kr", 36, [["1s", 2], ["2s", 2], ["2p", 6], ["3s", 2], ["3p", 6], ["4s", 2], ["3d", 10], ["4p", 6]]]];
  function condensed(cfg, nOrder) {
    var occ = {}; cfg.forEach(function (x) { occ[x[0]] = x[1]; });
    var core = null;
    CORES.forEach(function (c) { if (c[2].every(function (x) { return occ[x[0]] === x[1]; })) core = c; });
    var rest = cfg.filter(function (x) { return !core || !core[2].some(function (y) { return y[0] === x[0]; }); });
    if (nOrder) rest = rest.slice().sort(function (a, b) { return (+a[0][0] - +b[0][0]) || ("spdf".indexOf(a[0][1]) - "spdf".indexOf(b[0][1])); });
    return (core ? "[" + core[0] + "]" : "") + cfgHTML(rest);
  }
  calc.condensed = condensed;
  mount.config = function (host, D) {
    var withCharge = host.getAttribute("data-charge") === "1", T = withCharge ? "ion" : "cfg";   // test-id prefix per variant
    var st = { z: withCharge ? 26 : 16, q: withCharge ? 3 : 0, k: null };
    var ui = shell(host, { title: withCharge ? "Explorer: configurations of ions" : "Explorer: build an electron configuration",
      intro: withCharge ? "Pick an element and a charge. For a cation, watch which electrons leave first." : "Pick an element, then use the step slider to add electrons one at a time, following Aufbau, Pauli, and Hund.",
      source: withCharge ? "Source: Day 6 p.21–23 (cations lose the highest-n electrons first; anions add by Aufbau)." : "Source: Day 6 p.6–20 (Aufbau, Pauli, Hund; filling order on Day 6 p.19); exceptions set aside per Day 7 p.6." });
    var sZ = select(ui.controls, { label: "Element", testid: T + "-element", value: String(st.z), options: D.elements.map(function (e, i) { return [String(i + 1), (i + 1) + " " + e[0] + ", " + e[1]]; }),
      onChange: function (v) { st.z = +v; st.k = null; clampQ(); draw(); } });
    var sQ = null;
    if (withCharge) sQ = select(ui.controls, { label: "Charge", testid: T + "-charge", value: String(st.q), options: [[-3, "3−"], [-2, "2−"], [-1, "1−"], [0, "0 (neutral atom)"], [1, "1+"], [2, "2+"], [3, "3+"]].map(function (x) { return [String(x[0]), x[1]]; }),
      onChange: function (v) { st.q = +v; clampQ(); draw(); } });
    var sK = withCharge ? null : slider(ui.controls, { label: "Electrons placed", testid: "cfg-step", min: 0, max: st.z, step: 1, value: st.z, format: function (v) { return v + " of " + st.z; }, onInput: function (v) { st.k = v; draw(); } });
    presetButtons(ui, T, withCharge ? [["Fe³⁺", [26, 3]], ["Ni²⁺ (Day 6 p.21)", [28, 2]], ["V³⁺ (Top Hat)", [23, 3]], ["F⁻ (Day 6 p.21)", [9, -1]], ["S²⁻", [16, -2]], ["Zn²⁺", [30, 2]]]
      : [["C (Day 6 p.16)", [6, 0]], ["N", [7, 0]], ["O", [8, 0]], ["S", [16, 0]], ["Fe", [26, 0]], ["Cr (exception)", [24, 0]]],
      function (p) { st.z = p[0]; st.q = p[1]; st.k = null; sZ.value = String(p[0]); if (sQ) sQ.value = String(p[1]); draw(); });
    function clampQ() { if (st.z - st.q < 0) { st.q = 0; if (sQ) sQ.value = "0"; } }
    function boxes(cfgOcc, removed) {
      var html = "<div class='cfg-ladder'>", order = D.fillOrder, cap = { s: 2, p: 6, d: 10 }, last = 0;
      order.forEach(function (sub, i) { if ((cfgOcc[sub] || 0) + (removed[sub] || 0) > 0) last = i; });
      for (var i = 0; i <= Math.max(last, 0); i++) {
        var sub = order[i], n = cfgOcc[sub] || 0, rm = removed[sub] || 0, orb = cap[sub[1]] / 2;
        var arr = [];
        for (var o = 0; o < orb; o++) arr.push([]);
        // Hund: singly fill up-arrows first, then pair with down-arrows
        var total = n + rm;
        for (var e = 0; e < total; e++) { var slot = e < orb ? e : e - orb; arr[slot].push(e < orb ? "↑" : "↓"); }
        // mark removed electrons: the last `rm` placed
        var marks = [];
        for (var e2 = total - rm; e2 < total; e2++) marks.push(e2 < orb ? [e2, 0] : [e2 - orb, 1]);
        html += "<div class='cfg-row'><span class='sub-label'>" + sub + "</span>";
        arr.forEach(function (a, oi) {
          html += "<span class='obox'>" + a.map(function (sp, si) {
            var gone = marks.some(function (m) { return m[0] === oi && m[1] === si; });
            return "<span class='spin" + (gone ? " removed" : "") + "'>" + sp + (gone ? "<span class='sr-only'> (removed)</span>" : "") + "</span>";
          }).join("") + "</span>";
        });
        html += "<span class='sub-count'>" + n + (rm ? " (" + rm + " removed)" : "") + "</span></div>";
      }
      return html + "</div>";
    }
    function draw() {
      if (sK) { sK.input.max = st.z; if (st.k === null || st.k > st.z) { st.k = st.z; } sK.set(st.k); }
      var z = st.z, q = st.q, sym = D.elements[z - 1][0], name = D.elements[z - 1][1];
      var cfg = D.configs[String(z)][String(q)] || [];
      var shownCfg = cfg, removed = {};
      if (!withCharge && st.k < z) {
        var left = st.k; shownCfg = [];
        D.fillOrder.forEach(function (sub) { var c = { s: 2, p: 6, d: 10 }[sub[1]]; if (left > 0) { var k = Math.min(left, c); shownCfg.push([sub, k]); left -= k; } });
      }
      var occ = {}; shownCfg.forEach(function (x) { occ[x[0]] = x[1]; });
      if (withCharge && q > 0) {
        var neutral = D.configs[String(z)]["0"], nOcc = {};
        neutral.forEach(function (x) { nOcc[x[0]] = x[1]; });
        for (var s in nOcc) { var d = nOcc[s] - (occ[s] || 0); if (d > 0) removed[s] = d; }
      }
      ui.view.innerHTML = boxes(occ, removed);
      var species = ion(sym, q), ne = z - q, nowE = withCharge ? ne : st.k;
      var unp = calc.unpaired(shownCfg);
      var full = cfgHTML(shownCfg) || "(no electrons)";
      var rmList = Object.keys(removed).map(function (s) { return removed[s] + " from " + s; }).join(", ");
      var exc = D.configExceptions[String(z)] && q === 0 && (!sK || st.k === z);
      var hiN = shownCfg.reduce(function (m, x) { return Math.max(m, +x[0][0]); }, 0);
      var outer = shownCfg.filter(function (x) { return +x[0][0] === hiN; }).reduce(function (s, x) { return s + x[1]; }, 0);
      ui.readout.innerHTML = (withCharge ? species + " has " + ne + " electrons: " : name + " with " + nowE + " of " + z + " electrons placed: ") + full +
        (shownCfg.length ? " = " + condensed(shownCfg, false) : "") + ". " + unp + " unpaired electron" + (unp === 1 ? "" : "s") + "." +
        (rmList ? " Removed first: " + rmList + " (highest n leaves first, Day 6 p.21)." : "") +
        (exc ? " <span class='note-inline'>Real " + sym + " is an exception, " + D.configExceptions[String(z)] + "; this course ignores exceptions (Day 7 p.6), so the rules' answer is shown.</span>" : "");
      kvSet(ui.kv, [["Species", species], ["Electrons", String(withCharge ? ne : nowE)], ["Filling order", condensed(shownCfg, false) || "—"], ["n order (also accepted)", condensed(shownCfg, true) || "—"],
        ["Unpaired electrons", String(unp)], ["Electrons in the outermost shell (n = " + hiN + ")", String(outer)]]);
      var rows = [];
      [-2, -1, 0, 1, 2, 3].forEach(function (qq) { var c = D.configs[String(z)][String(qq)]; if (c && z - qq >= 0) rows.push([ion(sym, qq), z - qq, condensed(c, false), calc.unpaired(c)]); });
      ui.table.innerHTML = tableHTML(["Species", "Electrons", "Configuration", "Unpaired"], rows);
    }
    draw();
  };

  /* ================================================================ m12/m13: periodic trends heat map */
  mount.trends = function (host, D) {
    var start = host.getAttribute("data-prop") || "radius", T = start === "radius" ? "trend" : "trend-" + start;   // test-id prefix per mount
    var st = { prop: start, values: true, sel: "Na" };
    var PROPS = {
      radius: { label: "Atomic radius (pm), Day 6 p.24", data: D.atomicRadius, unit: "pm", src: "Day 6 p.24 = Day 7 p.7" },
      ie: { label: "First ionization energy IE₁ (kJ/mol), Day 7 p.9", data: D.ie1, unit: "kJ/mol", src: "Day 7 p.9" },
      ea: { label: "Electron affinity EA₁ (kJ/mol), Day 7 p.11", data: D.ea, unit: "kJ/mol", src: "Day 7 p.11" }
    };
    var ui = shell(host, { title: "Explorer: periodic trends in the lecture data",
      intro: "Switch the property and read the patterns: across a period, down a group, and the exceptions. Select any cell for its value.",
      source: "Source: values exactly as printed on the slides (Day 6 p.24; Day 7 p.9, p.11). EA: “>0” is printed for Be and Mg; * marks values the slide labels as calculated." });
    var sP = select(ui.controls, { label: "Property", testid: T + "-property", value: st.prop, options: Object.keys(PROPS).map(function (k) { return [k, PROPS[k].label]; }), onChange: function (v) { st.prop = v; draw(); } });
    checkbox(ui.controls, { label: "Show numbers in the cells", testid: T + "-values", value: true, onChange: function (v) { st.values = v; draw(); } });
    function color(v, P) {
      if (st.prop === "ea") {
        if (v === null) return { fill: "#f7d4cf", hatch: true };
        if (v > 0) return { fill: v > 30 ? DIV_POS[1] : DIV_POS[0] };
        if (v === 0) return { fill: DIV_MID };
        var t = Math.min(1, -v / 350), idx = Math.round((1 - t) * (DIV_NEG.length - 1));
        return { fill: DIV_NEG[idx] };
      }
      var vals = Object.keys(P.data).map(function (k) { return P.data[k]; }).filter(function (x) { return x !== null; });
      var lo = Math.min.apply(null, vals), hi = Math.max.apply(null, vals);
      return { fill: rampColor((v - lo) / (hi - lo)) };
    }
    function draw() {
      var P = PROPS[st.prop], cw = 64, ch = 46, x0 = 44, y0 = 30, s = "<defs><pattern id='hatch' width='6' height='6' patternUnits='userSpaceOnUse' patternTransform='rotate(45)'><line x1='0' y1='0' x2='0' y2='6' stroke='#d9665c' stroke-width='2'/></pattern></defs>";
      D.groupLabels.forEach(function (g, c) { s += "<text class='tick' x='" + (x0 + c * cw + cw / 2) + "' y='" + (y0 - 10) + "' text-anchor='middle'>" + g + "</text>"; });
      D.layout.forEach(function (row, r) {
        s += "<text class='tick' x='" + (x0 - 10) + "' y='" + (y0 + r * ch + ch / 2 + 4) + "' text-anchor='end'>" + (r + 1) + "</text>";
        row.forEach(function (sym, c) {
          if (!sym) return;
          var v = P.data[sym];
          if (v === undefined) return;
          var col = color(v, P), x = x0 + c * cw, y = y0 + r * ch, ink = inkOn(col.fill);
          var calcMark = st.prop === "ea" && D.eaCalc.indexOf(sym) >= 0 ? "*" : "";
          var vtxt = v === null ? ">0" : (st.prop === "ea" ? String(v).replace("-", "−") : String(v));
          s += "<g class='cell" + (sym === st.sel ? " sel" : "") + "' tabindex='0' role='button' data-sym='" + sym + "' aria-label='" + sym + ": " + vtxt.replace("−", "minus ") + " " + P.unit + (calcMark ? ", calculated" : "") + "'>" +
            "<rect x='" + (x + 1) + "' y='" + (y + 1) + "' width='" + (cw - 2) + "' height='" + (ch - 2) + "' rx='3' fill='" + col.fill + "'/>" +
            (col.hatch ? "<rect x='" + (x + 1) + "' y='" + (y + 1) + "' width='" + (cw - 2) + "' height='" + (ch - 2) + "' rx='3' fill='url(#hatch)' opacity='0.5'/>" : "") +
            "<text x='" + (x + 7) + "' y='" + (y + 17) + "' class='cell-sym' fill='" + ink + "'>" + sym + "</text>" +
            (st.values ? "<text x='" + (x + cw - 6) + "' y='" + (y + ch - 8) + "' text-anchor='end' class='cell-val' fill='" + ink + "'>" + vtxt + calcMark + "</text>" : "") + "</g>";
        });
      });
      s += "<text class='tick muted' x='" + x0 + "' y='" + (y0 + 6 * ch + 18) + "'>columns are groups; rows are periods</text>";
      // legend
      var lx = x0 + 8 * cw + 16, ly = y0;
      if (st.prop === "ea") {
        var steps = [["−349 (most energy released)", DIV_NEG[0]], ["−200", DIV_NEG[2]], ["−50", DIV_NEG[5]], ["0", DIV_MID], ["positive", DIV_POS[1]], [">0 (printed)", "#f7d4cf"]];
        steps.forEach(function (st2, i) { s += "<rect x='" + lx + "' y='" + (ly + i * 22) + "' width='18' height='16' rx='2' fill='" + st2[1] + "'/><text class='tick' x='" + (lx + 24) + "' y='" + (ly + i * 22 + 12) + "'>" + st2[0] + "</text>"; });
      } else {
        for (var i = 0; i < RAMP.length; i++) s += "<rect x='" + lx + "' y='" + (ly + i * 12) + "' width='18' height='12' fill='" + RAMP[RAMP.length - 1 - i] + "'/>";
        var vals = Object.keys(P.data).map(function (k) { return P.data[k]; });
        s += "<text class='tick' x='" + (lx + 24) + "' y='" + (ly + 10) + "'>" + Math.max.apply(null, vals) + " (largest)</text><text class='tick' x='" + (lx + 24) + "' y='" + (ly + RAMP.length * 12) + "'>" + Math.min.apply(null, vals) + " (smallest)</text>";
      }
      ui.view.innerHTML = svgWrap(x0 + 8 * cw + 200, y0 + 6 * ch + 26, P.label + " heat map of the main-group elements.", s);
      $cells().forEach(function (g) {
        var pick = function () { st.sel = g.getAttribute("data-sym"); draw(); var again = ui.view.querySelector(".cell[data-sym='" + st.sel + "']"); if (again) again.focus(); };
        g.addEventListener("click", pick);
        g.addEventListener("keydown", function (e) { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); pick(); } });
      });
      var v = P.data[st.sel], vt = v === null ? ">0" : String(v).replace("-", "−");
      var extra = st.prop === "ea" ? (v === null ? " The slide prints “>0”: energy must be supplied." : v < 0 ? " Negative: energy is released when the atom gains an electron." : v > 0 ? " Positive: energy must be supplied." : "") +
        (D.eaCalc.indexOf(st.sel) >= 0 ? " (calculated value)" : "") : "";
      ui.readout.innerHTML = st.sel + ": " + vt + " " + P.unit + " (" + P.src + ")." + extra;
      kvSet(ui.kv, [["Selected", st.sel], ["Value", vt + " " + P.unit]]);
      ui.table.innerHTML = tableHTML(["Period"].concat(D.groupLabels.map(function (g) { return "Group " + g; })), D.layout.map(function (row, r) {
        return [r + 1].concat(row.map(function (sym) { if (!sym) return ""; var x = P.data[sym]; return x === undefined ? "" : sym + " " + (x === null ? ">0" : String(x).replace("-", "−")) + (st.prop === "ea" && D.eaCalc.indexOf(sym) >= 0 ? "*" : ""); })); }));
    }
    function $cells() { return Array.prototype.slice.call(ui.view.querySelectorAll(".cell")); }
    draw();
  };

  /* ================================================================ m12: sizes to scale */
  mount.sizes = function (host, D) {
    var opts = [];
    Object.keys(D.atomicRadius).forEach(function (s) { opts.push([s, s + " atom", D.atomicRadius[s]]); });
    Object.keys(D.ionicRadius).forEach(function (k) { var m = k.match(/^([A-Z][a-z]?)(\d?)([+-])$/); var q = (m[2] ? +m[2] : 1) * (m[3] === "+" ? 1 : -1); opts.push([k, m[1] + " ion " + (Math.abs(q) > 1 ? Math.abs(q) : "") + (q > 0 ? "+" : "−"), D.ionicRadius[k], m[1], q]); });
    var st = { a: "Na", b: "Na+", c: "Cl", d: "Cl-" };
    var ui = shell(host, { title: "Explorer: atoms and ions drawn to scale",
      intro: "Pick up to four particles. Radii are the lecture's values; circles are drawn to scale.",
      source: "Source: Day 6 p.24; Day 7 p.8 (textbook Figs. 3.35–3.36 give the unit, pm)." });
    var S = {};
    ["a", "b", "c", "d"].forEach(function (k, i) {
      S[k] = select(ui.controls, { label: "Particle " + (i + 1), testid: "size-" + k, value: st[k], options: [["", "(none)"]].concat(opts.map(function (o) { return [o[0], o[1] + " (" + o[2] + " pm)"]; })), onChange: function (v) { st[k] = v; draw(); } });
    });
    presetButtons(ui, "size", [["Na, Na⁺, Cl, Cl⁻", ["Na", "Na+", "Cl", "Cl-"]], ["18-electron ions", ["S2-", "Cl-", "K+", "Ca2+"]], ["10-electron ions", ["O2-", "F-", "Na+", "Mg2+"]], ["Group 1 atoms", ["Li", "Na", "K", "Cs"]]],
      function (p) { ["a", "b", "c", "d"].forEach(function (k, i) { st[k] = p[i]; S[k].value = p[i]; }); draw(); });
    function label(k) { var o = opts.filter(function (x) { return x[0] === k; })[0]; if (!o) return ""; return o.length > 3 ? ion(o[3], o[4]) : o[0]; }
    function labelSVG(k) { var o = opts.filter(function (x) { return x[0] === k; })[0]; if (!o) return ""; return o.length > 3 ? ionSVG(o[3], o[4]) : o[0]; }
    function draw() {
      var list = ["a", "b", "c", "d"].map(function (k) { return st[k]; }).filter(Boolean);
      var sc = 0.36, x = 20, s = "";
      list.forEach(function (k) {
        var o = opts.filter(function (x2) { return x2[0] === k; })[0], r = o[2] * sc;
        s += "<circle cx='" + (x + r) + "' cy='120' r='" + r + "' class='" + (o.length > 3 ? (o[4] > 0 ? "cation" : "anion") : "atom-c") + "'/>" +
          "<text class='tick strong' x='" + (x + r) + "' y='" + (120 + r + 18) + "' text-anchor='middle'>" + labelSVG(k) + "</text>" +
          "<text class='tick' x='" + (x + r) + "' y='" + (120 + r + 32) + "' text-anchor='middle'>" + o[2] + " pm</text>";
        x += 2 * r + 24;
      });
      ui.view.innerHTML = svgWrap(Math.max(600, x), 240, "Particles drawn to scale: " + list.join(", "), s);
      ui.readout.innerHTML = list.map(function (k) { var o = opts.filter(function (x2) { return x2[0] === k; })[0]; return label(k) + " " + o[2] + " pm"; }).join("; ") + ".";
      kvSet(ui.kv, []);
      ui.table.innerHTML = tableHTML(["Particle", "Radius (pm)"], list.map(function (k) { var o = opts.filter(function (x2) { return x2[0] === k; })[0]; return [label(k), o[2]]; }));
    }
    draw();
  };

  /* ================================================================ m13: successive ionization energies */
  mount.successiveIE = function (host, D) {
    var syms = Object.keys(D.successiveIE);
    var st = { sym: "Be", mystery: false, revealed: false };
    var ui = shell(host, { title: "Explorer: successive ionization energies",
      intro: "Choose an element. The bars climb on a log scale; look for the one big jump. In mystery mode the element is hidden. Identify it from the jump.",
      source: "Source: Day 7 p.10 (textbook Table 3.2, values as printed; N IE₄ = O IE₄ = 7465 and N IE₅ = Ne IE₄ = 9391 look like small printing errors in the source table)." });
    var sS = select(ui.controls, { label: "Element", testid: "sie-element", value: st.sym, options: syms.map(function (s) { return [s, s]; }), onChange: function (v) { st.sym = v; st.mystery = false; draw(); } });
    var row = el("div", { class: "ctl-row" }); ui.controls.appendChild(row);
    button(row, "Mystery element", "btn-sie-mystery", function () { var pool = syms.filter(function (s) { return D.successiveIE[s].length > 2; }); st.sym = pool[Math.floor(Math.random() * pool.length)]; st.mystery = true; st.revealed = false; sS.value = ""; draw(); });
    var rv = button(row, "Reveal the element", "btn-sie-reveal", function () { st.revealed = true; sS.value = st.sym; draw(); });
    function draw() {
      var ies = D.successiveIE[st.sym], n = ies.length, hide = st.mystery && !st.revealed;
      rv.disabled = !hide;
      var ratios = ies.slice(1).map(function (v, i) { return v / ies[i]; });
      var val = D.valence2[st.sym], core = n > val; // electrons beyond valence are core
      var jumpAt = core ? val : -1; // jump between IE_val and IE_val+1
      var f = frame({ w: 600, h: 300, x0: 0, x1: 10, y0: 100, y1: 200000, ylog: true, yticks: [[100, "100"], [1000, "1,000"], [10000, "10,000"], [100000, "100,000"]],
        xticks: [], xlabel: "which electron is removed (IE₁, IE₂, …)", ylabel: "ionization energy (kJ/mol, log scale)", m: { l: 64, r: 16, t: 14, b: 44 } });
      var g = f.axes, slot = f.pw / 10;
      ies.forEach(function (v, i) {
        var isCore = core && i >= val, x = f.m.l + i * slot + slot / 2 - 12, y = f.ys(v), y0 = f.ys(100);
        g += "<path class='bar' d='M" + x + " " + y0 + " V" + (y + 4) + " q0 -4 4 -4 h16 q4 0 4 4 V" + y0 + " Z' fill='" + (isCore ? SERIES[1] : SERIES[0]) + "'><title>" + formulaText("IE" + (i + 1)) + " = " + v.toLocaleString("en-US") + " kJ/mol</title></path>" +
          "<text class='tick' x='" + (x + 12) + "' y='" + (y0 + 16) + "' text-anchor='middle'>" + formulaText("IE" + (i + 1)) + "</text>";
      });
      if (jumpAt > 0) {
        var jx = f.m.l + jumpAt * slot;
        g += "<line class='jump' x1='" + jx + "' x2='" + jx + "' y1='" + f.m.t + "' y2='" + f.ys(100) + "'/><text class='direct-label strong' x='" + (jx + 5) + "' y='" + (f.m.t + 12) + "'>big jump: core electrons start here (×" + ratios[jumpAt - 1].toFixed(1) + ")</text>";
      }
      var legend = core ? "<div class='legend-row'><span class='lg'><span class='lg-sw' style='background:" + SERIES[0] + "'></span>valence electrons removed</span><span class='lg'><span class='lg-sw' style='background:" + SERIES[1] + "'></span>core (1s) electrons removed</span></div>" : "";
      ui.view.innerHTML = legend + svgWrap(600, 300, "Successive ionization energies of " + (hide ? "a mystery element" : st.sym) + " on a log scale.", g);
      var who = hide ? "this element" : st.sym;
      ui.readout.innerHTML = core ? "Largest jump: IE<sub>" + jumpAt + "</sub> → IE<sub>" + (jumpAt + 1) + "</sub> (×" + ratios[jumpAt - 1].toFixed(1) + "). So " + who + " has " + val + " valence electron" + (val === 1 ? "" : "s") +
        (hide ? ". Which second-period element has that many? Reveal to check." : ", and IE<sub>" + (jumpAt + 1) + "</sub> starts pulling 1s core electrons.") :
        "All of " + who + "'s electrons are in n = 1: there are no core electrons, so there is no valence-to-core jump.";
      kvSet(ui.kv, [["Electrons", String(n)], ["Valence electrons (before the jump)", core ? String(val) : String(n)], ["Largest ratio", ratios.length ? "×" + Math.max.apply(null, ratios).toFixed(1) : "—"]]);
      ui.table.innerHTML = tableHTML(["IE", "kJ/mol", "Ratio to the previous IE"], ies.map(function (v, i) { return ["IE<sub>" + (i + 1) + "</sub>", v.toLocaleString("en-US"), i ? "×" + ratios[i - 1].toFixed(2) : "—"]; }));
    }
    draw();
  };

  /* ================================================================ m14: Coulomb energy */
  mount.coulomb = function (host, D) {
    useData(D);
    var CAT = [["Li+", "Li", 1], ["Na+", "Na", 1], ["K+", "K", 1], ["Be2+", "Be", 2], ["Mg2+", "Mg", 2], ["Ca2+", "Ca", 2], ["Al3+", "Al", 3]];
    var AN = [["F-", "F", -1], ["Cl-", "Cl", -1], ["Br-", "Br", -1], ["O2-", "O", -2], ["S2-", "S", -2], ["Se2-", "Se", -2]];
    var st = { c: "Na+", a: "Cl-", d: 0.283, wall: true };
    var ui = shell(host, { title: "Explorer: the energy of an ion pair",
      intro: "Choose a cation and an anion, then move them together. E<sub>el</sub> = 2.31 × 10<sup>−19</sup> J·nm (Q<sub>1</sub>Q<sub>2</sub>/d). Which matters more: charge or distance?",
      source: "Source: Day 7 p.8 (radii), p.15 (E<sub>el</sub> and the energy curve), p.17 (lattice energies). The repulsion wall is a schematic background model, not the lecture's equation." });
    var sC = select(ui.controls, { label: "Cation", testid: "cou-cation", value: st.c, options: CAT.map(function (c) { return [c[0], ionText(c[1], c[2]) + " (" + D.ionicRadius[c[0]] + " pm)"]; }), onChange: function (v) { st.c = v; touch(); draw(); } });
    var sA = select(ui.controls, { label: "Anion", testid: "cou-anion", value: st.a, options: AN.map(function (a) { return [a[0], ionText(a[1], a[2]) + " (" + D.ionicRadius[a[0]] + " pm)"]; }), onChange: function (v) { st.a = v; touch(); draw(); } });
    var sl = slider(ui.controls, { label: "Distance between the ion centers, d", testid: "cou-distance", min: 0.1, max: 1.0, step: 0.001, value: st.d, format: function (v) { return v.toFixed(3) + " nm"; }, onInput: function (v) { st.d = v; draw(); } });
    var row = el("div", { class: "ctl-row" }); ui.controls.appendChild(row);
    button(row, "Set the ions touching (d = r₊ + r₋)", "btn-cou-touch", function () { touch(); draw(); });
    checkbox(ui.controls, { label: "Show the schematic repulsion wall", testid: "cou-wall", value: st.wall, onChange: function (v) { st.wall = v; draw(); } });
    presetButtons(ui, "cou", [["NaCl", ["Na+", "Cl-"]], ["KCl", ["K+", "Cl-"]], ["MgO", ["Mg2+", "O2-"]], ["CaS", ["Ca2+", "S2-"]], ["LiF", ["Li+", "F-"]]],
      function (p) { st.c = p[0]; st.a = p[1]; sC.value = p[0]; sA.value = p[1]; touch(); draw(); });
    function q(list, k) { return list.filter(function (x) { return x[0] === k; })[0]; }
    function touch() { st.d = (D.ionicRadius[st.c] + D.ionicRadius[st.a]) / 1000; sl.set(st.d); }
    function draw() {
      var c = q(CAT, st.c), a = q(AN, st.a), Q = c[2] * a[2], d0 = (D.ionicRadius[st.c] + D.ionicRadius[st.a]) / 1000;
      var E = calc.eel(c[2], a[2], st.d);
      // schematic total: attraction + B exp(-d/rho), with the minimum placed at d0
      var rho = 0.03, B = -K.coul * Q / (d0 * d0) * rho * Math.exp(d0 / rho);
      var tot = function (d) { return calc.eel(c[2], a[2], d) + B * Math.exp(-d / rho); };
      var ymin = Math.min(calc.eel(c[2], a[2], 0.1), -2e-19) / 1e-19, lo = Math.floor(ymin * 1.05);
      var f = frame({ w: 600, h: 300, x0: 0.1, x1: 1.0, y0: lo, y1: Math.max(4, -lo * 0.25), xticks: [[0.2, "0.2"], [0.4, "0.4"], [0.6, "0.6"], [0.8, "0.8"], [1.0, "1.0"]],
        yticks: [[0, "0"], [Math.round(lo / 2), String(Math.round(lo / 2)).replace("-", "−")], [lo, String(lo).replace("-", "−")]], xlabel: "d, distance between ion centers (nm)", ylabel: "energy (10⁻¹⁹ J per pair)" });
      var clip = "<defs><clipPath id='cou-clip'><rect x='" + f.m.l + "' y='" + f.m.t + "' width='" + f.pw + "' height='" + f.ph + "'/></clipPath></defs>";
      var g = clip + f.axes + "<line class='zero' x1='" + f.m.l + "' x2='" + (f.m.l + f.pw) + "' y1='" + f.ys(0) + "' y2='" + f.ys(0) + "'/>";
      var pa = [], pt = [];
      for (var d = 0.1; d <= 1.0001; d += 0.004) { pa.push([f.xs(d), f.ys(calc.eel(c[2], a[2], d) / 1e-19)]); pt.push([f.xs(d), f.ys(Math.min(tot(d), 50e-19) / 1e-19)]); }
      g += "<g clip-path='url(#cou-clip)'><path d='" + linePath(pa) + "' class='series-line' stroke='" + SERIES[0] + "'/>" + (st.wall ? "<path d='" + linePath(pt) + "' class='series-line' stroke='" + SERIES[1] + "'/>" : "") + "</g>";
      g += "<circle cx='" + f.xs(st.d) + "' cy='" + f.ys(E / 1e-19) + "' r='5' class='dot' fill='" + SERIES[0] + "'/>";
      g += "<line class='landmark' x1='" + f.xs(d0) + "' x2='" + f.xs(d0) + "' y1='" + f.m.t + "' y2='" + (f.m.t + f.ph) + "'/><text class='tick muted' x='" + (f.xs(d0) + 4) + "' y='" + (f.m.t + 12) + "'>touching, " + d0.toFixed(3) + " nm</text>";
      var legend = "<div class='legend-row'><span class='lg'><span class='lg-sw' style='background:" + SERIES[0] + "'></span>E<sub>el</sub> from the equation (attraction)</span>" + (st.wall ? "<span class='lg'><span class='lg-sw' style='background:" + SERIES[1] + "'></span>schematic total with repulsion (background model)</span>" : "") + "</div>";
      ui.view.innerHTML = legend + svgWrap(600, 300, "Electrostatic potential energy versus distance for the chosen ion pair.", g);
      var svg = ui.view.querySelector("svg");
      hoverLayer(ui.view, svg, f, invLinear(f, 0.1, 1.0), function (x) { return "d = " + x.toFixed(3) + " nm<br>E<sub>el</sub> = " + sci(calc.eel(c[2], a[2], x)) + " J"; });
      var formula = (function () { var g2 = calc.gcd(c[2], -a[2]), nc = -a[2] / g2, na = c[2] / g2; return formulaHTML([[c[1], nc], [a[1], na]]); })();
      var key = formula.replace(/<\/?sub>/g, ""), U = D.lattice[key], perMol = E * K.NA / 1000;
      var oneToOne = c[2] === -a[2];
      var msg = ion(c[1], c[2]) + " and " + ion(a[1], a[2]) + " at d = " + st.d.toFixed(3) + " nm: Q<sub>1</sub>Q<sub>2</sub> = " + String(Q).replace("-", "−") + ", so E<sub>el</sub> = " + sci(E) + " J per pair" +
        " (× N<sub>A</sub>: " + num(perMol, 3) + " kJ/mol). Negative means the pair is lower in energy than separated ions.";
      if (U !== undefined && oneToOne) {
        var at0 = calc.eel(c[2], a[2], d0) * K.NA / 1000;
        msg += " At the touching distance one pair gives " + num(at0, 3) + " kJ/mol; the real lattice energy of " + formula + " is U = " + String(U).replace("-", "−") +
          " kJ/mol (Day 7 p.17), about " + (U / at0).toFixed(2) + " times as large: the lattice is “even more stable.”";
      }
      ui.readout.innerHTML = msg;
      kvSet(ui.kv, [["Q₁Q₂", String(Q).replace("-", "−")], ["d", st.d.toFixed(3) + " nm"], ["E<sub>el</sub>", sci(E) + " J per pair"], ["Per mole (× N<sub>A</sub>, background)", num(perMol, 3) + " kJ/mol"],
        ["Formula", formula], ["Lattice energy U (Day 7 p.17)", U !== undefined ? String(U).replace("-", "−") + " kJ/mol" : "not in the lecture table"]]);
      var rows = [["Na+", "Cl-"], ["K+", "Cl-"], ["Li+", "F-"], ["Mg2+", "O2-"], ["Ca2+", "S2-"]].map(function (p) {
        var cc = q(CAT, p[0]), aa = q(AN, p[1]), dd = (D.ionicRadius[p[0]] + D.ionicRadius[p[1]]) / 1000, e = calc.eel(cc[2], aa[2], dd), fk = cc[1] + aa[1];
        return [ion(cc[1], cc[2]) + " / " + ion(aa[1], aa[2]), dd.toFixed(3), sci(e), num(e * K.NA / 1000, 3), D.lattice[fk] !== undefined ? String(D.lattice[fk]).replace("-", "−") : "—"];
      });
      ui.table.innerHTML = tableHTML(["Pair", "d touching (nm)", "E<sub>el</sub> per pair (J)", "× N<sub>A</sub> (kJ/mol)", "U, Day 7 p.17 (kJ/mol)"], rows);
    }
    draw();
  };

  /* ================================================================ m15: formula builder */
  mount.formula = function (host, D) {
    var MET = [["Li", 1, "lithium"], ["Na", 1, "sodium"], ["K", 1, "potassium"], ["Mg", 2, "magnesium"], ["Ca", 2, "calcium"], ["Ba", 2, "barium"], ["Al", 3, "aluminum"]];
    var NON = [["F", -1, "fluoride"], ["Cl", -1, "chloride"], ["Br", -1, "bromide"], ["I", -1, "iodide"], ["O", -2, "oxide"], ["S", -2, "sulfide"], ["N", -3, "nitride"]];
    var GROUP = { Li: 1, Na: 1, K: 1, Mg: 2, Ca: 2, Ba: 2, Al: 13, F: 17, Cl: 17, Br: 17, I: 17, O: 16, S: 16, N: 15 };
    var st = { m: "Al", x: "O", nc: 1, na: 1 };
    var ui = shell(host, { title: "Explorer: build a neutral ionic compound",
      intro: "Choose a metal and a nonmetal, then add ions until the total charge is zero. The smallest whole-number ratio is the formula.",
      source: "Source: Day 7 p.18–21 (ion charges from the valence shell, “The TOTAL charge has to be zero,” and the naming rule). Ions beyond those on Day 7 p.19 follow the same group rule (connection)." });
    select(ui.controls, { label: "Metal (cation)", testid: "fx-metal", value: st.m, options: MET.map(function (m) { return [m[0], m[2] + " (group " + GROUP[m[0]] + ")"]; }), onChange: function (v) { st.m = v; st.nc = 1; st.na = 1; draw(); } });
    var ELNAME = { F: "fluorine", Cl: "chlorine", Br: "bromine", I: "iodine", O: "oxygen", S: "sulfur", N: "nitrogen" };
    select(ui.controls, { label: "Nonmetal (anion)", testid: "fx-nonmetal", value: st.x, options: NON.map(function (n) { return [n[0], ELNAME[n[0]] + " (group " + GROUP[n[0]] + ")"]; }), onChange: function (v) { st.x = v; st.nc = 1; st.na = 1; draw(); } });
    var cnt = el("div", { class: "ctl-counters" }); ui.controls.appendChild(cnt);
    function counter(label, key, tid) {
      var wrap = el("div", { class: "counter", role: "group", "aria-label": label });
      wrap.appendChild(el("span", { class: "counter-label" }, label));
      button(wrap, "−", "formula-" + tid + "-minus", function () { st[key] = Math.max(1, st[key] - 1); draw(); });
      var out = el("output", { class: "counter-val", "data-testid": "formula-" + tid + "-count" });
      wrap.appendChild(out);
      button(wrap, "+", "formula-" + tid + "-plus", function () { st[key] = Math.min(6, st[key] + 1); draw(); });
      cnt.appendChild(wrap);
      return out;
    }
    var oc = counter("Cations", "nc", "cation"), oa = counter("Anions", "na", "anion");
    var row = el("div", { class: "ctl-row" }); ui.controls.appendChild(row);
    button(row, "Balance it for me", "btn-formula-solve", function () { var m = MET.filter(function (x) { return x[0] === st.m; })[0], n = NON.filter(function (x) { return x[0] === st.x; })[0], g = calc.gcd(m[1], -n[1]); st.nc = -n[1] / g; st.na = m[1] / g; draw(); });
    function draw() {
      var m = MET.filter(function (x) { return x[0] === st.m; })[0], n = NON.filter(function (x) { return x[0] === st.x; })[0];
      oc.textContent = st.nc; oa.textContent = st.na;
      var total = st.nc * m[1] + st.na * n[1];
      var tiles = "";
      for (var i = 0; i < st.nc; i++) tiles += "<span class='tile tile-cat'>" + ion(m[0], m[1]) + "<span class='tile-q'>" + "+".repeat(m[1]) + "</span></span>";
      for (var j = 0; j < st.na; j++) tiles += "<span class='tile tile-an'>" + ion(n[0], n[1]) + "<span class='tile-q'>" + "−".repeat(-n[1]) + "</span></span>";
      var g = calc.gcd(st.nc, st.na), lowest = g === 1;
      var fHTML = formulaHTML([[m[0], st.nc], [n[0], st.na]]);
      var name = m[2] + " " + n[2];
      var cfgM = D.configs[String(D.elements.findIndex(function (e) { return e[0] === m[0]; }) + 1)];
      var cfgN = D.configs[String(D.elements.findIndex(function (e) { return e[0] === n[0]; }) + 1)];
      var why = "<p class='xp-caption'>" + m[0] + " (group " + GROUP[m[0]] + ") loses " + m[1] + " valence electron" + (m[1] > 1 ? "s" : "") + " → " + ion(m[0], m[1]) + (cfgM ? " = " + condensed(cfgM[String(m[1])], false) : "") +
        ". " + n[0] + " (group " + GROUP[n[0]] + ") gains " + (-n[1]) + " → " + ion(n[0], n[1]) + (cfgN ? " = " + condensed(cfgN[String(n[1])], false) : "") + ". Both reach a noble-gas configuration (Day 7 p.18).</p>";
      ui.view.innerHTML = why + "<div class='tiles' aria-label='" + st.nc + " cations and " + st.na + " anions'>" + tiles + "</div>" +
        "<p class='charge-sum " + (total === 0 ? "ok" : "no") + "'><span aria-hidden='true'>" + (total === 0 ? "✓" : "✗") + "</span> Total charge: " + st.nc + "(" + (m[1] > 0 ? "+" : "") + m[1] + ") + " + st.na + "(" + String(n[1]).replace("-", "−") + ") = " + String(total).replace("-", "−") + "</p>";
      ui.readout.innerHTML = total !== 0 ? "Not neutral yet: the total charge is " + String(total).replace("-", "−") + ". Add " + (total > 0 ? "anions" : "cations") + "." :
        lowest ? "Neutral with the smallest whole-number ratio: " + fHTML + ", named " + name + " (cation name + anion name ending in -ide, no prefixes; Day 7 p.21)." :
          "Neutral, but " + st.nc + " : " + st.na + " reduces to " + (st.nc / g) + " : " + (st.na / g) + ". Formulas use the smallest ratio.";
      kvSet(ui.kv, [["Cation", ion(m[0], m[1])], ["Anion", ion(n[0], n[1])], ["Total charge", String(total).replace("-", "−")], ["Formula", total === 0 && lowest ? fHTML : "—"], ["Name", total === 0 ? name : "—"]]);
      ui.table.innerHTML = tableHTML(["Metal", "Nonmetal", "Formula", "Name"], MET.slice(0, 7).map(function (mm) {
        var gg = calc.gcd(mm[1], -n[1]); return [ion(mm[0], mm[1]), ion(n[0], n[1]), formulaHTML([[mm[0], -n[1] / gg], [n[0], mm[1] / gg]]), mm[2] + " " + n[2]]; }));
    }
    draw();
  };

  return { calc: calc, mount: mount, fmt: { sci: sci, num: num }, useData: useData, _K: K,
    ui: { el: el, shell: shell, slider: slider, select: select, checkbox: checkbox, radios: radios, button: button,
      presetButtons: presetButtons, kvSet: kvSet, tableHTML: tableHTML, svgWrap: svgWrap, linePath: linePath, frame: frame,
      hoverLayer: hoverLayer, invLinear: invLinear, sci: sci, num: num, fix: fix, esc: esc, ion: ion, ionText: ionText, uniSup: uniSup, formulaText: formulaText, signed: signed, ionSVG: ionSVG, sciSVG: sciSVG,
      formulaHTML: formulaHTML, formulaSVG: formulaSVG, cfgHTML: cfgHTML, wavelengthColor: wavelengthColor, rampColor: rampColor, inkOn: inkOn,
      SERIES: SERIES, RAMP: RAMP, DIV_NEG: DIV_NEG, DIV_POS: DIV_POS, DIV_MID: DIV_MID, reduceMotion: reduceMotion } };
});

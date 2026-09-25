/* Textbook-preview explorers for the CurrentCourseGuide (Ch. 1–4 sections not yet lectured).
   Classic script loaded after explorers.js; adds to window.Explorers.mount. In node, module.exports
   gives the pure calculation functions (tested by verification/CurrentCourseGuide/test_explorers_preview.js). */
(function (root, factory) {
  if (typeof module === "object" && module.exports) module.exports = factory(require("./explorers.js"));
  else factory(root.Explorers);
})(typeof self !== "undefined" ? self : this, function (X) {
  "use strict";
  var U = X.ui, K = X._K, mount = X.mount;
  var MINUS = "−";

  /* ================================================================ pure calculations */
  var P = {};

  // ---- significant figures (textbook §1.7 rules)
  P.sigInfo = function (raw) {
    var s = String(raw || "").trim().replace(/[−–]/g, "-").replace(/,/g, "");
    var m = s.match(/^([+-]?)(\d*\.?\d*)(?:\s*(?:[eE]|[x×*]\s*10\s*\^?)\s*([+-]?\d+))?$/);
    if (!m || !/\d/.test(m[2])) return null;
    var mant = m[2], exp = m[3] ? parseInt(m[3], 10) : 0, hasPoint = mant.indexOf(".") >= 0;
    var chars = mant.split(""), firstNZ = -1, lastNZ = -1;
    chars.forEach(function (c, i) { if (/[1-9]/.test(c)) { if (firstNZ < 0) firstNZ = i; lastNZ = i; } });
    var out = [], sf = 0, amb = 0;
    chars.forEach(function (c, i) {
      if (c === ".") { out.push({ ch: c, kind: "point" }); return; }
      if (firstNZ < 0) { out.push({ ch: c, kind: "lead" }); return; }             // all zeros
      if (i < firstNZ) { out.push({ ch: c, kind: "lead" }); return; }
      if (i <= lastNZ) { out.push({ ch: c, kind: "sig" }); sf++; return; }
      if (hasPoint) { out.push({ ch: c, kind: "sig" }); sf++; return; }             // trailing zero after a decimal point
      out.push({ ch: c, kind: "amb" }); amb++;                                     // trailing zero, no decimal point
    });
    if (firstNZ < 0) sf = Math.max(1, hasPoint ? chars.filter(function (c) { return c === "0"; }).length : 1);
    var value = (m[1] === "-" ? -1 : 1) * parseFloat(mant) * Math.pow(10, exp);
    var decimals = (hasPoint ? mant.length - mant.indexOf(".") - 1 : 0) - exp;      // place of the last written digit
    return { sign: m[1], mantissa: mant, exp: exp, digits: out, sf: sf, ambiguous: amb, value: value, decimals: decimals };
  };
  // decimal-string rounding with the textbook's round-half-to-even tie rule
  function toDecimalString(x) {
    if (!isFinite(x)) return String(x);
    var s = Math.abs(x).toPrecision(15);
    if (s.indexOf("e") >= 0) {
      var parts = s.split("e"), m = parts[0].replace(".", ""), e = parseInt(parts[1], 10), pointPos = (parts[0].indexOf(".") >= 0 ? parts[0].indexOf(".") : parts[0].length) + e;
      if (pointPos <= 0) s = "0." + "0".repeat(-pointPos) + m;
      else if (pointPos >= m.length) s = m + "0".repeat(pointPos - m.length);
      else s = m.slice(0, pointPos) + "." + m.slice(pointPos);
    }
    return (x < 0 ? "-" : "") + s;
  }
  P.roundToDecimals = function (x, d) {
    // Round to d decimal places (d < 0 rounds to tens, hundreds, ...) using the textbook's tie rule:
    // a dropped digit of exactly 5 (nothing after it) rounds to the nearest even digit.
    if (!isFinite(x) || x === 0) return x;
    var neg = x < 0, str = toDecimalString(Math.abs(x));
    if (str.indexOf(".") < 0) str += ".";
    var ip = str.split(".")[0], fp = str.split(".")[1], digits = (ip + fp).split("").map(Number);
    var pos = ip.length + d;                         // number of digits kept, counted from the left
    if (pos >= digits.length) return x;
    if (pos < 0) return 0;
    var kept = digits.slice(0, pos), rest = digits.slice(pos);
    var first = rest[0], after = rest.slice(1).some(function (v) { return v > 0; });
    var last = kept.length ? kept[kept.length - 1] : 0;
    if (first > 5 || (first === 5 && (after || last % 2 === 1))) {
      var k = kept.length - 1;
      while (k >= 0 && kept[k] === 9) { kept[k] = 0; k--; }
      if (k >= 0) kept[k]++; else kept.unshift(1);
    }
    var n = kept.length ? parseInt(kept.join(""), 10) : 0;
    var shift = ip.length - pos;                     // place value of the last kept digit is 10^shift
    var val = shift >= 0 ? n * Math.pow(10, shift) : n / Math.pow(10, -shift);
    return neg ? -val : val;
  };
  P.roundToSigFigs = function (x, sf) {
    if (x === 0) return 0;
    var e = Math.floor(Math.log10(Math.abs(x)));
    return P.roundToDecimals(x, sf - 1 - e);
  };
  P.formatSig = function (x, sf) {
    if (x === 0) return "0";
    var r = P.roundToSigFigs(x, sf), e = Math.floor(Math.log10(Math.abs(r)));
    if (e >= -3 && e < 6) {
      var dec = Math.max(0, sf - 1 - e);
      var s = Math.abs(r).toFixed(dec);
      if (dec === 0 && sf < e + 1) return (r < 0 ? MINUS : "") + s + " (" + U.sci(r, sf) + ")";
      return (r < 0 ? MINUS : "") + s;
    }
    return U.sci(r, sf);
  };
  P.combine = function (a, op, b) {
    var A = P.sigInfo(a), B = P.sigInfo(b);
    if (!A || !B) return null;
    var raw = op === "+" ? A.value + B.value : op === "-" ? A.value - B.value : op === "*" ? A.value * B.value : A.value / B.value;
    if (op === "+" || op === "-") {
      var d = Math.min(A.decimals, B.decimals);
      var r = P.roundToDecimals(raw, d);
      return { raw: raw, result: r, rule: "decimal places", keep: d, text: r.toFixed(Math.max(0, d)) };
    }
    var sf = Math.min(A.sf, B.sf);
    return { raw: raw, result: P.roundToSigFigs(raw, sf), rule: "significant figures", keep: sf, text: P.formatSig(raw, sf) };
  };

  // ---- statistics (textbook §1.9); Student t computed numerically (background)
  P.mean = function (xs) { return xs.reduce(function (s, x) { return s + x; }, 0) / xs.length; };
  P.stdev = function (xs) { var m = P.mean(xs); return Math.sqrt(xs.reduce(function (s, x) { return s + (x - m) * (x - m); }, 0) / (xs.length - 1)); };
  function lgamma(z) { // Lanczos
    var g = 7, c = [0.99999999999980993, 676.5203681218851, -1259.1392167224028, 771.32342877765313, -176.61502916214059, 12.507343278686905, -0.13857109526572012, 9.9843695780195716e-6, 1.5056327351493116e-7];
    if (z < 0.5) return Math.log(Math.PI / Math.sin(Math.PI * z)) - lgamma(1 - z);
    z -= 1; var x = c[0]; for (var i = 1; i < g + 2; i++) x += c[i] / (z + i);
    var t = z + g + 0.5; return 0.5 * Math.log(2 * Math.PI) + (z + 0.5) * Math.log(t) - t + Math.log(x);
  }
  function tcdfPos(t, v) { // P(0 < T < t) by Simpson integration of the t pdf
    var c = Math.exp(lgamma((v + 1) / 2) - lgamma(v / 2)) / Math.sqrt(v * Math.PI), n = 2000, h = t / n, s = 0;
    for (var i = 0; i <= n; i++) { var x = i * h, f = c * Math.pow(1 + x * x / v, -(v + 1) / 2); s += (i === 0 || i === n ? 1 : i % 2 ? 4 : 2) * f; }
    return s * h / 3;
  }
  P.tCritical = function (df, conf) { // two-sided critical t
    var target = conf / 2, lo = 0, hi = 100;
    for (var k = 0; k < 80; k++) { var mid = (lo + hi) / 2; if (tcdfPos(mid, df) < target) lo = mid; else hi = mid; }
    return (lo + hi) / 2;
  };
  P.T_TABLE = { 3: [2.353, 3.182, 5.841], 4: [2.132, 2.776, 4.604], 5: [2.015, 2.571, 4.032], 10: [1.812, 2.228, 3.169], 20: [1.725, 2.086, 2.845] };
  P.GRUBBS = { 3: [1.155, 1.155], 4: [1.481, 1.496], 5: [1.715, 1.764], 6: [1.887, 1.973], 7: [2.020, 2.139], 8: [2.126, 2.274], 9: [2.215, 2.387], 10: [2.290, 2.482], 11: [2.355, 2.564], 12: [2.412, 2.636] };
  P.analyze = function (xs) {
    var n = xs.length; if (n < 2) return null;
    var m = P.mean(xs), s = P.stdev(xs), df = n - 1;
    var fromTable = P.T_TABLE[df] ? P.T_TABLE[df][1] : null, t = fromTable || P.tCritical(df, 0.95);
    var half = t * s / Math.sqrt(n), far = 0, idx = 0;
    xs.forEach(function (x, i) { if (Math.abs(x - m) > far) { far = Math.abs(x - m); idx = i; } });
    var Z = s > 0 ? far / s : 0, ref = P.GRUBBS[n] ? P.GRUBBS[n][0] : null;
    return { n: n, mean: m, s: s, t: t, tFromTable: !!fromTable, half: half, suspect: idx, Z: Z, Zref: ref, outlier: ref !== null && Z > ref };
  };

  // ---- unit conversion (textbook Table 1.3 equivalences)
  var UNITS = {
    length: { base: "m", units: { m: 1, cm: 0.01, mm: 0.001, km: 1000, "in": 0.0254, ft: 0.3048, mi: 1000 / 0.6214 },
      exact: { m: 1, cm: 1, mm: 1, km: 1, "in": 1, ft: 1 }, note: "1 in = 2.54 cm (exact); 1 ft = 12 in (exact); 1 km = 0.6214 mi" },
    mass: { base: "kg", units: { kg: 1, g: 0.001, mg: 1e-6, lb: 1 / 2.205, oz: 1 / 35.27 }, exact: { kg: 1, g: 1, mg: 1 }, note: "1 kg = 2.205 lb = 35.27 oz" },
    volume: { base: "L", units: { L: 1, mL: 0.001, "m³": 1000, "cm³": 0.001, gal: 1 / 0.2642, qt: 1 / 1.057 }, exact: { L: 1, mL: 1, "m³": 1, "cm³": 1 }, note: "1 m³ = 1000 L (exact); 1 L = 0.2642 gal = 1.057 qt; 1 mL = 1 cm³" },
    speed: { base: "m/s", units: { "m/s": 1, "km/h": 1000 / 3600, "mi/h": (1000 / 0.6214) / 3600 }, exact: { "m/s": 1, "km/h": 1 }, note: "1 h = 3600 s (exact); 1 km = 0.6214 mi" },
    density: { base: "g/cm³", units: { "g/cm³": 1, "g/mL": 1, "kg/L": 1, "kg/m³": 0.001 }, exact: { "g/cm³": 1, "g/mL": 1, "kg/L": 1, "kg/m³": 1 }, note: "1 mL = 1 cm³; 1 kg = 1000 g; 1 m³ = 10⁶ cm³" }
  };
  P.UNITS = UNITS;
  P.convert = function (cat, v, from, to) {
    if (cat === "temperature") {
      var c = from === "K" ? v - 273.15 : from === "°F" ? (5 / 9) * (v - 32) : v;
      return { value: to === "K" ? c + 273.15 : to === "°F" ? (9 / 5) * c + 32 : c, celsius: c };
    }
    var C = UNITS[cat];
    return { value: v * C.units[from] / C.units[to], exact: !!(C.exact[from] && C.exact[to]) };
  };

  // ---- isotope patterns (Cl and Br isotopes; other atoms at their nominal masses; background abundances)
  P.isotopePattern = function (counts, iso) {
    var peaks = { 0: 1 }, nominal = { H: 1, C: 12, N: 14, O: 16, F: 19 };
    Object.keys(counts).forEach(function (el) {
      for (var k = 0; k < counts[el]; k++) {
        var next = {};
        var opts = iso[el] ? iso[el].map(function (r) { return [r[0], r[2]]; }) : [[nominal[el], 1]];
        Object.keys(peaks).forEach(function (m) {
          opts.forEach(function (o) { var mm = +m + o[0]; next[mm] = (next[mm] || 0) + peaks[m] * o[1]; });
        });
        peaks = next;
      }
    });
    var list = Object.keys(peaks).map(function (m) { return { m: +m, p: peaks[m] }; }).sort(function (a, b) { return a.m - b.m; });
    var mx = Math.max.apply(null, list.map(function (x) { return x.p; }));
    return list.filter(function (x) { return x.p / mx > 0.001; }).map(function (x) { return { m: x.m, p: x.p, rel: 100 * x.p / mx }; });
  };
  P.heisenbergDu = function (m, dx) { return K.h / (4 * Math.PI * m * dx); };
  P.formulaCounts = function (f) { var out = {}, re = /([A-Z][a-z]?)(\d*)/g, m; while ((m = re.exec(f)) !== null) { if (!m[0]) break; out[m[1]] = (out[m[1]] || 0) + (m[2] ? +m[2] : 1); } return out; };
  P.molarMass = function (f, am) { var c = P.formulaCounts(f); return Object.keys(c).reduce(function (s, el) { return s + am[el] * c[el]; }, 0); };
  P.bondClass = function (d) { d = Math.round(Math.abs(d) * 100) / 100; return d <= 0.4 ? "nonpolar covalent" : d < 2.0 ? "polar covalent" : "ionic"; };

  if (!U || typeof document === "undefined") return { calc: P };

  /* ================================================================ shared bits */
  var el = U.el, sci = U.sci, num = U.num, fix = U.fix, SERIES = U.SERIES;
  var ATOM_COLOR = { H: ["#F4F5F7", "#8A94A3"], C: ["#3A3F47", "#1F2329"], O: ["#D0403A", "#9A2C27"], N: ["#3F6FD8", "#284C9E"], Ne: ["#F0A6C8", "#C2688F"], Cl: ["#5DBB63", "#3A8A40"], Na: ["#9B7BD0", "#6F52A6"], S: ["#E8C23A", "#B08F16"], Si: ["#D9B38C", "#A07F5C"], Ar: ["#A8DCE8", "#6BA9B8"] };
  function atomColors(e) { return ATOM_COLOR[e] || ["#C9CED6", "#7C8796"]; }
  function inkFor(e) { return e === "C" || e === "N" || e === "O" ? "#FFFFFF" : "#17212E"; }   // label contrast ≥ 4.5:1 on each fill
  function rng(seed) { var s = seed >>> 0; return function () { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; }; }
  function supsub(A, Z, sym, Q) { // stacked nuclide symbol as HTML
    var q = Q ? (Math.abs(Q) === 1 ? "" : Math.abs(Q)) + (Q > 0 ? "+" : MINUS) : "";
    return "<span class='nuc'><span class='nuc-az'><sup>" + A + "</sup><sub>" + Z + "</sub></span>" + sym + (q ? "<sup>" + q + "</sup>" : "") + "</span>";
  }

  /* ================================================================ t1-3 particle views of matter */
  mount.particleBox = function (host) {
    var SAMPLES = [
      { key: "a", truth: "el", units: [{ atoms: ["Ne"], n: 16 }], why: "Every unit is the same single kind of atom: a pure substance that can't be broken down, an <strong>element</strong> (like neon)." },
      { key: "b", truth: "el", units: [{ atoms: ["O", "O"], n: 11 }], why: "Every unit is the same molecule made of one kind of atom (O<sub>2</sub>): still an <strong>element</strong>. Diatomic elements are molecules, not compounds." },
      { key: "c", truth: "cp", units: [{ atoms: ["O", "H", "H"], n: 10 }], why: "Every unit is identical and contains two kinds of atoms bonded in a fixed ratio (H<sub>2</sub>O): a <strong>compound</strong>." },
      { key: "d", truth: "ho", units: [{ atoms: ["N", "N"], n: 9 }, { atoms: ["O", "O"], n: 5 }], why: "Two different kinds of units (N<sub>2</sub> and O<sub>2</sub>), spread evenly: a <strong>homogeneous mixture</strong>, like air." },
      { key: "e", truth: "he", units: [{ atoms: ["Si"], n: 14, region: "left" }, { atoms: ["O", "H", "H"], n: 8, region: "right" }], why: "Two kinds of units in separate regions: a <strong>heterogeneous mixture</strong>, like sand in water." },
      { key: "f", truth: "ho", units: [{ atoms: ["Na"], n: 4, q: "+" }, { atoms: ["Cl"], n: 4, q: MINUS }, { atoms: ["O", "H", "H"], n: 9 }], why: "Water molecules mixed evenly with Na<sup>+</sup> and Cl<sup>−</sup> ions from dissolved salt: a <strong>homogeneous mixture</strong> (a solution). Evaporation would separate it." }
    ];
    var NAMES = { el: "element", cp: "compound", ho: "homogeneous mixture", he: "heterogeneous mixture" };
    var st = { i: 0, seed: 7, answered: false };
    var ui = U.shell(host, { title: "Explorer: classify matter from a particle view",
      intro: "Each box is a zoomed-in view of a sample (circles are atoms, touching circles are bonded). Decide what it is, then check.",
      source: "Source: textbook §1.3 and Fig. 1.2 (TB PDF p.39–44, printed 5–10), textbook preview. Drawings are schematic." });
    U.select(ui.controls, { label: "Sample", testid: "pb-sample", value: "0", options: SAMPLES.map(function (s, i) { return [String(i), "Sample " + s.key.toUpperCase()]; }), onChange: function (v) { st.i = +v; st.answered = false; draw(); } });
    var row = el("div", { class: "ctl-row" }); ui.controls.appendChild(row);
    U.button(row, "Draw a new arrangement", "btn-pb-shuffle", function () { st.seed += 13; draw(); });
    var quiz = el("div", { class: "ctl-row", role: "group", "aria-label": "Your classification" }); ui.presets.appendChild(el("p", { class: "xp-presets-label" }, "Your answer")); ui.presets.appendChild(quiz);
    Object.keys(NAMES).forEach(function (k) { U.button(quiz, NAMES[k], "pb-answer-" + k, function () { st.answered = k; draw(); }); });
    function place(units, W, Hh) {
      var R = rng(st.seed + st.i * 101), items = [], tries = 0;
      units.forEach(function (u) {
        for (var k = 0; k < u.n; k++) {
          var ok = false, x, y;
          while (!ok && tries < 5000) {
            tries++;
            var x0 = u.region === "left" ? 20 : u.region === "right" ? W / 2 + 20 : 20, x1 = u.region === "left" ? W / 2 - 30 : W - 40;
            x = x0 + R() * (x1 - x0); y = 20 + R() * (Hh - 40);
            ok = items.every(function (it) { return Math.hypot(it.x - x, it.y - y) > 30; });
          }
          items.push({ x: x, y: y, atoms: u.atoms, q: u.q, rot: R() * Math.PI * 2 });
        }
      });
      return items;
    }
    function atomSVG(a, cx, cy, q) {
      var r = a === "H" ? 6.5 : 9, col = atomColors(a);
      return "<circle cx='" + cx.toFixed(1) + "' cy='" + cy.toFixed(1) + "' r='" + r + "' fill='" + col[0] + "' stroke='" + col[1] + "' stroke-width='1.2'/>" +
        "<text x='" + cx.toFixed(1) + "' y='" + (cy + 3.2).toFixed(1) + "' text-anchor='middle' class='atom-label' style='fill:" + inkFor(a) + "'>" + a + (q ? "<tspan class='sup' dy='-4'>" + q + "</tspan>" : "") + "</text>";
    }
    function draw() {
      var S = SAMPLES[st.i], W = 420, Hh = 250, items = place(S.units, W, Hh), svg = "<rect x='2' y='2' width='" + (W - 4) + "' height='" + (Hh - 4) + "' fill='#FFFFFF' stroke='#B7BDC7'/>";
      if (S.units.some(function (u) { return u.region; })) svg += "<line x1='" + W / 2 + "' x2='" + W / 2 + "' y1='8' y2='" + (Hh - 8) + "' stroke='#E5E7EB'/>";
      items.forEach(function (it) {
        var A = it.atoms;
        if (A.length === 1) svg += atomSVG(A[0], it.x, it.y, it.q);
        else if (A.length === 2) {                                    // diatomic: two touching atoms
          var dx = 7.5 * Math.cos(it.rot), dy = 7.5 * Math.sin(it.rot);
          svg += atomSVG(A[0], it.x - dx, it.y - dy) + atomSVG(A[1], it.x + dx, it.y + dy);
        } else {                                                     // bent triatomic (water): central atom first
          svg += atomSVG(A[1], it.x + 12 * Math.cos(it.rot + 0.9), it.y + 12 * Math.sin(it.rot + 0.9)) +
                 atomSVG(A[2], it.x + 12 * Math.cos(it.rot - 0.9), it.y + 12 * Math.sin(it.rot - 0.9)) + atomSVG(A[0], it.x, it.y);
        }
      });
      ui.view.innerHTML = U.svgWrap(W, Hh, "Particle view of sample " + S.key.toUpperCase(), svg);
      if (st.answered) {
        var right = st.answered === S.truth;
        ui.readout.innerHTML = (right ? "<strong>✓ Right: " : "<strong>✗ Not quite: ") + NAMES[S.truth] + ".</strong> " + S.why +
          " <span class='xp-caption'>Fig. 1.2's questions: different kinds of units present? → mixture; one kind of unit with more than one kind of atom? → compound.</span>";
      } else ui.readout.innerHTML = "Choose an answer. Look at the <em>units</em> (single atoms or bonded groups): are they all identical? Does one unit contain more than one kind of atom? Are different units spread evenly?";
      U.kvSet(ui.kv, [["Kinds of units", String(S.units.length)], ["Atoms per unit", S.units.map(function (u) { return u.atoms.length; }).join(", ")]]);
      ui.table.innerHTML = U.tableHTML(["Sample", "Classification", "Reason"], SAMPLES.map(function (s) { return [s.key.toUpperCase(), NAMES[s.truth], s.why]; }));
      ui.details.hidden = !st.answered;
    }
    draw();
  };

  /* ================================================================ t1-4 states of matter (schematic particle motion) */
  mount.states = function (host) {
    var W = 420, Hh = 260, N = 36, R = 7, st = { T: 15, playing: false, prev: "solid", raf: 0, parts: [] };
    var ui = U.shell(host, { title: "Explorer: solid, liquid, gas",
      intro: "Raise the temperature (a schematic scale, not real degrees) and watch the particles. Press Play to animate; Pause stops all motion.",
      source: "Source: textbook §1.4, Figs. 1.9–1.10 (TB PDF p.48–49, printed 14–15), textbook preview. Schematic model." });
    var sl = U.slider(ui.controls, { label: "Temperature (schematic)", testid: "states-T", min: 0, max: 100, step: 1, value: st.T, format: function (v) { return v; }, onInput: function (v) { st.T = v; update(); } });
    var row = el("div", { class: "ctl-row" }); ui.controls.appendChild(row);
    var play = U.button(row, "Play", "btn-states-play", function () { st.playing = !st.playing; play.textContent = st.playing ? "Pause" : "Play"; if (st.playing && !U.reduceMotion) loop(); }, "primary");
    U.presetButtons(ui, "states", [["Solid", 10], ["Liquid", 50], ["Gas", 90]], function (T) { st.T = T; sl.set(T); update(); });
    var r0 = rng(3);
    for (var i = 0; i < N; i++) { var gx = i % 6, gy = Math.floor(i / 6); st.parts.push({ lx: 140 + gx * 2.2 * R, ly: Hh - 30 - gy * 2.2 * R, x: 140 + gx * 2.2 * R, y: Hh - 30 - gy * 2.2 * R, vx: r0() - 0.5, vy: r0() - 0.5 }); }
    function state() { return st.T < 30 ? "solid" : st.T < 70 ? "liquid" : "gas"; }
    function stepPhysics() {
      var s = state(), jit = 0.4 + st.T / 25;
      st.parts.forEach(function (p) {
        if (s === "solid") { p.x = p.lx + (Math.random() - 0.5) * jit; p.y = p.ly + (Math.random() - 0.5) * jit; }
        else {
          var sp = s === "liquid" ? 0.8 + st.T / 60 : 1.5 + st.T / 25;
          p.vx += (Math.random() - 0.5) * 0.6; p.vy += (Math.random() - 0.5) * 0.6 + (s === "liquid" ? 0.08 : 0);
          var v = Math.hypot(p.vx, p.vy) || 1; p.vx = p.vx / v * sp; p.vy = p.vy / v * sp;
          p.x += p.vx; p.y += p.vy;
          var top = s === "liquid" ? Hh - 110 : R + 2;
          if (p.x < R + 2) { p.x = R + 2; p.vx = Math.abs(p.vx); } if (p.x > W - R - 2) { p.x = W - R - 2; p.vx = -Math.abs(p.vx); }
          if (p.y < top) { p.y = top; p.vy = Math.abs(p.vy); } if (p.y > Hh - R - 2) { p.y = Hh - R - 2; p.vy = -Math.abs(p.vy); }
        }
      });
    }
    function render() {
      var svg = "<rect x='2' y='2' width='" + (W - 4) + "' height='" + (Hh - 4) + "' fill='#FFFFFF' stroke='#B7BDC7'/>";
      st.parts.forEach(function (p) { svg += "<circle cx='" + p.x.toFixed(1) + "' cy='" + p.y.toFixed(1) + "' r='" + R + "' fill='#6DA7EC' stroke='#1C5CAB' stroke-width='1'/>"; });
      ui.view.innerHTML = U.svgWrap(W, Hh, "Particles in the " + state() + " state", svg);
    }
    function describe() {
      var s = state(), change = "";
      var names = { "solid>liquid": "melting (absorbs energy)", "liquid>solid": "freezing (releases energy)", "liquid>gas": "vaporization (absorbs energy)", "gas>liquid": "condensation (releases energy)", "solid>gas": "sublimation (absorbs energy)", "gas>solid": "deposition (releases energy)" };
      if (s !== st.prev) { change = names[st.prev + ">" + s]; st.prev = s; }
      var desc = { solid: "ordered, touching, vibrating in place: definite shape and volume", liquid: "touching but disordered, sliding past each other: definite volume, no fixed shape", gas: "far apart, moving freely: fills the container, highly compressible" };
      ui.readout.innerHTML = "<strong>" + s + "</strong>: particles are " + desc[s] + "." + (change ? " Last change: <strong>" + change + "</strong>." : "");
      U.kvSet(ui.kv, [["State", s], ["Particle spacing", s === "gas" ? "large" : "small"], ["Particle motion", s === "solid" ? "vibration" : s === "liquid" ? "tumbling" : "free flight"]]);
      ui.table.innerHTML = U.tableHTML(["Change", "Direction", "Energy"], [["melting", "solid → liquid", "absorbed"], ["freezing", "liquid → solid", "released"], ["vaporization", "liquid → gas", "absorbed"], ["condensation", "gas → liquid", "released"], ["sublimation", "solid → gas", "absorbed"], ["deposition", "gas → solid", "released"]]);
    }
    function update() {
      if (state() === "solid") st.parts.forEach(function (p) { p.x = p.lx; p.y = p.ly; });
      if (!st.playing || U.reduceMotion) { for (var k = 0; k < (state() === "solid" ? 1 : 60); k++) stepPhysics(); render(); }
      describe();
    }
    function loop() {
      if (!st.playing || !document.body.contains(host)) return;
      if (host.offsetParent !== null) { stepPhysics(); render(); }
      st.raf = window.requestAnimationFrame(loop);
    }
    update();
  };

  /* ================================================================ t1-5 kinetic energy */
  mount.kinetic = function (host) {
    var OBJ = { electron: [9.109e-31, "an electron", 2.0e6], baseball: [0.145, "a baseball (145 g)", 40.0], tennis: [0.0580, "a tennis ball (58.0 g)", 57.5], sprinter: [60.0, "a 60.0 kg sprinter", 10.0], car: [1.50e3, "a 1500 kg car", 25.0] };
    var st = { o: "baseball", logu: Math.log10(40.0), mf: 1 };
    var ui = U.shell(host, { title: "Explorer: kinetic energy, KE = ½mu²",
      intro: "Pick an object and a speed. Then use the doubling buttons: which doubles KE, and which quadruples it?",
      source: "Source: textbook §1.5, Eq. 1.3 (TB PDF p.50, printed 16), textbook preview. Energy landmarks are computed with the same equation or from the lecture (photon energy, Day 3 p.17)." });
    var sO = U.select(ui.controls, { label: "Object", testid: "ke-object", value: st.o, options: Object.keys(OBJ).map(function (k) { return [k, OBJ[k][1]]; }), onChange: function (v) { st.o = v; st.mf = 1; st.logu = Math.log10(OBJ[v][2]); sl.set(st.logu); draw(); } });
    var sl = U.slider(ui.controls, { label: "Speed u", testid: "ke-speed", min: -1, max: 7.5, step: 0.01, value: st.logu, format: function (v) { return sci(Math.pow(10, v)) + " m/s"; }, onInput: function (v) { st.logu = v; draw(); } });
    var row = el("div", { class: "ctl-row" }); ui.controls.appendChild(row);
    var last = null;
    U.button(row, "Double the speed", "btn-ke-2u", function () { last = ke(); st.logu = Math.min(7.5, st.logu + Math.log10(2)); sl.set(st.logu); draw("speed"); });
    U.button(row, "Double the mass", "btn-ke-2m", function () { last = ke(); st.mf *= 2; draw("mass"); });
    function ke() { return 0.5 * OBJ[st.o][0] * st.mf * Math.pow(Math.pow(10, st.logu), 2); }
    function draw(what) {
      var m = OBJ[st.o][0] * st.mf, u = Math.pow(10, st.logu), E = 0.5 * m * u * u;
      var x = function (e) { return 30 + (Math.log10(e) + 26) / 34 * 540; };
      var s = "<line class='baseline' x1='30' x2='570' y1='60' y2='60'/>";
      for (var k = -26; k <= 8; k += 4) s += "<line class='tickmark' x1='" + x(Math.pow(10, k)) + "' x2='" + x(Math.pow(10, k)) + "' y1='60' y2='66'/><text class='tick' x='" + x(Math.pow(10, k)) + "' y='80' text-anchor='middle'>10<tspan class='sup' dy='-5'>" + (k < 0 ? MINUS + (-k) : k) + "</tspan></text>";
      var marks = [[3.75e-19, "one green photon"], [116, "fast pitch"], [4.69e5, "car at 25 m/s"]];
      marks.forEach(function (mk, i) { s += "<line class='landmark' x1='" + x(mk[0]) + "' x2='" + x(mk[0]) + "' y1='40' y2='60'/><text class='tick muted' x='" + x(mk[0]) + "' y='" + (34 - 12 * (i % 2)) + "' text-anchor='middle'>" + mk[1] + "</text>"; });
      var lx = Math.max(30, Math.min(570, x(E)));
      s += "<path class='marker-head' d='M" + (lx - 7) + " 100 h14 l-7 -10 z'/><text class='tick strong' x='" + Math.min(500, Math.max(80, lx)) + "' y='118' text-anchor='middle'>KE = " + U.sciSVG(E, 3, "J") + "</text><text class='tick muted' x='30' y='136'>energy, J (log scale)</text>";
      ui.view.innerHTML = U.svgWrap(600, 140, "Kinetic energy on a log scale: " + E.toExponential(2) + " joules.", s);
      var ratio = what && last ? " That multiplied KE by " + num(E / last, 3) + (what === "speed" ? " (2² = 4)." : " (KE is proportional to m).") : "";
      ui.readout.innerHTML = "KE = ½ × " + sci(m, 4) + " kg × (" + sci(u) + " m/s)<sup>2</sup> = <strong>" + sci(E) + " J</strong> for " + OBJ[st.o][1] + (st.mf > 1 ? " with " + st.mf + "× the mass" : "") + "." + ratio;
      U.kvSet(ui.kv, [["m", sci(m, 4) + " kg"], ["u", sci(u) + " m/s"], ["KE", sci(E) + " J"]]);
      ui.table.innerHTML = U.tableHTML(["Object", "m (kg)", "typical u (m/s)", "KE (J)"], Object.keys(OBJ).map(function (k) { var o = OBJ[k]; return [o[1], sci(o[0], 4), sci(o[2]), sci(0.5 * o[0] * o[2] * o[2])]; }));
    }
    draw();
  };

  /* ================================================================ t1-6 formulas and models */
  mount.models = function (host, D) {
    var mols = D.molecules, st = { i: 5, view: "ball" };
    var ui = U.shell(host, { title: "Explorer: formulas and models",
      intro: "Switch between representations of the same molecule. Colors follow the textbook's palette (H white, C black, O red, N blue); letters label every atom.",
      source: "Source: textbook §1.6, Fig. 1.15 (TB PDF p.51–52, printed 17–18), textbook preview. 2-D coordinates generated with RDKit (background); real molecules are 3-D." });
    U.select(ui.controls, { label: "Molecule", testid: "mol-select", value: String(st.i), options: mols.map(function (m, i) { return [String(i), m.name]; }), onChange: function (v) { st.i = +v; draw(); } });
    U.radios(ui.controls, { label: "Representation", testid: "mol-view", value: st.view, options: [["structural", "structural formula"], ["ball", "ball-and-stick"], ["space", "space-filling"]], onChange: function (v) { st.view = v; draw(); } });
    var VDW = { H: 1.10, C: 1.70, N: 1.55, O: 1.52 };
    function draw() {
      var m = mols[st.i], W = 420, Hh = 260, xs = m.atoms.map(function (a) { return a.x; }), ys = m.atoms.map(function (a) { return a.y; });
      var minx = Math.min.apply(null, xs), maxx = Math.max.apply(null, xs), miny = Math.min.apply(null, ys), maxy = Math.max.apply(null, ys);
      var span = Math.max(maxx - minx, maxy - miny, 1.5), sc = Math.min((W - 90) / span, (Hh - 90) / span, 60);
      var X0 = function (x) { return W / 2 + (x - (minx + maxx) / 2) * sc; }, Y0 = function (y) { return Hh / 2 - (y - (miny + maxy) / 2) * sc; };
      var s = "<rect x='2' y='2' width='" + (W - 4) + "' height='" + (Hh - 4) + "' fill='#FFFFFF' stroke='#ECEEF2'/>";
      if (st.view === "space") {
        var order = m.atoms.map(function (a, i) { return i; }).sort(function (a, b) { return (m.atoms[a].el === "H") - (m.atoms[b].el === "H"); });
        order.forEach(function (i) { var a = m.atoms[i], c = atomColors(a.el); s += "<circle cx='" + X0(a.x) + "' cy='" + Y0(a.y) + "' r='" + (VDW[a.el] || 1.6) * sc * 0.62 + "' fill='" + c[0] + "' stroke='" + c[1] + "' stroke-width='1'/>"; });
        m.atoms.forEach(function (a) { s += "<text x='" + X0(a.x) + "' y='" + (Y0(a.y) + 4) + "' text-anchor='middle' class='atom-label' style='fill:" + inkFor(a.el) + "'>" + a.el + "</text>"; });
      } else {
        m.bonds.forEach(function (b) {
          var A = m.atoms[b.a], B = m.atoms[b.b], x1 = X0(A.x), y1 = Y0(A.y), x2 = X0(B.x), y2 = Y0(B.y), dx = x2 - x1, dy = y2 - y1, L = Math.hypot(dx, dy) || 1, nx = -dy / L * 3.5, ny = dx / L * 3.5;
          for (var k = 0; k < b.order; k++) { var o = (k - (b.order - 1) / 2) * 2; s += "<line x1='" + (x1 + nx * o) + "' y1='" + (y1 + ny * o) + "' x2='" + (x2 + nx * o) + "' y2='" + (y2 + ny * o) + "' stroke='#475467' stroke-width='" + (st.view === "ball" ? 3 : 1.6) + "'/>"; }
        });
        m.atoms.forEach(function (a) {
          if (st.view === "ball") { var c = atomColors(a.el); s += "<circle cx='" + X0(a.x) + "' cy='" + Y0(a.y) + "' r='" + (a.el === "H" ? 9 : 13) + "' fill='" + c[0] + "' stroke='" + c[1] + "' stroke-width='1.2'/>"; }
          else s += "<circle cx='" + X0(a.x) + "' cy='" + Y0(a.y) + "' r='10' fill='#FFFFFF'/>";
          s += "<text x='" + X0(a.x) + "' y='" + (Y0(a.y) + 4.5) + "' text-anchor='middle' class='" + (st.view === "ball" ? "atom-label" : "tick strong") + "' style='fill:" + (st.view === "ball" ? inkFor(a.el) : "#17212E") + ";font-size:" + (st.view === "ball" ? 10 : 15) + "px'>" + a.el + "</text>";
        });
      }
      ui.view.innerHTML = U.svgWrap(W, Hh, m.name + " as a " + st.view + " representation", s);
      var counts = P.formulaCounts(m.formula);
      ui.readout.innerHTML = m.name + ": molecular formula <strong>" + U.formulaHTML(Object.keys(counts).map(function (k) { return [k, counts[k]]; })) + "</strong>; empirical formula " + U.formulaHTML(Object.keys(P.formulaCounts(m.empirical)).map(function (k) { return [k, P.formulaCounts(m.empirical)[k]]; })) +
        "; condensed " + m.condensed.replace(/(\d)/g, "<sub>$1</sub>") + ". " + (st.view === "ball" ? "Ball-and-stick shows the bond angles clearly, but the atoms look too far apart." : st.view === "space" ? "Space-filling shows the overall shape, with atoms overlapping as they really do, but hides some atoms." : "The structural formula shows which atoms are bonded (double lines are double bonds).");
      U.kvSet(ui.kv, Object.keys(counts).map(function (k) { return [k + " atoms", String(counts[k])]; }));
      ui.table.innerHTML = U.tableHTML(["Molecule", "Molecular formula", "Empirical formula", "Condensed"], mols.map(function (x) {
        var c1 = P.formulaCounts(x.formula), c2 = P.formulaCounts(x.empirical);
        return [x.name, U.formulaHTML(Object.keys(c1).map(function (k) { return [k, c1[k]]; })), U.formulaHTML(Object.keys(c2).map(function (k) { return [k, c2[k]]; })), x.condensed.replace(/(\d)/g, "<sub>$1</sub>")]; }));
    }
    draw();
  };

  /* ================================================================ t1-7 significant figures */
  mount.sigfigs = function (host) {
    var st = { a: "0.004060", x: "12.3", op: "*", y: "0.0450" };
    var ui = U.shell(host, { title: "Explorer: which digits are significant?",
      intro: "Type a measured value to see which digits count. Then combine two values: the calculator applies the × ÷ rule or the + − rule, and rounds only at the end (ties to even, as the textbook does).",
      source: "Source: textbook §1.7 (TB PDF p.56–59, printed 22–25), textbook preview." });
    var inA = el("div", { class: "ctl ctl-num" }, "<label for='sf-a'>A measured value</label><input id='sf-a' type='text' inputmode='decimal' data-testid='input-sf-value' value='" + st.a + "'>");
    ui.controls.appendChild(inA);
    inA.querySelector("input").addEventListener("input", function (e) { st.a = e.target.value; draw(); });
    var calc = el("div", { class: "ctl" }, "<label for='sf-x'>Calculator</label><div class='ctl-row'><input id='sf-x' type='text' inputmode='decimal' data-testid='input-sf-x' value='" + st.x + "' style='width:7em'>" +
      "<select id='sf-op' data-testid='select-sf-op' aria-label='operation'><option value='*'>×</option><option value='/'>÷</option><option value='+'>+</option><option value='-'>−</option></select>" +
      "<input id='sf-y' type='text' inputmode='decimal' data-testid='input-sf-y' value='" + st.y + "' style='width:7em' aria-label='second value'></div>");
    ui.controls.appendChild(calc);
    ["sf-x", "sf-op", "sf-y"].forEach(function (id) { calc.querySelector("#" + id).addEventListener("input", function () { st.x = calc.querySelector("#sf-x").value; st.op = calc.querySelector("#sf-op").value; st.y = calc.querySelector("#sf-y").value; draw(); }); });
    calc.querySelector("#sf-op").addEventListener("change", function () { st.op = calc.querySelector("#sf-op").value; draw(); });
    U.presetButtons(ui, "sf", [["0.0592", "0.0592"], ["3.00 × 10⁸", "3.00e8"], ["101.3", "101.3"], ["96,500", "96500"], ["2.5270", "2.5270"]], function (v) { st.a = v; inA.querySelector("input").value = v; draw(); });
    function draw() {
      var I = P.sigInfo(st.a), html = "";
      if (!I) html = "<p class='xp-caption'>Type a number such as 0.0810 or 3.00e8.</p>";
      else {
        html = "<p class='sigfig-digits' aria-label='digits'>" + (I.sign === "-" ? MINUS : "") + I.digits.map(function (d) { return "<span class='" + (d.kind === "sig" ? "sf" : d.kind === "amb" ? "amb" : d.kind === "lead" ? "nsf" : "") + "'>" + d.ch + "</span>"; }).join("") + (I.exp ? " × 10<sup>" + String(I.exp).replace("-", MINUS) + "</sup>" : "") + "</p>" +
          "<p class='xp-caption'><span class='sigfig-digits' style='font-size:14px'><span class='sf'>green</span></span> = significant; grey = leading zeros (place the decimal point only); <span class='sigfig-digits' style='font-size:14px'><span class='amb'>amber</span></span> = trailing zeros with no decimal point (ambiguous).</p>";
      }
      var C = P.combine(st.x, st.op, st.y), opSym = { "*": "×", "/": "÷", "+": "+", "-": MINUS }[st.op];
      if (C) {
        var A = P.sigInfo(st.x), B = P.sigInfo(st.y);
        html += "<p class='xp-caption'><strong>Calculator:</strong> " + st.x + " " + opSym + " " + st.y + " = " + (+C.raw.toPrecision(10)) + " (unrounded). " +
          (C.rule === "significant figures" ? "× and ÷ keep the fewest significant figures: " + A.sf + " and " + B.sf + " → " + C.keep + ". Result: <strong>" + C.text + "</strong>."
            : "+ and − keep the fewest decimal places: " + Math.max(0, A.decimals) + " and " + Math.max(0, B.decimals) + " → " + Math.max(0, C.keep) + ". Result: <strong>" + C.text + "</strong>.") + "</p>";
      }
      ui.view.innerHTML = html;
      ui.readout.innerHTML = I ? st.a + " has <strong>" + I.sf + " significant figure" + (I.sf === 1 ? "" : "s") + "</strong>" + (I.ambiguous ? " (plus " + I.ambiguous + " ambiguous trailing zero" + (I.ambiguous > 1 ? "s" : "") + ": write it in scientific notation to say which count)" : "") + ". In scientific notation: " + P.formatSig(I.value, I.sf) + "." : "";
      U.kvSet(ui.kv, I ? [["Significant figures", String(I.sf)], ["Last digit's place", I.decimals > 0 ? "10<sup>" + MINUS + I.decimals + "</sup>" : "10<sup>" + (-I.decimals) + "</sup>"]] : []);
      ui.table.innerHTML = U.tableHTML(["Rule (textbook §1.7)", "Example", "Sig figs"], [["leading zeros never count", "0.0592", "3"], ["zeros after a decimal point and a nonzero digit count", "3.00 × 10<sup>8</sup>", "3"], ["trailing zeros without a decimal point are ambiguous", "96,500", "3 to 5"], ["captive zeros count", "101.3", "4"]]);
    }
    draw();
  };

  /* ================================================================ t1-8 unit conversions */
  mount.units = function (host) {
    var st = { cat: "length", v: "26.2", from: "mi", to: "km", flip: false };
    var ui = U.shell(host, { title: "Explorer: conversion factors that cancel",
      intro: "Choose a quantity type, a value, and units. The chain shows every factor with the canceled units struck through. Try “Flip the factor” to see what a wrong setup looks like.",
      source: "Source: textbook §1.8 and Table 1.3 (TB PDF p.54, p.60–64; printed 20, 26–30), textbook preview." });
    var sCat = U.select(ui.controls, { label: "Quantity", testid: "units-cat", value: st.cat, options: [["length", "length"], ["mass", "mass"], ["volume", "volume"], ["speed", "speed"], ["density", "density"], ["temperature", "temperature"]], onChange: function (v) { st.cat = v; var u = unitList(); st.from = u[0]; st.to = u[1]; rebuild(); draw(); } });
    var inV = el("div", { class: "ctl ctl-num" }, "<label for='un-v'>Value</label><input id='un-v' type='text' inputmode='decimal' data-testid='input-units-value' value='" + st.v + "'>");
    ui.controls.appendChild(inV);
    inV.querySelector("input").addEventListener("input", function (e) { st.v = e.target.value; draw(); });
    var fromWrap = el("div"), toWrap = el("div"); ui.controls.appendChild(fromWrap); ui.controls.appendChild(toWrap);
    var row = el("div", { class: "ctl-row" }); ui.controls.appendChild(row);
    var flipB = U.button(row, "Flip the factor", "btn-units-flip", function () { st.flip = !st.flip; flipB.setAttribute("aria-pressed", st.flip ? "true" : "false"); draw(); });
    U.presetButtons(ui, "units", [["26.2 mi → km", ["length", "26.2", "mi", "km"]], ["355 mL → qt", ["volume", "355", "mL", "qt"]], ["98.6 °F → °C", ["temperature", "98.6", "°F", "°C"]], ["65 mi/h → m/s", ["speed", "65", "mi/h", "m/s"]], ["19.3 g/cm³ → kg/m³", ["density", "19.3", "g/cm³", "kg/m³"]]],
      function (p) { st.cat = p[0]; st.v = p[1]; st.from = p[2]; st.to = p[3]; st.flip = false; sCat.value = p[0]; inV.querySelector("input").value = p[1]; rebuild(); draw(); });
    function unitList() { return st.cat === "temperature" ? ["K", "°C", "°F"] : Object.keys(P.UNITS[st.cat].units); }
    function rebuild() {
      fromWrap.innerHTML = ""; toWrap.innerHTML = "";
      U.select(fromWrap, { label: "From", testid: "units-from", value: st.from, options: unitList().map(function (u) { return [u, u]; }), onChange: function (v) { st.from = v; draw(); } });
      U.select(toWrap, { label: "To", testid: "units-to", value: st.to, options: unitList().map(function (u) { return [u, u]; }), onChange: function (v) { st.to = v; draw(); } });
    }
    function frac(n, d, cancelN, cancelD) { return "<span class='frac'><span class='num'>" + (cancelN ? n.replace(/ ([^ ]+)$/, " <span class='cancel'>$1</span>") : n) + "</span><span class='den'>" + (cancelD ? d.replace(/ ([^ ]+)$/, " <span class='cancel'>$1</span>") : d) + "</span></span>"; }
    function draw() {
      var I = P.sigInfo(st.v), v = I ? I.value : NaN, html = "";
      if (!I) { ui.view.innerHTML = "<p class='xp-caption'>Enter a number.</p>"; ui.readout.innerHTML = ""; return; }
      if (st.cat === "temperature") {
        var r = P.convert("temperature", v, st.from, st.to), steps = [];
        if (st.from === "°F") steps.push("T(°C) = (5/9)[T(°F) − 32] = (5/9)(" + st.v + " − 32) = " + fix(r.celsius, 2) + " °C");
        if (st.from === "K") steps.push("T(°C) = T(K) − 273.15 = " + fix(r.celsius, 2) + " °C");
        if (st.to === "K") steps.push("T(K) = T(°C) + 273.15 = " + fix(r.value, 2) + " K");
        if (st.to === "°F") steps.push("T(°F) = (9/5)T(°C) + 32 = " + fix(r.value, 2) + " °F");
        html = "<p class='chain'>" + (steps.join("<br>") || "Same unit.") + "</p><p class='xp-caption'>Temperature isn't converted with a single ratio: the zero points differ (Table 1.3).</p>";
        ui.view.innerHTML = html;
        ui.readout.innerHTML = st.v + " " + st.from + " = <strong>" + fix(r.value, 1) + " " + st.to + "</strong>.";
        U.kvSet(ui.kv, []); ui.table.innerHTML = U.tableHTML(["°F", "°C", "K"], [["32", "0", "273.15"], ["212", "100", "373.15"], ["98.6", "37.0", "310.2"], ["−459.67", "−273.15", "0"]]); return;
      }
      var C = P.UNITS[st.cat], base = C.base, f1 = C.units[st.from], f2 = C.units[st.to], parts = [];
      var numStr = function (x) { return x === 1 ? "1" : Math.abs(Math.log10(x)) >= 4 ? sci(x, 4) : num(x, 4); };
      if (st.from !== base) parts.push(st.flip ? frac("1 " + st.from, numStr(f1) + " " + base, false, false) : frac(numStr(f1) + " " + base, "1 " + st.from, st.to !== base, true));
      if (st.to !== base) parts.push(frac("1 " + st.to, numStr(f2) + " " + base, false, true));
      var result = st.flip ? v / f1 / f2 : v * f1 / f2;
      var sf = I.sf, exact = !!(C.exact[st.from] && C.exact[st.to]);
      html = "<div class='chain'><span>" + st.v + " <span class='" + (st.flip ? "" : "cancel") + "'>" + st.from + "</span></span>" + parts.map(function (p) { return "<span aria-hidden='true'>×</span>" + p; }).join("") + "<span>= " + (st.flip ? "?" : P.formatSig(result, sf) + " " + st.to) + "</span></div>";
      if (st.flip) html += "<p class='xp-caption' style='color:#8E1C13'>✗ The units no longer cancel: you'd be left with " + st.from + "<sup>2</sup> in the answer's units. A leftover unit means the factor is upside down.</p>";
      html += "<p class='xp-caption'>Table 1.3: " + C.note + ". " + (exact ? "Every factor here is exact, so the answer keeps the value's " + sf + " significant figures." : "A measured factor (4 s.f.) can limit the result; here the value's " + sf + " s.f. is the weak link.") + "</p>";
      ui.view.innerHTML = html;
      ui.readout.innerHTML = st.flip ? "Flipped factor: the setup is wrong. Put the unit you're converting <em>from</em> in the denominator." : st.v + " " + st.from + " = <strong>" + P.formatSig(result, sf) + " " + st.to + "</strong>.";
      U.kvSet(ui.kv, [["Significant figures kept", String(sf)], ["Factors exact?", exact ? "yes" : "no (defined to 4 s.f.)"]]);
      ui.table.innerHTML = U.tableHTML(["Unit", "In " + base], Object.keys(C.units).map(function (u) { return [u, numStr(C.units[u])]; }));
    }
    rebuild(); draw();
  };

  /* ================================================================ t1-9 statistics */
  function niceTicks(lo, hi, count) {
    // Axis ticks at round values (1, 2, or 5 times a power of ten) covering [lo, hi].
    var raw = (hi - lo) / count, mag = Math.pow(10, Math.floor(Math.log10(raw))), f = raw / mag;
    var step = (f < 1.5 ? 1 : f < 3.5 ? 2 : f < 7.5 ? 5 : 10) * mag, out = [];
    for (var v = Math.ceil(lo / step - 1e-9) * step; v <= hi + step * 1e-9; v += step) out.push(Math.round(v / step) * step);
    return { values: out, decimals: Math.max(0, -Math.floor(Math.log10(step) + 1e-9)) };
  }
  function farthest(xs, A) {
    // Name the value Grubbs' test examines; when two values tie for farthest, say so.
    var far = Math.abs(xs[A.suspect] - A.mean), tied = xs.filter(function (x) { return Math.abs(Math.abs(x - A.mean) - far) < 1e-9 * Math.max(1, far); });
    var uniq = tied.filter(function (x, i) { return tied.indexOf(x) === i; });
    return uniq.length > 1 ? "values (" + uniq.join(" and ") + ", equally far from the mean)" : "value (" + xs[A.suspect] + ")";
  }
  mount.stats = function (host) {
    var PRESETS = [["River water O₂ (mg/L)", "12.3, 12.6, 12.4, 12.5, 12.7"], ["Balance check (g)", "5.02, 5.05, 5.03, 5.04, 5.21"], ["Only four values", "4.61, 4.63, 4.60, 4.64"], ["Lab titrations (mL)", "24.1, 24.3, 24.2, 24.0, 24.4, 24.2"]];
    var st = { text: PRESETS[0][1] };
    var ui = U.shell(host, { title: "Explorer: mean, standard deviation, confidence interval, and Grubbs' test",
      intro: "Edit the data (commas or spaces between values). The dot plot shows the mean, a ±s band, and the 95% confidence interval for the mean.",
      source: "Source: textbook §1.9, Eqs. 1.5–1.8, Tables 1.5 and 1.7 (TB PDF p.65–70, printed 31–36), textbook preview. For n − 1 values not in Table 1.5, t is computed from the t distribution (background)." });
    var box = el("div", { class: "ctl" }, "<label for='st-data'>Data</label><textarea id='st-data' class='stat-data' data-testid='input-stats-data'>" + st.text + "</textarea>");
    ui.controls.appendChild(box);
    box.querySelector("textarea").addEventListener("input", function (e) { st.text = e.target.value; draw(); });
    U.presetButtons(ui, "stats", PRESETS, function (t) { st.text = t; box.querySelector("textarea").value = t; draw(); });
    function draw() {
      var xs = st.text.split(/[\s,;]+/).map(function (s) { return parseFloat(s.replace(/[−]/g, "-")); }).filter(function (x) { return isFinite(x); });
      var A = P.analyze(xs);
      if (!A) { ui.view.innerHTML = "<p class='xp-caption'>Enter at least two numbers.</p>"; ui.readout.innerHTML = ""; U.kvSet(ui.kv, []); return; }
      var lo = Math.min.apply(null, xs), hi = Math.max.apply(null, xs), pad = (hi - lo || 1) * 0.35, x0 = lo - pad, x1 = hi + pad, W = 600, Hh = 150;
      var X0 = function (x) { return 30 + (x - x0) / (x1 - x0) * (W - 60); };
      var s = "<rect x='" + X0(A.mean - A.s) + "' y='30' width='" + (X0(A.mean + A.s) - X0(A.mean - A.s)) + "' height='60' fill='#E8EEFB'/>" +
        "<rect x='" + X0(A.mean - A.half) + "' y='52' width='" + (X0(A.mean + A.half) - X0(A.mean - A.half)) + "' height='16' fill='#86B6EF'/>" +
        "<line x1='" + X0(A.mean) + "' x2='" + X0(A.mean) + "' y1='24' y2='96' stroke='#17212E' stroke-width='2'/>" +
        "<line class='baseline' x1='30' x2='" + (W - 30) + "' y1='110' y2='110'/>";
      var T = niceTicks(x0, x1, 5);
      T.values.forEach(function (tv) { s += "<line class='tickmark' x1='" + X0(tv) + "' x2='" + X0(tv) + "' y1='110' y2='115'/><text class='tick' x='" + X0(tv) + "' y='128' text-anchor='middle'>" + tv.toFixed(T.decimals) + "</text>"; });
      var stack = {};
      xs.forEach(function (x, i) { var key = x.toFixed(6); stack[key] = (stack[key] || 0) + 1; var yy = 60 - (stack[key] - 1) * 12; s += "<circle cx='" + X0(x) + "' cy='" + yy + "' r='5' class='dot' fill='" + (i === A.suspect && A.outlier ? "#B42318" : "#1F4FB8") + "'><title>" + x + "</title></circle>"; });
      s += "<text class='direct-label strong' x='" + (X0(A.mean) + 4) + "' y='20'>x̄ = " + num(A.mean, 4) + "</text><text class='tick muted' x='30' y='145'>light band: x̄ ± s; darker bar: 95% confidence interval</text>";
      ui.view.innerHTML = U.svgWrap(W, Hh, "Dot plot of " + A.n + " values with mean, standard deviation band, and confidence interval.", s);
      var gr = A.Zref === null ? "Grubbs' reference Z isn't listed in Table 1.7 for n = " + A.n + " (the table covers 3–12)." :
        "Grubbs' test on the most distant " + farthest(xs, A) + ": Z = " + fix(A.Z, 2) + (A.outlier ? " > " : " ≤ ") + A.Zref + " → " + (A.outlier ? "<strong>an outlier</strong> at 95%." : "not an outlier at 95%.");
      ui.readout.innerHTML = "n = " + A.n + ": x̄ = <strong>" + num(A.mean, 4) + "</strong>, s = <strong>" + num(A.s, 2) + "</strong>, 95% confidence interval μ = x̄ ± " + num(A.half, 2) + " (t = " + fix(A.t, 3) + (A.tFromTable ? ", Table 1.5" : ", computed") + "). " + gr;
      U.kvSet(ui.kv, [["n", String(A.n)], ["mean x̄", num(A.mean, 5)], ["s", num(A.s, 3)], ["t (95%)", fix(A.t, 3)], ["ts/√n", num(A.half, 3)], ["Z (farthest value)", fix(A.Z, 3)]]);
      var m = A.mean;
      ui.table.innerHTML = U.tableHTML(["x<sub>i</sub>", "x<sub>i</sub> − x̄", "(x<sub>i</sub> − x̄)<sup>2</sup>"], xs.map(function (x) { return [x, fix(x - m, 4), fix((x - m) * (x - m), 6)]; }));
    }
    draw();
  };

  /* ================================================================ t2-2 nuclide builder */
  mount.nuclide = function (host, D) {
    var st = { Z: 6, N: 6, e: 6 };
    var ui = U.shell(host, { title: "Explorer: build a nuclide",
      intro: "Change protons, neutrons, and electrons one at a time. Which number changes the element? Which makes an isotope? Which makes an ion?",
      source: "Source: textbook §2.2 (TB PDF p.87–88, printed 53–54), textbook preview; isotopes and the particle table: Day 2 p.22–23 (RAMP UP, covered in lecture)." });
    var sZ = U.slider(ui.controls, { label: "Protons (Z)", testid: "nuc-Z", min: 1, max: 36, step: 1, value: st.Z, format: String, onInput: function (v) { st.Z = v; draw(); } });
    var sN = U.slider(ui.controls, { label: "Neutrons", testid: "nuc-N", min: 0, max: 50, step: 1, value: st.N, format: String, onInput: function (v) { st.N = v; draw(); } });
    var sE = U.slider(ui.controls, { label: "Electrons", testid: "nuc-e", min: 0, max: 40, step: 1, value: st.e, format: String, onInput: function (v) { st.e = v; draw(); } });
    U.presetButtons(ui, "nuc", [["carbon-12", [6, 6, 6]], ["carbon-13", [6, 7, 6]], ["oxide ion ¹⁶O²⁻", [8, 8, 10]], ["⁵⁶Fe³⁺", [26, 30, 23]], ["³⁷Cl⁻", [17, 20, 18]]],
      function (p) { st.Z = p[0]; st.N = p[1]; st.e = p[2]; sZ.set(p[0]); sN.set(p[1]); sE.set(p[2]); draw(); });
    function draw() {
      var e = D.elements[st.Z - 1], sym = e[0], name = e[1], A = st.Z + st.N, Q = st.Z - st.e;
      var total = A, s = "", cx = 150, cy = 120, rr = 6;
      var kinds = [], pLeft = st.Z, nLeft = st.N;
      while (pLeft > 0 || nLeft > 0) { if (pLeft > 0) { kinds.push("p"); pLeft--; } if (nLeft > 0) { kinds.push("n"); nLeft--; } }
      kinds.forEach(function (k, i) {
        var ang = i * 2.39996, rad = rr * 1.05 * Math.sqrt(i);
        s += "<circle cx='" + (cx + rad * Math.cos(ang)).toFixed(1) + "' cy='" + (cy + rad * Math.sin(ang)).toFixed(1) + "' r='" + rr + "' fill='" + (k === "p" ? "#E3524A" : "#AEB5C0") + "' stroke='#FFF' stroke-width='1'/>";
      });
      var er = Math.max(60, rr * 1.05 * Math.sqrt(total) + 30);
      s += "<circle cx='" + cx + "' cy='" + cy + "' r='" + er + "' class='orbit'/>";
      for (var k = 0; k < st.e; k++) { var a2 = k / Math.max(1, st.e) * 2 * Math.PI; s += "<circle cx='" + (cx + er * Math.cos(a2)).toFixed(1) + "' cy='" + (cy + er * Math.sin(a2)).toFixed(1) + "' r='3.5' class='electron'/>"; }
      s += "<text class='tick' x='330' y='70'>red: protons (" + st.Z + ")</text><text class='tick' x='330' y='88'>grey: neutrons (" + st.N + ")</text><text class='tick' x='330' y='106'>blue dots: electrons (" + st.e + ")</text><text class='tick muted' x='330' y='130'>schematic; not to scale</text>";
      ui.view.innerHTML = "<p class='nuc-big'>" + supsub(A, st.Z, sym, Q) + "</p>" + U.svgWrap(600, 250, "Nucleus with " + st.Z + " protons and " + st.N + " neutrons; " + st.e + " electrons.", s);
      var kind = Q === 0 ? "a neutral atom" : Q > 0 ? "a cation (" + Math.abs(Q) + " fewer electrons than protons)" : "an anion (" + Math.abs(Q) + " more electrons than protons)";
      ui.readout.innerHTML = "Z = " + st.Z + " makes this <strong>" + name + "</strong>; A = " + st.Z + " + " + st.N + " = " + A + " (" + name + "-" + A + "); charge Q = " + st.Z + " − " + st.e + " = " + String(Q).replace("-", MINUS) + ", so it's " + kind + ".";
      U.kvSet(ui.kv, [["Element", name + " (" + sym + ")"], ["Mass number A", String(A)], ["Charge", Q === 0 ? "0" : (Math.abs(Q) === 1 ? "" : Math.abs(Q)) + (Q > 0 ? "+" : MINUS)]]);
      ui.table.innerHTML = U.tableHTML(["Change", "What it does"], [["protons", "changes the element (Z)"], ["neutrons", "makes a different isotope (A changes, Z doesn't)"], ["electrons", "makes an ion (charge changes; the nucleus doesn't)"]]);
    }
    draw();
  };

  /* ================================================================ t2-3 periodic table navigator */
  mount.ptable = function (host, D) {
    var PT = D.periodicTable, st = { hl: "none", sel: 17 };
    var GROUPS = { alkali: function (e) { return e.group === 1 && e.z !== 1; }, alkaline: function (e) { return e.group === 2; }, chalcogen: function (e) { return e.group === 16; }, halogen: function (e) { return e.group === 17; }, noble: function (e) { return e.group === 18; },
      main: function (e) { return e.group && (e.group <= 2 || e.group >= 13); }, transition: function (e) { return e.group >= 3 && e.group <= 12; }, lanth: function (e) { return e.f === "lanthanide"; }, act: function (e) { return e.f === "actinide"; },
      metal: function (e) { return e.cat === "metal"; }, nonmetal: function (e) { return e.cat === "nonmetal"; }, metalloid: function (e) { return e.cat === "metalloid"; } };
    var ui = U.shell(host, { title: "Explorer: navigate the periodic table",
      intro: "Highlight a category or a named group, then select an element for its details. Colors: tan metals, blue nonmetals, green metalloids (textbook Fig. 2.9b).",
      source: "Source: textbook §2.3, Figs. 2.9b, 2.11, 2.12 (TB PDF p.91–93, printed 57–59), textbook preview; layout basics on Day 2 p.24 (RAMP UP). Element names: background." });
    U.select(ui.controls, { label: "Highlight", testid: "pt-highlight", value: "none", options: [["none", "no highlight"], ["metal", "metals"], ["nonmetal", "nonmetals"], ["metalloid", "metalloids"], ["main", "main-group elements (1, 2, 13–18)"], ["transition", "transition metals (3–12)"], ["alkali", "alkali metals"], ["alkaline", "alkaline earth metals"], ["chalcogen", "chalcogens"], ["halogen", "halogens"], ["noble", "noble gases"], ["lanth", "lanthanides"], ["act", "actinides"]],
      onChange: function (v) { st.hl = v; draw(); } });
    function cellFor(e) {
      var row = e.f === "lanthanide" ? 9 : e.f === "actinide" ? 10 : e.period, col = e.f ? (e.z - (e.f === "lanthanide" ? 58 : 90) + 4) : e.group;
      return { row: row, col: col };
    }
    function draw() {
      var html = "<div class='pt-grid' role='grid' aria-label='Periodic table'>", cells = {};
      PT.forEach(function (e) { var c = cellFor(e); cells[c.row + "-" + c.col] = e; });
      for (var r = 1; r <= 10; r++) {
        if (r === 8) { html += "<div class='pt-gap' style='grid-column: span 18; height: 8px'></div>"; continue; }
        for (var c2 = 1; c2 <= 18; c2++) {
          var e = cells[r + "-" + c2];
          if (!e) { html += "<div class='pt-gap' aria-hidden='true'></div>"; continue; }
          var dim = st.hl !== "none" && !GROUPS[st.hl](e);
          html += "<button type='button' class='pt-cell " + e.cat + (dim ? " dim" : "") + (e.z === st.sel ? " sel" : "") + "' data-z='" + e.z + "' data-testid='pt-" + e.sym + "' aria-label='" + e.name + ", " + e.z + "'><span class='pt-z'>" + e.z + "</span><span class='pt-s'>" + e.sym + "</span></button>";
        }
      }
      html += "</div><div class='pt-legend'><span style='--c:#FBEBC8'>metal</span><span style='--c:#CFE0F5'>nonmetal</span><span style='--c:#CDEBD9'>metalloid</span></div>";
      ui.view.innerHTML = html;
      Array.prototype.forEach.call(ui.view.querySelectorAll(".pt-cell"), function (b) { b.addEventListener("click", function () { st.sel = +b.getAttribute("data-z"); draw(); var again = ui.view.querySelector(".pt-cell[data-z='" + st.sel + "']"); if (again) again.focus(); }); });
      var e2 = PT[st.sel - 1];
      var gname = e2.group === 1 && e2.z !== 1 ? "alkali metal" : e2.group === 2 ? "alkaline earth metal" : e2.group === 16 ? "chalcogen" : e2.group === 17 ? "halogen" : e2.group === 18 ? "noble gas" : e2.f ? e2.f : (e2.group >= 3 && e2.group <= 12) ? "transition metal" : "";
      var ions = e2.ions.length ? e2.ions.map(function (q) { return U.ion(e2.sym, q === "+" ? 1 : q === "-" ? -1 : (q.slice(-1) === "+" ? 1 : -1) * parseInt(q, 10)); }).join(", ") : "none listed in Fig. 2.11";
      ui.readout.innerHTML = "<strong>" + e2.name + "</strong> (" + e2.sym + ", Z = " + e2.z + "): " + (e2.group ? "group " + e2.group + ", " : "") + "period " + e2.period + "; " + e2.cat + (gname ? "; " + gname : "") + ". Common ion(s): " + ions + ".";
      U.kvSet(ui.kv, [["Group", e2.group ? String(e2.group) : "f block"], ["Period", String(e2.period)], ["Category", e2.cat], ["Main group?", e2.group && (e2.group <= 2 || e2.group >= 13) ? "yes" : "no"]]);
      ui.table.innerHTML = U.tableHTML(["Group", "Name", "Common ion charge (Table 2.2)"], [["1", "alkali metals (not H)", "1+"], ["2", "alkaline earth metals", "2+"], ["13", "", "3+"], ["15", "", "3−"], ["16", "chalcogens", "2−"], ["17", "halogens", "1−"], ["18", "noble gases", "none"]]);
    }
    draw();
  };

  /* ================================================================ t2-4 isotope mixer */
  mount.isotopes = function (host, D) {
    var ISO = D.isotopes, st = { el: "Cl", ab: null };
    var ui = U.shell(host, { title: "Explorer: weighted average atomic mass",
      intro: "Drag the abundances. The average slides toward the more abundant isotope and can never leave the range of the isotope masses.",
      source: "Source: textbook §2.4, Eq. 2.3 (TB PDF p.94–95, printed 60–61), textbook preview. Neon's values are the textbook's Table 2.3; the other isotope data are standard reference values (background)." });
    var sE = U.select(ui.controls, { label: "Element", testid: "iso-element", value: st.el, options: Object.keys(ISO).map(function (k) { return [k, k + " (" + ISO[k].length + " isotopes)"]; }), onChange: function (v) { st.el = v; st.ab = null; build(); draw(); } });
    var sliders = el("div", { class: "xp-controls" }); ui.controls.appendChild(sliders);
    var row = el("div", { class: "ctl-row" }); ui.controls.appendChild(row);
    U.button(row, "Natural abundances", "btn-iso-natural", function () { st.ab = null; build(); draw(); });
    function build() {
      sliders.innerHTML = "";
      var I = ISO[st.el];
      if (!st.ab) st.ab = I.map(function (r) { return r[2] * 100; });
      var handles = [];
      I.slice(0, I.length - 1).forEach(function (r, i) {
        handles[i] = U.slider(sliders, { label: "<sup>" + r[0] + "</sup>" + st.el + " abundance", testid: "iso-" + i, min: 0, max: 100, step: 0.1, value: st.ab[i], format: function (v) { return v.toFixed(1) + "%"; },
          onInput: function (v) {
            st.ab[i] = v; var rest = 100 - st.ab.slice(0, I.length - 1).reduce(function (s2, x) { return s2 + x; }, 0);
            if (rest < 0) { st.ab[i] += rest; rest = 0; handles[i].set(st.ab[i]); }
            st.ab[I.length - 1] = rest; draw();
          } });
      });
    }
    function draw() {
      var I = ISO[st.el], fr = st.ab.map(function (a) { return a / 100; }), avg = I.reduce(function (s, r, i) { return s + r[1] * fr[i]; }, 0);
      var m0 = I[0][1] - 0.6, m1 = I[I.length - 1][1] + 0.6, W = 600, Hh = 190, X0 = function (m) { return 40 + (m - m0) / (m1 - m0) * (W - 80); };
      var s = "<line class='baseline' x1='40' x2='" + (W - 40) + "' y1='150' y2='150'/>";
      I.forEach(function (r, i) {
        var hgt = fr[i] * 110, x = X0(r[1]);
        s += "<rect x='" + (x - 10) + "' y='" + (150 - hgt) + "' width='20' height='" + hgt + "' rx='3' fill='" + SERIES[i % SERIES.length] + "'/>" +
          "<text class='tick' x='" + x + "' y='168' text-anchor='middle'>" + r[0] + st.el + " " + fix(r[1], 4) + "</text><text class='val' x='" + x + "' y='" + (144 - hgt) + "' text-anchor='middle'>" + st.ab[i].toFixed(2) + "%</text>";
      });
      s += "<line class='marker' x1='" + X0(avg) + "' x2='" + X0(avg) + "' y1='20' y2='150'/><path class='marker-head' d='M" + (X0(avg) - 6) + " 18 h12 l-6 8 z'/><text class='direct-label strong' x='" + (X0(avg) + 6) + "' y='30'>average " + fix(avg, 3) + " amu</text>";
      ui.view.innerHTML = U.svgWrap(W, Hh, "Isotope abundances of " + st.el + " and their weighted average " + avg.toFixed(3) + " amu.", s);
      ui.readout.innerHTML = "m<sub>" + st.el + "</sub> = " + I.map(function (r, i) { return fix(fr[i], 4) + " × " + fix(r[1], 4); }).join(" + ") + " = <strong>" + fix(avg, 3) + " amu</strong>.";
      U.kvSet(ui.kv, [["Weighted average", fix(avg, 4) + " amu"], ["Simple average (wrong)", fix(I.reduce(function (s, r) { return s + r[1]; }, 0) / I.length, 4) + " amu"]]);
      ui.table.innerHTML = U.tableHTML(["Isotope", "Mass (amu)", "Abundance", "Contribution (amu)"], I.map(function (r, i) { return ["<sup>" + r[0] + "</sup>" + st.el, fix(r[1], 4), st.ab[i].toFixed(3) + "%", fix(r[1] * fr[i], 4)]; }));
    }
    build(); draw();
  };

  /* ================================================================ t2-5 mole map */
  mount.moles = function (host, D) {
    var SUBS = ["H2O", "CO2", "NaCl", "NH3", "CH4", "C6H12O6", "Au", "Fe", "Al"], AM = D.atomicMass, NA = D.constants.NA.value;
    var st = { f: "H2O", given: "mass", v: "10.0" };
    var ui = U.shell(host, { title: "Explorer: grams ↔ moles ↔ particles",
      intro: "Choose a substance and which quantity you know. The map fills in the other two, with every conversion factor written out.",
      source: "Source: textbook §2.5, Figs. 2.14 and 2.18 (TB PDF p.98–101, printed 64–67), textbook preview. Molar masses from the atomic masses in data.js (textbook values where printed)." });
    U.select(ui.controls, { label: "Substance", testid: "mol-sub", value: st.f, options: SUBS.map(function (f) { return [f, U.formulaText(f)]; }), onChange: function (v) { st.f = v; draw(); } });
    U.radios(ui.controls, { label: "I know the…", testid: "mol-given", value: st.given, options: [["mass", "mass (g)"], ["moles", "amount (mol)"], ["particles", "number of particles"]], onChange: function (v) { st.given = v; draw(); } });
    var inV = el("div", { class: "ctl ctl-num" }, "<label for='mol-v'>Value</label><input id='mol-v' type='text' inputmode='decimal' data-testid='input-mol-value' value='" + st.v + "'>");
    ui.controls.appendChild(inV);
    inV.querySelector("input").addEventListener("input", function (e) { st.v = e.target.value; draw(); });
    function fHTML(f) { var c = P.formulaCounts(f); return U.formulaHTML(Object.keys(c).map(function (k) { return [k, c[k]]; })); }
    function draw() {
      var I = P.sigInfo(st.v.replace(/×\s*10\^?/, "e")); var mm = P.molarMass(st.f, AM);
      if (!I) { ui.readout.innerHTML = "Enter a number (e.g., 10.0 or 3.34e23)."; return; }
      var sf = Math.min(I.sf, 4), g, n, N;
      if (st.given === "mass") { g = I.value; n = g / mm; N = n * NA; }
      else if (st.given === "moles") { n = I.value; g = n * mm; N = n * NA; }
      else { N = I.value; n = N / NA; g = n * mm; }
      var unit = /^[A-Z][a-z]?$/.test(st.f) ? "atoms" : st.f === "NaCl" ? "formula units" : "molecules";
      var boxes = "<div class='chain'><span><strong>" + P.formatSig(g, sf) + " g</strong></span><span aria-hidden='true'>⇄</span><span class='frac'><span class='num'>÷ " + fix(mm, 3) + " g/mol</span><span class='den'>× " + fix(mm, 3) + " g/mol</span></span><span aria-hidden='true'>⇄</span><span><strong>" + P.formatSig(n, sf) + " mol</strong></span><span aria-hidden='true'>⇄</span><span class='frac'><span class='num'>× N<sub>A</sub></span><span class='den'>÷ N<sub>A</sub></span></span><span aria-hidden='true'>⇄</span><span><strong>" + P.formatSig(N, sf) + "</strong> " + unit + "</span></div>";
      ui.view.innerHTML = boxes + "<p class='xp-caption'>Molar mass of " + fHTML(st.f) + " = " + Object.keys(P.formulaCounts(st.f)).map(function (k) { var c = P.formulaCounts(st.f)[k]; return (c > 1 ? c + "(" : "") + fix(AM[k], k === "H" ? 4 : 3) + (c > 1 ? ")" : ""); }).join(" + ") + " = " + fix(mm, 3) + " g/mol. N<sub>A</sub> = 6.022 × 10<sup>23</sup> mol<sup>−1</sup>.</p>";
      ui.readout.innerHTML = P.formatSig(g, sf) + " g of " + fHTML(st.f) + " = " + P.formatSig(n, sf) + " mol = " + P.formatSig(N, sf) + " " + unit + ". Every route between grams and particles passes through moles.";
      U.kvSet(ui.kv, [["Molar mass", fix(mm, 3) + " g/mol"], ["Mass of one particle", sci(mm / NA, 4) + " g"]]);
      ui.table.innerHTML = U.tableHTML(["Substance", "Molar mass (g/mol)", "Mass of 1 mol"], SUBS.map(function (f) { var x = P.molarMass(f, AM); return [fHTML(f), fix(x, 3), fix(x, 3) + " g"]; }));
    }
    draw();
  };

  /* ================================================================ t2-6 mass spectrum (isotope patterns) */
  mount.massSpec = function (host, D) {
    var MOLS = { "HCl": { H: 1, Cl: 1 }, "Cl2": { Cl: 2 }, "HBr": { H: 1, Br: 1 }, "Br2": { Br: 2 }, "CH3Cl": { C: 1, H: 3, Cl: 1 }, "CO2": { C: 1, O: 2 } };
    var st = { m: "Cl2" };
    var ui = U.shell(host, { title: "Explorer: the molecular-ion region of a mass spectrum",
      intro: "Choose a molecule. Peaks are computed from chlorine and bromine isotope abundances (background values); other atoms are treated as single isotopes. Fragment peaks are not modeled.",
      source: "Source: textbook §2.6 (TB PDF p.104–106, printed 70–72), textbook preview; isotope abundances: background." });
    U.select(ui.controls, { label: "Molecule", testid: "ms-mol", value: st.m, options: Object.keys(MOLS).map(function (k) { return [k, k.replace(/(\d)/g, "₍$1₎").replace(/₍(\d)₎/g, function (_, d) { return "₀₁₂₃₄₅₆₇₈₉"[+d]; })]; }), onChange: function (v) { st.m = v; draw(); } });
    function draw() {
      var peaks = P.isotopePattern(MOLS[st.m], D.isotopes), ms = peaks.map(function (p) { return p.m; });
      var lo = Math.min.apply(null, ms) - 3, hi = Math.max.apply(null, ms) + 3;
      var f = U.frame({ w: 600, h: 260, x0: lo, x1: hi, y0: 0, y1: 110, yticks: [[0, "0"], [50, "50"], [100, "100"]], xticks: (function () { var t = []; for (var x = Math.ceil(lo); x <= hi; x++) if (x % 2 === 0) t.push([x, String(x)]); return t; })(), xlabel: "m/z (u)", ylabel: "relative intensity" });
      var g = f.axes;
      peaks.forEach(function (p) { var x = f.xs(p.m), y = f.ys(p.rel); g += "<rect x='" + (x - 3) + "' y='" + y + "' width='6' height='" + (f.ys(0) - y) + "' fill='" + SERIES[0] + "'><title>m/z " + p.m + ": " + p.rel.toFixed(1) + "</title></rect><text class='direct-label' x='" + x + "' y='" + (y - 5) + "' text-anchor='middle'>" + p.m + "</text>"; });
      ui.view.innerHTML = U.svgWrap(600, 260, "Computed molecular-ion peaks for " + st.m, g);
      ui.readout.innerHTML = "Molecular-ion peaks: " + peaks.map(function (p) { return "m/z " + p.m + " (" + p.rel.toFixed(0) + ")"; }).join(", ") + ". " + (peaks.length === 1 ? "One peak: no Cl or Br isotopes to split it (¹³C etc. neglected)." : "Each peak is a different isotope combination; the heights follow the isotope abundances.");
      U.kvSet(ui.kv, [["Peaks", String(peaks.length)], ["Tallest", "m/z " + peaks.reduce(function (a, b) { return b.rel > a.rel ? b : a; }).m]]);
      ui.table.innerHTML = U.tableHTML(["m/z", "Relative intensity (tallest = 100)", "Probability"], peaks.map(function (p) { return [p.m, p.rel.toFixed(1), p.p.toFixed(4)]; }));
    }
    draw();
  };

  /* ================================================================ t3-5 Heisenberg */
  mount.heisenberg = function (host, D) {
    var PART = { electron: [9.109e-31, "electron"], proton: [1.673e-27, "proton"], alpha: [6.645e-27, "α particle"], baseball: [0.142, "baseball (142 g)"], dust: [1e-12, "dust grain (1 ng)"] };
    var st = { p: "electron", logdx: Math.log10(5.3e-11) };
    var ui = U.shell(host, { title: "Explorer: the uncertainty trade-off",
      intro: "Choose a particle and how precisely you know where it is. The minimum speed uncertainty comes from Δx · mΔu ≥ h/(4π).",
      source: "Source: textbook §3.5, Eq. 3.14 (TB PDF p.137, printed 103), textbook preview." });
    var sP = U.select(ui.controls, { label: "Particle", testid: "hz-particle", value: st.p, options: Object.keys(PART).map(function (k) { return [k, PART[k][1]]; }), onChange: function (v) { st.p = v; draw(); } });
    var sl = U.slider(ui.controls, { label: "Position uncertainty Δx", testid: "hz-dx", min: -16, max: -2, step: 0.05, value: st.logdx, format: function (v) { return sci(Math.pow(10, v)) + " m"; }, onInput: function (v) { st.logdx = v; draw(); } });
    U.presetButtons(ui, "hz", [["electron in an atom (53 pm)", ["electron", 5.3e-11]], ["proton in a nucleus (1 fm)", ["proton", 1e-15]], ["baseball to 680 nm", ["baseball", 6.8e-7]]], function (p) { st.p = p[0]; st.logdx = Math.log10(p[1]); sP.value = p[0]; sl.set(st.logdx); draw(); });
    function draw() {
      var m = PART[st.p][0], dx = Math.pow(10, st.logdx), du = P.heisenbergDu(m, dx);
      var x = function (v) { return 30 + (Math.log10(v) + 32) / 42 * 540; };
      var s = "<line class='baseline' x1='30' x2='570' y1='60' y2='60'/>";
      for (var k = -32; k <= 10; k += 6) s += "<line class='tickmark' x1='" + x(Math.pow(10, k)) + "' x2='" + x(Math.pow(10, k)) + "' y1='60' y2='66'/><text class='tick' x='" + x(Math.pow(10, k)) + "' y='80' text-anchor='middle'>10<tspan class='sup' dy='-5'>" + (k < 0 ? MINUS + (-k) : k) + "</tspan></text>";
      [[343, "speed of sound"], [2.998e8, "speed of light"], [1e-9, "1 nm per second"]].forEach(function (mk, i) { s += "<line class='landmark' x1='" + x(mk[0]) + "' x2='" + x(mk[0]) + "' y1='40' y2='60'/><text class='tick muted' x='" + x(mk[0]) + "' y='" + (34 - 12 * (i % 2)) + "' text-anchor='middle'>" + mk[1] + "</text>"; });
      var lx = Math.max(30, Math.min(570, x(du)));
      s += "<path class='marker-head' d='M" + (lx - 7) + " 100 h14 l-7 -10 z'/><text class='tick strong' x='" + Math.min(500, Math.max(80, lx)) + "' y='118' text-anchor='middle'>Δu ≥ " + U.sciSVG(du, 2, "m/s") + "</text><text class='tick muted' x='30' y='136'>speed, m/s (log scale)</text>";
      ui.view.innerHTML = U.svgWrap(600, 140, "Minimum speed uncertainty " + du.toExponential(2) + " meters per second", s);
      var verdict = du > 3e8 ? "larger than the speed of light, so the particle can't be confined that tightly" : du > 1e5 ? "enormous: a definite path is meaningless" : du > 1 ? "significant on an everyday scale" : "far too small ever to notice";
      ui.readout.innerHTML = "Δu ≥ h/(4π m Δx) = 6.626 × 10<sup>−34</sup> ÷ (4π × " + sci(m, 4) + " kg × " + sci(dx) + " m) = <strong>" + sci(du, 2) + " m/s</strong>: " + verdict + ".";
      U.kvSet(ui.kv, [["m", sci(m, 4) + " kg"], ["Δx", sci(dx) + " m"], ["minimum Δu", sci(du, 2) + " m/s"], ["Δu ÷ c", sci(du / 2.998e8, 2)]]);
      ui.table.innerHTML = U.tableHTML(["Case", "Δx (m)", "minimum Δu (m/s)"], [["electron, 53 pm", sci(5.3e-11), sci(P.heisenbergDu(9.109e-31, 5.3e-11), 2)], ["proton, 1 fm", sci(1e-15), sci(P.heisenbergDu(1.673e-27, 1e-15), 2)], ["baseball, 680 nm", sci(6.8e-7), sci(P.heisenbergDu(0.142, 6.8e-7), 2)]]);
    }
    draw();
  };

  /* ================================================================ t3-11 photoelectron spectra */
  mount.pes = function (host, D) {
    var PES = D.pes, TB = D.pesTextbook, syms = Object.keys(PES), st = { el: "Al" };
    var ui = U.shell(host, { title: "Explorer: photoelectron spectra",
      intro: "Choose an element and predict the peaks first. Binding energy decreases from left to right, as in the textbook, on a log scale so core and valence peaks fit on one axis.",
      source: "Source: textbook §3.11 (TB PDF p.162–163, printed 128–129), textbook preview. Li and Al are the textbook's values; the others are approximate reference values (background)." });
    U.select(ui.controls, { label: "Element", testid: "pes-element", value: st.el, options: syms.map(function (s) { return [s, s + (TB.indexOf(s) >= 0 ? " (textbook values)" : "")]; }), onChange: function (v) { st.el = v; draw(); } });
    function draw() {
      var rows = PES[st.el], f = U.frame({ w: 600, h: 260, x0: 0, x1: 1, y0: 0, y1: 7, yticks: [[0, "0"], [2, "2"], [4, "4"], [6, "6"]], xticks: [], xlabel: "binding energy (MJ/mol, log scale, decreasing →)", ylabel: "relative number of electrons" });
      var xpos = function (be) { return f.m.l + (Math.log10(500) - Math.log10(be)) / (Math.log10(500) - Math.log10(0.3)) * f.pw; };
      var g = f.axes;
      [500, 100, 10, 1, 0.3].forEach(function (t) { g += "<line class='tickmark' x1='" + xpos(t) + "' x2='" + xpos(t) + "' y1='" + (f.m.t + f.ph) + "' y2='" + (f.m.t + f.ph + 4) + "'/><text class='tick' x='" + xpos(t) + "' y='" + (f.m.t + f.ph + 17) + "' text-anchor='middle'>" + t + "</text>"; });
      rows.forEach(function (r) { var x = xpos(r[1]), y = f.ys(r[2]); g += "<rect x='" + (x - 4) + "' y='" + y + "' width='8' height='" + (f.ys(0) - y) + "' rx='2' fill='" + SERIES[0] + "'><title>" + r[0] + ": " + r[1] + " MJ/mol, " + r[2] + " e⁻</title></rect><text class='direct-label strong' x='" + x + "' y='" + (y - 18) + "' text-anchor='middle'>" + r[0] + "</text><text class='direct-label' x='" + x + "' y='" + (y - 5) + "' text-anchor='middle'>" + r[1] + "</text>"; });
      ui.view.innerHTML = U.svgWrap(600, 260, "Photoelectron spectrum of " + st.el, g);
      var cfg = rows.map(function (r) { return r[0] + "<sup>" + r[2] + "</sup>"; }).join("");
      var ie = D.ie1[st.el];
      ui.readout.innerHTML = st.el + ": " + rows.length + " peaks → " + cfg + " (" + rows.reduce(function (s, r) { return s + r[2]; }, 0) + " electrons). Smallest binding energy " + rows[rows.length - 1][1] + " MJ/mol = " + Math.round(rows[rows.length - 1][1] * 1000) + " kJ/mol" + (ie ? ", compared with IE₁ = " + ie + " kJ/mol on Day 7 p.9." : ".");
      U.kvSet(ui.kv, [["Peaks", String(rows.length)], ["Electrons", String(rows.reduce(function (s, r) { return s + r[2]; }, 0))], ["Data source", TB.indexOf(st.el) >= 0 ? "textbook" : "reference (background)"]]);
      ui.table.innerHTML = U.tableHTML(["Subshell", "Binding energy (MJ/mol)", "Electrons (peak height)"], rows.map(function (r) { return [r[0], r[1], r[2]]; }));
    }
    draw();
  };

  /* ================================================================ t4-2 bond polarity */
  mount.polarity = function (host, D) {
    var EN = D.electronegativity, syms = Object.keys(EN), st = { a: "H", b: "Cl" };
    var chi = function (sym) { return EN[sym].toFixed(1); };   // Fig. 4.5 prints one decimal (Cl 3.0)
    var ui = U.shell(host, { title: "Explorer: electronegativity and bond polarity",
      intro: "Pick two elements. Δχ decides the bond type by the textbook's guidelines, and the more electronegative atom gets δ−.",
      source: "Source: textbook §4.2, Fig. 4.5 values and the 0.4 / 2.0 guidelines (TB PDF p.186–187, printed 152–153), textbook preview." });
    var sA = U.select(ui.controls, { label: "First atom", testid: "pol-a", value: st.a, options: syms.map(function (s) { return [s, s + " (χ = " + chi(s) + ")"]; }), onChange: function (v) { st.a = v; draw(); } });
    var sB = U.select(ui.controls, { label: "Second atom", testid: "pol-b", value: st.b, options: syms.map(function (s) { return [s, s + " (χ = " + chi(s) + ")"]; }), onChange: function (v) { st.b = v; draw(); } });
    U.presetButtons(ui, "pol", [["H–F", ["H", "F"]], ["C–H", ["C", "H"]], ["Na–Cl", ["Na", "Cl"]], ["Cl–Cl", ["Cl", "Cl"]], ["C–O", ["C", "O"]]], function (p) { st.a = p[0]; st.b = p[1]; sA.value = p[0]; sB.value = p[1]; draw(); });
    function draw() {
      var xa = EN[st.a], xb = EN[st.b], d = Math.round(Math.abs(xa - xb) * 100) / 100, cls = P.bondClass(d), W = 600, Hh = 200;
      var X0 = function (v) { return 40 + v / 3.4 * (W - 80); };
      var s = "<rect x='" + X0(0) + "' y='30' width='" + (X0(0.4) - X0(0)) + "' height='22' fill='#E6F4F2'/><rect x='" + X0(0.4) + "' y='30' width='" + (X0(2.0) - X0(0.4)) + "' height='22' fill='#CDE2FB'/><rect x='" + X0(2.0) + "' y='30' width='" + (X0(3.4) - X0(2.0)) + "' height='22' fill='#F7DAD7'/>" +
        "<text class='tick' x='" + X0(0.2) + "' y='45' text-anchor='middle'>nonpolar</text><text class='tick' x='" + X0(1.2) + "' y='45' text-anchor='middle'>polar covalent</text><text class='tick' x='" + X0(2.7) + "' y='45' text-anchor='middle'>ionic</text>";
      [0, 0.4, 1, 2, 3].forEach(function (t) { s += "<text class='tick' x='" + X0(t) + "' y='70' text-anchor='middle'>" + t + "</text>"; });
      s += "<path class='marker-head' d='M" + (X0(d) - 7) + " 24 h14 l-7 8 z'/><text class='tick strong' x='" + X0(d) + "' y='18' text-anchor='middle'>Δχ = " + d.toFixed(1) + "</text>";
      var left = xa <= xb ? st.a : st.b, right = xa <= xb ? st.b : st.a, polar = d > 0.4;
      s += "<circle cx='230' cy='140' r='26' fill='#DCE7F7' stroke='#1F4FB8'/><circle cx='370' cy='140' r='30' fill='" + (polar ? "#F7DAD7" : "#DCE7F7") + "' stroke='" + (polar ? "#B42318" : "#1F4FB8") + "'/><line x1='256' x2='340' y1='140' y2='140' stroke='#475467' stroke-width='3'/>" +
        "<text class='tick strong' x='230' y='145' text-anchor='middle' style='font-size:15px'>" + left + "</text><text class='tick strong' x='370' y='145' text-anchor='middle' style='font-size:15px'>" + right + "</text>";
      if (cls === "ionic") s += "<text class='tick strong' x='230' y='104' text-anchor='middle'>+</text><text class='tick strong' x='370' y='100' text-anchor='middle'>−</text>";
      else if (polar) s += "<text class='tick strong' x='230' y='104' text-anchor='middle'>δ+</text><text class='tick strong' x='370' y='100' text-anchor='middle'>δ−</text><line x1='250' x2='350' y1='186' y2='186' stroke='#17212E' stroke-width='1.5'/><path d='M350 186 l-8 -5 v10 z' fill='#17212E'/><line x1='258' x2='258' y1='181' y2='191' stroke='#17212E' stroke-width='1.5'/>";
      ui.view.innerHTML = U.svgWrap(W, Hh, st.a + "–" + st.b + " bond: delta chi " + d.toFixed(1) + ", " + cls, s);
      ui.readout.innerHTML = st.a + " (χ = " + chi(st.a) + ") and " + st.b + " (χ = " + chi(st.b) + "): Δχ = " + d.toFixed(1) + " → <strong>" + cls + "</strong>" + (polar && cls !== "ionic" ? "; " + right + " is δ− and " + left + " is δ+ (the arrow points toward " + right + ")." : cls === "ionic" ? "; electrons transfer to " + right + ", making ions." : "; the pair is shared (nearly) equally.") + " The cutoffs are “more like guidelines than strict limits.”";
      U.kvSet(ui.kv, [["χ(" + st.a + ")", chi(st.a)], ["χ(" + st.b + ")", chi(st.b)], ["Δχ", d.toFixed(1)], ["Bond type", cls]]);
      var main = D.layout.map(function (row) { return row.map(function (sym) { return sym && EN[sym] !== undefined ? sym + " " + chi(sym) : ""; }); });
      ui.table.innerHTML = U.tableHTML(D.groupLabels.map(function (g) { return "Group " + g; }), main);
    }
    draw();
  };

  X.calcPreview = P;
  return { calc: P };
});

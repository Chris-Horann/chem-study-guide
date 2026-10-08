/* Chapter 18 explorer for the CurrentCourseGuide (§18.4–18.5 only; Day 12 p.14–25): building a band from the
   molecular orbitals of N sodium atoms, and the band pictures of conductors, semiconductors, and insulators, with
   heating and doping. Classic script loaded after explorers.js; adds to window.Explorers.mount.
   The cluster levels come from a simple chain model (verification/CurrentCourseGuide/ch18_data.py checks them against
   numpy eigenvalues; expected_values.json "bands"). In node, module.exports gives the pure calculations (tested by
   test_explorers_ch18.js). */
(function (root, factory) {
  if (typeof module === "object" && module.exports) module.exports = factory(require("./explorers.js"));
  else factory(root.Explorers);
})(typeof self !== "undefined" ? self : this, function (X) {
  "use strict";
  var U = X.ui, mount = X.mount;

  /* ================================================================ pure calculations */
  var C = {};
  // Chain model (background): N atomic orbitals of energy alpha, each coupled to its neighbours, give N MOs at
  // alpha − 2·beta·cos(kπ/(N + 1)), k = 1 … N, lowest first. Arbitrary energy units; Na2's two MOs sit at alpha ∓ beta.
  C.S = { alpha: 0, beta: 1 };          // MOs from the Na 3s orbitals
  C.P = { alpha: 3.6, beta: 1 };        // MOs from the empty 3p orbitals (each drawn line stands for three)
  C.levels = function (n, a, b) {
    var out = [];
    for (var k = 1; k <= n; k++) out.push(a - 2 * b * Math.cos(k * Math.PI / (n + 1)));
    return out;
  };
  // electrons fill the lowest MOs, at most two per MO (Day 12 p.8–9)
  C.fill = function (n, ePerAtom) {
    var e = n * ePerAtom, occ = [];
    for (var k = 0; k < n; k++) { var x = Math.max(0, Math.min(2, e)); occ.push(x); e -= x; }
    return occ;
  };
  C.cluster = function (n) {
    var s = C.levels(n, C.S.alpha, C.S.beta), p = C.levels(n, C.P.alpha, C.P.beta), occ = C.fill(n, 1);
    var filled = occ.filter(function (o) { return o > 0; }).length;
    var r = { n: n, s: s, p: p, occ: occ, mos: n, electrons: n, filled: filled, empty: n - filled,
      width: s[n - 1] - s[0], overlap: s[n - 1] > p[0] };
    r.widthRatio = r.width / (4 * C.S.beta);              // the band's limiting width is 4 beta
    if (n >= 2) { r.gap = s[filled] - s[filled - 1]; r.gapRatio = r.gap / (2 * C.S.beta); }   // Na2's gap = 2 beta
    return r;
  };
  // background model for crossing a gap: the fraction of electrons that cross is proportional to e^(−Eg/2RT)
  C.R = 8.314;
  C.crossFactor = function (egKJ, tC) { return Math.exp(-egKJ * 1000 / (2 * C.R * (tC + 273.15))); };
  // the professor's band sketch (Day 12 p.24): band edges in drawing units, fraction of the valence band filled
  C.MATERIALS = [
    { key: "diamond", label: "Insulator (diamond)", vb: [0, 2], cb: [3.9, 5.0], vbFill: 1, egKJ: 530, src: "Day 12 p.24" },
    { key: "zinc", label: "Conductor (zinc)", vb: [0, 2], cb: [2, 5.0], vbFill: 1, egKJ: 0, src: "Day 12 p.23–24" },
    { key: "sodium", label: "Conductor (sodium)", vb: [0, 2], cb: [2, 5.0], vbFill: 0.5, egKJ: 0, src: "Day 12 p.22, p.24" },
    { key: "silicon", label: "Semiconductor (silicon)", vb: [0, 2], cb: [2.9, 4.1], vbFill: 1, egKJ: 106, src: "Day 12 p.24–25" }
  ];
  // the conductor rule (Day 12 p.18): a partially filled valence band, or a filled one touching or overlapping an
  // empty band, conducts; otherwise the size of the gap decides
  C.classify = function (m) {
    if (m.vbFill < 1 || m.cb[0] <= m.vb[1]) return "conductor";
    return m.cb[0] - m.vb[1] < 1 ? "semiconductor" : "insulator";
  };

  /* ================================================================ the explorer (browser only) */
  var el = U && U.el;
  var OCC = "#7B5BAE", EMPTY = "#E2876F", PBAND = "#A3ABB6", FILL = "#5B9BD5", EDGE = "#3E6A97", INK = "#17212E";
  function sci(x) {
    var e = Math.floor(Math.log10(x)), m = x / Math.pow(10, e);
    if (m >= 9.95) { m = 1; e += 1; }
    return m.toFixed(1) + " × 10<sup>" + (e < 0 ? "−" + (-e) : e) + "</sup>";
  }
  function sub(n) { return String(n).split("").map(function (d) { return "₀₁₂₃₄₅₆₇₈₉"[+d]; }).join(""); }
  function arrow(x, cy, up) {
    var t = cy - 7, b = cy + 7, h = up ? t : b, k = up ? 4 : -4;
    return "<path d='M" + x + " " + (up ? b : t) + " V" + h + " M" + (x - 3) + " " + (h + k) + " L" + x + " " + h + " L" + (x + 3) + " " + (h + k) + "' style='fill:none;stroke:" + INK + ";stroke-width:1.5;stroke-linecap:round;stroke-linejoin:round'/>";
  }
  function line(x1, x2, y, color, w, dash) {
    return "<line x1='" + x1.toFixed(1) + "' y1='" + y.toFixed(1) + "' x2='" + x2.toFixed(1) + "' y2='" + y.toFixed(1) + "' style='stroke:" + color + ";stroke-width:" + w + (dash ? ";stroke-dasharray:4 3" : "") + "'/>";
  }
  function rect(x, y, w, h, fill, stroke, extra) {
    return "<rect x='" + x.toFixed(1) + "' y='" + y.toFixed(1) + "' width='" + w.toFixed(1) + "' height='" + Math.max(0, h).toFixed(1) + "' style='fill:" + fill + ";stroke:" + (stroke || "none") + ";stroke-width:1.2" + (extra || "") + "'/>";
  }
  function text(x, y, s, cls, anchor) {
    return "<text class='" + (cls || "tick") + "' x='" + x.toFixed(1) + "' y='" + y.toFixed(1) + "'" + (anchor ? " text-anchor='" + anchor + "'" : "") + ">" + s + "</text>";
  }
  function dblArrow(x, y1, y2, color) {
    var a = Math.min(y1, y2), b = Math.max(y1, y2);
    return "<path d='M" + x + " " + (a + 1) + " V" + (b - 1) + " M" + (x - 3.5) + " " + (a + 6) + " L" + x + " " + (a + 1) + " L" + (x + 3.5) + " " + (a + 6) +
      " M" + (x - 3.5) + " " + (b - 6) + " L" + x + " " + (b - 1) + " L" + (x + 3.5) + " " + (b - 6) + "' style='fill:none;stroke:" + color + ";stroke-width:1.6'/>";
  }
  function energyAxis(x, yTop, yBot) {
    return "<line x1='" + x + "' y1='" + yBot + "' x2='" + x + "' y2='" + (yTop + 6) + "' style='stroke:#6B7686;stroke-width:1.2'/><path d='M" + x + " " + yTop + " l-5 9 h10 z' style='fill:#6B7686'/>" +
      "<text class='axis-label' transform='translate(" + (x - 8) + " " + ((yTop + yBot) / 2) + ") rotate(-90)' text-anchor='middle'>energy</text>";
  }

  mount.bands = function (host, D) {
    var NS = [1, 2, 4, 8, 16, 32, 64, 0];                   // 0 = a real piece of sodium (about 10²³ atoms)
    var byKey = {}, seenN = {}, seenM = {};
    C.MATERIALS.forEach(function (m) { byKey[m.key] = m; });
    var st = { mode: "build", i: 0, mat: "silicon", heat: "room", dope: "none" };
    var ui = U.shell(host, { title: "Explorer: from molecular orbitals to bands",
      intro: "Build a band: add sodium atoms and watch the MOs from their 3s orbitals crowd together until the HOMO–LUMO gap disappears. Compare solids: the professor's four band pictures, then heat silicon or dope it.",
      source: "Source: Day 12 p.7, p.18–25 (lecture: Na<sub>2</sub>, Na<sub>4</sub>, Na<sub><i>N</i></sub>, Zn<sub><i>N</i></sub>, the band sketch, doping). " +
        "The cluster energies come from a simple chain model (background, not from lecture): <i>N</i> orbitals give <i>N</i> levels at −2 cos(<i>k</i>π/(<i>N</i> + 1)) in arbitrary units. " +
        "Band diagrams are schematic, like the slides' sketches. Numbers marked textbook are from §18.5 (PDF p.920)." });
    var modeR = U.radios(ui.controls, { label: "View", testid: "bands-mode", value: st.mode,
      options: [["build", "Build a band (sodium)"], ["compare", "Compare solids"]], onChange: function (v) { st.mode = v; draw(); } });
    var buildBox = el("div"), cmpBox = el("div");
    ui.controls.appendChild(buildBox); ui.controls.appendChild(cmpBox);
    var nSlider = U.slider(buildBox, { label: "Sodium atoms", testid: "bands-n", min: 0, max: NS.length - 1, step: 1, value: 0,
      format: function (i) { return NS[i] ? String(NS[i]) : "a real piece (about 10²³)"; }, onInput: function (v) { st.i = v; draw(); } });
    var matSel = U.select(cmpBox, { label: "Solid", testid: "bands-solid", value: st.mat,
      options: C.MATERIALS.map(function (m) { return [m.key, m.label]; }),
      onChange: function (v) { st.mat = v; if (v !== "silicon" && st.dope !== "none") { st.dope = "none"; dopeR.set("none"); } draw(); } });
    var heatR = U.radios(cmpBox, { label: "Temperature", testid: "bands-heat", value: st.heat,
      options: [["room", "room temperature (25 °C)"], ["hot", "heated, T ↑ (100 °C)"]], onChange: function (v) { st.heat = v; draw(); } });
    var dopeR = U.radios(cmpBox, { label: "Doping (silicon only)", testid: "bands-dope", value: st.dope,
      options: [["none", "none"], ["P", "phosphorus (n-type)"], ["Ga", "gallium (p-type)"]],
      onChange: function (v) { st.dope = v; if (v !== "none" && st.mat !== "silicon") { st.mat = "silicon"; matSel.value = "silicon"; } draw(); } });
    function setMode(m) { st.mode = m; modeR.set(m); }
    U.presetButtons(ui, "bands", [["Na₂ (Day 12 p.19)", ["build", 1]], ["Na₄ (p.21)", ["build", 2]], ["Sodium metal (p.22)", ["build", 7]],
      ["Diamond (p.24)", ["compare", "diamond", "room", "none"]], ["Zinc (p.23)", ["compare", "zinc", "room", "none"]],
      ["Heated silicon (p.24)", ["compare", "silicon", "hot", "none"]], ["n-type silicon (p.25)", ["compare", "silicon", "room", "P"]],
      ["p-type silicon (p.25)", ["compare", "silicon", "room", "Ga"]]], function (p) {
      setMode(p[0]);
      if (p[0] === "build") { st.i = p[1]; nSlider.set(p[1]); }
      else { st.mat = p[1]; matSel.value = p[1]; st.heat = p[2]; heatR.set(p[2]); st.dope = p[3]; dopeR.set(p[3]); }
      draw();
    });

    /* ---------------- build a band: Na, Na2, Na4, ... Na_N side by side (textbook Fig. 18.25 = Day 12 p.22) */
    function drawBuild() {
      var W = 560, Hh = 390, g = "", n = NS[st.i], cols = NS.slice(0, st.i + 1);
      var y = function (E) { return 262 - 36 * E; };          // E −2.2 … 5.8 → y 341 … 53
      var colW = Math.min(64, 470 / cols.length), x0 = 72;
      g += energyAxis(26, 40, 345);
      g += text(x0 - 8, y(C.S.alpha) + 4, "3s", "tick strong", "end") + text(x0 - 8, y(C.P.alpha) + 4, "3p", "tick", "end");
      cols.forEach(function (N, j) {
        var cx = x0 + colW * (j + 0.5), half = Math.min(20, colW * 0.36), cur = j === cols.length - 1;
        if (cur) g += rect(cx - colW / 2 + 2, 36, colW - 4, 318, "rgba(91,155,213,0.08)", "rgba(62,106,151,0.35)", ";stroke-dasharray:3 3");
        g += text(cx, 372, N === 0 ? "Na<tspan class='sub' dy='4'>N</tspan>" : N === 1 ? "Na" : "Na<tspan class='sub' dy='4'>" + N + "</tspan>", "direct-label strong", "middle");
        if (N === 0) {                                          // the continuous bands of a real crystal
          g += rect(cx - half, y(C.P.alpha + 2), 2 * half, y(C.P.alpha - 2) - y(C.P.alpha + 2), PBAND, null, ";fill-opacity:0.55");
          g += rect(cx - half, y(0), 2 * half, y(-2) - y(0), OCC);
          g += rect(cx - half, y(2), 2 * half, y(0) - y(2), EMPTY);
          g += rect(cx - half, y(2), 2 * half, y(C.P.alpha - 2) - y(2), "url(#bands-hatch)", null);
          return;
        }
        var c = C.cluster(N), small = N <= 4;
        c.p.forEach(function (E) { g += line(cx - half, cx + half, y(E), PBAND, small ? 1.6 : 1, N <= 8); });
        c.s.forEach(function (E, k) {
          var o = c.occ[k];
          g += line(cx - half, cx + half, y(E), o > 0 ? OCC : EMPTY, small ? 2.2 : (N <= 16 ? 1.4 : 1));
          if (small && o) g += o === 2 ? arrow(cx - 5, y(E), true) + arrow(cx + 5, y(E), false) : arrow(cx, y(E), true);
        });
        if (cur && N >= 2 && N <= 16) {                         // the HOMO–LUMO gap, as on Day 12 p.20–21
          var yh = y(c.s[c.filled - 1]), yl = y(c.s[c.filled]);
          g += dblArrow(cx + half + 7, yh, yl, "#C0392B");
        }
      });
      g += "<defs><pattern id='bands-hatch' width='6' height='6' patternUnits='userSpaceOnUse' patternTransform='rotate(45)'><line x1='0' y1='0' x2='0' y2='6' style='stroke:#6B7686;stroke-width:1.4'/></pattern></defs>";
      var name = n === 0 ? "a real piece of sodium" : n === 1 ? "one sodium atom" : "Na" + sub(n);
      ui.view.innerHTML = U.svgWrap(W, Hh, "Energy levels from the 3s and 3p orbitals of " + name + ", with the clusters before it", g) +
        "<p class='xp-caption'>Purple lines: occupied MOs (arrows are electrons); orange: empty MOs from the 3s orbitals; grey: MOs from the empty 3p orbitals (each grey line stands for three). " +
        "The red arrow marks the HOMO–LUMO gap. In the last column the levels have merged into bands; the hatched region is where the 3s and 3p bands overlap.</p>";
      var msg, kv;
      if (n === 1) {
        msg = "One Na atom, [Ne]3s<sup>1</sup>: its 3s orbital holds one electron, and nothing has combined yet. Add a second atom.";
        kv = [["Atoms", 1], ["3s orbitals", 1], ["Valence electrons", 1]];
      } else if (n === 0) {
        msg = "A real piece of sodium has an enormous number of atoms, so its 3s orbitals give an enormous number of MOs, so close together that they form a continuous band: " +
          "the lower half occupied, the upper half empty, a “Valence band (partially filled)” that also overlaps the empty band from the 3p orbitals (Day 12 p.22). " +
          "A partially filled valence band makes sodium a conductor (p.18). The HOMO–LUMO gap is effectively zero: “the words “HOMO” and “LUMO” begin to become meaningless” (p.21).";
        kv = [["Atoms", "about 10<sup>23</sup>"], ["MOs from the 3s orbitals", "as many as atoms"], ["Filled", "the lower half"], ["HOMO–LUMO gap", "effectively 0"], ["Overlaps the 3p band?", "yes"]];
      } else {
        var c = C.cluster(n);
        msg = "Na" + sub(n) + ": " + n + " atoms, so their 3s orbitals give <strong>" + n + " MOs</strong> (“one molecular orbital out for every atomic orbital that we put in,” Day 12 p.7). " +
          "Its " + n + " valence electrons fill the lowest " + c.filled + ", two per MO; the other " + c.empty + " are empty. " +
          "The HOMO–LUMO gap is " + c.gapRatio.toFixed(2) + " times Na<sub>2</sub>'s" + (n > 2 ? ": “the HOMO-LUMO gap gets smaller <em>quickly</em>” (p.21)" : " (Day 12 p.19–20)") + ". " +
          (c.overlap ? "The 3s levels now reach above the lowest 3p levels: the two sets have begun to overlap (Fig. 18.25 on Day 12 p.22)." : "The 3s and 3p levels don't overlap yet.");
        kv = [["Atoms", n], ["MOs from the 3s orbitals", n], ["Valence electrons", n], ["Filled MOs", c.filled], ["Empty MOs", c.empty],
          ["HOMO–LUMO gap (Na<sub>2</sub> = 1)", c.gapRatio.toFixed(2)], ["Spread of the 3s levels (largest = 1)", c.widthRatio.toFixed(2)]];
        seenN[n] = c;
      }
      ui.readout.innerHTML = msg;
      U.kvSet(ui.kv, kv);
      var rows = NS.filter(function (N) { return N > 1 && seenN[N]; }).map(function (N) { var c = seenN[N]; return ["Na" + sub(N), c.mos, c.filled, c.empty, c.gapRatio.toFixed(2)]; });
      ui.table.innerHTML = (rows.length ? U.tableHTML(["Cluster", "MOs from 3s", "Filled", "Empty", "HOMO–LUMO gap (Na<sub>2</sub> = 1)"], rows) : "") +
        "<p class='table-note'>The clusters you have built so far. Na<sub>2</sub> and Na<sub>4</sub> are the slides' examples (Day 12 p.19–21); the gap values come from the chain model.</p>";
    }

    /* ---------------- compare solids: the professor's sketch (Day 12 p.24) and doping (p.25) */
    function drawCompare() {
      var m = byKey[st.mat], hot = st.heat === "hot", W = 440, Hh = 360, g = "", cls = C.classify(m);
      var y = function (E) { return 330 - 54 * E; };            // E 0 … 5.0 → y 330 … 60
      var x0 = 100, x1 = 240, bw = x1 - x0;
      g += energyAxis(40, 40, 330);
      // valence band, shaded where filled
      var vTop = y(m.vb[1]), vBot = y(m.vb[0]), fTop = y(m.vb[0] + (m.vb[1] - m.vb[0]) * m.vbFill);
      g += rect(x0, vTop, bw, vBot - vTop, "#FFFFFF", EDGE) + rect(x0, fTop, bw, vBot - fTop, FILL, EDGE);
      // conduction band (empty)
      var cTop = y(m.cb[1]), cBot = y(m.cb[0]);
      g += rect(x0, cTop, bw, cBot - cTop, "#FFFFFF", EDGE);
      var vLabel = m.vbFill < 1 ? "valence band (partially filled)" : "valence band (filled)";
      // heated semiconductor: a strip of electrons at the bottom of the upper band, vacancies at the top of the lower band
      var strip = 9;
      if (m.key === "silicon" && hot) {
        g += rect(x0, cBot - strip, bw, strip, FILL, EDGE) + rect(x0 + 1, vTop + 1, bw - 2, strip, "#FFFFFF", null);
      }
      // doping (silicon only)
      var lvl;
      if (m.key === "silicon" && st.dope === "P") {
        lvl = cBot + 11;                                         // just below the conduction band (Day 12 p.25)
        g += line(x0, x1, lvl, OCC, 2.2, true) + text(x1 + 10, lvl + 4, "phosphorus donor level", "tick");
        var nUp = hot ? 6 : 4;
        for (var i = 0; i < 6; i++) {
          var dx = x0 + 17 + i * 21;
          if (i < nUp) g += "<circle cx='" + dx + "' cy='" + (cBot - 5) + "' r='3.2' style='fill:" + INK + "'/>";
          else g += "<circle cx='" + dx + "' cy='" + (lvl - 5) + "' r='3.2' style='fill:" + INK + "'/>";
        }
      }
      if (m.key === "silicon" && st.dope === "Ga") {
        lvl = vTop - 13;                                         // just above the valence band (Day 12 p.25)
        g += line(x0, x1, lvl, OCC, 2.2, true) + text(x1 + 10, lvl + 4, "gallium acceptor level", "tick");
        var nAcc = hot ? 6 : 4;
        for (var j = 0; j < 6; j++) {
          var hx = x0 + 17 + j * 21;
          if (j < nAcc) {
            g += "<circle cx='" + hx + "' cy='" + (lvl - 5) + "' r='3.2' style='fill:" + INK + "'/>";
            g += "<circle cx='" + hx + "' cy='" + (vTop + 9) + "' r='6' style='fill:#FFFFFF;stroke:" + INK + ";stroke-width:1.2'/>" +
              "<text class='tick strong' x='" + hx + "' y='" + (vTop + 13) + "' text-anchor='middle'>+</text>";
          }
        }
      }
      // gap arrow and labels
      if (m.cb[0] > m.vb[1]) {
        g += dblArrow(x0 - 18, vTop, cBot, INK) + "<text class='direct-label strong' x='" + (x0 - 26) + "' y='" + ((vTop + cBot) / 2 + 4) + "' text-anchor='end'>E<tspan class='sub' dy='4'>g</tspan></text>";
      } else {
        g += text(x0 - 12, vTop + 4, "no gap", "tick strong", "end");
      }
      g += text(x1 + 10, (cTop + cBot) / 2 + 4, "conduction band (empty)", "tick") + text(x1 + 10, (vTop + vBot) / 2 + 4, vLabel, "tick");
      g += text((x0 + x1) / 2, 348, m.label + (st.dope === "P" ? ", P-doped" : st.dope === "Ga" ? ", Ga-doped" : "") + (hot ? ", heated" : ""), "direct-label strong", "middle");
      ui.view.innerHTML = U.svgWrap(W, Hh, "Band diagram of " + m.label + (st.dope !== "none" ? " doped with " + (st.dope === "P" ? "phosphorus" : "gallium") : "") + (hot ? ", heated" : ""), g) +
        "<p class='xp-caption'>Schematic, like the slides' sketches: blue = filled with electrons, white = empty; dots are electrons and circled + signs are vacancies (holes). The drawing shows where electrons are, not how many.</p>";

      var why = { diamond: "a filled valence band below a <strong>large</strong> gap: “Any material with a <strong>large enough band gap</strong> acts as an insulator” (Day 12 p.18).",
        zinc: "the filled 4s band and the empty 4p band touch, with no gap (on Day 12 p.23 they overlap): “a filled valence band that overlaps with an empty conduction band is an electrical conductor” (p.18).",
        sodium: "the 3s band is only half filled, so empty MOs sit right above the filled ones: “a partially filled valence band” (Day 12 p.18, p.22).",
        silicon: "a filled valence band and a <strong>small</strong> gap below an empty band: “And then there are the metalloids…” (Day 12 p.18, p.24)." }[m.key];
      var msg = m.label + ": " + why;
      if (m.key === "silicon" || m.key === "diamond") {
        var f25 = C.crossFactor(m.egKJ, 25), f100 = C.crossFactor(m.egKJ, 100);
        if (m.key === "silicon" && st.dope === "none") msg += hot ?
          " Heated (“T ↑,” Day 12 p.24): more electrons cross the gap, so the upper band gains a few electrons and the lower band a few vacancies, and silicon conducts better." :
          " At room temperature only a few electrons cross (textbook, PDF p.920).";
        if (m.key === "diamond") msg += hot ? " Even heated, essentially no electrons cross a gap this large." : "";
        if (st.dope === "none") msg += " Background (not from lecture): in a simple model, the fraction of electrons that cross goes as e<sup>−<i>E</i><sub>g</sub>/2<i>RT</i></sup>, which is " +
          sci(hot ? f100 : f25) + " at " + (hot ? "100" : "25") + " °C for a gap of " + (m.key === "silicon" ? "106 kJ/mol (the textbook's value)" : "about 530 kJ/mol (a literature value)") +
          (m.key === "silicon" && hot ? ", about " + Math.round(f100 / f25) + " times its 25 °C value." : ".");
      } else if (hot) {
        msg += " Heating doesn't change this picture: the highest electrons already have empty orbitals right next to them.";
      }
      if (st.dope === "P") msg += " <strong>n-type</strong> (Day 12 p.25): each P atom brings a fifth valence electron (Si has 4). Those electrons sit in a donor level just below the conduction band (about 4 kJ/mol below, textbook PDF p.920), so they move up into it easily" + (hot ? "; heated, nearly all of them have." : ".");
      if (st.dope === "Ga") msg += " <strong>p-type</strong> (Day 12 p.25): each Ga atom brings only 3 valence electrons. Its empty acceptor level lies just above the valence band (about 7 kJ/mol above, textbook PDF p.920); valence electrons move up into it and leave positive holes (⊕) behind, which let charge move.";
      ui.readout.innerHTML = msg;
      U.kvSet(ui.kv, [["Class", cls], ["Highest electrons", m.vbFill < 1 ? "inside a half-filled band" : "at the top of a filled band"],
        ["Empty orbitals right above them?", cls === "conductor" ? "yes" : "no: across a " + (cls === "insulator" ? "large" : "small") + " gap"],
        ["Band gap", m.key === "silicon" ? "106 kJ/mol (textbook)" : m.key === "diamond" ? "large (≈ 530 kJ/mol, literature)" : "none"],
        ["Doping", st.dope === "P" ? "P: n-type" : st.dope === "Ga" ? "Ga: p-type" : "none"]]);
      var key = m.key + ":" + st.dope + ":" + st.heat;
      seenM[key] = [m.label + (st.dope !== "none" ? " + " + st.dope : "") + (hot ? ", heated" : ""), cls, st.dope === "P" ? "n-type" : st.dope === "Ga" ? "p-type" : "—"];
      var rows = Object.keys(seenM).map(function (k) { return seenM[k]; });
      ui.table.innerHTML = U.tableHTML(["Solid", "Class (Day 12 p.18)", "Doping type"], rows) +
        "<p class='table-note'>The cases you have looked at so far. Diamond, zinc, sodium, and silicon are the professor's examples (Day 12 p.24); doping with P and Ga is Day 12 p.25.</p>";
    }

    function draw() {
      buildBox.hidden = st.mode !== "build"; cmpBox.hidden = st.mode !== "compare";
      if (st.mode === "build") drawBuild(); else drawCompare();
    }
    draw();
  };

  X.calcCh18 = C;
  return { calc: C };
});

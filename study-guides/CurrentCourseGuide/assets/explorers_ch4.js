/* Chapter 4 explorers for the CurrentCourseGuide (Day 8 lecture topics and §4.3–4.9 textbook previews):
   naming, Lewis symbols, the five steps, resonance, bond lengths and energies, formal charge, exceptions to the
   octet rule, and vibrating bonds. Classic script loaded after explorers.js; adds to window.Explorers.mount.
   Every Lewis drawing comes precomputed from verification/CurrentCourseGuide/lewis.py (checked structures).
   In node, module.exports gives the pure calculations (tested by test_explorers_ch4.js). */
(function (root, factory) {
  if (typeof module === "object" && module.exports) module.exports = factory(require("./explorers.js"));
  else factory(root.Explorers);
})(typeof self !== "undefined" ? self : this, function (X) {
  "use strict";
  var U = X.ui, mount = X.mount;
  var MINUS = "−";

  /* ================================================================ pure calculations */
  var C = {};
  C.gcd = function (a, b) { a = Math.abs(a); b = Math.abs(b); while (b) { var t = b; b = a % b; a = t; } return a; };
  var ROMAN = ["", "I", "II", "III", "IV", "V", "VI", "VII"];

  // ---- ionic compounds: charge balance → formula; cation name (+ Roman numeral) + anion name (Day 7 p.20–21; Day 8 p.7–9)
  C.ionic = function (cat, an) {
    var g = C.gcd(cat.q, an.q), nc = Math.abs(an.q) / g, na = cat.q / g;
    function part(f, n, poly) { return n === 1 ? f : (poly ? "(" + f + ")" : f) + n; }
    return { nc: nc, na: na, formula: part(cat.f, nc, cat.poly) + part(an.f, na, an.poly),
      name: cat.name + (cat.numeral ? "(" + ROMAN[cat.q] + ")" : "") + " " + an.name };
  };
  C.spaced = function (name) { return name.replace("(", " ("); };           // the slides' spacing: copper (II) oxide
  C.fHTML = function (f) { return String(f).replace(/(\d+)/g, "<sub>$1</sub>"); };
  C.ionHTML = function (fhtml, q) { var a = Math.abs(q); return fhtml + "<sup>" + (a === 1 ? "" : a) + (q > 0 ? "+" : MINUS) + "</sup>"; };

  // ---- covalent compounds: prefixes (Day 8 p.12–13); optional textbook vowel rule (PDF p.188)
  C.covalent = function (first, n1, second, n2, dropVowel, P) {
    var p1 = n1 === 1 ? "" : P[n1 - 1], p2 = P[n2 - 1];
    if (dropVowel && /[ao]$/.test(p2) && /^[aeiou]/.test(second[1])) p2 = p2.slice(0, -1);
    return { formula: first[0] + (n1 > 1 ? n1 : "") + second[0] + (n2 > 1 ? n2 : ""), name: p1 + first[1] + " " + p2 + second[1] };
  };
  C.covOrderOK = function (a, b, order) { return order.indexOf(a) < order.indexOf(b); };

  // ---- formal charge (textbook Eq. 4.2): atom rows are [symbol, valence e-, lone-pair e-, unpaired e-, shared e-, FC, shell]
  C.fcOf = function (row) { return row[1] - (row[2] + row[3] + row[4] / 2); };
  C.fcBest = function (structs, chi) {
    // criteria (textbook PDF p.210): (1) every FC zero; (2) most atoms zero or as close to zero as possible;
    // (3) negative FCs on the more electronegative atoms. Operationalized: smallest Σ|FC|, then most zeros,
    // then the largest Σ χ·|FC| over negative atoms.
    var scored = structs.map(function (s, i) {
      var f = s.atoms.map(function (a) { return C.fcOf(a); });
      var sumAbs = 0, zeros = 0, negChi = 0;
      f.forEach(function (x, k) { sumAbs += Math.abs(x); if (x === 0) zeros++; if (x < 0) negChi += chi[s.atoms[k][0]] * -x; });
      return { i: i, sumAbs: sumAbs, zeros: zeros, negChi: negChi };
    });
    var order = scored.slice().sort(function (a, b) { return a.sumAbs - b.sumAbs || b.zeros - a.zeros || b.negChi - a.negChi; });
    var best = order[0], next = order[1];
    var crit = best.sumAbs === 0 ? 1 : (next && next.sumAbs === best.sumAbs && next.zeros === best.zeros) ? 3 : 2;
    return { best: best.i, criterion: crit, scored: scored };
  };

  // ---- Lewis symbols: dots one per side before pairing (Day 8 p.17); a port of lewis.symbol_svg (k = dots placed)
  C.symbolCounts = function (el, k) {
    var count = { left: 0, right: 0, bottom: 0, top: 0 };
    if (el === "He") { count.left = k; return count; }
    var o1 = ["left", "right", "bottom", "top"], o2 = ["top", "bottom", "left", "right"];
    for (var n = 0; n < k; n++) { if (n < 4) count[o1[n]] = 1; else count[o2[n - 4]] = 2; }
    return count;
  };
  C.symbolSVG = function (el, V, k) {
    if (k === undefined) k = V;
    var W = 70, H = 64, cx = W / 2, cy = H / 2, r0 = el.length === 1 ? 15.5 : 19.5;
    var sides = [["left", -1, 0], ["right", 1, 0], ["bottom", 0, 1], ["top", 0, -1]];
    var count = C.symbolCounts(el, k), out = ["<text class='lw-atom' x='" + cx.toFixed(1) + "' y='" + (cy + 6.5).toFixed(1) + "' text-anchor='middle'>" + el + "</text>"];
    sides.forEach(function (sd) {
      var n = count[sd[0]], dx = sd[1], dy = sd[2], qx = cx + dx * r0, qy = cy + dy * r0;
      if (n === 1) out.push("<circle class='lw-dot' cx='" + qx.toFixed(1) + "' cy='" + qy.toFixed(1) + "' r='2.3'/>");
      else if (n === 2) {
        var px = -dy * 3.3, py = dx * 3.3;
        out.push("<circle class='lw-dot' cx='" + (qx + px).toFixed(1) + "' cy='" + (qy + py).toFixed(1) + "' r='2.2'/>" +
          "<circle class='lw-dot' cx='" + (qx - px).toFixed(1) + "' cy='" + (qy - py).toFixed(1) + "' r='2.2'/>");
      }
    });
    var unpaired = 0;
    for (var s in count) if (count[s] === 1) unpaired++;
    var aria = k === V ? "Lewis symbol of " + el + ": " + V + " valence electron" + (V !== 1 ? "s" : "") + ", " + unpaired + " unpaired"
      : "Lewis symbol of " + el + ", " + k + " of " + V + " valence electrons placed, " + unpaired + " unpaired";
    return { svg: "<svg class='lw-sym' viewBox='0 0 " + W + " " + H + "' width='" + W + "' height='" + H + "' role='img' aria-label='" + aria + "'>" + out.join("") + "</svg>", unpaired: unpaired };
  };

  // ---- vibrations: point-charge illustration of the net charge separation (BACKGROUND model)
  var VIB = {
    CO2: { label: "CO₂", atoms: [["O", -1, -1], ["C", 0, 2], ["O", 1, -1]], masses: [16, 12, 16], modes: ["sym", "asym", "bend"] },
    N2: { label: "N₂", atoms: [["N", -0.55, 0], ["N", 0.55, 0]], masses: [14, 14], modes: ["stretch"] },
    O2: { label: "O₂", atoms: [["O", -0.6, 0], ["O", 0.6, 0]], masses: [16, 16], modes: ["stretch"] },
    CO: { label: "CO", atoms: [["C", -0.5, 1], ["O", 0.5, -1]], masses: [12, 16], modes: ["stretch"] },
    HCl: { label: "HCl", atoms: [["H", -0.6, 1], ["Cl", 0.6, -1]], masses: [1, 35], modes: ["stretch"] }
  };
  C.VIB = VIB;
  C.vib = function (key, mode, phase) {
    var m = VIB[key], s = Math.sin(phase), A = 0.14;
    var pos = m.atoms.map(function (a) { return { el: a[0], x: a[1], y: 0, q: a[2] }; });
    if (key === "CO2") {
      var f = m.masses[1] / (m.masses[0] + m.masses[2]);                      // keeps the centre of mass fixed
      if (mode === "sym") { pos[0].x -= A * s; pos[2].x += A * s; }
      else if (mode === "asym") { pos[1].x += A * s; pos[0].x -= A * s * f; pos[2].x -= A * s * f; }
      else { pos[1].y += A * s; pos[0].y -= A * s * f; pos[2].y -= A * s * f; }
    } else {
      var m1 = m.masses[0], m2 = m.masses[1], L = (m.atoms[1][1] - m.atoms[0][1]) * (1 + A * s);
      pos[0].x = -L * m2 / (m1 + m2); pos[1].x = L * m1 / (m1 + m2);
    }
    var dx = 0, dy = 0;
    pos.forEach(function (p) { dx += p.q * p.x; dy += p.q * p.y; });
    return { atoms: pos, dipole: { x: dx, y: dy } };
  };
  C.vibSwing = function (key, mode) {                                        // size of the dipole's oscillation
    var a = C.vib(key, mode, Math.PI / 2).dipole, b = C.vib(key, mode, -Math.PI / 2).dipole;
    return Math.hypot(a.x - b.x, a.y - b.y) / 2;
  };

  C.bondSeries = function (table, a, b) {
    return table.filter(function (r) { return (r.a === a && r.b === b) || (r.a === b && r.b === a); })
      .sort(function (x, y) { return x.order - y.order; });
  };
  C.boText = function (x) {
    if (Math.abs(x - Math.round(x)) < 1e-9) return String(Math.round(x));
    return Math.abs(x * 2 - Math.round(x * 2)) < 1e-9 ? x.toFixed(1) : x.toFixed(2);
  };

  /* ================================================================ shared view helpers (browser only) */
  var el = U && U.el;
  function fcText(v) { return v === 0 ? "0" : (v > 0 ? "+" : MINUS) + Math.abs(v); }
  function tag(t) {
    return t === "lecture" ? "<span class='pill-label lecture'>Lecture example</span>" :
      t === "textbook" ? "<span class='pill-label preview'>Textbook example</span>" : "<span class='pill-label'>New example</span>";
  }
  function dataTable(head, rows) { return "<div class='table-wrap'>" + U.tableHTML(head, rows).replace("<table>", "<table class='data'>") + "</div>"; }
  function prevNext(parent, name, onPrev, onNext) {
    var row = el("div", { class: "ctl-row" });
    var a = U.button(row, "Previous step", "btn-" + name + "-prev", onPrev);
    var b = U.button(row, "Next step", "btn-" + name + "-next", onNext);
    parent.appendChild(row);
    return [a, b];
  }

  /* ================================================================ naming (m16 ionic, m17 covalent, t4-3 acid) */
  mount.naming = function (host, D) {
    var N = D.naming, mode = host.getAttribute("data-mode") || "ionic", tid = "nm-" + mode;
    if (mode === "covalent") return namingCovalent(host, N, tid);
    if (mode === "acid") return namingAcid(host, N, tid);
    var cats = N.cations, ans = N.anions;
    var st = { c: "Cu2", a: "O", spaced: false };
    var ui = U.shell(host, { title: "Explorer: name an ionic compound",
      intro: "Pick a cation and an anion. The explorer balances the charges, writes the formula, and builds the name, showing each rule it uses.",
      source: "Source: Day 7 p.20–21 and Day 8 p.6–9 (charge balance, cation + anion names, Roman numerals, polyatomic ions); textbook §4.3 PDF p.191–193 for the no-numeral metals and parentheses (textbook preview). Transition-metal ion charges: textbook Fig. 2.11." });
    function catLabel(c) { return U.formulaText(c.f) + (c.q > 1 ? U.uniSup(c.q + "+") : "⁺") + "  " + c.name + (c.numeral ? "(" + ROMAN[c.q] + ")" : ""); }
    function anLabel(a) { return U.formulaText(a.f) + U.uniSup((a.q < -1 ? -a.q : "") + MINUS) + "  " + a.name; }
    U.select(ui.controls, { label: "Cation", testid: tid + "-cat", value: st.c, options: cats.map(function (c) { return [c.key, catLabel(c)]; }), onChange: function (v) { st.c = v; draw(); } });
    U.select(ui.controls, { label: "Anion", testid: tid + "-an", value: st.a, options: ans.map(function (a) { return [a.key, anLabel(a)]; }), onChange: function (v) { st.a = v; draw(); } });
    U.checkbox(ui.controls, { label: "Show the slides' spacing, “copper (II) oxide”", testid: tid + "-spaced", value: st.spaced, onChange: function (v) { st.spaced = v; draw(); } });
    U.presetButtons(ui, tid, [["CuO (Day 8 p.7)", { c: "Cu2", a: "O" }], ["LiNO₃ (Day 8 p.9)", { c: "Li", a: "NO3" }], ["NH₄ClO₂ (Day 8 p.9)", { c: "NH4", a: "ClO2" }],
      ["Mg₃(PO₄)₂ (textbook)", { c: "Mg", a: "PO4" }], ["zinc chloride (textbook)", { c: "Zn", a: "Cl" }]], function (p) {
      st.c = p.c; st.a = p.a; host.querySelector("[data-testid='select-" + tid + "-cat']").value = p.c; host.querySelector("[data-testid='select-" + tid + "-an']").value = p.a; draw(); });
    function draw() {
      var c = cats.filter(function (x) { return x.key === st.c; })[0], a = ans.filter(function (x) { return x.key === st.a; })[0];
      var r = C.ionic(c, a), catH = C.ionHTML(C.fHTML(c.f), c.q), anH = C.ionHTML(a.html, a.q);
      var name = st.spaced ? C.spaced(r.name) : r.name, tiles = "", i;
      for (i = 0; i < r.nc; i++) tiles += "<span class='tile tile-cat'><span>" + catH + "</span></span>";
      for (i = 0; i < r.na; i++) tiles += "<span class='tile tile-an'><span>" + anH + "</span></span>";
      var bal = r.nc + " × (" + (c.q > 0 ? "+" : "") + c.q + ") + " + r.na + " × (" + MINUS + (-a.q) + ") = 0";
      var steps = ["<li>Charges: " + catH + " and " + anH + (a.poly ? " (a polyatomic ion from the ion table, Day 8 p.8)" : "") + ".</li>",
        "<li>Total charge zero (Day 7 p.20): " + bal + " → " + r.nc + " : " + r.na + ".</li>"];
      if (c.numeral) steps.push("<li>" + c.name[0].toUpperCase() + c.name.slice(1) + " forms more than one common ion, so the name gives this ion's charge as a Roman numeral: (" + ROMAN[c.q] + ") (Day 8 p.7).</li>");
      else if (c.key === "Zn" || c.key === "Ag") steps.push("<li><span class='pill-label preview'>Textbook preview</span> " + c.name + " forms only one cation, so the textbook uses no numeral (PDF p.191).</li>");
      if ((a.poly && r.na > 1) || (c.poly && r.nc > 1)) steps.push("<li><span class='pill-label preview'>Textbook preview</span> More than one of a polyatomic ion: put it in parentheses before its subscript (PDF p.193).</li>");
      steps.push("<li>Name: the cation's name, then the anion's name, with no prefixes (Day 7 p.21; Day 8 p.9)" + (a.alt ? "; the slide also gives its other name, " + a.alt : "") + ".</li>");
      ui.view.innerHTML = "<div class='tiles' aria-label='" + r.nc + " cation" + (r.nc > 1 ? "s" : "") + " and " + r.na + " anion" + (r.na > 1 ? "s" : "") + "'>" + tiles + "</div><ol class='rules'>" + steps.join("") + "</ol>";
      ui.readout.innerHTML = "Formula <strong>" + C.fHTML(r.formula) + "</strong>; name <strong>" + name + "</strong>.";
      U.kvSet(ui.kv, [["Cation", catH], ["Anion", anH], ["Ratio", r.nc + " : " + r.na], ["Formula", C.fHTML(r.formula)], ["Name", name]]);
      ui.table.innerHTML = U.tableHTML(["Cation", "Formula with " + anH, "Name"], cats.map(function (cc) {
        var rr = C.ionic(cc, a); return [C.ionHTML(C.fHTML(cc.f), cc.q), C.fHTML(rr.formula), st.spaced ? C.spaced(rr.name) : rr.name]; }));
    }
    draw();
  };

  function namingCovalent(host, N, tid) {
    var st = { a: "S", n1: 1, b: "O", n2: 2, vowel: false };
    var ui = U.shell(host, { title: "Explorer: name a covalent compound",
      intro: "Choose two nonmetals and how many atoms of each. Watch which prefixes the name needs.",
      source: "Source: Day 8 p.12–13 (prefix rule, Table 4.3, no “mono” on the first element). Textbook preview: dropping a prefix's final o or a before “oxide” (PDF p.188); which element is written first (PDF p.220)." });
    var nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map(function (n) { return [String(n), n + " (" + N.prefixes[n - 1] + "-)"]; });
    U.select(ui.controls, { label: "First element", testid: tid + "-el1", value: st.a, options: N.covFirst.map(function (x) { return [x[0], x[0] + "  " + x[1]]; }), onChange: function (v) { st.a = v; draw(); } });
    U.select(ui.controls, { label: "Number of atoms", testid: tid + "-n1", value: "1", options: nums.slice(0, 4), onChange: function (v) { st.n1 = +v; draw(); } });
    U.select(ui.controls, { label: "Second element", testid: tid + "-el2", value: st.b, options: N.covSecond.map(function (x) { return [x[0], x[0] + "  " + x[1]]; }), onChange: function (v) { st.b = v; draw(); } });
    U.select(ui.controls, { label: "Number of atoms", testid: tid + "-n2", value: "2", options: nums, onChange: function (v) { st.n2 = +v; draw(); } });
    U.checkbox(ui.controls, { label: "Apply the textbook's vowel rule (monoxide, pentoxide)", testid: tid + "-vowel", value: false, onChange: function (v) { st.vowel = v; draw(); } });
    U.presetButtons(ui, tid, [["SO₂ (Day 8 p.13)", ["S", 1, "O", 2]], ["SO₃ (Day 8 p.13)", ["S", 1, "O", 3]], ["S₂F₂ (Day 8 p.13)", ["S", 2, "F", 2]], ["N₂O (textbook)", ["N", 2, "O", 1]]], function (p) {
      st.a = p[0]; st.n1 = p[1]; st.b = p[2]; st.n2 = p[3];
      [["el1", p[0]], ["n1", String(p[1])], ["el2", p[2]], ["n2", String(p[3])]].forEach(function (q) { host.querySelector("[data-testid='select-" + tid + "-" + q[0] + "']").value = q[1]; });
      draw(); });
    function draw() {
      var first = N.covFirst.filter(function (x) { return x[0] === st.a; })[0], second = N.covSecond.filter(function (x) { return x[0] === st.b; })[0];
      if (st.a === st.b) { ui.view.innerHTML = "<p class='xp-caption'>Pick two different elements: a binary compound has two.</p>"; ui.readout.innerHTML = ""; U.kvSet(ui.kv, []); return; }
      var r = C.covalent(first, st.n1, second, st.n2, st.vowel, N.prefixes), plain = C.covalent(first, st.n1, second, st.n2, false, N.prefixes);
      var tb = C.covalent(first, st.n1, second, st.n2, true, N.prefixes);
      var rules = ["<li>Both are nonmetals: a covalent compound, named with prefixes (Day 8 p.12).</li>",
        "<li>First word: " + (st.n1 === 1 ? "one " + first[1] + " atom, and “we do not use ‘mono’ for the <strong>first</strong> element”" : N.prefixes[st.n1 - 1] + "- for " + st.n1 + " atoms") + " (Day 8 p.12).</li>",
        "<li>Second word: " + N.prefixes[st.n2 - 1] + "- for " + st.n2 + ", and the element's name ending in -ide: " + second[1] + ".</li>"];
      if (tb.name !== plain.name) rules.push("<li><span class='pill-label preview'>Textbook preview</span> The textbook drops the prefix's final vowel before “oxide”: " + tb.name + " (PDF p.188). The slides give no rule, so " + plain.name + " follows them literally.</li>");
      if (!C.covOrderOK(st.a, st.b, N.covOrder)) rules.push("<li class='rule-no'><span class='rule-icon' aria-hidden='true'>✗</span>Usually written the other way round: " + st.b + " comes first here (the element farther left, or lower in its group: textbook PDF p.220; oxygen is written after the halogens other than F, as in the textbook's dibromine monoxide, PDF p.189).</li>");
      ui.view.innerHTML = "<p class='xp-caption'>Formula: <strong>" + C.fHTML(r.formula) + "</strong></p><ol class='rules'>" + rules.join("") + "</ol>";
      ui.readout.innerHTML = C.fHTML(r.formula) + " is <strong>" + r.name + "</strong>.";
      U.kvSet(ui.kv, [["Formula", C.fHTML(r.formula)], ["Name (slides' rules)", plain.name], ["Name (textbook)", tb.name]]);
      ui.table.innerHTML = U.tableHTML(["Number", "Prefix (Table 4.3)"], N.prefixes.map(function (p, i) { return [i + 1, p + "-"]; }));
    }
    draw();
  }

  function namingAcid(host, N, tid) {
    var st = { a: "Cl" };
    var ui = U.shell(host, { title: "Explorer: name an acid",
      intro: "Pick the anion. An acid needs enough H⁺ ions to balance its charge; the anion's name ending decides the acid's name.",
      source: "Source: textbook preview, §4.3 Binary Acids and Oxoacids (PDF p.193–195, Table 4.5). Not yet taught in lecture." });
    var byKey = {};
    N.anions.forEach(function (a) { byKey[a.key] = a; });
    U.select(ui.controls, { label: "Anion", testid: tid + "-an", value: st.a, options: N.acids.map(function (x) { var a = byKey[x.anion]; return [x.anion, U.formulaText(a.f) + U.uniSup((a.q < -1 ? -a.q : "") + MINUS) + "  " + a.name]; }), onChange: function (v) { st.a = v; draw(); } });
    U.presetButtons(ui, tid, [["chloride", "Cl"], ["sulfate", "SO4"], ["nitrite", "NO2"], ["hypochlorite", "ClO"]], function (k) { st.a = k; host.querySelector("[data-testid='select-" + tid + "-an']").value = k; draw(); });
    function draw() {
      var x = N.acids.filter(function (y) { return y.anion === st.a; })[0], a = byKey[st.a], anH = C.ionHTML(a.html, a.q);
      var rule = x.kind === "binary" ? "A binary acid (H + one other element, in water): hydro- + the element's root + -ic + acid."
        : /ate$/.test(a.name) ? "An oxoacid from an -ate anion: -ate → -ic acid, no hydro-." : "An oxoacid from an -ite anion: -ite → -ous acid, no hydro-.";
      ui.view.innerHTML = "<div class='tiles'>" + new Array(-a.q + 1).join("<span class='tile tile-cat'><span>H<sup>+</sup></span></span>") + "<span class='tile tile-an'><span>" + anH + "</span></span></div>" +
        "<ol class='rules'><li>" + (-a.q) + " H<sup>+</sup> balance " + anH + ": " + C.fHTML(x.f) + (x.kind === "binary" ? "(aq)" : "") + ".</li><li>" + rule + "</li><li>Anion: " + a.name + " → <strong>" + x.name + "</strong> (" + x.src + ").</li></ol>";
      ui.readout.innerHTML = C.fHTML(x.f) + (x.kind === "binary" ? "(aq)" : "") + " is <strong>" + x.name + "</strong>.";
      U.kvSet(ui.kv, [["Anion", anH + " " + a.name], ["Acid", C.fHTML(x.f)], ["Name", x.name]]);
      ui.table.innerHTML = U.tableHTML(["Anion", "Acid", "Name"], N.acids.map(function (y) { var b = byKey[y.anion]; return [C.ionHTML(b.html, b.q) + " " + b.name, C.fHTML(y.f), y.name]; }));
    }
    draw();
  }

  /* ================================================================ m18: Lewis symbols */
  mount.lewisSymbol = function (host, D) {
    var S = D.lewisSymbols, st = { el: "N", k: null };
    var ui = U.shell(host, { title: "Explorer: Lewis symbols and bonding capacity",
      intro: "Pick an element, then add its valence electrons one at a time: one per side before pairing. Unpaired dots are the bonds it can form.",
      source: "Source: Day 8 p.16–18 (octet rule, placement rule, bonding capacity). The dot arrangement follows the slide's table." });
    var grid = el("div", { class: "sym-grid", role: "group", "aria-label": "Elements" });
    var COLS = [1, 2, 13, 14, 15, 16, 17, 18];
    ui.controls.appendChild(el("p", { class: "ctl-label" }, "Element"));
    S.forEach(function (x) {
      var b = el("button", { type: "button", class: "sym-btn", "data-testid": "sym-" + x.el, "aria-pressed": "false", style: "grid-column:" + (COLS.indexOf(x.group) + 1) }, x.el);
      b.addEventListener("click", function () { st.el = x.el; st.k = null; draw(); });
      grid.appendChild(b);
    });
    ui.controls.appendChild(grid);
    var sl = U.slider(ui.controls, { label: "Electrons placed", testid: "sym-step", min: 0, max: 8, step: 1, value: 5, format: function (v) { return String(v); }, onInput: function (v) { st.k = v; draw(true); } });
    function draw(fromSlider) {
      var x = S.filter(function (y) { return y.el === st.el; })[0];
      if (st.k === null || st.k > x.valence) st.k = x.valence;
      sl.input.max = x.valence; if (!fromSlider) sl.set(st.k);
      Array.prototype.forEach.call(grid.children, function (b) { b.setAttribute("aria-pressed", b.textContent === st.el ? "true" : "false"); });
      var r = C.symbolSVG(x.el, x.valence, st.k), full = st.k === x.valence;
      var metal = ["Li", "Na", "K", "Be", "Mg", "Ca", "Al"].indexOf(x.el) >= 0, noble = x.group === 18;
      var goal = x.el === "H" || x.el === "He" ? 2 : 8;
      ui.view.innerHTML = "<div class='sym-big'>" + r.svg.replace("width='70' height='64'", "width='210' height='192'") + "</div>";
      var msg = !full ? st.k + " of " + x.valence + " valence electrons placed. " + (st.k < 4 ? "Each new dot goes on an empty side." : "All four sides have a dot, so each new one makes a pair.")
        : x.el + ": group " + x.group + ", " + x.valence + " valence electron" + (x.valence > 1 ? "s" : "") + ", " + r.unpaired + " unpaired. " +
          (noble ? "A noble gas: its valence shell is already full, so it forms no bonds." :
            metal ? "A metal: it usually <em>loses</em> these " + x.valence + " electron" + (x.valence > 1 ? "s" : "") + " to form a cation (Day 7 p.18) rather than sharing them." :
              "Bonding capacity " + r.unpaired + ": it forms " + r.unpaired + " covalent bond" + (r.unpaired > 1 ? "s" : "") + " to reach " + goal + " electrons (Day 8 p.18)." + (x.el === "C" ? " Carbon “ALMOST ALWAYS forms 4 covalent bonds.”" : ""));
      ui.readout.innerHTML = msg;
      U.kvSet(ui.kv, [["Group", x.group], ["Valence electrons", x.valence], ["Unpaired dots", r.unpaired], ["Goal", goal + " electrons" + (goal === 2 ? " ([He])" : "")]]);
      ui.table.innerHTML = U.tableHTML(["Element", "Group", "Valence e⁻", "Unpaired (bonding capacity)"], S.map(function (y) { return [y.el, y.group, y.valence, y.unpaired]; }));
    }
    draw();
  };

  /* ================================================================ m19: the five steps */
  mount.lewisSteps = function (host, D) {
    var S = D.lewisSteps, ids = Object.keys(S), st = { id: "NH3", step: 0 };
    var ui = U.shell(host, { title: "Explorer: the five steps, one at a time",
      intro: "Pick a molecule and step through the professor's five steps. Before each step, predict where the next electrons go.",
      source: "Source: Day 8 p.21 (the five steps, word for word) with the Day 8 examples (F₂ p.19, NH₃ p.22–23, C₂H₂ p.24–25, O₃ p.28–30). Other molecules are textbook §4.4–4.5 examples. Counting an ion's charge in step 1 and the brackets are textbook preview." });
    U.select(ui.controls, { label: "Molecule or ion", testid: "steps-mol", value: st.id, options: ids.map(function (k) { var s = S[k]; return [k, s.name.replace(/ \(.*\)$/, "") + (s.tag === "lecture" ? "  (lecture)" : "")]; }), onChange: function (v) { st.id = v; st.step = 0; draw(); } });
    prevNext(ui.controls, "steps", function () { st.step = Math.max(0, st.step - 1); draw(); }, function () { st.step = Math.min(4, st.step + 1); draw(); });
    var TEXT = ["1. Determine the number of valence electrons.",
      "2. Arrange symbols of elements to show how the atoms are bonded together and connect them with single bonds. The central atom is the one with the largest bonding capacity.",
      "3. Complete the octet of atoms bonded to each “central” atom by adding lone pairs of electrons (exception: hydrogen only needs two).",
      "4. Compare the number of valence electrons in the Lewis structure to the number determined in step 1. 5. Use any leftover electrons to complete the octet on the central atom.",
      ""];
    function shortText(list) {
      if (list.length === 1) return list[0] + " has";
      var same = list.every(function (x) { return x === list[0]; });
      return (same ? "both " + list[0] + " atoms" : list.join(" and ")) + " have";
    }
    function draw() {
      var s = S[st.id], k = st.step;
      var total = s.total, head = "<p class='xp-caption'>" + tag(s.tag) + " " + s.formula + "</p>";
      if (k === 0) {
        var rows = s.table.map(function (r) { return [r[0], r[1], r[2], r[1] * r[2]]; });
        if (s.charge) rows.push([s.charge < 0 ? "plus " + (-s.charge) + " for the " + (-s.charge > 1 ? -s.charge : "") + MINUS + " charge" : "minus " + s.charge + " for the " + (s.charge > 1 ? s.charge : "") + "+ charge", "", "", (s.charge < 0 ? "+" : MINUS) + Math.abs(s.charge)]);
        rows.push(["<strong>Valence electrons</strong>", "", "", "<strong>" + total + "</strong>"]);
        ui.view.innerHTML = head + "<p class='step-text'>" + TEXT[0] + "</p>" + dataTable(["Element", "Atoms", "Valence e⁻ per atom", "Total"], rows) +
          (s.charge ? "<p class='note'><span class='pill-label preview'>Textbook preview</span> The slides' examples are all neutral; the textbook adds an electron for each negative charge and removes one for each positive charge (PDF p.197).</p>" : "");
        ui.readout.innerHTML = "Step 1: " + total + " valence electrons to place.";
      } else {
        var f = s.frames[k - 1], short = f.short.length ? f.short : [];
        var label = k === 4 ? (f.same ? "Finished: every atom already has its octet (H: 2)." : "After step 5, " + shortText(s.frames[2].short) + " fewer than 8, so lone pairs on a neighboring atom became shared pairs, as in O₂, N₂, C₂H₂, and O₃ (Day 8 p.20, p.25, p.30). Now every atom has its octet (H: 2).") : TEXT[k];
        ui.view.innerHTML = head + "<p class='step-text'>" + (k === 3 ? TEXT[3] : k === 4 ? "" : TEXT[k]) + "</p><div class='lw-row'>" + f.svg + "</div>" +
          "<p class='xp-caption'>" + f.label + ".</p>" + (k === 4 && !f.same ? "<p class='connection'>The five steps stop at step 5; the slides' ethyne and ozone examples show this last move (Day 8 p.25, p.30). The textbook writes it into its step 5 (PDF p.197).</p>" : "");
        var left = total - f.used;
        ui.readout.innerHTML = (k === 4 ? label : "Placed " + f.used + " of " + total + " electrons; " + left + " left over." + (short.length && k === 3 ? " Now " + shortText(short).replace(/ has$/, " is").replace(/ have$/, " are") + " still short of an octet." : ""));
      }
      U.kvSet(ui.kv, [["Step", (k === 0 ? "1" : k === 3 ? "4–5" : k === 4 ? "after 5" : String(k + 1)) + " of 5"], ["Valence electrons", total], ["Placed", k === 0 ? "0" : s.frames[k - 1].used]]);
      ui.table.innerHTML = U.tableHTML(["Molecule", "Valence e⁻", "Needs a multiple bond?"], ids.map(function (q) { var x = S[q]; return [x.formula, x.total, x.frames[3].same ? "no" : "yes"]; }));
      host.querySelector("[data-testid='btn-steps-prev']").disabled = k === 0;
      host.querySelector("[data-testid='btn-steps-next']").disabled = k === 4;
    }
    draw();
  };

  /* ================================================================ t4-5: resonance */
  mount.resonance = function (host, D) {
    var R = D.resonance, st = { key: "O3", avg: false };
    var ui = U.shell(host, { title: "Explorer: resonance structures and their average",
      intro: "Compare the valid structures of one species, then switch to their average, the resonance hybrid. What happens to the bonds that trade places?",
      source: "Source: ozone (Day 8 p.30; Day 9 p.6–10) and benzene (Day 9 p.12–13) are the lecture's examples: structures “in resonance” are interconverted “by just moving electrons” (Day 9 p.8), and the real molecule is “an average of the two” (Day 9 p.9). Nitrate, carbonate, and the numerical bond orders are textbook preview (§4.5–4.6, PDF p.203–208). Bond lengths: Table 4.6 (Day 9 p.14). The slide draws the hybrid with dashed partial bonds and lone-pair dots (Day 9 p.10); this guide's drawing adds bond-order numbers and leaves out the dots." });
    U.select(ui.controls, { label: "Species", testid: "res-species", value: st.key, options: R.map(function (r) { return [r.key, r.label + (r.tag === "lecture" ? "  (lecture)" : "")]; }), onChange: function (v) { st.key = v; draw(); } });
    U.radios(ui.controls, { label: "Show", testid: "res-view", value: "all", options: [["all", "the resonance structures"], ["avg", "their average"]], onChange: function (v) { st.avg = v === "avg"; draw(); } });
    function draw() {
      var r = R.filter(function (x) { return x.key === st.key; })[0];
      var pics = st.avg ? "<div class='lw-row'>" + r.hybrid + "</div><p class='xp-caption'>Solid lines: shared pairs in every structure. Dashed: a pair spread over several bonds. Numbers: average bond order.</p>"
        : "<div class='lw-row'>" + r.structs.map(function (s) { return s.svg; }).join("<span class='lw-arrow' role='img' aria-label='resonance arrow'>↔</span>") + "</div>";
      var bo = C.boText(r.avg), pair = r.pair[0], L1 = r.single[0], L2 = r.double[0];
      ui.view.innerHTML = "<p class='xp-caption'>" + tag(r.tag) + " " + r.label + "</p>" + pics;
      ui.readout.innerHTML = r.structs.length + " equivalent structures. The " + pair.replace("–", "–") + " bonds share " + r.pairs + " pairs over " + r.nBonds + " bonds: bond order " + r.pairs + "/" + r.nBonds + " = " + bo +
        ", so each should be between a single bond (" + L1 + " pm) and a double bond (" + L2 + " pm)" + (r.measured ? "; measured: " + r.measured + " pm." : ".");
      U.kvSet(ui.kv, [["Structures", r.structs.length], ["Average bond order", bo], [pair + " (single)", L1 + " pm, " + r.single[1] + " kJ/mol"], [r.pair[1] + " (double)", L2 + " pm, " + r.double[1] + " kJ/mol"], ["Measured", r.measured ? r.measured + " pm" : "not given in the textbook"]]);
      ui.table.innerHTML = U.tableHTML(["Species", "Structures", "Bond", "Average bond order", "Source"], R.map(function (x) { return [x.label, x.structs.length, x.pair[0], C.boText(x.avg), x.src]; }));
    }
    draw();
  };

  /* ================================================================ t4-6: bond lengths and energies (Table 4.6) */
  mount.bondChart = function (host, D) {
    var T = D.bondTable, R = D.resonance, st = { pair: "C–O", metric: "pm", mark: "CO3" };
    var PAIRS = [["C–C", "C", "C"], ["C–N", "C", "N"], ["C–O", "C", "O"], ["N–N", "N", "N"], ["N–O", "N", "O"], ["O–O", "O", "O"], ["S–O", "S", "O"]];
    var ui = U.shell(host, { title: "Explorer: bond order, length, and strength",
      intro: "Pick a pair of atoms and compare its single, double, and triple bonds. Then place a resonance-averaged bond on the same axes.",
      source: "Source: Table 4.6 (Day 9 p.14, the textbook's table, PDF p.207) and outcome 7, “Describe how bond order, bond energy, and bond length are related” (Day 9 p.5). Ozone's measured 128 pm is on Day 9 p.7. Carbonate's 129 pm and the numerical bond orders of resonance-averaged bonds are textbook preview (§4.6, PDF p.206–208)." });
    U.select(ui.controls, { label: "Atom pair", testid: "bond-pair", value: st.pair, options: PAIRS.map(function (p) { return [p[0], p[0]]; }), onChange: function (v) { st.pair = v; st.mark = ""; draw(); } });
    U.radios(ui.controls, { label: "Show", testid: "bond-metric", value: st.metric, options: [["pm", "bond length (pm)"], ["kj", "bond energy (kJ/mol)"]], onChange: function (v) { st.metric = v; draw(); } });
    var markSel = U.select(ui.controls, { label: "Add a resonance-averaged bond", testid: "bond-mark", value: st.mark, options: [["", "none"]].concat(R.map(function (r) { return [r.key, r.label + " (" + r.pair[0] + ", order " + C.boText(r.avg) + ")"]; })), onChange: function (v) {
      st.mark = v; if (v) { var r = R.filter(function (x) { return x.key === v; })[0]; st.pair = r.pair[0].replace(/[=≡]/, "–"); host.querySelector("[data-testid='select-bond-pair']").value = st.pair; } draw(); } });
    function draw() {
      var p = PAIRS.filter(function (x) { return x[0] === st.pair; })[0], rows = C.bondSeries(T, p[1], p[2]);
      var vals = rows.map(function (r) { return r[st.metric]; }), mk = st.mark ? R.filter(function (x) { return x.key === st.mark; })[0] : null;
      var lo = st.metric === "pm" ? 60 : 0, hi = st.metric === "pm" ? 180 : 1150;
      var f = U.frame({ w: 520, h: 300, x0: 0.5, x1: 3.5, y0: lo, y1: hi, xlabel: "bond order", ylabel: st.metric === "pm" ? "bond length (pm)" : "bond energy (kJ/mol)",
        xticks: [[1, "1"], [1.5, "1.5"], [2, "2"], [2.5, "2.5"], [3, "3"]], yticks: (st.metric === "pm" ? [60, 90, 120, 150, 180] : [0, 250, 500, 750, 1000]).map(function (v) { return [v, String(v)]; }) });
      var pts = rows.map(function (r) { return [f.xs(r.order), f.ys(r[st.metric])]; });
      var g = "<path class='series-line' d='" + U.linePath(pts) + "' style='stroke:" + U.SERIES[0] + "'/>";
      rows.forEach(function (r, i) {
        g += "<g><title>" + r.bond + ": " + r.pm + " pm, " + r.kj + " kJ/mol</title><circle cx='" + pts[i][0].toFixed(1) + "' cy='" + pts[i][1].toFixed(1) + "' r='6' style='fill:" + U.SERIES[0] + ";stroke:#FFF;stroke-width:2'/>" +
          "<text class='direct-label' x='" + (pts[i][0] + (i === 0 ? -10 : 10)).toFixed(1) + "' y='" + (pts[i][1] - 8).toFixed(1) + "'" + (i === 0 ? " text-anchor='end'" : "") + ">" + r.bond + " " + r[st.metric] + "</text></g>";
      });
      var note = "";
      if (mk && mk.pair[0].replace(/[=≡]/, "–") === st.pair) {
        var x = f.xs(mk.avg);
        g += "<line x1='" + x.toFixed(1) + "' x2='" + x.toFixed(1) + "' y1='" + f.m.t + "' y2='" + (f.m.t + f.ph) + "' style='stroke:" + U.SERIES[1] + ";stroke-width:2;stroke-dasharray:5 4'/>" +
          "<text class='direct-label' x='" + (x + 6).toFixed(1) + "' y='" + (f.m.t + 14) + "'>" + mk.label.split(",")[0] + ", order " + C.boText(mk.avg) + "</text>";
        if (mk.measured && st.metric === "pm") {
          var y = f.ys(mk.measured);
          g += "<g><title>measured: " + mk.measured + " pm</title><rect x='" + (x - 6).toFixed(1) + "' y='" + (y - 6).toFixed(1) + "' width='12' height='12' style='fill:#FFF;stroke:" + U.SERIES[1] + ";stroke-width:2.5'/></g>" +
            "<text class='direct-label' x='" + (x - 10).toFixed(1) + "' y='" + (y + 18).toFixed(1) + "' text-anchor='end'>measured " + mk.measured + " pm</text>";
        }
        note = mk.label + ": bond order " + C.boText(mk.avg) + " falls between the single and double bonds" + (mk.measured ? ", and its measured length (" + mk.measured + " pm) does too." : ".");
      }
      ui.view.innerHTML = U.svgWrap(520, 300, st.pair + " bonds: " + rows.map(function (r) { return r.bond + " " + r[st.metric]; }).join(", "), f.axes + g);
      var trend = st.metric === "pm" ? "More shared pairs, shorter bond" : "More shared pairs, stronger bond (but not in proportion)";
      ui.readout.innerHTML = trend + ": " + rows.map(function (r) { return r.bond + " " + r[st.metric] + (st.metric === "pm" ? " pm" : " kJ/mol"); }).join(" → ") + ". " + note;
      U.kvSet(ui.kv, rows.map(function (r) { return [r.bond, r.pm + " pm; " + r.kj + " kJ/mol"]; }));
      ui.table.innerHTML = U.tableHTML(["Bond", "Length (pm)", "Energy (kJ/mol)"], T.map(function (r) { return [r.bond, r.pm, r.kj + (r.bond === "C=O" ? "<sup>a</sup>" : "")]; })) +
        "<p class='source'><sup>a</sup>799 kJ/mol for the C=O bonds in CO₂ (Table 4.6 footnote).</p>";
    }
    draw();
  };

  /* ================================================================ t4-7: formal charge */
  mount.formalCharge = function (host, D) {
    var F = D.fcSets, chi = D.chi, st = { key: "N2O", i: 0, show: false };
    var ui = U.shell(host, { title: "Explorer: formal charges and the best structure",
      intro: "Work out each atom's formal charge with the four steps (Day 9 p.22), then reveal it. For a set of structures, see which one the rules on Day 9 p.23 pick, and why. Phosphoric acid is the Day 9 p.26 Top Hat question (structures 1–3; P is in row 3, so it may exceed an octet, Day 9 p.29).",
      source: "Source: Day 9 p.19–26 (the N₂O exercise, the four steps and four rules, the phosphoric-acid Top Hat) and Day 9 p.30 (sulfate). The verdict applies rules 1–3; rule 4, the sum check, is in the readout. Carbon dioxide, phosphate, and sulfuric acid are textbook examples (§4.7–4.8, PDF p.211–216)." });
    U.select(ui.controls, { label: "Species", testid: "fc-set", value: st.key, options: F.map(function (f) { return [f.key, f.label]; }), onChange: function (v) { st.key = v; st.i = 0; build(); } });
    var box = el("div"); ui.controls.appendChild(box);
    var cb = U.checkbox(ui.controls, { label: "Reveal the formal charges", testid: "fc-reveal", value: false, onChange: function (v) { st.show = v; draw(); } });
    function build() {
      var f = F.filter(function (x) { return x.key === st.key; })[0];
      box.innerHTML = "";
      if (f.structs.length > 1) U.radios(box, { label: "Structure", testid: "fc-struct", value: "0", options: f.labels.map(function (l, i) { return [String(i), l]; }), onChange: function (v) { st.i = +v; draw(); } });
      st.show = false; cb.checked = false;
      draw();
    }
    function draw() {
      var f = F.filter(function (x) { return x.key === st.key; })[0], s = f.structs[st.i];
      var names = s.atoms.map(function (a, k) {
        var same = s.atoms.filter(function (b) { return b[0] === a[0]; }).length > 1;
        return a[0] + (same ? "<sub>" + (s.atoms.slice(0, k + 1).filter(function (b) { return b[0] === a[0]; }).length) + "</sub>" : "");
      });
      var rows = [["valence e⁻"].concat(s.atoms.map(function (a) { return a[1]; })), ["lone-pair e⁻"].concat(s.atoms.map(function (a) { return a[2] + a[3]; })),
        ["shared e⁻"].concat(s.atoms.map(function (a) { return a[4]; })), ["FC = V − [LP + ½ shared]"].concat(s.atoms.map(function (a) { return st.show ? "<strong>" + fcText(C.fcOf(a)) + "</strong>" : "?"; }))];
      ui.view.innerHTML = "<div class='lw-row'>" + (st.show ? s.svgFC : s.svg) + "</div>" + dataTable(["Step"].concat(names), rows);
      var sum = s.atoms.reduce(function (t, a) { return t + C.fcOf(a); }, 0), verdict = "";
      if (f.structs.length > 1 && st.show) {
        var b = C.fcBest(f.structs, chi), why = ["", "every formal charge is 0 (criterion 1)", "its formal charges are closest to zero (criterion 2)", "it ties on criterion 2, and its negative formal charge sits on the more electronegative atom (criterion 3)"][b.criterion];
        verdict = " Best of the set: <strong>" + f.labels[b.best] + "</strong>, because " + why + "." + (st.key === "SO4" || st.key === "PO4" ? " (The central atom exceeds an octet: allowed for period 3, §4.8. The textbook adds that the real bonding averages both kinds of structure, PDF p.215.)" : st.key === "H3PO4" ? " (Structure 3 gives P ten valence electrons, an expanded octet, and makes every formal charge 0: “An expanded shell produces a structure whose atoms' formal charges are closer to zero” (Day 9 p.29). The Top Hat slide gives no answer; this pick is ours, by the slide's rules.)" : st.key === "N2O" ? " The textbook's reality check: the real N–N bond lies between structures A and B (PDF p.210–211)." : "");
      }
      ui.readout.innerHTML = (st.show ? "Formal charges add up to " + fcText(sum) + (s.charge ? ", the ion's charge." : ", as they must for a neutral molecule.") : "Compute each atom's FC from the table, then check it with “Reveal the formal charges.”") + verdict;
      U.kvSet(ui.kv, [["Species", f.label], ["Structure", f.labels[st.i]], ["Valence electrons", s.total], ["Sum of FC", st.show ? fcText(sum) : "?"]]);
      ui.table.innerHTML = U.tableHTML(["Structure"].concat(["formal charges"]), f.structs.map(function (x, i) { return [f.labels[i], st.show ? x.atoms.map(function (a) { return a[0] + " " + fcText(C.fcOf(a)); }).join(", ") : "revealed with the checkbox"]; }));
    }
    build();
  };

  /* ================================================================ t4-8: exceptions to the octet rule */
  mount.octet = function (host, D) {
    var O = D.octet, st = { id: "NO" };
    var ui = U.shell(host, { title: "Explorer: when the octet rule bends",
      intro: "Pick a species. The bars count the valence electrons around each atom; the line marks the octet (2 for H, which “forms duets,” Day 9 p.27).",
      source: "Source: Day 9 p.27–30: electron-deficient BeCl₂, BCl₃, and AlCl₃; the radicals NO and NO₂; expanded octets in PCl₅, SF₆, and SO₄²⁻ (“hypervalency… is not well understood”). Phosphate and sulfuric acid are textbook §4.8 examples (PDF p.215–216). NH₃ (Day 8 p.23), CH₄, and CO₂ are ordinary octet molecules for comparison." });
    U.select(ui.controls, { label: "Species", testid: "oct-species", value: st.id, options: O.map(function (o) { return [o.id, o.name.replace(/ \(.*\)$/, "")]; }), onChange: function (v) { st.id = v; draw(); } });
    function draw() {
      var o = O.filter(function (x) { return x.id === st.id; })[0], W = 520, H = 230, n = o.atoms.length, bw = Math.min(46, (W - 80) / n - 8);
      var f = U.frame({ w: W, h: H, x0: 0, x1: n, y0: 0, y1: 13, ylabel: "electrons around the atom", yticks: [[0, "0"], [2, "2"], [4, "4"], [6, "6"], [8, "8"], [10, "10"], [12, "12"]], m: { l: 56, r: 16, t: 14, b: 34 } });
      var g = "<line x1='" + f.m.l + "' x2='" + (f.m.l + f.pw) + "' y1='" + f.ys(8).toFixed(1) + "' y2='" + f.ys(8).toFixed(1) + "' style='stroke:#17212E;stroke-width:1.5;stroke-dasharray:6 4'/>" +
        "<text class='direct-label' x='" + (f.m.l + 4) + "' y='" + (f.ys(8) - 6).toFixed(1) + "'>octet</text>";
      var cats = [];
      o.atoms.forEach(function (a, k) {
        var e = a[6], goal = a[0] === "H" ? 2 : 8, x = f.xs(k + 0.5) - bw / 2, kind = e < goal ? "short" : e > goal ? "over" : "ok";
        var col = kind === "short" ? "#B42318" : kind === "over" ? "#5B3FA8" : "#0F7B4B";
        if (kind !== "ok") cats.push(a[0] + " has " + e);
        g += "<g><title>" + a[0] + ": " + e + " electrons</title><rect x='" + x.toFixed(1) + "' y='" + f.ys(e).toFixed(1) + "' width='" + bw.toFixed(1) + "' height='" + (f.ys(0) - f.ys(e)).toFixed(1) + "' rx='3' style='fill:" + col + "'/>" +
          "<text class='direct-label' x='" + (x + bw / 2).toFixed(1) + "' y='" + (f.ys(e) - 5).toFixed(1) + "' text-anchor='middle'>" + e + (kind === "short" ? " ▼" : kind === "over" ? " ▲" : "") + "</text>" +
          "<text class='tick' x='" + (x + bw / 2).toFixed(1) + "' y='" + (f.ys(0) + 16).toFixed(1) + "' text-anchor='middle'>" + a[0] + "</text></g>";
      });
      var odd = o.total % 2 === 1, central = o.central.length ? o.atoms[o.central[0]] : o.atoms[0], cz = central[6];
      var verdict = odd ? "Odd electron count (" + o.total + "): one electron must stay unpaired, so this is a <strong>free radical</strong> (Day 9 p.28). The less electronegative atom takes the incomplete octet (textbook PDF p.212–214)."
        : cz < 8 && central[0] !== "H" ? "<strong>Electron-deficient</strong>: " + central[0] + " has only " + cz + " valence electrons. “Be, B, and Al form electron-deficient molecules” (Day 9 p.27; textbook PDF p.212)."
          : cz > 8 ? "<strong>More than an octet</strong>: " + central[0] + " (period 3) holds " + cz + ": an expanded octet, possible for nonmetals “in the third row and below”, with F, O, or Cl partners, and when it brings formal charges closer to zero (Day 9 p.29; the textbook's Z &gt; 12 rule, PDF p.214)."
            : "Every atom has its octet (H: 2). No exception here.";
      ui.view.innerHTML = "<div class='lw-row'>" + o.svg + "</div>" + U.svgWrap(W, H, "Electrons around each atom in " + o.name + ": " + o.atoms.map(function (a) { return a[0] + " " + a[6]; }).join(", "), f.axes + g) +
        "<p class='xp-caption'>Green: exactly 8 (2 for H). Red with ▼: fewer. Purple with ▲: more.</p>";
      ui.readout.innerHTML = verdict;
      U.kvSet(ui.kv, [["Valence electrons", o.total + (odd ? " (odd)" : " (even)")], ["Central atom", central[0] + ", " + cz + " electrons"], ["Exceptions", cats.length ? cats.join("; ") : "none"]]);
      ui.table.innerHTML = U.tableHTML(["Species", "Valence e⁻", "Central atom's electrons"], O.map(function (x) { var c = x.central.length ? x.atoms[x.central[0]] : x.atoms[0]; return [x.formula, x.total, c[0] + " " + c[6]]; }));
    }
    draw();
  };

  /* ================================================================ t4-9: vibrating bonds */
  mount.vibrations = function (host) {
    var st = { mol: "CO2", mode: "sym", phase: 0, playing: !U.reduceMotion };
    var MODES = { sym: "symmetric stretch", asym: "asymmetric stretch", bend: "bend", stretch: "stretch" };
    var ui = U.shell(host, { title: "Explorer: which vibrations can absorb infrared light?",
      intro: "Watch a vibration and the molecule's net charge separation. If the separation swings back and forth, the vibration can absorb IR at its frequency.",
      source: "Source: textbook preview, §4.9 (PDF p.217–218, Fig. 4.13). The moving picture and the charge-separation trace are a simplified point-charge illustration (background), in arbitrary units." });
    var molSel = U.select(ui.controls, { label: "Molecule", testid: "vib-mol", value: st.mol, options: Object.keys(C.VIB).map(function (k) { return [k, C.VIB[k].label]; }), onChange: function (v) { st.mol = v; st.mode = C.VIB[v].modes[0]; buildModes(); draw(); } });
    var modeBox = el("div"); ui.controls.appendChild(modeBox);
    var row = el("div", { class: "ctl-row" }); ui.controls.appendChild(row);
    var play = U.button(row, st.playing ? "Pause" : "Play", "btn-vib-play", function () { st.playing = !st.playing; play.textContent = st.playing ? "Pause" : "Play"; if (st.playing) loop(); });
    var sl = U.slider(ui.controls, { label: "Moment in the vibration", testid: "vib-phase", min: 0, max: 360, step: 5, value: 0, format: function (v) { return v + "°"; }, onInput: function (v) { st.phase = v * Math.PI / 180; st.playing = false; play.textContent = "Play"; draw(); } });
    function buildModes() {
      modeBox.innerHTML = "";
      var m = C.VIB[st.mol].modes;
      if (m.length > 1) U.radios(modeBox, { label: "Vibration", testid: "vib-mode", value: st.mode, options: m.map(function (k) { return [k, MODES[k]]; }), onChange: function (v) { st.mode = v; draw(); } });
      else modeBox.appendChild(el("p", { class: "xp-caption" }, "A two-atom molecule has one vibration: a stretch."));
    }
    var W = 520, H = 250;
    function draw(frameOnly) {
      var v = C.vib(st.mol, st.mode, st.phase), swing = C.vibSwing(st.mol, st.mode), active = swing > 1e-9;
      var cx = W / 2, cy = 88, sc = 120, g = "";
      var R = { O: 17, C: 15, N: 16, H: 10, Cl: 20 }, COL = { O: "#B42318", C: "#3A3F47", N: "#2F5DB8", H: "#E8E8E8", Cl: "#0F7B4B" };
      for (var i = 0; i + 1 < v.atoms.length; i++) {
        var a = v.atoms[i], b = v.atoms[i + 1];
        g += "<line x1='" + (cx + a.x * sc).toFixed(1) + "' y1='" + (cy - a.y * sc).toFixed(1) + "' x2='" + (cx + b.x * sc).toFixed(1) + "' y2='" + (cy - b.y * sc).toFixed(1) + "' style='stroke:#6B7686;stroke-width:5'/>";
      }
      v.atoms.forEach(function (a) {
        var x = cx + a.x * sc, y = cy - a.y * sc;
        g += "<circle cx='" + x.toFixed(1) + "' cy='" + y.toFixed(1) + "' r='" + R[a.el] + "' style='fill:" + COL[a.el] + ";stroke:#17212E;stroke-width:1'/>" +
          "<text x='" + x.toFixed(1) + "' y='" + (y + 5).toFixed(1) + "' text-anchor='middle' style='fill:" + (a.el === "H" ? "#17212E" : "#FFFFFF") + ";font-family:var(--sans);font-size:13px;font-weight:600'>" + a.el + "</text>" +
          (a.q ? "<text x='" + x.toFixed(1) + "' y='" + (y - R[a.el] - 6).toFixed(1) + "' text-anchor='middle' class='direct-label'>" + (a.q > 0 ? "δ+" : "δ−") + "</text>" : "");
      });
      // trace of the dipole component along the vibration over one period
      var comp = st.mol === "CO2" && st.mode === "bend" ? "y" : "x", base = C.vib(st.mol, st.mode, 0).dipole[comp];
      var tx0 = 60, tx1 = W - 20, ty = 200, amp = 34, pts = [];
      for (var k = 0; k <= 72; k++) { var ph = k / 72 * 2 * Math.PI, d = C.vib(st.mol, st.mode, ph).dipole[comp] - base; pts.push([tx0 + (tx1 - tx0) * k / 72, ty - (swing ? d / Math.max(swing, 1e-9) * amp * Math.min(1, swing / 0.3) : 0)]); }
      var cur = ((st.phase % (2 * Math.PI)) + 2 * Math.PI) % (2 * Math.PI), dc = C.vib(st.mol, st.mode, cur).dipole[comp] - base;
      var mx = tx0 + (tx1 - tx0) * cur / (2 * Math.PI), my = ty - (swing ? dc / Math.max(swing, 1e-9) * amp * Math.min(1, swing / 0.3) : 0);
      g += "<line x1='" + tx0 + "' x2='" + tx1 + "' y1='" + ty + "' y2='" + ty + "' class='baseline'/>" +
        "<text class='axis-label' x='" + tx0 + "' y='" + (ty - amp - 10) + "'>change in net charge separation</text>" +
        "<path d='" + U.linePath(pts) + "' style='fill:none;stroke:" + (active ? U.SERIES[0] : "#6B7686") + ";stroke-width:2'/>" +
        "<circle cx='" + mx.toFixed(1) + "' cy='" + my.toFixed(1) + "' r='5' style='fill:" + U.SERIES[1] + "'/>";
      ui.view.innerHTML = U.svgWrap(W, H, C.VIB[st.mol].label + " " + MODES[st.mode] + ": " + (active ? "the charge separation oscillates (infrared-active)" : "no net change in charge separation (infrared-inactive)"), g);
      var why = active ? (st.mol === "CO2" ? (st.mode === "asym" ? "One C=O bond shortens as the other lengthens, so the changes don't cancel (Fig. 4.13b)." : "Bending moves the O atoms off the line, so the charge separation swings up and down (Fig. 4.13c).") : "One polar bond: stretching changes its charge separation, and there's nothing to cancel it.")
        : (st.mol === "CO2" ? "The two C=O bonds stretch together, and their equal and opposite changes cancel (Fig. 4.13a)." : "Two identical atoms: the bond is nonpolar, so stretching it changes nothing electrical (textbook Concept Test, PDF p.218).");
      if (frameOnly) return;                              // animation frames leave the aria-live readout alone
      ui.readout.innerHTML = "<strong>" + (active ? "Infrared-active" : "Infrared-inactive") + ".</strong> " + why;
      U.kvSet(ui.kv, [["Molecule", C.VIB[st.mol].label], ["Vibration", MODES[st.mode]], ["Net charge separation", active ? "oscillates" : "stays the same"]]);
      ui.table.innerHTML = U.tableHTML(["Molecule", "Vibration", "IR-active?"], [].concat.apply([], Object.keys(C.VIB).map(function (k) { return C.VIB[k].modes.map(function (m) { return [C.VIB[k].label, MODES[m], C.vibSwing(k, m) > 1e-9 ? "yes" : "no"]; }); })));
    }
    var last = null, raf = null;
    function loop(t) {
      if (!st.playing) { last = null; return; }
      if (host.offsetParent !== null) {
        if (last !== null && t) { st.phase = (st.phase + (t - last) / 1000 * 2 * Math.PI * 0.6) % (2 * Math.PI); sl.set(Math.round(st.phase * 180 / Math.PI / 5) * 5); }
        draw(true);
      }
      last = t || null;
      raf = window.requestAnimationFrame(loop);
    }
    buildModes();
    draw();
    if (st.playing) loop();
  };

  X.calcCh4 = C;
  return { calc: C };
});

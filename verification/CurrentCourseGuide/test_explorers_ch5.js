// Node tests: Chapter 5 explorer calculations (assets/explorers_ch5.js) against the independent Python reference
// values in ch5_data.py (written to expected_values.json by build_guide.py)
//   node verification/CurrentCourseGuide/test_explorers_ch5.js
// Before a full build, CH5_DATA and CH5_EXPECTED may point to JSON dumps of ch5_data.build() and expected().
"use strict";
const path = require("path");
const fs = require("fs");
const CX = require(path.join(__dirname, "../../study-guides/CurrentCourseGuide/assets/explorers_ch5.js"));
const C = CX.calc;
let D, EXP;
if (process.env.CH5_DATA) {
  D = JSON.parse(fs.readFileSync(process.env.CH5_DATA, "utf8"));
  EXP = JSON.parse(fs.readFileSync(process.env.CH5_EXPECTED, "utf8"));
} else {
  const sandbox = {};
  new Function("window", fs.readFileSync(path.join(__dirname, "../../study-guides/CurrentCourseGuide/assets/data.js"), "utf8"))(sandbox);
  D = sandbox.GUIDE_DATA;
  EXP = JSON.parse(fs.readFileSync(path.join(__dirname, "expected_values.json"), "utf8"));
}
const G = D.ch5, E = EXP.ch5;
let pass = 0, fail = 0; const bad = [];
function ok(c, name, detail) { if (c) pass++; else { fail++; bad.push(name + (detail !== undefined ? " -> " + detail : "")); } }
function same(a, b) { return JSON.stringify(a) === JSON.stringify(b); }

// ---- VSEPR: every SN / lone-pair combination and both "not observed" variants, JS frames vs. the Python polyhedra
Object.keys(E.vsepr).forEach(function (k) {
  const [sn, nlp, variant] = k.split("-"), want = E.vsepr[k];
  const got = C.shapeInfo(+sn, +nlp, { axial: variant === "axial", adjacent: variant === "adjacent" });
  ok(same(got.angles, want.angles), "VSEPR " + k + " bond angles", JSON.stringify(got.angles) + " vs " + JSON.stringify(want.angles));
  ok(same(got.contacts, want.contacts), "VSEPR " + k + " 90° contacts", JSON.stringify(got.contacts) + " vs " + JSON.stringify(want.contacts));
  ok(same(got.lpSites, want.lpSites), "VSEPR " + k + " lone-pair sites", JSON.stringify(got.lpSites) + " vs " + JSON.stringify(want.lpSites));
  ok(got.epg === want.epg, "VSEPR " + k + " electron-pair geometry", got.epg);
  if (variant === "pref") ok(got.mg === want.mg && got.observed, "VSEPR " + k + " molecular geometry", got.mg + " vs " + want.mg);
  else ok(!got.observed && got.mg === null, "VSEPR " + k + " marked not observed");
});
// every explorer name matches the data file's table, and the professor's table rows agree with it
Object.keys(G.vsepr.mg).forEach(function (k) { ok(C.MG[k] === G.vsepr.mg[k], "name for " + k); });
G.vsepr.profTable.forEach(function (r) {
  ok(C.MG[r[0] + "-" + r[2]].replace(" (angular)", "").toLowerCase() === r[3].toLowerCase().replace("see-saw", "seesaw"), "Day 10 p.26 row " + r.slice(0, 4).join(" "));
});
// stated angles: the presets draw the angle they cite
G.vsepr.presets.forEach(function (p) {
  ok(p.ligands.length + p.lp === p.sn, "preset " + p.key + " counts SN = atoms + lone pairs");
  if (!p.angle) return;
  const info = C.shapeInfo(p.sn, p.lp, { angle: p.angle }), d = info.domains, atoms = d.dirs.filter(function (_, i) { return !d.lp[i]; });
  let hit = false;
  for (let i = 0; i < atoms.length; i++) for (let j = i + 1; j < atoms.length; j++) if (Math.abs(C.angle(atoms[i], atoms[j]) - p.angle) < 1e-6) hit = true;
  ok(hit, "preset " + p.key + " is drawn with its " + p.angle + "° angle");
});
ok(Math.abs(C.angle(C.domains(4, 0).dirs[0], C.domains(4, 0).dirs[1]) - 109.4712) < 1e-3, "tetrahedral angle 109.47°");

// ---- polarity: Δχ-weighted vector sums, JS vs. numpy
G.dipoles.forEach(function (m) {
  const got = C.dipole(m, G.chi), want = E.dipoles[m.key];
  ok(Math.abs(got.mag - want.mag) < 1e-3, "dipole sum " + m.key, got.mag.toFixed(4) + " vs " + want.mag);
  ok(got.polar === want.polar && got.unknown === want.unknown, "polar verdict " + m.key, got.polar + "/" + got.unknown);
});
const T52 = { HF: 1.82, H2O: 1.85, NH3: 1.47, CHCl3: 1.01, CCl3F: 0.45 };
Object.keys(T52).forEach(function (k) {
  const m = G.dipoles.filter(function (x) { return x.key === k; })[0];
  ok(m && m.mu === T52[k] && /Table 5\.2/.test(m.muSrc), "Table 5.2 value for " + k + " (Day 11 p.8)");
});
ok(["CO2", "CF4", "BF3", "CCl4", "PCl5", "XeF4"].every(function (k) { return !C.dipole(G.dipoles.filter(function (x) { return x.key === k; })[0], G.chi).polar; }), "symmetric molecules are nonpolar");
// the caveat the explorer states: Δχ arrows rank CCl3F above CHCl3, the measured moments the other way
(function () {
  const a = C.dipole(G.dipoles.filter(function (x) { return x.key === "CHCl3"; })[0], G.chi).mag, b = C.dipole(G.dipoles.filter(function (x) { return x.key === "CCl3F"; })[0], G.chi).mag;
  ok(b > a, "Δχ model ranks CCl3F (" + b.toFixed(2) + ") above CHCl3 (" + a.toFixed(2) + "), opposite to Table 5.2 (the stated caveat)");
})();
ok(Math.abs(G.chi.O - G.chi.C - 1.0) < 1e-9 && Math.abs(G.chi.F - G.chi.C - 1.5) < 1e-9 && Math.abs(G.chi.O - G.chi.H - 1.4) < 1e-9, "the slides' Δχ values 1.0, 1.5, 1.4 (Day 10 p.29–31)");

// ---- hybrid orbitals: box occupancies, JS vs. Python, and electron conservation
G.hybrid.forEach(function (h) {
  const got = C.hybridize(h), want = E.hybrid[h.key];
  ok(got.hyb === want.hyb, "hybridization " + h.key, got.hyb + " vs " + want.hyb);
  ok(same(got.ground, want.ground) && same(got.hybrids, want.hybrids) && same(got.unhybridized, want.unhybridized), "boxes " + h.key,
    JSON.stringify([got.ground, got.hybrids, got.unhybridized]) + " vs " + JSON.stringify([want.ground, want.hybrids, want.unhybridized]));
  ok(got.unpairedGround === want.unpairedGround, "unpaired in ground state " + h.key);
  const total = function (a) { return a.reduce(function (s, x) { return s + x; }, 0); };
  ok(total(got.ground) === total(got.hybrids) + total(got.unhybridized), "electrons conserved " + h.key);
  ok(got.hybrids.length === h.sn && got.unhybridized.length === 4 - h.sn, "one hybrid per electron domain " + h.key);
});
const lect = { "C-CH4": [[1, 1, 1, 1], []], "N-NH3": [[2, 1, 1, 1], []], "O-H2O": [[2, 2, 1, 1], []], "C-CH2O": [[1, 1, 1], [1]], "O-CH2O": [[2, 2, 1], [1]], "N-N2H2": [[2, 1, 1], [1]], "C-C2H2": [[1, 1], [1, 1]] };
Object.keys(lect).forEach(function (k) {
  const h = G.hybrid.filter(function (x) { return x.key === k; })[0], got = C.hybridize(h);
  ok(same([got.hybrids, got.unhybridized], lect[k]), "boxes as drawn on the slides for " + k + " (Day 11 p.13–23)");
});

// ---- σ and π counts
G.sigmaPi.forEach(function (s) {
  const got = C.sigmaPi(s.bonds), want = E.sigmaPi[s.key];
  ok(got.sigma === want.sigma && got.pi === want.pi, "σ/π " + s.key, got.sigma + "/" + got.pi + " vs " + want.sigma + "/" + want.pi);
  ok((s.colored.match(/lw-sigma/g) || []).length === got.sigma && (s.colored.match(/lw-pi/g) || []).length === got.pi, "colored drawing has one σ line per bond and one line per π bond: " + s.key);
});

// ---- chirality: chiral exactly when the four groups differ; the BFS reaches all 12 rotations
G.chirality.presets.forEach(function (p) {
  const want = E.chirality[p.key];
  ok(C.superimposable(p.groups) === want.superimposable, "superimposable " + p.key);
  ok(C.chiral(p.groups) === want.fourDifferent && C.chiral(p.groups) === !want.superimposable, "chiral verdict " + p.key);
});
C.superimposable(["a", "b", "c", "d"]);
ok(C._lastOrbit === 12, "the turns generate all 12 rotations of a tetrahedron", C._lastOrbit);
(function () {            // a turn about a bond keeps every group on a corner of the tetrahedron
  const m = C.TETRA.map(C.mirror), t = m.map(function (v) { return C.rotateAbout(v, m[0], 120); });
  ok(t.every(function (v) { return Math.min.apply(null, C.TETRA.map(function (p) { return Math.hypot(v[0] - p[0], v[1] - p[1], v[2] - p[2]); })) < 1e-9; }), "120° turns map corners to corners");
  const g = ["H", "Br", "Br", "Cl"], turned = m.map(function (v) { return C.rotateAbout(v, m[0], 120); });
  ok(C.matchCount(g, turned) === 4 || C.matchCount(g, turned.map(function (v) { return C.rotateAbout(v, m[0], 120); })) === 4, "CHBr2Cl: turning the mirror image about the C–H bond superimposes it (textbook Fig. 5.40)");
})();

// ---- MO diagrams: every species and allowed charge, JS vs. Python
G.mo.species.forEach(function (sp) {
  const qs = C.moCharges(sp, G.mo.orders), keys = Object.keys(E.mo).filter(function (k) { return k.split(":")[0] === sp.key; }).map(function (k) { return +k.split(":")[1]; }).sort(function (a, b) { return a - b; });
  ok(same(qs, keys), "allowed charges for " + sp.key, JSON.stringify(qs) + " vs " + JSON.stringify(keys));
  qs.forEach(function (q) {
    const got = C.moFill(G.mo.orders, sp.order, sp.valence[0] + sp.valence[1] - q), want = E.mo[sp.key + ":" + q];
    ok(got.bo === want.bo && got.unpaired === want.unpaired && got.config === want.config && same(got.levels.map(function (L) { return L.boxes; }), want.boxes),
      "MO " + sp.key + " charge " + q, JSON.stringify([got.bo, got.unpaired, got.config]) + " vs " + JSON.stringify([want.bo, want.unpaired, want.config]));
  });
});
(function () {
  const f = C.moFill(G.mo.orders, "high", 12);
  ok(f.bo === 2 && f.unpaired === 2, "O2: bond order 2 and two unpaired electrons, the Day 11 p.27 paramagnetism");
  ok(C.configHTML(f) === "(σ<sub>2s</sub>)<sup>2</sup>(σ*<sub>2s</sub>)<sup>2</sup>(σ<sub>2p</sub>)<sup>2</sup>(π<sub>2p</sub>)<sup>4</sup>(π*<sub>2p</sub>)<sup>2</sup>", "O2 configuration in the textbook's notation");
  ok(C.moFill(G.mo.orders, "low", 10).config === "(σ2s)2(σ*2s)2(π2p)4(σ2p)2", "N2 uses the Z ≤ 7 order (Fig. 5.49a)");
  ok(C.boText(2.5) === "2.5" && C.boText(3) === "3" && C.boText(0.5) === "0.5", "bond order text");
})();

// ---- explorers leave out their module's attempt and transfer species (the rule kept since the Ch. 4 build):
// no preset's formula may appear in the prompt of that module's attempt or transfer problem
if (D.problems) {
  const strip = function (h) { return String(h).replace(/<[^>]+>/g, "").replace(/[₀-₉]/g, function (c) { return String(c.charCodeAt(0) - 0x2080); }); };
  const presetFormulas = {
    m20: G.vsepr.presets.filter(function (p) { return p.mode !== "lone"; }).map(function (p) { return strip(p.html); }),
    m21: G.vsepr.presets.filter(function (p) { return p.mode !== "bonds"; }).map(function (p) { return strip(p.html); }),
    m22: G.dipoles.map(function (m) { return strip(m.html); }),
    m23: G.hybrid.map(function (h) { return strip(h.molecule); }),
    m24: G.sigmaPi.map(function (s) { return strip(s.html); }),
    "t5-6": G.chirality.presets.map(function (p) { return strip(p.label); }),
    "t5-7": ["O2", "N2", "B2", "He2", "NO"]   // the MO explorer's preset buttons (O₂²⁻ too, checked below)
  };
  // reviewed passing mentions: the formula is named for comparison, but the problem is about another species
  const REVIEWED_MENTIONS = {
    "m23-attempt": ["NH3", "H2O"],      // "Day 11 p.16 builds NH3 and H2O… Do the same for H3O+"
    "t5-7-attempt": ["NO", "O2"],       // the prompt cites NO (textbook) and O2–Ne2 (Day 12 p.11) only to name the MO order for NF
    "t5-7-transfer": ["NO"]             // "CN− is a heteronuclear diatomic like NO"
  };
  Object.keys(presetFormulas).forEach(function (mid) {
    D.problems.filter(function (p) { return p.module === mid && (p.kind === "attempt" || p.kind === "transfer"); }).forEach(function (p) {
      const text = strip(p.prompt);
      const hit = presetFormulas[mid].filter(function (f) {
        if ((REVIEWED_MENTIONS[p.id] || []).indexOf(f) >= 0) return false;
        // whole-formula match: not followed by another digit, letter, or charge (so "NO" doesn't match "NO2" or "NO+")
        return new RegExp("(^|[^A-Za-z0-9])" + f.replace(/[.*+?^${}()|[\]\\]/g, "\\$&") + "(?![A-Za-z0-9+−-])").test(text);
      });
      ok(!hit.length, mid + " " + p.kind + " (" + p.id + ") uses no " + mid + " explorer preset", hit.join(", "));
    });
  });
}

// ---- the scene renderer makes well-formed markup for every preset (no NaN, balanced tags)
(function () {
  let nan = 0, unbalanced = 0;
  G.vsepr.presets.forEach(function (p) {
    const d = C.domains(p.sn, p.lp, { angle: p.angle }), atoms = [{ p: [0, 0, 0], el: p.center }], bonds = [], lobes = [];
    let li = 0;
    d.dirs.forEach(function (v, i) { if (d.lp[i]) lobes.push({ at: [0, 0, 0], dir: v, len: 0.95, dots: 2 }); else { atoms.push({ p: v, el: p.ligands[li] }); bonds.push({ a: [0, 0, 0], b: v, order: p.orders[li] }); li++; } });
    [[0, 0], [25, 15], [90, 90], [-180, -90]].forEach(function (yp) {
      const svg = C.scene({ s: 100, cx: 260, cy: 160, yaw: yp[0], pitch: yp[1], atoms: atoms, bonds: bonds, lobes: lobes, arcs: [{ c: [0, 0, 0], u: atoms[1].p, v: atoms[atoms.length - 1].p, label: "x" }] });
      if (/NaN|undefined/.test(svg)) nan++;
      if ((svg.match(/<g/g) || []).length !== (svg.match(/<\/g>/g) || []).length) unbalanced++;
    });
  });
  ok(nan === 0, "no NaN or undefined in any 3-D drawing", nan);
  ok(unbalanced === 0, "balanced groups in every 3-D drawing", unbalanced);
})();

console.log("explorers_ch5: " + pass + " passed, " + fail + " failed");
if (fail) { bad.forEach(function (b) { console.log("  FAIL " + b); }); process.exit(1); }

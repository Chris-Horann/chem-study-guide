// Node tests: Chapter 4 explorer calculations (assets/explorers_ch4.js) against Python reference values
//   node verification/CurrentCourseGuide/test_explorers_ch4.js
"use strict";
const path = require("path");
const fs = require("fs");
const CX = require(path.join(__dirname, "../../study-guides/CurrentCourseGuide/assets/explorers_ch4.js"));
const C = CX.calc;
const sandbox = {};
new Function("window", fs.readFileSync(path.join(__dirname, "../../study-guides/CurrentCourseGuide/assets/data.js"), "utf8"))(sandbox);
const D = sandbox.GUIDE_DATA;
const EXP = JSON.parse(fs.readFileSync(path.join(__dirname, "expected_values.json"), "utf8"));
let pass = 0, fail = 0; const bad = [];
function ok(c, name, detail) { if (c) pass++; else { fail++; bad.push(name + (detail !== undefined ? " -> " + detail : "")); } }

// ---- ionic names and formulas: every cation × anion pair, JS vs. the independent Python implementation
const N = D.naming, cat = {}, an = {};
N.cations.forEach(function (c) { cat[c.key] = c; });
N.anions.forEach(function (a) { an[a.key] = a; });
let ionBad = 0;
EXP.naming.ionic.forEach(function (r) {
  const got = C.ionic(cat[r[0]], an[r[1]]);
  if (got.formula !== r[2] || got.name !== r[3] || got.nc !== r[4] || got.na !== r[5]) { ionBad++; if (ionBad < 5) bad.push("ionic " + r[0] + "+" + r[1] + ": " + JSON.stringify(got) + " vs " + r.slice(2)); }
});
ok(ionBad === 0, "ionic formula and name for all " + EXP.naming.ionic.length + " cation/anion pairs match Python", ionBad + " mismatches");
ok(C.spaced("copper(II) oxide") === "copper (II) oxide", "slide spacing variant");
ok(C.fHTML("(NH4)2SO4") === "(NH<sub>4</sub>)<sub>2</sub>SO<sub>4</sub>", "formula HTML with parentheses");

// ---- covalent names: JS vs. Python over every allowed element pair, counts, and both vowel rules
let covBad = 0;
const first = {}, second = {};
N.covFirst.forEach(function (x) { first[x[0]] = x; });
N.covSecond.forEach(function (x) { second[x[0]] = x; });
EXP.naming.covalent.forEach(function (r) {
  const got = C.covalent(first[r[0]], r[1], second[r[2]], r[3], r[4], N.prefixes);
  if (got.formula !== r[5] || got.name !== r[6]) { covBad++; if (covBad < 5) bad.push("covalent " + r.slice(0, 5) + ": " + JSON.stringify(got) + " vs " + r.slice(5)); }
  if (!C.covOrderOK(r[0], r[2], N.covOrder)) covBad++;
});
ok(covBad === 0, "covalent formula and name for all " + EXP.naming.covalent.length + " cases match Python", covBad + " mismatches");
ok(C.covalent(first.S, 2, second.F, 2, false, N.prefixes).name === "disulfur difluoride", "S2F2 (Day 8 p.13)");
ok(C.covalent(first.N, 2, second.O, 4, true, N.prefixes).name === "dinitrogen tetroxide", "N2O4 with the textbook vowel rule (Sample Ex. 4.3)");
ok(!C.covOrderOK("O", "Cl", N.covOrder) && C.covOrderOK("Cl", "O", N.covOrder) && C.covOrderOK("O", "F", N.covOrder), "element order: Cl2O, OF2");

// ---- acids: formula H count matches the anion charge; -ate → -ic, -ite → -ous, binary → hydro-…-ic
N.acids.forEach(function (x) {
  const a = an[x.anion], hCount = (x.f.match(/^H(\d*)/) || [])[1];
  ok((hCount ? +hCount : 1) === -a.q, "acid " + x.f + " has " + (-a.q) + " H");
  const rule = x.kind === "binary" ? /^hydro.*ic acid$/.test(x.name) : /ate$/.test(a.name) ? /ic acid$/.test(x.name) && !/^hydro/.test(x.name) : /ous acid$/.test(x.name);
  ok(rule, "acid naming rule for " + a.name + " → " + x.name);
});
ok(!N.acids.some(function (x) { return x.anion === "I"; }), "HI(aq) (the t4-3 attempt) is not in the explorer");

// ---- formal charges: JS recomputation matches lewis.py; each FC set sums to its charge; the criteria pick the textbook's choice
function allStructs() {
  const out = [];
  D.fcSets.forEach(function (f) { f.structs.forEach(function (s) { out.push(s); }); });
  D.octet.forEach(function (s) { out.push(s); });
  D.resonance.forEach(function (r) { r.structs.forEach(function (s) { out.push(s); }); });
  return out;
}
let fcBad = 0;
allStructs().forEach(function (s) {
  s.atoms.forEach(function (a) { if (C.fcOf(a) !== a[5]) fcBad++; });
  const sum = s.atoms.reduce(function (t, a) { return t + C.fcOf(a); }, 0);
  if (sum !== s.charge) fcBad++;
  const drawn = s.atoms.reduce(function (t, a) { return t + a[2] + a[3]; }, 0) + s.bonds.reduce(function (t, b) { return t + 2 * b[2]; }, 0);
  if (drawn !== s.total) fcBad++;
});
ok(fcBad === 0, "formal charges, charge sums, and electron totals for every explorer structure", fcBad);
Object.keys(EXP.fcBest).forEach(function (k) {
  const f = D.fcSets.filter(function (x) { return x.key === k; })[0];
  const b = C.fcBest(f.structs, D.chi);
  ok(b.best === EXP.fcBest[k], "best structure for " + k + " = " + f.labels[EXP.fcBest[k]], f.labels[b.best] + " (criterion " + b.criterion + ")");
});
const n2o = C.fcBest(D.fcSets.filter(function (x) { return x.key === "N2O"; })[0].structs, D.chi);
ok(n2o.criterion === 3, "N2O is decided by criterion 3 (textbook PDF p.210)", n2o.criterion);
const co2 = C.fcBest(D.fcSets.filter(function (x) { return x.key === "CO2"; })[0].structs, D.chi);
ok(co2.criterion === 1, "CO2 is decided by criterion 1 (all zero)", co2.criterion);
const hidden = ["CO", "SCN-a", "SCN-b", "SCN-c", "SO3-oct", "SO3-exp", "OH-", "NH4+", "O3a", "BF3"];
const fcAndOctet = [].concat.apply(D.octet.slice(), D.fcSets.map(function (f) { return f.structs; }));
ok(!fcAndOctet.some(function (s) { return hidden.indexOf(s.id) >= 0; }), "attempt/transfer structures (CO, SCN⁻, SO₃²⁻, OH⁻, NH₄⁺, O₃, BF₃) are not in the FC or octet explorers",
   fcAndOctet.filter(function (s) { return hidden.indexOf(s.id) >= 0; }).map(function (s) { return s.id; }).join());

// ---- resonance: average bond orders from the structures themselves
D.resonance.forEach(function (r) {
  const s0 = r.structs[0], pair = r.pair[0].split("–"), n = r.structs.length;
  let pairs = 0, bonds = 0;
  s0.bonds.forEach(function (b, k) {
    const e = [s0.atoms[b[0]][0], s0.atoms[b[1]][0]].sort().join(), want = pair.slice().sort().join();
    if (e === want) { bonds++; r.structs.forEach(function (s) { pairs += s.bonds[k][2] / n; }); }
  });
  ok(Math.abs(pairs / bonds - r.avg) < 1e-6, "average bond order for " + r.key, pairs / bonds + " vs " + r.avg);
  ok(r.single[0] > r.double[0] && r.single[1] < r.double[1], r.key + ": single longer and weaker than double (Table 4.6)");
  if (r.measured) ok(r.measured < r.single[0] && r.measured > r.double[0], r.key + ": measured length between single and double");
});
ok(!D.resonance.some(function (r) { return r.key === "NO2-" || r.key === "HCO2-"; }), "nitrite and formate (t4-5 attempt/transfer) are not in the resonance explorer");

// ---- Table 4.6: 35 bonds; within each atom pair, length falls and energy rises with bond order
ok(D.bondTable.length === 35, "Table 4.6 has 35 rows", D.bondTable.length);
[["C", "C"], ["C", "N"], ["C", "O"], ["N", "N"], ["N", "O"], ["O", "O"], ["S", "O"]].forEach(function (p) {
  const s = C.bondSeries(D.bondTable, p[0], p[1]);
  let mono = s.length >= 2;
  for (let i = 1; i < s.length; i++) if (!(s[i].pm < s[i - 1].pm && s[i].kj > s[i - 1].kj)) mono = false;
  ok(mono, p.join("–") + ": shorter and stronger with bond order", JSON.stringify(s.map(function (r) { return [r.order, r.pm, r.kj]; })));
});

// ---- Lewis symbols: the JS port reproduces lewis.symbol_svg exactly
D.lewisSymbols.forEach(function (x) {
  const r = C.symbolSVG(x.el, x.valence);
  ok(r.svg === x.svg, "Lewis symbol SVG of " + x.el + " matches Python");
  ok(r.unpaired === x.unpaired, "unpaired dots of " + x.el, r.unpaired + " vs " + x.unpaired);
});
ok(C.symbolSVG("C", 4, 2).unpaired === 2 && C.symbolSVG("O", 6, 5).unpaired === 3, "partial builds: dots one per side before pairing");
ok(C.symbolSVG("He", 2).unpaired === 0, "He drawn as one pair");

// ---- five-step frames: electron bookkeeping
Object.keys(D.lewisSteps).forEach(function (k) {
  const s = D.lewisSteps[k], total = s.table.reduce(function (t, r) { return t + r[1] * r[2]; }, 0) - s.charge;
  ok(total === s.total, k + ": step-1 table total = " + s.total, total);
  ok(s.frames.length === 4 && s.frames[3].used === s.total && s.frames[2].used <= s.total, k + ": frames end with all " + s.total + " electrons placed");
  ok(s.frames[3].same === (s.frames[2].short.length === 0), k + ": a multiple-bond step appears exactly when a central atom is short");
});
ok(!("HCN" in D.lewisSteps) && !("C2H4" in D.lewisSteps), "HCN and C2H4 (m19 attempt/transfer) are not in the steps explorer");

// ---- vibrations: which modes change the charge separation
ok(C.vibSwing("CO2", "sym") < 1e-12, "CO2 symmetric stretch: no dipole change (IR-inactive, Fig. 4.13a)");
ok(C.vibSwing("CO2", "asym") > 0.1, "CO2 asymmetric stretch: dipole oscillates (IR-active)");
ok(C.vibSwing("CO2", "bend") > 0.1, "CO2 bend: dipole oscillates (IR-active)");
ok(C.vibSwing("N2", "stretch") < 1e-12 && C.vibSwing("O2", "stretch") < 1e-12, "N2 and O2 stretches: no dipole change");
ok(C.vibSwing("CO", "stretch") > 0.05 && C.vibSwing("HCl", "stretch") > 0.05, "CO and HCl stretches: dipole oscillates");
let comFixed = true;
[0.3, 1.1, 2.0].forEach(function (ph) {
  ["sym", "asym", "bend"].forEach(function (m) {
    const v = C.vib("CO2", m, ph), masses = [16, 12, 16];
    const cx = v.atoms.reduce(function (t, a, i) { return t + masses[i] * a.x; }, 0), cy = v.atoms.reduce(function (t, a, i) { return t + masses[i] * a.y; }, 0);
    if (Math.abs(cx) > 1e-9 || Math.abs(cy) > 1e-9) comFixed = false;
  });
});
ok(comFixed, "CO2 vibrations keep the centre of mass fixed");
ok(C.boText(4 / 3) === "1.33" && C.boText(1.5) === "1.5" && C.boText(2) === "2", "bond-order formatting");

console.log(`Ch. 4 explorer tests: ${pass} passed, ${fail} failed`);
if (fail) { console.log(bad.map(function (x) { return "  FAIL " + x; }).join("\n")); process.exit(1); }

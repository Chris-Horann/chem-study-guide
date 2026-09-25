// Node tests: explorer physics (assets/explorers.js calc) vs. Python reference values (expected_values.json)
//   node verification/CurrentCourseGuide/test_explorers.js
"use strict";
const path = require("path");
const fs = require("fs");
const X = require(path.join(__dirname, "../../study-guides/CurrentCourseGuide/assets/explorers.js"));
const exp = JSON.parse(fs.readFileSync(path.join(__dirname, "expected_values.json"), "utf8"));
// load GUIDE_DATA from data.js without a browser
const dataSrc = fs.readFileSync(path.join(__dirname, "../../study-guides/CurrentCourseGuide/assets/data.js"), "utf8");
const sandbox = {};
new Function("window", dataSrc)(sandbox);
const D = sandbox.GUIDE_DATA;
X.useData(D);
const c = X.calc;

let pass = 0, fail = 0; const bad = [];
function ok(cond, name, detail) { if (cond) pass++; else { fail++; bad.push(name + (detail ? " -> " + detail : "")); } }
function rel(a, b) { return Math.abs(a - b) / Math.max(Math.abs(b), 1e-300); }

exp.bohr.forEach(function (t) {
  const dE = c.bohrDE(t.ni, t.nf), nm = c.nmFromE(Math.abs(dE));
  ok(rel(dE, t.dE) < 1e-12, "bohrDE " + t.ni + "->" + t.nf, dE + " vs " + t.dE);
  ok(rel(nm, t.nm) < 1e-12, "bohr nm " + t.ni + "->" + t.nf, nm + " vs " + t.nm);
});
ok(c.bohrDE(1, Infinity) === 2.178e-18, "ionization from n = 1 is +2.178e-18 J");
exp.photon.forEach(function (t) {
  const r = c.photonFromNm(t.nm);
  ok(rel(r.E, t.E) < 1e-12 && rel(r.nu, t.nu) < 1e-12, "photon " + t.nm + " nm");
});
exp.debroglie.forEach(function (t) { ok(rel(c.deBroglie(t.m, t.u), t.lam) < 1e-12, "de Broglie m=" + t.m); });
exp.eel.forEach(function (t) { ok(rel(c.eel(t.q1, t.q2, t.d), t.E) < 1e-12, "E_el " + t.q1 + "/" + t.q2 + " d=" + t.d); });
exp.photoelectric.forEach(function (t) { ok(rel(c.photonFromNm(t.nm).E - t.phi, t.KE) < 1e-12, "photoelectric KE"); });

// Planck: the closed-form peak equals the brute-force maximum and Wien's constant
const pk = c.planckPeakNm(5000), num = c.planckPeakNumeric(5000);
ok(Math.abs(pk - num) < 0.5, "Planck peak closed form vs numeric at 5000 K", pk + " vs " + num);
ok(rel(pk, exp.planckPeakNm5000) < 0.002, "Planck peak vs Wien 2.8978e-3 m K / T", pk + " vs " + exp.planckPeakNm5000);
ok(pk > 570 && pk < 590, "5000 K peak ≈ 580 nm (Day 3 p.14 plots ≈ 0.58 μm)", pk);
ok(c.planck(1e-6, 6000) > c.planck(1e-6, 3000), "hotter is brighter at 1 μm");
ok(c.rayleighJeans(2e-7, 5000) > 10 * c.planck(2e-7, 5000), "classical curve diverges at short wavelength");

// Balmer lines
[[3, 656.2], [4, 486.1], [5, 434.0], [6, 410.1], [7, 397.0], [8, 388.9]].forEach(function (x) {
  ok(Math.abs(c.balmerNm(x[0]) - x[1]) < 0.06, "Balmer n=" + x[0], c.balmerNm(x[0]));
});
// regions and colors
ok(c.region(530e-9) === "visible" && c.colorName(530) === "green", "530 nm is visible green");
ok(c.region(250e-9) === "ultraviolet", "250 nm UV");
ok(c.region(1e-10) === "X-rays", "0.1 nm X-ray");
ok(c.region(2.998e8 / 2.45e9) === "microwave", "2.45 GHz microwave");
ok(c.region(2.998e8 / 98.5e6) === "radio", "98.5 MHz radio");
ok(c.region(1876e-9) === "infrared", "4->3 line infrared");
ok(c.seriesName(1) === "Lyman" && c.seriesName(2) === "Balmer" && c.seriesName(3) === "Paschen", "series names");

// configurations in data.js agree with the Python reference; unpaired counts agree
Object.keys(exp.configs).forEach(function (k) {
  const zq = k.split(":");
  const got = D.configs[zq[0]][zq[1]];
  ok(JSON.stringify(got) === JSON.stringify(exp.configs[k]), "config " + k, JSON.stringify(got));
});
Object.keys(exp.unpaired).forEach(function (k) {
  const zq = k.split(":");
  ok(c.unpaired(D.configs[zq[0]][zq[1]]) === exp.unpaired[k], "unpaired " + k);
});
// condensed notation, both orders
function strip(h) { return h.replace(/<sup>(\d+)<\/sup>/g, "^$1"); }
ok(strip(c.condensed(D.configs["26"]["0"], false)) === "[Ar]4s^23d^6", "Fe filling order", strip(c.condensed(D.configs["26"]["0"], false)));
ok(strip(c.condensed(D.configs["26"]["0"], true)) === "[Ar]3d^64s^2", "Fe n order");
ok(strip(c.condensed(D.configs["26"]["3"], false)) === "[Ar]3d^5", "Fe3+ condensed");
ok(strip(c.condensed(D.configs["16"]["-2"], false)) === "[Ar]", "S2- = [Ar]");
ok(strip(c.condensed(D.configs["28"]["2"], false)) === "[Ar]3d^8", "Ni2+ = [Ar]3d8 (Day 6 p.21)");
ok(strip(c.condensed(D.configs["23"]["3"], false)) === "[Ar]3d^2", "V3+ = [Ar]3d2 (Top Hat Day 6 p.23)");
ok(strip(c.condensed(D.configs["9"]["-1"], false)) === "[Ne]", "F- = [Ne]");
ok(strip(c.condensed(D.configs["11"]["1"], false)) === "[Ne]", "Na+ = [Ne]");
// every table entry has the right electron count and never exceeds subshell capacity
let cfgOK = true;
Object.keys(D.configs).forEach(function (z) {
  Object.keys(D.configs[z]).forEach(function (q) {
    const cfg = D.configs[z][q], n = cfg.reduce(function (s, x) { return s + x[1]; }, 0);
    if (n !== +z - +q) cfgOK = false;
    cfg.forEach(function (x) { if (x[1] > { s: 2, p: 6, d: 10 }[x[0][1]]) cfgOK = false; });
  });
});
ok(cfgOK, "all configuration-table entries have Z − charge electrons and respect capacity");

// radial distributions: normalized, peaks and zeros where the index says
const R = D.radial;
["1s", "2s", "2p", "3s", "3p", "3d"].forEach(function (n) {
  const ys = R.curves[n]; let s = 0;
  for (let i = 1; i < ys.length; i++) s += (ys[i] + ys[i - 1]) / 2 * R.step;
  ok(Math.abs(s - 1) < 0.01, "radial " + n + " integrates to 1 over 0–1500 pm", s);
});
ok(Math.abs(R.features["1s"].peaks[0] - 52.9) < 0.5, "1s peak 53 pm (Day 5 p.17)");
ok(Math.abs(R.features["2s"].nodes[0] - 105.8) < 0.5, "2s zero ≈ 106 pm");
ok(Math.abs(R.features["3s"].nodes[0] - 100.6) < 0.5 && Math.abs(R.features["3s"].nodes[1] - 375.6) < 0.5, "3s zeros ≈ 101 and 376 pm");
ok(Math.abs(R.features["2p"].peaks[0] - 211.7) < 0.5, "2p peak ≈ 212 pm");
ok(Math.abs(R.features["3d"].peaks[0] - 476.3) < 0.5, "3d peak ≈ 476 pm");
ok(R.features["3s"].peaks.length === 3, "3s has three peaks (Day 5 p.18)");

// successive IE: largest jump sits right after the valence electrons (Day 7 p.10 red line)
Object.keys(D.successiveIE).forEach(function (s) {
  const ies = D.successiveIE[s], v = D.valence2[s];
  if (ies.length <= v) return;
  let best = 0, at = -1;
  for (let i = 1; i < ies.length; i++) { const r = ies[i] / ies[i - 1]; if (r > best) { best = r; at = i; } }
  ok(at === v, "largest IE jump after the valence electrons for " + s, at + " vs " + v);
});

console.log(`explorer tests: ${pass} passed, ${fail} failed`);
if (fail) { console.log(bad.map(function (x) { return "  FAIL " + x; }).join("\n")); process.exit(1); }

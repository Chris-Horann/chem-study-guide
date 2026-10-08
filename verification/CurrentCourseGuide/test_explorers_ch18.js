// Node tests: the Ch. 18 band explorer's calculations (assets/explorers_ch18.js) against the independent Python
// reference in ch18_data.py (numpy eigenvalues; written to expected_values.json by build_guide.py)
//   node verification/CurrentCourseGuide/test_explorers_ch18.js
"use strict";
const path = require("path");
const fs = require("fs");
const CX = require(path.join(__dirname, "../../study-guides/CurrentCourseGuide/assets/explorers_ch18.js"));
const C = CX.calc;
const EXP = JSON.parse(fs.readFileSync(path.join(__dirname, "expected_values.json"), "utf8"));
const E = EXP.bands;
const sandbox = {};
new Function("window", fs.readFileSync(path.join(__dirname, "../../study-guides/CurrentCourseGuide/assets/data.js"), "utf8"))(sandbox);
const D = sandbox.GUIDE_DATA;
let pass = 0, fail = 0; const bad = [];
function ok(c, name, detail) { if (c) pass++; else { fail++; bad.push(name + (detail !== undefined ? " -> " + detail : "")); } }
function close(a, b, tol) { return Math.abs(a - b) <= (tol || 1e-9) * Math.max(1, Math.abs(b)); }

// ---- cluster levels, filling, HOMO-LUMO gap, band width, and 3s/3p overlap vs. the numpy eigenvalues
Object.keys(E.clusters).forEach(function (k) {
  const n = +k, want = E.clusters[k], got = C.cluster(n);
  ok(got.s.length === n && got.s.every(function (x, i) { return close(x, want.levels[i]); }), "Na" + n + " 3s levels", JSON.stringify(got.s.slice(0, 3)));
  ok(got.p.every(function (x, i) { return close(x, want.pLevels[i]); }), "Na" + n + " 3p levels");
  ok(got.filled === want.filled && got.empty === want.empty, "Na" + n + " filled/empty", got.filled + "/" + got.empty);
  ok(got.mos === n && got.electrons === n, "Na" + n + ": one MO per 3s orbital, one electron per atom");
  ok(close(got.gapRatio, want.gapRatio, 1e-9), "Na" + n + " HOMO-LUMO gap ratio", got.gapRatio + " vs " + want.gapRatio);
  ok(close(got.widthRatio, want.widthRatio, 1e-9), "Na" + n + " band width ratio");
  ok(got.overlap === want.overlap, "Na" + n + " 3s/3p overlap", got.overlap);
});
// the gap shrinks monotonically ("gets smaller quickly", Day 12 p.21) and the band width approaches its limit
const ns = Object.keys(E.clusters).map(Number).sort(function (a, b) { return a - b; });
ok(ns.every(function (n, i) { return i === 0 || C.cluster(n).gapRatio < C.cluster(ns[i - 1]).gapRatio; }), "HOMO-LUMO gap shrinks as atoms are added");
ok(close(C.cluster(2).gapRatio, 1), "Na2's gap is the unit");
ok(C.cluster(64).widthRatio > 0.99 && C.cluster(64).widthRatio < 1, "band width approaches 4 beta");
ok(!C.cluster(4).overlap && C.cluster(8).overlap, "3s and 3p levels first overlap between Na4 and Na8 (Fig. 18.25: no overlap for Na4)");

// ---- the professor's four band pictures (Day 12 p.24) classify as on the slide
C.MATERIALS.forEach(function (m) { ok(C.classify(m) === E.classes[m.key], m.key + " is a " + E.classes[m.key], C.classify(m)); });

// ---- background crossing factor e^(-Eg/2RT)
ok(close(C.crossFactor(106, 25), E.cross.Si25, 1e-9) && close(C.crossFactor(106, 100), E.cross.Si100, 1e-9) && close(C.crossFactor(530, 25), E.cross.C25, 1e-9), "crossing factors");
const ratio = C.crossFactor(106, 100) / C.crossFactor(106, 25);
ok(ratio > 65 && ratio < 80, "Si: about 70-fold from 25 to 100 °C (the module's background note)", ratio);
ok(C.crossFactor(530, 25) < 1e-46, "diamond: below 1e-46 at 25 °C (the module's background note)");

// ---- the explorer leaves out the module's attempt and transfer species (Be; the transfer's photon wavelength)
const src = fs.readFileSync(path.join(__dirname, "../../study-guides/CurrentCourseGuide/assets/explorers_ch18.js"), "utf8");
ok(!/beryllium|\bBe\b/.test(src), "explorer never shows beryllium (the attempt's metal)");
ok(!/wavelength|\bnm\b/.test(src), "explorer never computes a photon wavelength (the transfer)");
const att = D.problems.filter(function (p) { return p.module === "m25" && (p.kind === "attempt" || p.kind === "transfer"); });
ok(att.length === 2, "m25 has one attempt and one transfer", att.length);

console.log("explorers_ch18: " + pass + " passed, " + fail + " failed");
if (fail) { bad.forEach(function (b) { console.log("  FAIL " + b); }); process.exit(1); }

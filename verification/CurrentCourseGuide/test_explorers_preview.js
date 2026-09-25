// Node tests: textbook-preview explorer calculations (assets/explorers_preview.js)
//   node verification/CurrentCourseGuide/test_explorers_preview.js
"use strict";
const path = require("path");
const fs = require("fs");
const PX = require(path.join(__dirname, "../../study-guides/CurrentCourseGuide/assets/explorers_preview.js"));
const P = PX.calc;
const sandbox = {};
new Function("window", fs.readFileSync(path.join(__dirname, "../../study-guides/CurrentCourseGuide/assets/data.js"), "utf8"))(sandbox);
const D = sandbox.GUIDE_DATA;
let pass = 0, fail = 0; const bad = [];
function ok(c, name, detail) { if (c) pass++; else { fail++; bad.push(name + (detail !== undefined ? " -> " + detail : "")); } }
function near(a, b, tol) { return Math.abs(a - b) <= tol; }

// significant figures (textbook §1.7 examples)
[["0.0592", 3], ["3.00e8", 3], ["101.3", 4], ["0.004060", 4], ["2.5270", 5], ["0.0810", 3], ["100.", 3], ["2.53", 3], ["7", 1]].forEach(function (t) {
  const I = P.sigInfo(t[0]); ok(I && I.sf === t[1], "sig figs " + t[0], I && I.sf);
});
const amb = P.sigInfo("96500"); ok(amb.sf === 3 && amb.ambiguous === 2, "96,500: 3 certain + 2 ambiguous zeros", JSON.stringify(amb && [amb.sf, amb.ambiguous]));
ok(P.sigInfo("3.00e8").decimals === -6, "3.00e8 last digit in the 10^6 place");
ok(P.sigInfo("abc") === null, "non-number rejected");

// rounding with the textbook's half-to-even tie rule (TB PDF p.57-58)
[[76.45, 1, 76.4], [76.55, 1, 76.6], [76.4521, 1, 76.5], [126.5371, 2, 126.54], [0.0456, 3, 0.046], [2.5, 0, 2], [3.5, 0, 4], [6.2, -1, 10], [4.4, -1, 0], [19.176, 0, 19], [0.505, 2, 0.5], [99.96, 1, 100.0]].forEach(function (t) {
  const r = P.roundToDecimals(t[0], t[1]); ok(near(r, t[2], 1e-12), "round " + t[0] + " to " + t[1] + " decimals", r);
});
ok(near(P.roundToSigFigs(507.0047, 3), 507, 1e-9), "507.0047 → 3 s.f.");
ok(near(P.roundToSigFigs(1.018361, 3), 1.02, 1e-12), "1.018361 → 3 s.f.");
ok(near(P.roundToSigFigs(-8.1625e-19, 3), -8.16e-19, 1e-30), "negative sci value rounds");

// weak-link calculator (textbook Sample Exercises 1.5-1.6 and the sunlight example)
let c = P.combine("124.01", "+", "2.5271"); ok(near(c.result, 126.54, 1e-9) && c.rule === "decimal places", "124.01 + 2.5271 = 126.54", JSON.stringify(c));
c = P.combine("58.5", "-", "50.0"); ok(near(c.result, 8.5, 1e-9), "58.5 − 50.0 = 8.5", c.result);
c = P.combine("163", "/", "8.5"); ok(near(c.result, 19, 1e-9) && c.keep === 2, "163 ÷ 8.5 → 19 (2 s.f.)", JSON.stringify(c));
c = P.combine("1.52e11", "/", "2.998e8"); ok(near(c.result, 507, 1e-9), "1.52e11 ÷ 2.998e8 → 507 s", c.result);

// t critical values reproduce Table 1.5 (TB PDF p.67)
[[3, 3.182], [4, 2.776], [5, 2.571], [10, 2.228], [20, 2.086]].forEach(function (t) {
  const v = P.tCritical(t[0], 0.95); ok(near(v, t[1], 0.002), "t(95%, df=" + t[0] + ") ≈ " + t[1], v.toFixed(4));
});
ok(near(P.tCritical(3, 0.90), 2.353, 0.003) && near(P.tCritical(3, 0.99), 5.841, 0.005), "t df=3 at 90% and 99%");
ok(near(P.tCritical(1000, 0.95), 1.962, 0.004), "large df approaches 1.960");

// the textbook's creatinine example (TB PDF p.65-67): mean 0.6820, s 0.00935, CI half-width 0.0116
const cr = P.analyze([0.685, 0.676, 0.669, 0.688, 0.692]);
ok(near(cr.mean, 0.6820, 5e-5) && near(cr.s, 0.00935, 5e-5) && near(cr.half, 0.0116, 5e-5) && cr.tFromTable, "creatinine statistics", JSON.stringify(cr));
// the penny example (TB PDF p.69): Z = 2.85 > 2.290
const pen = P.analyze([2.486, 2.495, 2.500, 2.502, 2.502, 2.505, 2.506, 2.507, 2.515, 3.107]);
ok(near(pen.mean, 2.562, 0.0006) && near(pen.s, 0.191, 0.0006) && near(pen.Z, 2.85, 0.01) && pen.outlier && pen.suspect === 9, "penny Grubbs test", JSON.stringify(pen));
// the sodium example (TB PDF p.69-70): lowest value not an outlier (Z = 1.5 < 1.715)
const na = P.analyze([35.8, 36.6, 36.3, 36.8, 36.4]);
ok(near(na.mean, 36.38, 0.005) && near(na.s, 0.38, 0.005) && !na.outlier, "sodium data: no outlier", JSON.stringify(na));

// unit conversions (Table 1.3) and the textbook's temperature example (TB PDF p.64)
ok(near(P.convert("length", 26.2, "mi", "km").value, 42.16, 0.01), "26.2 mi → 42.2 km");
ok(near(P.convert("length", 5.00, "in", "cm").value, 12.7, 1e-9) && P.convert("length", 5, "in", "cm").exact, "5.00 in → 12.7 cm (exact)");
ok(near(P.convert("volume", 355, "mL", "qt").value, 0.3752, 0.0002), "355 mL → 0.375 qt");
ok(near(P.convert("temperature", 98.6, "°F", "°C").value, 37.0, 0.01), "98.6 °F → 37.0 °C");
ok(near(P.convert("temperature", 2.73, "K", "°C").value, -270.42, 0.001) && near(P.convert("temperature", 2.73, "K", "°F").value, -454.756, 0.001), "2.73 K → −270.42 °C, −454.76 °F");
ok(near(P.convert("density", 19.3, "g/cm³", "kg/m³").value, 19300, 1e-6), "19.3 g/cm³ → 1.93e4 kg/m³");
ok(near(P.convert("speed", 207.0, "km/h", "m/s").value, 57.50, 0.005), "207.0 km/h → 57.50 m/s (textbook tennis serve)");

// isotope patterns from background abundances
const cl2 = P.isotopePattern({ Cl: 2 }, D.isotopes);
ok(cl2.length === 3 && cl2[0].m === 70 && cl2[1].m === 72 && cl2[2].m === 74 && near(cl2[1].rel, 64.0, 0.1) && near(cl2[2].rel, 10.24, 0.05), "Cl2 peaks 70/72/74 at 100/64.0/10.2", JSON.stringify(cl2));
const hcl = P.isotopePattern({ H: 1, Cl: 1 }, D.isotopes);
ok(hcl.length === 2 && hcl[0].m === 36 && hcl[1].m === 38 && near(hcl[1].rel, 32.0, 0.1), "HCl peaks 36/38", JSON.stringify(hcl));
const hbr = P.isotopePattern({ H: 1, Br: 1 }, D.isotopes);
ok(hbr.length === 2 && hbr[0].m === 80 && near(hbr[1].rel, 97.3, 0.1), "HBr peaks 80/82 nearly equal", JSON.stringify(hbr));
const co2 = P.isotopePattern({ C: 1, O: 2 }, D.isotopes);
ok(co2.length === 1 && co2[0].m === 44, "CO2 single peak at 44 (13C neglected)");

// Heisenberg (TB PDF p.138) and molar masses
ok(near(P.heisenbergDu(0.142, 6.80e-7) / 5.46e-28, 1, 0.002), "baseball Δu ≥ 5.46e-28 m/s");
ok(near(P.heisenbergDu(9.109e-31, 5.3e-11) / 1.09e6, 1, 0.005), "electron Δu ≥ 1.1e6 m/s");
ok(near(P.molarMass("C6H12O6", D.atomicMass), 180.155, 0.002), "glucose 180.155 g/mol");
ok(near(P.molarMass("H2SO3", D.atomicMass), 82.078, 0.001), "H2SO3 82.078 g/mol (textbook Sample Exercise 2.7)");
ok(near(P.molarMass("CaCO3", D.atomicMass), 100.086, 0.001), "CaCO3 100.086 g/mol (textbook Sample Exercise 2.10)");
// bond classes (textbook §4.2 guidelines)
ok(P.bondClass(0.4) === "nonpolar covalent" && P.bondClass(0.5) === "polar covalent" && P.bondClass(1.9) === "polar covalent" && P.bondClass(2.0) === "ionic", "bond-class cutoffs");
ok(P.bondClass(D.electronegativity.Ca - D.electronegativity.Cl) === "ionic", "Ca–Cl Δχ = 2.0 → ionic (textbook Sample Exercise 4.2)");
// periodic-table data sanity
const PT = D.periodicTable;
ok(PT.length === 118 && PT.filter(function (e) { return e.cat === "metalloid"; }).map(function (e) { return e.sym; }).join(",") === "B,Si,Ge,As,Sb,Te,At", "metalloids match textbook Fig. 2.9b");
ok(PT.filter(function (e) { return e.f === "lanthanide"; }).length === 14 && PT.filter(function (e) { return e.f === "actinide"; }).length === 14, "14 lanthanides and 14 actinides");
ok(PT[56].group === 3 && PT[88].group === 3, "La and Ac placed in group 3 as in Fig. 2.9b");
// PES data: outermost binding energy ≈ IE1 (Day 7 p.9) within 3%
Object.keys(D.pes).forEach(function (s) {
  const rows = D.pes[s], be = rows[rows.length - 1][1] * 1000, ie = D.ie1[s];
  ok(ie && Math.abs(be - ie) / ie < 0.03, "PES outermost ≈ IE1 for " + s, be + " vs " + ie);
});

console.log(`preview explorer tests: ${pass} passed, ${fail} failed`);
if (fail) { console.log(bad.map(function (x) { return "  FAIL " + x; }).join("\n")); process.exit(1); }

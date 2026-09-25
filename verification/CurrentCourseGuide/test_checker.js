// Node tests for study-guides/CurrentCourseGuide/assets/checker.js
//   node verification/CurrentCourseGuide/test_checker.js
"use strict";
const path = require("path");
const fs = require("fs");
const C = require(path.join(__dirname, "../../study-guides/CurrentCourseGuide/assets/checker.js"));
const bank = JSON.parse(fs.readFileSync(path.join(__dirname, "problem_bank.json"), "utf8"));

let pass = 0, fail = 0;
const failures = [];
function ok(cond, name, detail) {
  if (cond) pass++;
  else { fail++; failures.push(name + (detail ? "  ->  " + detail : "")); }
}
function near(a, b, rel) { return Math.abs(a - b) <= (rel || 1e-12) * Math.max(1, Math.abs(b)); }

// ------------------------------------------------------------ number parsing
const nums = [
  ["5.66e14", 5.66e14, 3], ["5.66E14", 5.66e14, 3], ["5.66 x 10^14", 5.66e14, 3], ["5.66×10^14", 5.66e14, 3],
  ["5.66 × 10⁻¹⁹", 5.66e-19, 3], ["−8.16 × 10^−19", -8.16e-19, 3], ["-8.16e-19", -8.16e-19, 3],
  ["5.66*10^14", 5.66e14, 3], ["5.66 * 10**14", 5.66e14, 3], ["11,577", 11577, 5], ["1312", 1312, 4],
  ["0.0042", 0.0042, 2], [".5", 0.5, 1], ["2.00", 2, 3], ["10^-19", 1e-19, 1], ["4.4", 4.4, 2],
  ["3.00 x 10 ^ 8", 3e8, 3], ["6.626e−34", 6.626e-34, 4], ["  441  ", 441, 3], ["1.80×10−10", 1.8e-10, 3],
];
for (const [s, v, sf] of nums) {
  const p = C.parseNumber(s);
  ok(p.ok && near(p.value, v, 1e-12), "parseNumber value " + JSON.stringify(s), JSON.stringify(p));
  ok(p.ok && p.sigfigs === sf, "parseNumber sigfigs " + JSON.stringify(s), p.sigfigs + " vs " + sf);
}
for (const s of ["", "abc", "1,5", "5.66 x 14", "e14", "5..6"]) {
  ok(!C.parseNumber(s).ok, "parseNumber rejects " + JSON.stringify(s));
}
ok(C.parseNumber("1800").sigfigsAmbiguous === true, "1800 sig figs flagged ambiguous");

// ------------------------------------------------------------ numeric checking
const nuSpec = { type: "numeric", value: 5.6566e14, tol: 0.01, sigfigs: 3, askUnit: true, units: ["s^-1", "hz", "s⁻¹", "1/s"] };
ok(C.checkNumeric(nuSpec, "5.66e14", "s^-1").correct, "numeric correct with unit");
ok(C.checkNumeric(nuSpec, "5.66e14", "Hz").correct, "unit case-insensitive Hz");
ok(C.checkNumeric(nuSpec, "5.66e14", "s⁻¹").correct, "unit with superscripts");
ok(C.checkNumeric(nuSpec, "5.66e14", "").status === "unit-missing", "unit missing flagged");
ok(C.checkNumeric(nuSpec, "5.66e14", "m").status === "unit-wrong", "unit wrong flagged");
ok(C.checkNumeric(nuSpec, "5.66e5", "Hz").status === "power", "nm-left-in power of ten flagged");
ok(C.checkNumeric(nuSpec, "5.7e14", "Hz").correct && C.checkNumeric(nuSpec, "5.7e14", "Hz").notes.length === 1, "sig-fig note but correct");
const eSpec = { type: "numeric", value: -8.1625e-19, tol: 0.01, sigfigs: 3 };
ok(C.checkNumeric(eSpec, "8.16e-19").status === "sign", "sign error flagged");
ok(C.checkNumeric(eSpec, "-8.16e-22").status === "power", "pm vs nm flagged as power of ten");
ok(C.checkNumeric(eSpec, "-8.4e-19").status === "close", "close-but-outside flagged");
ok(C.checkNumeric(eSpec, "-2e-19").status === "incorrect", "plain incorrect");
ok(C.checkNumeric(eSpec, "").status === "empty", "empty");
const intSpec = { type: "numeric", value: 16, tol: 0 };
ok(C.checkNumeric(intSpec, "16").correct && !C.checkNumeric(intSpec, "16.1").correct, "integer exact match");
ok(C.unitMatches("kJ mol⁻¹", ["kj/mol", "kj mol^-1"]), "kJ mol⁻¹ accepted");
ok(C.unitMatches("m·s⁻¹", ["m/s", "m s^-1"]), "m·s⁻¹ accepted");
ok(C.unitMatches(" J ", ["j"]), "J accepted");

// ------------------------------------------------------------ text / formula / names
const f = { type: "text", kind: "formula", accepted: ["Al2O3"], caseInsensitive: false };
ok(C.checkText(f, "Al2O3").correct, "formula exact");
ok(C.checkText(f, "Al₂O₃").correct, "formula with subscript digits");
ok(C.checkText(f, " Al2 O3 ").correct, "formula with spaces");
ok(C.checkText(f, "al2o3").status === "case", "formula capitalization");
ok(C.checkText(f, "AlO").status === "incorrect", "AlO wrong subscripts");
ok(C.checkText(f, "Al3O2").status === "incorrect", "Al3O2 wrong subscripts");
ok(C.checkText({ type: "text", kind: "formula", accepted: ["BaO"] }, "Ba2O2").status === "ratio", "Ba2O2 reduce ratio");
ok(C.checkText({ type: "text", kind: "formula", accepted: ["MCl3"] }, "MCl3").correct, "MCl3 with placeholder M");
const nm = { type: "text", accepted: ["aluminum oxide", "aluminium oxide"], caseInsensitive: true };
ok(C.checkText(nm, "Aluminum Oxide").correct, "name case-insensitive");
ok(C.checkText(nm, "aluminium oxide.").correct, "British spelling and trailing period");
ok(C.checkText(nm, "dialuminum trioxide").status === "prefix", "prefix name flagged");
ok(C.checkText({ type: "text", accepted: ["sodium chloride"], caseInsensitive: true }, "sodium chlorine").message.indexOf("-ide") >= 0, "-ine vs -ide");
ok(C.checkText({ type: "text", accepted: ["4d"], caseInsensitive: true }, "4D").correct, "subshell label");

// ------------------------------------------------------------ configurations
const Fe = { "1s": 2, "2s": 2, "2p": 6, "3s": 2, "3p": 6, "4s": 2, "3d": 6 };
const cfgInputs = ["[Ar]4s2 3d6", "[Ar]3d6 4s2", "[Ar] 4s^2 3d^6", "[Ar]4s²3d⁶", "1s2 2s2 2p6 3s2 3p6 4s2 3d6",
  "1s22s22p63s23p64s23d6", "1s^2 2s^2 2p^6 3s^2 3p^6 3d^6 4s^2", "[ar]4s2,3d6"];
for (const s of cfgInputs) {
  const p = C.parseConfig(s);
  ok(p.ok && JSON.stringify(Object.keys(p.occ).sort().map(k => k + p.occ[k])) === JSON.stringify(Object.keys(Fe).sort().map(k => k + Fe[k])),
    "parseConfig Fe " + JSON.stringify(s), JSON.stringify(p));
}
const zn = C.parseConfig("[Ar]3d104s2");
ok(zn.ok && zn.occ["3d"] === 10 && zn.occ["4s"] === 2, "3d10 then 4s2 without separators");
const sc = C.parseConfig("[Ar]3d14s2");
ok(sc.ok && sc.occ["3d"] === 1 && sc.occ["4s"] === 2, "3d1 then 4s2 without separators");
ok(!C.parseConfig("1s3").ok, "over-capacity rejected");
ok(!C.parseConfig("2d1").ok, "2d rejected");
ok(!C.parseConfig("[Ne]2p6").ok, "duplicate subshell inside core rejected");
ok(!C.parseConfig("[Xx]3s2").ok, "unknown core rejected");
const fe3 = { type: "config", target: { "1s": 2, "2s": 2, "2p": 6, "3s": 2, "3p": 6, "3d": 5 }, electrons: 23, species: "Fe<sup>3+</sup>" };
ok(C.checkConfig(fe3, "[Ar]3d5").correct, "Fe3+ correct");
ok(C.checkConfig(fe3, "[Ar]4s2 3d3").status === "cation-rule", "Fe3+ removing 3d first flagged");
ok(C.checkConfig(fe3, "[Ar]4s2 3d6").status === "count", "Fe3+ with neutral count flagged");
const ca = { type: "config", target: { "1s": 2, "2s": 2, "2p": 6, "3s": 2, "3p": 6, "4s": 2 }, electrons: 20, species: "Ca" };
ok(C.checkConfig(ca, "[Ar]3d2").status === "fill-order", "Ca as 3d2 flagged fill order");
const s2 = { type: "config", target: { "1s": 2, "2s": 2, "2p": 6, "3s": 2, "3p": 6 }, electrons: 18, species: "S<sup>2−</sup>" };
ok(C.checkConfig(s2, "[Ar]").correct && C.checkConfig(s2, "[Ne]3s2 3p6").correct, "S2- as [Ar] or [Ne]3s2 3p6");
ok(C.parseConfig("<b>1s2</b>").ok === false && C.parseConfig("<b>").reason.indexOf("<") < 0, "user text escaped in messages");

// ------------------------------------------------------------ every answer key is accepted by the checker
function fmt(v, sf) {
  if (Number.isInteger(v) && Math.abs(v) < 1e6 && !sf) return String(v);
  return v.toPrecision(Math.max(sf || 4, 4));
}
function cfgString(target) {
  const order = ["1s", "2s", "2p", "3s", "3p", "4s", "3d", "4p", "5s", "4d", "5p"];
  return order.filter(k => target[k]).map(k => k + target[k]).join(" ");
}
function keyResponse(spec) {
  switch (spec.type) {
    case "numeric": return { value: fmt(spec.value, spec.sigfigs), unit: spec.askUnit ? spec.units[0] : "" };
    case "choice": return { index: spec.options.findIndex(o => o.correct) };
    case "order": { const r = {}; spec.answerOrder.forEach((k, i) => { r[k] = i + 1; }); return { ranks: r }; }
    case "match": return { answers: spec.rows.map(r => r.answer) };
    case "text": return { value: spec.accepted[0] };
    case "config": return { value: cfgString(spec.target) };
    case "multi": return { parts: spec.parts.map(keyResponse) };
  }
  return null;
}
let keyed = 0;
for (const p of bank) {
  if (p.answer.type === "self") continue;
  const res = C.check(p.answer, keyResponse(p.answer));
  keyed++;
  ok(res.correct, "answer key accepted: " + p.id, JSON.stringify(res).slice(0, 200));
  // the key rounded to its stated significant figures must also be accepted
  (function roundedKeys(spec, label) {
    if (spec.type === "numeric" && spec.sigfigs) {
      const r = C.check(spec, { value: spec.value.toPrecision(spec.sigfigs), unit: spec.askUnit ? spec.units[0] : "" });
      ok(r.correct, "key at " + spec.sigfigs + " s.f. accepted: " + label, spec.value.toPrecision(spec.sigfigs) + " -> " + r.status);
    }
    if (spec.type === "multi") spec.parts.forEach((pt, i) => roundedKeys(pt, label + "." + i));
  })(p.answer, p.id);
  // a clearly wrong response must not pass
  if (p.answer.type === "numeric") {
    const wrong = C.check(p.answer, { value: String(p.answer.value * 1.37 + 1), unit: p.answer.askUnit ? p.answer.units[0] : "" });
    ok(!wrong.correct, "wrong numeric rejected: " + p.id);
  }
  if (p.answer.type === "choice") {
    const wi = p.answer.options.findIndex(o => !o.correct);
    ok(!C.check(p.answer, { index: wi }).correct, "wrong choice rejected: " + p.id);
  }
}

// every accepted alternative passes, and every targeted wrong answer (trap) gets its own message, never "correct"
let trapped = 0;
function trapChecks(spec, label) {
  if (spec.type === "multi") { spec.parts.forEach((pt, i) => trapChecks(pt, label + "." + i)); return; }
  if (spec.type === "text") spec.accepted.forEach(a => ok(C.check(spec, { value: a }).correct, "accepted alternative passes: " + label + " " + a));
  (spec.traps || []).forEach(t => {
    trapped++;
    if (spec.type === "numeric") {
      const r = C.check(spec, { value: String(t.value), unit: spec.askUnit ? spec.units[0] : "" });
      ok(!r.correct && r.status === "trap" && r.message === t.message, "numeric trap fires: " + label + " " + t.value, r.status);
    } else {
      t.answers.forEach(a => {
        const r = C.check(spec, { value: a });
        ok(!r.correct && r.status === "trap", "text trap fires: " + label + " " + a, r.status);
        ok(spec.accepted.indexOf(a) < 0, "trap answer is not also accepted: " + label + " " + a);
      });
    }
  });
}
for (const p of bank) if (p.answer.type !== "self") trapChecks(p.answer, p.id);
ok(trapped > 100, "trap coverage", trapped);

console.log(`checker tests: ${pass} passed, ${fail} failed; ${keyed} answer keys round-tripped; ${trapped} traps checked`);
if (fail) { console.log(failures.map(x => "  FAIL " + x).join("\n")); process.exit(1); }

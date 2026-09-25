/* ChemCheck: answer checking for the CurrentCourseGuide study guide.
   Pure functions, no DOM. Messages are trusted HTML (user text is escaped). Loads as a classic script (window.ChemCheck) or in node (module.exports).
   Tested by verification/CurrentCourseGuide/test_checker.js. */
(function (root, factory) {
  if (typeof module === "object" && module.exports) module.exports = factory();
  else root.ChemCheck = factory();
})(typeof self !== "undefined" ? self : this, function () {
  "use strict";

  var SUP = { "⁰": "0", "¹": "1", "²": "2", "³": "3", "⁴": "4", "⁵": "5", "⁶": "6", "⁷": "7", "⁸": "8", "⁹": "9", "⁻": "-", "⁺": "+" };
  var SUB = { "₀": "0", "₁": "1", "₂": "2", "₃": "3", "₄": "4", "₅": "5", "₆": "6", "₇": "7", "₈": "8", "₉": "9" };
  var CAPACITY = { s: 2, p: 6, d: 10, f: 14 };
  var CORES = {
    He: "1s2", Ne: "1s2 2s2 2p6", Ar: "1s2 2s2 2p6 3s2 3p6",
    Kr: "1s2 2s2 2p6 3s2 3p6 4s2 3d10 4p6", Xe: "1s2 2s2 2p6 3s2 3p6 4s2 3d10 4p6 5s2 4d10 5p6"
  };

  function supRunsToCaret(s) {
    // "4s²3d⁶" -> "4s^2 3d^6 " ; "10⁻¹⁹" -> "10^-19 "
    return s.replace(/[⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺]+/g, function (run) {
      var t = "";
      for (var i = 0; i < run.length; i++) t += SUP[run[i]];
      return "^" + t + " ";
    });
  }
  function subToDigits(s) {
    return s.replace(/[₀₁₂₃₄₅₆₇₈₉]/g, function (c) { return SUB[c]; });
  }
  function esc(s) {
    return String(s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; });
  }
  function normMinus(s) {
    return s.replace(/[−‒–—﹣－]/g, "-");
  }

  /* ------------------------------------------------------------ numbers */
  function countSigFigs(mant) {
    // mant: digits with optional '.', no sign, no exponent
    var hasPoint = mant.indexOf(".") >= 0;
    var digits = mant.replace(".", "");
    var stripped = digits.replace(/^0+/, "");
    if (stripped === "") return { n: 1, ambiguous: false }; // "0" or "0.0"
    if (hasPoint) return { n: stripped.length, ambiguous: false };
    var noTrail = stripped.replace(/0+$/, "");
    return { n: noTrail.length, ambiguous: noTrail.length !== stripped.length };
  }

  function parseNumber(raw) {
    if (raw === null || raw === undefined) return { ok: false, reason: "empty" };
    var s = String(raw).trim();
    if (!s) return { ok: false, reason: "empty" };
    s = normMinus(supRunsToCaret(s));
    s = s.replace(/\s+/g, " ").trim();
    // thousands separators: 11,577 or 1,234,567 (only when groups are exactly 3 digits)
    if (/^[+-]?\d{1,3}(,\d{3})+(\.\d*)?(\s|$|[eE×xX*·])/.test(s)) s = s.replace(/,(?=\d{3})/g, "");
    s = s.replace(/\s*([×xX*·])\s*/g, "$1").replace(/\s*\^\s*/g, "^").replace(/\s*([eE])\s*(?=[+-]?\d)/g, "$1").trim();
    var m = s.match(/^([+-]?)(\d+\.?\d*|\.\d+)(?:(?:[×xX*·]10(?:\^|\*\*)?([+-]?\d+))|(?:[eE]([+-]?\d+)))?$/);
    var mant, exp = 0, sign = 1;
    if (m) {
      sign = m[1] === "-" ? -1 : 1;
      mant = m[2];
      if (m[3] !== undefined) exp = parseInt(m[3], 10);
      else if (m[4] !== undefined) exp = parseInt(m[4], 10);
    } else {
      var m2 = s.match(/^([+-]?)10\^([+-]?\d+)$/);
      if (!m2) return { ok: false, reason: "format" };
      sign = m2[1] === "-" ? -1 : 1;
      mant = "1";
      exp = parseInt(m2[2], 10);
    }
    var value = sign * parseFloat(mant) * Math.pow(10, exp);
    if (!isFinite(value)) return { ok: false, reason: "format" };
    var sf = countSigFigs(mant);
    return { ok: true, value: value, sigfigs: sf.n, sigfigsAmbiguous: sf.ambiguous };
  }

  function normUnit(u) {
    if (u === null || u === undefined) return "";
    var s = normMinus(supRunsToCaret(String(u))).toLowerCase();
    s = s.replace(/[·•⋅*]/g, " ").replace(/\^\s*/g, "^").replace(/\s+/g, " ").trim();
    s = s.replace(/\s*\/\s*/g, "/").replace(/ \^/g, "^");
    return s;
  }
  function unitMatches(input, accepted) {
    var a = normUnit(input);
    var compact = a.replace(/\s+/g, "");
    for (var i = 0; i < accepted.length; i++) {
      var b = normUnit(accepted[i]);
      if (a === b || compact === b.replace(/\s+/g, "")) return true;
    }
    return false;
  }

  function sfNote(spec, parsed) {
    if (!spec.sigfigs || parsed.sigfigsAmbiguous) return "";
    if (parsed.sigfigs === spec.sigfigs) return "";
    return "Value accepted. Significant figures: the data support " + spec.sigfigs +
      " (you gave " + parsed.sigfigs + ").";
  }

  function checkNumeric(spec, input, unitInput) {
    var p = parseNumber(input);
    if (!p.ok) {
      return { status: p.reason === "empty" ? "empty" : "invalid", correct: false,
        message: p.reason === "empty" ? "Enter an answer first." :
          "That isn't a number this checker can read. Try 5.66e14, 5.66 × 10^14, or 0.0042." };
    }
    var t = spec.value, v = p.value, tol = spec.tol === undefined ? 0.01 : spec.tol;
    var close = function (x) {
      if (tol === 0) return Math.abs(x - t) < 1e-9 * Math.max(1, Math.abs(t));
      if (t === 0) return Math.abs(x) <= tol;
      return Math.abs(x - t) / Math.abs(t) <= tol + 1e-12;
    };
    var notes = [];
    if (close(v)) {
      var n = sfNote(spec, p);
      if (n) notes.push(n);
      if (spec.askUnit) {
        if (!unitInput || !String(unitInput).trim()) {
          return { status: "unit-missing", correct: false, value: v,
            message: "The number is right. Now add its unit: an answer without a unit is incomplete." };
        }
        if (!unitMatches(unitInput, spec.units || [])) {
          return { status: "unit-wrong", correct: false, value: v,
            message: "The number is right, but that unit doesn't fit. Which unit does this quantity carry? Check the units that cancel in your setup." };
        }
      }
      return { status: "correct", correct: true, value: v, notes: notes, message: "Correct." };
    }
    var tr3 = trapFor(spec, function (x) { return x.value !== undefined && Math.abs(v - x.value) <= Math.max(Math.abs(x.value) * (x.tol === undefined ? 0.01 : x.tol), 1e-12); });
    if (tr3) return tr3;
    if (t !== 0 && close(-v)) {
      return { status: "sign", correct: false, value: v,
        message: spec.signMessage || "The size is right, but the sign is wrong. Decide whether energy is released (negative) or absorbed (positive)." };
    }
    if (tol === 0 && Math.abs(t - Math.round(t)) < 1e-12)
      return { status: "incorrect", correct: false, value: v, message: "Not this count. Recount step by step, or open the next hint." };
    if (t !== 0 && v !== 0 && (v / t) > 0) {
      var k = Math.log10(v / t), kr = Math.round(k);
      if (kr !== 0 && Math.abs(k - kr) <= Math.log10(1 + Math.max(tol, 0.005)) + 1e-9) {
        return { status: "power", correct: false, value: v,
          message: "Your answer is off by a factor of 10" + (kr > 0 ? "^" + kr : "^(" + kr + ")") +
            ". That usually means a unit conversion (nm ↔ m, pm ↔ nm, g ↔ kg, J ↔ kJ) or an exponent slip." };
      }
    }
    if (t !== 0 && Math.abs(v - t) / Math.abs(t) <= 0.05) {
      return { status: "close", correct: false, value: v,
        message: "Close, but outside the tolerance. Check your rounding and the constants you used." };
    }
    return { status: "incorrect", correct: false, value: v, message: "Check your setup, or open the next hint." };
  }

  /* ------------------------------------------------------------ choice / order / match */
  function checkChoice(spec, index) {
    if (index === null || index === undefined || index < 0) return { status: "empty", correct: false, message: "Choose an option first." };
    var o = spec.options[index];
    return { status: o.correct ? "correct" : "incorrect", correct: !!o.correct, message: o.feedback || (o.correct ? "Correct." : "Not this one.") };
  }

  function checkOrder(spec, ranks) {
    // ranks: {key: rankNumber}
    var n = spec.items.length, seen = {}, i;
    for (i = 0; i < n; i++) {
      var r = ranks[spec.items[i].key];
      if (!r) return { status: "empty", correct: false, message: "Give every item a rank from 1 to " + n + "." };
      if (seen[r]) return { status: "invalid", correct: false, message: "Each rank can be used only once." };
      seen[r] = true;
    }
    var right = 0;
    for (i = 0; i < n; i++) if (ranks[spec.answerOrder[i]] === i + 1) right++;
    if (right === n) return { status: "correct", correct: true, message: "Correct order." };
    return { status: "incorrect", correct: false, positionsRight: right,
      message: right + " of " + n + " in the right position. Recheck the trend you're using." };
  }

  function checkMatch(spec, answers) {
    var n = spec.rows.length, right = 0;
    for (var i = 0; i < n; i++) {
      if (!answers[i]) return { status: "empty", correct: false, message: "Make a choice for every row." };
      if (answers[i] === spec.rows[i].answer) right++;
    }
    if (right === n) return { status: "correct", correct: true, message: "All matched correctly." };
    return { status: "incorrect", correct: false, rowsRight: right, message: right + " of " + n + " rows right." };
  }

  /* ------------------------------------------------------------ text, names, formulas */
  function normText(s) {
    return normMinus(String(s || "")).replace(/<[^>]*>/g, "").replace(/\s+/g, " ").trim().replace(/[.。]$/, "");
  }
  function normFormula(s) {
    return subToDigits(normText(s)).replace(/<\/?su[bp]>/gi, "").replace(/\s+/g, "");
  }
  function parseFormula(f) {
    // Element counts, with parenthesized groups: Mg3(PO4)2 -> {Mg: 3, P: 2, O: 8}. Returns null if unreadable.
    var pos = 0;
    function group() {
      var out = {};
      while (pos < f.length && f[pos] !== ")") {
        var part;
        if (f[pos] === "(") {
          pos++;
          part = group();
          if (part === null || f[pos] !== ")") return null;
          pos++;
        } else {
          var m = /^[A-Z][a-z]?/.exec(f.slice(pos));
          if (!m) return null;
          part = {};
          part[m[0]] = 1;
          pos += m[0].length;
        }
        var d = /^\d+/.exec(f.slice(pos)), n = d ? parseInt(d[0], 10) : 1;
        if (d) pos += d[0].length;
        for (var k in part) out[k] = (out[k] || 0) + part[k] * n;
      }
      return out;
    }
    var res = group();
    return res !== null && pos === f.length && Object.keys(res).length ? res : null;
  }
  function sameCounts(a, b) {
    var ka = Object.keys(a).sort(), kb = Object.keys(b).sort();
    if (ka.join(",") !== kb.join(",")) return false;
    for (var i = 0; i < ka.length; i++) if (a[ka[i]] !== b[ka[i]]) return false;
    return true;
  }
  function trapFor(spec, test) {
    // spec.traps: [{answers: [...]} or {value, tol}, message]; a known wrong answer gets its own explanation
    var T = spec.traps || [];
    for (var i = 0; i < T.length; i++) if (test(T[i])) return { status: "trap", correct: false, message: T[i].message };
    return null;
  }
  function gcd(a, b) { return b ? gcd(b, a % b) : a; }

  function checkText(spec, input) {
    var kind = spec.kind || "text";
    if (!normText(input)) return { status: "empty", correct: false, message: "Enter an answer first." };
    if (kind === "formula") {
      var f = normFormula(input), i;
      for (i = 0; i < spec.accepted.length; i++) if (f === spec.accepted[i]) return { status: "correct", correct: true, message: "Correct." };
      for (i = 0; i < spec.accepted.length; i++) {
        if (f.toLowerCase() === spec.accepted[i].toLowerCase())
          return { status: "case", correct: false, message: "Check capitalization: each element symbol starts with a capital letter, and a second letter is lowercase (Co is cobalt; CO is carbon monoxide)." };
      }
      var tr = trapFor(spec, function (t) { return (t.answers || []).some(function (a) { return normFormula(a) === f; }); });
      if (tr) return tr;
      var want = parseFormula(spec.accepted[0]), poly = /\(/.test(spec.accepted[0]);
      if (poly && f === spec.accepted[0].replace(/[()]/g, ""))
        return { status: "parens", correct: false, message: "Right ions, but put parentheses around a polyatomic ion before its subscript: " + spec.accepted[0] + " means more than one of that whole ion." };
      var got = parseFormula(f);
      if (!got) return { status: "invalid", correct: false, message: "Write the formula with element symbols, numbers, and parentheses only, e.g., MgCl2 or Ca(NO3)2." };
      if (want) {
        if (sameCounts(got, want))
          return { status: "parens", correct: false, message: "Right atoms, but write each polyatomic ion as a unit, in parentheses when there's more than one: " + spec.accepted[0] + "." };
        var gk = Object.keys(got).sort().join(","), wk = Object.keys(want).sort().join(",");
        if (gk !== wk) return { status: "incorrect", correct: false, message: poly ? "Those aren't the right elements. Check each ion's formula in the polyatomic-ion table." : "Those aren't the right elements. Which two elements form this compound?" };
        var els = Object.keys(want), ratioOk = true, g = 0;
        for (i = 0; i < els.length; i++) g = gcd(g, got[els[i]]);
        for (i = 0; i < els.length; i++) if (got[els[i]] / g !== want[els[i]]) ratioOk = false;
        if (ratioOk && g > 1) return { status: "ratio", correct: false, message: "Right ions and right ratio, but reduce the formula to the smallest whole-number ratio." };
        return { status: "incorrect", correct: false, message: "Right elements, wrong subscripts. Add up the charges: the total must be zero (Day 7 p.20)." };
      }
      return { status: "incorrect", correct: false, message: "Check the wording and spelling, or open the next hint." };
    }
    var t = normText(input), cmp = spec.caseInsensitive === false ? t : t.toLowerCase();
    for (var j = 0; j < spec.accepted.length; j++) {
      var a = normText(spec.accepted[j]);
      if (cmp === (spec.caseInsensitive === false ? a : a.toLowerCase())) return { status: "correct", correct: true, message: "Correct." };
    }
    var low = t.toLowerCase();
    var tr2 = trapFor(spec, function (x) { return (x.answers || []).some(function (a) { return normText(a).toLowerCase() === low; }); });
    if (tr2) return tr2;
    if (!spec.prefixesAllowed && /\b(mono|di|tri|tetra|penta|hexa)[a-z]+/.test(low)) {
      var stripped = low.replace(/\b(mono|di|tri|tetra|penta|hexa)(?=[a-z])/g, "");
      for (var k = 0; k < spec.accepted.length; k++) {
        if (stripped === normText(spec.accepted[k]).toLowerCase())
          return { status: "prefix", correct: false, message: "Drop the number prefixes. A binary ionic name is just cation name + anion name ending in -ide: MgCl₂ is “magnesium chloride” (Day 7 p.21)." };
      }
    }
    if (/ine$/.test(low) && spec.accepted.some(function (x) { return /ide$/.test(x); }))
      return { status: "incorrect", correct: false, message: "The anion's name ends in -ide (chlorine becomes chloride), Day 7 p.21." };
    return { status: "incorrect", correct: false, message: "Check the wording and spelling, or open the next hint." };
  }

  /* ------------------------------------------------------------ electron configurations */
  function parseConfig(raw) {
    var s = normMinus(supRunsToCaret(String(raw || "")));
    s = s.replace(/[,;.]/g, " ").trim();
    if (!s) return { ok: false, reason: "Enter a configuration first." };
    var occ = {}, order = [];
    var core = s.match(/^\[\s*([A-Za-z]{2})\s*\]/);
    if (core) {
      var sym = core[1].charAt(0).toUpperCase() + core[1].charAt(1).toLowerCase();
      if (!CORES[sym]) return { ok: false, reason: "Unknown noble-gas core [" + esc(core[1]) + "]. Use [He], [Ne], [Ar], or [Kr]." };
      var c = parseConfig(CORES[sym]);
      for (var key in c.occ) { occ[key] = c.occ[key]; order.push(key); }
      s = s.slice(core[0].length);
    }
    s = s.replace(/\s+/g, " ");
    var i = 0, n = s.length;
    while (i < n) {
      var ch = s.charAt(i);
      if (ch === " ") { i++; continue; }
      if (!/[1-7]/.test(ch)) return { ok: false, reason: "Couldn't read “" + esc(s.slice(i, i + 6).trim()) + "”. Write subshells like 1s2 2s2 2p6, or 1s^2 2s^2." };
      var shell = ch; i++;
      while (s.charAt(i) === " ") i++;
      var letter = s.charAt(i).toLowerCase();
      if (!/[spdf]/.test(letter)) return { ok: false, reason: "After the shell number " + shell + ", expected s, p, d, or f." };
      i++;
      while (s.charAt(i) === " ") i++;
      var count;
      if (s.charAt(i) === "^") {
        i++;
        var mm = s.slice(i).match(/^\s*(\d{1,2})/);
        if (!mm) return { ok: false, reason: "Missing electron count after ^." };
        count = parseInt(mm[1], 10); i += mm[0].length;
      } else {
        var d1 = s.charAt(i), d2 = s.charAt(i + 1), after = s.charAt(i + 2);
        if (!/\d/.test(d1)) return { ok: false, reason: "Missing the electron count for " + shell + letter + "." };
        if (/\d/.test(d2) && !/[spdfSPDF]/.test(after) && parseInt(d1 + d2, 10) <= CAPACITY[letter]) {
          count = parseInt(d1 + d2, 10); i += 2;
        } else { count = parseInt(d1, 10); i += 1; }
      }
      var sub = shell + letter;
      var l = "spdf".indexOf(letter);
      if (l > parseInt(shell, 10) - 1) return { ok: false, reason: sub + " doesn't exist: ℓ must be at most n − 1 (Day 5 p.12)." };
      if (count > CAPACITY[letter]) return { ok: false, reason: "A " + letter + " subshell holds at most " + CAPACITY[letter] + " electrons (Pauli, Day 5 p.15)." };
      if (occ[sub] !== undefined) {
        return { ok: false, reason: sub + " appears twice" + (core ? " (it may already be inside the noble-gas core)." : ".") };
      }
      if (count > 0) { occ[sub] = count; order.push(sub); }
    }
    var total = 0;
    for (var k in occ) total += occ[k];
    return { ok: true, occ: occ, electrons: total, order: order };
  }

  function sameOcc(a, b) {
    var k;
    for (k in a) if (a[k] !== (b[k] || 0)) return false;
    for (k in b) if (b[k] !== (a[k] || 0)) return false;
    return true;
  }

  function checkConfig(spec, input) {
    var p = parseConfig(input);
    if (!p.ok) return { status: "invalid", correct: false, message: p.reason };
    if (sameOcc(p.occ, spec.target)) {
      return { status: "correct", correct: true, message: "Correct. (Either order, filling order or n order, is accepted: both appear in lecture.)" };
    }
    if (p.electrons !== spec.electrons) {
      return { status: "count", correct: false,
        message: "Your configuration holds " + p.electrons + " electrons, but " + (spec.species || "this species") + " has " + spec.electrons +
          ". Electrons = Z − charge." };
    }
    var t = spec.target;
    if (spec.incorrectNote) return { status: "incorrect", correct: false, message: spec.incorrectNote };
    if ((p.occ["4s"] || 0) > (t["4s"] || 0) && (p.occ["3d"] || 0) < (t["3d"] || 0) && (t["4s"] || 0) === 0) {
      return { status: "cation-rule", correct: false,
        message: "Right electron count, but a cation loses its highest-n electrons first: 4s empties before 3d, “regardless of the order in which they were added” (Day 6 p.21)." };
    }
    if ((p.occ["3d"] || 0) > (t["3d"] || 0) && (p.occ["4s"] || 0) < (t["4s"] || 0)) {
      return { status: "fill-order", correct: false, message: "Right electron count, but 4s is lower in energy than 3d, so 4s fills first (Day 6 p.19)." };
    }
    return { status: "incorrect", correct: false,
      message: "Right electron count, but some electrons are in the wrong subshells. Follow the filling order on Day 6 p.19 and fill each subshell before the next." };
  }


  /* ------------------------------------------------------------ dispatch */
  function check(spec, response) {
    switch (spec.type) {
      case "numeric": return checkNumeric(spec, response.value, response.unit);
      case "choice": return checkChoice(spec, response.index);
      case "order": return checkOrder(spec, response.ranks || {});
      case "match": return checkMatch(spec, response.answers || []);
      case "text": return checkText(spec, response.value);
      case "config": return checkConfig(spec, response.value);
      case "multi":
        var parts = [], all = true, anyEmpty = false;
        for (var i = 0; i < spec.parts.length; i++) {
          var r = check(spec.parts[i], (response.parts || [])[i] || {});
          parts.push(r);
          if (!r.correct) all = false;
          if (r.status === "empty") anyEmpty = true;
        }
        return { status: all ? "correct" : (anyEmpty ? "empty" : "incorrect"), correct: all, parts: parts,
          message: all ? "All parts correct." : (anyEmpty ? "Answer every part first." : "Some parts need another look.") };
      default:
        return { status: "invalid", correct: false, message: "This item isn't auto-checked." };
    }
  }

  return {
    esc: esc, parseNumber: parseNumber, countSigFigs: countSigFigs, normUnit: normUnit, unitMatches: unitMatches,
    checkNumeric: checkNumeric, checkChoice: checkChoice, checkOrder: checkOrder, checkMatch: checkMatch,
    checkText: checkText, parseFormula: parseFormula, parseConfig: parseConfig, checkConfig: checkConfig, check: check
  };
});

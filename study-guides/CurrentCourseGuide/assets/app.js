/* CurrentCourseGuide application: routing, stages, problems, progress.
   Classic script (works from file://). Depends on data.js, scope.js, checker.js, explorers.js. */
(function () {
  "use strict";
  var D = window.GUIDE_DATA, CC = window.ChemCheck, EX = window.Explorers || { mount: {} };
  if (!D || !CC) { document.body.insertAdjacentHTML("afterbegin", "<p class='fatal'>The guide's data files didn't load. Keep the assets folder next to index.html.</p>"); return; }

  var KEY = D.meta.storageKey;
  var PROBS = {}, BY_MODULE = {};
  D.problems.forEach(function (p) {
    PROBS[p.id] = p;
    (BY_MODULE[p.module] = BY_MODULE[p.module] || []).push(p);
  });
  var MOD = {};
  D.modules.forEach(function (m) { MOD[m.id] = m; });
  var STAGE_IDS = D.stages.map(function (s) { return s[0]; });
  var STAGE_LABEL = {};
  D.stages.forEach(function (s) { STAGE_LABEL[s[0]] = s[1]; });
  var KIND_ORDER = { attempt: 0, practice: 1, transfer: 2, mastery: 3, mixed: 4 };

  /* ------------------------------------------------------------ progress store */
  var storageOK = true;
  function fresh() { return { v: 1, problems: {}, selfChecks: {}, visited: {}, stages: {}, last: null, mixedOrder: null }; }
  function load() {
    try {
      var raw = window.localStorage.getItem(KEY);
      if (!raw) return fresh();
      var s = JSON.parse(raw);
      return s && s.v === 1 ? s : fresh();
    } catch (e) { storageOK = false; return fresh(); }
  }
  var S = load();
  function compactState() {
    var out = {}, k, r;
    for (k in S) out[k] = S[k];
    out.problems = {};
    for (k in S.problems) { r = S.problems[k]; if (r.attempts || r.revealed || r.hints || r.rating || r.text || r.correct) out.problems[k] = r; }
    return out;
  }
  function save() {
    try { window.localStorage.setItem(KEY, JSON.stringify(compactState())); }
    catch (e) { storageOK = false; }
    if (!storageOK) { var n = document.getElementById("storage-note"); if (n) n.hidden = false; }
  }
  function rec(id) {
    return S.problems[id] || (S.problems[id] = { attempts: 0, correct: false, firstTry: false, hints: 0, revealed: false, revealedBeforeCorrect: false });
  }

  /* ------------------------------------------------------------ helpers */
  function $(sel, el) { return (el || document).querySelector(sel); }
  function $all(sel, el) { return Array.prototype.slice.call((el || document).querySelectorAll(sel)); }
  function h(tag, attrs, html) {
    var e = document.createElement(tag);
    if (attrs) for (var k in attrs) {
      if (attrs[k] === null || attrs[k] === undefined || attrs[k] === false) continue;
      if (k === "class") e.className = attrs[k];
      else if (k === "text") e.textContent = attrs[k];
      else e.setAttribute(k, attrs[k] === true ? "" : attrs[k]);
    }
    if (html !== undefined && html !== null) e.innerHTML = html;
    return e;
  }
  var ICON = { ok: "✓", no: "✗", warn: "!", info: "i" };
  function feedbackHTML(kind, label, msg, notes) {
    if (msg && msg.indexOf(label) === 0) msg = msg.slice(label.length).replace(/^\s+/, "");   // never "Not yet. Not yet."
    var s = "<span class='fb-icon' aria-hidden='true'>" + ICON[kind] + "</span><span class='fb-text'><strong>" + label + "</strong> " + (msg || "");
    if (notes && notes.length) s += " <span class='fb-note'>" + notes.join(" ") + "</span>";
    return s + "</span>";
  }
  function problemsOf(module, kinds) {
    var list = (BY_MODULE[module] || []).filter(function (p) { return !kinds || kinds.indexOf(p.kind) >= 0; });
    return list.slice().sort(function (a, b) { return KIND_ORDER[a.kind] - KIND_ORDER[b.kind]; });
  }

  /* ------------------------------------------------------------ mastery */
  function credit(p) {
    var r = S.problems[p.id];
    if (!r) return 0;
    if (p.answer.type === "self") return r.rating === "got" ? 1 : r.rating === "partly" ? 0.5 : 0;
    if (r.correct && !r.revealedBeforeCorrect) return 1;
    if (r.correct) return 0.25;
    return 0;
  }
  function moduleScore(mid) {
    var list = BY_MODULE[mid] || [], sum = 0, touched = false, solved = 0;
    list.forEach(function (p) {
      var r = S.problems[p.id];
      if (r && (r.attempts || r.revealed || r.hints || r.rating)) touched = true;
      var c = credit(p); sum += c; if (c >= 1) solved++;
    });
    var score = list.length ? sum / list.length : 0;
    var label = !touched && !S.visited[mid] ? "Not started" : score >= 0.8 ? "Mastered" : score >= 0.4 ? "Practicing" : "Learning";
    return { score: score, label: label, solved: solved, total: list.length, touched: touched };
  }

  /* ------------------------------------------------------------ spectrum band + sidebar */
  function wavelengthColor(nm) {
    var r = 0, g = 0, b = 0;
    if (nm < 440) { r = -(nm - 440) / 60; b = 1; }
    else if (nm < 490) { g = (nm - 440) / 50; b = 1; }
    else if (nm < 510) { g = 1; b = -(nm - 510) / 20; }
    else if (nm < 580) { r = (nm - 510) / 70; g = 1; }
    else if (nm < 645) { r = 1; g = -(nm - 645) / 65; }
    else { r = 1; }
    var f = nm < 420 ? 0.35 + 0.65 * (nm - 380) / 40 : nm > 680 ? 0.35 + 0.65 * (750 - nm) / 70 : 1;
    function c(x) { return Math.round(255 * Math.pow(Math.max(0, x) * f, 0.8)); }
    return "rgb(" + c(r) + "," + c(g) + "," + c(b) + ")";
  }
  function renderBand() {
    var band = document.getElementById("band");
    if (!band) return;
    if (!band.childElementCount) {
      D.modules.forEach(function (m, i) {
        var nm = 410 + i * (290 / (D.modules.length - 1));
        var b = h("a", { class: "band-line" + (m.label === "preview" ? " is-preview" : ""), href: "#" + m.id, "data-testid": "band-" + m.id, style: "--line:" + wavelengthColor(nm) });
        b.appendChild(h("span", { class: "band-glow", "aria-hidden": "true" }));
        band.appendChild(b);
      });
    }
    $all(".band-line", band).forEach(function (b, i) {
      var m = D.modules[i], sc = moduleScore(m.id);
      var lvl = sc.label === "Not started" ? 0.12 : 0.28 + 0.72 * sc.score;
      b.style.setProperty("--lvl", lvl.toFixed(3));
      b.classList.toggle("is-mastered", sc.label === "Mastered");
      b.setAttribute("aria-label", "Section " + m.sec + ", " + m.title + " (" + D.labelText[m.label] + "): " + sc.label + ", " + sc.solved + " of " + sc.total + " items solved");
      b.title = "§" + m.sec + " " + m.short + ": " + sc.label;
    });
  }
  function renderSidebar() {
    D.modules.forEach(function (m) {
      var el = $("[data-status='" + m.id + "']");
      if (!el) return;
      var sc = moduleScore(m.id);
      el.textContent = sc.label;
      el.setAttribute("data-level", sc.label.toLowerCase().replace(/\s+/g, "-"));
    });
    var mx = $("[data-status='mixed']");
    if (mx) {
      var list = BY_MODULE.mixed || [], n = list.filter(function (p) { return credit(p) >= 1; }).length;
      mx.textContent = n + " of " + list.length;
    }
  }
  function refreshProgress() { renderBand(); renderSidebar(); renderDashboard(); }

  /* ------------------------------------------------------------ dashboard (start page) */
  function renderDashboard() {
    var box = document.getElementById("dashboard");
    if (!box) return;
    var html = "";
    D.units.forEach(function (u) {
      html += "<p class='dash-unit'>" + u.chapter + ": " + u.title + "</p><ol class='dash-list'>";
      u.modules.forEach(function (mid) {
        var m = MOD[mid], sc = moduleScore(mid);
        html += "<li><a href='#" + m.id + "'><span class='dash-num'>§" + m.sec + "</span><span class='dash-title'>" + m.title +
          " <span class='pill-label " + (m.label === "preview" ? "preview" : "lecture") + "'>" + D.labelText[m.label] + "</span></span>" +
          "<span class='dash-meter' aria-hidden='true'><span style='width:" + Math.round(sc.score * 100) + "%'></span></span>" +
          "<span class='dash-status' data-level='" + sc.label.toLowerCase().replace(/\s+/g, "-") + "'>" + sc.label + "</span></a></li>";
      });
      html += "</ol>";
    });
    box.innerHTML = html;
    var resume = document.getElementById("resume");
    if (resume) {
      if (S.last && S.last !== "start") {
        var mid = S.last.split("/")[0], m = MOD[mid];
        resume.hidden = false;
        resume.href = "#" + S.last;
        resume.textContent = m ? "Resume: §" + m.sec + " " + m.title : "Resume where you left off";
      } else resume.hidden = true;
    }
  }

  /* ------------------------------------------------------------ problem widgets */
  function numericWidget(spec, tid, wrap) {
    var row = h("div", { class: "ans-row" });
    var inp = h("input", { type: "text", inputmode: "decimal", autocomplete: "off", spellcheck: "false", class: "ans-num",
      "data-testid": tid, placeholder: "e.g., 5.66e-19", "aria-label": (wrap.label || "Answer") + (spec.unitLabel && !spec.askUnit ? " in " + spec.unitLabel.replace(/<[^>]+>/g, "") : "") });
    row.appendChild(inp);
    var unit = null;
    if (spec.askUnit) {
      unit = h("input", { type: "text", autocomplete: "off", spellcheck: "false", class: "ans-unit", "data-testid": tid + "-unit",
        placeholder: "unit", "aria-label": (wrap.label || "Answer") + " unit" });
      row.appendChild(unit);
    } else if (spec.unitLabel) {
      row.appendChild(h("span", { class: "ans-unit-fixed" }, spec.unitLabel));
    }
    return { el: row, get: function () { return { value: inp.value, unit: unit ? unit.value : "" }; },
      set: function (r) { if (r) { inp.value = r.value || ""; if (unit) unit.value = r.unit || ""; } }, focus: inp };
  }
  function textWidget(spec, tid, wrap) {
    var ph = spec.placeholder || (spec.type === "config" ? "e.g., [Ne]3s2 3p4" : "");
    var inp = h("input", { type: "text", autocomplete: "off", spellcheck: "false", class: spec.type === "config" ? "ans-cfg" : "ans-text",
      "data-testid": tid, placeholder: ph, "aria-label": wrap.label || "Answer" });
    var row = h("div", { class: "ans-row" });
    row.appendChild(inp);
    if (spec.type === "config") row.appendChild(h("span", { class: "ans-help" }, "Type superscripts as plain digits (3p4), with ^ (3p^4), or as ⁴. Either filling order or n order is fine."));
    if (spec.kind === "formula") row.appendChild(h("span", { class: "ans-help" }, "Type subscripts as plain digits: MgCl2 means MgCl<sub>2</sub>."));
    return { el: row, get: function () { return { value: inp.value }; }, set: function (r) { if (r) inp.value = r.value || ""; }, focus: inp };
  }
  function choiceWidget(spec, tid, pid) {
    var fs = h("fieldset", { class: "ans-choice" });
    fs.appendChild(h("legend", { class: "sr-only" }, "Choose one answer"));
    spec.options.forEach(function (o, i) {
      var lab = h("label", { class: "choice" });
      var r = h("input", { type: "radio", name: "ch-" + pid, value: String(i), "data-testid": tid + "-" + i });
      lab.appendChild(r);
      lab.appendChild(h("span", { class: "choice-text" }, o.html));
      fs.appendChild(lab);
    });
    return { el: fs, get: function () {
      var c = $("input:checked", fs); return { index: c ? parseInt(c.value, 10) : -1 }; },
      set: function (r) { if (r && r.index >= 0) { var x = $all("input", fs)[r.index]; if (x) x.checked = true; } },
      focus: $("input", fs) };
  }
  function orderWidget(spec, tid) {
    var box = h("div", { class: "ans-order" });
    box.appendChild(h("p", { class: "ans-help" }, "Give each item a rank: " + spec.direction + "."));
    var n = spec.items.length, selects = {};
    spec.items.forEach(function (it) {
      var row = h("label", { class: "order-row" });
      var sel = h("select", { "data-testid": tid + "-" + it.key });
      sel.appendChild(h("option", { value: "" }, "rank"));
      for (var k = 1; k <= n; k++) sel.appendChild(h("option", { value: String(k) }, String(k)));
      selects[it.key] = sel;
      row.appendChild(sel);
      row.appendChild(h("span", { class: "order-item" }, it.html));
      box.appendChild(row);
    });
    return { el: box, get: function () {
      var ranks = {}; for (var k in selects) ranks[k] = selects[k].value ? parseInt(selects[k].value, 10) : 0; return { ranks: ranks }; },
      set: function (r) { if (r && r.ranks) for (var k in r.ranks) if (selects[k] && r.ranks[k]) selects[k].value = String(r.ranks[k]); },
      focus: selects[spec.items[0].key] };
  }
  function matchWidget(spec, tid) {
    var t = h("div", { class: "ans-match" }), sels = [];
    spec.rows.forEach(function (row, i) {
      var lab = h("label", { class: "match-row" });
      lab.appendChild(h("span", { class: "match-item" }, row.html));
      var sel = h("select", { "data-testid": tid + "-" + i });
      sel.appendChild(h("option", { value: "" }, "choose…"));
      spec.options.forEach(function (o) { sel.appendChild(h("option", { value: o.key }, o.html.replace(/<[^>]+>/g, ""))); });
      sels.push(sel);
      lab.appendChild(sel);
      t.appendChild(lab);
    });
    return { el: t, get: function () { return { answers: sels.map(function (s) { return s.value; }) }; },
      set: function (r) { if (r && r.answers) r.answers.forEach(function (v, i) { if (sels[i]) sels[i].value = v || ""; }); }, focus: sels[0] };
  }
  function makeWidget(spec, tid, pid, label) {
    var wrap = { label: label };
    switch (spec.type) {
      case "numeric": return numericWidget(spec, tid, wrap);
      case "text": case "config": return textWidget(spec, tid, wrap);
      case "choice": return choiceWidget(spec, tid, pid);
      case "order": return orderWidget(spec, tid);
      case "match": return matchWidget(spec, tid);
      case "multi":
        var box = h("div", { class: "ans-multi" }), parts = [];
        spec.parts.forEach(function (part, k) {
          var row = h("div", { class: "part" });
          row.appendChild(h("p", { class: "part-label", id: pid + "-lbl-" + k }, part.label));
          var w = makeWidget(part, tid + "-" + k, pid + "-" + k, part.label.replace(/<[^>]+>/g, ""));
          row.appendChild(w.el);
          var fb = h("p", { class: "part-fb", "aria-live": "polite" });
          row.appendChild(fb);
          parts.push({ w: w, fb: fb });
          box.appendChild(row);
        });
        return { el: box, parts: parts, get: function () { return { parts: parts.map(function (p) { return p.w.get(); }) }; },
          set: function (r) { if (r && r.parts) r.parts.forEach(function (x, i) { if (parts[i]) parts[i].w.set(x); }); }, focus: parts[0].w.focus };
    }
    return null;
  }

  function renderProblem(p, host) {
    var r = rec(p.id);
    var art = h("article", { class: "ex ex-" + p.kind + (p.answer.type === "self" ? " ex-self" : ""), id: "ex-" + p.id, "data-id": p.id });
    var head = h("header", { class: "ex-head" });
    head.appendChild(h("span", { class: "ex-level" }, p.level || ""));
    var modLabel = MOD[p.module] ? MOD[p.module].label : "mixed";
    if (p.kind !== "mixed" && (p.label === "preview" && modLabel !== "preview" || p.label === "lecture" && modLabel === "preview")) {
      head.appendChild(h("span", { class: "pill-label " + p.label }, p.label === "preview" ? "Textbook preview" : "Covered in lecture"));
    }
    if (p.label === "preview") art.classList.add("ex-preview");
    var st = h("span", { class: "ex-state" });
    head.appendChild(st);
    art.appendChild(head);
    if (p.signal) art.appendChild(h("p", { class: "signal-inline" }, "<span class='signal-label'>Lecture signal</span> " + p.signal));
    art.appendChild(h("div", { class: "ex-prompt" }, p.prompt));
    var src = h("p", { class: "source" }, "Source: " + p.source);

    if (p.answer.type === "self") {
      var ta = h("textarea", { class: "ans-explain", rows: "4", "data-testid": "answer-" + p.id, "aria-label": "Your explanation", placeholder: "Write your explanation first, in your own words." });
      if (r.text) ta.value = r.text;
      ta.addEventListener("input", function () { r.text = ta.value; save(); });
      art.appendChild(ta);
      var acts = h("div", { class: "ex-actions" });
      var rv = h("button", { type: "button", class: "btn", "data-testid": "reveal-" + p.id }, "Compare with a model answer");
      acts.appendChild(rv);
      art.appendChild(acts);
      var model = h("div", { class: "ex-solution", hidden: true }, "<h4>Model answer</h4>" + p.answer.model);
      art.appendChild(model);
      var rate = h("div", { class: "rate", hidden: true, role: "group", "aria-label": "Rate your explanation" });
      rate.appendChild(h("p", { class: "rate-q" }, "How did your explanation compare?"));
      [["got", "I had the key ideas"], ["partly", "Partly"], ["notyet", "Not yet"]].forEach(function (x) {
        var b = h("button", { type: "button", class: "btn rate-btn", "data-testid": "rate-" + p.id + "-" + x[0], "aria-pressed": r.rating === x[0] ? "true" : "false" }, x[1]);
        b.addEventListener("click", function () {
          r.rating = x[0]; save();
          $all(".rate-btn", rate).forEach(function (bb) { bb.setAttribute("aria-pressed", bb === b ? "true" : "false"); });
          st.innerHTML = stateLabel(p);
          refreshProgress();
        });
        rate.appendChild(b);
      });
      art.appendChild(rate);
      rv.addEventListener("click", function () {
        var open = model.hidden;
        model.hidden = !open; rate.hidden = false;
        rv.textContent = open ? "Hide the model answer" : "Compare with a model answer";
        if (open && !r.revealed) { r.revealed = true; save(); }
      });
      if (r.revealed) { model.hidden = false; rate.hidden = false; rv.textContent = "Hide the model answer"; }
      st.innerHTML = stateLabel(p);
      art.appendChild(src);
      host.appendChild(art);
      return;
    }

    var w = makeWidget(p.answer, "answer-" + p.id, p.id, "Answer");
    var ansBox = h("div", { class: "ex-answer" });
    ansBox.appendChild(w.el);
    art.appendChild(ansBox);
    var actions = h("div", { class: "ex-actions" });
    var bCheck = h("button", { type: "button", class: "btn primary", "data-testid": "check-" + p.id }, "Check");
    var nH = (p.hints || []).length;
    var bHint = h("button", { type: "button", class: "btn", "data-testid": "hint-btn-" + p.id }, "Hint 1 of " + nH);
    var bRev = h("button", { type: "button", class: "btn ghost", "data-testid": "reveal-" + p.id }, "Show solution");
    actions.appendChild(bCheck);
    if (nH) actions.appendChild(bHint);
    actions.appendChild(bRev);
    art.appendChild(actions);
    var fb = h("div", { class: "ex-feedback", role: "status", "aria-live": "polite" });
    art.appendChild(fb);
    var hintList = h("ol", { class: "ex-hints", hidden: true, "aria-label": "Hints" });
    art.appendChild(hintList);
    var sol = h("div", { class: "ex-solution", hidden: true }, "<h4>Solution</h4>" + p.solution);
    art.appendChild(sol);
    var cue = null;
    if (p.kind === "mixed") {
      var home = MOD[p.home];
      cue = h("div", { class: "ex-cue", hidden: true }, "<h4>What gave it away</h4><p>" + p.cue + "</p>" +
        (home ? "<p class='cue-home'><span class='pill-label " + p.label + "'>" + (p.label === "preview" ? "Textbook preview" : "Covered in lecture") + "</span> Review: <a href='#" + home.id + "'>§" + home.sec + " " + home.title + "</a></p>" : ""));
      art.appendChild(cue);
    }
    art.appendChild(src);

    function showHints(n) {
      hintList.innerHTML = "";
      for (var i = 0; i < n && i < nH; i++) {
        hintList.appendChild(h("li", { class: "hint", "data-step": String(i + 1) }, "<span class='hint-label'>Hint " + (i + 1) + "</span> " + p.hints[i]));
      }
      hintList.hidden = n === 0;
      if (n >= nH) { bHint.textContent = "No more hints"; bHint.disabled = true; }
      else bHint.textContent = "Hint " + (n + 1) + " of " + nH;
    }
    function showSolution(open) {
      sol.hidden = !open;
      bRev.textContent = open ? "Hide solution" : "Show solution";
      if (open && cue) cue.hidden = false;
    }
    bHint.addEventListener("click", function () {
      r.hints = Math.min(nH, (r.hints || 0) + 1); save();
      showHints(r.hints);
      var last = hintList.lastElementChild; if (last) { last.setAttribute("tabindex", "-1"); last.focus(); }
      refreshProgress();
    });
    bRev.addEventListener("click", function () {
      var open = sol.hidden;
      if (open) {
        if (!r.revealed) { r.revealed = true; if (!r.correct) r.revealedBeforeCorrect = true; save(); refreshProgress(); }
        st.innerHTML = stateLabel(p);
      }
      showSolution(open);
    });
    function doCheck() {
      var resp = w.get();
      var res = CC.check(p.answer, resp);
      if (res.status === "empty") { fb.className = "ex-feedback fb-warn"; fb.innerHTML = feedbackHTML("warn", "Nothing to check yet.", res.message); return; }
      r.attempts = (r.attempts || 0) + 1;
      r.resp = resp;
      if (res.correct && !r.correct) {
        r.correct = true;
        r.firstTry = r.attempts === 1 && !r.hints;
      }
      save();
      if (w.parts) {
        res.parts.forEach(function (pr, i) {
          var pf = w.parts[i].fb;
          pf.className = "part-fb " + (pr.correct ? "fb-ok" : "fb-no");
          pf.innerHTML = feedbackHTML(pr.correct ? "ok" : "no", pr.correct ? "Correct." : "Not yet.", pr.correct ? (pr.notes || []).join(" ") : pr.message);
        });
      }
      var kind = res.correct ? "ok" : (res.status === "sign" || res.status === "power" || res.status === "close" || res.status.indexOf("unit") === 0 || res.status === "case" || res.status === "ratio" || res.status === "prefix") ? "warn" : "no";
      fb.className = "ex-feedback fb-" + kind;
      var label = res.correct ? "Correct." : kind === "warn" ? "Almost." : "Not yet.";
      var msg = res.correct ? (p.answer.type === "choice" ? res.message.replace(/^Right[:.]?\s*/, "") : "") : res.message;
      fb.innerHTML = feedbackHTML(kind, label, msg, res.correct ? res.notes : null);
      if (res.correct) {
        if (cue) cue.hidden = false;
        if (sol.hidden) fb.insertAdjacentHTML("beforeend", " <span class='fb-next'>Open the solution to compare your reasoning.</span>");
      }
      st.innerHTML = stateLabel(p);
      refreshProgress();
    }
    bCheck.addEventListener("click", doCheck);
    art.addEventListener("keydown", function (e) {
      if (e.key === "Enter" && e.target && e.target.tagName === "INPUT" && e.target.type === "text") { e.preventDefault(); doCheck(); }
    });

    // restore
    if (r.resp) w.set(r.resp);
    if (r.hints) showHints(r.hints); else hintList.hidden = true;
    if (r.correct && cue) cue.hidden = false;
    if (r.correct) { fb.className = "ex-feedback fb-ok"; fb.innerHTML = feedbackHTML("ok", "Solved.", r.revealedBeforeCorrect ? "(after viewing the solution)" : ""); }
    st.innerHTML = stateLabel(p);
    host.appendChild(art);
  }
  function stateLabel(p) {
    var r = S.problems[p.id];
    if (!r) return "";
    if (p.answer.type === "self") return r.rating ? "<span class='pill pill-" + r.rating + "'>" + ({ got: "Explained", partly: "Partly explained", notyet: "Revisit" })[r.rating] + "</span>" : "";
    if (r.correct && !r.revealedBeforeCorrect) return "<span class='pill pill-got'><span aria-hidden='true'>✓</span> Solved" + (r.firstTry ? " on the first try" : "") + "</span>";
    if (r.correct) return "<span class='pill pill-partly'>Solved after the solution</span>";
    if (r.revealed) return "<span class='pill pill-notyet'>Solution viewed</span>";
    if (r.attempts) return "<span class='pill pill-try'>" + r.attempts + (r.attempts === 1 ? " try" : " tries") + "</span>";
    return "";
  }

  /* ------------------------------------------------------------ compare stage */
  function renderCompare(mid) {
    var slot = $("[data-compare='" + mid + "']");
    if (!slot) return;
    var p = problemsOf(mid, ["attempt"])[0];
    if (!p) return;
    var r = S.problems[p.id] || {};
    slot.innerHTML = "";
    var ready = r.attempts || r.revealed || slot.getAttribute("data-open") === "1";
    if (!ready) {
      var gate = h("div", { class: "gate" }, "<p>Try the <a href='#" + mid + "/attempt'>Attempt problem</a> first: comparing works best after you have committed to an answer.</p>");
      var b = h("button", { type: "button", class: "btn", "data-testid": "reveal-compare-" + mid }, "Show the comparison anyway");
      b.addEventListener("click", function () { slot.setAttribute("data-open", "1"); renderCompare(mid); });
      gate.appendChild(b);
      slot.appendChild(gate);
      return;
    }
    var c = p.compare;
    slot.appendChild(h("div", { class: "compare-grid" },
      "<section class='cmp cmp-wrong'><h3><span aria-hidden='true'>✗</span> Tempting reasoning</h3>" + c.wrong +
      "<p class='cmp-why'><strong>Why it's tempting:</strong> " + c.tempting + "</p></section>" +
      "<section class='cmp cmp-fails'><h3><span aria-hidden='true'>!</span> Why it fails</h3><p>" + c.fails + "</p></section>" +
      "<section class='cmp cmp-right'><h3><span aria-hidden='true'>✓</span> Correct reasoning</h3>" + p.solution + "</section>"));
    slot.appendChild(h("p", { class: "source" }, "Source: " + p.source));
  }

  /* ------------------------------------------------------------ stages */
  function buildStageTabs(section) {
    var mid = section.id;
    var bar = $(".stage-tabs", section);
    if (!bar || bar.childElementCount) return;
    bar.setAttribute("role", "tablist");
    bar.setAttribute("aria-label", "Stages of this module");
    STAGE_IDS.forEach(function (sid, i) {
      var panel = $(".stage[data-stage='" + sid + "']", section);
      if (!panel) return;
      panel.id = panel.id || (mid + "-" + sid);
      panel.setAttribute("role", "tabpanel");
      var b = h("button", { type: "button", role: "tab", class: "stage-tab", id: mid + "-tab-" + sid, "aria-controls": panel.id,
        "data-stage": sid, "data-testid": "stage-" + mid + "-" + sid, tabindex: "-1" },
        "<span class='stage-num' aria-hidden='true'>" + (i + 1) + "</span><span class='stage-name'>" + STAGE_LABEL[sid] + "</span><span class='stage-seen' aria-hidden='true'></span>");
      panel.setAttribute("aria-labelledby", b.id);
      b.addEventListener("click", function () { showStage(mid, sid, true); });
      b.addEventListener("keydown", function (e) {
        var tabs = $all(".stage-tab", bar), k = tabs.indexOf(b);
        if (e.key === "ArrowRight" || e.key === "ArrowLeft") {
          e.preventDefault();
          var nx = tabs[(k + (e.key === "ArrowRight" ? 1 : tabs.length - 1)) % tabs.length];
          nx.focus(); showStage(mid, nx.getAttribute("data-stage"), true, true);
        } else if (e.key === "Home" || e.key === "End") {
          e.preventDefault();
          var t = e.key === "Home" ? tabs[0] : tabs[tabs.length - 1];
          t.focus(); showStage(mid, t.getAttribute("data-stage"), true, true);
        }
      });
      bar.appendChild(b);
      // continue button at the end of each stage
      var next = STAGE_IDS[i + 1];
      var foot = h("div", { class: "stage-foot" });
      if (next) {
        var nb = h("button", { type: "button", class: "btn primary", "data-testid": "next-" + mid + "-" + sid }, "Continue to " + STAGE_LABEL[next]);
        nb.addEventListener("click", function () {
          showStage(mid, next, true);
          window.scrollTo(0, Math.max(0, section.offsetTop - 70));
          var t = document.getElementById(mid + "-tab-" + next); if (t) t.focus({ preventScroll: true });
        });
        foot.appendChild(nb);
      } else {
        var idx = D.modules.findIndex(function (m) { return m.id === mid; });
        var nm = D.modules[idx + 1];
        foot.innerHTML = nm ? "<a class='btn primary' href='#" + nm.id + "' data-testid='next-module-" + mid + "'>Next: §" + nm.sec + " " + nm.title + "</a>"
          : "<a class='btn primary' href='#mixed' data-testid='next-module-" + mid + "'>Go to the mixed review</a>";
      }
      panel.appendChild(foot);
    });
  }
  function showStage(mid, sid, userAction, keepFocus) {
    var section = document.getElementById(mid);
    if (!section || STAGE_IDS.indexOf(sid) < 0) sid = "learn";
    $all(".stage", section).forEach(function (p) { p.hidden = p.getAttribute("data-stage") !== sid; });
    $all(".stage-tab", section).forEach(function (t) {
      var on = t.getAttribute("data-stage") === sid;
      t.setAttribute("aria-selected", on ? "true" : "false");
      t.setAttribute("tabindex", on ? "0" : "-1");
    });
    var st = S.stages[mid] || (S.stages[mid] = { seen: {}, current: "learn" });
    st.seen[sid] = true; st.current = sid;
    $all(".stage-tab", section).forEach(function (t) { t.classList.toggle("is-seen", !!st.seen[t.getAttribute("data-stage")]); });
    if (sid === "compare") renderCompare(mid);
    if (sid === "explore") mountExplorers(section);
    S.last = mid + "/" + sid;
    save();
    if (userAction && window.history && window.history.replaceState) window.history.replaceState(null, "", "#" + mid + "/" + sid);
  }

  /* ------------------------------------------------------------ explorers */
  function mountExplorers(scope) {
    $all("[data-explorer]", scope).forEach(function (el) {
      if (el.getAttribute("data-mounted")) return;
      var name = el.getAttribute("data-explorer");
      var fn = EX.mount && EX.mount[name];
      if (fn) {
        try { fn(el, D); el.setAttribute("data-mounted", "1"); }
        catch (e) { el.innerHTML = "<p class='fatal'>This explorer failed to load (" + String(e && e.message || e).replace(/</g, "&lt;") + ").</p>"; if (window.console) console.error(e); }
      } else el.innerHTML = "<p class='fatal'>Explorer “" + name + "” is missing.</p>";
    });
  }

  /* ------------------------------------------------------------ slots, checklists */
  function fillSlots() {
    $all(".slot[data-module]").forEach(function (slot) {
      if (slot.getAttribute("data-filled")) return;
      var mid = slot.getAttribute("data-module"), kinds = (slot.getAttribute("data-kinds") || "").split(/\s+/).filter(Boolean);
      var list = problemsOf(mid, kinds.length ? kinds : null);
      if (mid === "mixed" && S.mixedOrder) {
        var pos = {}; S.mixedOrder.forEach(function (id, i) { pos[id] = i; });
        list.sort(function (a, b) { return (pos[a.id] === undefined ? 999 : pos[a.id]) - (pos[b.id] === undefined ? 999 : pos[b.id]); });
      }
      list.forEach(function (p) { renderProblem(p, slot); });
      slot.setAttribute("data-filled", "1");
    });
    $all(".cando[data-module]").forEach(function (ul) {
      var mid = ul.getAttribute("data-module");
      var box = S.selfChecks[mid] || (S.selfChecks[mid] = {});
      $all("li[data-key]", ul).forEach(function (li) {
        if ($("input", li)) return;
        var key = li.getAttribute("data-key");
        var id = "cando-" + mid + "-" + key;
        var inp = h("input", { type: "checkbox", id: id, "data-testid": id });
        inp.checked = !!box[key];
        inp.addEventListener("change", function () { box[key] = inp.checked; save(); });
        var lab = h("label", { for: id }, li.innerHTML);
        li.innerHTML = "";
        li.appendChild(inp); li.appendChild(lab);
      });
    });
    var sh = document.getElementById("mixed-shuffle");
    if (sh && !sh.getAttribute("data-bound")) {
      sh.setAttribute("data-bound", "1");
      sh.addEventListener("click", function () {
        var ids = (BY_MODULE.mixed || []).map(function (p) { return p.id; });
        for (var i = ids.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)); var t = ids[i]; ids[i] = ids[j]; ids[j] = t; }
        S.mixedOrder = ids; save();
        var slot = $(".slot[data-module='mixed']");
        slot.innerHTML = ""; slot.removeAttribute("data-filled"); fillSlots();
      });
    }
  }

  /* ------------------------------------------------------------ router */
  var firstRoute = true;
  function route() {
    var hash = (location.hash || "").replace(/^#/, "") || "start";
    var parts = hash.split("/"), page = parts[0], stage = parts[1];
    var el = document.getElementById(page);
    if (!el || !el.classList.contains("page")) { page = "start"; el = document.getElementById("start"); }
    $all("main > .page").forEach(function (p) { p.hidden = p !== el; });
    $all(".nav-link").forEach(function (a) {
      if (a.getAttribute("data-nav") === page) a.setAttribute("aria-current", "page"); else a.removeAttribute("aria-current");
    });
    $all(".band-line").forEach(function (a) { a.classList.toggle("is-current", a.getAttribute("href") === "#" + page); });
    S.visited[page] = true;
    if (el.classList.contains("module")) {
      buildStageTabs(el);
      var st = S.stages[page];
      showStage(page, stage || (st && st.current) || "learn", false);
    } else {
      S.last = page === "start" ? S.last : page;
      mountExplorers(el);
      save();
    }
    closeMenu();
    refreshProgress();
    if (!firstRoute) {
      window.scrollTo(0, 0);
      var hd = $("h1", el);
      if (hd) { hd.setAttribute("tabindex", "-1"); hd.focus({ preventScroll: true }); }
    }
    firstRoute = false;
    document.title = (el.getAttribute("data-title") || ($("h1", el) ? $("h1", el).textContent : "Study guide")) + " | Chem 1151 study guide";
  }

  /* ------------------------------------------------------------ menu, reset */
  function closeMenu() {
    document.body.classList.remove("menu-open");
    var t = $("[data-testid='menu-toggle']"); if (t) t.setAttribute("aria-expanded", "false");
  }
  function initChrome() {
    var t = $("[data-testid='menu-toggle']");
    if (t) t.addEventListener("click", function () {
      var open = !document.body.classList.contains("menu-open");
      document.body.classList.toggle("menu-open", open);
      t.setAttribute("aria-expanded", open ? "true" : "false");
      if (open) { var a = $(".sidebar .nav-link[aria-current]") || $(".sidebar .nav-link"); if (a) a.focus(); }
    });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape" && document.body.classList.contains("menu-open")) { closeMenu(); if (t) t.focus(); } });
    var scrim = document.getElementById("scrim");
    if (scrim) scrim.addEventListener("click", closeMenu);
    var rb = $("[data-testid='reset-progress']");
    if (rb) rb.addEventListener("click", function () {
      if (window.confirm("Erase all saved progress for this guide (answers, hints, ratings, checklists)? This can't be undone.")) {
        S = fresh();
        try { window.localStorage.removeItem(KEY); } catch (e) { /* ignore */ }
        location.hash = "#start";
        location.reload();
      }
    });
    var sp = document.getElementById("scope-panel");
    if (sp && window.SCOPE_PANEL) sp.innerHTML = window.SCOPE_PANEL.html;
    if (!storageOK) { var n = document.getElementById("storage-note"); if (n) n.hidden = false; }
  }

  initChrome();
  fillSlots();
  window.addEventListener("hashchange", route);
  route();
})();

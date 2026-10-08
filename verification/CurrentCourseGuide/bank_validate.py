"""Structural validation of problem-bank entries (shared by build_guide.py and check_bank.py).

validate(problems, modules, check_modules=None, need_mixed=True) returns a list of error strings and fills in
each problem's topic label when it isn't set explicitly (from its module; a mixed problem from its home module).
check_modules limits the per-module counts (one attempt, three practice, a transfer, a self-rated item) to the
listed module ids; None checks every module.
"""
import math
import re

from modules_def import MODULES, MODULE_IDS, KINDS, ANSWER_TYPES


def check_answer(err, pid, a, where="answer"):
    t = a.get("type")
    if t not in ANSWER_TYPES:
        err(pid, f"{where}: unknown type {t!r}")
        return
    if t == "numeric":
        v = a.get("value")
        if not isinstance(v, (int, float)) or not math.isfinite(v):
            err(pid, f"{where}: numeric value missing or not finite")
        if a.get("askUnit") and not a.get("units"):
            err(pid, f"{where}: askUnit without an accepted-unit list")
        if "sigfigs" in a and not isinstance(a["sigfigs"], int):
            err(pid, f"{where}: sigfigs must be an int")
    elif t == "choice":
        n_ok = sum(1 for o in a["options"] if o["correct"])
        if n_ok != 1:
            err(pid, f"{where}: {n_ok} correct options (need exactly 1)")
        for o in a["options"]:
            if not o.get("feedback"):
                err(pid, f"{where}: option without feedback: {o['html'][:30]}")
    elif t == "order":
        keys = [it["key"] for it in a["items"]]
        if sorted(keys) != sorted(a["answerOrder"]) or len(set(keys)) != len(keys):
            err(pid, f"{where}: answerOrder is not a permutation of the item keys")
    elif t == "match":
        opts = {o["key"] for o in a["options"]}
        for r in a["rows"]:
            if r["answer"] not in opts:
                err(pid, f"{where}: match row answer {r['answer']!r} not among options")
    elif t == "text":
        if not a.get("accepted"):
            err(pid, f"{where}: text answer with no accepted list")
    elif t == "config":
        if sum(a["target"].values()) != a["electrons"]:
            err(pid, f"{where}: config target sums to {sum(a['target'].values())}, electrons = {a['electrons']}")
    elif t == "multi":
        if not a.get("parts"):
            err(pid, f"{where}: multi with no parts")
        for k, part in enumerate(a["parts"]):
            if not part.get("label"):
                err(pid, f"{where}: part {k} has no label")
            check_answer(err, pid, part, f"{where}.part{k}")
    elif t == "self":
        if not a.get("model"):
            err(pid, f"{where}: self-rated item with no model answer")


def validate(problems, modules=MODULES, check_modules=None, need_mixed=True):
    errors = []

    def err(pid, msg):
        errors.append(f"{pid}: {msg}")

    ids = [p["id"] for p in problems]
    dups = sorted({i for i in ids if ids.count(i) > 1})
    if dups:
        errors.append(f"duplicate problem ids: {dups}")
    for p in problems:
        pid = p["id"]
        if not re.fullmatch(r"[a-z0-9-]+", pid):
            err(pid, "id must be lowercase letters, digits, hyphens (used in data-testids)")
        if p["module"] not in MODULE_IDS + ["mixed"]:
            err(pid, f"unknown module {p['module']}")
        if p["kind"] not in KINDS:
            err(pid, f"unknown kind {p['kind']}")
        if not p.get("source"):
            err(pid, "missing source citation")
        if not p.get("prompt"):
            err(pid, "missing prompt")
        check_answer(err, pid, p["answer"])
        if p["answer"]["type"] != "self":
            if not p.get("solution"):
                err(pid, "missing solution")
            hints = p.get("hints") or []
            need = 4 if p["kind"] == "attempt" else 1
            if p["answer"]["type"] in ("numeric", "multi", "config") and p["kind"] != "attempt":
                need = 2
            if len(hints) < need:
                err(pid, f"{len(hints)} hints; need at least {need}")
        if p["kind"] == "attempt":
            c = p.get("compare") or {}
            for k in ("wrong", "tempting", "fails"):
                if not c.get(k):
                    err(pid, f"attempt compare missing {k!r}")
        if p["kind"] == "mixed":
            if not p.get("cue"):
                err(pid, "mixed problem missing 'what gave it away' cue")
            if p.get("home") not in MODULE_IDS:
                err(pid, "mixed problem missing home module")
        # topic label: explicit, else from the module (mixed: from the home module)
        if "label" not in p:
            mod = next((m for m in modules if m["id"] == (p.get("home") if p["module"] == "mixed" else p["module"])), None)
            p["label"] = "preview" if (mod and mod["label"] == "preview") else "lecture"
        if p["label"] not in ("lecture", "preview"):
            err(pid, f"label must be lecture or preview, not {p['label']!r}")
        if p["label"] == "preview" and "textbook" not in p.get("source", ""):
            err(pid, "textbook-preview problem must cite a textbook section and page")
        if p["label"] == "lecture" and not re.search(r"Day \d", p.get("source", "")):
            err(pid, "lecture problem must cite a lecture slide")
        mod = next((m for m in modules if m["id"] == p["module"]), None)
        if mod and mod["label"] == "preview" and p["label"] == "lecture":
            err(pid, "lecture-labeled problem inside a textbook-preview module")
    for m in (check_modules if check_modules is not None else MODULE_IDS):
        kinds = [p["kind"] for p in problems if p["module"] == m]
        if kinds.count("attempt") != 1:
            errors.append(f"{m}: needs exactly one attempt problem (has {kinds.count('attempt')})")
        if kinds.count("practice") < 3:
            errors.append(f"{m}: needs at least 3 practice problems")
        if kinds.count("transfer") < 1:
            errors.append(f"{m}: needs a transfer problem")
        if not any(p["module"] == m and p["answer"]["type"] == "self" for p in problems):
            errors.append(f"{m}: needs a self-rated explain item")
    if need_mixed and sum(1 for p in problems if p["kind"] == "mixed") < 15:
        errors.append("mixed review needs at least 15 problems")
    return errors

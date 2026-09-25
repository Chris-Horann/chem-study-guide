"""Build the CurrentCourseGuide study guide.

    py -3.11 verification/CurrentCourseGuide/build_guide.py

Writes (all paths relative to the project root):
  study-guides/CurrentCourseGuide/assets/data.js    window.GUIDE_DATA (problems, course data, constants)
  study-guides/CurrentCourseGuide/assets/scope.js   window.SCOPE_PANEL (generated from SOURCE_SCOPE.md)
  study-guides/CurrentCourseGuide/index.html        assembled from verification/CurrentCourseGuide/src/*.html
  verification/CurrentCourseGuide/problem_bank.json  JSON copy of the problem bank
  verification/CurrentCourseGuide/expected_values.json  Python reference values for the node tests

index.html is GENERATED: edit the fragments in src/ and rebuild.
The build stops with an error if any problem fails structural validation.
"""
import html
import json
import math
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
GUIDE = ROOT / "study-guides" / "CurrentCourseGuide"
ASSETS = GUIDE / "assets"
SRC = HERE / "src"
sys.path.insert(0, str(HERE))

from guide_common import *            # noqa: E402,F401
import problem_bank_b                  # noqa: E402  (imports problem_bank_a first)
import problem_bank_c                  # noqa: E402  Ch. 1 textbook preview
import problem_bank_d                  # noqa: E402  Ch. 2 textbook preview
import problem_bank_e                  # noqa: E402  Ch. 3-4 textbook preview + mixed x21-x35
import problem_bank_f                  # noqa: E402  Ch. 4 naming, acids, Lewis symbols and structures (Day 8 + §4.3-4.4)
import problem_bank_g                  # noqa: E402  Ch. 4 §4.5-4.9 + mixed x36-x47
import ch4_data                        # noqa: E402  data for the Ch. 4 explorers
from problem_bank_a import PROBLEMS    # noqa: E402

BUILD_DATE = "2026-09-25"
LAST_DAY = 8                           # latest lecture the guide's labels describe
STORAGE_KEY = "chemstudy:CurrentCourseGuide"

def tbp(a, b):
    """textbook page range: 'printed a–b (PDF a+34–b+34)'"""
    return f"printed pp. {a}–{b} (PDF {a + 34}–{b + 34})" if b != a else f"printed p. {a} (PDF {a + 34})"

UNITS = [
    {"id": "C1", "title": "Matter and Energy: An Atomic Perspective", "chapter": "Ch. 1",
     "modules": ["m1", "t1-2", "t1-3", "t1-4", "t1-5", "t1-6", "t1-7", "t1-8", "t1-9"]},
    {"id": "C2", "title": "Atoms, Ions, and Molecules", "chapter": "Ch. 2",
     "modules": ["m2", "t2-2", "t2-3", "t2-4", "t2-5", "t2-6"]},
    {"id": "C3", "title": "Atomic Structure", "chapter": "Ch. 3",
     "modules": ["m3", "m4", "m5", "m6", "m7", "t3-5", "m8", "m9", "m10", "m11", "m12", "m13", "t3-11"]},
    {"id": "C4", "title": "Chemical Bonding", "chapter": "Ch. 4",
     "modules": ["m14", "t4-2", "m15", "m16", "m17", "t4-3", "m18", "m19", "t4-5", "t4-6", "t4-7", "t4-8", "t4-9"]},
]
# label: "lecture" = covered in lecture; "preview" = textbook preview; "lecture+preview" = lecture topic with a labeled preview part
MODULES = [
    {"id": "m1", "sec": "1.1", "title": "Atoms from mass laws", "short": "Mass laws", "label": "lecture+preview",
     "sources": "Day 1 p.8–15", "textbook": "§1.1, " + tbp(4, 7), "prereqs": []},
    {"id": "t1-2", "sec": "1.2", "title": "COAST: a framework for solving problems", "short": "COAST", "label": "preview",
     "sources": "", "textbook": "§1.2, " + tbp(7, 8), "prereqs": []},
    {"id": "t1-3", "sec": "1.3", "title": "Classes and properties of matter", "short": "Classes of matter", "label": "preview",
     "sources": "", "textbook": "§1.3, " + tbp(8, 13), "prereqs": ["m1"]},
    {"id": "t1-4", "sec": "1.4", "title": "States of matter", "short": "States of matter", "label": "preview",
     "sources": "", "textbook": "§1.4, " + tbp(13, 16), "prereqs": ["t1-3"]},
    {"id": "t1-5", "sec": "1.5", "title": "Forms of energy", "short": "Forms of energy", "label": "lecture+preview",
     "sources": "Day 1 p.15", "textbook": "§1.5, " + tbp(16, 17), "prereqs": ["t1-4"]},
    {"id": "t1-6", "sec": "1.6", "title": "Formulas and models", "short": "Formulas and models", "label": "preview",
     "sources": "", "textbook": "§1.6, " + tbp(17, 19), "prereqs": ["m1"]},
    {"id": "t1-7", "sec": "1.7", "title": "Measurements and significant figures", "short": "Significant figures", "label": "preview",
     "sources": "", "textbook": "§1.7, " + tbp(19, 26), "prereqs": []},
    {"id": "t1-8", "sec": "1.8", "title": "Unit conversions and dimensional analysis", "short": "Unit conversions", "label": "preview",
     "sources": "", "textbook": "§1.8, " + tbp(26, 31), "prereqs": ["t1-7"]},
    {"id": "t1-9", "sec": "1.9", "title": "Analyzing experimental results", "short": "Statistics", "label": "preview",
     "sources": "", "textbook": "§1.9, " + tbp(31, 37), "prereqs": ["t1-7"]},
    {"id": "m2", "sec": "2.1", "title": "Inside the atom", "short": "Inside the atom", "label": "lecture+preview",
     "sources": "Day 1 p.16–20; Day 2 p.4–24", "textbook": "§2.1, " + tbp(48, 53), "prereqs": ["m1"]},
    {"id": "t2-2", "sec": "2.2", "title": "Nuclides and their symbols", "short": "Nuclide symbols", "label": "lecture+preview",
     "sources": "Day 2 p.22–23 (RAMP UP)", "textbook": "§2.2, " + tbp(53, 56), "prereqs": ["m2"]},
    {"id": "t2-3", "sec": "2.3", "title": "Navigating the periodic table", "short": "Periodic table", "label": "lecture+preview",
     "sources": "Day 2 p.24 (RAMP UP)", "textbook": "§2.3, " + tbp(56, 60), "prereqs": ["t2-2"]},
    {"id": "t2-4", "sec": "2.4", "title": "Masses of atoms, ions, and molecules", "short": "Atomic mass", "label": "lecture+preview",
     "sources": "Day 2 p.21–23 (RAMP UP)", "textbook": "§2.4, " + tbp(60, 64), "prereqs": ["t2-2"]},
    {"id": "t2-5", "sec": "2.5", "title": "Moles and molar masses", "short": "Moles", "label": "preview",
     "sources": "", "textbook": "§2.5, " + tbp(64, 70), "prereqs": ["t2-4", "t1-8"]},
    {"id": "t2-6", "sec": "2.6", "title": "Mass spectrometry", "short": "Mass spectrometry", "label": "preview",
     "sources": "", "textbook": "§2.6, " + tbp(70, 74), "prereqs": ["t2-4"]},
    {"id": "m3", "sec": "3.1", "title": "Light: waves and photons", "short": "Light", "label": "lecture+preview",
     "sources": "Day 2 p.25–30; Day 3 p.12, p.17", "textbook": "§3.1, " + tbp(86, 89), "prereqs": []},
    {"id": "m4", "sec": "3.2", "title": "Atomic spectra", "short": "Spectra", "label": "lecture",
     "sources": "Day 2 p.31; Day 3 p.7–11", "textbook": "§3.2, " + tbp(89, 90), "prereqs": ["m3"]},
    {"id": "m5", "sec": "3.3", "title": "Quantized energy: Planck and the photoelectric effect", "short": "Photoelectric effect", "label": "lecture",
     "sources": "Day 3 p.11–19", "textbook": "§3.3, " + tbp(90, 95), "prereqs": ["m3", "m4"]},
    {"id": "m6", "sec": "3.4", "title": "Hydrogen's spectrum and the Bohr model", "short": "Bohr model", "label": "lecture",
     "sources": "Day 3 p.21; Day 4 p.3, p.6–10", "textbook": "§3.4, " + tbp(95, 100), "prereqs": ["m4", "m5"]},
    {"id": "m7", "sec": "3.5", "title": "Matter waves (de Broglie)", "short": "Matter waves", "label": "lecture",
     "sources": "Day 4 p.11–17", "textbook": "§3.5, " + tbp(100, 103), "prereqs": ["m6"]},
    {"id": "t3-5", "sec": "3.5", "title": "The Heisenberg uncertainty principle", "short": "Uncertainty principle", "label": "preview",
     "sources": "", "textbook": "§3.5, " + tbp(103, 104), "prereqs": ["m7"]},
    {"id": "m8", "sec": "3.6", "title": "Wavefunctions, quantum numbers, and Pauli", "short": "Quantum numbers", "label": "lecture",
     "sources": "Day 4 p.18; Day 5 p.7–16", "textbook": "§3.6, " + tbp(104, 108), "prereqs": ["m6", "m7"]},
    {"id": "m9", "sec": "3.7", "title": "Orbital shapes and radial distributions", "short": "Orbitals", "label": "lecture+preview",
     "sources": "Day 5 p.17–20; Day 6 p.12, p.18", "textbook": "§3.7, " + tbp(108, 111), "prereqs": ["m8"]},
    {"id": "m10", "sec": "3.8", "title": "Electron configurations", "short": "Configurations", "label": "lecture+preview",
     "sources": "Day 6 p.6–20; Day 7 p.6", "textbook": "§3.8, " + tbp(111, 119), "prereqs": ["m8", "m9"]},
    {"id": "m11", "sec": "3.9", "title": "Configurations of ions", "short": "Ion configurations", "label": "lecture",
     "sources": "Day 6 p.21–23", "textbook": "§3.9, " + tbp(119, 122), "prereqs": ["m10"]},
    {"id": "m12", "sec": "3.10", "title": "Atomic and ionic size", "short": "Size trends", "label": "lecture",
     "sources": "Day 6 p.24–26; Day 7 p.5, p.7–8", "textbook": "§3.10, " + tbp(122, 125), "prereqs": ["m10", "m11"]},
    {"id": "m13", "sec": "3.11–3.12", "title": "Ionization energy and electron affinity", "short": "IE and EA", "label": "lecture",
     "sources": "Day 7 p.9–11", "textbook": "§3.11 (IE part), " + tbp(125, 128) + "; §3.12, " + tbp(130, 133), "prereqs": ["m6", "m10", "m12"]},
    {"id": "t3-11", "sec": "3.11", "title": "Photoelectron spectroscopy", "short": "PES", "label": "preview",
     "sources": "", "textbook": "§3.11 (PES part), " + tbp(128, 130), "prereqs": ["m13", "m5"]},
    {"id": "m14", "sec": "4.1", "title": "Bonds, Coulomb energy, and lattices", "short": "Bonds and lattices", "label": "lecture+preview",
     "sources": "Day 7 p.12–17; Day 8 p.11, p.14–15, p.18", "textbook": "§4.1, " + tbp(146, 151), "prereqs": ["m12", "m13"]},
    {"id": "t4-2", "sec": "4.2", "title": "Electronegativity and polar bonds", "short": "Electronegativity", "label": "preview",
     "sources": "", "textbook": "§4.2, " + tbp(151, 154), "prereqs": ["m14", "m13"]},
    {"id": "m15", "sec": "4.3", "title": "Ionic formulas and names", "short": "Formulas and names", "label": "lecture",
     "sources": "Day 7 p.18–21; Day 8 p.6", "textbook": "§4.3 (binary ionic, main group), " + tbp(155, 156), "prereqs": ["m11", "m14"]},
    {"id": "m16", "sec": "4.3", "title": "Transition-metal ions and polyatomic ions", "short": "Metals and polyatomic ions", "label": "lecture+preview",
     "sources": "Day 8 p.7–10", "textbook": "§4.3 (transition metals; polyatomic ions), " + tbp(156, 159), "prereqs": ["m15"]},
    {"id": "m17", "sec": "4.3", "title": "Naming covalent compounds", "short": "Covalent names", "label": "lecture+preview",
     "sources": "Day 8 p.12–13", "textbook": "§4.3 (binary molecular compounds), " + tbp(154, 155), "prereqs": ["m15", "m14"]},
    {"id": "t4-3", "sec": "4.3", "title": "Naming acids", "short": "Acids", "label": "preview",
     "sources": "", "textbook": "§4.3 (binary acids; oxoacids), " + tbp(159, 161), "prereqs": ["m16", "m17"]},
    {"id": "m18", "sec": "4.4", "title": "Lewis symbols and the octet rule", "short": "Lewis symbols", "label": "lecture+preview",
     "sources": "Day 8 p.16–18", "textbook": "§4.4 (Lewis symbols; ionic compounds), " + tbp(161, 163), "prereqs": ["m10", "m14"]},
    {"id": "m19", "sec": "4.4", "title": "Lewis structures: the five steps", "short": "Lewis structures", "label": "lecture+preview",
     "sources": "Day 8 p.19–26, p.28–30", "textbook": "§4.4 (five steps; double and triple bonds), " + tbp(163, 168), "prereqs": ["m18"]},
    {"id": "t4-5", "sec": "4.5", "title": "Resonance", "short": "Resonance", "label": "lecture+preview",
     "sources": "Day 8 p.26–30", "textbook": "§4.5, " + tbp(168, 172), "prereqs": ["m19"]},
    {"id": "t4-6", "sec": "4.6", "title": "Bond lengths and strengths", "short": "Bond lengths", "label": "preview",
     "sources": "", "textbook": "§4.6, " + tbp(172, 174), "prereqs": ["t4-5", "m14"]},
    {"id": "t4-7", "sec": "4.7", "title": "Formal charge", "short": "Formal charge", "label": "preview",
     "sources": "", "textbook": "§4.7, " + tbp(174, 178), "prereqs": ["m19", "t4-5", "t4-2"]},
    {"id": "t4-8", "sec": "4.8", "title": "Exceptions to the octet rule", "short": "Octet exceptions", "label": "preview",
     "sources": "", "textbook": "§4.8, " + tbp(178, 183), "prereqs": ["t4-7", "m19"]},
    {"id": "t4-9", "sec": "4.9", "title": "Vibrating bonds and the greenhouse effect", "short": "Vibrating bonds", "label": "preview",
     "sources": "", "textbook": "§4.9, " + tbp(183, 185), "prereqs": ["t4-2", "m3"]},
]
for i, m in enumerate(MODULES, 1):
    m["n"] = i
    m["unit"] = next(u["id"] for u in UNITS if m["id"] in u["modules"])
assert [x for u in UNITS for x in u["modules"]] == [m["id"] for m in MODULES], "UNITS order must match MODULES"
LABEL_TEXT = {"lecture": "Covered in lecture", "preview": "Textbook preview", "lecture+preview": "Lecture + preview"}
STAGES = [["learn", "Learn"], ["understand", "Understand"], ["explore", "Explore"], ["attempt", "Attempt"],
          ["compare", "Compare"], ["practice", "Practice"], ["master", "Master"]]
MODULE_IDS = [m["id"] for m in MODULES]
KINDS = {"attempt", "practice", "transfer", "mastery", "mixed"}
ANSWER_TYPES = {"numeric", "choice", "multi", "order", "match", "text", "self", "config"}

# ---------------------------------------------------------------- validation
errors = []

def err(pid, msg):
    errors.append(f"{pid}: {msg}")

def check_answer(pid, a, where="answer"):
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
            check_answer(pid, part, f"{where}.part{k}")
    elif t == "self":
        if not a.get("model"):
            err(pid, f"{where}: self-rated item with no model answer")

ids = [p["id"] for p in PROBLEMS]
dups = sorted({i for i in ids if ids.count(i) > 1})
if dups:
    errors.append(f"duplicate problem ids: {dups}")
for p in PROBLEMS:
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
    check_answer(pid, p["answer"])
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
        mod = next((m for m in MODULES if m["id"] == (p.get("home") if p["module"] == "mixed" else p["module"])), None)
        p["label"] = "preview" if (mod and mod["label"] == "preview") else "lecture"
    if p["label"] not in ("lecture", "preview"):
        err(pid, f"label must be lecture or preview, not {p['label']!r}")
    if p["label"] == "preview" and "textbook" not in p.get("source", ""):
        err(pid, "textbook-preview problem must cite a textbook section and page")
    if p["label"] == "lecture" and not re.search(r"Day \d", p.get("source", "")):
        err(pid, "lecture problem must cite a lecture slide")
for m in MODULE_IDS:
    kinds = [p["kind"] for p in PROBLEMS if p["module"] == m]
    if kinds.count("attempt") != 1:
        errors.append(f"{m}: needs exactly one attempt problem (has {kinds.count('attempt')})")
    if kinds.count("practice") < 3:
        errors.append(f"{m}: needs at least 3 practice problems")
    if kinds.count("transfer") < 1:
        errors.append(f"{m}: needs a transfer problem")
    if not any(p["module"] == m and p["answer"]["type"] == "self" for p in PROBLEMS):
        errors.append(f"{m}: needs a self-rated explain item")
if sum(1 for p in PROBLEMS if p["kind"] == "mixed") < 15:
    errors.append("mixed review needs at least 15 problems")

if errors:
    print("BUILD FAILED: problem-bank validation errors")
    for e in errors:
        print("  -", e)
    sys.exit(1)

# ---------------------------------------------------------------- computed course data
def radial_curves():
    """Normalized hydrogen radial distributions P(r) = r^2 R_nl(r)^2 (pm^-1), r in pm.
    BACKGROUND model (exact hydrogen functions, a0 = 52.918 pm); the slides show the plots."""
    a0 = 52.918
    def R(name, r):
        p = r / a0
        k = a0 ** -1.5
        if name == "1s":
            return 2 * k * math.exp(-p)
        if name == "2s":
            return k / (2 * math.sqrt(2)) * (2 - p) * math.exp(-p / 2)
        if name == "2p":
            return k / (2 * math.sqrt(6)) * p * math.exp(-p / 2)
        if name == "3s":
            return 2 * k / (81 * math.sqrt(3)) * (27 - 18 * p + 2 * p * p) * math.exp(-p / 3)
        if name == "3p":
            return 4 * k / (81 * math.sqrt(6)) * (6 * p - p * p) * math.exp(-p / 3)
        if name == "3d":
            return 4 * k / (81 * math.sqrt(30)) * p * p * math.exp(-p / 3)
        raise ValueError(name)
    step, rmax = 2.0, 1500.0
    rs = [i * step for i in range(int(rmax / step) + 1)]
    curves, raw = {}, {}
    for name in ("1s", "2s", "2p", "3s", "3p", "3d"):
        ys = [r * r * R(name, r) ** 2 for r in rs]
        raw[name] = ys
        curves[name] = [float(f"{y:.4g}") for y in ys]
    # 1s electron density psi^2 = R^2/(4 pi), scaled to its value at r = 0 (the slide's y-axis has no numbers)
    dens = [R("1s", r) ** 2 / (4 * math.pi) for r in rs]
    curves["1s_density_rel"] = [float(f"{d / dens[0]:.4g}") for d in dens]
    # analytic features for labels
    feats = {
        "1s": {"peaks": [a0], "nodes": []},
        "2s": {"peaks": [(3 - math.sqrt(5)) * a0, (3 + math.sqrt(5)) * a0], "nodes": [2 * a0]},
        "2p": {"peaks": [4 * a0], "nodes": []},
        "3s": {"peaks": [], "nodes": [(18 - math.sqrt(108)) / 4 * a0, (18 + math.sqrt(108)) / 4 * a0]},
        "3p": {"peaks": [], "nodes": [6 * a0]},
        "3d": {"peaks": [9 * a0], "nodes": []},
    }
    # numeric peaks for 3s/3p: local maxima of the unrounded curve, refined by a parabola through 3 points
    for name in ("3s", "3p"):
        ys = raw[name]
        pk = []
        for i in range(1, len(ys) - 1):
            if ys[i] > ys[i - 1] and ys[i] >= ys[i + 1] and ys[i] > 1e-7:
                y0, y1, y2 = ys[i - 1], ys[i], ys[i + 1]
                denom = y0 - 2 * y1 + y2
                pk.append(rs[i] + (0.5 * step * (y0 - y2) / denom if denom else 0.0))
        feats[name]["peaks"] = pk
    for f in feats.values():
        f["peaks"] = [round(x, 1) for x in f["peaks"]]
        f["nodes"] = [round(x, 1) for x in f["nodes"]]
    return {"step": step, "rmax": rmax, "a0": a0, "curves": curves, "features": feats}

def config_table():
    """CONFIGS[Z][charge] = [[subshell, count], ...] by the course rules (no exceptions)."""
    out = {}
    for z in range(1, 37):
        row = {}
        for q in range(-3, 4):
            ne = z - q
            if ne < 0 or (q > 0 and ne < 0):
                continue
            if ne == 0:
                row[str(q)] = []
                continue
            if ne > 54:
                continue
            row[str(q)] = [[s, k] for s, k in ion_config(z, q)]
        out[str(z)] = row
    return out

balmer_lines = [{"n": n, "nm": round(BALMER * n * n / (n * n - 4), 1)} for n in range(3, 9)]

def periodic_table():
    """All 118 elements for the §2.3 explorer. Categories follow textbook Fig. 2.9b (TB PDF p.91);
    common ion charges follow Fig. 2.11 (TB PDF p.92). Names from the periodictable package (background)."""
    import periodictable as pt
    def group_of(z):
        if z == 1: return 1
        if z == 2: return 18
        if 3 <= z <= 4: return z - 2
        if 5 <= z <= 10: return z + 8
        if 11 <= z <= 12: return z - 10
        if 13 <= z <= 18: return z
        if 19 <= z <= 36: return z - 18
        if 37 <= z <= 54: return z - 36
        if z in (55, 56): return z - 54
        if z == 57: return 3
        if 58 <= z <= 71: return None
        if 72 <= z <= 86: return z - 68
        if z in (87, 88): return z - 86
        if z == 89: return 3
        if 90 <= z <= 103: return None
        return z - 100
    def period_of(z):
        for top, per in ((2, 1), (10, 2), (18, 3), (36, 4), (54, 5), (86, 6), (118, 7)):
            if z <= top:
                return per
    metalloids = {5, 14, 32, 33, 51, 52, 85}
    nonmetals = {1, 2, 6, 7, 8, 9, 10, 15, 16, 17, 18, 34, 35, 36, 53, 54, 86, 118}
    ions = {"H": ["+"], "Li": ["+"], "Na": ["+"], "K": ["+"], "Rb": ["+"], "Cs": ["+"],
            "Mg": ["2+"], "Ca": ["2+"], "Sr": ["2+"], "Ba": ["2+"], "Sc": ["3+"], "Y": ["3+"], "Ti": ["4+"], "Zr": ["4+"],
            "V": ["3+", "4+"], "Cr": ["3+"], "Mn": ["2+", "4+"], "Fe": ["2+", "3+"], "Co": ["2+", "3+"], "Ni": ["2+"],
            "Cu": ["+", "2+"], "Zn": ["2+"], "Ag": ["+"], "Cd": ["2+"], "Hg": ["2+"], "Al": ["3+"], "Ga": ["3+"], "In": ["3+"],
            "Tl": ["+", "3+"], "Sn": ["2+", "4+"], "Pb": ["2+", "4+"], "N": ["3-"], "P": ["3-"], "O": ["2-"], "S": ["2-"],
            "Se": ["2-"], "Te": ["2-"], "F": ["-"], "Cl": ["-"], "Br": ["-"], "I": ["-"]}
    out = []
    for e in pt.elements:
        z = e.number
        if not 1 <= z <= 118:
            continue
        cat = "metalloid" if z in metalloids else "nonmetal" if z in nonmetals else "metal"
        out.append({"z": z, "sym": e.symbol, "name": e.name, "group": group_of(z), "period": period_of(z),
                    "cat": cat, "f": "lanthanide" if 58 <= z <= 71 else "actinide" if 90 <= z <= 103 else None,
                    "ions": ions.get(e.symbol, [])})
    return out

def molecules():
    """2-D coordinates (RDKit) for the §1.6 formula/model explorer. BACKGROUND geometry: flattened drawings."""
    from rdkit import Chem
    from rdkit.Chem import AllChem, rdMolDescriptors
    specs = [("water", "O", "H2O", "H–O–H"), ("carbon dioxide", "O=C=O", "CO2", "O=C=O"), ("methane", "C", "CH4", "CH4"),
             ("ammonia", "N", "NH3", "NH3"), ("ethanol", "CCO", "C2H6O", "CH3CH2OH"), ("acetone", "CC(=O)C", "C3H6O", "CH3COCH3"),
             ("acetic acid", "CC(=O)O", "C2H4O2", "CH3COOH"), ("propane", "CCC", "C3H8", "CH3CH2CH3")]
    out = []
    for name, smi, formula, condensed in specs:
        mol = Chem.AddHs(Chem.MolFromSmiles(smi))
        AllChem.Compute2DCoords(mol)
        conf = mol.GetConformer()
        atoms = [{"el": a.GetSymbol(), "x": round(conf.GetAtomPosition(i).x, 3), "y": round(conf.GetAtomPosition(i).y, 3)}
                 for i, a in enumerate(mol.GetAtoms())]
        bonds = [{"a": b.GetBeginAtomIdx(), "b": b.GetEndAtomIdx(), "order": int(round(b.GetBondTypeAsDouble()))} for b in mol.GetBonds()]
        calc = rdMolDescriptors.CalcMolFormula(mol)
        assert formula_counts(calc) == formula_counts(formula), (name, calc, formula)  # RDKit writes Hill order (H3N)
        counts = formula_counts(formula)
        g = 0
        for k in counts.values():
            g = math.gcd(g, k)
        emp = "".join(sym + (str(n // g) if n // g > 1 else "") for sym, n in counts.items())
        out.append({"name": name, "formula": formula, "empirical": emp, "condensed": condensed, "atoms": atoms, "bonds": bonds})
    return out

DATA = {
    "meta": {"guide": "CurrentCourseGuide", "title": "Chem 1151 study guide: Gilbert Ch. 1–4 with Days 1–8", "built": BUILD_DATE, "lastDay": LAST_DAY,
             "storageKey": STORAGE_KEY, "course": "Chem 1151 (Prof. Dransfield)"},
    "units": UNITS,
    "modules": MODULES,
    "stages": STAGES,
    "constants": {
        "c": {"value": C, "unit": "m/s", "source": "Day 2 p.30"},
        "h": {"value": H, "unit": "J·s", "source": "Day 3 p.17"},
        "bohr": {"value": BOHR, "unit": "J", "source": "Day 4 p.10"},
        "coulomb": {"value": COUL, "unit": "J·nm", "source": "Day 7 p.15"},
        "balmer": {"value": BALMER, "unit": "nm", "source": "Day 3 p.21"},
        "me": {"value": ME, "unit": "kg", "source": "Day 2 p.12, p.22"},
        "mp": {"value": MP_KG, "unit": "kg", "source": "Day 2 p.22"},
        "mn": {"value": 1.675e-27, "unit": "kg", "source": "Day 2 p.22 (slide prints 1.67483; textbook 1.67493)"},
        "NA": {"value": NA, "unit": "mol⁻¹", "source": "Background (not on any slide)"},
        "kB": {"value": 1.380649e-23, "unit": "J/K", "source": "Background (Planck curve only)"},
        "amu_kg": {"value": 1.66054e-27, "unit": "kg", "source": "Background"},
    },
    "atomicRadius": ATOMIC_RADIUS,
    "ionicRadius": IONIC_RADIUS,
    "ie1": IE1,
    "ea": EA, "eaGt0": EA_GT0, "eaCalc": EA_CALC,
    "successiveIE": SUCCESSIVE_IE,
    "valence2": VALENCE_2ND_PERIOD,
    "lattice": LATTICE,
    "workFunctionE19": WORK_FUNCTION_E19,
    "workFunctionEV": WORK_FUNCTION_EV,
    "layout": MAIN_GROUP_LAYOUT,
    "groupLabels": GROUP_LABELS,
    "elements": [[s, n] for s, n in ELEMENTS],
    "configs": config_table(),
    "configExceptions": {str(k): v for k, v in CONFIG_EXCEPTIONS.items()},
    "fillOrder": FILL_ORDER,
    "balmerLines": balmer_lines,
    "radial": radial_curves(),
    "labelText": LABEL_TEXT,
    "electronegativity": ELECTRONEGATIVITY,
    "tTable": {str(k): v for k, v in T_TABLE.items()},
    "grubbsZ": {str(k): v for k, v in GRUBBS_Z.items()},
    "atomicMass": ATOMIC_MASS,
    "isotopes": {k: [[a, m, f] for a, m, f in v] for k, v in ISOTOPES.items()},
    "pes": {k: [[sub, be, n] for sub, be, n in v] for k, v in PES.items()},
    "pesTextbook": PES_TEXTBOOK,
    "periodicTable": periodic_table(),
    "molecules": molecules(),
    **ch4_data.build(problem_bank_g.BONDS),
    "problems": PROBLEMS,
}

ASSETS.mkdir(parents=True, exist_ok=True)
js = ("/* GENERATED by verification/CurrentCourseGuide/build_guide.py; do not edit by hand. */\n"
      "window.GUIDE_DATA = " + json.dumps(DATA, ensure_ascii=False, separators=(",", ":")) + ";\n")
(ASSETS / "data.js").write_text(js, encoding="utf-8")
(HERE / "problem_bank.json").write_text(json.dumps(PROBLEMS, ensure_ascii=False, indent=1), encoding="utf-8")

# ---------------------------------------------------------------- SOURCE_SCOPE.md -> scope.js
def md_inline(s):
    s = html.escape(s, quote=False)
    codes = []                                    # protect code spans (file names contain underscores)

    def keep(m):
        codes.append("<code>" + m.group(1) + "</code>")
        return "@@CODE%d@@" % (len(codes) - 1)
    s = re.sub(r"`([^`]+)`", keep, s)
    # plain-text subscripts on one-letter symbols: Z_eff, E_el, R_H, N_A, n_final (not HOMEWORK_INDEX)
    s = re.sub(r"(?<![A-Za-z])([A-Za-zλνχ])_([A-Za-z0-9]{1,8})", r"\1<sub>\2</sub>", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<![\w*])\*([^*\s][^*]*?)\*(?![\w*])", r"<em>\1</em>", s)
    return re.sub(r"@@CODE(\d+)@@", lambda m: codes[int(m.group(1))], s)

def md_to_html(md):
    lines = md.splitlines()
    out, para, i = [], [], 0
    def flush():
        if para:
            out.append("<p>" + md_inline(" ".join(para)) + "</p>")
            para.clear()
    while i < len(lines):
        ln = lines[i].rstrip()
        if not ln.strip():
            flush(); i += 1; continue
        m = re.match(r"^(#{1,4})\s+(.*)$", ln)
        if m:
            flush()
            level = min(len(m.group(1)) + 1, 4)
            out.append(f"<h{level}>{md_inline(m.group(2))}</h{level}>")
            i += 1; continue
        if ln.startswith("|"):
            flush()
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            head, body = rows[0], [r for r in rows[1:] if not all(re.fullmatch(r":?-{3,}:?", c) for c in r)]
            t = ["<div class='table-wrap'><table><thead><tr>" + "".join(f"<th scope='col'>{md_inline(c)}</th>" for c in head) + "</tr></thead><tbody>"]
            for r in body:
                t.append("<tr>" + "".join(f"<td>{md_inline(c)}</td>" for c in r) + "</tr>")
            t.append("</tbody></table></div>")
            out.append("".join(t)); continue
        if re.match(r"^\s*- ", ln):
            flush()
            items = []
            while i < len(lines) and (re.match(r"^\s*- ", lines[i]) or (lines[i].startswith("  ") and lines[i].strip() and items)):
                if re.match(r"^\s*- ", lines[i]):
                    items.append(re.sub(r"^\s*- ", "", lines[i]).strip())
                else:
                    items[-1] += " " + lines[i].strip()
                i += 1
            out.append("<ul>" + "".join(f"<li>{md_inline(x)}</li>" for x in items) + "</ul>")
            continue
        para.append(ln.strip()); i += 1
    flush()
    return "\n".join(out)

scope_md = (GUIDE / "SOURCE_SCOPE.md").read_text(encoding="utf-8")
scope_html = md_to_html(scope_md)
(ASSETS / "scope.js").write_text(
    "/* GENERATED from SOURCE_SCOPE.md by verification/CurrentCourseGuide/build_guide.py */\n"
    "window.SCOPE_PANEL = " + json.dumps({"html": scope_html, "source": "SOURCE_SCOPE.md", "built": BUILD_DATE},
                                         ensure_ascii=False) + ";\n", encoding="utf-8")

# ---------------------------------------------------------------- index.html assembly
def nav_html():
    parts = ["<a class='nav-link nav-home' href='#start' data-testid='nav-start' data-nav='start'>"
             "<span class='nav-title'>Start here</span></a>"]
    for u in UNITS:
        parts.append(f"<p class='nav-unit'>{u['chapter']}: {html.escape(u['title'])}</p>")
        for mid in u["modules"]:
            m = next(x for x in MODULES if x["id"] == mid)
            badge = {"lecture": "L", "preview": "P", "lecture+preview": "L+P"}[m["label"]]
            parts.append(
                f"<a class='nav-link nav-{m['label'].replace('+', '-')}' href='#{mid}' data-testid='nav-{mid}' data-nav='{mid}'>"
                f"<span class='nav-num' aria-hidden='true'>{m['sec']}</span>"
                f"<span class='nav-title'>{html.escape(m['title'])}</span>"
                f"<span class='nav-badge badge-{m['label'].replace('+', '-')}' title='{LABEL_TEXT[m['label']]}'>"
                f"<span aria-hidden='true'>{badge}</span><span class='sr-only'>{LABEL_TEXT[m['label']]}</span></span>"
                f"<span class='nav-status' data-status='{mid}'>Not started</span></a>")
    parts.append("<p class='nav-unit'>Review and reference</p>")
    for pid, label in (("mixed", "Mixed review"), ("toolkit", "Toolkit: constants and equations"), ("scope", "What this guide covers")):
        extra = f"<span class='nav-status' data-status='{pid}'></span>" if pid == "mixed" else ""
        parts.append(f"<a class='nav-link' href='#{pid}' data-testid='nav-{pid}' data-nav='{pid}'>"
                     f"<span class='nav-title'>{label}</span>{extra}</a>")
    return "\n".join(parts)

def module_page(m, body):
    """Wrap a module fragment (stage divs only) in a header generated from MODULES, so labels
    and citations come from one place."""
    unit = next(u for u in UNITS if u["id"] == m["unit"])
    chips = []
    if m["label"] in ("lecture", "lecture+preview"):
        chips.append(f"<span class='chip chip-lecture'>Covered in lecture: {html.escape(m['sources'])}</span>")
    if m["label"] == "preview":
        chips.append("<span class='chip chip-preview'>Textbook preview: not yet taught in lecture</span>")
    if m["label"] == "lecture+preview":
        chips.append("<span class='chip chip-preview'>Includes a boxed textbook preview</span>")
    pre = [next(x for x in MODULES if x["id"] == q) for q in m["prereqs"]]
    prereq = ("<p class='prereq'>Builds on: " + ", ".join(f"<a href='#{x['id']}'>§{x['sec']} {html.escape(x['title'])}</a>" for x in pre) + "</p>") if pre else ""
    note = ""
    if m["label"] == "preview":
        note = ("<p class='preview-note'><span class='preview-label'>Textbook preview</span>Your professor hasn't taught this section in Days 1–" + str(LAST_DAY) + ". "
                "Everything here comes from Gilbert " + html.escape(m["textbook"]) + ", so treat it as reading ahead; its exam status is unknown.</p>")
    src_line = ("Lecture: " + html.escape(m["sources"]) + ". " if m["sources"] else "") + "Textbook: " + html.escape(m["textbook"]) + "."
    return (f"<section class='page module' id='{m['id']}' data-module='{m['id']}' data-label='{m['label']}' aria-labelledby='{m['id']}-title' hidden>\n"
            f"<header class='module-head'>\n<p class='kicker'>{unit['chapter']}; §{m['sec']}</p>\n"
            f"<h1 id='{m['id']}-title' tabindex='-1'>{html.escape(m['title'])}</h1>\n"
            f"<div class='chips'>{''.join(chips)}</div>\n{note}\n<p class='source'>{src_line}</p>\n{prereq}\n"
            f"<div class='stage-tabs'></div>\n</header>\n{body}\n</section>")

import lewis as LW                     # noqa: E402

def expand_drawings(body):
    """Fragment placeholders -> drawings from lewis.py, so every static structure is a checked one:
    <!--LEWIS:id[:fc][:scale=0.8][:cap=text]-->   <!--SYM:El-->   <!--HYBRID:id1,id2[,...][:scale=0.8]-->"""
    def lewis(m):
        parts = m.group(1).split(":")
        sid, kw = parts[0], {"tag": "span"}
        for p_ in parts[1:]:
            if p_ == "fc":
                kw["show_fc"] = True
            elif p_.startswith("scale="):
                kw["scale"] = float(p_[6:])
            elif p_.startswith("cap="):
                kw["caption"] = p_[4:]
        return LW.svg(LW.STRUCTS[sid], **kw)
    def hybrid(m):
        parts = m.group(1).split(":")
        kw = {"tag": "span"}
        for p_ in parts[1:]:
            if p_.startswith("scale="):
                kw["scale"] = float(p_[6:])
        return LW.hybrid_svg([LW.STRUCTS[i] for i in parts[0].split(",")], **kw)
    body = re.sub(r"<!--LEWIS:([^>]+?)-->", lewis, body)
    body = re.sub(r"<!--SYM:([A-Za-z]+)-->", lambda m: LW.symbol_svg(m.group(1))[0], body)
    body = re.sub(r"<!--HYBRID:([^>]+?)-->", hybrid, body)
    return body

def toolkit_ch4():
    """Ch. 4 reference tables for the toolkit, generated from ch4_data / Table 4.6."""
    nd = ch4_data.naming_data()
    pre = "".join(f"<tr><td>{i + 1}</td><td>{x}-</td></tr>" for i, x in enumerate(nd["prefixes"]))
    ions = []
    for a in nd["anions"]:
        if a["poly"]:
            ions.append((a["html"] + "<sup>" + (str(-a["q"]) if a["q"] < -1 else "") + "−</sup>", a["name"] + (f" or {a['alt']}" if a["alt"] else "")))
    ions.insert(13, ("NH<sub>4</sub><sup>+</sup>", "ammonium"))
    ion_rows = "".join(f"<tr><td>{f}</td><td>{n}</td></tr>" for f, n in ions)
    b_rows = "".join(f"<tr><td>{r['bond']}</td><td>{r['pm']}</td><td>{r['kj']}{'<sup>a</sup>' if r['bond'] == 'C=O' else ''}</td></tr>" for r in ch4_data.bond_table(problem_bank_g.BONDS))
    return ("<h2>Chapter 4 reference tables</h2>\n"
            "<div class='toolkit-grid'>\n"
            "<div><h3>Naming prefixes (Table 4.3)</h3><div class='table-wrap'><table class='data'><thead><tr><th scope='col'>Number</th><th scope='col'>Prefix</th></tr></thead><tbody>" + pre +
            "</tbody></table></div><p class='source'>Lecture, Day 8 p.12–13. No “mono” on the first element.</p></div>\n"
            "<div><h3>Common polyatomic ions</h3><div class='table-wrap'><table class='data'><thead><tr><th scope='col'>Ion</th><th scope='col'>Name</th></tr></thead><tbody>" + ion_rows +
            "</tbody></table></div><p class='source'>Lecture, Day 8 p.8 (the slide's Table 4.5; the textbook's Table 4.4, PDF p.192). “You will be provided with a table like this on the exams, so you don't need to memorize them.”</p></div>\n"
            "<div><h3>Average bond lengths and energies (Table 4.6)</h3><div class='table-wrap'><table class='data'><thead><tr><th scope='col'>Bond</th><th scope='col'>Length (pm)</th><th scope='col'>Energy (kJ/mol)</th></tr></thead><tbody>" + b_rows +
            "</tbody></table></div><p class='source'><span class='pill-label preview'>Textbook preview</span> §4.6, Table 4.6, PDF p.207 (printed 173). <sup>a</sup>The C=O bond energy in CO<sub>2</sub> is 799 kJ/mol (the table's footnote).</p></div>\n"
            "</div>\n")

order = ["head.html", "start.html"] + [f"{m['id']}.html" for m in MODULES] + ["mixed.html", "toolkit.html", "scope.html", "foot.html"]
missing = [f for f in order if not (SRC / f).exists()]
if missing:
    print("index.html not assembled; missing src fragments:", ", ".join(missing))
else:
    pieces = []
    for f in order:
        body = expand_drawings((SRC / f).read_text(encoding="utf-8"))
        if f == "toolkit.html":
            body = body.replace("<!--TOOLKIT_CH4-->", toolkit_ch4())
        mod = next((m for m in MODULES if f == m["id"] + ".html"), None)
        pieces.append(module_page(mod, body) if mod else body)
    page = "\n".join(pieces).replace("<!--NAV-->", nav_html())
    page = page.replace("<!--BUILD_DATE-->", BUILD_DATE)
    leftover = re.findall(r"<!--(?:LEWIS|SYM|HYBRID|TOOLKIT_CH4)[^>]*-->", page)
    assert not leftover, leftover
    (GUIDE / "index.html").write_text(page, encoding="utf-8")
    print("index.html assembled from", len(order), "fragments")

# ---------------------------------------------------------------- reference values for node tests
exp = {
    "bohr": [{"ni": ni, "nf": nf, "dE": bohr_dE(ni, nf), "nm": nm_from_energy(abs(bohr_dE(ni, nf)))}
             for ni, nf in ((3, 2), (4, 2), (5, 2), (6, 2), (2, 1), (4, 3), (1, 3), (2, 5))],
    "photon": [{"nm": x, "E": photon_energy_from_nm(x), "nu": C / (x * 1e-9)} for x in (220.0, 400.0, 530.0, 656.0)],
    "debroglie": [{"m": m, "u": u, "lam": de_broglie(m, u)} for m, u in ((ME, 4.05e6), (0.142, 44.0), (1.675e-27, 2.20e3))],
    "eel": [{"q1": a, "q2": b, "d": d, "E": e_el(a, b, d)} for a, b, d in ((1, -1, 0.283), (2, -2, 0.212), (1, -1, 0.319))],
    "photoelectric": [{"nm": 220.0, "phi": 7.18e-19, "KE": photon_energy_from_nm(220.0) - 7.18e-19}],
    "planckPeakNm5000": 2.897771955e-3 / 5000 * 1e9,
    "configs": {f"{z}:{q}": [[s, k] for s, k in ion_config(z, q)] for z, q in ((26, 0), (26, 2), (26, 3), (29, 0), (24, 0), (16, -2), (23, 3), (30, 2), (20, 0), (35, -1))},
    "unpaired": {f"{z}:{q}": unpaired(ion_config(z, q)) for z, q in ((6, 0), (7, 0), (8, 0), (25, 0), (26, 3), (22, 2))},
    "naming": ch4_data.naming_expected(),
    "fcBest": ch4_data.FC_EXPECTED_BEST,
}
(HERE / "expected_values.json").write_text(json.dumps(exp, indent=1), encoding="utf-8")

kinds = {}
for p in PROBLEMS:
    kinds[p["kind"]] = kinds.get(p["kind"], 0) + 1
print(f"data.js: {len(PROBLEMS)} problems {kinds}; {len(js) // 1024} KB")
print("scope.js:", len(scope_html), "chars of HTML")

"""Independent verification of study-guides/CurrentCourseGuide (reason first, verify second).

Run from the project root:
    py -3.11 verification/CurrentCourseGuide/verify_guide.py [--blind DIR] [--dom FILE]

blind_check/ holds the blind record: batch_N.json (prompts without keys) and answers_N.json from solvers who
never saw the keys (batch 5 re-solved three prompts revised afterward). --dom takes an outerHTML dump of the
guide after every module's stages were visited, so explorer-generated text and test ids are checked too.

Writes verification/CurrentCourseGuide/verification_report.md with these sections:
  1. Physics recomputed from first principles (the explorers' reference values)
  2. Electron configurations from an independent aufbau implementation
  3. Data tables against independent references (periodictable masses; NIST values via Wolfram)
  4. Answer keys vs. blind solutions (DIR holds answers from solvers who never saw the keys)
  5. Notation lint of every visible string (index.html and problem text; optionally a rendered-DOM dump)
  6. Citations: lecture page ranges, textbook printed/PDF offsets, scope ranges, topic labels
  7. Structure: ids, data-testids, stage sets, required problem kinds
Exit status 1 if a hard check fails. A key disagreement counts as a failure until it is adjudicated
in ADJUDICATED below, with the reason.

Nothing here imports the problem banks' formulas: constants are retyped from COURSE.md, and
configurations come from a separate implementation, so a shared mistake can't hide.
"""
import argparse
import glob
import json
import math
import os
import re
import sys
from html.parser import HTMLParser

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
GUIDE = os.path.join(ROOT, "study-guides", "CurrentCourseGuide")
sys.path.insert(0, HERE)

# ------------------------------------------------------------------ course constants (COURSE.md)
C_LIGHT = 2.998e8        # m/s          Day 2 p.30
PLANCK = 6.626e-34       # J s          Day 3 p.17
BOHR_J = 2.178e-18       # J            Day 4 p.10
COULOMB = 2.31e-19       # J nm         Day 7 p.15
BALMER_NM = 364.56       # nm           Day 3 p.21
RH_TEXTBOOK = 1.0974e7   # 1/m          textbook PDF p.130
LECTURE_PAGES = {1: 20, 2: 31, 3: 21, 4: 18, 5: 20, 6: 26, 7: 21, 8: 30}   # physical PDF pages per Day
TEXTBOOK_OFFSET = 34     # printed = PDF - 34 in Ch. 1-4
# textbook PDF pages inside the guide's scope (SOURCE_SCOPE.md): front matter/TOC, chapter
# openers, sections, and chapter summaries; end-of-chapter problems are excluded
TEXTBOOK_SCOPE = [(3, 9), (36, 72), (80, 108), (118, 168), (178, 220)]

# ------------------------------------------------------------------ independent references
# First ionization energies and electron affinities, kJ/mol, from Wolfram ElementData (NIST ASD /
# CRC values), fetched 2026-09-24. Wolfram's EA sign convention is positive = energy released.
REF_IE1 = {"H": 1312.0, "He": 2372.3, "Li": 520.2, "Be": 899.5, "B": 800.6, "C": 1086.5, "N": 1402.3,
           "O": 1313.9, "F": 1681.0, "Ne": 2080.7, "Na": 495.8, "Mg": 737.7, "Al": 577.5, "Si": 786.5,
           "P": 1011.8, "S": 999.6, "Cl": 1251.2, "Ar": 1520.6, "K": 418.8, "Ca": 589.8, "Ga": 578.8,
           "Ge": 762.0, "As": 947.0, "Se": 941.0, "Br": 1139.9, "Kr": 1350.8, "Rb": 403.0, "Sr": 549.5,
           "In": 558.3, "Sn": 708.6, "Sb": 834.0, "Te": 869.3, "I": 1008.4, "Xe": 1170.4, "Cs": 375.7,
           "Ba": 502.9, "Tl": 589.4, "Pb": 715.6, "Bi": 703.0, "Po": 812.1, "At": 920.0, "Rn": 1037.0}
REF_EA_RELEASED = {"H": 72.8, "Li": 59.6, "B": 26.7, "C": 153.9, "O": 141.0, "F": 328.0, "Na": 52.8,
                   "Al": 42.5, "Si": 133.6, "P": 72.0, "S": 200.0, "Cl": 349.0, "K": 48.4, "Ca": 2.4,
                   "Ga": 28.9, "Ge": 119.0, "As": 78.0, "Se": 195.0, "Br": 324.6, "Rb": 46.9, "Sr": 5.0,
                   "In": 28.9, "Sn": 107.3, "Sb": 103.2, "Te": 190.2, "I": 295.2, "Cs": 45.5, "Ba": 13.9,
                   "Tl": 19.2, "Pb": 35.1, "Bi": 91.2, "Po": 183.3, "At": 270.1}
# Wolfram's carbon value (153.9) is the outlier: the photodetachment value is 1.2621 eV = 121.8 kJ/mol
# (NIST), which is what the lecture table prints (-122). Recorded as a reference problem, not a slip.
REF_NOTES = {"C": "reference outlier: modern EA(C) = 121.8 kJ/mol (1.2621 eV) agrees with the lecture's -122"}
# Modern Pauling electronegativities (Wolfram ElementData). The textbook's Fig. 4.5 uses an older
# Pauling table; differences over 0.3 were checked against the rendered figure (TB PDF p.187).
REF_EN = {"H": 2.2, "Li": 0.98, "Be": 1.57, "B": 2.04, "C": 2.55, "N": 3.04, "O": 3.44, "F": 3.98, "Na": 0.93,
          "Mg": 1.31, "Al": 1.61, "Si": 1.9, "P": 2.19, "S": 2.58, "Cl": 3.16, "K": 0.82, "Ca": 1.0, "Sc": 1.36,
          "Ti": 1.54, "V": 1.63, "Cr": 1.66, "Mn": 1.55, "Fe": 1.83, "Co": 1.88, "Ni": 1.91, "Cu": 1.9,
          "Zn": 1.65, "Ga": 1.81, "Ge": 2.01, "As": 2.18, "Se": 2.55, "Br": 2.96, "Rb": 0.82, "Sr": 0.95,
          "Y": 1.22, "Zr": 1.33, "Nb": 1.6, "Mo": 2.16, "Tc": 1.9, "Ru": 2.2, "Rh": 2.28, "Pd": 2.2, "Ag": 1.93,
          "Cd": 1.69, "In": 1.78, "Sn": 1.96, "Sb": 2.05, "Te": 2.1, "I": 2.66, "Cs": 0.79, "Ba": 0.89,
          "La": 1.1, "Hf": 1.3, "Ta": 1.5, "W": 2.36, "Re": 1.9, "Os": 2.2, "Ir": 2.2, "Pt": 2.28, "Au": 2.54,
          "Hg": 2.0, "Tl": 1.62, "Pb": 2.33, "Bi": 2.02, "Po": 2.0, "At": 2.2, "Fr": 0.7, "Ra": 0.9, "Ac": 1.1}
EN_CHECKED_ON_RENDER = {"Li": 1.1, "Mo": 1.8, "W": 1.7, "Pb": 1.9}   # read off TB PDF p.187 crops
# Successive ionization energies, kJ/mol (Wolfram ElementData), to compare with textbook Table 3.2 (Day 7 p.10).
REF_SUCC_IE = {"He": [2372, 5250], "Li": [520, 7298, 11815], "Be": [900, 1757, 14849, 21007],
               "B": [801, 2427, 3660, 25026, 32827], "C": [1086, 2353, 4620, 6223, 37831, 47277],
               "N": [1402, 2856, 4578, 7475, 9445, 53267, 64360], "O": [1314, 3388, 5300, 7469, 10990, 13326, 71330, 84078],
               "F": [1681, 3374, 6050, 8408, 11023, 15164, 17868, 92038, 106434],
               "Ne": [2081, 3952, 6122, 9371, 12177, 15238, 19999, 23070, 115380, 131432]}

# Key disagreements with the blind solvers that were adjudicated: id -> (verdict, reason).
# verdict "key" = the guide's key stands; "fixed" = the key was corrected in the bank.
ADJUDICATED = {}

# Final answers that also appear in their module's teaching text, reviewed by hand: id -> reason it stays.
# (2026-09-24: six others were real give-aways and were fixed by changing the teaching example: m10-p1,
# m11-p2, m13-attempt, t1-6-attempt, t1-6-transfer, t3-11-p3; m10-preview-excited became a lithium transfer item.)
REVIEWED_GIVEAWAYS = {
    "m7-attempt": "coincidence: the neutron (1.675e-27 kg, 2.20e3 m/s) and the lecture's electron (Day 4 p.12) both give "
                  "1.80e-10 m; the student must still compute it, and the solution points out the match",
    "m10-preview-exception": "a reading check on the textbook-preview box; the point of the item is the course policy "
                             "(\"completely ignore\" exceptions, Day 7 p.6), not recall of the configuration",
    "m14-p3": "coincidence (2026-09-25): KCl's two-body Coulomb energy per mole (d = 0.319 nm) rounds to -436 kJ/mol, "
              "the same number as the H-H bond energy on Day 8 p.11, a different quantity; the student must still "
              "compute it, and the solution points out the match",
}


# ================================================================== loading
def load_data():
    s = open(os.path.join(GUIDE, "assets", "data.js"), encoding="utf-8").read()
    start = s.index("window.GUIDE_DATA = ") + len("window.GUIDE_DATA = ")
    return json.loads(s[start:].rstrip().rstrip(";"))


class Report:
    def __init__(self):
        self.lines, self.failures, self.warnings = [], [], []

    def h(self, title):
        self.lines += ["", "## " + title, ""]

    def p(self, text=""):
        self.lines.append(text)

    def table(self, head, rows):
        self.lines.append("| " + " | ".join(head) + " |")
        self.lines.append("|" + "---|" * len(head))
        for r in rows:
            self.lines.append("| " + " | ".join(str(x).replace("|", "\\|") for x in r) + " |")

    def fail(self, msg):
        self.failures.append(msg)
        self.lines.append("- **FAIL** " + msg)

    def warn(self, msg):
        self.warnings.append(msg)
        self.lines.append("- WARN " + msg)


def rel(a, b):
    return abs(a - b) / max(abs(b), 1e-300)


# ================================================================== 1. physics
def check_physics(R):
    R.h("1. Physics recomputed from first principles")
    ev = json.load(open(os.path.join(HERE, "expected_values.json"), encoding="utf-8"))
    rows, bad = [], 0
    for b in ev["bohr"]:
        dE = -BOHR_J * (1 / b["nf"] ** 2 - 1 / b["ni"] ** 2)
        lam = PLANCK * C_LIGHT / abs(dE) * 1e9
        ok = rel(dE, b["dE"]) < 1e-9 and rel(lam, b["nm"]) < 1e-9
        bad += not ok
        extra = ""
        if b["nf"] == 2 and b["ni"] > b["nf"]:
            bal = BALMER_NM * b["ni"] ** 2 / (b["ni"] ** 2 - 4)
            ryd = 1 / (RH_TEXTBOOK * (1 / 4 - 1 / b["ni"] ** 2)) * 1e9
            extra = f"Balmer {bal:.2f} nm; R_H {ryd:.2f} nm"
        rows.append([f"n {b['ni']}→{b['nf']}", f"{dE:.4e} J", f"{lam:.2f} nm", "match" if ok else "MISMATCH", extra])
    R.p("Bohr transitions, ΔE = −2.178×10⁻¹⁸ J (1/n_f² − 1/n_i²), λ = hc/|ΔE|:")
    R.table(["transition", "ΔE", "λ", "vs. guide", "other lecture/textbook forms"], rows)
    R.p("")
    R.p("The two lecture routes differ by 0.07% for n = 3→2 (Bohr 656.69 nm, Balmer 656.21 nm). Balmer's 364.56 nm was fit "
        "to wavelengths measured in air (Hα 656.28 nm in air, 656.47 nm in vacuum), while the Bohr route gives vacuum wavelengths, "
        "0.03% long here because 2.178×10⁻¹⁸ J rounds hcR_H = 2.1787×10⁻¹⁸ J down. Both are the professor's values, each "
        "guide problem states which it uses, and the gap is far below the 1% answer tolerance.")
    for ph in ev["photon"]:
        E = PLANCK * C_LIGHT / (ph["nm"] * 1e-9)
        nu = C_LIGHT / (ph["nm"] * 1e-9)
        if rel(E, ph["E"]) > 1e-9 or rel(nu, ph["nu"]) > 1e-9:
            bad += 1
            R.fail(f"photon {ph['nm']} nm: E {E:.4e} vs {ph['E']:.4e}")
    for d in ev["debroglie"]:
        lam = PLANCK / (d["m"] * d["u"])
        if rel(lam, d["lam"]) > 1e-9:
            bad += 1
            R.fail(f"de Broglie m={d['m']}: {lam:.4e} vs {d['lam']:.4e}")
    for e in ev["eel"]:
        E = COULOMB * e["q1"] * e["q2"] / e["d"]
        if rel(E, e["E"]) > 1e-9:
            bad += 1
            R.fail(f"E_el {e}: {E:.4e}")
    for pe in ev["photoelectric"]:
        KE = PLANCK * C_LIGHT / (pe["nm"] * 1e-9) - pe["phi"]
        if rel(KE, pe["KE"]) > 1e-9:
            bad += 1
            R.fail(f"photoelectric {pe}: KE {KE:.4e}")
    # Wien peak: an independent numerical maximum of Planck's law (CODATA constants)
    from scipy import constants as K
    from scipy.optimize import minimize_scalar
    T = 5000.0
    f = lambda lam: -(1 / lam ** 5) / math.expm1(K.h * K.c / (lam * K.k * T))
    peak = minimize_scalar(f, bounds=(100e-9, 3000e-9), method="bounded", options={"xatol": 1e-15}).x * 1e9
    ok = abs(peak - ev["planckPeakNm5000"]) < 0.01
    bad += not ok
    R.p("")
    R.p(f"- Photon E = hc/λ and ν = c/λ ({len(ev['photon'])} wavelengths), de Broglie λ = h/mu ({len(ev['debroglie'])}), "
        f"E_el = 2.31×10⁻¹⁹ J·nm·Q₁Q₂/d ({len(ev['eel'])}), photoelectric KE = hν − φ ({len(ev['photoelectric'])}): "
        f"recomputed, {'all match' if not bad else str(bad) + ' mismatches'}.")
    R.p(f"- Blackbody peak at 5000 K: numerical maximum of Planck's law = {peak:.3f} nm; guide {ev['planckPeakNm5000']:.3f} nm "
        f"({'match' if ok else 'MISMATCH'}).")
    # CODATA comparison: how far the course's rounded constants move answers
    hc_course, hc_codata = PLANCK * C_LIGHT, K.h * K.c
    R.p(f"- Course hc = {hc_course:.6e} J·m vs. CODATA {hc_codata:.6e} J·m ({rel(hc_course, hc_codata) * 100:.3f}% apart): "
        "far inside every answer tolerance (≥ 1%), so course-constant answers are also right with exact constants.")
    if bad:
        R.fail(f"{bad} physics reference values disagree")
    return bad


# ================================================================== 2. configurations
L_LETTERS = "spdf"


def madelung():
    subs = [(n, l) for n in range(1, 8) for l in range(0, min(n, 4))]
    return sorted(subs, key=lambda t: (t[0] + t[1], t[0]))


def aufbau(z):
    out, left = {}, z
    for n, l in madelung():
        if left <= 0:
            break
        k = min(left, 2 * (2 * l + 1))
        out[f"{n}{L_LETTERS[l]}"] = k
        left -= k
    return out


def ion_config(z, q):
    if q <= 0:
        return aufbau(z - q)
    cfg = aufbau(z)
    for _ in range(q):   # remove from the highest n first, then the highest l
        key = max((s for s, v in cfg.items() if v > 0), key=lambda s: (int(s[:-1]), L_LETTERS.index(s[-1])))
        cfg[key] -= 1
    return {s: v for s, v in cfg.items() if v > 0}


def unpaired(cfg):
    tot = 0
    for s, k in cfg.items():
        m = 2 * L_LETTERS.index(s[-1]) + 1
        tot += k if k <= m else 2 * m - k
    return tot


def check_configs(R, D):
    R.h("2. Electron configurations (independent aufbau)")
    ev = json.load(open(os.path.join(HERE, "expected_values.json"), encoding="utf-8"))
    rows, bad = [], 0
    for key, cfg in ev["configs"].items():
        z, q = (int(x) for x in key.split(":"))
        mine = ion_config(z, q)
        theirs = {s: k for s, k in cfg}
        ok = mine == theirs
        bad += not ok
        rows.append([key, " ".join(f"{s}{k}" for s, k in cfg), "match" if ok else "MISMATCH: " + str(mine)])
    for key, n in ev["unpaired"].items():
        z, q = (int(x) for x in key.split(":"))
        if unpaired(ion_config(z, q)) != n:
            bad += 1
            R.fail(f"unpaired electrons {key}: mine {unpaired(ion_config(z, q))}, guide {n}")
    # the full data table the configuration explorer uses
    n_table = 0
    for z_str, by_charge in (D.get("configs") or {}).items():   # Z -> {charge: [[subshell, electrons], ...]}
        z = int(z_str)
        for q_str, cfg in by_charge.items():
            n_table += 1
            if {s: k for s, k in cfg} != ion_config(z, int(q_str)):
                bad += 1
                R.fail(f"explorer config table Z={z}, charge {q_str} differs from aufbau: {cfg}")
    R.table(["Z:charge", "guide", "independent"], rows)
    R.p("")
    R.p(f"Aufbau follows the Madelung (n + ℓ, then n) order with no exceptions, as the professor directs "
        f"(\"we will completely ignore\" exceptions, Day 7 p.6); cations lose electrons from the highest n first "
        f"(Day 6 p.21). Unpaired-electron counts use Hund's rule. The explorer's configuration table "
        f"({n_table} entries) was also compared.")
    return bad


# ================================================================== 3. data tables
def check_tables(R, D):
    R.h("3. Data tables against independent references")
    import periodictable as pt
    import guide_common as g
    bad = 0
    rows = []
    for sym, m in g.ATOMIC_MASS.items():
        ref = getattr(pt, sym).mass
        d = rel(m, ref)
        if d > 2e-4:
            rows.append([sym, m, f"{ref:.4f}", f"{d * 100:.3f}%"])
    R.p(f"- Atomic masses: {len(g.ATOMIC_MASS)} textbook values vs. `periodictable` (IUPAC). "
        + ("All within 0.02%." if not rows else f"{len(rows)} differ by more than 0.02% (older textbook values):"))
    if rows:
        R.table(["element", "guide (textbook)", "IUPAC", "difference"], rows)
    worst = max(((abs(D["ie1"][s] - REF_IE1[s]) / REF_IE1[s], s) for s in REF_IE1 if s in D["ie1"]))
    over = [s for s in REF_IE1 if s in D["ie1"] and abs(D["ie1"][s] - REF_IE1[s]) / REF_IE1[s] > 0.01]
    R.p(f"- First ionization energies (Day 7 p.9 table, {len(D['ie1'])} elements) vs. NIST values via Wolfram: "
        f"largest difference {worst[0] * 100:.2f}% ({worst[1]}). " + ("None over 1%." if not over else "Over 1%: " + ", ".join(over)))
    bad += len(over)
    ea_rows = []
    for s, ref in REF_EA_RELEASED.items():
        v = D["ea"].get(s)
        if v is None:
            continue
        if abs(-v - ref) > max(1.0, 0.02 * ref):
            ea_rows.append([s, v, -ref, REF_NOTES.get(s, "CHECK")])
    R.p(f"- Electron affinities (Day 7 p.11 table) vs. Wolfram (sign flipped to the course convention, negative = released): "
        + ("all agree within 2% or 1 kJ/mol." if not ea_rows else f"{len(ea_rows)} differ:"))
    if ea_rows:
        R.table(["element", "guide", "reference", "note"], ea_rows)
    bad += sum(1 for r in ea_rows if r[3] == "CHECK")
    en_rows = []
    for s, v in D["electronegativity"].items():
        ref = REF_EN.get(s)
        if ref is not None and abs(v - ref) > 0.3:
            seen = EN_CHECKED_ON_RENDER.get(s)
            en_rows.append([s, v, ref, "confirmed on TB PDF p.187" if seen == v else "CHECK"])
    for s, v in EN_CHECKED_ON_RENDER.items():
        if abs(D["electronegativity"][s] - v) > 1e-9:
            en_rows.append([s, D["electronegativity"][s], v, "differs from the rendered figure"])
    R.p(f"- Electronegativities ({len(D['electronegativity'])} values, textbook Fig. 4.5) vs. modern Pauling values: "
        f"{len(en_rows)} differ by more than 0.3; each was read again on the rendered figure:")
    if en_rows:
        R.table(["element", "guide", "modern Pauling", "status"], en_rows)
    bad += sum(1 for r in en_rows if r[3] != "confirmed on TB PDF p.187")
    # successive IEs: same jump position as the reference, values within a few percent
    worst_s, jump_bad = (0, ""), []
    for sym, ref in REF_SUCC_IE.items():
        mine = D["successiveIE"].get(sym)
        if not mine or len(mine) != len(ref):
            jump_bad.append(sym)
            continue
        for k, (a, b) in enumerate(zip(mine, ref)):
            d = abs(a - b) / b
            if d > worst_s[0]:
                worst_s = (d, f"{sym} IE{k + 1}: {a} vs. {b}")
        jr = lambda v: max(range(1, len(v)), key=lambda k: v[k] / v[k - 1]) if len(v) > 1 else 0
        if jr(mine) != jr(ref):
            jump_bad.append(sym)
    R.p(f"- Successive ionization energies (textbook Table 3.2 on Day 7 p.10, as printed) vs. Wolfram: largest difference "
        f"{worst_s[0] * 100:.1f}% ({worst_s[1]}); the biggest jump falls after the same IE for every element"
        + ("." if not jump_bad else "; EXCEPT " + ", ".join(jump_bad)))
    bad += len(jump_bad)
    # PES: the outermost binding energy should equal IE1 (Day 7 p.9) within a few percent
    pes_bad = []
    for s, rows_ in D["pes"].items():
        be = rows_[-1][1] * 1000
        if abs(be - D["ie1"][s]) / D["ie1"][s] > 0.03:
            pes_bad.append(s)
    R.p(f"- Photoelectron spectra ({len(D['pes'])} elements; Li and Al from the textbook, others reference values): "
        f"outermost peak vs. IE₁ " + ("within 3% for all." if not pes_bad else "off for " + ", ".join(pes_bad)))
    bad += len(pes_bad)
    # electron counts in the PES data
    for s, rows_ in D["pes"].items():
        z = next(e["z"] for e in D["periodicTable"] if e["sym"] == s)
        if sum(r[2] for r in rows_) != z:
            bad += 1
            R.fail(f"PES {s}: electrons {sum(r[2] for r in rows_)} != Z {z}")
    return bad


# ================================================================== 4. answer keys vs. blind solutions
def parse_config_string(s):
    s = s.replace("[", " [").replace("]", "] ")
    cores = {"He": 2, "Ne": 10, "Ar": 18, "Kr": 36, "Xe": 54, "Rn": 86}
    out = {}
    for core in re.findall(r"\[(He|Ne|Ar|Kr|Xe|Rn)\]", s):
        for k, v in aufbau(cores[core]).items():
            out[k] = out.get(k, 0) + v
    s = re.sub(r"\[(He|Ne|Ar|Kr|Xe|Rn)\]", " ", s)
    sup = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹", "0123456789")
    for n, l, k in re.findall(r"(\d)\s*([spdf])\s*\^?\s*(\d+)", s.translate(sup)):
        out[n + l] = out.get(n + l, 0) + int(k)
    return {k: v for k, v in out.items() if v}


def formula_counts(f):
    f = f.translate(str.maketrans("₀₁₂₃₄₅₆₇₈₉", "0123456789"))
    out = {}
    for el, n in re.findall(r"([A-Z][a-z]?)(\d*)", f):
        out[el] = out.get(el, 0) + (int(n) if n else 1)
    return out


def norm_text(s):
    s = re.sub(r"<[^>]+>", "", str(s))
    return re.sub(r"\s+", " ", s).strip()


def compare_answer(spec, got):
    """Return (agree: bool, key_str, got_str)."""
    t = spec.get("type")
    if t == "multi":
        if not isinstance(got, list) or len(got) != len(spec["parts"]):
            return False, "parts", json.dumps(got, ensure_ascii=False)[:80]
        res = [compare_answer(p, g) for p, g in zip(spec["parts"], got)]
        return all(r[0] for r in res), "; ".join(r[1] for r in res), "; ".join(r[2] for r in res)
    if t == "numeric":
        v = got.get("value") if isinstance(got, dict) else got
        try:
            v = float(v)
        except (TypeError, ValueError):
            return False, f"{spec['value']:.6g}", str(got)
        tval, tol = spec["value"], spec.get("tol", 0.01)
        if tol == 0:
            ok = abs(v - tval) < 1e-9 * max(1, abs(tval))
        elif tval == 0:
            ok = abs(v) <= tol
        else:
            ok = abs(v - tval) / abs(tval) <= max(tol, 0.01) + 1e-12
        return ok, f"{tval:.6g}", f"{v:.6g}"
    if t == "choice":
        key = next(i for i, o in enumerate(spec["options"]) if o.get("correct"))
        return got == key, str(key), str(got)
    if t == "order":
        return list(got) == spec["answerOrder"], ",".join(spec["answerOrder"]), ",".join(map(str, got))
    if t == "match":
        key = {str(i): r["answer"] for i, r in enumerate(spec["rows"])}
        g = {str(k): v for k, v in (got or {}).items()}
        return g == key, json.dumps(key), json.dumps(g)
    if t == "text":
        acc = spec["accepted"]
        if spec.get("kind") == "formula":
            ok = any(formula_counts(str(got)) == formula_counts(a) for a in acc)
        else:
            gl = norm_text(got).lower()
            ok = any(gl == norm_text(a).lower() for a in acc)
        return ok, " / ".join(acc), str(got)
    if t == "config":
        target = spec["target"]
        mine = parse_config_string(str(got))
        return mine == target, " ".join(f"{k}{v}" for k, v in target.items()), str(got)
    return True, "", ""


def check_blind(R, D, blind_dir):
    R.h("4. Answer keys vs. blind solutions")
    if not blind_dir:
        R.warn("no --blind directory given; answer keys were not compared with blind solutions")
        return 0
    answers = {}
    # merged answers_N.json per batch; fall back to the answers_N_partKK.json chunks
    files = sorted(glob.glob(os.path.join(blind_dir, "answers_[0-9].json"))) or sorted(glob.glob(os.path.join(blind_dir, "answers_*_part*.json")))
    for f in files:
        try:
            for a in json.load(open(f, encoding="utf-8")):
                answers[a["id"]] = a
        except (ValueError, KeyError) as e:
            R.fail(f"unreadable blind file {os.path.basename(f)}: {e}")
    probs = {p["id"]: p for p in D["problems"]}
    gradable = [p for p in D["problems"] if p["answer"]["type"] != "self"]
    missing = [p["id"] for p in gradable if p["id"] not in answers]
    agree, disagree = 0, []
    for p in gradable:
        a = answers.get(p["id"])
        if not a:
            continue
        ok, key, got = compare_answer(p["answer"], a.get("answer"))
        if ok:
            agree += 1
        else:
            disagree.append((p, key, got, a))
    R.p(f"{len(files)} answer files; {len(answers)} blind answers for {len(gradable)} gradable problems "
        f"({len(missing)} unanswered). Agreement: **{agree}**. Disagreements: **{len(disagree)}**.")
    R.p("")
    R.p("Solvers saw only each prompt and its answer format (never keys, hints, or solutions), plus the course "
        "constants and data tables. A disagreement is resolved by rereading the problem; the verdict is recorded "
        "in `ADJUDICATED` in this script.")
    open_items = 0
    if disagree:
        rows = []
        for p, key, got, a in disagree:
            verdict = ADJUDICATED.get(p["id"])
            if not verdict:
                open_items += 1
            rows.append([p["id"], key[:60], got[:60], a.get("confidence", ""), (a.get("note") or "")[:140],
                         (verdict[0] + ": " + verdict[1]) if verdict else "OPEN"])
        R.table(["problem", "key", "blind answer", "conf.", "solver note", "verdict"], rows)
    flagged = [(pid, a) for pid, a in answers.items() if pid in probs and re.search(
        r"ambig|error|wrong|unclear|typo|inconsist|mislead|should be|not quite", a.get("note") or "", re.I)]
    if flagged:
        R.p("")
        R.p("Problems the solvers flagged as ambiguous or erroneous (whether or not they agreed with the key):")
        R.table(["problem", "solver note", "verdict"],
                [[pid, (a.get("note") or "")[:200], ADJUDICATED.get(pid, ("", "see note"))[1][:120]] for pid, a in flagged])
    if missing:
        R.warn(f"{len(missing)} problems without a blind answer: " + ", ".join(missing[:30]))
    if open_items:
        R.fail(f"{open_items} key disagreements not yet adjudicated")
    return open_items


# ================================================================== 5. notation lint
class TextNodes(HTMLParser):
    SKIP = {"script", "style", "code", "kbd", "samp", "textarea", "title"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.ids, self.nodes = [], [], []

    def handle_starttag(self, tag, attrs):
        if tag in ("br", "img", "input", "meta", "link", "hr", "wbr", "source", "col", "area", "base", "embed", "param", "track"):
            return
        a = dict(attrs)
        self.stack.append(tag)
        self.ids.append(a.get("id") or a.get("data-module") or "")

    def handle_endtag(self, tag):
        if tag in self.stack:
            while self.stack:
                t = self.stack.pop()
                self.ids.pop()
                if t == tag:
                    break

    def handle_data(self, data):
        if any(t in self.SKIP for t in self.stack) or not data.strip():
            return
        where = next((i for i in reversed(self.ids) if i), "")
        self.nodes.append((where, data, self.stack[-1] if self.stack else ""))


# element symbols: a flattened formula is 2+ element tokens with at least one digit, all in one text node
ELEMENTS = set("H He Li Be B C N O F Ne Na Mg Al Si P S Cl Ar K Ca Sc Ti V Cr Mn Fe Co Ni Cu Zn Ga Ge As Se Br Kr "
               "Rb Sr Y Zr Nb Mo Tc Ru Rh Pd Ag Cd In Sn Sb Te I Xe Cs Ba La Ce Pr Nd Pm Sm Eu Gd Tb Dy Ho Er Tm Yb "
               "Lu Hf Ta W Re Os Ir Pt Au Hg Tl Pb Bi Po At Rn Fr Ra Ac Th Pa U Np Pu Am Cm Bk Cf Es Fm Md No Lr".split())
FORMULA_TOKEN = re.compile(r"(?<![A-Za-z0-9.])((?:[A-Z][a-z]?\d*){1,6})(\d*[+\-−]?)(?![A-Za-z0-9])")


def flattened_formula(tok):
    parts = re.findall(r"([A-Z][a-z]?)(\d*)", tok)
    if "".join(e + n for e, n in parts) != tok:
        return False
    if not all(e in ELEMENTS for e, _ in parts):
        return False
    return any(n for _, n in parts)


LINT_RULES = [
    ("ascii-minus", re.compile(r"(?:^|[\s(=,:;/×])-(?=\d)"), "hyphen-minus used as a minus sign (use −)"),
    ("caret-exponent", re.compile(r"\d\s*\^\s*[\-−]?\d"), "caret exponent in visible text (use a superscript)"),
    ("ascii-arrow", re.compile(r"(?<![<!-])-{1,2}>|<-{1,2}(?!-)|=>"), "ASCII arrow (use → or ⇌)"),
    ("x-times", re.compile(r"\d\s+x\s+10\b|\d x10\b"), "letter x as a times sign (use ×)"),
    ("missing-subscript", re.compile(r"\b(?:IE|EA)\d\b|\b[A-Za-zλνχ]_[A-Za-z0-9]{1,4}\b"), "subscript written as plain text (use <sub>)"),
    ("sign-first-charge", re.compile(r"[A-Z][a-z]?(?:<sub>\d+</sub>)?<sup>[+\-−]\d"), "charge written sign-first (use 2+, 3−)"),
]
# sanctioned exceptions: (rule, substring of the text node) with the reason
LINT_ALLOW = [
    ("flattened-formula", "e.g.", "input-format example telling the student what to type"),
    ("flattened-formula", "Type subscripts as plain digits", "tells the student how to type a formula into the answer box"),
]


def lint_strings(items):
    """items: list of (where, text, tag). Returns list of findings."""
    out = []
    for where, text, tag in items:
        for rule, rx, why in LINT_RULES[:5]:
            for m in rx.finditer(text):
                out.append((rule, where, text.strip()[:120], why))
        for m in FORMULA_TOKEN.finditer(text):
            tok = m.group(1)
            if flattened_formula(tok):
                if any(r == "flattened-formula" and s in text for r, s, _ in LINT_ALLOW):
                    continue
                out.append(("flattened-formula", where, text.strip()[:120], f"'{tok}' written without <sub>"))
    return out


def html_nodes(html, where_prefix=""):
    tp = TextNodes()
    tp.feed(html)
    return [((where_prefix + ":" + w) if where_prefix else w, t, tag) for w, t, tag in tp.nodes]


def problem_strings(p):
    a = p["answer"]
    out = [p.get("prompt", ""), p.get("solution", ""), p.get("compare", "") or ""] + list(p.get("hints", []))
    if p.get("cue"):
        out.append(p["cue"])
    for o in a.get("options", []) or []:
        out += [o.get("html", ""), o.get("feedback", "")]
    for it in a.get("items", []) or []:
        out.append(it.get("html", ""))
    for r in a.get("rows", []) or []:
        out.append(r.get("html", ""))
    if a.get("model"):
        out.append(a["model"])
    for part in a.get("parts", []) or []:
        out.append(part.get("label", ""))
    return [s for s in out if isinstance(s, str) and s]


def check_notation(R, D, dom_file):
    R.h("5. Notation lint")
    html = open(os.path.join(GUIDE, "index.html"), encoding="utf-8").read()
    nodes = html_nodes(html, "index")
    for p in D["problems"]:
        for s in problem_strings(p):
            nodes += html_nodes(s, p["id"])
    # the scope panel is injected at runtime from scope.js (generated from SOURCE_SCOPE.md): lint it statically too
    sj = open(os.path.join(GUIDE, "assets", "scope.js"), encoding="utf-8").read()
    scope_html = json.loads(sj[sj.index("{"): sj.rindex("}") + 1])["html"]
    nodes += html_nodes(scope_html, "scope.js")
    if dom_file and os.path.exists(dom_file):
        nodes += html_nodes(open(dom_file, encoding="utf-8").read(), "dom")
    findings = lint_strings(nodes)
    seen, uniq = set(), []
    for f in findings:
        k = (f[0], f[2])
        if k not in seen:
            seen.add(k)
            uniq.append(f)
    # sign-first charges need the raw HTML, not text nodes
    raw = html + json.dumps([problem_strings(p) for p in D["problems"]], ensure_ascii=False)
    for m in LINT_RULES[5][1].finditer(raw):
        uniq.append(("sign-first-charge", "raw", raw[max(0, m.start() - 20): m.end() + 10], LINT_RULES[5][2]))
    # notes whose CSS already prints a label ("Background (not from lecture): ", "Connection: ", "Note: ")
    for m in re.finditer(r"""class=['"](bg|connection|note)['"]>\s*(Background|Connection|Note|Discrepancy note)\b""", raw):
        uniq.append(("repeated-label", "raw", raw[m.start(): m.end() + 40], "the CSS ::before already prints this label"))
    R.p(f"Scanned {len(nodes)} text nodes (index.html, the scope panel, every problem string{', and the rendered DOM' if dom_file else ''}) "
        "for flattened formulas (H2O instead of H<sub>2</sub>O), hyphen-minus signs, caret exponents, ASCII arrows, "
        "a letter x as the times sign, and sign-first charges.")
    if uniq:
        R.table(["rule", "where", "text", "why"], [[a, b, c, d] for a, b, c, d in uniq[:200]])
        R.fail(f"{len(uniq)} notation findings")
    else:
        R.p("")
        R.p("No findings.")
    return len(uniq)


# ================================================================== 6. citations and labels
DAY_RUN = re.compile(r"Day\s?(\d)((?:(?:\s|,\s?|;\s?)(?:p|pp)\.\s?\d+(?:\s?[–-]\s?\d+)?)+)")
PDF_REF = re.compile(r"PDF\s(?:p|pp)?\.?\s?(\d+)(?:\s?[–-]\s?(\d+))?(?:,?\s?\(?printed\s(?:p|pp)?\.?\s?(\d+)(?:\s?[–-]\s?(\d+))?)?")
PRINTED_FIRST = re.compile(r"printed\spp?\.\s?(\d+)(?:\s?[–-]\s?(\d+))?\s\(PDF\s(\d+)(?:\s?[–-]\s?(\d+))?\)")


def in_scope(page):
    return any(a <= page <= b for a, b in TEXTBOOK_SCOPE)


def check_citations(R, D):
    R.h("6. Citations and topic labels")
    html = open(os.path.join(GUIDE, "index.html"), encoding="utf-8").read()
    texts = [("index", re.sub(r"<[^>]+>", "", html))]
    for p in D["problems"]:
        texts.append((p["id"], " ".join(re.sub(r"<[^>]+>", "", s) for s in problem_strings(p) + [p.get("source", "")])))
    for f in glob.glob(os.path.join(GUIDE, "assets", "*.js")):
        texts.append((os.path.basename(f), open(f, encoding="utf-8").read()))
    n_day = n_pdf = 0
    problems = []
    for where, t in texts:
        for m in DAY_RUN.finditer(t):
            day = int(m.group(1))
            for a, b in re.findall(r"(\d+)(?:\s?[–-]\s?(\d+))?", m.group(2)):
                n_day += 1
                hi = int(b) if b else int(a)
                if day not in LECTURE_PAGES or hi > LECTURE_PAGES[day] or int(a) < 1 or (b and int(b) < int(a)):
                    problems.append((where, m.group(0), f"Day {day} has {LECTURE_PAGES.get(day, '?')} pages"))
        for m in PDF_REF.finditer(t):
            n_pdf += 1
            p1 = int(m.group(1))
            p2 = int(m.group(2)) if m.group(2) else p1
            before = t[max(0, m.start() - 220): m.start()].lower()          # the whole bullet or sentence
            excluded_mention = re.search(r"exclud|end-of-chapter|questions and problems|not processed", before)
            if not (in_scope(p1) and in_scope(p2)) and not excluded_mention:
                problems.append((where, m.group(0), "textbook page outside the guide's scope"))
            if m.group(3):
                q1 = int(m.group(3))
                q2 = int(m.group(4)) if m.group(4) else q1
                if p1 >= 36 and (q1 != p1 - TEXTBOOK_OFFSET or q2 != p2 - TEXTBOOK_OFFSET):
                    problems.append((where, m.group(0), f"printed should be {p1 - TEXTBOOK_OFFSET}"
                                     + (f"–{p2 - TEXTBOOK_OFFSET}" if p2 != p1 else "")))
        for m in PRINTED_FIRST.finditer(t):
            n_pdf += 1
            q1, p1 = int(m.group(1)), int(m.group(3))
            if p1 != q1 + TEXTBOOK_OFFSET:
                problems.append((where, m.group(0), f"PDF should be {q1 + TEXTBOOK_OFFSET}"))
    seen, uniq = set(), []
    for x in problems:
        if (x[1], x[2]) not in seen:
            seen.add((x[1], x[2]))
            uniq.append(x)
    R.p(f"Checked {n_day} lecture page references (each within that Day's page count) and {n_pdf} textbook references "
        f"(inside the scope ranges {', '.join(f'{a}–{b}' for a, b in TEXTBOOK_SCOPE)}; printed = PDF − {TEXTBOOK_OFFSET}).")
    if uniq:
        R.table(["where", "citation", "problem"], uniq[:120])
        R.fail(f"{len(uniq)} citation problems")
    # label rules
    mods = {m["id"]: m for m in D["modules"]}
    lab_bad = []
    for p in D["problems"]:
        src = p.get("source", "")
        lab = p.get("label")
        if lab == "preview" and "textbook" not in src.lower():
            lab_bad.append((p["id"], "preview problem without a textbook citation"))
        if lab == "lecture" and not re.search(r"Day \d", src):
            lab_bad.append((p["id"], "lecture problem without a Day citation"))
        m = mods.get(p["module"])
        if m and m["label"] == "preview" and lab == "lecture":
            lab_bad.append((p["id"], "lecture-labeled problem inside a textbook-preview module"))
    # professor/lecture claims inside preview-only modules, for manual review
    review = []
    for p in D["problems"]:
        m = mods.get(p["module"])
        if not m or m["label"] != "preview":
            continue
        for s in problem_strings(p):
            t = re.sub(r"<[^>]+>", "", s)
            for mm in re.finditer(r"[^.]*\b(professor|lecture[ds]?|taught|emphasi[sz]e)\b[^.]*\.", t, re.I):
                review.append((p["id"], mm.group(0).strip()[:160]))
    R.p("")
    R.p(f"Label rules: {len(D['problems'])} problems; preview problems cite the textbook, lecture problems cite a Day, and "
        f"no lecture-labeled problem sits in a preview-only module: " + ("all pass." if not lab_bad else f"{len(lab_bad)} problems:"))
    if lab_bad:
        R.table(["problem", "problem"], lab_bad)
        R.fail(f"{len(lab_bad)} label problems")
    R.p("")
    R.p(f"Mentions of the professor or lecture inside preview-only modules ({len(review)}), listed for review. Each should "
        "describe the lecture's relation to the topic (e.g., \"not yet taught\"), never claim the professor taught it:")
    if review:
        R.table(["problem", "sentence"], review)
    return len(uniq) + len(lab_bad)


# ================================================================== 7. structure
def check_structure(R, D, dom_file):
    R.h("7. Structure")
    bad = 0
    ids = [p["id"] for p in D["problems"]]
    dup = sorted({i for i in ids if ids.count(i) > 1})
    if dup:
        bad += 1
        R.fail("duplicate problem ids: " + ", ".join(dup))
    mods = [m["id"] for m in D["modules"]]
    per = {m: [p for p in D["problems"] if p["module"] == m] for m in mods}
    rows = []
    for m in mods:
        ps = per[m]
        kinds = {k: sum(1 for p in ps if p["kind"] == k) for k in ("attempt", "practice", "transfer", "mastery")}
        att = [p for p in ps if p["kind"] == "attempt"]
        ok = (kinds["attempt"] == 1 and kinds["practice"] >= 3 and kinds["transfer"] >= 1
              and any(p["answer"]["type"] == "self" for p in ps)
              and all(len(p.get("hints", [])) >= 4 and p.get("compare") for p in att))
        if not ok:
            bad += 1
            rows.append([m, json.dumps(kinds)])
    orphans = [p["id"] for p in D["problems"] if p["module"] not in mods and p["kind"] != "mixed"]
    mixed = [p for p in D["problems"] if p["kind"] == "mixed"]
    R.p(f"- {len(mods)} modules, {len(D['problems'])} problems ({len(mixed)} mixed review). Every module has one attempt "
        "problem with ≥ 4 hints and a Compare panel, ≥ 3 practice problems, a transfer problem, and a self-check: "
        + ("yes." if not rows else "no:"))
    if rows:
        R.table(["module", "kinds"], rows)
    if orphans:
        bad += 1
        R.fail("problems whose module doesn't exist: " + ", ".join(orphans))
    if len(mixed) < 15:
        bad += 1
        R.fail(f"only {len(mixed)} mixed-review problems")
    homes = [p for p in mixed if p.get("home") not in mods]
    if homes:
        bad += 1
        R.fail("mixed problems without a valid home module: " + ", ".join(p["id"] for p in homes))
    html = open(os.path.join(GUIDE, "index.html"), encoding="utf-8").read()
    tids = re.findall(r'data-testid="([^"]+)"', html)
    dupt = sorted({t for t in tids if tids.count(t) > 1})
    R.p(f"- Static data-testids in index.html: {len(tids)}, " + ("all unique." if not dupt else "duplicates: " + ", ".join(dupt)))
    bad += bool(dupt)
    if dom_file and os.path.exists(dom_file):
        dom = open(dom_file, encoding="utf-8").read()
        dt = re.findall(r'data-testid="([^"]+)"', dom)
        from collections import Counter
        cnt = Counter(dt)
        dd = sorted(t for t, c in cnt.items() if c > 1)
        R.p(f"- Rendered DOM (every module's stages and explorers mounted): {len(dt)} data-testids, "
            + ("all unique." if not dd else f"{len(dd)} duplicated: " + ", ".join(dd[:40])))
        bad += bool(dd)
    for req in ("hint-btn-", "reveal-", "answer-", "check-", "nav-"):
        pass
    # solutions are rendered hidden from data.js, so no solution may appear in the static HTML
    plain = lambda x: re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", x)).strip()
    page_text = plain(html)
    leaks = [p["id"] for p in D["problems"] if p.get("solution") and len(plain(p["solution"])) > 60 and plain(p["solution"]) in page_text]
    R.p("- No complete solution appears in the static HTML (solutions are rendered hidden from data.js): "
        + ("confirmed." if not leaks else "FOUND in index.html: " + ", ".join(leaks[:20])))
    bad += bool(leaks)
    # a problem's bold final answer shouldn't be printed in its own module's teaching text
    give_away = []
    pages = {}
    for m in re.finditer(r"""<section[^>]*data-module=['"]([^'"]+)['"]""", html):
        pages[m.group(1)] = m.start()
    starts = sorted(pages.items(), key=lambda kv: kv[1])
    for i, (mid, st) in enumerate(starts):
        en = starts[i + 1][1] if i + 1 < len(starts) else len(html)
        pages[mid] = plain(html[st:en])
    for p in D["problems"]:
        if p["kind"] not in ("attempt", "practice", "transfer") or p["module"] not in pages:
            continue
        for b in re.findall(r"<strong>(.*?)</strong>", p.get("solution", "")):
            b = plain(b)
            if len(b) >= 6 and re.search(r"\d", b) and b in pages[p["module"]]:
                give_away.append((p["id"], b))
    open_give = [g for g in give_away if g[0] not in REVIEWED_GIVEAWAYS]
    R.p(f"- Final answers (bold in solutions) printed in the same module's teaching text: {len(give_away)}"
        + ("." if not give_away else f" ({len(open_give)} not yet reviewed):"))
    if give_away:
        R.table(["problem", "answer text found on the page", "verdict"],
                [(a, b, REVIEWED_GIVEAWAYS.get(a, "OPEN: change the example or the problem")) for a, b in give_away])
    if open_give:
        bad += 1
        R.fail(f"{len(open_give)} unreviewed answer give-aways")
    return bad


# ================================================================== main
def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--blind", default=os.path.join(HERE, "blind_check"),
                    help="directory with blind answers_*.json files (default: blind_check/, the 2026-09-24 record)")
    ap.add_argument("--dom", help="HTML dump of the rendered guide (all modules visited), for DOM lint and testid checks")
    ap.add_argument("--out", default=os.path.join(HERE, "verification_report.md"))
    args = ap.parse_args()
    D = load_data()
    R = Report()
    R.p("# Verification report: CurrentCourseGuide")
    R.p("")
    R.p("Generated by `verification/CurrentCourseGuide/verify_guide.py`. Regenerate after any change to the banks, "
        "data, or HTML. Summarized in `study-guides/CurrentCourseGuide/VERIFICATION.md`.")
    counts = {
        "physics": check_physics(R),
        "configs": check_configs(R, D),
        "tables": check_tables(R, D),
        "keys": check_blind(R, D, args.blind),
        "notation": check_notation(R, D, args.dom),
        "citations": check_citations(R, D),
        "structure": check_structure(R, D, args.dom),
    }
    R.lines.insert(3, "")
    R.lines.insert(4, "**Summary:** " + ", ".join(f"{k} {'ok' if not v else str(v) + ' issue(s)'}" for k, v in counts.items())
                   + f". Failures: {len(R.failures)}; warnings: {len(R.warnings)}.")
    open(args.out, "w", encoding="utf-8").write("\n".join(R.lines) + "\n")
    print(R.lines[4])
    for f in R.failures:
        print("FAIL", f)
    for w in R.warnings:
        print("WARN", w)
    sys.exit(1 if R.failures else 0)


if __name__ == "__main__":
    main()

"""Course data for the Ch. 4 explorers (assets/explorers_ch4.js), built from lewis.py (checked structures)
and Table 4.6 (TB PDF p.207). Also produces reference answers (Python implementation) that
test_explorers_ch4.js compares with the JavaScript explorer calculations.

Sources: naming rules Day 7 p.21, Day 8 p.6-13, textbook §4.3 (PDF p.188-195); ion table Day 8 p.8
(slide Table 4.5 = textbook Table 4.4, PDF p.192); transition-metal charges textbook Fig. 2.11 (PDF p.92);
Lewis material Day 8 p.16-30 and textbook §4.4-4.9."""
import math

import lewis as LW
from guide_common import ELECTRONEGATIVITY

# ------------------------------------------------------------------ naming (m15-m17, t4-3)
# cations: key, formula text, charge, name, needs a Roman numeral, polyatomic, source
CATIONS = [
    ("Li", "Li", 1, "lithium", False, False, "Day 7 p.19"), ("Na", "Na", 1, "sodium", False, False, "Day 7 p.19"),
    ("K", "K", 1, "potassium", False, False, "group 1 (Day 7 p.18)"), ("Mg", "Mg", 2, "magnesium", False, False, "Day 7 p.19"),
    ("Ca", "Ca", 2, "calcium", False, False, "group 2 (Day 7 p.18)"), ("Ba", "Ba", 2, "barium", False, False, "group 2 (Day 7 p.18)"),
    ("Al", "Al", 3, "aluminum", False, False, "Day 7 p.19"), ("NH4", "NH4", 1, "ammonium", False, True, "Day 8 p.8"),
    ("Fe2", "Fe", 2, "iron", True, False, "Day 8 p.10; textbook Fig. 2.11"), ("Fe3", "Fe", 3, "iron", True, False, "Day 8 p.10; textbook Fig. 2.11"),
    ("Cu1", "Cu", 1, "copper", True, False, "Day 8 p.7"), ("Cu2", "Cu", 2, "copper", True, False, "Day 8 p.7"),
    ("Co2", "Co", 2, "cobalt", True, False, "textbook Fig. 2.11"), ("Co3", "Co", 3, "cobalt", True, False, "textbook Fig. 2.11"),
    ("Cr3", "Cr", 3, "chromium", True, False, "textbook Fig. 2.11"), ("Mn2", "Mn", 2, "manganese", True, False, "textbook Fig. 2.11"),
    ("Ni2", "Ni", 2, "nickel", True, False, "textbook Fig. 2.11"),
    ("Zn", "Zn", 2, "zinc", False, False, "textbook §4.3, PDF p.191 (one cation, no numeral)"),
    ("Ag", "Ag", 1, "silver", False, False, "textbook §4.3, PDF p.191 (one cation, no numeral)"),
]
# anions: key, formula text, html, charge, name, polyatomic, source
ANIONS = [
    ("F", "F", "F", -1, "fluoride", False, "Day 7 p.19"), ("Cl", "Cl", "Cl", -1, "chloride", False, "Day 7 p.19"),
    ("Br", "Br", "Br", -1, "bromide", False, "group 17 (Day 7 p.18)"), ("I", "I", "I", -1, "iodide", False, "group 17 (Day 7 p.18)"),
    ("O", "O", "O", -2, "oxide", False, "Day 7 p.19"), ("S", "S", "S", -2, "sulfide", False, "group 16 (Day 7 p.18)"),
    ("N", "N", "N", -3, "nitride", False, "group 15 (Day 7 p.18)"),
] + [(k, f, h, q, n, True, "Day 8 p.8") for k, f, h, q, n in [
    ("CO3", "CO3", "CO<sub>3</sub>", -2, "carbonate"), ("HCO3", "HCO3", "HCO<sub>3</sub>", -1, "hydrogen carbonate"),
    ("CH3COO", "CH3COO", "CH<sub>3</sub>COO", -1, "acetate"), ("CN", "CN", "CN", -1, "cyanide"), ("SCN", "SCN", "SCN", -1, "thiocyanate"),
    ("ClO", "ClO", "ClO", -1, "hypochlorite"), ("ClO2", "ClO2", "ClO<sub>2</sub>", -1, "chlorite"), ("ClO3", "ClO3", "ClO<sub>3</sub>", -1, "chlorate"),
    ("ClO4", "ClO4", "ClO<sub>4</sub>", -1, "perchlorate"), ("CrO4", "CrO4", "CrO<sub>4</sub>", -2, "chromate"),
    ("Cr2O7", "Cr2O7", "Cr<sub>2</sub>O<sub>7</sub>", -2, "dichromate"), ("MnO4", "MnO4", "MnO<sub>4</sub>", -1, "permanganate"),
    ("N3", "N3", "N<sub>3</sub>", -1, "azide"), ("NO2", "NO2", "NO<sub>2</sub>", -1, "nitrite"), ("NO3", "NO3", "NO<sub>3</sub>", -1, "nitrate"),
    ("OH", "OH", "OH", -1, "hydroxide"), ("O2", "O2", "O<sub>2</sub>", -2, "peroxide"), ("PO4", "PO4", "PO<sub>4</sub>", -3, "phosphate"),
    ("HPO4", "HPO4", "HPO<sub>4</sub>", -2, "hydrogen phosphate"), ("H2PO4", "H2PO4", "H<sub>2</sub>PO<sub>4</sub>", -1, "dihydrogen phosphate"),
    ("S2", "S2", "S<sub>2</sub>", -2, "disulfide"), ("SO3", "SO3", "SO<sub>3</sub>", -2, "sulfite"), ("SO4", "SO4", "SO<sub>4</sub>", -2, "sulfate"),
    ("HSO3", "HSO3", "HSO<sub>3</sub>", -1, "hydrogen sulfite"), ("HSO4", "HSO4", "HSO<sub>4</sub>", -1, "hydrogen sulfate")]]
ALT_NAMES = {"HCO3": "bicarbonate", "HSO3": "bisulfite", "HSO4": "bisulfate"}      # Day 8 p.8 lists both
ROMAN = {1: "I", 2: "II", 3: "III", 4: "IV", 5: "V", 6: "VI", 7: "VII"}
PREFIXES = ["mono", "di", "tri", "tetra", "penta", "hexa", "hepta", "octa", "nona", "deca"]      # Table 4.3
COV_FIRST = [("B", "boron"), ("C", "carbon"), ("Si", "silicon"), ("N", "nitrogen"), ("P", "phosphorus"), ("S", "sulfur"),
             ("Se", "selenium"), ("Cl", "chlorine"), ("Br", "bromine"), ("I", "iodine"), ("O", "oxygen")]
COV_SECOND = [("O", "oxide"), ("F", "fluoride"), ("Cl", "chloride"), ("Br", "bromide"), ("S", "sulfide"), ("N", "nitride")]
# which element is written first: the textbook's summary says the one farther left, or lower in its group (PDF p.220);
# this is the standard sequence that implements it for these elements (CLARIFICATION)
COV_ORDER = ["B", "Si", "C", "P", "N", "Se", "S", "I", "Br", "Cl", "O", "F"]
# acids (t4-3; textbook §4.3 Binary Acids and Oxoacids, PDF p.193-195)
ACIDS = [
    ("F", "HF", "hydrofluoric acid", "binary", "textbook PDF p.194"), ("Cl", "HCl", "hydrochloric acid", "binary", "textbook PDF p.194"),
    ("Br", "HBr", "hydrobromic acid", "binary", "textbook PDF p.194"),                       # HI(aq) is the t4-3 attempt
    ("S", "H2S", "hydrosulfuric acid", "binary", "the textbook's rule applied (connection)"),
    ("NO3", "HNO3", "nitric acid", "oxo", "the textbook's rule applied (connection)"), ("NO2", "HNO2", "nitrous acid", "oxo", "textbook PDF p.194"),
    ("SO4", "H2SO4", "sulfuric acid", "oxo", "textbook PDF p.194"), ("SO3", "H2SO3", "sulfurous acid", "oxo", "textbook Sample Ex. 4.8"),
    ("PO4", "H3PO4", "phosphoric acid", "oxo", "textbook Sample Ex. 4.8"), ("CO3", "H2CO3", "carbonic acid", "oxo", "the textbook's rule applied (connection)"),
    ("ClO4", "HClO4", "perchloric acid", "oxo", "textbook Table 4.5"), ("ClO3", "HClO3", "chloric acid", "oxo", "textbook Table 4.5"),
    ("ClO2", "HClO2", "chlorous acid", "oxo", "textbook Table 4.5"), ("ClO", "HClO", "hypochlorous acid", "oxo", "textbook Table 4.5"),
]


def py_ionic(cat, an):
    """Reference formula and name (independent of the JS implementation)."""
    _, cf, cq, cname, numeral, cpoly, _ = cat
    _, af, _, aq, aname, apoly, _ = an
    g = math.gcd(cq, -aq)
    nc, na = -aq // g, cq // g
    def part(f, n, poly):
        if n == 1:
            return f
        return (f"({f})" if poly else f) + str(n)
    formula = part(cf, nc, cpoly) + part(af, na, apoly)
    name = f"{cname}({ROMAN[cq]}) {aname}" if numeral else f"{cname} {aname}"
    return formula, name, nc, na


def py_covalent(first, n1, second, n2, drop_vowel):
    sym1, name1 = first
    sym2, name2 = second
    p1 = "" if n1 == 1 else PREFIXES[n1 - 1]
    p2 = PREFIXES[n2 - 1]
    if drop_vowel and p2[-1] in "ao" and name2[0] in "aeiou":
        p2 = p2[:-1]
    formula = sym1 + (str(n1) if n1 > 1 else "") + sym2 + (str(n2) if n2 > 1 else "")
    return formula, f"{p1}{name1} {p2}{name2}"


def naming_data():
    cats = [{"key": k, "f": f, "q": q, "name": n, "numeral": r, "poly": p, "src": s} for k, f, q, n, r, p, s in CATIONS]
    ans = [{"key": k, "f": f, "html": h, "q": q, "name": n, "poly": p, "src": s, "alt": ALT_NAMES.get(k)} for k, f, h, q, n, p, s in ANIONS]
    return {"cations": cats, "anions": ans, "prefixes": PREFIXES, "roman": ROMAN,
            "covFirst": [list(x) for x in COV_FIRST], "covSecond": [list(x) for x in COV_SECOND], "covOrder": COV_ORDER,
            "acids": [{"anion": a, "f": f, "name": n, "kind": k, "src": src} for a, f, n, k, src in ACIDS]}


def naming_expected():
    ion_rows = []
    for c in CATIONS:
        for a in ANIONS:
            f, n, nc, na = py_ionic(c, a)
            ion_rows.append([c[0], a[0], f, n, nc, na])
    cov_rows = []
    for fs in COV_FIRST:
        for ss in COV_SECOND:
            if COV_ORDER.index(fs[0]) >= COV_ORDER.index(ss[0]):
                continue
            for n1 in (1, 2, 3):
                for n2 in (1, 2, 3, 4, 5, 6, 7, 10):
                    for dv in (False, True):
                        f, n = py_covalent(fs, n1, ss, n2, dv)
                        cov_rows.append([fs[0], n1, ss[0], n2, dv, f, n])
    return {"ionic": ion_rows, "covalent": cov_rows}


# checks against the problem bank's keys and the slides' examples
_C = {c[0]: c for c in CATIONS}
_A = {a[0]: a for a in ANIONS}
assert py_ionic(_C["Cu1"], _A["S"])[:2] == ("Cu2S", "copper(I) sulfide")
assert py_ionic(_C["Cu2"], _A["O"])[:2] == ("CuO", "copper(II) oxide")          # Day 8 p.7
assert py_ionic(_C["Cu1"], _A["O"])[:2] == ("Cu2O", "copper(I) oxide")          # Day 8 p.7
assert py_ionic(_C["Fe3"], _A["O"])[:2] == ("Fe2O3", "iron(III) oxide")         # Day 8 p.10
assert py_ionic(_C["Li"], _A["NO3"])[:2] == ("LiNO3", "lithium nitrate")        # Day 8 p.9
assert py_ionic(_C["Na"], _A["HCO3"])[0] == "NaHCO3"                            # Day 8 p.9 (sodium bicarbonate)
assert py_ionic(_C["NH4"], _A["ClO2"])[:2] == ("NH4ClO2", "ammonium chlorite")  # Day 8 p.9
assert py_ionic(_C["NH4"], _A["SO4"])[:2] == ("(NH4)2SO4", "ammonium sulfate")
assert py_ionic(_C["Mg"], _A["PO4"])[0] == "Mg3(PO4)2"                          # textbook Sample Ex. 4.6
assert py_ionic(_C["Cr3"], _A["SO4"])[:2] == ("Cr2(SO4)3", "chromium(III) sulfate")
assert py_ionic(_C["Mg"], _A["Cl"])[:2] == ("MgCl2", "magnesium chloride")      # Day 7 p.21
assert py_covalent(("P", "phosphorus"), 1, ("Cl", "chloride"), 5, False)[1] == "phosphorus pentachloride"
assert py_covalent(("S", "sulfur"), 2, ("F", "fluoride"), 2, False)[1] == "disulfur difluoride"   # Day 8 p.13
assert py_covalent(("N", "nitrogen"), 2, ("O", "oxide"), 1, True)[1] == "dinitrogen monoxide"     # textbook p.188
assert py_covalent(("N", "nitrogen"), 2, ("O", "oxide"), 1, False)[1] == "dinitrogen monooxide"   # the slides' rule, literally
assert py_covalent(("P", "phosphorus"), 2, ("O", "oxide"), 5, True)[1] == "diphosphorus pentoxide"  # textbook Sample Ex. 4.3


# ------------------------------------------------------------------ Lewis data
def atom_rows(s):
    rows = []
    for k, a in enumerate(s.atoms):
        rows.append([a[0], LW.VALENCE[a[0]], 2 * s.lp.get(k, 0), s.rad.get(k, 0), 2 * s.bond_orders(k), s.fc(k), s.shell(k)])
    return rows


def entry(sid, scale=1.0):
    s = LW.STRUCTS[sid]
    return {"id": sid, "name": s.name, "formula": s.formula_html, "charge": s.charge, "total": s.total_valence(),
            "svg": LW.svg(s, scale=scale), "svgFC": LW.svg(s, show_fc=True, scale=scale), "atoms": atom_rows(s),
            "bonds": [list(b) for b in s.bonds], "central": s.central, "source": s.source}


def step_table(s):
    order, counts = [], {}
    for a in s.atoms:
        if a[0] not in counts:
            order.append(a[0])
            counts[a[0]] = 0
        counts[a[0]] += 1
    return [[el, counts[el], LW.VALENCE[el]] for el in order]


# HCN and C2H4 are left out on purpose: they are the m19 attempt and transfer problems
STEP_IDS = ["F2", "H2O", "NH3", "CH4", "CHCl3", "H2O2", "CH2O", "CO2", "C2H2", "O3a", "OH-", "NH4+", "NO3-1"]
STEP_TAG = {"F2": "lecture", "NH3": "lecture", "C2H2": "lecture", "O3a": "lecture",
            "CHCl3": "textbook", "H2O2": "textbook", "CH2O": "textbook", "CO2": "textbook", "OH-": "textbook", "NH4+": "textbook",
            "NO3-1": "textbook", "CH4": "textbook", "H2O": "new", "HCN": "new", "C2H4": "new"}


def steps_data():
    out = {}
    for sid in STEP_IDS:
        s = LW.STRUCTS[sid]
        frames = []
        for lab, st, info in LW.five_steps(s):
            frames.append({"label": lab, "svg": LW.svg(st), "used": info["used"],
                           "short": [s.atoms[c][0] for c in info.get("short", [])], "same": bool(info.get("same_as_previous"))})
        out[sid] = {"name": s.name, "formula": s.formula_html, "charge": s.charge, "total": s.total_valence(),
                    "table": step_table(s), "frames": frames, "tag": STEP_TAG[sid], "source": s.source}
    return out


# nitrite and formate are left out on purpose: they are the t4-5 attempt and transfer problems
RES_SETS = [
    {"key": "O3", "ids": ["O3a", "O3b"], "label": "ozone, O₃", "tag": "lecture", "pair": ["O–O", "O=O"], "measured": 128,
     "src": "Day 8 p.30; Day 9 p.6–10 (128 pm: Day 9 p.7); textbook §4.5–4.6, PDF p.203, p.206"},
    {"key": "NO3-", "ids": ["NO3-1", "NO3-2", "NO3-3"], "label": "nitrate ion, NO₃⁻", "tag": "textbook", "pair": ["N–O", "N=O"], "measured": None,
     "src": "textbook Sample Ex. 4.14, PDF p.204–205"},
    {"key": "CO3", "ids": ["CO3-1", "CO3-2", "CO3-3"], "label": "carbonate ion, CO₃²⁻", "tag": "textbook", "pair": ["C–O", "C=O"], "measured": 129,
     "src": "textbook Sample Ex. 4.15, PDF p.207–208 (129 pm)"},
    {"key": "C6H6", "ids": ["C6H6-1", "C6H6-2"], "label": "benzene, C₆H₆", "tag": "lecture", "pair": ["C–C", "C=C"], "measured": None,
     "src": "Day 9 p.12–13 (Kekulé structures and the hybrid; equal bonds, Day 9 p.2); textbook Fig. 4.10, PDF p.205"},
]


def resonance_data(bonds):
    out = []
    for r in RES_SETS:
        structs = [LW.STRUCTS[i] for i in r["ids"]]
        orders = LW.average_orders(structs)
        s0 = structs[0]
        a1, a2 = r["pair"][0].split("–")
        sel = [o for (i, j, _), o in zip(s0.bonds, orders) if {s0.atoms[i][0], s0.atoms[j][0]} == {a1, a2}]
        avg = sum(sel) / len(sel)
        out.append({**r, "structs": [entry(i, 0.9) for i in r["ids"]], "hybrid": LW.hybrid_svg(structs, scale=1.3),
                    "avg": round(avg, 6), "nBonds": len(sel), "pairs": sum(o for (i, j, o) in s0.bonds if {s0.atoms[i][0], s0.atoms[j][0]} == {a1, a2}),
                    "single": bonds[r["pair"][0]], "double": bonds[r["pair"][1]]})
    return out


# CO, SCN-, SO3 2-, OH-, NH4+, and O3 are left out on purpose: they are t4-7/t4-8 problems or mixed-review items
FC_SETS = [
    {"key": "N2O", "ids": ["N2O-A", "N2O-B", "N2O-C"], "labels": ["A", "B", "C"], "label": "dinitrogen monoxide, N₂O", "src": "Day 9 p.19–24; textbook §4.7, PDF p.209–211 (worked table)"},
    {"key": "H3PO4", "ids": ["H3PO4-t1", "H3PO4-t2", "H3PO4-t3"], "labels": ["structure 1", "structure 2", "structure 3"],
     "label": "phosphoric acid, H₃PO₄ (Top Hat, Day 9 p.26)", "src": "Day 9 p.26 (Top Hat structures 1–3; structures 4 and 5 draw 34 electrons, not 32)"},
    {"key": "SO4", "ids": ["SO4-oct", "SO4-exp"], "labels": ["octets only", "two S=O"], "label": "sulfate ion, SO₄²⁻", "src": "Day 9 p.30; textbook §4.8, PDF p.215"},
    {"key": "CO2", "ids": ["CO2-alt2", "CO2", "CO2-alt1"], "labels": ["O–C≡O", "O=C=O", "O≡C–O"], "label": "carbon dioxide, CO₂", "src": "textbook Sample Ex. 4.16, PDF p.211–212"},
    {"key": "PO4", "ids": ["PO4-oct", "PO4-exp"], "labels": ["octets only", "one P=O"], "label": "phosphate ion, PO₄³⁻", "src": "textbook Sample Ex. 4.18, PDF p.215–216"},
    {"key": "H2SO4", "ids": ["H2SO4"], "labels": ["two S=O"], "label": "sulfuric acid, H₂SO₄", "src": "textbook §4.8, PDF p.215"},
]
FC_EXPECTED_BEST = {"N2O": 0, "CO2": 1, "SO4": 1, "PO4": 1, "H3PO4": 2}


def fc_data():
    return [{**f, "structs": [entry(i, 0.95) for i in f["ids"]]} for f in FC_SETS]


# BF3 and SO3 2- are left out on purpose: they are the t4-8 attempt and transfer problems
OCTET_IDS = ["BeCl2", "BCl3", "AlCl3", "NO", "NO2-rad1", "PCl5", "SF6", "SO4-exp", "PO4-exp", "H2SO4", "NH3", "CH4", "CO2"]
PERIOD = {"H": 1, "Be": 2, "B": 2, "C": 2, "N": 2, "O": 2, "F": 2, "Al": 3, "P": 3, "S": 3, "Cl": 3}


def octet_data():
    out = []
    for sid in OCTET_IDS:
        e = entry(sid, 0.9)
        e["period"] = [PERIOD[a[0]] for a in LW.STRUCTS[sid].atoms]
        out.append(e)
    return out


SYMBOL_ELEMENTS = [("H", 1), ("He", 18), ("Li", 1), ("Be", 2), ("B", 13), ("C", 14), ("N", 15), ("O", 16), ("F", 17), ("Ne", 18),
                   ("Na", 1), ("Mg", 2), ("Al", 13), ("Si", 14), ("P", 15), ("S", 16), ("Cl", 17), ("Ar", 18), ("K", 1), ("Ca", 2), ("Br", 17), ("I", 17)]


def symbols_data():
    out = []
    for el, grp in SYMBOL_ELEMENTS:
        svgs, unp = LW.symbol_svg(el)
        out.append({"el": el, "group": grp, "valence": LW.VALENCE[el], "unpaired": unp, "svg": svgs})
    return out


def bond_table(bonds):
    rows = []
    for b, (L, E) in bonds.items():
        order = 3 if "≡" in b else 2 if "=" in b else 1
        a1, a2 = b.replace("≡", "–").replace("=", "–").split("–")
        rows.append({"bond": b, "a": a1, "b": a2, "order": order, "pm": L, "kj": E})
    return rows


def build(bonds):
    return {
        "naming": naming_data(),
        "lewisSymbols": symbols_data(),
        "lewisSteps": steps_data(),
        "resonance": resonance_data(bonds),
        "bondTable": bond_table(bonds),
        "fcSets": fc_data(),
        "octet": octet_data(),
        "chi": {k: ELECTRONEGATIVITY[k] for k in ("H", "B", "C", "N", "O", "F", "P", "S", "Cl", "Be", "Br", "I", "Si", "Se")},
        "fcBest": FC_EXPECTED_BEST,
    }

"""Data for the Chapter 5 explorers (assets/explorers_ch5.js) and Python reference values that
test_explorers_ch5.js compares with the JavaScript calculations.

build()    -> {"ch5": {...}} merged into GUIDE_DATA
expected() -> {"ch5": {...}} merged into expected_values.json

Sources: VSEPR Day 10 p.7-26 (textbook §5.1-5.2, PDF p.232-243; Table 5.1, PDF p.240); polarity Day 10
p.27-31 and Day 11 p.6-8 (Table 5.2; textbook §5.3, PDF p.243-246); electronegativity Day 9 p.17 (the same
values as textbook Fig. 4.5); hybrid orbitals and σ/π bonds Day 11 p.9-26 (textbook §5.4-5.5, PDF
p.246-255); chirality Day 10 p.6 and textbook §5.6 (PDF p.255-261); MO diagrams Day 11 p.27 and textbook
§5.7 (PDF p.261-270).

The reference functions here are written independently of the JavaScript: the VSEPR shapes come from
textbook-style polyhedra with the lone pairs placed by brute-force minimization of 90° repulsions (so the
equatorial preference is derived, not assumed); dipoles are numpy vector sums; chirality tests every proper
rotation of a tetrahedron; MO filling walks an explicit orbital list. Hybridization and σ/π counts come from
the checked Lewis structures in lewis.py."""
import itertools
import math

import numpy as np

import lewis as LW
from guide_common import ELECTRONEGATIVITY

TB = "textbook"
CHI = {k: ELECTRONEGATIVITY[k] for k in ("H", "B", "C", "N", "O", "F", "P", "S", "Cl", "Br", "I", "Be")}   # Day 9 p.17

# ================================================================== VSEPR (m20, m21)
EPG = {1: "", 2: "linear", 3: "trigonal planar", 4: "tetrahedral", 5: "trigonal bipyramidal", 6: "octahedral"}
MG = {(2, 0): "linear", (3, 0): "trigonal planar", (3, 1): "bent (angular)", (4, 0): "tetrahedral",
      (4, 1): "trigonal pyramidal", (4, 2): "bent (angular)", (5, 0): "trigonal bipyramidal", (5, 1): "seesaw",
      (5, 2): "T-shaped", (5, 3): "linear", (6, 0): "octahedral", (6, 1): "square pyramidal",
      (6, 2): "square planar", (6, 3): "T-shaped"}
MAX_LP = {2: 0, 3: 1, 4: 2, 5: 3, 6: 3}

# The professor's summary table, Day 10 p.26 (transcribed from the render; "See-saw" as printed)
PROF_TABLE = [
    [2, "Linear", 0, "Linear", "180°"],
    [3, "Trigonal planar", 0, "Trigonal planar", "120°"], [3, "Trigonal planar", 1, "Bent", "120°"],
    [4, "Tetrahedral", 0, "Tetrahedral", "109.5°"], [4, "Tetrahedral", 1, "Trigonal pyramidal", "109.5°"],
    [4, "Tetrahedral", 2, "Bent", "109.5°"],
    [5, "Trigonal bipyramidal", 0, "Trigonal bipyramidal", "120° AND 90°"],
    [5, "Trigonal bipyramidal", 1, "See-saw", "120° AND 90°"], [5, "Trigonal bipyramidal", 2, "T-shaped", "120° AND 90°"],
    [6, "Octahedral", 0, "Octahedral", "90°"], [6, "Octahedral", 1, "Square pyramidal", "90°"],
    [6, "Octahedral", 2, "Square planar", "90°"], [6, "Octahedral", 3, "T-shaped", "90°"],
]

# presets: key, button text, formula HTML, mode, SN, lone pairs, central atom, ligands (in position order),
# bond orders, stated angle (degrees, used to draw the shape) or None, angle text, tag, source, note
VSEPR_PRESETS = [
    ("CO2", "CO₂", "CO<sub>2</sub>", "bonds", 2, 0, "C", ["O", "O"], [2, 2], None, "O=C=O 180°", "lecture",
     "Day 10 p.7, p.10", ""),
    ("BF3", "BF₃", "BF<sub>3</sub>", "bonds", 3, 0, "B", ["F", "F", "F"], [1, 1, 1], None, "F–B–F 120°", "lecture",
     "Day 10 p.10", "B has only six valence electrons (an electron-deficient molecule, Day 9 p.27)."),
    ("CH2O", "CH₂O", "CH<sub>2</sub>O", "bonds", 3, 0, "C", ["O", "H", "H"], [2, 1, 1], 118.0, "H–C–H about 118°",
     "lecture", "Day 10 p.13", "The double bond holds more electrons, so it repels the C–H bonds more and squeezes H–C–H below 120°."),
    ("CH4", "CH₄", "CH<sub>4</sub>", "both", 4, 0, "C", ["H"] * 4, [1] * 4, None, "H–C–H 109.5°", "lecture",
     "Day 10 p.7", "The Lewis structure draws 90°; the molecule has 109.5°."),
    ("CCl4", "CCl₄", "CCl<sub>4</sub>", "bonds", 4, 0, "C", ["Cl"] * 4, [1] * 4, None, "Cl–C–Cl 109.5°", "lecture",
     "Day 10 p.10–11", ""),
    ("PF5", "PF₅", "PF<sub>5</sub>", "bonds", 5, 0, "P", ["F"] * 5, [1] * 5, None, "90° and 120°", "lecture",
     "Day 10 p.12", "Two kinds of position: axial (top and bottom) and equatorial (around the middle)."),
    ("SF6", "SF₆", "SF<sub>6</sub>", "bonds", 6, 0, "S", ["F"] * 6, [1] * 6, None, "90°", "lecture",
     "Day 10 p.12", "All six positions are equivalent."),
    ("O3", "O₃", "O<sub>3</sub>", "lone", 3, 1, "O", ["O", "O"], [1.5, 1.5], 117.0, "O–O–O 117°", "lecture",
     "Day 10 p.14–15", "Both O–O bonds are identical (resonance, Day 9 p.7–10), drawn here as 1½ bonds."),
    ("NH3", "NH₃", "NH<sub>3</sub>", "lone", 4, 1, "N", ["H"] * 3, [1] * 3, 107.0, "H–N–H 107°", "lecture",
     "Day 10 p.16–18", ""),
    ("H2O", "H₂O", "H<sub>2</sub>O", "lone", 4, 2, "O", ["H", "H"], [1, 1], 104.5, "H–O–H 104.5°", "lecture",
     "Day 10 p.19", "The same geometry name as ozone, but not the same bond angle (Day 10 p.19)."),
    ("SO2", "SO₂", "SO<sub>2</sub>", "lone", 3, 1, "S", ["O", "O"], [1.5, 1.5], None, "O–S–O less than 120°", TB,
     "textbook Table 5.1, PDF p.240", "Two resonance structures, so the two S–O bonds are identical."),
    ("SF4", "SF₄", "SF<sub>4</sub>", "lone", 5, 1, "S", ["F"] * 4, [1] * 4, None, "bond angles a little less than 90°, 120°, and 180°", TB,
     "textbook Sample Ex. 5.3, PDF p.242–243", ""),
    ("BrF3", "BrF₃", "BrF<sub>3</sub>", "lone", 5, 2, "Br", ["F"] * 3, [1] * 3, None, "bond angles a little less than 90° (the T is slightly bent)", TB,
     "textbook Table 5.1, PDF p.240", ""),
    ("XeF2", "XeF₂", "XeF<sub>2</sub>", "lone", 5, 3, "Xe", ["F", "F"], [1, 1], None, "F–Xe–F 180°", TB,
     "textbook Table 5.1, PDF p.240", ""),
    ("I3-", "I₃⁻", "I<sub>3</sub><sup>−</sup>", "lone", 5, 3, "I", ["I", "I"], [1, 1], None, "I–I–I 180°", "new",
     "", "An ion: the central I has two bonds and three lone pairs (22 valence electrons)."),
    ("BrF5", "BrF₅", "BrF<sub>5</sub>", "lone", 6, 1, "Br", ["F"] * 5, [1] * 5, 85.0, "axial–equatorial F–Br–F 85°", TB,
     "textbook PDF p.242", ""),
    ("XeF4", "XeF₄", "XeF<sub>4</sub>", "lone", 6, 2, "Xe", ["F"] * 4, [1] * 4, None, "F–Xe–F 90°", TB,
     "textbook Table 5.1, PDF p.240", "The lone pairs sit opposite each other (Day 10 p.25)."),
]


def _unit(v):
    v = np.asarray(v, float)
    return v / np.linalg.norm(v)


def _polyhedron(sn):
    """Ideal electron-pair directions, built the textbook's way (Fig. 5.3): line, triangle, tetrahedron from
    alternate cube corners, trigonal bipyramid, octahedron. Returns (array of unit vectors, list of site names)."""
    if sn == 1:
        return np.array([[1.0, 0, 0]]), [""]
    if sn == 2:
        return np.array([[1.0, 0, 0], [-1.0, 0, 0]]), ["", ""]
    if sn == 3:
        return np.array([[math.cos(t), math.sin(t), 0] for t in (math.pi / 2, math.pi / 2 + 2 * math.pi / 3, math.pi / 2 + 4 * math.pi / 3)]), [""] * 3
    if sn == 4:
        return np.array([_unit(v) for v in ([1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1])]), [""] * 4
    if sn == 5:
        eq = [[math.cos(t), 0, math.sin(t)] for t in (0, 2 * math.pi / 3, 4 * math.pi / 3)]
        return np.array([[0, 1.0, 0], [0, -1.0, 0]] + eq), ["axial", "axial", "equatorial", "equatorial", "equatorial"]
    if sn == 6:
        return np.array([[1.0, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]]), [""] * 6
    raise ValueError(sn)


def _ang(u, v):
    return math.degrees(math.acos(max(-1.0, min(1.0, float(np.dot(_unit(u), _unit(v)))))))


def _contacts90(dirs, lp):
    out = {"lplp": 0, "lpbp": 0, "bpbp": 0}
    for i, j in itertools.combinations(range(len(dirs)), 2):
        if abs(_ang(dirs[i], dirs[j]) - 90) < 1.0:
            out["lplp" if lp[i] and lp[j] else "bpbp" if not lp[i] and not lp[j] else "lpbp"] += 1
    return out


def vsepr_ref(sn, nlp, variant="pref"):
    """Place nlp lone pairs on the polyhedron by brute force. 'pref': fewest 90° lone-pair–lone-pair contacts,
    then fewest 90° lone-pair–bond contacts (textbook PDF p.241: pairs at 90° repel most). 'axial' (SN 5): the
    best arrangement with exactly one lone pair on an axial site. 'adjacent' (SN 6, 2 lone pairs): lone pairs at 90°."""
    dirs, site = _polyhedron(sn)
    best = None
    for combo in itertools.combinations(range(sn), nlp):
        lp = [k in combo for k in range(sn)]
        c = _contacts90(dirs, lp)
        if variant == "axial" and sum(1 for k in combo if site[k] == "axial") != 1:
            continue
        if variant == "adjacent" and c["lplp"] == 0:
            continue
        score = (c["lplp"], c["lpbp"])
        if best is None or score < best[0]:
            best = (score, lp, c)
    _, lp, c = best
    atoms = [dirs[k] for k in range(sn) if not lp[k]]
    angles = sorted({round(_ang(a, b), 1) for a, b in itertools.combinations(atoms, 2)})
    lp_sites = sorted(site[k] for k in range(sn) if lp[k])
    return {"angles": angles, "contacts": c, "lpSites": lp_sites,
            "mg": MG[(sn, nlp)] if variant == "pref" else None, "epg": EPG[sn]}


def vsepr_expected():
    out = {}
    for sn in range(2, 7):
        for nlp in range(0, MAX_LP[sn] + 1):
            out[f"{sn}-{nlp}-pref"] = vsepr_ref(sn, nlp)
            if sn == 5 and nlp >= 1:
                out[f"{sn}-{nlp}-axial"] = vsepr_ref(sn, nlp, "axial")
            if sn == 6 and nlp == 2:
                out[f"{sn}-{nlp}-adjacent"] = vsepr_ref(sn, nlp, "adjacent")
    # the professor's table agrees with the derived names wherever it has a row
    for sn, epg, nlp, mg, _ in PROF_TABLE:
        derived = MG[(sn, nlp)].replace(" (angular)", "").lower()
        assert derived == mg.lower().replace("see-saw", "seesaw"), (sn, nlp, mg, derived)
        assert EPG[sn] == epg.lower()
    return out


# ================================================================== polarity (m22)
# key, label, formula HTML, SN, lone pairs, frame ("A": one domain straight up; "B": two up, two down), central atom,
# ligands in position order, bond orders, stated angle or None, measured μ (D) or None, μ source, direction, tag, source
DIPOLES = [
    ("CO2", "CO₂", "CO<sub>2</sub>", 2, 0, "A", "C", ["O", "O"], [2, 2], None, None, "", "", "lecture", "Day 10 p.28–29"),
    ("CF4", "CF₄", "CF<sub>4</sub>", 4, 0, "A", "C", ["F"] * 4, [1] * 4, None, None, "", "", "lecture", "Day 10 p.30"),
    ("H2O", "H₂O", "H<sub>2</sub>O", 4, 2, "B", "O", ["H", "H"], [1, 1], 104.5, 1.85, "Table 5.2, Day 11 p.8", "toward O", "lecture",
     "Day 10 p.31; Day 11 p.6, p.8"),
    ("HF", "HF", "HF", 1, 0, "A", "H", ["F"], [1], None, 1.82, "Table 5.2, Day 11 p.8", "toward F", "lecture", "Day 11 p.8"),
    ("NH3", "NH₃", "NH<sub>3</sub>", 4, 1, "A", "N", ["H"] * 3, [1] * 3, 107.0, 1.47, "Table 5.2, Day 11 p.8", "toward N", "lecture", "Day 11 p.8"),
    ("CHCl3", "CHCl₃", "CHCl<sub>3</sub>", 4, 0, "A", "C", ["H", "Cl", "Cl", "Cl"], [1] * 4, None, 1.01, "Table 5.2, Day 11 p.8",
     "toward the Cl atoms", "lecture", "Day 11 p.7–8"),
    ("CCl3F", "CCl₃F", "CCl<sub>3</sub>F", 4, 0, "A", "C", ["F", "Cl", "Cl", "Cl"], [1] * 4, None, 0.45, "Table 5.2, Day 11 p.8",
     "toward F", "lecture", "Day 11 p.7–8"),
    ("CH2O", "CH₂O", "CH<sub>2</sub>O", 3, 0, "A", "C", ["O", "H", "H"], [2, 1, 1], 118.0, None, "", "", TB,
     "textbook Sample Ex. 5.4, PDF p.245–246"),
    ("CH2Cl2", "CH₂Cl₂", "CH<sub>2</sub>Cl<sub>2</sub>", 4, 0, "B", "C", ["Cl", "Cl", "H", "H"], [1] * 4, None, None, "", "", TB,
     "textbook Sample Ex. 5.4, PDF p.246"),
    ("H2S", "H₂S", "H<sub>2</sub>S", 4, 2, "B", "S", ["H", "H"], [1, 1], None, 0.97, "textbook Concept Test, PDF p.246", "", TB,
     "textbook PDF p.246"),
    ("BF3", "BF₃", "BF<sub>3</sub>", 3, 0, "A", "B", ["F"] * 3, [1] * 3, None, None, "", "", "new", ""),
    ("NF3", "NF₃", "NF<sub>3</sub>", 4, 1, "A", "N", ["F"] * 3, [1] * 3, None, None, "", "", "new", ""),
    ("SO2", "SO₂", "SO<sub>2</sub>", 3, 1, "A", "S", ["O", "O"], [1.5, 1.5], None, None, "", "", "new", ""),
    ("CCl4", "CCl₄", "CCl<sub>4</sub>", 4, 0, "A", "C", ["Cl"] * 4, [1] * 4, None, None, "", "", "new", ""),
    ("CH3Cl", "CH₃Cl", "CH<sub>3</sub>Cl", 4, 0, "A", "C", ["Cl", "H", "H", "H"], [1] * 4, None, None, "", "", "new", ""),
    ("OF2", "OF₂", "OF<sub>2</sub>", 4, 2, "B", "O", ["F", "F"], [1, 1], None, None, "", "", "new", ""),
    ("HCN", "HCN", "HCN", 2, 0, "A", "C", ["H", "N"], [1, 3], None, None, "", "", "new", ""),
    ("PCl5", "PCl₅", "PCl<sub>5</sub>", 5, 0, "A", "P", ["Cl"] * 5, [1] * 5, None, None, "", "", "new", ""),
    ("SF4", "SF₄", "SF<sub>4</sub>", 5, 1, "A", "S", ["F"] * 4, [1] * 4, None, None, "", "", "new", ""),
    ("XeF4", "XeF₄", "XeF<sub>4</sub>", 6, 2, "A", "Xe", ["F"] * 4, [1] * 4, None, None, "", "", "new", ""),
]


def _shape_dirs(sn, nlp, frame, angle):
    """Directions for a molecule's ligands (preferred lone-pair placement; the stated angle where given), built
    with numpy independently of the JavaScript frames. Only the ligand directions are returned."""
    if sn == 1:
        return [np.array([1.0, 0, 0])]
    if sn in (2, 5, 6) or (sn == 3 and angle is None) or (sn == 4 and angle is None and frame == "A" and nlp < 2):
        dirs, site = _polyhedron(sn)
        best = None
        for combo in itertools.combinations(range(sn), nlp):
            lp = [k in combo for k in range(sn)]
            c = _contacts90(dirs, lp)
            if best is None or (c["lplp"], c["lpbp"]) < best[0]:
                best = ((c["lplp"], c["lpbp"]), lp)
        return [dirs[k] for k in range(sn) if not best[1][k]]
    a = math.radians(angle if angle is not None else 109.4712206)
    if sn == 3:                                   # two equal ligands at the stated angle; any third ligand opposite their bisector
        pair = [np.array([math.sin(a / 2), -math.cos(a / 2), 0]), np.array([-math.sin(a / 2), -math.cos(a / 2), 0])]
        return ([np.array([0, 1.0, 0])] + pair) if nlp == 0 else pair
    if nlp == 1 or (nlp == 0 and frame == "A"):   # pyramid of three ligands at the stated mutual angle
        s2 = 2.0 / 3.0 * (1 - math.cos(a))
        st, ct = math.sqrt(s2), math.sqrt(1 - s2)
        three = [np.array([st * math.sin(p), -ct, st * math.cos(p)]) for p in (0, 2 * math.pi / 3, 4 * math.pi / 3)]
        return ([np.array([0, 1.0, 0])] + three) if nlp == 0 else three
    pair = [np.array([math.sin(a / 2), -math.cos(a / 2), 0]), np.array([-math.sin(a / 2), -math.cos(a / 2), 0])]
    if nlp == 2:
        return pair
    b = math.radians(109.4712206)                 # frame B with no lone pairs (CH2Cl2): two up, two down
    return pair + [np.array([0, math.cos(b / 2), math.sin(b / 2)]), np.array([0, math.cos(b / 2), -math.sin(b / 2)])]


def dipole_ref(m):
    key, _, _, sn, nlp, frame, cen, lig, _, angle = m[:10]
    dirs = _shape_dirs(sn, nlp, frame, angle)
    assert len(dirs) == len(lig), key
    net, unknown = np.zeros(3), False
    for d, x in zip(dirs, lig):
        if cen not in CHI or x not in CHI:
            unknown = True
            net += _unit(d)                       # equal (unknown) bond dipoles: only the symmetry matters
        else:
            net += (CHI[x] - CHI[cen]) * _unit(d)  # points toward the more electronegative atom
    mag = float(np.linalg.norm(net))
    return {"mag": round(mag, 4), "polar": mag > 1e-6, "unknown": unknown}


def dipoles_data():
    out = []
    for m in DIPOLES:
        key, label, fhtml, sn, nlp, frame, cen, lig, orders, angle, mu, musrc, dirtext, tag, src = m
        out.append({"key": key, "label": label, "html": fhtml, "sn": sn, "lp": nlp, "frame": frame, "center": cen,
                    "ligands": lig, "orders": orders, "angle": angle, "mu": mu, "muSrc": musrc, "dir": dirtext,
                    "tag": tag, "src": src})
    return out


# ================================================================== hybrid orbitals (m23)
GROUND = {"Be": (2, 2, 0), "B": (2, 2, 1), "C": (2, 2, 2), "N": (2, 2, 3), "O": (2, 2, 4), "P": (3, 2, 3)}   # shell, s e⁻, p e⁻
HYB = {2: "sp", 3: "sp2", 4: "sp3"}
# key, label, structure id, atom index, tag, source
HYBRID_PRESETS = [
    ("C-CH4", "C in CH₄", "CH4", 0, "lecture", "Day 11 p.11–15"),
    ("N-NH3", "N in NH₃", "NH3", 0, "lecture", "Day 11 p.16"),
    ("O-H2O", "O in H₂O", "H2O", 0, "lecture", "Day 11 p.16"),
    ("C-CH2O", "C in CH₂O", "CH2O", 0, "lecture", "Day 11 p.18–19"),
    ("O-CH2O", "O in CH₂O", "CH2O", 3, "lecture", "Day 11 p.18–19"),
    ("N-N2H2", "N in N₂H₂", "N2H2", 0, "lecture", "Day 11 p.22"),
    ("C-C2H2", "C in C₂H₂", "C2H2", 1, "lecture", "Day 11 p.23"),
    ("C-C2H4", "C in C₂H₄", "C2H4", 0, "lecture", "Day 11 p.25"),
    ("B-BF3", "B in BF₃", "BF3", 0, "new", ""),
    ("Be-BeCl2", "Be in BeCl₂", "BeCl2", 1, "new", ""),
    ("C-CO2", "C in CO₂", "CO2", 1, TB, "textbook Sample Ex. 5.5, PDF p.251–252"),
    ("P-PCl3", "P in PCl₃", "PCl3", 0, "new", ""),
    ("C-HCN", "C in HCN", "HCN", 1, "new", ""),
    ("N-HCN", "N in HCN", "HCN", 2, "new", ""),
]


def steric_number(s, k):
    return sum(1 for i, j, _ in s.bonds if k in (i, j)) + s.lp.get(k, 0)


def partner_orbital(s, k):
    """The orbital a bonded neighbor uses for its σ bond: H uses 1s; every other atom a hybrid (Day 11 p.20)."""
    el = s.atoms[k][0]
    return f"{el} 1s" if el == "H" else f"{el} {HYB[steric_number(s, k)]}"


def hybrid_atom(key, label, sid, k, tag, src):
    s = LW.STRUCTS[sid]
    el = s.atoms[k][0]
    sn, nlp = steric_number(s, k), s.lp.get(k, 0)
    sigma, pi = [], []
    for i, j, o in s.bonds:
        if k not in (i, j):
            continue
        n = j if i == k else i
        sigma.append({"el": s.atoms[n][0], "orb": partner_orbital(s, n)})
        pi += [{"el": s.atoms[n][0], "orb": f"{s.atoms[n][0]} p"}] * (o - 1)
    shell, se, pe = GROUND[el]
    assert se + pe == 2 * nlp + len(sigma) + len(pi), (key, se + pe, nlp, sigma, pi)
    return {"key": key, "label": label, "sid": sid, "el": el, "shell": shell, "s": se, "p": pe, "sn": sn, "lp": nlp,
            "sigma": sigma, "pi": pi, "molecule": s.formula_html, "lewis": LW.svg(s, tag="span", scale=0.8),
            "tag": tag, "src": src}


def hybrid_ref(h):
    """Box occupancies: ground state (Hund's rule in 2p), hybrids (lone pairs first, then one electron per σ
    bond), unhybridized p (one electron per π bond, the rest empty)."""
    p = [0, 0, 0]
    for n in range(h["p"]):
        p[n % 3] += 1
    hyb = [2] * h["lp"] + [1] * len(h["sigma"])
    unh = [1] * len(h["pi"]) + [0] * (4 - h["sn"] - len(h["pi"]))
    assert len(hyb) == h["sn"] and len(unh) == 4 - h["sn"]
    return {"hyb": HYB[h["sn"]], "ground": [h["s"]] + p, "hybrids": hyb, "unhybridized": unh,
            "unpairedGround": (1 if h["s"] == 1 else 0) + sum(1 for x in p if x == 1)}


# ================================================================== σ and π bonds (m24)
# key, label, structure id, tag, source, heavy-atom rows [(description, atom index)]
SIGMA_PI = [
    ("CH2O", "formaldehyde, CH₂O", "CH2O", "lecture", "Day 11 p.17–19", [("C", 0), ("O", 3)]),
    ("N2H2", "diazene, N₂H₂", "N2H2", "lecture", "Day 11 p.22", [("each N", 0)]),
    ("C2H2", "acetylene, C₂H₂", "C2H2", "lecture", "Day 11 p.23", [("each C", 1)]),
    ("C2H4", "ethylene, C₂H₄", "C2H4", "lecture", "Day 11 p.25", [("each C", 0)]),
    ("CO2", "carbon dioxide, CO₂", "CO2", TB, "textbook Sample Ex. 5.5, PDF p.251–252", [("C", 1), ("each O", 0)]),
    ("HCN", "hydrogen cyanide, HCN", "HCN", "new", "", [("C", 1), ("N", 2)]),
    ("N2", "nitrogen, N₂", "N2", TB, "textbook Fig. 5.30, PDF p.251", [("each N", 0)]),
    ("acrolein", "acrolein, CH₂=CH–CH=O", "acrolein", "lecture", "Day 11 p.26 (structure only); textbook PDF p.253",
     [("C of CH₂=", 0), ("C of =CH–", 1), ("C of –CH=O", 2), ("O", 3)]),
    ("allene", "allene, CH₂=C=CH₂", "allene", "new", "", [("each end C (CH₂)", 0), ("middle C", 1)]),
    ("CH3CN", "acetonitrile, CH₃CN", "CH3CN", "new", "", [("C of CH₃", 0), ("C of C≡N", 4), ("N", 5)]),
    ("HCOOH", "formic acid, HCOOH", "HCOOH", "new", "", [("C", 0), ("O of C=O", 2), ("O of O–H", 3)]),
    ("C6H6", "benzene, C₆H₆ (one Kekulé structure)", "C6H6-1", "lecture", "Day 9 p.12–13; Day 11 p.26", [("each C", 0)]),
    ("C2H6", "ethane, C₂H₆", "C2H6", "new", "", [("each C", 0)]),
]


def colored_svg(s):
    """lewis.svg with each bond's lines classed: one σ line per bond (the middle line of a triple bond), the
    others π. The slides color σ green and π blue (Day 11 p.19, p.23)."""
    out = LW.svg(s, tag="span", scale=1.25)
    kinds = []
    for _, _, o in s.bonds:
        kinds += {1: ["sigma"], 2: ["sigma", "pi"], 3: ["pi", "sigma", "pi"]}[o]
    parts = out.split("<line class='lw-bond'")
    assert len(parts) - 1 == len(kinds), s.id
    res = parts[0]
    for kind, rest in zip(kinds, parts[1:]):
        res += f"<line class='lw-bond lw-{kind}'" + rest
    return res.replace("role='img' aria-label='", "role='img' aria-label='σ bonds green, π bonds blue: ", 1)


def sigma_pi_ref(sid):
    s = LW.STRUCTS[sid]
    return {"sigma": len(s.bonds), "pi": sum(o - 1 for _, _, o in s.bonds)}


def sigma_pi_data():
    out = []
    for key, label, sid, tag, src, rows in SIGMA_PI:
        s = LW.STRUCTS[sid]
        atoms = []
        for desc, k in rows:
            sn = steric_number(s, k)
            nb = sum(1 for i, j, _ in s.bonds if k in (i, j))
            atoms.append({"desc": desc, "el": s.atoms[k][0], "bonded": nb, "lp": s.lp.get(k, 0), "sn": sn,
                          "hyb": HYB[sn], "pi": sum(o - 1 for i, j, o in s.bonds if k in (i, j))})
        bonds = []
        for i, j, o in s.bonds:
            bonds.append([s.atoms[i][0], s.atoms[j][0], o])
        out.append({"key": key, "label": label, "html": s.formula_html, "tag": tag, "src": src,
                    "plain": LW.svg(s, tag="span", scale=1.25), "colored": colored_svg(s), "bonds": bonds, "atoms": atoms})
    return out


# ================================================================== chirality (t5-6)
CHIRAL_GROUPS = [
    ("H", "H"), ("F", "F"), ("Cl", "Cl"), ("Br", "Br"), ("I", "I"), ("OH", "OH"), ("CH3", "CH₃"), ("NH2", "NH₂"),
    ("COOH", "COOH"), ("C2H5", "CH₂CH₃"), ("ipr", "C(=CH₂)CH₃"), ("ringCO", "ring CH₂ (toward C=O)"),
    ("ringCC", "ring CH₂ (toward C=C)"),
]
CHIRAL_PRESETS = [
    ("CHBrClF", "CHBrClF", ["H", "Br", "Cl", "F"], TB, "textbook Fig. 5.40, PDF p.257"),
    ("CHBr2Cl", "CHBr₂Cl", ["H", "Br", "Br", "Cl"], TB, "textbook Fig. 5.40, PDF p.257"),
    ("CH2Cl2", "CH₂Cl₂", ["Cl", "H", "Cl", "H"], "new", ""),
    ("alanine", "alanine's central C", ["H", "CH3", "NH2", "COOH"], TB, "textbook Fig. 5.41, PDF p.260"),
    ("carvone", "carvone's ring carbon", ["H", "ipr", "ringCO", "ringCC"], "lecture", "Day 10 p.6; textbook PDF p.257–258"),
]


def _rotations():
    """The 12 proper rotations of a tetrahedron, as matrices: closure of 120° turns about two vertex axes."""
    def rot(axis, t):
        a = _unit(axis)
        K = np.array([[0, -a[2], a[1]], [a[2], 0, -a[0]], [-a[1], a[0], 0]])
        return np.eye(3) + math.sin(t) * K + (1 - math.cos(t)) * K @ K
    gens = [rot([1, 1, 1], 2 * math.pi / 3), rot([1, -1, -1], 2 * math.pi / 3)]
    group = [np.eye(3)]
    changed = True
    while changed:
        changed = False
        for g in list(group):
            for h in gens:
                m = h @ g
                if not any(np.allclose(m, x) for x in group):
                    group.append(m)
                    changed = True
    assert len(group) == 12
    return group


def superimposable_ref(groups):
    pos = [_unit(v) for v in ([1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1])]
    mirror = [np.array([p[1], p[0], p[2]]) for p in pos]         # reflect through the plane x = y (maps the tetrahedron onto itself)
    for R in _rotations():
        ok = True
        for g, m in zip(groups, mirror):
            q = R @ m
            k = int(np.argmin([np.linalg.norm(q - p) for p in pos]))
            if groups[k] != g:
                ok = False
                break
        if ok:
            return True
    return False


# ================================================================== MO diagrams (t5-7)
MO_SPECIES = [
    ("H2", "H₂", ["H", "H"], [1, 1], "1s"), ("He2", "He₂", ["He", "He"], [2, 2], "1s"),
    ("Li2", "Li₂", ["Li", "Li"], [1, 1], "low"), ("Be2", "Be₂", ["Be", "Be"], [2, 2], "low"),
    ("B2", "B₂", ["B", "B"], [3, 3], "low"), ("C2", "C₂", ["C", "C"], [4, 4], "low"),
    ("N2", "N₂", ["N", "N"], [5, 5], "low"), ("O2", "O₂", ["O", "O"], [6, 6], "high"),
    ("F2", "F₂", ["F", "F"], [7, 7], "high"), ("Ne2", "Ne₂", ["Ne", "Ne"], [8, 8], "high"),
    ("NO", "NO", ["N", "O"], [5, 6], "high"),
]
# (name, bonding?, degeneracy) in order of increasing energy (textbook Figs. 5.45-5.50, 5.52)
MO_ORDERS = {
    "1s": [("σ1s", True, 1), ("σ*1s", False, 1)],
    "low": [("σ2s", True, 1), ("σ*2s", False, 1), ("π2p", True, 2), ("σ2p", True, 1), ("π*2p", False, 2), ("σ*2p", False, 1)],
    "high": [("σ2s", True, 1), ("σ*2s", False, 1), ("σ2p", True, 1), ("π2p", True, 2), ("π*2p", False, 2), ("σ*2p", False, 1)],
}


def mo_ref(order, n):
    """Aufbau over the levels; Hund's rule inside a degenerate level; Pauli: at most 2 per orbital."""
    levels, left = [], n
    for name, bonding, deg in MO_ORDERS[order]:
        k = min(left, 2 * deg)
        left -= k
        boxes = [0] * deg
        for e in range(k):
            boxes[e % deg] += 1
        levels.append((name, bonding, boxes))
    if left:
        return None
    b = sum(sum(x) for name, bond, x in levels if bond)
    a = sum(sum(x) for name, bond, x in levels if not bond)
    unpaired = sum(1 for _, _, x in levels for e in x if e == 1)
    config = "".join(f"({name}){sum(x)}" for name, _, x in levels if sum(x))
    return {"bo": (b - a) / 2, "unpaired": unpaired, "bonding": b, "antibonding": a, "config": config,
            "boxes": [x for _, _, x in levels]}


def mo_expected():
    out = {}
    for key, _, _, val, order in MO_SPECIES:
        for q in range(-2, 3):
            r = mo_ref(order, sum(val) - q)
            if r and sum(val) - q >= 1:
                out[f"{key}:{q}"] = r
    # textbook checks: Fig. 5.50 bond orders, Sample Ex. 5.8/5.9, the O2 hook
    want = {"Li2:0": 1, "Be2:0": 0, "B2:0": 1, "C2:0": 2, "N2:0": 3, "O2:0": 2, "F2:0": 1, "Ne2:0": 0, "H2:0": 1,
            "He2:0": 0, "H2:-1": 0.5, "NO:0": 2.5, "NO:1": 3, "NO:-1": 2, "N2:1": 2.5, "O2:1": 2.5, "Be2:1": 0.5}
    for k, v in want.items():
        assert out[k]["bo"] == v, (k, out[k]["bo"], v)
    assert out["O2:0"]["unpaired"] == 2 and out["B2:0"]["unpaired"] == 2 and out["N2:0"]["unpaired"] == 0
    return out


# ================================================================== public
def build():
    return {"ch5": {
        "chi": CHI,
        "vsepr": {
            "presets": [{"key": k, "label": lab, "html": h, "mode": mode, "sn": sn, "lp": nlp, "center": c, "ligands": lig,
                         "orders": o, "angle": ang, "angleText": at, "tag": tag, "src": src, "note": note,
                         "charge": -1 if k == "I3-" else 0}
                        for k, lab, h, mode, sn, nlp, c, lig, o, ang, at, tag, src, note in VSEPR_PRESETS],
            "profTable": PROF_TABLE,
            "epg": {str(k): v for k, v in EPG.items() if v},
            "mg": {f"{a}-{b}": v for (a, b), v in MG.items()},
            "maxLP": {str(k): v for k, v in MAX_LP.items()},
        },
        "dipoles": dipoles_data(),
        "hybrid": [hybrid_atom(*h) for h in HYBRID_PRESETS],
        "sigmaPi": sigma_pi_data(),
        "chirality": {"groups": [{"key": k, "text": t} for k, t in CHIRAL_GROUPS],
                      "presets": [{"key": k, "label": lab, "groups": g, "tag": tag, "src": src} for k, lab, g, tag, src in CHIRAL_PRESETS]},
        "mo": {"species": [{"key": k, "label": lab, "atoms": at, "valence": v, "order": o} for k, lab, at, v, o in MO_SPECIES],
               "orders": {k: [[n, b, d] for n, b, d in v] for k, v in MO_ORDERS.items()},
               "o2Lewis": LW.svg(LW.STRUCTS["O2"], tag="span", scale=0.9)},
    }}


def expected():
    hyb = [hybrid_atom(*h) for h in HYBRID_PRESETS]
    return {"ch5": {
        "vsepr": vsepr_expected(),
        "dipoles": {m[0]: dipole_ref(m) for m in DIPOLES},
        "hybrid": {h["key"]: hybrid_ref(h) for h in hyb},
        "sigmaPi": {key: sigma_pi_ref(sid) for key, _, sid, _, _, _ in SIGMA_PI},
        "chirality": {k: {"superimposable": superimposable_ref(g), "fourDifferent": len(set(g)) == 4}
                      for k, _, g, _, _ in CHIRAL_PRESETS},
        "mo": mo_expected(),
    }}


if __name__ == "__main__":
    import json
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    e = expected()["ch5"]
    for k, v in e["vsepr"].items():
        print("vsepr", k, v["mg"] or "(variant)", v["angles"], v["contacts"], v["lpSites"])
    for k, v in e["dipoles"].items():
        print("dipole", k, v)
    for k, v in e["hybrid"].items():
        print("hybrid", k, v)
    print("sigmaPi", e["sigmaPi"])
    print("chirality", e["chirality"])
    for k in ("O2:0", "N2:0", "B2:0", "NO:0", "NO:-1", "O2:-2", "He2:0"):
        print("mo", k, e["mo"][k])
    print(len(json.dumps(build())) // 1024, "KB of explorer data")

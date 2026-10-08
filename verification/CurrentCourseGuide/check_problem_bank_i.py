"""Independent re-derivation of every computed key in problem_bank_i.py (m20 VSEPR, m21 lone pairs, m22 polarity).

    py -3.11 verification/CurrentCourseGuide/check_problem_bank_i.py

The bank takes steric numbers from lewis.py's drawn lone pairs and looks shapes up in the lecture's table. This script
uses none of that:
  1. Species come from SMILES typed here (RDKit, unsanitized so hypervalent atoms parse). The central atom's lone pairs
     are (valence electrons − formal charge − bond orders) / 2, and SN = neighbors + lone pairs.
  2. Electron-pair arrangements come from minimizing 1/r repulsion of SN points on a sphere (the Thomson problem),
     not from a table; the resulting angles are checked (180°, 120°, 109.47°, 90°/120°/180°, 90°/180°).
  3. Lone pairs are placed by trying every placement on the ideal points and keeping the lowest weighted repulsion
     (pair weight = product of sizes, lone pair 1.6 and bonding pair 1: LL 2.56 > LB 1.6 > BB 1; energy ∝ 1/d⁶).
  4. Shape names come from the bond-angle signature of the atoms left over, not from (SN, lone pairs).
  5. Polarity is the vector sum of bond dipoles of size Δχ (course values, retyped here from Day 9 p.17) pointing to
     the more electronegative atom; |sum| > 1e-6 → polar. Directions are read off the same sums.
  6. Angle trends (lone pairs and double bonds squeeze angles) relax the ideal arrangement in a points-on-a-sphere
     model in which a lone pair (1.6) or a double bond (1.3) is a "bigger" charge than a single bond (1); RDKit MMFF
     geometries are a second check where the force field has parameters (CH2O, COCl2).
Then every key in the bank is compared with these results. Exit status 1 on any disagreement.
"""
import itertools
import math
import os
import sys

import numpy as np
from scipy.optimize import minimize

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.stdout.reconfigure(encoding="utf-8")

from rdkit import Chem                      # noqa: E402
from rdkit.Chem import AllChem              # noqa: E402

import problem_bank_i as B                  # noqa: E402  (the keys under test)

CHI = {"H": 2.1, "B": 2.0, "C": 2.5, "N": 3.0, "O": 3.5, "F": 4.0, "P": 2.1, "S": 2.5, "Cl": 3.0, "Se": 2.4,
       "Br": 2.8, "I": 2.5, "Al": 1.5, "Be": 1.5}          # Day 9 p.17; no value for Xe (noble gases omitted)
VAL = {"H": 1, "Be": 2, "B": 3, "Al": 3, "C": 4, "N": 5, "P": 5, "O": 6, "S": 6, "Se": 6, "F": 7, "Cl": 7, "Br": 7,
       "I": 7, "Xe": 8, "Kr": 8, "Te": 6}
XE_PLACEHOLDER = 2.6                       # any value (Xe, Kr): a symmetric set of identical bonds cancels whatever the bond dipole is

# species: id -> (SMILES written here, central atom symbol)
SPECIES = {
    "HCN": ("[H]C#N", "C"), "CO2": ("O=C=O", "C"), "BF3": ("FB(F)F", "B"), "BCl3": ("ClB(Cl)Cl", "B"),
    "CCl4": ("ClC(Cl)(Cl)Cl", "C"), "PF5": ("FP(F)(F)(F)F", "P"), "SF6": ("FS(F)(F)(F)(F)F", "S"),
    "CH2O": ("[H]C([H])=O", "C"), "COCl2": ("O=C(Cl)Cl", "C"), "CH4": ("[H]C([H])([H])[H]", "C"),
    "NO3-": ("[O-][N+](=O)[O-]", "N"), "NH4+": ("[H][N+]([H])([H])[H]", "N"), "NO2+": ("O=[N+]=O", "N"),
    "SO4-exp": ("O=S(=O)([O-])[O-]", "S"), "SO4-oct": ("[O-][S+2]([O-])([O-])[O-]", "S"),
    "BrF3": ("FBr(F)F", "Br"), "PH3": ("[H]P([H])[H]", "P"), "H2S": ("[H]S[H]", "S"), "H3O+": ("[H][O+]([H])[H]", "O"),
    "OF2": ("FOF", "O"), "NH3": ("[H]N([H])[H]", "N"), "NH2-": ("[H][N-][H]", "N"), "H2O": ("[H]O[H]", "O"),
    "SeF4": ("F[Se](F)(F)F", "Se"), "ICl4-": ("Cl[I-](Cl)(Cl)Cl", "I"),
    "XeF2": ("F[Xe]F", "Xe"), "XeF4": ("F[Xe](F)(F)F", "Xe"), "BrF5": ("FBr(F)(F)(F)F", "Br"),
    "SO3-oct": ("[O-][S+]([O-])[O-]", "S"), "SO3-exp": ("O=S([O-])[O-]", "S"), "CO3": ("[O-]C(=O)[O-]", "C"),
    "PCl3": ("ClP(Cl)Cl", "P"), "NF3": ("FN(F)F", "N"), "SO2": ("O=[S+][O-]", "S"), "CH3Cl": ("[H]C([H])([H])Cl", "C"),
    "CH2Cl2": ("[H]C([H])(Cl)Cl", "C"), "CHCl3": ("[H]C(Cl)(Cl)Cl", "C"), "CCl3F": ("FC(Cl)(Cl)Cl", "C"),
    "PCl5": ("ClP(Cl)(Cl)(Cl)Cl", "P"), "SF4": ("FS(F)(F)F", "S"), "SF5Cl": ("FS(F)(F)(F)(F)Cl", "S"),
    "HF": ("[H]F", "F"), "CF4": ("FC(F)(F)F", "C"),
    # replacements after the textbook-overlap check (2026-10-06)
    "AlCl3": ("Cl[Al](Cl)Cl", "Al"), "AlCl4-": ("Cl[Al-](Cl)(Cl)Cl", "Al"), "HCO2-": ("[H]C(=O)[O-]", "C"),
    "BrF4-": ("F[Br-](F)(F)F", "Br"), "ClF5": ("FCl(F)(F)(F)F", "Cl"), "KrF2": ("F[Kr]F", "Kr"), "TeF5-": ("F[Te-](F)(F)(F)F", "Te"),
    "PF3": ("FP(F)F", "P"), "H2Se": ("[H][Se][H]", "Se"), "BH4-": ("[H][B-]([H])([H])[H]", "B"), "SeF6": ("F[Se](F)(F)(F)(F)F", "Se"),
    "CH3F": ("[H]C([H])([H])F", "C"), "CH2F2": ("[H]C([H])(F)F", "C"), "CHF3": ("[H]C(F)(F)F", "C"),
}

FAIL = []
ROWS = []


def check(what, got, want):
    ok = (abs(got - want) < 1e-6) if isinstance(want, (int, float)) and isinstance(got, (int, float)) and not isinstance(want, bool) else got == want
    ROWS.append((what, got, want, "ok" if ok else "MISMATCH"))
    if not ok:
        FAIL.append(what)


# ------------------------------------------------------------------ 1. lone pairs from SMILES
def center_info(sid):
    smi, el = SPECIES[sid]
    m = Chem.MolFromSmiles(smi, sanitize=False)
    m.UpdatePropertyCache(strict=False)
    cands = [a for a in m.GetAtoms() if a.GetSymbol() == el and a.GetDegree() + a.GetTotalNumHs() > 1] or \
            [a for a in m.GetAtoms() if a.GetSymbol() == el]
    c = max(cands, key=lambda a: a.GetDegree() + a.GetTotalNumHs())
    outer = [n.GetSymbol() for n in c.GetNeighbors()] + ["H"] * c.GetTotalNumHs()
    bo = sum(b.GetBondTypeAsDouble() for b in c.GetBonds()) + c.GetTotalNumHs()
    nonbond = VAL[el] - c.GetFormalCharge() - bo
    assert nonbond >= 0 and nonbond % 2 == 0, (sid, nonbond)
    return {"center": el, "outer": outer, "lp": int(nonbond // 2), "sn": len(outer) + int(nonbond // 2)}


# ------------------------------------------------------------------ 2. Thomson arrangements
def thomson(n, starts=40, seed=1):
    rng = np.random.default_rng(seed)

    def pts(x):
        th, ph = x[:n], x[n:]
        return np.stack([np.sin(th) * np.cos(ph), np.sin(th) * np.sin(ph), np.cos(th)], axis=1)

    def energy(x):
        p = pts(x)
        e = 0.0
        for i in range(n):
            for j in range(i + 1, n):
                e += 1 / np.linalg.norm(p[i] - p[j])
        return e
    best = None
    for _ in range(starts):
        x0 = np.concatenate([np.arccos(rng.uniform(-1, 1, n)), rng.uniform(0, 2 * np.pi, n)])
        r = minimize(energy, x0, method="L-BFGS-B")
        if best is None or r.fun < best.fun - 1e-9:
            best = r
    return pts(best.x)


def angle(u, v):
    return math.degrees(math.acos(max(-1.0, min(1.0, float(np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v)))))))


def signature(vecs):
    return sorted(round(angle(vecs[i], vecs[j]) * 2) / 2 for i in range(len(vecs)) for j in range(i + 1, len(vecs)))


# exact polyhedra, used below; each is checked against the numerically minimized arrangement (same angle set)
_t = [(math.cos(math.radians(a)), math.sin(math.radians(a)), 0.0) for a in (0, 120, 240)]
POLY = {2: np.array([(0, 0, 1.0), (0, 0, -1.0)]),
        3: np.array(_t),
        4: np.array([(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]) / math.sqrt(3),
        5: np.array([(0, 0, 1.0), (0, 0, -1.0)] + _t),
        6: np.array([(1.0, 0, 0), (-1.0, 0, 0), (0, 1.0, 0), (0, -1.0, 0), (0, 0, 1.0), (0, 0, -1.0)])}
for n in range(2, 7):
    check(f"Thomson minimum for {n} points has the angle set of the ideal shape", signature(thomson(n)), signature(POLY[n]))
check("tetrahedral angle arccos(−1/3)", round(math.degrees(math.acos(-1 / 3)), 2), 109.47)


def classify(vecs):
    """shape name from the angle signature of the positions occupied by atoms."""
    s = signature(vecs)
    k = len(vecs)
    if k == 2:
        return "linear" if s == [180.0] else "bent"
    if k == 3:
        if s == [120.0] * 3:
            return "trigonal planar"
        if s == [90.0, 90.0, 180.0]:
            return "T-shaped"
        if len(set(s)) == 1 and s[0] < 120:
            return "trigonal pyramidal"
    if k == 4:
        if s == [109.5] * 6:
            return "tetrahedral"
        if s == [90.0] * 4 + [180.0] * 2:
            return "square planar"
        if s == [90.0] * 4 + [120.0, 180.0]:
            return "seesaw"
    if k == 5:
        if s == [90.0] * 6 + [120.0] * 3 + [180.0]:
            return "trigonal bipyramidal"
        if s == [90.0] * 8 + [180.0] * 2:
            return "square pyramidal"
    if k == 6 and s == [90.0] * 12 + [180.0] * 3:
        return "octahedral"
    return "?" + str(s)


# ------------------------------------------------------------------ 3. lone-pair placement
# pair weight = product of "sizes" (lone pair 1.6, bonding pair 1): LL 2.56 > LB 1.6 > BB 1. (Weights like 3/2/1, with
# LL − 2·LB + BB = 0, make cis and trans lone pairs at SN 6 exactly degenerate, so the product form matters.)
SIZE = {"L": 1.6, "B": 1.0}
W = {(a, b): SIZE[a] * SIZE[b] for a in "LB" for b in "LB"}


def place(sn, lp):
    P = POLY[sn]
    best = None
    for combo in itertools.combinations(range(sn), lp):
        kind = ["L" if i in combo else "B" for i in range(sn)]
        e = sum(W[(kind[i], kind[j])] / np.linalg.norm(P[i] - P[j]) ** 6 for i in range(sn) for j in range(i + 1, sn))
        shape = classify([P[i] for i in range(sn) if kind[i] == "B"])
        if best is None or e < best[0] - 1e-9:
            best = (e, combo, shape)
        elif abs(e - best[0]) < 1e-9:
            assert shape == best[2], ("degenerate placements give different shapes", sn, lp)
    return best


def geometry(sid):
    ci = center_info(sid)
    e, combo, shape = place(ci["sn"], ci["lp"])
    P = POLY[ci["sn"]]
    bonded = [P[i] for i in range(ci["sn"]) if i not in combo]
    lps = [P[i] for i in combo]
    return {**ci, "epg": classify(list(P)), "mg": shape, "bonded": bonded, "lps": lps}


# ------------------------------------------------------------------ 5. dipole sums
def dipole(sid, outer_order=None):
    g = geometry(sid)
    outer = outer_order or g["outer"]
    cc = CHI.get(g["center"], XE_PLACEHOLDER)
    net = np.zeros(3)
    for el, u in zip(outer, g["bonded"]):
        net += (CHI[el] - cc) * u / np.linalg.norm(u)
    return net, g, outer


def polar(sid):
    if sid == "HF":
        return True
    net, _, _ = dipole(sid)
    return float(np.linalg.norm(net)) > 1e-6


# ------------------------------------------------------------------ 6. relaxed points-on-a-sphere angle model
def sphere_model(sizes, start, n=6):
    """relax the ideal arrangement `start` (rows in the same order as sizes) by minimizing Σ s_i s_j / d_ij^n over unit
    vectors; sizes: 1 single bond, 1.3 double bond, 1.6 lone pair. Local minimization keeps the lone-pair placement."""
    k = len(sizes)
    s = np.array(sizes)
    start = np.asarray(start, dtype=float)
    th0 = np.arccos(np.clip(start[:, 2], -1, 1))
    ph0 = np.arctan2(start[:, 1], start[:, 0])
    rng = np.random.default_rng(3)

    def pts(x):
        th, ph = x[:k], x[k:]
        return np.stack([np.sin(th) * np.cos(ph), np.sin(th) * np.sin(ph), np.cos(th)], axis=1)

    def energy(x):
        p = pts(x)
        e = 0.0
        for i in range(k):
            for j in range(i + 1, k):
                e += s[i] * s[j] / np.linalg.norm(p[i] - p[j]) ** n
        return e
    x0 = np.concatenate([th0, ph0]) + rng.normal(0, 1e-3, 2 * k)      # nudge off the poles' degenerate angles
    r = minimize(energy, x0, method="BFGS", options={"gtol": 1e-10, "maxiter": 5000})
    return pts(r.x)


def start_for(sn, lp_idx, order):
    """ideal positions for SN regions, lone pairs at lp_idx, returned in `order` ('L'/'B' per row)."""
    P = POLY[sn]
    L = [P[i] for i in lp_idx]
    Bp = [P[i] for i in range(sn) if i not in lp_idx]
    out, li, bi = [], 0, 0
    for o in order:
        if o == "L":
            out.append(L[li]); li += 1
        else:
            out.append(Bp[bi]); bi += 1
    return np.array(out)


def mmff_angle(smiles, a, b, c):
    """MMFF94 optimized angle a–b–c (atom indices in the H-added molecule), or None if no parameters."""
    try:
        m = Chem.AddHs(Chem.MolFromSmiles(smiles))
        AllChem.EmbedMolecule(m, randomSeed=7)
        if AllChem.MMFFOptimizeMolecule(m, maxIters=2000) == -1:
            return None
        conf = m.GetConformer()
        from rdkit.Chem import rdMolTransforms
        return rdMolTransforms.GetAngleDeg(conf, a, b, c)
    except Exception:                                 # noqa: BLE001
        return None


# ------------------------------------------------------------------ bank keys
PB = {p["id"]: p for p in B.PROBLEMS[B.I_START:]}


def part(pid, k=None):
    a = PB[pid]["answer"]
    return a["parts"][k] if k is not None else a


def correct_html(spec):
    return next(o["html"] for o in spec["options"] if o["correct"])


def plain(h):
    import re
    return re.sub(r"<[^>]+>", "", h)


# ---------------- m20
g = geometry("HCN")
check("m20-attempt (a) SN of C in HCN", part("m20-attempt", 0)["value"], g["sn"])
check("m20-attempt (b) H–C–N angle", part("m20-attempt", 1)["value"], round(angle(*g["bonded"]), 1))
rows = part("m20-p2")["rows"]
for r, sid in zip(rows, ["AlCl3", "AlCl4-", "NO2+", "PCl5", "SO4-exp"]):
    check(f"m20-p2 SN, {plain(r['html'].split('<span')[0]).strip()}", int(r["answer"]), center_info(sid)["sn"])
check("m20-p2 sulfate SN is the same for the octet structure", center_info("SO4-oct")["sn"], center_info("SO4-exp")["sn"])
g = geometry("HCO2-")                                     # the SMILES fixes one resonance structure; SN can't depend on which
check("m20-p3 (a) formate SN of C", part("m20-p3", 0)["value"], g["sn"])
check("m20-p3 (b) the other resonance structure", part("m20-p3", 1)["value"], center_info("HCO2-")["sn"])
check("m20-p3 (c) O–C–O angle", correct_html(part("m20-p3", 2)), f"about {round(angle(*g['bonded'][1:]))}°, the same for both structures")
P5 = POLY[5]
ax = [i for i in range(5) if any(abs(angle(P5[i], P5[j]) - 180) < 0.5 for j in range(5) if j != i)]
eq = [i for i in range(5) if i not in ax]
check("m20-p4 (a) axial positions", part("m20-p4", 0)["value"], len(ax))
check("m20-p4 (b) axial–equatorial", part("m20-p4", 1)["value"], round(angle(P5[ax[0]], P5[eq[0]])))
check("m20-p4 (c) equatorial–equatorial", part("m20-p4", 2)["value"], round(angle(P5[eq[0]], P5[eq[1]])))
check("m20-p4 (d) axial–axial", part("m20-p4", 3)["value"], round(angle(P5[ax[0]], P5[ax[1]])))
g = geometry("BCl3")
check("m20-p5 (a) SN of B", part("m20-p5", 0)["value"], g["sn"])
check("m20-p5 (b) shape", correct_html(part("m20-p5", 1)), g["mg"])
check("m20-p5 (c) Cl–B–Cl", part("m20-p5", 2)["value"], round(angle(g["bonded"][0], g["bonded"][1])))
pl = sphere_model([1.3, 1.0, 1.0], POLY[3])           # C=O, C–H, C–H
hch, hco = angle(pl[1], pl[2]), angle(pl[0], pl[1])
check("m20-p6 (a) model: H–C=O larger than H–C–H", correct_html(part("m20-p6", 0)), "each H–C=O angle" if hco > hch else "the H–C–H angle")
check("m20-p6 (a) model: the three angles are planar (sum 360°)", round(hch + 2 * hco, 3), 360.0)
check("m20-p6 (b) (360° − 118°)/2", part("m20-p6", 1)["value"], (360 - 118) / 2)
sn10 = 10 // 2                                            # single bonds only, no lone pairs: one pair per region
check("m20-p7 (a) 10 electrons → SN", part("m20-p7", 0)["value"], sn10)
check("m20-p7 (b) arrangement of 5 regions", correct_html(part("m20-p7", 1)), classify(list(POLY[sn10])))
pf5 = center_info("PF5")
check("m20-p7 (c) PF5: 5 regions, 10 electrons around P", (correct_html(part("m20-p7", 2)), pf5["sn"], 2 * pf5["sn"]), ("PF<sub>5</sub>", sn10, 10))
g = geometry("COCl2")
check("m20-transfer (a) SN of C in COCl2", part("m20-transfer", 0)["value"], g["sn"])
check("m20-transfer (b) shape", correct_html(part("m20-transfer", 1)), g["mg"])
check("m20-transfer (c) model: Cl–C–Cl < 120°", correct_html(part("m20-transfer", 2)), "smaller than 120°" if hch < 120 else "?")
mm = mmff_angle("O=C(Cl)Cl", 2, 1, 3)
if mm is not None:
    check(f"m20-transfer MMFF Cl–C–Cl = {mm:.1f}° is below 120°", mm < 120, True)
mm = mmff_angle("C=O", 2, 0, 3)
if mm is not None:
    check(f"m20-p6 MMFF H–C–H in CH2O = {mm:.1f}° is below 120°", mm < 120, True)
check("m20-m-sanity: tetrahedral 109.47° > square 90°", min(signature(POLY[4])) > 90, True)

# ---------------- m21
g = geometry("BrF4-")
check("m21-attempt (a) SN of Br", part("m21-attempt", 0)["value"], g["sn"])
check("m21-attempt (b) electron-pair geometry", correct_html(part("m21-attempt", 1)), g["epg"])
check("m21-attempt (c) molecular geometry", correct_html(part("m21-attempt", 2)), g["mg"])
opts = {o["key"]: o["html"] for o in part("m21-p2")["options"]}
for r, sid in zip(part("m21-p2")["rows"], ["PF3", "H2Se", "H3O+", "OF2", "BH4-"]):
    check(f"m21-p2 shape of {plain(r['html'])}", opts[r["answer"]], geometry(sid)["mg"])
angs = {}
for key, lp in (("nh4", 0), ("nh3", 1), ("nh2", 2)):
    order = ["B", "B"] + ["B"] * (2 - lp) + ["L"] * lp
    pts_ = sphere_model([SIZE[o] for o in order], start_for(4, place(4, lp)[1], order))
    angs[key] = angle(pts_[0], pts_[1])
model_order = sorted(angs, key=lambda k: -angs[k])
check(f"m21-p3 model H–N–H angles {', '.join(f'{k} {v:.1f}°' for k, v in angs.items())}", part("m21-p3")["answerOrder"], model_order)
check("m21-p3 NH4+ / NH3 / NH2− lone pairs", [center_info(s)["lp"] for s in ("NH4+", "NH3", "NH2-")], [0, 1, 2])
g = geometry("SeF4")
check("m21-p4 (a) SN of Se", part("m21-p4", 0)["value"], g["sn"])
lp_pos = g["lps"][0]
n90 = sum(1 for v in POLY[5] if abs(angle(lp_pos, v) - 90) < 0.5)
check("m21-p4 (b) lone pair position (2 neighbors at 90° = equatorial)", correct_html(part("m21-p4", 1)), "equatorial" if n90 == 2 else "axial")
check("m21-p4 (c) shape", correct_html(part("m21-p4", 2)), g["mg"])
g = geometry("ClF5")
check("m21-p5 (a) SN", part("m21-p5", 0)["value"], g["sn"])
e_one = [sum(W[("L" if i == c else "B", "L" if j == c else "B")] / np.linalg.norm(POLY[6][i] - POLY[6][j]) ** 6
             for i in range(6) for j in range(i + 1, 6)) for c in range(6)]
check("m21-p5 (b) every lone-pair position on the octahedron has the same energy", correct_html(part("m21-p5", 1)),
      "No: all six positions are equivalent." if max(e_one) - min(e_one) < 1e-9 else "?")
check("m21-p5 (c) shape", correct_html(part("m21-p5", 2)), g["mg"])
e1, combo1, _ = place(5, 1)
n90 = sum(1 for v in POLY[5] if abs(angle(POLY[5][combo1[0]], v) - 90) < 0.5)
check("m21-p6 one lone pair at SN 5 goes equatorial", correct_html(part("m21-p6")), "an equatorial position" if n90 == 2 else "an axial position")
def lb90(lp_sites):
    return sum(1 for i in lp_sites for j in range(5) if j not in lp_sites and abs(angle(P5[i], P5[j]) - 90) < 0.5)


check("m21-p7 (a) 90° lone pair–bond contacts, both lone pairs equatorial", part("m21-p7", 0)["value"], lb90(eq[:2]))
check("m21-p7 (b) 90° lone pair–bond contacts, both lone pairs axial", part("m21-p7", 1)["value"], lb90(ax))
_, combo2, shape2 = place(5, 2)
check("m21-p7 (c) lowest-energy placement of two lone pairs: both equatorial, T-shaped", correct_html(part("m21-p7", 2)),
      "(i), giving a T-shaped molecule" if set(combo2) <= set(eq) and shape2 == "T-shaped" else "?")
g = geometry("KrF2")
check("m21-p8 (a) SN", part("m21-p8", 0)["value"], g["sn"])
check("m21-p8 (b) shape", correct_html(part("m21-p8", 1)), g["mg"])
check("m21-p9 TeF5− and ICl4−: lone pairs on the central atom", (center_info("TeF5-")["lp"], center_info("ICl4-")["lp"]), (1, 2))
order = ["L"] + ["B"] * 5                                # square pyramid (TeF5−, like BrF5): lone pair + 5 bonds
sp = sphere_model([SIZE[o] for o in order], start_for(6, place(6, 1)[1], order))
axf = max(range(1, 6), key=lambda i: angle(sp[0], sp[i]))
eqf = [i for i in range(1, 6) if i != axf]
brf5 = np.mean([angle(sp[axf], sp[i]) for i in eqf])
order = ["L", "L"] + ["B"] * 4                           # square planar (ICl4−, like XeF4): two lone pairs (placed by step 3) + 4 bonds
sq = sphere_model([SIZE[o] for o in order], start_for(6, place(6, 2)[1], order))
xef4 = sorted(round(angle(sq[i], sq[j]), 1) for i in range(2, 6) for j in range(i + 1, 6))
check(f"m21-p9 (a) model: square pyramid axial–equatorial {brf5:.1f}°", correct_html(part("m21-p9", 0)), "smaller than 90°" if brf5 < 89.5 else "?")
check(f"m21-p9 (b) model: square planar X–A–X angles {xef4}", correct_html(part("m21-p9", 1)), "exactly 90°" if xef4 == [90.0] * 4 + [180.0] * 2 else "?")
for k, sid in ((0, "SO3-oct"), (1, "SO3-exp")):
    check(f"m21-transfer ({'ab'[k]}) SN of S, {sid}", part("m21-transfer", k)["value"], geometry(sid)["sn"])
check("m21-transfer (c) shape", correct_html(part("m21-transfer", 2)), geometry("SO3-oct")["mg"])
check("m21-transfer carbonate, for contrast, is trigonal planar", geometry("CO3")["mg"], "trigonal planar")
pairs = {"H<sub>2</sub>O and H<sub>2</sub>S": ("H2O", "H2S"), "NH<sub>3</sub> and BF<sub>3</sub>": ("NH3", "BF3"),
         "CH<sub>4</sub> and XeF<sub>4</sub>": ("CH4", "XeF4"), "CO<sub>2</sub> and XeF<sub>2</sub>": ("CO2", "XeF2")}
fits = [h for h, (a, b) in pairs.items() if geometry(a)["mg"] == geometry(b)["mg"] and geometry(a)["epg"] != geometry(b)["epg"]]
check("m21-m-recognize: the only pair with the same shape and different electron-pair geometries", [correct_html(part("m21-m-recognize"))], fits)
of2 = sphere_model([1.0, 1.0, 1.6, 1.6], start_for(4, place(4, 2)[1], ["B", "B", "L", "L"]))
check(f"m21-m-sanity model F–O–F = {angle(of2[0], of2[1]):.1f}° < 109.47°", angle(of2[0], of2[1]) < 109.47, True)

# ---------------- m22
g = geometry("PCl3")
check("m22-attempt (a) shape", correct_html(part("m22-attempt", 0)), g["mg"])
check("m22-attempt (b) polarity", correct_html(part("m22-attempt", 1)), "polar" if polar("PCl3") else "nonpolar")
for r, sid in zip(part("m22-p2")["rows"], ["BF3", "NF3", "SF6", "OF2", "XeF2"]):
    check(f"m22-p2 {plain(r['html'])}", r["answer"], "polar" if polar(sid) else "nonpolar")
for r, sid in zip(part("m22-p3")["rows"], ["CH4", "CH3F", "CH2F2", "CHF3", "CF4"]):
    check(f"m22-p3 {plain(r['html'])}", r["answer"], "polar" if polar(sid) else "nonpolar")
for k, sid, el, want in ((0, "CH3Cl", "Cl", "toward the Cl atom"), (1, "CH2F2", "F", "toward the F atoms, along the line that bisects the F–C–F angle")):
    net, g, outer = dipole(sid)
    side = sum(u for o, u in zip(outer, g["bonded"]) if o == el)
    check(f"m22-p4 ({'ab'[k]}) {sid}: net dipole points to the {el} side", correct_html(part("m22-p4", k)), want if float(np.dot(net, side)) > 1e-9 else "?")
net, g, outer = dipole("PCl5")
P5b = g["bonded"]
axb = [i for i in range(5) if any(abs(angle(P5b[i], P5b[j]) - 180) < 0.5 for j in range(5) if j != i)]
eqb = [i for i in range(5) if i not in axb]
ax_sum = np.linalg.norm(sum(P5b[i] for i in axb))
eq_sum = np.linalg.norm(sum(P5b[i] for i in eqb))
check("m22-p5 PCl5: axial pair and equatorial triangle each cancel", (round(float(ax_sum), 6), round(float(eq_sum), 6), polar("PCl5")), (0.0, 0.0, False))
check("m22-p5 key", correct_html(part("m22-p5")).startswith("The three equatorial dipoles"), True)
dHF, dOH = abs(CHI["H"] - CHI["F"]), abs(CHI["O"] - CHI["H"])
check("m22-p6 (a) more polar bond", plain(correct_html(part("m22-p6", 0))).startswith("H–F"), dHF > dOH)
SLIDE_T52 = {"HF": 1.82, "H2O": 1.85, "NH3": 1.47, "CHCl3": 1.01, "CCl3F": 0.45}     # Day 11 p.8, retyped
check("m22-p6 Table 5.2 values in the bank", B.TAB52, SLIDE_T52)
check("m22-p6 (b) larger dipole moment", plain(correct_html(part("m22-p6", 1))).startswith("H2O"), SLIDE_T52["H2O"] > SLIDE_T52["HF"])
check("m22-p7 polar one of SeF4 / SeF6", correct_html(part("m22-p7")), "SeF<sub>4</sub> only" if polar("SeF4") and not polar("SeF6") else "?")
dHCl = abs(CHI["H"] - CHI["Cl"])
check(f"m22-p8 Δχ H–Cl {dHCl:.1f} < H–F {dHF:.1f}: HCl's dipole is smaller", correct_html(part("m22-p8")).startswith("Smaller") and dHCl < dHF, True)
net, g, outer = dipole("H2O")
check("m22-p9 (a) water's δ− (O) end faces the positive plate", correct_html(part("m22-p9", 0)),
      "with the O end toward the positive plate" if float(np.dot(net, sum(g["bonded"]))) < 0 else "?")
check("m22-p9 (b) 1.85 D × 3.34e-30 C·m/D", round(part("m22-p9", 1)["value"] / 1e-30, 4), round(1.85 * 3.34, 4))
check("m22-p9 (b) sig figs", part("m22-p9", 1)["sigfigs"], 3)
g = geometry("SF5Cl")
check("m22-transfer (a) shape", correct_html(part("m22-transfer", 0)), g["mg"])
check("m22-transfer (b) polarity", correct_html(part("m22-transfer", 1)), "polar" if polar("SF5Cl") else "nonpolar")
for n in range(2, 7):
    check(f"m22-m-recognize: identical dipoles on the {n}-point arrangement cancel", round(float(np.linalg.norm(POLY[n].sum(axis=0))), 6), 0.0)
check("m22-m-recognize: XeF2 and XeF4 cancel too", (polar("XeF2"), polar("XeF4")), (False, False))
# CHCl3 and CCl3F: naive sums, with C–H nonpolar (the bank's numbers) and with C–H included
n1, g1, o1 = dipole("CHCl3")
n2, g2, o2 = dipole("CCl3F")
chcl3_with_ch = float(np.linalg.norm(n1))
cl_only = float(np.linalg.norm(sum((CHI["Cl"] - CHI["C"]) * u for el, u in zip(o1, g1["bonded"]) if el == "Cl")))
ccl3f = float(np.linalg.norm(n2))
check("m22-m-sanity naive CHCl3 (C–H nonpolar)", round(cl_only, 3), B.NAIVE_CHCl3)
check("m22-m-sanity naive CCl3F", round(ccl3f, 3), B.NAIVE_CCl3F)
check(f"m22-m-sanity naive CHCl3 with C–H counted = {chcl3_with_ch:.2f}: still below CCl3F", chcl3_with_ch < ccl3f, True)
# Table 5.2 directions, from the same sums
net, g, outer = dipole("H2O")
check("Table 5.2 H2O toward O", float(np.dot(net, sum(g["bonded"]))) < 0, True)
net, g, outer = dipole("NH3")
check("Table 5.2 NH3 toward N", float(np.dot(net, sum(g["bonded"]))) < 0, True)
check("Table 5.2 CHCl3 toward the Cl atoms", float(np.dot(n1, g1["bonded"][o1.index("H")])) < 0, True)
check("Table 5.2 CCl3F toward F", float(np.dot(n2, g2["bonded"][o2.index("F")])) > 0, True)
check("lecture Δχ: C–O 1.0, C–F 1.5, O–H 1.4 (Day 10 p.29–31)",
      [round(abs(CHI[a] - CHI[b]), 2) for a, b in (("C", "O"), ("C", "F"), ("O", "H"))], [1.0, 1.5, 1.4])
for sid in ("CO2", "CF4"):
    check(f"lecture: {sid} nonpolar", polar(sid), False)
check("lecture: H2O polar", polar("H2O"), True)

# ---------------- every species' shape vs. the bank's table lookup
MAP = {"HCN": "HCN", "CO2": "CO2", "BF3": "BF3", "BCl3": "BCl3", "CCl4": "CCl4", "PF5": "PF5", "SF6": "SF6", "CH2O": "CH2O",
       "COCl2": "COCl2", "CH4": "CH4", "NO3-": "NO3-1", "NH4+": "NH4+", "NO2+": "NO2+", "SO4-exp": "SO4-exp", "SO4-oct": "SO4-oct",
       "BrF3": "BrF3", "PH3": "PH3", "H2S": "H2S", "H3O+": "H3O+", "OF2": "OF2", "NH3": "NH3", "NH2-": "NH2-", "H2O": "H2O",
       "SeF4": "SeF4", "ICl4-": "ICl4-", "XeF2": "XeF2", "XeF4": "XeF4", "BrF5": "BrF5", "SO3-oct": "SO3-oct",
       "SO3-exp": "SO3-exp", "CO3": "CO3-1", "PCl3": "PCl3", "NF3": "NF3", "SO2": "SO2-1", "CH3Cl": "CH3Cl", "CH2Cl2": "CH2Cl2",
       "CHCl3": "CHCl3", "CCl3F": "CCl3F", "PCl5": "PCl5", "SF4": "SF4", "SF5Cl": "SF5Cl", "CF4": "CF4",
       "AlCl3": "AlCl3", "AlCl4-": "AlCl4-", "HCO2-": "HCO2-1", "BrF4-": "BrF4-", "ClF5": "ClF5", "KrF2": "KrF2", "PF3": "PF3",
       "H2Se": "H2Se", "BH4-": "BH4-", "SeF6": "SeF6", "CH3F": "CH3F", "CH2F2": "CH2F2", "CHF3": "CHF3"}
ZERO_DCHI = {"PH3"}   # χ(P) = χ(H) = 2.1: a Δχ sum gives no dipole at all (measured PH3 ≈ 0.57 D); no problem asks it
for k, sid in MAP.items():
    g, v = geometry(k), B.vsepr(sid)
    if k in ZERO_DCHI:
        check(f"{k}: SN / electron-pair / molecular geometry (polarity not compared: every Δχ is 0)", (g["sn"], g["epg"], g["mg"]),
              (v["sn"], v["epg"], v["mg"]))
        continue
    check(f"{k}: SN / electron-pair / molecular geometry / polar", (g["sn"], g["epg"], g["mg"], polar(k)),
          (v["sn"], v["epg"], v["mg"], B.is_polar(sid)))

w = max(len(r[0]) for r in ROWS)
for r in ROWS:
    print(f"{r[0]:<{w}}  {str(r[1])[:60]:<60}  {str(r[2])[:60]:<60}  {r[3]}")
print(f"\n{len(ROWS)} checks, {len(FAIL)} mismatches" + (":\n  " + "\n  ".join(FAIL) if FAIL else ""))
sys.exit(1 if FAIL else 0)

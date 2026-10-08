"""Independent check of problem_bank_j (m23 hybrid orbitals, m24 sigma and pi bonds).

    py -3.11 verification/CurrentCourseGuide/check_problem_bank_j.py

The bank computes its keys from the lewis.py structures. This script rebuilds every molecule from SMILES written
here (not from lewis.py), lets RDKit assign hybridization and bond orders, counts lone pairs from valence electrons,
formal charge, and bond orders, and compares the results with every hybridization, steric number, sigma/pi count,
lone-pair count, and angle key in the bank. It also checks that each sp / sp2 / sp3 choice marks the expected
option, and computes the hybrid-orbital angles from unit vectors with numpy. Exit status 1 on any mismatch.
"""
import os
import sys

import numpy as np
from rdkit import Chem

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.stdout.reconfigure(encoding="utf-8")

import problem_bank_g  # noqa: E402,F401
from problem_bank_a import PROBLEMS  # noqa: E402
import problem_bank_j as J  # noqa: E402

BY_ID = {p["id"]: p for p in PROBLEMS}
VAL = {"H": 1, "Be": 2, "B": 3, "C": 4, "N": 5, "O": 6, "F": 7, "P": 5, "S": 6, "Cl": 7}
RD_SN = {Chem.HybridizationType.SP: 2, Chem.HybridizationType.SP2: 3, Chem.HybridizationType.SP3: 4}
HYB_HTML = {2: "sp", 3: "sp<sup>2</sup>", 4: "sp<sup>3</sup>"}
KEY = {2: "sp", 3: "sp2", 4: "sp3"}
fails, n_checks = [], 0


def mol(smi):
    m = Chem.AddHs(Chem.MolFromSmiles(smi))
    Chem.Kekulize(m, clearAromaticFlags=True)
    return m


def counts(smi):
    """(sigma, pi) for the whole molecule: one sigma per bond, the extra bond order is pi."""
    m = mol(smi)
    return m.GetNumBonds(), sum(int(b.GetBondTypeAsDouble()) - 1 for b in m.GetBonds())


def atom_info(smi, idx):
    """(RDKit steric-number equivalent of its hybridization, SN from degree + lone pairs, lone pairs, pi bonds)"""
    m = mol(smi)
    a = m.GetAtomWithIdx(idx)
    order_sum = sum(int(b.GetBondTypeAsDouble()) for b in a.GetBonds())
    lp = (VAL[a.GetSymbol()] - a.GetFormalCharge() - order_sum) // 2
    return RD_SN[a.GetHybridization()], a.GetDegree() + lp, lp, order_sum - a.GetDegree()


def check(label, got, want):
    global n_checks
    n_checks += 1
    ok = got == want if not isinstance(want, float) else abs(got - want) < 1e-6 * max(1, abs(want))
    if not ok:
        fails.append(f"{label}: bank {got!r} vs independent {want!r}")


def part(pid, i):
    return BY_ID[pid]["answer"]["parts"][i]


def correct_html(spec):
    return next(o["html"] for o in spec["options"] if o["correct"])


def hyb_part(pid, i, smi, idx):
    rd, sn, _, _ = atom_info(smi, idx)
    check(f"{pid} part {i} ({smi} atom {idx}): RDKit vs SN", rd, sn)
    check(f"{pid} part {i} hybridization", correct_html(part(pid, i)), HYB_HTML[rd])


def num_part(pid, i, want):
    check(f"{pid} part {i}", part(pid, i)["value"], want)


# ---------------------------------------------------------------- m23
rd, sn, lp, _ = atom_info("[OH3+]", 0)                             # H3O+
num_part("m23-attempt", 0, sn)
hyb_part("m23-attempt", 1, "[OH3+]", 0)
num_part("m23-attempt", 2, 2 * lp + (sn - lp))
check("H3O+: electrons in O's hybrids = 6 − 1", 2 * lp + (sn - lp), VAL["O"] - 1)
num_part("m23-attempt", 3, lp)
check("m23-attempt (e)", correct_html(part("m23-attempt", 4)).startswith("an O sp<sup>3</sup> hybrid and an H 1s"), True)
check("m23-p1 (b)", "sp<sup>3</sup> hybrid and an H 1s" in correct_html(part("m23-p1", 1)), True)
# m23-p2: SN 3 → 3 hybrids, made from the 2s and SN − 1 = 2 of the three 2p orbitals; 3 − 2 = 1 p orbital is left
num_part("m23-p2", 0, 3)
num_part("m23-p2", 1, 3 - (3 - 1))
rd, sn, lp, _ = atom_info("CO", 1)                                 # methanol O (the audit moved m23-p5 off water)
num_part("m23-p5", 0, sn)
num_part("m23-p5", 1, lp)
num_part("m23-p5", 2, sn - lp)
num_part("m23-p5", 3, 2 * lp + (sn - lp))
check("m23-p5 electrons = O valence", 2 * lp + (sn - lp), VAL["O"])
P6 = [("C", 0), ("[NH4+]", 0), ("FN(F)F", 1), ("ClP(Cl)Cl", 1), ("FB(F)F", 1), ("Cl[Be]Cl", 1)]
P7 = [("S=C=S", 1), ("[O-][N+](=O)[O-]", 1), ("[S-]C#N", 1), ("[O-][S+]([O-])[O-]", 1), ("OCl", 0), ("[O-]C([O-])=O", 1), ("C=O", 1)]
for pid, table in (("m23-p6", P6), ("m23-p7", P7)):
    rows = BY_ID[pid]["answer"]["rows"]
    check(f"{pid} row count", len(rows), len(table))
    for r, (smi, idx) in zip(rows, table):
        rd, sn, _, _ = atom_info(smi, idx)
        check(f"{pid} {smi} atom {idx}: RDKit vs SN", rd, sn)
        check(f"{pid} {smi} atom {idx}", r["answer"], KEY[rd])
# SO2: the octet resonance structure gives S the same SN
# resonance forms give the same count: sulfite with one S=O, thiocyanate drawn S=C=N
check("SO3 2- with S=O, S", atom_info("O=S([O-])[O-]", 1)[:2], (4, 4))
check("SCN- as S=C=N, C", atom_info("S=C=[N-]", 1)[:2], (2, 2))


# hybrid angles from unit vectors
def angle(u, v):
    return float(np.degrees(np.arccos(np.dot(u, v) / np.linalg.norm(u) / np.linalg.norm(v))))


tet = [np.array(v, float) for v in ((1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1))]
tri = [np.array((np.cos(t), np.sin(t), 0.0)) for t in np.radians((90, 210, 330))]
lin = [np.array((0, 0, 1.0)), np.array((0, 0, -1.0))]
want_angles = {"a180": angle(*lin), "a120": angle(tri[0], tri[1]), "a109": angle(tet[0], tet[1]), "a90": angle(np.eye(3)[0], np.eye(3)[1])}
opts = {o["key"]: o["html"] for o in BY_ID["m23-p8"]["answer"]["options"]}
for k, v in want_angles.items():
    shown = float(opts[k].rstrip("°"))
    check(f"m23-p8 option {k} ({opts[k]}) vs {v:.2f}", abs(shown - v) < 0.05, True)
check("m23-p8 rows", [r["answer"] for r in BY_ID["m23-p8"]["answer"]["rows"]], ["a180", "a120", "a109", "a90"])
ANG_KEY = {2: "a180", 3: "a120", 4: "a109"}
for r, (smi, idx) in zip(BY_ID["m23-p8"]["answer"]["rows"], [("S=C=S", 1), ("[O-]C([O-])=O", 1), ("[NH4+]", 0)]):
    rd, sn, lp, _ = atom_info(smi, idx)
    check(f"m23-p8 {smi}: RDKit vs SN, no lone pairs", (rd, lp), (sn, 0))
    check(f"m23-p8 {smi}", r["answer"], ANG_KEY[rd])
# transfer: diamond-like C (four C neighbors, neopentane's center) and graphite-like C (coronene's inner ring)
hyb_part("m23-transfer", 0, "CC(C)(C)C", 1)
coronene = "c1cc2ccc3ccc4ccc5ccc6ccc1c7c2c3c4c5c67"
m_cor = mol(coronene)
inner = [a.GetIdx() for a in m_cor.GetAtoms() if a.GetSymbol() == "C" and all(n.GetSymbol() == "C" for n in a.GetNeighbors())]
check("coronene inner carbons", len(inner), 12)                   # 6 inner-ring + 6 ring-fusion carbons, none with H
rd, sn, lp, npi = atom_info(coronene, inner[0])
check("graphite-like C: RDKit vs SN", rd, sn)
check("m23-transfer part 1", correct_html(part("m23-transfer", 1)), HYB_HTML[rd])
num_part("m23-transfer", 2, round(angle(tri[0], tri[1]), 6))
num_part("m23-transfer", 3, VAL["C"] - 3)                          # 3 sigma electrons in sp2 hybrids, 1 in p

# ---------------------------------------------------------------- m24
s, p_ = counts("C=N")                                              # methanimine
num_part("m24-attempt", 0, s)
num_part("m24-attempt", 1, p_)
hyb_part("m24-attempt", 2, "C=N", 0)
hyb_part("m24-attempt", 3, "C=N", 1)
check("methanimine N lone pairs", atom_info("C=N", 1)[2], 1)
check("m24-attempt (e)", "unhybridized 2p orbitals on C and N" in correct_html(part("m24-attempt", 4)), True)
s, p_ = counts("C#C")
num_part("m24-p2", 0, s)
num_part("m24-p2", 1, p_)
hyb_part("m24-p2", 2, "C#C", 0)
hyb_part("m24-p3", 0, "[O-]N=O", 1)                                # nitrite N (the audit moved m24-p3 off diazene)
check("m24-p3 (b)", correct_html(part("m24-p3", 1)), "an sp<sup>2</sup> hybrid orbital")
_, _, lp_n, _ = atom_info("[O-]N=O", 1)
check("nitrite N lone pairs", lp_n, 1)
for i, smi in enumerate(("N#[N+][O-]", "O=CO", "NN")):
    s, p_ = counts(smi)
    num_part("m24-p4", 2 * i, s)
    num_part("m24-p4", 2 * i + 1, p_)
for i, smi in enumerate(("C=CC=O", "c1ccccc1")):
    s, p_ = counts(smi)
    num_part("m24-p5", 2 * i, s)
    num_part("m24-p5", 2 * i + 1, p_)
for k in range(4):                                                 # every heavy atom of acrolein is sp2
    check(f"acrolein atom {k}", atom_info("C=CC=O", k)[0], 3)
P6b = [("CC#N", 0), ("CC#N", 1), ("CC#N", 2), ("OC=O", 1), ("OC=O", 2), ("C=C=C", 0), ("C=C=C", 1)]
rows = BY_ID["m24-p6"]["answer"]["rows"]
check("m24-p6 row count", len(rows), len(P6b))
for r, (smi, idx) in zip(rows, P6b):
    rd, sn, _, _ = atom_info(smi, idx)
    check(f"m24-p6 {smi} atom {idx}: RDKit vs SN", rd, sn)
    check(f"m24-p6 {smi} atom {idx}", r["answer"], KEY[rd])
s, p_ = counts("CN=C=O")
num_part("m24-transfer", 0, s)
num_part("m24-transfer", 1, p_)
hyb_part("m24-transfer", 2, "CN=C=O", 1)
hyb_part("m24-transfer", 3, "CN=C=O", 2)
num_part("m24-transfer", 4, round(angle(*lin), 6))
check("N2O: every structure 2 sigma, 2 pi", (counts("[N-]=[N+]=O"), counts("N#[N+][O-]")), ((2, 2), (2, 2)))
_, _, _, pi_ch3 = atom_info("CC#N", 0)
_, _, _, pi_n = atom_info("CC#N", 2)
check("m24-m-recognize: CH3 carbon pi bonds", pi_ch3, 0)
check("m24-m-recognize: nitrile N pi bonds", pi_n, 2)
check("m24-m-recognize key", "CH<sub>3</sub> carbon" in correct_html(BY_ID["m24-m-recognize"]["answer"]), True)
check("m24-m-sanity: CO counts", counts("[C-]#[O+]"), (1, 2))
check("m24-m-sanity: CO atoms SN 2", (atom_info("[C-]#[O+]", 0)[:2], atom_info("[C-]#[O+]", 1)[:2]), ((2, 2), (2, 2)))

# m24-p8: allene's two CH2 planes are perpendicular (MMFF geometry); ethylene's are coplanar (contrast)
from rdkit.Chem import AllChem  # noqa: E402


def ch2_plane_angle(smi, c1, c2):
    m3 = Chem.AddHs(Chem.MolFromSmiles(smi))
    AllChem.EmbedMolecule(m3, randomSeed=7)
    AllChem.MMFFOptimizeMolecule(m3)
    pos = m3.GetConformer().GetPositions()

    def normal(c):
        hs = [n.GetIdx() for n in m3.GetAtomWithIdx(c).GetNeighbors() if n.GetSymbol() == "H"]
        v = np.cross(pos[hs[0]] - pos[c], pos[hs[1]] - pos[c])
        return v / np.linalg.norm(v)
    return float(np.degrees(np.arccos(min(1.0, abs(np.dot(normal(c1), normal(c2)))))))


check("allene CH2 planes ~90 deg", abs(ch2_plane_angle("C=C=C", 0, 2) - 90) < 2, True)
check("ethylene CH2 planes ~0 deg", ch2_plane_angle("C=C", 0, 1) < 2, True)
check("m24-p8 key", "perpendicular planes" in correct_html(BY_ID["m24-p8"]["answer"]), True)


# m24-p9: atoms spanned by the pi system = the largest set joined by RDKit-conjugated bonds (2 for an isolated double bond)
def pi_system_size(smi):
    m2 = Chem.MolFromSmiles(smi)
    best = 0
    for b in m2.GetBonds():
        if b.GetBondTypeAsDouble() > 1:
            if not b.GetIsConjugated():
                best = max(best, 2)
                continue
            seen, stack = set(), [b.GetBeginAtomIdx()]
            while stack:
                a = stack.pop()
                if a in seen:
                    continue
                seen.add(a)
                for bb in m2.GetAtomWithIdx(a).GetBonds():
                    if bb.GetIsConjugated():
                        stack.append(bb.GetOtherAtomIdx(a))
            best = max(best, len(seen))
    return best


num_part("m24-p9", 0, pi_system_size("C=CC=CC"))
num_part("m24-p9", 1, pi_system_size("C=CCC=C"))
# methyl isocyanate: N=C=O is linear in the MMFF geometry
m_mic = Chem.AddHs(Chem.MolFromSmiles("CN=C=O"))
AllChem.EmbedMolecule(m_mic, randomSeed=7)
AllChem.MMFFOptimizeMolecule(m_mic)
_pos = m_mic.GetConformer().GetPositions()
check("methyl isocyanate N=C=O ~180 deg", abs(angle(_pos[1] - _pos[2], _pos[3] - _pos[2]) - 180) < 3, True)

# the bank's own lewis.py bookkeeping agrees with RDKit for every structure it uses
for sid, smi in (("CH4", "C"), ("NH3", "N"), ("H2O", "O"), ("C2H4", "C=C"), ("C2H2", "C#C"), ("HCN", "C#N"), ("CO2", "O=C=O"),
                 ("N2", "N#N"), ("acrolein", "C=CC=O"), ("C6H6-1", "c1ccccc1"), ("C6H6-2", "c1ccccc1"), ("CH3CN", "CC#N"),
                 ("HCOOH", "OC=O"), ("allene", "C=C=C"), ("CH3NCO", "CN=C=O"), ("N2H2", "N=N"), ("CH2O", "C=O"), ("CO", "[C-]#[O+]"),
                 ("N2O-A", "N#[N+][O-]"), ("N2H4", "NN"), ("CH2NH", "C=N"), ("H3O+", "[OH3+]"), ("NF3", "FN(F)F")):
    check(f"lewis.py {sid} sigma/pi", J.sigma_pi(sid), counts(smi))

print(f"check_problem_bank_j: {n_checks} checks, {len(fails)} mismatches")
for f in fails:
    print("  -", f)
sys.exit(1 if fails else 0)

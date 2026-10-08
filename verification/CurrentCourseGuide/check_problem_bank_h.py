"""Independent re-derivation of the keys in problem_bank_h.py (Day 9 items for t4-2, t4-5...t4-8).

    py -3.11 verification/CurrentCourseGuide/check_problem_bank_h.py

Works from the slides' numbers typed in afresh (the Day 9 p.17 electronegativity table, Day 9 p.14 Table 4.6) and from
RDKit molecules built from SMILES, not from guide_common, lewis.py, or the bank's own helpers; then compares with the
keys the bank stores. Exit status 1 on any mismatch."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.stdout.reconfigure(encoding="utf-8")
from rdkit import Chem  # noqa: E402

# Day 9 p.17 (read off the slide; the noble gases have no values)
CHI = {"H": 2.1, "Be": 1.5, "B": 2.0, "C": 2.5, "N": 3.0, "O": 3.5, "F": 4.0, "Al": 1.5, "S": 2.5, "Cl": 3.0, "Ca": 1.0, "Br": 2.8}
# Day 9 p.14, the four red-boxed groups: bond -> (pm, kJ/mol)
T46 = {"C–C": (154, 348), "C=C": (134, 614), "C≡C": (120, 839), "C–O": (143, 358), "C=O": (123, 743), "C≡O": (113, 1072),
       "O–O": (148, 146), "O=O": (121, 498), "F–F": (143, 155), "Cl–Cl": (200, 243), "Br–Br": (228, 193), "I–I": (266, 151)}
VAL = {"H": 1, "Be": 2, "C": 4, "N": 5, "O": 6, "F": 7, "Al": 3, "P": 5, "S": 6, "Cl": 7, "Br": 7}
errors = []


def check(name, got, want):
    if got != want:
        errors.append(f"{name}: bank {got!r} vs independent {want!r}")


def cls(d):          # Day 9 p.18: <= 0.4 nonpolar covalent; 0.4 < d < 2.0 polar covalent; >= 2.0 ionic
    d = round(d, 2)
    return "np" if d <= 0.4 else ("pc" if d < 2.0 else "io")


def fcs(smiles):
    m = Chem.MolFromSmiles(smiles)
    return [a.GetFormalCharge() for a in m.GetAtoms()], [a.GetNumRadicalElectrons() for a in m.GetAtoms()]


import problem_bank_h  # noqa: E402,F401
from problem_bank_a import PROBLEMS  # noqa: E402
B = {p["id"]: p for p in PROBLEMS}


def correct(spec):
    return next(o["html"] for o in spec["options"] if o["correct"])


# ---- t4-2
d = abs(CHI["Br"] - CHI["H"])
check("battery: H–Br polar, Br δ−", (cls(d), CHI["Br"] > CHI["H"]), ("pc", True))
check("battery key names Br as δ−", correct(B["t4-2-lec-battery"]["answer"]).startswith("Br is the δ− end"), True)
rows = B["t4-2-lec-cutoffs"]["answer"]["rows"]
check("cutoffs rows", [r["answer"] for r in rows], [cls(abs(CHI[a] - CHI[b])) for a, b in (("C", "H"), ("S", "Cl"), ("Ca", "Cl"), ("N", "Cl"))])
check("cutoffs boundary cases", [cls(0.4), cls(2.0)], ["np", "io"])
parts = B["t4-2-lec-beal"]["answer"]["parts"]
check("beal Δχ(Al–Cl)", parts[0]["value"], round(abs(CHI["Al"] - CHI["Cl"]), 2))
check("beal class", correct(parts[1]), {"np": "nonpolar covalent", "pc": "polar covalent", "io": "ionic"}[cls(abs(CHI["Al"] - CHI["Cl"]))])
check("beal Be–Cl same Δχ", round(abs(CHI["Be"] - CHI["Cl"]), 2), round(abs(CHI["Al"] - CHI["Cl"]), 2))

# ---- t4-5: NO2 hybrid dots (each O has 4 lone-pair electrons in one structure and 6 in the other; N keeps one electron)
f1, r1 = fcs("O=[N+][O-]")                                 # O=N(+)–O(−): RDKit puts the odd electron on N
check("NO2 radical on N", r1, [0, 1, 0])
parts = B["t4-5-lec-no2hybrid"]["answer"]["parts"]
check("NO2 hybrid dots on O", parts[0]["value"], (4 + 6) / 2)
check("NO2 hybrid dots on N", parts[1]["value"], 1)
check("ozone vs NO2 electron totals", (3 * VAL["O"], VAL["N"] + 2 * VAL["O"]), (18, 17))
# HCN and HNC are different molecules (the H moved), so they can't be resonance structures of each other
check("HCN and HNC differ in connectivity", Chem.MolToSmiles(Chem.MolFromSmiles("C#N")) != Chem.MolToSmiles(Chem.MolFromSmiles("[C-]#[NH+]")), True)
check("notres key is the HCN pair", "H–C≡N" in B["t4-5-lec-notres"]["solution"], True)

# ---- t4-6: the red boxes
for grp in (["C–C", "C=C", "C≡C"], ["C–O", "C=O", "C≡O"], ["O–O", "O=O"]):
    check(f"box {grp[0]} shorter and stronger", all(T46[a][0] > T46[b][0] and T46[a][1] < T46[b][1] for a, b in zip(grp, grp[1:])), True)
hal = ["F–F", "Cl–Cl", "Br–Br", "I–I"]
parts = B["t4-6-lec-halogens"]["answer"]["parts"]
check("halogen longest", correct(parts[0]), max(hal, key=lambda b: T46[b][0]))
check("halogen strongest", correct(parts[1]), max(hal, key=lambda b: T46[b][1]))
check("shortest is strongest?", correct(parts[2]), "yes" if min(hal, key=lambda b: T46[b][0]) == max(hal, key=lambda b: T46[b][1]) else "no")
check("O–O energy order", B["t4-6-lec-oo-energy"]["answer"]["answerOrder"], ["o2", "o3", "h2o2"])
check("not additive", (T46["C=C"][1] < 2 * T46["C–C"][1], T46["C≡C"][1] < 3 * T46["C–C"][1]), (True, True))

# ---- t4-7: N2O (A N≡N–O, B N=N=O, C N–N≡O), H3PO4, sulfate O, NO2's N
want = {"A": fcs("N#[N+][O-]")[0], "B": fcs("[N-]=[N+]=O")[0], "C": fcs("[N-2][N+]#[O+]")[0]}
check("N2O formal charges", want, {"A": [0, 1, -1], "B": [-1, 1, 0], "C": [-2, 1, 1]})
parts = B["t4-7-lec-n2o"]["answer"]["parts"]
check("N2O (a) end N in C", parts[0]["value"], want["C"][0])
check("N2O (b) O in C", parts[1]["value"], want["C"][2])
score = {k: (sum(abs(x) for x in v), -sum(1 for x in v if x == 0), -sum(CHI[e] * -x for e, x in zip("NNO", v) if x < 0)) for k, v in want.items()}
check("N2O worst", correct(parts[2]), max(score, key=score.get))
check("N2O best", correct(parts[3]), min(score, key=score.get))
total = 3 * VAL["H"] + VAL["P"] + 4 * VAL["O"]
drawn4 = 2 * 7 + 2 * (3 + 2 + 3 + 2)          # option 4: 7 bonds; lone pairs 3, 2, 3, 2
drawn5 = 2 * 8 + 2 * (2 + 2 + 3 + 2)          # option 5: 8 bonding pairs (P=O counts 2); lone pairs 2, 2, 3, 2
check("H3PO4 electrons, options 4 and 5", (total, drawn4, drawn5), (32, 34, 34))
f3, _ = fcs("O=P(O)(O)O")
f2, _ = fcs("[O-][P+](O)(O)O")
check("H3PO4 option 3 all zero; option 2 P +1", (set(f3), max(f2)), ({0}, 1))
tophat = B["t4-7-tophat"]["answer"]["options"]
check("Top Hat key is option 3", [i for i, o in enumerate(tophat) if o["correct"]], [2])
f, _ = fcs("[O-]S(=O)(=O)[O-]")
f_oct, _ = fcs("[O-][S+2]([O-])([O-])[O-]")
check("sulfate: octet S +2, O −1; expanded S 0, sum −2", (f_oct[1], f_oct[0], f[1], sum(f), sum(f_oct)), (2, -1, 0, -2, -2))
check("single-bonded O assigned 7", VAL["O"] - (6 + 1), -1)
f, r = fcs("O=[N+][O-]")
check("NO2 N formal charge", B["t4-7-lec-no2"]["answer"]["value"], f[1])

# ---- t4-8
EXC = {"BeF2": VAL["Be"] + 2 * VAL["F"], "AlBr3": VAL["Al"] + 3 * VAL["Br"], "NO": VAL["N"] + VAL["O"], "OH": VAL["O"] + VAL["H"],
       "SF4": VAL["S"] + 4 * VAL["F"], "PCl5": VAL["P"] + 5 * VAL["Cl"]}
check("classify parity", {k: v % 2 for k, v in EXC.items()}, {"BeF2": 0, "AlBr3": 0, "NO": 1, "OH": 1, "SF4": 0, "PCl5": 0})
check("SF4 electrons on S", (EXC["SF4"] - 4 * 8) + 4 * 2, 10)       # 4 bonds + the leftover 2 as a lone pair
check("classify keys", [r["answer"] for r in B["t4-8-lec-classify"]["answer"]["rows"]], ["def", "def", "rad", "rad", "exp", "exp"])
f, r = fcs("[CH3]")
parts = B["t4-8-lec-ch3"]["answer"]["parts"]
check("CH3 valence electrons", parts[0]["value"], VAL["C"] + 3 * VAL["H"])
check("CH3 electrons on C (3 bonds + 1)", parts[1]["value"], 3 * 2 + r[0])

print("\n".join(errors) if errors else f"all keys agree ({len(B)} problems loaded)")
sys.exit(1 if errors else 0)

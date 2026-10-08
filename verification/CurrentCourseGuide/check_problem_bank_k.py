"""Independent checks for problem_bank_k (t5-6 chirality, t5-7 molecular orbital theory).

    py -3.11 verification/CurrentCourseGuide/check_problem_bank_k.py

1. MO theory. Fills the textbook's valence MO orders (Figs. 5.45-5.52) electron by electron, one orbital at a time
   (at most two per orbital; through a degenerate set singly before pairing), with its own orbital lists, and compares
   bond orders and unpaired-electron counts with
     a. the values the textbook prints (Fig. 5.50; Sample Ex. 5.7, 5.8, 5.9; NO's 2.5; B2 and O2 paramagnetic),
     b. problem_bank_k's own filling (SP), and every MO key in the t5-7 problems,
     c. the N2/O2 ladder table in src/t5-7.html (arrows per MO).
2. Chirality. Counts stereocenters two ways for every molecule the bank uses: RDKit's stereo perception, and the
   textbook's test done on the graph (an sp3 carbon whose four neighbours fall in four different symmetry classes,
   from canonical ranks without tie-breaking). Then checks every stereocenter key in the t5-6 problems.
3. Overlap. The species and molecules the practice, attempt, and transfer items ask about must not be the textbook's
   own (worked examples, Sample and Practice Exercises, Concept Tests, Visual Problems, end-of-chapter problems in
   Ch. 5, PDF p.255-285) or the mixed review's (x58-x60); the attempt and transfer species must not be explorer presets
   (explorers_ch5.js, ch5_data.py). The lecture examples O2 (Day 11 p.27) and carvone (Day 10 p.6) are exempt.
Exit status 1 on any mismatch.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.stdout.reconfigure(encoding="utf-8")

from rdkit import Chem                      # noqa: E402

import problem_bank_k as K                  # noqa: E402
from problem_bank_a import PROBLEMS         # noqa: E402
import lewis as LW                          # noqa: E402

errs = []


def check(cond, msg):
    if not cond:
        errs.append(msg)


# ---------------------------------------------------------------- 1. MO filling, written independently of the bank
VAL = {"H": 1, "He": 2, "Li": 1, "Be": 2, "B": 3, "C": 4, "N": 5, "O": 6, "F": 7, "Ne": 8}
# (orbital, +1 bonding / -1 antibonding, energy level); orbitals sharing a level are degenerate
ONE_S = [("s1s", 1, 0), ("s1s*", -1, 1)]
LIGHT = [("s2s", 1, 0), ("s2s*", -1, 1), ("p2px", 1, 2), ("p2py", 1, 2), ("s2p", 1, 3), ("p2px*", -1, 4), ("p2py*", -1, 4), ("s2p*", -1, 5)]
HEAVY = [("s2s", 1, 0), ("s2s*", -1, 1), ("s2p", 1, 2), ("p2px", 1, 3), ("p2py", 1, 3), ("p2px*", -1, 4), ("p2py*", -1, 4), ("s2p*", -1, 5)]


def fill(orbitals, n):
    occ = {name: 0 for name, _, _ in orbitals}
    for _ in range(n):
        for level in sorted({lv for _, _, lv in orbitals}):
            group = [name for name, _, lv in orbitals if lv == level]
            empty = [g for g in group if occ[g] == 0]
            half = [g for g in group if occ[g] == 1]
            if empty:
                occ[empty[0]] += 1
                break
            if half:
                occ[half[0]] += 1
                break
        else:
            raise ValueError("more electrons than orbitals")
    sign = {name: s for name, s, _ in orbitals}
    bonding = sum(e for o, e in occ.items() if sign[o] > 0)
    anti = sum(e for o, e in occ.items() if sign[o] < 0)
    return {"bo": (bonding - anti) / 2, "unpaired": sum(1 for e in occ.values() if e == 1), "occ": occ, "n": n}


def diatomic(a, b, q=0, orbitals=None):
    if orbitals is None:
        if a in ("H", "He") and b in ("H", "He"):
            orbitals = ONE_S
        elif a == b and a in ("Li", "Be", "B", "C", "N"):
            orbitals = LIGHT
        else:
            orbitals = HEAVY
    return fill(orbitals, VAL[a] + VAL[b] - q)


# a. the textbook's printed values: species -> (bond order, unpaired electrons or None)
PRINTED = {
    "H2": (1, 0), "He2": (0, 0), "H2-": (0.5, None), "H2+": (0.5, None),                    # PDF p.262-263 (SE 5.7 and its practice)
    "Li2": (1, 0), "Be2": (0, 0), "B2": (1, 2), "C2": (2, 0), "N2": (3, 0), "O2": (2, 2),   # Fig. 5.50, PDF p.266
    "F2": (1, 0), "Ne2": (0, 0),
    "Li2+": (0.5, None), "Be2+": (0.5, None), "B2+": (0.5, None), "C2+": (1.5, None),       # SE 5.8 table, PDF p.267
    "N2+": (2.5, None), "O2+": (2.5, None), "F2+": (1.5, None), "Ne2+": (0.5, None),
    "NO": (2.5, 1), "NO+": (3, None), "NO-": (2, None),                                     # PDF p.268-269
}


def parse(sp):
    m = re.fullmatch(r"([A-Z][a-z]?)(2)?([A-Z][a-z]?)?(\+2|\+|-2|-)?", sp)
    a = m.group(1)
    b = a if m.group(2) else m.group(3)
    q = {None: 0, "+": 1, "-": -1, "+2": 2, "-2": -2}[m.group(4)]
    return a, b, q


for sp, (bo, unp) in PRINTED.items():
    r = diatomic(*parse(sp))
    check(abs(r["bo"] - bo) < 1e-9, f"MO: {sp} bond order {r['bo']} vs. textbook {bo}")
    if unp is not None:
        check(r["unpaired"] == unp, f"MO: {sp} unpaired {r['unpaired']} vs. textbook {unp}")
# SE 5.8: only Be2+, O2+, F2+, Ne2+ gain bond order; its practice: the 1- anions that gain are Be2-, B2-, C2-
up_cat = [x for x in ("Li", "Be", "B", "C", "N", "O", "F", "Ne") if diatomic(x, x, 1)["bo"] > diatomic(x, x)["bo"]]
check(up_cat == ["Be", "O", "F", "Ne"], f"MO: cations that gain bond order {up_cat}")
up_an = [x for x in ("Li", "Be", "B", "C", "N", "O", "F") if diatomic(x, x, -1)["bo"] > diatomic(x, x)["bo"]]   # Ne2- has no valence MO left
check(up_an == ["Be", "B", "C"], f"MO: anions that gain bond order {up_an}")
# the Concept Test (PDF p.267): which don't exist, which is paramagnetic besides O2
check([x for x in ("Li", "Be", "B", "C", "N", "O", "F", "Ne") if diatomic(x, x)["bo"] == 0] == ["Be", "Ne"], "MO: bond-order-0 molecules")
check([x for x in ("Li", "Be", "B", "C", "N", "O", "F", "Ne") if diatomic(x, x)["unpaired"]] == ["B", "O"], "MO: paramagnetic molecules")
# CO and CN- (10 electrons): both energy orders give bond order 3 and no unpaired electrons
for a, b, q in (("C", "O", 0), ("C", "N", -1)):
    for orbs in (LIGHT, HEAVY):
        r = diatomic(a, b, q, orbs)
        check((r["bo"], r["unpaired"]) == (3, 0), f"MO: {a}{b}{q} with either order")

# b. the bank's own filling and its keys
for sp, (a, b, q) in K.SPECIES.items():
    mine = diatomic(a, b, q)
    theirs = K.SP[sp]
    check(abs(mine["bo"] - theirs["bo"]) < 1e-9 and mine["unpaired"] == theirs["unpaired"] and mine["n"] == theirs["n"],
          f"bank SP[{sp}] = {theirs['bo']}/{theirs['unpaired']} vs. independent {mine['bo']}/{mine['unpaired']}")
    # the configuration string must list the same occupancies, in the textbook's order
    occ = mine["occ"]
    total = {"s1s": "σ<sub>1s</sub>", "s1s*": "σ*<sub>1s</sub>", "s2s": "σ<sub>2s</sub>", "s2s*": "σ*<sub>2s</sub>", "s2p": "σ<sub>2p</sub>", "s2p*": "σ*<sub>2p</sub>"}
    parts = []
    orbs = ONE_S if a in ("H", "He") and b in ("H", "He") else (LIGHT if a == b and a in ("Li", "Be", "B", "C", "N") else HEAVY)
    seen = set()
    for name, _, lv in orbs:
        if lv in seen:
            continue
        seen.add(lv)
        group = [o for o, _, l2 in orbs if l2 == lv]
        e = sum(occ[o] for o in group)
        if not e:
            continue
        lab = total.get(name) or ("π*<sub>2p</sub>" if name.endswith("*") else "π<sub>2p</sub>")
        parts.append(f"({lab})<sup>{e}</sup>")
    check("".join(parts) == theirs["config"], f"bank config for {sp}: {theirs['config']} vs. {''.join(parts)}")

P = {p["id"]: p for p in PROBLEMS[K.K_START:]}


def part(pid, i):
    return P[pid]["answer"]["parts"][i]


def right(spec):
    return next(o["html"] for o in spec["options"] if o["correct"])


NF = diatomic("N", "F")
check(part("t5-7-attempt", 0)["value"] == NF["bo"] == 2 and part("t5-7-attempt", 1)["value"] == NF["unpaired"] == 2, "t5-7-attempt keys (NF)")
check(right(part("t5-7-attempt", 2)) == ("paramagnetic" if NF["unpaired"] else "diamagnetic"), "t5-7-attempt (c)")
check(all((diatomic("N", "F", 0, o)["bo"], diatomic("N", "F", 0, o)["unpaired"]) == (2, 2) for o in (LIGHT, HEAVY)), "NF: same result in either order")
excited = {"s1s": 1, "s1s*": 1}                                       # H2 after one electron is promoted to σ*1s
check([part("t5-7-p2", i)["value"] for i in range(3)] == [diatomic("He", "H", 1)["bo"], diatomic("H", "H", -2)["bo"], (excited["s1s"] - excited["s1s*"]) / 2]
      == [1, 0, 0], "t5-7-p2 keys")
o2 = LW.STRUCTS["O2"]
check(P["t5-7-p3"]["answer"]["value"] == sum(o2.rad.values()) == 0 and o2.drawn_electrons() == 12, "t5-7-p3 key")
for row, sp in zip(P["t5-7-p4"]["answer"]["rows"], K.BO_ROWS):
    a, b, q = parse(sp)
    want = diatomic(a, b, q)["bo"]
    check(row["answer"] == "bo" + LW.bo_text(want), f"t5-7-p4 row {sp}: {row['answer']} vs. {want}")
    check(diatomic(a, b, q, LIGHT)["bo"] == diatomic(a, b, q, HEAVY)["bo"], f"t5-7-p4 {sp}: bond order depends on the energy order")
for row, sp in zip(P["t5-7-p5"]["answer"]["rows"], K.MAG_ROWS):
    a, b, q = parse(sp)
    check(row["answer"] == ("para" if diatomic(a, b, q)["unpaired"] else "dia"), f"t5-7-p5 row {sp}")
    if "He" not in (a, b):
        check(diatomic(a, b, q, LIGHT)["unpaired"] == diatomic(a, b, q, HEAVY)["unpaired"], f"t5-7-p5 {sp}: magnetism depends on the energy order")
pairs = [("NF", "NF+"), ("BF", "BF-"), ("Ne2+2", "Ne2"), ("Be2+2", "Be2")]
gain = [x for x, y in pairs if diatomic(*parse(y))["bo"] > diatomic(*parse(x))["bo"]]
check(gain == ["NF"] and right(P["t5-7-p6"]["answer"]).startswith("NF →"), "t5-7-p6 key")
CF, CFp = diatomic("C", "F"), diatomic("C", "F", 1)
check((part("t5-7-p7", 0)["value"], part("t5-7-p7", 1)["value"]) == (CF["bo"], CFp["bo"]) == (2.5, 3)
      and right(part("t5-7-p7", 2)) == ("paramagnetic" if CF["unpaired"] else "diamagnetic"), "t5-7-p7 keys (CF)")
keyed = {"ofp": "OF+", "of": "OF", "ofm": "OF-"}
want = sorted(keyed, key=lambda k: diatomic(*parse(keyed[k]))["bo"])          # lowest bond order = longest bond first
check(P["t5-7-p8"]["answer"]["answerOrder"] == want, f"t5-7-p8 order {P['t5-7-p8']['answer']['answerOrder']} vs. {want}")
flip = [x for x in ("Be2-2", "CO-", "Ne2+2") if diatomic(*parse(x), LIGHT)["unpaired"] != diatomic(*parse(x), HEAVY)["unpaired"]]
check(flip == ["Be2-2"] and right(P["t5-7-p9"]["answer"]) == "Be<sub>2</sub><sup>2−</sup>", f"t5-7-p9 key ({flip})")
check(diatomic("Be", "Be", -2, LIGHT)["bo"] == diatomic("Be", "Be", -2, HEAVY)["bo"] == 1, "t5-7-p9: same bond order in either order")
# the 3-center π system of nitrite (as for ozone, Figs. 5.54-5.55): three p orbitals -> π (bonding), n (nonbonding), π* (antibonding)
pi3 = {"pi": 0, "n": 0, "pi*": 0}
left = LW.STRUCTS["NO2-1"].total_valence() - (2 * 2 + 5 * 2)
for orb in ("pi", "n", "pi*"):
    pi3[orb] = min(2, left)
    left -= pi3[orb]
pi_bonds = (pi3["pi"] - pi3["pi*"]) / 2
check(part("t5-7-p10", 0)["value"] == (2 + pi_bonds) / 2 == 1.5, "t5-7-p10 (a)")
check(part("t5-7-p10", 1)["value"] == 2 + (pi3["n"] / 2) / 2 == 2.5, "t5-7-p10 (b)")
cn = diatomic("C", "N", -1)
check((part("t5-7-transfer", 0)["value"], part("t5-7-transfer", 1)["value"]) == (cn["n"], cn["bo"]), "t5-7-transfer (a), (b)")
check(right(part("t5-7-transfer", 2)) == ("paramagnetic" if cn["unpaired"] else "diamagnetic"), "t5-7-transfer (c)")
same = [x for x in ("N2", "O2", "NO", "C2") if (diatomic(*parse(x))["n"], diatomic(*parse(x))["bo"]) == (cn["n"], cn["bo"])]
check(same == ["N2"] and right(part("t5-7-transfer", 3)) == "N<sub>2</sub>", "t5-7-transfer (d)")
check(diatomic("B", "F", -1)["bo"] == 2.5, "t5-7-m-sanity BF- remark")

# c. the ladder table in src/t5-7.html: rows top to bottom, N2 then O2 columns
frag = open(os.path.join(HERE, "src", "t5-7.html"), encoding="utf-8").read()
table = re.search(r'<table class="data" data-check="mo-ladder">(.*?)</table>', frag, re.S).group(1)
rows = re.findall(r"<tr><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td></tr>", table)
check(len(rows) == 6, f"ladder table has {len(rows)} rows")


def label_key(html):
    html = re.sub(r"\s*\(two MOs\)", "", html)
    return {"σ<sub>2s</sub>": "s2s", "σ*<sub>2s</sub>": "s2s*", "σ<sub>2p</sub>": "s2p", "σ*<sub>2p</sub>": "s2p*",
            "π<sub>2p</sub>": "p2p", "π*<sub>2p</sub>": "p2p*"}[html]


for col, (orbs, mol) in enumerate(((LIGHT, diatomic("N", "N")), (HEAVY, diatomic("O", "O")))):
    levels = []
    for name, _, lv in orbs:
        key = "p2p*" if name.startswith("p") and name.endswith("*") else ("p2p" if name.startswith("p") else name)
        if not levels or levels[-1][0] != lv:
            levels.append((lv, key, [name]))
        else:
            levels[-1][2].append(name)
    top_down = list(reversed(levels))
    for (lv, key, names), row in zip(top_down, rows):
        lab, arrows = row[2 * col], row[2 * col + 1]
        check(label_key(lab) == key, f"ladder column {col}: {lab} where {key} belongs")
        want_txt = " ".join("↑↓" if mol["occ"][n] == 2 else "↑" if mol["occ"][n] == 1 else "" for n in names).strip() or "empty"
        if want_txt != "empty" and "" in [("↑↓" if mol["occ"][n] == 2 else "↑" if mol["occ"][n] == 1 else "") for n in names]:
            want_txt = " ".join(("↑↓" if mol["occ"][n] == 2 else "↑" if mol["occ"][n] == 1 else "_") for n in names)
        check(arrows == want_txt, f"ladder column {col} {key}: '{arrows}' vs. '{want_txt}'")

# ---------------------------------------------------------------- 2. stereocenters, two ways
def by_symmetry_classes(smiles):
    m = Chem.AddHs(Chem.MolFromSmiles(smiles))
    ranks = list(Chem.CanonicalRankAtoms(m, breakTies=False))
    n = 0
    for at in m.GetAtoms():
        if at.GetSymbol() == "C" and at.GetHybridization() == Chem.HybridizationType.SP3 and at.GetDegree() == 4:
            if len({ranks[nb.GetIdx()] for nb in at.GetNeighbors()}) == 4:
                n += 1
    return n


for name, smi in K.SMI.items():
    rd = len(Chem.FindMolChiralCenters(Chem.MolFromSmiles(smi), includeUnassigned=True, useLegacyImplementation=False))
    gr = by_symmetry_classes(smi)
    check(rd == gr == K.NSC[name], f"stereocenters in {name}: RDKit {rd}, symmetry classes {gr}, bank {K.NSC[name]}")
# carvone: the stereocenter's two ring CH2 neighbours are in different classes (C=C side vs. C=O side, PDF p.258)
mc = Chem.AddHs(Chem.MolFromSmiles(K.SMI["carvone"]))
rk = list(Chem.CanonicalRankAtoms(mc, breakTies=False))
center = [a for a in mc.GetAtoms() if a.GetSymbol() == "C" and a.GetDegree() == 4 and len({rk[n.GetIdx()] for n in a.GetNeighbors()}) == 4]
check(len(center) == 1, "carvone: one stereocenter")
ring_ch2 = [n for n in center[0].GetNeighbors() if n.IsInRing() and n.GetTotalNumHs(includeNeighbors=True) == 2]
check(len(ring_ch2) == 2 and rk[ring_ch2[0].GetIdx()] != rk[ring_ch2[1].GetIdx()], "carvone: the two ring CH2 groups differ")

check(part("t5-6-attempt", 0)["value"] == by_symmetry_classes("CCC(C)O") == 1 and right(part("t5-6-attempt", 1)) == "yes", "t5-6-attempt keys")
P3 = {"CHFClI": "FC(Cl)I", "CHCl<sub>2</sub>I": "ClC(Cl)I", "CH<sub>2</sub>FI": "FCI", "CF<sub>2</sub>ClBr": "FC(F)(Cl)Br"}
for o in P["t5-6-p3"]["answer"]["options"]:
    check(o["correct"] == (by_symmetry_classes(P3[o["html"]]) > 0), f"t5-6-p3 option {o['html']}")
P5 = {"glyceraldehyde": "OCC(O)C=O", "glycerol": "OCC(O)CO", "1-phenylethanol": "CC(O)c1ccccc1", "2-propanol": "CC(C)O", "bromochloromethane": "BrCCl"}
for row in P["t5-6-p5"]["answer"]["rows"]:
    nm = row["html"].split(",")[0]
    check(row["answer"] == ("chiral" if by_symmetry_classes(P5[nm]) else "achiral"), f"t5-6-p5 row {nm}")
check(P["t5-6-p8"]["answer"]["value"] == by_symmetry_classes("CNC(C)C(O)c1ccccc1") == 2, "t5-6-p8 key (pseudoephedrine)")
# limonene: like carvone, the stereocenter's two ring CH2 neighbours differ (one is bonded to a C=C carbon, one to another CH2)
ml = Chem.AddHs(Chem.MolFromSmiles(K.SMI["limonene"]))
rl = list(Chem.CanonicalRankAtoms(ml, breakTies=False))
cl = [a for a in ml.GetAtoms() if a.GetSymbol() == "C" and a.GetDegree() == 4 and len({rl[n.GetIdx()] for n in a.GetNeighbors()}) == 4]
ring2 = [n for n in cl[0].GetNeighbors() if n.IsInRing() and n.GetTotalNumHs(includeNeighbors=True) == 2] if len(cl) == 1 else []
check(len(cl) == 1 and len(ring2) == 2 and rl[ring2[0].GetIdx()] != rl[ring2[1].GetIdx()], "limonene: one stereocenter with two different ring CH2 branches")
check(right(part("t5-6-transfer", 0)).startswith("Yes: around the ring") and right(part("t5-6-transfer", 1)).startswith("Nothing"), "t5-6-transfer keys (limonene)")
check(by_symmetry_classes("ClC(Br)I") == 1 and by_symmetry_classes("BrC(I)I") == 0, "t5-6-m-explain species")
check(by_symmetry_classes("C=Cc1ccccc1") == 0 and right(P["t5-6-m-sanity"]["answer"]).startswith("A planar molecule"), "t5-6-m-sanity: styrene has no stereocenter")
# every 2-butanol drawing's highlighted atom is its stereocenter (atom 1 of the lewis.py structure)
bt = LW.STRUCTS["2-butanol"]
nbrs = sorted(bt.atoms[j][0] if i == 1 else bt.atoms[i][0] for i, j, _ in bt.bonds if 1 in (i, j))
check(nbrs == ["C", "C", "H", "O"], f"2-butanol atom 1 neighbours {nbrs}")

# ---------------------------------------------------------------- 3. textbook and mixed-review overlap; explorer presets
canon = Chem.CanonSmiles
TEXTBOOK_CHIRAL = [
    "FC(Cl)Br", "ClC(Br)Br",                                                                       # Fig. 5.40 (PDF p.257)
    "CC(C)C(C)CC", "CC1CCCC=C1", "CCC(N)C(=O)O", "OC(=O)C=Cc1ccccc1", "CCC(C)CC1CC(=O)CCC1C",     # Sample Ex. 5.6 (PDF p.258-259)
    "C1CCC2CCCCC2C1", "CC(C)C(C)C(C)C", "CCCC(=O)OC(C)CC", "NC(C(=O)O)c1ccc(O)cc1",               # its Practice Exercise
    "CC(N)C(=O)O", "CC(C)(C)NCC(O)c1ccc(O)c(CO)c1", "CC1OC(C[N+](C)(C)C)CC1O",                   # alanine, albuterol, muscarine (PDF p.260-261)
    "CC1=CCC(O)(CC1)C(C)C", "CC(C)C1CCC(C)CC1O",                                                 # Visual Problems 5.7, 5.8 (PDF p.277)
    "CC(C)Cc1ccc(cc1)C(C)C(=O)O", "NCC(=O)O", "CC(=O)Oc1ccccc1C(=O)O", "OC(=O)C(=O)O", "C=C",   # Visual Problem 5.10 (PDF p.278)
    "CC(Cl)Br", "CC(=O)O", "CCCl", "CCC(C)(O)C(C)=O", "NC1CCCCC1", "CC(O)C(=O)O", "CCC(=O)O", "OCCC(=O)O",
    "CC(C)C(N)C(=O)O", "CC(N)C(N)C(=O)O", "CC(=O)CCc1ccc(O)cc1", "CC(NC(C)(C)C)C(=O)c1cccc(Cl)c1",   # Problems 5.85-5.92 (PDF p.282-283)
]
MIXED_CHIRAL = ["CCCC(C)CC", "CCC(C)CC", "CCC(C)C", "CC(Cl)Cl", "CCC(C)Cl"]                   # x58; the 2-chlorobutane type
avoid = {canon(x) for x in TEXTBOOK_CHIRAL + MIXED_CHIRAL}
ASKED_CHIRAL = {"t5-6-attempt": ["CCC(C)O"], "t5-6-p3": list(P3.values()), "t5-6-p5": list(P5.values()),
                "t5-6-p8": ["CNC(C)C(O)c1ccccc1"], "t5-6-transfer": [K.SMI["limonene"]], "t5-6-m-explain": ["ClC(Br)I", "BrC(I)I"],
                "t5-6-m-sanity": ["C=Cc1ccccc1"]}
for pid, smis in ASKED_CHIRAL.items():
    for x in smis:
        check(canon(x) not in avoid, f"{pid}: {x} is a textbook or mixed-review molecule")
TEXTBOOK_MO = ({"H2", "He2", "H2-", "H2+", "NO", "NO+", "NO-", "CO"}
               | {e + "2" + q for e in ("Li", "Be", "B", "C", "N", "O", "F", "Ne") for q in ("", "+", "-")}   # Fig. 5.50; Sample Ex. 5.8 and its practice
               | {"He2+", "Ne2+", "C2+2", "O2-2", "N2-2", "C2-2", "B2-2", "B2+2", "N2+2", "O2+2", "F2+"})       # Problems 5.99-5.108, 5.135-5.136; Visual 5.5
MIXED_MO = {"B2-2", "F2-2", "C2"}
ASKED_MO = {"t5-7-attempt": ["NF"], "t5-7-p2": ["HeH+", "H2-2"], "t5-7-p4": K.BO_ROWS, "t5-7-p5": K.MAG_ROWS,
            "t5-7-p6": ["NF+", "BF-", "Ne2+2", "Be2+2"], "t5-7-p7": ["CF", "CF+"], "t5-7-p8": ["OF+", "OF", "OF-"],
            "t5-7-p9": ["Be2-2", "CO-", "Ne2+2", "He2+2"], "t5-7-transfer": ["CN-"]}
for pid, sps in ASKED_MO.items():
    for x in sps:
        check(x not in TEXTBOOK_MO | MIXED_MO, f"{pid}: {x} is a textbook or mixed-review species")
js = open(os.path.join(HERE, "..", "..", "study-guides", "CurrentCourseGuide", "assets", "explorers_ch5.js"), encoding="utf-8").read()
block = re.search(r'presetButtons\(ui, "mo", \[(.*?)\], function', js, re.S).group(1)
MO_PRESETS = {sp + ("" if q == "0" else ("+" if int(q) > 0 else "-") + (str(abs(int(q))) if abs(int(q)) > 1 else ""))
              for sp, q in re.findall(r'\["(\w+)", (-?\d+)\]', block)}
check(MO_PRESETS == {"O2", "N2", "B2", "He2", "NO", "O2-2"}, f"moDiagram presets read as {sorted(MO_PRESETS)}")
for pid in ("t5-7-attempt", "t5-7-transfer"):
    check(not set(ASKED_MO[pid]) & MO_PRESETS, f"{pid} uses an explorer preset species")
import ch5_data                              # noqa: E402
CHI_PRESETS = {k for k, *_ in ch5_data.CHIRAL_PRESETS}
check(not {"2-butanol", "limonene"} & CHI_PRESETS, "a t5-6 attempt or transfer molecule is a chirality-explorer preset")

print(f"MO species checked: {len(PRINTED)} textbook values, {len(K.SPECIES)} bank species; molecules checked for stereocenters: {len(K.SMI)}")
if errs:
    print(f"{len(errs)} problems:")
    for e in errs:
        print("  -", e)
    sys.exit(1)
print("all checks passed")

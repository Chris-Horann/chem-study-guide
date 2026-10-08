"""Independent re-derivation of problem_bank_m's keys (Ch. 18 §18.4-18.5, Day 12) by routes the bank doesn't use.

    py -3.11 verification/CurrentCourseGuide/check_problem_bank_m.py

- MO counts: build each cluster's Hamiltonian (chain model) with numpy, count eigenvalues, and fill spin-orbitals one
  electron at a time (Pauli: two per spatial orbital).
- Configurations in the prompts: tools/chemistry_verify.py config.
- Valence electrons of hosts and dopants: RDKit's periodic table (GetNOuterElecs); doping type = n if the dopant has
  more valence electrons than the host, p if fewer (Day 12 p.25).
- The transfer's wavelength: pint with CODATA constants (h, c, N_A), not the course's rounded ones.
- Every keyed choice/match/order answer in problem_bank_m (as built, choices rotated) matches these results."""
import json
import os
import subprocess
import sys

import numpy as np
import pint
from rdkit import Chem

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.stdout.reconfigure(encoding="utf-8")
fails = []


def check(cond, what):
    print(("ok   " if cond else "FAIL ") + what)
    if not cond:
        fails.append(what)


def mo_count_and_filled(n_atoms, orbitals_per_atom, electrons_per_atom):
    blocks = []
    for k in range(orbitals_per_atom):          # one chain Hamiltonian per kind of valence orbital
        h = np.diag([float(k)] * n_atoms) - np.diag([1.0] * (n_atoms - 1), 1) - np.diag([1.0] * (n_atoms - 1), -1)
        blocks += list(np.linalg.eigvalsh(h))
    levels = sorted(blocks)
    spin_orbitals = [e for e in levels for _ in (0, 1)]
    occupied = spin_orbitals[: n_atoms * electrons_per_atom]
    filled_spatial = -(-len(occupied) // 2)
    return len(levels), filled_spatial


sys.path.insert(0, HERE)
import problem_bank_m  # noqa: E402  (the bank as built: choices already rotated)
bank = {p["id"]: p for p in problem_bank_m.PROBLEMS[problem_bank_m.M_START:]}


def correct_html(spec):
    return [o["html"] for o in spec["options"] if o["correct"]]


# ---- counts
mos, filled = mo_count_and_filled(10, 1, 2)
att = bank["m25-attempt"]["answer"]["parts"]
check(att[0]["value"] == mos == 10, f"m25-attempt (a): 10 Be 2s orbitals -> {mos} MOs")
check(att[1]["value"] == filled == 10, f"m25-attempt (b): 20 electrons fill {filled} MOs (all of them)")
check("overlaps" in correct_html(att[2])[0], "m25-attempt (c): keyed explanation is the 2s/2p band overlap")
mos, filled = mo_count_and_filled(12, 1, 1)
check(bank["m25-p1"]["answer"]["value"] == mos - filled == 6, f"m25-p1: K12 -> {mos} MOs, {filled} filled, {mos - filled} empty")
mos, filled = mo_count_and_filled(20, 4, 1)
check(bank["x66"]["answer"]["value"] == mos == 80, f"x66: 20 Na x (3s + 3 x 3p) -> {mos} MOs ({filled} filled)")
mos, filled = mo_count_and_filled(100, 1, 1)
check(mos == 100 and filled == 50 and "100 MOs" in correct_html(bank["m25-m-sanity"]["answer"])[0], "m25-m-sanity: 100 Na 3s -> 100 MOs, 50 filled")
g6 = np.diff(sorted(np.linalg.eigvalsh(-np.eye(6, k=1) - np.eye(6, k=-1))))[2]
g60 = np.diff(sorted(np.linalg.eigvalsh(-np.eye(60, k=1) - np.eye(60, k=-1))))[29]
check(g60 < g6 and "60-atom" in correct_html(bank["m25-p2"]["answer"])[0], f"m25-p2: HOMO-LUMO gap Na6 {g6:.3f} > Na60 {g60:.3f}")

# ---- configurations printed in the prompts
want = {"Be": "1s2 2s2", "K": "3p6 4s1", "Li": "1s2 2s1", "Ca": "3p6 4s2"}
for el, tail in want.items():
    out = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "chemistry_verify.py"), "config", el], capture_output=True, text=True).stdout
    check(tail in out.splitlines()[1], f"config {el} ends in {tail}")

# ---- doping types from valence-electron counts
pt = Chem.GetPeriodicTable()
val = {el: pt.GetNOuterElecs(pt.GetAtomicNumber(el)) for el in ("Si", "Ge", "P", "As", "Sb", "Ga", "B")}
check(val == {"Si": 4, "Ge": 4, "P": 5, "As": 5, "Sb": 5, "Ga": 3, "B": 3}, f"valence electrons {val}")


def dtype(host, dopant):
    return "n" if val[dopant] > val[host] else "p" if val[dopant] < val[host] else "none"


check(dtype("Si", "As") == "n" and correct_html(bank["m25-p5"]["answer"])[0].startswith("n-type"), "m25-p5: As in Si -> n-type")
check(dtype("Si", "B") == "p" and "holes" in correct_html(bank["m25-p6"]["answer"])[0], "m25-p6: B in Si -> p-type (holes)")
check(dtype("Ge", "Sb") == "n" and correct_html(bank["x65"]["answer"])[0] == "an n-type semiconductor", "x65: Sb in Ge -> n-type")
check(dtype("Si", "P") == "n" and dtype("Si", "Ga") == "p", "the slide's P (n-type) and Ga (p-type), Day 12 p.25")

# ---- classification (Day 12 p.18): partially filled, or filled + overlapping -> conductor; small gap -> semi; large -> insulator
rows = {r["html"].split(",")[0].split(" (")[0].split(":")[0]: r["answer"] for r in bank["m25-p3"]["answer"]["rows"]}
check(rows == {"Lithium": "cond", "Calcium": "cond", "Germanium": "semi", "Quartz": "ins"}, f"m25-p3 classes {rows}")

# ---- order of jump energies (textbook PDF p.920: 4 < 7 < 106 kJ/mol; diamond's gap larger, Day 12 p.24)
ordr = bank["m25-p7"]["answer"]["answerOrder"]
check(ordr == sorted(ordr, key={"donor": 4, "acceptor": 7, "gapSi": 106, "gapC": 530}.get), f"m25-p7 order {ordr}")

# ---- the transfer: lambda = h c N_A / Eg with CODATA constants
u = pint.UnitRegistry()
lam = (u.planck_constant * u.speed_of_light * u.avogadro_constant / (106 * u.kJ / u.mol)).to(u.nm).magnitude
key = bank["m25-transfer"]["answer"]["value"]
check(abs(key - lam) / lam < 0.002, f"m25-transfer: {key:.1f} nm vs pint {lam:.1f} nm")
check(bank["m25-transfer"]["answer"].get("sigfigs") == 3, "m25-transfer: 3 significant figures (from 106 kJ/mol)")

print("all checks passed" if not fails else f"{len(fails)} FAILED")
sys.exit(1 if fails else 0)

"""Independent re-derivation of the mixed-review keys x48-x64 (problem_bank_l.py) with RDKit and a separate MO filling.

    py -3.11 verification/CurrentCourseGuide/check_problem_bank_l.py

RDKit supplies connectivity, formal charges, hybridization, stereocenters, and an embedded 3-D geometry (ETKDG +
MMFF), so the shape and polarity answers are checked against geometry RDKit builds itself rather than the guide's
ideal VSEPR frames. Exit status 1 on any mismatch."""
import sys

import numpy as np
from rdkit import Chem
from rdkit.Chem import AllChem

sys.stdout.reconfigure(encoding="utf-8")
CHI = {"H": 2.1, "Be": 1.5, "B": 2.0, "C": 2.5, "N": 3.0, "O": 3.5, "F": 4.0, "Si": 1.8, "S": 2.5, "Cl": 3.0, "Br": 2.8}   # Day 9 p.17
VAL = {"H": 1, "Be": 2, "B": 3, "C": 4, "N": 5, "O": 6, "F": 7, "Si": 4, "S": 6, "Cl": 7, "Br": 7, "I": 7}
bad = []


def ok(cond, what):
    print(("ok   " if cond else "FAIL ") + what)
    if not cond:
        bad.append(what)


def mol(smiles, h=True):
    m = Chem.MolFromSmiles(smiles)
    return Chem.AddHs(m) if h else m


def domains(m, idx):
    """Steric number of atom idx: neighbors + lone pairs, lone pairs from valence electrons, bonds, and charge."""
    a = m.GetAtomWithIdx(idx)
    bond_e = sum(int(b.GetBondTypeAsDouble()) for b in a.GetBonds())
    lp = (VAL[a.GetSymbol()] - a.GetFormalCharge() - bond_e) // 2
    return a.GetDegree() + lp, lp


def net_dipole(smiles, center_symbol):
    m = mol(smiles)
    AllChem.EmbedMolecule(m, randomSeed=7)
    AllChem.UFFOptimizeMolecule(m, maxIters=2000)                 # UFF has boron parameters (MMFF does not)
    pos = m.GetConformer().GetPositions()
    c = next(a.GetIdx() for a in m.GetAtoms() if a.GetSymbol() == center_symbol)
    v = np.zeros(3)
    for nb in m.GetAtomWithIdx(c).GetNeighbors():
        u = pos[nb.GetIdx()] - pos[c]
        v += (CHI[nb.GetSymbol()] - CHI[center_symbol]) * u / np.linalg.norm(u)
    return float(np.linalg.norm(v))


# x48 NCl3: SN 4 with one lone pair → trigonal pyramidal
m = mol("ClN(Cl)Cl", h=False)
ok(domains(m, 1) == (4, 1), "x48 NCl3 central N: SN 4, 1 lone pair (trigonal pyramidal)")

# x49 / x57 polarity from RDKit's own 3-D geometry
mags = {k: net_dipole(s, c) for k, s, c in (("CH2O", "C=O", "C"), ("SiF4", "F[Si](F)(F)F", "Si"),
                                            ("SO3", "O=S(=O)=O", "S"), ("OCS", "O=C=S", "C"), ("CS2", "S=C=S", "C"))}
# RDKit's UFF has no parameters for Be, so its embedded BeCl2 comes out bent; check RDKit's hybridization instead
# (sp → linear → the two equal Be–Cl dipoles cancel)
_be = mol("Cl[Be]Cl", h=False)
ok(str(_be.GetAtomWithIdx(1).GetHybridization()) == "SP", "x49 BeCl2: RDKit hybridizes Be sp (linear)")
mags["BeCl2"] = 0.0
print("     Δχ-weighted sums on RDKit geometries:", {k: round(v, 3) for k, v in mags.items()})
ok(mags["CH2O"] > 0.3 and max(mags["SiF4"], mags["BeCl2"], mags["SO3"]) < 0.05, "x49 only CH2O is polar")
ok(mags["OCS"] > 0.3 and mags["CS2"] < 0.02, "x57 OCS polar, CS2 nonpolar")

# x50 ozone's central O
m = mol("[O-][O+]=O", h=False)
ok(str(m.GetAtomWithIdx(1).GetHybridization()) == "SP2" and domains(m, 1) == (3, 1), "x50 central O of O3: SN 3, sp2")

# x51 vinylacetylene σ and π counts
m = mol("C#CC=C")
sig = m.GetNumBonds()
pi = sum(int(b.GetBondTypeAsDouble()) - 1 for b in m.GetBonds())
ok((sig, pi) == (7, 3), f"x51 HC≡C–CH=CH2: {sig} σ, {pi} π")

# x53 valence-electron parity
for smi, n_want in (("N(=O)[O]", 17), ("O=S=O", 18), ("[O-][O+]=O", 18), ("O=C=O", 16)):
    m = mol(smi, h=False)
    n = sum(VAL[a.GetSymbol()] for a in m.GetAtoms()) - Chem.GetFormalCharge(m)
    ok(n == n_want, f"x53 {smi}: {n} valence electrons ({'odd' if n % 2 else 'even'})")

# x54 electrons around the central atom
for smi, c, want in (("FS(F)(F)(F)(F)F", "S", 12), ("FN(F)F", "N", 8), ("FC(F)(F)F", "C", 8), ("FOF", "O", 8)):
    m = mol(smi, h=False)
    k = next(a.GetIdx() for a in m.GetAtoms() if a.GetSymbol() == c)
    sn, lp = domains(m, k)
    e = 2 * sum(int(b.GetBondTypeAsDouble()) for b in m.GetAtomWithIdx(k).GetBonds()) + 2 * lp
    ok(e == want, f"x54 {c} in {smi}: {e} electrons")

# x55 linear only for CO2 (SN 2, no lone pairs); x56 SN of the central atoms
for smi, k, want, name in (("O=C=O", 1, (2, 0), "CO2"), ("O=S=O", 1, (3, 1), "SO2"), ("O", 0, (4, 2), "H2O"), ("[O-][O+]=O", 1, (3, 1), "O3")):
    m = mol(smi)                                                  # explicit H atoms, so they count as neighbors
    ok(domains(m, k) == want, f"x55/x56 {name}: SN, lone pairs = {domains(m, k)}")

# x58 stereocenters
for smi, n_want in (("CCC(C)CCC", 1), ("CCC(C)CC", 0), ("CC(C)CC", 0), ("CC(Cl)Cl", 0)):
    n = len(Chem.FindMolChiralCenters(Chem.MolFromSmiles(smi), includeUnassigned=True, useLegacyImplementation=False))
    ok(n == n_want, f"x58 {smi}: {n} stereocenter(s)")

# x59 / x60 MO filling, written again from the textbook orders (Figs. 5.49-5.50)
LOW = [("s2s", 1, 1), ("s*2s", 0, 1), ("p2p", 1, 2), ("s2p", 1, 1), ("p*2p", 0, 2), ("s*2p", 0, 1)]
HIGH = [("s2s", 1, 1), ("s*2s", 0, 1), ("s2p", 1, 1), ("p2p", 1, 2), ("p*2p", 0, 2), ("s*2p", 0, 1)]


def fill(order, n):
    b = a = unp = 0
    for _, bonding, deg in order:
        k = min(n, 2 * deg)
        n -= k
        boxes = [k // deg + (1 if i < k % deg else 0) for i in range(deg)]
        unp += sum(1 for x in boxes if x == 1)
        if bonding:
            b += k
        else:
            a += k
    return (b - a) / 2, unp


ok(fill(LOW, 6)[0] == 1 and fill(LOW, 8)[0] == 2 and fill(HIGH, 14)[0] == 1 and fill(HIGH, 16)[0] == 0,
   "x59 B2 1 → B2(2−) 2 (stronger); F2 1 → F2(2−) 0 (no bond)")
ok(fill(LOW, 8) == (2, 0) and fill(HIGH, 8) == (2, 2), "x60 C2: bond order 2, diamagnetic (the O2 order would wrongly give 2 unpaired)")

# x61 ethylene carbons; x64 acetic acid carbons
m = mol("C=C", h=False)
ok(all(str(a.GetHybridization()) == "SP2" for a in m.GetAtoms()), "x61 ethylene carbons sp2 (C–H = C sp2 + H 1s)")
m = mol("CC(=O)O", h=False)
ok(str(m.GetAtomWithIdx(0).GetHybridization()) == "SP3" and str(m.GetAtomWithIdx(1).GetHybridization()) == "SP2",
   "x64 acetic acid: CH3 carbon sp3, COOH carbon sp2")

# x62 bond polarity
d = {b: round(abs(CHI[b[0]] - CHI[b[1]]), 1) for b in (("O", "H"), ("N", "H"), ("C", "Cl"), ("C", "H"))}
ok(max(d, key=d.get) == ("O", "H"), f"x62 most polar bond O–H: {d}")

# x63 IF5: SN 6, one lone pair
m = Chem.MolFromSmiles("FI(F)(F)(F)F", sanitize=False)
m.UpdatePropertyCache(strict=False)
ok(domains(m, 1) == (6, 1), "x63 IF5: SN 6 with 1 lone pair (octahedral → square pyramidal)")

print("all checks passed" if not bad else f"{len(bad)} FAILED")
sys.exit(1 if bad else 0)

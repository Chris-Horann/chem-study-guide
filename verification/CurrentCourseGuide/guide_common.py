"""Shared constants, course data tables, and HTML formatting helpers for the
CurrentCourseGuide build. Course values come from the ingested lecture slides
(see materials/COURSE_INDEX.md); anything else is marked BACKGROUND."""
import math
import re

# ---------------------------------------------------------------- constants
# Course (lecture) values
C = 2.998e8            # m/s              Day 2 p.30
H = 6.626e-34          # J s              Day 3 p.17 (Day 4 p.11 lists 6.62607004e-34)
BOHR = 2.178e-18       # J                Day 4 p.10
COUL = 2.31e-19        # J nm             Day 7 p.15
BALMER = 364.56        # nm               Day 3 p.21
ME = 9.109e-31         # kg               Day 2 p.12 (9.109e-28 g); Day 2 p.22 lists 9.10938e-31
MP_KG = 1.67262e-27    # kg               Day 2 p.22
MP_AMU = 1.00728       # amu              Day 2 p.22
ME_AMU = 5.48580e-4    # amu              Day 2 p.22
# BACKGROUND (not on any slide)
NA = 6.022e23          # mol^-1           textbook PDF p.183 uses 6.022e23
EV = 1.602177e-19      # J per eV         (work-function conversion only)

HC = H * C

# ---------------------------------------------------------------- course data
# Atomic radii, pm (Day 6 p.24 = Day 7 p.7; unit from textbook Fig. 3.35 caption)
ATOMIC_RADIUS = {
    "H": 37, "He": 32,
    "Li": 152, "Be": 112, "B": 88, "C": 77, "N": 75, "O": 73, "F": 71, "Ne": 69,
    "Na": 186, "Mg": 160, "Al": 143, "Si": 117, "P": 110, "S": 103, "Cl": 99, "Ar": 97,
    "K": 227, "Ca": 197, "Ga": 135, "Ge": 122, "As": 121, "Se": 119, "Br": 114, "Kr": 110,
    "Rb": 247, "Sr": 215, "In": 167, "Sn": 140, "Sb": 141, "Te": 143, "I": 133, "Xe": 130,
    "Cs": 265, "Ba": 222, "Tl": 170, "Pb": 154, "Bi": 150, "Po": 167, "At": 140, "Rn": 145,
}
# Ionic radii, pm (Day 7 p.8 = textbook Fig. 3.36)
IONIC_RADIUS = {
    "Li+": 76, "Be2+": 27, "O2-": 140, "F-": 133,
    "Na+": 102, "Mg2+": 72, "Al3+": 54, "S2-": 184, "Cl-": 181,
    "K+": 138, "Ca2+": 100, "Se2-": 198, "Br-": 195,
}
# First ionization energies, kJ/mol (Day 7 p.9)
IE1 = {
    "H": 1312, "He": 2372,
    "Li": 520, "Be": 900, "B": 801, "C": 1086, "N": 1402, "O": 1314, "F": 1681, "Ne": 2081,
    "Na": 496, "Mg": 738, "Al": 578, "Si": 787, "P": 1012, "S": 1000, "Cl": 1251, "Ar": 1521,
    "K": 419, "Ca": 590, "Ga": 579, "Ge": 762, "As": 947, "Se": 941, "Br": 1140, "Kr": 1351,
    "Rb": 403, "Sr": 550, "In": 558, "Sn": 709, "Sb": 834, "Te": 869, "I": 1008, "Xe": 1170,
    "Cs": 376, "Ba": 503, "Tl": 589, "Pb": 716, "Bi": 703, "Po": 812, "At": 925, "Rn": 1037,
}
# Electron affinities, kJ/mol (Day 7 p.11). ">0" entries -> None with flag; calculated values flagged.
EA = {
    "H": -72.6, "He": 0.0,
    "Li": -59.6, "Be": None, "B": -26.7, "C": -122, "N": 7, "O": -141, "F": -328, "Ne": 29,
    "Na": -52.9, "Mg": None, "Al": -42.5, "Si": -134, "P": -72.0, "S": -200, "Cl": -349, "Ar": 35,
    "K": -48.4, "Ca": -2.4, "Ga": -28.9, "Ge": -119, "As": -78.2, "Se": -195, "Br": -325, "Kr": 39,
    "Rb": -46.9, "Sr": -5.0, "In": -28.9, "Sn": -107, "Sb": -103, "Te": -190, "I": -295, "Xe": 41,
    "Cs": -45.5, "Ba": -14, "Tl": -19.2, "Pb": -35.2, "Bi": -91.3, "Po": -183.3, "At": -270, "Rn": 41,
}
EA_GT0 = ["Be", "Mg"]                                   # printed ">0"
EA_CALC = ["He", "Ne", "Ar", "Kr", "Xe", "Rn", "At"]    # printed with superscript a ("Calculated values")
# Successive ionization energies, kJ/mol (Day 7 p.10 = textbook Table 3.2)
SUCCESSIVE_IE = {
    "H": [1312],
    "He": [2372, 5249],
    "Li": [520, 7296, 12040],
    "Be": [900, 1758, 15050, 21070],
    "B": [801, 2426, 3660, 24682, 32508],
    "C": [1086, 2348, 4617, 6201, 37926, 46956],
    "N": [1402, 2860, 4581, 7465, 9391, 52976, 64414],
    "O": [1314, 3383, 5298, 7465, 10956, 13304, 71036, 84280],
    "F": [1681, 3371, 6020, 8428, 11017, 15170, 17879, 92106, 106554],
    "Ne": [2081, 3949, 6140, 9391, 12160, 15231, 19986, 23057, 115584, 131236],
}
VALENCE_2ND_PERIOD = {"H": 1, "He": 2, "Li": 1, "Be": 2, "B": 3, "C": 4, "N": 5, "O": 6, "F": 7, "Ne": 8}
# Lattice energies, kJ/mol (Day 7 p.17, slide version of Table 4.2 incl. CaS)
LATTICE = {"LiF": -1049, "LiCl": -864, "NaF": -930, "NaCl": -786, "NaBr": -754,
           "KCl": -720, "KBr": -691, "MgO": -3791, "MgCl2": -2540, "CaS": -3093}
# BACKGROUND: approximate work functions, 1e-19 J (Wolfram|Alpha eV values x 1.602e-19);
# the lecture graph (Day 3 p.19) gives only the order Cs < K < Ca < Mg < Hg.
WORK_FUNCTION_EV = {"Cs": 1.95, "K": 2.29, "Ca": 2.87, "Mg": 3.66, "Hg": 4.48}
WORK_FUNCTION_E19 = {k: round(v * EV / 1e-19, 2) for k, v in WORK_FUNCTION_EV.items()}

# Main-group layout (period, column index 0..7 for groups 1,2,13..18)
MAIN_GROUP_LAYOUT = [
    ["H", None, None, None, None, None, None, "He"],
    ["Li", "Be", "B", "C", "N", "O", "F", "Ne"],
    ["Na", "Mg", "Al", "Si", "P", "S", "Cl", "Ar"],
    ["K", "Ca", "Ga", "Ge", "As", "Se", "Br", "Kr"],
    ["Rb", "Sr", "In", "Sn", "Sb", "Te", "I", "Xe"],
    ["Cs", "Ba", "Tl", "Pb", "Bi", "Po", "At", "Rn"],
]
GROUP_LABELS = [1, 2, 13, 14, 15, 16, 17, 18]

# Elements 1-36 (BACKGROUND periodic-table facts, for the configuration builder)
ELEMENTS = [
    ("H", "hydrogen"), ("He", "helium"), ("Li", "lithium"), ("Be", "beryllium"), ("B", "boron"),
    ("C", "carbon"), ("N", "nitrogen"), ("O", "oxygen"), ("F", "fluorine"), ("Ne", "neon"),
    ("Na", "sodium"), ("Mg", "magnesium"), ("Al", "aluminum"), ("Si", "silicon"), ("P", "phosphorus"),
    ("S", "sulfur"), ("Cl", "chlorine"), ("Ar", "argon"), ("K", "potassium"), ("Ca", "calcium"),
    ("Sc", "scandium"), ("Ti", "titanium"), ("V", "vanadium"), ("Cr", "chromium"), ("Mn", "manganese"),
    ("Fe", "iron"), ("Co", "cobalt"), ("Ni", "nickel"), ("Cu", "copper"), ("Zn", "zinc"),
    ("Ga", "gallium"), ("Ge", "germanium"), ("As", "arsenic"), ("Se", "selenium"), ("Br", "bromine"),
    ("Kr", "krypton"),
]
# Real ground-state exceptions in Z <= 36 (BACKGROUND; the course ignores them, Day 7 p.6)
CONFIG_EXCEPTIONS = {24: "[Ar]4s¹3d⁵", 29: "[Ar]4s¹3d¹⁰"}
FILL_ORDER = ["1s", "2s", "2p", "3s", "3p", "4s", "3d", "4p", "5s", "4d", "5p"]
CAPACITY = {"s": 2, "p": 6, "d": 10, "f": 14}

# ---------------------------------------------------------------- physics helpers
def photon_energy_from_nm(lam_nm):
    return HC / (lam_nm * 1e-9)

def nm_from_energy(E_J):
    return HC / E_J * 1e9

def bohr_dE(n_i, n_f):
    """Professor's form: dE = -2.178e-18 J (1/n_f^2 - 1/n_i^2); n may be math.inf."""
    inv = lambda n: 0.0 if n == math.inf else 1.0 / n**2
    return -BOHR * (inv(n_f) - inv(n_i))

def de_broglie(m_kg, u):
    return H / (m_kg * u)

def e_el(q1, q2, d_nm):
    return COUL * q1 * q2 / d_nm

def aufbau_config(z):
    """Aufbau (course rules, no exceptions): list of (subshell, count) in filling order."""
    out, left = [], z
    for sub in FILL_ORDER:
        if left <= 0:
            break
        k = min(left, CAPACITY[sub[-1]])
        out.append((sub, k))
        left -= k
    return out

def ion_config(z, charge):
    """Course rule: anions add by Aufbau; cations remove from highest n first
    (within the same n: p before s, i.e. highest l first)."""
    if charge <= 0:
        return aufbau_config(z - charge)
    occ = dict(aufbau_config(z))
    for _ in range(charge):
        # highest n, then highest l among occupied subshells
        cand = sorted([s for s, k in occ.items() if k > 0],
                      key=lambda s: (int(s[:-1]), "spdf".index(s[-1])))
        last = cand[-1]
        occ[last] -= 1
        if occ[last] == 0:
            del occ[last]
    return [(s, occ[s]) for s in FILL_ORDER if s in occ]

def unpaired(config):
    total = 0
    for sub, k in config:
        orbitals = CAPACITY[sub[-1]] // 2
        total += k if k <= orbitals else 2 * orbitals - k
    return total

# ---------------------------------------------------------------- HTML helpers
SUP = str.maketrans("0123456789+-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻")
MINUS = "−"

def sig_round(x, sf):
    if x == 0:
        return 0.0
    return round(x, sf - 1 - int(math.floor(math.log10(abs(x)))))

def sci_parts(x, sf):
    """Return (mantissa_str, exponent) with sf significant figures."""
    if x == 0:
        return ("0", 0)
    exp = int(math.floor(math.log10(abs(x))))
    mant = x / 10**exp
    mant_r = round(mant, sf - 1)
    if abs(mant_r) >= 10:
        exp += 1
        mant_r = round(x / 10**exp, sf - 1)
    s = f"{abs(mant_r):.{sf - 1}f}"
    if x < 0:
        s = MINUS + s
    return s, exp

def sci(x, sf=3):
    """Scientific notation as HTML: 5.66 × 10<sup>14</sup> (true minus signs)."""
    m, e = sci_parts(x, sf)
    if e == 0:
        return m
    es = (MINUS + str(-e)) if e < 0 else str(e)
    return f"{m} × 10<sup>{es}</sup>"

def fix(x, decimals):
    s = f"{abs(x):.{decimals}f}"
    return (MINUS + s) if x < 0 else s

def num(x, sf=3):
    """Plain (non-scientific) number rounded to sf significant figures."""
    r = sig_round(x, sf)
    exp = int(math.floor(math.log10(abs(r)))) if r else 0
    decimals = max(0, sf - 1 - exp)
    s = f"{abs(r):,.{decimals}f}"
    return (MINUS + s) if r < 0 else s

def chem(s):
    """Formula / ion to HTML: 'Al2O3' -> Al<sub>2</sub>O<sub>3</sub>; 'Mg^2+' -> Mg<sup>2+</sup>;
    'O^2-' -> O<sup>2−</sup>; 'e^-' -> e<sup>−</sup>."""
    if "^" in s:
        base, charge = s.split("^", 1)
        charge = charge.replace("-", MINUS)
        return chem(base) + f"<sup>{charge}</sup>"
    return re.sub(r"(?<=[A-Za-z\)])(\d+)", r"<sub>\1</sub>", s)

def config_html(config):
    """[(sub, k)] -> '1s<sup>2</sup>2s<sup>2</sup>…'"""
    return "".join(f"{s}<sup>{k}</sup>" for s, k in config)

# ================================================================ TEXTBOOK-PREVIEW data (Gilbert 3rd ed.)
# Pauling electronegativities exactly as printed in Fig. 4.5 (TB PDF p.187, printed 153).
ELECTRONEGATIVITY = {
    "H": 2.1,
    "Li": 1.1, "Be": 1.5, "B": 2.0, "C": 2.5, "N": 3.0, "O": 3.5, "F": 4.0,
    "Na": 0.9, "Mg": 1.2, "Al": 1.5, "Si": 1.8, "P": 2.1, "S": 2.5, "Cl": 3.0,
    "K": 0.8, "Ca": 1.0, "Sc": 1.3, "Ti": 1.5, "V": 1.6, "Cr": 1.6, "Mn": 1.5, "Fe": 1.8, "Co": 1.8,
    "Ni": 1.8, "Cu": 1.9, "Zn": 1.6, "Ga": 1.6, "Ge": 1.8, "As": 2.0, "Se": 2.4, "Br": 2.8,
    "Rb": 0.8, "Sr": 1.0, "Y": 1.2, "Zr": 1.4, "Nb": 1.6, "Mo": 1.8, "Tc": 1.9, "Ru": 2.2, "Rh": 2.2,
    "Pd": 2.2, "Ag": 1.9, "Cd": 1.7, "In": 1.7, "Sn": 1.8, "Sb": 1.9, "Te": 2.1, "I": 2.5,
    "Cs": 0.7, "Ba": 0.9, "La": 1.1, "Hf": 1.3, "Ta": 1.5, "W": 1.7, "Re": 1.9, "Os": 2.2, "Ir": 2.2,
    "Pt": 2.2, "Au": 2.4, "Hg": 1.9, "Tl": 1.8, "Pb": 1.9, "Bi": 1.9, "Po": 2.0, "At": 2.2,
    "Fr": 0.7, "Ra": 0.9, "Ac": 1.1,
}
def bond_class(dchi):
    """Textbook §4.2 guidelines (TB PDF p.186): <= 0.4 nonpolar covalent; 0.4-2.0 polar covalent; >= 2.0 ionic."""
    d = round(abs(dchi), 2)
    if d <= 0.4:
        return "nonpolar covalent"
    if d < 2.0:
        return "polar covalent"
    return "ionic"

# t values (Table 1.5, TB PDF p.67, printed 33): key = n - 1
T_TABLE = {3: (2.353, 3.182, 5.841), 4: (2.132, 2.776, 4.604), 5: (2.015, 2.571, 4.032),
           10: (1.812, 2.228, 3.169), 20: (1.725, 2.086, 2.845), "inf": (1.645, 1.960, 2.576)}
# Grubbs reference Z (Table 1.7, TB PDF p.69, printed 35): key = n -> (95%, 99%)
GRUBBS_Z = {3: (1.155, 1.155), 4: (1.481, 1.496), 5: (1.715, 1.764), 6: (1.887, 1.973), 7: (2.020, 2.139),
            8: (2.126, 2.274), 9: (2.215, 2.387), 10: (2.290, 2.482), 11: (2.355, 2.564), 12: (2.412, 2.636)}

def mean(xs):
    return sum(xs) / len(xs)

def stdev(xs):
    m = mean(xs)
    return math.sqrt(sum((x - m) ** 2 for x in xs) / (len(xs) - 1))

# Atomic masses (u = g/mol). Values the textbook prints in §2.4–2.6 are used where it prints them
# (H 1.0079, C 12.011, O 15.999, S 32.065, Cl 35.453, Ca 40.078, Xe 131.29, Au 196.97, Sr 87.62, Pt 195.08);
# the rest are standard atomic weights of the same vintage (BACKGROUND).
ATOMIC_MASS = {
    "H": 1.0079, "He": 4.0026, "Li": 6.941, "Be": 9.0122, "B": 10.811, "C": 12.011, "N": 14.007, "O": 15.999,
    "F": 18.998, "Ne": 20.180, "Na": 22.990, "Mg": 24.305, "Al": 26.982, "Si": 28.086, "P": 30.974,
    "S": 32.065, "Cl": 35.453, "Ar": 39.948, "K": 39.098, "Ca": 40.078, "Fe": 55.845, "Cu": 63.546,
    "Zn": 65.38, "Br": 79.904, "Ag": 107.87, "I": 126.90, "Au": 196.97, "Hg": 200.59, "Pb": 207.2,
    "Sr": 87.62, "Ba": 137.33, "Xe": 131.29, "Kr": 83.798, "Ga": 69.723, "Pt": 195.08,
}
AMU_KG = 1.66054e-27   # 1 u in kg (textbook §2.1, TB PDF p.86)

def formula_counts(f):
    """'C6H12O6' -> {'C': 6, 'H': 12, 'O': 6} (no parentheses)."""
    out = {}
    for sym, n in re.findall(r"([A-Z][a-z]?)(\d*)", f):
        out[sym] = out.get(sym, 0) + (int(n) if n else 1)
    return out

def molar_mass(f):
    return sum(ATOMIC_MASS[s] * n for s, n in formula_counts(f).items())

# Isotope masses (u) and natural abundances (fraction). BACKGROUND reference values (IUPAC/NIST),
# except the neon set, which the textbook prints in Table 2.3 (TB PDF p.94).
ISOTOPES = {
    "Ne": [(20, 19.9924, 0.904838), (21, 20.9940, 0.002696), (22, 21.9914, 0.092465)],
    "B": [(10, 10.0129, 0.199), (11, 11.0093, 0.801)],
    "Mg": [(24, 23.9850, 0.7899), (25, 24.9858, 0.1000), (26, 25.9826, 0.1101)],
    "Cl": [(35, 34.9689, 0.7576), (37, 36.9659, 0.2424)],
    "Br": [(79, 78.9183, 0.5069), (81, 80.9163, 0.4931)],
    "Cu": [(63, 62.9296, 0.6915), (65, 64.9278, 0.3085)],
    "Ga": [(69, 68.9256, 0.60108), (71, 70.9247, 0.39892)],
}

# Photoelectron binding energies, MJ/mol, by subshell. Li and Al are the textbook's values
# (TB PDF p.163, printed 129); every other element is an approximate reference value (BACKGROUND),
# whose outermost value agrees with IE1 on Day 7 p.9.
PES = {
    "H": [("1s", 1.31, 1)], "He": [("1s", 2.37, 2)],
    "Li": [("1s", 6.26, 2), ("2s", 0.52, 1)],
    "Be": [("1s", 11.5, 2), ("2s", 0.90, 2)],
    "B": [("1s", 19.3, 2), ("2s", 1.36, 2), ("2p", 0.80, 1)],
    "C": [("1s", 28.6, 2), ("2s", 1.72, 2), ("2p", 1.09, 2)],
    "N": [("1s", 39.6, 2), ("2s", 2.45, 2), ("2p", 1.40, 3)],
    "O": [("1s", 52.6, 2), ("2s", 3.12, 2), ("2p", 1.31, 4)],
    "F": [("1s", 67.2, 2), ("2s", 3.88, 2), ("2p", 1.68, 5)],
    "Ne": [("1s", 84.0, 2), ("2s", 4.68, 2), ("2p", 2.08, 6)],
    "Na": [("1s", 104, 2), ("2s", 6.84, 2), ("2p", 3.67, 6), ("3s", 0.50, 1)],
    "Mg": [("1s", 126, 2), ("2s", 9.07, 2), ("2p", 5.31, 6), ("3s", 0.74, 2)],
    "Al": [("1s", 151, 2), ("2s", 12.1, 2), ("2p", 7.19, 6), ("3s", 1.09, 2), ("3p", 0.58, 1)],
    "Si": [("1s", 178, 2), ("2s", 15.1, 2), ("2p", 10.3, 6), ("3s", 1.46, 2), ("3p", 0.79, 2)],
    "P": [("1s", 208, 2), ("2s", 18.7, 2), ("2p", 13.5, 6), ("3s", 1.95, 2), ("3p", 1.01, 3)],
    "S": [("1s", 239, 2), ("2s", 22.7, 2), ("2p", 16.5, 6), ("3s", 2.05, 2), ("3p", 1.00, 4)],
    "Cl": [("1s", 273, 2), ("2s", 26.8, 2), ("2p", 20.2, 6), ("3s", 2.44, 2), ("3p", 1.25, 5)],
    "Ar": [("1s", 309, 2), ("2s", 31.5, 2), ("2p", 24.1, 6), ("3s", 2.82, 2), ("3p", 1.52, 6)],
    "K": [("1s", 347, 2), ("2s", 37.1, 2), ("2p", 29.1, 6), ("3s", 3.93, 2), ("3p", 2.38, 6), ("4s", 0.42, 1)],
    "Ca": [("1s", 390, 2), ("2s", 42.7, 2), ("2p", 34.0, 6), ("3s", 4.65, 2), ("3p", 2.90, 6), ("4s", 0.59, 2)],
}
PES_TEXTBOOK = ["Li", "Al"]

# Unit equivalencies from Table 1.3 (TB PDF p.54, printed 20)
LB_PER_KG = 2.205
MI_PER_KM = 0.6214
CM_PER_IN = 2.54          # exact
GAL_PER_L = 0.2642
QT_PER_L = 1.057

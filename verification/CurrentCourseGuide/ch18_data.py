"""Reference values for the Ch. 18 band explorer (assets/explorers_ch18.js), computed independently of the JS formula.

The explorer's cluster levels use the closed form alpha - 2*beta*cos(k*pi/(N+1)) for a chain of N atoms. Here the same
levels come from numpy's eigenvalues of the N x N chain Hamiltonian (alpha on the diagonal, -beta next to it), and the
electron filling is done by counting. build_guide.py writes expected() into expected_values.json ("bands");
test_explorers_ch18.js compares the JS calculations with it."""
import math

import numpy as np

S_ALPHA, S_BETA = 0.0, 1.0                  # Na 3s-derived levels (arbitrary units)
P_ALPHA, P_BETA = 3.6, 1.0                  # 3p-derived levels (schematic)
NS = [2, 4, 8, 16, 32, 64]
R = 8.314


def chain_levels(n, alpha, beta):
    h = np.diag([alpha] * n) + np.diag([-beta] * (n - 1), 1) + np.diag([-beta] * (n - 1), -1)
    return sorted(np.linalg.eigvalsh(h).tolist())


def cluster(n):
    s, p = chain_levels(n, S_ALPHA, S_BETA), chain_levels(n, P_ALPHA, P_BETA)
    electrons, filled = n, 0
    while electrons > 0:                     # two per MO, lowest first
        electrons -= 2
        filled += 1
    gap = s[filled] - s[filled - 1]
    return {"levels": s, "pLevels": p, "filled": filled, "empty": n - filled, "gapRatio": gap / (2 * S_BETA),
            "widthRatio": (s[-1] - s[0]) / (4 * S_BETA), "overlap": s[-1] > p[0]}


def cross_factor(eg_kj, t_c):
    return math.exp(-eg_kj * 1000 / (2 * R * (t_c + 273.15)))


def expected():
    return {"bands": {
        "clusters": {str(n): cluster(n) for n in NS},
        "classes": {"diamond": "insulator", "zinc": "conductor", "sodium": "conductor", "silicon": "semiconductor"},   # Day 12 p.24
        "cross": {"Si25": cross_factor(106, 25), "Si100": cross_factor(106, 100), "C25": cross_factor(530, 25)},
    }}


if __name__ == "__main__":
    e = expected()["bands"]
    for n in NS:
        c = e["clusters"][str(n)]
        print(n, c["filled"], c["empty"], round(c["gapRatio"], 4), round(c["widthRatio"], 4), c["overlap"])
    print(e["cross"])

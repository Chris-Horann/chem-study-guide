"""Independent chemistry checks for study-guide content.

Run from the project root (C:\\Users\\chris\\ChemStudy) with Python 3.11:

    py -3.11 tools/chemistry_verify.py molar-mass "Ca3(PO4)2" "CuSO4*5H2O"
    py -3.11 tools/chemistry_verify.py balance  "C3H8 + O2 -> CO2 + H2O"
    py -3.11 tools/chemistry_verify.py balance  "MnO4^- + Fe^2+ + H^+ -> Mn^2+ + Fe^3+ + H2O"
    py -3.11 tools/chemistry_verify.py check    "2 H2(g) + O2(g) -> 2 H2O(l)"
    py -3.11 tools/chemistry_verify.py electrons "SO4^2-" "NH4^+"
    py -3.11 tools/chemistry_verify.py config   Fe  Fe^3+  Cu  Cl^-  24
    py -3.11 tools/chemistry_verify.py qn       3 2 -1 +1/2
    py -3.11 tools/chemistry_verify.py sigfigs  0.00450 1200 1.200e3 "1200."
    py -3.11 tools/chemistry_verify.py round    0.0082057 3
    py -3.11 tools/chemistry_verify.py units    "2.00 mol * 0.08206 L*atm/(mol*K) * 298 K / (10.0 L)" --to atm
    py -3.11 tools/chemistry_verify.py weak-acid --K 1.8e-5 --C 0.10
    py -3.11 tools/chemistry_verify.py weak-acid --K 1.8e-5 --C 0.10 --base
    py -3.11 tools/chemistry_verify.py quadratic 1 1.8e-5 -1.8e-6
    py -3.11 tools/chemistry_verify.py linfit --x 0 10 20 30 --y 1.0 0.61 0.37 0.22 --ty ln

Formula syntax: charges use ^ ("SO4^2-", "Fe^3+", "[Fe(CN)6]^4-"); hydrates use
* or · ("CuSO4*5H2O"); physical states "(s) (l) (g) (aq)" are ignored; electrons
are "e^-" or "e-". Equations: species separated by " + " (spaces required),
arrows ->, →, =, <=>, ⇌. Coefficients may be integers, decimals, or fractions.

These are checks, not explanations. Always reason chemically first, then use
this tool to confirm. Atomic weights come from the `periodictable` package
(IUPAC standard values); if the course periodic table uses rounded values,
re-run with --digits or compare against the course table and report the difference.
"""

from __future__ import annotations

import argparse
import math
import re
import sys
from fractions import Fraction

# ----------------------------------------------------------------- formula parsing

STATE_RE = re.compile(r"\((?:s|l|g|aq|cr|am)\)$", re.I)
CHARGE_RE = re.compile(r"\^\{?\s*(\d*)\s*([+-])\s*\}?$|\^\{?\s*([+-])\s*(\d*)\s*\}?$")
ELECTRON_NAMES = {"e", "e-", "e^-", "e^{-}", "e−"}


def split_charge(s: str) -> tuple[str, int]:
    s = s.strip().replace("−", "-").replace("⁺", "+").replace("⁻", "-")
    m = CHARGE_RE.search(s)
    if not m:
        return s, 0
    if m.group(2):
        mag, sign = m.group(1), m.group(2)
    else:
        sign, mag = m.group(3), m.group(4)
    q = int(mag) if mag else 1
    return s[: m.start()], q if sign == "+" else -q


def parse_group(s: str, i: int = 0, closer: str | None = None) -> tuple[dict[str, int], int]:
    counts: dict[str, int] = {}
    while i < len(s):
        ch = s[i]
        if ch in "([{":
            close = {"(": ")", "[": "]", "{": "}"}[ch]
            inner, i = parse_group(s, i + 1, close)
            n, i = read_int(s, i)
            for k, v in inner.items():
                counts[k] = counts.get(k, 0) + v * n
        elif ch in ")]}":
            if ch != closer:
                raise ValueError(f"unbalanced '{ch}' in {s!r}")
            return counts, i + 1
        elif ch.isupper():
            j = i + 1
            while j < len(s) and s[j].islower():
                j += 1
            el = s[i:j]
            n, i = read_int(s, j)
            counts[el] = counts.get(el, 0) + n
        elif ch.isspace():
            i += 1
        else:
            raise ValueError(f"unexpected {ch!r} in formula {s!r}")
    if closer:
        raise ValueError(f"missing '{closer}' in {s!r}")
    return counts, i


def read_int(s: str, i: int) -> tuple[int, int]:
    j = i
    while j < len(s) and s[j].isdigit():
        j += 1
    return (int(s[i:j]) if j > i else 1), j


def parse_formula(raw: str) -> tuple[dict[str, int], int]:
    """Return ({element: count}, charge). Electrons -> ({}, -1)."""
    s = raw.strip()
    s = STATE_RE.sub("", s).strip()
    if s in ELECTRON_NAMES:
        return {}, -1
    body, charge = split_charge(s)
    total: dict[str, int] = {}
    for part in re.split(r"[*·•]", body):
        part = part.strip()
        if not part:
            continue
        mult, k = read_int(part, 0)
        comp, _ = parse_group(part[k:])
        for el, n in comp.items():
            total[el] = total.get(el, 0) + n * mult
    for el in total:
        if not _element(el):
            raise ValueError(f"unknown element symbol {el!r} in {raw!r}")
    return total, charge


# ----------------------------------------------------------------- element data

_PT = None


def _pt():
    global _PT
    if _PT is None:
        try:
            import periodictable
        except ImportError:
            sys.exit("periodictable is required: py -3.11 -m pip install periodictable")
        _PT = periodictable
    return _PT


def _element(sym: str):
    pt = _pt()
    try:
        el = getattr(pt, sym)
        return el if getattr(el, "number", 0) > 0 else None
    except AttributeError:
        return None


def element_from_token(tok: str):
    if tok.isdigit():
        return _pt().elements[int(tok)]
    el = _element(tok)
    if el is None:
        raise ValueError(f"unknown element {tok!r}")
    return el


# ----------------------------------------------------------------- molar mass

def cmd_molar_mass(args):
    for f in args.formulas:
        comp, q = parse_formula(f)
        total = 0.0
        rows = []
        for el, n in comp.items():
            m = _element(el).mass
            if args.digits is not None:
                m = round(m, args.digits)
            total += n * m
            rows.append(f"    {el:<3} {n:>3} x {m:<10.5g} = {n * m:.4f}")
        charge = f" (charge {q:+d}; electron mass neglected)" if q else ""
        print(f"{f}: {total:.4f} g/mol{charge}")
        print("\n".join(rows))


# ----------------------------------------------------------------- equations

ARROW_RE = re.compile(r"\s*(?:<=>|<->|⇌|⇄|->|→|⟶|=)\s*")
COEF_RE = re.compile(r"^\s*(\d+(?:\.\d+)?(?:/\d+)?)\s*(?=[A-Z(\[e])")


def split_species(side: str) -> list[tuple[Fraction | None, str]]:
    out = []
    for term in re.split(r"\s+\+\s+", side.strip()):
        term = term.strip()
        if not term:
            continue
        m = COEF_RE.match(term)
        coef = None
        if m:
            coef = Fraction(m.group(1)) if "/" in m.group(1) else Fraction(m.group(1)).limit_denominator(1000)
            term = term[m.end():].strip()
        out.append((coef, term))
    return out


def parse_equation(eq: str):
    parts = ARROW_RE.split(eq)
    if len(parts) != 2:
        raise ValueError("equation needs exactly one arrow (->, →, =, <=>, ⇌)")
    return split_species(parts[0]), split_species(parts[1])


def balance_matrix(react, prod):
    species = [s for _, s in react] + [s for _, s in prod]
    parsed = [parse_formula(s) for s in species]
    elements = sorted({el for comp, _ in parsed for el in comp})
    rows = []
    for el in elements:
        rows.append([comp.get(el, 0) * (1 if i < len(react) else -1)
                     for i, (comp, _) in enumerate(parsed)])
    if any(q for _, q in parsed):
        rows.append([q * (1 if i < len(react) else -1) for i, (_, q) in enumerate(parsed)])
        elements.append("charge")
    return species, elements, rows, parsed


def cmd_balance(args):
    import sympy
    react, prod = parse_equation(args.equation)
    species, labels, rows, _ = balance_matrix(react, prod)
    ns = sympy.Matrix(rows).nullspace()
    if not ns:
        print("No non-trivial solution: check formulas (a species may be wrong or missing).")
        return
    if len(ns) > 1:
        print(f"{len(ns)} independent solutions: the equation is a combination of separate "
              "reactions; balancing is not unique. Basis vectors:")
    for v in ns:
        lcm = sympy.ilcm(*[term.q for term in v])
        vec = [int(x * lcm) for x in v]
        if all(x <= 0 for x in vec):
            vec = [-x for x in vec]
        g = math.gcd(*vec)
        vec = [x // g for x in vec]
        if any(x <= 0 for x in vec):
            print("  (a coefficient is zero or negative: some species is on the wrong side or unnecessary)")
        n = len(react)
        fmt = lambda cs, ss: " + ".join((f"{c} " if c != 1 else "") + s for c, s in zip(cs, ss))
        print("  " + fmt(vec[:n], species[:n]) + " -> " + fmt(vec[n:], species[n:]))
    print("Checked:", ", ".join(labels))


def cmd_check(args):
    react, prod = parse_equation(args.equation)
    ok = True
    totals: dict[str, list[Fraction]] = {}
    for side_idx, side in enumerate((react, prod)):
        for coef, sp in side:
            c = coef if coef is not None else Fraction(1)
            comp, q = parse_formula(sp)
            for el, n in comp.items():
                totals.setdefault(el, [Fraction(0), Fraction(0)])[side_idx] += c * n
            totals.setdefault("charge", [Fraction(0), Fraction(0)])[side_idx] += c * q
    for k, (l, r) in totals.items():
        status = "ok" if l == r else "UNBALANCED"
        ok &= l == r
        if k == "charge" and l == 0 and r == 0:
            continue
        print(f"  {k:<7} left {str(l):>6}   right {str(r):>6}   {status}")
    coefs = [c for c, _ in react + prod if c is not None]
    if any(c.denominator != 1 for c in coefs):
        print("  note: fractional coefficients (acceptable for per-mole thermochemical equations only)")
    print("BALANCED" if ok else "NOT BALANCED")


def cmd_electrons(args):
    for f in args.formulas:
        comp, q = parse_formula(f)
        total = sum(_element(el).number * n for el, n in comp.items()) - q
        valence = 0
        known = True
        for el, n in comp.items():
            v = main_group_valence(_element(el).number)
            if v is None:
                known = False
            else:
                valence += v * n
        vtxt = f"{valence - q} valence e- (for Lewis structures)" if known else \
            "valence count skipped (transition metal present)"
        print(f"{f}: {total} total electrons; {vtxt}")


def main_group_valence(z: int) -> int | None:
    if z <= 2:
        return z
    periods = [2, 10, 18, 36, 54, 86, 118]
    prev = max(p for p in periods if p < z)
    offset = z - prev
    if prev in (2, 10):
        return offset
    # periods 4+: groups 1-2, then 10 d-block, (14 f-block for 6+), then p-block
    fblock = 14 if prev >= 54 else 0
    if offset <= 2:
        return offset
    d_start = 3 + fblock
    if offset < d_start + 10 and offset >= d_start:
        return None
    if offset < d_start:
        return None  # f-block
    return offset - 10 - fblock


# ----------------------------------------------------------------- electron configuration

L_LETTER = "spdf"
MADELUNG = sorted(((n, l) for n in range(1, 8) for l in range(0, 4) if l < n),
                  key=lambda nl: (nl[0] + nl[1], nl[0]))
CAPACITY = {l: 2 * (2 * l + 1) for l in range(4)}
# Ground-state exceptions (neutral atoms), given as overrides of the Aufbau result.
EXCEPTIONS = {
    24: {(4, 0): 1, (3, 2): 5},   # Cr
    29: {(4, 0): 1, (3, 2): 10},  # Cu
    41: {(5, 0): 1, (4, 2): 4},   # Nb
    42: {(5, 0): 1, (4, 2): 5},   # Mo
    44: {(5, 0): 1, (4, 2): 7},   # Ru
    45: {(5, 0): 1, (4, 2): 8},   # Rh
    46: {(5, 0): 0, (4, 2): 10},  # Pd
    47: {(5, 0): 1, (4, 2): 10},  # Ag
    57: {(4, 3): 0, (5, 2): 1},   # La
    58: {(4, 3): 1, (5, 2): 1},   # Ce
    64: {(4, 3): 7, (5, 2): 1},   # Gd
    78: {(6, 0): 1, (5, 2): 9},   # Pt
    79: {(6, 0): 1, (5, 2): 10},  # Au
    89: {(5, 3): 0, (6, 2): 1},   # Ac
    90: {(5, 3): 0, (6, 2): 2},   # Th
    91: {(5, 3): 2, (6, 2): 1},   # Pa
    92: {(5, 3): 3, (6, 2): 1},   # U
    93: {(5, 3): 4, (6, 2): 1},   # Np
    96: {(5, 3): 7, (6, 2): 1},   # Cm
}
NOBLE = [(86, "Rn"), (54, "Xe"), (36, "Kr"), (18, "Ar"), (10, "Ne"), (2, "He")]


def aufbau(n_electrons: int) -> dict[tuple[int, int], int]:
    conf, left = {}, n_electrons
    for nl in MADELUNG:
        if left <= 0:
            break
        take = min(CAPACITY[nl[1]], left)
        conf[nl] = take
        left -= take
    return conf


def neutral_config(z: int) -> dict[tuple[int, int], int]:
    conf = aufbau(z)
    if z in EXCEPTIONS:
        conf.update(EXCEPTIONS[z])
    return {k: v for k, v in conf.items() if v}


def ion_config(z: int, charge: int) -> dict[tuple[int, int], int]:
    conf = neutral_config(z)
    if charge > 0:
        for _ in range(charge):
            # remove from highest n, then highest l (e.g. 4s before 3d; 5p before 5s)
            key = max((k for k, v in conf.items() if v), key=lambda nl: (nl[0], nl[1]))
            conf[key] -= 1
            if conf[key] == 0:
                del conf[key]
    elif charge < 0:
        conf = aufbau(z - charge) if z not in EXCEPTIONS else _add(conf, -charge)
    return conf


def _add(conf, k):
    conf = dict(conf)
    for _ in range(k):
        for nl in MADELUNG:
            if conf.get(nl, 0) < CAPACITY[nl[1]]:
                conf[nl] = conf.get(nl, 0) + 1
                break
    return conf


def unpaired(conf) -> int:
    total = 0
    for (n, l), e in conf.items():
        orbitals = 2 * l + 1
        total += e if e <= orbitals else 2 * orbitals - e
    return total


def fmt_conf(conf, order: str) -> str:
    keys = sorted(conf, key=(lambda nl: (nl[0], nl[1])) if order == "n" else MADELUNG.index)
    return " ".join(f"{n}{L_LETTER[l]}{conf[(n, l)]}" for n, l in keys)


def noble_core(conf) -> tuple[str, dict]:
    for z, sym in NOBLE:
        core = aufbau(z)
        if all(conf.get(k, 0) == v for k, v in core.items()):
            return f"[{sym}]", {k: v for k, v in conf.items() if k not in core}
    return "", conf


def cmd_config(args):
    for tok in args.species:
        base, q = split_charge(tok)
        el = element_from_token(base)
        conf = ion_config(el.number, q)
        core, rest = noble_core(conf)
        n_e = sum(conf.values())
        up = unpaired(conf)
        label = el.symbol + (f"^{abs(q) if abs(q) > 1 else ''}{'+' if q > 0 else '-'}" if q else "")
        print(f"{label} (Z={el.number}, {n_e} e-)")
        print(f"   full, filling order : {fmt_conf(conf, 'fill')}")
        print(f"   noble gas, by n     : {core} {fmt_conf(rest, 'n')}".rstrip())
        print(f"   noble gas, fill ord : {core} {fmt_conf(rest, 'fill')}".rstrip())
        print(f"   unpaired e-: {up} -> {'paramagnetic' if up else 'diamagnetic'}")
        if q == 0 and el.number in EXCEPTIONS:
            print("   note: ground-state EXCEPTION to simple Aufbau order")
        if q > 0 and any(l == 2 for (_, l) in neutral_config(el.number)):
            print("   note: cation electrons removed from highest n first (ns before (n-1)d)")


def cmd_qn(args):
    n, l, ml = int(args.n), int(args.l), int(args.ml)
    ms = Fraction(args.ms) if args.ms is not None else None
    problems = []
    if n < 1:
        problems.append("n must be a positive integer")
    if not 0 <= l <= n - 1:
        problems.append(f"l must be 0..n-1 (0..{n - 1})")
    if not -l <= ml <= l:
        problems.append(f"ml must be -l..+l ({-l}..{l})")
    if ms is not None and ms not in (Fraction(1, 2), Fraction(-1, 2)):
        problems.append("ms must be +1/2 or -1/2")
    if problems:
        print("INVALID: " + "; ".join(problems))
    else:
        sub = f"{n}{L_LETTER[l]}" if l < 4 else f"n={n}, l={l}"
        print(f"VALID: electron in a {sub} orbital; {2 * l + 1} orbitals in this subshell, "
              f"{n * n} orbitals in shell n={n}")


# ----------------------------------------------------------------- significant figures

def count_sigfigs(s: str) -> tuple[int, int | None, str]:
    """Return (min_count, max_count_or_None, note)."""
    t = s.strip().replace(",", "").lstrip("+-")
    m = re.fullmatch(r"(\d*\.?\d*)(?:[eE]([+-]?\d+)|\s*[x×]\s*10\^?\(?([+-]?\d+)\)?)?", t)
    if not m or not m.group(1) or m.group(1) == ".":
        raise ValueError(f"cannot parse number {s!r}")
    mant = m.group(1)
    digits = mant.replace(".", "")
    stripped = digits.lstrip("0")
    if not stripped:
        return (1 if "." not in mant else max(1, len(mant.split(".")[1])), None,
                "zero: sig figs follow decimal places")
    if "." in mant:
        return len(stripped), None, ""
    trailing = len(stripped) - len(stripped.rstrip("0"))
    if trailing:
        return len(stripped) - trailing, len(stripped), \
            "AMBIGUOUS trailing zeros without decimal point; write in scientific notation"
    return len(stripped), None, ""


def cmd_sigfigs(args):
    for s in args.values:
        lo, hi, note = count_sigfigs(s)
        rng = f"{lo}" if hi is None else f"{lo} to {hi}"
        print(f"{s}: {rng} sig figs" + (f"  ({note})" if note else ""))
    print("\nRules: x/÷ -> fewest sig figs; +/- -> fewest decimal places; "
          "log(x) -> decimal places = sig figs of x; 10^x -> sig figs = decimal places of x; "
          "exact counts and defined conversions do not limit.")


def round_sig(x: float, n: int) -> str:
    if x == 0:
        return "0." + "0" * (n - 1) if n > 1 else "0"
    exp = math.floor(math.log10(abs(x)))
    return f"{x:.{n - 1}e}" if (exp < -3 or exp >= n + 2) else f"{round(x, n - 1 - exp):.{max(n - 1 - exp, 0)}f}"


def cmd_round(args):
    x = float(args.value)
    n = args.n
    print(f"{args.value} -> {n} sig figs: {round_sig(x, n)}   (sci: {x:.{n - 1}e})")
    if abs(x) >= 10 ** n and float(x).is_integer():
        print("  note: write in scientific notation to show the sig figs unambiguously")


# ----------------------------------------------------------------- units

def cmd_units(args):
    try:
        import pint
    except ImportError:
        sys.exit("pint is required: py -3.11 -m pip install pint")
    u = pint.UnitRegistry()
    expr = args.expression.replace("×", "*").replace("·", "*")
    q = u.parse_expression(expr)
    if args.to:
        q = q.to(args.to)
    if hasattr(q, "magnitude"):
        print(f"{q.magnitude:.6g} {q.units:~P}")
        print(f"dimensionality: {q.dimensionality}")
        if args.to is None and not q.dimensionless:
            print(f"SI base: {q.to_base_units():.6g~P}")
    else:
        print(q)


# ----------------------------------------------------------------- equilibria

def cmd_quadratic(args):
    a, b, c = args.a, args.b, args.c
    disc = b * b - 4 * a * c
    print(f"discriminant = {disc:.6g}")
    if disc < 0:
        print("no real roots")
        return
    r1 = (-b + math.sqrt(disc)) / (2 * a)
    r2 = (-b - math.sqrt(disc)) / (2 * a)
    print(f"roots: {r1:.6g}, {r2:.6g}")
    print("Choose the root that keeps every ICE-table concentration non-negative; "
          "reject the other and say why.")


def cmd_weak_acid(args):
    K, C = args.K, args.C
    kind = "base" if args.base else "acid"
    x = (-K + math.sqrt(K * K + 4 * K * C)) / 2
    x_approx = math.sqrt(K * C)
    pct = 100 * x / C
    pct_approx = 100 * x_approx / C
    p = -math.log10(x)
    p_approx = -math.log10(x_approx)
    ion = "OH-" if args.base else "H3O+"
    print(f"weak {kind}: K = {K:g}, C = {C:g} M   (water autoionization neglected)")
    print(f"  exact  [{ion}] = {x:.4g} M   p{'OH' if args.base else 'H'} = {p:.3f}")
    print(f"  approx [{ion}] = {x_approx:.4g} M   p{'OH' if args.base else 'H'} = {p_approx:.3f}   "
          f"(x << C assumption)")
    print(f"  % ionization: exact {pct:.3g}%, approx {pct_approx:.3g}%  -> "
          f"5% rule {'PASSES' if pct_approx < 5 else 'FAILS: use the quadratic'}")
    if args.base:
        print(f"  pH (25 °C) = 14.00 - pOH = {14 - p:.3f} (exact), {14 - p_approx:.3f} (approx)")
    if x < 1e-6:
        print("  warning: [ion] near 1e-7 M; water's contribution is no longer negligible")


def cmd_linfit(args):
    xs = args.x
    ys = args.y
    if len(xs) != len(ys) or len(xs) < 2:
        sys.exit("need matching --x and --y lists with at least 2 points")
    tf = {"none": lambda v: v, "ln": math.log, "log": math.log10, "inv": lambda v: 1 / v}
    ylab = {"none": "y", "ln": "ln(y)", "log": "log10(y)", "inv": "1/y"}[args.ty]
    xlab = {"none": "x", "ln": "ln(x)", "log": "log10(x)", "inv": "1/x"}[args.tx]
    X = [tf[args.tx](v) for v in xs]
    Y = [tf[args.ty](v) for v in ys]
    n = len(X)
    mx, my = sum(X) / n, sum(Y) / n
    sxx = sum((x - mx) ** 2 for x in X)
    sxy = sum((x - mx) * (y - my) for x, y in zip(X, Y))
    syy = sum((y - my) ** 2 for y in Y)
    slope = sxy / sxx
    icpt = my - slope * mx
    r2 = (sxy * sxy) / (sxx * syy) if syy else 1.0
    print(f"{ylab} = {slope:.6g} * {xlab} + {icpt:.6g}    R^2 = {r2:.6f}")
    if args.ty == "ln" and args.tx == "none":
        print(f"  first-order check: k = -slope = {-slope:.6g}; [A]0 = e^intercept = {math.exp(icpt):.6g}")
    if args.ty == "inv" and args.tx == "none":
        print(f"  second-order check: k = slope = {slope:.6g}; [A]0 = 1/intercept = {1 / icpt:.6g}")
    if args.ty == "ln" and args.tx == "inv":
        print(f"  Arrhenius / Clausius-Clapeyron check: slope = -Ea/R (or -ΔHvap/R) -> "
              f"{-slope * 8.314:.6g} J/mol")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("molar-mass"); s.add_argument("formulas", nargs="+")
    s.add_argument("--digits", type=int, help="round atomic masses (to mimic a course table)")
    s.set_defaults(func=cmd_molar_mass)
    s = sub.add_parser("balance"); s.add_argument("equation"); s.set_defaults(func=cmd_balance)
    s = sub.add_parser("check"); s.add_argument("equation"); s.set_defaults(func=cmd_check)
    s = sub.add_parser("electrons"); s.add_argument("formulas", nargs="+"); s.set_defaults(func=cmd_electrons)
    s = sub.add_parser("config"); s.add_argument("species", nargs="+"); s.set_defaults(func=cmd_config)
    s = sub.add_parser("qn"); s.add_argument("n"); s.add_argument("l"); s.add_argument("ml")
    s.add_argument("ms", nargs="?"); s.set_defaults(func=cmd_qn)
    s = sub.add_parser("sigfigs"); s.add_argument("values", nargs="+"); s.set_defaults(func=cmd_sigfigs)
    s = sub.add_parser("round"); s.add_argument("value"); s.add_argument("n", type=int); s.set_defaults(func=cmd_round)
    s = sub.add_parser("units"); s.add_argument("expression"); s.add_argument("--to")
    s.set_defaults(func=cmd_units)
    s = sub.add_parser("quadratic"); s.add_argument("a", type=float); s.add_argument("b", type=float)
    s.add_argument("c", type=float); s.set_defaults(func=cmd_quadratic)
    s = sub.add_parser("weak-acid"); s.add_argument("--K", type=float, required=True)
    s.add_argument("--C", type=float, required=True); s.add_argument("--base", action="store_true")
    s.set_defaults(func=cmd_weak_acid)
    s = sub.add_parser("linfit"); s.add_argument("--x", type=float, nargs="+", required=True)
    s.add_argument("--y", type=float, nargs="+", required=True)
    s.add_argument("--tx", choices=["none", "ln", "log", "inv"], default="none")
    s.add_argument("--ty", choices=["none", "ln", "log", "inv"], default="none")
    s.set_defaults(func=cmd_linfit)

    argv = sys.argv[1:]
    if argv[:1] == ["quadratic"] and "--" not in argv:
        argv.insert(1, "--")  # allow negative coefficients like -1.8e-6
    args = ap.parse_args(argv)
    try:
        args.func(args)
    except ValueError as e:
        sys.exit(f"error: {e}")


if __name__ == "__main__":
    main()

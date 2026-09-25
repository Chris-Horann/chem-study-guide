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
    py -3.11 tools/chemistry_verify.py weak-acid --K 1.8e-5 --C 0.10 [--base]
    py -3.11 tools/chemistry_verify.py quadratic 1 1.8e-5 -1.8e-6
    py -3.11 tools/chemistry_verify.py linfit --x 0 10 20 30 --y 1.0 0.61 0.37 0.22 --ty ln

Formula syntax: charges use ^ ("SO4^2-", "Fe^3+", "[Fe(CN)6]^4-"); hydrates use
* or · ("CuSO4*5H2O"); physical states "(s) (l) (g) (aq)" are ignored; electrons
are "e^-" or "e-". Equations: species separated by " + " (spaces required),
arrows ->, →, =, <=>, ⇌. Coefficients may be integers, decimals, or fractions.

These are checks, not explanations. Reason chemically first, then confirm here.
Atomic weights come from the `periodictable` package (IUPAC standard values). If
the course periodic table uses rounded values, use --digits or compare against
the course table and report the difference.

The functions (parse_formula, molar_mass, ion_config, count_sigfigs, ...) can also
be imported in Python/Jupyter: sys.path.insert(0, "tools"); import chemistry_verify as cv
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
ELECTRON_NAMES = {"e", "e-", "e^-", "e^{-}"}


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


def read_int(s: str, i: int) -> tuple[int, int]:
    j = i
    while j < len(s) and s[j].isdigit():
        j += 1
    return (int(s[i:j]) if j > i else 1), j


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


def parse_formula(raw: str) -> tuple[dict[str, int], int]:
    """Return ({element: count}, charge). Electrons -> ({}, -1)."""
    s = STATE_RE.sub("", raw.strip()).strip()
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
    try:
        el = getattr(_pt(), sym)
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

def molar_mass(formula: str, digits: int | None = None) -> float:
    comp, _ = parse_formula(formula)
    mass = lambda el: round(_element(el).mass, digits) if digits is not None else _element(el).mass
    return sum(n * mass(el) for el, n in comp.items())


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
            coef = Fraction(m.group(1)).limit_denominator(1000)
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
    labels = sorted({el for comp, _ in parsed for el in comp})
    sign = lambda i: 1 if i < len(react) else -1
    rows = [[comp.get(el, 0) * sign(i) for i, (comp, _) in enumerate(parsed)] for el in labels]
    if any(q for _, q in parsed):
        rows.append([q * sign(i) for i, (_, q) in enumerate(parsed)])
        labels.append("charge")
    return species, labels, rows


def chempy_crosscheck(react, prod):
    """Second, independent balance via ChemPy (neutral species only)."""
    try:
        from chempy import balance_stoichiometry
    except ImportError:
        return None
    if any(parse_formula(s)[1] for _, s in react + prod):
        return None  # ChemPy's charge syntax differs; skip ionic equations
    clean = lambda s: STATE_RE.sub("", s).strip()
    try:
        r, p = balance_stoichiometry({clean(s) for _, s in react}, {clean(s) for _, s in prod})
        return {**{k: int(v) for k, v in r.items()}, **{k: int(v) for k, v in p.items()}}
    except Exception as e:  # ChemPy raises on underdetermined systems
        return f"ChemPy could not balance: {e}"


def cmd_balance(args):
    import sympy
    react, prod = parse_equation(args.equation)
    species, labels, rows = balance_matrix(react, prod)
    ns = sympy.Matrix(rows).nullspace()
    if not ns:
        print("No non-trivial solution: check formulas (a species may be wrong or missing).")
        return
    if len(ns) > 1:
        print(f"{len(ns)} independent solutions: the equation combines separate reactions; "
              "balancing is not unique. Basis vectors:")
    n = len(react)
    fmt = lambda cs, ss: " + ".join((f"{c} " if c != 1 else "") + s for c, s in zip(cs, ss))
    first = None
    for v in ns:
        lcm = sympy.ilcm(*[term.q for term in v])
        vec = [int(x * lcm) for x in v]
        if all(x <= 0 for x in vec):
            vec = [-x for x in vec]
        g = math.gcd(*vec)
        vec = [x // g for x in vec]
        first = first or vec
        if any(x <= 0 for x in vec):
            print("  (a coefficient is zero or negative: a species is on the wrong side or unnecessary)")
        print("  " + fmt(vec[:n], species[:n]) + " -> " + fmt(vec[n:], species[n:]))
    print("Checked:", ", ".join(labels))
    if len(ns) == 1:
        cc = chempy_crosscheck(react, prod)
        if isinstance(cc, dict):
            mine = {STATE_RE.sub("", s).strip(): c for s, c in zip(species, first)}
            print("ChemPy cross-check:", "AGREES" if cc == mine else f"DISAGREES {cc}")
        elif isinstance(cc, str):
            print(cc)


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
        ok &= l == r
        if k == "charge" and l == 0 and r == 0:
            continue
        print(f"  {k:<7} left {str(l):>6}   right {str(r):>6}   {'ok' if l == r else 'UNBALANCED'}")
    if any(c.denominator != 1 for c, _ in react + prod if c is not None):
        print("  note: fractional coefficients (acceptable for per-mole thermochemical equations only)")
    print("BALANCED" if ok else "NOT BALANCED")


def main_group_valence(z: int) -> int | None:
    """Valence electrons for main-group elements; None for d/f-block."""
    if z <= 2:
        return z
    prev = max(p for p in [2, 10, 18, 36, 54, 86, 118] if p < z)
    offset = z - prev
    if prev in (2, 10) or offset <= 2:
        return offset
    fblock = 14 if prev >= 54 else 0
    if offset < 3 + fblock + 10:
        return None
    return offset - 10 - fblock


def cmd_electrons(args):
    for f in args.formulas:
        comp, q = parse_formula(f)
        total = sum(_element(el).number * n for el, n in comp.items()) - q
        vals = [main_group_valence(_element(el).number) for el in comp]
        if None in vals:
            vtxt = "valence count skipped (transition/inner-transition metal present)"
        else:
            valence = sum(v * n for v, n in zip(vals, comp.values())) - q
            vtxt = f"{valence} valence e- (for Lewis structures)"
        print(f"{f}: {total} total electrons; {vtxt}")


# ----------------------------------------------------------------- electron configuration

L_LETTER = "spdf"
MADELUNG = sorted(((n, l) for n in range(1, 8) for l in range(0, 4) if l < n),
                  key=lambda nl: (nl[0] + nl[1], nl[0]))
CAPACITY = {l: 2 * (2 * l + 1) for l in range(4)}
# Ground-state exceptions (neutral atoms), as overrides of the Aufbau result.
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
    conf.update(EXCEPTIONS.get(z, {}))
    return {k: v for k, v in conf.items() if v}


def ion_config(z: int, charge: int) -> dict[tuple[int, int], int]:
    conf = neutral_config(z)
    if charge > 0:
        for _ in range(charge):
            # remove from highest n, then highest l (4s before 3d; 5p before 5s)
            key = max(conf, key=lambda nl: (nl[0], nl[1]))
            conf[key] -= 1
            if conf[key] == 0:
                del conf[key]
    elif charge < 0:
        for _ in range(-charge):
            nl = next(nl for nl in MADELUNG if conf.get(nl, 0) < CAPACITY[nl[1]])
            conf[nl] = conf.get(nl, 0) + 1
    return conf


def unpaired(conf) -> int:
    """Hund's rule count for the free atom/ion (high-spin)."""
    return sum(e if e <= 2 * l + 1 else 2 * (2 * l + 1) - e for (_, l), e in conf.items())


def fmt_conf(conf, order: str) -> str:
    keys = sorted(conf, key=(lambda nl: nl) if order == "n" else MADELUNG.index)
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
        up = unpaired(conf)
        label = el.symbol + (f"^{abs(q) if abs(q) > 1 else ''}{'+' if q > 0 else '-'}" if q else "")
        print(f"{label} (Z={el.number}, {sum(conf.values())} e-)")
        print(f"   full, filling order : {fmt_conf(conf, 'fill')}")
        print(f"   noble gas, by n     : {core} {fmt_conf(rest, 'n')}".rstrip())
        print(f"   noble gas, fill ord : {core} {fmt_conf(rest, 'fill')}".rstrip())
        print(f"   unpaired e-: {up} -> {'paramagnetic' if up else 'diamagnetic'}")
        if q == 0 and el.number in EXCEPTIONS:
            print("   note: ground-state EXCEPTION to simple Aufbau order")
        if q > 0 and any(l == 2 for (_, l) in neutral_config(el.number)):
            print("   note: cation electrons removed from highest n first (ns before (n-1)d)")
    print("\nOrdering convention (by n vs. filling order) must follow COURSE.md.")


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
    stripped = mant.replace(".", "").lstrip("0")
    if not stripped:
        return (max(1, len(mant.split(".")[1])) if "." in mant else 1), None, \
            "zero: sig figs follow decimal places"
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
        print(f"{s}: {lo if hi is None else f'{lo} to {hi}'} sig figs" + (f"  ({note})" if note else ""))
    print("\nRules: x/÷ -> fewest sig figs; +/- -> fewest decimal places; "
          "log(x) -> decimal places = sig figs of x; 10^x -> sig figs = decimal places of x; "
          "exact counts and defined conversions do not limit. Course policy: see COURSE.md.")


def round_sig(x: float, n: int) -> str:
    if x == 0:
        return "0." + "0" * (n - 1) if n > 1 else "0"
    exp = math.floor(math.log10(abs(x)))
    if exp < -3 or exp >= n + 2:
        return f"{x:.{n - 1}e}"
    return f"{round(x, n - 1 - exp):.{max(n - 1 - exp, 0)}f}"


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
    q = u.parse_expression(args.expression.replace("×", "*").replace("·", "*"))
    if args.to:
        q = q.to(args.to)
    if hasattr(q, "magnitude"):
        print(f"{q.magnitude:.6g} {q.units:~P}")
        print(f"dimensionality: {q.dimensionality}")
        if args.to is None and not q.dimensionless:
            print(f"SI base: {q.to_base_units():.6g~P}")
    else:
        print(q)


# ----------------------------------------------------------------- equilibria / graphs

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
    x = (-K + math.sqrt(K * K + 4 * K * C)) / 2
    xa = math.sqrt(K * C)
    p, pa = -math.log10(x), -math.log10(xa)
    ion, pl = ("OH-", "pOH") if args.base else ("H3O+", "pH")
    print(f"weak {'base' if args.base else 'acid'}: K = {K:g}, C = {C:g} M   "
          "(water autoionization neglected)")
    print(f"  exact  [{ion}] = {x:.4g} M   {pl} = {p:.3f}")
    print(f"  approx [{ion}] = {xa:.4g} M   {pl} = {pa:.3f}   (x << C assumption)")
    print(f"  % ionization: exact {100 * x / C:.3g}%, approx {100 * xa / C:.3g}%  -> 5% rule "
          f"{'PASSES' if 100 * xa / C < 5 else 'FAILS: use the quadratic'}")
    if args.base:
        print(f"  pH (25 °C) = 14.00 - pOH = {14 - p:.3f} (exact), {14 - pa:.3f} (approx)")
    if x < 1e-6:
        print("  warning: [ion] near 1e-7 M; water's contribution is no longer negligible")


def cmd_linfit(args):
    xs, ys = args.x, args.y
    if len(xs) != len(ys) or len(xs) < 2:
        sys.exit("need matching --x and --y lists with at least 2 points")
    tf = {"none": lambda v: v, "ln": math.log, "log": math.log10, "inv": lambda v: 1 / v}
    name = {"none": "{}", "ln": "ln({})", "log": "log10({})", "inv": "1/{}"}
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
    print(f"{name[args.ty].format('y')} = {slope:.6g} * {name[args.tx].format('x')} + {icpt:.6g}"
          f"    R^2 = {r2:.6f}")
    if args.ty == "ln" and args.tx == "none":
        print(f"  first-order: k = -slope = {-slope:.6g}; [A]0 = e^intercept = {math.exp(icpt):.6g}")
    if args.ty == "inv" and args.tx == "none":
        print(f"  second-order: k = slope = {slope:.6g}; [A]0 = 1/intercept = {1 / icpt:.6g}")
    if args.ty == "ln" and args.tx == "inv":
        print(f"  Arrhenius / Clausius-Clapeyron: slope = -Ea/R -> Ea = {-slope * 8.314:.6g} J/mol")


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
    s = sub.add_parser("round"); s.add_argument("value"); s.add_argument("n", type=int)
    s.set_defaults(func=cmd_round)
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

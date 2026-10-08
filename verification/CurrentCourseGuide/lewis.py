"""Lewis structures for the CurrentCourseGuide Ch. 4 modules: definitions, checks, and SVG rendering.

Every structure the guide draws is defined here once. `check()` verifies the electron total against the
formula, octets (H: 2), and formal charges (FC = valence e⁻ − [lone-pair e⁻ + ½ shared e⁻], textbook
Eq. 4.2, TB PDF p.209); `rdkit_check()` rebuilds the structure in RDKit as an independent test of
connectivity, formula, and charge. `svg()` renders a structure the way the slides and textbook draw
them: element symbols, lines for bonds, dot pairs on the free sides, brackets and charge for ions.

    py -3.11 verification/CurrentCourseGuide/lewis.py      # checks every structure, prints a table
"""
import math

VALENCE = {"H": 1, "He": 2, "Li": 1, "Be": 2, "B": 3, "C": 4, "N": 5, "O": 6, "F": 7, "Ne": 8,
           "Na": 1, "Mg": 2, "Al": 3, "Si": 4, "P": 5, "S": 6, "Cl": 7, "Ar": 8, "K": 1, "Ca": 2,
           "As": 5, "Se": 6, "Br": 7, "Kr": 8, "I": 7, "Xe": 8,
           "Ga": 3, "Ge": 4, "In": 3, "Sb": 5}      # Ga-Sb: Lewis symbols only (the dopants of Day 12 p.25 and m25)
MINUS = "−"
UNIT = 46                       # px per unit of bond length
RDKIT_NO_VALENCE = {"BrF5", "ClF3", "BrF3"}   # hypervalent halogens: RDKit valence check skipped (see rdkit_check)


def sup_charge(q):
    """Charge as magnitude then sign: 1 -> '+', -2 -> '2−'."""
    if not q:
        return ""
    a = abs(q)
    return ("" if a == 1 else str(a)) + ("+" if q > 0 else MINUS)


def fc_text(v):
    return "0" if v == 0 else ("+" if v > 0 else MINUS) + str(abs(v))


class Structure:
    def __init__(self, sid, name, formula_html, atoms, bonds, lp=None, rad=None, charge=0, central=None,
                 note="", source=""):
        self.id, self.name, self.formula_html = sid, name, formula_html
        self.atoms = [(a[0], float(a[1]), float(a[2])) for a in atoms]      # (symbol, x, y) in units; y down
        self.bonds = [tuple(b) for b in bonds]                               # (i, j, order)
        self.lp = dict(lp or {})                                             # atom -> lone pairs
        self.rad = dict(rad or {})                                           # atom -> unpaired electrons
        self.charge = charge
        self.central = list(central) if central is not None else self._guess_central()
        self.note, self.source = note, source

    # ------------------------------------------------------------ bookkeeping
    def _guess_central(self):
        deg = [0] * len(self.atoms)
        for i, j, _ in self.bonds:
            deg[i] += 1
            deg[j] += 1
        return [k for k, d in enumerate(deg) if d > 1]

    def bond_orders(self, k):
        return sum(o for i, j, o in self.bonds if k in (i, j))

    def total_valence(self):
        return sum(VALENCE[a[0]] for a in self.atoms) - self.charge

    def drawn_electrons(self):
        return 2 * sum(o for _, _, o in self.bonds) + 2 * sum(self.lp.values()) + sum(self.rad.values())

    def shell(self, k):
        return 2 * self.bond_orders(k) + 2 * self.lp.get(k, 0) + self.rad.get(k, 0)

    def fc(self, k):
        return VALENCE[self.atoms[k][0]] - (2 * self.lp.get(k, 0) + self.rad.get(k, 0) + self.bond_orders(k))

    def fcs(self):
        return [self.fc(k) for k in range(len(self.atoms))]

    def formula_counts(self):
        out = {}
        for a in self.atoms:
            out[a[0]] = out.get(a[0], 0) + 1
        return out

    def check(self, expect_octets=True):
        errs = []
        if self.drawn_electrons() != self.total_valence():
            errs.append(f"{self.id}: drawn {self.drawn_electrons()} e⁻ vs. {self.total_valence()} valence e⁻")
        if sum(self.fcs()) != self.charge:
            errs.append(f"{self.id}: formal charges sum to {sum(self.fcs())}, charge is {self.charge}")
        if expect_octets:
            for k, a in enumerate(self.atoms):
                want = 2 if a[0] == "H" else 8
                if self.shell(k) != want:
                    errs.append(f"{self.id}: {a[0]}{k} has {self.shell(k)} e⁻ (want {want})")
        return errs

    def rdkit_check(self):
        """Rebuild in RDKit with our formal charges and radicals; return (smiles, formula, charge) or raise."""
        from rdkit import Chem
        from rdkit.Chem.rdMolDescriptors import CalcMolFormula
        m = Chem.RWMol()
        for k, a in enumerate(self.atoms):
            at = Chem.Atom(a[0])
            at.SetFormalCharge(self.fc(k))
            at.SetNoImplicit(True)
            at.SetNumRadicalElectrons(self.rad.get(k, 0))
            m.AddAtom(at)
        types = {1: Chem.BondType.SINGLE, 2: Chem.BondType.DOUBLE, 3: Chem.BondType.TRIPLE}
        for i, j, o in self.bonds:
            m.AddBond(i, j, types[o])
        mol = m.GetMol()
        if self.id in RDKIT_NO_VALENCE:
            # RDKit's default valence table has no Br(V); skip only its valence check (electron count,
            # octet/expanded-octet count, and formal charges are still checked in check())
            Chem.SanitizeMol(mol, Chem.SanitizeFlags.SANITIZE_ALL ^ Chem.SanitizeFlags.SANITIZE_PROPERTIES)
        else:
            Chem.SanitizeMol(mol)
        return Chem.MolToSmiles(mol), CalcMolFormula(mol), Chem.GetFormalCharge(mol)

    def copy(self, **kw):
        s = Structure(self.id, self.name, self.formula_html, self.atoms, self.bonds, self.lp, self.rad,
                      self.charge, self.central, self.note, self.source)
        for k, v in kw.items():
            setattr(s, k, v)
        return s


# ================================================================ the five steps (Day 8 p.21)
def five_steps(final):
    """Intermediate structures for steps 2-5, generated from the final structure.
    Step 2: skeleton with single bonds. Step 3: lone pairs completing the octets of outer atoms (H: none).
    Step 4: leftover electrons as lone pairs on the central atom(s). Step 5: the final structure (lone pairs
    turned into multiple bonds where a central atom was short). Returns [(label, Structure, info)]."""
    skel = final.copy(bonds=[(i, j, 1) for i, j, _ in final.bonds], lp={}, rad={})
    outer = [k for k in range(len(final.atoms)) if k not in final.central]
    lp3 = {}
    for k in outer:
        if final.atoms[k][0] != "H":
            need = 8 - skel.shell(k)
            if need > 0:
                lp3[k] = need // 2
    s3 = skel.copy(lp=lp3)
    total = final.total_valence()
    left = total - s3.drawn_electrons()
    lp4, rad4 = dict(lp3), {}
    cen = list(final.central) or [0]
    k = 0
    while left >= 2:                       # spread leftover pairs over the central atoms
        c = cen[k % len(cen)]
        lp4[c] = lp4.get(c, 0) + 1
        left -= 2
        k += 1
    if left == 1:
        rad4[cen[0]] = 1
    s4 = skel.copy(lp=lp4, rad=rad4)
    short = [c for c in final.central if final.atoms[c][0] != "H" and s4.shell(c) < 8]
    # Steps 4 and 5 on the slide: compare the count with step 1, then put leftover electrons on the central atom.
    # Sharing lone pairs as multiple bonds when a central atom is still short is not one of the five steps; the
    # slides show it in the O2, N2, ethyne, and ozone examples (Day 8 p.20, p.25, p.29-30).
    return [
        ("Step 2: skeleton with single bonds", skel, {"used": skel.drawn_electrons()}),
        ("Step 3: complete the outer atoms' octets", s3, {"used": s3.drawn_electrons()}),
        ("Steps 4–5: compare the count; leftover electrons go on the central atom", s4,
         {"used": s4.drawn_electrons(), "total": total, "short": short}),
        (("Finished: lone pairs shared to complete the octets" if short else "Finished structure"), final,
         {"used": final.drawn_electrons(), "same_as_previous": not short}),
    ]


# ================================================================ SVG rendering
def _angle(dx, dy):
    return math.degrees(math.atan2(-dy, dx)) % 360          # math convention: 0 = right, 90 = up


def _adist(a, b):
    d = abs(a - b) % 360
    return min(d, 360 - d)


def _lp_directions(s, k, n):
    x, y = s.atoms[k][1], s.atoms[k][2]
    used = []
    for i, j, _ in s.bonds:
        if k in (i, j):
            o = j if i == k else i
            used.append(_angle(s.atoms[o][1] - x, s.atoms[o][2] - y))
    chosen = []
    cands = list(range(0, 360, 15))
    for _ in range(n):
        best, bestv = None, -1
        for c in cands:
            ref = used + chosen
            v = min((_adist(c, r) for r in ref), default=360)
            v += 0.5 if c % 90 == 0 else 0                     # prefer the four sides of the symbol
            if v > bestv:
                best, bestv = c, v
        chosen.append(best)
    return chosen


def svg(s, show_fc=False, highlight=(), bracket=None, label=None, caption=None, pad=0.9, klass="lewis",
        fc_only_nonzero=False, scale=1.0, tag="figure"):
    """tag="figure" for a block drawing (caption as <figcaption>); tag="span" for phrasing contexts such as
    multiple-choice options inside a <label>."""
    bracket = (s.charge != 0) if bracket is None else bracket
    xs = [a[1] for a in s.atoms]
    ys = [a[2] for a in s.atoms]
    x0, x1, y0, y1 = min(xs) - pad, max(xs) + pad, min(ys) - pad, max(ys) + pad
    if bracket:
        x0 -= 0.25
        x1 += 0.55
    W, H = (x1 - x0) * UNIT, (y1 - y0) * UNIT
    P = lambda x, y: ((x - x0) * UNIT, (y - y0) * UNIT)
    out = []
    for k in highlight:
        cx, cy = P(s.atoms[k][1], s.atoms[k][2])
        out.append(f"<circle class='lw-hl' cx='{cx:.1f}' cy='{cy:.1f}' r='15'/>")
    for i, j, o in s.bonds:
        (ax, ay), (bx, by) = P(s.atoms[i][1], s.atoms[i][2]), P(s.atoms[j][1], s.atoms[j][2])
        L = math.hypot(bx - ax, by - ay)
        ux, uy = (bx - ax) / L, (by - ay) / L
        px, py = -uy, ux
        sh = 12.5
        for m in range(o):
            off = (m - (o - 1) / 2) * 4.2
            out.append(f"<line class='lw-bond' x1='{ax + ux * sh + px * off:.1f}' y1='{ay + uy * sh + py * off:.1f}' "
                       f"x2='{bx - ux * sh + px * off:.1f}' y2='{by - uy * sh + py * off:.1f}'/>")
    for k, a in enumerate(s.atoms):
        cx, cy = P(a[1], a[2])
        out.append(f"<text class='lw-atom' x='{cx:.1f}' y='{cy + 6.5:.1f}' text-anchor='middle'>{a[0]}</text>")
        nlp, nr = s.lp.get(k, 0), s.rad.get(k, 0)
        dirs = _lp_directions(s, k, nlp + nr)
        r0 = 15.5 if len(a[0]) == 1 else 19
        for d_i, ang in enumerate(dirs):
            t = math.radians(ang)
            dx, dy = math.cos(t), -math.sin(t)
            qx, qy = cx + dx * r0, cy + dy * r0
            if d_i < nlp:
                pxx, pyy = -dy * 3.3, dx * 3.3
                out.append(f"<circle class='lw-dot' cx='{qx + pxx:.1f}' cy='{qy + pyy:.1f}' r='2.1'/>"
                           f"<circle class='lw-dot' cx='{qx - pxx:.1f}' cy='{qy - pyy:.1f}' r='2.1'/>")
            else:
                out.append(f"<circle class='lw-dot lw-rad' cx='{qx:.1f}' cy='{qy:.1f}' r='2.3'/>")
        if show_fc:
            f = s.fc(k)
            if not (fc_only_nonzero and f == 0):
                # put the label in the widest gap left by bonds and electron dots, preferring the diagonals
                taken = dirs + [_angle(s.atoms[o][1] - a[1], s.atoms[o][2] - a[2])
                                for i, j, _ in s.bonds if k in (i, j) for o in [j if i == k else i]]
                best, bestv = 45, -1
                for c in (45, 135, 315, 225, 90, 0, 180, 270, 20, 70, 110, 160, 200, 250, 290, 340):
                    v = min((_adist(c, t) for t in taken), default=360) + (0.4 if c in (45, 135, 225, 315) else 0)
                    if v > bestv:
                        best, bestv = c, v
                t = math.radians(best)
                fx, fy = cx + math.cos(t) * 25, cy - math.sin(t) * 25 + 4
                out.append(f"<text class='lw-fc{' lw-fc0' if f == 0 else ''}' x='{fx:.1f}' y='{fy:.1f}' text-anchor='middle'>{fc_text(f)}</text>")
    if bracket:
        bx0, bx1 = 0.25 * UNIT, W - 0.55 * UNIT
        out.append(f"<path class='lw-bracket' d='M{bx0 + 6:.1f} 6 H{bx0:.1f} V{H - 6:.1f} H{bx0 + 6:.1f}'/>"
                   f"<path class='lw-bracket' d='M{bx1 - 6:.1f} 6 H{bx1:.1f} V{H - 6:.1f} H{bx1 - 6:.1f}'/>"
                   f"<text class='lw-charge' x='{bx1 + 4:.1f}' y='14'>{sup_charge(s.charge)}</text>")
    aria = (label or describe(s)).replace("'", "’")
    if tag == "span":
        cap = f"<span class='lw-cap'>{caption}</span>" if caption else ""
    else:
        cap = f"<figcaption class='lw-cap'>{caption}</figcaption>" if caption else ""
    return (f"<{tag} class='{klass}'><svg viewBox='0 0 {W:.0f} {H:.0f}' width='{W * scale:.0f}' height='{H * scale:.0f}' role='img' "
            f"aria-label='{aria}'>" + "".join(out) + f"</svg>{cap}</{tag}>")


def bo_text(x):
    """Bond order for display: 1.5, 1.33, 1.25, 2."""
    if abs(x - round(x)) < 1e-9:
        return str(int(round(x)))
    return f"{x:.1f}" if abs(x * 2 - round(x * 2)) < 1e-9 else f"{x:.2f}"


def average_orders(structs):
    """Average bond order of each bond over a set of resonance structures that share atoms and bond list order."""
    base = structs[0]
    for t in structs[1:]:
        assert [(i, j) for i, j, _ in t.bonds] == [(i, j) for i, j, _ in base.bonds], (base.id, t.id)
    return [sum(t.bonds[b][2] for t in structs) / len(structs) for b in range(len(base.bonds))]


def hybrid_svg(structs, caption=None, scale=1.0, pad=0.9, tag="figure", label=None):
    """The resonance-averaged structure: whole shared pairs as solid lines, a fractional part as a dashed line,
    with the average bond order printed beside each fractional bond. Lone pairs are omitted (they differ from
    structure to structure); an ion keeps its brackets and charge. BACKGROUND drawing convention."""
    s = structs[0]
    orders = average_orders(structs)
    xs = [a[1] for a in s.atoms]
    ys = [a[2] for a in s.atoms]
    x0, x1, y0, y1 = min(xs) - pad, max(xs) + pad, min(ys) - pad, max(ys) + pad
    bracket = s.charge != 0
    if bracket:
        x0 -= 0.25
        x1 += 0.55
    W, H = (x1 - x0) * UNIT, (y1 - y0) * UNIT
    P = lambda x, y: ((x - x0) * UNIT, (y - y0) * UNIT)
    out = []
    for (i, j, _), avg in zip(s.bonds, orders):
        (ax, ay), (bx, by) = P(s.atoms[i][1], s.atoms[i][2]), P(s.atoms[j][1], s.atoms[j][2])
        L = math.hypot(bx - ax, by - ay)
        ux, uy = (bx - ax) / L, (by - ay) / L
        px, py = -uy, ux
        whole = int(avg + 1e-9)
        frac = avg - whole
        n = whole + (1 if frac > 1e-6 else 0)
        for m in range(n):
            off = (m - (n - 1) / 2) * 4.2
            dash = " stroke-dasharray='3 3'" if (m == n - 1 and frac > 1e-6) else ""
            out.append(f"<line class='lw-bond'{dash} x1='{ax + ux * 12.5 + px * off:.1f}' y1='{ay + uy * 12.5 + py * off:.1f}' "
                       f"x2='{bx - ux * 12.5 + px * off:.1f}' y2='{by - uy * 12.5 + py * off:.1f}'/>")
        if frac > 1e-6:
            mx, my = (ax + bx) / 2, (ay + by) / 2
            # label on the side away from the molecule's centre
            cx = sum(P(a[1], a[2])[0] for a in s.atoms) / len(s.atoms)
            cy = sum(P(a[1], a[2])[1] for a in s.atoms) / len(s.atoms)
            sgn = 1 if (mx - cx) * px + (my - cy) * py >= 0 else -1
            txt = bo_text(avg)
            out.append(f"<text class='lw-fc lw-bo' x='{mx + sgn * px * 17:.1f}' y='{my + sgn * py * 17 + 4:.1f}' text-anchor='middle'>{txt}</text>")
    for a in s.atoms:
        cx, cy = P(a[1], a[2])
        out.append(f"<text class='lw-atom' x='{cx:.1f}' y='{cy + 6.5:.1f}' text-anchor='middle'>{a[0]}</text>")
    if bracket:
        bx0, bx1 = 0.25 * UNIT, W - 0.55 * UNIT
        out.append(f"<path class='lw-bracket' d='M{bx0 + 6:.1f} 6 H{bx0:.1f} V{H - 6:.1f} H{bx0 + 6:.1f}'/>"
                   f"<path class='lw-bracket' d='M{bx1 - 6:.1f} 6 H{bx1:.1f} V{H - 6:.1f} H{bx1 - 6:.1f}'/>"
                   f"<text class='lw-charge' x='{bx1 + 4:.1f}' y='14'>{sup_charge(s.charge)}</text>")
    kinds = sorted({f"{s.atoms[i][0]}–{s.atoms[j][0]} {bo_text(o)}" for (i, j, _), o in zip(s.bonds, orders) if o % 1})
    aria = (label or f"Average of the resonance structures of {s.name}: bond orders " + ", ".join(kinds)).replace("'", "’")
    cap = ""
    if caption:
        cap = f"<span class='lw-cap'>{caption}</span>" if tag == "span" else f"<figcaption class='lw-cap'>{caption}</figcaption>"
    return (f"<{tag} class='lewis lewis-hybrid'><svg viewBox='0 0 {W:.0f} {H:.0f}' width='{W * scale:.0f}' height='{H * scale:.0f}' role='img' "
            f"aria-label='{aria}'>" + "".join(out) + f"</svg>{cap}</{tag}>")


def charge_words(q):
    return f"{abs(q)}{'+' if q > 0 else MINUS}"


def atom_label(s, k):
    """'O', 'central O', 'left O', 'lower right O': enough to tell same-element atoms apart when read aloud."""
    sym = s.atoms[k][0]
    same = [i for i, a in enumerate(s.atoms) if a[0] == sym]
    if len(same) == 1:
        return sym
    if len(s.central) == 1 and k in s.central:
        return "central " + sym
    heavy = [a for a in s.atoms if a[0] != "H"] or s.atoms           # positions relative to the heavy atoms
    cx = sum(a[1] for a in heavy) / len(heavy)
    cy = sum(a[2] for a in heavy) / len(heavy)
    dx, dy = s.atoms[k][1] - cx, s.atoms[k][2] - cy
    pos = ("upper " if dy < -0.3 else "lower " if dy > 0.3 else "") + ("left " if dx < -0.3 else "right " if dx > 0.3 else "")
    return (pos or "middle ") + sym


def describe(s, named=True):
    """Plain-language description for screen readers (and text-only solvers). named=False drops the species'
    name, for multiple-choice options, so the correct drawing isn't the only one with a proper name."""
    if s.id.startswith("C6H6"):
        return (f"Lewis structure{' of ' + s.name if named else ''}: a ring of six C atoms with alternating single and double bonds, "
                "one H bonded to each C")
    names = {1: "single", 2: "double", 3: "triple"}
    lab = [atom_label(s, k) for k in range(len(s.atoms))]
    parts = [f"{lab[i]}–{lab[j]} {names[o]} bond" for i, j, o in s.bonds]
    lps = [f"{n} lone pair{'s' if n > 1 else ''} on {'the ' if ' ' in lab[k] else ''}{lab[k]}" for k, n in sorted(s.lp.items()) if n]
    rads = [f"an unpaired electron on {'the ' if ' ' in lab[k] else ''}{lab[k]}" for k, n in s.rad.items() if n]
    ch = f"; overall charge {charge_words(s.charge)}" if s.charge else ""
    head = f"Lewis structure of {s.name}: " if named else "Lewis structure: "
    return head + ", ".join(parts + lps + rads) + ch


def symbol_svg(el):
    """Lewis symbol: dots placed on four sides one at a time before pairing (Day 8 p.17).
    Singles go left, right, bottom, top (as in the slide's table); pairs form top, bottom, left, right.
    He is drawn with one pair on the left, as on the slide."""
    v = VALENCE[el]
    W, H = 70, 64
    cx, cy = W / 2, H / 2
    out = [f"<text class='lw-atom' x='{cx:.1f}' y='{cy + 6.5:.1f}' text-anchor='middle'>{el}</text>"]
    sides = {"left": (-1, 0), "right": (1, 0), "bottom": (0, 1), "top": (0, -1)}
    count = {k: 0 for k in sides}
    if el == "He":
        count["left"] = 2
    else:
        order1, order2 = ["left", "right", "bottom", "top"], ["top", "bottom", "left", "right"]
        for n in range(v):
            if n < 4:
                count[order1[n]] = 1
            else:
                count[order2[n - 4]] = 2
    r0 = 15.5 if len(el) == 1 else 19.5
    for side, n in count.items():
        dx, dy = sides[side]
        qx, qy = cx + dx * r0, cy + dy * r0
        if n == 1:
            out.append(f"<circle class='lw-dot' cx='{qx:.1f}' cy='{qy:.1f}' r='2.3'/>")
        elif n == 2:
            px, py = -dy * 3.3, dx * 3.3
            out.append(f"<circle class='lw-dot' cx='{qx + px:.1f}' cy='{qy + py:.1f}' r='2.2'/>"
                       f"<circle class='lw-dot' cx='{qx - px:.1f}' cy='{qy - py:.1f}' r='2.2'/>")
    unpaired = sum(1 for n in count.values() if n == 1)
    aria = f"Lewis symbol of {el}: {v} valence electron{'s' if v != 1 else ''}, {unpaired} unpaired"
    return (f"<svg class='lw-sym' viewBox='0 0 {W} {H}' width='{W}' height='{H}' role='img' aria-label='{aria}'>"
            + "".join(out) + "</svg>"), unpaired


# ================================================================ the structures
def S(*a, **k):
    return Structure(*a, **k)


STRUCTS = {}


def add(s):
    STRUCTS[s.id] = s
    return s


# lecture examples (Day 8)
add(S("F2", "fluorine, F₂", "F<sub>2</sub>", [("F", 0, 0), ("F", 1.3, 0)], [(0, 1, 1)], {0: 3, 1: 3},
      central=[], source="Day 8 p.19"))
add(S("O2", "oxygen, O₂", "O<sub>2</sub>", [("O", 0, 0), ("O", 1.3, 0)], [(0, 1, 2)], {0: 2, 1: 2},
      central=[], source="Day 8 p.20"))
add(S("N2", "nitrogen, N₂", "N<sub>2</sub>", [("N", 0, 0), ("N", 1.3, 0)], [(0, 1, 3)], {0: 1, 1: 1},
      central=[], source="Day 8 p.20"))
add(S("NH3", "ammonia, NH₃", "NH<sub>3</sub>", [("N", 1, 0), ("H", 0, 0), ("H", 2, 0), ("H", 1, 1)],
      [(0, 1, 1), (0, 2, 1), (0, 3, 1)], {0: 1}, central=[0], source="Day 8 p.22–23"))
add(S("C2H2", "ethyne (acetylene), C₂H₂", "C<sub>2</sub>H<sub>2</sub>",
      [("H", 0, 0), ("C", 1, 0), ("C", 2.2, 0), ("H", 3.2, 0)], [(0, 1, 1), (1, 2, 3), (2, 3, 1)], {},
      central=[1, 2], source="Day 8 p.24–25"))
add(S("O3a", "ozone, O₃ (double bond on the left)", "O<sub>3</sub>",
      [("O", 0, 0.9), ("O", 1.05, 0.25), ("O", 2.1, 0.9)], [(0, 1, 2), (1, 2, 1)], {0: 2, 1: 1, 2: 3},
      central=[1], source="Day 8 p.30"))
add(S("O3b", "ozone, O₃ (double bond on the right)", "O<sub>3</sub>",
      [("O", 0, 0.9), ("O", 1.05, 0.25), ("O", 2.1, 0.9)], [(0, 1, 1), (1, 2, 2)], {0: 3, 1: 1, 2: 2},
      central=[1], source="Day 8 p.30"))
# textbook §4.4 examples and practice molecules
add(S("CH4", "methane, CH₄", "CH<sub>4</sub>", [("C", 1, 1), ("H", 0, 1), ("H", 2, 1), ("H", 1, 0), ("H", 1, 2)],
      [(0, 1, 1), (0, 2, 1), (0, 3, 1), (0, 4, 1)], {}, central=[0], source="textbook §4.4, PDF p.198"))
add(S("H2O", "water, H₂O", "H<sub>2</sub>O", [("O", 1, 0), ("H", 0, 0), ("H", 2, 0)],
      [(0, 1, 1), (0, 2, 1)], {0: 2}, central=[0], source="new example"))
add(S("CHCl3", "chloroform, CHCl₃", "CHCl<sub>3</sub>",
      [("C", 1, 1), ("Cl", 0, 1), ("Cl", 2, 1), ("H", 1, 0), ("Cl", 1, 2)],
      [(0, 1, 1), (0, 2, 1), (0, 3, 1), (0, 4, 1)], {1: 3, 2: 3, 4: 3}, central=[0], source="textbook §4.4, PDF p.198"))
add(S("OH-", "hydroxide ion, OH⁻", "OH<sup>−</sup>", [("O", 0, 0), ("H", 1, 0)], [(0, 1, 1)], {0: 3},
      charge=-1, central=[0], source="textbook §4.4, PDF p.199–200"))
add(S("NH4+", "ammonium ion, NH₄⁺", "NH<sub>4</sub><sup>+</sup>",
      [("N", 1, 1), ("H", 0, 1), ("H", 2, 1), ("H", 1, 0), ("H", 1, 2)], [(0, 1, 1), (0, 2, 1), (0, 3, 1), (0, 4, 1)], {},
      charge=1, central=[0], source="textbook §4.4 practice, PDF p.200"))
add(S("H2O2", "hydrogen peroxide, H₂O₂", "H<sub>2</sub>O<sub>2</sub>",
      [("H", 0, 0), ("O", 1, 0), ("O", 2.2, 0), ("H", 3.2, 0)], [(0, 1, 1), (1, 2, 1), (2, 3, 1)], {1: 2, 2: 2},
      central=[1, 2], source="textbook §4.4, PDF p.200"))
add(S("CH2O", "formaldehyde, CH₂O", "CH<sub>2</sub>O", [("C", 1, 1), ("H", 0, 1), ("H", 2, 1), ("O", 1, 0)],
      [(0, 1, 1), (0, 2, 1), (0, 3, 2)], {3: 2}, central=[0], source="textbook §4.4, PDF p.201"))
add(S("CO2", "carbon dioxide, CO₂", "CO<sub>2</sub>", [("O", 0, 0), ("C", 1.2, 0), ("O", 2.4, 0)],
      [(0, 1, 2), (1, 2, 2)], {0: 2, 2: 2}, central=[1], source="textbook §4.4 practice, §4.7 Sample Ex. 4.16"))
add(S("HCN", "hydrogen cyanide, HCN", "HCN", [("H", 0, 0), ("C", 1, 0), ("N", 2.2, 0)],
      [(0, 1, 1), (1, 2, 3)], {2: 1}, central=[1], source="new example"))
add(S("PCl3", "phosphorus trichloride, PCl₃", "PCl<sub>3</sub>",
      [("P", 1, 0), ("Cl", 0, 0), ("Cl", 2, 0), ("Cl", 1, 1)], [(0, 1, 1), (0, 2, 1), (0, 3, 1)], {0: 1, 1: 3, 2: 3, 3: 3},
      central=[0], source="textbook §4.4 practice, PDF p.199"))
add(S("CO", "carbon monoxide, CO", "CO", [("C", 0, 0), ("O", 1.2, 0)], [(0, 1, 3)], {0: 1, 1: 1},
      central=[], source="textbook §4.6 Fig. 4.12"))
# resonance (§4.5) and bond order (§4.6)
for n, dbl in enumerate(("up", "left", "right")):
    orders = {"up": (2, 1, 1), "left": (1, 2, 1), "right": (1, 1, 2)}[dbl]
    lps = {1: 3 - (orders[0] - 1), 2: 3 - (orders[1] - 1), 3: 3 - (orders[2] - 1)}
    add(S(f"NO3-{n + 1}", "nitrate ion, NO₃⁻", "NO<sub>3</sub><sup>−</sup>",
          [("N", 1, 1), ("O", 1, 0), ("O", 0, 1.6), ("O", 2, 1.6)], [(0, 1, orders[0]), (0, 2, orders[1]), (0, 3, orders[2])],
          lps, charge=-1, central=[0], source="textbook §4.5 Sample Ex. 4.14, PDF p.204–205"))
    add(S(f"CO3-{n + 1}", "carbonate ion, CO₃²⁻", "CO<sub>3</sub><sup>2−</sup>",
          [("C", 1, 1), ("O", 1, 0), ("O", 0, 1.6), ("O", 2, 1.6)], [(0, 1, orders[0]), (0, 2, orders[1]), (0, 3, orders[2])],
          lps, charge=-2, central=[0], source="textbook §4.6 Sample Ex. 4.15, PDF p.206–208"))
for n, side in enumerate(("left", "right")):
    o = (2, 1) if side == "left" else (1, 2)
    add(S(f"NO2-{n + 1}", "nitrite ion, NO₂⁻", "NO<sub>2</sub><sup>−</sup>",
          [("O", 0, 0.9), ("N", 1.05, 0.25), ("O", 2.1, 0.9)], [(0, 1, o[0]), (1, 2, o[1])],
          {0: 3 - (o[0] - 1), 1: 1, 2: 3 - (o[1] - 1)}, charge=-1, central=[1], source="new example (nitrite, Table 4.4)"))
# formal charge (§4.7): N2O A/B/C and CO2 alternatives
add(S("N2O-A", "dinitrogen monoxide, N₂O (structure A)", "N<sub>2</sub>O", [("N", 0, 0), ("N", 1.2, 0), ("O", 2.4, 0)],
      [(0, 1, 3), (1, 2, 1)], {0: 1, 2: 3}, central=[1], source="textbook §4.7, PDF p.210"))
add(S("N2O-B", "dinitrogen monoxide, N₂O (structure B)", "N<sub>2</sub>O", [("N", 0, 0), ("N", 1.2, 0), ("O", 2.4, 0)],
      [(0, 1, 2), (1, 2, 2)], {0: 2, 2: 2}, central=[1], source="textbook §4.7, PDF p.210"))
add(S("N2O-C", "dinitrogen monoxide, N₂O (structure C)", "N<sub>2</sub>O", [("N", 0, 0), ("N", 1.2, 0), ("O", 2.4, 0)],
      [(0, 1, 1), (1, 2, 3)], {0: 3, 2: 1}, central=[1], source="textbook §4.7, PDF p.210"))
add(S("CO2-alt1", "carbon dioxide, CO₂ (O≡C–O form)", "CO<sub>2</sub>", [("O", 0, 0), ("C", 1.2, 0), ("O", 2.4, 0)],
      [(0, 1, 3), (1, 2, 1)], {0: 1, 2: 3}, central=[1], source="textbook §4.7 Sample Ex. 4.16"))
add(S("CO2-alt2", "carbon dioxide, CO₂ (O–C≡O form)", "CO<sub>2</sub>", [("O", 0, 0), ("C", 1.2, 0), ("O", 2.4, 0)],
      [(0, 1, 1), (1, 2, 3)], {0: 3, 2: 1}, central=[1], source="textbook §4.7 Sample Ex. 4.16"))
add(S("NO2+", "nitronium ion, NO₂⁺", "NO<sub>2</sub><sup>+</sup>", [("O", 0, 0), ("N", 1.2, 0), ("O", 2.4, 0)],
      [(0, 1, 2), (1, 2, 2)], {0: 2, 2: 2}, charge=1, central=[1], source="textbook §4.5/4.7 practice"))
add(S("SCN-a", "thiocyanate ion, SCN⁻ (S–C≡N)", "SCN<sup>−</sup>", [("S", 0, 0), ("C", 1.2, 0), ("N", 2.4, 0)],
      [(0, 1, 1), (1, 2, 3)], {0: 3, 2: 1}, charge=-1, central=[1], source="new example (thiocyanate, Table 4.4)"))
add(S("SCN-b", "thiocyanate ion, SCN⁻ (S=C=N)", "SCN<sup>−</sup>", [("S", 0, 0), ("C", 1.2, 0), ("N", 2.4, 0)],
      [(0, 1, 2), (1, 2, 2)], {0: 2, 2: 2}, charge=-1, central=[1], source="new example"))
add(S("SCN-c", "thiocyanate ion, SCN⁻ (S≡C–N)", "SCN<sup>−</sup>", [("S", 0, 0), ("C", 1.2, 0), ("N", 2.4, 0)],
      [(0, 1, 3), (1, 2, 1)], {0: 1, 2: 3}, charge=-1, central=[1], source="new example"))
# octet exceptions (§4.8)
add(S("BF3", "boron trifluoride, BF₃", "BF<sub>3</sub>", [("B", 1, 1), ("F", 1, 0), ("F", 0, 1.6), ("F", 2, 1.6)],
      [(0, 1, 1), (0, 2, 1), (0, 3, 1)], {1: 3, 2: 3, 3: 3}, central=[0], source="textbook §4.8 (B forms electron-deficient molecules), PDF p.212"))
add(S("BeCl2", "beryllium chloride, BeCl₂ (molecule)", "BeCl<sub>2</sub>", [("Cl", 0, 0), ("Be", 1.25, 0), ("Cl", 2.5, 0)],
      [(0, 1, 1), (1, 2, 1)], {0: 3, 2: 3}, central=[1], source="textbook §4.8 (Be), PDF p.212"))
add(S("NO", "nitrogen monoxide, NO", "NO", [("N", 0, 0), ("O", 1.2, 0)], [(0, 1, 2)], {0: 1, 1: 2}, rad={0: 1},
      central=[], source="textbook §4.8, PDF p.212–213"))
add(S("NO2-rad1", "nitrogen dioxide, NO₂", "NO<sub>2</sub>", [("O", 0, 0.9), ("N", 1.05, 0.25), ("O", 2.1, 0.9)],
      [(0, 1, 2), (1, 2, 1)], {0: 2, 2: 3}, rad={1: 1}, central=[1], source="textbook §4.8 Sample Ex. 4.17, PDF p.213–214"))
add(S("NO2-rad2", "nitrogen dioxide, NO₂", "NO<sub>2</sub>", [("O", 0, 0.9), ("N", 1.05, 0.25), ("O", 2.1, 0.9)],
      [(0, 1, 1), (1, 2, 2)], {0: 3, 2: 2}, rad={1: 1}, central=[1], source="textbook §4.8 Sample Ex. 4.17"))
add(S("PCl5", "phosphorus pentachloride, PCl₅", "PCl<sub>5</sub>",
      [("P", 1.2, 1.2), ("Cl", 1.2, 0), ("Cl", 0, 0.9), ("Cl", 2.4, 0.9), ("Cl", 0.5, 2.3), ("Cl", 1.9, 2.3)],
      [(0, 1, 1), (0, 2, 1), (0, 3, 1), (0, 4, 1), (0, 5, 1)], {1: 3, 2: 3, 3: 3, 4: 3, 5: 3}, central=[0],
      source="textbook §4.8, PDF p.214"))
add(S("SF6", "sulfur hexafluoride, SF₆", "SF<sub>6</sub>",
      [("S", 1.2, 1.2), ("F", 1.2, 0), ("F", 1.2, 2.4), ("F", 0, 0.6), ("F", 2.4, 0.6), ("F", 0, 1.8), ("F", 2.4, 1.8)],
      [(0, 1, 1), (0, 2, 1), (0, 3, 1), (0, 4, 1), (0, 5, 1), (0, 6, 1)], {k: 3 for k in range(1, 7)}, central=[0],
      source="textbook §4.8, PDF p.214"))
add(S("SO4-oct", "sulfate ion, SO₄²⁻ (octets only)", "SO<sub>4</sub><sup>2−</sup>",
      [("S", 1, 1), ("O", 1, 0), ("O", 0, 1), ("O", 2, 1), ("O", 1, 2)], [(0, 1, 1), (0, 2, 1), (0, 3, 1), (0, 4, 1)],
      {1: 3, 2: 3, 3: 3, 4: 3}, charge=-2, central=[0], source="textbook §4.8, PDF p.215"))
add(S("SO4-exp", "sulfate ion, SO₄²⁻ (two S=O)", "SO<sub>4</sub><sup>2−</sup>",
      [("S", 1, 1), ("O", 1, 0), ("O", 0, 1), ("O", 2, 1), ("O", 1, 2)], [(0, 1, 2), (0, 2, 1), (0, 3, 1), (0, 4, 2)],
      {1: 2, 2: 3, 3: 3, 4: 2}, charge=-2, central=[0], source="textbook §4.8, PDF p.215"))
add(S("PO4-oct", "phosphate ion, PO₄³⁻ (octets only)", "PO<sub>4</sub><sup>3−</sup>",
      [("P", 1, 1), ("O", 1, 0), ("O", 0, 1), ("O", 2, 1), ("O", 1, 2)], [(0, 1, 1), (0, 2, 1), (0, 3, 1), (0, 4, 1)],
      {1: 3, 2: 3, 3: 3, 4: 3}, charge=-3, central=[0], source="textbook §4.8 Sample Ex. 4.18, PDF p.216"))
add(S("PO4-exp", "phosphate ion, PO₄³⁻ (one P=O)", "PO<sub>4</sub><sup>3−</sup>",
      [("P", 1, 1), ("O", 1, 0), ("O", 0, 1), ("O", 2, 1), ("O", 1, 2)], [(0, 1, 2), (0, 2, 1), (0, 3, 1), (0, 4, 1)],
      {1: 2, 2: 3, 3: 3, 4: 3}, charge=-3, central=[0], source="textbook §4.8 Sample Ex. 4.18, PDF p.216"))
add(S("H2SO4", "sulfuric acid, H₂SO₄", "H<sub>2</sub>SO<sub>4</sub>",
      [("S", 1.2, 1), ("O", 1.2, 0), ("O", 0, 1), ("O", 2.4, 1), ("O", 1.2, 2), ("H", -1, 1), ("H", 3.4, 1)],
      [(0, 1, 2), (0, 2, 1), (0, 3, 1), (0, 4, 2), (2, 5, 1), (3, 6, 1)], {1: 2, 2: 2, 3: 2, 4: 2}, central=[0, 2, 3],
      source="textbook §4.8, PDF p.215"))

# extra structures for the Ch. 4 problems (new examples, checked below like the rest)
for n, side in enumerate(("left", "right")):
    o = (2, 1) if side == "left" else (1, 2)
    add(S(f"HCO2-{n + 1}", "formate ion, HCO₂⁻", "HCO<sub>2</sub><sup>−</sup>",
          [("O", 0, 0.9), ("C", 1.05, 0.25), ("O", 2.1, 0.9), ("H", 1.05, -0.85)], [(0, 1, o[0]), (1, 2, o[1]), (1, 3, 1)],
          {0: 3 - (o[0] - 1), 2: 3 - (o[1] - 1)}, charge=-1, central=[1], source="new example"))
add(S("C2H4", "ethene, C₂H₄", "C<sub>2</sub>H<sub>4</sub>",
      [("C", 1, 0.6), ("C", 2.2, 0.6), ("H", 0.3, -0.2), ("H", 0.3, 1.4), ("H", 2.9, -0.2), ("H", 2.9, 1.4)],
      [(0, 1, 2), (0, 2, 1), (0, 3, 1), (1, 4, 1), (1, 5, 1)], {}, central=[0, 1], source="new example"))
add(S("CH3OH", "methanol, CH₃OH", "CH<sub>3</sub>OH",
      [("C", 1, 1), ("H", 0, 1), ("H", 1, 0), ("H", 1, 2), ("O", 2.2, 1), ("H", 3.2, 1)],
      [(0, 1, 1), (0, 2, 1), (0, 3, 1), (0, 4, 1), (4, 5, 1)], {4: 2}, central=[0, 4], source="new example"))
add(S("SO3-oct", "sulfite ion, SO₃²⁻ (octets only)", "SO<sub>3</sub><sup>2−</sup>",
      [("S", 1, 0.9), ("O", 0, 0.9), ("O", 2, 0.9), ("O", 1, 1.95)], [(0, 1, 1), (0, 2, 1), (0, 3, 1)],
      {0: 1, 1: 3, 2: 3, 3: 3}, charge=-2, central=[0], source="new example (compare textbook §4.8 practice, selenite)"))
add(S("SO3-exp", "sulfite ion, SO₃²⁻ (one S=O)", "SO<sub>3</sub><sup>2−</sup>",
      [("S", 1, 0.9), ("O", 0, 0.9), ("O", 2, 0.9), ("O", 1, 1.95)], [(0, 1, 2), (0, 2, 1), (0, 3, 1)],
      {0: 1, 1: 2, 2: 3, 3: 3}, charge=-2, central=[0], source="new example"))
add(S("Cl-ion", "chloride ion, Cl⁻", "Cl<sup>−</sup>", [("Cl", 0, 0)], [], {0: 4}, charge=-1, central=[],
      source="textbook §4.4, PDF p.196 (ionic Lewis structures)"))
add(S("S2-ion", "sulfide ion, S²⁻", "S<sup>2−</sup>", [("S", 0, 0)], [], {0: 4}, charge=-2, central=[],
      source="new example (ionic Lewis structure, textbook §4.4 PDF p.196 style)"))
add(S("HOCl", "hypochlorous acid, HOCl", "HOCl", [("H", 0, 0.6), ("O", 1, 0), ("Cl", 2.2, 0.6)],
      [(0, 1, 1), (1, 2, 1)], {1: 2, 2: 3}, central=[1], source="new example"))
add(S("CS2", "carbon disulfide, CS₂", "CS<sub>2</sub>", [("S", 0, 0), ("C", 1.25, 0), ("S", 2.5, 0)],
      [(0, 1, 2), (1, 2, 2)], {0: 2, 2: 2}, central=[1], source="new example"))
add(S("CS2-alt", "carbon disulfide, CS₂ (S≡C–S form)", "CS<sub>2</sub>", [("S", 0, 0), ("C", 1.25, 0), ("S", 2.5, 0)],
      [(0, 1, 3), (1, 2, 1)], {0: 1, 2: 3}, central=[1], source="new example"))
add(S("N2H4", "hydrazine, N₂H₄", "N<sub>2</sub>H<sub>4</sub>",
      [("N", 1, 0.6), ("N", 2.2, 0.6), ("H", 0.3, -0.2), ("H", 0.3, 1.4), ("H", 2.9, -0.2), ("H", 2.9, 1.4)],
      [(0, 1, 1), (0, 2, 1), (0, 3, 1), (1, 4, 1), (1, 5, 1)], {0: 1, 1: 1}, central=[0, 1], source="new example"))
add(S("BrF5", "bromine pentafluoride, BrF₅", "BrF<sub>5</sub>",
      [("Br", 1.2, 1.1), ("F", 1.2, -0.1), ("F", 0, 1.1), ("F", 2.4, 1.1), ("F", 0.35, 2.15), ("F", 2.05, 2.15)],
      [(0, 1, 1), (0, 2, 1), (0, 3, 1), (0, 4, 1), (0, 5, 1)], {0: 1, 1: 3, 2: 3, 3: 3, 4: 3, 5: 3}, central=[0],
      source="new example"))
for n, which in enumerate((1, 2)):
    o1, o2 = (2, 1) if which == 1 else (1, 2)
    add(S(f"HCO3-{n + 1}", "hydrogen carbonate ion, HCO₃⁻", "HCO<sub>3</sub><sup>−</sup>",
          [("C", 1.2, 1.0), ("O", 1.2, -0.2), ("O", 0.15, 1.6), ("O", 2.25, 1.6), ("H", 3.25, 1.6)],
          [(0, 1, o1), (0, 2, o2), (0, 3, 1), (3, 4, 1)], {1: 3 - (o1 - 1), 2: 3 - (o2 - 1), 3: 2}, charge=-1,
          central=[0, 3], source="new example (bicarbonate, Day 8 p.8–9)"))
    add(S(f"CH3COO-{n + 1}", "acetate ion, CH₃COO⁻", "CH<sub>3</sub>COO<sup>−</sup>",
          [("C", 1, 1), ("H", 0, 1), ("H", 1, 0), ("H", 1, 2), ("C", 2.2, 1), ("O", 3.0, 0.15), ("O", 3.0, 1.85)],
          [(0, 1, 1), (0, 2, 1), (0, 3, 1), (0, 4, 1), (4, 5, o1), (4, 6, o2)], {5: 3 - (o1 - 1), 6: 3 - (o2 - 1)}, charge=-1,
          central=[0, 4], source="new example (acetate, Day 8 p.8)"))
_R = 1.25
_hexa =[(_R * math.cos(math.radians(90 - 60 * k)) + 2.3, -_R * math.sin(math.radians(90 - 60 * k)) + 2.3) for k in range(6)]
_hexH = [(2.12 * math.cos(math.radians(90 - 60 * k)) + 2.3, -2.12 * math.sin(math.radians(90 - 60 * k)) + 2.3) for k in range(6)]
for n in range(2):
    atoms = [("C", x, y) for x, y in _hexa] + [("H", x, y) for x, y in _hexH]
    ring = [(k, (k + 1) % 6, 2 if (k + n) % 2 == 0 else 1) for k in range(6)]
    add(S(f"C6H6-{n + 1}", "benzene, C₆H₆", "C<sub>6</sub>H<sub>6</sub>", atoms, ring + [(k, k + 6, 1) for k in range(6)], {},
          central=list(range(6)), source="textbook §4.5 Fig. 4.10, PDF p.205"))

# ---------------------------------------------------------------- Day 9 and Chapter 5 structures (added 2026-10-06)
def _around(cx, cy, r, angles):
    """points at the given angles (degrees, 0 = right, 90 = up) around (cx, cy); y runs down the page."""
    return [(cx + r * math.cos(math.radians(a)), cy - r * math.sin(math.radians(a))) for a in angles]


def _star(sid, name, html_f, center, outer, angles, lp_center=0, lp_outer=3, charge=0, r=1.2, source="new example"):
    """central atom + outer atoms at the given angles; every outer atom gets lp_outer lone pairs."""
    pts = _around(1.3, 1.3, r, angles)
    atoms = [(center, 1.3, 1.3)] + [(el, x, y) for el, (x, y) in zip(outer, pts)]
    bonds = [(0, k, 1) for k in range(1, len(atoms))]
    lp = {k: (0 if atoms[k][0] == "H" else lp_outer) for k in range(1, len(atoms))}
    if lp_center:
        lp[0] = lp_center
    return add(S(sid, name, html_f, atoms, bonds, lp, charge=charge, central=[0], source=source))


# Day 9 p.27: electron-deficient molecules
_star("AlCl3", "aluminum chloride, AlCl₃ (molecule)", "AlCl<sub>3</sub>", "Al", ["Cl"] * 3, [90, 210, 330], source="Day 9 p.27")
_star("BCl3", "boron trichloride, BCl₃", "BCl<sub>3</sub>", "B", ["Cl"] * 3, [90, 210, 330], source="Day 9 p.27")
# Day 9 p.26 (Top Hat): three of the five phosphoric-acid structures have the right electron count (32);
# options 4 and 5 (H on P; an H bonded to both P and O) are drawn ad hoc where they're used, since they're wrong.
_P = [("P", 1.3, 1.3), ("O", 1.3, 0.05), ("O", 0.05, 1.3), ("O", 2.55, 1.3), ("O", 1.3, 2.55),
      ("H", -0.95, 1.3), ("H", 3.55, 1.3), ("H", 1.3, 3.55)]
_PB = [(0, 1), (0, 2), (0, 3), (0, 4), (2, 5), (3, 6), (4, 7)]
add(S("H3PO4-t1", "phosphoric acid, H₃PO₄ (Top Hat structure 1)", "H<sub>3</sub>PO<sub>4</sub>", _P,
      [(i, j, 2 if (i, j) == (0, 4) else 1) for i, j in _PB], {1: 3, 2: 2, 3: 2, 4: 1}, central=[0, 2, 3, 4], source="Day 9 p.26"))
add(S("H3PO4-t2", "phosphoric acid, H₃PO₄ (Top Hat structure 2)", "H<sub>3</sub>PO<sub>4</sub>", _P,
      [(i, j, 1) for i, j in _PB], {1: 3, 2: 2, 3: 2, 4: 2}, central=[0, 2, 3, 4], source="Day 9 p.26"))
add(S("H3PO4-t3", "phosphoric acid, H₃PO₄ (Top Hat structure 3)", "H<sub>3</sub>PO<sub>4</sub>", _P,
      [(i, j, 2 if (i, j) == (0, 1) else 1) for i, j in _PB], {1: 2, 2: 2, 3: 2, 4: 2}, central=[0, 2, 3, 4], source="Day 9 p.26"))
# Day 10: VSEPR examples with no lone pairs on the central atom
_star("CCl4", "carbon tetrachloride, CCl₄", "CCl<sub>4</sub>", "C", ["Cl"] * 4, [90, 180, 0, 270], source="Day 10 p.10–11")
_star("CF4", "carbon tetrafluoride, CF₄", "CF<sub>4</sub>", "C", ["F"] * 4, [90, 180, 0, 270], source="Day 10 p.30")
_star("PF5", "phosphorus pentafluoride, PF₅", "PF<sub>5</sub>", "P", ["F"] * 5, [90, 162, 18, 234, 306], source="Day 10 p.12")
# textbook Table 5.1 (TB PDF p.240), Sample Ex. 5.3, and new examples with lone pairs on the central atom
_star("SF4", "sulfur tetrafluoride, SF₄", "SF<sub>4</sub>", "S", ["F"] * 4, [90, 180, 0, 270], lp_center=1,
      source="textbook §5.2 Sample Ex. 5.3, PDF p.242–243")
_star("SCl4", "sulfur tetrachloride, SCl₄", "SCl<sub>4</sub>", "S", ["Cl"] * 4, [90, 180, 0, 270], lp_center=1,
      source="textbook Table 5.1, PDF p.240")
_star("ClF3", "chlorine trifluoride, ClF₃", "ClF<sub>3</sub>", "Cl", ["F"] * 3, [90, 0, 270], lp_center=2,
      source="textbook §5.2 practice, PDF p.243")
_star("BrF3", "bromine trifluoride, BrF₃", "BrF<sub>3</sub>", "Br", ["F"] * 3, [90, 0, 270], lp_center=2,
      source="textbook Table 5.1, PDF p.240")
add(S("XeF2", "xenon difluoride, XeF₂", "XeF<sub>2</sub>", [("F", 0, 0), ("Xe", 1.4, 0), ("F", 2.8, 0)],
      [(0, 1, 1), (1, 2, 1)], {0: 3, 1: 3, 2: 3}, central=[1], source="textbook Table 5.1, PDF p.240"))
_star("XeF4", "xenon tetrafluoride, XeF₄", "XeF<sub>4</sub>", "Xe", ["F"] * 4, [90, 180, 0, 270], lp_center=2,
      source="textbook Table 5.1, PDF p.240")
_star("IF5", "iodine pentafluoride, IF₅", "IF<sub>5</sub>", "I", ["F"] * 5, [90, 162, 18, 234, 306], lp_center=1,
      source="textbook Table 5.1, PDF p.240")
add(S("I3-", "triiodide ion, I₃⁻", "I<sub>3</sub><sup>−</sup>", [("I", 0, 0), ("I", 1.4, 0), ("I", 2.8, 0)],
      [(0, 1, 1), (1, 2, 1)], {0: 3, 1: 3, 2: 3}, charge=-1, central=[1], source="new example"))
_star("ICl4-", "tetrachloroiodate ion, ICl₄⁻", "ICl<sub>4</sub><sup>−</sup>", "I", ["Cl"] * 4, [90, 180, 0, 270], lp_center=2, charge=-1)
for n, side in enumerate(("left", "right")):
    o = (2, 1) if side == "left" else (1, 2)
    add(S(f"SO2-{n + 1}", "sulfur dioxide, SO₂", "SO<sub>2</sub>", [("O", 0, 0.9), ("S", 1.05, 0.25), ("O", 2.1, 0.9)],
          [(0, 1, o[0]), (1, 2, o[1])], {0: 3 - (o[0] - 1), 1: 1, 2: 3 - (o[1] - 1)}, central=[1],
          source="textbook Table 5.1, PDF p.240 (two resonance forms)"))
add(S("SO2-exp", "sulfur dioxide, SO₂ (two S=O)", "SO<sub>2</sub>", [("O", 0, 0.9), ("S", 1.05, 0.25), ("O", 2.1, 0.9)],
      [(0, 1, 2), (1, 2, 2)], {0: 2, 1: 1, 2: 2}, central=[1], source="new example (expanded octet, Day 9 p.29)"))
# polarity (Day 10 p.29-31; Day 11 p.7-8; textbook §5.3)
add(S("CH2Cl2", "dichloromethane, CH₂Cl₂", "CH<sub>2</sub>Cl<sub>2</sub>",
      [("C", 1, 1), ("H", 1, 0), ("H", 0, 1), ("Cl", 2, 1), ("Cl", 1, 2)], [(0, 1, 1), (0, 2, 1), (0, 3, 1), (0, 4, 1)],
      {3: 3, 4: 3}, central=[0], source="textbook §5.3 Sample Ex. 5.4, PDF p.245–246"))
_star("CCl3F", "trichlorofluoromethane, CCl₃F", "CCl<sub>3</sub>F", "C", ["F", "Cl", "Cl", "Cl"], [90, 180, 0, 270],
      source="Day 11 p.7–8 (Table 5.2)")
add(S("CH3Cl", "chloromethane, CH₃Cl", "CH<sub>3</sub>Cl", [("C", 1, 1), ("H", 1, 0), ("H", 0, 1), ("H", 1, 2), ("Cl", 2.1, 1)],
      [(0, 1, 1), (0, 2, 1), (0, 3, 1), (0, 4, 1)], {4: 3}, central=[0], source="new example"))
add(S("HF", "hydrogen fluoride, HF", "HF", [("H", 0, 0), ("F", 1.1, 0)], [(0, 1, 1)], {1: 3}, central=[],
      source="Day 11 p.8 (Table 5.2)"))
add(S("H2S", "hydrogen sulfide, H₂S", "H<sub>2</sub>S", [("S", 1, 0), ("H", 0, 0), ("H", 2, 0)],
      [(0, 1, 1), (0, 2, 1)], {0: 2}, central=[0], source="textbook §5.3 Concept Test, PDF p.246"))
add(S("OF2", "oxygen difluoride, OF₂", "OF<sub>2</sub>", [("O", 1, 0), ("F", 0, 0), ("F", 2, 0)],
      [(0, 1, 1), (0, 2, 1)], {0: 2, 1: 3, 2: 3}, central=[0], source="new example"))
add(S("NF3", "nitrogen trifluoride, NF₃", "NF<sub>3</sub>", [("N", 1, 0), ("F", 0, 0), ("F", 2, 0), ("F", 1, 1)],
      [(0, 1, 1), (0, 2, 1), (0, 3, 1)], {0: 1, 1: 3, 2: 3, 3: 3}, central=[0], source="new example"))
add(S("PH3", "phosphine, PH₃", "PH<sub>3</sub>", [("P", 1, 0), ("H", 0, 0), ("H", 2, 0), ("H", 1, 1)],
      [(0, 1, 1), (0, 2, 1), (0, 3, 1)], {0: 1}, central=[0], source="textbook §5.4 practice, PDF p.252"))
add(S("H3O+", "hydronium ion, H₃O⁺", "H<sub>3</sub>O<sup>+</sup>", [("O", 1, 0), ("H", 0, 0), ("H", 2, 0), ("H", 1, 1)],
      [(0, 1, 1), (0, 2, 1), (0, 3, 1)], {0: 1}, charge=1, central=[0], source="new example"))
# hybridization, sigma and pi (Day 11 p.17-26; textbook §5.4-5.5)
add(S("N2H2", "diazene, N₂H₂", "N<sub>2</sub>H<sub>2</sub>", [("N", 1, 0.6), ("N", 2.2, 0.6), ("H", 0.3, -0.2), ("H", 2.9, 1.4)],
      [(0, 1, 2), (0, 2, 1), (1, 3, 1)], {0: 1, 1: 1}, central=[0, 1], source="Day 11 p.22"))
add(S("acrolein", "acrolein, CH₂=CH–CH=O", "C<sub>3</sub>H<sub>4</sub>O",
      [("C", 1.0, 1.0), ("C", 2.1, 0.4), ("C", 3.2, 1.0), ("O", 4.3, 0.4), ("H", 0.2, 0.35), ("H", 0.2, 1.65), ("H", 2.1, -0.65), ("H", 3.2, 2.05)],
      [(0, 1, 2), (1, 2, 1), (2, 3, 2), (0, 4, 1), (0, 5, 1), (1, 6, 1), (2, 7, 1)], {3: 2}, central=[0, 1, 2],
      source="Day 11 p.26; textbook §5.5, PDF p.254"))
add(S("CH3CN", "acetonitrile, CH₃CN", "CH<sub>3</sub>CN",
      [("C", 1, 1), ("H", 1, 0), ("H", 0, 1), ("H", 1, 2), ("C", 2.2, 1), ("N", 3.4, 1)],
      [(0, 1, 1), (0, 2, 1), (0, 3, 1), (0, 4, 1), (4, 5, 3)], {5: 1}, central=[0, 4], source="new example"))
add(S("allene", "allene (propadiene), H₂C=C=CH₂", "C<sub>3</sub>H<sub>4</sub>",
      [("C", 0.9, 0.8), ("C", 2.1, 0.8), ("C", 3.3, 0.8), ("H", 0.2, 0.1), ("H", 0.2, 1.5), ("H", 4.0, 0.1), ("H", 4.0, 1.5)],
      [(0, 1, 2), (1, 2, 2), (0, 3, 1), (0, 4, 1), (2, 5, 1), (2, 6, 1)], {}, central=[0, 1, 2], source="new example"))
add(S("C2H6", "ethane, C₂H₆", "C<sub>2</sub>H<sub>6</sub>",
      [("C", 1, 1), ("C", 2.2, 1), ("H", 1, 0), ("H", 0, 1), ("H", 1, 2), ("H", 2.2, 0), ("H", 3.2, 1), ("H", 2.2, 2)],
      [(0, 1, 1), (0, 2, 1), (0, 3, 1), (0, 4, 1), (1, 5, 1), (1, 6, 1), (1, 7, 1)], {}, central=[0, 1], source="new example"))
add(S("HCOOH", "formic acid, HCOOH", "HCOOH",
      [("C", 1.2, 1.0), ("H", 1.2, -0.1), ("O", 0.1, 1.6), ("O", 2.3, 1.6), ("H", 3.3, 1.6)],
      [(0, 1, 1), (0, 2, 2), (0, 3, 1), (3, 4, 1)], {2: 2, 3: 2}, central=[0, 3], source="new example"))

# ---------------------------------------------------------------- per-author blocks (Extension 3, 2026-10-06)
# Each author adds structures only inside its own block, plus their ids to NON_OCTET_EXTRA (octet not complete
# on purpose) and EXPECT_EXTRA (independent SMILES and/or formal charges), so edits never touch the same lines.
NON_OCTET_EXTRA, EXPECT_EXTRA = set(), {}
# ==== block A (Day 9 Ch. 4 revision) start
# Day 9 p.15-18: the lecture's polar-bond examples (H-Cl under the battery; Cl2 on the potential-map scale)
add(S("HCl", "hydrogen chloride, HCl", "HCl", [("H", 0, 0), ("Cl", 1.25, 0)], [(0, 1, 1)], {1: 3}, central=[],
      source="Day 9 p.15–18"))
add(S("Cl2", "chlorine, Cl₂", "Cl<sub>2</sub>", [("Cl", 0, 0), ("Cl", 1.4, 0)], [(0, 1, 1)], {0: 3, 1: 3}, central=[],
      source="Day 9 p.16–18"))
# a new odd-electron example for t4-8 (Day 9 p.28: "radicals" or "free radicals")
add(S("CH3-rad", "methyl radical, CH₃", "CH<sub>3</sub>", [("C", 1, 1), ("H", 0, 1), ("H", 2, 1), ("H", 1, 2)],
      [(0, 1, 1), (0, 2, 1), (0, 3, 1)], {}, rad={0: 1}, central=[0], source="new example"))
NON_OCTET_EXTRA |= {"CH3-rad"}
EXPECT_EXTRA.update({"HCl": ("Cl", [0, 0]), "Cl2": ("ClCl", [0, 0]), "CH3-rad": ("[CH3]", [0, 0, 0, 0])})
# ==== block A end
# ==== block B (Ch. 5 §5.1-5.3) start
# new examples for the VSEPR and polarity problems (problem_bank_i.py); none is a Ch. 5 textbook example or exercise
add(S("COCl2", "phosgene, COCl₂", "COCl<sub>2</sub>", [("C", 1.2, 1.0), ("O", 1.2, -0.2), ("Cl", 0.1, 1.65), ("Cl", 2.3, 1.65)],
      [(0, 1, 2), (0, 2, 1), (0, 3, 1)], {1: 2, 2: 3, 3: 3}, central=[0], source="new example"))
add(S("NH2-", "amide ion, NH₂⁻", "NH<sub>2</sub><sup>−</sup>", [("N", 1, 0), ("H", 0, 0), ("H", 2, 0)],
      [(0, 1, 1), (0, 2, 1)], {0: 2}, charge=-1, central=[0], source="new example"))
_star("SeF4", "selenium tetrafluoride, SeF₄", "SeF<sub>4</sub>", "Se", ["F"] * 4, [90, 180, 0, 270], lp_center=1)
add(S("SF5Cl", "sulfur chloride pentafluoride, SF₅Cl", "SF<sub>5</sub>Cl",
      [("S", 1.2, 1.2), ("Cl", 1.2, 0), ("F", 1.2, 2.4), ("F", 0, 0.6), ("F", 2.4, 0.6), ("F", 0, 1.8), ("F", 2.4, 1.8)],
      [(0, k, 1) for k in range(1, 7)], {k: 3 for k in range(1, 7)}, central=[0], source="new example"))
add(S("SeF6", "selenium hexafluoride, SeF₆", "SeF<sub>6</sub>",
      [("Se", 1.2, 1.2), ("F", 1.2, 0), ("F", 1.2, 2.4), ("F", 0, 0.6), ("F", 2.4, 0.6), ("F", 0, 1.8), ("F", 2.4, 1.8)],
      [(0, k, 1) for k in range(1, 7)], {k: 3 for k in range(1, 7)}, central=[0], source="new example"))
_star("AlCl4-", "tetrachloroaluminate ion, AlCl₄⁻", "AlCl<sub>4</sub><sup>−</sup>", "Al", ["Cl"] * 4, [90, 180, 0, 270], charge=-1)
_star("BrF4-", "tetrafluorobromate ion, BrF₄⁻", "BrF<sub>4</sub><sup>−</sup>", "Br", ["F"] * 4, [90, 180, 0, 270], lp_center=2, charge=-1)
_star("ClF5", "chlorine pentafluoride, ClF₅", "ClF<sub>5</sub>", "Cl", ["F"] * 5, [90, 162, 18, 234, 306], lp_center=1)
add(S("KrF2", "krypton difluoride, KrF₂", "KrF<sub>2</sub>", [("F", 0, 0), ("Kr", 1.4, 0), ("F", 2.8, 0)],
      [(0, 1, 1), (1, 2, 1)], {0: 3, 1: 3, 2: 3}, central=[1], source="new example"))
add(S("PF3", "phosphorus trifluoride, PF₃", "PF<sub>3</sub>", [("P", 1, 0), ("F", 0, 0), ("F", 2, 0), ("F", 1, 1)],
      [(0, 1, 1), (0, 2, 1), (0, 3, 1)], {0: 1, 1: 3, 2: 3, 3: 3}, central=[0], source="new example"))
add(S("H2Se", "hydrogen selenide, H₂Se", "H<sub>2</sub>Se", [("Se", 1, 0), ("H", 0, 0), ("H", 2, 0)],
      [(0, 1, 1), (0, 2, 1)], {0: 2}, central=[0], source="new example"))
add(S("BH4-", "tetrahydroborate (borohydride) ion, BH₄⁻", "BH<sub>4</sub><sup>−</sup>",
      [("B", 1, 1), ("H", 0, 1), ("H", 2, 1), ("H", 1, 0), ("H", 1, 2)], [(0, 1, 1), (0, 2, 1), (0, 3, 1), (0, 4, 1)], {},
      charge=-1, central=[0], source="new example"))
add(S("CH3F", "fluoromethane, CH₃F", "CH<sub>3</sub>F", [("C", 1, 1), ("H", 1, 0), ("H", 0, 1), ("H", 1, 2), ("F", 2.1, 1)],
      [(0, 1, 1), (0, 2, 1), (0, 3, 1), (0, 4, 1)], {4: 3}, central=[0], source="new example"))
add(S("CH2F2", "difluoromethane, CH₂F₂", "CH<sub>2</sub>F<sub>2</sub>",
      [("C", 1, 1), ("H", 1, 0), ("H", 0, 1), ("F", 2, 1), ("F", 1, 2)], [(0, 1, 1), (0, 2, 1), (0, 3, 1), (0, 4, 1)],
      {3: 3, 4: 3}, central=[0], source="new example"))
add(S("CHF3", "trifluoromethane, CHF₃", "CHF<sub>3</sub>",
      [("C", 1, 1), ("F", 0, 1), ("F", 2, 1), ("H", 1, 0), ("F", 1, 2)], [(0, 1, 1), (0, 2, 1), (0, 3, 1), (0, 4, 1)],
      {1: 3, 2: 3, 4: 3}, central=[0], source="new example"))
NON_OCTET_EXTRA |= {"SeF4", "SF5Cl", "SeF6", "BrF4-", "ClF5", "KrF2"}
RDKIT_NO_VALENCE |= {"BrF4-", "ClF5", "KrF2"}     # hypervalent Br⁻, Cl, and Kr: RDKit's valence table has none
EXPECT_EXTRA.update({"COCl2": ("O=C(Cl)Cl", [0, 0, 0, 0]), "NH2-": ("[NH2-]", [-1, 0, 0]),
                     "SeF4": (None, [0] * 5), "SF5Cl": ("FS(F)(F)(F)(F)Cl", [0] * 7), "SeF6": (None, [0] * 7),
                     "AlCl4-": ("Cl[Al-](Cl)(Cl)Cl", [-1, 0, 0, 0, 0]), "BrF4-": (None, [-1, 0, 0, 0, 0]),
                     "ClF5": (None, [0] * 6), "KrF2": (None, [0, 0, 0]), "PF3": ("FP(F)F", [0] * 4),
                     "H2Se": ("[SeH2]", [0, 0, 0]), "BH4-": ("[BH4-]", [-1, 0, 0, 0, 0]), "CH3F": ("CF", None),
                     "CH2F2": ("FCF", None), "CHF3": ("FC(F)F", None)})
# ==== block B end
# ==== block C (Ch. 5 §5.4-5.5) start
# m24 transfer problem: CH3-N=C=O (sp3 C, sp2 N, sp C, sp2 O), drawn with N=C=O straight as an sp carbon requires
add(S("CH3NCO", "methyl isocyanate, CH₃–N=C=O", "CH<sub>3</sub>NCO",
      [("C", 1.0, 1.0), ("N", 2.1, 0.4), ("C", 3.3, 0.4), ("O", 4.5, 0.4), ("H", 0.2, 0.35), ("H", 0.2, 1.65), ("H", 1.0, 2.0)],
      [(0, 1, 1), (1, 2, 2), (2, 3, 2), (0, 4, 1), (0, 5, 1), (0, 6, 1)], {1: 1, 3: 2}, central=[0, 1, 2], source="new example"))
EXPECT_EXTRA["CH3NCO"] = ("CN=C=O", [0] * 7)
# m24 attempt: methanimine H2C=NH, formaldehyde's N analog (sp2 C, sp2 N with its lone pair)
add(S("CH2NH", "methanimine, H₂C=NH", "CH<sub>2</sub>NH",
      [("C", 1.0, 0.6), ("N", 2.2, 0.6), ("H", 0.3, -0.2), ("H", 0.3, 1.4), ("H", 2.9, 1.4)],
      [(0, 1, 2), (0, 2, 1), (0, 3, 1), (1, 4, 1)], {1: 1}, central=[0, 1], source="new example"))
EXPECT_EXTRA["CH2NH"] = ("C=N", [0] * 5)
# ==== block C end
# ==== block D (Ch. 5 §5.6-5.7) start
# §5.6 chirality: the textbook's chiral/achiral pair (Fig. 5.40) and a new example with a stereocenter (C2)
_star("CHBrClF", "bromochlorofluoromethane, CHBrClF", "CHBrClF", "C", ["H", "Br", "Cl", "F"], [90, 180, 0, 270],
      source="textbook §5.6 Fig. 5.40, PDF p.257")
_star("CHBr2Cl", "dibromochloromethane, CHBr₂Cl", "CHBr<sub>2</sub>Cl", "C", ["H", "Br", "Cl", "Br"], [90, 180, 0, 270],
      source="textbook §5.6 Fig. 5.40, PDF p.257")
add(S("2-butanol", "2-butanol, CH₃CH(OH)CH₂CH₃", "C<sub>4</sub>H<sub>10</sub>O",
      [("C", 1.0, 1.2), ("C", 2.2, 1.2), ("C", 3.4, 1.2), ("C", 4.6, 1.2), ("O", 2.2, 0.0), ("H", 2.2, -1.0), ("H", 2.2, 2.2),
       ("H", 0.0, 1.2), ("H", 1.0, 0.2), ("H", 1.0, 2.2), ("H", 3.4, 0.2), ("H", 3.4, 2.2), ("H", 5.6, 1.2), ("H", 4.6, 0.2),
       ("H", 4.6, 2.2)],
      [(0, 1, 1), (1, 2, 1), (2, 3, 1), (1, 4, 1), (4, 5, 1), (1, 6, 1), (0, 7, 1), (0, 8, 1), (0, 9, 1), (2, 10, 1),
       (2, 11, 1), (3, 12, 1), (3, 13, 1), (3, 14, 1)], {4: 2}, central=[0, 1, 2, 3, 4], source="new example"))
# §5.7: a diatomic ion whose MO bond order matches its Lewis structure (new example, the t5-7 transfer)
add(S("CN-", "cyanide ion, CN⁻", "CN<sup>−</sup>", [("C", 0, 0), ("N", 1.2, 0)], [(0, 1, 3)], {0: 1, 1: 1}, charge=-1,
      central=[], source="new example"))
EXPECT_EXTRA.update({
    "CHBrClF": ("FC(Cl)Br", [0] * 5), "CHBr2Cl": ("ClC(Br)Br", [0] * 5), "2-butanol": ("CCC(C)O", [0] * 15),
    "CN-": ("[C-]#N", [-1, 0]),
})
# ==== block D end
# ==== block E (integration, mixed review) start
add(S("NCl3", "nitrogen trichloride, NCl₃", "NCl<sub>3</sub>", [("N", 1, 0), ("Cl", 0, 0), ("Cl", 2, 0), ("Cl", 1, 1)],
      [(0, 1, 1), (0, 2, 1), (0, 3, 1)], {0: 1, 1: 3, 2: 3, 3: 3}, central=[0], source="new example"))
EXPECT_EXTRA["NCl3"] = ("ClN(Cl)Cl", [0, 0, 0, 0])
# ==== block E end

# structures whose octets are deliberately not all complete
NON_OCTET = {"BF3", "BeCl2", "NO", "NO2-rad1", "NO2-rad2", "PCl5", "SF6", "SO4-exp", "PO4-exp", "H2SO4", "SO3-exp", "BrF5",
             "AlCl3", "BCl3", "H3PO4-t1", "H3PO4-t3", "PF5", "SF4", "SCl4", "ClF3", "BrF3", "XeF2", "XeF4", "IF5", "I3-",
             "ICl4-", "SO2-exp"} | NON_OCTET_EXTRA

# What each structure should look like, independently of the definitions above: RDKit canonical SMILES and
# formal charges (textbook values where the textbook prints them).
EXPECT = {
    "O3a": ("[O-][O+]=O", None), "O3b": ("[O-][O+]=O", None),
    "N2O-A": (None, [0, 1, -1]), "N2O-B": (None, [-1, 1, 0]), "N2O-C": (None, [-2, 1, 1]),   # TB PDF p.210
    "CO2-alt1": (None, [1, 0, -1]), "CO2-alt2": (None, [-1, 0, 1]),                           # TB PDF p.211
    "NO2-rad1": (None, [0, 1, -1]),                                                           # TB PDF p.213
    "SO4-oct": (None, [2, -1, -1, -1, -1]), "SO4-exp": (None, [0, 0, -1, -1, 0]),             # TB PDF p.215
    "PO4-oct": (None, [1, -1, -1, -1, -1]), "PO4-exp": (None, [0, 0, -1, -1, -1]),            # TB PDF p.216
    "C6H6-1": ("c1ccccc1", None), "C6H6-2": ("c1ccccc1", None),
    "HCO2-1": ("O=C[O-]", None), "HCO2-2": ("O=C[O-]", None),
    "HCO3-1": ("O=C([O-])O", [0, 0, -1, 0, 0]), "HCO3-2": ("O=C([O-])O", [0, -1, 0, 0, 0]),
    "CH3COO-1": ("CC(=O)[O-]", None), "CH3COO-2": ("CC(=O)[O-]", None),
    "HOCl": ("OCl", [0, 0, 0]), "CS2": ("S=C=S", [0, 0, 0]), "CS2-alt": (None, [1, 0, -1]),
    "N2H4": ("NN", None), "BrF5": (None, [0, 0, 0, 0, 0, 0]),
    # Day 9 and Ch. 5 additions: connectivity from SMILES written independently of the definitions above
    "AlCl3": ("Cl[Al](Cl)Cl", [0, 0, 0, 0]), "BCl3": ("ClB(Cl)Cl", [0, 0, 0, 0]),
    "H3PO4-t1": (None, [0, -1, 0, 0, 1, 0, 0, 0]), "H3PO4-t2": (None, [1, -1, 0, 0, 0, 0, 0, 0]),
    "H3PO4-t3": ("O=P(O)(O)O", [0, 0, 0, 0, 0, 0, 0, 0]),
    "CCl4": ("ClC(Cl)(Cl)Cl", None), "CF4": ("FC(F)(F)F", None), "PF5": (None, [0] * 6),
    "SF4": (None, [0] * 5), "SCl4": (None, [0] * 5), "ClF3": (None, [0] * 4), "BrF3": (None, [0] * 4),
    "XeF2": (None, [0, 0, 0]), "XeF4": (None, [0] * 5), "IF5": (None, [0] * 6),
    "I3-": (None, [0, -1, 0]), "ICl4-": (None, [-1, 0, 0, 0, 0]),
    "SO2-1": ("O=[S+][O-]", [0, 1, -1]), "SO2-2": ("O=[S+][O-]", [-1, 1, 0]), "SO2-exp": ("O=S=O", [0, 0, 0]),
    "CH2Cl2": ("ClCCl", None), "CCl3F": ("FC(Cl)(Cl)Cl", None), "CH3Cl": ("CCl", None), "HF": ("F", None),
    "H2S": ("S", None), "OF2": ("FOF", None), "NF3": ("FN(F)F", None), "PH3": ("P", None), "H3O+": ("[OH3+]", [1, 0, 0, 0]),
    "N2H2": ("N=N", None), "acrolein": ("C=CC=O", None), "CH3CN": ("CC#N", None), "allene": ("C=C=C", None),
    "C2H6": ("CC", None), "HCOOH": ("O=CO", None),
}
EXPECT.update(EXPECT_EXTRA)


def check_all(verbose=True):
    errs, rows = [], []
    for sid, s in STRUCTS.items():
        e = s.check(expect_octets=sid not in NON_OCTET)
        errs += e
        try:
            smi, formula, q = s.rdkit_check()
        except Exception as ex:                    # noqa: BLE001
            errs.append(f"{sid}: RDKit rejected the structure ({ex})")
            continue
        if q != s.charge:
            errs.append(f"{sid}: RDKit charge {q} vs. {s.charge}")
        ex_smi, ex_fc = EXPECT.get(sid, (None, None))
        if ex_fc is not None and s.fcs() != ex_fc:
            errs.append(f"{sid}: formal charges {s.fcs()} vs. textbook {ex_fc}")
        if ex_smi is not None:
            from rdkit import Chem
            if Chem.CanonSmiles(ex_smi) != Chem.CanonSmiles(smi):
                errs.append(f"{sid}: SMILES {smi} vs. expected {ex_smi}")
        rows.append((sid, s.total_valence(), formula, smi, s.fcs()))
    if verbose:
        for r in rows:
            print(f"{r[0]:10s} {r[1]:3d} e⁻  {r[2]:10s} {r[3]:22s} FC {r[4]}")
        print("errors:", errs if errs else "none")
    return errs


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(1 if check_all() else 0)

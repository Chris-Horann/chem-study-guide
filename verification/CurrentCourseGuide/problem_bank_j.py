"""Problem bank J: Ch. 5 §5.4-5.5: valence bond theory, hybrid orbitals, sigma and pi bonds, molecules with several
central atoms (Day 11 p.9-26; textbook §5.4-5.5, PDF p.246-255).
m23 valence bond theory and hybrid orbitals; m24 pi bonds and molecules with several central atoms.

Every key is computed from the checked lewis.py structures: steric number = bonded atoms + lone pairs (Day 10 p.9,
p.16; textbook Eq. 5.1), hybridization from SN (Table 5.3, Day 11 p.24), sigma bonds = bonded pairs, pi bonds = the
extra shared pairs of double and triple bonds (Day 11 p.17, p.20, p.23), box occupancies from lone pairs, sigma and pi
bonds. check_problem_bank_j.py re-derives every hybridization and sigma/pi count with RDKit from independent SMILES.
Choice items are written correct-option-first and rotated at the end (balanced_spread, below); the sp / sp2 / sp3
option lists keep their natural order."""
import math

from guide_common import *                                              # noqa: F401,F403
from problem_bank_a import PROBLEMS, add, num_ans, choice, KJMOL_UNITS  # noqa: F401
from problem_bank_b import text_ans, formula_ans, order_ans           # noqa: F401
from problem_bank_c import P, tb                                       # noqa: F401
from problem_bank_e import X                                           # noqa: F401
from problem_bank_f import LS, LX, tname, tformula, tnum, names        # noqa: F401
import problem_bank_g                                                  # noqa: F401  (Ch. 4 banks load first)
import choice_order
import lewis as LW

J_START = len(PROBLEMS)

TET = math.degrees(math.acos(-1 / 3))           # angle between sp3 hybrids, 109.47°
assert abs(TET - 109.47) < 0.01
HYB = {2: "sp", 3: "sp<sup>2</sup>", 4: "sp<sup>3</sup>"}
HYB_TXT = {2: "sp", 3: "sp²", 4: "sp³"}         # for <option> text and aria-labels, which can't hold markup
ANGLE = {2: 180.0, 3: 120.0, 4: TET}
RES = "<span class='lw-arrow' role='img' aria-label='resonance arrow'>↔</span>"


# ------------------------------------------------------------------ valence-bond bookkeeping from lewis.py
def neighbors(s, k):
    return [j if i == k else i for i, j, _ in s.bonds if k in (i, j)]


def steric(sid, k):
    """steric number of atom k: bonded atoms + lone pairs; a multiple bond counts once (Day 10 p.9-10, p.16)."""
    s = LW.STRUCTS[sid]
    return len(neighbors(s, k)) + s.lp.get(k, 0)


def sigma_pi(sid):
    """(sigma, pi) for a whole structure: one sigma per bonded pair, the extra pairs of multiple bonds are pi."""
    s = LW.STRUCTS[sid]
    return len(s.bonds), sum(o - 1 for _, _, o in s.bonds)


def atom_pi(sid, k):
    s = LW.STRUCTS[sid]
    return sum(o - 1 for i, j, o in s.bonds if k in (i, j))


def boxes(sid, k):
    """Valence-bond box occupancy of atom k: hybrids (2 per lone pair, then 1 per sigma bond) and unhybridized
    p orbitals (1 per pi bond, the rest empty). The electrons must add up to the atom's valence electrons."""
    s = LW.STRUCTS[sid]
    sn = steric(sid, k)
    hy = [2] * s.lp.get(k, 0) + [1] * len(neighbors(s, k))
    npi = atom_pi(sid, k)
    p = [1] * npi + [0] * (4 - sn - npi)
    assert len(hy) == sn and min(p, default=0) >= 0
    assert sum(hy) + sum(p) == LW.VALENCE[s.atoms[k][0]] - s.fc(k), (sid, k)
    return hy, p


def ground(el):
    """(n, 2s electrons, 2p occupancy) of a free main-group atom, Hund's rule in the p boxes (Day 6)."""
    v = LW.VALENCE[el]
    n = 2 if el in ("Be", "B", "C", "N", "O", "F") else 3
    s_e = min(v, 2)
    p = [0, 0, 0]
    for i in range(v - s_e):
        p[i % 3] += 1
    return n, s_e, sorted(p, reverse=True)


def _cells(occ):
    return "".join(f"<span class='obox'>{'↑↓' if x == 2 else '↑' if x == 1 else ''}</span>" for x in occ)


def _ladder(rows, caption):
    """rows top (higher energy) first: [(label_html, occupancy)]"""
    body = "".join(f"<div class='cfg-row'><span class='sub-label'>{lab}</span>{_cells(occ)}</div>" for lab, occ in rows)
    return f"<div class='cfg-ladder'>{body}<p class='xp-caption'>{caption}</p></div>"


def _words(occ):
    return ", ".join({2: "a pair", 1: "one electron", 0: "empty"}[x] for x in occ)


def box_diagram(sid, k):
    """The slides' box diagram (Day 11 p.13, p.16, p.18, p.22-23): ground-state atom → hybrids + unhybridized p."""
    s = LW.STRUCTS[sid]
    el = s.atoms[k][0]
    assert s.fc(k) == 0, "box diagrams start from the neutral atom"
    n, s_e, p0 = ground(el)
    hy, p = boxes(sid, k)
    sn = steric(sid, k)
    left = _ladder([(f"{n}p", p0), (f"{n}s", [s_e])], f"{el} atom")
    right = _ladder(([("p", p)] if p else []) + [(HYB[sn], hy)], f"{HYB[sn]}-hybridized {el}")
    aria = (f"{el} before hybridizing: {n}s {_words([s_e])}; {n}p {_words(p0)}. After: {len(hy)} {HYB_TXT[sn]} hybrids "
            f"({_words(hy)})" + (f" and {len(p)} unhybridized p ({_words(p)})" if p else "") + ".")
    return f"<div class='lw-row' role='img' aria-label='{aria}'>{left}<span class='lw-arrow'>→</span>{right}</div>"


def hyb_choice(sn, fb, none_fb=None):
    """sp / sp2 / sp3 in their natural order (kept by the rotation), optional 4th option 'unhybridized'."""
    opts = [(HYB[n], n == sn, fb[n]) for n in (2, 3, 4)]
    if none_fb:
        opts.append(none_fb)
    c = choice(*opts)
    c["_natural"] = True
    return c


HYB_OPTIONS = [{"key": "sp", "html": "sp"}, {"key": "sp2", "html": "sp²"}, {"key": "sp3", "html": "sp³"}]
HYB_KEY = {2: "sp", 3: "sp2", 4: "sp3"}


def hyb_match(rows):
    """rows: [(html, structure id, atom index)] → match answer keyed by each atom's steric number."""
    return {"type": "match", "rows": [{"html": h, "answer": HYB_KEY[steric(sid, k)]} for h, sid, k in rows],
            "options": HYB_OPTIONS}


# =====================================================================================
# m23  Valence bond theory and hybrid orbitals (Day 11 p.9-16, p.20, p.24; textbook §5.4, PDF p.246-253)
# =====================================================================================
SN_H3O = steric("H3O+", 0)
HY_H3O, P_H3O = boxes("H3O+", 0)                       # O brings 6 − 1 = 5 electrons (the ion's + charge)
assert (SN_H3O, sum(HY_H3O), HY_H3O.count(2), P_H3O) == (4, 5, 1, [])
H3O_BOXES = ("<div class='lw-row' role='img' aria-label='O in H₃O⁺: four sp³ hybrids holding a pair, one electron, one electron, one electron.'>"
             + _ladder([(HYB[4], HY_H3O)], "sp<sup>3</sup>-hybridized O in H<sub>3</sub>O<sup>+</sup>") + "</div>")
add(id="m23-attempt", module="m23", kind="attempt", level="Guided attempt",
    prompt="<p>Day 11 p.16 builds NH<sub>3</sub> and H<sub>2</sub>O from hybrid orbitals. Do the same for the hydronium ion, H<sub>3</sub>O<sup>+</sup>.</p>"
           "<p class='lw-row'>" + LS("H3O+", scale=0.8) + "</p>"
           "<p>(a) What is the steric number of O? (b) What is O's hybridization? (c) Count O as the atom that carries the ion's + charge (its formal charge is +1). How many electrons does it put into its hybrid orbitals? "
           "(d) How many of those hybrids hold a lone pair? (e) Which orbitals overlap head-on to make each O–H σ bond?</p>",
    answer={"type": "multi", "parts": [
        {"label": "(a) steric number of O", **tnum(SN_H3O, traps=[(3, "That counts only the three bonded H atoms. O's lone pair is an electron domain too: SN = atoms + lone pairs (Day 10 p.16).")])},
        {"label": "(b) hybridization of O", **hyb_choice(SN_H3O, {
            2: "sp is for SN 2, two electron domains.",
            3: "sp<sup>2</sup> is for SN 3. This O has four domains: three bonds and a lone pair.",
            4: "Right: SN 4 → four hybrids, made from the 2s and all three 2p orbitals: sp<sup>3</sup> (Day 11 p.16, p.24)."},
            none_fb=("none: O bonds with three half-filled 2p orbitals", False,
                     "That picture puts the three O–H bonds at 90° to one another. With four electron domains, the O mixes all four valence orbitals into sp<sup>3</sup> hybrids, as N does in NH<sub>3</sub> (Day 11 p.16)."))},
        {"label": "(c) electrons in O's hybrids", **tnum(sum(HY_H3O), traps=[
            (6, "O has 6 valence electrons, but the ion's + charge means one electron is gone: 6 − 1 = 5."),
            (8, "Count only O's own electrons. The three H atoms bring their electrons when the bonds form.")])},
        {"label": "(d) hybrids holding a lone pair", **tnum(HY_H3O.count(2), traps=[
            (2, "Two lone-pair hybrids is neutral H<sub>2</sub>O. Here O has 5 electrons, three of them used singly for the three O–H bonds."),
            (0, "Five electrons in four hybrids: one hybrid has to hold two.")])},
        {"label": "(e) each O–H σ bond is the overlap of", **choice(
            ("an O sp<sup>3</sup> hybrid and an H 1s orbital", True, "Right: σ bonds come from head-on overlap of hybrid orbitals, and H uses its 1s (Day 11 p.20)."),
            ("an O 2p orbital and an H 1s orbital", False, "That's the unhybridized picture, which puts the bonds at 90°. In the hybrid picture, all three 2p orbitals are mixed into the sp<sup>3</sup> set."),
            ("an O sp<sup>3</sup> hybrid and an H sp<sup>3</sup> hybrid", False, "H doesn't hybridize: “Exception: Hydrogen uses a 1s orbital to make bonds” (Day 11 p.20)."),
            ("an O sp<sup>3</sup> hybrid holding a lone pair and an H 1s orbital", False, "The lone pair is the one hybrid that does not bond. Each bond uses a half-filled hybrid, one electron from O and one from H."))}]},
    hints=["Valence bond theory: a covalent bond forms when half-filled orbitals on two atoms overlap (Day 11 p.9). To match the shapes VSEPR predicts, the atom first mixes its valence orbitals into hybrid orbitals.",
           "The counting rule: one hybrid orbital for every electron domain, so the number of hybrids equals the steric number (Day 11 p.12). SN 2 → sp, SN 3 → sp<sup>2</sup>, SN 4 → sp<sup>3</sup> (Table 5.3, Day 11 p.24).",
           "H<sub>3</sub>O<sup>+</sup>'s Lewis structure has three O–H bonds and one lone pair on O. Each is one electron domain. For the electrons, start from O's 6 valence electrons and account for the + charge.",
           "SN 4 → four sp<sup>3</sup> hybrids from O's 2s and three 2p orbitals. O brings 6 − 1 = 5 electrons: [↑↓][↑][↑][↑]. The three single electrons pair up with the electrons of three H atoms."],
    solution=H3O_BOXES +
             f"<p>(a) <strong>{SN_H3O}</strong> (three atoms + one lone pair). (b) <strong>sp<sup>3</sup></strong>. (c) <strong>{sum(HY_H3O)}</strong>: O's 6 valence electrons minus 1 for the + charge. "
             f"(d) <strong>{HY_H3O.count(2)}</strong>, the lone pair. (e) Each O–H σ bond is the head-on overlap of a half-filled <strong>O sp<sup>3</sup></strong> hybrid with an <strong>H 1s</strong> orbital.</p>"
             "<p>Another way to count gives the same picture: start from water's diagram (O's 6 electrons, two lone pairs) and let an H<sup>+</sup>, which brings no electron, bond to one lone-pair hybrid. "
             "Either way the ion ends with three O–H bonds and one lone pair.</p>"
             "<p>The box diagram matches NH<sub>3</sub>'s N exactly (Day 11 p.16): H<sub>3</sub>O<sup>+</sup> and NH<sub>3</sub> have the same number of electrons, three σ bonds, and one lone pair, "
             "so the hydronium ion is trigonal pyramidal too.</p>",
    compare={"wrong": "<p>“O has 6 valence electrons, so its four sp<sup>3</sup> hybrids are [↑↓][↑↓][↑][↑], just like water's, with two lone pairs.”</p>",
             "tempting": "It's exactly the water diagram on Day 11 p.16, and O really does have 6 valence electrons.",
             "fails": "It keeps two lone pairs, but H<sub>3</sub>O<sup>+</sup>'s Lewis structure has only one: one of water's lone pairs has become the third O–H bond. "
                      "Counted from O<sup>+</sup> (6 − 1 = 5 electrons), the hybrids are [↑↓][↑][↑][↑]: three half-filled hybrids for the three bonds and one lone pair, the same pattern as N in NH<sub>3</sub> (Day 11 p.16). "
                      "Counted from water instead, the H<sup>+</sup> brings no electron and bonds to one lone-pair hybrid, which gives the same result."},
    source="Day 11 p.12, p.16, p.20, p.24; Day 10 p.16")

add(id="m23-p1", module="m23", kind="practice", level="Warm-up",
    prompt="<p>Day 11 p.10 introduces the σ bond, and p.15 builds methane from four of them. (a) Which description fits a σ bond? "
           "(b) In CH<sub>4</sub>, which orbitals overlap to make each C–H σ bond?</p>",
    answer={"type": "multi", "parts": [
        {"label": "(a) a σ bond is", **choice(
            ("a covalent bond with its highest electron density between the two atoms, along the bond axis", True, "Right: the definition on Day 11 p.10."),
            ("a covalent bond with its electron density greatest above and below the bond axis", False, "That's a π bond (Day 11 p.17)."),
            ("a bond in which one atom gives an electron to the other", False, "That's electron transfer, the ionic picture (Day 7 p.14). A σ bond is a shared pair."),
            ("a bond that only two H atoms can form", False, "The slide's example is H–H, but every single bond is a σ bond: C–H, N–H, C–C, and so on."))},
        {"label": "(b) each C–H bond in CH<sub>4</sub> is the overlap of", **choice(
            ("a C sp<sup>3</sup> hybrid and an H 1s orbital", True, "Right (Day 11 p.15): four equivalent sp<sup>3</sup>–1s overlaps."),
            ("a C 2p orbital and an H 1s orbital, for all four bonds", False, "C has only three 2p orbitals, and they're 90° apart. Methane's four bonds are 109.5° apart."),
            ("a C 2s orbital for one bond and C 2p orbitals for the other three", False, "That's the promoted-electron picture the professor rejects: its four bonds wouldn't be equivalent (Day 11 p.11)."),
            ("a C sp<sup>3</sup> hybrid and an H sp<sup>3</sup> hybrid", False, "H uses its 1s orbital (Day 11 p.20)."))}]},
    hints=["(a) The H–H example on Day 11 p.10 is labeled “Overlap = σ bond.” Where is the overlap?",
           "(b) Carbon has SN 4 in CH<sub>4</sub>, “so we want 4 hybridized orbitals” (Day 11 p.13). Which orbital does each H bring?"],
    solution="<p>(a) A σ bond is “a covalent bond in which the highest electron density lies between the two atoms along the bond axis” (Day 11 p.10). "
             "(b) <strong>C sp<sup>3</sup> + H 1s</strong>: carbon's four sp<sup>3</sup> hybrids each hold one electron and point to the corners of a tetrahedron, 109.5° apart, "
             "and each overlaps head-on with one H 1s orbital (Day 11 p.13, p.15).</p>",
    source="Day 11 p.10, p.13, p.15")

add(id="m23-p2", module="m23", kind="practice", level="Warm-up",
    prompt="<p>A second-period atom has a steric number of 3. (a) How many hybrid orbitals does it form? (b) How many of its 2p orbitals are left unhybridized?</p>",
    answer={"type": "multi", "parts": [
        {"label": "(a) hybrid orbitals", **tnum(3, traps=[(4, "Four hybrids is sp<sup>3</sup>, for SN 4. Make one hybrid per electron domain (Day 11 p.12).")])},
        {"label": "(b) unhybridized 2p orbitals", **tnum(4 - 3, traps=[
            (0, "Three hybrids use only three of the four valence orbitals (2s and two 2p), so one 2p is left over (Day 11 p.18)."),
            (2, "Two unhybridized p orbitals belong to an sp atom, with SN 2 (Day 11 p.23).")])}]},
    hints=["“The number of hybridized orbitals equals the steric number of the atom” (Day 11 p.12).",
           "“The number of valence atomic orbitals combined equals the number of hybrid orbitals created” (Day 11 p.20). A second-period atom has four valence orbitals: 2s and three 2p."],
    solution="<p>(a) <strong>3</strong> hybrids, called sp<sup>2</sup> because they're made from one s and two p orbitals. (b) <strong>1</strong> unhybridized 2p orbital, perpendicular to the plane of the three hybrids. "
             "The formaldehyde slide shows exactly this: “Three sp<sup>2</sup> hybrid orbitals” plus “One unhybridized p orbital” (Day 11 p.18). That leftover p orbital is what makes a π bond (<a href='#m24'>§5.4–5.5</a>).</p>",
    source="Day 11 p.12, p.18, p.20")

add(id="m23-p3", module="m23", kind="practice", level="Concept",
    prompt="<p>Day 11 p.11: “Methane only has <strong>two</strong> unpaired electrons, so how can it make <strong>four</strong> sigma bonds? One suggestion is that it could promote an electron from 2s to 2p, "
           "producing four unpaired electrons. But that's not what methane <strong>looks</strong> like!” What's wrong with the promotion picture?</p>",
    answer=choice(("Its four unpaired electrons would sit in one 2s and three 2p orbitals, so the four C–H bonds wouldn't all be alike, and three of them would be 90° apart. Methane has four equivalent bonds pointing to the corners of a tetrahedron.", True,
                   "Right: “We need four equivalent bonds pointing to the vertices of a tetrahedron!” (Day 11 p.11). Mixing the four orbitals into four sp<sup>3</sup> hybrids gives exactly that."),
                  ("Promoting an electron takes energy, so it can't happen.", False,
                   "The slide doesn't argue about energy. Its objection is shape: the bonds that promotion predicts don't look like methane's."),
                  ("Carbon's ground state already has four unpaired electrons, so no promotion is needed.", False,
                   "Ground-state carbon is 2s<sup>2</sup>2p<sup>2</sup>: the 2s electrons are paired, leaving two unpaired 2p electrons (the slide's “Ground state” diagram)."),
                  ("Promotion would turn carbon into an ion.", False,
                   "Moving an electron from 2s to 2p within the same atom doesn't change its charge.")),
    hints=["Picture the bonds a promoted carbon would make: one from a spherical 2s orbital and three from 2p orbitals at right angles to each other."],
    solution="<p>Promotion gives four unpaired electrons, but in four <em>different</em> orbitals: one spherical 2s and three 2p orbitals at 90° to one another. "
             "Bonds made from them would be one of one kind and three of another, with 90° angles. Methane's four bonds are identical and 109.5° apart, so the professor rejects it: "
             "“We need four equivalent bonds pointing to the vertices of a tetrahedron!” (Day 11 p.11). Pauling's answer is hybridization: mix (“average”) the 2s and the three 2p orbitals "
             "into four equivalent sp<sup>3</sup> hybrids (Day 11 p.12–13).</p>"
             "<p class='note'>“Methane only has two unpaired electrons” means the carbon atom in its ground state, 2s<sup>2</sup>2p<sup>2</sup>, as the slide's diagram shows. The CH<sub>4</sub> molecule itself has no unpaired electrons.</p>",
    source="Day 11 p.11–13; " + tb("5.4", 247))

add(id="m23-p4", module="m23", kind="practice", level="Concept",
    prompt="<p>Which statement breaks one of the rules on Day 11 p.20?</p>",
    answer=choice(("The lone pair on N in NH<sub>3</sub> sits in an unhybridized 2p orbital.", True,
                   "Right, it breaks the last rule: “Lone pairs always reside in hybrid orbitals.” N's lone pair is in one of its four sp<sup>3</sup> hybrids (Day 11 p.16)."),
                  ("Each H in CH<sub>4</sub> uses its 1s orbital to make its σ bond.", False,
                   "That's the rules' stated exception: “Hydrogen uses a 1s orbital to make bonds”."),
                  ("An atom with SN 3 combines three atomic orbitals into three hybrid orbitals.", False,
                   "That follows the rules: one hybrid per electron domain, and “The number of valence atomic orbitals combined equals the number of hybrid orbitals created.”"),
                  ("A σ bond forms by head-on overlap of hybrid orbitals.", False,
                   "That's the rule for σ bonds: “σ bonds involve head-on overlap of hybrid orbitals.”")),
    hints=["Test each statement against the rules on Day 11 p.20, one rule at a time."],
    solution="<p>The rules on Day 11 p.20, word for word:</p><ul class='steps'><li>“Each electron domain on the central atom requires one hybrid orbital.”</li>"
             "<li>“The number of valence atomic orbitals combined equals the number of hybrid orbitals created.”</li>"
             "<li>“σ bonds involve head-on overlap of hybrid orbitals. Exception: Hydrogen uses a 1s orbital to make bonds”</li>"
             "<li>“π bonds always result from side-to-side overlap of unhybridized orbitals.”</li>"
             "<li>“Lone pairs always reside in hybrid orbitals.”</li></ul>"
             "<p>A lone pair in an unhybridized 2p orbital breaks the last one.</p>",
    source="Day 11 p.16, p.20")

# The O of methanol, not water: water's O is worked in the module's own table and in the m23-attempt compare panel,
# so asking about water here would be a give-away. Same pattern (2 bonded atoms + 2 lone pairs), same key values.
O_MEOH = next(k for k, a in enumerate(LW.STRUCTS["CH3OH"].atoms) if a[0] == "O")
SN_MEOH = steric("CH3OH", O_MEOH)
HY_MEOH, _ = boxes("CH3OH", O_MEOH)
assert (SN_MEOH, HY_MEOH) == (4, [2, 2, 1, 1]) and (SN_MEOH, HY_MEOH) == (steric("H2O", 0), boxes("H2O", 0)[0])
add(id="m23-p5", module="m23", kind="practice", level="Standard",
    prompt="<p>Day 11 p.16 hybridizes the O atom in water. Do the same for the O atom in methanol, CH<sub>3</sub>OH, which is bonded to the C and to one H.</p>"
           "<p class='lw-row'>" + LS("CH3OH", scale=0.8) + "</p>"
           "<p>(a) What is O's steric number? (b) How many of O's sp<sup>3</sup> hybrids hold a lone pair? "
           "(c) How many hold one electron, ready to form a σ bond? (d) How many electrons are in O's four sp<sup>3</sup> hybrids altogether?</p>",
    answer={"type": "multi", "parts": [
        {"label": "(a) steric number of O", **tnum(SN_MEOH, traps=[(2, "That counts only the two bonded atoms, C and H. Add O's two lone pairs.")])},
        {"label": "(b) hybrids with a lone pair", **tnum(HY_MEOH.count(2))},
        {"label": "(c) hybrids with one electron", **tnum(HY_MEOH.count(1))},
        {"label": "(d) electrons in the four hybrids", **tnum(sum(HY_MEOH), traps=[
            (8, "Count only O's own electrons: the hybrids hold O's valence electrons. The C and the H bring theirs when the bonds form."),
            (4, "O is in group 16: 6 valence electrons.")])}]},
    hints=["Methanol's O has two bonds, one to the C and one to the H, and two lone pairs. Each is an electron domain.",
           "SN 4 → four sp<sup>3</sup> hybrids. Put O's 6 valence electrons in them, pairing only when you must, as Day 11 p.16 does for the O in water."],
    solution=box_diagram("CH3OH", O_MEOH) +
             f"<p>(a) <strong>{SN_MEOH}</strong>. (b) <strong>{HY_MEOH.count(2)}</strong>, the lone pairs. (c) <strong>{HY_MEOH.count(1)}</strong>: one overlaps head-on with an sp<sup>3</sup> hybrid "
             "of the C (the C, with four bonded atoms, is sp<sup>3</sup> too), and the other with the H 1s orbital. "
             f"(d) <strong>{sum(HY_MEOH)}</strong>, all of O's valence electrons: hybridizing rearranges an atom's electrons; it doesn't add or remove any.</p>"
             "<p>The diagram is the one Day 11 p.16 draws for the O in water: an O with two bonded atoms and two lone pairs fills its sp<sup>3</sup> hybrids "
             "[↑↓][↑↓][↑][↑], whatever the two atoms are.</p>",
    source="Day 11 p.16, p.20")

M23_P6 = [("CH<sub>4</sub>", "CH4", 0), ("NH<sub>4</sub><sup>+</sup>", "NH4+", 0), ("NF<sub>3</sub>", "NF3", 0),
          ("PCl<sub>3</sub>", "PCl3", 0), ("BF<sub>3</sub>", "BF3", 0), ("BeCl<sub>2</sub>", "BeCl2", 1)]
add(id="m23-p6", module="m23", kind="practice", level="Standard",
    prompt="<p>Give the hybridization of the central atom in each species. All of them have only single bonds, so count bonded atoms plus lone pairs.</p>",
    answer=hyb_match(M23_P6),
    hints=["Draw each Lewis structure first: lone pairs on the central atom count (Day 10 p.9, p.16).",
           "SN 2 → sp, SN 3 → sp<sup>2</sup>, SN 4 → sp<sup>3</sup> (Day 11 p.24). B and Be are electron-deficient: count what's actually there (Day 9 p.27)."],
    solution="<p class='lw-row'>" + "".join(LS(sid, scale=0.62) for _, sid, _ in M23_P6) + "</p>"
             "<p>CH<sub>4</sub>, NH<sub>4</sub><sup>+</sup>: four bonded atoms → SN 4 → <strong>sp<sup>3</sup></strong>. NF<sub>3</sub>, PCl<sub>3</sub>: three atoms + one lone pair → SN 4 → <strong>sp<sup>3</sup></strong>. "
             "BF<sub>3</sub>: three atoms and no lone pair on B, which has only 6 electrons → SN 3 → <strong>sp<sup>2</sup></strong>, with one empty p orbital. "
             "BeCl<sub>2</sub>: two atoms → SN 2 → <strong>sp</strong>, with two empty p orbitals.</p>",
    source="Day 11 p.12, p.24; Day 10 p.9, p.16; Day 9 p.27")

M23_P7 = [("the C in CS<sub>2</sub>", "CS2", 1), ("the N in NO<sub>3</sub><sup>−</sup>", "NO3-1", 0), ("the C in SCN<sup>−</sup>", "SCN-a", 1),
          ("the S in SO<sub>3</sub><sup>2−</sup>", "SO3-oct", 0), ("the O in HOCl", "HOCl", 1), ("the C in CO<sub>3</sub><sup>2−</sup>", "CO3-1", 0),
          ("the O in CH<sub>2</sub>O", "CH2O", 3)]
# resonance doesn't change the count: the same SN in every structure of each ion
assert steric("NO3-1", 0) == steric("NO3-2", 0) == steric("NO3-3", 0) == 3
assert steric("CO3-1", 0) == steric("CO3-2", 0) == steric("CO3-3", 0) == 3
assert steric("SCN-a", 1) == steric("SCN-b", 1) == steric("SCN-c", 1) == 2
assert steric("SO3-oct", 0) == steric("SO3-exp", 0) == 4
add(id="m23-p7", module="m23", kind="practice", level="Standard",
    prompt="<p>A double or triple bond counts as <em>one</em> electron domain: CO<sub>2</sub>, with two double bonds, has SN 2 (Day 10 p.10). Give the hybridization of each atom. "
           "Four of them sit in ions from the polyatomic-ion table (Day 8 p.8); for an ion with resonance structures, any one of its structures gives the count.</p>",
    answer=hyb_match(M23_P7),
    hints=["Draw each Lewis structure and count the bonded atoms and lone pairs around the atom in question.",
           "CS<sub>2</sub> and SCN<sup>−</sup>: the C has 2 bonded atoms and no lone pair. SO<sub>3</sub><sup>2−</sup>: S has 3 atoms and 1 lone pair. HOCl: O has 2 atoms and 2 lone pairs."],
    solution="<p class='lw-row'>" + LS("CS2", scale=0.7) + LS("NO3-1", scale=0.62) + LS("SCN-a", scale=0.7) + LS("SO3-oct", scale=0.62) + LS("HOCl", scale=0.7)
             + LS("CO3-1", scale=0.62) + LS("CH2O", scale=0.7) + "</p>"
             "<p>CS<sub>2</sub> C: 2 atoms → <strong>sp</strong>. NO<sub>3</sub><sup>−</sup> N: 3 atoms, no lone pair → SN 3 → <strong>sp<sup>2</sup></strong>. SCN<sup>−</sup> C: 2 atoms → <strong>sp</strong>. "
             "SO<sub>3</sub><sup>2−</sup> S: 3 atoms + 1 lone pair → SN 4 → <strong>sp<sup>3</sup></strong>. HOCl O: 2 atoms + 2 lone pairs → <strong>sp<sup>3</sup></strong>. "
             "CO<sub>3</sub><sup>2−</sup> C: 3 atoms → <strong>sp<sup>2</sup></strong>. CH<sub>2</sub>O O: 1 atom + 2 lone pairs → SN 3 → <strong>sp<sup>2</sup></strong> (Day 11 p.18).</p>"
             "<p>Resonance doesn't change these counts: in every structure of NO<sub>3</sub><sup>−</sup>, CO<sub>3</sub><sup>2−</sup>, SCN<sup>−</sup>, and SO<sub>3</sub><sup>2−</sup>, "
             "the central atom has the same bonded atoms and lone pairs; only the multiple bonds move.</p>",
    source="Day 11 p.18, p.24; Day 10 p.10; Day 8 p.8")

M23_P8 = [("the S–C–S angle in CS<sub>2</sub>", "CS2", 1), ("the O–C–O angle in CO<sub>3</sub><sup>2−</sup>", "CO3-1", 0),
          ("the H–N–H angle in NH<sub>4</sub><sup>+</sup>", "NH4+", 0)]
ANGLE_KEY = {2: "a180", 3: "a120", 4: "a109"}
assert [steric(sid, k) for _, sid, k in M23_P8] == [2, 3, 4] and all(LW.STRUCTS[sid].lp.get(k, 0) == 0 for _, sid, k in M23_P8)
add(id="m23-p8", module="m23", kind="practice", level="Concept",
    prompt="<p>Each central atom here has no lone pairs, so its bond angles are the angles between its hybrid orbitals. Work out each atom's hybridization, then match each angle.</p>",
    answer={"type": "match",
            "rows": [{"html": h, "answer": ANGLE_KEY[steric(sid, k)]} for h, sid, k in M23_P8]
                    + [{"html": "the angle between the two unhybridized p orbitals on the C of CS<sub>2</sub>", "answer": "a90"}],
            "options": [{"key": "a180", "html": f"{ANGLE[2]:.0f}°"}, {"key": "a120", "html": f"{ANGLE[3]:.0f}°"},
                        {"key": "a109", "html": f"{ANGLE[4]:.1f}°"}, {"key": "a90", "html": "90°"}]},
    hints=["CS<sub>2</sub>'s C has 2 bonded atoms, CO<sub>3</sub><sup>2−</sup>'s C has 3, and NH<sub>4</sub><sup>+</sup>'s N has 4, none with lone pairs. Which hybridization does each SN give?",
           "Hybrids spread as far apart as possible: 2 in a line, 3 in a plane, 4 toward the corners of a tetrahedron (Table 5.3, Day 11 p.24). Unhybridized p orbitals keep the 2p orientation, one along each axis."],
    solution=f"<p>CS<sub>2</sub>: sp C → S–C–S <strong>{ANGLE[2]:.0f}°</strong>. CO<sub>3</sub><sup>2−</sup>: sp<sup>2</sup> C → O–C–O <strong>{ANGLE[3]:.0f}°</strong>. "
             f"NH<sub>4</sub><sup>+</sup>: sp<sup>3</sup> N → H–N–H <strong>{ANGLE[4]:.1f}°</strong>. These are the “Angles between Hybrid Orbitals” in Table 5.3 (Day 11 p.24), "
             "and the same ideal angles VSEPR gives for SN 2, 3, and 4 (Day 10 p.26); with no lone pairs on the central atom, nothing squeezes them. "
             "The two unhybridized p orbitals on CS<sub>2</sub>'s sp carbon are <strong>90°</strong> apart, like the 2p orbitals they were, and each makes one of its π bonds (<a href='#m24'>§5.4–5.5</a>).</p>",
    source="Day 11 p.11, p.23–24; Day 10 p.26")

P(id="m23-p9", module="m23", kind="practice", level="Textbook preview",
  prompt="<p>The textbook compares the energies of different hybrid orbitals on the same atom. Which is lower in energy, an sp<sup>2</sup> or an sp<sup>3</sup> hybrid, and why?</p>",
  answer=choice(("sp<sup>2</sup>, because only two p orbitals are mixed with the s orbital", True,
                 "Right: “The energy levels of sp<sup>2</sup> orbitals are slightly lower than those of sp<sup>3</sup> orbitals because only two p orbitals are mixed with the s orbital” (PDF p.249)."),
                ("sp<sup>3</sup>, because more orbitals are mixed", False,
                 "Mixing in more of the higher-energy 2p orbitals raises the average; it doesn't lower it."),
                ("Neither: both are averages of the same 2s and 2p orbitals, so their energies are equal", False,
                 "They average the same orbitals in different proportions: one s with two p versus one s with three p. With less of the higher-energy 2p in the mix, sp<sup>2</sup> ends up lower."),
                ("sp<sup>2</sup>, because sp<sup>2</sup> hybrids hold more lone pairs", False,
                 "An orbital's energy depends on which orbitals were mixed to make it, not on what it holds.")),
  hints=["On the slides' energy diagrams, 2s lies below 2p (Day 11 p.13, p.18). Which hybrid has the smaller share of 2p?"],
  solution="<p><strong>sp<sup>2</sup></strong>. The textbook: “The energy levels of sp<sup>2</sup> orbitals are slightly lower than those of sp<sup>3</sup> orbitals because only two p orbitals are mixed with the s orbital "
           "in a set of sp<sup>2</sup> orbitals” (§5.4, PDF p.249). The 2s orbital is the lower-energy ingredient, so a hybrid with more s in the mix lies lower. "
           "The slides draw the hybrid boxes between the 2s and 2p levels but don't compare sp<sup>2</sup> with sp<sup>3</sup> (Day 11 p.16, p.18).</p>",
  source=tb("5.4", 249) + "; Day 11 p.13, p.16, p.18")

add(id="m23-transfer", module="m23", kind="transfer", level="Transfer",
    prompt="<p>Carbon has two common solid forms. In <strong>diamond</strong>, every C atom is bonded to four other C atoms that sit at the corners of a tetrahedron around it. "
           "In <strong>graphite</strong>, every C atom is bonded to three other C atoms in a flat sheet of hexagons.</p>"
           "<p>(a) What is the hybridization of C in diamond? (b) In graphite? (c) What C–C–C angle do you predict within a graphite sheet? "
           "(d) How many of each graphite C atom's four valence electrons are left in an unhybridized p orbital?</p>",
    answer={"type": "multi", "parts": [
        {"label": "(a) C in diamond", **hyb_choice(4, {
            2: "sp would mean two neighbors in a straight line.",
            3: "sp<sup>2</sup> fits three neighbors in a plane. Diamond's C has four.",
            4: "Right: four neighbors, no lone pairs → SN 4 → sp<sup>3</sup>, like the C in CH<sub>4</sub>."})},
        {"label": "(b) C in graphite", **hyb_choice(3, {
            2: "sp is for two neighbors (SN 2).",
            3: "Right: three neighbors → SN 3 → sp<sup>2</sup>, with one 2p orbital left over.",
            4: "sp<sup>3</sup> needs four electron domains. Each graphite C has three neighbors and no lone pair."})},
        {"label": "(c) C–C–C angle in a sheet", **num_ans(ANGLE[3], tol=0.005, unit_label="°"),
         "traps": [{"value": round(TET, 1), "tol": 0.005, "message": "109.5° is the sp<sup>3</sup> angle, diamond's. Graphite's C is sp<sup>2</sup>."}]},
        {"label": "(d) electrons left in the unhybridized p orbital", **tnum(4 - 3, traps=[
            (0, "Three electrons go into the three sp<sup>2</sup> hybrids that make the σ bonds, but carbon has four."),
            (2, "Two would be an sp carbon, with two unhybridized p orbitals.")])}]},
    hints=["Count the electron domains around one C atom in each solid. These C atoms have no lone pairs.",
           "Diamond: 4 bonded atoms → SN 4. Graphite: 3 bonded atoms → SN 3, which leaves one 2p orbital out of the hybrid set (Day 11 p.18, p.24)."],
    solution=f"<p>(a) <strong>sp<sup>3</sup></strong>: four C neighbors → SN 4, as for the C in CH<sub>4</sub>, with {ANGLE[4]:.1f}° angles. (b) <strong>sp<sup>2</sup></strong>: three neighbors → SN 3. "
             f"(c) <strong>{ANGLE[3]:.0f}°</strong>, the angle between sp<sup>2</sup> hybrids, which is also the inside angle of a regular hexagon. "
             "(d) <strong>1</strong>: three of carbon's four valence electrons go into the three σ bonds, and the fourth sits in the unhybridized 2p orbital perpendicular to the sheet.</p>"
             "<p class='bg'>Those p electrons on neighboring atoms overlap side by side across the whole sheet, like benzene's (<a href='#m24'>§5.4–5.5</a>), one reason graphite conducts electricity and diamond doesn't.</p>",
    source="Day 11 p.12–15, p.18, p.24")

add(id="m23-m-explain", module="m23", kind="mastery", level="Explain",
    prompt="<p>Explain, as the lecture does (Day 11 p.11–15), why the carbon in CH<sub>4</sub> is described with four sp<sup>3</sup> hybrid orbitals rather than its ground-state orbitals or a promoted electron. "
           "Say how many hybrids there are and why, what each holds, and what each overlaps.</p>",
    answer={"type": "self", "model":
            "<p>Ground-state carbon, 2s<sup>2</sup>2p<sup>2</sup>, has only two unpaired electrons, so it could make only two bonds, from 2p orbitals at 90°. Promoting a 2s electron gives four unpaired electrons, "
            "but in one 2s and three 2p orbitals, so the four bonds wouldn't be equivalent: “that's not what methane <strong>looks</strong> like! We need four equivalent bonds pointing to the vertices of a tetrahedron!” (Day 11 p.11). "
            "Pauling's fix is hybridization: mix (“average”) the 2s and three 2p orbitals into new orbitals, one for every electron domain (Day 11 p.12). Carbon in CH<sub>4</sub> has SN 4, so it makes four sp<sup>3</sup> hybrids, "
            "each holding one electron and pointing to a corner of a tetrahedron, 109.5° apart (p.13–15). Each overlaps an H 1s orbital head-on to form a σ bond, giving four identical C–H bonds.</p>"},
    hints=[], solution="", source="Day 11 p.11–15")

add(id="m23-m-recognize", module="m23", kind="mastery", level="Recognize",
    prompt="<p>Which clue tells you that an atom is sp<sup>2</sup> hybridized?</p>",
    answer=choice(("It has exactly three electron domains (SN 3): bonded atoms plus lone pairs, with a double bond counting once.", True,
                   "Right: SN 3 → three hybrids → sp<sup>2</sup> (Day 11 p.12, p.24)."),
                  ("It has a double bond.", False,
                   "Often true, but not the test: the N in NO<sub>2</sub><sup>+</sup>, O=N=O, has two double bonds and is sp (SN 2). Count domains instead."),
                  ("It's bonded to three atoms.", False,
                   "The N in NH<sub>3</sub> is bonded to three atoms but also has a lone pair: SN 4, sp<sup>3</sup>."),
                  ("It has one lone pair.", False,
                   "Lone pairs count toward SN but don't settle it: NH<sub>3</sub>'s N (one lone pair) is sp<sup>3</sup>; diazene's N (one lone pair) is sp<sup>2</sup>.")),
    hints=["What does the number of hybrids depend on (Day 11 p.12)?"],
    solution="<p>Hybridization follows the <strong>steric number</strong>, not the bond count or the number of lone pairs on its own: SN 2 → sp, SN 3 → sp<sup>2</sup>, SN 4 → sp<sup>3</sup> (Day 11 p.12, p.24). "
             "The textbook puts it this way: “the SN of an atom with an octet of valence electrons is directly linked to both its hybridization and its molecular geometry” (PDF p.248).</p>"
             "<p class='connection'>For a C, N, or O atom with an octet, a shortcut follows: only single bonds and lone pairs → sp<sup>3</sup>; one double bond → sp<sup>2</sup>; a triple bond or two double bonds → sp. "
             "Electron-deficient B and Be have no octet, so count their domains directly (BF<sub>3</sub>: sp<sup>2</sup>; BeCl<sub>2</sub>: sp).</p>",
    source="Day 11 p.12, p.24; " + tb("5.4", 248))

add(id="m23-m-sanity", module="m23", kind="mastery", level="Sanity check",
    prompt="<p>Day 11 p.24's Table 5.3 lists, for sp<sup>3</sup> with 3 σ bonds, the molecular geometry “Trigonal planar” with angles “&lt;109.5°”. A classmate concludes from it that NH<sub>3</sub> is flat. What's right?</p>",
    answer=choice(("NH<sub>3</sub> is trigonal pyramidal: with sp<sup>3</sup> N, the three H atoms sit on three corners of a tetrahedron and the lone pair on the fourth. That row's label disagrees with Day 10 p.18 and p.26 and with the textbook's own Table 5.3.", True,
                   "Right. A planar molecule would need SN 3 and 120° angles, not sp<sup>3</sup> and angles below 109.5°: the row contradicts itself. Trust the reasoning (and Day 10 p.18: “trigonal pyramidal”, 107°)."),
                  ("NH<sub>3</sub> is trigonal planar, as the table says.", False,
                   "Flat would need three domains at 120°. N has four (three bonds and a lone pair), and the measured angle is 107° (Day 10 p.18)."),
                  ("NH<sub>3</sub> is tetrahedral.", False,
                   "Tetrahedral is the electron-pair geometry. The molecular geometry names the positions of the atoms only (Day 10 p.16)."),
                  ("NH<sub>3</sub> is bent.", False,
                   "Bent is sp<sup>3</sup> with two σ bonds and two lone pairs, like H<sub>2</sub>O (Day 10 p.19).")),
    hints=["Check the row against itself: does “trigonal planar” fit an sp<sup>3</sup> atom with angles below 109.5°?"],
    solution="<p><strong>Trigonal pyramidal.</strong> An sp<sup>3</sup> atom points its four hybrids toward the corners of a tetrahedron. With three σ bonds, the fourth hybrid holds a lone pair (NH<sub>3</sub>, Day 11 p.16), "
             "and the three atoms form a pyramid with N at its top: “SN = 4 and three atoms predicts trigonal pyramidal geometry,” 107° (Day 10 p.16–18; also the table on Day 10 p.26). "
             "The textbook's Table 5.3 gives “Trigonal pyramidal” in this row (PDF p.252).</p>"
             "<p class='note'>The slide's version of Table 5.3 (Day 11 p.24) prints “Trigonal planar” for sp<sup>3</sup> with 3 σ bonds. It's a slip in that table: the professor's own Day 10 slides say trigonal pyramidal.</p>",
    source="Day 11 p.16, p.24; Day 10 p.16–18, p.26; " + tb("5.4", 252))


# =====================================================================================
# m24  π bonds and molecules with several central atoms (Day 11 p.17-26; textbook §5.4-5.5, PDF p.249-255)
# =====================================================================================
SP_IMINE = sigma_pi("CH2NH")
assert SP_IMINE == (4, 1) and steric("CH2NH", 0) == steric("CH2NH", 1) == 3 and boxes("CH2NH", 1) == ([2, 1, 1], [1])
add(id="m24-attempt", module="m24", kind="attempt", level="Guided attempt",
    prompt="<p>Methanimine, H<sub>2</sub>C=NH, is formaldehyde with an N–H in place of the O. Work out its bonding the way the lecture works formaldehyde (Day 11 p.17–19).</p>"
           "<p class='lw-row'>" + LS("CH2NH", scale=0.8) + "</p>"
           "<p>(a) How many σ bonds does it have? (b) How many π bonds? (c) What is the hybridization of the C? (d) Of the N? (e) Which orbitals form the π bond?</p>",
    answer={"type": "multi", "parts": [
        {"label": "(a) σ bonds", **tnum(SP_IMINE[0], traps=[
            (SP_IMINE[0] + SP_IMINE[1], "You counted both lines of C=N as σ bonds. Only one bond between two atoms lies along the bond axis; the second is π (Day 11 p.17)."),
            (SP_IMINE[0] - 1, "Don't forget the N–H bond: every bond to H is a σ bond.")])},
        {"label": "(b) π bonds", **tnum(SP_IMINE[1], traps=[
            (2, "A π bond has two lobes, above and below the plane, but it's one bond. One double bond means one π bond.")])},
        {"label": "(c) hybridization of the C", **hyb_choice(steric("CH2NH", 0), {
            2: "sp is for SN 2, like acetylene's triple-bonded carbons (Day 11 p.23).",
            3: "Right: two H atoms and the N → SN 3, like the C of formaldehyde (Day 11 p.18).",
            4: "The C has four bond lines but only three electron domains: the double bond counts once. An sp<sup>3</sup> C would have no p orbital left for the π bond."})},
        {"label": "(d) hybridization of the N", **hyb_choice(steric("CH2NH", 1), {
            2: "That leaves out N's lone pair. It counts: 2 bonded atoms + 1 lone pair = SN 3.",
            3: "Right: the C, the H, and a lone pair → SN 3, like each N of diazene (Day 11 p.22).",
            4: "Counting the C=N as two domains gives 4. A double bond counts once, so SN is 3."})},
        {"label": "(e) the π bond forms from", **choice(
            ("side-to-side overlap of the unhybridized 2p orbitals on C and N", True, "Right: “π bonds always result from side-to-side overlap of unhybridized orbitals” (Day 11 p.20)."),
            ("head-on overlap of an sp<sup>2</sup> hybrid on C with one on N", False, "That's the C–N σ bond, the other half of the double bond."),
            ("overlap of N's lone-pair hybrid with the C", False, "The lone pair stays on N in its own sp<sup>2</sup> hybrid; it isn't shared (“Lone pairs always reside in hybrid orbitals,” Day 11 p.20)."),
            ("side-to-side overlap of two sp<sup>2</sup> hybrids", False, "Hybrids make σ bonds by head-on overlap. Side-to-side overlap belongs to the unhybridized p orbitals."))}]},
    hints=["“Each double bond consists of a sigma bond AND a pi (π) bond” (Day 11 p.17). Every single bond is a σ bond.",
           "σ bonds: head-on overlap of hybrid orbitals (H uses 1s). π bonds: side-to-side overlap of unhybridized orbitals (Day 11 p.20).",
           "Count each atom's electron domains. C: two H atoms and the N. N: the C, the H, and a lone pair. The double bond counts once.",
           "Both atoms have SN 3, so each is sp<sup>2</sup> with one unhybridized 2p orbital, as in formaldehyde. σ: two C–H, one C–N, one N–H. π: the two leftover 2p orbitals, side by side."],
    solution=box_diagram("CH2NH", 1) +
             f"<p>(a) <strong>{SP_IMINE[0]}</strong> σ bonds: two C–H, the C–N σ bond, and N–H. (b) <strong>{SP_IMINE[1]}</strong> π bond. (c) <strong>sp<sup>2</sup></strong> C (SN 3). "
             "(d) <strong>sp<sup>2</sup></strong> N (SN 3): its 5 electrons fill the sp<sup>2</sup> hybrids [↑↓][↑][↑] and the p orbital [↑], so the lone pair sits in a hybrid, as in diazene (Day 11 p.22). "
             "(e) The π bond is the side-to-side overlap of the C and N 2p orbitals, with its density above and below the molecular plane.</p>",
    compare={"wrong": "<p>“The C=N double bond is two σ bonds, so methanimine has five σ bonds and no π bond. And N, with a lone pair and three bond lines, is sp<sup>3</sup>.”</p>",
             "tempting": "The Lewis structure draws both lines of C=N alike, and counting every line plus the lone pair gives N four of something.",
             "fails": "Only one pair of orbitals can overlap head-on along the C–N axis, so only one of the two bonds is σ (Day 11 p.17). And the steric number counts electron domains, not lines: "
                      "N has two bonded atoms and a lone pair, SN 3, so it's sp<sup>2</sup> and keeps one 2p orbital. That p orbital and carbon's overlap side by side to make the π bond, "
                      "just as C and O do in formaldehyde (Day 11 p.18–19). Four σ, one π."},
    source="Day 11 p.17–20, p.22")

add(id="m24-p1", module="m24", kind="practice", level="Warm-up",
    prompt="<p>Which description fits a π bond (Day 11 p.17)?</p>",
    answer=choice(("A covalent bond with its electron density greatest above and below the bonding axis", True, "Right: the definition on Day 11 p.17."),
                  ("A covalent bond with its highest electron density between the two atoms, along the bond axis", False, "That's a σ bond (Day 11 p.10)."),
                  ("Two bonds, one above and one below the bond axis", False,
                   "Tempting, because a π bond has two lobes, but it's one bond. The textbook stresses it: the π bond is “one bond formed by the two atoms' p orbitals through two points of contact—it is not two bonds” (PDF p.249)."),
                  ("A bond formed by head-on overlap of two hybrid orbitals", False,
                   "Head-on overlap of hybrids makes σ bonds. π bonds come from side-to-side overlap of unhybridized orbitals (Day 11 p.20).")),
    hints=["Compare the σ definition (Day 11 p.10) with the π one (p.17): where is the electron density?"],
    solution="<p>A π bond is “a covalent bond in which electron density is greatest above and below the bonding axis” (Day 11 p.17). "
             "It forms by side-to-side overlap of unhybridized p orbitals (p.20), and it's one bond with two lobes.</p>",
    source="Day 11 p.10, p.17, p.20; " + tb("5.4", 249))

SP_C2H2 = sigma_pi("C2H2")
add(id="m24-p2", module="m24", kind="practice", level="Warm-up",
    prompt="<p>Acetylene, H–C≡C–H (Day 11 p.23). (a) How many σ bonds? (b) How many π bonds? (c) What is the hybridization of each C?</p>",
    answer={"type": "multi", "parts": [
        {"label": "(a) σ bonds", **tnum(SP_C2H2[0], traps=[(5, "Only one of the triple bond's three shared pairs is σ: a triple bond is one σ + two π."),
                                                           (2, "Count the C–C σ bond too: H–C, C–C, and C–H.")])},
        {"label": "(b) π bonds", **tnum(SP_C2H2[1], traps=[(3, "One of the three shared pairs lies on the C–C axis: that one is σ, not π.")])},
        {"label": "(c) hybridization of each C", **hyb_choice(steric("C2H2", 1), {
            2: "Right: two domains (the H and the other C) → two sp hybrids, leaving two unhybridized p orbitals for the two π bonds (Day 11 p.23).",
            3: "SN 3 would need three domains. Each C here has two: the H and the triple bond.",
            4: "An sp<sup>3</sup> C has no unhybridized p orbitals, so it couldn't make any π bond."})}]},
    hints=["H–C≡C–H: two C–H single bonds and one C≡C triple bond.", "A triple bond is one σ and two π. Each C has SN 2."],
    solution=box_diagram("C2H2", 1) +
             f"<p>(a) <strong>{SP_C2H2[0]}</strong> σ: H–C, C–C, C–H (the slide's “H1s σ sp,” “sp σ sp,” and “sp σ H1s”). "
             f"(b) <strong>{SP_C2H2[1]}</strong> π: “π bond (1)” and “π bond (2),” from the two pairs of unhybridized p orbitals, at right angles to each other. "
             "(c) <strong>sp</strong>: “Two sp hybrid orbitals” and “Two unhybridized p orbitals” on each C (Day 11 p.23).</p>",
    source="Day 11 p.23")

# The N of nitrite, not diazene: diazene's N is worked in the module's teaching text (Day 11 p.22), so asking about it
# here would be a give-away. Same pattern (2 bonded atoms + 1 lone pair, one pi bond), same keys.
N_NO2 = next(k for k, a in enumerate(LW.STRUCTS["NO2-1"].atoms) if a[0] == "N")
assert steric("NO2-1", N_NO2) == steric("NO2-2", N_NO2) == 3 and boxes("NO2-1", N_NO2) == boxes("N2H2", 0) == ([2, 1, 1], [1])
add(id="m24-p3", module="m24", kind="practice", level="Concept",
    prompt="<p>The nitrite ion, NO<sub>2</sub><sup>−</sup>, is on the polyatomic-ion table (Day 8 p.8). Here is one of its two resonance structures:</p>"
           "<p class='lw-row'>" + LS("NO2-1", scale=0.8) + "</p>"
           "<p>(a) What is the hybridization of the N? (b) Which orbital holds the N's lone pair?</p>",
    answer={"type": "multi", "parts": [
        {"label": "(a) hybridization of the N", **hyb_choice(steric("NO2-1", N_NO2), {
            2: "That leaves out the lone pair. It counts as a domain: SN = 2 atoms + 1 lone pair = 3.",
            3: "Right: two O atoms and a lone pair → SN 3, like each N of diazene (Day 11 p.22).",
            4: "The N=O double bond counts as one domain, so SN is 3, not 4."})},
        {"label": "(b) the N's lone pair is in", **choice(
            ("an sp<sup>2</sup> hybrid orbital", True, "Right: “Lone pairs always reside in hybrid orbitals” (Day 11 p.20), just as the diazene slide draws each N's lone pair in an sp<sup>2</sup> lobe (Day 11 p.22)."),
            ("the unhybridized 2p orbital", False, "That orbital holds the N electron that forms the N=O π bond, side by side with a p orbital on the O."),
            ("the 2s orbital", False, "The 2s orbital has been mixed into the sp<sup>2</sup> set; it isn't separate any more."),
            ("an sp<sup>3</sup> hybrid orbital", False, "This N is sp<sup>2</sup>: it has no sp<sup>3</sup> hybrids."))}]},
    hints=["Count the N's electron domains: bonded atoms + lone pairs, with the double bond counted once. Resonance doesn't change the count; in the other structure the double bond goes to the other O.",
           "N's 5 valence electrons in three sp<sup>2</sup> hybrids and one p orbital: [↑↓][↑][↑] + [↑], the pattern of each N in diazene (Day 11 p.22)."],
    solution=box_diagram("NO2-1", N_NO2) +
             "<p>(a) <strong>sp<sup>2</sup></strong>: two bonded O atoms and one lone pair, SN 3, in either resonance structure. (b) <strong>An sp<sup>2</sup> hybrid.</strong> "
             "N's 5 electrons go [↑↓][↑][↑] in its sp<sup>2</sup> hybrids and [↑] in the unhybridized p: the paired hybrid is the lone pair, the two single hybrids form the two N–O σ bonds, "
             "and the p electron forms the N=O π bond. It's the bonding of each N in diazene (Day 11 p.22), with two O atoms in place of the H and the other N.</p>",
    source="Day 11 p.20, p.22; Day 8 p.8")

M24_P4 = [("N<sub>2</sub>O", "N2O-A"), ("HCOOH", "HCOOH"), ("N<sub>2</sub>H<sub>4</sub>", "N2H4")]
_p4_parts = []
for _html, _sid in M24_P4:
    _s, _p = sigma_pi(_sid)
    _traps = [(_s + _p, "That's the number of bond lines. Each multiple bond contains only one σ bond.")] if _p else []
    _p4_parts.append({"label": f"{_html}: σ bonds", **tnum(_s, traps=_traps)})
    _p4_parts.append({"label": f"{_html}: π bonds", **tnum(_p)})
assert [sigma_pi(x) for _, x in M24_P4] == [(2, 2), (4, 1), (5, 0)]
assert sigma_pi("N2O-B") == sigma_pi("N2O-C") == sigma_pi("N2O-A")                   # every N2O structure gives 2 σ, 2 π
assert steric("N2H4", 0) == steric("N2H4", 1) == 4 and steric("N2H2", 0) == 3
add(id="m24-p4", module="m24", kind="practice", level="Standard",
    prompt="<p>Count the σ and π bonds in each molecule. N<sub>2</sub>O is drawn as the structure that formal charge favors (the Day 9 p.19–24 example).</p>"
           "<p class='lw-row'>" + LS("N2O-A", scale=0.75) + LS("HCOOH", scale=0.7) + LS("N2H4", scale=0.75) + "</p>",
    answer={"type": "multi", "parts": _p4_parts},
    hints=["Every pair of bonded atoms shares exactly one σ bond. The extra lines of double and triple bonds are π (Day 11 p.17, p.23).",
           "N<sub>2</sub>O as drawn: N≡N and N–O. HCOOH: H–C, C=O, C–O, O–H. N<sub>2</sub>H<sub>4</sub>: only single bonds."],
    solution="<p>N<sub>2</sub>O: <strong>2 σ, 2 π</strong>; its other two structures (N=N=O and N–N≡O, Day 9 p.20) give the same counts. HCOOH: <strong>4 σ, 1 π</strong>. "
             "N<sub>2</sub>H<sub>4</sub>: <strong>5 σ, 0 π</strong>. The rule: σ = the number of bonded pairs of atoms; π = 1 per double bond and 2 per triple bond.</p>"
             "<p class='connection'>Hydrazine, N<sub>2</sub>H<sub>4</sub>, and diazene, N<sub>2</sub>H<sub>2</sub> (Day 11 p.22), differ by one π bond: each N in diazene is sp<sup>2</sup>, "
             "while each N in hydrazine (three bonded atoms and a lone pair) is sp<sup>3</sup> and has no p orbital left for a π bond.</p>",
    source="Day 11 p.17, p.20, p.22–23; Day 9 p.20, p.24")

SP_ACR, SP_BZ = sigma_pi("acrolein"), sigma_pi("C6H6-1")
assert SP_ACR == (7, 2) and SP_BZ == (12, 3) and sigma_pi("C6H6-2") == SP_BZ
assert all(steric("acrolein", k) == 3 for k in (0, 1, 2, 3)) and all(steric("C6H6-1", k) == 3 for k in range(6))
add(id="m24-p5", module="m24", kind="practice", level="Standard",
    prompt="<p>Day 11 p.26 shows acrolein and benzene without comment. Count their σ and π bonds (for benzene, use either structure with alternating double bonds).</p>"
           "<p class='lw-row'>" + LS("acrolein", scale=0.75) + LS("C6H6-1", scale=0.6) + "</p>",
    answer={"type": "multi", "parts": [
        {"label": "acrolein: σ bonds", **tnum(SP_ACR[0], traps=[(SP_ACR[0] + SP_ACR[1], "That's the number of bond lines. Each double bond contains only one σ bond."),
                                                               (SP_ACR[0] - 4, "Include the four C–H bonds: every bond, including each bond to H, has one σ bond.")])},
        {"label": "acrolein: π bonds", **tnum(SP_ACR[1])},
        {"label": "benzene: σ bonds", **tnum(SP_BZ[0], traps=[(6, "You counted only the ring. Each C also has a C–H σ bond."),
                                                             (SP_BZ[0] + SP_BZ[1], "That's the number of bond lines. Each C=C contains only one σ bond.")])},
        {"label": "benzene: π bonds", **tnum(SP_BZ[1], traps=[(6, "Only the three double bonds of a structure contain π bonds. Six counts every ring bond.")])}]},
    hints=["σ = one per bonded pair of atoms, including every C–H. π = one per double bond.",
           "Acrolein, CH<sub>2</sub>=CH–CH=O: 4 C–H, C=C, C–C, C=O. Benzene: 6 C–C and 6 C–H, with 3 C=C in each alternating structure."],
    solution=f"<p>Acrolein: <strong>{SP_ACR[0]} σ</strong> (4 C–H, C–C, and one each in C=C and C=O) and <strong>{SP_ACR[1]} π</strong>. "
             f"Benzene: <strong>{SP_BZ[0]} σ</strong> (6 C–C + 6 C–H) and <strong>{SP_BZ[1]} π</strong>. Every C in both molecules, and acrolein's O, has SN 3 and is sp<sup>2</sup>.</p>"
             "<p class='connection'>Benzene's two structures put the three π bonds in different places (Day 9 p.13). In the orbital picture, the six unhybridized 2p orbitals overlap all the way around the ring, "
             "so the π electrons spread over the whole ring: the π “cloud” above and below the ring drawn on Day 11 p.26. That's the orbital view of benzene's resonance hybrid.</p>",
    source="Day 11 p.26; Day 9 p.12–13; " + tb("5.5", 254))

M24_P6 = [("CH<sub>3</sub>CN: the CH<sub>3</sub> carbon", "CH3CN", 0), ("CH<sub>3</sub>CN: the carbon bonded to N", "CH3CN", 4),
          ("CH<sub>3</sub>CN: the N", "CH3CN", 5), ("HCOOH: the C", "HCOOH", 0), ("HCOOH: the O double-bonded to C", "HCOOH", 2),
          ("allene, H<sub>2</sub>C=C=CH<sub>2</sub>: an end carbon", "allene", 0), ("allene: the middle carbon", "allene", 1)]
assert [steric(s, k) for _, s, k in M24_P6] == [4, 2, 2, 3, 3, 3, 2]
SP_CH3CN, SP_HCOOH, SP_ALLENE = sigma_pi("CH3CN"), sigma_pi("HCOOH"), sigma_pi("allene")
add(id="m24-p6", module="m24", kind="practice", level="Standard",
    prompt="<p>A molecule with several “central” atoms: give each atom's hybridization, one atom at a time.</p>"
           "<p class='lw-row'>" + LS("CH3CN", scale=0.7) + LS("HCOOH", scale=0.7) + LS("allene", scale=0.7) + "</p>",
    answer=hyb_match(M24_P6),
    hints=["Treat each non-H atom as its own center: count its bonded atoms and lone pairs, with a multiple bond counted once.",
           "CH<sub>3</sub>CN: the CH<sub>3</sub> C has 4 bonded atoms; the other C has 2; N has 1 atom and 1 lone pair. Allene's middle C has two double bonds and nothing else."],
    solution=f"<p>CH<sub>3</sub>CN: <strong>sp<sup>3</sup></strong>, <strong>sp</strong>, <strong>sp</strong> ({SP_CH3CN[0]} σ, {SP_CH3CN[1]} π). "
             f"HCOOH: the C is <strong>sp<sup>2</sup></strong> (three domains: H, O, O) and the C=O oxygen <strong>sp<sup>2</sup></strong> (1 atom + 2 lone pairs); {SP_HCOOH[0]} σ, {SP_HCOOH[1]} π. "
             f"Allene: end carbons <strong>sp<sup>2</sup></strong>, middle carbon <strong>sp</strong> (two double bonds, SN 2); {SP_ALLENE[0]} σ, {SP_ALLENE[1]} π.</p>",
    source="Day 11 p.18–25")

add(id="m24-p7", module="m24", kind="practice", level="Concept",
    prompt="<p>Which atoms of ethylene, H<sub>2</sub>C=CH<sub>2</sub>, lie in one plane?</p>",
    answer=choice(("All six atoms", True, "Right: each C is trigonal planar (Day 11 p.25), and the π bond holds the two CH<sub>2</sub> halves in the same plane."),
                  ("Only the two C atoms; the H atoms point above and below them", False,
                   "Above and below the plane is where the π electron density is, not where the H atoms are."),
                  ("The two C atoms and two of the H atoms; the other CH<sub>2</sub> group is twisted 90°", False,
                   "Twisting one CH<sub>2</sub> by 90° would turn its p orbital perpendicular to the other's, and the side-to-side overlap, the π bond, would be lost."),
                  ("None: each carbon is tetrahedral", False, "Tetrahedral is SN 4. Each ethylene C has SN 3: trigonal planar, 120°.")),
    hints=["What's the shape around each C (Day 11 p.25)? For the π bond to form, how must the two p orbitals line up?"],
    solution="<p><strong>All six.</strong> Each C is sp<sup>2</sup>, with its three σ bonds in one plane, 120° apart (“Trigonal planar” at each C, Day 11 p.25). "
             "The π bond needs the two unhybridized p orbitals parallel so that they can overlap side by side, and that happens only when the two CH<sub>2</sub> planes coincide. "
             "The textbook: “all six atoms lie in the same plane” (§5.5, PDF p.253).</p>",
    source="Day 11 p.25; " + tb("5.5", 253, 254))

assert steric("allene", 1) == 2 and atom_pi("allene", 1) == 2 and steric("allene", 0) == steric("allene", 2) == 3
P(id="m24-p8", module="m24", kind="practice", level="Textbook preview",
  prompt="<p>Allene, H<sub>2</sub>C=C=CH<sub>2</sub>, has an sp middle carbon that makes a π bond to each end carbon. The textbook's CO<sub>2</sub> example shows that the two π bonds "
         "of an sp atom lie at 90° to each other (Sample Ex. 5.5, PDF p.252). What does that mean for allene's two CH<sub>2</sub> groups?</p>"
         "<p class='lw-row'>" + LS("allene", scale=0.75) + "</p>",
  answer=choice(("They lie in perpendicular planes: each CH<sub>2</sub> plane is perpendicular to the p orbital its π bond uses, and those two p orbitals on the middle carbon are 90° apart.", True,
                 "Right: twisting either CH<sub>2</sub> out of that position would break the side-to-side overlap of its π bond."),
                ("They lie in the same plane, like the two CH<sub>2</sub> halves of ethylene.", False,
                 "Ethylene's two carbons share one π bond, which needs both p orbitals parallel. Allene's end carbons bond to two different, perpendicular p orbitals of the middle carbon."),
                ("Each CH<sub>2</sub> group can turn freely, so their planes keep changing.", False,
                 "Turning a CH<sub>2</sub> would twist its p orbital away from the middle carbon's and break the π bond, so each CH<sub>2</sub> is held in place."),
                ("They're at 120° to each other, like the bonds around an sp<sup>2</sup> carbon.", False,
                 "120° is the angle between sp<sup>2</sup> hybrids in one plane. The two π bonds of an sp atom are 90° apart.")),
  hints=["Each end carbon is sp<sup>2</sup>, so its CH<sub>2</sub> group lies in the plane perpendicular to its own unhybridized p orbital. Which of the middle carbon's two p orbitals does each end carbon's p orbital overlap?"],
  solution="<p><strong>Perpendicular planes.</strong> The middle carbon is sp, with two unhybridized p orbitals at 90° to each other, like each carbon of acetylene (Day 11 p.23). "
           "One overlaps the left carbon's p orbital and the other overlaps the right carbon's. Each end carbon is sp<sup>2</sup>, and its CH<sub>2</sub> plane is perpendicular to its own p orbital, "
           "so the two CH<sub>2</sub> planes end up at 90°. It's the textbook's argument for CO<sub>2</sub>, whose two O atoms have their sp<sup>2</sup> planes “rotated 90°” with respect to each other (PDF p.252).</p>"
           "<p class='bg'>Measured structures of allene agree: its two H–C–H planes are perpendicular.</p>",
  source=tb("5.4", 252) + "; Day 11 p.23")


def pi_spread(orders):
    """Carbon chain given by the bond orders between neighbors: the number of atoms in the longest run of neighbors that
    each have an unhybridized p orbital (an atom in a multiple bond), which is what the π electrons can spread over."""
    n = len(orders) + 1
    has_p = []
    for i in range(n):
        left = orders[i - 1] if i > 0 else 1
        right = orders[i] if i < n - 1 else 1
        has_p.append(left > 1 or right > 1)
    best = run = 0
    for h in has_p:
        run = run + 1 if h else 0
        best = max(best, run)
    return best


SPREAD_A, SPREAD_B = pi_spread([2, 1, 2, 1]), pi_spread([2, 1, 1, 2])     # CH2=CH–CH=CH–CH3 and CH2=CH–CH2–CH=CH2
assert (SPREAD_A, SPREAD_B) == (4, 2)
P(id="m24-p9", module="m24", kind="practice", level="Textbook preview",
  prompt="<p>The textbook defines <strong>conjugation</strong> as “alternating single and multiple bonds in molecular compounds in which adjacent atoms have unhybridized p orbitals,” "
         "and says that the π electrons in such molecules are delocalized (PDF p.254). Over how many carbon atoms can the π electrons spread in each of these chains?</p>",
  answer={"type": "multi", "parts": [
      {"label": "(a) CH<sub>2</sub>=CH–CH=CH–CH<sub>3</sub>", **tnum(SPREAD_A, traps=[
          (5, "The CH<sub>3</sub> carbon has only single bonds: it's sp<sup>3</sup>, with no p orbital to join in."),
          (2, "Only one single bond separates the two double bonds, so all four of their carbons have p orbitals side by side in one run.")])},
      {"label": "(b) CH<sub>2</sub>=CH–CH<sub>2</sub>–CH=CH<sub>2</sub>", **tnum(SPREAD_B, traps=[
          (4, "The middle CH<sub>2</sub> is sp<sup>3</sup> and has no p orbital, so it splits the chain into two separate π bonds."),
          (5, "Count only atoms that have an unhybridized p orbital, and only neighbors in an unbroken run.")])}]},
  hints=["Mark each carbon's hybridization: a carbon in a double bond is sp<sup>2</sup> and has a p orbital; a carbon with only single bonds is sp<sup>3</sup> and has none.",
         "The π electrons can spread over a run of neighboring atoms that all have p orbitals. Find the longest run in each chain."],
  solution=f"<p>(a) <strong>{SPREAD_A}</strong>: the first four carbons are all sp<sup>2</sup>, so their p orbitals sit side by side and the π electrons of both double bonds spread over all four; "
           f"the sp<sup>3</sup> CH<sub>3</sub> carbon is left out. (b) <strong>{SPREAD_B}</strong>: the sp<sup>3</sup> CH<sub>2</sub> in the middle has no p orbital, so each π bond stays between its own two carbons. "
           "Benzene is the ring version of (a): six sp<sup>2</sup> carbons whose π electrons spread all the way around (PDF p.254).</p>"
           "<p class='note'>The professor says molecules with delocalized electrons are more stable “for reasons beyond the scope of this class” (Day 9 p.10). "
           "The textbook's reason is that delocalization spreads the electrons out, lowering their repulsion: “the greater the degree of delocalization, the greater the stability” (PDF p.255).</p>",
  source=tb("5.5", 254, 255) + "; Day 9 p.10")

SP_MIC = sigma_pi("CH3NCO")
assert SP_MIC == (6, 2) and [steric("CH3NCO", k) for k in (0, 1, 2, 3)] == [4, 3, 2, 3]
add(id="m24-transfer", module="m24", kind="transfer", level="Transfer",
    prompt="<p>Methyl isocyanate, CH<sub>3</sub>–N=C=O, has three “central” atoms in a row.</p><p class='lw-row'>" + LS("CH3NCO", scale=0.8) + "</p>"
           "<p>(a) How many σ bonds does it have? (b) How many π bonds? (c) What is the hybridization of the N? (d) Of the C bonded to O? "
           "(e) What N=C=O bond angle do you predict?</p>",
    answer={"type": "multi", "parts": [
        {"label": "(a) σ bonds", **tnum(SP_MIC[0], traps=[(SP_MIC[0] + SP_MIC[1], "That counts every bond line. Each double bond contains only one σ bond."),
                                                         (SP_MIC[0] - 3, "Include the three C–H bonds.")])},
        {"label": "(b) π bonds", **tnum(SP_MIC[1], traps=[(4, "Each double bond has one π bond, not two."),
                                                         (1, "There are two double bonds, N=C and C=O, and each has a π bond.")])},
        {"label": "(c) the N", **hyb_choice(steric("CH3NCO", 1), {
            2: "That leaves out the lone pair on N. It counts: 2 bonded atoms + 1 lone pair = SN 3.",
            3: "Right: the CH<sub>3</sub> carbon, the other C, and a lone pair → SN 3.",
            4: "The N=C double bond counts as one domain, so SN is 3."})},
        {"label": "(d) the C bonded to O", **hyb_choice(steric("CH3NCO", 2), {
            2: "Right: two double bonds and nothing else → SN 2.",
            3: "SN 3 would need three domains. This C has two: the N=C and the C=O.",
            4: "Each double bond counts as one domain, so SN is 2."})},
        {"label": "(e) N=C=O angle", **num_ans(ANGLE[2], tol=0.005, unit_label="°"),
         "traps": [{"value": ANGLE[3], "tol": 0.005, "message": "120° belongs to an sp<sup>2</sup> center. The C between N and O is sp."}]}]},
    hints=["Bonds: three C–H, C–N, N=C, C=O. Each bonded pair has one σ; the extra lines are π.",
           "Count domains at N (two bonded atoms and a lone pair) and at the C bonded to O (two double bonds)."],
    solution=f"<p>(a) <strong>{SP_MIC[0]}</strong> σ (3 C–H, C–N, and one each in N=C and C=O). (b) <strong>{SP_MIC[1]}</strong> π (one in N=C, one in C=O). "
             "(c) <strong>sp<sup>2</sup></strong>: 2 atoms + 1 lone pair, SN 3, with the lone pair in an sp<sup>2</sup> hybrid. "
             "(d) <strong>sp</strong> (SN 2): its two unhybridized p orbitals make the π bond to N and the π bond to O. The CH<sub>3</sub> carbon is sp<sup>3</sup> and the O is sp<sup>2</sup>. "
             f"(e) <strong>{ANGLE[2]:.0f}°</strong>: an sp carbon's two hybrids point in opposite directions, so N=C=O is a straight line.</p>",
    source="Day 11 p.17–25")

add(id="m24-m-explain", module="m24", kind="mastery", level="Explain",
    prompt="<p>Explain the bonding in formaldehyde, H<sub>2</sub>C=O, as Day 11 p.17–19 does: each atom's hybridization, which orbitals overlap to make each bond (count C=O as one σ and one π), "
           "where O's lone pairs sit, and where the π electron density is.</p>",
    answer={"type": "self", "model":
            "<p>C has three electron domains (two H atoms and the O), so it mixes its 2s with two 2p orbitals into three sp<sup>2</sup> hybrids, 120° apart in a plane, and keeps one unhybridized 2p orbital "
            "perpendicular to that plane. O has one bonded atom and two lone pairs, also SN 3, so it's sp<sup>2</sup> too (Day 11 p.18). The σ bonds: two C sp<sup>2</sup>–H 1s and one C sp<sup>2</sup>–O sp<sup>2</sup>, "
            "each a head-on overlap along the bond axis. The π bond: side-to-side overlap of the parallel C and O p orbitals, with its density above and below the molecular plane. "
            "O's two lone pairs sit in its other two sp<sup>2</sup> hybrids (“Lone pairs always reside in hybrid orbitals,” p.20). So the C=O double bond is one σ bond plus one π bond (p.17, p.19).</p>"},
    hints=[], solution="", source="Day 11 p.17–20")

assert steric("CH3CN", 0) == 4 and atom_pi("CH3CN", 0) == 0 and atom_pi("CH3CN", 5) == 2
add(id="m24-m-recognize", module="m24", kind="mastery", level="Recognize",
    prompt="<p>Which atom cannot take part in a π bond?</p>",
    answer=choice(("The CH<sub>3</sub> carbon of CH<sub>3</sub>CN", True,
                   "Right: four σ bonds → SN 4 → sp<sup>3</sup>. All four valence orbitals went into hybrids, so no unhybridized p orbital is left for side-to-side overlap (Day 11 p.20)."),
                  ("The N of CH<sub>3</sub>CN", False, "This N is sp (1 atom + 1 lone pair), with two unhybridized p orbitals: the two π bonds of C≡N."),
                  ("The C of CH<sub>2</sub>O", False, "sp<sup>2</sup>, with one p orbital: the π half of C=O (Day 11 p.18)."),
                  ("The O of CH<sub>2</sub>O", False, "Also sp<sup>2</sup>, with one p orbital: the other end of the π bond (Day 11 p.18).")),
    hints=["A π bond needs an unhybridized p orbital (Day 11 p.20). Which atom has none left?"],
    solution="<p>The <strong>sp<sup>3</sup> CH<sub>3</sub> carbon</strong>. A π bond needs an unhybridized p orbital on each of the two atoms (Day 11 p.20). "
             "An sp<sup>3</sup> atom has mixed its 2s and all three 2p orbitals into hybrids, so it can make only σ bonds. "
             "Quick test: an atom with only single bonds and lone pairs (SN 4) is sp<sup>3</sup> and has no π bonds; an sp<sup>2</sup> atom can make one π bond, an sp atom two.</p>",
    source="Day 11 p.18, p.20")

assert sigma_pi("CO") == (1, 2) and steric("CO", 0) == steric("CO", 1) == 2
add(id="m24-m-sanity", module="m24", kind="mastery", level="Sanity check",
    prompt="<p>A classmate says the triple bond in carbon monoxide, C≡O, is three σ bonds, all along the C–O axis. What's wrong with that?</p>"
           "<p class='lw-row'>" + LS("CO", scale=0.8) + "</p>",
    answer=choice(("Only one pair of orbitals can overlap head-on along the axis between two atoms. The other two shared pairs come from side-to-side overlap of unhybridized p orbitals: one σ + two π.", True,
                   "Right, the same as acetylene's triple bond (Day 11 p.23)."),
                  ("Nothing: three shared pairs are three σ bonds.", False,
                   "Then all three pairs would crowd into the same region between the nuclei, but C and O each have only one hybrid pointing at the other atom."),
                  ("It's three π bonds.", False, "The first bond between two atoms is always σ, from head-on overlap."),
                  ("CO has a double bond, not a triple bond.", False,
                   "With a C=O double bond and lone pairs completing O's octet, C would have only 6 electrons. Sharing a third pair gives both atoms an octet.")),
    hints=["How many orbitals on each atom point straight at the other atom?"],
    solution="<p>In :C≡O: each atom has 1 bonded atom + 1 lone pair: SN 2, sp. On each atom, one sp hybrid holds the lone pair and the other points at the other atom, making the <strong>one σ bond</strong>. "
             "The two unhybridized p orbitals on each atom overlap side by side with the matching p orbitals on the other atom, making <strong>two π bonds</strong> at right angles, "
             "just like acetylene's “π bond (1)” and “π bond (2)” (Day 11 p.23). A triple bond is 1 σ + 2 π.</p>",
    source="Day 11 p.20, p.23")


# ------------------------------------------------------------------ answer positions
# The items above are written correct-option-first. sp / sp2 / sp3 lists keep their natural order; every other
# choice spec is rotated (distractors keep their relative order) so that the correct option lands on positions taken
# in turn from a fixed balanced cycle. Bank G picks positions from an MD5 hash instead; on a bank this small the hash
# left almost half of the correct answers in the first position.
NATURAL = set()
for _p in PROBLEMS[J_START:]:
    for _path, _spec in choice_order.walk(_p["answer"]):
        if _spec.pop("_natural", False):
            NATURAL.add((_p["id"], _path))
CYCLE = {3: [1, 2, 0], 4: [2, 0, 3, 1, 3, 1, 0, 2]}


def balanced_spread(problems, keep):
    used, perms = {}, {}
    for p in problems:
        for path, spec in choice_order.walk(p["answer"]):
            if (p["id"], path) in keep:
                continue
            opts = spec["options"]
            n = len(opts)
            k = next(i for i, o in enumerate(opts) if o["correct"])
            seq = CYCLE.get(n, list(range(n)))
            target = seq[used.get(n, 0) % len(seq)]
            used[n] = used.get(n, 0) + 1
            r = (k - target) % n
            perm = [(i + r) % n for i in range(n)]              # new index -> old index
            spec["options"] = [opts[j] for j in perm]
            assert spec["options"][target]["correct"]
            perms.setdefault(p["id"], {})[path] = perm
    return perms


CHOICE_PERMS_J = balanced_spread(PROBLEMS[J_START:], NATURAL)

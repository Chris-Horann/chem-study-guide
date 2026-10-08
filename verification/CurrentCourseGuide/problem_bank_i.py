"""Problem bank I: Ch. 5 §5.1-5.3: molecular shape, VSEPR (no lone pairs, lone pairs), polar molecules (Day 10 p.3-31; Day 11 p.6-8; textbook §5.1-5.3, PDF p.232-246).
m20 steric number and the five no-lone-pair shapes; m21 electron-pair vs. molecular geometry; m22 polar molecules.
Keys are computed here from lewis.py structures: steric numbers from the drawn bonds and lone pairs, shape names from
the lecture's table (Day 10 p.26, plus SN 5 with three lone pairs from Day 10 p.23), polar/nonpolar from a symmetry
rule, angles from ideal coordinates. check_problem_bank_i.py re-derives every key a different way (repulsion-minimized
electron-pair positions, shape names from bond-angle signatures, and Δχ-weighted bond-vector sums)."""
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

I_START = len(PROBLEMS)
EN = ELECTRONEGATIVITY                                                 # course values (Day 9 p.17)

# ------------------------------------------------------------------ VSEPR bookkeeping from the Lewis structures
EPG = {2: "linear", 3: "trigonal planar", 4: "tetrahedral", 5: "trigonal bipyramidal", 6: "octahedral"}
# molecular geometry by (SN, lone pairs on the central atom): Day 10 p.26, plus SN 5 with three lone pairs (Day 10 p.23)
MG = {(2, 0): "linear", (3, 0): "trigonal planar", (3, 1): "bent", (4, 0): "tetrahedral", (4, 1): "trigonal pyramidal",
      (4, 2): "bent", (5, 0): "trigonal bipyramidal", (5, 1): "seesaw", (5, 2): "T-shaped", (5, 3): "linear",
      (6, 0): "octahedral", (6, 1): "square pyramidal", (6, 2): "square planar", (6, 3): "T-shaped"}
SYMMETRIC = {"linear", "trigonal planar", "tetrahedral", "trigonal bipyramidal", "octahedral", "square planar"}


def vsepr(sid):
    s = LW.STRUCTS[sid]
    c = s.central[0]
    nb = sorted({j if i == c else i for i, j, _ in s.bonds if c in (i, j)})
    lp = s.lp.get(c, 0)
    sn = len(nb) + lp
    return {"sn": sn, "atoms": len(nb), "lp": lp, "epg": EPG[sn], "mg": MG[(sn, lp)],
            "outer": [s.atoms[k][0] for k in nb], "center": s.atoms[c][0]}


def is_polar(sid):
    """identical outer atoms in a symmetric arrangement → the bond dipoles cancel; anything else → polar
    (true for every molecule used here; check_problem_bank_i.py sums the bond vectors to confirm)."""
    v = vsepr(sid)
    return not (len(set(v["outer"])) == 1 and v["mg"] in SYMMETRIC)


def name_choice(key, *opts):
    """opts: (name, feedback); the option whose name equals the computed key is the correct one."""
    assert sum(1 for n, _ in opts if n == key) == 1, (key, [n for n, _ in opts])
    return choice(*[(n, n == key, fb) for n, fb in opts])


def pol_choice(sid, fb_polar, fb_nonpolar):
    k = is_polar(sid)
    return choice(("polar", k, fb_polar), ("nonpolar", not k, fb_nonpolar))


def dchi(a, b):
    return round(abs(EN[a] - EN[b]), 2)


def ang(u, v):
    d = sum(a * b for a, b in zip(u, v)) / math.sqrt(sum(a * a for a in u) * sum(b * b for b in v))
    return round(math.degrees(math.acos(max(-1.0, min(1.0, d)))), 2)


# ideal trigonal bipyramid: two axial positions, three equatorial
TBP = [(0, 0, 1), (0, 0, -1)] + [(math.cos(math.radians(t)), math.sin(math.radians(t)), 0) for t in (0, 120, 240)]
A_AX_EQ, A_EQ_EQ, A_AX_AX = ang(TBP[0], TBP[2]), ang(TBP[2], TBP[3]), ang(TBP[0], TBP[1])
N90_EQ = sum(1 for j in range(5) if j != 2 and abs(ang(TBP[2], TBP[j]) - 90) < 0.01)
N90_AX = sum(1 for j in range(5) if j != 0 and abs(ang(TBP[0], TBP[j]) - 90) < 0.01)
assert (A_AX_EQ, A_EQ_EQ, A_AX_AX, N90_EQ, N90_AX) == (90, 120, 180, 2, 3)
IDEAL = {2: 180, 3: 120, 4: 109.5}                                     # Day 10 p.9-11


def sn_rows(sids):
    return [{"html": f"{LW.STRUCTS[s].formula_html} {LS(s, scale=0.55)}", "answer": str(vsepr(s)["sn"])} for s in sids]


SN_OPTS = [{"key": str(k), "html": str(k)} for k in range(2, 7)]
RES = "<span class='lw-arrow' role='img' aria-label='resonance arrow'>↔</span>"
# ideal tetrahedron: Δχ-weighted bond vectors (outer atoms in this vertex order), for the direction items
TET = [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]


def toward(center, outer, el):
    """does the Δχ bond-vector sum on an ideal tetrahedron point toward the `el` atoms?"""
    net = [sum((EN[o] - EN[center]) * u[k] for o, u in zip(outer, TET)) for k in range(3)]
    side = [sum(u[k] for o, u in zip(outer, TET) if o == el) for k in range(3)]
    return sum(a * b for a, b in zip(net, side)) > 1e-9


def lp_bp_90(lp_idx):
    """90° lone pair–bonding pair contacts on the ideal trigonal bipyramid with lone pairs at lp_idx (0, 1 axial)."""
    return sum(1 for i in lp_idx for j in range(5) if j not in lp_idx and abs(ang(TBP[i], TBP[j]) - 90) < 0.01)


def lp_lp_90(lp_idx):
    return sum(1 for a in lp_idx for b in lp_idx if a < b and abs(ang(TBP[a], TBP[b]) - 90) < 0.01)
GEO_KEY = {"linear": "lin", "bent": "bent", "trigonal planar": "tpl", "trigonal pyramidal": "tpy", "tetrahedral": "td",
           "T-shaped": "t", "seesaw": "ss", "square planar": "sqp", "square pyramidal": "sqpy", "octahedral": "oh",
           "trigonal bipyramidal": "tbp"}
POL_OPTS = [{"key": "polar", "html": "polar"}, {"key": "nonpolar", "html": "nonpolar"}]


def pol_rows(sids, html=None):
    html = html or {}
    return [{"html": html.get(s, LW.STRUCTS[s].formula_html), "answer": "polar" if is_polar(s) else "nonpolar"} for s in sids]


# =====================================================================================
# m20  Molecular shape and VSEPR: steric number (Day 10 p.3, p.6-13; textbook §5.1-5.2, PDF p.232-237)
# =====================================================================================
V_HCN = vsepr("HCN")
assert V_HCN["sn"] == 2 and V_HCN["mg"] == "linear"
add(id="m20-attempt", module="m20", kind="attempt", level="Guided attempt",
    prompt=f"<p>Hydrogen cyanide, HCN, has this Lewis structure:</p><p>{LS('HCN', scale=0.85)}</p>"
           "<p>(a) What is the steric number of the central C atom? (b) Predict the H–C–N bond angle.</p>",
    answer={"type": "multi", "parts": [
        {"label": "(a) steric number of C", **tnum(V_HCN["sn"], traps=[
            (4, "That counts the bond lines: one for C–H and three for C≡N. The three pairs of a triple bond all lie between the same two nuclei, so together they are one region, one direction."),
            (5, "That adds N's lone pair. It belongs to N, not to the central C.")])},
        {"label": "(b) H–C–N angle", **tnum(IDEAL[V_HCN["sn"]], unit_label="°", traps=[
            (109.5, "That's the tetrahedral angle, from counting four bonds (SN 4). C has only two regions."),
            (120, "That's the angle for three regions. Count again: one toward H, one toward N.")])}]},
    hints=["Concept: VSEPR spreads the regions of electron density around the central atom as far apart as possible (Day 10 p.8). The steric number counts those regions: “In how many <em>directions</em> are there electrons?” (Day 10 p.9)",
           "Relationship: each lone pair on the central atom is one region, and so is each bond to a neighboring atom, however many shared pairs it has.",
           "Setup: from C, electrons point toward H (the single bond) and toward N (the triple bond). C has no lone pair.",
           "Near-complete: two regions get farthest apart on opposite sides of C, CO<sub>2</sub>'s arrangement (Day 10 p.10). What angle is that?"],
    solution="<p>(a) <strong>SN 2</strong>: one region toward H and one toward N; C has no lone pair. (b) <strong>180°</strong>. Two regions sit on opposite sides of C, so HCN is <strong>linear</strong>, like CO<sub>2</sub> (Day 10 p.10).</p>"
             "<p>The three shared pairs of the triple bond don't spread out on their own: all three are held between the same two nuclei, so they point in one direction. Each C=O in CO<sub>2</sub> works the same way.</p>"
             "<p class='bg'>Measured, HCN is linear.</p>",
    compare={"wrong": "<p>“C makes four bonds, one single plus a triple, so SN = 4: tetrahedral, 109.5°.”</p>",
             "tempting": "Counting four bonds to carbon works for CH<sub>4</sub> and CCl<sub>4</sub>, where every bond is single, and C does have an octet here.",
             "fails": "The steric number counts directions, not lines or electrons. The triple bond's three pairs all point from C toward N: one region. With only two regions, C's electrons sit on opposite sides, 180° apart, so the molecule is linear."},
    source="Day 10 p.8–10; " + tb("5.2", 234, 235))

add(id="m20-p1", module="m20", kind="practice", level="Warm-up",
    prompt="<p>Which description matches the lecture's <em>steric number</em> (Day 10 p.9)?</p>",
    answer=choice(("How many regions of high electron density surround the central atom: in how many directions there are electrons", True,
                   "Right: both of the professor's phrasings (Day 10 p.9)."),
                  ("How many bond lines the central atom has", False, "A double or triple bond is several lines but one region: CO<sub>2</sub>'s C has four lines and SN 2."),
                  ("How many valence electrons surround the central atom", False, "That's a different count: B in BF<sub>3</sub> has 6 electrons and SN 3; S in SF<sub>6</sub> has 12 and SN 6."),
                  ("How many atoms are in the molecule", False, "Only what surrounds the central atom counts: the atoms bonded to it and its own lone pairs.")),
    hints=["Day 10 p.9 gives the definition two ways; the second one asks about directions."],
    solution="<p>The steric number is “how many regions of high electron density surround the central atom / Or / In how many <em>directions</em> are there electrons?” (Day 10 p.9). "
             "Each lone pair on the central atom is one region, and so is each bond to a neighboring atom, single, double, or triple. The summary table calls the regions “electron domains” (Day 10 p.26).</p>",
    source="Day 10 p.9, p.26")

SN_SIDS = ["AlCl3", "AlCl4-", "NO2+", "PCl5", "SO4-exp"]
add(id="m20-p2", module="m20", kind="practice", level="Concept",
    prompt="<p>Give the steric number of the central atom in each Lewis structure.</p>",
    answer={"type": "match", "rows": sn_rows(SN_SIDS), "options": SN_OPTS},
    hints=["Around the central atom only, count each bond to an atom (whatever its order) and each lone pair.",
           "None of these central atoms has a lone pair, so SN = the number of atoms bonded to it."],
    solution="<p>" + "; ".join(f"{LW.STRUCTS[s].formula_html}: {vsepr(s)['atoms']} atoms, no lone pair → SN {vsepr(s)['sn']}" for s in SN_SIDS) + ". "
             "Adding a chloride ion to AlCl<sub>3</sub> (Day 9 p.27) adds a fourth region and completes Al's octet. NO<sub>2</sub><sup>+</sup>'s two double bonds count once each. "
             "Sulfate's expanded-octet structure puts 12 electrons around S (Day 9 p.30), but they still point in only four directions.</p>",
    source="Day 10 p.9; Day 9 p.27–30")

assert vsepr("HCO2-1")["sn"] == vsepr("HCO2-2")["sn"] == 3 and vsepr("HCO2-1")["mg"] == "trigonal planar"
add(id="m20-p3", module="m20", kind="practice", level="Concept",
    prompt=f"<p>The formate ion, HCO<sub>2</sub><sup>−</sup>, has two resonance structures:</p><div class='lw-row'>{LS('HCO2-1', scale=0.7)}{RES}{LS('HCO2-2', scale=0.7)}</div>"
           "<p>(a) What is C's steric number in the first structure? (b) In the second? (c) Predict the O–C–O bond angle.</p>",
    answer={"type": "multi", "parts": [
        {"label": "(a) SN of C, first structure", **tnum(vsepr("HCO2-1")["sn"], traps=[(4, "The C=O double bond is one region, not two.")])},
        {"label": "(b) SN of C, second structure", **tnum(vsepr("HCO2-2")["sn"], traps=[(4, "The C=O double bond is one region, not two.")])},
        {"label": "(c) O–C–O angle", **choice(("about 109.5°", False, "That's SN 4. C has three regions in both structures."),
                                             ("about 120° in one structure and about 109.5° in the other", False,
                                              "Resonance structures differ only in where the electrons are (Day 9 p.8); the atoms, and the directions around C, are the same in both."),
                                             ("about 120°, the same for both structures", True, "Right: SN 3, trigonal planar, whichever structure you draw."),
                                             ("180°", False, "That's SN 2."))}]},
    hints=["Around C, in each structure: a bond to H, bonds to two O atoms, no lone pair.",
           "Resonance moves electrons, not atoms (Day 9 p.8). Does that change the number of directions around C?"],
    solution="<p>(a) and (b) <strong>SN 3</strong> in both: C is bonded to H and to two O atoms and has no lone pair, whichever O has the double bond. "
             "(c) About 120°: <strong>trigonal planar</strong> either way. The real ion is the average of the two structures (Day 9 p.9–10), with two identical C–O bonds; resonance changes bond orders, not the shape. "
             "The textbook makes the same point for ozone, whose central O has an SN of 3 “in both resonance structures” (PDF p.238).</p>"
             "<p class='bg'>The real ion's O–C–O angle is somewhat larger than 120°: each C–O bond is partly double, so the two of them "
             "repel each other more than either repels C–H, the formaldehyde argument of Day 10 p.13. VSEPR's prediction, about 120°, "
             "is what the question asks for.</p>",
    source="Day 9 p.8–10; Day 10 p.9–10, p.13; " + tb("5.2", 238))

add(id="m20-p4", module="m20", kind="practice", level="Standard",
    prompt="<p>PF<sub>5</sub> (Day 10 p.12) is trigonal bipyramidal, with two kinds of F positions, axial and equatorial (the terms on Day 10 p.20). "
           "(a) How many F atoms are axial? (b) What is the angle between an axial and an equatorial P–F bond? (c) Between two equatorial bonds? (d) Between the two axial bonds?</p>",
    answer={"type": "multi", "parts": [
        {"label": "(a) axial F atoms", **tnum(2, traps=[(3, "Three is the equatorial set, the triangle around the middle of P. The axial F atoms are the two on the vertical axis.")])},
        {"label": "(b) axial–equatorial angle", **tnum(A_AX_EQ, unit_label="°", traps=[(120, "120° is between two equatorial bonds.")])},
        {"label": "(c) equatorial–equatorial angle", **tnum(A_EQ_EQ, unit_label="°", traps=[(90, "90° is between an axial and an equatorial bond.")])},
        {"label": "(d) axial–axial angle", **tnum(A_AX_AX, unit_label="°", traps=[(90, "The two axial bonds point in opposite directions.")])}]},
    hints=["Picture two triangular pyramids sharing a base: the base corners are equatorial, the two tips axial.",
           "The equatorial bonds lie in one plane with P, evenly spaced; the axial bonds are perpendicular to that plane, one up and one down."],
    solution="<p>(a) <strong>2</strong> axial F atoms, one above and one below; the other 3 are equatorial. (b) <strong>90°</strong> and (c) <strong>120°</strong>, the two angles marked on Day 10 p.12. "
             "(d) <strong>180°</strong>: the axial bonds point in opposite directions (stated in the textbook, PDF p.234).</p>"
             "<p>The two kinds of position matter as soon as one of them holds a lone pair (Day 10 p.20–23).</p>",
    source="Day 10 p.12, p.20; " + tb("5.2", 234))

V_BCl3 = vsepr("BCl3")
add(id="m20-p5", module="m20", kind="practice", level="Standard",
    prompt=f"<p>Boron trichloride is one of the lecture's electron-deficient molecules: B ends up with only six valence electrons (Day 9 p.27).</p><p>{LS('BCl3', scale=0.75)}</p>"
           "<p>(a) What is B's steric number? (b) Name the molecular geometry. (c) Predict the Cl–B–Cl bond angle.</p>",
    answer={"type": "multi", "parts": [
        {"label": "(a) steric number of B", **tnum(V_BCl3["sn"], traps=[(4, "Four needs a fourth region. B has three bonds and no lone pair; a missing octet doesn't add a direction.")])},
        {"label": "(b) molecular geometry", **name_choice(V_BCl3["mg"],
            ("trigonal pyramidal", "A pyramid needs a lone pair on the central atom (SN 4, like NH<sub>3</sub>). B has none."),
            ("trigonal planar", "Right: three regions, no lone pair."),
            ("tetrahedral", "That's SN 4. An incomplete octet still means three regions."),
            ("T-shaped", "T-shaped is SN 5 with two lone pairs."))},
        {"label": "(c) Cl–B–Cl angle", **tnum(IDEAL[V_BCl3["sn"]], unit_label="°", traps=[(109.5, "109.5° is the tetrahedral angle (SN 4).")])}]},
    hints=["Count regions on B, not electrons.", "Three regions spread out in a plane, like BF<sub>3</sub> (Day 10 p.10)."],
    solution="<p>(a) <strong>SN 3</strong>. (b) <strong>Trigonal planar</strong>. (c) <strong>120°</strong>. B's three bonds are its only regions: the place where an octet's fourth pair “should” be isn't a region. "
             "It's the arrangement of BF<sub>3</sub>, the lecture's SN 3 example (Day 10 p.10).</p>",
    source="Day 9 p.27; Day 10 p.9–10")

HCH = 118                                                               # Day 10 p.13
HCO = (360 - HCH) / 2
add(id="m20-p6", module="m20", kind="practice", level="Stretch",
    prompt="<p>Formaldehyde, H<sub>2</sub>C=O, is planar, and the lecture gives its H–C–H angle as “about 118°” (Day 10 p.13). "
           "(a) Which is larger, the H–C–H angle or each H–C=O angle? (b) The three angles around a planar atom add up to 360°. Estimate each H–C=O angle.</p>",
    answer={"type": "multi", "parts": [
        {"label": "(a) the larger angle", **choice(("the H–C–H angle", False, "H–C–H is the angle squeezed below 120° (Day 10 p.13)."),
                                                 ("each H–C=O angle", True, "Right: the double bond pushes both C–H bonds away from itself, toward each other."),
                                                 ("all three are 120°", False, "That's the ideal trigonal planar value; the double bond's stronger repulsion distorts it (Day 10 p.13)."))},
        {"label": "(b) each H–C=O angle", **num_ans(HCO, tol=0.005, unit_label="°"),
         "traps": [{"value": 118, "tol": 0.001, "message": "That's the H–C–H angle itself."},
                   {"value": 120, "tol": 0.001, "message": "That's the ideal value. If H–C–H closes to 118°, the other two angles must open up."}]}]},
    hints=["Double bonds “repel the other electrons more strongly” (Day 10 p.13).", "360° − 118° is shared equally by the two H–C=O angles."],
    solution=f"<p>(a) Each <strong>H–C=O</strong> angle. The double bond's extra electrons push both C–H bonds away from it, which closes the H–C–H angle. "
             f"(b) (360° − {HCH}°)/2 = <strong>{HCO:.0f}°</strong>.</p>"
             "<p>The textbook says the same thing: H–C–H “slightly smaller than the 120°” and the H–C=O angles “about 1° larger” (PDF p.237). "
             "<span class='bg'>Measured values are about 116.5° and 121.8°.</span></p>",
    source="Day 10 p.13; " + tb("5.2", 237))

E_AROUND = 10
assert LW.STRUCTS["PF5"].shell(0) == E_AROUND and vsepr("PF5")["sn"] == E_AROUND // 2
add(id="m20-p7", module="m20", kind="practice", level="Standard",
    prompt=f"<p>A central atom has only single bonds, no lone pairs, and {E_AROUND} electrons around it. "
           "(a) What is its steric number? (b) Name its electron-pair geometry. (c) Which of the lecture's molecules has a central atom like this?</p>",
    answer={"type": "multi", "parts": [
        {"label": "(a) steric number", **tnum(E_AROUND // 2, traps=[(E_AROUND, "That's the number of electrons. Here each region is one shared pair, 2 electrons."),
                                                                   (4, "Four regions would hold 8 electrons, an octet.")])},
        {"label": "(b) electron-pair geometry", **name_choice(EPG[E_AROUND // 2],
            ("octahedral", "That's SN 6, 12 electrons."),
            ("trigonal bipyramidal", "Right: five regions."),
            ("tetrahedral", "That's SN 4, an octet."),
            ("trigonal planar", "That's SN 3, 6 electrons."))},
        {"label": "(c) a lecture example", **choice(("BF<sub>3</sub>", False, "B has 6 electrons around it (SN 3, Day 9 p.27)."),
                                                  ("CCl<sub>4</sub>", False, "C has an octet (SN 4)."),
                                                  ("PF<sub>5</sub>", True, "Right: five P–F bonds, 10 electrons, an expanded octet (Day 9 p.29; Day 10 p.12)."),
                                                  ("SF<sub>6</sub>", False, "S has 12 electrons around it (SN 6)."))}]},
    hints=["With single bonds only and no lone pairs, every region is one shared pair of electrons.", "Regions = electrons ÷ 2."],
    solution=f"<p>(a) {E_AROUND} electrons ÷ 2 per bond = <strong>SN {E_AROUND // 2}</strong>. (b) <strong>Trigonal bipyramidal</strong>. (c) <strong>PF<sub>5</sub></strong> (Day 10 p.12). "
             "More than an octet is the expanded octet of Day 9 p.29–30, and fewer, like BF<sub>3</sub>'s 6, is the electron-deficient case of Day 9 p.27: either way the steric number is just the count of pairs.</p>",
    source="Day 9 p.27–30; Day 10 p.9–12")

P(id="m20-p8", module="m20", kind="practice", level="Textbook preview",
  prompt="<p>Day 10 p.11 draws CCl<sub>4</sub> with plain lines, a solid wedge, and a dashed wedge. In the textbook's convention, what does the solid wedge mean?</p>",
  answer=choice(("a bond going into the page, away from you", False, "That's the dashed wedge."),
                ("a bond in the plane of the page", False, "That's a plain line."),
                ("a bond coming out of the page, toward you", True, "Right (PDF p.236)."),
                ("a double bond", False, "Wedges show direction in space, not bond order.")),
  hints=["Think of the wedge widening as the bond comes closer to you."],
  solution="<p>Solid wedge: <strong>toward the viewer</strong>. Dashed wedge: into the page. Plain line: in the plane of the page (textbook PDF p.236). "
           "In the CCl<sub>4</sub> drawing, C and two Cl atoms lie in the page, one Cl points toward you, and one away: the four corners of a tetrahedron.</p>",
  source=tb("5.2", 236) + "; drawn on Day 10 p.11")

V_COCl2 = vsepr("COCl2")
add(id="m20-transfer", module="m20", kind="transfer", level="Transfer",
    prompt="<p>Phosgene, COCl<sub>2</sub>, a toxic gas, has C bonded to O and to two Cl atoms. Draw its Lewis structure (24 valence electrons). "
           "(a) What is C's steric number? (b) Name the molecular geometry. (c) Is the Cl–C–Cl angle larger than, equal to, or smaller than 120°?</p>",
    answer={"type": "multi", "parts": [
        {"label": "(a) steric number of C", **tnum(V_COCl2["sn"], traps=[(4, "C has four bonding pairs (a double bond and two singles), but the double bond is one region.")])},
        {"label": "(b) molecular geometry", **name_choice(V_COCl2["mg"],
            ("tetrahedral", "That counts the C=O as two regions."),
            ("trigonal pyramidal", "C has no lone pair to make a pyramid."),
            ("bent", "Bent needs a lone pair on the central atom."),
            ("trigonal planar", "Right: three regions, no lone pair."))},
        {"label": "(c) Cl–C–Cl compared with 120°", **choice(("larger than 120°", False, "The double bond pushes the C–Cl bonds together, not apart."),
                                                            ("equal to 120°", False, "That's the ideal; the double bond's stronger repulsion changes it, as in formaldehyde (Day 10 p.13)."),
                                                            ("smaller than 120°", True, "Right: the formaldehyde argument (Day 10 p.13)."))}]},
    hints=["Lewis structure first (Day 10 p.8): C, with the largest bonding capacity, goes in the middle (Day 8 p.21). With single bonds only, C would have just 6 electrons, "
           "so one bond must be double. Which one gives every atom a formal charge of zero (Day 9 p.23)?",
           "24 electrons: a C=O double bond and two C–Cl single bonds, with 2 lone pairs on O and 3 on each Cl (8 bonding + 16 lone-pair electrons).",
           "Count C's regions: toward O (one region, though it's a double bond) and toward each Cl.",
           "Formaldehyde's double bond squeezes its H–C–H angle to about 118° (Day 10 p.13)."],
    solution=f"<div class='lw-row'>{LS('COCl2', scale=0.8)}</div>"
             "<p>(a) <strong>SN 3</strong>: three neighbors, no lone pair on C. (b) <strong>Trigonal planar</strong>. (c) <strong>Smaller</strong> than 120°: "
             "the C=O double bond repels the two C–Cl bonds more strongly than they repel each other, the formaldehyde argument (Day 10 p.13).</p>"
             "<p class='bg'>Measured: Cl–C–Cl ≈ 112°, Cl–C=O ≈ 124°.</p>",
    source="Day 10 p.8–13; Day 8 p.21; Day 9 p.23")

add(id="m20-m-explain", module="m20", kind="mastery", level="Explain",
    prompt="<p>Explain why the steric number, not the number of electrons around the central atom, decides the electron-pair geometry. Use BF<sub>3</sub>, SF<sub>6</sub>, and CO<sub>2</sub> as examples.</p>",
    answer={"type": "self", "model": "<p>VSEPR says the electron pairs around a central atom repel and arrange themselves as far apart as possible (Day 10 p.8). What gets arranged is regions, the directions in which electrons point (Day 10 p.9): "
                                     "each lone pair and each bond to a neighbor, whatever its order. BF<sub>3</sub>'s boron has only six electrons (Day 9 p.27) but three regions, so it is trigonal planar, 120°. "
                                     "SF<sub>6</sub>'s sulfur has twelve (an expanded octet, Day 9 p.29) and six regions: octahedral, 90°. CO<sub>2</sub>'s carbon has eight electrons, four in each double bond, "
                                     "but only two regions, so it is linear, 180°. Counting electrons would give CO<sub>2</sub> and CCl<sub>4</sub> the same shape, which is wrong.</p>"},
    hints=[], solution="", source="Day 10 p.8–12; Day 9 p.27–30")

add(id="m20-m-recognize", module="m20", kind="mastery", level="Recognize",
    prompt="<p>Which question can't be answered from a Lewis structure alone, so that you need VSEPR?</p>",
    answer=choice(("Which atoms is C bonded to in CH<sub>2</sub>O?", False, "Connections are exactly what a Lewis structure shows."),
                  ("How many lone pairs does the O in H<sub>2</sub>O have?", False, "Lone pairs are drawn in the Lewis structure."),
                  ("What is the H–C–H bond angle in CH<sub>4</sub>?", True, "Right: a Lewis structure is flat, so angles need the 3-D arrangement (Day 10 p.7–8)."),
                  ("What is the formal charge on N in NH<sub>4</sub><sup>+</sup>?", False, "Formal charge is counted from the Lewis structure (Day 9 p.22).")),
    hints=["What does the flat CH<sub>4</sub> cross get wrong (Day 10 p.7)?"],
    solution="<p>The <strong>bond angle</strong>. A Lewis structure shows connections, lone pairs, and formal charges, but its angles are just how it was drawn: CH<sub>4</sub>'s cross shows 90°, while the real angle is 109.5° (Day 10 p.7). "
             "Angles and shapes need VSEPR, and VSEPR needs a valid Lewis structure (Day 10 p.8).</p>",
    source="Day 10 p.7–8; Day 9 p.22")

add(id="m20-m-sanity", module="m20", kind="mastery", level="Sanity check",
    prompt="<p>A classmate looks at CH<sub>4</sub>'s Lewis structure, a flat cross, and says the H–C–H angle must be 90°, since four bonds are “as far apart as possible” at the corners of a square. What's wrong?</p>",
    answer=choice(("Nothing: 90° is as far apart as four bonds can get.", False, "Only in a plane. In three dimensions the closest pair can be 109.5° apart."),
                  ("In three dimensions the four regions get farther apart, at the corners of a tetrahedron, 109.5° apart; the flat drawing only shows connections.", True, "Right (Day 10 p.7, p.10–11)."),
                  ("CH<sub>4</sub> is trigonal planar, so the angle is 120°.", False, "Trigonal planar is SN 3. CH<sub>4</sub>'s C has four regions."),
                  ("The angle is 180°, because opposite H atoms repel most.", False, "In a flat square, opposite pairs are 180° apart but neighbors only 90°. The tetrahedron makes all six angles 109.5°.")),
    hints=["Is the molecule stuck in the plane of the page?"],
    solution="<p>A Lewis structure is two-dimensional (Day 10 p.7). In three dimensions four regions can do better than 90°: at the corners of a tetrahedron the closest pairs are 109.5° apart, as CCl<sub>4</sub>'s wedge drawing shows (Day 10 p.10–11). "
             "That's why the measured H–C–H angle is 109.5°.</p>",
    source="Day 10 p.7, p.10–11")

# =====================================================================================
# m21  Lone pairs: electron-pair vs. molecular geometry (Day 10 p.14-26; textbook §5.2, PDF p.237-243)
# =====================================================================================
V_BrF4 = vsepr("BrF4-")
assert (V_BrF4["sn"], V_BrF4["epg"], V_BrF4["mg"]) == (6, "octahedral", "square planar")
add(id="m21-attempt", module="m21", kind="attempt", level="Guided attempt",
    prompt=f"<p>The tetrafluorobromate ion, BrF<sub>4</sub><sup>−</sup>, has this Lewis structure:</p><p>{LS('BrF4-', scale=0.8)}</p>"
           "<p>(a) What is the steric number of Br? (b) Name the electron-pair geometry. (c) Name the molecular geometry.</p>",
    answer={"type": "multi", "parts": [
        {"label": "(a) steric number of Br", **tnum(V_BrF4["sn"], traps=[
            (4, "That counts only the F atoms. Each of Br's two lone pairs is a region too."),
            (5, "Count again: four bonds plus two lone pairs.")])},
        {"label": "(b) electron-pair geometry", **name_choice(V_BrF4["epg"],
            ("tetrahedral", "That's SN 4: the count without Br's lone pairs."),
            ("trigonal bipyramidal", "That's SN 5."),
            ("octahedral", "Right: six regions."),
            ("square planar", "That's the molecular geometry. The electron-pair geometry includes the lone pairs."))},
        {"label": "(c) molecular geometry", **name_choice(V_BrF4["mg"],
            ("tetrahedral", "That's CF<sub>4</sub>'s shape, right only with no lone pairs on the central atom. Br has two."),
            ("seesaw", "Seesaw is SN 5 with one lone pair."),
            ("square pyramidal", "Square pyramidal is SN 6 with one lone pair."),
            ("square planar", "Right: with the two lone pairs opposite each other, the four F atoms form a flat square."))}]},
    hints=["Concept: lone pairs on the central atom are regions too, so they help set the electron-pair geometry; the molecular geometry describes the “atoms only” (Day 10 p.14, p.16).",
           "Relationship: SN = atoms bonded to Br + lone pairs on Br. Br brings 7 valence electrons and the charge adds 1: 8, of which 4 go into the bonds.",
           "Setup: SN 6 → octahedral electron pairs. With two lone pairs at SN 6, “things are again not equivalent” (Day 10 p.25).",
           "Near-complete: put the two lone pairs opposite each other, above and below Br. Where are the four F atoms then, and which shape on Day 10 p.25 is that?"],
    solution="<p>(a) <strong>SN 6</strong>: 4 F atoms + 2 lone pairs. (b) <strong>Octahedral</strong>. (c) The two lone pairs sit opposite each other, so the four F atoms lie in one plane around Br: "
             "<strong>square planar</strong> (Day 10 p.25), with 90° F–Br–F angles.</p>"
             "<p>Because the two lone pairs push equally from both sides, the angles stay at 90°; the textbook says this of square planar molecules (PDF p.242).</p>",
    compare={"wrong": "<p>“BrF<sub>4</sub><sup>−</sup> has four F atoms around Br, just like CF<sub>4</sub>, so it's tetrahedral with 109.5° angles.”</p>",
             "tempting": "The formula looks like CF<sub>4</sub>'s, and four bonded atoms gave a tetrahedron on Day 10 p.10–11 (CCl<sub>4</sub>).",
             "fails": "Those slides are all headed “Central Atom with No Lone Pairs.” Br has 7 valence electrons, plus 1 from the charge: 4 go into bonds and 4 stay on Br as two lone pairs, which are regions too. "
                      "Six regions make an octahedron; the two lone pairs take opposite positions, and the four F atoms are left in a flat square."},
    source="Day 10 p.14, p.24–26; " + tb("5.2", 242))

add(id="m21-p1", module="m21", kind="practice", level="Warm-up",
    prompt="<p>What does a <em>molecular</em> geometry describe?</p>",
    answer=choice(("the positions of all the bonding pairs and lone pairs", False, "That's the electron-pair geometry (Day 10 p.8)."),
                  ("the relative positions of the atoms only", True, "Right: “atoms only” is bold on Day 10 p.14 and p.16."),
                  ("the positions of the lone pairs only", False, "Lone pairs shape the molecule, but the name describes where the atoms are."),
                  ("the arrangement drawn in the Lewis structure", False, "A Lewis structure is flat and shows connections, not positions in space (Day 10 p.7).")),
    hints=["Day 10 p.8 defines both geometries; p.14 repeats one of them in bold."],
    solution="<p>“The molecular geometry describes relative positions of <strong>atoms only</strong>” (Day 10 p.14, p.16). The electron-pair geometry includes every region, lone pairs too (Day 10 p.8). "
             "When the central atom has lone pairs the two names differ.</p>",
    source="Day 10 p.8, p.14, p.16")

SN4_SIDS = ["PF3", "H2Se", "H3O+", "OF2", "BH4-"]
assert all(vsepr(s)["sn"] == 4 for s in SN4_SIDS)
GEO_OPTS4 = [{"key": GEO_KEY[n], "html": n} for n in ("tetrahedral", "trigonal pyramidal", "bent", "trigonal planar", "linear")]
add(id="m21-p2", module="m21", kind="practice", level="Concept",
    prompt="<p>In each of these species the central atom has a steric number of 4. Name each one's molecular geometry.</p>",
    answer={"type": "match", "rows": [{"html": LW.STRUCTS[s].formula_html, "answer": GEO_KEY[vsepr(s)["mg"]]} for s in SN4_SIDS], "options": GEO_OPTS4},
    hints=["Draw each Lewis structure and count the lone pairs on the central atom: 0, 1, or 2.",
           "SN 4 with 0 lone pairs → tetrahedral; 1 → trigonal pyramidal; 2 → bent (Day 10 p.26)."],
    solution="<div class='lw-row'>" + "".join(LS(s, scale=0.6) for s in SN4_SIDS) + "</div><p>"
             + "; ".join(f"{LW.STRUCTS[s].formula_html}: {vsepr(s)['atoms']} atoms + {vsepr(s)['lp']} lone pair{'s' if vsepr(s)['lp'] != 1 else ''} → {vsepr(s)['mg']}" for s in SN4_SIDS)
             + ". All five have a tetrahedral electron-pair geometry; only BH<sub>4</sub><sup>−</sup>'s molecular geometry is tetrahedral too.</p>",
    source="Day 10 p.16–19, p.26")

NH_SIDS = [("nh4", "NH4+", "NH<sub>4</sub><sup>+</sup>"), ("nh3", "NH3", "NH<sub>3</sub>"), ("nh2", "NH2-", "NH<sub>2</sub><sup>−</sup> (amide ion)")]
assert all(vsepr(s)["sn"] == 4 for _, s, _ in NH_SIDS)
NH_ORDER = [k for k, s, _ in sorted(NH_SIDS, key=lambda t: vsepr(t[1])["lp"])]  # more lone pairs → smaller angle
add(id="m21-p3", module="m21", kind="practice", level="Standard",
    prompt="<p>Rank these by H–N–H bond angle. In each, N has a steric number of 4.</p>",
    answer=order_ans([(k, h) for k, _, h in NH_SIDS], NH_ORDER, "largest H–N–H angle (1) to smallest (3)"),
    hints=["Count the lone pairs on N in each (NH<sub>2</sub><sup>−</sup> has 5 + 2 + 1 = 8 valence electrons).",
           "More lone pairs squeeze the bonding pairs more: 109.5° → 107° → 104.5° in the lecture's CH<sub>4</sub>, NH<sub>3</sub>, H<sub>2</sub>O (Day 10 p.7, p.18–19)."],
    solution=f"<div class='lw-row'>{LS('NH4+', scale=0.6)}{LS('NH3', scale=0.65)}{LS('NH2-', scale=0.65)}</div>"
             "<p><strong>NH<sub>4</sub><sup>+</sup> &gt; NH<sub>3</sub> &gt; NH<sub>2</sub><sup>−</sup></strong>: 0, 1, and 2 lone pairs on N. NH<sub>4</sub><sup>+</sup> is a regular tetrahedron (109.5°), NH<sub>3</sub> is 107° (Day 10 p.18), "
             "and NH<sub>2</sub><sup>−</sup> has water's count of bonds and lone pairs, so it's bent with an angle close to water's 104.5°.</p>"
             "<p>The textbook states the rule behind the ranking: two lone pairs push harder than one (PDF p.238).</p>",
    source="Day 10 p.7, p.16–19; " + tb("5.2", 238))

V_SeF4 = vsepr("SeF4")
add(id="m21-p4", module="m21", kind="practice", level="Standard",
    prompt=f"<p>Selenium tetrafluoride, SeF<sub>4</sub>:</p><p>{LS('SeF4', scale=0.75)}</p>"
           "<p>(a) What is Se's steric number? (b) Is the lone pair axial or equatorial? (c) Name the molecular geometry.</p>",
    answer={"type": "multi", "parts": [
        {"label": "(a) steric number of Se", **tnum(V_SeF4["sn"], traps=[(4, "That counts the F atoms only; Se's lone pair is a fifth region.")])},
        {"label": "(b) the lone pair's position", **choice(("axial", False, "The lecture's answer slide puts it equatorial (Day 10 p.22). The textbook's reason: an axial lone pair would have three neighbors at 90° instead of two (PDF p.241)."),
                                                         ("equatorial", True, "Right (Day 10 p.22)."))},
        {"label": "(c) molecular geometry", **name_choice(V_SeF4["mg"],
            ("tetrahedral", "Tetrahedral needs SN 4 with no lone pair."),
            ("square planar", "Square planar is SN 6 with two opposite lone pairs."),
            ("seesaw", "Right: Day 10 p.22 (“See-saw” in the p.26 table)."),
            ("trigonal pyramidal", "That's SN 4 with one lone pair."))}]},
    hints=["Se is in group 16 like O and S: 6 valence electrons, 4 of them used in bonds.", "One lone pair at SN 5 goes equatorial (Day 10 p.22)."],
    solution="<p>(a) <strong>SN 5</strong> (4 F + 1 lone pair): trigonal bipyramidal electron pairs. (b) <strong>Equatorial</strong>. (c) <strong>Seesaw</strong>: two axial F atoms and two equatorial F atoms (Day 10 p.22). "
             "Se is directly below S, and SeF<sub>4</sub> has the shape of the textbook's SF<sub>4</sub> (Sample Ex. 5.3, PDF p.242–243).</p>",
    source="Day 10 p.20–22, p.26; " + tb("5.2", 241, 243))

V_ClF5 = vsepr("ClF5")
assert (V_ClF5["sn"], V_ClF5["mg"]) == (6, "square pyramidal")
add(id="m21-p5", module="m21", kind="practice", level="Standard",
    prompt=f"<p>Chlorine pentafluoride, ClF<sub>5</sub>:</p><p>{LS('ClF5', scale=0.7)}</p>"
           "<p>(a) What is the steric number of Cl? (b) Does it matter which of the six positions the lone pair takes? (c) Name the molecular geometry.</p>",
    answer={"type": "multi", "parts": [
        {"label": "(a) steric number of Cl", **tnum(V_ClF5["sn"], traps=[(5, "Five F atoms, but Cl also has a lone pair: six regions.")])},
        {"label": "(b) the lone pair's position", **choice(("Yes: it must take an axial position.", False, "An octahedron has no separate axial and equatorial sets: all six positions are alike."),
                                                         ("No: all six positions are equivalent.", True, "Right: “It doesn't matter which position we replace with the lone pair!” (Day 10 p.24)."),
                                                         ("Yes: it must take an equatorial position.", False, "That's the rule for the trigonal bipyramid (SN 5). At SN 6 every position is the same."))},
        {"label": "(c) molecular geometry", **name_choice(V_ClF5["mg"],
            ("trigonal bipyramidal", "That's SN 5 with no lone pairs; Cl has six regions."),
            ("square pyramidal", "Right (Day 10 p.24)."),
            ("square planar", "Square planar is SN 6 with two lone pairs."),
            ("seesaw", "Seesaw is SN 5 with one lone pair."))}]},
    hints=["Cl: 7 valence electrons, 5 of them in bonds; the other 2 form a lone pair.", "SN 6 with one lone pair: Day 10 p.24."],
    solution="<p>(a) <strong>SN 6</strong> (5 F + 1 lone pair): octahedral electron pairs. (b) <strong>No</strong>: “Weirdly, all of the positions are now equivalent again” (Day 10 p.24). "
             "(c) <strong>Square pyramidal</strong>: four F atoms form the square base around Cl, and the fifth points straight out from it, opposite the lone pair.</p>",
    source="Day 10 p.24, p.26")

add(id="m21-p6", module="m21", kind="practice", level="Concept",
    signal="Posed on Day 10 p.20, just before a Top Hat slide (p.21) whose poll isn't in the PDF. The answer slides (p.22–23) show the lone pairs equatorial; this key follows them.",
    prompt="<p>“If we replace an atom in the trigonal bipyramid with a lone pair, will it occupy an axial or an equatorial position?” (Day 10 p.20)</p>",
    answer=choice(("an axial position", False, "The answer slides put it equatorial (Day 10 p.22). The textbook explains why: an axial position has three neighbors at 90°, an equatorial one only two, and pairs 90° apart repel most (PDF p.241)."),
                  ("an equatorial position", True, "Right: the answer slides put every lone pair equatorial (Day 10 p.22–23)."),
                  ("either one: all five positions are equivalent", False, "That's true of the octahedron with one lone pair (Day 10 p.24), not of the trigonal bipyramid, which has two kinds of position."),
                  ("it depends on which atoms are bonded", False, "VSEPR places the lone pairs the same way whatever the outer atoms are.")),
    hints=["On Day 10 p.20's drawing, how many neighbors does an axial position have at 90°, and how many does an equatorial one? "
           "(Counting 90° neighbors is the textbook's way to decide, PDF p.241.)"],
    solution="<p><strong>Equatorial.</strong> Day 10 p.22 shows one lone pair equatorial (seesaw), and p.23 shows two and three (T-shaped, linear). "
             "The reason, from the textbook: electron pairs 90° apart repel more than pairs 120° apart, and an equatorial position has two 90° neighbors while an axial position has three (PDF p.241).</p>",
    source="Day 10 p.20–23; " + tb("5.2", 241))

C_EQ2, C_AX2 = lp_bp_90((2, 3)), lp_bp_90((0, 1))
assert (C_EQ2, C_AX2, lp_lp_90((2, 3)), lp_lp_90((0, 1))) == (4, 6, 0, 0)
P(id="m21-p7", module="m21", kind="practice", level="Textbook preview",
  prompt="<p>The textbook counts 90° contacts to explain the lecture's choice (PDF p.241). Apply it to SN 5 with <em>two</em> lone pairs in two arrangements: "
         "(i) both lone pairs equatorial; (ii) both lone pairs axial. Neither arrangement puts the two lone pairs 90° apart. "
         "(a) In (i), how many lone pair–bonding pair contacts are there at 90°? Count each lone pair's 90° neighbors and add them, so a bonding pair next to both lone pairs counts twice. "
         "(b) The same count in (ii)? (c) Which arrangement does VSEPR predict, and what shape results?</p>",
  answer={"type": "multi", "parts": [
      {"label": "(a) 90° contacts, both lone pairs equatorial", **tnum(C_EQ2, traps=[(2, "That's one lone pair's count. Add the other lone pair's: each equatorial lone pair has two axial neighbors at 90°."),
                                                                               (6, "That's the axial arrangement.")])},
      {"label": "(b) 90° contacts, both lone pairs axial", **tnum(C_AX2, traps=[(3, "That's one lone pair's count. Each axial lone pair has three equatorial neighbors at 90°."),
                                                                          (4, "That's the equatorial arrangement.")])},
      {"label": "(c) the predicted arrangement", **choice(("(ii), giving a trigonal planar molecule", False, "Six 90° contacts against four: the axial arrangement repels more, so it isn't observed."),
                                                        ("(i), giving a trigonal planar molecule", False, "With both lone pairs equatorial, the atoms sit in the two axial positions and one equatorial one: a T, not a triangle."),
                                                        ("(i), giving a T-shaped molecule", True, "Right: fewer 90° contacts (Day 10 p.23)."),
                                                        ("(ii), giving a T-shaped molecule", False, "With both lone pairs axial, the three atoms would all be equatorial: a flat triangle. And that arrangement has more 90° contacts."))}]},
  hints=["An equatorial position is 90° from the two axial positions; an axial position is 90° from all three equatorial positions.",
         "Count each lone pair's 90° neighbors that are bonding pairs, then add the two lone pairs' counts."],
  solution=f"<p>(a) <strong>{C_EQ2}</strong>: each equatorial lone pair is 90° from the two axial bonding pairs. (b) <strong>{C_AX2}</strong>: each axial lone pair is 90° from all three equatorial bonding pairs. "
           "(c) Fewer 90° repulsions win: <strong>both lone pairs equatorial</strong>, which leaves the three atoms in a T (Day 10 p.23). "
           "The rule behind it: “the repulsions between pairs of electrons increase as the angle between them decreases” (PDF p.241).</p>",
  source=tb("5.2", 241) + "; Day 10 p.20–23")

V_KrF2 = vsepr("KrF2")
assert (V_KrF2["sn"], V_KrF2["mg"]) == (5, "linear")
add(id="m21-p8", module="m21", kind="practice", level="Standard",
    prompt=f"<p>Krypton difluoride, KrF<sub>2</sub>, one of the few compounds of krypton:</p><p>{LS('KrF2', scale=0.75)}</p>"
           "<p>(a) What is the steric number of Kr? (b) Name the molecular geometry. (This is the case the Day 10 p.26 table leaves out.)</p>",
    answer={"type": "multi", "parts": [
        {"label": "(a) steric number of Kr", **tnum(V_KrF2["sn"], traps=[(2, "Count Kr's three lone pairs too."), (3, "Three lone pairs + two F atoms.")])},
        {"label": "(b) molecular geometry", **name_choice(V_KrF2["mg"],
            ("bent", "Bent comes from SN 3 or SN 4. Here the lone pairs fill all three equatorial positions, leaving the F atoms opposite each other."),
            ("T-shaped", "T-shaped is SN 5 with two lone pairs: three atoms, not two."),
            ("linear", "Right: three equatorial lone pairs leave the two F atoms axial, 180° apart (Day 10 p.23)."),
            ("trigonal planar", "Only two atoms are bonded to Kr."))}]},
    hints=["Kr, a noble gas, has 8 valence electrons: 2 go into the two bonds and 6 stay as three lone pairs.", "Three lone pairs at SN 5 all go equatorial (Day 10 p.23)."],
    solution="<p>(a) <strong>SN 5</strong> (2 F + 3 lone pairs). (b) <strong>Linear</strong>, F–Kr–F = 180°: the three lone pairs take the equatorial triangle and the two F atoms the axial positions (Day 10 p.23, bottom row). "
             "The textbook's example of this geometry is XeF<sub>2</sub>, the fluoride of krypton's heavier neighbor in group 18 (Table 5.1, PDF p.240).</p>",
    source="Day 10 p.23, p.26; " + tb("5.2", 240, 242))

DIST = {1: "smaller than 90°", 2: "exactly 90°"}      # one lone pair pushes from one side; two opposite ones balance (TB PDF p.242)
DIST_OPTS = ("larger than 90°", "exactly 90°", "smaller than 90°")
assert vsepr("ICl4-")["lp"] == 2


def dist_choice(n_lp, fb):
    return choice(*[(o, o == DIST[n_lp], fb[o]) for o in DIST_OPTS])


P(id="m21-p9", module="m21", kind="practice", level="Stretch",
  prompt="<p>Work out the shapes of the ions TeF<sub>5</sub><sup>−</sup> and ICl<sub>4</sub><sup>−</sup> from their Lewis structures (Te is in group 16, I in group 17). "
         "Then predict how the angles between neighboring outer atoms, ideally 90°, compare with 90°: (a) the F–Te–F angles in TeF<sub>5</sub><sup>−</sup>; "
         "(b) the Cl–I–Cl angles in ICl<sub>4</sub><sup>−</sup>.</p>",
  answer={"type": "multi", "parts": [
      {"label": "(a) TeF<sub>5</sub><sup>−</sup>: angles between neighboring F atoms", **dist_choice(1, {
          "larger than 90°": "Te keeps one lone pair, below the square of four F atoms. It pushes them up, toward the fifth F and closer to each other, so the angles close.",
          "exactly 90°": "Only if something balanced the lone pair's push from the other side, as a second, opposite lone pair would.",
          "smaller than 90°": "Right: the textbook's BrF<sub>5</sub> has 85° (PDF p.242)."})},
      {"label": "(b) ICl<sub>4</sub><sup>−</sup>: angles between neighboring Cl atoms", **dist_choice(2, {
          "larger than 90°": "Four Cl atoms around a square can't all open past 90°: four 90° angles fill the full 360°.",
          "exactly 90°": "Right: the two lone pairs push equally from above and below.",
          "smaller than 90°": "That needs a lone pair on one side only. Here the two lone pairs sit on opposite sides and balance."})}]},
  hints=["Count each central atom's lone pairs: Te has 6 valence electrons and I has 7, and each ion's −1 charge adds one more. How many are left after the bonds?",
         "Name each shape (Day 10 p.24–25). Where is each lone pair, and is there one on each side of the square of four atoms?",
         "A lone pair on one side pushes the atoms of the square toward the other side; equal pushes from opposite sides balance."],
  solution="<p>TeF<sub>5</sub><sup>−</sup>: Te has 6 + 1 = 7 valence electrons, 5 of them in bonds, so it keeps one lone pair: SN 6, square pyramidal (Day 10 p.24). "
           "ICl<sub>4</sub><sup>−</sup>: I has 7 + 1 = 8, 4 of them in bonds, so it keeps two lone pairs: SN 6, square planar, with the lone pairs opposite each other (Day 10 p.25).</p>"
           "<p>(a) <strong>Smaller</strong> than 90°: the lone pair sits below the square and pushes its four F atoms up, toward the fifth F and closer to each other. "
           "The textbook says the angles of a square pyramidal molecule “should be slightly less than the ideal angle of 90°”; in BrF<sub>5</sub> the axial–equatorial angles are 85° (PDF p.242). "
           "(b) <strong>Exactly</strong> 90°: the two lone pairs sit on opposite sides of the square, so their pushes balance; square planar angles “are all 90° or 180°” (PDF p.242).</p>",
  source=tb("5.2", 242) + "; Day 10 p.24–25")

VS1, VS2 = vsepr("SO3-oct"), vsepr("SO3-exp")
assert VS1["mg"] == VS2["mg"]
add(id="m21-transfer", module="m21", kind="transfer", level="Transfer",
    prompt="<p>The sulfite ion, SO<sub>3</sub><sup>2−</sup>, is on the polyatomic-ion table (Day 8 p.8–9). Here are two Lewis structures for it, one with octets only and one with an S=O double bond (an expanded octet, Day 9 p.29):</p>"
           f"<div class='lw-row'>{LS('SO3-oct', scale=0.7)}{LS('SO3-exp', scale=0.7)}</div>"
           "<p>(a) What is S's steric number in the first structure? (b) In the second? (c) Name the ion's molecular geometry.</p>",
    answer={"type": "multi", "parts": [
        {"label": "(a) SN of S, octet structure", **tnum(VS1["sn"], traps=[(3, "S has three O neighbors and a lone pair: four regions.")])},
        {"label": "(b) SN of S, structure with S=O", **tnum(VS2["sn"], traps=[(5, "The S=O double bond is one region, not two.")])},
        {"label": "(c) molecular geometry", **name_choice(VS1["mg"],
            ("trigonal planar", "That's carbonate, CO<sub>3</sub><sup>2−</sup>, whose C has no lone pair. S in sulfite keeps one."),
            ("tetrahedral", "That's the electron-pair geometry. The shape names the atoms only."),
            ("trigonal pyramidal", "Right: three O atoms and a lone pair on S, like NH<sub>3</sub>."),
            ("T-shaped", "T-shaped needs SN 5."))}]},
    hints=["Find the lone pairs on S in each drawing.", "Bond orders don't change the number of regions."],
    solution="<p>(a) and (b) <strong>SN 4</strong> in both: three O atoms + one lone pair. Choosing the octet structure or the expanded-octet one changes bond orders and formal charges, not the number of directions around S. "
             "(c) <strong>Trigonal pyramidal</strong>, like NH<sub>3</sub> (Day 10 p.16–18). Carbonate, CO<sub>3</sub><sup>2−</sup>, has the same formula pattern but no lone pair on C, so it's trigonal planar.</p>",
    source="Day 10 p.16–18, p.26; Day 8 p.8–9; Day 9 p.29")

add(id="m21-m-explain", module="m21", kind="mastery", level="Explain",
    prompt="<p>Explain why ammonia's electron-pair geometry is tetrahedral but its molecular geometry is trigonal pyramidal, and why its bond angle is 107° rather than 109.5°.</p>",
    answer={"type": "self", "model": "<p>N in NH<sub>3</sub> has three bonds and one lone pair: four regions, SN 4, so the electron pairs point to the corners of a tetrahedron. That's the electron-pair geometry, which includes lone pairs (Day 10 p.8). "
                                     "The molecular geometry describes the atoms only (Day 10 p.16): one corner holds the lone pair, so N and the three H atoms form a pyramid on a triangular base, trigonal pyramidal. "
                                     "The lone pair takes up more room than a bonding pair (the slides draw ozone's lone pair as a large lobe pressing on its bonds, Day 10 p.15) and pushes the bonding pairs together, closing the H–N–H angle from 109.5° to 107° (Day 10 p.18).</p>"},
    hints=[], solution="", source="Day 10 p.8, p.15–18")

add(id="m21-m-recognize", module="m21", kind="mastery", level="Recognize",
    prompt="<p>Which pair of molecules has the same molecular geometry but different electron-pair geometries?</p>",
    answer=choice(("H<sub>2</sub>O and H<sub>2</sub>S", False, "Both are bent with SN 4: the same electron-pair geometry too."),
                  ("NH<sub>3</sub> and BF<sub>3</sub>", False, "Different molecular geometries: trigonal pyramidal vs. trigonal planar."),
                  ("CH<sub>4</sub> and XeF<sub>4</sub>", False, "Different molecular geometries: tetrahedral vs. square planar."),
                  ("CO<sub>2</sub> and XeF<sub>2</sub>", True, "Right: both linear, but CO<sub>2</sub>'s C has SN 2 and XeF<sub>2</sub>'s Xe has SN 5, with three equatorial lone pairs.")),
    hints=["Work out the SN and both geometry names for each molecule."],
    solution="<p><strong>CO<sub>2</sub> and XeF<sub>2</sub>.</strong> Both are linear, but CO<sub>2</sub> gets there with SN 2 (Day 10 p.10) and XeF<sub>2</sub> with SN 5 and three equatorial lone pairs (Day 10 p.23; textbook Table 5.1, PDF p.240). "
             "Ozone and water are the lecture's version of the same trap: both bent, from SN 3 and SN 4 (Day 10 p.19).</p>",
    source="Day 10 p.10, p.19, p.23; " + tb("5.2", 240))

add(id="m21-m-sanity", module="m21", kind="mastery", level="Sanity check",
    prompt="<p>A student reports the F–O–F angle in OF<sub>2</sub> as 125°, reasoning that O's two lone pairs push the F atoms apart. Is that reasonable?</p>",
    answer=choice(("Yes: lone pairs repel bonding pairs, so the angle opens past 120°.", False, "Lone pairs push the bonding pairs toward each other, which closes the angle between them."),
                  ("No: OF<sub>2</sub> is linear, 180°.", False, "Linear needs two regions; O has four."),
                  ("No: O has SN 4, so the ideal angle is 109.5°, and lone pairs push the bonding pairs together, making the angle smaller than 109.5°, not larger.", True, "Right: compare water's 104.5° (Day 10 p.19)."),
                  ("Yes: F atoms are big, so they need a wide angle.", False, "VSEPR's angle comes from the regions around O, and with two lone pairs it's below 109.5°.")),
    hints=["What are O's SN and its electron-pair geometry's ideal angle? Which way do lone pairs move a bond angle?"],
    solution="<p>O has 2 F atoms + 2 lone pairs: SN 4, tetrahedral electron pairs, ideal angle 109.5°. Lone pairs squeeze the angle below that, as in water (104.5°, Day 10 p.19). "
             "So 125° is impossible by VSEPR; expect something near water's angle. <span class='bg'>Measured: about 103°.</span></p>",
    source="Day 10 p.18–19, p.26")

# =====================================================================================
# m22  Polar bonds and polar molecules (Day 10 p.27-31; Day 11 p.6-8; textbook §5.3, PDF p.243-246)
# =====================================================================================
V_PCl3 = vsepr("PCl3")
assert V_PCl3["mg"] == "trigonal pyramidal" and is_polar("PCl3")
add(id="m22-attempt", module="m22", kind="attempt", level="Guided attempt",
    prompt=f"<p>Phosphorus trichloride, PCl<sub>3</sub>:</p><p>{LS('PCl3', scale=0.8)}</p>"
           "<p>(a) Name its molecular geometry. (b) Is the molecule polar or nonpolar? (χ: P 2.1, Cl 3.0; Day 9 p.17)</p>",
    answer={"type": "multi", "parts": [
        {"label": "(a) molecular geometry", **name_choice(V_PCl3["mg"],
            ("trigonal planar", "That ignores the lone pair on P. P has SN 4."),
            ("trigonal pyramidal", "Right: SN 4 with one lone pair."),
            ("tetrahedral", "That's the electron-pair geometry; the shape names the atoms only."),
            ("T-shaped", "T-shaped needs SN 5."))},
        {"label": "(b) polar or nonpolar", **pol_choice("PCl3", "Right: the three P–Cl dipoles all lean toward the Cl side of the pyramid, so they can't cancel.",
                                                          "Three identical bond dipoles cancel only when they're spread evenly in a plane, as in BF<sub>3</sub>. In a pyramid they all lean the same way.")}]},
    hints=["Concept: a molecule is polar when its bond dipoles don't cancel, and whether they cancel depends on the shape (Day 10 p.29–31).",
           f"Relationship: Δχ = 3.0 − 2.1 = {dchi('P', 'Cl')} for each P–Cl bond: polar, with each arrow pointing to Cl.",
           "Setup: P has 3 bonds + 1 lone pair, SN 4, so P and the three Cl atoms form a pyramid with P at the top.",
           "Near-complete: in a pyramid every bond dipole has a part pointing down toward the Cl atoms, and nothing points up to cancel it. Compare BF<sub>3</sub>, whose three equal dipoles lie flat, 120° apart."],
    solution=f"<p>(a) <strong>Trigonal pyramidal</strong> (SN 4: 3 Cl + 1 lone pair). (b) <strong>Polar</strong>. Each P–Cl bond is polar (Δχ = {dchi('P', 'Cl')}). "
             "In a flat triangle three equal dipoles would cancel, but in the pyramid only their sideways parts cancel; their downward parts add, so the bond dipoles don't cancel.</p>"
             "<p class='bg'>Measured dipole moment: about 0.56 D.</p>",
    compare={"wrong": "<p>“All three P–Cl bonds are the same, so their dipoles cancel, like BF<sub>3</sub>'s: PCl<sub>3</sub> is nonpolar.”</p>",
             "tempting": "Identical outer atoms did cancel in the lecture's nonpolar examples, CO<sub>2</sub> and CF<sub>4</sub> (Day 10 p.29–30), and in BF<sub>3</sub>.",
             "fails": "Cancellation needs a symmetric arrangement, not just identical bonds. P's lone pair makes PCl<sub>3</sub> a pyramid, so all three dipoles lean toward the same side, the way water's two O–H dipoles both lean toward O (Day 10 p.31)."},
    source="Day 10 p.16–18, p.29–31; Day 9 p.17; " + tb("5.3", 243, 244))

add(id="m22-p1", module="m22", kind="practice", level="Warm-up",
    prompt="<p>Which statement about polar bonds and polar molecules is correct?</p>",
    answer=choice(("A molecule with polar bonds is always polar.", False, "CO<sub>2</sub>'s bonds are polar (Δχ = 1.0), but “the two dipole moments are perfectly opposed” (Day 10 p.29)."),
                  ("A molecule is polar whenever its central atom is less electronegative than its outer atoms.", False, "That sets the direction of each bond dipole, not whether they cancel: C is less electronegative than F in nonpolar CF<sub>4</sub>."),
                  ("Only ionic compounds can be polar.", False, "Water is covalent and polar (Day 10 p.31)."),
                  ("A molecule with polar bonds is nonpolar if its bond dipoles cancel.", True, "Right: CO<sub>2</sub> and CF<sub>4</sub> (Day 10 p.29–30).")),
    hints=["Day 10 p.29–30: polar bonds, nonpolar molecules."],
    solution="<p>A molecule's polarity depends on its bond dipoles <strong>and</strong> its shape. CO<sub>2</sub> (linear) and CF<sub>4</sub> (tetrahedral) have polar bonds but are nonpolar; bent H<sub>2</sub>O is polar (Day 10 p.29–31).</p>",
    source="Day 10 p.29–31")

POL_SIDS = ["BF3", "NF3", "SF6", "OF2", "XeF2"]
assert [is_polar(s) for s in POL_SIDS] == [False, True, False, True, False]
add(id="m22-p2", module="m22", kind="practice", level="Standard",
    prompt="<p>Classify each molecule as polar or nonpolar.</p>",
    answer={"type": "match", "rows": pol_rows(POL_SIDS), "options": POL_OPTS},
    hints=["For each: Lewis structure → SN and lone pairs → shape (§5.2).",
           "Identical bond dipoles cancel only in a symmetric arrangement: linear, trigonal planar, tetrahedral, trigonal bipyramidal, octahedral, or square planar."],
    solution="<p>BF<sub>3</sub>: trigonal planar, three equal dipoles 120° apart → <strong>nonpolar</strong>. NF<sub>3</sub>: trigonal pyramidal (lone pair on N) → <strong>polar</strong>. "
             "SF<sub>6</sub>: octahedral, every S–F dipole canceled by the one opposite it → <strong>nonpolar</strong>. OF<sub>2</sub>: bent → <strong>polar</strong>. "
             "XeF<sub>2</sub>: linear, two equal Xe–F dipoles in opposite directions (its three lone pairs sit evenly around the middle) → <strong>nonpolar</strong>.</p>"
             "<p>BF<sub>3</sub> and NF<sub>3</sub> look alike on paper; the lone pair on N is the whole difference.</p>",
    source="Day 10 p.14–26, p.29–31; " + tb("5.3", 243, 246))

FLU_SIDS = ["CH4", "CH3F", "CH2F2", "CHF3", "CF4"]
assert [is_polar(s) for s in FLU_SIDS] == [False, True, True, True, False]
add(id="m22-p3", module="m22", kind="practice", level="Concept",
    prompt="<p>Replace the H atoms of methane with F atoms one at a time. Which of these molecules are polar?</p>",
    answer={"type": "match", "rows": pol_rows(FLU_SIDS), "options": POL_OPTS},
    hints=["All five are tetrahedral: SN 4, no lone pairs on C.",
           f"C–H is nonpolar by the lecture's cutoff (Δχ = {dchi('C', 'H')}, Day 9 p.18); C–F is polar (Δχ = {dchi('C', 'F')}). When are all four corners alike?"],
    solution="<p>CH<sub>4</sub> and CF<sub>4</sub> are <strong>nonpolar</strong>: four identical bonds at the corners of a tetrahedron cancel (CF<sub>4</sub> is the lecture's example, Day 10 p.30). "
             "CH<sub>3</sub>F, CH<sub>2</sub>F<sub>2</sub>, and CHF<sub>3</sub> are <strong>polar</strong>: with two kinds of corner, the C–F dipoles aren't balanced by equal dipoles pointing the other way. "
             "The textbook's rule of thumb says the same: with more than one kind of atom bonded to the central atom, a permanent dipole is “highly likely” (PDF p.246).</p>",
    source="Day 10 p.30; Day 9 p.18; " + tb("5.3", 246))

assert toward("C", ["Cl", "H", "H", "H"], "Cl") and toward("C", ["F", "F", "H", "H"], "F")
add(id="m22-p4", module="m22", kind="practice", level="Standard",
    prompt="<p>Which way does the net dipole point in (a) chloromethane, CH<sub>3</sub>Cl, and (b) difluoromethane, CH<sub>2</sub>F<sub>2</sub>? Both are tetrahedral. (χ: H 2.1, C 2.5, F 4.0, Cl 3.0; Day 9 p.17)</p>",
    answer={"type": "multi", "parts": [
        {"label": "(a) chloromethane", **choice(("toward the three H atoms", False, "The C–H dipoles are small and point from H toward C, the same general way as the C–Cl dipole."),
                                                ("toward the Cl atom", True, "Right: the polar C–Cl bond dominates."),
                                                ("no net dipole: the bond dipoles cancel", False, "Three C–H bonds can't balance one C–Cl bond: the four corners differ."))},
        {"label": "(b) difluoromethane", **choice(("toward the F atoms, along the line that bisects the F–C–F angle", True, "Right: the two C–F dipoles add along that line."),
                                                  ("toward the H atoms", False, "Each bond dipole points to its more electronegative atom: F, not H."),
                                                  ("no net dipole: the bond dipoles cancel", False, "Two C–F dipoles are canceled only by equal dipoles pointing the other way, and C–H dipoles are much smaller."))}]},
    hints=["Each bond dipole points to its more electronegative atom; C–H (Δχ 0.4) is essentially nonpolar.",
           "Add the arrows: in a tetrahedron the C–halogen dipoles lean toward the halogen side, and the small C–H dipoles (H → C) lean the same way."],
    solution="<p>(a) <strong>Toward Cl</strong>. (b) <strong>Toward the F atoms</strong>, along the bisector of the F–C–F angle. In both, the C–H dipoles are small and point from H toward C, the same general direction as the C–halogen dipoles, so nothing cancels. "
             "That's the CHCl<sub>3</sub> pattern of Day 11 p.7–8, where Table 5.2 puts the dipole “toward the three Cl atoms.”</p>"
             "<p class='bg'>Measured dipole moments: CH<sub>3</sub>Cl about 1.9 D, CH<sub>2</sub>F<sub>2</sub> about 2.0 D.</p>",
    source="Day 10 p.27–31; Day 11 p.7–8; Day 9 p.17–18")

assert not is_polar("PCl5")
add(id="m22-p5", module="m22", kind="practice", level="Concept",
    prompt=f"<p>PCl<sub>5</sub> has five polar P–Cl bonds (Δχ = {dchi('P', 'Cl')}), yet it's nonpolar. Why?</p>",
    answer=choice(("The axial dipoles cancel the equatorial ones.", False, "Axial and equatorial bonds are 90° apart, and perpendicular dipoles can't cancel each other. Each set cancels on its own."),
                  ("The lone pairs on the Cl atoms cancel the bond dipoles.", False, "The outer atoms' lone pairs don't undo the bond dipoles; the symmetric arrangement does."),
                  ("The three equatorial dipoles, 120° apart in a plane, cancel one another, and the two axial dipoles point in opposite directions and cancel each other.", True, "Right."),
                  ("P–Cl bonds are nonpolar.", False, f"Δχ = 3.0 − 2.1 = {dchi('P', 'Cl')} is polar covalent (Day 9 p.18).")),
    hints=["Split the trigonal bipyramid into its axial pair and its equatorial triangle (Day 10 p.12)."],
    solution="<p>In the trigonal bipyramid (SN 5, no lone pairs on P; Day 10 p.12) the two axial P–Cl dipoles point in opposite directions and cancel, and the three equatorial dipoles, 120° apart, cancel just as BF<sub>3</sub>'s do. "
             "Like CO<sub>2</sub> and CF<sub>4</sub>, the molecule is nonpolar although every bond is polar (Day 10 p.29–30).</p>",
    source="Day 10 p.12, p.29–30; Day 9 p.18")

TAB52 = {"HF": 1.82, "H2O": 1.85, "NH3": 1.47, "CHCl3": 1.01, "CCl3F": 0.45}       # Table 5.2 (Day 11 p.8; TB PDF p.245)
add(id="m22-p6", module="m22", kind="practice", level="Standard",
    prompt="<p>Use Table 5.2 (Day 11 p.8) and the course χ values (Day 9 p.17). (a) Which bond is more polar, H–F or O–H? (b) Which molecule has the larger dipole moment, HF or H<sub>2</sub>O? (c) How can both answers be true?</p>",
    answer={"type": "multi", "parts": [
        {"label": "(a) the more polar bond", **choice((f"H–F (Δχ {dchi('H', 'F')})", dchi("H", "F") > dchi("O", "H"), "Right: 4.0 − 2.1."),
                                                    (f"O–H (Δχ {dchi('O', 'H')})", dchi("O", "H") > dchi("H", "F"), "Check the values: 3.5 − 2.1 for O–H, 4.0 − 2.1 for H–F."))},
        {"label": "(b) the larger dipole moment", **choice((f"HF ({TAB52['HF']} D)", TAB52["HF"] > TAB52["H2O"], "Read Table 5.2 again."),
                                                         (f"H<sub>2</sub>O ({TAB52['H2O']} D)", TAB52["H2O"] > TAB52["HF"], "Right: by a little."))},
        {"label": "(c) why both are true", **choice(("Table 5.2 must be wrong, since H–F is the more polar bond.", False, "μ measures the whole molecule, not one bond. HF has one bond dipole; water has two that partly add."),
                                                  ("A dipole moment belongs to the whole molecule: water's two O–H dipoles add, because the molecule is bent, and its lone pairs contribute too.", True, "Right."),
                                                  ("O is more electronegative than F.", False, "F (4.0) is the most electronegative element; O is 3.5."),
                                                  ("Water's bond dipoles cancel, so its dipole moment comes from something else.", False, "Water's dipoles don't cancel; that's why it's polar (Day 10 p.31)."))}]},
    hints=["Δχ from the course table (Day 9 p.17).", "HF has one bond dipole. How many does water have, and do they point partly the same way?"],
    solution=f"<p>(a) <strong>H–F</strong> (Δχ {dchi('H', 'F')} vs. {dchi('O', 'H')}). (b) <strong>H<sub>2</sub>O</strong>, {TAB52['H2O']} D vs. {TAB52['HF']} D (Table 5.2, Day 11 p.8). "
             "(c) A dipole moment measures the whole molecule. Water's two O–H dipoles point partly the same way, toward O, and add (Day 10 p.31). "
             "The textbook's definition of a permanent dipole includes unequal distributions of lone pairs as well as bonding pairs (PDF p.244).</p>",
    source="Day 11 p.8; Day 10 p.31; Day 9 p.17; " + tb("5.3", 244, 245))

assert is_polar("SeF4") and not is_polar("SeF6")
add(id="m22-p7", module="m22", kind="practice", level="Stretch",
    prompt="<p>Selenium forms SeF<sub>4</sub> (seesaw, one lone pair on Se) and SeF<sub>6</sub> (octahedral, no lone pairs). Both have polar Se–F bonds. Which is polar?</p>",
    answer=choice(("SeF<sub>6</sub> only", False, "SeF<sub>6</sub> has six equal dipoles in three opposite pairs: they cancel, as in SF<sub>6</sub>."),
                  ("both", False, "SeF<sub>6</sub>'s arrangement is symmetric: opposite pairs cancel."),
                  ("neither", False, "In SeF<sub>4</sub> the two equatorial Se–F dipoles both point away from the lone pair and add."),
                  ("SeF<sub>4</sub> only", True, "Right: the lone pair makes the seesaw lopsided.")),
    hints=["Sketch each shape (Day 10 p.12, p.22).", "Opposite, equal dipoles cancel. In which molecule is every dipole paired with an opposite one?"],
    solution="<p><strong>SeF<sub>4</sub></strong>. In the ideal seesaw the two axial Se–F dipoles cancel each other, but the two equatorial ones both point away from the lone pair and add. "
             "SeF<sub>6</sub> is octahedral like the lecture's SF<sub>6</sub> (Day 10 p.12): its six dipoles form three opposite pairs and cancel.</p>",
    source="Day 10 p.12, p.22, p.29–30")

assert dchi("H", "F") > dchi("H", "Cl") > 0.4
add(id="m22-p8", module="m22", kind="practice", level="Concept",
    prompt=f"<p>HF's dipole moment is {TAB52['HF']} D (Table 5.2, Day 11 p.8). Is the dipole moment of HCl larger or smaller, and why? (χ: H 2.1, F 4.0, Cl 3.0; Day 9 p.17)</p>",
    answer=choice(("Larger: Cl is a bigger atom, so its charges are farther apart.", False,
                   f"The H–Cl bond is longer, which does spread the charges farther apart, but the charge shift itself is much smaller (Δχ {dchi('H', 'Cl')} vs. {dchi('H', 'F')}). Measured, HCl's dipole moment is smaller."),
                  ("The same: both are polar bonds between H and a halogen.", False, f"Both are polar, by different amounts: Δχ {dchi('H', 'F')} vs. {dchi('H', 'Cl')}."),
                  (f"Smaller: Cl is less electronegative than F, so the shared pair is pulled less far from H (Δχ {dchi('H', 'Cl')} vs. {dchi('H', 'F')}).", True, "Right."),
                  ("Zero: HCl is nonpolar.", False, f"Δχ = {dchi('H', 'Cl')} is polar covalent (Day 9 p.18), and H–Cl is the lecture's own example of a polar bond (Day 9 p.15).")),
    hints=["Each molecule has one bond, so its dipole is that bond's dipole. Compare Δχ."],
    solution=f"<p><strong>Smaller.</strong> In a one-bond molecule the molecular dipole is the bond dipole. Δχ is {dchi('H', 'F')} for H–F but only {dchi('H', 'Cl')} for H–Cl, so less electron density shifts toward Cl than toward F. "
             "The lecture's battery picture of H–Cl (Day 9 p.15) shows that it's polar, just less so than H–F.</p><p class='bg'>Measured: about 1.1 D for HCl.</p>",
    source="Day 11 p.8; Day 9 p.15–18")

MU_CM = TAB52["H2O"] * 3.34e-30
CM_UNITS = ["C·m", "C m", "C*m", "coulomb-meter", "coulomb meter", "coulomb-meters", "coulomb meters"]
P(id="m22-p9", module="m22", kind="practice", level="Textbook preview",
  prompt="<p>(a) Gaseous HF molecules point every which way until an electric field is switched on between two charged plates; then they line up (textbook Fig. 5.19). How do water molecules line up in the field? "
         "(b) Express water's dipole moment, 1.85 D, in coulomb-meters (1 D = 3.34 × 10<sup>−30</sup> C·m).</p>",
  answer={"type": "multi", "parts": [
      {"label": "(a) water in the field", **choice(("with the H end toward the positive plate", False, "The H end is δ+; it's attracted to the negative plate."),
                                                  ("with the O end toward the positive plate", True, "Right: the O end is δ− (Day 10 p.31)."),
                                                  ("randomly, whether the field is on or off", False, "Random only with the field off; polar molecules line up when it's on."),
                                                  ("not at all: water is neutral overall", False, "Neutral overall, but polar: its two ends carry opposite partial charges."))},
      {"label": "(b) dipole moment", **num_ans(MU_CM, sf=3, unit_label="C·m", units=CM_UNITS, ask_unit=True),
       "traps": [{"value": TAB52["H2O"] / 3.34e-30, "tol": 0.01, "message": "That divides. Multiply: D × (C·m per D)."}]}]},
  hints=["Opposite charges attract: which plate does water's δ− end face, and which end is that (Day 10 p.31)?", "1.85 D × (3.34 × 10<sup>−30</sup> C·m / 1 D)."],
  solution=f"<p>(a) <strong>O end toward the positive plate</strong>, H end toward the negative plate: water's net dipole points toward O (Day 10 p.31). “The more polar a molecule, the more strongly it aligns with an electric field” (PDF p.245), and that alignment is how μ is measured (PDF p.244). "
           f"(b) 1.85 D × 3.34 × 10<sup>−30</sup> C·m/D = <strong>{sci(MU_CM, 3)} C·m</strong> (3 significant figures).</p>",
  source=tb("5.3", 244, 245) + "; Day 10 p.31; Day 11 p.8")

V_SF5Cl = vsepr("SF5Cl")
assert is_polar("SF5Cl") and not is_polar("SF6")
add(id="m22-transfer", module="m22", kind="transfer", level="Transfer",
    prompt="<p>SF<sub>6</sub> is nonpolar. In SF<sub>5</sub>Cl one F is replaced by Cl, and S still has no lone pairs. (a) Name the molecular geometry. (b) Is SF<sub>5</sub>Cl polar? (χ: S 2.5, F 4.0, Cl 3.0)</p>",
    answer={"type": "multi", "parts": [
        {"label": "(a) molecular geometry", **name_choice(V_SF5Cl["mg"],
            ("square pyramidal", "Square pyramidal is SN 6 with a lone pair. Here the sixth position holds an atom, Cl."),
            ("trigonal bipyramidal", "That's SN 5; S has six neighbors."),
            ("octahedral", "Right: six atoms around S, no lone pairs, SN 6."),
            ("seesaw", "Seesaw is SN 5 with one lone pair."))},
        {"label": "(b) polar or nonpolar", **pol_choice("SF5Cl", "Right: the S–Cl dipole isn't matched by the S–F dipole opposite it.",
                                                          "In SF<sub>6</sub> every dipole is canceled by the one opposite it. Which bond is opposite S–Cl here, and is it the same?")}]},
    hints=["In SF<sub>6</sub>, each S–F dipole is canceled by the one opposite it (Day 10 p.12).",
           f"Which bond is opposite the S–Cl bond, and are their dipoles equal? Δχ: S–F {dchi('S', 'F')}, S–Cl {dchi('S', 'Cl')}."],
    solution=f"<p>(a) <strong>Octahedral</strong>. (b) <strong>Polar</strong>. The four S–F bonds around the middle form two opposite pairs and cancel. "
             f"But the S–Cl bond (Δχ {dchi('S', 'Cl')}) is opposite an S–F bond (Δχ {dchi('S', 'F')}): unequal dipoles pointing in opposite directions leave a net dipole along that axis. "
             "The textbook's rule of thumb: when more than one kind of atom is bonded to the central atom, a permanent dipole is “highly likely” (PDF p.246).</p>",
    source="Day 10 p.12, p.29–30; Day 9 p.17; " + tb("5.3", 246))

add(id="m22-m-explain", module="m22", kind="mastery", level="Explain",
    prompt="<p>Explain why CO<sub>2</sub> is nonpolar while H<sub>2</sub>O is polar, although both have polar bonds.</p>",
    answer={"type": "self", "model": "<p>Both have polar bonds: C–O Δχ = 1.0 and O–H Δχ = 1.4 (Day 10 p.29, p.31), each dipole pointing to O. The difference is shape. "
                                     "CO<sub>2</sub>'s C has two regions (SN 2), so the molecule is linear and its two equal dipoles point in exactly opposite directions: “perfectly opposed,” they cancel, and the molecule is nonpolar (Day 10 p.29). "
                                     "Water's O has two bonds and two lone pairs (SN 4), so the molecule is bent, 104.5°. Both O–H dipoles point partly toward O, “not perfectly opposed,” and they add to a net dipole toward O: "
                                     "the molecule is polar (Day 10 p.31), with a measured dipole moment of 1.85 D (Day 11 p.8).</p>"},
    hints=[], solution="", source="Day 10 p.19, p.29–31; Day 11 p.8")

add(id="m22-m-recognize", module="m22", kind="mastery", level="Recognize",
    prompt="<p>Which description guarantees that a molecule's bond dipoles cancel?</p>",
    answer=choice(("Every bond in the molecule is polar.", False, "Polar bonds make the question worth asking; they don't settle it (H<sub>2</sub>O)."),
                  ("The central atom has at least one lone pair.", False, "Lone pairs usually spoil the symmetry (NH<sub>3</sub>, H<sub>2</sub>O). XeF<sub>2</sub> and XeF<sub>4</sub> cancel anyway, but that's no guarantee."),
                  ("All the outer atoms are the same element, and the central atom has no lone pairs.", True,
                   "Right: then the bonds point to the corners of one of the five symmetric arrangements (Day 10 p.9–12) and cancel, as in CO<sub>2</sub>, CF<sub>4</sub>, PCl<sub>5</sub>, SF<sub>6</sub>."),
                  ("The central atom is the least electronegative atom.", False, "That sets which way each bond dipole points, not whether they cancel.")),
    hints=["What do CO<sub>2</sub>, BF<sub>3</sub>, CF<sub>4</sub>, PF<sub>5</sub>, and SF<sub>6</sub> have in common?"],
    solution="<p>Identical outer atoms around a central atom with <strong>no lone pairs</strong> sit at the corners of a linear, trigonal planar, tetrahedral, trigonal bipyramidal, or octahedral arrangement, and equal dipoles in those arrangements cancel. "
             "Two shapes with lone pairs also cancel, because their lone pairs sit symmetrically: linear XeF<sub>2</sub> and square planar XeF<sub>4</sub>. Anything else needs a closer look; mixed outer atoms almost always give a polar molecule (textbook PDF p.246).</p>",
    source="Day 10 p.9–12, p.29–31; " + tb("5.3", 246))

# naive Δχ sums for the two Table 5.2 tetrahedra (C at the origin; the unique atom on +z, the three others 109.47° from it):
# the three equal bonds add to one bond's worth along −z (3 × cos 109.47° = −1); C–H is taken as nonpolar, as in the textbook
NAIVE_CHCl3 = dchi("C", "Cl")
NAIVE_CCl3F = dchi("C", "F") - dchi("C", "Cl")
assert NAIVE_CCl3F > NAIVE_CHCl3 and TAB52["CCl3F"] < TAB52["CHCl3"]
add(id="m22-m-sanity", module="m22", kind="mastery", level="Sanity check",
    prompt=f"<p>A student adds Δχ-weighted bond arrows and predicts that CCl<sub>3</sub>F (C–F Δχ {dchi('C', 'F')}, opposite three C–Cl at {dchi('C', 'Cl')}) has a larger dipole moment than CHCl<sub>3</sub>. "
           f"Table 5.2 says {TAB52['CCl3F']} D for CCl<sub>3</sub>F and {TAB52['CHCl3']} D for CHCl<sub>3</sub> (Day 11 p.8). What should the student conclude?</p>",
    answer=choice(("Table 5.2 must have the two values switched.", False, "The textbook prints the same values (PDF p.245). Trust the measurement over a rough model."),
                  ("CCl<sub>3</sub>F is actually nonpolar.", False, f"{TAB52['CCl3F']} D isn't zero: the molecule is weakly polar, with its dipole toward F."),
                  ("Δχ arrows predict directions and whether dipoles cancel, not the sizes of molecular dipoles; in CCl<sub>3</sub>F the C–F and C–Cl dipoles point opposite ways and nearly cancel.", True, "Right."),
                  ("The C–H bond in CHCl<sub>3</sub> is the most polar bond in either molecule.", False, f"C–H is the least polar (Δχ = {dchi('C', 'H')}).")),
    hints=["Which way does the C–F dipole point relative to the three C–Cl dipoles?", "Does Δχ alone decide how big a bond dipole is?"],
    solution=f"<p>The Δχ model gets the <strong>directions</strong> right: CHCl<sub>3</sub>'s dipole points toward the Cl atoms and CCl<sub>3</sub>F's toward F, as Table 5.2 says. "
             f"Its sizes are only stand-ins: the arrow sums come out about {NAIVE_CHCl3:.1f} for CHCl<sub>3</sub> and {NAIVE_CCl3F:.1f} for CCl<sub>3</sub>F (in Δχ units), the wrong order. "
             "In CCl<sub>3</sub>F the C–F dipole points away from the three Cl atoms, against their combined dipole, so the two largely cancel; the measurement shows how much.</p>"
             "<p class='bg'>Real bond dipoles depend on bond length and on how the electrons are spread, not just on Δχ. C–F and C–Cl bonds turn out to have similar dipoles: "
             "CH<sub>3</sub>F (about 1.86 D) and CH<sub>3</sub>Cl (about 1.89 D) are almost equal, although their Δχ values are 1.5 and 0.5.</p>",
    source="Day 11 p.7–8; Day 9 p.17; " + tb("5.3", 245))

# ------------------------------------------------------------------ answer positions
# Correct options above were placed by hand; spread them the way the Ch. 4 banks are (choice_order.py), without
# writing the Ch. 4 remap record. Items whose options read in a natural order keep it.
choice_order.KEEP |= {("m20-transfer", ".2"), ("m21-p4", ".1"), ("m21-p9", ".0"), ("m21-p9", ".1")}
I_CHOICE_PERMS = choice_order.spread(PROBLEMS[I_START:], record=None)

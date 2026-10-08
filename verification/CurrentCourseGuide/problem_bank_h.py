"""Problem bank H: Day 9 lecture items for Ch. 4: §4.2 electronegativity, §4.5 resonance, §4.6 bond lengths,
§4.7 formal charge, §4.8 octet exceptions (Day 9 p.2-30).

The existing problems of those modules were relabeled in place (problem_bank_e.py for t4-2, problem_bank_g.py for
t4-5...t4-8; ids and answers unchanged). This bank adds new lecture problems (ids <module>-lec-..., t4-7-tophat),
spreads their correct choices over the option positions (choice_order.spread, as bank G does), and orders each
module's items lecture-first, then by level, so the new items sit among the old ones instead of after them.
Every key is computed from lewis.py structures, the course electronegativity table, or Table 4.6."""
from guide_common import *                                              # noqa: F401,F403
from problem_bank_a import PROBLEMS, add, num_ans, choice, KJMOL_UNITS  # noqa: F401
from problem_bank_b import text_ans, formula_ans, order_ans           # noqa: F401
from problem_bank_c import P, tb                                       # noqa: F401
from problem_bank_e import X, dchi                                     # noqa: F401
from problem_bank_f import LS, LX, tname, tformula, tnum, names        # noqa: F401
import problem_bank_g                                                  # noqa: F401  (Ch. 4 banks load first)
from problem_bank_g import BONDS, RES, BECOMES, fc_ans
import choice_order
import lewis as LW                                                     # noqa: F401

H_START = len(PROBLEMS)
S = LW.STRUCTS
CLS = {"nonpolar covalent": "np", "polar covalent": "pc", "ionic": "io"}
CLS_OPTS = [{"key": "np", "html": "nonpolar covalent"}, {"key": "pc", "html": "polar covalent"}, {"key": "io", "html": "ionic"}]
TOPHAT_UNASKED = ("Top Hat question prepared for class but not asked: “We didn't have time for this one, but it's a GREAT practice question” (Day 9 p.26). "
                  "The slide gives no answer; this key is ours.")


def bond_str(b):
    L, E = BONDS[b]
    return f"{b} {L} pm, {E} kJ/mol"


# =====================================================================================
# t4-2  Electronegativity and polar bonds (Day 9 p.15-18; Day 10 p.27)
# =====================================================================================
assert dchi("Br", "H") == 0.7 and ELECTRONEGATIVITY["Br"] > ELECTRONEGATIVITY["H"]
add(id="t4-2-lec-battery", module="t4-2", kind="practice", level="Warm-up",
    prompt="<p>Day 9 p.15 compares an H–Cl bond with a battery: the H end plays the part of the + terminal (δ+), the Cl end the part of the − terminal (δ−). "
           "Now take an H–Br bond (χ: H 2.1, Br 2.8; Day 9 p.17). Which description is right?</p>",
    answer=choice(("Br is the δ− end, like the battery's − terminal, and the crossed arrow points at Br.", True,
                   "Right: Br is more electronegative (2.8 vs. 2.1), so it has more of the electron density."),
                  ("H is the δ− end, because the crossed arrow's + tail sits at Br.", False,
                   "Backwards: the + tail marks the δ+ end, and the arrowhead points to the δ− end (Day 9 p.15)."),
                  ("Neither end: H–Br is nonpolar.", False, f"Δχ = 2.8 − 2.1 = {dchi('Br', 'H')}, above 0.4: polar covalent (Day 9 p.18)."),
                  ("Both ends are δ−, since both atoms are nonmetals.", False, "A polar bond has one δ+ end and one δ− end, like the battery's two terminals.")),
    hints=["The more electronegative atom is the one with “more of the electron density” (Day 9 p.15)."],
    solution=f"<p>Δχ = 2.8 − 2.1 = {dchi('Br', 'H')} → polar covalent, with <strong>Br the δ− end</strong>: H<sup>δ+</sup>–Br<sup>δ−</sup>. "
             "The crossed arrow has its + tail at H and its head at Br, just like the slide's H–Cl (Day 9 p.15; shown again on Day 10 p.27).</p>",
    source="Day 9 p.15, p.17–18; Day 10 p.27")

CUT = [("C", "H"), ("S", "Cl"), ("Ca", "Cl"), ("N", "Cl")]
assert [dchi(a, b) for a, b in CUT] == [0.4, 0.5, 2.0, 0.0]
add(id="t4-2-lec-cutoffs", module="t4-2", kind="practice", level="Concept",
    prompt="<p>The slide's cutoffs are Δχ ≤ 0.4 nonpolar covalent, 0.4 &lt; Δχ &lt; 2.0 polar covalent, and Δχ ≥ 2.0 ionic (Day 9 p.18). Classify each bond, watching the boundaries.</p>",
    answer={"type": "match", "rows": [{"html": f"{a}–{b}", "answer": CLS[bond_class(dchi(a, b))]} for a, b in CUT], "options": CLS_OPTS},
    hints=["χ from the course's table (Day 9 p.17): C 2.5, H 2.1, S 2.5, Cl 3.0, Ca 1.0, N 3.0.",
           "Exactly 0.4 is still nonpolar (≤); exactly 2.0 is already ionic (≥)."],
    solution="<p>" + "; ".join(f"{a}–{b}: Δχ = {dchi(a, b)} → <strong>{bond_class(dchi(a, b))}</strong>" for a, b in CUT) +
             ". The boundaries belong to the outer classes: 0.4 counts as nonpolar, 2.0 as ionic. N and Cl are different elements with the same χ, 3.0, so their bond is nonpolar.</p>"
             "<p class='note'>The textbook classifies the Cl–Ca bond the same way (Sample Ex. 4.2, PDF p.188) and warns that the cutoffs are “more like guidelines than strict limits” (PDF p.186).</p>",
    source="Day 9 p.17–18; " + tb("4.2", 186, 188))

assert dchi("Al", "Cl") == 1.5 and dchi("Be", "Cl") == 1.5
add(id="t4-2-lec-beal", module="t4-2", kind="practice", level="Stretch",
    prompt="<p>Day 9 p.27 draws BeCl<sub>2</sub> and AlCl<sub>3</sub> as molecules held together by shared pairs, although Be and Al are metals. "
           "(a) What is Δχ for an Al–Cl bond (Day 9 p.17)? (b) Classify the Al–Cl bond. (c) Does Δχ support drawing AlCl<sub>3</sub> with covalent bonds?</p>",
    answer={"type": "multi", "parts": [
        {"label": "(a) Δχ(Al–Cl)", **num_ans(dchi("Al", "Cl"), sf=2, tol=0.001),
         "traps": [{"value": 4.5, "tol": 0.001, "message": "That's the sum of the two values. Δχ is their difference."}]},
        {"label": "(b) bond type", **choice(("nonpolar covalent", False, "Δχ is well above 0.4."),
                                            ("polar covalent", True, "Right: 0.4 &lt; 1.5 &lt; 2.0."),
                                            ("ionic", False, "Ionic starts at Δχ ≥ 2.0 (Day 9 p.18)."))},
        {"label": "(c) covalent bonds?", **choice(("Yes: Δχ is below 2.0, so the electrons are shared, though unequally.", True, "Right."),
                                                 ("No: a metal and a nonmetal always form an ionic bond.", False,
                                                  "Day 7 p.14 describes covalent bonds as existing “between non-metals,” but Δχ is the finer test, and here it's below the ionic cutoff."))}]},
    hints=["χ(Al) = 1.5 and χ(Cl) = 3.0 (Day 9 p.17).", "Compare Δχ with the cutoffs 0.4 and 2.0 (Day 9 p.18)."],
    solution=f"<p>(a) Δχ = 3.0 − 1.5 = <strong>{dchi('Al', 'Cl')}</strong>. (b) <strong>Polar covalent</strong> (0.4 &lt; 1.5 &lt; 2.0). "
             "(c) <strong>Yes</strong>: on the slide's scale the Al–Cl pair is shared unequally, not transferred, so a Lewis structure with Al–Cl bonds fits. "
             f"Be–Cl is the same: χ(Be) = 1.5, so Δχ = {dchi('Be', 'Cl')} too. The Day 7 picture of covalent bonds “between non-metals” (Day 7 p.14) is a rough guide; Δχ is the course's measure of how a bond's electrons are shared.</p>",
    source="Day 9 p.17–18, p.27; Day 7 p.14")

add(id="t4-2-lec-explain", module="t4-2", kind="mastery", level="Explain",
    prompt="<p>Use the three potential maps on Day 9 p.16 (Cl<sub>2</sub>, HCl, NaCl) to explain how Δχ sorts bonds into nonpolar covalent, polar covalent, and ionic.</p>",
    answer={"type": "self", "model": "<p>The maps color charge on one scale, from dark blue (“1+”) through green-yellow (0) to dark red (“1−”). In Cl<sub>2</sub> two identical atoms (Δχ = 0) share the pair equally: "
                                     "“Nonpolar covalent: even charge distribution.” In HCl, Cl (χ 3.0) has more of the electron density than H (2.1): Δχ = 0.9, “Polar covalent: uneven charge distribution,” "
                                     "orange at the Cl end (δ−) and green-yellow at the H end. In NaCl, Δχ = 3.0 − 0.9 = 2.1: the electron is handed over, “Ionic: complete transfer of electron,” with Na<sup>+</sup> blue and Cl<sup>−</sup> red. "
                                     "The bigger Δχ, the more uneven the sharing, and the slide's cutoffs (Δχ ≤ 0.4, between 0.4 and 2.0, ≥ 2.0) mark three regions of one continuum (Day 9 p.16–18).</p>"},
    hints=[], solution="", source="Day 9 p.15–18")

# =====================================================================================
# t4-5  Resonance (Day 9 p.2, p.6-13; NO2 from p.28)
# =====================================================================================
O3a, O3b = S["O3a"], S["O3b"]
assert O3a.total_valence() == O3b.total_valence() == 18 and [b[:2] for b in O3a.bonds] == [b[:2] for b in O3b.bonds]
add(id="t4-5-lec-arrows", module="t4-5", kind="practice", level="Concept",
    prompt=f"<p>On Day 9 p.9 two red curved arrows turn the first ozone structure into the second:</p><p class='lw-row'>{LS('O3a', scale=0.7)}{BECOMES}{LS('O3b', scale=0.7)}</p><p>What do the arrows move?</p>",
    answer=choice(("Electron pairs: one pair of the double bond becomes a lone pair on the left O, and a lone pair on the right O becomes a new shared pair with the central O.", True,
                   "Right: same atoms in the same places; only electrons move (Day 9 p.8)."),
                  ("Atoms: the two end O atoms trade places.", False, "No atom moves. Structures in resonance are interconverted “by just moving electrons” (Day 9 p.8)."),
                  ("Single electrons: one electron jumps from each end O to the central O.", False, "Each arrow carries a pair, a bond's worth or a lone pair's worth of electrons, and the total stays 18."),
                  ("The molecule itself: ozone switches from one structure to the other.", False,
                   "The arrows show how one drawing becomes the other. The molecule “is NOT ‘changing’ back and forth between these two structures” (Day 9 p.9).")),
    hints=["Compare the two drawings: which lines and dots differ, and which atoms stay put?"],
    solution="<p>Each curved arrow moves an <strong>electron pair</strong>. One takes one of the two shared pairs between the left O and the center and puts it on the left O as a lone pair (that bond becomes single). "
             "The other takes a lone pair of the right O and makes it a second shared pair with the center (that bond becomes double). Nothing else changes: the atoms, the 18 electrons, and every octet stay the same, "
             "which is what “in resonance” requires (Day 9 p.8–9).</p>",
    source="Day 9 p.8–9")

HNC = LX("hydrogen isocyanide, HNC", [("H", 0, 0), ("N", 1, 0), ("C", 2.2, 0)], [(0, 1, 1), (1, 2, 3)], {2: 1}, neutral=True, scale=0.55)
_hnc = LW.Structure("x", "HNC", "", [("H", 0, 0), ("N", 1, 0), ("C", 2.2, 0)], [(0, 1, 1), (1, 2, 3)], {2: 1})
assert _hnc.drawn_electrons() == _hnc.total_valence() == S["HCN"].total_valence() == 10 and _hnc.shell(1) == _hnc.shell(2) == 8
for a_, b_ in (("NO2-rad1", "NO2-rad2"), ("N2O-A", "N2O-B"), ("CO3-1", "CO3-2")):                # same skeletons: only electrons differ
    assert [b[:2] for b in S[a_].bonds] == [b[:2] for b in S[b_].bonds] and S[a_].total_valence() == S[b_].total_valence()


def pair_html(a, b):
    return LS(a, neutral=True, scale=0.55) + RES + LS(b, neutral=True, scale=0.55)


add(id="t4-5-lec-notres", module="t4-5", kind="practice", level="Standard",
    prompt="<p>Structures are “in resonance” when they “can be interconverted by just moving electrons” (Day 9 p.8). Which pair is <em>not</em> in resonance?</p>",
    answer=choice((LS("HCN", neutral=True, scale=0.55) + " and " + HNC, True,
                   "Right: the H is bonded to C in one and to N in the other. Moving an atom makes a different molecule, not a resonance structure."),
                  (pair_html("NO2-rad1", "NO2-rad2"), False, "In resonance: the atoms stay put and only a bond pair and a lone pair move. The professor joins these two with ↔ (Day 9 p.28)."),
                  (pair_html("N2O-A", "N2O-B"), False,
                   "In resonance, even though they aren't equivalent: moving two electron pairs turns one into the other. The Day 9 p.24 table calls N<sub>2</sub>O's structures resonance structures."),
                  (pair_html("CO3-1", "CO3-2"), False, "In resonance: the double bond moves from one O to another by moving electrons only.")),
    hints=["For each pair, check the skeleton first: is every atom bonded to the same atoms in both drawings?"],
    solution="<p>The <strong>H–C≡N and H–N≡C</strong> pair. In every other pair the skeleton is identical and only electrons (lone pairs and multiple bonds) are placed differently. "
             "In the HCN pair the H is attached to a different atom, so the two drawings are different molecules, not resonance structures of one molecule (Day 9 p.8).</p>",
    source="Day 9 p.8, p.24, p.28")

R1, R2 = S["NO2-rad1"], S["NO2-rad2"]
end_dots = sorted({(2 * R1.lp.get(k, 0) + 2 * R2.lp.get(k, 0)) / 2 for k in (0, 2)})
assert end_dots == [5.0] and R1.rad == R2.rad == {1: 1} and R1.lp.get(1, 0) == R2.lp.get(1, 0) == 0
add(id="t4-5-lec-no2hybrid", module="t4-5", kind="practice", level="Standard",
    prompt=f"<p>Day 9 p.28 joins the two structures of nitrogen dioxide with ↔:</p><p class='lw-row'>{LS('NO2-rad1', scale=0.75)}{RES}{LS('NO2-rad2', scale=0.75)}</p>"
           "<p>Draw its resonance hybrid the way Day 9 p.10 draws ozone's. (a) How many dots go on each O? (b) How many dots go on N? (c) How is each N–O bond drawn?</p>",
    answer={"type": "multi", "parts": [
        {"label": "(a) dots on each O", **tnum(5, traps=[(4, "That's the O with the double bond in one structure. The hybrid averages each O's 4 and 6."),
                                                         (6, "That's the O with the single bond in one structure. The hybrid averages each O's 4 and 6.")])},
        {"label": "(b) dots on N", **tnum(1, traps=[(2, "N has one unpaired electron in both structures, not a pair.")])},
        {"label": "(c) each N–O bond", **choice(("one solid line plus one dashed line (a partial bond)", True, "Right: the slide's “dashed lines to indicate partial bonds” (Day 9 p.10)."),
                                               ("a double bond", False, "Neither bond is double in the real molecule; each is double in only one of the two structures."),
                                               ("a single bond", False, "That leaves out the pair that's shared between the two bonds."),
                                               ("one double bond and one single bond", False, "That's one resonance structure, and “neither structure alone is correct” (Day 9 p.9)."))}]},
    hints=["Each O has 2 lone pairs (4 dots) in the structure where its bond is double and 3 lone pairs (6 dots) where it's single.",
           "The hybrid shows the average, as ozone's end O atoms get 5 dots on Day 9 p.10. N's unpaired electron sits in the same place in both structures."],
    solution="<p>(a) <strong>5</strong> on each O, the average of 4 and 6. (b) <strong>1</strong> on N: its unpaired electron is the same in both structures. "
             "(c) Each N–O bond is a solid line plus a dashed line, a partial bond, the same convention as the ozone hybrid on Day 9 p.10. "
             "NO<sub>2</sub> is built like ozone with one electron fewer (17 instead of 18): where ozone's central O has a lone pair, NO<sub>2</sub>'s N has a single electron.</p>",
    source="Day 9 p.9–10, p.28")

add(id="t4-5-lec-benzene", module="t4-5", kind="practice", level="Concept",
    prompt="<p>Kekulé's benzene was a ring of alternating single and double bonds, “<em>nearly</em> correct” (Day 9 p.12). Which statement describes the real molecule, according to Day 9 p.2 and p.13?</p>",
    answer=choice(("All six C–C bonds are identical, between a single and a double bond: benzene is a resonance hybrid, drawn with dashed partial bonds or a circle in the ring.", True,
                   "Right: Lonsdale measured equal C–C bonds (Day 9 p.2), and benzene “doesn't behave as though it has double bonds” (Day 9 p.13)."),
                  ("Three short C=C bonds alternate with three long C–C bonds, as in one Kekulé structure.", False,
                   "That's one resonance structure. Measured, all six bonds are the same length (Day 9 p.2)."),
                  ("The ring flips rapidly between the two Kekulé structures.", False,
                   "Resonance structures aren't states the molecule switches between: it's “ALWAYS somewhere in between” (Day 9 p.9)."),
                  ("All six C–C bonds are double bonds.", False, "Each C also bonds to an H. With two C=C bonds, a C would have 10 electrons.")),
    hints=["What did Lonsdale's crystallography find about the C–C bond lengths (Day 9 p.2)?"],
    solution="<p>Benzene's two Kekulé structures (Day 9 p.13) are in resonance: one becomes the other by moving the three double bonds around the ring. Neither is the real molecule. "
             "The real molecule is the <strong>resonance hybrid</strong>, with six identical C–C bonds between single and double. Lonsdale's crystallography showed the equal bond lengths in 1929 (Day 9 p.2), "
             "and benzene's chemistry is “fundamentally different than any alkenes” (Day 9 p.13). The slide draws the hybrid two ways: dashed partial bonds, and a hexagon with a circle.</p>",
    source="Day 9 p.2, p.9, p.12–13")

add(id="t4-5-lec-rhino", module="t4-5", kind="practice", level="Concept",
    prompt="<p>Day 9 p.11 is a cartoon whose only words are its labels: rhinoceros = [dragon ↔ unicorn]. In the resonance analogy, what does the rhinoceros stand for?</p>",
    answer=choice(("The resonance hybrid: one real thing, described as a blend of two imaginary pictures.", True, "That's our reading of the cartoon; the slide gives labels but no explanation."),
                  ("One of the two resonance structures.", False, "The dragon and the unicorn, joined by ↔ inside the brackets, play the resonance structures: drawings that don't exist on their own."),
                  ("An animal that is a dragon one moment and a unicorn the next.", False,
                   "That's the misreading the professor warns against: the molecule “is NOT ‘changing’ back and forth” (Day 9 p.9)."),
                  ("The ↔ arrow.", False, "↔ joins the two drawings; the rhinoceros is on the other side of the = sign.")),
    hints=["Which side of the = sign is real, and which side is imaginary?"],
    solution="<p>Our reading (the slide labels the animals but explains nothing): the rhinoceros is the <strong>resonance hybrid</strong>, a real animal. The dragon and the unicorn are the resonance structures, imaginary drawings "
             "that you could blend to describe it. As with ozone, the real thing is never one drawing or the other: “neither structure alone is correct” (Day 9 p.9).</p>",
    source="Day 9 p.9, p.11")

# =====================================================================================
# t4-6  Bond lengths and strengths (Day 9 p.5, p.7, p.14: Table 4.6 with four red-boxed groups)
# =====================================================================================
for grp in (["C–C", "C=C", "C≡C"], ["C–O", "C=O", "C≡O"], ["O–O", "O=O"]):     # each red box: shorter and stronger with order
    assert all(BONDS[a][0] > BONDS[b][0] and BONDS[a][1] < BONDS[b][1] for a, b in zip(grp, grp[1:]))
add(id="t4-6-lec-boxes", module="t4-6", kind="practice", level="Warm-up",
    prompt="<p>Table 4.6 on Day 9 p.14 has red boxes around C–C/C=C/C≡C, C–O/C=O/C≡O, and O–O/O=O (and a fourth around the halogens). What pattern do the first three boxes show?</p>",
    answer=choice(("More shared pairs, shorter and stronger bonds.", True, f"Right: e.g., {bond_str('C–C')} → {bond_str('C=C')} → {bond_str('C≡C')}."),
                  ("More shared pairs, longer and stronger bonds.", False, "Read the length column: 154 → 134 → 120 pm. The bonds get shorter."),
                  ("A triple bond is exactly three times as strong as a single bond.", False, f"C≡C is {BONDS['C≡C'][1]} kJ/mol, less than 3 × {BONDS['C–C'][1]} = {3 * BONDS['C–C'][1]}."),
                  ("Bond order doesn't affect length; only the atoms do.", False, "Same two atoms, different bond orders, different lengths: that's the point of each box.")),
    hints=["Read down each box: the bond order rises from – to = to ≡."],
    solution="<p>In every box the bond order rises and the bonds get <strong>shorter and stronger</strong>: "
             + "; ".join(" → ".join(f"{b} {BONDS[b][0]} pm/{BONDS[b][1]} kJ/mol" for b in grp) for grp in (["C–C", "C=C", "C≡C"], ["C–O", "C=O", "C≡O"], ["O–O", "O=O"]))
             + ". That's outcome 7, “Describe how bond order, bond energy, and bond length are related,” bold on Day 9 p.5.</p>",
    source="Day 9 p.5, p.14")

HAL = ["F–F", "Cl–Cl", "Br–Br", "I–I"]
assert max(HAL, key=lambda b: BONDS[b][0]) == "I–I" and max(HAL, key=lambda b: BONDS[b][1]) == "Cl–Cl" and min(HAL, key=lambda b: BONDS[b][0]) == "F–F"
add(id="t4-6-lec-halogens", module="t4-6", kind="practice", level="Standard",
    prompt="<p>The fourth red box on Day 9 p.14 holds the halogens: F–F, Cl–Cl, Br–Br, I–I. (a) Which of the four bonds is the longest? (b) Which is the strongest? "
           "(c) Is the shortest one also the strongest, as in the carbon boxes?</p>",
    answer={"type": "multi", "parts": [
        {"label": "(a) longest", **choice(("F–F", False, f"{BONDS['F–F'][0]} pm: the shortest."), ("Cl–Cl", False, f"{BONDS['Cl–Cl'][0]} pm."),
                                          ("Br–Br", False, f"{BONDS['Br–Br'][0]} pm."), ("I–I", True, f"Right: {BONDS['I–I'][0]} pm."))},
        {"label": "(b) strongest", **choice(("F–F", False, f"Shortest, but only {BONDS['F–F'][1]} kJ/mol, less than Cl–Cl's {BONDS['Cl–Cl'][1]}."),
                                            ("Cl–Cl", True, f"Right: {BONDS['Cl–Cl'][1]} kJ/mol."),
                                            ("Br–Br", False, f"{BONDS['Br–Br'][1]} kJ/mol."), ("I–I", False, f"{BONDS['I–I'][1]} kJ/mol, the weakest."))},
        {"label": "(c) shortest = strongest?", **choice(("yes", False, "Compare F–F with Cl–Cl in the energy column."),
                                                        ("no", True, "Right: F–F is the shortest halogen bond but weaker than Cl–Cl."))}]},
    hints=["All four are single bonds, so bond order can't explain the differences; atom size can.",
           "Day 9 p.14: " + "; ".join(f"{b} {BONDS[b][0]} pm, {BONDS[b][1]} kJ/mol" for b in HAL) + "."],
    solution=f"<p>(a) <strong>I–I</strong> ({BONDS['I–I'][0]} pm). The lengths grow down the group, {' → '.join(str(BONDS[b][0]) for b in HAL)} pm, because the atoms get bigger (Day 7 p.7), so the bonded nuclei sit farther apart. "
             f"(b) <strong>Cl–Cl</strong>, {BONDS['Cl–Cl'][1]} kJ/mol. (c) <strong>No.</strong> Below chlorine, energy falls as the bonds get longer ({BONDS['Cl–Cl'][1]} → {BONDS['Br–Br'][1]} → {BONDS['I–I'][1]} kJ/mol), "
             f"but F–F breaks the pattern: it's the shortest halogen bond and yet weak, {BONDS['F–F'][1]} kJ/mol. In the carbon boxes, shorter always meant stronger because the bond order was changing; here every bond is single.</p>"
             "<p class='bg'>The usual explanation: F atoms are so small that the lone pairs on the two atoms crowd and repel each other, weakening the bond. The slides don't explain it.</p>",
    source="Day 9 p.14; Day 7 p.7")

add(id="t4-6-lec-co2", module="t4-6", kind="practice", level="Concept",
    prompt=f"<p>Table 4.6 gives {BONDS['C=O'][1]} kJ/mol for a C=O bond, but its footnote gives 799 kJ/mol for the carbon–oxygen bonds in CO<sub>2</sub> (Day 9 p.14). What does the difference tell you about the table?</p>",
    answer=choice(("Its values are averages over many compounds; the same kind of bond varies a little from one molecule to another.", True,
                   "Right: the table's title is “Average Lengths and Energies of Selected Covalent Bonds” (Day 9 p.14)."),
                  ("CO<sub>2</sub>'s carbon–oxygen bonds are triple bonds.", False, f"CO<sub>2</sub> is O=C=O (Day 10 p.7, p.10): double bonds. A C≡O bond is {BONDS['C≡O'][1]} kJ/mol."),
                  ("The table has an error.", False, "The footnote is deliberate: one molecule's bond can differ from the average."),
                  ("Bond energies can't be tabulated at all, because they depend on the molecule.", False, "The averages are useful estimates; they just aren't exact for every molecule.")),
    hints=["Read the table's title on Day 9 p.14."],
    solution=f"<p>Table 4.6 is titled “Average Lengths and Energies of Selected Covalent Bonds” (Day 9 p.14): each value is an <strong>average</strong> over many compounds. "
             f"A particular molecule's bond can be a bit stronger or weaker: the C=O bonds in CO<sub>2</sub> (799 kJ/mol) are stronger than the average C=O ({BONDS['C=O'][1]} kJ/mol). "
             "So values estimated from the table are approximate. The textbook makes the same point with formaldehyde, CH<sub>2</sub>O, whose C=O bond energy is 743 kJ/mol (PDF p.208).</p>",
    source="Day 9 p.14; Day 10 p.7, p.10; " + tb("4.6", 208))

assert BONDS["O=O"][1] > BONDS["O–O"][1]
add(id="t4-6-lec-oo-energy", module="t4-6", kind="practice", level="Standard",
    prompt="<p>Day 9 p.7 compares ozone's O–O bonds with those in H–O–O–H and O=O. Rank the O–O bonds of these three molecules by bond energy.</p>",
    answer=order_ans([("h2o2", "H<sub>2</sub>O<sub>2</sub> (H–O–O–H)"), ("o3", "O<sub>3</sub>"), ("o2", "O<sub>2</sub>")], ["o2", "o3", "h2o2"], "strongest (1) to weakest (3)"),
    hints=[f"Table 4.6 (Day 9 p.14): O–O {BONDS['O–O'][1]} kJ/mol, O=O {BONDS['O=O'][1]} kJ/mol.",
           "Ozone's bonds are “somewhere in between” single and double (Day 9 p.7), so expect an in-between energy."],
    solution=f"<p>O<sub>2</sub> (O=O, {BONDS['O=O'][1]} kJ/mol) &gt; O<sub>3</sub> &gt; H<sub>2</sub>O<sub>2</sub> (O–O, {BONDS['O–O'][1]} kJ/mol). "
             "Ozone's bonds are an average of single and double (Day 9 p.9), so their strength should fall between the single- and double-bond values, just as their length (128 pm) falls between 148 and 121 pm (Day 9 p.7).</p>"
             "<p class='note'>The slides give ozone's bond length, not its bond energy; the in-between strength is an inference from the pattern in the red boxes (Day 9 p.14).</p>",
    source="Day 9 p.7, p.9, p.14")

# =====================================================================================
# t4-7  Formal charge (Day 9 p.19-26; NO2 from p.28, sulfate from p.30)
# =====================================================================================
NA, NB, NC = S["N2O-A"], S["N2O-B"], S["N2O-C"]
assert NA.fcs() == [0, 1, -1] and NB.fcs() == [-1, 1, 0] and NC.fcs() == [-2, 1, 1]
assert all(s.total_valence() == 16 for s in (NA, NB, NC)) and ELECTRONEGATIVITY["O"] > ELECTRONEGATIVITY["N"]
add(id="t4-7-lec-n2o", module="t4-7", kind="practice", level="Standard",
    prompt="<p>Day 9 p.24 shows the three N<sub>2</sub>O structures from p.20 and asks: “Which is the <strong>worst</strong> structure? Which is the best?”</p>"
           f"<p class='lw-row'>{LS('N2O-A', scale=0.72, caption='A')}{LS('N2O-B', scale=0.72, caption='B')}{LS('N2O-C', scale=0.72, caption='C')}</p>"
           "<p>(a) What is the formal charge on the end N in structure C? (b) On the O in structure C? (c) Which structure is the worst? (d) Which is the best?</p>",
    answer={"type": "multi", "parts": [
        {"label": "(a) FC on the end N in C", **fc_ans(NC.fc(0), traps=[(-1, "Count again: 3 lone pairs (6 e⁻) + ½ × 2 bonding e⁻ = 7 assigned, and N has 5 valence electrons."),
                                                                        (0, "That end N has 3 lone pairs and only one bond: it's assigned more than its 5 valence electrons.")])},
        {"label": "(b) FC on the O in C", **fc_ans(NC.fc(2), traps=[(0, "O has one lone pair (2 e⁻) and a triple bond (½ × 6 = 3): 5 assigned, one fewer than its 6 valence electrons.")])},
        {"label": "(c) worst", **choice(("A", False, "A's formal charges are 0, +1, −1, with the −1 on O."), ("B", False, "B's are −1, +1, 0: no charge bigger than 1."),
                                        ("C", True, "Right: a −2, and a positive formal charge on O, the most electronegative atom."))},
        {"label": "(d) best", **choice(("A", True, "Right: A and B tie on rule 2, and rule 3 puts the −1 on O, the more electronegative atom."),
                                       ("B", False, "B ties A on rule 2, but its −1 is on N, which is less electronegative than O (rule 3)."),
                                       ("C", False, "C has the largest formal charges."))}]},
    hints=["Use the four steps “For each atom” (Day 9 p.22): FC = valence e⁻ − [lone-pair e⁻ + ½(bonding e⁻)].",
           "For B (N=N=O, two lone pairs on each end atom) the formal charges are end N −1, central N +1, O 0. For A they're 0, +1, −1.",
           "The rules (Day 9 p.23): all zero is best; otherwise most atoms at or near zero; negative formal charges on the more electronegative atom."],
    solution=f"<div class='lw-row'>{LS('N2O-A', show_fc=True, scale=0.8, caption='A')}{LS('N2O-B', show_fc=True, scale=0.8, caption='B')}{LS('N2O-C', show_fc=True, scale=0.8, caption='C')}</div>"
             "<p>(a) <strong>−2</strong>: the end N in C has 3 lone pairs (6 e⁻) and one single bond (½ × 2 = 1), so it's assigned 7, two more than its 5 valence electrons. "
             "(b) <strong>+1</strong>: the O has one lone pair (2) and a triple bond (½ × 6 = 3), 5 assigned against 6 valence. "
             "(c) <strong>C</strong> is the worst: a −2, and a positive charge on O. (d) <strong>A</strong> is the best: A (0, +1, −1) and B (−1, +1, 0) tie on rule 2, "
             "and rule 3 prefers A, whose −1 sits on O (χ 3.5) rather than N (3.0). Each set sums to 0 ✓ (rule 4).</p>"
             "<p>The professor's caution still holds: “the answer is ‘none of them’… But one of them is better than the other two, and <strong>closer</strong> to the real structure” (Day 9 p.21). "
             "The textbook's filled-in version of this table agrees (PDF p.210).</p>",
    source="Day 9 p.19–24; " + tb("4.7", 209, 210))

T1, T2, T3 = S["H3PO4-t1"], S["H3PO4-t2"], S["H3PO4-t3"]
TH_ATOMS = [("P", 1.3, 1.3), ("O", 1.3, 0.05), ("O", 0.05, 1.3), ("O", 2.55, 1.3), ("O", 1.3, 2.55), ("H", -0.95, 1.3), ("H", 1.3, 3.55)]
TH4 = (TH_ATOMS + [("H", 2.2, 2.2)], [(0, 1, 1), (0, 2, 1), (0, 3, 1), (0, 4, 1), (2, 5, 1), (4, 6, 1), (0, 7, 1)], {1: 3, 2: 2, 3: 3, 4: 2})
TH5 = ([("P", 1.3, 1.3), ("O", 1.3, 0.05), ("O", 0.05, 1.3), ("H", 2.45, 1.3), ("O", 3.6, 1.3), ("O", 1.3, 2.55), ("H", -0.95, 1.3), ("H", 1.3, 3.55)],
       [(0, 1, 2), (0, 2, 1), (0, 3, 1), (3, 4, 1), (0, 5, 1), (2, 6, 1), (5, 7, 1)], {1: 2, 2: 2, 4: 3, 5: 2})
_t4, _t5 = (LW.Structure("x", "H3PO4 option", "", *t) for t in (TH4, TH5))
assert T1.total_valence() == 32 and all(s.drawn_electrons() == 32 for s in (T1, T2, T3))
assert _t4.drawn_electrons() == _t5.drawn_electrons() == 34 and _t5.shell(3) == 4                # options 4 and 5 draw 34 electrons; 5 gives an H four
assert T3.fcs() == [0] * 8 and T3.shell(0) == 10 and T2.fc(0) == 1 and T2.shell(0) == 8 and sorted(T1.fcs()) == [-1, 0, 0, 0, 0, 0, 0, 1]
TH_OPTS = [LS("H3PO4-t1", neutral=True, scale=0.5, caption="1"), LS("H3PO4-t2", neutral=True, scale=0.5, caption="2"), LS("H3PO4-t3", neutral=True, scale=0.5, caption="3"),
           LX("structure 4", *TH4, neutral=True, scale=0.5, caption="4"), LX("structure 5", *TH5, neutral=True, scale=0.5, caption="5")]
add(id="t4-7-tophat", module="t4-7", kind="practice", level="In-class Top Hat", signal=TOPHAT_UNASKED,
    prompt="<p>“Choose the <strong>best</strong> Lewis structure for phosphoric acid” (Day 9 p.26). The five options are the slide's, numbered as on the slide.</p>",
    answer=choice((TH_OPTS[0], False, "32 electrons, but formal charges −1 on the top O and +1 on the O that has both a double bond and an H. Option 3 does better."),
                  (TH_OPTS[1], False, "32 electrons and every atom has an octet, but P is +1 and the top O −1. Rule 1 prefers a structure with every formal charge 0, and P (row 3) may expand its octet (Day 9 p.29)."),
                  (TH_OPTS[2], True, "Right: 32 electrons and every formal charge 0 (rule 1). P has 10 electrons, an expanded octet, which row-3 P may have (Day 9 p.29)."),
                  (TH_OPTS[3], False, "Count the electrons: this drawing uses 34, but H<sub>3</sub>PO<sub>4</sub> has 32."),
                  (TH_OPTS[4], False, "Count the electrons: 34, not 32. It also gives one H two bonds (4 electrons), though “H forms duets” (Day 9 p.27).")),
    hints=["Step 1 first: H<sub>3</sub>PO<sub>4</sub> has 3 × 1 + 5 + 4 × 6 = 32 valence electrons. Count each option.",
           "Then compute formal charges (Day 9 p.22) for the options that pass, and apply the rules (Day 9 p.23)."],
    solution="<p>Our key: option <strong>3</strong>. Check the count first: H<sub>3</sub>PO<sub>4</sub> has 3 + 5 + 24 = 32 valence electrons. Options 4 and 5 draw 34, so they're out "
             "(and 5 gives an H four electrons, though “H forms duets,” Day 9 p.27). Among 1–3, the formal charges decide (Day 9 p.22–23):</p>"
             f"<div class='lw-row'>{LS('H3PO4-t1', show_fc=True, scale=0.55, caption='1')}{LS('H3PO4-t2', show_fc=True, scale=0.55, caption='2')}{LS('H3PO4-t3', show_fc=True, scale=0.55, caption='3')}</div>"
             "<p>Option 1 has −1 on the top O and +1 on the bottom O; option 2 has +1 on P and −1 on the top O; option 3 has every formal charge 0, which rule 1 calls the best. "
             "Its P has 10 electrons, allowed because “Atoms of nonmetals in the third row and below can have expanded octets,” and “An expanded shell produces a structure whose atoms' formal charges are closer to zero” (Day 9 p.29). "
             "Sulfate on Day 9 p.30 is the same move. (The Top Hat slide comes before the expanded-octet slides and gives no answer; rule 1 on p.23 alone already picks option 3.)</p>",
    source="Day 9 p.22–23, p.26–27, p.29–30")

SOo = S["SO4-oct"]
assert all(SOo.fc(k) == -1 for k in (1, 2, 3, 4)) and SOo.fc(0) == 2 and 2 * SOo.lp[1] + SOo.bond_orders(1) == 7
add(id="t4-7-lec-meaning", module="t4-7", kind="practice", level="Warm-up",
    prompt=f"<p>On Day 9 p.30 each O of the all-single-bond sulfate structure is labeled −1:</p><p>{LS('SO4-oct', show_fc=True, scale=0.7)}</p><p>By the definition on Day 9 p.22, what does that −1 mean?</p>",
    answer=choice(("In this structure the O is assigned 7 electrons (6 in its lone pairs + half of the 2 it shares), one more than a free O atom's 6 valence electrons.", True, "Right: FC = 6 − (6 + 1) = −1."),
                  ("The O has gained a whole electron from S, making a real O<sup>−</sup> ion.", False,
                   "Formal charge is a comparison, not a measured charge: it splits each bond evenly, and the S–O bonds are polar covalent, not ionic."),
                  ("The O has 7 lone-pair electrons.", False, "It has 6 lone-pair electrons (3 pairs); the seventh assigned electron is its half of the bond."),
                  ("The O has one electron fewer than a free O atom.", False, "That would be +1. Assigned more than the valence count → negative.")),
    hints=["Formal charge is “a comparison of how many electrons the atoms have in the compound to how many they had as free atoms” (Day 9 p.22)."],
    solution=f"<p>Each single-bonded O is assigned its 6 lone-pair electrons plus half of the shared pair: 7, one more than O's 6 valence electrons, so FC = 6 − 7 = <strong>−1</strong> (Day 9 p.22). "
             f"It's bookkeeping: the real S–O bonds are polar covalent (Δχ = {dchi('S', 'O')}, Day 9 p.17–18), so no O carries a full extra electron.</p>",
    source="Day 9 p.17–18, p.22, p.30")

NO2r = S["NO2-rad1"]
assert NO2r.fcs() == [0, 1, -1] and NO2r.rad == {1: 1}
add(id="t4-7-lec-no2", module="t4-7", kind="practice", level="Stretch",
    prompt=f"<p>On Day 9 p.28 the N of nitrogen dioxide carries a red “+1”:</p><p>{LS('NO2-rad1')}</p><p>Check it with the four steps. N has one unpaired electron, a double bond, and a single bond. What is its formal charge?</p>",
    answer=fc_ans(NO2r.fc(1), traps=[(2, "The unpaired electron counts: step 2 counts every electron on the atom that isn't in a bond, even a single one."),
                                     (-2, "Count half of the bonding electrons, not all six.")]),
    hints=["Step 2 counts every electron not in a bond, including a single unpaired one: 1.", "Step 3: the double and single bonds hold 4 + 2 = 6 electrons; half is 3. FC = 5 − (1 + 3)."],
    solution=f"<p>5 − (1 + ½ × 6) = 5 − 4 = <strong>+1</strong>, matching the slide's red label. The double-bonded O is 6 − (4 + 2) = {NO2r.fc(0)} and the single-bonded O is 6 − (6 + 1) = −1, "
             "so the sum is 0 for the neutral molecule ✓ (rule 4, Day 9 p.23).</p>",
    source="Day 9 p.22–23, p.28")

# =====================================================================================
# t4-8  Exceptions to the octet rule (Day 9 p.27-30)
# =====================================================================================
V = LW.VALENCE
EXC = [("BeF<sub>2</sub>", V["Be"] + 2 * V["F"], "def", "Be has 4"), ("AlBr<sub>3</sub>", V["Al"] + 3 * V["Br"], "def", "Al has 6"),
       ("NO", V["N"] + V["O"], "rad", "odd"), ("OH (the neutral molecule, not the OH<sup>−</sup> ion)", V["O"] + V["H"], "rad", "odd"),
       ("SF<sub>4</sub>", S["SF4"].total_valence(), "exp", f"S has {S['SF4'].shell(0)}"), ("PCl<sub>5</sub>", S["PCl5"].total_valence(), "exp", f"P has {S['PCl5'].shell(0)}")]
assert [t % 2 for _, t, k, _ in EXC] == [0, 0, 1, 1, 0, 0] and S["SF4"].shell(0) == S["PCl5"].shell(0) == 10
add(id="t4-8-lec-classify", module="t4-8", kind="practice", level="Standard",
    prompt="<p>Match each species with the octet exception it shows (Day 9 p.27–29).</p>",
    answer={"type": "match", "rows": [{"html": h, "answer": k} for h, _, k, _ in EXC],
            "options": [{"key": "def", "html": "electron-deficient (fewer than 8 on the central atom)"}, {"key": "rad", "html": "odd number of electrons (free radical)"},
                        {"key": "exp", "html": "expanded octet (more than 8)"}]},
    hints=["Count valence electrons first: an odd total forces an unpaired electron (Day 9 p.28).",
           "Be, B, and Al form electron-deficient molecules (Day 9 p.27); a nonmetal in row 3 or below bonded to F, O, or Cl can expand its octet (Day 9 p.29)."],
    solution="<p>" + "; ".join(f"{h.split(' (')[0]}: {t} valence electrons, " + ("odd → <strong>free radical</strong>" if k == "rad" else
                                ("<strong>electron-deficient</strong> (" + n + ")" if k == "def" else "<strong>expanded octet</strong> (" + n + ")")) for h, t, k, n in EXC) +
             ". The OH<sup>−</sup> ion, with 8 electrons, is not a radical: the extra electron completes the pairs.</p>",
    source="Day 9 p.27–30")

SOe = S["SO4-exp"]
assert SOo.fc(0) == 2 and SOe.fc(0) == 0 and sum(SOo.fcs()) == sum(SOe.fcs()) == -2 and SOe.shell(0) == 12 and SOo.shell(0) == 8
add(id="t4-8-lec-so4", module="t4-8", kind="practice", level="Concept",
    prompt=f"<p>On Day 9 p.30 the professor redraws sulfate with two curved arrows:</p><p class='lw-row'>{LS('SO4-oct', show_fc=True, scale=0.62)}{BECOMES}{LS('SO4-exp', show_fc=True, scale=0.62)}</p>"
           "<p>Why make the two S=O bonds, when the first structure already gives every atom an octet?</p>",
    answer=choice(("To bring the formal charges closer to zero: S goes from +2 to 0. S is a row-3 nonmetal bonded to O, so it may expand its octet.", True,
                   "Right: “An expanded shell produces a structure whose atoms' formal charges are closer to zero” (Day 9 p.29)."),
                  ("To give S an octet.", False, "S already had an octet in the first structure; in the second it has 12."),
                  ("To change the ion's charge from 2− to 0.", False, "The charge stays 2−: the formal charges sum to −2 in both structures (rule 4, Day 9 p.23)."),
                  ("Because S must always have 12 electrons.", False, "An expanded octet is allowed, not required; the slide expands it because that lowers the formal charges.")),
    hints=["Compare the formal charges in the two structures, using rules 1–2 (Day 9 p.23)."],
    solution="<p>Every atom has an octet on the left, but the formal charges are far from zero: S +2 and each O −1. Turning two O lone pairs into S=O bonds gives S 0, two O at 0, and two O at −1 "
             "(the sum is still −2), with 12 electrons on S. The professor's rule: atoms in the third row and below “will expand their octet when they bond with strongly electronegative elements (F, O, and Cl). "
             "An expanded shell produces a structure whose atoms' formal charges are <strong>closer to zero</strong>” (Day 9 p.29). Why expansion is possible isn't taught: hypervalency “is not well understood.”</p>",
    source="Day 9 p.23, p.29–30")

CH3 = S["CH3-rad"]
assert CH3.total_valence() == 7 and CH3.shell(0) == 7
add(id="t4-8-lec-ch3", module="t4-8", kind="practice", level="Standard",
    prompt="<p>The methyl radical, CH<sub>3</sub>, is a short-lived fragment in which C is bonded to three H atoms. (a) How many valence electrons does it have? "
           "(b) How many electrons surround C? (c) Which kind of octet exception is it?</p>",
    answer={"type": "multi", "parts": [
        {"label": "(a) valence electrons", **tnum(CH3.total_valence(), traps=[(8, "C has 4 and each H 1: 4 + 3 = 7.")])},
        {"label": "(b) electrons around C", **tnum(CH3.shell(0), traps=[(8, "Three bonds give 6, plus the one unpaired electron: 7. There's no eighth electron."),
                                                                        (6, "Don't forget the leftover electron: it stays on C, unpaired.")])},
        {"label": "(c) exception", **choice(("odd number of electrons: a free radical", True, "Right: an odd count forces one electron to be unpaired (Day 9 p.28)."),
                                            ("electron-deficient, like BCl<sub>3</sub>", False, "C is short of 8, but because the count is odd: one electron has no partner. The slide's electron-deficient atoms are Be, B, and Al (Day 9 p.27)."),
                                            ("expanded octet", False, "C is in row 2: never more than 8."))}]},
    hints=["4 + 3 × 1.", "Three C–H bonds use 6 electrons; the last one has nothing to pair with."],
    solution=f"<p>{LS('CH3-rad')}</p><p>(a) <strong>7</strong>. (b) <strong>7</strong>: three bonds (6) plus one unpaired electron. (c) A <strong>free radical</strong>: "
             "“Some species have an odd number of electrons, which forces some of them to be unpaired. These species are called ‘radicals’ or ‘free radicals,’ and they are very reactive” (Day 9 p.28).</p>"
             "<p class='connection'>Free radicals return on the Day 11 Representation Matters slide: Rebecca Gerschman's finding that “free radicals cause cell death and aging” (Day 11 p.3).</p>",
    source="Day 9 p.27–28; Day 11 p.3")

add(id="t4-8-lec-hyper", module="t4-8", kind="practice", level="Concept",
    prompt="<p>The professor calls expanded octets “hypervalency” and says it “is not well understood” (Day 9 p.29). Which statement can you make from the slides?</p>",
    answer=choice(("Nonmetals in the third row and below can be drawn with more than 8 electrons, especially when bonded to F, O, or Cl, and doing so can bring formal charges closer to zero.", True,
                   "Right: that's what Day 9 p.29 states. It doesn't say how the extra electrons are accommodated."),
                  ("Any atom can exceed an octet if it's bonded to fluorine.", False, "Only nonmetals in the third row and below (Day 9 p.29). C, N, O, and F never exceed 8."),
                  ("S in SF<sub>6</sub> holds the extra electrons in its 3d orbitals.", False, "The slides give no mechanism, and the textbook says studies show that d orbitals contribute little (PDF p.214)."),
                  ("Expanded octets are a drawing error to avoid.", False, "The slides draw them as valid structures: PCl<sub>5</sub>, SF<sub>6</sub>, and SO<sub>4</sub><sup>2−</sup> (Day 9 p.29–30).")),
    hints=["What does Day 9 p.29 state, and what does it leave unexplained?"],
    solution="<p>The slide gives a rule and a reason to use it, not a mechanism: row-3-and-below nonmetals “can have expanded octets,” they expand “when they bond with strongly electronegative elements (F, O, and Cl),” "
             "and “An expanded shell produces a structure whose atoms' formal charges are closer to zero” (Day 9 p.29). How the atom holds the extra electrons “is not well understood.” "
             "The textbook agrees that d orbitals “contribute little” (PDF p.214), and its §5.7 offers a model with no expanded octet (textbook preview, PDF p.271–273).</p>",
    source="Day 9 p.29–30; " + tb("4.8", 214) + "; " + tb("5.7", 271, 273))

# =====================================================================================
# audit fixes (2026-10-06) to earlier problems of these modules, edited in place; ids and keys unchanged
# =====================================================================================
_BY_ID = {p["id"]: p for p in PROBLEMS}


def _sub(pid, field, old, new):
    """replace one exact substring of a problem's text field; fails loudly if the original text has changed."""
    p = _BY_ID[pid]
    assert p[field].count(old) == 1, (pid, field, old)
    p[field] = p[field].replace(old, new)


def _part_label(pid, k, old, new):
    part = _BY_ID[pid]["answer"]["parts"][k]
    assert part["label"] == old, (pid, k, part["label"])
    part["label"] = new


# The slides say "an average of the two" (Day 9 p.9) but give no number; the lecture-labeled items ask for the
# average number of shared pairs (single = 1, double = 2, Day 8 p.19-20) and name the textbook's term for it.
_sub("t4-5-attempt", "prompt", "What is the average N–O bond order? Enter a decimal.",
     "On average, how many shared pairs does each N–O bond have? (The textbook calls this number the bond order, PDF p.206.) Enter a decimal.")
_part_label("t4-5-attempt", 1, "(b) average N–O bond order", "(b) average shared pairs per N–O bond")
_BY_ID["t4-5-attempt"]["hints"][0] = ("Resonance structures keep one skeleton and differ only in where electrons sit (Day 9 p.8). Nitrite is built like ozone. "
                                      "Step 1: N 5 + 2 × O 6 + 1 for the 1− charge = 18 electrons, the same count as ozone (Day 8 p.28).")
_BY_ID["t4-5-attempt"]["hints"][3] = "Each N–O bond is double (2 shared pairs) in one structure and single (1 pair) in the other: average = (2 + 1)/2."
_sub("t4-5-attempt", "solution", "(b) <strong>1.5</strong>. As", "(b) <strong>1.5</strong> shared pairs per bond. As")
_sub("t4-5-transfer", "prompt", "(b) What is the average C–O bond order? Enter a decimal.",
     "(b) On average, how many shared pairs does each C–O bond have (the textbook's bond order)? Enter a decimal.")
_part_label("t4-5-transfer", 1, "(b) C–O bond order", "(b) shared pairs per C–O bond")
_sub("t4-6-attempt", "prompt", "has C bonded to three O atoms, and the H is bonded to one of those O atoms. ",
     "has C bonded to three O atoms, and the H is bonded to one of those O atoms. Count a bond's order as its number of shared pairs "
     "(outcome 7 uses the term, Day 9 p.5; the textbook defines it, PDF p.206). ")
# hint ladders: concept -> relationship -> setup -> near-complete setup, leaving the last step to the student
_BY_ID["t4-6-attempt"]["hints"] = [
    "Resonance averages only the bonds that trade places between equivalent structures (Day 9 p.8–9); a bond that is the same in every structure keeps its own order.",
    "More shared pairs, shorter bond: the pattern in Table 4.6's red boxes (Day 9 p.14).",
    "Draw it: 1 + 4 + 18 + 1 = 24 valence electrons, with C central and the H on one O. Which O atoms could take the C=O double bond?",
    "The O–H oxygen keeps a single bond to C in every structure. The C=O can sit on either of the other two O atoms, so those two bonds share 3 pairs between them."]
_BY_ID["t4-8-attempt"]["hints"] = [
    "An atom can share only the valence electrons it has: each bond it forms uses one of its own (bonding capacity, Day 8 p.18). Follow the five steps (Day 8 p.21) and see where the electrons run out.",
    "B has 3 valence electrons and each F has 7. Each B–F bond holds 2 electrons, and each F needs 3 lone pairs to reach 8.",
    "After three B–F bonds and the F lone pairs, is anything left for B? If an F lone pair became a B=F bond (the step-5 move), what formal charges would B and that F get (Day 9 p.22)?",
    "A B=F bond makes that F +1 and B −1: a positive charge on the most electronegative element, the reverse of rule 3 (Day 9 p.23). Keep the structure in which every formal charge is 0, and count B's electrons."]
# the rule "leave the incomplete octet on the less electronegative atom" is the textbook's (PDF p.213; the t4-8 preview box)
_BY_ID["t4-8-p5"]["label"] = "preview"
# quote the textbook exactly (its em dash is not reproduced)
_sub("t4-5-m-sanity", "solution",
     "The textbook: “The true structure is an average of those three: a molecular ion with three equivalent bonds rather than a double bond and two single bonds” (PDF p.205).",
     "The textbook says the true structure “is an average of those three”: “a molecular ion with three equivalent bonds rather than a double bond and two single bonds” (PDF p.205).")

# =====================================================================================
# answer positions and order within each module
# =====================================================================================
NEW = PROBLEMS[H_START:]
# keep the slide's order for the Top Hat options and natural orders (A/B/C, the halogen group, nonpolar/polar/ionic, yes/no)
NO_SPREAD = {"t4-7-tophat", "t4-7-lec-n2o", "t4-6-lec-halogens", "t4-2-lec-beal"}
choice_order.spread([p for p in NEW if p["id"] not in NO_SPREAD], record=None)

KIND_RANK = {"attempt": 0, "practice": 1, "transfer": 2, "mastery": 3}
LEVEL_RANK = {"Warm-up": 0, "Concept": 1, "Standard": 2, "In-class Top Hat": 2.5, "Stretch": 3, "Textbook preview": 4,
              "Explain": 0, "Recognize": 1, "Sanity check": 2}
DAY9_MODULES = ["t4-2", "t4-5", "t4-6", "t4-7", "t4-8"]


def order_module(mid):
    """Lecture items first, then textbook preview; within each, by level (stable). Positions in PROBLEMS are reused,
    so other modules' problems don't move."""
    idx = [i for i, p in enumerate(PROBLEMS) if p["module"] == mid]
    items = sorted((PROBLEMS[i] for i in idx),
                   key=lambda p: (KIND_RANK[p["kind"]], p.get("label", "lecture") != "lecture", LEVEL_RANK.get(p["level"], 2)))
    for i, p in zip(idx, items):
        PROBLEMS[i] = p


for _m in DAY9_MODULES:
    order_module(_m)

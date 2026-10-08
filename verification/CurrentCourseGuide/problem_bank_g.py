"""Problem bank G: the rest of Ch. 4 (textbook §4.5–4.9, with the Day 8 ozone and allotrope slides):
t4-5 resonance, t4-6 bond lengths and strengths, t4-7 formal charge, t4-8 exceptions to the octet rule,
t4-9 vibrating bonds and the greenhouse effect; mixed review x36-x47.
Day 9 taught §4.5–4.8: on 2026-10-06 those modules' problems were relabeled lecture where the idea they test is on
the slides (ids and answers unchanged); new Day 9 problems are in problem_bank_h.py. t4-9 stays a textbook preview.
Every Lewis structure comes from lewis.py (checked there against electron counts, octets, formal charges,
and RDKit). Table 4.6 values were read off the rendered page (TB PDF p.207, printed 173)."""
from guide_common import *
from problem_bank_a import PROBLEMS, add, num_ans, choice, KJMOL_UNITS
from problem_bank_b import text_ans, formula_ans, order_ans
from problem_bank_c import P, tb
from problem_bank_e import X
from problem_bank_f import LS, LX, tname, tformula, tnum, names, CH4_START
import choice_order
import lewis as LW

PM_UNITS = ["pm", "picometer", "picometers", "picometre", "picometres"]
KJ_UNITS = ["kj", "kilojoule", "kilojoules"]

# Table 4.6 (TB PDF p.207): bond -> (length pm, energy kJ/mol). The C=O energy is 743; its footnote gives 799 for CO2.
BONDS = {
    "C–C": (154, 348), "C=C": (134, 614), "C≡C": (120, 839), "C–N": (147, 293), "C=N": (127, 615), "C≡N": (116, 891),
    "C–O": (143, 358), "C=O": (123, 743), "C≡O": (113, 1072), "C–H": (110, 413), "C–F": (133, 485), "C–Cl": (177, 328),
    "N–H": (104, 391), "N–N": (147, 163), "N=N": (124, 418), "N≡N": (110, 945), "N–O": (136, 201), "N=O": (122, 607),
    "N≡O": (106, 678), "O–O": (148, 146), "O=O": (121, 498), "O–H": (96, 463), "S–O": (151, 265), "S=O": (143, 523),
    "S–S": (204, 266), "S–H": (134, 347), "H–H": (74, 436), "H–F": (92, 567), "H–Cl": (127, 431), "H–Br": (141, 366),
    "H–I": (161, 299), "F–F": (143, 155), "Cl–Cl": (200, 243), "Br–Br": (228, 193), "I–I": (266, 151),
}
assert len(BONDS) == 35

RES = "<span class='lw-arrow' role='img' aria-label='resonance arrow'>↔</span>"
BECOMES = "<span class='lw-arrow' role='img' aria-label='becomes'>→</span>"

FC_SIGN = ("The size is right, but the sign is wrong. FC = valence electrons − (lone-pair electrons + ½ shared electrons): "
           "if the atom is assigned more electrons than it has valence electrons, the formal charge is negative.")


def fc_ans(value, traps=None):
    a = tnum(value, traps=traps)
    a["signMessage"] = FC_SIGN
    return a


def bond_order(s, a, b):
    """average bond order between atom types a and b over one resonance set, from lewis.py structures."""
    return sum(o for i, j, o in s.bonds if {s.atoms[i][0], s.atoms[j][0]} == {a, b}) / \
        sum(1 for i, j, o in s.bonds if {s.atoms[i][0], s.atoms[j][0]} == {a, b})


# =====================================================================================
# t4-5  Resonance (lecture: Day 8 p.26-30 ozone, allotropes; Day 9 p.6-13; textbook §4.5, PDF p.202-206)
# Relabeled 2026-10-06 (Day 9 teaches resonance); m-recognize, the textbook's resonance test, stays preview.
# =====================================================================================
BO_NO2m = bond_order(LW.STRUCTS["NO2-1"], "N", "O")
assert abs(BO_NO2m - 1.5) < 1e-9
add(id="t4-5-attempt", module="t4-5", kind="attempt", level="Guided attempt",
    prompt="<p>The nitrite ion, NO<sub>2</sub><sup>−</sup> (on the polyatomic-ion table, Day 8 p.8), has N bonded to both O atoms. "
           "(a) How many equivalent Lewis structures can you draw for it? (b) The real ion is an average of its structures, as ozone is (Day 9 p.9). What is the average N–O bond order? Enter a decimal.</p>",
    answer={"type": "multi", "parts": [
        {"label": "(a) equivalent structures", **tnum(2, traps=[(1, "Look again at step 5: the lone pair that becomes the second N–O bond can come from either O."),
                                                             (3, "There are only two O atoms to supply the double bond, and N can't take a second double bond without going past 8 electrons.")])},
        {"label": "(b) average N–O bond order", **num_ans(BO_NO2m, tol=0.01),
         "traps": [{"value": 2, "tol": 0, "message": "That's the double bond in one structure. Average over both structures."},
                   {"value": 1, "tol": 0, "message": "That's the single bond in one structure. Average over both structures."}]}]},
    hints=["Step 1: N 5 + 2 × O 6 + 1 for the 1− charge = 18 electrons, the same count as ozone (Day 8 p.28).",
           "Steps 2–4: O–N–O with single bonds, three lone pairs on each O, and the last pair on N. N then has only 6 electrons.",
           "Step 5, as for ozone (Day 8 p.29–30): turn one O lone pair into a second N–O bond. It can be either O, and the two results interconvert “by just moving electrons” (Day 9 p.8).",
           "Each N–O bond is double in one structure and single in the other: average bond order = (2 + 1)/2."],
    solution="<div class='lw-row'>" + LS("NO2-1", scale=0.85) + RES + LS("NO2-2", scale=0.85) + "</div>"
             "<p>(a) <strong>2</strong> equivalent structures, “in resonance” (Day 9 p.8). (b) <strong>1.5</strong>. As the professor says of ozone, “neither structure alone is correct”: "
             "the real ion is “an average of the two” (Day 9 p.9), with two identical N–O bonds between single and double. The textbook calls this number the bond order (§4.6, PDF p.206).</p>",
    compare={"wrong": "<p>“One N=O and one N–O: two different bonds, with bond orders 2 and 1.”</p>",
             "tempting": "That's exactly what any single Lewis structure shows, and the five steps stop after one structure.",
             "fails": "The double bond could just as well be on the other O, and nothing chemical distinguishes the two O atoms. For ozone, the same situation gives two identical 128 pm bonds, between O–O (148 pm) and O=O (121 pm) (Day 9 p.7). "
                      "The real ion is the average: both N–O bonds have order 1.5."},
    source="Day 9 p.7–10; Day 8 p.8, p.28–30; " + tb("4.5", 203, 205) + "; " + tb("4.6", 206))

add(id="t4-5-p1", module="t4-5", kind="practice", level="Warm-up",
    prompt="<p>O<sub>2</sub> and O<sub>3</sub> are both pure oxygen. What does the lecture call different molecular forms of the same element?</p>",
    answer=choice(("allotropes", True, "Right: “Allotropes: different molecular forms of the same element. O<sub>2</sub> vs O<sub>3</sub>” (Day 8 p.27)."),
                  ("isotopes", False, "Isotopes are atoms of one element with different numbers of neutrons (Day 2). O<sub>2</sub> and O<sub>3</sub> differ in how many atoms are bonded together."),
                  ("resonance structures", False, "Resonance structures are drawings of one molecule. O<sub>2</sub> and O<sub>3</sub> are different molecules."),
                  ("ions", False, "Both are neutral molecules.")),
    hints=["Day 8 p.27 has the definition, next to the lightning photo."],
    solution="<p><strong>Allotropes</strong> (Day 8 p.27). Lightning splits O<sub>2</sub> into O atoms, which join other O<sub>2</sub> molecules to form O<sub>3</sub> (the slide's particle inset; textbook Fig. 4.9).</p>",
    source="Day 8 p.27")

O3_OPTS = LS("O3a", scale=0.7) + " and " + LS("O3b", scale=0.7)
add(id="t4-5-p2", module="t4-5", kind="practice", level="Concept",
    prompt=f"<p>The professor finishes ozone with two structures (Day 8 p.30):</p><p>{O3_OPTS}</p><p>How do they differ?</p>",
    answer=choice(("Only in which end O has the double bond (and so which end O has three lone pairs).", True, "Right: the atoms are connected the same way; only the electrons are arranged differently."),
                  ("In the order the atoms are connected.", False, "Both are O–O–O with the same central O."),
                  ("One uses 18 valence electrons and the other 16.", False, "Count them: both use all 18."),
                  ("One obeys the octet rule and the other doesn't.", False, "Every O has 8 electrons in both.")),
    hints=["Compare the skeletons first, then the bonds and lone pairs."],
    solution="<p>Same atoms, same connections, same 18 electrons, octets everywhere: they differ <strong>only in where the double bond (and the lone pairs) sit</strong>. "
             "This is the “more than one perfectly valid Lewis structure” case the professor flags on Day 8 p.26. Day 9 names it: the structures are “equivalent,” which “does not mean they are the same,” "
             "and because one becomes the other “by only moving electrons,” they are “in resonance” (Day 9 p.8).</p>",
    source="Day 8 p.26–30; Day 9 p.8; " + tb("4.5", 203))

add(id="t4-5-p3", module="t4-5", kind="practice", level="Standard",
    prompt="<p>The acetate ion, CH<sub>3</sub>COO<sup>−</sup> (on the polyatomic-ion table, Day 8 p.8), has a CH<sub>3</sub> group and two O atoms bonded to the same C. How many equivalent resonance structures does it have?</p>",
    answer=tnum(2, traps=[(1, "One structure puts the double bond on one O. Could it be on the other?"), (3, "Only the two O atoms can take the double bond; the CH<sub>3</sub> carbon already has four bonds.")]),
    hints=["24 valence electrons: 2 × 4 + 3 × 1 + 2 × 6 + 1.",
           "The carboxylate C needs one C=O to complete its octet. How many O atoms could supply it? Moving that pair to the other O is “just moving electrons” (Day 9 p.8)."],
    solution="<div class='lw-row'>" + LS("CH3COO-1", scale=0.7) + RES + LS("CH3COO-2", scale=0.7) + "</div>"
             "<p><strong>2</strong>: the double bond can be to either O, so the two structures are in resonance, and the real ion is their average: two identical C–O bonds, each between single and double (Day 9 p.8–10). "
             "In the textbook's terms each C–O bond has bond order 1.5, and its quick test for resonance fits this ion (PDF p.205–206).</p>",
    source="Day 9 p.8–10; Day 8 p.8; " + tb("4.5", 203, 205))

add(id="t4-5-p4", module="t4-5", kind="practice", level="Concept",
    prompt="<p>Both O–O bonds in ozone are 128 pm long. Why?</p>",
    answer=choice(("The real molecule is an average of the two resonance structures, with the electrons of the extra bond delocalized over both bonds.", True, "Right (Day 9 p.7, p.9–10)."),
                  ("The molecule flips back and forth between the two structures, so we measure an average.", False,
                   "Tempting, but the slide says the molecule “is NOT ‘changing’ back and forth between these two structures” (Day 9 p.9). There's one real structure, in between the drawings."),
                  ("One bond is double and one is single, and the lengths happen to match.", False, "A typical O=O bond is 121 pm and a typical O–O bond 148 pm (Day 9 p.7): they can't match."),
                  ("Ozone has two double bonds.", False, "Then the central O would have 10 electrons.")),
    hints=["128 pm is between O=O (121 pm) and O–O (148 pm) (Day 9 p.7)."],
    solution="<p>“Which of these structures is correct? Interestingly, the answer turns out to be ‘neither’” (Day 9 p.7). The molecule is “ALWAYS somewhere in between. An average of the two” (Day 9 p.9): "
             "two identical bonds, intermediate between single and double. The electrons that move between the drawings are “delocalized” (Day 9 p.10).</p>"
             "<p class='note'>The textbook says the same with a number, bond order 1.5, and calls the extra stability “resonance stabilization” (PDF p.204, p.206). The slide leaves the reason “beyond the scope of this class” (Day 9 p.10).</p>",
    source="Day 9 p.7–10; " + tb("4.5", 203, 204))

add(id="t4-5-p5", module="t4-5", kind="practice", level="Standard",
    prompt="<p>Which species has equivalent resonance structures?</p>",
    answer=choice(("CO<sub>3</sub><sup>2−</sup>", True, "Right: C has one double and two single bonds to O atoms, and the double bond can be at any of the three."),
                  ("CH<sub>4</sub>", False, "Only single C–H bonds; there's no alternative arrangement."),
                  ("NH<sub>3</sub>", False, "Three single bonds and a lone pair; nothing to rearrange."),
                  ("H<sub>2</sub>O", False, "Two single bonds; no multiple bond to move.")),
    hints=["Look for a double bond that could be moved to a different, identical neighbor “by just moving electrons” (Day 9 p.8).",
           "The textbook's test: an atom with both single and double bonds to atoms of the same element (PDF p.205)."],
    solution="<p><strong>CO<sub>3</sub><sup>2−</sup></strong>. Its central C has a C=O and two C–O bonds, and the double bond can be drawn to any of the three O atoms; "
             "the three drawings interconvert by moving electrons only (Day 9 p.8), like ozone's two.</p>",
    source="Day 9 p.8–9; " + tb("4.5", 205) + "; " + tb("4.6", 207, 208))

add(id="t4-5-p6", module="t4-5", kind="practice", level="Warm-up",
    prompt="<p>What does the double-headed arrow ↔ between two Lewis structures mean?</p>",
    answer=choice(("The structures are resonance forms, and the real bonding is an average of them.", True, "Right (Day 9 p.9–10)."),
                  ("A reaction that runs in both directions.", False, "That's the equilibrium arrow ⇌, a different symbol."),
                  ("The atoms move from one position to another.", False, "Resonance forms have the same atom positions; only electrons are drawn differently (Day 9 p.8)."),
                  ("Electrons are transferred to make ions.", False, "No ions form; it's one molecule drawn two ways.")),
    hints=["↔ is not ⇌. On Day 9 p.9 the professor draws ↔ between the two ozone structures."],
    solution="<p>On Day 9 p.9 the two ozone structures are joined by ↔, with the reminder that “neither structure alone is correct” and the molecule is “an average of the two.” "
             "Keep ↔ distinct from ⇌ (equilibrium). The plain → on the same slide links a structure drawn with curved arrows to the structure they produce: a drawing step, not a reaction. "
             "The textbook: “A double-headed arrow is used between resonance forms to symbolize the averaging effect of bonding-pair delocalization” (PDF p.204).</p>",
    source="Day 9 p.9–10; " + tb("4.5", 204))

BO_HCO2 = bond_order(LW.STRUCTS["HCO2-1"], "C", "O")
add(id="t4-5-transfer", module="t4-5", kind="transfer", level="Transfer",
    prompt="<p>In the formate ion, HCO<sub>2</sub><sup>−</sup>, C is bonded to H and to both O atoms. (a) How many equivalent resonance structures does it have? (b) What is the average C–O bond order? Enter a decimal.</p>",
    answer={"type": "multi", "parts": [{"label": "(a) structures", **tnum(2)}, {"label": "(b) C–O bond order", **num_ans(BO_HCO2, tol=0.01)}]},
    hints=["H 1 + C 4 + 2 × 6 + 1 = 18 electrons.",
           "With H–C and two C–O single bonds and octets on both O, C has only 6 electrons: one O must share a second pair. Either O can, and the two structures interconvert by just moving electrons (Day 9 p.8)."],
    solution="<div class='lw-row'>" + LS("HCO2-1", scale=0.8) + RES + LS("HCO2-2", scale=0.8) + "</div>"
             "<p>(a) <strong>2</strong>. (b) <strong>1.5</strong>: the same pattern as ozone and nitrite, with 18 electrons and one double bond shared between two equivalent positions. "
             "The real ion is the average (Day 9 p.9).</p>",
    source="Day 9 p.8–10; " + tb("4.5", 203, 205) + "; " + tb("4.6", 206))

add(id="t4-5-m-explain", module="t4-5", kind="mastery", level="Explain",
    prompt="<p>Explain, using ozone, what the professor means by “delocalized” electrons (Day 9 p.10), and why a single Lewis structure can't describe O<sub>3</sub>.</p>",
    answer={"type": "self", "model": "<p>Any one Lewis structure of O<sub>3</sub> puts a double bond on one side and a single bond on the other (Day 8 p.30). But both measured O–O bonds are 128 pm, between a typical O–O (148 pm) and O=O (121 pm) (Day 9 p.7). "
                                     "The two structures are “in resonance”: one becomes the other “by just moving electrons” (Day 9 p.8). “Neither structure alone is correct”; the molecule isn't flipping between them but is “ALWAYS somewhere in between. An average of the two” (Day 9 p.9). "
                                     "The electrons that move between the drawings belong to both bonds at once: they're “delocalized,” shown in the resonance hybrid as dashed partial bonds (Day 9 p.10). "
                                     "Molecules with delocalized electrons are “more stable,” for reasons “beyond the scope of this class” (Day 9 p.10).</p>"},
    hints=[], solution="", source="Day 9 p.7–10; Day 8 p.30; " + tb("4.5", 203, 204))

P(id="t4-5-m-recognize", module="t4-5", kind="mastery", level="Recognize",
  prompt="<p>Which clue tells you to look for equivalent resonance structures?</p>",
  answer=choice(("An atom has single and double bonds to two or more atoms of the same element.", True, "Right: the textbook's test (PDF p.205)."),
                ("The molecule contains any double bond.", False, "CH<sub>2</sub>O has a C=O but only one position for it."),
                ("The electron count is odd.", False, "That signals a free radical (§4.8)."),
                ("The central atom has a lone pair.", False, "NH<sub>3</sub> has one, and no resonance.")),
  hints=["Compare O<sub>3</sub> and NO<sub>3</sub><sup>−</sup> with CH<sub>2</sub>O."],
  solution="<p>Same-element neighbors with a mix of single and double bonds (O<sub>3</sub>, NO<sub>3</sub><sup>−</sup>, CO<sub>3</sub><sup>2−</sup>, benzene's ring). "
           "The test is the textbook's; the lecture's ozone and benzene both fit it (Day 9 p.6–13).</p>",
  source=tb("4.5", 205) + "; Day 9 p.6–13")

add(id="t4-5-m-sanity", module="t4-5", kind="mastery", level="Sanity check",
    prompt="<p>A student says the nitrate ion has one short N=O bond and two longer N–O bonds. What's wrong with that?</p>",
    answer=choice(("All three N–O bonds are identical: the real ion is an average of three resonance structures.", True, "Right: as for ozone, “neither structure alone is correct” (Day 9 p.9)."),
                  ("Nothing; that's what the Lewis structure shows.", False, "One drawing shows that, but no single resonance structure is the real ion (Day 9 p.9)."),
                  ("Nitrate has three double bonds.", False, "Then N would have 12 electrons."),
                  ("Nitrate has no double bonds.", False, "Then N would have only 6 electrons.")),
    hints=["How many equivalent structures does nitrate have? The real ion is their average (Day 9 p.9)."],
    solution="<p>Nitrate has three equivalent structures, and the real ion is their average, so all three N–O bonds are identical. "
             "The textbook: “The true structure is an average of those three: a molecular ion with three equivalent bonds rather than a double bond and two single bonds” (PDF p.205).</p>",
    source="Day 9 p.9–10; " + tb("4.5", 205))

# =====================================================================================
# t4-6  Bond lengths and strengths (lecture: Day 9 p.5, p.7, p.14 (Table 4.6); textbook §4.6, PDF p.206-208)
# Relabeled 2026-10-06; p2 and p3 rest on the textbook's definition of bond energy and stay preview.
# =====================================================================================
BO_NO3 = bond_order(LW.STRUCTS["NO3-1"], "N", "O")
assert abs(BO_NO3 - 4 / 3) < 1e-9
add(id="t4-6-attempt", module="t4-6", kind="attempt", level="Guided attempt",
    prompt="<p>The hydrogen carbonate ion, HCO<sub>3</sub><sup>−</sup>, has C bonded to three O atoms, and the H is bonded to one of those O atoms. "
           "(a) What is the bond order of the C–O bond to the O that carries the H? (b) What is the average bond order of the other two C–O bonds? Enter a decimal. "
           "(c) Which C–O bond is the longest?</p>",
    answer={"type": "multi", "parts": [
        {"label": "(a) C–O(H) bond order", **tnum(1),
         "traps": [{"value": 4 / 3, "tol": 0.01, "message": "Resonance averages only equivalent bonds. The O with the H isn't equivalent to the other two."},
                   {"value": 1.5, "tol": 0.001, "message": "1.5 belongs to the two equivalent C–O bonds. The bond to the O–H oxygen is single in both structures."}]},
        {"label": "(b) average of the other two", **num_ans(1.5, tol=0.01),
         "traps": [{"value": 4 / 3, "tol": 0.01, "message": "4/3 is carbonate's value, with 4 shared pairs over 3 equivalent bonds. Here the extra pair is shared by only 2 bonds."},
                   {"value": 2, "tol": 0, "message": "That's the double bond in one structure. Average over the two equivalent bonds."}]},
        {"label": "(c) longest C–O bond", **choice(("the bond to the O that carries the H", True, "Right: bond order 1 → the longest (C–O 143 pm)."),
                                                 ("one of the other two", False, "Those have bond order 1.5: shorter."),
                                                 ("all three are the same length", False, "That's carbonate, whose three bonds are equivalent."))}]},
    hints=["Draw it: 1 + 4 + 18 + 1 = 24 valence electrons, with C central and H on one O.",
           "The O–H oxygen already has two bonds (to C and to H) and two lone pairs: its C–O bond stays single.",
           "The C needs one C=O bond to complete its octet. It can go to either O that has no H: two equivalent structures, in resonance (Day 9 p.8).",
           "Those two bonds share 3 pairs between them: an average of 3/2. A lower bond order means a longer bond (the red boxes in Table 4.6, Day 9 p.14)."],
    solution="<div class='lw-row'>" + LS("HCO3-1", scale=0.8) + RES + LS("HCO3-2", scale=0.8) + "</div>"
             "<p>(a) <strong>1</strong>. (b) <strong>1.5</strong>. (c) The <strong>C–O(H)</strong> bond, the only one that's single in both structures. "
             "Bond order predicts length: the C–O(H) bond should be near the single-bond average (143 pm), the other two between 143 and 123 pm (Table 4.6, Day 9 p.14).</p>"
             "<p class='bg'>Measured structures of hydrogen carbonate salts show exactly this pattern: one longer C–O bond and two shorter, equal ones.</p>",
    compare={"wrong": "<p>“All three C–O bonds have bond order 4/3, like carbonate.”</p>",
             "tempting": "Hydrogen carbonate looks like carbonate with an H added, and carbonate's three C–O bonds are equivalent.",
             "fails": "The H makes one O different: that O's bond to C is single in both equivalent structures. Resonance averages only the bonds that trade places, here 3 shared pairs over 2 bonds (1.5), not 4 over 3."},
    source="Day 9 p.8–10, p.14; Day 8 p.8–9 (hydrogen carbonate on the ion table); " + tb("4.6", 206, 208) + "; " + tb("4.5", 205))

add(id="t4-6-p1", module="t4-6", kind="practice", level="Warm-up",
    prompt="<p>Rank these carbon–carbon bonds by length.</p>",
    answer=order_ans([("cc1", "C–C"), ("cc2", "C=C"), ("cc3", "C≡C")], ["cc1", "cc2", "cc3"], "longest (1) to shortest (3)"),
    hints=["Look at the first red box in Table 4.6 (Day 9 p.14): as the bond order rises, the length falls."],
    solution="<p>C–C 154 pm &gt; C=C 134 pm &gt; C≡C 120 pm (Table 4.6, Day 9 p.14). More shared pairs pull the nuclei closer together.</p>",
    source="Day 9 p.14; " + tb("4.6", 206, 207))

P(id="t4-6-p2", module="t4-6", kind="practice", level="Concept",
  prompt="<p>Table 4.6 lists the H–H bond energy as 436 kJ/mol. What does that number mean?</p>",
  answer=choice(("436 kJ must be added to break 1 mol of H–H bonds in the gas phase (and the same amount is released when they form).", True, "Right (textbook PDF p.208)."),
                ("436 kJ is released when 1 mol of H–H bonds breaks.", False, "Breaking bonds always takes energy in; bond energies are positive."),
                ("436 kJ is the energy of a single H–H bond.", False, "It's per mole of bonds: one bond is 436 kJ ÷ 6.022 × 10<sup>23</sup>."),
                ("436 kJ/mol is H<sub>2</sub>'s ionization energy.", False, "Ionization removes an electron; bond energy separates the atoms.")),
  hints=["It's the depth of the energy well on Day 8 p.11."],
  solution="<p>Bond energy is “the energy needed to break one mole of bonds in the gas phase”; it's always positive because breaking bonds requires adding energy (textbook PDF p.208). "
           "For H–H it's the depth of the minimum on the lecture's energy curve, −436 kJ/mol at 74 pm (Day 8 p.11), which Table 4.6 lists as a positive 436 kJ/mol (Day 9 p.14). The slides don't define the term.</p>",
  source=tb("4.6", 208) + "; Day 8 p.11; Day 9 p.14")

E_CH4 = 4 * BONDS["C–H"][1]
P(id="t4-6-p3", module="t4-6", kind="practice", level="Standard",
  prompt="<p>Using Table 4.6's average C–H bond energy (413 kJ/mol; Day 9 p.14), estimate the energy needed to break all the C–H bonds in 1 mol of CH<sub>4</sub>.</p>",
  answer={**num_ans(E_CH4, tol=0.01, unit_label="kJ", units=KJ_UNITS + KJMOL_UNITS, ask_unit=True),
          "traps": [{"value": 413, "tol": 0.001, "message": "That's 1 mol of C–H bonds. Each CH<sub>4</sub> molecule has four."}]},
  hints=["How many C–H bonds does one CH<sub>4</sub> have?", "1 mol CH<sub>4</sub> × 4 mol C–H bonds/mol CH<sub>4</sub> × 413 kJ/mol C–H."],
  solution=f"<p>1 mol CH<sub>4</sub> × (4 mol C–H / 1 mol CH<sub>4</sub>) × (413 kJ / 1 mol C–H) = <strong>{E_CH4} kJ</strong> (about 1.65 × 10<sup>3</sup> kJ; the 4 is an exact count). "
           "Table 4.6 values are averages over many compounds, so this is an estimate (PDF p.208).</p>",
  source=tb("4.6", 207, 208) + "; Day 9 p.14")

add(id="t4-6-p4", module="t4-6", kind="practice", level="Standard",
    prompt="<p>Which has the shorter and stronger carbon–oxygen bond: carbon monoxide, CO, or carbon dioxide, CO<sub>2</sub>?</p>",
    answer=choice(("CO, with a C≡O triple bond", True, "Right: bond order 3 vs. 2 (C≡O 113 pm, 1072 kJ/mol)."),
                  ("CO<sub>2</sub>, because it has two C=O bonds", False, "Having more bonds doesn't make each bond shorter. Compare the order of each carbon–oxygen bond."),
                  ("They're the same", False, "CO's bond is triple; CO<sub>2</sub>'s are double."),
                  ("Can't tell without a measurement", False, "Bond order predicts the trend.")),
    hints=["Draw both with the five steps (Day 8 p.21): :C≡O: and O=C=O. Then compare bond orders in the C–O box of Table 4.6 (Day 9 p.14)."],
    solution="<p><strong>CO</strong>: bond order 3 → shorter (113 pm) and stronger (1072 kJ/mol) than a C=O bond (Table 4.6 average 123 pm; 799 kJ/mol in CO<sub>2</sub>, per the table's footnote; Day 9 p.14).</p>",
    source="Day 9 p.14; Day 8 p.21; " + tb("4.6", 206, 208))

add(id="t4-6-p5", module="t4-6", kind="practice", level="Concept",
    prompt="<p>Rank the O–O bonds in these molecules by length.</p>",
    answer=order_ans([("h2o2", "H<sub>2</sub>O<sub>2</sub> (H–O–O–H)"), ("o3", "O<sub>3</sub>"), ("o2", "O<sub>2</sub>")], ["h2o2", "o3", "o2"], "longest (1) to shortest (3)"),
    hints=["Bond orders: H<sub>2</sub>O<sub>2</sub> 1; O<sub>3</sub> an average of 1 and 2 (resonance, Day 9 p.9); O<sub>2</sub> 2.", "Higher bond order → shorter bond."],
    solution="<p>H<sub>2</sub>O<sub>2</sub> 148 pm &gt; O<sub>3</sub> 128 pm &gt; O<sub>2</sub> 121 pm: the comparison on Day 9 p.7, which draws H–O–O–H and O=O beside ozone. "
             "Ozone's resonance-averaged bonds land between the other two.</p>",
    source="Day 9 p.7, p.9, p.14; " + tb("4.6", 206))

E_NITRITE = (BONDS["N–O"][1] + BONDS["N=O"][1]) / 2
add(id="t4-6-transfer", module="t4-6", kind="transfer", level="Transfer",
    prompt="<p>Nitrite, NO<sub>2</sub><sup>−</sup>, has two equivalent resonance structures, so each N–O bond is an average of a single and a double bond (bond order 1.5). "
           "Estimate the energy of one mole of these N–O bonds from Table 4.6 (N–O 201 kJ/mol, N=O 607 kJ/mol; Day 9 p.14).</p>",
    answer={**num_ans(E_NITRITE, tol=0.01, unit_label="kJ/mol", units=KJMOL_UNITS, ask_unit=True),
            "traps": [{"value": 201, "tol": 0.001, "message": "That's a pure single bond. Both N–O bonds are identical, with order 1.5."},
                      {"value": 607, "tol": 0.001, "message": "That's a pure double bond. Both N–O bonds are identical, with order 1.5."},
                      {"value": 808, "tol": 0.001, "message": "That's the two bonds' energies added. Bond order 1.5 is halfway between single and double: average them."}]},
    hints=["Ozone's averaged bonds are “somewhere in between” in length (Day 9 p.7). Expect the same for energy.", "Take the halfway energy between 201 and 607 kJ/mol."],
    solution=f"<p>(201 + 607)/2 = <strong>{E_NITRITE:.0f} kJ/mol</strong>. The textbook makes the same halfway estimate for the ring bonds of para-dichlorobenzene, with bond order 1.5: (348 + 614)/2 = 481 kJ/mol (Sample Ex. 4.19, PDF p.219).</p>"
             "<p class='note'>Table 4.6 values are averages over many molecules (the table's title, Day 9 p.14), so halfway estimates are rough. The textbook's carbonate example shows it for lengths: bond order 1.33 predicts “between 143 and 123 pm,” and the measured value is 129 pm (PDF p.208).</p>",
    source="Day 9 p.7, p.14; " + tb("4.6", 206, 208) + "; " + tb("4.9", 219))

add(id="t4-6-m-explain", module="t4-6", kind="mastery", level="Explain",
    prompt="<p>Explain why a C≡C bond is shorter and stronger than a C=C bond, which is shorter and stronger than a C–C bond.</p>",
    answer={"type": "self", "model": "<p>Bond order is the number of shared pairs. More shared electrons between the nuclei attract both nuclei more strongly, pulling them closer (shorter bond) "
                                     "and making the bond harder to break (higher bond energy): C–C 154 pm/348 kJ/mol, C=C 134/614, C≡C 120/839, the first red box in Table 4.6 (Day 9 p.14). "
                                     "Each added pair adds less energy than the first, so a triple bond isn't three times a single bond. (The slides show the numbers; the shared-electron explanation is ours.)</p>"},
    hints=[], solution="", source="Day 9 p.5, p.14; " + tb("4.6", 206, 208))

add(id="t4-6-m-recognize", module="t4-6", kind="mastery", level="Recognize",
    prompt="<p>A measured bond length falls between Table 4.6's single- and double-bond values. What should you suspect?</p>",
    answer=choice(("Resonance: the bond is an average of single and double, with a bond order between 1 and 2.", True, "Right: ozone's 128 pm is the lecture's example (Day 9 p.7)."),
                  ("A measurement error.", False, "Intermediate lengths are real; they signal averaged bonding."),
                  ("The bond is ionic.", False, "Bond length doesn't make a bond ionic."),
                  ("A triple bond.", False, "A triple bond would be shorter than the double bond.")),
    hints=["Ozone: 128 pm, between O–O 148 and O=O 121 (Day 9 p.7)."],
    solution="<p>An intermediate length means the bond is an average of single and double, the signature of resonance (O<sub>3</sub> on Day 9 p.7; NO<sub>3</sub><sup>−</sup> and CO<sub>3</sub><sup>2−</sup> in the textbook).</p>",
    source="Day 9 p.7; " + tb("4.6", 206))

add(id="t4-6-m-sanity", module="t4-6", kind="mastery", level="Sanity check",
    prompt="<p>A student estimates the C≡C bond energy as 3 × 348 = 1044 kJ/mol. Table 4.6 gives 839 kJ/mol. What does the difference tell you?</p>",
    answer=choice(("Bond energy rises with bond order, but not in proportion: the second and third pairs add less than the first.", True,
                   "Right: 348 → 614 → 839 kJ/mol, steps of 266 and 225."),
                  ("Table 4.6 must be wrong.", False, "Every boxed group of the table shows the same pattern (C–O/C=O/C≡O, O–O/O=O; Day 9 p.14)."),
                  ("Triple bonds are weaker than single bonds.", False, "839 is larger than 348."),
                  ("The student should have divided by 3.", False, "That would give a value smaller than a single bond.")),
    hints=["Compare 614 with 2 × 348."],
    solution="<p>Multiplying assumes each shared pair adds the same energy. The table shows otherwise: C=C (614) is less than 2 × 348, and C≡C (839) less than 3 × 348 (Table 4.6, Day 9 p.14).</p>",
    source="Day 9 p.14; " + tb("4.6", 207, 208))

# =====================================================================================
# t4-7  Formal charge (lecture: Day 9 p.19-26; textbook §4.7, PDF p.208-212)
# Relabeled 2026-10-06; p6 (the textbook's bonding-capacity shortcut) stays preview.
# =====================================================================================
CO = LW.STRUCTS["CO"]
assert CO.fcs() == [-1, 1]
add(id="t4-7-attempt", module="t4-7", kind="attempt", level="Guided attempt",
    prompt=f"<p>Carbon monoxide has the Lewis structure</p><p>{LS('CO')}</p><p>Find the formal charge on (a) C and (b) O.</p>",
    answer={"type": "multi", "parts": [
        {"label": "(a) FC on C", **fc_ans(CO.fc(0), traps=[(0, "C has 4 valence electrons but is assigned 2 (lone pair) + 3 (half of 6 shared) = 5.")])},
        {"label": "(b) FC on O", **fc_ans(CO.fc(1), traps=[(0, "O has 6 valence electrons but is assigned only 2 + 3 = 5."),
                                                           (-1, "Formal charge doesn't follow electronegativity. Count: 6 − (2 + ½ × 6).")])}]},
    hints=["Formal charge compares “how many electrons the atoms have in the compound to how many they had as free atoms” (Day 9 p.22): FC = (valence e⁻) − [(lone-pair e⁻) + ½(bonding e⁻)].",
           "Each atom has one lone pair (2 e⁻) and shares the triple bond's 6 electrons, so each is assigned 2 + 3 = 5.",
           "C: 4 − 5 = ?",
           "O: 6 − 5 = ? Check with rule 4 (Day 9 p.23): the formal charges must add to 0 for a neutral molecule."],
    solution=f"<p>{LS('CO', show_fc=True, scale=0.95)}</p><p>(a) C: 4 − (2 + 3) = <strong>−1</strong>. (b) O: 6 − (2 + 3) = <strong>+1</strong>. Sum 0 ✓ (rule 4, Day 9 p.23). "
             "The textbook's shortcut agrees: O forms 3 bonds, one more than its bonding capacity of 2 → +1; C forms 3, one fewer than its 4 → −1 (PDF p.211).</p>",
    compare={"wrong": "<p>“O is more electronegative, so O must be −1 and C +1.”</p>",
             "tempting": "Rule 3 says negative formal charges belong on the more electronegative atom (Day 9 p.23), so it feels like a rule for computing them.",
             "fails": "Rule 3 is for choosing among structures; it doesn't set the charges. Formal charge is a count, done “for each atom” with the four steps (Day 9 p.22). "
                      ":C≡O: is the only structure with octets on both atoms, and its formal charges are C −1, O +1. (The textbook: formal charge “is not a real charge, but rather an accounting system,” PDF p.209.)"},
    source="Day 9 p.22–23; " + tb("4.7", 209, 211) + "; " + tb("4.6", 206))

add(id="t4-7-p1", module="t4-7", kind="practice", level="Warm-up",
    prompt=f"<p>Find the formal charge on O in the hydroxide ion:</p><p>{LS('OH-')}</p>",
    answer=fc_ans(LW.STRUCTS["OH-"].fc(0)),
    hints=["O: 6 valence e⁻; 3 lone pairs = 6 e⁻; one bond = 2 bonding e⁻ (the four steps, Day 9 p.22).", "6 − (6 + 1)."],
    solution="<p>6 − (6 + ½ × 2) = <strong>−1</strong>. H is 1 − (0 + 1) = 0, so the sum is −1, the ion's charge ✓ (rule 4, Day 9 p.23).</p>",
    source="Day 9 p.22–23; " + tb("4.7", 209, 210) + "; " + tb("4.4", 199, 200))

add(id="t4-7-p2", module="t4-7", kind="practice", level="Warm-up",
    prompt=f"<p>Find the formal charge on N in the ammonium ion:</p><p>{LS('NH4+')}</p>",
    answer=fc_ans(LW.STRUCTS["NH4+"].fc(0)),
    hints=["N: 5 valence e⁻, no lone pairs, four bonds (8 bonding e⁻).", "5 − (0 + 4)."],
    solution="<p>5 − (0 + ½ × 8) = <strong>+1</strong>, and each H is 0: sum +1, the ion's charge ✓ (rule 4, Day 9 p.23). "
             "The textbook's shortcut agrees: N forms 4 bonds, one more than its bonding capacity of 3 (PDF p.211).</p>",
    source="Day 9 p.22–23; " + tb("4.7", 209, 211))

CS2_OPT_BAD = LX("CS₂ with single bonds and two lone pairs on C", [("S", 0, 0), ("C", 1.25, 0), ("S", 2.5, 0)], [(0, 1, 1), (1, 2, 1)], {0: 3, 1: 2, 2: 3}, neutral=True)
add(id="t4-7-p3", module="t4-7", kind="practice", level="Standard",
    prompt="<p>Which Lewis structure best describes carbon disulfide, CS<sub>2</sub>?</p>",
    answer=choice((LS("CS2", neutral=True), True, "Right: every formal charge is 0 (rule 1, Day 9 p.23)."),
                  (LS("CS2-alt", neutral=True), False, "Valid electron count and octets, but formal charges +1, 0, −1. A structure with all zeros beats it."),
                  (CS2_OPT_BAD, False, "That uses 20 electrons; CS<sub>2</sub> has only 16.")),
    hints=["Compute the formal charges in each valid structure (Day 9 p.22).", "Rule 1 (Day 9 p.23): the best structure is the one in which the formal charge on each atom is zero."],
    solution=f"<p>{LS('CS2', show_fc=True)} S=C=S: all formal charges 0, so it best represents CS<sub>2</sub> (rule 1). "
             f"The S≡C–S form {LS('CS2-alt', show_fc=True)} carries +1 and −1. The third drawing isn't a valid structure at all: it uses 20 electrons. The textbook reaches the same verdict for CO<sub>2</sub> (Sample Ex. 4.16).</p>",
    source="Day 9 p.22–23; " + tb("4.7", 210, 212))

add(id="t4-7-p4", module="t4-7", kind="practice", level="Standard",
    prompt="<p>In any valid Lewis structure of the sulfate ion, SO<sub>4</sub><sup>2−</sup>, what must the formal charges add up to?</p>",
    answer=fc_ans(-2, traps=[(0, "0 is the sum for a neutral molecule. For an ion, the formal charges add up to the ion's charge.")]),
    hints=["Sulfate's charge is 2−.", "Rule 4: “If you've done it right, the sum of the formal charges will be the charge on the molecule/ion” (Day 9 p.23)."],
    solution="<p><strong>−2</strong>. Both of the professor's sulfate structures pass this check (Day 9 p.30): S +2 with four O at −1 (four single bonds), or S 0 with two O at 0 and two at −1 (two S=O).</p>",
    source="Day 9 p.23, p.30; " + tb("4.7", 210) + "; " + tb("4.8", 215))

add(id="t4-7-p5", module="t4-7", kind="practice", level="Standard",
    prompt="<p>What is the formal charge on a nitrogen atom that has two lone pairs and forms one double bond?</p>",
    answer=fc_ans(-1, traps=[(-3, "Only half of the bonding electrons count: the double bond's 4 electrons contribute 2."),
                             (1, "Compare what N is assigned (4 + 2 = 6) with its 5 valence electrons: more assigned → negative.")]),
    hints=["N is in group 15: 5 valence electrons.", "Assigned: 4 (two lone pairs) + ½ × 4 (double bond) = 6."],
    solution="<p>5 − (4 + 2) = <strong>−1</strong>. It's the end N in N=N=O, one of the three N<sub>2</sub>O structures on Day 9 p.20. "
             "The textbook's shortcut agrees: two bonds, one fewer than N's bonding capacity of 3 → −1 (PDF p.211).</p>",
    source="Day 9 p.20, p.22; " + tb("4.7", 209, 211))

P(id="t4-7-p6", module="t4-7", kind="practice", level="Standard",
  prompt="<p>A Cl atom forms two single bonds and has two lone pairs (an octet). Without writing out Eq. 4.2, what is its formal charge?</p>",
  answer=fc_ans(1, traps=[(-1, "One <em>fewer</em> bond than the bonding capacity gives −1; this Cl has one more.")]),
  hints=["Cl's bonding capacity is 1: one unpaired dot (Day 8 p.18).", "The textbook's shortcut: one more bond than the bonding capacity → +1."],
  solution="<p><strong>+1</strong>. Two bonds is one more than chlorine's bonding capacity of 1, and the textbook's shortcut says that gives +1 (PDF p.211). Check with the four steps (Day 9 p.22): 7 − (4 + 2) = +1.</p>",
  source=tb("4.7", 211) + "; Day 8 p.18; Day 9 p.22")

SCN = {k: LW.STRUCTS[f"SCN-{k}"] for k in "abc"}
assert SCN["a"].fcs() == [-1, 0, 0] and SCN["b"].fcs() == [0, 0, -1] and SCN["c"].fcs() == [1, 0, -2]
assert ELECTRONEGATIVITY["N"] > ELECTRONEGATIVITY["S"]
add(id="t4-7-transfer", module="t4-7", kind="transfer", level="Transfer",
    prompt="<p>The thiocyanate ion, SCN<sup>−</sup> (on the polyatomic-ion table), has the skeleton S–C–N (textbook PDF p.197). Which Lewis structure is best by the rules on Day 9 p.23? (χ: S 2.5, C 2.5, N 3.0; Day 9 p.17.)</p>",
    answer=choice((LS("SCN-a", neutral=True), False, "Formal charges −1 (S), 0, 0. It ties with another structure on rule 2; check where the −1 sits."),
                  (LS("SCN-b", neutral=True), True, "Right: formal charges 0, 0, −1, with the −1 on N, the more electronegative atom (rule 3)."),
                  (LS("SCN-c", neutral=True), False, "Formal charges +1, 0, −2: farther from zero than the other two.")),
    hints=["Compute each atom's formal charge in all three structures (Day 9 p.22). All three have 16 electrons and octets.",
           "No structure is all zeros (it's an ion), so use rule 2, then rule 3 to break a tie (Day 9 p.23)."],
    solution="<div class='lw-row'>" + "".join(LS(f"SCN-{k}", show_fc=True, scale=0.9, caption=k) for k in "abc") + "</div>"
             "<p>a: S −1, C 0, N 0. b: S 0, C 0, N −1. c: S +1, C 0, N −2. Structure c is out (rule 2). a and b tie with two zeros and one −1, "
             "so rule 3 decides: the negative charge belongs on N (χ 3.0) rather than S (2.5). <strong>Structure b</strong> is best.</p>"
             "<p class='bg'>SCN<sup>−</sup>'s measured bond lengths lie between structures a and b, so both contribute. As the professor says of N<sub>2</sub>O, the best structure still isn't the real one (Day 9 p.21).</p>",
    source="Day 9 p.17, p.21–23; Day 8 p.8 (SCN⁻ on the ion table); " + tb("4.7", 210, 211) + "; " + tb("4.4", 197))

add(id="t4-7-m-explain", module="t4-7", kind="mastery", level="Explain",
    prompt="<p>What does a formal charge count, and why isn't it the atom's real charge?</p>",
    answer={"type": "self", "model": "<p>It compares “how many electrons the atoms have in the compound to how many they had as free atoms” (Day 9 p.22): the free atom's valence electrons minus the electrons assigned to it in one structure, "
                                     "all of its lone-pair electrons plus half of each bond's electrons. Splitting every bond exactly in half pretends the pair is shared equally, but most bonds aren't: "
                                     "“one of the atoms has more of the electron density” (Day 9 p.15). So the real charge distribution differs. The textbook calls formal charge “an accounting system,” used to compare possible structures (PDF p.209).</p>"},
    hints=[], solution="", source="Day 9 p.15, p.22; " + tb("4.7", 209))

add(id="t4-7-m-recognize", module="t4-7", kind="mastery", level="Recognize",
    prompt="<p>When do you need formal charges?</p>",
    answer=choice(("When you can draw more than one valid Lewis structure that aren't equivalent, and must choose the best one.", True, "Right: N<sub>2</sub>O on Day 9 p.21–22, and SCN<sup>−</sup> or CO<sub>2</sub>."),
                  ("Every time you count valence electrons.", False, "Counting electrons is step 1 of any structure; formal charge comes after."),
                  ("Only for ionic compounds.", False, "It's for covalent structures, including neutral molecules like N<sub>2</sub>O."),
                  ("Only when resonance structures are equivalent.", False, "Equivalent structures have identical formal-charge patterns, so FC can't choose among them.")),
    hints=["Why did the professor introduce formal charge with N<sub>2</sub>O (Day 9 p.21–22)?"],
    solution="<p>To choose among <strong>nonequivalent</strong> structures: “These structures are not equivalent! … To choose between them, we will introduce the idea of formal charge” (Day 9 p.21–22). "
             "Equivalent resonance structures, like ozone's, need no choosing.</p>",
    source="Day 9 p.21–22; " + tb("4.7", 208, 210))

add(id="t4-7-m-sanity", module="t4-7", kind="mastery", level="Sanity check",
    prompt="<p>For a neutral molecule, a student finds formal charges of +1, 0, and 0. What does that tell you?</p>",
    answer=choice(("There's an error: the formal charges of a neutral molecule must add up to 0.", True, "Right: rule 4 (Day 9 p.23). Recount lone pairs and bonding electrons."),
                  ("The molecule is a radical.", False, "Radicals still have formal charges that add up to the overall charge."),
                  ("The +1 atom is a cation.", False, "Formal charge isn't a real charge, and the sum is wrong anyway."),
                  ("Nothing; any values are possible.", False, "The sum is a built-in check.")),
    hints=["What must the formal charges add up to (Day 9 p.23)?"],
    solution="<p>“If you've done it right, the sum of the formal charges will be the charge on the molecule/ion” (rule 4, Day 9 p.23). A sum of +1 for a neutral molecule means an electron was miscounted.</p>",
    source="Day 9 p.23; " + tb("4.7", 210))

# =====================================================================================
# t4-8  Exceptions to the octet rule (lecture: Day 9 p.27-30; textbook §4.8, PDF p.212-217)
# Relabeled 2026-10-06 (Day 9 teaches all three exceptions); the textbook's reasons are cited where used.
# =====================================================================================
BF3 = LW.STRUCTS["BF3"]
assert BF3.total_valence() == 24 and BF3.shell(0) == 6
add(id="t4-8-attempt", module="t4-8", kind="attempt", level="Guided attempt",
    prompt="<p>Draw BF<sub>3</sub> (B central). (a) How many valence electrons does it have? (b) In the best structure, how many electrons surround B?</p>",
    answer={"type": "multi", "parts": [
        {"label": "(a) valence electrons", **tnum(BF3.total_valence(), traps=[(10, "Count all valence electrons: F has 7 each.")])},
        {"label": "(b) electrons around B", **tnum(BF3.shell(0), traps=[(8, "An octet on B needs a B=F double bond. Work out the formal charges that bond would create.")])}]},
    hints=["B 3 + 3 × F 7 = 24.",
           "Skeleton: three B–F single bonds. Three lone pairs on each F uses 6 + 18 = 24: nothing is left, and B has 6 electrons.",
           "Could step 5 give B an octet? A B=F bond would make that F's formal charge +1 and B's −1 (the four steps, Day 9 p.22).",
           "Rule 3 says negative formal charge belongs on the more electronegative atom (Day 9 p.23), and F is the most electronegative element. So B keeps 6: “Be, B, and Al form electron-deficient molecules” (Day 9 p.27)."],
    solution=f"<p>{LS('BF3', show_fc=True)}</p><p>(a) <strong>24</strong>. (b) <strong>6</strong>. All formal charges are 0. The slide's BCl<sub>3</sub> looks the same (Day 9 p.27), and BF<sub>3</sub> itself appears on Day 10 p.10 with 6 electrons on B. "
             "The textbook: “The three dots in the Lewis symbols of boron and aluminum indicate that their atoms can form three bonds, but doing so results in only six valence-shell electrons … Be, B, and Al tend to form electron-deficient molecules” (PDF p.212).</p>",
    compare={"wrong": "<p>F=BF<sub>2</sub>, with a double bond so that B has an octet.</p>",
             "tempting": "Step 5 says: if the central atom is short, turn an outer lone pair into a bond. That worked for O<sub>3</sub> and HCN.",
             "fails": "Here it gives F a +1 formal charge and B −1: the negative charge on the less electronegative atom and a positive one on fluorine (rule 3, Day 9 p.23). "
                      "Boron has only three valence electrons to share, so it forms three bonds and stays electron-deficient (Day 9 p.27)."},
    source="Day 9 p.22–23, p.27; Day 10 p.10; " + tb("4.8", 212) + "; " + tb("4.7", 210))

add(id="t4-8-p1", module="t4-8", kind="practice", level="Warm-up",
    prompt="<p>How many valence electrons does chlorine dioxide, ClO<sub>2</sub>, have, and what does that number tell you?</p>",
    answer={"type": "multi", "parts": [
        {"label": "valence electrons", **tnum(7 + 2 * 6, traps=[(20, "Cl has 7 valence electrons (group 17), and the molecule is neutral."), (18, "Count Cl's 7 plus 6 for each O.")])},
        {"label": "what it tells you", **choice(("An odd count: at least one electron is unpaired, so ClO<sub>2</sub> is a free radical.", True,
                                                 "Right: “Some species have an odd number of electrons, which forces some of them to be unpaired” (Day 9 p.28)."),
                                                ("An even count: every atom can have an octet.", False, "Check the total: is it even?"),
                                                ("Cl must have an expanded octet.", False, "The odd count is the key fact: some electron is unpaired whatever the arrangement."))}]},
    hints=["Cl (group 17) 7 + 2 × O (group 16) 6.", "Can an odd number of electrons all be in pairs?"],
    solution="<p>7 + 12 = <strong>19</strong>, an odd number, so no Lewis structure can pair every electron: ClO<sub>2</sub> is a <strong>free radical</strong>, like NO (11) and NO<sub>2</sub> (17) on Day 9 p.28.</p>",
    source="Day 9 p.28; " + tb("4.8", 212, 213))

add(id="t4-8-p2", module="t4-8", kind="practice", level="Standard",
    prompt="<p>In PF<sub>5</sub>, how many valence electrons surround the central P atom?</p>",
    answer=tnum(10, traps=[(8, "Count the bonds: five P–F bonds, 2 electrons each.")]),
    hints=["Five P–F single bonds, and no lone pair on P (5 + 35 = 40 electrons; the F atoms' lone pairs use 30).", "Each bond is one shared pair: 2 electrons."],
    solution="<p>5 × 2 = <strong>10</strong>. “Atoms of nonmetals in the third row and below can have expanded octets” (Day 9 p.29): P is in row 3, like the P of the slide's PCl<sub>5</sub> (Day 9 p.30), "
             "and F is one of the strongly electronegative partners (F, O, and Cl) the slide names. PF<sub>5</sub> itself is a VSEPR example on Day 10 p.12.</p>",
    source="Day 9 p.29–30; Day 10 p.12; " + tb("4.8", 214))

add(id="t4-8-p3", module="t4-8", kind="practice", level="Stretch",
    prompt="<p>Bromine pentafluoride, BrF<sub>5</sub>, has Br in the center bonded to five F atoms. How many valence electrons surround Br?</p>",
    answer=tnum(LW.STRUCTS["BrF5"].shell(0), traps=[(10, "Five bonds give 10, but count every electron: are any left over after the F atoms have octets?"),
                                                    (8, "Br is in row 4: it can exceed an octet here (Day 9 p.29).")]),
    hints=["Total: Br 7 + 5 × 7 = 42.", "Five Br–F bonds (10) plus three lone pairs on each F (30) use 40; the last 2 go on Br."],
    solution=f"<p>{LS('BrF5', scale=0.7)} Five bonds (10) + one lone pair (2) = <strong>12</strong> electrons around Br, with every formal charge 0. "
             "Like S in SF<sub>6</sub>, Br is a nonmetal below row 2 and is bonded to F (Day 9 p.29).</p>",
    source="Day 9 p.29; " + tb("4.8", 214))

add(id="t4-8-p4", module="t4-8", kind="practice", level="Concept",
    prompt="<p>Which atom can have more than eight valence electrons around it in a Lewis structure?</p>",
    answer=choice(("S", True, "Right: a nonmetal in the third row (Day 9 p.29)."),
                  ("N", False, "Row 2: its valence shell has only four orbitals, so at most 8 electrons (the textbook's reason, PDF p.212)."),
                  ("C", False, "Row 2: at most 8."),
                  ("O", False, "Row 2: at most 8.")),
    hints=["“Atoms of nonmetals in the third row and below can have expanded octets” (Day 9 p.29)."],
    solution="<p><strong>S</strong>, a nonmetal in the third row (Day 9 p.29). The textbook explains the limit for row 2: nine electrons on N is “impossible for an atom with only four orbitals in its valence shell” (PDF p.212).</p>",
    source="Day 9 p.29; " + tb("4.8", 212, 214))

add(id="t4-8-p5", module="t4-8", kind="practice", level="Concept",
    prompt="<p>In an odd-electron molecule made of N and O atoms, which atom should be left with the incomplete octet?</p>",
    answer=choice(("N, because O is more electronegative and should keep its octet.", True, "Right: the slide's NO and NO<sub>2</sub> both leave N with 7 (Day 9 p.28)."),
                  ("O, because it has more valence electrons to spare.", False, "The slides put the odd electron on N (Day 9 p.28); the textbook adds that leaving O short “makes matters worse”: O attracts bonding electrons more strongly (PDF p.213)."),
                  ("It doesn't matter which one.", False, "The structure with the octet on the more electronegative atom is the reasonable one, as drawn on Day 9 p.28."),
                  ("Neither: move an electron so both have octets.", False, "With an odd total, one electron must stay unpaired (Day 9 p.28).")),
    hints=["Which element attracts bonding electrons more strongly? (χ: N 3.0, O 3.5; Day 9 p.17.)"],
    solution=f"<div class='lw-row'>{LS('NO2-rad1', show_fc=True, scale=0.85)}{RES}{LS('NO2-rad2', show_fc=True, scale=0.85)}</div>"
             "<p><strong>N</strong>, as in the professor's NO and NO<sub>2</sub> (Day 9 p.28). The textbook gives the reason: for NO, moving an electron to give N an octet leaves O with 7, which “makes matters worse because now the more electronegative element (O) … has an incomplete octet” (PDF p.213). "
             "In NO<sub>2</sub> both O atoms keep octets and N has 7 (Sample Ex. 4.17), and its odd electron lets two NO<sub>2</sub> molecules pair up as N<sub>2</sub>O<sub>4</sub> (textbook).</p>",
    source="Day 9 p.17, p.28; " + tb("4.8", 212, 214))

add(id="t4-8-p6", module="t4-8", kind="practice", level="Warm-up",
    prompt="<p>What is a free radical?</p>",
    answer=choice(("An atom, ion, or molecule with unpaired electrons.", True, "Right: the slide's “radicals” or “free radicals” have an odd number of electrons, which “forces some of them to be unpaired” (Day 9 p.28)."),
                  ("Any ion with a negative charge.", False, "Radicals are defined by unpaired electrons, not charge."),
                  ("A molecule with an expanded octet.", False, "SF<sub>6</sub> has 12 electrons on S, all paired."),
                  ("A molecule with a triple bond.", False, "N<sub>2</sub> has a triple bond and no unpaired electrons.")),
    hints=["NO and NO<sub>2</sub> are the examples on Day 9 p.28."],
    solution="<p>“Some species have an odd number of electrons, which forces some of them to be unpaired. These species are called ‘radicals’ or ‘free radicals,’ and they are very reactive” (Day 9 p.28). "
             "The textbook's definition: “an atom, ion, or molecule with unpaired electrons” (PDF p.213).</p>",
    source="Day 9 p.28; " + tb("4.8", 213))

SO3o, SO3e = LW.STRUCTS["SO3-oct"], LW.STRUCTS["SO3-exp"]
assert SO3o.fc(0) == 1 and SO3e.fc(0) == 0 and SO3e.shell(0) == 10
add(id="t4-8-transfer", module="t4-8", kind="transfer", level="Transfer",
    prompt="<p>The sulfite ion, SO<sub>3</sub><sup>2−</sup>, has S bonded to three O atoms and one lone pair on S. "
           "(a) With only single S–O bonds (every atom with an octet), what is the formal charge on S? "
           "(b) Now turn one O lone pair into an S=O double bond, so that S's formal charge becomes 0. How many electrons surround S in that structure?</p>",
    answer={"type": "multi", "parts": [
        {"label": "(a) FC on S, octets only", **fc_ans(SO3o.fc(0))},
        {"label": "(b) electrons around S, minimized FC", **tnum(SO3e.shell(0), traps=[(8, "That's the octet structure. Converting one O lone pair into an S=O bond changes S's count.")])}]},
    hints=["Valence electrons: 6 + 3 × 6 + 2 = 26.",
           "(a) S: 6 − (2 + ½ × 6) = ?",
           "(b) As the professor does for sulfate (Day 9 p.30), turn one O lone pair into an S=O bond: S then has 0 formal charge.",
           "Count around S: 1 lone pair (2) + one double bond (4) + two single bonds (4)."],
    solution=f"<div class='lw-row'>{LS('SO3-oct', show_fc=True, scale=0.85)}{BECOMES}{LS('SO3-exp', show_fc=True, scale=0.85)}</div>"
             "<p>(a) <strong>+1</strong> (and each O −1). (b) <strong>10</strong>: with one S=O, S goes to 0 and that O to 0, leaving −1 on the other two O. "
             "A second S=O wouldn't help: S would go to −1, putting a negative charge on the less electronegative atom (rule 3, Day 9 p.23). "
             "S is in row 3 and bonded to O, so it may expand its octet when that brings formal charges closer to zero (Day 9 p.29). The S=O can be drawn to any of the three O atoms, so the structures are also in resonance.</p>",
    source="Day 9 p.23, p.29–30; Day 8 p.8 (sulfite on the ion table); " + tb("4.8", 214, 216))

add(id="t4-8-m-explain", module="t4-8", kind="mastery", level="Explain",
    prompt="<p>Explain why SF<sub>6</sub> can have 12 electrons around S, but no Lewis structure can give N more than 8.</p>",
    answer={"type": "self", "model": "<p>The professor's rule: “Atoms of nonmetals in the third row and below can have expanded octets,” especially when they bond to F, O, or Cl, and an expanded shell gives formal charges closer to zero (Day 9 p.29). "
                                     "S is in row 3 and bonded to six F, so SF<sub>6</sub> can have 12 (Day 9 p.30). N is in row 2, so it can't. Why it works isn't taught: hypervalency “is not well understood” (Day 9 p.29). "
                                     "The textbook's reason for the row-2 limit is that N's valence shell (2s, 2p) has only four orbitals, which hold at most 8 electrons (PDF p.212). "
                                     "It adds that d orbitals “contribute little” (PDF p.214), and its §5.7 offers a model for SF<sub>6</sub> without an expanded octet (textbook preview, PDF p.271–273).</p>"},
    hints=[], solution="", source="Day 9 p.29–30; " + tb("4.8", 212, 214) + "; " + tb("5.7", 271, 273))

add(id="t4-8-m-recognize", module="t4-8", kind="mastery", level="Recognize",
    prompt="<p>Which species has an odd number of valence electrons, so no structure can give every atom an octet?</p>",
    answer=choice(("NO<sub>2</sub>", True, "Right: 5 + 12 = 17."), ("CO<sub>2</sub>", False, "16, even."), ("O<sub>3</sub>", False, "18, even."), ("NO<sub>3</sub><sup>−</sup>", False, "24 with the charge, even.")),
    hints=["Add up the valence electrons, including any charge."],
    solution="<p><strong>NO<sub>2</sub></strong>, 17 electrons: a free radical (Day 9 p.28).</p>",
    source="Day 9 p.28; " + tb("4.8", 212, 213))

add(id="t4-8-m-sanity", module="t4-8", kind="mastery", level="Sanity check",
    prompt="<p>To give N an octet, a student draws NO with a triple bond (one lone pair on O; one lone pair and one unpaired electron on N). What's wrong?</p>",
    answer=choice(("N would then have 9 electrons, which is impossible for a row-2 atom.", True, "Right: only nonmetals in the third row and below can exceed an octet (Day 9 p.29)."),
                  ("Nothing; both atoms now have octets.", False, "Count N: 6 shared + 2 lone + 1 unpaired = 9."),
                  ("NO has 12 electrons, not 11.", False, "5 + 6 = 11."),
                  ("O can't form triple bonds.", False, "It can (:C≡O:); the problem is N's count.")),
    hints=["Count every electron around N."],
    solution="<p>6 (triple bond) + 2 (lone pair) + 1 (unpaired) = 9 around N. Only nonmetals in the third row and below can exceed an octet (Day 9 p.29); "
             "the textbook calls 9 on N “impossible for an atom with only four orbitals in its valence shell” (PDF p.212). With 11 electrons, the professor's NO leaves N with 7 (Day 9 p.28).</p>",
    source="Day 9 p.28–29; " + tb("4.8", 212, 213))

# =====================================================================================
# t4-9  Vibrating bonds and the greenhouse effect (textbook §4.9, PDF p.217-219)
# =====================================================================================
P(id="t4-9-attempt", module="t4-9", kind="attempt", level="Guided attempt",
  prompt="<p>In CO<sub>2</sub> (O=C=O), the symmetric stretch is IR-inactive: the two identical C=O bonds' fluctuating fields cancel. "
         "Dinitrogen monoxide, N<sub>2</sub>O, is also linear, but its atoms are arranged N–N–O. (a) Is its symmetric stretch (both bonds lengthening and shortening together) IR-active? (b) Why?</p>",
  answer={"type": "multi", "parts": [
      {"label": "(a) IR-active?", **choice(("yes", True, "Right."), ("no", False, "Look at the two bonds: are they identical, like CO<sub>2</sub>'s?"))},
      {"label": "(b) reason", **choice(("Its two bonds are different (N–N and N–O), so their fluctuating fields don't cancel.", True, "Right."),
                                       ("N<sub>2</sub>O isn't linear.", False, "It is linear; the shape isn't the difference."),
                                       ("N<sub>2</sub>O has no polar bonds.", False, "N–O is polar: Δχ = 3.5 − 3.0 = 0.5 (§4.2)."),
                                       ("Every stretch absorbs IR.", False, "CO<sub>2</sub>'s symmetric stretch doesn't."))}]},
  hints=["A vibration absorbs IR only if it makes the molecule's charge separation fluctuate (textbook PDF p.217).",
         "In CO<sub>2</sub>, the two changes are equal and opposite because the two bonds are identical.",
         "In N<sub>2</sub>O, compare the two bonds: N–N (Δχ = 0) and N–O (Δχ = 0.5).",
         "Unequal bonds give unequal changes, which can't cancel."],
  solution="<p>(a) <strong>Yes</strong>. (b) The cancellation in CO<sub>2</sub> depends on two <em>identical</em> polar bonds pointing in opposite directions (Fig. 4.13a). "
           "N<sub>2</sub>O's end atoms differ, so its bonds differ in polarity: when both stretch, the changes in charge separation don't cancel, and the vibration can absorb IR.</p>"
           "<p class='bg'>N<sub>2</sub>O does absorb infrared radiation in this vibration, and it is a greenhouse gas.</p>",
  compare={"wrong": "<p>“N<sub>2</sub>O is linear like CO<sub>2</sub>, so its symmetric stretch is IR-inactive too.”</p>",
           "tempting": "Same straight shape, same kind of motion: it feels like the same case.",
           "fails": "What cancels in CO<sub>2</sub> is two <em>identical</em> bond polarities. In N<sub>2</sub>O the bonds aren't identical, so their changes are unequal and there's a net fluctuation."},
  source=tb("4.9", 217, 218) + "; " + tb("4.7", 208) + "; " + tb("4.2", 186, 187))

P(id="t4-9-p1", module="t4-9", kind="practice", level="Warm-up",
  prompt="<p>Is the stretching vibration of a hydrogen molecule, H<sub>2</sub>, infrared-active?</p>",
  answer=choice(("No: the H–H bond is nonpolar, so stretching it creates no fluctuating field.", True, "Right: identical atoms, Δχ = 0."),
                ("Yes: every bond vibrates.", False, "Every bond vibrates, but only vibrations that change the charge distribution absorb IR."),
                ("Yes: H<sub>2</sub> is the lightest molecule, so it vibrates fastest.", False, "Speed isn't the criterion; a fluctuating charge separation is."),
                ("Only at high temperature.", False, "Temperature doesn't make a nonpolar bond polar.")),
  hints=["What is Δχ for a bond between two identical atoms?"],
  solution="<p><strong>No.</strong> Two identical atoms share electrons equally, so the stretch produces no oscillating field to interact with IR light. N<sub>2</sub> and O<sub>2</sub> are the same case (textbook Concept Test, PDF p.218).</p>",
  source=tb("4.9", 217, 218) + "; " + tb("4.2", 186))

P(id="t4-9-p2", module="t4-9", kind="practice", level="Standard",
  prompt="<p>How many of CO<sub>2</sub>'s three vibrations in textbook Fig. 4.13 are infrared-active?</p>",
  answer=tnum(2, traps=[(3, "One of the three is IR-inactive."), (1, "Both the asymmetric stretch and the bend are active.")]),
  hints=["Symmetric stretch: fields cancel.", "Asymmetric stretch and bend: fields don't cancel."],
  solution="<p><strong>2</strong>: the asymmetric stretch and the bending mode (Fig. 4.13b, c).</p>"
           "<p class='bg'>Strictly, a linear molecule like CO<sub>2</sub> can bend in two perpendicular planes, so it has four vibrations; the figure shows the bend once.</p>",
  source=tb("4.9", 217, 218))

P(id="t4-9-p3", module="t4-9", kind="practice", level="Concept",
  prompt="<p>Earth's average surface temperature is 287 K. In which region of the spectrum does it emit most strongly?</p>",
  answer=choice(("Infrared", True, "Right (textbook §4.9 margin note)."), ("Visible", False, "The much hotter Sun peaks in the visible."),
                ("Ultraviolet", False, "Far too energetic for a 287 K surface."), ("X-ray", False, "Far too energetic.")),
  hints=["Lower temperature → longer peak wavelength (the blackbody curves, Ch. 3)."],
  solution="<p><strong>Infrared</strong>: “The average temperature of Earth's surface is 287 K, which means that it emits its peak intensity of electromagnetic radiation in the infrared region” (textbook PDF p.218).</p>"
           "<p class='bg'>Wien's law puts the peak at λ<sub>max</sub> = (2.898 × 10<sup>−3</sup> m·K)/287 K ≈ 1.0 × 10<sup>−5</sup> m = 10 μm.</p>",
  source=tb("4.9", 218))

P(id="t4-9-p4", module="t4-9", kind="practice", level="Standard",
  prompt="<p>A CO<sub>2</sub> molecule in the atmosphere absorbs an IR photon emitted by Earth's surface. According to the textbook, what happens next?</p>",
  answer=choice(("It later emits a photon of the same energy, which is as likely to head back toward Earth as out to space.", True, "Right: that's how heat gets trapped."),
                ("It keeps the energy permanently.", False, "The energy increase is temporary: the molecule returns to its ground state."),
                ("It always re-emits the photon toward space.", False, "Reemission goes in any direction."),
                ("The C=O bonds break.", False, "IR photons make bonds vibrate; they don't break them.")),
  hints=["The textbook describes absorption, then reemission (PDF p.217)."],
  solution="<p>The molecule's internal energy rises temporarily; it then emits a photon of the same energy as it returns to its ground state. Reemitted photons “are just as likely to move back toward Earth's surface as they are to go upward toward space,” "
           "so a significant fraction of the heat is trapped (PDF p.217).</p>",
  source=tb("4.9", 217))

P(id="t4-9-p5", module="t4-9", kind="practice", level="Standard",
  prompt="<p>Why does a vibrating polar bond interact with infrared light rather than, say, visible light?</p>",
  answer=choice(("Bond vibrations have natural frequencies in the infrared range, and absorption needs the light's frequency to match.", True, "Right (textbook PDF p.217)."),
                ("Visible light can't reach the atmosphere.", False, "It reaches the ground; that's how we see."),
                ("Infrared light has more energy than visible light.", False, "Less: IR photons have longer wavelengths and lower energy (Ch. 3)."),
                ("Polar bonds only absorb light of one color.", False, "The point is the frequency match, not a color.")),
  hints=["Match the vibration's frequency to the photon's frequency."],
  solution="<p>“The natural frequencies of the vibrations correspond to frequencies of infrared radiation” (PDF p.217). A photon at that frequency can interact with the bond's fluctuating field.</p>",
  source=tb("4.9", 217))

P(id="t4-9-transfer", module="t4-9", kind="transfer", level="Transfer",
  prompt="<p>Carbonyl sulfide, O=C=S, is linear like CO<sub>2</sub>, with different atoms at its two ends. How many of its three vibrations (symmetric stretch, asymmetric stretch, bend) can absorb infrared radiation? (χ: O 3.5, C 2.5, S 2.5.)</p>",
  answer=tnum(3, traps=[(2, "In CO<sub>2</sub> the symmetric stretch cancels because the two bonds are identical. Are C=O and C=S identical?"),
                        (1, "Both the asymmetric stretch and the bend were already active in CO<sub>2</sub>.")]),
  hints=["Which CO<sub>2</sub> vibration was inactive, and why?", "C=O is polar (Δχ 1.0) but C=S isn't (Δχ 0): the two bonds can't cancel."],
  solution="<p><strong>3</strong>. The asymmetric stretch and the bend are active for the same reasons as in CO<sub>2</sub>. The symmetric stretch is active too: only one of the two bonds is polar, so nothing cancels its fluctuating field.</p>"
           "<p class='bg'>All three vibrations of OCS do absorb infrared light.</p>",
  source=tb("4.9", 217, 218) + "; " + tb("4.2", 186, 187))

P(id="t4-9-m-explain", module="t4-9", kind="mastery", level="Explain",
  prompt="<p>Explain why CO<sub>2</sub>'s asymmetric stretch absorbs IR but its symmetric stretch doesn't, even though the same two polar bonds vibrate in both.</p>",
  answer={"type": "self", "model": "<p>Each polar C=O bond makes a small electric field that changes as the bond length changes. In the symmetric stretch both bonds lengthen and shorten together, "
                                   "and because they point in opposite directions their changes cancel: no net fluctuation, so IR-inactive. In the asymmetric stretch one bond lengthens as the other shortens, "
                                   "so the changes add up to a side-to-side fluctuation that can absorb an IR photon of the same frequency (textbook Fig. 4.13).</p>"},
  hints=[], solution="", source=tb("4.9", 217, 218))

P(id="t4-9-m-recognize", module="t4-9", kind="mastery", level="Recognize",
  prompt="<p>Which molecule's bond stretch can absorb infrared radiation?</p>",
  answer=choice(("CO", True, "Right: one polar bond (Δχ 1.0)."), ("N<sub>2</sub>", False, "Nonpolar."), ("Cl<sub>2</sub>", False, "Nonpolar."), ("O<sub>2</sub>", False, "Nonpolar.")),
  hints=["Look for a polar bond between different atoms."],
  solution="<p><strong>CO</strong>. The others are made of identical atoms, so their bonds are nonpolar and their stretches are IR-inactive.</p>",
  source=tb("4.9", 217, 218) + "; " + tb("4.2", 186))

P(id="t4-9-m-sanity", module="t4-9", kind="mastery", level="Sanity check",
  prompt="<p>A classmate argues that N<sub>2</sub> and O<sub>2</sub> must be the main greenhouse gases, since they make up 99% of the atmosphere. What's the flaw?</p>",
  answer=choice(("Abundance isn't the test: their nonpolar bonds can't absorb IR, so they don't trap heat.", True, "Right."),
                ("Nothing; the most abundant gases matter most.", False, "Only IR-absorbing gases trap outgoing heat."),
                ("They make up only 50% of the atmosphere.", False, "The 99% figure is the textbook's."),
                ("N<sub>2</sub> and O<sub>2</sub> absorb visible light instead.", False, "They're transparent to visible light.")),
  hints=["Which property lets a molecule absorb IR?"],
  solution="<p>A greenhouse gas must absorb IR, which requires an IR-active vibration (§4.9). N<sub>2</sub> and O<sub>2</sub> have none; CO<sub>2</sub> and CH<sub>4</sub>, present in far smaller amounts, do (textbook §4.1, §4.9).</p>",
  source=tb("4.9", 218) + "; " + tb("4.1", 180))

# =====================================================================================
# Mixed review x36-x47 (Day 8 lecture + Ch. 4 textbook preview; unlabeled until answered)
# =====================================================================================
X(id="x36", label="lecture", prompt="<p>Name Cu(NO<sub>3</sub>)<sub>2</sub>.</p>",
  answer=tname(names("copper(II) nitrate"), traps=[(names("copper(I) nitrate"), "Two NO<sub>3</sub><sup>−</sup> carry −2, so Cu is +2."),
                                                   (["copper nitrate"], "Copper has two common ions; the name needs the numeral (Day 8 p.7)."),
                                                   (["copper dinitrate"], "Ionic names use no prefixes.")]),
  hints=["A transition metal with a polyatomic anion…", "2 × (−1) from nitrate → Cu<sup>2+</sup>."],
  solution="<p>Cu<sup>2+</sup> + 2 NO<sub>3</sub><sup>−</sup>: <strong>copper(II) nitrate</strong> (the slides would space it “copper (II) nitrate”).</p>",
  cue="A transition metal + a polyatomic ion → charge balance gives the Roman numeral; the ion keeps its table name (Day 8 p.7–9).", source="Day 8 p.7–9", home="m16")

X(id="x37", label="lecture", prompt="<p>Write the formula of dinitrogen pentoxide.</p>",
  answer=tformula(["N2O5"], traps=[(["N5O2"], "di- goes with nitrogen, penta- with oxide.")]),
  hints=["Two nonmetals, prefixes in the name…", "di- = 2, penta- = 5."],
  solution="<p><strong>N<sub>2</sub>O<sub>5</sub></strong>.</p>",
  cue="Number prefixes in a name → a covalent compound; each prefix is a subscript (Day 8 p.12–13).", source="Day 8 p.12–13", home="m17")

X(id="x38", prompt="<p>How many valence electrons are in the sulfate ion, SO<sub>4</sub><sup>2−</sup>?</p>",
  answer=tnum(LW.STRUCTS["SO4-oct"].total_valence(), traps=[(30, "Include the charge: 2− adds two electrons."), (28, "A negative charge adds electrons.")]),
  hints=["Count valence electrons, then account for the charge…", "6 + 4 × 6 + 2."],
  solution="<p>6 + 24 + 2 = <strong>32</strong>.</p>",
  cue="A Lewis-structure count for an ion → add one electron per negative charge (textbook step 1).", source=tb("4.4", 197) + "; " + tb("4.8", 215), home="m19")

O3 = LW.STRUCTS["O3a"]
X(id="x39", prompt=f"<p>What is the formal charge on the central O atom in ozone?</p><p>{LS('O3a')}</p>",
  answer=fc_ans(O3.fc(1)),
  hints=["Valence electrons minus the electrons assigned to that atom…", "Central O: 1 lone pair, 3 shared pairs: 6 − (2 + 3)."],
  solution=f"<p>6 − (2 + ½ × 6) = <strong>+1</strong>. {LS('O3a', show_fc=True)} The end O atoms are 0 and −1: sum 0 ✓.</p>",
  cue="“Formal charge on an atom” → Eq. 4.2 (or the bonds-vs.-bonding-capacity shortcut: 3 bonds on O → +1).", source=tb("4.7", 209, 211) + "; Day 8 p.30", home="t4-7")

PO4e = LW.STRUCTS["PO4-exp"]
BO_PO4 = bond_order(PO4e, "P", "O")
assert abs(BO_PO4 - 1.25) < 1e-9
X(id="x40", prompt="<p>The textbook's best Lewis structure of phosphate, PO<sub>4</sub><sup>3−</sup>, has one P=O and three P–O bonds, and the double bond can be drawn to any of the four O atoms. What is the average P–O bond order? Enter a decimal.</p>",
  answer={**num_ans(BO_PO4, tol=0.01), "traps": [{"value": 1.5, "tol": 0.001, "message": "Count shared pairs per bond: 5 pairs over 4 bonds."},
                                                 {"value": 4 / 3, "tol": 0.01, "message": "That's nitrate's 4 pairs over 3 bonds. Phosphate has 5 pairs over 4 bonds."}]},
  hints=["Resonance averages the shared pairs over equivalent bonds…", "(2 + 1 + 1 + 1)/4."],
  solution="<p>5 shared pairs ÷ 4 P–O bonds = <strong>1.25</strong>.</p>",
  cue="Equivalent bonds + a multiple bond that can move → resonance → bond order = shared pairs ÷ bonds.", source=tb("4.8", 216) + "; " + tb("4.6", 207, 208), home="t4-6")

X(id="x41", label="lecture", prompt="<p>Which compound's name needs a Roman numeral?</p>",
  answer=choice(("FeO", True, "Right: iron forms Fe<sup>2+</sup> and Fe<sup>3+</sup>, so this is iron(II) oxide."),
                ("MgO", False, "Magnesium forms only Mg<sup>2+</sup>."), ("Na<sub>2</sub>O", False, "Sodium forms only Na<sup>+</sup>."),
                ("CaO", False, "Calcium forms only Ca<sup>2+</sup>.")),
  hints=["Look for a transition metal…"],
  solution="<p><strong>FeO</strong>, iron(II) oxide. Main-group metals with one common ion need no numeral.</p>",
  cue="A transition metal with more than one common ion → Roman numeral (Day 8 p.7).", source="Day 8 p.7; Day 7 p.19", home="m16")

X(id="x42", label="lecture", prompt="<p>How many lone pairs are in the Lewis structure of ammonia, NH<sub>3</sub>?</p>",
  answer=tnum(sum(LW.STRUCTS["NH3"].lp.values()), traps=[(0, "8 valence electrons, but three bonds use only 6. Where do the other 2 go?"), (4, "H atoms never carry lone pairs.")]),
  hints=["Count the valence electrons and subtract those in bonds…", "8 − 6 = 2 electrons = 1 pair on N."],
  solution=f"<p>{LS('NH3')} <strong>1</strong> lone pair, on N (Day 8 p.22–23).</p>",
  cue="Lone pairs in a Lewis structure → total valence electrons minus bonding electrons (five steps, Day 8 p.21).", source="Day 8 p.21–23", home="m19")

X(id="x43", prompt="<p>Which of these molecules has a vibration that can absorb infrared radiation?</p>",
  answer=choice(("CO<sub>2</sub>", True, "Right: its asymmetric stretch and bend."), ("N<sub>2</sub>", False, "Nonpolar bond: IR-inactive."),
                ("O<sub>2</sub>", False, "Nonpolar bond: IR-inactive."), ("Cl<sub>2</sub>", False, "Nonpolar bond: IR-inactive.")),
  hints=["IR absorption needs a vibration that changes the charge distribution…"],
  solution="<p><strong>CO<sub>2</sub></strong>. Its polar C=O bonds give IR-active asymmetric-stretch and bending vibrations (textbook Fig. 4.13).</p>",
  cue="“Absorbs IR” / greenhouse gas → look for polar bonds whose vibration changes the charge distribution (§4.9).", source=tb("4.9", 217, 218), home="t4-9")

X(id="x44", prompt="<p>Which molecule is electron-deficient (its central atom has fewer than 8 electrons in the best Lewis structure)?</p>",
  answer=choice(("BCl<sub>3</sub>", True, "Right: B forms three bonds and has 6 electrons."), ("NCl<sub>3</sub>", False, "N has 3 bonds + 1 lone pair = 8."),
                ("PCl<sub>3</sub>", False, "P has 3 bonds + 1 lone pair = 8."), ("CCl<sub>4</sub>", False, "C has 4 bonds = 8.")),
  hints=["Which central atom has only three valence electrons to share?"],
  solution="<p><strong>BCl<sub>3</sub></strong>: like BF<sub>3</sub>, boron forms three bonds and ends with 6 valence electrons (textbook §4.8).</p>",
  cue="A group 2 or 13 central atom (Be, B, Al) → expect an electron-deficient molecule (§4.8).", source=tb("4.8", 212), home="t4-8")

X(id="x45", prompt="<p>Name the acid H<sub>2</sub>SO<sub>4</sub>.</p>",
  answer=tname(["sulfuric acid", "sulphuric acid"], traps=[(["sulfurous acid"], "Sulfurous acid is H<sub>2</sub>SO<sub>3</sub>, from sulfite."),
                                                         (["hydrosulfuric acid"], "hydro- is for binary acids like H<sub>2</sub>S(aq)."),
                                                         (["hydrogen sulfate", "dihydrogen sulfate"], "As an acid, it's named from the anion: -ate → -ic acid.")]),
  hints=["An oxoacid: find its anion…", "Sulfate (-ate) → -ic acid."],
  solution="<p>sulfate → <strong>sulfuric acid</strong>.</p>",
  cue="H + an oxoanion → an oxoacid: -ate → -ic, -ite → -ous (textbook §4.3).", source=tb("4.3", 194), home="t4-3")

X(id="x46", label="lecture", prompt="<p>How many dots are in the Lewis symbol of silicon (group 14)?</p>",
  answer=tnum(4, traps=[(14, "A Lewis symbol shows only valence electrons.")]),
  hints=["Dots = valence electrons…", "Group 14 → 4."],
  solution=f"<p>{LW.symbol_svg('Si')[0]} <strong>4</strong>, all unpaired: bonding capacity 4, like C.</p>",
  cue="“Lewis symbol” → valence electrons only, one per side before pairing (Day 8 p.17).", source="Day 8 p.17–18", home="m18")

X(id="x47", prompt="<p>Which bond is the longest?</p>",
  answer=choice(("C–C", True, "Right: 154 pm."), ("C=C", False, "134 pm."), ("C≡C", False, "120 pm."), ("C–H", False, "110 pm: H is small.")),
  hints=["Bond order and atom size both matter…"],
  solution="<p><strong>C–C</strong>, 154 pm (Table 4.6): the lowest carbon–carbon bond order, and C is larger than H.</p>",
  cue="Compare bond lengths → bond order first (more shared pairs, shorter), then atom size (§4.6).", source=tb("4.6", 207), home="t4-6")

# the Ch. 4 items were written correct-option-first; spread the correct answers over the positions
CHOICE_PERMS = choice_order.spread(PROBLEMS[CH4_START:])

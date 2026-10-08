"""Problem bank K: Ch. 5 §5.6-5.7: chirality (Day 10 p.3, p.6; textbook §5.6, PDF p.255-261) and molecular orbital theory (Day 11 p.27; Day 12 p.4-13; textbook §5.7, PDF p.261-273).

t5-6: the lecture shows chiral carvone (Day 10 p.6) without defining "chiral"; the definitions, the mirror-image test,
optical activity, and molecular recognition are textbook §5.6 (with §5.1, PDF p.232), so most items are preview.
Day 12 p.4 prints §5.6 in grey, so it stays preview.
t5-7: Day 11 p.27 poses O2's paramagnetism; Day 12 p.6-13 teaches MO theory: H2, H2-, He2 (p.8-9), MOs from 2p
(p.10), Li2-Ne2 with both energy orders and their bond orders, HOMO and LUMO (p.11), and which model answers which
question (p.13). Items that need only that (homonuclear diatomics and 1s-only species, bond order, paramagnetism) are
lecture; items built on two-element 2p species (the textbook's NO convention), the textbook's ions, or ozone's pi
system stay preview.
Bond orders and unpaired-electron counts are computed here by filling the textbook's valence MO orders (Figs.
5.45-5.52); stereocenter counts come from RDKit's stereo perception. check_problem_bank_k.py re-derives both
independently (electron-by-electron filling; neighbour symmetry classes) and against the textbook's printed values.

Textbook overlap (checked 2026-10-06): practice items use species that are not the textbook's worked examples, Sample
or Practice Exercises, Concept Tests, Visual Problems, or end-of-chapter problems (Ch. 5, PDF p.255-285), nor the
mixed review's (x58-x60). The textbook's own cases (CHBrClF and CHBr2Cl, NO, ozone) are taught in the modules' preview
boxes; O2 (Day 11 p.27), carvone (Day 10 p.6), and H2, H2-, He2, Li2-Ne2 (Day 12 p.8-11) are lecture examples. Neither MO
explorer preset (O2, N2, B2, He2, NO, O2 2-) is an attempt or transfer species."""
import hashlib

from rdkit import Chem

from guide_common import *                                              # noqa: F401,F403
from problem_bank_a import PROBLEMS, add, num_ans, choice, KJMOL_UNITS  # noqa: F401
from problem_bank_b import text_ans, formula_ans, order_ans           # noqa: F401
from problem_bank_c import P, tb                                       # noqa: F401
from problem_bank_e import X                                           # noqa: F401
from problem_bank_f import LS, LX, tname, tformula, tnum, names        # noqa: F401
import problem_bank_g                                                  # noqa: F401  (Ch. 4 banks load first)
import choice_order
import lewis as LW                                                     # noqa: F401

K_START = len(PROBLEMS)

# ---------------------------------------------------------------- molecular orbitals (textbook §5.7)
MO_VAL = {"H": 1, "He": 2, "Li": 1, "Be": 2, "B": 3, "C": 4, "N": 5, "O": 6, "F": 7, "Ne": 8}
MO_Z = {"H": 1, "He": 2, "Li": 3, "Be": 4, "B": 5, "C": 6, "N": 7, "O": 8, "F": 9, "Ne": 10}
S1, S1S = "σ<sub>1s</sub>", "σ*<sub>1s</sub>"
S2, S2S, P2, S2P, P2S, S2PS = "σ<sub>2s</sub>", "σ*<sub>2s</sub>", "π<sub>2p</sub>", "σ<sub>2p</sub>", "π*<sub>2p</sub>", "σ*<sub>2p</sub>"
# valence MOs from the bottom up: (label, orbitals in the set, bonding?)
ORDER_1S = [(S1, 1, True), (S1S, 1, False)]                                                       # H2, He2 (Figs. 5.45-5.46)
ORDER_LIGHT = [(S2, 1, True), (S2S, 1, False), (P2, 2, True), (S2P, 1, True), (P2S, 2, False), (S2PS, 1, False)]   # Z ≤ 7 (Fig. 5.49a)
ORDER_HEAVY = [(S2, 1, True), (S2S, 1, False), (S2P, 1, True), (P2, 2, True), (P2S, 2, False), (S2PS, 1, False)]   # O2-Ne2 (Fig. 5.49b); NO (Fig. 5.52)


def mo(a, b, charge=0, order=None):
    """valence MO occupancy of the diatomic a-b with the given charge: lowest MOs first, two electrons per orbital,
    one per orbital through a degenerate set before pairing (textbook guidelines 4-5, PDF p.264)."""
    n = MO_VAL[a] + MO_VAL[b] - charge
    if order is None:
        if {a, b} <= {"H", "He"}:
            order = ORDER_1S
        elif a == b and MO_Z[a] <= 7:
            order = ORDER_LIGHT
        else:
            order = ORDER_HEAVY      # O2-Ne2, and heteronuclear diatomics as in the NO diagram (Fig. 5.52; Sample Ex. 5.9 practice: CO)
    occ, left = [], n
    for lab, k, bonding in order:
        e = min(left, 2 * k)
        left -= e
        occ.append((lab, k, bonding, e))
    assert left == 0, (a, b, charge)
    nb = sum(e for _, _, bd, e in occ if bd)
    na = sum(e for _, _, bd, e in occ if not bd)
    return {"n": n, "bonding": nb, "antibonding": na, "bo": (nb - na) / 2,
            "unpaired": sum(min(e, 2 * k - e) for _, k, _, e in occ),
            "config": "".join(f"({lab})<sup>{e}</sup>" for lab, _, _, e in occ if e)}


SPECIES = {"O2": ("O", "O", 0), "N2": ("N", "N", 0), "C2": ("C", "C", 0), "NO": ("N", "O", 0), "Be2": ("Be", "Be", 0),
           "Ne2": ("Ne", "Ne", 0),
           "NF": ("N", "F", 0), "NF+": ("N", "F", 1), "HeH+": ("He", "H", 1), "H2-2": ("H", "H", -2),
           "Li2-2": ("Li", "Li", -2), "Be2+2": ("Be", "Be", 2), "Be2-2": ("Be", "Be", -2), "F2+2": ("F", "F", 2),
           "Ne2+2": ("Ne", "Ne", 2), "He2+2": ("He", "He", 2), "BN-": ("B", "N", -1), "BF": ("B", "F", 0),
           "BF-": ("B", "F", -1), "CO-": ("C", "O", -1), "OF+": ("O", "F", 1), "OF": ("O", "F", 0), "OF-": ("O", "F", -1),
           "CF+": ("C", "F", 1), "CF": ("C", "F", 0), "CN-": ("C", "N", -1)}
SP = {k: mo(*v) for k, v in SPECIES.items()}
SPH = {k: ((f"{a}<sub>2</sub>" if a == b else a + b) + (f"<sup>{LW.sup_charge(q)}</sup>" if q else "")) for k, (a, b, q) in SPECIES.items()}


def bo(d):
    return LW.bo_text(d["bo"])


def mo_table(species):
    rows = "".join(f"<tr><td>{SPH[x]}</td><td>{SP[x]['n']}</td><td>{SP[x]['config']}</td><td>{bo(SP[x])}</td></tr>" for x in species)
    return ("<div class='table-wrap'><table class='data'><thead><tr><th scope='col'>Species</th><th scope='col'>Valence e⁻</th>"
            "<th scope='col'>Configuration</th><th scope='col'>Bond order</th></tr></thead><tbody>" + rows + "</tbody></table></div>")


# ---------------------------------------------------------------- stereocenters (textbook §5.6)
def stereocenters(smiles):
    """number of stereocenters, from RDKit's stereo perception (unassigned centers included)."""
    return len(Chem.FindMolChiralCenters(Chem.MolFromSmiles(smiles), includeUnassigned=True, useLegacyImplementation=False))


SMI = {"2-butanol": "CC(O)CC", "CHFClI": "FC(Cl)I", "CHCl2I": "ClC(Cl)I", "CH2FI": "FCI", "CF2ClBr": "FC(F)(Cl)Br",
       "glyceraldehyde": "OCC(O)C=O", "glycerol": "OCC(O)CO", "1-phenylethanol": "CC(O)c1ccccc1", "2-propanol": "CC(C)O",
       "CH2BrCl": "ClCBr", "pseudoephedrine": "CNC(C)C(O)c1ccccc1", "limonene": "CC1=CCC(CC1)C(C)=C",
       "carvone": "CC1=CCC(CC1=O)C(C)=C", "CHBrClI": "ClC(Br)I", "CHBrI2": "BrC(I)I", "styrene": "C=Cc1ccccc1"}
NSC = {k: stereocenters(v) for k, v in SMI.items()}
assert NSC["carvone"] == NSC["limonene"] == NSC["2-butanol"] == NSC["CHFClI"] == NSC["CHBrClI"] == 1
assert NSC["pseudoephedrine"] == 2 and NSC["styrene"] == NSC["CHBrI2"] == 0


def chir(name):
    return "chiral" if NSC[name] else "achiral"


RES = "<span class='lw-arrow' role='img' aria-label='resonance arrow'>↔</span>"

# =====================================================================================
# t5-6  Chirality and molecular recognition (lecture: Day 10 p.6, carvone; textbook §5.6, PDF p.255-261)
# =====================================================================================
BUTANOL_SVG = LS("2-butanol", highlight=(1,), scale=0.8,
                 label="Lewis structure of 2-butanol: a chain of four carbon atoms, the second carrying an O–H group; the second carbon is circled as the stereocenter")
P(id="t5-6-attempt", module="t5-6", kind="attempt", level="Guided attempt",
  prompt="<p>2-Butanol, CH<sub>3</sub>CH(OH)CH<sub>2</sub>CH<sub>3</sub>, is a chain of four carbon atoms with an OH group on the second carbon. "
         "(a) How many stereocenters (chiral carbon atoms) does it have? (b) Is 2-butanol chiral?</p>",
  answer={"type": "multi", "parts": [
      {"label": "(a) stereocenters", **tnum(NSC["2-butanol"], traps=[
          (0, "Look at the second carbon: its four groups are H, OH, CH<sub>3</sub>, and CH<sub>2</sub>CH<sub>3</sub>. Are any two of them the same?"),
          (2, "The third carbon is a CH<sub>2</sub>: two of its four groups are identical H atoms, so it can't be a stereocenter.")])},
      {"label": "(b) chiral?", **choice(("yes", True, "Right: a molecule with one stereocenter can't be superimposed on its mirror image."),
                                        ("no", False, "Find the stereocenter first: a carbon with four different groups is the most common cause of chirality (textbook PDF p.257)."))}]},
  hints=["Chiral means “not superimposable on its mirror image” (textbook PDF p.256). The usual cause is a stereocenter: an sp<sup>3</sup> carbon bonded to four different atoms or groups of atoms.",
         "Check the carbons one at a time. A carbon that carries two or three identical groups (a CH<sub>2</sub> or a CH<sub>3</sub>) can't be a stereocenter.",
         "The first and fourth carbons are CH<sub>3</sub> groups and the third is a CH<sub>2</sub>, so only the second carbon is left to check.",
         "The second carbon's four groups are –H, –OH, –CH<sub>3</sub>, and –CH<sub>2</sub>CH<sub>3</sub>. Compare whole groups, not just the first atom: is a one-carbon group the same as a two-carbon group?"],
  solution=f"<p>{BUTANOL_SVG}</p>"
           "<p>(a) <strong>1</strong>: the second carbon (circled) is bonded to H, OH, CH<sub>3</sub>, and CH<sub>2</sub>CH<sub>3</sub>, four different groups. "
           "(b) <strong>Yes</strong>. 2-Butanol exists as two enantiomers, mirror images that can't be superimposed. Both have this same flat Lewis structure; "
           "only a 3-D drawing, with a wedge and a dash at that carbon, tells them apart. The textbook's Sample Ex. 5.6(a) makes the same kind of comparison: "
           "a carbon bonded to CH<sub>3</sub>, H, a two-carbon group, and a three-carbon group is a stereocenter (PDF p.259).</p>",
  compare={"wrong": "<p>“The second carbon is bonded to H, O, C, and C. Two of its neighbors are the same element, so it isn't a stereocenter, and 2-butanol is achiral.”</p>",
           "tempting": "CHBrClF, the textbook's first chiral molecule, has four different <em>atoms</em> on its carbon, so it's natural to compare only the atoms that touch the carbon.",
           "fails": "The test is four different atoms <em>or groups of atoms</em> (textbook PDF p.256). The two carbons attached to it begin different groups: the CH<sub>3</sub> ends there, "
                    "while the CH<sub>2</sub> continues to another CH<sub>3</sub>. No rotation of the mirror image can swap a one-carbon group with a two-carbon group, so the second carbon is a stereocenter. "
                    "As the textbook puts it, “we often have to look beyond the atoms bonded directly to it” (PDF p.259)."},
  source=tb("5.6", 256, 259))

add(id="t5-6-p1", module="t5-6", kind="practice", level="Warm-up",
    prompt="<p>On Day 10 p.6, the professor's example of chiral molecules is “R(−) and S(+) carvone”: one smells of spearmint, the other of caraway. What is different about the two molecules?</p>",
    answer=choice(("Only the 3-D arrangement of the groups at one carbon (the circled one); the formula and the bonds are the same.", True,
                   "Right: same formula, C<sub>10</sub>H<sub>14</sub>O, and the same bonds. That's the slide's point: “Molecular geometries are clearly more complicated than Lewis structures” (Day 10 p.6)."),
                  ("Their molecular formulas.", False, "Both are C<sub>10</sub>H<sub>14</sub>O: the slide draws a single condensed structure that fits both."),
                  ("Which atoms are bonded to which.", False, "The atoms are connected the same way in both. That's why one Lewis structure fits both."),
                  ("One has a C=O double bond and the other doesn't.", False, "Both drawings have the ring's C=O and its C=C bonds.")),
    hints=["Compare the two wedge drawings on the slide. What changes at the circled carbon, and what stays the same?"],
    solution="<p>The two carvones have the same formula and the same bonds. They differ only in how two groups at the circled carbon point in space: "
             "in the caraway drawing the H is on a dashed wedge (behind the ring) and the –C(CH<sub>3</sub>)=CH<sub>2</sub> group on a solid wedge (in front); "
             "in the spearmint drawing it's the other way round (Day 10 p.6). That's why the professor introduces them with “Molecular geometries are clearly more complicated than Lewis structures.” "
             "The textbook calls molecules like these stereoisomers, and because the two carvones are mirror images, enantiomers (PDF p.256).</p>",
    source="Day 10 p.6; " + tb("5.6", 255, 256))

P(id="t5-6-p2", module="t5-6", kind="practice", level="Warm-up",
  prompt="<p>Match each term with its textbook definition.</p>",
  answer={"type": "match",
          "rows": [{"html": "isomers", "answer": "iso"}, {"html": "stereoisomers", "answer": "stereo"},
                   {"html": "enantiomers", "answer": "enan"}, {"html": "racemic mixture", "answer": "rac"}],
          "options": [{"key": "rac", "html": "equal amounts of the two mirror-image forms of a compound"},
                      {"key": "stereo", "html": "same formula and same bonds, different arrangement of the atoms in space"},
                      {"key": "enan", "html": "a pair of molecules that are nonsuperimposable mirror images"},
                      {"key": "iso", "html": "same chemical formula, different molecular structures"}]},
  hints=["Start with the broadest term and narrow down: which terms require the same bonds, and which require mirror images?"],
  solution="<p><strong>Isomers</strong>: “compounds that have the same chemical formula but different molecular structures.” "
           "<strong>Stereoisomers</strong>: “molecules with the same formula and bonding order, but with different spatial arrangements of their atoms,” so their Lewis structures are identical. "
           "<strong>Enantiomers</strong>: stereoisomers whose structures are “nonsuperimposable mirror images,” like the two carvones (PDF p.256). "
           "<strong>Racemic mixture</strong>: “a sample containing equal amounts of both enantiomers of a compound” (PDF p.260). "
           "Each term is narrower than the one before it: all enantiomers are stereoisomers, and all stereoisomers are isomers.</p>",
  source=tb("5.6", 256, 260))

P(id="t5-6-p3", module="t5-6", kind="practice", level="Concept",
  prompt="<p>Which of these molecules is chiral?</p>",
  answer=choice(("CHFClI", NSC["CHFClI"] > 0, "Right: H, F, Cl, and I are four different atoms on one carbon, so the molecule can't be superimposed on its mirror image."),
                ("CHCl<sub>2</sub>I", NSC["CHCl2I"] > 0, "Two of its four groups are Cl atoms. Reflect it and turn the image about the C–H bond: it lands on the original."),
                ("CH<sub>2</sub>FI", NSC["CH2FI"] > 0, "Two of its groups are H atoms, so a turn of the mirror image puts every atom back on an atom of the same element."),
                ("CF<sub>2</sub>ClBr", NSC["CF2ClBr"] > 0, "Two of its groups are F atoms: the mirror image can be turned to match the original.")),
  hints=["Look for a carbon bonded to four <em>different</em> atoms or groups."],
  solution="<p><strong>CHFClI</strong>: four different atoms on one carbon, so the molecule and its mirror image are two different molecules, enantiomers. "
           "Each of the others repeats an atom (two Cl, two H, two F), and a molecule like that can always be turned to match its mirror image. "
           "It's the test the textbook applies to CHBrClF and CHBr<sub>2</sub>Cl (Fig. 5.40, PDF p.257).</p>",
  source=tb("5.6", 256, 257))

P(id="t5-6-p4", module="t5-6", kind="practice", level="Concept",
  prompt="<p>A company tests the two enantiomers of a new drug. One binds tightly to its target protein; its mirror image barely binds at all. "
         "The two have the same formula, the same bonds, and the same polarity. What explains the difference?</p>",
  answer=choice(("The binding site is built from chiral molecules, so only one mirror-image shape fits it, as a left glove fits only a left hand.", True,
                 "Right: molecular recognition depends on complementary 3-D shapes (textbook §5.1, §5.6)."),
                ("The two enantiomers must differ by an atom somewhere.", False, "Enantiomers have identical formulas and identical bonds; only the arrangement in space differs."),
                ("It can't be the molecules: one of the samples must be impure.", False, "Pure enantiomers often act very differently. The textbook's examples include albuterol, the methorphans, and the carvones."),
                ("One enantiomer is polar and the other isn't.", False, "Mirror images have the same bond dipoles, arranged as mirror images, so they have the same polarity.")),
  hints=["“The human body is a chiral environment” (textbook PDF p.260). What does a chiral binding site do with two mirror-image molecules?"],
  solution="<p>Biological effects depend on <strong>molecular recognition</strong>: a molecule must fit a receptor or active site with a complementary 3-D shape (textbook §5.1, PDF p.232; §5.5, PDF p.253). "
           "Proteins are chiral (PDF p.257), so “just as a left glove fits only a left hand,” one enantiomer fits a site that its mirror image doesn't (PDF p.232). "
           "That's how one carvone smells of spearmint and the other of caraway (Day 10 p.6), and why “typically, only one enantiomer of a chiral drug is active” (PDF p.260).</p>",
  source=tb("5.6", 257, 260) + "; " + tb("5.1", 232) + "; Day 10 p.6")

P(id="t5-6-p5", module="t5-6", kind="practice", level="Standard",
  prompt="<p>Classify each molecule as chiral or achiral.</p>",
  answer={"type": "match",
          "rows": [{"html": "glyceraldehyde, HOCH<sub>2</sub>–CH(OH)–CHO", "answer": chir("glyceraldehyde")},
                   {"html": "glycerol, HOCH<sub>2</sub>–CH(OH)–CH<sub>2</sub>OH", "answer": chir("glycerol")},
                   {"html": "1-phenylethanol, C<sub>6</sub>H<sub>5</sub>–CH(OH)–CH<sub>3</sub>", "answer": chir("1-phenylethanol")},
                   {"html": "2-propanol, CH<sub>3</sub>CH(OH)CH<sub>3</sub>", "answer": chir("2-propanol")},
                   {"html": "bromochloromethane, CH<sub>2</sub>BrCl", "answer": chir("CH2BrCl")}],
          "options": [{"key": "achiral", "html": "achiral"}, {"key": "chiral", "html": "chiral"}]},
  hints=["In each molecule, find the sp<sup>3</sup> carbon that could be a stereocenter and list its four groups. (C<sub>6</sub>H<sub>5</sub> is a benzene ring; its carbons are sp<sup>2</sup>.)",
         "Two H atoms, or two identical groups such as CH<sub>3</sub> or CH<sub>2</sub>OH, on the same carbon rule that carbon out."],
  solution="<p><strong>Glyceraldehyde</strong>: chiral; its middle carbon carries H, OH, CH<sub>2</sub>OH, and CHO. "
           "<strong>Glycerol</strong>: achiral; its middle carbon carries two identical CH<sub>2</sub>OH groups. Changing one end of the molecule is enough to remove the stereocenter. "
           "<strong>1-Phenylethanol</strong>: chiral (H, OH, CH<sub>3</sub>, and the ring). <strong>2-Propanol</strong>: achiral (two CH<sub>3</sub> groups on the middle carbon). "
           "<strong>CH<sub>2</sub>BrCl</strong>: achiral (two H atoms).</p>",
  source=tb("5.6", 256, 259))

P(id="t5-6-p6", module="t5-6", kind="practice", level="Standard",
  prompt="<p>Day 10 p.6 calls the spearmint compound “R(−) carvone” and the caraway compound “S(+) carvone.” (a) What does the (−) tell you? "
         "(b) What does a 50 : 50 mixture of the two do to plane-polarized light?</p>",
  answer={"type": "multi", "parts": [
      {"label": "(a) the (−)", **choice(("The compound rotates the plane of polarized light counterclockwise.", True, "Right: (+) is clockwise, (−) counterclockwise (textbook PDF p.256)."),
                                        ("The molecule carries a negative charge.", False, "Carvone is a neutral molecule; the sign belongs to the rotation, not to a charge."),
                                        ("It rotates light to the right, because R means right.", False, "R isn't a direction of rotation. It names the arrangement around the stereocenter, and this R compound rotates light counterclockwise: (−)."),
                                        ("It's the less stable of the two forms.", False, "The sign says nothing about stability; it reports the direction of rotation."))},
      {"label": "(b) a 50 : 50 mixture", **choice(("It doesn't rotate the light at all.", True, "Right: equal and opposite rotations cancel. That's a racemic mixture."),
                                                  ("It rotates the light half as far as pure (−)-carvone does.", False, "The (+) form rotates the light just as far the other way, so the two cancel completely."),
                                                  ("It rotates the light clockwise, because the (+) form wins.", False, "Neither wins: the amounts and the angles are equal."),
                                                  ("It rotates the light twice as far.", False, "The two rotations are in opposite directions, so they cancel instead of adding."))}]},
  hints=["The textbook adds (+) and (−) to names “to refer to the specific effect each isomer has on plane-polarized light” (PDF p.256).",
         "In a racemic mixture, “one isomer rotates the plane of polarized light in one direction, and the other to the same extent in the opposite direction” (PDF p.260)."],
  solution="<p>(a) (−) means the compound rotates plane-polarized light <strong>counterclockwise</strong>; (+) means clockwise (textbook Fig. 5.39, PDF p.256–257). "
           "(b) <strong>No rotation</strong>: a 50 : 50 mixture is a racemic mixture, and the two equal, opposite rotations cancel (PDF p.260).</p>"
           "<p class='bg'>R and S are a separate label. They describe the 3-D arrangement of the four groups around the stereocenter, by naming rules from organic chemistry that neither the slides nor the textbook's §5.6 cover. "
           "R or S doesn't predict the sign of rotation, which has to be measured. The slide pairs the labels correctly: (R)-(−)-carvone is spearmint and (S)-(+)-carvone is caraway.</p>",
  source="Day 10 p.6; " + tb("5.6", 256, 260))

P(id="t5-6-p7", module="t5-6", kind="practice", level="Stretch",
  prompt="<p>The circled carbon in carvone (Day 10 p.6) is bonded to an H atom, to a –C(CH<sub>3</sub>)=CH<sub>2</sub> group, and to two ring –CH<sub>2</sub>– groups. "
         "Why do the two ring –CH<sub>2</sub>– groups count as <em>different</em> groups?</p>",
  answer=choice(("Going around the ring one way from the circled carbon leads to the C=C double bond; going the other way leads to the C=O group.", True, "Right: the textbook's explanation (PDF p.258)."),
                ("They don't: the circled carbon isn't really a stereocenter.", False, "Then the two carvones would be one and the same molecule, with one smell."),
                ("One –CH<sub>2</sub>– points in front of the ring and the other behind it.", False, "Both are part of the ring. Front and back describe the H and the side group at the circled carbon."),
                ("One of the two carbons has a lone pair.", False, "A ring –CH<sub>2</sub>– carbon forms four bonds and has no lone pairs.")),
  hints=["Look past the –CH<sub>2</sub>– groups themselves. What is each one bonded to next, going around the ring?"],
  solution="<p>Follow the ring from the circled carbon: one way you reach the CH= carbon of the ring's C=C bond, the other way the C=O carbon. "
           "“That asymmetry in the ring is the reason that carvone is not superimposable on its mirror image” (textbook PDF p.258). "
           "With the H and the –C(CH<sub>3</sub>)=CH<sub>2</sub> group, that makes four different groups. "
           "For ring carbons the textbook's advice is to walk around the ring looking for an asymmetry (Sample Ex. 5.6, Think About It, PDF p.259).</p>",
  source="Day 10 p.6; " + tb("5.6", 257, 259))

P(id="t5-6-p8", module="t5-6", kind="practice", level="Stretch",
  prompt="<p>Pseudoephedrine, a decongestant in some cold medicines, is C<sub>6</sub>H<sub>5</sub>–CH(OH)–CH(CH<sub>3</sub>)–NH–CH<sub>3</sub>, where C<sub>6</sub>H<sub>5</sub> is a benzene ring. "
         "How many stereocenters (carbon atoms bonded to four different groups) does it have?</p>",
  answer=tnum(NSC["pseudoephedrine"], traps=[(1, "Check both CH carbons: the one with the OH and the one with the CH<sub>3</sub> branch."),
                                             (0, "Each CH carbon here carries four different groups."),
                                             (3, "Count only carbon atoms. The N, with its lone pair, flips between its two arrangements, so the textbook doesn't treat it as a stereocenter (Sample Ex. 5.10, PDF p.274).")]),
  hints=["Only sp<sup>3</sup> carbons with four different groups count. The ring carbons are sp<sup>2</sup>, and each CH<sub>3</sub> carries three identical H atoms.",
         "List the four groups on each CH. The one with the OH: H, OH, the ring, and CH(CH<sub>3</sub>)NHCH<sub>3</sub>. The other: H, CH<sub>3</sub>, NHCH<sub>3</sub>, and CH(OH)C<sub>6</sub>H<sub>5</sub>."],
  solution="<p><strong>2</strong>: both CH carbons have four different groups. A molecule can have several stereocenters; the textbook's Sample Ex. 5.6(e) has three (PDF p.259).</p>"
           "<p class='bg'>Two stereocenters give four stereoisomers (two pairs of enantiomers). Pseudoephedrine is one of them; ephedrine, a different drug, is another.</p>",
  source=tb("5.6", 256, 259) + "; textbook Sample Ex. 5.10, PDF p.274 (printed 240)")

P(id="t5-6-transfer", module="t5-6", kind="transfer", level="Transfer",
  prompt="<p>Limonene, C<sub>10</sub>H<sub>16</sub>, gives orange peel much of its smell. Its structure is carvone's (Day 10 p.6) with the ring's C=O group replaced by a CH<sub>2</sub> group. "
         "(a) Is the ring carbon that carries the –C(CH<sub>3</sub>)=CH<sub>2</sub> group still a stereocenter? "
         "(b) A sample labeled “racemic limonene” is placed in a polarimeter. What happens to the plane of polarized light?</p>",
  answer={"type": "multi", "parts": [
      {"label": "(a) still a stereocenter?", **choice(("Yes: around the ring one way, a single CH<sub>2</sub> leads to the C=C; the other way, two CH<sub>2</sub> groups come first, so the ring branches still differ.", NSC["limonene"] == 1,
                                                       "Right: the two ring branches differ in how far they are from the C=C."),
                                                      ("No: without the C=O, its two ring –CH<sub>2</sub>– branches are identical.", False, "Look farther along each branch. One CH<sub>2</sub> is bonded to a ring C=C carbon, the other to another CH<sub>2</sub>."),
                                                      ("No: a carbon in a ring can't be a stereocenter.", False, "Carvone's circled carbon is a ring carbon and a stereocenter (Day 10 p.6)."),
                                                      ("Yes, and so is every other ring carbon.", False, "The ring CH<sub>2</sub> carbons carry two identical H atoms, and the C=C carbons are sp<sup>2</sup>."))},
      {"label": "(b) racemic limonene", **choice(("Nothing: equal amounts of the two enantiomers rotate it equally in opposite directions.", True, "Right: a racemic mixture is optically inactive."),
                                                 ("It rotates clockwise, because one enantiomer is the orange-peel form.", False, "A racemic mixture contains as much of the (−) form as the (+) form, so the rotations cancel."),
                                                 ("It rotates twice as far as one enantiomer would.", False, "The two rotations are in opposite directions, so they cancel."))}]},
  hints=["(a) Walk around the ring from that carbon in both directions. What does each ring branch reach, and after how many steps?",
         "(b) “A racemic mixture does not rotate plane-polarized light at all” (textbook PDF p.260)."],
  solution="<p>(a) <strong>Yes</strong>. One neighboring ring CH<sub>2</sub> is bonded straight to a carbon of the C=C; the other is bonded to a second CH<sub>2</sub> before the ring reaches the C=C. "
           "Those are different groups, and with the H and the –C(CH<sub>3</sub>)=CH<sub>2</sub> group the carbon has four different groups, so limonene is chiral, like carvone. "
           "It's the textbook's carvone argument (PDF p.258) with the distance to the C=C taking the place of the C=O. "
           "(b) <strong>No rotation</strong>: a racemic mixture is optically inactive (PDF p.260).</p>"
           "<p class='bg'>The orange-peel form is (R)-(+)-limonene.</p>",
  source="Day 10 p.6; " + tb("5.6", 257, 260))

P(id="t5-6-m-explain", module="t5-6", kind="mastery", level="Explain",
  prompt="<p>Using the textbook's mirror-image test, explain why bromochloroiodomethane, CHBrClI, is chiral but bromodiiodomethane, CHBrI<sub>2</sub>, is not.</p>",
  answer={"type": "self", "model": "<p>Reflect each molecule in a mirror, then try to turn the mirror image so that it lands exactly on the original. "
                                   "In CHBrI<sub>2</sub> two of the four groups are the same (I), so after the reflection a turn puts every atom back on an atom of the same element: "
                                   "the mirror image is the same molecule, and the compound is achiral. In CHBrClI all four groups differ. When H, C, and Br are lined up with the original, "
                                   "Cl and I end up in each other's places, and no rotation fixes that. The molecule and its mirror image are different molecules, enantiomers, "
                                   "so CHBrClI is chiral and its carbon is a stereocenter. The textbook makes the same comparison for CHBrClF and CHBr<sub>2</sub>Cl (Fig. 5.40, PDF p.257).</p>"},
  hints=[], solution="", source=tb("5.6", 256, 257))

P(id="t5-6-m-recognize", module="t5-6", kind="mastery", level="Recognize",
  prompt="<p>Which feature is the most common sign that a molecule is chiral?</p>",
  answer=choice(("An sp<sup>3</sup> carbon bonded to four different atoms or groups.", True, "Right: a stereocenter (textbook PDF p.256–257)."),
                ("A carbon–carbon double bond.", False, "A double-bond carbon is sp<sup>2</sup>: it has only three groups, and they lie in a plane."),
                ("A carbon atom in a ring.", False, "Ring carbons can be stereocenters (carvone's is), but a ring carbon with two H atoms isn't."),
                ("A polar bond.", False, "Polarity and chirality are separate questions: CH<sub>2</sub>Cl<sub>2</sub> is polar and achiral.")),
  hints=["What does the textbook call a chiral carbon atom?"],
  solution="<p>A <strong>stereocenter</strong>: an sp<sup>3</sup> carbon bonded to four different atoms or groups of atoms. "
           "“Although several features within molecules can lead to chirality, the most common is the presence of a chiral carbon atom” (textbook PDF p.257).</p>",
  source=tb("5.6", 256, 257))

P(id="t5-6-m-sanity", module="t5-6", kind="mastery", level="Sanity check",
  prompt="<p>A student concludes that a flat molecule in which every carbon atom is sp<sup>2</sup>, such as styrene, C<sub>6</sub>H<sub>5</sub>–CH=CH<sub>2</sub>, is chiral. Why can't that be right?</p>",
  answer=choice(("A planar molecule's mirror image can always be superimposed on it, and it has no sp<sup>3</sup> carbon to be a stereocenter.", NSC["styrene"] == 0,
                 "Right: “Planar molecules cannot be chiral” (textbook PDF p.259)."),
                ("It can be right: any molecule with a C=C double bond is chiral.", False, "Double-bond carbons are sp<sup>2</sup>, with three groups each in a plane: no stereocenter."),
                ("It can be right: only measuring optical rotation can decide chirality.", False, "Measuring rotation is one way to tell, but the structure settles it here (PDF p.256, p.259)."),
                ("It's chiral only if the ring is a benzene ring.", False, "A benzene ring is planar too; it doesn't create chirality.")),
  hints=["Reflect a flat molecule through its own plane. What do you get?"],
  solution="<p>“Planar molecules cannot be chiral because they have superimposable mirror images” (textbook Sample Ex. 5.6, PDF p.259). "
           "Reflecting a flat molecule through its own plane gives back the same molecule, so it can't have a nonsuperimposable mirror image; "
           "and with every carbon sp<sup>2</sup>, there is no carbon with four groups to be a stereocenter.</p>",
  source=tb("5.6", 258, 259))

# =====================================================================================
# t5-7  Molecular orbital theory (lecture: Day 11 p.27, O2's paramagnetism; textbook §5.7, PDF p.261-273)
# =====================================================================================
O2m = SP["O2"]
assert O2m["bo"] == 2 and O2m["unpaired"] == 2 and (O2m["bonding"], O2m["antibonding"]) == (8, 4)
NFm = SP["NF"]
assert (NFm["n"], NFm["bo"], NFm["unpaired"], NFm["bonding"], NFm["antibonding"]) == (12, 2, 2, 8, 4)
assert all((mo("N", "F", 0, order=o)["bo"], mo("N", "F", 0, order=o)["unpaired"]) == (2, 2) for o in (ORDER_LIGHT, ORDER_HEAVY))
P(id="t5-7-attempt", module="t5-7", kind="attempt", level="Guided attempt",
  prompt="<p>Nitrogen monofluoride, NF, is a short-lived molecule. Use the MO order the textbook draws for NO (Fig. 5.52), which is the order Day 12 p.11 uses for O<sub>2</sub> through Ne<sub>2</sub>, from the bottom up: "
         f"{S2}, {S2S}, {S2P}, {P2} (a set of two orbitals), {P2S} (a set of two), {S2PS}. "
         "Fill in NF's valence electrons. (a) What is the bond order? (b) How many electrons are unpaired? (c) Is NF paramagnetic or diamagnetic?</p>",
  answer={"type": "multi", "parts": [
      {"label": "(a) bond order", **num_ans(NFm["bo"], tol=0.01),
       "traps": [{"value": 4, "tol": 0, "message": "Eq. 5.2 has a factor of ½: ½(8 − 4)."},
                 {"value": 3, "tol": 0, "message": f"Count the antibonding electrons too: {S2S} holds 2 and {P2S} holds 2."},
                 {"value": 1, "tol": 0, "message": f"{P2S} gets only NF's last 2 electrons, not 4."}]},
      {"label": "(b) unpaired electrons", **tnum(NFm["unpaired"], traps=[
          (0, f"The two {P2S} orbitals have the same energy. Hund's rule: one electron in each before any pairing (Day 6 p.16)."),
          (1, f"Two electrons go into the {P2S} set, one in each orbital.")])},
      {"label": "(c) magnetism", **choice(("paramagnetic", True, "Right: unpaired electrons make a substance paramagnetic (Day 11 p.27)."),
                                          ("diamagnetic", False, "Diamagnetic means every electron is paired. Check part (b)."))}]},
  hints=["MO theory puts the valence electrons into orbitals that belong to the whole molecule, lowest energy first. Each MO holds at most two electrons, with opposite spins, "
         "and in a set of equal-energy MOs the electrons spread out before they pair, as Day 12 p.11 fills its diagrams (textbook guidelines 4 and 5, PDF p.264).",
         "Bond order = ½[(number of bonding electrons) − (number of antibonding electrons)] (Day 12 p.8; the textbook's Eq. 5.2). The starred orbitals are antibonding.",
         f"N brings 5 valence electrons and F 7: 12 in all, the same count as O<sub>2</sub>. {S2}, {S2S}, {S2P}, and the two {P2} orbitals hold 2 + 2 + 2 + 4 = 10 of them.",
         f"The last 2 go into the two {P2S} orbitals, which have the same energy. Bonding: 2 ({S2}) + 2 ({S2P}) + 4 ({P2}) = 8. Antibonding: 2 ({S2S}) + 2 ({P2S}) = 4."],
  solution=f"<p>NF: {NFm['config']}.</p>"
           f"<p>(a) ½(8 − 4) = <strong>{bo(NFm)}</strong>. (b) <strong>{NFm['unpaired']}</strong>: the two {P2S} electrons occupy separate orbitals with parallel spins (Hund's rule). "
           "(c) <strong>Paramagnetic</strong>: “Only molecules with unpaired electrons are paramagnetic” (Day 11 p.27).</p>"
           "<p>NF has the same 12 valence electrons as O<sub>2</sub>, and the same arrangement of its last two: the pair circled on Day 12 p.11, behind the liquid-oxygen photo on Day 11 p.27. "
           "The five steps can't show it: every Lewis structure they give for NF pairs all 12 electrons.</p>"
           "<p class='bg'>Experiments agree: NF's ground state has two unpaired electrons, like O<sub>2</sub>'s.</p>",
  compare={"wrong": f"<p>“The last two electrons pair up in one {P2S} orbital, so NF has no unpaired electrons and is diamagnetic.”</p>",
           "tempting": "Filling each orbital with two electrons before moving up feels like the aufbau principle, and the Lewis structures of NF pair all 12 electrons, just as O=O pairs O<sub>2</sub>'s (Day 8 p.20).",
           "fails": f"The two {P2S} orbitals are degenerate (equal in energy). Hund's rule, the same rule that leaves carbon's two 2p electrons unpaired (Day 6 p.16), puts one electron in each, with parallel spins. "
                    "So NF has two unpaired electrons, exactly like O<sub>2</sub>, the molecule the Day 11 p.27 slide shows held by a magnet."},
  source=tb("5.7", 263, 268) + "; Day 11 p.27; Day 12 p.8, p.11; Day 6 p.16")

add(id="t5-7-p1", module="t5-7", kind="practice", level="Warm-up",
    prompt="<p>On Day 11 p.27, liquid oxygen poured between the poles of a magnet stays there. What does that tell you about O<sub>2</sub> molecules?</p>",
    answer=choice(("They have unpaired electrons.", True, "Right: “Only molecules with unpaired electrons are paramagnetic” (Day 11 p.27)."),
                  ("They are polar.", False, "The bond joins two identical atoms (Δχ = 0), so O<sub>2</sub> is nonpolar. Polarity is about lining up in an electric field, not a magnetic one."),
                  ("They are ions.", False, "O<sub>2</sub> is a neutral molecule."),
                  ("They contain a triple bond.", False, "O<sub>2</sub> has a double bond (Day 8 p.20), and the number of bonds isn't what a magnet responds to.")),
    hints=["Read the slide's second sentence: which molecules are paramagnetic?"],
    solution="<p>O<sub>2</sub> is <strong>paramagnetic</strong>, “attracted to a magnetic field,” and “Only molecules with unpaired electrons are paramagnetic” (Day 11 p.27, repeated on Day 12 p.6). "
             "So some of O<sub>2</sub>'s electrons must be unpaired: Day 12 p.11 finds two, in the π*<sub>2p</sub> orbitals. The photo is the textbook's Fig. 5.51 (PDF p.267).</p>",
    source="Day 11 p.27; Day 12 p.6, p.11; " + tb("5.7", 266, 267))

HeHm, H2dm = SP["HeH+"], SP["H2-2"]
assert (HeHm["n"], HeHm["bo"], H2dm["n"], H2dm["bo"]) == (2, 1, 4, 0)
H2X_BO = (1 - 1) / 2                       # excited H2: one electron in σ1s, one in σ*1s
add(id="t5-7-p2", module="t5-7", kind="practice", level="Warm-up",
  prompt=f"<p>These species use only the {S1} and {S1S} molecular orbitals, the two MOs Day 12 p.8–9 fills for H<sub>2</sub>, H<sub>2</sub><sup>−</sup>, and He<sub>2</sub>. Find the bond order of (a) the helium hydride ion, HeH<sup>+</sup>; (b) H<sub>2</sub><sup>2−</sup>; "
         f"and (c) an H<sub>2</sub> molecule that has absorbed a photon, which moved one of its electrons from {S1} up to {S1S}. Enter numbers.</p>",
  answer={"type": "multi", "parts": [
      {"label": "(a) HeH<sup>+</sup>", **num_ans(HeHm["bo"], tol=0.01),
       "traps": [{"value": 2, "tol": 0, "message": f"Its 2 electrons make one pair in {S1}: ½(2 − 0)."},
                 {"value": 0, "tol": 0, "message": f"HeH<sup>+</sup> has 2 electrons (He 2 + H 1 − 1 for the charge), and both fit in {S1}."}]},
      {"label": "(b) H<sub>2</sub><sup>2−</sup>", **num_ans(H2dm["bo"], tol=0.01),
       "traps": [{"value": 1, "tol": 0, "message": f"H<sub>2</sub><sup>2−</sup> has 4 electrons, so {S1S} fills too, and its pair cancels the bonding pair."},
                 {"value": 2, "tol": 0, "message": "Count the antibonding pair as well: ½(2 − 2)."}]},
      {"label": "(c) H<sub>2</sub> after the photon", **num_ans(H2X_BO, tol=0.01),
       "traps": [{"value": 1, "tol": 0, "message": f"That's H<sub>2</sub> before the photon. One electron is now in {S1S}: ½(1 − 1)."},
                 {"value": 0.5, "tol": 0, "message": "Both electrons count: one bonding, one antibonding."}]}]},
  hints=["Count the electrons first: He brings 2 and H 1; a 1+ charge removes one, and a 2− charge adds two.",
         f"Fill {S1} (at most 2) before {S1S}, except in (c), where the photon has already moved one electron up. Bond order = ½(bonding − antibonding) (Day 12 p.8)."],
  solution=f"<p>(a) HeH<sup>+</sup>: 2 electrons, {HeHm['config']}, ½(2 − 0) = <strong>{bo(HeHm)}</strong>, a real bond, like H<sub>2</sub>'s (Day 12 p.8). "
           f"(b) H<sub>2</sub><sup>2−</sup>: 4 electrons, {H2dm['config']}, ½(2 − 2) = <strong>{bo(H2dm)}</strong>: no net bond, like He<sub>2</sub> (Day 12 p.9). "
           f"(c) ({S1})<sup>1</sup>({S1S})<sup>1</sup>: ½(1 − 1) = <strong>0</strong>. In this excited state MO theory predicts no net bond.</p>"
           f"<p class='connection'>The photon in (c) lifts an electron from H<sub>2</sub>'s HOMO ({S1}) to its LUMO ({S1S}), the two orbitals Day 12 p.11 defines. "
           "Moving an electron into an antibonding MO weakens a bond; the textbook uses the same idea for excited molecules in the aurora (PDF p.269–270).</p>",
  source="Day 12 p.8–9, p.11; " + tb("5.7", 261, 270))

O2L = LW.STRUCTS["O2"]
assert O2L.total_valence() == 12 and not O2L.rad
add(id="t5-7-p3", module="t5-7", kind="practice", level="Concept",
    prompt=f"<p>The lecture's Lewis structure of O<sub>2</sub> (Day 8 p.20) is</p><p>{LS('O2')}</p><p>How many unpaired electrons does it show?</p>",
    answer=tnum(sum(O2L.rad.values()), traps=[(4, "Those are the lone pairs. A lone pair is two paired electrons; count electrons that have no partner."),
                                             (2, "Look again: every dot belongs to a pair, and each bond line is a shared pair.")]),
    hints=["Each bond line is a shared pair, and the dots come in lone pairs.",
           f"{O2L.total_valence()} valence electrons = 2 shared pairs + 4 lone pairs. Is any electron left over?"],
    solution="<p><strong>0</strong>: two shared pairs and four lone pairs account for all 12 valence electrons, each one in a pair. "
             "A substance made of such molecules would be diamagnetic, yet O<sub>2</sub> sticks to a magnet. That's the contradiction on Day 11 p.27: "
             "“Lewis structures, VSEPR, and valence bond/hybridization theories ALL fail to predict this.” "
             "With the octet rule, the double bond pairs every electron; a structure with two unpaired electrons would leave each O with only 7. "
             "MO theory finds two unpaired electrons and still a bond order of 2 (Day 12 p.11).</p>",
    source="Day 8 p.20; Day 11 p.27; Day 12 p.11")

BO_ROWS = ["Li2-2", "Be2+2", "F2+2", "Ne2+2", "BN-"]
P(id="t5-7-p4", module="t5-7", kind="practice", level="Standard",
  prompt=f"<p>Fill the valence MO diagram of each species and match it with its bond order. Use {P2} below {S2P} for Li<sub>2</sub> through N<sub>2</sub> and their ions; "
         f"use {S2P} below {P2} for O<sub>2</sub> through Ne<sub>2</sub> and their ions, and, as the textbook draws NO, for the molecule made of two different atoms.</p>",
  answer={"type": "match", "rows": [{"html": SPH[x], "answer": f"bo{bo(SP[x])}"} for x in BO_ROWS],
          "options": [{"key": f"bo{v}", "html": v} for v in ("0", "0.5", "1", "1.5", "2", "2.5", "3")]},
  hints=["Count valence electrons, then adjust for the charge: Li 1, Be 2, B 3, N 5, F 7, Ne 8 per atom; a 2− charge adds two electrons, a 2+ charge removes two, and a 1− charge adds one.",
         "Bond order = ½(bonding − antibonding) (Day 12 p.8). Species with the same number of valence electrons have the same bond order: F<sub>2</sub><sup>2+</sup> has 12, like O<sub>2</sub>."],
  solution=mo_table(BO_ROWS)
           + "<p>Shortcuts by electron count: Ne<sub>2</sub><sup>2+</sup> has F<sub>2</sub>'s 14 electrons and its bond order; Li<sub>2</sub><sup>2−</sup> has Be<sub>2</sub>'s 4 and, like Be<sub>2</sub>, no net bond (Day 12 p.11).</p>",
  source="Day 12 p.8, p.11; " + tb("5.7", 264, 268))

MAG_ROWS = ["BF", "CO-", "He2+2", "OF"]
P(id="t5-7-p5", module="t5-7", kind="practice", level="Standard",
  prompt=f"<p>Classify each species as paramagnetic or diamagnetic. For the molecules made of two different atoms, use {S2P} below {P2}, the order the textbook draws for NO.</p>",
  answer={"type": "match", "rows": [{"html": SPH[x], "answer": "para" if SP[x]["unpaired"] else "dia"} for x in MAG_ROWS],
          "options": [{"key": "dia", "html": "diamagnetic"}, {"key": "para", "html": "paramagnetic"}]},
  hints=["Paramagnetic means at least one unpaired electron (Day 11 p.27).",
         f"Count the electrons, fill, and look at the highest occupied level: a single electron in a σ orbital, or 1 or 3 electrons in a pair of π orbitals, leaves one unpaired."],
  solution="<ul>" + "".join(f"<li>{SPH[x]}: {SP[x]['n']} electrons, {SP[x]['config']}, {SP[x]['unpaired']} unpaired → <strong>{'paramagnetic' if SP[x]['unpaired'] else 'diamagnetic'}</strong></li>" for x in MAG_ROWS) + "</ul>"
           "<p>Here the odd-electron species are the paramagnetic ones. An even count doesn't guarantee pairing, though: O<sub>2</sub>, with 12, is paramagnetic (Day 11 p.27).</p>",
  source=tb("5.7", 266, 268) + "; Day 11 p.27")

CHG = [("NF", "NF+"), ("BF", "BF-"), ("Ne2+2", "Ne2"), ("Be2+2", "Be2")]
assert [a for a, b in CHG if SP[b]["bo"] > SP[a]["bo"]] == ["NF"]


def _chg(a, b):
    return f"{bo(SP[a])} → {bo(SP[b])}"


P(id="t5-7-p6", module="t5-7", kind="practice", level="Standard",
  prompt="<p>Adding or removing electrons can raise or lower a bond order. Which change <em>raises</em> it?</p>",
  answer=choice((f"{SPH['NF']} → {SPH['NF+']}", True, f"Right: the electron leaves {P2S}, an antibonding orbital: {_chg('NF', 'NF+')}."),
                (f"{SPH['BF']} → {SPH['BF-']}", False, f"The added electron goes into {P2S}, an antibonding orbital: {_chg('BF', 'BF-')}."),
                (f"{SPH['Ne2+2']} → {SPH['Ne2']}", False, f"The two added electrons go into {S2PS}, which is antibonding: {_chg('Ne2+2', 'Ne2')}."),
                (f"{SPH['Be2+2']} → {SPH['Be2']}", False, f"The two added electrons go into {S2S}, which is antibonding: {_chg('Be2+2', 'Be2')}.")),
  hints=["A removed electron comes out of the highest occupied MO; an added one goes into the lowest MO with room.",
         "Losing an antibonding electron, or gaining a bonding one, raises the bond order."],
  solution=f"<p><strong>NF → NF<sup>+</sup></strong>: NF's highest electrons are in {P2S}, so ionizing it removes antibonding density and the bond order rises from 2 to 2.5. "
           f"In the other three changes the new electrons go into antibonding orbitals ({P2S}, {S2PS}, {S2S}), so the bond order falls. "
           "The textbook reasons the same way about ions in Sample Ex. 5.8 (PDF p.267).</p>",
  source=tb("5.7", 267, 268))

CFm, CFpm = SP["CF"], SP["CF+"]
assert (CFm["n"], CFm["bo"], CFm["unpaired"], CFpm["bo"]) == (11, 2.5, 1, 3)
P(id="t5-7-p7", module="t5-7", kind="practice", level="Standard",
  prompt=f"<p>Carbon monofluoride, CF, is a reactive molecule with 11 valence electrons, the same count as NO. Using the order {S2}, {S2S}, {S2P}, {P2}, {P2S}, {S2PS}, find "
         "(a) the bond order of CF and (b) the bond order of the CF<sup>+</sup> ion. Enter numbers. (c) Is CF paramagnetic or diamagnetic?</p>",
  answer={"type": "multi", "parts": [
      {"label": "(a) CF", **num_ans(CFm["bo"], tol=0.01),
       "traps": [{"value": 3, "tol": 0, "message": f"That's CF<sup>+</sup>. CF still has one electron in {P2S}."},
                 {"value": 2, "tol": 0, "message": "Count again: 8 bonding electrons and 3 antibonding (2 in σ*<sub>2s</sub>, 1 in π*<sub>2p</sub>)."}]},
      {"label": "(b) CF<sup>+</sup>", **num_ans(CFpm["bo"], tol=0.01),
       "traps": [{"value": 2, "tol": 0, "message": f"CF<sup>+</sup> loses CF's {P2S} electron, an antibonding one, so the bond order goes up, not down."},
                 {"value": 2.5, "tol": 0, "message": "That's CF itself. Remove one electron first."}]},
      {"label": "(c) CF", **choice(("paramagnetic", True, "Right: one unpaired electron."), ("diamagnetic", False, "With 11 electrons, at least one must be unpaired."))}]},
  hints=[f"C 4 + F 7 = 11 electrons. {S2}, {S2S}, {S2P}, and {P2} take 10; the 11th goes into {P2S}.",
         "CF<sup>+</sup> has one electron fewer. Which orbital loses it, and is that orbital bonding or antibonding?"],
  solution=f"<p>CF: {CFm['config']}. (a) ½(8 − 3) = <strong>{bo(CFm)}</strong>. "
           f"(b) CF<sup>+</sup>: {CFpm['config']}, ½(8 − 2) = <strong>{bo(CFpm)}</strong>. "
           "(c) <strong>Paramagnetic</strong>: one unpaired electron, so CF is a free radical, as its odd electron count already tells you (Day 9 p.28).</p>"
           "<p>It's the same pattern the textbook works out for NO and NO<sup>+</sup> (Fig. 5.52 and Sample Ex. 5.9, PDF p.268–269): with 11 electrons the last one sits in π*<sub>2p</sub>, and removing it raises the bond order to 3.</p>",
  source=tb("5.7", 268, 269) + "; Day 9 p.28")

OFAM = [("ofp", "OF+"), ("of", "OF"), ("ofm", "OF-")]
assert [SP[x]["bo"] for _, x in OFAM] == [2, 1.5, 1]
P(id="t5-7-p8", module="t5-7", kind="practice", level="Stretch",
  prompt="<p>Rank these species by O–F bond length.</p>",
  answer=order_ans([(k, SPH[x]) for k, x in OFAM], [k for k, x in sorted(OFAM, key=lambda t: SP[t[1]]["bo"])], "longest (1) to shortest (3)"),
  hints=[f"OF has 6 + 7 = 13 valence electrons, so {P2S} holds 3. An added electron goes into {P2S}; a removed one comes out of it.",
         f"Each {P2S} electron changes the bond order by ½. Higher bond order → shorter bond (Table 4.6, Day 9 p.14)."],
  solution="<ul>" + "".join(f"<li>{SPH[x]}: {SP[x]['n']} valence electrons, {SP[x]['config']}, bond order <strong>{bo(SP[x])}</strong></li>" for _, x in OFAM) + "</ul>"
           "<p>Longest to shortest: OF<sup>−</sup> &gt; OF &gt; OF<sup>+</sup>. All three differ only in the number of π*<sub>2p</sub> electrons, so the bond order, and with it the bond length, "
           "tracks that number (higher bond order, shorter bond: Day 9 p.7, p.14).</p>",
  source=tb("5.7", 265, 268) + "; Day 9 p.7, p.14")

BE_L, BE_H = mo("Be", "Be", -2, order=ORDER_LIGHT), mo("Be", "Be", -2, order=ORDER_HEAVY)
assert (BE_L["unpaired"], BE_H["unpaired"], BE_L["bo"], BE_H["bo"]) == (2, 0, 1, 1)
SAME = [x for x in ("CO-", "Ne2+2", "He2+2") if mo(*SPECIES[x], order=ORDER_LIGHT if x != "He2+2" else None)["unpaired"]
        == mo(*SPECIES[x], order=ORDER_HEAVY if x != "He2+2" else None)["unpaired"]]
assert SAME == ["CO-", "Ne2+2", "He2+2"]
add(id="t5-7-p9", module="t5-7", kind="practice", level="Stretch",
  prompt=f"<p>Day 12 p.11 uses two energy orders: {P2} below {S2P} (Li<sub>2</sub> through N<sub>2</sub>) and {S2P} below {P2} (O<sub>2</sub> through Ne<sub>2</sub>). "
         "For which species would switching between the two orders change the predicted magnetism?</p>",
  answer=choice((SPH["Be2-2"], True, f"Right: its 6 valence electrons leave 2 for the 2p bonding MOs. With {P2} lower they take one {P2} orbital each (paramagnetic); with {S2P} lower they pair in {S2P} (diamagnetic)."),
                (SPH["CO-"], False, f"11 electrons: every bonding MO fills in either order, and the 11th sits alone in {P2S}. Paramagnetic both ways."),
                (SPH["Ne2+2"], False, f"14 electrons fill everything except {S2PS} in either order: diamagnetic both ways."),
                (SPH["He2+2"], False, f"Its 2 electrons sit in {S1}; the 2p MOs aren't involved.")),
  hints=[f"The two orders differ only in which bonding level, {S2P} or the {P2} pair, fills first. Count how many electrons reach those levels.",
         "The order matters only when those levels hold exactly 2 or 4 electrons: then it decides whether the electrons pair."],
  solution=f"<p><strong>Be<sub>2</sub><sup>2−</sup></strong>. With {P2} lower: {BE_L['config']}, 2 unpaired, paramagnetic. With {S2P} lower: {BE_H['config']}, diamagnetic. "
           "The bond order is 1 either way; only the magnetism changes. That's why magnetic measurements can test which order applies. "
           f"Day 12 p.11 puts {P2} below {S2P} for Li<sub>2</sub> through N<sub>2</sub>, and the textbook gives the reason, 2s–2p mixing that raises {S2P} for Z ≤ 7 (PDF p.265–266). "
           "Filled with Be<sub>2</sub>'s order, as the textbook fills ions with their parent molecule's order (Sample Ex. 5.8, PDF p.267), Be<sub>2</sub><sup>2−</sup> would be predicted paramagnetic.</p>",
  source="Day 12 p.11; Day 11 p.27; " + tb("5.7", 265, 267))

# the 3-center π system of an 18-electron, ozone-like species (Figs. 5.54-5.55): two σ bonds and five lone pairs first,
# then π (bonding), n (nonbonding), π* (antibonding)
NO2m = LW.STRUCTS["NO2-1"]
assert NO2m.total_valence() == 18
PI3_FRAME = 2 * 2 + 5 * 2
PI3_E = NO2m.total_valence() - PI3_FRAME
_pi = [min(2, max(0, PI3_E - 2 * i)) for i in range(3)]          # electrons in π, n, π*
PI3_BO = (_pi[0] - _pi[2]) / 2
PI3_AVG = (2 + PI3_BO) / 2
PI3_LP_END = 2 + _pi[1] / 2 / 2                                    # framework pairs + half of the n pair
assert (PI3_E, _pi, PI3_AVG, PI3_LP_END) == (4, [2, 2, 0], 1.5, 2.5)
HYB_NO2 = LW.hybrid_svg([LW.STRUCTS["NO2-1"], LW.STRUCTS["NO2-2"]], tag="span", scale=0.8)
P(id="t5-7-p10", module="t5-7", kind="practice", level="Stretch",
  prompt="<p>Apply the textbook's MO picture of ozone to the nitrite ion, NO<sub>2</sub><sup>−</sup>, which has the same 18 valence electrons. "
         "Start from two N–O σ bonds and five lone pairs (one on N, two on each O): 14 electrons. The other 4 go into three MOs made from one p orbital on each atom: "
         "a bonding π, a nonbonding n, and an antibonding π*. (a) What is the average N–O bond order? (b) The nonbonding n pair is spread over the two O atoms, as the textbook finds for ozone's end atoms. "
         "On average, how many lone pairs does each O carry? Enter numbers.</p>",
  answer={"type": "multi", "parts": [
      {"label": "(a) average N–O bond order", **num_ans(PI3_AVG, tol=0.01),
       "traps": [{"value": 2, "tol": 0, "message": "That's the double bond in one resonance structure. The one π bond is spread over both N–O bonds."},
                 {"value": 3, "tol": 0, "message": "3 is the total, 2 σ + 1 π, shared by two N–O bonds."}]},
      {"label": "(b) lone pairs on each O", **num_ans(PI3_LP_END, tol=0.01),
       "traps": [{"value": 3, "tol": 0, "message": "That's the single-bonded O in one resonance structure. The nonbonding pair is shared by both O atoms."},
                 {"value": 2, "tol": 0, "message": "Add each O's share of the nonbonding pair, which is spread over the two O atoms."}]}]},
  hints=["Fill π, n, π* from the bottom with 4 electrons: π<sup>2</sup> n<sup>2</sup> π*<sup>0</sup>. Only π and π* change the bond order: ½(2 − 0) = 1 π bond, spread over the whole ion.",
         "Average bond order = (2 σ + 1 π) ÷ 2 N–O bonds. For (b): each O has 2 lone pairs in the framework, plus a share of the nonbonding pair, which sits on the two O atoms."],
  solution="<p>(a) (2 + 1)/2 = <strong>1.5</strong>, the value resonance gives for nitrite's two equivalent bonds (<a href='#t4-5'>§4.5</a>). "
           "(b) 2 + ½ = <strong>2.5</strong>: the nonbonding pair is shared by the two O atoms, just as the textbook finds for ozone (PDF p.270–271).</p>"
           f"<p class='lw-row'>{HYB_NO2}</p>"
           "<p class='connection'>The professor's resonance hybrid of ozone shows the same averaging: a solid line plus a dashed partial bond on each side, and five dots, 2.5 lone pairs, on each end O (Day 9 p.10). "
           "MO theory reaches that picture without drawing resonance structures.</p>",
  source=tb("5.7", 270, 271) + "; Day 9 p.7–10; Day 8 p.8")

CNm = SP["CN-"]
assert (CNm["n"], CNm["bo"], CNm["unpaired"]) == (10, 3, 0)
assert all((mo("C", "N", -1, order=o)["bo"], mo("C", "N", -1, order=o)["unpaired"]) == (3, 0) for o in (ORDER_LIGHT, ORDER_HEAVY))
ISO = [x for x in ("N2", "O2", "NO", "C2") if (SP[x]["n"], SP[x]["bo"]) == (CNm["n"], CNm["bo"])]
assert ISO == ["N2"]
P(id="t5-7-transfer", module="t5-7", kind="transfer", level="Transfer",
  prompt="<p>The cyanide ion, CN<sup>−</sup>, is a heteronuclear diatomic like NO. (a) How many valence electrons go into its molecular orbitals? (b) What is its bond order? "
         "(c) Is it paramagnetic or diamagnetic? (d) Which neutral molecule has the same number of valence electrons and the same bond order?</p>",
  answer={"type": "multi", "parts": [
      {"label": "(a) valence electrons", **tnum(CNm["n"], traps=[(9, "The 1− charge adds an electron: 4 + 5 + 1."), (8, "A negative charge adds electrons; it doesn't remove them.")])},
      {"label": "(b) bond order", **num_ans(CNm["bo"], tol=0.01),
       "traps": [{"value": 2.5, "tol": 0, "message": f"That's NO, with 11 electrons. CN<sup>−</sup> has 10, so none reaches {P2S}."},
                 {"value": 2, "tol": 0, "message": f"Count again: 8 bonding electrons ({S2}, {S2P}, two {P2}) and 2 antibonding ({S2S})."}]},
      {"label": "(c) magnetism", **choice(("paramagnetic", False, "With 10 electrons, every occupied MO is full: no unpaired electrons."), ("diamagnetic", True, "Right: every occupied orbital is full."))},
      {"label": "(d) same count and bond order", **choice(("N<sub>2</sub>", True, "Right: 10 valence electrons and bond order 3."),
                                                         ("O<sub>2</sub>", False, f"O<sub>2</sub> has 12 valence electrons and bond order {bo(SP['O2'])}."),
                                                         ("NO", False, f"NO has 11 valence electrons and bond order {bo(SP['NO'])}."),
                                                         ("C<sub>2</sub>", False, f"C<sub>2</sub> has 8 valence electrons and bond order {bo(SP['C2'])}."))}]},
  hints=["C brings 4 valence electrons and N 5, and the 1− charge adds one more.",
         f"Ten electrons fill {S2}, {S2S}, {S2P}, and both {P2} orbitals, and none reaches {P2S}. With 10 electrons, either energy order fills the same orbitals."],
  solution=f"<p>(a) 4 + 5 + 1 = <strong>{CNm['n']}</strong>. (b) {CNm['config']}: ½(8 − 2) = <strong>{bo(CNm)}</strong>. (c) <strong>Diamagnetic</strong>: every occupied orbital is full. "
           "(d) <strong>N<sub>2</sub></strong> (Day 12 p.11). CN<sup>−</sup>, N<sub>2</sub>, CO, and NO<sup>+</sup> all have 10 valence electrons and bond order 3; the textbook compares NO<sup>+</sup> with N<sub>2</sub> the same way (Sample Ex. 5.9, PDF p.269).</p>"
           f"<p>The Lewis structure agrees: {LS('CN-', scale=0.8)} a triple bond, with every electron paired.</p>",
  source="Day 12 p.8, p.11; " + tb("5.7", 265, 269))

add(id="t5-7-m-explain", module="t5-7", kind="mastery", level="Explain",
  prompt="<p>Explain why liquid oxygen is attracted to a magnet (Day 11 p.27), why the Lewis structure O=O can't account for it, and how MO theory does (Day 12 p.11).</p>",
  answer={"type": "self", "model": "<p>Only substances whose molecules have unpaired electrons are attracted into a magnetic field: they're paramagnetic. "
                                   "The Lewis structure of O<sub>2</sub> puts all 12 valence electrons in pairs (two bonding pairs and four lone pairs), so it predicts no unpaired electrons, "
                                   "and VSEPR and valence bond theory, which start from it, can't do better (Day 11 p.27). In MO theory the electrons fill orbitals that belong to the whole molecule: "
                                   f"{O2m['config']}. The last two electrons enter two equal-energy {P2S} orbitals one at a time (Hund's rule), leaving two unpaired electrons, "
                                   "while the bond order, ½(8 − 4) = 2, still matches the double bond (Day 12 p.11; textbook PDF p.265–266).</p>"},
  hints=[], solution="", source="Day 11 p.27; Day 12 p.6, p.11; Day 8 p.20; " + tb("5.7", 265, 266))

add(id="t5-7-m-recognize", module="t5-7", kind="mastery", level="Recognize",
    prompt="<p>Which question calls for molecular orbital theory rather than a Lewis structure, VSEPR, or hybridization?</p>",
    answer=choice(("Is O<sub>2</sub> attracted to a magnet?", True, "Right: the slide's example of what the other models “ALL fail to predict” (Day 11 p.27)."),
                  ("What is the shape of a water molecule?", False, "VSEPR answers that: SN 4 with two lone pairs gives a bent molecule (Day 10 p.19)."),
                  ("How many bonds does a carbon atom usually form?", False, "The Lewis symbol's bonding capacity answers that (Day 8 p.18)."),
                  ("Which orbitals overlap to form the C–H bonds in CH<sub>4</sub>?", False, "Valence bond theory answers that: carbon's sp<sup>3</sup> hybrids overlap the H 1s orbitals (Day 11 p.13–15).")),
    hints=["Which property did Day 11 p.27 say the other models fail to predict?"],
    solution="<p><strong>Magnetism</strong>, which depends on unpaired electrons (Day 11 p.27). Day 12 p.13 sorts the models by the question asked: connectivity, “Lewis structures are fine”; "
             "3-D shape, “VSEPR or VBT should work”; “magnetic or spectroscopic properties,” “We're going to need to use MO.” "
             "The textbook's summary is the same, with MO theory as “our most powerful model” (PDF p.273).</p>",
    source="Day 11 p.27; Day 12 p.13; Day 10 p.19; Day 8 p.18; Day 11 p.13–15; " + tb("5.7", 273))

H2m = mo("H", "H", -1)                      # H2- (Day 12 p.9): an anion with an ordinary bond order
assert H2m["bo"] == 0.5
add(id="t5-7-m-sanity", module="t5-7", kind="mastery", level="Sanity check",
  prompt="<p>A classmate fills an MO diagram and gets a bond order of −0.5 for a diatomic species. What does that tell you?</p>",
  answer=choice(("There's a mistake: filling from the bottom up puts electrons into each bonding orbital before its antibonding partner, so a bond order can't be negative.", True,
                 "Right: recheck the energy order and redo the filling."),
                ("The species exists, but its bond is very weak.", False, "A bond order of 0 already means no net bonding (He<sub>2</sub>, Day 12 p.9). A negative value isn't a weaker bond; it signals an error."),
                ("The species must be an anion.", False, f"Anions have ordinary bond orders: H<sub>2</sub><sup>−</sup> on Day 12 p.9 has {bo(H2m)}. The sign of a charge isn't the sign of a bond order."),
                ("The two atoms are held together by an ionic bond instead.", False, "Bond order says nothing about ionic character; this value signals a filling error.")),
  hints=[f"When you fill from the bottom up, which fills first: {S2} or {S2S}? {P2} or {P2S}?"],
  solution="<p>In every MO diagram on Day 12 p.8–11, each antibonding MO lies above its bonding partner, in both energy orders. Filling from the bottom up therefore gives a ground-state molecule "
           "at least as many bonding as antibonding electrons, and the smallest possible bond order is 0, for molecules that don't exist (He<sub>2</sub>, Be<sub>2</sub>, Ne<sub>2</sub>; Day 12 p.9, p.11; "
           "the textbook says the same of He<sub>2</sub>, PDF p.262). "
           "A negative result means antibonding orbitals were filled before their bonding partners: recheck the energy order and redo the filling.</p>",
  source="Day 12 p.8–11; " + tb("5.7", 262, 266))


# ---------------------------------------------------------------- answer positions
# Like the Ch. 4 banks (choice_order.spread), the items above were written with the correct option first. Rotate each
# choice so the correct options are spread evenly over the positions: specs with n options are ordered by an MD5 hash of
# problem id + part path, and the k-th gets its correct option at position k mod n (stable across builds; distractors
# keep their relative order). Items whose options have a natural order (yes/no, paramagnetic/diamagnetic) are kept.
KEEP_K = {("t5-6-attempt", ".1"), ("t5-7-attempt", ".2"), ("t5-7-p7", ".2"), ("t5-7-transfer", ".2")}


def _spread(problems, keep=KEEP_K):
    specs = [(p["id"], path, spec) for p in problems for path, spec in choice_order.walk(p["answer"]) if (p["id"], path) not in keep]
    by_n = {}
    for pid, path, spec in specs:
        by_n.setdefault(len(spec["options"]), []).append((hashlib.md5((pid + path).encode()).hexdigest(), spec))
    for n, group in by_n.items():
        for rank, (_, spec) in enumerate(sorted(group, key=lambda t: t[0])):
            opts = spec["options"]
            k = next(i for i, o in enumerate(opts) if o["correct"])
            target = rank % n
            r = (k - target) % n
            spec["options"] = [opts[(i + r) % n] for i in range(n)]
            assert spec["options"][target]["correct"]


_spread(PROBLEMS[K_START:])

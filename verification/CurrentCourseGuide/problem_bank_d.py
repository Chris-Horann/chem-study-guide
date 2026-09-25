"""Problem bank D: Chapter 2 TEXTBOOK-PREVIEW modules (t2-2 … t2-6) and the preview item in m2."""
import math
from guide_common import *
from problem_bank_a import PROBLEMS, add, num_ans, choice, G_UNITS
from problem_bank_b import text_ans, formula_ans, order_ans
from problem_bank_c import P, tb

MOL_UNITS = ["mol", "mole", "moles"]
GMOL_UNITS = ["g/mol", "g mol^-1", "g mol-1", "g·mol^-1", "g/mole", "g mol⁻¹", "g·mol⁻¹"]
U_UNITS = ["u", "amu", "da", "dalton", "daltons"]
PCT_UNITS = ["%", "percent"]

def sym_ans(sym, name):
    return {"type": "text", "accepted": [sym, name, name.capitalize()], "caseInsensitive": False, "kind": "text", "placeholder": "symbol"}

# =====================================================================================
# m2 preview item: radioactivity (§2.1 Radioactivity, TB PDF p.84–85)
# =====================================================================================
P(id="m2-preview-radioactivity", module="m2", kind="practice", level="Textbook preview",
  prompt="<p>Which description of α and β particles matches the textbook's Radioactivity subsection?</p>",
  answer=choice(("α particles are high-energy electrons; β particles are helium nuclei.", False, "Swapped."),
                ("β particles are high-energy electrons (1−); α particles are helium-4 nuclei (2+), and the two bend in opposite directions in a magnetic field.", True, "Right (textbook §2.1)."),
                ("Both are neutral, so neither bends in a magnetic field.", False, "Both are charged; Rutherford deflected both with magnets."),
                ("α and β particles have the same mass.", False, "The α particle is far more massive.")),
  hints=["Rutherford matched the β particle's mass-to-charge ratio to Thomson's electron.", "The gold-foil experiment (Day 2 p.15) fired positively charged α particles."],
  solution="<p>β = high-energy electron; α = <sup>4</sup>He nucleus, charge 2+. They deflect in opposite directions. <span class='note'>The textbook says α particles are “about 10,000 times more massive” than β particles; the actual ratio is about 7.29 × 10<sup>3</sup> (an order-of-magnitude statement).</span></p>",
  source=tb("2.1", 84, 85) + "; Day 2 p.15")

# =====================================================================================
# t2-2 Nuclides and their symbols (§2.2, TB PDF p.87–90); isotopes/particle table = LECTURE (RAMP UP)
# =====================================================================================
P(id="t2-2-attempt", module="t2-2", kind="attempt", level="Guided attempt",
  prompt="<p>How many protons, neutrons, and electrons are in the ion <sup>56</sup>Fe<sup>3+</sup>? (Fe: Z = 26.)</p>",
  answer={"type": "multi", "parts": [
      {"label": "protons", **num_ans(26, tol=0)}, {"label": "neutrons", **num_ans(30, tol=0)}, {"label": "electrons", **num_ans(23, tol=0)}]},
  hints=["In <sup>A</sup>X<sup>Q</sup>, the superscript before the symbol is the mass number A; the one after is the charge Q (textbook §2.2).",
         "Protons = Z, which the element's identity fixes.",
         "Neutrons = A − Z.",
         "Electrons = Z − Q: a 3+ ion has 3 fewer electrons than protons."],
  solution="<p>Protons = Z = <strong>26</strong>; neutrons = 56 − 26 = <strong>30</strong>; electrons = 26 − 3 = <strong>23</strong>. "
           "The charge comes from missing electrons, not extra protons: the nucleus is unchanged.</p>",
  compare={"wrong": "<p>“Electrons = 26 + 3 = 29, and neutrons = 56.”</p>",
           "tempting": "“3+” looks like “add 3,” and 56 is the only other number in the symbol.",
           "fails": "A positive charge means electrons were <em>lost</em>: 26 − 3 = 23. A counts protons plus neutrons, so neutrons = A − Z = 30 (the isotope idea from the RAMP UP slide, Day 2 p.23)."},
  source=tb("2.2", 87, 88) + "; Day 2 p.22–23")

P(id="t2-2-p1", module="t2-2", kind="practice", level="Warm-up",
  prompt="<p>Write the nuclide symbol for an atom with 17 protons and 20 neutrons, in the form <sup>A</sup>X (for example, type 37Cl or Cl-37).</p>",
  answer={"type": "text", "accepted": ["37Cl", "³⁷Cl", "Cl-37", "chlorine-37", "Chlorine-37"], "caseInsensitive": False, "kind": "text", "placeholder": "e.g., 12C"},
  hints=["Z = 17 identifies the element.", "A = protons + neutrons."],
  solution="<p>Z = 17 is chlorine; A = 17 + 20 = 37 → <strong><sup>37</sup>Cl</strong> (chlorine-37), or <sup>37</sup><sub>17</sub>Cl with Z shown.</p>",
  source=tb("2.2", 87, 88))

P(id="t2-2-p2", module="t2-2", kind="practice", level="Warm-up",
  prompt="<p>Which pair are isotopes of each other?</p>",
  answer=choice(("<sup>12</sup>C and <sup>13</sup>C", True, "Right: same Z (6), different numbers of neutrons."),
                ("<sup>14</sup>C and <sup>14</sup>N", False, "Same A, but different Z: different elements."),
                ("<sup>16</sup>O and <sup>16</sup>O<sup>2−</sup>", False, "Same nuclide; one is an ion."),
                ("<sup>1</sup>H and <sup>4</sup>He", False, "Different elements.")),
  hints=["Isotopes: same element (same Z), different A."],
  solution="<p><strong><sup>12</sup>C and <sup>13</sup>C</strong>: both have 6 protons, with 6 and 7 neutrons (the RAMP UP slide's example, Day 2 p.23).</p>",
  source=tb("2.2", 87) + "; Day 2 p.23")

P(id="t2-2-p3", module="t2-2", kind="practice", level="Standard",
  prompt="<p>How many electrons are in <sup>80</sup>Se<sup>2−</sup>? (Se: Z = 34.)</p>",
  answer=num_ans(36, tol=0),
  hints=["Electrons = Z − Q.", "Q = −2, so the ion has 2 more electrons than protons."],
  solution="<p>34 − (−2) = <strong>36</strong> electrons, the same number as krypton.</p>",
  source=tb("2.2", 88))

P(id="t2-2-p4", module="t2-2", kind="practice", level="Standard",
  prompt="<p>A particle has 20 protons, 20 neutrons, and 18 electrons. Which symbol describes it?</p>",
  answer=choice(("<sup>40</sup>Ca<sup>2+</sup>", True, "Right: Z = 20 (Ca), A = 40, charge 20 − 18 = +2."), ("<sup>40</sup>Ar", False, "Argon has Z = 18; protons, not electrons, identify the element."),
                ("<sup>40</sup>Ca<sup>2−</sup>", False, "Fewer electrons than protons means a positive charge."), ("<sup>20</sup>Ca<sup>2+</sup>", False, "A counts protons and neutrons: 40.")),
  hints=["Protons fix the element; A = p + n; Q = p − e."],
  solution="<p>Z = 20 → Ca; A = 40; Q = 20 − 18 = +2 → <strong><sup>40</sup>Ca<sup>2+</sup></strong>.</p>",
  source=tb("2.2", 88, 90))

P(id="t2-2-p5", module="t2-2", kind="practice", level="Standard",
  prompt="<p>In the particle symbol <sup>0</sup><sub>−1</sub>e for an electron, what does the subscript −1 represent?</p>",
  answer=choice(("its atomic number", False, "An electron has no protons."), ("its relative charge", True, "Right: for particles, the subscript gives the relative charge (textbook §2.2)."),
                ("its number of neutrons", False, "Electrons contain no neutrons."), ("its mass in u", False, "The superscript 0 is its mass number.")),
  hints=["For ¹₁p the subscript is 1, and for ¹₀n it's 0. What do the proton and the neutron differ in?"],
  solution="<p>The <strong>relative charge</strong>. For nuclides the subscript is Z, which is the nuclear charge anyway, so the notation is consistent.</p>",
  source=tb("2.2", 88) + "; Table 2.1, " + tb("2.1", 87))

P(id="t2-2-transfer", module="t2-2", kind="transfer", level="Transfer",
  prompt="<p>A monatomic ion <sup>A</sup>X<sup>2−</sup> has 18 electrons and 18 neutrons. Identify X (symbol) and A.</p>",
  answer={"type": "multi", "parts": [
      {"label": "X (symbol)", **sym_ans("S", "sulfur")}, {"label": "A", **num_ans(34, tol=0)}]},
  hints=["Work backward: electrons = Z − Q.", "18 = Z − (−2), so Z = 16.", "Z = 16 is sulfur.", "A = Z + neutrons."],
  solution="<p>Z = 18 + (−2) = 16 → <strong>S</strong>; A = 16 + 18 = <strong>34</strong> → <sup>34</sup>S<sup>2−</sup>.</p>",
  source=tb("2.2", 88))

P(id="t2-2-m-explain", module="t2-2", kind="mastery", level="Explain",
  prompt="<p>Why did the discovery of isotopes force a change to Dalton's definition of an element?</p>",
  answer={"type": "self", "model": "<p>Dalton said all atoms of an element are identical, including their mass (Day 1 p.14, covered in lecture). Aston's positive-ray analyzer found neon atoms with two different masses (about 20 u and 22 u). "
                                   "So an element was redefined by its number of protons (atomic number Z); isotopes share Z but differ in neutrons, so they have different mass numbers A (textbook §2.2).</p>"},
  hints=[], solution="", source=tb("2.2", 87) + "; Day 1 p.14")

P(id="t2-2-m-recognize", module="t2-2", kind="mastery", level="Recognize",
  prompt="<p>Which number alone determines which element an atom is?</p>",
  answer=choice(("mass number A", False, "Different elements can share A."), ("atomic number Z", True, "Right: the number of protons (Day 2 p.24)."),
                ("number of neutrons", False, "Isotopes differ in neutrons but are the same element."), ("charge Q", False, "Ions of one element have different charges.")),
  hints=["Day 2 p.24: an element's position is set by …"],
  solution="<p><strong>Z</strong>, the number of protons (Day 2 p.24; textbook §2.2).</p>",
  source=tb("2.2", 87) + "; Day 2 p.24")

P(id="t2-2-m-sanity", module="t2-2", kind="mastery", level="Sanity check",
  prompt="<p>A student writes a nuclide with Z = 8 and A = 7. What's wrong?</p>",
  answer=choice(("Nothing", False, "A counts protons plus neutrons."), ("A can't be smaller than Z, since A = protons + neutrons.", True, "Right."),
                ("Z must be even.", False, "No such rule."), ("Oxygen has no isotopes.", False, "It has several.")),
  hints=["A = Z + (number of neutrons), and neutrons ≥ 0."],
  solution="<p>A ≥ Z always; only <sup>1</sup>H has A = Z (textbook §2.2).</p>", source=tb("2.2", 89))

# =====================================================================================
# t2-3 Navigating the periodic table (§2.3, TB PDF p.90–94); layout basics = LECTURE (RAMP UP Day 2 p.24)
# =====================================================================================
P(id="t2-3-attempt", module="t2-3", kind="attempt", level="Guided attempt",
  prompt="<p>Identify each element (symbol).</p>",
  answer={"type": "multi", "parts": [
      {"label": "(a) the halogen in period 3", **sym_ans("Cl", "chlorine")},
      {"label": "(b) the alkaline earth metal in period 4", **sym_ans("Ca", "calcium")},
      {"label": "(c) the metalloid in group 14, period 3", **sym_ans("Si", "silicon")},
      {"label": "(d) the noble gas in period 2", **sym_ans("Ne", "neon")}]},
  hints=["Periods are rows (numbered at the left); groups are columns.",
         "Group names (textbook Fig. 2.12): alkali metals 1, alkaline earth metals 2, chalcogens 16, halogens 17, noble gases 18.",
         "Go to the named group, then down to the named row.",
         "(c): in row 3, group 14 is the green (metalloid) cell."],
  solution="<p>(a) group 17, row 3 → <strong>Cl</strong>. (b) group 2, row 4 → <strong>Ca</strong>. (c) group 14, row 3 → <strong>Si</strong>. (d) group 18, row 2 → <strong>Ne</strong>.</p>",
  compare={"wrong": "<p>“(a) the halogen in period 3 is P, the third element across.”</p>",
           "tempting": "It's easy to mix up rows and columns, or to count positions instead of reading group numbers.",
           "fails": "A period is a row; the halogens are the column labeled 17. In row 3 that's Cl (textbook §2.3; periods and groups also appear on the RAMP UP slide, Day 2 p.24)."},
  source=tb("2.3", 91, 93) + "; Day 2 p.24")

P(id="t2-3-p1", module="t2-3", kind="practice", level="Warm-up",
  prompt="<p>Classify each element.</p>",
  answer={"type": "match",
          "rows": [{"html": "Mg", "answer": "m"}, {"html": "S", "answer": "n"}, {"html": "Ge", "answer": "md"}, {"html": "Br", "answer": "n"}],
          "options": [{"key": "m", "html": "metal"}, {"key": "n", "html": "nonmetal"}, {"key": "md", "html": "metalloid"}]},
  hints=["Metals are on the left and in the middle; nonmetals at the upper right; metalloids along the staircase between them (textbook Fig. 2.9b)."],
  solution="<p>Mg <strong>metal</strong>; S <strong>nonmetal</strong>; Ge <strong>metalloid</strong>; Br <strong>nonmetal</strong> (the one nonmetal that's a liquid at room temperature).</p>",
  source=tb("2.3", 91))

P(id="t2-3-p2", module="t2-3", kind="practice", level="Standard",
  prompt="<p>Predict the charge of the most common monatomic ion of each element (textbook Table 2.2 pattern).</p>",
  answer={"type": "match",
          "rows": [{"html": "Ba", "answer": "2+"}, {"html": "Se", "answer": "2-"}, {"html": "Ga", "answer": "3+"}, {"html": "I", "answer": "1-"}],
          "options": [{"key": "1+", "html": "1+"}, {"key": "2+", "html": "2+"}, {"key": "3+", "html": "3+"},
                      {"key": "1-", "html": "1−"}, {"key": "2-", "html": "2−"}, {"key": "3-", "html": "3−"}]},
  hints=["Groups 1, 2, 13 → 1+, 2+, 3+; groups 15, 16, 17 → 3−, 2−, 1−.", "Find each element's group."],
  solution="<p>Ba (group 2) <strong>2+</strong>; Se (16) <strong>2−</strong>; Ga (13) <strong>3+</strong>; I (17) <strong>1−</strong>. The lecture gives the same pattern for Li, Na, Mg, Al, Cl, F, O (Day 7 p.19).</p>",
  source=tb("2.3", 92, 93) + "; Day 7 p.19")

P(id="t2-3-p3", module="t2-3", kind="practice", level="Warm-up",
  prompt="<p>Match each element to its group name.</p>",
  answer={"type": "match",
          "rows": [{"html": "K", "answer": "alk"}, {"html": "Sr", "answer": "ae"}, {"html": "O", "answer": "ch"}, {"html": "Cl", "answer": "ha"}, {"html": "Kr", "answer": "ng"}],
          "options": [{"key": "alk", "html": "alkali metal"}, {"key": "ae", "html": "alkaline earth metal"}, {"key": "ch", "html": "chalcogen"},
                      {"key": "ha", "html": "halogen"}, {"key": "ng", "html": "noble gas"}]},
  hints=["Groups 1, 2, 16, 17, 18 (textbook Fig. 2.12)."],
  solution="<p>K alkali metal (1); Sr alkaline earth (2); O chalcogen (16); Cl halogen (17); Kr noble gas (18).</p>",
  source=tb("2.3", 93))

P(id="t2-3-p4", module="t2-3", kind="practice", level="Standard",
  prompt="<p><span class='tag-conn'>Connects to Module 15</span> Write the formula of the ionic compound formed by strontium and iodine.</p>",
  answer=formula_ans(["SrI2"]),
  hints=["Sr is an alkaline earth metal (2+); I is a halogen (1−).", "How many 1− ions cancel one 2+ ion?"],
  solution="<p>Sr<sup>2+</sup> + 2 I<sup>−</sup> → <strong>SrI<sub>2</sub></strong> (strontium iodide), the same 1 : 2 pattern as CaCl<sub>2</sub>.</p>",
  source=tb("2.3", 93) + "; Day 7 p.20")

P(id="t2-3-transfer", module="t2-3", kind="transfer", level="Transfer",
  prompt="<p>Why did Mendeleev leave empty cells in his 1872 table?</p>",
  answer=choice(("He ran out of room.", False, "The gaps were deliberate."), ("To keep elements with similar properties in the same column, predicting elements not yet discovered", True, "Right: the gaps made predictions that were later confirmed."),
                ("Because those elements are radioactive", False, "Radioactivity was discovered in 1896."), ("Because atomic numbers were unknown", False, "True, but that's not why he left gaps.")),
  hints=["What did lining up similar properties require him to do?"],
  solution="<p>To keep chemically similar elements in the same column. He then <strong>predicted</strong> the missing elements' properties (textbook §2.3).</p>",
  source=tb("2.3", 90))

P(id="t2-3-m-explain", module="t2-3", kind="mastery", level="Explain",
  prompt="<p><span class='tag-conn'>Connection to Module 10</span> Why do elements in the same group have similar chemical properties?</p>",
  answer={"type": "self", "model": "<p>Elements in a group have the same valence-shell configuration (for example ns<sup>1</sup> for group 1), and valence electrons “primarily determine the chemical properties” (Day 6 p.14, covered in lecture). "
                                   "So Li, Na, and K all lose one electron to form 1+ ions (textbook §2.3; §3.8).</p>"},
  hints=[], solution="", source=tb("2.3", 92, 93) + "; Day 6 p.14")

P(id="t2-3-m-recognize", module="t2-3", kind="mastery", level="Recognize",
  prompt="<p>Which groups hold the transition metals?</p>",
  answer=choice(("1–2", False, "The s block."), ("3–12", True, "Right."), ("13–18", False, "The p block (main group)."), ("the two bottom rows", False, "Those are the lanthanides and actinides.")),
  hints=["Main-group elements are groups 1, 2, and 13–18."],
  solution="<p>Groups <strong>3–12</strong> (the d block, Day 6 p.20).</p>", source=tb("2.3", 92) + "; Day 6 p.20")

P(id="t2-3-m-sanity", module="t2-3", kind="mastery", level="Sanity check",
  prompt="<p>A classmate calls sodium “a nonmetal gas.” What's the correction?</p>",
  answer=choice(("Correct", False, "Na is at the far left."), ("Sodium is an alkali metal: a shiny, soft solid that forms Na<sup>+</sup>.", True, "Right."),
                ("Sodium is a metalloid.", False, "Metalloids lie along the staircase."), ("Sodium is a noble gas.", False, "Group 18 are the noble gases.")),
  hints=["Where is Na in the table?"],
  solution="<p>Sodium is a group 1 <strong>alkali metal</strong>.</p>", source=tb("2.3", 91, 93))

# =====================================================================================
# t2-4 Average atomic mass; molecular and formula mass (§2.4, TB PDF p.94–98); amu = LECTURE (Day 2 p.21)
# =====================================================================================
iso = ISOTOPES
m_B = sum(m * a for _, m, a in iso["B"])
P(id="t2-4-attempt", module="t2-4", kind="attempt", level="Guided attempt",
  prompt="<p>Boron has two stable isotopes: <sup>10</sup>B, 10.0129 amu (19.9%), and <sup>11</sup>B, 11.0093 amu (80.1%). What is boron's average atomic mass?</p>",
  answer=num_ans(m_B, sf=4, unit_label="amu", units=U_UNITS),
  hints=["An average atomic mass is a weighted average (textbook Eq. 2.3).",
         "Convert the percents to decimals: 0.199 and 0.801.",
         "Multiply each isotope's mass by its abundance.",
         "Add: 10.0129 × 0.199 + 11.0093 × 0.801."],
  solution=f"<p>m<sub>B</sub> = 10.0129 amu × 0.199 + 11.0093 amu × 0.801 = {fix(10.0129 * 0.199, 4)} + {fix(11.0093 * 0.801, 4)} = <strong>{fix(m_B, 2)} amu</strong>. "
           "It lies much closer to 11 than to 10 because <sup>11</sup>B is four times as abundant. No boron atom has this mass: every atom has one of the two isotope masses.</p>",
  compare={"wrong": f"<p>“(10.0129 + 11.0093)/2 = {fix((10.0129 + 11.0093) / 2, 3)} amu.”</p>",
           "tempting": "“Average” usually means add and divide by the count.",
           "fails": "A simple average treats both isotopes as equally common. Here <sup>11</sup>B is 80.1% of the atoms, so it must count four times as much: weight by abundance (Eq. 2.3)."},
  source=tb("2.4", 94, 95) + "; isotope data: background (standard reference values)")

m_Mg = sum(m * a for _, m, a in iso["Mg"])
P(id="t2-4-p1", module="t2-4", kind="practice", level="Standard",
  prompt="<p>Magnesium: <sup>24</sup>Mg 23.9850 amu (78.99%), <sup>25</sup>Mg 24.9858 amu (10.00%), <sup>26</sup>Mg 25.9826 amu (11.01%). Average atomic mass?</p>",
  answer=num_ans(m_Mg, sf=4, unit_label="amu", units=U_UNITS),
  hints=["Same method with three isotopes.", "0.7899 × 23.9850 + 0.1000 × 24.9858 + 0.1101 × 25.9826."],
  solution=f"<p>= {fix(0.7899 * 23.9850, 4)} + {fix(0.1000 * 24.9858, 4)} + {fix(0.1101 * 25.9826, 4)} = <strong>{fix(m_Mg, 2)} amu</strong>, the value in the periodic table.</p>",
  source=tb("2.4", 94) + "; isotope data: background")

(_, m69, _), (_, m71, _) = iso["Ga"]
x69 = (m71 - 69.723) / (m71 - m69)
P(id="t2-4-p2", module="t2-4", kind="practice", level="Stretch",
  prompt="<p>Gallium has two stable isotopes, <sup>69</sup>Ga (68.9256 amu) and <sup>71</sup>Ga (70.9247 amu), and an average atomic mass of 69.723 amu. What percent of gallium atoms are <sup>69</sup>Ga?</p>",
  answer=num_ans(x69 * 100, sf=3, unit_label="%", units=PCT_UNITS),
  hints=["Let x = the fraction of <sup>69</sup>Ga; then 1 − x is <sup>71</sup>Ga.", "69.723 = x(68.9256) + (1 − x)(70.9247).", "x = (70.9247 − 69.723)/(70.9247 − 68.9256).", "Convert the fraction to a percent."],
  solution=f"<p>x = (70.9247 − 69.723)/(70.9247 − 68.9256) = {fix(x69, 4)} → <strong>{fix(x69 * 100, 1)}%</strong> <sup>69</sup>Ga (and {fix(100 - x69 * 100, 1)}% <sup>71</sup>Ga). The average sits closer to 69, as expected.</p>",
  source=tb("2.4", 96, 97))

mw_h2o = molar_mass("H2O")
P(id="t2-4-p3", module="t2-4", kind="practice", level="Warm-up",
  prompt="<p>What is the molecular mass of water, H<sub>2</sub>O? (H 1.0079 amu, O 15.999 amu.)</p>",
  answer=num_ans(mw_h2o, sf=5, unit_label="amu", units=U_UNITS),
  hints=["Add the average atomic masses of every atom in one molecule.", "2 × 1.0079 + 15.999."],
  solution=f"<p>2(1.0079 amu) + 15.999 amu = <strong>{fix(mw_h2o, 3)} amu</strong>.</p>",
  source=tb("2.4", 97))

fm_mgcl2 = molar_mass("MgCl2")
P(id="t2-4-p4", module="t2-4", kind="practice", level="Standard",
  prompt="<p>MgCl<sub>2</sub> is ionic. What is the mass of one formula unit? (Mg 24.305, Cl 35.453 amu.)</p>",
  answer=num_ans(fm_mgcl2, sf=5, unit_label="amu", units=U_UNITS),
  hints=["An ionic compound has a formula mass: one formula unit is one Mg<sup>2+</sup> and two Cl<sup>−</sup>.", "Ion masses ≈ atom masses (electrons are negligible)."],
  solution=f"<p>24.305 + 2(35.453) = <strong>{fix(fm_mgcl2, 3)} amu</strong> per formula unit. It's a <em>formula mass</em>, not a molecular mass: there are no MgCl<sub>2</sub> molecules, only a lattice (Day 7 p.16).</p>",
  source=tb("2.4", 97, 98) + "; Day 7 p.16")

x63 = (64.93 - 63.55) / (64.93 - 62.93)
P(id="t2-4-transfer", module="t2-4", kind="transfer", level="Transfer",
  prompt="<p>Copper has isotopes of mass 62.93 amu and 64.93 amu, and an average atomic mass of 63.55 amu. What percent of copper atoms are the lighter isotope?</p>",
  answer=num_ans(x63 * 100, sf=2, tol=0.02, unit_label="%", units=PCT_UNITS),
  hints=["Two isotopes: x and 1 − x.", "63.55 = 62.93x + 64.93(1 − x).", "x = (64.93 − 63.55)/(64.93 − 62.93)."],
  solution=f"<p>x = 1.38/2.00 = {fix(x63, 2)} → <strong>{fix(x63 * 100, 0)}%</strong> of copper is the lighter isotope. The average (63.55) is closer to 62.93, consistent with that.</p>",
  source=tb("2.4", 96, 97))

P(id="t2-4-m-explain", module="t2-4", kind="mastery", level="Explain",
  prompt="<p>Explain why the periodic table lists 35.45 amu for chlorine even though no chlorine atom has that mass.</p>",
  answer={"type": "self", "model": "<p>Chlorine atoms are either <sup>35</sup>Cl (≈ 34.97 amu) or <sup>37</sup>Cl (≈ 36.97 amu). The table lists the <em>weighted average</em> over natural abundances (about 76% and 24%), which is what a sample containing huge numbers of atoms behaves like (textbook §2.4). "
                                   "It's closer to 35 because <sup>35</sup>Cl is more common.</p>"},
  hints=[], solution="", source=tb("2.4", 94, 95))

P(id="t2-4-m-recognize", module="t2-4", kind="mastery", level="Recognize",
  prompt="<p>“The isotopes' masses and percent abundances are given; find the element's atomic mass.” What operation?</p>",
  answer=choice(("simple average", False, "Only if the abundances were equal."), ("abundance-weighted average", True, "Right: Eq. 2.3."), ("the sum of the masses", False, "No."), ("the most abundant isotope's mass", False, "That ignores the others.")),
  hints=["Eq. 2.3: m<sub>X</sub> = a<sub>1</sub>m<sub>1</sub> + a<sub>2</sub>m<sub>2</sub> + …"],
  solution="<p>A <strong>weighted average</strong> with decimal abundances as the weights.</p>", source=tb("2.4", 94))

P(id="t2-4-m-sanity", module="t2-4", kind="mastery", level="Sanity check",
  prompt="<p>A student calculates that an element with isotopes of 50.0 and 52.0 amu has an average atomic mass of 53.1 amu. Possible?</p>",
  answer=choice(("Yes", False, "A weighted average must lie between the extremes."), ("No: the average must lie between 50.0 and 52.0 amu.", True, "Right."),
                ("Yes, if one isotope is radioactive.", False, "Still a weighted average."), ("Only if the abundances add to more than 100%.", False, "Then the abundances themselves are wrong.")),
  hints=["Can a weighted average be larger than every value being averaged?"],
  solution="<p>No. A weighted average always lies <strong>between</strong> the smallest and largest isotope masses.</p>", source=tb("2.4", 94))

# =====================================================================================
# t2-5 Moles and molar masses (§2.5, TB PDF p.98–104)
# =====================================================================================
n_h2o = 10.0 / mw_h2o
N_h2o = n_h2o * NA
P(id="t2-5-attempt", module="t2-5", kind="attempt", level="Guided attempt",
  prompt="<p>How many (a) moles and (b) molecules of water are in 10.0 g of water? (Molar mass of H<sub>2</sub>O = 18.015 g/mol; N<sub>A</sub> = 6.022 × 10<sup>23</sup> mol<sup>−1</sup>.)</p>",
  answer={"type": "multi", "parts": [
      {"label": "(a) moles", **num_ans(n_h2o, sf=3, unit_label="mol", units=MOL_UNITS)},
      {"label": "(b) molecules", **num_ans(N_h2o, sf=3)}]},
  hints=["Follow the map: mass → moles → particles (textbook Fig. 2.18).",
         "Mass → moles: divide by the molar mass.",
         "10.0 g × (1 mol / 18.015 g).",
         "Moles → molecules: multiply by N<sub>A</sub>."],
  solution=f"<p>(a) 10.0 g × (1 mol/18.015 g) = <strong>{num(n_h2o, 3)} mol</strong>. (b) {num(n_h2o, 4)} mol × 6.022 × 10<sup>23</sup> molecules/mol = <strong>{sci(N_h2o)} molecules</strong>.</p>",
  compare={"wrong": f"<p>“10.0 × 18.015 = 180 mol” or “10.0 g × 6.022 × 10<sup>23</sup> = {sci(10.0 * NA)} molecules.”</p>",
           "tempting": "Multiplying whatever numbers are given feels like progress.",
           "fails": "With units written out, g × g/mol gives g²/mol, not mol, and grams × N<sub>A</sub> skips the mole entirely. Grams must pass through moles (divide by g/mol) before N<sub>A</sub> can count particles."},
  source=tb("2.5", 98, 101))

mm_nh3 = molar_mass("NH3")
P(id="t2-5-p1", module="t2-5", kind="practice", level="Warm-up",
  prompt="<p>What is the molar mass of ammonia, NH<sub>3</sub>? (N 14.007, H 1.0079 g/mol.)</p>",
  answer=num_ans(mm_nh3, sf=5, unit_label="g/mol", units=GMOL_UNITS),
  hints=["Sum over the atoms in the formula.", "14.007 + 3(1.0079)."],
  solution=f"<p>14.007 + 3(1.0079) = <strong>{fix(mm_nh3, 3)} g/mol</strong>, the same number as the molecular mass in amu.</p>",
  source=tb("2.5", 100))

m_nacl = 0.250 * molar_mass("NaCl")
P(id="t2-5-p2", module="t2-5", kind="practice", level="Standard",
  prompt="<p>What is the mass of 0.250 mol of NaCl? (Na 22.990, Cl 35.453 g/mol.)</p>",
  answer=num_ans(m_nacl, sf=3, unit_label="g", units=G_UNITS),
  hints=["Moles → mass: multiply by the molar mass.", "Molar mass of NaCl = 58.443 g/mol."],
  solution=f"<p>0.250 mol × 58.443 g/mol = <strong>{num(m_nacl, 3)} g</strong>.</p>",
  source=tb("2.5", 101))

N_al = 5.00 / ATOMIC_MASS["Al"] * NA
P(id="t2-5-p3", module="t2-5", kind="practice", level="Standard",
  prompt="<p>How many atoms are in 5.00 g of aluminum? (Al 26.982 g/mol.)</p>",
  answer=num_ans(N_al, sf=3),
  hints=["Mass → moles → atoms.", "5.00 g ÷ 26.982 g/mol, then × N<sub>A</sub>."],
  solution=f"<p>5.00 g × (1 mol/26.982 g) × 6.022 × 10<sup>23</sup> atoms/mol = <strong>{sci(N_al)} atoms</strong>.</p>",
  source=tb("2.5", 98, 101))

m_ch4 = molar_mass("CH4") / NA
P(id="t2-5-p4", module="t2-5", kind="practice", level="Stretch",
  prompt="<p>What is the mass in grams of one molecule of methane, CH<sub>4</sub>? (C 12.011, H 1.0079 g/mol.)</p>",
  answer=num_ans(m_ch4, sf=4, unit_label="g", units=G_UNITS),
  hints=["Molar mass = mass per mole of molecules.", "Divide the molar mass by N<sub>A</sub> to get grams per molecule.", "Molar mass of CH<sub>4</sub> = 12.011 + 4(1.0079) = 16.043 g/mol."],
  solution=f"<p>16.043 g/mol ÷ 6.022 × 10<sup>23</sup> molecules/mol = <strong>{sci(m_ch4, 4)} g</strong> per molecule. Check: 16.043 amu × 1.66054 × 10<sup>−24</sup> g/amu gives the same.</p>",
  source=tb("2.5", 98, 100))

P(id="t2-5-p5", module="t2-5", kind="practice", level="Standard",
  prompt="<p>How many moles of oxygen <em>atoms</em> are in 2.00 mol of glucose, C<sub>6</sub>H<sub>12</sub>O<sub>6</sub>?</p>",
  answer=num_ans(12.0, sf=3, unit_label="mol", units=MOL_UNITS),
  hints=["The subscript is a mole ratio: 6 mol O atoms per 1 mol of glucose.", "2.00 mol × 6."],
  solution="<p>2.00 mol C<sub>6</sub>H<sub>12</sub>O<sub>6</sub> × (6 mol O / 1 mol C<sub>6</sub>H<sub>12</sub>O<sub>6</sub>) = <strong>12.0 mol O</strong>.</p>",
  source=tb("2.5", 100, 101))

N_cu = 8.96 / ATOMIC_MASS["Cu"] * NA
P(id="t2-5-transfer", module="t2-5", kind="transfer", level="Transfer",
  prompt="<p>How many copper atoms are in a 1.00 cm<sup>3</sup> cube of copper? (Density 8.96 g/cm<sup>3</sup>; Cu 63.546 g/mol.)</p>",
  answer=num_ans(N_cu, sf=3),
  hints=["Chain: volume → mass → moles → atoms.", "Density converts cm<sup>3</sup> to g.", "8.96 g ÷ 63.546 g/mol.", "× N<sub>A</sub>."],
  solution=f"<p>1.00 cm<sup>3</sup> × 8.96 g/cm<sup>3</sup> = 8.96 g; ÷ 63.546 g/mol = {num(8.96 / ATOMIC_MASS['Cu'], 3)} mol; × 6.022 × 10<sup>23</sup> = <strong>{sci(N_cu)} atoms</strong>.</p>",
  source=tb("2.5", 102, 103) + "; " + tb("1.3", 43))

P(id="t2-5-m-explain", module="t2-5", kind="mastery", level="Explain",
  prompt="<p>Why does gold's molar mass in g/mol have the same number as its atomic mass in amu (196.97)?</p>",
  answer={"type": "self", "model": "<p>The mole is defined so that N<sub>A</sub> particles of mass 1 amu have a mass of 1 g (1 amu × 6.022 × 10<sup>23</sup> ≈ 1 g). "
                                   "So one atom's mass in amu, multiplied by N<sub>A</sub>, gives the same number in grams per mole. The mole bridges the particle scale (amu) and the lab scale (grams) (textbook §2.5).</p>"},
  hints=[], solution="", source=tb("2.5", 100))

P(id="t2-5-m-recognize", module="t2-5", kind="mastery", level="Recognize",
  prompt="<p>You have a number of molecules and want grams. What is the chain?</p>",
  answer=choice(("molecules × molar mass", False, "Skips the mole."), ("molecules ÷ N<sub>A</sub>, then × molar mass", True, "Right: particles → moles → mass (Fig. 2.18)."),
                ("molecules × N<sub>A</sub> ÷ molar mass", False, "Both steps inverted."), ("molecules ÷ molar mass", False, "Units don't work.")),
  hints=["Every route between particles and grams passes through moles."],
  solution="<p>÷ N<sub>A</sub> (particles → mol), then × ℳ (mol → g).</p>", source=tb("2.5", 101))

P(id="t2-5-m-sanity", module="t2-5", kind="mastery", level="Sanity check",
  prompt="<p>A student finds that 1.0 g of carbon contains 5.0 × 10<sup>40</sup> atoms. Reasonable?</p>",
  answer=choice(("Yes: atoms are tiny.", False, "Check the order of magnitude."), ("No: 1.0 g of C is about 0.083 mol, about 5 × 10<sup>22</sup> atoms.", True, "Right: off by 10<sup>18</sup>."),
                ("Yes, carbon is light.", False, "Still about 10<sup>22</sup>."), ("No: it should be less than 1 atom.", False, "No.")),
  hints=["Estimate: 1 g ÷ 12 g/mol ≈ 0.08 mol."],
  solution="<p>1.0 g ÷ 12.011 g/mol × 6.022 × 10<sup>23</sup> ≈ <strong>5.0 × 10<sup>22</sup></strong> atoms.</p>", source=tb("2.5", 98, 101))

# =====================================================================================
# t2-6 Mass spectrometry (§2.6, TB PDF p.104–108)
# =====================================================================================
cands = {"C4H10": molar_mass("C4H10"), "C3H8": molar_mass("C3H8"), "C4H8": molar_mass("C4H8"), "C5H12": molar_mass("C5H12")}
P(id="t2-6-attempt", module="t2-6", kind="attempt", level="Guided attempt",
  prompt="<p>An unknown hydrocarbon's mass spectrum has its molecular-ion peak (M<sup>+</sup>) at m/z = 58. Which molecular formula fits?</p>",
  answer=choice((f"C<sub>4</sub>H<sub>10</sub> ({fix(cands['C4H10'], 2)} amu)", True, "Right: its molecular mass rounds to 58."),
                (f"C<sub>3</sub>H<sub>8</sub> ({fix(cands['C3H8'], 2)} amu)", False, "That would give M<sup>+</sup> at 44."),
                (f"C<sub>4</sub>H<sub>8</sub> ({fix(cands['C4H8'], 2)} amu)", False, "That would give 56."),
                (f"C<sub>5</sub>H<sub>12</sub> ({fix(cands['C5H12'], 2)} amu)", False, "That would give 72.")),
  hints=["M<sup>+</sup> is the molecule minus one electron, so its mass is essentially the molecular mass (textbook §2.6).",
         "Charge is 1+, so m/z = m.",
         "Compute each candidate's molecular mass: C 12.011, H 1.0079.",
         "Which one is 58?"],
  solution=f"<p>C<sub>4</sub>H<sub>10</sub>: 4(12.011) + 10(1.0079) = <strong>{fix(cands['C4H10'], 2)} amu</strong> → M<sup>+</sup> at m/z 58. The smaller peaks in such a spectrum are fragment ions.</p>",
  compare={"wrong": "<p>“The tallest peak is always the molecular ion.”</p>",
           "tempting": "The tallest peak is the most noticeable.",
           "fails": "The molecular-ion peak is the prominent peak with the <em>highest mass</em>. Fragments can be taller. In the textbook's benzene spectrum M<sup>+</sup> happens to be tallest, but that's not a rule."},
  source=tb("2.6", 104, 106))

P(id="t2-6-p1", module="t2-6", kind="practice", level="Warm-up",
  prompt="<p>In a mass spectrometer, how does a molecule usually become a molecular ion M<sup>+</sup>?</p>",
  answer=choice(("It gains a proton.", False, "Not in electron-impact ionization."), ("A high-energy electron knocks one of its electrons out.", True, "Right."),
                ("It splits in half.", False, "That makes fragment ions."), ("It absorbs visible light.", False, "No.")),
  hints=["The textbook's benzene example (Fig. 2.21)."],
  solution="<p>Bombarding electrons <strong>knock out one electron</strong>, leaving a 1+ ion with essentially the molecule's mass.</p>",
  source=tb("2.6", 104))

mm_eth = molar_mass("C2H6O")
P(id="t2-6-p2", module="t2-6", kind="practice", level="Standard",
  prompt="<p>At what m/z would the molecular-ion peak of ethanol, C<sub>2</sub>H<sub>6</sub>O, appear?</p>",
  answer=num_ans(46.0, sf=2),
  hints=["m/z = the ion's mass ÷ its charge, and M<sup>+</sup> has a 1+ charge.", "Each ion is one molecule made of particular isotopes: use the common ones, <sup>12</sup>C, <sup>1</sup>H, <sup>16</sup>O."],
  solution=f"<p>An ion made of the most common isotopes has mass 2(12) + 6(1) + 16 = 46, so M<sup>+</sup> appears at <strong>m/z = 46</strong>, the way the textbook labels molecular-ion peaks (C<sub>2</sub>H<sub>2</sub> at 26, C<sub>6</sub>H<sub>6</sub> at 78). "
           f"The average molar mass, {fix(mm_eth, 2)} g/mol, is a little higher because it includes heavier isotopes, which make small peaks at m/z 47 and 48.</p>",
  source=tb("2.6", 104, 105))

P(id="t2-6-p3", module="t2-6", kind="practice", level="Standard",
  prompt="<p>The mass spectrum of HBr shows two molecular-ion peaks of nearly equal height, at m/z = 80 and 82. Why?</p>",
  answer=choice(("HBr breaks into two fragments.", False, "Fragments would be lighter than M<sup>+</sup>."), ("Bromine's two isotopes, <sup>79</sup>Br and <sup>81</sup>Br, are nearly equally abundant.", True, "Right: H<sup>79</sup>Br and H<sup>81</sup>Br."),
                ("One peak is HBr<sup>2+</sup>.", False, "A 2+ ion would appear near m/z 40."), ("Hydrogen has two isotopes.", False, "<sup>2</sup>H is too rare to make a peak that large.")),
  hints=["Each peak is one kind of molecule. What differs between them?"],
  solution="<p>H<sup>79</sup>Br (m/z 80) and H<sup>81</sup>Br (m/z 82); <sup>79</sup>Br and <sup>81</sup>Br are about 50.7% and 49.3% of bromine (background values). The textbook shows the same effect for HCl.</p>",
  source=tb("2.6", 106) + "; bromine abundances: background")

P(id="t2-6-p4", module="t2-6", kind="practice", level="Warm-up",
  prompt="<p>Why can the mass of an ion be read directly off the m/z axis?</p>",
  answer=choice(("Because z is usually 1", True, "Right: m/1 = m."), ("Because m/z doesn't depend on charge", False, "It does: a 2+ ion appears at half its mass."), ("Because ions have no mass", False, "No."), ("Because electrons are heavy", False, "No.")),
  hints=["What's m ÷ 1?"],
  solution="<p>Most ions in the spectrum carry a <strong>1+</strong> charge, so m/z = m.</p>", source=tb("2.6", 104))

a35, a37 = ISOTOPES["Cl"][0][2], ISOTOPES["Cl"][1][2]
r72_70 = (2 * a35 * a37) / (a35 * a35)
P(id="t2-6-transfer", module="t2-6", kind="transfer", level="Transfer",
  prompt="<p>Chlorine is about 75.76% <sup>35</sup>Cl and 24.24% <sup>37</sup>Cl. In the mass spectrum of Cl<sub>2</sub>, what is the ratio of the height of the m/z 72 peak (<sup>35</sup>Cl<sup>37</sup>Cl) to the m/z 70 peak (<sup>35</sup>Cl<sub>2</sub>)?</p>",
  answer=num_ans(r72_70, sf=3, tol=0.02),
  hints=["Each Cl atom in a molecule is independently <sup>35</sup>Cl or <sup>37</sup>Cl.",
         "P(<sup>35</sup>Cl<sub>2</sub>) = 0.7576<sup>2</sup>.",
         "P(<sup>35</sup>Cl<sup>37</sup>Cl) = 2 × 0.7576 × 0.2424 (either atom can be the heavy one).",
         "Divide the second by the first."],
  solution=f"<p>(2 × 0.7576 × 0.2424)/(0.7576)<sup>2</sup> = 2 × 0.2424/0.7576 = <strong>{fix(r72_70, 2)}</strong>. A third, smaller peak at m/z 74 (<sup>37</sup>Cl<sub>2</sub>) also appears.</p>"
           "<p class='bg'>Combining isotope probabilities this way goes beyond the textbook's §2.6 examples; the isotope abundances are standard reference values.</p>",
  source=tb("2.6", 106) + "; chlorine abundances: background")

P(id="t2-6-m-explain", module="t2-6", kind="mastery", level="Explain",
  prompt="<p>Describe how a mass spectrometer turns a sample into a mass spectrum.</p>",
  answer={"type": "self", "model": "<p>The sample is vaporized and bombarded with high-energy electrons, which knock out electrons to make molecular ions (M<sup>+</sup>) and fragment ions. "
                                   "The ions are separated by mass-to-charge ratio (m/z), the way Aston's analyzer separated neon ions, and counted. The spectrum plots relative intensity against m/z; the highest-mass prominent peak (M<sup>+</sup>) gives the molecular mass, and the fragment pattern helps identify the compound (textbook §2.6).</p>"},
  hints=[], solution="", source=tb("2.6", 104, 106))

P(id="t2-6-m-recognize", module="t2-6", kind="mastery", level="Recognize",
  prompt="<p>Aston's positive-ray analyzer (§2.2) was the forerunner of which instrument?</p>",
  answer=choice(("the cathode-ray tube", False, "Thomson's tube came first."), ("the mass spectrometer", True, "Right."), ("the spectroscope", False, "That separates light."), ("the STM", False, "That images atoms.")),
  hints=["Both separate ions by mass and charge."],
  solution="<p>The <strong>mass spectrometer</strong> (textbook §2.2 and §2.6).</p>", source=tb("2.2", 87) + "; " + tb("2.6", 104))

P(id="t2-6-m-sanity", module="t2-6", kind="mastery", level="Sanity check",
  prompt="<p>A student claims methane (CH<sub>4</sub>) shows its molecular-ion peak at m/z = 18. Plausible?</p>",
  answer=choice(("Yes", False, "CH<sub>4</sub> is about 16 amu."), ("No: M<sup>+</sup> for CH<sub>4</sub> is at m/z 16; a peak at 18 suggests water.", True, "Right."),
                ("Yes, because of isotopes", False, "Isotope peaks are small and appear at 17."), ("No: at 12", False, "That would be a C<sup>+</sup> fragment.")),
  hints=["12.011 + 4(1.0079) = ?"],
  solution="<p>CH<sub>4</sub>: 16.04 amu → M<sup>+</sup> at <strong>16</strong>.</p>", source=tb("2.6", 104))

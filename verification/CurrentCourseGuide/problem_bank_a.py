"""Problem bank, modules m1-m8. Every numeric key is COMPUTED here from the course
relationships; verify_guide.py re-derives each one independently."""
import math
from guide_common import *

FREQ_UNITS = ["s^-1", "s-1", "1/s", "/s", "hz", "s⁻¹", "s^−1", "s−1", "per s", "per second"]
J_UNITS = ["j", "joule", "joules", "j/photon", "j per photon"]
NM_UNITS = ["nm", "nanometer", "nanometers", "nanometre", "nanometres"]
M_UNITS = ["m", "meter", "meters", "metre", "metres"]
KJMOL_UNITS = ["kj/mol", "kj mol^-1", "kj mol-1", "kj·mol^-1", "kj/mole", "kj mol⁻¹", "kj·mol⁻¹"]
MS_UNITS = ["m/s", "m s^-1", "m s-1", "ms^-1", "m·s^-1", "m s⁻¹", "m·s⁻¹"]
G_UNITS = ["g", "gram", "grams"]

def num_ans(value, sf=None, unit_label=None, units=None, tol=0.01, ask_unit=False):
    d = {"type": "numeric", "value": value, "tol": tol}
    if sf is not None:
        d["sigfigs"] = sf
    if unit_label:
        d["unitLabel"] = unit_label
    if units:
        d["units"] = units
    d["askUnit"] = ask_unit
    return d

def choice(*opts):
    """opts: (html, correct, feedback)"""
    return {"type": "choice", "options": [{"html": h, "correct": c, "feedback": f} for h, c, f in opts]}

PROBLEMS = []
def add(**kw):
    PROBLEMS.append(kw)
    return kw

# =====================================================================================
# m1  Atoms from mass laws  (Day 1 p.8–15)
# =====================================================================================
r_A = 2.664 / 1.332
add(id="m1-attempt", module="m1", kind="attempt", level="Guided attempt",
    prompt="<p>Carbon forms two different oxides. In oxide A, 1.000 g of carbon is combined with 1.332 g of oxygen. "
           "In oxide B, 1.000 g of carbon is combined with 2.664 g of oxygen.</p>"
           "<p>For a fixed mass of carbon, what is the ratio of oxygen masses, B : A? Enter it as a decimal.</p>",
    answer=num_ans(r_A, sf=4),
    hints=["Two different compounds made of the same two elements: that is the setting of the Law of Multiple Proportions (Day 1 p.13).",
           "The law compares the mass of one element that combines with a <em>fixed</em> mass of the other.",
           "Carbon is already fixed at 1.000 g in both oxides, so you can compare the two oxygen masses directly.",
           "Ratio = (2.664 g O) ÷ (1.332 g O). The grams cancel, leaving a pure number."],
    solution=f"<p>Ratio (B : A) = 2.664 g ÷ 1.332 g = <strong>{fix(r_A, 3)}</strong>. That is a 2 : 1 ratio of small whole numbers, exactly what the Law of Multiple Proportions predicts (Day 1 p.13).</p>"
             "<p>At the particle level, oxide B carries two oxygen atoms for every one that oxide A carries, per carbon atom. "
             "Atoms combine only in whole numbers (Dalton, Day 1 p.14), so the oxygen mass can only change in whole-number steps.</p>"
             "<p class='bg'>The simplest formulas that fit are CO and CO<sub>2</sub>. Choosing actual formulas needs more information than this ratio gives.</p>",
    compare={
        "wrong": "<p>“Oxide A is 1.332 ÷ 2.332 = 57.1% O and oxide B is 2.664 ÷ 3.664 = 72.7% O. Then 72.7 ÷ 57.1 = 1.27, which isn’t a whole number, so the law fails.”</p>",
        "tempting": "Percent composition is the method from Day 1 p.11, so reaching for it feels natural.",
        "fails": "Percentages change the basis: each percentage is out of a different total mass. The law compares one element's mass per <em>fixed</em> mass of the other element. Fix carbon at 1.000 g and the ratio is exactly 2 : 1."},
    source="Day 1 p.13–14")

m_water = 3.00 / (1.01 / 9.01)
add(id="m1-p1", module="m1", kind="practice", level="Warm-up",
    prompt="<p>Pure water is always 11.2% hydrogen by mass (Day 1 p.11). A sample of pure water contains 3.00 g of hydrogen. What is the mass of the water sample?</p>",
    answer=num_ans(m_water, sf=3, unit_label="g"),
    hints=["Same compound means same composition: this is the Law of Constant Composition.",
           "Mass fraction of H = (mass of H) ÷ (mass of water) = 0.112.",
           "Rearrange: mass of water = (mass of H) ÷ 0.112.",
           "Mass of water = 3.00 g ÷ 0.112."],
    solution=f"<p>Mass of water = 3.00 g ÷ 0.112 = <strong>{num(m_water, 3)} g</strong> (3 significant figures, matching 3.00 g and 11.2%). "
             f"Check: 26.8 g × 0.112 = 3.00 g of H, so the rest, {num(m_water - 3.00, 3)} g, is oxygen.</p>",
    source="Day 1 p.11")

r_S = 1.50 / 1.00
add(id="m1-p2", module="m1", kind="practice", level="Standard",
    prompt="<p>Sulfur forms two oxides. In sample X, 1.00 g of sulfur is combined with 1.00 g of oxygen. In sample Y, 1.00 g of sulfur is combined with 1.50 g of oxygen.</p>"
           "<p>For a fixed mass of sulfur, what is the ratio of oxygen masses, Y : X?</p>",
    answer=num_ans(r_S, sf=3),
    hints=["Two compounds of the same two elements, so think multiple proportions.",
           "Is the mass of one element already held fixed in both samples?",
           "Yes: sulfur is 1.00 g in both, so compare the oxygen masses.",
           "Ratio = 1.50 g ÷ 1.00 g."],
    solution="<p>Ratio = 1.50 g ÷ 1.00 g = <strong>1.50</strong>, a 3 : 2 ratio of small whole numbers.</p>"
             "<p class='bg'>This is the textbook's sulfur–oxygen example, SO<sub>3</sub> vs. SO<sub>2</sub> (textbook §1.1, PDF p.41, printed 7).</p>",
    source="Day 1 p.13")

add(id="m1-p3", module="m1", kind="practice", level="Standard",
    prompt="<p>A 10.0 g sample of a white solid is heated in an open dish. A gas escapes, and 5.60 g of solid remains. Nothing else enters or leaves. What mass of gas escaped?</p>",
    answer=num_ans(10.0 - 5.60, sf=3, unit_label="g"),
    hints=["Which law governs where the “missing” mass went?",
           "Conservation of mass: matter is neither created nor destroyed (Day 1 p.10).",
           "Total mass before = mass of the solid left + mass of the gas that escaped.",
           "Mass of gas = 10.0 g − 5.60 g."],
    solution="<p>Mass of gas = 10.0 g − 5.60 g = <strong>4.4 g</strong>. For subtraction, the answer keeps the fewest decimal places: 10.0 has one, so report 4.4 g. "
             "The mass didn't disappear; it left as a gas. That is exactly why the law was hard to see for centuries: gas masses are hard to track (Day 1 p.10).</p>",
    source="Day 1 p.10")
PROBLEMS[-1]["answer"]["sigfigs"] = 2

add(id="m1-p4", module="m1", kind="practice", level="Standard",
    prompt="<p>Which postulate of Dalton's atomic theory directly explains the Law of Multiple Proportions?</p>",
    answer=choice(
        ("Matter consists of atoms, which cannot be destroyed.", False,
         "That postulate explains conservation of mass: atoms are rearranged, not destroyed."),
        ("All atoms of the same element are identical to each other.", False,
         "Identical atoms help explain why one compound has a fixed composition, but they don't by themselves produce whole-number ratios between two compounds."),
        ("Atoms combine in small whole-number ratios when forming compounds.", True,
         "Right. If compound B has two O atoms for every one in compound A (per C atom), the oxygen mass must double: a small whole-number ratio."),
        ("Atoms of different elements have different masses.", False,
         "True for Dalton (the second postulate says atoms of different elements differ), but different masses alone don't force whole-number ratios.")),
    hints=["Match each of Dalton's three postulates (Day 1 p.14) to the law it explains.",
           "Multiple proportions is about <em>whole-number</em> ratios. Which postulate mentions whole numbers?"],
    solution="<p><strong>Atoms combine in small whole-number ratios.</strong> That postulate makes the oxygen mass per fixed mass of carbon change in whole-number steps. "
             "The “cannot be destroyed” postulate explains conservation of mass, and “identical atoms” supports constant composition.</p>",
    source="Day 1 p.14")

r3 = 2.28 / 0.571
add(id="m1-transfer", module="m1", kind="transfer", level="Transfer",
    prompt="<p>Nitrogen forms several oxides. Per 1.00 g of nitrogen, compound I contains 0.571 g O, compound II contains 1.14 g O, and compound III contains 2.28 g O.</p>"
           "<p>What is the ratio of oxygen masses, III : I? Then decide whether all three compounds obey the same law.</p>",
    answer=num_ans(r3, sf=3),
    hints=["The mass of one element (nitrogen) is fixed, so multiple proportions applies.",
           "Divide each oxygen mass by the smallest one.",
           "III : I = 2.28 ÷ 0.571 and II : I = 1.14 ÷ 0.571.",
           "Round each result to the nearest small whole number and check that it's close."],
    solution=f"<p>III : I = 2.28 ÷ 0.571 = <strong>{fix(r3, 2)}</strong> ≈ 4, and II : I = 1.14 ÷ 0.571 = {fix(1.14 / 0.571, 2)} ≈ 2. "
             "The oxygen masses are in the ratio 1 : 2 : 4, all small whole numbers, so all three compounds obey the Law of Multiple Proportions.</p>"
             "<p class='bg'>Formulas consistent with 1 : 2 : 4 are N<sub>2</sub>O, NO, and NO<sub>2</sub> "
             "(O per g N: 16.00/28.01 = 0.571; 16.00/14.01 = 1.14; 32.00/14.01 = 2.28).</p>",
    source="Day 1 p.13")

add(id="m1-m-explain", module="m1", kind="mastery", level="Explain",
    prompt="<p>In two or three sentences: why does the Law of Constant Composition make sense if matter is made of atoms?</p>",
    answer={"type": "self", "model": "<p>Every unit of a pure compound contains the same number of each kind of atom, and all atoms of one element have the same mass (Dalton, Day 1 p.14). "
                                     "So every sample, of any size, has the same mass ratio of its elements. Water is always 11.2% H because every water unit has the same H and O atoms (Day 1 p.11).</p>"},
    hints=[], solution="", source="Day 1 p.11, p.14")

add(id="m1-m-recognize", module="m1", kind="mastery", level="Recognize",
    prompt="<p>“Every sample of table salt, from any source, is 39.3% sodium by mass.” Which law does this illustrate?</p>",
    answer=choice(("Law of Constant Composition (Definite Proportions)", True, "Right: one compound, always the same composition by mass."),
                  ("Law of Multiple Proportions", False, "That law needs two different compounds of the same two elements."),
                  ("Law of Conservation of Mass", False, "That law is about total mass before and after a change."),
                  ("Law of Conservation of Energy", False, "Energy isn't mentioned; this is about composition.")),
    hints=["One compound or two? Composition or a before/after comparison?"],
    solution="<p><strong>Constant Composition.</strong> One compound always has the same proportion of its elements by mass (Day 1 p.11).</p>",
    source="Day 1 p.11")

add(id="m1-m-sanity", module="m1", kind="mastery", level="Sanity check",
    prompt="<p>A student reports that a sample of pure water is 20% hydrogen by mass. What is the best conclusion?</p>",
    answer=choice(("Water's composition depends on where it came from.", False, "That would violate constant composition, which holds for every pure compound."),
                  ("The sample isn't pure water, or the measurement is wrong.", True, "Right: pure water is always 11.2% H by mass (Day 1 p.11)."),
                  ("The hydrogen atoms in this sample are heavier.", False, "Dalton: all atoms of one element are identical (Day 1 p.14). Isotopes change masses only slightly and don't explain 20% (RAMP UP, Day 2 p.23)."),
                  ("Some mass was destroyed during the measurement.", False, "Mass is conserved (Day 1 p.10).")),
    hints=["What does the Law of Constant Composition promise about every pure sample?"],
    solution="<p>Pure water is always 11.2% hydrogen by mass. A 20% result means the sample isn't pure water, or the measurement went wrong.</p>",
    source="Day 1 p.11")

# =====================================================================================
# m2  Inside the atom  (Day 1 p.16–20; Day 2 p.4–24)
# =====================================================================================
ratio_pe = MP_AMU / ME_AMU
add(id="m2-attempt", module="m2", kind="attempt", level="Guided attempt",
    prompt="<p>Using the particle table from Day 2 p.22 (proton 1.00728 amu; electron 5.48580 × 10<sup>−4</sup> amu), how many electrons would it take to equal the mass of one proton?</p>",
    answer=num_ans(ratio_pe, sf=4, tol=0.01),
    hints=["Compare masses, not charges.",
           "Number of electrons = (mass of a proton) ÷ (mass of an electron).",
           "Both masses are in amu, so the units cancel.",
           "1.00728 amu ÷ (5.48580 × 10<sup>−4</sup> amu) = ?"],
    solution=f"<p>1.00728 ÷ (5.48580 × 10<sup>−4</sup>) = <strong>{num(ratio_pe, 4)}</strong>, so about 1836 electrons weigh as much as one proton. "
             "That's why Thomson concluded the cathode-ray particles were “TINY” (Day 2 p.10), and why Day 2 p.12 says a hydrogen atom is about 2000 times heavier than an electron (the exact figure is about 1837).</p>",
    compare={
        "wrong": "<p>“The table lists charges of +1.60218 × 10<sup>−19</sup> C and −1.60218 × 10<sup>−19</sup> C. Their sizes are equal, so it takes 1 electron.”</p>",
        "tempting": "Charge and mass sit side by side in the table, and the charges really are equal in size.",
        "fails": "Charge and mass are different properties. Equal-and-opposite charges are why a hydrogen atom is neutral; the <em>masses</em> differ by a factor of about 1836."},
    source="Day 2 p.12, p.22")

add(id="m2-p1", module="m2", kind="practice", level="Warm-up",
    prompt="<p>In a cathode-ray tube, the beam bends toward the positively charged plate. What does that tell you about the particles in the beam?</p>",
    answer=choice(("They are positively charged.", False, "Like charges repel, so a positive beam would bend <em>away</em> from the + plate."),
                  ("They are negatively charged.", True, "Right: opposite charges attract (Day 2 p.10)."),
                  ("They are neutral.", False, "A neutral beam wouldn't bend in an electric field at all."),
                  ("They are light waves.", False, "Light isn't bent by charged plates; this beam is (Day 2 p.7).")),
    hints=["Which way do opposite charges move toward each other?"],
    solution="<p><strong>Negatively charged.</strong> The beam is attracted to the + plate (Day 2 p.7, p.10).</p>",
    source="Day 2 p.7, p.10")

add(id="m2-p2", module="m2", kind="practice", level="Standard",
    prompt="<p>Which gold-foil observation could the plum-pudding model NOT explain?</p>",
    answer=choice(("Most α particles passed straight through the foil.", False, "Both models predict that: the atom is mostly open to a fast α particle (Day 2 p.16–17)."),
                  ("A few α particles bounced back at large angles.", True, "Right: spread-out positive charge can't turn a heavy α particle around. A tiny, concentrated nucleus can (Day 2 p.15–17)."),
                  ("α particles are positively charged.", False, "That's a property of the α particle, not something the foil experiment revealed."),
                  ("The gold foil was very thin.", False, "That's part of the setup, not an observation that tests a model.")),
    hints=["Compare the predicted paths in the plum-pudding picture (Day 2 p.16) with the nuclear picture (Day 2 p.17).",
           "Which result is the “15-inch shell … came back and hit you” surprise (Day 2 p.15)?"],
    solution="<p><strong>The few large-angle bounce-backs.</strong> In the plum-pudding atom every α path goes nearly straight through (Day 2 p.16). A bounce-back requires a tiny, dense, positive nucleus (Day 2 p.17–19).</p>",
    source="Day 2 p.15–19")

scale_m = (288 / 0.01) * 1.0e-2
add(id="m2-p3", module="m2", kind="practice", level="Standard",
    prompt="<p>In the Day 2 p.20 figure, a gold atom is about 288 pm across and its nucleus about 0.01 pm. If the nucleus were enlarged to the size of a 1.0 cm marble, about how wide would the atom be, in meters?</p>",
    answer=num_ans(scale_m, sf=1, unit_label="m", tol=0.05),
    hints=["This is a scale (ratio) problem, so keep the ratio of the two sizes the same.",
           "Atom ÷ nucleus = 288 pm ÷ 0.01 pm.",
           "Multiply that ratio by the new nucleus size, 1.0 cm.",
           "288 ÷ 0.01 = 28,800, so the atom would be 28,800 cm. Now convert to meters."],
    solution=f"<p>288 pm ÷ 0.01 pm ≈ 2.9 × 10<sup>4</sup>, so the atom is about 28,800 cm ≈ <strong>{num(scale_m, 3)} m</strong> across. That's roughly three football fields around a marble. "
             "With 0.01 pm known to only one significant figure, “about 3 × 10<sup>2</sup> m” is the honest answer.</p>"
             "<p class='note'>The sources disagree slightly: Day 2 p.19 says the nucleus is “about 1/10,000” the size of the atom, while the figure's numbers give about 1/29,000. Both are order-of-magnitude statements (~10<sup>−4</sup>).</p>",
    source="Day 2 p.19–20")

add(id="m2-p4", module="m2", kind="practice", level="Standard",
    prompt="<p><span class='tag-ramp'>RAMP UP (self-study)</span> A neutral carbon-13 atom (<sup>13</sup>C) has how many protons, neutrons, and electrons?</p>",
    answer={"type": "multi", "parts": [
        {"label": "protons", **num_ans(6, tol=0)},
        {"label": "neutrons", **num_ans(7, tol=0)},
        {"label": "electrons", **num_ans(6, tol=0)}]},
    hints=["An element's identity is set by its number of protons (Day 2 p.24). Carbon is element 6.",
           "The mass number, 13, counts protons + neutrons.",
           "Neutrons = 13 − 6.",
           "A neutral atom has as many electrons as protons."],
    solution="<p><strong>6 protons, 7 neutrons, 6 electrons.</strong> <sup>13</sup>C is an isotope of carbon with one “extra” neutron compared with <sup>12</sup>C (Day 2 p.23).</p>",
    source="Day 2 p.23–24 (RAMP UP)")

add(id="m2-transfer", module="m2", kind="transfer", level="Transfer",
    prompt="<p>In a modified Thomson-style tube, a beam bends toward the <em>negative</em> plate. At the same speed, it takes a much stronger magnet to bend this beam than to bend cathode rays. What can you conclude about the particles?</p>",
    answer=choice(("Negative and lighter than electrons", False, "A negative beam would bend toward the + plate."),
                  ("Positive and much more massive per unit charge than electrons", True, "Right: attraction to the − plate means positive charge, and resisting the magnet means more mass per unit of charge."),
                  ("Neutral", False, "Neutral particles wouldn't bend toward either plate."),
                  ("Positive and lighter than electrons", False, "Lighter particles would be easier to bend, not harder.")),
    hints=["First use the direction of the bend to find the sign of the charge.",
           "Then think about what makes a moving particle harder to deflect."],
    solution="<p>They're <strong>positively charged</strong> (attracted to the − plate) and <strong>much heavier per unit charge</strong> than electrons (harder to bend). "
             "This reverses Thomson's reasoning on Day 2 p.10.</p><p class='bg'>Beams like this are positive ions, historically called “canal rays.”</p>",
    source="Day 2 p.10")

add(id="m2-m-explain", module="m2", kind="mastery", level="Explain",
    prompt="<p>Explain why most α particles went straight through the gold foil but a few bounced back.</p>",
    answer={"type": "self", "model": "<p>The atom is mostly empty space: a diffuse cloud of very light electrons that can't deflect a heavy α particle. "
                                     "Nearly all the mass and all the positive charge sit in a tiny nucleus, roughly 10<sup>−4</sup> of the atom's width (Day 2 p.19–20). "
                                     "Most α particles never pass near a nucleus. The rare one headed almost straight at a nucleus feels an enormous repulsion and is thrown back (Day 2 p.15–18).</p>"},
    hints=[], solution="", source="Day 2 p.15–20")

add(id="m2-m-match", module="m2", kind="mastery", level="Recognize",
    prompt="<p>Match each experiment to what it revealed.</p>",
    answer={"type": "match",
            "rows": [{"html": "Thomson's cathode-ray tube (1897)", "answer": "e"},
                     {"html": "Millikan's oil drops (1909)", "answer": "q"},
                     {"html": "Rutherford's gold foil (1911)", "answer": "n"}],
            "options": [{"key": "e", "html": "Atoms contain tiny negative particles"},
                        {"key": "q", "html": "The electron's charge (and mass)"},
                        {"key": "n", "html": "A tiny, massive, positive nucleus"}]},
    hints=["Day 2 p.12 and p.14 list the three experiments in order."],
    solution="<p>Thomson → tiny negative particles in all atoms (Day 2 p.10). Millikan → the electron's charge and mass, q<sub>e</sub> = −1.602 × 10<sup>−19</sup> C (Day 2 p.12). Rutherford → the nucleus (Day 2 p.14).</p>"
             "<p class='bg'>Strictly, the oil drops measured the charge; combining it with Thomson's charge-to-mass ratio gave the mass.</p>",
    source="Day 2 p.10–14")

add(id="m2-m-sanity", module="m2", kind="mastery", level="Sanity check",
    prompt="<p>A classmate says the α particles that bounced back must have hit electrons. What's wrong with that?</p>",
    answer=choice(("Nothing; electrons are what the α particles hit most.", False, "Electrons are far too light to reverse a heavy α particle."),
                  ("Electrons are about 1/1836 of a proton's mass, far too light to turn a heavy α particle around.", True, "Right: only the massive, positive nucleus can do that (Day 2 p.12, p.22)."),
                  ("Electrons are positively charged, so they'd attract α particles.", False, "Electrons are negative (Day 2 p.10)."),
                  ("Electrons are outside the atom.", False, "Electrons are inside the atom, in a diffuse cloud (Day 2 p.17).")),
    hints=["Compare the electron's mass with the proton's (Day 2 p.22)."],
    solution="<p>An electron has about 1/1836 of a proton's mass (Day 2 p.22). It can't reverse a heavy α particle; only the massive nucleus can.</p>",
    source="Day 2 p.12, p.22")

# =====================================================================================
# m3  Light  (Day 2 p.25–30; Day 3 p.12, p.17; Day 4 p.10)
# =====================================================================================
lam = 530e-9
nu530 = C / lam
E530 = H * nu530
add(id="m3-attempt", module="m3", kind="attempt", level="Guided attempt",
    prompt="<p>Green light has a wavelength λ = 5.30 × 10<sup>2</sup> nm. Find (a) its frequency and (b) the energy of one photon.</p>",
    answer={"type": "multi", "parts": [
        {"label": "(a) frequency ν", **num_ans(nu530, sf=3, unit_label="s<sup>−1</sup>", units=FREQ_UNITS, ask_unit=True)},
        {"label": "(b) photon energy E", **num_ans(E530, sf=3, unit_label="J", units=J_UNITS, ask_unit=True)}]},
    hints=["Light: wavelength ↔ frequency through c; photon energy through h (Day 2 p.30; Day 3 p.17).",
           "λν = c, so ν = c/λ. Then E = hν.",
           "Convert λ to meters first: 5.30 × 10<sup>2</sup> nm × (10<sup>−9</sup> m / 1 nm) = 5.30 × 10<sup>−7</sup> m.",
           "ν = (2.998 × 10<sup>8</sup> m/s) ÷ (5.30 × 10<sup>−7</sup> m); E = (6.626 × 10<sup>−34</sup> J·s) × ν."],
    solution=f"<p>ν = c/λ = (2.998 × 10<sup>8</sup> m/s) ÷ (5.30 × 10<sup>−7</sup> m) = <strong>{sci(nu530)} s<sup>−1</sup></strong>.</p>"
             f"<p>E = hν = (6.626 × 10<sup>−34</sup> J·s)({sci(nu530)} s<sup>−1</sup>) = <strong>{sci(E530)} J</strong> per photon.</p>"
             "<p>Units: m/s ÷ m = s<sup>−1</sup>; J·s × s<sup>−1</sup> = J. Three significant figures, set by 5.30 × 10<sup>2</sup> nm. "
             "Sanity check: visible light sits near 10<sup>14</sup>–10<sup>15</sup> Hz on the spectrum (Day 2 p.29), and this value does.</p>",
    compare={
        "wrong": f"<p>“ν = 2.998 × 10<sup>8</sup> ÷ 530 = {sci(C / 530)} s<sup>−1</sup>.”</p>",
        "tempting": "The wavelength is given in nm, and it's easy to plug the number straight in.",
        "fails": "c is in m/s, so λ must be in meters. 5.66 × 10<sup>5</sup> Hz is a radio frequency on the Day 2 p.29 spectrum, not green light. A unit mismatch shows up as an impossible region."},
    source="Day 2 p.30; Day 3 p.17")

add(id="m3-p1", module="m3", kind="practice", level="Warm-up",
    prompt="<p>Rank these from <strong>highest</strong> photon energy (1) to <strong>lowest</strong> (5).</p>",
    answer={"type": "order", "direction": "highest energy (1) to lowest (5)",
            "items": [{"key": "mw", "html": "microwaves"}, {"key": "red", "html": "red light"},
                      {"key": "uv", "html": "ultraviolet"}, {"key": "gam", "html": "γ rays"},
                      {"key": "ir", "html": "infrared"}],
            "answerOrder": ["gam", "uv", "red", "ir", "mw"]},
    hints=["Energy per photon rises with frequency and falls with wavelength: E = hν = hc/λ.",
           "The spectrum on Day 2 p.29 runs from “Shortest wavelength (Highest energy)” (γ rays) to “Longest wavelength (Lowest energy)” (radio)."],
    solution="<p><strong>γ rays > ultraviolet > red light > infrared > microwaves.</strong> Shorter wavelength means higher frequency, which means more energy per photon (Day 2 p.29).</p>",
    source="Day 2 p.28–29")

lam_fm = C / 98.5e6
add(id="m3-p2", module="m3", kind="practice", level="Standard",
    prompt="<p>An FM radio station broadcasts at 98.5 MHz (1 MHz = 10<sup>6</sup> s<sup>−1</sup>). What is the wavelength?</p>",
    answer=num_ans(lam_fm, sf=3, unit_label="m", units=M_UNITS),
    hints=["Frequency to wavelength for light (any EM radiation): λν = c.",
           "λ = c/ν.",
           "ν = 98.5 × 10<sup>6</sup> s<sup>−1</sup> = 9.85 × 10<sup>7</sup> s<sup>−1</sup>.",
           "λ = (2.998 × 10<sup>8</sup> m/s) ÷ (9.85 × 10<sup>7</sup> s<sup>−1</sup>)."],
    solution=f"<p>λ = c/ν = (2.998 × 10<sup>8</sup> m/s) ÷ (9.85 × 10<sup>7</sup> s<sup>−1</sup>) = <strong>{num(lam_fm, 3)} m</strong>, radio waves a few meters long, consistent with the “Radio” band on Day 2 p.29.</p>",
    source="Day 2 p.29–30")

lam_441 = nm_from_energy(4.41e-19)
add(id="m3-p3", module="m3", kind="practice", level="Standard",
    prompt="<p>A photon carries 4.41 × 10<sup>−19</sup> J. What is its wavelength in nanometers, and what color is it?</p>",
    answer=num_ans(lam_441, sf=3, unit_label="nm", units=NM_UNITS),
    hints=["Energy of one photon ↔ wavelength.",
           "E = hc/λ, so λ = hc/E.",
           "λ = (6.626 × 10<sup>−34</sup> J·s)(2.998 × 10<sup>8</sup> m/s) ÷ (4.41 × 10<sup>−19</sup> J), in meters.",
           "Convert meters to nm by dividing by 10<sup>−9</sup> m/nm."],
    solution=f"<p>λ = hc/E = (1.986 × 10<sup>−25</sup> J·m) ÷ (4.41 × 10<sup>−19</sup> J) = {sci(lam_441 * 1e-9)} m = <strong>{num(lam_441, 3)} nm</strong>. That's blue on the visible scale (Day 2 p.29 shows 450 nm as blue).</p>",
    source="Day 2 p.29–30; Day 4 p.10")

add(id="m3-p4", module="m3", kind="practice", level="Standard",
    prompt="<p>If you double the wavelength of light, what happens to its frequency and to the energy of each photon?</p>",
    answer=choice(("Both double.", False, "λν = c is fixed, so if λ goes up, ν must go down."),
                  ("Both are halved.", True, "Right: ν = c/λ halves, and E = hν halves with it."),
                  ("Frequency halves, but energy doubles.", False, "E = hν, so energy follows frequency, not wavelength."),
                  ("Nothing changes, because light always travels at c.", False, "The speed stays c. That's exactly why ν must change when λ does.")),
    hints=["Hold c fixed in λν = c.", "Energy follows frequency: E = hν."],
    solution="<p><strong>Both halve.</strong> c is constant, so ν = c/λ drops by half, and E = hν drops by half too.</p>",
    source="Day 2 p.30")

E_mw = H * 2.45e9
E_uv = photon_energy_from_nm(250.0)
n_ratio = E_uv / E_mw
add(id="m3-transfer", module="m3", kind="transfer", level="Transfer",
    prompt="<p>A microwave oven uses 2.45 GHz radiation (2.45 × 10<sup>9</sup> s<sup>−1</sup>). How many microwave photons carry the same total energy as <em>one</em> ultraviolet photon of wavelength 2.50 × 10<sup>2</sup> nm?</p>",
    answer=num_ans(n_ratio, sf=3),
    hints=["You need the energy of one photon of each kind.",
           "Microwave: E = hν. UV: E = hc/λ.",
           f"E<sub>microwave</sub> = (6.626 × 10<sup>−34</sup>)(2.45 × 10<sup>9</sup>) J; E<sub>UV</sub> = (6.626 × 10<sup>−34</sup>)(2.998 × 10<sup>8</sup>) ÷ (2.50 × 10<sup>−7</sup>) J.",
           "Number of microwave photons = E<sub>UV</sub> ÷ E<sub>microwave</sub>."],
    solution=f"<p>E<sub>microwave</sub> = {sci(E_mw)} J; E<sub>UV</sub> = {sci(E_uv)} J. Ratio = <strong>{sci(n_ratio)}</strong>: nearly half a million microwave photons to match one UV photon.</p>"
             "<p class='bg'>That's why microwaves warm food by sheer number of photons, while a single UV photon carries enough energy to do chemistry, even to damage molecules.</p>",
    source="Day 2 p.30; Day 3 p.17")

add(id="m3-m-explain", module="m3", kind="mastery", level="Explain",
    prompt="<p>Explain why wavelength and frequency are inversely related for light.</p>",
    answer={"type": "self", "model": "<p>Every electromagnetic wave travels at the same speed, c. Frequency counts how many crests pass a point each second, and wavelength is the distance between crests. "
                                     "So crests per second × meters per crest = meters per second: λν = c (Day 2 p.30). With c fixed, a longer wavelength must mean fewer crests per second.</p>"},
    hints=[], solution="", source="Day 2 p.30")

E_red = 3.00e-19
add(id="m3-m-recognize", module="m3", kind="mastery", level="Recognize",
    prompt="<p>“A laser emits photons that each carry 3.00 × 10<sup>−19</sup> J. What color is the laser?” Which relationship do you need first?</p>",
    answer=choice(("E = hc/λ, to get λ, then read the color off the spectrum", True, f"Right: λ = hc/E = {num(nm_from_energy(E_red), 3)} nm, which is red."),
                  ("λ = h/(mu)", False, "That's the de Broglie wavelength of a moving mass. A photon's energy uses E = hc/λ."),
                  ("KE = hν − φ", False, "No metal or ejected electron is involved."),
                  ("ΔE = −2.178 × 10<sup>−18</sup> J (1/n<sub>f</sub><sup>2</sup> − 1/n<sub>i</sub><sup>2</sup>)", False, "No hydrogen energy levels are involved.")),
    hints=["What object carries the energy: a photon, an electron in a metal, a hydrogen atom, or a moving mass?"],
    solution=f"<p>A photon's energy ↔ wavelength: E = hc/λ gives λ = {num(nm_from_energy(E_red), 3)} nm, which is red light (Day 2 p.29).</p>",
    source="Day 2 p.29–30; Day 4 p.10")

add(id="m3-m-sanity", module="m3", kind="mastery", level="Sanity check",
    prompt="<p>A student calculates that green light (530 nm) has a frequency of 5.66 × 10<sup>5</sup> Hz. What is the most likely error?</p>",
    answer=choice(("Wrong value of c", False, "Even a slightly different c wouldn't cause a 10<sup>9</sup> error."),
                  ("Wavelength left in nm instead of converted to m", True, "Right: that's off by exactly 10<sup>9</sup>. Visible light is about 10<sup>14</sup>–10<sup>15</sup> Hz."),
                  ("Used E = hν instead of λν = c", False, "The result is a frequency, so the student did use λν = c, just with the wrong units."),
                  ("Nothing; that's a reasonable visible frequency", False, "Day 2 p.29 puts visible light near 10<sup>14</sup>–10<sup>15</sup> Hz.")),
    hints=["Compare the answer with the frequency scale on the Day 2 p.29 spectrum."],
    solution="<p>The wavelength was left in nm. 5.66 × 10<sup>5</sup> × 10<sup>9</sup> = 5.66 × 10<sup>14</sup> Hz is the right value.</p>",
    source="Day 2 p.29–30")

# =====================================================================================
# m4  Atomic spectra  (Day 2 p.31; Day 3 p.7–11)
# =====================================================================================
add(id="m4-attempt", module="m4", kind="attempt", level="Guided attempt",
    prompt="<p>A star's spectrum is a continuous rainbow crossed by dark lines at 656, 486, 434, and 410 nm. What can you conclude?</p>",
    answer=choice(("The star emits light only at those four wavelengths.", False, "That describes an emission spectrum: bright lines on black. Here the lines are dark."),
                  ("Hydrogen atoms in the star's outer layers absorb those wavelengths.", True, "Right: dark lines on a continuous background mean absorption, and 656/486/434/410 nm are hydrogen's lines (Day 3 p.9–10)."),
                  ("The star contains no hydrogen.", False, "Those are exactly hydrogen's wavelengths; the dark lines are hydrogen <em>absorbing</em>."),
                  ("The dark lines are an artifact of the prism.", False, "Wollaston and Fraunhofer saw the same lines with different instruments (Day 2 p.31).")),
    hints=["Start with the kind of spectrum: an unbroken rainbow, bright lines on black, or a rainbow crossed by dark lines?",
           "Dark lines on a continuous background mean light is missing at specific wavelengths: the <strong>absence</strong> of light (Day 2 p.31). Something between the source and you absorbed it.",
           "Which element has lines at 656, 486, 434, and 410 nm? Compare with the emission spectra on Day 3 p.9.",
           "Those are hydrogen's four visible lines, and an element absorbs at the same wavelengths it emits (Day 3 p.10). So what is doing the absorbing, and where?"],
    solution="<p>The sun-like star emits a continuous spectrum, and hydrogen atoms in its atmosphere absorb specific wavelengths. That's the Kirchhoff explanation of Wollaston's dark lines (Day 3 p.10). "
             "The four wavelengths match hydrogen's four visible emission lines (Day 3 p.9).</p>",
    compare={
        "wrong": "<p>“Those four numbers are hydrogen's emission lines, so this is hydrogen's emission spectrum.”</p>",
        "tempting": "The wavelengths match hydrogen's emission lines exactly.",
        "fails": "Emission appears as bright lines on a dark background. A continuous rainbow with dark gaps is an absorption spectrum. Same element, same wavelengths, opposite appearance (Day 3 p.8–10)."},
    source="Day 2 p.31; Day 3 p.9–10")

add(id="m4-p1", module="m4", kind="practice", level="Warm-up",
    prompt="<p>Match each description to the type of spectrum.</p>",
    answer={"type": "match",
            "rows": [{"html": "A few bright colored lines on a black background", "answer": "em"},
                     {"html": "A complete rainbow with narrow black gaps", "answer": "ab"},
                     {"html": "A complete rainbow with no gaps (a glowing hot solid)", "answer": "co"}],
            "options": [{"key": "em", "html": "emission"}, {"key": "ab", "html": "absorption"}, {"key": "co", "html": "continuous"}]},
    hints=["Bunsen and Kirchhoff's flames gave “very incomplete spectra with a few lines” (Day 3 p.8); white light through a sample gave rainbows “with characteristic gaps” (Day 3 p.10)."],
    solution="<p>Bright lines = <strong>emission</strong>; rainbow with gaps = <strong>absorption</strong>; unbroken rainbow = <strong>continuous</strong> (a hot solid, like the heated metal on Day 3 p.12).</p>",
    source="Day 3 p.8–12")

add(id="m4-p2", module="m4", kind="practice", level="Standard",
    prompt="<p>Why were line spectra a problem for the physics of the early 1800s?</p>",
    answer=choice(("The lines were too faint to measure.", False, "Fraunhofer measured them precisely (Day 3 p.7)."),
                  ("Existing theories couldn't explain WHY each element emits and absorbs only specific wavelengths.", True, "Right: that's “The Limits of Classical Physics” (Day 3 p.11)."),
                  ("Prisms couldn't separate the colors.", False, "Prisms separated them fine; that's how the lines were found."),
                  ("Every element had the same lines.", False, "The opposite: each element has its own set (Day 3 p.9).")),
    hints=["See the “Limits of Classical Physics” slide (Day 3 p.11)."],
    solution="<p>Classical physics could describe the lines but not explain <em>why</em> an element emits and absorbs only certain wavelengths (Day 3 p.11). Quantization, starting with Planck, was the way out.</p>",
    source="Day 3 p.11")

add(id="m4-p3", module="m4", kind="practice", level="Standard",
    prompt="<p>Hot hydrogen gas emits bright lines at 656, 486, 434, and 410 nm. White light is now passed through <em>cold</em> hydrogen gas and into a prism. Where do dark lines appear?</p>",
    answer=choice(("At the same four wavelengths", True, "Right: the absorption and emission lines of an element coincide (Day 3 p.10 overlays them)."),
                  ("At four different wavelengths, shifted toward the red", False, "Day 3 p.10 draws hydrogen's emission lines exactly on top of its dark absorption lines."),
                  ("Nowhere; cold gas doesn't absorb light", False, "Absorption is how Kirchhoff explained the dark lines in sunlight (Day 3 p.10)."),
                  ("Everywhere except those four wavelengths", False, "That would be an emission spectrum seen in reverse; absorption removes only specific wavelengths.")),
    hints=["Look at the Day 3 p.10 figure, where hydrogen's emission lines are drawn over its absorption spectrum.",
           "What does the atom need in order to absorb a photon, and is that any different from what it gives off when it emits?"],
    solution="<p><strong>At the same four wavelengths.</strong> An element absorbs exactly the wavelengths it can emit, so its dark absorption lines sit where its bright emission lines would be (Day 3 p.10).</p>",
    source="Day 3 p.9–10")

E486 = photon_energy_from_nm(486.0)
add(id="m4-p4", module="m4", kind="practice", level="Connection",
    prompt="<p><span class='tag-conn'>Connects to Module 3</span> One of hydrogen's visible lines is at 486 nm. What is the energy of one photon of that light?</p>",
    answer=num_ans(E486, sf=3, unit_label="J", units=J_UNITS),
    hints=["Each line is light of one wavelength, so each line is photons of one energy.",
           "E = hc/λ (Day 2 p.30; Day 4 p.10).",
           "Convert first: 486 nm = 4.86 × 10<sup>−7</sup> m.",
           "E = (6.626 × 10<sup>−34</sup> J·s)(2.998 × 10<sup>8</sup> m/s) ÷ (4.86 × 10<sup>−7</sup> m)."],
    solution=f"<p>E = hc/λ = (1.986 × 10<sup>−25</sup> J·m) ÷ (4.86 × 10<sup>−7</sup> m) = <strong>{sci(E486)} J</strong>.</p>"
             "<p class='connection'>A line spectrum means hydrogen can only emit or absorb a few specific photon energies. Explaining <em>why</em> is exactly what the Bohr model does (Module 6, Day 4 p.10).</p>",
    source="Day 3 p.9; Day 2 p.30")

add(id="m4-transfer", module="m4", kind="transfer", level="Transfer",
    prompt="<p>A glowing gas in a discharge tube shows bright lines at exactly the wavelengths where cold neon gas absorbs light. What's the best conclusion?</p>",
    answer=choice(("The glowing gas is neon.", True, "Right: an element emits and absorbs at the same wavelengths, so matching lines identify it."),
                  ("The glowing gas is hydrogen, because all glowing gases emit hydrogen lines.", False, "Each element has its own line pattern (Day 3 p.9)."),
                  ("Nothing; emission and absorption lines of one element never match.", False, "They do match. Day 3 p.10 overlays hydrogen's emission and absorption lines."),
                  ("The gas must be a mixture of every element.", False, "One element's pattern accounts for the lines.")),
    hints=["What does Day 3 p.10 show about the positions of emission vs. absorption lines of the same element?"],
    solution="<p>Line positions are an element's fingerprint, and emission and absorption lines coincide (Day 3 p.10). So the glowing gas is neon.</p>"
             "<p class='bg'>A cold gas absorbs mainly from its lowest energy level, so it shows fewer lines than the glowing gas emits, but every absorption line sits at one of the element's emission wavelengths.</p>",
    source="Day 3 p.9–10")

add(id="m4-m-explain", module="m4", kind="mastery", level="Explain",
    prompt="<p>Why do an element's absorption lines appear at the same wavelengths as its emission lines?</p>",
    answer={"type": "self", "model": "<p>Both involve the same allowed energy changes of the atom's electrons. Absorbing a photon lifts an electron up by one allowed gap; emitting a photon drops it down by the same gap. "
                                     "The photon's energy, and therefore its wavelength, equals that gap either way. (Bohr's model makes this explicit on Day 4 p.10; on Day 3 it was an unexplained observation, p.11.)</p>"},
    hints=[], solution="", source="Day 3 p.10–11; Day 4 p.10")

add(id="m4-m-sanity", module="m4", kind="mastery", level="Sanity check",
    prompt="<p>A student says the dark Fraunhofer lines prove the sun doesn't produce those wavelengths at all. What's the better explanation?</p>",
    answer=choice(("The sun produces a continuous spectrum, and elements in its atmosphere absorb those wavelengths.", True, "Right: that's the partial explanation on Day 3 p.10."),
                  ("The lines come from Earth's clouds.", False, "The lecture attributes them to absorption by elements in the solar atmosphere."),
                  ("The student is right.", False, "Kirchhoff's absorption experiments showed the gaps come from absorption (Day 3 p.10)."),
                  ("The lines are wavelengths the prism can't bend.", False, "Prisms bend all visible wavelengths.")),
    hints=["Day 3 p.10: “light is emitted continuously by the sun, but …”"],
    solution="<p>“Light is emitted continuously by the sun, but is absorbed by elements in the solar atmosphere” (Day 3 p.10).</p>",
    source="Day 3 p.10")

# =====================================================================================
# m5  Quantization: Planck & the photoelectric effect  (Day 3 p.11–19)
# =====================================================================================
E220 = photon_energy_from_nm(220.0)
phi_a = 7.18e-19
KE_a = E220 - phi_a
add(id="m5-attempt", module="m5", kind="attempt", level="Guided attempt",
    prompt="<p>Ultraviolet light with λ = 2.20 × 10<sup>2</sup> nm shines on a metal whose threshold energy (work function) is φ = 7.18 × 10<sup>−19</sup> J. "
           "Is an electron ejected? If so, what is its kinetic energy?</p>",
    answer=num_ans(KE_a, sf=3, unit_label="J", units=J_UNITS, ask_unit=True),
    hints=["Light ejecting electrons from a metal is the photoelectric effect: KE = hν − φ (Day 3 p.19).",
           "Find the photon's energy, E = hc/λ, and compare it with φ.",
           "E = (6.626 × 10<sup>−34</sup> J·s)(2.998 × 10<sup>8</sup> m/s) ÷ (2.20 × 10<sup>−7</sup> m).",
           "If E > φ, then KE = E − 7.18 × 10<sup>−19</sup> J."],
    solution=f"<p>E = hc/λ = (1.986 × 10<sup>−25</sup> J·m) ÷ (2.20 × 10<sup>−7</sup> m) = {sci(E220)} J. That's larger than φ, so yes, an electron is ejected.</p>"
             f"<p>KE = hν − φ = {sci(E220)} J − 7.18 × 10<sup>−19</sup> J = <strong>{sci(KE_a)} J</strong>.</p>"
             "<p>Sig figs: in units of 10<sup>−19</sup> J this is 9.03 − 7.18 = 1.85, and subtraction keeps two decimal places, so 3 significant figures here.</p>",
    compare={
        "wrong": f"<p>“KE = hν + φ = {sci(E220 + phi_a)} J. Also, a brighter lamp would make the electrons faster.”</p>",
        "tempting": "Adding feels natural (“the metal contributes energy”), and brighter light <em>feels</em> more energetic.",
        "fails": "φ is the energy <em>spent</em> to free the electron; only the excess becomes kinetic energy (Day 3 p.19). Brightness means more photons, not more energy per photon, so it changes how many electrons are ejected, not how fast they move (Day 3 p.18)."},
    source="Day 3 p.18–19")

phi_K = 3.67e-19
nu0 = phi_K / H
lam0_nm = C / nu0 * 1e9
add(id="m5-p1", module="m5", kind="practice", level="Standard",
    prompt="<p><span class='tag-bg'>Background value</span> Potassium's work function is about φ = 3.67 × 10<sup>−19</sup> J. Find (a) the threshold frequency ν<sub>0</sub> and (b) the longest wavelength (nm) that can eject electrons.</p>",
    answer={"type": "multi", "parts": [
        {"label": "(a) ν₀", **num_ans(nu0, sf=3, unit_label="s<sup>−1</sup>", units=FREQ_UNITS)},
        {"label": "(b) longest λ", **num_ans(lam0_nm, sf=3, unit_label="nm", units=NM_UNITS)}]},
    hints=["At threshold, the photon has just enough energy: KE = 0, so hν<sub>0</sub> = φ (Day 3 p.19).",
           "ν<sub>0</sub> = φ/h; then λ<sub>0</sub> = c/ν<sub>0</sub>.",
           "ν<sub>0</sub> = (3.67 × 10<sup>−19</sup> J) ÷ (6.626 × 10<sup>−34</sup> J·s).",
           "λ<sub>0</sub> = (2.998 × 10<sup>8</sup> m/s) ÷ ν<sub>0</sub>, then convert m → nm."],
    solution=f"<p>ν<sub>0</sub> = φ/h = <strong>{sci(nu0)} s<sup>−1</sup></strong>; λ<sub>0</sub> = c/ν<sub>0</sub> = {sci(lam0_nm * 1e-9)} m = <strong>{num(lam0_nm, 3)} nm</strong> (green). "
             "Longer wavelengths, like red light, carry too little energy per photon, no matter how bright.</p>",
    source="Day 3 p.18–19")

add(id="m5-p2", module="m5", kind="practice", level="Warm-up",
    prompt="<p>Red light shining on a metal ejects no electrons. What happens if you make the red light twice as bright?</p>",
    answer=choice(("Electrons are ejected, because the total energy doubled.", False, "Energy arrives one photon at a time, and each red photon is still below threshold."),
                  ("Still no electrons.", True, "Right: Day 3 p.18 panel (c), brighter red light, still gives no current."),
                  ("Electrons are ejected with twice the kinetic energy.", False, "Nothing is ejected below threshold, so there's no kinetic energy to double."),
                  ("The metal's work function drops.", False, "φ is a property of the metal, not of the light.")),
    hints=["Does brightness change the energy of each photon, or the number of photons?"],
    solution="<p><strong>Still none.</strong> Brightness changes the number of photons, not the energy of each one. Every red photon is still below φ (Day 3 p.18).</p>",
    source="Day 3 p.18")

E400 = photon_energy_from_nm(400.0)
phi_c = E400 - 1.53e-19
add(id="m5-p3", module="m5", kind="practice", level="Standard",
    prompt="<p>Light of wavelength 4.00 × 10<sup>2</sup> nm ejects electrons from a metal with a maximum kinetic energy of 1.53 × 10<sup>−19</sup> J. What is the metal's work function φ?</p>",
    answer=num_ans(phi_c, sf=3, unit_label="J", units=J_UNITS),
    hints=["Same relationship, solved for a different unknown: KE = hν − φ.",
           "φ = hν − KE = hc/λ − KE.",
           "hc/λ = (6.626 × 10<sup>−34</sup>)(2.998 × 10<sup>8</sup>) ÷ (4.00 × 10<sup>−7</sup>) J.",
           "Subtract 1.53 × 10<sup>−19</sup> J from the photon energy."],
    solution=f"<p>hc/λ = {sci(E400)} J; φ = {sci(E400)} − 1.53 × 10<sup>−19</sup> = <strong>{sci(phi_c)} J</strong>.</p>",
    source="Day 3 p.19")

add(id="m5-p4", module="m5", kind="practice", level="Standard",
    prompt="<p>On the Day 3 p.19 graph of maximum kinetic energy vs. light frequency, the lines for different metals are parallel but shifted left or right. What does a line farther to the <em>right</em> mean?</p>",
    answer=choice(("A larger threshold frequency, so a larger work function", True, "Right: the line crosses KE = 0 at ν<sub>0</sub>, and mercury's line sits farthest right."),
                  ("A steeper slope", False, "The lines are parallel; every metal has the same slope."),
                  ("More electrons ejected", False, "The graph shows energy per electron, not how many."),
                  ("A larger value of h", False, "h is a universal constant, the same for every metal.")),
    hints=["Where does each line meet the frequency axis (KE = 0)?", "At that point hν<sub>0</sub> = φ."],
    solution="<p>A line farther right crosses KE = 0 at a higher ν<sub>0</sub>, so φ = hν<sub>0</sub> is larger. On Day 3 p.19 the order is Cs < K < Ca < Mg < Hg. "
             "<span class='connection'>The lines are parallel because the slope is h for every metal.</span></p>",
    source="Day 3 p.19")

add(id="m5-p5", module="m5", kind="practice", level="Warm-up",
    prompt="<p>One star glows red; another glows blue-white. Which is hotter?</p>",
    answer=choice(("The red star", False, "Hotter objects peak at shorter wavelengths, toward blue."),
                  ("The blue-white star", True, "Right: “red hot” → “white hot” as temperature rises (Day 3 p.12), and hotter blackbody curves peak at shorter λ (Day 3 p.13–14)."),
                  ("They're the same temperature.", False, "Color changes with temperature (Day 3 p.12)."),
                  ("You can't tell from color.", False, "For a glowing object, color tracks temperature (Day 3 p.12–14).")),
    hints=["How did the heated metal's color change as it got hotter (Day 3 p.12)?"],
    solution="<p>The <strong>blue-white</strong> star. As temperature rises, the peak of the emission curve shifts to shorter wavelengths (Day 3 p.13–14).</p>",
    source="Day 3 p.12–14")

lam_det = nm_from_energy(1.80e-19)
add(id="m5-transfer", module="m5", kind="transfer", level="Transfer",
    prompt="<p>A light detector registers a photon only if the photon carries at least 1.80 × 10<sup>−19</sup> J. What is the longest wavelength (nm) it can detect, and in which region is that?</p>",
    answer=num_ans(lam_det, sf=3, unit_label="nm", units=NM_UNITS),
    hints=["A minimum photon energy acts like a threshold, the same logic as φ.",
           "Longest wavelength ↔ smallest energy: λ<sub>max</sub> = hc/E<sub>min</sub>.",
           "λ = (1.986 × 10<sup>−25</sup> J·m) ÷ (1.80 × 10<sup>−19</sup> J).",
           "Convert to nm and locate it on the Day 2 p.29 spectrum."],
    solution=f"<p>λ<sub>max</sub> = hc/E<sub>min</sub> = {sci(lam_det * 1e-9)} m = <strong>{num(lam_det, 3)} nm</strong>, in the near infrared (past 750 nm). "
             "It detects all visible light and some infrared.</p>",
    source="Day 3 p.19; Day 2 p.29")

add(id="m5-m-explain", module="m5", kind="mastery", level="Explain",
    prompt="<p>Explain why brighter light doesn't help below the threshold frequency, but does increase the current above it.</p>",
    answer={"type": "self", "model": "<p>Light arrives as photons of energy hν (Planck, Day 3 p.17), and one photon frees at most one electron. Below threshold (hν < φ), no single photon has enough energy, so adding more of them changes nothing (Day 3 p.18 panels b and c). "
                                     "Above threshold, each photon can free an electron, so more photons (brighter light) free more electrons: more current. Each electron's kinetic energy is still set by hν − φ, not by brightness.</p>"},
    hints=[], solution="", source="Day 3 p.17–19")

add(id="m5-m-recognize", module="m5", kind="mastery", level="Recognize",
    prompt="<p>Which observation shows most directly that light's energy comes in packets?</p>",
    answer=choice(("Light travels at c = 2.998 × 10<sup>8</sup> m/s.", False, "That's true of the wave description too."),
                  ("A threshold frequency exists in the photoelectric effect, regardless of intensity.", True, "Right: energy is delivered one photon at a time (Day 3 p.18–19)."),
                  ("A prism splits sunlight into colors.", False, "That's explained by wave behavior."),
                  ("Radio waves have long wavelengths.", False, "That's a wave property.")),
    hints=["Which result can't be explained by a smooth, “ramp-like” energy supply (Day 3 p.17)?"],
    solution="<p>The <strong>threshold frequency</strong>: bright red light never ejects electrons, but dim violet light does (Day 3 p.18). Energy comes in packets of hν.</p>",
    source="Day 3 p.17–18")

add(id="m5-m-sanity", module="m5", kind="mastery", level="Sanity check",
    prompt="<p>A student calculates KE = −2.1 × 10<sup>−20</sup> J for the “ejected” electron. What does that mean?</p>",
    answer=choice(("The electron moves backward.", False, "Kinetic energy (½mu²) can't be negative."),
                  ("The photon's energy is below φ, so no electron is ejected at all.", True, "Right: a negative KE from KE = hν − φ means hν < φ."),
                  ("The light is too bright.", False, "Intensity doesn't enter KE = hν − φ."),
                  ("The metal has a negative work function.", False, "φ is always positive; it's energy that must be supplied.")),
    hints=["Can kinetic energy be negative?"],
    solution="<p>A negative answer from KE = hν − φ means hν < φ: the photon is below threshold and nothing is ejected.</p>",
    source="Day 3 p.19")

# =====================================================================================
# m6  Hydrogen spectrum & the Bohr model  (Day 3 p.21; Day 4 p.3, p.6–10)
# =====================================================================================
dE42 = bohr_dE(4, 2)
lam42 = nm_from_energy(abs(dE42))
dE_wrong = -BOHR * (1 / 2 - 1 / 4)
add(id="m6-attempt", module="m6", kind="attempt", level="Guided attempt",
    prompt="<p>Find the wavelength (nm) of the photon emitted when hydrogen's electron drops from n = 4 to n = 2.</p>",
    answer=num_ans(lam42, sf=3, unit_label="nm", units=NM_UNITS, ask_unit=True),
    hints=["Hydrogen plus energy levels: use Bohr's ΔE equation (Day 4 p.10).",
           "ΔE = −2.178 × 10<sup>−18</sup> J (1/n<sub>final</sub><sup>2</sup> − 1/n<sub>initial</sub><sup>2</sup>); the photon carries |ΔE| = hc/λ.",
           "n<sub>initial</sub> = 4, n<sub>final</sub> = 2: ΔE = −2.178 × 10<sup>−18</sup> J (1/4 − 1/16).",
           f"ΔE = {sci(dE42, 4)} J (negative: energy leaves as light). λ = hc/|ΔE| = (1.986 × 10<sup>−25</sup> J·m) ÷ ({sci(abs(dE42), 4)} J)."],
    solution=f"<p>ΔE = −2.178 × 10<sup>−18</sup> J (1/2<sup>2</sup> − 1/4<sup>2</sup>) = −2.178 × 10<sup>−18</sup> J × 0.1875 = {sci(dE42, 4)} J. "
             "The negative sign says the atom loses energy: a photon is emitted.</p>"
             f"<p>λ = hc/|ΔE| = {sci(lam42 * 1e-9, 4)} m = <strong>{num(lam42, 3)} nm</strong>, the blue-green Balmer line (Day 4 p.10; Day 3 p.9).</p>",
    compare={
        "wrong": f"<p>“ΔE = −2.178 × 10<sup>−18</sup> (1/2 − 1/4) = {sci(dE_wrong, 4)} J, so λ = {num(nm_from_energy(abs(dE_wrong)), 3)} nm.”</p>",
        "tempting": "Plugging in n rather than n² is an easy slip, and the result still looks like a reasonable wavelength.",
        "fails": "Bohr energies go as 1/n², not 1/n. The wrong result, 365 nm, is ultraviolet, but every n → 2 hydrogen line in the Balmer series is visible (Day 4 p.10). Checking the region catches the error."},
    source="Day 4 p.10")

dE52 = bohr_dE(5, 2)
lam52 = nm_from_energy(abs(dE52))
add(id="m6-p1", module="m6", kind="practice", level="Warm-up",
    prompt="<p>What wavelength (nm) is emitted when hydrogen's electron drops from n = 5 to n = 2?</p>",
    answer=num_ans(lam52, sf=3, unit_label="nm", units=NM_UNITS),
    hints=["Same method as the guided attempt.",
           "ΔE = −2.178 × 10<sup>−18</sup> J (1/2<sup>2</sup> − 1/5<sup>2</sup>).",
           "1/4 − 1/25 = 0.21.",
           "λ = hc/|ΔE|."],
    solution=f"<p>ΔE = −2.178 × 10<sup>−18</sup> × 0.21 = {sci(dE52, 4)} J; λ = hc/|ΔE| = <strong>{num(lam52, 3)} nm</strong> (violet-blue; on Day 4 p.10 the 5 → 2 arrow is drawn blue).</p>",
    source="Day 4 p.10")

dE13 = bohr_dE(1, 3)
lam13 = nm_from_energy(abs(dE13))
add(id="m6-p2", module="m6", kind="practice", level="Standard",
    prompt="<p>What wavelength (nm) must a hydrogen atom absorb to move its electron from n = 1 to n = 3?</p>",
    answer=num_ans(lam13, sf=3, unit_label="nm", units=NM_UNITS),
    hints=["Absorption uses the same equation; ΔE simply comes out positive.",
           "n<sub>initial</sub> = 1, n<sub>final</sub> = 3.",
           "ΔE = −2.178 × 10<sup>−18</sup> J (1/9 − 1/1).",
           "λ = hc/ΔE."],
    solution=f"<p>ΔE = −2.178 × 10<sup>−18</sup> J (1/9 − 1) = <strong>+</strong>{sci(dE13, 4)} J (positive: energy absorbed). λ = hc/ΔE = <strong>{num(lam13, 3)} nm</strong>, in the ultraviolet, as expected for the Lyman end of the diagram (Day 4 p.10).</p>",
    source="Day 4 p.10")

dE2inf = bohr_dE(2, math.inf)
kjmol2 = dE2inf * NA / 1000
add(id="m6-p3", module="m6", kind="practice", level="Standard",
    prompt="<p><span class='tag-preview'>Uses N<sub>A</sub> = 6.022 × 10<sup>23</sup> mol<sup>−1</sup>: textbook preview, §2.5</span> How much energy, in kJ/mol, removes the electron completely from hydrogen atoms whose electrons start in n = 2?</p>",
    answer=num_ans(kjmol2, sf=3, unit_label="kJ/mol", units=KJMOL_UNITS),
    hints=["Complete removal means n<sub>final</sub> = ∞ (the top of the Day 4 p.10 diagram).",
           "1/∞<sup>2</sup> = 0, so ΔE = −2.178 × 10<sup>−18</sup> J (0 − 1/2<sup>2</sup>).",
           "That's the energy per atom. Multiply by N<sub>A</sub> = 6.022 × 10<sup>23</sup> mol<sup>−1</sup>.",
           "Convert J/mol to kJ/mol."],
    solution=f"<p>ΔE = +2.178 × 10<sup>−18</sup> J × ¼ = {sci(dE2inf, 4)} J per atom; × 6.022 × 10<sup>23</sup> mol<sup>−1</sup> = {sci(dE2inf * NA, 4)} J/mol = <strong>{num(kjmol2, 3)} kJ/mol</strong>. "
             "That's a quarter of hydrogen's ground-state value, 1312 kJ/mol (Day 7 p.9).</p>",
    source="Day 4 p.10; Day 7 p.9")

add(id="m6-p4", module="m6", kind="practice", level="Standard",
    prompt="<p>Which transition emits the photon with the <strong>longest</strong> wavelength?</p>",
    answer=choice(("n = 2 → 1", False, f"Biggest gap of the four ({sci(abs(bohr_dE(2, 1)))} J), so the shortest wavelength."),
                  ("n = 3 → 2", False, f"Gap = {sci(abs(bohr_dE(3, 2)))} J: visible red, but not the smallest gap here."),
                  ("n = 4 → 3", True, f"Right: smallest gap ({sci(abs(bohr_dE(4, 3)))} J), so the longest λ ({num(nm_from_energy(abs(bohr_dE(4, 3))), 4)} nm, infrared: Paschen)."),
                  ("n = 6 → 2", False, "Big n-values don't mean a small gap. Levels crowd together near the top, but a drop all the way to n = 2 is large.")),
    hints=["Longest wavelength ↔ smallest energy gap.",
           "Levels get closer together as n increases (Day 4 p.10), so compare the gaps."],
    solution="<p><strong>4 → 3.</strong> The smallest energy gap gives the longest wavelength (infrared, the Paschen series on Day 4 p.10).</p>",
    source="Day 4 p.10")

add(id="m6-p5", module="m6", kind="practice", level="Warm-up",
    prompt="<p>Why can't the Bohr equation predict helium's spectrum?</p>",
    answer=choice(("Helium has no electrons.", False, "Helium has two."),
                  ("With two electrons, the electrons are correlated, and the Bohr model falls apart.", True, "Right: Day 4 p.3."),
                  ("Helium doesn't emit light.", False, "It does; Day 3 p.9 shows helium's emission spectrum."),
                  ("The Bohr constant is different for every element.", False, "Rydberg/Ritz scaling works only for one-electron atoms (Day 4 p.8); helium's two electrons interact.")),
    hints=["See the Day 4 p.3 note: the Bohr model is TRUE for one-electron atoms, but …"],
    solution="<p>The Bohr model works for hydrogen and other one-electron atoms. Once a second electron is involved, the electrons are correlated, and “the Bohr model falls apart” (Day 4 p.3).</p>",
    source="Day 4 p.3")

# transfer: identify initial level for 1282 nm landing on n = 3
E1282 = photon_energy_from_nm(1282.0)
inv_ni2 = 1 / 9 - E1282 / BOHR
ni = 1 / math.sqrt(inv_ni2)
add(id="m6-transfer", module="m6", kind="transfer", level="Transfer",
    prompt="<p>A hydrogen emission line is observed at 1282 nm (infrared). The electron lands in n = 3. From which level did it start?</p>",
    answer=num_ans(round(ni), tol=0),
    hints=["Work the Bohr equation backward: from λ, find |ΔE|, then n<sub>initial</sub>.",
           "|ΔE| = hc/λ; for emission ΔE = −|ΔE| = −2.178 × 10<sup>−18</sup> J (1/3<sup>2</sup> − 1/n<sub>i</sub><sup>2</sup>).",
           f"|ΔE| = {sci(E1282, 4)} J, so 1/9 − 1/n<sub>i</sub><sup>2</sup> = |ΔE| ÷ 2.178 × 10<sup>−18</sup> J = {fix(E1282 / BOHR, 4)}.",
           f"1/n<sub>i</sub><sup>2</sup> = 0.1111 − {fix(E1282 / BOHR, 4)} = {fix(inv_ni2, 4)}; solve for n<sub>i</sub> and round to the nearest integer."],
    solution=f"<p>|ΔE| = hc/λ = {sci(E1282, 4)} J. Then 1/n<sub>i</sub><sup>2</sup> = 1/9 − {fix(E1282 / BOHR, 4)} = {fix(inv_ni2, 4)}, so n<sub>i</sub><sup>2</sup> = {fix(1 / inv_ni2, 1)} and <strong>n<sub>i</sub> = 5</strong>. "
             "This is the 5 → 3 Paschen line, one of the infrared arrows on Day 4 p.10.</p>",
    source="Day 4 p.10")

add(id="m6-m-explain", module="m6", kind="mastery", level="Explain",
    prompt="<p>What does the negative sign in ΔE mean for an emission, and why is the photon's energy |ΔE|?</p>",
    answer={"type": "self", "model": "<p>For emission, n<sub>final</sub> < n<sub>initial</sub>, so ΔE comes out negative: the electron (the atom) loses energy. "
                                     "Energy is conserved (Day 1 p.15), so the lost energy leaves as a photon, and the photon's energy is the size of the drop, |ΔE| = hc/λ (Day 4 p.10). "
                                     "For absorption ΔE is positive, and the absorbed photon supplies exactly that amount.</p>"},
    hints=[], solution="", source="Day 4 p.10; Day 1 p.15")

add(id="m6-m-recognize", module="m6", kind="mastery", level="Recognize",
    prompt="<p>“Hydrogen gas absorbs light, and its electrons jump from n = 2 to n = 4. What wavelength was absorbed?” Which relationship(s) do you need?</p>",
    answer=choice(("λ = h/(mu)", False, "No moving mass; the absorbed light is photons."),
                  ("Bohr's ΔE equation, then E = hc/λ", True, "Right: levels → ΔE → photon wavelength (Day 4 p.10)."),
                  ("KE = hν − φ", False, "That's for electrons ejected from a metal."),
                  ("E<sub>el</sub> = 2.31 × 10<sup>−19</sup> J·nm (Q<sub>1</sub>Q<sub>2</sub>/d)", False, "That's the attraction between ions.")),
    hints=["Hydrogen + n values → which equation?"],
    solution=f"<p>ΔE = −2.178 × 10<sup>−18</sup> J (1/16 − 1/4) = +{sci(bohr_dE(2, 4))} J, then λ = hc/ΔE = {num(nm_from_energy(bohr_dE(2, 4)), 3)} nm. It's the same line as the 4 → 2 emission.</p>",
    source="Day 4 p.10")

add(id="m6-m-sanity", module="m6", kind="mastery", level="Sanity check",
    prompt="<p>A student finds that hydrogen's 3 → 2 transition emits light with λ = 6.57 × 10<sup>−9</sup> m. Is that reasonable?</p>",
    answer=choice(("Yes; it's a visible Balmer line.", False, "Visible light is 400–750 nm = 4–7.5 × 10<sup>−7</sup> m."),
                  ("No; it's off by a factor of 100. The 3 → 2 line is about 657 nm = 6.57 × 10<sup>−7</sup> m, red light.", True, "Right: an exponent slip. Balmer lines are visible (Day 4 p.10)."),
                  ("No; 3 → 2 is an absorption, so there's no photon.", False, "3 → 2 is a drop, so it's an emission."),
                  ("Yes; all hydrogen lines are X-rays.", False, "Hydrogen's lines span UV, visible, and IR (Day 4 p.10).")),
    hints=["Convert 6.57 × 10<sup>−9</sup> m to nm. Where does that fall on the Day 2 p.29 spectrum?"],
    solution="<p>6.57 × 10<sup>−9</sup> m = 6.57 nm, which is X-ray territory. The 3 → 2 line is red, about 657 nm. Always compare your answer with the series' region.</p>",
    source="Day 4 p.10; Day 2 p.29")

# =====================================================================================
# m7  Matter waves (de Broglie)  (Day 4 p.11–17)
# =====================================================================================
lam_n = de_broglie(1.675e-27, 2.20e3)
add(id="m7-attempt", module="m7", kind="attempt", level="Guided attempt",
    prompt="<p>A slow (“thermal”) neutron, m = 1.675 × 10<sup>−27</sup> kg, moves at 2.20 × 10<sup>3</sup> m/s. What is its de Broglie wavelength?</p>",
    answer=num_ans(lam_n, sf=3, unit_label="m", units=M_UNITS, ask_unit=True),
    hints=["A moving particle with mass has a wavelength: de Broglie (Day 4 p.11).",
           "λ = h/(mu), with m in kg and u in m/s.",
           "Units: J·s ÷ (kg·m/s) = (kg·m²/s²)·s ÷ (kg·m/s) = m.",
           "λ = (6.626 × 10<sup>−34</sup> J·s) ÷ [(1.675 × 10<sup>−27</sup> kg)(2.20 × 10<sup>3</sup> m/s)]."],
    solution=f"<p>λ = h/(mu) = (6.626 × 10<sup>−34</sup> J·s) ÷ [(1.675 × 10<sup>−27</sup> kg)(2.20 × 10<sup>3</sup> m/s)] = <strong>{sci(lam_n)} m</strong>, 3 s.f. set by 2.20 × 10<sup>3</sup>. "
             "That's about the size of an atom, so neutrons like this behave as waves when they meet atoms, just like the electron on Day 4 p.12.</p>",
    compare={
        "wrong": f"<p>“λ = 6.626 × 10<sup>−34</sup> ÷ (1.675 × 10<sup>−24</sup> × 2.20 × 10<sup>3</sup>) = {sci(de_broglie(1.675e-24, 2.20e3))} m”, using the mass in grams.</p>",
        "tempting": "Masses of tiny particles are often quoted in grams (Day 2 p.12 gives m<sub>e</sub> in g).",
        "fails": "h is in J·s = kg·m²/s, so mass must be in kg for the units to cancel to meters (Day 4 p.11). Mass in grams gives an answer 1000 times too small."},
    source="Day 4 p.11–12")

lam_e1 = de_broglie(ME, 1.00e6)
add(id="m7-p1", module="m7", kind="practice", level="Warm-up",
    prompt="<p>What is the de Broglie wavelength of an electron (m = 9.109 × 10<sup>−31</sup> kg) moving at 1.00 × 10<sup>6</sup> m/s?</p>",
    answer=num_ans(lam_e1, sf=3, unit_label="m", units=M_UNITS),
    hints=["λ = h/(mu).", "The mass is already in kg.", "Multiply m × u first.", "λ = 6.626 × 10<sup>−34</sup> ÷ (9.109 × 10<sup>−31</sup> × 1.00 × 10<sup>6</sup>)."],
    solution=f"<p>λ = <strong>{sci(lam_e1)} m</strong>, several atoms wide. That's why electron beams diffract like X-rays (Day 4 p.17).</p>",
    source="Day 4 p.11–12, p.17")

u_e = H / (ME * 1.00e-10)
add(id="m7-p2", module="m7", kind="practice", level="Standard",
    prompt="<p>How fast must an electron move to have a de Broglie wavelength of 0.100 nm?</p>",
    answer=num_ans(u_e, sf=3, unit_label="m/s", units=MS_UNITS),
    hints=["Rearrange λ = h/(mu) to solve for u.", "u = h/(mλ).", "0.100 nm = 1.00 × 10<sup>−10</sup> m.", "u = 6.626 × 10<sup>−34</sup> ÷ (9.109 × 10<sup>−31</sup> × 1.00 × 10<sup>−10</sup>)."],
    solution=f"<p>u = h/(mλ) = <strong>{sci(u_e)} m/s</strong>, about 2% of the speed of light.</p>",
    source="Day 4 p.11")

lam_t = de_broglie(0.0570, 50.0)
add(id="m7-p3", module="m7", kind="practice", level="Standard",
    prompt="<p>A tennis ball (57.0 g) is served at 50.0 m/s. What is its de Broglie wavelength?</p>",
    answer=num_ans(lam_t, sf=3, unit_label="m", units=M_UNITS),
    hints=["Same equation as the baseball on Day 4 p.14.", "Convert 57.0 g to kg first.", "57.0 g = 0.0570 kg.", "λ = 6.626 × 10<sup>−34</sup> ÷ (0.0570 × 50.0)."],
    solution=f"<p>λ = <strong>{sci(lam_t)} m</strong>, about 10<sup>32</sup> times smaller than the ball itself, so no wave behavior is ever noticeable (compare the baseball, 1.06 × 10<sup>−34</sup> m, Day 4 p.14).</p>",
    source="Day 4 p.14")

add(id="m7-p4", module="m7", kind="practice", level="Warm-up",
    prompt="<p>All moving at the same speed, which has the <strong>longest</strong> de Broglie wavelength?</p>",
    answer=choice(("an electron", True, "Right: λ = h/(mu), so the smallest mass gives the longest λ."),
                  ("a proton", False, "About 1836 times heavier than an electron (Day 2 p.22), so its λ is shorter."),
                  ("a helium atom", False, "Heavier still."),
                  ("a baseball", False, "By far the heaviest, so by far the shortest λ.")),
    hints=["At fixed u, λ is inversely proportional to m."],
    solution="<p>The <strong>electron</strong>: λ ∝ 1/m at the same speed.</p>",
    source="Day 4 p.11")

add(id="m7-p5", module="m7", kind="practice", level="Standard",
    prompt="<p>According to de Broglie's picture, which of these could be a stable orbit around the nucleus?</p>",
    answer=choice(("One where 2.25 wavelengths fit around the circumference", False, "A non-integer number of waves doesn't close on itself (the n = 2¼ picture, Day 4 p.16)."),
                  ("One where exactly 3 wavelengths fit around the circumference", True, "Right: a whole number of wavelengths makes a standing wave that closes (Day 4 p.15–16)."),
                  ("One where 3.5 wavelengths fit around the circumference", False, "Not a whole number, so the wave interferes with itself."),
                  ("Any orbit, as long as the electron moves fast enough", False, "de Broglie's point is that only whole-number orbits work.")),
    hints=["Day 4 p.15: an electron can only exist in an orbit if there is “an integer number of de Broglie wavelengths in the circumference.”"],
    solution="<p>Only a whole number of wavelengths (here 3) makes a wave that closes smoothly on itself. That gave Bohr's n a physical meaning (Day 4 p.16).</p>",
    source="Day 4 p.15–16")

ratio_up = MP_KG / 9.10938e-31
add(id="m7-transfer", module="m7", kind="transfer", level="Transfer",
    prompt="<p>An electron and a proton have the same de Broglie wavelength. How many times faster is the electron moving? Use the masses in kg from Day 2 p.22.</p>",
    answer=num_ans(ratio_up, sf=4),
    hints=["Same λ means h/(m<sub>e</sub>u<sub>e</sub>) = h/(m<sub>p</sub>u<sub>p</sub>).",
           "So m<sub>e</sub>u<sub>e</sub> = m<sub>p</sub>u<sub>p</sub>.",
           "u<sub>e</sub>/u<sub>p</sub> = m<sub>p</sub>/m<sub>e</sub>.",
           "m<sub>p</sub> = 1.67262 × 10<sup>−27</sup> kg; m<sub>e</sub> = 9.10938 × 10<sup>−31</sup> kg."],
    solution=f"<p>u<sub>e</sub>/u<sub>p</sub> = m<sub>p</sub>/m<sub>e</sub> = <strong>{num(ratio_up, 4)}</strong>. Equal wavelength means equal momentum (mu), so the lighter particle must move about 1836 times faster.</p>",
    source="Day 4 p.11; Day 2 p.22")

add(id="m7-m-explain", module="m7", kind="mastery", level="Explain",
    prompt="<p>Why don't we ever notice the wave nature of a baseball?</p>",
    answer={"type": "self", "model": "<p>Its de Broglie wavelength is about 10<sup>−34</sup> m (Day 4 p.14), unimaginably smaller than the ball or anything it interacts with. "
                                     "Wave behavior matters only when λ is comparable to the size of the object or of what it passes through (Day 4 p.11). An electron's λ (~10<sup>−10</sup> m) matches the size of atoms, so it behaves as a wave there.</p>"},
    hints=[], solution="", source="Day 4 p.11–14")

add(id="m7-m-recognize", module="m7", kind="mastery", level="Recognize",
    prompt="<p>“Find the wavelength of an α particle moving at 1.5 × 10<sup>7</sup> m/s.” Which equation?</p>",
    answer=choice(("E = hc/λ", False, "That's for photons. An α particle has mass and speed."),
                  ("λ = h/(mu)", True, "Right: a moving mass, so de Broglie."),
                  ("λν = c", False, "Only light travels at c."),
                  ("Balmer's formula", False, "That's for hydrogen's visible lines.")),
    hints=["Photon or particle with mass?"],
    solution="<p>A particle with mass and speed: <strong>λ = h/(mu)</strong> (Day 4 p.11).</p>",
    source="Day 4 p.11")

lam_bad = de_broglie(9.10938e-28, 4.05e6)
add(id="m7-m-sanity", module="m7", kind="mastery", level="Sanity check",
    prompt=f"<p>A student redoes the Day 4 p.12 example (electron at 4.05 × 10<sup>6</sup> m/s) and gets λ = {sci(lam_bad, 2)} m instead of 1.80 × 10<sup>−10</sup> m. What went wrong?</p>",
    answer=choice(("The mass was left in grams (9.10938 × 10<sup>−28</sup> g).", True, "Right: that makes λ exactly 1000 times too small."),
                  ("The speed was in km/s.", False, "That would change λ by 1000, but in the other direction."),
                  ("h was rounded to 6.626 × 10<sup>−34</sup>.", False, "The lecture rounds h the same way; rounding can't cause a factor of 1000."),
                  ("Nothing; both answers are acceptable.", False, "They differ by a factor of 1000.")),
    hints=["Compare the two answers: what's the ratio?"],
    solution="<p>The ratio is exactly 1000, the g → kg factor. The worked example converts 9.10938 × 10<sup>−28</sup> g to 9.10938 × 10<sup>−31</sup> kg first (Day 4 p.12).</p>",
    source="Day 4 p.12")

# =====================================================================================
# m8  Wavefunctions, quantum numbers & Pauli  (Day 4 p.18; Day 5 p.7–16)
# =====================================================================================
add(id="m8-attempt", module="m8", kind="attempt", level="Guided attempt",
    prompt="<p>For the n = 4 shell: (a) how many orbitals does it contain, and (b) how many electrons can it hold?</p>",
    answer={"type": "multi", "parts": [
        {"label": "(a) orbitals", **num_ans(16, tol=0)},
        {"label": "(b) electrons", **num_ans(32, tol=0)}]},
    hints=["Count the allowed values of ℓ and m<sub>ℓ</sub> (Day 5 p.12–13).",
           "ℓ runs from 0 to n − 1; each ℓ has 2ℓ + 1 values of m<sub>ℓ</sub>, one orbital each.",
           "n = 4: ℓ = 0, 1, 2, 3 (4s, 4p, 4d, 4f) → 1 + 3 + 5 + 7 orbitals.",
           "Each orbital holds two electrons (Pauli, Day 5 p.15)."],
    solution="<p>(a) 1 + 3 + 5 + 7 = <strong>16 orbitals</strong>, matching Table 3.1 on Day 5 p.13 (in general n<sup>2</sup>). (b) 2 electrons per orbital → <strong>32 electrons</strong> (2n<sup>2</sup>).</p>",
    compare={
        "wrong": "<p>“n = 4 has four subshells (s, p, d, f), so 4 orbitals and 8 electrons.”</p>",
        "tempting": "The four values of ℓ are easy to count, and each subshell has one letter.",
        "fails": "A subshell isn't an orbital. Each subshell has 2ℓ + 1 orbitals (its m<sub>ℓ</sub> values): s 1, p 3, d 5, f 7 (Day 5 p.13)."},
    source="Day 5 p.12–15")

add(id="m8-p1", module="m8", kind="practice", level="Warm-up",
    prompt="<p>Which set (n, ℓ, m<sub>ℓ</sub>, m<sub>s</sub>) is allowed?</p>",
    answer=choice(("(2, 1, −1, +½)", True, "Right: ℓ = 1 ≤ n − 1; m<sub>ℓ</sub> = −1 is within −1…+1; m<sub>s</sub> = +½. A 2p electron."),
                  ("(3, 3, 0, −½)", False, "ℓ must be at most n − 1 = 2."),
                  ("(4, 2, −3, +½)", False, "For ℓ = 2, m<sub>ℓ</sub> runs only from −2 to +2."),
                  ("(1, 0, 0, 0)", False, "m<sub>s</sub> must be +½ or −½ (Day 5 p.14).")),
    hints=["Check in order: n ≥ 1 → 0 ≤ ℓ ≤ n − 1 → −ℓ ≤ m<sub>ℓ</sub> ≤ +ℓ → m<sub>s</sub> = ±½."],
    solution="<p><strong>(2, 1, −1, +½)</strong> is allowed: a 2p electron. The others break one rule each (Day 5 p.10–14).</p>",
    source="Day 5 p.10–16")

add(id="m8-p2", module="m8", kind="practice", level="Standard",
    prompt="<p>What is the maximum number of electrons in a 5f subshell?</p>",
    answer=num_ans(14, tol=0),
    hints=["f means ℓ = 3 (Day 5 p.12).", "Number of orbitals = number of m<sub>ℓ</sub> values = 2ℓ + 1.", "2(3) + 1 = 7 orbitals.", "Each holds 2 electrons."],
    solution="<p>ℓ = 3 → m<sub>ℓ</sub> = −3…+3 → 7 orbitals × 2 = <strong>14 electrons</strong>. The n = 5 doesn't change the count; any f subshell holds 14.</p>",
    source="Day 5 p.12–15")

add(id="m8-p3", module="m8", kind="practice", level="Standard",
    prompt="<p>What is the subshell label for n = 4, ℓ = 2? (e.g., type <em>3p</em>)</p>",
    answer={"type": "text", "accepted": ["4d"], "caseInsensitive": True, "placeholder": "e.g., 3p"},
    hints=["The number is n; the letter comes from ℓ (Day 5 p.12).", "ℓ = 0, 1, 2, 3 → s, p, d, f."],
    solution="<p><strong>4d</strong>: n = 4, and ℓ = 2 is the letter d.</p>",
    source="Day 5 p.12")

add(id="m8-p4", module="m8", kind="practice", level="Warm-up",
    prompt="<p>Which quantum number sets an orbital's <strong>orientation</strong> in space?</p>",
    answer=choice(("n", False, "n sets size and energy."), ("ℓ", False, "ℓ sets shape."),
                  ("m<sub>ℓ</sub>", True, "Right (Day 5 p.10, p.13)."), ("m<sub>s</sub>", False, "m<sub>s</sub> is the electron's spin, not the orbital's orientation.")),
    hints=["Day 5 p.10 pairs each quantum number with one property: size/energy, shape, orientation."],
    solution="<p><strong>m<sub>ℓ</sub></strong> (orientation). n → size and energy; ℓ → shape; m<sub>s</sub> → spin (Day 5 p.10–14).</p>",
    source="Day 5 p.10–14")

add(id="m8-p5", module="m8", kind="practice", level="Standard",
    prompt="<p>What does |Ψ|<sup>2</sup> represent?</p>",
    answer=choice(("The path the electron travels around the nucleus", False, "Orbitals aren't paths; that's the Bohr picture."),
                  ("The probability density: where the electron is likely to be found", True, "Right (Max Born, 1926; Day 5 p.8)."),
                  ("The electron's charge", False, "The charge is always −1.602 × 10<sup>−19</sup> C."),
                  ("Nothing physical", False, "Ψ itself has no direct physical meaning, but |Ψ|<sup>2</sup> does (Day 5 p.8).")),
    hints=["Day 5 p.8 distinguishes Ψ from |Ψ|<sup>2</sup>."],
    solution="<p>|Ψ|<sup>2</sup> is the <strong>probability density</strong>. Regions of high probability are what we call orbitals (Day 5 p.8).</p>",
    source="Day 5 p.8")

add(id="m8-transfer", module="m8", kind="transfer", level="Transfer",
    prompt="<p>Imagine a universe where m<sub>s</sub> could take <em>three</em> values (−1, 0, +1), with every other rule unchanged. How many electrons could a p subshell hold?</p>",
    answer=num_ans(9, tol=0),
    hints=["The counting logic transfers: (number of orbitals) × (electrons allowed per orbital).",
           "A p subshell still has 3 orbitals (m<sub>ℓ</sub> = −1, 0, +1).",
           "Pauli: no two electrons share all four quantum numbers, so each orbital can hold one electron per m<sub>s</sub> value.",
           "3 orbitals × 3 spin values."],
    solution="<p>3 orbitals × 3 allowed m<sub>s</sub> values = <strong>9 electrons</strong>. In our universe, 2 spin values give 3 × 2 = 6. The Pauli principle is what turns quantum-number counting into electron capacity (Day 5 p.15).</p>",
    source="Day 5 p.13–15")

add(id="m8-m-explain", module="m8", kind="mastery", level="Explain",
    prompt="<p>Describe what n, ℓ, and m<sub>ℓ</sub> each tell you about an orbital, and what m<sub>s</sub> adds.</p>",
    answer={"type": "self", "model": "<p>n (1, 2, 3 …): relative size and energy; larger n means the electron is likely farther from the nucleus. "
                                     "ℓ (0 … n − 1): shape (s, p, d, f). m<sub>ℓ</sub> (−ℓ … +ℓ): orientation in space; the number of values is the number of orbitals in the subshell. "
                                     "Those three label an orbital (Day 5 p.10–13). m<sub>s</sub> (±½) labels the electron's spin, and with Pauli it limits each orbital to two electrons (Day 5 p.14–15).</p>"},
    hints=[], solution="", source="Day 5 p.10–15")

add(id="m8-m-recognize", module="m8", kind="mastery", level="Recognize",
    prompt="<p>“Could two electrons in the same atom both have n = 3, ℓ = 1, m<sub>ℓ</sub> = 0, m<sub>s</sub> = +½?” Which principle answers this?</p>",
    answer=choice(("Aufbau principle", False, "Aufbau is about filling order."),
                  ("Hund's rule", False, "Hund is about spreading electrons over degenerate orbitals."),
                  ("Pauli exclusion principle: no", True, "Right: no two electrons can share all four quantum numbers (Day 5 p.15)."),
                  ("Bohr model: yes", False, "The Bohr model doesn't use four quantum numbers.")),
    hints=["Identical sets of all four quantum numbers …"],
    solution="<p><strong>Pauli: no.</strong> No two electrons can have the same set of four quantum numbers (Day 5 p.15).</p>",
    source="Day 5 p.15")

add(id="m8-m-sanity", module="m8", kind="mastery", level="Sanity check",
    prompt="<p>A student's answer mentions a “2d orbital.” Is that possible?</p>",
    answer=choice(("Yes; it's a small d orbital.", False, "d means ℓ = 2, which needs n ≥ 3."),
                  ("No; for n = 2, ℓ can only be 0 or 1 (s or p).", True, "Right: ℓ ≤ n − 1 (Day 5 p.12)."),
                  ("Yes, but only in hydrogen.", False, "The ℓ ≤ n − 1 rule holds for every atom."),
                  ("No; d orbitals don't exist.", False, "They do: 3d, 4d … (Day 5 p.20).")),
    hints=["What values of ℓ are allowed when n = 2?"],
    solution="<p>For n = 2, ℓ = 0 or 1 only, so 2s and 2p. The first d subshell is 3d (Day 5 p.12).</p>",
    source="Day 5 p.12")

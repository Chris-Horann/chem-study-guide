"""Problem bank E: Chapter 3–4 TEXTBOOK-PREVIEW modules (t3-5 Heisenberg, t3-11 PES; t4-2 electronegativity, taught on
Day 9 and relabeled lecture on 2026-10-06),
preview items inside lecture modules (m3, m10, m14), and mixed-review problems x21–x35."""
import math
from guide_common import *
from problem_bank_a import PROBLEMS, add, num_ans, choice, J_UNITS, M_UNITS, MS_UNITS, NM_UNITS, KJMOL_UNITS, G_UNITS
from problem_bank_b import text_ans, formula_ans, order_ans, cfg_ans
from problem_bank_c import P, tb, G_CM3_UNITS, ML_UNITS, KM_UNITS
from problem_bank_d import MOL_UNITS, GMOL_UNITS, U_UNITS, sym_ans

MJMOL_UNITS = ["mj/mol", "mj mol^-1", "mj mol-1", "mj·mol^-1"]
MP = 1.673e-27  # proton mass, kg (Day 2 p.22: 1.67262e-27)

def heis_du(m, dx):
    return H / (4 * math.pi * m * dx)

# =====================================================================================
# Preview items inside lecture modules
# =====================================================================================
P(id="m3-preview-maxwell", module="m3", kind="practice", level="Textbook preview",
  prompt="<p>According to the textbook's picture of electromagnetic radiation (Maxwell's theory), what is oscillating as a light wave travels?</p>",
  answer=choice(("air molecules", False, "Light needs no medium; it crosses the vacuum of space."), ("an electric field and a magnetic field, at right angles to each other", True, "Right (textbook Fig. 3.2)."),
                ("electrons inside the light beam", False, "The beam isn't made of electrons."), ("nothing: light is only particles", False, "The wave description works too (λν = c).")),
  hints=["Textbook Fig. 3.2 draws two perpendicular waves."],
  solution="<p>Perpendicular <strong>electric and magnetic fields</strong> oscillate as the wave moves. Their wavelength and frequency are the λ and ν of λν = c (Day 2 p.30, covered in lecture).</p>",
  source=tb("3.1", 121) + "; Day 2 p.30")

P(id="m10-preview-excited", module="m10", kind="practice", level="Textbook preview",
  prompt="<p>The textbook's example is sodium: a flame moves its 3s electron up to 3p, giving the first excited state [Ne]3p<sup>1</sup>. Apply the same idea to lithium, whose ground state is [He]2s<sup>1</sup>. Write lithium's <em>first excited state</em>, where the 2s electron has moved up to the next-lowest subshell.</p>",
  answer={"type": "config", "target": {"1s": 2, "2p": 1}, "electrons": 3, "species": "excited Li",
          "incorrectNote": "An excited state keeps all 3 electrons but moves one electron up to a higher subshell. Which subshell comes after 2s (Day 6 p.19)?"},
  hints=["An excited state keeps all 3 electrons but moves one to a higher-energy orbital.", "After 2s, the next subshell to fill is 2p (Day 6 p.19)."],
  solution="<p><strong>1s<sup>2</sup>2p<sup>1</sup> = [He]2p<sup>1</sup></strong>. When the electron falls back from 2p to 2s, the atom emits the energy difference as light: the red of a lithium flame. The textbook makes the same point with sodium's yellow-orange light (§3.8, Figs. 3.30–3.31); emission lines were covered on Day 3 p.8–9.</p>",
  source=tb("3.8", 149, 150) + "; Day 3 p.8")

P(id="m10-preview-exception", module="m10", kind="practice", level="Textbook preview",
  prompt="<p>By the lecture's rules, chromium would be [Ar]4s<sup>2</sup>3d<sup>4</sup>. What does the textbook report as chromium's actual ground-state configuration, and what does this course do with such exceptions?</p>",
  answer=choice(("[Ar]3d<sup>5</sup>4s<sup>1</sup>; the course ignores exceptions (Day 7 p.6).", True, "Right: a half-filled 3d set is lower in energy (textbook §3.8)."),
                ("[Ar]3d<sup>6</sup>; the course requires memorizing it.", False, "The professor said the class will “completely ignore” exceptions."),
                ("[Ar]4s<sup>2</sup>3d<sup>4</sup>; there's no exception.", False, "The textbook says Cr is an exception."),
                ("[Kr]; the course ignores it.", False, "Cr has 24 electrons, not 36.")),
  hints=["The textbook points to the stability of a half-filled d subshell.", "Day 7 p.6: “We will completely ignore this in this class.”"],
  solution="<p>The textbook gives <strong>[Ar]3d<sup>5</sup>4s<sup>1</sup></strong> (and Cu [Ar]3d<sup>10</sup>4s<sup>1</sup>, Ag [Kr]4d<sup>10</sup>5s<sup>1</sup>). In this course: “We will <em>completely ignore this</em>” (Day 7 p.6). The guide's problems always use the rules.</p>",
  source=tb("3.8", 150, 152) + "; Day 7 p.6")

# The two m14 items below were textbook-preview items until Day 8 taught their content (H–H curve, Day 8 p.11;
# bonding capacity, Day 8 p.18). They are lecture items now; the ids are kept so saved progress still matches.
add(id="m14-preview-covalent", module="m14", kind="practice", level="Standard",
    prompt="<p>On the Day 8 energy curve for two H atoms (p.11; textbook Fig. 4.2), the energy is lowest, −436 kJ/mol, at 74 pm. What do those two numbers represent?</p>",
    answer=choice(("74 pm is the H–H bond length; 436 kJ/mol is the bond energy (the energy to break a mole of H–H bonds).", True, "Right: the textbook's names for them (§4.1, §4.6)."),
                  ("74 pm is the radius of an H atom; 436 kJ/mol is its ionization energy.", False, "H's IE₁ is 1312 kJ/mol (Day 7 p.9), and 74 pm is the distance between two nuclei."),
                  ("74 pm is where the atoms repel most.", False, "Repulsion takes over at shorter distances: the steep left wall, “Increasing repulsion” (Day 8 p.11)."),
                  ("436 kJ/mol is the lattice energy of H<sub>2</sub>.", False, "H<sub>2</sub> is molecular, not an ionic lattice.")),
    hints=["It's the same shape as the ion-pair curve on Day 7 p.15: attraction, a minimum, then repulsion."],
    solution="<p>The minimum marks the <strong>bond length</strong> (74 pm) and the <strong>bond energy</strong> (436 kJ/mol) of the covalent H–H bond, where two electrons are shared by both nuclei. "
             "The slide shows the curve without naming the two numbers (Day 8 p.11); the names are the textbook's (§4.1, PDF p.184; §4.6, PDF p.208). "
             "It's the covalent counterpart of the ionic curve on Day 7 p.15.</p>",
    source="Day 8 p.11; Day 7 p.15; " + tb("4.1", 184, 185))

add(id="m14-preview-valence", module="m14", kind="practice", level="Concept",
    prompt="<p>The lecture defines <em>bonding capacity</em> (Day 8 p.18). The textbook uses the word <em>valence</em> by itself, not as part of “valence electrons,” for the same idea. What does it mean?</p>",
    answer=choice(("The number of covalent bonds an element's atoms form (to complete an octet).", True, "Right: bonding capacity (Day 8 p.18), the textbook's “valence” (§4.1, PDF p.181)."),
                  ("The number of electrons in an atom's outermost shell.", False, "That describes the valence <em>electrons</em> (Day 6 p.14). Bonding capacity counts bonds, not electrons."),
                  ("The charge of the element's most common ion.", False, "Ion charges come from gaining or losing electrons (Day 7 p.19). Bonding capacity is about shared-pair bonds."),
                  ("The energy needed to remove an atom's outermost electron.", False, "That's the first ionization energy (Day 7 p.9).")),
    hints=["“The bonding capacity of an element is the number of covalent bonds an atom forms…” (Day 8 p.18).", "Think bonds, not electrons."],
    solution="<p><strong>The number of bonds an atom forms.</strong> “The bonding capacity of an element is the number of covalent bonds an atom forms to have an octet of electrons in its valence shell” (Day 8 p.18). "
             "The textbook calls this capacity the element's <em>valence</em> (§4.1, PDF p.181, printed 147). Valence electrons are a set of electrons (Day 6 p.14); bonding capacity is a number of bonds: "
             "C has 4 valence electrons and bonding capacity 4, but O has 6 valence electrons and bonding capacity 2.</p>",
    source="Day 8 p.18; Day 6 p.14; " + tb("4.1", 181))

# =====================================================================================
# t3-5 Heisenberg uncertainty principle (§3.5, TB PDF p.137–138)
# =====================================================================================
du_e = heis_du(ME, 1.0e-10)
du_wrong = H / (ME * 1.0e-10)
P(id="t3-5-attempt", module="t3-5", kind="attempt", level="Guided attempt",
  prompt="<p>An electron (m = 9.109 × 10<sup>−31</sup> kg) is confined to a region about the size of an atom, Δx = 1.0 × 10<sup>−10</sup> m. What is the minimum uncertainty in its speed? (h = 6.626 × 10<sup>−34</sup> J·s)</p>",
  answer=num_ans(du_e, sf=2, tol=0.02, unit_label="m/s", units=MS_UNITS, ask_unit=True),
  hints=["Heisenberg: Δx · mΔu ≥ h/(4π) (textbook Eq. 3.14).",
         "Solve for the velocity uncertainty: Δu ≥ h/(4π m Δx).",
         "m = 9.109 × 10<sup>−31</sup> kg; h = 6.626 × 10<sup>−34</sup> J·s (1 J = 1 kg·m²/s²).",
         "Δu ≥ 6.626 × 10<sup>−34</sup> ÷ (4π × 9.109 × 10<sup>−31</sup> × 1.0 × 10<sup>−10</sup>)."],
  solution=f"<p>Δu ≥ h/(4π m Δx) = 6.626 × 10<sup>−34</sup> J·s ÷ (4π × 9.109 × 10<sup>−31</sup> kg × 1.0 × 10<sup>−10</sup> m) = <strong>{sci(du_e, 2)} m/s</strong>. "
           "That's an enormous uncertainty for anything that fits inside an atom, which is why the idea of a definite path (Bohr's orbit) breaks down and orbitals describe probabilities (Day 5 p.8, covered in lecture).</p>",
  compare={"wrong": f"<p>“Δu = h/(mΔx) = {sci(du_wrong, 2)} m/s.”</p>",
           "tempting": "It looks like the de Broglie equation rearranged, and the 4π is easy to drop.",
           "fails": "The uncertainty relation carries h/(4π). Dropping 4π makes the answer about 12.6 times too big. The two equations answer different questions: de Broglie gives a wavelength from a momentum; Heisenberg gives the smallest possible product of the uncertainties."},
  source=tb("3.5", 137, 138))

du_p = heis_du(MP, 1.0e-15)
P(id="t3-5-p1", module="t3-5", kind="practice", level="Standard",
  prompt="<p>A proton (m = 1.673 × 10<sup>−27</sup> kg) is confined within a nucleus, Δx = 1.0 × 10<sup>−15</sup> m. Minimum speed uncertainty? (h = 6.626 × 10<sup>−34</sup> J·s)</p>",
  answer=num_ans(du_p, sf=2, tol=0.02, unit_label="m/s", units=MS_UNITS),
  hints=["Δu ≥ h/(4π m Δx).", "Same form, with the proton's mass and a much smaller Δx."],
  solution=f"<p>Δu ≥ 6.626 × 10<sup>−34</sup> ÷ (4π × 1.673 × 10<sup>−27</sup> × 1.0 × 10<sup>−15</sup>) = <strong>{sci(du_p, 2)} m/s</strong>, about 10% of the speed of light.</p>",
  source=tb("3.5", 137))

P(id="t3-5-p2", module="t3-5", kind="practice", level="Warm-up",
  prompt="<p>If you pin down a particle's position twice as precisely (Δx halved), what happens to the minimum uncertainty in its speed?</p>",
  answer=choice(("It halves.", False, "Δx and Δu trade off inversely."), ("It doubles.", True, "Right: Δu ≥ h/(4π m Δx)."), ("It stays the same.", False, "They're linked."), ("It becomes zero.", False, "It can never be zero.")),
  hints=["Look at where Δx appears in Δu ≥ h/(4π m Δx)."],
  solution="<p>Δu ∝ 1/Δx: halving Δx <strong>doubles</strong> the minimum Δu.</p>", source=tb("3.5", 137))

du_t = heis_du(0.0570, 1.0e-6)
P(id="t3-5-p3", module="t3-5", kind="practice", level="Standard",
  prompt="<p>A 57.0 g tennis ball's position is known to within 1.0 μm (1.0 × 10<sup>−6</sup> m). Minimum speed uncertainty? (h = 6.626 × 10<sup>−34</sup> J·s)</p>",
  answer=num_ans(du_t, sf=2, tol=0.02, unit_label="m/s", units=MS_UNITS),
  hints=["Mass in kg: 0.0570 kg.", "Δu ≥ 6.626 × 10<sup>−34</sup> ÷ (4π × 0.0570 × 1.0 × 10<sup>−6</sup>)."],
  solution=f"<p>Δu ≥ <strong>{sci(du_t, 2)} m/s</strong>, far too small ever to notice. The same contrast as the de Broglie baseball (Day 4 p.14).</p>",
  source=tb("3.5", 137, 138) + "; Day 4 p.14")

P(id="t3-5-p4", module="t3-5", kind="practice", level="Standard",
  prompt="<p>In Heisenberg's thought experiment, why can't we simply watch an electron move around the nucleus?</p>",
  answer=choice(("Electrons are invisible because they're negative.", False, "Charge isn't the issue."),
                ("Seeing something so small needs very short-wavelength light (γ rays), whose high-energy photons knock the electron off course.", True, "Right (textbook §3.5)."),
                ("Electrons move faster than light.", False, "They don't."), ("Microscopes can't be built.", False, "The limit is physical, not technological.")),
  hints=["Recall E = hc/λ: what does short-wavelength light carry?"],
  solution="<p>Short-wavelength light has high-energy photons (E = hc/λ, Day 4 p.10), so looking <strong>changes the momentum</strong> you're trying to measure.</p>",
  source=tb("3.5", 137) + "; Day 4 p.10")

dx_min = H / (4 * math.pi * ME * 1.0e5)
P(id="t3-5-transfer", module="t3-5", kind="transfer", level="Transfer",
  prompt="<p>An experiment measures an electron's speed to within 1.0 × 10<sup>5</sup> m/s (m = 9.109 × 10<sup>−31</sup> kg; h = 6.626 × 10<sup>−34</sup> J·s). What is the smallest possible uncertainty in its position? Compare it with an atom's size (~10<sup>−10</sup> m).</p>",
  answer=num_ans(dx_min, sf=2, tol=0.02, unit_label="m", units=M_UNITS),
  hints=["Rearrange for Δx.", "Δx ≥ h/(4π m Δu).", "6.626 × 10<sup>−34</sup> ÷ (4π × 9.109 × 10<sup>−31</sup> × 1.0 × 10<sup>5</sup>)."],
  solution=f"<p>Δx ≥ <strong>{sci(dx_min, 2)} m</strong>, several atoms wide. Knowing the speed that well means the electron can't be located inside one atom.</p>",
  source=tb("3.5", 137))

P(id="t3-5-m-explain", module="t3-5", kind="mastery", level="Explain",
  prompt="<p>Why does the uncertainty principle matter for electrons but not for baseballs?</p>",
  answer={"type": "self", "model": "<p>Δu ≥ h/(4π m Δx): the uncertainty in velocity is inversely proportional to mass. For a baseball, m is so large that Δu is around 10<sup>−28</sup> m/s, which is undetectable. "
                                   "For an electron (10<sup>−31</sup> kg) confined to an atom, Δu is around 10<sup>6</sup> m/s, as large as the speed itself. So electrons can't be given definite paths, and we describe them with probabilities (orbitals) instead (textbook §3.5; Day 5 p.8).</p>"},
  hints=[], solution="", source=tb("3.5", 137, 138))

P(id="t3-5-m-recognize", module="t3-5", kind="mastery", level="Recognize",
  prompt="<p>“Given Δx for a particle, find the minimum Δu.” Which relationship?</p>",
  answer=choice(("λ = h/(mu)", False, "That's de Broglie's wavelength."), ("Δx · mΔu ≥ h/(4π)", True, "Right: Eq. 3.14."), ("E = hν", False, "Photon energy."), ("KE = ½mu²", False, "Kinetic energy.")),
  hints=["Uncertainties → Heisenberg."],
  solution="<p><strong>Δx · mΔu ≥ h/(4π)</strong>.</p>", source=tb("3.5", 137))

P(id="t3-5-m-sanity", module="t3-5", kind="mastery", level="Sanity check",
  prompt="<p>A student claims a perfect instrument could measure an electron's position and speed exactly, at the same time. What's wrong?</p>",
  answer=choice(("Nothing, with good enough technology", False, "The limit is built into nature, not the instrument."), ("Δx · mΔu can never be less than h/(4π), so both can't be zero at once.", True, "Right."),
                ("Electrons have no position.", False, "They have positions, just not simultaneously exact ones along with momentum."), ("Speed can be exact, but position is never measurable.", False, "Each alone can be sharp; the product is what's limited.")),
  hints=["What's the smallest the product can be?"],
  solution="<p>The product of the uncertainties has a floor, h/(4π), so they can't both be zero.</p>", source=tb("3.5", 137, 138))

# =====================================================================================
# t3-11 Photoelectron spectroscopy (§3.11, TB PDF p.162–164)
# =====================================================================================
P(id="t3-11-attempt", module="t3-11", kind="attempt", level="Guided attempt",
  prompt="<p>A photoelectron spectrum shows three peaks: 84.0 MJ/mol (relative height 2), 4.68 MJ/mol (height 2), and 2.08 MJ/mol (height 6). (a) How many electrons does the atom have? (b) Which element is it (symbol)?</p>",
  answer={"type": "multi", "parts": [
      {"label": "(a) electrons", **num_ans(10, tol=0)}, {"label": "(b) element", **sym_ans("Ne", "neon")}]},
  hints=["In PES, peak height is proportional to the number of electrons with that binding energy (textbook §3.11).",
         "Add the heights: that's the total number of electrons.",
         "Assign subshells from the largest binding energy (closest to the nucleus) to the smallest: 1s, 2s, 2p.",
         "1s<sup>2</sup>2s<sup>2</sup>2p<sup>6</sup> is which element?"],
  solution="<p>(a) 2 + 2 + 6 = <strong>10</strong> electrons. (b) 1s<sup>2</sup> (84.0), 2s<sup>2</sup> (4.68), 2p<sup>6</sup> (2.08) → <strong>Ne</strong>. The smallest binding energy, 2.08 MJ/mol = 2080 kJ/mol, matches neon's IE₁ of 2081 kJ/mol (Day 7 p.9).</p>"
           "<p class='bg'>The Ne binding energies are reference values; the textbook's own examples are Li and Al.</p>",
  compare={"wrong": "<p>“Three peaks means three electrons: lithium.”</p>",
           "tempting": "Counting peaks is the quickest thing to do.",
           "fails": "Each peak is a <em>subshell</em>, not an electron. Its height counts the electrons in that subshell (Al: 2 : 2 : 6 : 2 : 1). Heights 2, 2, 6 add up to 10 electrons."},
  source=tb("3.11", 162, 163) + "; Day 7 p.9")

P(id="t3-11-p1", module="t3-11", kind="practice", level="Warm-up",
  prompt="<p>In lithium's spectrum (peaks at 6.26 and 0.52 MJ/mol), why is the 6.26 MJ/mol peak twice as tall?</p>",
  answer=choice(("It is the 1s subshell, with 2 electrons; the 0.52 peak is the single 2s electron.", True, "Right: heights 2 : 1 match 1s<sup>2</sup>2s<sup>1</sup>."),
                ("Higher energy always gives taller peaks.", False, "Height counts electrons, not energy."),
                ("It is two overlapping peaks.", False, "One subshell."), ("The 2s electron is shielded.", False, "Shielding changes position, not height.")),
  hints=["What does peak height count?"],
  solution="<p>Height ∝ number of electrons: 1s<sup>2</sup> (2) vs. 2s<sup>1</sup> (1) (textbook §3.11).</p>", source=tb("3.11", 162, 163))

P(id="t3-11-p2", module="t3-11", kind="practice", level="Standard",
  prompt="<p>Which of these elements has a PES peak at the largest binding energy?</p>",
  answer=choice(("Na", False, "Fewest protons of the four."), ("Mg", False, "More than Na, but not the most."), ("Al", False, "13 protons."), ("Si", True, "Right: 14 protons pull hardest on the 1s electrons.")),
  hints=["The largest binding energy in any spectrum is for 1s.", "Which nucleus has the most protons?"],
  solution="<p><strong>Si</strong>: with Z = 14, its 1s electrons feel the most nuclear charge. The textbook's contrast is Al's 151 MJ/mol vs. Li's 6.26 MJ/mol.</p>",
  source=tb("3.11", 162, 163))

per_atom = 0.52e6 / NA
P(id="t3-11-p3", module="t3-11", kind="practice", level="Standard",
  prompt="<p><span class='tag-conn'>Connects to Module 13</span> Lithium's 2s binding energy is 0.52 MJ/mol. Convert it to kJ/mol and compare with Li's IE<sub>1</sub> on Day 7 p.9.</p>",
  answer=num_ans(520, sf=2, unit_label="kJ/mol", units=KJMOL_UNITS),
  hints=["1 MJ = 1000 kJ.", "0.52 MJ/mol × 1000 kJ/MJ."],
  solution=f"<p>0.52 MJ/mol = <strong>520 kJ/mol</strong>, equal to lithium's IE<sub>1</sub> (520 kJ/mol, Day 7 p.9): removing the outermost electron is the first ionization. (Per atom: {sci(per_atom, 2)} J.)</p>",
  source=tb("3.11", 163) + "; Day 7 p.9")

P(id="t3-11-p4", module="t3-11", kind="practice", level="Standard",
  prompt="<p>The x-axis of a photoelectron spectrum is drawn with binding energy <em>decreasing</em> from left to right. Moving left to right, the electrons are…</p>",
  answer=choice(("closer to the nucleus", False, "Closer electrons have larger binding energies, on the left."), ("farther from the nucleus (outer subshells)", True, "Right (textbook §3.11)."),
                ("heavier", False, "All electrons have the same mass."), ("unpaired", False, "Pairing isn't read from position.")),
  hints=["Large binding energy → tightly held → close to the nucleus."],
  solution="<p>Right side = small binding energies = <strong>outer, valence electrons</strong>.</p>", source=tb("3.11", 162))

P(id="t3-11-transfer", module="t3-11", kind="transfer", level="Transfer",
  prompt="<p>A spectrum has five peaks with relative heights 2 : 2 : 6 : 2 : 6 (from largest to smallest binding energy). Identify the element (symbol).</p>",
  answer=sym_ans("Ar", "argon"),
  hints=["Assign the subshells in order: 1s, 2s, 2p, 3s, 3p.", "Add the heights for the electron count."],
  solution="<p>1s<sup>2</sup>2s<sup>2</sup>2p<sup>6</sup>3s<sup>2</sup>3p<sup>6</sup> → 18 electrons → <strong>Ar</strong>.</p>", source=tb("3.11", 162, 163))

P(id="t3-11-m-explain", module="t3-11", kind="mastery", level="Explain",
  prompt="<p>How does a photoelectron spectrum give direct evidence for subshells and electron configurations?</p>",
  answer={"type": "self", "model": "<p>X-ray photons eject electrons from every subshell. Binding energy = photon energy − the photoelectron's KE, the same bookkeeping as KE = hν − φ (Day 3 p.19). "
                                   "Electrons in the same subshell share one binding energy, so each subshell makes one peak. Its position shows how tightly those electrons are held (closer, less shielded → larger), and its height shows how many there are. Al's 2 : 2 : 6 : 2 : 1 pattern is 1s<sup>2</sup>2s<sup>2</sup>2p<sup>6</sup>3s<sup>2</sup>3p<sup>1</sup> (textbook §3.11).</p>"},
  hints=[], solution="", source=tb("3.11", 162, 163) + "; Day 3 p.19")

P(id="t3-11-m-recognize", module="t3-11", kind="mastery", level="Recognize",
  prompt="<p>Which relationship from lecture is PES built on?</p>",
  answer=choice(("λ = h/(mu)", False, "de Broglie."), ("KE = hν − φ (energy in excess of the binding energy becomes KE)", True, "Right: the photoelectric bookkeeping (Day 3 p.19)."),
                ("E<sub>el</sub> = 2.31 × 10<sup>−19</sup> J·nm (Q<sub>1</sub>Q<sub>2</sub>/d)", False, "Ion pairs."), ("Balmer's formula", False, "Hydrogen lines.")),
  hints=["Photons eject electrons…"],
  solution="<p>The photoelectric relation: the photon's energy minus the binding energy becomes kinetic energy.</p>", source=tb("3.11", 162) + "; Day 3 p.19")

P(id="t3-11-m-sanity", module="t3-11", kind="mastery", level="Sanity check",
  prompt="<p>A student labels one peak “3s, height 3.” What's wrong?</p>",
  answer=choice(("Nothing", False, "An s subshell holds at most 2 electrons."), ("An s subshell holds at most 2 electrons (Pauli), so no s peak can have height 3.", True, "Right."),
                ("3s peaks are always the largest.", False, "No."), ("s peaks can't appear in PES.", False, "They do.")),
  hints=["Day 5 p.15: how many electrons can one orbital hold?"],
  solution="<p>One s orbital holds at most 2 electrons (Day 5 p.15), so the maximum height for an s peak is 2.</p>", source=tb("3.11", 163) + "; Day 5 p.15")

# =====================================================================================
# t4-2 Electronegativity and polar bonds (lecture: Day 9 p.15–18, Day 10 p.27; textbook §4.2, TB PDF p.185–188)
# Relabeled 2026-10-06: Day 9 teaches χ, Δχ, and the cutoffs; only the χ–IE₁ comparison (m-explain) stays preview.
# =====================================================================================
EN = ELECTRONEGATIVITY
def dchi(a, b):
    return round(abs(EN[a] - EN[b]), 2)

add(id="t4-2-attempt", module="t4-2", kind="attempt", level="Guided attempt",
    prompt="<p>Consider the H–F bond (χ: H 2.1, F 4.0; Day 9 p.17). (a) What is Δχ? (b) Classify the bond. (c) Which atom carries the partial negative charge (δ−)?</p>",
    answer={"type": "multi", "parts": [
        {"label": "(a) Δχ", **num_ans(dchi("H", "F"), sf=2, tol=0.001)},
        {"label": "(b) bond type", **choice(("nonpolar covalent", False, "Δχ is well above 0.4."), ("polar covalent", True, "0.4 &lt; 1.9 &lt; 2.0."),
                                             ("ionic", False, "Ionic starts at Δχ ≥ 2.0 on the slide's scale (Day 9 p.18)."))},
        {"label": "(c) δ− atom", **choice(("H", False, "H is less electronegative."),
                                          ("F", True, "The more electronegative atom has more of the electron density, so it's the δ− end."))}]},
    hints=["Electronegativity, χ, is the course's way “to describe the polarity of bonds” (Day 9 p.17): in a polar bond, “one of the atoms has more of the electron density” (Day 9 p.15).",
           "Δχ = |4.0 − 2.1|.",
           "The slide's cutoffs (Day 9 p.18): Δχ ≤ 0.4 nonpolar covalent; 0.4 &lt; Δχ &lt; 2.0 polar covalent; Δχ ≥ 2.0 ionic.",
           "The shared pair sits closer to the higher-χ atom, which becomes δ−: the battery's − end on Day 9 p.15."],
    solution=f"<p>(a) Δχ = 4.0 − 2.1 = <strong>{dchi('H', 'F')}</strong>. (b) <strong>Polar covalent</strong> (0.4 &lt; 1.9 &lt; 2.0). (c) <strong>F</strong> is δ− and H is δ+: H<sup>δ+</sup>–F<sup>δ−</sup>, "
             "with the crossed arrow's + tail at H and its head at F, as for H–Cl on Day 9 p.15.</p>",
    compare={"wrong": "<p>“Δχ = 1.9 is almost 2, so H–F is ionic, with H<sup>+</sup> and F<sup>−</sup>.”</p>",
             "tempting": "1.9 is close to the cutoff, and F is famously “electron-hungry.”",
             "fails": "On the slide's scale ionic starts at Δχ ≥ 2.0 (Day 9 p.18), so 1.9 is polar covalent: the pair is shared unequally, not transferred. That gives partial charges (δ+, δ−), "
                      "like HCl's potential map, not full charges like NaCl's (Day 9 p.16). The textbook adds that the cutoffs are “more like guidelines than strict limits” (PDF p.186): a value this close to 2.0 means a very polar bond."},
    source="Day 9 p.15–18; " + tb("4.2", 186, 187))

add(id="t4-2-p1", module="t4-2", kind="practice", level="Standard",
    prompt="<p>Rank these bonds from most polar (1) to least polar (4): C–H, N–H, O–H, F–H.</p>",
    answer=order_ans([("CH", "C–H"), ("NH", "N–H"), ("OH", "O–H"), ("FH", "F–H")], ["FH", "OH", "NH", "CH"], "most polar (1) to least polar (4)"),
    hints=["Compute Δχ for each bond with H (2.1), using the course's table (Day 9 p.17).", "C 2.5, N 3.0, O 3.5, F 4.0."],
    solution=f"<p>Δχ: F–H {dchi('F', 'H')} > O–H {dchi('O', 'H')} > N–H {dchi('N', 'H')} > C–H {dchi('C', 'H')}. So <strong>F–H > O–H > N–H > C–H</strong>. "
             "(C–H, at 0.4, is nonpolar covalent on the slide's scale, which puts Δχ ≤ 0.4 in that class, Day 9 p.18.)</p>",
    source="Day 9 p.17–18; " + tb("4.2", 186, 187))

pairs = [("Cl", "Cl"), ("C", "O"), ("K", "Cl"), ("P", "H")]
cls = {"nonpolar covalent": "np", "polar covalent": "pc", "ionic": "io"}
add(id="t4-2-p2", module="t4-2", kind="practice", level="Standard",
    prompt="<p>Classify each bond using Δχ and the slide's cutoffs (Day 9 p.18).</p>",
    answer={"type": "match",
            "rows": [{"html": f"{a}–{b}", "answer": cls[bond_class(dchi(a, b))]} for a, b in pairs],
            "options": [{"key": "np", "html": "nonpolar covalent"}, {"key": "pc", "html": "polar covalent"}, {"key": "io", "html": "ionic"}]},
    hints=["Δχ for each pair from the course's table (Day 9 p.17).", "Cl–Cl 0; C–O 1.0; K–Cl 2.2; P–H 0."],
    solution="<p>" + "; ".join(f"{a}–{b}: Δχ = {dchi(a, b)} → <strong>{bond_class(dchi(a, b))}</strong>" for a, b in pairs) + ". P–H is a reminder that Δχ, not the element types, decides.</p>",
    source="Day 9 p.17–18; " + tb("4.2", 186, 187))

add(id="t4-2-p3", module="t4-2", kind="practice", level="Warm-up",
    prompt="<p>Which element is the most electronegative?</p>",
    answer=choice(("N", False, "3.0"), ("P", False, "2.1"), ("O", True, "Right: 3.5, the highest of the four."), ("S", False, "2.5")),
    hints=["Look them up on the course's table (Day 9 p.17): the tallest bars are at the upper right, next to F."],
    solution="<p><strong>O</strong> (3.5): upper right, next to F (Day 9 p.17).</p>", source="Day 9 p.17; " + tb("4.2", 186, 187))

add(id="t4-2-p4", module="t4-2", kind="practice", level="Standard",
    prompt="<p>In a C–Cl bond, which atom is δ+?</p>",
    answer=choice(("C", True, "Right: C 2.5 &lt; Cl 3.0, so the shared pair shifts toward Cl."), ("Cl", False, "Cl is more electronegative, so it's δ−."),
                  ("neither", False, "Δχ = 0.5 is polar (0.4 &lt; Δχ &lt; 2.0)."), ("both", False, "One end is + and the other −, like a battery's two terminals (Day 9 p.15).")),
    hints=["The less electronegative atom ends up with less of the electron density (Day 9 p.15)."],
    solution="<p><strong>C</strong> is δ+ and Cl is δ−: C<sup>δ+</sup>–Cl<sup>δ−</sup> (Δχ = 0.5).</p>", source="Day 9 p.15, p.17–18; " + tb("4.2", 186, 187))

add(id="t4-2-transfer", module="t4-2", kind="transfer", level="Transfer",
    prompt="<p><span class='tag-conn'>Connects to Module 14</span> Calculate Δχ for Mg and O. Is that consistent with the lattice energy of MgO on Day 7 p.17?</p>",
    answer={"type": "multi", "parts": [
        {"label": "Δχ", **num_ans(dchi("Mg", "O"), sf=2, tol=0.001)},
        {"label": "consistent?", **choice(("Yes: Δχ ≥ 2.0 means ionic, and MgO has a large (very negative) lattice energy.", True, "Right."),
                                          ("No: MgO should be covalent.", False, "Δχ = 2.3 is above the ionic cutoff, Δχ ≥ 2.0 (Day 9 p.18)."))}]},
    hints=["χ(Mg) = 1.2, χ(O) = 3.5 (Day 9 p.17).", "Compare with 2.0."],
    solution=f"<p>Δχ = 3.5 − 1.2 = <strong>{dchi('Mg', 'O')}</strong> ≥ 2.0 → ionic on the slide's scale (Day 9 p.18), matching the Mg<sup>2+</sup>O<sup>2−</sup> lattice with U = −3791 kJ/mol (Day 7 p.17).</p>",
    source="Day 9 p.17–18; Day 7 p.17; " + tb("4.2", 186, 187))

P(id="t4-2-m-explain", module="t4-2", kind="mastery", level="Explain",
  prompt="<p>Why does electronegativity follow the same periodic trends as first ionization energy?</p>",
  answer={"type": "self", "model": "<p>Both measure how strongly a nucleus attracts outer electrons. Across a row, Z<sub>eff</sub> rises and atoms shrink, so the nucleus holds its own valence electrons more tightly (higher IE₁, Day 7 p.9) and pulls harder on shared bonding electrons (higher χ). "
                                   "Down a group, valence electrons are farther out and more shielded, so both decrease (textbook §4.2, Fig. 4.6). The course's χ table shows the result (Day 9 p.17); the comparison with IE₁ is the textbook's.</p>"},
  hints=[], solution="", source=tb("4.2", 186, 187) + "; Day 7 p.9; Day 9 p.17")

add(id="t4-2-m-recognize", module="t4-2", kind="mastery", level="Recognize",
    prompt="<p>“Is the bond between these two atoms polar?” What do you calculate?</p>",
    answer=choice(("the sum of their atomic masses", False, "Mass doesn't matter."), ("Δχ, their electronegativity difference", True, "Right (Day 9 p.18)."),
                  ("E<sub>el</sub>", False, "That's for ion pairs with known charges."), ("their IE₁ difference", False, "Related, but the course's measure of bond polarity is Δχ (Day 9 p.17–18).")),
    hints=["Bond polarity depends on …"],
    solution="<p><strong>Δχ</strong>, compared with the cutoffs 0.4 and 2.0 (Day 9 p.18).</p>", source="Day 9 p.17–18; " + tb("4.2", 186))

add(id="t4-2-m-sanity", module="t4-2", kind="mastery", level="Sanity check",
    prompt="<p>A student says the Br–Br bond is polar with Δχ = 2.8. What's wrong?</p>",
    answer=choice(("Nothing", False, "Two identical atoms can't differ in χ."), ("Δχ for two identical atoms is 0: Br–Br is nonpolar covalent (2.8 is Br's own χ).", True, "Right."),
                  ("Br–Br is ionic.", False, "No."), ("χ(Br) is 4.0.", False, "That's F.")),
    hints=["Δ means difference."],
    solution="<p>Δχ = 2.8 − 2.8 = <strong>0</strong>: a nonpolar covalent bond, like the even charge distribution of Cl<sub>2</sub> on Day 9 p.16.</p>", source="Day 9 p.16–18; " + tb("4.2", 186))

# =====================================================================================
# Mixed review additions x21–x35 (lecture + textbook preview; unlabeled until answered)
# =====================================================================================
def X(**kw):
    kw.setdefault("label", "preview")
    return add(module="mixed", kind="mixed", level="Mixed", **kw)

d_x21 = 45.6 / 5.20
X(id="x21", prompt="<p>A 5.20 cm<sup>3</sup> sample of a liquid has a mass of 45.6 g. What is its density?</p>",
  answer=num_ans(d_x21, sf=3, unit_label="g/cm<sup>3</sup>", units=G_CM3_UNITS),
  hints=["Mass and volume given, and a ratio asked…", "d = m/V."],
  solution=f"<p>d = 45.6 g ÷ 5.20 cm<sup>3</sup> = <strong>{num(d_x21, 3)} g/cm<sup>3</sup></strong>.</p>",
  cue="Mass and volume, ratio asked → density, d = m/V (textbook preview §1.3).", source=tb("1.3", 43), home="t1-3")

x22 = 3.14159 * 2.1
X(id="x22", prompt="<p>A calculation multiplies 3.14159 by the measured value 2.1 cm. How should the result be reported?</p>",
  answer=num_ans(x22, sf=2, tol=0.02, unit_label="cm", units=["cm"]),
  hints=["It's a multiplication: count significant figures.", "The weak link is 2.1 (2 s.f.)."],
  solution=f"<p>{fix(x22, 4)} → <strong>6.6 cm</strong> (2 s.f., set by 2.1).</p>",
  cue="× or ÷ with measured values → the fewest significant figures wins (textbook preview §1.7).", source=tb("1.7", 58), home="t1-7")

x23 = 250.0 / 2.54
X(id="x23", prompt="<p>How many inches is 250.0 cm? (1 in = 2.54 cm exactly.)</p>",
  answer=num_ans(x23, sf=4, unit_label="in", units=["in", "inch", "inches"]),
  hints=["Cancel cm.", "250.0 cm × (1 in/2.54 cm)."],
  solution=f"<p>250.0 cm × (1 in/2.54 cm) = <strong>{num(x23, 4)} in</strong> (4 s.f.; the exact factor doesn't limit).</p>",
  cue="One unit to another → a conversion factor written so the old unit cancels (textbook preview §1.8).", source=tb("1.8", 61), home="t1-8")

x24 = 0.0500 * NA
X(id="x24", prompt="<p>How many molecules are in 0.0500 mol of CO<sub>2</sub>?</p>",
  answer=num_ans(x24, sf=3),
  hints=["Moles to particles…", "× N<sub>A</sub>."],
  solution=f"<p>0.0500 mol × 6.022 × 10<sup>23</sup> mol<sup>−1</sup> = <strong>{sci(x24)} molecules</strong>.</p>",
  cue="Moles ↔ number of particles → the Avogadro constant (textbook preview §2.5).", source=tb("2.5", 98, 99), home="t2-5")

X(id="x25", prompt="<p>How many neutrons are in one atom of <sup>127</sup>I? (I: Z = 53.)</p>",
  answer=num_ans(74, tol=0),
  hints=["The symbol gives A; the element gives Z.", "Neutrons = A − Z."],
  solution="<p>127 − 53 = <strong>74</strong> neutrons.</p>",
  cue="A nuclide symbol and a particle count → A = protons + neutrons (textbook preview §2.2).", source=tb("2.2", 87, 88), home="t2-2")

m_x26 = 0.60 * 69.0 + 0.40 * 71.0
X(id="x26", prompt="<p>An element is 60.0% of an isotope with mass 69.0 amu and 40.0% of an isotope with mass 71.0 amu. What is its average atomic mass?</p>",
  answer=num_ans(m_x26, sf=3, unit_label="amu", units=U_UNITS),
  hints=["Several isotopes with abundances…", "Weighted average: 0.600(69.0) + 0.400(71.0)."],
  solution=f"<p>0.600(69.0) + 0.400(71.0) = <strong>{num(m_x26, 3)} amu</strong>.</p>",
  cue="Isotope masses plus percent abundances → weighted average (textbook preview §2.4).", source=tb("2.4", 94), home="t2-4")

X(id="x27", prompt="<p>Classify the N–O bond (χ: N 3.0, O 3.5).</p>",
  answer=choice(("nonpolar covalent", False, "Δχ = 0.5 is just above 0.4."), ("polar covalent", True, "Right: Δχ = 0.5."), ("ionic", False, "Far below 2.0."), ("metallic", False, "Two nonmetals.")),
  hints=["Take the difference in χ.", "Compare with 0.4 and 2.0."],
  solution="<p>Δχ = 0.5 → <strong>polar covalent</strong> (textbook guidelines).</p>",
  cue="“Polar or nonpolar?” for a bond → Δχ and the 0.4 / 2.0 guidelines (textbook preview §4.2).", source=tb("4.2", 186), home="t4-2")

KE_x28 = 0.5 * 1.50e3 * 20.0 ** 2
X(id="x28", prompt="<p>What is the kinetic energy of a 1.50 × 10<sup>3</sup> kg car moving at 20.0 m/s?</p>",
  answer=num_ans(KE_x28, sf=3, unit_label="J", units=J_UNITS),
  hints=["Energy of motion…", "KE = ½mu²."],
  solution=f"<p>½(1.50 × 10<sup>3</sup> kg)(20.0 m/s)<sup>2</sup> = <strong>{sci(KE_x28)} J</strong>.</p>",
  cue="Mass and speed, energy asked → KE = ½mu² (textbook preview §1.5). Not λ = h/(mu), which gives a wavelength.", source=tb("1.5", 50), home="t1-5")

data_x29 = [4.8, 5.2, 5.0, 5.1, 4.9]
X(id="x29", prompt="<p>Five repeated measurements: 4.8, 5.2, 5.0, 5.1, and 4.9 mL. What is the standard deviation?</p>",
  answer=num_ans(stdev(data_x29), sf=2, tol=0.02, unit_label="mL", units=ML_UNITS),
  hints=["Spread of repeated results…", "s = √[Σ(x<sub>i</sub> − x̄)<sup>2</sup>/(n − 1)], with x̄ = 5.0."],
  solution=f"<p>x̄ = 5.0 mL. Deviations −0.2, 0.2, 0, 0.1, −0.1; their squares 0.04, 0.04, 0, 0.01, 0.01 sum to Σ(x<sub>i</sub> − x̄)<sup>2</sup> = 0.10; s = √(0.10/4) = <strong>{fix(stdev(data_x29), 2)} mL</strong>.</p>",
  cue="Repeated measurements, precision asked → standard deviation with n − 1 (textbook preview §1.9).", source=tb("1.9", 66), home="t1-9")

X(id="x30", prompt="<p>Water vapor forms droplets on a cold glass. Name the change, and say whether energy is absorbed or released.</p>",
  answer=choice(("condensation; released", True, "Right."), ("condensation; absorbed", False, "Going toward liquid releases energy."), ("deposition; released", False, "Deposition makes a solid."), ("vaporization; absorbed", False, "That's liquid → gas.")),
  hints=["Gas → liquid."],
  solution="<p><strong>Condensation</strong>, which <strong>releases</strong> energy (textbook Fig. 1.10).</p>",
  cue="A change of state → name it by its start and end states; toward solid releases energy (textbook preview §1.4).", source=tb("1.4", 48, 49), home="t1-4")

du_x31 = heis_du(ME, 2.0e-10)
X(id="x31", prompt="<p>An electron's position is known to within 2.0 × 10<sup>−10</sup> m. What is the minimum uncertainty in its speed? (m<sub>e</sub> = 9.109 × 10<sup>−31</sup> kg; h = 6.626 × 10<sup>−34</sup> J·s)</p>",
  answer=num_ans(du_x31, sf=2, tol=0.02, unit_label="m/s", units=MS_UNITS),
  hints=["Uncertainty in position → uncertainty in speed…", "Δu ≥ h/(4π m Δx)."],
  solution=f"<p>Δu ≥ 6.626 × 10<sup>−34</sup> ÷ (4π × 9.109 × 10<sup>−31</sup> × 2.0 × 10<sup>−10</sup>) = <strong>{sci(du_x31, 2)} m/s</strong>.</p>",
  cue="Uncertainties in position and speed → Heisenberg, Δx·mΔu ≥ h/(4π) (textbook preview §3.5).", source=tb("3.5", 137), home="t3-5")

X(id="x32", prompt="<p>A photoelectron spectrum has three peaks with relative heights 2, 2, and 3. Which element is it?</p>",
  answer=sym_ans("N", "nitrogen"),
  hints=["Peak heights count electrons.", "1s<sup>2</sup>2s<sup>2</sup>2p<sup>3</sup>."],
  solution="<p>2 + 2 + 3 = 7 electrons → <strong>N</strong>.</p>",
  cue="Peaks with relative heights → PES: heights count the electrons in each subshell (textbook preview §3.11).", source=tb("3.11", 162, 163), home="t3-11")

X(id="x33", prompt="<p>Classify pure table salt, NaCl.</p>",
  answer=choice(("element", False, "Two elements are combined."), ("compound", True, "Right: a pure substance of Na<sup>+</sup> and Cl<sup>−</sup> in a fixed 1 : 1 ratio."), ("homogeneous mixture", False, "Fixed composition, so not a mixture."), ("heterogeneous mixture", False, "Uniform, and pure.")),
  hints=["Fixed composition? Made of more than one element?"],
  solution="<p>A <strong>compound</strong> (an ionic one: Day 7 p.14 covers the bond type; textbook §1.3 the classification).</p>",
  cue="“Element, compound, or mixture?” → the Fig. 1.2 questions (textbook preview §1.3).", source=tb("1.3", 43) + "; Day 7 p.14", home="t1-3")

mm_x34 = molar_mass("Na2O")
X(id="x34", prompt="<p>What is the molar mass of the ionic compound formed by sodium and oxygen? (Na 22.990, O 15.999 g/mol.)</p>",
  answer=num_ans(mm_x34, sf=5, unit_label="g/mol", units=GMOL_UNITS),
  hints=["First the formula: Na<sup>+</sup> and O<sup>2−</sup> (Day 7 p.19–20).", "Na<sub>2</sub>O: 2(22.990) + 15.999."],
  solution=f"<p>Formula Na<sub>2</sub>O (charge balance, Day 7 p.20); molar mass = 2(22.990) + 15.999 = <strong>{fix(mm_x34, 3)} g/mol</strong>.</p>",
  cue="Two steps hidden in one: write the ionic formula (lecture, Day 7 p.18–20), then add molar masses (textbook preview §2.5).", source="Day 7 p.19–20; " + tb("2.5", 100), home="t2-5")

X(id="x35", prompt="<p>A compound's mass spectrum has its highest-mass prominent peak at m/z = 44. Which formula fits?</p>",
  answer=choice(("CO<sub>2</sub>", True, "Right: 12.011 + 2(15.999) = 44.01."), ("H<sub>2</sub>O", False, "18."), ("CH<sub>4</sub>", False, "16."), ("N<sub>2</sub>", False, "28.")),
  hints=["The molecular ion's m/z ≈ the molecular mass."],
  solution="<p><strong>CO<sub>2</sub></strong> (44.01 amu). <span class='bg'>Propane, C<sub>3</sub>H<sub>8</sub>, is also about 44; distinguishing them needs the fragment pattern or higher-resolution masses.</span></p>",
  cue="“Molecular-ion peak at m/z = …” → mass spectrometry; M<sup>+</sup> ≈ molecular mass (textbook preview §2.6).", source=tb("2.6", 104, 105), home="t2-6")

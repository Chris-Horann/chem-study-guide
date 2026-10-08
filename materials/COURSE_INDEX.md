# Course Index

Cumulative understanding of lecture slides, lecture notes, and professor review
material, organized by CONCEPT (not by file). Maintained by `/ingest-course`;
merge new sources into existing concepts instead of appending per-file dumps.
Homework analysis lives in `HOMEWORK_INDEX.md`; textbook locations live in
`TEXTBOOK_MAP.md`.

**Status:** INGESTED — Day 1–11 lecture slides (275 PDF pages: Day 1–8 187,
Day 9 30, Day 10 31, Day 11 27), every page visually inspected at 220 DPI, with
300–400 DPI zooms wherever notation was small or the text layer was garbled. No
lecture notes, review sheets, homework, or image files have been supplied yet.
Last updated 2026-10-05 (Day 9–11).

**Citation key:** `Day N p.X` = `materials/lectures/Day N Lecture Slides.pdf`,
physical PDF page X (one slide per page). `TB PDF p.X (printed Y)` = the Gilbert
textbook PDF (see `TEXTBOOK_MAP.md`; printed = PDF − 34 in Ch. 1–5). "Top Hat" =
an in-class clicker question; its text is known only when it is on the slide.
Non-content slides (announcements, "Representation Matters", generic Top Hat
instructions) are summarized in `COURSE.md`, not here.

## Conventions

- Every bullet carries a label: `[SOURCE-DERIVED]`, `[SUPPORTED EMPHASIS]`,
  `[INFERRED]`, `[CLARIFICATION]`, `[VERIFICATION]`, `[UNCERTAIN]`.
- Every SOURCE-DERIVED or SUPPORTED EMPHASIS bullet cites `file p.N` (1-based
  physical PDF page; slide number = page number for slide decks).
- Chemistry notation is transcribed from the rendered page, not the text layer,
  using Unicode sub/superscripts: SO₄²⁻, Fe³⁺, ΔH°, ⇌, →, e⁻.
- Quote the professor's wording when the wording itself matters.
- UNCERTAIN entries say what could not be read and where, e.g.
  `[UNCERTAIN] Day 4 p.7: handwritten exponent on K could be 10⁻⁵ or 10⁻⁸`.

## Concept entry template

Copy this block for each concept. Omit empty fields rather than padding them.

```markdown
## <Concept name, using the professor's term>

**Sources:** Day N Lecture Slides.pdf p.a–b; <notes/review file> p.c
**Unit / lecture order:** <where it sits in the course>
**Prerequisites:** <concepts> (see COURSE_MAP.md)
**Emphasis evidence:** <repetition count, "exam" callouts, review placement,
highlighting, or "none observed">

### Definitions and terminology
- [SOURCE-DERIVED] … (file p.)

### Equations and relationships
- [SOURCE-DERIVED] <equation> — variables, units, stated conditions (file p.)

### Three representations
- Macroscopic: …
- Symbolic: …
- Particulate: …

### Professor explanations, models, and diagrams
- [SOURCE-DERIVED] … (file p.) — describe diagrams/graphs: axes, labels, what they show

### Worked examples
- (file p.) <problem gist> — method used, steps shown, answer format, sig figs

### Procedures, shortcuts, assumptions, warnings
- [SOURCE-DERIVED] …

### Recognition cues
- [SOURCE-DERIVED]/[INFERRED] …

### Common mistakes flagged
- [SOURCE-DERIVED] … (only if the materials flag them) / [INFERRED] …

### Connections
- Builds on: … ; Used later in: … (file p.)

### Uncertainties and discrepancies
- [UNCERTAIN] … / textbook disagreement → logged in COURSE.md
```

## Concepts

Ordered as taught. The unit groupings match `COURSE_MAP.md`.

---

# Unit A — Matter and Atomic Theory (Ch. 1; Day 1)

## Before Atomic Theory: Conservation of Mass, Constant Composition, and Multiple Proportions

**Sources:** Day 1 p.6–13
**Unit / lecture order:** Day 1, first chemistry content of the course
**Prerequisites:** mass-percent arithmetic; significant figures (Ch. 1 outcome 6, listed but not lectured)
**Emphasis evidence:** §1.1 is the only bold section on the Ch. 1 list (Day 1 p.6) and outcome 1 the only bold outcome (Day 1 p.7); the multiple-proportions numbers 8.00, 16.00, and 2:1 are printed in red (Day 1 p.13).

### Definitions and terminology
- [SOURCE-DERIVED] Ancient atomism: Leucippus and Democritus (ca. 400 BCE) coined "atomos" ("uncuttable"); all matter is made of tiny particles, and a material's properties depend on the kind of atoms in it; "dangerously close to the truth" (Day 1 p.8). The slides call this account "very Eurocentric" (Indian, Hindu, Buddhist, Islamic, and medieval European writings also exist) and return to Boyle and Newton (1600s) "since this isn't a history or philosophy class" (Day 1 p.8–9).
- [SOURCE-DERIVED] Law of Conservation of Mass (credited to Lavoisier, "but maybe it should be Mikhail Lomonosov"): "matter can neither be created nor destroyed"; the law was hidden for centuries "because of the difficulty of tracking the mass of *gases* in reactions" (Day 1 p.10).
- [SOURCE-DERIVED] Law of Constant Composition, or Law of Definite Proportions (Proust, 1797): "The same compound will always be composed of its constituent elements in the same proportion by mass" (Day 1 p.11).
- [SOURCE-DERIVED] Law of Multiple Proportions (Dalton, 1803): "When two elements combine to make two (or more) compounds, the ratio of the masses of one of the elements which combine with a given mass of the second element is always a ratio of small whole numbers" (Day 1 p.13).

### Equations and relationships
- [SOURCE-DERIVED] Mass percent: 1.01 / (1.01 + 8.00) × 100% = 11.2% (Day 1 p.11; the slide types "x100%"). Mass of the element ÷ total mass × 100%.

### Three representations
- Macroscopic: [SOURCE-DERIVED] measured masses: 1.01 g H per 8.00 g O in water, and 1.01 g H per 16.00 g O in hydrogen peroxide (Day 1 p.11, p.13).
- Symbolic: [SOURCE-DERIVED] H₂O vs H₂O₂ (Day 1 p.13); the mass-percent calculation (Day 1 p.11).
- Particulate: [INFERRED] a fixed mass ratio means a fixed atom ratio; H₂O₂ has twice as many O atoms per H atom as H₂O, so the O mass per fixed H mass doubles.

### Professor explanations, models, and diagrams
- [SOURCE-DERIVED] Early resistance to Proust: tin oxide seemed to have variable tin content, but the experiments were studying *different* tin compounds ("we'll have a Law for that on the next slide!"); even Proust's supporters could not say *why* the law held (Day 1 p.12).

### Worked examples
- (Day 1 p.11) Water is 11.2% hydrogen by mass, "the remaining 88.8% is oxygen." Method: mass fraction × 100%, O found by difference. Inputs have 3 s.f., so the answer has 3 s.f. [VERIFICATION: 1.01/9.01 = 0.11210 → 11.2%; Python]
- (Day 1 p.13) At a fixed 1.01 g of H, the O masses are 8.00 g (H₂O) and 16.00 g (H₂O₂), a 2:1 ratio of small whole numbers. [VERIFICATION: 16.00/8.00 = 2.000]

### Recognition cues
- [INFERRED] "Same compound from any source has the same % by mass" → constant composition. "Two compounds of the same two elements; compare one element's mass per fixed mass of the other" → multiple proportions; expect a small whole-number ratio.

### Common mistakes flagged
- [INFERRED] Comparing the two compounds' percent compositions directly instead of first fixing the mass of one element.

### Connections
- Used later in: Dalton's atomic theory, which explains "all three of these Laws" (Day 1 p.14).

### Uncertainties and discrepancies
- [CLARIFICATION] Day 1 p.8 says atomism was "discovered again in Aristotle"; historically Aristotle argued against atomism (his critiques preserved the idea). History phrasing only.

## Dalton's Atomic Theory

**Sources:** Day 1 p.14, p.18; Day 2 p.2, p.12
**Unit / lecture order:** Day 1
**Prerequisites:** the three laws above
**Emphasis evidence:** none observed beyond its place as the payoff of the Day 1 sequence.

### Definitions and terminology
- [SOURCE-DERIVED] "In 1808, Dalton hypothesized an explanation for all three of these Laws, which later became known as atomic theory: • Matter consists of **atoms**, which are the smallest identifiable unit of **matter** and cannot be destroyed. • All atoms of the same **element** are identical to each other, but are different than atoms of any other element. • Atoms combine in small whole-number ratios when forming compounds." (Day 1 p.14)

### Professor explanations, models, and diagrams
- [SOURCE-DERIVED] "Atomic Theory ruled for nearly 100 years", until experiments beginning in 1897 ***disproved*** that the atom is the smallest unit of matter (Day 1 p.18; Day 2 p.12).

### Connections
- Builds on: the laws of chemical combination (Day 1 p.14). Used later in: the discovery of subatomic particles overturns postulate 1 (Day 1 p.18); [INFERRED] isotopes (Day 2 p.23) overturn "all atoms of the same element are identical", though the slides do not say so.

### Uncertainties and discrepancies
- [CLARIFICATION] The textbook dates Dalton's theory to 1803 (TB PDF p.40, printed 6); the slide says 1808 (Day 1 p.14). History detail → COURSE.md Discrepancies.

## Conservation of Energy and Mass–Energy

**Sources:** Day 1 p.7, p.15; Day 3 p.2
**Unit / lecture order:** Day 1
**Emphasis evidence:** [SUPPORTED EMPHASIS] explicit instructor statement in the slide title: "Other Laws we need from Chapter 1" (Day 1 p.15).

### Definitions and terminology
- [SOURCE-DERIVED] Law of Conservation of Energy: "In the course of **normal** physical and chemical processes, energy cannot be created or destroyed, but it can be converted from one form to another" (Day 1 p.15).
- [SOURCE-DERIVED] Law of Conservation of Mass-Energy: "While the total mass and energy of a system is conserved, mass and energy can interconvert", E = mc² (Day 1 p.15).

### Equations and relationships
- [SOURCE-DERIVED] E = mc² (Day 1 p.15); variables not defined on the slide. [CLARIFICATION: E energy (J), m mass (kg), c = 2.998 × 10⁸ m/s (value on Day 2 p.30).]

### Professor explanations, models, and diagrams
- [SOURCE-DERIVED] A "Representation Matters" slide shows a nuclear transmutation, ²⁷Al + α → ³⁰P + ¹n; the text layer drops the α (Day 3 p.2, 400-dpi zoom). [VERIFICATION: mass numbers 27 + 4 = 30 + 1; atomic numbers 13 + 2 = 15 + 0.]

### Connections
- [INFERRED] "normal" separates chemical processes, where mass is conserved, from nuclear processes like Day 3 p.2, where mass and energy interconvert. The mass defect hidden in "6 protons + 6 neutrons = 12 amu" (Day 2 p.21) is the same idea.
- [INFERRED] Energy bookkeeping underlies KE = hν − φ (Day 3 p.19) and photon energy = |ΔE| (Day 4 p.10).

### Uncertainties and discrepancies
- [UNCERTAIN] Heat, work, and potential and kinetic energy (Ch. 1 outcome 4 and §1.5, both italic, Day 1 p.6–7) are listed but not lectured; whether they are examinable is not stated.

## Listed but Not Lectured: Ch. 1 §1.3–1.8 and Ch. 2 §2.2–2.5 Topics

**Sources:** Day 1 p.6–7, p.16–17; Day 2 p.4–5, p.24
**Emphasis evidence:** printed in italic on the chapter slides, neither bold nor grey.

- [SOURCE-DERIVED] Ch. 1 italic sections: 1.3 Classes and Properties of Matter; 1.4 States of Matter; 1.5 Forms of Energy; 1.6 Formulas and Models; 1.7 Expressing Experimental Results; 1.8 Unit Conversions and Dimensional Analysis. Italic outcomes 2–7 cover classes of matter and physical vs. chemical properties, states of matter at the particle level, heat, work, and potential and kinetic energy, formulas and models, exact vs. uncertain values with significant figures, and unit conversion (Day 1 p.6–7).
- [SOURCE-DERIVED] Ch. 2 italic sections: 2.2 Nuclides and Their Symbols; 2.3 Navigating the Periodic Table; 2.4 The Masses of Atoms, Ions, and Molecules; 2.5 Moles and Molar Masses. Italic outcomes 2–6 cover nuclide symbols → p, n, e⁻ counts; periodic-table properties; average atomic mass from abundances; mass ↔ particles ↔ moles; and molar masses (Day 1 p.16–17; Day 2 p.4–5).
- [SOURCE-DERIVED] Grey (de-emphasized) items: 1.2 COAST: A Framework for Solving Problems; 1.9 Analyzing Experimental Results; 2.6 Mass Spectrometry; Ch. 2 outcome 7 (mass spectra) (Day 1 p.6, p.16–17).
- [SOURCE-DERIVED] The Ch. 2 italic topics match what the professor delegates: "RAMP UP has lots more to say about the periodic table, isotopes, ions, nuclide symbols, etc." (Day 2 p.24).
- [INFERRED] Formatting key: bold = lectured that day; italic = assigned outside lecture (RAMP UP); grey = not covered. [UNCERTAIN] The slides never state this key; confirm with the syllabus or professor.
- [SOURCE-DERIVED] "Ramp Up IS on this exam" (Day 10 p.2; Day 11 p.2), so the RAMP UP topics named on Day 2 p.24 (periodic table, isotopes, ions, nuclide symbols) are on Midterm 1. [INFERRED] The other italic Ch. 1–2 topics (sig figs, unit conversion, moles) are probably RAMP UP too, but the slides only list the Day 2 p.24 ones.
- [SOURCE-DERIVED] Later lectures use these skills without teaching them: g → kg and 1 J = 1 kg·m²/s² in the de Broglie examples (Day 4 p.11–14); significant figures in every worked answer (Day 1 p.11; Day 4 p.12, p.14); kJ/mol quantities (Day 7 p.9–17), which presuppose the mole.

---

# Unit B — Atoms, Ions, and Molecules (Ch. 2 §2.1; Day 1 p.16–20, Day 2 p.4–24)

## The Discovery of the Subatomic: Thomson, Millikan, and Rutherford

**Sources:** Day 1 p.16–20; Day 2 p.4–18
**Unit / lecture order:** begins at the end of Day 1 (p.18–20); main treatment Day 2 p.6–18
**Prerequisites:** Dalton's atomic theory; [INFERRED] opposite charges attract, and magnetic fields deflect moving charges
**Emphasis evidence:** §2.1 is the only bold Ch. 2 section, and outcome 1 ("Explain how the experiments of Thomson, Millikan, and Rutherford contributed to our understanding of atomic structure") the only bold Ch. 2 outcome (Day 1 p.16–17; repeated Day 2 p.4–5). The cathode-ray-tube diagram appears in two lectures (Day 1 p.20; Day 2 p.6).

### Definitions and terminology
- [SOURCE-DERIVED] 1897: J.J. Thomson discovered the **electron** in cathode-ray-tube experiments (Day 1 p.18; Day 2 p.12).
- [SOURCE-DERIVED] 1909: Robert Millikan determined the mass and charge of the electron with an oil-droplet experiment (Day 2 p.12).
- [SOURCE-DERIVED] 1911: Ernest Rutherford* showed that "the vast majority of the mass of an atom was in the nucleus" in a gold foil experiment (Day 2 p.14).

### Equations and relationships
- [SOURCE-DERIVED] q_e = −1.602 × 10⁻¹⁹ C; m_e = 9.109 × 10⁻²⁸ g "(!!!)"; "The mass of the smallest atom (H) is **2000 times** larger than that!" (Day 2 p.12). [VERIFICATION: m_H/m_e = 1.00794 / 5.48580 × 10⁻⁴ = 1837; "2000" is a rounded figure.]

### Three representations
- Macroscopic: a glowing tube whose beam bends toward the + plate or in a magnetic field (Day 1 p.19–20; Day 2 p.6–8); flashes on a fluorescent screen, a few at large angles (Day 2 p.15, p.18).
- Symbolic: ⊖/⊕ charges in the diagrams; q_e and m_e values (Day 2 p.12).
- Particulate: tiny negative electrons in every atom; plum pudding (diffuse positive charge) vs. the nuclear model (a tiny, dense, positive nucleus in a diffuse electron cloud) (Day 2 p.11, p.16–17).

### Professor explanations, models, and diagrams
- [SOURCE-DERIVED] Photos of a cathode ray tube with a Maltese-cross target, off and on (blue glow near the cathode; green glow and the cross's shadow at the far end) (Day 1 p.19). [CLARIFICATION: the sharp shadow shows the rays travel in straight lines from the cathode.]
- [SOURCE-DERIVED] Labeled CRT (Day 1 p.20; Day 2 p.6): cathode (−) and anode (+) on a high-voltage source, evacuated tube, S/N magnets, beam bent onto a phosphorescent spot. With charged plates the beam bends toward the + plate (Day 2 p.7); with magnets and plates together it goes straight (Day 2 p.8).
- [SOURCE-DERIVED] Thomson's reasoning: deflected by a magnet, so "it has mass and charge"; deflected toward the + plate, so "it's negatively charged"; the two effects "pitted against each other" show "it's TINY". So atoms contain very small negatively charged particles (Day 2 p.10). [CLARIFICATION: balancing the deflections gives the charge-to-mass ratio; the slide does not use that term.]
- [SOURCE-DERIVED] Plum-pudding model (1904): "Positive charge distributed throughout spherical atom" with embedded electrons, because electrons are inside atoms, "atoms are usually uncharged… so there must also be a *positive* charge inside every atom!" (Day 2 p.11)
- [SOURCE-DERIVED] Millikan apparatus, no explanatory text: an atomizer sprays oil drops through a hole in the upper positive plate; X-rays cross the gap; negative lower plate; microscope (Day 2 p.13).
- [SOURCE-DERIVED] Gold foil: α emitter → beam of α particles → thin gold foil inside a ring-shaped fluorescent screen; most particles pass straight through; some are "deflected by collisions with nucleus" (Day 2 p.15, p.18). Quote: "It was almost as if you had fired a 15-inch shell at a piece of tissue paper and it came back and hit you" (Day 2 p.15; no speaker named on the slide, but the textbook attributes it to Rutherford, TB PDF p.85).
- [SOURCE-DERIVED] Prediction vs. result: under plum pudding every α path goes essentially straight through (Day 2 p.16); under the nuclear model the α aimed at the nucleus is thrown back (Day 2 p.17).

### Recognition cues
- [INFERRED] "Bent by an electric/magnetic field" → charged; "toward the + plate" → negative; "most pass through, a few bounce back" → mostly empty space around a tiny, dense, positive nucleus.

### Common mistakes flagged
- [INFERRED] Thinking α particles bounce off electrons. Electrons are far too light (≈ 1/1837 of H, Day 2 p.12); only the massive nucleus can turn an α particle back.

### Connections
- Builds on: Dalton's atomic theory (Day 1 p.18). Used later in: the nuclear atom (Day 2 p.19); Bohr's model starts from Rutherford's nucleus (Day 4 p.8).

### Uncertainties and discrepancies
- [UNCERTAIN] Day 2 p.14: "Rutherford*" has an asterisk with no footnote on any slide. [CLARIFICATION: Geiger and Marsden ran the experiments under Rutherford (TB PDF p.85), which may be what the asterisk flags.]
- [CLARIFICATION] The oil-drop experiment measured the electron's charge; the mass followed from Thomson's charge-to-mass ratio (TB PDF p.83). The slide compresses this (Day 2 p.12).
- [SOURCE-DERIVED] A Top Hat question was asked on Day 2 p.9; its text is not in the PDF.

## The Nuclear Atom

**Sources:** Day 2 p.17–20
**Unit / lecture order:** Day 2
**Prerequisites:** the discovery of the subatomic
**Emphasis evidence:** none observed beyond the bold §2.1.

### Definitions and terminology
- [SOURCE-DERIVED] "The nucleus is the positively charged center of atom, containing nearly all the mass of the atom. The nucleus is about 1/10,000 the size of the atom. It consists of two types of particles: Protons: positively charged subatomic particles. Neutrons: electronically [sic] neutral subatomic particles." (Day 2 p.19)

### Professor explanations, models, and diagrams
- [SOURCE-DERIVED] Figure: a nucleus of dark neutrons and light protons "~0.01 pm" across, inside a gold atom's blue electron cloud "~288 pm" across (Day 2 p.20).

### Three representations
- Particulate: a tiny, dense nucleus (protons + neutrons) inside a diffuse electron cloud that fills most of the volume (Day 2 p.17, p.20).

### Connections
- Builds on: the gold-foil results (Day 2 p.14–18). Used later in: RAMP UP particle properties (Day 2 p.21–24); the Bohr model (Day 4 p.8).

### Uncertainties and discrepancies
- [VERIFICATION] The figure's 0.01 pm / 288 pm = 1/28,800, vs. "about 1/10,000" in the text (Day 2 p.19). Both are order-of-magnitude statements; the textbook caption gives 1/10,000 for the same figure (TB PDF p.86). → COURSE.md Discrepancies.

## RAMP UP Content: Atomic Mass Units, Subatomic Particles, Isotopes, and the Periodic Table

**Sources:** Day 2 p.21–24 (grey-background slides boxed in red: "RAMP UP CONTENT!")
**Unit / lecture order:** Day 2; shown in lecture but labeled as RAMP UP self-study material
**Prerequisites:** the nuclear atom
**Emphasis evidence:** [SOURCE-DERIVED] explicit delegation: "RAMP UP has lots more to say about the periodic table, isotopes, ions, nuclide symbols, etc." (Day 2 p.24).

### Definitions and terminology
- [SOURCE-DERIVED] "Atomic mass units (amu) are the unit used to express the *relative* masses of atoms and subatomic particles. 1 amu is equal to 1/12 of the mass of a carbon atom (specifically, a carbon-12 atom). 6 protons + 6 neutrons = 12 amu. 1 amu = 1 dalton (Da)." (Day 2 p.21, repeated p.23)
- [SOURCE-DERIVED] "But not all carbon atoms have an atomic mass of 12 amu! SOME carbon atoms have 'extra' neutrons. Another way of saying this is that there is more than one **isotope** of carbon." (Day 2 p.23)
- [SOURCE-DERIVED] "An element's position in the table is determined by the number of protons in the nucleus"; "Elements in the same **group** (column) have similar chemical properties" (Day 2 p.24).

### Equations and relationships
- [SOURCE-DERIVED] Properties of subatomic particles (Day 2 p.22) — Particle | Symbol | Mass (amu) | Mass Number | Mass (kg) | Charge (relative) | Charge (C):
  Neutron | ¹₀n | 1.00866 | 1 | 1.67483 × 10⁻²⁷ | 0 | 0 ·
  Proton | ¹₁p | 1.00728 | 1 | 1.67262 × 10⁻²⁷ | 1+ | +1.60218 × 10⁻¹⁹ ·
  Electron | ⁰₋₁e | 5.48580 × 10⁻⁴ | 0 | 9.10938 × 10⁻³¹ | 1− | −1.60218 × 10⁻¹⁹.
  Relative charges are written magnitude-then-sign ("1+", "1−").

### Professor explanations, models, and diagrams
- [SOURCE-DERIVED] Periodic table (groups 1–18, periods 1–7; callouts "Atomic number" and "Symbol for element") shaded in three colors with no legend (Day 2 p.24). [INFERRED: tan = metals; green = metalloids (B, Si, Ge, As, Sb, Te, At); blue = nonmetals.]

### Uncertainties and discrepancies
- [VERIFICATION] The neutron's mass in kg is printed 1.67483 × 10⁻²⁷ (Day 2 p.22), but the textbook's Table 2.1 prints 1.67493 × 10⁻²⁷ kg (TB PDF p.87, printed 53), and 1.00866 u × 1.66054 × 10⁻²⁷ kg/u = 1.67493 × 10⁻²⁷ kg. Slide typo → COURSE.md Discrepancies.
- [CLARIFICATION] "6 protons + 6 neutrons = 12 amu" counts mass numbers. The table's free-particle masses sum to 12.0956 amu (12.0989 with 6 electrons), more than the defined 12 amu of a ¹²C atom; the difference is nuclear binding energy (mass–energy, Day 1 p.15). [VERIFICATION: Python]
- [CLARIFICATION] Terminology: the professor says "amu"; the textbook says "unified atomic mass unit (u)" = dalton (TB PDF p.86) → TEXTBOOK_MAP Convention differences.
- [UNCERTAIN] What RAMP UP is (platform, module, or reading) is not stated in the slides.
- [SUPPORTED EMPHASIS] Exam status, resolved by an explicit instructor statement repeated in two lectures: "Reminder: Ramp Up IS on this exam, and you get extra credit in this class based on how much Ramp Up you do before next Thursday" (Day 10 p.2; Day 11 p.2), i.e., Midterm 1.

---

# Unit C — Atomic Structure: Explaining the Properties of Elements (Ch. 3; Day 2 p.25 – Day 7 p.11)

## Electromagnetic Radiation: Wavelength, Frequency, and Energy

**Sources:** Day 2 p.25–30; Day 3 p.12
**Unit / lecture order:** Day 2, start of Ch. 3
**Prerequisites:** scientific notation; unit prefixes such as nm (INFERRED)
**Emphasis evidence:** §3.1 and outcome 1 bold (Day 2 p.25–26); the EM-spectrum figure appears in two lectures (Day 2 p.29; Day 3 p.12); a Top Hat ranking question was prepared (Day 2 p.28).

### Equations and relationships
- [SOURCE-DERIVED] "Speed of light, c = 2.998 × 10⁸ m/s"; λν = c; ν = c/λ; E = hν (Day 2 p.30). λ = wavelength (m); ν = frequency (s⁻¹, Hz); E = energy of one photon (J); h = Planck's constant (value on Day 3 p.17). [CLARIFICATION: at fixed c, λ and ν are inversely proportional, and E ∝ ν ∝ 1/λ.]

### Three representations
- Macroscopic: visible colors; radio, microwave, IR, UV, X-ray, and γ-ray technologies (photo strip, Day 2 p.29).
- Symbolic: λν = c; E = hν; wave diagrams.
- Particulate: [INFERRED] light as a wave with a wavelength and frequency (Day 2 p.30); the photon (particle) picture arrives on Day 3 p.17.

### Professor explanations, models, and diagrams
- [SOURCE-DERIVED] EM spectrum (Day 2 p.29; Day 3 p.12): γ rays | X-rays | ultraviolet | visible | infrared | microwave | radio. "Approximate frequencies, Hz" run 10²⁴ → 10⁴ left to right; "Approximate wavelengths, m" run 10⁻¹⁶ → 10⁴. Visible is expanded as 400–750 nm, violet to red. The γ end is labeled "Shortest wavelength (Highest energy)"; the radio end "Longest wavelength (Lowest energy)".
- [SOURCE-DERIVED] Two waves on the same axis, with λ_A twice λ_B (Day 2 p.30). [INFERRED: B has twice A's frequency.]

### Worked examples
- [SUPPORTED EMPHASIS] Top Hat, prepared but not done ("We didn't actually do the second question today, but it *would* have been this"): "Rank the following types of electromagnetic radiation by wavelength, with the longest wavelength at the top": A Infrared, B Ultraviolet, C Green, D Orange, E X-Rays (Day 2 p.28). The slide gives no answer. Reference: infrared > orange > green > ultraviolet > X-rays. [VERIFICATION: against the Day 2 p.29 scale]

### Recognition cues
- [INFERRED] λ given and ν or photon energy asked → λν = c, then E = hν (or E = hc/λ, written on Day 4 p.10). A color or region name → locate it on the spectrum.

### Common mistakes flagged
- [INFERRED] Using λ in nm with c in m/s; assuming a longer wavelength means more energy (the figure labels the opposite).

### Uncertainties and discrepancies
- [SOURCE-DERIVED] Frequency is typeset as the italic "𝑣" glyph on Day 2 p.30 and Day 3 p.17 but as Greek ν on Day 3 p.19, Day 4 p.10, and Day 7 p.9; the text layer drops or garbles both. Read either as ν (frequency).
- [SOURCE-DERIVED] The Day 2 p.27 Top Hat question is not in the PDF.

## Atomic Spectra: The Solar Spectrum, Emission, and Absorption

**Sources:** Day 2 p.31; Day 3 p.7–11, p.21; Day 4 p.6
**Unit / lecture order:** end of Day 2 into Day 3
**Prerequisites:** EM radiation (wavelength scale)
**Emphasis evidence:** §3.2 bold (Day 2 p.25; Day 3 p.5); the hydrogen emission spectrum is shown three times (Day 3 p.9, p.21; Day 4 p.6); "absence" and "opposite" printed bold (Day 2 p.31; Day 3 p.7–8).

### Definitions and terminology
- [SOURCE-DERIVED] Solar spectrum (Wollaston 1802, Fraunhofer): sunlight through a prism is "NOT continuous, but contained series of very narrow dark lines; the **absence** of light at specific wavelengths". These are the Fraunhofer lines (Fraunhofer is credited because his numbers were better); "Importantly, they had no explanation" (Day 2 p.31; Day 3 p.7).
- [SOURCE-DERIVED] Atomic emission (Bunsen and Kirchhoff): element samples burned in a flame gave "very incomplete spectra with a few lines", the **opposite** of Wollaston's result (Day 3 p.8).
- [SOURCE-DERIVED] Absorption: light through elemental samples gave spectra that were "mostly continuous, with characteristic gaps", like Wollaston's. Partial explanation: "light is emitted continuously by the sun, but is absorbed by elements in the solar atmosphere" (Day 3 p.10).
- [SOURCE-DERIVED] "The Limits of Classical Physics": the existing theories "couldn't explain WHY different elements absorbed and emitted different wavelengths of light" (Day 3 p.11).

### Three representations
- Macroscopic: flame colors; bright lines; dark lines in sunlight (Day 3 p.8–10).
- Symbolic: spectra drawn against a 400–700 nm wavelength scale (Day 3 p.9–10).
- Particulate: [INFERRED, explained by Bohr on Day 4 p.10] each line is one specific energy change of an electron in the atom.

### Professor explanations, models, and diagrams
- [SOURCE-DERIVED] Emission spectra of H, He, and Ne on a 400–700 nm scale (Day 3 p.9). H has four lines (two violet, one blue-green, one red); He has several, including a bright yellow; Ne has many, crowded into orange–red. [VERIFICATION: the Balmer formula gives H lines at 410.1, 434.0, 486.1, 656.2 nm.]
- [SOURCE-DERIVED] Absorption setup: white-light source → sample → slit → prism → screen. Absorption spectra of H, He, and Ne are shown, with H's emission lines overlaid at the same positions as its dark absorption lines (Day 3 p.10).
- [SOURCE-DERIVED] A spectroscope with a burner and a single bright yellow emission line, element unlabeled (Day 3 p.8).

### Recognition cues
- [INFERRED] Dark lines on a continuous background → absorption; bright lines on a dark background → emission; the same element gives the same wavelengths either way (Day 3 p.10 overlay).

### Connections
- Used later in: Planck's quantization (Day 3 p.11); Balmer's formula (Day 3 p.21; Day 4 p.6–7); Bohr's energy levels (Day 4 p.10).

## Blackbody Radiation and Planck's Quantization of Energy

**Sources:** Day 3 p.11–17
**Unit / lecture order:** Day 3
**Prerequisites:** atomic spectra; E = hν and frequency (Day 2 p.30)
**Emphasis evidence:** §3.3 bold (Day 3 p.5); "SHOCKING" and "ANY" in capitals (Day 3 p.16–17).

### Definitions and terminology
- [SOURCE-DERIVED] Kirchhoff's studies of blackbody radiation "prompted the first theory able to support these experiments: Planck's hypothesis about the quantization of energy" (Day 3 p.11).
- [SOURCE-DERIVED] Planck (1900) was optimizing emission from Edison's "newfangled 'light bulb'", found that classical physics couldn't explain it, and made a "SHOCKING assumption": "Light is emitted from objects in discrete 'packets' that he called 'quanta'" (Day 3 p.16).
- [SOURCE-DERIVED] "Planck: light can't be emitted with ANY arbitrary amount of energy; it's a staircase, not a ramp. Each quantum of light emitted has energy equal to some constant (now 'Planck's constant') times the frequency of the light: E = hν where h = 6.626 × 10⁻³⁴ J·s. Today, we call these 'packets' of light **photons**." (Day 3 p.17; a photo shows a ramp beside a staircase)

### Equations and relationships
- [SOURCE-DERIVED] E = hν, with h = 6.626 × 10⁻³⁴ J·s (Day 3 p.17). E = energy of one photon (J); ν = frequency (s⁻¹).

### Three representations
- Macroscopic: hot metal glows red → orange → yellow-white; "red hot", "white hot"; "As the metal gets hotter, its COLOR changes" (Day 3 p.12).
- Symbolic: radiance-vs-wavelength curves; E = hν.
- Particulate: energy is emitted in discrete quanta (photons), "a staircase, not a ramp."

### Professor explanations, models, and diagrams
- [SOURCE-DERIVED] Graph 1 (Day 3 p.13): y = log emission intensity (no numbers); x = wavelength (nm), log scale 100–100,000, with UV, visible, and IR bands. Curves for 6000, 2000, 1000, 500, and 300 K: hotter curves sit higher and peak at shorter λ.
- [SOURCE-DERIVED] Graph 2 (Day 3 p.14): y = spectral radiance (0–14, no units); x = wavelength (μm, 0–3). Curves for 5000 K (peak ≈ 0.58 μm), 4000 K, and 3000 K, with the visible band shaded. A black "Classical theory (5000 K)" curve rises without limit at short λ (Day 3 p.15–16).
- [CLARIFICATION] Wien's law, λ_max = 2.898 × 10⁻³ m·K / T, gives 580 nm at 5000 K, matching the plotted peak. The slides do not use the name "ultraviolet catastrophe."

### Recognition cues
- [INFERRED] Temperature ↔ color or peak-wavelength questions → read the blackbody graph. "Quantized", "discrete packets", "photon" → Planck.

### Common mistakes flagged
- [INFERRED] Reading a curve's plotting color as the color the object emits.

### Connections
- Builds on: atomic spectra (Day 3 p.11). Used later in: the photoelectric effect (Day 3 p.18); Bohr "borrowed the brave leap from Planck" (Day 4 p.8).

## The Photoelectric Effect

**Sources:** Day 3 p.18–20
**Unit / lecture order:** Day 3
**Prerequisites:** Planck's E = hν
**Emphasis evidence:** §3.3 bold (Day 3 p.5); outcome 2 ("Describe quantum theory and use it to explain the photoelectric effect") bold (Day 3 p.6).

### Definitions and terminology
- [SOURCE-DERIVED] "For a few years, 'blackbody radiation' was the ONLY phenomenon that needed to be explained by quantization. So, people were (justly) skeptical. Enter, stage left: the photoelectric effect and Albert Einstein." (Day 3 p.18)
- [SOURCE-DERIVED] "In 1905, Einstein showed that the kinetic energy (KE) of the ejected electron equals the amount of energy in excess of the threshold energy, φ (also called the 'work function'). That threshold energy represents the **minimum frequency** which can cause an electron to be ejected." (Day 3 p.19)

### Equations and relationships
- [SOURCE-DERIVED] KE = hν − φ = hν − hν₀ (Day 3 p.19; confirmed on a 300-dpi zoom; the text layer garbles it to "KE = h- = h−h"). KE = kinetic energy of the ejected electron (J); ν = frequency of the incident light; φ = threshold energy, or work function (J); ν₀ = threshold frequency, with φ = hν₀.

### Three representations
- Macroscopic: current flows only above a threshold color, and brighter light below it does not help (Day 3 p.18).
- Symbolic: KE = hν − φ; KE-vs-ν straight lines.
- Particulate: one photon ejects one electron; the photon's energy above φ becomes the electron's kinetic energy.

### Professor explanations, models, and diagrams
- [SOURCE-DERIVED] Phototubes (Day 3 p.18): (a) violet light on the metal (negative electrode) ejects electrons and the meter shows current; (b) dim red light gives no current; (c) brighter red light still gives no current.
- [SOURCE-DERIVED] Graph (Day 3 p.19): maximum kinetic energy (y) vs. frequency (x), no numbers; five parallel straight lines whose x-intercepts increase from cesium to potassium, calcium, magnesium, and mercury. [INFERRED: the slope is h for every metal; the x-intercept is ν₀; below ν₀ no electrons are ejected regardless of intensity.]

### Recognition cues
- [INFERRED] "Threshold" or "work function", "ejected electrons", "minimum frequency", "kinetic energy of the electrons" → KE = hν − φ. Intensity-vs-frequency questions → only frequency (photon energy) controls ejection.

### Common mistakes flagged
- [INFERRED] Believing brighter light below the threshold will eventually eject electrons (Day 3 p.18 panel c shows it won't).

### Uncertainties and discrepancies
- [CLARIFICATION] The slide calls φ a threshold *energy* and then says it "represents the minimum frequency"; strictly φ = hν₀, so φ is the minimum energy and ν₀ the minimum frequency.
- [CLARIFICATION] Symbols: the slide uses lowercase φ; the textbook uses uppercase Φ and writes Φ = hν − KE_electron (TB PDF p.128, printed 94, Eq. 3.6) → TEXTBOOK_MAP Convention differences.
- [SOURCE-DERIVED] The Day 3 p.20 Top Hat question is not in the PDF.

## The Hydrogen Spectrum: Balmer and Rydberg Equations

**Sources:** Day 3 p.21; Day 4 p.6–8
**Unit / lecture order:** end of Day 3, repeated at the start of Day 4
**Prerequisites:** atomic spectra
**Emphasis evidence:** repeated across two lectures (Day 3 p.21; Day 4 p.6–7); §3.4 bold (Day 3 p.5; Day 4 p.4); outcome 3 bold (Day 3 p.6; Day 4 p.5).

### Equations and relationships
- [SOURCE-DERIVED] Balmer (1885): λ = 364.56 nm × n²/(n² − 4), where n is an integer ≥ 3 (Day 3 p.21; Day 4 p.6–7).
- [SOURCE-DERIVED] Rydberg (1888): 1/λ = R_H(1/n₁² − 1/n₂²), where n₁ and n₂ are integers and n₂ > n₁; "R_H is the 'Rydberg constant'"; "The Balmer equation is a special case of the Rydberg equation where n₁ = 2!" (Day 4 p.7). The slides give no value for R_H.
- [SOURCE-DERIVED] Ritz (1908): the Rydberg equation works for any one-electron atom if the Rydberg constant is changed (Day 4 p.8).

### Professor explanations, models, and diagrams
- [SOURCE-DERIVED] Balmer's formula was predictive: scientists looked for the n = 7 and 8 lines and found "lines that nobody knew existed in the ultraviolet"; "Balmer was on to something powerful, even if he had no explanation" (Day 4 p.7). "Clearly, there was something profound hiding in this purely empirical formula" (Day 4 p.8).

### Worked examples
- [VERIFICATION] Balmer formula (Python): n = 3, 4, 5, 6, 7, 8 → 656.2, 486.1, 434.0, 410.1, 397.0, 388.9 nm (n = 7 and 8 are in the near UV, as the slide says). Implied R_H = 4/364.56 nm = 1.0972 × 10⁷ m⁻¹; the textbook gives 1.0974 × 10⁷ m⁻¹ (TB PDF p.130, printed 96).

### Recognition cues
- [INFERRED] Wavelength of a hydrogen (or one-electron) line between two integer levels → Rydberg or Bohr. "Visible hydrogen lines" → n₁ = 2 (Balmer).

### Uncertainties and discrepancies
- [UNCERTAIN] Whether students must know R_H's value (none on the slides). The Bohr form with −2.178 × 10⁻¹⁸ J (Day 4 p.10) may be the working equation.
- [CLARIFICATION] The textbook writes Balmer's equation with m (an integer > 2) instead of n (TB PDF p.129). Naming only.

## The Bohr Model of the Hydrogen Atom

**Sources:** Day 4 p.1, p.3, p.8–10, p.15–16; Day 6 p.8
**Unit / lecture order:** Day 4 (lecture titles Day 3 p.1 "The Quantum Revolution; the Bohr Model" and Day 4 p.1 "The Bohr Model, Wavefunctions, and Quantum Numbers")
**Prerequisites:** the nuclear atom; Planck's quantization; Balmer and Rydberg; E = hν = hc/λ
**Emphasis evidence:** §3.4 bold (Day 3 p.5; Day 4 p.4); named in two lecture titles; the Bohr-atom figure appears in two lectures (Day 4 p.9; Day 6 p.8).

### Definitions and terminology
- [SOURCE-DERIVED] In 1913, Bohr was trying to understand why the negatively charged electrons of Rutherford's nuclear atom "didn't spiral into the positively charged nucleus". He "borrowed the brave leap from Planck: Electrons maintained their distance from the nucleus because their angular momenta were **quantized**. This led to their distance from the nucleus also being quantized!" (Day 4 p.8)
- [SOURCE-DERIVED] Where the model holds: "The Bohr model turns out to be TRUE for hydrogen and other one-electron atoms, even if that makes you uncomfortable. But once even a *second* electron is involved, the Bohr model falls apart. The electrons don't exist *independently* of each other. There are [sic] *correlated*. It turns out that the math to solve this is nearly impossible." (Day 4 p.3, a Representation Matters slide on Oktay Sinanoğlu)

### Equations and relationships
- [SOURCE-DERIVED] ΔE = −2.178 × 10⁻¹⁸ J (1/n_final² − 1/n_initial²) (Day 4 p.10, 300-dpi zoom). ΔE = change in the electron's energy (J per atom). [CLARIFICATION: emission (n_final < n_initial) makes ΔE < 0 and absorption makes ΔE > 0; the photon carries |ΔE| (TB PDF p.132, printed 98).]
- [SOURCE-DERIVED] Shown alongside ΔE: 1/λ = R_H(1/n₁² − 1/n₂²) and E = hν = hc/λ (Day 4 p.10).

### Three representations
- Macroscopic: hydrogen's discrete colored lines.
- Symbolic: the ΔE equation; the level diagram; series names.
- Particulate: one electron jumps between quantized orbits; the emitted photon's energy equals the gap.

### Professor explanations, models, and diagrams
- [SOURCE-DERIVED] Bohr atom: a nucleus with circular orbits n = 1, 2, 3 and one electron; labels Nucleus, Electron, Orbits (Day 4 p.9; the Day 6 p.8 reprise draws the electron on n = 2). [INFERRED: radii drawn roughly ∝ n².]
- [SOURCE-DERIVED] Hydrogen energy-level diagram (Day 4 p.10): levels n = 1–6 and ∞, closer together going up; an "Ionization" arrow from n = 1 to n = ∞; Lyman (ultraviolet) arrows down to n = 1 from n = 2–6; Balmer (visible) arrows down to n = 2 from n = 3 (red), 4 (green), 5 (blue), 6 (violet); Paschen (infrared) arrows down to n = 3 from n = 4, 5, 6.

### Worked examples
- [VERIFICATION] Using ΔE = −2.178 × 10⁻¹⁸ J(1/n_f² − 1/n_i²) and λ = hc/|ΔE| (Python): 2→1 = 121.6 nm (UV); 3→2 = 656.7 nm (red); 4→2 = 486.4 nm; 6→2 = 410.4 nm; 4→3 = 1876 nm (IR). Ionization from n = 1: ΔE = +2.178 × 10⁻¹⁸ J per atom × 6.022 × 10²³ mol⁻¹ = 1312 kJ/mol, exactly hydrogen's IE₁ on Day 7 p.9.

### Recognition cues
- [INFERRED] "Hydrogen" or "one-electron atom", "transition from n = a to n = b", "wavelength of the emitted/absorbed photon", "ionize from the ground state" → ΔE equation, then E = hc/λ. Landing on level 1 → UV (Lyman); 2 → visible (Balmer); 3 → IR (Paschen).

### Common mistakes flagged
- [INFERRED] Swapping n_final and n_initial (sign error); forgetting ΔE is per atom (× N_A for per mole); using Bohr for multi-electron atoms, where it "falls apart" (Day 4 p.3).

### Connections
- Builds on: Rutherford's nucleus, Planck's quantization, Balmer/Rydberg (Day 4 p.7–8). Used later in: de Broglie's standing-wave justification (Day 4 p.15–16); the principal quantum number n (Day 5 p.10–11); ionization energy (Day 7 p.9).

### Uncertainties and discrepancies
- [INFERRED] The Day 6 p.8 reprise has no text; it probably recalls Bohr's n just before electron configurations are built.

## The de Broglie Equation: Wave–Particle Duality of Matter

**Sources:** Day 4 p.11–17
**Unit / lecture order:** Day 4
**Prerequisites:** the particle nature of light (Planck, photoelectric effect); unit conversion (g → kg; J = kg·m²/s²)
**Emphasis evidence:** §3.5 bold (Day 3 p.5; Day 4 p.4); outcome 4 bold (Day 3 p.6; Day 4 p.5); two worked examples (Day 4 p.12, p.14).

### Definitions and terminology
- [SOURCE-DERIVED] In 1924, as part of his Ph.D. dissertation, de Broglie suggested that "matter possesses a wave-particle duality, just as had been shown for light. **All** matter, but especially subatomic particles, could be treated as a moving wave. For small subatomic particles, this effect is relatively significant!" (Day 4 p.11)
- [SOURCE-DERIVED] "The closer the de Broglie wavelength is to the physical size of the moving object, the more the object is behaving as a wave." (Day 4 p.11)

### Equations and relationships
- [SOURCE-DERIVED] λ = h/(m u): λ = de Broglie wavelength in meters; h = Planck's constant = 6.62607004 × 10⁻³⁴ J·s; m = mass in kilograms (1 J = 1 kg·m²/s²); u = velocity in meters per second (Day 4 p.11). The professor's symbol for velocity is u.

### Three representations
- Macroscopic: electron-beam diffraction rings look like X-ray diffraction rings (Day 4 p.17).
- Symbolic: λ = h/(mu).
- Particulate: an electron in an atom behaves as a standing wave around the nucleus (Day 4 p.15–16).

### Professor explanations, models, and diagrams
- [SOURCE-DERIVED] Standing waves justify Bohr's orbits: "Electrons can only exist in an orbit if there are an integer number of de Broglie wavelengths in the circumference of that orbit. Why might that be a reasonable assumption?" (Day 4 p.15). A violin string of length L carries standing waves of 1, 2, and 3 half-wavelengths (n = 1, 2, 3) but not 2½ (Day 4 p.15). Around an orbit, an n = 3 wave closes on itself and an n = 2¼ wave does not (Day 4 p.16). "The n **quantum number** from the Bohr model now had a physical meaning beyond an arbitrary quantization!" (Day 4 p.16)
- [SOURCE-DERIVED] "Later in 1924, Thomson and Davisson / Germer demonstrated the wave-nature of matter": X-ray diffraction rings beside electron-beam diffraction rings (Day 4 p.17).

### Worked examples
- (Day 4 p.12) Electron: m = 9.10938 × 10⁻²⁸ g, u = 4.05 × 10⁶ m/s. λ = 6.626 × 10⁻³⁴ J·s / [(9.10938 × 10⁻³¹ kg)(4.05 × 10⁶ m/s)] = 1.80 × 10⁻¹⁰ m. Steps shown: g → kg first; units written in every factor; h rounded to 6.626 × 10⁻³⁴ in the arithmetic; answer to 3 s.f. (limited by 4.05). [VERIFICATION: 1.796 × 10⁻¹⁰ m → 1.80 × 10⁻¹⁰ m, Python]
- (Day 4 p.14) Baseball: m = 142 g thrown at 44.0 m/s ("roughly 98 mph"). λ = 6.626 × 10⁻³⁴ J·s / [(0.142 kg)(44.0 m/s)] = 1.06 × 10⁻³⁴ m (3 s.f.). [VERIFICATION: 1.0605 × 10⁻³⁴ m; the textbook works the same baseball, TB PDF p.135, printed 101.]
- [INFERRED] The contrast: an electron's λ (≈ 10⁻¹⁰ m) is about the size of an atom, so its wave behavior matters; a baseball's (≈ 10⁻³⁴ m) is irrelevant.

### Recognition cues
- [INFERRED] Mass and speed given, wavelength asked (or "wave nature of a particle") → λ = h/(mu); convert mass to kg first.

### Common mistakes flagged
- [INFERRED] Leaving the mass in grams (the worked example shows the g → kg step explicitly, Day 4 p.12); confusing u (velocity) with ν (frequency).

### Connections
- Builds on: light's wave–particle duality ("just as had been shown for light," Day 4 p.11); the Bohr model (Day 4 p.15–16). Used later in: Schrödinger's wavefunctions describe "the wave-particle duality of the electrons" (Day 5 p.7).

### Uncertainties and discrepancies
- [CLARIFICATION] The string counts *half*-wavelengths, while the orbit condition counts whole wavelengths around the circumference (Day 4 p.15–16). Both are standing-wave conditions, but students may mix them up.
- [CLARIFICATION] The electron-diffraction experiments (Davisson–Germer; G. P. Thomson) are usually dated 1927, not "later in 1924" (outside knowledge; history detail) → COURSE.md Discrepancies.
- [SOURCE-DERIVED] Textbook §3.5 also covers the Heisenberg uncertainty principle (TB PDF p.137–138), which the lectures do not → TEXTBOOK_MAP Scope notes.
- [SOURCE-DERIVED] The Day 4 p.13 Top Hat question is not in the PDF.

## The Schrödinger Equation and Wavefunctions

**Sources:** Day 4 p.18; Day 5 p.7–9
**Unit / lecture order:** end of Day 4, repeated and continued on Day 5
**Prerequisites:** de Broglie's wave–particle duality
**Emphasis evidence:** [SOURCE-DERIVED] explicit scope statement: "The *mathematics* of this equation are beyond the scope of this class, but your TAs and I will be happy to talk to you about it outside of lecture! For this class, we're going to concern ourselves with the **solutions** to this equation" (Day 5 p.7). The slide is repeated across lectures (Day 4 p.18; Day 5 p.7).

### Definitions and terminology
- [SOURCE-DERIVED] In 1925, Schrödinger calculated hydrogen's electron energy levels with HΨ = EΨ, where H is the "Hamiltonian operator", E the "Total energy", and Ψ the "Wavefunction of an electron" (Day 4 p.18; Day 5 p.7).
- [SOURCE-DERIVED] The solutions, which Schrödinger called **wavefunctions**, "appeared to correctly describe the wave-particle duality of the electrons" (Day 5 p.7).
- [SOURCE-DERIVED] "The function **Ψ = sin(x)** is the simplest form of a wavefunction. But most solutions are significantly more complex." (Day 5 p.8–9)
- [SOURCE-DERIVED] "While the wavefunction, Ψ, does not have physical meaning, |Ψ|² is the **probability density** of the electron and tells us where it is likely to be found around an atom. (This was Max Born, 1926). Those three-dimensional regions of high probability came to be called **orbitals.**" (Day 5 p.8)

### Professor explanations, models, and diagrams
- [SOURCE-DERIVED] An unlabeled sine wave (Day 5 p.8–9), and an example hydrogen 3s wavefunction (Day 5 p.9, 400-dpi zoom): ψ₃ₛ = 1/(18√3 π) · (1/a₀)^{3/2} · [6 − 4r/a₀ + 4r²/(9a₀²)] · e^{−r/3a₀}.

### Connections
- Builds on: de Broglie (Day 5 p.7). Used later in: the quantum numbers that label the solutions (Day 5 p.10); orbital pictures that plot ψ² and 4πr²ψ² (Day 5 p.17–18).

### Uncertainties and discrepancies
- [VERIFICATION] As printed, with the radical over the 3 only, the 3s function integrates to 1/π; with the prefactor 1/(18√(3π)) it integrates to 1 (sympy). Probably a typesetting slip, in math the slides declare out of scope (Day 5 p.7). → COURSE.md Discrepancies; not examinable.

## Quantum Numbers (n, ℓ, m_ℓ, m_s)

**Sources:** Day 5 p.10–16
**Unit / lecture order:** Day 5 (title "Quantum Numbers, Atomic Orbitals, and Electron Configurations", Day 5 p.1)
**Prerequisites:** Schrödinger wavefunctions; Bohr's n
**Emphasis evidence:** §3.6 bold (Day 4 p.4; Day 5 p.5); outcome 5 bold (Day 4 p.5; Day 5 p.6); a Top Hat question (Day 5 p.16); the key words **size**, **energy**, **shape**, and **orientation** are bold (Day 5 p.10–11).

### Definitions and terminology
- [SOURCE-DERIVED] Orbitals "are each independent solutions to the Schrödinger equation, and are each described by three quantum numbers. Together, the quantum numbers specify the energy, shape, and orientation of orbitals in an atom." (Day 5 p.10)
- [SOURCE-DERIVED] Principal quantum number n: "is *like* Bohr's single quantum number, and is a positive integer describing the relative **size** and **energy** of an atomic orbital or group of orbitals in an atom." "Indeed, in an atom with only one electron, it IS Bohr's quantum number, with the proviso that the orbital is three dimensional rather than a circle. But it's more complicated when there's more than one electron. In general, higher values of n correspond to probability of electrons being further away from the nucleus." (Day 5 p.10–11)
- [SOURCE-DERIVED] Angular momentum quantum number ℓ: "an integer having any value from 0 to (n − 1) that defines the **shape** of an orbital" (Day 5 p.10, p.12). Letter identifiers: ℓ = 0, 1, 2, 3, 4 ↔ s, p, d, f, g (Day 5 p.12).
- [SOURCE-DERIVED] "All orbitals with the same value of n are in the same 'shell.' All orbitals with the same values of n AND ℓ are in the same 'subshell.'" For n = 1 the only ℓ is 0, so there is one orbital, 1s; n = 2 gives 2s and 2p; n = 3 gives 3s, 3p, and 3d (Day 5 p.12).
- [SOURCE-DERIVED] Magnetic quantum number m_ℓ: "defines the **orientation** of an orbital in space, and it ranges from −ℓ to ℓ in increments of 1… for now let's focus on *how many* allowed values this produces." (Day 5 p.13)
- [SOURCE-DERIVED] Spin quantum number m_s: the first three numbers "aren't **quite** enough to describe an electron." In 1922, Walther Gerlach passed a beam of silver atoms through a magnet and "half the atoms were deflected in one direction and half in the other", which led to the "'invention' of a fourth quantum number: m_s, the spin quantum number, which has two allowed values: ±½" (Day 5 p.14). Figure: source of Ag atoms → beam → magnet → detecting screen with two spots labeled m_s = −½ and m_s = +½.

### Equations and relationships
- [SOURCE-DERIVED] Textbook Table 3.1, "Quantum Numbers of the Orbitals in the First Four Shells", reproduced on Day 5 p.13: n = 1 → s, m_ℓ 0 (1 orbital; shell total 1); n = 2 → s (1) + p, m_ℓ −1, 0, +1 (3) = 4; n = 3 → s + p + d, m_ℓ −2…+2 (5) = 9; n = 4 → s + p + d + f, m_ℓ −3…+3 (7) = 16.
- [VERIFICATION] Orbitals per subshell = 2ℓ + 1 and per shell = n² (Python). The slide does not state these rules, though the table shows them; the textbook states them (TB PDF p.141, printed 107).

### Three representations
- Symbolic: (n, ℓ, m_ℓ, m_s) sets; subshell labels such as 2p and 3d.
- Particulate: n ~ size and energy; ℓ ~ shape; m_ℓ ~ orientation; m_s ~ one of two spin states (the two beams, Day 5 p.14).

### Worked examples
- [SUPPORTED EMPHASIS] Top Hat (Day 5 p.16): "Which ONE set of quantum numbers is valid?" as (n, ℓ, m_ℓ, m_s): a (1, 0, −1, +½); b (3, 2, −2, +½); c (2, 2, 0, 0); d (2, 0, 1, −½); e (−3, −2, −1, −½). No answer on the slide. Reference answer: b. [VERIFICATION: `tools/chemistry_verify.py qn`. In a and d, m_ℓ must be 0 when ℓ = 0; in c, ℓ must be ≤ n − 1 and m_s cannot be 0; in e, n must be positive and ℓ ≥ 0.]

### Procedures, shortcuts, assumptions, warnings
- [INFERRED from Day 5 p.10–15] Check a set in order: n is a positive integer → 0 ≤ ℓ ≤ n − 1 → −ℓ ≤ m_ℓ ≤ +ℓ → m_s = ±½.

### Recognition cues
- [INFERRED] "Which set is allowed/valid", "how many orbitals (or electrons) in n = 3 or in a 4d subshell", "which subshell has n = 4, ℓ = 2" → quantum-number rules.

### Common mistakes flagged
- [INFERRED] ℓ = n; m_ℓ outside −ℓ…+ℓ; m_s = 0 or ±1; negative n. Each wrong Top Hat option on Day 5 p.16 is one of these.

### Connections
- Builds on: Bohr's n (Day 5 p.10–11) and the Schrödinger solutions (Day 5 p.10). Used later in: Pauli (Day 5 p.15); orbital shapes (Day 5 p.17–20); electron configurations, "a convenient way to communicate the quantum numbers of all electrons" (Day 6 p.6).

### Uncertainties and discrepancies
- [CLARIFICATION] The slide names only Gerlach (1922); the textbook credits Stern and Gerlach and attributes the spin idea to Goudsmit and Uhlenbeck (1925) (TB PDF p.141, printed 107). History detail → COURSE.md Discrepancies.

## The Pauli Exclusion Principle

**Sources:** Day 5 p.15; Day 6 p.6
**Unit / lecture order:** Day 5
**Prerequisites:** quantum numbers, including m_s
**Emphasis evidence:** "**number**" and "**two**" printed bold (Day 5 p.15); listed first of the three configuration rules (Day 6 p.6).

### Definitions and terminology
- [SOURCE-DERIVED] In 1925 Pauli proposed that "no two electrons can have the exact same set of four quantum numbers" (Day 5 p.15).
- [SOURCE-DERIVED] "The most immediate consequence for this class is that this limits the **number** of electrons which can be placed into a given subshell. If a pair of electrons have the same values of n, ℓ, and m_ℓ, then they must have *opposite* spins. Once two electrons occupy the same orbital (with opposite spins), it is not possible to add a third electron to that orbital. All orbitals are filled when they contain **two** electrons." (Day 5 p.15)

### Equations and relationships
- [INFERRED] Capacities, from the Day 5 p.13 orbital counts × 2: s 2, p 6, d 10, f 14; shell n holds 2n² electrons.

### Connections
- Used later in: electron configurations (Day 6 p.6); paired ↑↓ boxes in orbital diagrams (Day 6 p.16–17).

## Sizes and Shapes of Atomic Orbitals

**Sources:** Day 5 p.17–20
**Unit / lecture order:** Day 5
**Prerequisites:** wavefunctions and |Ψ|²; quantum numbers
**Emphasis evidence:** §3.7 bold (Day 5 p.5).

### Definitions and terminology
- [SOURCE-DERIVED] "Ok, but what do these wavefunctions LOOK like. Let's start with the simplest solution: n = 1, ℓ = 0. That's the 1s orbital. And it's a sphere! Which means that there's no such thing as a 'spatial orientation,' so there's only one value of m_ℓ" (Day 5 p.17).
- [SOURCE-DERIVED] "All s orbitals are spheres. They have no angular dependence on orientation. Orbital size increases with increasing value of principal quantum number, n." (Day 5 p.18)
- [SOURCE-DERIVED] "ℓ = 1 produces p orbitals. Each p orbital consists of two lobes pointing in opposite directions. There are THREE of them, pointing along each of the Cartesian coordinate axes, and corresponding to the three allowed values of m_ℓ" (Day 5 p.19).
- [SOURCE-DERIVED] "ℓ = 2 produces d orbitals. d orbitals are… complicated. There are FIVE of them, corresponding to the five allowed values of m_ℓ" (Day 5 p.20).

### Three representations
- Symbolic: ψ² and 4πr²ψ² graphs; labels 2p_x, 3d_z².
- Particulate: probability clouds: spheres (s), two-lobed dumbbells (p), four-lobed cloverleaves (d); larger with larger n.

### Professor explanations, models, and diagrams
- [SOURCE-DERIVED] 1s (Day 5 p.17): (a) y = "Electron density (ψ²)", x = distance from nucleus (pm, 0–400), highest at the nucleus and falling outward; (b) y = "Electron distribution (4πr²ψ²)", starting at zero and peaking at **53 pm**; (c) dot-density cross-section; (d) a sphere on x, y, z axes.
- [SOURCE-DERIVED] 1s, 2s, 3s (Day 5 p.18): dot-density quarter-circles grow with n above their 4πr²ψ² plots. 1s has one peak (≈ 50 pm). 2s has a small inner peak, one zero (dashed line, ≈ 110 pm), and its main peak ≈ 280 pm. 3s has three peaks, two zeros (≈ 100 and ≈ 370 pm), and its main peak ≈ 680 pm. Dashed arrows link each zero to an empty ring in the dot picture. The word "node" is not used.
- [SOURCE-DERIVED] 2p_x, 2p_y, 2p_z boundary surfaces, two lobes along each axis (Day 5 p.19). 3d_xy, 3d_xz, 3d_yz have four lobes between the axes; 3d_x²−y² has lobes on the x and y axes; 3d_z² has two lobes on z plus a ring in the xy-plane (Day 5 p.20). No f-orbital shapes are shown.

### Worked examples
- [VERIFICATION] Hydrogen radial distributions (sympy/numpy, a₀ = 52.918 pm): 1s max 53 pm; 2s node 106 pm, main max 277 pm; 3s nodes 101 and 376 pm, main max 692 pm; 2p max 212 pm; 3p node 318 pm, main max 635 pm; 3d max 476 pm. These match the positions plotted on Day 5 p.17–18 and Day 6 p.12, p.18.

### Recognition cues
- [INFERRED] "Where is the electron most likely to be found?" → the peak of 4πr²ψ² (radial distribution), not of ψ². "How many lobes or orientations?" → ℓ and m_ℓ.

### Common mistakes flagged
- [INFERRED] Reading ψ² (largest at r = 0) as the most likely distance; Day 5 p.17 shows both plots, and 4πr²ψ² peaks at 53 pm.

### Connections
- Used later in: radial distributions explain penetration (Day 6 p.12, p.18); orbital overlap in valence bond theory: two H 1s spheres form a σ bond (Day 11 p.10), and carbon's 2s sphere and 2p lobes (Day 11 p.11) are mixed into hybrid orbitals (Day 11 p.12–16); side-by-side p overlap makes π bonds (Day 11 p.17–23).

### Uncertainties and discrepancies
- [CLARIFICATION] The three p orbitals match the three m_ℓ values *by count*; p_x and p_y are combinations of the m_ℓ = ±1 solutions, not one-to-one matches ("corresponding to," Day 5 p.19).

## Electron Configurations: The Aufbau Principle and Notation

**Sources:** Day 6 p.6–11, p.14–15, p.17
**Unit / lecture order:** Day 6 (planned in the Day 5 title, taught Day 6)
**Prerequisites:** quantum numbers; Pauli; penetration (why 2s fills before 2p); the periodic table (atomic number = electron count)
**Emphasis evidence:** outcome 6 bold (Day 5 p.6; Day 6 p.5); §3.8 bold (Day 5 p.5; Day 6 p.4); named in two lecture titles (Day 5 p.1; Day 6 p.1); "Have A Periodic Table Handy!!!" (Day 6 p.1).

### Definitions and terminology
- [SOURCE-DERIVED] "Electron configurations are a convenient way to communicate the quantum numbers of all electrons in an atom without having to write all 4 numbers for every electron." Notation template: n ℓ^# (principal quantum number, subshell letter, number of electrons as a superscript), "e.g. a 1s¹ electron configuration". The rules needed: the Pauli exclusion principle, the Aufbau principle, and Hund's rule (Day 6 p.6).
- [SOURCE-DERIVED] **Aufbau principle:** "*In the ground state* of an atom, the lowest energy orbitals are fully-filled *before* filling orbitals of higher energy." (Day 6 p.7)
- [SOURCE-DERIVED] "Those 2s¹ electrons are called the **valence electrons**, and they're what primarily determine the *chemical properties* of an element. The 1s² or [He] electrons are the **core electrons**, and aren't involved in most 'normal' chemical reactions." (Day 6 p.14)
- [SOURCE-DERIVED] **Degenerate**: the three 2p orbitals "all have the same energy," so "It doesn't matter *which* 2p orbital that first electron goes into" (Day 6 p.15).

### Three representations
- Symbolic: 1s²2s²2p⁴; [He]2s²2p⁴; orbital boxes.
- Particulate: electrons fill orbitals from the lowest energy up; the valence electrons are outermost and do the chemistry.

### Worked examples
- [SOURCE-DERIVED] Building up (Day 6 p.9–15). H: "How many electrons does hydrogen have? And what orbital is the lowest energy? n = 1, ℓ = 0. The electron configuration for H is 1s¹" (p.9). He: 1s² (p.10). Li: the 1s is full, so is the next orbital "2s or 2p?" (p.11); answer 2s, by penetration (p.12–13), giving 1s²2s¹, "which we can/will abbreviate [He]2s¹" (p.14). Be: 1s²2s² = [He]2s²; B: 1s²2s²2p¹ = [He]2s²2p¹ (p.15).
- [SOURCE-DERIVED] Table of H → Ne with orbital diagrams and full and condensed configurations (Day 6 p.17): C [He]2s²2p²; N [He]2s²2p³; O [He]2s²2p⁴; F [He]2s²2p⁵; Ne 1s²2s²2p⁶ = "[He]2s²2p⁶ = [Ne]". The condensed column is blank for H and He. [VERIFICATION: `tools/chemistry_verify.py config` matches all ten.]

### Procedures, shortcuts, assumptions, warnings
- [INFERRED from Day 6 p.9–17] Count the electrons from Z (periodic table) → fill subshells in order of increasing energy (Aufbau), at most 2 per orbital (Pauli), one per degenerate orbital before pairing (Hund) → optionally write the filled core as [noble gas].

### Recognition cues
- [INFERRED] "Write the (ground-state / condensed) electron configuration", "how many valence electrons" → Aufbau plus the element's position in the periodic table.

### Connections
- Builds on: quantum numbers and Pauli (Day 6 p.6); penetration (Day 6 p.12). Used later in: Hund's rule (Day 6 p.16); configurations of ions (Day 6 p.21); the ionization-energy orbital diagram (Day 7 p.9); ion formation (Day 7 p.18).

## Penetration, Shielding, and Effective Nuclear Charge (Z_eff)

**Sources:** Day 6 p.12–13, p.18–19; Day 7 p.5
**Unit / lecture order:** Day 6
**Prerequisites:** radial distributions (Day 5 p.17–18); Coulombic attraction
**Emphasis evidence:** "**penetration**" bold (Day 6 p.12–13, p.18); two radial-distribution slides plus the Li shielding picture; outcome 7 ("Use atomic orbitals and effective nuclear charge to predict periodic trends") bold on Day 7 p.5.

### Definitions and terminology
- [SOURCE-DERIVED] "The **energy** of the 2s orbital is **lower** than the energy of the 2p orbitals due to **penetration**: The s orbital has electron density closer to the nucleus than the p orbitals, which is a lower energy arrangement due to Coulombic attraction." (Day 6 p.12)
- [SOURCE-DERIVED] "Another way to think about this is that the p orbital is **shielded** from the nucleus by the electrons that lie between it and the protons." (Day 6 p.13)
- [SOURCE-DERIVED] For n = 3: "The energy of the 3s orbital is lower than the energy of the 3p orbitals due to penetration, and the 3p is lower energy than the 3d. Electrons fill 3s and 3p before 3d. But wait…" (Day 6 p.18)

### Three representations
- Symbolic: Z_eff ≈ 1+ for lithium's 2s electron; radial-distribution curves.
- Particulate: inner electrons screen the nucleus; an electron whose orbital dips inside the core (s more than p, p more than d) feels more of the nuclear charge and sits lower in energy.

### Professor explanations, models, and diagrams
- [SOURCE-DERIVED] 4πr²ψ² vs. distance (pm) for 2s and 2p (Day 6 p.12): 2p has one peak ≈ 200 pm; 2s has a small inner peak ≈ 45 pm (arrow "Penetration of 2s"), a zero ≈ 110 pm, and its main peak ≈ 270 pm.
- [SOURCE-DERIVED] Lithium (Day 6 p.13): "Nucleus (Z = 3+)" with 3 protons; a dense inner 1s² region; an outer "2s¹ (Z_eff ≈ 1+)". This is the only appearance of Z_eff in the slides; no formula for it is given.
- [SOURCE-DERIVED] 3s, 3p, 3d radial distributions (0–1000 pm), with "Penetration" arrows on the inner 3s and 3p peaks (Day 6 p.18).

### Recognition cues
- [INFERRED] "Why is 2s lower than 2p?", "why does 4s fill before 3d?", "why do atoms shrink across a period?" → penetration, shielding, Z_eff.

### Common mistakes flagged
- [INFERRED] Judging energy by where the main peak sits. The 2s main peak is *farther* out than 2p's, and 3d's single peak is the closest of the n = 3 set, yet the energies follow the inner, penetrating lobes (Day 6 p.12, p.18).

### Connections
- Used later in: filling order (Day 6 p.18–19); every Day 7 periodic trend (outcome 7, Day 7 p.5). [INFERRED] "Coulombic attraction" (Day 6 p.12) returns as E_el (Day 7 p.15).

### Uncertainties and discrepancies
- [CLARIFICATION] In one-electron hydrogen, 2s and 2p have the same energy; penetration splits subshells only in multi-electron atoms (consistent with "more complicated when there's more than one electron," Day 5 p.11).
- [UNCERTAIN] Whether a quantitative Z_eff (e.g., Z minus the core electrons) is expected; only "Z_eff ≈ 1+" appears (Day 6 p.13). The textbook uses the same lithium example (TB PDF p.146–147, printed 112–113).

## Hund's Rule and Orbital Diagrams

**Sources:** Day 6 p.15–17
**Unit / lecture order:** Day 6
**Prerequisites:** the Aufbau principle; degenerate orbitals
**Emphasis evidence:** outcome 6 bold ("Use the Aufbau principle and Hund's rule…", Day 6 p.5); "HAVE to" in capitals (Day 6 p.16).

### Definitions and terminology
- [SOURCE-DERIVED] "But carbon has a second p electron. Where does it go? Hund's rule states that the lowest energy arrangement occurs when we maximize unpaired spins when putting electrons into degenerate orbitals. Electrons are negatively charged, and repel each other. So that second p electron goes into either of the two empty p orbitals. We will refrain from 'pairing' electrons until we HAVE to." (Day 6 p.16)

### Professor explanations, models, and diagrams
- [SOURCE-DERIVED] Carbon: 1s [↑↓] 2s [↑↓] 2p [↑][↑][ ], with the two 2p electrons parallel (Day 6 p.16). The H → Ne table (Day 6 p.17) shows N 2p [↑][↑][↑], O [↑↓][↑][↑], F [↑↓][↑↓][↑], and Ne all paired. Drawing convention: unpaired electrons point up; a pair fills the leftmost box first.

### Recognition cues
- [INFERRED] "Orbital diagram", "number of unpaired electrons" → Hund's rule. The slides do not use "paramagnetic."

### Common mistakes flagged
- [INFERRED] Pairing two electrons in one p box before every p box has one; drawing the unpaired electrons with opposite spins.

### Connections
- Used later in: [INFERRED] the O → O⁺ orbital diagram for ionization energy (Day 7 p.9) and nitrogen's circled electron affinity (Day 7 p.11); the slides do not explain either in words. [SOURCE-DERIVED] Box diagrams return in valence bond theory: carbon's ground state "only has **two** unpaired electrons" (Day 11 p.11), and the hybridization diagrams fill sp³, sp², and sp boxes one electron at a time before pairing (Day 11 p.13–23). [INFERRED] Unpaired electrons also underlie O₂'s paramagnetism (Day 11 p.27).

## Filling Order beyond n = 2 (4s before 3d) and Exceptions to the Filling Rules

**Sources:** Day 6 p.18–20; Day 7 p.6
**Unit / lecture order:** Day 6, with exceptions on Day 7
**Prerequisites:** penetration; electron configurations
**Emphasis evidence:** [SOURCE-DERIVED] explicit scope statement on the exceptions: "We will *completely ignore this* in this class" (Day 7 p.6). "But it turns out that even **4s** is lower in energy than 3d!" (Day 6 p.19, with 4s in bold).

### Definitions and terminology
- [SOURCE-DERIVED] "But it turns out that even 4s is lower in energy than 3d!" (Day 6 p.19)
- [SOURCE-DERIVED] "It turns out that *some* atoms (almost always transition metals) exhibit electron configurations that are NOT the ones we would predict from the rules we learned on Monday. For example, convince yourself that Mo, molybdenum, 'should' have an electron configuration of [Kr]5s²4d⁴. It **doesn't**. It's [Kr]5s¹4d⁵. We will *completely ignore this* in this class, because the transition metals don't crop up that often. But the book talks about it." (Day 7 p.6)

### Professor explanations, models, and diagrams
- [SOURCE-DERIVED] Orbital-energy ladder (energy up the page, one box per orbital): 1s < 2s < 2p < 3s < 3p < 4s < 3d < 4p < 5s < 4d < 5p < 6s < 4f < 5d < 6p < 7s < 5f < 6d < 7p (Day 6 p.19). [VERIFICATION: identical to the (n + ℓ, then n) order computed in Python.]
- [SOURCE-DERIVED] Three filling-order aids on one image-only slide (Day 6 p.20). (1) A row chart: 1s | 2s 2p | 3s 3p | 4s 3d 4p | 5s 4d 5p | 6s 4f 5d 6p | 7s 5f 6d 7p. (2) A periodic table colored by block: s (groups 1–2 plus He), d (groups 3–12; 3d–6d), p (groups 13–18; 2p–7p), f (Ce–Lu = 4f; Th–Lr = 5f). (3) The diagonal-arrow mnemonic, "Start here and move along the arrows one by one." Which aid the professor prefers is not stated.

### Recognition cues
- [INFERRED] Any element past Ar → 4s before 3d. A transition-metal "exception" question → outside this course's scope (Day 7 p.6).

### Uncertainties and discrepancies
- [SOURCE-DERIVED] Ordering convention varies. Day 7 p.6 writes Mo in filling order ([Kr]5s²4d⁴ → [Kr]5s¹4d⁵), while Day 6 p.21 writes Ni in n order ([Ar]3d⁸4s²); the textbook uses n order (e.g., [Ar]3d⁵4s¹ for Cr, TB PDF p.151, printed 117). Both orders appear in lecture → COURSE.md Professor conventions. [VERIFICATION: `tools/chemistry_verify.py config Mo` → [Kr]5s¹4d⁵, flagged as a ground-state exception.]

## Electron Configurations of Ions

**Sources:** Day 6 p.21–23
**Unit / lecture order:** Day 6
**Prerequisites:** electron configurations; 4s-before-3d filling
**Emphasis evidence:** §3.9 bold (Day 6 p.4); outcome 6 bold (Day 6 p.5); "regardless of the order in which they were added" and the "4s²" printed bold (Day 6 p.21); a Top Hat question (Day 6 p.23).

### Definitions and terminology
- [SOURCE-DERIVED] "The electron configurations of monatomic ions are formed by adding electrons to or removing them from the electron configuration of the parent ion." (Day 6 p.21)
- [SOURCE-DERIVED] "Negative ions (e.g., F⁻) are formed by following Aufbau, Pauli, and Hund. F + e⁻ → F⁻   [He]2s²2p⁵ → [He]2s²2p⁶ = [Ne]" (Day 6 p.21)
- [SOURCE-DERIVED] "But positively charged ions (e.g., Na⁺) are formed by removing electrons from the highest principal quantum number (n) **regardless of the order in which they were added.** Na → Na⁺ + e⁻   [Ne]3s¹ → [Ne]   BUT: Ni → Ni²⁺ + 2e⁻   [Ar]3d⁸**4s²** → [Ar]3d⁸" (Day 6 p.21, 300-dpi zoom)

### Three representations
- Symbolic: the equations above, with e⁻ as a product when a cation forms and as a reactant when an anion forms; single-headed arrows; charges written magnitude-then-sign (Ni²⁺) (Day 6 p.21).
- Particulate: a cation loses its outermost (highest-n) electrons; an anion gains electrons into the next open orbital.

### Worked examples
- [SUPPORTED EMPHASIS] Top Hat (Day 6 p.23): "How many 3d electrons does V³⁺ have?" No answer on the slide. Reference: V [Ar]3d³4s² → V³⁺ [Ar]3d², so 2. [VERIFICATION: `tools/chemistry_verify.py config V^3+`]
- [VERIFICATION] F⁻ = [Ne], Na⁺ = [Ne], Ni²⁺ = [Ar]3d⁸ (`tools/chemistry_verify.py config`).

### Recognition cues
- [INFERRED] "Configuration of Fe³⁺", "how many d electrons in a transition-metal cation" → remove the highest-n (4s) electrons first, then 3d.

### Common mistakes flagged
- [SUPPORTED EMPHASIS] Removing the last-filled 3d electrons first; the bold "regardless of the order in which they were added" and the "BUT: Ni…" example target exactly this (Day 6 p.21).

### Uncertainties and discrepancies
- [INFERRED] "parent ion" (Day 6 p.21) means the parent (neutral) atom.

## Periodic Trends: Atomic Radius

**Sources:** Day 6 p.24–26; Day 7 p.7
**Unit / lecture order:** end of Day 6, figure repeated at the start of Day 7
**Prerequisites:** Z_eff; n (orbital size)
**Emphasis evidence:** figure shown in two lectures (Day 6 p.24; Day 7 p.7); a Top Hat question prepared (Day 6 p.26, "We didn't have time for this"); §3.10 bold (Day 6 p.4; Day 7 p.4); outcome 7 bold (Day 6 p.5; Day 7 p.5).

### Professor explanations, models, and diagrams
- [SOURCE-DERIVED] Main-group atomic radii, one sphere per element sized to scale (Day 6 p.24 = Day 7 p.7). No unit is printed; the textbook's Fig. 3.35 caption says picometers (TB PDF p.157, printed 123). Values: n=1 H 37, He 32 · n=2 Li 152, Be 112, B 88, C 77, N 75, O 73, F 71, Ne 69 · n=3 Na 186, Mg 160, Al 143, Si 117, P 110, S 103, Cl 99, Ar 97 · n=4 K 227, Ca 197, Ga 135, Ge 122, As 121, Se 119, Br 114, Kr 110 · n=5 Rb 247, Sr 215, In 167, Sn 140, Sb 141, Te 143, I 133, Xe 130 · n=6 Cs 265, Ba 222, Tl 170, Pb 154, Bi 150, Po 167, At 140, Rn 145.
- [SOURCE-DERIVED] Neither slide states the trend or its cause in words.

### Worked examples
- [SUPPORTED EMPHASIS] Top Hat, prepared but not done: "Rank these atoms from largest to smallest. F S P As Cl" (Day 6 p.26). Reference, from the figure: As (121) > P (110) > S (103) > Cl (99) > F (71). [VERIFICATION: sorted in Python from the printed values]

### Procedures, shortcuts, assumptions, warnings
- [INFERRED] The numbers show radius growing down a group (higher n) and shrinking across a period (rising Z_eff); outcome 7 ties the trends to Z_eff (Day 7 p.5), and the textbook explains this figure the same way (TB PDF p.156–157, printed 122–123).
- [CLARIFICATION] The printed values have irregularities: He 32 < H 37; Sn 140 < Sb 141 < Te 143; Bi 150 < Po 167; At 140 < Rn 145.

### Recognition cues
- [INFERRED] "Rank by atomic size", "which is larger?" → up down a group, down across a period.

### Common mistakes flagged
- [INFERRED] Assuming more electrons always means a bigger atom; across period 2 the radius falls from Li 152 to Ne 69 as electrons are added.

## Periodic Trends: Ionic Radius

**Sources:** Day 7 p.8
**Unit / lecture order:** Day 7
**Prerequisites:** atomic radius; configurations of ions
**Emphasis evidence:** §3.10 "The Sizes of Atoms and Ions" bold (Day 7 p.4).

### Professor explanations, models, and diagrams
- [SOURCE-DERIVED] Figure only, no text (Day 7 p.8); the same figure as textbook Fig. 3.36, whose caption gives picometers (TB PDF p.158, printed 124). Atom / ion pairs: n=2 Li 152 / Li⁺ 76; Be 112 / Be²⁺ 27; O 73 / O²⁻ 140; F 71 / F⁻ 133 · n=3 Na 186 / Na⁺ 102; Mg 160 / Mg²⁺ 72; Al 143 / Al³⁺ 54; S 103 / S²⁻ 184; Cl 99 / Cl⁻ 181 · n=4 K 227 / K⁺ 138; Ca 197 / Ca²⁺ 100; Se 119 / Se²⁻ 198; Br 114 / Br⁻ 195.

### Procedures, shortcuts, assumptions, warnings
- [INFERRED] The pattern in the numbers: every cation is smaller than its atom and every anion is larger. [CLARIFICATION: a cation loses its valence shell, and the remaining electrons each feel more nuclear charge; an anion adds electron–electron repulsion (TB PDF p.157, printed 123).]
- [INFERRED] The 10-electron (isoelectronic) ions shrink as Z rises: O²⁻ 140 > F⁻ 133 > Na⁺ 102 > Mg²⁺ 72 > Al³⁺ 54. The pattern is in the printed values but not stated.

### Recognition cues
- [INFERRED] "Compare an atom and its ion", "rank ions with the same number of electrons" → cation < atom < anion; within an isoelectronic series, higher Z is smaller.

### Uncertainties and discrepancies
- [UNCERTAIN] No text accompanies the figure, so which comparisons are expected (atom vs. ion, isoelectronic series) is not stated.

## Periodic Trends: Ionization Energy

**Sources:** Day 7 p.9–10
**Unit / lecture order:** Day 7
**Prerequisites:** electron configurations and orbital diagrams; Z_eff; valence vs. core electrons
**Emphasis evidence:** §3.11 bold (Day 6 p.4; Day 7 p.4); outcome 7 bold (Day 7 p.5).

### Definitions and terminology
- [SOURCE-DERIVED] M (g) + hν → M⁺ (g) + e⁻   IE₁ = +XXX kJ/mol (Day 7 p.9, 300-dpi zoom; the text layer drops the ν). The atoms are gaseous; a photon removes one electron; IE₁ is positive; units are kJ/mol.

### Equations and relationships
- [SOURCE-DERIVED] Textbook Table 3.2, "Successive Ionization Energies of the First 10 Elements" (kJ/mol), shown as an image (Day 7 p.10): H 1312 · He 2372, 5249 · Li 520, 7296, 12,040 · Be 900, 1758, 15,050, 21,070 · B 801, 2426, 3660, 24,682, 32,508 · C 1086, 2348, 4617, 6201, 37,926, 46,956 · N 1402, 2860, 4581, 7465, 9391, 52,976, 64,414 · O 1314, 3383, 5298, 7465, 10,956, 13,304, 71,036, 84,280 · F 1681, 3371, 6020, 8428, 11,017, 15,170, 17,879, 92,106, 106,554 · Ne 2081, 3949, 6140, 9391, 12,160, 15,231, 19,986, 23,057, 115,584, 131,236. A red staircase line runs after IE₁ for Li, IE₂ for Be, IE₃ for B, and so on to IE₈ for Ne.

### Three representations
- Macroscopic: the energy (kJ/mol) needed to ionize a mole of gaseous atoms.
- Symbolic: M(g) + hν → M⁺(g) + e⁻; IE₁, IE₂, …
- Particulate: one electron pulled away from the nucleus; harder when Z_eff is high or the electron is close, and far harder once core electrons are reached.

### Professor explanations, models, and diagrams
- [SOURCE-DERIVED] O: 1s [↑↓] 2s [↑↓] 2p [↑↓][↑][↑] → O⁺: 1s [↑↓] 2s [↑↓] 2p [↑][↑][↑] + e⁻. The electron removed is the *paired* 2p electron (Day 7 p.9).
- [SOURCE-DERIVED] 3-D bar chart, "First ionization energy, IE₁ (kJ/mol)", 0–2500, with arrows "Increasing IE₁" across groups 1–18 and "Decreasing IE₁" down n = 1–6 (Day 7 p.9). Values: H 1312, He 2372 · Li 520, Be 900, B 801, C 1086, N 1402, O 1314, F 1681, Ne 2081 · Na 496, Mg 738, Al 578, Si 787, P 1012, S 1000, Cl 1251, Ar 1521 · K 419, Ca 590, Ga 579, Ge 762, As 947, Se 941, Br 1140, Kr 1351 · Rb 403, Sr 550, In 558, Sn 709, Sb 834, Te 869, I 1008, Xe 1170 · Cs 376, Ba 503, Tl 589, Pb 716, Bi 703, Po 812, At 925, Rn 1037.
- [INFERRED] The slides give no explanation in words. The chart's arrows show IE₁ rising across a period and falling down a group; the O → O⁺ diagram points to the N > O anomaly (a paired electron is easier to remove); the red line separates valence electrons from core (1s) electrons. [CLARIFICATION: the textbook gives all of these explanations: Z_eff for the trends, s-vs-p penetration for Be > B and Mg > Al, paired-electron repulsion for N > O, and the red line "when all the valence electrons … have been removed" (TB PDF p.159–161, printed 125–127).]

### Worked examples
- [VERIFICATION] In every row of Table 3.2, the largest jump between successive IEs sits exactly at the red line (Li ×14.0 … Ne ×5.0), i.e., right after the last valence electron is removed (Python).
- [VERIFICATION] IE₁ anomalies in the printed values: Be 900 > B 801; Mg 738 > Al 578; N 1402 > O 1314; P 1012 > S 1000; As 947 > Se 941.
- [VERIFICATION] H IE₁ = 1312 kJ/mol equals Bohr's ionization energy, 2.178 × 10⁻¹⁸ J × 6.022 × 10²³ mol⁻¹ (Day 4 p.10 ↔ Day 7 p.9).

### Recognition cues
- [INFERRED] "Which has the highest/lowest IE₁?", "explain N vs. O", "which element matches this set of successive IEs?" (find the big jump) → trends, anomalies, and the valence/core jump.

### Common mistakes flagged
- [INFERRED] Expecting IE₁ to rise smoothly across a period (missing Be/B and N/O); misreading the big-jump position, which comes right after the number of valence electrons.

### Uncertainties and discrepancies
- [VERIFICATION] Table 3.2 prints N IE₄ = O IE₄ = 7465 and N IE₅ = Ne IE₄ = 9391. Wolfram|Alpha reference values: N IE₄ 7475, O IE₄ 7469, N IE₅ 9445, Ne IE₄ 9371 kJ/mol. The slide copies the textbook exactly (TB PDF p.161), so the source table itself seems to contain small errors (≤ 0.6%). Trends are unaffected. → COURSE.md Discrepancies.
- [SOURCE-DERIVED] The professor writes ionization with a photon (hν); the textbook writes Mg → Mg⁺ + e⁻ with no photon (TB PDF p.159) → TEXTBOOK_MAP Convention differences.
- [SOURCE-DERIVED] The slide's section title "3.11 Ionization Energies" drops the textbook's "…and Photoelectron Spectroscopy"; photoelectron spectroscopy does not appear in the lectures → TEXTBOOK_MAP Scope notes.

## Periodic Trends: Electron Affinity

**Sources:** Day 7 p.11
**Unit / lecture order:** Day 7
**Prerequisites:** electron configurations; Hund's rule (half-filled subshells); Z_eff
**Emphasis evidence:** [SUPPORTED EMPHASIS] instructor annotation: the "±" is printed in red and nitrogen's value (+7) is circled in red (Day 7 p.11). §3.12 bold (Day 6 p.4; Day 7 p.4).

### Definitions and terminology
- [SOURCE-DERIVED] M (g) + e⁻ → M⁻ (g)   EA₁ = ± XXX kJ/mol (Day 7 p.11, 400-dpi zoom). EA can have either sign.

### Equations and relationships
- [SOURCE-DERIVED] Electron-affinity table (kJ/mol; ᵃ = "Calculated values"): H −72.6 · Li −59.6, Be >0 · Na −52.9, Mg >0 · K −48.4, Ca −2.4 · Rb −46.9, Sr −5.0 · Cs −45.5, Ba −14 · B −26.7, C −122, N +7 (circled), O −141, F −328, Ne (+29)ᵃ · Al −42.5, Si −134, P −72.0, S −200, Cl −349, Ar (+35)ᵃ · Ga −28.9, Ge −119, As −78.2, Se −195, Br −325, Kr (+39)ᵃ · In −28.9, Sn −107, Sb −103, Te −190, I −295, Xe (+41)ᵃ · Tl −19.2, Pb −35.2, Bi −91.3, Po −183.3, At −270ᵃ, Rn (+41)ᵃ · He (0.0)ᵃ (Day 7 p.11).

### Procedures, shortcuts, assumptions, warnings
- [INFERRED from the values; CLARIFICATION from TB PDF p.164, printed 130] Sign convention: EA₁ is the energy *change* on adding an electron. Negative means energy is released (the anion is lower in energy); positive means energy must be supplied (N, Be, Mg, the noble gases). The most negative value is Cl (−349), not F (−328).
- [INFERRED] Nothing on the slide explains the circled N. [CLARIFICATION: adding an electron to nitrogen's half-filled 2p³ forces pairing; Be and Mg must add to a higher-energy p subshell; noble gases would need a new shell (TB PDF p.164).]

### Recognition cues
- [INFERRED] "Which element releases the most energy on gaining an electron?", "why is N's EA positive?", reading the sign of an EA value.

### Common mistakes flagged
- [INFERRED] Treating a "larger" EA as a bigger positive number; in this convention the most favorable EA is the most negative. Assuming F has the most negative EA.

### Connections
- [INFERRED] The counterpart of ionization energy (adding vs. removing an electron); both bear on which ions form (Day 7 p.18–19).

---

# Unit D — Chemical Bonding (Ch. 4; Day 7 p.12 – Day 9 p.30)

## Primary Types of Chemical Bonds (Ionic, Covalent, Metallic)

**Sources:** Day 7 p.12–14; Day 8 p.11, p.14–15
**Unit / lecture order:** Day 7, start of Ch. 4; Day 8 adds the covalent energy curve, metallic bonding, and Table 4.1
**Prerequisites:** metals vs. nonmetals on the periodic table (Day 2 p.24); valence electrons (Day 6 p.14)
**Emphasis evidence:** only "4.1 **Chemical Bonds**" is bold (not "and Greenhouse Gases"), and only "**Bonding**" in "4.2 Electronegativity and Bonding" (Day 7 p.12); Ch. 4 outcome 1 bold (Day 7 p.13).

### Definitions and terminology
- [SOURCE-DERIVED] "1. Ionic bonds: Exist between oppositely charged ions, and are defined by electrostatic attraction. NaCl" (Day 7 p.14)
- [SOURCE-DERIVED] "2. Covalent bonds: Exist between non-metals, and are defined by shared electrons which are highly localized. H₂" (Day 7 p.14)
- [SOURCE-DERIVED] "3. Metallic bonds: Exist between metal atoms, and are defined by shared electrons which are highly mobile. Cu" (Day 7 p.14)
- [SOURCE-DERIVED] "Metallic Bonds: Atoms in metallic solids are held together by a “sea” of mobile electrons that flows freely among all the atoms in a piece of metal. In a block of copper metal, there is no experimental evidence for any two atoms being “bonded”. Each copper atom shares its valence electrons with ALL its neighbors. This begins to account for the conductivity of metals, but that's all we'll say here in Chapter 4." (Day 8 p.14, beside a cube of Cu atoms)
- [SOURCE-DERIVED] Picked up again on Day 12: metals are "Heat and electricity conductors" (p.17), explained with bands built from MO diagrams (p.18–24); see Band Theory (Unit F).
- [SOURCE-DERIVED] Textbook Table 4.1, "Types of Chemical Bonds", shown on the slide (Day 8 p.15). Elements involved: ionic "Metals and nonmetals"; covalent "Nonmetals and metalloids"; metallic "Metals". Electron distribution: "Transferred", "Shared", "Delocalized". Particulate views: a K⁺/Cl⁻ lattice, Br₂ molecules, a Cu lattice. Macroscopic views: white salt crystals, orange-brown bromine in a bottle, a spool of copper wire.

### Three representations
- Macroscopic: the three examples: salt (NaCl), hydrogen gas (H₂), copper metal (Cu) (Day 7 p.14); salt crystals, bromine, and copper wire (Day 8 p.15).
- Symbolic: NaCl, H₂, Cu; KCl, Br₂, Cu (Day 8 p.15).
- Particulate: ions held together by attraction; an electron pair localized between two nonmetal atoms; electrons moving freely among metal atoms, a "sea" (Day 8 p.14).

### Professor explanations, models, and diagrams
- [SOURCE-DERIVED] "Potential energy during **covalent** H-H bond formation" (Day 8 p.11; textbook Fig. 4.2). Potential energy (kJ/mol, 0 to −500) vs. "Distance between nuclei (pm)", 0–300. (a) Far apart: two separate H electron clouds, energy 0. (b) Closer: a blue arrow, "Increasing attraction", follows the curve down. (c) The minimum, −436 kJ/mol at 74 pm (dashed line; 74 printed bold on the axis), where the two clouds merge. (d) Closer still: a red arrow, "Increasing repulsion", up the steep left wall.
- [INFERRED] The same shape as the ion-pair curve for E_el (Day 7 p.15): attraction, a minimum at the bond distance, then repulsion. The slide gives no name to 74 pm or 436 kJ/mol; the textbook calls them the bond length and the bond energy (TB PDF p.184) [CLARIFICATION]. §4.5, "Lengths and Strengths of Covalent Bonds", is bold on Day 8 p.4.

### Recognition cues
- [INFERRED] Metal + nonmetal → ionic; nonmetal + nonmetal → covalent; a metal alone → metallic (from the slide's "between…" wording and examples).

### Connections
- Used later in: Coulombic potential energy explains the ionic bond (Day 7 p.15); electronegativity places the bond types on one scale, nonpolar covalent → polar covalent → ionic (Day 9 p.16–18); valence bond theory reuses the H–H curve, "We talked about this already in the context of the H-H potential energy surface" (Day 11 p.9).

### Uncertainties and discrepancies
- [SOURCE-DERIVED] Two phrasings now appear in the slides: "Covalent bonds: Exist between non-metals… highly localized" and metallic "highly mobile" (Day 7 p.14), and Table 4.1's "Nonmetals and metalloids" and "Delocalized" (Day 8 p.15; textbook TB PDF p.184). They don't conflict: the table also counts metalloids → COURSE.md glossary.
- [SOURCE-DERIVED] Resolved on Day 9: electronegativity is now lectured (Day 9 p.15–18), the word "**Electronegativity**" is bold in the §4.2 title, and Ch. 4 outcome 3 is bold (Day 9 p.4–5). See **Electronegativity and Bond Polarity**.

## Electrostatic (Coulombic) Potential Energy

**Sources:** Day 7 p.15 (and "Coulombic attraction," Day 6 p.12)
**Unit / lecture order:** Day 7
**Prerequisites:** ionic bonds; ion charges; ionic radii (for d)
**Emphasis evidence:** Ch. 4 outcome 2 bold ("Calculate and compare the relative strengths of ion-ion attractions," Day 7 p.13).

### Equations and relationships
- [SOURCE-DERIVED] "Electrostatic potential energy, also called Coulombic potential energy: E_el = 2.31 × 10⁻¹⁹ J·nm (Q₁Q₂/d)" (Day 7 p.15, 400-dpi zoom; the slide types "2.31x10⁻¹⁹", and the text layer is garbled). The variables are not defined on the slide. [CLARIFICATION: Q₁ and Q₂ are the ion charges in units of the electron charge (e.g., +1, −2); d is the distance between the ion centers in nm; E_el is in J per ion pair and negative for opposite charges (TB PDF p.181, printed 147, Eq. 4.1).]
- [VERIFICATION] k·e² = (8.988 × 10⁹ N·m²/C²)(1.602 × 10⁻¹⁹ C)² = 2.307 × 10⁻¹⁹ J·nm (Python).

### Three representations
- Symbolic: E_el ∝ Q₁Q₂/d; the potential-energy curve.
- Particulate: a cation and an anion attract until their electron clouds start to repel; the bottom of the energy well is the ionic bond.

### Professor explanations, models, and diagrams
- [SOURCE-DERIVED] Energy vs. "Distance between cation and anion" (Day 7 p.15): +E_el up (red arrow), −E_el down (blue arrow). (a) Far apart: "No interaction," E = 0. (b) Closer: the energy falls (attraction). (c) A minimum at the dashed line. (d) Very close: the energy rises steeply (repulsion). Ion pairs are drawn along the top at each distance. The equation describes the attraction only, not the repulsive wall at (d).

### Recognition cues
- [INFERRED] "Which pair has the stronger attraction?", "calculate E_el for a pair of ions" → multiply the charges (a 2+/2− pair is 4× a 1+/1− pair at the same d); a smaller d gives a stronger attraction.

### Common mistakes flagged
- [INFERRED] Leaving d in pm instead of nm; dropping the signs of the charges; forgetting E_el is per ion pair (× N_A for per mole).

### Connections
- Builds on: "Coulombic attraction" as the reason for penetration (Day 6 p.12); [INFERRED] ionic radii supply d (Day 7 p.8), though the slides do not connect them. Used later in: lattice energy, compared with "our two-body equation for Coulombic attractions" (Day 7 p.17).

## Ionic Lattices and Lattice Energy

**Sources:** Day 7 p.16–17 (Table 4.2 stays on screen through p.21)
**Unit / lecture order:** Day 7
**Prerequisites:** Coulombic potential energy
**Emphasis evidence:** **crystalline lattices** and **even more stable** printed bold (Day 7 p.16–17); Table 4.2 kept on screen for five slides (Day 7 p.17–21).

### Definitions and terminology
- [SOURCE-DERIVED] "Ionic compounds form **crystalline lattices**. These are dense, highly ordered structures where the oppositely charged particles are in close proximity. They are almost always solids." (Day 7 p.16)
- [SOURCE-DERIVED] "The ionic lattices are **even more stable** than we might expect from our two-body equation for Coulombic attractions." (Day 7 p.17)

### Equations and relationships
- [SOURCE-DERIVED] "Table 4.2 Lattice Energies (U) of Some Common Ionic Compounds", U (kJ/mol): LiF −1049; LiCl −864; NaF −930; NaCl −786; NaBr −754; KCl −720; KBr −691; MgO −3791; MgCl₂ −2540; CaS −3093 (Day 7 p.17). U is negative: energy is released when the lattice forms.

### Three representations
- Macroscopic: a pile of white salt crystals (Day 7 p.16).
- Symbolic: U values in kJ/mol.
- Particulate: a 3-D array of alternating large (green) and smaller (purple) spheres (Day 7 p.16–17).

### Worked examples
- [VERIFICATION] One ion pair's E_el, with d = r₊ + r₋ from the Day 7 p.8 radii, × N_A: NaCl −492 vs. U −786; KCl −436 vs. U −720 (the textbook gets −436 kJ/mol for KCl the same way, TB PDF p.183); MgO −2625 vs. U −3791 kJ/mol. The real lattice is 1.4–1.65× more stable than one ion pair, consistent with "even more stable" (Python).

### Recognition cues
- [INFERRED] "Rank these lattice energies", "why is MgO's lattice energy about four times NaF's?" → charge product first (2+/2− → ×4), then ion size.

### Uncertainties and discrepancies
- [SOURCE-DERIVED] Resolved on Day 8: the same drawing appears on Day 8 p.15 inside Table 4.1, labeled Cl⁻ (green) and K⁺ (purple). [INFERRED] The unlabeled Day 7 p.16–17 image is therefore solid KCl, used as a generic ionic lattice (the slide's own example compound is NaCl, Day 7 p.14).
- [SOURCE-DERIVED] The slide's Table 4.2 includes CaS −3093; the supplied 3rd-edition textbook's Table 4.2 ends at MgCl₂ −2540 (TB PDF p.184, printed 150). This suggests an edition mismatch → COURSE.md Discrepancies.
- [CLARIFICATION] The slide doesn't say why the lattice is extra-stable: each ion touches several oppositely charged neighbors, not just one (TB PDF p.183).

## Formulas of Ionic Compounds

**Sources:** Day 7 p.18–20
**Unit / lecture order:** Day 7
**Prerequisites:** configurations of ions and noble-gas configurations; periodic-table groups; charge balance
**Emphasis evidence:** Ch. 4 outcome 4 bold (Day 7 p.13); §4.3 bold (Day 7 p.12); the coefficient **2** and the subscript **₂** printed in red (Day 7 p.20); "TOTAL" in capitals.

### Definitions and terminology
- [SOURCE-DERIVED] "How do we determine the *formula* for an ionic compound? Cations are positively charged ions which are usually formed when an atom loses its valence electrons to acquire a noble gas electron configuration. Anions form when an atom gains enough electrons to *fill* its valence shell and acquire a noble gas electron configuration." (Day 7 p.18)
- [SOURCE-DERIVED] Ion charges: Li → Li⁺; Na → Na⁺; "But" Mg → Mg²⁺; Al → Al³⁺; Cl → Cl⁻; F → F⁻; O → O²⁻ (Day 7 p.19; this shorthand omits the electrons).
- [SOURCE-DERIVED] "The TOTAL charge has to be zero, so the positive charges and the negative charges have to cancel. Li⁺ + Cl⁻ → LiCl · Mg²⁺ + O²⁻ → MgO · Mg²⁺ + 2 Cl⁻ → MgCl₂" (Day 7 p.20; the 2 and the subscript ₂ in red).

### Three representations
- Symbolic: ion charges → a formula with subscripts (MgCl₂).
- Particulate: [INFERRED] two Cl⁻ ions for each Mg²⁺ in the lattice; the formula gives the ratio of ions, not a molecule.

### Worked examples
- [VERIFICATION] Every ion on Day 7 p.19 has a noble-gas configuration: Li⁺ [He]; Na⁺, Mg²⁺, Al³⁺, F⁻, O²⁻ [Ne]; Cl⁻ [Ar] (`tools/chemistry_verify.py config`). All three formula equations on Day 7 p.20 balance in atoms and charge (`tools/chemistry_verify.py check`).

### Procedures, shortcuts, assumptions, warnings
- [INFERRED from Day 7 p.18–20] Get each ion's charge from its group (lose the valence electrons, or fill the valence shell) → choose the smallest whole-number ratio that makes the total charge zero → write that ratio as subscripts.

### Recognition cues
- [INFERRED] "Formula of the compound formed by Al and O", "what ion does S form?" → group-based charges plus charge balance.

### Common mistakes flagged
- [SUPPORTED EMPHASIS] The red coefficient/subscript pair (Day 7 p.20) marks the step where the number of ions in the equation becomes the subscript in the formula.
- [INFERRED] Writing MgCl (unbalanced charge) or Mg₂O₂ (not the lowest ratio).

### Connections
- Builds on: configurations of ions (Day 6 p.21); valence electrons (Day 6 p.14). Used later in: naming (Day 7 p.21).

## Naming Binary Ionic Compounds

**Sources:** Day 7 p.21; Day 8 p.6 (repeated)
**Unit / lecture order:** Day 7, last slide of the deck; repeated to open Day 8's content
**Prerequisites:** ionic formulas; element names
**Emphasis evidence:** Ch. 4 outcome 4 bold (Day 7 p.13; Day 8 p.5); §4.3 bold (Day 7 p.12; Day 8 p.4); red circles around LiF, NaCl, MgO, and MgCl₂ in the table (Day 7 p.21). The same slide, with the same circles, returns on Day 8 p.6: shown on two consecutive lecture days.

### Definitions and terminology
- [SOURCE-DERIVED] "How do we *name* an ionic compound? The name of a binary ionic compound is just the name of the cation followed by the name of the anion. The name of the cation is just the name of the parent element! The name of the anion is the name of the parent element with the ending changed to –ide." (Day 7 p.21)

### Worked examples
- [SOURCE-DERIVED] lithium fluoride, sodium chloride, magnesium oxide, "But also magnesium chloride!", matching the four red-circled formulas LiF, NaCl, MgO, MgCl₂ (Day 7 p.21). Names are written in lowercase.

### Recognition cues
- [INFERRED] Two elements, main-group metal + nonmetal → cation name + anion stem with -ide, and no number prefixes.

### Common mistakes flagged
- [INFERRED] Adding number prefixes ("magnesium dichloride"). "But also magnesium chloride!" signals that the subscript 2 does not appear in the name.

### Uncertainties and discrepancies
- [SOURCE-DERIVED] Day 7 left out Roman-numeral names for transition metals, polyatomic ions, prefixes for molecular compounds, and acids. Day 8 covers the first three (p.7–13; see the concepts below). Acids (textbook §4.3) have not appeared on any slide through Day 8.

## Transition-Metal Ions: Roman Numerals in Names

**Sources:** Day 8 p.7, p.10 (Top Hat)
**Unit / lecture order:** Day 8, right after the binary-ionic naming rule is repeated (p.6)
**Prerequisites:** naming binary ionic compounds; formulas of ionic compounds (charge balance); configurations of transition-metal cations (Day 6 p.21–23)
**Emphasis evidence:** "**transition metals**" printed bold (Day 8 p.7); a Top Hat question follows (p.10); Ch. 4 outcome 4 bold on Day 7 p.13 and Day 8 p.5.

### Definitions and terminology
- [SOURCE-DERIVED] "Many **transition metals** have more than one common ion! These different ions have different chemical properties, so we need to be able to *name* them differently. We add a Roman numeral that represents the charge on the metal to the name of the ion. There are also “historical names”, but we're not going to worry about them." (Day 8 p.7)
- [SOURCE-DERIVED] The Top Hat question calls the Roman-numeral name the "systematic name" (Day 8 p.10).

### Three representations
- Macroscopic: two copper oxides that look different: CuO is a black powder, Cu₂O a red powder (photos (a) and (b), Day 8 p.7).
- Symbolic: CuO "copper (II) oxide" (historical: cupric oxide); Cu₂O "copper (I) oxide" (historical: cuprous oxide) (Day 8 p.7).
- Particulate: [INFERRED] Cu²⁺ with O²⁻ (1 : 1) vs. Cu⁺ with O²⁻ (2 : 1); the Roman numeral is the charge on each copper ion, not the number of copper atoms.

### Worked examples
- (Day 8 p.7) CuO → copper (II) oxide; Cu₂O → copper (I) oxide. The slide shows the answers only, not the charge-balance step.
- (Day 8 p.10) Top Hat: "What is the systematic name for Fe₂O₃?" The answer is not on the slide. [VERIFICATION] 2 Fe³⁺ + 3 O²⁻ → Fe₂O₃ balances in atoms and charge (`tools/chemistry_verify.py check`), so the name is iron(III) oxide; the slide's spacing would give "iron (III) oxide".

### Procedures, shortcuts, assumptions, warnings
- [INFERRED from Day 8 p.7, p.10] Work backward from the formula: the anion's charge is fixed by its group (or by the polyatomic-ion table), so charge balance gives the metal's charge, which becomes the Roman numeral.

### Recognition cues
- [INFERRED] A transition metal (groups 3–12) in an ionic formula → a Roman numeral is needed; a main-group metal with one common ion (Na⁺, Mg²⁺, Al³⁺) → no Roman numeral (Day 7 p.19–21).

### Common mistakes flagged
- [INFERRED] Reading the Roman numeral as the subscript (Cu₂O is copper (I), not "copper (II)"); dropping the numeral for a transition metal; using the historical -ic/-ous names, which the course doesn't require (Day 8 p.7).

### Connections
- Builds on: formulas of ionic compounds (charge balance, Day 7 p.20); transition-metal cations such as Ni²⁺ and V³⁺ (Day 6 p.21–23). [INFERRED]

### Uncertainties and discrepancies
- [SOURCE-DERIVED] The slide writes a space before the Roman numeral, "copper (II) oxide" (Day 8 p.7). Standard IUPAC style has no space: copper(II) oxide [CLARIFICATION]. Either form communicates the charge; the textbook's form is checked in `TEXTBOOK_MAP.md`.

## Polyatomic Ions

**Sources:** Day 8 p.8–9
**Unit / lecture order:** Day 8
**Prerequisites:** covalent bonds (Day 7 p.14); ion charges; naming ionic compounds
**Emphasis evidence:** "**Polyatomic ions:**" bold (Day 8 p.8); red circles around HCO₃⁻, ClO₂⁻, NH₄⁺, and NO₃⁻ (Day 8 p.9); an explicit exam statement (below); Ch. 4 outcome 5 bold (Day 8 p.5).

### Definitions and terminology
- [SOURCE-DERIVED] "**Polyatomic ions:** several non-metal atoms covalently bonded together, but with an overall charge. Almost all of them are anions, but ammonium is a cation." (Day 8 p.8)
- [SOURCE-DERIVED] Exam policy: "You will be provided with a table like this on the exams, so you don't need to memorize them… … but the sooner you learn the ones we see frequently, the faster you'll be able to solve whatever problem is being asked." (Day 8 p.8)
- [SOURCE-DERIVED] "Table 4.5 Some Common Polyatomic Ions" (Day 8 p.8–9, 400-dpi zoom): CO₃²⁻ carbonate; HCO₃⁻ hydrogen carbonate or bicarbonate; CH₃COO⁻ acetate; CN⁻ cyanide; SCN⁻ thiocyanate; ClO⁻ hypochlorite; ClO₂⁻ chlorite; ClO₃⁻ chlorate; ClO₄⁻ perchlorate; CrO₄²⁻ chromate; Cr₂O₇²⁻ dichromate; MnO₄⁻ permanganate; N₃⁻ azide; NH₄⁺ ammonium; NO₂⁻ nitrite; NO₃⁻ nitrate; OH⁻ hydroxide; O₂²⁻ peroxide; PO₄³⁻ phosphate; HPO₄²⁻ hydrogen phosphate; H₂PO₄⁻ dihydrogen phosphate; S₂²⁻ disulfide; SO₃²⁻ sulfite; SO₄²⁻ sulfate; HSO₃⁻ hydrogen sulfite or bisulfite; HSO₄⁻ hydrogen sulfate or bisulfate.

### Three representations
- Symbolic: the formula and charge of each ion (Table 4.5); in a compound, the ion keeps its formula: NH₄ClO₂ = NH₄⁺ + ClO₂⁻.
- Particulate: [INFERRED] atoms held together by covalent bonds inside the ion, while the whole ion attracts oppositely charged ions ionically (both bond types in one compound).

### Worked examples
- (Day 8 p.9) Under the heading "How do we *name* an ionic compound?": "LiNO₃ is lithium nitrate; NaHCO₃ is sodium bicarbonate; NH₄ClO₂ is ammonium chlorite", with the same cation-then-anion rule. [VERIFICATION] each is charge-balanced 1 : 1 (`tools/chemistry_verify.py check`).

### Recognition cues
- [INFERRED] A group of atoms that matches a Table 4.5 formula (NO₃, SO₄, NH₄, …) → name it as a unit and don't change its ending; a single-element anion → the -ide ending.

### Common mistakes flagged
- [INFERRED] Breaking the ion apart when naming or counting charge ("lithium nitrogen trioxide"); confusing -ate with -ite (NO₃⁻ vs. NO₂⁻); treating NH₄⁺ as an anion.

### Connections
- Builds on: covalent bonds (Day 7 p.14): the slide defines these ions as "covalently bonded" (Day 8 p.8); naming binary ionic compounds (Day 8 p.9 reuses that rule). Used later in: Lewis structures of polyatomic ions (Ch. 4 outcome 5, Day 8 p.5).

### Uncertainties and discrepancies
- [CLARIFICATION] The definition says "several non-metal atoms", but chromate, dichromate, and permanganate contain the metals Cr and Mn.
- [CLARIFICATION] Day 8 p.9 keeps the heading "The name of a binary ionic compound…" for LiNO₃, NaHCO₃, and NH₄ClO₂, which have three or four elements. "Binary" means two elements; the same cation-then-anion rule applies to any ionic compound.
- [INFERRED, not on the slides] Patterns in Table 4.5: -ate has one more O than -ite (NO₃⁻/NO₂⁻, SO₄²⁻/SO₃²⁻); per- and hypo- extend the chlorine series (ClO₄⁻ … ClO⁻); "hydrogen" or "bi-" adds H and lowers the charge by 1 (CO₃²⁻ → HCO₃⁻).

## Naming Covalent Compounds

**Sources:** Day 8 p.12–13
**Unit / lecture order:** Day 8, after ionic naming and the covalent H–H curve
**Prerequisites:** naming binary ionic compounds (same parent-element and -ide pattern); telling covalent from ionic compounds (nonmetals only)
**Emphasis evidence:** "**first**" (twice) and "**number**" printed bold (Day 8 p.12); Table 4.3 on screen for two slides (p.12–13); Ch. 4 outcome 4 ("Name molecular and ionic compounds…") bold on Day 7 p.13 and Day 8 p.5.

### Definitions and terminology
- [SOURCE-DERIVED] "How do we *name* a covalent compound? The name of a binary covalent compound starts with the name of the parent element of the **first** element in the formula… … followed by the name of the parent element of the second element with ending changed to –ide. We use prefixes to indicate the **number** of each kind of atom in the formula. Exception: we do not use “mono” for the **first** element." (Day 8 p.12)
- [SOURCE-DERIVED] "Table 4.3 Naming Prefixes for Molecular Compounds": one mono-, two di-, three tri-, four tetra-, five penta-, six hexa-, seven hepta-, eight octa-, nine nona-, ten deca- (Day 8 p.12–13).

### Worked examples
- (Day 8 p.13) SO₂: sulfur dioxide; SO₃: sulfur trioxide; S₂F₂: disulfur difluoride.

### Procedures, shortcuts, assumptions, warnings
- [SOURCE-DERIVED] First element: its element name, with a prefix only if there are two or more atoms ("we do not use “mono” for the first element"). Second element: prefix plus the -ide name (Day 8 p.12).

### Recognition cues
- [INFERRED] Two nonmetals → covalent → prefixes (sulfur dioxide); a metal + a nonmetal → ionic → no prefixes (magnesium chloride, Day 7 p.21). The subscripts go into the name only for covalent compounds.

### Common mistakes flagged
- [INFERRED] Using prefixes for ionic compounds ("magnesium dichloride", the Day 7 p.21 contrast), or leaving them out for covalent ones ("sulfur oxide" can't tell SO₂ from SO₃); writing "monosulfur".

### Connections
- Builds on: naming binary ionic compounds (the same parent-element and -ide wording, Day 8 p.6 vs. p.12); primary types of chemical bonds (covalent = nonmetals, Day 7 p.14).

### Uncertainties and discrepancies
- [CLARIFICATION] The slides don't mention dropping a prefix's final vowel before "oxide" (monoxide, pentoxide, as in CO, carbon monoxide). The textbook's practice is recorded in `TEXTBOOK_MAP.md`.

## Lewis Symbols and the Octet Rule

**Sources:** Day 8 p.16–18
**Unit / lecture order:** Day 8, opening §4.4
**Prerequisites:** valence electrons (Day 6 p.14); electron configurations and orbital filling (Day 6 p.6–17); noble-gas configurations of ions (Day 7 p.18)
**Emphasis evidence:** §4.4 bold (Day 7 p.12; Day 8 p.4); Ch. 4 outcome 5 bold (Day 8 p.5); "**sharing pairs of electrons**", "**valence**", "**bonding capacity**", and "**unpaired**" bold (Day 8 p.16–18); an explicit instruction to memorize (below).

### Definitions and terminology
- [SOURCE-DERIVED] "G. N. Lewis of Weymouth Massachusetts! 1916. Proposed that atoms form bonds by **sharing pairs of electrons** in order to mimic the valence electron configuration of noble gases. This is the “octet rule”: All main group atoms tend to gain, lose, or share electrons so that each atom has eight valence electrons. Hydrogen only needs two electrons to obtain [He]" (Day 8 p.16)
- [SOURCE-DERIVED] "Lewis symbols: The chemical symbol for an element surrounded by one or more dots representing **valence** electrons. Write the symbol. Place dots on four sides of the symbol, one at a time before pairing. This is LIKE putting electrons into s and p orbitals, but Lewis didn't know that orbitals existed." (Day 8 p.17)
- [SOURCE-DERIVED] "The **bonding capacity** of an element is the number of covalent bonds an atom forms to have an octet of electrons in its valence shell. The number of **unpaired** electrons in a Lewis symbol indicates the number of bonds that will form." (Day 8 p.18)
- [SUPPORTED EMPHASIS] "As a critical example that you should “memorize” right now: carbon ALMOST ALWAYS forms 4 covalent bonds." (Day 8 p.18; the only "memorize" instruction in Days 1–8)

### Three representations
- Symbolic: the Lewis-symbol periodic table (Day 8 p.17–18, 400-dpi zoom): ·H and :He; ·Li, ·Be· (two single dots), B with 3 dots, C with 4 single dots, N with 5 (one pair), O with 6 (two pairs), F with 7 (three pairs), Ne with 8 (four pairs). Each column repeats the pattern, and the tiles are colored as metals (tan), metalloids (green), and nonmetals (blue).
- Particulate: [INFERRED] the dots are the valence electrons, the ones that take part in bonding; unpaired dots are the sites where a bond can form.

### Procedures, shortcuts, assumptions, warnings
- [SOURCE-DERIVED] Write the symbol, then add dots on four sides one at a time before pairing (Day 8 p.17). [INFERRED] It's the same "don't pair until you have to" rule as Hund's rule (Day 6 p.16).

### Recognition cues
- [INFERRED] Count the unpaired dots for the number of bonds: H 1, C 4, N 3, O 2, F (halogens) 1. [VERIFICATION] 8 minus the valence electrons for groups 14–17, and 2 − 1 for H (Python).

### Common mistakes flagged
- [INFERRED] Drawing all of a main-group atom's electrons instead of only the valence electrons; pairing dots too early (C drawn with two pairs would suggest 2 bonds, not 4).

### Connections
- Builds on: valence electrons (Day 6 p.14); orbital filling (the slide's "LIKE putting electrons into s and p orbitals", Day 8 p.17); noble-gas configurations of ions (Day 7 p.18): the octet rule's "gain, lose, or share" covers both ions and shared pairs. Used later in: Lewis structures (Day 8 p.19–30).

### Uncertainties and discrepancies
- [CLARIFICATION] Lewis dots show bonding sites, not orbital occupancy. Be (2s²) is drawn ·Be·, and C (2s²2p², two unpaired electrons in the orbital picture) is drawn with four single dots. The slide flags this as an analogy ("LIKE… but Lewis didn't know that orbitals existed").
- [CLARIFICATION] The lecture's *bonding capacity* (Day 8 p.18) is what the textbook calls an element's *valence*: "the capacity of the atoms of a particular element to form chemical bonds" (TB PDF p.181).

## Lewis Structures of Molecular Compounds

**Sources:** Day 8 p.19–26, p.28–30; Day 9 p.6, p.19–20
**Unit / lecture order:** Day 8, §4.4, the last topic of the deck; Day 9 repeats the ozone exercise and adds N₂O
**Prerequisites:** Lewis symbols and the octet rule; bonding capacity
**Emphasis evidence:** "**more than one pair of electrons**", "A double bond!", "A triple bond!" printed bold (Day 8 p.20); §4.4 bold and outcome 5 bold (Day 8 p.4–5; again Day 9 p.4–5). [SUPPORTED EMPHASIS] The five steps appear word for word on nine slides across two lectures (Day 8 p.21, 22, 23, 25, 28, 29, 30; Day 9 p.6, p.19), with "**bonding capacity**" bold each time.

### Definitions and terminology
- [SOURCE-DERIVED] "In a fluorine, F₂, molecule, each F atom shares one electron to attain an octet." The figure shows :F: (three pairs) with one single dot, plus the mirror-image F; arrows point to the two single electrons, "Electrons to share" (Day 8 p.19; © 2012 Pearson figure).
- [SOURCE-DERIVED] "Formation of Multiple Bonds: In O₂ and N₂, **more than one pair of electrons** are shared in order to achieve a filled valence shell." Two O atoms (6 dots each) → O::O (two shared pairs, two lone pairs on each O) = O=O, "A double bond!". Two N atoms (5 dots each) → :N:::N: = :N≡N:, "A triple bond!" (Day 8 p.20)

### Three representations
- Symbolic: dots for every electron (O::O) and the same structure with lines for shared pairs (O=O), shown side by side with "=" (Day 8 p.20).
- Particulate: [INFERRED] a shared pair lies between two nuclei and counts toward both atoms' octets; lone pairs belong to one atom.

### Worked examples
- (Day 8 p.19–20) F₂ single bond; O₂ double bond; N₂ triple bond. [VERIFICATION] 14, 12, and 10 valence electrons, which is exactly 1 bond + 6 lone pairs, 2 bonds + 4 lone pairs, and 3 bonds + 2 lone pairs (`tools/chemistry_verify.py electrons`).

### Recognition cues
- [INFERRED] If single bonds leave an atom short of an octet, turn lone pairs into shared pairs: 2 unpaired electrons per O → a double bond; 3 per N → a triple bond (bonding capacity, Day 8 p.18).

### Procedures, shortcuts, assumptions, warnings
- [SOURCE-DERIVED] "Five Steps for Drawing Lewis Structures: 1. Determine the number of valence electrons. 2. Arrange symbols of elements to show how the atoms are bonded together and connect them with single bonds. The central atom is the one with the largest **bonding capacity**. 3. Complete the octet of atoms bonded to each “central” atom by adding lone pairs of electrons (exception: hydrogen only needs two). 4. Compare the number of valence electrons in the Lewis structure to the number determined in step 1. 5. Use any leftover electrons to complete the octet on the central atom." (Day 8 p.21)
- [SOURCE-DERIVED] Step 1 is done as a table: element symbol, number of atoms, valence electrons per atom, total (Day 8 p.22, p.25, p.28).
- [INFERRED] The five steps don't say what to do when the central atom still lacks an octet after step 5. The ethyne and ozone examples show the answer: turn lone pairs on the bonded atoms into shared pairs (multiple bonds), as with O₂ and N₂ (Day 8 p.20, p.25, p.29–30).

### Worked examples
- (Day 8 p.22–23) Ammonia, NH₃: N 1 × 5 = 5, H 3 × 1 = 3, "Valence electrons in NH₃ 8". The skeleton has N in the center with three N–H single bonds, drawn T-shaped; the leftover 2 electrons go on N as a lone pair.
- [UNCERTAIN] Day 8 p.23 carries a callout in the PDF's text layer that is hidden in the rendered slide (black text beneath another text box; probably revealed by animation in class): "Note that a Lewis structure is a two-dimensional representation. We'll see later that ammonia is tetrahedral, but Lewis structures can't tell us that!" [SOURCE-DERIVED] Resolved on Day 10: ammonia's *electron-pair* geometry is tetrahedral and its *molecular* geometry trigonal pyramidal, 107° (Day 10 p.16–18). [INFERRED] The callout's "tetrahedral" means the electron-pair geometry.
- (Day 8 p.24–25) "That was pretty easy, right? Let's try another one." C₂H₂: "Historical name: acetylene; Systematic name: ethyne". C 2 × 4 = 8, H 2 × 1 = 2, "TOTAL: 10". The skeleton H–C–C–H becomes H–C≡C–H.
- (Day 8 p.28–30) Ozone, O₃: O 3 × 6 = 18. The skeleton O–O–O (p.28) gets three lone pairs on each end O, then one lone pair on the central O (p.29), which leaves the central O with only 6 electrons. The final slide shows two bent structures, O=O–O and O–O=O: the double-bonded end O has two lone pairs, the central O one, and the single-bonded end O three (p.30).
- [VERIFICATION] RDKit and `tools/chemistry_verify.py electrons`: NH₃ 8, C₂H₂ 10, and O₃ 18 valence electrons. Every atom in the final structures has an octet (H has 2). In each O₃ structure the formal charges are −1 (single-bonded O), +1 (central), and 0; formal charge (§4.7) is not bold on Day 8 p.4 [CLARIFICATION] but is taught on Day 9 (see **Formal Charge**).
- (Day 9 p.6) "Practice Exercise: Ozone, O₃" repeated with the two final structures beside the five steps, to open Day 9's resonance lesson.
- (Day 9 p.19–20) "Practice Exercise: N₂O": step-1 table N 2 × 5 = 10, O 1 × 6 = 6, "TOTAL: 16"; skeleton N–N–O. After step 3 the central N has only 4 electrons (p.20, row 2); three complete structures follow: :N≡N–Ö:, :N̈–N≡O:, and N=N=O with two lone pairs on each end atom. Choosing among them needs formal charge (Day 9 p.21–24).

### Professor explanations, models, and diagrams
- [SOURCE-DERIVED] "Further Considerations: That was pretty easy, right? So why is this ever difficult? Sometimes it is **impossible** for every atom to have an octet. Sometimes it is possible to draw more than one perfectly valid Lewis structure. We'll need to learn some new chemistry to help us resolve these situations: Electronegativity, Formal Charge, **Resonance**" (Day 8 p.26; only "impossible" and "Resonance" are bold). The slide shows the finished NH₃ and C₂H₂ structures.
- [SOURCE-DERIVED] Confirmed on Day 9: the two O₃ structures (Day 8 p.30) are "in resonance" (Day 9 p.8) and are joined by ↔ (Day 9 p.9). The announced topics (electronegativity, formal charge, resonance) are all taught on Day 9, along with the octet exceptions ("impossible for every atom to have an octet").

### Recognition cues
- [INFERRED] "Draw the Lewis structure of …" → the five steps. H is never central (bonding capacity 1); with C present, C is central (4 bonds, "memorize", Day 8 p.18). If the electron count comes out short of octets, add a multiple bond.

### Common mistakes flagged
- [INFERRED] Skipping step 1's electron count (the table exists for this); putting H in the middle; giving H lone pairs; stopping at step 5 with a central atom that has only 6 electrons (the O₃ stage on p.29); forgetting that the two O₃ structures are equally valid.

### Connections
- Builds on: Lewis symbols and bonding capacity (Day 8 p.16–18); covalent bonds as shared electrons (Day 7 p.14); allotropes, which introduce O₃ (Day 8 p.27). Used later in: resonance (Day 9 p.6–13), formal charge (Day 9 p.19–26), and the octet exceptions (Day 9 p.27–30), as announced on Day 8 p.26; VSEPR, which needs "a valid Lewis structure!" (Day 10 p.8); valence bond theory, which "reconcile[s]" Lewis structures with orbitals (Day 11 p.9).

## Allotropes: O₂ and O₃

**Sources:** Day 8 p.27 (and the Mario Molina slide, p.2)
**Unit / lecture order:** Day 8, just before the ozone practice exercise
**Prerequisites:** molecules and formulas; covalent bonds
**Emphasis evidence:** one slide; "CFCs might lead to the destruction of the ozone layer" bold on the Representation Matters slide (Day 8 p.2).

### Definitions and terminology
- [SOURCE-DERIVED] "Allotropes: different molecular forms of the same element. O₂ vs O₃" (Day 8 p.27)

### Three representations
- Macroscopic: lightning; the "Ozone in the Atmosphere" profile of altitude (km at left, 0–35; miles at right) vs. ozone concentration, peaking in the stratospheric "Ozone Layer" near 20–25 km, with "Tropospheric Ozone" below and "Ozone increases from pollution" near the ground; satellite maps of the Antarctic ozone hole, 1979 vs. 2008 (Day 8 p.27).
- Particulate: space-filling spheres, O₂ → two O atoms, then O₂ + O → O₃ (the inset above the lightning, Day 8 p.27).
- Symbolic: [VERIFICATION] O₂ → 2 O and O₂ + O → O₃ balance (`tools/chemistry_verify.py check`).

### Connections
- Builds on: the Representation Matters slide: Molina and Rowland predicted "that CFCs might lead to the destruction of the ozone layer" (Day 8 p.2). Used later in: the ozone Lewis structure (Day 8 p.28–30); resonance (Day 9 p.6–10); the bent, 117° shape of a central atom with one lone pair (Day 10 p.14–15).

## Resonance

**Sources:** Day 9 p.6–13 (and Day 9 p.2, Representation Matters; Day 10 p.14–15; Day 11 p.26)
**Unit / lecture order:** Day 9 ("Advanced Lewis Structures", Day 9 p.1), right after the ozone practice exercise is repeated
**Prerequisites:** Lewis structures (five steps); allotropes (O₃); typical single vs. double bond lengths
**Emphasis evidence:** §4.6 Resonance bold (Day 8 p.4; Day 9 p.4) and "**Resonance**" bold as the announced next topic (Day 8 p.26); outcome 6 ("Draw resonance structures and use formal charges to evaluate their relative importance") fully bold on Day 9 p.5, where Day 8 p.5 bolded only its first half; the key phrases "**neither structure alone is correct**", "**in between**", "**average**", "**better**", "**more stable**" are bold (Day 9 p.9–10). Five slides on ozone (Day 9 p.6–10) and two on benzene (p.12–13); the Representation Matters slide (Kathleen Lonsdale and benzene's equal C–C bonds, Day 9 p.2) introduces the same idea.

### Definitions and terminology
- [SOURCE-DERIVED] "These structures are **equivalent**. That does **not** mean they are **the same**. But we can transform one of these structures into the other **by only moving electrons.** When two (or more) structures can be interconverted by just moving electrons, we say they are "in resonance," and each of them is a "resonance structure."" (Day 9 p.8)
- [SOURCE-DERIVED] "Importantly, **neither structure alone is correct**. The molecule is NOT "changing" back and forth between these two structures. Rather, it is ALWAYS somewhere **in between**. An **average** of the two." (Day 9 p.9–10)
- [SOURCE-DERIVED] "An even **better** way to draw this structure is as the "resonance hybrid", where we use dashed lines to indicate partial bonds. We say that those electrons are "delocalized". For reasons beyond the scope of this class, molecules with delocalized electrons are **more stable** than they would be otherwise." (Day 9 p.10)

### Equations and relationships
- [SOURCE-DERIVED] The evidence: "Which of these structures is correct? Interestingly, the answer turns out to be "neither." In ozone, O₃, the bond length between **each** two oxygen atoms is 128 pm. A typical O—O bond is 148 pm. A typical O=O bond is 121 pm. The bonds in ozone are somewhere in between." Reference molecules are drawn beside the numbers: O=O (O₂, 121 pm, blue) and H–O–O–H (H₂O₂, 148 pm, red) (Day 9 p.7). The same values are in Table 4.6 (Day 9 p.14) and the textbook (TB PDF p.203, p.206).

### Three representations
- Macroscopic: [SOURCE-DERIVED] measured bond lengths (O₃, Day 9 p.7); benzene's C–C bonds, all "the same length, and … somewhere between a single and a double bond", found by Lonsdale's crystallography in 1929 (Day 9 p.2); benzene "doesn't **behave** as though it has double bonds – its chemistry is fundamentally different than any alkenes" (Day 9 p.13).
- Symbolic: [SOURCE-DERIVED] resonance structures joined by the double-headed arrow ↔ (Day 9 p.9, p.13); red curved arrows showing which electron pairs move, with a plain → between the two structures (Day 9 p.9); the hybrid drawn with solid + dashed lines (Day 9 p.10, p.13) and benzene as a hexagon with an inscribed circle (Day 9 p.13).
- Particulate: [SOURCE-DERIVED] the moving electrons are "delocalized" (Day 9 p.10). [INFERRED] Every O₃ molecule is the same hybrid at every instant; nothing flips between forms (the slide's "NOT 'changing' back and forth").

### Professor explanations, models, and diagrams
- [SOURCE-DERIVED] Curved arrows (Day 9 p.9): two red arrows turn O=O–O into O–O=O. One moves the second pair of the double bond onto the left terminal O; the other moves a lone pair of the right terminal O into the O–O bond. Below, the same two structures are joined by ↔.
- [SOURCE-DERIVED] The O₃ resonance hybrid (Day 9 p.10, 300-dpi crop): bent, each O–O drawn as a solid + a dashed line, one lone pair on the central O, and five dots on each terminal O (the average of its 6 and 4).
- [SOURCE-DERIVED] Analogy cartoon: "rhinoceros = [ dragon ↔ unicorn ]" (Day 9 p.11, credited to chim.lu; no text). [INFERRED] The real animal (the hybrid) is not a dragon one moment and a unicorn the next; it is described as a blend of two imaginary creatures (the resonance structures).
- [SOURCE-DERIVED] Benzene (Day 9 p.12–13): its formula, C₆H₆, was known in the mid-1800s, "but with the chemistry we knew at the time, we couldn't draw any structures that made any sense." Kekulé (in 1865 or so, "inspired by a dream he had of a snake devouring its own tail") proposed a ring of alternating single and double bonds that was "*nearly* correct." Slide p.13 shows the two Kekulé structures (↔), then two hybrid drawings: dashed partial bonds, and the circle.

### Worked examples
- (Day 9 p.6–10) Ozone. The Day 8 answer (two structures, Day 9 p.6) → "neither" (p.7) → "in resonance" (p.8) → curved arrows and ↔ (p.9) → the hybrid (p.10).
- [VERIFICATION] Each O₃ structure has formal charges 0 (double-bonded O), +1 (central O), −1 (single-bonded O), sum 0, 18 valence electrons (RDKit). Averaged over the two structures, each terminal O is −½ and each O–O bond order is 1.5 (Python). [CLARIFICATION: the textbook states the bond order 1.5, "neither 1 nor 2" (TB PDF p.206); the slides say only "in between".]

### Recognition cues
- [INFERRED] Two or more valid Lewis structures in which the atoms stay put and only electrons (lone pairs, multiple bonds) move → resonance. If atoms move, the structures are different molecules, not resonance structures.
- [INFERRED] An atom with a double bond to one atom and a single bond to another atom of the same element (the central O of O₃; N in NO₂; S in SO₄²⁻, Day 9 p.28–30) → look for equivalent resonance structures. [CLARIFICATION: the textbook gives this test, "having both single and double bonds to two or more atoms of the same element" (TB PDF p.205).]

### Common mistakes flagged
- [SOURCE-DERIVED] The slide's own warning: the molecule "is NOT 'changing' back and forth between these two structures" (Day 9 p.9).
- [INFERRED] Reading "equivalent" as "the same picture" (Day 9 p.8 separates the two); moving atoms instead of electrons; using ↔ for a reaction or ⇌ for resonance; expecting O₃ to have one 121 pm bond and one 148 pm bond.

### Connections
- Builds on: the ozone Lewis structures (Day 8 p.28–30; Day 9 p.6); typical bond lengths (Day 9 p.7, p.14). Used later in: formal charge, which ranks non-equivalent resonance structures (Day 9 p.24 table, "the resonance structures of N₂O"); NO₂ and SO₄²⁻ among the octet exceptions (Day 9 p.28–30); the ozone VSEPR example, whose two resonance structures give one geometry (Day 10 p.14–15); benzene's delocalized π cloud in valence bond theory (Day 11 p.26).

### Uncertainties and discrepancies
- [SOURCE-DERIVED] Scope: why delocalization stabilizes a molecule is "beyond the scope of this class" (Day 9 p.10). [CLARIFICATION: the textbook's reason is that delocalization lowers the electrons' potential energy, "resonance stabilization" (TB PDF p.204).]
- [CLARIFICATION] Lonsdale's 1929 crystal structure was of hexamethylbenzene, C₆(CH₃)₆, which showed a flat ring with equal C–C bonds; the slide says "benzene" (Day 9 p.2). History detail on a non-content slide.

## The Lengths and Strengths of Covalent Bonds

**Sources:** Day 9 p.7, p.14; Day 8 p.11 (the H–H curve)
**Unit / lecture order:** Day 9, between benzene resonance and electronegativity
**Prerequisites:** single, double, and triple bonds in Lewis structures; the covalent H–H energy curve
**Emphasis evidence:** §4.5 "The Lengths and Strengths of Covalent Bonds" bold (Day 8 p.4; Day 9 p.4); Ch. 4 outcome 7 ("Describe how bond order, bond energy, and bond length are related") bold on Day 9 p.5 and on no earlier day; four groups of rows boxed in red on Table 4.6 (Day 9 p.14).

### Definitions and terminology
- [SOURCE-DERIVED] The slides define none of the three terms: "bond order", "bond energy", and "bond length" appear only in outcome 7 (Day 9 p.5) and in Table 4.6's column headings "Bond Length (pm)" and "Bond Energy (kJ/mol)" (Day 9 p.14). [CLARIFICATION: textbook definitions: bond order is the number of bonds between two atoms, 1 for a single bond, 2 for a double, 3 for a triple (TB PDF p.206); bond energy is the energy needed to break one mole of a specific covalent bond in the gas phase (TB PDF p.185), always positive (TB PDF p.208).]

### Equations and relationships
- [SOURCE-DERIVED] Table 4.6 "Average Lengths and Energies of Selected Covalent Bonds", the textbook's table as an image (Day 9 p.14 = TB PDF p.207), in pm / kJ/mol: C–C 154/348, C=C 134/614, C≡C 120/839 · C–N 147/293, C=N 127/615, C≡N 116/891 · C–O 143/358, C=O 123/743ᵃ, C≡O 113/1072 · C–H 110/413 · C–F 133/485 · C–Cl 177/328 · N–H 104/391 · N–N 147/163, N=N 124/418, N≡N 110/945 · N–O 136/201, N=O 122/607, N≡O 106/678 · O–O 148/146, O=O 121/498 · O–H 96/463 · S–O 151/265, S=O 143/523 · S–S 204/266 · S–H 134/347 · H–H 74/436 · H–F 92/567 · H–Cl 127/431 · H–Br 141/366 · H–I 161/299 · F–F 143/155 · Cl–Cl 200/243 · Br–Br 228/193 · I–I 266/151. Footnote: "ᵃThe bond energy of the C—O bond in CO₂ is 799 kJ/mol." 35 rows.
- [SUPPORTED EMPHASIS] Red boxes (annotation, Day 9 p.14) surround exactly four groups: C–C/C=C/C≡C; C–O/C=O/C≡O; O–O/O=O; F–F/Cl–Cl/Br–Br/I–I. [INFERRED] Each carbon and oxygen group shows that a higher bond order means a shorter and stronger bond. The halogen group shows length growing down the group (143 → 266 pm) while energy does not fall smoothly (F–F 155 < Cl–Cl 243 kJ/mol). The slide does not say why each group is boxed.
- [SOURCE-DERIVED] H–H: the 74 pm minimum and −436 kJ/mol depth of the Day 8 p.11 curve equal Table 4.6's H–H row, 74 pm and 436 kJ/mol (Day 9 p.14). [INFERRED: bond length is the curve's minimum position; bond energy is the depth of the well, reported as a positive number.]

### Three representations
- Macroscopic: [SOURCE-DERIVED] the measured quantities in Table 4.6, average bond lengths (pm) and bond energies (kJ/mol) (Day 9 p.14).
- Symbolic: [SOURCE-DERIVED] bond lines –, =, ≡ in Table 4.6's Bond column (Day 9 p.14).
- Particulate: [INFERRED] more shared pairs between two nuclei pull them closer and take more energy to separate.

### Worked examples
- (Day 9 p.7) O₃'s 128 pm falls between O–O 148 and O=O 121 pm, the evidence for resonance.
- [VERIFICATION] Python: O₃ bond order = 3 bonding pairs / 2 bonds = 1.5. Doubling is not additive: C=C 614 < 2 × 348 = 696 kJ/mol; C≡C 839 < 3 × 348 = 1044 kJ/mol.

### Recognition cues
- [INFERRED] "Rank these bonds by length or by strength", "which C–O bond is shortest?", "what does an intermediate bond length tell you?" → bond order first (from the Lewis structure, averaged over resonance structures), then Table 4.6.

### Common mistakes flagged
- [INFERRED] Expecting a double bond to be twice as strong as a single bond; expecting bond energy to fall steadily down a group (F–F is weaker than Cl–Cl); mixing up "longer" with "stronger" (they run opposite for a given pair of atoms).

### Connections
- Builds on: the covalent H–H curve (Day 8 p.11). Used in: the resonance evidence (Day 9 p.7). [CLARIFICATION] Valence bond theory's σ + π picture of multiple bonds (Day 11 p.17–23) is the usual explanation for why a double bond is less than twice a single bond; the slides don't connect the two.

### Uncertainties and discrepancies
- [CLARIFICATION] "Table 4.6" is the same number in the supplied 3rd edition (TB PDF p.207), unlike Day 8's "Table 4.5" polyatomic ions (the book's Table 4.4).
- [UNCERTAIN] Whether Table 4.6 is given on exams or must be recalled is not stated (compare the explicit polyatomic-ion policy, Day 8 p.8).

## Electronegativity and Bond Polarity

**Sources:** Day 9 p.15–18; Day 10 p.27 (repeated)
**Unit / lecture order:** Day 9, after Table 4.6; the "Polar Bonds" slide is repeated to open the polarity part of Day 10
**Prerequisites:** covalent vs. ionic bonds; periodic trends (ionization energy, electron affinity)
**Emphasis evidence:** "4.2 **Electronegativity** and Bonding" (the word bold, Day 9 p.4); Ch. 4 outcome 3 ("Predict the polarity of covalent bonds on the basis of differences in the electronegativity between the bonded atoms") bold on Day 9 p.5, after being plain on Day 7 p.13 and Day 8 p.5; "**electronegativity,**" bold (Day 9 p.17); the battery figure in two lectures (Day 9 p.15; Day 10 p.27) and the electrostatic-potential figure on two slides (Day 9 p.16, p.18).

### Definitions and terminology
- [SOURCE-DERIVED] "Even when G.N. Lewis was developing the rules for his Lewis structures, he was aware that the electrons in covalent bonds didn't have to be shared **equally**. In many (most?) covalent bonds, one of the atoms has more of the electron density." (Day 9 p.15)
- [SOURCE-DERIVED] "To describe the polarity of bonds, we will introduce the concept of **electronegativity,** given the symbol χ." (Day 9 p.17). The slides give no further definition. [CLARIFICATION: the textbook: "a relative measure of an atom’s ability to attract electrons to itself within a bond" (margin definition; the body text on PDF p.186: "an atom’s tendency to attract electrons toward itself within a chemical bond") (TB PDF p.187).]

### Equations and relationships
- [SOURCE-DERIVED] Bond classes by electronegativity difference (Day 9 p.18): "Δχ ≤ 0.4 nonpolar covalent · 0.4 < Δχ < 2.0 polar covalent · Δχ ≥ 2.0 ionic", with "χ of Cl = 3.0 · χ of H = 2.1 · χ of Na = 0.9" beside the Cl₂, HCl, and NaCl maps. [VERIFICATION: Cl₂ Δχ = 0, nonpolar; HCl 3.0 − 2.1 = 0.9, polar covalent; NaCl 3.0 − 0.9 = 2.1, ionic (Python).] The textbook uses the same thresholds (TB PDF p.186).
- [SOURCE-DERIVED] Electronegativity values (Day 9 p.17; the textbook's Fig. 4.5 as 3-D bars, 300-dpi crop): H 2.1 · Li 1.1, Be 1.5, B 2.0, C 2.5, N 3.0, O 3.5, F 4.0 · Na 0.9, Mg 1.2, Al 1.5, Si 1.8, P 2.1, S 2.5, Cl 3.0 · K 0.8, Ca 1.0, Sc 1.3, Ti 1.5, V 1.6, Cr 1.6, Mn 1.5, Fe 1.8, Co 1.8, Ni 1.8, Cu 1.9, Zn 1.6, Ga 1.6, Ge 1.8, As 2.0, Se 2.4, Br 2.8 · Rb 0.8, Sr 1.0, Y 1.2, Zr 1.4, Nb 1.6, Mo 1.8, Tc 1.9, Ru 2.2, Rh 2.2, Pd 2.2, Ag 1.9, Cd 1.7, In 1.7, Sn 1.8, Sb 1.9, Te 2.1, I 2.5 · Cs 0.7, Ba 0.9, La 1.1, Hf 1.3, Ta 1.5, W 1.7, Re 1.9, Os 2.2, Ir 2.2, Pt 2.2, Au 2.4, Hg 1.9, Tl 1.8, Pb 1.9, Bi 1.9, Po 2.0, At 2.2 · Fr 0.7, Ra 0.9, Ac 1.1. No values for the noble gases.

### Three representations
- Macroscopic: [SOURCE-DERIVED] a battery with a + end and a − end, the analogy for a polar bond's δ+ and δ− ends (Day 9 p.15; Day 10 p.27).
- Symbolic: [SOURCE-DERIVED] δ+ and δ− labels; a crossed arrow over H–Cl with the + tail at H and the arrowhead at Cl (Day 9 p.15); Δχ values.
- Particulate: [SOURCE-DERIVED] electrostatic potential maps (Day 9 p.16, p.18) on a color scale from dark blue "1+" ("100% ionic") through "δ+", green-yellow "0" ("Nonpolar covalent"), and "δ−" to red "1−" ("100% ionic"): (a) Cl₂, "Nonpolar covalent: even charge distribution"; (b) HCl, "Polar covalent: uneven charge distribution" (greener at H, orange at Cl); (c) NaCl, "Ionic: complete transfer of electron" (Na⁺ blue, Cl⁻ red).

### Professor explanations, models, and diagrams
- [INFERRED] One color scale for all three maps puts the bond types on a single continuum: ionic bonding is the extreme of unequal sharing. The slides show this (Day 9 p.16, p.18) without saying it.

### Recognition cues
- [INFERRED] "Classify this bond as nonpolar covalent, polar covalent, or ionic", "which bond is most polar?", "which end is δ−?" → look up both χ values, subtract, and compare with 0.4 and 2.0; the more electronegative atom is δ−, and the arrowhead points to it.

### Common mistakes flagged
- [INFERRED] Pointing the arrow toward the δ+ end (this course: the arrowhead is at δ−, Day 9 p.15); treating the 0.4 and 2.0 cutoffs as sharp boundaries [CLARIFICATION: the textbook: "those cutoff values are more like guidelines than strict limits" (TB PDF p.186)]; assuming metal + nonmetal always means Δχ ≥ 2.0.

### Connections
- Builds on: covalent vs. ionic bonds (Day 7 p.14). [INFERRED] χ follows the IE₁ trend, rising across a row and falling down a group (Day 7 p.9); the slides don't make the comparison [CLARIFICATION: the textbook does, Fig. 4.6, TB PDF p.187]. Used later in: formal-charge rule 3, negative charges on "the more/most electronegative element" (Day 9 p.23); expanded octets around "strongly electronegative elements (F, O, and Cl)" (Day 9 p.29); polar molecules, with Δχ quoted for each bond (Day 10 p.27–31).

### Uncertainties and discrepancies
- [SOURCE-DERIVED] Li is 1.1 here (Day 9 p.17), as in the textbook's Fig. 4.5; many other tables list 1.0 (already logged in COURSE.md Discrepancies).
- [UNCERTAIN] Whether an electronegativity table is provided on exams is not stated.

## Formal Charge

**Sources:** Day 9 p.19–26, p.28, p.30
**Unit / lecture order:** Day 9, after electronegativity
**Prerequisites:** Lewis structures (five steps); valence-electron counts; electronegativity (rule 3)
**Emphasis evidence:** §4.7 "Formal Charge: Choosing among Lewis Structures" bold on Day 9 p.4 (plain on Day 8 p.4); outcome 6 fully bold (Day 9 p.5); "**formal charge**" and "**each atom:**" bold (Day 9 p.22); the FC equation on two slides (p.22, p.25); two Top Hat slides (p.25, and p.26, "a GREAT practice question").

### Definitions and terminology
- [SOURCE-DERIVED] "To choose between them, we will introduce the idea of **formal charge**, which is a comparison of how many electrons the atoms have in the compound to how many they had as free atoms. For **each atom:** 1. Determine the number of valence electrons in the free atom. 2. Count the number of electrons in lone pairs on the atom in the structure. 3. Count the number of electrons in bonds to the atom and divide that number by 2. 4. Sum the results of 2 and 3 and subtract from the number determined in step 1." (Day 9 p.22)

### Equations and relationships
- [SOURCE-DERIVED] FC = (number of valence e⁻) − [number of unshared e⁻ + ½(number of e⁻ in bonding pairs)], with the three terms colored blue, red, and green (Day 9 p.22, p.25; the textbook's Eq. 4.2, TB PDF p.209). The Day 9 p.24 table writes it FC = valence − [lone pair + ½ (shared)].

### Procedures, shortcuts, assumptions, warnings
- [SOURCE-DERIVED] "When choosing between multiple Lewis structures: 1. The best structure is the one in which the formal charge on each atom is zero. 2. If no such structure can be drawn, the best structure is the one where most of the atoms have formal charges equal to zero or as close to zero as possible. 3. Any negative formal charges should be on the atom(s) of the more/most electronegative element. 4. If you've done it right, the sum of the formal charges will be the charge on the molecule/ion." (Day 9 p.23)
- [SOURCE-DERIVED] Formal charges are written in red next to the atoms: "+1", "−1", "0", "+2" (Day 9 p.28, p.30).

### Three representations
- Symbolic: [SOURCE-DERIVED] the FC bookkeeping table (Day 9 p.24) and red FC labels on structures (Day 9 p.28, p.30).
- Particulate: [INFERRED] a formal charge compares an atom's share of the electrons (its lone pairs plus half of each shared pair) with the free atom's valence count; it is bookkeeping, not a measured charge.

### Worked examples
- (Day 9 p.19–24) N₂O. Step 1 table: N 2 × 5 = 10, O 1 × 6 = 6, "TOTAL: 16"; skeleton N–N–O (p.19). After step 3 the central N has only 4 electrons; three complete structures follow (p.20): A :N≡N–Ö:, B N=N=O with two lone pairs on each end atom, C :N̈–N≡O: (each counts to 16). "These structures are **not equivalent!** Which of them is "right"? Well, again, the answer is "none of them"… But one of them is better than the other two, and **closer** to the real structure." (p.21). The textbook's table "Formal charge calculations for the resonance structures of N₂O" is shown with its cells blank for class (p.24): "Which is the **worst** structure? Which is the best?" No answers on the slides. Reference values from the textbook's filled table (TB PDF p.210), [VERIFICATION] RDKit and Python, in N, N, O order: A 0, +1, −1; B −1, +1, 0; C −2, +1, +1, each summing to 0. Best: A (A and B tie on rule 2; A has the −1 on O, the more electronegative atom: rule 3, as the textbook argues on TB PDF p.210). Worst: C (a −2, and +1 on O).
- [SUPPORTED EMPHASIS] Top Hat, prepared but not asked: "We didn't have time for this one, but it's a GREAT practice question. Choose the **best** Lewis structure for phosphoric acid." (Day 9 p.26; 400-dpi crops). Five structures: (1) a P=O to an OH oxygen, with the top O single-bonded and three lone pairs; (2) four P–O single bonds; (3) one P=O to the terminal O and three P–O–H; (4) an H bonded directly to P; (5) an H bonded to both P and O. No answer on the slide. Reference answer: (3). [VERIFICATION, RDKit and Python: H₃PO₄ has 32 valence electrons. (3) has 32, every formal charge 0, and 10 electrons on P (an expanded octet, which row-3 P may have, Day 9 p.29). (2) has 32 and all octets, but P +1 and the terminal O −1. (1) has 32 but O +1 and another O −1. (4) and (5) draw 34 electrons, and (5) gives H four electrons.]
- [SOURCE-DERIVED] NO₂ (Day 9 p.28) and SO₄²⁻ (Day 9 p.30) carry red formal charges; see **Exceptions to the Octet Rule**.
- [SOURCE-DERIVED] The Day 9 p.25 Top Hat question is not in the PDF; only the FC equation is on the slide.

### Recognition cues
- [INFERRED] "Which Lewis structure is best (most important)?", "assign formal charges", or several valid structures that differ in atom order or bond placement → formal charge, then the four rules.

### Common mistakes flagged
- [INFERRED] Giving each atom both electrons of every bond (that is the octet count, not the formal charge); treating formal charge as the real charge or as an oxidation number; skipping rule 4's sum check; preferring a structure whose negative charge sits on the less electronegative atom (N₂O structure B).
- [SOURCE-DERIVED] The best structure is still not the real one: "the answer is 'none of them'" (Day 9 p.21). [CLARIFICATION: the textbook says the real N–N bond lies between structures A and B (TB PDF p.210).]

### Connections
- Builds on: Lewis structures; resonance (the Day 9 p.24 table calls the N₂O structures resonance structures); electronegativity (rule 3). Used later in: expanded octets, which make formal charges "closer to zero" (Day 9 p.29–30).

### Uncertainties and discrepancies
- [CLARIFICATION] Same method as the textbook's three criteria (TB PDF p.210). Rule 2 drops the textbook's clause "or if the structure is that of a polyatomic ion"; the slide's rule 4 (FCs sum to the charge) is stated in the textbook's text rather than in its list.
- [INFERRED] Day 9 p.21 calls the three N₂O structures "not equivalent", and the p.24 table calls them "resonance structures"; by the p.8 definition (interconvertible "by just moving electrons") they are, so non-equivalent structures can also be resonance structures, contributing unequally.

## Exceptions to the Octet Rule

**Sources:** Day 9 p.27–30 (announced on Day 8 p.26)
**Unit / lecture order:** Day 9, the end of the deck and of the Ch. 4 lectures
**Prerequisites:** Lewis structures; bonding capacity; formal charge; electronegativity
**Emphasis evidence:** §4.8 bold (Day 9 p.4); the title on three slides (p.27–29); "**odd number**", "**unpaired**", "**expanded octets**", "**hypervalency**" bold (p.28–29); announced on Day 8: "Sometimes it is **impossible** for every atom to have an octet" (Day 8 p.26).

### Definitions and terminology
- [SOURCE-DERIVED] "Not all atoms have a complete octet when forming covalent bonds. •H forms duets. •Be, B, and Al form *electron-deficient* molecules." (Day 9 p.27)
- [SOURCE-DERIVED] "Some species have an **odd number** of electrons, which forces some of them to be **unpaired.** These species are called "radicals" or "free radicals," and they are very reactive." (Day 9 p.28)
- [SOURCE-DERIVED] "Atoms of nonmetals in the third row and below can have **expanded octets**. Examples: PCl₅, SF₆ , SO₄²⁻. This is called **hypervalency**, and it is not well understood. Atoms will expand their octet when they bond with strongly electronegative elements (F, O, and Cl). An expanded shell produces a structure whose atoms' formal charges are closer to zero." (Day 9 p.29)

### Three representations
- Symbolic: [SOURCE-DERIVED] Cl–Be–Cl (4 electrons on Be), BCl₃ and AlCl₃ (6 on B and Al), each Cl with three lone pairs (Day 9 p.27); NO with an unpaired dot on N (p.28); NO₂'s two structures with formal charges and ↔ (p.28); [SO₄]²⁻ in square brackets with the charge outside (p.30); PCl₅ and SF₆ with three lone pairs on every halogen (p.30).
- Particulate: [INFERRED] an odd electron count leaves one electron without a partner, which is why radicals react so readily. Free radicals return on the Day 11 Representation Matters slide (Rebecca Gerschman: "free radicals cause cell death and aging", Day 11 p.3).
- Macroscopic: [CLARIFICATION] NO and NO₂ come from car exhaust and drive photochemical smog (TB PDF p.212).

### Worked examples
- (Day 9 p.28) NO: N=O; N carries one lone pair and one unpaired electron (7 electrons), O two lone pairs. NO₂: O=N–O ↔ O–N=O with formal charges 0, +1, −1 in red and the odd electron on N. [VERIFICATION: NO 11 and NO₂ 17 valence electrons; RDKit gives FCs 0/0 for NO and 0/+1/−1 for NO₂, one radical electron each.]
- (Day 9 p.30) SO₄²⁻: with four S–O single bonds every atom has an octet, but S is +2 and each O −1. Two red curved arrows turn two O lone pairs into S=O bonds (→): S 0, the two double-bonded O 0, the two single-bonded O −1, sum −2 (the ion's charge), and S now has 12 electrons. [VERIFICATION: 32 valence electrons; RDKit FCs S +2 / O −1 ×4 vs. S 0 / O 0, 0, −1, −1.]
- (Day 9 p.30) PCl₅ (10 electrons on P) and SF₆ (12 on S), all formal charges 0. [VERIFICATION: 40 and 48 valence electrons (`tools/chemistry_verify.py electrons`).]

### Recognition cues
- [INFERRED] Be, B, or Al as the central atom → may stop short of an octet. An odd valence-electron total → a radical; the odd electron goes on the atom left with fewer than eight (N in NO and NO₂). A central atom from row 3 or below bonded to F, O, or Cl, with more bonds than its bonding capacity or octet-only formal charges far from zero → expanded octet.

### Common mistakes flagged
- [INFERRED] Expanding the octet of a row-2 atom (C, N, O, F never exceed eight); forcing an octet on B with a B=F double bond; trying to give every atom in NO eight electrons.

### Connections
- Builds on: formal charge (p.29, "closer to zero"); electronegativity (F, O, Cl). Used later in: [INFERRED] the VSEPR examples BF₃ (SN 3), PF₅ (SN 5), and SF₆ (SN 6) are an electron-deficient molecule and two expanded octets (Day 10 p.10, p.12; SF₆ appears on both days); [INFERRED] unpaired electrons return with O₂'s paramagnetism (Day 11 p.27).

### Uncertainties and discrepancies
- [SOURCE-DERIVED] "hypervalency… is not well understood" (Day 9 p.29); no mechanism is taught. [CLARIFICATION: the textbook says studies show "d orbitals contribute little to the bonding" (TB PDF p.214), and its Ch. 5 explains SN > 4 without expanded octets (TB PDF p.271–273).]
- [CLARIFICATION] The textbook prefers the same two-S=O SO₄²⁻ structure by formal charge but adds that experiment suggests the real bonding averages both kinds of structure (TB PDF p.215).

---

# Unit E — Bonding Theories: Explaining Molecular Geometry (Ch. 5; Day 10 p.4 – Day 11 p.27)

Ch. 5 section bolding: Day 10 p.4 bolds §5.1–5.3; Day 11 p.4 bolds §5.3–5.5. §5.6 (Chirality) and §5.7 (MO theory) are bold on neither day. Outcomes: Day 10 p.5 bolds 1–2; Day 11 p.5 bolds 2–3; outcomes 4 (MO) and 5 (IR, greenhouse) are bold on neither. Unlike Ch. 4, the slides' Ch. 5 section numbers and titles match the supplied textbook (see `TEXTBOOK_MAP.md`).

## Molecular Shape and Biological Activity: Chiral Molecules

**Sources:** Day 10 p.3, p.6
**Unit / lecture order:** Day 10, opening Ch. 5
**Prerequisites:** Lewis structures
**Emphasis evidence:** §5.1 bold on Day 10 p.4 (plain on Day 11 p.4); "**chiral**" bold (Day 10 p.6); the Representation Matters slide bolds "**three-dimensional structure affects biological activity**" (Lloyd Noel Ferguson, Day 10 p.3). No professor outcome mentions chirality (Day 10 p.5), and §5.6 Chirality is bold on neither day.

### Definitions and terminology
- [SOURCE-DERIVED] "Molecular geometries are clearly more complicated than Lewis structures. One example is the existence of **chiral** molecules, like R(-) and S(+) carvone" (Day 10 p.6). "Chiral" is not defined on the slides. [CLARIFICATION: the textbook: "a molecule that is not superimposable on its mirror image" (TB PDF p.256).]

### Three representations
- Macroscopic: [SOURCE-DERIVED] photos of spearmint tea and caraway-seed bread (Day 10 p.6): the two carvones smell and taste different. Ferguson "studied *taste*, and how very similar molecules can produce very different tastes" (Day 10 p.3).
- Symbolic: [SOURCE-DERIVED] "(+)-Carvone (caraway)" and "(−)-Carvone (spearmint)", drawn with a hashed and a solid wedge at one ring carbon, which is circled in red in both drawings; a condensed structural formula of carvone (Day 10 p.6).
- Particulate: [INFERRED] the two molecules have the same atoms, bonds, and Lewis structure but are mirror images, so the flat Lewis structure cannot tell them apart.

### Connections
- Builds on: Lewis structures, which this slide says are not enough (Day 10 p.6–7). Used later in: [INFERRED] §5.6 Chirality and Molecular Recognition, listed but not bold (Day 10 p.4; Day 11 p.4).

### Uncertainties and discrepancies
- [UNCERTAIN] Whether chirality (identifying stereocenters, R/S or (+)/(−) labels) is examinable: one motivating slide only, §5.6 not bold, and no outcome; the textbook's Ch. 5 has a chirality outcome (LO4, TB PDF p.232) that the slides' list leaves out.
- [CLARIFICATION] R/S (configuration) and (+)/(−) (direction of optical rotation) are separate labels; the slide pairs them correctly: (R)-(−)-carvone is spearmint and (S)-(+)-carvone is caraway.

## VSEPR Theory: Steric Number and Central Atoms with No Lone Pairs

**Sources:** Day 10 p.7–13
**Unit / lecture order:** Day 10 (title "VSEPR; Polar bonds and polar molecules", Day 10 p.1)
**Prerequisites:** a valid Lewis structure (including the octet exceptions: BF₃, PF₅, SF₆)
**Emphasis evidence:** §5.2 bold (Day 10 p.4); Ch. 5 outcome 1 ("Use VSEPR theory and the concept of steric number to predict the bond angles in molecules and the shapes of molecules with one central atom") bold on Day 10 p.5; "**repulsion**", "**electron-pair geometry**", and "**molecular geometry**" bold (Day 10 p.8); named in the lecture title (Day 10 p.1).

### Definitions and terminology
- [SOURCE-DERIVED] "Valence-shell electron-pair **repulsion** theory is based on the principle that electrons have negative charge and repel one another. It assumes that pairs of electrons are arranged about central atoms in ways that minimize repulsions between the pairs. To predict molecular shape, we start with an **electron-pair geometry** which describes the relative position in three-dimensional space of all the bonding and lone pairs of electrons. From there, we can predict a **molecular geometry** which describes the relative positions of the atoms in a molecule. To predict molecular geometry, you must know electron-pair geometry… and to know the electron-pair geometry, you must have a valid Lewis structure!" (Day 10 p.8)
- [SOURCE-DERIVED] "Steric Number: how many regions of high electron density surround the central atom / Or / In how many *directions* are there electrons?" (Day 10 p.9). The summary table calls these "Electron Domains" (Day 10 p.26), and the hybridization slides speak of "every electron domain" (Day 11 p.12, p.20). [CLARIFICATION: the textbook instead counts SN = (atoms bonded to the central atom) + (lone pairs on the central atom), Eq. 5.1 (TB PDF p.234); the counts agree, since a double or triple bond is one region and one bonded atom.]
- [SOURCE-DERIVED] "*Sometimes* Lewis structures are enough…" (Day 10 p.7): CO₂'s Lewis structure O=C=O matches its linear, 180° shape; CH₄'s flat Lewis cross does not show its real 109.5° angles (ball-and-stick models, a textbook figure).

### Equations and relationships
- [SOURCE-DERIVED] No lone pairs on the central atom (Day 10 p.9–12): SN 2 linear, 180° (CO₂) · SN 3 trigonal planar, 120° (BF₃) · SN 4 tetrahedral, 109.5° (CCl₄) · SN 5 trigonal bipyramidal, 90° and 120° (PF₅) · SN 6 octahedral, 90° (SF₆). Generic drawings label these MX₂ … MX₆ (Day 10 p.9).
- [VERIFICATION] The tetrahedral angle is arccos(−⅓) = 109.47° (Python).

### Three representations
- Symbolic: [SOURCE-DERIVED] Lewis structure → ball-and-stick model → wedge-and-dash drawing with the angle marked → polyhedron (tetrahedron, trigonal bipyramid, octahedron) (Day 10 p.10–12). [CLARIFICATION: textbook convention: a solid wedge points toward the viewer, a dashed wedge into the page, a plain line lies in the page (TB PDF p.236).]
- Particulate: [SOURCE-DERIVED] electron pairs around the central atom repel and spread as far apart as possible (Day 10 p.8).
- Macroscopic: [INFERRED] measured bond angles (180°, 120°, 109.5°) are the observable check on the model.

### Professor explanations, models, and diagrams
- [SOURCE-DERIVED] "How do double bonds affect these predictions? Double bonds consist of MORE electrons than single bonds, so they repel the other electrons more strongly. Consider formaldehyde: What would you predict the H-C-H bond angle to be? It's about 118°" (Day 10 p.13; H₂C=O Lewis structure). [INFERRED] So a double bond counts as one region for the steric number, but it squeezes the other angles below the ideal 120°.

### Worked examples
- (Day 10 p.10) CO₂ SN 2 linear; BF₃ SN 3 trigonal planar (B has 6 electrons, Day 9 p.27); CCl₄ SN 4 tetrahedral. (p.12) PF₅ SN 5 trigonal bipyramidal; SF₆ SN 6 octahedral. (p.13) Formaldehyde SN 3, H–C–H about 118°.
- [VERIFICATION] RDKit MMFF geometry: CH₄ H–C–H 109.5°, CH₂O H–C–H 115.5° (a force-field check that the angle falls below 120°, not a reference value).

### Recognition cues
- [INFERRED] "Predict the shape / bond angle / electron-pair geometry" → Lewis structure → count the regions on the central atom (each lone pair and each single, double, or triple bond is one region) → SN → geometry.

### Common mistakes flagged
- [SOURCE-DERIVED] Skipping the Lewis structure: "you must have a valid Lewis structure!" (Day 10 p.8).
- [INFERRED] Counting a double or triple bond as two or three regions; reading angles off the flat Lewis drawing (CH₄'s cross looks like 90°, Day 10 p.7).

### Connections
- Builds on: Lewis structures (Day 10 p.7–8); [INFERRED] the octet exceptions supply the SN 3, 5, and 6 examples (BF₃, PF₅, SF₆; Day 9 p.27–30). Used later in: central atoms with lone pairs (Day 10 p.14–26); the polarity of CO₂ and CF₄ (Day 10 p.29–30); hybridization, where "the number of hybridized orbitals equals the steric number" (Day 11 p.12).

### Uncertainties and discrepancies
- [CLARIFICATION] Formaldehyde's measured H–C–H angle is about 116.5°. The slide's "about 118°" (Day 10 p.13) agrees with the textbook, whose H–C=O angles "about 1° larger" than 120° imply 118° (TB PDF p.237). Both are below 120°, which is the point.

## VSEPR: Central Atoms with Lone Pairs (Electron-Pair vs. Molecular Geometry)

**Sources:** Day 10 p.14–26
**Unit / lecture order:** Day 10
**Prerequisites:** VSEPR with no lone pairs; ozone's resonance structures
**Emphasis evidence:** outcome 1 bold (Day 10 p.5); "**atoms only**" bold twice (p.14, p.16); a "Note:" warning (p.19); two Top Hat slides (p.17, p.21); a summary table built for the course (p.26).

### Definitions and terminology
- [SOURCE-DERIVED] "Remember that the molecular geometry describes relative positions of **atoms only**" (Day 10 p.14, p.16). Lone pairs are called "nonbonding pair[s]" (p.14, p.16, p.19).

### Equations and relationships
- [SOURCE-DERIVED] Summary table (Day 10 p.26, a plain professor-made table): Number of Electron Domains | Electron Pair Geometry | # of Lone Pairs | Molecular Geometry | Ideal Bond Angles. 2 Linear: 0 Linear; 180° · 3 Trigonal planar: 0 Trigonal planar, 1 Bent; 120° · 4 Tetrahedral: 0 Tetrahedral, 1 Trigonal pyramidal, 2 Bent; 109.5° · 5 Trigonal bipyramidal: 0 Trigonal bipyramidal, 1 See-saw, 2 T-shaped; "120° AND 90°" · 6 Octahedral: 0 Octahedral, 1 Square pyramidal, 2 Square planar, 3 T-shaped; 90°.

### Worked examples
- (Day 10 p.14–15) Ozone: "SN = 3 with two atoms and one nonbonding pair predicts trigonal planar arrangement… SN = 3 and two atoms predicts angular ("**bent**") molecular geometry." Figures: both resonance structures with a lone-pair lobe on the central O → "(a) Electron-pair geometry = trigonal planar" and "(b) Molecular geometry = bent"; a large lone-pair lobe pushes the two bonding-pair lobes together: "O—O—O bond angle = 117°".
- (Day 10 p.16–18) Ammonia: "SN = 4 with three atoms and one nonbonding pair predicts tetrahedral arrangement… SN = 4 and three atoms predicts **trigonal pyramidal** geometry." Figures: (a) Lewis structure → (b) tetrahedral electron-pair geometry → (c) trigonal pyramidal molecular geometry, 107° (p.18).
- (Day 10 p.19) Water: "SN = 4 with **two** atoms and **two** nonbonding pairs predicts tetrahedral arrangement. SN = 4 and two atoms predicts **bent** geometry. Note: the same geometry NAME as for ozone, but not the same bond angle!" Figure (c): "Bent (angular) molecular geometry", 104.5°.
- (Day 10 p.20–23) SN 5: "Now things get more interesting… If we replace an atom in the trigonal bipyramid with a lone pair, will it occupy an axial or an equatorial position?" (p.20; AB₅ drawn with axial B_a and equatorial B_e, 90° and 120° marked). The answer slides (p.22–23, figures only) put every lone pair in an equatorial position: one lone pair → "Seesaw molecular geometry" (after "(b) Rotated 90° about horizontal axis"); two → T-shaped; three → linear. [CLARIFICATION: the textbook's reason: an equatorial lone pair has two neighbors at 90°, an axial one would have three, and repulsion grows as the angle shrinks (TB PDF p.241).]
- (Day 10 p.24–25) SN 6: "Consider a molecule with SN = 6 but with a lone pair. Weirdly, all of the positions are now equivalent again. It doesn't matter which position we replace with the lone pair!" → square pyramidal. "But now consider a molecule with SN = 6 but with TWO lone pairs… Now things are again not equivalent!" → the two lone pairs sit opposite each other → square planar.
- [SOURCE-DERIVED] The Top Hat questions on Day 10 p.17 (after the ammonia build-up) and p.21 (after the axial-or-equatorial question) are not in the PDF.
- [VERIFICATION] RDKit MMFF geometry: NH₃ 106.0°, H₂O 104.0°, ordered as on the slides (109.5° > 107° > 104.5°). A force-field check of the trend, not reference values.

### Three representations
- Symbolic: [SOURCE-DERIVED] paired drawings, (a) electron-pair geometry with lone-pair lobes in place → (b)/(c) atoms only (Day 10 p.15–25).
- Particulate: [SOURCE-DERIVED] the lone-pair lobe is drawn larger than the bonding-pair lobes and pushes them together (Day 10 p.15). [INFERRED] So lone pairs shrink the angles: 120° → 117° (O₃); 109.5° → 107° (NH₃) → 104.5° (H₂O).
- Macroscopic: [INFERRED] the measured bond angles (117°, 107°, 104.5°) are the evidence for lone-pair repulsion.

### Recognition cues
- [INFERRED] Lone pairs on the central atom → name the electron-pair geometry from SN first, then the molecular geometry from the number of bonded atoms; the table's "ideal" angle is an upper limit, and real lone-pair angles are smaller.

### Common mistakes flagged
- [SOURCE-DERIVED] "the same geometry NAME as for ozone, but not the same bond angle!" (Day 10 p.19): bent O₃ (SN 3, about 117°) vs. bent H₂O (SN 4, 104.5°).
- [INFERRED] Giving the electron-pair geometry when the molecular geometry is asked (NH₃ is trigonal pyramidal, not tetrahedral); putting an SN 5 lone pair axial; putting two SN 6 lone pairs at 90° instead of opposite each other.

### Connections
- Builds on: VSEPR without lone pairs (Day 10 p.9–13); ozone's resonance structures (Day 10 p.14–15). Used later in: polarity of bent H₂O (Day 10 p.31) and NH₃ (Day 11 p.8); sp³ hybrids holding the lone pairs of NH₃ and H₂O (Day 11 p.16).

### Uncertainties and discrepancies
- [SOURCE-DERIVED] The Day 10 p.26 table leaves out SN 5 with three lone pairs (linear), which p.23 shows, and includes SN 6 with three lone pairs (T-shaped), which no figure shows, so "T-shaped" appears twice. [CLARIFICATION: both are standard VSEPR results (AX₂E₃ linear, e.g. XeF₂; AX₃E₃ T-shaped). The textbook's Table 5.1 lists XeF₂ as linear and says of SN 6 with 3 or 4 lone pairs, "Although these geometries are possible, we will not encounter any molecules with them" (TB PDF p.240).] → COURSE.md Discrepancies.
- [SOURCE-DERIVED] Spelling: "See-saw" in the table (p.26), "Seesaw" in the figure caption (p.22; also the textbook's spelling, TB PDF p.240–241).
- [SOURCE-DERIVED] Resolves the Day 8 p.23 hidden callout ("We'll see later that ammonia is tetrahedral"): tetrahedral is ammonia's electron-pair geometry; its molecular geometry is trigonal pyramidal (Day 10 p.16–18). → COURSE.md Discrepancies updated.
- [CLARIFICATION] The table's angle column gives the ideal (electron-pair) angles for every row: 109.5° for bent water although water's angle is 104.5° (p.19). The textbook's Table 5.1 writes "<109.5°" for those rows (TB PDF p.240).

## Polar Molecules: Bond Dipoles and Molecular Dipole Moments

**Sources:** Day 10 p.27–31; Day 11 p.6–8
**Unit / lecture order:** end of Day 10, continued at the start of Day 11 (titles "VSEPR; Polar bonds and polar molecules", Day 10 p.1, and "Polar bonds and polar molecules; Valence bond theory and hybrid orbitals", Day 11 p.1)
**Prerequisites:** electronegativity and bond polarity (Δχ); VSEPR molecular geometries
**Emphasis evidence:** §5.3 bold on both days (Day 10 p.4; Day 11 p.4); outcome 2 ("Predict whether a substance is polar or nonpolar on the basis of its molecular structure") bold on both days (Day 10 p.5; Day 11 p.5); in two lecture titles; the H₂O slide shown in two lectures (Day 10 p.31; Day 11 p.6); "**molecule**" and "**not**" bold (Day 10 p.29–31).

### Definitions and terminology
- [SOURCE-DERIVED] CO₂: "Each BOND in CO₂ is polar (Δχ = 1.0) But the two dipole moments are perfectly opposed. The **molecule** is nonpolar!" (Day 10 p.29). CF₄: "Each BOND in CF₄ is polar (Δχ = 1.5!) But all four dipole moments are perfectly opposed. The **molecule** is nonpolar!" (p.30). H₂O: "Each BOND in H₂O is polar (Δχ = 1.4) But the dipole moments are **not** perfectly opposed. The **molecule** is polar!" (p.31; repeated Day 11 p.6).
- [SOURCE-DERIVED] "Dipole moment" is used without a definition; the debye is the unit in Table 5.2 (Day 11 p.8). [CLARIFICATION: the textbook defines the dipole moment (μ) as "a measure of the degree to which a molecule aligns itself in an applied electric field; a quantitative expression of the polarity of a molecule", with 1 D = 3.34 × 10⁻³⁰ C·m, and gives no μ = Q × r equation (TB PDF p.244–245).]

### Equations and relationships
- [SOURCE-DERIVED] Table 5.2 "Permanent Dipole Moments of Several Polar Molecules" (Day 11 p.8; the same as the textbook's Table 5.2, TB PDF p.245): HF 1.82 D (toward F) · H₂O 1.85 D (toward O) · NH₃ 1.47 D (toward N) · CHCl₃ 1.01 D (toward the Cl atoms) · CCl₃F 0.45 D (toward F). Each structure is drawn with its bond-dipole arrows.
- [VERIFICATION] The slides' Δχ values follow from the Day 9 p.17 table: C–O 3.5 − 2.5 = 1.0; C–F 4.0 − 2.5 = 1.5; O–H 3.5 − 2.1 = 1.4 (Python).

### Three representations
- Symbolic: [SOURCE-DERIVED] a red crossed arrow on each polar bond pointing to the more electronegative atom; for H₂O, the two bond arrows combine (⇒) into one net arrow toward O (Day 10 p.29–31).
- Particulate: [SOURCE-DERIVED] electrostatic potential maps: CO₂ with the same color at both O ends, CF₄ uniform, H₂O red at O and blue-green at the H end (Day 10 p.29–31); CHCl₃ and CCl₃F (Day 11 p.7).
- Macroscopic: [CLARIFICATION] a polar molecule lines up in an electric field, which is how a dipole moment is measured (textbook Fig. 5.19, TB PDF p.244).

### Professor explanations, models, and diagrams
- [SOURCE-DERIVED] "Polar Bonds" (Day 10 p.27) repeats the Day 9 p.15 H–Cl / battery picture before the molecules.
- [SOURCE-DERIVED] CHCl₃ vs. CCl₃F (Day 11 p.7, figure only): both tetrahedral; CHCl₃ is drawn with three C–Cl dipoles and no C–H arrow; CCl₃F with three C–Cl dipoles plus a C–F dipole. Table 5.2 gives 1.01 vs. 0.45 D (Day 11 p.8). [INFERRED: the C–F dipole points away from the three Cl atoms, partly offsetting their net dipole. CLARIFICATION: the textbook treats C–H (Δχ 0.4) as essentially nonpolar, which is why no arrow is drawn (TB PDF p.245).]

### Recognition cues
- [INFERRED] "Is the molecule polar?" → Lewis structure → VSEPR shape → bond dipoles from Δχ → do they cancel by symmetry? Identical outer atoms arranged symmetrically with no lone pairs on the center (linear AX₂, trigonal planar AX₃, tetrahedral AX₄, trigonal bipyramidal AX₅, octahedral AX₆) → nonpolar even when every bond is polar. Bent or trigonal pyramidal shapes, or mixed outer atoms (CHCl₃, CCl₃F) → polar.

### Common mistakes flagged
- [SOURCE-DERIVED] Equating polar bonds with a polar molecule: CO₂ and CF₄ have polar bonds and are nonpolar (Day 10 p.29–30).
- [INFERRED] Judging polarity from a flat Lewis drawing (H₂O drawn H–O–H in a line would look nonpolar); forgetting that the lone pairs bend H₂O so its dipoles cannot cancel.

### Connections
- Builds on: Δχ and the crossed arrow (Day 9 p.15–18; repeated Day 10 p.27); VSEPR shapes (Day 10 p.9–26).

### Uncertainties and discrepancies
- [UNCERTAIN] Whether dipole-moment values or the debye must be known: only Table 5.2 (Day 11 p.8) shows them, and no equation is given on the slides or in the textbook's Ch. 5.
- [SOURCE-DERIVED] Day 11 p.7 has no visible title on the rendered slide; the text layer holds a hidden "Polar Molecules!" title.

## Valence Bond Theory: Orbital Overlap and Sigma (σ) Bonds

**Sources:** Day 11 p.9–11
**Unit / lecture order:** Day 11
**Prerequisites:** atomic orbital shapes (Day 5 p.17–20); electron configurations and orbital diagrams (Day 6); the covalent H–H energy curve (Day 8 p.11)
**Emphasis evidence:** §5.4 bold (Day 11 p.4); outcome 3 ("Use atomic hybridization and valence bond theory to explain orbital overlap, bond angles, and molecular shape") bold on Day 11 p.5; named in the lecture title (Day 11 p.1); "**Valence bond theory**", "**half-filled orbitals**", "**sigma (σ) bond:**" bold (p.9–10); "**two**", "**four**", "**looks**" bold (p.11).

### Definitions and terminology
- [SOURCE-DERIVED] "VSEPR grew out of Lewis structures, which pre-date our understanding of atomic orbitals. Can we reconcile the two ideas? **Valence bond theory** (Linus Pauling, late 1920s) suggests that covalent bonds form when **half-filled orbitals** on different atoms overlap. The electrons in overlapping orbitals are attracted to the nuclei of both bonded atoms, increasing stability. We talked about this already in the context of the H-H potential energy surface." (Day 11 p.9, beside the Day 8 p.11 H–H curve: −436 kJ/mol at **74** pm)
- [SOURCE-DERIVED] "In the new language of Valence Bond Theory, that overlap of H electron density leads to a **sigma (σ) bond:** A covalent bond in which the highest electron density lies between the two atoms along the bond axis" (Day 11 p.10; figure: H 1s + H 1s → "Overlap = σ bond").

### Professor explanations, models, and diagrams
- [SOURCE-DERIVED] The methane problem (Day 11 p.11): "But we pretty quickly run into trouble with this picture. Consider methane. Methane only has **two** unpaired electrons, so how can it make **four** sigma bonds? One suggestion is that it could promote an electron from 2s to 2p, producing four unpaired electrons. But that's not what methane **looks** like! We need four equivalent bonds pointing to the vertices of a tetrahedron!" Diagrams: carbon's ground state 1s² 2s² 2p² with two unpaired 2p electrons ("Electrons available to bond"); an excited state 2s¹ 2p³ ("Four electrons available to bond"); the four electrons drawn in a 2s sphere and the 2p_x, 2p_y, 2p_z lobes; CH₄ with "four single bonds".

### Three representations
- Particulate: [SOURCE-DERIVED] overlapping orbital lobes; σ density concentrated on the line between the nuclei (Day 11 p.10).
- Symbolic: [SOURCE-DERIVED] orbital box diagrams on an energy axis (ground vs. excited carbon, Day 11 p.11).
- Macroscopic: [INFERRED] the bond length and bond energy of H₂ (Day 8 p.11) are what the overlap picture explains.

### Recognition cues
- [INFERRED] "Which orbitals overlap to make this bond?", "is it a σ or a π bond?" → valence bond theory.

### Common mistakes flagged
- [SOURCE-DERIVED] The promoted-electron picture fails for CH₄ ("that's not what methane **looks** like!", Day 11 p.11). [INFERRED: it would give one bond from 2s and three mutually perpendicular bonds from 2p, not four equivalent tetrahedral bonds.]

### Connections
- Builds on: the H–H curve (Day 11 p.9 ↔ Day 8 p.11); orbital shapes (Day 5 p.17–20); carbon's configuration and Hund's rule (Day 6 p.16–17). Used later in: hybridization (Day 11 p.12–16).

### Uncertainties and discrepancies
- [SOURCE-DERIVED] Wording: "Methane only has two unpaired electrons" (Day 11 p.11) refers to the free carbon atom, as the slide's ground-state diagram shows; CH₄ itself has none.
- [CLARIFICATION] The textbook never introduces promotion; it mixes carbon's filled 2s and half-filled 2p orbitals directly into four half-filled sp³ orbitals (TB PDF p.247–248). The slide raises promotion only to reject it.
- [CLARIFICATION] Valence bond theory began with Heitler and London's H₂ calculation (1927) and was developed by Pauling and Slater; the slide credits Pauling, as the textbook does (TB PDF p.247). History detail.

## Hybrid Orbitals (sp³, sp², sp) and Steric Number

**Sources:** Day 11 p.12–16, p.18, p.20, p.22–25
**Unit / lecture order:** Day 11
**Prerequisites:** valence bond theory; steric number (VSEPR); orbital box diagrams
**Emphasis evidence:** outcome 3 bold (Day 11 p.5); "**hybridization:**" and "**averaging**" bold (p.12); the rules slide (p.20); Table 5.3 under the title "Hybridization Based on Steric Number" (p.24).

### Definitions and terminology
- [SOURCE-DERIVED] "Pauling got around this by suggesting the idea of **hybridization:** The mixing of atomic orbitals to generate new sets of orbitals that are then available to form covalent bonds with other atoms. Because orbitals are "just" mathematical functions, you can do anything to them that you can do to any other math function – such as **averaging** them. We will need one hybridized orbital for every electron domain. That is, the number of hybridized orbitals equals the steric number of the atom." (Day 11 p.12)
- [SOURCE-DERIVED] "Hybrid orbital theory accounts for molecular geometries and bonding. Each electron domain on the central atom requires one hybrid orbital. The number of valence atomic orbitals combined equals the number of hybrid orbitals created. σ bonds involve head-on overlap of hybrid orbitals. Exception: Hydrogen uses a 1s orbital to make bonds. π bonds always result from side-to-side overlap of unhybridized orbitals. Lone pairs always reside in hybrid orbitals." (Day 11 p.20)
- [SOURCE-DERIVED] A hybrid orbital has a "Major lobe" and a "Minor lobe"; drawings usually show only the major lobe (Day 11 p.14, figure only).

### Equations and relationships
- [SOURCE-DERIVED] Table 5.3 "Summary of Hybridization Schemes and Orbital Orientations" (Day 11 p.24): Hybridization | Orientation of Hybrid Orbitals | Number of σ Bonds | Molecular Geometries | Angles between Hybrid Orbitals: sp — 2 — Linear — 180° · sp² — 3, 2 — Trigonal planar, Bent — 120°, <120° · sp³ — 4, 3, 2 — Tetrahedral, "Trigonal planar" [sic], Bent — 109.5°, <109.5°, <109.5°. The drawings show two sp lobes with two unhybridized p orbitals, three sp² lobes with one p, and four sp³ lobes.
- [INFERRED from Day 11 p.12, p.24] SN 2 → sp, SN 3 → sp², SN 4 → sp³. The number of hybrids equals SN and equals the number of atomic orbitals mixed (s + p; s + 2p; s + 3p). The slides don't spell out the superscript rule.

### Worked examples
- (Day 11 p.13–15) CH₄: carbon's 2s [↑↓] and 2p [↑][↑][ ] "Hybridize" into four sp³ [↑][↑][↑][↑]: "The C in methane has a steric number of 4, so we want 4 hybridized orbitals." The four sp³ lobes, 109.5° apart, each overlap one H 1s.
- (Day 11 p.16) NH₃: N 2s [↑↓] 2p [↑][↑][↑] → sp³ [↑↓][↑][↑][↑]; the filled sp³ holds the lone pair and three half-filled sp³ overlap H 1s. H₂O: O 2s [↑↓] 2p [↑↓][↑][↑] → sp³ [↑↓][↑↓][↑][↑]; two lone-pair sp³ lobes and two O–H σ bonds.
- (Day 11 p.18, p.22–23) sp² C and O in formaldehyde, sp² N in diazene, sp C in acetylene; see **Pi (π) Bonds**.
- [VERIFICATION] RDKit hybridization: CH₄ C sp³; NH₃ N sp³; H₂O O sp³; CH₂O C sp², O sp²; N₂H₂ N sp²; C₂H₂ C sp; C₂H₄ C sp²; CO₂ C sp. Each box diagram conserves the atom's valence electrons (C 4, N 5, O 6).

### Recognition cues
- [INFERRED] "What is the hybridization of the central atom?" → Lewis structure → SN → sp, sp², or sp³; "which orbital holds the lone pair?" → a hybrid orbital (Day 11 p.20).

### Common mistakes flagged
- [INFERRED] Using the number of bonded atoms instead of SN (NH₃ has three atoms but SN 4, sp³); hybridizing H (it uses 1s, Day 11 p.20); counting a π bond as needing a hybrid orbital.

### Connections
- Builds on: steric number (Day 10 p.9; "the number of hybridized orbitals equals the steric number", Day 11 p.12); the methane problem (Day 11 p.11). Used later in: π bonds (Day 11 p.17–26).

### Uncertainties and discrepancies
- [SOURCE-DERIVED] Table 5.3's sp³ row (Day 11 p.24, 400-dpi crop) labels the 3-σ-bond geometry "Trigonal planar". The supplied textbook's Table 5.3 says "Trigonal pyramidal" (TB PDF p.252), as do the professor's own slides (Day 10 p.18, p.26), and an sp³ atom with three bonds and a lone pair (NH₃, 107°) is trigonal pyramidal. The slide's table also differs from the supplied book's in layout (no Steric Number column; "<120°" and "<109.5°" entries), so it probably comes from another edition. → COURSE.md Discrepancies.
- [SOURCE-DERIVED] No hybridization is given for SN 5 or 6: Table 5.3 stops at sp³, although PCl₅, PF₅, and SF₆ appear on Day 9 p.29–30 and Day 10 p.12. [CLARIFICATION: the textbook also stops at sp³ and explicitly sets aside the d-orbital (sp³d, sp³d²) explanation, treating SN > 4 with sp² + p or sp + 2p hybrids and three-center bonds of bond order ½ (TB PDF p.271–273).]
- [INFERRED] The hybridization diagrams go straight from the ground-state boxes to the hybrids, with no promotion step (Day 11 p.13, p.18, p.23), consistent with p.11's rejection of promotion.

## Pi (π) Bonds: Double and Triple Bonds and Molecules with Multiple "Central" Atoms

**Sources:** Day 11 p.17–19, p.21–23, p.25–26
**Unit / lecture order:** Day 11
**Prerequisites:** hybrid orbitals; σ bonds; double and triple bonds in Lewis structures (Day 8 p.20, p.25)
**Emphasis evidence:** §5.5 "Molecules with Multiple 'Central' Atoms" bold (Day 11 p.4); outcome 3 bold (Day 11 p.5); a Top Hat slide (p.21).

### Definitions and terminology
- [SOURCE-DERIVED] "Pauling was also able to explain those mysterious double bonds in our Lewis structures. Each double bond consists of a sigma bond AND a pi (π) bond: A covalent bond in which electron density is greatest above and below the bonding axis. To illustrate, let's look at formaldehyde." (Day 11 p.17)
- [SOURCE-DERIVED] "π bonds always result from side-to-side overlap of unhybridized orbitals" (Day 11 p.20).

### Worked examples
- (Day 11 p.18–19) Formaldehyde, H₂C=O: C is sp² (three sp² [↑][↑][↑] + one unhybridized p [↑]); O is sp² (three sp² [↑↓][↑↓][↑] + one p [↑]). σ bonds: two H 1s–C sp² and one C sp²–O sp²; π: the side-by-side C p–O p overlap above and below the molecular plane; O's lone pairs in its two other sp² orbitals. The Lewis structure is color-coded: σ bonds green (both C–H and one line of C=O), the π bond blue (the second line of C=O).
- (Day 11 p.22) Diazene, N₂H₂: each N is sp² (one sp² holding a lone pair, two bonding sp², one p); σ H 1s–N sp² and N sp²–N sp²; π from p–p. Lewis structure H–N=N–H, the H atoms on opposite sides (trans), one lone pair on each N.
- (Day 11 p.23) Acetylene, C₂H₂: each C is sp ("Two sp hybrid orbitals" + "Two unhybridized p orbitals"); σ H 1s–C sp and C sp–C sp; "π bond (1)" and "π bond (2)" at right angles; H–C≡C–H. A triple bond is one σ + two π.
- (Day 11 p.25, figure only) Ethylene, H₂C=CH₂: "Trigonal planar" at each C; the σ framework (C sp²–C sp² and H 1s–C sp²) and one π bond above and below the plane.
- (Day 11 p.26, figure only) Acrolein CH₂=CH–CH=O; benzene's two Kekulé structures (↔) beside its delocalized π cloud above and below the ring; naphthalene, phenanthrene, anthracene, and benzo[a]pyrene.
- [SOURCE-DERIVED] The Top Hat question on Day 11 p.21 is not in the PDF.
- [VERIFICATION] RDKit σ/π counts: CH₂O 3 σ + 1 π; N₂H₂ 3 σ + 1 π; C₂H₂ 3 σ + 2 π; C₂H₄ 5 σ + 1 π; CO₂ 2 σ + 2 π.

### Three representations
- Particulate: [SOURCE-DERIVED] σ density on the bond axis (head-on overlap) vs. π density above and below it (side-by-side p overlap) (Day 11 p.17, p.19, p.23).
- Symbolic: [SOURCE-DERIVED] bond lines color-coded σ (green) and π (blue) (Day 11 p.19, p.23).
- Macroscopic: [CLARIFICATION] multiple bonds are shorter and stronger (Table 4.6, Day 9 p.14); the σ + π picture is the usual explanation.

### Recognition cues
- [INFERRED] Count bonds: every single bond is σ; a double bond is 1 σ + 1 π; a triple bond 1 σ + 2 π. An atom with one double bond is sp² (SN 3); one with a triple bond or two double bonds is sp (SN 2). With several interior ("central") atoms, find SN and hybridization for each in turn.

### Common mistakes flagged
- [INFERRED] Counting a double bond as two σ bonds; hybridizing the p orbital that forms the π bond; forgetting that diazene's lone pairs sit in sp² orbitals ("Lone pairs always reside in hybrid orbitals", Day 11 p.20).

### Connections
- Builds on: Lewis double and triple bonds (Day 8 p.20, p.25); hybridization (Day 11 p.12–16); formaldehyde's VSEPR angle (Day 10 p.13). Used later in: benzene's delocalized π electrons, the orbital picture of its resonance (Day 11 p.26 ↔ Day 9 p.12–13).

### Uncertainties and discrepancies
- [UNCERTAIN] Ethylene, acrolein, benzene, and the polycyclic aromatics (Day 11 p.25–26) are figures without text; what students should take from p.26 (delocalization? planarity?) is not stated. [CLARIFICATION: the textbook uses them for conjugation, delocalized π electrons, and aromatic compounds (TB PDF p.253–255).]

## Molecular Orbital Theory: O₂ Paramagnetism, Bond Order, HOMO and LUMO

**Sources:** Day 11 p.27; Day 12 p.4–13
**Unit / lecture order:** announced on the last slide of Day 11; taught on Day 12 p.6–13, just before Ch. 18
**Emphasis evidence:** "*paramagnetic*" italic and "ALL fail" in capitals (Day 11 p.27, repeated as Day 12 p.6). On Day 12, **§5.7 Molecular Orbital Theory is bold** in the Ch. 5 list while §5.6 Chirality is grey (p.4), and **outcome 4 is bold** (p.5): "Draw molecular orbital (MO) diagrams of small molecules and use MO theory to predict bond order and explain the magnetic properties and UV/visible spectra of molecular compounds". O₂'s two π*₂p electrons are circled in red on Fig. 5.50 (p.11). (On Day 10–11, §5.7 and outcome 4 were bold on neither day.)

### Definitions and terminology
- [SOURCE-DERIVED] "But wait, there's more! Diatomic oxygen (O₂) is *paramagnetic* – it is attracted to a magnetic field. Only molecules with unpaired electrons are paramagnetic. Lewis structures, VSEPR, and valence bond/hybridization theories ALL fail to predict this. So let's talk briefly about Molecular Orbital Theory" (Day 11 p.27; repeated as Day 12 p.6). Photo: liquid O₂ held between the poles of a magnet.
- [SOURCE-DERIVED] "MO Theory takes the “scrambling” effect of valence bond/hybridization theory to the extreme: Let's take ALL the valence atomic orbitals from the individual atoms and redistribute them over the entire molecule! Just as with hybridization, we'll get one molecular orbital out for every atomic orbital that we put in. Let's start with the simplest of molecules, H2, and see how this works." (Day 12 p.7)
- [SOURCE-DERIVED] "HOMO: Highest Occupied Molecular Orbital"; "LUMO: Lowest Unoccupied Molecular Orbital" (Day 12 p.11).
- [SOURCE-DERIVED] The slides never use the word "diamagnetic"; the textbook defines it (TB PDF p.266).

### Equations and relationships
- [SOURCE-DERIVED] "Bond order = ½ [(number of bonding e⁻) – (number of antibonding e⁻)]" (Day 12 p.8, p.9); the textbook's Eq. 5.2 (TB PDF p.262).

### Worked examples and figures
- [SOURCE-DERIVED] H₂ (the textbook's Fig. 5.45): H 1s (↑) + H 1s (↓) → σ1s (↑↓, boxed in red, lower) and σ*1s (empty, higher), with dotted correlation lines; the σ1s picture is one oval of density spanning both nuclei, and σ*1s has two lobes with a "Node" between them (Day 12 p.8).
- [SOURCE-DERIVED] H₂ (σ1s)², H₂⁻ (σ1s)²(σ*1s)¹, and He₂ (σ1s)²(σ*1s)² drawn side by side with the bond-order formula (Day 12 p.9). The bond orders are not printed. [VERIFICATION] ½(2 − 0) = 1, ½(2 − 1) = ½, ½(2 − 2) = 0 (Python, the same filling the guide's `problem_bank_k.py` uses).
- [SOURCE-DERIVED] 2p combinations (the textbook's Fig. 5.48): 2pz + 2pz along the bond axis → σ2p (density between the nuclei) and σ*2p (a node); 2px and 2py side by side → two π2p and two π*2p (Day 12 p.10).
- [SOURCE-DERIVED] The textbook's Fig. 5.50 (Day 12 p.11). Li₂–N₂, bottom to top: σ2s, σ*2s, π2p, σ2p, π*2p, σ*2p (π2p and σ2p labels in blue). O₂–Ne₂: σ2s, σ*2s, σ2p, π2p, π*2p, σ*2p. Bond orders printed: Li₂ 1, Be₂ 0, B₂ 1, C₂ 2, N₂ 3, O₂ 2, F₂ 1, Ne₂ 0. B₂ shows one electron in each π2p orbital and O₂ one in each π*2p orbital (circled in red). [VERIFICATION] all eight bond orders and the unpaired counts (B₂ 2, O₂ 2, the rest 0) re-derived by filling (`ch5_data.mo_ref`).
- [SOURCE-DERIVED] "Top Hat Time!" (Day 12 p.12): the question is not in the PDF.
- [SOURCE-DERIVED] "Theories of Bonding" (Day 12 p.13): "In Chapters 4 and 5 we have encountered several theories of bonding. Each has its own strengths and characteristics. Which to use depends upon the questions asked. Do we want to know about connectivity? Lewis structures are fine. Do we want to know about 3-D shape? VSEPR or VBT should work. Do we want to know about magnetic or spectroscopic properties? We're going to need to use MO".

### Recognition cues
- [INFERRED] "paramagnetic", "attracted to a magnet", "unpaired electrons", "bond order" of a diatomic or its ion, "HOMO/LUMO" → fill an MO diagram. Connectivity → Lewis; 3-D shape → VSEPR or VBT; magnetism or spectra → MO (Day 12 p.13).

### Connections
- Builds on: [INFERRED] O₂'s Lewis structure, O=O with every electron paired (Day 8 p.20), which is why Lewis theory "fails"; unpaired electrons in radicals (Day 9 p.28) and Hund's rule (Day 6 p.16). [SOURCE-DERIVED] the "scrambling" of hybridization and "one … orbital out for every atomic orbital … put in" (Day 12 p.7, recalling Day 11 p.12).
- Used later in: [SOURCE-DERIVED] band theory, which starts from the MO diagrams of Na₂ and Na₄ and their HOMO–LUMO gap (Day 12 p.19–21; see Band Theory below).

### Uncertainties and discrepancies
- [UNCERTAIN] Whether MO theory is on Midterm 1 ("THURSDAY!", Day 12 p.2): the slides don't list exam topics. It was taught three days before the exam [INFERRED from the dates].
- [UNCERTAIN] The Day 12 p.12 Top Hat question (not in the PDF).
- [SOURCE-DERIVED] The slides show the two orders by molecule (Fig. 5.50) and never state a rule such as "Z ≤ 7"; the textbook gives the reason (2s–2p mixing, TB PDF p.266). Heteronuclear diatomics (NO, Fig. 5.52), the auroras, and ozone's π system are textbook only (TB PDF p.268–271).

---

# Unit F — The Solid State (Ch. 18, §18.4–18.5 only; Day 12 p.14–25)

**Emphasis evidence (unit):** the Ch. 18 list on Day 12 p.14 bolds only **§18.4 Metallic Bonds and Conduction Bands** and **§18.5 Semiconductors**; §18.1–18.3 and §18.6–18.9 are plain. Outcome 3 is the only bold outcome (Day 12 p.15): "**Use band theory to explain the conductivity of metals and semiconductors**". Outcomes 1 (unit-cell dimensions vs. radii), 2 (densities), and 4 (classes of solids) are plain.

## Metals, Metalloids, and Nonmetals: Properties of Metals

**Sources:** Day 12 p.14–17
**Unit / lecture order:** opens the Ch. 18 part of Day 12, after "Theories of Bonding" (p.13)
**Emphasis evidence:** "Malleable", "Ductile", and "Heat and electricity conductors" are bold on p.17.

### Definitions and terminology
- [SOURCE-DERIVED] A periodic table colored by class, with no text: metals (tan), metalloids (green: B, Si, Ge, As, Sb, Te, At), nonmetals (blue) (Day 12 p.16).
- [SOURCE-DERIVED] "Metals versus Nonmetals. Metals share the following characteristics: • **Malleable: can be formed into thin sheets** • **Ductile: can be pulled into thin wires** • Lustrous: have a shiny appearance • **Heat and electricity conductors** • Relatively large densities • Relatively high melting and boiling points • All are solids at room temperature except mercury, Hg • Tend to form cations • Very few colors: grey, silver, gold/copper" (Day 12 p.17; photo "Copper wiring").
- [SOURCE-DERIVED] Textbook: malleability is "the ability to be shaped", ductility "the ability to be drawn out"; "One reason that metals have both malleability and ductility … is that the bonds between atoms in a solid are weak" (TB PDF p.918). Metalloids are a "staircase" of elements "that tend to have the physical properties of metals and the chemical properties of nonmetals"; they conduct worse than metals but better than nonmetals (TB PDF p.920).

### Connections
- Builds on: [SOURCE-DERIVED] the Ch. 4 electron sea, which "begins to account for the conductivity of metals, but that's all we'll say here in Chapter 4" (Day 8 p.14); metallic bonds, "shared electrons which are highly mobile" (Day 7 p.14). [INFERRED] "Tend to form cations" ↔ low ionization energies (Day 7 p.9–10).
- Used later in: band theory (p.18–24) and semiconductors (p.18 "And then there are the metalloids…").

## Band Theory: Conductors and Insulators

**Sources:** Day 12 p.18–24; textbook §18.4 (TB PDF p.918–920)
**Unit / lecture order:** Day 12 p.18 (the rule), p.19–23 (building bands from MO diagrams), p.24 (the professor's band sketch)
**Emphasis evidence:** "**large enough band gap**" bold (p.18). The conductor rule appears three times: on p.18, and in boxes beside the Na_N (p.22) and Zn_N (p.23) figures, with the clause that applies to each figure in black and the other in grey. Outcome 3 bold (p.15).

### Definitions and terminology
- [SOURCE-DERIVED] "Insulators vs. Conductors. Any material with a partially filled valence band or a filled valence band that overlaps with an empty conduction band is an electrical conductor. Any material with a **large enough band gap** acts as an insulator. And then there are the metalloids…" (Day 12 p.18). The slide defines neither "band" nor "band gap" in words.
- [SOURCE-DERIVED] Textbook margin definitions (TB PDF p.920–921): band theory "an extension of molecular orbital theory that describes bonding in solids"; valence band "a band of orbitals that are filled or partially filled by valence electrons"; conduction band "an unoccupied band higher in energy than a valence band in which electrons can migrate"; conductor "a material with partially filled valence bands or filled valence bands that overlap with empty conduction bands, leading to highly mobile electrons"; band gap (E_g) "the energy gap between the valence and conduction bands"; insulator "a material with a large energy gap between its valence and conduction bands".

### Worked examples and figures
- [SOURCE-DERIVED] "MO Theory: Na2" (p.19–20): Na 3s (↑) with the empty 3p (grey, dashed) above; Na₂ has one filled MO (↑↓) below the 3s level and one empty MO above it. p.20 circles both in red and adds a red double arrow, "HOMO-LUMO Gap".
- [SOURCE-DERIVED] "MO Theory: Na4" (p.21): "As we add more and more atoms (and electrons) to the MO diagram, the HOMO-LUMO gap gets smaller *quickly*" / "Pretty soon, the words “HOMO” and “LUMO” begin to become meaningless." Na₄ has four MOs from the 3s orbitals, two filled and two empty, with HOMO and LUMO circled and a smaller red gap arrow; the 3p levels split above (grey).
- [SOURCE-DERIVED] Na → Na₂ → Na₄ → Na_N (the textbook's Fig. 18.25, Day 12 p.22): the 3s levels merge into a band whose lower half is occupied (purple) and upper half empty (salmon), overlapping the empty 3p band (grey); "Valence band (partially filled)". Box: "Any material with a partially filled valence band [black] or a filled valence band that overlaps with an empty conduction band [grey] is an electrical conductor."
- [SOURCE-DERIVED] Zn → Zn_N (the textbook's Fig. 18.26, Day 12 p.23): the 4s band is filled ("Valence band (filled)"), the 4p band empty ("Conduction band (empty)"), and the two "Overlap". The box shows the overlap clause in black.
- [SOURCE-DERIVED] The professor's band sketch (p.24), energy axis "E" pointing up, filled band shading in blue: "Insulator (diamond)": a filled band, a large gap, an empty band. "Conductor (zinc)": a filled band touching an empty band. "Conductor (sodium)": a band filled in its lower part only, touching an empty band above. "Semiconductor (silicon)": a filled band and a small gap below an empty band. "T ↑": the same semiconductor with a strip of electrons at the bottom of the upper band and an empty strip at the top of the lower band.
- [SOURCE-DERIVED] Textbook §18.4 (TB PDF p.918–919): in solid Na (body-centered cubic) each atom bonds to eight neighbors, so "sharing a limited number of valence electrons with many bonding partners makes the bond linking any two metal atoms relatively weak", which is why sodium can be cut with a knife; Na₂'s 3s orbitals give two MOs "above and below the initial value"; for a piece of solid Na "an equally enormous number of molecular orbitals" forms "a continuous band of energies with no gap between the occupied lower half and the empty upper half"; Zn's filled 4s band overlaps the empty 4p conduction band; "the two views of valence bands … are not mutually exclusive" (Zn's 4s and 4p can be treated as one partially filled band).
- [SOURCE-DERIVED] Textbook Concept Test: "Use band theory to explain the electrical conductivity of magnesium metal" (TB PDF p.920); not in the lecture.

### Recognition cues
- [INFERRED] "conductor", "insulator", "band gap", "valence/conduction band", "why does a metal conduct" → band theory. One valence s electron per atom (Na) → a partially filled band; a filled valence s subshell (Zn) → conducts only because an empty band overlaps it.

### Connections
- Builds on: [SOURCE-DERIVED] MO theory: Day 12 p.19–21 title the band slides "MO Theory: Na2" and "MO Theory: Na4"; the textbook calls band theory "an extension of molecular orbital theory" (TB PDF p.918). [SOURCE-DERIVED] The textbook links back to the electron sea ("In Chapter 4, we described metal atoms “floating” in seas of mobile bonding electrons … a more sophisticated approach, called band theory, better explains", TB PDF p.918) ↔ Day 8 p.14. [SOURCE-DERIVED, textbook] Na [Ne]3s¹ and Zn [Ar]3d¹⁰4s² decide whether the valence band is half-filled or filled (TB PDF p.918–919) ↔ electron configurations (Day 6).
- Used later in: semiconductors (Day 12 p.24–25).

### Uncertainties and discrepancies
- [UNCERTAIN] Whether Ch. 18 is on Midterm 1 (Thursday, Day 12 p.2): the slides don't list the exam's topics.
- [SOURCE-DERIVED] The textbook gives NaCl's band gap as "6.8 × 10⁵ kJ/mol" (TB PDF p.920, checked on the render). [VERIFICATION] 6.8 × 10⁵ kJ/mol ÷ 96.485 kJ mol⁻¹ eV⁻¹ ≈ 7.0 × 10³ eV per electron, an X-ray energy, far beyond any electronic band gap. [CLARIFICATION] NaCl's measured gap is about 8.5–9 eV ≈ 8 × 10² kJ/mol; the printed value is probably 6.8 × 10⁵ J/mol (= 6.8 × 10² kJ/mol). Not on the slides. Logged in COURSE.md → Discrepancies.

## Semiconductors and Doping

**Sources:** Day 12 p.18, p.24–25; textbook §18.5 (TB PDF p.920–921)
**Unit / lecture order:** the last slides of Day 12
**Emphasis evidence:** §18.5 bold (p.14); outcome 3 bold (p.15).

### Definitions and terminology
- [SOURCE-DERIVED] "And then there are the metalloids…" (p.18); "Semiconductor (silicon)": a filled band below an empty one with a small gap; "T ↑": some electrons in the upper band and vacancies in the lower one (p.24).
- [SOURCE-DERIVED] "Doping of Semiconductors" (p.25; the textbook's Fig. 18.27 without its caption): (a) Pure Si, conduction band over valence band with the gap labeled E_g, Lewis symbol ·Si· (4 dots); (b) n-type, a "Phosphorus donor level" just below the conduction band, ·Si· + ·P· (5 dots); (c) p-type, a "Gallium acceptor level" just above the valence band, with ⊕ marks along the top of the valence band, ·Si· + ·Ga· (3 dots).
- [SOURCE-DERIVED] Textbook (TB PDF p.920–921): semiconductor "a material with electrical conductivity between that of metals and insulators that can be chemically altered to increase its electrical conductivity"; in metalloids the bands "do not overlap but instead are separated by an energy gap"; Si's band gap "106 kJ/mol at 25°C"; "only a few valence-band electrons in Si have enough energy to move to the conduction band"; doping replaces some Si atoms "with atoms of an element having a similar atomic radius but a different number of valence electrons" (the dopant); "doped semiconductors represent substitutional alloys"; P's extra electrons occupy a donor level "only about 4 kJ/mol below the Si conduction band" → n-type, "because the dopant donates negative charges (electrons)"; Ga makes an acceptor level "about 7 kJ/mol above the Si valence band", and valence electrons that move into it leave "positively charged “holes”" (⊕) → p-type; n-type semiconductor "containing an electron-rich dopant", p-type "an electron-poor dopant"; devices combine n- and p-type.
- [SOURCE-DERIVED] Textbook-only extras on TB PDF p.921 (before the §18.6 heading): group 13–15 alloys such as GaAs (same average of 4 valence electrons per atom, larger band gaps; IR emission at 874 nm), AlGaAs₂ at 620 nm, LEDs (blue from InₓGa₁₋ₓN and GaN), CdS and CdSe; Concept Test: "Which element, Se or Sn, would form an n-type semiconductor with GaAs?" Not in the lecture.

### Recognition cues
- [INFERRED] A dopant with one more valence electron than the host (group 15 in Si) → n-type, donor level just below the conduction band; one fewer (group 13 in Si) → p-type, acceptor level just above the valence band, holes. "Heated semiconductor" → more electrons across the gap (p.24).

### Connections
- Builds on: [SOURCE-DERIVED] Lewis symbols, drawn on p.25 to count the dopants' valence electrons (↔ Day 8 p.16–17); the metalloids on the p.16 periodic table; the band gap (p.18).
- [INFERRED] Thermal promotion across a gap ↔ the energy needed to move an electron to a higher level (Day 4 p.10; Day 12 p.24).

### Uncertainties and discrepancies
- [SOURCE-DERIVED] The slides give no energies; 106, 4, and 7 kJ/mol are the textbook's (TB PDF p.920). [CLARIFICATION] 106 kJ/mol ≈ 1.10 eV per electron; the usual room-temperature value for Si is 1.12 eV ≈ 108 kJ/mol (agreement within 2%).
- [UNCERTAIN] What the ⊕ marks mean is not said on the slide (p.25); the textbook's caption calls them "positively charged holes" (TB PDF p.920).

---

## Source coverage log

One line per processed source: what it covered and which concepts it touched.

| Source | Pages processed | Concepts touched | Date |
|---|---|---|---|
| `lectures/Day 1 Lecture Slides.pdf` | 1–20 of 20 (p.19–20 image-only; p.1–5 course policy) | Before Atomic Theory (laws); Dalton's Atomic Theory; Conservation of Energy and Mass–Energy; Listed but Not Lectured; Discovery of the Subatomic (CRT intro) | 2026-09-24 |
| `lectures/Day 2 Lecture Slides.pdf` | 1–31 of 31 (p.6–8, 13, 16–18, 20, 29 image-only) | Discovery of the Subatomic; The Nuclear Atom; RAMP UP Content; EM Radiation; Atomic Spectra | 2026-09-24 |
| `lectures/Day 3 Lecture Slides.pdf` | 1–21 of 21 | Atomic Spectra; Blackbody Radiation and Planck; Photoelectric Effect; Balmer and Rydberg; Conservation of Mass–Energy (p.2 transmutation) | 2026-09-24 |
| `lectures/Day 4 Lecture Slides.pdf` | 1–18 of 18 (p.9 image-only) | Balmer and Rydberg; Bohr Model; de Broglie; Schrödinger | 2026-09-24 |
| `lectures/Day 5 Lecture Slides.pdf` | 1–20 of 20 | Schrödinger and Wavefunctions; Quantum Numbers; Pauli; Sizes and Shapes of Orbitals | 2026-09-24 |
| `lectures/Day 6 Lecture Slides.pdf` | 1–26 of 26 (p.17, 20 image-only) | Electron Configurations; Penetration/Shielding/Z_eff; Hund's Rule; Filling Order; Configurations of Ions; Atomic Radius | 2026-09-24 |
| `lectures/Day 7 Lecture Slides.pdf` | 1–21 of 21 (p.10 image-only; p.15 text layer garbled) | Filling Exceptions; Atomic Radius; Ionic Radius; Ionization Energy; Electron Affinity; Types of Bonds; Coulombic Potential Energy; Lattice Energy; Ionic Formulas; Naming Binary Ionic Compounds | 2026-09-24 |
| `lectures/Day 8 Lecture Slides.pdf` | 1–30 of 30 (p.11, 15, 27 image-only; p.23 has hidden text in the text layer; 400-dpi zooms of Tables 4.5 and the Lewis symbols) | Naming Binary Ionic Compounds (repeat); Transition-Metal Roman Numerals; Polyatomic Ions; Types of Bonds (H–H curve, metallic, Table 4.1); Lattice Energy (image resolved); Naming Covalent Compounds; Lewis Symbols and the Octet Rule; Lewis Structures; Allotropes | 2026-09-25 |
| `lectures/Day 9 Lecture Slides.pdf` | 1–30 of 30 (p.11, 14, 16, 20, 30 image-only; p.24 a blanked textbook table; 300–400-dpi zooms of the O₃ hybrid, the electronegativity table, and the H₃PO₄ structures) | Lewis Structures (O₃ repeat, N₂O); Resonance; Lengths and Strengths of Covalent Bonds (Table 4.6); Electronegativity and Bond Polarity; Formal Charge; Exceptions to the Octet Rule; Allotropes (O₃) | 2026-10-05 |
| `lectures/Day 10 Lecture Slides.pdf` | 1–31 of 31 (p.11 image-only; p.15, 22, 23 a title plus figures; p.17, 21 blank Top Hat slides; p.26 a professor-made table) | Molecular Shape and Biological Activity (chirality); VSEPR, no lone pairs; VSEPR with lone pairs; Electronegativity (Polar Bonds repeat); Polar Molecules; Lewis Structures (ammonia callout resolved); RAMP UP exam status | 2026-10-05 |
| `lectures/Day 11 Lecture Slides.pdf` | 1–27 of 27 (p.7 title hidden; p.14–16, 18, 19, 25, 26 image-only; p.21 a blank Top Hat slide; 400-dpi zoom of Table 5.3's sp³ row) | Polar Molecules (repeat, Table 5.2); Valence Bond Theory and σ Bonds; Hybrid Orbitals; π Bonds and Multiple Central Atoms; MO Theory (announced); Types of Bonds (H–H curve reused) | 2026-10-05 |
| `lectures/Day 12 Lecture Slides 430.pdf` | 1–25 of 25 (p.12 a blank Top Hat slide; p.16 a periodic table with no text; p.22, p.23, p.25 textbook figures; p.24 a professor-made band sketch) | MO Theory (now taught: H₂, H₂⁻, He₂, Fig. 5.48, Fig. 5.50, HOMO/LUMO, theories of bonding); Metals, Metalloids, and Nonmetals; Band Theory; Semiconductors and Doping; Midterm 1 announcements | 2026-10-06 |
| textbook §18.4–18.5 (TB PDF p.918–921, printed 884–887) | text layer read; p.918–921 rendered and viewed (Figs. 18.25–18.27; the NaCl band-gap value) | Band Theory; Semiconductors and Doping; Metals (malleability, ductility) | 2026-10-06 |

# Course Index

Cumulative understanding of lecture slides, lecture notes, and professor review
material, organized by CONCEPT (not by file). Maintained by `/ingest-course`;
merge new sources into existing concepts instead of appending per-file dumps.
Homework analysis lives in `HOMEWORK_INDEX.md`; textbook locations live in
`TEXTBOOK_MAP.md`.

**Status:** INGESTED — Day 1–8 lecture slides (187 PDF pages), every page
visually inspected at 220 DPI, with 300–400 DPI zooms wherever notation was
small or the text layer was garbled. No lecture notes, review sheets, homework,
or image files have been supplied yet. Last updated 2026-09-25 (Day 8).

**Citation key:** `Day N p.X` = `materials/lectures/Day N Lecture Slides.pdf`,
physical PDF page X (one slide per page). `TB PDF p.X (printed Y)` = the Gilbert
textbook PDF (see `TEXTBOOK_MAP.md`; printed = PDF − 34 in Ch. 1–4). "Top Hat" =
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
- [UNCERTAIN] What RAMP UP is (platform, module, or reading) and whether its topics are examinable are not stated in the slides.

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
- Used later in: [INFERRED] the O → O⁺ orbital diagram for ionization energy (Day 7 p.9) and nitrogen's circled electron affinity (Day 7 p.11); the slides do not explain either in words.

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

# Unit D — Chemical Bonding (Ch. 4; Day 7 p.12–21)

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
- Used later in: Coulombic potential energy explains the ionic bond (Day 7 p.15).

### Uncertainties and discrepancies
- [SOURCE-DERIVED] Two phrasings now appear in the slides: "Covalent bonds: Exist between non-metals… highly localized" and metallic "highly mobile" (Day 7 p.14), and Table 4.1's "Nonmetals and metalloids" and "Delocalized" (Day 8 p.15; textbook TB PDF p.184). They don't conflict: the table also counts metalloids → COURSE.md glossary.
- [UNCERTAIN] Electronegativity (textbook §4.2) is partly bolded on Day 7 p.12 ("…and **Bonding**") but has no slide content yet, and Ch. 4 outcome 3 (bond polarity from electronegativity) is not bold (Day 7 p.13).

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

**Sources:** Day 8 p.19–26, p.28–30
**Unit / lecture order:** Day 8, §4.4, the last topic of the deck
**Prerequisites:** Lewis symbols and the octet rule; bonding capacity
**Emphasis evidence:** "**more than one pair of electrons**", "A double bond!", "A triple bond!" printed bold (Day 8 p.20); §4.4 bold and outcome 5 bold (Day 8 p.4–5). [SUPPORTED EMPHASIS] The five steps appear word for word on seven slides (Day 8 p.21, 22, 23, 25, 28, 29, 30), with "**bonding capacity**" bold each time.

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
- [UNCERTAIN] Day 8 p.23 carries a callout in the PDF's text layer that is hidden in the rendered slide (black text beneath another text box; probably revealed by animation in class): "Note that a Lewis structure is a two-dimensional representation. We'll see later that ammonia is tetrahedral, but Lewis structures can't tell us that!" [CLARIFICATION] ammonia's four electron groups point to the corners of a tetrahedron, and its atoms form a trigonal pyramid. Molecular shape comes later (textbook Ch. 5, not yet mapped).
- (Day 8 p.24–25) "That was pretty easy, right? Let's try another one." C₂H₂: "Historical name: acetylene; Systematic name: ethyne". C 2 × 4 = 8, H 2 × 1 = 2, "TOTAL: 10". The skeleton H–C–C–H becomes H–C≡C–H.
- (Day 8 p.28–30) Ozone, O₃: O 3 × 6 = 18. The skeleton O–O–O (p.28) gets three lone pairs on each end O, then one lone pair on the central O (p.29), which leaves the central O with only 6 electrons. The final slide shows two bent structures, O=O–O and O–O=O: the double-bonded end O has two lone pairs, the central O one, and the single-bonded end O three (p.30).
- [VERIFICATION] RDKit and `tools/chemistry_verify.py electrons`: NH₃ 8, C₂H₂ 10, and O₃ 18 valence electrons. Every atom in the final structures has an octet (H has 2). In each O₃ structure the formal charges are −1 (single-bonded O), +1 (central), and 0; formal charge (§4.7) is not bold on Day 8 p.4 [CLARIFICATION].

### Professor explanations, models, and diagrams
- [SOURCE-DERIVED] "Further Considerations: That was pretty easy, right? So why is this ever difficult? Sometimes it is **impossible** for every atom to have an octet. Sometimes it is possible to draw more than one perfectly valid Lewis structure. We'll need to learn some new chemistry to help us resolve these situations: Electronegativity, Formal Charge, **Resonance**" (Day 8 p.26; only "impossible" and "Resonance" are bold). The slide shows the finished NH₃ and C₂H₂ structures.
- [INFERRED] The two O₃ structures (Day 8 p.30) are the "more than one perfectly valid Lewis structure" case, i.e., resonance (§4.6, bold on Day 8 p.4). The slides don't use the word "resonance" for O₃ yet, and no ↔ arrow is drawn.

### Recognition cues
- [INFERRED] "Draw the Lewis structure of …" → the five steps. H is never central (bonding capacity 1); with C present, C is central (4 bonds, "memorize", Day 8 p.18). If the electron count comes out short of octets, add a multiple bond.

### Common mistakes flagged
- [INFERRED] Skipping step 1's electron count (the table exists for this); putting H in the middle; giving H lone pairs; stopping at step 5 with a central atom that has only 6 electrons (the O₃ stage on p.29); forgetting that the two O₃ structures are equally valid.

### Connections
- Builds on: Lewis symbols and bonding capacity (Day 8 p.16–18); covalent bonds as shared electrons (Day 7 p.14); allotropes, which introduce O₃ (Day 8 p.27). Used later in (announced): electronegativity, formal charge, and resonance (Day 8 p.26).

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
- Builds on: the Representation Matters slide: Molina and Rowland predicted "that CFCs might lead to the destruction of the ozone layer" (Day 8 p.2). Used later in: the ozone Lewis structure (Day 8 p.28–30).

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

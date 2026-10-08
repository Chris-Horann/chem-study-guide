# Source scope — Chem 1151 Current Course Guide

Built: 2026-09-24; gap check and fixes 2026-09-25 (the same request, re-issued); extended 2026-09-25 with Day 8 and the rest of Ch. 4; extended 2026-10-06 with Days 9–11 and all of Ch. 5, then the same day with Day 12 and Ch. 18 §18.4–18.5. Requested scope (student, 2026-09-24): "Cover every section and major
concept in Gilbert textbook Chapters 1–3, including topics the lectures have not reached.
Begin Chapter 4 with its first two sections. Also include any later Chapter 4 sections
directly covered by the lectures ingested so far. Incorporate the Day 1–7 lectures and
preserve the professor's terminology and methods where they apply." (This replaces the
first request, which covered only the Day 1–7 lecture material.)

**Extended 2026-09-25** (student): "Extend the finished study guide… with Day 8 and **all remaining sections of
Gilbert textbook Chapter 4**. Preserve the existing Days 1–7 and Chapters 1–3 content… Cover every Chapter 4
section and major concept, including material ahead of the lectures. Clearly label each topic as covered in
lecture or textbook preview." The guide now covers Gilbert Ch. 1–4 in full and Days 1–8.

**Extended 2026-10-06** (student): the ingest request "Put three new lecture slides cover all of chapter 5 as well from
the book", then `/build-study-guide` with no arguments, then "keep going". Read as: add the Day 9–11 lectures and
**every section of Gilbert Chapter 5**, including material ahead of the lectures (labeled textbook preview); relabel
the Ch. 4 sections Day 9 now teaches (§4.2, §4.5–4.8) from preview to lecture; keep every existing module, problem
id, and the progress key. The guide now covers Gilbert Ch. 1–5 in full and Days 1–11.

**Extended 2026-10-06, Day 12** (student): "I also added day 12 lecture and also put down notes for 18.4-18.5, do this
quick and just do these things, dont try to go through all of the other modules". Read as: ingest Day 12; add the two
Ch. 18 sections Day 12 bolds, §18.4 Metallic Bonds and Conduction Bands and §18.5 Semiconductors, as one new module
(m25, with notes on both sections in the textbook preview box); mark §5.7's MO content as lecture where Day 12 p.6–13
teaches it; leave every other module as it was. The rest of Ch. 18 (§18.1–18.3, §18.6–18.9) is not in the guide.

## How topics are labeled in the guide

- **Covered in lecture**: taught on the Day 1–12 slides (`materials/lectures/`). Every block
  cites the file and slide (PDF page).
- **Textbook preview**: in Gilbert Ch. 1–5 or §18.4–18.5 but **not taught in any lecture so
  far** (through Day 12). It is included because the student asked for it. The guide never presents it as
  something the professor said, taught, or emphasized, and its exam status is unknown.
- Inside a lecture topic, "Background (not from lecture)" marks outside or textbook
  explanation of a lectured idea, and "Connection" marks an inference.

## Lecture sources used

| File | Pages | Topics |
|---|---|---|
| `materials/lectures/Day 1 Lecture Slides.pdf` | 6–15 | Ch. 1 outcomes; conservation of mass; constant composition / definite proportions; multiple proportions; Dalton's atomic theory; conservation of energy and mass–energy |
| `materials/lectures/Day 1 Lecture Slides.pdf` | 16–20 | Ch. 2 outcomes; Thomson and the cathode-ray tube |
| `materials/lectures/Day 2 Lecture Slides.pdf` | 4–20 | Thomson's experiments; plum pudding; Millikan; Rutherford's gold foil; the nuclear atom |
| `materials/lectures/Day 2 Lecture Slides.pdf` | 21–24 | RAMP UP slides: amu, subatomic-particle table, isotopes, periodic table |
| `materials/lectures/Day 2 Lecture Slides.pdf` | 25–31 | EM radiation (λν = c, E = hν); EM spectrum; solar spectrum |
| `materials/lectures/Day 3 Lecture Slides.pdf` | 2, 7–21 | emission and absorption spectra; blackbody radiation; Planck's quanta; photoelectric effect; Balmer's formula |
| `materials/lectures/Day 4 Lecture Slides.pdf` | 3, 6–18 | Balmer → Rydberg; Bohr model and ΔE; hydrogen series; de Broglie; standing waves; diffraction; Schrödinger (existence only) |
| `materials/lectures/Day 5 Lecture Slides.pdf` | 7–20 | wavefunctions, probability density; quantum numbers; Pauli; orbital shapes and radial distributions |
| `materials/lectures/Day 6 Lecture Slides.pdf` | 6–26 | electron configurations; penetration, shielding, Z_eff; Hund's rule; 4s before 3d; ion configurations; atomic radius |
| `materials/lectures/Day 7 Lecture Slides.pdf` | 4–21 | filling exceptions (acknowledged, then excluded); atomic and ionic radius; ionization energy; electron affinity; ionic, covalent, metallic bonds; Coulombic E_el; lattice energy; ionic formulas; naming binary ionic compounds |
| `materials/lectures/Day 8 Lecture Slides.pdf` | 3–30 | midterm announcement (p.3); Ch. 4 section list and outcomes (p.4–5); naming ionic compounds, repeated (p.6); transition-metal Roman numerals (p.7, Top Hat p.10); polyatomic ions, Table 4.5, "provided… on the exams" (p.8–9); covalent H–H energy curve (p.11); naming covalent compounds, Table 4.3 prefixes (p.12–13); metallic bonds, electron sea (p.14); Table 4.1 (p.15); octet rule (p.16); Lewis symbols (p.17); bonding capacity, "carbon ALMOST ALWAYS forms 4 covalent bonds" (p.18); F₂, O₂, N₂ (p.19–20); five steps (p.21); NH₃ (p.22–23); C₂H₂ (p.24–25); further considerations: electronegativity, formal charge, resonance announced (p.26); allotropes O₂/O₃ (p.27); O₃ (p.28–30) |
| `materials/lectures/Day 9 Lecture Slides.pdf` | 3–30 | "Advanced Lewis Structures": midterm "NEXT THURSDAY" (p.3); Ch. 4 list and outcomes, bold items (p.4–5); ozone practice repeated (p.6); resonance: 128 pm vs. 148 and 121 pm, "equivalent" is not "the same", curved arrows, ↔, never switching back and forth, the hybrid with dashed bonds and 5-dot ends, delocalization "beyond the scope of this class" (p.7–11); Kekulé's benzene and its hybrid (p.12–13); Table 4.6 with boxed rows (p.14); polar bonds, battery analogy, potential maps, the χ table, the 0.4/2.0 guidelines (p.15–18); N₂O: step-1 table, three structures, formal charge (four steps, four rules, the blank table; p.19–24); Top Hat questions (p.25; H₃PO₄, p.26); octet exceptions: H duets, electron-deficient Be, B, Al (p.27), radicals NO and NO₂ (p.28), expanded octets and "hypervalency… not well understood" (p.29), SO₄²⁻, PCl₅, SF₆ (p.30) |
| `materials/lectures/Day 10 Lecture Slides.pdf` | 2, 4–31 | exam review and "Ramp Up IS on this exam" (p.2); Ch. 5 list and outcomes (p.4–5); chiral carvone (p.6); "Sometimes Lewis structures are enough" (p.7); VSEPR, electron-pair vs. molecular geometry (p.8); steric number and the five shapes (p.9–12); formaldehyde about 118° (p.13); lone pairs: ozone 117°, ammonia 107°, water 104.5° (p.14–19); SN 5 lone pairs equatorial: seesaw, T-shaped, linear (p.20–23; Top Hat p.17, p.21, questions not in the PDF); SN 6: square pyramidal, square planar (p.24–25); the professor's summary table (p.26); polar bonds (p.27); CO₂ and CF₄ nonpolar, H₂O polar (p.28–31) |
| `materials/lectures/Day 11 Lecture Slides.pdf` | 2, 4–27 | midterm "NEXT THURSDAY" (p.2); Ch. 5 list and outcomes (p.4–5); H₂O polar (p.6); CHCl₃ vs. CCl₃F (p.7); Table 5.2 (p.8); valence bond theory and the H–H curve (p.9); σ bonds (p.10); the methane problem and promotion (p.11); hybridization, one hybrid per electron domain (p.12–16); π bonds and formaldehyde (p.17–19); the hybrid-orbital rules (p.20; Top Hat p.21, question not in the PDF); diazene, acetylene (p.22–23); Table 5.3 (p.24); ethylene, acrolein, benzene, PAHs (p.25–26); O₂ is paramagnetic, "let's talk briefly about Molecular Orbital Theory" (p.27) |
| `materials/lectures/Day 12 Lecture Slides 430.pdf` | 2, 4–25 | midterm "THURSDAY!" (p.2); Ch. 5 list and outcomes, §5.7 and outcome 4 bold, §5.6 grey (p.4–5); O₂ repeated (p.6); MO theory: one MO per atomic orbital (p.7), H₂ σ1s/σ*1s and the bond-order formula (p.8), H₂⁻ and He₂ (p.9), 2p σ and π MOs (p.10), Fig. 5.50 with both orders, bond orders, HOMO and LUMO (p.11; Top Hat p.12, question not in the PDF), "Theories of Bonding" (p.13); Ch. 18 list and outcomes, §18.4–18.5 and outcome 3 bold (p.14–15); metals, metalloids, nonmetals (p.16–17); the conductor/insulator rule (p.18); Na₂, Na₄, Na_N and the HOMO–LUMO gap (p.19–22); Zn_N (p.23); the professor's band sketch with T ↑ (p.24); doping, P donor and Ga acceptor levels (p.25) |

Non-content slides (announcements, "Representation Matters", generic Top Hat
instructions) are not taught.

## Textbook sections included

Gilbert, Kirss, Bretz, Foster, *Chemistry: An Atoms-Focused Approach*, 3rd ed.
(`materials/textbook/…(1).pdf`). **Printed page = PDF page − 34** in Ch. 1–5 and Ch. 18. Section
page ranges run from the section's first page to the next section's first page.

| Section | Printed pp. | PDF pp. | Label | Guide module |
|---|---|---|---|---|
| Ch. 1 opener, learning outcomes | 2–4 | 36–38 | outcomes compared with Day 1 p.7 | Start page |
| §1.1 Exploring the Particulate Nature of Matter | 4–7 | 38–41 | covered in lecture (Day 1 p.8–14); scientific-methods part is textbook preview | m1 |
| §1.2 COAST: A Framework for Solving Problems | 7–8 | 41–42 | textbook preview (greyed out on Day 1 p.6) | t1-2 |
| §1.3 Classes and Properties of Matter (incl. Separating Mixtures) | 8–13 | 42–47 | textbook preview | t1-3 |
| §1.4 States of Matter | 13–16 | 47–50 | textbook preview | t1-4 |
| §1.5 Forms of Energy | 16–17 | 50–51 | conservation of energy: covered in lecture (Day 1 p.15); work, PE, KE, heat: textbook preview | t1-5 |
| §1.6 Formulas and Models | 17–19 | 51–53 | textbook preview | t1-6 |
| §1.7 Expressing Experimental Results (Precision and Accuracy; Significant Figures; Significant Figures in Calculations) | 19–26 | 53–60 | textbook preview (italic on Day 1 p.6–7) | t1-7 |
| §1.8 Unit Conversions and Dimensional Analysis | 26–31 | 60–65 | textbook preview (italic) | t1-8 |
| §1.9 Analyzing Experimental Results | 31–37 | 65–71 | textbook preview (greyed out) | t1-9 |
| Ch. 1 Summary, Problem-Solving Summary | 37–38 | 71–72 | used as a completeness check | — |
| Ch. 2 opener, learning outcomes | 46–48 | 80–82 | outcomes compared with Day 1 p.16–17 | Start page |
| §2.1 When Projectiles Bounced Off Tissue Paper: The Rutherford Model (Electrons; Radioactivity; The Nuclear Atom) | 48–53 | 82–87 | covered in lecture (Day 1 p.16–20; Day 2 p.4–20); the Radioactivity subsection is textbook preview | m2 |
| §2.2 Nuclides and Their Symbols | 53–56 | 87–90 | isotopes and the particle table: covered in lecture (RAMP UP slides, Day 2 p.21–23); nuclide symbols and ions: textbook preview | t2-2 |
| §2.3 Navigating the Periodic Table | 56–60 | 90–94 | layout basics: covered in lecture (RAMP UP slide, Day 2 p.24); the rest: textbook preview | t2-3 |
| §2.4 The Masses of Atoms, Ions, and Molecules | 60–64 | 94–98 | amu: covered in lecture (RAMP UP, Day 2 p.21); average atomic mass, molecular and formula mass: textbook preview | t2-4 |
| §2.5 Moles and Molar Masses | 64–70 | 98–104 | textbook preview | t2-5 |
| §2.6 Mass Spectrometry: Determining Molecular Masses | 70–74 | 104–108 | textbook preview (greyed out on Day 1 p.16) | t2-6 |
| Ch. 2 Summary | 74 | 108 | completeness check | — |
| Ch. 3 opener, learning outcomes | 84–86 | 118–120 | outcomes compared with Day 2 p.26, Day 3 p.6 | Start page |
| §3.1 Nature's Fireworks and the Electromagnetic Spectrum | 86–89 | 120–123 | covered in lecture (Day 2 p.25–30); Maxwell's oscillating fields: textbook preview | m3 |
| §3.2 Atomic Spectra | 89–90 | 123–124 | covered in lecture (Day 2 p.31; Day 3 p.7–11) | m4 |
| §3.3 Particles of Light: Quantum Theory (Photons of Energy; The Photoelectric Effect) | 90–95 | 124–129 | covered in lecture (Day 3 p.11–19) | m5 |
| §3.4 The Hydrogen Spectrum and the Bohr Model | 95–100 | 129–134 | covered in lecture (Day 3 p.21; Day 4 p.3, p.6–10) | m6 |
| §3.5 Electrons as Waves: De Broglie Wavelengths | 100–103 | 134–137 | covered in lecture (Day 4 p.11–17) | m7 |
| §3.5 Electrons as Waves: The Heisenberg Uncertainty Principle | 103–104 | 137–138 | textbook preview | t3-5 |
| §3.6 Quantum Numbers | 104–108 | 138–142 | covered in lecture (Day 4 p.18; Day 5 p.7–16) | m8 |
| §3.7 The Sizes and Shapes of Atomic Orbitals | 108–111 | 142–145 | covered in lecture (Day 5 p.17–20); the terms "node" and "boundary surface": textbook preview | m9 |
| §3.8 The Periodic Table and Filling Orbitals | 111–119 | 145–153 | covered in lecture (Day 6 p.6–20; Day 7 p.6); excited states and the Cr/Cu/Ag exceptions: textbook preview | m10 |
| §3.9 Electron Configurations of Ions | 119–122 | 153–156 | covered in lecture (Day 6 p.21–23) | m11 |
| §3.10 The Sizes of Atoms and Ions | 122–125 | 156–159 | covered in lecture (Day 6 p.24–26; Day 7 p.7–8) | m12 |
| §3.11 Ionization Energies | 125–128 | 159–162 | covered in lecture (Day 7 p.9–10) | m13 |
| §3.11 Photoelectron Spectroscopy | 128–130 | 162–164 | textbook preview | t3-11 |
| §3.12 Electron Affinities | 130–133 | 164–167 | covered in lecture (Day 7 p.11) | m13 |
| Ch. 3 Summary, Problem-Solving Summary | 133–134 | 167–168 | completeness check | — |
| Ch. 4 opener, learning outcomes | 144–146 | 178–180 | outcomes compared with Day 7 p.13 | Start page |
| §4.1 Chemical Bonds and Greenhouse Gases (Ionic; Covalent; Metallic Bonds) | 146–151 | 180–185 | covered in lecture (Day 7 p.12–17; Day 8 p.11 H–H energy curve, p.14 electron sea, p.15 Table 4.1, p.18 bonding capacity); greenhouse gases: textbook preview | m14 |
| §4.2 Electronegativity, Unequal Sharing, and Polar Bonds | 151–154 | 185–188 | covered in lecture (Day 9 p.15–18: polar bonds, the battery analogy, potential maps, the χ table, the 0.4/2.0 guidelines; Day 10 p.27); the textbook's definitions and extra examples are boxed as preview | t4-2 |
| §4.3 Naming Compounds and Writing Formulas: Binary Molecular Compounds | 154–155 | 188–189 | covered in lecture (Day 8 p.12–13); dropping a prefix's vowel before "oxide": textbook preview | m17 |
| §4.3 …: Binary Ionic Compounds of Main Group Elements | 155–156 | 189–190 | covered in lecture (Day 7 p.18–21; Day 8 p.6) | m15 |
| §4.3 …: Binary Ionic Compounds of Transition Metals | 156–157 | 190–191 | covered in lecture (Day 8 p.7, p.10); no numeral for Ag⁺, Cd²⁺, Zn²⁺: textbook preview | m16 |
| §4.3 …: Polyatomic Ions | 157–159 | 191–193 | covered in lecture (Day 8 p.8–9); formulas that need parentheses (Mg₃(PO₄)₂): textbook preview | m16 |
| §4.3 …: Binary Acids; Oxoacids | 159–161 | 193–195 | textbook preview | t4-3 |
| §4.4 Lewis Symbols and Lewis Structures (Lewis Symbols; Lewis Structures of Ionic Compounds; Five Steps; Double and Triple Bonds) | 161–168 | 195–202 | covered in lecture (Day 8 p.16–26, p.28–30); Lewis structures of ionic compounds and ions in brackets, the ion-charge count in step 1, and the electronegativity tie-breaker: textbook preview | m18, m19 |
| §4.5 Resonance (the slides number it 4.6) | 168–172 | 202–206 | covered in lecture (Day 8 p.26–30; Day 9 p.6–13: ozone's equal bonds, curved arrows, ↔, the resonance hybrid, delocalization, benzene); nitrate, carbonate, and the textbook's rules for resonance: preview | t4-5 |
| §4.6 The Lengths and Strengths of Covalent Bonds (the slides number it 4.5) | 172–174 | 206–208 | covered in lecture (Day 8 p.11; Day 9 p.7 ozone's bond lengths, p.14 Table 4.6 with the boxed rows); averaging shared pairs over equivalent bonds: a connection the guide infers from Day 9 p.9–10; the textbook's "bond order" definition, its values such as 4/3, and the bond-energy definitions: preview | t4-6 |
| §4.7 Formal Charge: Choosing among Lewis Structures | 174–178 | 208–212 | covered in lecture (Day 9 p.19–26: N₂O, the four steps, the four rules, the H₃PO₄ Top Hat); the textbook's other examples: preview | t4-7 |
| §4.8 Exceptions to the Octet Rule | 178–183 | 212–217 | covered in lecture (Day 9 p.27–30: electron-deficient Be, B, Al; radicals NO, NO₂; expanded octets PCl₅, SF₆, SO₄²⁻); the textbook's Z &gt; 12 rule, NO₂ dimerizing, and its d-orbital remark: preview | t4-8 |
| §4.9 Vibrating Bonds and the Greenhouse Effect | 183–185 | 217–219 | textbook preview (not taught through Day 11; the professor's Ch. 5 outcome 5 names this topic, Day 10 p.5) | t4-9 |
| Ch. 4 Summary, Problem-Solving Summary | 185–186 | 219–220 | completeness check | — |
| Ch. 5 opener, Particulate Preview, learning outcomes | 196–198 | 230–232 | outcomes compared with Day 10 p.5 and Day 11 p.5 | modules m20–t5-7 |
| §5.1 Biological Activity and Molecular Shape | 198–199 | 232–233 | covered in lecture (Day 10 p.3, p.6–7: carvone, "Sometimes Lewis structures are enough…"); molecular recognition: preview | m20, t5-6 |
| §5.2 VSEPR: Central Atoms with No Lone Pairs | 200–203 | 234–237 | covered in lecture (Day 10 p.8–13); Eq. 5.1 as written, the wedge convention, the three steps, the Concept Test: preview | m20 |
| §5.2 VSEPR: Central Atoms with Lone Pairs | 203–209 | 237–243 | covered in lecture (Day 10 p.14–26); the four repulsion rankings, counting 90° repulsions, Table 5.1's examples, BrF₅'s 85°: preview | m21 |
| §5.3 Polar Bonds and Polar Molecules | 209–212 | 243–246 | covered in lecture (Day 10 p.27–31; Day 11 p.6–8, Table 5.2); the bond-dipole and dipole-moment definitions, the debye, alignment in a field, C–H "essentially nonpolar", H₂S: preview | m22 |
| §5.4 Valence Bond Theory and Hybrid Orbitals (sp³, sp², sp) | 213–219 | 247–253 | covered in lecture (Day 11 p.9–24); no promotion step in the textbook, sp² lower in energy than sp³, Sample Ex. 5.5 (CO₂): preview | m23, m24 |
| §5.5 Molecules with Multiple "Central" Atoms | 219–221 | 253–255 | covered in lecture (Day 11 p.22–26: diazene, acetylene, ethylene, acrolein, benzene); conjugation, aromatic compounds, PAHs and DNA, ethylene and tomatoes: preview | m24 |
| §5.6 Chirality and Molecular Recognition | 221–227 | 255–261 | lecture hook only (carvone, Day 10 p.6; the slide gives no definition; §5.6 is grey on Day 12 p.4); everything else: textbook preview | t5-6 |
| §5.7 Molecular Orbital Theory (H₂; homonuclear and heteronuclear diatomics; auroras; O₃; SN &gt; 4) | 227–239 | 261–273 | covered in lecture: O₂'s paramagnetism (Day 11 p.27) and, on Day 12 p.6–13, one MO per atomic orbital, H₂, H₂⁻, He₂, the bond-order formula, the 2p σ and π MOs, Fig. 5.50's two orders and bond orders for Li₂–Ne₂, HOMO and LUMO, and which theory answers which question; the five guidelines, "diamagnetic", the 2s–2p mixing reason, ions, NO, auroras, O₃, SN &gt; 4: textbook preview | t5-7 |
| Sample Ex. 5.10, Summary, Problem-Solving Summary | 240–242 | 274–276 | completeness check | — |
| §18.4 Metallic Bonds and Conduction Bands | 884–886 | 918–920 | covered in lecture (Day 12 p.17–24: metals' properties; Na₂ → Na₄ → Na_N; Zn_N; the conductor rule; the band sketch); weak metallic bonds and Na's body-centered cubic packing, the margin definitions, the "not mutually exclusive" remark, the Mg Concept Test: preview | m25 |
| §18.5 Semiconductors | 886–887 | 920–921 | covered in lecture (Day 12 p.18, p.24–25: metalloids, the small gap, T ↑, P donor and Ga acceptor levels, n-type and p-type); every number (Si 106 kJ/mol, 4 and 7 kJ/mol, NaCl), holes, substitutional alloys, GaAs and LEDs, CdS/CdSe, the GaAs Concept Test: preview | m25 |

## Review material used for weighting (with evidence)

None supplied, so no topic is weighted by exam evidence. The small "Lecture signal" notes
cite only formatting or annotation evidence recorded in `materials/COURSE_INDEX.md`: bold
items on the chapter slides, red text or circles, slides repeated across lectures, and
in-class Top Hat questions. Textbook-preview topics never get lecture signals.

## Homework problem types modeled (HOMEWORK_INDEX types, not copied problems)

None. No homework has been supplied (`materials/HOMEWORK_INDEX.md`). Every practice
problem is **new**. They are modeled on the lecture's worked examples (Day 1 p.11, p.13;
Day 4 p.12, p.14), the in-class Top Hat questions (Day 2 p.28; Day 5 p.16; Day 6 p.23,
p.26; Day 8 p.10; Day 9 p.26 phosphoric acid; the Day 10 p.20 axial-or-equatorial question; reproduced with our
own answer keys), and, for textbook-preview topics, the kinds
of skills the textbook's Sample Exercises practice. No textbook example or exercise is
copied, and textbook answers are not reproduced. The Ch. 4 problems were compared with §4.3–4.9's Sample
Exercises, Practice Exercises, Concept Tests, and in-text examples, and the 20 that overlapped were replaced with new species
(details in `VERIFICATION.md`). Worked textbook examples (N₂O's formal-charge table, nitrate, carbonate) appear
only as cited teaching content. The Ch. 5 problems were compared the same way with §5.1–5.7's Sample and Practice
Exercises, Concept Tests, in-text examples, and the end-of-chapter Visual Problems and Questions (read for this
comparison only); in those passes 46 items changed, for textbook overlap, explorer overlap, or duplication (VERIFICATION.md §1c).

## Explicitly excluded

- **Everything after Ch. 5** (Ch. 6 starts at PDF 286) except §18.4–18.5: not read. In Ch. 18, §18.1–18.3 and
  §18.6–18.9 (listed plain on Day 12 p.14) are excluded; §18.4–18.5 (PDF 918–921) were read for m25.
- **End-of-chapter material**: Visual Problems and Questions and Problems (Ch. 1 PDF
  72–79, Ch. 2 PDF 109–117, Ch. 3 PDF 168–177, Ch. 4 PDF 221–231, Ch. 5 PDF 277–285) were not processed.
- **Schrödinger mathematics** ("beyond the scope of this class", Day 5 p.7). The 3s
  wavefunction formula (Day 5 p.9) is not reproduced.
- **History details** (dates, attributions) from "Representation Matters" slides and
  textbook narrative: never tested.
- **Out-of-range lectures**: none; Day 11 is the latest supplied. Non-content slides (Representation Matters,
  announcements, blank Top Hat slides) are not taught; their history isn't tested.
- **Delocalization's extra stability** ("for reasons beyond the scope of this class", Day 9 p.10): stated, not
  explained. **Hypervalency** ("not well understood", Day 9 p.29): the slides' expanded-octet structures are taught;
  the textbook's three-center model appears only inside the §5.7 preview, labeled as the textbook's alternative.
- Anything in the Appendixes (e.g., the full t table): not read.

## Professor conventions applied (from COURSE.md)

- **Constants**: c = 2.998 × 10⁸ m/s; h = 6.626 × 10⁻³⁴ J·s; Bohr constant 2.178 × 10⁻¹⁸ J;
  Coulomb constant 2.31 × 10⁻¹⁹ J·nm; Balmer constant 364.56 nm; m_e = 9.109 × 10⁻³¹ kg.
  N_A = 6.022 × 10²³ mol⁻¹ is not on any slide; lecture-topic problems that use it say so,
  and it is taught in the §2.5 textbook-preview module.
- **Symbols**: ν for frequency; u for velocity (λ = h/(mu); the textbook also uses u);
  φ for the threshold energy (work function; the textbook writes Φ); amu (the textbook
  writes u, the unified atomic mass unit).
- **Equations in the professor's form**: KE = hν − φ = hν − hν₀;
  ΔE = −2.178 × 10⁻¹⁸ J (1/n_final² − 1/n_initial²); λ = h/(mu); M(g) + hν → M⁺(g) + e⁻;
  M(g) + e⁻ → M⁻(g); E_el = 2.31 × 10⁻¹⁹ J·nm (Q₁Q₂/d).
- **Signs**: ΔE < 0 for emission; IE always positive; EA ± (negative = energy released);
  lattice energy U negative; E_el negative for attraction.
- **Configurations**: filling order ([Ar]4s²3d⁶) and n order ([Ar]3d⁶4s²) are both
  accepted (both appear in lecture; the textbook uses n order). Cations lose their
  highest-n electrons first (Day 6 p.21). Exceptions are ignored in this course (Day 7 p.6);
  the textbook's exceptions appear only in a labeled preview box.
- **Significant figures**: no lecture policy; answers carry the precision of the
  least-precise input (as in the worked examples). The §1.7 preview module teaches the
  textbook's rules, including its round-half-to-even tie rule. Numeric answers are
  checked at ±1%, with separate sig-fig and unit feedback.
- **Naming**: cation = element name; anion = element stem + "-ide"; no number prefixes
  (Day 7 p.21). Transition-metal ions get a Roman numeral for their charge, the "systematic name" (Day 8 p.7,
  p.10); the slides' spacing "copper (II) oxide" and the textbook's "copper(II) oxide" are both accepted;
  historical names (cupric) are not required. Polyatomic ions come from the table the professor provides on
  exams (Day 8 p.8), shown in the toolkit. Covalent names: prefixes, no "mono" on the first element (Day 8
  p.12); the textbook's dropped vowel (monoxide) is taught as a preview and both forms are accepted.
- **Lewis structures**: the professor's five steps, word for word (Day 8 p.21), with step 1 as a table
  (Day 8 p.22); "bonding capacity" (the textbook's *valence*) for the number of bonds; the central atom has the
  largest bonding capacity. The textbook's extra rules (ion charges in step 1, brackets, the electronegativity
  tie-breaker, converting lone pairs in step 5) are labeled as textbook preview.
- **Resonance and formal charge** (Day 9): "equivalent" structures are not "the same"; the molecule never switches
  between them; the hybrid is drawn with dashed partial bonds. Formal charge by the professor's four steps and four
  rules (Day 9 p.22–23); an expanded octet is preferred when it brings formal charges closer to zero (Day 9 p.29).
- **VSEPR** (Day 10): steric number = "regions of high electron density" or "directions" (p.9), also "electron
  domains" (p.26); electron-pair geometry first, then the molecular geometry of the atoms only (p.8, p.14); the
  slides' shape names (bent with "angular" in parentheses, seesaw, T-shaped, square pyramidal, square planar); the
  slides' angles (117°, 107°, 104.5°, about 118°). The Day 10 p.26 table is reproduced as printed, with its gaps noted.
- **Polarity**: polar bonds AND a shape whose bond dipoles don't cancel (Day 10 p.29–31); crossed arrows point to
  the δ− end (Day 9 p.15). Δχ values from the slide's χ table (Day 9 p.17).
- **Hybridization** (Day 11): one hybrid per electron domain (SN 2 sp, 3 sp², 4 sp³; p.12, p.24); the p.20 rules
  (σ head-on, H uses 1s; π side-to-side from unhybridized p; lone pairs in hybrids). Promotion is shown only as the
  rejected idea (p.11). No sp³d or sp³d² anywhere: neither the slides nor the textbook use them.

## Open uncertainties carried into the guide

- **Textbook edition**: the slides' Ch. 4 numbering (4.5 Lengths and Strengths, 4.6 Resonance), their Table 4.5
  (polyatomic ions; the book's Table 4.4), and the CaS row in Table 4.2 differ from the supplied 3rd edition.
  Sections are cited by title and page.
- **Day 8 p.23 hidden callout** ("…ammonia is tetrahedral…"): in the PDF text layer only. Day 10 p.16–18 resolves it:
  ammonia's electron pairs are tetrahedral; its molecular geometry is trigonal pyramidal.
- **Midterm 1** is "NEXT THURSDAY" (Day 9 p.3; Day 10 p.2; Day 11 p.2; Thu 2026-10-08, inferred), with a review on
  Tuesday 5:25–6:35 in Hurtig 129 and "Ramp Up IS on this exam". Its topic list is not stated.
- **Top Hat questions without text in the PDF** (Day 9 p.25; Day 10 p.17, p.21; Day 11 p.21): the guide doesn't
  guess them; where the next slide answers one (Day 10 p.22–23), the guide uses that answer.
- **Day 11 p.24 (Table 5.3)** prints "Trigonal planar" for sp³ with 3 σ bonds; Day 10 p.18 and p.26 and the
  textbook's Table 5.3 (PDF p.252) say trigonal pyramidal. The guide shows the slide and explains the slip.
- **Day 10 p.26 table**: no row for SN 5 with 3 lone pairs (linear, shown on Day 10 p.23); SN 6 with 3 lone pairs listed
  as T-shaped (the textbook: possible, but not met in practice, PDF p.240); the angle column gives electron-pair angles.
- **Formaldehyde "about 118°"** (Day 10 p.13) matches the textbook's implication (PDF p.237); the measured value
  is about 116.5° (background).
- **"Methane only has two unpaired electrons"** (Day 11 p.11) means carbon's ground state, as its figure shows.
- **Ch. 5 outcomes**: the slides' list (Day 10 p.5) has no chirality outcome and adds a greenhouse outcome that is
  the supplied edition's §4.9, consistent with the edition question above. Chirality (§5.6) and MO theory (§5.7)
  are mostly preview; exam status unknown.
- **Textbook slips in Ch. 5** (logged in COURSE.md): Sample Ex. 5.9's NO⁻ configuration; Figs. 5.58–5.59 box
  counts; the aurora "π*" sentence; "(+) enantiomers" of amino acids; Fig. 5.49's caption. The guide uses corrected versions.
- **Exam status** of textbook-preview and RAMP UP topics is unknown.
- **Lattice image identity** (Day 7 p.16–17): the slide doesn't label the ions.
- **Table 3.2 values** (Day 7 p.10 = textbook): used exactly as printed; they differ from NIST reference values
  by up to 1.9% (Li IE₃), and N IE₄ = O IE₄ and N IE₅ = Ne IE₄ as printed. No valence/core jump moves.
- **Neutron mass** typo on Day 2 p.22 (1.67483 vs. 1.67493 × 10⁻²⁷ kg): problems use
  1.675 × 10⁻²⁷ kg.
- **R_H** has no value on the slides, so no problem requires it.
- **Work-function values** in the photoelectric explorer are approximate literature values
  (background); the lecture graph gives only their order.
- **Textbook-internal slips** (Sample Ex. 2.5 silver mass; C = 12.001 u; Li "1 2s¹"):
  logged in COURSE.md. The guide doesn't reuse those examples. Found in Ch. 4: Sample Ex. 4.9 says Ca loses its
  "3s" electrons (they're 4s; noted where the guide cites that example); Fig. 4.12 labels the C=O bond in CO₂
  123 pm, the Table 4.6 average (the measured value is about 116 pm), so no problem depends on it; the summary's
  "element to the left goes first" rule (PDF p.220) conflicts with the book's own dibromine monoxide (PDF p.189).
- **§4.9** is still untaught (not bold on Day 9 p.4); its exam status is unknown.
- **Day 12 and Midterm 1.** Day 12 (MO theory, §18.4–18.5) comes three days before the midterm ("THURSDAY!", Day 12
  p.2); whether it is on the exam isn't stated.
- **NaCl's band gap** is printed as "6.8 × 10⁵ kJ/mol" (PDF p.920), about 7 × 10³ eV per electron; the measured gap
  is about 8.5–9 eV ≈ 8 × 10² kJ/mol (background), so the value is probably J/mol. m25 shows both and tests neither.
- **Ch. 18 band diagrams** in the guide follow the professor's schematic sketch (Day 12 p.24); the cluster energies
  in the m25 explorer come from a simple chain model (background), and the e^(−E_g/2RT) estimate is background.
- **PES binding energies** other than Li and Al come from reference data (background),
  not from the textbook.

## Build status (2026-10-06, after Extension 3 and Day 12)

Every section listed above has a module with teaching stages, an explorer (t1-2 has none by design), problems,
hints, and solutions: 49 modules and 607 problems, 13 of the modules in Ch. 4, 7 in Ch. 5, and 1 (m25) for §18.4–18.5.
A concept-level check (311 concepts drawn from the textbook sections and the lectures; `verification/CurrentCourseGuide/coverage_check.py`
→ `coverage_report.md`) finds each one taught in its own section's module; §4.3's four subsections are checked
separately against m15, m16, m17, and t4-3. Every gradable problem (557) was re-solved blind and agrees with its key.
Checks run: see `VERIFICATION.md`. Working log: `verification/CurrentCourseGuide/BUILD_STATUS.md`.

Still incomplete or deliberately not processed:

- **`/audit-study-guide`** was run on 2026-10-06 for the Extension 3 sections only (at the student's request): the
  seven Ch. 5 modules, the Day 9 rewrites of §4.2 and §4.5–4.8 (with m19 and t4-9), the Ch. 5 explorers, and the
  toolkit's Ch. 5 tables; mixed review x48–x64 got the key checks and blind solving but no line-by-line content
  audit. m25 (§18.4–18.5, added afterward) has the build's checks, a blind re-solve, and its own browser check, but no
  separate content audit. The Ch. 1–4 sections that predate Extension 3 have the build's checks but no audit.
- **End-of-chapter Questions and Problems** (Ch. 1 PDF 72–79, Ch. 2 PDF 109–117, Ch. 3 PDF 168–177, Ch. 4 PDF
  221–231, Ch. 5 PDF 277–285) were not processed as content; all guide problems are new.
- **Photoelectron spectra** for elements other than Li and Al use reference values (background), checked only for
  consistency with IE₁ and Z.

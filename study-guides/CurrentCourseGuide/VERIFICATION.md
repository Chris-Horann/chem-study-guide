# Verification: Chem 1151 study guide (CurrentCourseGuide)

Built 2026-09-24; gap check and re-verification 2026-09-25; extended the same day with Day 8 and the rest of Ch. 4
(§1b below); extended 2026-10-06 with Days 9–11 and all of Ch. 5 (§1c), then the same day with Day 12 and Ch. 18
§18.4–18.5 (§1d). This file records what was checked during
the build and how. The `/audit-study-guide` pass of 2026-10-06 covers the Extension 3 sections only (its own
section at the end); section 8 lists what is still open for the rest of the guide.

Every check can be re-run from the project root:

```
py -3.11 verification/CurrentCourseGuide/build_guide.py        # validates the banks, writes data.js, index.html
node verification/CurrentCourseGuide/test_checker.js           # answer checker + every key round-trip
node verification/CurrentCourseGuide/test_explorers.js         # lecture-explorer physics
node verification/CurrentCourseGuide/test_explorers_preview.js # textbook-preview explorer calculations
node verification/CurrentCourseGuide/test_explorers_ch4.js     # Ch. 4 explorers vs. independent Python values
node verification/CurrentCourseGuide/test_explorers_ch5.js     # Ch. 5 explorers vs. independent Python values (ch5_data.py)
node verification/CurrentCourseGuide/test_explorers_ch18.js    # the §18.4–18.5 band explorer vs. numpy eigenvalues (ch18_data.py)
py -3.11 verification/CurrentCourseGuide/check_bank.py problem_bank_i --modules m20,m21,m22   # one bank + its fragments
py -3.11 verification/CurrentCourseGuide/check_problem_bank_m.py   # (and _h … _l) re-derive each new bank's keys
py -3.11 verification/CurrentCourseGuide/lewis.py              # every Lewis structure: electrons, octets, FC, RDKit
py -3.11 verification/CurrentCourseGuide/coverage_check.py     # concept coverage, per section
py -3.11 verification/CurrentCourseGuide/verify_guide.py --dom <outerHTML dump>   # independent checks
```

`verify_guide.py` writes the full evidence to `verification/CurrentCourseGuide/verification_report.md`.

## Summary

| Check | Method | Result |
|---|---|---|
| Answer keys, independent | 557 gradable problems solved **blind** by solvers who saw only the prompts and answer formats (batches 1–6 on 2026-09-24/25; batches 7–9, the 109 Ch. 4 problems, on 2026-09-25; batches 10–12, the 127 Extension 3 problems, on 2026-10-06; batch 13, the 13 §18.4–18.5 problems, and batch 14, five problems the audit reworded, re-solved the same day) | 557 / 557 agree |
| Answer keys, checker | every key round-tripped through the in-browser checker (`test_checker.js`), including each key rounded to its stated sig figs, every accepted alternative, and every targeted wrong answer ("trap") | 1,550 tests pass; 557 keys round-tripped; 237 traps fire |
| Lewis structures | 126 structures in `lewis.py`: electron total vs. valence count, octets (H: 2) except the declared exceptions, formal charges (Eq. 4.2) summing to the charge, textbook FC values where printed (N₂O, CO₂, NO₂, SO₄²⁻, PO₄³⁻), and an independent RDKit rebuild (formula, charge, SMILES) | all pass |
| Physics reference values | recomputed from first principles with the course constants (`verify_guide.py` §1) | all match |
| Blackbody peak | numerical maximum of Planck's law (scipy, CODATA constants) vs. the explorer's Wien peak | 579.554 nm both |
| Electron configurations | separate aufbau implementation (Madelung order, no exceptions; cations lose highest n first) vs. all 249 explorer entries and the answer keys | all match |
| Data tables | atomic masses vs. `periodictable`; IE₁, EA, successive IEs, and electronegativities vs. Wolfram ElementData (NIST); Table 4.6 (35 bonds) read off the rendered page; outliers re-read on the rendered pages | see §3; no transcription errors |
| Explorer calculations | `test_explorers.js` (91), `test_explorers_preview.js` (82), `test_explorers_ch4.js` (157: naming for all 608 ion pairs and 2,304 covalent cases against a separate Python implementation, formal charges, criteria winners, bond orders, Table 4.6 trends, Lewis symbols byte-for-byte, vibration dipoles), `test_explorers_ch5.js` (384: every VSEPR shape and variant against polyhedra with brute-force lone-pair placement, dipole sums against numpy, hybrid boxes, σ/π counts, all 12 tetrahedral rotations, every MO species and charge, explorer-vs-attempt overlap), `test_explorers_ch18.js` (56: every cluster's levels against numpy eigenvalues, filling, HOMO–LUMO gaps, the 3s/3p overlap onset, the four solids' classes, the background crossing factors, and that the explorer leaves out the attempt's and transfer's material) | 770 tests pass |
| Notation | lint of 50,459 text nodes: index.html, every problem string, and the rendered page with all 51 explorers mounted | 0 findings |
| Concept coverage | 311 concepts from the in-scope textbook sections and lectures (86 added for Day 9 and Ch. 5; 24 for Day 12: 3 in §5.7, 21 in §18.4–18.5), each searched for in its own section's module (`coverage_check.py`); §4.3's four subsections checked against their own modules | 311 / 311 |
| Citations | 5,201 lecture page references within each Day's page count; 1,651 textbook references inside the scope ranges, printed = PDF − 34 | all pass |
| Topic labels | preview problems cite the textbook, lecture problems cite a Day, nothing lecture-labeled inside a preview-only module | all pass |
| Structure | 49 modules, each with an attempt (≥ 4 hints + Compare), ≥ 3 practice, transfer, self-check; 66 mixed; 607 problems; 5,155 unique `data-testid`s in the rendered DOM; no solution text in the static HTML | all pass |
| Chapter 5 data | `verify_guide.py` §8: Table 5.2, the drawn angles (O₃ 117°, NH₃ 107°, H₂O 104.5°, CH₂O 118°, BrF₅ 85°), the Day 10 p.26 table row by row, the MO orders and each species' order, the hybrid presets' electron counts, σ/π presets vs. RDKit, and the four Ch. 5 banks' check scripts | all pass |
| Browser | Chromium at 1280 px and 390 px: all modules and stages, every explorer, answer checking (including traps and Lewis-drawing options), no horizontal overflow at 390 px; 2026-10-06: every stage of all 48 modules visited, 50/50 explorers mount; after Day 12: m25 at 1440, 768, and 390 px, 51/51 explorers mount | no console errors |

## 1. Answer keys

**How the keys were made.** Each numeric key is computed in Python inside the problem banks
(`verification/CurrentCourseGuide/problem_bank_a.py` … `_e.py`) from the course constants in
`guide_common.py`: c = 2.998 × 10⁸ m/s, h = 6.626 × 10⁻³⁴ J·s, Bohr constant 2.178 × 10⁻¹⁸ J,
Balmer 364.56 nm, E_el constant 2.31 × 10⁻¹⁹ J·nm, and N_A = 6.022 × 10²³ mol⁻¹ (a textbook-preview
value). Textbook-preview problems use the textbook's atomic masses. Choice, order, match, text, and
configuration keys were written from the cited pages.

**Blind re-solve.** The 307 gradable problems (31 self-rated items excluded) were exported without
keys, hints, or solutions and split among four independent solvers. They had only the course
conventions and data tables (`verification/CurrentCourseGuide/blind_check/`). They agreed with every
key. The blind pass also flagged these problems, which were then changed:

| Problem | What was wrong or unclear | Change |
|---|---|---|
| x2 | KE = hν − φ was reported as 8.13 × 10⁻²⁰ J; the subtraction rule keeps the 10⁻²¹ J place, so 2 s.f. | key sig figs 3 → 2; the solution explains the rule (textbook §1.7) |
| t1-8-p3 (b) | the solution showed 310.1 K (a binary-rounding artifact) | 310.15 → **310.2 K**, with the round-half-to-even explanation |
| m13-transfer, m6-p3, m13-p6, m14-p3 | lecture problems use N_A, a textbook-preview value, without giving it | the value appears in the preview tag |
| t3-5 problems, x31 | h and mₑ weren't given | stated in each prompt |
| m14-m-sanity | the student's wrong value had the wrong size as well as the wrong sign | now +8.16 × 10⁻¹⁹ J at d = 0.283 nm, so only the sign is wrong |
| t2-6-p2 | the solution mixed average and isotopic masses for a mass-spectrum peak | nominal isotope masses give m/z = 46, as the textbook labels peaks; the average mass 46.07 is explained |
| t1-2-transfer | "which step do you first notice…" could be read as Collect and Organize | the prompt quotes the textbook's Analyze sentence (TB PDF p.42) |
| x29 | "Σ = 0.10" didn't say it was the sum of squared deviations | reworded |
| m15-p4 (AlCl₃) | Δχ = 1.5 is polar covalent by §4.2, yet the item names it as ionic | Connection note: the Day 7 naming rule treats metal + nonmetal as ionic, so the name is unchanged |
| m2-m-match, m4-transfer | slide shortcuts (Millikan "charge and mass"; absorption = emission lines) | short Background notes added; the answers are unchanged |

**Answers given away by the teaching text.** `verify_guide.py` searches each module's own pages for
each attempt, practice, and transfer problem's final answer. Six real give-aways were fixed by
changing the teaching example, not the problem:

- Fe → Ni (the professor's own Day 6 p.21 example) in m10.
- S²⁻ → F⁻ in m11.
- Glucose and H₂O₂ → ethane and butane in t1-6.
- B → Be for successive IEs in m13.
- Li → Al for the PES unit conversion in t3-11.

The sodium excited-state item became a lithium transfer item. Two matches stay, with reasons:

- **m7-attempt:** the neutron's wavelength coincides with the lecture electron's 1.80 × 10⁻¹⁰ m, and the solution says so.
- **m10-preview-exception:** a reading check on the preview box, where the point is the course's policy on exceptions.

## 1b. Chapter 4 extension (2026-09-25)

**What was added.** Ten modules (m16, m17, t4-3, m18, m19, t4-5, t4-6, t4-7, t4-8, t4-9), 119 problems in
`problem_bank_f.py` and `problem_bank_g.py` (including mixed x36–x47), eight explorers in
`assets/explorers_ch4.js`, and Day 8 content in m14 and m15. Two m14 items became lecture items once Day 8
taught their content (the H–H curve, p.11; bonding capacity, p.18); their ids are unchanged.

**Every Lewis structure has one source.** Drawings in problems, solutions, module text, and explorers are
generated at build time from `lewis.py`, which checks each structure (Summary table). Module fragments use
placeholders (`<!--LEWIS:id-->`), so no drawing is typed by hand. Each drawing has a screen-reader description
that names atoms by position ("left O", "central O"). Multiple-choice options use descriptions without the
species' name, so the correct drawing isn't the only one with a proper name.

**Blind re-solve.** The 109 new gradable problems went to three solvers (`blind_check/batch_7–9.json`) with the
ion table, Table 4.3, Table 4.6, the electronegativities, and the course's naming and five-step conventions.
All 109 agreed with the keys. Their notes led to these changes:

| Problem | Note | Change |
|---|---|---|
| all new choice items | 51 of 53 had the correct option first, so "pick the first one" would work | `choice_order.py` rotates each to an MD5-seeded position (now 12/11/9/15 across the four positions of the four-option items); two with a natural order are kept. The solvers' records are kept as `*_asgiven.json` and remapped by `remap_blind_choices.py` |
| m18-p3 | "how many electrons does H need" could mean 1 more | asks for the total once H matches He |
| m17-p4 | "nitric oxide" is a common name | the prompt asks for the systematic name; "nitric oxide" gets its own message |
| t4-8-transfer (b) | "the structure that minimizes formal charges" ties with a two-S=O form on criterion 2 | the prompt names the structure; the solution explains why a second S=O loses on criterion 3 |
| m19-p2 | the "least electronegative atom in the center" shortcut would pick Cl in HOCl | the solution explains the course's bonding-capacity rule and the textbook's tie-breaker |
| m17 items | Stock names such as sulfur(VI) oxide exist in IUPAC naming | feedback says the course's rule requires prefixes, instead of calling the name wrong |
| t4-6-p3 | the unit could be written kJ or kJ/mol (per mole of CH₄) | both accepted |
| t4-7-p3, t4-9-p2, x45 | a distractor that is invalid by electron count; CO₂'s doubly degenerate bend; "name H₂SO₄" | solution notes and a clearer prompt |

**Overlap with the textbook's own examples.** The Ch. 4 problems were compared with §4.3–4.9's Sample
Exercises, Practice Exercises, Concept Tests, and in-text examples. Twenty overlapped and were replaced with new
species: SF₆ → SiF₄, CO → NO, NO₂ → Cl₂O₇, ammonium sulfate → ammonium phosphate, CaF₂ → K₂S, NO₃⁻ → ClO₃⁻
(electron count), CH₂O → HOCl, CO₂ → CS₂ (twice), H₂O₂ → N₂H₄, HBr(aq) → HI(aq), nitrate → acetate (resonance
count), benzene's C–C length → nitrite's N–O energy, the S Concept Test → an N atom, the text's three-bonded O →
a two-bonded Cl, NO → ClO₂, PCl₅ → PF₅, SF₆ → BrF₅, NO₂'s incomplete octet → the general rule, and the N₂/O₂
Concept Test → H₂.

**Overlap with the explorers.** Explorers leave out the species used in their module's attempt and transfer
problems (HCN and C₂H₄ in the five-step explorer; nitrite and formate in the resonance explorer; CO, SCN⁻, SO₃²⁻,
OH⁻, NH₄⁺, and O₃ in the formal-charge explorer; BF₃ and SO₃²⁻ in the octet explorer; HI in the acid explorer).
m18's attempt uses arsenic, which isn't in the Lewis-symbol explorer. `test_explorers_ch4.js` checks all of this.

**Answers printed in the teaching text.** New content put two numbers on a page that holds a problem's answer:
- t4-6's carbonate length, 129 pm, equalled the nitrite length transfer: the transfer now estimates the bond energy (404 kJ/mol).
- m14's new H–H curve shows −436 kJ/mol, which KCl's per-mole E_el (m14-p3) also rounds to. It's a coincidence between different quantities, recorded in `verify_guide.py` REVIEWED_GIVEAWAYS; the m14-p3 solution points it out.

## 1c. Days 9–11 and Chapter 5 (Extension 3, 2026-10-06)

**What was added.** Seven Ch. 5 modules (m20 VSEPR, m21 lone pairs, m22 polarity, m23 hybrid orbitals, m24 σ and π
bonds, t5-6 chirality, t5-7 MO theory; 97 problems in `problem_bank_i.py` … `_k.py`), Day 9 rewrites of t4-2,
t4-5, t4-6, t4-7, t4-8 (now lecture topics with boxed previews; 21 new lecture problems in `problem_bank_h.py`, every
earlier problem relabeled in place with its id unchanged), mixed review x48–x64 (`problem_bank_l.py`), six explorers
(`assets/explorers_ch5.js`: vsepr in two modes, dipoles, hybrid, sigmaPi, chirality, moDiagram), the toolkit's Ch. 5
tables, and the start page's Midterm 1 note. Mixed items x27, x39, x44, and x47 became lecture items (Day 9).

**Keys.** Every key is computed: shapes and angles from `lewis.py` structures and `ch5_data.py`'s polyhedra, MO
fillings from explicit orbital lists, stereocenters from RDKit. Each new bank has its own re-derivation script
(`check_problem_bank_h.py` slide values and RDKit; `_i.py` 165 checks: lone pairs from SMILES, repulsion-minimized
shapes, Δχ vector sums, MMFF geometries; `_j.py` 150 checks: RDKit hybridization and σ/π counts; `_k.py` MO fills in
both 2p orders and two stereocenter methods; `_l.py` RDKit for the mixed items, including UFF geometries for the
polarity items and, because UFF has no Be parameters, RDKit's sp hybridization for BeCl₂).

**Blind re-solve.** The 127 new gradable problems went to three solvers (`blind_check/batch_10–12.json`) with
`course_data_ch5.json` (the Day 10 p.26 table, Table 5.2, Table 5.3, the hybrid rules, the textbook's MO orders).
**127 / 127 agree.** Their notes led to wording changes, no key changes:

| Problem | Note | Change |
|---|---|---|
| m23-attempt (c) | "electrons O puts into its hybrids" is 5 counting O⁺, but 6 if H₃O⁺ is pictured as water + H⁺ | the prompt fixes the convention (O carries the +1); the solution and Compare panel show that both pictures end with one lone pair |
| t5-6-p8 | pseudoephedrine's N also has three different groups | "stereocenters (carbon atoms bonded to four different groups)" |
| t5-7-p10 (b) | 2.5 lone pairs per O assumes the n pair is split between the O atoms | stated in the prompt, as the textbook does for ozone |
| t5-7 attempt, p4, p5 | the prompts said the textbook orders every two-element molecule like NO; it draws only NO | "the order the textbook draws for NO"; a Background note in §5.7 says CO and CN⁻ actually put π₂p below σ₂p, and that these problems' answers are the same in either order (checked for NF, BN⁻, BF, CO⁻, OF, CF, CN⁻) |
| m21-p7 | "bonding pairs 90° from a lone pair, counting for both" could mean distinct pairs | counts lone pair–bonding pair contacts, a pair next to both lone pairs counting twice |
| t4-2-lec-battery | "the H end lines up with the + terminal" reads like alignment in a field | "plays the part of the + terminal" (the slide's analogy) |
| t4-7-tophat | the slide comes before the expanded-octet slides | the solution says the key is ours and that rule 1 alone already picks option 3 |

**Overlap with the textbook.** Each fork compared its problems with Ch. 5's Sample Exercises, Practice Exercises,
Concept Tests, in-text examples, and (Fork B, Fork D) the end-of-chapter Visual Problems and Questions. In these passes
46 items changed (15 in m20–m22, 13 in m23–m24, 16 in t5-6/t5-7, 2 mixed) for textbook overlap, explorer overlap, or
duplication; the textbook cases moved include: the SN/octet and H₂S Concept Tests, nitrate, ammonium, PH₃, H₂S,
ICl₄⁻, ICl₂⁻, the chloromethanes, HCN's polarity, SF₄/XeF₄ (m20–m22); the practice exercise CCl₄/HCN/SO₂/PH₃, HCN,
CO₂, N₂, butadiene, CO₂'s perpendicular π bonds (m23–m24); H₂⁻, B₂, O₂⁺, NO⁺, the Fig. 5.50 molecules, ozone, alanine,
glycine, threonine, CHBrClF, cinnamic acid, ibuprofen (t5-6, t5-7); 2-chlorobutane and N₂⁺/O₂⁺ in the mixed review.
Worked textbook cases stay only as cited teaching content.

**Overlap with the explorers.** As in Ch. 4, no explorer preset is the species of its module's attempt or transfer
problem: m21's attempt moved to BrF₄⁻, m23's to H₃O⁺, m24's to methanimine, t5-7's to NF (O₂ is the MO explorer's
Day 11 p.27 preset), and the VSEPR preset ClF₃ (a Sample Ex. 5.3 practice answer) became the textbook's BrF₃.
`test_explorers_ch5.js` enforces it, with three reviewed passing mentions (the prompts name NH₃/H₂O or NO for
comparison). The dipole, hybrid, chirality, and MO explorers list their results only for the cases the student has
already tried, so their tables don't hand out practice answers.

**Chemistry calls worth knowing.** The dipole explorer sums Δχ-weighted bond vectors: it predicts direction and
cancellation, not size, and it says so (Δχ ranks CCl₃F above CHCl₃; Table 5.2 measures 0.45 vs. 1.01 D). With the
course's χ values P–H has Δχ = 0, so the model would call PH₃ nonpolar (measured ≈ 0.57 D); the explorer leaves PH₃
out and no problem asks it. Xe has no χ in the course table, so XeF₄ is shown as canceling by symmetry. Formic acid's
O–H oxygen is sp³ by the course's steric-number rule; RDKit calls it sp² (conjugation); the σ/π explorer follows the
course and notes the difference.

**Source corrections found while building.** The indexes quoted the textbook's definition of electronegativity in
words it doesn't use; corrected in COURSE.md, COURSE_INDEX.md, and TEXTBOOK_MAP.md to the margin definition, "a
relative measure of an atom's ability to attract electrons to itself within a bond" (TB PDF p.187). The rewritten
§4.8 module had dropped the textbook's "(Z > 12)" (PDF p.214); restored in its preview box.

## 1d. Day 12 and Ch. 18 §18.4–18.5 (2026-10-06)

**What was added.** Day 12 (`Day 12 Lecture Slides 430.pdf`, 25 pages) teaches MO theory (p.6–13) and then the two
Ch. 18 sections its list bolds, §18.4 Metallic Bonds and Conduction Bands and §18.5 Semiconductors (p.14–25). The MO
part was folded into t5-7 by the audit (below). The Ch. 18 part is one new module, **m25** "Metals, bands, and
semiconductors" (unit C18), with a fragment (`src/m25.html`), 12 problems plus mixed review x65–x66
(`problem_bank_m.py`), and a band explorer (`assets/explorers_ch18.js`: "Build a band" with Na, Na₂ … Na₆₄ and a real
crystal, and "Compare solids" with the professor's four band pictures, heating, and P or Ga doping). Textbook §18.4–18.5
(PDF p.918–921, printed 884–887) is the preview box. No other module was reworked (the student's instruction).

| Check | Method | Result |
|---|---|---|
| Keys | `check_problem_bank_m.py`: MO counts from numpy eigenvalues with spin-orbital filling; configurations from `chemistry_verify.py config`; dopant valence electrons from RDKit's periodic table (n-type if more than the host, p-type if fewer); the transfer's λ with pint's CODATA h, c, N_A (1128.6 nm vs. the key's 1128.5 nm) | 20 / 20 checks pass |
| Keys, blind | batch 13 (13 gradable problems), a fresh solver with the Day 12 notes and the textbook's §18.5 values | 13 / 13 agree |
| Explorer | `test_explorers_ch18.js` against `ch18_data.py` (numpy `eigvalsh` of each chain Hamiltonian) | 56 pass |
| Teaching-text numbers | Si's gap 106 kJ/mol ≈ 1.10 eV (the usual 1.12 eV ≈ 108 kJ/mol); donor 4 and acceptor 7 kJ/mol ≈ 0.041 and 0.073 eV; e^(−E_g/2RT) for Si rises 73.5-fold from 25 to 100 °C (the text says "about 70-fold"); diamond 5.47 eV ≈ 528 kJ/mol, factor 3.7 × 10⁻⁴⁷ at 25 °C ("below 10⁻⁴⁶"); NaCl's printed 6.8 × 10⁵ kJ/mol ÷ 96.485 = 7.0 × 10³ eV | Python; all as stated |
| Quotations | every Day 12 quotation checked against the slide renders (p.2, p.7, p.11, p.17–25) and every §18.4–18.5 quotation against PDF p.918–921 (renders viewed, including Figs. 18.25–18.27) | match |
| Browser | m25 at 1440×900, 768×1024, 390×844: every slider stop, all 8 presets, all 24 solid × temperature × doping cases (no NaN; doping forces silicon; another solid resets doping); hint ladders one step at a time, solutions hidden until revealed, Compare gated by the attempt; the transfer accepts 1.13e3, 1130, and 1129 (with a sig-fig note), says "Almost" for 1100, gives targeted messages for 1.13e6 (kJ not converted) and 1.13e-6 (meters), and rejects "abc", "--5", "1e", and empty input | pass; no console errors; no horizontal page overflow |

Fixed during the browser check: the doping levels were drawn on the wrong sides of silicon's narrow gap (the P donor
level looked like it sat above the valence band); the drawn gaps were widened so the donor level sits just below the
conduction band and the acceptor level just above the valence band, as on Day 12 p.25. The compare drawing was made
narrower so its labels stay readable at 390 px. Two readouts were reworded, and a doubled "Connection:" label was removed.

m25 came after the content audit below and has had the checks in this section, not a separate independent content audit.

## 2. Calculations

- **Bohr transitions** (8 transitions; ΔE and λ), **photon energy and frequency** (4), **de Broglie
  wavelengths** (3), **E_el** (3), and **photoelectric KE** (1) all match first-principles
  recomputation.
- **The two lecture routes to hydrogen's lines differ by 0.07%** (n = 3 → 2: Bohr 656.69 nm, Balmer
  656.21 nm).
  - Balmer's 364.56 nm was fit to wavelengths measured in air (Hα is 656.28 nm in air, 656.47 nm in
    vacuum).
  - The Bohr route gives vacuum wavelengths. They come out 0.03% long because 2.178 × 10⁻¹⁸ J rounds
    hcR_H = 2.1787 × 10⁻¹⁸ J down.
  - Every problem states which route it uses, and the tolerance is ≥ 1%.
- **Course hc vs. CODATA:** 0.001% apart, so course-constant answers are also right with exact
  constants.
- **Textbook worked examples** reproduced by the preview explorers:
  - creatinine mean, s, and 95% CI (0.6820, 0.00935, ± 0.0116);
  - the penny Grubbs test (Z = 2.85 > 2.290) and the sodium data (no outlier);
  - Table 1.5 t values to ± 0.002;
  - Table 1.3 conversions and the 2.73 K → −270.42 °C example;
  - molar masses of H₂SO₃ (82.078 g/mol) and CaCO₃ (100.086 g/mol);
  - the Heisenberg baseball (5.46 × 10⁻²⁸ m/s).
- **Ch. 4:** bond orders are computed from the structures' own bond lists: O₃ and NO₂⁻ 1.5, NO₃⁻ and CO₃²⁻ 4/3,
  HCO₂⁻ 1.5, HCO₃⁻ 1 and 1.5, PO₄³⁻ (one P=O) 5/4. The CH₄ C–H energy sum is 4 × 413 = 1652 kJ; nitrite's
  halfway N–O energy is (201 + 607)/2 = 404 kJ/mol. The textbook's own estimates reproduce: PDB/benzene
  (154 + 134)/2 = 144 pm and (348 + 614)/2 = 481 kJ/mol. A 287 K surface peaks at 2.898 × 10⁻³/287 = 10.1 μm
  (Wien, background). Every formal charge in a key comes from Eq. 4.2 in `lewis.py`; the explorer recomputes
  them in JavaScript and gets the same values.

## 3. Data tables

| Table (source) | Compared with | Result |
|---|---|---|
| Atomic masses, 35 (textbook) | `periodictable` (IUPAC) | all within 0.02% |
| IE₁, 42 elements (Day 7 p.9) | Wolfram / NIST | largest difference 0.54% (At) |
| EA₁ (Day 7 p.11) | Wolfram / NIST | all within 2% or 1 kJ/mol except C. Wolfram lists 153.9 kJ/mol, but the modern value, 121.8 kJ/mol (1.2621 eV), supports the slide's −122. |
| Successive IEs (textbook Table 3.2 on Day 7 p.10) | Wolfram / NIST | faithful to the slide (re-read on the render), but the printed table differs from reference values by up to 1.9% (Li IE₃ 12,040 vs. 11,815). The largest jump falls after the same IE for every element, so no answer changes. Logged in COURSE.md → Discrepancies. |
| Electronegativities, 69 (textbook Fig. 4.5) | modern Pauling values | Mo 1.8, W 1.7, Pb 1.9 and Li 1.1 differ from modern tables; each was re-read on the rendered figure (TB PDF p.187), which prints exactly these older values |
| PES, 20 elements (Li, Al textbook; others reference) | IE₁ (Day 7 p.9); Z | outermost peak within 3% of IE₁; peak heights sum to Z |
| Table 4.6, 35 bonds (TB PDF p.207) | read twice off 300-dpi crops; for every atom pair, length falls and energy rises with bond order (`test_explorers_ch4.js`) | no transcription errors; the C=O footnote (799 kJ/mol in CO₂) is carried |
| Polyatomic ions, 26 (Day 8 p.8 = TB Table 4.4) | the slide's table (400-dpi zoom) and the textbook table | identical entries |

## 4. Notation

The lint checks for:
- flattened formulas (H2O for H₂O);
- hyphen-minus used as a minus sign, caret exponents, ASCII arrows, and the letter x as a times sign;
- sign-first charges (Fe⁺³ for Fe³⁺);
- plain-text subscripts (IE1, m_ℓ);
- note labels printed twice.

The first pass over the rendered page found:
- dropdown labels such as "H2O" and "Be2+" (an `<option>` can't hold markup, so these now use Unicode: H₂O, Be²⁺);
- an "m_ℓ -1" tooltip in the quantum-number explorer, now mₗ = −1;
- a "10^8" preset label;
- 18 notes that printed their label twice ("Background (not from lecture): Background: …").

All are fixed.

**Correction (2026-09-25).** Two lint rules added late on 2026-09-24, "plain-text subscripts" and
"label printed twice", contained stray control characters in place of `\b` and could never match.
Their clean results that day were meaningless. Both were repaired, proven on planted examples, and
re-run over the rendered page. They found 12 real issues, all fixed:
- the successive-IE explorer wrote IE1…IE5 (now IE₁…IE₅ in the chart, `<sub>` in the text and table);
- the "What this guide covers" panel showed Z_eff, E_el, R_H, and n_final². The scope-panel converter
  now renders single-letter X_abc as a subscript outside code spans.

The same explorer now opens on Be instead of B, because B's "3 valence electrons" would pre-answer the
m13 attempt about aluminum.

Earlier fixes in the same pass:
- **Electronegativities:** print with the figure's one decimal (Cl 3.0, not 3).
- **Explorer colors:** SVG labels and the visible-spectrum gradient had their colors silently overridden by the stylesheet, which left black-on-black carbon labels and a grey visible band. Both render correctly now, and every atom label has ≥ 4.5 : 1 contrast.
- **Feedback text:** no longer reads "Not yet. Not yet."
- **Stats explorer:** axes use round tick values, and ties for "farthest value" are named.
- **Slider labels:** show the exact preset value (530 nm, not the slider step's 531 nm).

One sanctioned exception is the answer-box instruction "Type subscripts as plain digits: MgCl2 means MgCl₂".

**Ch. 4.** Charges are written magnitude-then-sign (SO₄²⁻, Fe³⁺, Cu⁺) everywhere, including dropdowns
(Unicode) and SVG. Ion drawings carry brackets with the charge outside, as the textbook draws them. Resonance
uses ↔ (never ⇌), with an accessible label. Names accept the slides' spacing "copper (II)" and the textbook's
"copper(II)". Formula answers must use parentheses for repeated polyatomic ions: "NH43PO4" gets its own message.

## 5. Citations, scope, and labels

- Every lecture reference is inside its Day's page count: Day 1 has 20 pages, Day 2 31, Day 3 21, Day 4 18,
  Day 5 20, Day 6 26, Day 7 21, Day 8 30, Day 9 30, Day 10 31, Day 11 27, and Day 12 25.
- Every textbook reference is inside TB PDF 3–9, 36–72, 80–108, 118–168, 178–220, 230–278, or 918–921 (§18.4–18.5). Quotations used in the
  Ch. 4 modules were checked against the rendered pages.
- Every printed page number equals the PDF page minus 34 (also checked in Ch. 18: PDF 918–921 = printed 884–887).
- The scope panel mentions the excluded end-of-chapter pages only as exclusions.
- In preview-only modules, the three sentences that mention the lecture describe its relation to the topic
  (for example, "the lecture hasn't stated a rounding policy"). None claims the professor taught it.

## 6. Browser checks done during the build

Chromium via Playwright over a local HTTP server. Playwright blocks `file://` URLs, so the file wasn't
opened by double-click here. The guide uses only classic scripts, with no `fetch` and no modules, so it
doesn't depend on a server.

- Every stage of all 41 modules, plus mixed review, the toolkit, and the scope panel.
- All 43 explorers mount, with no console errors or warnings. Each Ch. 4 explorer was also looked at in a
  screenshot; label collisions in the bond chart and octet chart, charges wrapping below ion symbols, and the
  small averaged-structure drawing were fixed.
- Ch. 4 checking in the page: a trap answer ("copper(II) sulfide" for Cu₂S) shows its targeted message; the
  slides' spacing is accepted; a Lewis-drawing choice grades; a formal-charge sign error gets its hint.
- At 390 px no Ch. 4 stage or the toolkit scrolls sideways.
- Answer checking: numeric (with units and sig figs), multi-part, configuration, choice, order, match, and text.
- The hint ladder reveals one step at a time. Solutions stay hidden until revealed, and the Compare gate works.
- Progress survives a reload. "Reset progress" clears it after a confirmation.
- At 390 px, the sidebar becomes a menu drawer that opens scrolled to the current section.

## 7. Discrepancies shown to the student

These are recorded in COURSE.md → Discrepancies and noted where they matter in the guide:
- the successive-IE table's small differences from reference values;
- the nucleus-to-atom size (1/10,000 on Day 2 p.19 vs. about 1/29,000 from the figure);
- the Day 2 p.22 neutron-mass typo;
- the edition differences (Ch. 4 numbering; CaS in Table 4.2);
- Li's printed electronegativity (1.1);
- the textbook's internal slips (the Sample Ex. 2.5 silver mass, C printed as 12.001 u, Li "1 2s¹");
- the professor's ionization equation with hν;
- the professor's five steps vs. the textbook's step 5 (the multiple-bond move is shown from the slides' own examples);
- Roman-numeral spacing, and the polyatomic-ion table provided on exams vs. the textbook's "memorize";
- the textbook's Ch. 4 slips: calcium's "3s" electrons (noted where Sample Ex. 4.9 is cited); CO₂'s 123 pm in
  Fig. 4.12 (not used); the naming-order rule vs. dibromine monoxide (the explorer writes halogen oxides with O last);
- Day 11 p.24's Table 5.3 ("Trigonal planar" for sp³ with 3 σ bonds; trigonal pyramidal on Day 10 p.18, p.26 and in
  the textbook), shown in m23 and the toolkit with its slip marked;
- Day 10 p.26's summary table (no SN 5 + 3 lone pairs row although p.23 shows linear; SN 6 + 3 lone pairs as
  T-shaped, which the textbook says isn't met; "ideal" angles that lone pairs shrink), reproduced as printed with notes;
- formaldehyde's "about 118°" (slide and textbook) vs. the measured ≈ 116.5° (background); "Methane only has two
  unpaired electrons" read as carbon's ground state (Day 11 p.11);
- the slides' expanded octets (Day 9 p.29) vs. the textbook's three-center bonds for SN > 4 (§5.7, a labeled preview);
- the textbook's Ch. 5 slips (Sample Ex. 5.9's NO⁻ line, Figs. 5.58–5.59's 3s boxes, the aurora π* sentence,
  "(+) enantiomers" of amino acids, Fig. 5.49's caption), each corrected where the guide uses that material;
- the textbook's §18.5 value for NaCl's band gap, "6.8 × 10⁵ kJ/mol" (≈ 7 × 10³ eV; the measured gap is about
  8.5–9 eV ≈ 8 × 10² kJ/mol, background), shown in m25 with the likely J/mol reading and not tested; Fig. 18.27's
  caption "just above the Si valence electrons" (the valence band).

## 8. Not yet verified (Chapters 1–4 sections that predate Extension 3)

- **Line-by-line review of the teaching text.** This pass verified the keys, calculations, data, notation,
  and citations, but not every explanatory sentence. Read each Learn and Understand stage for chemical
  accuracy, and for any sentence that overstates what the lecture said.
- **Accessibility.** Walk through with the keyboard only and a screen reader, especially the SVG explorers.
  Check forced-colors mode.
- **Other browsers.** Only Chromium was tested. Firefox and Safari still need checking, including
  `localStorage` under `file://`.
- **Double-click use.** Open the guide from `file://` by double-clicking it.
- **Reference-only data.** Photoelectron spectra for elements other than Li and Al are reference values.
  They were checked only for consistency: outermost peak ≈ IE₁, and peak heights sum to Z.
- **Not processed.** End-of-chapter Questions and Problems (Ch. 1 PDF 72–79, Ch. 2 109–117, Ch. 3 168–177,
  Ch. 4 221–231).
- **Ch. 4 judgment calls to review.** The formal-charge explorer operationalizes the textbook's criteria as:
  smallest total |FC|, then most zeros, then negative charge on the more electronegative atom. That's right for
  every set it shows, but it's a reading of qualitative rules. The SCN⁻ transfer and the sulfite transfer rely
  on criterion 3, and their solutions say where real bonding differs. The vibration explorer is a point-charge
  illustration labeled as background. Check the Lewis drawings' screen-reader descriptions with an actual
  screen reader, and the animation with reduced motion switched on (it starts paused).

## Audit 2026-10-06 (Extension 3 sections only)

Run at the student's request on the sections Extension 3 added or rewrote: the seven Ch. 5 modules (m20–m24, t5-6,
t5-7), the Day 9 rewrites of t4-2 and t4-5…t4-8 (with the small m19 and t4-9 edits), the Ch. 5 explorers and the Ch. 4
explorer string edits, the toolkit's Ch. 5 tables, and the start page's Midterm 1 note. Three independent auditors did
the content and chemistry passes (fixing, not just reporting); the UI pass and the integration were done here. The
Ch. 1–4 sections that predate Extension 3, and m25 (§1d), were not part of it.

### Content audit
- scope: about 535 teaching-text claims and 170 problems (m20–m22: ~140 claims, 41 problems; m23, m24, t5-6, t5-7:
  ~225 statements, 56 problems; t4-2, t4-5…t4-8, m19, t4-9: ~170 claims, 73 problems).
- expansions found → action:
  - the textbook's 90° neighbor-counting argument was unattributed in m21-p4(b), m21-p6, and the m21 Explore prompt →
    credited to the textbook (PDF p.241);
  - m22's Recognize list used CH₂O, a textbook-only example → CCl₃F; "smell" in m20 → textbook Fig. 5.1, as Background;
  - t4-5-attempt, t4-5-transfer, and t4-6-attempt, lecture items, asked for a numeric bond order (textbook-only) →
    reworded as the average number of shared pairs per bond (Day 8 p.19–20; Day 9 p.9) with the textbook's term named,
    plus a labeled Connection paragraph in t4-6;
  - t4-8-p5 tests the textbook's rule for where an odd electron goes (PDF p.213) → relabeled preview;
  - t4-2's preview box explained Z<sub>eff</sub> in words the textbook doesn't use → the textbook quoted (PDF p.187),
    the gloss labeled as ours;
  - t5-7 rewritten for Day 12: H₂, H₂⁻, He₂, the 2p MOs, Fig. 5.50's two orders and bond orders, O₂'s circled π*
    electrons, HOMO/LUMO, and "Theories of Bonding" are now lecture text (Day 12 p.6–13); the guidelines,
    "diamagnetic", the 2s–2p mixing reason, ions, NO, auroras, ozone, and SN &gt; 4 stay in the preview box.
    t5-7-p2, p9, m-explain, and m-sanity were relabeled lecture;
  - t5-6: Day 12 p.4 prints §5.6 in grey (noted; the grey key is inferred); "polarimeter", a word the textbook never
    uses, was removed.
- give-aways the automated check can't see (it flags only bold answers with a digit): m23-p5 (its water answers
  were printed in the module) → methanol's O; m24-p3 (diazene, fully worked in the text) → nitrite's N; m24-p7,
  m23-p9, the m24 Recognize list and Explore prompt, and the m20 preview quotation that printed m20-p6(b)'s 121° →
  reworded; the t4-7 Explore prompt now says to open phosphoric acid only after the Top Hat item.
- attribution: "a table … made for the course" (m21 signal) → "a table of its own, not the textbook's Table 5.1";
  "The professor sets H–Cl…" (t4-2), "the professor's Table 4.6" (t4-6), and "The professor draws them himself"
  (t4-8) → descriptions of the slides.
- conventions: ok (steric number and electron domains, "See-saw", the Day 10 p.26 table as printed, the four
  formal-charge steps and four rules word for word, the five steps, bonding capacity).
- provenance spot-checks (rendered pages): Day 9 p.2–30 → ok except p.11 (it has labels), p.13 (signal implied
  bolding), p.14 (three of four boxes show the trend), p.21 and p.24 (quotations), p.27 (duets), p.30 (no FC labels on
  PCl₅/SF₆) → fixed; Day 10 p.1, p.3–31 → ok except p.6 (no smell) and p.15 (the large lobe is ozone's) → fixed;
  Day 11 p.1, p.4–27 → ok except p.7 (an unstated "because") → fixed; the p.20 rules now quoted word for word;
  Day 12 p.2, p.4–13 → ok; Day 3 p.8–12 → p.8–10 (fixed); Day 6 p.16; Day 7 p.7–17; Day 8 p.4–27 → ok; TB PDF
  p.186–219 → ok except p.187 and p.205 (fixed); PDF p.230–274 → ok except p.237 (a quotation that gave away an
  answer), p.240 (Table 5.1's description), and the m23 preview label 246 → 247 (fixed). Every Lecture-signal claim
  was checked against bold text, capitals, red marks, and Top Hat slides.

### Chemistry audit
| Item | Check | Tool | Result | Action |
|---|---|---|---|---|
| Valence electrons, 53 species | recount | `chemistry_verify.py electrons` | all match | — |
| Formal charges: N₂O A/B/C, CO, NO₂, SO₄²⁻ (both), SO₃²⁻, SCN⁻, H₃PO₄ options, PCl₅, SF₆ | rebuilt from independent SMILES | RDKit | match; H₃PO₄ option 1's +1 O confirmed on a zoomed crop | — |
| χ table (29 values), 20 Δχ classes, Table 4.6 sums | vs. the slides | Python | match | — |
| Hybridization and lone pairs (H₃O⁺, methanol O, nitrite N, diazene N) | perception | RDKit | match | m23-p5, m24-p3 species changed (keys unchanged) |
| Stereocenters, 18 molecules | `FindMolChiralCenters` | RDKit | match | — |
| MO filling, 23 species; Li₂–Ne₂ bond orders 1 0 1 2 3 2 1 0; N₂/O₂ HOMO and LUMO | independent filling | Python | match | — |
| SN 6 with 3 lone pairs | enumerate placements | numpy | mer (T-shaped) beats fac | — |
| CF₄ "perfectly opposed" | bond vectors | numpy | no two bonds antiparallel; each cancels the other three | note added in m22 |
| Formate's O–C–O | force field | RDKit MMFF | 131° (VSEPR says about 120°) | background note in m20-p3 |
| TeF₅⁻ and ICl₄⁻ angles | relaxed repulsion model | numpy | 87.2°/89.9°; 90°/180° | keys hold; m21-p9 reworded |
| Background dipole moments | lookup | Wolfram | CH₂F₂ 1.979, CH₃Cl 1.896, CH₃F 1.858, HCl 1.109, PCl₃ 0.56 D | match |
| 1.85 D in C·m | conversion | `chemistry_verify.py units` | 6.18 × 10⁻³⁰ C·m | — |
| Reworded problems | re-solved blind (batch 14) | fresh solver | m21-p9, m23-p5, m24-p3, t4-5-attempt, t4-5-transfer: 5/5 agree | — |

### UI audit
| Feature | Test performed | Result | Fix |
|---|---|---|---|
| Navigation, hint ladders, solution reveals, Compare gate | Playwright on every Extension 3 module | pass | — |
| Answer checking | correct, rounded, wrong-unit, trap, empty, and garbage (`abc`, `1e`, `--5`) entries; order and match items | pass | — |
| Ch. 5 explorers | every control at its limits, all presets, all 49 MO species × charge cases | pass | label collisions, bond z-order, the 109.5° label, the net-dipole arrow, spin arrows, the 2p label, and lobes over atoms fixed during the build |
| Progress | persists across a reload; "Reset progress" clears it after the confirmation | pass | — |
| Overflow | 768 px: the header band; 390 px: match rows, look-alike and data tables | 0 px horizontal page overflow (m19 practice, mixed review, m25) | "Responsive fixes (2026-10-06 audit)" block in style.css |
| Explorers after the audit edits | every module's Explore stage visited | 51 / 51 mount | — |
- viewports: 1440×900, 768×1024, 390×844: no overflow; wide tables scroll inside their own boxes at 390 px.
- console: no errors or warnings.
- file:// compatibility: classic scripts only; no `fetch`, no ES modules, no CDN (checked by grep, including
  `explorers_ch18.js`). Playwright served the files through request routing because the local server was stopped for
  low memory; double-click use still needs a manual check.

### Corrections made
- Fragments: m20, m21, m22, m23, m24, t5-6, t5-7 (rewritten for Day 12), t4-2, t4-5, t4-6, t4-7, t4-8, m19 (a note that
  Day 9 p.30 draws [SO₄]²⁻ with its 2 extra electrons, which matches the textbook's ion rule).
- Banks: `problem_bank_h.py` (t4-5 and t4-6 attempts and transfer reworded, hint ladders of t4-6-attempt and
  t4-8-attempt rewritten, t4-8-p5 relabeled preview), `problem_bank_i.py` (m20-p3, m20-transfer, m21-p4, m21-p6,
  m21-m-explain, m21-p9), `problem_bank_j.py` (m23-p4 quotation; m23-p5 and m24-p3 new species), `problem_bank_k.py`
  (Day 12 citations; four relabels; t5-7-m-sanity's example; t5-6-p6 option). **No answer key changed.**
- Integration: `check_problem_bank_j.py` now tests methanol's O and nitrite's N; the MO explorer's source line and
  presets cite Day 12 p.8–11; `test_explorers_ch5.js` records the t5-7 attempt's mention of the O₂–Ne₂ order as reviewed;
  SOURCE_SCOPE's §4.6 row separates the inferred averaging (Day 9 p.9–10) from the textbook's bond-order definition.

### Unresolved (needs the student or professor)
- Whether MO theory and §18.4–18.5 are on Midterm 1 (Thursday, Day 12 p.2): no coverage list has been supplied.
- Day 11 p.24's "Trigonal planar" for sp³ with 3 σ bonds (shown as printed beside Day 10 p.18, p.26 and the textbook).
- What grey means on the chapter slides (§5.6 on Day 12 p.4); the key is inferred.
- Which textbook edition the course assigns.
- Table 5.2 gives CCl₃F's dipole as pointing toward F (slide and textbook agree; not independently checked).
- The Top Hat items' answer keys are ours; the slides give none.
- Not covered by this audit: the content of mixed review x48–x64 (checked by RDKit re-derivation, blind solving, and
  the lint and citation checks only), m25 (§1d), and the Ch. 1–4 sections that predate Extension 3 (§8).

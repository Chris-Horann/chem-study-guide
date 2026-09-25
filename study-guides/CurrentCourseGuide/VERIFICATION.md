# Verification: Chem 1151 study guide (CurrentCourseGuide)

Built 2026-09-24; gap check and re-verification 2026-09-25; extended the same day with Day 8 and the rest of Ch. 4
(§1b below). This file records what was checked during the build and how. The separate
`/audit-study-guide` pass has **not** been run yet; section 8 lists what it still needs to cover.

Every check can be re-run from the project root:

```
py -3.11 verification/CurrentCourseGuide/build_guide.py        # validates the banks, writes data.js, index.html
node verification/CurrentCourseGuide/test_checker.js           # answer checker + every key round-trip
node verification/CurrentCourseGuide/test_explorers.js         # lecture-explorer physics
node verification/CurrentCourseGuide/test_explorers_preview.js # textbook-preview explorer calculations
node verification/CurrentCourseGuide/test_explorers_ch4.js     # Ch. 4 explorers vs. independent Python values
py -3.11 verification/CurrentCourseGuide/lewis.py              # every Lewis structure: electrons, octets, FC, RDKit
py -3.11 verification/CurrentCourseGuide/coverage_check.py     # concept coverage, per section
py -3.11 verification/CurrentCourseGuide/verify_guide.py --dom <outerHTML dump>   # independent checks
```

`verify_guide.py` writes the full evidence to `verification/CurrentCourseGuide/verification_report.md`.

## Summary

| Check | Method | Result |
|---|---|---|
| Answer keys, independent | 417 gradable problems solved **blind** by solvers who saw only the prompts and answer formats (batches 1–6 on 2026-09-24/25; batches 7–9, the 109 new Ch. 4 problems, on 2026-09-25) | 417 / 417 agree |
| Answer keys, checker | every key round-tripped through the in-browser checker (`test_checker.js`), including each key rounded to its stated sig figs, every accepted alternative, and every targeted wrong answer ("trap") | 1,210 tests pass; 114 traps fire |
| Lewis structures | 66 structures in `lewis.py`: electron total vs. valence count, octets (H: 2) except the §4.8 exceptions, formal charges (Eq. 4.2) summing to the charge, textbook FC values where printed (N₂O, CO₂, NO₂, SO₄²⁻, PO₄³⁻), and an independent RDKit rebuild (formula, charge, SMILES) | all pass |
| Physics reference values | recomputed from first principles with the course constants (`verify_guide.py` §1) | all match |
| Blackbody peak | numerical maximum of Planck's law (scipy, CODATA constants) vs. the explorer's Wien peak | 579.554 nm both |
| Electron configurations | separate aufbau implementation (Madelung order, no exceptions; cations lose highest n first) vs. all 249 explorer entries and the answer keys | all match |
| Data tables | atomic masses vs. `periodictable`; IE₁, EA, successive IEs, and electronegativities vs. Wolfram ElementData (NIST); Table 4.6 (35 bonds) read off the rendered page; outliers re-read on the rendered pages | see §3; no transcription errors |
| Explorer calculations | `test_explorers.js` (91), `test_explorers_preview.js` (82), `test_explorers_ch4.js` (156: naming for all 608 ion pairs and 2,304 covalent cases against a separate Python implementation, formal charges, criteria winners, bond orders, Table 4.6 trends, Lewis symbols byte-for-byte, vibration dipoles) | 329 tests pass |
| Notation | lint of 32,860 text nodes: index.html, every problem string, and the rendered page with all 43 explorers mounted | 0 findings |
| Concept coverage | 201 concepts from the in-scope textbook sections and lectures, each searched for in its own section's module (`coverage_check.py`); §4.3's four subsections checked against their own modules | 201 / 201 |
| Citations | 2,384 lecture page references within each Day's page count; 1,118 textbook references inside the scope ranges, printed = PDF − 34 | all pass |
| Topic labels | preview problems cite the textbook, lecture problems cite a Day, nothing lecture-labeled inside a preview-only module | all pass |
| Structure | 41 modules, each with an attempt (≥ 4 hints + Compare), ≥ 3 practice, transfer, self-check; 47 mixed; 458 problems; 3,770 unique `data-testid`s in the rendered DOM; no solution text in the static HTML | all pass |
| Browser | Chromium at 1280 px and 390 px: all modules and stages, every explorer, answer checking (including traps and Lewis-drawing options), no horizontal overflow at 390 px | no console errors |

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
  Day 5 20, Day 6 26, Day 7 21, and Day 8 30.
- Every textbook reference is inside TB PDF 3–9, 36–72, 80–108, 118–168, or 178–220. Quotations used in the
  Ch. 4 modules were checked against the rendered pages.
- Every printed page number equals the PDF page minus 34.
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
  Fig. 4.12 (not used); the naming-order rule vs. dibromine monoxide (the explorer writes halogen oxides with O last).

## 8. Not yet verified: for `/audit-study-guide`

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

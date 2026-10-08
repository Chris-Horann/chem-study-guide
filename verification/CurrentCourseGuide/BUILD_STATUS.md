# CurrentCourseGuide: build status (resume from here)

Working log for `/build-study-guide` → `study-guides/CurrentCourseGuide/`. Update this
file after every milestone so a stopped session can resume without redoing work.
**Do not regenerate anything marked DONE**; extend it.

Last updated: 2026-10-06

## Requested scope (student, 2026-09-24, supersedes the Days-1–7-only scope)

1. Every section and major concept of Gilbert Ch. 1–3, including topics not yet lectured.
2. Ch. 4 §4.1 and §4.2, plus later Ch. 4 material the lectures cover (§4.3, binary ionic
   compounds of main-group elements only: Day 7 p.18–21).
3. Day 1–7 lectures incorporated with the professor's terminology and methods.
4. Every topic labeled **covered in lecture** or **textbook preview**. Never imply the
   professor taught a textbook-only topic. Nothing beyond these chapters/sections is read.
5. Do NOT run `/audit-study-guide` in this pass.

## Coverage checklist (textbook section → guide module)

Printed page = PDF page − 34 (Ch. 1–4). Status: DONE = module content + problems written;
BANK = problems written, HTML pending; BUILT = teaching stages, explorer, and problems in index.html; READ = textbook section read, nothing written yet;
TODO = not started.

| Section (printed pp.; PDF pp.) | Lecture coverage | Guide module | Status |
|---|---|---|---|
| Ch. 1 opener (2–3; 36–37) | outcomes on Day 1 p.6–7 | Start page | READ |
| §1.1 Exploring the Particulate Nature of Matter (4–7; 38–41) | lecture: Day 1 p.8–14 | m1 | BUILT |
| §1.2 COAST: A Framework for Solving Problems (7–8; 41–42) | preview (greyed, Day 1 p.6) | t1-2 | BUILT |
| §1.3 Classes and Properties of Matter; Separating Mixtures (8–13; 42–47) | preview | t1-3 | BUILT |
| §1.4 States of Matter (13–16; 47–50) | preview | t1-4 | BUILT |
| §1.5 Forms of Energy (16–17; 50–51) | conservation of energy: lecture Day 1 p.15; the rest preview | t1-5 | BUILT |
| §1.6 Formulas and Models (17–19; 51–53) | preview | t1-6 | BUILT |
| §1.7 Expressing Experimental Results (19–26; 53–60) | preview (italic, Day 1 p.6) | t1-7 | BUILT |
| §1.8 Unit Conversions and Dimensional Analysis (26–31; 60–65) | preview (italic) | t1-8 | BUILT |
| §1.9 Analyzing Experimental Results (31–37; 65–71) | preview (greyed) | t1-9 | BUILT |
| Ch. 2 opener (46–47; 80–81) | outcomes on Day 1 p.16–17 | Start page | READ |
| §2.1 Rutherford Model: Electrons; Radioactivity; The Nuclear Atom (48–53; 82–87) | lecture: Day 1 p.16–20, Day 2 p.4–20 (Radioactivity subsection: preview) | m2 (+ preview block) | BUILT |
| §2.2 Nuclides and Their Symbols (53–56; 87–90) | isotopes + particle table: lecture RAMP UP slides Day 2 p.21–23; nuclide symbols preview | t2-2 | BUILT |
| §2.3 Navigating the Periodic Table (56–60; 90–94) | basics: lecture RAMP UP Day 2 p.24; rest preview | t2-3 | BUILT |
| §2.4 The Masses of Atoms, Ions, and Molecules (60–64; 94–98) | amu: lecture RAMP UP Day 2 p.21; rest preview | t2-4 | BUILT |
| §2.5 Moles and Molar Masses (64–70; 98–104) | preview | t2-5 | BUILT |
| §2.6 Mass Spectrometry (70–74; 104–108) | preview (greyed) | t2-6 | BUILT |
| Ch. 3 opener (84–85; 118–119) | outcomes Day 2 p.26, Day 3 p.6 | Start page | READ |
| §3.1 Nature's Fireworks and the EM Spectrum (86–89; 120–123) | lecture | m3 | BUILT |
| §3.2 Atomic Spectra (89–90; 123–124) | lecture | m4 | BUILT |
| §3.3 Particles of Light: Quantum Theory (90–95; 124–129) | lecture | m5 | BUILT |
| §3.4 The Hydrogen Spectrum and the Bohr Model (95–100; 129–134) | lecture | m6 | BUILT |
| §3.5 Electrons as Waves: De Broglie (100–103; 134–137) | lecture | m7 | BUILT |
| §3.5 Electrons as Waves: Heisenberg Uncertainty Principle (103–104; 137–138) | preview | t3-5 | BUILT |
| §3.6 Quantum Numbers (104–108; 138–142) | lecture | m8 | BUILT |
| §3.7 The Sizes and Shapes of Atomic Orbitals (108–111; 142–145) | lecture | m9 | BUILT |
| §3.8 The Periodic Table and Filling Orbitals (111–119; 145–153) | lecture (exceptions Cr/Cu: preview; "we will completely ignore this", Day 7 p.6) | m10 (+ preview block) | BUILT |
| §3.9 Electron Configurations of Ions (119–122; 153–156) | lecture | m11 | BUILT |
| §3.10 The Sizes of Atoms and Ions (122–125; 156–159) | lecture | m12 | BUILT |
| §3.11 Ionization Energies (125–128; 159–162) | lecture | m13 | BUILT |
| §3.11 Photoelectron Spectroscopy (128–130; 162–164) | preview | t3-11 | BUILT |
| §3.12 Electron Affinities (130–133; 164–167) | lecture | m13 | BUILT |
| Ch. 4 opener (144–145; 178–179) | outcomes Day 7 p.12–13 | Start page | READ |
| §4.1 Chemical Bonds and Greenhouse Gases (146–151; 180–185) | lecture (bond types, E_el, lattices); greenhouse-gas material preview | m14 (+ preview block) | BUILT |
| §4.2 Electronegativity, Unequal Sharing, and Polar Bonds (151–154; 185–188) | preview (listed Day 7 p.12, not yet lectured) | t4-2 | BUILT |
| §4.3 Binary Ionic Compounds of Main Group Elements (155–156; 189–190) | lecture Day 7 p.18–21 | m15 | BUILT |
| §4.3 other subsections (molecular, transition-metal, polyatomic, acids) | not lectured, not in scope | — | excluded |
| End-of-chapter Questions and Problems | — | not reproduced (all guide problems are new) | excluded |

## Build artifacts

| Artifact | Status | Notes |
|---|---|---|
| `verification/CurrentCourseGuide/guide_common.py` | DONE | constants, lecture data tables, config rules, HTML helpers |
| `problem_bank_a.py` (m1–m8), `problem_bank_b.py` (m9–m15, Top Hat, mixed x1–x20) | DONE | 168 problems, keys computed |
| `build_guide.py` | DONE (31 modules by chapter/section; labels; periodic table, molecules, PES, EN data) | validates bank, writes data.js, scope.js, assembles index.html from `src/` |
| `assets/checker.js` + `test_checker.js` | DONE | 740 tests pass (307 keys round-trip, incl. keys rounded to their stated sig figs) |
| `assets/app.js` | DONE | routing, stages (flexible sets; t1-2 has no Explore), problems, progress, label pills, chapter-grouped dashboard, `compactState()` storage pruning |
| `assets/explorers.js` + `test_explorers.js` | DONE for lecture modules (17 explorers); helpers exposed as Explorers.ui | 91 tests pass |
| `assets/explorers_preview.js` + `test_explorers_preview.js` | DONE | 15 preview explorers: particleBox, states, kinetic, models, sigfigs, units, stats, nuclide, ptable, isotopes, moles, massSpec, heisenberg, pes, polarity; 82 tests pass |
| `assets/style.css` | DONE | |
| `src/*.html` fragments → `index.html` | DONE | all 37 fragments written (head, start, 31 modules, mixed, toolkit, scope, foot); index.html assembles. Module headers are generated by build_guide.py from MODULES. |
| Preview problem banks `problem_bank_c.py` (Ch. 1), `_d.py` (Ch. 2), `_e.py` (Ch. 3–4 + mixed x21–x35) | DONE | 338 problems total validate; checker 740 tests pass |
| `verify_guide.py` + `verification_report.md` + `blind_check/` | DONE | physics, configs, data tables vs. NIST/IUPAC, blind key comparison (307/307), notation lint incl. rendered DOM, citations, structure; 0 failures |
| `SOURCE_SCOPE.md` | DONE | incomplete list filled in (2026-09-24) |
| `VERIFICATION.md` | DONE | summary of every check; §8 lists what the audit still needs |
| COURSE.md registry row + student note; TEXTBOOK_MAP rows; SOURCE_MANIFEST pages | DONE | registry row added (not audited); successive-IE discrepancy row extended |

## Next steps (in order)

1. DONE: textbook preview sections read (text + renders of notation-heavy pages); findings in `materials/TEXTBOOK_MAP.md` → Textbook preview notes; manifest marked (PDF 3–9, 36–73, 80–110, 118–168, 178–190); textbook slips logged in COURSE.md.
2. DONE: `SOURCE_SCOPE.md` rewritten for the new scope.
3. DONE: preview problem banks written and validated.
4. DONE: `style.css`, `src/` fragments, preview explorers; browser smoke + interaction test passed (all 31 modules, all explorers mount, no console errors).
4a. DONE: visual review (desktop and 390 px; explorers; feedback; solution; menu; reset). Fixes: SVG fill overrides, label contrast, χ decimals, stats ticks, slider labels, duplicate feedback text, focus ring on headings.
5. DONE: `verify_guide.py` (blind re-solve 307/307; 6 answer give-aways fixed; notation, citation, and test-id fixes), node tests (740 + 91 + 82), `VERIFICATION.md`, registry.
5a. DONE 2026-09-25 (same request re-issued): inspected files and manifest; `coverage_check.py` concept checklist (143 concepts; 1 gap: §4.1 "valence" = bonding capacity → m14 preview paragraph + `m14-preview-valence`, blind-checked); repaired two lint rules that never fired and fixed the 12 findings; successive-IE explorer defaults to Be. Manifest shows `Day 8 Lecture Slides.pdf` as NEW: not ingested, not used (scope is Days 1–7).
6. NEXT (not run in this build, by request): `/audit-study-guide`. Re-run `verify_guide.py --dom <dump>` after any change; see VERIFICATION.md §8.

## Extension 2: Day 8 + all remaining Ch. 4 (requested 2026-09-25)

Request: add Day 8 and every remaining section of Gilbert Ch. 4; keep Days 1–7 and Ch. 1–3 content;
label each topic covered in lecture / textbook preview; update navigation and SOURCE_SCOPE.md; check
chemistry and answers; do NOT run `/audit-study-guide`.

Ch. 4 in the supplied 3rd ed. (printed = PDF − 34). The slides' Ch. 4 list numbers 4.5 and 4.6 the other
way round (Day 8 p.4): slides 4.5 = Lengths and Strengths, 4.6 = Resonance.

| Section (printed; PDF) | Lecture coverage (Days 1–8) | Module | Status |
|---|---|---|---|
| §4.1 Chemical Bonds and Greenhouse Gases (146–151; 180–185) | lecture Day 7 p.12–17; Day 8 p.11 (H–H curve), p.14–15 (metallic, Table 4.1), p.18 (bonding capacity) | m14 (Day 8 items moved into lecture content; 2 items relabeled lecture, ids kept) | DONE |
| §4.2 Electronegativity, Unequal Sharing, and Polar Bonds (151–154; 185–188) | preview (announced Day 8 p.26) | t4-2 | DONE (Day 8 p.4, p.26 notes) |
| §4.3 Binary Molecular Compounds (154–155; 188–189) | lecture Day 8 p.12–13 | m17 | DONE |
| §4.3 Binary Ionic Compounds of Main Group Elements (155–156; 189–190) | lecture Day 7 p.18–21; Day 8 p.6 | m15 | DONE (Day 8 p.6) |
| §4.3 Binary Ionic Compounds of Transition Metals (156–157; 190–191) | lecture Day 8 p.7, p.10 | m16 | DONE |
| §4.3 Polyatomic Ions (157–159; 191–193) | lecture Day 8 p.8–9 | m16 | DONE |
| §4.3 Binary Acids; Oxoacids (159–161; 193–195) | preview | t4-3 | DONE |
| §4.4 Lewis Symbols and Lewis Structures (161–168; 195–202) | lecture Day 8 p.16–26, p.28–30 | m18, m19 | DONE |
| §4.5 Resonance (168–172; 202–206) | allotropes and O₃'s two structures: lecture Day 8 p.26–30; resonance itself: preview | t4-5 (L+P) | DONE |
| §4.6 The Lengths and Strengths of Covalent Bonds (172–174; 206–208) | preview (bold on Day 8 p.4; H–H curve Day 8 p.11 is the lecture link) | t4-6 | DONE |
| §4.7 Formal Charge: Choosing among Lewis Structures (174–178; 208–212) | preview (announced Day 8 p.26) | t4-7 | DONE |
| §4.8 Exceptions to the Octet Rule (178–183; 212–217) | preview ("Sometimes it is impossible for every atom to have an octet", Day 8 p.26) | t4-8 | DONE |
| §4.9 Vibrating Bonds and the Greenhouse Effect (183–185; 217–219) | preview | t4-9 | DONE |
| Ch. 4 Summary, Problem-Solving Summary (185–186; 219–220) | — | completeness check (coverage_check.py) | DONE |
| Ch. 4 Visual Problems, Questions and Problems (187–; 221–231) | — | not reproduced (all problems new) | excluded |

Finished 2026-09-25. New files: `problem_bank_f.py`, `problem_bank_g.py`, `lewis.py` (structures, checks,
renderer), `ch4_data.py` (explorer data + Python reference answers), `choice_order.py`, `make_blind_batches.py`,
`remap_blind_choices.py`, `test_explorers_ch4.js`, `assets/explorers_ch4.js`, `src/m16.html` … `src/t4-9.html`.
Results: build OK (41 modules, 458 problems); node tests 1,210 + 91 + 82 + 156 pass; `lewis.py` errors: none;
blind 417/417; `verify_guide.py --dom`: 0 failures, 0 warnings; coverage 201/201; browser pass at 1280 and 390 px.
Details in the guide's VERIFICATION.md §1b. Not run, by request: `/audit-study-guide`.

## Extension 3: Days 9–11 + all of Ch. 5 (2026-10-06)

Request: `/ingest-course` "Put three new lecture slides cover all of chapter 5 as well from the book" (2026-10-05,
done), then `/build-study-guide` with no arguments and "keep going". Read as: add Days 9–11 and every Ch. 5 section
(material ahead of the lectures labeled textbook preview); relabel the Ch. 4 sections Day 9 teaches; keep every
module, problem id, and the progress key. The build skill's last step, `/audit-study-guide`, runs after the build.

| Section (printed; PDF) | Lecture coverage | Module | Status |
|---|---|---|---|
| §4.2 (151–154; 185–188) | Day 9 p.15–18; Day 10 p.27 | t4-2 (now L+P) | DONE (Fork A) |
| §4.5 (168–172; 202–206) | Day 8 p.26–30; Day 9 p.6–13 | t4-5 (L+P) | DONE (Fork A) |
| §4.6 (172–174; 206–208) | Day 8 p.11; Day 9 p.7, p.14 | t4-6 (now L+P) | DONE (Fork A) |
| §4.7 (174–178; 208–212) | Day 9 p.19–26 | t4-7 (now L+P) | DONE (Fork A) |
| §4.8 (178–183; 212–217) | Day 9 p.27–30 | t4-8 (now L+P) | DONE (Fork A) |
| §4.9 (183–185; 217–219) | not taught | t4-9 (P) | source line updated |
| §5.1–5.2, no lone pairs (198–203; 232–237) | Day 10 p.3, p.6–13 | m20 | DONE (Fork B) |
| §5.2, lone pairs (203–209; 237–243) | Day 10 p.14–26 | m21 | DONE (Fork B) |
| §5.3 (209–212; 243–246) | Day 10 p.27–31; Day 11 p.6–8 | m22 | DONE (Fork B) |
| §5.4 (213–219; 247–253) | Day 11 p.9–16, p.20, p.24 | m23 | DONE (Fork C) |
| §5.4–5.5 (217–221; 251–255) | Day 11 p.17–26 | m24 | DONE (Fork C) |
| §5.6 (221–227; 255–261) | Day 10 p.3, p.6 (hook) | t5-6 (mostly P) | DONE (Fork D) |
| §5.7 (227–239; 261–273) | Day 11 p.27 (hook) | t5-7 (mostly P) | DONE (Fork D) |
| Ch. 5 Summary etc. (240–242; 274–276) | — | completeness check | DONE |
| Ch. 5 Questions and Problems (243–251; 277–285) | — | not reproduced | excluded |

How it was built: four forks wrote the module content in parallel from a common brief
(`EXT3_BRIEF.md` in this folder: file ownership, problem and fragment conventions, notation, labels, explorer specs), each
owning its own files. Infrastructure first: `modules_def.py` (units, modules, labels), `bank_validate.py`,
`fragments.py`, `check_bank.py` (validate one bank and its fragments without a full build). The integrator wrote
the Ch. 5 explorers (`assets/explorers_ch5.js`, data in `ch5_data.py`, tests in `test_explorers_ch5.js`), the mixed
review x48–x64 (`problem_bank_l.py`, keys re-derived by `check_problem_bank_l.py`), the toolkit's Ch. 5 tables, the
start page, SOURCE_SCOPE.md, and the Ch. 5 checks in `verify_guide.py` (§8) and `coverage_check.py`.

New files: `problem_bank_h.py` (Day 9 lecture items for t4-2…t4-8), `problem_bank_i.py` (m20–m22), `problem_bank_j.py`
(m23–m24), `problem_bank_k.py` (t5-6, t5-7), `problem_bank_l.py` (mixed), `check_problem_bank_h…l.py`, `ch5_data.py`,
`modules_def.py`, `bank_validate.py`, `fragments.py`, `check_bank.py`, `test_explorers_ch5.js`,
`drawings/o3_svgs.py` (the two hand-built ozone drawings in t4-5), `src/m20.html` … `src/t5-7.html`.

Interruption 2026-10-06: all four forks stopped on a usage limit and were resumed from their transcripts; the
local preview server was stopped by the system for low memory and not restarted (browser checks serve the files
through Playwright request routing instead).

Results (final build, 2026-10-06, after the audit and Day 12): build OK (49 modules, 607 problems, 66 mixed);
`check_bank.py` no findings for banks f–m; `check_problem_bank_h…m.py` all pass; `lewis.py` 126 structures, errors none;
node tests 1,550 + 91 + 82 + 157 + 384 + 56, all pass; `coverage_check.py` 311/311; `verify_guide.py --dom` (all 51
explorers mounted) 0 failures, 0 warnings; blind record 557/557 agree (batches 1–14). The audit (Extension 3 sections
only) and its fixes are in the guide's VERIFICATION.md, "Audit 2026-10-06"; the three auditors were also stopped
once by a usage limit and resumed.

## Day 12 + Ch. 18 §18.4–18.5 (2026-10-06)

Student: "I also added day 12 lecture and also put down notes for 18.4-18.5, do this quick and just do these things,
dont try to go through all of the other modules". Done:
- Ingested `Day 12 Lecture Slides 430.pdf` (25 pages, all viewed): COURSE_INDEX (MO theory now taught; new Unit F:
  metals, band theory, semiconductors and doping), COURSE.md (lecture row, announcements, bolding, terminology,
  conventions, the NaCl band-gap discrepancy), COURSE_MAP (unit, chain 12, 8 edges, diagram), TEXTBOOK_MAP (§18.4–18.5
  rows, Ch. 18 offset = 34 checked on four renders, notes); manifest: Day 12 ingested, textbook pages 902, 917–923 mapped.
- Guide: unit C18 with module m25 (`src/m25.html`, `problem_bank_m.py` + `check_problem_bank_m.py`, explorer
  `assets/explorers_ch18.js` + `ch18_data.py` + `test_explorers_ch18.js`), mixed x65–x66; t5-7's Day 12 MO content went
  in through the audit; header, start page, and SOURCE_SCOPE updated. No other module was reworked.



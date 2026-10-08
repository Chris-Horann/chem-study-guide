# Extension 3 of CurrentCourseGuide: common brief for every fork

You are one of four forks writing content for `study-guides/CurrentCourseGuide/` (Day 9–11 lectures + all of
Gilbert Ch. 5). The parent (integrator) has already set up the infrastructure. All paths below are relative to
`C:\Users\chris\ChemStudy\verification\CurrentCourseGuide\` unless they start with `study-guides/`.
Run Python as `py -3.11` with `export PYTHONIOENCODING=utf-8`. Today is 2026-10-06.

## What already exists (don't change these files)
- `modules_def.py`: all modules, labels, sources, prerequisites. New Ch. 5 modules: m20 (§5.1–5.2), m21 (§5.2 lone
  pairs), m22 (§5.3), m23 (§5.4), m24 (§5.4–5.5), t5-6 (§5.6), t5-7 (§5.7), all labeled "lecture+preview".
  The Ch. 4 modules t4-2, t4-5, t4-6, t4-7, t4-8 are now "lecture+preview" (taught Day 9); t4-9 stays "preview".
- `bank_validate.py`, `fragments.py`, `check_bank.py`, `build_guide.py`, `verify_guide.py`, `app.js`,
  `checker.js`, `style.css`, `ch5_data.py` / `explorers_ch5.js` (the integrator writes the Ch. 5 explorers).
- `lewis.py`: 101 checked structures. Ids you can use (besides the Ch. 4 ones already listed in the file):
  AlCl3, BCl3, H3PO4-t1, H3PO4-t2, H3PO4-t3 (Day 9 p.26 Top Hat structures 1–3), CCl4, CF4, PF5, SF4, SCl4, ClF3,
  BrF3, XeF2, XeF4, IF5, I3-, ICl4-, SO2-1, SO2-2 (octet resonance pair), SO2-exp (O=S=O), CH2Cl2, CCl3F, CH3Cl, HF,
  H2S, OF2, NF3, PH3, H3O+, N2H2 (trans diazene), acrolein, CH3CN, allene, C2H6, HCOOH; and from Ch. 4: F2, O2, N2,
  NH3, C2H2, O3a, O3b, CH4, H2O, CHCl3, OH-, NH4+, H2O2, CH2O, CO2, HCN, PCl3, CO, NO3-1/2/3, CO3-1/2/3, NO2-1/2,
  N2O-A/B/C, CO2-alt1/alt2, NO2+, SCN-a/b/c, BF3, BeCl2, NO, NO2-rad1/2, PCl5, SF6, SO4-oct, SO4-exp, PO4-oct,
  PO4-exp, H2SO4, HCO2-1/2, C2H4, CH3OH, SO3-oct, SO3-exp, Cl-ion, S2-ion, HOCl, CS2, CS2-alt, N2H4, BrF5,
  HCO3-1/2, CH3COO-1/2, C6H6-1/2.
  If you need another *checked* structure, add it ONLY inside your own block in `lewis.py` (between
  `# ==== block X ... start` and `# ==== block X end`), using `add(S(...))` or `_star(...)` like the lines above it;
  put its id in `NON_OCTET_EXTRA` if its octets are deliberately incomplete and an independent expectation in
  `EXPECT_EXTRA[id] = (smiles_or_None, fc_list_or_None)`. Then run `py -3.11 lewis.py` (must print `errors: none`).
  Wrong structures for multiple-choice options are drawn ad hoc with `LX(name, atoms, bonds, lp, charge=0, neutral=True)`
  (see problem_bank_f.py), never added to STRUCTS.

## Files you own
Only the files named in your own brief. Never edit another fork's files. If you think a shared file needs a
change (an explorer feature, a CSS class), say so in your final report instead of editing it.

## Problem conventions (follow problem_bank_g.py exactly)
- Helpers: `add(...)` (label derived from the module: lecture unless the module is "preview"), `P(...)` (label
  "preview"; must cite the textbook via `tb(sec, pdf_from, pdf_to)`), `choice(...)`, `num_ans`, `tnum`,
  `order_ans`, `text_ans`, `formula_ans`, `LS(id, scale=..., neutral=True)` (inline checked drawing), `LX(...)`.
  A problem may set `label="lecture"` or `label="preview"` explicitly. A lecture-labeled problem MUST cite
  "Day N p.X"; a preview one MUST cite "textbook §…, PDF p.…". Label by what the problem tests: a lecture idea
  → lecture (cite the slide; add the textbook page too if you used it); a textbook-only idea → preview.
- ids: `<mod>-attempt`, `<mod>-p1`…, `<mod>-transfer`, `<mod>-m-explain` (answer type "self" with a `model`),
  `<mod>-m-recognize`, `<mod>-m-sanity`; extra items `<mod>-p7`, `<mod>-lec-…`, `<mod>-tophat` etc. Lowercase,
  digits, hyphens only.
- Per module: exactly ONE attempt (≥ 4 hints forming a ladder: concept → relationship → setup → near-complete
  setup; plus `compare={"wrong": "<p>…</p>", "tempting": "…", "fails": "…"}`), at least 3 practice (aim for 6–8,
  graded Warm-up → Concept → Standard → Stretch), at least 1 transfer, and mastery items: one self-rated explain,
  one recognize, one sanity check. numeric/multi problems need ≥ 2 hints, others ≥ 1.
- Every choice option needs feedback; distractors must come from real misconceptions, and their feedback says
  why the idea is tempting or where it breaks.
- Keys are computed in Python where there is arithmetic (bond orders from `lewis.py` structures, electron counts
  from `s.total_valence()`, formal charges from `s.fcs()`, angles from geometry). Don't hand-type a computed number.
- `level` strings in use (keep to these): "Guided attempt", "Warm-up", "Concept", "Standard", "Stretch",
  "Transfer", "Explain", "Recognize", "Sanity check", "Textbook preview", "In-class Top Hat" (for problems built
  on a slide's Top Hat question).
- Solutions: full reasoning, units carried, the professor's method first; mention a textbook alternative as
  such. Never post homework answers (no homework has been supplied; Top Hat slide questions are lecture material
  and may be used, with our reference answer clearly ours since the slides give none).
- The checker accepts: numeric (±tol), choice, multi (parts), order (ranks), match (rows → option keys), text
  (accepted list; `kind="formula"` compares element counts), self (model answer). Prefer choice/order/match/multi
  for qualitative chemistry (shape names, polar/nonpolar, hybridization); use text answers only with a generous
  accepted list (e.g., ["sp3", "sp^3", "sp³"]).

## Fragment conventions (copy the structure of src/t4-5.html and src/m19.html)
- No `<h1>` (the header is generated). Stage divs in this order: learn, understand, explore, attempt, compare,
  practice, master, each `<div class="stage" data-stage="…"><h2>…</h2>…</div>`.
- Learn: `<p class="big-idea">`, a `<div class="triad">` with three `.rep` boxes (rep-observe "What we observe",
  rep-write "What we write", rep-particles "What the particles are doing" / "What the electrons are doing"), and
  `<p class="source">Source: Day 10 p.8–12.</p>`.
- Understand: `<div class="eqcard">` (an `.eq` line, a `<dl>` of terms, `.use` paragraphs), worked lecture
  examples, a `<table class="lookalike">` when two ideas are easy to confuse, `<div class="recognize">` with a
  "Recognize it" list, `<aside class="signal"><span class="signal-label">Lecture signal</span>…</aside>` ONLY with
  evidence (bold on the slide, repetition across slides/lectures, Top Hat, an explicit instruction), and textbook-only
  material inside `<div class="preview-box"><span class="preview-label">Textbook preview (§5.2, PDF p.238–243,
  printed 204–209)</span>…</div>`. Use `<p class="bg">` for outside knowledge ("Background (not from lecture)" is
  printed by CSS: don't write the label yourself), `<p class="connection">` for links the guide infers, `<p class="note">`.
- Explore: a short predict-first prompt that matches the explorer's real features (specs below), then
  `<div class="explorer" data-explorer="NAME"></div>` (add `data-mode="…"` where the spec says so).
- Attempt/practice/master: `<div class="slot" data-module="ID" data-kinds="attempt|practice|transfer mastery"></div>`.
  Compare: `<div class="compare-slot" data-compare="ID"></div>` + `<h3>Common mistakes</h3><ul class="mistakes">…`.
  Master ends with `<h3>Can you…?</h3><ul class="cando" data-module="ID"><li data-key="…">…</li>…</ul>` (3–4 items).
- Lewis drawings in fragments: `<!--LEWIS:id:scale=0.8-->`, `<!--LEWIS:id:fc:scale=0.7:cap=A-->`,
  `<!--HYBRID:id1,id2:scale=0.7-->`, inside `<p class="lw-row">…</p>`; resonance arrow
  `<span class="lw-arrow" role="img" aria-label="resonance arrow">↔</span>`.
- Cite every block: slides as "Day 10 p.14–15"; textbook as "PDF p.240" or "textbook §5.2, PDF p.240 (printed 206)"
  (printed = PDF − 34). Ch. 5 is PDF 230–278; pages outside the guide's scope fail the citation check.

## Notation (lint-enforced; a notation error is a chemistry error)
- Formulas with `<sub>`: SF<sub>4</sub>, never SF4 in visible text. Charges magnitude-then-sign in `<sup>`:
  SO<sub>4</sub><sup>2−</sup>, I<sub>3</sub><sup>−</sup>, H<sub>3</sub>O<sup>+</sup>. Use the Unicode minus (−) for
  negative numbers and charges, × for multiplication, °, →, ↔ (resonance), ⇌ (equilibrium). No ASCII arrows (->),
  no caret exponents, no letter x as a times sign. Hybrids: sp<sup>3</sup>, sp<sup>2</sup>, sp. Greek σ, π, δ+, δ−, χ, Δχ, μ.
- MO labels: σ<sub>2s</sub>, σ*<sub>2s</sub>, π<sub>2p</sub>, π*<sub>2p</sub>, σ<sub>2p</sub>, σ*<sub>2p</sub>
  (write the star as a plain asterisk before the subscript, as the textbook does).

## Labels and honesty
- Teach the professor's version first, in the professor's words (quote slides); explain where the textbook differs.
- Never say or imply the professor said, taught, or emphasized textbook-only content. Lecture content cites a slide.
- Known slide/textbook issues you must handle as recorded in COURSE.md → Discrepancies (show both, don't "fix"
  silently): Day 11 p.24's Table 5.3 says "Trigonal planar" for sp³ with 3 σ bonds (correct: trigonal pyramidal,
  Day 10 p.18, p.26; textbook Table 5.3 PDF p.252); Day 10 p.26's table omits SN 5 + 3 lone pairs (linear, shown on
  Day 10 p.23) and lists SN 6 + 3 lone pairs as T-shaped (textbook: "possible… we will not encounter any molecules
  with them", PDF p.240); formaldehyde H–C–H "about 118°" (slide = textbook's implication; measured ≈ 116.5°,
  background); "Methane only has two unpaired electrons" means carbon's ground state (Day 11 p.11); the Ch. 5
  outcome list differs from the book's (no chirality outcome; a greenhouse outcome that is the book's §4.9);
  textbook slips in Ch. 5 (Sample Ex. 5.9 NO⁻ typo; Fig. 5.58/5.59 box diagrams; aurora π* sentence; "(+)
  enantiomers" for amino acids).
- Scope statements on the slides: delocalization's stabilization "beyond the scope of this class" (Day 9 p.10);
  hypervalency "not well understood" (Day 9 p.29); MO theory "briefly" (Day 11 p.27). Respect them.

## Explorer specs (Explore prompts must match what these will do)
- `vsepr` with `data-mode="bonds"` (m20) or `data-mode="lone"` (m21): choose SN 2–6 (and, in "lone" mode, 0–3 lone
  pairs where possible: SN 3 ≤ 1, SN 4 ≤ 2, SN 5 ≤ 3, SN 6 ≤ 3); a rotatable 3-D ball-and-stick view (yaw/pitch
  sliders), a "show lone pairs" toggle (electron-pair vs molecular geometry), the electron-pair and molecular geometry
  names, ideal angles, and presets with sources: bonds mode CO₂, BF₃, CCl₄, PF₅, SF₆ (Day 10 p.10–12), CH₂O
  (Day 10 p.13, about 118°); lone mode O₃ (117°), NH₃ (107°), H₂O (104.5°) from Day 10 p.14–19, plus SF₄, ClF₃,
  XeF₂, BrF₅, XeF₄, SO₂, I₃⁻ (textbook/new). For SN 5 a "put one lone pair axial instead" toggle counts 90° lone-pair
  neighbors (3 axial vs 2 equatorial); for SN 6 with 2 lone pairs an "adjacent vs opposite" toggle counts 90°
  lone-pair–lone-pair contacts. Names used: linear, trigonal planar, tetrahedral, trigonal bipyramidal, octahedral;
  bent (angular), trigonal pyramidal, seesaw, T-shaped, square pyramidal, square planar.
- `dipoles` (m22): molecule presets (lecture CO₂, CF₄, H₂O; Table 5.2 HF, H₂O, NH₃, CHCl₃, CCl₃F; plus BF₃, NF₃, CH₂O,
  SO₂, CH₂Cl₂, CCl₄, CH₃Cl, H₂S, OF₂, HCN, PCl₅, SF₄, XeF₄), rotatable 3-D shape, a bond-dipole arrow on each bond
  pointing to the more electronegative atom with length ∝ Δχ (course χ values, Day 9 p.17), the vector sum (net arrow),
  a polar/nonpolar verdict, and Table 5.2's measured μ in debyes where listed. It states that arrow lengths use Δχ as
  a stand-in, which predicts direction and cancellation, not the size of μ (e.g., CHCl₃ vs CCl₃F). No χ for Xe in the
  course table (noble gases omitted), so XeF₄ shows "cancels by symmetry".
- `hybrid` (m23): presets for an atom in a molecule: C in CH₄, N in NH₃, O in H₂O (Day 11 p.13–16); C and O in CH₂O,
  N in N₂H₂, C in C₂H₂, C in C₂H₄ (Day 11 p.18–25); B in BF₃, Be in BeCl₂, C in CO₂, P in PCl₃, C and N in HCN (new).
  Shows SN, the ground-state 2s/2p box diagram, a "hybridize" step into hybrid boxes (sp, sp², sp³) plus unhybridized
  p boxes with electrons, which hybrids hold lone pairs or make σ bonds, which p orbitals make π bonds, and a
  "why not promote an electron?" toggle with the professor's objection (Day 11 p.11).
- `sigmaPi` (m24): presets formaldehyde, diazene, acetylene, ethylene (lecture); CO₂, HCN, N₂, acrolein, allene,
  CH₃CN, HCOOH, benzene, C₂H₆ (new/textbook). Shows the Lewis structure with σ bonds and π bonds in two colors
  (as the slides color them), the σ and π counts, and each interior atom's SN and hybridization.
- `chirality` (t5-6): pick the four groups on a tetrahedral carbon (presets CHBrClF and CHBr₂Cl (textbook), CH₂Cl₂,
  the alanine carbon: H, CH₃, NH₂, COOH, and the carvone stereocenter: H, isopropenyl, two different ring CH₂
  branches); shows the molecule and its mirror image in 3-D, a button that rotates the mirror image 120° about a bond
  to try to superimpose it, and a verdict (chiral when all four groups differ).
- `moDiagram` (t5-7): choose H₂, He₂, Li₂ … Ne₂, or NO, and a charge (−2 … +2 where sensible); shows the valence
  MO energy ladder with the textbook's orderings (π<sub>2p</sub> below σ<sub>2p</sub> for Z ≤ 7; σ<sub>2p</sub> below
  π<sub>2p</sub> for O₂–Ne₂ and for NO), the electrons filled by aufbau, Hund, and Pauli, the bond order
  ½(bonding − antibonding), the number of unpaired electrons, and paramagnetic vs diamagnetic. O₂ preset = the
  Day 11 p.27 hook.

## Verification before you finish
1. `py -3.11 check_bank.py <your bank> --modules <your modules>` must print `no findings` (it runs the bank
   validator, fragment structure checks, notation lint, citation ranges, and lewis.py checks).
2. Re-derive every answer independently (reason first, then compute; RDKit / `tools/chemistry_verify.py` /
   numpy for geometry where useful). Put any non-trivial verification script in `verification/CurrentCourseGuide/`
   named `check_<yourbank>.py` and run it.
3. Don't run build_guide.py's full build expecting success: other forks' modules may be unfinished.
4. Final reply (≤ 500 words): files changed; problem ids per module with one-line keys; new lewis.py structures;
   discrepancies/uncertainties found; anything the integrator must do (explorer features your text assumes, CSS
   classes you used that may not exist).

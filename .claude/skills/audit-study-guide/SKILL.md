---
name: audit-study-guide
description: Audit and repair a finished chemistry study guide in study-guides/ with three audits. Content: scope and provenance against the course sources, and preservation of professor conventions. Chemistry: independent checks of equations, balances, numbers, units, sig figs, notation, plots, and structures. UI: a real Playwright run testing navigation, hints, reveals, quizzes, inputs, sliders, graphs, progress, responsive layout, and console errors. Fixes what is safely fixable and records the results in VERIFICATION.md. Use after /build-study-guide, after editing a guide, or whenever the user asks to check, test, verify, QA, proofread, or fix a study guide.
---

# Audit a Study Guide

Target: `study-guides/<guide-name>/`. If the user didn't name one, list the
folders and pick the most recently modified one, saying which you picked. Paths are
relative to `C:\Users\chris\ChemStudy`; run Python with `py -3.11`.

Read first: `CLAUDE.md`, `COURSE.md` (conventions and discrepancies),
`materials/COURSE_INDEX.md`, `materials/HOMEWORK_INDEX.md`,
`materials/TEXTBOOK_MAP.md`, and the guide's `SOURCE_SCOPE.md` and
`VERIFICATION.md`.

Principle: **fix, don't just report.** Fix anything whose correct form is clear
from the sources or from verification, such as typos, notation, wrong numbers,
broken handlers, and layout bugs. Do not "fix" a claim that follows the
professor's material but disagrees with the textbook or with computation. Flag
it and log it as a discrepancy instead. Re-test after every fix.

## Audit 1 — Content and scope

1. Inventory every examinable item in `index.html`: each concept, claim,
   equation, and problem.
2. For each item, confirm a supporting COURSE_INDEX entry with a citation inside
   the range in SOURCE_SCOPE.md. Spot-check citations against the rendered
   pages (`materials/.../<pdf-name>_pages/page-NNN.png`): check at least one per
   topic, plus every citation behind a SUPPORTED EMPHASIS claim.
3. **Scope expansion.** Flag content sourced only from the textbook,
   homework-only concepts, and out-of-range lectures that are presented as
   examinable. Remove them, or relabel them as "Background (not from lecture)".
4. **Professor attribution.** Every "the professor says/emphasizes/expects" must
   be backed by SOURCE-DERIVED or SUPPORTED EMPHASIS evidence. Downgrade anything
   else to neutral wording.
5. **Conventions.** Terminology, notation, sign conventions, configuration
   ordering, constants, and sig-fig policy must match COURSE.md → Professor
   conventions. Where the textbook differs, the guide must explain the difference.
6. **Pedagogy.** Independent problems come before worked solutions. Every
   independent problem has a hint ladder (concept → relationship → setup →
   near-complete → solution). Mixed practice does not name the method. Each topic
   connects the macroscopic, symbolic, and particulate levels.
7. Correct SOURCE_SCOPE.md if it misdescribes the guide.

## Audit 2 — Chemistry

Re-derive; do not just re-read. For every item:

- **Equations**: atom and charge balance
  (`py -3.11 tools/chemistry_verify.py check "<eq>"`), states, arrow type, and
  whether it is net ionic when the text says so.
- **Numbers**: recompute each answer independently, using a different route or
  tool from the one in VERIFICATION.md when possible (`chemistry_verify.py`, a
  script in `verification/<guide-name>/`, or Wolfram). Check the units
  (`units ... --to`), sig figs (`sigfigs`, `round`), and the thermochemical sign.
- **Answer checkers**: the accepted value and tolerance in the JS match the
  verified answer. A correct answer entered with reasonable rounding is accepted,
  and the classic wrong answers are rejected.
- **Structures and electrons**: valence-electron counts (`electrons`), formal
  charges, lone pairs, resonance, geometry, polarity claims, configurations and
  ion configurations (`config`), and quantum numbers (`qn`).
- **Equilibrium, acid–base, kinetics, electrochemistry**: expression form (no pure
  solids or liquids), root selection (`quadratic`, `weak-acid`), linearized fits
  (`linfit`), and E° and n consistency.
- **Graphs**: regenerate the data from the model; check the axes, units, labels,
  slopes, intercepts, and limiting behavior. Check that slider ranges stay
  physical: no negative pressures and no concentrations above solubility unless
  intended.
- **Notation in the rendered HTML**: search `index.html` for flattened notation
  (for example `SO42-`, `H2O` outside `<sub>`, `^`, `->`) and for
  capitalization errors (Co vs. CO).

## Audit 3 — UI (Playwright, for real)

1. Serve the folder in the background:
   `py -3.11 -m http.server 8765 --bind 127.0.0.1 --directory "study-guides/<guide-name>"`
   (use the Bash tool with `run_in_background`). Navigate to
   `http://127.0.0.1:8765/index.html` with `mcp__plugin_playwright_playwright__browser_navigate`.
2. Also confirm the guide works from `file://`, since the student double-clicks
   it. Grep `index.html` and `assets/` for `type="module"`, `fetch(`, `import `,
   and `http` URLs to CDNs or fonts that the page needs in order to work. Replace
   any of these with inline or classic scripts.
3. Take a `browser_snapshot` to get element refs. Then exercise each of these and
   confirm the result, not just the click:
   - **navigation**: every sidebar link scrolls to or shows its section; the
     active state updates
   - **hint buttons**: each press reveals exactly the next hint; the count or
     disabled state is correct at the end of the ladder
   - **solution reveals**: hidden at load (check this before clicking), and
     visible after a deliberate click
   - **quizzes and answer checking**: submit a correct, an incorrect, a
     rounded-correct, a wrong-unit, and an empty or garbage answer (for
     example `abc`, `1e`, `--5`). Check that the feedback is right and nothing
     throws.
   - **sliders and inputs**: move them to the minimum, the maximum, and a middle
     value; check that the readouts and graphs update and stay physical
   - **graphs and interactive visualizations**: render without overlap, labels
     readable, and they respond to their controls
   - **progress and mastery**: progress updates after answering, persists across
     a reload (localStorage), and reset clears it
   - **console**: `browser_console_messages` must show no errors (and warnings
     should be explained)
4. **Screenshots**: `browser_take_screenshot` of the top of the page, each major
   section, and one open hint ladder and revealed solution. Take them at
   1440×900, 768×1024, and 390×844 (`browser_resize`). Look at every screenshot:
   check for overflow, overlapping text, clipped SVGs, unreadable contrast, a
   sidebar covering content on mobile, and sub/superscripts that look wrong. Save
   the important ones to `verification/<guide-name>/screenshots/`.
5. Fix the defects, then reload and re-test the affected features.
6. Stop the background server (TaskStop) and close the browser (`browser_close`).

## Record the results in VERIFICATION.md

Append a dated audit section (keep earlier sections):

```markdown
## Audit <date>
### Content audit
- scope: <n items checked>, <expansions found → action>
- provenance spot-checks: <file p. → ok/fixed>
- conventions: <ok / fixed …>
### Chemistry audit
| Item | Check | Tool | Result | Action |
### UI audit
| Feature | Test performed | Result | Fix |
- viewports: 1440×900, 768×1024, 390×844 — <findings>
- console: <errors / none>
- file:// compatibility: <ok / fixed>
### Corrections made
### Unresolved (needs the student or professor)
```

Update the guide's row in COURSE.md → Study-guide registry (Audited = date).
Report to the user what was fixed, and anything that still needs their judgment
(for example, a discrepancy between the lecture and the textbook). Don't call the
guide done until the content, chemistry, and UI audits have all passed.

---
name: build-study-guide
description: Build or update an active-learning interactive HTML study guide for this General Chemistry course (exam review, unit guide, topic guide, lecture range, or practice set) from the persistent course indexes, with scope set by lecture and review material, practice modeled on the homework, textbook depth only for in-scope topics, progressive hints, hidden solutions, and computational verification. Use whenever the user asks for a study guide, exam or midterm or final prep, a review page, practice problems, an interactive explainer, or a guide for specific lectures or topics. Run /ingest-course first if the relevant materials are not yet indexed.
---

# Build an Interactive Chemistry Study Guide

The output is a learning experience, not a summary: Learn → Understand → Explore →
Attempt → Compare → Practice → Master. Paths are relative to
`C:\Users\chris\ChemStudy`; run Python with `py -3.11`.

## 1. Load context

Read `CLAUDE.md`, `COURSE.md`, `COURSE_MAP.md`, `materials/COURSE_INDEX.md`,
`materials/HOMEWORK_INDEX.md`, and `materials/TEXTBOOK_MAP.md`. Then run
`py -3.11 tools/source_manifest.py status`. If the requested scope includes
NEW/CHANGED/PARTIAL files, tell the user and offer to run `/ingest-course` first.
Guides are built from indexed knowledge.

## 2. Fix the scope before writing anything

- Take the scope from the request: an exam, lecture range, or topics. If it is
  ambiguous and COURSE.md has no exam coverage, ask one question (for example,
  "Days 1–6, or only the topics on the review sheet?").
- **In scope** = concepts in COURSE_INDEX with lecture, notes, or review sources
  inside that range. Review material can narrow or weight the scope, with evidence.
- Homework-only concepts stay out, or appear only in a clearly labeled
  "beyond lecture" note.
- Textbook sections come only from TEXTBOOK_MAP rows for in-scope topics. Content
  listed under Scope notes is not examinable.
- Choose a folder name: `study-guides/<kebab-name>/` (for example,
  `exam1-days1-6`). If it exists, update it in place and keep the student's
  localStorage key stable.
- Write `SOURCE_SCOPE.md` first (template below). It is the contract for the
  guide.

## 3. Plan each topic module

Order topics by `COURSE_MAP.md` so prerequisites come first. For each topic,
choose which of these elements help; omit the ones that don't:

1. intuitive big idea · 2. prerequisites (link to the earlier module) ·
3. macroscopic interpretation · 4. symbolic/formal representation ·
5. particle-level explanation · 6. why the relationship works · 7. equations and
models · 8. variables and units · 9. limiting cases and assumptions ·
10. recognition cues · 11. telling similar problem types apart ·
12. diagrams/graphs · 13. guided worked example · 14. independent problem ·
15. progressive hints · 16. hidden complete solution · 17. likely incorrect vs.
correct reasoning · 18. common mistakes · 19. mixed practice · 20. transfer
problem · 21. mastery check.

Map these onto the stages:

| Stage | Contents |
|---|---|
| **Learn** | big idea, prerequisites, macroscopic → symbolic → particulate |
| **Understand** | why it works, equations with variables/units, assumptions, limiting cases |
| **Explore** | one interactive model where manipulation builds intuition |
| **Attempt** | independent problem before any worked solution; hint ladder |
| **Compare** | worked solution alongside tempting-but-wrong reasoning |
| **Practice** | graded problems with fading scaffolding; mixed, unlabeled problems |
| **Master** | transfer problem plus a mastery check (explain, recognize, solve, sanity-check) |

**Content sources.** Use the professor's terminology, notation, methods, and
conventions from COURSE.md. Go back to the rendered pages
(`materials/.../<pdf-name>_pages/page-NNN.png`) when an index entry is too thin to
teach from. Use textbook sections to deepen intuition, and cite them.
Give every factual block a source tag (see §6).

**Represent three levels explicitly.** In every topic, show MACROSCOPIC (what
is measured or seen), SYMBOLIC (equation, structure, graph), and PARTICULATE (what
the particles are doing), and practice translating between them. Example: "a
graph shape → what the molecules are doing".

## 4. Problems

- Write **new** problems modeled on the HOMEWORK_INDEX problem types (structure,
  difficulty, traps). Do not copy homework problems or post homework answers.
- Build a difficulty ladder per topic: guided → independent → combined → transfer.
- **Hint ladder** for each independent problem:
  1. identify the concept
  2. identify the relationship
  3. establish the setup
  4. near-complete setup
  5. solution: complete reasoning, with units carried and sig figs justified
- **Mixed practice** draws across topics and does NOT label the method. After the
  student answers, show a "what gave it away" note that names the recognition cues.
- For each misconception, give the tempting wrong answer, why it is tempting, and
  why it fails.
- Answer checking: numeric answers accept a tolerance (default ±1% relative,
  or looser when the course's sig-fig policy allows). Separately give feedback on
  sig figs and units when they are entered. Formula and species answers are
  compared after normalizing whitespace. Multiple-choice distractors come from
  real misconceptions.

## 5. Verify while building (reason first, verify second)

Work every answer conceptually, then check it independently. Save the checks in
`verification/<guide-name>/`:

- `py -3.11 tools/chemistry_verify.py` covers balance/check, molar-mass,
  electrons, config, qn, sigfigs, round, units, weak-acid, quadratic, and linfit.
- For plots, simulations, equilibrium or kinetics solving, and numerical methods,
  use a Python script in `verification/<guide-name>/`, or the Jupyter MCP. For
  Jupyter, start the server with `Start-ChemJupyter.ps1`, then call
  `connect_to_jupyter` with `http://localhost:8889` and token `CHEM_TOKEN`; the
  MCP's default server is a different project. Create and edit notebooks only
  through the Jupyter MCP tools.
- Use Wolfram (`mcp__wolfram__WolframAlpha` / `WolframLanguageEvaluator`) as a
  second independent check on non-trivial numbers.
- Every data point on a graph comes from a computed model, never hand-placed.
- If a result disagrees with the course material or the textbook, do not silently
  pick one. Record the disagreement in VERIFICATION.md and COURSE.md →
  Discrepancies, and show it to the student in the guide when it matters.

## 6. Build the HTML

Before designing, invoke the `frontend-design:frontend-design` skill. Invoke
`playground:playground` for explorer-style interactives and `dataviz` for
charts. Consider BioRender (`mcp__plugin_biorender_BioRender__*`) only when a
realistic scientific figure clearly beats an SVG. Prefer hand-built SVG for
anything the student should manipulate.

**Hard technical requirements** (the student opens the file by double-clicking):

- `index.html` must work from `file://` with no server and no network. Inline the
  CSS and JS, or load them as classic `<script src="assets/...">` files. Do not
  use ES-module imports of local files, `fetch()` of local JSON, or CDN
  dependencies. If math typesetting is really needed, vendor it into `assets/`.
  Otherwise use HTML `<sub>`/`<sup>` and Unicode (ΔH°, ⇌, e⁻).
- Chemistry notation must be semantically correct HTML (SO<sub>4</sub><sup>2−</sup>).
  Never write flattened text like "SO42-".
- Solutions and hint steps are hidden by default (`hidden` or `<details>`), and
  they are revealed only by a deliberate click. The hint ladder reveals one step at
  a time.
- Progress: store it in `localStorage` under the key `chemstudy:<guide-name>`.
  Track attempts, correct answers, hints used, and mastery per topic. Show it in
  the sidebar, and include a reset button.
- Layout: navigation sidebar (collapsing to a menu on narrow screens), a stage
  indicator per topic, keyboard-accessible controls, visible focus states, and
  color that is never the only signal.
- Give each interactive element a stable `data-testid` (`hint-btn-<id>`,
  `reveal-<id>`, `answer-<id>`, `check-<id>`, `slider-<id>`, `nav-<topic>`), so
  the audit can drive it with Playwright.
- Show provenance on screen but keep it quiet: a small "Source: Day 3 p.12" line
  per block. Show CLARIFICATION blocks as "Background (not from lecture)", and
  INFERRED links as "Connection". Never present an inference as the
  professor's statement.
- Include a closing "Mixed review" section (unlabeled problems across topics) and
  a "What this guide covers" panel generated from SOURCE_SCOPE.md.

Folder layout:

```
study-guides/<guide-name>/
  index.html
  assets/            (only if needed: js, css, svg, images)
  SOURCE_SCOPE.md
  VERIFICATION.md
```

### SOURCE_SCOPE.md template

```markdown
# Source scope — <guide title>
Built: <date> · Requested scope: <user's words>

## Course materials covered
| File | Pages | Topics |
## Review material used for weighting (with evidence)
## Homework problem types modeled (HOMEWORK_INDEX types, not copied problems)
## Textbook sections consulted (chapter, section, printed/PDF pages, purpose)
## Explicitly excluded
- homework-only concepts, textbook-only content, out-of-range lectures
## Professor conventions applied (from COURSE.md)
## Open uncertainties carried into the guide
```

## 7. Finish

1. Write `VERIFICATION.md` with every calculation checked (method, tool, result,
   and whether it matched), every notation check, and every discrepancy.
2. Run `/audit-study-guide` on the new guide. It performs the content,
   chemistry, and UI audits, fixes problems, and extends VERIFICATION.md.
3. Add or update the guide's row in COURSE.md → Study-guide registry.
4. Tell the user the path to `index.html`, what it covers, and any uncertainties.

Before calling it done, answer each of these for every topic: can the student
explain it; connect particles to equations; recognize it unlabeled; distinguish
it from look-alikes; solve a representative problem; spot an unreasonable
answer; transfer it? If any answer is no, improve that module.

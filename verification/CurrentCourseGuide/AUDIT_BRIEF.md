# Content + chemistry audit brief (Extension 3 sections, 2026-10-06)

You are auditing part of an interactive General Chemistry study guide that someone else wrote. Be independent and
skeptical: the authors' own checks passed, so look for what checks can't see. Project root: `C:\Users\chris\ChemStudy`.
Run Python as `py -3.11` (set `PYTHONIOENCODING=utf-8`). Do not start web servers or browsers.

## Read first
- `CLAUDE.md` (source authority, labels, notation, tutoring philosophy) and `COURSE.md` (Professor conventions,
  Discrepancies). Search `materials/COURSE_INDEX.md` and `materials/TEXTBOOK_MAP.md` for your topics rather than
  reading them whole.
- `study-guides/CurrentCourseGuide/SOURCE_SCOPE.md` (labels, scope, conventions applied).
- `verification/CurrentCourseGuide/EXT3_BRIEF.md` (the authors' conventions: fragment structure, problem helpers,
  notation rules, known slide/textbook discrepancies).
- Your module fragments `verification/CurrentCourseGuide/src/<id>.html` and your problems in the bank file(s) named in
  your assignment. `verification/CurrentCourseGuide/problem_bank.json` holds every problem as built (search by id).

## How the guide labels things
Modules are "lecture+preview": lecture content cites a slide ("Day 10 p.14"); textbook-only content sits inside
`<div class="preview-box">` (labeled Textbook preview, citing "PDF p.NNN"). `<p class="bg">` = Background (not from
lecture); `<p class="connection">` = an inference. `<aside class="signal">` (Lecture signal) needs real emphasis
evidence (bold on the slide, repetition, Top Hat, explicit instruction). Problems are labeled lecture (must cite a Day)
or preview (must cite the textbook).

## What to check (fix, don't just report)
1. **Every examinable claim** in your modules' teaching text (Learn, Understand, Explore prompt, Compare/Common
   mistakes, Master can-do list) and in your problems (prompts, options and feedback, hints, solutions, compare panels):
   is it supported by the cited slide or textbook page, and correctly labeled? Inventory as you go (count items).
2. **Spot-check citations against the rendered pages**: lecture renders are in
   `materials/lectures/Day N Lecture Slides_pages/` and textbook renders in
   `materials/textbook/<book>_pages/` (list the folders to find file names; view PNGs with the Read tool). Check at
   least one citation per topic, every quotation you can, and EVERY Lecture-signal claim. Record each as
   "file p.N → ok / fixed".
3. **Scope**: textbook-only content presented as lecture (outside a preview box, or a problem labeled lecture that
   tests a textbook-only idea) → move it into the preview box, relabel the problem preview, or reword.
4. **Professor attribution**: any "the professor says/emphasizes/expects/prefers" (or "the slides stress", "the lecture
   insists") without slide evidence → neutral wording.
5. **Conventions**: COURSE.md → Professor conventions (terminology such as steric number, electron domains,
   electron-pair geometry; bonding capacity; the five steps; formal-charge steps; shape names). Where the textbook
   differs, the guide must say so.
6. **Chemistry**: re-derive every number, angle, electron count, formal charge, shape, polarity, hybridization,
   σ/π count, bond order, stereocenter count in the teaching text (keys were already blind-verified, but check them
   too if something looks off). Use `tools/chemistry_verify.py` (`electrons`, `config`, `qn`, `check`, `units`,
   `sigfigs`), RDKit, or a short numpy script in your scratchpad. Check notation: subscripts/superscripts, charges as
   magnitude-then-sign (SO₄²⁻), Unicode minus, ↔ for resonance, σ/π symbols, hybrid notation sp<sup>3</sup>.
7. **Pedagogy**: the attempt comes before any worked solution of the same problem; the attempt's hint ladder goes
   concept → relationship → setup → near-complete setup; Learn connects what we observe / what we write / what the
   particles do; distractor feedback names a real misconception; no answer to a problem is printed in its module's
   teaching text (give-away).

## Rules for edits
- Edit ONLY the files in your assignment. Keep problem ids. Keep fragment structure (stage divs, slots, can-do list).
- Don't change an answer key unless it is wrong; if you change one, list it explicitly in your report (it must be
  re-solved blind). Rewording prompts, feedback, hints, and solutions is fine.
- Don't "fix" a professor claim that disagrees with the textbook: flag it, and make sure the guide shows both.
- After editing, run: `py -3.11 verification/CurrentCourseGuide/check_bank.py <bank> --modules <ids>` (must say
  "no findings"), `py -3.11 verification/CurrentCourseGuide/lewis.py` (errors: none), and your bank's
  `check_problem_bank_<x>.py`. Do not run build_guide.py.

## Report (reply, ≤ 600 words)
- items inventoried; scope expansions found → action; attribution fixes; convention fixes
- provenance spot-checks: a list "Day 10 p.15 → ok", "TB PDF p.241 → fixed (…)"
- chemistry checks: item → tool → result → action
- every edit: file/id → what changed (flag any key change)
- unresolved items that need the student or professor (discrepancies)

# ChemStudy project handoff

**Last status reported:** September 24, 2026. This document is a handoff from the conversation, not a fresh inspection of the Windows project. Check the actual files before changing anything.

## Purpose

This is Chris's persistent General Chemistry learning project at `C:\Users\chris\ChemStudy`. Its goal is to turn the actual course material into a reliable course map and then an interactive study guide that teaches independent problem solving. The project should survive closing and reopening Claude Code. This handoff records the state and decisions that may otherwise be lost between sessions.

The intended workflow is:

1. Ingest course material into persistent indexes and a concept/prerequisite map.
2. Check that the course map matches the sources.
3. Build an active-learning HTML guide from the indexed course scope.
4. Audit the chemistry, source alignment, and interface. Fix issues and record verification.

Do not skip ingestion or let a general chemistry textbook determine the scope.

## Current state, as reported by Claude Code

- Project configuration exists: `CLAUDE.md`, `COURSE.md`, `COURSE_MAP.md`, `AGENTS.md`, `materials/COURSE_INDEX.md`, `materials/HOMEWORK_INDEX.md`, `materials/TEXTBOOK_MAP.md`, and `materials/SOURCE_MANIFEST.json`.
- Project skills exist in `.claude/skills/`: `ingest-course`, `build-study-guide`, and `audit-study-guide`. Copies were also put in `.agents/skills/` on the morning of September 24, with an `AGENTS.md` mirroring `CLAUDE.md`.
- Tools exist: `tools/render_pdf.py`, `tools/source_manifest.py`, and `tools/chemistry_verify.py`.
- PowerShell launchers exist: `Render-CoursePDFs.ps1`, `Start-ChemJupyter.ps1`, and `Start-ChemClaude.ps1`.
- Earlier configuration backups were reportedly saved in `_setup_backup/20260923-172410/` and `_setup_backup/20260923-172552/`.
- Seven lecture slide PDFs (`materials/lectures/Day 1 Lecture Slides.pdf` … `Day 7 Lecture Slides.pdf`, 157 pages) and the Gilbert *Atoms-Focused Approach*, 3rd edition, textbook PDF (`materials/textbook/`) are present.
- **Days 1–8 are ingested** (Days 1–7 on 2026-09-24, Day 8 on 2026-09-25). Every slide was visually inspected. `materials/COURSE_INDEX.md` (32 concepts), `COURSE_MAP.md`, `COURSE.md`, and `materials/TEXTBOOK_MAP.md` are populated. `SOURCE_MANIFEST.json` records all seven lectures as ingested and the textbook as mapped (Ch. 1–4 matching sections only). Open questions, especially which textbook edition the course uses, are in `COURSE.md` → Discrepancies.
- One study guide exists: `study-guides/CurrentCourseGuide/` (see below). No homework, professor review sheets, lecture notes, or syllabus have been supplied; `materials/HOMEWORK_INDEX.md` says so.
- A Jupyter connection timed out in the last Claude Code session. Direct Python was reportedly still working. If Jupyter is needed, start `Start-ChemJupyter.ps1` in a separate PowerShell window, leave it running, and reconnect. Do not treat that timeout as evidence that the source files were processed.

These are reported facts from the earlier session, not a claim that I have accessed or verified Chris's Windows filesystem.

## Course-source rules

Use sources in this order:

1. Lecture slides and lecture notes define what the course covers and preserve the instructor's language and methods.
2. Professor review material refines supported assessment emphasis.
3. Homework shows expected problem types and difficulty.
4. Only textbook sections matching established lecture/review topics deepen explanations.
5. Outside knowledge and computation clarify or verify, with clear labeling.

Do not read, summarize, or render the whole textbook. Do not infer instructor emphasis without evidence. Preserve original source filename and PDF page/slide number for every indexed claim. Mark genuinely unreadable content `UNCERTAIN` instead of guessing. Distinguish source-derived statements, supported emphasis, inference, general clarification, and independent verification.

## PDF and image workflow

The lecture PDFs are mostly slides with selectable text plus some diagrams and images. Use a hybrid workflow:

- Extract embedded PDF text for navigation, searching, and initial topic detection.
- For each new or changed lecture PDF, render every slide to PNG once, usually at 220 DPI; visually inspect pages, especially any chemistry notation, equations, diagrams, graphs, arrows, color coding, and annotations.
- For small writing, ambiguous notation, or handwriting, render relevant pages at about 300 DPI and inspect them again.
- Keep page numbering exact: `page-001.png` corresponds to PDF page 1.
- Use visual evidence when text extraction loses a subscript, superscript, ionic charge, reaction/equilibrium arrow, structure, spatial relationship, or handwritten correction.
- Render review sheets and handwritten notes fully when present. Process homework visually where diagrams, notation, or writing matter. For the textbook, identify matching sections first and render only relevant pages when useful.
- Use the existing renderer and manifest. Reuse page images only when they correspond to the current PDF content and resolution. A filename existing by itself does not prove the PDF is unchanged.

`Render-CoursePDFs.ps1` can be run from **ordinary PowerShell**, in `C:\Users\chris\ChemStudy`, to render lecture and review PDFs. The project ingestion skill should also manage rendering automatically when configured to do so. Rendering alone is not ingestion; the slides still require visual analysis and index updates.

## Ingestion output

Run the existing `/ingest-course` skill on the available materials when Chris asks to proceed. First read the existing project instructions, indexes, and manifest and inspect the real directory tree. Use hashes/change detection to process new or changed files while preserving previous valid work.

Update:

- `materials/COURSE_INDEX.md`: concept-centered lecture understanding with exact source/page references, notation, formulas, models, diagrams, examples, prerequisites, supported emphasis, and uncertainties.
- `materials/HOMEWORK_INDEX.md`: problem structures, recognition cues, expected methods, difficulty, prerequisites, and traps when homework exists. Do not fill it with invented homework or a dump of answers.
- `materials/TEXTBOOK_MAP.md`: only matching textbook chapter/section and printed/PDF pages, why relevant, and whether actually consulted.
- `COURSE_MAP.md`: dependency relationships grounded in supplied material, with inferences identified.
- `materials/SOURCE_MANIFEST.json`: accurate hashes and processing status. Record a source as fully ingested only after its pages were actually processed, inspected as needed, and indexed.
- `COURSE.md`: current course status and scope.

After ingestion, present a short audit of topics, prerequisites, lecture pages, homework links, textbook mappings, uncertainties, and possible source disagreements before building a guide.

## Guide and audit, when requested

The `/build-study-guide` skill should make a portable interactive HTML guide under `study-guides/`, with `index.html`, `SOURCE_SCOPE.md`, and `VERIFICATION.md`. It should teach the intuitive big idea, prerequisites, macroscopic observations, symbolic notation, particle-level reasoning, equations and units, recognition cues, worked examples, independent attempts with progressive hints and hidden solutions, common wrong reasoning, mixed practice, transfer, and mastery checks. New analogous practice is preferable to copying homework. The lecture scope controls inclusion.

The `/audit-study-guide` skill should check every topic against cited sources, independently verify chemistry and calculations (including balance, charge, units, significant figures, graphs, and answers), and open the app with Playwright to test its controls and inspect representative screenshots at multiple widths. Fix safe errors and document exactly what passed and what was corrected in `VERIFICATION.md`.

## Next action

Days 1–8 are ingested and the guide covers them. Next: `/audit-study-guide` on `study-guides/CurrentCourseGuide/` when Chris asks; run `/ingest-course` on new material as it arrives (Day 9+, homework, review sheets, syllabus). Before building, check `py -3.11 tools/source_manifest.py status`, and ideally confirm (1) which textbook edition is assigned and (2) whether the italic Ch. 1–2 / RAMP UP topics are examinable (see `COURSE.md`).

To reopen the local project, Chris can start PowerShell and run:

```powershell
cd C:\Users\chris\ChemStudy
powershell -ExecutionPolicy Bypass -File .\Start-ChemClaude.ps1
```

A separate PowerShell window can run `Start-ChemJupyter.ps1` if a Jupyter server is needed. Direct Python may be sufficient for ingestion. Do not block the whole project on Jupyter unless the requested computation requires it.

## Maintenance

Keep this file short and update its **current state** after each substantial ingestion, guide build, or audit. The actual source PDFs, manifest, indexes, and verification files are the authority if this handoff becomes stale. Keep project-level behavior in `CLAUDE.md`/`AGENTS.md` and detailed procedures in the existing skills; this document is a status and intent reminder.

## Study guide built and extended, audit pending (2026-09-24, extended 2026-09-25)

`/build-study-guide` built `study-guides/CurrentCourseGuide/` on 2026-09-24 and extended it on 2026-09-25 (scope set
by the student: every section of Gilbert Ch. 1–4 and the Day 1–8 lectures; topics labeled "covered in lecture" or
"textbook preview"). 41 modules, 458 problems, and 43 explorers. Midterm 1 is "two weeks from" Day 8 (Day 8 p.3).
Open `study-guides/CurrentCourseGuide/index.html`.

- What was checked: `study-guides/CurrentCourseGuide/VERIFICATION.md` (every key blind re-solved,
  417/417; `verify_guide.py` 0 failures, 0 warnings). Working log: `verification/CurrentCourseGuide/BUILD_STATUS.md`.
- **Next step: `/audit-study-guide`**, which the student deliberately deferred. VERIFICATION.md §8 lists
  what it still needs.
- To change content, edit the problem banks or `verification/CurrentCourseGuide/src/*.html`, then run
  `py -3.11 verification/CurrentCourseGuide/build_guide.py`, the four node tests, `lewis.py`, and `verify_guide.py`.
  Lewis structures are defined once in `verification/CurrentCourseGuide/lewis.py`.
  Never hand-edit `assets/data.js`, `assets/scope.js`, or `index.html`.

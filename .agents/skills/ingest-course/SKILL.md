---
name: ingest-course
description: Process new or changed General Chemistry course materials (lecture slides, lecture notes, homework, professor review sheets, images, and only the matching textbook sections) into the persistent indexes — COURSE_INDEX.md, HOMEWORK_INDEX.md, TEXTBOOK_MAP.md, COURSE_MAP.md, COURSE.md — with SHA-256 change tracking, exact filename + page provenance, and visual inspection of rendered pages for chemistry notation. Use whenever the user adds files to materials/, or asks to ingest, process, read, analyze, index, catch up on, or update course materials, lectures, notes, homework, or the textbook mapping. Do not use it to build study guides.
---

# Ingest Course Materials

Turn raw files in `materials/` into cumulative, concept-organized, provenance-tagged
course knowledge. Work incrementally: process only what is new or changed, reuse
renders, and never rebuild an index from scratch when a merge will do.

All paths are relative to the project root `C:\Users\chris\ChemStudy`. Run tools
with `py -3.11`. Quote paths: the lecture filenames contain spaces.

## 0. Load state first

Read, in order: `AGENTS.md`, `COURSE.md`, `COURSE_MAP.md`,
`materials/COURSE_INDEX.md`, `materials/HOMEWORK_INDEX.md`,
`materials/TEXTBOOK_MAP.md`. Then run:

```
py -3.11 tools/source_manifest.py status
```

This read-only report lists `NEW`, `CHANGED`, `MOVED`, `PARTIAL`, and `MISSING`
files. Everything else is unchanged, so skip it.

- **MOVED**: same content under a new path. Update citations in the indexes to the
  new path, `mark` the new path with the old status, and `forget` the old path. Do
  not re-read it.
- **CHANGED**: run `py -3.11 tools/source_manifest.py diff "<path>"` to get the
  changed pages. Re-process only those pages, then find every index bullet citing
  those pages and revise or remove it. Keep bullets for unchanged pages.
- **MISSING**: tell the user. Keep its index content (it is still evidence) unless
  the user says the file was withdrawn. Then `forget` it.
- **PARTIAL**: continue from the first page not in `pages_done`.

If the user named specific files, restrict the run to those. For a large batch,
say what you will process, in which order, and roughly how many pages, then work
through it. Order: lectures and notes in course order, then review, then
homework, then textbook mapping (it depends on the topics found).

## 1. Lectures, notes, and review: read every page visually

Per file:

1. **Probe**: `py -3.11 tools/render_pdf.py probe "<pdf>" --summary`. This gives the
   page count and flags pages with no text layer, heavy images, many vector
   drawings, or broken glyphs.
2. **Extract text** for navigation and search:
   `py -3.11 tools/render_pdf.py text "<pdf>"` (written to `<pdf-name>_pages/text/`).
   Never transcribe chemistry notation from text alone: it routinely loses
   subscripts, superscripts, charges, arrows, Greek letters, and layout.
3. **Render**: `py -3.11 tools/render_pdf.py render "<pdf>"`. Default 220 DPI; use
   `--dpi 300` for handwritten or scanned notes and dense slides. Existing renders
   are reused automatically, including ones made by `Render-CoursePDFs.ps1`.
4. **Inspect each page image** with the Read tool
   (`<pdf-name>_pages/page-NNN.png`). When a subscript, charge, exponent, arrow,
   lone pair, or handwritten mark is too small to read, zoom in:
   `py -3.11 tools/render_pdf.py crop "<pdf>" --page N --box x0,y0,x1,y1 --dpi 400`
   (fractions of the page, origin top-left). Where the text layer and the image
   disagree, the image wins.
5. **Mark genuinely unreadable content UNCERTAIN** with file, page, location, and
   the candidate readings. Never guess.

For long files, work in chunks of about 10 pages. After each chunk, write its
findings into the indexes, then `mark ... --status partial --pages <chunk>`. An
interrupted run then resumes cleanly. For batches of many files, you may hand
single files to subagents to extract. Give each the page-analysis checklist
below and require page-cited, labeled bullets back. Do the merge into the
indexes yourself.

### Notation checklist (check every page against it)

Subscripts vs. coefficients · superscripts and ionic charges (magnitude then
sign: SO₄²⁻) · element capitalization (Co vs. CO) · physical states (s, l, g, aq)
· reaction arrows (→) vs. equilibrium arrows (⇌) vs. resonance arrows (↔) ·
electrons (e⁻) in half-reactions · oxidation states · lone pairs, formal charges,
and bond order in Lewis structures · resonance structures · orbitals and orbital
diagrams · electron configurations (ordering, noble-gas cores) · quantum numbers ·
units and prefixes · significant figures as printed · scientific notation and
exponents · logarithms (log vs. ln) · thermodynamic signs (ΔH < 0, q, w) ·
graph axes, units, scales, and slopes · color coding, highlighting, circles, and
arrows added by the professor · handwritten corrections and strike-throughs.

### Page-analysis checklist (record what is present)

Topic and subtopics · definitions · equations and relationships (variables,
units, stated conditions) · the professor's explanations and wording · worked
examples (method, steps shown, answer format, sig figs) · diagrams and graphs
(what the axes are and what the figure shows) · particle-level models ·
problem-solving procedures · shortcuts and mnemonics · assumptions · warnings
("students often…") · repeated ideas · explicit emphasis ("this will be on the
exam", boxed or starred items, "important") · prerequisites · connections to
earlier topics · uncertainties.

### Emphasis rules

Record **SUPPORTED EMPHASIS** only with concrete evidence: explicit statements,
repetition across lectures (cite each occurrence), highlighting or annotation,
placement on review material, or "practice this" callouts. Slide count alone is
weak evidence; say so if you use it. Never write "the professor emphasizes X"
without that evidence.

## 2. Write into the indexes (merge, don't append)

**`materials/COURSE_INDEX.md`**: organize by concept using the template in that
file. Before adding a concept, search the file for it (and synonyms). If it
exists, merge the new evidence into it with new citations. Use the professor's
term as the heading. Label every bullet. Add a row to the Source coverage log.

**`COURSE.md`**: fill identity facts, the lecture sequence, and exam coverage when
the materials state them. Fill the **Professor conventions** table from what
you actually see: sig-fig handling, constants, configuration ordering, sign
conventions, H⁺ vs. H₃O⁺, named methods. Log every conflict between sources
under **Discrepancies**. Update the ingestion status line.

**`COURSE_MAP.md`**: add concepts under the course's own units, in course order.
Add edges with basis SOURCE-DERIVED (the materials connect them explicitly;
cite it) or INFERRED. Regenerate the mermaid diagram from the edge list
(dashed = inferred). Update dependency chains and cross-topic connections. Never
import generic syllabus structure.

## 3. Homework → `materials/HOMEWORK_INDEX.md`

Render and inspect homework pages the same way whenever notation, diagrams, or
layout matter. Catalogue by **problem type**, not by assignment, using the
template in that file: concepts tested, structure, expected technique (link it
to the lecture page that teaches it), recognition cues, look-alikes, prerequisite
skills, multi-step combinations, difficulty 1–5, traps, notation, and
professor-specific expectations (only with evidence).

- Do not write solutions into the index. At most record a short reference answer
  for later verification.
- Concepts that appear only in homework go under **Homework-only concepts** in
  `COURSE_MAP.md`. Flag them to the user; they are not course scope.

## 4. Textbook → `materials/TEXTBOOK_MAP.md` (targeted only)

Never read or render the whole book. Only after lecture topics are known:

1. `py -3.11 tools/render_pdf.py toc "<book.pdf>" --max-level 2` for chapter and
   section PDF pages. If there are no bookmarks, render the printed table of
   contents pages (usually within the first ~25 PDF pages) and read them.
2. `py -3.11 tools/render_pdf.py search "<book.pdf>" "<professor term>" "<synonym>"`
   to locate sections for each course topic.
3. `py -3.11 tools/render_pdf.py labels "<book.pdf>" --pages a-b` for the printed
   page numbers. Record the printed ↔ PDF offset in the textbook files table.
4. Skim only the candidate section pages (text layer, rendered when figures,
   tables, or equations matter) to confirm relevance.
5. Add a mapping row: course topic, lecture source/pages, chapter, section,
   printed pages, PDF pages, why it is relevant, and consulted status.
6. Record textbook content beyond course scope under **Scope notes**, and
   convention differences under **Convention differences** (mirrored in
   COURSE.md).
7. `py -3.11 tools/source_manifest.py mark "<book.pdf>" --status mapped --pages <consulted pages>`.
   Pages accumulate across runs.

The textbook may deepen explanations. It never adds topics.

## 5. Images, Office files, other formats

- `materials/images/*.png|jpg|webp`: view directly with Read. Treat them like a
  page of whichever category they belong to (ask the user if that is unclear). Cite
  them by filename.
- `.pptx` / `.docx`: use the `anthropic-skills:pptx` / `anthropic-skills:docx`
  skills to extract content and speaker notes. LibreOffice is not installed, so
  there is no PDF conversion. Cite slide numbers.
- Files reported as UNSUPPORTED by `status`: tell the user.

## 6. Commit state only after the indexes are written

Once a file's content is in the indexes:

```
py -3.11 tools/source_manifest.py mark "<path>" --status ingested --indexes COURSE_INDEX,COURSE_MAP,COURSE --note "<one-line summary>"
```

Use `--status partial --pages ...` for incomplete files and `--status skipped
--note "<reason>"` for intentional skips (duplicates, blank pages, boilerplate).
Never mark a file before its content is saved: the manifest is what lets a future
session trust that the work was done.

## 7. Report back

Summarize:

1. files processed, with pages
2. concepts added or updated
3. professor conventions found
4. COURSE_MAP edges added
5. textbook mappings added
6. every UNCERTAIN item, with file, page, and what is unclear, so the student can
   check the original or ask the professor
7. discrepancies found
8. homework-only concepts
9. unchanged files skipped

Do not build a study guide unless asked.

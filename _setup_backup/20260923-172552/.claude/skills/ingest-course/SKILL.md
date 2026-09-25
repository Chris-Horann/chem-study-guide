---
name: ingest-course
description: Process new or changed chemistry lecture slides, notes, homework, review material, images, and relevant textbook sections. Update the persistent course indexes and conceptual map while preserving exact source filenames and page numbers. Use whenever the user asks to ingest, process, analyze, or update chemistry course materials.
---

# Ingest Chemistry Course Material

Before processing material, read:

1. CLAUDE.md
2. COURSE.md
3. COURSE_MAP.md
4. materials/COURSE_INDEX.md
5. materials/HOMEWORK_INDEX.md
6. materials/TEXTBOOK_MAP.md
7. materials/SOURCE_MANIFEST.json

Process new or changed sources whenever possible instead of rebuilding everything.

## Source hierarchy

Use:

1. lecture slides and notes
2. professor review material
3. assigned homework
4. matching textbook sections
5. outside knowledge only for clarification or verification

Lecture material determines course scope.

## Change detection

Use tools/source_manifest.py and materials/SOURCE_MANIFEST.json to identify new or changed files.

Do not unnecessarily reprocess unchanged material.

Do not commit manifest state until processing has completed successfully.

## Lecture PDF processing

Lecture PDFs use a hybrid text + visual workflow.

For every newly added or changed lecture PDF:

1. inspect embedded PDF text
2. use embedded text for search, navigation, topic identification, and locating relevant slides
3. render every slide to PNG using tools/render_pdf.py
4. store images beside the PDF in:

   <pdf-name>_pages/
       page-001.png
       page-002.png
       ...

5. use approximately 220 DPI by default
6. increase to approximately 300 DPI when notation is small, handwriting is present, or diagrams require more detail
7. preserve exact PDF page/slide numbers
8. visually inspect the rendered slide whenever chemical meaning may depend on visual information
9. combine textual extraction and visual interpretation

Do not assume extracted PDF text preserves chemistry notation correctly.

Visually check:
- subscripts
- superscripts
- ionic charges
- coefficients
- physical states
- reaction arrows
- equilibrium arrows
- oxidation states
- electrons
- Lewis structures
- resonance
- formal charges
- lone pairs
- orbitals
- electron configurations
- molecular geometry
- particle models
- graphs and graph axes
- color coding
- highlighting
- spatial relationships
- annotations
- images
- handwritten corrections

When embedded text and the rendered slide disagree, use the rendered slide to determine what is visibly present.

Mark unreadable material UNCERTAIN rather than guessing.

Reuse rendered pages for unchanged PDFs.

## Notes

For scanned or handwritten notes, render every page at approximately 300 DPI.

Visually inspect the actual page images.

Do not rely solely on OCR.

## Professor review material

Treat review PDFs similarly to lecture slides.

Render every page once and inspect both text and visual content.

Review material may support claims of assessment emphasis when the source actually indicates that emphasis.

## Homework

Analyze homework separately in materials/HOMEWORK_INDEX.md.

For homework PDFs:
- use embedded text for navigation when reliable
- render pages whenever notation, diagrams, structures, or layout matters
- preserve page and problem numbers

Identify:
- concepts tested
- recognition cues
- problem structures
- expected calculation techniques
- prerequisite skills
- multi-step combinations
- recurring traps
- notation
- approximate difficulty
- relationships to lecture topics

Do not turn the homework index into an answer key.

## Textbook

Do NOT render or read the entire textbook.

First determine course topics from lecture material.

Then locate only corresponding textbook sections.

Maintain materials/TEXTBOOK_MAP.md.

For each mapping record:
- course topic
- lecture sources/pages
- textbook chapter
- textbook section
- printed textbook pages if available
- PDF pages if different
- reason for mapping
- consulted status

Use embedded textbook text when reliable.

Render only relevant textbook pages when diagrams, equations, tables, notation, or formatting need visual inspection.

The textbook deepens explanations but does not define course scope.

## Course Index

Update materials/COURSE_INDEX.md primarily by CONCEPT.

For each topic include, when present:
- source filename
- original page/slide number
- topic and subtopics
- definitions
- equations
- relationships
- macroscopic interpretation
- symbolic representation
- particle-level explanation
- professor explanations
- worked examples
- problem-solving techniques
- diagrams
- graphs
- recognition cues
- common mistakes
- explicit emphasis
- prerequisites
- connections
- uncertainties

Merge multiple sources intelligently while preserving provenance.

## Source evidence labels

Distinguish:

SOURCE-DERIVED
Directly supported by supplied material.

SUPPORTED EMPHASIS
Supported by repetition, highlighting, review placement, annotations, or explicit instructor statements.

INFERRED
Reasonable conceptual or prerequisite inference.

CLARIFICATION
General chemistry knowledge supplied to improve understanding.

VERIFICATION
Independent computational check.

UNCERTAIN
Cannot be interpreted confidently.

Never turn an inference into a claim about what the professor said.

## Course Map

Update COURSE_MAP.md using actual course material.

Represent conceptual and prerequisite relationships.

Do not force the course into a generic General Chemistry order.

## Completion

After successful ingestion:

1. update SOURCE_MANIFEST.json
2. summarize files processed
3. summarize pages processed
4. list topics added or updated
5. list textbook mappings
6. list uncertainties
7. list unchanged files skipped

Do not build a study guide unless the user asks.

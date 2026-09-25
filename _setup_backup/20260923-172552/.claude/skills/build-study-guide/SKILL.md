---
name: build-study-guide
description: Build or update a polished interactive chemistry study guide from the persistent course indexes, homework analysis, professor material, and only matching textbook sections. Use when the user asks for a chemistry study guide, exam guide, unit guide, or interactive review.
---

# Build Interactive Chemistry Study Guide

Read:

1. CLAUDE.md
2. COURSE.md
3. COURSE_MAP.md
4. materials/COURSE_INDEX.md
5. materials/HOMEWORK_INDEX.md
6. materials/TEXTBOOK_MAP.md

Determine exact supported scope before building.

Lecture material defines scope.

Professor review may refine assessment emphasis.

Homework determines expected problem types and difficulty.

Textbook material only deepens topics already supported by the course.

## Learning sequence

Build:

Learn
â†’ Understand
â†’ Explore
â†’ Attempt
â†’ Compare
â†’ Practice
â†’ Master

The result must be an active-learning experience rather than a passive summary.

## Three representations

Whenever useful connect:

MACROSCOPIC
What is observed or measured?

SYMBOLIC
What equations, structures, formulas, graphs, or mathematical relationships represent the process?

PARTICULATE
What are atoms, molecules, ions, electrons, bonds, and intermolecular forces doing?

Teach translation between these representations.

## Topic modules

For each major topic include as appropriate:

- intuitive big idea
- prerequisites
- why it matters
- macroscopic interpretation
- symbolic representation
- particle-level explanation
- formal equations/models
- variable meanings
- units
- assumptions
- limiting cases
- recognition cues
- look-alike problem types
- visual explanation
- guided worked example
- independent attempt
- progressive hints
- hidden full solution
- likely incorrect reasoning versus correct reasoning
- common mistakes
- mixed practice
- transfer problem
- mastery check

## Progressive hints

Prefer:

Hint 1: identify the concept
Hint 2: identify the relevant relationship
Hint 3: establish the setup
Hint 4: near-complete setup
Solution: complete reasoning

Do not reveal independent-practice solutions by default.

Do not label every mixed-practice problem with the method required.

Recognition is part of mastery.

## Practice design

Use homework to infer:
- style
- difficulty
- common structures
- multi-step combinations

Create analogous new problems rather than simply copying homework.

Gradually reduce scaffolding.

## Interactive UI

Use installed Playground and Frontend Design capabilities when useful.

Possible educational interactions:
- periodic trends
- electron configurations
- orbital diagrams
- Lewis structures
- molecular geometry
- polarity
- particle models
- dimensional-analysis chains
- stoichiometric relationships
- limiting-reactant visualization
- gas-law sliders
- heating curves
- reaction coordinate diagrams
- equilibrium shifts
- concentration changes
- titration curves
- kinetics graphs
- electrochemical cells
- quizzes
- progressive hints
- solution reveals
- answer checking
- concept maps
- progress indicators
- navigation sidebar

Use BioRender only when it genuinely improves a scientific explanation.

Prefer HTML/SVG when a diagram is simple and benefits from interaction.

## Output

Store each guide in its own folder under study-guides/.

Prefer:

study-guides/<guide-name>/
    index.html
    SOURCE_SCOPE.md
    VERIFICATION.md
    assets/        if necessary

SOURCE_SCOPE.md must state exactly which course materials/pages are covered.

## Verification

Reason first, verify second.

Use Jupyter/Python, Wolfram, and local chemistry libraries where useful.

Check as applicable:
- atom balance
- charge balance
- stoichiometry
- molar masses
- electron counts
- electron configurations
- units
- dimensional consistency
- significant figures
- thermochemical signs
- equilibrium expressions
- equilibrium roots
- pH calculations
- kinetics calculations
- electrochemistry
- graph values
- slopes
- intercepts

Do not use computation as the conceptual explanation.

Record verification in VERIFICATION.md.

## Final educational check

For each major topic ask:

Can the student explain it?
Can the student connect particles to equations?
Can the student recognize it in an unlabeled problem?
Can the student distinguish it from similar concepts?
Can the student solve a representative problem?
Can the student detect unreasonable answers?
Can the student transfer it to a new problem?

Improve the module when the answer is no.

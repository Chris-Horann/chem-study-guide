---
name: audit-study-guide
description: Audit and repair a generated chemistry study guide for source alignment, chemistry accuracy, calculations, visual quality, and interactive behavior. Use after building or updating a guide.
---

# Audit Chemistry Study Guide

Perform three audits.

## 1. Source alignment audit

Check:
- every examinable topic is supported by course sources
- no accidental textbook-driven scope expansion occurred
- professor terminology and conventions are preserved
- source/page provenance is correct
- SOURCE_SCOPE.md accurately describes the guide
- unsupported claims are identified and corrected

## 2. Chemistry accuracy audit

Independently verify as applicable:
- equations
- chemical formulas
- subscripts
- superscripts
- charges
- reaction arrows
- equilibrium arrows
- atom balance
- charge balance
- stoichiometric coefficients
- molar masses
- numerical calculations
- dimensional consistency
- units
- significant figures
- electron counts
- electron configurations
- thermochemical signs
- equilibrium expressions
- pH calculations
- kinetics
- electrochemistry
- graph values
- axes
- slopes
- structures
- diagrams

Use Jupyter/Python, Wolfram, Pint, ChemPy, periodictable, RDKit, SymPy, NumPy, or SciPy when useful.

Reason first and verify second.

Fix errors when safe rather than merely reporting them.

## 3. UI and usability audit

Use Playwright to actually open the finished guide.

Test:
- navigation
- hint buttons
- solution reveals
- quizzes
- answer checking
- input validation
- sliders
- interactive diagrams
- graphs
- progress indicators
- responsive layout

Inspect major pages visually.

Check browser console errors.

Test multiple viewport sizes when practical.

Fix broken behavior and layout problems when safe.

## Verification record

Update VERIFICATION.md with:
- what was checked
- tools used
- failures found
- corrections made
- unresolved uncertainties

Do not declare the guide complete until content accuracy and interface behavior have both been checked.

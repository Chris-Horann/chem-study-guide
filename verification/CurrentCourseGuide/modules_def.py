"""Module and unit definitions for the CurrentCourseGuide (shared by build_guide.py and check_bank.py).

Labels: "lecture" = covered in lecture; "preview" = textbook preview; "lecture+preview" = a lecture topic
with a labeled textbook-preview part. Module ids are stable (they key the student's saved progress), so a
module keeps its id when its label changes: t4-2, t4-5 ... t4-8 started as textbook previews and were
taught on Day 9.
"""

BUILD_DATE = "2026-10-06"
LAST_DAY = 12                          # latest lecture the guide's labels describe
STORAGE_KEY = "chemstudy:CurrentCourseGuide"


def tbp(a, b):
    """textbook page range: 'printed a–b (PDF a+34–b+34)'"""
    return f"printed pp. {a}–{b} (PDF {a + 34}–{b + 34})" if b != a else f"printed p. {a} (PDF {a + 34})"


UNITS = [
    {"id": "C1", "title": "Matter and Energy: An Atomic Perspective", "chapter": "Ch. 1",
     "modules": ["m1", "t1-2", "t1-3", "t1-4", "t1-5", "t1-6", "t1-7", "t1-8", "t1-9"]},
    {"id": "C2", "title": "Atoms, Ions, and Molecules", "chapter": "Ch. 2",
     "modules": ["m2", "t2-2", "t2-3", "t2-4", "t2-5", "t2-6"]},
    {"id": "C3", "title": "Atomic Structure", "chapter": "Ch. 3",
     "modules": ["m3", "m4", "m5", "m6", "m7", "t3-5", "m8", "m9", "m10", "m11", "m12", "m13", "t3-11"]},
    {"id": "C4", "title": "Chemical Bonding", "chapter": "Ch. 4",
     "modules": ["m14", "t4-2", "m15", "m16", "m17", "t4-3", "m18", "m19", "t4-5", "t4-6", "t4-7", "t4-8", "t4-9"]},
    {"id": "C5", "title": "Bonding Theories: Explaining Molecular Geometry", "chapter": "Ch. 5",
     "modules": ["m20", "m21", "m22", "m23", "m24", "t5-6", "t5-7"]},
    {"id": "C18", "title": "The Solid State (§18.4–18.5 only)", "chapter": "Ch. 18",
     "modules": ["m25"]},
]

MODULES = [
    {"id": "m1", "sec": "1.1", "title": "Atoms from mass laws", "short": "Mass laws", "label": "lecture+preview",
     "sources": "Day 1 p.8–15", "textbook": "§1.1, " + tbp(4, 7), "prereqs": []},
    {"id": "t1-2", "sec": "1.2", "title": "COAST: a framework for solving problems", "short": "COAST", "label": "preview",
     "sources": "", "textbook": "§1.2, " + tbp(7, 8), "prereqs": []},
    {"id": "t1-3", "sec": "1.3", "title": "Classes and properties of matter", "short": "Classes of matter", "label": "preview",
     "sources": "", "textbook": "§1.3, " + tbp(8, 13), "prereqs": ["m1"]},
    {"id": "t1-4", "sec": "1.4", "title": "States of matter", "short": "States of matter", "label": "preview",
     "sources": "", "textbook": "§1.4, " + tbp(13, 16), "prereqs": ["t1-3"]},
    {"id": "t1-5", "sec": "1.5", "title": "Forms of energy", "short": "Forms of energy", "label": "lecture+preview",
     "sources": "Day 1 p.15", "textbook": "§1.5, " + tbp(16, 17), "prereqs": ["t1-4"]},
    {"id": "t1-6", "sec": "1.6", "title": "Formulas and models", "short": "Formulas and models", "label": "preview",
     "sources": "", "textbook": "§1.6, " + tbp(17, 19), "prereqs": ["m1"]},
    {"id": "t1-7", "sec": "1.7", "title": "Measurements and significant figures", "short": "Significant figures", "label": "preview",
     "sources": "", "textbook": "§1.7, " + tbp(19, 26), "prereqs": []},
    {"id": "t1-8", "sec": "1.8", "title": "Unit conversions and dimensional analysis", "short": "Unit conversions", "label": "preview",
     "sources": "", "textbook": "§1.8, " + tbp(26, 31), "prereqs": ["t1-7"]},
    {"id": "t1-9", "sec": "1.9", "title": "Analyzing experimental results", "short": "Statistics", "label": "preview",
     "sources": "", "textbook": "§1.9, " + tbp(31, 37), "prereqs": ["t1-7"]},
    {"id": "m2", "sec": "2.1", "title": "Inside the atom", "short": "Inside the atom", "label": "lecture+preview",
     "sources": "Day 1 p.16–20; Day 2 p.4–24", "textbook": "§2.1, " + tbp(48, 53), "prereqs": ["m1"]},
    {"id": "t2-2", "sec": "2.2", "title": "Nuclides and their symbols", "short": "Nuclide symbols", "label": "lecture+preview",
     "sources": "Day 2 p.22–23 (RAMP UP)", "textbook": "§2.2, " + tbp(53, 56), "prereqs": ["m2"]},
    {"id": "t2-3", "sec": "2.3", "title": "Navigating the periodic table", "short": "Periodic table", "label": "lecture+preview",
     "sources": "Day 2 p.24 (RAMP UP)", "textbook": "§2.3, " + tbp(56, 60), "prereqs": ["t2-2"]},
    {"id": "t2-4", "sec": "2.4", "title": "Masses of atoms, ions, and molecules", "short": "Atomic mass", "label": "lecture+preview",
     "sources": "Day 2 p.21–23 (RAMP UP)", "textbook": "§2.4, " + tbp(60, 64), "prereqs": ["t2-2"]},
    {"id": "t2-5", "sec": "2.5", "title": "Moles and molar masses", "short": "Moles", "label": "preview",
     "sources": "", "textbook": "§2.5, " + tbp(64, 70), "prereqs": ["t2-4", "t1-8"]},
    {"id": "t2-6", "sec": "2.6", "title": "Mass spectrometry", "short": "Mass spectrometry", "label": "preview",
     "sources": "", "textbook": "§2.6, " + tbp(70, 74), "prereqs": ["t2-4"]},
    {"id": "m3", "sec": "3.1", "title": "Light: waves and photons", "short": "Light", "label": "lecture+preview",
     "sources": "Day 2 p.25–30; Day 3 p.12, p.17", "textbook": "§3.1, " + tbp(86, 89), "prereqs": []},
    {"id": "m4", "sec": "3.2", "title": "Atomic spectra", "short": "Spectra", "label": "lecture",
     "sources": "Day 2 p.31; Day 3 p.7–11", "textbook": "§3.2, " + tbp(89, 90), "prereqs": ["m3"]},
    {"id": "m5", "sec": "3.3", "title": "Quantized energy: Planck and the photoelectric effect", "short": "Photoelectric effect", "label": "lecture",
     "sources": "Day 3 p.11–19", "textbook": "§3.3, " + tbp(90, 95), "prereqs": ["m3", "m4"]},
    {"id": "m6", "sec": "3.4", "title": "Hydrogen's spectrum and the Bohr model", "short": "Bohr model", "label": "lecture",
     "sources": "Day 3 p.21; Day 4 p.3, p.6–10", "textbook": "§3.4, " + tbp(95, 100), "prereqs": ["m4", "m5"]},
    {"id": "m7", "sec": "3.5", "title": "Matter waves (de Broglie)", "short": "Matter waves", "label": "lecture",
     "sources": "Day 4 p.11–17", "textbook": "§3.5, " + tbp(100, 103), "prereqs": ["m6"]},
    {"id": "t3-5", "sec": "3.5", "title": "The Heisenberg uncertainty principle", "short": "Uncertainty principle", "label": "preview",
     "sources": "", "textbook": "§3.5, " + tbp(103, 104), "prereqs": ["m7"]},
    {"id": "m8", "sec": "3.6", "title": "Wavefunctions, quantum numbers, and Pauli", "short": "Quantum numbers", "label": "lecture",
     "sources": "Day 4 p.18; Day 5 p.7–16", "textbook": "§3.6, " + tbp(104, 108), "prereqs": ["m6", "m7"]},
    {"id": "m9", "sec": "3.7", "title": "Orbital shapes and radial distributions", "short": "Orbitals", "label": "lecture+preview",
     "sources": "Day 5 p.17–20; Day 6 p.12, p.18", "textbook": "§3.7, " + tbp(108, 111), "prereqs": ["m8"]},
    {"id": "m10", "sec": "3.8", "title": "Electron configurations", "short": "Configurations", "label": "lecture+preview",
     "sources": "Day 6 p.6–20; Day 7 p.6", "textbook": "§3.8, " + tbp(111, 119), "prereqs": ["m8", "m9"]},
    {"id": "m11", "sec": "3.9", "title": "Configurations of ions", "short": "Ion configurations", "label": "lecture",
     "sources": "Day 6 p.21–23", "textbook": "§3.9, " + tbp(119, 122), "prereqs": ["m10"]},
    {"id": "m12", "sec": "3.10", "title": "Atomic and ionic size", "short": "Size trends", "label": "lecture",
     "sources": "Day 6 p.24–26; Day 7 p.5, p.7–8", "textbook": "§3.10, " + tbp(122, 125), "prereqs": ["m10", "m11"]},
    {"id": "m13", "sec": "3.11–3.12", "title": "Ionization energy and electron affinity", "short": "IE and EA", "label": "lecture",
     "sources": "Day 7 p.9–11", "textbook": "§3.11 (IE part), " + tbp(125, 128) + "; §3.12, " + tbp(130, 133), "prereqs": ["m6", "m10", "m12"]},
    {"id": "t3-11", "sec": "3.11", "title": "Photoelectron spectroscopy", "short": "PES", "label": "preview",
     "sources": "", "textbook": "§3.11 (PES part), " + tbp(128, 130), "prereqs": ["m13", "m5"]},
    {"id": "m14", "sec": "4.1", "title": "Bonds, Coulomb energy, and lattices", "short": "Bonds and lattices", "label": "lecture+preview",
     "sources": "Day 7 p.12–17; Day 8 p.11, p.14–15, p.18", "textbook": "§4.1, " + tbp(146, 151), "prereqs": ["m12", "m13"]},
    {"id": "t4-2", "sec": "4.2", "title": "Electronegativity and polar bonds", "short": "Electronegativity", "label": "lecture+preview",
     "sources": "Day 9 p.15–18; Day 10 p.27", "textbook": "§4.2, " + tbp(151, 154), "prereqs": ["m14", "m13"]},
    {"id": "m15", "sec": "4.3", "title": "Ionic formulas and names", "short": "Formulas and names", "label": "lecture",
     "sources": "Day 7 p.18–21; Day 8 p.6", "textbook": "§4.3 (binary ionic, main group), " + tbp(155, 156), "prereqs": ["m11", "m14"]},
    {"id": "m16", "sec": "4.3", "title": "Transition-metal ions and polyatomic ions", "short": "Metals and polyatomic ions", "label": "lecture+preview",
     "sources": "Day 8 p.7–10", "textbook": "§4.3 (transition metals; polyatomic ions), " + tbp(156, 159), "prereqs": ["m15"]},
    {"id": "m17", "sec": "4.3", "title": "Naming covalent compounds", "short": "Covalent names", "label": "lecture+preview",
     "sources": "Day 8 p.12–13", "textbook": "§4.3 (binary molecular compounds), " + tbp(154, 155), "prereqs": ["m15", "m14"]},
    {"id": "t4-3", "sec": "4.3", "title": "Naming acids", "short": "Acids", "label": "preview",
     "sources": "", "textbook": "§4.3 (binary acids; oxoacids), " + tbp(159, 161), "prereqs": ["m16", "m17"]},
    {"id": "m18", "sec": "4.4", "title": "Lewis symbols and the octet rule", "short": "Lewis symbols", "label": "lecture+preview",
     "sources": "Day 8 p.16–18", "textbook": "§4.4 (Lewis symbols; ionic compounds), " + tbp(161, 163), "prereqs": ["m10", "m14"]},
    {"id": "m19", "sec": "4.4", "title": "Lewis structures: the five steps", "short": "Lewis structures", "label": "lecture+preview",
     "sources": "Day 8 p.19–26, p.28–30; Day 9 p.6, p.19–20", "textbook": "§4.4 (five steps; double and triple bonds), " + tbp(163, 168), "prereqs": ["m18"]},
    {"id": "t4-5", "sec": "4.5", "title": "Resonance", "short": "Resonance", "label": "lecture+preview",
     "sources": "Day 8 p.26–30; Day 9 p.2, p.6–13", "textbook": "§4.5, " + tbp(168, 172), "prereqs": ["m19"]},
    {"id": "t4-6", "sec": "4.6", "title": "Bond lengths and strengths", "short": "Bond lengths", "label": "lecture+preview",
     "sources": "Day 8 p.11; Day 9 p.7, p.14", "textbook": "§4.6, " + tbp(172, 174), "prereqs": ["t4-5", "m14"]},
    {"id": "t4-7", "sec": "4.7", "title": "Formal charge", "short": "Formal charge", "label": "lecture+preview",
     "sources": "Day 9 p.19–26", "textbook": "§4.7, " + tbp(174, 178), "prereqs": ["m19", "t4-5", "t4-2"]},
    {"id": "t4-8", "sec": "4.8", "title": "Exceptions to the octet rule", "short": "Octet exceptions", "label": "lecture+preview",
     "sources": "Day 9 p.27–30", "textbook": "§4.8, " + tbp(178, 183), "prereqs": ["t4-7", "m19"]},
    {"id": "t4-9", "sec": "4.9", "title": "Vibrating bonds and the greenhouse effect", "short": "Vibrating bonds", "label": "preview",
     "sources": "", "textbook": "§4.9, " + tbp(183, 185), "prereqs": ["t4-2", "m3"]},
    # ---------------------------------------------------------------- Ch. 5 (Day 10-11 lectures; all of Gilbert Ch. 5)
    {"id": "m20", "sec": "5.1–5.2", "title": "Molecular shape and VSEPR: steric number", "short": "VSEPR basics", "label": "lecture+preview",
     "sources": "Day 10 p.3, p.6–13", "textbook": "§5.1, " + tbp(198, 199) + "; §5.2 (no lone pairs), " + tbp(199, 203),
     "prereqs": ["m19", "t4-8"]},
    {"id": "m21", "sec": "5.2", "title": "Lone pairs: electron-pair vs. molecular geometry", "short": "Lone pairs and shape", "label": "lecture+preview",
     "sources": "Day 10 p.14–26", "textbook": "§5.2 (lone pairs), " + tbp(203, 209), "prereqs": ["m20", "t4-5"]},
    {"id": "m22", "sec": "5.3", "title": "Polar bonds and polar molecules", "short": "Polar molecules", "label": "lecture+preview",
     "sources": "Day 10 p.27–31; Day 11 p.6–8", "textbook": "§5.3, " + tbp(209, 212), "prereqs": ["t4-2", "m21"]},
    {"id": "m23", "sec": "5.4", "title": "Valence bond theory and hybrid orbitals", "short": "Hybrid orbitals", "label": "lecture+preview",
     "sources": "Day 11 p.9–16, p.20, p.24", "textbook": "§5.4 (valence bond theory; sp³, sp², sp), " + tbp(212, 219),
     "prereqs": ["m9", "m10", "m21"]},
    {"id": "m24", "sec": "5.4–5.5", "title": "π bonds and molecules with several central atoms", "short": "σ and π bonds", "label": "lecture+preview",
     "sources": "Day 11 p.17–26", "textbook": "§5.4 (sp² and sp), " + tbp(215, 219) + "; §5.5, " + tbp(219, 221),
     "prereqs": ["m23", "m19", "t4-5"]},
    {"id": "t5-6", "sec": "5.6", "title": "Chirality and molecular recognition", "short": "Chirality", "label": "lecture+preview",
     "sources": "Day 10 p.3, p.6", "textbook": "§5.6, " + tbp(221, 227), "prereqs": ["m20", "m23"]},
    {"id": "t5-7", "sec": "5.7", "title": "Molecular orbital theory", "short": "MO theory", "label": "lecture+preview",
     "sources": "Day 11 p.27; Day 12 p.4–13", "textbook": "§5.7, " + tbp(227, 239), "prereqs": ["m24", "t4-8", "m10"]},
    # ---------------------------------------------------------------- Ch. 18 §18.4-18.5 only (Day 12 p.14-25)
    {"id": "m25", "sec": "18.4–18.5", "title": "Metals, bands, and semiconductors", "short": "Band theory", "label": "lecture+preview",
     "sources": "Day 12 p.14–25", "textbook": "§18.4, " + tbp(884, 886) + "; §18.5, " + tbp(886, 887), "prereqs": ["t5-7", "m14", "m10", "m18"]},
]
for i, m in enumerate(MODULES, 1):
    m["n"] = i
    m["unit"] = next(u["id"] for u in UNITS if m["id"] in u["modules"])
assert [x for u in UNITS for x in u["modules"]] == [m["id"] for m in MODULES], "UNITS order must match MODULES"
LABEL_TEXT = {"lecture": "Covered in lecture", "preview": "Textbook preview", "lecture+preview": "Lecture + preview"}
STAGES = [["learn", "Learn"], ["understand", "Understand"], ["explore", "Explore"], ["attempt", "Attempt"],
          ["compare", "Compare"], ["practice", "Practice"], ["master", "Master"]]
MODULE_IDS = [m["id"] for m in MODULES]
KINDS = {"attempt", "practice", "transfer", "mastery", "mixed"}
ANSWER_TYPES = {"numeric", "choice", "multi", "order", "match", "text", "self", "config"}

# explorers a fragment may mount with data-explorer="name" (explorers.js, explorers_preview.js, explorers_ch4.js, explorers_ch5.js, explorers_ch18.js)
CH5_EXPLORERS = {"vsepr", "dipoles", "hybrid", "sigmaPi", "chirality", "moDiagram"}

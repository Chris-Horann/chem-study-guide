"""Concept-level coverage check for study-guides/CurrentCourseGuide.

    py -3.11 verification/CurrentCourseGuide/coverage_check.py

For every major concept of the in-scope sections (Gilbert Ch. 1-5; concept list from materials/TEXTBOOK_MAP.md
"Textbook preview notes", "Textbook notes: rest of Ch. 4", and "Textbook notes: Ch. 5", materials/COURSE_INDEX.md,
and the Day 9-11 lecture slides),
search the guide's teaching text, problems, and explorer code, and report where it is taught.
A concept counts as covered only if its own section's module (or the module that section maps to)
mentions it; hits elsewhere are listed but don't count. Writes coverage_report.md next to this file.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
GUIDE = os.path.join(HERE, "..", "..", "study-guides", "CurrentCourseGuide")

# section -> module(s) that own it
OWNER = {
    "1.1": ["m1"], "1.2": ["t1-2"], "1.3": ["t1-3"], "1.4": ["t1-4"], "1.5": ["t1-5"], "1.6": ["t1-6"],
    "1.7": ["t1-7"], "1.8": ["t1-8"], "1.9": ["t1-9"],
    "2.1": ["m2"], "2.2": ["t2-2"], "2.3": ["t2-3"], "2.4": ["t2-4"], "2.5": ["t2-5"], "2.6": ["t2-6"],
    "3.1": ["m3"], "3.2": ["m4"], "3.3": ["m5"], "3.4": ["m6"], "3.5": ["m7", "t3-5"], "3.6": ["m8"],
    "3.7": ["m9"], "3.8": ["m10"], "3.9": ["m11"], "3.10": ["m12"], "3.11": ["m13", "t3-11"], "3.12": ["m13"],
    "4.1": ["m14"], "4.2": ["t4-2"], "4.3": ["m15", "m16", "m17", "t4-3"], "4.4": ["m18", "m19"], "4.5": ["t4-5"],
    "4.6": ["t4-6"], "4.7": ["t4-7"], "4.8": ["t4-8"], "4.9": ["t4-9"],
    "5.1": ["m20", "t5-6"], "5.2": ["m20", "m21"], "5.3": ["m22"], "5.4": ["m23", "m24"], "5.5": ["m24"],
    "5.6": ["t5-6"], "5.7": ["t5-7"],
    "18.4": ["m25"], "18.5": ["m25"],          # Ch. 18: only the two sections Day 12 teaches
}
# §4.3 subsections: each must be covered by its own module, not just by any §4.3 module
SUB_OWNER = {"4.3 molecular": ["m17"], "4.3 transition": ["m16"], "4.3 polyatomic": ["m16"], "4.3 acids": ["t4-3"]}

# (section, concept, regex). Regexes run on tag-stripped text, case-insensitive.
CONCEPTS = [
    ("1.1", "scientific method: hypothesis, experiment, theory", r"hypothes"),
    ("1.1", "law vs. theory (laws describe, theories explain)", r"theor(y|ies)[^.]{0,80}explain|explain[^.]{0,80}theor"),
    ("1.1", "Law of Conservation of Mass", r"conservation of mass"),
    ("1.1", "Law of Constant Composition / Definite Proportions", r"constant composition|definite proportions"),
    ("1.1", "Law of Multiple Proportions", r"multiple proportions"),
    ("1.1", "Dalton's atomic theory (postulates)", r"dalton"),
    ("1.2", "COAST: Collect and Organize", r"collect and organi[sz]e"),
    ("1.2", "COAST: Analyze", r"\banalyze\b"),
    ("1.2", "COAST: Solve", r"\bsolve\b"),
    ("1.2", "COAST: Think About It", r"think about it"),
    ("1.2", "a framework, not a recipe; estimate first", r"not a recipe|estimate"),
    ("1.3", "pure substance: element vs. compound", r"pure substance"),
    ("1.3", "homogeneous vs. heterogeneous mixture; solution", r"homogeneous"),
    ("1.3", "physical vs. chemical property/process", r"chemical (property|properties|process|change)"),
    ("1.3", "intensive vs. extensive properties", r"intensive"),
    ("1.3", "density d = m/V", r"density"),
    ("1.3", "distillation (volatility)", r"distill"),
    ("1.3", "filtration (particle size)", r"filtrat"),
    ("1.3", "chromatography (stationary vs. mobile phase)", r"chromatograph"),
    ("1.4", "solid / liquid / gas definitions (shape, volume, compressibility)", r"compress"),
    ("1.4", "phase-change names (melting ... deposition)", r"sublimation"),
    ("1.4", "deposition", r"deposition"),
    ("1.4", "energy absorbed vs. released in phase changes", r"releases? energy|energy is released|absorbs? energy"),
    ("1.5", "energy = capacity to do work; w = F × d", r"capacity to do work|w = f"),
    ("1.5", "potential energy (position, composition; chemical energy)", r"potential energy"),
    ("1.5", "kinetic energy KE = ½mu²", r"½\s?mu|1/2\s?mu|kinetic energy"),
    ("1.5", "heat = transfer due to a temperature difference", r"\bheat\b"),
    ("1.5", "conservation of energy (lecture)", r"conservation of energy"),
    ("1.6", "diatomic elements", r"diatomic"),
    ("1.6", "molecular formula", r"molecular formula"),
    ("1.6", "structural and condensed structural formulas", r"condensed"),
    ("1.6", "ball-and-stick and space-filling models", r"space-filling"),
    ("1.6", "empirical formula", r"empirical formula"),
    ("1.6", "ionic compounds are not molecules (formula units)", r"not (a )?molecules?|formula unit"),
    ("1.7", "SI base units", r"base unit"),
    ("1.7", "SI prefixes", r"prefix"),
    ("1.7", "exact vs. uncertain values", r"exact"),
    ("1.7", "precision vs. accuracy", r"accura"),
    ("1.7", "significant-figure zero rules", r"leading zero|trailing zero|captive"),
    ("1.7", "scientific notation", r"scientific notation"),
    ("1.7", "rounding; round-half-to-even tie rule", r"even"),
    ("1.7", "weak-link rules for × ÷ and + −", r"decimal place"),
    ("1.8", "conversion factors as ratios equal to 1", r"conversion factor"),
    ("1.8", "dimensional analysis (units cancel)", r"cancel"),
    ("1.8", "temperature scales (K, °C, °F)", r"°f"),
    ("1.8", "cubing length factors for volume units", r"cub(e|ing)|cm<sup>3</sup>|cm³|m³"),
    ("1.8", "Gimli Glider / unit-error consequences", r"gimli|glider"),
    ("1.9", "mean", r"\bmean\b"),
    ("1.9", "standard deviation (n − 1)", r"standard deviation"),
    ("1.9", "confidence interval with t", r"confidence interval"),
    ("1.9", "normal distribution (68% within 1 s)", r"68|normal distribution|bell"),
    ("1.9", "outliers: Grubbs' test", r"grubbs"),
    ("1.9", "ethics: don't discard data without a reason", r"ethic|without a (valid )?reason"),
    ("1.9", "control samples", r"control"),
    ("2.1", "Thomson cathode rays / electron", r"cathode"),
    ("2.1", "Millikan oil drop / electron charge", r"millikan"),
    ("2.1", "Rutherford gold foil / nucleus", r"gold foil|gold-foil"),
    ("2.1", "plum-pudding model", r"pudding"),
    ("2.1", "radioactivity: α, β, γ", r"radioactiv"),
    ("2.1", "α particle = helium nucleus; β = electron", r"helium nucle|high-energy electron|β particle|beta particle"),
    ("2.1", "Chadwick / neutron", r"neutron"),
    ("2.2", "isotope", r"isotope"),
    ("2.2", "nuclide / nucleon", r"nuclide|nucleon"),
    ("2.2", "atomic number Z and mass number A", r"mass number"),
    ("2.2", "ion electrons = Z − charge", r"z − |z - |electrons = z"),
    ("2.3", "Mendeleev", r"mendeleev"),
    ("2.3", "periods and groups", r"period"),
    ("2.3", "metals, nonmetals, metalloids", r"metalloid"),
    ("2.3", "main-group vs. transition metals", r"transition metal"),
    ("2.3", "lanthanides and actinides", r"lanthanide|actinide"),
    ("2.3", "group names (alkali, alkaline earth, chalcogens, halogens, noble gases)", r"alkaline earth|chalcogen"),
    ("2.3", "common monatomic ion charges", r"common ion|ion charge|charges? of"),
    ("2.4", "atomic mass unit", r"\bamu\b|\bu\b|unified atomic"),
    ("2.4", "average atomic mass (weighted)", r"weighted"),
    ("2.4", "two-isotope abundance problems (x and 1 − x)", r"1 − x|1 - x"),
    ("2.4", "molecular mass", r"molecular mass"),
    ("2.4", "formula mass / formula unit", r"formula mass"),
    ("2.5", "the mole / Avogadro's number", r"avogadro|n<sub>a</sub>|na ="),
    ("2.5", "molar mass", r"molar mass"),
    ("2.5", "mass ↔ moles ↔ particles map", r"particles"),
    ("2.6", "mass spectrometer, m/z", r"m/z"),
    ("2.6", "molecular ion M⁺", r"molecular ion|molecular-ion"),
    ("2.6", "fragment ions", r"fragment"),
    ("2.6", "isotope peaks (Cl 35/37)", r"37|isotope peak"),
    ("3.1", "wavelength, frequency, c = λν", r"λν|λ ν|c = λ"),
    ("3.1", "EM spectrum regions", r"ultraviolet|infrared|microwave"),
    ("3.1", "Maxwell's oscillating electric and magnetic fields", r"maxwell|magnetic field"),
    ("3.1", "hertz (s⁻¹)", r"hertz|\bhz\b"),
    ("3.2", "emission vs. absorption line spectra", r"absorption"),
    ("3.2", "continuous spectrum", r"continuous"),
    ("3.3", "blackbody radiation", r"blackbody|black body|black-body"),
    ("3.3", "Planck: quantized energy, E = hν", r"planck"),
    ("3.3", "photoelectric effect", r"photoelectric"),
    ("3.3", "threshold / work function φ", r"threshold|work function"),
    ("3.4", "Balmer equation", r"balmer"),
    ("3.4", "Rydberg equation", r"rydberg"),
    ("3.4", "Bohr model energy levels", r"bohr"),
    ("3.4", "ionization from level n (n → ∞)", r"∞"),
    ("3.5", "de Broglie wavelength λ = h/mu", r"de broglie"),
    ("3.5", "Heisenberg uncertainty principle", r"heisenberg"),
    ("3.5", "standing waves", r"standing wave"),
    ("3.6", "principal quantum number n", r"principal"),
    ("3.6", "angular momentum ℓ, magnetic mℓ", r"magnetic quantum|m<sub>ℓ</sub>|mℓ"),
    ("3.6", "spin quantum number ms", r"spin"),
    ("3.6", "Pauli exclusion principle", r"pauli"),
    ("3.7", "orbital shapes s, p, d", r"dumbbell|lobe"),
    ("3.7", "radial distribution / probability", r"radial"),
    ("3.7", "nodes", r"\bnode"),
    ("3.7", "boundary surface (90%)", r"boundary"),
    ("3.8", "Aufbau principle / filling order", r"aufbau"),
    ("3.8", "Hund's rule", r"hund"),
    ("3.8", "orbital diagrams", r"orbital (box|diagram)|box"),
    ("3.8", "noble-gas core notation", r"noble-gas core|\[ar\]|\[ne\]"),
    ("3.8", "valence vs. core electrons", r"valence"),
    ("3.8", "shielding / penetration / Z_eff", r"shield|penetrat|z<sub>eff</sub>"),
    ("3.8", "degenerate orbitals", r"degenerate"),
    ("3.8", "excited states (preview)", r"excited"),
    ("3.8", "exceptions Cr, Cu (preview; ignored in class)", r"exception"),
    ("3.8", "blocks of the periodic table (s, p, d, f)", r"block"),
    ("3.9", "cation configurations: highest n first", r"highest n|highest-n"),
    ("3.9", "anion configurations", r"anion"),
    ("3.9", "isoelectronic", r"isoelectronic"),
    ("3.10", "atomic radius trends", r"atomic radi"),
    ("3.10", "ionic radius: cations smaller, anions larger", r"ionic radi|cations? (are )?smaller|cation &lt; atom &lt; anion|cation < atom < anion"),
    ("3.11", "first ionization energy trend", r"ionization energ"),
    ("3.11", "successive ionization energies", r"successive"),
    ("3.11", "photoelectron spectroscopy (preview)", r"photoelectron"),
    ("3.12", "electron affinity", r"electron affinit"),
    ("4.1", "ionic, covalent, metallic bonds", r"metallic"),
    ("4.1", "Coulomb E_el", r"e<sub>el</sub>|coulomb"),
    ("4.1", "lattice energy", r"lattice energ"),
    ("4.1", "greenhouse gases (preview)", r"greenhouse"),
    ("4.1", "H–H bond energy curve: bond length, bond energy (Day 8 p.11)", r"bond length|bond energy"),
    ("4.1", "electron sea (Day 8 p.14)", r"\bsea\b"),
    ("4.1", "Table 4.1: transferred / shared / delocalized electrons (Day 8 p.15)", r"delocalized"),
    ("4.1", "valence = bonding capacity", r"bonding capacity|valence"),
    ("4.2", "polar covalent bond", r"polar covalent"),
    ("4.2", "dipole; δ+ / δ−; crossed arrow", r"dipole|δ\+"),
    ("4.2", "electronegativity χ", r"electronegativ"),
    ("4.2", "Δχ cutoffs 0.4 / 2.0", r"0\.4"),
    ("4.2", "electronegativity trend (like IE₁)", r"increases? across|across a (row|period)"),
    ("4.3", "binary ionic formulas by charge balance", r"charge"),
    ("4.3", "naming: cation + anion -ide, no prefixes", r"-ide|ide\b"),
    ("4.3", "why no prefixes: characteristic charges (textbook)", r"prefix"),
    ("4.3 molecular", "binary molecular names: prefixes (Table 4.3)", r"penta|hexa|tetra"),
    ("4.3 molecular", "no mono on the first element", r"mono[^.]{0,60}first element|first element[^.]{0,60}mono"),
    ("4.3 molecular", "vowel dropped before oxide (textbook)", r"monoxide|pentoxide|tetroxide|heptoxide"),
    ("4.3 molecular", "which element is written first (textbook)", r"to the left of|written first|comes first"),
    ("4.3 transition", "Roman numeral = transition-metal ion charge", r"roman numeral"),
    ("4.3 transition", "copper (I)/(II) oxide; historical names not required", r"copper ?\(i\) oxide|cuprous|historical"),
    ("4.3 transition", "one-cation metals Ag, Cd, Zn take no numeral (textbook)", r"zn<sup>2\+</sup>|zinc"),
    ("4.3 polyatomic", "polyatomic ions: covalently bonded, overall charge", r"polyatomic"),
    ("4.3 polyatomic", "ion table provided on exams (Day 8 p.8)", r"provided with a table|provided on exams"),
    ("4.3 polyatomic", "-ate vs. -ite; per- and hypo-", r"hypochlor|perchlor"),
    ("4.3 polyatomic", "parentheses for multiple polyatomic ions (textbook)", r"parenthes"),
    ("4.3 polyatomic", "hydrogen-containing oxoanions; bicarbonate", r"bicarbonate|hydrogen carbonate"),
    ("4.3 acids", "binary acids: hydro-…-ic acid; (aq)", r"hydro[a-z]*ic acid"),
    ("4.3 acids", "oxoacids: -ate → -ic, -ite → -ous", r"-ous|ous acid"),
    ("4.4", "octet rule; hydrogen needs two", r"octet rule"),
    ("4.4", "Lewis symbols: dots one per side before pairing", r"one (at a time|per side) before pairing"),
    ("4.4", "bonding capacity = unpaired electrons", r"bonding capacity"),
    ("4.4", "carbon almost always forms 4 bonds (memorize)", r"almost always"),
    ("4.4", "Lewis structures of ionic compounds: brackets (textbook)", r"bracket"),
    ("4.4", "bonding pair, lone pair, single bond", r"lone pair"),
    ("4.4", "the five steps", r"five steps"),
    ("4.4", "central atom: largest bonding capacity", r"largest <strong>bonding capacity|largest bonding capacity"),
    ("4.4", "valence electrons of ions: add/subtract for charge (textbook)", r"negative charge|for the 1− charge|each negative"),
    ("4.4", "double and triple bonds (O₂, N₂, ethyne)", r"triple bond"),
    ("4.4", "Lewis structures are two-dimensional (textbook)", r"two-dimensional|3-d shape|flat"),
    ("4.5", "allotropes: O₂ vs. O₃ (Day 8 p.27)", r"allotrope"),
    ("4.5", "resonance structures (definition)", r"resonance structure"),
    ("4.5", "ozone: two equal 128 pm bonds", r"128 pm"),
    ("4.5", "delocalization", r"delocali"),
    ("4.5", "double-headed arrow ↔", r"↔|double-headed"),
    ("4.5", "resonance stabilization", r"resonance stabilization"),
    ("4.5", "nitrate: three equivalent structures", r"nitrate"),
    ("4.5", "test: single and double bonds to the same element; benzene", r"benzene"),
    ("4.6", "bond order", r"bond order"),
    ("4.6", "length decreases, energy increases with bond order", r"shorter|decreases"),
    ("4.6", "bond energy: break 1 mol in the gas phase, always positive", r"gas phase"),
    ("4.6", "Table 4.6 average values (799 vs. 743)", r"799"),
    ("4.6", "fractional bond order from resonance (carbonate 1.33)", r"1\.33|4/3"),
    ("4.7", "formal charge is bookkeeping, not a real charge", r"not a real charge|accounting"),
    ("4.7", "Eq. 4.2: FC = V − [LP + ½ shared]", r"lone-pair e|½"),
    ("4.7", "FCs sum to 0 or the ion's charge", r"add up to"),
    ("4.7", "three criteria for the best structure", r"criteri"),
    ("4.7", "N₂O structures A, B, C", r"n<sub>2</sub>o"),
    ("4.7", "shortcut: bonds vs. bonding capacity", r"one more bond|one fewer"),
    ("4.7", "reality check: the best FC structure isn't the whole story", r"reality check|contributes|between a and b|between structures a and b"),
    ("4.8", "electron-deficient Be, B, Al", r"electron-deficient"),
    ("4.8", "odd-electron molecules, free radicals (NO, NO₂)", r"free radical"),
    ("4.8", "NO₂ dimerizes to N₂O₄", r"n<sub>2</sub>o<sub>4</sub>"),
    ("4.8", "expanded octets for Z > 12 (PCl₅, SF₆)", r"z &gt; 12|z > 12"),
    ("4.8", "d orbitals contribute little", r"contribute little"),
    ("4.8", "sulfate/phosphate: expanded octet lowers formal charges", r"sulfate|phosphate"),
    ("4.9", "bonds vibrate: stretch and bend", r"stretch"),
    ("4.9", "IR absorption needs a fluctuating field (charge separation)", r"fluctuat"),
    ("4.9", "CO₂: symmetric stretch IR-inactive; asymmetric and bend active", r"symmetric stretch"),
    ("4.9", "greenhouse effect: absorb and re-emit in all directions", r"re-emit|reemit"),
    ("4.9", "N₂ and O₂ are IR-inactive", r"n<sub>2</sub> and o<sub>2</sub>"),
    ("4.9", "Earth's surface (287 K) emits infrared", r"287 k"),
    # Day 9 lecture (Ch. 4 sections now taught)
    ("4.2", "electronegativity, symbol χ, and the slide's χ table (Day 9 p.17)", r"χ"),
    ("4.2", "Δχ guidelines 0.4 and 2.0 (Day 9 p.18)", r"2\.0"),
    ("4.2", "polar bond: the battery analogy, δ+ and δ− (Day 9 p.15)", r"battery"),
    ("4.2", "electrostatic potential maps (Day 9 p.16)", r"potential map|electrostatic potential"),
    ("4.5", "curved arrows move electrons between resonance structures (Day 9 p.9)", r"curved arrow"),
    ("4.5", "the molecule does not switch back and forth (Day 9 p.9)", r"back and forth"),
    ("4.5", "resonance hybrid with dashed partial bonds (Day 9 p.10)", r"resonance hybrid|partial bond"),
    ("4.5", "Kekulé's benzene (Day 9 p.12–13)", r"kekul"),
    ("4.6", "Table 4.6 on the slide (Day 9 p.14)", r"day 9 p\.14"),
    ("4.7", "the professor's four steps for formal charge (Day 9 p.22)", r"day 9 p\.22"),
    ("4.7", "phosphoric acid Top Hat (Day 9 p.26)", r"phosphoric acid|h<sub>3</sub>po<sub>4</sub>"),
    ("4.8", "hypervalency “not well understood” (Day 9 p.29)", r"hypervalen"),
    ("4.8", "expanded octets give formal charges closer to zero (Day 9 p.29)", r"closer to zero"),
    # Chapter 5 (Day 10-11 lecture; §5.6-5.7 mostly textbook preview)
    ("5.1", "Lewis structures are flat; molecules are 3-D (Day 10 p.6–7)", r"flat|two-dimensional|2-d|3-d"),
    ("5.1", "CO₂ 180° and CH₄ 109.5° vs. the Lewis drawing (Day 10 p.7)", r"109\.5"),
    ("5.1", "molecular recognition (textbook)", r"molecular recognition"),
    ("5.2", "VSEPR: electron pairs repel and spread out (Day 10 p.8)", r"repul"),
    ("5.2", "electron-pair geometry vs. molecular geometry (Day 10 p.8)", r"electron-pair geometry"),
    ("5.2", "steric number (Day 10 p.9)", r"steric number"),
    ("5.2", "electron domains (Day 10 p.26)", r"electron domain"),
    ("5.2", "trigonal bipyramidal: axial and equatorial positions", r"equatorial"),
    ("5.2", "octahedral (SF₆)", r"octahedral"),
    ("5.2", "double bonds repel more: formaldehyde about 118° (Day 10 p.13)", r"118"),
    ("5.2", "ozone bent, 117° (Day 10 p.14–15)", r"117"),
    ("5.2", "ammonia trigonal pyramidal, 107° (Day 10 p.16–18)", r"107"),
    ("5.2", "water bent, 104.5° (Day 10 p.19)", r"104\.5"),
    ("5.2", "SN 5 lone pairs equatorial: seesaw", r"seesaw|see-saw"),
    ("5.2", "SN 5: T-shaped", r"t-shaped"),
    ("5.2", "SN 6: square pyramidal (Day 10 p.24)", r"square pyramidal"),
    ("5.2", "SN 6: square planar, lone pairs opposite (Day 10 p.25)", r"square planar"),
    ("5.2", "the professor's summary table (Day 10 p.26)", r"day 10 p\.26"),
    ("5.2", "repulsion ranking: lone pair > double bond > single bond (textbook)", r"lone pair.{0,80}(bonding pair|double bond)"),
    ("5.2", "wedge-and-dash drawings (textbook)", r"wedge"),
    ("5.2", "BrF₅'s 85° (textbook)", r"85°"),
    ("5.3", "bond dipole (textbook term)", r"bond dipole"),
    ("5.3", "bond dipoles add as vectors; they can cancel", r"cancel"),
    ("5.3", "CO₂ and CF₄ nonpolar despite polar bonds (Day 10 p.29–30)", r"cf<sub>4</sub>"),
    ("5.3", "water polar: dipoles not perfectly opposed (Day 10 p.31)", r"perfectly opposed"),
    ("5.3", "dipole moment μ in debyes", r"debye"),
    ("5.3", "Table 5.2 values (Day 11 p.8)", r"1\.85"),
    ("5.3", "CHCl₃ vs. CCl₃F (Day 11 p.7)", r"ccl<sub>3</sub>f"),
    ("5.3", "C–H essentially nonpolar (textbook)", r"essentially nonpolar"),
    ("5.3", "polar molecules align in an electric field (textbook)", r"electric field"),
    ("5.4", "valence bond theory (Day 11 p.9)", r"valence bond"),
    ("5.4", "overlap of half-filled orbitals (Day 11 p.9)", r"half-filled"),
    ("5.4", "σ bond: density between the nuclei, along the axis (Day 11 p.10)", r"σ bond"),
    ("5.4", "the methane problem; promotion rejected (Day 11 p.11)", r"promot"),
    ("5.4", "hybridization mixes (averages) orbitals (Day 11 p.12)", r"averag|mix"),
    ("5.4", "number of hybrids = steric number (Day 11 p.12)", r"steric number"),
    ("5.4", "sp³ hybrids (CH₄, NH₃, H₂O)", r"sp<sup>3</sup>"),
    ("5.4", "sp² hybrids", r"sp<sup>2</sup>"),
    ("5.4", "major and minor lobes (Day 11 p.14)", r"minor lobe|major lobe"),
    ("5.4", "lone pairs reside in hybrid orbitals; H uses 1s (Day 11 p.20)", r"1s"),
    ("5.4", "Table 5.3 (Day 11 p.24) and its sp³ row slip", r"table 5\.3"),
    ("5.4", "π bond: side-to-side overlap of unhybridized p orbitals (Day 11 p.17, p.20)", r"side-to-side|side by side"),
    ("5.5", "a double bond is one σ and one π bond (Day 11 p.17)", r"σ and (one )?π|σ bond and a π bond|one σ"),
    ("5.5", "π density above and below the plane (Day 11 p.19)", r"above and below"),
    ("5.5", "diazene, N₂H₂ (Day 11 p.22)", r"diazene"),
    ("5.5", "acetylene: sp, two π bonds (Day 11 p.23)", r"acetylene"),
    ("5.5", "ethylene: all six atoms in one plane (Day 11 p.25)", r"ethylene"),
    ("5.5", "acrolein (Day 11 p.26)", r"acrolein"),
    ("5.5", "benzene's delocalized π electrons (Day 11 p.26)", r"delocali"),
    ("5.5", "conjugation (textbook)", r"conjugat"),
    ("5.5", "aromatic compounds and PAHs (textbook)", r"aromatic|naphthalene|polycyclic"),
    ("5.6", "carvone (Day 10 p.6)", r"carvone"),
    ("5.6", "chiral: not superimposable on its mirror image", r"superimpos"),
    ("5.6", "enantiomers", r"enantiomer"),
    ("5.6", "stereocenter: four different groups", r"stereocenter|chiral carbon"),
    ("5.6", "stereoisomers and isomers", r"stereoisomer"),
    ("5.6", "optical activity: (+) clockwise, (−) counterclockwise", r"polarimeter|plane-polarized|counterclockwise"),
    ("5.6", "racemic mixture", r"racemic"),
    ("5.6", "chiral drugs (albuterol, dextro- and levomethorphan)", r"albuterol|methorphan"),
    ("5.6", "planar molecules cannot be chiral", r"planar"),
    ("5.7", "O₂ is paramagnetic (Day 11 p.27)", r"paramagnetic"),
    ("5.7", "diamagnetic", r"diamagnetic"),
    ("5.7", "molecular orbitals belong to the whole molecule", r"molecular orbital"),
    ("5.7", "bonding vs. antibonding orbitals", r"antibonding"),
    ("5.7", "bond order = ½(bonding − antibonding) (Eq. 5.2)", r"½"),
    ("5.7", "He₂ does not exist", r"he<sub>2</sub>"),
    ("5.7", "two MO orders: π₂p below σ₂p for Z ≤ 7", r"z ≤ 7|z &le; 7|li<sub>2</sub>"),
    ("5.7", "Hund's rule fills the degenerate π* orbitals", r"hund"),
    ("5.7", "NO: bond order 2.5", r"2\.5"),
    ("5.7", "ions of O₂: bond orders and lengths", r"o<sub>2</sub><sup>"),
    ("5.7", "auroras and Table 5.4 (textbook)", r"aurora"),
    ("5.7", "ozone's delocalized π system: bond order 1.5 (textbook)", r"1\.5"),
    ("5.7", "SN > 4 without expanded octets (textbook) vs. the slides' expanded octets", r"expand"),
    ("5.7", "HOMO and LUMO (Day 12 p.11)", r"\bHOMO\b"),
    ("5.7", "one MO out for every atomic orbital put in (Day 12 p.7)", r"one molecular orbital out for every atomic orbital|one MO (out )?for every atomic orbital"),
    ("5.7", "which theory answers which question: Lewis, VSEPR/VBT, MO (Day 12 p.13)", r"Theories of Bonding"),
    # Ch. 18 §18.4-18.5 (Day 12 p.14-25; textbook PDF p.918-921)
    ("18.4", "properties of metals: malleable, ductile, conductors (Day 12 p.17)", r"malleable"),
    ("18.4", "metalloids on the periodic table (Day 12 p.16)", r"metalloid"),
    ("18.4", "one MO for every atomic orbital: N atoms give N MOs", r"one molecular orbital out for every atomic orbital"),
    ("18.4", "Na₂ and Na₄: the HOMO–LUMO gap shrinks as atoms are added", r"homo.{0,3}lumo gap"),
    ("18.4", "band theory, an extension of MO theory (textbook)", r"band theory"),
    ("18.4", "valence band", r"valence band"),
    ("18.4", "conduction band", r"conduction band"),
    ("18.4", "conductor: a partially filled band, or a filled band overlapping an empty one", r"partially filled"),
    ("18.4", "sodium: a half-filled 3s band overlapping the 3p band", r"3p"),
    ("18.4", "zinc: a filled 4s band overlapping the empty 4p band", r"4p"),
    ("18.4", "weak, diffuse metal–metal bonds; Na bcc with eight neighbors (textbook)", r"eight others|body-centered"),
    ("18.5", "band gap, E_g", r"band gap"),
    ("18.5", "insulator: a large enough band gap (diamond)", r"insulator"),
    ("18.5", "semiconductor: a small gap (silicon)", r"semiconductor"),
    ("18.5", "heating a semiconductor promotes more electrons (Day 12 p.24)", r"T ↑|heat"),
    ("18.5", "Si band gap 106 kJ/mol (textbook)", r"106 kJ"),
    ("18.5", "doping and dopants", r"dopant"),
    ("18.5", "n-type: donor level just below the conduction band", r"donor level"),
    ("18.5", "p-type: acceptor level just above the valence band", r"acceptor level"),
    ("18.5", "holes (textbook)", r"\bholes?\b"),
    ("18.5", "group 13–15 compound semiconductors and LEDs (textbook)", r"gaas|light-emitting"),
]


def strip(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s))


def main():
    html = open(os.path.join(GUIDE, "index.html"), encoding="utf-8").read()
    s = open(os.path.join(GUIDE, "assets", "data.js"), encoding="utf-8").read()
    D = json.loads(s[s.index("window.GUIDE_DATA = ") + 20:].rstrip().rstrip(";"))
    # teaching text per module (with markup kept for sub/sup patterns, and stripped)
    secs = [(m.group(1), m.start()) for m in re.finditer(r"""<section[^>]*data-module=['"]([^'"]+)['"]""", html)]
    text = {}
    for i, (mid, st) in enumerate(secs):
        en = secs[i + 1][1] if i + 1 < len(secs) else len(html)
        text[mid] = html[st:en]
    for p in D["problems"]:
        mid = p["module"] if p["module"] != "mixed" else p.get("home", "mixed")
        blob = " ".join([p.get("prompt", ""), p.get("solution", ""), json.dumps(p.get("compare", ""), ensure_ascii=False),
                         " ".join(p.get("hints", [])), json.dumps(p["answer"], ensure_ascii=False)])
        text[mid] = text.get(mid, "") + " " + blob
    ex = {}
    for f in ("explorers.js", "explorers_preview.js", "explorers_ch4.js", "explorers_ch5.js", "explorers_ch18.js"):
        ex[f] = open(os.path.join(GUIDE, "assets", f), encoding="utf-8").read()
    rows, gaps = [], []
    for sec, concept, rx in CONCEPTS:
        r = re.compile(rx, re.I)
        owners = SUB_OWNER.get(sec) or OWNER[sec]
        own = [m for m in owners if r.search(text.get(m, "")) or r.search(strip(text.get(m, "")))]
        other = sorted(m for m in text if m not in owners and (r.search(text[m]) or r.search(strip(text[m]))))
        exp = [f for f, t in ex.items() if r.search(t)]
        status = "covered" if own else "GAP"
        if not own:
            gaps.append((sec, concept))
        ev = ""
        for m in own:
            t = strip(text.get(m, ""))
            mm = r.search(t)
            if mm:
                ev = t[max(0, mm.start() - 50): mm.end() + 60].strip().replace("|", "/")
                break
        rows.append((sec, concept, status, ", ".join(own) or "—", ", ".join(other[:6]) + (" …" if len(other) > 6 else ""),
                     ", ".join(exp), ev))
    out = ["# Concept coverage: CurrentCourseGuide", "",
           "Generated by `coverage_check.py`. A concept is covered when its own section's module teaches or practices it.", "",
           f"**{len(CONCEPTS) - len(gaps)} of {len(CONCEPTS)} concepts covered; gaps: {len(gaps)}.**", "",
           "| § | concept | status | owning module | also in | explorer code | evidence (owning module) |", "|---|---|---|---|---|---|---|"]
    out += ["| " + " | ".join(r) + " |" for r in rows]
    open(os.path.join(HERE, "coverage_report.md"), "w", encoding="utf-8").write("\n".join(out) + "\n")
    print(f"{len(CONCEPTS) - len(gaps)} / {len(CONCEPTS)} covered")
    for g in gaps:
        print("GAP", g[0], g[1])
    sys.exit(1 if gaps else 0)


if __name__ == "__main__":
    main()

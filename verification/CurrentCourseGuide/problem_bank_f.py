"""Problem bank F: Ch. 4 naming and Lewis-structure modules (Day 8 + textbook §4.3–4.4):
m16 transition-metal and polyatomic-ion names, m17 covalent names, t4-3 acids (textbook preview),
m18 Lewis symbols and the octet rule, m19 Lewis structures (the five steps)."""
from guide_common import *
from problem_bank_a import PROBLEMS, add, num_ans, choice
from problem_bank_b import text_ans, formula_ans, order_ans, TOPHAT_NOTE
from problem_bank_c import P, tb
import lewis as LW

CH4_START = len(PROBLEMS)   # first Ch. 4 problem; bank G rotates choice options from here on (choice_order.py)


def LS(sid, **kw):
    """Compact Lewis-structure SVG for prompts, options, and solutions (inline <span>, valid inside <p> and <label>).
    neutral=True: a screen-reader description without the species' name, for multiple-choice options."""
    kw.setdefault("scale", 0.78)
    kw.setdefault("tag", "span")
    if kw.pop("neutral", False):
        kw.setdefault("label", LW.describe(LW.STRUCTS[sid], named=False))
    return LW.svg(LW.STRUCTS[sid], **kw)


def LX(name, atoms, bonds, lp, charge=0, **kw):
    """An ad-hoc (possibly wrong) structure for a multiple-choice option; not a checked structure."""
    kw.setdefault("scale", 0.78)
    kw.setdefault("tag", "span")
    st = LW.Structure("x", name, "", atoms, bonds, lp, charge=charge)
    if kw.pop("neutral", False):
        kw.setdefault("label", LW.describe(st, named=False))
    return LW.svg(st, **kw)


def names(*base):
    """Accept the standard 'copper(I) oxide' and the slides' spacing 'copper (I) oxide' (Day 8 p.7)."""
    out = []
    for b in base:
        out += [b, b.replace("(", " (")]
    return out


def tname(accepted, traps=None, covalent=False, placeholder="name"):
    a = text_ans(accepted, ci=True, placeholder=placeholder)
    if covalent:
        a["prefixesAllowed"] = True
    if traps:
        a["traps"] = [{"answers": t[0], "message": t[1]} for t in traps]
    return a


def tformula(accepted, traps=None, placeholder="e.g., MgCl2"):
    a = formula_ans(accepted, placeholder=placeholder)
    if traps:
        a["traps"] = [{"answers": t[0], "message": t[1]} for t in traps]
    return a


def tnum(value, traps=None, **kw):
    kw.setdefault("tol", 0)
    a = num_ans(value, **kw)
    if traps:
        a["traps"] = [{"value": v, "tol": 0, "message": m} for v, m in traps]
    return a


HIST = "That's the historical name. The course uses the systematic, Roman-numeral name; historical names: “we're not going to worry about them” (Day 8 p.7)."
NUMERAL = "The Roman numeral is the charge on each metal ion, not the number of metal atoms in the formula."
PREFIX_IONIC = ("This is ionic (a metal and a nonmetal), so it's named cation + anion with no prefixes (Day 7 p.21). "
                "Prefixes are for covalent compounds (Day 8 p.12).")

# =====================================================================================
# m16  Naming ionic compounds: transition metals and polyatomic ions (Day 8 p.6–10; textbook §4.3)
# =====================================================================================
add(id="m16-attempt", module="m16", kind="attempt", level="Guided attempt",
    prompt="<p>Copper forms more than one sulfide. One of them has the formula Cu<sub>2</sub>S. What is its systematic name?</p>",
    answer=tname(names("copper(I) sulfide", "copper(I) sulphide"),
                 traps=[(names("copper(II) sulfide", "copper(II) sulphide"), NUMERAL + " Two Cu ions balance one S<sup>2−</sup>, so each Cu is +1."),
                        (["dicopper sulfide", "dicopper monosulfide"], PREFIX_IONIC),
                        (["copper sulfide"], "Copper has more than one common ion, so the name must say which one: add a Roman numeral for its charge (Day 8 p.7)."),
                        (["cuprous sulfide"], HIST)]),
    hints=["Copper is a transition metal with more than one common ion, so the name needs a Roman numeral for the metal's charge (Day 8 p.7).",
           "Sulfur is in group 16, like O (O<sup>2−</sup>, Day 7 p.19): it gains 2 electrons to fill its valence shell (Day 7 p.18), giving S<sup>2−</sup>, sulfide.",
           "The total charge must be zero (Day 7 p.20): 2 × (charge on each Cu) + (−2) = 0.",
           "Each Cu is +1, so the numeral is (I), and the anion is sulfide."],
    solution="<p>2 Cu<sup>+</sup> (+2) + S<sup>2−</sup> (−2) = 0, so each copper is +1: <strong>copper(I) sulfide</strong> "
             "(the slides space it “copper (I)”). It's the same reasoning as Cu<sub>2</sub>O, copper (I) oxide, on Day 8 p.7.</p>",
    compare={"wrong": "<p>“Copper(II) sulfide”, read off the subscript 2.</p>",
             "tempting": "The only number in the formula is the 2, and the other copper oxide on the slide was “(II)”.",
             "fails": "The subscript counts copper ions; the numeral is each ion's charge. Two ions share the 2− charge of sulfide, so each is +1. Copper(II) sulfide is CuS, a different compound."},
    source="Day 8 p.7; Day 7 p.19–20")

add(id="m16-tophat", module="m16", kind="practice", level="In-class Top Hat",
    signal=TOPHAT_NOTE,
    prompt="<p>“What is the systematic name for Fe<sub>2</sub>O<sub>3</sub>?” (Day 8 p.10)</p>",
    answer=tname(names("iron(III) oxide"),
                 traps=[(names("iron(II) oxide"), NUMERAL + " Three O<sup>2−</sup> carry −6, so the two Fe carry +6."),
                        (["diiron trioxide"], PREFIX_IONIC), (["ferric oxide"], HIST), (["iron oxide"], "Iron has more than one common ion; the name needs its charge as a Roman numeral (Day 8 p.7).")]),
    hints=["Oxide is O<sup>2−</sup> (group 16); three of them carry 6−.", "Two iron ions must total +6."],
    solution="<p>3 O<sup>2−</sup> = −6, so 2 Fe = +6 and each Fe is +3: <strong>iron(III) oxide</strong> (“iron (III) oxide” in the slides' spacing).</p>",
    source="Day 8 p.10; Day 7 p.19–20")

add(id="m16-p1", module="m16", kind="practice", level="Warm-up",
    prompt="<p>Write the formula of iron(II) chloride.</p>",
    answer=tformula(["FeCl2"], traps=[(["FeCl3"], "That's iron(III) chloride. (II) means Fe<sup>2+</sup>, which needs two Cl<sup>−</sup>."),
                                      (["Fe2Cl"], "The numeral isn't a subscript: (II) is the charge, +2, so one Fe<sup>2+</sup> needs two Cl<sup>−</sup>.")]),
    hints=["(II) → Fe<sup>2+</sup>; chloride is Cl<sup>−</sup>.", "How many Cl<sup>−</sup> cancel +2?"],
    solution="<p>Fe<sup>2+</sup> + 2 Cl<sup>−</sup> → <strong>FeCl<sub>2</sub></strong>.</p>",
    source="Day 8 p.7; Day 7 p.20")

add(id="m16-p2", module="m16", kind="practice", level="Standard",
    prompt="<p>Name K<sub>2</sub>CO<sub>3</sub>.</p>",
    answer=tname(["potassium carbonate"],
                 traps=[(["dipotassium carbonate"], PREFIX_IONIC),
                        (["potassium carbon trioxide", "potassium carbon oxide"], "CO<sub>3</sub><sup>2−</sup> is one polyatomic ion, carbonate. Name it as a unit (Day 8 p.8–9)."),
                        (["potassium carbide"], "Carbide would be a C-only anion. CO<sub>3</sub><sup>2−</sup> is carbonate (Day 8 p.8).")]),
    hints=["K is in group 1: K<sup>+</sup>.", "CO<sub>3</sub><sup>2−</sup> is in the polyatomic-ion table: carbonate."],
    solution="<p>2 K<sup>+</sup> + CO<sub>3</sub><sup>2−</sup>: cation name, then the polyatomic ion's name, <strong>potassium carbonate</strong>, "
             "the same rule as LiNO<sub>3</sub>, lithium nitrate (Day 8 p.9). No prefix for the two K<sup>+</sup> ions.</p>",
    source="Day 8 p.8–9")

P(id="m16-p3", module="m16", kind="practice", level="Textbook preview",
  prompt="<p>Write the formula of ammonium phosphate.</p>",
  answer=tformula(["(NH4)3PO4"], traps=[(["NH4PO4"], "Check the charges: NH<sub>4</sub><sup>+</sup> is +1 and PO<sub>4</sub><sup>3−</sup> is −3, so the formula needs three ammonium ions."),
                                       (["NH43PO4"], "Right ions and ratio, but NH43 reads as “N, H<sub>43</sub>.” Put ammonium in parentheses: (NH4)3PO4.")],
                  placeholder="e.g., Ca(NO3)2"),
  hints=["Ammonium is NH<sub>4</sub><sup>+</sup>; phosphate is PO<sub>4</sub><sup>3−</sup> (polyatomic-ion table).",
         "Three NH<sub>4</sub><sup>+</sup> balance one PO<sub>4</sub><sup>3−</sup>. Wrap the repeated ion in parentheses."],
  solution="<p>3 NH<sub>4</sub><sup>+</sup> + PO<sub>4</sub><sup>3−</sup> → <strong>(NH<sub>4</sub>)<sub>3</sub>PO<sub>4</sub></strong>. "
           "The parentheses make the subscript 3 apply to the whole ammonium ion, as in the textbook's Mg<sub>3</sub>(PO<sub>4</sub>)<sub>2</sub> (§4.3, Sample Ex. 4.6, PDF p.193). "
           "The lecture's examples, LiNO<sub>3</sub>, NaHCO<sub>3</sub>, and NH<sub>4</sub>ClO<sub>2</sub>, were all 1 : 1 and needed none (Day 8 p.9).</p>",
  source=tb("4.3", 192, 193) + "; Day 8 p.8")

add(id="m16-p4", module="m16", kind="practice", level="Concept",
    prompt="<p>Why isn't “copper oxide” a complete name?</p>",
    answer=choice(("Copper forms more than one common ion (Cu<sup>+</sup> and Cu<sup>2+</sup>), so it could mean CuO or Cu<sub>2</sub>O.", True,
                   "Right: “These different ions have different chemical properties, so we need to be able to name them differently” (Day 8 p.7)."),
                  ("Oxide can carry different charges.", False, "Oxide is O<sup>2−</sup> (group 16) in both compounds."),
                  ("Copper is a nonmetal, so the name needs prefixes.", False, "Copper is a transition metal, and ionic names use no prefixes."),
                  ("Oxygen is written first in the formula.", False, "The formulas CuO and Cu<sub>2</sub>O put the metal first, as usual.")),
    hints=["Compare the two powders on Day 8 p.7: black CuO and red Cu<sub>2</sub>O."],
    solution="<p>Because copper has <strong>two common ions</strong>, the bare name can't tell black CuO (copper (II) oxide) from red Cu<sub>2</sub>O (copper (I) oxide) (Day 8 p.7).</p>",
    source="Day 8 p.7")

P(id="m16-p5", module="m16", kind="practice", level="Textbook preview",
  prompt="<p>According to the textbook, which compound is named <em>without</em> a Roman numeral?</p>",
  answer=choice(("ZnCl<sub>2</sub>", True, "Right: zinc forms only Zn<sup>2+</sup>, so it's simply zinc chloride (textbook §4.3)."),
                ("FeCl<sub>3</sub>", False, "Iron forms Fe<sup>2+</sup> and Fe<sup>3+</sup>: iron(III) chloride."),
                ("CuCl", False, "Copper forms Cu<sup>+</sup> and Cu<sup>2+</sup>: copper(I) chloride."),
                ("CoCl<sub>2</sub>", False, "Cobalt forms more than one ion: cobalt(II) chloride.")),
  hints=["The textbook exempts transition metals that form only one cation: Ag<sup>+</sup>, Cd<sup>2+</sup>, Zn<sup>2+</sup>."],
  solution="<p><strong>ZnCl<sub>2</sub></strong>, zinc chloride. The textbook uses numerals “unless the metal forms just one cation, as with Ag<sup>+</sup>, Cd<sup>2+</sup>, and Zn<sup>2+</sup>” (PDF p.191). The slides don't mention these exceptions.</p>",
  source=tb("4.3", 191))

add(id="m16-p6", module="m16", kind="practice", level="Standard",
    prompt="<p>Name Ca(NO<sub>3</sub>)<sub>2</sub>.</p>",
    answer=tname(["calcium nitrate"],
                 traps=[(["calcium dinitrate"], PREFIX_IONIC + " The 2 counts nitrate ions; it doesn't go into the name."),
                        (["calcium nitrite"], "NO<sub>3</sub><sup>−</sup> is nitrate. Nitrite is NO<sub>2</sub><sup>−</sup> (Day 8 p.8)."),
                        (["calcium(II) nitrate", "calcium (II) nitrate"], "Calcium (group 2) forms only Ca<sup>2+</sup>, so it takes no Roman numeral.")]),
    hints=["Ca → Ca<sup>2+</sup>; NO<sub>3</sub><sup>−</sup> is nitrate (table).", "The subscript 2 after the parentheses counts nitrate ions."],
    solution="<p>Ca<sup>2+</sup> + 2 NO<sub>3</sub><sup>−</sup> → <strong>calcium nitrate</strong>: cation name + polyatomic-ion name, no prefixes (Day 8 p.8–9).</p>",
    source="Day 8 p.8–9")

add(id="m16-transfer", module="m16", kind="transfer", level="Transfer",
    prompt="<p>A compound has the formula Cr<sub>2</sub>(SO<sub>4</sub>)<sub>3</sub>. What is its systematic name?</p>",
    answer=tname(names("chromium(III) sulfate", "chromium(III) sulphate"),
                 traps=[(names("chromium(II) sulfate"), NUMERAL + " Three SO<sub>4</sub><sup>2−</sup> carry −6, shared by two Cr."),
                        (["chromium sulfate"], "Chromium forms more than one ion, so the name needs its charge (Day 8 p.7)."),
                        (["dichromium trisulfate"], PREFIX_IONIC)]),
    hints=["SO<sub>4</sub><sup>2−</sup> is sulfate (polyatomic-ion table).", "Three sulfates carry 3 × (−2) = −6.", "Two Cr must total +6."],
    solution="<p>3 SO<sub>4</sub><sup>2−</sup> = −6, so 2 Cr = +6 and each is Cr<sup>3+</sup>: <strong>chromium(III) sulfate</strong>. "
             "It combines two Day 8 ideas: the Roman numeral (p.7) and a polyatomic anion named as a unit (p.8–9).</p>",
    source="Day 8 p.7–9")

add(id="m16-m-explain", module="m16", kind="mastery", level="Explain",
    prompt="<p>Explain why FeCl<sub>2</sub>'s name needs a Roman numeral but MgCl<sub>2</sub>'s doesn't.</p>",
    answer={"type": "self", "model": "<p>Magnesium (group 2) always forms Mg<sup>2+</sup> (Day 7 p.19), so “magnesium chloride” can only mean MgCl<sub>2</sub>. "
                                     "Iron is a transition metal with more than one common ion (Fe<sup>2+</sup>, Fe<sup>3+</sup>), so “iron chloride” could mean FeCl<sub>2</sub> or FeCl<sub>3</sub>; "
                                     "the numeral (II) names the charge (Day 8 p.7).</p>"},
    hints=[], solution="", source="Day 8 p.7; Day 7 p.19")

P(id="m16-m-recognize", module="m16", kind="mastery", level="Recognize",
  prompt="<p>Which compound's formula needs parentheses?</p>",
  answer=choice(("magnesium hydroxide", True, "Right: Mg<sup>2+</sup> needs two OH<sup>−</sup>, so Mg(OH)<sub>2</sub>."),
                ("sodium hydroxide", False, "One OH<sup>−</sup> balances Na<sup>+</sup>: NaOH."),
                ("ammonium chloride", False, "One of each: NH<sub>4</sub>Cl."),
                ("potassium nitrate", False, "One of each: KNO<sub>3</sub>.")),
  hints=["Parentheses appear when a formula needs two or more of the same polyatomic ion."],
  solution="<p><strong>Mg(OH)<sub>2</sub></strong>: the subscript 2 must apply to the whole OH<sup>−</sup> ion (textbook §4.3, PDF p.193).</p>",
  source=tb("4.3", 193) + "; Day 8 p.8")

add(id="m16-m-sanity", module="m16", kind="mastery", level="Sanity check",
    prompt="<p>A classmate names Cu<sub>2</sub>O “copper (II) oxide” because the formula has a 2. What's wrong?</p>",
    answer=choice(("The numeral is each copper ion's charge. Cu<sub>2</sub>O contains Cu<sup>+</sup>, so it's copper (I) oxide.", True, "Right (Day 8 p.7)."),
                  ("Nothing; the 2 goes into the name.", False, "Then Cu<sub>2</sub>O and CuO would both be “(II)”."),
                  ("It should be “dicopper oxide”.", False, PREFIX_IONIC),
                  ("The numeral should be the oxide's charge.", False, "The numeral always describes the metal ion.")),
    hints=["Balance the charges: 2 Cu + O<sup>2−</sup> = 0."],
    solution="<p>O<sup>2−</sup> is −2, so two Cu share +2: each is Cu<sup>+</sup>, <strong>copper (I) oxide</strong>, exactly as labeled on Day 8 p.7.</p>",
    source="Day 8 p.7")

# =====================================================================================
# m17  Naming covalent compounds (Day 8 p.12–13; textbook §4.3 Binary Molecular Compounds)
# =====================================================================================
NO_MONO = "No “mono” on the first element (Day 8 p.12)."
add(id="m17-attempt", module="m17", kind="attempt", level="Guided attempt",
    prompt="<p>Name the covalent compound PCl<sub>5</sub>.</p>",
    answer=tname(["phosphorus pentachloride"], covalent=True,
                 traps=[(["monophosphorus pentachloride"], NO_MONO),
                        (["phosphorus chloride"], "Covalent names need prefixes to show how many of each atom (Day 8 p.12). PCl<sub>3</sub> is also a phosphorus chloride."),
                        (names("phosphorus(V) chloride"), "In this course, Roman numerals name transition-metal ions in ionic compounds. P and Cl are both nonmetals, so the course's rule is prefixes (Day 8 p.12)."),
                        (["phosphorous pentachloride"], "Spelling: the element is phosphorus. “Phosphorous” is an adjective.")]),
    hints=["Two nonmetals → a covalent compound → prefixes (Day 8 p.12).",
           "First element: its element name, with no “mono” when there's only one.",
           "Second element: prefix + the name ending in -ide. Five Cl → penta- (Table 4.3).",
           "phosphorus + pentachloride."],
    solution="<p><strong>phosphorus pentachloride</strong>: one P (no “mono” on the first element), five Cl → penta- + chloride (Day 8 p.12–13).</p>",
    compare={"wrong": "<p>“Phosphorus chloride” or “phosphorus(V) chloride”.</p>",
             "tempting": "Ionic names skip prefixes, and Roman numerals worked for copper on the same day.",
             "fails": "Those are ionic-compound rules. For two nonmetals, the course's name carries the atom counts as prefixes, or PCl<sub>3</sub> and PCl<sub>5</sub> would share one name. In this course, Roman numerals name only metal-ion charges."},
    source="Day 8 p.12–13")

add(id="m17-p1", module="m17", kind="practice", level="Warm-up",
    prompt="<p>Write the formula of silicon tetrafluoride.</p>",
    answer=tformula(["SiF4"], traps=[(["SiF"], "tetra- means 4 F."), (["Si4F"], "The prefix belongs to fluoride, the word it's attached to.")]),
    hints=["tetra- = 4 (Table 4.3).", "No prefix on silicon means one Si."],
    solution="<p>One Si, four F: <strong>SiF<sub>4</sub></strong>.</p>", source="Day 8 p.12–13")

add(id="m17-p2", module="m17", kind="practice", level="Standard",
    prompt="<p>Name N<sub>2</sub>F<sub>4</sub>.</p>",
    answer=tname(["dinitrogen tetrafluoride"], covalent=True,
                 traps=[(["nitrogen tetrafluoride"], "Two N atoms: the first element takes a prefix too when there's more than one (S<sub>2</sub>F<sub>2</sub> is disulfur difluoride, Day 8 p.13)."),
                        (["nitrogen fluoride"], "Covalent names carry the counts as prefixes (Day 8 p.12).")]),
    hints=["Two N → di-; four F → tetra- (Table 4.3).", "The second element ends in -ide: fluoride."],
    solution="<p><strong>dinitrogen tetrafluoride</strong>: the first element gets di- because there are two (only “mono” is skipped), and the second gets tetra- + fluoride.</p>",
    source="Day 8 p.12–13")

add(id="m17-p3", module="m17", kind="practice", level="Concept",
    prompt="<p>Which compound is named with number prefixes?</p>",
    answer=choice(("NCl<sub>3</sub>", True, "Right: two nonmetals, so it's covalent: nitrogen trichloride."),
                  ("CaCl<sub>2</sub>", False, "Ionic (metal + nonmetal): calcium chloride, no prefixes."),
                  ("FeCl<sub>3</sub>", False, "Ionic: iron(III) chloride, with a Roman numeral, not a prefix."),
                  ("NaCl", False, "Ionic: sodium chloride.")),
    hints=["Prefixes belong to covalent compounds: nonmetals only (Day 7 p.14; Day 8 p.12)."],
    solution="<p><strong>NCl<sub>3</sub></strong>, nitrogen trichloride. The others contain a metal, so they're ionic and named without prefixes.</p>",
    source="Day 8 p.12; Day 7 p.14")

P(id="m17-p4", module="m17", kind="practice", level="Textbook preview",
  prompt="<p>Write the systematic name of NO, a gas in car exhaust.</p>",
  answer=tname(["nitrogen monoxide"], covalent=True,
               traps=[(["nitrogen monooxide"], "The textbook drops the o of mono- before a vowel: monoxide, not monooxide (§4.3, PDF p.188). The slides don't state this rule."),
                      (["mononitrogen monoxide", "mononitrogen monooxide"], NO_MONO),
                      (["nitrogen oxide"], "Which nitrogen oxide? NO, NO<sub>2</sub>, and N<sub>2</sub>O all exist; the prefix says how many O."),
                      (["nitric oxide"], "That's a common name. Name it systematically with the Day 8 prefixes.")]),
  hints=["One N (no prefix), one O → mono- + oxide.", "Before a vowel, the textbook shortens mono- + oxide to monoxide."],
  solution="<p><strong>nitrogen monoxide</strong>. By the Day 8 rules it's “nitrogen mono-oxide”; the textbook adds that a prefix ending in o or a loses that vowel before “oxide” (PDF p.188). It's the name the textbook uses for NO in §4.8 (PDF p.212).</p>",
  source=tb("4.3", 188) + "; Day 8 p.12")

add(id="m17-p5", module="m17", kind="practice", level="Standard",
    prompt="<p>Write the formula of dinitrogen trioxide.</p>",
    answer=tformula(["N2O3"], traps=[(["N3O2"], "The prefix goes with the element it's attached to: di- with nitrogen, tri- with oxide.")]),
    hints=["di- = 2 (nitrogen); tri- = 3 (oxide)."],
    solution="<p><strong>N<sub>2</sub>O<sub>3</sub></strong>.</p>", source="Day 8 p.12–13")

add(id="m17-transfer", module="m17", kind="transfer", level="Transfer",
    prompt="<p>(a) The anesthetic “laughing gas” is dinitrogen monoxide (textbook §4.7). Write its formula. (b) Name Cl<sub>2</sub>O<sub>7</sub>, a chlorine oxide.</p>",
    answer={"type": "multi", "parts": [
        {"label": "(a) formula", **tformula(["N2O"])},
        {"label": "(b) name of Cl<sub>2</sub>O<sub>7</sub>", **tname(["dichlorine heptoxide", "dichlorine heptaoxide"], covalent=True,
                                                                     traps=[(["chlorine heptoxide", "chlorine heptaoxide"], "Two Cl atoms: the first element takes a prefix when there's more than one (Day 8 p.13, S<sub>2</sub>F<sub>2</sub>)."),
                                                                            (["dichlorine oxide"], "The prefix for 7 O is hepta-."),
                                                                            (["chlorine(VII) oxide", "chlorine (VII) oxide"], "In this course, Roman numerals are for metal ions. Cl and O are nonmetals: use prefixes (Day 8 p.12).")])}]},
    hints=["(a) di- = 2 N; mono- = 1 O.", "(b) Two Cl → di-; seven O → hepta- + oxide (Table 4.3)."],
    solution="<p>(a) <strong>N<sub>2</sub>O</strong>. (b) <strong>dichlorine heptoxide</strong>: the textbook drops the a of hepta- before “oxide” (PDF p.188); by the slides' rules alone it's dichlorine heptaoxide, and both are accepted. "
             "Names become formulas and formulas become names with the same Table 4.3 prefixes.</p>",
    source="Day 8 p.12–13; " + tb("4.3", 188) + "; " + tb("4.7", 208) + " for N₂O")

add(id="m17-m-explain", module="m17", kind="mastery", level="Explain",
    prompt="<p>Why do covalent names need prefixes when binary ionic names don't?</p>",
    answer={"type": "self", "model": "<p>A main-group ion has a characteristic charge, so the ratio in an ionic compound follows from the name (“magnesium chloride” can only be MgCl<sub>2</sub>; the textbook makes the same point). "
                                     "Two nonmetals can combine in several ratios, like SO<sub>2</sub> and SO<sub>3</sub> (Day 8 p.13), so the name itself must state the counts.</p>"},
    hints=[], solution="", source="Day 8 p.12–13; Day 7 p.21; " + tb("4.3", 189, 190))

add(id="m17-m-recognize", module="m17", kind="mastery", level="Recognize",
    prompt="<p>Which name follows the Day 8 rules for CCl<sub>4</sub>?</p>",
    answer=choice(("carbon tetrachloride", True, "Right."), ("monocarbon tetrachloride", False, NO_MONO),
                  ("carbon chloride", False, "Covalent names need the count of Cl."), ("carbon(IV) chloride", False, "Roman numerals are for metal ions.")),
    hints=["Two nonmetals; one C; four Cl."], solution="<p><strong>carbon tetrachloride</strong>.</p>", source="Day 8 p.12")

add(id="m17-m-sanity", module="m17", kind="mastery", level="Sanity check",
    prompt="<p>A student names SO<sub>3</sub> “sulfur(VI) oxide”. What's the problem?</p>",
    answer=choice(("In this course, covalent compounds (two nonmetals) are named with prefixes: sulfur trioxide.", True, "Right (Day 8 p.12–13)."),
                  ("Nothing; Roman numerals work for any element.", False, "In this course they name transition-metal ion charges (Day 8 p.7)."),
                  ("It should be “monosulfur trioxide”.", False, NO_MONO),
                  ("Sulfur's numeral should be (III), for three O.", False, "Numerals don't count atoms, and covalent names don't use them.")),
    hints=["Is sulfur a metal?"],
    solution="<p>Sulfur and oxygen are both nonmetals: <strong>sulfur trioxide</strong>, as on Day 8 p.13.</p>"
             "<p class='bg'>Names with Roman numerals for nonmetal compounds, such as sulfur(VI) oxide, do exist in formal (IUPAC) naming, but the course names covalent compounds with prefixes (Day 8 p.12).</p>", source="Day 8 p.13")

# =====================================================================================
# t4-3  Naming acids (textbook preview: §4.3 Binary Acids, Oxoacids, PDF p.193–195)
# =====================================================================================
P(id="t4-3-attempt", module="t4-3", kind="attempt", level="Guided attempt",
  prompt="<p>Name HI(aq), hydrogen iodide dissolved in water.</p>",
  answer=tname(["hydroiodic acid", "hydriodic acid"],
               traps=[(["hydrogen iodide"], "That's HI itself, the molecular compound. Dissolved in water, (aq), it's named as an acid."),
                      (["iodic acid"], "Iodic acid is an oxoacid (HIO<sub>3</sub>). A binary acid needs the hydro- prefix."),
                      (["hydroiodous acid"], "-ous goes with -ite oxoanions. A binary acid ends in -ic.")]),
  hints=["A binary acid is H plus one other element, dissolved in water (textbook §4.3).",
         "Name = hydro- + the second element's root + -ic + acid.",
         "Iodine's root is iod-.",
         "hydro + iod + ic + acid."],
  solution="<p><strong>hydroiodic acid</strong> (also written hydriodic acid). The (aq) matters: HI is hydrogen iodide; HI(aq) is the acid, just as the textbook's HBr is hydrogen bromide and HBr(aq) is hydrobromic acid (§4.3, PDF p.194).</p>",
  compare={"wrong": "<p>“Hydrogen iodide”.</p>",
           "tempting": "It's the correct name of HI, and binary compounds are usually named that way.",
           "fails": "Without (aq), HI is the molecular compound. In water it has separated into H<sup>+</sup> and I<sup>−</sup> ions, and the textbook names such solutions as acids: hydro- + -ic."},
  source=tb("4.3", 194))

P(id="t4-3-p1", module="t4-3", kind="practice", level="Warm-up",
  prompt="<p>Name HNO<sub>3</sub>, the acid of the nitrate ion.</p>",
  answer=tname(["nitric acid"], traps=[(["nitrous acid"], "Nitrous acid is HNO<sub>2</sub>, from nitrite. Nitrate (-ate) gives an -ic acid."),
                                       (["hydronitric acid"], "hydro- is only for binary acids. HNO<sub>3</sub> is an oxoacid.")]),
  hints=["Oxoacid: the anion ends in -ate, so the acid ends in -ic (textbook §4.3)."],
  solution="<p>nitrate → <strong>nitric acid</strong>.</p>", source=tb("4.3", 194))

P(id="t4-3-p2", module="t4-3", kind="practice", level="Standard",
  prompt="<p>Name HClO<sub>2</sub>, the acid of the chlorite ion.</p>",
  answer=tname(["chlorous acid"], traps=[(["chloric acid"], "Chloric acid is HClO<sub>3</sub>, from chlorate. Chlorite (-ite) gives an -ous acid."),
                                         (["hydrochloric acid"], "That's HCl(aq), a binary acid. HClO<sub>2</sub> contains oxygen.")]),
  hints=["-ite → -ous acid (textbook Table 4.5)."],
  solution="<p>chlorite → <strong>chlorous acid</strong> (textbook Table 4.5, PDF p.192).</p>", source=tb("4.3", 192, 194))

P(id="t4-3-p3", module="t4-3", kind="practice", level="Standard",
  prompt="<p>Write the formula of carbonic acid, the acid of the carbonate ion.</p>",
  answer=tformula(["H2CO3"], traps=[(["HCO3"], "Carbonate is CO<sub>3</sub><sup>2−</sup>; two H<sup>+</sup> are needed to balance it. (HCO<sub>3</sub><sup>−</sup> is the hydrogen carbonate ion.)")]),
  hints=["Carbonate: CO<sub>3</sub><sup>2−</sup>.", "An oxoacid balances the anion's charge with H<sup>+</sup> ions."],
  solution="<p>2 H<sup>+</sup> + CO<sub>3</sub><sup>2−</sup> → <strong>H<sub>2</sub>CO<sub>3</sub></strong>.</p>", source=tb("4.3", 194))

P(id="t4-3-p4", module="t4-3", kind="practice", level="Standard",
  prompt="<p>Match each anion ending to the acid it names.</p>",
  answer={"type": "match",
          "rows": [{"html": "-ide (Cl<sup>−</sup>, chloride)", "answer": "hydro"}, {"html": "-ate (SO<sub>4</sub><sup>2−</sup>, sulfate)", "answer": "ic"},
                   {"html": "-ite (SO<sub>3</sub><sup>2−</sup>, sulfite)", "answer": "ous"}],
          "options": [{"key": "hydro", "html": "hydro-…-ic acid"}, {"key": "ic", "html": "…-ic acid"}, {"key": "ous", "html": "…-ous acid"}]},
  hints=["Binary acids take hydro-; oxoacids don't."],
  solution="<p>chloride → hydrochloric acid; sulfate → sulfuric acid; sulfite → sulfurous acid (textbook §4.3).</p>", source=tb("4.3", 194))

P(id="t4-3-p5", module="t4-3", kind="practice", level="Stretch",
  prompt="<p>Name HClO, the acid of the hypochlorite ion.</p>",
  answer=tname(["hypochlorous acid"], traps=[(["hypochloric acid"], "Hypochlorite ends in -ite, so the acid ends in -ous."), (["chlorous acid"], "Keep the hypo- prefix: chlorous acid is HClO<sub>2</sub>.")]),
  hints=["Keep the prefix; change -ite to -ous."],
  solution="<p>hypochlorite → <strong>hypochlorous acid</strong> (textbook Table 4.5).</p>", source=tb("4.3", 192, 194))

P(id="t4-3-transfer", module="t4-3", kind="transfer", level="Transfer",
  prompt="<p>The iodate ion is IO<sub>3</sub><sup>−</sup>. Name the acid HIO<sub>3</sub>.</p>",
  answer=tname(["iodic acid"], traps=[(["iodous acid"], "Iodate ends in -ate, so the acid ends in -ic."), (["hydroiodic acid"], "That's HI(aq), a binary acid.")]),
  hints=["Same pattern as chlorate → chloric acid.", "-ate → -ic."],
  solution="<p>iodate → <strong>iodic acid</strong>, just as chlorate gives chloric acid (textbook Table 4.5).</p>", source=tb("4.3", 192, 194))

P(id="t4-3-m-explain", module="t4-3", kind="mastery", level="Explain",
  prompt="<p>Why is HCl(aq) “hydrochloric acid” while HClO<sub>3</sub> is “chloric acid” with no hydro-?</p>",
  answer={"type": "self", "model": "<p>HCl(aq) is a binary acid: H plus one other element, so it takes hydro- + -ic. HClO<sub>3</sub> is an oxoacid, named from its oxoanion: chlorate (-ate) → chloric acid (-ic), with no hydro- (textbook §4.3, PDF p.194).</p>"},
  hints=[], solution="", source=tb("4.3", 194))

P(id="t4-3-m-recognize", module="t4-3", kind="mastery", level="Recognize",
  prompt="<p>Which is a binary acid?</p>",
  answer=choice(("HF(aq)", True, "Right: H plus one other element, in water (hydrofluoric acid)."), ("HNO<sub>3</sub>", False, "An oxoacid (contains O)."),
                ("H<sub>2</sub>SO<sub>4</sub>", False, "An oxoacid."), ("NaOH", False, "A base, not an acid.")),
  hints=["Binary = two elements."], solution="<p><strong>HF(aq)</strong>, hydrofluoric acid.</p>", source=tb("4.3", 194))

P(id="t4-3-m-sanity", module="t4-3", kind="mastery", level="Sanity check",
  prompt="<p>A student names H<sub>2</sub>SO<sub>4</sub> “hydrosulfuric acid”. What's wrong?</p>",
  answer=choice(("hydro- is only for binary acids. H<sub>2</sub>SO<sub>4</sub> comes from sulfate, so it's sulfuric acid.", True, "Right (textbook §4.3)."),
                ("Nothing.", False, "Hydrosulfuric acid is H<sub>2</sub>S(aq)."),
                ("It should be sulfurous acid.", False, "Sulfurous acid is H<sub>2</sub>SO<sub>3</sub>, from sulfite."),
                ("Acids take Roman numerals.", False, "They don't.")),
  hints=["Does the formula contain oxygen?"], solution="<p><strong>sulfuric acid</strong>: sulfate (-ate) → -ic, no hydro-.</p>", source=tb("4.3", 194))

# =====================================================================================
# m18  Lewis symbols, the octet rule, and bonding capacity (Day 8 p.16–18; textbook §4.4)
# =====================================================================================
AS_SYM, AS_UNP = LW.symbol_svg("As")
add(id="m18-attempt", module="m18", kind="attempt", level="Guided attempt",
    prompt="<p>Arsenic (As) is in group 15, below N and P. (a) How many dots are in its Lewis symbol? (b) What is its bonding capacity?</p>",
    answer={"type": "multi", "parts": [
        {"label": "(a) dots", **tnum(5, traps=[(33, "That's all of arsenic's electrons. A Lewis symbol shows only the valence electrons (Day 8 p.17)."),
                                                (3, "That's the number of <em>unpaired</em> dots. Count every dot, pairs included.")])},
        {"label": "(b) bonding capacity", **tnum(AS_UNP, traps=[(5, "Count the unpaired dots only: the pair doesn't form a bond (Day 8 p.18)."),
                                                               (8, "8 is the octet As reaches, not the number of bonds it forms.")])}]},
    hints=["A Lewis symbol shows the valence electrons (Day 8 p.17).",
           "Group 15 → 5 valence electrons, the same as N.",
           "Place dots one per side before pairing: 4 singles, then the 5th makes a pair.",
           "Bonding capacity = the number of unpaired dots (Day 8 p.18)."],
    solution=f"<p>{AS_SYM} <strong>5 dots</strong>: one pair and three singles, so <strong>bonding capacity 3</strong>. As forms 3 bonds to complete its octet, like N in NH<sub>3</sub> (Day 8 p.22–23): Lewis symbols repeat down a group (Day 8 p.17).</p>",
    compare={"wrong": "<p>“33 dots, bonding capacity 5.”</p>",
             "tempting": "Arsenic has 33 electrons, and every dot looks like an electron that could bond.",
             "fails": "Only valence electrons appear in a Lewis symbol, and only unpaired dots form bonds: a paired dot is a lone pair. Three shared pairs plus the lone pair give As its octet."},
    source="Day 8 p.16–18, p.22–23")

add(id="m18-p1", module="m18", kind="practice", level="Warm-up",
    prompt="<p>What is carbon's bonding capacity?</p>",
    answer=tnum(4, traps=[(2, "Carbon's symbol has four single dots, one per side: C forms 4 bonds (Day 8 p.18).")]),
    hints=["Group 14 → 4 valence electrons, placed one per side: all four unpaired (Day 8 p.17).", "Day 8 p.18 says to memorize this one."],
    solution="<p><strong>4</strong>: “As a critical example that you should ‘memorize’ right now: carbon ALMOST ALWAYS forms 4 covalent bonds” (Day 8 p.18).</p>",
    source="Day 8 p.18")

add(id="m18-p2", module="m18", kind="practice", level="Standard",
    prompt="<p>Which element's Lewis symbol has two pairs of dots and two single dots?</p>",
    answer=choice(("O", True, "Right: 6 valence electrons → two pairs and two singles, bonding capacity 2."),
                  ("N", False, "N has 5: one pair and three singles."), ("F", False, "F has 7: three pairs and one single."), ("C", False, "C has 4 single dots.")),
    hints=["Two pairs + two singles = 6 valence electrons."],
    solution="<p>" + LW.symbol_svg("O")[0] + " <strong>O</strong> (group 16).</p>", source="Day 8 p.17")

add(id="m18-p3", module="m18", kind="practice", level="Warm-up",
    prompt="<p>Once a hydrogen atom has the valence configuration of a noble gas, how many valence electrons does it have in total?</p>",
    answer=tnum(2, traps=[(8, "Hydrogen is the exception: “Hydrogen only needs two electrons to obtain [He]” (Day 8 p.16)."),
                          (1, "That's how many it gains by sharing. The question asks for the total around H.")]),
    hints=["H has one electron.", "Which noble gas is closest to H, and how many electrons does it have?"],
    solution="<p><strong>2</strong>, the configuration of He: “Hydrogen only needs two electrons to obtain [He]” (Day 8 p.16). So H forms one bond and is never a central atom.</p>",
    source="Day 8 p.16")

P(id="m18-p4", module="m18", kind="practice", level="Textbook preview",
  prompt="<p>Draw the Lewis structure of potassium sulfide, K<sub>2</sub>S, the way the textbook draws ionic compounds. How many dots surround (a) each K<sup>+</sup> ion and (b) the S<sup>2−</sup> ion?</p>",
  answer={"type": "multi", "parts": [
      {"label": "(a) dots on each K<sup>+</sup>", **tnum(0, traps=[(1, "K loses its one valence electron to become K<sup>+</sup>, so no dots are left.")])},
      {"label": "(b) dots on S<sup>2−</sup>", **tnum(8, traps=[(6, "S has 6 valence electrons, and S<sup>2−</sup> has gained 2 more.")])}]},
  hints=["Group 1 atoms lose their valence s electron to form cations (Day 7 p.18).",
         "A nonmetal anion has a complete octet, drawn inside brackets with the charge outside."],
  solution="<p>(a) <strong>0</strong>. (b) <strong>8</strong>: K<sup>+</sup> " + LS("S2-ion") + " K<sup>+</sup>, with the eight dots in brackets and 2− outside. It's the textbook's pattern for ionic compounds (§4.4, PDF p.196, Sample Ex. 4.9, CaF<sub>2</sub>): cations have no dots; anions have octets in brackets.</p>"
           "<p class='note'>That sample exercise says calcium loses its “3s” electrons. Calcium's valence electrons are 4s: Ca is [Ar]4s<sup>2</sup> (Day 6 filling order).</p>",
  source=tb("4.4", 196) + "; Day 7 p.18")

add(id="m18-p5", module="m18", kind="practice", level="Standard",
    prompt="<p>Bromine is in group 17. How many covalent bonds does a Br atom typically form?</p>",
    answer=tnum(1, traps=[(7, "7 is the number of valence electrons (dots); only one is unpaired.")]),
    hints=["Group 17 → 7 valence electrons: three pairs and one single dot.", "Bonding capacity = the number of unpaired dots (Day 8 p.18)."],
    solution="<p><strong>1</strong>: one unpaired dot, like F in F<sub>2</sub> (Day 8 p.19).</p>", source="Day 8 p.17–19")

add(id="m18-p6", module="m18", kind="practice", level="Concept",
    prompt="<p>What does the octet rule say?</p>",
    answer=choice(("Main-group atoms tend to gain, lose, or share electrons so that each has eight valence electrons.", True, "Right (Day 8 p.16)."),
                  ("Every atom has exactly eight electrons.", False, "It's about valence electrons after bonding, and only a tendency."),
                  ("Atoms form eight bonds.", False, "Eight electrons, not eight bonds."),
                  ("Only noble gases have octets.", False, "Other atoms reach one by bonding: that's the rule's point.")),
    hints=["Lewis, 1916 (Day 8 p.16)."],
    solution="<p>“All main group atoms tend to gain, lose, or share electrons so that each atom has eight valence electrons” (Day 8 p.16).</p>",
    source="Day 8 p.16")

add(id="m18-transfer", module="m18", kind="transfer", level="Transfer",
    prompt="<p>Silicon is in group 14, just below carbon. Predict the formula of the simplest compound of silicon and hydrogen, in which each H forms one bond.</p>",
    answer=tformula(["SiH4"], traps=[(["SiH2"], "Si has four unpaired dots, like C, so it forms 4 bonds.")]),
    hints=["Same group as C → same Lewis-symbol pattern (Day 8 p.17).", "Bonding capacity 4, and each H takes one bond."],
    solution="<p><strong>SiH<sub>4</sub></strong>: Si, like C, has four unpaired dots and forms four bonds, the silicon version of CH<sub>4</sub>.</p>",
    source="Day 8 p.17–18")

add(id="m18-m-explain", module="m18", kind="mastery", level="Explain",
    prompt="<p>Beryllium's configuration is 1s<sup>2</sup>2s<sup>2</sup>, with its valence electrons paired, yet its Lewis symbol is ·Be· with two single dots. Explain.</p>",
    answer={"type": "self", "model": "<p>Lewis symbols place one dot on each side before pairing (Day 8 p.17), so Be's two valence electrons are drawn apart. "
                                     "The symbol predates orbitals: the slide calls it “LIKE putting electrons into s and p orbitals, but Lewis didn't know that orbitals existed”. "
                                     "It shows bonding sites, not orbital occupancy, and Be does tend to form two bonds.</p>"},
    hints=[], solution="", source="Day 8 p.17")

add(id="m18-m-recognize", module="m18", kind="mastery", level="Recognize",
    prompt="<p>Which element's Lewis symbol has the same pattern of dots as sulfur's?</p>",
    answer=choice(("O", True, "Right: same group (16), same six valence electrons."), ("Cl", False, "Group 17: seven dots."),
                  ("P", False, "Group 15: five dots."), ("Ar", False, "Group 18: eight dots.")),
    hints=["Lewis symbols repeat down a group (Day 8 p.17)."], solution="<p><strong>O</strong>, the element above S in group 16.</p>", source="Day 8 p.17")

add(id="m18-m-sanity", module="m18", kind="mastery", level="Sanity check",
    prompt="<p>A student draws carbon's Lewis symbol with two pairs of dots and concludes that carbon forms two bonds. What's wrong?</p>",
    answer=choice(("Dots go one per side before pairing, so C has four single dots and forms four bonds.", True, "Right (Day 8 p.17–18)."),
                  ("Nothing; C forms two bonds.", False, "Carbon “ALMOST ALWAYS forms 4 covalent bonds” (Day 8 p.18)."),
                  ("Carbon has six valence electrons.", False, "It has four (group 14)."), ("Lewis symbols show all electrons.", False, "Only valence electrons.")),
    hints=["Recall the placement rule on Day 8 p.17."], solution="<p>Four single dots → <strong>four bonds</strong>.</p>", source="Day 8 p.17–18")

# =====================================================================================
# m19  Lewis structures: the five steps (Day 8 p.19–30; textbook §4.4)
# =====================================================================================
add(id="m19-attempt", module="m19", kind="attempt", level="Guided attempt",
    prompt="<p>Use the five steps (Day 8 p.21) on hydrogen cyanide, HCN, with C as the central atom. "
           "(a) How many valence electrons does HCN have? (b) Is the C–N bond single, double, or triple? (c) How many lone pairs are on N?</p>",
    answer={"type": "multi", "parts": [
        {"label": "(a) valence electrons", **tnum(LW.STRUCTS["HCN"].total_valence(), traps=[(14, "Count only valence electrons: H 1, C 4, N 5.")])},
        {"label": "(b) C–N bond", **choice(("single", False, "With single bonds only, C has just 4 electrons around it."), ("double", False, "A double bond still leaves C with 6 electrons."),
                                           ("triple", True, "Right: C then has 8 (one C–H pair + three C–N pairs)."))},
        {"label": "(c) lone pairs on N", **tnum(LW.STRUCTS["HCN"].lp.get(2, 0), traps=[(3, "That's after step 3. Step 5 turns two of those lone pairs into bonds.")])}]},
    hints=["Step 1: H 1 + C 4 + N 5 = 10 valence electrons (Day 8 p.21).",
           "Step 2: H–C–N with single bonds; C has the largest bonding capacity.",
           "Step 3: give N three lone pairs. Steps 4–5: that uses 4 + 6 = 10 electrons, so none are left over, and C has only 4 around it.",
           "C is still short, as the carbons in ethyne were (Day 8 p.25): turn two of N's lone pairs into two more C–N shared pairs → H–C≡N with one lone pair on N."],
    solution="<div class='lw-row'>" + "".join(LW.svg(st, caption=lab.split(':')[0], scale=0.7) for lab, st, _ in LW.five_steps(LW.STRUCTS["HCN"])) + "</div>"
             "<p>(a) <strong>10</strong>. (b) <strong>triple</strong>. (c) <strong>1</strong> lone pair on N. Every atom now has an octet (H has 2), "
             "and C forms 4 bonds, as it “ALMOST ALWAYS” does (Day 8 p.18). It's built the same way as ethyne on Day 8 p.24–25.</p>",
    compare={"wrong": "<p>H–C–N̈ with single bonds, and 2 more electrons parked on C to make the count come out.</p>",
             "tempting": "Step 5 says to “use any leftover electrons” on the central atom, so adding dots to C seems allowed.",
             "fails": "There are no leftover electrons: step 3 already used all 10. Adding dots would make 12, more than HCN has. The only way to give C an octet is to share more of N's electrons, which makes multiple bonds, as for O<sub>2</sub> and N<sub>2</sub> (Day 8 p.20)."},
    source="Day 8 p.20–25")

P(id="m19-p1", module="m19", kind="practice", level="Textbook preview",
  prompt="<p>How many valence electrons are in the chlorate ion, ClO<sub>3</sub><sup>−</sup>?</p>",
  answer=tnum(LW.VALENCE["Cl"] + 3 * LW.VALENCE["O"] + 1, traps=[(25, "Include the charge: a 1− ion has one extra electron (textbook step 1)."),
                                                              (24, "A negative charge adds electrons; it doesn't remove them.")]),
  hints=["Cl 7 + 3 × O 6 = 25.", "The 1− charge means one more electron."],
  solution="<p>7 + 18 + 1 = <strong>26</strong>. The textbook's step 1 adds an electron for each negative charge and subtracts one for each positive charge (§4.4, PDF p.197); the slides' examples were all neutral.</p>",
  source=tb("4.4", 197))

add(id="m19-p2", module="m19", kind="practice", level="Warm-up",
    prompt="<p>In hypochlorous acid, HOCl, which atom goes in the center?</p>",
    answer=choice(("O", True, "Right: O's bonding capacity (2) is the largest."), ("Cl", False, "Cl's bonding capacity is 1, like H's."),
                  ("H", False, "H can form only one bond, so it's never central."), ("It has no central atom.", False, "One atom must bond to the other two.")),
    hints=["“The central atom is the one with the largest bonding capacity” (Day 8 p.21).", "Bonding capacities: H 1, O 2, Cl 1."],
    solution=f"<p><strong>O</strong>: H–O–Cl. {LS('HOCl')} With 1 + 6 + 7 = 14 valence electrons, two single bonds and five lone pairs complete every octet (H has 2).</p>"
             "<p class='note'>A shortcut some books use, “the least electronegative atom goes in the center,” would pick Cl (χ 3.0, below O's 3.5) and give the wrong skeleton. "
             "The course's rule is the largest bonding capacity (Day 8 p.21); the textbook uses electronegativity only to break a tie in bonding capacity (PDF p.197).</p>",
    source="Day 8 p.18, p.21")

add(id="m19-p3", module="m19", kind="practice", level="Standard",
    prompt="<p>Carbon disulfide, CS<sub>2</sub>, has C in the center. (a) How many valence electrons does it have? (b) How many lone pairs are in the finished structure?</p>",
    answer={"type": "multi", "parts": [{"label": "(a) valence electrons", **tnum(LW.STRUCTS["CS2"].total_valence())},
                                       {"label": "(b) lone pairs", **tnum(sum(LW.STRUCTS["CS2"].lp.values()), traps=[(6, "With 6 lone pairs and single bonds, C would have only 4 electrons.")])}]},
    hints=["C 4 + 2 × S 6: S is in group 16, like O.", "After steps 2–5, C has only 4 electrons; turn one lone pair on each S into a bond, as with ethyne's carbons (Day 8 p.25)."],
    solution=f"<p>(a) <strong>16</strong>. (b) <strong>4</strong> lone pairs, two on each S, with two C=S double bonds: {LS('CS2')} It has the same pattern as CO<sub>2</sub>, the textbook's practice molecule (§4.4, PDF p.202).</p>",
    source="Day 8 p.20–21, p.25; " + tb("4.4", 202))

N2_OK = LS("N2", neutral=True)
N2_W1 = LX("N₂ with a double bond", [("N", 0, 0), ("N", 1.3, 0)], [(0, 1, 2)], {0: 2, 1: 2}, neutral=True)
N2_W2 = LX("N₂ with a single bond", [("N", 0, 0), ("N", 1.3, 0)], [(0, 1, 1)], {0: 3, 1: 3}, neutral=True)
N2_W3 = LX("N₂ with a triple bond and no lone pairs", [("N", 0, 0), ("N", 1.3, 0)], [(0, 1, 3)], {}, neutral=True)
add(id="m19-p4", module="m19", kind="practice", level="Standard",
    prompt="<p>Which is the correct Lewis structure of N<sub>2</sub>?</p>",
    answer=choice((N2_OK, True, "Right: 10 valence electrons, and each N has 6 shared + 2 lone = 8."),
                  (N2_W1, False, "That drawing uses 12 electrons; N<sub>2</sub> has only 10."),
                  (N2_W2, False, "That uses 14 electrons: far too many."),
                  (N2_W3, False, "That uses only 6 electrons; each N needs a lone pair to reach 8.")),
    hints=["Count: 2 × 5 = 10 valence electrons.", "Check each option's electron total and each N's octet."],
    solution=f"<p>{N2_OK} :N≡N: uses exactly 10 electrons and gives each N an octet: “A triple bond!” (Day 8 p.20).</p>",
    source="Day 8 p.20")

add(id="m19-p5", module="m19", kind="practice", level="Standard",
    prompt="<p>Hydrazine, N<sub>2</sub>H<sub>4</sub>, has the skeleton H<sub>2</sub>N–NH<sub>2</sub>. In its Lewis structure, (a) how many bonds are there, and (b) how many lone pairs?</p>",
    answer={"type": "multi", "parts": [{"label": "(a) bonds", **tnum(len(LW.STRUCTS["N2H4"].bonds))}, {"label": "(b) lone pairs", **tnum(sum(LW.STRUCTS["N2H4"].lp.values()))}]},
    hints=["2 × 5 + 4 × 1 = 14 valence electrons.", "Five single bonds use 10; the remaining 4 go on the two N atoms."],
    solution=f"<p>(a) <strong>5</strong> single bonds. (b) <strong>2</strong> lone pairs, one on each N. {LS('N2H4')} Each N is a “central” atom with three bonds and a lone pair, like the N in NH<sub>3</sub> (Day 8 p.23).</p>",
    source="Day 8 p.21–23")

P(id="m19-p6", module="m19", kind="practice", level="Textbook preview",
  prompt=f"<p>The textbook draws the hydroxide ion like this: {LS('OH-')} Why the brackets and the − outside?</p>",
  answer=choice(("The charge belongs to the whole ion: the brackets enclose all its electrons, including the extra one.", True, "Right (textbook §4.4)."),
                ("The O atom alone is negative; H is positive.", False, "The charge written outside the brackets is the ion's overall charge."),
                ("Brackets mean the structure has resonance.", False, "Resonance uses a double-headed arrow between structures."),
                ("Brackets show a missing electron.", False, "The ion has one extra electron, not one missing.")),
  hints=["Count: O 6 + H 1 + 1 extra = 8."],
  solution="<p>The brackets show that the whole group of atoms carries the 1− charge (textbook §4.4, PDF p.200); the 8 electrons inside include the extra one.</p>",
  source=tb("4.4", 199, 200))

add(id="m19-transfer", module="m19", kind="transfer", level="Transfer",
    prompt="<p>Ethene, C<sub>2</sub>H<sub>4</sub>, has each C bonded to two H atoms and to the other C. (a) How many valence electrons does it have? (b) What is the bond order of the C–C bond (1, 2, or 3)?</p>",
    answer={"type": "multi", "parts": [{"label": "(a) valence electrons", **tnum(LW.STRUCTS["C2H4"].total_valence())},
                                       {"label": "(b) C–C bond order", **tnum(2, traps=[(3, "That's ethyne, C<sub>2</sub>H<sub>2</sub>. With two H on each C, one extra shared pair is enough."),
                                                                                       (1, "With only single bonds, each C has 6 electrons.")])}]},
    hints=["2 × 4 + 4 × 1 = 12.",
           "Five single bonds use 10. The 2 left over go on one C (steps 4–5), which leaves the other C with only 6. Share that pair between the carbons."],
    solution=f"<p>(a) <strong>12</strong>. (b) <strong>2</strong>, a C=C double bond: {LS('C2H4')} Each C then forms 4 bonds. Compare ethyne's triple bond on Day 8 p.25.</p>",
    source="Day 8 p.21–25")

add(id="m19-m-explain", module="m19", kind="mastery", level="Explain",
    prompt="<p>Use ozone (Day 8 p.28–30) to explain what to do when the central atom still lacks an octet after step 5's leftover electrons are placed.</p>",
    answer={"type": "self", "model": "<p>O<sub>3</sub> has 18 valence electrons. After single bonds, three lone pairs on each end O, and the leftover pair on the center, the central O has only 6 electrons. "
                                     "No electrons are left to add, so a lone pair on an end O becomes a second bond to the center. Now every O has an octet: O=O–O (Day 8 p.29–30; textbook step 5, PDF p.197).</p>"},
    hints=[], solution="", source="Day 8 p.28–30")

add(id="m19-m-recognize", module="m19", kind="mastery", level="Recognize",
    prompt="<p>Which situation tells you a Lewis structure needs a double or triple bond?</p>",
    answer=choice(("All the electrons are placed, but the central atom has fewer than 8.", True, "Right: share more pairs (Day 8 p.20, p.30)."),
                  ("The molecule contains hydrogen.", False, "H only ever forms single bonds."),
                  ("The electron count is odd.", False, "That signals an unpaired electron, not a multiple bond."),
                  ("An outer atom has three lone pairs.", False, "That's normal for a singly bonded halogen or O.")),
    hints=["Think of HCN and O<sub>3</sub>."], solution="<p>When the electrons run out before the central atom's octet is complete.</p>", source="Day 8 p.20–30")

O2_BAD = LX("O₂ drawn with a single bond", [("O", 0, 0), ("O", 1.3, 0)], [(0, 1, 1)], {0: 3, 1: 3})
add(id="m19-m-sanity", module="m19", kind="mastery", level="Sanity check",
    prompt=f"<p>A student draws O<sub>2</sub> like this:</p><p>{O2_BAD}</p><p>What's wrong?</p>",
    answer=choice(("It uses 14 electrons, but O<sub>2</sub> has only 12. The correct structure has a double bond.", True, "Right (Day 8 p.20)."),
                  ("Nothing; each O has an octet.", False, "Octets alone aren't enough: the electron total must match too."),
                  ("O should have four lone pairs.", False, "That would be even more electrons."),
                  ("The bond should be triple.", False, "A triple bond with an octet on each O uses only 10 electrons; O<sub>2</sub> has 12.")),
    hints=["Count the dots and bonds: 2 × 6 = 12 valence electrons available."],
    solution=f"<p>6 lone pairs + 1 bond = 14 electrons, 2 too many. With 12: {LS('O2')} O=O, “A double bond!” (Day 8 p.20).</p>",
    source="Day 8 p.20")

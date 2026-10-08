"""Problem bank L: mixed review x48 onward (unlabeled problems across Ch. 1-5, weighted toward Day 9-11), and the
relabeling of Ch. 4 mixed items whose topic Day 9 now teaches.

Keys are computed from the checked Lewis structures (lewis.py) and the independent Chapter 5 reference functions
(ch5_data.py: steric numbers, VSEPR names, MO filling). check_problem_bank_l.py re-derives every key with RDKit."""
from guide_common import *                                              # noqa: F401,F403
from problem_bank_a import PROBLEMS, add, num_ans, choice, KJMOL_UNITS  # noqa: F401
from problem_bank_b import text_ans, formula_ans, order_ans           # noqa: F401
from problem_bank_c import P, tb                                       # noqa: F401
from problem_bank_e import X                                           # noqa: F401
from problem_bank_f import LS, LX, tname, tformula, tnum, names        # noqa: F401
import problem_bank_g                                                  # noqa: F401
import lewis as LW                                                     # noqa: F401
import ch5_data as C5
import choice_order

L_START = len(PROBLEMS)


def central(sid):
    s = LW.STRUCTS[sid]
    k = s.central[0]
    return s, k, C5.steric_number(s, k), s.lp.get(k, 0)


def mo(key, q=0):
    sp = next(x for x in C5.MO_SPECIES if x[0] == key)
    return C5.mo_ref(sp[4], sum(sp[3]) - q)


# ------------------------------------------------------------------ Day 9 now teaches these Ch. 4 mixed items' topics
RELABEL = {
    "x39": "Day 9 p.22–23; Day 8 p.30; " + tb("4.7", 209, 211),      # formal charge (four steps and rules, Day 9 p.22–23)
    "x44": "Day 9 p.27; " + tb("4.8", 212),                          # BCl3 is on the electron-deficient slide
    "x47": "Day 9 p.14; " + tb("4.6", 207),                          # Table 4.6 with the C–C/C=C/C≡C rows boxed
}
for _pid, _src in RELABEL.items():
    _p = next(q for q in PROBLEMS if q["id"] == _pid)
    _p["label"] = "lecture"
    _p["source"] = _src

# x27 (bank e): bond polarity from Δχ is Day 9 lecture now (the χ table, p.17; the guidelines, p.18)
_p = next(q for q in PROBLEMS if q["id"] == "x27")
_p["label"] = "lecture"
_p["source"] = "Day 9 p.17–18; " + tb("4.2", 186)
assert "(textbook preview §4.2)" in _p["cue"] and "(textbook guidelines)" in _p["solution"]
_p["cue"] = _p["cue"].replace("(textbook preview §4.2)", "(Day 9 p.18)")
_p["solution"] = _p["solution"].replace("(textbook guidelines)", "(the slide's guidelines, Day 9 p.18)")

# m19-p6 (bank f, textbook preview): the slides draw an ion in brackets too
_p = next(q for q in PROBLEMS if q["id"] == "m19-p6")
if "Day 9 p.30" not in _p["solution"]:
    _p["solution"] = _p["solution"].replace("</p>", " The slides draw sulfate the same way, [SO<sub>4</sub>]<sup>2−</sup> with the charge outside the brackets (Day 9 p.30).</p>", 1)

# =====================================================================================
# Mixed review x48-x64 (Day 9-11 lecture + Ch. 5 textbook preview; unlabeled until answered)
# =====================================================================================
s_ncl3, _, sn, lp = central("NCl3")
assert (sn, lp) == (4, 1) and C5.MG[(sn, lp)] == "trigonal pyramidal" and s_ncl3.total_valence() == 26
X(id="x48", label="lecture", prompt="<p>What is the molecular geometry of nitrogen trichloride, NCl<sub>3</sub>?</p>",
  answer=choice(("trigonal pyramidal", True, "Right: 3 bonded atoms + 1 lone pair (SN 4), like NH<sub>3</sub>."),
                ("trigonal planar", False, "Three atoms around N, but N also has a lone pair: SN 4, not 3."),
                ("tetrahedral", False, "That's the electron-pair geometry. The molecular geometry describes the atoms only (Day 10 p.16)."),
                ("T-shaped", False, "T-shaped needs SN 5 (two lone pairs); N can't hold more than an octet.")),
  hints=["Draw the Lewis structure first: 5 + 3 × 7 = 26 valence electrons…",
         "Three N–Cl bonds and the Cl lone pairs use 24 electrons; the last 2 are a lone pair on N, so SN = 3 + 1."],
  solution=f"<p>{LS('NCl3')} 26 valence electrons: three N–Cl bonds, three lone pairs on each Cl, and one lone pair on N, so SN = 4. The electron pairs are tetrahedral, and the three Cl atoms form a <strong>trigonal pyramid</strong>, exactly like NH<sub>3</sub> (Day 10 p.16–18).</p>",
  cue="“Molecular geometry” → Lewis structure → steric number → electron-pair geometry → the atoms only (Day 10 p.8, p.16).",
  source="Day 10 p.16–18", home="m21")

def net_dchi(center, ligands, sn, nlp=0):
    """Δχ-weighted vector sum on the ideal VSEPR shape (ch5_data's polyhedra, preferred lone-pair placement)."""
    dirs = C5._shape_dirs(sn, nlp, "A", None)
    v = sum((ELECTRONEGATIVITY[x] - ELECTRONEGATIVITY[center]) * d for x, d in zip(ligands, dirs))
    return float((v @ v) ** 0.5)


pol = {"CH2O": net_dchi("C", ["O", "H", "H"], 3), "SiF4": net_dchi("Si", ["F"] * 4, 4), "BeCl2": net_dchi("Be", ["Cl"] * 2, 2),
       "SO3": net_dchi("S", ["O"] * 3, 3)}
assert pol["CH2O"] > 0.5 and max(pol["SiF4"], pol["BeCl2"], pol["SO3"]) < 1e-9
X(id="x49", label="lecture", prompt="<p>Which molecule is polar?</p>",
  answer=choice(("CH<sub>2</sub>O", True, "Right: the C=O bond dipole is not balanced by the two small C–H dipoles."),
                ("SiF<sub>4</sub>", False, "Its Si–F bonds are very polar, but four equal dipoles pointing to the corners of a tetrahedron cancel, as in CF<sub>4</sub> (Day 10 p.30)."),
                ("BeCl<sub>2</sub>", False, "Linear, with two equal Be–Cl dipoles perfectly opposed, as in CO<sub>2</sub> (Day 10 p.29)."),
                ("SO<sub>3</sub>", False, "Trigonal planar with three identical S–O bonds (resonance makes them equal): the dipoles cancel.")),
  hints=["Polar bonds aren't enough; look at the shape and whether the atoms around the center are all the same…",
         "Which molecule has different atoms bonded to its central atom?"],
  solution="<p><strong>CH<sub>2</sub>O</strong>. All four molecules have polar bonds, but SiF<sub>4</sub> (tetrahedral), BeCl<sub>2</sub> (linear), and SO<sub>3</sub> (trigonal planar) each have identical atoms arranged symmetrically, so their bond dipoles cancel (the reasoning of Day 10 p.29–30). In formaldehyde the strong C=O dipole toward O is not balanced by the nearly nonpolar C–H bonds (textbook Sample Ex. 5.4).</p>",
  cue="“Polar molecule?” → polar bonds AND a shape whose bond dipoles don't cancel; different atoms around the center usually means polar (Day 10 p.29–31).",
  source="Day 10 p.29–31; " + tb("5.3", 245, 246), home="m22")

s_o3 = LW.STRUCTS["O3a"]
assert C5.HYB[C5.steric_number(s_o3, 1)] == "sp2"
X(id="x50", label="lecture", prompt="<p>What is the hybridization of the central O atom in ozone, O<sub>3</sub>?</p>",
  answer=choice(("sp<sup>2</sup>", True, "Right: SN 3 (2 bonded atoms + 1 lone pair) → three sp<sup>2</sup> hybrids, with one p orbital left over."),
                ("sp<sup>3</sup>", False, "Count the central O's own electron domains: 2 bonded atoms + 1 lone pair = 3, not 4."),
                ("sp", False, "Two bonded atoms, but the lone pair is a third electron domain.")),
  hints=["One hybrid orbital per electron domain…", "Central O: two O neighbors and one lone pair."],
  solution="<p>In either resonance structure the central O has 2 bonded atoms + 1 lone pair: SN 3 (Day 10 p.14), so it uses <strong>sp<sup>2</sup></strong> hybrids (Day 11 p.12, p.24). Its leftover p orbital makes the π bond, which resonance spreads over both O–O bonds (textbook §5.7, PDF p.270).</p>",
  cue="“Hybridization of an atom” → count its electron domains (bonded atoms + lone pairs): 2 sp, 3 sp<sup>2</sup>, 4 sp<sup>3</sup> (Day 11 p.12, p.24).",
  source="Day 10 p.14; Day 11 p.12, p.24; " + tb("5.7", 270), home="m23")

# vinylacetylene HC≡C–CH=CH2: bonds C–H, C≡C, C–C, C–H, C=C, C–H, C–H
VINYLACET = [("C", "H", 1), ("C", "C", 3), ("C", "C", 1), ("C", "H", 1), ("C", "C", 2), ("C", "H", 1), ("C", "H", 1)]
n_sig, n_pi = len(VINYLACET), sum(o - 1 for *_, o in VINYLACET)
assert (n_sig, n_pi) == (7, 3)
X(id="x51", label="lecture", prompt="<p>Vinylacetylene, HC≡C–CH=CH<sub>2</sub>, was once the starting material for a synthetic rubber. How many σ bonds and how many π bonds does it have?</p>",
  answer={"type": "multi", "parts": [
      {"label": "σ bonds", **tnum(n_sig, traps=[(sum(o for *_, o in VINYLACET), "Count a double or triple bond as one σ bond plus π bonds, not as two or three σ bonds.")])},
      {"label": "π bonds", **tnum(n_pi, traps=[(2, "C≡C has two π bonds and C=C has one."), (1, "The triple bond has two π bonds.")])}]},
  hints=["Every bond, single or multiple, contains exactly one σ bond…", "The bonds: four C–H, C≡C, C–C, and C=C."],
  solution="<p>Seven bonds → <strong>7 σ</strong> (four C–H, C≡C, C–C, C=C). The C≡C adds two π bonds and the C=C one: <strong>3 π</strong> (Day 11 p.17, p.23).</p>",
  cue="“How many σ and π bonds” → one σ per bond; each double bond adds 1 π, each triple bond 2 (Day 11 p.17, p.23).", source="Day 11 p.17, p.23", home="m24")

assert s_o3.total_valence() == 18
X(id="x52", label="lecture", prompt="<p>Ozone has two Lewis structures, O=O–O and O–O=O. Which statement about the real molecule is correct?</p>",
  answer=choice(("Both O–O bonds are 128 pm long, between a typical O–O bond (148 pm) and O=O bond (121 pm).", True, "Right: the real molecule is always in between, an average of the two structures (Day 9 p.7–9)."),
                ("One O–O bond is 121 pm and the other is 148 pm, as one Lewis structure shows.", False, "That's what a single structure predicts; measurements find two equal bonds (Day 9 p.7)."),
                ("The molecule switches back and forth between the two structures.", False, "The slide rules this out: the molecule is NOT changing back and forth; it is always in between (Day 9 p.9)."),
                ("Both bonds are double bonds, 121 pm.", False, "Two double bonds plus ozone's 18 valence electrons would put 10 electrons on the central O.")),
  hints=["Resonance structures differ only in where electrons are drawn…", "Compare 128 pm with 148 pm and 121 pm."],
  solution="<p>Measured: both bonds are 128 pm (Day 9 p.7). Neither structure alone is right; the molecule is “ALWAYS somewhere in between”, an average (Day 9 p.9), drawn as a resonance hybrid with partial bonds (Day 9 p.10).</p>",
  cue="Two structures that differ only in where electrons sit, joined by ↔ → resonance: the real bonds are averages (Day 9 p.7–10).", source="Day 9 p.7–10", home="t4-5")

counts = {sid: LW.STRUCTS[sid].total_valence() for sid in ("NO2-rad1", "SO2-1", "O3a", "CO2")}
assert counts == {"NO2-rad1": 17, "SO2-1": 18, "O3a": 18, "CO2": 16}
X(id="x53", label="lecture", prompt="<p>Which of these is a free radical?</p>",
  answer=choice(("NO<sub>2</sub>", True, "Right: 5 + 2 × 6 = 17 valence electrons, an odd number, so one must be unpaired (Day 9 p.28)."),
                ("SO<sub>2</sub>", False, "6 + 2 × 6 = 18: an even count, so every electron can pair."),
                ("O<sub>3</sub>", False, "18 valence electrons: even."),
                ("CO<sub>2</sub>", False, "16 valence electrons: even.")),
  hints=["Count the valence electrons…", "A radical has an odd count."],
  solution="<p><strong>NO<sub>2</sub></strong>: 17 valence electrons. An odd number “forces some of them to be unpaired”: a radical (Day 9 p.28). SO<sub>2</sub> and O<sub>3</sub> (18) and CO<sub>2</sub> (16) have even counts.</p>",
  cue="“Radical”, “unpaired electron”, or an odd valence-electron count → an exception to the octet rule (Day 9 p.28).", source="Day 9 p.28", home="t4-8")

shells = {sid: central(sid)[0].shell(central(sid)[1]) for sid in ("SF6", "NF3", "CF4", "OF2")}
assert shells == {"SF6": 12, "NF3": 8, "CF4": 8, "OF2": 8}
X(id="x54", label="lecture", prompt="<p>In which molecule does the central atom have more than eight valence electrons around it?</p>",
  answer=choice(("SF<sub>6</sub>", True, "Right: six S–F bonds put 12 electrons around S, a third-row atom (Day 9 p.29)."),
                ("NF<sub>3</sub>", False, "N: 3 bonds + 1 lone pair = 8. A second-row atom can't expand its octet."),
                ("CF<sub>4</sub>", False, "C: 4 bonds = 8."),
                ("OF<sub>2</sub>", False, "O: 2 bonds + 2 lone pairs = 8.")),
  hints=["Which central atom is in the third row or below?", "Count the bonds on S: six."],
  solution="<p><strong>SF<sub>6</sub></strong>: 12 electrons around S. “Atoms of nonmetals in the third row and below can have expanded octets”, especially when bonded to F, O, or Cl (Day 9 p.29).</p>",
  cue="A third-row (or lower) central atom with more than four bonds → an expanded octet (Day 9 p.29).", source="Day 9 p.29–30", home="t4-8")

shapes = {sid: C5.MG[central(sid)[2:]] for sid in ("CO2", "SO2-1", "H2O", "O3a")}
assert shapes == {"CO2": "linear", "SO2-1": "bent (angular)", "H2O": "bent (angular)", "O3a": "bent (angular)"}
X(id="x55", label="lecture", prompt="<p>Which molecule is linear?</p>",
  answer=choice(("CO<sub>2</sub>", True, "Right: C has two double bonds and no lone pairs, so SN 2: 180° (Day 10 p.10)."),
                ("SO<sub>2</sub>", False, "Same pattern as CO<sub>2</sub> on paper, but S keeps a lone pair: SN 3, bent."),
                ("H<sub>2</sub>O", False, "Two lone pairs on O: SN 4, bent, 104.5° (Day 10 p.19)."),
                ("O<sub>3</sub>", False, "One lone pair on the central O: SN 3, bent, 117° (Day 10 p.15).")),
  hints=["Draw each Lewis structure and look at the central atom's lone pairs…",
         "Lone pairs count toward the steric number even though the molecular geometry ignores them."],
  solution="<p>Only <strong>CO<sub>2</sub></strong>: its C has 2 bonded atoms and no lone pairs (SN 2, linear). SO<sub>2</sub> looks similar on paper, but its S has a lone pair (SN 3, bent); H<sub>2</sub>O (SN 4) and O<sub>3</sub> (SN 3) are bent too.</p>",
  cue="The same formula pattern (two atoms on a central atom) doesn't mean the same shape: the central atom's lone pairs decide (Day 10 p.10, p.14–19).",
  source="Day 10 p.10, p.14–19; " + tb("5.2", 240), home="m20")

X(id="x56", label="lecture", prompt="<p>Ozone and water are both bent. Which has the larger bond angle, and why?</p>",
  answer=choice(("O<sub>3</sub>: its central atom has SN 3 (trigonal planar electron pairs), while water's O has SN 4.", True, "Right: 117° vs 104.5° (Day 10 p.15, p.19)."),
                ("Neither: both are bent, so their angles are the same.", False, "“The same geometry NAME as for ozone, but not the same bond angle!” (Day 10 p.19)"),
                ("H<sub>2</sub>O: its O–H bonds are shorter, so the H atoms spread out more.", False, "Bond length doesn't set VSEPR angles; the number of electron domains does."),
                ("O<sub>3</sub>: O atoms are bigger than H atoms, so they push apart.", False, "Tempting, but VSEPR explains it with electron domains: 3 around ozone's central O, 4 around water's O.")),
  hints=["Count the electron domains on each central atom…", "Ozone's central O: 2 atoms + 1 lone pair. Water's O: 2 atoms + 2 lone pairs."],
  solution="<p><strong>O<sub>3</sub></strong> (117°) beats H<sub>2</sub>O (104.5°). Ozone's central O has SN 3, so its electron pairs start from 120°; water's O has SN 4, starting from 109.5°, and its two lone pairs squeeze the angle further (Day 10 p.14–19).</p>",
  cue="Same shape name, different angle → compare steric numbers first, then lone pairs (Day 10 p.19).", source="Day 10 p.14–19", home="m21")

pol2 = {"OCS": net_dchi("C", ["O", "S"], 2), "CS2": net_dchi("C", ["S", "S"], 2)}
assert pol2["OCS"] > 0.5 and pol2["CS2"] < 1e-9 and ELECTRONEGATIVITY["C"] == ELECTRONEGATIVITY["S"]
X(id="x57", label="lecture", prompt="<p>Carbonyl sulfide (O=C=S) and carbon disulfide (S=C=S) are both linear. Which is polar?</p>",
  answer=choice(("O=C=S only", True, "Right: its two bond dipoles are unequal (C=O Δχ 1.0, C=S Δχ 0), so they can't cancel."),
                ("S=C=S only", False, "C and S have the same χ (2.5), so CS<sub>2</sub>'s bonds aren't even polar."),
                ("both", False, "S=C=S has two identical, nonpolar bonds: there is nothing to add up."),
                ("neither: linear molecules are always nonpolar", False, "A linear shape cancels the bond dipoles only when the two are equal.")),
  hints=["Same shape; now compare the two bonds in each molecule…", "Δχ: C=O 3.5 − 2.5; C=S 2.5 − 2.5."],
  solution="<p><strong>O=C=S only</strong>. In CO<sub>2</sub> two equal dipoles are perfectly opposed (Day 10 p.29). In O=C=S the C=O dipole (Δχ 1.0) has no equal partner opposite it, because C=S has Δχ = 0, so a net dipole remains. S=C=S is nonpolar on two counts: it is linear, and its bonds have Δχ = 0 (the textbook asks about CS<sub>2</sub>, PDF p.246).</p>",
  cue="Polarity of a symmetric-looking shape → cancellation needs equal bond dipoles, not just a symmetric shape (Day 10 p.29–31).",
  source="Day 10 p.29–31; Day 9 p.17; " + tb("5.3", 246), home="m22")

X(id="x58", prompt="<p>Which compound is chiral?</p>",
  answer=choice(("CH<sub>3</sub>CH<sub>2</sub>CH(CH<sub>3</sub>)CH<sub>2</sub>CH<sub>2</sub>CH<sub>3</sub>", True, "Right: its third carbon carries H, CH<sub>3</sub>, CH<sub>2</sub>CH<sub>3</sub>, and CH<sub>2</sub>CH<sub>2</sub>CH<sub>3</sub>, four different groups."),
                ("CH<sub>3</sub>CH<sub>2</sub>CH(CH<sub>3</sub>)CH<sub>2</sub>CH<sub>3</sub>", False, "Its CH carbon has two identical CH<sub>2</sub>CH<sub>3</sub> groups, one on each side."),
                ("CH<sub>3</sub>CH(CH<sub>3</sub>)CH<sub>2</sub>CH<sub>3</sub>", False, "Its CH carbon carries two identical CH<sub>3</sub> groups."),
                ("CH<sub>3</sub>CHCl<sub>2</sub>", False, "Two identical Cl atoms on the same carbon.")),
  hints=["Look for an sp<sup>3</sup> carbon bonded to four different groups…",
         "For each CH carbon, write out the whole group on each side; branches that start the same can differ farther along."],
  solution="<p><strong>CH<sub>3</sub>CH<sub>2</sub>CH(CH<sub>3</sub>)CH<sub>2</sub>CH<sub>2</sub>CH<sub>3</sub></strong>. Its CH carbon has four different groups: H, CH<sub>3</sub>, an ethyl group, and a propyl group. In CH<sub>3</sub>CH<sub>2</sub>CH(CH<sub>3</sub>)CH<sub>2</sub>CH<sub>3</sub> the two groups on either side of the CH are both ethyl, so that carbon is not a stereocenter (textbook §5.6).</p>",
  cue="“Chiral” → find an sp<sup>3</sup> carbon with four different groups; compare whole branches, not just the first atom (textbook §5.6).",
  source=tb("5.6", 256, 259), home="t5-6")

bo = {k: mo(*k)["bo"] for k in (("B2", 0), ("B2", -2), ("F2", 0), ("F2", -2))}
assert bo == {("B2", 0): 1, ("B2", -2): 2, ("F2", 0): 1, ("F2", -2): 0}
X(id="x59", prompt="<p>Adding two electrons to a molecule can strengthen or break its bond. Which bond gets stronger: B<sub>2</sub> → B<sub>2</sub><sup>2−</sup>, or F<sub>2</sub> → F<sub>2</sub><sup>2−</sup>?</p>",
  answer=choice(("B<sub>2</sub> → B<sub>2</sub><sup>2−</sup> only", True, "Right: both new electrons go into bonding π<sub>2p</sub> orbitals, so the bond order rises from 1 to 2."),
                ("F<sub>2</sub> → F<sub>2</sub><sup>2−</sup> only", False, "F<sub>2</sub>'s next empty orbital is σ*<sub>2p</sub>, antibonding: the bond order falls from 1 to 0."),
                ("both", False, "Which orbitals receive the electrons, bonding or antibonding? It differs for these two."),
                ("neither: adding electrons always weakens a bond", False, "Electrons added to bonding orbitals raise the bond order.")),
  hints=["Bond order = ½(bonding − antibonding)…",
         "Find each molecule's lowest empty orbitals: B<sub>2</sub> (Z ≤ 7 order) has half-filled π<sub>2p</sub>; F<sub>2</sub> has only σ*<sub>2p</sub> left."],
  solution="<p>B<sub>2</sub> has 6 valence electrons, (σ<sub>2s</sub>)<sup>2</sup>(σ*<sub>2s</sub>)<sup>2</sup>(π<sub>2p</sub>)<sup>2</sup>, bond order 1. Two more fill the π<sub>2p</sub> orbitals: ½(6 − 2) = 2. F<sub>2</sub> has 14, bond order 1; two more go into σ*<sub>2p</sub>: ½(8 − 8) = 0, so F<sub>2</sub><sup>2−</sup> has no bond at all. Only <strong>B<sub>2</sub>'s bond gets stronger</strong> (textbook §5.7, Figs. 5.49–5.50).</p>",
  cue="Ions of diatomic molecules → MO diagram: do the added or removed electrons sit in bonding or antibonding orbitals? (textbook §5.7).",
  source=tb("5.7", 265, 266), home="t5-7")

c2, c2_wrong = C5.mo_ref("low", 8), C5.mo_ref("high", 8)
assert (c2["bo"], c2["unpaired"], c2_wrong["bo"], c2_wrong["unpaired"]) == (2, 0, 2, 2)
X(id="x60", prompt="<p>Using the molecular orbital order that applies to C<sub>2</sub>, what are its bond order and magnetism?</p>",
  answer=choice(("bond order 2, diamagnetic", True, "Right: (σ<sub>2s</sub>)<sup>2</sup>(σ*<sub>2s</sub>)<sup>2</sup>(π<sub>2p</sub>)<sup>4</sup>, every electron paired."),
                ("bond order 2, paramagnetic", False, "That's what O<sub>2</sub>'s order gives (σ<sub>2p</sub> filled before π<sub>2p</sub>, leaving two π electrons unpaired). For Z ≤ 7, π<sub>2p</sub> lies lower."),
                ("bond order 4, diamagnetic", False, "Count the antibonding electrons too: ½(6 − 2)."),
                ("bond order 1, paramagnetic", False, "That's B<sub>2</sub>, with two fewer electrons.")),
  hints=["C<sub>2</sub> has 8 valence electrons, and Z ≤ 7 puts π<sub>2p</sub> below σ<sub>2p</sub>…", "Fill σ<sub>2s</sub>, σ*<sub>2s</sub>, then both π<sub>2p</sub> orbitals."],
  solution="<p>8 valence electrons fill (σ<sub>2s</sub>)<sup>2</sup>(σ*<sub>2s</sub>)<sup>2</sup>(π<sub>2p</sub>)<sup>4</sup> (π<sub>2p</sub> below σ<sub>2p</sub> for Z ≤ 7, textbook Fig. 5.49). Bond order ½(6 − 2) = <strong>2</strong>; no unpaired electrons, so it is <strong>diamagnetic</strong> (Fig. 5.50).</p>",
  cue="A second-row diatomic → pick the right MO order (Z ≤ 7: π<sub>2p</sub> below σ<sub>2p</sub>), fill it, then count (textbook §5.7).",
  source=tb("5.7", 265, 266), home="t5-7")

s_c2h4 = LW.STRUCTS["C2H4"]
assert C5.HYB[C5.steric_number(s_c2h4, 0)] == "sp2" and C5.partner_orbital(s_c2h4, 2) == "H 1s"
X(id="x61", label="lecture", prompt="<p>Which orbitals overlap to form each C–H bond in ethylene, C<sub>2</sub>H<sub>4</sub>?</p>",
  answer=choice(("a C sp<sup>2</sup> hybrid and an H 1s orbital", True, "Right: each C has SN 3 (three bonded atoms), and H always uses its 1s (Day 11 p.20)."),
                ("a C sp<sup>3</sup> hybrid and an H 1s orbital", False, "That's methane's carbon (SN 4). Each of ethylene's carbons has three bonded atoms: SN 3."),
                ("an unhybridized C 2p orbital and an H 1s orbital", False, "Each C's unhybridized p orbital makes the C=C π bond; σ bonds use hybrids."),
                ("a C sp<sup>2</sup> hybrid and an H sp<sup>2</sup> hybrid", False, "Hydrogen has only its 1s orbital: “Hydrogen uses a 1s orbital to make bonds” (Day 11 p.20).")),
  hints=["Find each carbon's steric number…", "σ bonds are head-on overlaps of a hybrid with the partner's orbital; H uses 1s."],
  solution="<p>Each carbon bonds to 3 atoms with no lone pairs: SN 3 → <strong>sp<sup>2</sup></strong>. Each C–H σ bond is a C sp<sup>2</sup>–H 1s overlap; the remaining sp<sup>2</sup> hybrids make the C–C σ bond, and the unhybridized p orbitals make the π bond (Day 11 p.20, p.25).</p>",
  cue="“Which orbitals overlap” → each atom's hybridization from its SN; H always 1s; σ head-on, π side-to-side (Day 11 p.20).", source="Day 11 p.20, p.25", home="m23")

dchi = {b: round(abs(ELECTRONEGATIVITY[b[0]] - ELECTRONEGATIVITY[b[1]]), 1) for b in (("O", "H"), ("N", "H"), ("C", "Cl"), ("C", "H"))}
assert dchi == {("O", "H"): 1.4, ("N", "H"): 0.9, ("C", "Cl"): 0.5, ("C", "H"): 0.4}
X(id="x62", label="lecture", prompt="<p>Which bond is the most polar?</p>",
  answer=choice(("O–H", True, "Right: Δχ = 3.5 − 2.1 = 1.4."), ("N–H", False, "Δχ = 3.0 − 2.1 = 0.9."),
                ("C–Cl", False, "Δχ = 3.0 − 2.5 = 0.5."), ("C–H", False, "Δχ = 2.5 − 2.1 = 0.4: right at the nonpolar cutoff.")),
  hints=["Bond polarity grows with the electronegativity difference…", "From the χ table: H 2.1, C 2.5, N 3.0, O 3.5, Cl 3.0."],
  solution="<p>Δχ: O–H 1.4, N–H 0.9, C–Cl 0.5, C–H 0.4. The largest difference, <strong>O–H</strong>, makes the most polar bond (Day 9 p.17–18).</p>",
  cue="“Most polar bond” → the largest Δχ (Day 9 p.17–18).", source="Day 9 p.17–18", home="t4-2")

s_if5, _, sn, lp = central("IF5")
assert (sn, lp) == (6, 1) and C5.EPG[sn] == "octahedral" and C5.MG[(sn, lp)] == "square pyramidal"
X(id="x63", label="lecture", prompt=f"<p>Iodine pentafluoride, IF<sub>5</sub>:</p><p>{LS('IF5', scale=0.85)}</p><p>Give (a) its electron-pair geometry and (b) its molecular geometry.</p>",
  answer={"type": "multi", "parts": [
      {"label": "(a) electron-pair geometry", **choice(("octahedral", True, "Right: SN 6 (5 bonded atoms + 1 lone pair)."),
                                                       ("trigonal bipyramidal", False, "Five atoms, but the lone pair counts too: SN 6."),
                                                       ("square pyramidal", False, "That's the molecular geometry; the electron-pair geometry includes the lone pair."),
                                                       ("tetrahedral", False, "Count again: 5 + 1 = 6 electron domains."))},
      {"label": "(b) molecular geometry", **choice(("square pyramidal", True, "Right: one lone pair on an octahedron; all six positions are equivalent (Day 10 p.24)."),
                                                   ("trigonal bipyramidal", False, "That's SN 5 with no lone pairs, like PF<sub>5</sub>."),
                                                   ("seesaw", False, "Seesaw is SN 5 with one lone pair."),
                                                   ("square planar", False, "Square planar is SN 6 with two lone pairs."))}]},
  hints=["Count I's electron domains in the Lewis structure…", "SN 6 with one lone pair: does it matter which position the lone pair takes?"],
  solution="<p>I has 5 bonded atoms + 1 lone pair: SN 6, <strong>octahedral</strong> electron pairs. With one lone pair every position is equivalent, so the five F atoms form a <strong>square pyramid</strong> (Day 10 p.24, p.26; the textbook's Table 5.1 uses IF<sub>5</sub> as its example, PDF p.240).</p>",
  cue="A central atom from period 3 or below with five atoms and a lone pair → SN 6 → square pyramidal (Day 10 p.24–26).",
  source="Day 10 p.24–26; " + tb("5.2", 240, 242), home="m21")

X(id="x64", label="lecture", prompt="<p>Acetic acid is CH<sub>3</sub>COOH, with a C=O double bond on the second carbon. Which carbon is sp<sup>2</sup>-hybridized?</p>",
  answer=choice(("the carbon of COOH", True, "Right: three bonded atoms (C, =O, and OH) and no lone pairs: SN 3."),
                ("the carbon of CH<sub>3</sub>", False, "Four bonded atoms (three H and a C): SN 4, sp<sup>3</sup>."),
                ("both carbons", False, "The CH<sub>3</sub> carbon has four single bonds: SN 4."),
                ("neither: carbon is always sp<sup>3</sup>", False, "Carbon's hybridization follows its steric number: SN 3 for a carbon with one double bond and two single bonds.")),
  hints=["Find each carbon's steric number separately…", "A double bond counts as one electron domain."],
  solution="<p>The CH<sub>3</sub> carbon: 4 bonded atoms → SN 4, sp<sup>3</sup>. The COOH carbon: 3 bonded atoms (CH<sub>3</sub>, O, OH) and no lone pairs → SN 3, <strong>sp<sup>2</sup></strong>; its unhybridized p orbital makes the C=O π bond (Day 11 p.12, p.17–19).</p>",
  cue="A molecule with several “central” atoms → find each atom's SN separately (Day 11 p.22–26).", source="Day 11 p.12, p.17–26", home="m24")

# written correct-option-first, like the Ch. 4 banks: spread the correct answers over the positions
L_CHOICE_PERMS = choice_order.spread(PROBLEMS[L_START:], record=None)

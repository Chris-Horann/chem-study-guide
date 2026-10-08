"""Problem bank M: Ch. 18 §18.4-18.5 only (Day 12 p.14-25): metals, band theory, conductors, insulators, semiconductors,
and doping; plus mixed review x65-x66.

Day 12 teaches the band picture from MO diagrams (Na2, Na4, Na_N, Zn_N; p.19-23), the conductor/insulator rule (p.18),
the professor's band sketch (p.24), and doping with P and Ga (p.25), so most items are lecture items. The numbers (Si's
band gap 106 kJ/mol; donor 4 and acceptor 7 kJ/mol) and the word "holes" are textbook §18.5 (PDF p.920), so the items
that use them are preview items. Keys are computed here (orbital and electron counts; E = hc/lambda per electron);
check_problem_bank_m.py re-derives them independently (numpy eigenvalues of the cluster model, pint units, and group
numbers from the periodictable package).

Textbook overlap (checked 2026-10-06): the textbook's §18.4-18.5 cases are Na, Zn, Si, P, Ga, NaCl, GaAs, AlGaAs2, GaN,
CdS/CdSe and the Concept Tests on Mg and on GaAs doped with Se or Sn (PDF p.918-921). The problems use Be, K, Li, Ca, Ge,
quartz, As, B, and Sb instead; Na, Zn, Si, P, and Ga appear only as the lecture's own examples. The band explorer's cases
(Na clusters; diamond, zinc, sodium, silicon, P- and Ga-doped silicon) are not attempt or transfer species, except that
the transfer problem uses silicon's band gap to find a photon wavelength, which the explorer never computes."""
from guide_common import *                                              # noqa: F401,F403
from problem_bank_a import PROBLEMS, add, num_ans, choice, NM_UNITS     # noqa: F401
from problem_bank_b import order_ans                                   # noqa: F401
from problem_bank_c import P, tb                                       # noqa: F401
from problem_bank_e import X                                           # noqa: F401
from problem_bank_f import tnum                                        # noqa: F401
import problem_bank_l                                                  # noqa: F401  (earlier banks load first)
import choice_order

M_START = len(PROBLEMS)

# ---------------------------------------------------------------- counts (one MO per atomic orbital, two electrons per MO)
def cluster(n_atoms, orbitals_per_atom, electrons_per_atom):
    mos = n_atoms * orbitals_per_atom
    e = n_atoms * electrons_per_atom
    filled = -(-e // 2)                     # a lone electron still occupies an MO
    return {"mos": mos, "electrons": e, "filled": filled, "empty": mos - filled}


BE10 = cluster(10, 1, 2)                    # ten Be 2s orbitals, 2 electrons each
K12 = cluster(12, 1, 1)                     # twelve K 4s orbitals, 1 electron each
NA20 = cluster(20, 4, 1)                    # 3s + three 3p per Na
NA100 = cluster(100, 1, 1)
assert (BE10["mos"], BE10["filled"], K12["empty"], NA20["mos"], NA100["mos"], NA100["filled"]) == (10, 10, 6, 80, 100, 50)

# ---------------------------------------------------------------- the transfer: longest wavelength that crosses Si's gap
EG_SI = 106e3                               # J/mol, textbook PDF p.920
E_PER_E = EG_SI / NA                        # J per electron
LAM_SI = HC / E_PER_E                       # m
LAM_SI_NM = LAM_SI * 1e9
assert abs(LAM_SI_NM - 1128.5) < 1

# =====================================================================================
# m25  Metals, bands, and semiconductors (Day 12 p.14-25; §18.4-18.5)
# =====================================================================================
add(id="m25-attempt", module="m25", kind="attempt", level="Guided attempt",
    prompt="<p>Beryllium, [He]2s<sup>2</sup>, is a metal and conducts electricity. Picture a small cluster of 10 Be atoms whose 2s orbitals combine into molecular orbitals.</p>"
           "<p>(a) How many MOs do the ten 2s orbitals form? (b) How many of those MOs are filled in the ground state? (c) Which statement explains why solid beryllium conducts?</p>",
    answer={"type": "multi", "parts": [
        {"label": "(a) MOs from the 2s orbitals", **tnum(BE10["mos"], traps=[
            (20, "That's the number of electrons. Count orbitals: “one molecular orbital out for every atomic orbital that we put in” (Day 12 p.7)."),
            (5, "Ten 2s orbitals go in, so ten MOs come out (Day 12 p.7).")])},
        {"label": "(b) filled MOs", **tnum(BE10["filled"], traps=[
            (5, "Each Be atom brings two 2s electrons: 20 electrons, two per MO, fill all ten."),
            (20, "An MO holds at most two electrons, so 20 electrons fill 10 MOs.")])},
        {"label": "(c) why Be conducts", **choice(
            ("Its 2s band is full, but an empty band made from the 2p orbitals overlaps it, so electrons can move into empty orbitals.", True,
             "Right: the rule's second case, a filled valence band that overlaps an empty conduction band, as in zinc (Day 12 p.18, p.23)."),
            ("Its 2s band is half filled, like sodium's.", False,
             "Sodium has one 3s electron per atom; beryllium has two 2s electrons per atom, and they fill the 2s band (part b)."),
            ("A full band conducts best, because it has the most electrons.", False,
             "The number of electrons isn't the test. A filled band with no empty band overlapping it doesn't meet the rule (Day 12 p.18): diamond's filled valence band insulates (p.24)."),
            ("Be atoms lose their 2s electrons, and the Be<sup>2+</sup> ions carry the current.", False,
             "The atoms stay in place; mobile electrons carry the current, the “sea” of mobile electrons of Day 8 p.14."))}]},
    hints=["This is band theory: MOs for a whole solid. “We'll get one molecular orbital out for every atomic orbital that we put in” (Day 12 p.7), and each MO holds at most two electrons.",
           "The test for a conductor: “a partially filled valence band or a filled valence band that overlaps with an empty conduction band” (Day 12 p.18).",
           "Ten Be atoms bring ten 2s orbitals and 2 × 10 = 20 valence electrons. How many MOs form, and how many MOs does it take to hold 20 electrons?",
           "Ten MOs, and 20 electrons fill all ten, so the band made from the 2s orbitals is full, like zinc's 4s band (Day 12 p.23). Which part of the rule can a full band still meet?"],
    solution="<p>(a) <strong>10</strong>: one MO for each 2s orbital (Day 12 p.7). (b) <strong>10</strong>: the 20 valence electrons (2 per Be) fill all ten, two per MO. "
             "Counted on its own, the band made from the 2s orbitals is full, and that stays true for the enormous number of atoms in a real piece of beryllium.</p>"
             "<p>(c) A full band can still conduct if an empty band overlaps it. Beryllium's empty 2p orbitals form a band that overlaps the filled 2s band, so electrons can move into empty orbitals: "
             "the second case of the rule (Day 12 p.18), the same picture as zinc's 4s and 4p bands (Day 12 p.23).</p>"
             "<p class='bg'>Beryllium is indeed a metallic conductor; its 2s and 2p bands overlap, as the textbook describes for zinc's 4s and 4p bands (PDF p.919).</p>",
    compare={"wrong": "<p>“Beryllium's 2s band is completely filled, so its electrons have nowhere to go. Beryllium must be an insulator.”</p>",
             "tempting": "The first half is right: on its own, a filled band is what diamond has, and diamond insulates (Day 12 p.24).",
             "fails": "It skips the second half of the rule: “a filled valence band that overlaps with an empty conduction band is an electrical conductor” (Day 12 p.18). "
                      "Beryllium's empty 2p band overlaps its filled 2s band, just as zinc's 4p band overlaps its 4s band (p.23), so beryllium conducts, as a metal should (p.17)."},
    source="Day 12 p.7, p.17–18, p.22–24")

add(id="m25-p1", module="m25", kind="practice", level="Warm-up",
    prompt="<p>Potassium, [Ar]4s<sup>1</sup>, has one valence electron per atom. In a cluster of 12 K atoms, the 4s orbitals combine into molecular orbitals. How many of those MOs are <em>empty</em> in the ground state?</p>",
    answer=tnum(K12["empty"], traps=[(12, "That's the total number of MOs, one per 4s orbital (Day 12 p.7). Twelve electrons fill only six of them."),
                                     (0, "Twelve electrons, two per MO, fill six MOs, and the other six stay empty, as in Na<sub>4</sub>, where two of the four are filled (Day 12 p.21)."),
                                     (24, "There are only 12 MOs, one for each 4s orbital.")]),
    hints=["One MO out for every atomic orbital put in (Day 12 p.7); at most two electrons per MO.",
           "12 orbitals → 12 MOs. The 12 valence electrons fill the lowest 12 ÷ 2 of them."],
    solution="<p>Twelve 4s orbitals give 12 MOs. The 12 valence electrons fill the lowest 6, two per MO, so <strong>6</strong> are empty: "
             "the lower half filled and the upper half empty, the pattern of sodium's 3s levels in Na<sub>2</sub>, Na<sub>4</sub>, and Na<sub><i>N</i></sub> (Day 12 p.19–22).</p>",
    source="Day 12 p.7, p.19–22")

add(id="m25-p2", module="m25", kind="practice", level="Warm-up",
    prompt="<p>Compare a cluster of 6 sodium atoms with a cluster of 60. Which has the smaller HOMO–LUMO gap?</p>",
    answer=choice(("The 60-atom cluster: it has ten times as many MOs from its 3s orbitals, spread over nearly the same range of energies, so neighboring levels are closer.", True,
                   "Right: “the HOMO-LUMO gap gets smaller <em>quickly</em>” as atoms are added (Day 12 p.21)."),
                  ("The 6-atom cluster: fewer electrons means less repulsion, so its levels are closer together.", False,
                   "The gap depends on how many MOs share the range of energies, not on repulsion: more atoms, more MOs, closer levels (Day 12 p.21)."),
                  ("Neither: the gap is fixed by the energy of the Na 3s orbital.", False,
                   "The 3s energy sets where the levels are centered, but the gap between the highest filled and the lowest empty MO shrinks as atoms are added (Day 12 p.19–21)."),
                  ("The 60-atom cluster, because each of its MOs holds more electrons.", False,
                   "Every MO still holds at most two electrons; what changes is how many MOs there are (Day 12 p.7).")),
    hints=["Day 12 p.21: what happens to the HOMO–LUMO gap “as we add more and more atoms”?"],
    solution="<p>The <strong>60-atom cluster</strong>. Each cluster has one MO per 3s orbital, 6 MOs vs. 60 (Day 12 p.7). The levels spread over a range of energies that widens only a little as atoms are added, "
             "so with ten times as many levels, neighbors, including the HOMO and the LUMO, are much closer: “the HOMO-LUMO gap gets smaller <em>quickly</em>” (Day 12 p.21). "
             "In a real piece of sodium the gap is effectively zero, and the levels form a band (p.22).</p>",
    source="Day 12 p.7, p.19–22")

MATCH_ROWS = [("Lithium, [He]2s<sup>1</sup>: its 2s band is half filled", "cond"),
              ("Calcium, [Ar]4s<sup>2</sup>: its filled 4s band overlaps an empty band above it", "cond"),
              ("Germanium: a filled valence band, then a small gap, then an empty band", "semi"),
              ("Quartz (SiO<sub>2</sub>): a filled valence band, then a large gap, then an empty band", "ins")]
add(id="m25-p3", module="m25", kind="practice", level="Concept",
    prompt="<p>Use each band description to classify the solid.</p>",
    answer={"type": "match", "rows": [{"html": h, "answer": k} for h, k in MATCH_ROWS],
            "options": [{"key": "cond", "html": "conductor"}, {"key": "semi", "html": "semiconductor"}, {"key": "ins", "html": "insulator"}]},
    hints=["Day 12 p.18: a conductor has “a partially filled valence band or a filled valence band that overlaps with an empty conduction band”; a “large enough band gap” makes an insulator. "
           "A small gap makes a semiconductor, like the professor's silicon (p.24)."],
    solution="<p>Lithium: <strong>conductor</strong>, a partially filled band, like sodium's (Day 12 p.22). Calcium: <strong>conductor</strong>, a filled band overlapped by an empty one, like zinc's (p.23). "
             "Germanium: <strong>semiconductor</strong>, a small gap, like silicon's (p.24); germanium is a metalloid (p.16). Quartz: <strong>insulator</strong>, a large gap, like diamond's (p.24).</p>",
    source="Day 12 p.16, p.18, p.22–24")

add(id="m25-p4", module="m25", kind="practice", level="Standard",
    prompt="<p>A piece of pure silicon is warmed from room temperature to 100 °C. What happens to its electrical conductivity, and why?</p>",
    answer=choice(("It increases: more electrons have enough energy to jump the gap into the empty band, and they leave vacancies in the filled band.", True,
                   "Right: the professor's “T ↑” panel (Day 12 p.24)."),
                  ("It increases, because heating closes the band gap and silicon becomes a metal.", False,
                   "In the “T ↑” sketch the gap stays the same size; what changes is how many electrons have the energy to cross it (Day 12 p.24)."),
                  ("It doesn't change: the number of valence electrons is fixed.", False,
                   "The number of electrons is fixed, but how many of them sit in the upper, empty band is not (Day 12 p.24)."),
                  ("It decreases, because heated electrons fall back into the filled band.", False,
                   "Heating supplies energy, which lifts electrons up across the gap rather than dropping them down (Day 12 p.24).")),
    hints=["Silicon is the professor's semiconductor: a filled band, a small gap, an empty band. What does the “T ↑” panel add (Day 12 p.24)?"],
    solution="<p>Conductivity <strong>increases</strong>. Silicon's gap is small, so as the temperature rises, more electrons gain enough energy to cross it: the “T ↑” panel shows a strip of electrons at the bottom of the upper band "
             "and a matching empty strip at the top of the lower band (Day 12 p.24). With electrons in a band that has room, and room in the band they left, both bands are partly filled, which is the first case of the conductor rule (p.18).</p>",
    source="Day 12 p.18, p.24")

add(id="m25-p5", module="m25", kind="practice", level="Standard",
    prompt="<p>A small amount of arsenic (As, group 15) replaces some of the atoms in a silicon crystal. Which description is right?</p>",
    answer=choice(("n-type: each As atom brings one more valence electron than the Si it replaces, and those extra electrons sit in a donor level just below the conduction band.", True,
                   "Right: arsenic is in phosphorus's group, so it dopes silicon the way P does (Day 12 p.25)."),
                  ("p-type: arsenic has more electrons, so it pulls electrons out of silicon's valence band.", False,
                   "A dopant with <em>more</em> valence electrons than the host gives n-type silicon, like P (Day 12 p.25); p-type needs one with fewer, like Ga."),
                  ("n-type: each As atom takes an electron from silicon, leaving a negative charge behind.", False,
                   "The label is right, but the reason is backward: arsenic brings an extra electron rather than taking one (its Lewis symbol has 5 dots to silicon's 4, Day 8 p.16–17)."),
                  ("Neither: arsenic is a metalloid like silicon, so nothing changes.", False,
                   "Both are metalloids (Day 12 p.16), but arsenic has 5 valence electrons to silicon's 4, and that difference is what doping uses (Day 12 p.25).")),
    hints=["Compare valence electrons, as the Lewis symbols on Day 12 p.25 do: Si has 4. How many does a group 15 element have?",
           "On p.25, phosphorus (group 15) gives the n-type picture: a donor level just below the conduction band."],
    solution="<p><strong>n-type.</strong> Arsenic, like phosphorus, is in group 15, with 5 valence electrons to silicon's 4 (Day 8 p.16–17). Each As atom that takes a silicon atom's place brings one extra electron, "
             "and the extra electrons occupy a donor level just below the empty conduction band, the picture labeled n-type on Day 12 p.25.</p>",
    source="Day 12 p.16, p.25; Day 8 p.16–17")

P(id="m25-p6", module="m25", kind="practice", level="Standard",
  prompt="<p>Boron (group 13) is added in small amounts to silicon. How does the boron-doped silicon carry a current?</p>",
  answer=choice(("Valence-band electrons move up into the boron acceptor level, leaving positive holes in the valence band; electrons hopping into those holes let charge move.", True,
                 "Right: boron dopes silicon the way gallium does in the textbook (PDF p.920): a p-type semiconductor."),
                ("Boron's extra valence electron moves up into the conduction band.", False,
                 "Boron has one valence electron <em>fewer</em> than silicon (3 vs. 4), so it brings no extra electron. That's the n-type picture, for a group 15 dopant."),
                ("The boron atoms become positive ions that move through the crystal and carry the charge.", False,
                 "The dopant atoms stay fixed in the crystal; the charge moves as electrons fill one hole and open another (textbook PDF p.920)."),
                ("The acceptor level lies just below the conduction band, so its electrons jump into the conduction band.", False,
                 "That's a donor level (n-type). An acceptor level lies just above the valence band and starts out empty (Day 12 p.25).")),
  hints=["Count valence electrons: B has 3, Si 4. Which picture on Day 12 p.25, n-type or p-type, has a dopant with one electron fewer than silicon?",
         "In the p-type picture, the empty acceptor level sits just above the valence band. What happens to the valence band when electrons move up into that level?"],
  solution="<p>Boron, with 3 valence electrons, is one short of silicon's 4, so it makes p-type silicon, as gallium does (Day 12 p.25). Its empty acceptor level lies just above the valence band. "
           "Valence electrons move up into it, leaving behind “positively charged ‘holes’” in the valence band, the ⊕ marks on the slide's figure. "
           "Charge then moves as neighboring electrons hop into the holes, “filling one hole and creating another” (textbook §18.5, PDF p.920).</p>",
  source=tb("18.5", 920) + "; Day 12 p.25")

ORDER_ITEMS = [("donor", "an electron in a phosphorus donor level moving up into silicon's conduction band"),
               ("acceptor", "a silicon valence electron moving up into a gallium acceptor level"),
               ("gapSi", "a valence electron in pure silicon crossing the band gap"),
               ("gapC", "a valence electron in diamond crossing its band gap")]
JUMP_KJ = {"donor": 4, "acceptor": 7, "gapSi": 106}       # textbook PDF p.920; diamond: the professor's "large" gap (Day 12 p.24)
assert sorted(JUMP_KJ, key=JUMP_KJ.get) == ["donor", "acceptor", "gapSi"]
P(id="m25-p7", module="m25", kind="practice", level="Stretch",
  prompt="<p>Order these electron jumps by the energy they need, smallest first.</p>",
  answer=order_ans([(k, h) for k, h in ORDER_ITEMS], ["donor", "acceptor", "gapSi", "gapC"], "smallest (1) to largest (4)"),
  hints=["The textbook's values: a donor level about 4 kJ/mol below the conduction band, an acceptor level about 7 kJ/mol above the valence band, and silicon's gap 106 kJ/mol (PDF p.920).",
         "Diamond is the professor's insulator, with the large gap (Day 12 p.24)."],
  solution="<p>Donor level → conduction band (about 4 kJ/mol) &lt; valence band → Ga acceptor level (about 7 kJ/mol) &lt; across silicon's gap (106 kJ/mol) &lt; across diamond's gap (large; Day 12 p.24). "
           "That is why doping helps so much: it replaces a 106 kJ/mol jump with one of only a few kJ/mol (textbook §18.5, PDF p.920).</p>"
           "<p class='bg'>Diamond's gap is about 530 kJ/mol (5.5 eV), a literature value.</p>",
  source=tb("18.5", 920) + "; Day 12 p.24–25")

P(id="m25-transfer", module="m25", kind="transfer", level="Transfer",
  prompt="<p>Silicon solar cells run on light. A photon can lift an electron from silicon's valence band into its conduction band only if it supplies at least the band-gap energy, "
         "106 kJ/mol (the textbook's value). What is the longest wavelength of light that can do this? Give the answer in nm.</p>",
  answer={**num_ans(LAM_SI_NM, sf=3, unit_label="nm", units=NM_UNITS),
          "traps": [{"value": LAM_SI_NM * 1000, "tol": 0.02, "message": "Convert kJ to J first: 106 kJ/mol = 1.06 × 10<sup>5</sup> J/mol."},
                    {"value": LAM_SI, "tol": 0.02, "message": "That's the wavelength in meters; the box wants nanometers (1 m = 10<sup>9</sup> nm)."}]},
  hints=["One photon lifts one electron, so the photon must supply at least the band-gap energy <em>per electron</em>. The longest wavelength goes with the smallest energy that still works (E = hc/λ, Day 3 p.17; Day 4 p.10).",
         "Per electron: E = (1.06 × 10<sup>5</sup> J/mol) ÷ (6.022 × 10<sup>23</sup> mol<sup>−1</sup>).",
         "λ = hc/E, with h = 6.626 × 10<sup>−34</sup> J·s and c = 2.998 × 10<sup>8</sup> m/s; then convert m to nm."],
  solution=f"<p>Energy per electron: E = (1.06 × 10<sup>5</sup> J/mol) ÷ (6.022 × 10<sup>23</sup> mol<sup>−1</sup>) = {sci(E_PER_E, 4)} J. "
           f"Longest wavelength: λ = hc/E = (6.626 × 10<sup>−34</sup> J·s)(2.998 × 10<sup>8</sup> m/s) ÷ ({sci(E_PER_E, 4)} J) = {sci(LAM_SI, 4)} m = <strong>{sci(LAM_SI_NM, 3)} nm</strong> "
           "(3 significant figures, from 106).</p>"
           "<p>That is in the infrared, just beyond the red end of the visible range (400–750 nm on Day 2 p.29). Shorter wavelengths carry more energy, so every visible photon can lift an electron across silicon's gap; "
           "light with λ longer than about 1130 nm cannot.</p>",
  source=tb("18.5", 920) + "; Day 2 p.29; Day 3 p.17; Day 4 p.10")

add(id="m25-m-explain", module="m25", kind="mastery", level="Explain",
    prompt="<p>Explain, using band theory, why a sodium wire conducts electricity but a diamond does not. Say how many MOs a piece of metal has, how they are filled, and what an electron needs in order to move.</p>",
    answer={"type": "self", "model": "<p>In a piece of sodium, every atom's 3s orbital goes into the MOs, so <i>N</i> atoms give <i>N</i> MOs (Day 12 p.7), so close together in energy that they form a band. "
                                     "Each Na brings one electron, so the <i>N</i> electrons fill only the lower half of the band, two per MO, and empty MOs lie right above the filled ones: "
                                     "a partially filled valence band, which makes sodium a conductor (Day 12 p.18, p.22). Diamond's valence band is completely filled, and the next, empty band lies above "
                                     "a large band gap (p.24), so almost no electron can reach an empty orbital, and diamond is an insulator. An electron needs an empty orbital at nearly its own energy to move into (the textbook's explanation, PDF p.919).</p>"},
    hints=[], solution="", source="Day 12 p.7, p.18, p.22, p.24; " + tb("18.4", 919))

add(id="m25-m-recognize", module="m25", kind="mastery", level="Recognize",
    prompt="<p>Which question calls for band theory rather than a Lewis structure, VSEPR, or the MO diagram of a single molecule?</p>",
    answer=choice(("Why does a copper wire conduct electricity while a diamond does not?", True,
                   "Right: conduction in solids is what band theory explains (Day 12 p.15, p.18)."),
                  ("What is the shape of a silane molecule, SiH<sub>4</sub>?", False, "A shape question: VSEPR or valence bond theory (Day 12 p.13)."),
                  ("Is an O<sub>2</sub> molecule paramagnetic?", False, "A magnetism question about one molecule: its MO diagram (Day 12 p.11, p.13)."),
                  ("How many bonds does a silicon atom usually form?", False, "Connectivity: a Lewis symbol and its bonding capacity answer that (Day 8 p.17–18; Day 12 p.13).")),
    hints=["Day 12 p.13 matches each question to a model; the band slides (p.18–25) are about conduction."],
    solution="<p>The <strong>copper wire and diamond</strong> question: whether a solid conducts depends on how its bands are filled (Day 12 p.18, p.24). "
             "Day 12 p.13 matches the other questions to their models: connectivity → Lewis structures, 3-D shape → VSEPR or valence bond theory, magnetic or spectroscopic properties → MO theory.</p>",
    source="Day 12 p.13, p.15, p.18, p.24; Day 8 p.17–18")

add(id="m25-m-sanity", module="m25", kind="mastery", level="Sanity check",
    prompt="<p>A classmate writes: “The 3s orbitals of 100 sodium atoms form 50 molecular orbitals.” What's wrong?</p>",
    answer=choice(("MOs come one per atomic orbital, so 100 3s orbitals give 100 MOs. Fifty is how many of them the 100 electrons fill.", True,
                   "Right (Day 12 p.7, p.21–22)."),
                  ("Nothing: two electrons per MO, so 100 electrons need 50 MOs.", False,
                   "That counts the filled MOs. The other 50 exist too, empty, and they are why sodium conducts (Day 12 p.22)."),
                  ("It should be 200, because each 3s orbital splits into a bonding and an antibonding MO.", False,
                   "Two atomic orbitals make two MOs, one bonding and one antibonding (Na<sub>2</sub>, Day 12 p.19), so the count stays one MO per atomic orbital.")),
    hints=["How many MOs came out of the two 3s orbitals of Na<sub>2</sub> (Day 12 p.19), and of the four in Na<sub>4</sub> (p.21)?"],
    solution="<p>One MO forms for every atomic orbital that goes in (Day 12 p.7): Na<sub>2</sub> has 2, Na<sub>4</sub> has 4 (p.19–21), and 100 Na atoms have <strong>100</strong> MOs from their 3s orbitals. "
             "The 100 valence electrons fill the lowest 50, two per MO, leaving the upper 50 empty: a half-filled band (p.22). The classmate counted the filled MOs only.</p>",
    source="Day 12 p.7, p.19–22")

# ---------------------------------------------------------------- mixed review
X(id="x65", label="lecture", prompt="<p>A trace of antimony (Sb) is added to germanium. What kind of material results?</p>",
  answer=choice(("an n-type semiconductor", True, "Right: Sb (group 15) has one more valence electron than Ge (group 14), as P has than Si (Day 12 p.25)."),
                ("a p-type semiconductor", False, "p-type needs a dopant with fewer valence electrons than the host, as Ga has than Si (Day 12 p.25). Sb has one more than Ge."),
                ("an insulator", False, "Doping adds electrons (or vacancies) close to the band edges, which raises conductivity; it doesn't open a large gap."),
                ("a metal, because antimony is a metal", False, "Antimony is a metalloid on the course's periodic table (Day 12 p.16), and a trace of it doesn't turn germanium into a metal.")),
  hints=["What group is each element in, and how many valence electrons does each have?", "One more valence electron than the host atom…"],
  solution="<p>Germanium is a metalloid semiconductor in group 14, with 4 valence electrons; antimony, in group 15, has 5 (Day 12 p.16; Lewis symbols, Day 8 p.16–17). "
           "Each Sb atom in germanium's place brings one extra electron, in a donor level just below the conduction band: an <strong>n-type</strong> semiconductor, like P in Si (Day 12 p.25).</p>",
  cue="A trace of one element added to a metalloid → doping: compare the two elements' valence electrons (Day 12 p.25).", source="Day 12 p.16, p.25; Day 8 p.16–17", home="m25")

X(id="x66", label="lecture", prompt="<p>Twenty sodium atoms combine all of their valence orbitals, the 3s and the three 3p orbitals of each atom, into molecular orbitals. How many MOs form?</p>",
  answer=tnum(NA20["mos"], traps=[(20, "That counts only the 3s orbitals. Each Na atom also brings three empty 3p orbitals."),
                                  (60, "Add the 20 MOs from the 3s orbitals too."),
                                  (10, "Twenty electrons fill ten MOs, but the question asks how many MOs form in all.")]),
  hints=["“One molecular orbital out for every atomic orbital that we put in” (Day 12 p.7)…", "Each atom brings 1 + 3 = 4 valence orbitals."],
  solution=f"<p>20 atoms × 4 valence orbitals (one 3s + three 3p) = <strong>{NA20['mos']} MOs</strong> (Day 12 p.7). Only {NA20['filled']} of them are filled, by the 20 valence electrons. "
           "In the solid, the 3s-derived MOs make the valence band and the 3p-derived MOs the empty band that overlaps it (Day 12 p.22).</p>",
  cue="“How many MOs?” → count atomic orbitals, not electrons (Day 12 p.7).", source="Day 12 p.7, p.19–22", home="m25")

# written correct-option-first, like the other banks: spread the correct answers over the positions
M_CHOICE_PERMS = choice_order.spread(PROBLEMS[M_START:], record=None)

"""Problem bank, modules m9-m15 and mixed review. Keys are computed here;
verify_guide.py re-derives them independently."""
import math
from guide_common import *
from problem_bank_a import (PROBLEMS, add, num_ans, choice, FREQ_UNITS, J_UNITS, NM_UNITS,
                            M_UNITS, KJMOL_UNITS, MS_UNITS)

def cfg_target(z, charge=0):
    return {s: k for s, k in ion_config(z, charge)}

def cfg_ans(z, charge, species_html):
    return {"type": "config", "target": cfg_target(z, charge), "electrons": z - charge, "species": species_html}

def order_ans(items, answer_keys, direction):
    return {"type": "order", "direction": direction,
            "items": [{"key": k, "html": h} for k, h in items], "answerOrder": answer_keys}

def text_ans(accepted, ci=True, placeholder=None, kind="text"):
    d = {"type": "text", "accepted": accepted, "caseInsensitive": ci, "kind": kind}
    if placeholder:
        d["placeholder"] = placeholder
    return d

def formula_ans(accepted, placeholder="e.g., MgCl2"):
    return {"type": "text", "accepted": accepted, "caseInsensitive": False, "kind": "formula", "placeholder": placeholder}

Z = {sym: i + 1 for i, (sym, _) in enumerate(ELEMENTS)}

# =====================================================================================
# m9  Orbital shapes & radial distributions  (Day 5 p.17–20; Day 6 p.12, p.18)
# =====================================================================================
add(id="m9-attempt", module="m9", kind="attempt", level="Guided attempt",
    prompt="<p>Look at the two 1s graphs from Day 5 p.17 (reproduced in Explore). Where is the electron density ψ<sup>2</sup> highest, and at what distance is the electron <em>most likely</em> to be found?</p>",
    answer=choice(("Both at the nucleus", False, "ψ² is highest at the nucleus, but a point there has almost no volume around it."),
                  ("Both at 53 pm", False, "ψ² peaks at r = 0, not at 53 pm."),
                  ("ψ² is highest at the nucleus; the most likely distance is 53 pm", True, "Right: density × shell size (4πr²ψ²) peaks at 53 pm (Day 5 p.17)."),
                  ("ψ² is highest at 53 pm; the most likely distance is the nucleus", False, "It's the other way around.")),
    hints=["Two graphs, two questions: Day 5 p.17 plots ψ<sup>2</sup> (panel a) and 4πr<sup>2</sup>ψ<sup>2</sup> (panel b).",
           "ψ<sup>2</sup> is a density: probability per unit volume at one point. It is largest at r = 0.",
           "To get the probability at a <em>distance</em> r, add up every point at that distance: a thin spherical shell of area 4πr<sup>2</sup>. So the probability at distance r goes as 4πr<sup>2</sup>ψ<sup>2</sup>.",
           "At r = 0 the shell has no area, so 4πr<sup>2</sup>ψ<sup>2</sup> = 0; far away, ψ<sup>2</sup> ≈ 0. In between, the product peaks. Where, for 1s?"],
    solution="<p>Density ψ<sup>2</sup> is largest right at the nucleus, but the thin shells near r = 0 have almost no volume. Multiplying by the shell area 4πr<sup>2</sup> gives the radial distribution, which starts at zero and peaks at <strong>53 pm</strong> (Day 5 p.17).</p>",
    compare={
        "wrong": "<p>“The density is highest at the nucleus, so that's where the electron is most likely to be.”</p>",
        "tempting": "“Highest density” sounds like “most likely location.”",
        "fails": "Probability = density × volume. A region right at the nucleus has almost no volume, while a shell at 53 pm has a lot. The Day 5 p.17 graphs show both curves side by side for exactly this reason."},
    source="Day 5 p.17")

add(id="m9-p1", module="m9", kind="practice", level="Warm-up",
    prompt="<p>From the 3s radial distribution (Day 5 p.18, or the Explore panel): not counting r = 0, at how many distances does the probability 4πr<sup>2</sup>ψ<sup>2</sup> fall to zero?</p>",
    answer=num_ans(2, tol=0),
    hints=["Count the places where the 4πr<sup>2</sup>ψ<sup>2</sup> curve touches zero between peaks (not at r = 0).",
           "The 3s curve has three peaks."],
    solution="<p><strong>2</strong>, at about 100 pm and 370 pm, between the three peaks. On Day 5 p.18 they're marked with dashed lines and appear as empty rings in the dot picture. <span class='preview'>Textbook preview: these zero-probability spheres are called <em>nodes</em>, and an s orbital has n − 1 of them (textbook §3.7, PDF p.144, printed 110). The slide marks them with dashed lines but doesn't use the word.</span></p>",
    source="Day 5 p.18")

add(id="m9-p2", module="m9", kind="practice", level="Warm-up",
    prompt="<p>How many 3d orbitals are there?</p>",
    answer=num_ans(5, tol=0),
    hints=["d means ℓ = 2; count the m<sub>ℓ</sub> values.", "m<sub>ℓ</sub> runs from −ℓ to +ℓ in steps of 1: −2, −1, 0, +1, +2."],
    solution="<p><strong>5</strong>, one per m<sub>ℓ</sub> value (−2 … +2): 3d<sub>xy</sub>, 3d<sub>xz</sub>, 3d<sub>yz</sub>, 3d<sub>x²−y²</sub>, 3d<sub>z²</sub> (Day 5 p.20).</p>",
    source="Day 5 p.20")

add(id="m9-p3", module="m9", kind="practice", level="Standard",
    prompt="<p>Which orbital has its most probable distance farthest from the nucleus?</p>",
    answer=choice(("1s", False, "1s is the smallest."), ("2s", False, "2s is larger than 1s, but not the largest here."),
                  ("3s", True, "Right: orbital size increases with n (Day 5 p.18)."), ("They're all the same size.", False, "Day 5 p.18 shows them growing with n.")),
    hints=["Day 5 p.18: “Orbital size increases with increasing value of principal quantum number, n.”"],
    solution="<p><strong>3s</strong>. Size grows with n; the main 3s peak sits near 680 pm, compared with about 280 pm for 2s and 53 pm for 1s (Day 5 p.17–18).</p>",
    source="Day 5 p.17–18")

add(id="m9-p4", module="m9", kind="practice", level="Standard",
    prompt="<p>In the n = 3 radial plots (Day 6 p.18), which orbital has electron density that penetrates closest to the nucleus?</p>",
    answer=choice(("3s", True, "Right: its small inner peaks sit closest to the nucleus (the “Penetration” arrows)."),
                  ("3p", False, "3p penetrates too, but less than 3s."),
                  ("3d", False, "3d has one peak and doesn't penetrate the inner shells, even though that peak is the closest of the three main peaks."),
                  ("All penetrate equally.", False, "That's exactly why their energies differ (Day 6 p.18).")),
    hints=["Look for small inner peaks close to r = 0.", "Day 6 p.18 labels them “Penetration.”"],
    solution="<p><strong>3s</strong> penetrates most, then 3p, then 3d. That's why, in multi-electron atoms, 3s < 3p < 3d in energy (Day 6 p.18).</p>",
    source="Day 6 p.18")

add(id="m9-transfer", module="m9", kind="transfer", level="Transfer",
    prompt="<p>The zeros in an s orbital's radial distribution are called nodes (a textbook term). Following the pattern 1s (0 zeros), 2s (1), 3s (2), how many should a 4s orbital have?</p>",
    answer=num_ans(3, tol=0),
    hints=["List the pattern: n = 1 → 0 zeros, n = 2 → 1, n = 3 → 2.", "Each step up in n adds one zero for an s orbital, so the count is n − 1."],
    solution="<p><strong>3 nodes.</strong> <span class='preview'>Textbook preview: “The number of nodes in any s orbital is equal to n − 1” (textbook §3.7, PDF p.144, printed 110).</span></p>",
    source="Day 5 p.18")

add(id="m9-m-explain", module="m9", kind="mastery", level="Explain",
    prompt="<p>Why does the 1s radial distribution 4πr<sup>2</sup>ψ<sup>2</sup> start at zero at the nucleus even though ψ<sup>2</sup> is largest there?</p>",
    answer={"type": "self", "model": "<p>4πr<sup>2</sup>ψ<sup>2</sup> is the probability in a thin shell at radius r: density times the shell's area. At r = 0 the shell has zero area, so the probability is zero even though the density is highest. "
                                     "As r grows, the shells get bigger while the density falls, and the product peaks at 53 pm (Day 5 p.17).</p>"},
    hints=[], solution="", source="Day 5 p.17")

add(id="m9-m-recognize", module="m9", kind="mastery", level="Recognize",
    prompt="<p>An orbital has two lobes pointing in opposite directions along one axis. Which type is it?</p>",
    answer=choice(("s", False, "s orbitals are spheres."), ("p", True, "Right (Day 5 p.19)."), ("d", False, "Most d orbitals have four lobes (Day 5 p.20)."), ("f", False, "No f shapes were shown; they're more complex.")),
    hints=["Day 5 p.19 describes this shape."],
    solution="<p>A <strong>p</strong> orbital: two lobes along one Cartesian axis (Day 5 p.19).</p>",
    source="Day 5 p.19")

add(id="m9-m-sanity", module="m9", kind="mastery", level="Sanity check",
    prompt="<p>A classmate says “a 2p orbital holds 6 electrons.” What's the correction?</p>",
    answer=choice(("Correct as stated", False, "Any single orbital holds at most 2 electrons (Day 5 p.15)."),
                  ("Each 2p orbital holds 2; the 2p <em>subshell</em> (three orbitals) holds 6.", True, "Right: orbital ≠ subshell."),
                  ("A 2p orbital holds 3 electrons.", False, "An orbital holds at most 2 (Pauli)."),
                  ("2p orbitals hold 8 electrons.", False, "That's the whole n = 2 shell (2s + 2p).")),
    hints=["Orbital vs. subshell: which one does Pauli limit to two electrons?"],
    solution="<p>An <em>orbital</em> holds 2 electrons (Day 5 p.15). The 2p <em>subshell</em> has three orbitals, so it holds 6.</p>",
    source="Day 5 p.15, p.19")

# =====================================================================================
# m10 Electron configurations (Day 6 p.6–20; Day 7 p.6)
# =====================================================================================
add(id="m10-attempt", module="m10", kind="attempt", level="Guided attempt",
    prompt="<p>Write the ground-state electron configuration of sulfur (Z = 16), and give its number of unpaired electrons.</p>",
    answer={"type": "multi", "parts": [
        {"label": "configuration", **cfg_ans(16, 0, "S")},
        {"label": "unpaired electrons", **num_ans(unpaired(ion_config(16, 0)), tol=0)}]},
    hints=["Three rules: Pauli, Aufbau, Hund (Day 6 p.6).",
           "Fill in energy order: 1s, 2s, 2p, 3s, 3p … until all 16 electrons are placed.",
           "1s<sup>2</sup> 2s<sup>2</sup> 2p<sup>6</sup> 3s<sup>2</sup> uses 12 electrons, leaving 4 for 3p.",
           "Put the four 3p electrons in three boxes: one in each first (Hund), then pair the fourth."],
    solution="<p><strong>1s<sup>2</sup>2s<sup>2</sup>2p<sup>6</sup>3s<sup>2</sup>3p<sup>4</sup> = [Ne]3s<sup>2</sup>3p<sup>4</sup></strong>. In the 3p boxes, [↑↓][↑][↑] gives <strong>2 unpaired electrons</strong> (Hund's rule, Day 6 p.16).</p>",
    compare={
        "wrong": "<p>“3p<sup>4</sup> means [↑↓][↑↓][ ]: fill each box completely before moving on, so 0 unpaired.”</p>",
        "tempting": "Filling one box at a time looks tidy and mirrors how whole subshells fill.",
        "fails": "Electrons repel, so in degenerate orbitals the lowest-energy arrangement maximizes unpaired spins. “We will refrain from ‘pairing’ electrons until we HAVE to” (Day 6 p.16)."},
    source="Day 6 p.6–17")

add(id="m10-p1", module="m10", kind="practice", level="Standard",
    prompt="<p>Write the ground-state configuration of iron (Z = 26). You can use a noble-gas core, in either filling order or n order.</p>",
    answer=cfg_ans(26, 0, "Fe"),
    hints=["After [Ar] (18 electrons), 8 remain.", "4s fills before 3d (Day 6 p.19).", "4s holds 2; 6 go into 3d.", "[Ar]4s<sup>2</sup>3d<sup>?</sup>"],
    solution="<p><strong>[Ar]4s<sup>2</sup>3d<sup>6</sup></strong> (also written [Ar]3d<sup>6</sup>4s<sup>2</sup>; the lecture uses both orders, Day 6 p.21; Day 7 p.6).</p>",
    source="Day 6 p.19–21")

add(id="m10-p2", module="m10", kind="practice", level="Standard",
    prompt="<p>Phosphorus (Z = 15): write its configuration and give its number of unpaired electrons.</p>",
    answer={"type": "multi", "parts": [
        {"label": "configuration", **cfg_ans(15, 0, "P")},
        {"label": "unpaired electrons", **num_ans(unpaired(ion_config(15, 0)), tol=0)}]},
    hints=["[Ne] covers 10 electrons.", "5 remain: 3s<sup>2</sup> then 3p<sup>3</sup>.", "Three 3p electrons in three degenerate boxes …", "Hund: one per box."],
    solution="<p><strong>[Ne]3s<sup>2</sup>3p<sup>3</sup></strong>, with 3p as [↑][↑][↑]: <strong>3 unpaired</strong> (like nitrogen on Day 6 p.17).</p>",
    source="Day 6 p.16–17")

add(id="m10-p3", module="m10", kind="practice", level="Standard",
    prompt="<p>Why does lithium's third electron go into 2s rather than 2p?</p>",
    answer=choice(("2s is smaller, so its electron sits closer to the nucleus overall.", False, "The main 2s peak is actually <em>farther</em> out than 2p's (Day 6 p.12). The key is the small inner peak."),
                  ("2s penetrates closer to the nucleus (it's less shielded), so it's lower in energy.", True, "Right: Day 6 p.12–13."),
                  ("Hund's rule puts it there.", False, "Hund's rule applies within one set of degenerate orbitals."),
                  ("Pauli forbids 2p for lithium.", False, "Pauli limits each orbital to two electrons; it doesn't pick 2s over 2p.")),
    hints=["Look at the 2s vs. 2p radial distributions on Day 6 p.12. Which one has density close to the nucleus?"],
    solution="<p>2s has a small inner lobe that penetrates inside the 1s<sup>2</sup> core. That electron is less shielded and feels more of the nuclear charge (Coulombic attraction), so 2s is lower in energy than 2p (Day 6 p.12–13).</p>",
    source="Day 6 p.12–13")

add(id="m10-p4", module="m10", kind="practice", level="Standard",
    prompt="<p>Which element has the ground-state configuration [Ar]4s<sup>2</sup>3d<sup>3</sup>?</p>",
    answer=choice(("Ti (Z = 22)", False, "Ti is [Ar]4s²3d²."), ("V (Z = 23)", True, "Right: 18 + 2 + 3 = 23."),
                  ("Cr (Z = 24)", False, "Cr would be [Ar]4s²3d⁴ by the course's filling rules (the real atom is an exception, which the course ignores, Day 7 p.6)."), ("Sc (Z = 21)", False, "Sc is [Ar]4s²3d¹.")),
    hints=["Count the electrons: [Ar] = 18."],
    solution="<p>18 + 2 + 3 = 23 → <strong>vanadium</strong>, the Top Hat element of Day 6 p.23.</p>",
    source="Day 6 p.19, p.23")

add(id="m10-p5", module="m10", kind="practice", level="Warm-up",
    prompt="<p>A student draws nitrogen's 2p electrons as [↑↓][↑][ ]. Which rule is broken?</p>",
    answer=choice(("Pauli exclusion principle", False, "The paired electrons have opposite spins, so Pauli is satisfied."),
                  ("Aufbau principle", False, "The right orbitals are filled; the problem is how the electrons are spread."),
                  ("Hund's rule", True, "Right: electrons should occupy empty degenerate orbitals before pairing (Day 6 p.16)."),
                  ("No rule is broken.", False, "The lowest-energy arrangement is [↑][↑][↑] (Day 6 p.17).")),
    hints=["Degenerate orbitals: spread out, or pair up?"],
    solution="<p><strong>Hund's rule.</strong> Nitrogen's ground state is 2p: [↑][↑][↑] (Day 6 p.17).</p>",
    source="Day 6 p.16–17")

add(id="m10-transfer", module="m10", kind="transfer", level="Transfer",
    prompt="<p>An element's condensed configuration is [Ne]3s<sup>2</sup>3p<sup>5</sup>. Identify the element (symbol) and give its number of unpaired electrons.</p>",
    answer={"type": "multi", "parts": [
        {"label": "element symbol", **text_ans(["Cl", "chlorine"], ci=True, placeholder="symbol")},
        {"label": "unpaired electrons", **num_ans(1, tol=0)}]},
    hints=["Count electrons: [Ne] = 10.", "10 + 2 + 5 = ?", "Element 17 is …", "3p<sup>5</sup> = [↑↓][↑↓][↑]."],
    solution="<p>10 + 2 + 5 = 17 → <strong>Cl</strong>. 3p<sup>5</sup> = [↑↓][↑↓][↑] → <strong>1 unpaired electron</strong>. One electron short of [Ar], which is why Cl readily forms Cl<sup>−</sup> (Day 7 p.19).</p>",
    source="Day 6 p.16–17; Day 7 p.19")

add(id="m10-m-explain", module="m10", kind="mastery", level="Explain",
    prompt="<p>Explain, using penetration and shielding, why 2s is lower in energy than 2p in lithium.</p>",
    answer={"type": "self", "model": "<p>The 1s<sup>2</sup> core electrons sit between the nucleus and the n = 2 electrons and shield them, so an outer electron feels only part of the 3+ nuclear charge (Z<sub>eff</sub> ≈ 1+ for Li's 2s electron, Day 6 p.13). "
                                     "The 2s orbital has a small inner lobe that penetrates inside the core, so part of the time its electron feels much more nuclear charge; 2p has no such inner lobe. "
                                     "Greater attraction means lower energy, so 2s < 2p (Day 6 p.12–13).</p>"},
    hints=[], solution="", source="Day 6 p.12–13")

add(id="m10-m-recognize", module="m10", kind="mastery", level="Recognize",
    prompt="<p>An element's last electron (by Aufbau) enters a 3d orbital. In which block of the periodic table is it?</p>",
    answer=choice(("s block", False, "s-block elements end in an s electron."), ("p block", False, "p-block elements end in a p electron."),
                  ("d block (groups 3–12)", True, "Right: the colored-block periodic table on Day 6 p.20."), ("f block", False, "f-block elements end in an f electron.")),
    hints=["Day 6 p.20 colors the periodic table by the subshell being filled."],
    solution="<p>The <strong>d block</strong>, groups 3–12. The periodic table's blocks follow the filling order (Day 6 p.20).</p>",
    source="Day 6 p.20")

add(id="m10-m-sanity", module="m10", kind="mastery", level="Sanity check",
    prompt="<p>A classmate writes calcium (Z = 20) as [Ar]3d<sup>2</sup>. What's wrong?</p>",
    answer=choice(("Nothing", False, "4s fills before 3d."),
                  ("4s is lower in energy than 3d, so Ca is [Ar]4s<sup>2</sup>.", True, "Right: “even 4s is lower in energy than 3d!” (Day 6 p.19)."),
                  ("Calcium has only 18 electrons.", False, "Z = 20 means 20 electrons."),
                  ("It should be [Ar]4p<sup>2</sup>.", False, "4p comes after 3d in the filling order (Day 6 p.19).")),
    hints=["Check the energy ladder on Day 6 p.19."],
    solution="<p>Ca = <strong>[Ar]4s<sup>2</sup></strong>. 4s fills before 3d (Day 6 p.19).</p>",
    source="Day 6 p.19")

# =====================================================================================
# m11 Configurations of ions (Day 6 p.21–23)
# =====================================================================================
add(id="m11-attempt", module="m11", kind="attempt", level="Guided attempt",
    prompt="<p>Write the configuration of Fe<sup>3+</sup> and give its number of 3d electrons.</p>",
    answer={"type": "multi", "parts": [
        {"label": "configuration", **cfg_ans(26, 3, "Fe<sup>3+</sup>")},
        {"label": "3d electrons", **num_ans(5, tol=0)}]},
    hints=["Cations lose electrons from the highest n first (Day 6 p.21).",
           "Fe = [Ar]4s<sup>2</sup>3d<sup>6</sup>.",
           "Remove 3 electrons: both 4s electrons first (n = 4), then one 3d.",
           "[Ar]3d<sup>?</sup>"],
    solution="<p>Fe [Ar]4s<sup>2</sup>3d<sup>6</sup> → remove 4s<sup>2</sup>, then one 3d → <strong>Fe<sup>3+</sup> = [Ar]3d<sup>5</sup></strong>: <strong>5 3d electrons</strong>.</p>",
    compare={
        "wrong": "<p>“3d filled last, so remove 3d first: Fe<sup>3+</sup> = [Ar]4s<sup>2</sup>3d<sup>3</sup>.”</p>",
        "tempting": "“Last in, first out” feels logical.",
        "fails": "The lecture rule removes electrons from the highest n “<strong>regardless of the order in which they were added</strong>” (Day 6 p.21). 4s (n = 4) goes before 3d (n = 3), exactly as in Ni → Ni<sup>2+</sup>."},
    source="Day 6 p.21")

add(id="m11-p1", module="m11", kind="practice", level="Standard",
    prompt="<p>Write the configuration of Co<sup>2+</sup> (Co: Z = 27).</p>",
    answer=cfg_ans(27, 2, "Co<sup>2+</sup>"),
    hints=["Co = [Ar]4s<sup>2</sup>3d<sup>7</sup>.", "Remove the two highest-n electrons first."],
    solution="<p>Co [Ar]4s<sup>2</sup>3d<sup>7</sup> → <strong>Co<sup>2+</sup> = [Ar]3d<sup>7</sup></strong>.</p>",
    source="Day 6 p.21")

add(id="m11-p2", module="m11", kind="practice", level="Warm-up",
    prompt="<p>Write the configuration of S<sup>2−</sup> (S: Z = 16).</p>",
    answer=cfg_ans(16, -2, "S<sup>2−</sup>"),
    hints=["Anions add electrons following Aufbau, Pauli, and Hund (Day 6 p.21).", "S = [Ne]3s<sup>2</sup>3p<sup>4</sup>; add 2 electrons."],
    solution="<p>[Ne]3s<sup>2</sup>3p<sup>4</sup> + 2e<sup>−</sup> → <strong>[Ne]3s<sup>2</sup>3p<sup>6</sup> = [Ar]</strong>, the same configuration as argon.</p>",
    source="Day 6 p.21")

add(id="m11-p3", module="m11", kind="practice", level="Standard",
    prompt="<p>How many 3d electrons does Mn<sup>2+</sup> have (Mn: Z = 25)?</p>",
    answer=num_ans(5, tol=0),
    hints=["Mn = [Ar]4s<sup>2</sup>3d<sup>5</sup>.", "Remove the two 4s electrons first."],
    solution="<p>Mn [Ar]4s<sup>2</sup>3d<sup>5</sup> → Mn<sup>2+</sup> [Ar]3d<sup>5</sup> → <strong>5</strong> (same method as the V<sup>3+</sup> Top Hat, Day 6 p.23).</p>",
    source="Day 6 p.21–23")

add(id="m11-p4", module="m11", kind="practice", level="Standard",
    prompt="<p>Which ion is <strong>not</strong> isoelectronic with neon (10 electrons)?</p>",
    answer=choice(("Na<sup>+</sup>", False, "11 − 1 = 10 electrons."), ("O<sup>2−</sup>", False, "8 + 2 = 10 electrons."),
                  ("K<sup>+</sup>", True, "Right: 19 − 1 = 18 electrons, isoelectronic with argon."), ("Mg<sup>2+</sup>", False, "12 − 2 = 10 electrons.")),
    hints=["Electrons in an ion = Z − charge."],
    solution="<p><strong>K<sup>+</sup></strong> has 18 electrons ([Ar]). The others all have 10 ([Ne]).</p>",
    source="Day 6 p.21; Day 7 p.19")

add(id="m11-transfer", module="m11", kind="transfer", level="Transfer",
    prompt="<p>How many unpaired electrons does Ti<sup>2+</sup> have (Ti: Z = 22)?</p>",
    answer=num_ans(unpaired(ion_config(22, 2)), tol=0),
    hints=["First the configuration: Ti = [Ar]4s<sup>2</sup>3d<sup>2</sup>.", "Ti<sup>2+</sup> loses both 4s electrons.", "Two electrons in five degenerate 3d orbitals …", "Hund: one per orbital."],
    solution="<p>Ti<sup>2+</sup> = [Ar]3d<sup>2</sup>; the two 3d electrons occupy separate orbitals with parallel spins → <strong>2 unpaired</strong>.</p>",
    source="Day 6 p.16, p.21")

add(id="m11-m-explain", module="m11", kind="mastery", level="Explain",
    prompt="<p>Explain the cation rule using Ni → Ni<sup>2+</sup> (Day 6 p.21).</p>",
    answer={"type": "self", "model": "<p>Ni is [Ar]4s<sup>2</sup>3d<sup>8</sup>: 4s filled before 3d. Forming a cation removes electrons from the highest principal quantum number first, “regardless of the order in which they were added,” so the two 4s (n = 4) electrons leave and Ni<sup>2+</sup> = [Ar]3d<sup>8</sup>. "
                                     "<span class='bg'>The textbook's reason is that as 3d fills, the 3d electrons feel a larger Z<sub>eff</sub> than the 4s electrons, so 4s ends up higher in energy and ionizes first (textbook §3.9, PDF p.154–155, printed 120–121).</span></p>"},
    hints=[], solution="", source="Day 6 p.21")

add(id="m11-m-recognize", module="m11", kind="mastery", level="Recognize",
    prompt="<p>Which of these needs the “remove the highest n first” rule?</p>",
    answer=choice(("The configuration of F<sup>−</sup>", False, "Anions add electrons by Aufbau."),
                  ("The configuration of Zn<sup>2+</sup>", True, "Right: a transition-metal cation (4s leaves before 3d)."),
                  ("The configuration of a neutral Ne atom", False, "Neutral atoms use Aufbau."),
                  ("The configuration of S", False, "Neutral atoms use Aufbau.")),
    hints=["Which one is a cation formed from an atom that has both 4s and 3d electrons?"],
    solution="<p><strong>Zn<sup>2+</sup></strong>: Zn [Ar]4s<sup>2</sup>3d<sup>10</sup> → Zn<sup>2+</sup> [Ar]3d<sup>10</sup>.</p>",
    source="Day 6 p.21")

add(id="m11-m-sanity", module="m11", kind="mastery", level="Sanity check",
    prompt="<p>A student writes Zn<sup>2+</sup> as [Ar]4s<sup>2</sup>3d<sup>8</sup>. What's the correction?</p>",
    answer=choice(("It's correct.", False, "The 4s electrons (highest n) must leave first."),
                  ("[Ar]3d<sup>10</sup>: the two 4s electrons leave first.", True, "Right: Day 6 p.21's rule."),
                  ("[Ar]4s<sup>1</sup>3d<sup>9</sup>", False, "Both electrons come from 4s."),
                  ("[Kr]", False, "Zn<sup>2+</sup> has 28 electrons, not 36.")),
    hints=["Which electrons have the highest n in zinc?"],
    solution="<p>Zn<sup>2+</sup> = <strong>[Ar]3d<sup>10</sup></strong>.</p>",
    source="Day 6 p.21")

# =====================================================================================
# m12 Periodic trends: atomic & ionic size (Day 6 p.24–26; Day 7 p.7–8)
# =====================================================================================
add(id="m12-attempt", module="m12", kind="attempt", level="Guided attempt",
    prompt="<p>Rank from <strong>largest</strong> (1) to <strong>smallest</strong> (4) atomic radius: Na, Mg, K, Cl.</p>",
    answer=order_ans([("Na", "Na"), ("Mg", "Mg"), ("K", "K"), ("Cl", "Cl")], ["K", "Na", "Mg", "Cl"], "largest (1) to smallest (4)"),
    hints=["Size trend: down a group, bigger; across a period, smaller (Day 6 p.24 figure).",
           "K is directly below Na in group 1; Na, Mg, and Cl are all in period 3.",
           "Across period 3 the radius falls: Na > Mg > … > Cl.",
           "K has an extra shell (n = 4), so it is the largest."],
    solution="<p><strong>K (227 pm) > Na (186) > Mg (160) > Cl (99)</strong>, using the values from Day 6 p.24.</p>",
    compare={
        "wrong": "<p>“Cl has the most electrons of the period-3 atoms, so it's the biggest: Cl > Mg > Na > K.”</p>",
        "tempting": "More electrons sounds like more stuff, so a bigger atom.",
        "fails": "Across a period, electrons go into the same shell while the nuclear charge increases. Z<sub>eff</sub> rises and pulls the shell in (Ch. 3 outcome 7, Day 7 p.5). The data confirm it: Na 186 pm → Cl 99 pm."},
    source="Day 6 p.24; Day 7 p.5")

add(id="m12-p1", module="m12", kind="practice", level="Warm-up",
    prompt="<p>Rank from largest (1) to smallest (4): Be, Mg, Ca, Ba.</p>",
    answer=order_ans([("Be", "Be"), ("Mg", "Mg"), ("Ca", "Ca"), ("Ba", "Ba")], ["Ba", "Ca", "Mg", "Be"], "largest (1) to smallest (4)"),
    hints=["All four are in group 2.", "Down a group, n increases, so the atoms get bigger."],
    solution="<p><strong>Ba (222) > Ca (197) > Mg (160) > Be (112)</strong> pm (Day 6 p.24).</p>",
    source="Day 6 p.24")

add(id="m12-p2", module="m12", kind="practice", level="Warm-up",
    prompt="<p>Which is larger: a Cl atom or a Cl<sup>−</sup> ion?</p>",
    answer=choice(("Cl atom", False, "Adding an electron increases electron–electron repulsion, and the particle expands."),
                  ("Cl<sup>−</sup> ion", True, "Right: 181 pm vs. 99 pm (Day 7 p.8)."),
                  ("Same size", False, "Day 7 p.8 shows them very different."),
                  ("Can't tell", False, "Day 7 p.8 gives both values.")),
    hints=["Compare the atom and ion pairs on Day 7 p.8."],
    solution="<p><strong>Cl<sup>−</sup></strong> (181 pm) is much larger than Cl (99 pm). Anions are larger than their atoms (Day 7 p.8).</p>",
    source="Day 7 p.8")

add(id="m12-p3", module="m12", kind="practice", level="Standard",
    prompt="<p>These four ions all have 18 electrons. Rank them from largest (1) to smallest (4): S<sup>2−</sup>, Cl<sup>−</sup>, K<sup>+</sup>, Ca<sup>2+</sup>.</p>",
    answer=order_ans([("S2-", "S<sup>2−</sup>"), ("Cl-", "Cl<sup>−</sup>"), ("K+", "K<sup>+</sup>"), ("Ca2+", "Ca<sup>2+</sup>")],
                     ["S2-", "Cl-", "K+", "Ca2+"], "largest (1) to smallest (4)"),
    hints=["Same number of electrons (isoelectronic); what differs is the number of protons.", "More protons pull the same 18 electrons in more tightly."],
    solution="<p><strong>S<sup>2−</sup> (184) > Cl<sup>−</sup> (181) > K<sup>+</sup> (138) > Ca<sup>2+</sup> (100)</strong> pm (Day 7 p.8): Z = 16, 17, 19, 20 pulling on the same 18 electrons.</p>",
    source="Day 7 p.8")

add(id="m12-p4", module="m12", kind="practice", level="Standard",
    prompt="<p>Why is Li<sup>+</sup> (76 pm) so much smaller than Li (152 pm)?</p>",
    answer=choice(("Li<sup>+</sup> has more protons.", False, "Same nucleus: 3 protons."),
                  ("Li<sup>+</sup> lost its only n = 2 electron; the remaining 1s<sup>2</sup> electrons sit much closer to the nucleus.", True, "Right: a whole shell is gone."),
                  ("Positive ions always double in size.", False, "They shrink."),
                  ("The measurement is wrong.", False, "Day 7 p.8 (textbook Fig. 3.36) reports these values.")),
    hints=["Li = 1s<sup>2</sup>2s<sup>1</sup>. What's left after it loses one electron?"],
    solution="<p>Li → Li<sup>+</sup> removes the 2s electron, the entire n = 2 shell. What remains is the compact 1s<sup>2</sup> core.</p>",
    source="Day 6 p.14; Day 7 p.8")

add(id="m12-transfer", module="m12", kind="transfer", level="Transfer",
    prompt="<p>Se<sup>2−</sup>, Br<sup>−</sup>, Rb<sup>+</sup>, and Sr<sup>2+</sup> all have 36 electrons. Rank them from largest (1) to smallest (4). (Only two of these values appear in the lecture; reason from the trend.)</p>",
    answer=order_ans([("Se2-", "Se<sup>2−</sup>"), ("Br-", "Br<sup>−</sup>"), ("Rb+", "Rb<sup>+</sup>"), ("Sr2+", "Sr<sup>2+</sup>")],
                     ["Se2-", "Br-", "Rb+", "Sr2+"], "largest (1) to smallest (4)"),
    hints=["Isoelectronic series: fewer protons means a larger ion.", "Z: Se 34, Br 35, Rb 37, Sr 38."],
    solution="<p><strong>Se<sup>2−</sup> > Br<sup>−</sup> > Rb<sup>+</sup> > Sr<sup>2+</sup></strong>. The lecture gives Se<sup>2−</sup> 198 pm and Br<sup>−</sup> 195 pm (Day 7 p.8); the cations follow from the same logic as the 18-electron series.</p>",
    source="Day 7 p.8")

add(id="m12-m-explain", module="m12", kind="mastery", level="Explain",
    prompt="<p>Why do atoms get smaller across a period even though they gain electrons?</p>",
    answer={"type": "self", "model": "<p>Across a period, each added electron goes into the same valence shell (same n), so it doesn't add much distance, while each added proton increases the nuclear charge. "
                                     "The inner (core) electrons stay the same, so the effective nuclear charge Z<sub>eff</sub> on the valence electrons rises and pulls them closer. "
                                     "Radius falls, from Li 152 pm to Ne 69 pm (Day 6 p.24; outcome 7, Day 7 p.5).</p>"},
    hints=[], solution="", source="Day 6 p.24; Day 7 p.5")

add(id="m12-m-recognize", module="m12", kind="mastery", level="Recognize",
    prompt="<p>Which comparison is settled by “same electrons, more protons → smaller”?</p>",
    answer=choice(("Na vs. K", False, "Different numbers of electrons and shells: that's the down-a-group trend."),
                  ("Na<sup>+</sup> vs. F<sup>−</sup>", True, "Right: both have 10 electrons (isoelectronic)."),
                  ("Cl vs. Cl<sup>−</sup>", False, "Same nucleus, different electron count: that's the atom-vs-anion comparison."),
                  ("Li vs. Ne", False, "That's the across-a-period trend.")),
    hints=["Which pair has the same number of electrons?"],
    solution="<p><strong>Na<sup>+</sup> vs. F<sup>−</sup></strong>: both have 10 electrons, and Na<sup>+</sup> has more protons, so it's smaller (102 vs. 133 pm, Day 7 p.8).</p>",
    source="Day 7 p.8")

add(id="m12-m-sanity", module="m12", kind="mastery", level="Sanity check",
    prompt="<p>A table claims cesium atoms are smaller than lithium atoms. Plausible?</p>",
    answer=choice(("Yes; Cs has a higher Z, so it pulls harder.", False, "Down a group, the added shells win: radius increases."),
                  ("No; radius increases down a group (Cs 265 pm vs. Li 152 pm).", True, "Right (Day 6 p.24)."),
                  ("Yes; metals shrink down a group.", False, "They grow."),
                  ("Can't compare atoms in the same group.", False, "The same-group comparison is the clearest trend.")),
    hints=["Where are Li and Cs relative to each other?"],
    solution="<p>Not plausible: Cs (265 pm) is much larger than Li (152 pm). Each period down adds a shell (Day 6 p.24).</p>",
    source="Day 6 p.24")

# =====================================================================================
# m13 IE & EA (Day 7 p.9–11)
# =====================================================================================
add(id="m13-attempt", module="m13", kind="attempt", level="Guided attempt",
    prompt="<p>An unknown period-3 element has IE<sub>1</sub> = 578, IE<sub>2</sub> = 1817, IE<sub>3</sub> = 2745, and IE<sub>4</sub> = 11,577 kJ/mol. "
           "(a) How many valence electrons does it have? (b) Identify the element (symbol).</p>",
    answer={"type": "multi", "parts": [
        {"label": "(a) valence electrons", **num_ans(3, tol=0)},
        {"label": "(b) element", **text_ans(["Al", "aluminum", "aluminium"], ci=True, placeholder="symbol")}]},
    hints=["Successive ionization energies: look for the big jump (Day 7 p.10).",
           "The jump comes when you start removing core electrons.",
           "Ratios: 1817/578 ≈ 3.1; 2745/1817 ≈ 1.5; 11,577/2745 ≈ 4.2. The biggest jump is after IE<sub>3</sub>.",
           "3 valence electrons in period 3 → group 13."],
    solution="<p>The big jump is between IE<sub>3</sub> and IE<sub>4</sub>, so <strong>3 valence electrons</strong>. Period 3 + group 13 = <strong>Al</strong> (IE<sub>1</sub> = 578 kJ/mol on Day 7 p.9). "
             "IE<sub>4</sub> removes a 2p core electron, which is far more tightly held.</p>"
             "<p class='bg'>IE<sub>2</sub>–IE<sub>4</sub> are reference values (Wolfram Alpha: 1816.7, 2744.8, 11,577 kJ/mol). Only IE<sub>1</sub> appears on the slides.</p>",
    compare={
        "wrong": "<p>“IE<sub>4</sub> is the huge one, so there are 4 valence electrons: group 14, Si.”</p>",
        "tempting": "The standout number is the fourth.",
        "fails": "IE<sub>4</sub> is huge <em>because</em> the fourth electron is a core electron. The number of valence electrons equals the number removed <em>before</em> the jump: 3 (the red staircase on Day 7 p.10 marks the same boundary)."},
    source="Day 7 p.9–10")

add(id="m13-p1", module="m13", kind="practice", level="Warm-up",
    prompt="<p>Which has the highest first ionization energy?</p>",
    answer=choice(("Na", False, "496 kJ/mol: lowest in period 3."), ("Mg", False, "738 kJ/mol."), ("Al", False, "578 kJ/mol."),
                  ("Cl", True, "Right: 1251 kJ/mol (Day 7 p.9); IE₁ rises across a period.")),
    hints=["IE<sub>1</sub> generally increases across a period (the “Increasing IE₁” arrow, Day 7 p.9)."],
    solution="<p><strong>Cl</strong> (1251 kJ/mol). Across period 3, Z<sub>eff</sub> rises and the valence electrons are held more tightly (Day 7 p.9).</p>",
    source="Day 7 p.9")

add(id="m13-p2", module="m13", kind="practice", level="Standard",
    prompt="<p>Why is oxygen's IE<sub>1</sub> (1314 kJ/mol) lower than nitrogen's (1402 kJ/mol), against the general trend?</p>",
    answer=choice(("Oxygen has fewer protons than nitrogen.", False, "O has 8; N has 7."),
                  ("The electron O loses is paired in a 2p orbital, and repulsion between the pair makes it easier to remove.", True, "Right: the O → O⁺ orbital diagram on Day 7 p.9 shows exactly that electron."),
                  ("Oxygen's electron comes from 2s.", False, "It comes from 2p (Day 7 p.9)."),
                  ("Nitrogen is a noble gas.", False, "Nitrogen is in group 15.")),
    hints=["Look at the O → O<sup>+</sup> orbital boxes on Day 7 p.9: which electron leaves?"],
    solution="<p>In O (2p: [↑↓][↑][↑]) the electron removed is one of a pair. Repulsion between paired electrons raises its energy, so it's easier to remove, and O<sup>+</sup> is left with a half-filled 2p<sup>3</sup> (Day 7 p.9). "
             "<span class='bg'>Textbook §3.11, PDF p.160, printed 126.</span></p>",
    source="Day 7 p.9")

add(id="m13-p3", module="m13", kind="practice", level="Standard",
    prompt="<p>Using Table 3.2 (Day 7 p.10), carbon's biggest jump comes between IE<sub>n</sub> and IE<sub>n+1</sub>. What is n?</p>",
    answer=num_ans(4, tol=0),
    hints=["Carbon's values: 1086, 2348, 4617, 6201, 37,926, 46,956 kJ/mol.", "Find the largest ratio between neighbors."],
    solution="<p>6201 → 37,926 (×6.1) is the jump, so <strong>n = 4</strong>: carbon has 4 valence electrons (2s<sup>2</sup>2p<sup>2</sup>), and IE<sub>5</sub> removes a 1s core electron.</p>",
    source="Day 7 p.10")

add(id="m13-p4", module="m13", kind="practice", level="Warm-up",
    prompt="<p>The first electron affinity of Cl is −349 kJ/mol. What does the negative sign mean?</p>",
    answer=choice(("Energy is released when a gaseous Cl atom gains an electron.", True, "Right: the anion is lower in energy (Day 7 p.11 convention)."),
                  ("Energy must be supplied to add the electron.", False, "That's a positive EA, like N's +7."),
                  ("Cl loses an electron.", False, "EA is about <em>gaining</em> an electron: M(g) + e⁻ → M⁻(g)."),
                  ("The value is a typo.", False, "Most EA values are negative (Day 7 p.11).")),
    hints=["EA<sub>1</sub> is the energy change for M(g) + e<sup>−</sup> → M<sup>−</sup>(g) (Day 7 p.11)."],
    solution="<p>Negative = <strong>energy released</strong>: Cl(g) + e<sup>−</sup> → Cl<sup>−</sup>(g) gives off 349 kJ per mole.</p>",
    source="Day 7 p.11")

add(id="m13-p5", module="m13", kind="practice", level="Standard",
    prompt="<p>According to the Day 7 p.11 table, which element has a <strong>positive</strong> EA<sub>1</sub>?</p>",
    answer=choice(("C", False, "−122 kJ/mol."), ("N", True, "Right: +7 kJ/mol, circled in red on Day 7 p.11."), ("O", False, "−141 kJ/mol."), ("F", False, "−328 kJ/mol.")),
    hints=["One value in period 2 is circled on the slide."],
    solution="<p><strong>N</strong> (+7 kJ/mol). <span class='bg'>Adding an electron would cost nitrogen the stability of its half-filled 2p subshell (textbook §3.12, PDF p.164, printed 130).</span></p>",
    source="Day 7 p.11")

ieH = BOHR * NA / 1000
add(id="m13-p6", module="m13", kind="practice", level="Standard",
    prompt="<p><span class='tag-preview'>Uses N<sub>A</sub> = 6.022 × 10<sup>23</sup> mol<sup>−1</sup>: textbook preview, §2.5</span> Use the Bohr model to calculate hydrogen's first ionization energy in kJ/mol, then compare it with the Day 7 p.9 value.</p>",
    answer=num_ans(ieH, sf=4, unit_label="kJ/mol", units=KJMOL_UNITS),
    hints=["Ionization from the ground state: n<sub>initial</sub> = 1 → n<sub>final</sub> = ∞ (Day 4 p.10).",
           "ΔE = −2.178 × 10<sup>−18</sup> J (0 − 1) = +2.178 × 10<sup>−18</sup> J per atom.",
           "Multiply by N<sub>A</sub> = 6.022 × 10<sup>23</sup> mol<sup>−1</sup>.",
           "Divide by 1000 for kJ."],
    solution=f"<p>2.178 × 10<sup>−18</sup> J × 6.022 × 10<sup>23</sup> mol<sup>−1</sup> = {sci(BOHR * NA, 4)} J/mol = <strong>{num(ieH, 4)} kJ/mol</strong>, matching the 1312 on Day 7 p.9. The Bohr model and the ionization data agree for hydrogen.</p>",
    source="Day 4 p.10; Day 7 p.9")

E_Na = 496e3 / NA
lam_Na = nm_from_energy(E_Na)
add(id="m13-transfer", module="m13", kind="transfer", level="Transfer",
    prompt="<p><span class='tag-preview'>Uses N<sub>A</sub> = 6.022 × 10<sup>23</sup> mol<sup>−1</sup>: textbook preview, §2.5</span> What is the longest wavelength of light (nm) that could ionize a gaseous sodium atom (IE<sub>1</sub> = 496 kJ/mol) with a single photon, M(g) + hν → M<sup>+</sup>(g) + e<sup>−</sup>?</p>",
    answer=num_ans(lam_Na, sf=3, unit_label="nm", units=NM_UNITS),
    hints=["The photon must carry at least the ionization energy of one atom.",
           "Energy per atom = (496 × 10<sup>3</sup> J/mol) ÷ (6.022 × 10<sup>23</sup> mol<sup>−1</sup>).",
           "Then λ = hc/E.",
           "Convert m → nm."],
    solution=f"<p>E per atom = 496 × 10<sup>3</sup> ÷ 6.022 × 10<sup>23</sup> = {sci(E_Na)} J; λ = hc/E = {sci(lam_Na * 1e-9)} m = <strong>{num(lam_Na, 3)} nm</strong>, in the ultraviolet. "
             "The professor's IE equation (Day 7 p.9) makes this link to photon energy (Day 2 p.30).</p>",
    source="Day 7 p.9; Day 2 p.30")

add(id="m13-m-explain", module="m13", kind="mastery", level="Explain",
    prompt="<p>Explain the IE<sub>1</sub> trends across a period and down a group in terms of Z<sub>eff</sub> and distance.</p>",
    answer={"type": "self", "model": "<p>Across a period, Z<sub>eff</sub> on the valence electrons increases and the atoms shrink, so the outermost electron is held more tightly: IE<sub>1</sub> rises (Li 520 → Ne 2081 kJ/mol). "
                                     "Down a group, the valence electron is in a higher-n shell, farther out and shielded by more core electrons, so it's easier to remove: IE<sub>1</sub> falls (Li 520 → Cs 376). "
                                     "Exceptions such as Be > B and N > O come from subshell and pairing effects (Day 7 p.9).</p>"},
    hints=[], solution="", source="Day 7 p.5, p.9")

add(id="m13-m-recognize", module="m13", kind="mastery", level="Recognize",
    prompt="<p>A problem gives IE<sub>1</sub> through IE<sub>5</sub> for an unknown element and asks for its group. What should you look for first?</p>",
    answer=choice(("The largest single IE value", False, "Every IE is bigger than the one before; you need the <em>jump</em>, not the biggest number."),
                  ("The largest ratio between successive IEs", True, "Right: the jump marks where core electrons begin (Day 7 p.10)."),
                  ("The smallest IE value", False, "IE₁ alone doesn't give the group."),
                  ("The average of all the IEs", False, "Not meaningful here.")),
    hints=["What does the red staircase on Day 7 p.10 separate?"],
    solution="<p>Find the <strong>biggest jump</strong> between neighbors. The number of electrons removed before the jump is the number of valence electrons.</p>",
    source="Day 7 p.10")

add(id="m13-m-sanity", module="m13", kind="mastery", level="Sanity check",
    prompt="<p>A student says “fluorine has the most negative electron affinity of all the elements.” Check against Day 7 p.11.</p>",
    answer=choice(("Correct: F −328 is the most negative.", False, "Cl is −349 kJ/mol, even more negative."),
                  ("Not quite: Cl (−349 kJ/mol) is more negative than F (−328).", True, "Right: from the table on Day 7 p.11."),
                  ("Noble gases have the most negative EAs.", False, "Their (calculated) values are positive."),
                  ("All EAs are positive.", False, "Most are negative.")),
    hints=["Compare F and Cl in the Day 7 p.11 table."],
    solution="<p>Per the table, <strong>Cl (−349)</strong> is more negative than F (−328 kJ/mol).</p>",
    source="Day 7 p.11")

# =====================================================================================
# m14 Bonds, Coulomb energy & lattices (Day 7 p.12–17)
# =====================================================================================
d_nacl = (102 + 181) / 1000
E_nacl = e_el(1, -1, d_nacl)
add(id="m14-attempt", module="m14", kind="attempt", level="Guided attempt",
    prompt="<p>Calculate E<sub>el</sub> for one Na<sup>+</sup>–Cl<sup>−</sup> ion pair with the ions touching: d = 102 pm + 181 pm (the ionic radii on Day 7 p.8).</p>",
    answer=num_ans(E_nacl, sf=3, unit_label="J", units=J_UNITS, ask_unit=True),
    hints=["Ion–ion attraction → E<sub>el</sub> = 2.31 × 10<sup>−19</sup> J·nm (Q<sub>1</sub>Q<sub>2</sub>/d) (Day 7 p.15).",
           "Q<sub>1</sub> = +1, Q<sub>2</sub> = −1; d must be in nm.",
           "d = 102 pm + 181 pm = 283 pm = 0.283 nm.",
           "E<sub>el</sub> = (2.31 × 10<sup>−19</sup> J·nm)(+1)(−1) ÷ (0.283 nm)."],
    solution=f"<p>E<sub>el</sub> = (2.31 × 10<sup>−19</sup> J·nm)(+1)(−1) ÷ (0.283 nm) = <strong>{sci(E_nacl)} J</strong> per ion pair. "
             "It's negative because opposite charges attract, so the pair is lower in energy than separated ions (Day 7 p.15). nm ÷ nm cancels, leaving J.</p>",
    compare={
        "wrong": f"<p>“E<sub>el</sub> = 2.31 × 10<sup>−19</sup> × (+1)(−1) ÷ 283 = {sci(e_el(1, -1, 283))} J”, or the same number reported as positive.</p>",
        "tempting": "Radii are given in pm, and the minus sign is easy to drop.",
        "fails": "The constant's units are J·<strong>nm</strong>, so d must be in nm (0.283 nm), or the answer is 1000× too small. And Q<sub>1</sub>Q<sub>2</sub> = −1: a positive E<sub>el</sub> would mean repulsion."},
    source="Day 7 p.8, p.15")

E_mgo = e_el(2, -2, (72 + 140) / 1000)
add(id="m14-p1", module="m14", kind="practice", level="Standard",
    prompt="<p>Calculate E<sub>el</sub> for one Mg<sup>2+</sup>–O<sup>2−</sup> pair with d = 72 pm + 140 pm.</p>",
    answer=num_ans(E_mgo, sf=3, unit_label="J", units=J_UNITS),
    hints=["Same equation; now Q<sub>1</sub> = +2 and Q<sub>2</sub> = −2.", "d = 212 pm = 0.212 nm.", "Q<sub>1</sub>Q<sub>2</sub> = −4.", "E<sub>el</sub> = 2.31 × 10<sup>−19</sup> × (−4) ÷ 0.212 J."],
    solution=f"<p>E<sub>el</sub> = 2.31 × 10<sup>−19</sup> J·nm × (−4) ÷ 0.212 nm = <strong>{sci(E_mgo)} J</strong>, about 5 times NaCl's value: 4× from the charges, and a bit more from the smaller d.</p>",
    source="Day 7 p.8, p.15")

add(id="m14-p2", module="m14", kind="practice", level="Standard",
    prompt="<p>Rank these ion pairs by strength of attraction (most negative E<sub>el</sub> = 1): MgO (d = 0.212 nm), NaF (d = 0.235 nm), KCl (d = 0.319 nm).</p>",
    answer=order_ans([("MgO", "MgO"), ("NaF", "NaF"), ("KCl", "KCl")], ["MgO", "NaF", "KCl"], "strongest (1) to weakest (3)"),
    hints=["Charges first: Q<sub>1</sub>Q<sub>2</sub> = −4 for MgO, −1 for the others.", "Then distance: a smaller d gives a stronger attraction."],
    solution=f"<p><strong>MgO > NaF > KCl</strong>: {sci(e_el(2, -2, 0.212))}, {sci(e_el(1, -1, 0.235))}, {sci(e_el(1, -1, 0.319))} J. The lattice energies follow the same order: −3791, −930, −720 kJ/mol (Day 7 p.17).</p>",
    source="Day 7 p.15, p.17")

E_kcl = e_el(1, -1, 0.319)
kcl_mol = E_kcl * NA / 1000
add(id="m14-p3", module="m14", kind="practice", level="Stretch",
    prompt="<p><span class='tag-preview'>Uses N<sub>A</sub> = 6.022 × 10<sup>23</sup> mol<sup>−1</sup>: textbook preview, §2.5</span> For KCl (d = 0.319 nm), calculate E<sub>el</sub> per <em>mole</em> of ion pairs in kJ/mol, and compare it with KCl's lattice energy (−720 kJ/mol, Day 7 p.17).</p>",
    answer=num_ans(kcl_mol, sf=3, unit_label="kJ/mol", units=KJMOL_UNITS),
    hints=["First E<sub>el</sub> for one pair, then scale to a mole.", "E<sub>el</sub> = 2.31 × 10<sup>−19</sup> × (−1) ÷ 0.319 J.", "Multiply by 6.022 × 10<sup>23</sup> mol<sup>−1</sup>.", "Divide by 1000."],
    solution=f"<p>E<sub>el</sub> = {sci(E_kcl)} J per pair × 6.022 × 10<sup>23</sup> = <strong>{num(kcl_mol, 3)} kJ/mol</strong>. The real lattice energy, −720 kJ/mol, is about {fix(-720 / kcl_mol, 2)} times more negative: "
             "“The ionic lattices are even more stable than we might expect from our two-body equation” (Day 7 p.17). The textbook does this same calculation (§4.1, PDF p.183, printed 149).</p>"
             "<p class='note'>The number happens to match the H–H bond energy on Day 8 p.11 (436 kJ/mol): a coincidence between two different quantities, an ion pair's attraction and a covalent bond.</p>",
    source="Day 7 p.15–17")

add(id="m14-p4", module="m14", kind="practice", level="Warm-up",
    prompt="<p>Classify each substance's bonding using the Day 7 p.14 definitions.</p>",
    answer={"type": "match",
            "rows": [{"html": "CaCl<sub>2</sub>", "answer": "ionic"}, {"html": "CO<sub>2</sub>", "answer": "covalent"},
                     {"html": "Fe (solid)", "answer": "metallic"}, {"html": "KBr", "answer": "ionic"},
                     {"html": "H<sub>2</sub>O", "answer": "covalent"}],
            "options": [{"key": "ionic", "html": "ionic"}, {"key": "covalent", "html": "covalent"}, {"key": "metallic", "html": "metallic"}]},
    hints=["Metal + nonmetal → oppositely charged ions → ionic. Nonmetals only → covalent. Metal atoms only → metallic (Day 7 p.14)."],
    solution="<p>CaCl<sub>2</sub>, KBr: <strong>ionic</strong> (metal + nonmetal). CO<sub>2</sub>, H<sub>2</sub>O: <strong>covalent</strong> (nonmetals). Fe: <strong>metallic</strong>.</p>",
    source="Day 7 p.14")

add(id="m14-p5", module="m14", kind="practice", level="Standard",
    prompt="<p>Why is NaCl's lattice energy (−786 kJ/mol) more negative than its two-body E<sub>el</sub> estimate (about −492 kJ/mol)?</p>",
    answer=choice(("The ions are closer together in the lattice than in a pair.", False, "The two-body estimate already uses the touching distance."),
                  ("In the lattice, each ion is attracted by several oppositely charged neighbors, not just one.", True, "Right: many attractions add up."),
                  ("Lattices contain extra electrons.", False, "The crystal is neutral: Na⁺ and Cl⁻ in a 1 : 1 ratio."),
                  ("E<sub>el</sub> is positive for NaCl.", False, "Opposite charges give negative E<sub>el</sub>.")),
    hints=["Picture the crystalline lattice on Day 7 p.16: how many neighbors does each ion touch?"],
    solution="<p>In the lattice, each ion is surrounded by several oppositely charged neighbors, so many attractions add up and the lattice is “even more stable” than one pair (Day 7 p.17). "
             "<span class='bg'>Textbook §4.1, PDF p.183, printed 149.</span></p>",
    source="Day 7 p.16–17")

add(id="m14-transfer", module="m14", kind="transfer", level="Transfer",
    prompt="<p>CaO isn't in the Day 7 table. Predict which has the more negative lattice energy, CaO or KF, and give the main reason.</p>",
    answer=choice(("KF, because K and F are more reactive", False, "Reactivity isn't what E<sub>el</sub> measures; charge and distance are."),
                  ("CaO, because Q<sub>1</sub>Q<sub>2</sub> = −4 for Ca<sup>2+</sup>/O<sup>2−</sup> vs. −1 for K<sup>+</sup>/F<sup>−</sup>", True, "Right: the charge product dominates (compare MgO −3791 vs. NaF −930)."),
                  ("They're about equal, since the ion sizes are similar", False, "Similar sizes, but four times the charge product."),
                  ("KF, because F<sup>−</sup> is smaller than O<sup>2−</sup>", False, "The size difference is minor next to the ×4 charge effect.")),
    hints=["What changes E<sub>el</sub> = 2.31 × 10<sup>−19</sup> J·nm Q<sub>1</sub>Q<sub>2</sub>/d the most here?"],
    solution="<p><strong>CaO.</strong> Q<sub>1</sub>Q<sub>2</sub> is −4 vs. −1, and d is similar (Ca<sup>2+</sup> 100 + O<sup>2−</sup> 140 pm vs. K<sup>+</sup> 138 + F<sup>−</sup> 133 pm, Day 7 p.8). The same pattern shows in MgO (−3791) vs. NaF (−930) on Day 7 p.17.</p>",
    source="Day 7 p.8, p.15, p.17")

add(id="m14-m-explain", module="m14", kind="mastery", level="Explain",
    prompt="<p>Why is E<sub>el</sub> negative for a cation–anion pair, and what does the Day 7 p.15 energy curve show when the ions get too close?</p>",
    answer={"type": "self", "model": "<p>Q<sub>1</sub>Q<sub>2</sub> is negative for opposite charges, so E<sub>el</sub> < 0: the pair is lower in energy than separated ions. The closer they get, the more negative E<sub>el</sub> becomes, which means stronger attraction. "
                                     "But on the Day 7 p.15 curve, at very short distances the energy rises steeply (repulsion as the electron clouds overlap). The bottom of the well is the bonding distance.</p>"},
    hints=[], solution="", source="Day 7 p.15")

add(id="m14-m-recognize", module="m14", kind="mastery", level="Recognize",
    prompt="<p>“Compare the attraction between Li<sup>+</sup> and F<sup>−</sup> with that between K<sup>+</sup> and Br<sup>−</sup>.” What decides it?</p>",
    answer=choice(("The charges differ, so compare Q<sub>1</sub>Q<sub>2</sub>.", False, "Both pairs are +1/−1."),
                  ("Same charges, so the smaller distance (LiF) gives the stronger attraction.", True, "Right: E<sub>el</sub> ∝ Q<sub>1</sub>Q<sub>2</sub>/d."),
                  ("Bond type: one is covalent.", False, "Both are ionic."),
                  ("Molar mass", False, "Mass doesn't enter E<sub>el</sub>.")),
    hints=["Look at both factors in E<sub>el</sub> = 2.31 × 10<sup>−19</sup> J·nm Q<sub>1</sub>Q<sub>2</sub>/d."],
    solution="<p>Equal charges, so the <strong>distance</strong> decides: LiF has smaller ions, a smaller d, and stronger attraction (U: LiF −1049 vs. KBr −691 kJ/mol, Day 7 p.17).</p>",
    source="Day 7 p.15, p.17")

add(id="m14-m-sanity", module="m14", kind="mastery", level="Sanity check",
    prompt="<p>A student computes E<sub>el</sub> = +8.16 × 10<sup>−19</sup> J for one Na<sup>+</sup>–Cl<sup>−</sup> pair at d = 0.283 nm. What's the problem?</p>",
    answer=choice(("Nothing; energies are positive.", False, "Opposite charges attract, giving a negative E<sub>el</sub>."),
                  ("Sign error: Q<sub>1</sub>Q<sub>2</sub> = (+1)(−1) is negative, so E<sub>el</sub> must be negative.", True, "Right: Day 7 p.15 (the −E<sub>el</sub> side of the curve)."),
                  ("The distance must be in pm.", False, "The constant uses nm."),
                  ("Na<sup>+</sup> and Cl<sup>−</sup> repel.", False, "Opposite charges attract.")),
    hints=["What's the sign of (+1)(−1)?"],
    solution="<p>A positive E<sub>el</sub> would mean repulsion. For Na<sup>+</sup>/Cl<sup>−</sup>, Q<sub>1</sub>Q<sub>2</sub> = −1, so E<sub>el</sub> = 2.31 × 10<sup>−19</sup> J·nm × (−1) ÷ 0.283 nm = <strong>−8.16 × 10<sup>−19</sup> J</strong>: the size is right, the sign is wrong.</p>",
    source="Day 7 p.15")

# =====================================================================================
# m15 Ionic formulas & names (Day 7 p.18–21)
# =====================================================================================
add(id="m15-attempt", module="m15", kind="attempt", level="Guided attempt",
    prompt="<p>Write the formula and the name of the ionic compound formed by aluminum and sulfur.</p>",
    answer={"type": "multi", "parts": [
        {"label": "formula", **formula_ans(["Al2S3"], placeholder="e.g., MgCl2")},
        {"label": "name", **text_ans(["aluminum sulfide", "aluminium sulfide", "aluminum sulphide", "aluminium sulphide"], ci=True, placeholder="name")}]},
    hints=["Ionic compound: find each ion's charge, then make the total charge zero (Day 7 p.18–20).",
           "Al (group 13) loses its 3 valence electrons → Al<sup>3+</sup>; S (group 16) gains 2 to fill its valence shell → S<sup>2−</sup>.",
           "The lowest common multiple of 3 and 2 is 6: two Al<sup>3+</sup> (+6) and three S<sup>2−</sup> (−6).",
           "Formula: Al<sub>2</sub>S<sub>3</sub>. Name: cation name + anion stem + “-ide” (Day 7 p.21)."],
    solution="<p>2 Al<sup>3+</sup> (+6) + 3 S<sup>2−</sup> (−6) → total 0 → <strong>Al<sub>2</sub>S<sub>3</sub></strong>, named <strong>aluminum sulfide</strong>: the cation keeps the element's name, the anion's ending changes to -ide, and there are no prefixes (Day 7 p.21).</p>",
    compare={
        "wrong": "<p>“AlS” (just pair them), “Al<sub>3</sub>S<sub>2</sub>” (the charges crossed the wrong way), or “dialuminum trisulfide”.</p>",
        "tempting": "One of each looks simplest; swapping looks like the criss-cross trick; prefixes look like extra precision.",
        "fails": "AlS has a net charge of +3 − 2 = +1, but “The TOTAL charge has to be zero” (Day 7 p.20). Al<sub>3</sub>S<sub>2</sub> gives +9 − 4 = +5. Binary ionic names use no number prefixes: it's “magnesium chloride,” not “magnesium dichloride” (Day 7 p.21)."},
    source="Day 7 p.18–21")

add(id="m15-p1", module="m15", kind="practice", level="Warm-up",
    prompt="<p>Formula of the ionic compound formed by calcium and chlorine?</p>",
    answer=formula_ans(["CaCl2"]),
    hints=["Ca → Ca<sup>2+</sup>; Cl → Cl<sup>−</sup>.", "How many Cl<sup>−</sup> cancel one Ca<sup>2+</sup>?"],
    solution="<p>Ca<sup>2+</sup> + 2 Cl<sup>−</sup> → <strong>CaCl<sub>2</sub></strong>, just like MgCl<sub>2</sub> on Day 7 p.20.</p>",
    source="Day 7 p.19–20")

add(id="m15-p2", module="m15", kind="practice", level="Standard",
    prompt="<p>Formula of the ionic compound formed by potassium and sulfur?</p>",
    answer=formula_ans(["K2S"]),
    hints=["K → K<sup>+</sup> (group 1); S → S<sup>2−</sup> (group 16, like O).", "Two K<sup>+</sup> cancel one S<sup>2−</sup>."],
    solution="<p>2 K<sup>+</sup> + S<sup>2−</sup> → <strong>K<sub>2</sub>S</strong>.</p>",
    source="Day 7 p.18–20")

add(id="m15-p3", module="m15", kind="practice", level="Warm-up",
    prompt="<p>Name Na<sub>2</sub>O.</p>",
    answer=text_ans(["sodium oxide"], ci=True, placeholder="name"),
    hints=["Cation name first, then anion stem + -ide."],
    solution="<p><strong>sodium oxide</strong> (no “di-”, Day 7 p.21).</p>",
    source="Day 7 p.21")

add(id="m15-p4", module="m15", kind="practice", level="Warm-up",
    prompt="<p>Name AlCl<sub>3</sub>.</p>",
    answer=text_ans(["aluminum chloride", "aluminium chloride"], ci=True, placeholder="name"),
    hints=["chlorine → chloride."],
    solution="<p><strong>aluminum chloride</strong>: cation name, then the anion's name ending in -ide (Day 7 p.21).</p>"
             "<p class='connection'>By the textbook's electronegativity guideline (§4.2, a textbook preview), Al–Cl has Δχ = 3.0 − 1.5 = 1.5, which is polar covalent. The Day 7 naming rule still treats a metal + nonmetal pair as a binary ionic compound, so the name is the same either way.</p>",
    source="Day 7 p.21")

add(id="m15-p5", module="m15", kind="practice", level="Stretch",
    prompt="<p><span class='tag-conn'>Extends the Day 7 rule to group 15</span> Formula of the ionic compound formed by magnesium and nitrogen?</p>",
    answer=formula_ans(["Mg3N2"]),
    hints=["N gains enough electrons to fill its valence shell (Day 7 p.18): 2s<sup>2</sup>2p<sup>3</sup> + 3 e<sup>−</sup> → N<sup>3−</sup>.",
           "Mg<sup>2+</sup> and N<sup>3−</sup>: the lowest common multiple of 2 and 3 is 6.",
           "Three Mg<sup>2+</sup> (+6), two N<sup>3−</sup> (−6).",
           "Mg<sub>?</sub>N<sub>?</sub>"],
    solution="<p>3 Mg<sup>2+</sup> + 2 N<sup>3−</sup> → <strong>Mg<sub>3</sub>N<sub>2</sub></strong> (magnesium nitride). <span class='connection'>N<sup>3−</sup> follows the Day 7 p.18 rule, though the slides only showed Cl<sup>−</sup>, F<sup>−</sup>, and O<sup>2−</sup>.</span></p>",
    source="Day 7 p.18–20")

add(id="m15-p6", module="m15", kind="practice", level="Standard",
    prompt="<p>Which is the correct name for CaF<sub>2</sub>?</p>",
    answer=choice(("calcium difluoride", False, "Binary ionic names use no prefixes (“But also magnesium chloride!”, Day 7 p.21)."),
                  ("calcium fluoride", True, "Right."),
                  ("calcium fluorine", False, "The anion name ends in -ide."),
                  ("fluorine calcide", False, "The cation comes first and keeps its element name.")),
    hints=["Day 7 p.21's naming rules; notice “magnesium chloride” for MgCl<sub>2</sub>."],
    solution="<p><strong>calcium fluoride</strong>.</p>",
    source="Day 7 p.21")

add(id="m15-transfer", module="m15", kind="transfer", level="Transfer",
    prompt="<p>An unknown metal M forms the oxide M<sub>2</sub>O<sub>3</sub>. (a) What is the charge on the M ion (enter a number)? (b) What formula would M form with chlorine?</p>",
    answer={"type": "multi", "parts": [
        {"label": "(a) charge on M", **num_ans(3, tol=0)},
        {"label": "(b) formula with Cl", **formula_ans(["MCl3"], placeholder="use M for the metal")}]},
    hints=["Work backward from charge balance: three O<sup>2−</sup> give −6.",
           "Two M ions must provide +6 in total.",
           "So each M is 3+.",
           "M<sup>3+</sup> + Cl<sup>−</sup> → M?Cl?"],
    solution="<p>3 × (−2) = −6, so 2 × (charge on M) = +6 → <strong>M<sup>3+</sup></strong> (a group 13 metal, like Al). With Cl<sup>−</sup>: <strong>MCl<sub>3</sub></strong>.</p>",
    source="Day 7 p.18–20")

add(id="m15-m-explain", module="m15", kind="mastery", level="Explain",
    prompt="<p>Why does magnesium chloride's formula have a subscript 2 while its name has no “di-”?</p>",
    answer={"type": "self", "model": "<p>The formula states the ratio of ions needed for zero total charge: one Mg<sup>2+</sup> needs two Cl<sup>−</sup>, hence MgCl<sub>2</sub> (the red 2 on Day 7 p.20). "
                                     "The name only identifies the ions, cation then anion-ide. Their charges are fixed for these main-group ions, so the ratio is implied and no prefix is needed: “But also magnesium chloride!” (Day 7 p.21).</p>"},
    hints=[], solution="", source="Day 7 p.20–21")

add(id="m15-m-recognize", module="m15", kind="mastery", level="Recognize",
    prompt="<p>Which ion does selenium (group 16) form?</p>",
    answer=choice(("Se<sup>+</sup>", False, "Nonmetals in group 16 gain electrons."), ("Se<sup>2−</sup>", True, "Right: like O<sup>2−</sup> and S<sup>2−</sup> (Day 7 p.8 lists Se<sup>2−</sup>)."),
                  ("Se<sup>6+</sup>", False, "Losing six electrons isn't how a main-group anion forms."), ("Se<sup>−</sup>", False, "One electron doesn't complete the shell; it needs two.")),
    hints=["Same group as O."],
    solution="<p><strong>Se<sup>2−</sup></strong>: gaining 2 electrons reaches the [Kr] configuration.</p>",
    source="Day 7 p.8, p.18")

add(id="m15-m-sanity", module="m15", kind="mastery", level="Sanity check",
    prompt="<p>A student writes barium oxide as Ba<sub>2</sub>O<sub>2</sub>. What's the fix?</p>",
    answer=choice(("It's correct.", False, "Formulas use the smallest whole-number ratio."),
                  ("Reduce to the lowest ratio: BaO.", True, "Right: Ba²⁺ and O²⁻ cancel 1 : 1, like MgO (Day 7 p.20)."),
                  ("BaO<sub>2</sub>", False, "That has a net charge of +2 − 4 = −2."),
                  ("Ba<sub>2</sub>O", False, "That has a net charge of +4 − 2 = +2.")),
    hints=["Compare Mg<sup>2+</sup> + O<sup>2−</sup> → MgO on Day 7 p.20."],
    solution="<p><strong>BaO</strong>: 2+ and 2− cancel one-to-one.</p>",
    source="Day 7 p.20")

# =====================================================================================
# Mixed review (unlabeled; "what gave it away" cue after answering)
# =====================================================================================
x_debrog = de_broglie(ME, 3.00e6)
add(id="x1", module="mixed", kind="mixed", level="Mixed",
    prompt="<p>An electron (m = 9.109 × 10<sup>−31</sup> kg) moves at 3.00 × 10<sup>6</sup> m/s. What is its wavelength?</p>",
    answer=num_ans(x_debrog, sf=3, unit_label="m", units=M_UNITS),
    hints=["What kind of object is it: a photon, or a particle with mass?", "λ = h/(mu)."],
    solution=f"<p>λ = h/(mu) = 6.626 × 10<sup>−34</sup> ÷ (9.109 × 10<sup>−31</sup> × 3.00 × 10<sup>6</sup>) = <strong>{sci(x_debrog)} m</strong>.</p>",
    cue="A particle <em>with mass</em> and a speed, asking for a wavelength → de Broglie, λ = h/(mu) (Day 4 p.11). Not E = hc/λ, which is for photons.",
    source="Day 4 p.11", home="m7")

E_x2 = H * 5.00e14
KE_x2 = E_x2 - 2.50e-19
add(id="x2", module="mixed", kind="mixed", level="Mixed",
    prompt="<p>Light with ν = 5.00 × 10<sup>14</sup> s<sup>−1</sup> strikes a metal whose threshold energy is 2.50 × 10<sup>−19</sup> J. What is the kinetic energy of the ejected electrons?</p>",
    answer=num_ans(KE_x2, sf=2, unit_label="J", units=J_UNITS),
    hints=["Light + metal + threshold energy …", "KE = hν − φ."],
    solution=f"<p>hν = (6.626 × 10<sup>−34</sup> J·s)(5.00 × 10<sup>14</sup> s<sup>−1</sup>) = {sci(E_x2)} J; KE = hν − φ = {sci(E_x2)} J − 2.50 × 10<sup>−19</sup> J = <strong>{sci(KE_x2, 2)} J</strong>. "
             f"Subtraction keeps the last decimal place both values share (the 10<sup>−21</sup> J place), so only 2 significant figures survive ({sci(KE_x2, 3)} J before rounding; the textbook's rule, §1.7).</p>",
    cue="“Metal,” “threshold energy/work function,” “ejected electrons” → photoelectric effect, KE = hν − φ (Day 3 p.19).",
    source="Day 3 p.19", home="m5")

add(id="x3", module="mixed", kind="mixed", level="Mixed",
    prompt="<p>Which set (n, ℓ, m<sub>ℓ</sub>, m<sub>s</sub>) could describe the outermost electron of a ground-state potassium atom?</p>",
    answer=choice(("(4, 0, 0, +½)", True, "Right: K = [Ar]4s¹, a 4s electron."),
                  ("(4, 1, 0, +½)", False, "That's 4p; 4s fills before 4p."),
                  ("(3, 2, 0, +½)", False, "That's 3d; K's last electron goes to 4s, which is lower in energy (Day 6 p.19)."),
                  ("(4, 0, 1, +½)", False, "For ℓ = 0, m<sub>ℓ</sub> must be 0.")),
    hints=["Write K's configuration first."],
    solution="<p>K = [Ar]4s<sup>1</sup> → n = 4, ℓ = 0, m<sub>ℓ</sub> = 0, m<sub>s</sub> = +½ (or −½).</p>",
    cue="Quantum numbers of a specific atom's electron → configuration first (Day 6), then translate to (n, ℓ, m<sub>ℓ</sub>, m<sub>s</sub>) (Day 5 p.10–14).",
    source="Day 5 p.10–14; Day 6 p.19", home="m8")

add(id="x4", module="mixed", kind="mixed", level="Mixed",
    prompt="<p>Rank by first ionization energy, highest (1) to lowest (4): Na, Mg, P, Cl.</p>",
    answer=order_ans([("Na", "Na"), ("Mg", "Mg"), ("P", "P"), ("Cl", "Cl")], ["Cl", "P", "Mg", "Na"], "highest (1) to lowest (4)"),
    hints=["All period 3: which way does IE₁ go across a period?"],
    solution="<p><strong>Cl (1251) > P (1012) > Mg (738) > Na (496)</strong> kJ/mol (Day 7 p.9).</p>",
    cue="“Ionization energy” + elements in one period → the periodic trend (Day 7 p.9).",
    source="Day 7 p.9", home="m13")

add(id="x5", module="mixed", kind="mixed", level="Mixed",
    prompt="<p>Formula of the compound formed by calcium and nitrogen?</p>",
    answer=formula_ans(["Ca3N2"]),
    hints=["Ion charges from the groups.", "Ca<sup>2+</sup> and N<sup>3−</sup>."],
    solution="<p>3 Ca<sup>2+</sup> (+6) + 2 N<sup>3−</sup> (−6) → <strong>Ca<sub>3</sub>N<sub>2</sub></strong>.</p>",
    cue="Metal + nonmetal → ions; zero total charge sets the subscripts (Day 7 p.18–20).",
    source="Day 7 p.18–20", home="m15")

add(id="x6", module="mixed", kind="mixed", level="Mixed",
    prompt="<p>Configuration of Co<sup>3+</sup> (Co: Z = 27)?</p>",
    answer=cfg_ans(27, 3, "Co<sup>3+</sup>"),
    hints=["Neutral atom first, then remove electrons.", "Highest n leaves first."],
    solution="<p>Co [Ar]4s<sup>2</sup>3d<sup>7</sup> → Co<sup>3+</sup> <strong>[Ar]3d<sup>6</sup></strong>.</p>",
    cue="A transition-metal <em>cation</em> → remove 4s before 3d (Day 6 p.21).",
    source="Day 6 p.21", home="m11")

lam_x7 = nm_from_energy(bohr_dE(2, 5))
add(id="x7", module="mixed", kind="mixed", level="Mixed",
    prompt="<p>A hydrogen atom absorbs a photon, and its electron goes from n = 2 to n = 5. What wavelength (nm) was absorbed?</p>",
    answer=num_ans(lam_x7, sf=3, unit_label="nm", units=NM_UNITS),
    hints=["Hydrogen + two n values …", "ΔE = −2.178 × 10<sup>−18</sup> J (1/5<sup>2</sup> − 1/2<sup>2</sup>), then λ = hc/ΔE."],
    solution=f"<p>ΔE = +{sci(bohr_dE(2, 5), 4)} J; λ = hc/ΔE = <strong>{num(lam_x7, 3)} nm</strong>, the same wavelength as the 5 → 2 emission line.</p>",
    cue="“Hydrogen” + “n = 2 to n = 5” → Bohr ΔE equation, then E = hc/λ (Day 4 p.10). Absorption makes ΔE positive.",
    source="Day 4 p.10", home="m6")

add(id="x8", module="mixed", kind="mixed", level="Mixed",
    prompt="<p>Compound A: 1.000 g contains 0.400 g of element X and 0.600 g of element Y. Compound B: 1.000 g contains 0.250 g of X and 0.750 g of Y. "
           "For a fixed mass of X, what is the ratio of Y masses, B : A?</p>",
    answer=num_ans((0.750 / 0.250) / (0.600 / 0.400), sf=3),
    hints=["Fix the mass of X first: grams of Y per gram of X in each compound.", "A: 0.600/0.400; B: 0.750/0.250."],
    solution="<p>A: 1.500 g Y per g X; B: 3.000 g Y per g X → ratio <strong>2.00</strong>, a 2 : 1 small whole-number ratio.</p>",
    cue="Two compounds of the same two elements → multiple proportions; fix one element's mass first (Day 1 p.13).",
    source="Day 1 p.13", home="m1")

add(id="x9", module="mixed", kind="mixed", level="Mixed",
    prompt="<p>Which is larger: Mg<sup>2+</sup> or Na<sup>+</sup>?</p>",
    answer=choice(("Mg<sup>2+</sup>", False, "Same 10 electrons but 12 protons pulling on them."), ("Na<sup>+</sup>", True, "Right: 102 vs. 72 pm (Day 7 p.8)."),
                  ("Same size", False, "Same electron count, different nuclear charge."), ("Can't tell", False, "Isoelectronic ions compare by Z.")),
    hints=["Count electrons in each ion."],
    solution="<p><strong>Na<sup>+</sup></strong> (102 pm) > Mg<sup>2+</sup> (72 pm). Both have 10 electrons; Mg has more protons.</p>",
    cue="Two ions with the same electron count → isoelectronic: more protons, smaller (Day 7 p.8).",
    source="Day 7 p.8", home="m12")

E_x10 = e_el(2, -2, (100 + 184) / 1000)
add(id="x10", module="mixed", kind="mixed", level="Mixed",
    prompt="<p>Ca<sup>2+</sup> (100 pm) and S<sup>2−</sup> (184 pm) touch. What is the electrostatic potential energy of the pair?</p>",
    answer=num_ans(E_x10, sf=3, unit_label="J", units=J_UNITS),
    hints=["Two ions + a distance …", "E<sub>el</sub> = 2.31 × 10<sup>−19</sup> J·nm (Q<sub>1</sub>Q<sub>2</sub>/d), d in nm."],
    solution=f"<p>d = 284 pm = 0.284 nm; E<sub>el</sub> = 2.31 × 10<sup>−19</sup> × (−4) ÷ 0.284 = <strong>{sci(E_x10)} J</strong>.</p>",
    cue="Ion charges + distance → Coulombic E<sub>el</sub> (Day 7 p.15).",
    source="Day 7 p.15", home="m14")

add(id="x11", module="mixed", kind="mixed", level="Mixed",
    prompt="<p>Which observation shows that light behaves as particles (packets of energy)?</p>",
    answer=choice(("Light bends through a prism.", False, "Wave behavior."),
                  ("A metal ejects electrons only above a threshold frequency, however bright the light.", True, "Right: energy arrives one photon (hν) at a time."),
                  ("λν = c", False, "A wave relationship."),
                  ("X-rays diffract off crystals.", False, "Diffraction is a wave behavior (Day 4 p.17).")),
    hints=["Which result can't be explained by a smooth “ramp” of energy?"],
    solution="<p>The <strong>threshold frequency</strong> in the photoelectric effect (Day 3 p.18–19).</p>",
    cue="“Particle nature of light” → photons and the threshold behavior of the photoelectric effect (Day 3 p.17–19).",
    source="Day 3 p.17–19", home="m5")

add(id="x12", module="mixed", kind="mixed", level="Mixed",
    prompt="<p>How many unpaired electrons does a ground-state manganese atom (Z = 25) have?</p>",
    answer=num_ans(unpaired(ion_config(25, 0)), tol=0),
    hints=["Configuration first.", "[Ar]4s<sup>2</sup>3d<sup>5</sup>: five electrons in five d orbitals …"],
    solution="<p>Mn = [Ar]4s<sup>2</sup>3d<sup>5</sup>; Hund's rule puts one electron in each 3d orbital → <strong>5 unpaired</strong>.</p>",
    cue="“Unpaired electrons” → configuration + Hund's rule (Day 6 p.16).",
    source="Day 6 p.16, p.19", home="m10")

lam_x13 = nm_from_energy(4.50e-19)
add(id="x13", module="mixed", kind="mixed", level="Mixed",
    prompt="<p>A photon carries 4.50 × 10<sup>−19</sup> J. What is its wavelength in nm?</p>",
    answer=num_ans(lam_x13, sf=3, unit_label="nm", units=NM_UNITS),
    hints=["Photon energy → wavelength.", "λ = hc/E."],
    solution=f"<p>λ = hc/E = <strong>{num(lam_x13, 3)} nm</strong> (violet-blue visible light).</p>",
    cue="A <em>photon's</em> energy → E = hc/λ (Day 2 p.30; Day 4 p.10).",
    source="Day 2 p.30", home="m3")

add(id="x14", module="mixed", kind="mixed", level="Mixed",
    prompt="<p>Name Li<sub>2</sub>O.</p>",
    answer=text_ans(["lithium oxide"], ci=True, placeholder="name"),
    hints=["Cation name + anion stem + -ide."],
    solution="<p><strong>lithium oxide</strong>.</p>",
    cue="A binary ionic formula → cation name + anion-ide, no prefixes (Day 7 p.21).",
    source="Day 7 p.21", home="m15")

add(id="x15", module="mixed", kind="mixed", level="Mixed",
    prompt="<p>Which particle has the largest radius: K, K<sup>+</sup>, Ar, or Cl<sup>−</sup>?</p>",
    answer=choice(("K", True, "Right: 227 pm, with its 4s electron in a new shell."), ("K<sup>+</sup>", False, "138 pm: it lost the 4s electron."),
                  ("Ar", False, "97 pm."), ("Cl<sup>−</sup>", False, "181 pm: large, but K's n = 4 shell is larger.")),
    hints=["Which one has an electron in the n = 4 shell?"],
    solution="<p><strong>K</strong> (227 pm) > Cl<sup>−</sup> (181) > K<sup>+</sup> (138) > Ar (97) (Day 6 p.24; Day 7 p.8).</p>",
    cue="Sizes of atoms and ions together → count shells first, then protons vs. electrons (Day 6 p.24; Day 7 p.8).",
    source="Day 6 p.24; Day 7 p.8", home="m12")

pct_O = 16.00 / (1.01 + 16.00) * 100
add(id="x16", module="mixed", kind="mixed", level="Mixed",
    prompt="<p>Hydrogen peroxide contains 1.01 g of hydrogen for every 16.00 g of oxygen (Day 1 p.13). What is its percent oxygen by mass?</p>",
    answer=num_ans(pct_O, sf=3, unit_label="%"),
    hints=["What fraction of the compound's mass is oxygen?", "Mass percent = mass of O ÷ total mass × 100%, where the total is 1.01 g + 16.00 g."],
    solution=f"<p>16.00 ÷ (1.01 + 16.00) × 100% = <strong>{num(pct_O, 3)}%</strong> O.</p>",
    cue="“Percent by mass” → mass fraction × 100%, the Day 1 p.11 method.",
    source="Day 1 p.11, p.13", home="m1")

lam_x17 = nm_from_energy(abs(bohr_dE(7, 2)))
add(id="x17", module="mixed", kind="mixed", level="Mixed",
    prompt="<p>A hydrogen emission line comes from the electron dropping from n = 7 to n = 2. What is its wavelength in nm, and is it visible?</p>",
    answer=num_ans(lam_x17, sf=3, unit_label="nm", units=NM_UNITS),
    hints=["Hydrogen + two levels.", "Either Bohr's ΔE with λ = hc/|ΔE|, or Balmer's formula with n = 7 (both give the same line)."],
    solution=f"<p>Bohr: |ΔE| = 2.178 × 10<sup>−18</sup> J (1/4 − 1/49) → λ = <strong>{num(lam_x17, 3)} nm</strong>. Balmer: 364.56 nm × 49/45 = {num(BALMER * 49 / 45, 4)} nm. "
             "Just beyond the violet edge (400 nm), in the near ultraviolet: one of the lines “nobody knew existed” (Day 4 p.7).</p>",
    cue="Hydrogen line from n → 2 → Bohr ΔE or Balmer (Day 3 p.21; Day 4 p.7–10).",
    source="Day 4 p.7–10", home="m6")

add(id="x18", module="mixed", kind="mixed", level="Mixed",
    prompt="<p>Which hydrogen transition releases more energy: n = 3 → 1 or n = 5 → 2?</p>",
    answer=choice(("3 → 1", True, f"Right: {sci(abs(bohr_dE(3, 1)))} J vs. {sci(abs(bohr_dE(5, 2)))} J."), ("5 → 2", False, "Bigger n values, but a smaller energy gap."),
                  ("They're equal.", False, "Compute both with ΔE."), ("Neither; both absorb energy.", False, "Both are drops, so both are emissions.")),
    hints=["Levels crowd together at high n. Where is the biggest gap?"],
    solution=f"<p><strong>3 → 1</strong>: |ΔE| = {sci(abs(bohr_dE(3, 1)))} J (UV), vs. 5 → 2: {sci(abs(bohr_dE(5, 2)))} J (visible).</p>",
    cue="Comparing hydrogen transitions → Bohr ΔE; drops to n = 1 are the largest (Day 4 p.10).",
    source="Day 4 p.10", home="m6")

add(id="x19", module="mixed", kind="mixed", level="Mixed",
    prompt="<p>A copper wire conducts electricity. Which type of bonding explains that?</p>",
    answer=choice(("ionic", False, "Copper is a metal element, not a metal–nonmetal compound."), ("covalent", False, "Covalent electrons are highly localized (Day 7 p.14)."),
                  ("metallic", True, "Right: shared electrons that are “highly mobile” (Day 7 p.14)."), ("none", False, "Copper is held together by metallic bonds.")),
    hints=["Day 7 p.14 uses Cu as its example of one bond type."],
    solution="<p><strong>Metallic</strong> bonding: shared electrons that are highly mobile (Day 7 p.14).</p>",
    cue="A pure metal with a property like conductivity → metallic bonding (Day 7 p.14).",
    source="Day 7 p.14", home="m14")

add(id="x20", module="mixed", kind="mixed", level="Mixed",
    prompt="<p>A period-3 element has IE<sub>1</sub> = 738, IE<sub>2</sub> = 1451, and IE<sub>3</sub> = 7733 kJ/mol. Which group is it in?</p>",
    answer=num_ans(2, tol=0),
    hints=["Look for the big jump in successive IEs.", "The jump comes after IE₂."],
    solution="<p>The big jump comes after IE<sub>2</sub> (1451 → 7733), so there are 2 valence electrons: <strong>group 2</strong> (Mg; IE<sub>1</sub> 738 on Day 7 p.9). "
             "<span class='bg'>IE<sub>2</sub> = 1451 (textbook §3.11, PDF p.159, printed 125); IE<sub>3</sub> from reference data.</span></p>",
    cue="A list of successive ionization energies → find the jump (Day 7 p.10).",
    source="Day 7 p.9–10", home="m13")

# =====================================================================================
# In-class Top Hat questions shown on the slides (SUPPORTED EMPHASIS). The slides give
# no answers; the keys below are ours and are verified in verify_guide.py.
# =====================================================================================
TOPHAT_NOTE = "In-class Top Hat question, reproduced from the slide. The slide gives no answer; this key is ours."

add(id="m3-tophat", module="m3", kind="practice", level="In-class Top Hat",
    signal=TOPHAT_NOTE,
    prompt="<p>“Rank the following types of electromagnetic radiation by wavelength, with the longest wavelength at the top” (Day 2 p.28). Rank 1 = longest.</p>",
    answer=order_ans([("A", "A. Infrared"), ("B", "B. Ultraviolet"), ("C", "C. Green"), ("D", "D. Orange"), ("E", "E. X-Rays")],
                     ["A", "D", "C", "B", "E"], "longest wavelength (1) to shortest (5)"),
    hints=["Use the Day 2 p.29 spectrum: wavelength decreases from radio toward γ rays.",
           "Within the visible band, red/orange light has a longer wavelength than green, which is longer than violet."],
    solution="<p><strong>Infrared > orange > green > ultraviolet > X-rays.</strong> In the visible band, orange (≈600 nm) is longer than green (≈530 nm) (Day 2 p.29).</p>",
    source="Day 2 p.28–29")

add(id="m8-tophat", module="m8", kind="practice", level="In-class Top Hat",
    signal=TOPHAT_NOTE,
    prompt="<p>“Which ONE set of quantum numbers is valid?” (Day 5 p.16), written as (n, ℓ, m<sub>ℓ</sub>, m<sub>s</sub>).</p>",
    answer=choice(("a. (1, 0, −1, +½)", False, "For ℓ = 0, m<sub>ℓ</sub> can only be 0."),
                  ("b. (3, 2, −2, +½)", True, "Right: ℓ = 2 ≤ n − 1 = 2; m<sub>ℓ</sub> = −2 is within −2…+2; m<sub>s</sub> = +½. A 3d electron."),
                  ("c. (2, 2, 0, 0)", False, "Two problems: ℓ must be ≤ n − 1 = 1, and m<sub>s</sub> can't be 0."),
                  ("d. (2, 0, 1, −½)", False, "For ℓ = 0, m<sub>ℓ</sub> must be 0."),
                  ("e. (−3, −2, −1, −½)", False, "n must be a positive integer, and ℓ can't be negative.")),
    hints=["Check each set in order: n ≥ 1 → 0 ≤ ℓ ≤ n − 1 → −ℓ ≤ m<sub>ℓ</sub> ≤ +ℓ → m<sub>s</sub> = ±½ (Day 5 p.10–14)."],
    solution="<p><strong>b. (3, 2, −2, +½)</strong>: every rule is satisfied. a and d break the m<sub>ℓ</sub> rule; c breaks the ℓ and m<sub>s</sub> rules; e has a negative n and ℓ.</p>",
    source="Day 5 p.10–16")

add(id="m11-tophat", module="m11", kind="practice", level="In-class Top Hat",
    signal=TOPHAT_NOTE,
    prompt="<p>“How many 3d electrons does V<sup>3+</sup> have?” (Day 6 p.23). V: Z = 23.</p>",
    answer=num_ans(dict(ion_config(23, 3)).get("3d", 0), tol=0),
    hints=["Write neutral V first: [Ar]4s<sup>2</sup>3d<sup>3</sup>.",
           "Cations lose the highest-n electrons first, so 4s goes before 3d (Day 6 p.21).",
           "Three electrons leave: two from 4s, one from 3d."],
    solution="<p>V [Ar]4s<sup>2</sup>3d<sup>3</sup> → V<sup>3+</sup> <strong>[Ar]3d<sup>2</sup>: 2 3d electrons</strong>. Removing the 3d electrons first would give [Ar]4s<sup>2</sup>, the classic trap that the bold “regardless of the order in which they were added” is aimed at (Day 6 p.21).</p>",
    source="Day 6 p.21–23")

add(id="m12-tophat", module="m12", kind="practice", level="In-class Top Hat",
    signal="In-class Top Hat question, prepared but not done in class (“We didn't have time for this”). The slide gives no answer; this key is ours.",
    prompt="<p>“Rank these atoms from largest to smallest. F S P As Cl” (Day 6 p.26). Rank 1 = largest.</p>",
    answer=order_ans([("F", "F"), ("S", "S"), ("P", "P"), ("As", "As"), ("Cl", "Cl")], ["As", "P", "S", "Cl", "F"], "largest (1) to smallest (5)"),
    hints=["As is in period 4, the only one with an n = 4 valence shell.",
           "P, S, and Cl are in period 3: size falls across the period.",
           "F is in period 2, directly above Cl."],
    solution="<p><strong>As (121) > P (110) > S (103) > Cl (99) > F (71)</strong> pm, using the Day 6 p.24 values. Down a group adds a shell; across a period, Z<sub>eff</sub> pulls the same shell in.</p>",
    source="Day 6 p.24–26")

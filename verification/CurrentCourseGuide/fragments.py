"""HTML fragment helpers (shared by build_guide.py and check_bank.py).

expand_drawings(body)  fragment placeholders -> checked drawings from lewis.py:
    <!--LEWIS:id[:fc][:scale=0.8][:cap=text]-->   <!--SYM:El-->   <!--HYBRID:id1,id2[,...][:scale=0.8]-->
module_page(m, body)   wraps a module fragment (stage divs only) in the header generated from MODULES
fragment_problems(mid, body)  structural problems in one module fragment (stages, slots, explorer names, can-do list)
"""
import html
import re

import lewis as LW
from modules_def import UNITS, MODULES, LABEL_TEXT, LAST_DAY, STAGES

KNOWN_EXPLORERS = {
    # explorers.js (lecture modules, Days 1-7)
    "massRatios", "alphaScatter", "emSpectrum", "lineSpectrum", "photoelectric", "blackbody", "bohr", "deBroglie",
    "quantumNumbers", "radial", "config", "trends", "sizes", "successiveIE", "coulomb", "formula",
    # explorers_preview.js
    "particleBox", "states", "kinetic", "models", "sigfigs", "units", "stats", "nuclide", "ptable", "isotopes",
    "moles", "massSpec", "heisenberg", "pes", "polarity",
    # explorers_ch4.js
    "naming", "lewisSymbol", "lewisSteps", "resonance", "bondChart", "formalCharge", "octet", "vibrations",
    # explorers_ch5.js
    "vsepr", "dipoles", "hybrid", "sigmaPi", "chirality", "moDiagram",
    # explorers_ch18.js
    "bands",
}


def expand_drawings(body):
    def lewis(m):
        parts = m.group(1).split(":")
        sid, kw = parts[0], {"tag": "span"}
        for p_ in parts[1:]:
            if p_ == "fc":
                kw["show_fc"] = True
            elif p_.startswith("scale="):
                kw["scale"] = float(p_[6:])
            elif p_.startswith("cap="):
                kw["caption"] = p_[4:]
        return LW.svg(LW.STRUCTS[sid], **kw)

    def hybrid(m):
        parts = m.group(1).split(":")
        kw = {"tag": "span"}
        for p_ in parts[1:]:
            if p_.startswith("scale="):
                kw["scale"] = float(p_[6:])
        return LW.hybrid_svg([LW.STRUCTS[i] for i in parts[0].split(",")], **kw)

    body = re.sub(r"<!--LEWIS:([^>]+?)-->", lewis, body)
    body = re.sub(r"<!--SYM:([A-Za-z]+)-->", lambda m: LW.symbol_svg(m.group(1))[0], body)
    body = re.sub(r"<!--HYBRID:([^>]+?)-->", hybrid, body)
    return body


def module_page(m, body):
    """Wrap a module fragment in a header generated from MODULES, so labels and citations come from one place."""
    unit = next(u for u in UNITS if u["id"] == m["unit"])
    chips = []
    if m["label"] in ("lecture", "lecture+preview"):
        chips.append(f"<span class='chip chip-lecture'>Covered in lecture: {html.escape(m['sources'])}</span>")
    if m["label"] == "preview":
        chips.append("<span class='chip chip-preview'>Textbook preview: not yet taught in lecture</span>")
    if m["label"] == "lecture+preview":
        chips.append("<span class='chip chip-preview'>Includes a boxed textbook preview</span>")
    pre = [next(x for x in MODULES if x["id"] == q) for q in m["prereqs"]]
    prereq = ("<p class='prereq'>Builds on: " + ", ".join(f"<a href='#{x['id']}'>§{x['sec']} {html.escape(x['title'])}</a>" for x in pre) + "</p>") if pre else ""
    note = ""
    if m["label"] == "preview":
        note = ("<p class='preview-note'><span class='preview-label'>Textbook preview</span>Your professor hasn't taught this section in Days 1–" + str(LAST_DAY) + ". "
                "Everything here comes from Gilbert " + html.escape(m["textbook"]) + ", so treat it as reading ahead; its exam status is unknown.</p>")
    src_line = ("Lecture: " + html.escape(m["sources"]) + ". " if m["sources"] else "") + "Textbook: " + html.escape(m["textbook"]) + "."
    return (f"<section class='page module' id='{m['id']}' data-module='{m['id']}' data-label='{m['label']}' aria-labelledby='{m['id']}-title' hidden>\n"
            f"<header class='module-head'>\n<p class='kicker'>{unit['chapter']}; §{m['sec']}</p>\n"
            f"<h1 id='{m['id']}-title' tabindex='-1'>{html.escape(m['title'])}</h1>\n"
            f"<div class='chips'>{''.join(chips)}</div>\n{note}\n<p class='source'>{src_line}</p>\n{prereq}\n"
            f"<div class='stage-tabs'></div>\n</header>\n{body}\n</section>")


def fragment_problems(mid, body):
    """Structural checks of one module fragment (the build relies on these conventions)."""
    out = []
    stages = re.findall(r"""<div class=["']stage["'] data-stage=["']([a-z]+)["']""", body)
    want = [s for s, _ in STAGES]
    if [s for s in stages if s in want] != [s for s in want if s in stages]:
        out.append(f"{mid}: stages out of order: {stages}")
    for s in ("learn", "understand", "attempt", "compare", "practice", "master"):
        if s not in stages:
            out.append(f"{mid}: missing stage '{s}'")
    for kind_attr in ("attempt", "practice", "transfer mastery"):
        if f'data-module="{mid}" data-kinds="{kind_attr}"' not in body:
            out.append(f"{mid}: missing slot for kinds '{kind_attr}'")
    if f'data-compare="{mid}"' not in body:
        out.append(f"{mid}: missing compare slot")
    if f'class="cando" data-module="{mid}"' not in body:
        out.append(f"{mid}: missing can-do list")
    for name in re.findall(r"""data-explorer=["']([A-Za-z]+)["']""", body):
        if name not in KNOWN_EXPLORERS:
            out.append(f"{mid}: unknown explorer '{name}'")
    for sid in re.findall(r"<!--LEWIS:([^:>]+?)(?::[^>]*?)?-->", body):
        if sid.strip() not in LW.STRUCTS:
            out.append(f"{mid}: unknown Lewis structure id '{sid}'")
    for ids in re.findall(r"<!--HYBRID:([^:>]+?)(?::[^>]*?)?-->", body):
        for sid in ids.split(","):
            if sid.strip() not in LW.STRUCTS:
                out.append(f"{mid}: unknown Lewis structure id '{sid}' in HYBRID")
    if re.search(r"<h1[\s>]", body):
        out.append(f"{mid}: fragments must not contain <h1> (the header is generated)")
    return out

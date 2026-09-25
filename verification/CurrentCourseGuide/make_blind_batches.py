"""Write blind-check batches for problems that have no blind answer yet.

    py -3.11 verification/CurrentCourseGuide/make_blind_batches.py [--start 7] [--size 37]

Each batch_N.json holds prompts and answer formats only (no keys, hints, or solutions). Lewis-structure drawings
are replaced by their screen-reader descriptions, so a text-only solver sees what a screen-reader user hears.
course_data_ch4.json adds the Ch. 4 tables a student has: the polyatomic-ion table (provided on exams, Day 8 p.8),
Table 4.3 prefixes, Table 4.6, and the textbook's electronegativity values."""
import argparse
import glob
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
BLIND = os.path.join(HERE, "blind_check")


def plain(html):
    """HTML → text a solver can read: drawings become [drawing: description]; sub/sup kept as tags."""
    s = re.sub(r"<(figure|span) class='lewis[^']*'><svg[^>]*aria-label='([^']*)'[^>]*>.*?</svg>(?:<(?:figcaption|span) class='lw-cap'>([^<]*)</(?:figcaption|span)>)?</(?:figure|span)>",
               lambda m: f"[drawing: {m.group(2)}{' (' + m.group(3) + ')' if m.group(3) else ''}]", html, flags=re.S)
    s = re.sub(r"<svg class='lw-sym'[^>]*aria-label='([^']*)'[^>]*>.*?</svg>", lambda m: f"[drawing: {m.group(1)}]", s, flags=re.S)
    s = re.sub(r"<span class='lw-arrow'[^>]*>(.*?)</span>", r" \1 ", s)
    s = re.sub(r"</?(p|div|em|strong)[^>]*>", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def fmt(spec):
    t = spec["type"]
    if t == "numeric":
        d = {"type": "numeric"}
        if spec.get("askUnit") or spec.get("unitLabel"):
            d["unit_hint"] = "answer carries a unit"
        return d
    if t == "choice":
        return {"type": "choice", "options": [f"[{i}] " + plain(o["html"]) for i, o in enumerate(spec["options"])]}
    if t == "text":
        d = {"type": "text", "kind": spec.get("kind", "text")}
        if spec.get("placeholder"):
            d["placeholder"] = spec["placeholder"]
        return d
    if t == "order":
        return {"type": "order", "direction": spec["direction"], "items": [f"{it['key']}: {plain(it['html'])}" for it in spec["items"]]}
    if t == "match":
        return {"type": "match", "rows": [f"[{i}] {plain(r['html'])}" for i, r in enumerate(spec["rows"])],
                "options": [f"{o['key']}: {plain(o['html'])}" for o in spec["options"]]}
    if t == "multi":
        return {"type": "multi", "parts": [dict(fmt(p), label=plain(p["label"])) for p in spec["parts"]]}
    if t == "config":
        return {"type": "config", "species": spec.get("species", "")}
    raise ValueError(t)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", type=int, default=7)
    ap.add_argument("--size", type=int, default=37)
    a = ap.parse_args()
    bank = json.load(open(os.path.join(HERE, "problem_bank.json"), encoding="utf-8"))
    done = set()
    for f in glob.glob(os.path.join(BLIND, "answers_*.json")):
        for x in json.load(open(f, encoding="utf-8")):
            done.add(x["id"])
    todo = [p for p in bank if p["answer"]["type"] != "self" and p["id"] not in done]
    items = [{"id": p["id"], "module": p["module"], "label": p.get("label", ""), "prompt": plain(p["prompt"]), "answer_format": fmt(p["answer"])} for p in todo]
    n = 0
    for k in range(0, len(items), a.size):
        num = a.start + n
        assert num <= 9, "verify_guide.py reads answers_[0-9].json: use fewer, larger batches"
        json.dump(items[k:k + a.size], open(os.path.join(BLIND, f"batch_{num}.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(f"batch_{num}.json: {len(items[k:k + a.size])} problems")
        n += 1

    import sys
    sys.path.insert(0, HERE)
    import ch4_data
    import problem_bank_g
    from guide_common import ELECTRONEGATIVITY
    nd = ch4_data.naming_data()
    data = {
        "polyatomic_ions_Day8_p8": [[x["f"], x["q"], x["name"] + (" or " + x["alt"] if x["alt"] else "")] for x in nd["anions"] if x["poly"]] + [["NH4", 1, "ammonium"]],
        "prefixes_Table_4_3": nd["prefixes"],
        "bond_lengths_pm_and_energies_kJ_per_mol_Table_4_6": {k: {"pm": v[0], "kJ/mol": v[1]} for k, v in problem_bank_g.BONDS.items()},
        "Table_4_6_footnote": "The C=O bond energy in CO2 is 799 kJ/mol.",
        "electronegativity_textbook_Fig_4_5": ELECTRONEGATIVITY,
        "course_conventions": [
            "Five steps (Day 8 p.21): 1 count valence electrons; 2 skeleton with single bonds, central atom = largest bonding capacity; "
            "3 complete the octets of atoms bonded to the central atom (H needs 2); 4 compare with the count; 5 use leftover electrons to complete the central atom's octet "
            "(if still short, turn outer lone pairs into shared pairs).",
            "Roman numerals give the charge of a transition-metal ion; the slides write 'copper (II) oxide' with a space, the textbook 'copper(II) oxide'.",
            "Covalent names: prefixes for every count except no 'mono' on the first element; the textbook drops a prefix's final o/a before 'oxide'.",
        ],
    }
    json.dump(data, open(os.path.join(BLIND, "course_data_ch4.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("course_data_ch4.json written")


if __name__ == "__main__":
    main()

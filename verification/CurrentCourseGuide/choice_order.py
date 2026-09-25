"""Deterministic answer positions for multiple-choice items.

The Ch. 4 banks (F, G) were written with the correct option first. Left that way, "pick the first option" would
work on almost every new item. spread() rotates each choice spec so the correct option lands at a position picked
from an MD5 hash of the problem id and part path: stable across builds and roughly uniform. Rotation keeps the
distractors' relative order. Specs whose options have a natural order are listed in KEEP and left alone.
The permutations (new index -> old index) are written to blind_check/choice_order_ch4.json so the blind record,
whose solvers saw the original order, can be remapped."""
import hashlib
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
KEEP = {("m19-attempt", ".1"),       # single / double / triple, in bond-order order
        ("t4-9-attempt", ".0")}      # yes / no


def walk(ans, path=""):
    if ans["type"] == "choice":
        yield path, ans
    elif ans["type"] == "multi":
        for i, p in enumerate(ans["parts"]):
            yield from walk(p, f"{path}.{i}")


def spread(problems, record=os.path.join(HERE, "blind_check", "choice_order_ch4.json")):
    perms = {}
    for p in problems:
        for path, spec in walk(p["answer"]):
            if (p["id"], path) in KEEP:
                continue
            opts = spec["options"]
            n = len(opts)
            k = next(i for i, o in enumerate(opts) if o["correct"])
            target = int(hashlib.md5((p["id"] + path).encode()).hexdigest(), 16) % n
            r = (k - target) % n
            perm = [(i + r) % n for i in range(n)]              # new index -> old index
            spec["options"] = [opts[j] for j in perm]
            assert spec["options"][target]["correct"]
            perms.setdefault(p["id"], {})[path] = perm
    if record:
        json.dump(perms, open(record, "w", encoding="utf-8"), indent=1)
    return perms

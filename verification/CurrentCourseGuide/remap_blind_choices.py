"""Remap the 2026-09-25 blind record (batches 7-9) after choice_order.spread() rotated the Ch. 4 options.

    py -3.11 verification/CurrentCourseGuide/remap_blind_choices.py

The solvers saw the original option order. This keeps what they saw and answered as batch_N_asgiven.json and
answers_N_asgiven.json, then rewrites batch_N.json and answers_N.json in the guide's final order, using
blind_check/choice_order_ch4.json (new index -> old index). Safe to re-run: it always starts from the _asgiven files."""
import json
import os
import re
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
B = os.path.join(HERE, "blind_check")
perms = json.load(open(os.path.join(B, "choice_order_ch4.json"), encoding="utf-8"))


def at(obj, path):
    """(container, key) for a part path like '' or '.2'."""
    if not path:
        return None, None
    idx = [int(x) for x in path.strip(".").split(".")]
    for i in idx[:-1]:
        obj = obj[i]
    return obj, idx[-1]


def fmt_node(fmt, path):
    for i in [int(x) for x in path.strip(".").split(".")] if path else []:
        fmt = fmt["parts"][i]
    return fmt


n_ans = n_fmt = 0
for num in (7, 8, 9):
    bfile, afile = os.path.join(B, f"batch_{num}.json"), os.path.join(B, f"answers_{num}.json")
    bgiven, agiven = bfile.replace(".json", "_asgiven.json"), afile.replace(".json", "_asgiven.json")
    if not os.path.exists(bgiven):
        shutil.copy(bfile, bgiven)
    if not os.path.exists(agiven):
        shutil.copy(afile, agiven)
    batch = json.load(open(bgiven, encoding="utf-8"))
    answers = json.load(open(agiven, encoding="utf-8"))
    for item in batch:
        for path, perm in perms.get(item["id"], {}).items():
            f = fmt_node(item["answer_format"], path)
            old = [re.sub(r"^\[\d+\] ", "", o) for o in f["options"]]
            f["options"] = [f"[{i}] {old[j]}" for i, j in enumerate(perm)]
            n_fmt += 1
    for a in answers:
        for path, perm in perms.get(a["id"], {}).items():
            if not path:
                a["answer"] = perm.index(a["answer"])
            else:
                cont, k = at(a["answer"], path)
                cont[k] = perm.index(cont[k])
            n_ans += 1
    json.dump(batch, open(bfile, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump(answers, open(afile, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"remapped {n_fmt} choice formats and {n_ans} choice answers in batches 7-9")

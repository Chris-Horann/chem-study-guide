"""Validate one problem bank and its modules' fragments without building the whole guide.

    py -3.11 verification/CurrentCourseGuide/check_bank.py problem_bank_i --modules m20,m21,m22
    py -3.11 verification/CurrentCourseGuide/check_bank.py problem_bank_h --modules t4-2,t4-5,t4-6,t4-7,t4-8

Loads the finished Ch. 1-4 banks (a-g) and then the named bank, so a bank that edits earlier problems (as
problem_bank_h relabels Day 9 topics) is checked after its edits. Checks, for the listed modules:
  - every problem's structure (bank_validate.validate: answers, hints, compare panels, sources, labels)
  - per-module counts: one attempt, three practice, a transfer, a self-rated explain item
  - src/<module>.html: stages, slots, compare slot, can-do list, explorer names, Lewis structure ids
  - notation lint and citation page ranges (the same rules verify_guide.py applies)
  - lewis.py: every structure's electron count, octets, formal charges, and RDKit rebuild
Exit status 1 on any finding. Problems of other modules in the same bank (mixed review) are checked too.
"""
import argparse
import importlib
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.stdout.reconfigure(encoding="utf-8")

import problem_bank_g  # noqa: E402,F401  (loads a-g)
from problem_bank_a import PROBLEMS  # noqa: E402
from modules_def import MODULES, MODULE_IDS  # noqa: E402
from bank_validate import validate  # noqa: E402
from fragments import fragment_problems, expand_drawings  # noqa: E402
import lewis as LW  # noqa: E402
import verify_guide as VG  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("bank", help="module name, e.g. problem_bank_i")
    ap.add_argument("--modules", default="", help="comma-separated module ids this bank owns")
    ap.add_argument("--also", default="", help="comma-separated banks to load first (e.g. problem_bank_i for problem_bank_k)")
    a = ap.parse_args()
    for extra in [x for x in a.also.split(",") if x]:
        importlib.import_module(extra)
    before = {id(p) for p in PROBLEMS}
    importlib.import_module(a.bank)
    new = [p for p in PROBLEMS if id(p) not in before]
    mods = [m for m in a.modules.split(",") if m]
    for m in mods:
        if m not in MODULE_IDS:
            print(f"unknown module {m}")
            sys.exit(1)
    subset = [p for p in PROBLEMS if p["module"] in mods or id(p) not in before]
    errs = validate(subset, MODULES, check_modules=mods, need_mixed=False)
    # fragments
    for m in mods:
        f = os.path.join(HERE, "src", m + ".html")
        if not os.path.exists(f):
            errs.append(f"{m}: src/{m}.html missing")
            continue
        body = open(f, encoding="utf-8").read()
        errs += fragment_problems(m, body)
        try:
            body = expand_drawings(body)
        except KeyError as e:
            errs.append(f"{m}: unknown Lewis structure {e}")
            continue
        nodes = VG.html_nodes(body, m)
        for rule, where, text, why in VG.lint_strings(nodes):
            errs.append(f"lint {rule} in {where}: {text[:90]} ({why})")
        for mm in VG.DAY_RUN.finditer(re.sub(r"<[^>]+>", "", body)):
            day = int(mm.group(1))
            for x, y in re.findall(r"(\d+)(?:\s?[–-]\s?(\d+))?", mm.group(2)):
                hi = int(y) if y else int(x)
                if day not in VG.LECTURE_PAGES or hi > VG.LECTURE_PAGES[day]:
                    errs.append(f"{m}: citation {mm.group(0)} past the end of Day {day}")
    # problem strings: lint + citations
    for p in subset:
        nodes = []
        for s in VG.problem_strings(p):
            nodes += VG.html_nodes(s, p["id"])
        for rule, where, text, why in VG.lint_strings(nodes):
            errs.append(f"lint {rule} in {where}: {text[:90]} ({why})")
        for s in VG.problem_strings(p) + [p.get("source", "")]:
            for mm in VG.DAY_RUN.finditer(re.sub(r"<[^>]+>", "", s)):
                day = int(mm.group(1))
                for x, y in re.findall(r"(\d+)(?:\s?[–-]\s?(\d+))?", mm.group(2)):
                    hi = int(y) if y else int(x)
                    if day not in VG.LECTURE_PAGES or hi > VG.LECTURE_PAGES[day]:
                        errs.append(f"{p['id']}: citation {mm.group(0)} past the end of Day {day}")
            for mm in VG.PDF_REF.finditer(re.sub(r"<[^>]+>", "", s)):
                p1 = int(mm.group(1))
                p2 = int(mm.group(2)) if mm.group(2) else p1
                if not (VG.in_scope(p1) and VG.in_scope(p2)):
                    errs.append(f"{p['id']}: textbook page {mm.group(0)} outside the guide's scope")
                if mm.group(3):
                    q1 = int(mm.group(3))
                    if q1 != p1 - VG.TEXTBOOK_OFFSET:
                        errs.append(f"{p['id']}: {mm.group(0)}: printed should be {p1 - VG.TEXTBOOK_OFFSET}")
    errs += LW.check_all(verbose=False)
    kinds = {}
    for p in new:
        kinds[p["kind"]] = kinds.get(p["kind"], 0) + 1
    print(f"{a.bank}: {len(new)} new problems {kinds}; checked {len(subset)} problems in {', '.join(mods) or '(no modules)'}")
    if errs:
        print(f"{len(errs)} findings:")
        for e in errs:
            print("  -", e)
        sys.exit(1)
    print("no findings")


if __name__ == "__main__":
    main()

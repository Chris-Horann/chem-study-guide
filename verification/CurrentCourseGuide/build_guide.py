"""Build the CurrentCourseGuide study guide.

    py -3.11 verification/CurrentCourseGuide/build_guide.py

Writes (all paths relative to the project root):
  study-guides/CurrentCourseGuide/assets/data.js    window.GUIDE_DATA (problems, course data, constants)
  study-guides/CurrentCourseGuide/assets/scope.js   window.SCOPE_PANEL (generated from SOURCE_SCOPE.md)
  study-guides/CurrentCourseGuide/index.html        assembled from verification/CurrentCourseGuide/src/*.html
  verification/CurrentCourseGuide/problem_bank.json  JSON copy of the problem bank
  verification/CurrentCourseGuide/expected_values.json  Python reference values for the node tests

index.html is GENERATED: edit the fragments in src/ and rebuild.
The build stops with an error if any problem fails structural validation.
"""
import html
import json
import math
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
GUIDE = ROOT / "study-guides" / "CurrentCourseGuide"
ASSETS = GUIDE / "assets"
SRC = HERE / "src"
sys.path.insert(0, str(HERE))

from guide_common import *            # noqa: E402,F401
import problem_bank_b                  # noqa: E402  (imports problem_bank_a first)
import problem_bank_c                  # noqa: E402  Ch. 1 textbook preview
import problem_bank_d                  # noqa: E402  Ch. 2 textbook preview
import problem_bank_e                  # noqa: E402  Ch. 3-4 textbook preview + mixed x21-x35
import problem_bank_f                  # noqa: E402  Ch. 4 naming, acids, Lewis symbols and structures (Day 8 + §4.3-4.4)
import problem_bank_g                  # noqa: E402  Ch. 4 §4.5-4.9 + mixed x36-x47
import problem_bank_h                  # noqa: E402  Day 9 lecture items for §4.2, §4.5-4.8
import problem_bank_i                  # noqa: E402  Ch. 5 §5.1-5.3: VSEPR and polar molecules (Day 10-11)
import problem_bank_j                  # noqa: E402  Ch. 5 §5.4-5.5: hybrid orbitals, sigma and pi bonds (Day 11)
import problem_bank_k                  # noqa: E402  Ch. 5 §5.6-5.7: chirality, MO theory
import problem_bank_l                  # noqa: E402  mixed review x48 onward
import problem_bank_m                  # noqa: E402  Ch. 18 §18.4-18.5 (Day 12) + mixed x65-x66
import ch4_data                        # noqa: E402  data for the Ch. 4 explorers
import ch5_data                        # noqa: E402  data for the Ch. 5 explorers
import ch18_data                       # noqa: E402  reference values for the Ch. 18 band explorer
from problem_bank_a import PROBLEMS    # noqa: E402
from modules_def import (BUILD_DATE, LAST_DAY, STORAGE_KEY, tbp, UNITS, MODULES, LABEL_TEXT, STAGES,  # noqa: E402
                         MODULE_IDS, KINDS, ANSWER_TYPES)
from bank_validate import validate     # noqa: E402
from fragments import expand_drawings, module_page, fragment_problems   # noqa: E402

# ---------------------------------------------------------------- validation (bank_validate.py)
errors = validate(PROBLEMS, MODULES)
if errors:
    print("BUILD FAILED: problem-bank validation errors")
    for e in errors:
        print("  -", e)
    sys.exit(1)

# ---------------------------------------------------------------- computed course data
def radial_curves():
    """Normalized hydrogen radial distributions P(r) = r^2 R_nl(r)^2 (pm^-1), r in pm.
    BACKGROUND model (exact hydrogen functions, a0 = 52.918 pm); the slides show the plots."""
    a0 = 52.918
    def R(name, r):
        p = r / a0
        k = a0 ** -1.5
        if name == "1s":
            return 2 * k * math.exp(-p)
        if name == "2s":
            return k / (2 * math.sqrt(2)) * (2 - p) * math.exp(-p / 2)
        if name == "2p":
            return k / (2 * math.sqrt(6)) * p * math.exp(-p / 2)
        if name == "3s":
            return 2 * k / (81 * math.sqrt(3)) * (27 - 18 * p + 2 * p * p) * math.exp(-p / 3)
        if name == "3p":
            return 4 * k / (81 * math.sqrt(6)) * (6 * p - p * p) * math.exp(-p / 3)
        if name == "3d":
            return 4 * k / (81 * math.sqrt(30)) * p * p * math.exp(-p / 3)
        raise ValueError(name)
    step, rmax = 2.0, 1500.0
    rs = [i * step for i in range(int(rmax / step) + 1)]
    curves, raw = {}, {}
    for name in ("1s", "2s", "2p", "3s", "3p", "3d"):
        ys = [r * r * R(name, r) ** 2 for r in rs]
        raw[name] = ys
        curves[name] = [float(f"{y:.4g}") for y in ys]
    # 1s electron density psi^2 = R^2/(4 pi), scaled to its value at r = 0 (the slide's y-axis has no numbers)
    dens = [R("1s", r) ** 2 / (4 * math.pi) for r in rs]
    curves["1s_density_rel"] = [float(f"{d / dens[0]:.4g}") for d in dens]
    # analytic features for labels
    feats = {
        "1s": {"peaks": [a0], "nodes": []},
        "2s": {"peaks": [(3 - math.sqrt(5)) * a0, (3 + math.sqrt(5)) * a0], "nodes": [2 * a0]},
        "2p": {"peaks": [4 * a0], "nodes": []},
        "3s": {"peaks": [], "nodes": [(18 - math.sqrt(108)) / 4 * a0, (18 + math.sqrt(108)) / 4 * a0]},
        "3p": {"peaks": [], "nodes": [6 * a0]},
        "3d": {"peaks": [9 * a0], "nodes": []},
    }
    # numeric peaks for 3s/3p: local maxima of the unrounded curve, refined by a parabola through 3 points
    for name in ("3s", "3p"):
        ys = raw[name]
        pk = []
        for i in range(1, len(ys) - 1):
            if ys[i] > ys[i - 1] and ys[i] >= ys[i + 1] and ys[i] > 1e-7:
                y0, y1, y2 = ys[i - 1], ys[i], ys[i + 1]
                denom = y0 - 2 * y1 + y2
                pk.append(rs[i] + (0.5 * step * (y0 - y2) / denom if denom else 0.0))
        feats[name]["peaks"] = pk
    for f in feats.values():
        f["peaks"] = [round(x, 1) for x in f["peaks"]]
        f["nodes"] = [round(x, 1) for x in f["nodes"]]
    return {"step": step, "rmax": rmax, "a0": a0, "curves": curves, "features": feats}

def config_table():
    """CONFIGS[Z][charge] = [[subshell, count], ...] by the course rules (no exceptions)."""
    out = {}
    for z in range(1, 37):
        row = {}
        for q in range(-3, 4):
            ne = z - q
            if ne < 0 or (q > 0 and ne < 0):
                continue
            if ne == 0:
                row[str(q)] = []
                continue
            if ne > 54:
                continue
            row[str(q)] = [[s, k] for s, k in ion_config(z, q)]
        out[str(z)] = row
    return out

balmer_lines = [{"n": n, "nm": round(BALMER * n * n / (n * n - 4), 1)} for n in range(3, 9)]

def periodic_table():
    """All 118 elements for the §2.3 explorer. Categories follow textbook Fig. 2.9b (TB PDF p.91);
    common ion charges follow Fig. 2.11 (TB PDF p.92). Names from the periodictable package (background)."""
    import periodictable as pt
    def group_of(z):
        if z == 1: return 1
        if z == 2: return 18
        if 3 <= z <= 4: return z - 2
        if 5 <= z <= 10: return z + 8
        if 11 <= z <= 12: return z - 10
        if 13 <= z <= 18: return z
        if 19 <= z <= 36: return z - 18
        if 37 <= z <= 54: return z - 36
        if z in (55, 56): return z - 54
        if z == 57: return 3
        if 58 <= z <= 71: return None
        if 72 <= z <= 86: return z - 68
        if z in (87, 88): return z - 86
        if z == 89: return 3
        if 90 <= z <= 103: return None
        return z - 100
    def period_of(z):
        for top, per in ((2, 1), (10, 2), (18, 3), (36, 4), (54, 5), (86, 6), (118, 7)):
            if z <= top:
                return per
    metalloids = {5, 14, 32, 33, 51, 52, 85}
    nonmetals = {1, 2, 6, 7, 8, 9, 10, 15, 16, 17, 18, 34, 35, 36, 53, 54, 86, 118}
    ions = {"H": ["+"], "Li": ["+"], "Na": ["+"], "K": ["+"], "Rb": ["+"], "Cs": ["+"],
            "Mg": ["2+"], "Ca": ["2+"], "Sr": ["2+"], "Ba": ["2+"], "Sc": ["3+"], "Y": ["3+"], "Ti": ["4+"], "Zr": ["4+"],
            "V": ["3+", "4+"], "Cr": ["3+"], "Mn": ["2+", "4+"], "Fe": ["2+", "3+"], "Co": ["2+", "3+"], "Ni": ["2+"],
            "Cu": ["+", "2+"], "Zn": ["2+"], "Ag": ["+"], "Cd": ["2+"], "Hg": ["2+"], "Al": ["3+"], "Ga": ["3+"], "In": ["3+"],
            "Tl": ["+", "3+"], "Sn": ["2+", "4+"], "Pb": ["2+", "4+"], "N": ["3-"], "P": ["3-"], "O": ["2-"], "S": ["2-"],
            "Se": ["2-"], "Te": ["2-"], "F": ["-"], "Cl": ["-"], "Br": ["-"], "I": ["-"]}
    out = []
    for e in pt.elements:
        z = e.number
        if not 1 <= z <= 118:
            continue
        cat = "metalloid" if z in metalloids else "nonmetal" if z in nonmetals else "metal"
        out.append({"z": z, "sym": e.symbol, "name": e.name, "group": group_of(z), "period": period_of(z),
                    "cat": cat, "f": "lanthanide" if 58 <= z <= 71 else "actinide" if 90 <= z <= 103 else None,
                    "ions": ions.get(e.symbol, [])})
    return out

def molecules():
    """2-D coordinates (RDKit) for the §1.6 formula/model explorer. BACKGROUND geometry: flattened drawings."""
    from rdkit import Chem
    from rdkit.Chem import AllChem, rdMolDescriptors
    specs = [("water", "O", "H2O", "H–O–H"), ("carbon dioxide", "O=C=O", "CO2", "O=C=O"), ("methane", "C", "CH4", "CH4"),
             ("ammonia", "N", "NH3", "NH3"), ("ethanol", "CCO", "C2H6O", "CH3CH2OH"), ("acetone", "CC(=O)C", "C3H6O", "CH3COCH3"),
             ("acetic acid", "CC(=O)O", "C2H4O2", "CH3COOH"), ("propane", "CCC", "C3H8", "CH3CH2CH3")]
    out = []
    for name, smi, formula, condensed in specs:
        mol = Chem.AddHs(Chem.MolFromSmiles(smi))
        AllChem.Compute2DCoords(mol)
        conf = mol.GetConformer()
        atoms = [{"el": a.GetSymbol(), "x": round(conf.GetAtomPosition(i).x, 3), "y": round(conf.GetAtomPosition(i).y, 3)}
                 for i, a in enumerate(mol.GetAtoms())]
        bonds = [{"a": b.GetBeginAtomIdx(), "b": b.GetEndAtomIdx(), "order": int(round(b.GetBondTypeAsDouble()))} for b in mol.GetBonds()]
        calc = rdMolDescriptors.CalcMolFormula(mol)
        assert formula_counts(calc) == formula_counts(formula), (name, calc, formula)  # RDKit writes Hill order (H3N)
        counts = formula_counts(formula)
        g = 0
        for k in counts.values():
            g = math.gcd(g, k)
        emp = "".join(sym + (str(n // g) if n // g > 1 else "") for sym, n in counts.items())
        out.append({"name": name, "formula": formula, "empirical": emp, "condensed": condensed, "atoms": atoms, "bonds": bonds})
    return out

DATA = {
    "meta": {"guide": "CurrentCourseGuide", "title": "Chem 1151 study guide: Gilbert Ch. 1–5 and §18.4–18.5 with Days 1–12", "built": BUILD_DATE, "lastDay": LAST_DAY,
             "storageKey": STORAGE_KEY, "course": "Chem 1151 (Prof. Dransfield)"},
    "units": UNITS,
    "modules": MODULES,
    "stages": STAGES,
    "constants": {
        "c": {"value": C, "unit": "m/s", "source": "Day 2 p.30"},
        "h": {"value": H, "unit": "J·s", "source": "Day 3 p.17"},
        "bohr": {"value": BOHR, "unit": "J", "source": "Day 4 p.10"},
        "coulomb": {"value": COUL, "unit": "J·nm", "source": "Day 7 p.15"},
        "balmer": {"value": BALMER, "unit": "nm", "source": "Day 3 p.21"},
        "me": {"value": ME, "unit": "kg", "source": "Day 2 p.12, p.22"},
        "mp": {"value": MP_KG, "unit": "kg", "source": "Day 2 p.22"},
        "mn": {"value": 1.675e-27, "unit": "kg", "source": "Day 2 p.22 (slide prints 1.67483; textbook 1.67493)"},
        "NA": {"value": NA, "unit": "mol⁻¹", "source": "Background (not on any slide)"},
        "kB": {"value": 1.380649e-23, "unit": "J/K", "source": "Background (Planck curve only)"},
        "amu_kg": {"value": 1.66054e-27, "unit": "kg", "source": "Background"},
    },
    "atomicRadius": ATOMIC_RADIUS,
    "ionicRadius": IONIC_RADIUS,
    "ie1": IE1,
    "ea": EA, "eaGt0": EA_GT0, "eaCalc": EA_CALC,
    "successiveIE": SUCCESSIVE_IE,
    "valence2": VALENCE_2ND_PERIOD,
    "lattice": LATTICE,
    "workFunctionE19": WORK_FUNCTION_E19,
    "workFunctionEV": WORK_FUNCTION_EV,
    "layout": MAIN_GROUP_LAYOUT,
    "groupLabels": GROUP_LABELS,
    "elements": [[s, n] for s, n in ELEMENTS],
    "configs": config_table(),
    "configExceptions": {str(k): v for k, v in CONFIG_EXCEPTIONS.items()},
    "fillOrder": FILL_ORDER,
    "balmerLines": balmer_lines,
    "radial": radial_curves(),
    "labelText": LABEL_TEXT,
    "electronegativity": ELECTRONEGATIVITY,
    "tTable": {str(k): v for k, v in T_TABLE.items()},
    "grubbsZ": {str(k): v for k, v in GRUBBS_Z.items()},
    "atomicMass": ATOMIC_MASS,
    "isotopes": {k: [[a, m, f] for a, m, f in v] for k, v in ISOTOPES.items()},
    "pes": {k: [[sub, be, n] for sub, be, n in v] for k, v in PES.items()},
    "pesTextbook": PES_TEXTBOOK,
    "periodicTable": periodic_table(),
    "molecules": molecules(),
    **ch4_data.build(problem_bank_g.BONDS),
    **ch5_data.build(),
    "problems": PROBLEMS,
}

ASSETS.mkdir(parents=True, exist_ok=True)
js = ("/* GENERATED by verification/CurrentCourseGuide/build_guide.py; do not edit by hand. */\n"
      "window.GUIDE_DATA = " + json.dumps(DATA, ensure_ascii=False, separators=(",", ":")) + ";\n")
(ASSETS / "data.js").write_text(js, encoding="utf-8")
(HERE / "problem_bank.json").write_text(json.dumps(PROBLEMS, ensure_ascii=False, indent=1), encoding="utf-8")

# ---------------------------------------------------------------- SOURCE_SCOPE.md -> scope.js
def md_inline(s):
    s = html.escape(s, quote=False)
    codes = []                                    # protect code spans (file names contain underscores)

    def keep(m):
        codes.append("<code>" + m.group(1) + "</code>")
        return "@@CODE%d@@" % (len(codes) - 1)
    s = re.sub(r"`([^`]+)`", keep, s)
    # plain-text subscripts on one-letter symbols: Z_eff, E_el, R_H, N_A, n_final (not HOMEWORK_INDEX)
    s = re.sub(r"(?<![A-Za-z])([A-Za-zλνχ])_([A-Za-z0-9]{1,8})", r"\1<sub>\2</sub>", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<![\w*])\*([^*\s][^*]*?)\*(?![\w*])", r"<em>\1</em>", s)
    return re.sub(r"@@CODE(\d+)@@", lambda m: codes[int(m.group(1))], s)

def md_to_html(md):
    lines = md.splitlines()
    out, para, i = [], [], 0
    def flush():
        if para:
            out.append("<p>" + md_inline(" ".join(para)) + "</p>")
            para.clear()
    while i < len(lines):
        ln = lines[i].rstrip()
        if not ln.strip():
            flush(); i += 1; continue
        m = re.match(r"^(#{1,4})\s+(.*)$", ln)
        if m:
            flush()
            level = min(len(m.group(1)) + 1, 4)
            out.append(f"<h{level}>{md_inline(m.group(2))}</h{level}>")
            i += 1; continue
        if ln.startswith("|"):
            flush()
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            head, body = rows[0], [r for r in rows[1:] if not all(re.fullmatch(r":?-{3,}:?", c) for c in r)]
            t = ["<div class='table-wrap'><table><thead><tr>" + "".join(f"<th scope='col'>{md_inline(c)}</th>" for c in head) + "</tr></thead><tbody>"]
            for r in body:
                t.append("<tr>" + "".join(f"<td>{md_inline(c)}</td>" for c in r) + "</tr>")
            t.append("</tbody></table></div>")
            out.append("".join(t)); continue
        if re.match(r"^\s*- ", ln):
            flush()
            items = []
            while i < len(lines) and (re.match(r"^\s*- ", lines[i]) or (lines[i].startswith("  ") and lines[i].strip() and items)):
                if re.match(r"^\s*- ", lines[i]):
                    items.append(re.sub(r"^\s*- ", "", lines[i]).strip())
                else:
                    items[-1] += " " + lines[i].strip()
                i += 1
            out.append("<ul>" + "".join(f"<li>{md_inline(x)}</li>" for x in items) + "</ul>")
            continue
        para.append(ln.strip()); i += 1
    flush()
    return "\n".join(out)

scope_md = (GUIDE / "SOURCE_SCOPE.md").read_text(encoding="utf-8")
scope_html = md_to_html(scope_md)
(ASSETS / "scope.js").write_text(
    "/* GENERATED from SOURCE_SCOPE.md by verification/CurrentCourseGuide/build_guide.py */\n"
    "window.SCOPE_PANEL = " + json.dumps({"html": scope_html, "source": "SOURCE_SCOPE.md", "built": BUILD_DATE},
                                         ensure_ascii=False) + ";\n", encoding="utf-8")

# ---------------------------------------------------------------- index.html assembly
def nav_html():
    parts = ["<a class='nav-link nav-home' href='#start' data-testid='nav-start' data-nav='start'>"
             "<span class='nav-title'>Start here</span></a>"]
    for u in UNITS:
        parts.append(f"<p class='nav-unit'>{u['chapter']}: {html.escape(u['title'])}</p>")
        for mid in u["modules"]:
            m = next(x for x in MODULES if x["id"] == mid)
            badge = {"lecture": "L", "preview": "P", "lecture+preview": "L+P"}[m["label"]]
            parts.append(
                f"<a class='nav-link nav-{m['label'].replace('+', '-')}' href='#{mid}' data-testid='nav-{mid}' data-nav='{mid}'>"
                f"<span class='nav-num' aria-hidden='true'>{m['sec']}</span>"
                f"<span class='nav-title'>{html.escape(m['title'])}</span>"
                f"<span class='nav-badge badge-{m['label'].replace('+', '-')}' title='{LABEL_TEXT[m['label']]}'>"
                f"<span aria-hidden='true'>{badge}</span><span class='sr-only'>{LABEL_TEXT[m['label']]}</span></span>"
                f"<span class='nav-status' data-status='{mid}'>Not started</span></a>")
    parts.append("<p class='nav-unit'>Review and reference</p>")
    for pid, label in (("mixed", "Mixed review"), ("toolkit", "Toolkit: constants and equations"), ("scope", "What this guide covers")):
        extra = f"<span class='nav-status' data-status='{pid}'></span>" if pid == "mixed" else ""
        parts.append(f"<a class='nav-link' href='#{pid}' data-testid='nav-{pid}' data-nav='{pid}'>"
                     f"<span class='nav-title'>{label}</span>{extra}</a>")
    return "\n".join(parts)

import lewis as LW                     # noqa: E402

def toolkit_ch4():
    """Ch. 4 reference tables for the toolkit, generated from ch4_data / Table 4.6."""
    nd = ch4_data.naming_data()
    pre = "".join(f"<tr><td>{i + 1}</td><td>{x}-</td></tr>" for i, x in enumerate(nd["prefixes"]))
    ions = []
    for a in nd["anions"]:
        if a["poly"]:
            ions.append((a["html"] + "<sup>" + (str(-a["q"]) if a["q"] < -1 else "") + "−</sup>", a["name"] + (f" or {a['alt']}" if a["alt"] else "")))
    ions.insert(13, ("NH<sub>4</sub><sup>+</sup>", "ammonium"))
    ion_rows = "".join(f"<tr><td>{f}</td><td>{n}</td></tr>" for f, n in ions)
    b_rows = "".join(f"<tr><td>{r['bond']}</td><td>{r['pm']}</td><td>{r['kj']}{'<sup>a</sup>' if r['bond'] == 'C=O' else ''}</td></tr>" for r in ch4_data.bond_table(problem_bank_g.BONDS))
    return ("<h2>Chapter 4 reference tables</h2>\n"
            "<div class='toolkit-grid'>\n"
            "<div><h3>Naming prefixes (Table 4.3)</h3><div class='table-wrap'><table class='data'><thead><tr><th scope='col'>Number</th><th scope='col'>Prefix</th></tr></thead><tbody>" + pre +
            "</tbody></table></div><p class='source'>Lecture, Day 8 p.12–13. No “mono” on the first element.</p></div>\n"
            "<div><h3>Common polyatomic ions</h3><div class='table-wrap'><table class='data'><thead><tr><th scope='col'>Ion</th><th scope='col'>Name</th></tr></thead><tbody>" + ion_rows +
            "</tbody></table></div><p class='source'>Lecture, Day 8 p.8 (the slide's Table 4.5; the textbook's Table 4.4, PDF p.192). “You will be provided with a table like this on the exams, so you don't need to memorize them.”</p></div>\n"
            "<div><h3>Average bond lengths and energies (Table 4.6)</h3><div class='table-wrap'><table class='data'><thead><tr><th scope='col'>Bond</th><th scope='col'>Length (pm)</th><th scope='col'>Energy (kJ/mol)</th></tr></thead><tbody>" + b_rows +
            "</tbody></table></div><p class='source'>Lecture, Day 9 p.14 (the textbook's Table 4.6, PDF p.207, printed 173; the slide boxes the C–C, C–O, O–O, and halogen rows). <sup>a</sup>The C=O bond energy in CO<sub>2</sub> is 799 kJ/mol (the table's footnote).</p></div>\n"
            "</div>\n")

def toolkit_ch5():
    """Ch. 5 reference tables for the toolkit, generated from ch5_data (the slides' tables and the textbook's)."""
    vs = "".join(f"<tr><td>{sn}</td><td>{epg}</td><td>{lp}</td><td>{mg}</td><td>{ang}</td></tr>" for sn, epg, lp, mg, ang in ch5_data.PROF_TABLE)
    t52 = "".join(f"<tr><td>{m[2]}</td><td>{m[10]:.2f}</td><td>{m[12]}</td></tr>" for k in ("HF", "H2O", "NH3", "CHCl3", "CCl3F")
                  for m in ch5_data.DIPOLES if m[0] == k)                      # Table 5.2's row order
    hy = ("<tr><td>2</td><td>sp</td><td>2</td><td>linear</td><td>180°</td></tr>"
          "<tr><td>3</td><td>sp<sup>2</sup></td><td>3; 2</td><td>trigonal planar; bent</td><td>120°</td></tr>"
          "<tr><td>4</td><td>sp<sup>3</sup></td><td>4; 3; 2</td><td>tetrahedral; trigonal pyramidal; bent</td><td>109.5°</td></tr>")
    order = lambda k: " &lt; ".join(f"{n[:-2]}<sub>{n[-2:]}</sub>" for n, _, _ in ch5_data.MO_ORDERS[k])
    return ("<h2>Chapter 5 reference tables</h2>\n"
            "<div class='toolkit-grid'>\n"
            "<div><h3>VSEPR summary (the professor's table)</h3><div class='table-wrap'><table class='data'><thead><tr><th scope='col'>Electron domains</th><th scope='col'>Electron-pair geometry</th><th scope='col'>Lone pairs</th><th scope='col'>Molecular geometry</th><th scope='col'>Ideal bond angles</th></tr></thead><tbody>" + vs +
            "</tbody></table></div><p class='source'>Lecture, Day 10 p.26 (“See-saw” as printed). Not in the table but on Day 10 p.23: SN 5 with 3 lone pairs is linear (XeF<sub>2</sub>). The textbook says SN 6 with 3 lone pairs is possible but not met in practice (Table 5.1, PDF p.240). Lone pairs make real angles smaller than these ideal ones: NH<sub>3</sub> 107°, H<sub>2</sub>O 104.5°, O<sub>3</sub> 117° (Day 10 p.15–19).</p></div>\n"
            "<div><h3>Permanent dipole moments (Table 5.2)</h3><div class='table-wrap'><table class='data'><thead><tr><th scope='col'>Molecule</th><th scope='col'>μ (D)</th><th scope='col'>Points</th></tr></thead><tbody>" + t52 +
            "</tbody></table></div><p class='source'>Lecture, Day 11 p.8 (the textbook's Table 5.2, PDF p.245). CO<sub>2</sub>, CF<sub>4</sub>, and other molecules whose bond dipoles cancel have μ = 0 (Day 10 p.29–30).</p></div>\n"
            "<div><h3>Hybridization by steric number (Table 5.3)</h3><div class='table-wrap'><table class='data'><thead><tr><th scope='col'>SN</th><th scope='col'>Hybrids</th><th scope='col'>σ bonds</th><th scope='col'>Molecular geometries</th><th scope='col'>Angle between hybrids</th></tr></thead><tbody>" + hy +
            "</tbody></table></div><p class='source'>Lecture, Day 11 p.24 (the textbook's Table 5.3, PDF p.252). The slide's sp<sup>3</sup> row prints “Trigonal planar” for 3 σ bonds; the textbook's table and Day 10 p.18 say trigonal pyramidal. With lone pairs, the angles are less than the hybrids' angles.</p></div>\n"
            "<div><h3>Valence MO order (§5.7)</h3><p>Li<sub>2</sub>–N<sub>2</sub>: " + order("low") + "</p><p>O<sub>2</sub>–Ne<sub>2</sub> and NO: " + order("high") + "</p>"
            "<p>Bond order = ½[(bonding e<sup>−</sup>) − (antibonding e<sup>−</sup>)]; unpaired electrons → paramagnetic.</p>"
            "<p class='source'><span class='pill-label preview'>Textbook preview</span> §5.7, Figs. 5.49–5.52 and Eq. 5.2 (PDF p.262–268). The lecture only raises O<sub>2</sub>'s magnetism (Day 11 p.27).</p></div>\n"
            "</div>\n")

order = ["head.html", "start.html"] + [f"{m['id']}.html" for m in MODULES] + ["mixed.html", "toolkit.html", "scope.html", "foot.html"]
missing = [f for f in order if not (SRC / f).exists()]
frag_errors = []
for m in MODULES:
    f = SRC / (m["id"] + ".html")
    if f.exists():
        frag_errors += fragment_problems(m["id"], f.read_text(encoding="utf-8"))
if frag_errors:
    print("BUILD FAILED: fragment structure errors")
    for e in frag_errors:
        print("  -", e)
    sys.exit(1)
if missing:
    print("index.html not assembled; missing src fragments:", ", ".join(missing))
else:
    pieces = []
    for f in order:
        body = expand_drawings((SRC / f).read_text(encoding="utf-8"))
        if f == "toolkit.html":
            body = body.replace("<!--TOOLKIT_CH4-->", toolkit_ch4()).replace("<!--TOOLKIT_CH5-->", toolkit_ch5())
        mod = next((m for m in MODULES if f == m["id"] + ".html"), None)
        pieces.append(module_page(mod, body) if mod else body)
    page = "\n".join(pieces).replace("<!--NAV-->", nav_html())
    page = page.replace("<!--BUILD_DATE-->", BUILD_DATE)
    leftover = re.findall(r"<!--(?:LEWIS|SYM|HYBRID|TOOLKIT_CH4|TOOLKIT_CH5)[^>]*-->", page)
    assert not leftover, leftover
    (GUIDE / "index.html").write_text(page, encoding="utf-8")
    print("index.html assembled from", len(order), "fragments")

# ---------------------------------------------------------------- reference values for node tests
exp = {
    "bohr": [{"ni": ni, "nf": nf, "dE": bohr_dE(ni, nf), "nm": nm_from_energy(abs(bohr_dE(ni, nf)))}
             for ni, nf in ((3, 2), (4, 2), (5, 2), (6, 2), (2, 1), (4, 3), (1, 3), (2, 5))],
    "photon": [{"nm": x, "E": photon_energy_from_nm(x), "nu": C / (x * 1e-9)} for x in (220.0, 400.0, 530.0, 656.0)],
    "debroglie": [{"m": m, "u": u, "lam": de_broglie(m, u)} for m, u in ((ME, 4.05e6), (0.142, 44.0), (1.675e-27, 2.20e3))],
    "eel": [{"q1": a, "q2": b, "d": d, "E": e_el(a, b, d)} for a, b, d in ((1, -1, 0.283), (2, -2, 0.212), (1, -1, 0.319))],
    "photoelectric": [{"nm": 220.0, "phi": 7.18e-19, "KE": photon_energy_from_nm(220.0) - 7.18e-19}],
    "planckPeakNm5000": 2.897771955e-3 / 5000 * 1e9,
    "configs": {f"{z}:{q}": [[s, k] for s, k in ion_config(z, q)] for z, q in ((26, 0), (26, 2), (26, 3), (29, 0), (24, 0), (16, -2), (23, 3), (30, 2), (20, 0), (35, -1))},
    "unpaired": {f"{z}:{q}": unpaired(ion_config(z, q)) for z, q in ((6, 0), (7, 0), (8, 0), (25, 0), (26, 3), (22, 2))},
    "naming": ch4_data.naming_expected(),
    "fcBest": ch4_data.FC_EXPECTED_BEST,
    **ch5_data.expected(),
    **ch18_data.expected(),
}
(HERE / "expected_values.json").write_text(json.dumps(exp, indent=1), encoding="utf-8")

kinds = {}
for p in PROBLEMS:
    kinds[p["kind"]] = kinds.get(p["kind"], 0) + 1
print(f"data.js: {len(PROBLEMS)} problems {kinds}; {len(js) // 1024} KB")
print("scope.js:", len(scope_html), "chars of HTML")

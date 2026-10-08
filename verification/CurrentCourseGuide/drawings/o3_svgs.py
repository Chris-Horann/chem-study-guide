"""Generate two inline SVGs for src/t4-5.html in the style of lewis.svg():
(1) the ozone resonance hybrid as Day 9 p.10 draws it (solid + dashed bonds; 2 dots on the central O, 5 on each end O);
(2) the Day 9 p.9 curved arrows on O=O-O.
Writes o3_hybrid.svg and o3_arrows.svg (the markup pasted into src/t4-5.html) and PNG previews rendered with
PyMuPDF, next to this file. Run: py -3.11 verification/CurrentCourseGuide/drawings/o3_svgs.py"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import lewis as LW  # noqa: E402

OUT = os.path.dirname(os.path.abspath(__file__))
U = LW.UNIT
ATOMS = [("O", 0.0, 0.9), ("O", 1.05, 0.25), ("O", 2.1, 0.9)]
PAD = 0.9
X0 = min(a[1] for a in ATOMS) - PAD
X1 = max(a[1] for a in ATOMS) + PAD
Y0 = min(a[2] for a in ATOMS) - PAD
Y1 = max(a[2] for a in ATOMS) + PAD
W, H = (X1 - X0) * U, (Y1 - Y0) * U


def P(x, y):
    return ((x - X0) * U, (y - Y0) * U)


C = [P(a[1], a[2]) for a in ATOMS]
CX = sum(c[0] for c in C) / 3
CY = sum(c[1] for c in C) / 3


def line(x1, y1, x2, y2, dash=False):
    d = " stroke-dasharray='3 3'" if dash else ""
    return f"<line class='lw-bond'{d} x1='{x1:.1f}' y1='{y1:.1f}' x2='{x2:.1f}' y2='{y2:.1f}'/>"


def bond(i, j, kind):
    """kind: 'single', 'double', or 'hybrid' (solid outside + dashed toward the molecule's centre)."""
    (ax, ay), (bx, by) = C[i], C[j]
    L = math.hypot(bx - ax, by - ay)
    ux, uy = (bx - ax) / L, (by - ay) / L
    px, py = -uy, ux
    mx, my = (ax + bx) / 2, (ay + by) / 2
    inward = 1 if (CX - mx) * px + (CY - my) * py > 0 else -1
    sh = 12.5
    segs = {"single": [(0, False)], "double": [(-2.1, False), (2.1, False)],
            "hybrid": [(-2.1 * inward, False), (2.1 * inward, True)]}[kind]
    return "".join(line(ax + ux * sh + px * o, ay + uy * sh + py * o, bx - ux * sh + px * o, by - uy * sh + py * o, d) for o, d in segs)


def dots(k, pairs, singles):
    cx, cy = C[k]
    out = []
    for ang in pairs:
        t = math.radians(ang)
        dx, dy = math.cos(t), -math.sin(t)
        qx, qy = cx + dx * 15.5, cy + dy * 15.5
        ox, oy = -dy * 3.3, dx * 3.3
        out.append(f"<circle class='lw-dot' cx='{qx + ox:.1f}' cy='{qy + oy:.1f}' r='2.1'/><circle class='lw-dot' cx='{qx - ox:.1f}' cy='{qy - oy:.1f}' r='2.1'/>")
    for ang in singles:
        t = math.radians(ang)
        out.append(f"<circle class='lw-dot' cx='{cx + math.cos(t) * 15.5:.1f}' cy='{cy - math.sin(t) * 15.5:.1f}' r='2.1'/>")
    return "".join(out)


def atoms():
    return "".join(f"<text class='lw-atom' x='{cx:.1f}' y='{cy + 6.5:.1f}' text-anchor='middle'>O</text>" for cx, cy in C)


def wrap(body, aria, w=W, h=H, scale=0.85):
    return (f"<span class='lewis'><svg viewBox='0 0 {w:.0f} {h:.0f}' width='{w * scale:.0f}' height='{h * scale:.0f}' role='img' "
            f"aria-label='{aria}'>{body}</svg></span>")


# (1) the hybrid: central O one pair on top; each end O a single dot on top, pairs outside and below (as on the slide)
hyb = bond(0, 1, "hybrid") + bond(1, 2, "hybrid") + atoms() + dots(1, [90], []) + dots(0, [180, 270], [90]) + dots(2, [0, 270], [90])
HYB = wrap(hyb, "Resonance hybrid of ozone as drawn on Day 9 p.10: each O–O bond is a solid line plus a dashed line; one lone pair on the central O; five dots on each end O")


# (2) curved arrows on O=O–O (O3a: double bond left, three lone pairs on the right O)
def arrowhead(x, y, dx, dy, size=6.5):
    L = math.hypot(dx, dy)
    ux, uy = dx / L, dy / L
    px, py = -uy, ux
    b1 = (x - ux * size + px * size * 0.55, y - uy * size + py * size * 0.55)
    b2 = (x - ux * size - px * size * 0.55, y - uy * size - py * size * 0.55)
    return f"<path d='M{x:.1f} {y:.1f} L{b1[0]:.1f} {b1[1]:.1f} L{b2[0]:.1f} {b2[1]:.1f} Z' style='fill:#B42318'/>"


def curved(sx, sy, qx, qy, ex, ey):
    return (f"<path d='M{sx:.1f} {sy:.1f} Q{qx:.1f} {qy:.1f} {ex:.1f} {ey:.1f}' style='fill:none;stroke:#B42318;stroke-width:1.8'/>"
            + arrowhead(ex, ey, ex - qx, ey - qy))


O3 = LW.STRUCTS["O3a"]
lp_dirs = {k: LW._lp_directions(O3, k, O3.lp.get(k, 0)) for k in range(3)}
arr = bond(0, 1, "double") + bond(1, 2, "single") + atoms()
for k in range(3):
    arr += dots(k, lp_dirs[k], [])
# arrow 1: from the outer line of the double bond to the left O (the pair becomes a lone pair there)
(ax, ay), (bx, by) = C[0], C[1]
L = math.hypot(bx - ax, by - ay)
ux, uy = (bx - ax) / L, (by - ay) / L
px, py = -uy, ux
out_sgn = -1 if (CX - (ax + bx) / 2) * px + (CY - (ay + by) / 2) * py > 0 else 1
mx, my = (ax + bx) / 2 + px * out_sgn * 6, (ay + by) / 2 + py * out_sgn * 6
free = 115          # O0 lone pairs sit at 210 and 300 deg (lewis._lp_directions); the upper left is free
end1 = (ax + math.cos(math.radians(free)) * 14, ay - math.sin(math.radians(free)) * 14)
ctl1 = ((mx + end1[0]) / 2 + px * out_sgn * 18, (my + end1[1]) / 2 + py * out_sgn * 18)
arr += curved(mx, my, *ctl1, *end1)
# arrow 2: from the right O's upper lone pair into the O–O single bond
up = max(lp_dirs[2], key=lambda a: math.sin(math.radians(a)))
cx2, cy2 = C[2]
sx, sy = cx2 + math.cos(math.radians(up)) * 21, cy2 - math.sin(math.radians(up)) * 21
(ax, ay), (bx, by) = C[1], C[2]
L = math.hypot(bx - ax, by - ay)
ux, uy = (bx - ax) / L, (by - ay) / L
px, py = -uy, ux
out_sgn = -1 if (CX - (ax + bx) / 2) * px + (CY - (ay + by) / 2) * py > 0 else 1
ex, ey = (ax + bx) / 2 + px * out_sgn * 6, (ay + by) / 2 + py * out_sgn * 6
ctl2 = ((sx + ex) / 2 + px * out_sgn * 22, (sy + ey) / 2 + py * out_sgn * 22)
arr += curved(sx, sy, *ctl2, ex, ey)
ARR = wrap(arr, "Ozone, O=O–O, with two red curved arrows as on Day 9 p.9: one moves a pair of the double bond onto the left O; "
                "the other moves a lone pair of the right O into the O–O single bond")

open(os.path.join(OUT, "o3_hybrid.svg"), "w", encoding="utf-8").write(HYB)
open(os.path.join(OUT, "o3_arrows.svg"), "w", encoding="utf-8").write(ARR)

# previews (CSS classes inlined for the renderer)
import fitz  # noqa: E402
STYLE = ("<style>.lw-atom{font-family:serif;font-size:19px;fill:#17212E}.lw-bond{stroke:#17212E;stroke-width:1.8;stroke-linecap:round}"
         ".lw-dot{fill:#17212E}</style>")
for name, markup in (("o3_hybrid", HYB), ("o3_arrows", ARR)):
    svg = markup[markup.index("<svg"):markup.rindex("</svg>") + 6]
    svg = svg.replace("<svg ", "<svg xmlns='http://www.w3.org/2000/svg' ", 1).replace("role='img'", "")
    svg = svg.replace(">", ">" + STYLE, 1).replace("class='lw-bond'", "class='lw-bond' stroke='#17212E' stroke-width='1.8'")
    doc = fitz.open(stream=svg.encode("utf-8"), filetype="svg")
    pix = doc[0].get_pixmap(matrix=fitz.Matrix(3, 3), alpha=False)
    pix.save(os.path.join(OUT, name + ".png"))
print(len(HYB), len(ARR))

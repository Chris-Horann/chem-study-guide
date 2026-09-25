"""PDF inspection, rendering, and targeted lookup for course ingestion.

Run from the project root (C:\\Users\\chris\\ChemStudy) with Python 3.11:

    py -3.11 tools/render_pdf.py probe   "materials/lectures/Day 1 Lecture Slides.pdf" --summary
    py -3.11 tools/render_pdf.py render  "materials/lectures/Day 1 Lecture Slides.pdf" --pages 1-5,9
    py -3.11 tools/render_pdf.py render  "materials/notes/Week 2.pdf" --dpi 300
    py -3.11 tools/render_pdf.py crop    "materials/notes/Week 2.pdf" --page 4 --box 0.5,0,1,0.5
    py -3.11 tools/render_pdf.py text    "materials/lectures/Day 1 Lecture Slides.pdf" --print
    py -3.11 tools/render_pdf.py toc     materials/textbook/<book>.pdf --max-level 2
    py -3.11 tools/render_pdf.py labels  materials/textbook/<book>.pdf --pages 300-310
    py -3.11 tools/render_pdf.py search  materials/textbook/<book>.pdf "limiting reactant" "percent yield"

Page numbers are ALWAYS 1-based physical PDF pages (what a PDF viewer shows in
its page box), never printed page labels. `labels` maps between the two.

Outputs live beside the PDF in <pdf-stem>_pages/:
    page-001.png                     full-page renders (220 DPI default)
    crops/page-004_<box>_400dpi.png  high-DPI region zooms
    text/page-001.txt                extracted text layer (may be empty/garbled)
    render.json                      source sha256, DPI and content fingerprint per page

Renders are reused unless --force is given or a higher DPI is requested. If the
source file changes, only pages whose content fingerprint changed are discarded.
Pre-existing page-NNN.png files (e.g. from Render-CoursePDFs.ps1) are adopted.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

try:
    import pymupdf  # PyMuPDF >= 1.24
except ImportError:  # pragma: no cover
    try:
        import fitz as pymupdf  # type: ignore
    except ImportError:
        sys.exit("PyMuPDF is required: py -3.11 -m pip install pymupdf")

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DPI = 220


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.resolve().as_posix()


def pages_dir(pdf: Path) -> Path:
    return pdf.parent / f"{pdf.stem}_pages"


def page_name(p: int, page_count: int) -> str:
    return f"page-{p:0{max(3, len(str(page_count)))}d}"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def page_fingerprint(doc, p: int) -> str:
    """Hash of a page's content stream plus its embedded images (same as source_manifest)."""
    page = doc[p - 1]
    h = hashlib.sha256()
    try:
        h.update(page.read_contents() or b"")
    except Exception:
        pass
    for img in page.get_images(full=True):
        try:
            h.update(doc.xref_stream_raw(img[0]) or b"")
        except Exception:
            pass
    return h.hexdigest()[:16]


def parse_pages(spec: str | None, n: int) -> list[int]:
    """'1-3,7,10-' -> [1,2,3,7,10..n]. None/'all' -> all pages."""
    if not spec or spec.lower() == "all":
        return list(range(1, n + 1))
    pages: set[int] = set()
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            a, b = part.split("-", 1)
            pages.update(range(int(a) if a else 1, (int(b) if b else n) + 1))
        else:
            pages.add(int(part))
    bad = [p for p in pages if p < 1 or p > n]
    if bad:
        sys.exit(f"Page(s) out of range 1-{n}: {sorted(bad)}")
    return sorted(pages)


def compact_ranges(nums: list[int]) -> str:
    nums = sorted(nums)
    if not nums:
        return ""
    out, start, prev = [], nums[0], nums[0]
    for n in nums[1:]:
        if n == prev + 1:
            prev = n
            continue
        out.append(f"{start}-{prev}" if start != prev else f"{start}")
        start = prev = n
    out.append(f"{start}-{prev}" if start != prev else f"{start}")
    return ",".join(out)


def open_pdf(path_str: str):
    path = Path(path_str)
    if not path.is_absolute():
        path = Path.cwd() / path
    if not path.exists():
        sys.exit(f"Not found: {path_str}")
    return path, pymupdf.open(path)


# ---------------------------------------------------------------- probe

def page_profile(page) -> dict:
    text = page.get_text("text") or ""
    chars = len(text.strip())
    area = abs(page.rect) or 1.0
    img_area = 0.0
    images = page.get_images(full=True)
    for img in images:
        try:
            for r in page.get_image_rects(img[0]):
                img_area += abs(r & page.rect)
        except Exception:
            pass
    img_frac = min(img_area / area, 1.0)
    try:
        drawings = len(page.get_drawings())
    except Exception:
        drawings = 0
    # Replacement chars / private-use glyphs usually mean a broken text layer
    # (common with chemistry fonts: subscripts, arrows, Greek letters).
    odd = sum(1 for ch in text if ch == "\ufffd" or 0xE000 <= ord(ch) <= 0xF8FF)
    reasons = []
    if chars < 40:
        reasons.append("little/no text layer")
    if img_frac > 0.5:
        reasons.append(f"images cover {img_frac:.0%} of page")
    if drawings > 150:
        reasons.append(f"{drawings} vector drawing ops (diagram/graph/structure)")
    if odd:
        reasons.append(f"{odd} unmapped glyphs in text layer")
    return {
        "chars": chars,
        "words": len(text.split()),
        "images": len(images),
        "image_coverage": round(img_frac, 3),
        "drawings": drawings,
        "label": page.get_label() or None,
        "needs_visual": bool(reasons),
        "reasons": reasons,
    }


def cmd_probe(args):
    path, doc = open_pdf(args.pdf)
    pages = parse_pages(args.pages, doc.page_count)
    out = {
        "source": rel(path),
        "sha256": sha256_file(path),
        "page_count": doc.page_count,
        "has_toc": bool(doc.get_toc()),
        "metadata": {k: v for k, v in (doc.metadata or {}).items() if v},
        "pages": {p: page_profile(doc[p - 1]) for p in pages},
    }
    vis = [p for p, d in out["pages"].items() if d["needs_visual"]]
    out["summary"] = {
        "probed": len(pages),
        "needs_visual": len(vis),
        "needs_visual_pages": compact_ranges(vis),
        "note": "Flags are a minimum. Any page with chemistry notation still needs visual "
                "inspection; text layers routinely drop subscripts, charges, and arrows.",
    }
    if args.summary:
        out.pop("pages")
    print(json.dumps(out, indent=2, ensure_ascii=False))


# ---------------------------------------------------------------- render

def load_meta(d: Path) -> dict:
    f = d / "render.json"
    if f.exists():
        try:
            return json.loads(f.read_text(encoding="utf-8-sig"))
        except Exception:
            return {}
    return {}


def infer_dpi(png: Path, page) -> int:
    try:
        w = pymupdf.Pixmap(str(png)).width
        return round(w / (page.rect.width / 72))
    except Exception:
        return 0


def cmd_render(args):
    path, doc = open_pdf(args.pdf)
    pages = parse_pages(args.pages, doc.page_count)
    out_dir = pages_dir(path)
    out_dir.mkdir(parents=True, exist_ok=True)
    digest = sha256_file(path)
    meta = load_meta(out_dir)
    dpis = meta.get("pages", {})
    fps = meta.get("fingerprints", {})

    if meta.get("sha256") and meta["sha256"] != digest:
        # Source changed: keep only renders whose page fingerprint still matches.
        stale = []
        for key in list(dpis):
            p = int(key)
            if p > doc.page_count or fps.get(key) != page_fingerprint(doc, p):
                stale.append(p)
                dpis.pop(key, None)
                fps.pop(key, None)
                name = page_name(p, doc.page_count)
                stale_files = [out_dir / f"{name}.png", out_dir / "text" / f"{name}.txt",
                               *(out_dir / "crops").glob(f"{name}_*.png")]
                for f in stale_files:
                    if f.exists():
                        f.unlink()
        print(f"[source changed] discarded stale renders for pages: "
              f"{compact_ranges(stale) or 'none'}", file=sys.stderr)

    made, reused = [], []
    for p in pages:
        target = out_dir / f"{page_name(p, doc.page_count)}.png"
        key = str(p)
        if target.exists() and key not in dpis and not meta.get("sha256"):
            # Adopt a render made before render.json existed.
            dpis[key] = infer_dpi(target, doc[p - 1])
        if target.exists() and not args.force and dpis.get(key, 0) >= args.dpi - 2:
            fps.setdefault(key, page_fingerprint(doc, p))
            reused.append(target.name)
            continue
        doc[p - 1].get_pixmap(dpi=args.dpi, alpha=False).save(target)
        dpis[key] = args.dpi
        fps[key] = page_fingerprint(doc, p)
        made.append(target.name)

    order = lambda d: dict(sorted(d.items(), key=lambda kv: int(kv[0])))
    (out_dir / "render.json").write_text(json.dumps({
        "source": rel(path),
        "sha256": digest,
        "page_count": doc.page_count,
        "pages": order(dpis),
        "fingerprints": order(fps),
    }, indent=2), encoding="utf-8")
    print(json.dumps({"dir": rel(out_dir), "rendered": compact_ranges([int(n[5:-4]) for n in made]),
                      "reused": compact_ranges([int(n[5:-4]) for n in reused])}, indent=2))


def cmd_crop(args):
    """High-DPI zoom into a region to read small subscripts/charges/handwriting."""
    path, doc = open_pdf(args.pdf)
    if not 1 <= args.page <= doc.page_count:
        sys.exit(f"Page out of range 1-{doc.page_count}")
    x0, y0, x1, y1 = (float(v) for v in args.box.split(","))
    if not (0 <= x0 < x1 <= 1 and 0 <= y0 < y1 <= 1):
        sys.exit("--box must be fractions x0,y0,x1,y1 within 0..1 (x0<x1, y0<y1), origin top-left")
    page = doc[args.page - 1]
    r = page.rect
    clip = pymupdf.Rect(r.x0 + x0 * r.width, r.y0 + y0 * r.height,
                        r.x0 + x1 * r.width, r.y0 + y1 * r.height)
    out_dir = pages_dir(path) / "crops"
    out_dir.mkdir(parents=True, exist_ok=True)
    tag = f"{x0:g}-{y0:g}-{x1:g}-{y1:g}".replace(".", "")
    target = out_dir / f"{page_name(args.page, doc.page_count)}_{tag}_{args.dpi}dpi.png"
    page.get_pixmap(dpi=args.dpi, clip=clip, alpha=False).save(target)
    print(rel(target))


# ---------------------------------------------------------------- text

def cmd_text(args):
    path, doc = open_pdf(args.pdf)
    pages = parse_pages(args.pages, doc.page_count)
    out_dir = pages_dir(path) / "text"
    out_dir.mkdir(parents=True, exist_ok=True)
    for p in pages:
        t = doc[p - 1].get_text("text", sort=True)
        (out_dir / f"{page_name(p, doc.page_count)}.txt").write_text(t, encoding="utf-8")
        if args.print:
            print(f"===== {rel(path)} | PDF page {p} | label {doc[p - 1].get_label() or '-'} =====")
            print(t)
    if not args.print:
        print(json.dumps({"dir": rel(out_dir), "pages": compact_ranges(pages)}, indent=2))


# ---------------------------------------------------------------- textbook helpers

def cmd_toc(args):
    path, doc = open_pdf(args.pdf)
    toc = doc.get_toc(simple=True)
    if not toc:
        print("No embedded outline/bookmarks. Locate the printed table of contents "
              "(usually within the first ~25 PDF pages) with `text --print`, then use `labels`.")
        return
    for level, title, pdf_page in toc:
        if args.max_level and level > args.max_level:
            continue
        label = doc[pdf_page - 1].get_label() if 1 <= pdf_page <= doc.page_count else ""
        printed = f" (printed {label})" if label and label != str(pdf_page) else ""
        print(f"{'  ' * (level - 1)}{title}  ->  PDF p.{pdf_page}{printed}")


def cmd_labels(args):
    path, doc = open_pdf(args.pdf)
    has_any = False
    for p in parse_pages(args.pages, doc.page_count):
        label = doc[p - 1].get_label()
        has_any = has_any or bool(label)
        print(f"PDF p.{p}\tprinted: {label or '(no label)'}")
    if not has_any:
        print("\nNo page labels embedded. Determine the offset by reading the printed "
              "page number on a rendered page (printed = PDF - offset).", file=sys.stderr)


def cmd_search(args):
    path, doc = open_pdf(args.pdf)
    terms = [t.lower() for t in args.terms]
    results: dict[str, list[tuple[int, int]]] = {t: [] for t in terms}
    for p in parse_pages(args.pages, doc.page_count):
        text = re.sub(r"\s+", " ", (doc[p - 1].get_text("text") or "").lower())
        for t in terms:
            c = text.count(t)
            if c:
                results[t].append((p, c))
    for t in terms:
        hits = results[t]
        print(f'"{t}": {sum(c for _, c in hits)} hits on {len(hits)} pages')
        for p, c in sorted(sorted(hits, key=lambda x: -x[1])[: args.top]):
            label = doc[p - 1].get_label()
            lab = f" (printed {label})" if label and label != str(p) else ""
            print(f"    PDF p.{p}{lab}: {c}")
    print("\nSearch uses the text layer only; scanned pages will not match.", file=sys.stderr)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("probe", help="per-page text/image profile; flags pages needing visual inspection")
    s.add_argument("pdf"); s.add_argument("--pages"); s.add_argument("--summary", action="store_true")
    s.set_defaults(func=cmd_probe)

    s = sub.add_parser("render", help="render pages to PNG (cached, incremental)")
    s.add_argument("pdf"); s.add_argument("--pages"); s.add_argument("--dpi", type=int, default=DEFAULT_DPI)
    s.add_argument("--force", action="store_true")
    s.set_defaults(func=cmd_render)

    s = sub.add_parser("crop", help="high-DPI zoom of a page region (fractions of page)")
    s.add_argument("pdf"); s.add_argument("--page", type=int, required=True)
    s.add_argument("--box", required=True, help="x0,y0,x1,y1 as 0..1 fractions, origin top-left")
    s.add_argument("--dpi", type=int, default=400)
    s.set_defaults(func=cmd_crop)

    s = sub.add_parser("text", help="extract text layer to <pdf>_pages/text/")
    s.add_argument("pdf"); s.add_argument("--pages"); s.add_argument("--print", action="store_true")
    s.set_defaults(func=cmd_text)

    s = sub.add_parser("toc", help="embedded outline with PDF and printed pages")
    s.add_argument("pdf"); s.add_argument("--max-level", type=int, default=0)
    s.set_defaults(func=cmd_toc)

    s = sub.add_parser("labels", help="map PDF page numbers to printed page labels")
    s.add_argument("pdf"); s.add_argument("--pages")
    s.set_defaults(func=cmd_labels)

    s = sub.add_parser("search", help="find pages containing terms (text layer)")
    s.add_argument("pdf"); s.add_argument("terms", nargs="+"); s.add_argument("--pages")
    s.add_argument("--top", type=int, default=12)
    s.set_defaults(func=cmd_search)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()

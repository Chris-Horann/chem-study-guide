"""Source change detection for materials/ using SHA-256.

Run from the project root (C:\\Users\\chris\\ChemStudy) with Python 3.11:

    py -3.11 tools/source_manifest.py status            # what needs work (read-only)
    py -3.11 tools/source_manifest.py status --json
    py -3.11 tools/source_manifest.py diff  "materials/lectures/Day 3 Lecture Slides.pdf"
    py -3.11 tools/source_manifest.py mark  "materials/lectures/Day 3 Lecture Slides.pdf" --status ingested
    py -3.11 tools/source_manifest.py mark  "materials/lectures/Day 4 Lecture Slides.pdf" --status partial --pages 1-9
    py -3.11 tools/source_manifest.py mark  materials/textbook/<book>.pdf --status mapped --pages 120-131 --note "Sec 3.4-3.6"
    py -3.11 tools/source_manifest.py forget materials/lectures/old.pdf

State lives in materials/SOURCE_MANIFEST.json. `status` and `diff` never write.
Only `mark` and `forget` modify the manifest, so a file is recorded as processed
only after its content has actually been written into the indexes. (There is
deliberately no "commit everything" command.)

Statuses you can mark:
    ingested  fully processed into the indexes (all pages unless --pages given)
    partial   some pages processed (use --pages; accumulates across calls)
    mapped    textbook: only the listed pages were consulted/mapped (accumulates)
    skipped   intentionally not processed (duplicate, syllabus boilerplate, ...)

Derived states reported by `status`:
    new        on disk, never recorded
    changed    recorded, but the SHA-256 differs from when it was processed
    moved      new path whose content matches a recorded file that is gone
               (no re-ingest: `mark` the new path, `forget` the old one)
    partial    recorded as partial (continue the remaining pages)
    missing    recorded, but no longer on disk
    unchanged  nothing to do (textbook `mapped` files count as unchanged)

Ignored: <pdf>_pages/ render folders, Office lock files (~$*), desktop.ini,
Thumbs.db, and file types outside SOURCE_SUFFIXES (reported as "unsupported").
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MATERIALS = ROOT / "materials"
MANIFEST = MATERIALS / "SOURCE_MANIFEST.json"
CATEGORIES = ["lectures", "notes", "homework", "review", "textbook", "images"]
SOURCE_SUFFIXES = {".pdf", ".png", ".jpg", ".jpeg", ".webp", ".heic", ".gif",
                   ".txt", ".md", ".docx", ".pptx", ".xlsx", ".csv"}
IGNORE_NAMES = {"desktop.ini", "thumbs.db", ".ds_store"}
SCHEMA_VERSION = 2
ABOUT = ("Maintained by tools/source_manifest.py (mark/forget). Do not hand-edit entries. "
         "Keys are project-relative POSIX paths under materials/. Entry fields: category, "
         "sha256, size, status (ingested|partial|mapped|skipped), processed_at, pages_done, "
         "page_count, page_hashes (non-textbook PDFs), render_dir, indexes, notes.")


def now() -> str:
    return dt.datetime.now().astimezone().isoformat(timespec="seconds")


def rel(p: Path) -> str:
    return p.resolve().relative_to(ROOT).as_posix()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load() -> dict:
    # utf-8-sig: tolerate a BOM written by Windows PowerShell.
    text = MANIFEST.read_text(encoding="utf-8-sig") if MANIFEST.exists() else ""
    data = json.loads(text) if text.strip() else {}
    data.setdefault("sources", {})
    return data


def save(data: dict):
    out = {"version": SCHEMA_VERSION, "_about": ABOUT, "updated": now(),
           "sources": dict(sorted(data["sources"].items()))}
    tmp = MANIFEST.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    tmp.replace(MANIFEST)


def ignored(f: Path) -> bool:
    parts = f.relative_to(MATERIALS).parts
    return (any(p.endswith("_pages") for p in parts[:-1])
            or f.name.lower() in IGNORE_NAMES or f.name.startswith("~$"))


def scan() -> tuple[dict[str, Path], list[str]]:
    found, unsupported = {}, []
    for cat in CATEGORIES:
        d = MATERIALS / cat
        if not d.exists():
            continue
        for f in d.rglob("*"):
            if not f.is_file() or ignored(f):
                continue
            if f.suffix.lower() in SOURCE_SUFFIXES:
                found[rel(f)] = f
            else:
                unsupported.append(rel(f))
    return found, unsupported


def parse_pages(spec: str | None) -> list[int]:
    if not spec:
        return []
    out: set[int] = set()
    for part in spec.split(","):
        part = part.strip()
        if "-" in part:
            a, b = part.split("-", 1)
            out.update(range(int(a), int(b) + 1))
        elif part:
            out.add(int(part))
    return sorted(out)


def compact(nums) -> str:
    nums = sorted(set(nums))
    if not nums:
        return ""
    out, s, p = [], nums[0], nums[0]
    for n in nums[1:]:
        if n == p + 1:
            p = n
            continue
        out.append(f"{s}-{p}" if s != p else str(s))
        s = p = n
    out.append(f"{s}-{p}" if s != p else str(s))
    return ",".join(out)


def pdf_info(path: Path, page_hashes: bool) -> dict:
    """Page count and optional per-page fingerprints (content stream + embedded images)."""
    if path.suffix.lower() != ".pdf":
        return {}
    try:
        import pymupdf
    except ImportError:
        try:
            import fitz as pymupdf  # type: ignore
        except ImportError:
            return {}
    info: dict = {}
    with pymupdf.open(path) as doc:
        info["page_count"] = doc.page_count
        if page_hashes:
            hashes = []
            for page in doc:
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
                hashes.append(h.hexdigest()[:16])
            info["page_hashes"] = hashes
    return info


def classify(data: dict):
    on_disk, unsupported = scan()
    recorded = data["sources"]
    recorded_by_hash = {v.get("sha256"): k for k, v in recorded.items()}
    groups: dict[str, list[dict]] = {k: [] for k in
                                     ["new", "changed", "moved", "partial", "missing", "unchanged"]}
    for path, f in sorted(on_disk.items()):
        digest = sha256_file(f)
        entry = recorded.get(path)
        item = {"path": path, "category": path.split("/")[1], "size": f.stat().st_size}
        if entry is None:
            old = recorded_by_hash.get(digest)
            if old and old not in on_disk:
                groups["moved"].append({**item, "from": old})
            else:
                groups["new"].append(item)
        elif entry.get("sha256") != digest:
            groups["changed"].append({**item, "status_before": entry.get("status")})
        elif entry.get("status") == "partial":
            groups["partial"].append({**item, "pages_done": entry.get("pages_done", ""),
                                      "page_count": entry.get("page_count")})
        else:
            groups["unchanged"].append({**item, "status": entry.get("status")})
    for path in sorted(set(recorded) - set(on_disk)):
        groups["missing"].append({"path": path, "status": recorded[path].get("status")})
    return groups, unsupported


def cmd_status(args):
    data = load()
    groups, unsupported = classify(data)
    if args.json:
        print(json.dumps({**groups, "unsupported": unsupported}, indent=2, ensure_ascii=False))
        return
    todo = sum(len(groups[k]) for k in ("new", "changed", "moved", "partial", "missing"))
    print(f"Manifest: {rel(MANIFEST)}  ({len(data['sources'])} recorded)")
    for key in ["new", "changed", "moved", "partial", "missing"]:
        if groups[key]:
            print(f"\n{key.upper()} ({len(groups[key])})")
            for it in groups[key]:
                extra = ""
                if key == "moved":
                    extra = f"  <- same content as {it['from']}"
                elif key == "partial":
                    extra = f"  done: {it['pages_done'] or '-'} of {it.get('page_count') or '?'}"
                elif key == "changed":
                    extra = f"  (was {it['status_before']}; run `diff` for changed pages)"
                print(f"  {it['path']}{extra}")
    if unsupported:
        print(f"\nUNSUPPORTED file types (not tracked): {', '.join(unsupported)}")
    print(f"\nUNCHANGED: {len(groups['unchanged'])}")
    print("Nothing to ingest." if todo == 0 else f"{todo} item(s) need attention.")


def cmd_diff(args):
    data = load()
    path = Path(args.path)
    key = rel(path if path.is_absolute() else ROOT / path)
    entry = data["sources"].get(key)
    if not entry:
        sys.exit(f"{key} is not recorded; treat the whole file as new.")
    f = ROOT / key
    if not f.exists():
        sys.exit(f"{key} is missing on disk.")
    if sha256_file(f) == entry.get("sha256"):
        print("File unchanged.")
        return
    old = entry.get("page_hashes")
    if not old:
        print("File changed; no per-page fingerprints were recorded, so re-check every page.")
        return
    new = pdf_info(f, page_hashes=True).get("page_hashes", [])
    changed = [i + 1 for i in range(max(len(old), len(new)))
               if i >= len(old) or i >= len(new) or old[i] != new[i]]
    print(json.dumps({
        "path": key, "old_page_count": len(old), "new_page_count": len(new),
        "changed_or_added_pages": compact(p for p in changed if p <= len(new)),
        "removed_pages": compact(p for p in changed if p > len(new)),
        "note": "A page insertion shifts every later page; if many consecutive pages "
                "differ, compare renders visually to find the true edits.",
    }, indent=2))


def cmd_mark(args):
    data = load()
    path = Path(args.path)
    f = path if path.is_absolute() else ROOT / path
    if not f.exists():
        sys.exit(f"Not found: {args.path}")
    key = rel(f)
    parts = key.split("/")
    if parts[0] != "materials" or len(parts) < 3 or parts[1] not in CATEGORIES:
        sys.exit(f"{key} is not inside materials/<{'|'.join(CATEGORIES)}>/")
    prev = data["sources"].get(key, {})
    digest = sha256_file(f)
    category = parts[1]
    # Per-page fingerprints are cheap for course PDFs; skipped for large textbooks.
    info = pdf_info(f, page_hashes=category != "textbook")

    pages = parse_pages(args.pages)
    done = set(parse_pages(prev.get("pages_done"))) if prev.get("sha256") == digest else set()
    if args.status in ("partial", "mapped"):
        done.update(pages)
    elif args.status == "ingested":
        done = set(pages) if pages else set(range(1, info.get("page_count", 0) + 1))

    entry = {
        "category": category,
        "sha256": digest,
        "size": f.stat().st_size,
        "status": args.status,
        "first_seen": prev.get("first_seen", now()),
        "processed_at": now(),
        "pages_done": compact(done),
        **info,
    }
    render_dir = f.parent / f"{f.stem}_pages"
    if render_dir.is_dir():
        entry["render_dir"] = rel(render_dir)
    indexes = set(prev.get("indexes", []))
    if args.indexes:
        indexes |= {s.strip() for s in args.indexes.split(",") if s.strip()}
    if indexes:
        entry["indexes"] = sorted(indexes)
    notes = list(prev.get("notes", []))
    if args.note:
        notes.append(f"{now()[:10]}: {args.note}")
    if notes:
        entry["notes"] = notes
    data["sources"][key] = entry
    save(data)
    print(f"Recorded {key}: {args.status}, pages {entry['pages_done'] or '-'}")


def cmd_forget(args):
    data = load()
    key = Path(args.path).as_posix()
    if key not in data["sources"]:
        sys.exit(f"{key} not in manifest")
    del data["sources"][key]
    save(data)
    print(f"Removed {key} from manifest")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("status", help="report new/changed/moved/partial/missing (read-only)")
    s.add_argument("--json", action="store_true"); s.set_defaults(func=cmd_status)
    s = sub.add_parser("diff", help="which PDF pages changed since processing (read-only)")
    s.add_argument("path"); s.set_defaults(func=cmd_diff)
    s = sub.add_parser("mark", help="record a file as processed AFTER the indexes are updated")
    s.add_argument("path")
    s.add_argument("--status", required=True, choices=["ingested", "partial", "mapped", "skipped"])
    s.add_argument("--pages", help="PDF pages processed, e.g. 1-12,15")
    s.add_argument("--note")
    s.add_argument("--indexes", help="comma list of files updated, e.g. COURSE_INDEX,COURSE_MAP")
    s.set_defaults(func=cmd_mark)
    s = sub.add_parser("forget", help="drop a manifest entry (e.g. after a move or deletion)")
    s.add_argument("path"); s.set_defaults(func=cmd_forget)
    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()

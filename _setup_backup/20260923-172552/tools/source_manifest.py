from pathlib import Path
import hashlib
import json
import sys
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "materials" / "SOURCE_MANIFEST.json"

SOURCE_DIRS = [
    ROOT / "materials" / "lectures",
    ROOT / "materials" / "notes",
    ROOT / "materials" / "homework",
    ROOT / "materials" / "review",
    ROOT / "materials" / "textbook",
    ROOT / "materials" / "images",
]

VALID_SUFFIXES = {
    ".pdf", ".png", ".jpg", ".jpeg", ".webp",
    ".txt", ".md", ".docx", ".pptx"
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        while True:
            block = file.read(1024 * 1024)
            if not block:
                break
            digest.update(block)
    return digest.hexdigest()


def load_manifest():
    if not MANIFEST.exists():
        return {"version": 1, "sources": {}}
    return json.loads(MANIFEST.read_text(encoding="utf-8-sig"))


def save_manifest(data):
    MANIFEST.write_text(
        json.dumps(data, indent=2),
        encoding="utf-8"
    )


def scan():
    manifest = load_manifest()
    old_sources = manifest.get("sources", {})
    current = {}
    changes = []

    for directory in SOURCE_DIRS:
        if not directory.exists():
            continue

        for path in directory.rglob("*"):
            if not path.is_file():
                continue
            if path.suffix.lower() not in VALID_SUFFIXES:
                continue
            if path.parent.name.endswith("_pages"):
                continue

            relative = path.relative_to(ROOT).as_posix()
            stat = path.stat()
            hash_value = sha256_file(path)

            entry = {
                "path": relative,
                "size": stat.st_size,
                "mtime": stat.st_mtime,
                "sha256": hash_value,
            }

            current[relative] = entry

            previous = old_sources.get(relative)
            if previous is None:
                changes.append(("NEW", relative))
            elif previous.get("sha256") != hash_value:
                changes.append(("CHANGED", relative))

    for previous_path in old_sources:
        if previous_path not in current:
            changes.append(("REMOVED", previous_path))

    return current, changes, manifest


def main():
    current, changes, manifest = scan()

    print("ChemStudy source scan")
    print("=====================")

    if not changes:
        print("No source changes detected.")
    else:
        for status, path in changes:
            print(f"{status:8} {path}")

    if "--commit" in sys.argv:
        manifest["sources"] = current
        manifest["last_scan_utc"] = datetime.now(timezone.utc).isoformat()
        save_manifest(manifest)
        print("\nManifest updated.")
    else:
        print("\nDry run only. Use --commit to update SOURCE_MANIFEST.json.")


if __name__ == "__main__":
    main()

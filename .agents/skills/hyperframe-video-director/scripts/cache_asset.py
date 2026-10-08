#!/usr/bin/env python3
"""Register a downloaded asset into the project asset cache."""

from __future__ import annotations

import argparse
import hashlib
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _util import die, ensure_dir, resolve_project, which, write_json  # noqa: E402


KINDS = {"images", "videos", "icons", "screenshots"}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def query_key(query: str) -> str:
    return hashlib.sha256(query.strip().lower().encode("utf-8")).hexdigest()[:16]


def probe_dimensions(path: Path) -> list[int] | None:
    if not which("ffprobe"):
        return None
    import json
    import subprocess

    r = subprocess.run(
        [
            "ffprobe",
            "-v",
            "quiet",
            "-print_format",
            "json",
            "-show_streams",
            str(path),
        ],
        capture_output=True,
        text=True,
    )
    if r.returncode != 0:
        return None
    data = json.loads(r.stdout)
    for s in data.get("streams", []):
        if s.get("width") and s.get("height"):
            return [int(s["width"]), int(s["height"])]
    return None


def find_cached(meta_dir: Path, query: str) -> Path | None:
    key = query_key(query)
    for meta in meta_dir.glob("*.json"):
        try:
            import json

            data = json.loads(meta.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001
            continue
        if data.get("query_key") == key and data.get("file"):
            p = Path(data["file"])
            if not p.is_absolute():
                # resolve later by caller
                return meta
            if p.is_file():
                return meta
    return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True)
    parser.add_argument("--file", required=True, help="Source file to cache")
    parser.add_argument("--query", required=True)
    parser.add_argument("--kind", default="images", choices=sorted(KINDS))
    parser.add_argument("--usage", action="append", default=[], help="e.g. scene_01 (repeatable)")
    parser.add_argument("--source", default="")
    parser.add_argument("--reuse-only", action="store_true", help="Only look up cache; do not copy")
    args = parser.parse_args()

    project = resolve_project(args.project)
    meta_dir = ensure_dir(project / "assets" / "metadata")
    kind_dir = ensure_dir(project / "assets" / args.kind)

    existing = find_cached(meta_dir, args.query)
    if existing:
        import json

        data = json.loads(existing.read_text(encoding="utf-8"))
        rel = data.get("file", "")
        abs_path = (project / rel).resolve() if not Path(rel).is_absolute() else Path(rel)
        if abs_path.is_file():
            usages = list(dict.fromkeys([*(data.get("usage") or []), *args.usage]))
            data["usage"] = usages
            write_json(existing, data)
            print(f"cache hit: {rel}")
            return 0
        if args.reuse_only:
            die(f"cache entry missing file: {rel}")

    if args.reuse_only:
        die(f"no cache entry for query: {args.query}")

    src = Path(args.file).expanduser().resolve()
    if not src.is_file():
        die(f"file not found: {src}")

    digest = sha256_file(src)[:16]
    dest_name = f"{query_key(args.query)}_{digest}{src.suffix.lower()}"
    dest = kind_dir / dest_name
    if not dest.exists():
        shutil.copy2(src, dest)

    rel = dest.relative_to(project).as_posix()
    dims = probe_dimensions(dest)
    meta = {
        "file": rel,
        "source": args.source or str(src),
        "query": args.query,
        "query_key": query_key(args.query),
        "kind": args.kind,
        "dimensions": dims,
        "usage": args.usage,
        "sha256": sha256_file(dest),
        "cached_at": datetime.now(timezone.utc).isoformat(),
    }
    meta_path = meta_dir / f"{query_key(args.query)}.json"
    write_json(meta_path, meta)
    print(f"cached: {rel}")
    print(f"meta: {meta_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

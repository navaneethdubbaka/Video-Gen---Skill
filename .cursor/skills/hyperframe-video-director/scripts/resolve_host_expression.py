#!/usr/bin/env python3
"""Resolve greencode host GIF paths from greencode/my_animations/catalog.json."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _util import die  # noqa: E402


def workspace_root() -> Path:
    # scripts/ -> skill -> skills -> .cursor -> workspace
    return Path(__file__).resolve().parents[4]


def catalog_path(explicit: Path | None = None) -> Path:
    if explicit is not None:
        return explicit.expanduser().resolve()
    return workspace_root() / "greencode" / "my_animations" / "catalog.json"


def load_catalog(path: Path) -> dict:
    if not path.is_file():
        die(f"catalog not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def resolve_expression(catalog: dict, expression: str, catalog_file: Path) -> dict:
    expr = expression.strip().lower()
    entries = catalog.get("expressions") or []
    by_id = {str(e.get("id", "")).lower(): e for e in entries}
    entry = by_id.get(expr)
    if entry is None:
        # tag fallback
        for e in entries:
            tags = [str(t).lower() for t in (e.get("tags") or [])]
            if expr in tags:
                entry = e
                break
    if entry is None:
        # named fallbacks
        for fid in catalog.get("fallback_order") or ["talk_loop", "idle_bob"]:
            if fid.lower() in by_id:
                entry = by_id[fid.lower()]
                break
    if entry is None:
        die(f"unknown expression {expression!r}; known: {sorted(by_id)}")

    mode = str(catalog.get("mode") or "")
    # Prefer talking webp when catalog is talking_primary; fall back to gif then still
    candidates = []
    if mode == "talking_primary":
        # Prefer GIF for reliable 1x mouth timing in HyperFrames; webp second
        prefer = str((catalog.get("playback") or {}).get("prefer") or "talking_loop.gif")
        if prefer.endswith(".gif"):
            order = ("file_gif", "file", "still_file")
        else:
            order = ("file", "file_gif", "still_file")
        for key in order:
            rel = entry.get(key)
            if rel and rel not in candidates:
                candidates.append(rel)
    else:
        candidates.append(entry.get("file") or entry.get("still_file"))

    chosen = None
    abs_path = None
    for rel in candidates:
        if not rel:
            continue
        p = (catalog_file.parent / rel).resolve()
        if p.is_file():
            chosen = rel
            abs_path = p
            break
    if chosen is None:
        rel = entry.get("file") or entry.get("still_file") or ""
        abs_path = (catalog_file.parent / rel).resolve()
        chosen = rel

    return {
        "id": entry.get("id"),
        "file_rel": f"greencode/my_animations/{chosen}".replace("\\", "/"),
        "file_abs": str(abs_path),
        "exists": abs_path.is_file() if abs_path else False,
        "still_file": entry.get("still_file"),
        "tags": entry.get("tags") or [],
        "facing": entry.get("facing"),
        "loop": bool(entry.get("loop", True)),
        "preferred_patterns": entry.get("preferred_patterns") or [],
        "chroma_key": (catalog.get("chroma_key") or {}).get("color", "#00FF00"),
        "mode": mode,
    }


def validate(catalog: dict, catalog_file: Path) -> int:
    ok = True
    for e in catalog.get("expressions") or []:
        p = (catalog_file.parent / e["file"]).resolve()
        status = "OK" if p.is_file() else "MISSING"
        if status != "OK":
            ok = False
        print(f"{status}\t{e.get('id')}\t{p}")
    return 0 if ok else 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", type=Path, default=None, help="Path to catalog.json")
    parser.add_argument("--expression", "-e", help="Expression id or tag to resolve")
    parser.add_argument("--list", action="store_true", help="List catalog entries")
    parser.add_argument("--validate", action="store_true", help="Check all host files exist")
    parser.add_argument("--json", action="store_true", help="Print resolve result as JSON")
    args = parser.parse_args()

    cat_file = catalog_path(args.catalog)
    catalog = load_catalog(cat_file)

    if args.list:
        for e in catalog.get("expressions") or []:
            print(f"{e.get('id')}\t{e.get('file')}\ttags={','.join(e.get('tags') or [])}")
        return 0

    if args.validate:
        return validate(catalog, cat_file)

    if not args.expression:
        die("pass --expression, --list, or --validate")

    result = resolve_expression(catalog, args.expression, cat_file)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(result["file_rel"])
        if not result["exists"]:
            print(f"WARNING: file missing: {result['file_abs']}", file=sys.stderr)
            return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

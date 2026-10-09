#!/usr/bin/env python3
"""Patch storyboard.json visual.asset_path from analysis/entity-assets.json."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _util import die, read_json, resolve_project, write_json  # noqa: E402


def apply(project: Path, force: bool = False) -> int:
    sb_path = project / "storyboard" / "storyboard.json"
    ea_path = project / "analysis" / "entity-assets.json"
    if not sb_path.is_file():
        die(f"missing {sb_path}")
    if not ea_path.is_file():
        die(f"missing {ea_path} - run fetch_entity_image.py first")

    sb = read_json(sb_path)
    ea = read_json(ea_path)
    scenes = sb.get("scenes") or []

    # Map scene_id -> best entity asset (later entities in file win on overlap)
    by_scene: dict[int, dict] = {}
    by_name: dict[str, dict] = {}
    for ent in ea.get("entities") or []:
        if not ent.get("ok") or not ent.get("asset_path"):
            continue
        by_name[ent["name"].strip().lower()] = ent
        for sid in ent.get("scene_ids") or []:
            by_scene[int(sid)] = ent

    updated = 0
    for scene in scenes:
        sid = int(scene.get("scene_id") or 0)
        visual = scene.setdefault("visual", {})
        ent_name = (
            visual.get("entity")
            or (visual.get("requirement") or {}).get("entity")
            or scene.get("entity")
        )
        ent = None
        if ent_name:
            ent = by_name.get(str(ent_name).strip().lower())
        if ent is None:
            ent = by_scene.get(sid)
        if ent is None:
            continue

        existing = (visual.get("asset_path") or "").strip().replace("\\", "/")
        tagged = bool(visual.get("entity") or (visual.get("requirement") or {}).get("entity") or sid in by_scene)
        if existing and not force and not tagged and "entities/" not in existing:
            continue

        visual["asset_path"] = ent["asset_path"]
        visual["entity"] = ent["name"]
        if (visual.get("type") or "").lower() in ("", "generated_graphic", "text_only"):
            visual["type"] = "photograph" if ent.get("type") == "person" else "icon"
        req = visual.setdefault("requirement", {})
        req["entity"] = ent["name"]
        req["entity_type"] = ent.get("type")
        req.setdefault("subject", ent["name"])
        req.setdefault("narration_link", scene.get("narration") or ent["name"])
        if not (visual.get("search_query") or "").strip():
            visual["search_query"] = f"{ent['name']} {ent.get('type', '')} official photo".strip()
        updated += 1

    write_json(sb_path, sb)
    print(f"patched {updated} scene(s) in {sb_path}")
    return updated


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True)
    parser.add_argument("--force", action="store_true", help="overwrite existing non-entity asset_path")
    args = parser.parse_args()
    n = apply(resolve_project(args.project), force=args.force)
    return 0 if n >= 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())

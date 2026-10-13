#!/usr/bin/env python3
"""
Romanize Telugu caption words to Latin spellings and rebuild karaoke captions.html.

Run AFTER faceless captions.mjs build:

  python prepare_captions.py --project <PROJECT> [--skin <path>]

Defaults:
  - reads composition/hyperframes/caption_groups.json
  - writes romanized caption_groups.json
  - fills styles/insider-force-short/caption-skin.html (or --skin)
  - writes compositions/captions.html
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR))

from telugu_romanize import has_telugu, romanize_text  # noqa: E402


DEFAULT_SKIN = SKILL_DIR / "styles" / "insider-force-short" / "caption-skin.html"


def _project_hf(project: Path) -> Path:
    hf = project / "composition" / "hyperframes"
    if not hf.is_dir():
        raise SystemExit(f"missing HyperFrames dir: {hf}")
    return hf


def romanize_groups(data: dict) -> tuple[dict, int]:
    changed = 0
    groups = data.get("groups") or []
    for g in groups:
        words = g.get("words") or []
        for w in words:
            raw = str(w.get("text") or "")
            if has_telugu(raw):
                w["text"] = romanize_text(raw)
                changed += 1
        # rebuild group text from words
        g["text"] = " ".join(str(w.get("text") or "") for w in words).strip()
    return data, changed


def fill_skin(skin: str, groups: list, total: float, width: int, height: int) -> str:
    out = skin
    # strip HTML comments (same rationale as captions.mjs)
    prev = None
    while prev != out:
        prev = out
        out = re.sub(r"<!--[\s\S]*?-->", "", out)

    def one(pattern: str, repl: str, label: str) -> None:
        nonlocal out
        matches = list(re.finditer(pattern, out))
        if len(matches) != 1:
            raise SystemExit(f"caption skin: expected one {label}, found {len(matches)}")
        out = re.sub(pattern, repl, out, count=1)

    tokens = (
        ":root {\n"
        "  --cap-ink: #ffffff;\n"
        "  --cap-canvas: #0c0c0e;\n"
        "  --cap-accent: #5efc8d;\n"
        "  --cap-accent-2: #8a8a8a;\n"
        '  --font-display: "Space Grotesk", "Helvetica Neue", sans-serif;\n'
        '  --font-body: "Space Grotesk", "Helvetica Neue", sans-serif;\n'
        f"  --cap-band-top: {int(height * 0.875)}px;\n"
        f"  --cap-band-height: {int(height * 0.115)}px;\n"
        "}"
    )
    one(
        r"<style data-brand-tokens>\s*</style>",
        f"<style data-brand-tokens>\n{tokens}\n</style>",
        "brand-tokens hole",
    )

    payload = json.dumps(groups, ensure_ascii=False).replace("<", "\\u003c")
    one(r"var GROUPS = \[\];", f"var GROUPS = {payload};", "GROUPS hole")
    one(r"var DURATION = 0;", f"var DURATION = {total};", "DURATION hole")
    one(r'data-duration="0"', f'data-duration="{total}"', "data-duration")
    one(r'data-width="0"', f'data-width="{width}"', "data-width")
    one(r'data-height="0"', f'data-height="{height}"', "data-height")

    return (
        f'<template id="captions-template" data-composition-id="captions" '
        f'data-width="{width}" data-height="{height}">\n'
        f"{out.strip()}\n"
        f"</template>\n"
    )


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--project", required=True, type=Path)
    ap.add_argument("--skin", type=Path, default=None, help="caption-skin.html path")
    ap.add_argument("--skip-romanize", action="store_true")
    args = ap.parse_args()

    hf = _project_hf(args.project.resolve())
    groups_path = hf / "caption_groups.json"
    if not groups_path.is_file():
        raise SystemExit(f"missing {groups_path} — run captions.mjs build first")

    data = json.loads(groups_path.read_text(encoding="utf-8"))
    changed = 0
    if not args.skip_romanize:
        data, changed = romanize_groups(data)
        groups_path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    skin_path = args.skin or DEFAULT_SKIN
    if not skin_path.is_file():
        raise SystemExit(f"missing caption skin: {skin_path}")

    skin = skin_path.read_text(encoding="utf-8")
    total = float(data.get("total_duration_s") or 0)
    width = int(data.get("width") or 1080)
    height = int(data.get("height") or 1920)
    groups = data.get("groups") or []

    html = fill_skin(skin, groups, total, width, height)
    out_path = hf / "compositions" / "captions.html"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html, encoding="utf-8")

    # also stage skin for future captions.mjs rebuilds
    staged = hf / ".hyperframes" / "caption-skin.html"
    staged.parent.mkdir(parents=True, exist_ok=True)
    staged.write_text(skin_path.read_text(encoding="utf-8"), encoding="utf-8")

    telugu_left = sum(
        1
        for g in groups
        for w in (g.get("words") or [])
        if has_telugu(str(w.get("text") or ""))
    )
    print(
        f"prepare_captions: romanized {changed} word(s); "
        f"telugu_remaining={telugu_left}; wrote {out_path}"
    )
    if telugu_left:
        raise SystemExit("Telugu script still present in captions after romanize")


if __name__ == "__main__":
    main()

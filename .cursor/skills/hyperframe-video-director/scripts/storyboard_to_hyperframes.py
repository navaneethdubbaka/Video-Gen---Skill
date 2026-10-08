#!/usr/bin/env python3
"""Convert storyboard.json → STORYBOARD.md + SCRIPT.md for HyperFrames."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _util import die, ensure_dir, read_json, resolve_project  # noqa: E402


def slugify(s: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9]+", "-", (s or "scene").lower()).strip("-")
    return (s[:40] or "scene")


def map_transition(t: str | None) -> str:
    if not t:
        return "cut"
    t = t.lower().replace("-", "_")
    if t in ("hard_cut", "cut", "hard"):
        return "cut"
    if "fade" in t or "dissolve" in t or "cross" in t:
        return "crossfade"
    if "wipe" in t:
        return "wipe"
    return "cut"


def aspect_to_format(project: Path, storyboard: dict) -> str:
    style_path = project / (storyboard.get("style_spec_path") or "analysis/style-spec.json")
    if style_path.is_file():
        style = read_json(style_path)
        fmt = style.get("format") or {}
        w, h = fmt.get("width"), fmt.get("height")
        if w and h:
            return f"{w}x{h}"
        ar = fmt.get("aspect_ratio") or ""
        if ar in ("9:16", "9/16"):
            return "1080x1920"
        if ar in ("1:1", "1/1"):
            return "1080x1080"
        if ar in ("16:9", "16/9"):
            return "1920x1080"
    return "1080x1920"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True)
    parser.add_argument("--storyboard", default=None)
    args = parser.parse_args()

    project = resolve_project(args.project)
    sb_path = Path(args.storyboard) if args.storyboard else project / "storyboard" / "storyboard.json"
    if not sb_path.is_file():
        die(f"storyboard not found: {sb_path}")

    sb = read_json(sb_path)
    hf = ensure_dir(project / "composition" / "hyperframes")
    scenes = sb.get("scenes") or []
    if not scenes:
        die("no scenes in storyboard")

    fmt = aspect_to_format(project, sb)
    message = sb.get("message") or "Director short"
    lang = sb.get("language") or "en"

    lines = [
        "---",
        f"format: {fmt}",
        f'message: "{message.replace(chr(34), chr(39))}"',
        "arc: Hook → Develop → Payoff",
        f"audience: short-form viewers",
        "mode: autonomous",
        f"language: {lang}",
        "---",
        "",
    ]

    script_lines = [
        f"# Script — {sb.get('project') or project.name}",
        "",
        "> Captions / reference only. Do **not** TTS — user voiceover is authoritative.",
        "",
    ]

    for scene in scenes:
        sid = int(scene["scene_id"])
        start = float(scene["start"])
        end = float(scene["end"])
        dur = max(0.1, end - start)
        title = (scene.get("text") or {}).get("content") or scene.get("concept") or f"Scene {sid}"
        title_one = title.replace("\n", " ").strip()
        slug = slugify(title_one)
        narr = (scene.get("narration") or "").strip()
        concept = (scene.get("concept") or "").strip()
        visual = scene.get("visual") or {}
        motion = (scene.get("motion") or {}).get("type") or ""
        transition = map_transition(scene.get("transition"))
        src = f"compositions/frames/{sid:02d}-{slug}.html"

        lines += [
            f"## Frame {sid} — {title_one}",
            "",
            f"- scene: {concept or title_one}",
            f"- duration: {dur:.2f}s",
            f"- transition_in: {transition}",
            f"- status: outline",
            f'- voiceover: "{narr.replace(chr(34), chr(39))}"',
            f"- src: {src}",
            f"- start_s: {start}",
            f"- end_s: {end}",
            f"- visual_type: {visual.get('type', '')}",
            f"- motion: {motion}",
            "",
            concept or narr or title_one,
            "",
        ]
        if visual.get("asset_path"):
            lines += [f"Asset: `{visual['asset_path']}`", ""]
        if visual.get("search_query"):
            lines += [f"Search: {visual['search_query']}", ""]

        script_lines += [
            f"## Line (Frame {sid})",
            "",
            f"    {narr}",
            "",
        ]

    sb_out = hf / "STORYBOARD.md"
    sc_out = hf / "SCRIPT.md"
    sb_out.write_text("\n".join(lines), encoding="utf-8")
    sc_out.write_text("\n".join(script_lines), encoding="utf-8")
    print(f"wrote {sb_out}")
    print(f"wrote {sc_out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

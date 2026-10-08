#!/usr/bin/env python3
"""Convert storyboard.json → STORYBOARD.md + SCRIPT.md for HyperFrames."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _util import die, ensure_dir, read_json, resolve_project  # noqa: E402


# Faceless transitions.mjs registry names (non-cut inject real GSAP overlaps).
NON_CUT_CYCLE = [
    "zoom-through",
    "push-slide LEFT",
    "crossfade",
    "blur-crossfade",
    "push-slide UP",
    "squeeze",
]


def slugify(s: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9]+", "-", (s or "scene").lower()).strip("-")
    return (s[:40] or "scene")


def map_transition(t: str | None, scene_index: int, force_live: bool = True) -> str:
    """Map storyboard transition → faceless transition_in string."""
    raw = (t or "").strip().lower().replace("-", "_")

    mapped = None
    if raw in ("", "auto", "default"):
        mapped = None
    elif raw in ("hard_cut", "cut", "hard"):
        mapped = "cut"
    elif "blur" in raw and "fade" in raw:
        mapped = "blur-crossfade"
    elif "fade" in raw or "dissolve" in raw or "cross" in raw:
        mapped = "crossfade"
    elif "zoom" in raw:
        mapped = "zoom-through"
    elif "squeeze" in raw:
        mapped = "squeeze"
    elif "push" in raw or "slide" in raw or "wipe" in raw:
        direction = "LEFT"
        for d in ("LEFT", "RIGHT", "UP", "DOWN"):
            if d.lower() in raw:
                direction = d
                break
        if "right" in raw:
            direction = "RIGHT"
        elif "up" in raw:
            direction = "UP"
        elif "down" in raw:
            direction = "DOWN"
        mapped = f"push-slide {direction}"
    else:
        # pass through unknown registry-looking names lightly normalized
        mapped = (t or "cut").replace("_", "-")

    if not force_live:
        return mapped or "cut"

    # Ensure the piece is not all hard cuts: every other boundary after frame 1
    # gets a registry transition if the author left cut/auto.
    if scene_index == 0:
        return mapped or "cut"
    if mapped in (None, "cut") and scene_index % 2 == 1:
        return NON_CUT_CYCLE[(scene_index // 2) % len(NON_CUT_CYCLE)]
    return mapped or "cut"


def default_sfx(scene: dict, scene_index: int, transition: str) -> list[str]:
    existing = scene.get("sfx")
    if isinstance(existing, list) and existing:
        return [str(x).strip() for x in existing if str(x).strip()]
    if isinstance(existing, str) and existing.strip():
        return [s.strip() for s in existing.split(",") if s.strip()]

    # Auto palette — keeps shorts feeling live even if agent forgot sfx.
    if scene_index == 0:
        return ["pop"]
    if "zoom" in transition:
        return ["whoosh", "hit"]
    if "push" in transition or "squeeze" in transition:
        return ["whoosh"]
    if "fade" in transition:
        return ["rise"]
    motion = ((scene.get("motion") or {}).get("type") or "").lower()
    if "punch" in motion or "pop" in motion:
        return ["pop"]
    return ["whoosh"]


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
    parser.add_argument(
        "--allow-all-cuts",
        action="store_true",
        help="Do not auto-upgrade hard cuts to registry transitions",
    )
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
    force_live = not args.allow_all_cuts

    lines = [
        "---",
        f"format: {fmt}",
        f'message: "{message.replace(chr(34), chr(39))}"',
        "arc: Hook → Develop → Payoff",
        "audience: short-form viewers",
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

    non_cut = 0
    for i, scene in enumerate(scenes):
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
        motion = (scene.get("motion") or {}).get("type") or "pop_in"
        transition = map_transition(scene.get("transition"), i, force_live=force_live)
        if transition != "cut":
            non_cut += 1
        sfx = default_sfx(scene, i, transition)
        sfx_csv = ", ".join(sfx)
        src = f"compositions/frames/{sid:02d}-{slug}.html"

        lines += [
            f"## Frame {sid} — {title_one}",
            "",
            f"- scene: {concept or title_one}",
            f"- duration: {dur:.2f}s",
            f"- transition_in: {transition}",
            f"- sfx: {sfx_csv}",
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
            "Motion required: GSAP entrance on hero + staggered captions; idle micro-float OK.",
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
    boundaries = max(0, len(scenes) - 1)
    print(f"transitions: non-cut={non_cut} / scenes={len(scenes)} (boundaries~{boundaries})")
    if force_live and boundaries > 0 and non_cut == 0:
        print("WARN: all cuts — re-run without --allow-all-cuts or set richer transitions in storyboard.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

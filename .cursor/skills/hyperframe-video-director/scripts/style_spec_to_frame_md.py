#!/usr/bin/env python3
"""Seed composition/hyperframes/frame.md from analysis/style-spec.json."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _util import die, ensure_dir, read_json, resolve_project  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True)
    parser.add_argument("--style-spec", default=None)
    args = parser.parse_args()

    project = resolve_project(args.project)
    style_path = Path(args.style_spec) if args.style_spec else project / "analysis" / "style-spec.json"
    if not style_path.is_file():
        die(f"style-spec not found: {style_path}")

    style = read_json(style_path)
    fmt = style.get("format") or {}
    pacing = style.get("pacing") or {}
    typo = style.get("typography") or {}
    color = style.get("color") or {}
    imagery = style.get("imagery") or {}
    motion = style.get("motion_graphics") or {}
    transitions = style.get("transitions") or {}
    hierarchy = style.get("hierarchy") or {}

    w = fmt.get("width") or 1080
    h = fmt.get("height") or 1920
    ar = fmt.get("aspect_ratio") or f"{w}:{h}"
    palette = color.get("palette") or ["#111111", "#F5F5F0", "#E8C547"]
    palette_s = ", ".join(palette)

    md = f"""# frame.md — director style seed

> Generated from `analysis/style-spec.json`. Refine for the piece; keep VO timing authoritative.
> Do not copy reference footage. Grammar only.

## Canvas

- Aspect: **{ar}**
- Size: **{w}×{h}**
- FPS hint: {fmt.get("fps") or "30"}

## Pacing

- Average shot duration: {pacing.get("average_shot_duration", "n/a")}s
- Cut style: {pacing.get("cut_style", "n/a")}
- Density: {pacing.get("scene_density", "n/a")}
- Narration-driven cuts: {pacing.get("narration_driven_cuts", True)}

## Typography

- Style: {typo.get("style", "bold sans")}
- Characteristics: {typo.get("font_characteristics", "")}
- Size: {typo.get("text_size", "large")}
- Position: {typo.get("position", "lower_center")}
- Caption style: {typo.get("caption_style", "")}
- Emphasis: {typo.get("emphasis", "keyword")}

Prefer expressive non-default display fonts that match the grammar (avoid Inter/Roboto/Arial unless the style-spec demands them).

## Color

- Palette: {palette_s}
- Background: {color.get("background_treatment", "")}
- Contrast: {color.get("contrast", "high")}

## Imagery

- Treatment: {imagery.get("treatment", "full_screen")}
- Motion: {imagery.get("motion", "slow_zoom")}
- Subject positioning: {imagery.get("subject_positioning", "")}
- Photos: {imagery.get("uses_photographs", True)} · Icons: {imagery.get("uses_icons", False)} · Diagrams: {imagery.get("uses_diagrams", False)}

## Motion graphics

- Zoom: {motion.get("zoom_behavior", "")}
- Pan: {motion.get("pan_behavior", "")}
- Parallax: {motion.get("parallax", False)}
- Overlays: {", ".join(motion.get("overlays") or []) or "none"}
- Gradients / scrims: {motion.get("gradients", "")}
- Shadows: {motion.get("shadows", "")}

## Transitions

- Style: {transitions.get("style", "hard_cut")}
- Common: {", ".join(transitions.get("common") or ["hard_cut"])}

## Hierarchy

- {hierarchy.get("visual_hierarchy", "")}
- Emphasis timing: {hierarchy.get("emphasis_timing", "")}

## Notes

{style.get("notes") or "Original composition influenced by reference grammar."}
"""

    hf = ensure_dir(project / "composition" / "hyperframes")
    out = hf / "frame.md"
    out.write_text(md, encoding="utf-8")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

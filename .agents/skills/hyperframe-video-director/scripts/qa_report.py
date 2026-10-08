#!/usr/bin/env python3
"""Structural QA against storyboard, transcript, assets, and media probe."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _util import read_json, resolve_project, write_json  # noqa: E402


IMAGE_TYPES = {
    "photograph",
    "screenshot",
    "icon",
    "video_clip",
    "diagram",
    "multiple",
    "generated_graphic",  # still requires a real asset_path wrapping media
}


def resolve_asset(project: Path, asset_path: str) -> Path | None:
    if not asset_path:
        return None
    p = Path(asset_path)
    candidates = [
        p if p.is_absolute() else project / p,
        project / "composition" / "hyperframes" / p,
        project / "composition" / "hyperframes" / "public" / p.name,
    ]
    for c in candidates:
        if c.is_file():
            return c
    return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True)
    parser.add_argument("--tolerance", type=float, default=0.35, help="seconds allowed VO vs storyboard drift")
    parser.add_argument(
        "--phase",
        choices=("assets", "pre_render", "all"),
        default="all",
        help="assets=image gate only; pre_render/all include sfx/transition checks when artifacts exist",
    )
    args = parser.parse_args()

    project = resolve_project(args.project)
    issues: list[dict] = []

    sb_path = project / "storyboard" / "storyboard.json"
    tr_path = project / "analysis" / "transcript.json"
    probe_path = project / "analysis" / "media-probe.json"
    style_path = project / "analysis" / "style-spec.json"
    hf = project / "composition" / "hyperframes"

    if not sb_path.is_file():
        issues.append({"level": "error", "code": "missing_storyboard", "msg": str(sb_path)})
    if not tr_path.is_file():
        issues.append({"level": "error", "code": "missing_transcript", "msg": str(tr_path)})
    if not style_path.is_file():
        issues.append({"level": "error", "code": "missing_style_spec", "msg": str(style_path)})

    sb = read_json(sb_path) if sb_path.is_file() else {}
    tr = read_json(tr_path) if tr_path.is_file() else {}
    probe = read_json(probe_path) if probe_path.is_file() else {}

    scenes = sb.get("scenes") or []
    if not scenes:
        issues.append({"level": "error", "code": "no_scenes", "msg": "storyboard has zero scenes"})

    text_only_count = 0
    missing_asset = 0
    generated_without_asset = 0

    prev_end = 0.0
    for i, scene in enumerate(scenes):
        sid = scene.get("scene_id", i + 1)
        start = float(scene.get("start", 0))
        end = float(scene.get("end", 0))
        if end <= start:
            issues.append({"level": "error", "code": "bad_timing", "scene": sid, "msg": f"end<=start ({start}-{end})"})
        if i > 0 and start + 1e-3 < prev_end:
            issues.append({"level": "warn", "code": "overlap", "scene": sid, "msg": f"overlaps previous (start={start}, prev_end={prev_end})"})
        if i > 0 and start - prev_end > 0.75:
            issues.append({"level": "warn", "code": "gap", "scene": sid, "msg": f"gap after previous ({start - prev_end:.2f}s)"})
        if not (scene.get("narration") or "").strip():
            issues.append({"level": "warn", "code": "empty_narration", "scene": sid, "msg": "empty narration"})

        visual = scene.get("visual") or {}
        vtype = (visual.get("type") or "").lower()
        query = (visual.get("search_query") or "").strip()
        asset_path = (visual.get("asset_path") or "").strip()

        if vtype == "text_only":
            text_only_count += 1
        else:
            if not query:
                issues.append(
                    {
                        "level": "error",
                        "code": "missing_search_query",
                        "scene": sid,
                        "msg": "non-text_only scene needs visual.search_query tied to narration",
                    }
                )
            if not asset_path:
                missing_asset += 1
                issues.append(
                    {
                        "level": "error",
                        "code": "missing_asset_path",
                        "scene": sid,
                        "msg": "set visual.asset_path after caching a real image (see asset-research.md)",
                    }
                )
            else:
                found = resolve_asset(project, asset_path)
                if not found:
                    issues.append(
                        {
                            "level": "error",
                            "code": "asset_file_missing",
                            "scene": sid,
                            "msg": f"asset_path not on disk: {asset_path}",
                        }
                    )
            if vtype == "generated_graphic" and not asset_path:
                generated_without_asset += 1

        prev_end = max(prev_end, end)

    if scenes:
        ratio = text_only_count / len(scenes)
        if ratio > 0.20 + 1e-9:
            issues.append(
                {
                    "level": "error",
                    "code": "too_many_text_only",
                    "msg": f"{text_only_count}/{len(scenes)} scenes are text_only ({ratio:.0%}) - max 20%; use real images",
                }
            )
        if generated_without_asset:
            issues.append(
                {
                    "level": "error",
                    "code": "generated_graphic_without_image",
                    "msg": f"{generated_without_asset} generated_graphic scene(s) lack asset_path - inventing SVG is not enough",
                }
            )
        if missing_asset == len(scenes) - text_only_count and (len(scenes) - text_only_count) > 0:
            issues.append(
                {
                    "level": "error",
                    "code": "no_images_researched",
                    "msg": "no scenes have asset_path - run Step 7 asset research before compose",
                }
            )

    # Frame HTML must reference images once composed
    if args.phase != "assets":
        frames_dir = hf / "compositions" / "frames"
        if frames_dir.is_dir():
            frame_files = list(frames_dir.glob("*.html"))
            img_frames = 0
            timeline_frames = 0
            for ff in frame_files:
                text = ff.read_text(encoding="utf-8", errors="replace")
                if re.search(r"<img\b", text, re.I) or re.search(r"<video\b", text, re.I):
                    img_frames += 1
                if "__timelines" in text:
                    timeline_frames += 1
            if frame_files and img_frames < max(1, int(len(frame_files) * 0.7)):
                issues.append(
                    {
                        "level": "error",
                        "code": "frames_missing_img",
                        "msg": f"only {img_frames}/{len(frame_files)} frame HTML files contain <img>/<video> - rebuild with real assets",
                    }
                )
            if frame_files and timeline_frames < len(frame_files):
                issues.append(
                    {
                        "level": "error",
                        "code": "frames_missing_timelines",
                        "msg": f"only {timeline_frames}/{len(frame_files)} frames register window.__timelines - fix GSAP registration",
                    }
                )

    vo_dur = None
    if probe.get("voiceover") and probe["voiceover"].get("duration_s"):
        vo_dur = float(probe["voiceover"]["duration_s"])
    elif tr.get("audio_duration_secs"):
        vo_dur = float(tr["audio_duration_secs"])
    elif scenes:
        vo_dur = float(scenes[-1]["end"])

    if vo_dur is not None and scenes:
        last = float(scenes[-1]["end"])
        if abs(last - vo_dur) > args.tolerance:
            issues.append(
                {
                    "level": "warn",
                    "code": "duration_mismatch",
                    "msg": f"storyboard end {last:.2f}s vs VO {vo_dur:.2f}s (tol {args.tolerance})",
                }
            )

    if args.phase == "assets":
        # Skip compose/render-specific checks
        pass
    else:
        for rel in ("STORYBOARD.md", "SCRIPT.md", "frame.md", "audio_meta.json"):
            p = hf / rel
            if not p.is_file():
                issues.append({"level": "info", "code": "bridge_pending", "msg": f"missing {rel} (ok before handoff)"})

        if (hf / "audio_meta.json").is_file():
            meta = read_json(hf / "audio_meta.json")
            voices = meta.get("voices") or []
            if len(voices) != len(scenes) and scenes:
                issues.append(
                    {
                        "level": "error",
                        "code": "voice_count_mismatch",
                        "msg": f"audio_meta voices={len(voices)} scenes={len(scenes)}",
                    }
                )
            for v in voices:
                path = hf / v.get("path", "")
                if v.get("path") and not path.is_file():
                    issues.append({"level": "error", "code": "missing_voice_file", "msg": v.get("path")})
            sfx = meta.get("sfx") or []
            # Only hard-fail SFX once index exists (compose complete) or phase=pre_render
            if not sfx:
                level = "error" if (hf / "index.html").is_file() or args.phase == "pre_render" else "warn"
                issues.append(
                    {
                        "level": level,
                        "code": "missing_sfx",
                        "msg": "audio_meta.sfx empty — run faceless audio.mjs fetch-sfx before render",
                    }
                )

        cut_only = 0
        sfx_missing = 0
        for scene in scenes:
            t = (scene.get("transition") or "hard_cut").lower().replace("-", "_")
            if t in ("hard_cut", "cut", "hard", ""):
                cut_only += 1
            if not scene.get("sfx"):
                sfx_missing += 1
        if scenes and cut_only == len(scenes) and len(scenes) >= 3:
            issues.append(
                {
                    "level": "error",
                    "code": "all_hard_cuts",
                    "msg": "every scene is hard_cut — mix zoom-through/push-slide/crossfade (see motion-and-sfx.md)",
                }
            )
        if scenes and sfx_missing == len(scenes):
            issues.append(
                {
                    "level": "warn",
                    "code": "storyboard_sfx_empty",
                    "msg": "no scene.sfx in storyboard.json — bridge auto-fills STORYBOARD.md, but prefer explicit cues",
                }
            )

        story_md = hf / "STORYBOARD.md"
        if story_md.is_file():
            text = story_md.read_text(encoding="utf-8")
            if "- sfx:" not in text.lower():
                issues.append(
                    {
                        "level": "error",
                        "code": "storyboard_md_no_sfx",
                        "msg": "STORYBOARD.md has no sfx: lines — re-run storyboard_to_hyperframes.py",
                    }
                )
            non_cut_tokens = ("zoom-through", "push-slide", "crossfade", "blur-crossfade", "squeeze")
            if len(scenes) >= 3 and not any(tok in text for tok in non_cut_tokens):
                issues.append(
                    {
                        "level": "error",
                        "code": "storyboard_md_all_cuts",
                        "msg": "STORYBOARD.md has no non-cut transition_in — transitions.mjs will inject 0 effects",
                    }
                )

    errors = [i for i in issues if i["level"] == "error"]
    warns = [i for i in issues if i["level"] == "warn"]
    report = {
        "ok": len(errors) == 0,
        "phase": args.phase,
        "error_count": len(errors),
        "warn_count": len(warns),
        "scene_count": len(scenes),
        "text_only_count": text_only_count,
        "scenes_missing_asset_path": missing_asset,
        "voiceover_duration_s": vo_dur,
        "issues": issues,
    }
    out = project / "qa" / "report.json"
    write_json(out, report)

    print(f"QA {'PASS' if report['ok'] else 'FAIL'} - errors={len(errors)} warns={len(warns)} phase={args.phase}")
    for i in issues:
        if i["level"] in ("error", "warn"):
            scene = f" scene={i['scene']}" if "scene" in i else ""
            print(f"  [{i['level']}] {i['code']}{scene}: {i['msg']}")
    print(f"wrote {out}")
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

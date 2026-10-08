#!/usr/bin/env python3
"""Structural QA against storyboard, transcript, and media probe."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _util import read_json, resolve_project, write_json  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True)
    parser.add_argument("--tolerance", type=float, default=0.35, help="seconds allowed VO vs storyboard drift")
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
        if visual.get("type") not in (None, "text_only", "generated_graphic") and not (
            visual.get("asset_path") or visual.get("search_query")
        ):
            issues.append({"level": "warn", "code": "missing_visual_source", "scene": sid, "msg": "no asset_path or search_query"})
        prev_end = max(prev_end, end)

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

    # HyperFrames bridge artifacts
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

    errors = [i for i in issues if i["level"] == "error"]
    warns = [i for i in issues if i["level"] == "warn"]
    report = {
        "ok": len(errors) == 0,
        "error_count": len(errors),
        "warn_count": len(warns),
        "scene_count": len(scenes),
        "voiceover_duration_s": vo_dur,
        "issues": issues,
    }
    out = project / "qa" / "report.json"
    write_json(out, report)

    print(f"QA {'PASS' if report['ok'] else 'FAIL'} - errors={len(errors)} warns={len(warns)}")
    for i in issues:
        if i["level"] in ("error", "warn"):
            print(f"  [{i['level']}] {i['code']}: {i['msg']}")
    print(f"wrote {out}")
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

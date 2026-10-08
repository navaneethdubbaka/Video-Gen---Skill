#!/usr/bin/env python3
"""
Smoke test for hyperframe-video-director deterministic pipeline.

Creates short ffmpeg fixtures, runs init → ingest → probe → extract →
fixture transcript → storyboard → style → bridge scripts → qa_report.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / ".cursor" / "skills" / "hyperframe-video-director"
SCRIPTS = SKILL / "scripts"
FIXTURES = Path(__file__).resolve().parent / "fixtures"
SLUG = "smoke-director-short"
PROJECT = ROOT / "videos" / SLUG


def run(cmd: list[str], **kwargs) -> None:
    print("\n>>", " ".join(cmd))
    env = os.environ.copy()
    env.setdefault("PYTHONIOENCODING", "utf-8")
    r = subprocess.run(cmd, cwd=str(ROOT), text=True, capture_output=True, env=env, **kwargs)
    if r.stdout:
        print(r.stdout)
    if r.returncode != 0:
        print(r.stderr, file=sys.stderr)
        raise SystemExit(f"command failed ({r.returncode}): {cmd}")


def ensure_fixtures() -> tuple[Path, Path]:
    FIXTURES.mkdir(parents=True, exist_ok=True)
    ref = FIXTURES / "reference.mp4"
    vo = FIXTURES / "voiceover.wav"

    if not ref.is_file():
        # 6s 9:16 color bars-ish
        run(
            [
                "ffmpeg",
                "-y",
                "-f",
                "lavfi",
                "-i",
                "color=c=0x1a1a2e:s=1080x1920:d=6",
                "-f",
                "lavfi",
                "-i",
                "sine=frequency=440:duration=6",
                "-shortest",
                "-c:v",
                "libx264",
                "-pix_fmt",
                "yuv420p",
                "-c:a",
                "aac",
                str(ref),
            ]
        )

    if not vo.is_file():
        # 6s mono wav (silent-ish tone as stand-in for speech)
        run(
            [
                "ffmpeg",
                "-y",
                "-f",
                "lavfi",
                "-i",
                "sine=frequency=220:duration=6",
                "-ac",
                "1",
                "-ar",
                "44100",
                str(vo),
            ]
        )

    return ref, vo


def write_style_and_storyboard() -> None:
    style = {
        "format": {"aspect_ratio": "9:16", "width": 1080, "height": 1920, "fps": 30},
        "pacing": {
            "average_shot_duration": 2.0,
            "cut_style": "fast",
            "scene_density": "medium",
            "narration_driven_cuts": True,
        },
        "typography": {
            "style": "bold sans serif",
            "position": "lower_center",
            "emphasis": "keyword",
            "keyword_emphasis": True,
        },
        "color": {
            "palette": ["#1a1a2e", "#eaeaea", "#e94560"],
            "background_treatment": "solid dark",
            "contrast": "high",
        },
        "imagery": {"treatment": "full_screen", "motion": "slow_zoom", "uses_photographs": False},
        "transitions": {"style": "hard_cut", "common": ["hard_cut"]},
        "notes": "smoke fixture style",
    }
    (PROJECT / "analysis" / "style-spec.json").write_text(json.dumps(style, indent=2), encoding="utf-8")
    (PROJECT / "analysis" / "reference-analysis.json").write_text(
        json.dumps({"note": "synthetic fixture; no real reference grammar"}, indent=2),
        encoding="utf-8",
    )

    storyboard = {
        "project": SLUG,
        "language": "en",
        "message": "Smoke test short",
        "total_duration_s": 6.0,
        "style_spec_path": "analysis/style-spec.json",
        "instructions": "smoke",
        "scenes": [
            {
                "scene_id": 1,
                "start": 0.0,
                "end": 2.0,
                "narration": "This is a short test.",
                "concept": "Hook",
                "visual": {"type": "text_only"},
                "text": {"content": "SHORT TEST", "emphasis": ["TEST"]},
                "motion": {"type": "punch_in"},
                "transition": "hard_cut",
            },
            {
                "scene_id": 2,
                "start": 2.0,
                "end": 4.0,
                "narration": "Style guides the look.",
                "concept": "Style",
                "visual": {"type": "text_only"},
                "text": {"content": "STYLE", "emphasis": ["STYLE"]},
                "motion": {"type": "zoom_in"},
                "transition": "hard_cut",
            },
            {
                "scene_id": 3,
                "start": 4.0,
                "end": 6.0,
                "narration": "Voice owns the timing.",
                "concept": "Timing",
                "visual": {"type": "text_only"},
                "text": {"content": "TIMING", "emphasis": ["TIMING"]},
                "motion": {"type": "punch_in"},
                "transition": "hard_cut",
            },
        ],
    }
    (PROJECT / "storyboard" / "storyboard.json").write_text(
        json.dumps(storyboard, indent=2), encoding="utf-8"
    )


def main() -> int:
    py = sys.executable
    ref, vo = ensure_fixtures()

    # clean project
    if PROJECT.exists():
        shutil.rmtree(PROJECT)

    run([py, str(SCRIPTS / "doctor.py")])
    run([py, str(SCRIPTS / "init_project.py"), "--slug", SLUG, "--root", str(ROOT / "videos")])
    run([py, str(SCRIPTS / "download_reference.py"), "--project", str(PROJECT), "--source", str(ref)])
    run([py, str(SCRIPTS / "ingest_voiceover.py"), "--project", str(PROJECT), "--source", str(vo)])
    run([py, str(SCRIPTS / "probe_media.py"), "--project", str(PROJECT)])
    run([py, str(SCRIPTS / "extract_reference_frames.py"), "--project", str(PROJECT), "--max-frames", "6"])

    # transcription: live if key present, else fixture
    load_env = ROOT / ".env"
    if load_env.is_file():
        for line in load_env.read_text(encoding="utf-8").splitlines():
            if "=" in line and not line.strip().startswith("#"):
                k, _, v = line.partition("=")
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

    tr_out = PROJECT / "analysis" / "transcript.json"
    if os.environ.get("ELEVENLABS_API_KEY"):
        print("ELEVENLABS_API_KEY set - attempting live STT")
        run(
            [
                py,
                str(SCRIPTS / "transcription" / "cli.py"),
                "--audio",
                str(PROJECT / "input" / "voiceover.wav"),
                "--out",
                str(tr_out),
            ]
        )
        stt_mode = "live-elevenlabs"
    else:
        print("ELEVENLABS_API_KEY not set - using fixture transcript")
        run(
            [
                py,
                str(SCRIPTS / "transcription" / "cli.py"),
                "--fixture-transcript",
                str(FIXTURES / "transcript_fixture.json"),
                "--out",
                str(tr_out),
            ]
        )
        stt_mode = "fixture"

    write_style_and_storyboard()

    run([py, str(SCRIPTS / "style_spec_to_frame_md.py"), "--project", str(PROJECT)])
    run([py, str(SCRIPTS / "storyboard_to_hyperframes.py"), "--project", str(PROJECT)])
    run([py, str(SCRIPTS / "build_audio_meta_from_vo.py"), "--project", str(PROJECT)])
    run([py, str(SCRIPTS / "qa_report.py"), "--project", str(PROJECT)])

    # sanity asserts
    assert (PROJECT / "analysis" / "media-probe.json").is_file()
    assert list((PROJECT / "analysis" / "frames").glob("frame_*.jpg"))
    assert (PROJECT / "composition" / "hyperframes" / "STORYBOARD.md").is_file()
    assert (PROJECT / "composition" / "hyperframes" / "audio_meta.json").is_file()
    meta = json.loads((PROJECT / "composition" / "hyperframes" / "audio_meta.json").read_text(encoding="utf-8"))
    assert len(meta["voices"]) == 3
    for v in meta["voices"]:
        assert (PROJECT / "composition" / "hyperframes" / v["path"]).is_file()

    qa = json.loads((PROJECT / "qa" / "report.json").read_text(encoding="utf-8"))
    result = {
        "ok": qa.get("ok", False),
        "project": str(PROJECT),
        "stt_mode": stt_mode,
        "scenes": 3,
        "voice_clips": len(meta["voices"]),
        "frames_extracted": len(list((PROJECT / "analysis" / "frames").glob("frame_*.jpg"))),
        "qa": qa,
    }
    out = FIXTURES / "smoke_result.json"
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print("\n=== SMOKE RESULT ===")
    print(json.dumps(result, indent=2))
    print(f"wrote {out}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

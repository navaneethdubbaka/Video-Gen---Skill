#!/usr/bin/env python3
"""Split user VO by storyboard scenes → faceless-compatible audio_meta.json."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _util import (  # noqa: E402
    die,
    ensure_dir,
    find_voiceover,
    read_json,
    resolve_project,
    which,
    write_json,
)


def ffmpeg_slice(src: Path, dest: Path, start: float, end: float) -> float:
    if not which("ffmpeg"):
        die("ffmpeg not found")
    duration = max(0.05, end - start)
    dest.parent.mkdir(parents=True, exist_ok=True)
    # re-encode short slices for format safety
    cmd = [
        "ffmpeg",
        "-y",
        "-ss",
        f"{start:.3f}",
        "-i",
        str(src),
        "-t",
        f"{duration:.3f}",
        "-ac",
        "1",
        "-ar",
        "44100",
        str(dest),
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        die(f"ffmpeg slice failed [{start}-{end}]: {r.stderr[-800:]}")
    return duration


def words_for_scene(words: list[dict], start: float, end: float) -> list[dict]:
    out = []
    idx = 0
    for w in words:
        if (w.get("type") or "word") not in ("word", None):
            continue
        ws = float(w.get("start", 0))
        we = float(w.get("end", ws))
        # overlap with scene
        if we < start - 1e-3 or ws > end + 1e-3:
            continue
        text = w.get("text") or ""
        if not text.strip():
            continue
        out.append(
            {
                "id": w.get("id") or f"w{idx}",
                "text": text,
                "start": max(0.0, round(ws - start, 3)),
                "end": max(0.0, round(we - start, 3)),
            }
        )
        idx += 1
    return out


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True)
    parser.add_argument("--storyboard", default=None)
    parser.add_argument("--transcript", default=None)
    parser.add_argument("--hf-dir", default=None, help="HyperFrames dir (default composition/hyperframes)")
    args = parser.parse_args()

    project = resolve_project(args.project)
    sb_path = Path(args.storyboard) if args.storyboard else project / "storyboard" / "storyboard.json"
    tr_path = Path(args.transcript) if args.transcript else project / "analysis" / "transcript.json"
    hf = Path(args.hf_dir) if args.hf_dir else project / "composition" / "hyperframes"

    if not sb_path.is_file():
        die(f"storyboard not found: {sb_path}")
    if not tr_path.is_file():
        die(f"transcript not found: {tr_path}")

    storyboard = read_json(sb_path)
    transcript = read_json(tr_path)
    vo = find_voiceover(project)
    voices_dir = ensure_dir(hf / "assets" / "voices")

    scenes = storyboard.get("scenes") or []
    if not scenes:
        die("storyboard has no scenes")

    words = transcript.get("words") or []
    voices = []
    for scene in scenes:
        sid = int(scene["scene_id"])
        start = float(scene["start"])
        end = float(scene["end"])
        pad = f"{sid:02d}"
        dest = voices_dir / f"{pad}.wav"
        dur = ffmpeg_slice(vo, dest, start, end)
        # prefer measured duration from scene window
        dur = round(end - start, 3) if end > start else dur
        rel = f"assets/voices/{pad}.wav"
        voices.append(
            {
                "frame": sid,
                "path": rel,
                "duration_s": dur,
                "words": words_for_scene(words, start, end),
            }
        )

    meta = {"voices": voices, "bgm": None, "sfx": []}
    out = hf / "audio_meta.json"
    write_json(out, meta)
    print(f"wrote {out} ({len(voices)} voice clips)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

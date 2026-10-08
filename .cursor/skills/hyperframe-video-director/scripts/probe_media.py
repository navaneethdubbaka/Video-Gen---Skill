#!/usr/bin/env python3
"""ffprobe reference + voiceover → analysis/media-probe.json."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _util import (  # noqa: E402
    aspect_ratio_string,
    die,
    find_reference,
    find_voiceover,
    resolve_project,
    which,
    write_json,
)


def probe(path: Path) -> dict:
    if not which("ffprobe"):
        die("ffprobe not found on PATH")
    cmd = [
        "ffprobe",
        "-v",
        "quiet",
        "-print_format",
        "json",
        "-show_format",
        "-show_streams",
        str(path),
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        die(f"ffprobe failed for {path}: {r.stderr}")
    data = json.loads(r.stdout)
    video = next((s for s in data.get("streams", []) if s.get("codec_type") == "video"), None)
    audio = next((s for s in data.get("streams", []) if s.get("codec_type") == "audio"), None)
    fmt = data.get("format", {})
    width = int(video["width"]) if video and video.get("width") else None
    height = int(video["height"]) if video and video.get("height") else None
    duration = float(fmt.get("duration") or (video or {}).get("duration") or 0) or None
    fps = None
    if video and video.get("r_frame_rate") and video["r_frame_rate"] != "0/0":
        num, _, den = video["r_frame_rate"].partition("/")
        try:
            fps = float(num) / float(den or 1)
        except ValueError:
            fps = None
    return {
        "path": str(path.as_posix()),
        "duration_s": duration,
        "width": width,
        "height": height,
        "aspect_ratio": aspect_ratio_string(width, height) if width and height else None,
        "fps": fps,
        "video_codec": video.get("codec_name") if video else None,
        "audio_codec": audio.get("codec_name") if audio else None,
        "format_name": fmt.get("format_name"),
        "size_bytes": int(fmt["size"]) if fmt.get("size") else None,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True)
    args = parser.parse_args()

    project = resolve_project(args.project)
    ref = find_reference(project)
    try:
        vo = find_voiceover(project)
        vo_probe = probe(vo)
    except SystemExit:
        vo_probe = None

    out = {
        "reference": probe(ref),
        "voiceover": vo_probe,
    }
    dest = project / "analysis" / "media-probe.json"
    write_json(dest, out)
    print(f"wrote {dest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

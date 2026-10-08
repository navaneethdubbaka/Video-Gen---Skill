#!/usr/bin/env python3
"""Sample stills from reference video for vision-based style analysis."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _util import die, ensure_dir, find_reference, resolve_project, which  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True)
    parser.add_argument("--fps", type=float, default=1.0, help="Sample rate (frames per second)")
    parser.add_argument("--max-frames", type=int, default=24)
    args = parser.parse_args()

    if not which("ffmpeg"):
        die("ffmpeg not found on PATH")

    project = resolve_project(args.project)
    ref = find_reference(project)
    out_dir = ensure_dir(project / "analysis" / "frames")

    # clear prior jpg samples
    for old in out_dir.glob("frame_*.jpg"):
        old.unlink()

    pattern = str(out_dir / "frame_%03d.jpg")
    # fps filter then optionally limit via -frames:v
    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        str(ref),
        "-vf",
        f"fps={args.fps}",
        "-frames:v",
        str(args.max_frames),
        "-q:v",
        "3",
        pattern,
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        die(f"ffmpeg extract failed: {r.stderr[-1500:]}")

    frames = sorted(out_dir.glob("frame_*.jpg"))
    print(f"extracted {len(frames)} frames -> {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

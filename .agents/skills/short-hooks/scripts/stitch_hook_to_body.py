#!/usr/bin/env python3
"""Concat hook clip + body trimmed from cut_body_at → variant mp4."""

from __future__ import annotations

import argparse
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _util import die, ensure_dir, read_json, resolve_run, which  # noqa: E402


def stitch_one(run: Path, hook_id: str, cut: float, width: int, height: int) -> Path:
    if not which("ffmpeg"):
        die("ffmpeg not found")

    hook = run / "renders" / f"hook-{hook_id}.mp4"
    body = run / "input" / "body.mp4"
    if not hook.is_file():
        die(f"missing hook render: {hook}")
    if not body.is_file():
        die(f"missing body: {body}")

    out = ensure_dir(run / "renders") / f"variant-{hook_id}.mp4"
    # Normalize both to same size/fps then concat via filter
    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        str(hook),
        "-ss",
        f"{cut:.3f}",
        "-i",
        str(body),
        "-filter_complex",
        (
            f"[0:v]scale={width}:{height}:force_original_aspect_ratio=decrease,"
            f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=30,format=yuv420p[v0];"
            f"[1:v]scale={width}:{height}:force_original_aspect_ratio=decrease,"
            f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=30,format=yuv420p[v1];"
            f"[0:a]aresample=44100,aformat=sample_fmts=fltp:channel_layouts=stereo[a0];"
            f"[1:a]aresample=44100,aformat=sample_fmts=fltp:channel_layouts=stereo[a1];"
            f"[v0][a0][v1][a1]concat=n=2:v=1:a=1[v][a]"
        ),
        "-map",
        "[v]",
        "-map",
        "[a]",
        "-c:v",
        "libx264",
        "-preset",
        "fast",
        "-crf",
        "18",
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        "-movflags",
        "+faststart",
        str(out),
    ]

    # Hooks may be silent — generate silent audio if no audio stream
    probe = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-select_streams",
            "a",
            "-show_entries",
            "stream=index",
            "-of",
            "csv=p=0",
            str(hook),
        ],
        text=True,
        capture_output=True,
    )
    has_hook_audio = bool(probe.stdout.strip())

    if not has_hook_audio:
        # Rebuild filter with anullsrc for hook audio
        cmd = [
            "ffmpeg",
            "-y",
            "-i",
            str(hook),
            "-ss",
            f"{cut:.3f}",
            "-i",
            str(body),
            "-f",
            "lavfi",
            "-i",
            "anullsrc=channel_layout=stereo:sample_rate=44100",
            "-filter_complex",
            (
                f"[0:v]scale={width}:{height}:force_original_aspect_ratio=decrease,"
                f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=30,format=yuv420p[v0];"
                f"[1:v]scale={width}:{height}:force_original_aspect_ratio=decrease,"
                f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=30,format=yuv420p[v1];"
                f"[2:a]atrim=0:3.5,aresample=44100[a0];"
                f"[1:a]aresample=44100,aformat=sample_fmts=fltp:channel_layouts=stereo[a1];"
                f"[v0][a0][v1][a1]concat=n=2:v=1:a=1[v][a]"
            ),
            "-map",
            "[v]",
            "-map",
            "[a]",
            "-c:v",
            "libx264",
            "-preset",
            "fast",
            "-crf",
            "18",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-shortest",
            "-movflags",
            "+faststart",
            str(out),
        ]

    r = subprocess.run(cmd, text=True, capture_output=True)
    if r.returncode != 0:
        die(f"ffmpeg stitch failed for {hook_id}:\n{r.stderr[-1200:]}")
    print(f"wrote {out}")
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--run", required=True, help="hooks/<run-id> directory")
    ap.add_argument("--hook-id", default=None, help="h1 / h2 / …")
    ap.add_argument("--all", action="store_true", help="stitch every hook-* present")
    args = ap.parse_args()

    run = resolve_run(args.run)
    meta_path = run / "hooks.json"
    if not meta_path.is_file():
        die(f"missing {meta_path}")
    meta = read_json(meta_path)
    cut = float(meta.get("cut_body_at") or 2.8)
    body = meta.get("body") or {}
    width = int(body.get("width") or 1080)
    height = int(body.get("height") or 1920)

    ids: list[str] = []
    if args.all:
        ids = sorted(
            p.stem.replace("hook-", "")
            for p in (run / "renders").glob("hook-*.mp4")
        )
        if not ids:
            die("no renders/hook-*.mp4 found")
    elif args.hook_id:
        ids = [args.hook_id]
    else:
        die("pass --hook-id h1 or --all")

    for hid in ids:
        stitch_one(run, hid, cut, width, height)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

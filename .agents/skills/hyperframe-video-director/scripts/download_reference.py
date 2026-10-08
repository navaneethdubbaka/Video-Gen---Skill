#!/usr/bin/env python3
"""Ingest a local or YouTube reference into project input/."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _util import die, ensure_dir, resolve_project, which  # noqa: E402


VIDEO_EXTS = {".mp4", ".webm", ".mov", ".mkv", ".m4v"}


def is_url(s: str) -> bool:
    u = urlparse(s)
    return u.scheme in ("http", "https") and bool(u.netloc)


def copy_local(src: Path, dest_dir: Path) -> Path:
    if not src.is_file():
        die(f"local reference not found: {src}")
    ext = src.suffix.lower() or ".mp4"
    if ext not in VIDEO_EXTS:
        print(f"WARN: unusual video extension {ext}", file=sys.stderr)
    dest = dest_dir / f"reference{ext}"
    shutil.copy2(src, dest)
    return dest


def download_youtube(url: str, dest_dir: Path) -> Path:
    ytdlp = which("yt-dlp")
    if not ytdlp:
        die(
            "yt-dlp is not installed. Install yt-dlp, or provide a local reference file "
            "(e.g. --source ./reference.mp4)."
        )
    out_tmpl = str(dest_dir / "reference.%(ext)s")
    # Prefer mp4 when possible
    cmd = [
        ytdlp,
        "-f",
        "bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]/b",
        "--merge-output-format",
        "mp4",
        "-o",
        out_tmpl,
        "--no-playlist",
        url,
    ]
    print("Running:", " ".join(cmd))
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        # retry simpler format
        cmd2 = [ytdlp, "-o", out_tmpl, "--no-playlist", url]
        print("Retry:", " ".join(cmd2))
        r = subprocess.run(cmd2, capture_output=True, text=True)
        if r.returncode != 0:
            die(
                "Failed to download YouTube reference.\n"
                f"yt-dlp stderr:\n{(r.stderr or r.stdout or '')[:2000]}\n\n"
                "Provide a local file instead: --source ./reference.mp4"
            )

    matches = sorted(dest_dir.glob("reference.*"), key=lambda p: p.stat().st_mtime, reverse=True)
    matches = [m for m in matches if m.suffix.lower() in VIDEO_EXTS or m.suffix.lower() == ".mp4"]
    if not matches:
        # any reference.*
        matches = list(dest_dir.glob("reference.*"))
    if not matches:
        die("yt-dlp finished but no reference.* file found in input/")
    return matches[0]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True)
    parser.add_argument("--source", required=True, help="YouTube URL or local video path")
    args = parser.parse_args()

    project = resolve_project(args.project)
    dest_dir = ensure_dir(project / "input")

    if is_url(args.source):
        path = download_youtube(args.source, dest_dir)
    else:
        path = copy_local(Path(args.source).expanduser().resolve(), dest_dir)

    print(f"reference ready: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

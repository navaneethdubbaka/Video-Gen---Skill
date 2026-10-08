#!/usr/bin/env python3
"""Copy user voiceover into project input/voiceover.<ext>."""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _util import die, ensure_dir, resolve_project  # noqa: E402


AUDIO_EXTS = {".wav", ".mp3", ".m4a", ".aac", ".flac", ".ogg", ".wma"}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True)
    parser.add_argument("--source", required=True)
    args = parser.parse_args()

    project = resolve_project(args.project)
    src = Path(args.source).expanduser().resolve()
    if not src.is_file():
        die(f"voiceover not found: {src}")
    ext = src.suffix.lower() or ".wav"
    if ext not in AUDIO_EXTS:
        print(f"WARN: unusual audio extension {ext}", file=sys.stderr)

    dest_dir = ensure_dir(project / "input")
    # remove prior voiceover.*
    for old in dest_dir.glob("voiceover.*"):
        old.unlink()
    dest = dest_dir / f"voiceover{ext}"
    shutil.copy2(src, dest)
    print(f"voiceover ready: {dest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

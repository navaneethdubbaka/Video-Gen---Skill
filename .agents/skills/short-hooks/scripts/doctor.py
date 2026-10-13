#!/usr/bin/env python3
"""Check tools needed for short-hooks."""

from __future__ import annotations

import shutil
import sys


def main() -> int:
    ok = True
    for cmd in ("ffmpeg", "ffprobe", "node", "npx", "python"):
        path = shutil.which(cmd)
        if path:
            print(f"OK  {cmd}: {path}")
        else:
            print(f"MISS {cmd}")
            ok = False
    if not ok:
        print("Install missing tools before running short-hooks.", file=sys.stderr)
        return 1
    print("doctor: ready")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

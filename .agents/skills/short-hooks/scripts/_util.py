#!/usr/bin/env python3
"""Shared helpers for short-hooks scripts."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


def die(msg: str, code: int = 1) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)
    raise SystemExit(code)


def which(cmd: str) -> str | None:
    return shutil.which(cmd)


def ensure_dir(p: Path) -> Path:
    p.mkdir(parents=True, exist_ok=True)
    return p


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def run(cmd: list[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, text=True, capture_output=True, check=check)


def ffprobe_json(path: Path) -> dict[str, Any]:
    if not which("ffprobe"):
        die("ffprobe not found")
    r = run(
        [
            "ffprobe",
            "-v",
            "error",
            "-select_streams",
            "v:0",
            "-show_entries",
            "stream=width,height,r_frame_rate:format=duration",
            "-of",
            "json",
            str(path),
        ]
    )
    return json.loads(r.stdout)


def resolve_run(run: str | Path) -> Path:
    p = Path(run).expanduser().resolve()
    if not p.is_dir():
        die(f"run dir not found: {p}")
    return p

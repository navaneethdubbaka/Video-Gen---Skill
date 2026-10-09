"""Shared helpers for hyperframe-video-director scripts."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


def find_dotenv(start: Path | None = None) -> Path | None:
    here = (start or Path.cwd()).resolve()
    for p in [here, *here.parents]:
        candidate = p / ".env"
        if candidate.is_file():
            return candidate
        # also check skill-adjacent workspace root patterns
    return None


def load_dotenv(path: Path | None = None) -> None:
    """Load KEY=VALUE pairs into os.environ if not already set. No dependency on python-dotenv."""
    env_path = path or find_dotenv()
    if env_path is None:
        # skill .env next to SKILL.md parent workspace
        # scripts/ -> skill -> skills -> .cursor -> workspace
        workspace_env = Path(__file__).resolve().parents[4] / ".env"
        if workspace_env.is_file():
            env_path = workspace_env
        else:
            return
    try:
        text = env_path.read_text(encoding="utf-8")
    except OSError:
        return
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, val = line.partition("=")
        key = key.strip()
        val = val.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = val


def die(msg: str, code: int = 1) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)
    raise SystemExit(code)


def which(cmd: str) -> str | None:
    return shutil.which(cmd)


def run(cmd: list[str], *, cwd: Path | None = None, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        cwd=str(cwd) if cwd else None,
        text=True,
        capture_output=True,
        check=check,
    )


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def resolve_project(project: str | Path) -> Path:
    p = Path(project).expanduser().resolve()
    if not p.exists():
        die(f"project not found: {p}")
    return p


def find_voiceover(project: Path) -> Path:
    input_dir = project / "input"
    if not input_dir.is_dir():
        die(f"missing input/: {input_dir}")
    if (input_dir / "voiceover.wav").is_file():
        return input_dir / "voiceover.wav"
    preferred = sorted(input_dir.glob("voiceover.*"))
    if preferred:
        return preferred[0]
    for ext in ("wav", "mp3", "m4a", "aac", "flac", "ogg"):
        hits = list(input_dir.glob(f"*.{ext}"))
        if hits:
            return hits[0]
    die(f"no voiceover found under {input_dir}")


def find_reference(project: Path) -> Path:
    input_dir = project / "input"
    for name in ("reference.mp4", "reference.webm", "reference.mov", "reference.mkv"):
        p = input_dir / name
        if p.is_file():
            return p
    vids = []
    for ext in ("mp4", "webm", "mov", "mkv"):
        vids.extend(input_dir.glob(f"*.{ext}"))
    vids = [v for v in vids if not v.name.startswith("voiceover")]
    if vids:
        return vids[0]
    die(f"no reference video found under {input_dir}")


def aspect_ratio_string(width: int, height: int) -> str:
    if width <= 0 or height <= 0:
        return "unknown"
    # simple reduced ratio via gcd
    from math import gcd

    g = gcd(width, height)
    return f"{width // g}:{height // g}"


def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path

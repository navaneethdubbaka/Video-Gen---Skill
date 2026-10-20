#!/usr/bin/env python3
"""Batch-animate greencode host_stills into host_talking/<id>/ loops."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

BANNED = {"shock"}


def workspace_root() -> Path:
    return Path(__file__).resolve().parents[4]


def skill_root() -> Path:
    return Path(__file__).resolve().parents[1]


def run(cmd: list[str]) -> None:
    print("+", " ".join(cmd))
    r = subprocess.run(cmd, check=False)
    if r.returncode != 0:
        raise SystemExit(r.returncode)


def encode_dir(out_dir: Path, encode_ps1: Path) -> None:
    if not encode_ps1.is_file():
        print(f"skip encode (missing {encode_ps1})")
        return
    run(
        [
            "powershell",
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            str(encode_ps1),
            "-OutDir",
            str(out_dir),
        ]
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--encode", action="store_true", help="Run encode_loops.ps1 after frames")
    parser.add_argument("--ids", nargs="*", help="Subset of expression ids")
    parser.add_argument("--bootstrap", action="store_true", help="Re-bootstrap calib first")
    args = parser.parse_args()

    ws = workspace_root()
    sk = skill_root()
    stills = ws / "greencode" / "my_animations" / "host_stills"
    talking = ws / "greencode" / "my_animations" / "host_talking"
    calib_dir = sk / "calib"
    animate = sk / "scripts" / "animate_mouth.py"
    bootstrap = sk / "scripts" / "bootstrap_calib.py"
    encode_ps1 = sk / "scripts" / "encode_loops.ps1"

    if args.bootstrap or not any(calib_dir.glob("*.json")):
        run([sys.executable, str(bootstrap)])

    talking.mkdir(parents=True, exist_ok=True)
    for png in sorted(stills.glob("*.png")):
        if png.stem in BANNED:
            continue
        if args.ids and png.stem not in args.ids:
            continue
        calib = calib_dir / f"{png.stem}.json"
        if not calib.is_file():
            print(f"MISSING calib for {png.stem}, bootstrapping one…")
            run([sys.executable, str(bootstrap), "--ids", png.stem])
        out = talking / png.stem
        out.mkdir(parents=True, exist_ok=True)
        run(
            [
                sys.executable,
                str(animate),
                str(png),
                str(out),
                "--calib",
                str(calib),
            ]
        )
        if args.encode:
            encode_dir(out, encode_ps1)

    print("batch complete ->", talking)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

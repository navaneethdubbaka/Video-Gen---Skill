#!/usr/bin/env python3
"""Preflight checks for hyperframe-video-director."""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _util import load_dotenv, which  # noqa: E402


def check_cmd(name: str, args: list[str] | None = None) -> tuple[bool, str]:
    path = which(name)
    if not path:
        return False, "NOT FOUND"
    if args is None:
        return True, path
    try:
        # shell=True helps Windows resolve .cmd shims (npx.cmd)
        use_shell = os.name == "nt" and path.lower().endswith((".cmd", ".bat"))
        r = subprocess.run(
            [name, *args],
            capture_output=True,
            text=True,
            timeout=60,
            shell=use_shell,
        )
        out = (r.stdout or r.stderr or "").strip().splitlines()
        ver = out[0] if out else path
        return True, ver[:120]
    except Exception as e:  # noqa: BLE001
        return True, f"{path} (version check failed: {e})"


def main() -> int:
    parser = argparse.ArgumentParser(description="Doctor: tool + env preflight")
    parser.add_argument("--require-elevenlabs", action="store_true", help="Fail if API key missing")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    load_dotenv()

    checks = {
        "python": (True, sys.version.split()[0]),
        "ffmpeg": check_cmd("ffmpeg", ["-version"]),
        "ffprobe": check_cmd("ffprobe", ["-version"]),
        "yt-dlp": check_cmd("yt-dlp", ["--version"]),
        "node": check_cmd("node", ["-v"]),
        "npx": check_cmd("npx", ["-v"]),
    }

    # hyperframes via npx (may download)
    hf_ok, hf_msg = False, "skipped"
    if checks["npx"][0]:
        try:
            r = subprocess.run(
                "npx --yes hyperframes --version" if os.name == "nt" else ["npx", "--yes", "hyperframes", "--version"],
                capture_output=True,
                text=True,
                timeout=120,
                shell=(os.name == "nt"),
            )
            hf_ok = r.returncode == 0
            lines = (r.stdout or r.stderr or "").strip().splitlines()
            hf_msg = lines[-1] if lines else "ok"
        except Exception as e:  # noqa: BLE001
            hf_ok, hf_msg = False, str(e)
    checks["hyperframes"] = (hf_ok, hf_msg)

    key = os.environ.get("ELEVENLABS_API_KEY", "").strip()
    checks["ELEVENLABS_API_KEY"] = (
        bool(key),
        f"set (len={len(key)})" if key else "NOT SET - export ELEVENLABS_API_KEY or copy .env.example to .env",
    )

    required = ["ffmpeg", "ffprobe", "node", "python"]
    if args.require_elevenlabs:
        required.append("ELEVENLABS_API_KEY")

    rows = []
    failed = False
    for name, (ok, detail) in checks.items():
        status = "OK" if ok else "FAIL"
        if name in required and not ok:
            failed = True
        elif name == "ELEVENLABS_API_KEY" and not ok:
            status = "WARN"
        rows.append({"name": name, "ok": ok, "detail": detail, "status": status})

    if args.json:
        import json

        print(json.dumps({"ok": not failed, "checks": rows}, indent=2))
    else:
        print("hyperframe-video-director doctor\n")
        for r in rows:
            print(f"  [{r['status']:4}] {r['name']}: {r['detail']}")
        print()
        if failed:
            print("RESULT: FAIL - install missing required tools.")
        elif not key:
            print("RESULT: OK with warnings - set ELEVENLABS_API_KEY before live transcription.")
        else:
            print("RESULT: OK")

    # yt-dlp optional
    if not shutil.which("yt-dlp"):
        print("NOTE: yt-dlp missing - YouTube references require a local file instead.")

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())

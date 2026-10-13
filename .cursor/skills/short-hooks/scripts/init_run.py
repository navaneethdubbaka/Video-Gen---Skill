#!/usr/bin/env python3
"""Scaffold hooks/<run-id>/ from 3–4 hook voice-over files (standalone visuals)."""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _util import die, ensure_dir, ffprobe_json, which, write_json  # noqa: E402

AUDIO_EXTS = {".wav", ".mp3", ".m4a", ".aac", ".flac", ".ogg"}


def slugify(s: str) -> str:
    s = s.strip().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s or "hooks-run"


def collect_vos(vo_args: list[str], vo_dir: str | None) -> list[Path]:
    files: list[Path] = []
    for v in vo_args:
        p = Path(v).expanduser().resolve()
        if not p.is_file():
            die(f"VO not found: {p}")
        files.append(p)
    if vo_dir:
        d = Path(vo_dir).expanduser().resolve()
        if not d.is_dir():
            die(f"VO dir not found: {d}")
        found = sorted(
            p for p in d.iterdir() if p.is_file() and p.suffix.lower() in AUDIO_EXTS
        )
        if not found:
            die(f"no audio files in {d}")
        files.extend(found)
    # de-dupe preserving order
    seen: set[str] = set()
    out: list[Path] = []
    for p in files:
        key = str(p)
        if key not in seen:
            seen.add(key)
            out.append(p)
    return out


def probe_audio_duration(path: Path) -> float:
    if not which("ffprobe"):
        return 0.0
    import json
    import subprocess

    r = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "json",
            str(path),
        ],
        text=True,
        capture_output=True,
        check=False,
    )
    if r.returncode != 0:
        return 0.0
    data = json.loads(r.stdout or "{}")
    return float((data.get("format") or {}).get("duration") or 0)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--slug", required=True, help="topic slug for run folder name")
    ap.add_argument("--root", default="hooks", help="root dir for hook runs")
    ap.add_argument("--vo", action="append", default=[], help="hook voiceover path (repeat)")
    ap.add_argument("--vo-dir", default=None, help="folder of hook VO clips")
    ap.add_argument("--style-pack", default="insider-force-short")
    ap.add_argument("--width", type=int, default=1080)
    ap.add_argument("--height", type=int, default=1920)
    # Legacy optional: keep for stitch-later workflows
    ap.add_argument("--body", default=None, help="optional finished body mp4 (stitch later only)")
    ap.add_argument("--cut-at", type=float, default=None)
    args = ap.parse_args()

    vos = collect_vos(args.vo, args.vo_dir)
    if len(vos) < 1:
        die("provide --vo and/or --vo-dir with hook voiceovers")
    if len(vos) > 4:
        print(f"WARN: got {len(vos)} VOs — using first 4", file=sys.stderr)
        vos = vos[:4]

    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    run_id = f"{slugify(args.slug)}-{stamp}"
    root = Path(args.root).expanduser().resolve()
    run = ensure_dir(root / run_id)
    vo_dir = ensure_dir(run / "input" / "vo")
    ensure_dir(run / "analysis")
    ensure_dir(run / "assets" / "images")
    ensure_dir(run / "variants")
    ensure_dir(run / "renders")
    ensure_dir(run / "qa")

    vo_entries = []
    for i, src in enumerate(vos, start=1):
        hid = f"h{i}"
        ext = src.suffix.lower() or ".wav"
        dest = vo_dir / f"{hid}{ext}"
        shutil.copy2(src, dest)
        dur = probe_audio_duration(dest)
        ensure_dir(run / "analysis" / hid)
        ensure_dir(run / "variants" / hid)
        vo_entries.append(
            {
                "id": hid,
                "source": str(src),
                "path": f"input/vo/{hid}{ext}",
                "duration_s": round(dur, 3),
            }
        )
        if dur > 6.0:
            print(f"WARN: {hid} is {dur:.1f}s (>6s) — prefer shorter hook VOs", file=sys.stderr)

    body_meta = None
    if args.body:
        body_src = Path(args.body).expanduser().resolve()
        if not body_src.is_file():
            die(f"body not found: {body_src}")
        body_dest = run / "input" / "body.mp4"
        shutil.copy2(body_src, body_dest)
        probe = ffprobe_json(body_dest)
        write_json(run / "analysis" / "body-probe.json", probe)
        streams = probe.get("streams") or [{}]
        fmt = probe.get("format") or {}
        body_meta = {
            "path": "input/body.mp4",
            "width": int(streams[0].get("width") or args.width),
            "height": int(streams[0].get("height") or args.height),
            "duration_s": float(fmt.get("duration") or 0),
        }

    manifest = {
        "run_id": run_id,
        "mode": "vo_standalone",
        "style_pack": args.style_pack,
        "canvas": {"width": args.width, "height": args.height},
        "voiceovers": vo_entries,
        "body": body_meta,
        "cut_body_at": args.cut_at,
    }
    write_json(run / "input" / "manifest.json", manifest)

    hooks_stub = {
        "run_id": run_id,
        "mode": "vo_standalone",
        "style_pack": args.style_pack,
        "canvas": {"width": args.width, "height": args.height},
        "voiceovers": vo_entries,
        "body": body_meta,
        "cut_body_at": args.cut_at,
        "hooks": [],
        "notes": (
            "Agent: transcribe each VO, then fill hooks[] "
            "(formula/pattern/on_screen/visual) per schemas/hooks.schema.json. "
            "Render standalone hook-hN.mp4 — do not stitch to body unless asked."
        ),
    }
    write_json(run / "hooks.json", hooks_stub)

    print(f"run created: {run}")
    print(f"mode: vo_standalone  vos: {len(vo_entries)}  canvas: {args.width}x{args.height}")
    for e in vo_entries:
        print(f"  {e['id']}: {e['path']} ({e['duration_s']}s)")
    print("next: transcribe VOs -> fill hooks.json -> build/render each standalone hook")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

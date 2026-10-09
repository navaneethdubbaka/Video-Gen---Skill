#!/usr/bin/env python3
"""Copy user voiceover into project input/voiceover.<ext> and fingerprint it.

If the VO bytes change vs the last fingerprint, print INVALIDATE so agents do not
reuse old storyboard / assets / HyperFrames frames with a new narration.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _util import die, ensure_dir, resolve_project  # noqa: E402


AUDIO_EXTS = {".wav", ".mp3", ".m4a", ".aac", ".flac", ".ogg", ".wma"}

# Artifacts that MUST be rebuilt when VO content changes
INVALIDATE_PATHS = [
    "analysis/transcript.json",
    "storyboard/storyboard.json",
    "storyboard/entities.json",
    "composition/hyperframes/STORYBOARD.md",
    "composition/hyperframes/SCRIPT.md",
    "composition/hyperframes/audio_meta.json",
    "composition/hyperframes/caption_groups.json",
    "composition/hyperframes/compositions/captions.html",
    "composition/hyperframes/compositions/frames",
    "composition/hyperframes/index.html",
    "assets/images",
    "assets/metadata",
    "qa/report.json",
]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True)
    parser.add_argument("--source", required=True)
    parser.add_argument(
        "--invalidate",
        action="store_true",
        help="Delete stale VO-dependent artifacts when fingerprint changes",
    )
    args = parser.parse_args()

    project = resolve_project(args.project)
    src = Path(args.source).expanduser().resolve()
    if not src.is_file():
        die(f"voiceover not found: {src}")
    ext = src.suffix.lower() or ".wav"
    if ext not in AUDIO_EXTS:
        print(f"WARN: unusual audio extension {ext}", file=sys.stderr)

    dest_dir = ensure_dir(project / "input")
    for old in dest_dir.glob("voiceover.*"):
        old.unlink()
    dest = dest_dir / f"voiceover{ext}"
    shutil.copy2(src, dest)

    digest = sha256_file(dest)
    fp_path = project / "input" / "voiceover.sha256.json"
    prev = None
    if fp_path.is_file():
        try:
            prev = json.loads(fp_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            prev = None

    changed = bool(prev and prev.get("sha256") and prev.get("sha256") != digest)
    fp = {
        "sha256": digest,
        "bytes": dest.stat().st_size,
        "source": str(src),
        "path": str(dest.relative_to(project)).replace("\\", "/"),
        "ingested_at": datetime.now(timezone.utc).isoformat(),
        "previous_sha256": (prev or {}).get("sha256"),
        "changed": changed or prev is None,
    }
    fp_path.write_text(json.dumps(fp, indent=2) + "\n", encoding="utf-8")

    print(f"voiceover ready: {dest}")
    print(f"voiceover sha256: {digest}")

    if changed:
        print("VO_CHANGED=1")
        print(
            "INVALIDATE: new voiceover bytes — do NOT reuse old storyboard, "
            "assets, or composition frames. Re-transcribe, re-storyboard, "
            "re-research images, rebuild HyperFrames from scratch for this VO."
        )
        print("Invalidation targets:")
        for rel in INVALIDATE_PATHS:
            print(f"  - {rel}")
        if args.invalidate:
            removed = 0
            for rel in INVALIDATE_PATHS:
                target = project / rel
                if target.is_file():
                    target.unlink()
                    removed += 1
                elif target.is_dir():
                    shutil.rmtree(target)
                    removed += 1
            print(f"removed {removed} stale path(s)")
        else:
            print("Tip: re-run with --invalidate to delete those paths automatically.")
            print(
                "Preferred: init a NEW project slug for each distinct VO "
                "(never bolt a new VO onto videos/smoke-* or an old topic folder)."
            )
    else:
        print("VO_CHANGED=0 (same fingerprint as last ingest, or first ingest)")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

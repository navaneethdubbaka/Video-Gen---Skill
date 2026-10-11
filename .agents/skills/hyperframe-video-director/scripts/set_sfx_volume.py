#!/usr/bin/env python3
"""Set every SFX cue volume in audio_meta.json (default 0.8 = 80%).

Run AFTER faceless `audio.mjs fetch-sfx`, BEFORE `assemble-index.mjs`:

  python set_sfx_volume.py --project <PROJECT>
  python set_sfx_volume.py --project <PROJECT> --volume 0.8
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _util import die, read_json, resolve_project, write_json  # noqa: E402

DEFAULT_VOLUME = 0.8


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", required=True)
    parser.add_argument(
        "--volume",
        type=float,
        default=DEFAULT_VOLUME,
        help=f"linear gain 0..1 (default {DEFAULT_VOLUME} = 80%%)",
    )
    parser.add_argument(
        "--audio-meta",
        default=None,
        help="Path to audio_meta.json (default: <PROJECT>/composition/hyperframes/audio_meta.json)",
    )
    args = parser.parse_args()

    vol = float(args.volume)
    if not 0.0 <= vol <= 1.0:
        die(f"volume must be between 0 and 1, got {vol}")

    project = resolve_project(args.project)
    meta_path = (
        Path(args.audio_meta).expanduser().resolve()
        if args.audio_meta
        else project / "composition" / "hyperframes" / "audio_meta.json"
    )
    if not meta_path.is_file():
        die(f"audio_meta.json not found: {meta_path} (run fetch-sfx first)")

    meta = read_json(meta_path)
    sfx = meta.get("sfx")
    if not isinstance(sfx, list) or not sfx:
        die("audio_meta.json has empty sfx[] — run fetch-sfx before setting volume")

    updated = 0
    for cue in sfx:
        if not isinstance(cue, dict):
            continue
        prev = cue.get("volume")
        cue["volume"] = vol
        updated += 1
        if prev != vol:
            print(f"  sfx frame={cue.get('frame')} {cue.get('file')}: {prev} -> {vol}")

    meta["sfx"] = sfx
    write_json(meta_path, meta)
    print(f"set_sfx_volume: {updated} cue(s) at volume={vol} ({int(round(vol * 100))}%) -> {meta_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

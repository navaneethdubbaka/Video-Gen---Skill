#!/usr/bin/env python3
"""CLI: transcribe audio → transcript.json"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Allow `python …/transcription/cli.py` and package imports
HERE = Path(__file__).resolve().parent
SCRIPTS = HERE.parent
sys.path.insert(0, str(SCRIPTS))

from _util import die, load_dotenv, write_json  # noqa: E402
from transcription.provider import Transcript, transcribe  # noqa: E402


def load_fixture(path: Path) -> Transcript:
    from transcription.provider import TranscriptSegment, TranscriptWord

    data = json.loads(path.read_text(encoding="utf-8"))
    segs = [TranscriptSegment(**s) for s in data.get("segments", [])]
    words = [TranscriptWord(**{k: v for k, v in w.items() if k in ("text", "start", "end", "id", "type")}) for w in data.get("words", [])]
    return Transcript(
        language=data.get("language", "und"),
        segments=segs,
        words=words,
        text=data.get("text", ""),
        language_probability=data.get("language_probability"),
        audio_duration_secs=data.get("audio_duration_secs"),
        provider=data.get("provider", "fixture"),
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Transcribe voiceover (ElevenLabs STT)")
    parser.add_argument("--audio", help="Path to voiceover audio")
    parser.add_argument("--out", required=True, help="Output transcript.json")
    parser.add_argument("--provider", default="elevenlabs")
    parser.add_argument(
        "--fixture-transcript",
        help="Skip API; load this JSON as transcript (tests / offline)",
    )
    args = parser.parse_args()

    load_dotenv()
    out = Path(args.out)

    if args.fixture_transcript:
        t = load_fixture(Path(args.fixture_transcript))
    else:
        if not args.audio:
            die("--audio is required unless --fixture-transcript is set")
        t = transcribe(args.audio, provider=args.provider)

    write_json(out, t.to_dict())
    print(f"wrote {out} (language={t.language}, segments={len(t.segments)}, words={len(t.words)})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

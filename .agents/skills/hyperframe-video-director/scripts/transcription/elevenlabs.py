"""ElevenLabs Speech-to-Text (Scribe) provider."""

from __future__ import annotations

import json
import mimetypes
import os
import urllib.error
import urllib.request
from pathlib import Path

from _util import die, load_dotenv  # scripts/ on sys.path
from transcription.provider import Transcript, TranscriptWord, words_to_segments


API_URL = "https://api.elevenlabs.io/v1/speech-to-text"
DEFAULT_MODEL = "scribe_v1"


class ElevenLabsSTT:
    def __init__(self, api_key: str | None = None, model_id: str = DEFAULT_MODEL) -> None:
        load_dotenv()
        self.api_key = (api_key or os.environ.get("ELEVENLABS_API_KEY", "")).strip()
        self.model_id = model_id
        if not self.api_key:
            die(
                "ELEVENLABS_API_KEY is not set.\n"
                "Configure it before transcription:\n"
                "  PowerShell:  $env:ELEVENLABS_API_KEY = 'your-key'\n"
                "  Or copy .cursor/skills/hyperframe-video-director/.env.example to .env\n"
                "Never hardcode the key in source or SKILL.md."
            )

    def transcribe(self, audio_path: Path) -> Transcript:
        path = Path(audio_path)
        if not path.is_file():
            die(f"audio not found: {path}")

        boundary = "----hfDirectorBoundary7f3a9c"
        mime = mimetypes.guess_type(str(path))[0] or "application/octet-stream"
        file_bytes = path.read_bytes()

        fields = {
            "model_id": self.model_id,
            "timestamps_granularity": "word",
            "tag_audio_events": "false",
        }

        body = bytearray()
        for key, value in fields.items():
            body.extend(f"--{boundary}\r\n".encode())
            body.extend(f'Content-Disposition: form-data; name="{key}"\r\n\r\n'.encode())
            body.extend(f"{value}\r\n".encode())
        body.extend(f"--{boundary}\r\n".encode())
        body.extend(
            f'Content-Disposition: form-data; name="file"; filename="{path.name}"\r\n'.encode()
        )
        body.extend(f"Content-Type: {mime}\r\n\r\n".encode())
        body.extend(file_bytes)
        body.extend(b"\r\n")
        body.extend(f"--{boundary}--\r\n".encode())

        req = urllib.request.Request(
            API_URL,
            data=bytes(body),
            method="POST",
            headers={
                "xi-api-key": self.api_key,
                "Content-Type": f"multipart/form-data; boundary={boundary}",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=600) as resp:
                raw = json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            err = e.read().decode("utf-8", errors="replace")
            die(f"ElevenLabs STT HTTP {e.code}: {err[:2000]}")
        except urllib.error.URLError as e:
            die(f"ElevenLabs STT network error: {e}")

        return self._normalize(raw)

    def _normalize(self, raw: dict) -> Transcript:
        words_raw = raw.get("words") or []
        words: list[TranscriptWord] = []
        wi = 0
        for w in words_raw:
            wtype = w.get("type") or "word"
            text = w.get("text") or ""
            if wtype == "spacing":
                continue
            start = float(w["start"]) if w.get("start") is not None else 0.0
            end = float(w["end"]) if w.get("end") is not None else start
            if wtype == "word":
                tid = f"w{wi}"
                wi += 1
            else:
                tid = None
            words.append(
                TranscriptWord(
                    text=text,
                    start=start,
                    end=end,
                    id=tid,
                    type=wtype,
                )
            )

        segments = words_to_segments([w for w in words if w.type == "word"])
        text = (raw.get("text") or "").strip()
        if not text and segments:
            text = " ".join(s.text for s in segments)

        lang = raw.get("language_code") or raw.get("language") or "und"
        # normalize longer codes like "eng" → keep as returned; agent can map
        return Transcript(
            language=str(lang),
            segments=segments,
            words=words,
            text=text,
            language_probability=raw.get("language_probability"),
            audio_duration_secs=raw.get("audio_duration_secs"),
            provider="elevenlabs",
        )

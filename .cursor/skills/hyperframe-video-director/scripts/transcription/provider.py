"""Provider-agnostic transcription interface."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Protocol


@dataclass
class TranscriptWord:
    text: str
    start: float
    end: float
    id: str | None = None
    type: str = "word"


@dataclass
class TranscriptSegment:
    start: float
    end: float
    text: str


@dataclass
class Transcript:
    language: str
    segments: list[TranscriptSegment]
    words: list[TranscriptWord] = field(default_factory=list)
    text: str = ""
    language_probability: float | None = None
    audio_duration_secs: float | None = None
    provider: str = ""

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        return d


class TranscriptionProvider(Protocol):
    def transcribe(self, audio_path: Path) -> Transcript: ...


def words_to_segments(
    words: list[TranscriptWord],
    *,
    pause_gap: float = 0.55,
    max_segment_s: float = 4.5,
) -> list[TranscriptSegment]:
    """Group words into sentence-like segments using pauses and punctuation."""
    real = [w for w in words if (w.type or "word") == "word" and w.text.strip()]
    if not real:
        return []

    segments: list[TranscriptSegment] = []
    buf: list[TranscriptWord] = []

    def flush() -> None:
        nonlocal buf
        if not buf:
            return
        text = " ".join(w.text for w in buf).strip()
        text = " ".join(text.split())
        segments.append(TranscriptSegment(start=buf[0].start, end=buf[-1].end, text=text))
        buf = []

    for i, w in enumerate(real):
        buf.append(w)
        nxt = real[i + 1] if i + 1 < len(real) else None
        gap = (nxt.start - w.end) if nxt else 999.0
        ended = w.text.rstrip().endswith((".", "!", "?", "।", "?", "…"))
        long = (w.end - buf[0].start) >= max_segment_s
        if ended or gap >= pause_gap or long or nxt is None:
            flush()
    return segments


def transcribe(audio_path: Path | str, *, provider: str = "elevenlabs") -> Transcript:
    """Transcribe audio. Default provider: ElevenLabs Scribe."""
    path = Path(audio_path)
    if provider == "elevenlabs":
        from .elevenlabs import ElevenLabsSTT

        return ElevenLabsSTT().transcribe(path)
    raise ValueError(f"unknown transcription provider: {provider}")

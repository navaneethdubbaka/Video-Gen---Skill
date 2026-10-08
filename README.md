# Video Gen Skill — hyperframe-video-director

Reusable agent skill that creates short-form videos from:

1. A **reference** YouTube/local video (visual style only)
2. A **user voice-over** (Telugu or English) as the timing spine
3. Optional creative instructions

Composition and rendering are delegated to the existing **HyperFrames** skills. This repo does not fork HyperFrames.

## Skill location

```text
.cursor/skills/hyperframe-video-director/
```

### Install on other agents

| Host | Action |
| --- | --- |
| Cursor (this project) | Already under `.cursor/skills/` |
| Cursor (all projects) | Copy folder → `~/.cursor/skills/hyperframe-video-director` |
| Claude Code | Copy → `~/.claude/skills/hyperframe-video-director` (or project skills dir) |
| Google Antigravity | Copy into that product's skills directory |

## Configure ElevenLabs STT

```powershell
# PowerShell (session)
$env:ELEVENLABS_API_KEY = "your-key"

# or
copy .cursor\skills\hyperframe-video-director\.env.example .env
# edit .env and set ELEVENLABS_API_KEY=
```

Never commit `.env` or paste keys into prompts/JSON.

## Invoke in Cursor

```text
Use hyperframe-video-director.

Reference: ./reference.mp4
Voiceover: ./voiceover.wav
Optional: fast-paced documentary-style short.
```

### Frozen style pack (Insider Force / Colibri-look Short)

```text
Use hyperframe-video-director with style pack insider-force-short.

Voiceover: ./voiceover.wav
```

Pack path: `.cursor/skills/hyperframe-video-director/styles/insider-force-short/`  
Includes screenshot refs + `style-spec.json`. **No channel watermark** in outputs.

YouTube references work when `yt-dlp` is installed; otherwise provide a local file.

## Prerequisites

- Node.js ≥ 22 (HyperFrames CLI)
- Python 3.10+
- FFmpeg / ffprobe
- `npx hyperframes`
- Existing HyperFrames skills (`hyperframes`, `faceless-explainer`, `media-use`, …)
- `yt-dlp` (optional, for YouTube)
- `ELEVENLABS_API_KEY` (live transcription)

## Smoke test

```powershell
python tests/run_smoke.py
```

Uses fixtures under `tests/fixtures/`. Live STT runs only when `ELEVENLABS_API_KEY` is set; otherwise a fixture transcript validates the bridge.

## License / safety

Reference videos inform **style grammar** only. Do not copy copyrighted footage or logos into outputs.

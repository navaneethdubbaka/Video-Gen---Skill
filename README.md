# Video Gen Skill

Two project skills:

| Skill | Status | Use for |
| --- | --- | --- |
| [`hyperframe-video-director`](.cursor/skills/hyperframe-video-director/) | **Frozen** | Full short from reference style + VO |
| [`short-hooks`](.cursor/skills/short-hooks/) | Active | A/B **killer hook visuals** from short hook VOs (standalone clips) |

Composition/rendering → existing **HyperFrames** skills (not forked).

**Hard requirements for every video:** narration-relevant cached images (not SVG-only fakes), GSAP motion, mixed transitions, and boundary SFX.

**Entity images:** when VO names a public figure or famous company/brand, the skill fetches their Wikipedia/Commons image via `scripts/fetch_entity_image.py` and wires it into those scenes.

## Skill locations

```text
.cursor/skills/hyperframe-video-director/   # frozen full-pipeline director
.cursor/skills/short-hooks/                # hook A/B lab
```

### Install on other agents

Copy either/both folders into that host’s skills directory (Cursor / Claude Code / Antigravity). Also ship under `.agents/skills/` for Antigravity-style layouts.

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

### Antigravity / other agents (copy-paste)

```text
Use hyperframe-video-director with style pack insider-force-short.

Voiceover: <path-to-THIS-vo.wav>

CRITICAL:
- Create a NEW project slug from this VO's topic (videos/<topic-slug>/).
- Do NOT reuse videos/smoke-director-short or any older project's frames/assets.
- New VO ⇒ new transcript ⇒ new storyboard ⇒ new images ⇒ new HyperFrames frames.
- If you must reuse a folder, run ingest_voiceover.py --invalidate first.
- Captions: romanize Telugu to English spellings + karaoke highlight (prepare_captions.py).
- Real narration-matching images, GSAP motion, transitions + SFX, no watermark.
```

YouTube references work when `yt-dlp` is installed; otherwise provide a local file.

### short-hooks (standalone visuals from hook voiceovers)

```text
Use short-hooks. Style: insider-force-short.

Hook voiceovers:
  1) ./vo/hook-a.wav
  2) ./vo/hook-b.wav
  3) ./vo/hook-c.wav
```

Writes `hooks/<run-id>/renders/hook-hN.mp4` — **separate** attention-grabbing clips (not stitched to a full video).

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

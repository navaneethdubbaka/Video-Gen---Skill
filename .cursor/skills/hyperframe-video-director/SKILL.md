---
name: hyperframe-video-director
description: >
  Orchestrates short-form video creation from a reference video's visual style
  plus a user voice-over (Telugu or English). Analyzes reference grammar,
  transcribes VO via ElevenLabs STT, storyboards to VO timestamps, researches
  assets, then hands off composition/render to the existing HyperFrames skill
  (faceless-explainer pipeline). Use when the user provides a YouTube/local
  reference and a voiceover file, or asks for hyperframe-video-director /
  style-matched short / reference-style video with narration. Also use when the
  user names a style pack such as insider-force-short, Insider Force style,
  Colibri/Calibri laptop AI short look, or clean-tech sticker short.
---

# hyperframe-video-director

Orchestration skill. **You decide WHAT** (style, beats, assets, timing).  
**HyperFrames decides HOW** (HTML composition, animation, lint, render).

Do **not** recreate, fork, or replace HyperFrames. Do **not** invent a second renderer.

## When to use

User supplies (or paths equivalent to):

```text
Reference: <youtube-url | ./reference.mp4>
Voiceover: ./voiceover.wav
Optional instructions: …
```

## Hard rules

1. Voice-over timestamps are the **authoritative timeline** — never stretch/compress VO to fit visuals.
2. Reference video = **visual grammar only**. Never copy frames, footage, logos, or proprietary assets.
3. Prefer independently sourced assets (`/media-use` resolve, then cache).
4. Do not translate Telugu/English captions unless the user asks.
5. Secrets only from `ELEVENLABS_API_KEY` (env or local `.env`). Never hardcode keys.
6. Resume from existing artifacts; do not redo completed gates.
7. If a **style pack** is named (see [styles/README.md](styles/README.md)), load it and **skip** open-ended Step 4 analysis unless the user also supplies a new reference to re-analyze.
8. Style packs that forbid watermarks must ship **zero** channel URL footers (e.g. never `insiderforce.io`).
9. **Motion + transitions + SFX are mandatory.** Static HTML slides with silent hard cuts are a failed run. See [references/motion-and-sfx.md](references/motion-and-sfx.md).

## Style packs

| Pack | Load when user says… |
| --- | --- |
| [`insider-force-short`](styles/insider-force-short/SKILL.md) | Insider Force style, Colibri/Calibri short style, clean-tech sticker short, “style like that laptop AI video” |

On pack select: read the pack `SKILL.md`, copy its `style-spec.json` into the project, inspect its `refs/`, map scenes via its `scene-patterns.md`.

## Skill root

Resolve `SKILL_DIR` to this skill's directory (the folder containing this `SKILL.md`).

Scripts: `python <SKILL_DIR>/scripts/<name>.py …`

## Quick workflow

```text
Task Progress:
- [ ] 0 doctor
- [ ] 1 init project
- [ ] 2 ingest reference + voiceover
- [ ] 3 probe + extract frames
- [ ] 4 style_spec.json (agent)
- [ ] 5 transcribe VO → transcript.json
- [ ] 6 storyboard.json (agent)
- [ ] 7 assets (agent + cache)
- [ ] 8 HyperFrames handoff + compose
- [ ] 9 render draft → QA → iterate
- [ ] 10 promote final
```

Full checklist: [references/workflow.md](references/workflow.md)  
Handoff details: [references/hyperframes-handoff.md](references/hyperframes-handoff.md)  
Motion / SFX: [references/motion-and-sfx.md](references/motion-and-sfx.md)  
Safety: [references/safety.md](references/safety.md)

---

## Step 0 — Preflight

```bash
python <SKILL_DIR>/scripts/doctor.py
```

If `ELEVENLABS_API_KEY` is missing, stop and tell the user how to set it (see Configuration). Offline smoke tests may use `--fixture-transcript` only when the user/test explicitly allows it.

---

## Step 1 — Init project

Slug = kebab-case topic (not timestamp).

```bash
python <SKILL_DIR>/scripts/init_project.py --slug <project-slug> --root videos
```

Creates `videos/<slug>/` with `input/`, `analysis/`, `storyboard/`, `assets/`, `composition/`, `renders/`, `qa/`.

Work relative to `PROJECT=videos/<slug>` for the rest of the run.

---

## Step 2 — Ingest inputs

**Reference**

```bash
python <SKILL_DIR>/scripts/download_reference.py --project <PROJECT> --source <url-or-path>
```

- Local file → copy to `input/reference.mp4` (or keep extension).
- YouTube URL → `yt-dlp`. On failure: stop and ask for a local file. Do not silently continue.

**Voiceover**

```bash
python <SKILL_DIR>/scripts/ingest_voiceover.py --project <PROJECT> --source <path-to-audio>
```

---

## Step 3 — Probe + extract

```bash
python <SKILL_DIR>/scripts/probe_media.py --project <PROJECT>
python <SKILL_DIR>/scripts/extract_reference_frames.py --project <PROJECT>
```

Writes `analysis/media-probe.json` and `analysis/frames/`.

---

## Step 4 — Style analysis (agent)

**If a style pack is selected** (e.g. `insider-force-short`):

1. Read `styles/<pack>/SKILL.md` and follow it.
2. Copy `styles/<pack>/style-spec.json` → `<PROJECT>/analysis/style-spec.json`.
3. Inspect pack `refs/` with vision (do not re-derive blindly).
4. Skip open-ended analysis unless the user asks to refresh the pack from a new reference.

**Otherwise** (custom reference):

Read [references/style-analysis.md](references/style-analysis.md).  
Inspect extracted frames with vision tools + probe JSON.  
Write `analysis/style-spec.json` (schema: [schemas/style-spec.schema.json](schemas/style-spec.schema.json)).  
Also write `analysis/reference-analysis.json` (free-form notes backing the spec).

Extract grammar (pacing, typography, palette, motion, transitions) — **not** pixel copies.

---

## Step 5 — Transcribe voiceover

```bash
python <SKILL_DIR>/scripts/transcription/cli.py --audio <PROJECT>/input/voiceover.* --out <PROJECT>/analysis/transcript.json
```

Requires `ELEVENLABS_API_KEY`. Output preserves language + segment/word timestamps. Do not translate.

---

## Step 6 — Storyboard (agent)

Read [references/storyboard-guide.md](references/storyboard-guide.md).  
Build `storyboard/storyboard.json` from transcript segments + style-spec + user instructions.  
Schema: [schemas/storyboard.schema.json](schemas/storyboard.schema.json).

Each scene: narration window, concept, visual type/query, on-screen text, **motion**, **transition**, **sfx** — timed to VO.

Do not leave `transition: hard_cut` on every scene. Mix `zoom-through`, `push-slide`, `crossfade`, `blur-crossfade`, `squeeze` with cuts. Every scene needs an `sfx` cue (`whoosh` / `pop` / `hit` / `rise`). See [references/motion-and-sfx.md](references/motion-and-sfx.md).

---

## Step 7 — Assets (agent)

Read [references/asset-research.md](references/asset-research.md).

For each scene needing media:

1. Prefer `/media-use`:
   `node <media-use>/scripts/resolve.mjs --type image --intent "…" --project <PROJECT>/composition/hyperframes`
2. Else search/download candidates, **inspect with vision**, then:
   `python <SKILL_DIR>/scripts/cache_asset.py --project <PROJECT> --file <path> --query "…" --kind images --usage scene_03`
3. Reject assets that fight caption placement (subject filling the text zone).

---

## Step 8 — HyperFrames handoff

Follow [references/hyperframes-handoff.md](references/hyperframes-handoff.md) exactly.

Summary:

1. Read `/hyperframes`, then `/faceless-explainer` + `/hyperframes-core` + `/media-use` as needed.
2. `npx hyperframes skills update faceless-explainer`
3. `npx hyperframes init "<PROJECT>/composition/hyperframes" --non-interactive --example=blank`
4. Bridge scripts (deterministic):

```bash
python <SKILL_DIR>/scripts/style_spec_to_frame_md.py --project <PROJECT>
python <SKILL_DIR>/scripts/storyboard_to_hyperframes.py --project <PROJECT>
python <SKILL_DIR>/scripts/build_audio_meta_from_vo.py --project <PROJECT>
```

5. Agent builds `compositions/frames/NN-*.html` with **GSAP entrances** (faceless frame-worker + `/hyperframes-animation`). No static posters.
6. Faceless pipeline — **do not TTS** the user's VO:

```bash
# cwd = composition/hyperframes
node <FACELESS>/scripts/captions.mjs build --storyboard ./STORYBOARD.md --audio-meta ./audio_meta.json --hyperframes .
node <FACELESS>/scripts/audio.mjs fetch-sfx --storyboard ./STORYBOARD.md --hyperframes . --audio-meta ./audio_meta.json
node <FACELESS>/scripts/assemble-index.mjs --storyboard ./STORYBOARD.md --hyperframes . --audio-meta ./audio_meta.json
node <FACELESS>/scripts/transitions.mjs inject --storyboard ./STORYBOARD.md --hyperframes .
node <FACELESS>/scripts/transitions.mjs verify --storyboard ./STORYBOARD.md --index ./index.html
```

7. Confirm `audio_meta.json` has non-empty `sfx` and transitions inject is not `0 transitions` (unless jump-cut-only was requested).
8. `npx hyperframes lint` → `check` → `snapshot`.

---

## Step 9 — QA + iterate

```bash
python <SKILL_DIR>/scripts/qa_report.py --project <PROJECT>
```

Plus visual review per [references/qa-checklist.md](references/qa-checklist.md) against snapshots and style-spec.

On failure: fix scene → re-assemble → re-check → `renders/draft/vN.mp4`.

---

## Step 10 — Final

```bash
npx hyperframes render --quality high --output renders/video.mp4
```

(run inside `composition/hyperframes`). Copy to `<PROJECT>/renders/final/final.mp4`.

---

## Configuration

```bash
# PowerShell
$env:ELEVENLABS_API_KEY = "your-key"

# or copy skill .env.example → workspace/project .env
```

Never commit `.env` or keys into SKILL.md / JSON / git.

---

## Minimal invoke example

```text
Use hyperframe-video-director.

Reference: ./reference.mp4
Voiceover: ./voiceover.wav
Optional: fast-paced documentary-style short.
```

### Style-pack example (no new reference analysis)

```text
Use hyperframe-video-director with style pack insider-force-short.

Voiceover: ./voiceover.wav
Optional: no watermark; clean tech sticker look.
```

Autonomous mode if the user says "just build it" / "surprise me".

---

## Portability

Filesystem + Python/Node CLIs + HyperFrames skills. Minimal agent-specific APIs.  
Install: copy this folder to `.cursor/skills/`, `~/.cursor/skills/`, or the host agent's skills directory (Claude Code / Antigravity).

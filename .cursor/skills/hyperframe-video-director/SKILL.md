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
4. **Do not translate** Telugu meaning into English. For on-screen captions, **romanize** Telugu script into Latin/English spellings (e.g. `ane kotta chesindi`) via `prepare_captions.py`. Keep English words as-is.
5. **Karaoke captions are mandatory.** Spoken words must use `.is-active` / `.is-spoken` highlight (not a plain dual-tone pill). Run `prepare_captions.py` after `captions.mjs build`.
6. Secrets only from `ELEVENLABS_API_KEY` (env or local `.env`). Never hardcode keys.
7. Resume from existing artifacts; do not redo completed gates.
8. If a **style pack** is named (see [styles/README.md](styles/README.md)), load it and **skip** open-ended Step 4 analysis unless the user also supplies a new reference to re-analyze.
9. Style packs that forbid watermarks must ship **zero** channel URL footers (e.g. never `insiderforce.io`).
10. **Motion + transitions + SFX are mandatory.** Static HTML slides with silent hard cuts are a failed run. See [references/motion-and-sfx.md](references/motion-and-sfx.md).
11. **Relevant real images are mandatory.** Every scene (except ≤20% kinetic `text_only`) must research, download, vision-inspect, and cache a narration-matching image; set `visual.asset_path` and use it in frame HTML. Invented SVG/CSS-only “fake assets” are a failed run. See [references/asset-research.md](references/asset-research.md).
12. **Public figures & famous companies:** when VO names a recognizable person, company, brand, or product, fetch that entity’s image (Wikipedia/Wikimedia via script) and use it in those scenes. See [references/entity-images.md](references/entity-images.md).

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
- [ ] 7 assets researched + cached + asset_path set (GATE)
- [ ] 7b qa_report assets pass
- [ ] 8 HyperFrames handoff + compose (frames use real imgs)
- [ ] 9 render draft → QA → iterate
- [ ] 10 promote final
```

Full checklist: [references/workflow.md](references/workflow.md)  
Handoff details: [references/hyperframes-handoff.md](references/hyperframes-handoff.md)  
Motion / SFX: [references/motion-and-sfx.md](references/motion-and-sfx.md)  
Assets: [references/asset-research.md](references/asset-research.md)  
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

Each scene: narration window, concept, **visual.search_query**, on-screen text, **motion**, **transition**, **sfx** — timed to VO.

Prefer `visual.type`: `photograph` | `screenshot` | `icon` | `video_clip`.  
`text_only` ≤20% of scenes. Do **not** default to `generated_graphic` to skip research.

Do not leave `transition: hard_cut` on every scene. Mix `zoom-through`, `push-slide`, `crossfade`, `blur-crossfade`, `squeeze` with cuts. Every scene needs an `sfx` cue (`whoosh` / `pop` / `hit` / `rise`). See [references/motion-and-sfx.md](references/motion-and-sfx.md).

---

## Step 7 — Assets (agent) — HARD GATE

Read [references/asset-research.md](references/asset-research.md) and [references/entity-images.md](references/entity-images.md). **Do this before any frame HTML.**

### 7a — Entity images (public figures / famous companies)

From transcript + storyboard, list named public entities → write `analysis/entities.json` with `name`, `type`, `scene_ids`.

```bash
python <SKILL_DIR>/scripts/fetch_entity_image.py --project <PROJECT> --entities analysis/entities.json
python <SKILL_DIR>/scripts/apply_entity_assets.py --project <PROJECT>
```

Vision-check each file under `assets/images/entities/`. Tag scenes with `"visual": { "entity": "<Name>" }`.

### 7b — Remaining scenes

For **every** non-`text_only` scene still missing `asset_path`:

1. Write a narration-specific `search_query` + `requirement.narration_link`.
2. Prefer `/media-use`:
   `node <media-use>/scripts/resolve.mjs --type image --intent "…" --project <PROJECT>/composition/hyperframes`
3. Else web search → download 2–4 candidates → **vision-inspect for relevance** → pick one.
4. Cache:
   `python <SKILL_DIR>/scripts/cache_asset.py --project <PROJECT> --file <path> --query "…" --kind images --usage scene_03`
5. Set `visual.asset_path` in `storyboard.json`.
6. Reject irrelevant, watermarked, or caption-hostile crops.

Then:

```bash
python <SKILL_DIR>/scripts/qa_report.py --project <PROJECT> --phase assets
```

**STOP** if image-related errors remain (`missing_asset_path`, `too_many_text_only`, `asset_file_missing`, `entity_unresolved`, …). Do not compose frames yet.

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

5. Agent builds `compositions/frames/NN-*.html` with **real `<img>` heroes from `asset_path`** + **GSAP entrances** on `window.__timelines[id]` (faceless frame-worker + `/hyperframes-animation`). No SVG-only fake assets. No static posters.
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

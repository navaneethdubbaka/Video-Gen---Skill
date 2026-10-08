# HyperFrames handoff

This skill never renders video itself. After `style-spec.json`, `transcript.json`, `storyboard.json`, and assets exist, hand off to the **existing** HyperFrames ecosystem.

**Motion + SFX are mandatory.** Read [motion-and-sfx.md](motion-and-sfx.md) before building frames. A silent hard-cut slideshow of static HTML is a failed deliverable.

## Skills to read (in order)

1. `/hyperframes` — router (confirm you are not inventing a new engine)
2. `/faceless-explainer` — narration-timed modular frame pipeline (adapted; skip TTS)
3. `/hyperframes-core` — `data-*` contract, storyboard format, media-at-root rules
4. `/hyperframes-animation` — motion rules for frame workers (**required**)
5. `/media-use` — resolve BGM/SFX/images; **do not** use its STT for the VO (ElevenLabs already did)
6. `/hyperframes-cli` — lint / check / snapshot / preview / render

Keep skills current:

```bash
npx hyperframes skills update faceless-explainer
```

## Project path

```text
<PROJECT>/composition/hyperframes/
```

## Steps

### A. Init

If `hyperframes.json` is missing:

```bash
npx hyperframes init "<PROJECT>/composition/hyperframes" --non-interactive --example=blank
```

Optional: `npx hyperframes auth status` (relay verbatim). Autonomous runs may continue offline.

### B. Design system from style-spec

```bash
python <SKILL_DIR>/scripts/style_spec_to_frame_md.py --project <PROJECT>
```

### C. Storyboard + script bridge

```bash
python <SKILL_DIR>/scripts/storyboard_to_hyperframes.py --project <PROJECT>
```

Writes `STORYBOARD.md` with `transition_in` + `sfx:` on every frame, and `SCRIPT.md` for captions only.

**Do not** call faceless `audio.mjs` generate / TTS. The user's voice file is authoritative.

Confirm the printed `non-cut` count is > 0 when there are 3+ scenes. If not, edit storyboard transitions and re-run the bridge.

### D. VO → audio_meta

```bash
python <SKILL_DIR>/scripts/build_audio_meta_from_vo.py --project <PROJECT>
```

Produces frame-keyed voices. `sfx` may still be empty until fetch-sfx.

### E. Stage assets

Copy selected images into `composition/hyperframes/public/` or `assets/`. Prefer `resolve --adopt`.

### F. Build frames with real motion (agent) — CRITICAL

Follow faceless Step 4–5 + `/hyperframes-animation`:

- One HTML file per frame: `compositions/frames/NN-<slug>.html` in `<template>`
- **Every frame** must register a seekable GSAP timeline (`window.__timelines["id"]`)
- Hero: entrance scale/opacity/y; captions: staggered dual-tone reveals
- Idle micro-motion so holds never feel frozen
- Match style pack patterns; update `STORYBOARD.md` `src:` + `status: animated`

Static full-bleed `<img>` with no timeline = reject and rebuild that frame.

### G. Captions

```bash
node <FACELESS>/scripts/captions.mjs build \
  --storyboard ./STORYBOARD.md \
  --audio-meta ./audio_meta.json \
  --hyperframes .
```

### H. Fetch transition SFX (required)

```bash
node <FACELESS>/scripts/audio.mjs fetch-sfx \
  --storyboard ./STORYBOARD.md \
  --hyperframes . \
  --audio-meta ./audio_meta.json
```

Merges SFX into `audio_meta.json` without wiping VO. Optional light BGM via media-use resolve + manual `bgm` entry (ducked under voice) — never replace VO.

Verify `audio_meta.json` has a non-empty `sfx` array before continuing.

### I. Assemble

```bash
node <FACELESS>/scripts/assemble-index.mjs \
  --storyboard ./STORYBOARD.md \
  --hyperframes . \
  --audio-meta ./audio_meta.json
```

### J. Inject + verify transitions (required)

```bash
node <FACELESS>/scripts/transitions.mjs inject --storyboard ./STORYBOARD.md --hyperframes .
node <FACELESS>/scripts/transitions.mjs verify --storyboard ./STORYBOARD.md --index ./index.html
```

If inject reports `0 transitions (all cuts)`, diversify `transition_in` (zoom-through / push-slide / crossfade), re-bridge or edit STORYBOARD, re-assemble, inject again.

### K. Validate

```bash
npx hyperframes lint
npx hyperframes check
npx hyperframes snapshot --frames 9
```

QA: [qa-checklist.md](qa-checklist.md) + [motion-and-sfx.md](motion-and-sfx.md) gates. Listen for SFX on boundaries in preview when possible.

### L. Render

```bash
npx hyperframes render --quality draft --output ../../renders/draft/v1.mp4
npx hyperframes render --quality high --output ../../renders/final/final.mp4
```

## What you must not do

- Ship static HTML “slides” with no GSAP
- Skip `fetch-sfx` or `transitions.mjs inject`
- Call TTS to replace the user voiceover
- Embed reference video frames / channel watermarks
- Leave `sfx: []` in final `audio_meta.json`

## Duration authority

Scene lengths come from VO segments. Do **not** run `audio.mjs sync-durations` against generated TTS.

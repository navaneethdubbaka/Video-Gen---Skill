# HyperFrames handoff

This skill never renders video itself. After `style-spec.json`, `transcript.json`, `storyboard.json`, and assets exist, hand off to the **existing** HyperFrames ecosystem.

## Skills to read (in order)

1. `/hyperframes` — router (confirm you are not inventing a new engine)
2. `/faceless-explainer` — narration-timed modular frame pipeline (adapted; skip TTS)
3. `/hyperframes-core` — `data-*` contract, storyboard format, media-at-root rules
4. `/hyperframes-animation` — motion rules for frame workers
5. `/media-use` — resolve BGM/SFX/images; **do not** use its STT for the VO (ElevenLabs already did)
6. `/hyperframes-cli` — lint / check / snapshot / preview / render

Keep skills current:

```bash
npx hyperframes skills update faceless-explainer
```

## Project path

HyperFrames root:

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

### B. Design system from style-spec (not a stock preset)

```bash
python <SKILL_DIR>/scripts/style_spec_to_frame_md.py --project <PROJECT>
```

Writes `composition/hyperframes/frame.md` seeded from `analysis/style-spec.json` (aspect, palette, type position, motion language). Agent may refine `frame.md` to match grammar more tightly, but must not discard VO timing.

### C. Storyboard + script bridge

```bash
python <SKILL_DIR>/scripts/storyboard_to_hyperframes.py --project <PROJECT>
```

Writes:

- `STORYBOARD.md` — frame durations from scene `end - start`, transitions, voiceover guide text
- `SCRIPT.md` — narration text for caption grouping **only**

**Do not** call faceless `audio.mjs` generate / TTS. The user's voice file is authoritative.

### D. VO → audio_meta

```bash
python <SKILL_DIR>/scripts/build_audio_meta_from_vo.py --project <PROJECT>
```

- Splits `input/voiceover.*` into per-scene clips under `composition/hyperframes/assets/voices/NN.ext`
- Remaps transcript words to **frame-relative** times
- Writes frame-keyed `audio_meta.json` consumed by faceless assemblers:

```json
{
  "voices": [
    {
      "frame": 1,
      "path": "assets/voices/01.wav",
      "duration_s": 2.2,
      "words": [{ "id": "w0", "text": "Hello", "start": 0.0, "end": 0.4 }]
    }
  ],
  "bgm": null,
  "sfx": []
}
```

Optional BGM/SFX later via media-use / faceless `fetch-sfx` — never regenerate VO.

### E. Stage director assets into HyperFrames

Copy selected `assets/images/…` into `composition/hyperframes/public/` or `assets/` and reference from frame HTML. Prefer `resolve --adopt` when using media-use ledger.

### F. Visual design + build frames (agent)

Follow faceless-explainer Step 4–5 spirit:

- Enrich mental/shot plan from storyboard (no HTML until ready)
- One HTML file per frame: `compositions/frames/NN-<slug>.html` wrapped in `<template>`
- Match `style-spec` + `frame.md`
- Dispatch per-frame work like faceless `sub-agents/frame-worker.md`
- Update `STORYBOARD.md` `src:` + `status:` as frames land

### G. Captions + assemble (existing scripts)

Locate faceless skill scripts (typical: `~/.cursor/skills/faceless-explainer/scripts/`):

```bash
node <FACELESS>/scripts/captions.mjs build \
  --storyboard ./STORYBOARD.md \
  --audio-meta ./audio_meta.json \
  --hyperframes .

node <FACELESS>/scripts/assemble-index.mjs \
  --storyboard ./STORYBOARD.md \
  --hyperframes . \
  --audio-meta ./audio_meta.json
```

(Run with cwd = `composition/hyperframes`.)

### H. Validate

```bash
npx hyperframes lint
npx hyperframes check
npx hyperframes snapshot --frames 9
```

Then director QA (`qa_report.py` + visual checklist).

### I. Render

```bash
npx hyperframes render --quality draft --output ../../renders/draft/v1.mp4
# after QA pass:
npx hyperframes render --quality high --output ../../renders/final/final.mp4
```

Paths relative to `composition/hyperframes`.

## What you must not do

- Implement a custom MP4 compositor / alternate HTML runtime
- Call TTS to replace the user voiceover
- Embed reference video frames as the content bed
- Skip lint/check because "it looked fine in the browser once"

## Duration authority

Scene lengths come from VO segments. If HyperFrames sync helpers want to rewrite durations from TTS, **do not** run `audio.mjs sync-durations` against generated TTS — durations are already correct from `build_audio_meta_from_vo.py` / storyboard bridge.

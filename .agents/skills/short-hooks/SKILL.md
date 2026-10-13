---
name: short-hooks
description: >
  Turns 3–4 short hook voice-overs into separate killer attention-grabbing
  visual clips (standalone — not stitched to a full video). Transcribes each
  VO, designs a sticker/big-number hook visual timed to that audio, renders
  one MP4 per hook for A/B testing openings. Use when the user says
  short-hooks, hook VO, hook visuals only, A/B hooks from voiceover, or
  provides multiple short hook audio files. Does not rebuild a full short
  and does not require a finished body video.
---

# short-hooks

**Hook VO in → killer visual out.** Each hook is its **own** short clip.

You receive 3–4 short voice-overs (one per hook idea). For each VO you
transcribe, design a scroll-stopping visual (pattern A sticker or B big-number),
compose + render a standalone MP4 with that VO baked in. No full-video rebuild.
No stitching onto a body unless the user **explicitly** asks later.

Do **not** modify frozen `hyperframe-video-director`. Do **not** invent a second
renderer — HyperFrames + ffmpeg only.

## When to use

```text
Use short-hooks.

Style: insider-force-short   # optional
Hook VOs:
  1) ./hooks-vo/h1.wav
  2) ./hooks-vo/h2.wav
  3) ./hooks-vo/h3.wav
  4) ./hooks-vo/h4.wav   # optional
```

Or a folder of short clips: `Hook VO folder: ./hooks-vo/`

## Hard rules

1. **Input = hook voice-overs only.** Visuals are invented per VO — not taken from a finished long video.
2. **One VO → one standalone MP4.** Do not concat hooks together; do not attach a body by default.
3. **3–4 variants.** If user gives 1–2 VOs, still produce distinct formulas (ask for more VO only if duration/topic is unclear).
4. Each hook duration follows **that VO’s length** (prefer 1.5–5s; warn if >6s).
5. On-screen text **≤ 6 words**, pattern **A or B**, curiosity/shock — not textbook titles.
6. Distinct `formula` per variant ([hook-formulas.md](references/hook-formulas.md)).
7. VO is authoritative audio — never replace with TTS. Captions: romanize Telugu, karaoke highlight.
8. SFX entrance at volume **0.8**. Seekable GSAP `window.__timelines` required.
9. Default canvas **9:16 1080×1920** + `insider-force-short` grammar unless user says otherwise.
10. Output: `hooks/<run-id>/renders/hook-<id>.mp4` only (stitch-to-body is **optional**, separate ask).

## Skill root

`SKILL_DIR` = folder containing this `SKILL.md`.  
Director scripts (STT): `<DIRECTOR_DIR>/scripts/transcription/cli.py`  
`DIRECTOR_DIR` = sibling `../hyperframe-video-director` when present.

## Quick workflow

```text
Task Progress:
- [ ] 0 doctor
- [ ] 1 init run (copy hook VOs)
- [ ] 2 transcribe each VO → analysis/hN/transcript.json
- [ ] 3 write hooks.json recipes (formula + visual + on_screen)
- [ ] 4 research/cache 1 hero asset per hook (sticker/UI/number)
- [ ] 5 build HyperFrames variant per hook (VO + visual + SFX)
- [ ] 6 render hooks/<run>/renders/hook-hN.mp4
- [ ] 7 QA frames + deliver table
```

Details: [references/workflow.md](references/workflow.md)  
Formulas: [references/hook-formulas.md](references/hook-formulas.md)

---

## Step 0 — Doctor

```bash
python <SKILL_DIR>/scripts/doctor.py
```

Needs: ffmpeg, ffprobe, Node/npx hyperframes, `ELEVENLABS_API_KEY` for live STT.

---

## Step 1 — Init run (VO inputs)

```bash
python <SKILL_DIR>/scripts/init_run.py \
  --slug <topic-slug> \
  --vo ./h1.wav \
  --vo ./h2.wav \
  --vo ./h3.wav \
  --style-pack insider-force-short
```

Or:

```bash
python <SKILL_DIR>/scripts/init_run.py --slug <topic> --vo-dir ./hooks-vo/
```

Creates:

```text
hooks/<run-id>/
  input/vo/h1.wav …
  input/manifest.json
  analysis/h1/ …          # transcripts later
  hooks.json              # recipes (Step 3)
  variants/h1/hyperframes/
  renders/hook-h1.mp4 …
  qa/
```

---

## Step 2 — Transcribe each VO

For each `input/vo/hN.*`:

```bash
python <DIRECTOR_DIR>/scripts/transcription/cli.py \
  --audio hooks/<run>/input/vo/hN.wav \
  --out hooks/<run>/analysis/hN/transcript.json
```

Duration = transcript / ffprobe length. Do not stretch VO.

---

## Step 3 — Recipes (agent)

Read [references/hook-formulas.md](references/hook-formulas.md).  
Fill `hooks.json` ([schemas/hooks.schema.json](schemas/hooks.schema.json)):

| Field | Rule |
| --- | --- |
| `id` | `h1`…`h4` matching VO file |
| `vo_path` | `input/vo/hN.ext` |
| `formula` | unique across variants |
| `pattern` | `A` or `B` |
| `on_screen` | ≤6 words from VO meaning (romanize if Telugu) |
| `visual.search_query` | narration-tied sticker/UI/number |
| `duration_s` | = VO duration (cap warn >6s) |
| `sfx` | `pop` or `hit` |
| `why_it_stops_scroll` | one line |

Sharpen on-screen wording; **do not change** what the VO claims.

---

## Step 4 — Assets

One real image per hook (sticker cutout / UI crop / device for big number).  
Prefer `/media-use` resolve + director `cache_asset.py` into `hooks/<run>/assets/`.  
No generic crystal-brain stock. Pattern B may be type-led with a light device plate.

---

## Step 5 — Build each variant

Under `variants/<id>/hyperframes/`:

1. `npx hyperframes init … --non-interactive --example=blank`
2. Single composition timed to VO duration; mount VO as voice track
3. Visual: insider-force sticker or giant number; dual-tone ≤6 words
4. Slim karaoke captions from transcript words (romanize Telugu)
5. Entrance SFX @ 0.8; `window.__timelines[id]` seekable GSAP
6. Read `/hyperframes-animation` + `/motion-graphics` for pop/kinetic

---

## Step 6 — Render

```bash
# cwd = variants/hN/hyperframes
npx hyperframes render --quality high --output ../../renders/hook-hN.mp4
```

Deliverable = these standalone files. **Stop here** unless user asks to stitch onto a body ([stitch.md](references/stitch.md) optional).

---

## Step 7 — QA + deliver

- [ ] Each MP4 audio = that hook VO (not silence, not TTS)
- [ ] ≤6 words on screen; A/B pattern; distinct formulas
- [ ] Pop/punch in first 0.5s; no watermark
- [ ] Frame grab at t=0.4s → `qa/hN.jpg`

| Hook | Formula | On-screen | File |
| --- | --- | --- | --- |
| h1 | shock_claim | … | `renders/hook-h1.mp4` |

## Invoke example

```text
Use short-hooks. Style: insider-force-short.

Hook voiceovers:
  1) ./vo/hook-next-word.wav
  2) ./vo/hook-117m.wav
  3) ./vo/hook-no-finetune.wav
```

Each becomes its own attention-grabbing visual clip for testing which opening hits.

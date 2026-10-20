---
name: host-mouth-talk
description: >
  Turn a single illustrated portrait (or the greencode host_stills pack) into a
  seamless talking-mouth loop via mouth-ROI warp. Use when the user asks for
  talking mouth, animate mouth, mouth loop, host talking GIF/WebP, or to batch
  greencode/my_animations/host_stills into host_talking/.
---

# host-mouth-talk

Mouth-only talking loop for illustrated portraits (Claude mouth-warp algorithm).

Does **not** redraw lips. It fills the mouth hole with nearby skin, then vertically
scales the mouth ROI with the top lip anchored so the lower lip opens/closes on a
syllable-like rhythm (96 frames @ 24fps, seamless loop).

## When to use

- “Make this image talk” / talking mouth / mouth loop
- Batch update `greencode/my_animations/host_stills` → `host_talking/`
- After new host PNGs are dropped and need talking assets for video-gen
- **Key user talking GIFs** in `host_talking_loop_gif/` (green screen → alpha WebP for compose)

## Preferred video pipeline (greencode)

User drops green-screen talking GIFs → key → catalog `talking_primary` points at `host_talking/<id>/talking_loop.webp`:

```bash
python .cursor/skills/host-mouth-talk/scripts/key_talking_loop_gifs.py
```

Maps e.g. `presenting_talking_loop.gif` → `host_talking/present/`. Skips `shock`.

## Hard rules

1. **Calib required for warp batch.** Anime faces are unreliable for auto landmarks — each expression needs `calib/<id>.json`.
2. **Preserve alpha** on every frame (keyed WebP/GIF or PNG alpha).
3. **Never animate `shock`** — banned in the greencode catalog.
4. Compose prefers **`talking_loop.webp`** (alpha). Do not chroma-key again in HTML.
5. Video-gen must **not** stack infinite GSAP yoyo on top of the mouth loop — entrance only.

## Quick single image

```bash
pip install opencv-python numpy
python .cursor/skills/host-mouth-talk/scripts/animate_mouth.py your_image.png out_folder --calib .cursor/skills/host-mouth-talk/calib/talk_loop.json
```

Writes `out_folder/frames/f%03d.png` + `openness.txt`.

Encode:

```powershell
.cursor/skills/host-mouth-talk/scripts/encode_loops.ps1 -OutDir out_folder
```

## Batch greencode hosts

```bash
python .cursor/skills/host-mouth-talk/scripts/batch_host_stills.py
python .cursor/skills/host-mouth-talk/scripts/batch_host_stills.py --encode
```

Outputs:

```text
greencode/my_animations/host_talking/<id>/
  frames/
  talking_loop.gif
  talking_loop.webp
  talking_loop.mp4
  openness.txt
```

## Calib JSON shape

```json
{
  "poly": [[443, 420], [452, 416], "..."],
  "anchor_y": 413.0,
  "cx": 488.0,
  "skin_sample": [440, 446, 455, 482],
  "box": [388, 466, 416, 560],
  "roi": [420, 556, 392, 462],
  "ref_size": [1024, 1024]
}
```

`poly` / coords are in **source image pixels**. Bootstrap with `scripts/bootstrap_calib.py` then QA-fix mid-open frames.

## After batch

1. Update `greencode/my_animations/catalog.json` to `talking_primary` (paths to WebP).
2. Compose via hyperframe-video-director / greencode-video-gen using resolved talking assets.

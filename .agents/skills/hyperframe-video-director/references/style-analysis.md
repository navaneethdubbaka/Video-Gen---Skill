# Style analysis

Goal: extract a **reusable visual grammar** into `analysis/style-spec.json`.

Not a goal: recreate frames, logos, or footage from the reference.

## Inputs

- `analysis/media-probe.json` (aspect, resolution, duration, fps)
- `analysis/frames/*.jpg` (sampled stills — inspect with vision)
- Optional: watch pacing by comparing consecutive frames

## Extract

| Area | Look for |
| --- | --- |
| Format | aspect ratio, resolution, fps |
| Pacing | avg shot length, cut frequency, density |
| Typography | face feel, weight, size, position, caption rail vs keyword punch |
| Color | dominant palette, background treatment, contrast |
| Imagery | photo / screenshot / illustration / icon / diagram / chart mix |
| Treatment | full-bleed, inset, letterbox, overlays, scrims |
| Motion | zoom, pan, parallax, punch-ins |
| Transitions | hard cut, dissolve, wipe, whip |
| Hierarchy | what reads first; where text sits vs subject |
| Timing drivers | narration-driven vs beat-driven cuts |

## Process

1. Read probe for format facts.
2. Inspect 8–20 frames spanning the video (not only the first).
3. Infer average shot duration from visible cut changes when possible.
4. Write `style-spec.json` using the schema; adapt fields — do not invent fake precision.
5. Write `reference-analysis.json` with short evidence notes (what you saw).

## Consistency loop (later)

For every scene you build, compare:

```text
REFERENCE STYLE → style-spec → CURRENT SCENE
```

Check typography, spacing, pacing, image treatment, motion, density, transitions.

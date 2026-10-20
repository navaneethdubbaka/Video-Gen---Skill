# Character catalog — greencode-video-gen

**Primary host assets = talking mouth WebPs** (from `host-mouth-talk`).

```text
greencode/my_animations/
  catalog.json          # mode: talking_primary
  host_talking/<id>/talking_loop.webp   # USE THESE in compose
  host_stills/<id>.png                  # masters / fallback
  new/                                  # green-screen drops
```

Build/rebuild talking loops: `.cursor/skills/host-mouth-talk/` (per-image mouth calib — sizes differ).

## Resolve

```bash
python <SKILL_DIR>/scripts/resolve_host_expression.py --expression talk_emph
python <SKILL_DIR>/scripts/resolve_host_expression.py --list
python <SKILL_DIR>/scripts/resolve_host_expression.py --validate
```

Returns `host_stills/<id>.png` paths when catalog `mode` is `stills_primary`.

## Picker rules

| Cue | Prefer |
| --- | --- |
| Pattern `A` hook | `hang` / `point_up` / `facepalm_lite` (fail hook) |
| Pattern `B` big number | `point_up` / `thumbs_up` / `talk_emph` |
| Pattern `C`/`D` explain | `lean_in` / `talk_emph` / `talk_loop` |
| Pattern `E` sting | `idle_bob` / `lean_in` |
| Pattern `F` compare | `present` / `point_side` / `think` |
| Pattern `G` list | `think` → `thumbs_up` / `celebrate` |
| Pattern `H` entity | `present` / `point_side` / `talk_emph` |
| Pattern `I` soft / fail | `shrug` / `cross_arms` / `facepalm_lite` |
| Pattern `J` | **no host** |
| Pattern `K` CTA | `wave` / `thumbs_up` / `celebrate` |
| Showcase card | `present` |
| Soft win | `thumbs_up` (prefer over fists) |
| Fallback | `talk_emph` → `idle_bob` |

## Storyboard fields

```json
"visual": {
  "type": "host_still_plus_graphic",
  "host_expression": "hang",
  "host_asset": "greencode/my_animations/host_stills/hang.png",
  "asset_path": "assets/images/…"
}
```

For pattern `J`: `"host_expression": null`.

## Alive playback

1. Single PNG per scene (expression matched to VO beat).
2. GSAP entrance only — **no GIF/WebP host in frame HTML**.
3. Same expression ≤2 scenes in a row; ≥4 distinct when ≥8 scenes.
4. Full contract: [compose-alive.md](compose-alive.md).

## Hand quality gate

Host stills with visible hands must be **anatomically clean** (5 fingers, no motion trails, no ghost limbs).  
If a PNG has bad AI hands, regenerate it — do **not** extract mid-frames from GIFs (those bake smear). Prefer frame-0 stills or hand-authored clean PNGs.  
See [HOST_STILLS_QA.md](../../../../greencode/my_animations/HOST_STILLS_QA.md).

Prefer new hand-clean stills (`wave`, `cross_arms`, `thumbs_up`, `lean_in`, `present`, `facepalm_lite`) when the beat fits. Fall back to `talk_loop` / `shrug` / `idle_bob` if a hand pose looks off.

## Adding poses

1. Drop green-screen sources into `greencode/my_animations/new/`
2. Map filenames in `scripts/ingest_new_stills.py` → run it
3. Confirm `catalog.json` entry + `resolve_host_expression.py --validate`
4. Use the new `id` in storyboard. Never use `shock`.

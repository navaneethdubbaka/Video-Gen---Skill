# Character catalog — greencode-video-gen

**Primary host assets = keyed talking mouth GIFs @ 12fps** (from `host_talking_loop_gif` via `key_talking_loop_gifs.py`).

```text
greencode/my_animations/
  catalog.json                          # mode: talking_primary (v6)
  host_talking_loop_gif/*_talking_loop.gif   # user green-screen talking GIFs
  host_talking/<id>/talking_loop.gif    # USE THESE in compose (prefer; alpha; 12fps)
  host_talking/<id>/talking_loop.webp   # fallback
  host_stills/<id>.png                  # still fallback if no keyed loop
```

Re-key after dropping new GIFs (encodes at **12fps** so mouths play calm 1x):

```bash
python .cursor/skills/host-mouth-talk/scripts/key_talking_loop_gifs.py
```

`presenting_talking_loop.gif` → catalog id `present`. `shock` stays banned.

## Resolve

```bash
python <SKILL_DIR>/scripts/resolve_host_expression.py --expression talk_emph
python <SKILL_DIR>/scripts/resolve_host_expression.py --list
python <SKILL_DIR>/scripts/resolve_host_expression.py --validate
```

Prefers `talking_loop.gif` when catalog `playback.prefer` ends in `.gif`.

## Playback (non-negotiable)

| Rule | Value |
| --- | --- |
| Native fps | 12 |
| Playback rate | **1.0** — never speed to fit scene |
| Time-stretch | **Forbidden** |
| Stage | Light `#EDEDED` — host alpha, **no black plate** |
| GSAP | Entrance only; no infinite yoyo |

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
  "type": "host_gif_plus_graphic",
  "host_expression": "hang",
  "host_asset": "greencode/my_animations/host_talking/hang/talking_loop.gif",
  "asset_path": "assets/images/…",
  "search_query": "exact nouns from this scene VO",
  "narration_link": "paraphrase of the VO line this image illustrates"
}
```

For pattern `J`: `"host_expression": null`.

**`asset_path` / `search_query`:** must match the VO for that scene — see [compose-alive.md](compose-alive.md) + [asset-research.md](../../references/asset-research.md).

## Alive playback

1. Prefer keyed `talking_loop.gif` per scene (expression matched to VO beat).
2. GSAP entrance only — **playback rate 1.0**; never compress mouth timing into a short scene.
3. Same expression ≤2 scenes in a row; ≥4 distinct when ≥8 scenes.
4. Full contract: [compose-alive.md](compose-alive.md).

## Hand quality gate

Host stills with visible hands must be **anatomically clean** (5 fingers, no motion trails, no ghost limbs).  
If a PNG has bad AI hands, regenerate it — do **not** extract mid-frames from GIFs (those bake smear). Prefer frame-0 stills or hand-authored clean PNGs.  
See [HOST_STILLS_QA.md](../../../../greencode/my_animations/HOST_STILLS_QA.md).

Prefer new hand-clean stills (`wave`, `cross_arms`, `thumbs_up`, `lean_in`, `present`, `facepalm_lite`) when the beat fits. Fall back to `talk_loop` / `shrug` / `idle_bob` if a hand pose looks off.

## Adding poses

1. Drop green-screen talking GIFs into `host_talking_loop_gif/` **or** stills into `greencode/my_animations/new/`
2. For talking: run `key_talking_loop_gifs.py`. For stills: map in `scripts/ingest_new_stills.py` → run it
3. Confirm `catalog.json` entry + `resolve_host_expression.py --validate`
4. Use the new `id` in storyboard. Never use `shock`.

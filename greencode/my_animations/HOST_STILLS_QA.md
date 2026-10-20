# Host stills QA

Stills are **transparent PNGs** used in compose (`stills_primary`).  
`shock` is banned and unused.

## Core set

| Still | Hands? | Quality | Notes |
| --- | --- | --- | --- |
| `talk_loop.png` | No (bust) | OK | Keep |
| `shrug.png` | No | OK | Keep |
| `idle_bob.png` | Hidden | OK | Keep |
| `think.png` | Yes (chin) | Weak anatomy | Prefer regen if reusing heavily |
| `talk_emph.png` | Yes | Mixed | Prefer `lean_in` when possible |
| `point_up.png` | Yes | Mixed | Prefer `present` / `thumbs_up` when possible |
| `point_side.png` | Yes | Mixed | Prefer `present` when showcasing |
| `celebrate.png` | Yes (fists) | Mixed | Prefer `thumbs_up` / `wave` for soft wins |
| `hang.png` | Yes | OK to use | Hook pose |
| `shock.png` | — | **Banned** | Do not use |

## New set (from `my_animations/new/`, keyed 2026-10-15)

| Still | Pose | Use when |
| --- | --- | --- |
| `wave.png` | Open-palm hello | CTA / outro / greeting |
| `cross_arms.png` | Arms crossed | Skepticism / problem beat |
| `thumbs_up.png` | Thumbs up | Soft win / approve |
| `lean_in.png` | Curious mid-sentence gesture | Insight / “listen to this” |
| `present.png` | Both palms up toward side | Showcase card / product |
| `facepalm_lite.png` | Hand to forehead, wry smile | Soft fail / oops |

Ingest script: `greencode/my_animations/scripts/ingest_new_stills.py`  
(chroma-keys studio green → transparent PNG + audit previews in `host_stills_audit/`).

## Compose rule

Prefer the new set for CTA / fail / showcase / soft-win beats. Never use `shock`.

## Adding more

1. Drop green-screen JPG/PNG into `my_animations/new/`
2. Extend `SRC_MAP` in `scripts/ingest_new_stills.py`
3. Run the script → PNGs land in `host_stills/`
4. Add entry to `catalog.json`

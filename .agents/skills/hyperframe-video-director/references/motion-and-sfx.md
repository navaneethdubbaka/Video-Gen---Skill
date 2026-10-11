# Motion + transitions + SFX (required)

Static HTML slides are a **failed** director run. Every video must feel live:

1. **In-frame motion** (GSAP seekable timelines inside each frame)
2. **Inter-frame transitions** (faceless `transitions.mjs`, not only hard cuts)
3. **Transition / hit SFX** on nearly every scene change
4. Optional light **BGM** under VO (ducked)

## Hard gates before render

| Gate | Fail if |
| --- | --- |
| In-frame motion | Any frame HTML has no GSAP / no `window.__timelines` animation for hero + captions |
| Transitions | After assemble, `transitions.mjs inject` not run, OR every `transition_in` is `cut` with zero injected overlaps |
| SFX | `audio_meta.json` `sfx` array empty, OR STORYBOARD frames lack `sfx:` cues |
| Preview feel | Snapshots look like frozen posters with no entrance motion |

Do **not** ship a draft that only swaps full-screen images under VO.

## Allowed inter-frame transitions (faceless registry)

Use these `transition_in` values in `STORYBOARD.md` (incoming frame):

| Name | Energy | When |
| --- | --- | --- |
| `cut` | high | Punchy list beats — **still requires SFX** (whoosh/pop) |
| `crossfade` | calm | Soft topic shifts |
| `blur-crossfade` | calm | Background color/asset changes a lot |
| `push-slide LEFT` / `RIGHT` / `UP` / `DOWN` | medium | New chapter / product reveal |
| `zoom-through` | high | Big number / hook / “wow” beat |
| `squeeze` | medium | Occasional variety |

**Rule:** At least **~40%** of scene boundaries after frame 1 must be a **non-`cut`** registry transition. Never 100% cuts unless the user explicitly asks for jump-cut only — and even then SFX remains required.

## SFX vocabulary (storyboard)

Per frame in `STORYBOARD.md`:

```markdown
- sfx: whoosh
```

or comma list:

```markdown
- sfx: whoosh, click
```

| Cue | Use |
| --- | --- |
| `whoosh` | Default cut / slide / zoom boundary |
| `pop` / `click` | Sticker pop-in, icon reveal, UI badge |
| `hit` / `impact` | Big number punch |
| `rise` / `swell` | Soft reveal / crossfade |
| `none` | Silence — rare; never default |

**Rule:** Frame 1 gets an entrance SFX (`pop` or `whoosh`). Every later frame gets at least one SFX unless intentionally silent for drama (max 1 silent frame per ~30s).

Resolve with faceless (cwd = `composition/hyperframes`):

```bash
node <FACELESS>/scripts/audio.mjs fetch-sfx --storyboard ./STORYBOARD.md --hyperframes . --audio-meta ./audio_meta.json
```

This merges SFX into existing `audio_meta.json` **without** regenerating VO.

**SFX volume must be 80%.** Faceless defaults SFX to `0.35` — always normalize after fetch:

```bash
python <SKILL_DIR>/scripts/set_sfx_volume.py --project <PROJECT> --volume 0.8
```

Then re-run `assemble-index.mjs` so SFX tracks mount at that volume (`data-volume="0.8"`).

## In-frame motion (mandatory)

Each `compositions/frames/NN-*.html` must:

- Register a seekable GSAP timeline on `window.__timelines["<comp-id>"]`
- Animate hero asset: e.g. `from { scale: 0.92, opacity: 0, y: 24 }` over 0.35–0.55s with `power3.out` or springy ease
- Animate caption lines with stagger (0.06–0.12s)
- Optional idle: very slow float/zoom (`yoyo` / long duration) so holds never feel frozen
- Follow `/hyperframes-animation` + faceless `frame-worker.md` — no `Math.random`, no wall-clock

Pattern recipes by style pack live in that pack’s `scene-patterns.md`.

## Suggested boundary rhythm

```text
Frame 1  → pop + scale punch (cut)
Frame 2  → whoosh + zoom-through
Frame 3  → whoosh + cut + list stagger
Frame 4  → whoosh + push-slide LEFT
Frame 5  → click + cut
Frame 6  → rise + crossfade
…repeat variety…
```

## Assemble order (do not skip)

1. Build / update frame HTML with GSAP  
2. `captions.mjs build`  
3. `build_audio_meta_from_vo.py` (VO clips)  
4. `audio.mjs fetch-sfx` (merge SFX)  
5. `assemble-index.mjs`  
6. `transitions.mjs inject`  
7. `transitions.mjs verify`  
8. lint / check / snapshot / render  

If step 6 reports `0 transitions (all cuts)`, go back and diversify `transition_in` values, then inject again.

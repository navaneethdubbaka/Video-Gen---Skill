# Semantic storyboarding

Voice-over timestamps own the timeline. Build `storyboard/storyboard.json` from `analysis/transcript.json` + `analysis/style-spec.json` + user instructions.

## Per segment / scene

For each meaningful narration window ask:

1. What is being said?
2. What concept is communicated?
3. **Which style-pack `pattern` letter?** (`A`–`K` for insider-force-short). Required. Rotate — see [visual-quality.md](visual-quality.md).
4. What **real visual** communicates it best? (photo / UI screenshot / sticker cutout / icon PNG — not invented SVG, not generic AI-brain stock)
5. Does the reference style suggest a treatment (sticker, floating card, mockup, kinetic type)?
6. Asset type — prefer: `photograph` | `screenshot` | `icon` | `video_clip` | `multiple`  
   Use `text_only` for pattern `J` breaths (and ≤20% otherwise).  
   Do **not** use `generated_graphic` as a way to skip downloading an image.
7. If a **public figure / famous company / brand / product** is named, set `visual.entity` (e.g. `"Swiggy"`, `"Jensen Huang"`) and include them in `analysis/entities.json` — Step 7a fetches their image automatically ([entity-images.md](entity-images.md)).
8. Write a precise `search_query` tied to the narration nouns.
9. After Step 7 research, set `asset_path` to the cached file.
10. What on-screen text? **2–6 words** for kinetic lines; **≤2 lines** on cards. **Never** duplicate the card title as a mid-frame headline ([visual-quality.md](visual-quality.md)).
11. Which words to emphasize? (dual-tone black/gray + karaoke `.is-active`)
12. What **in-frame motion**? (pop_in, float, punch_in, stagger_list — never “none/static”)
13. What **inter-frame transition**? Mix registry transitions with cuts.
14. What **sfx** on entry? (`whoosh`, `pop`, `hit`, `rise`) — later normalized to volume **0.8**
15. When must the visual change? (align to segment boundaries)

### Pattern diversity (gate)

Before leaving Step 6, verify:

- Every scene has `"pattern": "A"` … `"K"`
- ≥4 distinct letters when there are ≥6 scenes
- No letter repeats 3× consecutively
- Card patterns `C`/`D`/`G`/`I` ≤ 50% of scenes
- ≥1 `J` breath when total duration ≥ 45s

### Retention / growth (gate)

- Scene 1: `pattern` **A or B**, `role: "hook"`, `text.content` ≤6 words, duration ≤3.5s
- Average scene duration ≤4s; no scene >6s (pattern `J` may hold to 7s)
- Last 8s: a scene with `role: "cta"` and pattern **J or K** (follow / Part 2 / open loop)
- Top-level `packaging` (or `analysis/packaging.json`): `title` + `first_frame_note`

See [visual-quality.md](visual-quality.md) §9.

## Visual field (required shape)

```json
"visual": {
  "type": "photograph",
  "search_query": "smartphone food delivery app home screen",
  "asset_path": "assets/images/<cached-file>.jpg",
  "requirement": {
    "subject": "…",
    "composition": { "subject_position": "center", "negative_space": "lower_third" },
    "purpose": "hero bed",
    "minimum_resolution": "1080p",
    "narration_link": "Swiggy Burstrex feature launch"
  }
}
```

`asset_path` may be empty **only** while drafting the storyboard; Step 7 must fill it before compose. Prefer writing the path as soon as the asset is cached.

## Timing

- Use transcript `segments[].start/end` as scene windows.
- Merge tiny fragments (<0.6s) into neighbors when they are not meaningful beats.
- Split long segments (>4–5s) only when meaning clearly shifts mid-segment.
- `total_duration_s` = last scene end (≈ VO duration).

## Style binding

Default every scene to `style-spec` typography/motion/transition language.  
Deliberate exceptions need a one-line reason in the scene `concept` or `motion.notes`.

Style chrome (white sticker border, floating card) wraps a **real image** — chrome alone is not the visual.

## Output

Follow [schemas/storyboard.schema.json](../schemas/storyboard.schema.json) and [templates/storyboard.example.json](../templates/storyboard.example.json).

Do not write HyperFrames HTML at this stage.

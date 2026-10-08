# Semantic storyboarding

Voice-over timestamps own the timeline. Build `storyboard/storyboard.json` from `analysis/transcript.json` + `analysis/style-spec.json` + user instructions.

## Per segment / scene

For each meaningful narration window ask:

1. What is being said?
2. What concept is communicated?
3. What **real visual** communicates it best? (photo / UI screenshot / icon PNG — not invented SVG)
4. Does the reference style suggest a treatment (sticker, floating card, mockup)?
5. Asset type — prefer: `photograph` | `screenshot` | `icon` | `video_clip` | `multiple`  
   Use `text_only` rarely (≤20% of scenes).  
   Do **not** use `generated_graphic` as a way to skip downloading an image.
6. Write a precise `search_query` tied to the narration nouns.
7. After Step 7 research, set `asset_path` to the cached file.
8. What on-screen text (same language as VO unless user asked to translate)?
9. Which words to emphasize?
10. What **in-frame motion**? (pop_in, float, punch_in, stagger_list — never “none/static”)
11. What **inter-frame transition**? Mix registry transitions with cuts.
12. What **sfx** on entry? (`whoosh`, `pop`, `hit`, `rise`)
13. When must the visual change? (align to segment boundaries)

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

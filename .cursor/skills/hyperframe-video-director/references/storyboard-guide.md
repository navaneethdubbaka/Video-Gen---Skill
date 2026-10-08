# Semantic storyboarding

Voice-over timestamps own the timeline. Build `storyboard/storyboard.json` from `analysis/transcript.json` + `analysis/style-spec.json` + user instructions.

## Per segment / scene

For each meaningful narration window ask:

1. What is being said?
2. What concept is communicated?
3. What visual communicates it best?
4. Does the reference style suggest a treatment?
5. Asset type: photograph / video clip / screenshot / diagram / icon / text-only / generated graphic / multiple?
6. What on-screen text (same language as VO unless user asked to translate)?
7. Which words to emphasize?
8. What **in-frame motion**? (pop_in, float, punch_in, stagger_list — never “none/static”)
9. What **inter-frame transition**? Prefer registry names: `zoom-through`, `push-slide LEFT`, `crossfade`, `blur-crossfade`, `squeeze`, or `hard_cut` — not all cuts.
10. What **sfx** on entry? (`whoosh`, `pop`, `hit`, `rise`) — required almost every scene.
11. When must the visual change? (align to segment boundaries)

## Timing

- Use transcript `segments[].start/end` as scene windows.
- Merge tiny fragments (<0.6s) into neighbors when they are not meaningful beats.
- Split long segments (>4–5s) only when meaning clearly shifts mid-segment.
- `total_duration_s` = last scene end (≈ VO duration).

## Style binding

Default every scene to `style-spec` typography/motion/transition language.  
Deliberate exceptions need a one-line reason in the scene `concept` or `motion.notes`.

## Output

Follow [schemas/storyboard.schema.json](../schemas/storyboard.schema.json) and [templates/storyboard.example.json](../templates/storyboard.example.json).

Do not write HyperFrames HTML at this stage.

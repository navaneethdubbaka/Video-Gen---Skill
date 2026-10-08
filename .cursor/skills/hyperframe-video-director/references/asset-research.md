# Asset research

Asset selection is a **design decision**, not a download race.

## When an asset is needed

Skip external media for `text_only` / pure kinetic type scenes unless the style requires a bed.

## Requirement object

```json
{
  "subject": "person using smartphone",
  "composition": {
    "subject_position": "right",
    "negative_space": "left"
  },
  "purpose": "background for headline",
  "minimum_resolution": "1080p"
}
```

If captions sit lower-center, prefer subjects that leave that zone clear (or plan a scrim).

## Acquisition order

1. Check `assets/metadata/` for a reusable prior download (same query hash).
2. `/media-use` resolve:
   ```bash
   node <MEDIA_USE>/scripts/resolve.mjs --type image --intent "<precise query>" --project <HF_DIR>
   ```
   Then copy/adopt into project `assets/` via `cache_asset.py` when useful for the director tree.
3. If catalog fails: web search → download 2–4 candidates → vision inspect → pick one.
4. Crop/resize only if needed for aspect/negative space; keep originals in cache when practical.

## Inspection (mandatory)

Reject candidates that:

- Put the subject dead-center when type needs the center
- Are too low-res / heavily compressed
- Are watermarked / logo-heavy / clearly proprietary brand frames
- Stretch awkwardly to the target aspect

Accept when relevance, composition, resolution, and text-safe space all pass.

## Cache

```bash
python <SKILL_DIR>/scripts/cache_asset.py \
  --project <PROJECT> \
  --file <candidate> \
  --query "…" \
  --kind images \
  --usage scene_01 \
  --source "<url-or-provider>"
```

Kinds: `images`, `videos`, `icons`, `screenshots`.

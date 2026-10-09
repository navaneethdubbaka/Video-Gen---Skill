# Entity images (public figures & famous companies)

When narration mentions a **public figure**, **famous company/brand**, **well-known product**, or similar recognizable entity, the director **must** fetch a real image of that entity and use it in the matching scenes.

Do not invent SVG logos or cartoon stand-ins when a public entity is named.

## Scope

| Fetch | Skip |
| --- | --- |
| Public figures (CEOs, celebrities, politicians in news) | Private / non-public individuals |
| Well-known companies & brands (Swiggy, NVIDIA, Apple, …) | Tiny unknown local businesses with no public presence |
| Famous products / apps with Wikipedia presence | Generic nouns (“a laptop”, “a phone”) — use normal stock search |

Safety: prefer Wikimedia/Wikipedia images; vision-inspect before use; do not scrape the reference Short’s frames; respect that logos may be trademarked — use for editorial explainer context, not as fake endorsement.

## Pipeline

### 1) Detect entities (agent)

After transcript + storyboard draft, write `analysis/entities.json`:

```json
{
  "entities": [
    {
      "name": "Swiggy",
      "type": "company",
      "scene_ids": [1, 2, 4],
      "reason": "Named repeatedly in VO; product story subject"
    },
    {
      "name": "Jensen Huang",
      "type": "person",
      "scene_ids": [1],
      "reason": "Public figure named in hook"
    }
  ]
}
```

Types: `person` | `company` | `organization` | `brand` | `product` | `other`

Also tag scenes in storyboard:

```json
"visual": {
  "entity": "Swiggy",
  "type": "photograph",
  "search_query": "Swiggy company"
}
```

### 2) Fetch (deterministic script)

```bash
python <SKILL_DIR>/scripts/fetch_entity_image.py --project <PROJECT> --entities analysis/entities.json
```

Or one-off:

```bash
python <SKILL_DIR>/scripts/fetch_entity_image.py --project <PROJECT> --name "Swiggy" --type company --scenes 1,2,4
```

- Source: Wikipedia page image, then **Wikimedia Commons** search (logos/portraits)
- Cache: `assets/images/entities/entity_<slug>_<type>.*`
- Ledger: `analysis/entity-assets.json` + `assets/metadata/entity_*.json`
- If both miss: agent web-searches `"<Name> official"` / portrait and `cache_asset.py`

### 3) Apply into storyboard

```bash
python <SKILL_DIR>/scripts/apply_entity_assets.py --project <PROJECT>
```

Sets `visual.asset_path` for scenes listed in `scene_ids` or tagged with `visual.entity`.

### 4) Vision QA

Open each fetched file. Confirm it depicts the right entity. If wrong (disambiguation), edit `entities.json` with a better Wikipedia title (e.g. `"Apple Inc."`) and re-fetch.

### 5) Compose

Use the cached path in frame HTML (`<img src="…">`) with sticker/card chrome per style pack. Animate with GSAP.

## Failure handling

If Wikipedia has no image:

1. Retry with a clearer name (`Apple Inc.`, `Meta Platforms`).
2. Fall back to `/media-use` resolve or web search with query `"<Name> official"` / `"<Name> portrait"`.
3. Still cache via `cache_asset.py` and set `asset_path`.
4. Never silently substitute a random unrelated stock photo.

## Relation to Step 7

Entity fetch runs **inside** Step 7 (assets), before `qa_report.py --phase assets`.  
Non-entity scenes still need normal asset research.

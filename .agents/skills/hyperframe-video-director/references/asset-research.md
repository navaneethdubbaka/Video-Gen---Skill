# Asset research (MANDATORY)

Relevant **real images** are not optional decoration. They are a hard deliverable.

Invented SVG/CSS-only frames (fake logos, empty cards, generic icons drawn in HTML) are a **failed** director run when the narration names a concrete subject, product, place, UI, or concept that can be pictured.

## Public figures & famous companies

If the narration names a recognizable person, company, brand, or product, **fetch that entity’s image first** (do not draw a fake logo).

See [entity-images.md](entity-images.md):

```bash
# after writing analysis/entities.json
python <SKILL_DIR>/scripts/fetch_entity_image.py --project <PROJECT> --entities analysis/entities.json
python <SKILL_DIR>/scripts/apply_entity_assets.py --project <PROJECT>
```

Then continue with normal research for any remaining scenes.

## Hard gates

Before building any HyperFrames HTML:

1. Every scene (except rare kinetic `text_only` beats — see below) has:
   - `visual.search_query` — precise, narration-specific
   - `visual.asset_path` — project-relative file under `assets/images|screenshots|icons|videos/`
2. The file exists on disk and is registered in `assets/metadata/`.
3. You **vision-inspected** the chosen file and confirmed it matches the narration concept.
4. Cap: **≤20%** of scenes may be `text_only` (pure kinetic type). All others need a real media file.
5. `generated_graphic` is **not** a substitute for an image. If you build a UI card / sticker chrome in HTML, it must still include a real `<img>` / screenshot / photo (product UI, photo of subject, downloaded icon PNG, etc.).

Do **not** proceed to Step 8 compose until `qa_report.py` reports no `missing_image` / `too_many_text_only` errors.

## What “relevant” means

The image must depict what the **narration is talking about**, not a vague mood.

| Narration about… | Good query / asset | Bad |
| --- | --- | --- |
| Swiggy Burstrex launch | Swiggy app UI / food-delivery phone mock photo | Random orange SVG “logo” |
| Security / token in URL | Browser address bar screenshot, lock icon PNG, code/token UI | Generic red triangle drawn in CSS |
| Laptop / local AI | Real laptop photo or 3D stock matching style | Empty gray rectangle |
| Base64 / decode | Terminal or code editor screenshot with encoded text | Decorative “</>” shape only |
| GitHub stars | GitHub repo UI screenshot or star icon + real-looking card with photo bed | Numbers alone on blank card |

If the subject is a brand, prefer **official-looking UI/product photography** or generic stock that reads as that category — never paste copyrighted logo marks when avoidable; never clone the reference Short’s frames.

## Requirement object (required per image scene)

```json
{
  "subject": "smartphone showing food delivery app home screen",
  "composition": {
    "subject_position": "center",
    "negative_space": "lower_third"
  },
  "purpose": "hero bed under dual-tone caption",
  "minimum_resolution": "1080p",
  "narration_link": "Swiggy Burstrex feature launch"
}
```

`narration_link` must quote or paraphrase the scene narration so relevance can be audited.

## Acquisition order

1. Reuse `assets/metadata/` cache if query + narration_link still match.
2. `/media-use` resolve:
   ```bash
   node <MEDIA_USE>/scripts/resolve.mjs --type image --intent "<precise query>" --project <HF_DIR>
   ```
3. If miss: web search → download **2–4** candidates → vision inspect → pick one.
4. Cache:
   ```bash
   python <SKILL_DIR>/scripts/cache_asset.py \
     --project <PROJECT> \
     --file <candidate> \
     --query "…" \
     --kind images \
     --usage scene_01 \
     --source "<url-or-provider>"
   ```
5. Write `visual.asset_path` (and optionally `visual.type`: `photograph` | `screenshot` | `icon`) back into `storyboard.json`.

Kinds: `images`, `videos`, `icons`, `screenshots`.

## Inspection (mandatory)

Reject if:

- Not about the narration subject
- Subject fills the caption zone with no room for type (unless you plan a scrim)
- Low-res / heavy compression / watermarks
- Stretched or wrong aspect with no crop plan
- Decorative abstract filler used to dodge research

Accept only when relevance + composition + resolution pass. Keep a one-line note in metadata `usage` / storyboard `concept` if helpful.

## Wiring into frames

In each frame HTML, the hero must reference the frozen file:

```html
<img class="hero" src="../../assets/images/<file>.jpg" alt="…" />
```

(or project-relative path the assembler resolves — copy into `composition/hyperframes/public/` or `assets/` and use that path).

GSAP animates that `<img>` / card that **contains** the image. Empty chrome without the image = fail.

## text_only exception

Allowed only for short kinetic emphasis lines (pattern J), max 20% of scenes, and never for the opening hook when a product/person/place is named.

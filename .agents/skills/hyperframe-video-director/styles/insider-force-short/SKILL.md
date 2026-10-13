---
name: insider-force-short
description: >
  Frozen visual style pack for 9:16 clean-tech explainer Shorts: light studio
  background, floating UI cards, sticker cutouts, kinetic dual-tone captions,
  product mockups. Use when the user asks for insider-force-short, Insider Force
  style, clean-tech sticker short, Colibri-video style, or "style like the
  Calibri/Colibri laptop AI short". Always omit channel watermarks.
---

# Style pack: insider-force-short

Frozen **visual grammar** extracted from a 9:16 tech-explainer Short (~103s, 720×1280).  
Use with `/hyperframe-video-director`. This pack **replaces Step 4 style analysis** — copy `style-spec.json` into the project instead of re-deriving from a new reference (unless the user supplies a different reference).

## Hard overrides (non-negotiable)

1. **No watermark.** Never render `insiderforce.io`, channel URLs, handle bars, or corner brand chips from the reference. Bottom-center URL space stays empty (or user brand only if they ask).
2. **Grammar only.** Do not copy reference frames, celebrity cutouts, product screenshots, or logos verbatim. Rebuild equivalent compositions with original / licensed assets.
3. **Voice-over owns timing.** Captions and cuts follow the user’s VO transcript, not the reference’s edit.
4. **Live motion + SFX.** Even though the reference often *looks* like hard cuts, every scene needs GSAP pop/float entrances and boundary SFX (`whoosh`/`pop`/`hit`). Mix in `zoom-through` / `push-slide` / `crossfade` on ~half of boundaries so the piece is not a silent slideshow. Follow parent [../../references/motion-and-sfx.md](../../references/motion-and-sfx.md).
5. **Real images inside the chrome.** Sticker / floating-card / laptop patterns must wrap a **downloaded, narration-relevant** photo or UI screenshot — not hand-drawn SVG logos or empty cards. Follow [../../references/asset-research.md](../../references/asset-research.md).
6. **Captions:** Telugu VO → Latin/English spellings (romanize, do not translate). Slim karaoke via [caption-skin.html](caption-skin.html) + `prepare_captions.py` — dual-tone in-frame type is primary on kinetic beats.
7. **Anti-slideshow visual quality:** every scene sets `pattern` A–K; ≥4 distinct patterns; no 3-in-a-row repeats; card patterns C/D/G/I ≤50%; ≥1 `J` breath; no double titles; ≤2 lines card body; one accent color; sticker/UI/paper assets not generic AI stock. See [scene-patterns.md](scene-patterns.md) + [../../references/visual-quality.md](../../references/visual-quality.md).
8. **Retention / growth:** scene 1 = A/B hook ≤3.5s ≤6 words; avg scene ≤4s; CTA (`role: cta`, J/K) in last 8s; packaging title + first-frame note.

## When to load

Triggers (any):

- `insider-force-short`
- “Insider Force style”
- “style like the Colibri / Calibri laptop AI video”
- “clean tech sticker short”
- User points at the local reference MP4 used to author this pack

## Agent steps when this pack is selected

1. Read this file + [style-spec.json](style-spec.json) + [scene-patterns.md](scene-patterns.md).
2. Open **refs** for visual ground truth (see [REF_INDEX.md](REF_INDEX.md)). Inspect with vision before composing.
3. Copy style into the project:

```bash
cp <SKILL_DIR>/styles/insider-force-short/style-spec.json <PROJECT>/analysis/style-spec.json
```

Also write `<PROJECT>/analysis/reference-analysis.json`:

```json
{ "style_pack": "insider-force-short", "watermark": "forbidden", "notes": "Using frozen pack; no channel URL." }
```

4. Continue director workflow from transcript → storyboard → assets → HyperFrames handoff.
5. Map each storyboard scene to a **scene pattern** from [scene-patterns.md](scene-patterns.md).
6. QA: confirm **zero** watermarks / URL footers in snapshots.

## Look (summary)

| Layer | Spec |
| --- | --- |
| Canvas | 9:16, prefer 1080×1920 (source was 720×1280) |
| Background | Flat off-white / light gray studio (`#EDEDED`–`#F4F4F4`); occasional subtle dot-grid panel |
| Depth | Soft diffused drop shadows under floating cards / mockups / stickers |
| Type | Clean geometric sans; **dual-tone lines** — bold black keywords + medium-gray secondary words; often lowercase |
| Caption zone | Lower-middle or mid; large centered lines; keyword weight punch |
| Accent | Sparse — one brand/signal color max (e.g. electric green / teal); mostly mono |
| Cuts | Narration-driven hard cuts; ~1.5–3s shots; dense idea packing |
| Motifs | Sticker cutouts + white outline; floating UI cards; laptop/phone 3D mockups; icon list with ✕/✓ circles; GitHub-stat cards; kinetic type-only beats |

## Forbidden

- Bottom `insiderforce.io` (or any cloned channel watermark)
- Recreating Jensen / celebrity stickers from the reference pixels
- Cloning Colibri/GLM UI screenshots from the reference — rebuild original UI cards
- Busy gradients, neon glow stacks, purple SaaS clichés
- Lower-third bars that look like the watermark strip

## Refs to inspect

| File | Pattern |
| --- | --- |
| [refs/ref_01.jpg](refs/ref_01.jpg) | Hook sticker + dual-tone headline |
| [refs/ref_02.jpg](refs/ref_02.jpg) | 3D hand + device + big number caption |
| [refs/ref_03.jpg](refs/ref_03.jpg) | Floating product website card |
| [refs/ref_04.jpg](refs/ref_04.jpg) | Doc card + orbiting logos + gray caption |
| [refs/ref_05.jpg](refs/ref_05.jpg) | Center brand/pixel mark moment |
| [refs/ref_06.jpg](refs/ref_06.jpg) | Floating laptop mockup + top caption |
| [refs/ref_07.jpg](refs/ref_07.jpg) | Warm product info card (serif body + sans chrome) |
| [refs/ref_08.jpg](refs/ref_08.jpg) | X/check icon list kinetic type |
| [refs/ref_09.jpg](refs/ref_09.jpg) | Laptop + overlay badges + “for Free” punch |
| [refs/ref_10.jpg](refs/ref_10.jpg) | GitHub stats floating card |
| [refs/ref_11.jpg](refs/ref_11.jpg) | Pure kinetic type (keyword bold) |
| [refs/ref_12.jpg](refs/ref_12.jpg) | Dot-grid panel + symbol + dual-tone line |

Full 0.5fps dump (optional deep dive): [frames/](frames/)

## Example invoke

```text
Use hyperframe-video-director with style pack insider-force-short.

Voiceover: ./voiceover.wav
Optional: no watermark; same clean tech sticker look as the Colibri short.
```

Or:

```text
Style like insider-force-short. Here's my VO: ./my.wav
```

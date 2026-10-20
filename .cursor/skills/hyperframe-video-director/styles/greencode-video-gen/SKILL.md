---
name: greencode-video-gen
description: >
  Frozen visual style pack for 9:16 light-studio character-hosted explainer Shorts:
  off-white stage (#EDEDED), terminal-green kinetic type, code/diagram cards, and
  the user’s keyed talking host GIFs from greencode/my_animations/host_talking.
  Use when the user asks for greencode-video-gen, Green Code style, greencode
  video gen, anime-host explainer, or points at the local greencode reference.
  Always omit channel watermarks, DNA marks, and any on-screen
  “GREENCODE / PATTERN / greencode video gen” chrome; use only the user’s
  host catalog with alive (non-screensaver) host playback at native 1x speed;
  every content photo must match that scene’s VO/script.
---

# Style pack: greencode-video-gen

Frozen **visual grammar** for **9:16 Shorts** with a **light studio stage** (not a black void).  
Use with `/hyperframe-video-director`. This pack **replaces Step 4 style analysis** — copy `style-spec.json` into the project instead of re-deriving from a new reference (unless the user supplies a different reference).

**Read before compose:** [compose-alive.md](compose-alive.md) — anti-screensaver, light stage, native host speed, script-matched assets.

## Hard overrides (non-negotiable)

1. **No watermark / no skill chrome.** Never render DNA marks, channel URLs, **`GREENCODE // …`**, **`PATTERN [X]`**, **`greencode video gen`**, or EP badges every scene.
2. **Grammar only.** Rebuild diagrams, code cards, and UI with original / licensed assets.
3. **Voice-over owns timing.** Captions and cuts follow the user’s VO transcript.
4. **Your host only.** Resolve from [`greencode/my_animations/catalog.json`](../../../../greencode/my_animations/catalog.json) via [character-catalog.md](character-catalog.md) + `resolve_host_expression.py`. Prefer **`talking_loop.gif`** (12fps keyed).
5. **Light stage.** Canvas `#EDEDED`–`#F4F4F4`. **Never** near-black void or black plate behind the host. Host already has alpha — do not chroma again.
6. **Host speed = 1x.** Native 12fps. Never time-stretch / speed the mouth loop to fit a short scene. Soft-loop or freeze after one cycle.
7. **Script-matched photos.** Every content image must depict what THAT scene’s VO says. Search query = narration nouns; vision-check before lock. No generic AI-brain / mood stock. See [asset-research.md](../../references/asset-research.md).
8. **Alive host, not GIF screensaver.** One entrance; **no infinite GSAP yoyo** stacked on looping GIF; expression diversifies with VO.
9. **No concept leak.** Never put storyboard `concept` / agent notes on canvas — only viewer-facing kinetic lines (2–6 words) and designed card body ≤2 lines.
10. **No double titles.** Card H1 ≠ mid-frame headline.
11. **Live graphic motion + SFX** @ volume **0.8**. Pattern letter changes **layout**, not a shared top-bar template.
12. **Captions:** Telugu → Latin romanization. Slim karaoke via [caption-skin.html](caption-skin.html); dual-tone near-black + `#39FF14` / `#1DB954` on kinetic beats.
13. **Anti-slideshow:** patterns A–K; ≥4 distinct; no 3-in-a-row; cards ≤50%; ≥1 `J` when ≥45s. See [scene-patterns.md](scene-patterns.md) + [../../references/visual-quality.md](../../references/visual-quality.md).
14. **Retention:** scene 1 = A/B hook ≤3.5s ≤6 words; avg ≤4s; CTA (`role: cta`, J/K) in last 8s.
15. **Composition:** host lower-left ~32–42% height; graphic stage ≤48% height; headline clear of host head; empty footer; hook at t=0.
16. **Vision QA** before final: fail on black stage, sped-up mouth, image≠VO, greencode badges, concept subtitles, double titles, looping screensaver host. Write `qa/visual-notes.md`.

## When to load

Triggers (any):

- `greencode-video-gen`
- “greencode video gen”
- “Green Code style” / “greencode style”
- “anime host explainer” / “dark anime host explainer” (pack is light-stage now)
- User points at the local greencode reference webm used to author this pack

## Agent steps when this pack is selected

1. Read this file + [style-spec.json](style-spec.json) + [scene-patterns.md](scene-patterns.md) + [character-catalog.md](character-catalog.md) + **[compose-alive.md](compose-alive.md)**.
2. Open **refs** ([REF_INDEX.md](REF_INDEX.md), [visual-notes.md](visual-notes.md)).
3. Copy style into the project:

```bash
cp <SKILL_DIR>/styles/greencode-video-gen/style-spec.json <PROJECT>/analysis/style-spec.json
```

Also write `<PROJECT>/analysis/reference-analysis.json`:

```json
{
  "style_pack": "greencode-video-gen",
  "watermark": "forbidden",
  "on_canvas_forbidden": ["GREENCODE", "PATTERN [", "greencode video gen", "DNA mark"],
  "host_catalog": "greencode/my_animations/catalog.json",
  "stage": "light",
  "host_playback_rate": 1.0,
  "script_match_assets": true,
  "notes": "Frozen pack; light stage; native 1x host GIF; VO-matched photos only; no debug chrome."
}
```

4. Transcript → storyboard → **script-matched** assets (per scene `narration_link`) → HyperFrames handoff.
5. Every scene: `pattern` + `host_expression` (null only for `J`). Enforce expression diversity (≥4 distinct when ≥8 scenes; ≤2 identical in a row).
6. Resolve hosts:

```bash
python <SKILL_DIR>/scripts/resolve_host_expression.py --expression <id>
```

7. Compose frames per [compose-alive.md](compose-alive.md) — light stage, host rate 1.0, different HTML layouts per pattern.
8. QA: light stage; host not sped up; every photo matches that scene’s VO; zero greencode/PATTERN chrome; no concept subtitles.

## Look (summary)

| Layer | Spec |
| --- | --- |
| Canvas | 9:16, 1080×1920 |
| Background | Light studio `#EDEDED`–`#F4F4F4` — **never** black void |
| Host | Keyed `talking_loop.gif` @ **12fps / 1x**; soft shadow; entrance only |
| Content images | Must match scene VO nouns (vision-checked) |
| Type | Near-black + terminal green dual-tone; 2–6 words |
| Caption | Slim light/gray pill; green `.is-active` |
| Accent | `#39FF14` / `#1DB954` only |
| Motifs | Terminal cards, diagrams, checklists, entity stickers, kinetic type |

## Forbidden

- Near-black / black void stage or black host plate
- Speeding host GIF/WebP to fit scene length
- Photos / stock that don’t match the VO line
- On-canvas `GREENCODE // …`, `PATTERN [X]`, skill-name titles
- Cloning reference character / DNA watermark
- Dumping `concept` as subtitle
- Infinite host bob + infinite GIF loop
- Leaving chroma green in the render

## Refs

See [REF_INDEX.md](REF_INDEX.md). Full dump: [frames/](frames/). Layout grammar from refs; **stage color is light** (pack override).

## Example invoke

```text
Use hyperframe-video-director with style pack greencode-video-gen.

Voiceover: ./voiceover.wav
Host GIFs: greencode/my_animations/host_talking/ (keyed talking_loop.gif @ 1x)
Light stage #EDEDED. Every photo must match that scene's VO.
Follow compose-alive.md — no GREENCODE badge, no sped-up mouth, no black background.
Render ONLY on E: via scripts/render-on-e.ps1 (never C: TEMP).
```

## Render (E: only)

```powershell
.\scripts\render-on-e.ps1 `
  -ProjectDir <PROJECT>/composition/hyperframes `
  -OutputName final.mp4
```

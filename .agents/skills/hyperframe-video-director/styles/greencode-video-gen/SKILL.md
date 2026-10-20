---
name: greencode-video-gen
description: >
  Frozen visual style pack for 9:16 dark character-hosted explainer Shorts:
  near-black stage, terminal-green kinetic type, code/diagram cards, and the
  user’s animated host GIFs from greencode/my_animations. Use when the user
  asks for greencode-video-gen, Green Code style, greencode video gen, dark
  anime-host explainer, or points at the local greencode LLM-from-scratch
  reference. Always omit channel watermarks, DNA marks, and any on-screen
  “GREENCODE / PATTERN / greencode video gen” chrome; use only the user’s
  host catalog with alive (non-screensaver) host playback.
---

# Style pack: greencode-video-gen

Frozen **visual grammar** adapted from a 16:9 dark host+graphic explainer to **9:16 Shorts**.  
Use with `/hyperframe-video-director`. This pack **replaces Step 4 style analysis** — copy `style-spec.json` into the project instead of re-deriving from a new reference (unless the user supplies a different reference).

**Read before compose:** [compose-alive.md](compose-alive.md) — non-negotiable anti-screensaver + anti-debug-chrome rules (from real Shorts QA).

## Hard overrides (non-negotiable)

1. **No watermark / no skill chrome.** Never render DNA marks, channel URLs, **`GREENCODE // …`**, **`PATTERN [X]`**, **`greencode video gen`**, or EP badges every scene.
2. **Grammar only.** Rebuild diagrams, code cards, and UI with original / licensed assets.
3. **Voice-over owns timing.** Captions and cuts follow the user’s VO transcript.
4. **Your host only.** Resolve from [`greencode/my_animations/catalog.json`](../../../../greencode/my_animations/catalog.json) via [character-catalog.md](character-catalog.md) + `resolve_host_expression.py`.
5. **Chroma-key green** (`#00FF00`) — no green boxes in the final frame. Prefer `host_keyed/` WebP when present.
6. **Alive host, not GIF screensaver.** One entrance; **no infinite GSAP yoyo** stacked on looping GIF; expression diversifies with VO; see [compose-alive.md](compose-alive.md).
7. **No concept leak.** Never put storyboard `concept` / agent notes on canvas — only viewer-facing kinetic lines (2–6 words) and designed card body ≤2 lines.
8. **No double titles.** Card H1 ≠ mid-frame headline.
9. **Live graphic motion + SFX** @ volume **0.8**. Pattern letter changes **layout**, not a shared top-bar template.
10. **Captions:** Telugu → Latin romanization. Slim karaoke via [caption-skin.html](caption-skin.html); dual-tone white + `#39FF14` primary on kinetic beats.
11. **Anti-slideshow:** patterns A–K; ≥4 distinct; no 3-in-a-row; cards ≤50%; ≥1 `J` when ≥45s. See [scene-patterns.md](scene-patterns.md) + [../../references/visual-quality.md](../../references/visual-quality.md).
12. **Retention:** scene 1 = A/B hook ≤3.5s ≤6 words; avg ≤4s; CTA (`role: cta`, J/K) in last 8s.
13. **Composition:** host lower-left ~32–42% height; graphic stage ≤48% height; headline clear of host head; empty footer; hook at t=0.
14. **Vision QA** before final: fail on greencode badges, concept subtitles, double titles, looping screensaver host, host covering type. Write `qa/visual-notes.md`.

## When to load

Triggers (any):

- `greencode-video-gen`
- “greencode video gen”
- “Green Code style” / “greencode style”
- “dark anime host explainer”
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
  "notes": "Frozen pack; user host only; chroma-key; alive host playback; no debug chrome."
}
```

4. Transcript → storyboard → assets → HyperFrames handoff.
5. Every scene: `pattern` + `host_expression` (null only for `J`). Enforce expression diversity (≥4 distinct when ≥8 scenes; ≤2 identical in a row).
6. Resolve hosts:

```bash
python <SKILL_DIR>/scripts/resolve_host_expression.py --expression <id>
```

7. Compose frames per [compose-alive.md](compose-alive.md) — **different HTML layouts per pattern**, not one template with a badge.
8. QA: zero greencode/PATTERN chrome; no concept subtitles; host not screensaver-looping; no green leftover.

## Look (summary)

| Layer | Spec |
| --- | --- |
| Canvas | 9:16, 1080×1920 |
| Background | Near-black void; optional faint scanline (~4% opacity) |
| Host | Bust from catalog; keyed; soft shadow; **settled** after entrance |
| Type | White + terminal green dual-tone; 2–6 words |
| Caption | Slim dark pill; green `.is-active` |
| Accent | `#39FF14` only |
| Motifs | Terminal cards, diagrams, checklists, entity stickers, kinetic type |

## Forbidden

- On-canvas `GREENCODE // …`, `PATTERN [X]`, skill-name titles
- Cloning reference character / DNA watermark
- Dumping `concept` as subtitle
- Infinite host bob + infinite GIF loop
- Light Insider Force sticker look (use `insider-force-short`)
- Leaving chroma green in the render

## Refs

See [REF_INDEX.md](REF_INDEX.md). Full dump: [frames/](frames/).

## Example invoke

```text
Use hyperframe-video-director with style pack greencode-video-gen.

Voiceover: ./voiceover.wav
Host GIFs: greencode/my_animations/host/
Follow compose-alive.md — no GREENCODE badge, no looping screensaver host.
Render ONLY on E: via scripts/render-on-e.ps1 (never C: TEMP).
```

## Render (E: only)

```powershell
.\scripts\render-on-e.ps1 `
  -ProjectDir "E:\Video Gen Skill\videos\<slug>\composition\hyperframes" `
  -Out "E:\Video Gen Skill\videos\<slug>\renders\draft\out.mp4" `
  -Workers 1
```

Do not run bare `npx hyperframes render` when `C:` is low on space — scratch goes to `%TEMP%` on C:.

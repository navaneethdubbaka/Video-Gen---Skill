# Hook visual quality (good vs fail)

Hooks are **scroll-stoppers**, not mini-explainers. If a frame looks like a body-scene slide, it fails.

Read this before writing `hooks.json` and again at Step 7 QA.

## Thumb test (mandatory)

Mute the VO. Look at `qa/hN.jpg` (≈0.4s) for **0.5 seconds**.

| Pass | Fail |
| --- | --- |
| One idea lands instantly | Need to read bullets / titles to get the point |
| Giant type **or** one sticker dominates | Dual-column cards, charts, report layouts |
| ≤6 on-screen words total (hero + badge) | Paragraphs inside the asset |
| Curiosity held if VO asks “why?” | Visual already answers the why |

If thumb test fails → rebuild visual (do not ship).

---

## Pattern purity

### Pattern A — sticker
- **One** cutout / product / face / UI crop with white outline
- Dual-tone line ≤6 words above or beside it
- Optional tiny badge (one label, not a second headline)
- No comparison tables inside the sticker

### Pattern B — big number
- **One** giant number owns the frame (e.g. `1.3B`)
- Short gray unit under it (e.g. `beat 175B` or `params`)
- Optional: tiny device plate or simple vs chip — **not** a full infographic
- Number should be readable from arm’s length on a phone

**Ban for Pattern B:** side-by-side “winner / loser” cards, bullet lists, section titles like “Parameter Efficiency”, multi-stat dashboards.

---

## Anti-patterns (learned from bad runs)

### 1. Body-scene density
**Bad:** Headline + comparison card with titles, two columns, 6 bullets, WINNER/OUTPERFORMED footers.  
**Good:** `1.3B` huge + gray `vs 175B` + maybe one sticker (trophy / reject stamp).  
Hooks tease; body explains.

### 2. Same message ×3
**Bad:** “1.3B BEAT” + badge “WINNER • 1.3B” + card footer “WINNER”.  
**Good:** One claim, one accent. Badge only if it adds new info.

### 3. Mystery without a knowledge contract (edtech fail)
Bare `why?` or a floating number with no outcome fails education feeds. Name what they’ll learn (`why humans preferred 1.3B`) and show a simple proof chip by 3s. Still **do not** dump RLHF bullet decks — that’s body. See [edtech-hooks.md](edtech-hooks.md).

### 4. Soft float = dead air
Entrance pop then gentle float for 5–8s is not a hook. Need **2–3 beats** tied to VO:
- Beat 0: punch-in hero
- Beat 1: at contrast word (e.g. when “175B” or “1.3B” lands) — scale snap / swap / strike
- Beat 2: optional badge or second line

### 5. Text-heavy generated “assets”
AI comparison graphics with titles + bullets count as **on-screen text**. They violate the ≤6-word rule even if `on_screen` in JSON is short. Prefer cutout stickers or type-only Pattern B.

### 6. Broken glyphs / tofu
Missing emoji boxes (□ after “Preferred”) = reject asset and regenerate without emoji, or use SVG/icon fonts that render.

### 7. Karaoke walls
Full multi-line caption pills compete with the hero. Prefer:
- ≤1 short caption line, or
- punch-words only (the shock nouns/numbers), romanized Telugu

### 8. Textbook titles via asset
Banned in copy: “Introduction”, “Overview”, “Parameter Efficiency”, “Model Size vs Alignment Quality”. Titles inside images are still banned.

### 9. Duration drift
Prefer VO **1.5–5s**. If VO >6s, warn the user — long VO invites explainer layouts. Still follow VO length, but keep visual sparse.

---

## Recipe → build checklist

Before render:

- [ ] `on_screen` ≤6 words **and** asset has no extra readable paragraphs
- [ ] Pattern A = one sticker; Pattern B = one giant number (not both stacked with a report card)
- [ ] `why_it_stops_scroll` is curiosity/shock — not “we explain the full comparison”
- [ ] If VO is open-loop, visual does not answer it
- [ ] Timeline has ≥2 seekable beats after t=0 (not only float)
- [ ] Asset inspected for tofu / watermark / tiny unreadable type

## QA frame checklist

- [ ] t≈0.4s: thumb test pass
- [ ] Mid-VO: a second beat happened (not identical to t=0.4)
- [ ] No WINNER/label spam
- [ ] Captions thin; hero still readable
- [ ] Audio = that hook VO @ full level; SFX entrance @ 0.8

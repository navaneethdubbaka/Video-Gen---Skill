# Visual quality gates (anti-slideshow)

These gates exist because all-card SaaS slides fail against the Insider Force / clean-tech sticker look.

## 1. Pattern variety (required)

Every scene must set `pattern` to a letter from the active style pack (`A`–`K` for `insider-force-short`).

| Gate | Fail if |
| --- | --- |
| Diversity | `< 4` distinct pattern letters across the storyboard (when ≥6 scenes) |
| Repeat ban | Same pattern letter used on **more than 2 consecutive** scenes |
| Card monopoly | Patterns that are “card chrome” (`C`, `D`, `G`, `I`) exceed **50%** of scenes |
| Kinetic breath | Zero `J` (pure kinetic type) scenes when duration ≥ 45s |
| Signature mix | Missing **both** of: at least one `H` (icon list) **or** one `A` (sticker); and at least one `J` |

Suggested minimum mix for ~60–90s: `A`, `B` or `F`, `J`, `H` or `G`, plus others.

## 2. No double titles (required)

Never render the same headline twice:

- Card/doc title **and** a matching bold line under the card = **fail**
- Pick **one**: either the card carries the title, **or** the kinetic line under it does

`text.content` should not equal / paraphrase the card’s internal H1.

## 3. Less text per frame (required)

| Element | Max |
| --- | --- |
| Kinetic / dual-tone line | **2–6 words** |
| Card body | **≤ 2 short lines** (≈ ≤ 18 words total on-card) |
| Tables / 3-column grids | **Forbidden** unless VO is literally listing metrics — then max **3 rows**, no truncated labels |
| Subtitle under headline | **≤ 8 words**, and must add new info (not repeat title) |

If the VO says more, **cut to the next scene** — do not stuff the card.

## 4. Captions lighter (required)

- Karaoke pill is **support**, not the design. Use the slim insider-force caption skin.
- Pattern `J` / `K` / empty kinetic holds: prefer **in-frame dual-tone type** as the reading surface; karaoke may stay but must not dominate (smaller pill, lower opacity).
- Do not stack: huge card title + huge mid headline + full-width karaoke of the same words.

## 5. Better assets (required)

| Prefer | Avoid |
| --- | --- |
| Sticker cutouts (thick white border) | Generic crystal brain / abstract AI stock |
| Real UI / paper / chart crops | Empty invent SVG “infographics” |
| Entity photos when named | Random laptop renders with illegible fake code |

`text_only` / pattern `J` is the main exception (no hero image).

## 6. One accent color (required for insider-force-short)

Palette: black / gray / white + **one** accent (default lime `#5EFC8D`).  
Fail rainbow pastel checklist cards (blue+green+purple+orange pills in one frame).

## 7. Breathing beats (required)

At least **one** pure kinetic / empty beat (`pattern: J`) every **~15–20s** of runtime  
(or ≥ 1 per 4–5 scenes when shorter).

## 8. Motion feel (required)

| Pattern | Motion |
| --- | --- |
| `A` sticker | Strong scale pop (0.85→1) + SFX `pop` |
| `J` kinetic | Word/line stagger; **longer hold**; no busy card motion |
| Dense cards (`D`/`G`/`I`) | **Shorter** hold; quick settle — then cut |
| All | `window.__timelines` seekable GSAP; not static posters |

## 9. Retention / growth gates (required)

These exist so videos get **watched and followed**, not just look clean.

### Hook (scene 1)

| Gate | Rule |
| --- | --- |
| Pattern | Scene 1 `pattern` must be **`A` (sticker) or `B` (big number)** — never open on a dense card (`C`/`D`/`G`/`I`) |
| On-screen text | Scene 1 `text.content` ≤ **6 words** |
| Timing | Scene 1 duration ≤ **3.5s** (payoff before scroll) |
| Feel | Claim / surprise / number — not a textbook title |

### Scene length (pacing)

| Gate | Rule |
| --- | --- |
| Average | Mean scene duration ≤ **4.0s** (when ≥5 scenes) |
| Hard max | No scene longer than **6.0s** unless `pattern` is `J` (kinetic breath may hold to 7s) |
| Density | Prefer more short scenes over one stuffed card |

### CTA / follow (end)

| Gate | Rule |
| --- | --- |
| Window | At least one scene whose `start` is within the **last 8s** of the video |
| Pattern | That scene (or last scene) should be **`J` or `K`** |
| Role | Set `"role": "cta"` on the CTA scene |
| Copy | Explicit follow / Part 2 / open loop — not another definition slide |
| Open loop | Prefer ending mid-story (“details next”) over a closed essay |

### First frame / packaging (agent + QA warn)

Write `analysis/packaging.json` (or storyboard top-level `packaging`):

```json
{
  "title": "curiosity + specific claim (not textbook)",
  "first_frame_note": "giant number OR sticker face — almost no body text",
  "series_tag": "optional recurring end phrase",
  "comment_bait": "optional one opinion beat near end"
}
```

Fail-soft (warn) if missing when duration ≥ 30s.

## Agent checklist before compose

```text
- [ ] Every scene has pattern A–K
- [ ] ≥4 distinct patterns; no 3-in-a-row same letter
- [ ] ≥1 J breath; card patterns ≤50%
- [ ] No double titles
- [ ] No clipped multi-column walls of text
- [ ] Accent = one color
- [ ] Assets are stickers/UI/paper (not generic AI stock)
- [ ] Scene 1 = A or B, ≤6 words, ≤3.5s
- [ ] Avg scene ≤4s; no scene >6s (7s only for J)
- [ ] CTA in last 8s (role: cta, pattern J/K)
- [ ] packaging title + first_frame_note noted
```

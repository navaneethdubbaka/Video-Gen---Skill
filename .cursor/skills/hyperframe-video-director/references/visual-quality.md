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

## 10. Vertical composition (required) — kill top-heavy slides

Failure mode seen in production: every scene = small card in the **upper third** + dual-tone mid + karaoke at the bottom edge, with a huge empty band in between. Reads as PowerPoint, not a Short.

| Gate | Rule |
| --- | --- |
| Hero scale | Hero card / sticker / mockup must occupy roughly **38–55% of frame height** (not a postage stamp floating high) |
| Grouping | Card + kinetic line are one **tight visual group** (gap card→headline ≤ ~6% of frame height) |
| Dead band | Fail if a large empty band (>~18% of frame height) sits between the kinetic line and the karaoke pill with nothing intentional there |
| Vertical center | The main group’s optical center should sit near **40–52%** from the top — not jammed into the top 30% |
| Pattern `J`/`K` | Type may sit mid-frame; still avoid orphaning a tiny pill alone at the bottom |

## 11. Phone-readable type (required) — no micro-text cards

If a viewer cannot read it in ~1s on a phone at arm’s length, **cut it**.

| Element | Min / max |
| --- | --- |
| Kinetic primary line | Large display (≥ ~64px @1080 wide); secondary gray still ≥ ~40px and contrast ≥ mid-gray `#6B6B6B` (not washed `#8A8A8A`) |
| Card H1 | ≤ **6 words**, readable |
| Card body | **≤ 2 short lines** OR **one** big number / one short quote (≤ ~12 words) |
| Metric cells | Max **2** stats per card; each number huge, label ≤ 3 words; **one accent color only** (no blue+green+purple rainbow cells) |
| Quotes / paper dumps | Forbidden as paragraphs. Use **1 punch line** or split into a new scene |
| Nested UI chrome | Fake code editors / multi-box rank cards must keep body ≥ ~22px equivalent — if labels blur, simplify to sticker/`H`/`J` |

## 12. Karaoke is support, not garbage fragments (required)

| Gate | Fail if |
| --- | --- |
| Orphan tokens | Pill shows a lone function word / fragment (`ikkada`, `gaa`, `lo`, `to`, `ee`) with no content noun/verb in the same window |
| Split pills | Active word rendered as a **separate** green/gray mini-pill beside a dark pill (looks broken) — keep **one** slim pill; only `.is-active` changes color inside it |
| Same words thrice | Card title + mid kinetic + karaoke all restating the same claim |
| Safe zone | Karaoke sits inside the bottom **~180px @1080×1920** Reels/TikTok UI collision zone — keep pill **above** that band (roughly y ≤ 1740) |

On pattern `J`/`K` and sticker hooks: prefer **hiding or heavily fading** karaoke when in-frame dual-tone already carries the line.

## 13. Chrome discipline (required)

| Element | Rule |
| --- | --- |
| Series / EP badge | At most **once in the first 5s** OR on the CTA — **not** on every card corner. Constant `RLHF • EP 3` badges = noise |
| Corner overlap | Badges must not half-clip the card radius; fully inside with ≥12px inset **or** fully outside as a top chip |
| Watermark / URL | Still forbidden (`insiderforce.io`, etc.) |
| Brand chip on CTA | `INSIDER FORCE` (or user brand) OK on `J`/`K` close only — not on body cards |

## 14. Layout recipe variety (required)

Do not ship N scenes that all read as: **floating card → dual-tone → karaoke**.

| Gate | Rule |
| --- | --- |
| Recipe cap | ≤ **40%** of scenes may use the full three-layer stack (hero card + mid kinetic + visible karaoke) |
| Alternates | Mix full-bleed stickers, big-number, pure `J`, icon-list `H`, laptop `F`, brand `E` where karaoke is off or minimal |
| Asset clarity | Stickers must read in 0.5s (face, logo, clear object). Abstract blobs / illegible icons that need a label inside the badge = fail → replace asset |

## 15. First frame + motion truth (required)

| Gate | Rule |
| --- | --- |
| t=0 content | Frame at **0.00s** must already show the hook hero (or its scale-in mid-flight) — **no blank gray studio** |
| Entrance | Hero opacity/scale begins by ≤ **80ms**; do not delay first paint for “polish” |
| Idle vs poster | After entrance, allow soft float — but if a snapshot mid-scene looks identical to a static PNG with no prior motion, fail motion QA |

## Agent checklist before compose

```text
- [ ] Every scene has pattern A–K
- [ ] ≥4 distinct patterns; no 3-in-a-row same letter
- [ ] ≥1 J breath; card patterns ≤50%
- [ ] No double titles (card H1 ≠ mid kinetic; no paraphrase)
- [ ] No micro-text / rainbow metric walls / paper dumps
- [ ] Accent = one color
- [ ] Assets are stickers/UI/paper (not generic AI stock); icons read in 0.5s
- [ ] Hero group not top-heavy; card+headline tightly grouped; no dead mid band
- [ ] ≤40% scenes use full card+kinetic+karaoke stack
- [ ] EP/series badge sparse (not every card)
- [ ] Karaoke: one pill, no orphan fragments, above platform safe zone
- [ ] Scene 1 = A or B, ≤6 words, ≤3.5s; visible at t=0
- [ ] Avg scene ≤4s; no scene >6s (7s only for J)
- [ ] CTA in last 8s (role: cta, pattern J/K)
- [ ] packaging title + first_frame_note noted
```

## Post-render vision pass (required)

After draft/final MP4 (or contact sheet), **vision-inspect ≥8 frames** spaced across the timeline. Fail the draft if any of these recur:

1. Top-heavy card + empty lower half
2. Unreadable card body / rainbow stats
3. Double title (card + matching kinetic)
4. Orphan karaoke fragments or dual split pills
5. EP badge on most cards
6. Blank or near-blank opening frame
7. Same three-layer recipe on consecutive scenes

Write findings into `qa/visual-notes.md` (bullet list) before promoting `renders/final/final.mp4`.

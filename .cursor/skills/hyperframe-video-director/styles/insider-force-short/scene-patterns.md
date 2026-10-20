# Scene patterns — insider-force-short

Pick **one pattern letter per storyboard scene** (`pattern: "A"` … `"K"`).  
Match the narration concept, not the reference topic.

**Hard gates** (also in [../../references/visual-quality.md](../../references/visual-quality.md)):

1. When ≥6 scenes: use **≥4 distinct** letters.
2. Never the **same letter 3× in a row**.
3. Card-heavy letters `C`/`D`/`G`/`I` ≤ **50%** of scenes.
4. Duration ≥45s → include **≥1 `J`** (pure kinetic breath).
5. Include **≥1 `A` (sticker) or `H` (icon list)** plus the `J` breath.
6. **No double titles** (card H1 ≠ mid-frame headline).
7. **≤2 lines** of body on any card; kinetic lines **2–6 words**.
8. Palette: black/gray/white + **one** accent (`#5EFC8D`) — no rainbow pastels.
9. **Hook:** scene 1 = **A or B** only, ≤6 words, ≤3.5s (`role: hook`); visible at **t=0** (no blank open).
10. **Pacing:** avg scene ≤4s; max 6s (7s only for `J`).
11. **CTA:** last 8s = `J`/`K` with `role: cta` (follow / Part 2 / open loop).
12. **No top-heavy slides:** hero ~38–55% frame height; tight card→headline gap; no giant empty band above karaoke.
13. **Phone-readable cards:** max 2 metric cells; one accent; no paper-paragraph dumps; no rainbow stats.
14. **Recipe cap:** ≤40% scenes may stack card + mid kinetic + visible karaoke; mix `A`/`B`/`E`/`F`/`H`/`J`/`K` with karaoke off/minimal.
15. **EP badge sparse:** series chip ≤ once early OR on CTA — never every card corner.
16. **Karaoke:** one slim pill, phrase-coherent windows, above bottom ~180px safe zone; no split green mini-pills.
## A — Hook sticker

**When:** Opening claim, villain/surprise reaction, brand “didn’t see this coming”.  
**Layout:** Centered cutout subject with **thick white border + soft shadow**; optional faded brand mark behind; dual-tone caption below (**no second title**).  
**Asset:** Real photo/PNG cutout (downloaded + cached). Border is CSS; subject is `<img>`.  
**Motion:** Strong pop/scale-in (0.85→1) → caption words. SFX `pop`.  
**Ref:** `refs/ref_01.jpg`  
**Do not:** invent SVG brand marks; do not paste reference celebrity pixels; do not use generic crystal-brain stock.

## B — Big number + device

**When:** Huge stat (“744 billion”, “25 GB”, “1 token/s”).  
**Layout:** Device/screen upper half; **huge black number** + gray unit word below (that *is* the title — no extra H1).  
**Motion:** Device float; number punch. SFX `hit`.  
**Ref:** `refs/ref_02.jpg`

## C — Floating product site card

**When:** Naming the tool / showing the product surface.  
**Layout:** Centered rounded website/app card with soft shadow; **minimal chrome**; ≤2 lines of UI copy.  
**Motion:** Card rises with slight tilt settle.  
**Ref:** `refs/ref_03.jpg`  
**Build original UI** — do not screenshot the reference site.

## D — Doc / paper card + orbiting marks

**When:** Credibility, paper, model card, “on par with…”.  
**Layout:** White rounded doc card; 1–2 small square logos orbiting corners; **one** gray caption under (not a repeat of the paper title).  
**Body:** Short quote or 1 chart — not a full research dump.  
**Ref:** `refs/ref_04.jpg`

## E — Center brand mark beat

**When:** Tool name reveal, logo sting.  
**Layout:** Huge negative space; centered mark + wordmark; no clutter.  
**Ref:** `refs/ref_05.jpg`

## F — Floating laptop / hardware

**When:** “on your laptop”, “machine you already own”, local/privacy.  
**Layout:** Centered laptop/phone with readable screen crop or sticker cutout; soft ground shadow; short caption.  
**Prefer:** real UI screenshot on screen / sticker cutout over empty 3D mock with fake blur code.  
**Ref:** `refs/ref_06.jpg`, `refs/ref_09.jpg`

## G — Warm product info card

**When:** Spec sheet, maker/size/status, CTA “Run it”.  
**Layout:** Beige/tan rounded card; sans tags + **serif body**; black CTA pill; **≤3 metadata rows**.  
**Ref:** `refs/ref_07.jpg`

## H — Icon deny/allow list

**When:** “No GPU / No cloud / No bill” style beats.  
**Layout:** Vertical list; black circles with white ✕ or ✓; bold labels; progressive reveal (upcoming line in gray).  
**Ref:** `refs/ref_08.jpg`  
**Use at least once** when the VO lists absences/benefits.

## I — Social proof card

**When:** Stars, forks, downloads, “2 weeks”.  
**Layout:** White GitHub-like stats card; soft shadow; **one** accent highlight on the key number.  
**Ref:** `refs/ref_10.jpg`  
**Use real numbers** from the user’s topic when available.

## J — Pure kinetic type

**When:** Emphasis lines, CTA speech, moral of story, **breathing beat**.  
**Layout:** No hero asset; 2–4 centered lines; bold keywords (#111); trailing word gray (#6B).  
**Ref:** `refs/ref_11.jpg`  
**Required** at least once per ≥45s video. Longer hold. Karaoke pill slim/optional — the type *is* the caption.

## K — Dot-grid symbol panel

**When:** Follow/CTA / brand close (without watermark).  
**Layout:** Light dot-grid rounded panel; large symbol; dual-tone caption; **empty footer** (no URL).  
**Ref:** `refs/ref_12.jpg` (grammar only — invent your own symbol if needed)

---

## Motion + SFX (all patterns)

| Layer | Default |
| --- | --- |
| Hero entrance | 0.35–0.5s scale + opacity + slight y (`power3.out` or back.out on stickers) |
| Captions | Dual-tone in-frame **or** slim karaoke — not both shouting the same words |
| Idle | Slow 8–12s yoyo float on mockups only; kinetic type stays still after reveal |
| Boundary SFX | `pop` (sticker/icon), `whoosh` (cut/slide), `hit` (big number), `rise` (crossfade) @ **volume 0.8** |
| Inter-frame | Alternate `cut` with `zoom-through` / `push-slide` / `crossfade` |

Never ship a pattern as a static PNG/HTML still.

## Caption recipe

```text
In-frame (preferred for J / hooks / stickers):
  [keyword bold #111] [support gray #6B]   ← 2–6 words; secondary ≥ #6B6B6B contrast

Karaoke (support — often OFF on J/A/B):
  ONE slim dark pill; lime .is-active on the word INSIDE the pill
  Never: orphan fragments (ikkada / gaa / lo alone)
  Never: separate green mini-pill glued beside the dark pill
  Keep above Reels/TikTok UI (bottom ~180px @1080×1920)

Chrome:
  EP/series badge sparse; Footer EMPTY (no watermark)
```

## Suggested arc (~60–100s)

1. Hook sticker (**A**, `role: hook`, ≤3.5s)  
2. Big number (**B**) or kinetic claim (**J**)  
3. Problem / status quo (**J** or **D**)  
4. Product / site (**C** or **E**)  
5. How it works (**F**)  
6. Spec card (**G**) — keep short  
7. Deny list (**H**)  
8. Honesty / breath (**J**)  
9. Social proof (**I**) — optional  
10. CTA kinetic (**J** or **K**, `role: cta`, last 8s) — follow / Part 2 — **no channel watermark**

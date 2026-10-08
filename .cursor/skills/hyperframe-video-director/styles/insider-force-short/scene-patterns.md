# Scene patterns — insider-force-short

Pick one pattern per storyboard scene. Match the narration concept, not the reference topic.

## A — Hook sticker

**When:** Opening claim, villain/surprise reaction, brand “didn’t see this coming”.  
**Layout:** Centered cutout subject with **thick white border + soft shadow**; optional faded brand mark behind; dual-tone caption below.  
**Motion:** Pop/scale-in sticker → caption words.  
**Ref:** `refs/ref_01.jpg`  
**Do not:** paste reference celebrity pixels; commission/source a new cutout or use abstract icon.

## B — Big number + device

**When:** Huge stat (“744 billion”, “25 GB”, “1 token/s”).  
**Layout:** 3D hand/device or floating screen upper half; **huge black number** + gray unit word below.  
**Motion:** Device float; number punch.  
**Ref:** `refs/ref_02.jpg`

## C — Floating product site card

**When:** Naming the tool / showing the product surface.  
**Layout:** Centered rounded website/app card with soft shadow on light studio bg; minimal chrome.  
**Motion:** Card rises with slight tilt settle.  
**Ref:** `refs/ref_03.jpg`  
**Build original UI** — do not screenshot the reference site.

## D — Doc / paper card + orbiting marks

**When:** Credibility, paper, model card, “on par with…”.  
**Layout:** White rounded doc card; 1–2 small square logos orbiting corners; gray caption underneath.  
**Ref:** `refs/ref_04.jpg`

## E — Center brand mark beat

**When:** Tool name reveal, logo sting.  
**Layout:** Huge negative space; centered mark + wordmark; no clutter.  
**Ref:** `refs/ref_05.jpg`

## F — Floating laptop / hardware

**When:** “on your laptop”, “machine you already own”, local/privacy.  
**Layout:** Centered 3D laptop/phone; soft ground shadow; short caption above or below.  
**Ref:** `refs/ref_06.jpg`, `refs/ref_09.jpg`

## G — Warm product info card

**When:** Spec sheet, maker/size/status, CTA “Run it”.  
**Layout:** Beige/tan rounded card; sans tags + **serif body**; black CTA pill.  
**Ref:** `refs/ref_07.jpg`

## H — Icon deny/allow list

**When:** “No GPU / No cloud / No bill” style beats.  
**Layout:** Vertical list; black circles with white ✕ or ✓; bold labels; progressive reveal (upcoming line in gray).  
**Ref:** `refs/ref_08.jpg`

## I — Social proof card

**When:** Stars, forks, downloads, “2 weeks”.  
**Layout:** White GitHub-like stats card; soft shadow; teal highlight on star count ok.  
**Ref:** `refs/ref_10.jpg`  
**Use real numbers** from the user’s topic when available.

## J — Pure kinetic type

**When:** Emphasis lines, CTA speech, moral of story.  
**Layout:** No hero asset; 2–4 centered lines; bold keywords; trailing word in gray.  
**Ref:** `refs/ref_11.jpg`

## K — Dot-grid symbol panel

**When:** Follow/CTA / brand close (without watermark).  
**Layout:** Light dot-grid rounded panel; large symbol; dual-tone caption; **empty footer** (no URL).  
**Ref:** `refs/ref_12.jpg` (grammar only — invent your own symbol if needed)

---

## Motion + SFX (all patterns)

Every pattern above **must** include:

| Layer | Default |
| --- | --- |
| Hero entrance | 0.4s scale 0.92→1 + opacity 0→1 + slight y (power3.out) |
| Captions | Staggered dual-tone word/line reveals |
| Idle | Slow 8–12s yoyo float or Ken-Burns on mockups |
| Boundary SFX | `pop` (sticker/icon), `whoosh` (cut/slide), `hit` (big number), `rise` (crossfade) |
| Inter-frame | Alternate `cut` with `zoom-through` / `push-slide` / `crossfade` |

Never ship a pattern as a static PNG/HTML still.

## Caption recipe (all patterns)

```text
Line 1: [keyword bold #111] [support gray #8A]
Line 2: optional second dual-tone line
Footer: EMPTY (no watermark)
```

Keep captions short — 2–6 words per line. Sync to VO stress.

## Suggested arc for this genre (~60–100s)

1. Hook sticker (A)  
2. Big number (B)  
3. Problem / status quo (J or D)  
4. Product name / site (C or E)  
5. How it works metaphor (F)  
6. Spec card (G)  
7. Deny list (H)  
8. Honesty beat — “not fast” (J)  
9. Social proof (I)  
10. CTA kinetic (J or K) — **no channel watermark**

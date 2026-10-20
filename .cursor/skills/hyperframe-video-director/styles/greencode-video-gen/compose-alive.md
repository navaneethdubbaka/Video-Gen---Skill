# Compose alive — greencode-video-gen

Hard compose contract so Shorts feel like a **host reacting to ideas**, not a looping GIF screensaver with debug chrome.

## Failures that must never ship

| Anti-pattern | Why it kills the piece |
| --- | --- |
| Near-black / void stage behind host | Pack is **light studio** now — black plates look broken next to keyed alpha hosts |
| Host GIF sped up to fit scene length | Mouth looks frantic; play at **native 1x** (12fps keyed loops) |
| Photos that don't match the VO line | Generic stock / wrong entity = trust kill |
| Top badge `GREENCODE // …` / `PATTERN [X]` | Debug chrome |
| Storyboard `concept` as subtitle | Agent notes, not viewer text |
| Same layout every scene | Slideshow |
| Card title **and** mid-frame H1 same words | Double titles |
| Host GIF + GSAP yoyo forever | Screensaver |
| Same expression many scenes in a row | Host never reacts |
| Host overlapping kinetic type / karaoke | Unreadable |

## Stage background (non-negotiable)

- Canvas / root fill: **`#EDEDED`–`#F4F4F4`** light studio (Insider-Force-like air).
- **Forbidden:** `#0A0A0A`, `#111111`, pure black void, black rounded plate behind the host.
- Host WebP/GIF already has **alpha** — composite directly on the light stage. Do **not** chroma-key again. Do **not** put the host in a black box.

## Content visuals MUST match the script

Every non-`J` scene with a graphic / photo:

1. Read that scene's VO / `narration_link`.
2. `visual.search_query` = the **exact nouns** being said (product, UI, person, concept).
3. Resolve via `/media-use` or fetch; **vision-check** the file depicts that subject.
4. Reject: abstract AI-brain, random neon, mood landscapes, wrong brand, decorative `</>` only.
5. `generated_graphic` cards still need a **real** `<img>` of the subject when the VO names one.
6. Fail QA if image and VO would not pass a "what is this about?" glance test.

Follow parent [asset-research.md](../../references/asset-research.md) strictly — greencode does **not** get a free pass for filler stock.

## Forbidden on-canvas chrome

Never render: `GREENCODE`, `GREEN CODE`, `greencode video gen`, `PATTERN [A]`, DNA marks, raw `concept` strings.

## Layout structure (9:16)

```text
┌─────────────────────────┐
│  LIGHT STAGE #EDEDED    │  ← NO black void
│                         │
│   GRAPHIC STAGE         │  ← max ~38–48% frame height
│   (script-matched img)  │
│                         │
│   short kinetic line    │
│                         │
│  HOST          karaoke  │  ← alpha host lower-LEFT
│  (keyed, 1x speed)      │
└─────────────────────────┘
```

## Host playback — keyed talking loops

**Primary:** `host_talking/<id>/talking_loop.gif` (prefer over webp for timing).  
Source: `host_talking_loop_gif/` keyed by `key_talking_loop_gifs.py` at **12fps**.

### Speed rules (non-negotiable)

1. Playback rate = **1.0**. Never `data-playback-rate` ≠ 1 on the host.
2. Never time-stretch / speed the mouth loop so it finishes inside a short scene.
3. If scene < loop length: soft-loop OR freeze after ~1 cycle — **do not** accelerate.
4. GSAP: entrance only (0.35–0.5s). **No** infinite yoyo.
5. Missing talking GIF → `host_stills/<id>.png` (static). Never invent speed.

```html
<img id="host-img" class="host-character" src="assets/host/<expr>_talk.gif" alt="" />
```

### Asset pipeline

| Path | Role |
| --- | --- |
| `host_talking_loop_gif/*_talking_loop.gif` | User green-screen talking GIFs |
| `host_talking/<id>/talking_loop.gif` | **Primary** compose host (keyed, 12fps) |
| `host_talking/<id>/talking_loop.webp` | Fallback |
| `host_stills/<id>.png` | Still when no keyed loop |

**Forbidden expression:** `shock`.

### Expression = scene reaction

| Beat | Host id |
| --- | --- |
| Hook | `hang` / `point_up` / `facepalm_lite` |
| Explain | `lean_in` / `talk_emph` / `talk_loop` |
| Showcase | `present` |
| Number / UI | `point_up` / `thumbs_up` |
| Think / list | `think` |
| Win / CTA | `celebrate` / `wave` / `thumbs_up` |
| Soft / fail | `shrug` / `cross_arms` / `facepalm_lite` |
| Pattern `J` | **no host** |

Diversity: ≤2 identical in a row; ≥4 distinct when ≥8 scenes.

## Graphic motion

Every non-J scene needs ≥2 of: hero entrance, staggered reveal / typewriter, punch-in, one transition SFX @ 0.8.

## Vision QA before final

Fail on: black stage, black host plate, sped-up mouth, image≠VO, greencode badges, concept subtitles, double titles. Write `qa/visual-notes.md`.

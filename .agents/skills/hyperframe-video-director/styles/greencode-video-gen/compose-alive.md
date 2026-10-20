# Compose alive — greencode-video-gen

Hard compose contract so Shorts feel like a **host reacting to ideas**, not a looping GIF screensaver with debug chrome.

Learned from QA of `videos/llm-series-ep3/renders/final/final.mp4`.

## Failures that must never ship

| Anti-pattern | Why it kills the piece |
| --- | --- |
| Top badge `GREENCODE // …` / `PATTERN [X]` / “greencode video gen” | Looks like debug UI / skill name, not a real Short |
| Storyboard `concept` dumped as on-screen subtitle | Meta notes for agents, not viewers |
| Same layout every scene (top bar + giant card + headline + host) | Slideshow; violates pattern diversity |
| Card title **and** mid-frame H1 saying the same thing | Double titles |
| Host GIF looping forever **plus** GSAP yoyo bob forever | Robotic “screensaver” feel |
| Same `talk_loop` for many scenes in a row | Host never reacts |
| Host overlapping kinetic type / karaoke | Unreadable |
| Hero card ~900px tall on 1920 | Top-heavy postage stamp; no air |
| EP / series chip every frame | Chrome spam |

## Forbidden on-canvas chrome

Never render any of:

- `GREENCODE`, `GREEN CODE`, `greencode video gen`, `greencode-video-gen`
- `LLM_EP_XX`, `PATTERN [A]`, pattern letters as UI
- Channel DNA marks, watermarks, handle bars
- Raw `concept` / `narration_link` / search_query strings

Series branding (if user asks) = **at most once** early OR on CTA — never every scene.

## On-screen text rules

1. Only `text.content` (2–6 words kinetic) and ≤2 lines of **designed** card body that a viewer needs.
2. Never put `concept`, packaging notes, or romanization debug on the canvas.
3. If the hero asset already contains a big title, leave mid-frame `text.content` empty (or the reverse) — **no double titles**.
4. Karaoke = one slim pill; do not invent a second caption row.

## Layout structure (9:16)

```text
┌─────────────────────────┐
│  (empty / optional 1×   │  ← NO greencode badge
│   series chip sparse)   │
│                         │
│   GRAPHIC STAGE         │  ← max ~38–48% frame height
│   (card / kinetic /     │
│    sticker)             │
│                         │
│   short kinetic line    │  ← mid, clear of host head
│                         │
│  HOST          karaoke  │  ← host lower-LEFT ~32–42% H
│  (keyed)                │
└─────────────────────────┘
```

- Host **lower-left**, not center-bottom covering the title.
- Keep a clear lane for karaoke above the bottom ~180px safe zone.
- Pattern **J**: full-bleed kinetic, **no host**, no top bar, no card.

## Host playback — talking mouth loops (primary)

**Primary host assets are mouth-talking WebPs** from `host_talking/<id>/talking_loop.webp` (built by skill `host-mouth-talk` from `host_stills` PNGs).

Why: pose still changes per beat (expression diversity), while a seamless ~4s mouth loop reads as speaking — without a second infinite bob.

### Required: talking host + entrance only

```html
<img id="host-img" class="host-character" src="assets/host/<expr>_talk.webp" alt="" />
```

GSAP (only):

1. Entrance 0.35–0.5s (`y` + opacity + slight scale, `back.out`)
2. **No** infinite yoyo / breathe stacked on the mouth loop
3. **Allowed:** `talking_loop.webp` (prefer) or `.gif` — mouth motion only
4. **Forbidden:** infinite GSAP yoyo; `shock`

### Asset pipeline

| Path | Role |
| --- | --- |
| `greencode/my_animations/host_talking/<id>/talking_loop.webp` | **Primary** compose host |
| `greencode/my_animations/host_talking/<id>/talking_loop.gif` | Preview / fallback |
| `greencode/my_animations/host_stills/*.png` | Masters for mouth calib + still fallback |
| `.cursor/skills/host-mouth-talk/` | Build / re-measure mouth loops |

**Forbidden expression:** `shock` — too uncanny; never pick it.

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

Diversity: same expression ≤ **2** consecutive; ≥ **4** distinct when ≥8 scenes. Use the **full** catalog — no bias to only the newest poses.

## Graphic motion — alive stage

Every non-J scene needs **at least two** of:

- Hero entrance (scale/y/opacity)
- Staggered list/row reveal OR typewriter/cursor on code cards
- Keyword punch on dual-tone words
- Boundary SFX (`pop` / `whoosh` / `hit` / `rise` @ 0.8)

Idle after entrance: cards may soft-float ≤4px; kinetic type stays still once revealed.

## Pattern ≠ identical chrome

`pattern` chooses **layout recipe** (see [scene-patterns.md](scene-patterns.md)), not a shared top-bar template. Implementing “every frame gets top-bar + 900px card + host” is a **pack failure** even if pattern letters differ in JSON.

## Pre-render QA (vision)

Inspect ≥8 frames. Fail if any recur:

- Greencode / PATTERN badge visible
- Concept-string subtitles
- Host looping hard for full scene duration with big bob
- Double titles
- Host covering mid headline
- Three-in-a-row identical compositions

Write findings to `qa/visual-notes.md` before promoting `final.mp4`.

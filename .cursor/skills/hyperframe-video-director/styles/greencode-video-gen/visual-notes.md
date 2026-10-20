# Visual notes — greencode-video-gen grammar

Extracted from the local reference webm (16:9, ~3:41, 4K). Pack output is **9:16**.

## Look (pack override vs reference)

| Reference source | **This pack ships** |
| --- | --- |
| Near-black void stage | **Light studio** `#EDEDED`–`#F4F4F4` |
| White + green type on black | Near-black + green type on light |
| Green-screen hosts keyed in-compose | Offline-keyed alpha GIF/WebP; no black plate |
| Speedy / stretched mouth loops | **12fps native 1x** — never time-stretch |

- Persistent anime host who reacts (point, hang, talk) beside graphics — not a faceless sticker short.
- Terminal / neon green accents on type and UI chrome.
- Pixel or monospace display for some headlines; clean sans for body.
- Slim karaoke above safe zone + in-frame dual-tone (near-black + green).
- Soft host ground shadow; graphics pop in with GSAP.
- **Content photos must match that scene’s VO** — no random stock.

## 9:16 remap

| 16:9 source | 9:16 pack |
| --- | --- |
| Host left, content right | Host lower-left ~35–45% height; content upper / mid |
| Wide terminal panels | Narrow vertical cards / stacked lists |
| Full-body host ok | Prefer bust talking GIFs from `host_talking/` |

## Host keying

Green is removed **offline** (`key_talking_loop_gifs.py`). Compose with alpha GIF on the **light** stage. Never leave green boxes; never put the host on a black rectangle.

## Script-matched assets

Every graphic scene: `search_query` / `narration_link` = what the VO says. Vision-check before lock. Fail if image and VO would fail a “what is this about?” glance test. See [asset-research.md](../../references/asset-research.md).

## Anti-clone

Rebuild diagrams, code cards, and entity images with original / licensed assets. Use **your** host catalog only.

## QA lessons from `llm-series-ep3` final.mp4

Failed ship criteria observed:

1. **`GREENCODE // LLM_EP_03` + `PATTERN [X]`** every scene — debug chrome, not product.
2. **Concept strings** as grey subtitles (“…hook with host reaction”).
3. **Identical stack** every beat: badge → huge terminal card → dual title → looping host.
4. **Host screensaver:** looping WebP/GIF + continuous GSAP bob; weak expression variety.
5. **Double titles** (card header + mid headline) and host covering type.
6. **Black void stage** next to transparent hosts — looks broken; use light stage.
7. **Sped-up mouth loops** — play at native 1x.
8. **Mismatched stock photos** — every image must match that scene’s script line.

Fix contract: [compose-alive.md](compose-alive.md).

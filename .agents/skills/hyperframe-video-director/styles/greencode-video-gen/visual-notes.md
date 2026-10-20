# Visual notes — greencode-video-gen grammar

Extracted from the local reference webm (16:9, ~3:41, 4K). Pack output is **9:16**.

## Look

- Near-black void stage (`#0A0A0A`–`#111111`).
- Persistent anime host who reacts (point, hang, talk) beside graphics — not a faceless sticker short.
- Terminal / neon green accents on type and UI chrome.
- Pixel or monospace display for some headlines; clean sans for body.
- Bottom captions in source; for Shorts use slim karaoke above safe zone + in-frame dual-tone (white + green).
- Soft host ground shadow; graphics pop in with GSAP.

## 9:16 remap

| 16:9 source | 9:16 pack |
| --- | --- |
| Host left, content right | Host lower-left ~35–45% height; content upper / mid |
| Wide terminal panels | Narrow vertical cards / stacked lists |
| Full-body host ok | Prefer bust GIFs from `greencode/my_animations/host/` |

## Chroma key

User host GIFs ship with solid green screen. Always key out green in compose (CSS / preprocess). Never leave green boxes in the final frame.

## Anti-clone

Rebuild diagrams, code cards, and entity images with original / licensed assets. Use **your** host catalog only.

## QA lessons from `llm-series-ep3` final.mp4

Failed ship criteria observed:

1. **`GREENCODE // LLM_EP_03` + `PATTERN [X]`** every scene — debug chrome, not product.
2. **Concept strings** as grey subtitles (“…hook with host reaction”).
3. **Identical stack** every beat: badge → huge terminal card → dual title → looping host.
4. **Host screensaver:** looping WebP/GIF + continuous GSAP bob; weak expression variety.
5. **Double titles** (card header + mid headline) and host covering type.

Fix contract: [compose-alive.md](compose-alive.md).

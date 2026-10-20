# Scene patterns — greencode-video-gen

Pick **one pattern letter per storyboard scene** (`pattern: "A"` … `"K"`).  
Also set `visual.host_expression` (catalog id) except for pattern `J` (host off).

**Hard gates** (also in [../../references/visual-quality.md](../../references/visual-quality.md)):

1. When ≥6 scenes: use **≥4 distinct** letters.
2. Never the **same letter 3× in a row**.
3. Card-heavy letters `C`/`D`/`I` ≤ **50%** of scenes.
4. Duration ≥45s → include **≥1 `J`** (pure kinetic breath, no host).
5. Include **≥1 `A` (hook host)** plus the `J` breath on longer pieces.
6. **No double titles** (card H1 ≠ mid-frame headline).
7. **≤2 lines** of body on any card; kinetic lines **2–6 words**.
8. Palette: black + white/gray + **one** terminal green (`#39FF14`) — no rainbow pastels.
9. **Hook:** scene 1 = **A or B** only, ≤6 words, ≤3.5s (`role: hook`); visible at **t=0**.
10. **Pacing:** avg scene ≤4s; max 6s (7s only for `J`).
11. **CTA:** last 8s = `J`/`K` with `role: cta`.
12. **Host:** resolve via [character-catalog.md](character-catalog.md). Chroma-key green. Playback rules in [compose-alive.md](compose-alive.md) — **no infinite yoyo + GIF loop**.
13. **No DNA / channel watermark.** No `GREENCODE //` / `PATTERN [X]` / skill-name chrome on canvas.
14. **No concept leak:** never render storyboard `concept` as subtitle.
15. **Layout variety:** each pattern letter = different composition recipe. Forbidden: one shared top-bar + 900px card + host template for every scene.
16. **Host expression diversity:** ≤2 identical `host_expression` in a row; ≥4 distinct when ≥8 scenes.
17. **Hero height:** graphic stage ≤ **48%** of frame (≈920px @1920); host lower-left, clear of mid headline.

## A — Hook host

**When:** Opening claim, surprise, “wait for it”.  
**Layout:** Host `hang` / `point_up` / `talk_emph` with **large empty stage** — small or no card; ≤6-word headline in free space (not duplicated on a card).  
**Host:** `hang` / `point_up` / `talk_emph` — **never `shock`**.  
**Motion:** Host pop + headline punch. SFX `pop`. **No top badge.**  
**Ref:** `refs/ref_01.jpg`, `refs/ref_02.jpg`  
**Do not:** full terminal card + same headline underneath; do not use `shock`.

## B — Big number

**When:** Huge stat (“$5,000”, “3 GPTs”, “100K”).  
**Layout:** Giant white/green number upper-mid; host `point_up` or `point_side` lower-left.  
**Host:** `point_up` / `point_side` / `talk_emph`.  
**Motion:** Number punch; host float. SFX `hit`.  
**Ref:** `refs/ref_09.jpg` (metrics energy — rebuild original numbers)

## C — Code / terminal card

**When:** Code, tokenizer, NumPy, model name.  
**Layout:** Dark monospace panel upper-mid; green accents; host `talk_loop` lower-left.  
**Host:** `talk_loop`.  
**Motion:** Card rise + type cursor blink optional.  
**Ref:** `refs/ref_04.jpg`, `refs/ref_07.jpg`

## D — Architecture / diagram

**When:** Layers, blocks, “how it works”.  
**Layout:** Simplified original diagram (not cloned); host `talk_loop` or `think`.  
**Host:** `talk_loop` / `think`.  
**Do not:** paste reference architecture tables verbatim.

## E — Name / brand sting

**When:** Series title, tool name reveal.  
**Layout:** Huge negative space; centered wordmark; host peek `idle_bob` or brief `point_up`.  
**Host:** `idle_bob` / `point_up`.

## F — Compare / split / device

**When:** Before/after, two options, “on your laptop”.  
**Layout:** Two stacked cards or device crop; host `point_side`.  
**Host:** `point_side`.  
**Ref:** `refs/ref_06.jpg` (grammar — original footage/UI only)

## G — Checklist reveal

**When:** Reasons list, milestones, deny/allow.  
**Layout:** Vertical list; green headers; progressive reveal; host `think` → later `celebrate`.  
**Host:** `think` then `celebrate` on done beats.  
**Ref:** `refs/ref_03.jpg`

## H — Entity sticker + reaction

**When:** Named person / company / product.  
**Layout:** Researched cutout or UI sticker; host `point_side` or `talk_emph`.  
**Host:** `point_side` / `talk_emph` / `talk_loop` — **never `shock`**.  
**Asset:** real downloaded entity image ([../../references/entity-images.md](../../references/entity-images.md)).

## I — Quote / paper beat

**When:** Soft claim, honesty, “I forgot how to…”.  
**Layout:** Short dark card ≤2 lines; host `shrug` or `think`.  
**Host:** `shrug` / `think`.

## J — Pure kinetic (no host)

**When:** Emphasis breath, moral, density break.  
**Layout:** No host; 2–4 centered white/green lines on black.  
**Host:** **off** (`host_expression: null`).  
**Required** ≥1× when duration ≥45s.

## K — CTA close

**When:** Follow / Part 2 / donate-adjacent CTA (user’s CTA, not cloned charity copy).  
**Layout:** Host `celebrate` or `point_side` + short dual-tone CTA; empty footer.  
**Host:** `celebrate` / `point_side`.  
**Ref:** `refs/ref_12.jpg`

---

## Motion + SFX (all patterns)

| Layer | Default |
| --- | --- |
| Host entrance | 0.35–0.5s scale + opacity (`back.out` on hooks) |
| Host idle | Slow 8–12s yoyo float; GIF provides face motion |
| Graphics | Pop / rise with `power3.out` |
| Captions | Dual-tone in-frame **or** slim karaoke — not both shouting |
| Boundary SFX | `pop` / `whoosh` / `hit` / `rise` @ **volume 0.8** |
| Inter-frame | Alternate `cut` with `zoom-through` / `push-slide` / `crossfade` |

## Host chroma key (compose)

```css
/* Approximate CSS chroma — prefer preprocess to transparent when possible */
.host-gif {
  mix-blend-mode: normal;
  /* If using a keyed <canvas>/SVG filter pipeline, target #00FF00 */
}
```

Storyboard must set:

```json
"visual": {
  "host_expression": "talk_loop",
  "host_asset": "greencode/my_animations/host/talk_loop.gif"
}
```

Resolve with `python <SKILL_DIR>/scripts/resolve_host_expression.py --expression talk_loop`.

## Suggested arc (~45–90s Short)

1. Hook host (**A**, `hang`/`point_up`/`talk_emph`, ≤3.5s) — never `shock`  
2. Big number (**B**) or kinetic claim (**J**)  
3. Problem list (**G**)  
4. Code card (**C**)  
5. Diagram (**D**) or entity (**H**)  
6. Honesty / breath (**J** or **I**)  
7. CTA (**K**, last 8s) — no watermark  

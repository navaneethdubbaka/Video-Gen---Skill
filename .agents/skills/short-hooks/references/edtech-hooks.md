# Edtech / explainer reel hooks (what actually works)

Sources distilled for this skill (2025–2026 short-form education practice):

- [Superdirector — Education Reels hooks](https://superdirector.app/hooks/reels/education)
- [Superdirector — Education TikTok hooks](https://superdirector.app/hooks/tiktok/education)
- [Vidiotion — 7 short-form hook patterns](https://vidiotion.com/blog/short-form-hook-patterns)
- [ReelsBuilder — 15 education hooks](https://reelsbuilder.ai/blog/15-hooks-for-education-reels-ready-to-use)
- [Captions.ai — scroll-stopping openings](https://captions.ai/blog/video-hooks-how-to-write-a-scroll-stopping-opening)

Apply this when the VO / topic is **edtech, LLM explainers, study tips, concept breakdowns** (our default niche). Lifestyle/entertainment hooks can stay mystery-led; education should not.

---

## Core rule (education ≠ entertainment)

| Entertainment hook | Edtech hook |
| --- | --- |
| Mystery / open loop / “wait for it” | **Clear knowledge contract** in 1–2s |
| Tease the answer | Name the outcome + the friction |
| Vague curiosity | Specific misconception or takeaway |
| “Why?” with no promise | “You learned X wrong — here’s what actually happens” |

Education viewers decide: *“Will I learn something useful if I stay?”*  
If the first frame only shows a floating number and “why?”, they swipe — clarity beats mystery here.

---

## Mute-first contract (mandatory)

Most Reels/Shorts are scrolled **muted**.

1. **Hook text on screen by frame ~6** (first ~0.2s), not after VO finishes a sentence.
2. **One line**, readable at phone arm’s length.
3. Place primary hook text in **upper or upper-middle** — never the bottom third (platform UI covers it). Karaoke can sit lower; the *hook claim* must not.
4. Same words spoken + on screen (redundancy is correct for education).

---

## Timing (first 3 seconds)

| Window | Must happen |
| --- | --- |
| 0–0.4s | Motion + hook line visible (nothing static/empty) |
| 0.4–1.5s | Spoken hook lands; matches on-screen text |
| 1.5–3.0s | **First payoff visual** that proves the promise (diagram beat, struck myth, vs chip, sticker proof) |

If payoff is not visible by ~3s, the hook is a preamble.

---

## Edtech formulas (prefer these)

Map VO meaning → one of these. Prefer over pure `open_loop`.

### `myth_bust` (strongest for EduTok)
On-screen: `you learned THIS wrong` / `bigger ≠ better`  
Visual: strike the myth, reveal the correct short claim.  
Example (InstructGPT): `BIGGER WASN'T BETTER`

### `knowledge_gap`
On-screen: specific fact they think they know, undercut.  
Example: `175B LOST TO 1.3B`

### `countdown_promise` (most reliable for teaching)
On-screen: `in 20s: why 1.3B won`  
Trades drama for a clear contract. Best when VO is longer.

### `stated_cost` / giant contrast
On-screen: real number contrast with meaning attached.  
**Not** bare `1.3B` alone — attach the outcome: `1.3B BEAT 175B` *and* prove it with a simple vs chip by 3s.

### `quiz_dare`
On-screen: `which model won — A or B?` then reveal.  
Comments do half the teaching.

### `example_first`
On-screen: `this one result` + show the preference / ranking visual immediately.

### `open_loop` — **demote for edtech**
Only if the VO itself is a cliffhanger *and* the on-screen line still names the topic (`why HUMANS preferred 1.3B`). Never bare `why?`.

---

## Visual grammar for faceless edtech hooks

What works in-feed for LLM / tech explainers:

1. **Claim line** (dual-tone, ≤6–8 words) upper-middle from frame 1  
2. **One proof object by 3s** — sticker, vs chip, struck word, simple rank card (not a body-length report)  
3. **Kinetic beats on meaning words** — not soft float for 8s  
4. **Thin punch captions** for Telugu/English VO; claim line ≠ full karaoke dump  

What fails (our bad runs):

- Giant number alone with no knowledge contract  
- “why?” teaser that withholds the lesson  
- Body-scene comparison tables / bullet decks  
- Hook text only in the bottom caption pill  
- Static first frame  

---

## Recipe fields (edtech)

When writing `hooks.json` for education topics, also set:

| Field | Rule |
| --- | --- |
| `on_screen` | Outcome or misconception — readable muted |
| `knowledge_contract` | One line: what viewer gets if they stay |
| `proof_by_3s` | What visual appears before 3s that proves the claim |
| `formula` | Prefer myth_bust / knowledge_gap / countdown_promise / example_first |
| `why_it_stops_scroll` | Must mention the *learning itch*, not just “big number” |

### InstructGPT / params example (good)

```text
formula: myth_bust
on_screen: BIGGER WASN'T BETTER
knowledge_contract: Why humans preferred 1.3B over 175B
proof_by_3s: simple vs chip — 1.3B ✓ vs 175B ✕ (no bullets)
beats: 0s claim → ~1.5s vs chip → VO contrast snap → hold (answer stays for body)
```

### Bad (what we shipped)

```text
formula: giant_number + open_loop
on_screen: 1.3B / why?
proof_by_3s: none (number float only)
→ fails mute test + fails knowledge contract
```

---

## QA additions (edtech)

- [ ] Mute at 0s: do you know what you’ll learn?
- [ ] Hook text in upper/mid third by 0.2s
- [ ] Proof visual by 3s
- [ ] Not pure mystery / bare “why?”
- [ ] One idea only; no body explainer deck

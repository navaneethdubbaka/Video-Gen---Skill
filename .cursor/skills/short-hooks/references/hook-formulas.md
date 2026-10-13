# Hook formulas (scroll-stoppers)

Each variant must use a **different** formula. On-screen ≤6 words. Duration 1.5–3.5s. Pattern **A** (sticker) or **B** (big number).

## Formulas

### `shock_claim`
Bold counter-intuitive statement.  
Examples: `it was never encryption` · `they shipped it broken`  
Pattern: A or J-feel but still A/B only → prefer **A** with subject sticker.

### `giant_number`
One huge number + gray unit.  
Examples: `117M` / `parameters` · `10×` / `overnight`  
Pattern: **B**

### `forbidden`
Deny list energy in one line.  
Examples: `no GPU` · `no fine-tune`  
Pattern: **A** with ✕ badge, or **B** if a zero/none number.

### `open_loop`
Promise unfinished story.  
Examples: `then we decoded it` · `part you missed`  
Pattern: **A** — face/UI sticker + incomplete line (trailing gray word).

### `villain`
Name the antagonist / lazy assumption.  
Examples: `everyone trusted the token` · `base models ignore you`  
Pattern: **A**

### `before_after`
Two-beat flip inside the hook (still ≤3.5s).  
On-screen: `fine-tune required` → punch to `zero-shot works`  
Pattern: **B** then micro cut, or single card with strikethrough.

## Writing rules

1. **Specific > clever.** Nouns from the actual video topic.
2. **Spoken energy.** Words you’d say out loud in 1 breath.
3. **No textbook titles.** Ban: “Introduction”, “Overview”, “What is GPT”.
4. **Romanize Telugu** for glyphs; keep meaning.
5. **First frame test:** if the thumbnail is only small gray text, fail — need sticker or giant type.

## Mapping user seeds

| User seed vibe | Formula |
| --- | --- |
| Big stat | `giant_number` |
| “Nobody tells you…” | `shock_claim` or `villain` |
| “No X / without Y” | `forbidden` |
| “Wait until…” / cliffhanger | `open_loop` |
| Contrast then/now | `before_after` |

If two seeds map to the same formula, rewrite the weaker one to the nearest unused formula **without** changing the claim.

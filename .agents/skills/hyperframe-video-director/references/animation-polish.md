# Animation polish (external skills)

These skills are **not copied into** `hyperframe-video-director`. Install them on the host agent, then this skill **routes** to them during compose.

## Install once (host machine)

```bash
# HyperFrames (keep fresh)
npx hyperframes skills update hyperframes-animation hyperframes-keyframes motion-graphics hyperframes-registry hyperframes-creative

# Motion taste + GSAP craft (skills.sh)
npx skills add emilkowalski/skills@improve-animations
npx skills add emilkowalski/skills@animation-vocabulary
npx skills add emilkowalski/skills@review-animations
npx skills add emilkowalski/skills@find-animation-opportunities
npx skills add greensock/gsap-skills@gsap-core
npx skills add greensock/gsap-skills@gsap-timeline
npx skills add greensock/gsap-skills@gsap-performance

# Optional design taste
npx skills add leonxlnx/taste-skill@high-end-visual-design
npx skills add pbakaus/impeccable@impeccable
```

Antigravity / Claude Code: same `npx skills add …` into that product’s skills directory (or copy installed folders).

## When to load (during Step 8)

| Phase | Skills to read / follow |
| --- | --- |
| Before writing any frame HTML | `/hyperframes-animation` (rules + 1 blueprint if needed), `/hyperframes-keyframes` if punch/zoom, `/hyperframes-registry` before inventing a named effect |
| Hook / CTA / kinetic `J` beats | `/motion-graphics` vocabulary for count-up, kinetic type, logo sting |
| After first pass of all frames | `find-animation-opportunities` → list dead holds |
| Fix pass | `improve-animations` + `animation-vocabulary` + `gsap-timeline` / `gsap-performance` |
| Before lint | `review-animations` on 2–3 hero frames + captions |
| Optional taste pass | `high-end-visual-design` / `impeccable` if frames look generic SaaS |

## Hard constraints (still HyperFrames)

External GSAP skills must **not** break seek-safety:

- One paused timeline per composition → `window.__timelines[id]`
- Prefer `gsap.set` / timeline tweens — **no** `tl.call()` for caption state (seek won’t fire)
- No `Math.random`, no wall-clock `Date.now` for motion
- Transforms/opacity only for perf (`gsap-performance`)

## If a polish skill is missing

Do **not** stop the run. Log a warn, continue with `/hyperframes-animation` only, and tell the user which `npx skills add` to run.

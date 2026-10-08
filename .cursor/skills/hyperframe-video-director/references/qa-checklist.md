# Video QA checklist

Run after each draft render / snapshot pass. Structural helper:

```bash
python <SKILL_DIR>/scripts/qa_report.py --project <PROJECT>
```

## Timing

- [ ] Voice starts at t=0 (or intentional lead-in ≤150ms)
- [ ] Visual changes align with narration segment boundaries
- [ ] No major dead air with static unrelated visuals
- [ ] No scene ends before its narration ends
- [ ] No scene lingers long after its narration

## Motion / transitions / SFX (fail the draft if any miss)

- [ ] Every frame has GSAP entrance (hero + captions) — not a frozen poster
- [ ] Inter-frame transitions injected (`transitions.mjs verify` passes; not all-cuts unless requested)
- [ ] `audio_meta.json` `sfx` non-empty; whoosh/pop/hit audible on scene changes
- [ ] Optional BGM ducked under VO (if present)

## Visual quality

- [ ] No overlapping / colliding elements
- [ ] No clipped text
- [ ] No off-screen assets
- [ ] Captions readable against background (scrim/contrast OK)
- [ ] Images not stretched
- [ ] Animations not broken / stuck
- [ ] No unexpected black or blank frames

## Style

Compare snapshots to `analysis/style-spec.json`:

- [ ] Typography position/weight matches
- [ ] Pacing/cut language matches
- [ ] Image treatment matches
- [ ] Motion language matches
- [ ] Transition language matches

## Content

- [ ] Each scene's visual represents the narration concept
- [ ] Language of on-screen text matches VO (unless translation requested)
- [ ] No copied reference footage/logos

## Iteration

```text
render_v1 → QA → fix → render_v2 → QA → final.mp4
```

Fix the specific failing scene; re-run assemble/check/snapshot; promote only when QA passes.

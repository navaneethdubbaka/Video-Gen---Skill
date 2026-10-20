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

## Images (fail before compose if any miss)

- [ ] ≤20% scenes are `text_only`
- [ ] Every other scene has `search_query` + `asset_path` on disk
- [ ] Assets vision-checked as narration-relevant (not generic filler)
- [ ] Frame HTML uses `<img>`/`<video>` for those assets (not SVG-only fakes)
- [ ] `python …/qa_report.py --project <PROJECT> --phase assets` PASSes

## Motion / transitions / SFX (fail the draft if any miss)

- [ ] Every frame has GSAP entrance (hero + captions) — not a frozen poster
- [ ] Inter-frame transitions injected (`transitions.mjs verify` passes; not all-cuts unless requested)
- [ ] `audio_meta.json` `sfx` non-empty; each cue `"volume": 0.8` (80%); whoosh/pop/hit audible on scene changes
- [ ] Pattern diversity: every scene has `pattern` A–K; ≥4 distinct; no 3-in-a-row; cards ≤50%; ≥1 `J` breath ([visual-quality.md](visual-quality.md))
- [ ] No double titles; no clipped multi-column text walls; one accent color
- [ ] Assets are stickers/UI/paper — not generic AI-brain stock; karaoke pill is slim
- [ ] Hook: scene 1 = A/B, ≤6 words, ≤3.5s
- [ ] Pacing: avg scene ≤4s; no scene >6s (7s only for J)
- [ ] CTA in last 8s (`role: cta`, pattern J/K) — follow / Part 2 / open loop
- [ ] `packaging.title` + `first_frame_note` set (curiosity title, not textbook)
- [ ] Optional BGM ducked under VO (if present)

## Visual quality

- [ ] No overlapping / colliding elements
- [ ] No clipped text
- [ ] No off-screen assets
- [ ] Captions readable against background (scrim/contrast OK)
- [ ] Images not stretched
- [ ] Animations not broken / stuck
- [ ] No unexpected black or blank frames
- [ ] **Not top-heavy:** hero + kinetic are a tight mid group; no giant empty band above karaoke ([visual-quality.md](visual-quality.md) §10)
- [ ] **Phone-readable:** no micro-text cards, paper dumps, or rainbow multi-color metric cells (§11)
- [ ] **No double titles** / paraphrase stacks (card H1 ≠ mid kinetic) (§2)
- [ ] **Karaoke:** one slim pill; no orphan fragments; above bottom ~180px safe zone (§12)
- [ ] **Chrome:** EP/series badge sparse (not every card); no half-clipped corner badges (§13)
- [ ] **Recipe variety:** ≤40% scenes use full card+kinetic+karaoke stack (§14)
- [ ] **t=0:** hook hero visible (not blank studio) (§15)
- [ ] Stickers/icons read in 0.5s (no abstract unlabeled blobs)

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

## Post-render vision (before promoting final)

- [ ] Vision-inspect ≥8 frames across the MP4 / contact sheet
- [ ] Write `qa/visual-notes.md` with pass/fail bullets
- [ ] Do **not** promote `renders/final/final.mp4` while any §10–15 fail recurs

## Iteration

```text
render_v1 → QA → vision notes → fix → render_v2 → QA → final.mp4
```

Fix the specific failing scene; re-run assemble/check/snapshot; promote only when QA passes.

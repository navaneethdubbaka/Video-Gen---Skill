# Workflow checklist + resume rules

Copy into the run notes and tick as you go.

```text
Task Progress:
- [ ] 0 doctor
- [ ] 1 init project
- [ ] 2 ingest reference + voiceover
- [ ] 3 probe + extract frames
- [ ] 4 style_spec.json
- [ ] 5 transcript.json
- [ ] 6 storyboard.json (pattern A–K + hook/CTA/pacing + packaging; visual-quality gates)
- [ ] 7a entities.json + fetch_entity_image + apply_entity_assets (public figures/companies)
- [ ] 7b remaining assets researched + vision-inspected + cached
- [ ] 7c every non-text_only scene has asset_path; qa_report --phase assets PASS
- [ ] 8 HyperFrames init + bridge scripts
- [ ] 8b compose frames with real img + GSAP window.__timelines
- [ ] 8b2 animation polish (Emil/GSAP skills if installed — animation-polish.md)
- [ ] 8c captions + fetch-sfx + assemble
- [ ] 8d transitions.mjs inject + verify
- [ ] 9 QA (structural + visual + motion/SFX + image relevance)
- [ ] 9b iterate if needed
- [ ] 10 final render promoted
```

## Resume rules

**First check VO fingerprint.** After ingest, read `input/voiceover.sha256.json`. If `changed: true` or `VO_CHANGED=1`, treat the project as dirty — do **not** resume storyboard/assets/frames.

| Gate artifact | If present |
| --- | --- |
| `videos/<slug>/` tree | Skip init **only** for the same VO topic; new VO topic → new slug |
| `input/reference.*` | Skip download unless user changed source |
| `input/voiceover.*` + matching `voiceover.sha256.json` | Skip re-copy if fingerprint matches source |
| `analysis/media-probe.json` | Skip probe unless media changed |
| `analysis/frames/` non-empty | Skip extract unless reference changed |
| `analysis/style-spec.json` | Skip style analysis unless user asks redo (style packs may stay) |
| `analysis/transcript.json` | Skip STT **only if** VO fingerprint unchanged |
| `storyboard/storyboard.json` | Skip **only if** VO fingerprint + instructions unchanged |
| Cached `assets/` + frame HTML | Skip **only if** storyboard unchanged; never keep old images for a new VO |
| `composition/hyperframes/hyperframes.json` | Skip `hyperframes init` shell only; still rebuild frames when storyboard changes |
| `composition/hyperframes/audio_meta.json` | Rebuild if storyboard/VO changed |
| `qa/report.json` with pass | Proceed to final if visual QA also clean **and** VO fingerprint unchanged |

### Forbidden resume pattern

❌ Open an old project → drop in a new `voiceover.wav` → keep old `compositions/frames/*` and old `assets/images/*` → only rebuild captions/audio_meta.

✅ New slug (preferred) **or** `ingest_voiceover.py --project … --source … --invalidate` then re-run steps 5→10.

Always re-run `doctor.py` when tools fail mysteriously.

## Ask only when needed

Ask at most one concise question if:

- Reference download fails and no local file exists
- Voiceover path is missing
- `ELEVENLABS_API_KEY` is unset (and fixture mode not authorized)

Do not ask about aspect, language, or style when they can be derived from reference + transcript.

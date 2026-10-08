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
- [ ] 6 storyboard.json
- [ ] 7 assets cached / resolved
- [ ] 8 HyperFrames init + bridge scripts
- [ ] 8b compose frames + captions + assemble
- [ ] 9 QA (structural + visual)
- [ ] 9b iterate if needed
- [ ] 10 final render promoted
```

## Resume rules

| Gate artifact | If present |
| --- | --- |
| `videos/<slug>/` tree | Skip init |
| `input/reference.*` | Skip download unless user changed source |
| `input/voiceover.*` | Skip copy |
| `analysis/media-probe.json` | Skip probe unless media changed |
| `analysis/frames/` non-empty | Skip extract unless reference changed |
| `analysis/style-spec.json` | Skip style analysis unless user asks redo |
| `analysis/transcript.json` | Skip STT unless VO changed |
| `storyboard/storyboard.json` | Skip storyboard unless transcript/style/instructions changed |
| `composition/hyperframes/hyperframes.json` | Skip `hyperframes init` |
| `composition/hyperframes/audio_meta.json` | Rebuild only if storyboard/VO changed |
| `qa/report.json` with pass | Proceed to final if visual QA also clean |

Always re-run `doctor.py` when tools fail mysteriously.

## Ask only when needed

Ask at most one concise question if:

- Reference download fails and no local file exists
- Voiceover path is missing
- `ELEVENLABS_API_KEY` is unset (and fixture mode not authorized)

Do not ask about aspect, language, or style when they can be derived from reference + transcript.

# short-hooks workflow (VO → standalone visuals)

```text
Task Progress:
- [ ] 0 doctor
- [ ] 1 init_run.py --vo … (or --vo-dir)
- [ ] 2 transcribe each input/vo/hN.*
- [ ] 3 hooks.json recipes (distinct formulas + thumb-test intent)
- [ ] 4 one sparse asset per hook (or type-only Pattern B)
- [ ] 5 HyperFrames build (VO + visual + SFX + ≥2 beats)
- [ ] 6 render renders/hook-hN.mp4
- [ ] 7 qa/ thumb test + deliver table
```

Gate references: [hook-formulas.md](hook-formulas.md), [visual-quality.md](visual-quality.md), [edtech-hooks.md](edtech-hooks.md).

## Gates (do not skip)

| Step | Fail if… |
| --- | --- |
| 3 recipes | Asset search implies comparison table / bullets / textbook title |
| 3 recipes | Edtech hook has no `knowledge_contract` / mute can’t tell what you’ll learn |
| 3 recipes | Bare `why?` or number-only with no outcome line |
| 4 assets | Text-heavy infographic, tofu glyphs, watermark |
| 5 build | Only entrance + soft float; no proof visual by 3s; no mid-VO beat |
| 7 QA | Mute thumb test fails; hook text only in bottom third; WINNER/label spam |

## Resume

| Artifact | Action |
| --- | --- |
| `input/vo/hN.*` | Skip re-copy |
| `analysis/hN/transcript.json` | Skip STT unless VO changed |
| `hooks.json` with filled `hooks[]` | Skip expand unless user changes intent **or** visual-quality gate fails |
| `renders/hook-hN.mp4` | Skip that render unless QA fails thumb test |

## Optional stitch

Only if user explicitly wants hook+body: see [stitch.md](stitch.md) + `--body` on init.
Default deliverable is **standalone** `hook-hN.mp4`.

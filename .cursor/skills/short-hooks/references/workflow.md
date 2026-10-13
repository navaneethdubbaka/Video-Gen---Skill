# short-hooks workflow (VO → standalone visuals)

```text
Task Progress:
- [ ] 0 doctor
- [ ] 1 init_run.py --vo … (or --vo-dir)
- [ ] 2 transcribe each input/vo/hN.*
- [ ] 3 hooks.json recipes (distinct formulas)
- [ ] 4 one real asset per hook
- [ ] 5 HyperFrames build (VO + visual + SFX)
- [ ] 6 render renders/hook-hN.mp4
- [ ] 7 qa/ + deliver table
```

## Resume

| Artifact | Action |
| --- | --- |
| `input/vo/hN.*` | Skip re-copy |
| `analysis/hN/transcript.json` | Skip STT unless VO changed |
| `hooks.json` with filled `hooks[]` | Skip expand unless user changes intent |
| `renders/hook-hN.mp4` | Skip that render |

## Optional stitch

Only if user explicitly wants hook+body: see [stitch.md](stitch.md) + `--body` on init.
Default deliverable is **standalone** `hook-hN.mp4`.

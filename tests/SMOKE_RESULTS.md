# Smoke test results

Last run: deterministic pipeline via `python tests/run_smoke.py`

## Result

| Field | Value |
| --- | --- |
| Status | **PASS** (`ok: true`) |
| Project | `videos/smoke-director-short` |
| STT mode | `fixture` (no `ELEVENLABS_API_KEY` in environment) |
| Scenes | 3 |
| Voice clips | 3 (`assets/voices/01.wav` … `03.wav`) |
| Frames extracted | 6 |
| QA | errors=0, warns=0 |

Machine-readable: [`fixtures/smoke_result.json`](fixtures/smoke_result.json)

## What was validated

1. `doctor.py` — ffmpeg, ffprobe, yt-dlp, node, npx, hyperframes CLI
2. Project scaffold + reference/VO ingest
3. Probe + frame extract
4. Transcript ingest (fixture path; live ElevenLabs when key is set)
5. `style_spec_to_frame_md` / `storyboard_to_hyperframes` / `build_audio_meta_from_vo`
6. Structural `qa_report.py`

## Not covered in this smoke (agent + HyperFrames compose)

- Vision style analysis of a real reference
- Full HTML frame composition / `npx hyperframes render`
- Live ElevenLabs STT (set `$env:ELEVENLABS_API_KEY` and re-run)

## Live STT

```powershell
$env:ELEVENLABS_API_KEY = "your-key"
python tests/run_smoke.py
```

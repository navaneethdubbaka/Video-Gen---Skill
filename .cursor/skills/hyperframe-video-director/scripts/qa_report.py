#!/usr/bin/env python3
"""Structural QA against storyboard, transcript, assets, and media probe."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _util import read_json, resolve_project, write_json  # noqa: E402


IMAGE_TYPES = {
    "photograph",
    "screenshot",
    "icon",
    "video_clip",
    "diagram",
    "multiple",
    "generated_graphic",  # still requires a real asset_path wrapping media
}


def resolve_asset(project: Path, asset_path: str) -> Path | None:
    if not asset_path:
        return None
    p = Path(asset_path)
    candidates = [
        p if p.is_absolute() else project / p,
        project / "composition" / "hyperframes" / p,
        project / "composition" / "hyperframes" / "public" / p.name,
    ]
    for c in candidates:
        if c.is_file():
            return c
    return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True)
    parser.add_argument("--tolerance", type=float, default=0.35, help="seconds allowed VO vs storyboard drift")
    parser.add_argument(
        "--phase",
        choices=("assets", "pre_render", "all"),
        default="all",
        help="assets=image gate only; pre_render/all include sfx/transition checks when artifacts exist",
    )
    args = parser.parse_args()

    project = resolve_project(args.project)
    issues: list[dict] = []

    sb_path = project / "storyboard" / "storyboard.json"
    tr_path = project / "analysis" / "transcript.json"
    probe_path = project / "analysis" / "media-probe.json"
    style_path = project / "analysis" / "style-spec.json"
    hf = project / "composition" / "hyperframes"

    if not sb_path.is_file():
        issues.append({"level": "error", "code": "missing_storyboard", "msg": str(sb_path)})
    if not tr_path.is_file():
        issues.append({"level": "error", "code": "missing_transcript", "msg": str(tr_path)})
    if not style_path.is_file():
        issues.append({"level": "error", "code": "missing_style_spec", "msg": str(style_path)})

    sb = read_json(sb_path) if sb_path.is_file() else {}
    tr = read_json(tr_path) if tr_path.is_file() else {}
    probe = read_json(probe_path) if probe_path.is_file() else {}

    scenes = sb.get("scenes") or []
    if not scenes:
        issues.append({"level": "error", "code": "no_scenes", "msg": "storyboard has zero scenes"})

    text_only_count = 0
    missing_asset = 0
    generated_without_asset = 0

    prev_end = 0.0
    for i, scene in enumerate(scenes):
        sid = scene.get("scene_id", i + 1)
        start = float(scene.get("start", 0))
        end = float(scene.get("end", 0))
        if end <= start:
            issues.append({"level": "error", "code": "bad_timing", "scene": sid, "msg": f"end<=start ({start}-{end})"})
        if i > 0 and start + 1e-3 < prev_end:
            issues.append({"level": "warn", "code": "overlap", "scene": sid, "msg": f"overlaps previous (start={start}, prev_end={prev_end})"})
        if i > 0 and start - prev_end > 0.75:
            issues.append({"level": "warn", "code": "gap", "scene": sid, "msg": f"gap after previous ({start - prev_end:.2f}s)"})
        if not (scene.get("narration") or "").strip():
            issues.append({"level": "warn", "code": "empty_narration", "scene": sid, "msg": "empty narration"})

        pat = (scene.get("pattern") or "").strip().upper()
        if not pat or not re.fullmatch(r"[A-K]", pat):
            issues.append(
                {
                    "level": "error",
                    "code": "missing_pattern",
                    "scene": sid,
                    "msg": "scene.pattern required (A–K for insider-force-short) — see visual-quality.md",
                }
            )

        text_content = ((scene.get("text") or {}).get("content") or "").strip()
        if text_content:
            words = [w for w in re.split(r"\s+", text_content) if w]
            if len(words) > 12:
                issues.append(
                    {
                        "level": "warn",
                        "code": "text_too_long",
                        "scene": sid,
                        "msg": f"text.content has {len(words)} words — keep kinetic lines 2–6 words / cards ≤2 lines",
                    }
                )

        visual = scene.get("visual") or {}
        vtype = (visual.get("type") or "").lower()
        query = (visual.get("search_query") or "").strip()
        asset_path = (visual.get("asset_path") or "").strip()

        # Entity tagged but unresolved
        ent = visual.get("entity") or (visual.get("requirement") or {}).get("entity")
        if ent and not asset_path:
            issues.append(
                {
                    "level": "error",
                    "code": "entity_unresolved",
                    "scene": sid,
                    "msg": f"visual.entity={ent!r} but no asset_path - run fetch_entity_image.py + apply_entity_assets.py",
                }
            )

        if vtype == "text_only":
            text_only_count += 1
        else:
            if not query:
                issues.append(
                    {
                        "level": "error",
                        "code": "missing_search_query",
                        "scene": sid,
                        "msg": "non-text_only scene needs visual.search_query tied to narration",
                    }
                )
            if not asset_path:
                missing_asset += 1
                issues.append(
                    {
                        "level": "error",
                        "code": "missing_asset_path",
                        "scene": sid,
                        "msg": "set visual.asset_path after caching a real image (see asset-research.md)",
                    }
                )
            else:
                found = resolve_asset(project, asset_path)
                if not found:
                    issues.append(
                        {
                            "level": "error",
                            "code": "asset_file_missing",
                            "scene": sid,
                            "msg": f"asset_path not on disk: {asset_path}",
                        }
                    )
            if vtype == "generated_graphic" and not asset_path:
                generated_without_asset += 1

        prev_end = max(prev_end, end)

    if scenes:
        # Visual quality / anti-slideshow (pattern diversity)
        patterns = [(scene.get("pattern") or "").strip().upper() for scene in scenes]
        valid_pats = [p for p in patterns if re.fullmatch(r"[A-K]", p)]
        if len(scenes) >= 6 and len(set(valid_pats)) < 4:
            issues.append(
                {
                    "level": "error",
                    "code": "pattern_diversity",
                    "msg": (
                        f"only {len(set(valid_pats))} distinct pattern(s) — need ≥4 "
                        "(avoid all-card slideshow; see visual-quality.md)"
                    ),
                }
            )
        for i in range(len(valid_pats) - 2):
            if valid_pats[i] and valid_pats[i] == valid_pats[i + 1] == valid_pats[i + 2]:
                issues.append(
                    {
                        "level": "error",
                        "code": "pattern_triple_repeat",
                        "msg": f"pattern {valid_pats[i]} repeats 3× in a row starting scene index {i + 1}",
                    }
                )
                break
        card_pats = {"C", "D", "G", "I"}
        card_n = sum(1 for p in valid_pats if p in card_pats)
        if valid_pats and card_n / len(valid_pats) > 0.5 + 1e-9:
            issues.append(
                {
                    "level": "error",
                    "code": "too_many_card_patterns",
                    "msg": f"{card_n}/{len(valid_pats)} scenes are card patterns C/D/G/I — max 50%",
                }
            )
        total_dur = float(sb.get("total_duration_s") or (scenes[-1].get("end") if scenes else 0) or 0)
        if total_dur >= 45 and "J" not in valid_pats:
            issues.append(
                {
                    "level": "error",
                    "code": "missing_kinetic_breath",
                    "msg": "duration ≥45s needs ≥1 pattern J (pure kinetic type) breathing beat",
                }
            )
        if len(scenes) >= 4 and not ({"A", "H"} & set(valid_pats)):
            issues.append(
                {
                    "level": "warn",
                    "code": "missing_sticker_or_icon_list",
                    "msg": "include at least one pattern A (sticker) or H (icon list) for signature look",
                }
            )

        # Retention / growth: hook, pacing, CTA, packaging
        first = scenes[0]
        first_pat = (first.get("pattern") or "").strip().upper()
        first_dur = float(first.get("end", 0)) - float(first.get("start", 0))
        first_text = ((first.get("text") or {}).get("content") or "").strip()
        first_words = [w for w in re.split(r"\s+", first_text) if w]
        if first_pat and first_pat not in ("A", "B"):
            issues.append(
                {
                    "level": "error",
                    "code": "weak_hook_pattern",
                    "msg": f"scene 1 pattern={first_pat!r} — hook must be A (sticker) or B (big number)",
                }
            )
        if first_words and len(first_words) > 6:
            issues.append(
                {
                    "level": "error",
                    "code": "hook_text_too_long",
                    "msg": f"scene 1 text has {len(first_words)} words — hook max 6",
                }
            )
        if first_dur > 3.5 + 1e-9:
            issues.append(
                {
                    "level": "error",
                    "code": "hook_too_long",
                    "msg": f"scene 1 is {first_dur:.2f}s — hook max 3.5s",
                }
            )

        durs = []
        for scene in scenes:
            d = float(scene.get("end", 0)) - float(scene.get("start", 0))
            durs.append(d)
            pat = (scene.get("pattern") or "").strip().upper()
            limit = 7.0 if pat == "J" else 6.0
            if d > limit + 1e-9:
                issues.append(
                    {
                        "level": "error",
                        "code": "scene_too_long",
                        "scene": scene.get("scene_id"),
                        "msg": f"scene duration {d:.2f}s > {limit:.0f}s max (J may use 7s)",
                    }
                )
        if len(durs) >= 5:
            avg = sum(durs) / len(durs)
            if avg > 4.0 + 1e-9:
                issues.append(
                    {
                        "level": "error",
                        "code": "avg_scene_too_long",
                        "msg": f"average scene {avg:.2f}s > 4.0s — cut denser for retention",
                    }
                )

        cta_ok = False
        if total_dur > 0:
            window_start = max(0.0, total_dur - 8.0)
            for scene in scenes:
                s0 = float(scene.get("start", 0))
                role = (scene.get("role") or "").strip().lower()
                pat = (scene.get("pattern") or "").strip().upper()
                in_window = s0 >= window_start - 1e-6
                if in_window and (role == "cta" or pat in ("J", "K")):
                    cta_ok = True
                    break
            # last scene fallback: must be J/K or role cta
            last = scenes[-1]
            last_pat = (last.get("pattern") or "").strip().upper()
            last_role = (last.get("role") or "").strip().lower()
            if last_role == "cta" or last_pat in ("J", "K"):
                cta_ok = True
            if not cta_ok:
                issues.append(
                    {
                        "level": "error",
                        "code": "missing_cta",
                        "msg": (
                            "need a CTA in the last 8s (role: cta and/or pattern J/K) "
                            "— follow / Part 2 / open loop"
                        ),
                    }
                )
            # prefer explicit role
            if cta_ok and not any((s.get("role") or "").strip().lower() == "cta" for s in scenes):
                issues.append(
                    {
                        "level": "warn",
                        "code": "cta_role_unmarked",
                        "msg": "mark the follow/Part-2 beat with role: \"cta\"",
                    }
                )

        packaging = sb.get("packaging") if isinstance(sb.get("packaging"), dict) else {}
        pkg_path = project / "analysis" / "packaging.json"
        if pkg_path.is_file():
            try:
                packaging = {**packaging, **(read_json(pkg_path) or {})}
            except Exception:
                pass
        if total_dur >= 30:
            if not (packaging.get("title") or "").strip():
                issues.append(
                    {
                        "level": "warn",
                        "code": "missing_packaging_title",
                        "msg": "set packaging.title (curiosity + specific — not textbook)",
                    }
                )
            if not (packaging.get("first_frame_note") or "").strip():
                issues.append(
                    {
                        "level": "warn",
                        "code": "missing_first_frame_note",
                        "msg": "set packaging.first_frame_note (giant number or sticker — almost no body text)",
                    }
                )

        ratio = text_only_count / len(scenes)
        if ratio > 0.20 + 1e-9:
            issues.append(
                {
                    "level": "error",
                    "code": "too_many_text_only",
                    "msg": f"{text_only_count}/{len(scenes)} scenes are text_only ({ratio:.0%}) - max 20%; use real images",
                }
            )
        if generated_without_asset:
            issues.append(
                {
                    "level": "error",
                    "code": "generated_graphic_without_image",
                    "msg": f"{generated_without_asset} generated_graphic scene(s) lack asset_path - inventing SVG is not enough",
                }
            )
        if missing_asset == len(scenes) - text_only_count and (len(scenes) - text_only_count) > 0:
            issues.append(
                {
                    "level": "error",
                    "code": "no_images_researched",
                    "msg": "no scenes have asset_path - run Step 7 asset research before compose",
                }
            )

    # Frame HTML must reference images once composed
    frames_dir = hf / "compositions" / "frames"
    if frames_dir.is_dir():
        frame_files = list(frames_dir.glob("*.html"))
        img_frames = 0
        timeline_frames = 0
        for ff in frame_files:
            text = ff.read_text(encoding="utf-8", errors="replace")
            if re.search(r"<img\b", text, re.I) or re.search(r"<video\b", text, re.I):
                img_frames += 1
            if "__timelines" in text:
                timeline_frames += 1
        if frame_files and img_frames < max(1, int(len(frame_files) * 0.7)):
            issues.append(
                {
                    "level": "error",
                    "code": "frames_missing_img",
                    "msg": f"only {img_frames}/{len(frame_files)} frame HTML files contain <img>/<video> - rebuild with real assets",
                }
            )
        if frame_files and timeline_frames < len(frame_files):
            issues.append(
                {
                    "level": "error",
                    "code": "frames_missing_timelines",
                    "msg": f"only {timeline_frames}/{len(frame_files)} frames register window.__timelines - fix GSAP registration",
                }
            )

    vo_dur = None
    if probe.get("voiceover") and probe["voiceover"].get("duration_s"):
        vo_dur = float(probe["voiceover"]["duration_s"])
    elif tr.get("audio_duration_secs"):
        vo_dur = float(tr["audio_duration_secs"])
    elif scenes:
        vo_dur = float(scenes[-1]["end"])

    if vo_dur is not None and scenes:
        last = float(scenes[-1]["end"])
        if abs(last - vo_dur) > args.tolerance:
            issues.append(
                {
                    "level": "warn",
                    "code": "duration_mismatch",
                    "msg": f"storyboard end {last:.2f}s vs VO {vo_dur:.2f}s (tol {args.tolerance})",
                }
            )

    if args.phase == "assets":
        # Skip compose/render-specific checks
        pass
    else:
        for rel in ("STORYBOARD.md", "SCRIPT.md", "frame.md", "audio_meta.json"):
            p = hf / rel
            if not p.is_file():
                issues.append({"level": "info", "code": "bridge_pending", "msg": f"missing {rel} (ok before handoff)"})

        if (hf / "audio_meta.json").is_file():
            meta = read_json(hf / "audio_meta.json")
            voices = meta.get("voices") or []
            if len(voices) != len(scenes) and scenes:
                issues.append(
                    {
                        "level": "error",
                        "code": "voice_count_mismatch",
                        "msg": f"audio_meta voices={len(voices)} scenes={len(scenes)}",
                    }
                )
            for v in voices:
                path = hf / v.get("path", "")
                if v.get("path") and not path.is_file():
                    issues.append({"level": "error", "code": "missing_voice_file", "msg": v.get("path")})
            sfx = meta.get("sfx") or []
            # Only hard-fail SFX once index exists (compose complete) or phase=pre_render
            if not sfx:
                level = "error" if (hf / "index.html").is_file() or args.phase == "pre_render" else "warn"
                issues.append(
                    {
                        "level": level,
                        "code": "missing_sfx",
                        "msg": "audio_meta.sfx empty — run faceless audio.mjs fetch-sfx before render",
                    }
                )
            else:
                bad_vol = [
                    c
                    for c in sfx
                    if isinstance(c, dict) and abs(float(c.get("volume", 0.35)) - 0.8) > 1e-6
                ]
                if bad_vol:
                    level = "error" if (hf / "index.html").is_file() or args.phase == "pre_render" else "warn"
                    issues.append(
                        {
                            "level": level,
                            "code": "sfx_volume_not_80",
                            "msg": (
                                f"{len(bad_vol)} SFX cue(s) not at volume 0.8 — "
                                "run set_sfx_volume.py --volume 0.8 then re-assemble"
                            ),
                        }
                    )

        cut_only = 0
        sfx_missing = 0
        for scene in scenes:
            t = (scene.get("transition") or "hard_cut").lower().replace("-", "_")
            if t in ("hard_cut", "cut", "hard", ""):
                cut_only += 1
            if not scene.get("sfx"):
                sfx_missing += 1
        if scenes and cut_only == len(scenes) and len(scenes) >= 3:
            issues.append(
                {
                    "level": "error",
                    "code": "all_hard_cuts",
                    "msg": "every scene is hard_cut — mix zoom-through/push-slide/crossfade (see motion-and-sfx.md)",
                }
            )
        if scenes and sfx_missing == len(scenes):
            issues.append(
                {
                    "level": "warn",
                    "code": "storyboard_sfx_empty",
                    "msg": "no scene.sfx in storyboard.json — bridge auto-fills STORYBOARD.md, but prefer explicit cues",
                }
            )

        story_md = hf / "STORYBOARD.md"
        if story_md.is_file():
            text = story_md.read_text(encoding="utf-8")
            if "- sfx:" not in text.lower():
                issues.append(
                    {
                        "level": "error",
                        "code": "storyboard_md_no_sfx",
                        "msg": "STORYBOARD.md has no sfx: lines — re-run storyboard_to_hyperframes.py",
                    }
                )
            non_cut_tokens = ("zoom-through", "push-slide", "crossfade", "blur-crossfade", "squeeze")
            if len(scenes) >= 3 and not any(tok in text for tok in non_cut_tokens):
                issues.append(
                    {
                        "level": "error",
                        "code": "storyboard_md_all_cuts",
                        "msg": "STORYBOARD.md has no non-cut transition_in — transitions.mjs will inject 0 effects",
                    }
                )

    errors = [i for i in issues if i["level"] == "error"]
    warns = [i for i in issues if i["level"] == "warn"]
    report = {
        "ok": len(errors) == 0,
        "phase": args.phase,
        "error_count": len(errors),
        "warn_count": len(warns),
        "scene_count": len(scenes),
        "text_only_count": text_only_count,
        "scenes_missing_asset_path": missing_asset,
        "voiceover_duration_s": vo_dur,
        "issues": issues,
    }
    out = project / "qa" / "report.json"
    write_json(out, report)

    print(f"QA {'PASS' if report['ok'] else 'FAIL'} - errors={len(errors)} warns={len(warns)} phase={args.phase}")
    for i in issues:
        if i["level"] in ("error", "warn"):
            scene = f" scene={i['scene']}" if "scene" in i else ""
            print(f"  [{i['level']}] {i['code']}{scene}: {i['msg']}")
    print(f"wrote {out}")
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

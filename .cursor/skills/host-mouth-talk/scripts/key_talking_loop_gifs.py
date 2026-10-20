#!/usr/bin/env python3
"""Chroma-key green out of host_talking_loop_gif/*.gif → host_talking/<id>/talking_loop.{webp,gif}.

Source green is ~BGR(5,254,5). Soft key keeps hair edges. shock is skipped (banned).
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import cv2
import numpy as np

WS = Path(__file__).resolve().parents[4]
SRC = WS / "greencode" / "my_animations" / "host_talking_loop_gif"
DST = WS / "greencode" / "my_animations" / "host_talking"
KEYED_SRC = SRC / "keyed"  # also leave transparent copies beside sources

# filename stem → catalog expression id
NAME_MAP = {
    "celebrate": "celebrate",
    "facepalm_lite": "facepalm_lite",
    "hang": "hang",
    "lean_in": "lean_in",
    "point_side": "point_side",
    "point_up": "point_up",
    "presenting": "present",
    "talk_emph": "talk_emph",
    "talk_loop": "talk_loop",
    "wave": "wave",
}
BANNED = {"shock"}


def soft_chroma_bgr(frame: np.ndarray) -> np.ndarray:
    """Return BGRA with green keyed out (soft)."""
    b, g, r = cv2.split(frame.astype(np.float32))
    # green dominance vs red/blue
    max_rb = np.maximum(r, b)
    greenness = (g - max_rb - 15.0) / 90.0
    greenness = np.clip(greenness, 0.0, 1.0)
    # also force pure-screen pixels fully transparent
    pure = (g > 200) & (r < 40) & (b < 40)
    greenness = np.where(pure, 1.0, greenness)
    alpha = ((1.0 - greenness) * 255.0).astype(np.uint8)
    # slight erode of alpha holes then blur for soft edge
    alpha_f = alpha.astype(np.float32) / 255.0
    alpha_f = cv2.GaussianBlur(alpha_f, (0, 0), 0.8)
    # zero RGB where fully transparent to avoid green fringe in bad players
    out = frame.copy()
    a3 = alpha_f[..., None]
    out = (out.astype(np.float32) * a3).astype(np.uint8)
    return np.dstack([out, (alpha_f * 255).astype(np.uint8)])


def read_gif_frames(path: Path) -> list[np.ndarray]:
    cap = cv2.VideoCapture(str(path))
    frames = []
    while True:
        ok, f = cap.read()
        if not ok:
            break
        frames.append(f)
    cap.release()
    return frames


def encode_dir(frames_bgra: list[np.ndarray], out_dir: Path, fps: float = 12.0) -> None:
    """Encode at 12fps so mouths play at calm 1x (96 frames ≈ 8s). Never time-stretch in compose."""
    out_dir.mkdir(parents=True, exist_ok=True)
    tmp = out_dir / "_key_frames"
    if tmp.exists():
        for p in tmp.glob("*"):
            p.unlink()
    else:
        tmp.mkdir()
    for i, fr in enumerate(frames_bgra):
        cv2.imwrite(str(tmp / f"f{i:03d}.png"), fr)
    pattern = str(tmp / "f%03d.png")
    webp = out_dir / "talking_loop.webp"
    gif = out_dir / "talking_loop.gif"
    # Explicit input rate + fps filter so GIF/WebP delays are not near-zero (speedy playback)
    fps_s = f"{fps:g}"
    subprocess.run(
        [
            "ffmpeg", "-y", "-framerate", fps_s, "-i", pattern,
            "-vf", f"fps={fps_s}",
            "-c:v", "libwebp", "-lossless", "0", "-q:v", "85",
            "-loop", "0", "-an", str(webp),
        ],
        check=True,
        capture_output=True,
    )
    subprocess.run(
        [
            "ffmpeg", "-y", "-framerate", fps_s, "-i", pattern,
            "-vf",
            f"fps={fps_s},split[a][b];[a]palettegen=reserve_transparent=1:max_colors=192[p];"
            "[b][p]paletteuse=dither=bayer:bayer_scale=3:alpha_threshold=48",
            "-loop", "0", str(gif),
        ],
        check=True,
        capture_output=True,
    )
    # cleanup temp frames
    for p in tmp.glob("*"):
        p.unlink()
    tmp.rmdir()


def process_one(gif_path: Path) -> str | None:
    stem = gif_path.name.replace("_talking_loop.gif", "")
    if stem in BANNED:
        print(f"skip banned: {stem}")
        return None
    expr = NAME_MAP.get(stem)
    if not expr:
        print(f"skip unmapped: {stem}")
        return None
    frames = read_gif_frames(gif_path)
    if not frames:
        print(f"empty: {gif_path.name}")
        return None
    keyed = [soft_chroma_bgr(f) for f in frames]
    out_dir = DST / expr
    encode_dir(keyed, out_dir)
    # also store keyed copies beside sources for reference
    import shutil

    KEYED_SRC.mkdir(parents=True, exist_ok=True)
    shutil.copy2(out_dir / "talking_loop.webp", KEYED_SRC / f"{expr}_talking_loop.webp")
    shutil.copy2(out_dir / "talking_loop.gif", KEYED_SRC / f"{expr}_talking_loop.gif")
    # alpha sanity
    sample = keyed[0]
    a = sample[:, :, 3]
    print(
        f"{expr}: {len(keyed)} frames {sample.shape[1]}x{sample.shape[0]} "
        f"alpha>0={(a > 8).mean()*100:.1f}% -> {out_dir}"
    )
    return expr


def main() -> int:
    gifs = sorted(SRC.glob("*_talking_loop.gif"))
    if not gifs:
        print(f"no gifs in {SRC}", file=sys.stderr)
        return 1
    done = []
    for g in gifs:
        e = process_one(g)
        if e:
            done.append(e)
    meta = {"sourced_from": str(SRC), "keyed_expressions": done, "banned_skipped": sorted(BANNED)}
    (DST / "_keyed_from_loop_gif.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    print(f"done {len(done)}: {', '.join(done)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Extract transparent mouth cutouts from host_talking frames for overlay use.

Writes greencode/my_animations/mouth_overlays/<id>/mouth_f%03d.png
plus talking_mouth.webp and talking_mouth.gif (soft-masked ROI).
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import cv2
import numpy as np

SKILL = Path(__file__).resolve().parents[1]
WS = Path(__file__).resolve().parents[4]
TALKING = WS / "greencode" / "my_animations" / "host_talking"
OUT = WS / "greencode" / "my_animations" / "mouth_overlays"
CALIB = SKILL / "calib"

PAD = 18
SOFT = 8


def load_calib(stem: str, w: int, h: int) -> dict | None:
    p = CALIB / f"{stem}.json"
    if not p.is_file():
        return None
    data = json.loads(p.read_text(encoding="utf-8"))
    ref = data.get("ref_size")
    if ref and (int(ref[0]) != w or int(ref[1]) != h):
        sx, sy = w / float(ref[0]), h / float(ref[1])
        poly = [[p[0] * sx, p[1] * sy] for p in data["poly"]]
        roi = data["roi"]
        roi = [roi[0] * sx, roi[1] * sx, roi[2] * sy, roi[3] * sy]
        return {
            "poly": poly,
            "anchor_y": float(data["anchor_y"]) * sy,
            "cx": float(data["cx"]) * sx,
            "roi": roi,
            "rotate": int(data.get("rotate", 0) or 0),
        }
    return {
        "poly": data["poly"],
        "anchor_y": float(data["anchor_y"]),
        "cx": float(data["cx"]),
        "roi": data["roi"],
        "rotate": int(data.get("rotate", 0) or 0),
    }


def soft_poly_alpha(h: int, w: int, poly: np.ndarray, soft: int = SOFT) -> np.ndarray:
    m = np.zeros((h, w), np.uint8)
    cv2.fillPoly(m, [poly.astype(np.int32)], 255)
    k = soft * 2 + 1
    m = cv2.GaussianBlur(m, (k, k), soft * 0.55)
    return m.astype(np.float32) / 255.0


def extract_one(stem: str) -> bool:
    frames_dir = TALKING / stem / "frames"
    if not frames_dir.is_dir():
        print(f"skip {stem}: no frames")
        return False
    paths = sorted(frames_dir.glob("f*.png"))
    if not paths:
        print(f"skip {stem}: empty frames")
        return False

    sample = cv2.imread(str(paths[0]), cv2.IMREAD_UNCHANGED)
    H, W = sample.shape[:2]
    cal = load_calib(stem, W, H)
    if not cal:
        print(f"skip {stem}: no calib")
        return False

    # Frames for hang are already rotated back to hang orientation;
    # calib coords are in upright (pre-rotate-back) space — invert ROI for hang.
    rotate = cal["rotate"]
    poly = np.array(cal["poly"], np.float32)
    x0, x1, y0, y1 = [int(round(v)) for v in cal["roi"]]
    ay, cx = cal["anchor_y"], cal["cx"]

    if rotate == 180:
        # Map upright calib → hung frame coords
        poly = np.stack([W - 1 - poly[:, 0], H - 1 - poly[:, 1]], axis=1)
        nx0, nx1 = W - 1 - x1, W - 1 - x0
        ny0, ny1 = H - 1 - y1, H - 1 - y0
        x0, x1, y0, y1 = nx0, nx1, ny0, ny1
        ay, cx = H - 1 - ay, W - 1 - cx

    # Expand crop for open mouth
    mouth_h = float(poly[:, 1].max() - poly[:, 1].min())
    y1 = min(H, int(y1 + mouth_h * 0.6 + PAD))
    y0 = max(0, int(min(y0, ay) - PAD))
    x0 = max(0, int(x0 - PAD))
    x1 = min(W, int(x1 + PAD))
    if x1 <= x0 or y1 <= y0:
        print(f"skip {stem}: bad roi")
        return False

    # Full-res soft alpha from poly (dilated in crop space)
    alpha_full = soft_poly_alpha(H, W, poly, soft=SOFT)
    # widen alpha a bit vertically below anchor for open frames
    yy = np.arange(H)[:, None]
    below = (yy >= ay).astype(np.float32)
    alpha_full = np.clip(alpha_full + below * cv2.dilate(
        (alpha_full > 0.05).astype(np.uint8),
        cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 15)),
    ).astype(np.float32) * 0.35, 0, 1)
    alpha_full = cv2.GaussianBlur(alpha_full, (0, 0), 1.2)

    out_dir = OUT / stem
    out_dir.mkdir(parents=True, exist_ok=True)
    # wipe old
    for old in out_dir.glob("mouth_f*.png"):
        old.unlink()

    cw, ch = x1 - x0, y1 - y0
    for i, path in enumerate(paths):
        img = cv2.imread(str(path), cv2.IMREAD_UNCHANGED)
        if img is None:
            continue
        if img.shape[2] == 4:
            bgr = img[:, :, :3]
            src_a = img[:, :, 3].astype(np.float32) / 255.0
        else:
            bgr = img
            src_a = np.ones((H, W), np.float32)

        crop = bgr[y0:y1, x0:x1]
        a = (alpha_full[y0:y1, x0:x1] * src_a[y0:y1, x0:x1] * 255.0).astype(np.uint8)
        # kill near-green chroma leftovers in crop (optional safety)
        g = crop.astype(np.int16)
        greenish = (g[:, :, 1] > g[:, :, 0] + 40) & (g[:, :, 1] > g[:, :, 2] + 40) & (g[:, :, 1] > 120)
        a = np.where(greenish, 0, a).astype(np.uint8)

        bgra = np.dstack([crop, a])
        cv2.imwrite(str(out_dir / f"mouth_f{i:03d}.png"), bgra)

    meta = {
        "stem": stem,
        "crop": [x0, y0, x1, y1],
        "size": [cw, ch],
        "anchor_in_crop": [cx - x0, ay - y0],
        "frames": len(paths),
        "source": str(frames_dir),
    }
    (out_dir / "meta.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")

    # Encode webp + gif with alpha
    pattern = str(out_dir / "mouth_f%03d.png")
    webp = out_dir / "talking_mouth.webp"
    gif = out_dir / "talking_mouth.gif"
    subprocess.run(
        [
            "ffmpeg", "-y", "-framerate", "24", "-i", pattern,
            "-c:v", "libwebp", "-lossless", "0", "-q:v", "80",
            "-loop", "0", "-an", str(webp),
        ],
        check=False,
        capture_output=True,
    )
    subprocess.run(
        [
            "ffmpeg", "-y", "-framerate", "24", "-i", pattern,
            "-vf", "split[a][b];[a]palettegen=reserve_transparent=1:max_colors=128[p];[b][p]paletteuse=dither=bayer:bayer_scale=3:alpha_threshold=64",
            "-loop", "0", str(gif),
        ],
        check=False,
        capture_output=True,
    )
    print(f"{stem}: {len(paths)} frames -> {out_dir} ({cw}x{ch})")
    return True


def main() -> int:
    ids = sys.argv[1:] or None
    OUT.mkdir(parents=True, exist_ok=True)
    stems = sorted(p.name for p in TALKING.iterdir() if p.is_dir())
    if ids:
        stems = [s for s in stems if s in ids]
    ok = 0
    for stem in stems:
        if extract_one(stem):
            ok += 1
    # also write a sheet of frame 0 mouths for quick pick
    print(f"done {ok}/{len(stems)} -> {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

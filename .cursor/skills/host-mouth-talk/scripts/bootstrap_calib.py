#!/usr/bin/env python3
"""Bootstrap mouth calib JSON for host stills via opaque-face bbox heuristics.

Claude's mouth poly is placed relative to an estimated mouth center inside the
opaque character bbox (anime-safe; no MediaPipe).
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import cv2
import numpy as np

# Local mouth outline relative to (cx, anchor_y) — from Claude's measured poly
# Original: CX=488, ANCHOR_Y=413 on ~1024 portrait
_LOCAL_POLY = np.array(
    [
        (-45, 7),
        (-36, 3),
        (-22, 1),
        (2, -1),
        (32, -1),
        (46, -1),
        (41, 9),
        (32, 17),
        (24, 21),
        (0, 25),
        (-22, 22),
        (-38, 15),
    ],
    np.float64,
)

# Scale of Claude poly was for mouth ~90px wide on 1024 image
_REF_MOUTH_W = 90.0


def opaque_bbox(alpha: np.ndarray, thresh: int = 40) -> tuple[int, int, int, int]:
    ys, xs = np.where(alpha > thresh)
    if len(xs) == 0:
        h, w = alpha.shape
        return 0, 0, w, h
    return int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1


def estimate_mouth_center(alpha: np.ndarray, bgr: np.ndarray) -> tuple[float, float, float]:
    """Return cx, anchor_y, mouth_scale (vs Claude ref)."""
    x0, y0, x1, y1 = opaque_bbox(alpha)
    bw, bh = max(1, x1 - x0), max(1, y1 - y0)
    # Face is upper ~55% of character bbox for bust shots
    face_h = bh * 0.55
    face_top = y0
    # Mouth ~ 62% down the face region (below nose)
    cy = face_top + face_h * 0.62
    cx = x0 + bw * 0.50
    mouth_w = bw * 0.22  # typical mouth width vs bust width
    scale = float(np.clip(mouth_w / _REF_MOUTH_W, 0.35, 2.5))
    return float(cx), float(cy), scale


def make_calib(path: Path) -> dict:
    raw = cv2.imread(str(path), cv2.IMREAD_UNCHANGED)
    if raw is None:
        raise SystemExit(f"cannot read {path}")
    if raw.ndim == 2:
        bgr = cv2.cvtColor(raw, cv2.COLOR_GRAY2BGR)
        alpha = np.full(bgr.shape[:2], 255, np.uint8)
    elif raw.shape[2] == 4:
        bgr = raw[:, :, :3]
        alpha = raw[:, :, 3]
    else:
        bgr = raw
        alpha = np.full(bgr.shape[:2], 255, np.uint8)

    h, w = bgr.shape[:2]
    cx, ay, scale = estimate_mouth_center(alpha, bgr)
    poly = [[float(cx + dx * scale), float(ay + dy * scale)] for dx, dy in _LOCAL_POLY]

    # Skin sample just above mouth (upper lip / cheek)
    sw = 28 * scale
    sh = 6 * scale
    skin = [ay - 18 * scale, ay - 18 * scale + sh, cx - sw, cx - sw + sw * 1.8]
    # Fill/search box around mouth
    box = [ay - 40 * scale, ay + 55 * scale, cx - 80 * scale, cx + 80 * scale]
    # Remap ROI
    roi = [cx - 75 * scale, cx + 75 * scale, ay - 30 * scale, ay + 55 * scale]

    def clamp_box_yxyx(b):
        y0, y1, x0, x1 = b
        return [
            float(np.clip(y0, 0, h - 1)),
            float(np.clip(y1, 1, h)),
            float(np.clip(x0, 0, w - 1)),
            float(np.clip(x1, 1, w)),
        ]

    def clamp_roi(r):
        x0, x1, y0, y1 = r
        return [
            float(np.clip(x0, 0, w - 1)),
            float(np.clip(x1, 1, w)),
            float(np.clip(y0, 0, h - 1)),
            float(np.clip(y1, 1, h)),
        ]

    return {
        "poly": poly,
        "anchor_y": ay,
        "cx": cx,
        "skin_sample": clamp_box_yxyx(skin),
        "box": clamp_box_yxyx(box),
        "roi": clamp_roi(roi),
        "ref_size": [w, h],
        "source": str(path).replace("\\", "/"),
        "bootstrap": {"cx": cx, "anchor_y": ay, "scale": scale},
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--stills-dir",
        type=Path,
        default=None,
        help="Default: <workspace>/greencode/my_animations/host_stills",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=None,
        help="Default: skill calib/",
    )
    parser.add_argument("--ids", nargs="*", help="Optional subset of expression ids")
    args = parser.parse_args()

    skill_root = Path(__file__).resolve().parents[1]
    workspace = Path(__file__).resolve().parents[4]
    stills = args.stills_dir or (workspace / "greencode" / "my_animations" / "host_stills")
    out = args.out_dir or (skill_root / "calib")
    out.mkdir(parents=True, exist_ok=True)

    banned = {"shock"}
    files = sorted(stills.glob("*.png"))
    for f in files:
        if f.stem in banned:
            continue
        if args.ids and f.stem not in args.ids:
            continue
        calib = make_calib(f)
        dest = out / f"{f.stem}.json"
        dest.write_text(json.dumps(calib, indent=2) + "\n", encoding="utf-8")
        print(f"wrote {dest.name}  cx={calib['cx']:.1f} ay={calib['anchor_y']:.1f} size={calib['ref_size']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

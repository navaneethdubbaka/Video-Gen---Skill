#!/usr/bin/env python3
"""Audit and auto-fix skin_sample boxes onto opaque cheek pixels near the mouth."""

from __future__ import annotations

import json
from pathlib import Path

import cv2
import numpy as np

SKILL = Path(__file__).resolve().parents[1]
WS = Path(__file__).resolve().parents[4]
STILLS = WS / "greencode" / "my_animations" / "host_stills"
CALIB = SKILL / "calib"


def load(path: Path, rot: int = 0):
    raw = cv2.imread(str(path), cv2.IMREAD_UNCHANGED)
    if rot == 180:
        raw = cv2.rotate(raw, cv2.ROTATE_180)
    if raw.shape[2] == 4:
        return raw[:, :, :3], raw[:, :, 3]
    return raw[:, :, :3], np.full(raw.shape[:2], 255, np.uint8)


def find_cheek(bgr: np.ndarray, alpha: np.ndarray, cx: float, ay: float) -> list[float]:
    """Pick a small opaque tan patch to the viewer's-right of the mouth (character left cheek)."""
    H, W = bgr.shape[:2]
    lab = cv2.cvtColor(bgr, cv2.COLOR_BGR2LAB).astype(np.float32)
    best = None
    best_score = -1.0
    # search offsets: right cheek (higher x), a bit below nose / beside mouth
    for dy in range(-8, 28, 2):
        for dx in range(28, 90, 2):
            y0 = int(ay + dy)
            x0 = int(cx + dx)
            y1, x1 = y0 + 10, x0 + 14
            if y0 < 0 or x0 < 0 or y1 > H or x1 > W:
                continue
            a = alpha[y0:y1, x0:x1]
            if a.mean() < 240:
                continue
            patch = bgr[y0:y1, x0:x1].reshape(-1, 3).astype(np.float32)
            med = np.median(patch, axis=0)
            # prefer mid-brightness tan (not green fringe, not dark stubble)
            L = float(np.median(lab[y0:y1, x0:x1, 0]))
            if L < 70 or L > 200:
                continue
            # reject green-ish (chroma key fringe)
            if med[1] > med[2] + 25 and med[1] > med[0] + 15:
                continue
            score = L - abs(med[0] - med[2]) * 0.2
            if score > best_score:
                best_score = score
                best = [float(y0), float(y1), float(x0), float(x1)]
    # also try left cheek
    for dy in range(-8, 28, 2):
        for dx in range(-90, -28, 2):
            y0 = int(ay + dy)
            x0 = int(cx + dx)
            y1, x1 = y0 + 10, x0 + 14
            if y0 < 0 or x0 < 0 or y1 > H or x1 > W:
                continue
            a = alpha[y0:y1, x0:x1]
            if a.mean() < 240:
                continue
            patch = bgr[y0:y1, x0:x1].reshape(-1, 3).astype(np.float32)
            med = np.median(patch, axis=0)
            L = float(np.median(lab[y0:y1, x0:x1, 0]))
            if L < 70 or L > 200:
                continue
            if med[1] > med[2] + 25 and med[1] > med[0] + 15:
                continue
            score = L - abs(med[0] - med[2]) * 0.2
            if score > best_score:
                best_score = score
                best = [float(y0), float(y1), float(x0), float(x1)]
    if best is None:
        # fallback tiny box near cx
        y0 = int(ay + 8)
        x0 = int(cx + 40)
        best = [float(y0), float(y0 + 10), float(x0), float(x0 + 14)]
    return best


def main() -> None:
    for p in sorted(CALIB.glob("*.json")):
        if p.name.startswith("_"):
            continue
        d = json.loads(p.read_text(encoding="utf-8"))
        rot = int(d.get("rotate", 0) or 0)
        bgr, alpha = load(STILLS / f"{p.stem}.png", rot)
        sy0, sy1, sx0, sx1 = [int(v) for v in d["skin_sample"]]
        H, W = bgr.shape[:2]
        sy0, sy1 = max(0, sy0), min(H, max(sy0 + 1, sy1))
        sx0, sx1 = max(0, sx0), min(W, max(sx0 + 1, sx1))
        patch = bgr[sy0:sy1, sx0:sx1]
        ap = alpha[sy0:sy1, sx0:sx1]
        med = patch.reshape(-1, 3).mean(0) if patch.size else np.zeros(3)
        amean = float(ap.mean()) if ap.size else 0.0
        bad = amean < 200 or float(med.mean()) < 40
        if bad:
            new = find_cheek(bgr, alpha, float(d["cx"]), float(d["anchor_y"]))
            d["skin_sample"] = [round(v, 2) for v in new]
            p.write_text(json.dumps(d, indent=2) + "\n", encoding="utf-8")
            ny0, ny1, nx0, nx1 = [int(v) for v in new]
            nmed = bgr[ny0:ny1, nx0:nx1].reshape(-1, 3).mean(0)
            print(f"{p.stem}: FIXED {sx0},{sy0} -> {nx0},{ny0} med={nmed.round(1)}")
        else:
            print(f"{p.stem}: ok med={med.round(1)} a={amean:.0f}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Per-expression mouth measure helpers: crop5x, poly overlay, animate, contact sheet."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

import cv2
import numpy as np

SKILL = Path(__file__).resolve().parents[1]
WS = Path(__file__).resolve().parents[4]
STILLS = WS / "greencode" / "my_animations" / "host_stills"
TALKING = WS / "greencode" / "my_animations" / "host_talking"
CALIB = SKILL / "calib"
QA = SKILL / "qa_crops"
ANIMATE = SKILL / "scripts" / "animate_mouth.py"


def composite(path: Path) -> np.ndarray:
    img = cv2.imread(str(path), cv2.IMREAD_UNCHANGED)
    if img is None:
        raise SystemExit(f"missing {path}")
    if img.ndim == 2:
        return cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    if img.shape[2] == 4:
        a = img[:, :, 3:4].astype(np.float32) / 255.0
        bgr = img[:, :, :3].astype(np.float32)
        bg = np.full_like(bgr, 60)
        return (bgr * a + bg * (1 - a)).astype(np.uint8)
    return img[:, :, :3].copy()


def make_crop(stem: str, x0: int, y0: int, x1: int, y1: int) -> Path:
    QA.mkdir(parents=True, exist_ok=True)
    comp = composite(STILLS / f"{stem}.png")
    h, w = comp.shape[:2]
    x0, y0 = max(0, x0), max(0, y0)
    x1, y1 = min(w, x1), min(h, y1)
    crop = comp[y0:y1, x0:x1]
    zoom = cv2.resize(crop, None, fx=5, fy=5, interpolation=cv2.INTER_CUBIC)
    out = QA / f"{stem}_crop5x.png"
    cv2.imwrite(str(out), zoom)
    meta = {"origin": [x0, y0], "window": [x0, y0, x1, y1], "size": [w, h], "zoom": 5}
    (QA / f"{stem}_meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    # grid helper for measuring zoomed pixels
    g = zoom.copy()
    step = 50
    for x in range(0, g.shape[1], step):
        cv2.line(g, (x, 0), (x, g.shape[0] - 1), (80, 80, 80), 1)
        cv2.putText(g, str(x), (x + 2, 14), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 255), 1)
    for y in range(0, g.shape[0], step):
        cv2.line(g, (0, y), (g.shape[1] - 1, y), (80, 80, 80), 1)
        cv2.putText(g, str(y), (2, y + 14), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 255), 1)
    cv2.imwrite(str(QA / f"{stem}_crop5x_grid.png"), g)
    print(f"{stem} crop origin=({x0},{y0}) size={x1-x0}x{y1-y0} -> {out}")
    return out


def zoomed_to_full(origin, zx, zy, zoom=5):
    return origin[0] + zx / zoom, origin[1] + zy / zoom


def write_calib(stem: str, calib: dict) -> Path:
    CALIB.mkdir(parents=True, exist_ok=True)
    path = CALIB / f"{stem}.json"
    path.write_text(json.dumps(calib, indent=2) + "\n", encoding="utf-8")
    # overlay
    comp = composite(STILLS / f"{stem}.png")
    poly = np.array(calib["poly"], np.int32)
    cv2.polylines(comp, [poly], True, (0, 255, 0), 2)
    cx, ay = int(round(calib["cx"])), int(round(calib["anchor_y"]))
    cv2.drawMarker(comp, (cx, ay), (0, 0, 255), cv2.MARKER_CROSS, 16, 2)
    x0, x1, y0, y1 = [int(round(v)) for v in calib["roi"]]
    cv2.rectangle(comp, (x0, y0), (x1, y1), (255, 128, 0), 1)
    sy0, sy1, sx0, sx1 = [int(round(v)) for v in calib["skin_sample"]]
    cv2.rectangle(comp, (sx0, sy0), (sx1, sy1), (255, 0, 255), 1)
    cv2.imwrite(str(QA / f"{stem}_poly.png"), comp)
    print("wrote", path)
    return path


def animate(stem: str) -> None:
    out = TALKING / stem
    out.mkdir(parents=True, exist_ok=True)
    subprocess.check_call(
        [
            sys.executable,
            str(ANIMATE),
            str(STILLS / f"{stem}.png"),
            str(out),
            "--calib",
            str(CALIB / f"{stem}.json"),
        ]
    )


def contact_sheet(stem: str) -> Path:
    d = TALKING / stem
    cal = json.loads((CALIB / f"{stem}.json").read_text(encoding="utf-8"))
    v = np.loadtxt(d / "openness.txt")
    idx = [int(np.argmin(v)), int(np.argmax(v)), 8, 24, 48, 72]
    x0, x1, y0, y1 = [int(round(v)) for v in cal["roi"]]
    # hang frames are rotated back — if rotate set, use full face mid crop instead
    rotate = int(cal.get("rotate", 0) or 0)
    tiles = []
    for i in idx:
        f = cv2.imread(str(d / "frames" / f"f{i:03d}.png"), cv2.IMREAD_UNCHANGED)
        if f.shape[2] == 4:
            a = f[:, :, 3:4].astype(np.float32) / 255.0
            bgr = f[:, :, :3].astype(np.float32)
            f = (bgr * a + 40 * (1 - a)).astype(np.uint8)
        else:
            f = f[:, :, :3]
        if rotate == 180:
            # approx mouth in upside-down frame: invert roi
            H, W = f.shape[:2]
            xx0, xx1 = W - x1, W - x0
            yy0, yy1 = H - y1, H - y0
            crop = f[max(0, yy0 - 8) : min(H, yy1 + 8), max(0, xx0 - 8) : min(W, xx1 + 8)]
        else:
            crop = f[max(0, y0 - 8) : min(f.shape[0], y1 + 8), max(0, x0 - 8) : min(f.shape[1], x1 + 8)]
        z = cv2.resize(crop, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
        cv2.putText(z, f"{i} s={v[i]:.2f}", (6, 22), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 0), 2)
        tiles.append(z)
    mh = max(t.shape[0] for t in tiles)
    mw = max(t.shape[1] for t in tiles)

    def pad(t):
        p = np.full((mh, mw, 3), 30, np.uint8)
        p[: t.shape[0], : t.shape[1]] = t
        return p

    tiles = [pad(t) for t in tiles]
    sheet = np.vstack([np.hstack(tiles[:3]), np.hstack(tiles[3:])])
    out = QA / f"{stem}_sheet.png"
    cv2.imwrite(str(out), sheet)
    print("sheet", out)
    return out


def encode(stem: str) -> None:
    ps1 = SKILL / "scripts" / "encode_loops.ps1"
    subprocess.check_call(
        [
            "powershell",
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            str(ps1),
            "-OutDir",
            str(TALKING / stem),
        ]
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("crop")
    c.add_argument("stem")
    c.add_argument("x0", type=int)
    c.add_argument("y0", type=int)
    c.add_argument("x1", type=int)
    c.add_argument("y1", type=int)

    a = sub.add_parser("animate")
    a.add_argument("stem")
    a.add_argument("--encode", action="store_true")

    s = sub.add_parser("sheet")
    s.add_argument("stem")

    args = ap.parse_args()
    if args.cmd == "crop":
        make_crop(args.stem, args.x0, args.y0, args.x1, args.y1)
    elif args.cmd == "animate":
        animate(args.stem)
        contact_sheet(args.stem)
        if args.encode:
            encode(args.stem)
    elif args.cmd == "sheet":
        contact_sheet(args.stem)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

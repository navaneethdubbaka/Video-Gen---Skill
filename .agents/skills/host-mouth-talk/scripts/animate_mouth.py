#!/usr/bin/env python3
"""Mouth-only talking loop for a single illustrated portrait.

usage: python animate_mouth.py <input_image> <output_dir> --calib <calib.json>
Writes frames/ (PNG with alpha) and openness.txt into output_dir.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

import cv2
import numpy as np


def load_rgba(path: str, rotate: int = 0) -> tuple[np.ndarray, np.ndarray | None]:
    """Return BGR uint8 + optional alpha float32 0..1 (or None)."""
    raw = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    if raw is None:
        raise SystemExit(f"cannot read image: {path}")
    if rotate == 180:
        raw = cv2.rotate(raw, cv2.ROTATE_180)
    elif rotate == 90:
        raw = cv2.rotate(raw, cv2.ROTATE_90_CLOCKWISE)
    elif rotate == 270:
        raw = cv2.rotate(raw, cv2.ROTATE_90_COUNTERCLOCKWISE)
    if raw.ndim == 2:
        bgr = cv2.cvtColor(raw, cv2.COLOR_GRAY2BGR)
        return bgr, None
    if raw.shape[2] == 4:
        bgr = raw[:, :, :3].copy()
        alpha = raw[:, :, 3].astype(np.float32) / 255.0
        return bgr, alpha
    return raw.copy(), None


def load_calib(path: Path, w: int, h: int) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    ref = data.get("ref_size")
    if ref and (int(ref[0]) != w or int(ref[1]) != h):
        sx = w / float(ref[0])
        sy = h / float(ref[1])

        def scale_xy(pts):
            return [[p[0] * sx, p[1] * sy] for p in pts]

        def scale_box(b):
            # [y0, y1, x0, x1] or [x0, x1, y0, y1] — we use y0,y1,x0,x1 for skin/box; roi is x0,x1,y0,y1
            return b

        # Explicit fields — scale appropriately
        poly = [[p[0] * sx, p[1] * sy] for p in data["poly"]]
        skin = data["skin_sample"]  # y0,y1,x0,x1
        skin = [skin[0] * sy, skin[1] * sy, skin[2] * sx, skin[3] * sx]
        box = data["box"]  # y0,y1,x0,x1
        box = [box[0] * sy, box[1] * sy, box[2] * sx, box[3] * sx]
        roi = data["roi"]  # x0,x1,y0,y1
        roi = [roi[0] * sx, roi[1] * sx, roi[2] * sy, roi[3] * sy]
        out = {
            "poly": poly,
            "anchor_y": float(data["anchor_y"]) * sy,
            "cx": float(data["cx"]) * sx,
            "skin_sample": skin,
            "box": box,
            "roi": roi,
        }
        for k in (
            "dilate_sprite",
            "dilate_fill",
            "s_max",
            "alpha_blur",
            "fill_blur",
            "lab_tol",
            "closed_source",
            "chin_y",
            "notes",
        ):
            if k in data:
                out[k] = data[k]
        return out

    out = {
        "poly": data["poly"],
        "anchor_y": float(data["anchor_y"]),
        "cx": float(data["cx"]),
        "skin_sample": data["skin_sample"],
        "box": data["box"],
        "roi": data["roi"],
    }
    for k in (
        "dilate_sprite",
        "dilate_fill",
        "s_max",
        "alpha_blur",
        "fill_blur",
        "lab_tol",
        "closed_source",
        "chin_y",
        "notes",
    ):
        if k in data:
            out[k] = data[k]
    return out


def _paint_open_mouth(img: np.ndarray, poly: np.ndarray, ay: float, cx: float) -> np.ndarray:
    """Draw a simple open-mouth interior (teeth + dark cavity) for closed-source portraits."""
    out = img.copy()
    xs = poly[:, 0]
    ys = poly[:, 1]
    x0, x1 = int(xs.min()), int(xs.max())
    # open height ~ 0.55 of mouth width
    mw = max(8, x1 - x0)
    open_h = int(mw * 0.45)
    y_top = int(round(ay))
    y_bot = y_top + open_h
    # outer lip dark
    cv2.ellipse(out, (int(cx), (y_top + y_bot) // 2), (mw // 2, open_h // 2), 0, 0, 360, (40, 30, 25), -1)
    # teeth strip
    teeth_y1 = y_top + max(3, open_h // 4)
    cv2.rectangle(out, (x0 + 3, y_top + 1), (x1 - 3, teeth_y1), (235, 235, 235), -1)
    # tongue hint
    cv2.ellipse(
        out,
        (int(cx), y_bot - open_h // 5),
        (mw // 3, open_h // 5),
        0,
        0,
        360,
        (90, 90, 180),
        -1,
    )
    # dark outline
    cv2.ellipse(out, (int(cx), (y_top + y_bot) // 2), (mw // 2, open_h // 2), 0, 0, 360, (20, 15, 12), 2)
    return out


def build_base(
    img: np.ndarray, calib: dict, s_max: float
) -> tuple[np.ndarray, np.ndarray, np.ndarray, tuple[float, float, int, int, int, int]]:
    H, W = img.shape[:2]
    poly = np.array(calib["poly"], np.int32)
    ANCHOR_Y = float(calib["anchor_y"])
    CX = float(calib["cx"])

    # Sprite: tight (mustache stays out). Fill: generous (full erase → no ghost outline).
    dil_sprite = int(calib.get("dilate_sprite", 1))
    dil_fill = int(calib.get("dilate_fill", 11))
    dil_sprite = max(1, dil_sprite)
    dil_sprite = dil_sprite if dil_sprite % 2 else dil_sprite + 1
    dil_fill = dil_fill if dil_fill % 2 else dil_fill + 1
    blur_a = float(calib.get("alpha_blur", 0.6))
    blur_f = float(calib.get("fill_blur", 1.2))
    lab_tol = float(calib.get("lab_tol", 12))

    m_sprite = np.zeros((H, W), np.uint8)
    cv2.fillPoly(m_sprite, [poly], 255)
    m_sprite = cv2.dilate(m_sprite, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (dil_sprite, dil_sprite)))
    # Hard clip: never warp anything at/above the top-lip anchor (protects mustache)
    yy_all = np.arange(H, dtype=np.float32)[:, None]
    m_sprite = np.where(yy_all < ANCHOR_Y, 0, m_sprite).astype(np.uint8)
    alpha_m = cv2.GaussianBlur(m_sprite.astype(np.float32) / 255.0, (0, 0), blur_a)
    # Re-zero after blur so soft edge cannot pull mustache pixels
    alpha_m = np.where(yy_all < ANCHOR_Y, 0.0, alpha_m).astype(np.float32)

    m_fill = np.zeros((H, W), np.uint8)
    cv2.fillPoly(m_fill, [poly], 255)
    m_fill = cv2.dilate(m_fill, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (dil_fill, dil_fill)))

    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB).astype(np.float32)
    sy0, sy1, sx0, sx1 = [int(round(v)) for v in calib["skin_sample"]]
    sy0, sy1 = max(0, sy0), min(H, max(sy0 + 1, sy1))
    sx0, sx1 = max(0, sx0), min(W, max(sx0 + 1, sx1))
    patch = lab[sy0:sy1, sx0:sx1].reshape(-1, 3)
    if patch.size == 0:
        med = np.array([128.0, 128.0, 128.0], np.float32)
    else:
        med = np.median(patch, axis=0)
    dist = np.linalg.norm(lab - med, axis=2)
    # Reject dark outlines / hair / beard from skin support (L channel too low)
    L = lab[:, :, 0]
    not_dark = L > (float(med[0]) - 18.0)
    skin = ((dist < lab_tol) & (m_sprite == 0) & not_dark).astype(np.float32)
    by0, by1, bx0, bx1 = [int(round(v)) for v in calib["box"]]
    box = np.zeros((H, W), np.float32)
    box[max(0, by0) : min(H, by1), max(0, bx0) : min(W, bx1)] = 1.0
    skin *= box

    imgf = img.astype(np.float32)
    med_bgr = np.median(img[sy0:sy1, sx0:sx1].reshape(-1, 3), axis=0).astype(np.float32)
    if float(med_bgr.mean()) < 30:
        # skin sample landed on void/fringe — fall back to opaque pixels near CX,AY
        yy0 = max(0, int(ANCHOR_Y) + 6)
        xx0 = min(W - 16, int(CX) + 36)
        med_bgr = np.median(img[yy0 : yy0 + 12, xx0 : xx0 + 16].reshape(-1, 3), axis=0).astype(np.float32)
        if float(med_bgr.mean()) < 30:
            med_bgr = np.array([90.0, 130.0, 170.0], np.float32)  # tan fallback BGR
    num = np.stack([cv2.GaussianBlur(imgf[..., c] * skin, (0, 0), 7) for c in range(3)], -1)
    den = cv2.GaussianBlur(skin, (0, 0), 7)[..., None]
    num2 = np.stack([cv2.GaussianBlur(imgf[..., c] * skin, (0, 0), 18) for c in range(3)], -1)
    den2 = cv2.GaussianBlur(skin, (0, 0), 18)[..., None]
    fill = np.where(den > 0.05, num / np.maximum(den, 1e-4), num2 / np.maximum(den2, 1e-4))
    # Prefer solid cheek median wherever fill support is weak OR pixel is dark (outline bleed)
    weak = ((den[..., 0] < 0.05) | (fill.mean(axis=2) < med_bgr.mean() * 0.55)) & (m_fill > 0)
    for c in range(3):
        fill[..., c] = np.where(weak, med_bgr[c], fill[..., c])
    fa = cv2.GaussianBlur(m_fill.astype(np.float32) / 255.0, (0, 0), blur_f)[..., None]
    # Harder core fill: full replace where fill mask is strong
    fa = np.maximum(fa, (m_fill.astype(np.float32) / 255.0)[..., None] * 0.92)
    base = np.clip(imgf * (1 - fa) + fill * fa, 0, 255).astype(np.uint8)

    sprite_img = img
    if calib.get("closed_source"):
        sprite_img = _paint_open_mouth(img, poly, ANCHOR_Y, CX)

    # ROI must fit widest mouth (s_max)
    mouth_bottom = float(poly[:, 1].max())
    need_y1 = int(np.ceil(ANCHOR_Y + (mouth_bottom - ANCHOR_Y) * s_max + 18))
    x0, x1, y0, y1 = [int(round(v)) for v in calib["roi"]]
    y1 = max(y1, need_y1)
    x0 = min(x0, int(poly[:, 0].min()) - 12)
    x1 = max(x1, int(poly[:, 0].max()) + 12)
    y0 = min(y0, int(ANCHOR_Y) - 12)
    x0, x1 = max(0, x0), min(W, max(x0 + 1, x1))
    y0, y1 = max(0, y0), min(H, max(y0 + 1, y1))
    return base, alpha_m, sprite_img, (ANCHOR_Y, CX, x0, x1, y0, y1)


def openness_curve(n: int = 96, seed: int = 7) -> np.ndarray:
    rng = np.random.default_rng(seed)
    keys_t, keys_v = [0.0], [0.28]
    t = 0.0
    openn = True
    while t < n - 6:
        t += rng.integers(3, 6)
        if openn:
            keys_v.append(float(rng.choice([0.8, 1.0, 1.15, 1.3])))
        else:
            keys_v.append(float(rng.choice([0.25, 0.35, 0.5])))
        keys_t.append(float(t))
        openn = not openn
    keys_t.append(float(n))
    keys_v.append(0.28)

    tt = np.arange(n, dtype=np.float64)
    vals = np.empty(n)
    for i, ti in enumerate(tt):
        k = np.searchsorted(keys_t, ti, side="right") - 1
        k = min(k, len(keys_t) - 2)
        u = (ti - keys_t[k]) / (keys_t[k + 1] - keys_t[k])
        u = 0.5 - 0.5 * np.cos(np.pi * u)
        vals[i] = keys_v[k] * (1 - u) + keys_v[k + 1] * u
    return vals


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("src")
    parser.add_argument("outdir")
    parser.add_argument("--calib", required=True, type=Path, help="Calib JSON with mouth geometry")
    parser.add_argument("--fps", type=int, default=24)
    parser.add_argument("--frames", type=int, default=96)
    parser.add_argument("--seed", type=int, default=7)
    args = parser.parse_args()

    frames_dir = os.path.join(args.outdir, "frames")
    os.makedirs(frames_dir, exist_ok=True)

    # Peek calib for rotate before load (uses raw file size; rotate applied in load_rgba)
    raw_calib = json.loads(Path(args.calib).read_text(encoding="utf-8"))
    rotate = int(raw_calib.get("rotate", 0) or 0)
    s_max = float(raw_calib.get("s_max", 1.3))

    img, src_alpha = load_rgba(args.src, rotate=rotate)
    H, W = img.shape[:2]
    calib = load_calib(args.calib, W, H)

    # Cap s_max against chin if provided
    chin_y = float(calib.get("chin_y") or 0) or None
    if chin_y is not None:
        poly = np.array(calib["poly"], np.float64)
        mouth_bottom = float(poly[:, 1].max())
        ay = float(calib["anchor_y"])
        if mouth_bottom > ay:
            s_cap = (chin_y - 4 - ay) / (mouth_bottom - ay)
            s_max = min(s_max, max(0.9, float(s_cap)))

    base, alpha_m, sprite_img, geom = build_base(img, calib, s_max)
    ANCHOR_Y, CX, X0, X1, Y0, Y1 = geom
    yy, xx = np.mgrid[Y0:Y1, X0:X1].astype(np.float32)
    spr_bgr = sprite_img[Y0:Y1, X0:X1]
    spr_a = alpha_m[Y0:Y1, X0:X1]

    def mouth_frame(s: float) -> np.ndarray:
        s = float(np.clip(s, 0.2, s_max))
        w = float(np.clip(1.0 - 0.10 * (s - 0.9), 0.9, 1.06))
        map_x = (CX + (xx - CX) / w) - X0
        # Clamp source Y so we never sample mustache/nose above the top lip
        src_y_img = ANCHOR_Y + (yy - ANCHOR_Y) / s
        src_y_img = np.maximum(src_y_img, ANCHOR_Y)
        map_y = src_y_img - Y0
        bgr = cv2.remap(spr_bgr, map_x, map_y, cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        a = cv2.remap(spr_a, map_x, map_y, cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=0)
        a = np.clip(a, 0, 1)
        # When closing, shrink alpha so compressed dark lip doesn't leave a thick ghost band
        if s < 0.85:
            shrink = 0.55 + 0.45 * ((s - 0.2) / 0.65)
            a = a * float(np.clip(shrink, 0.45, 1.0))
            # soft gate: drop very weak alpha that is just smear
            a = np.where(a < 0.12, 0.0, a)
        a = a[..., None]
        out = base.copy()
        roi_px = out[Y0:Y1, X0:X1].astype(np.float32)
        out[Y0:Y1, X0:X1] = np.clip(roi_px * (1 - a) + bgr.astype(np.float32) * a, 0, 255).astype(np.uint8)
        return out

    vals = openness_curve(args.frames, args.seed)
    vals = np.clip(vals, 0.2, s_max)
    # keep loop seam at closed-ish value
    vals[0] = vals[-1] = min(0.28, s_max)

    for i, s in enumerate(vals):
        bgr = mouth_frame(float(s))
        if rotate == 180:
            bgr = cv2.rotate(bgr, cv2.ROTATE_180)
            if src_alpha is not None:
                a_out = cv2.rotate((src_alpha * 255.0).astype(np.uint8), cv2.ROTATE_180)
            else:
                a_out = None
        else:
            a_out = (src_alpha * 255.0).astype(np.uint8) if src_alpha is not None else None

        if a_out is not None:
            bgra = np.dstack([bgr[:, :, 0], bgr[:, :, 1], bgr[:, :, 2], a_out])
            cv2.imwrite(os.path.join(frames_dir, f"f{i:03d}.png"), bgra)
        else:
            cv2.imwrite(os.path.join(frames_dir, f"f{i:03d}.png"), bgr)

    np.savetxt(os.path.join(args.outdir, "openness.txt"), vals, fmt="%.3f")
    print(
        "frames:",
        args.frames,
        "fps:",
        args.fps,
        "openness range:",
        float(vals.min().round(2)),
        float(vals.max().round(2)),
        "size:",
        f"{W}x{H}",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

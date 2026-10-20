#!/usr/bin/env python3
"""Chroma-key JPGs from my_animations/new into transparent host_stills PNGs."""

from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT / "new"
OUT_DIR = ROOT / "host_stills"
AUDIT_DIR = ROOT / "host_stills_audit"

SRC_MAP = {
    "image.png_20261015155526.jpg": "wave",
    "image.png_20261015155942.jpg": "cross_arms",
    "image.png_20261015160106.jpg": "thumbs_up",
    "image.png_20261015160311.jpg": "lean_in",
    "image.png_20261015160622.jpg": "present",
    "image.png_20261015160935.jpg": "facepalm_lite",
}


def key_green(im: Image.Image) -> Image.Image:
    arr = np.asarray(im.convert("RGBA")).astype(np.float32)
    r, g, b, a = arr[..., 0], arr[..., 1], arr[..., 2], arr[..., 3]

    # Studio green is ~ (10-25, 195-220, 10-30); keep threshold aggressive.
    green_dom = (g > 120) & (g > r * 1.55) & (g > b * 1.55) & (r < 110) & (b < 110)
    bright_green = (g > 160) & (r < 100) & (b < 100) & (g > r + 40) & (g > b + 40)
    mask = green_dom | bright_green

    alpha = a.copy()
    alpha[mask] = 0

    # Soft fringe → transparent
    soft = (g > 90) & (g > r * 1.2) & (g > b * 1.2) & (~mask)
    soft_factor = np.clip((g - np.maximum(r, b)) / 90.0, 0, 1)
    alpha[soft] = alpha[soft] * (1.0 - soft_factor[soft])

    # Despill remaining green halo on opaque edge pixels
    remain = alpha > 20
    spill = remain & (g > r + 12) & (g > b + 12)
    g2 = g.copy()
    g2[spill] = np.maximum(r[spill], b[spill]) * 0.92 + g[spill] * 0.08

    # Nuke faint sparkle watermark in bottom-right corner
    h, w = alpha.shape
    y0, x0 = int(h * 0.88), int(w * 0.88)
    corner = arr[y0:, x0:]
    cr, cg, cb = corner[..., 0], corner[..., 1], corner[..., 2]
    sparkle = ((cr + cg + cb) > 400) | ((cg > 140) & (cr < 110) & (cb < 110))
    ca = alpha[y0:, x0:]
    ca[sparkle] = 0
    alpha[y0:, x0:] = ca

    out = arr.copy()
    out[..., 1] = g2
    out[..., 3] = alpha
    return Image.fromarray(out.astype(np.uint8), "RGBA")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    AUDIT_DIR.mkdir(parents=True, exist_ok=True)

    for fname, expr in SRC_MAP.items():
        src = SRC_DIR / fname
        if not src.is_file():
            raise SystemExit(f"missing source: {src}")
        keyed = key_green(Image.open(src))
        out_path = OUT_DIR / f"{expr}.png"
        keyed.save(out_path, optimize=True)

        for bg, label in (((10, 10, 12, 255), "dark"), ((244, 244, 246, 255), "light")):
            base = Image.new("RGBA", keyed.size, bg)
            preview = Image.alpha_composite(base, keyed).convert("RGB")
            preview.save(AUDIT_DIR / f"{expr}_on_{label}.jpg", quality=90)

        opaque = int((np.asarray(keyed)[..., 3] > 200).sum())
        transparent = int((np.asarray(keyed)[..., 3] < 10).sum())
        print(f"{expr}: {out_path.name} opaque={opaque} transparent={transparent}")


if __name__ == "__main__":
    main()

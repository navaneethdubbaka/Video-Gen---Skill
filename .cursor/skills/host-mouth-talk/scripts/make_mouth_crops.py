#!/usr/bin/env python3
"""Save 5x zoomed mouth crops + polygon overlays for visual measurement."""

from __future__ import annotations

import json
from pathlib import Path

import cv2
import numpy as np

# Refined windows after first crop pass (x0,y0,x1,y1)
WINDOWS = {
    # 480x853 — mouth sits lower than first guess
    "talk_loop": (175, 360, 310, 460),
    "talk_emph": (175, 360, 310, 460),
    "think": (175, 350, 310, 450),
    "shrug": (175, 340, 315, 440),
    "idle_bob": (165, 360, 310, 460),
    "point_up": (175, 400, 315, 500),
    "point_side": (120, 350, 270, 450),
    "celebrate": (165, 320, 305, 420),
    "hang": (190, 400, 330, 520),  # upside-down: mouth near mid-lower
    # 1024x1024 — Claude-measured present mouth ~488,413
    "present": (420, 390, 560, 460),
    "wave": (420, 390, 560, 460),
    "thumbs_up": (420, 390, 560, 460),
    "lean_in": (420, 390, 560, 460),
    "cross_arms": (430, 390, 570, 460),
    "facepalm_lite": (360, 380, 520, 470),
}


def main() -> None:
    ws = Path(__file__).resolve().parents[4]
    stills = ws / "greencode" / "my_animations" / "host_stills"
    out = Path(__file__).resolve().parents[1] / "qa_crops"
    out.mkdir(parents=True, exist_ok=True)

    for stem, (x0, y0, x1, y1) in WINDOWS.items():
        src = stills / f"{stem}.png"
        if not src.is_file():
            print("missing", stem)
            continue
        img = cv2.imread(str(src), cv2.IMREAD_UNCHANGED)
        if img.shape[2] == 4:
            a = img[:, :, 3:4].astype(np.float32) / 255.0
            bgr = img[:, :, :3].astype(np.float32)
            bg = np.full_like(bgr, 180)
            comp = (bgr * a + bg * (1 - a)).astype(np.uint8)
        else:
            comp = img[:, :, :3]
        h, w = comp.shape[:2]
        x0c, y0c = max(0, x0), max(0, y0)
        x1c, y1c = min(w, x1), min(h, y1)
        crop = comp[y0c:y1c, x0c:x1c]
        zoom = cv2.resize(crop, None, fx=5, fy=5, interpolation=cv2.INTER_CUBIC)
        cv2.imwrite(str(out / f"{stem}_crop5x.png"), zoom)
        vis = comp.copy()
        cv2.rectangle(vis, (x0c, y0c), (x1c, y1c), (0, 255, 0), 2)
        cv2.imwrite(str(out / f"{stem}_box.png"), vis)
        meta = {"origin": [x0c, y0c], "size": [w, h], "window": [x0c, y0c, x1c, y1c]}
        (out / f"{stem}_meta.json").write_text(json.dumps(meta), encoding="utf-8")
        print(stem, meta)


if __name__ == "__main__":
    main()

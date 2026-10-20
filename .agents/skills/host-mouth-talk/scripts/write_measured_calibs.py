#!/usr/bin/env python3
"""Write visually measured calib JSON + polygon overlay PNGs for QA."""

from __future__ import annotations

import json
from pathlib import Path

import cv2
import numpy as np

# Claude's measured poly for the 1024 present-class open smile (image_png_20261015160807)
CLAUDE_1024 = {
    "poly": [
        [443, 420], [452, 416], [466, 414], [490, 412], [520, 412], [534, 412],
        [529, 422], [520, 430], [512, 434], [488, 438], [466, 435], [450, 428],
    ],
    "anchor_y": 413.0,
    "cx": 488.0,
    "skin_sample": [440, 446, 455, 482],
    "box": [388, 466, 416, 560],
    "roi": [420, 556, 392, 462],
    "ref_size": [1024, 1024],
    "s_max": 1.25,
    "notes": "Claude measured; open mouth with teeth+tongue",
}

# 480x853 family — measured from refined 5x crops (origin + local)
# talk_loop crop origin (175,360), mouth ~center of 135x100 with open teeth
CALIBS_480 = {
    # Mouth sits just below mustache on 480x853 busts — measured from poly overlay QA
    # Tight mouth-only polys (below mustache, above soul-patch) — 480x853
    "talk_loop": {
        "poly": [
            [215, 418], [228, 414], [240, 413], [252, 413], [265, 414], [275, 418],
            [272, 424], [265, 428], [252, 430], [240, 430], [228, 428], [218, 424],
        ],
        "anchor_y": 414.0,
        "cx": 245.0,
        "skin_sample": [400, 406, 290, 310],
        "box": [400, 445, 205, 290],
        "roi": [210, 285, 400, 445],
        "ref_size": [480, 853],
        "s_max": 1.18,
        "notes": "tight to lip line only — avoid mustache warp",
    },
    "talk_emph": {
        "poly": [
            [215, 408], [228, 404], [240, 403], [252, 403], [265, 404], [275, 408],
            [272, 414], [265, 418], [252, 420], [240, 420], [228, 418], [218, 414],
        ],
        "anchor_y": 404.0,
        "cx": 245.0,
        "skin_sample": [390, 396, 290, 310],
        "box": [390, 435, 205, 290],
        "roi": [210, 285, 390, 435],
        "ref_size": [480, 853],
        "s_max": 1.18,
    },
    "think": {
        "poly": [
            [215, 402], [228, 398], [240, 397], [252, 397], [265, 398], [275, 402],
            [272, 408], [265, 412], [252, 414], [240, 414], [228, 412], [218, 408],
        ],
        "anchor_y": 398.0,
        "cx": 245.0,
        "skin_sample": [385, 391, 290, 310],
        "box": [385, 430, 205, 290],
        "roi": [210, 285, 385, 430],
        "ref_size": [480, 853],
        "s_max": 1.1,
    },
    "shrug": {
        "poly": [
            [217, 392], [230, 388], [242, 387], [254, 387], [267, 388], [277, 392],
            [274, 398], [267, 402], [254, 404], [242, 404], [230, 402], [220, 398],
        ],
        "anchor_y": 388.0,
        "cx": 247.0,
        "skin_sample": [375, 381, 295, 315],
        "box": [375, 420, 205, 295],
        "roi": [210, 290, 375, 420],
        "ref_size": [480, 853],
        "s_max": 1.18,
    },
    "idle_bob": {
        "poly": [
            [207, 418], [220, 414], [232, 413], [244, 413], [257, 414], [267, 418],
            [264, 424], [257, 428], [244, 430], [232, 430], [220, 428], [210, 424],
        ],
        "anchor_y": 414.0,
        "cx": 237.0,
        "skin_sample": [400, 406, 275, 295],
        "box": [400, 445, 195, 280],
        "roi": [200, 275, 400, 445],
        "ref_size": [480, 853],
        "s_max": 1.18,
    },
    "point_up": {
        "poly": [
            [217, 454], [230, 450], [242, 449], [254, 449], [267, 450], [277, 454],
            [274, 460], [267, 464], [254, 466], [242, 466], [230, 464], [220, 460],
        ],
        "anchor_y": 450.0,
        "cx": 247.0,
        "skin_sample": [435, 441, 295, 315],
        "box": [435, 480, 205, 295],
        "roi": [210, 290, 435, 480],
        "ref_size": [480, 853],
        "s_max": 1.18,
    },
    "point_side": {
        "poly": [
            [165, 408], [178, 404], [190, 403], [202, 403], [215, 404], [225, 408],
            [222, 414], [215, 418], [202, 420], [190, 420], [178, 418], [168, 414],
        ],
        "anchor_y": 404.0,
        "cx": 195.0,
        "skin_sample": [390, 396, 240, 260],
        "box": [390, 435, 155, 245],
        "roi": [160, 240, 390, 435],
        "ref_size": [480, 853],
        "s_max": 1.18,
    },
    "celebrate": {
        "poly": [
            [208, 342], [222, 336], [236, 334], [250, 334], [264, 336], [276, 342],
            [272, 352], [262, 360], [250, 364], [236, 364], [224, 360], [212, 352],
        ],
        "anchor_y": 335.0,
        "cx": 242.0,
        "skin_sample": [320, 328, 290, 310],
        "box": [320, 380, 200, 290],
        "roi": [200, 285, 320, 380],
        "ref_size": [480, 853],
        "s_max": 1.1,
        "notes": "wide smile; ROI stops above chin/neck to avoid dark fill smear",
    },
    "hang": {
        "poly": [
            [215, 420], [228, 417], [240, 416], [252, 416], [265, 417], [275, 420],
            [272, 423], [265, 426], [252, 427], [240, 427], [228, 426], [218, 423],
        ],
        "anchor_y": 417.0,
        "cx": 245.0,
        "skin_sample": [405, 411, 290, 310],
        "box": [405, 445, 205, 290],
        "roi": [210, 285, 405, 445],
        "ref_size": [480, 853],
        "s_max": 1.08,
        "rotate": 180,
        "closed_source": True,
        "notes": "closed source after rotate; stretch-only",
    },
}

# 1024 family variants of Claude poly (small CX shifts from face position)
CALIBS_1024 = {
    "present": {**CLAUDE_1024},
    "wave": {
        **CLAUDE_1024,
        "poly": [
            [442, 422], [455, 415], [475, 412], [508, 412], [540, 414], [568, 420],
            [560, 440], [540, 455], [508, 460], [475, 458], [455, 448], [445, 435],
        ],
        "anchor_y": 414.0,
        "cx": 508.0,
        "skin_sample": [395, 405, 530, 560],
        "box": [380, 480, 420, 590],
        "roi": [425, 580, 385, 475],
        "s_max": 1.2,
        "notes": "wave open smile; measured from crop",
    },
    "lean_in": {**CLAUDE_1024, "notes": "lean_in similar open mouth; Claude poly baseline"},
    "thumbs_up": {
        **CLAUDE_1024,
        "poly": [
            [450, 418], [465, 414], [485, 412], [505, 412], [525, 414], [540, 418],
            [535, 424], [525, 428], [505, 430], [485, 430], [465, 428], [452, 424],
        ],
        "anchor_y": 414.0,
        "cx": 495.0,
        "skin_sample": [430, 438, 530, 560],
        "box": [390, 460, 430, 560],
        "roi": [430, 560, 395, 455],
        "s_max": 1.15,
        "notes": "CLOSED mouth in source — stretch only, no teeth interior",
        "closed_source": True,
    },
    "cross_arms": {
        **CLAUDE_1024,
        "cx": 510.0,
        "poly": [
            [460, 420], [475, 416], [495, 414], [515, 414], [535, 416], [550, 420],
            [545, 428], [535, 434], [515, 436], [495, 436], [475, 434], [462, 428],
        ],
        "anchor_y": 414.0,
        "skin_sample": [440, 448, 545, 575],
        "box": [390, 470, 440, 580],
        "roi": [445, 575, 395, 465],
        "s_max": 1.2,
    },
    "facepalm_lite": {
        "poly": [
            [400, 425], [420, 418], [445, 414], [470, 414], [495, 418], [515, 425],
            [508, 438], [495, 448], [470, 452], [445, 452], [420, 448], [405, 438],
        ],
        "anchor_y": 416.0,
        "cx": 455.0,
        "skin_sample": [400, 410, 520, 555],
        "box": [380, 480, 380, 540],
        "roi": [385, 535, 390, 470],
        "ref_size": [1024, 1024],
        "s_max": 1.15,
        "notes": "face shifted left; hand on forehead — mouth clear",
    },
}


def draw_overlay(stills: Path, out: Path, stem: str, calib: dict) -> None:
    src = stills / f"{stem}.png"
    img = cv2.imread(str(src), cv2.IMREAD_UNCHANGED)
    if img.shape[2] == 4:
        a = img[:, :, 3:4].astype(np.float32) / 255.0
        bgr = img[:, :, :3].astype(np.float32)
        bg = np.full_like(bgr, 40)
        vis = (bgr * a + bg * (1 - a)).astype(np.uint8)
    else:
        vis = img[:, :, :3].copy()
    poly = np.array(calib["poly"], np.int32)
    cv2.polylines(vis, [poly], True, (0, 255, 0), 2)
    cx, ay = int(calib["cx"]), int(calib["anchor_y"])
    cv2.circle(vis, (cx, ay), 4, (0, 0, 255), -1)
    cv2.line(vis, (cx - 40, ay), (cx + 40, ay), (0, 0, 255), 1)
    x0, x1, y0, y1 = [int(v) for v in calib["roi"]]
    cv2.rectangle(vis, (x0, y0), (x1, y1), (255, 128, 0), 1)
    cv2.imwrite(str(out / f"{stem}_poly.png"), vis)


def main() -> None:
    skill = Path(__file__).resolve().parents[1]
    ws = Path(__file__).resolve().parents[4]
    calib_dir = skill / "calib"
    overlay_dir = skill / "qa_crops"
    stills = ws / "greencode" / "my_animations" / "host_stills"
    calib_dir.mkdir(parents=True, exist_ok=True)
    overlay_dir.mkdir(parents=True, exist_ok=True)

    all_calibs = {**CALIBS_480, **CALIBS_1024}
    for stem, calib in all_calibs.items():
        path = calib_dir / f"{stem}.json"
        path.write_text(json.dumps(calib, indent=2) + "\n", encoding="utf-8")
        draw_overlay(stills, overlay_dir, stem, calib)
        print("wrote", stem, "rotate=" + str(calib.get("rotate", 0)))


if __name__ == "__main__":
    main()

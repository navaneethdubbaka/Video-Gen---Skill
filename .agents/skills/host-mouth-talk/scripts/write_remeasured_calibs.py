#!/usr/bin/env python3
"""Write visually remounted mouth calibs (STEP 1) then animate + contact sheets."""

from __future__ import annotations

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
MEASURE = SKILL / "scripts" / "measure_and_verify.py"

# Defaults after fill/ROI fixes in animate_mouth.py
D = dict(dilate_sprite=3, dilate_fill=17, alpha_blur=0.8, fill_blur=1.5, lab_tol=12)


def save(stem: str, calib: dict) -> None:
    CALIB.mkdir(parents=True, exist_ok=True)
    path = CALIB / f"{stem}.json"
    path.write_text(json.dumps(calib, indent=2) + "\n", encoding="utf-8")
    # poly overlay on still (apply rotate for hang preview)
    img = cv2.imread(str(STILLS / f"{stem}.png"), cv2.IMREAD_UNCHANGED)
    rot = int(calib.get("rotate", 0) or 0)
    if rot == 180:
        img = cv2.rotate(img, cv2.ROTATE_180)
    if img.shape[2] == 4:
        a = img[:, :, 3:4].astype(np.float32) / 255
        bgr = img[:, :, :3].astype(np.float32)
        vis = (bgr * a + 40 * (1 - a)).astype(np.uint8)
    else:
        vis = img[:, :, :3].copy()
    poly = np.array(calib["poly"], np.int32)
    cv2.polylines(vis, [poly], True, (0, 255, 0), 2)
    cv2.drawMarker(
        vis,
        (int(calib["cx"]), int(calib["anchor_y"])),
        (0, 0, 255),
        cv2.MARKER_CROSS,
        18,
        2,
    )
    x0, x1, y0, y1 = [int(v) for v in calib["roi"]]
    cv2.rectangle(vis, (x0, y0), (x1, y1), (255, 128, 0), 1)
    sy0, sy1, sx0, sx1 = [int(v) for v in calib["skin_sample"]]
    cv2.rectangle(vis, (sx0, sy0), (sx1, sy1), (255, 0, 255), 1)
    if "chin_y" in calib:
        cv2.line(vis, (x0, int(calib["chin_y"])), (x1, int(calib["chin_y"])), (0, 200, 255), 1)
    QA.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(QA / f"{stem}_poly.png"), vis)
    print(f"wrote {stem}: cx={calib['cx']} ay={calib['anchor_y']} s_max={calib.get('s_max')}")


def f2(ox, oy, zx, zy, z=2.0):
    return [round(ox + zx / z, 2), round(oy + zy / z, 2)]


def f4(ox, oy, zx, zy, z=4.0):
    return [round(ox + zx / z, 2), round(oy + zy / z, 2)]


def f5(ox, oy, zx, zy, z=5.0):
    return [round(ox + zx / z, 2), round(oy + zy / z, 2)]


def main() -> None:
    # ---------- 480x853 family (face2x origin 80,200 unless noted) ----------
    # talk_emph OPEN — was wrongly on neck
    ox, oy = 80, 200
    save(
        "talk_emph",
        {
            "poly": [
                f2(ox, oy, 262, 222),
                f2(ox, oy, 280, 215),
                f2(ox, oy, 300, 212),
                f2(ox, oy, 318, 212),
                f2(ox, oy, 335, 212),
                f2(ox, oy, 355, 215),
                f2(ox, oy, 375, 222),
                f2(ox, oy, 360, 232),
                f2(ox, oy, 345, 240),
                f2(ox, oy, 318, 242),
                f2(ox, oy, 290, 240),
                f2(ox, oy, 275, 232),
            ],
            "anchor_y": round(oy + 212 / 2, 2),
            "cx": round(ox + 318 / 2, 2),
            "skin_sample": [oy + 250 / 2, oy + 280 / 2, ox + 380 / 2, ox + 430 / 2],
            "box": [oy + 190 / 2, oy + 280 / 2, ox + 230 / 2, ox + 400 / 2],
            "roi": [ox + 240 / 2, ox + 400 / 2, oy + 190 / 2, oy + 280 / 2],
            "ref_size": [480, 853],
            "s_max": 1.25,
            "chin_y": round(oy + 300 / 2, 2),
            "notes": "OPEN teeth; remounted from face2x (was on neck)",
            **D,
        },
    )

    # idle_bob CLOSED
    save(
        "idle_bob",
        {
            "poly": [
                f2(ox, oy, 255, 192),
                f2(ox, oy, 280, 189),
                f2(ox, oy, 314, 188),
                f2(ox, oy, 350, 189),
                f2(ox, oy, 372, 190),
                f2(ox, oy, 365, 198),
                f2(ox, oy, 345, 206),
                f2(ox, oy, 314, 208),
                f2(ox, oy, 285, 206),
                f2(ox, oy, 265, 198),
            ],
            "anchor_y": round(oy + 188 / 2, 2),
            "cx": round(ox + 314 / 2, 2),
            "skin_sample": [oy + 220 / 2, oy + 250 / 2, ox + 380 / 2, ox + 430 / 2],
            "box": [oy + 160 / 2, oy + 250 / 2, ox + 230 / 2, ox + 400 / 2],
            "roi": [ox + 230 / 2, ox + 400 / 2, oy + 160 / 2, oy + 250 / 2],
            "ref_size": [480, 853],
            "s_max": 1.2,
            "chin_y": round(oy + 270 / 2, 2),
            "closed_source": True,
            "notes": "CLOSED smile — synthetic open mouth",
            **D,
        },
    )

    # shrug CLOSED
    save(
        "shrug",
        {
            "poly": [
                f2(ox, oy, 238, 228),
                f2(ox, oy, 270, 226),
                f2(ox, oy, 300, 226),
                f2(ox, oy, 330, 226),
                f2(ox, oy, 362, 228),
                f2(ox, oy, 345, 230),
                f2(ox, oy, 320, 232),
                f2(ox, oy, 300, 233),
                f2(ox, oy, 280, 232),
                f2(ox, oy, 255, 230),
            ],
            "anchor_y": round(oy + 226 / 2, 2),
            "cx": round(ox + 300 / 2, 2),
            "skin_sample": [oy + 250 / 2, oy + 280 / 2, ox + 380 / 2, ox + 430 / 2],
            "box": [oy + 200 / 2, oy + 280 / 2, ox + 210 / 2, ox + 390 / 2],
            "roi": [ox + 210 / 2, ox + 390 / 2, oy + 200 / 2, oy + 280 / 2],
            "ref_size": [480, 853],
            "s_max": 1.15,
            "chin_y": round(oy + 300 / 2, 2),
            "closed_source": True,
            "notes": "CLOSED — synthetic open mouth",
            **D,
        },
    )

    # point_side OPEN
    save(
        "point_side",
        {
            "poly": [
                f2(ox, oy, 220, 212),
                f2(ox, oy, 240, 200),
                f2(ox, oy, 275, 195),
                f2(ox, oy, 310, 200),
                f2(ox, oy, 330, 212),
                f2(ox, oy, 305, 224),
                f2(ox, oy, 275, 226),
                f2(ox, oy, 245, 224),
            ],
            "anchor_y": round(oy + 195 / 2, 2),
            "cx": round(ox + 275 / 2, 2),
            "skin_sample": [oy + 240 / 2, oy + 270 / 2, ox + 340 / 2, ox + 390 / 2],
            "box": [oy + 170 / 2, oy + 260 / 2, ox + 190 / 2, ox + 360 / 2],
            "roi": [ox + 190 / 2, ox + 360 / 2, oy + 170 / 2, oy + 260 / 2],
            "ref_size": [480, 853],
            "s_max": 1.2,
            "chin_y": round(oy + 300 / 2, 2),
            "notes": "OPEN teeth; face slightly turned",
            **D,
        },
    )

    # think CLOSED — faceB origin 60,150 x2; hand near chin → low s_max
    tox, toy = 60, 150
    save(
        "think",
        {
            "poly": [
                f2(tox, toy, 280, 535),
                f2(tox, toy, 310, 528),
                f2(tox, toy, 335, 523),
                f2(tox, toy, 355, 522),
                f2(tox, toy, 375, 523),
                f2(tox, toy, 405, 525),
                f2(tox, toy, 430, 528),
                f2(tox, toy, 405, 535),
                f2(tox, toy, 380, 542),
                f2(tox, toy, 355, 545),
                f2(tox, toy, 330, 542),
                f2(tox, toy, 305, 538),
            ],
            "anchor_y": round(toy + 522 / 2, 2),
            "cx": round(tox + 355 / 2, 2),
            "skin_sample": [toy + 560 / 2, toy + 590 / 2, tox + 450 / 2, tox + 500 / 2],
            "box": [toy + 500 / 2, toy + 580 / 2, tox + 250 / 2, tox + 460 / 2],
            "roi": [tox + 250 / 2, tox + 460 / 2, toy + 500 / 2, toy + 580 / 2],
            "ref_size": [480, 853],
            "s_max": 1.05,
            "chin_y": round(toy + 575 / 2, 2),
            "closed_source": True,
            "notes": "CLOSED; hand near chin — low s_max; synthetic open",
            **D,
        },
    )

    # point_up OPEN — crop5x origin 162,355 (from prior window)
    pox, poy = 162, 355
    save(
        "point_up",
        {
            "poly": [
                f5(pox, poy, 300, 210),
                f5(pox, poy, 380, 165),
                f5(pox, poy, 440, 165),
                f5(pox, poy, 560, 165),
                f5(pox, poy, 630, 210),
                f5(pox, poy, 580, 240),
                f5(pox, poy, 450, 270),
                f5(pox, poy, 320, 240),
            ],
            "anchor_y": round(poy + 165 / 5, 2),
            "cx": round(pox + 440 / 5, 2),
            "skin_sample": [poy + 220 / 5, poy + 260 / 5, pox + 700 / 5, pox + 780 / 5],
            "box": [poy + 120 / 5, poy + 300 / 5, pox + 250 / 5, pox + 680 / 5],
            "roi": [pox + 260 / 5, pox + 670 / 5, poy + 120 / 5, poy + 300 / 5],
            "ref_size": [480, 853],
            "s_max": 1.2,
            "chin_y": round(poy + 340 / 5, 2),
            "notes": "OPEN slight; teeth sliver; mustache tight to anchor",
            **D,
        },
    )

    # celebrate OPEN — crop5x origin 160,279
    cox, coy = 160, 279
    save(
        "celebrate",
        {
            "poly": [
                f5(cox, coy, 320, 190),
                f5(cox, coy, 400, 170),
                f5(cox, coy, 465, 175),
                f5(cox, coy, 540, 160),
                f5(cox, coy, 645, 190),
                f5(cox, coy, 600, 235),
                f5(cox, coy, 480, 265),
                f5(cox, coy, 370, 245),
            ],
            "anchor_y": round(coy + 175 / 5, 2),
            "cx": round(cox + 465 / 5, 2),
            "skin_sample": [coy + 250 / 5, coy + 290 / 5, cox + 100 / 5, cox + 180 / 5],
            "box": [coy + 140 / 5, coy + 300 / 5, cox + 280 / 5, cox + 680 / 5],
            "roi": [cox + 280 / 5, cox + 680 / 5, coy + 140 / 5, coy + 300 / 5],
            "ref_size": [480, 853],
            "s_max": 1.2,
            "chin_y": round(coy + 340 / 5, 2),
            "notes": "OPEN smile teeth",
            **D,
        },
    )

    # talk_loop OPEN — crop5x origin 173,385
    lox, loy = 173, 385
    save(
        "talk_loop",
        {
            "poly": [
                f5(lox, loy, 220, 205),
                f5(lox, loy, 250, 190),
                f5(lox, loy, 340, 170),
                f5(lox, loy, 445, 165),
                f5(lox, loy, 535, 175),
                f5(lox, loy, 600, 200),
                f5(lox, loy, 645, 215),
                f5(lox, loy, 620, 245),
                f5(lox, loy, 540, 260),
                f5(lox, loy, 450, 270),
                f5(lox, loy, 320, 260),
                f5(lox, loy, 240, 235),
            ],
            "anchor_y": round(loy + 165 / 5, 2),
            "cx": round(lox + 445 / 5, 2),
            "skin_sample": [loy + 150 / 5, loy + 220 / 5, lox + 40 / 5, lox + 120 / 5],
            "box": [loy + 120 / 5, loy + 290 / 5, lox + 180 / 5, lox + 680 / 5],
            "roi": [lox + 180 / 5, lox + 680 / 5, loy + 120 / 5, loy + 290 / 5],
            "ref_size": [480, 853],
            "s_max": 1.2,
            "chin_y": round(loy + 340 / 5, 2),
            "notes": "OPEN teeth",
            **D,
        },
    )

    # hang OPEN after 180 — crop x4 origin 140,350
    hox, hoy = 140, 350
    save(
        "hang",
        {
            "poly": [
                f4(hox, hoy, 336, 436),
                f4(hox, hoy, 380, 420),
                f4(hox, hoy, 410, 417),
                f4(hox, hoy, 440, 416),
                f4(hox, hoy, 470, 417),
                f4(hox, hoy, 510, 422),
                f4(hox, hoy, 552, 432),
                f4(hox, hoy, 515, 475),
                f4(hox, hoy, 480, 490),
                f4(hox, hoy, 440, 496),
                f4(hox, hoy, 400, 490),
                f4(hox, hoy, 365, 475),
            ],
            "anchor_y": round(hoy + 416 / 4, 2),
            "cx": round(hox + 440 / 4, 2),
            "skin_sample": [hoy + 520 / 4, hoy + 560 / 4, hox + 600 / 4, hox + 680 / 4],
            "box": [hoy + 380 / 4, hoy + 540 / 4, hox + 280 / 4, hox + 600 / 4],
            "roi": [hox + 280 / 4, hox + 600 / 4, hoy + 380 / 4, hoy + 540 / 4],
            "ref_size": [480, 853],
            "s_max": 1.15,
            "chin_y": round(hoy + 560 / 4, 2),
            "rotate": 180,
            "notes": "OPEN after 180 rotate; teeth visible — not closed",
            **D,
        },
    )

    # ---------- 1024 family ----------
    # present OPEN — crop5x origin 398,378 (Claude-aligned, tightened)
    prx, pry = 398, 378
    save(
        "present",
        {
            "poly": [
                f5(prx, pry, 205, 215),
                f5(prx, pry, 265, 185),
                f5(prx, pry, 360, 168),
                f5(prx, pry, 440, 165),
                f5(prx, pry, 560, 170),
                f5(prx, pry, 685, 175),
                f5(prx, pry, 715, 215),
                f5(prx, pry, 695, 255),
                f5(prx, pry, 590, 290),
                f5(prx, pry, 440, 310),
                f5(prx, pry, 330, 305),
                f5(prx, pry, 285, 280),
            ],
            "anchor_y": round(pry + 165 / 5, 2),
            "cx": round(prx + 440 / 5, 2),
            "skin_sample": [pry + 300 / 5, pry + 340 / 5, prx + 100 / 5, prx + 180 / 5],
            "box": [pry + 120 / 5, pry + 360 / 5, prx + 150 / 5, prx + 760 / 5],
            "roi": [prx + 160 / 5, prx + 760 / 5, pry + 120 / 5, pry + 360 / 5],
            "ref_size": [1024, 1024],
            "s_max": 1.25,
            "chin_y": round(pry + 400 / 5, 2),
            "notes": "OPEN teeth+tongue",
            **D,
        },
    )

    # lean_in OPEN — faceB origin 250,250 x2
    lx, ly = 250, 250
    save(
        "lean_in",
        {
            "poly": [
                f2(lx, ly, 375, 395),
                f2(lx, ly, 400, 375),
                f2(lx, ly, 440, 365),
                f2(lx, ly, 485, 362),
                f2(lx, ly, 530, 365),
                f2(lx, ly, 570, 375),
                f2(lx, ly, 595, 395),
                f2(lx, ly, 580, 425),
                f2(lx, ly, 535, 450),
                f2(lx, ly, 485, 458),
                f2(lx, ly, 435, 450),
                f2(lx, ly, 390, 425),
            ],
            "anchor_y": round(ly + 362 / 2, 2),
            "cx": round(lx + 485 / 2, 2),
            "skin_sample": [ly + 500 / 2, ly + 540 / 2, lx + 620 / 2, lx + 700 / 2],
            "box": [ly + 320 / 2, ly + 520 / 2, lx + 320 / 2, lx + 660 / 2],
            "roi": [lx + 320 / 2, lx + 660 / 2, ly + 320 / 2, ly + 520 / 2],
            "ref_size": [1024, 1024],
            "s_max": 1.25,
            "chin_y": round(ly + 520 / 2, 2),
            "notes": "OPEN teeth+tongue",
            **D,
        },
    )

    # cross_arms — similar to present, CX shifted right ~22px from present
    present_cal = json.loads((CALIB / "present.json").read_text(encoding="utf-8"))
    ca = dict(present_cal)
    shift = 22
    ca["cx"] = round(present_cal["cx"] + shift, 2)
    ca["poly"] = [[p[0] + shift, p[1]] for p in present_cal["poly"]]
    ca["roi"] = [
        present_cal["roi"][0] + shift,
        present_cal["roi"][1] + shift,
        present_cal["roi"][2],
        present_cal["roi"][3],
    ]
    ca["box"] = [
        present_cal["box"][0],
        present_cal["box"][1],
        present_cal["box"][2] + shift,
        present_cal["box"][3] + shift,
    ]
    ca["skin_sample"] = [
        present_cal["skin_sample"][0],
        present_cal["skin_sample"][1],
        present_cal["skin_sample"][2] + shift,
        present_cal["skin_sample"][3] + shift,
    ]
    ca["notes"] = "OPEN; CX shifted right vs present"
    save("cross_arms", ca)

    # wave OPEN — crop5x origin 402,373
    wox, woy = 402, 373
    save(
        "wave",
        {
            "poly": [
                f5(wox, woy, 220, 230),
                f5(wox, woy, 300, 185),
                f5(wox, woy, 440, 165),
                f5(wox, woy, 600, 175),
                f5(wox, woy, 705, 195),
                f5(wox, woy, 580, 280),
                f5(wox, woy, 440, 320),
                f5(wox, woy, 320, 300),
            ],
            "anchor_y": round(woy + 165 / 5, 2),
            "cx": round(wox + 440 / 5, 2),
            "skin_sample": [woy + 250 / 5, woy + 300 / 5, wox + 40 / 5, wox + 120 / 5],
            "box": [woy + 100 / 5, woy + 360 / 5, wox + 160 / 5, wox + 760 / 5],
            "roi": [wox + 160 / 5, wox + 760 / 5, woy + 100 / 5, woy + 380 / 5],
            "ref_size": [1024, 1024],
            "s_max": 1.25,
            "chin_y": round(woy + 400 / 5, 2),
            "notes": "OPEN smile teeth+tongue",
            **D,
        },
    )

    # thumbs_up CLOSED — crop5x origin 402,384
    tox2, toy2 = 402, 384
    save(
        "thumbs_up",
        {
            "poly": [
                f5(tox2, toy2, 180, 140),
                f5(tox2, toy2, 300, 155),
                f5(tox2, toy2, 400, 150),
                f5(tox2, toy2, 500, 135),
                f5(tox2, toy2, 600, 120),
                f5(tox2, toy2, 680, 110),
                f5(tox2, toy2, 640, 150),
                f5(tox2, toy2, 550, 180),
                f5(tox2, toy2, 440, 190),
                f5(tox2, toy2, 340, 185),
                f5(tox2, toy2, 230, 175),
            ],
            "anchor_y": round(toy2 + 150 / 5, 2),
            "cx": round(tox2 + 440 / 5, 2),
            "skin_sample": [toy2 + 250 / 5, toy2 + 300 / 5, tox2 + 40 / 5, tox2 + 120 / 5],
            "box": [toy2 + 80 / 5, toy2 + 230 / 5, tox2 + 120 / 5, tox2 + 740 / 5],
            "roi": [tox2 + 120 / 5, tox2 + 740 / 5, toy2 + 80 / 5, toy2 + 230 / 5],
            "ref_size": [1024, 1024],
            "s_max": 1.15,
            "chin_y": round(toy2 + 280 / 5, 2),
            "closed_source": True,
            "notes": "CLOSED smile — synthetic open mouth",
            **D,
        },
    )

    # facepalm_lite — faceB origin 250,250; slight open with teeth strip
    fx, fy = 250, 250
    save(
        "facepalm_lite",
        {
            "poly": [
                f2(fx, fy, 375, 385),
                f2(fx, fy, 425, 370),
                f2(fx, fy, 475, 365),
                f2(fx, fy, 525, 362),
                f2(fx, fy, 575, 360),
                f2(fx, fy, 565, 375),
                f2(fx, fy, 540, 405),
                f2(fx, fy, 480, 425),
                f2(fx, fy, 420, 420),
                f2(fx, fy, 390, 405),
            ],
            "anchor_y": round(fy + 365 / 2, 2),
            "cx": round(fx + 475 / 2, 2),
            "skin_sample": [fy + 480 / 2, fy + 520 / 2, fx + 620 / 2, fx + 700 / 2],
            "box": [fy + 320 / 2, fy + 480 / 2, fx + 320 / 2, fx + 640 / 2],
            "roi": [fx + 320 / 2, fx + 640 / 2, fy + 320 / 2, fy + 480 / 2],
            "ref_size": [1024, 1024],
            "s_max": 1.15,
            "chin_y": round(fy + 520 / 2, 2),
            "notes": "slight open teeth strip",
            **D,
        },
    )

    stems = [
        "present",
        "wave",
        "lean_in",
        "cross_arms",
        "facepalm_lite",
        "thumbs_up",
        "celebrate",
        "point_up",
        "talk_loop",
        "talk_emph",
        "idle_bob",
        "shrug",
        "think",
        "point_side",
        "hang",
    ]
    for stem in stems:
        print("=== animate", stem)
        subprocess.check_call(
            [
                sys.executable,
                str(ANIMATE),
                str(STILLS / f"{stem}.png"),
                str(TALKING / stem),
                "--calib",
                str(CALIB / f"{stem}.json"),
            ]
        )
        subprocess.check_call([sys.executable, str(MEASURE), "sheet", stem])


if __name__ == "__main__":
    main()

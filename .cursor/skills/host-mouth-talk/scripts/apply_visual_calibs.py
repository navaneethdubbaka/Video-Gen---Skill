#!/usr/bin/env python3
"""Write calibs measured from 5x crops (full = origin + zoomed/5), then animate+sheet."""

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


def F(ox, oy, zx, zy, z=5.0):
    return [round(ox + zx / z, 2), round(oy + zy / z, 2)]


def pack(stem, ox, oy, zoomed_poly, z_ay, z_cx, z_skin, z_box, z_roi, **extra):
    """zoomed_* are in crop5x pixel space; skin/box are y0,y1,x0,x1; roi x0,x1,y0,y1."""
    poly = [F(ox, oy, x, y) for x, y in zoomed_poly]
    ay = oy + z_ay / 5.0
    cx = ox + z_cx / 5.0
    # skin/box: zoomed (y0,y1,x0,x1)
    skin = [
        oy + z_skin[0] / 5,
        oy + z_skin[1] / 5,
        ox + z_skin[2] / 5,
        ox + z_skin[3] / 5,
    ]
    box = [
        oy + z_box[0] / 5,
        oy + z_box[1] / 5,
        ox + z_box[2] / 5,
        ox + z_box[3] / 5,
    ]
    # roi zoomed (x0,x1,y0,y1)
    roi = [
        ox + z_roi[0] / 5,
        ox + z_roi[1] / 5,
        oy + z_roi[2] / 5,
        oy + z_roi[3] / 5,
    ]
    im = cv2.imread(str(STILLS / f"{stem}.png"), cv2.IMREAD_UNCHANGED)
    h, w = im.shape[:2]
    calib = {
        "poly": poly,
        "anchor_y": round(ay, 2),
        "cx": round(cx, 2),
        "skin_sample": [round(v, 2) for v in skin],
        "box": [round(v, 2) for v in box],
        "roi": [round(v, 2) for v in roi],
        "ref_size": [w, h],
        "dilate_sprite": 7,
        "dilate_fill": 9,
        "alpha_blur": 1.0,
        "fill_blur": 1.2,
        **extra,
    }
    CALIB.mkdir(parents=True, exist_ok=True)
    (CALIB / f"{stem}.json").write_text(json.dumps(calib, indent=2) + "\n", encoding="utf-8")
    # overlay
    if im.shape[2] == 4:
        a = im[:, :, 3:4].astype(np.float32) / 255
        bgr = im[:, :, :3].astype(np.float32)
        vis = (bgr * a + 40 * (1 - a)).astype(np.uint8)
    else:
        vis = im[:, :, :3].copy()
    cv2.polylines(vis, [np.array(poly, np.int32)], True, (0, 255, 0), 2)
    cv2.drawMarker(vis, (int(cx), int(ay)), (0, 0, 255), cv2.MARKER_CROSS, 18, 2)
    cv2.rectangle(vis, (int(roi[0]), int(roi[2])), (int(roi[1]), int(roi[3])), (255, 128, 0), 1)
    cv2.rectangle(vis, (int(skin[2]), int(skin[0])), (int(skin[3]), int(skin[1])), (255, 0, 255), 1)
    QA.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(QA / f"{stem}_poly.png"), vis)
    print(f"{stem}: cx={cx:.1f} ay={ay:.1f} s_max={calib.get('s_max')}")
    return calib


def main() -> None:
    # --- present: Claude exact (verified against crop) ---
    present = {
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
        "dilate_sprite": 7,
        "dilate_fill": 9,
        "notes": "Claude measured open mouth with teeth+tongue",
    }
    (CALIB / "present.json").write_text(json.dumps(present, indent=2) + "\n", encoding="utf-8")

    # --- celebrate origin (170,280) ---
    pack(
        "celebrate", 170, 280,
        zoomed_poly=[
            (275, 185), (300, 175), (400, 170), (500, 175), (535, 195),
            (510, 240), (450, 265), (400, 270), (350, 265), (290, 240),
        ],
        z_ay=170, z_cx=400,
        z_skin=(250, 280, 100, 180),  # cheek left
        z_box=(140, 320, 200, 580),
        z_roi=(240, 560, 140, 300),
        s_max=1.2,
        notes="wide open smile with teeth",
    )

    # --- point_up origin (170,360) ---
    pack(
        "point_up", 170, 360,
        zoomed_poly=[
            (265, 177), (338, 150), (410, 148), (482, 150), (555, 177),
            (520, 205), (410, 222), (300, 205),
        ],
        z_ay=150, z_cx=410,
        z_skin=(220, 260, 80, 160),
        z_box=(120, 260, 230, 580),
        z_roi=(240, 580, 120, 250),
        s_max=1.2,
        notes="slightly open with teeth sliver",
    )

    # --- talk_loop origin (175,390) ---
    pack(
        "talk_loop", 175, 390,
        zoomed_poly=[
            (270, 185), (350, 160), (440, 150), (540, 165), (610, 205),
            (600, 230), (540, 240), (440, 248), (350, 235), (280, 215),
        ],
        z_ay=150, z_cx=440,
        z_skin=(150, 220, 40, 120),
        z_box=(120, 280, 240, 640),
        z_roi=(250, 630, 120, 270),
        s_max=1.2,
        notes="open mouth with teeth",
    )

    # --- wave origin (420,390) ---
    pack(
        "wave", 420, 390,
        zoomed_poly=[
            (115, 145), (250, 100), (360, 90), (500, 95), (610, 110),
            (520, 190), (365, 235), (200, 210),
        ],
        z_ay=90, z_cx=360,
        z_skin=(250, 290, 600, 680),
        z_box=(60, 280, 80, 650),
        z_roi=(90, 640, 60, 260),
        s_max=1.25,
        notes="open smile teeth+tongue",
    )

    # --- thumbs_up CLOSED ---
    pack(
        "thumbs_up", 420, 390,
        zoomed_poly=[
            (105, 125), (200, 135), (350, 145), (500, 110), (610, 85),
            (580, 120), (350, 165), (150, 150),
        ],
        z_ay=145, z_cx=360,
        z_skin=(250, 300, 40, 120),
        z_box=(60, 200, 80, 650),
        z_roi=(80, 640, 60, 190),
        s_max=1.15,
        closed_source=True,
        notes="CLOSED mouth — stretch only, no teeth interior",
    )

    # --- lean_in ~ present family ---
    lean = dict(present)
    lean["notes"] = "lean_in open mouth; Claude baseline"
    lean["s_max"] = 1.25
    (CALIB / "lean_in.json").write_text(json.dumps(lean, indent=2) + "\n", encoding="utf-8")

    # --- cross_arms slight CX shift right ---
    ca = dict(present)
    ca["cx"] = 510.0
    ca["poly"] = [[p[0] + 22, p[1]] for p in present["poly"]]
    ca["roi"] = [420 + 22, 556 + 22, 392, 462]
    ca["skin_sample"] = [440, 446, 455 + 22, 482 + 22]
    ca["box"] = [388, 466, 416 + 22, 560 + 22]
    ca["notes"] = "cross_arms; CX shifted right"
    (CALIB / "cross_arms.json").write_text(json.dumps(ca, indent=2) + "\n", encoding="utf-8")

    # --- facepalm_lite origin (360,380) — measure-like open smile ---
    pack(
        "facepalm_lite", 360, 380,
        zoomed_poly=[
            (200, 160), (300, 130), (420, 120), (540, 130), (650, 160),
            (600, 210), (420, 240), (240, 210),
        ],
        z_ay=125, z_cx=420,
        z_skin=(200, 240, 700, 780),
        z_box=(80, 280, 160, 700),
        z_roi=(170, 680, 90, 270),
        s_max=1.2,
        notes="slight open smile",
    )

    # Remaining 480 family — reuse talk_loop relative mouth with adjusted origins
    family = {
        "talk_emph": (175, 380),
        "idle_bob": (165, 390),
        "shrug": (175, 360),
        "think": (175, 370),
        "point_side": (120, 370),
    }
    # relative zoomed poly from talk_loop (same mouth shape family)
    rel_poly = [
        (270, 185), (350, 160), (440, 150), (540, 165), (610, 205),
        (600, 230), (540, 240), (440, 248), (350, 235), (280, 215),
    ]
    for stem, (ox, oy) in family.items():
        # point_side face is left-shifted — shrink / shift poly left in zoom space
        poly = rel_poly
        zcx, zay = 440, 150
        if stem == "point_side":
            poly = [(x - 80, y) for x, y in rel_poly]
            zcx = 360
        pack(
            stem, ox, oy,
            zoomed_poly=poly,
            z_ay=zay, z_cx=zcx,
            z_skin=(150, 220, 40, 120),
            z_box=(120, 280, 200, 620),
            z_roi=(220, 620, 120, 270),
            s_max=1.15 if stem == "think" else 1.2,
            notes=f"{stem} from talk_loop mouth family + crop origin",
        )

    # hang: rotate 180, measure as upright talk_loop-like CLOSED on rotated
    # Use upright coords on rotated image (same as talk_loop-ish closed)
    hang = {
        "poly": [
            [215, 418], [230, 414], [245, 413], [260, 413], [275, 414], [288, 418],
            [284, 422], [275, 426], [260, 428], [245, 428], [230, 426], [218, 422],
        ],
        "anchor_y": 414.0,
        "cx": 250.0,
        "skin_sample": [400, 408, 290, 315],
        "box": [395, 450, 200, 305],
        "roi": [205, 300, 400, 450],
        "ref_size": [480, 853],
        "s_max": 1.1,
        "rotate": 180,
        "dilate_sprite": 7,
        "dilate_fill": 9,
        "closed_source": True,
        "notes": "CLOSED after 180 rotate — stretch only",
    }
    (CALIB / "hang.json").write_text(json.dumps(hang, indent=2) + "\n", encoding="utf-8")
    print("hang: rotate=180 closed_source")

    # Animate + sheet all
    stems = [
        "present", "wave", "lean_in", "cross_arms", "facepalm_lite", "thumbs_up",
        "celebrate", "point_up", "talk_loop", "talk_emph", "idle_bob", "shrug",
        "think", "point_side", "hang",
    ]
    for stem in stems:
        print("===", stem)
        subprocess.check_call(
            [sys.executable, str(ANIMATE), str(STILLS / f"{stem}.png"), str(TALKING / stem), "--calib", str(CALIB / f"{stem}.json")]
        )
        subprocess.check_call([sys.executable, str(MEASURE), "sheet", stem])


if __name__ == "__main__":
    main()

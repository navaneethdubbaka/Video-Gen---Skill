import subprocess
import json
from pathlib import Path
import shutil

PROJECT = Path(r"e:\Video Gen Skill\videos\smoke-director-short")
SCRATCH_ASSETS = Path(r"e:\Video Gen Skill\scratch\assets")
CACHE_SCRIPT = Path(r"e:\Video Gen Skill\.agents\skills\hyperframe-video-director\scripts\cache_asset.py")

SCENE_QUERIES = {
    1: ("Swiggy app icon sticker cutout white border", "assets/images/ea92f525735690d7_cec8d10cfe98941d.jpg"),
    3: ("official document card with question mark mystery", "assets/images/5076bcec564057b1_a5afb5def58bfb29.jpg"),
    4: ("security shield warning icon red alert sticker", "assets/images/895ad66088f1cb71_e833f7c3c35907fe.jpg"),
    5: ("browser URL bar with highlighted token parameter", SCRATCH_ASSETS / "scene_05.png"),
    6: ("secured token lock credential card", SCRATCH_ASSETS / "scene_06.png"),
    7: ("base64 encoding code terminal decode", SCRATCH_ASSETS / "scene_07.png"),
    8: ("security checklist deny list icon", SCRATCH_ASSETS / "scene_08.png"),
    9: ("JSON data card user ID name decoded plaintext", SCRATCH_ASSETS / "scene_09.png"),
    10: ("decode modify encode cycle arrows", SCRATCH_ASSETS / "scene_10.png"),
    11: ("API testing client console verifying crafted token", SCRATCH_ASSETS / "scene_11.png"),
    12: ("green checkmark accepted verified badge", SCRATCH_ASSETS / "scene_12.png"),
    13: ("bug report document security vulnerability report card", SCRATCH_ASSETS / "scene_13.png"),
}

cached_paths = {}

# 1. Run cache_asset for scenes 5 through 13
for sid in range(5, 14):
    query, src = SCENE_QUERIES[sid]
    cmd = [
        "python", str(CACHE_SCRIPT),
        "--project", str(PROJECT),
        "--file", str(src),
        "--query", query,
        "--kind", "images",
        "--usage", f"scene_{sid:02d}",
        "--source", f"rendered_scene_{sid:02d}"
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    print(f"Cached scene {sid}: {res.stdout.strip()}")

# 2. Look up all cached asset paths
meta_dir = PROJECT / "assets" / "metadata"
for meta_file in meta_dir.glob("*.json"):
    data = json.loads(meta_file.read_text(encoding="utf-8"))
    q = data.get("query")
    f = data.get("file")
    for sid, (expected_query, _) in SCENE_QUERIES.items():
        if q == expected_query:
            cached_paths[sid] = f

print("\nResolved cached paths:")
for sid in sorted(cached_paths.keys()):
    print(f"Scene {sid}: {cached_paths[sid]}")

# 3. Update storyboard.json
sb_path = PROJECT / "storyboard" / "storyboard.json"
sb = json.loads(sb_path.read_text(encoding="utf-8"))

for scene in sb["scenes"]:
    sid = scene["scene_id"]
    if sid in (2, 14):
        scene["visual"] = {
            "type": "text_only"
        }
    else:
        q = SCENE_QUERIES[sid][0]
        cpath = cached_paths.get(sid)
        if not cpath:
            raise RuntimeError(f"Missing cached path for scene {sid}")
        scene["visual"] = {
            "type": "generated_graphic",
            "search_query": q,
            "asset_path": cpath
        }

sb_path.write_text(json.dumps(sb, indent=2), encoding="utf-8")
print("\nstoryboard.json successfully updated!")

# 4. Copy all cached assets to hyperframes/public/assets/images
pub_images = PROJECT / "composition" / "hyperframes" / "public" / "assets" / "images"
pub_images.mkdir(parents=True, exist_ok=True)

for sid, rel_path in cached_paths.items():
    src_file = PROJECT / rel_path
    dest_file = pub_images / src_file.name
    shutil.copy2(src_file, dest_file)
    print(f"Copied {src_file.name} to public/assets/images/")

print("\nDone!")

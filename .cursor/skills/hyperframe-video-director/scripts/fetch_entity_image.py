#!/usr/bin/env python3
"""
Fetch portrait / brand images for public figures and well-known companies.

Primary source: Wikipedia / Wikimedia (portable, no API key).
Writes analysis/entity-assets.json and caches files under assets/images/entities/.

Usage:
  python fetch_entity_image.py --project videos/foo --entities analysis/entities.json
  python fetch_entity_image.py --project videos/foo --name "Swiggy" --type company --scenes 1,3
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _util import die, ensure_dir, resolve_project, write_json  # noqa: E402

UA = "hyperframe-video-director/1.0 (entity-image-fetch; educational agent skill)"
WIKI_SUMMARY = "https://en.wikipedia.org/api/rest_v1/page/summary/{title}"
WIKI_SEARCH = "https://en.wikipedia.org/w/api.php"


def http_json(url: str, timeout: int = 30) -> dict | list:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def http_bytes(url: str, timeout: int = 60) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def slug(name: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9]+", "_", name.strip()).strip("_").lower()
    return (s[:60] or "entity")


def wiki_search_title(name: str) -> str | None:
    params = urllib.parse.urlencode(
        {
            "action": "opensearch",
            "search": name,
            "limit": 5,
            "namespace": 0,
            "format": "json",
        }
    )
    data = http_json(f"{WIKI_SEARCH}?{params}")
    # [query, [titles], [descs], [urls]]
    if isinstance(data, list) and len(data) > 1 and data[1]:
        return data[1][0]
    return None


def wiki_summary(title: str) -> dict | None:
    enc = urllib.parse.quote(title.replace(" ", "_"), safe="")
    url = WIKI_SUMMARY.format(title=enc)
    try:
        return http_json(url)  # type: ignore[return-value]
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise


def pick_image_url(summary: dict) -> tuple[str | None, str | None]:
    """Return (image_url, page_url). Prefer originalimage, else thumbnail."""
    page = summary.get("content_urls", {}).get("desktop", {}).get("page") or summary.get("url")
    orig = summary.get("originalimage") or {}
    thumb = summary.get("thumbnail") or {}
    url = orig.get("source") or thumb.get("source")
    return url, page


def commons_file_url(file_title: str) -> str | None:
    """Resolve a Commons File: title to a direct image URL."""
    params = urllib.parse.urlencode(
        {
            "action": "query",
            "titles": file_title,
            "prop": "imageinfo",
            "iiprop": "url",
            "format": "json",
        }
    )
    data = http_json(f"https://commons.wikimedia.org/w/api.php?{params}")
    pages = (data.get("query") or {}).get("pages") or {}
    for page in pages.values():
        infos = page.get("imageinfo") or []
        if infos and infos[0].get("url"):
            return infos[0]["url"]
    return None


def commons_search_image(name: str, etype: str) -> dict | None:
    """Search Wikimedia Commons for a logo/portrait file."""
    queries = [f"{name} logo", f"{name} Logo", name]
    if etype == "person":
        queries = [f"{name} portrait", f"{name} photo", name] + queries
    for q in queries:
        params = urllib.parse.urlencode(
            {
                "action": "query",
                "list": "search",
                "srsearch": q,
                "srnamespace": 6,  # File
                "srlimit": 8,
                "format": "json",
            }
        )
        data = http_json(f"https://commons.wikimedia.org/w/api.php?{params}")
        hits = ((data.get("query") or {}).get("search")) or []
        for hit in hits:
            title = hit.get("title") or ""
            if not title.startswith("File:"):
                continue
            # Prefer common image extensions
            lower = title.lower()
            if not any(lower.endswith(ext) for ext in (".png", ".jpg", ".jpeg", ".webp", ".svg")):
                continue
            url = commons_file_url(title)
            if url:
                # Skip SVG for simpler HTML <img> support unless nothing else
                if lower.endswith(".svg"):
                    continue
                return {
                    "image_url": url,
                    "page_url": f"https://commons.wikimedia.org/wiki/{urllib.parse.quote(title.replace(' ', '_'))}",
                    "wiki_title": title,
                    "source": "commons",
                    "query": q,
                }
        # second pass allow svg
        for hit in hits:
            title = hit.get("title") or ""
            if title.lower().endswith(".svg"):
                url = commons_file_url(title)
                if url:
                    return {
                        "image_url": url,
                        "page_url": f"https://commons.wikimedia.org/wiki/{urllib.parse.quote(title.replace(' ', '_'))}",
                        "wiki_title": title,
                        "source": "commons",
                        "query": q,
                    }
    return None


def fetch_one(name: str, etype: str) -> dict:
    """Resolve one entity to a local downloadable image URL + metadata."""
    tried: list[str] = []
    titles = [name]
    found = wiki_search_title(name)
    if found and found not in titles:
        titles.append(found)
    if etype in ("company", "organization", "brand", "product"):
        for suffix in (" (company)", " Inc.", " company"):
            cand = f"{name}{suffix}".strip()
            if cand not in titles:
                titles.append(cand)

    for t in titles:
        tried.append(f"wiki:{t}")
        try:
            summary = wiki_summary(t)
        except Exception as e:  # noqa: BLE001
            tried.append(f"wiki:{t} ERR {e}")
            summary = None
        if summary and summary.get("type") != "disambiguation":
            img, page = pick_image_url(summary)
            if img:
                return {
                    "ok": True,
                    "name": name,
                    "type": etype,
                    "wiki_title": summary.get("title") or t,
                    "image_url": img,
                    "page_url": page,
                    "extract": (summary.get("extract") or "")[:280],
                    "provider": "wikipedia",
                    "tried": tried,
                }

    tried.append("commons:search")
    try:
        commons = commons_search_image(name, etype)
    except Exception as e:  # noqa: BLE001
        tried.append(f"commons ERR {e}")
        commons = None
    if commons:
        return {
            "ok": True,
            "name": name,
            "type": etype,
            "wiki_title": commons.get("wiki_title"),
            "image_url": commons["image_url"],
            "page_url": commons.get("page_url"),
            "extract": "",
            "provider": "commons",
            "tried": tried,
        }

    return {
        "ok": False,
        "name": name,
        "type": etype,
        "tried": tried,
        "error": "no wikipedia/commons image — agent should web-search and cache_asset.py",
    }


def cache_download(project: Path, name: str, etype: str, image_url: str, usage: list[str], source_page: str) -> dict:
    ensure_dir(project / "assets" / "images" / "entities")
    ensure_dir(project / "assets" / "metadata")
    # extension from URL
    path_part = urllib.parse.urlparse(image_url).path
    ext = Path(path_part).suffix.lower()
    if ext not in (".jpg", ".jpeg", ".png", ".webp", ".gif"):
        ext = ".jpg"
    dest_name = f"entity_{slug(name)}_{etype}{ext}"
    dest = project / "assets" / "images" / "entities" / dest_name

    if not dest.is_file():
        data = http_bytes(image_url)
        if len(data) < 200:
            raise RuntimeError(f"downloaded image too small for {name}: {len(data)} bytes")
        dest.write_bytes(data)

    rel = dest.relative_to(project).as_posix()
    meta = {
        "file": rel,
        "source": source_page or image_url,
        "image_url": image_url,
        "query": f"entity:{etype}:{name}",
        "kind": "images",
        "entity": {"name": name, "type": etype},
        "usage": usage,
    }
    meta_path = project / "assets" / "metadata" / f"entity_{slug(name)}.json"
    write_json(meta_path, meta)
    return meta


def load_entities(path: Path | None, name: str | None, etype: str, scenes: str) -> list[dict]:
    if path:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
        ents = data.get("entities") if isinstance(data, dict) else data
        if not isinstance(ents, list) or not ents:
            die(f"no entities[] in {path}")
        return ents
    if not name:
        die("provide --entities file or --name")
    scene_ids = [int(x) for x in scenes.split(",") if x.strip()] if scenes else []
    return [{"name": name, "type": etype, "scene_ids": scene_ids}]


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch Wikipedia images for public entities")
    parser.add_argument("--project", required=True)
    parser.add_argument("--entities", default=None, help="analysis/entities.json")
    parser.add_argument("--name", default=None)
    parser.add_argument("--type", default="person", dest="etype", choices=("person", "company", "organization", "brand", "product", "other"))
    parser.add_argument("--scenes", default="", help="comma scene ids when using --name")
    parser.add_argument("--apply-storyboard", action="store_true", help="also patch storyboard asset_path for scene_ids")
    args = parser.parse_args()

    project = resolve_project(args.project)
    ent_path = Path(args.entities) if args.entities else project / "analysis" / "entities.json"
    if args.entities:
        ent_path = Path(args.entities)
        if not ent_path.is_file():
            # try relative to project
            alt = project / args.entities
            ent_path = alt if alt.is_file() else Path(args.entities)
    elif (project / "analysis" / "entities.json").is_file() and not args.name:
        ent_path = project / "analysis" / "entities.json"
    else:
        ent_path = None

    entities = load_entities(ent_path if ent_path and ent_path.is_file() else None, args.name, args.etype, args.scenes)

    results = []
    for ent in entities:
        name = (ent.get("name") or "").strip()
        etype = (ent.get("type") or "other").strip().lower()
        scene_ids = ent.get("scene_ids") or []
        usage = [f"scene_{int(s):02d}" for s in scene_ids] or ["entity"]
        if not name:
            continue
        print(f"resolving: {name} ({etype})")
        info = fetch_one(name, etype)
        if not info.get("ok"):
            print(f"  FAIL: {info.get('error')} tried={info.get('tried')}")
            results.append(info)
            continue
        try:
            meta = cache_download(
                project,
                name,
                etype,
                info["image_url"],
                usage,
                info.get("page_url") or "",
            )
        except Exception as e:  # noqa: BLE001
            info = {**info, "ok": False, "error": str(e)}
            print(f"  FAIL download: {e}")
            results.append(info)
            continue
        info["asset_path"] = meta["file"]
        info["scene_ids"] = scene_ids
        print(f"  OK -> {meta['file']} ({info.get('wiki_title')})")
        results.append(info)

    out = {
        "provider": "wikipedia+commons",
        "entities": results,
        "ok_count": sum(1 for r in results if r.get("ok")),
        "fail_count": sum(1 for r in results if not r.get("ok")),
    }
    out_path = project / "analysis" / "entity-assets.json"
    write_json(out_path, out)
    print(f"wrote {out_path} (ok={out['ok_count']} fail={out['fail_count']})")

    if args.apply_storyboard:
        import apply_entity_assets

        apply_entity_assets.apply(project)

    # Succeed if at least one entity resolved, or there were zero entities to fetch
    if not entities:
        return 0
    return 0 if out["ok_count"] > 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())

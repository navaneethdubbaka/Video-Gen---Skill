#!/usr/bin/env python3
"""Scaffold videos/<slug>/ project tree."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _util import die, ensure_dir, write_json  # noqa: E402


DIRS = [
    "input",
    "analysis/frames",
    "storyboard",
    "assets/images",
    "assets/videos",
    "assets/icons",
    "assets/screenshots",
    "assets/metadata",
    "composition/hyperframes",
    "renders/draft",
    "renders/final",
    "qa",
]


def slugify(s: str) -> str:
    s = s.strip().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    if not s:
        die("slug empty after normalization")
    return s


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--slug", required=True)
    parser.add_argument("--root", default="videos", help="Root directory for projects")
    parser.add_argument("--force", action="store_true", help="Allow existing directory")
    args = parser.parse_args()

    slug = slugify(args.slug)
    root = Path(args.root).expanduser().resolve()
    project = root / slug

    if project.exists() and not args.force:
        # idempotent: ensure dirs
        for d in DIRS:
            ensure_dir(project / d)
        print(f"project ready (existing): {project}")
        return 0

    ensure_dir(project)
    for d in DIRS:
        ensure_dir(project / d)

    write_json(
        project / "project.json",
        {
            "slug": slug,
            "skill": "hyperframe-video-director",
            "status": "initialized",
        },
    )
    print(f"project created: {project}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

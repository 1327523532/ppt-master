#!/usr/bin/env python3
"""
PPT Master - Icon Sync

Fetch chosen library icons into a project's own `icons/` folder at the moment
they are selected. The full SVG libraries no longer ship with the skill — only a
per-library name index does — so each icon is downloaded on demand from the
remote base URL (ICON_BASE_URL) into `<project>/icons/<lib>/`. Any name absent
from the index is reported on the spot and the command exits non-zero — so you
re-pick a valid icon then, not at export time. Over-fetching candidates is fine:
finalize only embeds the icons actually referenced by `<use data-icon>`.

Custom icons you place in `<project>/icons/<lib>/` yourself are honored too — a
name already present in the project is treated as satisfied, not fetched. Names
that exist in the index but fail to download (network / config) are reported
separately as fetch failures, distinct from missing.

Usage:
    python3 scripts/icon_sync.py <project_path> <lib/name> [<lib/name> ...]

Examples:
    python3 scripts/icon_sync.py projects/deck chunk-filled/home tabler-outline/chart
    python3 scripts/icon_sync.py projects/deck simple-icons/github

Dependencies:
    None (standard library only).

See references/executor-base.md §4 and templates/icons/README.md.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Optional

from icons.fetch import fetch_icon
from icons.index import has_icon

_LIB_ALIASES = {"chunk": "chunk-filled"}
_INDEX_DIR = Path(__file__).resolve().parent.parent / "templates" / "icons" / "index"


def _split_name(icon_name: str) -> tuple[str, str]:
    """`lib/name` -> (lib, name), applying the chunk→chunk-filled alias."""
    if "/" not in icon_name:
        # legacy un-prefixed names live in chunk-filled/
        return "chunk-filled", icon_name
    lib, name = icon_name.split("/", 1)
    return _LIB_ALIASES.get(lib, lib), name


def sync_icons(project_path: Path, icon_names: list[str]) -> tuple[list[str], list[str], list[str]]:
    """Resolve each `lib/name` into `<project>/icons/`, fetching on demand.

    Resolution order per icon:
      1. already in the project (custom icon or previously fetched) -> satisfied.
      2. not in the library name index -> missing (mistyped / nonexistent).
      3. in the index -> fetch the SVG from the remote base URL into the project.

    Returns (copied, missing, failed). `failed` holds icons that exist in the
    index but could not be fetched (network / non-SVG response) — distinct from
    `missing`. Raises RuntimeError if ICON_BASE_URL is unset but a fetch is
    needed, so the caller surfaces a clear config error.
    """
    project_icons = project_path / "icons"
    copied: list[str] = []
    missing: list[str] = []
    failed: list[str] = []

    for raw in icon_names:
        lib, name = _split_name(raw)
        dst = project_icons / lib / f"{name}.svg"
        if dst.is_file():
            copied.append(f"{lib}/{name} (already in project)")
        elif not has_icon(lib, name):
            missing.append(f"{lib}/{name}")
        elif fetch_icon(lib, name, project_icons):
            copied.append(f"{lib}/{name}")
        else:
            failed.append(f"{lib}/{name}")

    return copied, missing, failed


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Copy chosen library icons into a project's icons/ folder; report missing ones.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("project_path", help="Project directory")
    parser.add_argument("icons", nargs="+", help="Icon names to copy, e.g. chunk-filled/home")
    return parser


def main(argv: Optional[list[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    project = Path(args.project_path)
    if not project.is_dir():
        print(f"[ERROR] project not found: {project}", file=sys.stderr)
        return 1

    try:
        copied, missing, failed = sync_icons(project, args.icons)
    except RuntimeError as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 1

    if copied:
        print(f"[OK] {len(copied)} icon(s) in {project / 'icons'}:", file=sys.stderr)
        for c in copied:
            print(f"     + {c}", file=sys.stderr)

    if missing:
        print(f"\n[MISSING] {len(missing)} icon(s) not in the library — re-pick before continuing:", file=sys.stderr)
        for m in missing:
            lib = m.split("/", 1)[0]
            print(f"     ✗ {m}   (search: grep <keyword> {_INDEX_DIR}/{lib}.txt)", file=sys.stderr)

    if failed:
        print(f"\n[FETCH FAILED] {len(failed)} icon(s) exist but could not be fetched — check network / ICON_BASE_URL, then retry:", file=sys.stderr)
        for f in failed:
            print(f"     ⚠ {f}", file=sys.stderr)

    return 1 if (missing or failed) else 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""
PPT Master - Icon Index Builder (build-time tool, NOT shipped with the skill)

Scans the raw SVG icon source and writes one plain-text name index per library
to skills/ppt-master/templates/icons/index/<lib>.txt (one icon name per line,
sorted, without the .svg suffix). Strategist greps these indexes to discover
icon names; the raw SVGs themselves are fetched on demand from a remote URL at
selection time, so they no longer ship with the skill.

This lives under repo-root tools/ on purpose: it runs only when the icon source
changes (regenerate, then commit the indexes). It is never invoked by the
generation pipeline and is excluded from the packaged skill.

Usage:
    python3 tools/build_icon_index.py [--source <dir>] [--out <dir>]

Examples:
    python3 tools/build_icon_index.py
    python3 tools/build_icon_index.py --source icon-source --out skills/ppt-master/templates/icons/index

Dependencies:
    None (only uses standard library).

See .kiro/specs/icon-cdn-on-demand/design.md and skills/ppt-master/templates/icons/README.md.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Optional

_REPO_ROOT = Path(__file__).resolve().parent.parent
_SKILL_DIR = _REPO_ROOT / "skills" / "ppt-master"
# raw SVGs live at repo-root icon-source/ (out of the packaged skill path); the
# generated indexes ship under the skill's templates/icons/index/.
_DEFAULT_SOURCE = _REPO_ROOT / "icon-source"
_DEFAULT_OUT = _SKILL_DIR / "templates" / "icons" / "index"

# subdirectories under source that are not icon libraries
_SKIP_DIRS = {"index"}


def discover_libraries(source: Path) -> list[str]:
    """Return sorted lib names: source subdirs that hold at least one .svg."""
    libs: list[str] = []
    for child in sorted(source.iterdir()):
        if not child.is_dir() or child.name in _SKIP_DIRS:
            continue
        if any(child.glob("*.svg")):
            libs.append(child.name)
    return libs


def icon_names(lib_dir: Path) -> list[str]:
    """Sorted icon names (filename without .svg) in a library directory."""
    return sorted(p.stem for p in lib_dir.glob("*.svg"))


def build_index(source: Path, out_dir: Path) -> dict[str, int]:
    """Write <out_dir>/<lib>.txt for every library; return {lib: count}."""
    out_dir.mkdir(parents=True, exist_ok=True)
    counts: dict[str, int] = {}
    for lib in discover_libraries(source):
        names = icon_names(source / lib)
        text = "\n".join(names) + "\n" if names else ""
        (out_dir / f"{lib}.txt").write_text(text, encoding="utf-8")
        counts[lib] = len(names)
    return counts


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Build per-library icon name indexes from the SVG source.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--source", type=Path, default=_DEFAULT_SOURCE,
        help=f"Icon source directory (default: {_DEFAULT_SOURCE})",
    )
    parser.add_argument(
        "--out", type=Path, default=_DEFAULT_OUT,
        help=f"Index output directory (default: {_DEFAULT_OUT})",
    )
    return parser


def main(argv: Optional[list[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    source: Path = args.source
    if not source.is_dir():
        print(f"[ERROR] source not found: {source}", file=sys.stderr)
        return 1

    counts = build_index(source, args.out)
    if not counts:
        print(f"[ERROR] no icon libraries found under {source}", file=sys.stderr)
        return 1

    total = sum(counts.values())
    print(f"[OK] wrote {len(counts)} index file(s) to {args.out}:", file=sys.stderr)
    for lib, n in counts.items():
        print(f"     {lib}.txt  {n}", file=sys.stderr)
    print(f"     total       {total}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

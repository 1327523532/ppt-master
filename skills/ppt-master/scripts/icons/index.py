#!/usr/bin/env python3
"""
PPT Master - Icon Name Index (runtime, shipped with the skill)

Reads the per-library name indexes at templates/icons/index/<lib>.txt — one icon
name per line, no .svg suffix — produced by tools/build_icon_index.py. The raw
SVGs no longer ship with the skill, so callers use this index to tell whether a
requested icon name is real before fetching it on demand. has_icon() backs the
icon_sync gate: a name absent from the index is a mistyped / nonexistent icon, a
name present means it can be fetched from the remote base URL.

Dependencies:
    None (standard library only).

See .kiro/specs/icon-cdn-on-demand/design.md and templates/icons/README.md.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

_INDEX_DIR = Path(__file__).resolve().parent.parent.parent / "templates" / "icons" / "index"


@lru_cache(maxsize=None)
def load_index(lib: str) -> frozenset[str]:
    """read templates/icons/index/<lib>.txt -> set of names (no .svg).

    missing index file -> empty set (treated as unknown library, not an error)."""
    path = _INDEX_DIR / f"{lib}.txt"
    if not path.is_file():
        return frozenset()
    names = (line.strip() for line in path.read_text(encoding="utf-8").splitlines())
    return frozenset(n for n in names if n)


def has_icon(lib: str, name: str) -> bool:
    """True if `name` is listed in library `lib`'s name index."""
    return name in load_index(lib)

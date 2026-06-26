#!/usr/bin/env python3
"""
PPT Master - Export-time On-demand Icon Fetch (runtime, shipped with the skill)

Glue used only by the export pipeline (embed_icons / use_expander) to pull an
icon that is missing from the project on demand. It sits on top of icons.fetch:
it splits a `lib/name` placeholder, fetches the SVG into the project icons dir,
and — unlike selection-time icon_sync — swallows a missing-config error so a deck
still exports with a placeholder instead of aborting (Req 5.2).

Keeping this in its own module isolates the CDN-on-demand additions from the
original embed_icons resolver, so the fallback is easy to find and maintain.

Dependencies:
    None (standard library only; delegates HTTP to icons.fetch).

See .kiro/specs/icon-cdn-on-demand/design.md.
"""

from __future__ import annotations

from pathlib import Path

from .fetch import fetch_icon


def _lib_and_name(icon_name: str) -> tuple[str, str]:
    """Split `lib/name` into a canonical (lib, name).

    Un-prefixed names map to the legacy chunk-filled/ library; the 'chunk' alias
    resolves to 'chunk-filled' — mirroring embed_icons._resolve_in_dir.
    """
    if "/" in icon_name:
        lib, name = icon_name.split("/", 1)
        return ("chunk-filled" if lib == "chunk" else lib), name
    return "chunk-filled", icon_name


def fetch_missing_icon(icon_name: str, dest_dir: Path) -> bool:
    """fetch a missing `icon_name` into dest_dir/<lib>/<name>.svg on demand.

    returns True when the icon was fetched. unknown libs and network/non-SVG
    failures return False; a missing ICON_BASE_URL is swallowed (placeholder
    retained) so export never aborts on it."""
    lib, name = _lib_and_name(icon_name)
    try:
        return fetch_icon(lib, name, dest_dir)
    except RuntimeError:
        return False

#!/usr/bin/env python3
"""
PPT Master - On-demand Icon Fetch (runtime, shipped with the skill)

The raw SVG icon libraries no longer ship with the skill; only the name indexes
do (see icons/index.py). This module is the single place that pulls one real SVG
from the remote base URL on demand, into a project's own icons/ folder. It is
shared by icon_sync.py (selection time) and the export-time fallback in
embed_icons / use_expander.

URL rule: <ICON_BASE_URL>/<lib>/<name>.svg, e.g.
    https://cowork.lenovo.com/ppt-icon/chunk-filled/home.svg

Only the five known libraries are fetched remotely; any other prefix (e.g.
custom/) returns False without a request so project-local resolution still wins.

Dependencies:
    None (standard library urllib only; mirrors latex_render.py).

See .kiro/specs/icon-cdn-on-demand/design.md and templates/icons/README.md.
"""

from __future__ import annotations

import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

# scripts/ on sys.path so `from config import ...` resolves (same idiom as
# svg_to_pptx/use_expander.py); fetch.py lives in scripts/icons/.
_SCRIPTS_DIR = Path(__file__).resolve().parent.parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

from config import load_prefixed_env_file  # noqa: E402

KNOWN_LIBS = {
    "chunk-filled", "tabler-filled", "tabler-outline",
    "phosphor-duotone", "simple-icons",
}

_ENV_PREFIXES = ("ICON_",)
_TIMEOUT = 30


def icon_base_url() -> str | None:
    """read ICON_BASE_URL via config.load_prefixed_env_file; strip trailing '/'.

    returns None when the variable is not configured (callers raise a clear
    config error only when a remote fetch is actually needed)."""
    load_prefixed_env_file(_ENV_PREFIXES)
    base = os.environ.get("ICON_BASE_URL", "").strip()
    return base.rstrip("/") or None


def fetch_icon(lib: str, name: str, dest_dir: Path) -> bool:
    """download <base>/<lib>/<name>.svg into dest_dir/<lib>/<name>.svg.

    returns True on success. unknown libs (e.g. custom/) -> False, no request.
    raises RuntimeError when ICON_BASE_URL is unset but a fetch is needed, so the
    caller surfaces a clear config error instead of failing silently. network /
    non-200 / non-SVG responses -> False (nothing written)."""
    if lib not in KNOWN_LIBS:
        return False

    base = icon_base_url()
    if base is None:
        raise RuntimeError(
            "ICON_BASE_URL is not set; cannot fetch remote icons. "
            "Set it in your .env (e.g. ICON_BASE_URL=https://cowork.lenovo.com/ppt-icon)."
        )

    url = f"{base}/{lib}/{name}.svg"
    req = urllib.request.Request(url)
    token = os.environ.get("ICON_AUTH_TOKEN", "").strip()
    if token:
        req.add_header("Authorization", f"Bearer {token}")

    try:
        with urllib.request.urlopen(req, timeout=_TIMEOUT) as resp:
            data = resp.read()
    except (urllib.error.URLError, TimeoutError):
        return False

    # guard against HTML error pages served with 200; real SVGs carry a <svg
    # root, possibly after an <?xml?> declaration or comment.
    if b"<svg" not in data[:512]:
        return False

    out_path = dest_dir / lib / f"{name}.svg"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(data)
    return True

#!/usr/bin/env python3
"""
PPT Master - Local Icon CDN Server (dev/test tool, NOT shipped with the skill)

Serves the raw SVG icon source over HTTP so the on-demand fetch path can be
exercised without the real icon host. It maps GET /<lib>/<name>.svg straight to
<lib>/<name>.svg under the served directory, which is exactly the
<ICON_BASE_URL>/<lib>/<name>.svg rule icons.fetch expects — so pointing
ICON_BASE_URL at this server is enough to run the whole pipeline
(icon_sync -> finalize_svg -> svg_to_pptx) locally.

The icon source is committed as icon-source/icon-source.zip (one archive instead
of ~11k loose SVGs). On startup this script extracts that zip into .icon-cache/
at the repo root and serves the extracted copy. The cache is refreshed whenever
the zip changes and is git-ignored. Pass --source <dir> to serve a raw icon
directory directly and skip extraction.

This lives under repo-root tools/ on purpose: it is a maintainer/teammate test
helper, never invoked by the generation pipeline and excluded from the package.

Usage:
    python3 tools/icon_cdn_server.py [--source <dir>] [--host H] [--port P]

Examples:
    python3 tools/icon_cdn_server.py
    python3 tools/icon_cdn_server.py --port 8123
    # then, in another shell / your .env:
    #   ICON_BASE_URL=http://127.0.0.1:8123

Dependencies:
    None (standard library only).

See .kiro/specs/icon-cdn-on-demand/design.md.
"""

from __future__ import annotations

import argparse
import shutil
import sys
import zipfile
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Optional

_REPO_ROOT = Path(__file__).resolve().parent.parent
_DEFAULT_ZIP = _REPO_ROOT / "icon-source" / "icon-source.zip"
_DEFAULT_CACHE = _REPO_ROOT / ".icon-cache"


class _QuietHandler(SimpleHTTPRequestHandler):
    """SimpleHTTPRequestHandler that logs one concise line per request."""

    def log_message(self, fmt: str, *args) -> None:  # noqa: A003
        sys.stderr.write(f"  {self.command} {self.path} -> {args[1]}\n")


def ensure_extracted(zip_path: Path, dest: Path) -> Path:
    """extract zip_path into dest, refreshing only when the zip changed."""
    stamp = dest / ".zip-mtime"
    zip_mtime = str(zip_path.stat().st_mtime_ns)
    if stamp.is_file() and stamp.read_text() == zip_mtime:
        return dest
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True)
    with zipfile.ZipFile(zip_path) as zf:
        zf.extractall(dest)
    stamp.write_text(zip_mtime)
    return dest


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Serve the icon source as a local icon CDN for testing.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--source", type=Path, default=None,
        help="Raw icon directory to serve directly, skipping zip extraction "
             f"(default: extract {_DEFAULT_ZIP} into {_DEFAULT_CACHE})",
    )
    parser.add_argument("--host", default="127.0.0.1", help="Bind host (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=8000, help="Bind port (default: 8000)")
    return parser


def main(argv: Optional[list[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    if args.source is not None:
        source: Path = args.source
    elif _DEFAULT_ZIP.is_file():
        print(f"[OK] extracting {_DEFAULT_ZIP} -> {_DEFAULT_CACHE}", file=sys.stderr)
        source = ensure_extracted(_DEFAULT_ZIP, _DEFAULT_CACHE)
    else:
        print(f"[ERROR] icon source zip not found: {_DEFAULT_ZIP}", file=sys.stderr)
        return 1
    if not source.is_dir():
        print(f"[ERROR] icon source not found: {source}", file=sys.stderr)
        return 1

    handler = partial(_QuietHandler, directory=str(source))
    server = ThreadingHTTPServer((args.host, args.port), handler)
    base_url = f"http://{args.host}:{server.server_address[1]}"
    print(f"[OK] serving {source} at {base_url}", file=sys.stderr)
    print(f"     set ICON_BASE_URL={base_url}", file=sys.stderr)
    print("     Ctrl-C to stop", file=sys.stderr)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[OK] stopped", file=sys.stderr)
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

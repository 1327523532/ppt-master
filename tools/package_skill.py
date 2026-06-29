#!/usr/bin/env python3
"""
PPT Master - Skill Packager (dev tool, NOT shipped with the skill)

One-shot packaging of skills/ppt-master/ into a clean tarball — plus an identical
uncompressed folder alongside it — ready to drop into an agent's skill install
dir. It excludes build/runtime junk (__pycache__, *.pyc,
.DS_Store) and any real .env (secrets) while keeping .env.example, then
self-checks the archive: no bulk icon SVGs slipped in, the name indexes are
present, and no .env leaked. Icons are fetched on demand at runtime, so the
package must carry only templates/icons/index/ — never the SVG libraries.

Usage:
    python3 tools/package_skill.py [-o <output.tar.gz>]

Examples:
    python3 tools/package_skill.py
    python3 tools/package_skill.py -o /tmp/ppt-master-skill.tar.gz

Dependencies:
    None (standard library only).

See skills/ppt-master/scripts/icons/CHANGES.md.
"""

from __future__ import annotations

import argparse
import io
import shutil
import sys
import tarfile
import time
from pathlib import Path
from typing import Optional

_REPO_ROOT = Path(__file__).resolve().parent.parent
_SKILL_DIR = _REPO_ROOT / "skills" / "ppt-master"
_DEFAULT_OUT = _REPO_ROOT / "dist" / "ppt-master-skill.tar.gz"

_EXCLUDE_DIRS = {"__pycache__"}
_EXCLUDE_NAMES = {".DS_Store", ".env"}  # source .env = real secrets; never bundled
_EXCLUDE_SUFFIXES = {".pyc", ".pyo"}

# A minimal .env shipped in the package with REQUIRED config only — edit the
# value after unpacking. Optional backends (image / TTS / search) stay in
# .env.example to keep this file short and unambiguous.
_MIN_ENV = """\
# ─────────────────────────────────────────────────────────────
# PPT Master — required runtime config / 必配项
# Read at <skill-dir>/.env. Optional backends (image generation /
# TTS / web image search) live in .env.example.
# 可选后端（生图 / 配音 / 网络图搜）见 .env.example。
# ─────────────────────────────────────────────────────────────

# REQUIRED — remote icon host. Icons are fetched on demand from
# <ICON_BASE_URL>/<lib>/<name>.svg. Change to your icon host.
# 必配 — 图标托管地址，按需拉取图标用。改成你的地址。
ICON_BASE_URL=https://employeecowork-test.lenovo.com/skillicons

# Optional — bearer token if the icon host requires auth.
# 可选 — 图标托管需要鉴权时填。
# ICON_AUTH_TOKEN=
"""


def _excluded(path: Path) -> bool:
    """True if a path should be left out of the package."""
    if path.name in _EXCLUDE_NAMES:
        return True
    if path.suffix in _EXCLUDE_SUFFIXES:
        return True
    return any(part in _EXCLUDE_DIRS for part in path.parts)


def _add_min_env(tar: tarfile.TarFile) -> None:
    """Bundle a minimal required-only .env (edit the value after unpacking)."""
    data = _MIN_ENV.encode("utf-8")
    info = tarfile.TarInfo(name="ppt-master/.env")
    info.size = len(data)
    info.mtime = int(time.time())
    info.mode = 0o644
    tar.addfile(info, io.BytesIO(data))


def build_archive(skill_dir: Path, out_path: Path) -> int:
    """Write the cleaned tarball; return the number of files included."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with tarfile.open(out_path, "w:gz") as tar:
        for path in sorted(skill_dir.rglob("*")):
            if path.is_dir() or _excluded(path):
                continue
            tar.add(path, arcname=str(Path("ppt-master") / path.relative_to(skill_dir)))
            count += 1
        _add_min_env(tar)
        count += 1
    return count


def build_tree(skill_dir: Path, out_dir: Path) -> int:
    """Write the cleaned, uncompressed folder mirror of the tarball; return file count."""
    root = out_dir / "ppt-master"
    if out_dir.exists():
        shutil.rmtree(out_dir)
    count = 0
    for path in sorted(skill_dir.rglob("*")):
        if path.is_dir() or _excluded(path):
            continue
        dest = root / path.relative_to(skill_dir)
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, dest)
        count += 1
    (root / ".env").write_text(_MIN_ENV, encoding="utf-8")
    count += 1
    return count


def _check_members(members: list[str], env_text: str) -> list[str]:
    """Shared self-check over a list of member paths and the bundled .env text."""
    problems: list[str] = []
    icons_prefix = "ppt-master/templates/icons/"
    stray_svgs = [m for m in members if m.startswith(icons_prefix) and m.endswith(".svg")]
    indexes = [m for m in members if m.startswith(icons_prefix + "index/") and m.endswith(".txt")]
    env_members = [m for m in members if Path(m).name == ".env"]

    if stray_svgs:
        problems.append(f"{len(stray_svgs)} icon SVG(s) leaked into the package (should be 0): {stray_svgs[:3]} ...")
    if len(indexes) < 5:
        problems.append(f"expected 5 name-index files, found {len(indexes)}")
    if env_members != ["ppt-master/.env"]:
        problems.append(f"expected exactly the bundled ppt-master/.env, found {env_members}")
    if "ICON_BASE_URL" not in env_text:
        problems.append("bundled .env is missing the required ICON_BASE_URL")
    # defense: the bundled .env must carry no real secret values
    secret_leak = [ln for ln in env_text.splitlines()
                   if not ln.lstrip().startswith("#")
                   and any(k in ln for k in ("API_KEY", "SECRET", "TOKEN="))]
    if secret_leak:
        problems.append(f"bundled .env carries secret-looking values: {secret_leak}")
    return problems


def verify_archive(out_path: Path) -> list[str]:
    """Return a list of problems found in the built archive (empty = OK)."""
    with tarfile.open(out_path, "r:gz") as tar:
        members = [m.name for m in tar.getmembers() if m.isfile()]
        env_member = tar.extractfile("ppt-master/.env")
        env_text = env_member.read().decode("utf-8") if env_member else ""
    return _check_members(members, env_text)


def verify_tree(out_dir: Path) -> list[str]:
    """Return a list of problems found in the built folder (empty = OK)."""
    root = out_dir / "ppt-master"
    members = [
        "ppt-master/" + str(p.relative_to(root)).replace("\\", "/")
        for p in sorted(out_dir.rglob("*")) if p.is_file()
    ]
    env_file = root / ".env"
    env_text = env_file.read_text(encoding="utf-8") if env_file.is_file() else ""
    return _check_members(members, env_text)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Package skills/ppt-master/ into a clean, install-ready tarball.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "-o", "--output", type=Path, default=_DEFAULT_OUT,
        help=f"Output tarball path (default: {_DEFAULT_OUT})",
    )
    return parser


def main(argv: Optional[list[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    if not _SKILL_DIR.is_dir():
        print(f"[ERROR] skill dir not found: {_SKILL_DIR}", file=sys.stderr)
        return 1

    out_path: Path = args.output
    # uncompressed folder mirror, alongside the tarball (strip the archive suffix)
    name = out_path.name
    for suffix in (".tar.gz", ".tgz", ".tar"):
        if name.endswith(suffix):
            name = name[: -len(suffix)]
            break
    out_dir = out_path.with_name(name)

    count = build_archive(_SKILL_DIR, out_path)
    problems = verify_archive(out_path)
    tree_count = build_tree(_SKILL_DIR, out_dir)
    problems += verify_tree(out_dir)

    size_mb = out_path.stat().st_size / (1024 * 1024)
    print(f"[OK] packaged {count} file(s) -> {out_path} ({size_mb:.1f} MB)", file=sys.stderr)
    print(f"[OK] packaged {tree_count} file(s) -> {out_dir}/ (uncompressed folder)", file=sys.stderr)
    if problems:
        print("[FAIL] self-check found problems:", file=sys.stderr)
        for p in problems:
            print(f"     ✗ {p}", file=sys.stderr)
        return 1

    print("[OK] self-check passed: no icon SVGs bundled, 5 name indexes present, minimal .env carries only ICON_BASE_URL.", file=sys.stderr)
    print(f"\nNext: unpack into your agent's skill dir, then edit the bundled .env:\n"
          f"     tar -xzf {out_path} -C ~/.agents/skills\n"
          f"     # or copy the folder directly: cp -r {out_dir}/ppt-master ~/.agents/skills/\n"
          f"     # edit ~/.agents/skills/ppt-master/.env -> set ICON_BASE_URL to your icon host",
          file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

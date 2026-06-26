#!/usr/bin/env python3
"""Shared schema and hash helpers for PPT Master visual-review artifacts."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


RENDER_MANIFEST_SCHEMA = "ppt-master.visual-review.render-manifest.v1"
PAGE_REVIEW_SCHEMA = "ppt-master.visual-review.page.v1"
SUMMARY_SCHEMA = "ppt-master.visual-review.summary.v1"


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def sha256_file(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def sha256_json(data: dict[str, Any]) -> str:
    payload = json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def read_json_object(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as fh:
        data = json.load(fh)
    if not isinstance(data, dict):
        raise ValueError("top-level JSON must be an object")
    return data


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def review_dir(project_dir: Path) -> Path:
    return project_dir / ".review"


def render_manifest_path(project_dir: Path) -> Path:
    return review_dir(project_dir) / "render_manifest.json"


def visual_review_summary_path(project_dir: Path) -> Path:
    return review_dir(project_dir) / "visual_review_summary.md"


def visual_review_report_path(project_dir: Path) -> Path:
    return review_dir(project_dir) / "visual_review_report.json"


def gate_report_path(project_dir: Path) -> Path:
    return review_dir(project_dir) / "export_gate_report.json"


def page_review_path(project_dir: Path, stem: str) -> Path:
    return review_dir(project_dir) / f"{stem}.json"


def relpath(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return str(path)


def resolve_project_path(project_dir: Path, stored_path: str | None) -> Path | None:
    if not stored_path:
        return None
    path = Path(stored_path)
    if path.is_absolute():
        return path
    return project_dir / path


def svg_stem(page_name: str) -> str:
    return page_name[:-4] if page_name.endswith(".svg") else page_name


def load_render_manifest(project_dir: Path) -> dict[str, Any]:
    return read_json_object(render_manifest_path(project_dir))


def current_manifest_sha256(project_dir: Path) -> str:
    return sha256_file(render_manifest_path(project_dir))


def update_render_manifest(
    project_dir: Path,
    server_url: str,
    records: list[dict[str, Any]],
) -> dict[str, Any]:
    """Merge one render run into .review/render_manifest.json."""

    manifest_file = render_manifest_path(project_dir)
    if manifest_file.exists():
        try:
            manifest = read_json_object(manifest_file)
        except Exception:
            manifest = {}
    else:
        manifest = {}

    pages = manifest.get("pages")
    if not isinstance(pages, dict):
        pages = {}

    now = utc_now_iso()
    manifest = {
        "schema": RENDER_MANIFEST_SCHEMA,
        "generated_by": "visual_review.py",
        "project": str(project_dir.resolve()),
        "server_url": server_url,
        "updated_at": now,
        "pages": pages,
    }

    svg_dir = project_dir / "svg_output"
    preview_dir = project_dir / ".preview"

    for rec in records:
        page_name = str(rec.get("page", ""))
        if not page_name:
            continue
        stem = svg_stem(page_name)
        svg_path = svg_dir / page_name
        png_path = preview_dir / f"{stem}.png"

        entry: dict[str, Any] = {
            "page": stem,
            "svg_file": relpath(svg_path, project_dir),
            "ok": bool(rec.get("ok")),
            "rendered_at": now,
            "server_url": server_url,
        }
        if svg_path.is_file():
            entry["svg_sha256"] = sha256_file(svg_path)
        else:
            entry["error"] = f"missing SVG: {svg_path}"
            entry["ok"] = False

        if rec.get("ok") and png_path.is_file():
            entry.update(
                {
                    "png_file": relpath(png_path, project_dir),
                    "png_sha256": sha256_file(png_path),
                    "png_bytes": png_path.stat().st_size,
                    "all_background": bool(rec.get("all_background")),
                }
            )
        else:
            entry["error"] = rec.get("error") or entry.get("error") or "render failed"

        entry["render_id"] = sha256_json(
            {
                "page": entry.get("page"),
                "svg_sha256": entry.get("svg_sha256"),
                "png_sha256": entry.get("png_sha256"),
                "rendered_at": entry.get("rendered_at"),
            }
        )

        pages[stem] = entry

    write_json(manifest_file, manifest)
    return manifest

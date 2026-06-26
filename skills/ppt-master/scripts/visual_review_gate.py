#!/usr/bin/env python3
"""Hard gate for mandatory visual-review artifacts before export."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from visual_review_manifest import (
    PAGE_REVIEW_SCHEMA,
    RENDER_MANIFEST_SCHEMA,
    SUMMARY_SCHEMA,
    current_manifest_sha256,
    gate_report_path,
    load_render_manifest,
    page_review_path,
    read_json_object,
    render_manifest_path,
    resolve_project_path,
    sha256_file,
    utc_now_iso,
    visual_review_report_path,
    visual_review_summary_path,
    write_json,
)


ALLOWED_FINAL_STATUSES = {"ok", "fixed"}
BLOCKING_STATUSES = {"render_failed", "prereq_failed"}
USER_DECISION_STATUSES = {"resolved", "deferred"}


def _err(msg: str) -> None:
    print(msg, file=sys.stderr)


def _needs_human_resolved(data: dict[str, Any]) -> bool:
    decision = data.get("user_decision")
    if not isinstance(decision, dict):
        return False
    status = str(decision.get("status", "")).strip().lower()
    return status in USER_DECISION_STATUSES


def _summary_has_required_markers(summary_text: str, manifest_sha: str) -> bool:
    return (
        f"<!-- {SUMMARY_SCHEMA} -->" in summary_text
        and "<!-- generated_by: visual_review_aggregate.py -->" in summary_text
        and f"<!-- render_manifest_sha256: {manifest_sha} -->" in summary_text
    )


def _validate_render_manifest(project_dir: Path, svg_files: list[Path]) -> tuple[dict[str, Any] | None, str | None, list[str]]:
    errors: list[str] = []
    manifest_path = render_manifest_path(project_dir)
    if not manifest_path.is_file():
        return None, None, [
            f"missing render manifest: {manifest_path}. Run visual_review.py before export."
        ]

    try:
        manifest = load_render_manifest(project_dir)
        manifest_sha = current_manifest_sha256(project_dir)
    except Exception as exc:  # noqa: BLE001
        return None, None, [f"invalid render manifest: {manifest_path} ({exc})"]

    if manifest.get("schema") != RENDER_MANIFEST_SCHEMA:
        errors.append(
            f"render manifest schema mismatch: expected {RENDER_MANIFEST_SCHEMA}, "
            f"got {manifest.get('schema')!r}"
        )
    if manifest.get("generated_by") != "visual_review.py":
        errors.append("render manifest generated_by must be visual_review.py")

    pages = manifest.get("pages")
    if not isinstance(pages, dict):
        return manifest, manifest_sha, errors + ["render manifest pages must be an object"]

    for svg_path in svg_files:
        entry = pages.get(svg_path.stem)
        if not isinstance(entry, dict):
            errors.append(f"render manifest missing page entry for {svg_path.name}")
            continue

        if not entry.get("ok"):
            errors.append(f"render manifest marks {svg_path.name} as not rendered successfully")

        expected_svg_hash = entry.get("svg_sha256")
        actual_svg_hash = sha256_file(svg_path)
        if expected_svg_hash != actual_svg_hash:
            errors.append(
                f"render manifest is stale for {svg_path.name}: current SVG hash "
                "does not match rendered SVG hash. Re-run visual_review.py."
            )

        png_path = resolve_project_path(project_dir, entry.get("png_file"))
        if png_path is None or not png_path.is_file():
            errors.append(f"render manifest PNG missing for {svg_path.name}: {entry.get('png_file')!r}")
            continue

        expected_png_hash = entry.get("png_sha256")
        actual_png_hash = sha256_file(png_path)
        if expected_png_hash != actual_png_hash:
            errors.append(
                f"render manifest PNG hash mismatch for {svg_path.name}: re-run visual_review.py."
            )
        if entry.get("all_background"):
            errors.append(f"rendered PNG for {svg_path.name} is all-background; inspect render failure.")

    return manifest, manifest_sha, errors


def _validate_page_review(
    project_dir: Path,
    svg_path: Path,
    manifest_entry: dict[str, Any] | None,
) -> list[str]:
    errors: list[str] = []
    review_json = page_review_path(project_dir, svg_path.stem)
    if not review_json.is_file():
        return [f"missing visual-review result for {svg_path.name}: {review_json}"]

    try:
        data = read_json_object(review_json)
    except Exception as exc:  # noqa: BLE001
        return [f"invalid visual-review JSON for {svg_path.name}: {review_json} ({exc})"]

    if data.get("schema") != PAGE_REVIEW_SCHEMA:
        errors.append(
            f"{review_json.name} schema mismatch: expected {PAGE_REVIEW_SCHEMA}. "
            "Do not use legacy placeholder review JSON."
        )
    if str(data.get("page", "")) != svg_path.stem:
        errors.append(f"{review_json.name} page field must be {svg_path.stem!r}")
    render = data.get("render")
    if not isinstance(render, dict):
        errors.append(f"{review_json.name} missing render object with render_id and SVG/PNG hashes")
        render = {}

    if manifest_entry:
        if render.get("render_id") != manifest_entry.get("render_id"):
            errors.append(f"{review_json.name} render_id does not match render manifest")
        if render.get("svg_sha256") != manifest_entry.get("svg_sha256"):
            errors.append(f"{review_json.name} SVG hash does not match render manifest")
        if render.get("png_sha256") != manifest_entry.get("png_sha256"):
            errors.append(f"{review_json.name} PNG hash does not match render manifest")

    status = str(data.get("status", "")).strip().lower()
    if status in BLOCKING_STATUSES:
        errors.append(
            f"visual-review status for {svg_path.name} is blocking: {status}. "
            "Fix the render/static prerequisite issue and re-run visual review."
        )
    elif status == "needs_human":
        if not _needs_human_resolved(data):
            errors.append(
                f"visual-review status for {svg_path.name} is needs_human without "
                "a recorded user_decision.status=resolved|deferred."
            )
    elif status not in ALLOWED_FINAL_STATUSES:
        errors.append(
            f"visual-review status for {svg_path.name} is invalid for export: {status or '<missing>'}"
        )

    if review_json.stat().st_mtime < svg_path.stat().st_mtime:
        errors.append(
            f"stale visual-review result for {svg_path.name}: "
            f"{review_json.name} is older than the SVG. Re-run visual review."
        )

    return errors


def validate_visual_review_gate(project_dir: Path, require_summary: bool = True) -> list[str]:
    project_dir = project_dir.resolve()
    errors: list[str] = []
    svg_output = project_dir / "svg_output"
    review_dir = project_dir / ".review"

    if not svg_output.is_dir():
        return [f"svg_output directory not found: {svg_output}"]

    svg_files = sorted(svg_output.glob("*.svg"))
    if not svg_files:
        return [f"no SVG files found in {svg_output}"]

    if not review_dir.is_dir():
        return [
            f"missing visual-review directory: {review_dir}. "
            "Run workflows/visual-review.md before export."
        ]

    manifest, manifest_sha, manifest_errors = _validate_render_manifest(project_dir, svg_files)
    errors.extend(manifest_errors)
    pages = manifest.get("pages") if isinstance(manifest, dict) else {}
    if not isinstance(pages, dict):
        pages = {}

    if manifest_sha:
        for svg_path in svg_files:
            entry = pages.get(svg_path.stem)
            errors.extend(
                _validate_page_review(
                    project_dir,
                    svg_path,
                    entry if isinstance(entry, dict) else None,
                )
            )

    if require_summary:
        summary_path = visual_review_summary_path(project_dir)
        if not summary_path.is_file():
            errors.append(
                f"missing visual-review summary: {summary_path}. "
                "Run visual_review_aggregate.py before export."
            )
        elif manifest_sha:
            try:
                summary_text = summary_path.read_text(encoding="utf-8")
            except Exception as exc:  # noqa: BLE001
                errors.append(f"cannot read visual-review summary: {summary_path} ({exc})")
            else:
                if not _summary_has_required_markers(summary_text, manifest_sha):
                    errors.append(
                        "visual-review summary was not generated by visual_review_aggregate.py "
                        "for the current render manifest."
                    )

                newest_input_mtime = render_manifest_path(project_dir).stat().st_mtime
                for svg_path in svg_files:
                    review_json = page_review_path(project_dir, svg_path.stem)
                    if review_json.is_file():
                        newest_input_mtime = max(newest_input_mtime, review_json.stat().st_mtime)
                if summary_path.stat().st_mtime < newest_input_mtime:
                    errors.append(
                        f"stale visual-review summary: {summary_path} is older than "
                        "render manifest or per-page review JSON files."
                    )

    return errors


def build_gate_report(project_dir: Path, require_summary: bool = True) -> dict[str, Any]:
    errors = validate_visual_review_gate(project_dir, require_summary=require_summary)
    return {
        "schema": "ppt-master.visual-review.export-gate-report.v1",
        "generated_by": "visual_review_gate.py",
        "generated_at": utc_now_iso(),
        "project": str(project_dir.resolve()),
        "ok": not errors,
        "allowed_to_export": not errors,
        "blocking_errors": errors,
        "render_manifest": str(render_manifest_path(project_dir)),
        "visual_review_summary": str(visual_review_summary_path(project_dir)),
        "visual_review_report": str(visual_review_report_path(project_dir)),
    }


def write_gate_report(project_dir: Path, require_summary: bool = True) -> dict[str, Any]:
    report = build_gate_report(project_dir, require_summary=require_summary)
    write_json(gate_report_path(project_dir), report)
    return report


def enforce_visual_review_gate(project_dir: Path, command_name: str) -> bool:
    report = write_gate_report(project_dir)
    if report["ok"]:
        return True

    _err(f"[ERROR] Visual review gate failed for {command_name}:")
    for item in report["blocking_errors"]:
        _err(f"  - {item}")
    _err(f"Machine report: {gate_report_path(project_dir)}")
    _err("Export blocked. Complete or refresh workflows/visual-review.md and retry.")
    return False


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate visual-review export gate artifacts.")
    parser.add_argument("project_path", help="Path to project directory")
    parser.add_argument("--no-summary", action="store_true", help="Do not require aggregate summary")
    parser.add_argument("--write-report", action="store_true", help="Write .review/export_gate_report.json")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON report")
    args = parser.parse_args()

    project_dir = Path(args.project_path).resolve()
    report = (
        write_gate_report(project_dir, require_summary=not args.no_summary)
        if args.write_report
        else build_gate_report(project_dir, require_summary=not args.no_summary)
    )
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False, sort_keys=True))
    else:
        if report["ok"]:
            print("visual-review gate: ok")
        else:
            print("visual-review gate: failed", file=sys.stderr)
            for item in report["blocking_errors"]:
                print(f"  - {item}", file=sys.stderr)
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())

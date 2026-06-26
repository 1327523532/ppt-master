#!/usr/bin/env python3
"""Aggregate verified per-page visual-review JSON into export-gate artifacts."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from visual_review_gate import build_gate_report, validate_visual_review_gate
from visual_review_manifest import (
    SUMMARY_SCHEMA,
    current_manifest_sha256,
    page_review_path,
    read_json_object,
    utc_now_iso,
    visual_review_report_path,
    visual_review_summary_path,
    write_json,
)


def _cell(value: Any) -> str:
    text = "" if value is None else str(value)
    return text.replace("|", "\\|").replace("\n", " ").strip()


def _count_items(data: dict[str, Any], key: str) -> int:
    value = data.get(key)
    return len(value) if isinstance(value, list) else 0


def build_summary(project_dir: Path) -> tuple[str, dict[str, Any]]:
    project_dir = project_dir.resolve()
    manifest_sha = current_manifest_sha256(project_dir)
    rows: list[dict[str, Any]] = []
    status_counts: dict[str, int] = {}

    for svg_path in sorted((project_dir / "svg_output").glob("*.svg")):
        review_path = page_review_path(project_dir, svg_path.stem)
        data = read_json_object(review_path)
        status = str(data.get("status", "")).strip().lower()
        status_counts[status] = status_counts.get(status, 0) + 1
        rows.append(
            {
                "page": svg_path.stem,
                "role": data.get("role") or data.get("page_role") or "",
                "status": status,
                "hard_hits": _count_items(data, "hard_hits"),
                "soft_hits": _count_items(data, "soft_hits"),
                "fixes_applied": _count_items(data, "fixes_applied"),
                "needs_human_reason": data.get("needs_human_reason") or "",
                "review_json": str(review_path),
            }
        )

    generated_at = utc_now_iso()
    lines = [
        f"<!-- {SUMMARY_SCHEMA} -->",
        "<!-- generated_by: visual_review_aggregate.py -->",
        f"<!-- render_manifest_sha256: {manifest_sha} -->",
        "",
        "# Visual Review Summary",
        "",
        f"- project: `{project_dir}`",
        f"- generated_at: `{generated_at}`",
        f"- pages: `{len(rows)}`",
        f"- statuses: `{json.dumps(status_counts, ensure_ascii=False, sort_keys=True)}`",
        "",
        "| page | role | status | hard_hits | soft_hits | fixes_applied | needs_human_reason |",
        "|------|------|--------|-----------|-----------|---------------|---------------------|",
    ]
    for row in rows:
        lines.append(
            "| {page} | {role} | {status} | {hard_hits} | {soft_hits} | {fixes_applied} | {needs_human_reason} |".format(
                page=_cell(row["page"]),
                role=_cell(row["role"]),
                status=_cell(row["status"]),
                hard_hits=_cell(row["hard_hits"]),
                soft_hits=_cell(row["soft_hits"]),
                fixes_applied=_cell(row["fixes_applied"]),
                needs_human_reason=_cell(row["needs_human_reason"]),
            )
        )
    lines.append("")

    report = {
        "schema": "ppt-master.visual-review.aggregate-report.v1",
        "generated_by": "visual_review_aggregate.py",
        "generated_at": generated_at,
        "project": str(project_dir),
        "render_manifest_sha256": manifest_sha,
        "ok": True,
        "pages": rows,
        "status_counts": status_counts,
        "summary": str(visual_review_summary_path(project_dir)),
    }
    return "\n".join(lines), report


def main() -> int:
    parser = argparse.ArgumentParser(description="Aggregate visual-review page JSON files.")
    parser.add_argument("project_path", help="Path to project directory")
    parser.add_argument("--json", action="store_true", help="Print machine-readable aggregate report")
    args = parser.parse_args()

    project_dir = Path(args.project_path).resolve()
    pre_errors = validate_visual_review_gate(project_dir, require_summary=False)
    if pre_errors:
        report = build_gate_report(project_dir, require_summary=False)
        report["ok"] = False
        report["allowed_to_export"] = False
        report["note"] = "summary not generated because pre-summary visual-review gate failed"
        write_json(visual_review_report_path(project_dir), report)
        if args.json:
            print(json.dumps(report, indent=2, ensure_ascii=False, sort_keys=True))
        else:
            print("visual-review aggregate failed:", file=sys.stderr)
            for item in pre_errors:
                print(f"  - {item}", file=sys.stderr)
        return 1

    summary, report = build_summary(project_dir)
    visual_review_summary_path(project_dir).write_text(summary, encoding="utf-8")
    write_json(visual_review_report_path(project_dir), report)

    final_gate = build_gate_report(project_dir, require_summary=True)
    report["export_gate"] = final_gate
    write_json(visual_review_report_path(project_dir), report)

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False, sort_keys=True))
    else:
        print(f"visual-review summary: {visual_review_summary_path(project_dir)}")
        print(f"visual-review report: {visual_review_report_path(project_dir)}")
        if not final_gate["ok"]:
            print("visual-review aggregate generated, but export gate still fails:", file=sys.stderr)
            for item in final_gate["blocking_errors"]:
                print(f"  - {item}", file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

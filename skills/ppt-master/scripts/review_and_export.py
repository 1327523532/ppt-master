#!/usr/bin/env python3
"""Canonical checked export workflow for PPT Master projects."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

from visual_review_gate import build_gate_report, write_gate_report
from visual_review_manifest import utc_now_iso, write_json


def _run_step(name: str, cmd: list[str], cwd: Path) -> dict[str, Any]:
    print(f"\n[review-and-export] {name}")
    print(" ".join(cmd))
    proc = subprocess.run(cmd, cwd=str(cwd), check=False)
    return {
        "name": name,
        "command": cmd,
        "returncode": proc.returncode,
        "ok": proc.returncode == 0,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Run the checked PPT Master export sequence: static check, visual-review "
            "aggregate, notes split, finalize, and PPTX export."
        )
    )
    parser.add_argument("project_path", help="Path to project directory")
    parser.add_argument("--skip-static-check", action="store_true", help="Debug only: skip svg_quality_checker.py")
    parser.add_argument("--skip-total-md-split", action="store_true", help="Debug only: skip total_md_split.py")
    parser.add_argument("--report", default=None, help="Write workflow report JSON to this path")
    parser.add_argument(
        "svg_to_pptx_args",
        nargs=argparse.REMAINDER,
        help="Arguments after -- are passed to svg_to_pptx.py",
    )
    args = parser.parse_args()

    project_dir = Path(args.project_path).resolve()
    script_dir = Path(__file__).resolve().parent
    python = sys.executable or "python3"

    if not project_dir.is_dir():
        print(f"project path not found: {project_dir}", file=sys.stderr)
        return 2

    steps: list[dict[str, Any]] = []
    if not args.skip_static_check:
        steps.append(
            _run_step(
                "static SVG quality check",
                [python, str(script_dir / "svg_quality_checker.py"), str(project_dir)],
                script_dir.parent,
            )
        )
        if not steps[-1]["ok"]:
            return _finish(project_dir, args.report, steps, 1)

    steps.append(
        _run_step(
            "visual-review aggregate",
            [python, str(script_dir / "visual_review_aggregate.py"), str(project_dir)],
            script_dir.parent,
        )
    )
    if not steps[-1]["ok"]:
        write_gate_report(project_dir)
        return _finish(project_dir, args.report, steps, 1)

    gate = write_gate_report(project_dir)
    if not gate["ok"]:
        print("visual-review export gate failed:", file=sys.stderr)
        for item in gate["blocking_errors"]:
            print(f"  - {item}", file=sys.stderr)
        return _finish(project_dir, args.report, steps, 1)

    if not args.skip_total_md_split:
        steps.append(
            _run_step(
                "speaker notes split",
                [python, str(script_dir / "total_md_split.py"), str(project_dir)],
                script_dir.parent,
            )
        )
        if not steps[-1]["ok"]:
            return _finish(project_dir, args.report, steps, 1)

    steps.append(
        _run_step(
            "SVG finalize",
            [python, str(script_dir / "finalize_svg.py"), str(project_dir)],
            script_dir.parent,
        )
    )
    if not steps[-1]["ok"]:
        return _finish(project_dir, args.report, steps, 1)

    passthrough = list(args.svg_to_pptx_args)
    if passthrough and passthrough[0] == "--":
        passthrough = passthrough[1:]
    steps.append(
        _run_step(
            "PPTX export",
            [python, str(script_dir / "svg_to_pptx.py"), str(project_dir), *passthrough],
            script_dir.parent,
        )
    )
    return _finish(project_dir, args.report, steps, 0 if steps[-1]["ok"] else 1)


def _finish(project_dir: Path, report_arg: str | None, steps: list[dict[str, Any]], code: int) -> int:
    report = {
        "schema": "ppt-master.review-and-export-report.v1",
        "generated_by": "review_and_export.py",
        "generated_at": utc_now_iso(),
        "project": str(project_dir),
        "ok": code == 0,
        "steps": steps,
        "export_gate": build_gate_report(project_dir),
    }
    report_path = Path(report_arg).resolve() if report_arg else project_dir / ".review" / "review_and_export_report.json"
    write_json(report_path, report)
    print(f"\n[review-and-export] report: {report_path}")
    print(f"[review-and-export] ok: {str(code == 0).lower()}")
    return code


if __name__ == "__main__":
    sys.exit(main())

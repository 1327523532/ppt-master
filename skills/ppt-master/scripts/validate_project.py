#!/usr/bin/env python3
"""Validate that a project directory is consistent with SKILL.md's
"Free Design Is Opt-In" hard rule.

Contract:
    - Projects initialized with `--template <deck>` (the default) carry a
      `.template_applied` marker AND populated `<project>/templates/decks/<deck>/`.
      Their `spec_lock.md` MUST have a non-empty `page_layouts` section.
    - Projects initialized with `--template free-design` carry a `.free_design`
      marker AND empty `<project>/templates/`. `spec_lock.page_layouts` MAY
      remain empty; downstream checks must NOT treat that as a violation.
    - Both markers simultaneously = user error (re-init with different flags).

Exit codes:
    0 — pass
    1 — ERROR (blocks downstream steps; remediation required)
    2 — WARN (project usable; review recommended)

Usage:
    python scripts/validate_project.py <project_path>
    python scripts/validate_project.py <project_path> --strict   # WARN → exit 1
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

PROJECT_MARKERS = (".template_applied", ".free_design")
SECTION_HEADER_RE = re.compile(r"^##\s+([a-zA-Z_]+)\s*$", re.MULTILINE)
SECTION_BODY_RE = re.compile(
    r"^##\s+([a-zA-Z_]+)\s*$\n(.*?)(?=^##\s+[a-zA-Z_]+\s*$|\Z)",
    re.MULTILINE | re.DOTALL,
)


def detect_template_mode(project: Path) -> tuple[str, list[str]]:
    """Return (mode, list_of_marker_paths).

    mode ∈ {"template_applied", "free_design", "unmarked"}.
    """
    found = [m for m in PROJECT_MARKERS if (project / m).exists()]
    if len(found) == 2:
        return "both_markers", found
    if len(found) == 1:
        return found[0].lstrip("."), found
    return "unmarked", []


def parse_spec_lock_sections(spec_lock: Path) -> dict[str, str]:
    """Parse a spec_lock.md into {section_name: body}."""
    if not spec_lock.is_file():
        return {}
    text = spec_lock.read_text(encoding="utf-8")
    sections = {}
    for match in SECTION_BODY_RE.finditer(text):
        name = match.group(1).strip()
        body = match.group(2).strip()
        sections[name] = body
    return sections


def page_layouts_has_entries(spec_lock_sections: dict[str, str]) -> bool:
    """A page_layouts section counts as populated only if it has at least
    one ``- P<NN>: <basename>`` data line.
    """
    body = spec_lock_sections.get("page_layouts", "")
    for line in body.splitlines():
        s = line.strip()
        if not s or s.startswith("#") or s.startswith(">"):
            continue
        # Real data line: "- P01: 01_cover" or "- P<NN>:<base>"
        if re.match(r"^-\s+P\d+\s*:", s):
            return True
    return False


def collect_template_svgs(project: Path) -> list[str]:
    """Return basenames of every .svg directly under templates/decks/*."""
    decks_dir = project / "templates" / "decks"
    if not decks_dir.is_dir():
        return []
    basenames = []
    for deck_dir in decks_dir.iterdir():
        if not deck_dir.is_dir():
            continue
        for svg in deck_dir.glob("*.svg"):
            basenames.append(svg.stem)
    return sorted(set(basenames))


def validate(project: Path) -> tuple[int, list[str], list[str]]:
    """Run the full contract check. Return (exit_code, errors, warnings)."""
    errors: list[str] = []
    warnings: list[str] = []

    if not project.is_dir():
        return 1, [f"project directory does not exist: {project}"], []

    mode, markers = detect_template_mode(project)

    if mode == "both_markers":
        errors.append(
            f"both template markers present: {markers}. "
            "Re-run `init` with a single --template flag."
        )
        return 1, errors, []

    # Spec lock existence (always required).
    spec_lock = project / "spec_lock.md"
    if not spec_lock.is_file():
        errors.append(
            "spec_lock.md missing. Strategist must write spec_lock.md before "
            "Executor Step 6 begins (see SKILL.md Step 4)."
        )

    sections = parse_spec_lock_sections(spec_lock) if spec_lock.is_file() else {}
    has_layouts = page_layouts_has_entries(sections)
    template_svgs = collect_template_svgs(project)
    templates_populated = bool(template_svgs)

    if mode == "template_applied":
        # Required: page_layouts populated AND at least one template SVG copied.
        if not templates_populated:
            errors.append(
                f".template_applied present but templates/decks/ is empty. "
                "Default template files were not copied into the project. "
                "Re-run `init` (with same name it will refuse; delete the "
                "project directory first) or manually copy the deck SVGs."
            )
        if spec_lock.is_file() and not has_layouts:
            errors.append(
                ".template_applied present but spec_lock.md `page_layouts` "
                "section is empty or has no `P<NN>: <basename>` entries. "
                "Per SKILL.md 'Free Design Is Opt-In', free design is opt-in "
                "ONLY and a non-empty page_layouts mapping is the contract "
                "for template-inheritance projects. Add page-by-page template "
                "SVG mappings or re-init with `--template free-design` to "
                "explicitly opt out."
            )
        # Bonus: each entry in page_layouts should reference an existing SVG.
        if has_layouts and templates_populated:
            body = sections.get("page_layouts", "")
            for line in body.splitlines():
                m = re.match(r"^-\s+P\d+\s*:\s*([A-Za-z0-9_\-]+)", line.strip())
                if m and m.group(1) not in template_svgs:
                    warnings.append(
                        f"page_layouts entry references missing template SVG "
                        f"basename: {m.group(1)!r} (available: "
                        f"{', '.join(template_svgs) or 'none'})"
                    )

    elif mode == "free_design":
        if templates_populated:
            warnings.append(
                ".free_design marker set but templates/decks/ is non-empty. "
                "Marker wins (free design is the opt-in); the leftover SVGs "
                "are inert but suggest a previous init left them behind."
            )

    elif mode == "unmarked":
        # No marker at all. This is suspicious — likely an old project created
        # before this rule was enforced. Flag but don't block unless templates
        # are also empty.
        if not templates_populated:
            warnings.append(
                "no template marker (.template_applied / .free_design) found "
                "and templates/ is empty. This project predates the "
                "'Free Design Is Opt-In' rule. Re-run `init --template free-design` "
                "to write the marker and make the contract explicit."
            )
        else:
            warnings.append(
                "no template marker found but templates/decks/ is populated. "
                "Old project — validate will treat as template_applied for "
                "contract checks."
            )
            # Apply template_applied logic anyway.
            if spec_lock.is_file() and not has_layouts:
                errors.append(
                    "spec_lock.md `page_layouts` empty on a project with "
                    "populated templates/decks/. Either populate page_layouts "
                    "or delete the template SVGs (and write .free_design to "
                    "explicitly opt out)."
                )

    # Warn on hard-coded color/font drift outside spec_lock (cheap heuristic).
    if spec_lock.is_file():
        # Spot-check: page_rhythm / typography declared? bare-minimum contract.
        if "page_rhythm" not in sections:
            warnings.append("spec_lock.md has no `page_rhythm` section.")
        if "typography" not in sections:
            warnings.append("spec_lock.md has no `typography` section.")

    exit_code = 1 if errors else 2 if warnings else 0
    return exit_code, errors, warnings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Validate that a project is consistent with SKILL.md's "
            "'Free Design Is Opt-In' hard rule."
        ),
    )
    parser.add_argument("project_path", help="Project directory to validate")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat WARN as ERROR (exit 1).",
    )
    args = parser.parse_args(argv)

    project = Path(args.project_path).resolve()
    exit_code, errors, warnings = validate(project)

    mode, _ = detect_template_mode(project)
    print(f"validate_project: {project}")
    print(f"  template mode : {mode}")
    print(f"  templates dir : {'populated' if collect_template_svgs(project) else 'empty'}")
    print()
    if errors:
        print(f"[ERROR] {len(errors)} contract violation(s):")
        for e in errors:
            print(f"  - {e}")
    if warnings:
        print(f"[WARN] {len(warnings)} advisory item(s):")
        for w in warnings:
            print(f"  - {w}")
    if not errors and not warnings:
        print("[OK] Project passes template-contract validation.")

    if exit_code == 1:
        return 1
    if exit_code == 2 and args.strict:
        print("(strict mode: WARN promoted to ERROR, exit 1)")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

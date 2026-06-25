"""Replace {{PAGE_NUM}} / {{TOTAL_PAGES}} placeholders in a single SVG file.

Page-order source-of-truth is the alphabetical filename order of the SVGs
in the project (the same convention used by pptx_discovery.find_svg_files
and the finalize_svg.py loop). The caller (finalize_svg.py) computes the
1-based current index and the total count from the sorted file list, then
calls replace_in_file() for each SVG.

Why this lives in finalize_svg.py and not svg_to_pptx.py:
  - finalize_svg.py is the canonical "rewrite SVGs in place before export"
    pass, so any subsequent consumer (native pptx conversion, legacy pptx
    snapshot, live-preview re-export) sees the resolved page numbers.
  - Running it inside svg_to_pptx.py would only fix the native output and
    miss the --svg-snapshot preview, which reads svg_final/ directly.
"""

from __future__ import annotations

import re
from pathlib import Path


# Match the two canonical page-number placeholders. Both forms with or
# without the {{ }} braces are accepted so a hand-authored SVG that
# forgot one brace pair still gets resolved (Lenovo / pixel-retro /
# academic_defense / etc. all use the {{}} form).
_PAGE_NUM_RE = re.compile(r"\{\{\s*PAGE_NUM\s*\}\}|\bPAGE_NUM\b")
_TOTAL_PAGES_RE = re.compile(r"\{\{\s*TOTAL_PAGES\s*\}\}|\bTOTAL_PAGES\b")


def replace_in_file(
    svg_file: Path,
    page_index: int,
    total_pages: int,
) -> int:
    """Replace PAGE_NUM / TOTAL_PAGES placeholders in a single SVG.

    Args:
        svg_file: Path to the SVG file (modified in place).
        page_index: 1-based index of this SVG in the page sequence.
        total_pages: Total number of SVGs in the project.

    Returns:
        Number of placeholder tokens replaced (0 means nothing to do).
    """
    try:
        content = svg_file.read_text(encoding="utf-8")
    except OSError:
        return 0

    new_content, n_page = _PAGE_NUM_RE.subn(str(page_index), content)
    new_content, n_total = _TOTAL_PAGES_RE.subn(str(total_pages), new_content)

    total = n_page + n_total
    if total > 0:
        svg_file.write_text(new_content, encoding="utf-8")
    return total


def replace_in_project(svg_dir: Path) -> int:
    """Replace placeholders across every SVG in svg_dir (sorted order).

    Convenience wrapper for ad-hoc / out-of-pipeline use. In the canonical
    finalize_svg.py flow the loop is in finalize_project() so the count
    is computed once and passed to each per-file call.

    Returns:
        Total placeholder tokens replaced across all SVGs.
    """
    svg_files = sorted(svg_dir.glob("*.svg"))
    if not svg_files:
        return 0
    total = len(svg_files)
    replaced = 0
    for i, svg_file in enumerate(svg_files, start=1):
        replaced += replace_in_file(svg_file, i, total)
    return replaced

#!/usr/bin/env python3
"""Post-export sanity checks for generated PPTX files.

The visual-review workflow checks Chromium-rendered SVGs before export. This
script checks the exported native PPTX after conversion by round-tripping it
back to flat SVG and estimating text-frame geometry.
"""

from __future__ import annotations

import argparse
import shutil
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from xml.etree import ElementTree as ET


SVG_NS = "http://www.w3.org/2000/svg"


@dataclass
class TextBox:
    slide: str
    label: str
    x: float
    y: float
    w: float
    h: float

    @property
    def right(self) -> float:
        return self.x + self.w

    @property
    def bottom(self) -> float:
        return self.y + self.h


def _local_name(elem: ET.Element) -> str:
    return elem.tag.rsplit("}", 1)[-1]


def _as_float(value: str | None, default: float = 0.0) -> float:
    if value is None:
        return default
    try:
        return float(str(value).strip().replace("px", ""))
    except ValueError:
        return default


def _style_value(style: str | None, name: str) -> str | None:
    if not style:
        return None
    for chunk in style.split(";"):
        if ":" not in chunk:
            continue
        key, value = chunk.split(":", 1)
        if key.strip() == name:
            return value.strip()
    return None


def _estimate_width(text: str, font_size: float) -> float:
    total = 0.0
    for ch in text:
        if ch.isspace():
            total += 0.35
        elif ord(ch) > 127:
            total += 1.0
        elif ch.isupper() or ch.isdigit():
            total += 0.62
        else:
            total += 0.55
    return total * font_size


def _collect_lines(text_el: ET.Element) -> list[str]:
    line_parts: list[str] = []
    current: list[str] = []
    if text_el.text:
        current.append(text_el.text)
    for child in text_el:
        if _local_name(child) != "tspan":
            if child.text:
                current.append(child.text)
            if child.tail:
                current.append(child.tail)
            continue
        is_new_line = child.get("x") is not None or child.get("y") is not None or _as_float(child.get("dy"), 0.0) != 0
        if is_new_line and current:
            line_parts.append("".join(current).strip())
            current = []
        current.append("".join(child.itertext()))
        if child.tail:
            current.append(child.tail)
    if current:
        line_parts.append("".join(current).strip())
    return [line for line in line_parts if line]


def _text_boxes(svg_path: Path) -> tuple[list[TextBox], tuple[float, float]]:
    root = ET.parse(svg_path).getroot()
    width = _as_float(root.get("width"), 1280.0)
    height = _as_float(root.get("height"), 720.0)
    viewbox = root.get("viewBox") or root.get("viewbox")
    if viewbox:
        parts = viewbox.split()
        if len(parts) == 4:
            width = _as_float(parts[2], width)
            height = _as_float(parts[3], height)

    boxes: list[TextBox] = []
    for elem in root.iter():
        if _local_name(elem) != "text":
            continue
        text = " ".join(_collect_lines(elem))
        if not text:
            continue
        style = elem.get("style")
        font_size = _as_float(elem.get("font-size") or _style_value(style, "font-size"), 16.0)
        x = _as_float(elem.get("x"), 0.0)
        y = _as_float(elem.get("y"), 0.0)
        lines = _collect_lines(elem) or [text]
        line_width = max((_estimate_width(line, font_size) for line in lines), default=0.0)
        line_height = font_size * 1.35
        box_h = max(font_size * 1.2, line_height * len(lines))
        anchor = elem.get("text-anchor") or _style_value(style, "text-anchor") or "start"
        if anchor == "middle":
            box_x = x - line_width / 2
        elif anchor == "end":
            box_x = x - line_width
        else:
            box_x = x
        boxes.append(
            TextBox(
                slide=svg_path.name,
                label=text[:48],
                x=box_x,
                y=y - font_size,
                w=line_width,
                h=box_h,
            )
        )
    return boxes, (width, height)


def _overlap(a: TextBox, b: TextBox) -> float:
    ix = max(0.0, min(a.right, b.right) - max(a.x, b.x))
    iy = max(0.0, min(a.bottom, b.bottom) - max(a.y, b.y))
    return ix * iy


def check_svg_dir(svg_dir: Path, *, tolerance: float = 8.0) -> list[str]:
    errors: list[str] = []
    for svg_path in sorted(svg_dir.glob("*.svg")):
        boxes, (width, height) = _text_boxes(svg_path)
        for box in boxes:
            if box.x < -tolerance or box.y < -tolerance or box.right > width + tolerance or box.bottom > height + tolerance:
                errors.append(
                    f"{svg_path.name}: text out of canvas: {box.label!r} "
                    f"bbox=({box.x:.0f},{box.y:.0f},{box.w:.0f},{box.h:.0f})"
                )
        for idx, a in enumerate(boxes):
            for b in boxes[idx + 1:]:
                area = _overlap(a, b)
                if area <= 0:
                    continue
                smaller = max(1.0, min(a.w * a.h, b.w * b.h))
                if area >= smaller * 0.18 and area >= 120:
                    errors.append(
                        f"{svg_path.name}: possible text overlap: {a.label!r} / {b.label!r}"
                    )
    return errors


def check_pptx(pptx_path: Path, *, keep_artifacts: bool = False) -> tuple[list[str], Path | None]:
    scripts_dir = Path(__file__).resolve().parent
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))

    from pptx_to_svg import convert_pptx_to_svg
    from pptx_to_svg.converter import ConvertOptions

    if keep_artifacts:
        out_dir = pptx_path.with_name(f"{pptx_path.stem}_post_export_check")
        if out_dir.exists():
            shutil.rmtree(out_dir)
    else:
        out_dir = Path(tempfile.mkdtemp(prefix="pptx-export-check-"))

    convert_pptx_to_svg(
        pptx_path,
        out_dir,
        ConvertOptions(inheritance_mode="flat", media_subdir="assets"),
    )
    errors = check_svg_dir(out_dir / "svg")
    if not keep_artifacts:
        shutil.rmtree(out_dir, ignore_errors=True)
        return errors, None
    return errors, out_dir


def main() -> int:
    parser = argparse.ArgumentParser(description="Check exported PPTX text layout after native conversion.")
    parser.add_argument("pptx_file", help="Path to exported .pptx")
    parser.add_argument("--keep-artifacts", action="store_true", help="Keep round-trip SVG output next to the PPTX")
    args = parser.parse_args()

    pptx_path = Path(args.pptx_file).expanduser().resolve()
    if not pptx_path.is_file():
        print(f"Error: PPTX not found: {pptx_path}", file=sys.stderr)
        return 1
    errors, artifact_dir = check_pptx(pptx_path, keep_artifacts=args.keep_artifacts)
    if artifact_dir:
        print(f"Post-export SVG artifacts: {artifact_dir}")
    if errors:
        print("[ERROR] Post-export PPTX layout check failed:", file=sys.stderr)
        for item in errors[:30]:
            print(f"  - {item}", file=sys.stderr)
        if len(errors) > 30:
            print(f"  - ... and {len(errors) - 30} more", file=sys.stderr)
        return 1
    print("[OK] Post-export PPTX layout check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

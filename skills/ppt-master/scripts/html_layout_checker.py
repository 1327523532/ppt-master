#!/usr/bin/env python3
"""
PPT Master - HTML/DOM Layout Checker

Deterministic, non-VLM geometry floor for rendered slides. Renders each SVG in
svg_output/ through the live-preview server in headless Chromium, then reads the
browser's real DOM geometry (getBBox + getCTM) to catch out-of-bounds elements,
text overlap, container overflow, and broken images. Runs after
svg_quality_checker.py and before the (opt-out-able) visual-review, so the floor
holds even when the VLM pass is skipped.

This is the pure geometry checker — it does not edit svg_output/ and does not make
subjective design judgments (that stays with visual-review). Renderer helpers (SVG
discovery, server probe, render lock) are reused from visual_review.py rather than
reimplemented.

Usage:
    python3 scripts/html_layout_checker.py <project_path>
    python3 scripts/html_layout_checker.py <project_path> --pages 02 03
    python3 scripts/html_layout_checker.py <project_path> --server-url http://localhost:5050

Exit codes (per .kiro/specs/html-layout-check/design.md §1):
    0 — all requested pages pass, no hard error
    2 — project path invalid, no svg_output/, or live-preview server unreachable
    3 — rendering backend (playwright + chromium) missing or unable to launch
    4 — checks completed, one or more hard errors present
    5 — a page failed to render or its DOM probe failed

Dependencies:
    playwright (Chromium) — shared with visual_review.py

File layout:
    SECTION 1  Configuration       — every tunable constant, grouped by concern
    SECTION 2  DOM probe           — PROBE_JS + canvas resolution
    SECTION 3  Server lifecycle    — auto-start / reuse / reap the live-preview server
    SECTION 4  Geometry utilities  — pure rect math, no I/O, no judgment
    SECTION 5  Checks              — one function per issue code
    SECTION 6  CLI & orchestration — argparse, page probing loop, main()
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

_SCRIPTS_DIR = Path(__file__).resolve().parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

# reuse visual_review's renderer helpers as the single shared surface — do not
# reimplement SVG discovery or server probing here (avoids drift). playwright is
# lazy-imported inside visual_review's functions, so these module-level symbols
# import cleanly even when playwright is absent.
from visual_review import (  # noqa: E402,F401
    _safe_print,
    check_server,
    discover_pages,
    fetch_slide_text,
    file_lock,
)

# per-project server lock contract (pid + port), shared with svg_editor/server.py.
from server_common import process_alive, read_lock  # noqa: E402


# ════════════════════════════════════════════════════════════════════════════
# SECTION 1: Configuration
# Every tunable threshold lives here so the whole policy is adjustable in one
# place. Grouped by the concern each constant serves.
# ════════════════════════════════════════════════════════════════════════════

# ── Server lifecycle ────────────────────────────────────────────────────────
# svg_editor/server.py — the live-preview server this checker drives.
SERVER_SCRIPT = _SCRIPTS_DIR / "svg_editor" / "server.py"
# runtime lock written by the server under <project>/live_preview/ — the single
# source of truth for "is this project's server up, and on which port".
LIVE_PREVIEW_LOCK = Path("live_preview") / "lock.json"
# match server.py's own _wait_for_ready ceiling.
SERVER_READY_TIMEOUT = 15

# ── DOM probe ───────────────────────────────────────────────────────────────
# SVG tags whose render box the probe measures. Renderable geometry only —
# <defs>/<linearGradient>/<stop> carry no layout box and are skipped.
MEASURED_TAGS = ("text", "image", "rect", "path", "circle", "ellipse",
                 "polygon", "polyline", "line", "use", "g")
# R5 ceiling: how long the probe waits on document.fonts.ready before giving up
# (a never-loading webfont must not hang the whole check).
FONTS_READY_CEILING_MS = 3000
# per-image load-verification timeout (localhost should answer instantly; this
# only guards against a hung request).
IMAGE_VERIFY_TIMEOUT_MS = 2000

# ── Canvas bounds (OUT_OF_BOUNDS) ───────────────────────────────────────────
# slack on the canvas bounds check: absorbs float rounding and full-bleed
# backgrounds that sit exactly on the edge (e.g. <rect 0 0 1280 720>). Real
# overflow (text pushed off-canvas, a card past the frame) dwarfs this.
CANVAS_TOLERANCE_PX = 2.0

# ── Text overlap (TEXT_OVERLAP) ─────────────────────────────────────────────
# below this fraction of the smaller text box, an intersection reads as line-gap
# slack between adjacent lines, not a real overlap (design §2 default 0.15).
TEXT_OVERLAP_MIN_RATIO = 0.15
# same-<g> pairs are only treated as one logical block (tspan continuation / same
# paragraph) when their horizontal projections overlap at least this much. Real
# wrapped lines share a column (ratio ~1.0); side-by-side table cells wrapped in
# one row <g> barely overlap (ratio ~0.2) and must NOT be exempted.
SAME_BLOCK_X_OVERLAP_RATIO = 0.6
# horizontal penetration floor (px) for a same-line collision. The area-ratio
# test above only models vertically-stacked lines (wide, thin overlap); two long
# boxes colliding side-by-side make a thin, *tall* overlap whose area ratio is
# just as small, so they slip through. When the vertical overlap is near-total
# (same baseline, TEXT_OVERLAP_SAMELINE_Y_RATIO) yet the boxes still bite into
# each other horizontally past this floor, it is a real same-line collision. Set
# above a full-width trailing-punctuation phantom advance (~1em) so a CJK comma
# kissing the next column does not false-fire; a genuine collision bites deeper.
TEXT_OVERLAP_SAMELINE_X_PX = 8.0
# how much of the shorter box's height must overlap to call two boxes "same line".
TEXT_OVERLAP_SAMELINE_Y_RATIO = 0.5
# the same-line branch ignores a pair when one side is a lone oversized glyph
# (a decorative quote mark, drop cap, or bullet set far larger than the body it
# sits behind) — that is intentional ornament layered under text, not a line
# collision. Triggered only when one box is a single character AND its font size
# is at least this multiple of the other's. The vertically-stacked area test is
# unaffected; a same-size single glyph colliding mid-line still fires.
TEXT_OVERLAP_DECOR_FONT_RATIO = 2.0

# ── Container overflow (TEXT_CONTAINER_OVERFLOW) ────────────────────────────
# only filled shapes can hold text — a <line>/<text> is never a container.
CONTAINER_TAGS = ("rect", "path", "circle", "ellipse")
# tags trusted as a *heuristically-inferred* text container. Only <rect> — its
# bbox is the actual content box. A <circle>/<ellipse> bbox over-claims its empty
# corners and a <path> bbox is arbitrary geometry (donut arc, decorative swoosh),
# so centered/overlaid text reads as "overflowing" a box it was never seated in.
# Those false positives dominated circle/path inference in practice. Authors who
# genuinely want a non-rect shape checked still opt in explicitly via
# data-check-within, which bypasses this set.
HEURISTIC_CONTAINER_TAGS = ("rect",)
# R4 sanity bound: a candidate larger than this fraction of the canvas is a
# full-bleed background, not a card — skip it, or the page's white <rect> would
# "contain" every text and nothing could ever overflow.
CONTAINER_MAX_AREA_RATIO = 0.85
# a container's shortest side must clear this (px). Decks draw divider/underline
# rules as 1–3px-thick <rect>s; a thin bar spanning half the page would otherwise
# "contain" every text crossing it and false-fire overflow. A real card is
# tens of px on its short side.
CONTAINER_MIN_SIDE = 20.0
# slack before a text edge past its container counts as overflow (absorbs card
# padding rounded into the box, mirrors CANVAS_TOLERANCE_PX). Used for the
# vertical edges and the left edge.
CONTAINER_OVERFLOW_TOL = 2.0
# horizontal noise floor (px) for the right edge of a line NOT ending in wide
# punctuation. getBBox's advance box carries a few px of inter-glyph tracking
# past the visible ink even when the text fits, more so on longer Latin lines, so
# a flush line can report a right edge ~4px over. Set just above that (measured:
# fitting lines peak ~+4px, real clips start ~+5.7px) so true clipping still
# fires while sub-glyph noise does not. Lines ending in wide punctuation use the
# larger font-factor tolerance instead.
CONTAINER_OVERFLOW_H_NOISE = 5.0
# horizontal slack as a multiple of font size. getBBox returns a text's layout
# advance box, and a CJK full-width trailing punctuation (，：。) advances ~1em
# past its visible ink, plus inter-glyph tracking — so a line ending flush inside
# a card can report a right edge ~1.3 font-sizes beyond it. Forgive one trailing
# glyph's advance; real overflow (multiple chars past the edge) still fires.
CONTAINER_OVERFLOW_FONT_FACTOR = 1.3

# ── Element collision (ELEMENT_COLLISION_AMBIGUOUS) ─────────────────────────
# filled, space-occupying graphic tags that take part in collision detection.
# text has its own overlap check; g is a union box; line/polyline have no area.
COLLISION_TAGS = ("image", "use", "rect", "path", "circle", "ellipse", "polygon")
# at/above this fraction of the smaller box, the overlap means the smaller element
# sits *inside* the larger — a deliberate stack (icon on a chip), not a collision.
COLLISION_CONTAIN_RATIO = 0.9
# the smaller box must be at least this fraction of the larger by area to count as
# a peer collision. Below it (small icon over a big backdrop) is normal layering.
COLLISION_SIZE_RATIO = 0.4
# below this fraction of the smaller box, the intersection is edge-touch noise.
COLLISION_MIN_OVERLAP = 0.15
# absolute area floor (px²): elements smaller than this are chart markers, dots,
# or tiny decorations whose overlap is meaningless noise. ~24x24px — a real icon
# or card is larger; a data point on a trend line is not.
COLLISION_MIN_AREA = 576.0


def _env_flag(name: str, default: bool = False) -> bool:
    """Read a boolean env var. Only 1/true/yes/on (case-insensitive) enable it;
    anything else — including unset, '0', 'false' — is off. Avoids the
    'any non-empty string is truthy' trap."""
    val = os.environ.get(name)
    if val is None:
        return default
    return val.strip().lower() in ("1", "true", "yes", "on")


# element collision is OFF by default — it is the highest false-positive check and
# only a soft warning. Flip on with PPT_LAYOUT_COLLISION=1 (e.g. for A/B testing).
COLLISION_ENABLED = _env_flag("PPT_LAYOUT_COLLISION", default=False)


# ════════════════════════════════════════════════════════════════════════════
# SECTION 2: DOM probe
# Runs inside Chromium, reads geometry only, never mutates the SVG. Injects the
# slide the same way visual_review does, waits for fonts, then reports each
# element's render box plus per-image load status. All thresholds/judgments stay
# in Python — this returns raw geometry facts, nothing more.
# ════════════════════════════════════════════════════════════════════════════

PROBE_JS = r"""
async (cfg) => {
  const res = await fetch('/api/slide/' + cfg.pageName + '?_=' + Date.now());
  if (!res.ok) throw new Error('fetch /api/slide/' + cfg.pageName + ' returned ' + res.status);
  const data = await res.json();
  document.documentElement.innerHTML =
    '<head><style>html,body{margin:0;padding:0;overflow:hidden}svg{display:block}</style></head>'
    + '<body>' + data.content + '</body>';

  // R5: cap fonts.ready so a never-loading webfont can't hang the probe.
  await Promise.race([
    document.fonts.ready,
    new Promise(function (r) { setTimeout(r, cfg.fontsCeilingMs); }),
  ]);

  const svg = document.querySelector('svg');
  if (!svg) {
    return { root: null, elements: [], counts: { element: 0, text: 0, image: 0, checked_bbox: 0 } };
  }

  // root <svg> declared geometry, compared in Python for ROOT_DIMENSION_MISMATCH.
  const vb = svg.viewBox && svg.viewBox.baseVal;
  const root = {
    viewBoxW: vb ? vb.width : null,
    viewBoxH: vb ? vb.height : null,
    width: (svg.width && svg.width.baseVal) ? svg.width.baseVal.value : null,
    height: (svg.height && svg.height.baseVal) ? svg.height.baseVal.value : null,
  };

  // bbox four corners through the element's CTM into root user space, so a
  // transformed/rotated element yields its true axis-aligned box on canvas.
  function renderBox(el) {
    let b;
    try { b = el.getBBox(); } catch (e) { return null; }
    const m = el.getCTM();
    if (!m) return null;
    const cs = [[b.x, b.y], [b.x + b.width, b.y], [b.x, b.y + b.height], [b.x + b.width, b.y + b.height]];
    let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
    for (const c of cs) {
      const px = m.a * c[0] + m.c * c[1] + m.e;
      const py = m.b * c[0] + m.d * c[1] + m.f;
      if (px < minX) minX = px;
      if (py < minY) minY = py;
      if (px > maxX) maxX = px;
      if (py > maxY) maxY = py;
    }
    return { x: minX, y: minY, w: maxX - minX, h: maxY - minY };
  }

  // SVG <image> has no naturalWidth; load the same URL it resolved against and
  // trust onerror / naturalWidth==0 to flag a broken image.
  function verifyImage(href) {
    return new Promise(function (resolve) {
      let url;
      try { url = new URL(href, document.baseURI).href; } catch (e) { resolve(false); return; }
      const img = new Image();
      const t = setTimeout(function () { resolve(false); }, cfg.imageTimeoutMs);
      img.onload = function () { clearTimeout(t); resolve(img.naturalWidth > 0); };
      img.onerror = function () { clearTimeout(t); resolve(false); };
      img.src = url;
    });
  }

  const MEASURED = cfg.measuredTags;
  const elements = [];
  let textCount = 0, imageCount = 0, checkedBbox = 0;
  const imageJobs = [];
  // identity for each <g> so Python can tell whether two texts share the same
  // direct parent group (the "same logical block" rule (a)). Element ids are
  // unreliable here — most wrapping <g>s carry none — so use a DOM-walk serial.
  const groupSerials = new Map();
  let groupSeq = 0;
  function directGroupId(el) {
    const p = el.parentNode;
    if (!p || p.nodeType !== 1 || p.tagName.toLowerCase() !== 'g') return null;
    if (!groupSerials.has(p)) groupSerials.set(p, ++groupSeq);
    return groupSerials.get(p);
  }
  for (const el of svg.querySelectorAll('*')) {
    const tag = el.tagName.toLowerCase();
    if (tag === 'text') textCount++;
    if (tag === 'image') imageCount++;
    if (MEASURED.indexOf(tag) === -1) continue;
    const bbox = renderBox(el);
    if (bbox) checkedBbox++;
    const rec = {
      tag: tag,
      id: el.id || null,
      groupId: directGroupId(el),
      dataIgnore: el.hasAttribute('data-check-ignore'),
      dataWithin: el.getAttribute('data-check-within'),
      dataContainer: el.getAttribute('data-check-container'),
      dataRole: el.getAttribute('data-check-role'),
      bbox: bbox,
    };
    if (tag === 'text') {
      const fs = parseFloat(getComputedStyle(el).fontSize);
      rec.fontSize = isFinite(fs) ? fs : null;
      // does the line end in wide CJK *punctuation*? Only then does getBBox's
      // advance box overshoot the visible ink by ~1em — full-width punctuation
      // (。，、：；！？）」 …) has narrow ink but a full-width advance cell. A
      // trailing CJK *ideograph* fills its cell (phantom ~0) and a Latin glyph
      // has no phantom, so neither inherits that forgiveness.
      const t = (el.textContent || '').replace(/\s+$/, '');
      const last = t.length ? t[t.length - 1] : '';
      rec.endPunct = /[、。，．・…‥！？；：）〕】」』》〉”’｡｣､·]/.test(last)
        || /[！-／：-＠［-｀｛-･]/.test(last);
      // trimmed character count — a lone oversized glyph (decorative quote, drop
      // cap, bullet) is length 1 and must not read as a text block in collision.
      rec.charLen = t.trim().length;
      // text-anchor decides how the line is positioned: 'middle'/'end' lines are
      // placed by their center/right, so an edge spilling past a heuristic
      // container reads as a centering artifact, not a left-pinned clip.
      rec.anchor = getComputedStyle(el).textAnchor || 'start';
    }
    if (tag === 'image') {
      const href = (el.href && el.href.baseVal) || el.getAttribute('href')
        || el.getAttribute('xlink:href') || '';
      rec.href = href;
      rec.imageLoaded = null;
      const idx = elements.length;
      imageJobs.push(verifyImage(href).then(function (ok) { elements[idx].imageLoaded = ok; }));
    }
    elements.push(rec);
  }
  await Promise.all(imageJobs);

  return {
    root: root,
    elements: elements,
    counts: { element: elements.length, text: textCount, image: imageCount, checked_bbox: checkedBbox },
  };
}
"""


def resolve_canvas(project_path: Path) -> dict | None:
    """Expected canvas (width/height) this deck's pages should declare, read
    from spec_lock.md's pinned ``viewBox: 0 0 W H``.

    This is the one value compared against a page's *own* root viewBox to flag
    ROOT_DIMENSION_MISMATCH, so it has to come from outside the page — the spec
    lock is that external truth (the Strategist pins it before any SVG exists).
    Returns None when the lock is absent or unparseable; the caller then skips
    the dimension check rather than fabricate a canvas and false-fire on a
    legitimately non-1280x720 deck.

    OUT_OF_BOUNDS does not use this — it measures each element against that
    page's own viewBox, so it stays fully functional even when this is None.
    """
    lock = project_path / "spec_lock.md"
    try:
        text = lock.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None
    m = re.search(r"viewBox:\s*0\s+0\s+(\d+)\s+(\d+)", text)
    if not m:
        return None
    return {"width": int(m.group(1)), "height": int(m.group(2))}


# ════════════════════════════════════════════════════════════════════════════
# SECTION 3: Server lifecycle
# Resolve a live-preview server for the project — reuse a running one via its
# lock file, or auto-start one we own and reap. Never blind-probe a port (would
# risk attaching to a different project's server).
# ════════════════════════════════════════════════════════════════════════════

def _server_ready(server_url: str, timeout: float = 1.0) -> bool:
    """True if the server answers /api/slides at this URL."""
    try:
        check_server(server_url)
        return True
    except RuntimeError:
        return False


def ensure_server(
    project_path: Path, server_url: str | None
) -> tuple[str, subprocess.Popen | None]:
    """Resolve a live-preview server for this project, auto-starting one if needed.

    Returns ``(base_url, proc)``. ``proc`` is non-None only when we started the
    server ourselves — the caller terminates it in a finally block. A reused
    server (proc is None) is never touched, so a user's Step 6 live preview
    survives.

    Reuse is decided by this project's own lock file (pid + port), never by
    blind-probing a port — that would risk attaching to a *different* project's
    server and silently checking the wrong deck. Raises RuntimeError on any
    unrecoverable server condition (caller maps it to exit 2).
    """
    # explicit --server-url: manual override / escape hatch, user owns it.
    if server_url:
        if _server_ready(server_url):
            return server_url.rstrip("/"), None
        raise RuntimeError(
            f"live-preview server not reachable at {server_url} (passed via --server-url)"
        )

    # default path: trust this project's lock file as the single source of truth.
    lock_path = project_path / LIVE_PREVIEW_LOCK
    lock = read_lock(lock_path)
    if lock and process_alive(int(lock.get("pid", 0))):
        port = lock.get("port")
        reused_url = f"http://localhost:{port}"
        if _server_ready(reused_url):
            return reused_url, None
        # lock names a live pid but the port won't answer — do NOT fall back to
        # probing some other port (that is how the wrong project gets checked).
        raise RuntimeError(
            f"live-preview server lock at {lock_path} names pid {lock.get('pid')} "
            f"on port {port}, but it does not answer. Stop that process and retry."
        )

    # no live server for this project — start one we own and can reap.
    return _start_server(project_path)


def _start_server(project_path: Path) -> tuple[str, subprocess.Popen]:
    """Launch svg_editor/server.py as a foreground child (no --daemon, so we keep
    the handle and can terminate it). Returns (base_url, proc)."""
    cmd = [
        sys.executable,
        str(SERVER_SCRIPT),
        str(project_path),
        "--no-browser",
    ]
    try:
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
        )
    except OSError as e:
        raise RuntimeError(f"failed to start live-preview server: {e}") from e

    # the server picks its own free port and writes it to the lock file; poll
    # until the lock appears with a live port that answers, or we time out.
    lock_path = project_path / LIVE_PREVIEW_LOCK
    deadline = time.monotonic() + SERVER_READY_TIMEOUT
    while time.monotonic() < deadline:
        if proc.poll() is not None:
            raise RuntimeError(
                f"live-preview server exited early (code {proc.returncode}) before becoming ready"
            )
        lock = read_lock(lock_path)
        port = lock.get("port") if lock else None
        if port:
            url = f"http://localhost:{port}"
            if _server_ready(url):
                return url, proc
        time.sleep(0.25)

    proc.terminate()
    raise RuntimeError(
        f"live-preview server did not become ready within {SERVER_READY_TIMEOUT}s"
    )


# ════════════════════════════════════════════════════════════════════════════
# SECTION 4: Geometry utilities
# Pure rect math — no I/O, no judgment. Shared by the checks in SECTION 5.
# ════════════════════════════════════════════════════════════════════════════

def _el_ref(el: dict) -> str:
    """Stable reference for an element in an issue: '#id' when it has one, else
    '<tag@x,y>' from its render box so the report still points somewhere."""
    if el.get("id"):
        return f"#{el['id']}"
    bbox = el.get("bbox")
    if bbox:
        return f"<{el['tag']}@{round(bbox['x'])},{round(bbox['y'])}>"
    return f"<{el['tag']}>"


def _rect_area(b: dict) -> float:
    return max(0.0, b["w"]) * max(0.0, b["h"])


def _rect_intersection_area(a: dict, b: dict) -> float:
    ix = max(0.0, min(a["x"] + a["w"], b["x"] + b["w"]) - max(a["x"], b["x"]))
    iy = max(0.0, min(a["y"] + a["h"], b["y"] + b["h"]) - max(a["y"], b["y"]))
    return ix * iy


def _rect_overlap_extents(a: dict, b: dict) -> tuple[float, float]:
    """The (x, y) overlap extents of two boxes. Either is 0 when they don't
    intersect on that axis. Used to measure penetration depth per-axis, which the
    area alone cannot express — a thin-but-tall side-by-side collision and a
    wide-but-thin line-gap touch can share the same tiny area."""
    ix = max(0.0, min(a["x"] + a["w"], b["x"] + b["w"]) - max(a["x"], b["x"]))
    iy = max(0.0, min(a["y"] + a["h"], b["y"] + b["h"]) - max(a["y"], b["y"]))
    return ix, iy


def _x_overlap_ratio(a: dict, b: dict) -> float:
    """Horizontal projection overlap as a fraction of the narrower box. ~1.0 for
    wrapped lines sharing a column, near 0 for side-by-side cells. Width 0 → 0."""
    ix = max(0.0, min(a["x"] + a["w"], b["x"] + b["w"]) - max(a["x"], b["x"]))
    narrow = min(a["w"], b["w"])
    return ix / narrow if narrow > 0 else 0.0


def _text_exceeds(text_b: dict, cont_b: dict, tol: float, font_size: float | None,
                  end_punct: bool = False) -> bool:
    """True if the text box pokes past the container box beyond tolerance.
    The wide horizontal tolerance (one font-size, CONTAINER_OVERFLOW_FONT_FACTOR)
    exists only to absorb the full-width-punctuation advance artifact, so it
    applies to the *right* edge only when the line ends in wide CJK punctuation
    (end_punct). Otherwise the right edge gets CONTAINER_OVERFLOW_H_NOISE — a few
    px above inter-glyph tracking noise but below a real clip. Left and vertical
    edges always use the tight tol."""
    h_tol_right = CONTAINER_OVERFLOW_H_NOISE
    if end_punct and font_size:
        h_tol_right = max(h_tol_right, font_size * CONTAINER_OVERFLOW_FONT_FACTOR)
    return (
        text_b["x"] < cont_b["x"] - tol
        or text_b["y"] < cont_b["y"] - tol
        or text_b["x"] + text_b["w"] > cont_b["x"] + cont_b["w"] + h_tol_right
        or text_b["y"] + text_b["h"] > cont_b["y"] + cont_b["h"] + tol
    )


def _text_belongs_to(text_b: dict, cont_b: dict) -> bool:
    """True if a text box is plausibly seated in a container box. Uses the text's
    vertical center (line height is small and reliable) against the container's y
    band, and requires the x ranges to overlap — deliberately NOT 'center inside',
    because a badly overflowing line's center can fall outside the card on the very
    axis it overflows, which would make the worst cases un-attributable."""
    cy = text_b["y"] + text_b["h"] / 2.0
    if not (cont_b["y"] <= cy <= cont_b["y"] + cont_b["h"]):
        return False
    x_overlap = min(text_b["x"] + text_b["w"], cont_b["x"] + cont_b["w"]) - max(
        text_b["x"], cont_b["x"]
    )
    return x_overlap > 0


def _infer_container(
    text: dict, text_idx: int, elements: list[dict], canvas: dict
) -> dict | None:
    """Best guess at which filled shape holds this text, when no data-check-within
    marks it. Among elements painted *below* the text (smaller list index =
    earlier in document order = lower z-order), keep those that are a filled
    container tag, are not a full-bleed background (R4), and geometrically contain
    the text's center; return the smallest by area. None when nothing qualifies —
    free text on the page background has no container and must not be flagged.
    """
    b = text.get("bbox")
    if not b:
        return None
    canvas_area = canvas["width"] * canvas["height"]
    best = None
    best_area = None
    for cand in elements[:text_idx]:
        if cand["tag"] not in HEURISTIC_CONTAINER_TAGS:
            continue
        cb = cand.get("bbox")
        if not cb:
            continue
        if min(cb["w"], cb["h"]) < CONTAINER_MIN_SIDE:
            continue  # divider/underline rule, not a card
        area = _rect_area(cb)
        if area <= 0 or area > canvas_area * CONTAINER_MAX_AREA_RATIO:
            continue
        if not _text_belongs_to(b, cb):
            continue
        if best_area is None or area < best_area:
            best, best_area = cand, area
    return best


# ════════════════════════════════════════════════════════════════════════════
# SECTION 5: Checks
# One function per issue code. Each takes raw probe geometry and returns a list
# of issue dicts (empty when clean). No I/O — pure judgment over SECTION 4 math.
# ════════════════════════════════════════════════════════════════════════════

def check_out_of_bounds(elements: list[dict], canvas: dict) -> list[dict]:
    """Flag elements whose render box leaves the page's own canvas past the
    tolerance. <g> is skipped — its bbox is the union of its children, which
    would read as a false overflow."""
    issues: list[dict] = []
    w, h = canvas["width"], canvas["height"]
    tol = CANVAS_TOLERANCE_PX
    for el in elements:
        if el["tag"] == "g" or el.get("dataIgnore"):
            continue
        b = el.get("bbox")
        if not b:
            continue
        if b["x"] < -tol or b["y"] < -tol or b["x"] + b["w"] > w + tol or b["y"] + b["h"] > h + tol:
            issues.append({
                "code": "OUT_OF_BOUNDS",
                "severity": "error",
                "message": (
                    f"{el['tag']} render box "
                    f"({b['x']:.1f},{b['y']:.1f} {b['w']:.1f}x{b['h']:.1f}) "
                    f"leaves the {w}x{h} canvas"
                ),
                "elements": [_el_ref(el)],
                "bbox": {"a": b},
                "suggested_fix": "Move or resize this element back inside the canvas.",
            })
    return issues


def check_root_dimension(root: dict | None, expected: dict | None) -> list[dict]:
    """Compare the page's own root <svg> against the deck's expected canvas.
    Skipped entirely when either is unavailable (no spec_lock → no false
    fire on a legitimately non-default deck)."""
    if not root or not expected:
        return []
    rw, rh = root.get("viewBoxW"), root.get("viewBoxH")
    if rw is None or rh is None:
        return []
    if int(rw) == expected["width"] and int(rh) == expected["height"]:
        return []
    return [{
        "code": "ROOT_DIMENSION_MISMATCH",
        "severity": "error",
        "message": (
            f"root svg viewBox {int(rw)}x{int(rh)} does not match the deck "
            f"canvas {expected['width']}x{expected['height']}"
        ),
        "elements": ["svg"],
        "bbox": None,
        "suggested_fix": f"Set viewBox to 0 0 {expected['width']} {expected['height']}.",
    }]


def check_images(elements: list[dict]) -> list[dict]:
    """Flag <image> elements that failed to load or rendered to no area."""
    issues: list[dict] = []
    for el in elements:
        if el["tag"] != "image":
            continue
        b = el.get("bbox")
        zero_area = (not b) or b["w"] < 1 or b["h"] < 1
        if el.get("imageLoaded") is False or zero_area:
            issues.append({
                "code": "IMAGE_RENDER_BROKEN",
                "severity": "error",
                "message": (
                    f"image '{el.get('href') or '(no href)'}' did not render "
                    f"({'load failed' if el.get('imageLoaded') is False else 'zero-area box'})"
                ),
                "elements": [_el_ref(el)],
                "bbox": {"a": b} if b else None,
                "suggested_fix": "Fix the image href or its declared size.",
            })
    return issues


def check_text_overlap(elements: list[dict]) -> list[dict]:
    """Pairwise <text> bbox intersection, excluding same-logical-block pairs:
    (a) same direct parent <g> AND horizontally aligned (x-overlap ratio ≥
        SAME_BLOCK_X_OVERLAP_RATIO) — tspan continuation / wrapped lines in one
        column. Side-by-side cells sharing a row <g> are NOT exempted;
    (c) either element carries data-check-ignore.
    A pair counts as overlapping when EITHER the intersection clears
    TEXT_OVERLAP_MIN_RATIO of the smaller box (the area test, which models
    vertically-stacked lines), OR it is a same-line collision: the boxes share a
    baseline (vertical overlap ≥ TEXT_OVERLAP_SAMELINE_Y_RATIO of the shorter box)
    and still bite into each other horizontally past TEXT_OVERLAP_SAMELINE_X_PX.
    The second branch exists because two long side-by-side boxes colliding on one
    line make a thin, tall intersection whose *area* ratio is as small as a
    harmless line-gap touch — area alone is blind to it."""
    texts = [e for e in elements if e["tag"] == "text" and e.get("bbox")]
    issues: list[dict] = []
    for i in range(len(texts)):
        for j in range(i + 1, len(texts)):
            a, b = texts[i], texts[j]
            if a.get("dataIgnore") or b.get("dataIgnore"):
                continue
            if (
                a.get("groupId") is not None
                and a.get("groupId") == b.get("groupId")
                and _x_overlap_ratio(a["bbox"], b["bbox"]) >= SAME_BLOCK_X_OVERLAP_RATIO
            ):
                continue
            inter = _rect_intersection_area(a["bbox"], b["bbox"])
            if inter <= 0:
                continue
            smaller = min(_rect_area(a["bbox"]), _rect_area(b["bbox"]))
            if smaller <= 0:
                continue

            area_hit = inter >= smaller * TEXT_OVERLAP_MIN_RATIO

            # same-line collision: near-total vertical overlap plus a horizontal
            # bite the area test cannot see. Discount the left box's full-width
            # trailing-punctuation phantom advance (~1em) so a CJK comma kissing
            # the next column is not mistaken for a collision.
            ix, iy = _rect_overlap_extents(a["bbox"], b["bbox"])
            shorter_h = min(a["bbox"]["h"], b["bbox"]["h"])
            same_line = shorter_h > 0 and iy >= shorter_h * TEXT_OVERLAP_SAMELINE_Y_RATIO
            left = a if a["bbox"]["x"] <= b["bbox"]["x"] else b
            phantom = (left.get("fontSize") or 0) if left.get("endPunct") else 0.0
            sameline_hit = same_line and (ix - phantom) >= TEXT_OVERLAP_SAMELINE_X_PX

            # decorative-glyph guard: a lone oversized character (big quote mark,
            # drop cap, bullet) layered behind a body line is intentional ornament,
            # not a same-line collision. Only the same-line branch is gated — the
            # area test still catches a true mid-line pile-up.
            if sameline_hit:
                fa, fb = a.get("fontSize") or 0, b.get("fontSize") or 0
                a_decor = a.get("charLen", 99) <= 1 and fa >= fb * TEXT_OVERLAP_DECOR_FONT_RATIO
                b_decor = b.get("charLen", 99) <= 1 and fb >= fa * TEXT_OVERLAP_DECOR_FONT_RATIO
                if a_decor or b_decor:
                    sameline_hit = False

            if not (area_hit or sameline_hit):
                continue
            issues.append({
                "code": "TEXT_OVERLAP",
                "severity": "error",
                "message": (
                    f"two text elements overlap by {inter:.0f}px "
                    f"({inter / smaller * 100:.0f}% of the smaller box)"
                ),
                "elements": [_el_ref(a), _el_ref(b)],
                "bbox": {"a": a["bbox"], "b": b["bbox"]},
                "suggested_fix": "Separate the two text blocks or reduce line count.",
            })
    return issues


def check_container_overflow(elements: list[dict], canvas: dict) -> list[dict]:
    """Flag text that spills past the card/container holding it. Container is the
    element named by data-check-within when present (metadata wins), else the
    heuristic guess from _infer_container. Text with no resolvable container
    (free text on the background) is never flagged."""
    by_id = {e["id"]: e for e in elements if e.get("id")}
    issues: list[dict] = []
    for idx, el in enumerate(elements):
        if el["tag"] != "text" or not el.get("bbox"):
            continue
        within = el.get("dataWithin")
        if within:
            container = by_id.get(within)
            source = "data-check-within"
        else:
            container = _infer_container(el, idx, elements, canvas)
            source = "heuristic"
        if not container or not container.get("bbox"):
            continue
        if not _text_exceeds(el["bbox"], container["bbox"], CONTAINER_OVERFLOW_TOL,
                             el.get("fontSize"), el.get("endPunct", False)):
            continue
        # misattribution guard (heuristic only): a card the text overflows on BOTH
        # horizontal sides is not actually holding it — that is centered text over
        # a small decoration (icon/dot/badge) that _infer_container mis-picked, not
        # a clip. A real clip keeps its left padding and spills one side. A declared
        # data-check-within container is author truth and is never second-guessed.
        if source == "heuristic":
            tb, cb = el["bbox"], container["bbox"]
            tol = CONTAINER_OVERFLOW_TOL
            over_left = tb["x"] < cb["x"] - tol
            over_right = tb["x"] + tb["w"] > cb["x"] + cb["w"] + tol
            if over_left and over_right:
                continue
        issues.append({
            "code": "TEXT_CONTAINER_OVERFLOW",
            "severity": "error",
            "message": (
                f"text overflows its {source} container "
                f"{_el_ref(container)} on the canvas"
            ),
            "elements": [_el_ref(el), _el_ref(container)],
            "bbox": {"a": el["bbox"], "b": container["bbox"]},
            "suggested_fix": "Shrink the text or enlarge the container.",
        })
    return issues


def check_element_collision(elements: list[dict], canvas: dict) -> list[dict]:
    """Flag pairs of non-text graphics that cross-penetrate rather than stack.
    Always a warning, never a hard error (locked decision ②) — overlap among
    shapes is usually intentional (icon on a chip, card over an illustration),
    so this only nudges 'these two cross, take a look'.

    A pair is reported only when all hold: both clear an absolute size floor
    (COLLISION_MIN_AREA, so chart markers / dots are ignored); neither is a
    full-bleed background (R4); they are comparable in size (COLLISION_SIZE_RATIO,
    so a small icon over a big backdrop is skipped); and their overlap is in the
    mid band — above COLLISION_MIN_OVERLAP (edge-touch noise) yet below
    COLLISION_CONTAIN_RATIO (containment = deliberate stacking)."""
    canvas_area = canvas["width"] * canvas["height"]
    cands = [
        e for e in elements
        if e["tag"] in COLLISION_TAGS and e.get("bbox")
        and not e.get("dataIgnore")
        and COLLISION_MIN_AREA <= _rect_area(e["bbox"]) <= canvas_area * CONTAINER_MAX_AREA_RATIO
    ]
    issues: list[dict] = []
    for i in range(len(cands)):
        for j in range(i + 1, len(cands)):
            a, b = cands[i], cands[j]
            if a.get("groupId") is not None and a.get("groupId") == b.get("groupId"):
                continue
            inter = _rect_intersection_area(a["bbox"], b["bbox"])
            if inter <= 0:
                continue
            area_a, area_b = _rect_area(a["bbox"]), _rect_area(b["bbox"])
            smaller, larger = min(area_a, area_b), max(area_a, area_b)
            if smaller / larger < COLLISION_SIZE_RATIO:
                continue
            ratio = inter / smaller
            if ratio < COLLISION_MIN_OVERLAP or ratio >= COLLISION_CONTAIN_RATIO:
                continue
            issues.append({
                "code": "ELEMENT_COLLISION_AMBIGUOUS",
                "severity": "warning",
                "message": (
                    f"two graphics cross-overlap by {ratio * 100:.0f}% of the "
                    f"smaller box (peers, neither contains the other)"
                ),
                "elements": [_el_ref(a), _el_ref(b)],
                "bbox": {"a": a["bbox"], "b": b["bbox"]},
                "suggested_fix": "Confirm the overlap is intentional; align or separate if not.",
            })
    return issues


# ════════════════════════════════════════════════════════════════════════════
# SECTION 6: CLI & orchestration
# argparse surface, the per-page browser probing loop, and main() that wires
# server lifecycle → probe → checks → exit code together.
# ════════════════════════════════════════════════════════════════════════════

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="HTML/DOM geometry floor check for rendered SVG slides.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "project_path",
        help="Path to project directory (must contain svg_output/)",
    )
    parser.add_argument(
        "--pages", nargs="+", default=None,
        help="Page tokens to check (default: all SVGs in svg_output/). "
             "Accepts '02', '02_title', or '02_title.svg'.",
    )
    parser.add_argument(
        "--server-url", default=None,
        help="Override the live-preview server URL. Default: auto — reuse this "
             "project's running server via its lock file, else auto-start one.",
    )
    parser.add_argument(
        "--output", default=None,
        help="Report path (default: <project>/.layout_check/layout_report.json)",
    )
    parser.add_argument(
        "--fail-on-warning", action="store_true",
        help="Exit non-zero when only warnings are present (default: warnings pass)",
    )
    return parser


def probe_pages(server_url: str, pages: list[str]) -> list[dict]:
    """Run PROBE_JS against each page in one browser session, returning raw
    geometry per page (no judgment — that is the Python check layer in main).

    A single page that fails to fetch or whose probe throws is recorded as
    ``{page, render_failed: True, error}`` and the loop continues, per design's
    "one page's probe failing must not stop the others". A browser-launch
    failure propagates to the caller, which maps it to exit 3.
    """
    from playwright.sync_api import sync_playwright

    cfg = {
        "pageName": None,
        "fontsCeilingMs": FONTS_READY_CEILING_MS,
        "imageTimeoutMs": IMAGE_VERIFY_TIMEOUT_MS,
        "measuredTags": list(MEASURED_TAGS),
    }
    records: list[dict] = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        try:
            context = browser.new_context(viewport={"width": 1280, "height": 720})
            for page_name in pages:
                page_cfg = dict(cfg, pageName=page_name)
                try:
                    pg = context.new_page()
                    pg.goto(server_url, wait_until="domcontentloaded")
                    result = pg.evaluate(PROBE_JS, page_cfg)
                    pg.close()
                    result["page"] = page_name
                    records.append(result)
                except Exception as e:  # noqa: BLE001 — best-effort per page
                    records.append({
                        "page": page_name,
                        "render_failed": True,
                        "error": f"{type(e).__name__}: {e}",
                    })
        finally:
            browser.close()
    return records


def evaluate_page(rec: dict, expected_canvas: dict | None) -> dict:
    """Turn one raw probe record into a design-schema page result: run every
    check, bucket issues by severity, derive status and metrics. Pure — no I/O,
    no exit-code logic. A render_failed record yields a render_failed page with
    the probe error captured as a single pseudo-issue."""
    page = rec["page"]
    if rec.get("render_failed"):
        return {
            "page": page,
            "status": "render_failed",
            "metrics": {},
            "errors": [],
            "warnings": [{
                "code": "RENDER_FAILED",
                "severity": "warning",
                "message": rec.get("error", "probe failed"),
                "elements": [],
                "bbox": None,
                "suggested_fix": "Check the SVG renders in live preview.",
            }],
        }

    root = rec.get("root")
    elements = rec.get("elements", [])
    page_canvas = None
    if root and root.get("viewBoxW") and root.get("viewBoxH"):
        page_canvas = {"width": root["viewBoxW"], "height": root["viewBoxH"]}
    elif expected_canvas:
        page_canvas = expected_canvas

    issues: list[dict] = []
    if page_canvas:
        issues += check_out_of_bounds(elements, page_canvas)
        issues += check_container_overflow(elements, page_canvas)
        if COLLISION_ENABLED:
            issues += check_element_collision(elements, page_canvas)
    issues += check_root_dimension(root, expected_canvas)
    issues += check_images(elements)
    issues += check_text_overlap(elements)

    errors = [i for i in issues if i["severity"] == "error"]
    warnings = [i for i in issues if i["severity"] == "warning"]
    status = "error" if errors else ("warning" if warnings else "ok")

    counts = rec.get("counts", {})
    metrics = {
        "element_count": counts.get("element", 0),
        "text_count": counts.get("text", 0),
        "image_count": counts.get("image", 0),
        "checked_bbox_count": counts.get("checked_bbox", 0),
    }
    return {
        "page": page,
        "status": status,
        "metrics": metrics,
        "errors": errors,
        "warnings": warnings,
    }


def build_report(
    project_path: Path,
    server_url: str,
    canvas: dict | None,
    page_results: list[dict],
) -> dict:
    """Assemble the design-schema report root from evaluated page results.
    Summary counts pages by their status enum (ok/warning/error/render_failed)."""
    summary = {"pages": len(page_results), "ok": 0, "warning": 0, "error": 0, "render_failed": 0}
    for pr in page_results:
        summary[pr["status"]] = summary.get(pr["status"], 0) + 1
    return {
        "version": 1,
        "project": str(project_path),
        "server_url": server_url,
        "canvas": canvas,
        "summary": summary,
        "pages": page_results,
    }


def compute_exit_code(summary: dict, fail_on_warning: bool) -> int:
    """Exit code by design priority: render_failed (5) > hard error (4) >
    warning-with-flag (4) > 0. A page that could not be checked outranks a page
    with errors — 'a page went unchecked' is a worse floor breach than 'errors
    were found'. summary/report carry the full per-severity detail regardless."""
    if summary.get("render_failed", 0) > 0:
        return 5
    if summary.get("error", 0) > 0:
        return 4
    if fail_on_warning and summary.get("warning", 0) > 0:
        return 4
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    project_path = Path(args.project_path).resolve()
    if not project_path.is_dir():
        _safe_print(f"project path not found: {project_path}")
        return 2

    # validate svg_output/ before the heavier backend check: discover_pages
    # raises FileNotFoundError when svg_output/ is missing and ValueError on a bad
    # --pages token. Fail with exit 2 and no half-written report.
    try:
        pages = discover_pages(project_path, args.pages)
    except (FileNotFoundError, ValueError) as e:
        _safe_print(str(e))
        return 2

    # rendering backend is required for the DOM probe (added in later tasks).
    try:
        from playwright.sync_api import sync_playwright  # noqa: F401
    except ImportError:
        _safe_print(
            "playwright not installed. Install with:\n"
            "    pip install playwright\n"
            "    python3 -m playwright install chromium\n"
            "(see skills/ppt-master/requirements.txt)"
        )
        return 3

    # resolve a server: reuse this project's running one, or auto-start one we
    # own. Auto-start is what lets the floor hold even when nobody started a
    # preview manually (e.g. the VLM visual-review was skipped).
    try:
        base_url, proc = ensure_server(project_path, args.server_url)
    except RuntimeError as e:
        _safe_print(str(e))
        return 2

    # expected canvas from the spec lock (None when absent — dimension check
    # then skips rather than guessing). Resolved before the browser session so a
    # bad lock surfaces early.
    expected_canvas = resolve_canvas(project_path)

    try:
        records = probe_pages(base_url, pages)

        # evaluate every page into a design-schema page result (pure), print a
        # per-page severity summary, then assemble + write the JSON report.
        page_results = [evaluate_page(rec, expected_canvas) for rec in records]
        for pr in page_results:
            page, status = pr["page"], pr["status"]
            if status == "render_failed":
                msg = pr["warnings"][0]["message"] if pr["warnings"] else "probe failed"
                _safe_print(f"  {page}: render_failed — {msg}")
                continue
            errors, warnings = pr["errors"], pr["warnings"]
            if errors or warnings:
                parts = []
                if errors:
                    parts.append(f"{len(errors)} error(s)")
                if warnings:
                    parts.append(f"{len(warnings)} warning(s)")
                _safe_print(f"  {page}: " + ", ".join(parts))
                for i in errors + warnings:
                    _safe_print(f"      [{i['severity']}] {i['code']}: {i['message']}")
            else:
                _safe_print(f"  {page}: ok")

        report = build_report(project_path, base_url, expected_canvas, page_results)

        # write the JSON report (Report discipline: browser session started, so
        # write a complete report even when some pages render_failed).
        out_path = (
            Path(args.output) if args.output
            else project_path / ".layout_check" / "layout_report.json"
        )
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

        s = report["summary"]
        _safe_print(
            f"HTML layout check: {s['pages']} pages, {s['ok']} ok, "
            f"{s['warning']} warning, {s['error']} error"
            + (f", {s['render_failed']} render_failed" if s["render_failed"] else "")
        )
        _safe_print(f"Report: {out_path}")
        return compute_exit_code(s, args.fail_on_warning)
    finally:
        # R2: only reap a server we started ourselves — never a reused one (a
        # user's Step 6 live preview must survive this check).
        if proc is not None:
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()


if __name__ == "__main__":
    raise SystemExit(main())

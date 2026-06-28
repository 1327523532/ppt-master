---
description: Deterministic DOM geometry floor check for rendered slides. Run after svg_quality_checker.py, before visual-review and post-processing. Non-skippable.
---

# HTML Layout Check Workflow

> Standalone post-generation step. Goal: catch hard geometry defects — elements out of bounds, overlapping text, text overflowing its container, broken images — by rendering each page in headless Chromium and reading the browser's **real DOM geometry** (`getBBox` + `getCTM`). No VLM, no subjective judgment.
>
> Reads `<project>/svg_output/<page>.svg` through the live-preview server and reports per-page issues to `<project>/.layout_check/layout_report.json`. **Never touches** the SVGs, brand decisions, or any other file — it only measures and judges.
>
> This workflow is **independent** — invokable in a fresh chat session with only `<project_path>` as input. No upstream conversation context required.

## Positioning

This is the **deterministic floor** in a three-layer quality gate, sitting between the static checker and the subjective visual pass:

```
svg_quality_checker.py   →   html_layout_checker.py   →   visual-review
(regex on SVG source)        (real DOM geometry)          (VLM, subjective)
        static                    THIS WORKFLOW              opt-out-able
```

Unlike `visual-review`, this layer is **not opt-out-able**. Its entire reason to exist is to hold a geometry floor even when the user skips the VLM pass — so it runs on every deck and a non-zero exit blocks Step 7 (SKILL.md Step 6 → Step 7). Do not treat it like `visual-review`; there is no "skip layout check" path.

**Cost**: one headless render + DOM probe per page, all judgment in Python. No model tokens, no subagents — cheap relative to the VLM pass.

## When to Run

- Executor (SKILL.md Step 6) has finished all pages
- `svg_quality_checker.py` has passed
- Post-processing (`finalize_svg.py`, `svg_to_pptx.py`) has **not** yet run
- Always — there is no per-run opt-out

For decks containing data charts, run [`verify-charts`](./verify-charts.md) first — this checker measures bbox geometry, not chart coordinate math, and uncalibrated chart points can read as spurious overlaps.

## When NOT to Run

- The project has no `svg_output/<page>.svg` files yet — finish Executor first
- `svg_quality_checker.py` has not been run or has failed — fix static violations first
- After `finalize_svg.py` — finalize rewrites the SVG (tspan flattened, rect→path) and the report would describe the rebuilt artifact, not the design source. Always run against `svg_output/`.

---

## Prerequisites

```bash
# playwright + chromium installed (the headless renderer)
pip install playwright
python3 -m playwright install chromium
```

Unlike `visual_review.py`, this checker **auto-starts the live-preview server itself** — do NOT start one manually for it:

- If this project already has a live-preview server running (recorded in `<project>/live_preview/lock.json`), the checker **reuses** it and leaves it running.
- Otherwise the checker starts its own foreground server, uses it, and **reaps only that self-started process** on exit. A server you started yourself (Step 6 live preview) is never killed.

> **Why playwright, not cairosvg**: cairo's text API has no font-fallback chain, so CJK glyphs render as tofu boxes and their measured bbox is wrong. Playwright drives real chromium with `document.fonts.ready` awaited, producing the same geometry the live-preview browser shows — the only reliable measurement for bilingual decks.

---

## Step 1 — Run the check

```bash
python3 skills/ppt-master/scripts/html_layout_checker.py <project_path>
```

Optional flags:

- `--pages 02 03` — check specific page tokens only (accepts `02`, `02_title`, or `02_title.svg`); default is every SVG in `svg_output/`
- `--server-url http://localhost:5050` — override the live-preview URL; default is auto (reuse this project's running server via its lock, else auto-start)
- `--output <path>` — report path; default `<project>/.layout_check/layout_report.json`
- `--fail-on-warning` — exit non-zero on warnings too (default: warnings pass)

Exit codes are the gate:

- `0` — all requested pages pass, no hard error → proceed
- `2` — project path invalid, no `svg_output/`, or live-preview server unreachable
- `3` — playwright / chromium missing or unable to launch (see Prerequisites)
- `4` — checks ran, one or more **hard errors** present → must fix before Step 7
- `5` — a page failed to render or its DOM probe failed → must fix before Step 7

When several severities are present the exit code reports the worst: `5` > `4` > (`4` if `--fail-on-warning` and warnings) > `0`. The exit code is a single signal; the full per-page, per-severity detail is always in the JSON report.

### Issue codes

Hard errors (`severity: "error"` — block Step 7):

- `OUT_OF_BOUNDS` — an element's bbox extends past the canvas viewBox
- `ROOT_DIMENSION_MISMATCH` — the rendered root size disagrees with the spec_lock canvas
- `IMAGE_RENDER_BROKEN` — an `<image>` failed to load / decode
- `TEXT_OVERLAP` — two `<text>` runs from different logical blocks overlap beyond threshold
- `TEXT_CONTAINER_OVERFLOW` — text spills outside its inferred container (card / box)

Warnings (`severity: "warning"` — print + report, pass by default):

- `ELEMENT_COLLISION_AMBIGUOUS` — two non-text shapes overlap in a way that *might* be a mistake. **Off by default** (highest false-positive risk); enable with the env toggle:
  ```bash
  PPT_LAYOUT_COLLISION=1 python3 skills/ppt-master/scripts/html_layout_checker.py <project_path>
  ```
- `RENDER_FAILED` — surfaced as a per-page warning entry in the report when that page drove exit `5`

---

## Step 2 — Act on the result

- **Exit 0** — done; continue to `visual-review` (default-on) or post-processing per [`SKILL.md`](../SKILL.md) Step 7.
- **Exit 4** — open the JSON report, read each `error` entry's element ref + bbox, return to Visual Construction, regenerate the offending page, re-run the check. Do not proceed to Step 7 with errors outstanding.
- **Exit 5** — a page rendered blank or its probe threw. Usually a broken `<use>` / missing image / server hiccup. Re-run for that page only (`--pages <token>`); if it persists, inspect the SVG.
- **Exit 2 / 3** — environment problem, not a deck problem. Fix per Prerequisites (install playwright, ensure `svg_output/` exists) and re-run.

Before declaring any reported error a false positive, **read the actual bbox numbers in the report** and compare them to the container/canvas bounds. Do not dismiss a finding from a chart-type assumption or a glance at the rendered image — the checker reports real geometry, and visual impression has misjudged it before.

---

## Notes & invariants

- **Measures, never edits**: this checker reads DOM geometry and writes a report. It does not modify `svg_output/`. All fixes are made by regenerating the page in Visual Construction.
- **svg_output, not svg_final**: always run before `finalize_svg.py`. The rebuilt `svg_final` flattens text and reshapes elements; a report against it describes the effect, not the design source.
- **Server discipline**: the checker resolves the server via `<project>/live_preview/lock.json` and never blind-probes a port. A reused server is left running; only a self-started server is reaped on exit.
- **Thresholds live in Python**: the injected probe JS measures only; every tolerance (canvas, overlap ratio, container min-side, CJK font factor, collision floors) is a Python constant in SECTION 1 of the script. Tune there, never in the probe.
- **The floor is not the designer**: it catches hard geometry defects, not weak layout. Subjective rhythm / alignment / hierarchy is `visual-review`'s job.

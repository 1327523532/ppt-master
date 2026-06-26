# SVG Icon Library

PPT Master draws on **11,600+ high-quality SVG icons** across five libraries. Four are stylistic libraries (pick **one** per deck); one is a brand-logo library (`simple-icons`) used as an inset alongside the chosen stylistic library.

> **The full SVGs no longer ship with the skill.** This directory ships only a lightweight **name index** (`index/<lib>.txt`, one icon name per line) for discovery — keeping installs to a handful of files instead of 11k. The real SVGs are hosted remotely (`<ICON_BASE_URL>/<lib>/<name>.svg`) and fetched on demand into a deck's own `<project>/icons/` only for the icons it actually uses. Set `ICON_BASE_URL` in `.env`; see `.env.example`.

## Libraries

| Library | Style | Count | viewBox | Prefix |
|---------|-------|-------|---------|--------|
| `chunk-filled` | fill · straight-line geometry (sharp corners, rectilinear) | 640 | `0 0 16 16` | `chunk-filled/` |
| `tabler-filled` | fill · bezier-curve forms (smooth, rounded contours) | 1000+ | `0 0 24 24` | `tabler-filled/` |
| `tabler-outline` | stroke / line | 5000+ | `0 0 24 24` | `tabler-outline/` |
| `phosphor-duotone` | duotone · single color + 0.2 opacity backplate (soft depth) | 1200+ | `0 0 256 256` | `phosphor-duotone/` |
| `simple-icons` | **brand logos** (real company / product marks) — single-color silhouettes, color in via `fill` | 3400+ | `0 0 24 24` | `simple-icons/` |

---

## Per-project icons folder

At selection time the Strategist fetches the chosen icons into the deck's own `<project>/icons/<lib>/` with `icon_sync.py` — each is downloaded on demand from `<ICON_BASE_URL>/<lib>/<name>.svg`:

```bash
python3 skills/ppt-master/scripts/icon_sync.py <project_path> chunk-filled/home tabler-outline/bulb
```

A name absent from the library's name index is reported and the command exits non-zero — re-pick a real one then, not at export. (A name in the index that fails to download is reported separately as a fetch failure — check `ICON_BASE_URL` / network, don't re-pick.) `finalize_svg.py embed-icons` embeds **project-first** (from `<project>/icons/`); an icon still missing at export is fetched on demand as a last resort, else its placeholder is kept.

**Custom icons**: drop your own `.svg` into `<project>/icons/<lib>/` (any `<lib>`, e.g. `custom/`) and reference it as `data-icon="<lib>/<name>"` — it embeds like any library icon.

## Usage

Use placeholder syntax **during SVG generation**:

```xml
<!-- chunk-filled (sharp, geometric — tech/engineering/enterprise tone) -->
<use data-icon="chunk-filled/home" x="100" y="200" width="48" height="48" fill="#0076A8"/>

<!-- tabler-filled (rounded, organic — lifestyle/health/home tone) -->
<use data-icon="tabler-filled/home" x="100" y="200" width="48" height="48" fill="#0076A8"/>

<!-- tabler-outline (light, line-art — refined screen-only showcases) -->
<use data-icon="tabler-outline/home" x="100" y="200" width="48" height="48" fill="#0076A8"/>

<!-- phosphor-duotone (soft depth — single color renders the backplate at 20% opacity) -->
<use data-icon="phosphor-duotone/house" x="100" y="200" width="48" height="48" fill="#0076A8"/>

<!-- simple-icons (brand logo — used alongside the deck's primary library, not as a substitute) -->
<use data-icon="simple-icons/github" x="100" y="200" width="48" height="48" fill="#181717"/>
```

**Attributes**:
- `data-icon` — `<library>/<icon-name>` (filename without `.svg`)
- `x`, `y` — Position
- `width`, `height` — Size (recommend 32–48px for legibility)
- `fill` — Color

`finalize_svg.py` auto-embeds all placeholders during post-processing. To run manually:

```bash
python3 scripts/svg_finalize/embed_icons.py svg_output/*.svg
```

---

## Searching for Icons

Grep the name index — zero token cost (the full SVGs are not shipped; only `index/<lib>.txt`):

```bash
grep home skills/ppt-master/templates/icons/index/chunk-filled.txt
grep home skills/ppt-master/templates/icons/index/tabler-filled.txt
grep chart skills/ppt-master/templates/icons/index/tabler-outline.txt
grep house skills/ppt-master/templates/icons/index/phosphor-duotone.txt
grep github skills/ppt-master/templates/icons/index/simple-icons.txt
```

---

## Style Rules

**No default library — actively choose based on the deck's visual needs.** Read the source material first, then pick the library whose visual character best serves the presentation. Each library has a distinct visual personality:

- **`chunk-filled`** — **fill** style, built from straight-line commands only (M/L/H/V/Z). Sharp, precise right angles; rectilinear geometry; structured and highly legible at small sizes. Visual weight: heavy, solid, architectural.
- **`tabler-filled`** — **fill** style, built from bezier curves and arcs (C/A). Smooth, rounded, organic contours; warmer and softer than `chunk-filled`. Visual weight: medium, approachable.
- **`tabler-outline`** — **stroke** style (line art, default stroke-width 2). Airy, refined, lightweight; uses negative space. Visual weight: light, elegant. Best for screen-only viewing since thin strokes may become hard to read when printed or projected.
- **`phosphor-duotone`** — **duotone** style; main shape at full opacity plus a backplate of the same color at 20% opacity, producing a soft sense of depth. Visual weight: medium, layered, contemporary.

> **Two axes to consider when choosing**:
> 1. **Geometry**: straight lines (`chunk-filled`) vs. curves (`tabler-filled` / `phosphor-duotone`) vs. open strokes (`tabler-outline`)
> 2. **Visual weight**: heavy solid (`chunk-filled`) → medium solid (`tabler-filled`) → medium layered (`phosphor-duotone`) → light stroke (`tabler-outline`)

**One presentation = one stylistic library.** Pick `chunk-filled` / `tabler-filled` / `tabler-outline` / `phosphor-duotone` at the start and use it exclusively throughout for generic icons (home, chart, users, etc.). If the chosen library doesn't have an exact icon, find the closest available alternative within that same library — never cross stylistic libraries to fill a gap.

**Brand-logo exception (`simple-icons`).** `simple-icons` is **not a stylistic library** and does not participate in the "one library" rule. Its job is brand recognition — Slack's purple, GitHub's cat, AWS's color — which is intentionally heterogeneous. Use it **alongside** the chosen stylistic library, but **only** for actual company / product / service brand marks. Do **not** reach for it as a substitute when the chosen stylistic library lacks a generic icon.

| Use `simple-icons` for | Do NOT use `simple-icons` for |
|------------------------|-------------------------------|
| Customer / partner / ecosystem logos on a "trusted by" page | Generic concepts (home, chart, settings, etc.) |
| Tech stack icons on architecture / integration diagrams | Replacing a missing icon in `chunk-filled` / `tabler-*` / `phosphor-duotone` |
| Social media handles in a footer | Decorative / illustrative purposes |

⚠️ Do **not** mix icons from different **stylistic** libraries (`chunk-filled` / `tabler-filled` / `tabler-outline` / `phosphor-duotone`). `simple-icons` is the sole exception and may co-exist as a brand-logo inset — see the brand-logo exception above.

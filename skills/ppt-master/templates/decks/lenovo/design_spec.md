---
deck_id: lenovo
kind: deck
summary: Lenovo corporate deck — branded cover (replaceable title), TOC, chapter divider, content (open frame), and thanks page, light & dark themes
canvas_format: ppt169
page_count: 9
page_types: [cover, cover_dark, toc, toc_dark, chapter, content, content_dark, ending, ending_dark]
primary_color: "#E1251B"
placeholders: [TITLE, SUBTITLE, DECK_TITLE, PAGE_TITLE, KEY_MESSAGE, CONTENT_AREA, PAGE_NUM, TOTAL_PAGES, CHAPTER_TITLE, CHAPTER_DESC, CHAPTER_LABEL, TOC_ITEM_1_TITLE, TOC_ITEM_1_DESC, TOC_ITEM_2_TITLE, TOC_ITEM_2_DESC, TOC_ITEM_3_TITLE, TOC_ITEM_3_DESC, TOC_ITEM_4_TITLE, TOC_ITEM_4_DESC, TOC_ITEM_5_TITLE, TOC_ITEM_5_DESC, TOC_ITEM_6_TITLE, TOC_ITEM_6_DESC]
---

# Lenovo Deck — Design Specification

> Deck = identity + structure + middle. This deck ships a **ready-to-use** cover, TOC, chapter divider, content frame, and thanks / ending page — all with the Lenovo wordmark baked in and a per-theme variant (light + dark) for every page except the chapter divider, which is dark by design (a section break is a visual moment). Source artifacts live in `../brands/lenovo/sources/`; the active theme picks which variant the Strategist renders.

> **Use case**: corporate / executive decks, product launches, internal town halls, sales enablement, training material — any deck that opens with a Lenovo cover, lists 2-6 sections on a TOC, breaks into chapters, and closes with a Lenovo thanks. The content page ships an open `{{CONTENT_AREA}}` for the Strategist to inject any Layout Mode (Single Column, Two-Column 5:5 / 4:6, Three-Column Cards, Table, Timeline, Card Grid) from the standard library.

## I. Template Overview

| Property | Value |
|---|---|
| Display Name | Lenovo Branded Deck |
| Use Cases | Corporate / executive decks, product launches, internal town halls, sales enablement, training material |
| Source | `ref/Lenovo PPT Template 1*.potx` (cover = slide 1, section header = slide 9/13, agenda = slide 29, thanks = slide 15); `ref/Lenovo PPT Template 2.potx` for archetype inspiration |
| Tone | Professional, restrained, globally consistent, conclusion-first |
| Theme Selection | User picks `light` or `dark` at SKILL.md Step 4 (Eight Confirmations). Default `light` per the brand's `default_theme`. |

The deck now ships **5 page archetypes** (cover / TOC / chapter / content / thanks) with **9 SVG files** (every archetype except chapter has a light + dark pair). Logo placement follows the brand spec §IV: top-left on cover, TOC, chapter, thanks; top-right corner mark on content pages.

## II. Canvas Specification

| Field | Value |
|---|---|
| Format | `ppt169` (PowerPoint widescreen 16:9) |
| EMU | 12,188,825 × 6,858,000 |
| Inches | 13.333 × 7.5 |
| viewBox | `0 0 1280 720` (96 px-per-inch) |
| Margins | Left/right 0.82" (≈ 78 px), top 0.83" (≈ 80 px), bottom 0.50" (≈ 48 px) |
| Content area (content page) | x: 72 → 1210, y: 216 → 620 (1138 × 404 px) — matches `招商银行` 03_content.svg open-frame geometry |
| Color space | sRGB; HEX only |

## III. Color Scheme

Color values are mirrored from `../brands/lenovo/design_spec.md` §II. The Strategist picks the table matching the user's chosen theme; SVGs in this directory embed the values directly so the files render correctly on their own.

| Token | Light | Dark | Use |
|---|---|---|---|
| bg | `#FFFFFF` | `#191919` | Slide background |
| text | `#1A1A1A` | `#F2F2F2` | Title / subtitle / footer copy |
| muted-text | `#6B6B6B` | `#A0A0A0` | Secondary copy, axis labels, deck title in footer center |
| border | `#E0E0E0` | `#3A3A3A` | Dividers, content-area dashed outline |
| primary | `#E1251B` | `#E1251B` | Lenovo Red — accent under titles, key-message bar |
| accent (lavender) | `#D9C1D8` | `#D9C1D8` | TOC numbered-circle fill (stays lavender on both themes — the bright spot) |
| wordmark | `logo-light.png` (purple) | `logo-dark.png` (white) | Brand mark on every page |

## IV. Typography

| Role | Family | Weight | Size |
|---|---|---|---|
| Cover title | `Arial, "Microsoft YaHei", 黑体, sans-serif` | 700 | 43 pt (matches source `slideMaster1.titleStyle` `sz="4300"`) |
| Cover subtitle | `Arial, "Microsoft YaHei", 黑体, sans-serif` | 400 | 18 pt |
| Cover / chapter / TOC / content footer | `Arial, "Microsoft YaHei", 黑体, sans-serif` | 400 | 10 pt (left + right zones) |
| Footer center deck title | `Arial, "Microsoft YaHei", 黑体, sans-serif` | 400 | 9 pt italic, `muted-text` color |
| TOC title | `Arial, "Microsoft YaHei", 黑体, sans-serif` | 700 | 32 pt (e.g. "Contents") |
| TOC item title | `Arial, "Microsoft YaHei", 黑体, sans-serif` | 700 | 18 pt |
| TOC item desc | `Arial, "Microsoft YaHei", 黑体, sans-serif` | 400 | 14 pt, `muted-text` color |
| TOC number (in circle) | `Arial, "Microsoft YaHei", 黑体, sans-serif` | 700 | 28 pt, near-black (`#1A1A1A`) on the lavender circle |
| Chapter title | `Arial, "Microsoft YaHei", 黑体, sans-serif` | 700 | 54 pt |
| Chapter desc | `Arial, "Microsoft YaHei", 黑体, sans-serif` | 400 | 20 pt, `muted-text` color |
| Content page title | `Arial, "Microsoft YaHei", 黑体, sans-serif` | 700 | 28 pt |
| Content key message | `Arial, "Microsoft YaHei", 黑体, sans-serif` | 400 | 16 pt, `muted-text` color |
| Content open-area hint | `Arial, "Microsoft YaHei", 黑体, sans-serif` | 400 | 20 pt, `border` color (faint, signals "fill me") |
| Thanks title | `Arial, "Microsoft YaHei", 黑体, sans-serif` | 700 | 96 pt |

> Source title style: 43 pt, all caps via `cap="all"` transform, centered. The cover title is rendered with `text-transform: uppercase` so any `{{TITLE}}` text displays in caps regardless of the user's input case.

### IV.5 `{{DECK_TITLE}}` injection

The 3-zone footer center text on every content-style page (`02_toc.svg`, `02_chapter.svg`, `03_content*.svg`) is `{{DECK_TITLE}}` — italic 9 pt, `muted-text` color (see §IV Typography row "Footer center deck title"). The Strategist defaults `{{DECK_TITLE}}` to the same value as the cover's `{{TITLE}}` (the deck's headline). The user can override at Eight Confirmations to a different deck-level title if the cover title and the running header differ (for example a deck titled "Q3 Planning Workshop" on the cover but branded "FY26 Strategy Series" in the footer). If the user supplies no override, the Strategist copies the cover `{{TITLE}}` text into every content-style page's footer center.

## V. Logo

| File | Form | Theme | Usage on these pages |
|---|---|---|---|
| `./logo-light.png` | "Lenovo." wordmark in `#4D144A` deep purple, 1288×291 px, transparent bg | light | Top-left of `01_cover.svg`, `02_toc.svg`, `04_ending.svg`; top-right corner mark of `03_content.svg` |
| `./logo-dark.png` | "Lenovo." wordmark in white, 1288×291 px, transparent bg | dark | Top-left of `01_cover_dark.svg`, `02_toc_dark.svg`, `04_ending_dark.svg`, `02_chapter.svg`; top-right corner mark of `03_content_dark.svg` |

- Cover / TOC / chapter / thanks: top-left, `x=78, y=80, width=160, height=36` px (≈ 1.63" × 0.375")
- Content page corner mark: top-right, `x=1142, y=50, width=100, height=22` px (smaller, "watermark" weight)
- Clearspace: ≥ 0.5× wordmark height on all sides; never overlap text, page-number element, or the dashed `{{CONTENT_AREA}}` outline
- Source: extracted from `ref/Lenovo PPT Template 1 - 浅色.potx` `ppt/media/image1.png`; dark variant is a recolor of the light artwork

## VI. Layout Sketches

Five layout sketches for the five page archetypes. Wordmark position is shown in the top-left corner; on `03_content.svg` it moves to the top-right (corner mark).

### Cover layout (01_cover.svg, 01_cover_dark.svg)

```
+--------------------------------------------------------------+
| [logo]                                                       |  ← y=80
|                                                              |
|                                                              |
|                   {{TITLE}} (43 pt, centered, caps)         |  ← y=332
|                                                              |
|                                                              |
|                 {{SUBTITLE}} (18 pt, centered)               |  ← y=548
|                                                              |
| ©2026 Lenovo Internal. ...    {{DECK_TITLE}}    1 / 12      |  ← y=685
+--------------------------------------------------------------+
```

### TOC layout (02_toc.svg, 02_toc_dark.svg)

```
+--------------------------------------------------------------+
| [logo]                                                       |  ← y=80
| Contents                                          (red bar)  |  ← y=160
|                                                              |
|  (1)  {{TOC_ITEM_1_TITLE}}       (4)  {{TOC_ITEM_4_TITLE}}  |
|       {{TOC_ITEM_1_DESC}}             {{TOC_ITEM_4_DESC}}   |
|                                                              |
|  (2)  {{TOC_ITEM_2_TITLE}}       (5)  {{TOC_ITEM_5_TITLE}}  |
|       {{TOC_ITEM_2_DESC}}             {{TOC_ITEM_5_DESC}}   |
|                                                              |
|  (3)  {{TOC_ITEM_3_TITLE}}       (6)  {{TOC_ITEM_6_TITLE}}  |
|       {{TOC_ITEM_3_DESC}}             {{TOC_ITEM_6_DESC}}   |
|                                                              |
| ©2026 Lenovo Internal. ...    {{DECK_TITLE}}    2 / 12      |  ← y=685
+--------------------------------------------------------------+
```

6 lavender (#D9C1D8) circles, 68 px diameter, 2 columns × 3 rows. Numbers 1-6 in 28 pt near-black inside the circles; titles in 18 pt; descriptions in 14 pt muted-text. The Strategist can hide items 4-6 by leaving the placeholders empty if the deck has fewer sections.

### Chapter layout (02_chapter.svg) — dark only

```
+--------------------------------------------------------------+
| [logo] (white wordmark on dark)                              |  ← y=80
|                                                              |
|                                                              |
|                                                              |
|                                                              |
|              {{CHAPTER_TITLE}} (54 pt, centered)            |  ← y=335
|                                                              |
|              {{CHAPTER_DESC}} (20 pt, centered, muted)      |  ← y=395
|                                                              |
|                                                              |
|                                                              |
| ©2026 Lenovo Internal. ...    {{DECK_TITLE}}    3 / 12      |  ← y=685
+--------------------------------------------------------------+
```

Single dark variant — a section break is a visual moment, not a theme choice. No oversized chapter numeral or decorative shapes (per source `ref/Lenovo PPT Template 1.potx` slide 9/13 minimal style).

### Content layout (03_content.svg, 03_content_dark.svg)

```
+--------------------------------------------------------------+
|                                              [logo] (corner) |  ← y=50
|                                                              |
| {{PAGE_TITLE}} (28 pt, left)                                |  ← y=124
| ──────── (red accent, 160 px)                                |
| | {{KEY_MESSAGE}} (16 pt, muted, optional)                   |  ← y=181
|                                                              |
|  ┌──────────────────────────────────────────────────────┐   |
|  │                                                      │   |
|  │             {{CONTENT_AREA}}                        │   |  ← y=216..620
|  │             (Strategist fills                       │   |   (1138 × 404)
|  │              with Layout Mode)                      │   |
|  │                                                      │   |
|  └──────────────────────────────────────────────────────┘   |
|                                                              |
| ©2026 Lenovo Internal. ...    {{DECK_TITLE}}    4 / 12      |  ← y=685
+--------------------------------------------------------------+
```

Open `{{CONTENT_AREA}}` (1138 × 404 px, dashed outline for visibility) lets the Strategist render any of the standard Layout Modes (Single Column, Two-Column 5:5 / 4:6, Three-Column Cards, Table, Timeline, Card Grid) into the body. The `{{KEY_MESSAGE}}` slot is optional — the Strategist hides the red bar + text if the message is empty.

### Thanks layout (04_ending.svg, 04_ending_dark.svg)

```
+--------------------------------------------------------------+
| [logo]                                                       |  ← y=80
|                                                              |
|                                                              |
|                                                              |
|                   Thanks (96 pt, centered)                   |  ← y=360
|                                                              |
|                                                              |
+--------------------------------------------------------------+
```

No footer / no page number / no corner mark on the thanks page (per brand spec §VII.4).

## VII. Page Types

| Page | Source slide | Roster file(s) | Placeholders | Static text |
|---|---|---|---|---|
| Cover | slide 1 (slideLayout1) | `01_cover.svg`, `01_cover_dark.svg` | `{{TITLE}}`, `{{SUBTITLE}}` | Footer: `©2026 Lenovo Internal. All rights reserved.` (Internal classification, user-swappable to Unclassified / Confidential / Restricted) |
| TOC | slide 29 (agenda, layout 8) | `02_toc.svg`, `02_toc_dark.svg` | `{{TOC_ITEM_1_TITLE}}`…`{{TOC_ITEM_6_TITLE}}` and matching `_DESC` placeholders | "Contents" heading + 3-zone footer |
| Chapter | slide 9 / 13 (Section Header) | `02_chapter.svg` (dark only) | `{{CHAPTER_TITLE}}`, `{{CHAPTER_DESC}}` | 3-zone footer (still present on the dark page, per brand spec §VII.2) |
| Content | (open frame — no source) | `03_content.svg`, `03_content_dark.svg` | `{{PAGE_TITLE}}`, `{{KEY_MESSAGE}}`, `{{CONTENT_AREA}}` | 3-zone footer; the `{{CONTENT_AREA}}` is the Strategist's injection point |
| Thanks | slide 15 (slideLayout28) | `04_ending.svg`, `04_ending_dark.svg` | — | `Thanks` (literal, 96 pt) |

> **3-zone footer** (all content-style pages): left = classification line, center = `{{DECK_TITLE}}` (italic 9 pt muted), right = `{{PAGE_NUM}} / {{TOTAL_PAGES}}` in the format mandated by the brand spec §VII.2 / §VII.3. The classification level defaults to `Internal`; the user can switch to Unclassified / Confidential / Restricted at Eight Confirmations. The cover and thanks pages are exceptions — cover keeps the classification footer (per source), thanks has no footer at all (per brand spec §VII.4).

## VIII. Page Roster

| File | Theme | Renders |
|---|---|---|
| `01_cover.svg` | light | Cover with purple wordmark top-left, white bg, dark text, `{{TITLE}}` and `{{SUBTITLE}}` placeholders |
| `01_cover_dark.svg` | dark | Cover with white wordmark top-left, near-black bg, light text, same placeholders |
| `02_toc.svg` | light | TOC: purple wordmark top-left, "Contents" + red accent, 6 lavender numbered circles in 2×3 grid, `{{TOC_ITEM_N_TITLE}}` + `{{TOC_ITEM_N_DESC}}` placeholders |
| `02_toc_dark.svg` | dark | TOC: white wordmark top-left, near-black bg, same 6 circles, light text for titles |
| `02_chapter.svg` | dark only | Section divider: white wordmark top-left, near-black bg, centered `{{CHAPTER_TITLE}}` (54 pt) + `{{CHAPTER_DESC}}` (20 pt), 3-zone footer |
| `03_content.svg` | light | Content: small purple wordmark as top-right corner mark, `{{PAGE_TITLE}}` top-left with red accent, `{{KEY_MESSAGE}}` with red left bar, dashed `{{CONTENT_AREA}}` (1138×404), 3-zone footer |
| `03_content_dark.svg` | dark | Content: white wordmark as top-right corner mark, near-black bg, same chrome |
| `04_ending.svg` | light | Thanks: purple wordmark top-left, white bg, dark text, literal "Thanks" |
| `04_ending_dark.svg` | dark | Thanks: white wordmark top-left, near-black bg, light text, literal "Thanks" |

Strategist selects the matching pair at render time based on the user's chosen theme (`themes[0]` = light, `themes[1]` = dark; default = `default_theme` from `../brands/lenovo/design_spec.md` frontmatter). The chapter is the only page without a light/dark pair.

---

## IX. Layout Modes

The `03_content.svg` open frame `{{CONTENT_AREA}}` is `x: 72 → 1210, y: 216 → 620` — **1138 × 404 px** (width × height, with a `4 4` dashed border in `border` color so the Strategist can see the work area). All Layout Mode dimensions below are expressed in **local coordinates inside that 1138 × 404 content area** (top-left = `0, 0`); add `72` to the local `x` and `216` to the local `y` when emitting into the parent SVG.

The Strategist picks one Layout Mode per content page. Mode vocabulary mirrors `templates/layouts/government_blue` and `templates/layouts/government_red` §VI "Layout Modes" (the canonical `Layout Modes` wording across the layout library — see also `academic_defense` §VI "Layout Patterns" and `pixel_retro` §VI "Layout Modes" for cross-references). All modes use the Lenovo light-theme color tokens from §III (background: `bg`, primary text: `text`, dividers: `border`, accents: `primary` `#E1251B` and `accent` lavender `#D9C1D8`). Icons (if used) come from the project's chosen stylistic library via `<use data-icon="...">` and follow the rules in `templates/icons/README.md`.

### IX.1 Single Column

One full-width text block, vertically centered inside the content area.

```
+---------------------------------------------------+
|                                                   |
|   {{ITEM_TITLE}}                                  |
|   {{ITEM_BODY}}                                   |
|                                                   |
+---------------------------------------------------+
```

- **Dimensions**: 1138 × 404 (full area). Text column inset `x=0, y=0`, body block `width=1138, height=404`.
- **Placeholders** consumed: `{{ITEM_TITLE}}` (heading, 24 pt, `text` color), `{{ITEM_BODY}}` (paragraph, 16 pt, `text` color, multi-line via `<tspan>`); `{{PAGE_TITLE}}` and `{{KEY_MESSAGE}}` outside the content area remain from the page frame.
- **When to use**: A single key takeaway, definition, executive summary, or quote that needs full reading width. Use when the body of the slide is one idea and side-by-side comparison would dilute it.

### IX.2 Two-Column 5:5

Equal split, two cards side by side with a centered gap.

```
+-------------------------+ gap +-------------------------+
| {{ITEM_1_TITLE}}        |     | {{ITEM_2_TITLE}}        |
| {{ITEM_1_BODY}}         |     | {{ITEM_2_BODY}}         |
+-------------------------+     +-------------------------+
```

- **Dimensions**: each card `width = (1138 - 24) / 2 = 557 px`, `height = 404 px`. Card 1 at local `x=0`; card 2 at local `x=581`. Inter-card gap: 24 px. Inset: 16 px from the top of the content area.
- **Placeholders** consumed: `{{ITEM_1_TITLE}}`, `{{ITEM_1_BODY}}`, `{{ITEM_2_TITLE}}`, `{{ITEM_2_BODY}}` (2 columns). Each title is 20 pt bold, each body 14 pt regular; both in `text` color. Cards use a 1 px `border`-color outline or a 1 px top accent bar in `primary` red.
- **When to use**: Two-paragraph comparison, before/after, problem/solution, "old approach vs. new approach", or any two concepts of equal weight.

### IX.3 Two-Column 4:6

Narrow left + wide right. Left column suits a quoted message, label, or KPI; right column carries explanation or detail.

```
+-------------+      +-----------------------------------+
| {{LEFT_     |      | {{RIGHT_TITLE}}                   |
|  TITLE}}    |      | {{RIGHT_BODY}}                    |
| {{LEFT_     |      |                                   |
|  BODY}}     |      |                                   |
+-------------+      +-----------------------------------+
```

- **Dimensions**: left card `width = (1138 - 24) × 0.4 ≈ 446 px`, `height = 404 px`, local `x=0`. Right card `width = (1138 - 24) × 0.6 ≈ 668 px`, `height = 404 px`, local `x=470`. Inter-column gap: 24 px.
- **Placeholders** consumed: `{{LEFT_TITLE}}` (20 pt bold), `{{LEFT_BODY}}` (14 pt; typically a short quote, a single stat, or a "key message" sentence), `{{RIGHT_TITLE}}` (20 pt bold), `{{RIGHT_BODY}}` (14 pt; 3–5 lines of explanation). Left column may render a top accent bar in `accent` lavender to mirror the TOC circles.
- **When to use**: Image-left + text-right, definition-left + examples-right, key-quote-left + supporting-detail-right, or any "lead with the message, follow with the explanation" pairing.

### IX.4 Three-Column Cards

Three equal cards in a row, each with a small accent header and 2–4 lines of body text.

```
+----------+ gap +----------+ gap +----------+
| header 1 |     | header 2 |     | header 3 |
| body  1  |     | body  2  |     | body  3  |
+----------+     +----------+     +----------+
```

- **Dimensions**: each card `width = (1138 - 32) / 3 ≈ 369 px`, `height = 404 px`. Card N at local `x = N × (369 + 16)` for N = 0, 1, 2. Inter-card gap: 16 px. Top accent bar: 4 px tall, full card width, in `primary` red.
- **Placeholders** consumed: `{{ITEM_1_TITLE}}`, `{{ITEM_1_BODY}}`, `{{ITEM_2_TITLE}}`, `{{ITEM_2_BODY}}`, `{{ITEM_3_TITLE}}`, `{{ITEM_3_BODY}}` (3 columns). Each title 18 pt bold, each body 13 pt regular. Optional `{{ITEM_N_ICON}}` per column when a stylistic-library icon is appropriate (e.g. `chunk-filled/shield`, `tabler-outline/users`).
- **When to use**: Three pillars, three takeaways, three product lines, three audience segments, three principles. Best when each column is a distinct, equal-weight concept and the body fits in 2–4 lines.

### IX.5 Timeline

Horizontal axis with 3–5 node markers; each node carries a date/label above and a description below.

```
   2023         2024         2025         2026
   (●)──────────(●)──────────(●)──────────(●)
   {{NODE_1_    {{NODE_2_    {{NODE_3_    {{NODE_4_
    LABEL}}      LABEL}}      LABEL}}      LABEL}}
   {{NODE_1_    {{NODE_2_    {{NODE_3_    {{NODE_4_
    DESC}}       DESC}}       DESC}}       DESC}}
```

- **Dimensions**: axis line at local `y = 160`, full content-area width `x = 24 → 1114`. Node count **N = 3, 4, or 5**; node centers evenly spaced. For N nodes, node X = `24 + k × (1090 / (N − 1))` for `k = 0 … N−1`. Node dot: 14 px diameter, filled `primary` red. Date/label: 14 pt bold, 32 px above the line. Description: 12 pt regular, 32 px below the line, width capped at `1090 / N − 16` px.
- **Placeholders** consumed: `{{NODE_K_LABEL}}`, `{{NODE_K_DESC}}` for K = 1..N. Date/label rendered in `text` color, description in `muted-text`.
- **When to use**: Chronological milestones, project phases, roadmap, history, evolution. Best when the page is telling a "first A, then B, then C" story and each step deserves a few words of explanation.

### IX.6 Comparison Table

A single static table; row/column count is per-instance. For data-heavy grids (numerical comparisons, spec lists), use a 2–4 column × 2–6 row table.

```
+----------+--------------+--------------+--------------+
| Header 1 | {{COL_1_HDR}} | {{COL_2_HDR}} | {{COL_3_HDR}} |
+----------+--------------+--------------+--------------+
| {{ROW_1_LABEL}} | {{ROW_1_C1}} | {{ROW_1_C2}} | {{ROW_1_C3}} |
+----------+--------------+--------------+--------------+
| {{ROW_2_LABEL}} | {{ROW_2_C1}} | {{ROW_2_C2}} | {{ROW_2_C3}} |
+----------+--------------+--------------+--------------+
```

- **Dimensions**: outer table `width = 1138 px`, `height ≤ 404 px`. Column widths sum to 1138; first column ("label") gets 30% of the width, remaining columns split the rest evenly. Header row height: 44 px; body row height: `min(60, (404 − 44) / row_count)`. Header background: `border` color (light) or `text` color with white fill text (dark theme). Body rows alternate `bg` and a 4% `border` tint.
- **Placeholders** consumed: `{{COL_C_HDR}}` for C = 1..col_count, and `{{ROW_R_LABEL}}` + `{{ROW_R_Cc}}` for R = 1..row_count. Header text 14 pt bold; body 13 pt regular; first column (label) bold.
- **When to use**: Side-by-side specifications, plan tiers, scoring rubrics, before/after metrics, "option A vs. B vs. C" matrices. Use when the data is naturally tabular and a card grid would lose the alignment.

### IX.7 Card Grid 2×2

Four equal cards in a 2×2 arrangement. Best when the content is grouped into 4 short, similar-weight ideas.

```
+--------------------+ gap +--------------------+
| {{ITEM_1_TITLE}}   |     | {{ITEM_2_TITLE}}   |
| {{ITEM_1_BODY}}    |     | {{ITEM_2_BODY}}    |
+--------------------+     +--------------------+
| {{ITEM_3_TITLE}}   |     | {{ITEM_4_TITLE}}   |
| {{ITEM_3_BODY}}    |     | {{ITEM_4_BODY}}    |
+--------------------+     +--------------------+
```

- **Dimensions**: each card `width = (1138 − 24) / 2 = 557 px`, `height = (404 − 16) / 2 = 194 px`. Cards at local `(x, y)` = `(0, 0)`, `(581, 0)`, `(0, 210)`, `(581, 210)`. Inter-card gap: 24 px horizontal, 16 px vertical. Each card carries a 4 px left accent bar in `primary` red and 16 px internal padding.
- **Placeholders** consumed: `{{ITEM_N_TITLE}}`, `{{ITEM_N_BODY}}` for N = 1..4. Each title 18 pt bold, each body 13 pt regular, max 3 lines.
- **When to use**: Four principles, four phases (when a horizontal timeline is too wide), four pillars of a strategy, four user-persona highlights. Use when the page has four equal-weight ideas that don't form a sequence (if they form a sequence, prefer Timeline §IX.5).

---

> **Strategist notes for picking a mode**:
> 1. The page-level `{{PAGE_TITLE}}` (28 pt) and optional `{{KEY_MESSAGE}}` (16 pt, red left bar) sit **above** the content area and are independent of the mode choice.
> 2. If the source has a clearly defined **chart** (e.g. revenue over time, market share), drop the chart directly into the content area (using `templates/charts/<name>.svg` as a layout guide) and pick the closest of the modes above — usually Timeline (§IX.5) for time series, Two-Column 5:5 (§IX.2) for chart + commentary, or Comparison Table (§IX.6) for matrix data.
> 3. If the source has **3–4 distinct sections** that read as parallel ideas (not a sequence), prefer Three-Column Cards (§IX.4) over Card Grid 2×2 (§IX.7); the wider cards carry more body text.
> 4. If the body is a single long passage or quote with no parallel structure, Single Column (§IX.1) is the right choice — do not artificially split it into two columns.
> 5. All modes inherit Lenovo's light/dark tokens (§III). When rendering the dark variant, swap `bg` ↔ `text` (and `border` ↔ `muted-text`) at the card level; keep `primary` red and `accent` lavender untouched.

## X. Chapter Workflow

The chapter count and per-chapter content come from the Strategist's `design_spec.md §IX` outline — a user-confirmed output of the Eight Confirmations. This template ships **one** chapter SVG (`02_chapter.svg`); the Executor re-emits that same file once per chapter declared in the outline (option **a** — reuse, N duplicate emissions). Per-chapter variants (`02_chapter_01.svg`, `02_chapter_02.svg`, …) are not used; Lenovo is in `standard` replication mode where [`references/template-designer.md`](../../references/template-designer.md) §1 defines one chapter archetype. Role reference: [`references/strategist.md`](../../references/strategist.md) §6.2 step 4 (`page_layouts` in `spec_lock.md`); [`references/executor-base.md`](../../references/executor-base.md) §1 + §2.1 (per-page template resolution). Content comes from the Strategist's `§IX` chapter entries. Placeholder contract: each chapter page consumes one `{{CHAPTER_TITLE}}` and one `{{CHAPTER_DESC}}` (canonical per `template-designer.md` §4). Edge cases: if the user confirms N=0 chapters, the chapter page is omitted; N=1 yields exactly one chapter page; N≥2 yields N chapter pages in outline order.

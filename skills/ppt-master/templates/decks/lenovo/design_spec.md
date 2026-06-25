---
deck_id: lenovo
kind: deck
summary: Lenovo corporate deck — branded cover (replaceable title), TOC, chapter divider, content (open frame), and thanks page, light & dark themes
canvas_format: ppt169
page_count: 9
page_types: [cover, cover_dark, toc, toc_dark, chapter, content, content_dark, ending, ending_dark]
primary_color: "#E1251B"
placeholders: [TITLE, SUBTITLE, DECK_TITLE, PAGE_TITLE, KEY_MESSAGE, CONTENT_AREA, PAGE_NUM, TOTAL_PAGES, CHAPTER_TITLE, CHAPTER_DESC, TOC_ITEM_1_TITLE, TOC_ITEM_1_DESC, TOC_ITEM_2_TITLE, TOC_ITEM_2_DESC, TOC_ITEM_3_TITLE, TOC_ITEM_3_DESC, TOC_ITEM_4_TITLE, TOC_ITEM_4_DESC, TOC_ITEM_5_TITLE, TOC_ITEM_5_DESC, TOC_ITEM_6_TITLE, TOC_ITEM_6_DESC]
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

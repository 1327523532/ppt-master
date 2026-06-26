---
deck_id: Lenovo-Light
kind: deck
template_role: replica
theme: light
summary: Lenovo-branded enterprise decks, product launches (ThinkPad / IdeaPad / ThinkSystem), and partner-facing materials derived from the Lenovo reference template.
canvas_format: ppt169
page_count: 5
primary_color: "#E1251B"
placeholders:
  01_cover: [TITLE_LINE_1, TITLE_LINE_2, TITLE_LINE_3, SUBTITLE, PAGE_NUM]
  02_toc: [TOC_TITLE, ITEM_1_TITLE, ITEM_1_DESC, ITEM_2_TITLE, ITEM_2_DESC, ITEM_3_TITLE, ITEM_3_DESC, ITEM_4_TITLE, ITEM_4_DESC, LAYOUT_NAME, PAGE_NUM]
  03_chapter: [CHAPTER_NUM, CHAPTER_TITLE, CHAPTER_DESC, PAGE_NUM]
  04_content: [PAGE_TITLE, CARD_1_TITLE, CARD_1_DESC, CARD_1_BULLET_1, CARD_1_BULLET_2, CARD_1_BULLET_3, CARD_2_TITLE, CARD_2_DESC, CARD_2_BULLET_1, CARD_2_BULLET_2, CARD_2_BULLET_3, CARD_3_TITLE, CARD_3_DESC, CARD_3_BULLET_1, CARD_3_BULLET_2, CARD_3_BULLET_3, LAYOUT_NAME, PAGE_NUM]
  05_ending: [PAGE_NUM]
---

## Selection Guidance

**Use this deck when** the user supplies an explicit path to `templates/decks/Lenovo-Light/` OR requests a Lenovo-branded deck on a **light surface** (white / off-white background). Trigger phrasings include:

- `联想浅色模板` / `联想亮色版` / `联想白色主题`
- `Lenovo light theme` / `Lenovo light deck` / `Lenovo white background`
- `用 templates/decks/Lenovo-Light/`

If the user asks for a **dark** Lenovo deck (keynote / evening launch / dark-room / `联想深色模板` / `Lenovo dark theme`), route instead to [`../Lenovo-Dark/design_spec.md`](../Lenovo-Dark/design_spec.md). Both decks share the same outline (cover / TOC / content / chapter / ending) and brand identity (colors, typography, logo); only the surface treatment differs.

---

# Lenovo - Design Specification

> Replica derived from `ref/Lenovo-template_light.pptx` (59-slide source, 1 master / 29 layouts, 5 distinct page types). Page count is the canonical 5-page lifecycle (cover / toc / chapter / content / ending) — replicas cluster, they do not 1:1 mirror the source slide count.

## I. Template Overview

| Property | Description |
| --- | --- |
| **Template Name** | Lenovo |
| **Display Name** | Lenovo Replica Deck |
| **Use Cases** | Lenovo global enterprise decks, product launches (ThinkPad / IdeaPad / ThinkSystem), internal communications, partner-facing materials |
| **Design Tone** | Tech-corporate, restrained, brand-led, "Smarter technology for all" |
| **Theme Mode** | Hybrid (light cover / TOC / content pages with plum title typography + dark chapter divider + full-bleed gradient thanks page) |

Reference slides audited for visual fidelity: `ref/Lenovo-template_light.pptx` slide_02 (cover), slide_04 / slide_03 (content / chapter), slide_59 (thanks / ending). The deck reproduces the source's recurring footer pattern (red Lenovo mark + copyright + page number) and cover signature (rotated red Lenovo logo on the right edge).

## II. Canvas Specification

| Property | Value |
| --- | --- |
| **Format** | Standard 16:9 |
| **Dimensions** | 1280 x 720 px |
| **viewBox** | `0 0 1280 720` |
| **Safe Margins** | 80px left/right, 56px top, 56px bottom |
| **Primary Content Area** | x: 80-1160, y: 140-620 |

Slide-size provenance: `ref/Lenovo-template_light.pptx` `slideSize` → 1280×720 (ppt169). All page SVGs in this deck must declare `viewBox="0 0 1280 720"` and respect the 80/56/56/56 safe margins so the executor can lay out content without colliding with brand zones.

## III. Color Scheme

| Role | Color Value | Provenance | Usage |
| --- | --- | --- | --- |
| **Lenovo Primary** | `#E1251B` | fact (ref PPT theme `accent1`) | Logo block, top brand strip, narrow side brand bars, key callouts |
| **Lenovo Secondary** | `#871C23` | fact (ref PPT theme `accent2`) | Dark-page overlay, structural depth on chapter / ending |
| **Accent (warm)** | `#F26A52` | fact (ref PPT theme `dk2`) | Coral highlights, fine dividers on cover, content accents |
| **Accent (alert)** | `#4D144A` | fact (ref PPT theme `accent4`) | Deep plum for risk / high-contrast moments, dark-page support |
| **Text** | `#000000` | fact (ref PPT theme `dk1`) | Body text on light background |
| **Text (reverse)** | `#FFFFFF` | fact (ref PPT theme `lt1`) | Text on dark / brand-color surfaces |
| **White** | `#FFFFFF` | fact (ref PPT theme `lt1`) | Light page background |
| **Soft Neutral** | `#F7F5F8` | approx | Subtle light background depth on cover / content |

The first four rows are the official Lenovo brand surface extracted directly from the ref PPT theme XML. The text / bg pair follows the theme's `dk1` / `lt1` convention. The warm / alert accent pair (coral + deep plum) gives Strategist room for content-type differentiation (warm = callouts, alert = high contrast) without leaving the brand's restrained palette.

## IV. Typography

| Role | Family | Weight |
| --- | --- | --- |
| title | `Arial, "Microsoft YaHei", sans-serif` | 600–700 |
| body | `Arial, "Microsoft YaHei", sans-serif` | 400 |

> Ref PPT theme exposes `Arial` for both `majorLatin` (title) and `minorLatin` (body). Lenovo's public brand uses custom corporate typefaces that are not embedded in the ref PPT, so `Arial` is treated as the de-facto brand family with `Microsoft YaHei` as the CJK fallback. No PPTX font embedding is required because Arial is universally available. If a richer Lenovo brand face becomes available later, prepend it to the chain.

## V. Logo

| File | Form | Usage |
|---|---|---|
| `../brands/lenovo/lenovo_mark.svg` | Vector-extracted red rectangle (81.6×27.22) + 6 white "Lenovo" letterforms drawn as paths (extracted verbatim from `ref/Lenovo-template_light.pptx` slide_01/03/04 footer logo, theme accent1 `#E1251B`) | Recurring footer element on every page; rotated-and-scaled cover signature on the right edge; giant plum-toned "thanks" wordmark on the ending |

- The path data is the **official Lenovo wordmark** as embedded in the ref PPT — no hand-drawn approximation. Verified by visual rendering: 6 letterforms (L-e-n-o-v-o) cleanly aligned on the red rectangle.
- Clearspace: leave at least 0.5× mark height on all sides; never overlap text or photographic backgrounds.
- Mark color is fixed at `#E1251B`; the white letterforms inside the mark are non-recolorable.
- The same letterform paths are reused at larger scales on `01_cover.svg` (rotated -90°, scaled ~4×, on the right edge) and `05_ending.svg` (scaled ~6×, recolored to plum `#4D144A`, centered-left).

A separate wordmark or lockup SVG is intentionally not fabricated — the ref PPT does not expose a clean asset for one. If a future import yields a mark+wordmark lockup, add it as `../brands/lenovo/lenovo_lockup.svg` and update this table.

## VI. Page Structure

### Design Intent

1. Reproduce the ref PPT's recurring footer pattern (red Lenovo mark + copyright + page number) on every page — this is the signature element that ties the deck together.
2. Use PLUM `#4D144A` as the title color across cover / TOC / content (matches ref slide_02 cover), and as the giant "thanks" wordmark color on the ending.
3. Use the ref's actual letterform paths (extracted from slide_01) for the Lenovo mark — not a hand-drawn approximation.
4. The cover signature is a **rotated red Lenovo logo on the right edge** (per ref slide_02 layout-shape-14).
5. The ending signature is a **full-bleed gradient background with a giant plum "Lenovo" wordmark** (per ref slide_59) — this page is intentionally reusable as the final slide of any Lenovo deck.
6. Chapter dividers use dark plum full-bleed for visual break; the ref PPT's chapter candidates are visually similar to content pages, so the dark full-bleed is a deliberate visual emphasis on the chapter transition.

### Layout Grid (light pages: cover / toc / content)

| Zone | Bounds |
|---|---|
| Top zone (no strip) | y: 0–8 |
| Title region | x: 80–1100, y: 100–280 (plum, Arial bold 58–106pt) |
| Primary content | x: 80–1160, y: 200–620 |
| Footer mark | x: 80, y: 666.5 (~80×27 red Lenovo mark) |
| Copyright | x: 170, y: 685, 13.33pt black |
| Page number | x: 1248, y: 688, 13.33pt black, text-anchor middle |
| Layout-name (optional) | x: 640, y: 736, 10.67pt `#E6E6E6` light grey, text-anchor middle (per ref DNA) |

### Decorative DNA

- **Recurring footer**: small red Lenovo mark (~80×27) bottom-left, copyright text, page number bottom-right, optional layout-name centered at the very bottom in light grey.
- **Pull-quote marks** (content pages, ref slide_04): large plum " "  Freeforms in the upper-left of content pages; decorative only, not anchored to specific text.
- **Plum title typography**: title color `#4D144A` on light cover / TOC / content; white on the dark chapter divider.
- **Arial typography**: a single typeface family for both title and body, with weight contrast 600–700 — no decorative display fonts.
- **Plum / coral accents**: coral `#F26A52` is reserved for accent dividers and chapter accent bars; deep plum `#4D144A` carries the title weight.
- **Content page layout** (ref slide_50): title at top-left with thin plum divider; 3 cards in a row, each 340×~190 (stripe 44 + body ~150); alternating purple/plum/deep-plum stripes for visual rhythm; card body holds description + bulleted list. This is the canonical 'List multi column' layout from the official Lenovo deck.
- **Right-edge rotated logo** (cover only): the same Lenovo wordmark paths, rotated -90° and scaled 4×, on the right edge.
- **Gradient ending**: a coral → plum → lavender gradient background (`#F5A598 → #D2ADC9 → #E6BDC1 → #A7B6D3`) with a giant plum "Lenovo" wordmark dominating the lower-left; small red logo top-right; tiny "thanks" label in light grey.

## VII. Page Types

| File | Role | Description |
|---|---|---|
| `01_cover.svg` | cover | White background; plum title (Arial bold 106.67pt, 3 lines); plum subtitle (34.67pt); bottom-left footer mark + copyright; bottom-right page number; rotated red Lenovo logo on the right edge |
| `02_toc.svg` | toc | White background; plum section label "AGENDA"; plum title 58.67pt; thin plum divider; 2×2 agenda items with plum numbers; ref footer pattern; layout-name "Agenda" centered at the very bottom |
| `03_chapter.svg` | chapter | Dark plum `#4D144A` full-bleed; large translucent white chapter numeral; white title 46pt; coral accent vertical bar; decorative circles; ref footer pattern (white copyright for dark bg) |
| `04_content.svg` | content | White background; black title Arial bold 42.67pt at top-left with thin plum divider; 3 cards in a row, each with colored top stripe (purple `#6D1C69`, dark plum `#4C1249`, deep plum `#4D144A`) and white centered title; card body with description text + 3-item bullet list; ref footer pattern. Layout DNA sourced from `ref/Lenovo-template.pptx` slide_50 ("List multi column"). |
| `05_ending.svg` | ending | Full-bleed gradient (`#F5A598` coral → `#A7B6D3` lavender, top-left to bottom-right); "Smarter technology for all" tagline in plum, top-right, right-aligned; vertical red "Lenovo" wordmark on the right edge; giant sans-serif "thanks." in plum `#4D144A`, lower-left; ref footer pattern |

All 5 SVGs hand-authored, validated by `svg_quality_checker.py --format ppt169`, and committed. Filenames follow the canonical replica lifecycle. The ending page is designed to be reusable verbatim as the final slide of any Lenovo deck (per the design directive).

## VIII. SVG Page Roster

| File | Role | One-line purpose |
| --- | --- | --- |
| `01_cover.svg` | cover | Title slide; brand / project name + presenter + date |
| `02_toc.svg` | toc | Agenda / table of contents listing major sections |
| `03_chapter.svg` | chapter | Chapter divider (large numeral + chapter title) |
| `04_content.svg` | content | Main content page; body of the deck |
| `05_ending.svg` | ending | Closing / thank-you page |

All 5 SVGs hand-authored, validated by `svg_quality_checker.py --format ppt169`, and committed. Filenames follow the canonical replica lifecycle.

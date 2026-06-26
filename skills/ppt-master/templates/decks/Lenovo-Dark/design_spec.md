---
deck_id: Lenovo-Dark
kind: deck
template_role: replica
theme: dark
summary: Dark variant of the Lenovo replica deck — for keynote / evening-launch / dark-room presentations. Same outline as lenovo-light (cover / TOC / content / chapter / ending); surface tokens swapped via brand spec §VII.
canvas_format: ppt169
page_count: 5
primary_color: "#E1251B"
placeholders:
  01_cover: [TITLE_LINE_1, TITLE_LINE_2, TITLE_LINE_3, SUBTITLE, PAGE_NUM]
  02_toc: [TOC_TITLE, ITEM_1_TITLE, ITEM_1_DESC, ITEM_2_TITLE, ITEM_2_DESC, ITEM_3_TITLE, ITEM_3_DESC, ITEM_4_TITLE, ITEM_4_DESC, LAYOUT_NAME, PAGE_NUM]
  03_chapter: [CHAPTER_NUM, CHAPTER_TITLE, CHAPTER_DESC, PAGE_NUM]
  04_content: [PAGE_TITLE, CARD_1_TITLE, CARD_1_DESC, CARD_1_BULLET_1, CARD_1_BULLET_2, CARD_1_BULLET_3, CARD_2_TITLE, CARD_2_DESC, CARD_2_BULLET_1, CARD_2_BULLET_2, CARD_2_BULLET_3, CARD_3_TITLE, CARD_3_DESC, CARD_3_BULLET_1, CARD_3_BULLET_2, CARD_3_BULLET_3, LAYOUT_NAME, PAGE_NUM]
  05_ending: [PAGE_NUM]
fixed_pages:
  - role: ending
    file: 05_ending.svg
    count_toward_page_count: false
    reason: "Lenovo thanks page — appended verbatim after the user-authored deck, original file untouched and no slots filled in"
---

## Selection Guidance

**Use this deck when** the user supplies an explicit path to `templates/decks/Lenovo-Dark/` OR requests a Lenovo-branded deck on a **dark surface** (`#1E0113` cover / TOC / content / chapter; radial-gradient dark ending). Trigger phrasings include:

- `联想深色模板` / `联想暗色版` / `联想夜间版`
- `Lenovo dark theme` / `Lenovo dark deck` / `Lenovo keynote` / `Lenovo evening launch`
- `用 templates/decks/Lenovo-Dark/`

If the user asks for a **light** Lenovo deck (default enterprise / white background / `联想浅色模板` / `Lenovo light theme`), route instead to [`../Lenovo-Light/design_spec.md`](../Lenovo-Light/design_spec.md). Both decks share the same outline (cover / TOC / content / chapter / ending) and brand identity (colors, typography, logo); only the surface treatment differs.

---

# Lenovo-Dark - Design Specification

> Dark variant replica derived from `ref/Lenovo-template.pptx` slide_01/13/141 (dark page family) and slide_50 (3-card content layout, color-adjusted for dark surface). Surface tokens per brand spec §VII.

## I. Template Overview

| Property | Description |
| --- | --- |
| **Template Name** | Lenovo-Dark |
| **Display Name** | Lenovo Replica Deck (Dark Theme) |
| **Use Cases** | Cinema-style keynotes, internal review boards, evening launches, dark-room presentations |
| **Design Tone** | Same as light theme (tech-corporate, restrained, brand-led); surface treatment swapped to dark |
| **Theme Mode** | Dark (full-bleed `#1E0113` cover / TOC / content / chapter; radial-gradient dark ending) |

Reference slides audited: slide_01 (dark cover), slide_13 (dark content DNA), slide_141 (dark gradient ending). Same outline structure as the light deck.

## II. Canvas Specification

| Property | Value |
| --- | --- |
| **Format** | Standard 16:9 |
| **Dimensions** | 1280 x 720 px |
| **viewBox** | `0 0 1280 720` |
| **Safe Margins** | 80px left/right, 56px top, 56px bottom (same as light) |
| **Primary Content Area** | x: 80-1160, y: 140-620 |

## III. Color Scheme

| Role | Color Value | Provenance | Usage |
| --- | --- | --- | --- |
| **Page bg (dark)** | `#1E0113` | fact (ref slide_01/13/141) | Cover / TOC / content / chapter backgrounds |
| **Text (white)** | `#FFFFFF` | fact | Title, body, footer text on dark surfaces |
| **Text muted (white)** | `#FFFFFF` opacity 0.62 | approx | Subtitles, descriptions |
| **Brand red** | `#E1251B` | fact (theme accent1) | Mark + accent dividers — invariant per brand |
| **Plum accent** | `#4D144A` | fact (theme accent4) | Section labels, agenda numbers, title dividers |
| **Plum darker** | `#5C1559` | approx | Card 1 stripe (dark-theme adjusted from `#6D1C69`) |
| **Plum dark** | `#3F0E3F` | approx | Card 2 stripe (dark-theme adjusted from `#4C1249`) |
| **Plum deepest** | `#2A0825` | approx | Card 3 stripe (dark-theme adjusted from `#4D144A`) |
| **Coral accent** | `#64131E` | fact (ref slide_141 gradient) | Chapter accent bar (dark variant) |
| **Soft dim** | `#4E444E` | fact (theme lt2) | Tiny layout-name labels at bottom |

## IV. Typography

| Role | Family | Weight |
|---|---|---|
| title | `Arial, "Microsoft YaHei", sans-serif` | 600–700 |
| body | `Arial, "Microsoft YaHei", sans-serif` | 400 |

Same as light theme — typography is invariant across themes per brand spec §VII.

## V. Logo

| File | Form | Usage |
|---|---|---|
| `../brands/lenovo/lenovo_mark.svg` | Vector-extracted red rectangle (81.6×27.22) + 6 white "Lenovo" letterforms as paths (theme accent1 `#E1251B`) | Recurring footer element on every page; rotated-and-scaled cover signature; vertical right-edge wordmark on the ending |

Mark color is invariant: red `#E1251B` shows on both light and dark surfaces. The white letterforms inside the mark are non-recolorable.

## VI. Page Structure

### Design Intent

1. Invert the light-theme surface to dark; keep the recurring footer pattern (red mark + copyright + page number) and the brand identity otherwise identical.
2. The mark color is invariant; the surface and text tokens are the only things that change.
3. The dark cover signature is a rotated red Lenovo logo on the right edge (per ref slide_01) — same as the light cover.
4. The dark ending signature is a radial gradient on `#1E0113` (per ref slide_141) with a giant sans-serif "thanks." wordmark in WHITE.
5. Content pages use the same slide_50-sourced 3-card layout as the light deck, with card stripe colors adjusted for dark-theme harmony.

### Layout Grid (dark pages: cover / TOC / content / chapter)

| Zone | Bounds |
|---|---|
| Top zone (no strip) | y: 0–8 |
| Title region | x: 80–1100, y: 100–280 (WHITE, Arial bold 42.67pt on content; 106.67pt on cover) |
| Primary content | x: 80–1160, y: 200–620 |
| Footer mark | x: 80, y: 666.5 (~80×27 red Lenovo mark) |
| Copyright | x: 170, y: 685, 13.33pt WHITE |
| Page number | x: 1248, y: 688, 13.33pt WHITE, text-anchor middle |
| Layout-name (optional) | x: 640, y: 736, 10.67pt `#4E444E` dim grey, text-anchor middle |

### Decorative DNA

- **Recurring footer**: small red Lenovo mark (~80×27) bottom-left, WHITE copyright text, WHITE page number bottom-right.
- **Title typography**: WHITE on dark surfaces (matches ref slide_13); plum dividers under titles.
- **Arial typography**: same as light — a single typeface family for both title and body, with weight contrast 600–700.
- **Plum / coral accents**: plum `#4D144A` for dividers, numbers, and section labels; coral `#64131E` is reserved for chapter accent bars.
- **Right-edge rotated logo** (cover only): the same Lenovo wordmark paths, rotated -90° and scaled 4×, on the right edge — same as light.
- **Gradient ending**: solid `#1E0113` base + radial gradient overlay (`#391262 → #64131E → #831B22 → #4D144A`, fill-opacity 0.78) with a giant WHITE "thanks." wordmark dominating the lower-left; small red logo top-right; "Smarter technology for all" tagline in WHITE at top-right.

## VII. Page Types

| File | Role | Description |
|---|---|---|
| `01_cover.svg` | cover | Dark background `#1E0113`; WHITE title Arial bold 106.67pt (3 lines); WHITE subtitle 34.67pt; bottom-left footer mark + WHITE copyright; bottom-right WHITE page number; rotated red Lenovo logo on the right edge |
| `02_toc.svg` | toc | Dark background; plum section label "AGENDA"; WHITE title 58.67pt; thin plum divider; 2×2 agenda items with plum numbers; ref footer pattern in WHITE; layout-name "Agenda" centered at the very bottom in dim grey |
| `03_chapter.svg` | chapter | Full-bleed dark `#1E0113`; large translucent white chapter numeral; WHITE title 46pt; coral accent vertical bar; decorative circles; ref footer pattern (WHITE copyright for dark bg) |
| `04_content.svg` | content | Dark background; WHITE title Arial bold 42.67pt at top-left with thin plum divider; 3 cards in a row with adjusted dark-theme stripe colors (`#5C1559`, `#3F0E3F`, `#2A0825`) and WHITE centered title; card body with WHITE description text + 3-item bullet list; ref footer pattern in WHITE |
| `05_ending.svg` | ending | Dark base `#1E0113` + radial gradient overlay (`#391262 → #64131E → #831B22 → #4D144A`); "Smarter technology for all" tagline in WHITE, top-right; vertical red "Lenovo" wordmark on the right edge; giant sans-serif "thanks." in WHITE, lower-left; ref footer pattern in WHITE |

All 5 SVGs hand-authored, validated by `svg_quality_checker.py --format ppt169`, and committed.

### Fixed pages (do not count toward `page_count`)

`05_ending.svg` is a **fixed page** — it is appended to every Lenovo deck as-is, with the original SVG untouched and none of the `placeholders` filled in by the executor. The user-confirmed `page_count` (5) covers only the content body; the ending adds 1 page on top, for a total output of 6 slides. Listed in the frontmatter `fixed_pages` block for executor discovery. Cover, TOC, chapter, and content are the four user-authored page types and they fill the entire `page_count` budget.

## VIII. SVG Page Roster

| File | Role | One-line purpose |
| --- | --- | --- |
| `01_cover.svg` | cover | Title slide; brand / project name + presenter + date |
| `02_toc.svg` | toc | Agenda / table of contents listing major sections |
| `03_chapter.svg` | chapter | Chapter divider (large numeral + chapter title) |
| `04_content.svg` | content | Main content page; body of the deck |
| `05_ending.svg` | ending | Closing / thank-you page |

Filenames follow the canonical replica lifecycle. The deck is reusable as a starting point for any Lenovo dark-mode presentation.

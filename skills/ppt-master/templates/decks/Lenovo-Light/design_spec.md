---
deck_id: Lenovo-Light
kind: deck
template_role: replica
theme: light
summary: Lenovo-branded enterprise decks, product launches (ThinkPad / IdeaPad / ThinkSystem), and partner-facing materials derived from the Lenovo reference template (lenovo-template-02.pptx).
canvas_format: ppt169
page_count: 12
primary_color: "#E1251B"
placeholders:
  01_cover: [TITLE_LINE_1, TITLE_LINE_2, TITLE_LINE_3, SUBTITLE, PAGE_NUM]
  02_toc: [TOC_TITLE, ITEM_1_TITLE, ITEM_1_DESC, ITEM_2_TITLE, ITEM_2_DESC, ITEM_3_TITLE, ITEM_3_DESC, ITEM_4_TITLE, ITEM_4_DESC, PAGE_NUM]
  03_chapter: [CHAPTER_NUM, CHAPTER_TITLE, CHAPTER_DESC, PAGE_NUM]
  04a_content_one_col: [PAGE_TITLE, PARAGRAPH_LINE_1, PARAGRAPH_LINE_2, BULLET_1, BULLET_2, BULLET_3, BULLET_4, PAGE_NUM]
  04b_content_two_col: [PAGE_TITLE, PAGE_SUBTITLE, LEFT_CARD_1_TITLE, LEFT_CARD_1_DESC, LEFT_CARD_1_BULLET_1, LEFT_CARD_1_BULLET_2, LEFT_CARD_2_TITLE, LEFT_CARD_2_DESC, LEFT_CARD_2_BULLET_1, LEFT_CARD_2_BULLET_2, LEFT_CARD_3_TITLE, LEFT_CARD_3_DESC, LEFT_CARD_3_BULLET_1, LEFT_CARD_3_BULLET_2, RIGHT_CARD_TITLE, RIGHT_CARD_DESC, RIGHT_CARD_BULLET_1, RIGHT_CARD_BULLET_2, RIGHT_CARD_BULLET_3, PAGE_NUM]
  04c_content_three_col: [PAGE_TITLE, COL_1_TITLE, COL_1_DESC, COL_1_BULLET_1, COL_1_BULLET_2, COL_1_BULLET_3, COL_2_TITLE, COL_2_DESC, COL_2_BULLET_1, COL_2_BULLET_2, COL_2_BULLET_3, COL_3_TITLE, COL_3_DESC, COL_3_BULLET_1, COL_3_BULLET_2, COL_3_BULLET_3, COL_4_TITLE, COL_4_DESC, COL_4_BULLET_1, COL_4_BULLET_2, COL_4_BULLET_3, COL_5_TITLE, COL_5_DESC, COL_5_BULLET_1, COL_5_BULLET_2, COL_5_BULLET_3, PAGE_NUM]
  04d_content_three_deep: [COL_1_TITLE_LINE_1, COL_1_TITLE_LINE_2, COL_1_DESC, COL_2_TITLE_LINE_1, COL_2_TITLE_LINE_2, COL_2_DESC, COL_3_TITLE_LINE_1, COL_3_TITLE_LINE_2, COL_3_DESC, PAGE_NUM]
  05_section_title: [PAGE_TITLE, PAGE_SUBTITLE, PAGE_NUM]
  06_image_text: [PAGE_TITLE, BULLET_1, BULLET_2, BULLET_3, SUPPORTING_TEXT, IMAGE, PAGE_NUM]
  07_photo_statement: [IMAGE, STATEMENT_LINE_1, STATEMENT_LINE_2, STATEMENT_LINE_3, PAGE_NUM]
  08_big_idea: [BIG_IDEA_LINE_1, BIG_IDEA_LINE_2, SUPPORTING_TEXT, PAGE_NUM]
  09_blank: [PAGE_NUM]
  10_ending: [PAGE_NUM]
fixed_pages:
  - role: ending
    file: 10_ending.svg
    count_toward_page_count: false
    reason: "Lenovo thanks page — appended verbatim after the user-authored deck, original file untouched and no slots filled in"
---

## Selection Guidance

**Use this deck when** the user supplies an explicit path to `templates/decks/Lenovo-Light/` OR requests a Lenovo-branded deck on a **light surface** (white / off-white background). Trigger phrasings include:

- `联想浅色模板` / `联想亮色版` / `联想白色主题`
- `Lenovo light theme` / `Lenovo light deck` / `Lenovo white background`
- `用 templates/decks/Lenovo-Light/`

If the user asks for a **dark** Lenovo deck (keynote / evening launch / dark-room / `联想深色模板` / `Lenovo dark theme`), route instead to [`../Lenovo-Dark/design_spec.md`](../Lenovo-Dark/design_spec.md). Both decks share the same outline (cover / TOC / 8 content variants / chapter / ending) and brand identity (colors, typography, logo); only the surface treatment differs.

---

# Lenovo Light — Design Specification

> Replica derived from `lenovo-res/lenovo-template-02.pptx` (142-slide source, 1 master / 29 layouts). The 12-page user-authored outline covers cover / TOC / chapter / 8 content variants; the closing `10_ending.svg` is a fixed page appended verbatim.

## I. Template Overview

| Property | Description |
| --- | --- |
| **Template Name** | Lenovo Light |
| **Display Name** | Lenovo Replica Deck (Light) |
| **Use Cases** | Lenovo global enterprise decks, product launches (ThinkPad / IdeaPad / ThinkSystem), internal communications, partner-facing materials |
| **Design Tone** | Tech-corporate, restrained, brand-led, "Smarter technology for all" |
| **Theme Mode** | Light surface (white / pink-lavender gradient) with deep-plum ending |

Reference slides audited for visual fidelity: `lenovo-template-02.pptx` slide_01 (cover black), slide_05 (cover white — light variant), slide_09 (chapter "Section header"), slide_40 (goals & objectives, two-column), slide_48 (content title only), slide_50 (list multi column), slide_60 (3 column deep), slide_141 (closing — light), slide_142 (closing — black).

## II. Canvas Specification

| Property | Value |
| --- | --- |
| **Format** | Standard 16:9 |
| **Dimensions** | 1280 x 720 px |
| **viewBox** | `0 0 1280 720` |
| **Safe Margins** | 80px left/right, 56px top, 56px bottom |
| **Primary Content Area** | x: 80-1160, y: 100-640 |

Slide-size provenance: `lenovo-template-02.pptx` `slideSize` → 1280×720 (ppt169). All page SVGs in this deck must declare `viewBox="0 0 1280 720"` and respect the 80/56 safe margins so the executor can lay out content without colliding with the recurring footer mark.

## III. Color Scheme

| Role | HEX | Provenance | Usage |
| --- | --- | --- | --- |
| **Lenovo Red (brand primary)** | `#E1251B` | fact (ref PPT theme `accent1`) | Logo block, footer mark, right-edge vertical mark, callouts |
| **Lenovo Dark Red (brand secondary)** | `#871C23` | fact (ref PPT theme `accent2`) | Card backgrounds, structural depth on dark-page content |
| **Deep Plum (accent alert)** | `#4D144A` | fact (ref PPT theme `accent4`) | Title typography on light pages, "thanks." wordmark on ending, divider lines |
| **Coral (warm accent)** | `#F26A52` | fact (ref PPT theme `dk2`) | Stripe backgrounds, fine dividers, ending gradient stop |
| **Light Plum (accent 3)** | `#D9C1D8` | fact (ref PPT theme `accent3`) | Soft stripes in 04c, accent dividers |
| **Lavender (accent 5)** | `#C9D0F0` | fact (ref PPT theme `accent5`) | Soft stripes in 04c |
| **Deep Blue (accent 6)** | `#11184F` | fact (ref PPT theme `accent6`) | Lavender stripe text contrast |
| **Text** | `#000000` | fact (ref PPT theme `dk1`) | Body text and titles on light background |
| **Text (reverse)** | `#FFFFFF` | fact (ref PPT theme `lt1`) | Text on red / plum / dark surfaces |
| **Background** | `#FFFFFF` | fact (ref PPT theme `lt1`) | Default light page background |

For Dark theme overrides see `Lenovo-Dark/design_spec.md` §VII. Brand red, secondary red, font, and logo are **invariant** between themes.

## IV. Typography

| Role | Family | Weight |
| --- | --- | --- |
| title | `Arial, "Microsoft YaHei", sans-serif` | 700 |
| body | `Arial, "Microsoft YaHei", sans-serif` | 400 |
| accent label | `Arial, "Microsoft YaHei", sans-serif` | 600–700 |

> Ref PPT theme exposes `Arial` for both `majorLatin` (title) and `minorLatin` (body). Lenovo's public brand uses custom corporate typefaces that are not embedded in the ref PPT, so `Arial` is treated as the de-facto brand family with `Microsoft YaHei` as the CJK fallback.

## V. Logo

| File | Form | Usage |
|---|---|---|
| `../brands/lenovo/lenovo_mark.svg` | Vector-extracted red rectangle (81.6×27.22) + 6 white "Lenovo" letterforms drawn as paths (extracted verbatim from `lenovo-template-02.pptx` slide_01/03/04 footer logo, theme accent1 `#E1251B`) | Recurring footer element on every page; rotated-and-scaled right-edge signature on the cover, ending, and other key pages |

- The path data is the **official Lenovo wordmark** as embedded in the ref PPT — no hand-drawn approximation.
- Clearspace: leave at least 0.5× mark height on all sides; never overlap text or photographic backgrounds.
- Mark color is fixed at `#E1251B`; the white letterforms inside the mark are non-recolorable.
- The same letterform paths are reused at larger scales on `01_cover.svg` (rotated -90°, scaled ~3.93×, on the right edge) and `10_ending.svg` (rotated -90°, scaled ~3.93×, on the right edge above the "thanks." wordmark).

## VI. Page Structure

### Decorative DNA

- **Recurring footer**: small red Lenovo mark (~80×27) bottom-left, copyright text "2026 Lenovo Internal. All rights reserved.", page number bottom-right.
- **Plum title typography**: title color `#4D144A` on cover / TOC / content (white) variants; "thanks." on the ending.
- **Arial typography**: a single typeface family for both title and body, with weight contrast 700 / 400 — no decorative display fonts.
- **Right-edge rotated logo**: vertical red Lenovo wordmark on cover and ending, anchored to the right edge.
- **Light cover gradient**: pink (`#F5A598`) → lavender (`#D2ADC9`) → light blue (`#A7B6D3`) diagonal — matches P5 Title Slide_White.
- **Light ending gradient**: same pink → lavender → light blue — matches P141 Closing Slide.

### Layout Grid (light pages: cover / toc / content / ending)

| Zone | Bounds |
|---|---|
| Top zone (no strip) | y: 0–80 |
| Title region | x: 80–1100, y: 100–300 (plum or black Arial bold 32–80pt) |
| Primary content | x: 80–1200, y: 200–620 |
| Footer mark | x: 80, y: 666.5 (~80×27 red Lenovo mark) |
| Copyright | x: 170, y: 685, 13.33pt black |
| Page number | x: 1248, y: 688, 13.33pt black, text-anchor middle |

## VII. Page Types

| File | Role | Source layout | Description |
|---|---|---|---|
| `01_cover.svg` | cover | P5 Title Slide_White | Pink-lavender gradient bg; top-left "Smarter technology for all" tagline (plum); 3-line plum title; speaker/date subtitle; right-edge vertical red Lenovo mark; footer mark |
| `02_toc.svg` | toc | P9 Section Header_White + agenda | White bg; left-aligned "AGENDA" eyebrow (plum); black TOC title; 2×2 agenda grid with plum 2-digit numbers + black titles + gray descriptions; footer mark |
| `03_chapter.svg` | chapter | P9 Section Header_White | White bg; small plum chapter numeral (top-left, all-caps); big black 80pt section title; black subhead below; footer mark |
| `04a_content_one_col.svg` | content | P48 "Content Title" | White bg; black 42pt title; plum underline; 2-line paragraph; 4-bullet list; footer mark |
| `04b_content_two_col.svg` | content | P40 "Goals and objectives" | White bg; title + subtitle on top; 3 stacked colored cards on the left (purple / dark-red / deep-plum, each with circular icon + title + desc + 2 bullets); 1 tall gradient card on the right (purple → plum, with title + desc + 3 bullets) |
| `04c_content_three_col.svg` | content | P50 "List multi column" | White bg; title at top; 5 columns each with circular outline icon + colored short-title stripe (purple/pink/red/coral/lavender) + description + 3 bullets; footer mark |
| `04d_content_three_deep.svg` | content | P60 "3 column deep" | 3 full-height color columns (red `#B23A2A` / purple `#6D1C69` / deep blue `#21386A`); each with circular white-line icon + 2-line white title + description; white page number (no footer mark on full-bleed page) |
| `05_section_title.svg` | content | P40 "Title with Subtitle Only" | White bg; large 58pt black title centered-left; plum underline; 22pt gray subtitle below; footer mark |
| `06_image_text.svg` | content | P20 "Content with image layout" | White bg; left column with 32pt black title + 3 bullets + supporting text; right column large dashed-bordered image placeholder marked with `{{IMAGE}}`; footer mark |
| `07_photo_statement.svg` | content | P21 "Photo + Statement" | Full-bleed dashed-bordered image placeholder marked with `{{IMAGE}}`; semi-transparent white overlay on the lower-left; 3-line black bold statement; plum accent line; footer mark |
| `08_big_idea.svg` | content | (Big Idea layout) | White bg; centered 64pt plum 2-line headline; plum accent line; centered 18pt gray supporting text; footer mark |
| `09_blank.svg` | content | P23/P73 Blank Slide | White bg; only the recurring footer mark + page number. Full canvas free for content insertion. |
| `10_ending.svg` | ending | P141 Closing Slide | Pink-lavender gradient; top-right plum 3-line tagline "Smarter technology for all"; right-edge vertical red Lenovo mark; center-left giant 200pt plum "thanks."; footer mark |

All 12 user-authored SVGs + 1 fixed ending SVG, validated by `svg_quality_checker.py --template-mode --format ppt169`. Filenames follow the canonical replica lifecycle. The ending page is designed to be reusable verbatim as the final slide of any Lenovo deck (per the design directive).

### Fixed pages (do not count toward `page_count`)

`10_ending.svg` is a **fixed page** — it is appended to every Lenovo deck as-is, with the original SVG untouched and none of the `placeholders` filled in by the executor. The user-confirmed `page_count` (12) covers only the content body; the ending adds 1 page on top, for a total output of 13 slides. Listed in the frontmatter `fixed_pages` block for executor discovery.

## VIII. SVG Page Roster

| File | Role | One-line purpose |
|---|---|---|
| `01_cover.svg` | cover | Title slide; brand / project name + presenter + date |
| `02_toc.svg` | toc | Agenda / table of contents listing 4 major sections |
| `03_chapter.svg` | chapter | Chapter divider (large numeral + chapter title) |
| `04a_content_one_col.svg` | content | Single-column body content (title + paragraph + 4-bullet list) |
| `04b_content_two_col.svg` | content | Two-column body (3 stacked left cards + 1 tall right card) |
| `04c_content_three_col.svg` | content | Multi-column list (5 icon + stripe + description + bullets) |
| `04d_content_three_deep.svg` | content | Three full-height color columns with icon + title + desc |
| `05_section_title.svg` | content | Section pause / breathing slide (title + subtitle) |
| `06_image_text.svg` | content | Left text + right image placeholder |
| `07_photo_statement.svg` | content | Full-bleed image + lower-left statement |
| `08_big_idea.svg` | content | Centered big idea in plum + supporting subtitle |
| `09_blank.svg` | content | Blank canvas with only the recurring footer |
| `10_ending.svg` | ending | Closing / thank-you page (gradient + giant "thanks.") |

All SVGs hand-authored, validated by `svg_quality_checker.py --template-mode --format ppt169`, and committed.

---
deck_id: Lenovo-Dark
kind: deck
template_role: replica
theme: dark
summary: Dark variant of the Lenovo replica deck — for keynote / evening-launch / dark-room presentations. Same 12-page outline as lenovo-light (cover / TOC / 8 content variants / chapter / ending); surface tokens swapped via brand spec §VII.
canvas_format: ppt169
page_count: 12
primary_color: "#E1251B"
contract:
  bound_by: "SKILL.md Free Design Is Opt-In hard rule"
  default_invocation: "python scripts/project_manager.py init <name> --format ppt169 --template lenovo-dark"
  applies_via_default_template: lenovo-dark
  required_spec_lock_section: page_layouts
  required_page_layouts_entries:
    - P01: 01_cover
    - P02: 02_toc
    - P03: 03_chapter
    - P04: 04a_content_one_col
    - P05: 04b_content_two_col
    - P06: 04c_content_three_col
    - P07: 04d_content_three_deep
    - P08: 05_section_title
    - P09: 06_image_text
    - P10: 07_photo_statement
    - P11: 08_big_idea
    - P12: 09_blank
  free_design_opt_in: "Pass --template free-design to skip template inheritance. Writes .free_design marker; spec_lock.page_layouts may remain empty."
  verification_script: "python scripts/validate_project.py <project_path>"
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

**Use this deck when** the user supplies an explicit path to `templates/decks/Lenovo-Dark/` OR requests a Lenovo-branded deck on a **dark surface** (full dark plum `#1E0113` cover / TOC / content / chapter; deep-plum → deep-red gradient ending). Trigger phrasings include:

- `联想深色模板` / `联想深色版` / `联想黑色主题`
- `Lenovo dark theme` / `Lenovo dark deck` / `Lenovo black background` / `keynote Lenovo`
- `用 templates/decks/Lenovo-Dark/`

If the user asks for a **light** Lenovo deck (default enterprise / white background), route instead to [`../Lenovo-Light/design_spec.md`](../Lenovo-Light/design_spec.md). Both decks share the same 12-page outline and brand identity (colors, typography, logo); only the surface treatment differs.

---

# Lenovo Dark — Design Specification

> Replica derived from `lenovo-res/lenovo-template-02.pptx` (142-slide source, 1 master / 29 layouts). The 12-page user-authored outline covers cover / TOC / chapter / 8 content variants; the closing `10_ending.svg` is a fixed page appended verbatim. This is the dark counterpart to the Lenovo-Light deck.

## I. Template Overview

| Property | Description |
| --- | --- |
| **Template Name** | Lenovo Dark |
| **Display Name** | Lenovo Replica Deck (Dark) |
| **Use Cases** | Keynote launches (ThinkPad / IdeaPad / ThinkSystem), evening events, dark-room presentations, internal executive reviews |
| **Design Tone** | Tech-corporate, restrained, brand-led, "Smarter technology for all" |
| **Theme Mode** | Dark surface (`#1E0113` deep plum) with deep-plum → deep-red ending gradient |

Reference slides audited for visual fidelity: `lenovo-template-02.pptx` slide_01 (cover black), slide_141 (closing — light variant of source), slide_142 (closing — black, the dark source for `10_ending.svg`).

## II. Canvas Specification

| Property | Value |
| --- | --- |
| **Format** | Standard 16:9 |
| **Dimensions** | 1280 x 720 px |
| **viewBox** | `0 0 1280 720` |
| **Safe Margins** | 80px left/right, 56px top, 56px bottom |
| **Primary Content Area** | x: 80-1160, y: 100-640 |

Slide-size provenance: `lenovo-template-02.pptx` `slideSize` → 1280×720 (ppt169).

## III. Color Scheme

| Role | HEX | Provenance | Usage |
| --- | --- | --- | --- |
| **Lenovo Red (brand primary, invariant)** | `#E1251B` | fact (ref PPT theme `accent1`) | Logo block, footer mark, right-edge vertical mark, callouts |
| **Lenovo Dark Red (brand secondary, invariant)** | `#871C23` | fact (ref PPT theme `accent2`) | Card backgrounds, structural depth |
| **Surface bg (Dark)** | `#1E0113` | fact (per brand spec §VII) | Page background on cover / TOC / content / chapter |
| **Text primary (Dark)** | `#FFFFFF` | fact (per brand spec §VII) | Body text and titles on dark surface |
| **Deep Plum (accent cool, Dark)** | `#391262` | fact (per brand spec §VII) | Accent dividers, plum underlines |
| **Coral (accent warm, Dark)** | `#64131E` | fact (per brand spec §VII) | Muted dark red highlights, ending gradient stop |
| **Reverse text (on red mark)** | `#FFFFFF` | fact (invariant) | White letterforms inside the red mark |
| **Bricks (04d column colors, invariant)** | `#B23A2A` / `#6D1C69` / `#21386A` | fact (per source P60) | 04d column backgrounds |
| **Card colors (04b, 04c, invariant)** | `#6D1C69` / `#871C23` / `#4D144A` / `#D9C1D8` / `#F26A52` / `#C9D0F0` | fact (per source P40, P50) | Card / stripe backgrounds |

For Light theme overrides see `Lenovo-Light/design_spec.md` §III. Brand red, secondary red, font, and logo are **invariant** between themes.

## IV. Typography

| Role | Family | Weight |
| --- | --- | --- |
| title | `Arial, "Microsoft YaHei", sans-serif` | 700 |
| body | `Arial, "Microsoft YaHei", sans-serif` | 400 |
| accent label | `Arial, "Microsoft YaHei", sans-serif` | 600–700 |

Identical to the Light theme. The brand typeface is invariant between themes.

## V. Logo

Same as `Lenovo-Light` — see `../Lenovo-Light/design_spec.md` §V. The red mark + 6 white letterform paths are extracted verbatim from the source PPT and reused at the footer of every page and on the right-edge of the cover / ending.

## VI. Page Structure

### Decorative DNA

- **Recurring footer**: small red Lenovo mark (~80×27) bottom-left, copyright text "2026 Lenovo Internal. All rights reserved." (white on dark), page number bottom-right (white on dark).
- **Plum title typography** (when used): cool accent `#391262` in Dark.
- **Arial typography**: a single typeface family for both title and body, with weight contrast 700 / 400 — no decorative display fonts.
- **Right-edge rotated logo**: vertical red Lenovo wordmark on cover and ending, anchored to the right edge.
- **Dark cover**: full-bleed `#1E0113` solid (per source P1 Title Slide_Black) with white title and white tagline.
- **Dark ending**: deep plum `#3D0842` → deep red `#64131E` diagonal gradient (per source P142 Closing Slide_Black) with giant white "thanks." and white tagline.

### Layout Grid (dark pages: cover / toc / content / ending)

| Zone | Bounds |
|---|---|
| Top zone (no strip) | y: 0–80 |
| Title region | x: 80–1100, y: 100–300 (white Arial bold 32–80pt) |
| Primary content | x: 80–1200, y: 200–620 |
| Footer mark | x: 80, y: 666.5 (~80×27 red Lenovo mark) |
| Copyright | x: 170, y: 685, 13.33pt white |
| Page number | x: 1248, y: 688, 13.33pt white, text-anchor middle |

## VII. Page Types

| File | Role | Source layout | Description |
|---|---|---|---|
| `01_cover.svg` | cover | P1 Title Slide_Black | Full `#1E0113` solid bg; top-left "Smarter technology for all" tagline (white); 3-line white title; speaker/date subtitle (white); right-edge vertical red Lenovo mark; white footer mark + copyright |
| `02_toc.svg` | toc | P9 Section Header_White + agenda (dark surface) | Dark bg; left-aligned "AGENDA" eyebrow (white); white TOC title; 2×2 agenda grid with white 2-digit numbers + white titles + gray descriptions; white footer mark + copyright |
| `03_chapter.svg` | chapter | P9 Section Header_White (dark surface) | Dark bg; small white chapter numeral (top-left, all-caps); big white 80pt section title; white subhead below; white footer mark + copyright |
| `04a_content_one_col.svg` | content | P48 "Content Title" (dark surface) | Dark bg; white 42pt title; muted plum underline; 2-line white paragraph; 4-bullet list (white); white footer mark + copyright |
| `04b_content_two_col.svg` | content | P40 "Goals and objectives" | Dark bg; title + subtitle (white) on top; 3 stacked colored cards on the left (purple / dark-red / deep-plum, each with circular icon + title + desc + 2 bullets); 1 tall gradient card on the right (purple → plum, with title + desc + 3 bullets); white footer mark |
| `04c_content_three_col.svg` | content | P50 "List multi column" | Dark bg; title at top (white); 5 columns each with circular outline icon + colored short-title stripe (purple/pink/red/coral/lavender) + description + 3 bullets; white footer mark |
| `04d_content_three_deep.svg` | content | P60 "3 column deep" | 3 full-height color columns (red `#B23A2A` / purple `#6D1C69` / deep blue `#21386A`); each with circular white-line icon + 2-line white title + description; white page number (no footer mark on full-bleed page) |
| `05_section_title.svg` | content | P40 "Title with Subtitle Only" | Dark bg; large 58pt white title centered-left; muted plum underline; 22pt gray subtitle below; white footer mark |
| `06_image_text.svg` | content | P20 "Content with image layout" | Dark bg; left column with 32pt white title + 3 bullets + supporting text; right column large dashed-bordered image placeholder marked with `{{IMAGE}}` (use muted plum border); white footer mark |
| `07_photo_statement.svg` | content | P21 "Photo + Statement" | Full-bleed dashed-bordered image placeholder marked with `{{IMAGE}}`; semi-transparent dark overlay on the lower-left; 3-line white bold statement; muted plum accent line; white footer mark |
| `08_big_idea.svg` | content | (Big Idea layout) | Dark bg; centered 64pt muted-plum 2-line headline; muted plum accent line; centered 18pt light-gray supporting text; white footer mark |
| `09_blank.svg` | content | P23/P73 Blank Slide | Dark bg; only the recurring white footer mark + page number. Full canvas free for content insertion. |
| `10_ending.svg` | ending | P142 Closing Slide_Black | Deep-plum → deep-red gradient; top-right white 3-line tagline "Smarter technology for all"; right-edge vertical red Lenovo mark; center-left giant 200pt WHITE "thanks."; white footer mark + copyright |

All 12 user-authored SVGs + 1 fixed ending SVG, validated by `svg_quality_checker.py --template-mode --format ppt169`.

### Fixed pages (do not count toward `page_count`)

`10_ending.svg` is a **fixed page** — it is appended to every Lenovo deck as-is, with the original SVG untouched and none of the `placeholders` filled in by the executor.

## VIII. SVG Page Roster

| File | Role | One-line purpose |
|---|---|---|
| `01_cover.svg` | cover | Title slide; dark plum bg + white title + presenter + date + right-edge red mark |
| `02_toc.svg` | toc | Agenda / table of contents on dark surface |
| `03_chapter.svg` | chapter | Chapter divider on dark surface |
| `04a_content_one_col.svg` | content | Single-column body on dark surface |
| `04b_content_two_col.svg` | content | Two-column body (3 stacked left cards + 1 tall right card) |
| `04c_content_three_col.svg` | content | Multi-column list (5 icon + stripe + description + bullets) |
| `04d_content_three_deep.svg` | content | Three full-height color columns (red / purple / deep blue) |
| `05_section_title.svg` | content | Section pause / breathing slide on dark surface |
| `06_image_text.svg` | content | Left text + right image placeholder |
| `07_photo_statement.svg` | content | Full-bleed image + lower-left statement |
| `08_big_idea.svg` | content | Centered big idea on dark surface |
| `09_blank.svg` | content | Blank canvas with only the recurring footer |
| `10_ending.svg` | ending | Closing / thank-you page (deep-plum → deep-red gradient + giant white "thanks.") |

All SVGs hand-authored, validated by `svg_quality_checker.py --template-mode --format ppt169`, and committed.

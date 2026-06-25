---
brand_id: lenovo
kind: brand
summary: Lenovo corporate identity (OneLenovo palette) — light and dark themes
primary_color: "#E1251B"
themes: [light, dark]
default_theme: light
---

# Lenovo Brand Specification

> Identity-only preset with two themes. No SVG page roster — pages are composed freely under these constraints. Source artifacts live in `./sources/` (copies of `ref/Lenovo PPT Template 1*.potx`); the 141-slide `Lenovo PPT Template 2.potx` library stays under `ref/` and is **not** bundled here.

## I. Brand Overview

| Property | Value |
|---|---|
| Brand Name | Lenovo (联想) |
| Use Cases | Corporate / executive decks, product launches (Lenovo devices, infrastructure, services, solutions), internal town halls, sales enablement, training material |
| Tone | Professional, restrained, globally consistent, conclusion-first, low-emoji |
| Theme Selection | User picks `light` or `dark` at SKILL.md Step 4 (Eight Confirmations). Default `light`. Both themes share the same accent palette; only `bg` and `text` differ. |
| Page Anatomy | Three-act frame: cover (slide 1) → content pages (with footer + corner mark) → thanks / ending (last slide). Classification level (Unclassified / Internal / Confidential / Restricted) is required in every content-page footer — see §VII. |

The OneLenovo palette is the same `clrScheme` across both light and dark — the variant distinction lives in the slide background (`#FFFFFF` vs `#191919`) and the text color, not in the accent set. Strategy should pick the theme that matches the venue (light = projection in bright rooms / printed handouts; dark = keynote on stage / video export).

## II. Color Scheme

The accent set is shared across both themes; only `bg` and `text` invert. `primary_color` in the frontmatter is the accent1 value (`#E1251B`, Lenovo Red), used for emphasis and primary CTAs.

### II.1 Light Theme

| Role | HEX | Provenance | Notes |
|---|---|---|---|
| primary | `#E1251B` | fact | Lenovo Red — `accent1` in `ppt/theme/theme1.xml` (clrScheme `OneLenovo`); emphasis, primary CTA, focus highlights |
| secondary | `#F26A52` | fact | Coral — `dk2`; warm secondary tone for callouts |
| accent | `#871C23` | fact | Maroon — `accent2`; secondary red shade for dark-on-light emphasis |
| accent (lavender) | `#D9C1D8` | fact | `accent3`; soft secondary highlight, badge fills (also used as TOC numbered-circle fill in the deck; stays lavender on both themes — the bright spot on dark bg) |
| accent (deep purple) | `#4D144A` | fact | `accent4`; also the official wordmark color (see §IV) |
| accent (pale blue) | `#C9D0F0` | fact | `accent5`; cool secondary surface |
| accent (deep navy) | `#11184F` | fact | `accent6`; dark accent for contrast blocks |
| link | `#3046AD` | fact | `hlink`; hyperlinks, primary blue reference |
| text | `#1A1A1A` | approx | Body and headings on light bg (high contrast) |
| bg | `#FFFFFF` | fact | Slide background, card surfaces |
| surface | `#F5F5F5` | approx | Off-white — secondary card surfaces, tables |
| border | `#E0E0E0` | approx | Light gray — dividers, table borders |
| muted-text | `#6B6B6B` | approx | Mid gray — captions, axis labels |

### II.2 Dark Theme

| Role | HEX | Provenance | Notes |
|---|---|---|---|
| primary | `#E1251B` | fact | Lenovo Red — same red, accent1; the bright red keeps high contrast on dark bg |
| secondary | `#F26A52` | fact | Coral — same |
| accent | `#871C23` | fact | Maroon — same |
| accent (lavender) | `#D9C1D8` | fact | Same (also used as TOC numbered-circle fill in the deck; stays lavender on both themes — the bright spot on dark bg) |
| accent (deep purple) | `#4D144A` | fact | Same (but wordmark is reversed to white on this bg — see §IV) |
| accent (pale blue) | `#C9D0F0` | fact | Same |
| accent (deep navy) | `#11184F` | fact | Same; for darker accent blocks, pair with surface `#1F1F2A` for separation |
| link | `#5C7BD9` | approx | Lifted blue (was `#3046AD`) for legibility on dark bg |
| text | `#F2F2F2` | approx | Off-white body / headings on dark bg |
| bg | `#191919` | fact | Slide background — near-black (slide-master bg of the source dark variant) |
| surface | `#262626` | approx | Slightly lighter card / table surfaces |
| border | `#3A3A3A` | approx | Dark gray dividers |
| muted-text | `#A0A0A0` | approx | Light gray captions, axis labels |

> The two themes swap `bg` + `text` + `link` + `surface` + `border` + `muted-text`; the entire accent palette (`primary` / `secondary` / `accent` / `accent *`) is identical because the underlying `clrScheme` is the same. Strategist locks `default_theme` from the frontmatter as the pre-fill in Eight Confirmations and rotates to `themes[1]` only when the user explicitly asks for dark.

## III. Typography

| Role | Family | Weight |
|---|---|---|
| title | `Arial, "Microsoft YaHei", 黑体, sans-serif` | 700 |
| body | `Arial, "Microsoft YaHei", 黑体, sans-serif` | 400 |
| mono (optional) | `"Roboto Mono", Consolas, monospace` | 400 |

> Per the source `ppt/theme/theme1.xml` (major/minor Latin = `Arial`, East Asian = 黑体 / 宋体) and the slide-master title style (Arial Bold 32 pt sentence case). CJK fallback follows the theme's `+ea` font: 黑体 (Simplified) and 宋体 (Traditional) on Windows; `PingFang SC` / `Microsoft YaHei` on macOS. No proprietary brand font is required, so the stack renders cleanly without PPTX font embedding.

## IV. Logo

Single-lockup brand — one wordmark, two color variants (one per theme).

| File | Form | Usage |
|---|---|---|
| `./logo-light.png` | "Lenovo." wordmark in `#4D144A` deep purple, 1288×291 px, transparent bg (PNG, RGBA) | Cover hero, ending sign-off, any moment on a light / white background |
| `./logo-dark.png` | "Lenovo." wordmark in white, 1288×291 px, transparent bg (PNG, RGBA) | Cover hero, ending sign-off, any moment on a dark / near-black background; the dark variant is a recolor of the light artwork (white text on transparent) |

- Cover (slide 1): **required** — small wordmark in the top-left corner, theme-appropriate variant
- Thanks / ending (last slide): **required** — same wordmark in the top-left corner, mirroring the cover
- Per-page corner mark (every content slide): **required** — small wordmark in the top-right corner, theme-appropriate variant
- Clearspace: leave at least 0.5× wordmark height of empty space on all sides; never overlap text, photographic backgrounds, or the page-number element
- Wordmark color is fixed per file — do not re-tint at runtime; the dark variant exists precisely to avoid low-contrast re-tinting
- Source artifact: `sources/Lenovo PPT Template 1 - 浅色.potx` and `sources/Lenovo PPT Template 1 - 深色.potx` both embed the same `#4D144A` mark in their slide masters; the white-on-transparent dark file is a recolor of the source PNG (`ppt/media/image1.png`)
- Full page-frame specification (cover / content / thanks / footer text / corner mark) lives in §VII Page Anatomy

## V. Voice & Tone

- Formality: professional-neutral (corporate / B2B)
- Person: we / you (English); 我们 / 你 (Chinese)
- Emoji: avoid
- Abbreviations: spell-out-first-use (e.g. "Lenovo Group" on first mention, "Lenovo" thereafter; spell out product family names before using their codename)

## VI. Icon Style

- Preference: linear (stroke)

> Matches the icon library bundled in `ref/Lenovo PPT Template 2.potx` (151 SVG icons, predominantly `tabler` / `lucide` style strokes). When the deck uses `templates/icons/`, prefer the `tabler` or `lucide` stroke families; avoid filled libraries to stay consistent with the source's restrained visual language.

## VII. Page Anatomy

Every Lenovo branded deck ships a consistent three-act frame: cover (slide 1) → content pages (with footer + corner mark) → thanks / ending (last slide). This section fixes the placement of the wordmark, classification line, page number, and corner mark on each page. The Strategist renders these into SVG using the active theme's palette and the canvas format.

### VII.1 Cover (slide 1)

- Wordmark: top-left corner, ≤ 0.4× slide width, theme-appropriate variant (`logo-light.png` or `logo-dark.png`)
- Title: centered, Arial Bold 32pt, sentence case — **title text is replaceable per project**; the Strategist swaps the placeholder for the user's title
- Subtitle (optional): centered, beneath the title, Arial Regular 18pt — default placeholder is `<speaker name> | <date>`; the Strategist fills per project
- Background: theme `bg` color; no footer, no page number, no corner mark
- Optional hero image: lower 60% of the slide; title and wordmark stay in the upper 40% / top-left

### VII.2 Content page (every slide between cover and thanks)

- Corner mark: small wordmark in the top-right corner, ≤ 0.3× slide width, theme-appropriate variant
- Title: top-left, left-aligned, Arial Bold 28pt, sentence case
- Body: full content area below the title (page-type dependent)
- Footer: full-width strip along the bottom of the slide, three zones:
  - **Left zone** — classification line (see §VII.3 for the four levels)
  - **Center zone** — small deck title, Arial Regular 9pt italic, `muted-text` color
  - **Right zone** — page number, `X / N` format, Arial Regular 9pt
- Footer separator: 0.5pt horizontal rule in `border` color, ~0.1" above the footer text

### VII.3 Classification levels

Lenovo decks carry one of four classification markings in the content-page footer. The default is **Internal**; the user confirms the level at Eight Confirmations. The language below is mirrored from the source guidance slides (`sources/Lenovo PPT Template 1 - 浅色.potx` slide 8 / 9).

| Level | Footer text | Use case |
|---|---|---|
| Unclassified | `©2026 Lenovo. All rights reserved.` | Public decks, marketing, external-facing material |
| **Internal** (default) | `©2026 Lenovo Internal. All rights reserved.` | Cross-team sharing; the default for most internal use |
| Confidential | `©2026 Lenovo Confidential. All rights reserved.` | Information that should not leave a defined group |
| Restricted | `©2026 Lenovo Restricted. All rights reserved.` | Maximum protection; distribution limited to designated individuals |

### VII.4 Thanks / ending (last slide)

Mirrors the cover for symmetry. Layout **mirrors the source's thanks treatment** (`sources/Lenovo PPT Template 1 - 浅色.potx` slide 15: a single centered title placeholder reading "Thanks"):

- Wordmark: top-left corner, same size and position as the cover, theme-appropriate variant
- Title: centered, Arial Bold 96pt — content is the literal "Thanks" (or `感谢` for CJK decks); not replaced per project
- Optional secondary line: contact / Q&A prompt beneath the title, Arial Regular 24pt
- Background: theme `bg` color; no footer, no page number, no corner mark (the wordmark alone provides the brand signal)
- If the user wants a Q&A contact card, add it as a separate content page immediately before the thanks page

### VII.5 Chapter divider

A single-section break page between major parts of the deck. One slide, full-bleed, no body content beyond the chapter title. Concrete implementation: `templates/decks/lenovo/02_chapter.svg`.

- Wordmark: top-left, theme-appropriate variant (matches the cover's wordmark choice)
- Optional small "Part" / "Section" / "Chapter" label above the title — Arial Italic 14pt, `muted-text` color, centered (placeholder: `{{CHAPTER_LABEL}}`, e.g. `PART 01`, `SECTION A`, `CHAPTER 3`)
- Title: centered, Arial Bold 54pt — content is `{{CHAPTER_TITLE}}`
- Description: centered beneath the title, Arial Regular 20pt, `muted-text` color — content is `{{CHAPTER_DESC}}`
- 3-zone footer (per §VII.2): classification line / `{{DECK_TITLE}}` / `{{PAGE_NUM}} / {{TOTAL_PAGES}}`
- Background: theme `bg` color (the deck's chapter page renders dark even on a light deck — a section break is a visual moment, not a theme choice)
- No page transitions / entrance animations by default — the Strategist may opt in via `customize-animations` if the user asks

### VII.6 Table of contents

A single-page overview of the deck's 2–6 sections, presented as a 2×3 numbered grid. Concrete implementation: `templates/decks/lenovo/02_toc.svg` (light) and `02_toc_dark.svg` (dark).

- Wordmark: top-left, theme-appropriate variant
- Heading: top-left, Arial Bold 32pt, e.g. "Contents"; an optional 3px red accent line (Lenovo Red, `#E1251B`) sits ~3px under the heading, ~162px wide
- Numbered items: 2×3 grid of 68px-diameter lavender circles (`#D9C1D8`, the brand's `accent (lavender)`); the same lavender fill is used on both themes — on the dark TOC it is the bright spot against the near-black background
- Inside each circle: the section number in Arial Bold 28pt, near-black (`#1A1A1A`), centered (placeholders `{{TOC_NUM_1}}`–`{{TOC_NUM_6}}` so the Strategist can fill non-consecutive numbers)
- To the right of each circle: item title in Arial Bold 18pt (`{{TOC_ITEM_N_TITLE}}`) and optional description in Arial Regular 14pt, `muted-text` color (`{{TOC_ITEM_N_DESC}}`)
- Items 4–6 are optional — the Strategist hides a row by leaving its `_TITLE` and `_DESC` placeholders empty
- 3-zone footer (per §VII.2)

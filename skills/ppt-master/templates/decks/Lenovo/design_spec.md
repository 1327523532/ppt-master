---
deck_id: Lenovo
kind: deck
template_role: brand_shell
summary: Minimal Lenovo brand shell with restrained background colors and logo only; use when content layout should be generated freely.
canvas_format: ppt169
page_count: 5
primary_color: "#E1251B"
placeholders:
  01_cover: []
  02_chapter: []
  02_toc: []
  03_content: []
  04_ending: []
---

# Lenovo Minimal Brand Shell - Design Specification

> This deck intentionally keeps only Lenovo brand background colors and logo marks. It does not prescribe content modules, typography placeholders, agenda structures, or chart layouts.

## I. Template Overview

| Property | Description |
| --- | --- |
| **Template Name** | Lenovo |
| **Display Name** | Lenovo Minimal Brand Shell |
| **Use Cases** | Lenovo-branded presentations where the executor should create page-specific layout freely |
| **Design Tone** | Clean, restrained, corporate, brand-led |
| **Theme Mode** | Minimal brand shell: light neutral pages, dark burgundy overview page, restrained red/plum brand zones |

## II. Canvas Specification

| Property | Value |
| --- | --- |
| **Format** | Standard 16:9 |
| **Dimensions** | 1280 x 720 px |
| **viewBox** | `0 0 1280 720` |
| **Safe Margins** | 80px left/right, 56px top, 56px bottom |
| **Primary Content Area** | x: 80-1080 on cover/chapter, x: 80-1160 on content pages, y: 140-620 |

## III. Color Scheme

| Role | Color Value | Usage |
| --- | --- | --- |
| **Lenovo Red** | `#E1251B` | Logo block, thin top rule, narrow side brand bars |
| **Deep Plum** | `#4D144A` | Subtle background geometry and dark-page support |
| **Dark Burgundy** | `#1E0013` | Dark overview / divider background |
| **Black** | `#111111` | Optional divider opacity on light pages |
| **White** | `#FFFFFF` | Light page background and reverse logo text |
| **Soft Neutrals** | `#F7F5F8` / `#F1EEF4` / `#EAEAF5` | Light background depth |

## IV. Typography System

This template does not lock content typography. Use the project default type system unless a source deck or user instruction overrides it.

Logo text uses `Arial, sans-serif` as a vector-safe approximation for the Lenovo wordmark lockup.

## V. Page Structure

### Design Intent

1. Keep brand identity visible without forcing a fixed page layout.
2. Leave the main body open for generated content, charts, images, or diagrams.
3. Use Lenovo red in small but unmistakable brand zones.
4. Avoid imported photo backgrounds and PPTX sample content.
5. Avoid large translucent white panels over the background; they make pages look like generic card overlays rather than Lenovo-branded slides.

### Page Types

| File | Role | Description |
| --- | --- | --- |
| `01_cover.svg` | cover | Light neutral cover shell with thin top rule, narrow right brand bars, and Lenovo logo |
| `02_chapter.svg` | chapter | White chapter shell with logo, fine rule, and narrow side brand zone |
| `02_toc.svg` | toc | Dark burgundy shell with logo, fine rules, and side brand bar |
| `03_content.svg` | content | White content shell with top rule, logo, and subtle footer rule |
| `04_ending.svg` | ending | Light neutral closing shell with Lenovo logo and subtle geometry |

## VI. Usage Rules

1. Treat these SVGs as branded backgrounds, not filled slide layouts.
2. Executor may place titles, body content, diagrams, charts, or images in the open content area.
3. Do not reintroduce the old PPTX sample text, photo strips, lorem ipsum modules, or numbered agenda placeholders.
4. Keep Lenovo red as the primary brand signal and avoid competing dominant accent colors.
5. On cover and chapter pages, place title text directly on the open background; do not add a large card, frosted rectangle, or full-width translucent panel behind the title unless the user explicitly requests that style.
6. Keep generated content clear of the right-side red/plum brand zone on cover and dark overview pages.

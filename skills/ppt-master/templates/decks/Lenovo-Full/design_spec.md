---
template_id: Lenovo-Full
category: brand
summary: Lenovo-branded full-content decks — large multi-chapter reports, customer case libraries, internal training, full Lenovo brand language coverage with extensive chapter/content variant surface.
keywords: [lenovo, enterprise, full-library, replica, multi-chapter]
primary_color: "#E1251B"
canvas_format: ppt169
replication_mode: standard
---

# Lenovo-Full — Design Specification

## I. Template Overview

Lenovo enterprise presentation template designed for comprehensive slide libraries, multi-chapter reports, and internal training materials. The visual language balances corporate professionalism with subtle brand energy through the signature Lenovo red accent (#E1251B) against predominantly white or dark burgundy backgrounds.

**Theme mode**: Light (white-based content pages) with dark accent sections (burgundy/maroon backgrounds for cover and special pages).

**Visual identifiers at a glance**:
- Large, bold sans-serif titles with tight letter-spacing (-2px)
- Lenovo wordmark in red bar with white logotype at footer
- Minimal decoration — emphasis on typography and structured layouts
- Four-column SWOT layouts, problem/solution arrow diagrams, numbered agenda items

## II. Color Scheme

| Role | HEX | Usage |
|------|-----|-------|
| Primary (Lenovo Red) | `#E1251B` | Footer bar, accent elements, brand marker |
| Dark Background | `#1E0113` | Cover pages, dark section slides |
| Burgundy | `#4D144A` | SWOT quadrants, dark accents |
| Deep Purple | `#6D1C69` | Secondary SWOT quadrant |
| Coral Red | `#F26A52` | Tertiary SWOT quadrant, arrows |
| Warm Red | `#B8252E` | Quaternary SWOT quadrant |
| Light Lavender | `#AAB1ED` | Numbered circles, subtle accents |
| Text Primary | `#0D0D0D` | Body text on light backgrounds |
| Text Secondary | `#FFFFFF` | Text on dark backgrounds |
| Subtle Gray | `#64748B` | Secondary text, captions |

## III. Typography

(Omitted — uses canonical Arial stack as specified in brief)

## IV. Signature Design Elements

**Lenovo Footer Bar**: Red (#E1251B) horizontal bar at bottom-left of content pages containing the white "Lenovo" wordmark. The logo is constructed from vector paths (not an image asset).

```xml
<!-- Lenovo logo footer bar -->
<rect x="80" y="666" width="82" height="27" fill="#E1251B"/>
<!-- Vector wordmark paths for "Lenovo" in white -->
```

**Letter-spacing convention**: All titles use `letter-spacing: -2` for a modern, condensed appearance.

**Page number placement**: Bottom-right corner, 13px font size, matches background contrast (white text on dark, dark text on light).

**Section divider patterns**: SWOT layouts use four equal-width colored columns without borders — color differentiation alone defines boundaries.

## V. Page Roster

| Filename | Purpose | Visual Character | Content Slot |
|----------|---------|------------------|--------------|
| `01_cover.svg` | Cover page | Dark burgundy background (#1E0113), large multi-line white title, subtitle line, no footer bar | Title, subtitle, date/author |
| `02_toc.svg` | Table of contents | Dark background, numbered circles (1-6) with lavender fill, section titles in white, optional image tiles | TOC title, up to 6 section entries |
| `02_chapter.svg` | Chapter divider | White background, large bold chapter title left-aligned, minimal decoration | Chapter title, optional subtitle |
| `03_content.svg` | Content page | White background, page title with description line, flexible content area, Lenovo footer bar | Page title, description, content area |
| `04_ending.svg` | Ending page | Gradient background (radial burgundy to purple), subtle "thanks" text | Closing message, optional contact |

## VI. Assets

The Lenovo logo wordmark is embedded as vector paths within the SVG files — no external image assets required for the template skeleton. Projects using this template may add:
- Product images for cover backgrounds
- Team photos for ending slides
- Custom icons from the project icon library

## VII. Placeholder Overrides

None — uses canonical placeholder vocabulary defined in template-designer.md.

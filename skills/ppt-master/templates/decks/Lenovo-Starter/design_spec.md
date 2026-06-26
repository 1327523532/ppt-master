---
template_id: Lenovo-Starter
category: brand
summary: Lenovo-branded enterprise light decks — product launches, partner-facing materials, internal reports. Compact starter pack with the essential 5 page types.
keywords: [lenovo, enterprise, light, replica, starter]
primary_color: "#E1251B"
canvas_format: ppt169
replication_mode: standard
---

# Lenovo-Starter — Design Specification

## I. Template Overview

**Use cases**: Product launches, partner presentations, internal reports, sales decks, training materials.

**Design tone**: Clean, professional, enterprise-appropriate. Lenovo signature red accents on white backgrounds. Minimalist decoration with maximum readability.

**Theme mode**: Light — white surface (#FFFFFF), dark text, red accents.

**Visual identity at a glance**: The deck is recognized by the Lenovo red bar with logo in the footer, the generous use of white space, and the signature gradient decorations on select pages (soft pink-to-blue diagonal gradients on cover/TOC pages).

## II. Color Scheme

| Role | HEX | Usage |
|------|-----|-------|
| Primary (accent1) | `#E1251B` | Lenovo signature red — footer bar, chapter backgrounds, accent highlights |
| Deep Red 1 | `#64131E` | Gradient stops, dark accents |
| Deep Red 2 | `#B8252E` | Secondary red tones |
| Deep Purple 1 | `#4D144A` | Gradient stops, alternative dark accents |
| Deep Blue 1 | `#11184F` | Gradient stops, dark blue accents |
| Text primary | `#000000` | All body text, titles |
| Text secondary | `#FFFFFF` | Text on dark backgrounds |
| Background light | `#FFFFFF` | Page surface (light theme) |
| Background dark | `#1E0113` | Chapter/ending page backgrounds |
| Pale Blue | `#DDE0F8` | Step list backgrounds, info panels |
| Pale Red | `#FCE1DC` | Accent panels |

## III. Typography

Uses the canonical Arial stack: `Arial, "Microsoft YaHei", sans-serif`.

## IV. Signature Design Elements

### Footer Brand Bar
Every page includes a footer brand bar:
- Red rectangle (`#E1251B`) positioned at bottom-left: `x=80`, `y=666`, `width=82`, `height=27`
- Lenovo wordmark in white inside the red bar (vector paths for "Lenovo" text)

### Page Number Placement
Page numbers appear at bottom-right: `x=1225`, `y=672`, in 13px Arial.

### Gradient Decoration (Cover/TOC)
Cover and TOC pages use a soft diagonal gradient overlay:
- From bottom-left pink (`#FDE7E3`) to top-right blue (`#CAD3E5`)
- Applied as a right-side decorative panel

### Chapter Page Treatment
Chapter pages use:
- Full dark background (`#1E0113`)
- Large bold white title (80px, letter-spacing -2)
- Smaller white subhead (33px)
- Footer brand bar with Lenovo logo

## V. Page Roster

| Filename | Purpose | Visual Character |
|----------|---------|------------------|
| `01_cover.svg` | Cover slide | White background, large multi-line bold title (107px), subtitle at bottom, page number. Minimal — no decoration except footer brand bar. |
| `02_toc.svg` | Table of contents | White background with right-side gradient decoration panel. Title at top, bullet list content area on left, screenshot/hero image placeholder on right. Footer brand bar. |
| `02_chapter.svg` | Chapter divider | Full dark background (`#1E0113`). Large white bold title centered vertically, white subhead below. Footer brand bar with Lenovo logo. |
| `03_content.svg` | Content page | White background. Bold title at top (43px), flexible content area below. Footer brand bar and page number. Maximum flexibility for AI-driven layouts. |
| `04_ending.svg` | Thank-you/ending | Full white background. Large "Thanks" text (or `{{THANK_YOU}}` placeholder). Lenovo logo centered. Footer brand bar. |

## VI. Assets

| File | Dimensions | Usage |
|------|------------|-------|
| `assets/ending_logo.png` | 824x186 | Lenovo logo for ending page |

## VII. Placeholder Overrides

None — uses canonical placeholder vocabulary.

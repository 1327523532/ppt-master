---
brand_id: lenovo
kind: brand
summary: Lenovo brand identity — global enterprise decks, product launches (ThinkPad / IdeaPad / ThinkSystem), internal communications, partner-facing materials
primary_color: "#E1251B"
---

# Lenovo Brand Specification

> Identity-only preset. No SVG page roster — pages are composed freely under these constraints.

## I. Brand Overview

| Property | Value |
|---|---|
| Brand Name | Lenovo |
| Use Cases | Lenovo global enterprise decks, product launches (ThinkPad / IdeaPad / ThinkSystem), internal communications, partner-facing materials [approx] |
| Tone | Tech-corporate, restrained, brand-led, "Smarter technology for all" [approx] |

## II. Color Scheme

| Role | HEX | Provenance | Notes |
|---|---|---|---|
| primary | `#E1251B` | fact | Lenovo Red — extracted from `ref/Lenovo-template_light.pptx` theme (accent1) |
| secondary | `#871C23` | fact | Darker Lenovo Red — extracted from ref PPT theme (accent2); supporting brand zones |
| accent (warm) | `#F26A52` | fact | Coral — extracted from ref PPT theme (dk2); highlights, callouts |
| accent (alert) | `#4D144A` | fact | Deep purple — extracted from ref PPT theme (accent4); risk / contrast |
| text | `#000000` | fact | Body text on light background (dk1) |
| text (reverse) | `#FFFFFF` | fact | Text on dark / brand-color surfaces (lt1) |
| bg | `#FFFFFF` | fact | Pure white page background (lt1) |

The first four rows are the official Lenovo brand surface (extracted directly from the ref PPT theme XML). The text / bg pair follows the theme's `dk1` / `lt1` convention. The warm / alert accent pair (coral + deep purple) gives Strategist room for content-type differentiation (warm = callouts, alert = high contrast) without leaving the brand's restrained palette. Strategist may rotate the accent role per page rhythm.

## III. Typography

| Role | Family | Weight |
|---|---|---|
| title | `Arial, "Microsoft YaHei", sans-serif` | 600–700 |
| body | `Arial, "Microsoft YaHei", sans-serif` | 400 |

> Ref PPT theme exposes `Arial` for both `majorLatin` (title) and `minorLatin` (body). Lenovo's public brand uses custom corporate typefaces that are not embedded in the ref PPT, so `Arial` is treated as the de-facto brand family with `Microsoft YaHei` as the CJK fallback. No PPTX font embedding is required for the title / body chain because Arial is universally available; if a richer Lenovo brand face becomes available later, add it as the first family in the chain.

## IV. Logo

Lenovo's branded source deck (`ref/Lenovo-template_light.pptx`) does not embed a discrete logo file in `assets/` (the importer renamed every media file to `image{N}.{ext}`, and the visible "Lenovo" wordmark on the cover and ending is rendered via PowerPoint Freeform paths inside the slide layout, not as a separate image asset). The brand package ships a vector-extracted `lenovo_mark.svg` (81.6×27.22 viewBox, red `#E1251B` panel + 6 white "Lenovo" letterforms as paths) where the path data is taken verbatim from the recurring footer mark on ref slide_01/03/04. The same letterform paths are reused at scaled-up sizes on the deck's cover (rotated -90°, ~4×) and ending (~6×), and are recolored to plum `#4D144A` on the ending's signature "thanks." page. No separate wordmark or lockup file is fabricated.

| File | Form | Usage |
|---|---|---|
| `./lenovo_mark.svg` | Vector-extracted red rectangle (81.6×27.22) + 6 white "Lenovo" letterforms as paths (theme accent1 `#E1251B`) | Recurring footer element on every deck page; rotated-and-scaled cover signature; vertical right-edge wordmark on the ending |

- Cover: prefer the mark (and a scaled-up rotated variant on the right edge as the cover signature, per ref slide_02 layout-shape-14)
- Ending: a vertical red variant on the right edge; the giant hero text on the ending is the plain sans-serif "thanks." wordmark in plum (NOT the official Lenovo letterforms), per the canonical Lenovo thanks page
- Per-page (TOC / content / chapter): mark appears bottom-left as the recurring footer
- Clearspace: leave at least 0.5× mark height of empty space on all sides; never overlap text or photographic backgrounds
- Mark color is fixed at `#E1251B`; the white letterforms inside the mark are non-recolorable

## V. Voice & Tone

- Formality: professional-neutral [approx]
- Person: we / you (English), 我们 / 你 (Chinese)
- Emoji: avoid
- Abbreviations: spell-out-first-use

## VI. Icon Style

- Preference: stroke [approx]

> Outline / stroke icons read as "engineering / enterprise" and align with Lenovo's restrained product-UI aesthetic. When the deck uses `templates/icons/`, prefer `tabler` or `lucide` stroke families over filled libraries.


## VII. Theme Variants

Lenovo's branded source deck (`ref/Lenovo-template.pptx`) ships both a **light** and a **dark** variant of every page. The brand identity (colors, typography, logo, voice) is shared; only the surface treatment differs. Both variants ship from the same `templates/brands/lenovo/` package.

### Light theme (default)

| Surface | Token | HEX | Usage |
|---|---|---|---|
| Page bg | `surface.bg` | `#FFFFFF` | Cover / TOC / content / chapter backgrounds |
| Body text | `text.primary` | `#000000` | Body text on light surfaces |
| Title text | `text.title` | `#000000` | Headlines on light surfaces |
| Reverse text | `text.reverse` | `#FFFFFF` | Text on red / plum surfaces |
| Accent warm | `accent.warm` | `#F26A52` | Coral highlights |
| Accent cool | `accent.cool` | `#4D144A` | Deep plum dividers |

### Dark theme

| Surface | Token | HEX | Usage |
|---|---|---|---|
| Page bg | `surface.bg` | `#1E0113` | Cover / TOC / content / chapter backgrounds (dark plum/black) |
| Body text | `text.primary` | `#FFFFFF` | Body text on dark surfaces |
| Title text | `text.title` | `#FFFFFF` | Headlines on dark surfaces (80pt bold per slide_13) |
| Reverse text | `text.reverse` | `#E1251B` | Text on red mark surfaces (the mark stays red on both themes) |
| Accent warm | `accent.warm` | `#64131E` | Muted dark red highlights |
| Accent cool | `accent.cool` | `#391262` | Deep purple (matches dark ending gradient stops) |

**Invariant tokens** (do not change between themes):
- `brand.primary` = `#E1251B` (Lenovo red — used for the mark)
- `brand.secondary` = `#871C23` (darker Lenovo red)
- Logo file = `./lenovo_mark.svg` (vector-extracted, red panel + white letterforms)
- Typography = Arial / Microsoft YaHei (both themes)

**Theme selection rule:** Use light by default. Use dark when the audience expects a dark presentation (e.g. cinema-style keynotes, internal review boards, evening launches). The two themes share the same outline structure (cover / TOC / content / chapter / ending) so the executor can swap between them by changing only the surface tokens above.

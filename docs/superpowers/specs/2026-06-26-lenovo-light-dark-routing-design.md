# Lenovo Light/Dark Routing Optimization — Design

**Date:** 2026-06-26
**Scope:** Make `templates/decks/Lenovo-Light/` and `templates/decks/Lenovo-Dark/` self-describing for light-vs-dark selection.

## Problem

Two Lenovo decks exist side by side but their metadata does not let a reader (human or AI) tell from a glance which is light and which is dark, nor when to pick one over the other. Concrete gaps:

1. `decks_index.json` has no `theme` field — discovery cannot distinguish the two.
2. `Lenovo-Light/design_spec.md` has `deck_id: Lenovo` while the directory and index key are `Lenovo-Light`. `Lenovo-Dark/design_spec.md` is consistent (`deck_id: Lenovo-Dark`).
3. Neither spec tells the reader *when to pick this deck* — Strategist at Step 3 reads the spec but has no routing cue.
4. The brand spec §VII covers both themes side-by-side but the deck specs duplicate only fragments of that and do not cross-link.

## Goal

A user who says "用联想浅色模板" / "联想深色版" / "Lenovo light theme" / "Lenovo dark deck" can be routed to the correct `templates/decks/Lenovo-{Light|Dark}/` deterministically, **without** changing SKILL.md's Step 3 trigger rule (bare names never auto-fire — this is intentional).

The optimization works *within* the existing trigger model: it makes the two specs self-describing when they *are* picked (via explicit path or Step 3 confirmation), and it makes the discovery index (`decks_index.json`) answer "which Lenovo deck is light/dark?" without opening a spec.

## Approach (Sibling Pair with Explicit Routing)

The two decks stay as separate atomic packages (they have separate SVG rosters). Routing is added through three channels:

1. **Index field** (`decks_index.json`): add `theme` to each entry.
2. **Frontmatter fix** (`Lenovo-Light/design_spec.md`): change `deck_id: Lenovo` → `deck_id: Lenovo-Light`.
3. **Routing hint** (both specs): a short "When to use this deck" block after the frontmatter table that names the user phrasings it answers and cross-links to its sibling.

No SKILL.md change. No brand spec change (it already covers both themes under §VII).

## File-by-file Changes

### A. `templates/decks/decks_index.json`

Add `"theme": "light"` and `"theme": "dark"` to the respective entries. Existing fields (`summary`, `canvas_format`, `page_count`, `primary_color`) stay.

### B. `templates/decks/Lenovo-Light/design_spec.md`

- Frontmatter: `deck_id: Lenovo` → `deck_id: Lenovo-Light`.
- Insert after frontmatter and before `# Lenovo - Design Specification`: a new `## Selection Guidance` section with:
  - Trigger phrasings ("联想浅色模板", "Lenovo light deck", etc.)
  - Cross-link to `../Lenovo-Dark/design_spec.md` for dark use cases.
  - One-line rationale.

### C. `templates/decks/Lenovo-Dark/design_spec.md`

- Frontmatter: no change (already correct).
- Insert after frontmatter and before `# Lenovo-Dark - Design Specification`: a matching `## Selection Guidance` section, symmetric with the light spec.

## Non-Goals

- **Not changing SKILL.md** trigger rule. Bare-name auto-routing is a wider architecture decision that affects all 11 decks; out of scope.
- **Not merging the two decks.** They have different SVG rosters and need to stay separate.
- **Not editing the brand spec.** §VII already covers both themes; the deck specs cross-link instead of duplicating.
- **Not adding a new template kind.** Both decks stay `kind: deck`.

## Verification

1. `decks_index.json` validates as JSON and contains `theme` for both Lenovo entries.
2. Both design specs parse as Markdown with valid YAML frontmatter.
3. Both `deck_id` values match their directory names.
4. A grep over both specs finds the cross-link phrase `Lenovo-Dark` in the light spec and `Lenovo-Light` in the dark spec.

## Risks

- **Tooling that does NOT validate unknown JSON fields** will silently accept the new `theme` key — verified safe because the index is consumed by Strategist, which reads it as a discovery aid.
- **Tooling that DOES validate strict JSON schema** could reject the new field. None found in the current repo (no JSON Schema files reference `decks_index.json`); safe to proceed.
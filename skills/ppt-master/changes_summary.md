# ppt-master-lenovo Change Summary

| Category | Path / File | Change | Purpose / Impact |
|---|---|---|---|
| Removed assets | `references/ai-image-comparison/palette/*.png` | Removed 14 palette reference PNGs | Reduces skill size and avoids distracting illustration references; does not affect PPT generation |
| Asset docs | `references/ai-image-comparison/README.md` | Updated `palette/` description to say only manifests/prompts are retained | Keeps documentation aligned with removed PNGs |
| Asset manifests | `references/ai-image-comparison/palette/_manifest.json` / `_manifest.md` | Changed palette image state semantics from generated assets to pending/regenerable assets | Indicates images are no longer bundled and can be regenerated when needed |
| Strategist guidance | `references/strategist.md` | Updated guidance so Strategist does not rely on removed palette images | Prevents future agents from assuming bundled palette reference images exist |
| New Lenovo template | `templates/decks/Lenovo/01_cover.svg` | Added Lenovo cover brand shell | Provides Lenovo background color and logo only |
| New Lenovo template | `templates/decks/Lenovo/02_chapter.svg` | Added Lenovo chapter brand shell | Provides Lenovo background color and logo only |
| New Lenovo template | `templates/decks/Lenovo/02_toc.svg` | Added Lenovo TOC brand shell | Provides Lenovo background color and logo only |
| New Lenovo template | `templates/decks/Lenovo/03_content.svg` | Added Lenovo content brand shell | Provides Lenovo background color and logo only |
| New Lenovo template | `templates/decks/Lenovo/04_ending.svg` | Added Lenovo ending brand shell | Provides Lenovo background color and logo only |
| Template spec | `templates/decks/Lenovo/design_spec.md` | Defined Lenovo as a `brand_shell` template | Keeps only brand background, logo, safe zones, and brand constraints; avoids complex inherited layout |
| Template registry | `templates/decks/decks_index.json` | Registered `Lenovo` as a deck template | Makes the Lenovo template selectable by the skill |
| Template schema docs | `templates/decks/README.md` | Added `template_role: replica | brand_shell` explanation | Distinguishes full layout replica templates from lightweight brand shells |
| Executor rules | `references/executor-base.md` | Added `brand_shell` interpretation rule | Prevents large translucent panels, frosted cards, or default card containers from being added over brand-shell backgrounds unless requested |
| Executor rules | `references/executor-base.md` | Added PPTX-safe manual wrapping rule | Requires long titles, subtitles, bullets, captions, labels, and prose to be explicitly broken with `<tspan>` in SVG |
| Executor rules | `references/executor-base.md` | Marked cover/chapter/ending pages as high-risk text layout pages | Targets the title wrapping and overflow issues seen in the generated PPT |
| Shared standards | `references/shared-standards.md` | Added “PPTX-safe wrapping is authored, not delegated” | Makes manual text wrapping a shared quality standard, not only an executor preference |
| Quality checker | `scripts/svg_quality_checker.py` | Added `_check_unwrapped_text_fit` | Detects overlong single-line `<text>` elements before PPTX export |
| Quality checker | `scripts/svg_quality_checker.py` | Added `Text layout issues` error category | Turns likely PPTX text drift/overflow into a blocking quality issue |
| Main workflow | `SKILL.md` | Added `Visual Review` to the explicit pipeline | Makes visual verification part of the formal workflow |
| Main workflow | `SKILL.md` | Added `VISUAL REVIEW IS AN EXPORT BLOCKER` | Requires visual review before `finalize_svg.py` or `svg_to_pptx.py` |
| Main workflow | `SKILL.md` | Added Step 7 checks for `.review/visual_review_summary.md` and per-page JSON files | Prevents agents from exporting without persisted visual-review artifacts |
| Main workflow | `SKILL.md` | Added final-response requirement to report visual-review status and summary path | Prevents agents from claiming a PPT is complete when visual review was skipped |
| Visual review workflow | `workflows/visual-review.md` | Clarified that live preview is not visual review | Prevents agents from treating preview startup as validation |
| Visual review workflow | `workflows/visual-review.md` | Required `.review/visual_review_summary.md` plus one JSON result per page | Gives the visual-review gate concrete, checkable outputs |
| Validation | Lenovo template | Ran `python3 scripts/register_template.py Lenovo --kind deck` | Lenovo deck registration passed |
| Validation | Lenovo template | Ran `python3 scripts/svg_quality_checker.py templates/decks/Lenovo --template-mode --format ppt169` | Lenovo template quality check passed, 5/5 |
| Validation | Quality checker | Ran `python3 -m py_compile scripts/svg_quality_checker.py` | Quality checker syntax passed |
| Validation | User sample PPT project | Ran SVG quality checker on the DeepSeek/GPT project SVG output | New text-layout rule flagged P02-P05 as long single-line text risks |

## Not Yet Changed

| Path / Area | Current Status | Note |
|---|---|---|
| `references/ai-image-comparison/rendering/*.png` | Inspected but not deleted | These 20 PNGs are reference-only rendering examples, about 24 MB total. They are not hard dependencies for PPT generation or export. |


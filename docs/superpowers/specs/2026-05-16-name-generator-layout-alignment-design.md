# Name Generator Layout Alignment Design

## Goal

Align every `template-deploy/tools-src/*name-generator.html` template with the `random-name-generator.html` structural pattern for the filter panel, generated results area, and saved names placement, while adding a `Regenerate` button beside `Copy all` in the generated-results header.

## Scope

- Target all template files in `template-deploy/tools-src/` whose filenames end in `name-generator.html`, including `random-name-generator.html`.
- Standardize the shared tool layout only.
- Preserve each page's dataset-specific filters, result-card content, copy, and scripts.

## Design

### Shared structure

- Keep the outer `tool-card` and `tool-split` pattern.
- Use a left `ctrl` column for filters and a right `words-panel` column for generated names.
- Place `saved-section` after `tool-split`, so it sits below both the filter and results sections.

### Shared actions

- In the generated results header, place `Copy all` and `Regenerate` together inside `words-actions`.
- `Regenerate` should trigger the existing page generate button by clicking that page's `*-gen-btn`.

### Shared styling

- Normalize the structural styles for `.ctrl`, `.words-panel`, `.words-top`, `.words-actions`, `.word-list`, and `.saved-section`.
- Keep page-specific result styling such as badges, chips, pinyin, Hanzi, and meaning treatments unchanged.
- Preserve mobile toggle behavior and collapse behavior already used by the templates.

## Constraints

- Do not rewrite each generator's business logic.
- Do not remove ads or explainer content.
- Do not revert unrelated user changes in the working tree.

## Verification

- Confirm every target template has:
  - a `Regenerate` button in the results header
  - a `saved-section` located after `tool-split`
  - normalized control width and shared results layout selectors
- Spot-check representative templates from the reference page, a simple page, and a more custom page.

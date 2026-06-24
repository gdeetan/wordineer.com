# A-Words Page "Show More" Design

## Goal

Update the `5-letter-words-starting-with-a` page so it can support a much larger dataset without rendering every word card immediately on first view. The page should continue to load the full filtered dataset client-side, but only display an initial batch of cards and allow the user to reveal more with a `Show more words` button.

This change is intended to keep the page usable if `wordineer-deploy/data/five-letter-words-a.json` grows from its current curated size to a much larger list in the `1000+` range.

## Scope

In scope:

- Update the A-word page rendering logic in `template-deploy/tools-src/5-letter-words-starting-with-a.html`
- Add UI for progressive disclosure of word cards
- Keep filtering, copy/export, and idle full-dataset loading behavior working
- Ensure the results label reflects visible count versus total filtered count

Out of scope:

- Expanding the dataset itself
- Changing sitewide shared generator behavior
- Adding numbered pagination or infinite scroll
- Altering the page's visual style beyond the small control needed for `Show more`

## Recommended Approach

Use append-in-place progressive disclosure:

1. Load the full dataset the same way the page already does.
2. Render an initial batch of cards, recommended at `50`.
3. Add a `Show more words` button below the grid.
4. Each click appends the next batch from the current filtered result set.
5. Reset back to the first batch whenever filters change.

This is preferred over numbered pagination because users on this page are scanning and filtering rather than navigating to exact positions in the list.

## Behavior

### Initial state

- Before the full JSON loads, the page continues to render from the existing `SEED` data.
- After the full JSON loads, the page re-renders using the current filters.
- Only the first batch of matching results is shown.

### Batch size

- Use a constant batch size of `50`.
- The page shows up to `50` items initially.
- Each `Show more words` click reveals the next `50`.

### Filter changes

- When the user changes `Type` or `Difficulty`, recompute the filtered list.
- Reset the visible count to the initial batch size.
- Re-render the grid from the start of the newly filtered list.

### Results label

- Replace the simple total-only count with a visible/total label.
- Example: `Showing 50 of 1124 words`
- If the total matching set is less than or equal to the visible count, show the total cleanly, for example `Showing 38 of 38 words`

### Show more button

- Place the button below the word grid.
- Hide the button when:
  - there are no results
  - the total filtered result count is less than or equal to the current visible count
- Show the button only when more matching cards remain hidden.

### Copy/export behavior

- Keep copy/export based on the full filtered set, not only the visible subset.
- Reason: users expect filters to define the export set; the `Show more` control is a viewing aid, not a data restriction.

## Technical Design

### Existing state to preserve

The page already maintains:

- `allWords` as the loaded dataset
- `filtered` as the active filtered results
- `SEED` as the initial fallback data before full JSON loads

This structure should remain in place.

### New render state

Add:

- `BATCH_SIZE = 50`
- `visibleCount` initialized to `BATCH_SIZE`

### Render flow

1. Recompute `filtered` from `allWords` based on the selected filters.
2. Clamp `visibleCount` to at least `BATCH_SIZE` on reset paths and no more than `filtered.length` on render paths.
3. Render `filtered.slice(0, visibleCount)` into the word grid.
4. Update the count label to visible/total form.
5. Toggle the `Show more words` button based on whether `visibleCount < filtered.length`.

### Event handling

- Filter `change` events:
  - reset `visibleCount = BATCH_SIZE`
  - rerun render
- `Show more words` click:
  - increment `visibleCount += BATCH_SIZE`
  - clamp to `filtered.length`
  - rerun render

## Markup Changes

Add a small footer control region below the results/grid area with:

- a button element for `Show more words`
- optional wrapper for spacing/alignment consistent with the existing page

The existing grid and cards do not need structural redesign.

## Edge Cases

- Small datasets: if the filtered result count is `<= 50`, the button never appears.
- No results: keep the existing empty-state messaging and hide the button.
- Filter reductions: if a user had expanded the list and then applies a restrictive filter, the page resets to the first batch cleanly.
- Full-load transition: if the user interacts before full JSON has loaded, the page should still behave correctly when the full dataset replaces the seed data.

## Verification Plan

Manual verification should cover:

1. First load with current small dataset:
   - page still loads
   - no errors in console
   - button hidden when not needed
2. Larger dataset scenario:
   - first `50` render
   - repeated `Show more words` clicks append additional cards
   - button disappears at the end
3. Filter behavior:
   - `Type` filter resets visible list to first batch
   - `Difficulty` filter resets visible list to first batch
   - count label updates correctly
4. Export behavior:
   - copy/export still includes all filtered results, not only visible cards
5. Empty state:
   - zero matches shows empty-state text
   - `Show more words` button stays hidden

## Risks

- If rendering logic is coupled too tightly to the current total-only count display, the count update may be partially inconsistent until all render paths are updated.
- If future work expands the dataset substantially, page copy that currently references `101` curated words will also need updating to match the new source of truth.

## Decision Summary

- Use append-in-place `Show more words`
- Batch size `50`
- Reset expansion on filter change
- Keep copy/export tied to the full filtered set
- Keep the current page structure and shared loading model intact

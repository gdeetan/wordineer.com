# B-Words Page "Show More" Design

## Goal

Update the `5-letter-words-starting-with-b` page so it matches the A page's progressive disclosure behavior: render an initial batch of cards, then reveal more with a `Show more words` button.

## Scope

In scope:

- Update `template-deploy/tools-src/5-letter-words-starting-with-b.html`
- Add the same page-local batch rendering behavior used by the A page
- Preserve filtering, copy/export, and JSON loading behavior
- Rebuild and sync the generated B page

Out of scope:

- Refactoring this into shared sitewide logic
- Changing other letter pages in this task
- Altering the B dataset schema

## Recommended Approach

Copy the A-page pattern directly into the B page:

1. Render the first `50` matching cards initially
2. Add a `Show more words` button below the grid
3. Append the next `50` on each click
4. Reset the visible batch when filters change
5. Keep copy/export based on the full filtered set

## Compatibility Requirements

- The page must continue to fetch `five-letter-words-b.json`
- The count label must reflect visible versus total matching results
- The `Show more words` button must hide when all matching cards are visible

## Verification Plan

1. Confirm the B template contains the `Show more words` markup and `BATCH_SIZE = 50` logic
2. Rebuild the template output
3. Sync the built B page into `wordineer-deploy`
4. Verify both built and deployed B pages reference `five-letter-words-b.json`
5. Verify both built and deployed B pages contain the `Show more words` button logic

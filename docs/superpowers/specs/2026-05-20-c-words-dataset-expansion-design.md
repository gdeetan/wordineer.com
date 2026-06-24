# C-Words Dataset Expansion Design

## Goal

Expand `wordineer-deploy/data/five-letter-words-c.json` beyond `500` entries while preserving the existing object shape and page compatibility.

## Scope

In scope:

- Generate a larger C-only five-letter dataset from local repo sources
- Preserve the existing record shape: `w`, `t`, `d`, `diff`
- Reuse local metadata where available
- Apply approved fallback metadata for unmatched words
- Rebuild and verify the C page compatibility

Out of scope:

- Changing the page schema
- External definition enrichment in this task
- Expanding other letter datasets in this same task

## Recommended Approach

Use the same local-first relaxed pipeline used for A and B:

1. Use `wordineer-deploy/data/dictionary.json` as the broad candidate source for five-letter words starting with C.
2. Resolve metadata first from local structured sources:
   - `five-letter-words-c.json`
   - `five-letter-words.json`
   - `words_expanded.json`
3. For unmatched C-words, apply fallback metadata.
4. Normalize all retained records into the existing JSON object shape.
5. Write the expanded dataset back to disk.

## Data Sources

Primary candidate source:

- `wordineer-deploy/data/dictionary.json`

Preferred local metadata sources:

- `wordineer-deploy/data/five-letter-words-c.json`
- `wordineer-deploy/data/five-letter-words.json`
- `wordineer-deploy/data/words_expanded.json`

## Inclusion Rules

Only keep entries that satisfy all of the following:

- exactly five letters
- starts with `c` or `C`
- alphabetic only: `^[A-Za-z]{5}$`
- not a duplicate of another retained entry after lowercasing

## Metadata Rules

Preferred metadata source order:

1. existing `five-letter-words-c.json`
2. `five-letter-words.json`
3. `words_expanded.json`

Normalization rules:

- `w`: title-case for consistency with existing files
- `t`: preserve local value when available; otherwise fallback to `noun`
- `d`: preserve local definition when available; otherwise fallback to `definition unavailable`
- `diff`: preserve local difficulty when available; otherwise fallback to `hard`

## Fallback Policy

Approved fallback policy:

- For unresolved retained words, use:
  - `t`: `noun`
  - `d`: `definition unavailable`
  - `diff`: `hard`

## Output Contract

The generated file remains:

- path: `wordineer-deploy/data/five-letter-words-c.json`
- JSON array of objects
- each object includes:
  - `w`
  - `t`
  - `d`
  - `diff`

## Implementation Shape

Create or adapt a local generation script that:

1. loads all relevant local data files
2. builds the candidate C-word set
3. resolves local metadata where available
4. applies fallback metadata for unmatched words
5. sorts the final output deterministically
6. writes the expanded C dataset back to disk

## Compatibility Requirements

- The existing C page must continue to work without schema changes
- The current page behavior must continue to fetch `five-letter-words-c.json`

## Verification Plan

Verification must cover:

1. Count the final number of retained C-word entries
2. Count how many use fallback metadata
3. Validate the JSON file
4. Confirm every entry has `w`, `t`, `d`, and `diff`
5. Confirm no case-insensitive duplicates remain
6. Rebuild the template output
7. Verify the C page still references the dataset

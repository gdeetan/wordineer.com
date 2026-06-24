# A-Words Dataset Expansion Design

## Goal

Expand `wordineer-deploy/data/five-letter-words-a.json` from its current curated size to a broader `600+`-target A-only dataset, while preserving the existing object shape and avoiding obviously low-quality or malformed entries.

## Scope

In scope:

- Generate a larger A-only five-letter dataset from local repo sources
- Preserve the existing record shape: `w`, `t`, `d`, `diff`
- Keep data quality bounded by local structured metadata where possible
- Rebuild and verify page compatibility with the larger dataset

Out of scope:

- Changing the page schema or adding new record fields
- Pulling from external APIs or internet sources
- Expanding B/C or other letter datasets in this same task
- Rewriting sitewide word-data systems

## Recommended Approach

Use a local-source aggregation pipeline:

1. Use `wordineer-deploy/data/dictionary.json` as the broad candidate source for five-letter words starting with A.
2. Cross-reference candidates against `wordineer-deploy/data/words_expanded.json` to recover structured metadata.
3. Supplement from `wordineer-deploy/data/five-letter-words.json` and the current `five-letter-words-a.json`.
4. Normalize and dedupe case-insensitively.
5. Output the final A-only dataset in the existing JSON object format.

This is preferred over naive dictionary extraction because the page expects type, definition, and difficulty fields, not bare strings.

## Data Sources

Primary sources:

- `wordineer-deploy/data/dictionary.json`
- `wordineer-deploy/data/words_expanded.json`

Supplemental structured sources:

- `wordineer-deploy/data/five-letter-words.json`
- `wordineer-deploy/data/five-letter-words-a.json`

## Inclusion Rules

Only keep entries that satisfy all of the following:

- exactly five letters
- starts with `a` or `A`
- alphabetic only: `^[A-Za-z]{5}$`
- not a duplicate of another retained entry after lowercasing

## Metadata Rules

Preferred metadata source order:

1. existing `five-letter-words-a.json`
2. `five-letter-words.json`
3. `words_expanded.json`

Normalization rules:

- `w`: title-case for consistency with existing files
- `t`: preserve source value exactly where available
- `d`: preserve source definition where available
- `diff`: preserve source difficulty where available

## Fallback Policy

Approved relaxed policy:

- Prefer complete local structured metadata (`w`, `t`, `d`, `diff`) whenever available.
- For dictionary candidates with no local structured metadata match, include them with fallback values:
  - `t`: `noun`
  - `d`: `definition unavailable`
  - `diff`: `hard`
- Continue to reject malformed or non-alphabetic entries.

This policy prioritizes breadth and makes the file capable of exceeding `600` entries, at the cost of more generic metadata for unmatched words.

## Output Contract

The generated file remains:

- path: `wordineer-deploy/data/five-letter-words-a.json`
- JSON array of objects
- each object includes:
  - `w`
  - `t`
  - `d`
  - `diff`

## Implementation Shape

Create a small local generation script or one-off repo script that:

1. loads all relevant local data files
2. builds candidate A-word sets
3. resolves structured metadata using source precedence
4. filters incomplete or invalid entries
5. applies fallback metadata to unmatched valid candidates
6. sorts the final output deterministically
7. writes the expanded A dataset back to disk

## Compatibility Requirements

- The existing A page must continue to work without schema changes.
- The `Show more words` behavior already added to the page should handle the larger dataset without further architectural changes.
- Copy/export should continue to operate over the full filtered result set.

## Verification Plan

Verification must cover:

1. Count the final number of retained A-word entries.
2. Validate the JSON file.
3. Confirm every entry has `w`, `t`, `d`, and `diff`.
4. Confirm no case-insensitive duplicates remain.
5. Spot-check a sample of common and obscure entries.
6. Rebuild the template output.
7. Verify the A page still references the dataset and includes the `Show more` behavior.

## Risks

- Generic fallback metadata will reduce editorial precision for many low-frequency words.
- Existing page copy currently references `101` curated words and may become inaccurate after expansion.
- Definitions and difficulty ratings inherited from mixed local sources may vary in editorial tone.

## Decision Summary

- Target `600+` using dictionary breadth plus fallback metadata where needed
- Use `dictionary.json` for candidate breadth
- Use structured local files for metadata
- Apply fallback metadata for unmatched words:
  - `t: noun`
  - `d: definition unavailable`
  - `diff: hard`

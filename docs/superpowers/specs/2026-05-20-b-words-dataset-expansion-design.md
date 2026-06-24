# B-Words Dataset Expansion Design

## Goal

Expand `wordineer-deploy/data/five-letter-words-b.json` toward the full local candidate pool while maximizing the number of entries that have actual definitions.

## Scope

In scope:

- Generate a larger B-only five-letter dataset
- Preserve the existing record shape: `w`, `t`, `d`, `diff`
- Prefer real definitions over placeholder metadata
- Use external definition lookups for unmatched local candidates
- Rebuild and verify page compatibility with the larger dataset

Out of scope:

- Changing the page schema
- Expanding other letter datasets in this same task
- Rewriting sitewide data systems

## Recommended Approach

Use a local-first, externally enriched pipeline:

1. Use `wordineer-deploy/data/dictionary.json` as the broad candidate source for five-letter words starting with B.
2. Resolve metadata first from local structured sources:
   - `five-letter-words-b.json`
   - `five-letter-words.json`
   - `words_expanded.json`
3. For unmatched B-words, fetch definitions from an external dictionary source.
4. Normalize all retained records into the existing JSON object shape.
5. Use fallback metadata only for words that still cannot be resolved externally and are still being kept for breadth.

## Data Sources

Primary candidate source:

- `wordineer-deploy/data/dictionary.json`

Preferred local metadata sources:

- `wordineer-deploy/data/five-letter-words-b.json`
- `wordineer-deploy/data/five-letter-words.json`
- `wordineer-deploy/data/words_expanded.json`

External enrichment source:

- one dictionary API or other external dictionary source capable of returning short definitions and part-of-speech labels

## Inclusion Rules

Only keep entries that satisfy all of the following:

- exactly five letters
- starts with `b` or `B`
- alphabetic only: `^[A-Za-z]{5}$`
- not a duplicate of another retained entry after lowercasing

## Metadata Rules

Preferred metadata source order:

1. existing `five-letter-words-b.json`
2. `five-letter-words.json`
3. `words_expanded.json`
4. external dictionary source

Normalization rules:

- `w`: title-case for consistency with existing files
- `t`: preserve local value when available; otherwise use the clearest external part of speech
- `d`: preserve local definition when available; otherwise use one concise external definition
- `diff`: preserve local difficulty when available; otherwise default conservatively to `hard`

## External Lookup Policy

- Prefer one short, plain-English definition per word
- Prefer the first reliable noun, verb, adjective, or adverb sense
- If multiple senses exist, choose the clearest common-use definition
- Do not store long dictionary dumps or multi-paragraph entries

## Fallback Policy

Approved fallback policy:

- Prefer real definitions whenever possible
- For unresolved retained words, use:
  - `t`: `noun`
  - `d`: `definition unavailable`
  - `diff`: `hard`
- This fallback should be the last resort, not the primary fill strategy

## Output Contract

The generated file remains:

- path: `wordineer-deploy/data/five-letter-words-b.json`
- JSON array of objects
- each object includes:
  - `w`
  - `t`
  - `d`
  - `diff`

## Implementation Shape

Create or adapt a local generation script that:

1. loads all relevant local data files
2. builds the candidate B-word set
3. resolves local metadata where available
4. performs external lookups for unmatched words
5. applies minimal fallback metadata where external lookup fails
6. sorts the final output deterministically
7. writes the expanded B dataset back to disk

## Compatibility Requirements

- The existing B page must continue to work without schema changes
- The current `Show more words` page pattern should still support the larger dataset
- Copy/export behavior should remain unchanged

## Verification Plan

Verification must cover:

1. Count the final number of retained B-word entries
2. Count how many have real definitions versus fallback definitions
3. Validate the JSON file
4. Confirm every entry has `w`, `t`, `d`, and `diff`
5. Confirm no case-insensitive duplicates remain
6. Rebuild the template output
7. Verify the B page still references the dataset and includes the current interaction pattern

## Risks

- External lookups may fail for some obscure dictionary candidates
- External definitions may vary in editorial tone from the local dataset
- The final count depends on external source coverage and network availability
- Existing page copy may become inaccurate if it still references the smaller curated dataset

## Decision Summary

- Target the broad B-candidate pool from local dictionary data
- Preserve local metadata first
- Use external definitions to maximize real-definition coverage
- Use fallback metadata only as a last resort

# 5 Letter Words Starting With O Design

## Goal

Add a new `5-letter-words-starting-with-o` page that matches the existing `5-letter-words-starting-with-*` series in layout, breadcrumb, filtering behavior, and copy structure while providing `125` curated entries with definitions.

## References

- `template-deploy/tools-src/5-letter-words-starting-with-e.html`
- `template-deploy/tools-src/5-letter-words-starting-with-f.html`
- `template-deploy/tools-src/5-letter-words-starting-with-g.html`
- `template-deploy/tools-src/5-letter-words-starting-with-n.html`

## Approach

Reuse the current letter-page structure unchanged: breadcrumb, hero, filter bar, results controls, lazy-loaded word grid, A-Z navigation, prose sections, and FAQ block. Replace only the letter-specific metadata, structured data, examples, seed entries, fetch target, and article copy so the `O` page stays visually and behaviorally consistent with the rest of the series.

## Content Plan

- Create `template-deploy/tools-src/5-letter-words-starting-with-o.html`.
- Create `wordineer-deploy/data/five-letter-words-o.json` with `125` curated entries using the existing `{ w, t, d, diff }` shape.
- Keep the page copy above `120` words and tailor the prose to `O` patterns for Wordle, Scrabble, vocabulary building, and the FAQ.
- Use `O` examples with and without repeated letters so the FAQ and prose stay consistent with the final dataset.

## Verification

- Validate the JSON file with `python3 -m json.tool`.
- Run `cd template-deploy && python3 build.py`.
- Confirm the generated output includes the `Starting With O` breadcrumb, `5 Letter Words Starting With O` heading, and `/data/five-letter-words-o.json` fetch path.

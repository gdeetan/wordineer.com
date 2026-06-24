# 5 Letter Words Starting With N Design

## Goal

Add a new `5-letter-words-starting-with-n` page that matches the existing `5-letter-words-starting-with-*` series in layout, breadcrumb, filtering behavior, and copy structure while expanding the content to `125` curated entries with definitions.

## References

- `template-deploy/tools-src/5-letter-words-starting-with-e.html`
- `template-deploy/tools-src/5-letter-words-starting-with-f.html`
- `template-deploy/tools-src/5-letter-words-starting-with-g.html`
- `template-deploy/tools-src/5-letter-words-starting-with-m.html`

## Approach

Use the current letter-page template shape unchanged: breadcrumb, hero, filter bar, results controls, lazy-loaded word grid, A-Z navigation, prose sections, and FAQ block. Replace only the letter-specific metadata, examples, structured data, seed words, fetch target, and article copy so the `N` page remains visually and behaviorally consistent with the rest of the series.

## Content Plan

- Create `template-deploy/tools-src/5-letter-words-starting-with-n.html`.
- Create `wordineer-deploy/data/five-letter-words-n.json` with `125` curated entries using the existing `{ w, t, d, diff }` shape.
- Keep the page copy above `120` words and tailor the prose to `N` patterns for Wordle, Scrabble, vocabulary building, and the FAQ.
- Use `N` examples with and without repeated letters so the FAQ and prose stay internally consistent with the data file.

## Verification

- Validate the JSON file with `python3 -m json.tool`.
- Run `cd template-deploy && python3 build.py`.
- Confirm the generated output includes the `Starting With N` breadcrumb, `5 Letter Words Starting With N` heading, and `/data/five-letter-words-n.json` fetch path.

# Names Data Source Notes

`names.json` is a curated static dataset for the random name generator. Keep entries compact and manually reviewed before adding them to the public file.

`american-names-core.json` and `american-names-full.json` power the Random American name generator. The core file is a small first-load dataset. The full file expands variety to 1,500 total entries and is loaded after user interaction. `american-names.json` is kept as a compact compatibility copy of the core dataset.

Preferred source types:

- Behind the Name for given-name usage, gender, surname language, and etymology checks. Downloads are CC BY-SA 4.0 and require attribution if used directly.
- U.S. Census names data for frequency and demographic signals, not name meanings.
- Government baby-name datasets such as SSA, ONS, and National Records of Scotland for popularity trends, not etymology.
- Wikidata only as a secondary cross-check because records can be uneven.

American name generator sources:

- First and middle names are selected from SSA baby-name popularity data. Direct SSA edge downloads were unavailable during generation, so the working input was a public mirror of the SSA national max-occurrence data; labels are generic popularity/style labels, not copied meanings.
- Surnames are selected from the official U.S. Census 2010 surname API using ranks 1-600. Background filters use broad Census demographic signals plus conservative common-origin heuristics.

Do not bulk-copy names or meanings from commercial baby-name pages. Keep meanings short, avoid uncertain etymologies, and prefer broad origin labels only when a name is genuinely used across multiple related cultures.

# Random British Name Generator - Design Spec
Date: 2026-05-08

## Context
Build a dedicated `random-british-name-generator.html` page as part of the country-specific name generator cluster supporting the pillar page `random-name-generator.html`.

The page should reuse the existing Wordineer name generator UX:
- Count input first.
- Mobile "More options" toggle under the count field.
- Auto-regenerate when a filter changes.
- Generate, reset, copy, and save interactions consistent with the existing name pages.

Primary users:
- Writers naming British characters.
- Game masters, roleplayers, and worldbuilders.
- Teachers, students, and creators who need quick UK-style names.
- Users comparing country-specific name tools from the broader random name generator cluster.

The tool should feel more useful than generic English name generators by focusing on UK naming patterns, regional influence, double-barrelled surnames, eras, and short result notes.

Primary target page:
- URL: `/random-british-name-generator/`
- Output file: `wordineer-deploy/random-british-name-generator.html`
- Source file: `template-deploy/tools-src/random-british-name-generator.html`
- Dedicated data file: `wordineer-deploy/data/british-names.json`

---

## 1. High-CTR SEO Direction

### Recommended title tag
`Random British Name Generator - 2500+ UK Names`

Reason:
- Keeps the exact primary keyword at the front.
- Adds a concrete CTR hook with `2500+ UK Names`.
- Stays concise enough for search results.

### Alternate title tags
- `Random British Name Generator - 2500+ British Names`
- `British Name Generator: 2500+ First & Last Names`
- `Random British Names - 2500+ UK Name Ideas`

### H1
`Random British Name Generator`

### Hero intro
`Generate random British names from 2500+ UK-style first names, surnames, middle names, and double-barrelled combinations. Filter by gender, name type, style, era, region influence, surname type, and starting letter.`

### Meta description
`Generate random British names from 2500+ UK name options. Filter by gender, style, era, region influence, surname type, and name format. Free, fast, no sign-up.`

### Target keywords
Primary:
- random british name generator
- british name generator
- random british names
- british names
- UK name generator
- random UK name generator

Cluster/internal-link keywords:
- random name generator
- random american name generator
- random filipino name generator
- random japanese name generator
- random russian name generator
- random indian name generator

---

## 2. Competitor Takeaways

Checked references:
- `fantasynamegenerators.com/british-english-names.php`
- `reedsy.com/resources/character-name-generator/language/english/`
- `fakenamegenerator.com/gen-random-en-uk.php`
- `randomname.uk`
- `perchance.org/1700s-1800s-british-names`

### Worth using
- Gender filter.
- Quantity control.
- First name, last name, and full name output.
- Middle-name support.
- Double-barrelled surname support.
- Era/style controls for writers.
- Short name notes or meaning-style context.
- Clean educational text about how British names differ from generic English names.

### Not worth using in v1
- Fake identity data: address, phone, birthday, NINO, email, finance, employment, passwords, tracking numbers.
- Login-gated saved identities.
- XML/JSON/CSV output modes.
- Massive country/name-set dropdowns inside this page.
- Overly detailed genealogy claims.
- Too many historical sub-periods at launch.

### Positioning
This is a British name generator, not a fake identity generator. It should produce fictional name combinations that feel plausible for UK settings, with enough filters to help users choose a tone without making the interface heavy.

---

## 3. Data File

### Path
`wordineer-deploy/data/british-names.json`

### Target size
Use about `2500` tagged entries for launch.

Recommended split:
- `900-1100` first names.
- `250-400` middle-name-friendly entries. These can overlap with first names if the build process or data shape allows reuse.
- `900-1100` surnames.
- `100-200` surname particles, double-barrel parts, or curated double-barrel combinations.

Performance target:
- Ideal raw JSON: under `500KB`.
- Acceptable raw JSON: up to `1MB`.
- Avoid over `1MB` unless split or compressed later.

This is manageable for the current static site. Existing reference files include `japanese-names.json` at about `573KB` with `2934` items, so a British dataset with about `2500` entries should be safe.

### Recommended schema
Use compact arrays if file size matters, but keep enough metadata for filters and notes.

```json
{
  "first": [
    ["Eleanor", "f", ["classic", "literary"], ["victorian", "timeless"], ["english"], "Classic English first name"],
    ["Rhys", "m", ["classic"], ["timeless", "modern"], ["welsh"], "Welsh first-name influence"],
    ["Morgan", "u", ["modern", "literary"], ["modern", "timeless"], ["welsh"], "Neutral Welsh-influenced first name"]
  ],
  "middle": [
    ["Rose", "f", ["classic", "middle-friendly"], ["timeless"], ["english"], "Traditional British middle name"],
    ["James", "m", ["classic", "middle-friendly"], ["timeless"], ["english", "scottish"], "Common British middle name"]
  ],
  "last": [
    ["Whitmore", ["classic", "aristocratic"], ["english"], ["place-based"], "English place-style surname"],
    ["MacLeod", ["classic"], ["scottish"], ["patronymic"], "Scottish surname influence"],
    ["Pritchard", ["classic"], ["welsh"], ["patronymic"], "Welsh surname influence"]
  ],
  "doubleLastParts": [
    ["Montgomery", ["aristocratic"], ["scottish", "english"], "Classic double-barrel surname part"],
    ["Jones", ["common"], ["welsh", "english"], "Common UK surname part"]
  ]
}
```

First and middle fields:
`[name, gender, styles, eras, regions, note]`

Last name fields:
`[name, styles, regions, types, note]`

Double-barrel part fields:
`[name, styles, regions, note]`

### Gender values
- `m`
- `f`
- `u`

### Style values
- `common`
- `classic`
- `modern`
- `old-fashioned`
- `aristocratic`
- `literary`
- `unisex`

### Era values
- `any`
- `modern`
- `1990s-2000s`
- `mid-century`
- `victorian-edwardian`
- `timeless`

### Region values
- `english`
- `scottish`
- `welsh`
- `northern-irish`

Use these as region influence tags, not strict ethnicity or ancestry claims.

### Surname type values
- `common-uk`
- `occupational`
- `place-based`
- `patronymic`
- `aristocratic`
- `double-barrelled`

### Notes
Notes should be short, plain, and useful.

Examples:
- `Classic English style`
- `Modern British style`
- `Scottish surname influence`
- `Welsh first-name influence`
- `Northern Irish surname influence`
- `Double-barrelled surname`
- `Aristocratic feel`
- `Old-fashioned British style`
- `Common UK surname`
- `Neutral first name`

Do not hand-write long unique notes for all 2500 entries. Store short base notes in data, then let the generator combine result notes from selected tags.

---

## 4. Tool Page

### Source path
`template-deploy/tools-src/random-british-name-generator.html`

### Output path
`wordineer-deploy/random-british-name-generator.html`

### Clean URL
`/random-british-name-generator/`

### Core controls
Always visible:
- Count: numeric input, default `10`, min `1`, max `50`.

Behind the existing mobile "More options" panel:
- Gender:
  - `Any`
  - `Female`
  - `Male`
  - `Neutral`
- Name type:
  - `Full name`
  - `First name`
  - `Last name`
  - `First + middle + last`
  - `Double-barrelled full name`
- Style:
  - `Any style`
  - `Common`
  - `Classic`
  - `Modern`
  - `Old-fashioned`
  - `Aristocratic`
  - `Literary`
  - `Unisex`
- Region influence:
  - `Any influence`
  - `English`
  - `Scottish`
  - `Welsh`
  - `Northern Irish`
- Era:
  - `Any era`
  - `Modern`
  - `1990s-2000s`
  - `Mid-century`
  - `Victorian / Edwardian`
  - `Timeless`
- Surname type:
  - `Any surname`
  - `Common UK`
  - `Occupational`
  - `Place-based`
  - `Patronymic`
  - `Aristocratic`
  - `Double-barrelled`
- Starts with:
  - `Any letter`
  - `A-Z`

### Auto-generation behavior
When the user changes any filter, the output updates automatically.

Examples:
- Changing gender from `Male` to `Female` immediately lists female names.
- Changing region influence from `Any` to `Welsh` immediately favors Welsh-tagged first names or surnames.
- Changing surname type to `Double-barrelled` immediately generates names like `Amelia Clarke-Hughes`.

### Filter priority
When several filters are selected:
1. Filter first and middle names by gender.
2. Filter first and middle names by style.
3. Filter first and middle names by era.
4. Filter first names by starts-with.
5. Filter first and last names by region influence.
6. Filter last names by surname type.
7. If a filter leaves too few results, broaden the least important filter first.

Fallback order:
1. Keep gender.
2. Keep starts-with if selected.
3. Keep region influence if possible.
4. Drop style.
5. Drop era.
6. Drop surname type.

If no viable result exists, show a short reset suggestion instead of a scary error.

### Result card
Each result should show:
- Main generated name.
- Short note line.
- Copy/save actions consistent with existing name pages.

Examples:
```text
Eleanor Whitmore
Classic English style · common UK surname
```

```text
Rhys Montgomery-Jones
Welsh first-name influence · double-barrelled surname
```

```text
Harriet Sinclair
Victorian / literary feel · Scottish surname influence
```

Optional chips can be added if the existing page pattern already supports them:
- `female`
- `classic`
- `welsh`
- `double-barrelled`

---

## 5. Explainer and SEO Copy

### What is a random British name generator?
`A random British name generator creates first names, last names, and full names inspired by naming patterns from the United Kingdom. Instead of using one generic random name generator for every culture, this tool focuses on British-style names, including common UK surnames, classic given names, modern names, regional influences, and double-barrelled surnames.`

### How it works
`Choose how many names you want, then adjust the filters. You can generate male, female, or neutral names, switch between first names and full names, choose a style or era, and narrow the region influence or surname type. When you change a filter, the list updates automatically so you can compare name ideas quickly.`

### Why use country-specific name generators?
`Names are shaped by culture, language, history, and local naming habits. A random Filipino name generator, random Japanese name generator, and random British name generator should not all use the same filter structure because each country has different naming patterns. Country-specific tools give better results because the filters, name data, and combinations are built around the culture where each name fits.`

### British vs general random name generator
`Use the main random name generator when you want broad name ideas across many origins. Use this random British name generator when you want UK-style names with British first names, surnames, regional influence, and era controls. A focused country page gives more natural results than forcing every culture into one shared filter system.`

### Suggested FAQ
- `Are these real British names?`
  - `The tool uses real British-style first names and surnames, then combines them randomly for fictional use.`
- `Can I generate Scottish, Welsh, or Northern Irish names?`
  - `Yes. Use the Region influence filter to favor English, Scottish, Welsh, or Northern Irish name styles.`
- `Can I make double-barrelled British names?`
  - `Yes. Choose the double-barrelled full name option or select double-barrelled under surname type.`
- `Can I use these names for characters?`
  - `Yes. The tool is designed for character names, stories, games, roleplaying, and creative projects.`
- `Why is this different from the main random name generator?`
  - `The main random name generator covers many origins. This page uses British-specific filters and data, so the results can better match UK naming patterns.`

---

## 6. More Tools Section

For name-generator pages, change the section subtitle from:
`Every word generator you need, all free`

To:
`Every name generator you need, all free`

Recommended list:
- Random Name
- Random American Name
- Random Japanese Name
- Random British Name
- Random Russian Name
- Random Indian Name

Keep the broader "Other tools" section below if it already appears in the shared template.

---

## 7. Implementation Notes

### Template/source files
Make edits in `template-deploy/tools-src/` and shared fragments where possible, then regenerate with:
```bash
cd template-deploy
python3 build.py
```

Review generated output before copying or deploying.

### JavaScript
Reuse existing generator behavior where practical:
- Mobile more-options toggle.
- Count validation.
- Auto-generation on `change` and relevant `input` events.
- Copy/save controls.

If the shared `tool-engine.js` cannot cleanly support British-specific tags, add a British-specific initializer while preserving existing page behavior.

### Data handling
Load `data/british-names.json` over HTTP. Do not rely on opening HTML files directly because fetch paths require a local server.

### Testing
Manual test through:
```bash
cd wordineer-deploy
python3 -m http.server 8080
```

Check:
- Page loads with no console errors.
- `2500+ UK Names` appears in the title/meta direction and visible intro where appropriate.
- Count min/max validation works.
- Mobile `More options` expands below the count field.
- Changing filters auto-regenerates results.
- Gender changes update output immediately.
- Region influence affects notes and generated combinations.
- Double-barrelled surname mode works.
- Copy/save actions still work.
- Responsive layout is clean on mobile and desktop.

---

## 8. Open Decisions

Resolved:
- Include English, Scottish, Welsh, and Northern Irish region influence.
- Show short notes under each generated name.
- Use a dedicated JSON file.
- Target around 2500 names.
- Use a high-CTR title hook like `2500+ UK Names`.

Not included in v1:
- Fake identity profile data.
- Export formats.
- Account/login features.
- Audio pronunciation.
- Deep genealogy or surname-origin claims.

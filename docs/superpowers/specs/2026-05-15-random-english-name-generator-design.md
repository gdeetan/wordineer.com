# Random English Name Generator - Design Spec
Date: 2026-05-15

## Context
Build a dedicated `random-english-name-generator.html` page for the Wordineer name-generator cluster. This page should sit beside the existing British and American generators, but stay focused on names that feel specifically English rather than broadly UK-wide.

The page should reuse the established Wordineer generator pattern:
- Count input first.
- Mobile `More options` toggle directly below the count field.
- Filters update the output automatically when changed.
- Generate, reset, copy, and save interactions should match the existing name pages.

Primary users:
- Writers and editors naming English characters.
- Game masters and worldbuilders.
- Baby-name browsers looking for England-specific names.
- Users who want something narrower than the British page but broader than a single surname or baby-name list.

The page should beat the top results by being cleaner than Fantasy Name Generators, more focused than Reedsy, and more practical than a plain list page.

Primary target page:
- URL: `/random-english-name-generator/`
- Output file: `wordineer-deploy/random-english-name-generator.html`
- Source file: `template-deploy/tools-src/random-english-name-generator.html`
- Dedicated data file: `wordineer-deploy/data/english-names.json`

---

## 1. SEO Direction

### Recommended title tag
`1100+ Random English Names - Realistic First, Last & Full Names | Wordineer`

Reason:
- Keeps the main keyword near the front.
- Adds a CTR hook with `1100+`.
- Signals that the page supports more than one result type.

### Alternate title tags
- `1100+ Random English Names - Free Name Ideas | Wordineer`
- `Random English Name Generator - 1100+ Realistic Names`
- `1100+ English Names for Characters, Stories, and Baby Name Ideas`

### H1
`1100+ Random English Names`

### Hero intro
`Generate 1100+ random English names instantly. Filter by gender, name type, style, era, and starting letter. Great for characters, stories, baby names, pen names, and worldbuilding.`

### Meta description
`Generate 1100+ random English names instantly. Filter by gender, style, era, name type, and starting letter. First names are the default. Free, fast, and no sign-up.`

### Target keywords
Primary:
- random english name generator
- english name generator
- random english names
- english names
- english first names

Secondary:
- name generator for characters
- baby name ideas
- pen name ideas
- realistic english names

---

## 2. Product Positioning

This page should be clearly different from the British generator.

### English page means
- England-focused naming patterns.
- English surnames, English first names, and English-style combinations.
- English cultural feel without trying to represent all UK naming traditions.

### British page means
- Broader UK coverage across England, Scotland, Wales, and Northern Ireland.

### Why a separate page is the right path
- Better search intent match.
- Less internal cannibalization.
- Clearer user expectations.
- Easier to give each page a distinct filter set and dataset.

### Do not do
- Do not make this a duplicate of the British page with a smaller dataset.
- Do not turn it into a fake identity generator.
- Do not add broad international name pools here.

---

## 3. Competitor Takeaways

Checked references:
- `reedsy.com/resources/character-name-generator/language/english/`
- `fantasynamegenerators.com/english-names.php`
- `behindthename.com/random/`
- `byrdnash.com/english-town-name-generator/`
- `namegeneratorfun.com/english`

### Worth using
- Gender filter.
- Quantity control.
- Name type selector.
- Short explanatory copy about how English names work.
- Result notes or meaning hints under names.
- A clean mobile `More options` panel.
- Instant refresh when filters change.

### Not worth copying
- User-entered personalization fields.
- Life-story generation.
- Fake identity details.
- Huge taxonomy menus on the tool itself.
- Excessively academic etymology blocks in the generator UI.

### Competitive advantage to aim for
- Cleaner UI than Fantasy Name Generators.
- Stronger utility than NameGeneratorFun.
- Better focused than Reedsy.
- Less overwhelming than Behind the Name.

---

## 4. Data Plan

### Path
`wordineer-deploy/data/english-names.json`

### Recommended dataset size
Use enough data to honestly support the `1100+` claim in the title.

Recommended launch target:
- `900` first names
- `150` middle-friendly names
- `250` surnames

Total: `1300+` entries.

That gives the page enough depth to feel full while keeping the first-name pool as the main focus.

### Why not 900 total only
If the page only had 900 total names, `1100+` would be misleading. The title should match the actual inventory.

### Suggested schema
Use compact arrays so the file stays easy to load and filter:

```json
{
  "first": [
    ["James", "m", ["classic", "common"], ["timeless", "modern"], ["english"], "Classic English first name"],
    ["Hazel", "f", ["classic", "vintage"], ["timeless"], ["english"], "Soft vintage English first name"],
    ["Taylor", "u", ["modern", "unisex"], ["modern"], ["english"], "Neutral modern English-style first name"]
  ],
  "middle": [
    ["Rose", "f", ["classic"], ["timeless"], ["english"], "Traditional middle name"],
    ["Anne", "f", ["classic"], ["timeless"], ["english"], "Common English middle name"]
  ],
  "last": [
    ["Smith", ["common", "occupational"], ["english"], "Common English surname"],
    ["Blackwood", ["place-based", "literary"], ["english"], "English surname with a literary feel"]
  ]
}
```

### Field meanings
First and middle:
- `[name, gender, styles, eras, regions, note]`

Last:
- `[name, styles, regions, note]`

### Suggested filter tags
Gender:
- `m`
- `f`
- `u`

Styles:
- `common`
- `classic`
- `modern`
- `old-fashioned`
- `timeless`
- `literary`
- `elegant`
- `biblical`

Eras:
- `timeless`
- `modern`
- `vintage`
- `victorian`
- `edwardian`
- `mid-century`

Surname types:
- `common`
- `occupational`
- `place-based`
- `patronymic`
- `aristocratic`

Region tags:
- `english`

Keep region tagging simple on this page. The point is not to mimic the British generator's broader UK regional model.

---

## 5. Tool Page

### Source path
`template-deploy/tools-src/random-english-name-generator.html`

### Output path
`wordineer-deploy/random-english-name-generator.html`

### Core controls
Always visible:
- Count input.

Behind the mobile `More options` panel:
- Name type:
  - `First name`
  - `Full name`
  - `Last name`
  - `First + middle + last`
- Gender:
  - `Any`
  - `Female`
  - `Male`
  - `Neutral`
- Style:
  - `Any`
  - `Common`
  - `Classic`
  - `Modern`
  - `Old-fashioned`
  - `Timeless`
  - `Literary`
  - `Biblical`
- Era:
  - `Any`
  - `Modern`
  - `Vintage`
  - `Victorian`
  - `Edwardian`
  - `Mid-century`
- Starts with:
  - `Any letter`
  - A-Z
- Show meanings toggle.

### Default values
- Count: `10`
- Name type: `First name`
- Gender: `Any`
- Style: `Any`
- Era: `Any`
- Starts with: `Any letter`
- Show meanings: `on`

### Required behavior
- Changing any filter should regenerate the visible results automatically.
- Mobile should show only the count and primary action first.
- The `More options` button should reveal the remaining filters without crowding the screen.
- The first-name option should be selected by default when the page loads.
- Reset should restore the defaults above.

### Result behavior
Each result card should show:
- The generated name.
- Optional meaning or note line.
- Optional chips for gender, style, or era when helpful.

Actions:
- Copy one result.
- Copy all results.
- Save favorites.
- Copy saved names.

### Fallback behavior
- If filters are too narrow, broaden gracefully within the same category before showing an empty state.
- If there are still no matches, show a short message and suggest relaxing style, era, or starting-letter filters.

---

## 6. Suggested Page Copy

### Section: What is a random English name generator?
Use a short explanation that tells users the tool produces English-feeling names from a curated dataset. It should mention that English names often blend Anglo-Saxon, Norman, Biblical, Latin, and literary influences.

### Section: How it works
Explain the simple flow:
- Choose a number of names.
- Pick a name type.
- Narrow by gender, style, era, or starting letter.
- The list updates automatically as the user changes filters.

### Section: English vs British names
Explain that English names are England-focused, while British names cover the wider UK.

### Section: Who this is for
Mention writers, game masters, baby-name browsers, and people choosing pen names or character names.

### Section: FAQ
Suggested questions:
- What makes this different from the British name generator?
- Can I use these names in stories?
- Why is first name the default?
- How many names does this page have?
- Is this free?

---

## 7. Implementation Notes

### Page structure
Reuse the same layout pattern used by the current generator pages:
- Hero section.
- Tool card.
- Results panel.
- Saved names section.
- Educational content blocks.
- Related tools footer.

### Script behavior
Prefer a dedicated page script or a small page-specific branch in the shared generator engine rather than duplicating large inline logic.

The English page should support:
- Data loading from the dedicated JSON file.
- Filtering by name type, gender, style, era, and starting letter.
- Auto-refresh on control changes.
- Copy/save interactions.

### Title and description updates
The new page needs distinct metadata so it can rank separately from the British page:
- Title should emphasize `1100+`.
- Description should mention that first names are the default.
- OG title and description should match the SEO angle.

---

## 8. Non-Goals

Do not include:
- Fake identity generation.
- Address, email, phone, or password fields.
- Huge in-page taxonomies.
- Country-wide UK regional coverage.
- Pronunciation audio.
- Deep etymology explorer mode.

---

## 9. Acceptance Criteria

The page is ready when:
- The page exists at `/random-english-name-generator/`.
- `First name` is the default name type.
- The dataset contains `1300+` total entries with `900` first names.
- The title and H1 use the `1100+` framing.
- Filters update results automatically.
- The mobile `More options` toggle works.
- The page has explanatory copy for `What is a random English name generator?` and `How it works`.
- The new page is clearly differentiated from the British page.


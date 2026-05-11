# Random Scottish Name Generator - Design Spec
Date: 2026-05-11

## Context
Build a dedicated `random-scottish-name-generator.html` page as part of the country-specific name generator cluster supporting the pillar page `random-name-generator.html`.

The page should reuse the existing Wordineer name generator UX:
- Count input first.
- Mobile `More options` toggle under the count field.
- Auto-regenerate when a filter changes.
- Generate, reset, copy, and save interactions consistent with the stronger existing name pages.

Primary users:
- Writers naming Scottish characters.
- Game masters, roleplayers, and worldbuilders.
- Users looking for Scottish first names or surnames for stories, games, and creative projects.
- Casual visitors who want name inspiration without researching Scottish naming traditions manually.

The tool should feel more useful than generic Scottish generators by combining practical filters, cleaner mobile UX, short meaning notes, and a balanced mix of modern and traditional Scottish naming styles.

Primary target page:
- URL: `/random-scottish-name-generator/`
- Output file: `wordineer-deploy/random-scottish-name-generator.html`
- Source file: `template-deploy/tools-src/random-scottish-name-generator.html`
- Dedicated data file: `wordineer-deploy/data/scottish-names.json`

---

## 1. Product Direction

### Recommended dataset direction
Use a balanced mix weighted toward real modern Scottish names.

Target mix:
- `70%` real modern Scottish names.
- `30%` traditional Gaelic or older Scottish forms.

Reason:
- This serves the widest audience.
- It keeps the tool useful for both practical naming and fiction use.
- It avoids the page feeling either too generic or too fantasy-coded.
- It creates meaningful style filters without relying on invented Scottish-sounding names.

### Default generation direction
Set `Name type` to `Given name only` by default.

Reason:
- This matches the most common user intent.
- It makes gender, style, theme, and starting-letter filters more immediately useful.
- It keeps the tool distinct from simpler generators that default to broad full-name output.

### Positioning line
`A Scottish name generator with modern, traditional Gaelic, and anglicized name options.`

---

## 2. Competitor Takeaways

Checked references:
- `fantasynamegenerators.com/modern-scottish-names.php`
- `perchance.org/namegen-eu-scot`
- `reedsy.com/resources/character-name-generator/medieval/old-celtic/`
- `thestoryshack.com/tools/scottish-name-generator/`
- `namechef.co/name-generator/scottish/`
- `namenerds.com/scottish/generator.html`

### Worth using
- Simple quantity control.
- Fast random output.
- Gender filter.
- Given name, surname, and full-name output modes.
- Copy or save interactions.
- Educational text explaining what kind of Scottish names the tool includes.
- Practical filters like style, popularity, and starting letter.

### Not worth using in v1
- `Ends with` and `contains` search fields.
- Exact syllable filters.
- Social-class filters.
- Clan filters unless supported by strong and defensible data.
- Historical-period filters unless the dataset is deep enough to support them cleanly.
- Fake identity or profile-generation features.

### Positioning
This should be a Scottish name generator, not a fake identity tool and not a fantasy-only name generator. The page should produce plausible Scottish-style results from real or historically associated names, with enough filtering to help users choose the tone they want.

---

## 3. V1 Filter Set

Lock the following filters for v1:
- `Number of names`
- `Name type`
- `Gender`
- `Style`
- `Meaning theme`
- `Starts with`
- `Popularity`
- `Show meanings`

### Name type options
Order:
1. `Given name only`
2. `Full name`
3. `Surname only`

Default:
- `Given name only`

### Gender options
- `Any`
- `Male`
- `Female`
- `Unisex`

### Style options
- `Any`
- `Modern`
- `Traditional Gaelic`
- `Anglicized`
- `Classic`

### Meaning theme options
- `Any`
- `Nature`
- `Strength`
- `Sea`
- `Light`
- `Warrior`
- `Saintly`
- `Noble`
- `Joy`

### Popularity options
- `Any`
- `Common`
- `Familiar`
- `Rare`

### Show meanings
- Toggle control
- Default `On`

Reason for this set:
- Strong enough to outperform thin generators.
- Small enough to keep the UI readable and the data tagging manageable.
- Aligned with the current Wordineer country-name-generator pattern.

---

## 4. Filter Behavior and Defaults

### Layout behavior
- `Number of names` stays at the top.
- On mobile, `More options` appears directly below the count field.
- On desktop, advanced filters remain visible.
- On mobile, advanced filters are hidden until expanded.

### Auto-refresh behavior
- Changing any filter should regenerate results automatically.
- This includes `Name type`, `Gender`, `Style`, `Meaning theme`, `Starts with`, and `Popularity`.
- If the count input is valid, changing the count should also refresh results.

### Default values
- `Number of names`: `10`
- `Name type`: `Given name only`
- `Gender`: `Any`
- `Style`: `Any`
- `Meaning theme`: `Any`
- `Starts with`: `Any`
- `Popularity`: `Any`
- `Show meanings`: `On`

### Interaction expectations
- The page should preserve the same control rhythm used by the stronger existing name-generator pages.
- Mobile filtering should stay compact and predictable.
- The copy typography in the explainer, FAQ, and supporting sections should remain uniform with the other name-generator tool pages. Do not introduce a different copy font treatment for this page.

---

## 5. Data File

### Path
`wordineer-deploy/data/scottish-names.json`

### Top-level structure
```json
{
  "given": [],
  "surnames": []
}
```

### Recommended given-name schema
```json
{
  "name": "Eilidh",
  "gender": "f",
  "styles": ["traditional-gaelic", "classic"],
  "themes": ["light", "joy"],
  "meaning": "A common Scottish Gaelic name often linked to brightness or radiance.",
  "popularity": "familiar",
  "originLabel": "Gaelic"
}
```

Fields:
- `name`
- `gender`: `m`, `f`, `u`
- `styles`
- `themes`
- `meaning`
- `popularity`: `common`, `familiar`, `rare`
- `originLabel`: `Gaelic`, `Scots`, `Anglicized`, `Scottish`
- `pronunciation`: optional for future use, not required in v1

### Recommended surname schema
```json
{
  "name": "MacLeod",
  "styles": ["traditional-gaelic", "classic"],
  "themes": ["warrior", "noble"],
  "meaning": "From a historic Scottish clan surname meaning son of Leod.",
  "popularity": "familiar",
  "originLabel": "Gaelic"
}
```

Fields:
- `name`
- `styles`
- `themes`
- `meaning`
- `popularity`
- `originLabel`

### Data guidance
- Use a dedicated Scottish dataset rather than the generic random-name dataset.
- Keep the dataset grounded in real Scottish-associated names.
- Avoid made-up Scottish-sounding filler names.
- Tag names conservatively. If a theme or style is uncertain, omit it rather than over-tagging.
- Meanings should be short, plain-English helper notes rather than long etymology entries.

### Suggested launch scale
Recommended minimum:
- `300-500` given names.
- `200-350` surnames.

This is enough to make the filters meaningful without making curation unmanageable for the first release.

---

## 6. Result Format and Generation Rules

### Output modes
- `Given name only`: show a filtered given name.
- `Surname only`: show a filtered surname.
- `Full name`: combine one filtered given name and one filtered surname.

### Result display
- Show the generated name as the primary line.
- If `Show meanings` is on, show a short meaning note underneath.
- Keep copy and save actions for parity with the better generator UX.

### Generation rules
- Avoid duplicates within the same generated batch where possible.
- For `Full name`, combine from the current filtered given-name and surname pools.
- If `Starts with` is set:
  - apply it to the visible given name for `Given name only`
  - apply it to the visible surname for `Surname only`
  - apply it to the first visible part of the displayed result for `Full name`

### Empty state
Use a helpful empty-state message:

`No matching Scottish names found. Try a broader style, theme, gender, or starting letter.`

---

## 7. Tool Page Structure

### Source path
`template-deploy/tools-src/random-scottish-name-generator.html`

### Page structure
- Hero with H1 and short intro.
- Generator card with controls and results.
- Saved names section if consistent with the current pattern.
- Explainer section.
- FAQ section.
- `Who uses Wordineer` section.
- Related internal links to other name generators.

### Required UX alignment
- Match the mobile `More options` pattern already used on the stronger country-specific pages.
- Match the current copy font styling and text rhythm used on the other name-generator tool pages.
- Follow existing spacing, label, and helper-text patterns rather than introducing a new typography system.

---

## 8. Explainer and Supporting Copy

### Required explainer sections
1. `What Is a Random Scottish Name Generator?`
2. `How It Works`
3. `Scottish Names: Modern, Gaelic, and Anglicized Forms`
4. `More Random Name Generators`

### Draft direction for `What Is a Random Scottish Name Generator?`
Explain that the tool creates Scottish-style given names, surnames, or full names from a curated dataset of real and historically associated options. Position it for writers, roleplayers, game developers, and general name inspiration.

### Draft direction for `How It Works`
Explain that the user chooses a quantity, then adjusts filters like name type, gender, style, meaning theme, and starting letter. Note that results refresh automatically and mobile users can tap `More options` to reveal advanced filters.

### Draft direction for `Scottish Names: Modern, Gaelic, and Anglicized Forms`
Explain that Scottish names come from a mix of naming traditions, including Scottish Gaelic, Scots, and anglicized forms. Clarify that some names feel strongly Gaelic while others are more familiar in modern English-speaking use.

### Supporting note
Keep the copy style uniform with the other country-specific name-generator pages. Use the same font treatment and a similar tone and sentence density.

---

## 9. FAQ Topics

Include at least these FAQ questions:
- `Are these real Scottish names?`
- `Can I use these names for characters, stories, or games?`
- `Why do some Scottish names look more Gaelic and others more familiar?`
- `What does anglicized mean in Scottish names?`
- `Is this random Scottish name generator free?`

Answering principles:
- Be concise.
- Be practical.
- Avoid overstating historical certainty.

---

## 10. Who Uses This Page

Recommended audience blocks:
- `Writers`
- `Game Masters`
- `Game Developers`
- `Name Researchers`

Purpose:
- Reinforce use cases.
- Match the stronger existing generator pattern.
- Improve page trust and scannability.

---

## 11. Testing Expectations

Manual verification should cover:
- Count input validation.
- Mobile `More options` expand/collapse behavior.
- Auto-refresh on every filter change.
- `Given name only`, `Full name`, and `Surname only` output.
- Empty-state behavior for narrow filters.
- Meaning toggle behavior.
- Copy and save interactions.
- Responsive layout.
- No console errors.
- Uniform copy styling compared with the other name-generator pages.

---

## 12. Recommendation Summary

For v1, build a real Scottish name generator with:
- dedicated `scottish-names.json`
- `Given name only` as the default output mode
- a balanced dataset leaning modern
- practical filters rather than search-heavy filters
- short meaning notes
- the same mobile and typography behavior as the stronger existing name-generator pages

This scope is broad enough to outperform thin competitor tools and controlled enough to keep the data and UI maintainable.

# Random American Name Generator - Design Spec
Date: 2026-05-05

## Context
Build a dedicated Random American Name Generator as part of the name generator cluster supporting the pillar page `/random-name-generator/`. The page should reuse the existing Wordineer generator UX: count input, generate/reset buttons, result cards, copy/save controls, and the mobile "More options" toggle pattern.

The tool should outperform current top results by staying focused on realistic names, offering useful filters, and avoiding fake identity features that create privacy/trust issues.

Primary target page:
- URL: `/random-american-name-generator/`
- Output file: `random-american-name-generator.html`
- Source file: `template-deploy/tools-src/random-american-name-generator.html`
- Dedicated data file: `wordineer-deploy/data/american-names.json`

---

## 1. Competitor Takeaways

Checked references:
- `fantasynamegenerators.com/english-names.php`
- `namegeneratorfun.com/american`
- `fakenamegenerator.com/gen-male-us-us.php`
- `codeitbro.com/tool/american-name-generator`
- `generatorslist.com/random/names/american-name-generator`
- `randommer.io/Name`

Useful competitor features to keep:
- Gender filter: any, male, female.
- Name type filter: first name, surname, full name.
- Quantity control.
- Era/decade control for historical flavor.
- Copyable results.
- Simple explanatory SEO sections.

Features to avoid:
- Full fake identity profiles: addresses, SSNs, credit cards, passwords, phone numbers, fake emails.
- Login-gated saved identities.
- API/bulk export in the MVP.
- Long fictional character biographies.
- Overloaded ethnicity/culture controls on this page. Those should become separate cluster pages when useful.

Positioning:
- This is a name generator, not a fake identity generator.
- Results are fictional combinations from common American naming patterns.
- Focus on writers, game masters, teachers, baby name brainstorming, pen names, and creative projects.

---

## 2. Data File

**Path:** `wordineer-deploy/data/american-names.json`

**Recommended MVP schema:**
```json
{
  "first": [
    ["James", "m", ["classic", "common"], ["all", "1950s", "1980s", "modern"], "classic American male name"],
    ["Olivia", "f", ["modern", "common"], ["2000s", "modern"], "popular modern American female name"],
    ["Taylor", "u", ["modern", "unisex"], ["1980s", "1990s", "2000s", "modern"], "common unisex first name"]
  ],
  "middle": [
    ["Anne", "f", ["classic"], ["all"], "traditional middle name"],
    ["Lee", "u", ["classic", "southern"], ["all"], "common middle name"]
  ],
  "last": [
    ["Smith", ["common-us", "english"], "most familiar American surname style"],
    ["Garcia", ["common-us", "hispanic"], "common Hispanic American surname"],
    ["Murphy", ["irish-scottish"], "Irish-origin surname common in the US"]
  ]
}
```

**First and middle fields:**
- `[name, gender, styles, eras, note]`

**Last name fields:**
- `[name, styles, note]`

**Gender values:**
- `m`
- `f`
- `u`

**Style values for first/middle names:**
- `common`
- `classic`
- `modern`
- `old-fashioned`
- `southern`
- `unisex`

**Style values for last names:**
- `common-us`
- `english`
- `hispanic`
- `irish-scottish`
- `german`
- `italian`
- `french`
- `multicultural`

**Era values:**
- `all`
- `early-1900s`
- `1950s`
- `1970s`
- `1980s`
- `1990s`
- `2000s`
- `modern`

**Target data size:**
- First names: 350-500.
- Middle names: 100-200.
- Last names: 300-500.
- Total: 750-1,200 entries.
- Keep notes short, ideally under 80 characters.

**Source direction:**
- Use curated data for MVP.
- Prefer aggregate public data patterns from SSA baby names and Census surname/2020 names data.
- Do not include private identity data.

**Why a dedicated JSON file is the right choice:**
- American name filters need era, style, surname background, middle-name support, and result notes.
- Reusing a generic word/name dataset would make filtering messy.
- Dedicated files make the name generator cluster easier to extend for British, Japanese, Spanish, or other pages.

---

## 3. Tool Page

### Core Controls

Desktop layout should show controls in the tool panel. Mobile should show the same core count/generate area first, with advanced filters behind the existing "More options" toggle pattern.

Controls:
- Count: numeric input, default `10`, min `1`, max `50`.
- Gender: `Any`, `Female`, `Male`, `Neutral`.
- Name type:
  - `Full name`
  - `First name`
  - `Last name`
  - `First + middle + last`
- Era:
  - `Any era`
  - `Modern`
  - `2000s`
  - `1990s`
  - `1980s`
  - `1970s`
  - `1950s`
  - `Early 1900s`
- Style:
  - `Any style`
  - `Common`
  - `Classic`
  - `Modern`
  - `Old-fashioned`
  - `Southern`
  - `Unisex`
- Last name background:
  - `Any background`
  - `Common US`
  - `English / European`
  - `Hispanic American`
  - `Irish / Scottish`
  - `German`
  - `Italian`
  - `French`
- Starts with: `Any letter` plus A-Z.

### Filter Priority

When several filters are selected:
1. Filter first/middle names by gender.
2. Filter first/middle names by era.
3. Filter first/middle names by style.
4. Filter first names by starts-with.
5. Filter last names by background.
6. If a filter leaves too few results, gracefully broaden within the same category.

Example fallback:
- If `female + southern + starts with Z` has too few matches, keep `female + starts with Z`, then drop `southern`.
- Show no scary error unless there are truly zero viable names.

### Validation

- Count below 1: show inline error and clamp to 1.
- Count above 50: show inline error and clamp to 50.
- Missing data file: show fallback names and a subtle message only if needed.
- No matching names: show one-line message and suggest resetting filters.

### Result Item

Each result card should show:
- Main name: `Ava Grace Miller`
- Result note line:
  - `Modern American full name`
  - `Classic male first name`
  - `Common US surname`
- Optional chips:
  - `modern`
  - `female`
  - `common US surname`

Actions:
- Copy one result.
- Save one result.
- Copy all generated names.
- Copy saved names.

### Result Types

`Full name`:
- first + last
- Example: `Ethan Brooks`

`First name`:
- first only
- Example: `Madison`

`Last name`:
- surname only
- Example: `Johnson`

`First + middle + last`:
- first + middle + last
- Example: `Lily Anne Walker`

### Engine Integration

Preferred implementation:
- Reuse the custom generator area of `scripts/tool-engine.js` if it already supports page-specific generators cleanly.
- Otherwise add a narrowly scoped init path for `random-american-name-generator`.
- Keep shared copy/save/save-tag behavior consistent with the existing Random Name Generator page.

Do not duplicate large inline scripts inside the page unless the existing pattern requires it.

### Fallback Data

Include a small in-script fallback list for resilience:
- 20 first names.
- 10 middle names.
- 20 last names.

Fallback should be enough for the page to work if JSON loading fails during local testing, but the normal path should fetch `/data/american-names.json`.

---

## 4. SEO Copy Sections

### Meta

Title:
`Random American Name Generator - Realistic US Names | Wordineer`

Meta description:
`Generate random American names instantly. Create realistic first names, last names, full names, and middle-name combinations by gender, era, style, and starting letter. Free, no sign-up.`

Canonical:
`https://wordineer.com/random-american-name-generator/`

OG title:
`Random American Name Generator | Wordineer`

OG description:
`Create realistic American names for characters, stories, games, baby name ideas, pen names, and writing prompts. Filter by gender, era, style, and name type.`

### H1

`Random American Name Generator`

### Intro

Use this random American name generator to create realistic American first names, last names, and full names. Choose a gender, name type, era, style, and result count, then generate names for stories, games, baby name ideas, pen names, classroom prompts, and creative projects.

### What is a random American name generator?

A random American name generator creates name combinations that sound natural in the United States. Instead of building names from random letters, it uses familiar American first names, middle names, and surnames to produce believable results for characters, writing prompts, role-playing games, and brainstorming.

This page is more focused than a broad random name generator. It is designed for names that feel American in spelling, rhythm, and surname pairing, while still reflecting the mix of naming influences used across the United States.

### How it works

Choose how many names you want, select a gender or neutral mix, pick a name type, and optionally filter by era, style, surname background, or first letter. The tool combines first names, middle names, and surnames from American name lists to create realistic results.

You can copy a single name, copy the full list, or save favorites while you compare options.

### American name styles

American names come from many sources, including English, Spanish, Irish, German, Italian, French, Biblical, modern, and pop culture naming patterns. That mix is why names like James Miller, Sophia Garcia, Madison Brooks, and Elijah Johnson can all feel American in different ways.

Use the style filter when you want a more specific feel:
- Common for everyday names.
- Classic for familiar names that do not feel trendy.
- Modern for names popular in recent decades.
- Old-fashioned for vintage character names.
- Southern for names with a warmer regional style.
- Unisex for names used across genders.

### Ways to use the tool

Use the generator for:
- Fictional characters in novels, scripts, and short stories.
- NPCs for tabletop games and role-playing campaigns.
- Baby name brainstorming.
- Pen names and online aliases.
- Classroom writing prompts.
- Test names for design mockups and sample content.

### Related name generators

Need a different style of name? Try the main random name generator for mixed origins, the random Filipino name generator for Filipino names, or the random British name generator when that page is available.

Required internal keyword/link targets:
- `random name generator` -> `/random-name-generator.html` or `/random-name-generator/` depending current canonical decision.
- `random Filipino name generator` -> `/random-filipino-name-generator/`.
- `random British name generator` -> future `/random-british-name-generator/`.

### FAQ

Question: `Are these real people?`
Answer: `No. The tool creates fictional combinations from name lists. A generated name may coincidentally match a real person, but the results are not identity records.`

Question: `Can I use these names in a story or game?`
Answer: `Yes. These names are useful for fictional characters, RPG NPCs, screenplays, short stories, writing exercises, and other creative projects.`

Question: `What makes a name American?`
Answer: `American names often combine first names used in the United States with common surnames from many cultural backgrounds. The result can include English, Spanish, Irish, German, Italian, French, Biblical, modern, and pop culture influences.`

Question: `Can I generate old-fashioned American names?`
Answer: `Yes. Use the era and style filters to generate classic, vintage, or early twentieth-century name combinations.`

Question: `How is this different from the random name generator?`
Answer: `The random name generator covers many origins and name styles. This page focuses on names that feel natural in an American context.`

Question: `Does this tool generate fake identities?`
Answer: `No. It only generates names. It does not create addresses, SSNs, phone numbers, passwords, credit card numbers, or other identity details.`

---

## 5. tools.json Additions

Add the page to the name tools cluster once implemented.

Likely label:
- `American name`

Likely href:
- `/random-american-name-generator/`

Placement:
- Near `Random name` and `Filipino name` in the relevant tools list.

---

## 6. Internal Linking

Update the pillar page:
- Add a "More name generators" card/link for `Random American Name Generator`.
- Mention it in the section that lists specific name-origin tools.

Update related pages:
- `random-filipino-name-generator.html`: add related link to American generator once live.
- Future `random-british-name-generator.html`: link among American, Filipino, and the pillar page.

Suggested anchor text:
- `random American name generator`
- `American name generator`
- `realistic American names`

Avoid overstuffing. One natural exact-match link and one partial-match link are enough per related page.

---

## 7. Redirects

Add redirect support if the canonical URL uses a trailing slash:
- `/random-american-name-generator.html  /random-american-name-generator/  301`

Also ensure generated page path and canonical path match existing site conventions.

---

## 8. Verification

Manual testing through local HTTP server:
```bash
cd wordineer-deploy
python3 -m http.server 8080
```

Open:
- `http://localhost:8080/random-american-name-generator/`
- or `http://localhost:8080/random-american-name-generator.html` if testing output file directly through server.

Verify:
- JSON loads from `/data/american-names.json`.
- Generate button works.
- Count validation works for below 1 and above 50.
- Gender filter works.
- Name type filter works.
- Era filter works.
- Style filter works.
- Last name background filter works.
- Starts-with filter works.
- Copy one works.
- Save favorite works.
- Copy all works.
- Copy saved works.
- Reset restores defaults.
- Mobile "More options" toggle works.
- Results do not overflow on mobile.
- Browser console has no errors.

Validate JSON:
```bash
python3 -m json.tool wordineer-deploy/data/american-names.json >/dev/null
```

Build template output:
```bash
cd template-deploy
python3 build.py
```

Review generated files before deploy.

---

## Open Decisions

1. Should `neutral` names be a standalone gender option or included only under `Any`?
   - Recommendation: include both. `Any` mixes all genders; `Neutral` only returns `u` names.

2. Should the first version include middle names?
   - Recommendation: yes. It is a useful differentiator and not too complex.

3. Should result notes be shown under every name?
   - Recommendation: yes, but keep them short. This gives Wordineer more substance than thin competitor tools.

4. Should the MVP use official SSA/Census data imports?
   - Recommendation: no. Start with curated JSON inspired by public aggregate data. Full imports can be a later expansion.

5. Should the page include fake identity details?
   - Recommendation: no. Keep it names-only for user trust and cluster relevance.

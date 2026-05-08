# Random Japanese Name Generator - Design Spec
Date: 2026-05-06

## Context
Build a dedicated `random-japanese-name-generator.html` page as part of the name generator cluster supporting the pillar page `random-name-generator.html`. The tool should match the current Random Name Generator UX, including a mobile-collapsed "More options" panel, while using a dedicated Japanese names dataset because Japanese names need script fields, name-order handling, and culture-specific metadata.

Primary user groups:
- Writers naming Japanese characters
- Game masters and roleplayers
- Worldbuilders and game developers
- Users looking for Japanese name ideas with simple meanings

The tool should be fast, understandable, and culturally careful. It should not try to become a full baby-name, kanji, or fortune/stroke-count database.

---

## 1. High-CTR SEO Direction

### Recommended title tag
`Random Japanese Name Generator - Real Names & Meanings`

Reason:
- Keeps exact-match keyword at the front.
- Adds a trust/click hook with "Real Names & Meanings."
- Stays concise enough for search results.

### Alternate title tags
- `Japanese Name Generator: First, Last & Full Names`
- `Random Japanese Names With Meanings | Wordineer`
- `Japanese Name Generator - Names, Meanings & Kanji`

### H1
`Random Japanese Name Generator`

### Meta description
`Generate random Japanese names for characters, stories, games, and baby-name ideas. Filter by gender, style, meaning, and name order. Free, fast, no sign-up.`

### Target keywords
Primary:
- random japanese name generator
- japanese name generator
- random japanese names
- japanese names with meanings

Cluster/internal-link keywords:
- random name generator
- random filipino name generator
- random british name generator

---

## 2. Competitor Feature Takeaways

Sources reviewed:
- Reedsy Japanese Character Name Generator: `https://reedsy.com/resources/character-name-generator/language/japanese/`
- JapaneseNames.info: `https://japanese-names.info/generator/`
- Pon-Navi Nazuke: `https://en.pon-navi.net/nazuke/name/generator`
- Fantasy Name Generators: `https://www.fantasynamegenerators.com/japanese-names.php`
- NameGen.jp: `https://namegen.jp/en`
- Imagine Forest: `https://www.imagineforest.com/blog/japanese-name-generator/`
- MIT dataset candidate: `https://pypi.org/project/japanese-personal-name-dataset/`
- Dataset repository: `https://github.com/shuheilocale/japanese-personal-name-dataset`

### Worth using
- Gender filter
- First name / last name / full name filter
- Japanese order and Western order display
- Romaji plus optional Japanese script
- Name meanings or meaning notes
- Copy buttons
- Result count
- Simple educational text about Japanese name order
- Dedicated dataset instead of generic names

### Not worth using in v1
- Audio pronunciation
- Stroke count
- Fortune scoring
- Legal baby-name kanji validation
- Image-to-name generation
- Massive kanji search tools
- Regional surname distribution
- Scraped competitor data

Reason:
These features add complexity, accuracy risk, and maintenance burden. Wordineer can outdo simpler tools by being faster, clearer, better organized, and more useful for writers.

---

## 3. Data File

### Path
`wordineer-deploy/data/japanese-names.json`

### Recommended source approach
Use a licensed/open dataset as the base, then curate for UX quality. The strongest candidate found is `japanese-personal-name-dataset`, published under the MIT License, with:
- 5,678 male first-name readings
- 3,346 female first-name readings
- 2,000 last names
- Optimized/popular subsets of 703 male and 241 female first-name readings
- Hiragana, romaji, and kanji variations

Use the optimized first-name subsets first. Use up to 2,000 surnames if file size remains acceptable.

### Performance threshold
Target raw JSON size:
- Ideal: under 500KB
- Acceptable: up to 1MB
- Avoid: over 1MB unless split or lazy-loaded

Current reference sizes in `wordineer-deploy/data/`:
- `names.json`: 47KB
- `american-names-full.json`: 132KB
- `words.json`: 829KB
- `dictionary.json`: 2.5MB

For this page, aim for 300-700KB raw JSON. That should keep fetch and parse speed acceptable on mobile while allowing very broad combinations.

### Dataset size target
Recommended v1:
- 700 male given-name readings
- 240-500 female given-name readings
- 1,000-2,000 surnames
- Cap kanji variants to 1-5 per reading

This gives hundreds of thousands to millions of full-name combinations without loading unnecessary kanji variants.

### Compact schema
Use arrays rather than verbose objects if size becomes a concern.

```json
{
  "given": [
    ["Haruka", "はるか", ["遥", "春香"], "u", ["modern", "gentle"], ["nature", "spring"], "Distant, far-reaching, or spring fragrance depending on kanji."]
  ],
  "surnames": [
    ["Sato", "さとう", "佐藤", ["common", "classic"], ["plant"], "Wisteria field; one of Japan's most common surnames."]
  ]
}
```

Given-name fields:
`[romaji, hiragana, kanjiVariants, gender, styles, themes, meaning]`

Surname fields:
`[romaji, hiragana, kanji, styles, themes, meaning]`

Gender values:
- `m`
- `f`
- `u`

Style values:
- `modern`
- `traditional`
- `classic`
- `gentle`
- `strong`
- `elegant`
- `anime`

Theme values:
- `nature`
- `light`
- `season`
- `strength`
- `beauty`
- `wisdom`
- `peace`
- `place`
- `water`
- `flower`
- `sky`

### Accuracy note
Japanese names can have multiple kanji spellings, readings, and meanings. Meaning text should be phrased as "can mean," "often associated with," or "depending on kanji," not as a single definitive translation.

---

## 4. Tool Page

### Source path
`template-deploy/tools-src/random-japanese-name-generator.html`

### Output path
`wordineer-deploy/random-japanese-name-generator.html`

### Clean URL
`/random-japanese-name-generator/`

### Primary controls
Always visible:

| Control | Options |
|---|---|
| Name type | Full name / Given name only / Surname only |
| Gender | Any / Male / Female / Unisex |
| Count | 5 / 10 / 20, default 10 |

### More options
Mobile-collapsed, matching the current Random Name Generator page:

| Control | Options |
|---|---|
| Style | Any / Modern / Traditional / Classic / Gentle / Strong / Elegant / Anime/story |
| Meaning theme | Any / Nature / Light / Season / Strength / Beauty / Wisdom / Peace / Place / Water / Flower / Sky |
| Starts with | Any / A-Z |
| Name order | Japanese order / Western order / Show both |
| Script display | Romaji only / Romaji + Hiragana / Romaji + Hiragana + Kanji |

### Result card
Each result should show:
- Main generated name
- Japanese order line, e.g. `Sato Haruka`
- Western order line, e.g. `Haruka Sato`
- Script line when enabled, e.g. `佐藤 遥 / さとう はるか`
- Meaning line
- Style/theme badges
- Individual copy button

### Validation
- Count lower than 1: show existing-style error
- Count over 50: cap or show error
- No matching names: "No names match your filters. Try a broader style or theme."
- JSON load failure: "Name data could not load. Please refresh and try again."

---

## 5. Page Copy

### Intro
`Use this random Japanese name generator to create Japanese first names, surnames, and full names for characters, stories, games, and creative projects. Choose a gender, style, meaning theme, and name order, then copy the names you like.`

### Section: What Is a Random Japanese Name Generator?
`A random Japanese name generator creates Japanese-style names by combining given names and family names from a curated name list. Japanese names are usually written with the family name first, so a name like Sato Haruka places Sato before Haruka. This tool helps writers, roleplayers, game creators, and name researchers find names with readable spellings, useful meanings, and simple filters.`

### Section: How It Works
`Choose the type of name you want, select a gender or style, and click generate. The tool pulls matching names from a dedicated Japanese name dataset and displays each result with its romaji spelling, Japanese order, optional Japanese script, and meaning notes. Use More options on mobile to reveal extra filters without crowding the page.`

### Section: Japanese Name Order
`In Japanese, the family name usually comes before the given name. For example, Sato Haruka uses Sato as the family name and Haruka as the given name. This generator can show Japanese order, Western order, or both so the result is easier to use in stories, games, and character profiles.`

### Section: More Random Name Generators
`Need names from another background? Try the main random name generator for broad name ideas, or explore focused tools like the random Filipino name generator and random British name generator as the Wordineer name generator cluster grows.`

### FAQ candidates
1. Can I use these Japanese names in a story or game?
2. Are these real Japanese names?
3. Why do Japanese names show family name first?
4. Do Japanese names have one exact meaning?
5. Is this random Japanese name generator free?

---

## 6. Internal Linking

Add links from:
- `random-name-generator.html` to `random-japanese-name-generator.html`
- Japanese page to `random-name-generator.html`
- Japanese page to future/available cluster pages:
  - `random-filipino-name-generator.html`
  - `random-british-name-generator.html`
  - `random-american-name-generator.html` if present

Use natural anchor text in body copy and related-tools blocks.

---

## 7. Implementation Checklist

1. Create or convert `wordineer-deploy/data/japanese-names.json`.
2. Validate JSON with `python3 -m json.tool`.
3. Add source page at `template-deploy/tools-src/random-japanese-name-generator.html`.
4. Add metadata entry to `template-deploy/tools.json`.
5. Build template output with `cd template-deploy && python3 build.py`.
6. Copy/review generated output in `wordineer-deploy/` as required by repo workflow.
7. Add clean URL redirect/header entries if current deployment pattern requires it.
8. Add internal links from the pillar page and related generator areas.
9. Run local static server from `wordineer-deploy/`.
10. Test desktop and mobile:
    - Generate button
    - All filters
    - More options toggle
    - Copy buttons
    - JSON loading
    - Console errors
    - Responsive layout
    - SEO title/meta/canonical/schema

---

## 8. Open Decisions Before Build

Default decisions:
- Use optimized/popular source first, not full unfiltered source.
- Show both Japanese and Western order by default.
- Default script display: `Romaji + Hiragana + Kanji`.
- Default count: 10.
- Cap generated count at 50.

Potential decision to revisit:
- Whether to include `anime/story` as a style label. It has user demand, but should not generate fake names. Use it only as a vibe tag over real names that feel short, memorable, or character-friendly.

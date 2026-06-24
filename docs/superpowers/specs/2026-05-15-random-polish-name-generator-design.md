# Random Polish Name Generator — Design Spec

**Date:** 2026-05-15  
**Status:** Design approved  
**Audience:** Developers, QA, writers, game makers, baby name seekers

---

## Overview

The Random Polish Name Generator is a free, fast name generator for users seeking authentic Polish names with cultural depth. It filters by gender, era, and first letter, displays meanings and text-based pronunciation, and defaults to first names for quick scanning.

---

## Data Structure

### JSON File: `polish-names.json`

Located in `wordineer-deploy/data/polish-names.json`.

```json
{
  "given": [
    {
      "name": "Jakub",
      "gender": "m",
      "era": ["modern"],
      "meaning": "supplanter; one who holds the heel",
      "pronunciation": "YAH-koop"
    },
    {
      "name": "Zofia",
      "gender": "f",
      "era": ["traditional", "modern"],
      "meaning": "wisdom",
      "pronunciation": "ZOH-fee-ah"
    }
  ],
  "surnames": [
    {
      "name": "Kowalski",
      "meaning": "smith; one who works with metal",
      "pronunciation": "koh-VAL-skee"
    },
    {
      "name": "Nowak",
      "meaning": "new; recent arrival",
      "pronunciation": "NOH-vahk"
    }
  ]
}
```

**Schema:**
- **given names:**
  - `name` (string): The given name
  - `gender` (string): `"m"` or `"f"`
  - `era` (array): `["traditional"]`, `["modern"]`, or both
  - `meaning` (string): Short etymological or cultural meaning (~60 chars max)
  - `pronunciation` (string): Phonetic spelling in English (e.g., "YAH-koop")

- **surnames:**
  - `name` (string): The surname
  - `meaning` (string): Meaning or origin (~60 chars max)
  - `pronunciation` (string): Phonetic spelling

**Data size:**
- 300 male given names
- 300 female given names
- 400 surnames
- **Total: 1000+ combinations**

---

## UI & Filters

### Filter Controls (Left Panel, Desktop / Collapsible Mobile)

**Name Type** (Default: "First name")
- Options: "First name" | "Full name" | "Surname"
- Selector: dropdown or radio buttons
- Behavior: changes which parts of the name are displayed in results

**Gender** (Default: "Any")
- Options: "Male" | "Female" | "Any"
- Selector: dropdown or radio buttons
- Only applies to given names; surnames are always shown

**Era** (Default: "All")
- Options: "Traditional" | "Modern" | "All"
- Selector: dropdown or radio buttons
- Traditional = 18th–20th century; Modern = 1970s–present
- "All" shows both eras mixed

**First Letter** (Default: "All")
- Options: A–Z
- Selector: dropdown
- Filters results by first letter of the given name

**Number of names** (Default: 10)
- Range: 1–50
- Input: number field
- Behavior: updates results on change

**Show meanings & pronunciation** (Default: ON)
- Type: toggle checkbox with slider (like Greek/Italian generators)
- Behavior: hides/shows the meaning and pronunciation text under each name
- Mobile: toggle stays visible in advanced filters

### Mobile UX

- **Default view:** Name type, gender, era, number field visible
- **Advanced filters (collapsed by default):** First letter, show/hide toggle
- **Toggle button:** "More options" / "Fewer options" appears above filters on mobile
- When expanded: all filters visible, layout adjusts to single column

---

## Results Display

### Result Card

Each name displays as:
```
Jakub Kowalski
meaning: supplanter | smith
pronunciation: YAH-koop | koh-VAL-skee
```

Or with toggle OFF:
```
Jakub Kowalski
```

**Display logic:**
- If "First name" is selected: show only given name + meaning + pronunciation
- If "Full name" is selected: show given name + surname + both meanings + both pronunciations
- If "Surname" is selected: show only surname + meaning + pronunciation

---

## Page Content

### Title & Meta

**Page Title:** "1000+ Random Polish Names Generator | Wordineer"

**Meta Description:** "Generate authentic Polish names — Traditional classics (Henryk, Zofia) or Modern favorites (Jakub, Marta). Filter by gender, era, and first letter. Includes meanings and pronunciation. Free, no sign-up."

**Schema (JSON-LD FAQPage):**
- "What is a random Polish name generator?"
- "What's the difference between Traditional and Modern Polish names?"
- "Why do Polish surnames end in -ski?"
- "Can I use these names in my book?"

### Hero Section

**Heading:** "Random Polish Name Generator"

**Subheading:** "Generate authentic Polish names — from traditional classics (Henryk, Zofia) to modern favorites (Jakub, Marta). Filter by gender, era, and first letter. Includes meanings and pronunciation."

**Badge:** "Free · No sign-up · Instant"

### Explainer Section

**Title:** "How it works"

**Content (3–4 short paragraphs):**
1. Explain the tool's purpose: "Generates authentic Polish names for writers, game makers, baby names, character development."
2. Explain eras: "Traditional names (Henryk, Stanisław) carry Polish literary and historical weight. Modern names (Jakub, Emma) reflect contemporary Polish usage. Both sets are real, verified names."
3. Mention pronunciation + meanings: "Each name includes text-based pronunciation (for non-Polish speakers) and etymological meaning to help with character building."
4. Usage: "Quick first-name scans, or build full names by switching to 'Full name' mode."

**Title:** "Who uses this?"

**Content:** Writers building medieval Polish settings, game masters, parents seeking baby names, character developers, students researching Polish culture.

### FAQ Section

| Question | Answer |
|----------|--------|
| **What is a random Polish name generator?** | A tool that generates real Polish given names, surnames, or full names from a curated dataset of 1000+ authentic names. Each name includes its meaning and English-friendly pronunciation guide. |
| **What's the difference between Traditional and Modern Polish names?** | Traditional names (Henryk, Stanisław, Zofia) were most popular in the 18th–20th centuries and carry a sense of Polish history and literary tradition. Modern names (Jakub, Marta, Filip) have risen in popularity since the 1970s and reflect contemporary Polish usage. Choose Traditional for historical fiction; Modern for contemporary stories. |
| **Why do Polish surnames end in -ski?** | The -ski suffix is one of the most common Polish surname endings and originally meant "of/from" — for example, Kowalski meant "of the smith" (kowal = smith). Other common endings are -ak, -czyk, and -wicz. These endings reflect the name's origin: occupation, place, or patronymic tradition. |
| **Can I use these names in my book?** | Yes. All names here are real names from Polish traditions and culture. Names themselves are not copyrightable, so you can use them freely in fiction, screenplays, games, and other creative projects. The meanings and pronunciations are cultural glosses meant to help you understand and use the names authentically. |

---

## Technical Implementation

### File Changes

**Create:** `wordineer-deploy/data/polish-names.json`

**Create:** `template-deploy/tools-src/random-polish-name-generator.html`  
(Following the pattern of `random-danish-name-generator.html`)

**Update:** `template-deploy/tools.json`  
- Add to `mega` → "Name generators" category
- Add to `more_word_tools` → name_generator_tools section
- Add to `footer_cols` → relevant footer link

**Create (optional):** `wordineer-deploy/_redirects` entry  
- Add clean URL rewrite: `/random-polish-name-generator/ → /random-polish-name-generator.html`

**Update:** `build.py` (if needed)  
- Ensure the build system picks up the new tool-src file

### Build & Deploy

1. Create JSON data file
2. Create HTML template file
3. Update tools.json
4. Run `python3 build.py` in `template-deploy/`
5. Copy output to `wordineer-deploy/`
6. Preview locally at `localhost:8080/random-polish-name-generator/`
7. Push to git → auto-deploy to Cloudflare Pages

---

## Success Criteria

✓ Generator loads instantly (no blocking data fetches at page load)  
✓ First-name default renders 10 names immediately  
✓ Filters trigger auto-regeneration (no explicit "Generate" button)  
✓ Mobile toggle for advanced filters works smoothly  
✓ Meanings & pronunciation toggle displays/hides correctly  
✓ All 1000+ name combinations are achievable through the UI  
✓ Title and meta description are high-CTR (clear, benefit-focused)  
✓ FAQ and "How it works" sections load and display correctly  
✓ PageSpeed Lighthouse score remains strong (no new performance regressions)

---

## Verification Before Implementation

- [ ] Check Greek/Italian generator code for toggle implementation pattern
- [ ] Verify that `name type` filter default ("First name") is implemented
- [ ] Confirm data file loads via deferred fetch (not blocking initial render)
- [ ] Test mobile collapse/expand toggle
- [ ] Test pronunciation + meaning toggle on/off
- [ ] Verify clean URL redirect works (`/random-polish-name-generator/`)

---

## Scope & Boundaries

**In scope:**
- Polish given names + surnames (1000+ total)
- Meanings + text-based pronunciation
- Gender, era, first-letter filters
- Name type selector (first/full/surname)
- Meaning/pronunciation toggle
- FAQ + "How it works" explainer

**Out of scope:**
- Audio pronunciation (too heavy)
- Bulk export (CSV/JSON download)
- Popularity rankings
- Celebrity examples
- User accounts / saved favorites
- Advanced regional/occupational categories

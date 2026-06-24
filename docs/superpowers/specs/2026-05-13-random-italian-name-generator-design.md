# Random Italian Name Generator — Design Spec

**Date:** 2026-05-13
**Status:** Approved for implementation

---

## Context

Wordineer has locale-specific name generators for Japanese, Scottish, Filipino, British, German, Greek, Indian, Irish, Russian, Thai, and more. Italian is a high-search-volume gap. Competitors (Reedsy, Story Shack, Mythopedia, Unitpedia) offer minimal filters, no copy/save functionality, and no letter filter. A well-featured Italian generator with regional and style filters will outrank them on functionality.

---

## Approach

Dedicated `italian-names.json` data file — consistent with `japanese-names.json`, `scottish-names.json`, `philippine-names.json`. Italian-specific filters (region, style) require per-name metadata that the generic `names.json` schema does not support. Seed fallback hardcoded in the page for instant first render; full JSON loaded async.

---

## Data File

**Path:** `wordineer-deploy/data/italian-names.json`

### Schema

```json
{
  "given": [
    { "n": "Marco",    "g": "m", "s": "classic",   "r": "any",     "d": "warlike; defender" },
    { "n": "Giulia",   "g": "f", "s": "classic",   "r": "any",     "d": "youthful; soft-haired" },
    { "n": "Luca",     "g": "m", "s": "modern",    "r": "any",     "d": "light; bringer of light" },
    { "n": "Giuseppe", "g": "m", "s": "religious", "r": "any",     "d": "God will add; Italian form of Joseph" },
    { "n": "Fiore",    "g": "u", "s": "regional",  "r": "south",   "d": "flower" }
  ],
  "surnames": [
    { "n": "Russo",    "r": "south",   "d": "red-haired; common in southern Italy" },
    { "n": "Ferrari",  "r": "north",   "d": "blacksmith" },
    { "n": "Ricci",    "r": "central", "d": "curly-haired" }
  ]
}
```

### Field values

| Field | Values |
|---|---|
| `g` | `"m"` / `"f"` / `"u"` (unisex) |
| `s` | `"classic"` / `"modern"` / `"religious"` / `"regional"` (dialectal/folk forms) |
| `r` | `"north"` / `"central"` / `"south"` / `"sicily"` / `"any"` |
| `d` | Meaning string, ≤100 chars |

### Target counts

- Given names: 500+ (≈200 male, 200 female, 100 unisex)
- Surnames: 300+ with regional metadata

---

## Filters

| Filter | Default | Options |
|---|---|---|
| Number of names | **5** | 1–50 |
| Gender | Any | Any / Male / Female |
| Name type | Given name only | Given name only / Full name / Surname only |
| Style | Any | Any / Classic & Traditional / Modern / Religious & Saint / Regional & Dialectal |
| Region | Any | Any / Northern Italy / Central Italy / Southern Italy / Sicily |
| First letter | Any | Any / A–Z |
| Show meanings | On (checked) | Toggle checkbox |

### Mobile layout

Always visible: Number of names, Gender, Name type.
Collapsed behind "More options" toggle: Style, Region, First letter, Show meanings.
Same `aria-expanded` toggle pattern as all other name generators.

### Desktop layout

All filters visible in left-side `.ctrl` panel.

---

## JavaScript

**Variable prefix:** `it_`
**localStorage key:** `wnr_saved_it_names`

Follows identical structure to `random-japanese-name-generator.html`:

1. Seed fallback: ~30 hardcoded names in `init` slot for instant first render
2. Async load: `fetch('/data/italian-names.json')` after page ready; auto-regenerate on completion
3. Filter logic:
   - Gender: `n.g === cfg.gender || cfg.gender === 'any' || n.g === 'u'`
   - Style: match `n.s` to filter value (map UI label → data value)
   - Region: match `n.r` to filter value, `r === 'any'` entries always match
   - First letter: `n.n[0].toLowerCase() === cfg.letter` (skip if Any)
   - Name type: given-only → first name pool; surname-only → surnames pool; full → combine
4. Deduplication via `Set` on combined name strings
5. Keyboard: Space/Enter (not focused on input/select) triggers regenerate
6. Instant regeneration on any filter change

---

## Name Card Display

```
Marco Russo
[Classic] [Northern Italy]
warlike; defender · blacksmith
[📋 copy] [♥ save]
```

- Name: bold, large (consistent with other generators)
- Style + Region: colored pill badges
- Meaning: shown/hidden via "Show meanings" toggle; for full names, given meaning + surname meaning separated by " · "
- Copy button: checkmark feedback for 900ms
- Save/heart: toggles red fill + light red background; persists to localStorage

---

## Page Slots

### `meta`
- Title: `Random Italian Name Generator - 800+ Italian Names`
- Description: Generate random Italian names for characters, stories, games, and ancestry research. Filter by gender, region, style, and era. Free, fast, no sign-up.
- Canonical: `https://wordineer.com/random-italian-name-generator/`
- JSON-LD: FAQPage schema

### `hero`
- H1: "Random Italian Name Generator"
- Subhead: Generate authentic Italian names filtered by gender, region, and style.

### `explainer`
Two sections:
1. **What is a random Italian name generator?** — explains the tool purpose (writers, gamers, ancestry researchers, language learners)
2. **How it works** — describes filter options and data basis (real Italian given names and surnames)

### `faq` (6 questions)
1. What are common Italian last names?
2. How are Italian names structured?
3. What do Italian names mean?
4. Are Italian names gendered?
5. What's the difference between northern and southern Italian names?
6. Can I use these names for a story or character?

### `who`
Four use-case cards: Writers & storytellers / Game designers / Ancestry researchers / Language learners

---

## Files to Create / Modify

| File | Action |
|---|---|
| `template-deploy/tools-src/random-italian-name-generator.html` | **Create** |
| `wordineer-deploy/data/italian-names.json` | **Create** |
| `template-deploy/tools.json` | **Modify** — add to mega, more_word_tools, other_tools, footer_cols |
| `wordineer-deploy/_redirects` | **Modify** — add `/random-italian-name-generator/` rewrite |
| `wordineer-deploy/sitemap.xml` | **Modify** — add URL entry |

---

## Verification

1. `cd template-deploy && python3 build.py` — confirm no build errors
2. `cp template-deploy/output/random-italian-name-generator.html wordineer-deploy/`
3. `cd wordineer-deploy && python3 -m http.server 8080`
4. Open `http://localhost:8080/random-italian-name-generator.html`
5. Verify:
   - Page renders immediately with seed fallback names (5 given names, no full names)
   - Async JSON loads and regenerates automatically
   - Gender filter → only male/female/unisex names appear
   - Style filter → only matching style names appear
   - Region filter → `r: "any"` names always appear; regional names only when matched
   - First letter → names start with selected letter only
   - Full name mode → given name + surname combined
   - Surname only → only surnames shown (no gender filter applies)
   - Show meanings toggle → meanings appear/hide instantly
   - Copy button → checkmark feedback 900ms
   - Save button → heart fills, name persists after page reload
   - Mobile: More options toggle collapses/expands advanced filters
   - Space/Enter (unfocused) regenerates

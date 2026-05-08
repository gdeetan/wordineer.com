# Random Filipino Name Generator — Design Spec
Date: 2026-05-04

## Context
Building a dedicated Filipino name generator page as part of a name generator cluster supporting the pillar page `/random-name-generator/`. The tool needs its own JSON dataset (Filipino naming conventions differ too much from the generic `names.json` schema), a full tool-src page matching the existing name generator's UX patterns, SEO copy targeting Filipino name keywords, and internal linking updates on the random name generator page to surface the cluster.

---

## 1. Data File

**Path:** `wordineer-deploy/data/philippine-names.json`

**Schema:**
```json
{
  "first": [
    ["Ligaya", "f", "traditional", "happiness, joy"],
    ["Jose",   "m", "spanish",     "God will increase"],
    ["Angel",  "f", "modern",      "divine messenger"],
    ["Nene",   "f", "nickname",    "baby girl; term of endearment"]
  ],
  "last": [
    ["Santos",    "spanish",     "saints"],
    ["Reyes",     "spanish",     "kings"],
    ["Magsaysay", "traditional", "to say, to tell"]
  ]
}
```

- **First name fields:** `[name, gender, style, meaning]`
- **Last name fields:** `[name, style, meaning]`
- **Gender values:** `"m"` | `"f"` | `"u"`
- **Style values:** `"traditional"` | `"spanish"` | `"modern"` | `"nickname"`

**Target size:** Maximize coverage without bloating. Aim for ~350 first names and ~175 last names (~525 total). Keep each meaning under ~80 chars. Estimated file size ~45–55KB, on par with `names.json` (47KB).

**Style category definitions:**
- `traditional` — pre-colonial Malay-rooted names (Ligaya, Dalisay, Bayani, Luningning, Liwanag)
- `spanish` — saint names and Spanish words adopted during colonization (Jose, Maria, Santos, Cruz, Reyes)
- `modern` — English/international names common in the Philippines since the 20th century (Angel, Kim, Kylie, John)
- `nickname` — common Filipino diminutives and pet names (Nene, Totoy, Inday, Dodong, Tita)

**Note:** Last names do not use the `nickname` style — only `traditional` and `spanish` are needed there.

---

## 2. Tool Page

**Source path:** `template-deploy/tools-src/random-filipino-name-generator.html`
**Output path:** `wordineer-deploy/random-filipino-name-generator.html`
**Clean URL:** `/random-filipino-name-generator/`
**Config type:** `"tool"` (full layout with nav/grids/ads/footer)

### Filters

**Always visible (primary panel):**
| Control | Options |
|---|---|
| Gender | Any / Male / Female |
| Style | Any / Traditional Tagalog / Spanish-colonial / Modern/Western / Nickname form |
| Count | Number input, 1–50, default 5 |

**"More options" panel (mobile-collapsed, same toggle as random name generator):**
| Control | Options |
|---|---|
| Name type | Full name / First name only / Last name only |
| Starting letter | A–Z dropdown (default: Any) |

### Validation
- Count < 1 → error toast: "Please enter a number between 1 and 50."
- Count > 50 → error toast: "Maximum 50 names at a time."
- No names match current filters → error toast: "No names match your filters. Try adjusting your options."
- Mirror the exact validation logic and error UX from `random-name-generator.html`.

### Result item
Each generated name displays:
- Full name (first + last, or first/last only per name type filter)
- Meaning line (e.g., "happiness, joy")
- Style badge (e.g., "Traditional")
- Copy button (individual)
- Save/heart button (adds to saved list)

### Engine integration
Use the same `WORDINEER.init({ mode: 'custom', ... })` pattern as the random name generator:
```js
WORDINEER.init({
  mode:           'custom',
  data:           pfData,
  renderItem:     pfRenderItem,
  generateFn:     pfGenerateFn,
  listId:         'pf-list',
  countDisplayId: 'pf-count-display',
  generateBtnId:  'pf-gen-btn',
  copyAllBtnId:   'pf-copy-all-btn',
  savedKey:       'wnr_saved_filipino_names',
  savedListId:    'pf-saved-tags'
});
```

### Fallback data
Embed ~10 first names and ~6 last names (mix of all 4 styles) directly in the `<script>` block for instant first render before `philippine-names.json` loads.

---

## 3. SEO Copy Sections

**Slug:** `/random-filipino-name-generator/`
**Primary keyword:** random Filipino name generator
**Secondary keywords:** random name generator, random American name generator, randomest names

### Slots to populate:
| Slot | Content |
|---|---|
| `meta` | Title: "Random Filipino Name Generator — 525+ Names with Meanings" · Meta desc targeting primary keyword · JSON-LD FAQ schema |
| `hero` | H1: "Random Filipino Name Generator" · Subtitle: "Generate male, female, and unisex Filipino names — traditional, Spanish-colonial, modern, and nickname styles — with meanings." |
| `explainer` | **What is a Random Filipino Name Generator** (2–3 sentences, primary keyword) → **How Filipino Names Work** (~150 words: Spanish colonial surnames, Malay-rooted first names, modern Western adoption, nickname culture) → **Types of Filipino Names** (one short paragraph per style, maps to the 4 filter options) |
| `who` | Writers, game designers, genealogists researching Filipino heritage, parents choosing names, students writing stories set in the Philippines |
| `faq` | 5 questions: most common Filipino surnames · difference between traditional and Spanish-colonial · are Filipino names gender-specific · how Filipino nicknames work · can I use these for fiction |
| `related` | "Looking for names from other countries? Try the [Random Name Generator](/random-name-generator/) for 600+ names across 30+ origins." (targets "random name generator" and seeds internal link) |

---

## 4. tools.json Additions

Add the Filipino name generator to all 4 registry sections:

**`mega`** — add under the name generators group (alongside `/random-name-generator/`):
```json
{ "href": "/random-filipino-name-generator/", "text": "Filipino names" }
```

**`more_word_tools`** — new card:
```json
{
  "href": "/random-filipino-name-generator/",
  "name": "Random Filipino name",
  "desc": "Generate Filipino names with meanings — traditional, Spanish-colonial, and modern styles.",
  "icon_bg": "#F5E6E6",
  "icon_path": "<circle cx=\"6.5\" cy=\"4\" r=\"2.2\" stroke=\"#C0392B\" stroke-width=\"1.1\"/><path d=\"M1.5 11.5c0-2.8 2.2-5 5-5s5 2.2 5 5\" stroke=\"#C0392B\" stroke-width=\"1.1\" stroke-linecap=\"round\"/>"
}
```

**`other_tools`** — add link under the names category.

**`footer_cols`** — add link under the names column.

---

## 5. Internal Linking: Random Name Generator Page

Update `template-deploy/tools-src/random-name-generator.html` more tools grid to include:

| Link | URL | Status |
|---|---|---|
| Random Filipino Name Generator | `/random-filipino-name-generator/` | New (this build) |
| Random American Name Generator | `/random-american-name-generator/` | Future (stub link, build next) |
| Random Word Generator | `/random-word-generator/` | Exists (replaces any self-referencing slot) |

Do **not** change the random word generator page.

---

## 6. Redirects

Add to `wordineer-deploy/_redirects`:
```
/random-filipino-name-generator.html  /random-filipino-name-generator/  301
```

---

## 7. Verification

1. `cd template-deploy && python3 build.py` — should produce `output/random-filipino-name-generator.html` with no errors
2. `cp template-deploy/output/*.html wordineer-deploy/`
3. `cd wordineer-deploy && python3 -m http.server 8080`
4. Open `http://localhost:8080/random-filipino-name-generator.html`
5. Check: generate works with default filters, all 4 style filters produce results, count validation fires for 0 and 51, save/copy functions work, "More options" toggle works on mobile viewport
6. Open `http://localhost:8080/random-name-generator.html` — verify new internal links appear in more tools section
7. Confirm no self-referencing links on the random name generator page

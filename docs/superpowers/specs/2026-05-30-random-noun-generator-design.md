# Random Noun Generator — Design Spec
**Date:** 2026-05-30  
**Status:** Approved

---

## Context

Wordineer needs a dedicated Random Noun Generator page. Every competitor in the space offers a basic count-and-generate noun tool, but none implement a noun-type filter (abstract/concrete/proper/common/collective) despite all of them writing about these types in their copy. This is the key differentiator. Combined with Wordineer's existing definition display and save/favorites UX (also absent from all competitors), this becomes the strongest noun generator online.

**Primary audience:** Writers and creatives.  
**Goal:** Beat all competitor tools on both features and copy depth.

---

## Architecture

### New files
| File | Purpose |
|---|---|
| `template-deploy/tools-src/random-noun-generator.html` | Source tool file (edit here) |
| `wordineer-deploy/data/nouns.json` | Dedicated noun dataset |
| `wordineer-deploy/random-noun-generator.html` | Built output (copy from `template-deploy/output/`) |

### Modified files
| File | Change |
|---|---|
| `template-deploy/tools.json` | Add to mega, more_word_tools, footer_cols |
| `wordineer-deploy/_redirects` | Add clean URL redirect |

---

## Data: `wordineer-deploy/data/nouns.json`

Schema mirrors `words.json` but noun-only with added `nt` field:

```json
{ "w": "Abundance", "nt": "abstract", "diff": "medium", "d": "a very large quantity of something" }
```

**Fields:**
- `w` — word (string, title-case)
- `nt` — noun type: `"abstract"` | `"concrete"` | `"proper"` | `"common"` | `"collective"`
- `diff` — difficulty: `"easy"` | `"medium"` | `"hard"`
- `d` — definition, under ~100 chars

**Target size:** 400–600 nouns, balanced across types and difficulties.

**Distribution target:**
- abstract: ~25% (themes, emotions, concepts — most useful for writers)
- concrete: ~30% (tangible objects — most learner-friendly)
- common: ~20% (everyday items that don't fit abstract/concrete split)
- proper: ~15% (places, names, brands — useful for character/setting brainstorming)
- collective: ~10% (group nouns — small but distinctive)

---

## Tool UI

Mirrors the `random-word-generator` layout (left controls panel + right word list panel).

### Left panel controls
| Control | Values |
|---|---|
| Count | Number input, 1–50 |
| Noun Type | All Types / Abstract / Concrete / Proper / Common / Collective |
| Difficulty | Any / Easy / Medium / Hard |
| First Letter | Text input (single character) |
| Definitions | Toggle on/off |
| Buttons | Generate (primary, Space triggers), Reset |

### Right panel
- Word list with inline definitions (when toggled on)
- Per-word copy button on each entry
- Copy All + Regenerate buttons at top
- Saved words section (heart icon to save, copy-saved button)

### Breadcrumbs
Placed above the hero, matching `random-3-letter-word-generator` pattern:
```html
<div class="breadcrumb">
  <div class="breadcrumb-inner">
    <a href="/">Wordineer</a>
    <span class="breadcrumb-sep">›</span>
    <a href="/word-tools/">Word Tools</a>
    <span class="breadcrumb-sep">›</span>
    <span aria-current="page">Random Noun Generator</span>
  </div>
</div>
```

---

## Copy Structure (~1,140 words, writers-focused)

### Hero intro (~50w)
Hook for writers. Lead with the idea that the right noun unlocks a sentence. Mention the noun-type filter as the key feature.

### What is a Random Noun Generator? (~120w)
- Defines the tool
- Explains why a dedicated noun generator beats generic word generators
- Calls out the noun-type filter as unique to Wordineer

### Why Use a Random Noun Generator? (~180w)
Four use cases:
1. Creative writing / brainstorming — break blocks, discover unexpected imagery
2. Vocabulary building — expand range, discover new words with definitions
3. Word games — Pictionary, Scrabble, 20 Questions
4. Classroom — vocabulary exercises, grammar practice

### Types of Nouns Explained (~280w)
Define all 5 types with examples, then explain how the filter helps:
- **Abstract** — ideas, emotions, concepts (freedom, grief, velocity) → use for themes and internal conflict
- **Concrete** — tangible objects (hammer, river, cathedral) → use for sensory detail and setting
- **Proper** — specific names (Paris, Nile, Monday) → use for character names, locations, historical flavor
- **Common** — general categories (dog, city, book) → everyday language building blocks
- **Collective** — group nouns (flock, parliament, murder) → vivid, precise descriptions

### How to Use This Tool (~100w)
Three steps:
1. Choose noun type and difficulty
2. Hit Generate (or press Space)
3. Copy individual words or use Copy All; save favorites with the heart icon

### Best Practices for Writers (~150w)
- Use abstract nouns when you need to explore your story's themes
- Use concrete nouns to add physical texture to a scene
- Mix difficulty levels to vary the voice register
- Generate 10–15, read through without judging, save the 2–3 that spark something
- Toggle definitions on when you're building vocabulary, off when you want flow

### FAQ (~200w, 6–8 questions)
1. What is a noun?
2. What's the difference between abstract and concrete nouns?
3. What is a collective noun? (with examples)
4. Can I filter nouns by type?
5. Is this tool free?
6. How do I save results?
7. How many nouns are in the database?
8. Does this work for Pictionary / word games?

### Who Uses It (~60w, 4 cards)
- Fiction Writers
- Students
- Game Nights
- Educators

---

## URL & Routing

- **Canonical URL:** `/random-noun-generator/`
- **HTML file:** `random-noun-generator.html`
- **CONFIG block:**
  ```json
  { "url": "/random-noun-generator/", "output": "random-noun-generator.html", "type": "tool" }
  ```
- **`_redirects` entry:** `/random-noun-generator /random-noun-generator/ 301`
- **`tools.json` additions:**
  - `mega` → "Writing & Vocabulary" tools array
  - `more_word_tools` grid
  - `footer_cols` → "Writing & Vocabulary" links array

---

## Verification

1. `cd template-deploy && python3 build.py` — build completes without errors
2. `cp template-deploy/output/random-noun-generator.html wordineer-deploy/`
3. `cd wordineer-deploy && python3 -m http.server 8080`
4. Verify at `http://localhost:8080/random-noun-generator.html`:
   - All 5 noun type options filter correctly
   - Definitions toggle shows/hides inline definitions
   - Copy All copies the word list to clipboard
   - Save (heart) persists words in the saved section
   - Space bar triggers generate
   - Reset clears filters
   - Breadcrumbs render: Wordineer › Word Tools › Random Noun Generator
5. Check `_redirects` entry routes `/random-noun-generator` → `/random-noun-generator/`
6. Validate JSON-LD schema renders in page source
7. Lighthouse mobile score ≥ 90

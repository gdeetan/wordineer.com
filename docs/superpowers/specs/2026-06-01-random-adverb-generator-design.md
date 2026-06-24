# Design: Random Adverb Generator

**Date:** 2026-06-01  
**Status:** Approved  
**URL:** `/random-adverb-generator/`

---

## Context

No adverb generator exists on Wordineer. Competitors (RandomLists, AppZaza, TechWelkin, GeneratorsList, Perchance) all offer word-only output with zero filtering beyond quantity. None show definitions, none offer adverb subtype or difficulty filtering. This tool fills that gap by combining the noun generator's deep filtering with bulk-friendly export — becoming the most capable adverb generator in the top search results.

---

## Files Changed

| File | Action |
|------|--------|
| `wordineer-deploy/data/adverbs.json` | Create — ~500 adverb entries |
| `wordineer-deploy/scripts/tool-engine.js` | Edit — add `advTypeId` support + version bump |
| `template-deploy/tools-src/random-adverb-generator.html` | Create — new tool page |
| `template-deploy/tools-src/word-tools.html` | Edit — activate placeholder link |
| `template-deploy/tools.json` | Edit — add to mega, more_word_tools, footer_cols |
| `template-deploy/output/random-adverb-generator.html` | Build output (generated) |
| `wordineer-deploy/random-adverb-generator.html` | Deploy copy |

---

## 1. Data File — `adverbs.json`

Schema per entry:
```json
{ "w": "Quickly", "t": "adverb", "advType": "manner", "d": "at a fast speed", "diff": "easy", "borrowed": false }
```

Fields:
- `w` — word (title-case)
- `t` — always `"adverb"`
- `advType` — `"manner"` | `"time"` | `"place"` | `"degree"` | `"frequency"`
- `d` — definition, max ~100 chars
- `diff` — `"easy"` | `"medium"` | `"hard"`
- `borrowed` — boolean

Distribution target: ~500 total, ~100 per advType, spread across easy/medium/hard within each type.

**advType definitions:**
- `manner` — describes how an action is done (quickly, carefully, boldly)
- `time` — describes when (yesterday, soon, already, now)
- `place` — describes where (here, nearby, everywhere, upstairs)
- `degree` — describes how much/intensity (very, quite, almost, barely)
- `frequency` — describes how often (always, rarely, sometimes, daily)

---

## 2. Engine Change — `tool-engine.js`

Add `advTypeId` support following the exact `adjTypeId` pattern. Three insertions:

**Config mapping** (~line 648):
```js
advTypeId: cfg.advTypeId || null,
```

**Filter retrieval** (~line 275, alongside adjType):
```js
const advType = config.advTypeId ? (document.getElementById(config.advTypeId)?.value || 'all') : null;
```

**Filter logic** (~line 285, alongside adjType check):
```js
if (advType && advType !== 'all' && w.advType !== advType) return false;
```

Bump `?v=N` in all tool pages that reference `tool-engine.js` and `tool-engine.min.js`. Rebuild minified copy.

---

## 3. Tool Page — `random-adverb-generator.html`

### CONFIG block
```json
{ "url": "/random-adverb-generator/", "output": "random-adverb-generator.html", "type": "tool" }
```

### SLOT:meta
- `<title>Random Adverb Generator — Free Online Tool | Wordineer</title>`
- Meta description: ~155 chars covering adverb types, definitions, filters
- Canonical: `https://wordineer.com/random-adverb-generator/`
- JSON-LD: `WebApplication` schema

### SLOT:hero
Breadcrumb:
```html
<div class="breadcrumb">
  <div class="breadcrumb-inner">
    <a href="/">Wordineer</a>
    <span class="breadcrumb-sep">›</span>
    <a href="/word-tools/">Word Tools</a>
    <span class="breadcrumb-sep">›</span>
    <span aria-current="page">Random Adverb Generator</span>
  </div>
</div>
```
Followed by `<h1>` and short intro paragraph.

### SLOT:tool
Controls sidebar:
- Count input (1–50, default 10)
- Adverb Type select: All / Manner / Time / Place / Degree / Frequency
- Difficulty select: All / Easy / Medium / Hard
- First Letter select: All / A–Z
- Show Definitions toggle (checkbox)
- Sort A–Z toggle (checkbox)

Below results list:
- **Copy All** button — copies all visible words (word + definition if definitions are on, word-only otherwise), one per line

Word list container: `<ul id="word-list">`

### SLOT:init
```js
WORDINEER.init({
  listId:        'word-list',
  countId:       'ctrl-count',
  countDisplayId:'word-count',
  typeId:        'ctrl-type',
  advTypeId:     'ctrl-adverb-type',
  diffId:        'ctrl-diff',
  firstId:       'ctrl-first',
  defsId:        'ctrl-defs',
  dataUrl:       '/data/adverbs.json',
});
```

Copy All button logic (inline script):
- Reads all rendered `.word-item` text nodes
- If definitions visible, includes `word — definition` per line
- Uses `navigator.clipboard.writeText()`

### SLOT:explainer (~700 words across h2 sections)

1. **What Is a Random Adverb Generator?**  
   Defines the tool, explains it generates random English adverbs with optional definitions and filtering by type/difficulty/letter.

2. **Why Use a Random Adverb Generator?**  
   Use cases: writers seeking variety, ESL learners expanding vocabulary, teachers making exercises, game players needing prompts, students studying grammar.

3. **The 5 Types of Adverbs Explained**  
   Table or short paragraphs for each: Manner, Time, Place, Degree, Frequency — with 3 examples each and a sentence showing usage.

4. **How It Works**  
   Step-by-step: choose type/difficulty/letter → set count → generate → toggle definitions → Copy All.

5. **Best Practices for Using Adverbs**  
   Use strong adverbs over weak ones, avoid -ly overuse, vary types, let verbs do the work where possible.

6. **How to Avoid Adverb Overuse**  
   Practical tips: replace adverb+weak-verb with a strong verb, read aloud, use sparingly for emphasis.

### SLOT:faq (5–6 items, ~300 words)

1. What's the difference between an adverb and an adjective?
2. Can adverbs modify other adverbs?
3. Why should I vary the adverbs I use?
4. How does the difficulty filter work?
5. What does the adverb type filter do?
6. Is this tool free to use?

### SLOT:who (~100 words)
- Creative writers and novelists
- Students and ESL learners
- Teachers building vocabulary exercises
- Word game and trivia players
- Editors and proofreaders

---

## 4. word-tools.html — Activate Placeholder

Find:
```html
<div class="tool-name">Random Adverbs <span class="soon-badge">Coming soon</span></div>
```

Replace with an active link (matching the pattern of other activated tools in the file).

---

## 5. tools.json — Registry Entries

Add to all relevant sections:
- `mega` — Writing & Vocabulary group
- `more_word_tools` — tools grid
- `footer_cols` — footer links

Entry shape (match existing entries):
```json
{ "label": "Random Adverb Generator", "url": "/random-adverb-generator/" }
```

---

## 6. Build & Deploy

```bash
cd template-deploy && python3 build.py
cp template-deploy/output/random-adverb-generator.html wordineer-deploy/
cd wordineer-deploy && python3 -m http.server 8080
```

Verify:
- Tool generates adverbs on load
- All 5 type filters return correct subsets
- Difficulty + first letter filters combine correctly
- Definitions toggle shows/hides defs
- Sort A–Z reorders list
- Copy All copies correct text to clipboard
- Breadcrumb renders and links correctly
- word-tools hub links to the new page
- No console errors

---

## Competitor Differentiation Summary

| Feature | Wordineer | RandomLists | AppZaza | TechWelkin | GeneratorsList |
|---------|-----------|-------------|---------|------------|----------------|
| Definitions | ✅ | ❌ | ❌ | ❌ | ❌ |
| Adverb type filter | ✅ | ❌ | ❌ | ❌ | ❌ |
| Difficulty filter | ✅ | ❌ | ❌ | ❌ | ❌ |
| First letter filter | ✅ | ❌ | ❌ | ❌ | ❌ |
| Copy All | ✅ | ❌ | ✅ | ✅ | ❌ |
| Count control | ✅ (1–50) | ❌ | ✅ | ✅ | ✅ (max 20) |
| Sort A–Z | ✅ | ❌ | ✅ | ❌ | ❌ |

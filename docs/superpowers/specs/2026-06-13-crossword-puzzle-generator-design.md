# Crossword Puzzle Generator — Design Spec

**Date:** 2026-06-13  
**Status:** Approved  

---

## Context

Wordineer has a "Coming soon" placeholder for a Crossword Puzzle Generator in the Word Games section of `/word-tools/`. No single competitor delivers all of: custom input + auto-generate, print output + browser solve mode, and shareable URL encoding — all client-side with no account required. That combination is the differentiation angle.

**Target users:** Teachers (primary), students, parents/homeschoolers, game night hosts.

---

## Architecture

**Tool type:** `type: tool` (full layout with nav/grids/ads/footer)  
**URL:** `/crossword-puzzle-generator/` (trailing-slash canonical)  
**Source file:** `template-deploy/tools-src/crossword-puzzle-generator.html`  
**Data file:** `wordineer-deploy/data/crossword-words.json`  

### Grid Layout Algorithm (pure JS, no library)

1. Sort words by length descending
2. Place longest word horizontally at grid center
3. For each remaining word: scan placed words for shared letters → score candidate placements by grid compactness (maximize intersections, minimize grid expansion)
4. Place at best-scoring position; fall back to standalone placement if no intersection found
5. Output: 2D grid array + word-position list `{word, x, y, dir:"across"|"down", num}`

### Input Modes (tab-switched)

- **Auto-Generate:** difficulty dropdown (Easy / Medium / Hard) + category dropdown (Animals, Science, Geography, Food, Sports, School, Nature, Technology) → pulls from `crossword-words.json`
- **Custom Puzzle:** textarea, one `word, clue` per line → parsed, runs same algorithm

### Grid Rendering

HTML `<table>` — black `td` for blocked cells, white for letter cells. Clue numbers appear as superscripts in the top-left corner of numbered cells. Across/Down clue lists rendered as `<ol>` beside the grid.

### Output Modes

| Mode | Mechanism |
|------|-----------|
| Print (blank) | `window.print()` + `@media print` CSS; letters hidden before printing |
| Print (answer key) | Toggle shows filled letters; then print |
| Solve in Browser | Cells become `<input maxlength="1">`; click selects word; double-click/Tab toggles direction; arrow keys navigate; Check Answers gives green/red feedback; Reveal All fills correct letters |
| Share | Serialize `{words:[{w,c,x,y,dir,num}], title}` → JSON → `btoa()` → URL hash; on load detect hash and restore |

### Data File — `crossword-words.json`

```json
{
  "easy": {
    "animals": [{"w":"CAT","c":"A furry pet that purrs"}],
    "science": [],
    "geography": [],
    "food": [],
    "sports": [],
    "school": [],
    "nature": [],
    "technology": []
  },
  "medium": { ... },
  "hard": { ... }
}
```

~400 words total. Words 3–12 letters, uppercase. Clues ≤80 chars.

---

## UI Layout

### Breadcrumb
3-level: `Wordineer › Word Tools › Crossword Puzzle Generator`  
Pattern from `password-generator.html`:
```html
<div class="breadcrumb">
  <div class="breadcrumb-inner">
    <a href="/">Wordineer</a>
    <span class="breadcrumb-sep">›</span>
    <a href="/word-tools/">Word Tools</a>
    <span class="breadcrumb-sep">›</span>
    <span aria-current="page">Crossword Puzzle Generator</span>
  </div>
</div>
```

### Hero
Badge "Word Games" + H1 "Crossword Puzzle Generator" + value prop sentence.

### Tool Panel
```
┌─────────────────────────────────────────────────┐
│  [Auto-Generate ▸]  [Custom Puzzle]   ← tabs    │
│                                                 │
│  Auto: [Easy ▼ Difficulty] [Animals ▼ Category] │
│  Custom: textarea ("word, clue" one per line)   │
│                                                 │
│  [Generate Crossword]   [Clear]                 │
├─────────────────────────────────────────────────┤
│  GRID (table)          │  CLUES                 │
│  black/white cells     │  Across: 1. 2. 3. ...  │
│  with clue numbers     │  Down: 1. 2. 3. ...    │
│                        │                        │
│  [Print] [Answer Key ☐] [Solve] [Share]         │
└─────────────────────────────────────────────────┘
```

### Content Area Style
Matches `password-generator.html`:
- `<h2>` section headings
- `<p>` body paragraphs
- `.faq-item` / `.faq-q` / `.faq-a` for FAQ accordion
- `.uc-grid` / `.uc` / `.uc-title` / `.uc-body` for "who uses" cards

---

## Copy Plan

### Explainer (~620 words across 4 sub-sections)

1. **What is a Crossword Puzzle Generator?** (~150w) — defines the tool, who it's for, what it produces
2. **Why Use a Crossword Puzzle Generator?** (~150w) — vocabulary recall, spelling, engagement, speed vs. making by hand
3. **How It Works** (~120w) — step-by-step: choose mode → enter/select words → Generate → print or share link
4. **Best Practices for Better Crosswords** (~200w) — ideal word length (4–12 letters), writing good clues, optimal word count (10–20), mixing short and long words for grid density

### FAQ (~400 words, 8 questions)

1. How many words can I add to a crossword?
2. What happens if some of my words don't intersect?
3. What's the difference between Easy, Medium, and Hard mode?
4. How do I share my puzzle with students or friends?
5. Can I print a blank version without the answers showing?
6. Does my puzzle get saved anywhere?
7. Can I use proper nouns or multi-word phrases?
8. What's the ideal grid size for a classroom puzzle?

### Who Uses This (~100 words, 4 cards)

- Teachers — vocabulary review, test prep, classroom engagement
- Students — self-quizzing, making puzzles for friends
- Parents & Homeschoolers — custom lesson supplements at home
- Game Night Hosts — custom-topic party puzzles

---

## Integration Points

### word-tools.html (lines 360–364)
Replace `tool-item--soon` div with active `<a>`:
```html
<a href="/crossword-puzzle-generator/" class="tool-item">
  <div class="tool-icon" style="background:#EAF0F6"><!-- existing SVG --></div>
  <div class="tool-name">Crossword Puzzle Generator</div>
  <div class="tool-desc">Crossword-style prompts and puzzle ideas for solo play or classrooms.</div>
</a>
```

### tools.json
Add to `mega`, word games section, and `footer_cols`.

### _redirects
```
/crossword-puzzle-generator.html    /crossword-puzzle-generator/    301
/crossword-puzzle-generator/        /crossword-puzzle-generator.html    200
```

### sitemap.xml
```xml
<url>
  <loc>https://wordineer.com/crossword-puzzle-generator/</loc>
  <lastmod>2026-06-13</lastmod>
  <changefreq>monthly</changefreq>
  <priority>0.9</priority>
</url>
```

---

## Verification Checklist

- [ ] Auto-generate: difficulty + category → valid grid with no cell conflicts
- [ ] Custom mode: 10 word/clue pairs → crossword renders correctly
- [ ] Clue numbers match across/down lists
- [ ] Print blank: letters hidden, grid intact
- [ ] Print answer key: letters visible
- [ ] Solve mode: inputs editable, arrow key nav works, Check Answers gives color feedback
- [ ] Share: URL hash encodes puzzle; loading hash URL restores exact puzzle
- [ ] Breadcrumb: 3-level, matches password-generator style
- [ ] word-tools: link active, no "Coming soon" badge
- [ ] _redirects: clean URL resolves locally
- [ ] sitemap.xml: entry present
- [ ] PageSpeed: no load-time autofocus, word data deferred

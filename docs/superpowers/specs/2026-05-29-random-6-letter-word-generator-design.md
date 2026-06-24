# Design: Random 6 Letter Word Generator

**Date:** 2026-05-29
**Status:** Awaiting implementation

---

## Context

Wordineer already has 3, 4, and 5-letter word generator tools. Adding a 6-letter generator completes the core set and targets a high-intent audience: crossword solvers (6-letter slots are among the most common in standard crosswords), Scrabble players (6-letter words often score 15–30+ pts with bingo potential), and writers. Competitors (word.tips, dictionary.com) cover the space but leave gaps: no copy-to-clipboard, no educational content, no crossword-specific helper. This tool fills those gaps using the proven Wordineer pattern.

---

## Prerequisites

### New Data File Required
`wordineer-deploy/data/six-letter-words.json` — does not exist yet. Must be created before the tool can function.

**Schema** (same as all word data files):
```json
{ "w": "Garden", "t": "noun", "d": "a plot of ground for growing plants", "diff": "easy" }
```

- `w`: 6-letter word (capitalized)
- `t`: `"noun"` | `"adjective"` | `"verb"` | `"adverb"`
- `d`: definition ≤100 chars
- `diff`: `"easy"` | `"medium"` | `"hard"`

**Target size:** 2,000–3,000 curated entries (matches density of 4/5-letter sets)

**Distribution target:**
- Easy: ~30% (common everyday words)
- Medium: ~45% (less frequent but recognizable)
- Hard: ~25% (uncommon, advanced vocabulary)

---

## Feature Set

### Standard Controls (identical to 3/4/5-letter tools)
| Control | Values |
|---------|--------|
| Number of words | 1–50, default 20 |
| Word type | All / Noun / Adjective / Verb / Adverb |
| Difficulty | All / Easy / Medium / Hard |
| Starts with | Single letter A–Z |
| Ends with | Single letter A–Z |
| Show definitions | Toggle checkbox |
| Copy format | One per line / Comma-separated / Space-separated |
| Save words | Heart icon per word |
| Keyboard shortcut | Space to regenerate |

### Game Helper Mode (new — mirrors 5-letter Wordle helper)
- **Contains letter** — single letter input; filters to words containing that letter
- **Does NOT contain** — single letter input; excludes words with that letter
- **Label:** "Crossword & Word Game Helper"
- **Use cases:** Crossword slot solving, Wordle 6 / Canuckle / Squabble variants

### Results Panel
- Word count: "Showing X of Y matching words"
- Regenerate button
- Per-word: word text, type badge, difficulty badge (color-coded), Scrabble score badge ("14 pts"), optional definition, heart (save), copy icon
- Sort dropdown: Default / A–Z / Z–A / Scrabble Score ↓
- Saved words panel with bulk copy

### A-Z Browse Links
Footer links to `/6-letter-words-starting-with-{letter}/` for all 26 letters (consistent with 3/4/5-letter pattern; these pages to be built separately).

### Scrabble Score Display (new — unique vs. competitors)
- Each word shows its total Scrabble point value as a badge (e.g. "14 pts")
- **Sort by Scrabble score** dropdown option added to results panel (alongside existing A-Z sort)
- Score computed client-side using standard tile values:
  - 1 pt: A E I O U L N S T R
  - 2 pts: D G
  - 3 pts: B C M P
  - 4 pts: F H V W Y
  - 5 pts: K
  - 8 pts: J X
  - 10 pts: Q Z
- `scoreWord(w)` helper function: sums letter values for a word string
- Results panel sort options: Default (random) / A–Z / Z–A / Scrabble Score ↓
- Scrabble tip in explainer updated: "Use the Scrabble Score sort to surface the highest-value plays instantly"

### Out of Scope (this version)
- Per-letter JSON splits (`six-letter-words-a.json` etc.) — add if dataset grows large enough to warrant it
- Export / CSV download

---

## UI Layout

Identical to existing letter-length tools:
- **Left sidebar** (230px): control panel with all filters + game helper + generate/reset buttons
- **Right panel**: results with copy dropdown, word list, saved words
- **Mobile**: "More options" toggle collapses advanced filters
- **Below tool**: A-Z browse links

Reference files for layout/CSS/JS patterns:
- `template-deploy/tools-src/random-5-letter-word-generator.html` (closest match — has game helper)
- `template-deploy/tools-src/random-4-letter-word-generator.html` (standard filter pattern)

---

## Page Structure

**File:** `template-deploy/tools-src/random-6-letter-word-generator.html`

**Config:**
```json
{
  "url": "/random-6-letter-word-generator/",
  "output": "random-6-letter-word-generator.html"
}
```

### Slot: `meta`
- Title: `Random 6 Letter Word Generator | Wordineer`
- Description: Generate random 6-letter words instantly. Filter by type, difficulty, or starting letter. Includes crossword & word game helper mode.
- Canonical: `https://wordineer.com/random-6-letter-word-generator/`
- JSON-LD: SoftwareApplication schema (same pattern as other tools)

### Slot: `hero`
- Breadcrumb: Home → Word Tools → Random 6 Letter Word Generator
- Badge: "Free · No sign-up · Instant results"
- H1: "Random 6 Letter Word Generator"
- Subhead: "Generate random 6-letter words instantly. Filter by type, difficulty, or starting and ending letter — or use Crossword & Game Helper mode to narrow candidates by known and excluded letters."

### Slot: `tool`
Full tool UI (sidebar + results). See Feature Set above.

### Slot: `explainer`
Four subsections (~600 words total):

1. **What is a 6 letter word generator?** (~130 words)
   - Defines the tool: random selection from curated 6-letter English word dataset
   - Filters: type, difficulty, letter position, game helper
   - Positions it for games, writing, and learning
   - Notes instant load (seed) + async full dataset

2. **Why use a 6 letter word generator?** (~300 words, 5 subsections)
   - *Word games & Scrabble*: 6-letter words score 15–30+ pts; one away from a 7-letter bingo (+50 pts); examples of high-value plays
   - *Crossword solving*: 6-letter slots are the most common length in standard American crosswords; Game Helper lets you pin starts-with + contains to crack a clue fast
   - *Creative writing & naming*: sweet spot between meaning and brevity; strong for brand names, product names, character names, headlines
   - *Vocabulary building*: mid-length words are easiest to retain; definitions + type context accelerates learning
   - *Teaching & classroom*: spelling tests, vocabulary drills, literacy exercises for upper-elementary and middle school

3. **How it works** (~100 words)
   - Seed words load instantly (no wait on page load)
   - Full dataset loads async at browser idle or first user action
   - All filters apply client-side (no server round-trips)
   - Game Helper narrows pool by letter inclusion/exclusion before random pick

4. **Tips for getting the most out of this tool** (~100 words, 4 bullets)
   - Crossword: combine Starts With + Contains to pin a specific slot
   - Scrabble: use "Sort by Scrabble Score" to surface highest-value plays instantly; filter Hard + Noun for uncommon big scorers
   - Writing: set type to Adjective + Easy for punchy, clean descriptors
   - Teacher: set count to 10 + Easy + Noun for manageable weekly spelling lists

### Slot: `faq`
Six Q&As (~300 words):

1. **What is a 6 letter word generator?** — Tool definition, filters, free use
2. **How many 6-letter words are in English?** — ~17,000–22,000 total; this tool's curated dataset ~2,000–3,000
3. **What does the difficulty rating mean?** — Easy (everyday words), Medium (less frequent but recognizable), Hard (uncommon, advanced)
4. **Can I use this for Scrabble or crosswords?** — Yes; Game Helper mode + difficulty filter for Scrabble; starts-with + contains for crossword slots
5. **How does Game Helper mode work?** — Enter a letter in "Contains" to require it; enter a letter in "Does NOT contain" to exclude it; combine with other filters
6. **Is this tool free?** — Completely free, forever. No account, no limits, no paywalls.

### Slot: `who`
Four cards:
1. **Word game players** — Scrabble, crosswords, Wordle 6, Canuckle
2. **Writers & creatives** — naming, fiction, copywriting, headlines
3. **Students & learners** — vocabulary building, spelling practice
4. **Teachers & educators** — lesson planning, spelling lists, vocabulary drills

### Slot: `init`
JavaScript following the 5-letter tool pattern exactly:
- SEED array: ~25 common 6-letter words (embedded for instant render)
- `allWords` → async fetch from `/data/six-letter-words.json`
- `getFiltered()`: type, difficulty, starts/ends with, contains, excludes
- `pickRandom(pool, n)`: Fisher-Yates shuffle
- `scoreWord(w)`: sums standard Scrabble tile values for a word string
- `renderList()`: word items with badges (type, difficulty, Scrabble score), definitions, save/copy buttons
- `sortWords(words, mode)`: sorts by default (random order), A–Z, Z–A, or Scrabble score descending
- `validateAndGenerate()`: validation + render
- Event listeners: Generate, Regenerate, Reset, filter changes, Space key, mobile toggle, copy dropdown, save/unsave, copy single word

---

## Redirects

Add to `wordineer-deploy/_redirects`:
```
/random-6-letter-word-generator   /random-6-letter-word-generator/   301
```

---

## tools.json Updates

Add to all four relevant sections:
- `mega` (nav mega-menu)
- `more_word_tools` (tools grid)
- `other_tools`
- `footer_cols`

---

## Build & Deploy Steps

1. Create `wordineer-deploy/data/six-letter-words.json` (2,000–3,000 words)
2. Create `template-deploy/tools-src/random-6-letter-word-generator.html`
3. Update `template-deploy/tools.json` (4 sections)
4. Add redirect to `wordineer-deploy/_redirects`
5. Run `cd template-deploy && python3 build.py`
6. Copy output: `cp template-deploy/output/random-6-letter-word-generator.html wordineer-deploy/`
7. Preview locally: `cd wordineer-deploy && python3 -m http.server 8080`
8. Verify: generate words, test all filters, test game helper, test copy, test save, test mobile

---

## Verification Checklist

- [ ] Page loads instantly (seed words appear before any fetch)
- [ ] Full dataset loads async (word count increases after ~800ms)
- [ ] All filters work: type, difficulty, starts with, ends with
- [ ] Game Helper: contains letter filters correctly
- [ ] Game Helper: excludes letter filters correctly
- [ ] Scrabble score badge displays on every word
- [ ] Sort by Scrabble Score orders results high → low correctly
- [ ] `scoreWord()` returns correct value (e.g. "QUARTZ" = 24)
- [ ] Copy formats: line / comma / space all produce correct output
- [ ] Save words: add and remove words, bulk copy works
- [ ] Space key regenerates results
- [ ] Mobile: "More options" toggle shows/hides advanced filters
- [ ] A-Z browse links render (even if target pages don't exist yet)
- [ ] PageSpeed: no forced reflow warnings, no autofocus on load
- [ ] tools.json: tool appears in nav mega-menu and footer

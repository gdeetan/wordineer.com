# Design Spec: Random Wordle Generator

**Date:** 2026-06-08  
**URL:** `/random-wordle-generator/`  
**Output file:** `template-deploy/tools-src/random-wordle-generator.html`  
**Type:** `tool` (full layout with nav/grids/ads/footer)

---

## Context

Users searching for "random Wordle word", "5 letter word generator Wordle", and "Wordle starting words" land on game sites or very thin tools. Wordineer is missing this SEO surface. The tool is a clean, filter-driven 5-letter word generator specifically positioned for Wordle players — same generator pattern as existing tools, Wordle-branded copy. No custom puzzle builder, no game elements, no backend needed.

---

## Tool UI

### Layout
Split-panel layout matching `random-weird-words.html` and `random-5-letter-word-generator.html`:
- Left: `.ctrl` panel (controls)
- Right: `.words-panel` (results)

### Left ctrl panel
| Control | Type | Default | Options |
|---|---|---|---|
| How many words | number input | 5 | 1–10 |
| Difficulty | select | All levels | All / Easy (common) / Medium / Hard/rare |
| Starts with letter | text input | empty | A–Z (optional), maxlength=1 |
| Generate button | button | — | Primary CTA |

Keyboard: Enter / Space triggers generate (same hook as other tools).

### Right results panel
- Each result: large word display (`<span class="word-text">`) + definition below (`<p class="word-def">`)
- Copy icon per word — copies the word only (not definition) to clipboard
- "Copy all words" button at top of panel (copies newline-separated word list)
- Empty state: "Click Generate to get Wordle words" placeholder

### Breadcrumb
```html
<div class="breadcrumb">
  <div class="breadcrumb-inner">
    <a href="/">Wordineer</a>
    <span class="breadcrumb-sep">›</span>
    <a href="/word-tools/">Word Tools</a>
    <span class="breadcrumb-sep">›</span>
    <span aria-current="page">Random Wordle Generator</span>
  </div>
</div>
```

---

## Data

**Source:** `words_expanded.json` — same fetch pattern as `random-5-letter-word-generator.html`.  
**Filter:** `w.length === 5` (client-side, post-fetch).  
**Schema fields used:** `w` (word), `d` (definition), `diff` (difficulty: easy/medium/hard).  
No new data file needed.

**Seed words:** Inline a small set of 5-letter seed words in the init script (same SEED pattern as `tool-engine.js`) so the tool renders immediately without waiting for the JSON fetch.

---

## SEO / Meta

```
Title:       Random Wordle Word Generator — 5-Letter Words | Wordineer
Description: Generate random 5-letter words for Wordle. Filter by difficulty and starting letter. Free, instant, no sign-up.
Canonical:   https://wordineer.com/random-wordle-generator/
H1:          Random Wordle Word Generator
```

JSON-LD schema: `WebApplication` type (same as other tool pages).

---

## Copy Structure (~1,300+ words)

### Explainer slot

#### What is a Random Wordle Generator?
~150 words. Explains: tool picks random valid 5-letter English words from a curated dataset. Each word comes with its definition. Users can filter by difficulty and starting letter. Works instantly in the browser — no download, no account. Differentiates from full Wordle games: this is a word source, not the game itself.

#### Why Use a Random Wordle Generator?
~200 words. Cover:
- Breaking the "same 3 starting words every day" habit (CRANE, STARE, IRATE)
- Discovering vocabulary you didn't know: 5-letter words with clear definitions
- Warm-up practice: generate 5 words, try to mentally Wordle each one before playing
- Teachers: turns vocabulary practice into a familiar game format
- Writers: random 5-letter words as creative constraints/prompts
- Hosting a Wordle challenge: generate a hard word to text your friends, see who gets it

#### How This Tool Works
~100 words. Explains the data pipeline (curated word list → filter by length/difficulty/letter → display with definition). Covers the difficulty levels: easy words appear in everyday conversation, medium are less common, hard are rare or specialized.

#### How Does Wordle Work? (Quick Refresher)
~150 words. Brief rules for context — 5-letter word, 6 guesses, green/yellow/gray tile logic. Written for someone who has heard of Wordle but wants a refresher. Closes with: your starting word matters more than most players realize, which is why a word generator helps.

#### Best Starting Words for Wordle
~250 words. The SEO gold section. Cover:
- What makes a strong starting word: covers high-frequency letters (E, T, A, R, I, O, N, S, L, C), hits multiple vowels, avoids repeated letters
- Example strong starters: CRANE, SLATE, TRACE, STARE, RAISE, AUDIO, ADIEU
- Avoid weak starters: repeated letters, rare consonants, Q/Z/X/J-heavy words
- Strategy tip: vary your starter — using the same word daily makes you pattern-match to that word's letter positions, not the puzzle. Use this generator to rotate.
- Hard mode tip: generate a harder word as your starter to force yourself to think about uncommon letters

#### Best Practices
~150 words. Practical usage tips:
- Generate 5 words at once and pick the one that feels right for today
- Use "Easy" difficulty if you're new to Wordle, "Hard" if you want a challenge
- Filter by a specific starting letter to practice a letter cluster you find tricky
- Use as a vocabulary builder: look up each word's definition before playing
- Generate before your daily Wordle as a warm-up, not as a spoiler

### FAQ slot (5 questions, ~300 words total)

1. **What makes a good Wordle word?** — 5 letters, valid English word in Wordle's dictionary, no repeated letters ideally, contains common letters
2. **Can I use any 5-letter word in Wordle?** — No, Wordle uses a specific word list. Not all 5-letter words are valid guesses. This tool draws from a broad English word dataset — most words will be valid, but obscure ones may not be in Wordle's list.
3. **What's the difference between easy and hard words in this tool?** — Easy = common everyday words (PLANT, CRANE, STORM). Hard = rare, technical, or unusual (PSALM, THYME, FJORD). Hard-difficulty words are more likely to stump your opponent.
4. **How many 5-letter words are there in English?** — Thousands. The standard Wordle answer list has ~2,300 words; the valid-guess list has ~10,000+. This generator draws from a curated subset optimized for clarity.
5. **What's the single best Wordle strategy?** — Cover as many of the 12 most common English letters (E, T, A, R, I, O, N, S, L, C, U, D) as possible in your first two guesses. CRANE + TOILS, for example, hits 10 of those 12 in two words.

### Who Uses This Tool section

4 use-case cards (matching site pattern):
- **Daily Wordle players** — rotate starting words, avoid ruts
- **Teachers** — 5-letter vocab practice that students actually want to do
- **Word game enthusiasts** — Quordle, Dordle, Wordle variants all need 5-letter starting words
- **Writers** — 5-letter word constraints for creative exercises and naming

---

## Integration Points

### `template-deploy/tools-src/word-tools.html`
Add a new `<a class="tool-item">` card in the **"Random word generators"** section, after the existing random-N-letter-word links:

```html
<a class="tool-item" href="/random-wordle-generator/">
  <div class="tool-icon" style="background:#E8F4FE"><svg viewBox="0 0 13 13" fill="none"><rect x="2" y="2" width="3.5" height="3.5" rx="0.5" fill="#2B7FD4"/><rect x="7.5" y="2" width="3.5" height="3.5" rx="0.5" fill="#2B7FD4" opacity=".4"/><rect x="2" y="7.5" width="3.5" height="3.5" rx="0.5" fill="#2B7FD4" opacity=".4"/><rect x="7.5" y="7.5" width="3.5" height="3.5" rx="0.5" fill="#2B7FD4"/></svg></div>
  <div class="tool-name">Random Wordle Generator</div>
  <div class="tool-desc">Random 5-letter words for Wordle practice. Filter by difficulty and starting letter.</div>
</a>
```

### `template-deploy/tools.json`
Add to:
- `mega` → "Writing & Vocabulary" category: `{ "href": "/random-wordle-generator/", "text": "Random Wordle Generator" }`
- `more_word_tools` grid
- `footer_cols` (word tools column)

### `wordineer-deploy/_redirects`
```
/random-wordle-generator/ /random-wordle-generator.html 200
```

---

## Verification

1. `cd template-deploy && python3 build.py` — no errors, `output/random-wordle-generator.html` generated
2. `cp template-deploy/output/random-wordle-generator.html wordineer-deploy/`
3. `cd wordineer-deploy && python3 -m http.server 8080`
4. Open `http://localhost:8080/random-wordle-generator.html`
5. Verify:
   - Tool renders immediately (seed words visible before JSON loads)
   - All filters work: difficulty, starts-with, count
   - Generate button works; Enter/Space keyboard shortcut works
   - Copy-per-word and copy-all work
   - Breadcrumb shows correct path
   - Explainer and FAQ sections render correctly
   - Word Tools hub link (`/word-tools/`) shows the new card
   - `_redirects` entry present

---

## Files to Create / Modify

| Action | File |
|---|---|
| **Create** | `template-deploy/tools-src/random-wordle-generator.html` |
| **Modify** | `template-deploy/tools-src/word-tools.html` |
| **Modify** | `template-deploy/tools.json` |
| **Modify** | `wordineer-deploy/_redirects` |
| Build + copy | `template-deploy/output/random-wordle-generator.html` → `wordineer-deploy/` |

**Key patterns to reuse:**
- Breadcrumb: `template-deploy/tools-src/random-weird-words.html` lines 206-214
- Tool split-panel layout: `template-deploy/tools-src/random-weird-words.html`
- Data fetch + 5-letter filter: `template-deploy/tools-src/random-5-letter-word-generator.html`
- Copy-all pattern: any existing tool with multi-word output

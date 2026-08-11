# Scrabble Word Finder — Design Spec

**Date:** 2026-08-11
**Status:** Approved
**URL:** `/scrabble-word-finder/`
**Output:** `scrabble-word-finder.html`
**Type:** tool

---

## Overview

A Scrabble Word Finder / Anagram Solver that finds all valid words formable from a set of input letters. Distinct from the existing Word Unscramble tool (`/word-unscramble/`) via SEO targeting ("scrabble word finder", "anagram solver") and a sortable-table results UI that prioritises Scrabble point value. Shares the same codebase patterns and CSS conventions as all other Wordineer tool pages.

---

## Architecture

### File structure
- `template-deploy/tools-src/scrabble-word-finder.html` — source file (CONFIG + SLOT pattern, type: tool)
- No new data files — combine existing `dictionary.json` + `words_expanded.json` at runtime

### Data loading
- Deferred fetch at page idle (same pattern as word-unscramble and rhyming-dictionary)
- Primary source: `GET /data/dictionary.json` — provides words + definitions
- Supplement: `GET /data/words_expanded.json` — adds coverage
- Deduplicate by lowercase word string after both loads complete
- Scrabble scores computed client-side from TILE map (same values as word-unscramble)

### Word matching algorithm
- Same `canFormWord(word, inputCounts, wildcards)` logic as word-unscramble
- `?` = wildcard (blank tile), each counts as one character toward 15-letter limit
- Runs synchronously over the in-memory word array on Find

---

## UI

### Input
- Single text input, up to 15 characters (letters + `?`)
- **Find Words** button + Enter key trigger
- Clear button (×)

### Filters panel (collapsible on mobile)
- **Word length:** Any / 2–3 / 4–5 / 6–7 / 8+ letters
- **Min points:** Any / 5+ / 10+ / 15+
- **Starts with:** text input (1–3 chars)
- **Ends with:** text input (1–3 chars)
- **Must contain:** text input (1–3 chars)
- **Dictionary label:** NWL / SOWPODS / WWF — cosmetic toggle only (same underlying wordlist; explained in FAQ)

### Results table
Columns: **Word** | **Length** | **Points** | **Definition** | **Copy**

- Default sort: Points descending (highest-scoring words first)
- Sort toggle buttons above table: **Points ↓** / **Length ↓** / **A–Z**
- Definition: tooltip on hover (desktop), tap-to-reveal (mobile); sourced from dictionary.json entry if available, blank otherwise
- Copy button per row: copies just the word to clipboard
- **Copy all words** button above table: copies newline-separated word list
- Result count shown: "Found 47 words"
- Empty state: "No words found — try removing a filter or adding a wildcard (?)"
- Loading state: spinner until dictionary fetch completes

### Word display
- Each word in the table is lowercase
- Points badge styled consistently with site colour tokens
- Table is responsive: on mobile, Definition column is hidden; tap a row to expand definition inline

---

## SEO

### Meta
- **Title:** `Scrabble Word Finder — Find Every Word from Your Letters | Wordineer`
- **Description:** `Enter your Scrabble tiles and instantly find every valid word, sorted by point value. Supports blank tiles (?), filters by length and score. Free anagram solver.`
- **Canonical:** `https://wordineer.com/scrabble-word-finder/`
- **Schema:** `WebApplication` + `FAQPage`
- **Breadcrumb:** Home › Word Tools › Scrabble Word Finder

### Target keywords
- "scrabble word finder" (primary)
- "anagram solver"
- "unscramble letters scrabble"
- "words from letters scrabble"

### FAQ topics
1. How do I find Scrabble words from my letters?
2. What does the ? wildcard do?
3. Which dictionary does this use? (explains NWL/SOWPODS/WWF cosmetic toggle)
4. How are Scrabble points calculated?
5. What's the difference between this and the Word Unscramble tool?

### Internal links
- Word Unscramble (`/word-unscramble/`)
- 5-Letter Words (`/5-letter-words/`)
- Word Lists hub (`/word-lists/`)
- Random Word Generator (`/`)

---

## tools.json placement

- **mega:** Add to `Writing & Vocabulary` category (replace lowest-priority item if at 4-tool limit)
- **footer_cols:** Add to word tools column
- **more_word_tools:** Add entry

---

## Constraints

- No frameworks; vanilla JS only
- Follow existing CSS variable tokens (`--brand`, `--brand-dark`, etc.) — no new colour values
- Tool section width must match content area (same as other tool pages)
- Font, margins, spacing must match site style (copy from word-unscramble as base)
- Deferred data load — tool shows input UI immediately; results only after dictionary loaded
- FAQ must use JS-driven div accordion pattern (not `<details>`/`<summary>`)
- First FAQ item gets class `open`; every `.faq-q` needs chevron SVG
- `?v=N` cache-bust not needed (no changes to existing versioned assets)

---

## Out of scope

- Full board layout / Scrabble board solver
- Real dictionary validation per-game (NWL/SOWPODS/WWF toggle is cosmetic)
- User accounts or saved word lists
- Multiplayer or session tracking

# Design: Session 3 & 4 — Dad Jokes, Trivia Generator, Lorem Ipsum Generator

**Date:** 2026-07-15
**Status:** Approved
**Tools:** Random Dad Jokes, Random Trivia Generator, Lorem Ipsum Generator

---

## Context

Sessions 1 & 2 are complete (Scattergories, Catchphrase, Couples Truth or Dare, Writing Prompt Generator, Plot Generator). This spec covers the remaining three tools from the undeployed inventory. Sessions 3 and 4 are treated as a single implementation cycle; tools are independent and can be parallelized.

---

## Shared Conventions (all tools)

- SLOT template system: `meta`, `style`, `hero`, `tool`, `ad_b`, `explainer`, `faq`, `who`, `init`
- CONFIG block: `"type": "tool"` with tool-specific `url` and `output`
- Vanilla JS IIFE per tool in `SLOT:init` — no modifications to `tool-engine.js`
- CSS custom properties only (`var(--brand)`, `var(--bg)`, `var(--text)`, etc.) — no hardcoded color literals
- `fetch('/data/<file>.json')` + embedded SEED fallback if fetch fails
- sessionStorage for no-repeat tracking and favorites
- Register each tool in `tools.json` (mega, more_word_tools or relevant section, footer_cols)
- Replace "Coming soon" card on `/word-tools/` for each tool
- Build via `build.py`, copy output to `wordineer-deploy/`, preview locally before deploying

---

## Tool 1: Random Dad Jokes

**URL:** `/random-dad-jokes/`
**Output:** `random-dad-jokes.html`
**ID prefix:** `dj-`
**Target keywords:** "random dad jokes", "dad joke generator", "clean dad jokes", "dad jokes for kids"

### Data File

`wordineer-deploy/data/dad-jokes.json`

Schema:
```json
{ "q": "Why don't eggs tell jokes?", "a": "They'd crack each other up.", "topic": "food", "format": "qa" }
{ "text": "I used to hate facial hair but then it grew on me.", "topic": "general", "format": "oneliner" }
```

- 250+ entries total
- Topics: `food`, `animals`, `work`, `science`, `sports`, `seasonal`, `general`
- Formats: `qa` (question + punchline reveal), `oneliner` (displayed in full)
- All original, clean, family-safe (advertiser-safe for AdSense/Mediavine)

### UI

Single card layout (follows catchphrase-generator single-card pattern, not truth-or-dare 2-col grid):

- **`qa` format:** Show question text first; "Show Punchline" button reveals answer (increases time-on-page)
- **`oneliner` format:** Full joke displayed immediately
- Controls: topic filter dropdown, Next/Regenerate button, Copy button, Share (Web Share API with `navigator.share` → fallback to clipboard copy), heart/favorites (sessionStorage array), Groan-meter (1–5 tap rating, cosmetic only, stored in sessionStorage per joke ID — purely for fun, no analytics)
- No-repeat within session via sessionStorage Set on joke index

### SEO Copy

- Explainer: what makes a dad joke (groan-worthy wordplay, puns, anticlimax)
- Static "Best Of" section: 10 curated jokes rendered as `<dl><dt>Q:</dt><dd>A:</dd></dl>` pairs in static HTML (not JS-rendered, so crawlers can index them)
- FAQ: 5–6 questions with FAQPage schema
- Internal links: would-you-rather-generator, truth-or-dare-generator, charades-generator

---

## Tool 2: Random Trivia Generator

**URL:** `/random-trivia-generator/`
**Output:** `random-trivia-generator.html`
**ID prefix:** `tv-`
**Target keywords:** "random trivia generator", "trivia question generator", "trivia questions and answers", "trivia night questions"

### Data File

`wordineer-deploy/data/trivia.json`

Schema:
```json
{
  "q": "What is the only letter that does not appear in any U.S. state name?",
  "a": "Q",
  "options": ["Q", "Z", "X", "J"],
  "category": "words",
  "difficulty": "medium"
}
```

- 300+ entries
- Categories: `history`, `geography`, `science`, `entertainment`, `sports`, `food`, `words`, `general`
- Difficulties: `easy`, `medium`, `hard`
- `options` array: 4 choices including correct answer (shuffled at render time, not in data)
- "Words & language" category pulls from Wordineer's vocabulary/etymology angle (etymology, grammar trivia, word origins) — differentiator no competitor has
- Factually uncertain answers (< 95% confidence) flagged in post-build review list for user verification before commit

### UI

**Mode toggle** (segmented control at top of tool):

**Flashcard mode (default):**
- Question card front, tap/click to flip and reveal answer
- Next button, Copy, heart/favorites
- No-repeat per session via sessionStorage Set

**Quiz mode:**
- Multiple choice: 4 buttons rendered from `options` array (shuffled each render)
- Running score display (X / 10)
- 10-question rounds → round-end summary card ("8/10 — Great job!")
- Keyboard shortcuts: `1`/`2`/`3`/`4` to select answer, `Enter` or `Space` to advance
- No-repeat per round, shuffle new set on round restart

**Host mode:**
- Toggled via "Host Mode" button
- Larger type (CSS class swap), keyboard-only navigation
- `Space` = reveal answer, `→` = next question
- Designed for projector/TV display at trivia nights

**Filters:** category multi-select chips, difficulty dropdown — apply to all modes. Every combination must return ≥ 1 result (validated by scripts/validate-data.js).

### SEO Copy

- How to run a trivia night (setup, scoring, round structure)
- Question-writing tips
- Static 10 sample Q&As rendered in HTML for crawlers (separate from JS-rendered cards)
- FAQ with FAQPage schema
- Internal links: word-of-the-day, spelling-bee-words, random-word-generator

---

## Tool 3: Lorem Ipsum Generator

**URL:** `/lorem-ipsum-generator/`
**Output:** `lorem-ipsum-generator.html`
**ID prefix:** `li-`
**Target keywords:** "lorem ipsum generator", "lorem ipsum generator html", "lorem ipsum 3 paragraphs", "lorem ipsum words", "short lorem ipsum", "lorem ipsum alternative"

### Data

No dedicated data file. Generation is algorithmic:
- Latin mode: built-in word bank constant in the IIFE (~200 words from Cicero's *de Finibus*)
- Readable English mode: fetches `sentences.json` (already in `wordineer-deploy/data/`)
- Word Soup mode: fetches `words.json` (already in `wordineer-deploy/data/`)

### UI

**Output controls (left panel or top controls):**
- Unit selector: `Paragraphs` | `Sentences` | `Words` | `Characters` | `List items`
- Count input: 1–50 (paragraphs/sentences), 1–500 (words/chars), 1–20 (list items)
- "Start with 'Lorem ipsum dolor sit amet...'" toggle (on by default)
- Paragraph length: `Short` | `Medium` | `Long`

**Text mode selector:**
- `Classic Latin` (default)
- `Readable English` (from sentences.json — real grammar, no competitor has this)
- `Word Soup` (from words.json — varied word lengths for design mockups)

**Format tabs (output area):**
- `Plain text` | `HTML` | `Markdown`
- Each tab shows formatted output in a `<textarea>`
- Copy button per tab

**Live preview pane:**
- Renders output as styled HTML below the textarea
- Font size slider: 12–24px so designers can eyeball line breaks
- Font family toggle: Sans / Serif (switches between DM Sans and DM Serif Display)

**URL params:**
- `?unit=paragraphs&count=3&format=html&mode=latin`
- Parsed on page load to restore state
- State serialized to URL on each Generate click (replaceState, no history push)

### SEO Copy

- What lorem ipsum is: Cicero's *de Finibus Bonorum et Malorum* (45 BC), original Latin paraphrased in own words — do not copy lipsum.com wording
- When to use real content instead (copy testing, readability, SEO previews)
- Dev tips: Emmet `lorem` shorthand exists in VS Code/JetBrains — mention as context
- FAQ targeting long-tail queries ("lorem ipsum html", "3 paragraphs", "alternative to lorem ipsum") with FAQPage schema
- Internal links: random-paragraph-generator, random-sentence-generator, word-counter

---

## tools.json Registration

For each tool, add to:
- `mega` → appropriate category (Dad Jokes + Trivia → "Games & fun"; Lorem Ipsum → "Writing & vocabulary") — respect 4-tool-per-column limit
- `more_word_tools` or relevant grid section
- `footer_cols` → replace "planned" status entry if exists, else add under appropriate column

Replace "Coming soon" card on `/word-tools/` hub for all three tools.

---

## Validation

`scripts/validate-data.js` extended to cover all new JSON files:
- Every declared tag/filter value must have ≥ 5 matching entries
- For trivia: every category × difficulty combination must have ≥ 1 entry
- For dad jokes: every topic must have ≥ 5 entries; `qa` and `oneliner` formats both present

Additional checks:
- Lorem ipsum word count: request 137 words → verify output is exactly 137 words
- Lorem ipsum paragraph count: request 3 paragraphs → verify exactly 3 `<p>` tags in HTML output
- URL params round-trip: generate with params, parse URL, verify state matches
- Canonical URL in built output matches tool URL (not homepage)
- No console errors on load; graceful degradation if JSON fetch fails (SEED fallback)
- Static best-of jokes (dad jokes) and 10 sample trivia Q&As present in view-source output

Post-build: present trivia fact-verification flag list for user review before committing.

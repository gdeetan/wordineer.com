# Design: Random Number Generator 1–100

**Date:** 2026-07-06
**URL:** `/random-number-1-100/`
**Output:** `template-deploy/tools-src/random-number-1-100.html`

---

## Context

This is the canonical template for all Wave 2 number range variants (1–20, 1–50, 1–6, etc.). It must be built cleanly and parameterized so cloning it per-variant is a find-and-replace operation. It targets "random number generator 1 to 100" (~50K–100K/mo, KD 35–45) and is the second-highest-traffic page in the Wave 1 cluster.

---

## Architecture

Single static HTML file following the Wordineer `tools-src` CONFIG + SLOT pattern. All JS lives in the `<!-- SLOT:init -->` block as a namespaced IIFE (`WORDINEER_RN100`). No external dependencies. No fetch calls. No localStorage.

**File:** `template-deploy/tools-src/random-number-1-100.html`

**CONFIG:**
```json
{
  "url": "/random-number-1-100/",
  "output": "random-number-1-100.html",
  "type": "tool",
  "more_tools_key": "more_chance_tools",
  "more_tools_title": "More number & chance tools",
  "more_tools_subtitle": "Dice, coin flips, spinners, and more — all free"
}
```

---

## Slots

### `meta`
- `<title>`: "Random Number Generator 1 to 100 | Wordineer"
- `<meta name="description">`: ~155 chars, includes "random number between 1 and 100", teacher/classroom angle
- Canonical: `https://wordineer.com/random-number-1-100/`
- JSON-LD: `WebApplication`, `FAQPage`, `BreadcrumbList`

### `style`
- CSS namespace prefix: `.rn100-`
- Custom properties scoped to the tool: `--rn100-accent`, `--rn100-pill-bg`
- Result number: `font-size: clamp(4rem, 12vw, 6rem)`, centered, bold
- History chips: small, rounded, inline-flex, newest-first (CSS row-reverse or JS prepend)
- Distribution bars: horizontal, animated width transition
- Pool progress: small status text + progress bar strip
- Modes panel (exclude / blind pick): hidden by default, toggled via `.rn100--open` class
- Responsive: single column below 600px

### `hero`
- Breadcrumb: Wordineer → Number & Chance Tools → Random Number 1–100
- Badge: "Free online tool"
- H1: "Random Number Generator 1 to 100"
- Subhead: 1–2 sentences. Teacher angle: "Pick a random number between 1 and 100 instantly — no setup, works on any device."

### `tool`

**Default state (server-rendered):**
```html
<div class="rn100-result" aria-live="polite">42</div>
```
"42" shown statically so the page has visible content before JS runs.

**Controls row:**
- GENERATE button (primary, large) — `id="rn100-btn"`
- Copy button — copies current result to clipboard, shows "Copied!" toast for 1.5s

**Quick-range pills:**
Row of pill links below the result: "1–10" (links to `/random-number-1-10/`), "1–50" (links to `/random-number-1-50/`), "1–100" (triggers generate, highlighted as active), "1–1000" (links to `/random-number-1-1000/`)

**History strip:**
`<div id="rn100-history">` — up to 10 chips, newest prepended left. Cleared on page reload (no persistence).

**Mode controls (collapsed panel):**
Three toggle buttons below history: "Normal", "No-repeat pool", "Blind pick". Plus an "Exclude numbers" text link that expands the exclude field inline.

---

## Novel Features

### 1. No-Repeat Pool Mode
- Toggle: "Pool mode" button activates it; button gets active state
- State: internal array of 1–100 shuffled (Fisher-Yates) on activation
- Each generate pops one number from the shuffled array
- Pool status shown: "47 remaining in pool" with a thin progress bar
- When pool empties: show "Pool exhausted — reshuffling" banner, auto-reshuffle after 1.5s
- Excluded numbers are removed from the pool before shuffle

### 2. Distribution Panel
- Appears automatically after 10+ generates in the session (any mode)
- Shows 10 buckets: 1–10, 11–20, ..., 91–100
- Each bucket: label + horizontal bar (width proportional to count) + count badge
- Updates live on each generate
- "Reset stats" link clears counts and hides panel until 10 more generates

### 3. Exclude Numbers
- Collapsed by default; "Exclude numbers" text link expands it
- `<input type="text" placeholder="e.g. 13, 42, 7">` — comma-separated
- Parse on blur/generate; invalid entries shown as red chips, valid as gray chips
- Generate skips excluded numbers; if all numbers excluded, show error
- In pool mode, excluded numbers removed from pool before shuffle

### 4. Blind Pick Mode
- Two name inputs: "Player 1" and "Player 2" (placeholder text)
- Each player clicks their own "Pick" button — result hidden (shows "✓ Picked")
- "Reveal" button shown after both have picked — reveals both numbers side-by-side
- Winner highlighted; tie shown as "It's a tie!"
- "Play again" resets both picks

---

## JS Module Structure

```js
const WORDINEER_RN100 = (() => {
  const MIN = 1, MAX = 100;

  // State
  let current = null;
  let history = [];
  let stats = new Array(10).fill(0); // buckets 1-10, 11-20, ...
  let generateCount = 0;
  let excludeSet = new Set();

  // Pool mode state
  let poolMode = false;
  let pool = [];

  // Blind pick state
  let blindMode = false;
  let picks = [null, null];

  // Core
  function generate() { ... }       // normal or pool, respects excludeSet
  function updateResult(n) { ... }  // update DOM, history, stats
  function updateHistory() { ... }
  function updateStats() { ... }    // show/hide panel, update bars

  // Mode management
  function setMode(mode) { ... }    // 'normal' | 'pool' | 'blind'
  function shufflePool() { ... }    // Fisher-Yates on [MIN..MAX] minus excludeSet
  function parseExcludes(str) { ... }

  // UI helpers
  function copyResult() { ... }
  function showToast(msg) { ... }

  function init() { ... }           // cache DOM refs, bind events, keyboard handler

  return { init };
})();

document.addEventListener('DOMContentLoaded', WORDINEER_RN100.init);
```

---

## Keyboard Shortcuts
- Space / Enter → generate (when not focused on an input)
- Escape → close any open panels

---

## Explainer, FAQ, Who sections
- **Explainer:** How true randomness works, use cases (classrooms, raffles, games)
- **FAQ:** 5–7 questions covering "is this truly random", "how do I pick without repeats", "can I exclude numbers", etc.
- **Who:** Teacher, gamer, raffle organizer, developer use case cards

---

## SEO Internal Links
- Breadcrumb back to `/number-chance/`
- "More tools" grid from `tools.json` (`more_chance_tools` key)
- Inline links in explainer to `/dice-roller/`, `/coin-flip/`, `/random-number-generator/`

---

## Verification
1. Build: `cd template-deploy && python3 build.py` — no errors
2. Copy: `cp template-deploy/output/random-number-1-100.html wordineer-deploy/`
3. Serve: `cd wordineer-deploy && python3 -m http.server 8080`
4. Check: `http://localhost:8080/random-number-1-100.html`
   - Static "42" visible before JS loads
   - Generate button fires on click, Space, and Enter
   - Result is always 1–100
   - Quick-range pills present; 1–100 highlighted
   - History chips appear and are capped at 10
   - Pool mode: numbers don't repeat until exhausted, then reshuffle
   - Distribution panel appears after 10 generates
   - Exclude "50" — 50 never generated
   - Blind pick: both players pick, reveal shows winner
   - Copy button: clipboard gets the number, toast appears

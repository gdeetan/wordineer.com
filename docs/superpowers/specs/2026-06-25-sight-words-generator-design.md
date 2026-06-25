# Sight Words Generator — Design Spec
**Date:** 2026-06-25
**URL:** `/sight-words-generator/`
**Status:** Approved

---

## Overview

Master sight words generator tool for wordineer.com. Targets parents and teachers of early readers (Pre-K through 3rd grade). Combines Dolch and Fry lists in one interactive browser tool — the primary gap in the current competitor landscape, which is dominated by static PDFs and printable worksheets.

**Primary audience:** Parents teaching early readers at home, K-3 teachers, reading tutors, homeschool educators.

**Differentiators:**
- Free, instant, browser-based generator (no PDF, no signup)
- Both Dolch and Fry lists unified under one tool
- Audio pronunciation via browser TTS
- Practice Mode (flashcard-style recognition drill)
- Save words to browser-local review list
- Print-friendly output

---

## Data File: `sight-words-data.json`

Stored in `wordineer-deploy/data/`. Each entry:

```json
{
  "word": "the",
  "list": "both",
  "dolch_group": "pre-k",
  "fry_rank": 1,
  "fry_group": "1-100"
}
```

**Field definitions:**

| Field | Values | Notes |
|---|---|---|
| `word` | string | lowercase |
| `list` | `"dolch"` \| `"fry"` \| `"both"` | "both" = appears on both lists |
| `dolch_group` | `"pre-k"` \| `"kindergarten"` \| `"1st"` \| `"2nd"` \| `"3rd"` \| `"nouns"` \| `null` | null for Fry-only words |
| `fry_rank` | integer 1–300 \| `null` | null for Dolch-only words not in top 300 Fry |
| `fry_group` | `"1-100"` \| `"101-200"` \| `"201-300"` \| `null` | null for Dolch-only |

**Scope:** ~615 unique words (Dolch 315 + Fry top 300, deduplicated — words on both lists carry both `dolch_group` and `fry_group`).

Words that appear on both lists use `"list": "both"` and have both `dolch_group` and `fry_group` populated.

---

## Page Structure

Follows the standard `type: "tool"` template (CONFIG + SLOT syntax). Modeled on `sat-vocabulary-words.html`.

```
CONFIG → type: tool, url: /sight-words-generator.html
SLOT: meta
SLOT: style
SLOT: hero
SLOT: tool
SLOT: ad_b
SLOT: explainer
SLOT: faq
SLOT: who
SLOT: init
```

---

## META Slot

- `<title>`: Sight Words Generator — Dolch & Fry Lists with Audio & Practice Mode | Wordineer
- `<meta description>`: Free sight words generator with Dolch and Fry lists. Filter by grade, hear every word, and practice with flashcard mode. No login required.
- Canonical: `https://wordineer.com/sight-words-generator/`
- OG tags, BreadcrumbList schema, FAQPage schema, WebApplication schema
- Breadcrumb: Wordineer › Word Tools › Sight Words Generator

---

## HERO Slot

```
Breadcrumb: Wordineer › Word Tools › Sight Words Generator
Badge: Dolch + Fry · Audio · Practice Mode · Free
H1: Sight Words Generator
Subtitle: Generate sight word lists from the Dolch and Fry collections.
         Filter by grade level, hear every word read aloud, and drill with
         Practice Mode — no account, no download, no cost.
```

---

## TOOL Slot

### Controls Panel (left column)

| Control | Element | Default | Options |
|---|---|---|---|
| List | `<select id="ctrl-list">` | `all` | All Lists / Dolch / Fry |
| Grade / Group | `<select id="ctrl-group">` | `all` | Dynamic — see below |
| Word count | `<input type="number" id="ctrl-count">` | `15` | 5–50 |
| Show list label | `<input type="checkbox" id="ctrl-badge">` | checked | — |

**Grade/Group dropdown — dynamic by list selection:**

- **All / Dolch selected:** All Grades / Pre-K / Kindergarten / 1st Grade / 2nd Grade / 3rd Grade / Nouns
- **Fry selected:** All Groups / Words 1–100 / Words 101–200 / Words 201–300

Dropdown rebuilds via JS when List value changes.

Buttons: Generate (primary) · Reset · mobile "More options" toggle for count + badge controls.

### Results Panel (right column)

Top bar: `{N} words` · Practice Mode button · Copy All · Print

Word list (`<ul id="sw-list">`). Each `<li class="word-item">`:

```
[word text — large]   [badge: "Dolch Pre-K" or "Fry 1–100"]   [🔊 speaker]  [♡ heart]
```

- Badge hidden when `ctrl-badge` unchecked
- Speaker → `window.speechSynthesis` at rate 0.85
- Heart → toggles save to `localStorage["sw-saved"]`

Empty state: "No words match your filters. Try selecting a different grade or list."

### Saved Words Section (below tool card)

Collapsible panel (collapsed by default if empty). Shows all saved words as chips with × remove button. Copy Saved · Clear All buttons.

### Practice Mode Panel (replaces results panel)

- Header: ← Exit Practice | progress "3 of 15"
- Center: large word display
- Hear Word button (TTS)
- Prev / Next navigation buttons
- No "reveal definition" step — sight words are recognition-only

---

## EXPLAINER Slot

~1,500–2,000 words total. Tone: warm, practical, parent-facing. Not academic. Not AI-sounding.

### H2: What are sight words?

~250 words. Plain explanation of what sight words are and why they matter. The idea that ~300 high-frequency words make up 50–75% of written text — knowing them by instant recognition frees up cognitive load for comprehension. Mention the two major lists (Dolch, Fry) briefly.

### H2: Dolch vs. Fry — what's the difference?

~300 words. History of each list. Dolch (1930s–40s, 220 service words + 95 nouns = 315, organized Pre-K through 3rd grade). Fry (1950s, updated 1980, 1000 words ordered by frequency). Key practical point: Dolch is the standard for K-3 classrooms; Fry is more useful for tracking reading progress through Grade 9 and beyond. Both are public domain. Most schools use Dolch for early grades — if in doubt, start there.

### H2: How to use this generator

~200 words. Numbered list:
1. Choose a list (Dolch for classroom alignment, Fry for frequency-based practice)
2. Pick a grade or group
3. Set word count (10–15 for a session, 20–30 for review)
4. Click Generate — or press Space to reshuffle
5. Click the speaker on any word to hear it
6. Heart words your child struggles with
7. Hit Practice Mode and run a recognition drill

### H2: Five ways to practice sight words at home

~400 words. Practical techniques for parents:
1. **Flash card drill** — classic but effective; keep sessions to 5 minutes
2. **Find it in a book** — point out sight words during bedtime reading
3. **Sentence building** — say the word, have the child use it in a sentence aloud
4. **Rainbow writing** — write the word in multiple colors (kinesthetic reinforcement)
5. **Practice Mode** — use this tool's built-in drill; one word at a time, no distractions

### H2: When should my child know these words?

~300 words. Grade-by-grade milestones:
- Pre-K: recognize 10–20 of the 40 Dolch Pre-K words
- Kindergarten: know all 40 Pre-K words + begin Kindergarten list (52 words)
- 1st grade: full Dolch Pre-K + Kindergarten + 1st grade (133 words total)
- 2nd grade: full Dolch list through 2nd grade (179 words)
- 3rd grade: all 220 Dolch service words + working on nouns
- Note: these are guidelines, not pass/fail benchmarks — development varies

### H2: More tools for early readers

~100 words. Internal links section — see Internal Links below.

---

## FAQ Slot

6 questions with FAQPage schema:

1. What is the difference between Dolch and Fry sight words?
2. How many sight words should a kindergartner know?
3. What order should I teach sight words?
4. How long does it take to learn all the Dolch words?
5. Can I print the sight word list?
6. Is this tool free to use?

---

## WHO Slot (4 cards)

1. **Parents** — teaching early readers at home; use Practice Mode during evening sessions
2. **Kindergarten & 1st Grade Teachers** — build grade-specific word lists for morning warm-ups
3. **Reading Tutors & Interventionists** — quickly generate targeted lists by grade for reading support sessions
4. **Homeschool Educators** — structured sight word curriculum aligned to Dolch/Fry grade groupings

---

## INIT Slot (JavaScript)

IIFE pattern matching SAT vocab tool exactly.

Key object: `SW` with methods:
- `load()` — fetch `/data/sight-words-data.json`, cache to `SW.data`
- `filter()` — read ctrl-list, ctrl-group, ctrl-count; filter + shuffle + slice
- `generate()` — load().then(filter).then(render)
- `render(words)` — build `<li>` items with badge, speaker, heart
- `speak(word)` — `speechSynthesis.speak()` at rate 0.85
- `toggleSave(word)` — localStorage get/set `sw-saved` array
- `renderSaved()` — update saved panel chips
- `enterPractice()` — hide word list, show practice panel, set `practiceWords`
- `exitPractice()` — reverse
- `renderPractice()` — show current word, update progress counter
- `copyAll()`, `print()` — standard copy/print helpers
- `init()` — wire all event listeners, call `generate()` on load

Dynamic group dropdown rebuild on `ctrl-list` change:

```js
var GROUPS = {
  dolch: ['all','pre-k','kindergarten','1st','2nd','3rd','nouns'],
  fry:   ['all','1-100','101-200','201-300'],
  all:   ['all','pre-k','kindergarten','1st','2nd','3rd','nouns','1-100','101-200','201-300']
};
```

Filter logic:
- list filter: `word.list === selected || selected === 'all' || (selected === 'dolch' && (word.list === 'dolch' || word.list === 'both')) || ...`
- group filter: check `word.dolch_group` for Dolch groups, `word.fry_group` for Fry groups
- Shuffle (Fisher-Yates), slice to count

Space key → generate (same guard as SAT tool: skip if activeElement is input/select/button).

Auto-filter on `ctrl-list` and `ctrl-group` change (no need to click Generate for filter changes).

---

## CSS (STYLE Slot)

Extend SAT vocab tool styles. Key additions:
- `.word-badge` — small pill label (Dolch Pre-K, Fry 1–100)
- `.badge-dolch` — purple tint
- `.badge-fry` — teal tint
- `.badge-both` — neutral gray
- Print styles: hide controls, nav, ads; print word list only

---

## Internal Links (in explainer prose)

- `/spelling-bee-words-2nd-grade/` and `/spelling-bee-words-3rd-grade/` — natural next step after sight words mastery
- `/sight-words-kindergarten/` — pre-filtered grade page (coming soon)
- `/sight-words-1st-grade/` — pre-filtered grade page (coming soon)
- `/dolch-sight-words/` — full Dolch reference page (coming soon)
- `/fry-sight-words/` — full Fry reference page (coming soon)
- `/word-tools/` — hub

---

## tools.json Updates

Add to `mega["Writing & Vocabulary"]`, `more_word_tools`, and `footer_cols["Writing & Vocabulary"]`:

```json
{ "href": "/sight-words-generator/", "text": "Sight Words Generator" }
```

---

## _redirects Update

```
/sight-words-generator   /sight-words-generator/   301
```

---

## Deliverables

1. `template-deploy/tools-src/sight-words-generator.html`
2. `wordineer-deploy/data/sight-words-data.json` (~615 words)
3. `template-deploy/tools.json` — updated with new tool entry
4. `wordineer-deploy/_redirects` — clean URL redirect

Build steps (not in scope of this spec — done by developer after files are ready):
- `cd template-deploy && python3 build.py`
- `cp template-deploy/output/sight-words-generator.html wordineer-deploy/`
- Preview locally before deploying

---

## Out of Scope

- Grade-specific sub-pages (`/sight-words-kindergarten/`, etc.) — separate tickets
- Printable PDF generation — browser print is sufficient
- Progress tracking / accounts — no backend on this site
- Fry words 301–1000 — covered by dedicated `/fry-sight-words/` page later

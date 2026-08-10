# Mad Libs Generator — Design Spec

**Date:** 2026-08-10
**URL:** `/mad-libs/`
**Output:** `mad-libs.html`
**Type:** `tool`

---

## Goal

Build a Mad Libs generator that drives session time through interactive fill-in-the-blank gameplay. Primary audiences: kids/families, game night groups, teachers, ESL learners. Two play modes — manual (group/social) and random (solo/instant) — on a single page.

---

## Architecture

**Data loading:** Stories are inlined as a JS array in the `init` slot — no fetch required at runtime. `mad-libs.json` exists in `wordineer-deploy/data/` as the source of truth and for future expansion (switch to fetch when story count exceeds ~100).

**Word pools for random fill:** Pulled from existing data files already loaded on the page — `adjectives.json`, `nouns.json`, `verbs.json`, `adverbs.json`, `names.json`. These are loaded lazily after page idle (same pattern as other Wordineer tools). Random fill waits for them to be available; if not yet loaded, triggers the load.

**Sharing:** Completed stories are encoded in URL query params (`?story=zoo-day&adj1=silly&name1=Margaret…`). On page load, JS detects params and pre-fills + reveals the story automatically, with a "Shared story" indicator.

---

## Layout

Left sidebar (280px) + right story panel. Matches Scattergories layout exactly — reuses existing CSS variable system (`--brand`, `--bg`, `--border`, `--text`, etc.).

**Sidebar contains:**
- Category dropdown (All, Kids, Funny, Holiday, Adventure, Sports)
- Mode toggle: Manual / Random (radio button style, same as other toggles on site)
- Primary CTA button: "New Story" (Manual mode) / "Random Story" (Random mode)
- Secondary actions after a story is revealed: "Play Again", "Copy Story", "Share Link"

**Story panel contains:**
- Story title (e.g., "A Day at the Zoo")
- Story body with blanks rendered as labeled inputs (Manual) or bold colored words (Random/Revealed)
- Blank labels shown above each input: "Adjective", "Person's Name", "Verb", etc.
- "Reveal Story" button activates when all blanks are filled (Manual mode only)
- Filled words display bold + `var(--brand)` color inline in the revealed story

**Mobile:** Sidebar stacks above story panel. Category + mode controls collapse to a compact row.

---

## Data Format

Stories live in `wordineer-deploy/data/mad-libs.json` and are inlined into the page at build time.

```json
{
  "id": "zoo-day",
  "title": "A Day at the Zoo",
  "category": "kids",
  "template": "One {{adj1}} day, {{name1}} decided to visit the {{noun1}}. The first animal they saw was a {{adj2}} {{noun2}} that could {{verb1}} incredibly fast.",
  "blanks": [
    { "id": "adj1",  "label": "Adjective",     "type": "adjective" },
    { "id": "name1", "label": "Person's Name",  "type": "name" },
    { "id": "noun1", "label": "Place",          "type": "noun" },
    { "id": "adj2",  "label": "Adjective",      "type": "adjective" },
    { "id": "noun2", "label": "Animal",         "type": "noun" },
    { "id": "verb1", "label": "Verb",           "type": "verb" }
  ]
}
```

**`type` field** maps to the word pool used for random fill:
- `"adjective"` → adjectives.json
- `"noun"` → nouns.json
- `"verb"` → verbs.json
- `"adverb"` → adverbs.json
- `"name"` → names.json (first names only)
- `"number"` → random integer (inline, no data file needed)

---

## Story Library (20 stories at launch)

| Category | Count | Titles |
|---|---|---|
| `kids` | 5 | A Day at the Zoo, Outer Space Adventure, The Magic School, My Weird Pet, The Baking Disaster |
| `funny` | 5 | My First Day at Work, The Worst Date Ever, Cooking Disaster, The Superhero's Problem, Airport Chaos |
| `holiday` | 4 | Santa's Workshop, Halloween Night, Thanksgiving Feast, Happy Birthday |
| `adventure` | 3 | Pirates of the Seven Seas, The Dragon's Cave, Haunted Mansion |
| `sports` | 3 | The Big Game, Olympic Champion, Gym Day |

Each story has 6–10 blanks. Stories are self-contained — no blank depends on a previous blank's value.

---

## SEO

**Title:** `Mad Libs Generator — Free Online Word Game | Wordineer`

**Meta description:** `Play Mad Libs online for free. Pick a story, fill in the blanks, and laugh at the results. Works for kids, families, and game night. No account needed.`

**Target keywords:** "mad libs online", "mad libs generator", "fill in the blank story game", "mad libs for kids"

**Schema:** `FAQPage` + `BreadcrumbList`

**FAQ questions:**
1. What is Mad Libs?
2. Can I play Mad Libs alone?
3. Is this free? Do I need an account?
4. Can I share my completed Mad Lib with friends?
5. What age is Mad Libs good for?

**Who uses it section:** Kids, families on game night, teachers (ESL fill-in-the-blank exercises), party hosts

**Internal links:** Random Word Generator, Scattergories Generator, Would You Rather, Charades Generator

---

## tools.json Placement

- `mega` → Games & Fun category (replace least-used entry if at 4-link limit)
- `more_word_tools` grid on word game tool pages
- `footer_cols` → Games & Fun column (replace least-used if at limit)

---

## Build Steps

1. Create `wordineer-deploy/data/mad-libs.json` with all 20 stories
2. Create `template-deploy/tools-src/mad-libs.html` following CONFIG + SLOT pattern
3. Add entry to `tools.json` (mega, footer, more_tools)
4. Add clean URL rewrite to `wordineer-deploy/_redirects`: `/mad-libs/ → /mad-libs.html 200`
5. Run `python3 build.py` in `template-deploy/`
6. Copy `output/mad-libs.html` → `wordineer-deploy/`
7. Preview locally at `localhost:8080/mad-libs.html`

---

## Out of Scope (v1)

- User-submitted stories
- Print mode for completed stories
- Community story voting
- Story difficulty ratings

# Word of the Day — Linkable Asset (Phase 1)

**Date:** 2026-08-22
**URL:** `/word-of-the-day/`
**Source:** `template-deploy/tools-src/word-of-the-day.html`
**Output:** `word-of-the-day.html`
**Type:** `tool`
**Status:** Approved

---

## Goal

Turn `/word-of-the-day/` from a 12-word habit widget into a citable classroom resource: a published 2026 calendar of useful words, server-rendered on the same URL, with CSV download and print-to-PDF.

This is Phase 1 of a sequenced link play:

1. **Phase 1 (this spec):** year list on the hub + CSV + print + copy-this-week
2. **Phase 2 (later):** printable one-pagers and an embed widget with Wordineer attribution
3. **Phase 3 (later):** unique share cards / OG, RSS

Phase 1 does **not** add dated URLs.

---

## Why this is the linkable object

Dictionary.com already owns “today’s word.” Wordineer’s citation is different:

- The words are **useful in writing and speech**, not obscure trivia
- The **entire year is public** on day one (table + CSV)
- Every row includes a **5-minute classroom prompt** teachers can use without prep

A teacher blog or homeschool resource page can link to one URL and download the list. That is the backlink hook.

---

## URL and files

| Role | Path |
|---|---|
| Page | `/word-of-the-day/` |
| Source | `template-deploy/tools-src/word-of-the-day.html` |
| Dataset | `wordineer-deploy/data/wotd-2026.json` |
| CSV | `wordineer-deploy/data/wotd-2026.csv` |
| Build | `template-deploy/build.py` (`inject_data` + new SSR renderer) |

No new routes. No new template type. No new frameworks.

CONFIG on the source page must include `"inject_data": "wotd-2026.json"`.

`copy_data_assets()` already copies `*.json` into `template-deploy/output/data/`. Extend it so `wotd-2026.csv` is copied the same way `etymology-100.csv` is.

After build, copy `template-deploy/output/word-of-the-day.html` to `wordineer-deploy/` as usual.

---

## Page layout (top to bottom)

Keep the existing tool chrome (nav, ads below the tool, explainer, FAQ, who-uses, more-tools, footer). Change the tool body to:

1. **Breadcrumb + hero** — H1 stays “Word of the day”. Intro line must mention the free 2026 list and download.
2. **Today’s card** — existing card UI (word, listen, POS, pronunciation, difficulty, definition, plain English, example, memory hook, quiz, copy/save, Surprise me, saved words, previous 7 days).
3. **Year-list toolbar** (new, directly under the card, still inside the tool wrap):
   - Heading: “2026 word of the day list”
   - One sentence: this is the official calendar, free to download and print, words chosen for actual use in writing and conversation.
   - Actions: **Download CSV**, **Print / Save as PDF**, **Copy this week**
   - Month jump links: Jan–Dec
4. **Year table** (new) — 365 rows, grouped visually by month with `id="wotd-month-01"` … `wotd-month-12"`.
5. Existing explainer / FAQ / who-uses — updated to mention the published list.

Table columns (on-page):

| Date | Word | Part of speech | Definition | Classroom prompt |
|---|---|---|---|---|

CSV includes every schema field, not only table columns.

On viewports ≤700px the table may scroll horizontally rather than stacking into unreadable cards. Month jumps stay visible above the table.

---

## Dataset

One file, 365 objects, one per calendar date from `2026-01-01` through `2026-12-31`.

```json
{
  "date": "2026-08-22",
  "word": "lucid",
  "pos": "adjective",
  "pronunciation": "LOO-sid",
  "difficulty": "medium",
  "definition": "clear and easy to understand",
  "explanation": "A lucid idea, sentence, or explanation is clear enough that people can follow it without confusion.",
  "example": "Her lucid summary helped the whole class understand the difficult chapter.",
  "memory": "Think of a clear light switching on: lucid writing lights up the meaning.",
  "quiz": "Which sentence uses lucid correctly?",
  "answer": "Correct use: The teacher gave a lucid explanation of the problem.",
  "prompt": "Give students 60 seconds to rewrite a confusing sentence from today’s lesson so it is lucid."
}
```

### Invariants

- Exactly 365 objects
- Unique `date` values covering the full 2026 calendar
- Unique `word` values (case-insensitive); one lemma per year (`adapt` or `adaptable`, not both)
- `pos` is `noun`, `adjective`, `verb`, or `adverb`
- `difficulty` is `easy`, `medium`, or `hard`
- Mix: about 30% easy, 50% medium, 20% hard (allow ±5 percentage points)
- Every field is a non-empty string
- `definition` under ~100 characters
- `example` is one sentence that uses the word in a realistic setting
- `prompt` is one classroom action a teacher can run in about five minutes
- No HTML in JSON strings; italics and quotes are plain text

### Word selection (useful register)

The list is “words people actually write and say,” not a cabinet of rarities.

**Include:** high-utility academic/writing vocabulary (clear, precise, widely understood once learned). The current 12 curated words (`lucid`, `resilient`, `nuance`, `pragmatic`, `vivid`, `meticulous`, `cordial`, `tenacious`, `concise`, `curious`, `eloquent`, `adapt`) stay in the year and are assigned to dates.

**Prefer sources already on Wordineer:** `words.json` (easy/medium, length 4–12), ESL CEFR B1–C1 items, SAT/writing lists that are still general-purpose. Generate missing fields (example, memory, quiz, answer, prompt) to the schema above — do not leave generator leftovers like “Try writing one sentence that uses X.”

**Exclude:**

- Profanity and slurs
- Proper nouns and multi-word phrases
- Novelty / dialect jokes (`fopdoodle`, `gardyloo`, `snollygoster`)
- Untranslatable-aesthetic-only items (`mamihlapinatapai`, `kalsarikänni`) unless the word is established English (`schadenfreude` may stay; invented Koenig-isms should not dominate)
- Words whose only appeal is being weird

**Date assignment:** spread difficulty through each week so a class does not get four hard words in a row. Pattern to start from: easy, medium, medium, hard, medium, easy, medium, then adjust to hit the yearly mix.

The JSON is the source of truth. The CSV is generated from that JSON in the same change (same field order as the schema). Do not hand-edit CSV independently.

---

## Architecture

Static HTML. No CMS. No daily Cloudflare rebuild required for Phase 1.

### Build

1. `build.py` reads `wotd-2026.json` via existing `inject_data`.
2. `inject_page_data()` inlines it as `window._PAGE_DATA` (existing helper).
3. New branch in `inject_ssr_html()` for `url == '/word-of-the-day/'`:
   - Replace `<!-- SSR_TODAY -->` inside `#wotd-main` with the card inner HTML for the **build date in UTC**, mapped the same way as runtime (`2026-{MM}-{DD}`, Feb 29 → Feb 28)
   - Replace `<!-- SSR_ROWS -->` in the year-table `<tbody>` with 365 `<tr>` rows grouped by month headings / `id="wotd-month-MM"`

The year table must appear in view-source. Google does not need JavaScript to see the 365 words.

### Today’s card at runtime

JavaScript selects the row by the **visitor’s local calendar date**, mapped onto the 2026 list:

- In 2026: use local `YYYY-MM-DD` directly
- In any other year: use `2026-{MM}-{DD}`; if that date does not exist (Feb 29), use `2026-02-28`

That mapping keeps the page working after 31 Dec 2026 without a new file. The table caption stays “2026 word of the day list.”

If `_PAGE_DATA` is missing or invalid, fall back to the existing 12-word curated cycle (`dayNumber` from 2026-01-01). That fallback is only for a broken data file, not a second calendar.

**Surprise me** still pulls a random practice word. Pool = the 365 list excluding today’s official word, plus `words.json` rows once that file has loaded (same filter as today: length 4–13 with a definition). Surprise me never changes the official dated word and does not rewrite the year table.

**Previous 7 days** look up the previous seven local dates through the same 2026 mapping. They are buttons, not links.

**Listen, copy, save, quiz** keep current behavior, driven by the active card entry.

### Copy this week

Uses the visitor’s local week **Monday–Sunday** that contains today. Maps each of those seven dates onto the 2026 list. Copies a tab-separated block:

```
date	word	pos	definition	prompt
```

Toast: “Copied this week’s words.” If a mapped date is missing from the dataset, skip that row rather than inventing a word.

### Print / Save as PDF

No PDF library. A print stylesheet plus `window.print()` on the Print button.

`@media print` must hide: site nav, mega menu, ads, FAQ, who-uses, more-tools, footer, Surprise me, saved-words UI, quiz reveal chrome.

Print output includes:

- Title: “Wordineer 2026 Word of the Day”
- Credit line with `https://wordineer.com/word-of-the-day`
- The year table, with a page break before each month when possible

Teachers use the browser’s “Save as PDF.”

### CSV

The Download CSV button is a normal file link to `/data/wotd-2026.csv` (`download` attribute allowed). Header row matches the JSON keys in schema order.

---

## Copy and SEO on the hub

Update title and meta description so they name the free 2026 list, not only the daily habit.

Add JSON-LD `Dataset` pointing at the CSV:

- `@type`: `Dataset`
- `name`: Wordineer 2026 Word of the Day
- `url`: `https://wordineer.com/word-of-the-day`
- `distribution.contentUrl`: `https://wordineer.com/data/wotd-2026.csv`
- `encodingFormat`: `text/csv`

Keep existing `FAQPage`, `WebApplication`, and `BreadcrumbList`. Point `canonical`, `og:url`, and `WebApplication.url` at the same path form other tool pages use after `build.py` canonicalization.

FAQ must keep the JS accordion pattern (no `<details>`). Wrap answers in `<p>`. Add questions:

- Can I download the full year list?
- Can I print this for class?
- Are these the same words Dictionary.com uses? (No — this list is curated for useful writing words and is published for the whole year.)

Update the existing “does the word change every day” answer so it mentions the published 2026 calendar on the page.

Internal links in explainer: at least four related tools (word tools hub, cool words or SAT vocab, random word generator, ESL/CEFR or sight words). Do not hardcode mega-menu or footer.

---

## Error handling

| Case | Behavior |
|---|---|
| JSON missing at build | `inject_ssr_html` logs a warning, leaves placeholders, does not crash the rest of the site build |
| JSON missing in the browser | 12-word curated fallback for the card; year table still whatever was baked (possibly empty) |
| Local date maps to a missing row | show the nearest previous date in the file; toast nothing |
| Clipboard API missing | `copyText` no-ops besides the existing toast path |
| Speech synthesis missing | hide listen button (already implemented) |
| Print on mobile | still call `window.print()`; layout may be single-column |

Do not fetch the year list on first paint. Above-the-fold card works from the SSR’d entry plus inlined `_PAGE_DATA`.

---

## Out of scope (Phase 1)

- Dated permalinks (`/word-of-the-day/2026-08-22/`)
- A separate `/word-of-the-day/2026/` URL
- Embed widget
- Email signup
- RSS
- Per-word Open Graph images
- Search/filter UI on the table (month jumps only)
- A 2027 file
- Accounts / synced saved words
- Changing `tool-engine.js` or bumping global cache `?v=`

---

## Testing

No automated test framework. Verify with commands and a local server.

**Data**

```bash
python3 -m json.tool wordineer-deploy/data/wotd-2026.json >/dev/null
```

Confirm: 365 items; unique dates; unique words; difficulty mix within ±5pp of 30/50/20; every key present.

**Build**

```bash
cd template-deploy && python3 build.py
```

Confirm log line that 365 items were baked into `/word-of-the-day/`. Copy output HTML to `wordineer-deploy/`.

**Page (HTTP server, not `file://`)**

```bash
cd wordineer-deploy && python3 -m http.server 8080
```

Open `http://localhost:8080/word-of-the-day.html` (or the trailing-slash rewrite if `_redirects` is not applied locally — use the `.html` file).

| Check | Expected |
|---|---|
| View source | Year table contains real words; not an empty `<!-- SSR_ROWS -->` |
| Today’s card | Matches local date mapped to 2026; not stuck on “Ephemeral” after JS runs |
| Previous 7 | Show the mapped prior dates’ words |
| Surprise me | Changes the card, not the table, not the official date mapping |
| Download CSV | Downloads `wotd-2026.csv` with header + 365 rows |
| Copy this week | Clipboard has 7 TSV rows for the local Mon–Sun week |
| Print | Preview shows table + credit, hides nav/ads/FAQ |
| FAQ | Accordion toggles; first item open |
| Mobile 360px | Card usable; table scrolls horizontally; month jumps wrap |
| Console | No errors on load |

---

## Success criteria

Phase 1 is done when:

1. `/word-of-the-day/` shows a real daily word from the 365-word calendar
2. View-source contains all 365 words in an HTML table
3. CSV is downloadable from `/data/wotd-2026.csv`
4. Print stylesheet produces a teacher-usable year list
5. Copy-this-week copies the local week’s rows
6. No new URLs were added
7. Manual checks above pass

Outreach is not part of this spec. The page has to be citeable first.

---

## Phase 2 / 3 reminders (do not implement now)

- **Phase 2:** printable single-word cards; embeddable iframe or snippet that links back to `/word-of-the-day/`
- **Phase 3:** share text + unique OG; RSS of the dated list
- Dated archive URLs only after the hub list is live and linked

# Design: 5-Letter Words Starting With [XY] — Multi-Letter Prefix Pages

**Date:** 2026-08-13
**Status:** Approved
**Scope:** Batch 1 — 2-letter prefixes (e.g. `/5-letter-words-starting-with-st/`). Batch 2 — 3-letter prefixes — deferred.

---

## Problem

Wordineer has `/5-letter-words-starting-with-[a-z]/` (one page per first letter). WordHippo and competitors rank for high-volume Wordle queries like "5 letter words starting with st" and "5 letter words starting with cr" — multi-letter prefix pages that Wordineer doesn't have. These are among the highest-traffic word-game queries.

---

## Approach

Standalone Python generator script (`template-deploy/generate_prefix_pages.py`) reads existing per-letter JSON data, filters by prefix, and writes static HTML pages directly to `wordineer-deploy/`. Bypasses the CONFIG/SLOT build.py pipeline — the script templates pages itself. Idempotent: re-running overwrites cleanly.

Not chosen:
- **Extending build.py** — complicates existing pipeline unnecessarily
- **Single dynamic page with query params** — no SEO value; Google won't index separate URLs

---

## Batch 1 Scope

- **Word length:** 5-letter only
- **Prefix depth:** 2-letter combos (AA through ZZ = up to 676 pages)
- **Minimum word count:** 3 words — pages with fewer are skipped entirely, no stub pages
- **Estimated output:** ~400–500 pages after skipping sparse combos

Batch 2 (3-letter prefixes) uses the same script with `--batch 3` flag. Deferred until Batch 1 is indexed and performing.

---

## Data Source

Existing `wordineer-deploy/data/five-letter-words-[a-z].json` files. Each entry has:
```json
{ "w": "stare", "t": "verb", "d": "to look fixedly", "diff": "easy" }
```

Script reads the relevant letter file (e.g. `five-letter-words-s.json` for all ST* pages), filters by `w.startswith(prefix.lower())`, and builds the word list for that page. No new data files needed.

---

## Page Structure

**URL:** `/5-letter-words-starting-with-[xy]/` (trailing slash canonical)
**Type:** Static HTML, content layout (no tool engine)
**Breadcrumb:** Home → Word Lists → 5-Letter Words → 5 Letter Words Starting With [XY]

### Above the fold

- H1: `5 Letter Words Starting With [XY]`
- Exact word count statement: "There are N five-letter words starting with [XY] in this list."
- **Best Wordle picks callout** — 3–5 words chosen by letter frequency coverage in positions 3–5. Framed as: "If you've confirmed [X] and [Y] in positions 1 and 2, [WORD1] and [WORD2] are strong next guesses — they cover common letters in the remaining slots."
- Filterable word table: columns = Word | Type | Definition. Filters = All / Nouns / Verbs / Adjectives / Adverbs.

### Below the fold

- **Letter frequency breakdown** — "The most common letters in position 3 for words starting with [XY] are: A, R, O, I, E." Computed from the actual word list, not generic filler. Helps players decide their next guess.
- **Word groups** — scannable sections by part of speech: Verbs, Nouns, Adjectives. Plain labels only.
- **Related prefixes** — links to 3-letter children (STA, STE, STI, STO, STR, STU) — shown as chips, only links to pages that will exist in Batch 2.
- **Parent page link** — "See all 5-letter words starting with [X]" → back to single-letter page.
- **Cross-link** — "Need to match a specific pattern? Try the Wordle Helper."
- FAQ: 2–3 questions with real, specific answers.

---

## Content Rules (Anti-AI-Slop)

These rules are enforced in the generator templates — not left to chance:

- **Intros are factual, not editorial.** State the count and the best picks. No "Whether you're a Wordle enthusiast or..." openers.
- **Banned phrases:** "comprehensive", "ultimate", "perfect", "you've come to the right place", "look no further", "in this article", "action-packed"
- **FAQ answers are specific.** Include the actual word count. Mention actual words. Give real Wordle strategy (letter frequency, not generic tips).
- **Word group labels are plain.** "Verbs", "Nouns", "Adjectives" — not "Power Verbs" or "Descriptive Words."
- **No padding.** If a section has nothing real to say, it's omitted rather than filled with generic text.

---

## Generator Script Design

**File:** `template-deploy/generate_prefix_pages.py`

**Usage:**
```bash
cd template-deploy
python3 generate_prefix_pages.py --batch 2   # generates 2-letter prefix pages
python3 generate_prefix_pages.py --batch 3   # generates 3-letter prefix pages (Batch 2, deferred)
```

**What the script does:**
1. Reads all `five-letter-words-[a-z].json` from `../wordineer-deploy/data/`
2. Iterates all prefix combos for the given batch length
3. Filters words by prefix, skips combos with <3 words
4. For each valid combo, computes:
   - Word count
   - Best Wordle picks (words with highest coverage of ETAOIN SHRDLU in positions 3–5)
   - Position-3 letter frequency distribution
   - Word groups by part of speech
5. Renders HTML from an inline template string
6. Writes to `../wordineer-deploy/5-letter-words-starting-with-[xy].html`
7. Collects `_redirects` entries and appends them to `../wordineer-deploy/_redirects`
8. Appends sitemap entries to `../template-deploy/sitemap.xml`
9. Prints summary: N pages written, M combos skipped

**Idempotency:** Script overwrites existing files. Re-running is safe.

---

## SEO & Internal Linking

- **Canonicals:** trailing-slash URL (e.g. `https://wordineer.com/5-letter-words-starting-with-st/`)
- **_redirects:** `.html` → trailing slash (301), trailing slash → `.html` (200 rewrite) — same pattern as all other word-list pages
- **Sitemap:** All generated pages appended to sitemap.xml
- **No tools.json changes** — too many pages for the mega-menu. Discoverable via parent single-letter pages and Google.
- **Single-letter parent pages:** After Batch 1, update each single-letter page (e.g. `/5-letter-words-starting-with-s/`) to include a "Browse by prefix" grid linking to all valid 2-letter combos under that letter.

---

## Deployment Plan

**Batch 1 — 2-letter prefixes:**
1. Run `generate_prefix_pages.py --batch 2`
2. Review sample pages (ST, CR, SH, TH, PR) for content quality
3. Commit generated HTML + updated `_redirects` + updated `sitemap.xml`
4. Push → Cloudflare auto-deploys
5. Submit updated sitemap to Google Search Console
6. Monitor indexing and click data over 4–6 weeks

**Batch 2 — 3-letter prefixes:** Separate session after Batch 1 data confirms approach is working.

---

## Success Criteria

- All generated pages have ≥3 words
- No banned phrases in any page
- Best Wordle picks callout present on every page
- Letter frequency section computed from real data (not hardcoded)
- _redirects entries present for every generated page
- Sitemap updated
- Sample QA passes on ST, CR, SH, BL, TR pages

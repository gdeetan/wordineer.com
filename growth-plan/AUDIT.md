# Wordineer Site Audit — June 2026

Inspection done by fetching pages directly. This document captures the state of every section so the growth plan stages map to reality, not assumption.

---

## Critical findings (fix first)

### 1. /number-chance/ category is broken at the URL level

When I fetch `/coin-flip/`, `/random-number-generator/`, or `/dice-roller/`, the server returns the **homepage content** (the random word generator page) with `<link rel="canonical" href="https://wordineer.com/">`.

**What this means in plain terms:**
- These URLs aren't really tool pages. They serve the homepage.
- The canonical tag explicitly tells Google "this URL is the same as the homepage, ignore it."
- So Google will never index `/coin-flip/`, `/random-number-generator/`, `/dice-roller/`, or any other broken page under this category.
- Worse, the homepage is being linked from many places under different anchor text ("Flip a coin", "Number Generator", "Dice Roller"), which dilutes the homepage's topical relevance for "random word generator."

**The likely cause:** Cloudflare Pages is set up with a fallback that serves `index.html` for missing routes, instead of returning a proper 404. The build script (`build.py`) isn't generating these pages because the source files haven't been built.

**The fix:** Either build these pages properly (Stage 1) or remove them from the nav and homepage until they exist. Stage 1 of the plan builds them all out.

### 2. API keys are exposed in client-side JS

Saw this in the source of `random-word-generator.html`:
```javascript
apiKeys: {
  wordnik: 'vzxbo7m8vl91xgsicsuk79k0pd2w1z3k4z7xl2sv9sje9akxh',
  merriam: 'Y1c8533d7-23e6-4c3b-9c48-854066e8caff',
}
```

Anyone can view source and steal these. Rotate both immediately and move the API calls behind a Cloudflare Worker proxy that holds the keys server-side.

### 3. Hub pages have many "Coming soon" placeholders

The `/word-tools/` and `/number-chance/` hubs both have a lot of cards marked "Coming soon" (not links, just text). This is fine in small numbers but at this volume it signals "thin/unfinished site" to Google. Each stage of this plan addresses a chunk of these.

---

## Section-by-section state

### / (Homepage — Random Word Generator)

**State:** Live, well-built. Strong content. ~600-word explainer, FAQ with schema, internal links to sister tools.

**Targeting:** `random word generator` (KD ~50–60, head term, unlikely to crack top 10 with current authority).

**Improvements needed:**
- Add `SoftwareApplication` schema in addition to FAQ schema
- Move the affiliate Grammarly block to below the tool (currently above-the-fold ad placement is a Helpful Content risk)
- Add 2-3 more contextual internal links to long-tail child pages (e.g., 5-letter words) inside the explainer paragraphs

### /word-tools/ (Hub)

**State:** Live, well-built. Long explainer. Good internal linking.

**Targeting:** `word tools`, `word generator tools`, `free word tools`.

**Improvements needed:**
- Reduce "Coming soon" cards by either building them or removing them
- Add `CollectionPage` + `ItemList` schema listing all live tools
- Pages currently marked live in the grid that are NOT live should be marked correctly or hidden

### /name-generators/ (Hub)

**State:** Live, lean (intentionally — this is the gold-standard hub pattern).

**Targeting:** `name generators`, `random name generator by country/origin`.

**Improvements needed:**
- Light. Consider adding 2-3 paragraphs of SEO content below the grid (currently the page is link-heavy with little prose).

### /other-generators/ (Hub)

**State:** Live based on nav. Wasn't sampled in this audit. Verify it follows the same pattern.

### /account-tools/ (Hub)

**State:** Live based on nav. Wasn't sampled in this audit. Verify it follows the same pattern.

### /number-chance/ (Hub)

**State:** Hub page itself is LIVE with excellent SEO content (~2000+ words). But every single tool linked from it is "Coming soon."

**Critical:** This hub is currently a content-quality positive but a user-experience and crawl-budget negative. Users land here, see no working tools, and bounce. Google sees a content-heavy page that links to placeholders. Stage 1 fixes this entirely.

### /random-words-starting-with/ (Hub for A-Z)

**State:** Hub exists. Some letter pages (A, S, Q referenced in nav) exist. Unknown whether all 26 are built.

**Improvements:** Verify all 26 sub-pages are built and each has unique content (not just a programmatic filter applied to the same template with no static content).

### /spelling-bee-words-Xth-grade/

**State:** GENUINELY EXCELLENT. ~2,500-word page on the 5th grade version. Audio pronunciation, practice mode, 4-week schedule, word origin explanations, 6-question FAQ. This is the best page on the site.

**Use as reference:** When briefing new pages, reference this page as the depth and quality target.

**Improvements:** Verify all grades (K-7) are at this quality. If 2nd and 3rd grade pages are thinner versions, deepen them.

### Random word length variants (/random-3-letter-word-generator/ through /random-8-letter-word-generator/)

**State:** Pages exist per word-tools hub. Not deeply inspected in this audit.

**Verify:** Each must have unique static content (sample words baked into HTML, not just JS-rendered). Otherwise they're effectively identical pages from Google's view.

### Parts of speech (/random-noun-generator/, /random-verb-generator/, /random-adjective-generator/, /random-adverb-generator/)

**State:** Pages exist with rich descriptions in the word-tools hub.

**Verify:** Each has filters specific to its part of speech (you mention nouns by abstract/concrete/proper/collective, verbs by action/linking/auxiliary/modal — these depth filters should already be present).

### /random-quote-generator/

**State:** Live based on hub mentions ("with filters for topic, author, tone, length, favorites, and image cards").

**Opportunity:** Quote generators are a niche where backlinks come naturally from teachers and writing sites. Strong asset for the linkable-asset campaign (Stage 4).

### /wordle-game/

**State:** Live. Unusual asset — a working game, not just a generator. This is a real differentiator.

**Opportunity:** Wordle helpers/games attract organic backlinks from puzzle communities. Worth promoting in the outreach stage.

### Name generator family (25+ pages)

**State:** Live based on /name-generators/ hub. One sampled (Irish) was substantial with explainer content and FAQ.

**Verify:** All 25+ are at the same depth as the Irish page. If some are thin, deepen them.

---

## Indexing status

Quick check via `site:wordineer.com` showed:
- Homepage indexed
- Random Irish Name Generator indexed
- Several others appear indexed

You're past the "not indexed" problem. Now the bottleneck is rankings, depth, and backlinks.

**Action:** Set up Google Search Console (if not done). Check the Coverage report monthly. Watch for:
- "Discovered – currently not indexed" → low-quality signal, often coming-soon or thin pages
- "Crawled – currently not indexed" → Google saw it and didn't bother indexing, usually depth/quality issue
- "Duplicate without user-selected canonical" → the /coin-flip/ family will all show up here

---

## Technical SEO quick wins

These can all be done in a single afternoon and will improve rankings of already-indexed pages:

1. **Submit sitemap to GSC.** Generate `sitemap.xml` from `tools.json` listing every actual live URL. Submit via Search Console. Don't list "Coming soon" placeholder URLs.

2. **Fix the canonicals across the site.** Every page must have a self-referencing canonical (`<link rel="canonical" href="https://wordineer.com/this-page/">`). The broken pages currently have `canonical=https://wordineer.com/` — fix when you build them.

3. **Trailing slash consistency.** Pick one: `/coin-flip/` (slash) or `/coin-flip` (no slash) or `/coin-flip.html`. The whole site must use one form and 301 the others. Mixed signals dilute ranking.

4. **Robots.txt and sitemap reference.** Confirm `/robots.txt` is allowing crawl and references the sitemap.

5. **Open Graph image.** `og:image` points to `https://wordineer.com/og-image.png`. Verify this file exists and renders at 1200x630.

6. **Performance check.** Run PageSpeed Insights on:
   - `/` (homepage / random word gen)
   - `/spelling-bee-words-5th-grade/` (heavy page)
   - `/number-chance/` (long hub)
   - One letter page like `/random-words-starting-with/a/`
   Fix any LCP > 2.5s, CLS > 0.1, INP > 200ms issues before scaling.

---

## What this audit does NOT cover

- Whether every page in the nav actually exists as a built file (I sampled a few)
- Page speed numbers (run PageSpeed Insights yourself)
- Specific Google rankings (need GSC / Ahrefs / Semrush data)
- Backlink profile (need Ahrefs / Semrush)
- Mobile rendering (verify yourself)

Once you have GSC connected, the Performance report + Coverage report will give you ground truth on what's actually indexed and ranking.

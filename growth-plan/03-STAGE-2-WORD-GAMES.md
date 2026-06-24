# Stage 2 — Word games cluster

**Goal:** Fill out the party-games and group-games sub-cluster. Build the "Coming soon" cards currently in `/word-tools/` Word Games section.

**Why this stage second:**
- You already have Pictionary and Charades pages live, so the cluster has a foundation
- These games attract some of the highest-intent traffic on the entire site — someone searching "would you rather generator" is at a party, mid-session, ready to use a tool right now
- Multiple games share infrastructure: a category dropdown + a phrase database + a "reveal" UX
- Low/medium competition for niche variants (Christmas Charades, Couples Truth or Dare) where the head terms are competitive

**Realistic outcome at maturity:** 10,000–20,000 visits/month across this cluster.

**Estimated build effort:** 25–40 hours across 3–4 weeks.

---

## Keyword landscape

### Tier 1 — Highest-intent, build first

| Keyword | Est. Volume | Est. KD | Page |
|---|---|---|---|
| would you rather generator | 15,000–30,000 | 35–45 | `/would-you-rather-generator/` |
| truth or dare generator | 30,000–60,000 | 40–50 | `/truth-or-dare-generator/` |
| would you rather questions | 60,000–100,000 | 50–60 | (already partly served by generator) |
| truth or dare questions | 80,000–150,000 | 55–65 | (head term; tough) |
| scattergories generator | 8,000–15,000 | 25–35 | `/scattergories-generator/` |
| scattergories list generator | 4,000–8,000 | 20–30 | `/scattergories-list-generator/` |
| catchphrase generator | 3,000–6,000 | 25–35 | `/catchphrase-generator/` |

### Tier 2 — Niche variants (lowest competition, sweet spot)

| Keyword | Est. Volume | Est. KD |
|---|---|---|
| couples truth or dare | 8,000–15,000 | 30–40 |
| dirty truth or dare | 8,000–15,000 | 30–40 |
| truth or dare for adults | 6,000–12,000 | 30–40 |
| spicy truth or dare | 3,000–6,000 | 25–35 |
| would you rather for kids | 5,000–10,000 | 25–35 |
| would you rather questions hard | 3,000–6,000 | 25–35 |
| pictionary words easy | 5,000–10,000 | 30–40 |
| pictionary words hard | 4,000–8,000 | 30–40 |
| pictionary words for adults | 8,000–15,000 | 35–45 |
| pictionary words for kids | 4,000–8,000 | 25–35 |
| charades for kids | 8,000–15,000 | 30–40 |
| charades for adults | 5,000–10,000 | 30–40 |
| family charades | 2,000–4,000 | 25–35 |
| christmas charades | 3,000–6,000 | 25–35 (you already have this) |
| halloween charades | 1,500–3,000 | 20–30 |
| disney charades | 2,000–4,000 | 25–35 |

### Tier 3 — Trivia and other

| Keyword | Est. Volume | Est. KD |
|---|---|---|
| random trivia question generator | 5,000–10,000 | 30–40 |
| trivia questions and answers | 30,000–60,000 | 50–60 |
| random trivia | 4,000–8,000 | 30–40 |
| dad jokes generator | 8,000–15,000 | 30–40 |
| random joke generator | 10,000–20,000 | 35–45 |
| icebreaker questions generator | 4,000–8,000 | 25–35 |
| never have i ever generator | 8,000–15,000 | 30–40 |

---
## --- do this next ---
## Build order (week by week)

### Week 1 — Foundation: Would You Rather + Truth or Dare

These are the two highest-volume head terms in this cluster. Build them with category filters from day one to support the niche variants later.

1. **`/would-you-rather-generator/`** — main version. Filter by:
   - Category: All, Funny, Hard, Easy, Food, Travel, Hypothetical, Disgusting
   - Audience: All, Kids, Teens, Adults, Couples
   - Display: One at a time / List of 10
   - Has "Print" and "Copy" buttons
   - Static 10 example questions in HTML

2. **`/truth-or-dare-generator/`** — main version. Filter by:
   - Mode: Truth, Dare, Random
   - Audience: Family-friendly, Teens, Adults, Couples
   - Static 10 example prompts in HTML
   - "Spin" button for fairness if multiplayer

### Week 2 — Audience variants (clone the main tools with audience pre-set)

These are essentially the same tools with different default filters and audience-specific content/copy/FAQ:

- `/would-you-rather-for-kids/`
- `/would-you-rather-for-adults/`
- `/would-you-rather-hard/`
- `/would-you-rather-funny/`
- `/truth-or-dare-for-kids/`
- `/truth-or-dare-for-adults/`
- `/truth-or-dare-for-couples/`
- `/dirty-truth-or-dare/` (be careful here — write tasteful copy and use a content disclaimer, since search intent here is "spicy adult party game" not anything that would violate platform policies)

Each must have its own unique H1, intro, and FAQ — not just a filter applied to the main page.

### Week 3 — Scattergories, Catchphrase, Trivia

3. **`/scattergories-generator/`** — generate a random letter (A-Z, excluding rare like X/Q/Z by default) + a list of 12 categories per round. Has a timer (1, 2, 3 min options).

4. **`/scattergories-list-generator/`** — just generates a list of 12 categories without the letter. Used by people who own the physical game and just need lists.

5. **`/catchphrase-generator/`** — gives a single word/phrase to describe without using certain "taboo" words. Round timer included.

6. **`/random-trivia-generator/`** — generates trivia questions by category (history, science, pop culture, sports, geography, entertainment, general). Show/hide answers.

7. **`/dad-jokes-generator/`** — random dad jokes. Simple, but attracts links from humor blogs.

### Week 4 — Pictionary and Charades expansion

You already have `/pictionary-word-generator/` and `/charades-generator/`. Add audience and theme variants:

- `/pictionary-words-easy/`
- `/pictionary-words-hard/`
- `/pictionary-words-for-adults/`
- `/pictionary-words-for-kids/`
- `/charades-for-kids/`
- `/charades-for-adults/`
- `/family-charades/`
- `/halloween-charades-generator/`
- `/disney-charades-generator/`
- `/movie-charades-generator/`

You already have `/christmas-charades-generator/` — keep it, and use that exact page as the template for the seasonal variants above.

---

## Template approach

These tools share a common pattern: pick from a categorized phrase database, display one or a list, support filtering. One shared engine module can power them all.

### Suggested shared engine

Add `party-engine.js` exposing:

```js
WORDINEER.party.init({
  data: './would-you-rather-data.json',
  filters: { category, audience },
  displayMode: 'single' | 'list',
  countId: 'ctrl-count',
  countDisplayId: 'count-display',
  // ...
});
```

### Data files

One JSON per game with categorized phrases:
- `would-you-rather-data.json`
- `truth-or-dare-data.json`
- `trivia-data.json`
- `dad-jokes-data.json`
- `pictionary-data.json` (you may already have this)
- `charades-data.json`

Each entry tagged with categories so the filter UI can target subsets:

```json
{
  "phrases": [
    { "text": "Would you rather ...", "category": "Hypothetical", "audience": "Adults" },
    ...
  ]
}
```

### Sourcing data

You'll need 200–500 entries per game minimum to feel substantial. Sources:
- **Public domain compilations** (very limited; most "would you rather" lists online are copyrighted)
- **Original writing** — write your own. Best for SEO uniqueness and avoiding copyright issues
- **AI generation, then heavy human review** — this is fast but every entry needs a human pass for tone, originality, and quality

**Avoid:** Scraping from existing "would you rather" or "truth or dare" sites. Their content is copyrighted; you'd inherit duplication penalties.

---

## What each page must have (same as Stage 1)

1. Self-referencing canonical
2. Unique H1 matching target query
3. Unique 250–400 word intro
4. Static example prompts in HTML (5–10 of them)
5. Unique FAQ block (3–5 questions) with FAQ schema
6. Internal links to 4–6 sibling pages within prose
7. Self-contained explainer below the tool
8. Breadcrumb schema
9. Open Graph + Twitter Card meta

For the audience variants (e.g., "for adults", "for kids"), the intro paragraph is the most important differentiator. Don't just say "click generate" — talk about *why* this specific audience version exists, what makes the questions appropriate for that group, when to use it.

---

## Claude Code prompt — build the Would You Rather Generator

```
# Task: Build /would-you-rather-generator.html — the foundation of the word games cluster

You are building the master template for an entire family of party-game generators. Build this page well; the audience variants (kids/adults/funny/hard) will clone it.

## Step 1: Read these first

1. https://wordineer.com/spelling-bee-words-5th-grade/ — fetch this. Match its depth.
2. https://wordineer.com/pictionary-word-generator/ — fetch this. It's a sibling tool; match its UX patterns.
3. /random-word-generator.html (in project) — for the slot/CONFIG/init patterns.
4. /tool-engine.js — for the engine init pattern.
5. /global.css, /head.html, /nav.html, /footer.html.

## Step 2: CONFIG block

<!-- CONFIG
{
  "url": "/would-you-rather-generator.html",
  "output": "would-you-rather-generator.html"
}
-->

## Step 3: Meta block (SLOT:meta)

- <title>: Would You Rather Generator — Free Random Questions | Wordineer
- <meta name="description">: Generate random "would you rather" questions for parties, road trips, classrooms, and ice-breakers. Filter by audience and category. Free, no sign-up.
- <link rel="canonical" href="https://wordineer.com/would-you-rather-generator/">
- Open Graph tags
- BreadcrumbList schema
- FAQPage schema covering Step 7
- SoftwareApplication schema

## Step 4: Page structure

1. Eyebrow: "Free · No sign-up · Instant"
2. H1: "Would you rather generator"
3. Subtitle: "Random would-you-rather questions for parties, road trips, classrooms, and ice-breakers. Filter by audience or category — pick what fits your group."
4. The tool
5. Explainer
6. FAQ
7. Who-uses-it
8. Footer

## Step 5: The tool

Controls (left, 220px):
- Audience: All / Family-friendly / Kids / Teens / Adults / Couples
- Category: All / Funny / Hypothetical / Hard / Food / Travel / Disgusting / Deep
- Display: One at a time / List of 10
- Count: 1-25 (when in List mode)
- Generate button + Press Space hint

Results (right):
- Big readable display of question(s)
- "A" and "B" options shown clearly
- Copy / Print buttons
- "Vote" buttons for fun (purely client-side, just shows what you/your group picked)

Page must show 10 static example questions in HTML on first paint.

## Step 6: Data file

Create /would-you-rather-data.json with 200+ original questions, each tagged with audience and category. Write these yourself — do not copy from existing sites. Mix:
- 60% family-friendly hypotheticals ("...have super strength but only when no one is watching, or super speed but always while eating soup")
- 20% kid-appropriate silly ("...have spaghetti for hair or rainbow toenails")
- 15% teen/adult (clean but more substantive: career trade-offs, ethical dilemmas)
- 5% couples-specific (low-stakes relationship questions, not romantic or sexual)

For the "Adults" filter, include slightly edgier content (career trade-offs, life regrets, controversial preferences) but keep it tasteful — no sexual content, no drug content. Save the spicier content for a separate /would-you-rather-spicy/ page later if desired.

## Step 7: FAQ (5 questions)

1. "What is the would you rather game?" — Explain the format.
2. "How do you play would you rather?" — Rules and variations.
3. "Are these questions appropriate for kids?" — Use the audience filter; "Family-friendly" and "Kids" are vetted for ages 6+.
4. "Can I print these for a road trip?" — Yes, use the print button.
5. "Where do the questions come from?" — All questions are original, written by Wordineer. We continuously add more.

## Step 8: Explainer content (350-500 words)

Three H2s:

**H2: Where would you rather questions actually work**
~150 words. Real use cases: car trips with kids, dinner-party warm-ups, first-date conversation starters, classroom ice-breakers, team-building meetings, late-night dorm conversations. The point is variety — these questions reveal personality without being intrusive.

**H2: How to pick the right difficulty**
~120 words. Quick guide to the audience and category filters. Family-friendly Hypotheticals = airplane with kids. Adult Hard = thought-provoking dinner conversation. Couples = relationship-light. Funny = pure entertainment.

**H2: Variations on the basic game**
~150 words. Three or four variant rules — voting + reasoning, written responses, fastest-answerer-wins, no-repeating-answers. Show readers there's more than one way to play.

## Step 9: Who-uses-it (4 cards)

- Parents (long road trips and family dinners)
- Teachers (classroom warm-ups and SEL exercises)
- Game-night hosts (no equipment, instant ice-breaker)
- Couples (low-pressure conversation tool)

## Step 10: Internal links (in prose)

Link in the body content (not just nav/footer):
- /truth-or-dare-generator/ (sibling)
- /scattergories-generator/ (sibling)
- /pictionary-word-generator/ (sibling)
- /random-trivia-generator/ (sibling)
- /word-tools/ (hub)

## Step 11: Make this cloneable

Build the page so that the audience-variant pages (/would-you-rather-for-kids/, /would-you-rather-for-adults/) can clone it with these changes:
- Pre-set audience filter in the controls
- Hide the audience selector (since it's pre-set)
- Change H1, intro, FAQ, explainer to match the audience
- Same JSON data, same engine, same CSS

## Step 12: Deliverables

1. /would-you-rather-generator.html
2. /would-you-rather-data.json with 200+ original questions
3. /party-engine.js (or extend tool-engine.js)
4. CSS additions to global.css (commented as added for /word-games/ family)
5. Update /word-tools/ hub: mark "Would You Rather Generator" as live, link the card
6. Add to sitemap.xml
7. Summary at end

Do not deploy.
```

---

## Success metrics for Stage 2

- [ ] 15+ pages live across the word-games cluster
- [ ] All pages indexed within 2 weeks of submission
- [ ] At least 3 pages getting impressions within 30 days
- [ ] At least 1 page in top 20 within 60 days
- [ ] Top long-tail variant (e.g., "Christmas charades", "couples truth or dare") in top 10 within 90 days

---

## Strategic note on this cluster

The party-games cluster has different traffic seasonality than your word/vocabulary tools:
- **December:** spikes for Christmas charades, holiday icebreakers, family games
- **October:** Halloween charades, scary truth or dare
- **Summer:** road trip games, would you rather, camping games
- **Back to school (Aug-Sep):** classroom ice-breakers, getting-to-know-you

This means traffic comes in waves rather than steady-state. Plan content drops to match:
- Build Halloween Charades by mid-September
- Build Christmas Charades pages (you have one) by mid-November
- Build summer/road-trip variants by April-May

A page launched 3 weeks before its peak season will rank in time for the season. Launched mid-season, it misses the wave entirely.

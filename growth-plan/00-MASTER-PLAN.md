# Wordineer Growth Plan — Master Plan

**Goal:** Grow Wordineer to 100K+ monthly organic visits, then beyond.

**Strategy:** Win the long tail first. Use low-competition wins to build authority, attract organic backlinks, and create the foundation for ranking competitive head terms later.

**Timeline:** Realistic path to 100K/mo is 9–18 months from today with disciplined execution. Earlier is possible but unlikely; later is fine if quality stays high.

---

## Site state — what I found

Audit done by fetching the live site (Jun 2026). Detailed audit in `AUDIT.md`.

**Live and strong (50+ pages):**
- Random word generator family (3- to 8-letter, parts of speech, weird words, wordle)
- Spelling bee K-7 (genuinely excellent — best content on site)
- Random sentence/paragraph generators, word counter
- Word scramble, word unscramble, crossword puzzle, Pictionary word/phrase, charades
- Word of the day, random quote generator
- 25+ regional name generators (Asian, European, Americas, Middle East)
- Username, password, passphrase, memorable password, PIN generators
- Hub pages: /word-tools/, /name-generators/, /other-generators/, /account-tools/, /number-chance/

**BROKEN — serves homepage content with wrong canonical:**
- /coin-flip/
- /random-number-generator/
- /dice-roller/
- Likely the entire /number-chance/ category

**Shown as "Coming soon" on hubs (not built):**
- Number & chance: every single tool (coin flip variants, number range pages, dice roller, wheel of names, Magic 8 ball, lottery, etc.)
- Writing: story prompts, writing prompt generator, lorem ipsum
- Word games: Scattergories, Catchphrase, Would You Rather, Truth or Dare, Couples T-or-D, Random Trivia, Dad Jokes
- Vocabulary: SAT, ESL, sight words, cool words, Gen Z words

---

## The growth math

Realistic break-down to 100K/mo (~3,300 visits/day):

| Source | Realistic share | Notes |
|---|---|---|
| Top 10 strong pages (existing + new) | 40–50K/mo | Need 5–10 top-3 rankings on KD 20–40 terms |
| Programmatic long-tail (50+ pages, KD <25) | 30–40K/mo | Number ranges, letter pages, length pages |
| Linkable assets + blog | 5–15K/mo | Slower but compounds; brings backlinks |
| Brand + direct + referral | 5–10K/mo | Grows naturally with rest |

You won't get there from one hero page. You get there from 50–80 pages each pulling 500–2,000/mo, with 5–10 of them pulling 5,000+/mo.

---

## Deployment stages (in priority order)

### Stage 0 — Critical fixes (THIS WEEK, before anything else)
`01-STAGE-0-CRITICAL-FIXES.md`

Fix the broken /number-chance/ category routing. Rotate exposed API keys. Verify Search Console health. Without these fixes everything else under-performs.

### Stage 1 — Build the /number-chance/ cluster (weeks 1–4)
`02-STAGE-1-NUMBER-CHANCE.md`

The highest-ROI work on the entire site right now. The hub exists, the URLs are already linked from nav and homepage, and these are some of the lowest-competition tool keywords in the whole space. Programmatic structure means one template engine → 30+ pages. Realistic outcome: 15–30K visits/mo at maturity.

### Stage 2 — Existing tool improvements (weeks 3–6, parallel)
`05-EXISTING-TOOLS-IMPROVEMENTS.md`

Many already-built tools are missing things that would unlock more traffic: server-side static content, schema additions, better internal linking, depth content. This is high-leverage because the pages already exist and are indexed.

### Stage 3 — Word games cluster (weeks 5–8)
`03-STAGE-2-WORD-GAMES.md`

Would You Rather, Truth or Dare, Scattergories, Catchphrase, Random Trivia. Same template engine approach. Mid-KD but high commercial intent; many are already drafted in the word-tools hub.

### Stage 4 — Vocabulary cluster expansion (weeks 8–12)
`04-STAGE-3-VOCABULARY.md`

SAT, ESL, sight words, cool words, Gen Z words. Builds on the strength of your existing spelling bee pages (your best content) and rounds out the vocabulary cluster for topical authority.

### Stage 5 — Linkable assets + outreach (months 3–6)
`06-STAGE-4-LINKABLE-ASSETS.md`

5 data-driven assets designed to attract backlinks. Without backlinks you stall at ~5–10K/mo regardless of how many pages you build. This is the unlock for breaking through KD 25.

### Stage 6 — Long-tail expansion (months 4–12)
Picked from the highest-converting Stage 1–4 winners. Keep shipping programmatic variants. Refresh underperformers. Begin attacking medium-KD head terms only after you have 50+ ranking pages.

---

## What success looks like at each milestone

| Month | Done by then | Realistic monthly visits |
|---|---|---|
| 1 | Stage 0 complete, Stage 1 half built | 1–3K |
| 3 | Stage 1 done, Stage 2 in progress, top-3 rankings beginning | 5–10K |
| 6 | Stage 1–3 complete, 2 linkable assets live | 15–30K |
| 9 | Stage 4 complete, 10+ top-3 rankings on KD <30 terms | 35–60K |
| 12 | 5 linkable assets, 40+ backlinks, programmatic clusters maturing | 60–100K |
| 18 | First competitive (KD 40+) terms starting to rank | 120–200K |

These are realistic with consistent execution. They are not guaranteed — Google can update, niches shift, and search behavior changes. The plan adapts as data comes in.

---

## How to use this plan

Each stage MD has:
- **Why this stage now** — the keyword logic
- **Target keywords** with rough volume and KD estimates (always verify before building)
- **Page-by-page build list** with target URLs and one-line descriptions
- **Template approach** — what to clone, what to vary
- **Claude Code prompt** ready to paste
- **Success metrics** — when the stage is "done"

Work through them in order. Don't skip ahead. Stage 0 first, always.

---

## Three principles worth holding to

1. **One URL, one intent.** Never collapse multiple tools onto one page to "save effort." Google rewards specific landing pages for specific queries.
2. **Server-render the answer.** Every tool page must show actual words/numbers/results in the raw HTML, not just a "Generating…" placeholder. Google won't wait for your JS.
3. **Depth beats breadth eventually.** 30 deep pages outrank 300 shallow ones. The 5th grade spelling bee page is the model — match it.

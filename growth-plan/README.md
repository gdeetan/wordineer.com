# Wordineer Growth Plan

A complete, sequenced plan for taking Wordineer from its current state to 100K+ monthly organic visits.

This isn't a "do everything at once" plan. It's stage-by-stage, with each stage building on the previous one. Each stage has its own MD file with target keywords, build order, Claude Code prompts, and success metrics.

---

## If you only read one thing

Read **[`00-MASTER-PLAN.md`](./00-MASTER-PLAN.md)**.

It contains the strategy, the realistic timeline, what success looks like at each milestone, and which stage to do when.

---

## File guide

| File | What's in it | When to read |
|---|---|---|
| `00-MASTER-PLAN.md` | Strategy, timeline, stage sequencing, growth math | First, before everything |
| `AUDIT.md` | What's live, what's broken, what's "Coming soon", critical issues found | Second — context for every stage |
| `01-STAGE-0-CRITICAL-FIXES.md` | URGENT — broken pages, exposed API keys, Search Console health | THIS WEEK |
| `02-STAGE-1-NUMBER-CHANCE.md` | Build the entire number-chance cluster (25+ pages) | Weeks 1–4 |
| `03-STAGE-2-WORD-GAMES.md` | Build the word games cluster (Would You Rather, T-or-D, Scattergories, etc.) | Weeks 5–8 |
| `04-STAGE-3-VOCABULARY.md` | Build the vocabulary cluster (SAT, ESL, sight words, cool words) | Weeks 8–12 |
| `05-STAGE-4-LINKABLE-ASSETS.md` | 5 backlink-attracting content pieces + outreach playbook | Months 3–6 |
| `06-EXISTING-TOOLS-IMPROVEMENTS.md` | Improvements for already-published pages (parallel to other stages) | Continuous |

---

## The critical findings (you should know these now)

These came out of inspecting your live site directly. They affect the urgency of various stages:

### 1. The /number-chance/ category is currently broken
URLs like `/coin-flip/`, `/random-number-generator/`, `/dice-roller/` return the homepage content with `canonical="https://wordineer.com/"`. **This means Google treats them as duplicates of the homepage and won't index them.** It's also diluting your homepage's topical relevance for "random word generator" because dozens of links across your site point to "Flip a Coin", "Dice Roller", etc., all of which currently resolve to the same homepage URL.

**Fix path:** Stage 1 (Number & Chance build) covers this comprehensively. Until Stage 1 ships, remove those URLs from your nav and homepage to stop the bleed.

### 2. API keys are exposed in client-side JavaScript
Your `random-word-generator.html` includes Wordnik and Merriam-Webster API keys in the page source. Anyone can view-source them. Stage 0 covers rotation and moving them behind a Cloudflare Worker.

### 3. The /spelling-bee-words-5th-grade/ page is genuinely outstanding
~2,500 words, audio pronunciation, practice mode, 4-week schedule, original explainer content. It's the strongest page on the site and the model for what depth wins look like. Reference it as the depth target whenever briefing new pages.

### 4. The "Coming soon" cards are a moderate negative signal
The /word-tools/ hub has 15+ unbuilt cards. /number-chance/ hub has 25+. Google sees a content-heavy hub linking to nothing-pages. Stages 1–3 fix the majority of these.

---

## The strategy in 3 sentences

1. Win the long tail first. Focus Stages 1–3 on low-competition keywords where you can realistically rank top 5–10 without authority you don't have yet.
2. While building, attract organic backlinks deliberately through Stage 4 linkable assets — this is the unlock for breaking past KD 30 and growing past ~10K visits/month.
3. Improve existing pages continuously in parallel — a page going from #15 to #5 brings more traffic than a brand-new page going from nothing to #20.

---

## The realistic timeline

**100,000 monthly visits is realistic by month 9–12** if you ship Stages 0–3 in the first 12 weeks, Stage 4 across months 3–6, and improve existing pages 2 hours/week throughout.

It is NOT realistic in 3–4 months from a new domain in this niche. Anyone telling you otherwise is selling something.

| Month | Realistic visits/mo |
|---|---|
| 1 | 1,000–3,000 |
| 3 | 5,000–10,000 |
| 6 | 15,000–30,000 |
| 9 | 35,000–60,000 |
| 12 | 60,000–100,000 |
| 18 | 120,000–200,000 |

---

## How to actually execute this

**Weekly cadence (10–20 hours):**
- 6–10 hrs: current stage's new builds (Stage 1, then 2, then 3)
- 2 hrs: existing tool improvements (rotate through priority list in `06-`)
- 1–2 hrs: outreach (after Stage 4 starts) — HARO, Reddit, resource page hunting
- 30 min: Search Console review every Monday — note what's ranking, what's not, what's broken
- 30 min: log progress in a simple tracker (spreadsheet or Notion)

**Monthly cadence:**
- Review which pages have improved/declined in rankings
- Refresh top 10 traffic pages with updated dates and examples
- Audit any new "Coming soon" cards — either build them or remove them

**Quarterly:**
- Re-run keyword research on top categories (verify the targets you're chasing are still valid)
- Audit competitors who started ranking ahead of you — what changed
- Run PageSpeed Insights on top 10 pages

---

## What "success" actually looks like

At each milestone, here's what you should be seeing:

**Month 3 (Stages 0+1+half of 2 done):**
- 30+ new tool pages live
- Number & Chance cluster fully built
- 5+ pages getting impressions in Search Console
- 1–2 pages in top 20 for their target query

**Month 6 (Stages 1+2+3 done, Asset 1+2 published):**
- 70+ tool pages live
- 10+ pages in top 20
- 3+ pages in top 10
- 25+ referring domains
- 15K–30K monthly visits

**Month 12 (all stages done, all 5 assets published, ongoing outreach):**
- 80–100 tool pages live (some retired, some refreshed)
- 30+ pages in top 10
- 60+ referring domains
- 60K–100K monthly visits

**Month 18:**
- Beginning to rank for KD 40+ terms
- Some medium-volume head terms breaking into top 5
- 120K–200K monthly visits

---

## The honest caveats

1. **Volume and KD estimates throughout these documents are directional, not exact.** I don't have live access to Ahrefs/Semrush. Always verify the top 20 target keywords per stage with the free tier of a real keyword tool before committing weeks of build effort.

2. **Google changes things.** A Helpful Content Update, an AI Overview rollout, or a niche-specific algorithm shift can change the math. The plan adapts. The principles (depth, server-rendering, internal linking, backlinks) don't.

3. **Niche competition shifts.** A new tool site could launch tomorrow and outrank you. The defense is depth — pages with 2,000 words of genuine value (like your 5th grade spelling bee page) are much harder to displace than thin pages.

4. **You are not guaranteed to hit 100K/month.** Most tool sites stall at 5K–15K because they don't ship Stage 4 (backlinks). You might be the exception. You might not. The plan gives you the best shot.

5. **Burnout is the biggest risk.** 50 weeks of consistent 10–20 hr/week execution is harder than it sounds. Build buffer. Take breaks. Ship quality over volume when forced to choose.

---

## A note on tone in these documents

Each file is written to be practical, not motivational. There are no "you got this!" cheerleader sections. There are honest caveats about what won't work, what's overhyped, and where the realistic ceiling lies.

The reason: a site this far along doesn't need motivation. It needs honest analysis and a clear sequence of work.

If at any point a stage isn't working as documented — pages aren't indexing, rankings aren't moving, traffic isn't appearing — that's a signal to stop and diagnose, not push harder. The plan is a hypothesis. Reality is the data.

Good luck. Start with Stage 0.

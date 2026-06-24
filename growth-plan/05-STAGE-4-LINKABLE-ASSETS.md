# Stage 4 — Linkable assets and outreach

**Goal:** Build 5 backlink-attracting "linkable assets" and run outreach campaigns to land 50–100 referring domains over 6 months.

**Why this stage now (months 3–6):**
- Stages 1–3 built ~50 new pages. They'll start ranking, but most will plateau at page 2–3 without backlinks.
- The site's Domain Rating / Domain Authority is the single biggest ceiling on what KD you can crack. A handful of strong backlinks lifts every page on the site.
- Tool sites have a hard time attracting links organically. You have to deliberately create link-worthy content separate from your tools.
- 30+ referring domains is roughly the threshold where KD 30–40 keywords become winnable.

**Realistic outcome:** 40–80 backlinks across the 5 assets and ongoing outreach over 6 months. This is the unlock for breaking past ~10K monthly visits.

**Estimated effort:** 6–10 hours per asset (build) + 8–12 hours per asset (outreach) = ~80 hours total across 6 months. About 3 hours/week sustained.

---

## What makes content "linkable"

Linkable assets share four properties:

1. **Comprehensive** — the most complete resource on a specific topic. "The ultimate guide to X" with actual depth, not 1,500 words of fluff.
2. **Original data or angle** — either data nobody else has analyzed, or a take/format nobody else has produced.
3. **Useful to a defined audience** — teachers, journalists, hobbyists, students, etc. — that audience must include people who run websites.
4. **Quotable/citable** — has specific facts, numbers, lists that a journalist or blogger can reference.

A "list of 100 cool words" is not linkable on its own — that's just a tool page. "The 100 cool words analyzed for etymological origin and frequency" with a downloadable PDF is linkable, because it gives someone a reason to cite you specifically.

---

## The 5 assets to build (in order)

### Asset 1: "The 1,000 Most Common 5-Letter Words in English (Analyzed by Vowel Pattern)"

**Why:** Wordle is still played by millions. Strategic Wordle content gets links from gaming blogs, education sites, and even mainstream news. You already have the data — your `words.json` plus word frequency data.

**Format:**
- Single long-form page (~3,000 words) at `/best-5-letter-words/` or `/common-5-letter-words/`
- Sortable, filterable HTML table with all 1,000 words showing: word, vowel pattern (e.g., "AEIOU" all five, "AE_OU", etc.), frequency rank, common letter positions
- Downloadable CSV and PDF versions
- Analysis section: "What are the most common vowel patterns?" "Best opening words by information theory" "Words with no repeated letters"
- One signature insight: e.g., "AROSE is the optimal opener because…" with actual reasoning

**Outreach targets (30–50 sites):**
- Wordle strategy bloggers (Tom's Hardware, NYT-affiliated content, indie Wordle blogs)
- Word game enthusiast sites (PuzzleNation, etc.)
- Linguistics blogs
- Education and writing teachers who use word frequency data
- Reddit r/wordle (don't spam; share genuinely once)
- HackerNews "Show HN" if framed as a data analysis project

**Realistic backlinks:** 8–15 from this single asset over 60 days.

---

### Asset 2: "The 500 Hardest Spelling Bee Words by Grade Level (Free Printable PDF)"

**Why:** You have the strongest spelling bee content on the site (your K-7 pages are excellent). A consolidated mega-resource with downloadable PDFs is exactly what spelling bee parents, teachers, and homeschoolers link to.

**Format:**
- Single comprehensive page at `/spelling-bee-words-printable/`
- Curated 500 hardest words, organized by grade level (K-12)
- Each word has: word, syllabification, definition, etymology, audio button, example sentence
- Major asset: a single combined PDF (or multiple grade-level PDFs) ready to print
- Tied to your spelling bee tool pages with strong internal linking

**Outreach targets:**
- Homeschool blogs and resource pages (this is a HUGE audience and they link generously)
- Spelling bee parent communities (Facebook groups, blogs)
- Teacher pay teacher resources (link from blog posts, not store)
- District and school PTA pages
- HARO journalist queries about spelling bees (especially around Scripps National Spelling Bee in May/June)

**Realistic backlinks:** 15–25 over 90 days. Education niche links are unusually durable.

---

### Asset 3: "Every Wordle Answer (Searchable + Solver)"

**Why:** Wordle has a defined, finite answer set. Many sites maintain lists; few combine it with a smart solver. If your solver is genuinely better than competitors, this becomes the canonical resource.

**Format:**
- `/wordle-answers/` — searchable archive of past Wordle answers with dates
- Tied to your existing `/wordle-game/` for backlink reciprocity
- The solver: enter known letters + positions + excluded letters, get a ranked list of remaining possible answers
- A "today's hints" section that doesn't spoil the answer

**Outreach targets:**
- Same Wordle community as Asset 1
- TechRadar / Tom's Hardware (they publish Wordle hint articles daily and link to solvers)
- Game-news aggregators

**Realistic backlinks:** 10–20 over 60 days. This asset can spike traffic dramatically when picked up by tech press.

**Caution:** Keep this strictly informational — Wordle is owned by NYT and they're protective of the brand. Don't replicate the game itself (your `/wordle-game/` is technically a "guess a 5-letter word" game with similar rules — different from "the Wordle"). Don't use NYT's logos or specific branding.

---

### Asset 4: "A Vocabulary List for ESL Learners (CEFR-Tagged, A1–C2)"

**Why:** ESL is the single most link-friendly education niche. ESL teachers maintain blogs and resource lists. International education sites publish curated lists. Solid CEFR-tagged content gets cited.

**Format:**
- `/esl-vocabulary-cefr/` (or fold into the ESL vocab page from Stage 3)
- 1,500–2,000 carefully chosen words tagged with CEFR level (A1 beginner → C2 mastery)
- Each word with: definition in plain English, IPA pronunciation, audio button, example sentence at appropriate level, part of speech
- Downloadable: separate PDFs per CEFR level
- Filter by topic (food, travel, work, family, etc.)

**Outreach targets:**
- ESL teacher blogs (very generous link culture in this community)
- Reddit r/EnglishLearning, r/EFL (share, don't spam)
- ESL news and resource aggregators
- Cambridge, IELTS, TOEFL prep sites and blogs
- International school resource pages

**Realistic backlinks:** 12–20 over 90 days. ESL teachers refer their students to good resources and link from their teaching blogs.

---

### Asset 5: "The Etymology of 100 Common English Words You Use Every Day"

**Why:** Etymology is widely shared on social media (interesting word origins go viral). Pairs well with your random word generator brand. Attracts links from writing blogs, etymology enthusiasts, and education sites.

**Format:**
- `/etymology-100-common-words/`
- 100 words with: modern definition, root language, full etymology history with dates, related modern words
- Visual etymology trees for at least 10 of them (SVG family-tree style diagrams)
- Categorized: words from Latin, Greek, Old Norse, French, Arabic, German, Spanish, others
- A signature insight: "Why does English have so many words for the same thing?" (the Norman Conquest answer)

**Outreach targets:**
- r/etymology, r/linguistics, r/words (treasure trove of linkers)
- Etymology Online (the canonical site; reach out for a reciprocal mention or guest contribution)
- Writing blogs (etymology = "fascinating word origins" content)
- Twitter (etymology threads go viral; Tweet a teaser linking to the page)
- HARO journalist queries about language and writing
- College and university linguistics department resource pages

**Realistic backlinks:** 10–15 over 90 days, plus social shares that bring direct traffic.

---

## Outreach playbook

This is the part most tool sites skip. Don't.

### Phase 1: Set up tracking (one hour, once)

- Make a Google Sheet with columns: Date, Asset, Target site, Contact name, Contact email, Pitch sent (Y/N), Reply (Y/N), Link landed (Y/N), Notes
- This is your outreach CRM. You'll log every outreach contact here.

### Phase 2: Build the target list per asset (2-3 hours per asset)

For each asset, build a list of 50–80 specific sites you'll pitch:

- **Find them:** Use these Google searches:
  - `[your topic] "resources"` (e.g., `spelling bee "resources"`)
  - `[your topic] "useful links"`
  - `[your topic] inurl:resources`
  - `[topic] blog inurl:blog`
  - `intext:"link to" [your topic]`
- **Qualify:** the site should have a blog or resource page where your asset would naturally fit. Skip sites that haven't been updated in 2+ years.
- **Find a contact:** look for a contact page, then a specific person's email if possible. Generic `info@` and `hello@` rarely respond.

### Phase 3: Outreach email templates

Three templates per outreach round. Adapt the tone, never blast identical emails.

**Template 1 — Resource page suggestion:**

```
Subject: Resource for your [page title]

Hi [name],

I saw your [resource page] on [their site] — really useful list, especially [specific item you actually noticed].

I built a free [asset description] at [URL] that covers [specific value]. Thought it might be a fit for your list if you ever update it.

No worries either way — the page is free to use regardless.

[Your name]
Wordineer
```

Three sentences. No flattery beyond a specific genuine observation. No "I noticed your DA is X." No backlink request.

**Template 2 — Journalist pitch (HARO/Connectively style):**

```
Subject: [Reporter request topic] — quick stat from word frequency analysis

Hi [name],

Saw your query about [topic]. Here's a relevant data point: [one specific quantitative finding from your asset].

Full data and methodology at [URL] if you want to cite or expand.

Happy to provide additional analysis if useful for the piece.

[Your name]
Wordineer (free word and language tools)
```

**Template 3 — Reciprocal mention:**

```
Subject: [Your asset topic] — built this and thought of your work on [their related piece]

Hi [name],

Your post on [their specific piece] is one of the better takes I've read on [topic]. I just published [your asset] which goes deeper on [specific angle they didn't cover].

[URL] — happy to chat about it, swap notes, or whatever.

[Your name]
Wordineer
```

### Phase 4: The send schedule

- 5–10 outreach emails per day, max
- Send Tuesday-Thursday, mornings local time of the recipient
- Wait 7 days. Send ONE follow-up if no response. Then move on.
- Track every send in your sheet.
- Expect 5–15% reply rate. Of replies, expect 30–50% to result in a link.
- So 100 outreach emails = ~7-15 links. Quality of asset matters more than volume of outreach.

---

## Ongoing background tactics (in addition to asset outreach)

These run continuously, not as discrete campaigns.

### 1. HARO / Connectively / Qwoted (30 min/day)

Sign up. Reply to journalist queries about:
- Vocabulary, spelling, language education
- Word games, puzzles, Wordle
- Party games, family games
- Random tools and decision-making
- Productivity and writing tools

Most pitches won't land. The ones that do drop you on real publications (USA Today, HuffPost, niche industry magazines) which compound dramatically in Google's eyes.

### 2. Reddit (15-20 min/day, 5 days/week)

Become a contributor in r/teachers, r/homeschool, r/EnglishLearning, r/wordle, r/Pictionary, r/Etymology, r/SAT, r/writing.

Comment helpfully 10 times for every 1 time you link your tool. Mods detect spammers; the slow-build approach works.

### 3. Indie Hackers + Product Hunt (one-time launches)

- Indie Hackers: post your "milestone" updates monthly. Other founders link back.
- Product Hunt: launch each major asset (not the tool site itself again) as a separate PH launch. PH backlinks aren't huge but they bring real traffic and other linkers see them.

### 4. Quora (10 min/day, 3 days/week)

Answer questions in your topic areas. Link to your tool only when it's genuinely the best answer. Quora answers themselves rank in Google and bring referral traffic.

### 5. Resource page hunting (monthly)

Search `[your tool keyword] "resources"` once a month, find new resource pages, pitch each one. Resource pages keep popping up; ongoing harvesting compounds.

### 6. Niche forums

Wordsmith forums, education forums, party-game forums. Become a regular. Share tools only when genuinely useful.

---

## What NOT to do

- **Don't buy links.** Fiverr "DA 50 guest posts for $30" are PBNs that will tank your rankings within 6 months when Google detects the network.
- **Don't do link exchanges at scale.** A single reciprocal link from a relevant site is fine. Twenty exchanged links across the same set of sites is detectable and dangerous.
- **Don't send identical mass emails.** Every outreach email must be visibly customized to the recipient.
- **Don't ask for links directly.** Offer value (your asset). If it's useful, they'll link. Asking for a link in the first email is the fastest path to the spam folder.
- **Don't follow up more than once.** People are busy. One follow-up is courtesy; three is harassment.
- **Don't optimize anchor text.** Your backlinks should mostly use your brand name or natural text. A profile dominated by keyword-rich anchor text looks unnatural.

---

## Realistic backlink trajectory

| Month | Target referring domains | Source mix |
|---|---|---|
| 3 | 10 | Existing organic links + Asset 1 outreach |
| 6 | 30 | Assets 1-2 + HARO + Reddit/Quora ongoing |
| 9 | 55 | Assets 1-4 + niche guest posts + ongoing |
| 12 | 80 | All 5 assets + sustained outreach |

At 50+ referring domains, you can credibly rank for KD 30–40 terms. At 100+, KD 50 becomes possible.

---

## Linking this to traffic

A common mistake: thinking backlinks directly cause traffic. They don't — directly. They lift your rankings, which lift your CTR, which compounds across all your pages.

A new spelling-bee page with 0 backlinks might rank #28 for "spelling bee words 3rd grade". With 30 referring domains across the site, that same page now ranks #12. With 80 referring domains, #5. Same content. Different rankings. Massively different traffic.

That's why this stage matters more than building 30 more pages once you have 50 already.

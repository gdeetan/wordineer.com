# Random Adverb Generator Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a Random Adverb Generator page at `/random-adverb-generator/` with adverb-type, difficulty, first-letter, and sort filters — the most capable adverb generator in search results.

**Architecture:** Create `adverbs.json` dataset → add `advTypeId` + `sortId` to the tool engine → build the tool page following the noun/adjective generator pattern → activate the word-tools hub link.

**Tech Stack:** Static HTML/CSS/JS, WORDINEER IIFE engine (`tool-engine.js`), Python build system (`build.py`), Cloudflare Pages

---

## Files

| Action | Path |
|--------|------|
| Create | `wordineer-deploy/data/adverbs.json` |
| Modify | `wordineer-deploy/scripts/tool-engine.js` |
| Modify | `template-deploy/template/footer.html` |
| Create | `template-deploy/tools-src/random-adverb-generator.html` |
| Modify | `template-deploy/tools-src/word-tools.html` |
| Modify | `template-deploy/tools.json` |
| Build output | `template-deploy/output/random-adverb-generator.html` |
| Deploy copy | `wordineer-deploy/random-adverb-generator.html` |

---

## Task 1: Create adverbs.json dataset

**Files:**
- Create: `wordineer-deploy/data/adverbs.json`

### Schema

Each entry:
```json
{ "w": "Quickly", "t": "adverb", "advType": "manner", "d": "at a fast speed", "diff": "easy", "borrowed": false }
```

Fields:
- `w` — word, title-case
- `t` — always `"adverb"`
- `advType` — `"manner"` | `"time"` | `"place"` | `"degree"` | `"frequency"`
- `d` — definition, max ~100 chars, lowercase, no trailing period
- `diff` — `"easy"` | `"medium"` | `"hard"`
- `borrowed` — `false` for native English, `true` for loanwords

### advType definitions
- `manner` — how an action is done (quickly, carefully, boldly, gracefully)
- `time` — when something happens (yesterday, soon, already, immediately)
- `place` — where something happens (here, nearby, everywhere, upstairs)
- `degree` — how much / to what extent (very, quite, almost, barely, extremely)
- `frequency` — how often (always, rarely, sometimes, daily, occasionally)

### Distribution target: ~500 entries total

| advType | Easy | Medium | Hard | Subtotal |
|---------|------|--------|------|----------|
| manner | 20 | 40 | 40 | ~100 |
| time | 15 | 35 | 30 | ~80 |
| place | 15 | 30 | 25 | ~70 |
| degree | 15 | 35 | 30 | ~80 |
| frequency | 20 | 40 | 40 | ~100 |
| **Total** | ~85 | ~180 | ~165 | **~500** |

### Sample entries (write the full file following these patterns)

```json
[
  { "w": "Quickly", "t": "adverb", "advType": "manner", "d": "at a fast speed", "diff": "easy", "borrowed": false },
  { "w": "Slowly", "t": "adverb", "advType": "manner", "d": "at a low speed; not fast", "diff": "easy", "borrowed": false },
  { "w": "Carefully", "t": "adverb", "advType": "manner", "d": "with attention and caution", "diff": "easy", "borrowed": false },
  { "w": "Boldly", "t": "adverb", "advType": "manner", "d": "in a confident and courageous way", "diff": "easy", "borrowed": false },
  { "w": "Gently", "t": "adverb", "advType": "manner", "d": "in a mild or soft manner", "diff": "easy", "borrowed": false },
  { "w": "Fiercely", "t": "adverb", "advType": "manner", "d": "in a violent or intense way", "diff": "medium", "borrowed": false },
  { "w": "Gracefully", "t": "adverb", "advType": "manner", "d": "in a smooth and elegant manner", "diff": "medium", "borrowed": false },
  { "w": "Tenaciously", "t": "adverb", "advType": "manner", "d": "with great persistence and determination", "diff": "hard", "borrowed": false },
  { "w": "Surreptitiously", "t": "adverb", "advType": "manner", "d": "in a secret or stealthy way", "diff": "hard", "borrowed": false },
  { "w": "Now", "t": "adverb", "advType": "time", "d": "at the present moment", "diff": "easy", "borrowed": false },
  { "w": "Soon", "t": "adverb", "advType": "time", "d": "in a short time from now", "diff": "easy", "borrowed": false },
  { "w": "Yesterday", "t": "adverb", "advType": "time", "d": "on the day before today", "diff": "easy", "borrowed": false },
  { "w": "Already", "t": "adverb", "advType": "time", "d": "before the time expected or specified", "diff": "easy", "borrowed": false },
  { "w": "Eventually", "t": "adverb", "advType": "time", "d": "at some later time; in the end", "diff": "medium", "borrowed": false },
  { "w": "Immediately", "t": "adverb", "advType": "time", "d": "without any delay; right away", "diff": "medium", "borrowed": false },
  { "w": "Posthumously", "t": "adverb", "advType": "time", "d": "after the death of the person concerned", "diff": "hard", "borrowed": false },
  { "w": "Here", "t": "adverb", "advType": "place", "d": "in, at, or to this place", "diff": "easy", "borrowed": false },
  { "w": "There", "t": "adverb", "advType": "place", "d": "in, at, or to that place", "diff": "easy", "borrowed": false },
  { "w": "Nearby", "t": "adverb", "advType": "place", "d": "not far away; close at hand", "diff": "easy", "borrowed": false },
  { "w": "Everywhere", "t": "adverb", "advType": "place", "d": "in all places; all over", "diff": "easy", "borrowed": false },
  { "w": "Upstairs", "t": "adverb", "advType": "place", "d": "on or to a higher floor of a building", "diff": "medium", "borrowed": false },
  { "w": "Outdoors", "t": "adverb", "advType": "place", "d": "outside a building; in the open air", "diff": "medium", "borrowed": false },
  { "w": "Very", "t": "adverb", "advType": "degree", "d": "to a high degree; extremely", "diff": "easy", "borrowed": false },
  { "w": "Quite", "t": "adverb", "advType": "degree", "d": "to a moderate extent; fairly", "diff": "easy", "borrowed": false },
  { "w": "Almost", "t": "adverb", "advType": "degree", "d": "not quite; very nearly", "diff": "easy", "borrowed": false },
  { "w": "Barely", "t": "adverb", "advType": "degree", "d": "only just; hardly", "diff": "medium", "borrowed": false },
  { "w": "Profoundly", "t": "adverb", "advType": "degree", "d": "to a very great depth; intensely", "diff": "hard", "borrowed": false },
  { "w": "Always", "t": "adverb", "advType": "frequency", "d": "at all times; on every occasion", "diff": "easy", "borrowed": false },
  { "w": "Never", "t": "adverb", "advType": "frequency", "d": "not ever; at no time", "diff": "easy", "borrowed": false },
  { "w": "Often", "t": "adverb", "advType": "frequency", "d": "many times; frequently", "diff": "easy", "borrowed": false },
  { "w": "Rarely", "t": "adverb", "advType": "frequency", "d": "not very often; seldom", "diff": "easy", "borrowed": false },
  { "w": "Sometimes", "t": "adverb", "advType": "frequency", "d": "occasionally; now and then", "diff": "easy", "borrowed": false },
  { "w": "Occasionally", "t": "adverb", "advType": "frequency", "d": "at infrequent or irregular intervals", "diff": "medium", "borrowed": false },
  { "w": "Intermittently", "t": "adverb", "advType": "frequency", "d": "stopping and starting at irregular intervals", "diff": "hard", "borrowed": false },
  { "w": "Sporadically", "t": "adverb", "advType": "frequency", "d": "occurring at irregular and infrequent intervals", "diff": "hard", "borrowed": false }
]
```

- [ ] **Step 1: Write the full adverbs.json file**

Create `wordineer-deploy/data/adverbs.json` as a JSON array. Follow the schema and sample entries above. Write ~500 entries covering all 5 `advType` values, all 3 `diff` levels, using the distribution table. Every entry must have a non-empty `d` field under ~100 chars.

- [ ] **Step 2: Validate JSON structure**

```bash
python3 -c "
import json, sys
data = json.load(open('wordineer-deploy/data/adverbs.json'))
types = {e['advType'] for e in data}
diffs = {e['diff'] for e in data}
print(f'Count: {len(data)}')
print(f'advTypes: {sorted(types)}')
print(f'diffs: {sorted(diffs)}')
by_type = {}
for e in data:
    by_type[e['advType']] = by_type.get(e['advType'], 0) + 1
for k,v in sorted(by_type.items()): print(f'  {k}: {v}')
missing_d = [e[\"w\"] for e in data if not e.get(\"d\")]
if missing_d: print(f'Missing definitions: {missing_d}')
else: print('All definitions present')
"
```

Expected output:
```
Count: 490-510
advTypes: ['degree', 'frequency', 'manner', 'place', 'time']
diffs: ['easy', 'hard', 'medium']
  degree: ~80
  frequency: ~100
  manner: ~100
  place: ~70
  time: ~80
All definitions present
```

- [ ] **Step 3: Commit**

```bash
git add wordineer-deploy/data/adverbs.json
git commit -m "feat: add adverbs.json dataset (~500 entries, 5 types, 3 difficulty levels)"
```

---

## Task 2: Update tool-engine.js — add advTypeId and sortId

**Files:**
- Modify: `wordineer-deploy/scripts/tool-engine.js`

The engine currently supports `nounTypeId`, `verbTypeId`, `adjTypeId`. Add `advTypeId` and `sortId` following the same pattern.

Current version: `?v=23`. New version after this task: `?v=24`.

- [ ] **Step 1: Add advType filter retrieval (line 275 area)**

Find this block (lines 273–275):
```js
const nounType = config.nounTypeId ? (document.getElementById(config.nounTypeId)?.value || 'all') : null;
const verbType = config.verbTypeId ? (document.getElementById(config.verbTypeId)?.value || 'all') : null;
const adjType  = config.adjTypeId  ? (document.getElementById(config.adjTypeId)?.value  || 'all') : null;
```

Add one line immediately after:
```js
const nounType = config.nounTypeId ? (document.getElementById(config.nounTypeId)?.value || 'all') : null;
const verbType = config.verbTypeId ? (document.getElementById(config.verbTypeId)?.value || 'all') : null;
const adjType  = config.adjTypeId  ? (document.getElementById(config.adjTypeId)?.value  || 'all') : null;
const advType  = config.advTypeId  ? (document.getElementById(config.advTypeId)?.value  || 'all') : null;
```

- [ ] **Step 2: Add advType filter logic (line 285 area)**

Find this block (lines 283–285):
```js
if (nounType && nounType !== 'all' && w.nt !== nounType) return false;
if (verbType && verbType !== 'all' && w.vt !== verbType) return false;
if (adjType  && adjType  !== 'all' && w.at !== adjType)  return false;
```

Add one line immediately after:
```js
if (nounType && nounType !== 'all' && w.nt !== nounType) return false;
if (verbType && verbType !== 'all' && w.vt !== verbType) return false;
if (adjType  && adjType  !== 'all' && w.at !== adjType)  return false;
if (advType  && advType  !== 'all' && w.advType !== advType)  return false;
```

- [ ] **Step 3: Add sortId to config mapping (line 648 area)**

Find this block (lines 646–649):
```js
nounTypeId:     cfg.nounTypeId     || null,
verbTypeId:     cfg.verbTypeId     || null,
adjTypeId:      cfg.adjTypeId      || null,
dataUrl:        cfg.dataUrl        || null,
```

Replace with:
```js
nounTypeId:     cfg.nounTypeId     || null,
verbTypeId:     cfg.verbTypeId     || null,
adjTypeId:      cfg.adjTypeId      || null,
advTypeId:      cfg.advTypeId      || null,
sortId:         cfg.sortId         || null,
dataUrl:        cfg.dataUrl        || null,
```

- [ ] **Step 4: Add sort logic (line 299 area)**

Find this line (line 299):
```js
const shuffled = [...pool].sort(() => Math.random() - 0.5);
```

Replace with:
```js
const sortEl = config.sortId ? document.getElementById(config.sortId) : null;
const shuffled = (sortEl?.checked)
  ? [...pool].sort((a, b) => a.w.localeCompare(b.w))
  : [...pool].sort(() => Math.random() - 0.5);
```

- [ ] **Step 5: Bump version in footer.html**

File: `template-deploy/template/footer.html` line 24.

Find:
```html
<script src="/scripts/tool-engine.js?v=23"></script>
```

Replace with:
```html
<script src="/scripts/tool-engine.js?v=24"></script>
```

- [ ] **Step 6: Commit**

```bash
git add wordineer-deploy/scripts/tool-engine.js template-deploy/template/footer.html
git commit -m "feat: add advTypeId and sortId support to tool engine, bump v24"
```

---

## Task 3: Create random-adverb-generator.html

**Files:**
- Create: `template-deploy/tools-src/random-adverb-generator.html`

Use `template-deploy/tools-src/random-noun-generator.html` as the structural reference. Copy the full page structure, then make adverb-specific changes below.

- [ ] **Step 1: Write the CONFIG block**

```html
<!-- CONFIG
{ "url": "/random-adverb-generator/", "output": "random-adverb-generator.html", "type": "tool" }
-->
```

- [ ] **Step 2: Write SLOT:meta**

```html
<!-- SLOT:meta -->
<title>Random Adverb Generator — Free Online Tool | Wordineer</title>
<meta name="description" content="Generate random English adverbs instantly. Filter by type (manner, time, place, degree, frequency), difficulty, and starting letter. Definitions included — free, no sign-up.">
<link rel="canonical" href="https://wordineer.com/random-adverb-generator/">
<meta property="og:title" content="Random Adverb Generator">
<meta property="og:description" content="Generate random English adverbs with filters for type, difficulty, and starting letter. Definitions included.">
<meta property="og:url" content="https://wordineer.com/random-adverb-generator/">
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "WebApplication",
  "name": "Random Adverb Generator",
  "url": "https://wordineer.com/random-adverb-generator/",
  "description": "Generate random English adverbs. Filter by adverb type, difficulty level, and starting letter. Definitions included.",
  "applicationCategory": "UtilitiesApplication",
  "operatingSystem": "Any",
  "offers": { "@type": "Offer", "price": "0", "priceCurrency": "USD" }
}
</script>
<!-- /SLOT:meta -->
```

- [ ] **Step 3: Write SLOT:style**

Copy the full style block from `random-noun-generator.html` SLOT:style verbatim. It covers `.tool-wrap`, `.tool-card`, `.tool-split`, `.ctrl`, `.ctrl-row`, `.ctrl-label`, `.word-item`, `.word-def`, `.badge-*`, mobile toggle styles. No adverb-specific styles needed.

- [ ] **Step 4: Write SLOT:hero**

```html
<!-- SLOT:hero -->
<div class="breadcrumb">
  <div class="breadcrumb-inner">
    <a href="/">Wordineer</a>
    <span class="breadcrumb-sep">›</span>
    <a href="/word-tools/">Word Tools</a>
    <span class="breadcrumb-sep">›</span>
    <span aria-current="page">Random Adverb Generator</span>
  </div>
</div>
<div class="trust-badge">
  <svg viewBox="0 0 11 11" fill="none"><circle cx="5.5" cy="5.5" r="4.5" stroke="#3C3489" stroke-width="1"/><path d="M3.5 5.5l1.5 1.5L8 3.5" stroke="#3C3489" stroke-width="1.2" stroke-linecap="round"/></svg>
  Free · No sign-up · Instant
</div>
<h1>Random adverb generator</h1>
<p>Generate random English adverbs instantly — filter by adverb type, difficulty, and starting letter. The only adverb generator with manner, time, place, degree, and frequency filters built in.</p>
<!-- /SLOT:hero -->
```

- [ ] **Step 5: Write SLOT:tool**

```html
<!-- SLOT:tool -->
<div class="tool-wrap">
  <div class="tool-card">
    <div class="tool-split">

      <div class="ctrl">
        <select id="ctrl-type" style="display:none"><option value="adverb">adverb</option></select>
        <div class="ctrl-row">
          <label class="ctrl-label" for="ctrl-count">Number of adverbs</label>
          <input type="number" id="ctrl-count" value="10" min="1" max="50" inputmode="numeric" aria-describedby="count-error">
          <span class="count-error" id="count-error">Enter a number from 1 to 50</span>
        </div>
        <button type="button" class="mobile-more-toggle" id="mobile-more-toggle" aria-expanded="false" aria-controls="advanced-options">Toggle More Options</button>
        <div class="advanced-options" id="advanced-options">
          <div class="ctrl-row">
            <label class="ctrl-label" for="ctrl-adverb-type">Adverb type</label>
            <select id="ctrl-adverb-type">
              <option value="all">All types</option>
              <option value="manner">Manner</option>
              <option value="time">Time</option>
              <option value="place">Place</option>
              <option value="degree">Degree</option>
              <option value="frequency">Frequency</option>
            </select>
          </div>
          <div class="ctrl-row">
            <label class="ctrl-label" for="ctrl-diff">Difficulty</label>
            <select id="ctrl-diff">
              <option value="all">All levels</option>
              <option value="easy">Easy (common)</option>
              <option value="medium">Medium</option>
              <option value="hard">Advanced / rare</option>
            </select>
          </div>
          <div class="ctrl-row">
            <label class="ctrl-label" for="ctrl-first">First letter</label>
            <input type="text" id="ctrl-first" maxlength="1" placeholder="A" aria-label="First letter" style="text-transform:uppercase;text-align:center;">
          </div>
          <div class="def-row">
            <label class="toggle" aria-label="Show definitions"><input type="checkbox" id="ctrl-defs" checked><span class="toggle-sl"></span></label>
            <label for="ctrl-defs">Show definitions</label>
          </div>
          <div class="def-row">
            <label class="toggle" aria-label="Sort A–Z"><input type="checkbox" id="ctrl-sort"><span class="toggle-sl"></span></label>
            <label for="ctrl-sort">Sort A–Z</label>
          </div>
        </div>
        <button class="gen-btn" id="word-gen-btn">Generate adverbs</button>
        <button class="reset-btn" onclick="WORDINEER.reset()">Reset options</button>
        <div class="kbd">Press <kbd>Space</kbd> to regenerate</div>
        <div class="ad-sidebar">
          <span class="ad-sidebar-tag">Ad</span>
          <div class="ad-sidebar-logo">
            <svg viewBox="0 0 32 32" fill="none" width="32" height="32"><circle cx="16" cy="16" r="14" fill="#15a249"/><path d="M10 16c0-3.3 2.7-6 6-6s6 2.7 6 6-2.7 6-6 6" stroke="white" stroke-width="2" stroke-linecap="round"/><circle cx="16" cy="16" r="2.5" fill="white"/></svg>
            <span class="ad-sidebar-brand">Grammarly</span>
          </div>
          <div class="ad-sidebar-headline">Write with confidence</div>
          <div class="ad-sidebar-body">Fix grammar, improve clarity, and choose the right words — everywhere you write.</div>
          <a href="https://grammarly.com" target="_blank" rel="noopener" class="ad-sidebar-cta">Try free →</a>
          <div class="ad-sidebar-sub">Free plan · No credit card</div>
        </div>
      </div>

      <div class="words-panel">
        <div class="words-top">
          <span class="words-count" id="word-count">Generating…</span>
          <div class="words-actions">
            <button class="act-btn" onclick="WORDINEER.copyAll()">Copy all</button>
            <button class="act-btn" id="word-regen-btn">Regenerate</button>
          </div>
        </div>
        <ul class="word-list" id="word-list"></ul>
      </div>

    </div>
  </div>
</div>
<!-- /SLOT:tool -->
```

- [ ] **Step 6: Write SLOT:explainer**

Write the full explainer section (~700 words). Use plain, specific prose — no filler. Structure:

```html
<!-- SLOT:explainer -->
<div class="explainer">
  <h2>What is a Random Adverb Generator?</h2>
  <p>A random adverb generator picks English adverbs from a curated dataset and displays them on demand. This tool lets you filter results by adverb type (manner, time, place, degree, or frequency), difficulty level, and starting letter — so you get words that fit your exact need, not just a random pile of "-ly" words. Toggle definitions on to see what each word means, or sort results A–Z when you need an ordered list.</p>

  <h2>Why Use a Random Adverb Generator?</h2>
  <p>Writers reach for the same five adverbs out of habit — quickly, slowly, very, never, always. A random generator breaks that pattern by surfacing words you know but don't use. It's also practical for:</p>
  <ul>
    <li><strong>ESL learners</strong> building vocabulary at their level (use the Easy or Medium filter)</li>
    <li><strong>Teachers</strong> who need a word list for grammar exercises without spending 20 minutes compiling one</li>
    <li><strong>Game players</strong> who need random words for Pictionary, charades, or word games</li>
    <li><strong>Students</strong> studying the difference between adverb types for a grammar assignment</li>
    <li><strong>Editors</strong> scanning for weak adverb patterns — generating 20 alternatives makes it easy to spot a stronger word</li>
  </ul>

  <h2>The 5 Types of Adverbs Explained</h2>
  <p>Adverbs modify verbs, adjectives, and other adverbs. They fall into five main categories:</p>
  <ol>
    <li><strong>Manner</strong> — describes <em>how</em> an action is done. Examples: <em>quickly, carefully, boldly, awkwardly</em>. Usage: "She spoke <em>quietly</em>."</li>
    <li><strong>Time</strong> — describes <em>when</em> something happens. Examples: <em>yesterday, soon, already, immediately</em>. Usage: "He will arrive <em>shortly</em>."</li>
    <li><strong>Place</strong> — describes <em>where</em> something happens. Examples: <em>here, nearby, upstairs, everywhere</em>. Usage: "Leave the keys <em>there</em>."</li>
    <li><strong>Degree</strong> — describes <em>how much</em> or to what extent. Examples: <em>very, quite, barely, profoundly</em>. Usage: "The result was <em>surprisingly</em> accurate."</li>
    <li><strong>Frequency</strong> — describes <em>how often</em> something happens. Examples: <em>always, rarely, occasionally, daily</em>. Usage: "She <em>rarely</em> misses a deadline."</li>
  </ol>
  <p>Use the Adverb Type filter to focus on one category at a time — useful when you need a specific kind of modifier and don't want to sift through 500 words manually.</p>

  <h2>How It Works</h2>
  <p>Set your filters in the sidebar, then click <strong>Generate adverbs</strong> (or press Space to regenerate). The tool pulls from a dataset of over 500 curated English adverbs, each tagged by type and difficulty. Filters combine — you can ask for 15 hard manner adverbs starting with "S" and get exactly that. Toggle <strong>Show definitions</strong> to see a short meaning next to each word. Enable <strong>Sort A–Z</strong> to order results alphabetically, useful when building word lists. Click <strong>Copy all</strong> to copy the current results to your clipboard.</p>

  <h2>Best Practices for Using Adverbs in Writing</h2>
  <p>Adverbs are precise tools, not decoration. Used well, they add emphasis, timing, and nuance that would take a whole phrase to express otherwise. A few principles:</p>
  <ul>
    <li><strong>Choose specific over generic.</strong> "She spoke <em>hesitantly</em>" is stronger than "She spoke <em>in a hesitant way</em>" and sharper than just "She spoke <em>slowly</em>."</li>
    <li><strong>Vary by type.</strong> Overloading on manner adverbs ("-ly" words) makes prose feel labored. Mixing in frequency and degree adverbs ("rarely," "almost," "barely") keeps rhythm varied.</li>
    <li><strong>Place matters.</strong> "I <em>almost</em> never do that" and "I never <em>almost</em> do that" mean different things. Position your adverb next to what it modifies.</li>
    <li><strong>Use difficulty levels intentionally.</strong> Easy adverbs suit everyday writing and dialogue. Hard adverbs work for academic, literary, or technical contexts — but they'll stick out if the surrounding text is casual.</li>
  </ul>

  <h2>How to Avoid Adverb Overuse</h2>
  <p>The most common writing advice about adverbs is to cut them — but that's an oversimplification. The real goal is to avoid adverbs that prop up weak verbs. "He ran <em>quickly</em>" can usually become "He sprinted." But "She smiled <em>briefly</em>" works — there's no single verb for a short smile. Use this generator to find alternatives. If you're about to write "very sad," generate a few degree adverbs and you might land on "profoundly sad" or "barely holding it together." Adverb variation is faster than thesaurus-diving, and it surfaces words you already know.</p>
</div>
<!-- /SLOT:explainer -->
```

- [ ] **Step 7: Write SLOT:faq**

```html
<!-- SLOT:faq -->
<div class="faq">
  <h2 class="faq-title">Frequently asked questions</h2>

  <div class="faq-item open">
    <div class="faq-q"><span class="faq-q-text">What's the difference between an adverb and an adjective?</span><svg viewBox="0 0 12 12" fill="none"><path d="M2 4l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div>
    <div class="faq-a">Adjectives modify nouns ("a <em>quick</em> response"). Adverbs modify verbs, adjectives, or other adverbs ("she responded <em>quickly</em>"). The same root word often appears in both forms — "quick" (adjective) becomes "quickly" (adverb). A reliable test: if the word answers "how?", "when?", "where?", or "how often?" it's an adverb.</div>
  </div>

  <div class="faq-item">
    <div class="faq-q"><span class="faq-q-text">Can adverbs modify other adverbs?</span><svg viewBox="0 0 12 12" fill="none"><path d="M2 4l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div>
    <div class="faq-a">Yes. Degree adverbs like "very," "quite," and "barely" commonly stack on other adverbs: "She runs <em>incredibly</em> quickly." "He arrived <em>almost</em> immediately." This is grammatically correct and often more precise than a single word, but use it sparingly — stacking multiple adverbs in one sentence usually signals a verb that needs replacing.</div>
  </div>

  <div class="faq-item">
    <div class="faq-q"><span class="faq-q-text">Why should I vary the adverbs I use?</span><svg viewBox="0 0 12 12" fill="none"><path d="M2 4l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div>
    <div class="faq-a">Repetition is the most common cause of dull prose. If every action in your writing happens "quickly" or "suddenly," the reader stops registering those words. Varying across manner, degree, and frequency adverbs keeps readers engaged and gives your language texture — the difference between "She immediately, quietly, and deliberately left" versus "She left quickly, quickly, quickly."</div>
  </div>

  <div class="faq-item">
    <div class="faq-q"><span class="faq-q-text">How does the difficulty filter work?</span><svg viewBox="0 0 12 12" fill="none"><path d="M2 4l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div>
    <div class="faq-a"><strong>Easy</strong> words are common, high-frequency adverbs that most native speakers recognize immediately (quickly, never, here). <strong>Medium</strong> words are less common but widely understood (tenaciously, intermittently, profoundly). <strong>Hard</strong> words are rare, literary, or technical — useful for academic writing or vocabulary building but likely to puzzle a general audience.</div>
  </div>

  <div class="faq-item">
    <div class="faq-q"><span class="faq-q-text">What does the adverb type filter do?</span><svg viewBox="0 0 12 12" fill="none"><path d="M2 4l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div>
    <div class="faq-a">It restricts results to one grammatical category. Select <strong>Manner</strong> to get words like "gracefully" and "boldly" (how). Select <strong>Frequency</strong> for words like "rarely" and "always" (how often). This is useful when you know what kind of modifier you need — for example, a game that asks for a manner adverb specifically.</div>
  </div>

  <div class="faq-item">
    <div class="faq-q"><span class="faq-q-text">Is this tool free to use?</span><svg viewBox="0 0 12 12" fill="none"><path d="M2 4l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div>
    <div class="faq-a">Yes, completely free. No sign-up, no account, no usage limits. The tool runs entirely in your browser — nothing is sent to a server.</div>
  </div>
</div>
<!-- /SLOT:faq -->
```

- [ ] **Step 8: Write SLOT:who**

```html
<!-- SLOT:who -->
<div class="who">
  <h2>Who uses this tool?</h2>
  <div class="uc-grid">
    <div class="uc"><div class="uc-title">Fiction Writers</div><div class="uc-body">Generate manner and degree adverbs to vary sentence rhythm. Filter by difficulty to match your prose register — casual for dialogue, advanced for literary fiction.</div></div>
    <div class="uc"><div class="uc-title">Students &amp; ESL Learners</div><div class="uc-body">Filter by difficulty to target your level. Every adverb comes with a definition — vocabulary practice and grammar study in one tool.</div></div>
    <div class="uc"><div class="uc-title">Teachers</div><div class="uc-body">Build vocabulary lists and grammar exercises in seconds. Use the type filter to create worksheets focused on a single adverb category.</div></div>
    <div class="uc"><div class="uc-title">Game Players</div><div class="uc-body">Instant prompts for word games, Pictionary, and charades. Generate a batch, copy all, and you're ready.</div></div>
  </div>
</div>
<!-- /SLOT:who -->
```

- [ ] **Step 9: Write SLOT:init**

```html
<!-- SLOT:init -->
<script>
WORDINEER.init({
  listId:         'word-list',
  countId:        'ctrl-count',
  countDisplayId: 'word-count',
  typeId:         'ctrl-type',
  advTypeId:      'ctrl-adverb-type',
  diffId:         'ctrl-diff',
  firstId:        'ctrl-first',
  defsId:         'ctrl-defs',
  sortId:         'ctrl-sort',
  dataUrl:        '/data/adverbs.json',
});

(function(){
  const count = document.getElementById('ctrl-count');
  const toggle = document.getElementById('mobile-more-toggle');
  const advanced = document.getElementById('advanced-options');

  function setCountError(show) {
    const err = document.getElementById('count-error');
    if (err) err.classList.toggle('show', show);
    if (count) count.classList.toggle('input-error', show);
  }

  function validateAndGenerate() {
    const raw = parseInt(count?.value, 10);
    if (isNaN(raw) || raw < 1 || raw > 50) { setCountError(true); return; }
    setCountError(false);
    WORDINEER.generate();
  }

  document.getElementById('word-gen-btn')?.addEventListener('click', validateAndGenerate);
  document.getElementById('word-regen-btn')?.addEventListener('click', validateAndGenerate);

  if (count) {
    count.addEventListener('input', validateAndGenerate);
  }

  ['ctrl-adverb-type', 'ctrl-diff', 'ctrl-sort'].forEach(function(id) {
    const el = document.getElementById(id);
    if (!el) return;
    el.addEventListener('change', validateAndGenerate);
  });

  const firstEl = document.getElementById('ctrl-first');
  if (firstEl) firstEl.addEventListener('input', validateAndGenerate);

  if (toggle && advanced) {
    toggle.addEventListener('click', function(){
      const isOpen = advanced.classList.toggle('is-open');
      toggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
      toggle.textContent = isOpen ? 'Hide More Options' : 'Toggle More Options';
    });
  }
})();
</script>
<!-- /SLOT:init -->
```

- [ ] **Step 10: Commit**

```bash
git add template-deploy/tools-src/random-adverb-generator.html
git commit -m "feat: add random-adverb-generator.html tool page"
```

---

## Task 4: Update word-tools.html and tools.json

**Files:**
- Modify: `template-deploy/tools-src/word-tools.html` (line 270–274)
- Modify: `template-deploy/tools.json`

### word-tools.html

- [ ] **Step 1: Activate placeholder link**

Find (lines 270–274):
```html
        <div class="tool-item tool-item--soon">
          <div class="tool-icon" style="background:#E1F5EE"><svg viewBox="0 0 13 13" fill="none"><path d="M2.5 5.5h6M2.5 7.5h5" stroke="#1D9E75" stroke-width=".9" stroke-linecap="round"/><path d="M8 4l3 2.5-3 2.5" stroke="#1D9E75" stroke-width="1" stroke-linecap="round" stroke-linejoin="round"/></svg></div>
          <div class="tool-name">Random Adverbs <span class="soon-badge">Coming soon</span></div>
          <div class="tool-desc">How, when, where, and to what extent.</div>
        </div>
```

Replace with:
```html
        <a href="/random-adverb-generator/" class="tool-item">
          <div class="tool-icon" style="background:#E1F5EE"><svg viewBox="0 0 13 13" fill="none"><path d="M2.5 5.5h6M2.5 7.5h5" stroke="#1D9E75" stroke-width=".9" stroke-linecap="round"/><path d="M8 4l3 2.5-3 2.5" stroke="#1D9E75" stroke-width="1" stroke-linecap="round" stroke-linejoin="round"/></svg></div>
          <div class="tool-name">Random Adverbs</div>
          <div class="tool-desc">Filter by manner, time, place, degree, and frequency.</div>
        </a>
```

### tools.json — mega section

The `"mega"` section uses a simpler `{ href, text }` format grouped by category. The "Writing & Vocabulary" cat is at lines 3–12.

- [ ] **Step 2: Add to mega Writing & Vocabulary tools**

Find (lines 6–11):
```json
      "tools": [
        { "href": "/", "text": "Random Word Generator" },
        { "href": "/random-sentence-generator/", "text": "Random Sentence Generator" },
        { "href": "/random-paragraph-generator/", "text": "Random Paragraph Generator", "status": "planned" },
        { "href": "/word-counter/", "text": "Word Counter", "status": "planned" }
      ]
```

Replace with:
```json
      "tools": [
        { "href": "/", "text": "Random Word Generator" },
        { "href": "/random-sentence-generator/", "text": "Random Sentence Generator" },
        { "href": "/random-adverb-generator/", "text": "Random Adverb Generator" },
        { "href": "/random-paragraph-generator/", "text": "Random Paragraph Generator", "status": "planned" },
        { "href": "/word-counter/", "text": "Word Counter", "status": "planned" }
      ]
```

### tools.json — more_word_tools section

- [ ] **Step 3: Add to more_word_tools section**

Find the adjective generator entry in `"more_word_tools"` (around line 86):
```json
    {
      "href": "/random-adjective-generator/",
      "name": "Random Adjective Generator",
      "desc": "Generate random adjectives — filter by sentiment (positive, negative, neutral), difficulty, and starting letter. Definitions and comparative forms included.",
      "icon_bg": "#FEF3EE",
      "icon_path": "<path d=\"M2 4h9M2 7h6M2 10h8\" stroke=\"#C05621\" stroke-width=\"1.3\" stroke-linecap=\"round\"/><path d=\"M11 9.5l1.5 1-1.5 1\" stroke=\"#C05621\" stroke-width=\"1.1\" stroke-linecap=\"round\" stroke-linejoin=\"round\"/>"
    },
```

Add this entry immediately after it:
```json
    {
      "href": "/random-adverb-generator/",
      "name": "Random Adverb Generator",
      "desc": "Generate random adverbs — filter by type (manner, time, place, degree, frequency), difficulty, and starting letter. Definitions included.",
      "icon_bg": "#E1F5EE",
      "icon_path": "<path d=\"M2.5 5.5h6M2.5 7.5h5\" stroke=\"#1D9E75\" stroke-width=\".9\" stroke-linecap=\"round\"/><path d=\"M8 4l3 2.5-3 2.5\" stroke=\"#1D9E75\" stroke-width=\"1\" stroke-linecap=\"round\" stroke-linejoin=\"round\"/>"
    },
```

### tools.json — footer_cols section

- [ ] **Step 4: Add to footer_cols Writing & Vocabulary section**

Find the Writing & Vocabulary footer entry (around line 362):
```json
    {
      "title": "Writing &amp; Vocabulary",
      "view_all_href": "/word-tools/",
      "links": [
        { "href": "/", "text": "Random Word Generator" },
        { "href": "/random-sentence-generator/", "text": "Random Sentence Generator" },
        { "href": "/random-adjective-generator/", "text": "Random Adjective Generator" },
        { "href": "/random-paragraph-generator/", "text": "Random Paragraph Generator", "status": "planned" },
        { "href": "/word-counter/", "text": "Word Counter", "status": "planned" }
      ]
    },
```

Add the adverb link after the adjective entry:
```json
    {
      "title": "Writing &amp; Vocabulary",
      "view_all_href": "/word-tools/",
      "links": [
        { "href": "/", "text": "Random Word Generator" },
        { "href": "/random-sentence-generator/", "text": "Random Sentence Generator" },
        { "href": "/random-adjective-generator/", "text": "Random Adjective Generator" },
        { "href": "/random-adverb-generator/", "text": "Random Adverb Generator" },
        { "href": "/random-paragraph-generator/", "text": "Random Paragraph Generator", "status": "planned" },
        { "href": "/word-counter/", "text": "Word Counter", "status": "planned" }
      ]
    },
```

- [ ] **Step 5: Commit**

```bash
git add template-deploy/tools-src/word-tools.html template-deploy/tools.json
git commit -m "feat: activate Random Adverbs link in word-tools hub, add to tools.json registry"
```

---

## Task 5: Build, copy, preview, verify

**Files:**
- Build output: `template-deploy/output/random-adverb-generator.html`
- Deploy copy: `wordineer-deploy/random-adverb-generator.html`
- Also copies updated `word-tools.html` and all other pages (engine version bump v24)

- [ ] **Step 1: Run build**

```bash
cd template-deploy && python3 build.py
```

Expected: no errors, `output/random-adverb-generator.html` created.

- [ ] **Step 2: Copy output to deploy folder**

```bash
cp template-deploy/output/*.html wordineer-deploy/
```

- [ ] **Step 3: Start local preview server**

```bash
cd wordineer-deploy && python3 -m http.server 8080
```

Open `http://localhost:8080/random-adverb-generator.html` in browser.

- [ ] **Step 4: Verify tool functionality**

Check each item:

1. **Initial load** — page renders 10 adverbs immediately (from dataset), definitions visible
2. **Adverb type filter** — select "Manner" → all results have `advType: manner`. Select "Frequency" → all frequency adverbs. Select "All types" → mixed.
3. **Difficulty filter** — select "Easy" → only easy words. Select "Hard" → only hard/rare words.
4. **Combined filters** — set Type=Manner + Difficulty=Hard → only hard manner adverbs appear
5. **First letter filter** — type "S" → all results start with S
6. **Sort A–Z toggle** — enable → results sorted alphabetically. Disable → results randomized on next generate.
7. **Show definitions toggle** — uncheck → definitions hidden. Check → definitions visible.
8. **Copy all button** — click → clipboard contains list of words (one per line). Verify in a text editor.
9. **Count input** — change to 5 → 5 results. Change to 50 → up to 50 results. Enter 0 or 51 → error message shown, no generate.
10. **Space to regenerate** — press Space → new results generated
11. **Breadcrumb** — shows "Wordineer › Word Tools › Random Adverb Generator". Middle link goes to `/word-tools/`.
12. **word-tools hub** — open `http://localhost:8080/word-tools.html` → "Random Adverbs" card is now a clickable link, no "Coming soon" badge.
13. **Engine version** — view source of any page, confirm `tool-engine.js?v=24` (not v=23)
14. **No console errors** — browser dev tools shows no JS errors on page load or generate

- [ ] **Step 5: Final commit**

```bash
git add wordineer-deploy/random-adverb-generator.html wordineer-deploy/*.html
git commit -m "feat: build and deploy random-adverb-generator page (v24 engine)"
```

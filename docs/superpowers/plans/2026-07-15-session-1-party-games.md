# Session 1: Party Games Cluster Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build Scattergories Generator, Catchphrase Generator, and Couples Truth or Dare Generator — replacing three "Coming soon" cards on /word-tools/.

**Architecture:** Each tool is a self-contained HTML source file in `template-deploy/tools-src/` following the SLOT template system (CONFIG + SLOT:meta/style/hero/tool/init/explainer/faq/who). Data lives in `wordineer-deploy/data/` as tagged JSON. All JS is a vanilla IIFE in SLOT:init with inline seed data + lazy-load of full JSON. No external libraries.

**Tech Stack:** Vanilla JS (IIFE), CSS custom properties, DM Sans + DM Serif Display, Web Audio API (timer beeps), build.py static site generator.

---

## File Structure

### Create:
- `wordineer-deploy/data/scattergories.json`
- `wordineer-deploy/data/catchphrase.json`
- `wordineer-deploy/data/couples-truth-or-dare.json`
- `template-deploy/tools-src/scattergories-generator.html`
- `template-deploy/tools-src/catchphrase-generator.html`
- `template-deploy/tools-src/couples-truth-or-dare-generator.html`
- `scripts/validate-data.js`

### Modify:
- `template-deploy/tools.json` — register 3 tools in mega, more_word_tools, other_tools, footer_cols
- `template-deploy/tools-src/word-tools.html` — replace 3 coming-soon cards
- `wordineer-deploy/_redirects` — add redirect + rewrite lines for each new slug
- `template-deploy/tools-src/truth-or-dare-generator.html` — add link to couples variant in SLOT:who or SLOT:explainer

### Build output (generated, not edited directly):
- `template-deploy/output/scattergories-generator.html` → `wordineer-deploy/scattergories-generator.html`
- `template-deploy/output/catchphrase-generator.html` → `wordineer-deploy/catchphrase-generator.html`
- `template-deploy/output/couples-truth-or-dare-generator.html` → `wordineer-deploy/couples-truth-or-dare-generator.html`

---

## Task 1: Create validate-data.js

**Files:**
- Create: `scripts/validate-data.js`

- [ ] **Step 1: Write the validation script**

```javascript
#!/usr/bin/env node
// scripts/validate-data.js
// Run: node scripts/validate-data.js
// Validates that every declared filter/tag value in party-game data files
// has at least MIN_COUNT matching entries.

const fs = require('fs');
const path = require('path');

const DATA_DIR = path.join(__dirname, '../wordineer-deploy/data');
const MIN_COUNT = 5;
let errors = 0;

function check(label, items, getTag, tagValues) {
  for (const tag of tagValues) {
    const matches = items.filter(i => getTag(i) === tag);
    if (matches.length < MIN_COUNT) {
      console.error(`FAIL ${label}: tag "${tag}" has only ${matches.length} entries (min ${MIN_COUNT})`);
      errors++;
    } else {
      console.log(`  OK ${label}[${tag}]: ${matches.length} entries`);
    }
  }
}

function load(filename) {
  const fp = path.join(DATA_DIR, filename);
  if (!fs.existsSync(fp)) {
    console.error(`FAIL: ${fp} does not exist`);
    errors++;
    return null;
  }
  return JSON.parse(fs.readFileSync(fp, 'utf8'));
}

// --- scattergories.json ---
console.log('\n=== scattergories.json ===');
const sc = load('scattergories.json');
if (sc) {
  if (!Array.isArray(sc.lists) || sc.lists.length < 12) {
    console.error(`FAIL scattergories: need 12 lists, found ${sc.lists?.length ?? 0}`);
    errors++;
  } else {
    console.log(`  OK lists: ${sc.lists.length} (each has ${sc.lists.map(l=>l.length).join(',')} categories)`);
  }
  const themes = ['classic','kids','adults','holiday','food','pop-culture','hard'];
  for (const t of themes) {
    const cats = (sc.pool || {})[t] || [];
    if (cats.length < 10) {
      console.error(`FAIL scattergories pool[${t}]: only ${cats.length} categories (need 10+)`);
      errors++;
    } else {
      console.log(`  OK pool[${t}]: ${cats.length} categories`);
    }
  }
}

// --- catchphrase.json ---
console.log('\n=== catchphrase.json ===');
const cp = load('catchphrase.json');
if (cp) {
  const categories = ['everyday','actions','places','people','food','entertainment','idioms','hard'];
  const difficulties = ['easy','medium','hard'];
  check('catchphrase category', cp, i => i.category, categories);
  check('catchphrase difficulty', cp, i => i.difficulty, difficulties);
  console.log(`  Total entries: ${cp.length}`);
  if (cp.length < 400) {
    console.error(`FAIL catchphrase: only ${cp.length} entries (need 400+)`);
    errors++;
  }
}

// --- couples-truth-or-dare.json ---
console.log('\n=== couples-truth-or-dare.json ===');
const ctd = load('couples-truth-or-dare.json');
if (ctd) {
  const intensities = ['sweet','fun','romantic','spicy'];
  for (const intensity of intensities) {
    const group = (ctd[intensity] || {});
    const truths = (group.truth || []);
    const dares = (group.dare || []);
    if (truths.length < MIN_COUNT) {
      console.error(`FAIL couples[${intensity}].truth: only ${truths.length} (need ${MIN_COUNT}+)`);
      errors++;
    } else {
      console.log(`  OK couples[${intensity}].truth: ${truths.length}`);
    }
    if (dares.length < MIN_COUNT) {
      console.error(`FAIL couples[${intensity}].dare: only ${dares.length} (need ${MIN_COUNT}+)`);
      errors++;
    } else {
      console.log(`  OK couples[${intensity}].dare: ${dares.length}`);
    }
  }
}

console.log(`\n${errors === 0 ? '✓ All checks passed' : `✗ ${errors} error(s) found`}`);
process.exit(errors > 0 ? 1 : 0);
```

- [ ] **Step 2: Run to confirm it fails (data files don't exist yet)**

```bash
node scripts/validate-data.js
```

Expected: `FAIL: .../scattergories.json does not exist` (and similar for the other two). Exit code 1.

- [ ] **Step 3: Commit**

```bash
git add scripts/validate-data.js
git commit -m "feat: add validate-data.js for party game data files"
```

---

## Task 2: Create scattergories.json

**Files:**
- Create: `wordineer-deploy/data/scattergories.json`

- [ ] **Step 1: Write the data file**

Schema:
```json
{
  "lists": [ [...12 categories...], ...12 lists total ],
  "pool": {
    "classic": [...],
    "kids": [...],
    "adults": [...],
    "holiday": [...],
    "food": [...],
    "pop-culture": [...],
    "hard": [...]
  }
}
```

Write `wordineer-deploy/data/scattergories.json` with:
- **12 lists** of exactly 12 categories each (pre-built game rounds)
- **pool** object: each theme key has ≥15 unique categories (total pool ≥105)
- All categories are original phrasing, not copied from Hasbro

Example entries for each pool theme (write many more of these):
```json
{
  "lists": [
    ["Animals","Foods","Sports","Countries","Things in a kitchen","Movies","Ways to travel","Occupations","Things at a party","Colors","Things at a beach","Famous people"],
    ["School subjects","Musical instruments","Things you wear","Vegetables","Games you play indoors","Cities","Things in an office","Types of vehicles","Things that are soft","Types of weather","Brands","Hobbies"],
    ["Things that are round","Names for a pet","Things that can fly","Drinks","Furniture","Songs","Sports equipment","Things at a carnival","Types of stores","Things you do on a rainy day","Flowers","Types of shoes"],
    ["Things in a grocery store","Superhero names","Things at a zoo","Dance styles","Things that are green","Cooking utensils","Board games","Things you carry in a bag","Historical figures","Types of music","Things in a bathroom","Body of water"],
    ["Breakfast foods","Cartoon characters","Things that are expensive","Street names","Outdoor activities","Types of hats","Jobs that need a uniform","Things in a hotel room","Sports teams","Things you find underground","Languages","Words that mean happy"],
    ["Things that are cold","Movie genres","Things you see at a wedding","Kitchen appliances","Famous landmarks","Things that smell good","Types of boats","Words that rhyme with cat","Things in a classroom","TV shows","Things you recycle","Items in a first-aid kit"],
    ["Things in a park","Candy bars","Things you might find in a garage","Names of rivers","School supplies","Things that are fragile","Things you do at night","Types of clouds","Words that start with the same letter as you choose","Things in a wallet","Modes of communication","Things that make noise"],
    ["Fruits","Types of cheese","Things you see at the circus","Jobs you need a degree for","Things on a farm","Words that describe speed","Things in the sky","Styles of cooking","Famous duos","Things you do on vacation","Things that are long","Words that mean big"],
    ["Things in a library","Fast food items","Types of trees","Things that are shiny","Sports played on water","Words with double letters","Things at an airport","Household chores","Historical events","Things you can do with rope","Parts of a car","Fictional places"],
    ["Things associated with winter","Jewelry items","Words that mean sad","Things you'd find at a picnic","Types of sandwiches","Things associated with summer","Board game pieces","Things that can be customized","College majors","Things in a shoe store","Exercises","Things in a science lab"],
    ["Card games","Things that are purple","Types of doctors","Things you see in a city","Words that mean beautiful","Snack foods","Things in a toy store","Things that bounce","Items you'd pack for camping","Styles of architecture","Things with buttons","Mythological creatures"],
    ["Things that are yellow","Types of pasta","Words that mean tired","Things that grow in a garden","Wild animals","Things you'd find in a hospital","Famous artists","Desserts","Types of sports leagues","Things you use in cooking","Words that describe texture","Landmarks in Europe"]
  ],
  "pool": {
    "classic": ["Animals","Foods","Sports","Countries","Movies","Things in a kitchen","Ways to travel","Occupations","Things at a party","Colors","Things at a beach","Famous people","School subjects","Musical instruments","Things you wear","Vegetables","Games you play indoors","Cities","Hobbies","Flowers","Furniture","Languages","Things that are round","Body of water","Things that are cold"],
    "kids": ["Animals","Colors","Fruits","Vegetables","Things at school","Cartoon characters","Toys","Things you do outside","Things in a bedroom","Animals that can fly","Things that are soft","Things you eat for breakfast","Things that are round","Things that bounce","Animals at a zoo","Games you play outside","Things in a library","Famous cartoon characters","Things you draw","Things that are blue"],
    "adults": ["Things at a bar","Things that cost over a hundred dollars","Ways to procrastinate","Excuses for being late","Things you say on a first date","Things you find in a home office","Streaming shows","Things associated with wine","Things you do at a gym","Words your boss uses too much","Things that are overrated","Things you do when bored","Brands everyone knows","Things that stress people out","Habits people try to quit","Things in a medicine cabinet","Things in a city apartment","Words for being tired"],
    "holiday": ["Christmas songs","Holiday movies","Things on a Christmas tree","Holiday foods","New Year's traditions","Halloween costumes","Thanksgiving dishes","Things associated with winter","Holiday decorations","Things you give as gifts","Things associated with the Fourth of July","Valentine's Day traditions","Easter traditions","Things at a holiday party","Holiday candies","Winter activities","Holiday travel destinations"],
    "food": ["Pasta dishes","Fruits","Vegetables","Types of cheese","Things on a pizza","Hot drinks","Desserts","Breakfast foods","Street foods from around the world","Things you put on a sandwich","Spices","Types of bread","Foods from Italy","Frozen foods","Things you grill","Asian dishes","Foods that are orange","Things you dip","Types of soup","Baking ingredients"],
    "pop-culture": ["Marvel superheroes","Disney movies","Video game titles","Reality TV shows","Songs from the last decade","Celebrity first names","Movie sequel titles","Famous YouTube channels","Things from the nineties","Animated movies","Famous brands","Things associated with TikTok","Sports team names","Famous athletes","Award-winning movies","Things from the eighties","Video game characters"],
    "hard": ["Phobias","Chemical elements","Opera composers","Ancient civilizations","Economic terms","Literary genres","Architectural styles","Philosophical concepts","Latin phrases used in English","Types of fallacies","Scientific theories","Shakespearean plays","Types of government","Historical treaties","Branches of mathematics","Extinct animals","Types of clouds","Geological eras"]
  }
}
```

- [ ] **Step 2: Run validate-data.js — confirm scattergories passes**

```bash
node scripts/validate-data.js
```

Expected: `OK` lines for scattergories, still `FAIL` for catchphrase and couples (not yet written).

- [ ] **Step 3: Commit**

```bash
git add wordineer-deploy/data/scattergories.json
git commit -m "feat: add scattergories.json data (12 lists, 7-theme pool)"
```

---

## Task 3: Build scattergories-generator.html

**Files:**
- Create: `template-deploy/tools-src/scattergories-generator.html`

- [ ] **Step 1: Check charades-generator.html CONFIG for more_tools_key**

```bash
head -10 template-deploy/tools-src/charades-generator.html
```

Note the `more_tools_key` value. Use the same key in the scattergories CONFIG.

- [ ] **Step 2: Write the tool source file**

Create `template-deploy/tools-src/scattergories-generator.html`:

```html
<!-- CONFIG
{
  "type": "tool",
  "url": "/scattergories-generator/",
  "output": "scattergories-generator.html",
  "more_tools_key": "more_word_tools",
  "more_tools_title": "More word game generators",
  "more_tools_subtitle": "Free tools for game night"
}
-->

<!-- SLOT:meta -->
<title>Scattergories Generator — Roll a Letter, Get 12 Categories</title>
<meta name="description" content="Free Scattergories generator. Roll a random letter, get 12 categories, and set a timer. Perfect for game night, remote play, and parties.">
<link rel="canonical" href="https://wordineer.com/scattergories-generator/">
<meta property="og:title" content="Scattergories Generator — Roll a Letter, Get 12 Categories">
<meta property="og:description" content="Free Scattergories generator. Roll a random letter, get 12 categories, and set a timer.">
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "What letters are excluded and why?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "The official Scattergories die excludes Q, U, V, X, Y, and Z because very few common words or category answers begin with those letters, making gameplay frustratingly difficult. Our generator excludes the same six letters by default, though you can toggle 'use all 26 letters' for a harder challenge."
      }
    },
    {
      "@type": "Question",
      "name": "How many categories are in a round?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "A standard Scattergories round uses 12 categories. Our generator shows 12 categories per round, matching the original game card format."
      }
    },
    {
      "@type": "Question",
      "name": "How do I use this for remote play?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Share your screen or open the generator on a TV. Everyone sees the same letter and categories. Use the built-in timer, and when it goes off, each player reads their answers aloud. Duplicate answers cancel out — only unique answers score a point."
      }
    },
    {
      "@type": "Question",
      "name": "Can I print the category list?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Yes — click the Print button for a clean card layout with the letter and 12 numbered blank lines, ready to write answers on."
      }
    },
    {
      "@type": "Question",
      "name": "What is the timer for?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "The official game gives players 3 minutes per round. Our timer defaults to 3 minutes with a beep at 0. You can also choose 1, 2, or 5 minutes for faster or more relaxed games."
      }
    }
  ]
}
</script>
<!-- /SLOT:meta -->

<!-- SLOT:style -->
<style>
.scat-wrap { max-width: 960px; margin: 0 auto; padding: 24px 16px; }
.scat-card { background: var(--bg); border: 1px solid var(--border); border-radius: var(--radius-lg); overflow: hidden; box-shadow: var(--shadow); }
.scat-layout { display: grid; grid-template-columns: 280px 1fr; min-height: 520px; }

/* Controls sidebar */
.scat-controls { background: var(--bg-2); border-right: 1px solid var(--border); padding: 20px 16px; display: flex; flex-direction: column; gap: 20px; }
.scat-section-label { font-size: 11px; font-weight: 600; color: var(--text-3); text-transform: uppercase; letter-spacing: .06em; margin-bottom: 6px; }

/* Letter display */
.scat-letter-block { text-align: center; padding: 12px 0; }
.scat-letter { font-family: 'DM Serif Display', serif; font-size: 72px; line-height: 1; color: var(--brand); display: block; }
@keyframes scat-roll { 0%{transform:rotateY(0)} 50%{transform:rotateY(90deg);opacity:.4} 100%{transform:rotateY(0)} }
.scat-roll-anim { animation: scat-roll .35s ease; }
.scat-all-letters-label { font-size: 12px; color: var(--text-2); display: flex; align-items: center; gap: 6px; cursor: pointer; justify-content: center; margin-top: 8px; }

/* Timer */
.scat-timer-display { font-family: 'DM Serif Display', serif; font-size: 36px; text-align: center; color: var(--text); padding: 8px 0; letter-spacing: .02em; }
.scat-timer--warning { color: var(--amber); }
.scat-timer--critical { color: #c0392b; }
.scat-duration-row { display: flex; gap: 4px; }
.scat-duration-row button { flex: 1; padding: 5px 0; font-size: 12px; border: 1px solid var(--border); border-radius: 6px; background: var(--bg); color: var(--text-2); cursor: pointer; }
.scat-duration-row button:hover, .scat-duration-row button.active { border-color: var(--brand); color: var(--brand); }
.scat-timer-row { display: flex; gap: 6px; margin-top: 6px; }

/* Main panel */
.scat-main { display: flex; flex-direction: column; }
.scat-main-top { display: flex; align-items: center; justify-content: space-between; padding: 16px 20px 12px; border-bottom: 1px solid var(--border-2); }
.scat-main-top strong { font-weight: 600; color: var(--text); }
.scat-list { list-style: none; padding: 12px 20px; margin: 0; display: grid; grid-template-columns: 1fr 1fr; gap: 8px 16px; flex: 1; }
.scat-cat-item { display: flex; gap: 8px; align-items: flex-start; font-size: 15px; color: var(--text); }
.scat-cat-num { color: var(--brand); font-weight: 600; min-width: 20px; }

/* Action buttons */
.scat-actions { padding: 12px 20px; border-top: 1px solid var(--border-2); display: flex; flex-wrap: wrap; gap: 8px; }

/* Play mode overlay */
.scat--play-mode .scat-layout { grid-template-columns: 1fr; }
.scat--play-mode .scat-controls { display: none; }
.scat--play-mode .scat-main { align-items: center; justify-content: center; padding: 40px; }
.scat--play-mode .scat-letter { font-size: 120px; }
.scat--play-mode .scat-list { grid-template-columns: repeat(3, 1fr); font-size: 18px; }

/* Responsive */
@media (max-width: 700px) {
  .scat-layout { grid-template-columns: 1fr; }
  .scat-controls { border-right: none; border-bottom: 1px solid var(--border); }
  .scat-list { grid-template-columns: 1fr; }
}

@media print {
  .nav, .mega, .hero, .scat-actions, .scat-controls, .scat-main-top button,
  .ad-leaderboard, .content-wrap, .footer { display: none !important; }
  .scat-wrap { padding: 0; }
  .scat-layout { grid-template-columns: 1fr; }
  .scat-list { display: block; }
  .scat-cat-item { border-bottom: 1px solid #ccc; padding: 10px 0; font-size: 18px; }
}
</style>
<!-- /SLOT:style -->

<!-- SLOT:hero -->
<nav class="breadcrumb" aria-label="Breadcrumb">
  <ol itemscope itemtype="https://schema.org/BreadcrumbList">
    <li itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
      <a itemprop="item" href="/"><span itemprop="name">Home</span></a>
      <meta itemprop="position" content="1">
    </li>
    <li itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
      <a itemprop="item" href="/word-tools/"><span itemprop="name">Word tools</span></a>
      <meta itemprop="position" content="2">
    </li>
    <li itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
      <span itemprop="name">Scattergories Generator</span>
      <meta itemprop="position" content="3">
    </li>
  </ol>
</nav>
<h1>Scattergories Generator</h1>
<p>Roll a random letter, get 12 categories, and start the timer. Free to play — no account, no app, no setup.</p>
<!-- /SLOT:hero -->

<!-- SLOT:tool -->
<div class="scat-wrap" id="scat-tool-wrap" aria-label="Scattergories generator tool">
  <div class="scat-card">
    <div class="scat-layout">

      <!-- Sidebar -->
      <aside class="scat-controls">

        <!-- Letter roller -->
        <div>
          <div class="scat-section-label">Letter</div>
          <div class="scat-letter-block">
            <span class="scat-letter" id="scat-letter">S</span>
            <label class="scat-all-letters-label">
              <input type="checkbox" id="scat-all-letters"> Use all 26 letters
            </label>
          </div>
          <button class="primary-btn" id="scat-roll-btn">Roll Letter</button>
        </div>

        <!-- Category theme -->
        <div>
          <div class="scat-section-label">Category theme</div>
          <select class="pic-select" id="scat-theme-filter">
            <option value="all">All themes</option>
            <option value="classic">Classic</option>
            <option value="kids">Kids</option>
            <option value="adults">Adults</option>
            <option value="holiday">Holiday</option>
            <option value="food">Food</option>
            <option value="pop-culture">Pop culture</option>
            <option value="hard">Hard</option>
          </select>
        </div>

        <!-- Timer -->
        <div>
          <div class="scat-section-label">Round timer</div>
          <div class="scat-timer-display" id="scat-timer-display">3:00</div>
          <div class="scat-duration-row">
            <button data-duration="1">1 min</button>
            <button data-duration="2">2 min</button>
            <button data-duration="3" class="active">3 min</button>
            <button data-duration="5">5 min</button>
          </div>
          <div class="scat-timer-row">
            <button class="primary-btn" style="flex:2" id="scat-timer-start">Start</button>
            <button class="small-btn" style="flex:1" id="scat-timer-reset">Reset</button>
          </div>
        </div>

        <!-- Actions -->
        <div style="margin-top:auto; display:flex; flex-direction:column; gap:8px;">
          <button class="small-btn" id="scat-play-mode-btn">Play mode</button>
          <button class="small-btn" id="scat-print-btn">Print card</button>
        </div>

      </aside>

      <!-- Main panel -->
      <section class="scat-main">
        <div class="scat-main-top">
          <strong>Categories for this round</strong>
          <button class="small-btn" id="scat-new-list-btn">New list</button>
        </div>
        <ul class="scat-list" id="scat-list">
          <!-- Rendered by JS -->
        </ul>
        <div class="scat-actions">
          <button class="small-btn" id="scat-copy-btn">Copy list</button>
        </div>
      </section>

    </div>
  </div>
</div>
<!-- /SLOT:tool -->

<!-- SLOT:ad_b -->
<!-- ad placeholder -->
<!-- /SLOT:ad_b -->

<!-- SLOT:explainer -->
<h2>How to use the Scattergories generator</h2>
<p>Scattergories is a word game where every answer must start with a specific letter and fit a given category — and you only score if nobody else picked the same answer.</p>
<ol>
  <li><strong>Roll a letter</strong> — click the Roll button to get a random letter from the official 20-letter pool (Q, U, V, X, Y, and Z are excluded because very few common answers start with them).</li>
  <li><strong>Get your categories</strong> — 12 categories appear on the right. Click "New list" to swap to a different set at any time.</li>
  <li><strong>Start the timer</strong> — 3 minutes is the standard round length. Everyone writes down one answer per category that starts with the rolled letter.</li>
  <li><strong>Score</strong> — when time's up, players read their answers aloud. Any answer that matches another player's answer scores zero. Unique answers score one point. Alliterative answers (both words start with the letter) score two.</li>
</ol>

<h2>Playing online or remotely</h2>
<p>Share your screen on Zoom, Discord, or a TV, and everyone plays from one shared view. Agree on a scoring method before you start — some groups allow one point per unique answer, others allow two for creative answers that fit. The generator handles the letter roll, category shuffle, and timer so you can focus on playing.</p>
<!-- /SLOT:explainer -->

<!-- SLOT:faq -->
<h2>Frequently asked questions</h2>
<details>
  <summary>What letters are excluded and why?</summary>
  <p>The six letters Q, U, V, X, Y, and Z are excluded by default because very few everyday words start with them, making it nearly impossible to fill every category. The official game die uses the same 20-letter pool. Toggle "Use all 26 letters" if you want the harder version.</p>
</details>
<details>
  <summary>How many categories are in a Scattergories round?</summary>
  <p>A standard round uses 12 categories, matching the original game card. Our generator always shows 12 per round. Click "New list" to get a fresh set of 12 from the same theme.</p>
</details>
<details>
  <summary>Can I use this for remote play?</summary>
  <p>Yes — share your screen so everyone sees the same letter and categories. Roll the letter, start the timer, and everyone writes on paper or in a notes app. When time's up, read answers aloud on your call.</p>
</details>
<details>
  <summary>How do I print a Scattergories card?</summary>
  <p>Click "Print card" for a clean layout showing the letter and 12 numbered blank lines. Great for classroom use or offline parties where you don't want devices at the table.</p>
</details>
<details>
  <summary>What does the category theme filter do?</summary>
  <p>It draws categories from a specific set — Classic (general-knowledge categories suitable for all ages), Kids (simpler categories), Adults (pop culture and lifestyle), Holiday, Food, and Hard (trivia-level difficulty). "All themes" mixes them together for maximum variety.</p>
</details>
<details>
  <summary>What is Play Mode?</summary>
  <p>Play Mode expands the tool to fill the screen — bigger letter, bigger categories — so it's easier to see on a TV or across a table. Everything still works the same; it's just optimized for group viewing.</p>
</details>
<!-- /SLOT:faq -->

<!-- SLOT:who -->
<h2>Who uses the Scattergories generator</h2>
<ul>
  <li><strong>Game night hosts</strong> who want a no-setup alternative to finding the physical game</li>
  <li><strong>Teachers</strong> using Scattergories as a vocabulary and quick-thinking exercise</li>
  <li><strong>Remote teams</strong> running virtual happy hours and ice-breaker games</li>
  <li><strong>Families</strong> looking for a screen-time activity everyone from kids to grandparents can play</li>
</ul>
<p>Also check out our <a href="/charades-generator/">Charades generator</a>, <a href="/pictionary-word-generator/">Pictionary word generator</a>, <a href="/truth-or-dare-generator/">Truth or Dare generator</a>, <a href="/never-have-i-ever-generator/">Never Have I Ever generator</a>, and <a href="/would-you-rather-generator/">Would You Rather generator</a>.</p>
<!-- /SLOT:who -->

<!-- SLOT:init -->
<script>
(function(){
  'use strict';
  const OFFICIAL_LETTERS = 'ABCDEFGHIJKLMNOPRSTW';
  const ALL_LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';

  const SEED = {
    lists: [
      ["Animals","Foods","Sports","Countries","Things in a kitchen","Movies","Ways to travel","Occupations","Things at a party","Colors","Things at a beach","Famous people"],
      ["School subjects","Musical instruments","Things you wear","Vegetables","Games you play indoors","Cities","Things in an office","Types of vehicles","Things that are soft","Types of weather","Brands","Hobbies"],
      ["Things that are round","Names for a pet","Things that can fly","Drinks","Furniture","Songs","Sports equipment","Things at a carnival","Types of stores","Things on a rainy day","Flowers","Types of shoes"],
      ["Things in a grocery store","Superhero names","Things at a zoo","Dance styles","Things that are green","Cooking utensils","Board games","Things you carry in a bag","Historical figures","Types of music","Things in a bathroom","Bodies of water"]
    ],
    pool: {
      classic: ["Animals","Foods","Sports","Countries","Movies","Things in a kitchen","Ways to travel","Occupations","Things at a party","Colors","Things at a beach","Famous people","School subjects","Musical instruments","Things you wear","Vegetables","Games","Cities","Hobbies","Flowers"],
      kids: ["Animals","Colors","Fruits","Vegetables","Things at school","Cartoon characters","Toys","Things you do outside","Things in a bedroom","Animals that can fly","Things that are soft","Things you eat for breakfast","Things that bounce"],
      adults: ["Things at a bar","Things that cost over a hundred dollars","Ways to procrastinate","Excuses for being late","Streaming shows","Things associated with wine","Words your boss uses too much","Things that are overrated","Brands everyone knows"],
      holiday: ["Christmas songs","Holiday movies","Things on a Christmas tree","Holiday foods","Halloween costumes","Thanksgiving dishes","New Year's traditions","Holiday decorations","Things you give as gifts"],
      food: ["Pasta dishes","Fruits","Vegetables","Types of cheese","Things on a pizza","Hot drinks","Desserts","Breakfast foods","Street foods","Things you put on a sandwich","Spices","Types of bread"],
      'pop-culture': ["Marvel superheroes","Disney movies","Video game titles","Reality TV shows","Famous YouTube channels","Things from the nineties","Animated movies","Famous athletes","Award-winning movies"],
      hard: ["Phobias","Chemical elements","Opera composers","Ancient civilizations","Economic terms","Literary genres","Architectural styles","Philosophical concepts","Latin phrases","Extinct animals"]
    }
  };

  let fullData = null;

  const state = {
    letter: 'S',
    useAllLetters: false,
    theme: 'all',
    currentList: SEED.lists[0].slice(),
    timerSecs: 180,
    timerDuration: 180,
    activeDuration: 3,
    running: false,
    interval: null,
    playMode: false
  };

  let audioCtx = null;
  function getCtx() {
    if (!audioCtx) {
      try { audioCtx = new (window.AudioContext || window.webkitAudioContext)(); } catch(e){}
    }
    return audioCtx;
  }

  function beep(freq, dur) {
    const ctx = getCtx();
    if (!ctx) return;
    try {
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      osc.connect(gain);
      gain.connect(ctx.destination);
      osc.frequency.value = freq || 880;
      gain.gain.setValueAtTime(0.25, ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + (dur || 0.2));
      osc.start();
      osc.stop(ctx.currentTime + (dur || 0.2));
    } catch(e){}
  }

  function rollLetter() {
    const pool = state.useAllLetters ? ALL_LETTERS : OFFICIAL_LETTERS;
    let next;
    do { next = pool[Math.floor(Math.random() * pool.length)]; } while (next === state.letter && pool.length > 1);
    state.letter = next;
    const el = document.getElementById('scat-letter');
    if (el) {
      el.textContent = state.letter;
      el.classList.remove('scat-roll-anim');
      void el.offsetWidth;
      el.classList.add('scat-roll-anim');
    }
  }

  function getPool() {
    const src = fullData || SEED;
    if (state.theme === 'all') return Object.values(src.pool).flat();
    return (src.pool[state.theme] || []);
  }

  function newList() {
    const pool = getPool();
    const shuffled = [...pool].sort(() => Math.random() - 0.5);
    state.currentList = shuffled.slice(0, 12);
    renderList();
  }

  function renderList() {
    const ul = document.getElementById('scat-list');
    if (!ul) return;
    ul.innerHTML = state.currentList
      .map((cat, i) => `<li class="scat-cat-item"><span class="scat-cat-num">${i + 1}.</span><span>${cat}</span></li>`)
      .join('');
  }

  function renderTimer() {
    const m = Math.floor(state.timerSecs / 60);
    const s = state.timerSecs % 60;
    const el = document.getElementById('scat-timer-display');
    if (!el) return;
    el.textContent = `${m}:${String(s).padStart(2, '0')}`;
    el.classList.toggle('scat-timer--warning', state.timerSecs <= 30 && state.timerSecs > 10);
    el.classList.toggle('scat-timer--critical', state.timerSecs <= 10);
  }

  function startTimer() {
    if (state.running) {
      clearInterval(state.interval);
      state.running = false;
      document.getElementById('scat-timer-start').textContent = 'Start';
      return;
    }
    if (state.timerSecs <= 0) state.timerSecs = state.timerDuration;
    state.running = true;
    document.getElementById('scat-timer-start').textContent = 'Pause';
    state.interval = setInterval(function() {
      state.timerSecs--;
      renderTimer();
      if (state.timerSecs > 0 && state.timerSecs <= 10) beep(880, 0.1);
      if (state.timerSecs <= 0) {
        clearInterval(state.interval);
        state.running = false;
        document.getElementById('scat-timer-start').textContent = 'Start';
        beep(440, 0.5);
        setTimeout(function(){ beep(540, 0.4); }, 200);
        setTimeout(function(){ beep(660, 0.6); }, 400);
      }
    }, 1000);
  }

  function resetTimer() {
    clearInterval(state.interval);
    state.running = false;
    state.timerSecs = state.timerDuration;
    renderTimer();
    document.getElementById('scat-timer-start').textContent = 'Start';
  }

  function setDuration(mins) {
    state.activeDuration = mins;
    state.timerDuration = mins * 60;
    if (!state.running) {
      state.timerSecs = state.timerDuration;
      renderTimer();
    }
    document.querySelectorAll('[data-duration]').forEach(function(b){
      b.classList.toggle('active', +b.dataset.duration === mins);
    });
  }

  function loadFull() {
    if (fullData) return;
    fetch('/data/scattergories.json')
      .then(function(r){ return r.ok ? r.json() : null; })
      .then(function(d){ if (d) fullData = d; })
      .catch(function(){});
  }

  // Event wiring
  document.getElementById('scat-roll-btn').addEventListener('click', rollLetter);
  document.getElementById('scat-new-list-btn').addEventListener('click', newList);
  document.getElementById('scat-theme-filter').addEventListener('change', function(e){
    state.theme = e.target.value;
    newList();
  });
  document.getElementById('scat-timer-start').addEventListener('click', startTimer);
  document.getElementById('scat-timer-reset').addEventListener('click', resetTimer);
  document.querySelectorAll('[data-duration]').forEach(function(btn){
    btn.addEventListener('click', function(){ setDuration(+btn.dataset.duration); });
  });
  document.getElementById('scat-print-btn').addEventListener('click', function(){ window.print(); });
  document.getElementById('scat-play-mode-btn').addEventListener('click', function(){
    state.playMode = !state.playMode;
    document.getElementById('scat-tool-wrap').classList.toggle('scat--play-mode', state.playMode);
    document.getElementById('scat-play-mode-btn').textContent = state.playMode ? 'Exit play mode' : 'Play mode';
  });
  document.getElementById('scat-all-letters').addEventListener('change', function(e){
    state.useAllLetters = e.target.checked;
  });
  document.getElementById('scat-copy-btn').addEventListener('click', function(){
    const text = `Letter: ${state.letter}\n\n` + state.currentList.map((c,i)=>`${i+1}. ${c}`).join('\n');
    navigator.clipboard.writeText(text).catch(function(){});
    const btn = document.getElementById('scat-copy-btn');
    const orig = btn.textContent;
    btn.textContent = 'Copied!';
    setTimeout(function(){ btn.textContent = orig; }, 1500);
  });

  // Init
  renderList();
  renderTimer();
  loadFull();
})();
</script>
<!-- /SLOT:init -->
```

- [ ] **Step 3: Build and spot-check**

```bash
cd template-deploy && python3 build.py 2>&1 | tail -20
```

Expected: no errors, `scattergories-generator.html` appears in output.

```bash
grep 'canonical' template-deploy/output/scattergories-generator.html
```

Expected: `https://wordineer.com/scattergories-generator/` (NOT the homepage URL).

- [ ] **Step 4: Commit**

```bash
git add template-deploy/tools-src/scattergories-generator.html
git commit -m "feat: add scattergories-generator.html tool source"
```

---

## Task 4: Create catchphrase.json

**Files:**
- Create: `wordineer-deploy/data/catchphrase.json`

- [ ] **Step 1: Write the data file**

Schema — array of objects:
```json
[
  { "text": "string", "category": "everyday|actions|places|people|food|entertainment|idioms|hard", "difficulty": "easy|medium|hard" }
]
```

Target counts:
- 8 categories × ~50 entries per category = ~400 total
- Each category needs entries at all 3 difficulty levels (≥5 each)
- All entries must be original phrasing; do not copy from Hasbro's Catchphrase game

Example entries:
```json
[
  { "text": "Alarm clock", "category": "everyday", "difficulty": "easy" },
  { "text": "Traffic jam", "category": "everyday", "difficulty": "easy" },
  { "text": "Comfort zone", "category": "everyday", "difficulty": "medium" },
  { "text": "Double standard", "category": "everyday", "difficulty": "hard" },
  { "text": "Juggling", "category": "actions", "difficulty": "easy" },
  { "text": "Parallel parking", "category": "actions", "difficulty": "medium" },
  { "text": "Procrastinating", "category": "actions", "difficulty": "medium" },
  { "text": "Improvising", "category": "actions", "difficulty": "hard" },
  { "text": "Bus stop", "category": "places", "difficulty": "easy" },
  { "text": "Amusement park", "category": "places", "difficulty": "easy" },
  { "text": "Farmers market", "category": "places", "difficulty": "medium" },
  { "text": "DMV", "category": "places", "difficulty": "hard" },
  { "text": "Celebrity", "category": "people", "difficulty": "easy" },
  { "text": "Mechanic", "category": "people", "difficulty": "medium" },
  { "text": "Ventriloquist", "category": "people", "difficulty": "hard" },
  { "text": "Lunchbox", "category": "food", "difficulty": "easy" },
  { "text": "Guacamole", "category": "food", "difficulty": "medium" },
  { "text": "Tiramisu", "category": "food", "difficulty": "hard" },
  { "text": "Plot twist", "category": "entertainment", "difficulty": "medium" },
  { "text": "Cliffhanger", "category": "entertainment", "difficulty": "medium" },
  { "text": "Break a leg", "category": "idioms", "difficulty": "easy" },
  { "text": "Spill the beans", "category": "idioms", "difficulty": "easy" },
  { "text": "Bite the bullet", "category": "idioms", "difficulty": "medium" },
  { "text": "Burning the midnight oil", "category": "idioms", "difficulty": "hard" },
  { "text": "Quantum leap", "category": "hard", "difficulty": "hard" },
  { "text": "Archipelago", "category": "hard", "difficulty": "hard" }
]
```

Write 400+ entries following this schema and content guidelines.

- [ ] **Step 2: Validate**

```bash
node scripts/validate-data.js
```

Expected: catchphrase section now shows all OK.

- [ ] **Step 3: Commit**

```bash
git add wordineer-deploy/data/catchphrase.json
git commit -m "feat: add catchphrase.json data (400+ entries, 8 categories)"
```

---

## Task 5: Build catchphrase-generator.html

**Files:**
- Create: `template-deploy/tools-src/catchphrase-generator.html`

- [ ] **Step 1: Write the tool source file**

Note: The Catchphrase UI is phone-centric (passed device), so the layout differs from the sidebar+main pattern. It uses a large centered display.

```html
<!-- CONFIG
{
  "type": "tool",
  "url": "/catchphrase-generator/",
  "output": "catchphrase-generator.html",
  "more_tools_key": "more_word_tools",
  "more_tools_title": "More word game generators",
  "more_tools_subtitle": "Free tools for game night"
}
-->

<!-- SLOT:meta -->
<title>Catchphrase Generator — Random Words for the Catchphrase Game</title>
<meta name="description" content="Free Catchphrase word generator. Get random words and phrases, filter by category and difficulty, and use the built-in timer. No account needed.">
<link rel="canonical" href="https://wordineer.com/catchphrase-generator/">
<meta property="og:title" content="Catchphrase Generator — Random Words for the Catchphrase Game">
<meta property="og:description" content="Free Catchphrase word generator with categories, difficulty filter, timer, and score tracker.">
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "How do you play Catchphrase?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Players sit in a circle alternating teams. The active player sees the word and gives verbal clues until their team guesses it, then passes to the next player. When the timer runs out, the team holding the device loses the round. Keep score and play to 7 points."
      }
    },
    {
      "@type": "Question",
      "name": "Can I filter words by category or difficulty?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Yes. Use the category filter (everyday, actions, places, people, food, entertainment, idioms, hard) and difficulty filter (easy, medium, hard) to customize the word pool for your group."
      }
    },
    {
      "@type": "Question",
      "name": "Will words repeat?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Words won't repeat until the entire filtered pool is exhausted. Once every word has been shown, the pool resets automatically."
      }
    }
  ]
}
</script>
<!-- /SLOT:meta -->

<!-- SLOT:style -->
<style>
.cp-wrap { max-width: 960px; margin: 0 auto; padding: 24px 16px; }
.cp-card { background: var(--bg); border: 1px solid var(--border); border-radius: var(--radius-lg); overflow: hidden; box-shadow: var(--shadow); }

/* Main display - phone-centric layout */
.cp-display-block { padding: 48px 32px 32px; text-align: center; border-bottom: 1px solid var(--border-2); }
.cp-word { font-family: 'DM Serif Display', serif; font-size: 52px; line-height: 1.1; color: var(--text); margin-bottom: 16px; min-height: 70px; }
.cp-next-btn { background: var(--brand); color: #fff; border: none; border-radius: var(--radius); font-size: 18px; font-weight: 600; padding: 16px 48px; cursor: pointer; width: 100%; max-width: 360px; margin: 0 auto; display: block; }
.cp-next-btn:active { opacity: .85; }
.cp-tap-hint { color: var(--text-3); font-size: 13px; margin-top: 12px; }

/* Controls row */
.cp-controls { padding: 16px 20px; display: flex; flex-wrap: wrap; gap: 12px; align-items: center; border-bottom: 1px solid var(--border-2); }
.cp-filter-group { display: flex; align-items: center; gap: 8px; }
.cp-filter-group label { font-size: 12px; color: var(--text-2); font-weight: 600; }
.cp-filter-group select { padding: 6px 10px; border: 1px solid var(--border); border-radius: 6px; font-size: 13px; background: var(--bg); color: var(--text); }

/* Timer */
.cp-timer-block { display: flex; align-items: center; gap: 8px; margin-left: auto; }
.cp-timer-display { font-family: 'DM Serif Display', serif; font-size: 28px; min-width: 60px; text-align: center; color: var(--text); }
.cp-timer--warning { color: var(--amber); }
.cp-timer--critical { color: #c0392b; }
.cp-timer-btns { display: flex; gap: 4px; }

/* Score tracker */
.cp-score-block { padding: 16px 20px; display: flex; gap: 24px; align-items: center; }
.cp-team { display: flex; align-items: center; gap: 12px; }
.cp-team-label { font-weight: 600; font-size: 14px; color: var(--text); }
.cp-score-val { font-family: 'DM Serif Display', serif; font-size: 32px; color: var(--brand); min-width: 40px; text-align: center; }
.cp-score-btns { display: flex; flex-direction: column; gap: 2px; }
.cp-score-btns button { border: 1px solid var(--border); border-radius: 4px; background: var(--bg); cursor: pointer; font-size: 14px; line-height: 1; padding: 4px 8px; }
.cp-score-btns button:hover { border-color: var(--brand); color: var(--brand); }
.cp-reset-score { margin-left: auto; }

/* Duration chips */
.cp-dur-chips { display: flex; gap: 4px; }
.cp-dur-chips button { padding: 4px 8px; border: 1px solid var(--border); border-radius: 6px; font-size: 12px; background: var(--bg); color: var(--text-2); cursor: pointer; }
.cp-dur-chips button.active { border-color: var(--brand); color: var(--brand); }

.cp-pool-count { font-size: 12px; color: var(--text-3); padding: 8px 20px 0; }

@media (max-width: 600px) {
  .cp-word { font-size: 38px; }
  .cp-controls { flex-direction: column; align-items: flex-start; }
  .cp-timer-block { margin-left: 0; }
}
</style>
<!-- /SLOT:style -->

<!-- SLOT:hero -->
<nav class="breadcrumb" aria-label="Breadcrumb">
  <ol itemscope itemtype="https://schema.org/BreadcrumbList">
    <li itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
      <a itemprop="item" href="/"><span itemprop="name">Home</span></a>
      <meta itemprop="position" content="1">
    </li>
    <li itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
      <a itemprop="item" href="/word-tools/"><span itemprop="name">Word tools</span></a>
      <meta itemprop="position" content="2">
    </li>
    <li itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
      <span itemprop="name">Catchphrase Generator</span>
      <meta itemprop="position" content="3">
    </li>
  </ol>
</nav>
<h1>Catchphrase Generator</h1>
<p>Get random words and phrases for the Catchphrase game. Filter by category, set the timer, and track scores — all in one screen.</p>
<!-- /SLOT:hero -->

<!-- SLOT:tool -->
<div class="cp-wrap" aria-label="Catchphrase generator">
  <div class="cp-card">

    <!-- Word display -->
    <div class="cp-display-block">
      <div class="cp-word" id="cp-word">Press Next to start</div>
      <button class="cp-next-btn" id="cp-next-btn">Next word</button>
      <p class="cp-tap-hint">Tap anywhere on the word to advance</p>
    </div>

    <!-- Controls -->
    <div class="cp-controls">
      <div class="cp-filter-group">
        <label for="cp-category">Category</label>
        <select id="cp-category">
          <option value="all">All</option>
          <option value="everyday">Everyday</option>
          <option value="actions">Actions</option>
          <option value="places">Places</option>
          <option value="people">People</option>
          <option value="food">Food</option>
          <option value="entertainment">Entertainment</option>
          <option value="idioms">Idioms</option>
          <option value="hard">Hard</option>
        </select>
      </div>
      <div class="cp-filter-group">
        <label for="cp-difficulty">Difficulty</label>
        <select id="cp-difficulty">
          <option value="all">All</option>
          <option value="easy">Easy</option>
          <option value="medium">Medium</option>
          <option value="hard">Hard</option>
        </select>
      </div>
      <div class="cp-timer-block">
        <div class="cp-dur-chips">
          <button data-cp-dur="30">30s</button>
          <button data-cp-dur="60" class="active">60s</button>
          <button data-cp-dur="90">90s</button>
        </div>
        <div class="cp-timer-display" id="cp-timer-display">1:00</div>
        <div class="cp-timer-btns">
          <button class="small-btn" id="cp-timer-start">Start</button>
          <button class="small-btn" id="cp-timer-reset">Reset</button>
        </div>
      </div>
    </div>

    <div class="cp-pool-count" id="cp-pool-count"></div>

    <!-- Score tracker -->
    <div class="cp-score-block">
      <div class="cp-team">
        <span class="cp-team-label">Team 1</span>
        <span class="cp-score-val" id="cp-score-1">0</span>
        <div class="cp-score-btns">
          <button onclick="cpScore(1,1)">+</button>
          <button onclick="cpScore(1,-1)">−</button>
        </div>
      </div>
      <div class="cp-team">
        <span class="cp-team-label">Team 2</span>
        <span class="cp-score-val" id="cp-score-2">0</span>
        <div class="cp-score-btns">
          <button onclick="cpScore(2,1)">+</button>
          <button onclick="cpScore(2,-1)">−</button>
        </div>
      </div>
      <button class="small-btn cp-reset-score" id="cp-reset-score">Reset scores</button>
    </div>

  </div>
</div>
<!-- /SLOT:tool -->

<!-- SLOT:ad_b -->
<!-- /SLOT:ad_b -->

<!-- SLOT:explainer -->
<h2>How to play Catchphrase</h2>
<p>Players sit in a circle with two alternating teams. The player holding the device sees a word or phrase and gives verbal clues — no acting, no spelling, no saying part of the phrase — until their team guesses it correctly. Then they pass the device to the next player on the opposing team. When the timer runs out, the team currently holding the device loses a point. First team to 7 wins.</p>

<h2>Tips for better games</h2>
<ul>
  <li><strong>Filter by age group:</strong> Use "Everyday" and "Food" for mixed ages, "Hard" for competitive groups.</li>
  <li><strong>Accelerating tension:</strong> The 60-second timer creates natural pressure. If your group wants more chaos, try 30 seconds.</li>
  <li><strong>Remote play:</strong> Share your screen and designate one person to tap "Next" when a word is guessed correctly.</li>
</ul>
<!-- /SLOT:explainer -->

<!-- SLOT:faq -->
<h2>Frequently asked questions</h2>
<details>
  <summary>How do you play Catchphrase?</summary>
  <p>Players alternate between two teams in a circle. The active player clues their team into the word without saying it, then passes the device when their team guesses. When the timer ends, the team holding the device loses that round.</p>
</details>
<details>
  <summary>Will words repeat during a session?</summary>
  <p>No. Words won't repeat until the full filtered pool is exhausted. Once every word has appeared, the pool resets so the game can keep going.</p>
</details>
<details>
  <summary>Can I filter words by category?</summary>
  <p>Yes — choose from Everyday, Actions, Places, People, Food, Entertainment, Idioms, or Hard. You can also filter by difficulty level (Easy, Medium, Hard) to tailor the game to your group.</p>
</details>
<details>
  <summary>What does the timer do?</summary>
  <p>The timer counts down from 30, 60, or 90 seconds. A beep warns when 10 seconds remain, and a triple beep signals time's up. The team holding the device when the timer ends loses the round.</p>
</details>
<!-- /SLOT:faq -->

<!-- SLOT:who -->
<h2>Who uses this</h2>
<ul>
  <li><strong>Party hosts</strong> who want the Catchphrase experience without tracking down the physical game</li>
  <li><strong>Remote teams</strong> looking for a fast, no-prep icebreaker on video calls</li>
  <li><strong>Families</strong> with kids old enough to give verbal clues (roughly age 8+)</li>
</ul>
<p>Also try: <a href="/scattergories-generator/">Scattergories Generator</a>, <a href="/charades-generator/">Charades Generator</a>, <a href="/pictionary-word-generator/">Pictionary Generator</a>, <a href="/truth-or-dare-generator/">Truth or Dare Generator</a>, <a href="/would-you-rather-generator/">Would You Rather Generator</a>.</p>
<!-- /SLOT:who -->

<!-- SLOT:init -->
<script>
(function(){
  'use strict';
  const SEED = [
    {text:'Alarm clock',category:'everyday',difficulty:'easy'},
    {text:'Traffic jam',category:'everyday',difficulty:'easy'},
    {text:'Comfort zone',category:'everyday',difficulty:'medium'},
    {text:'Double standard',category:'everyday',difficulty:'hard'},
    {text:'Juggling',category:'actions',difficulty:'easy'},
    {text:'Parallel parking',category:'actions',difficulty:'medium'},
    {text:'Improvising',category:'actions',difficulty:'hard'},
    {text:'Bus stop',category:'places',difficulty:'easy'},
    {text:'Amusement park',category:'places',difficulty:'easy'},
    {text:'Farmers market',category:'places',difficulty:'medium'},
    {text:'Celebrity',category:'people',difficulty:'easy'},
    {text:'Mechanic',category:'people',difficulty:'medium'},
    {text:'Ventriloquist',category:'people',difficulty:'hard'},
    {text:'Lunchbox',category:'food',difficulty:'easy'},
    {text:'Guacamole',category:'food',difficulty:'medium'},
    {text:'Tiramisu',category:'food',difficulty:'hard'},
    {text:'Plot twist',category:'entertainment',difficulty:'medium'},
    {text:'Cliffhanger',category:'entertainment',difficulty:'medium'},
    {text:'Break a leg',category:'idioms',difficulty:'easy'},
    {text:'Spill the beans',category:'idioms',difficulty:'easy'},
    {text:'Bite the bullet',category:'idioms',difficulty:'medium'},
    {text:'Burning the midnight oil',category:'idioms',difficulty:'hard'},
    {text:'Archipelago',category:'hard',difficulty:'hard'},
    {text:'Quantum leap',category:'hard',difficulty:'hard'}
  ];

  let fullData = null;
  let pool = [];
  let seen = new Set();
  const scores = [0, 0];

  const state = {
    category: 'all',
    difficulty: 'all',
    timerSecs: 60,
    timerDuration: 60,
    activeDur: 60,
    running: false,
    interval: null
  };

  let audioCtx = null;
  function getCtx() {
    if (!audioCtx) {
      try { audioCtx = new (window.AudioContext || window.webkitAudioContext)(); } catch(e){}
    }
    return audioCtx;
  }
  function beep(freq, dur) {
    const ctx = getCtx();
    if (!ctx) return;
    try {
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      osc.connect(gain); gain.connect(ctx.destination);
      osc.frequency.value = freq;
      gain.gain.setValueAtTime(0.25, ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + dur);
      osc.start(); osc.stop(ctx.currentTime + dur);
    } catch(e){}
  }

  function buildPool() {
    const src = fullData || SEED;
    pool = src.filter(function(item){
      return (state.category === 'all' || item.category === state.category) &&
             (state.difficulty === 'all' || item.difficulty === state.difficulty);
    });
    seen = new Set();
    updatePoolCount();
  }

  function updatePoolCount() {
    const el = document.getElementById('cp-pool-count');
    if (el) el.textContent = `${pool.length - seen.size} words remaining in pool`;
  }

  function nextWord() {
    let avail = pool.filter(function(item){ return !seen.has(item.text); });
    if (!avail.length) { seen = new Set(); avail = pool.slice(); }
    if (!avail.length) { document.getElementById('cp-word').textContent = 'No words match filters'; return; }
    const item = avail[Math.floor(Math.random() * avail.length)];
    seen.add(item.text);
    document.getElementById('cp-word').textContent = item.text;
    updatePoolCount();
  }

  function renderTimer() {
    const m = Math.floor(state.timerSecs / 60);
    const s = state.timerSecs % 60;
    const el = document.getElementById('cp-timer-display');
    if (!el) return;
    el.textContent = m > 0 ? `${m}:${String(s).padStart(2,'0')}` : String(s);
    el.classList.toggle('cp-timer--warning', state.timerSecs <= 10 && state.timerSecs > 5);
    el.classList.toggle('cp-timer--critical', state.timerSecs <= 5);
  }

  function startTimer() {
    if (state.running) {
      clearInterval(state.interval);
      state.running = false;
      document.getElementById('cp-timer-start').textContent = 'Start';
      return;
    }
    if (state.timerSecs <= 0) state.timerSecs = state.timerDuration;
    state.running = true;
    document.getElementById('cp-timer-start').textContent = 'Pause';
    state.interval = setInterval(function(){
      state.timerSecs--;
      renderTimer();
      if (state.timerSecs > 0 && state.timerSecs <= 10) beep(880, 0.08);
      if (state.timerSecs <= 0) {
        clearInterval(state.interval);
        state.running = false;
        document.getElementById('cp-timer-start').textContent = 'Start';
        beep(440, 0.3);
        setTimeout(function(){ beep(440, 0.3); }, 350);
        setTimeout(function(){ beep(440, 0.5); }, 700);
      }
    }, 1000);
  }

  window.cpScore = function(team, delta) {
    scores[team - 1] = Math.max(0, scores[team - 1] + delta);
    document.getElementById('cp-score-' + team).textContent = scores[team - 1];
  };

  document.getElementById('cp-next-btn').addEventListener('click', nextWord);
  document.getElementById('cp-word').addEventListener('click', nextWord);
  document.getElementById('cp-category').addEventListener('change', function(e){
    state.category = e.target.value;
    buildPool();
  });
  document.getElementById('cp-difficulty').addEventListener('change', function(e){
    state.difficulty = e.target.value;
    buildPool();
  });
  document.getElementById('cp-timer-start').addEventListener('click', startTimer);
  document.getElementById('cp-timer-reset').addEventListener('click', function(){
    clearInterval(state.interval);
    state.running = false;
    state.timerSecs = state.timerDuration;
    renderTimer();
    document.getElementById('cp-timer-start').textContent = 'Start';
  });
  document.getElementById('cp-reset-score').addEventListener('click', function(){
    scores[0] = 0; scores[1] = 0;
    document.getElementById('cp-score-1').textContent = '0';
    document.getElementById('cp-score-2').textContent = '0';
  });
  document.querySelectorAll('[data-cp-dur]').forEach(function(btn){
    btn.addEventListener('click', function(){
      state.activeDur = +btn.dataset.cpDur;
      state.timerDuration = state.activeDur;
      if (!state.running) { state.timerSecs = state.timerDuration; renderTimer(); }
      document.querySelectorAll('[data-cp-dur]').forEach(function(b){
        b.classList.toggle('active', +b.dataset.cpDur === state.activeDur);
      });
    });
  });

  fetch('/data/catchphrase.json')
    .then(function(r){ return r.ok ? r.json() : null; })
    .then(function(d){ if (d) { fullData = d; buildPool(); } })
    .catch(function(){});

  buildPool();
  renderTimer();
})();
</script>
<!-- /SLOT:init -->
```

- [ ] **Step 2: Build and check canonical**

```bash
cd template-deploy && python3 build.py 2>&1 | grep -E 'error|Error|catchphrase'
grep 'canonical' template-deploy/output/catchphrase-generator.html
```

Expected canonical: `https://wordineer.com/catchphrase-generator/`

- [ ] **Step 3: Commit**

```bash
git add template-deploy/tools-src/catchphrase-generator.html
git commit -m "feat: add catchphrase-generator.html tool source"
```

---

## Task 6: Create couples-truth-or-dare.json

**Files:**
- Create: `wordineer-deploy/data/couples-truth-or-dare.json`

- [ ] **Step 1: Write the data file**

Schema (mirrors truth-or-dare.json structure):
```json
{
  "sweet":    { "truth": [...strings...], "dare": [...strings...] },
  "fun":      { "truth": [...strings...], "dare": [...strings...] },
  "romantic": { "truth": [...strings...], "dare": [...strings...] },
  "spicy":    { "truth": [...strings...], "dare": [...strings...] }
}
```

Target: ≥150 truths and ≥150 dares total, distributed across 4 intensities (≥20 truths + ≥20 dares per intensity). ALL content must be PG-13 / advertiser-safe — playful and romantic, nothing explicit.

Example entries:
```json
{
  "sweet": {
    "truth": [
      "What was your first impression of me?",
      "What's your favorite memory of us together?",
      "What's one thing I do that always makes you smile?",
      "What's a little habit of mine you secretly love?",
      "When did you first know you had feelings for me?"
    ],
    "dare": [
      "Write your partner a three-sentence love note and read it aloud.",
      "Give your partner a 60-second shoulder massage.",
      "Tell your partner three things you're grateful for about them.",
      "Hold hands without letting go for the next three rounds.",
      "Draw a portrait of your partner in 60 seconds and show them."
    ]
  },
  "fun": {
    "truth": [
      "What's the most embarrassing thing that's happened to us in public?",
      "What's the weirdest food combination you've eaten that I don't know about?",
      "Have you ever laughed at something I said and pretended not to?",
      "What's a movie or show you've been secretly watching without me?",
      "What's the most ridiculous thing we've argued about?"
    ],
    "dare": [
      "Do your best impression of your partner for 30 seconds.",
      "Let your partner style your hair however they want for the rest of the game.",
      "Sing the chorus of the last song stuck in your head.",
      "Text a friend a ridiculous emoji sequence and wait for their reply.",
      "Do 10 jumping jacks while your partner counts out loud."
    ]
  },
  "romantic": {
    "truth": [
      "What's the most romantic thing you've ever wanted to do for me but haven't yet?",
      "Describe your ideal date night with me in detail.",
      "What's a song that makes you think of us?",
      "What's one way I could make you feel more appreciated?",
      "What's something about our relationship that you never want to change?"
    ],
    "dare": [
      "Look your partner in the eyes for 60 seconds without laughing.",
      "Re-enact your favorite moment from your first date.",
      "Slow dance together for one full song, even without music.",
      "Cook or order your partner's favorite meal tonight.",
      "Whisper something kind to your partner that you've been meaning to say."
    ]
  },
  "spicy": {
    "truth": [
      "What's something adventurous you'd like us to try together?",
      "What's the most romantic trip you'd want to take with me?",
      "If we could escape for a weekend with no responsibilities, where would you go?",
      "What's one thing you've always wanted to tell me but felt shy about?",
      "What's a personality trait of mine that you find really attractive?"
    ],
    "dare": [
      "Plan a surprise date night and describe it in detail right now.",
      "Write a one-paragraph story about your ideal future together.",
      "Make a playlist of five songs that describe your feelings for your partner.",
      "Take a photo together that captures how you feel about each other and save it.",
      "Tell your partner the most attractive thing about them — in front of anyone else in the room."
    ]
  }
}
```

Write 150+ truths and 150+ dares total, keeping all content PG-13.

- [ ] **Step 2: Validate**

```bash
node scripts/validate-data.js
```

Expected: all three data files show OK. Exit code 0.

- [ ] **Step 3: Commit**

```bash
git add wordineer-deploy/data/couples-truth-or-dare.json
git commit -m "feat: add couples-truth-or-dare.json data (150+ truths, 150+ dares)"
```

---

## Task 7: Build couples-truth-or-dare-generator.html

**Files:**
- Create: `template-deploy/tools-src/couples-truth-or-dare-generator.html`

- [ ] **Step 1: Read the existing truth-or-dare-generator.html in full to copy its structure**

```bash
cat template-deploy/tools-src/truth-or-dare-generator.html
```

The couples variant mirrors this file exactly, with these differences:
- CONFIG url: `/couples-truth-or-dare-generator/`, output: `couples-truth-or-dare-generator.html`
- H1: "Couples Truth or Dare Generator"
- Meta description targets "couples truth or dare" keywords
- Category filter replaced with intensity filter: `sweet | fun | romantic | spicy` (same seg pattern as truth/dare/both selector)
- Data loaded from `/data/couples-truth-or-dare.json`
- ID prefix: `ctd-` instead of whatever prefix truth-or-dare uses
- SEED_DATA structure: `{sweet:{truth:[...],dare:[...]}, fun:..., romantic:..., spicy:...}`
- State: `{count, type:'both', intensity:'all', current:[], saved:[], seen:new Set(), hidden:false}`
- `filtered()` function iterates over selected intensity group(s) and selects truth/dare based on `state.type`
- Internal link: add link to `/truth-or-dare-generator/` in SLOT:who section
- FAQPage schema with 5+ couples-specific questions

Write `template-deploy/tools-src/couples-truth-or-dare-generator.html` following the truth-or-dare pattern exactly, with the above substitutions applied.

- [ ] **Step 2: Build and check**

```bash
cd template-deploy && python3 build.py 2>&1 | grep -E 'error|Error|couples'
grep 'canonical' template-deploy/output/couples-truth-or-dare-generator.html
```

Expected canonical: `https://wordineer.com/couples-truth-or-dare-generator/`

- [ ] **Step 3: Commit**

```bash
git add template-deploy/tools-src/couples-truth-or-dare-generator.html
git commit -m "feat: add couples-truth-or-dare-generator.html tool source"
```

---

## Task 8: Update tools.json

**Files:**
- Modify: `template-deploy/tools.json`

- [ ] **Step 1: Check existing party game tool entries to find correct section keys**

```bash
python3 -c "
import json
d = json.load(open('template-deploy/tools.json'))
# Show mega categories
for cat in d.get('mega', []):
    print('MEGA:', cat.get('cat'), '—', len(cat.get('tools',[])), 'tools')
# Show more_word_tools count
print('more_word_tools:', len(d.get('more_word_tools', [])))
# Find charades entry location
for key in d:
    items = d[key]
    if isinstance(items, list):
        for item in items:
            if isinstance(item, dict) and 'charades' in str(item.get('href','')):
                print(f'charades in section [{key}]:', item.get('href'))
"
```

- [ ] **Step 2: Add the three new tools**

In `template-deploy/tools.json`, add entries for each new tool in the appropriate sections:

**In `mega`**: Find the "Games & fun" (or equivalent) category. If it has fewer than 4 tool links, add Scattergories. If it's already at 4, skip — the hub page handles discovery.

**In `more_word_tools`** (or whichever section charades is in): Add all 3 entries:
```json
{
  "href": "/scattergories-generator/",
  "name": "Scattergories Generator",
  "desc": "Roll a random letter and get 12 categories for a round of Scattergories.",
  "icon_bg": "#E6F1FB",
  "icon_path": "<text x='6.5' y='9.5' text-anchor='middle' font-size='8' fill='#185FA5' font-family='DM Serif Display,serif'>S</text>"
},
{
  "href": "/catchphrase-generator/",
  "name": "Catchphrase Generator",
  "desc": "Random words and phrases for the Catchphrase game, with timer and score tracker.",
  "icon_bg": "#E1F5EE",
  "icon_path": "<text x='6.5' y='9.5' text-anchor='middle' font-size='8' fill='#1D9E75' font-family='DM Serif Display,serif'>C</text>"
},
{
  "href": "/couples-truth-or-dare-generator/",
  "name": "Couples Truth or Dare",
  "desc": "Truth or dare questions designed for couples, from sweet to spicy.",
  "icon_bg": "#FAEEDA",
  "icon_path": "<text x='6.5' y='9.5' text-anchor='middle' font-size='8' fill='#BA7517' font-family='DM Serif Display,serif'>♥</text>"
}
```

**In `other_tools`**: Find the Games category column. If it has fewer than 4 tool links, add Scattergories (most representative of the 3). If at 4, skip.

**In `footer_cols`**: Find the Games column. Same rule — add only if under 4 links.

- [ ] **Step 3: Verify JSON is valid**

```bash
python3 -c "import json; json.load(open('template-deploy/tools.json')); print('JSON valid')"
```

- [ ] **Step 4: Commit**

```bash
git add template-deploy/tools.json
git commit -m "feat: register scattergories, catchphrase, couples-t&d in tools.json"
```

---

## Task 9: Update word-tools.html

**Files:**
- Modify: `template-deploy/tools-src/word-tools.html`

- [ ] **Step 1: Find the coming-soon cards for these 3 tools**

```bash
grep -n 'Scattergories\|Catchphrase\|Couples' template-deploy/tools-src/word-tools.html
```

- [ ] **Step 2: Replace each coming-soon card with a live card**

For each of the 3 tools, find the block:
```html
<div class="tool-item tool-item--soon">
  ...Tool Name <span class="soon-badge">Coming soon</span>...
</div>
```

Replace with (example for Scattergories):
```html
<div class="tool-item">
  <a href="/scattergories-generator/" class="tool-item-link">
    <div class="tool-icon" style="background:#E6F1FB">
      <svg viewBox="0 0 13 13" fill="none"><text x="6.5" y="9.5" text-anchor="middle" font-size="8" fill="#185FA5" font-family="DM Serif Display,serif">S</text></svg>
    </div>
    <div class="tool-name">Scattergories Generator</div>
    <div class="tool-desc">Roll a letter, get 12 categories. Play the classic word game anywhere.</div>
  </a>
</div>
```

Apply the same pattern to Catchphrase and Couples Truth or Dare, using their respective URLs, icon colors, and descriptions.

**Note:** Look at adjacent live tool cards in word-tools.html to confirm the exact HTML structure (class names, link wrapping) before editing. Match the existing live card pattern exactly.

- [ ] **Step 3: Verify no remaining coming-soon badges for these tools**

```bash
grep -n 'soon-badge\|tool--soon' template-deploy/tools-src/word-tools.html | grep -i 'scatter\|catchphrase\|couples'
```

Expected: no output.

- [ ] **Step 4: Commit**

```bash
git add template-deploy/tools-src/word-tools.html
git commit -m "feat: activate scattergories, catchphrase, couples-t&d cards on /word-tools/"
```

---

## Task 10: Update _redirects

**Files:**
- Modify: `wordineer-deploy/_redirects`

- [ ] **Step 1: Find where new tool redirects should be inserted**

```bash
grep -n 'charades\|pictionary' wordineer-deploy/_redirects | head -10
```

- [ ] **Step 2: Add 6 new lines (2 per tool: .html→slash 301, slash→.html 200)**

Insert these lines in `wordineer-deploy/_redirects` in the same section as the other tool redirects. Maintain alphabetical or the existing ordering pattern.

```
/scattergories-generator.html  /scattergories-generator/  301
/catchphrase-generator.html    /catchphrase-generator/    301
/couples-truth-or-dare-generator.html  /couples-truth-or-dare-generator/  301
/scattergories-generator/      /scattergories-generator.html  200
/catchphrase-generator/        /catchphrase-generator.html    200
/couples-truth-or-dare-generator/  /couples-truth-or-dare-generator.html  200
```

Check existing redirect pattern — some tools use tab-separated values, some use spaces. Match the existing formatting exactly.

- [ ] **Step 3: Commit**

```bash
git add wordineer-deploy/_redirects
git commit -m "feat: add redirect rules for 3 new party game tools"
```

---

## Task 11: Add bidirectional link in truth-or-dare-generator.html

**Files:**
- Modify: `template-deploy/tools-src/truth-or-dare-generator.html`

- [ ] **Step 1: Find the SLOT:who section**

```bash
grep -n 'SLOT:who\|couples\|SLOT:/who' template-deploy/tools-src/truth-or-dare-generator.html
```

- [ ] **Step 2: Add link to couples variant**

In the SLOT:who section, add one sentence linking to the couples variant. Find the existing "Also check out" or similar paragraph and append:
```html
Looking for a couples-specific version? Try our <a href="/couples-truth-or-dare-generator/">Couples Truth or Dare Generator</a> with intensity filters from sweet to romantic.
```

If no such paragraph exists, add one before `<!-- /SLOT:who -->`.

- [ ] **Step 3: Commit**

```bash
git add template-deploy/tools-src/truth-or-dare-generator.html
git commit -m "feat: add link to couples-truth-or-dare from truth-or-dare page"
```

---

## Task 12: Final build, copy, and verify

**Files:**
- Generated: `wordineer-deploy/scattergories-generator.html`, `wordineer-deploy/catchphrase-generator.html`, `wordineer-deploy/couples-truth-or-dare-generator.html`

- [ ] **Step 1: Run build**

```bash
cd template-deploy && python3 build.py
```

Expected: no errors. Output lists all pages including the 3 new ones.

- [ ] **Step 2: Copy output to deploy folder**

```bash
cp template-deploy/output/*.html wordineer-deploy/
```

- [ ] **Step 3: Verify canonical URLs in built output**

```bash
for slug in scattergories-generator catchphrase-generator couples-truth-or-dare-generator; do
  echo "=== $slug ===";
  grep 'canonical' wordineer-deploy/${slug}.html;
done
```

Expected: each shows `https://wordineer.com/[slug]/` (NOT the homepage URL).

- [ ] **Step 4: Check sitemap includes all 3 new URLs**

```bash
grep -E 'scattergories|catchphrase|couples-truth' wordineer-deploy/sitemap.xml
```

Expected: 3 matching lines with the new URLs.

- [ ] **Step 5: Spot-check no console errors (start local server)**

```bash
cd wordineer-deploy && python3 -m http.server 8080
```

Open http://localhost:8080/scattergories-generator/ in a browser. Verify:
- Letter displays and Roll button works
- Category list renders
- Timer starts and makes beep sounds
- Theme filter changes the category pool
- Print button opens print dialog
- Play Mode toggles expanded view
- No JS console errors

Repeat for /catchphrase-generator/ and /couples-truth-or-dare-generator/.

- [ ] **Step 6: Run final validation**

```bash
node scripts/validate-data.js
```

Expected: exit code 0, all OK.

- [ ] **Step 7: Commit all generated output**

```bash
git add wordineer-deploy/scattergories-generator.html wordineer-deploy/catchphrase-generator.html wordineer-deploy/couples-truth-or-dare-generator.html wordineer-deploy/sitemap.xml
git commit -m "feat: deploy session 1 party games — scattergories, catchphrase, couples-t&d"
```

---

## Verification Summary

After completing all tasks:
- [ ] `node scripts/validate-data.js` exits 0
- [ ] All 3 canonical URLs correct in built HTML
- [ ] All 3 pages in sitemap.xml
- [ ] All 3 coming-soon cards replaced on /word-tools/
- [ ] _redirects has .html→/ 301 + /→.html 200 for all 3
- [ ] truth-or-dare-generator.html links to couples variant
- [ ] Local server: no JS errors, all features work on all 3 pages
- [ ] All data: 0 filter combinations return empty results

**Stop here and report results before committing.**

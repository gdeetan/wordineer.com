# Spelling Bee Words Generator — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a filterable Spelling Bee Words generator at `/spelling-bee-words/` with grade level, difficulty, word origin, and count filters — plus save, copy, and print features.

**Architecture:** New JSON dataset (`spelling-bee-words.json`) loaded deferred on first generate. All filtering is client-side. Tool source file (`tools-src/spelling-bee-words.html`) assembled by `build.py` into `output/`, then copied to `wordineer-deploy/`. No framework — vanilla JS, existing CSS variables.

**Tech Stack:** Python 3 (build.py), vanilla JS, JSON data, Cloudflare Pages static hosting.

---

## File Map

| Action | Path |
|--------|------|
| Create | `wordineer-deploy/data/spelling-bee-words.json` |
| Create | `template-deploy/tools-src/spelling-bee-words.html` |
| Modify | `template-deploy/tools.json` |
| Modify | `wordineer-deploy/_redirects` |
| Generated | `template-deploy/output/spelling-bee-words.html` (by build.py) |
| Copied | `wordineer-deploy/spelling-bee-words.html` (from output/) |

---

## Task 1: Create the spelling-bee-words.json dataset

**Files:**
- Create: `wordineer-deploy/data/spelling-bee-words.json`

### Schema

Each entry:
```json
{ "w": "entrepreneur", "grade": "adult", "diff": "hard", "origin": "French", "syl": 5, "pos": "noun", "d": "a person who organizes and operates a business" }
```

Field constraints:
- `grade`: `"k-2"` | `"3-4"` | `"5-6"` | `"7-8"` | `"9-12"` | `"adult"`
- `diff`: `"easy"` | `"medium"` | `"hard"` | `"expert"`
- `origin`: `"Latin"` | `"Greek"` | `"French"` | `"Germanic"` | `"Anglo-Saxon"` | `"Spanish"` | `"Other"`
- `syl`: integer 1-7
- `pos`: `"noun"` | `"verb"` | `"adjective"` | `"adverb"`
- `d`: definition string <=100 chars

### Distribution targets (~1,000 words total)

| Grade | Easy | Medium | Hard | Expert |
|-------|------|--------|------|--------|
| k-2   | 50   | 30     | -    | -      |
| 3-4   | 40   | 40     | 20   | -      |
| 5-6   | 25   | 40     | 30   | 10     |
| 7-8   | 15   | 35     | 45   | 25     |
| 9-12  | -    | 25     | 60   | 55     |
| adult | -    | 15     | 70   | 75     |

Origin distribution: Anglo-Saxon/Germanic dominant in k-2/3-4; Latin/Greek rise from 5-6 onward; French/Spanish/Other scattered throughout upper grades.

- [ ] **Step 1: Write the JSON file**

Write `wordineer-deploy/data/spelling-bee-words.json` as a JSON array of ~1,000 word objects. Use the sample words below as quality/style reference for all entries.

**Sample words (reference — not exhaustive, build out all tiers to hit distribution targets):**

```json
[
  { "w": "cat", "grade": "k-2", "diff": "easy", "origin": "Anglo-Saxon", "syl": 1, "pos": "noun", "d": "a small furry domestic animal" },
  { "w": "jump", "grade": "k-2", "diff": "easy", "origin": "Germanic", "syl": 1, "pos": "verb", "d": "to push off the ground with your feet" },
  { "w": "friend", "grade": "k-2", "diff": "easy", "origin": "Anglo-Saxon", "syl": 1, "pos": "noun", "d": "a person you like and enjoy spending time with" },
  { "w": "between", "grade": "k-2", "diff": "easy", "origin": "Anglo-Saxon", "syl": 2, "pos": "adverb", "d": "in the middle of two things or people" },
  { "w": "dragon", "grade": "k-2", "diff": "medium", "origin": "Greek", "syl": 2, "pos": "noun", "d": "a mythical fire-breathing creature" },
  { "w": "magic", "grade": "k-2", "diff": "medium", "origin": "Greek", "syl": 2, "pos": "noun", "d": "the use of supernatural powers" },
  { "w": "jungle", "grade": "3-4", "diff": "easy", "origin": "Other", "syl": 2, "pos": "noun", "d": "a thick tropical forest" },
  { "w": "captain", "grade": "3-4", "diff": "easy", "origin": "Latin", "syl": 2, "pos": "noun", "d": "the leader of a ship, team, or group" },
  { "w": "distance", "grade": "3-4", "diff": "medium", "origin": "Latin", "syl": 3, "pos": "noun", "d": "the amount of space between two points" },
  { "w": "enormous", "grade": "3-4", "diff": "medium", "origin": "Latin", "syl": 3, "pos": "adjective", "d": "very large in size or amount" },
  { "w": "adventure", "grade": "3-4", "diff": "hard", "origin": "Latin", "syl": 3, "pos": "noun", "d": "an exciting or unusual experience" },
  { "w": "especially", "grade": "5-6", "diff": "easy", "origin": "Latin", "syl": 4, "pos": "adverb", "d": "more than usual; particularly" },
  { "w": "necessary", "grade": "5-6", "diff": "medium", "origin": "Latin", "syl": 4, "pos": "adjective", "d": "needed; required; essential" },
  { "w": "exaggerate", "grade": "5-6", "diff": "hard", "origin": "Latin", "syl": 4, "pos": "verb", "d": "to make something seem larger or greater than it is" },
  { "w": "pneumonia", "grade": "5-6", "diff": "hard", "origin": "Greek", "syl": 4, "pos": "noun", "d": "a serious infection of the lungs" },
  { "w": "silhouette", "grade": "5-6", "diff": "expert", "origin": "French", "syl": 3, "pos": "noun", "d": "a dark shape seen against a lighter background" },
  { "w": "conscience", "grade": "7-8", "diff": "medium", "origin": "Latin", "syl": 3, "pos": "noun", "d": "the inner sense of right and wrong" },
  { "w": "pharmaceutical", "grade": "7-8", "diff": "hard", "origin": "Greek", "syl": 5, "pos": "adjective", "d": "relating to medicinal drugs" },
  { "w": "surveillance", "grade": "7-8", "diff": "hard", "origin": "French", "syl": 3, "pos": "noun", "d": "close observation of a person or place" },
  { "w": "Mediterranean", "grade": "7-8", "diff": "expert", "origin": "Latin", "syl": 6, "pos": "adjective", "d": "relating to the Mediterranean Sea region" },
  { "w": "conscientious", "grade": "9-12", "diff": "medium", "origin": "Latin", "syl": 5, "pos": "adjective", "d": "careful and diligent in doing what is right" },
  { "w": "bureaucracy", "grade": "9-12", "diff": "hard", "origin": "French", "syl": 4, "pos": "noun", "d": "a system of government with complex rules" },
  { "w": "chrysanthemum", "grade": "9-12", "diff": "expert", "origin": "Greek", "syl": 5, "pos": "noun", "d": "a garden flower with many petals" },
  { "w": "onomatopoeia", "grade": "9-12", "diff": "expert", "origin": "Greek", "syl": 7, "pos": "noun", "d": "a word that phonetically imitates the sound it describes" },
  { "w": "connoisseur", "grade": "adult", "diff": "hard", "origin": "French", "syl": 3, "pos": "noun", "d": "an expert judge in matters of taste" },
  { "w": "soliloquy", "grade": "adult", "diff": "hard", "origin": "Latin", "syl": 4, "pos": "noun", "d": "a speech made when alone or not addressing others" },
  { "w": "desiccate", "grade": "adult", "diff": "expert", "origin": "Latin", "syl": 3, "pos": "verb", "d": "to remove moisture from; to dry out completely" },
  { "w": "syzygy", "grade": "adult", "diff": "expert", "origin": "Greek", "syl": 3, "pos": "noun", "d": "alignment of three celestial bodies in a straight line" },
  { "w": "ptarmigan", "grade": "adult", "diff": "expert", "origin": "Other", "syl": 3, "pos": "noun", "d": "an Arctic grouse with feathered feet" }
]
```

Quality rules:
- Definitions must be <=100 chars and use plain language
- `syl` must be accurate for the word
- `origin` must be etymologically correct
- No duplicate `w` values in the array
- Easy k-2: 1-2 syllables, phonetic, common sight words
- Expert adult: 4+ syllables, rare, competition-level vocabulary

- [ ] **Step 2: Verify JSON is valid**

```bash
cd "/Users/garrickdeetan/Documents/Random Word Generator Tool Site"
python3 -c "import json; d=json.load(open('wordineer-deploy/data/spelling-bee-words.json')); print(f'{len(d)} words loaded')"
```

Expected: `950 words loaded` or similar (within 10% of 1,000).

- [ ] **Step 3: Verify distribution**

```bash
python3 -c "
import json
d = json.load(open('wordineer-deploy/data/spelling-bee-words.json'))
from collections import Counter
grades = Counter(w['grade'] for w in d)
diffs = Counter(w['diff'] for w in d)
origins = Counter(w['origin'] for w in d)
print('Grades:', dict(sorted(grades.items())))
print('Diffs:', dict(sorted(diffs.items())))
print('Origins:', dict(sorted(origins.items())))
print('Total:', len(d))
"
```

Expected: all 6 grade values present, all 4 diff values present, at least 5 origin values present, total >= 900.

- [ ] **Step 4: Commit**

```bash
git add wordineer-deploy/data/spelling-bee-words.json
git commit -m "feat: add spelling-bee-words.json dataset (~1000 words)"
```

---

## Task 2: Register tool in tools.json

**Files:**
- Modify: `template-deploy/tools.json`

- [ ] **Step 1: Read tools.json and locate the three insertion points**

Open `template-deploy/tools.json`. Find:
1. The `mega` array - the object whose category contains word/writing tools. Add to its `tools` array.
2. The `more_word_tools` array - add a new entry object.
3. The `footer_cols` array - find the column with word tool links, add to its `links` array.

- [ ] **Step 2: Add to mega menu tools array**

```json
{ "href": "/spelling-bee-words/", "text": "Spelling Bee Words" }
```

- [ ] **Step 3: Add to more_word_tools array**

```json
{
  "href": "/spelling-bee-words/",
  "name": "Spelling Bee Words",
  "desc": "Filter 1,000+ spelling bee words by grade, difficulty, and word origin. Save and print custom lists.",
  "icon_bg": "#EEF4FE",
  "icon_path": "<path d=\"M12 3l2.5 7.5H22l-6.5 4.5 2.5 7.5L12 18l-6 4.5 2.5-7.5L3 10.5h7.5z\" stroke=\"#3B6FD4\" stroke-width=\"1.3\" stroke-linecap=\"round\" stroke-linejoin=\"round\" fill=\"none\"/>"
}
```

- [ ] **Step 4: Add to footer_cols links array**

```json
{ "href": "/spelling-bee-words/", "text": "Spelling Bee Words" }
```

- [ ] **Step 5: Verify JSON is valid**

```bash
python3 -c "import json; json.load(open('template-deploy/tools.json')); print('tools.json OK')"
```

Expected: `tools.json OK`

- [ ] **Step 6: Commit**

```bash
git add template-deploy/tools.json
git commit -m "feat: register spelling-bee-words in tools.json (mega, grid, footer)"
```

---

## Task 3: Add clean URL redirect

**Files:**
- Modify: `wordineer-deploy/_redirects`

- [ ] **Step 1: Append redirect line**

Open `wordineer-deploy/_redirects` and add at the end:
```
/spelling-bee-words   /spelling-bee-words/   301
```

- [ ] **Step 2: Commit**

```bash
git add wordineer-deploy/_redirects
git commit -m "feat: add clean URL redirect for spelling-bee-words"
```

---

## Task 4: Create tool source HTML

**Files:**
- Create: `template-deploy/tools-src/spelling-bee-words.html`

- [ ] **Step 1: Create the file — CONFIG + SLOT:meta**

Write `template-deploy/tools-src/spelling-bee-words.html` starting with:

```html
<!-- CONFIG
{ "url": "/spelling-bee-words/", "output": "spelling-bee-words.html", "type": "tool" }
-->

<!-- SLOT:meta -->
<title>Spelling Bee Words Generator — Filter by Grade & Difficulty | Wordineer</title>
<meta name="description" content="Generate spelling bee words filtered by grade level (K-12 & adult), difficulty, and word origin. Save words, print custom lists, and practice for any bee competition.">
<meta property="og:title" content="Spelling Bee Words Generator | Wordineer">
<meta property="og:description" content="1,000+ spelling bee words filtered by grade, difficulty, and etymology. Free, instant, printable.">
<meta property="og:url" content="https://wordineer.com/spelling-bee-words/">
<link rel="canonical" href="https://wordineer.com/spelling-bee-words/">
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "WebApplication",
  "name": "Spelling Bee Words Generator",
  "url": "https://wordineer.com/spelling-bee-words/",
  "description": "Generate and filter spelling bee words by grade level, difficulty, and word origin.",
  "applicationCategory": "EducationApplication",
  "operatingSystem": "Any",
  "offers": { "@type": "Offer", "price": "0" }
}
</script>
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    { "@type": "Question", "name": "What grade levels does this spelling bee words tool cover?", "acceptedAnswer": { "@type": "Answer", "text": "The tool covers K-2, grades 3-4, 5-6, 7-8, 9-12, and adult spelling bee levels, totaling over 1,000 words." } },
    { "@type": "Question", "name": "Can I print the spelling bee word list?", "acceptedAnswer": { "@type": "Answer", "text": "Yes. Click the Print List button to open a clean, formatted printable version of your current word list." } },
    { "@type": "Question", "name": "Are these official Scripps National Spelling Bee words?", "acceptedAnswer": { "@type": "Answer", "text": "This tool is for practice and preparation. The words reflect the style and difficulty of competition spelling bees but are not the official Scripps word list." } },
    { "@type": "Question", "name": "What does word origin mean for spelling bee words?", "acceptedAnswer": { "@type": "Answer", "text": "Word origin (etymology) tells you which language a word came from. Learning origin patterns helps you predict spellings for unfamiliar words." } },
    { "@type": "Question", "name": "How do I save spelling bee words for focused practice?", "acceptedAnswer": { "@type": "Answer", "text": "Click the heart icon on any word to save it. Saved words appear below the list and persist until you remove them." } },
    { "@type": "Question", "name": "What is the difference between Easy, Medium, Hard, and Expert difficulty?", "acceptedAnswer": { "@type": "Answer", "text": "Easy maps to school-level bees, Medium to district bees, Hard to regional bees, and Expert to state and national competition level." } },
    { "@type": "Question", "name": "How many spelling bee words are in the database?", "acceptedAnswer": { "@type": "Answer", "text": "The database contains over 1,000 spelling bee words spanning all grade levels and difficulty tiers." } }
  ]
}
</script>
<!-- /SLOT:meta -->
```

- [ ] **Step 2: Append SLOT:style**

```html
<!-- SLOT:style -->
<style>
.breadcrumb { padding: 10px 0 0; }
.breadcrumb-inner { display: flex; align-items: center; gap: 6px; font-size: 0.82rem; color: var(--text-muted, #6b7280); flex-wrap: wrap; }
.breadcrumb-inner a { color: var(--text-muted, #6b7280); text-decoration: none; }
.breadcrumb-inner a:hover { text-decoration: underline; }
.breadcrumb-sep { color: var(--text-muted, #6b7280); }

.sb-seg { display: flex; flex-wrap: wrap; gap: 4px; margin-top: 4px; }
.sb-seg button { padding: 5px 10px; border-radius: 6px; border: 1px solid var(--border, #e5e7eb); background: #fff; font-size: 0.8rem; cursor: pointer; color: var(--text, #111); transition: background 0.15s, border-color 0.15s; }
.sb-seg button.active { background: var(--brand, #6c63ff); color: #fff; border-color: var(--brand, #6c63ff); }
.sb-seg button:hover:not(.active) { background: #f3f4f6; }

#sb-list { list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 8px; }
.sb-item { padding: 10px 12px; border: 1px solid var(--border, #e5e7eb); border-radius: 8px; background: #fff; }
.sb-word-row { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; }
.sb-word { font-size: 1.05rem; font-weight: 600; color: var(--text, #111); flex: 1 1 auto; }
.sb-origin { font-size: 0.72rem; padding: 2px 7px; border-radius: 99px; font-weight: 500; white-space: nowrap; }
.sb-origin[data-o="Latin"]       { background: #eef2ff; color: #3730a3; }
.sb-origin[data-o="Greek"]       { background: #f5f3ff; color: #6d28d9; }
.sb-origin[data-o="French"]      { background: #fff0f3; color: #9d174d; }
.sb-origin[data-o="Germanic"]    { background: #f0fdf4; color: #166534; }
.sb-origin[data-o="Anglo-Saxon"] { background: #ecfdf5; color: #065f46; }
.sb-origin[data-o="Spanish"]     { background: #fff7ed; color: #9a3412; }
.sb-origin[data-o="Other"]       { background: #f3f4f6; color: #374151; }
.sb-syl { font-size: 0.72rem; color: var(--text-muted, #6b7280); white-space: nowrap; }
.sb-pos { font-size: 0.72rem; color: var(--text-muted, #6b7280); font-style: italic; white-space: nowrap; }
.sb-save, .sb-copy-word { background: none; border: none; cursor: pointer; font-size: 1rem; padding: 2px 4px; color: var(--text-muted, #9ca3af); transition: color 0.15s; }
.sb-save:hover { color: #ef4444; }
.sb-save.saved { color: #ef4444; }
.sb-copy-word:hover { color: var(--brand, #6c63ff); }
.sb-def { font-size: 0.85rem; color: var(--text-muted, #6b7280); margin-top: 4px; line-height: 1.4; }
.sb-def.hidden { display: none; }
.sb-empty { color: var(--text-muted, #6b7280); font-size: 0.9rem; padding: 16px 0; text-align: center; }

.sb-top-bar { display: flex; align-items: center; gap: 8px; margin-bottom: 10px; flex-wrap: wrap; }
.sb-count-label { font-size: 0.85rem; color: var(--text-muted, #6b7280); flex: 1; }

.saved-section { margin-top: 16px; }
.saved-top { display: flex; align-items: center; gap: 8px; margin-bottom: 8px; flex-wrap: wrap; }
.saved-label { font-size: 0.85rem; font-weight: 600; color: var(--text, #111); }
.saved-copy { font-size: 0.8rem; color: var(--brand, #6c63ff); cursor: pointer; }
.saved-copy:hover { text-decoration: underline; }
.saved-tags { display: flex; flex-wrap: wrap; gap: 6px; }
.saved-tag { display: flex; align-items: center; gap: 4px; background: #f3f4f6; border-radius: 99px; padding: 3px 10px; font-size: 0.82rem; }
.saved-tag button { background: none; border: none; cursor: pointer; color: #9ca3af; font-size: 0.9rem; padding: 0; line-height: 1; }
.saved-tag button:hover { color: #ef4444; }

.def-toggle-row { display: flex; align-items: center; gap: 8px; margin-top: 12px; }
.def-toggle-row label { font-size: 0.85rem; color: var(--text, #111); cursor: pointer; }

@media print {
  header, nav, .breadcrumb, .ctrl, .sb-top-bar, .saved-section, footer, .ad, [class*="ad-"] { display: none !important; }
  .sb-item { border: none; border-bottom: 1px solid #e5e7eb; border-radius: 0; padding: 8px 0; break-inside: avoid; }
  .sb-word { font-size: 1.1rem; }
  .sb-word-row { gap: 12px; }
  .sb-def, .sb-def.hidden { display: block !important; }
  .sb-save, .sb-copy-word { display: none !important; }
  @page { margin: 1.5cm; }
}
</style>
<!-- /SLOT:style -->
```

- [ ] **Step 3: Append SLOT:hero**

```html
<!-- SLOT:hero -->
<div class="breadcrumb">
  <div class="breadcrumb-inner">
    <a href="/">Wordineer</a>
    <span class="breadcrumb-sep">›</span>
    <a href="/word-tools/">Word Tools</a>
    <span class="breadcrumb-sep">›</span>
    <span aria-current="page">Spelling Bee Words</span>
  </div>
</div>
<div class="hero-badge">1,000+ Words</div>
<h1>Spelling Bee Words Generator</h1>
<p>Filter over 1,000 spelling bee words by grade level, difficulty, and word origin. Save your practice list or print it for classroom use — no login required.</p>
<!-- /SLOT:hero -->
```

- [ ] **Step 4: Append SLOT:tool**

```html
<!-- SLOT:tool -->
<div class="tool-wrap">
  <div class="tool-card">
    <div class="tool-split">

      <div class="ctrl">
        <div class="ctrl-row">
          <label class="ctrl-label">Grade Level</label>
          <div class="sb-seg" id="seg-grade">
            <button class="active" data-val="all">All</button>
            <button data-val="k-2">K-2</button>
            <button data-val="3-4">3-4</button>
            <button data-val="5-6">5-6</button>
            <button data-val="7-8">7-8</button>
            <button data-val="9-12">9-12</button>
            <button data-val="adult">Adult</button>
          </div>
        </div>

        <div class="ctrl-row">
          <label class="ctrl-label">Difficulty</label>
          <div class="sb-seg" id="seg-diff">
            <button class="active" data-val="all">All</button>
            <button data-val="easy">Easy</button>
            <button data-val="medium">Medium</button>
            <button data-val="hard">Hard</button>
            <button data-val="expert">Expert</button>
          </div>
        </div>

        <div class="ctrl-row">
          <label class="ctrl-label" for="ctrl-origin">Word Origin</label>
          <select id="ctrl-origin" class="ctrl-select">
            <option value="all">All Origins</option>
            <option value="Latin">Latin</option>
            <option value="Greek">Greek</option>
            <option value="French">French</option>
            <option value="Germanic">Germanic</option>
            <option value="Anglo-Saxon">Anglo-Saxon</option>
            <option value="Spanish">Spanish</option>
            <option value="Other">Other</option>
          </select>
        </div>

        <div class="ctrl-row">
          <label class="ctrl-label" for="ctrl-count">Number of words</label>
          <input type="number" id="ctrl-count" value="20" min="5" max="50" class="ctrl-input">
        </div>

        <div class="def-toggle-row">
          <input type="checkbox" id="ctrl-defs" checked>
          <label for="ctrl-defs">Show definitions</label>
        </div>

        <button class="gen-btn" id="sb-gen-btn">Generate</button>
      </div>

      <div class="results-col">
        <div class="sb-top-bar">
          <span class="sb-count-label" id="sb-count">20 words</span>
          <button class="act-btn" id="sb-copy-all">Copy all</button>
          <button class="act-btn" id="sb-print-btn">Print list</button>
        </div>
        <ul class="word-list" id="sb-list"></ul>
      </div>

    </div>
  </div>

  <div class="saved-section">
    <div class="saved-top">
      <span class="saved-label">Saved words <span id="sb-saved-count">(0)</span></span>
      <span class="saved-copy" id="sb-copy-saved">Copy saved</span>
    </div>
    <div class="saved-tags" id="sb-saved-tags"></div>
  </div>
</div>
<!-- /SLOT:tool -->
```

- [ ] **Step 5: Append SLOT:ad_b**

```html
<!-- SLOT:ad_b -->
<!-- /SLOT:ad_b -->
```

- [ ] **Step 6: Append SLOT:explainer**

```html
<!-- SLOT:explainer -->
<section class="explainer">

<h2>What Is a Spelling Bee?</h2>
<p>A spelling bee is a competition in which participants are asked to spell words aloud, one at a time, until only one person remains without making an error. The format dates back to the 19th century in the United States and became nationally organized through the Scripps National Spelling Bee, held annually in Washington, D.C. Students from elementary through high school compete through school, district, regional, and state levels before reaching the national stage. Spelling bees build vocabulary, improve language awareness, and sharpen focus under pressure.</p>

<h2>What Is This Tool?</h2>
<p>The Wordineer Spelling Bee Words Generator gives you instant access to over 1,000 spelling bee words drawn from all competition levels — from early elementary up through adult regional bees. Unlike static word lists that show the same words every time, this generator produces a fresh, randomly drawn selection every time you click Generate. You control exactly what you get: filter by grade level, difficulty tier, word origin, and quantity. When you find words worth keeping, save them to your session list or print the entire set in a clean, numbered format ready for classroom use.</p>

<h2>Why Use Wordineer's Spelling Bee Words Generator?</h2>
<p>Most spelling bee word resources are static pages — the same list every visit, impossible to filter, and awkward to print. This tool works differently:</p>
<ul>
  <li><strong>Instant random generation</strong> — a new set of words every time, so practice never feels like memorizing the same list</li>
  <li><strong>Etymology badges on every word</strong> — see whether a word comes from Latin, Greek, French, or another family, which helps you decode unfamiliar spellings using origin patterns</li>
  <li><strong>Syllable count displayed</strong> — knowing how many syllables a word has helps with pacing and pronunciation before spelling</li>
  <li><strong>One-click print mode</strong> — generates a numbered, formatted word list ready for coaches to hand out or read aloud in practice rounds</li>
  <li><strong>Save words across the session</strong> — build a personal study list from multiple generated sets without retyping anything</li>
  <li><strong>No account, no paywall</strong> — completely free and works on any device</li>
</ul>

<h2>How It Works</h2>
<ol>
  <li><strong>Choose a grade level</strong> — select the level that matches the competition you're preparing for, or choose All to pull from every level.</li>
  <li><strong>Set a difficulty</strong> — Easy through Expert maps to school through national competition difficulty.</li>
  <li><strong>Filter by word origin (optional)</strong> — target Latin or Greek roots for a themed practice session, or leave it on All.</li>
  <li><strong>Set the count</strong> — choose 5 to 50 words per generated list.</li>
  <li><strong>Click Generate</strong> — a random selection meeting your filters appears instantly.</li>
  <li><strong>Save or print</strong> — heart-save individual words to your session list, or click Print List for a classroom-ready printout.</li>
</ol>

<h2>Grade-Level Breakdown</h2>
<p>Each grade band reflects the typical difficulty and vocabulary scope seen in competitions at that level:</p>
<ul>
  <li><strong>K-2 (School Bee, Early)</strong> — Short, phonetically regular words of 1-2 syllables. Common sight words and simple noun/verb vocabulary. Anglo-Saxon and Germanic roots dominate. Examples: <em>jump, friend, queen, dragon</em>.</li>
  <li><strong>Grades 3-4 (School Bee)</strong> — Two- and three-syllable words begin to appear. Common prefixes and suffixes (un-, re-, -tion, -ful). Latin borrowings start appearing in the medium range. Examples: <em>captain, distance, enormous, adventure</em>.</li>
  <li><strong>Grades 5-6 (District Bee)</strong> — Latin and Greek roots become prominent. Silent letters, double consonants, and irregular patterns increase. Examples: <em>necessary, pneumonia, exaggerate, silhouette</em>.</li>
  <li><strong>Grades 7-8 (Regional Bee)</strong> — Borrowed words from French, Italian, and Spanish. Advanced compound Greek roots. Long multi-syllable Latin academic vocabulary. Examples: <em>surveillance, pharmaceutical, Mediterranean</em>.</li>
  <li><strong>Grades 9-12 (State Bee)</strong> — Championship vocabulary. Rare patterns, obscure origins, words from science, law, music, and classical studies. Examples: <em>chrysanthemum, onomatopoeia, bureaucracy</em>.</li>
  <li><strong>Adult (Adult/Regional Bee)</strong> — The most demanding tier. Words rarely encountered in everyday use, from specialized fields and classical languages. Examples: <em>syzygy, desiccate, soliloquy, connoisseur</em>.</li>
</ul>

<h2>Understanding Word Origins</h2>
<p>One of the most powerful strategies in spelling bee preparation is learning to recognize word origin patterns. When you know where a word came from, you can often predict its spelling without having memorized it.</p>
<ul>
  <li><strong>Latin</strong> — The largest source of academic English vocabulary. Look for endings like <em>-tion, -ance, -ent, -ous, -ity</em>. Examples: <em>accommodation, perseverance, conscientious</em>.</li>
  <li><strong>Greek</strong> — Scientific and philosophical vocabulary. Key patterns: <em>ph</em> = /f/ (phonics, pharmacy), <em>ch</em> = /k/ (character, chorus), silent initial <em>p</em> (psychology, pterodactyl). Examples: <em>phenomenon, chrysanthemum, onomatopoeia</em>.</li>
  <li><strong>French</strong> — Elegant borrowings with unexpected endings: <em>-eur, -ette, -esque, -oire</em>. Examples: <em>entrepreneur, silhouette, picturesque</em>.</li>
  <li><strong>Germanic / Anglo-Saxon</strong> — The core of everyday English. Often phonetically straightforward, but watch for double consonants and -ght patterns. Examples: <em>strength, through, knight</em>.</li>
  <li><strong>Spanish / Italian / Arabic</strong> — Scattered across categories. Look for <em>-illo, -anza</em> (Spanish), <em>-etto, -ino</em> (Italian), or <em>al-</em> prefix (Arabic: algebra, alcohol).</li>
</ul>

<h2>Best Practices for Spelling Bee Preparation</h2>
<p>Spelling better means practicing smarter, not harder. Here are the habits that help most:</p>
<ul>
  <li><strong>Say the word aloud before spelling it.</strong> In competition, competitors may ask for the definition, part of speech, language of origin, and a sample sentence. Practice using all of these.</li>
  <li><strong>Learn the origin, not just the word.</strong> Knowing that <em>ph</em> = /f/ in Greek-origin words lets you spell dozens of words you've never seen before. One rule unlocks many words.</li>
  <li><strong>Drill easy words to build fluency.</strong> Nervousness causes mistakes on easy words in competition. Start each session with simpler words to build confidence before moving to harder ones.</li>
  <li><strong>Practice under mild time pressure.</strong> Practice spelling each word within 10 to 15 seconds to simulate competition pacing.</li>
  <li><strong>Review saved words daily.</strong> In the final week before a competition, focus your review on the words you've saved.</li>
  <li><strong>Mix grade levels in the same session.</strong> Master your own grade level first, then regularly preview words from the next level up to build stretch vocabulary.</li>
</ul>

<h2>Tips for Teachers and Coaches</h2>
<p>Running a classroom spelling bee or coaching a team for district competition? Here's how to get the most out of the generator:</p>
<ul>
  <li><strong>Use grade filter for level-appropriate lists.</strong> Pull exactly the difficulty range needed for your class without manually sorting through a massive list.</li>
  <li><strong>Print multiple difficulty tiers separately.</strong> Generate and print Easy words, then Medium, then Hard — use them as separate rounds in an elimination format.</li>
  <li><strong>Run themed practice sessions by origin.</strong> Filter to "Latin" or "Greek" origin words for a day focused on root patterns rather than random vocabulary.</li>
  <li><strong>Generate a fresh list every session.</strong> Prevents students from memorizing a fixed word sequence rather than actually learning to spell the words.</li>
  <li><strong>Use Expert words to challenge advanced students</strong> without jumping to an inappropriate grade level — Expert tier within any grade reflects what competition-level competitors encounter.</li>
</ul>

</section>
<!-- /SLOT:explainer -->
```

- [ ] **Step 7: Append SLOT:faq**

```html
<!-- SLOT:faq -->
<section class="faq">
<h2>Frequently Asked Questions</h2>

<details>
  <summary>What grade levels does this spelling bee words tool cover?</summary>
  <p>The tool covers K-2, grades 3-4, grades 5-6, grades 7-8, grades 9-12, and adult spelling bee levels. Each grade band reflects the vocabulary typically used at school, district, regional, and national competition levels for that age group.</p>
</details>

<details>
  <summary>How many spelling bee words are in the database?</summary>
  <p>The database contains over 1,000 spelling bee words distributed across all grade levels and all four difficulty tiers — Easy, Medium, Hard, and Expert.</p>
</details>

<details>
  <summary>Can I print the spelling bee word list?</summary>
  <p>Yes. After generating a word list, click <strong>Print List</strong>. This opens your browser's print dialog with a clean, numbered version of the word list — suitable for handing out in class or reading aloud in practice rounds.</p>
</details>

<details>
  <summary>What does word origin mean, and why does it matter?</summary>
  <p>Word origin (etymology) tells you which language a word came from — Latin, Greek, French, Germanic, etc. Words from the same origin family tend to share spelling patterns. Recognizing origin patterns lets you make educated guesses about spellings you haven't memorized.</p>
</details>

<details>
  <summary>How do I save words for focused practice?</summary>
  <p>Click the heart (♥) icon on any word to save it to your session list. Saved words appear below the word list and persist until you remove them. Use <strong>Copy saved</strong> to copy your saved list to the clipboard.</p>
</details>

<details>
  <summary>What is the difference between Easy, Medium, Hard, and Expert difficulty?</summary>
  <p>Easy words reflect school-level spelling bee vocabulary. Medium maps to district bee difficulty. Hard reflects regional and state bee competition. Expert covers words at the national and championship level — rare vocabulary from specialized fields and unusual spelling patterns.</p>
</details>

<details>
  <summary>Are these official Scripps National Spelling Bee words?</summary>
  <p>This tool is designed for spelling bee practice and preparation. The words reflect the style, difficulty, and vocabulary scope of competition spelling bees at each grade level, but this is not the official Scripps word list. For official competition preparation, consult the Scripps National Spelling Bee's published study resources.</p>
</details>

</section>
<!-- /SLOT:faq -->
```

- [ ] **Step 8: Append SLOT:who**

```html
<!-- SLOT:who -->
<section class="who">
<h2>Who Uses This Tool?</h2>
<ul>
  <li><strong>Students</strong> preparing for school, district, regional, and national spelling bee competitions</li>
  <li><strong>Parents</strong> running practice rounds at home with their children</li>
  <li><strong>Teachers</strong> building custom word lists and printable practice sheets for classroom bees</li>
  <li><strong>Spelling bee coaches</strong> who need fresh, level-appropriate lists for structured practice sessions</li>
  <li><strong>Homeschool educators</strong> covering spelling bee preparation without a pre-built curriculum</li>
  <li><strong>Adults</strong> competing in adult spelling bee events or building vocabulary for personal enrichment</li>
</ul>
</section>
<!-- /SLOT:who -->
```

- [ ] **Step 9: Append SLOT:init**

```html
<!-- SLOT:init -->
<script>
(function () {
  var SBT = {
    data: null,
    saved: JSON.parse(localStorage.getItem('sb-saved') || '[]'),
    grade: 'all',
    diff: 'all',

    load: function () {
      var self = this;
      if (self.data) return Promise.resolve(self.data);
      return fetch('/data/spelling-bee-words.json')
        .then(function (r) { return r.json(); })
        .then(function (d) { self.data = d; return d; });
    },

    filter: function (words) {
      var g = this.grade, d = this.diff;
      var origin = document.getElementById('ctrl-origin').value;
      var count = parseInt(document.getElementById('ctrl-count').value, 10) || 20;
      var result = words.slice();
      if (g !== 'all') result = result.filter(function (w) { return w.grade === g; });
      if (d !== 'all') result = result.filter(function (w) { return w.diff === d; });
      if (origin !== 'all') result = result.filter(function (w) { return w.origin === origin; });
      for (var i = result.length - 1; i > 0; i--) {
        var j = Math.floor(Math.random() * (i + 1));
        var tmp = result[i]; result[i] = result[j]; result[j] = tmp;
      }
      return result.slice(0, count);
    },

    generate: function () {
      var self = this;
      self.load().then(function (words) {
        self.render(self.filter(words));
      });
    },

    render: function (words) {
      var list = document.getElementById('sb-list');
      var countEl = document.getElementById('sb-count');
      var showDef = document.getElementById('ctrl-defs').checked;
      var saved = this.saved;

      if (!words.length) {
        list.innerHTML = '<li class="sb-empty">No words match your filters. Try adjusting grade or difficulty.</li>';
        countEl.textContent = '0 words';
        return;
      }

      countEl.textContent = words.length + ' word' + (words.length !== 1 ? 's' : '');
      list.innerHTML = words.map(function (w) {
        var isSaved = saved.indexOf(w.w) !== -1;
        var esc = w.w.replace(/\\/g, '\\\\').replace(/'/g, "\\'");
        return '<li class="sb-item" data-word="' + w.w + '">' +
          '<div class="sb-word-row">' +
          '<span class="sb-word">' + w.w + '</span>' +
          '<span class="sb-origin" data-o="' + w.origin + '">' + w.origin + '</span>' +
          '<span class="sb-syl">' + w.syl + ' syl</span>' +
          '<span class="sb-pos">' + w.pos + '</span>' +
          '<button class="sb-save' + (isSaved ? ' saved' : '') + '" onclick="SBT.toggleSave(\'' + esc + '\')" title="Save word">&#9829;</button>' +
          '<button class="sb-copy-word" onclick="SBT.copyWord(\'' + esc + '\')" title="Copy word">&#10064;</button>' +
          '</div>' +
          '<div class="sb-def' + (showDef ? '' : ' hidden') + '">' + w.d + '</div>' +
          '</li>';
      }).join('');
    },

    toggleSave: function (word) {
      var idx = this.saved.indexOf(word);
      if (idx === -1) this.saved.push(word);
      else this.saved.splice(idx, 1);
      localStorage.setItem('sb-saved', JSON.stringify(this.saved));
      this.renderSaved();
      var btn = document.querySelector('.sb-item[data-word="' + word + '"] .sb-save');
      if (btn) btn.classList.toggle('saved', this.saved.indexOf(word) !== -1);
    },

    renderSaved: function () {
      var container = document.getElementById('sb-saved-tags');
      var count = document.getElementById('sb-saved-count');
      count.textContent = '(' + this.saved.length + ')';
      container.innerHTML = this.saved.map(function (w) {
        var esc = w.replace(/\\/g, '\\\\').replace(/'/g, "\\'");
        return '<span class="saved-tag">' + w +
          '<button onclick="SBT.toggleSave(\'' + esc + '\')">&#215;</button></span>';
      }).join('');
    },

    copyAll: function () {
      var words = [].slice.call(document.querySelectorAll('#sb-list .sb-word')).map(function (el) { return el.textContent; });
      if (navigator.clipboard) navigator.clipboard.writeText(words.join('\n'));
    },

    copySaved: function () {
      if (navigator.clipboard) navigator.clipboard.writeText(this.saved.join('\n'));
    },

    copyWord: function (word) {
      if (navigator.clipboard) navigator.clipboard.writeText(word);
    },

    toggleDefs: function () {
      var show = document.getElementById('ctrl-defs').checked;
      [].slice.call(document.querySelectorAll('.sb-def')).forEach(function (el) {
        el.classList.toggle('hidden', !show);
      });
    },

    initSeg: function (id, key) {
      var self = this;
      var seg = document.getElementById(id);
      if (!seg) return;
      seg.addEventListener('click', function (e) {
        var btn = e.target.closest('button');
        if (!btn) return;
        [].slice.call(seg.querySelectorAll('button')).forEach(function (b) { b.classList.remove('active'); });
        btn.classList.add('active');
        self[key] = btn.dataset.val;
      });
    },

    init: function () {
      var self = this;
      self.renderSaved();
      self.initSeg('seg-grade', 'grade');
      self.initSeg('seg-diff', 'diff');
      document.getElementById('sb-gen-btn').addEventListener('click', function () { self.generate(); });
      document.getElementById('sb-copy-all').addEventListener('click', function () { self.copyAll(); });
      document.getElementById('sb-print-btn').addEventListener('click', function () { window.print(); });
      document.getElementById('sb-copy-saved').addEventListener('click', function () { self.copySaved(); });
      document.getElementById('ctrl-defs').addEventListener('change', function () { self.toggleDefs(); });
      if (typeof requestIdleCallback !== 'undefined') {
        requestIdleCallback(function () { self.generate(); });
      } else {
        setTimeout(function () { self.generate(); }, 100);
      }
    }
  };

  window.SBT = SBT;
  SBT.init();
}());
</script>
<!-- /SLOT:init -->
```

- [ ] **Step 10: Commit the tool source**

```bash
git add template-deploy/tools-src/spelling-bee-words.html
git commit -m "feat: add spelling-bee-words tool source (all slots)"
```

---

## Task 5: Build and verify

- [ ] **Step 1: Run the build**

```bash
cd "/Users/garrickdeetan/Documents/Random Word Generator Tool Site/template-deploy"
python3 build.py
```

Expected: no errors, `output/spelling-bee-words.html` present.

- [ ] **Step 2: Verify output**

```bash
wc -l "/Users/garrickdeetan/Documents/Random Word Generator Tool Site/template-deploy/output/spelling-bee-words.html"
```

Expected: 300+ lines.

```bash
grep -c "sb-gen-btn" "/Users/garrickdeetan/Documents/Random Word Generator Tool Site/template-deploy/output/spelling-bee-words.html"
grep -c "breadcrumb" "/Users/garrickdeetan/Documents/Random Word Generator Tool Site/template-deploy/output/spelling-bee-words.html"
grep -c "Spelling Bee Words" "/Users/garrickdeetan/Documents/Random Word Generator Tool Site/template-deploy/output/spelling-bee-words.html"
```

Expected: each returns a number > 0.

- [ ] **Step 3: Copy to deploy folder (rebuild all pages so nav updates)**

```bash
cd "/Users/garrickdeetan/Documents/Random Word Generator Tool Site/template-deploy"
python3 build.py
cp output/*.html ../wordineer-deploy/
```

- [ ] **Step 4: Start local server and verify manually**

```bash
cd "/Users/garrickdeetan/Documents/Random Word Generator Tool Site/wordineer-deploy"
python3 -m http.server 8080
```

Open `http://localhost:8080/spelling-bee-words.html` and check:

- [ ] Breadcrumbs: `Wordineer › Word Tools › Spelling Bee Words`
- [ ] Hero badge reads "1,000+ Words"
- [ ] Grade and Difficulty segmented buttons render and highlight on click
- [ ] Page auto-generates 20 words on load
- [ ] Each word card: word, origin badge (color-coded), syl count, pos, heart and copy icons, definition
- [ ] "Show definitions" toggle hides/shows all definitions
- [ ] Heart saves word to saved section; clicking again removes it
- [ ] Copy all copies word list to clipboard
- [ ] Print List opens print dialog; nav/controls hidden in print preview
- [ ] K-2 + Expert filter combination shows "No words match" gracefully
- [ ] Mega menu includes "Spelling Bee Words" link
- [ ] Footer includes "Spelling Bee Words" link

- [ ] **Step 5: Commit build output**

```bash
git add wordineer-deploy/spelling-bee-words.html wordineer-deploy/_redirects
git add template-deploy/output/spelling-bee-words.html
git commit -m "build: add spelling-bee-words to deploy folder"
```

---

## Final Verification

```bash
cd "/Users/garrickdeetan/Documents/Random Word Generator Tool Site"

# Dataset
python3 -c "import json; d=json.load(open('wordineer-deploy/data/spelling-bee-words.json')); print(len(d), 'words OK')"

# tools.json
python3 -c "import json; json.load(open('template-deploy/tools.json')); print('tools.json OK')"

# Build
cd template-deploy && python3 build.py && echo "Build OK"

# Key strings
grep -l "sb-gen-btn" output/spelling-bee-words.html && echo "JS wired OK"
grep -l "breadcrumb" output/spelling-bee-words.html && echo "Breadcrumb OK"
```

All five checks must pass before pushing to Cloudflare Pages.

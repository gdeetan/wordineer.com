# Stage 3 — Vocabulary cluster expansion

**Goal:** Round out the vocabulary cluster by building the "Coming soon" cards in `/word-tools/` Vocabulary & Learning section. Build on your spelling-bee strength to claim topical authority for English vocabulary tools.

**Why this stage third:**
- Your spelling bee K-7 pages are the strongest content on the site. They give you a credibility foothold in the education/learning niche.
- Education-niche backlinks are some of the easiest to attract organically (teacher blogs, homeschool sites, resource lists)
- Most "Coming soon" cards in this section target keywords with moderate volume and surprisingly low competition variants
- Cluster connection: SAT/ESL/vocabulary tools cross-link naturally with your existing strength

**Realistic outcome at maturity:** 15,000–25,000 visits/month across this cluster.

**Estimated build effort:** 30–50 hours across 4 weeks. The depth requirement is higher here than in Stage 1–2 because vocabulary content competes with established education sites.

---

## Progress tracker

| Week | Cluster | Status |
|---|---|---|
| Week 1 | SAT vocabulary (3 pages) | ✅ Done — deployed 2026-06-29 |
| Week 2 | Sight words (7 pages) | ✅ Done — deployed 2026-06-29 |
| Week 3 | Cool/aesthetic/beautiful/unique words | ⬜ Not started |
| Week 4 | Gen Z slang + ESL + writing tools | ⬜ Not started |

---

## Keyword landscape

### Tier 1 — Build first (highest ROI for the effort)

| Keyword | Est. Volume | Est. KD | Page | Status |
|---|---|---|---|---|
| sat vocabulary words | 20,000–40,000 | 45–55 | `/sat-vocabulary-words/` | ✅ Live |
| sat words list | 8,000–15,000 | 40–55 | `/sat-words-list/` | ✅ Live |
| hardest sat words | 2,000–4,000 | 30–40 | `/hardest-sat-words/` | ✅ Live |
| sight words | 100,000–200,000 | 55–70 | (head term) | ✅ Covered via generator |
| sight words generator | 4,000–8,000 | 25–35 | `/sight-words-generator/` | ✅ Live |
| sight words for kindergarten | 15,000–30,000 | 35–45 | `/sight-words-kindergarten/` | ✅ Live |
| sight words for 1st grade | 10,000–20,000 | 35–45 | `/sight-words-1st-grade/` | ✅ Live |
| dolch sight words | 15,000–30,000 | 40–50 | `/dolch-sight-words/` | ✅ Live |
| fry sight words | 10,000–20,000 | 40–50 | `/fry-sight-words/` | ✅ Live |
| cool words | 30,000–60,000 | 45–55 | `/cool-words/` | ⬜ Week 3 |
| weird words | 15,000–30,000 | 40–50 | (you have `/random-weird-words/`) | ⬜ Week 3 |
| aesthetic words | 8,000–15,000 | 35–45 | `/aesthetic-words/` | ⬜ Week 3 |
| beautiful words | 15,000–30,000 | 45–55 | `/beautiful-words/` | ⬜ Week 3 |
| gen z slang | 30,000–60,000 | 40–50 | `/gen-z-slang/` | ⬜ Week 4 |
| gen z words list | 8,000–15,000 | 30–40 | `/gen-z-words/` | ⬜ Week 4 |
| esl vocabulary | 6,000–12,000 | 35–45 | `/esl-vocabulary/` | ⬜ Week 4 |

### Tier 2 — Audience and topic variants

| Keyword | Est. Volume | Est. KD |
|---|---|---|
| sat words with definitions | 3,000–6,000 | 35–45 | → captured by `/sat-words-list/` ✅ |
| hardest sat words | 2,000–4,000 | 30–40 | → `/hardest-sat-words/` ✅ |
| sat vocabulary practice | 3,000–6,000 | 35–45 | → captured by `/sat-vocabulary-words/` ✅ |
| ged vocabulary words | 1,500–3,000 | 25–35 | ⬜ future |
| toefl vocabulary words | 4,000–8,000 | 35–45 | ⬜ future |
| ielts vocabulary words | 8,000–15,000 | 40–50 | ⬜ future |
| 100 most beautiful english words | 3,000–6,000 | 35–45 | ⬜ Week 3 |
| longest words in english | 8,000–15,000 | 45–55 | ⬜ future |
| unique words with deep meaning | 2,000–4,000 | 30–40 | ⬜ Week 3 |
| english words with greek roots | 1,500–3,000 | 30–40 | ⬜ future (SAT root filter covers this) |
| english words with latin roots | 1,500–3,000 | 30–40 | ⬜ future (SAT root filter covers this) |

### Tier 3 — Long-tail seed list (for after Tier 1-2)

- `/positive-words/` (positive vocabulary, popular with social media users)
- `/words-of-affirmation/` (relationship/love language angle)
- `/big-words-to-use-instead-of/` (writing improvement)
- `/words-to-replace-said/` (writing improvement, very popular with K-12)
- `/transition-words/` (essay writing)
- `/onomatopoeia-words/` (writing tool)
- `/oxymoron-list/` (interesting words)
- `/palindrome-list/` (interesting words)
- `/portmanteau-words/` (interesting words)

---

## Build order (week by week)

### ✅ Week 1 — SAT vocabulary (highest single-page value) — DONE

All three pages built, deployed to Cloudflare Pages, and added to sitemap.xml on 2026-06-29.

1. ✅ **`/sat-vocabulary-words/`** — Main SAT vocab tool (432 words, difficulty/root/POS filters, Practice Mode, audio, saved words)
2. ✅ **`/sat-words-list/`** — List-view variant with definitions visible by default; H1 covers both "sat words list" and "sat words with definitions"
3. ✅ **`/hardest-sat-words/`** — Filtered to hard-tier words only (~180 words)

Data file: `wordineer-deploy/data/sat-vocab-data.json` — 432 entries, fields: `{w, pos, d, ex, syl, root, root_note, diff}`

### ✅ Week 2 — Sight words (highest cumulative volume) — DONE

All seven pages built, deployed to Cloudflare Pages, and added to sitemap.xml on 2026-06-29. All pages share `wordineer-deploy/data/sight-words-data.json`.

1. ✅ **`/sight-words-generator/`** — Master tool with Dolch + Fry lists, filtered by list and grade
2. ✅ **`/sight-words-kindergarten/`** — Pre-filtered for Dolch Kindergarten words
3. ✅ **`/sight-words-1st-grade/`**
4. ✅ **`/sight-words-2nd-grade/`**
5. ✅ **`/sight-words-3rd-grade/`**
6. ✅ **`/dolch-sight-words/`** — Full Dolch list organized by Pre-K, K, 1st, 2nd, 3rd, Nouns
7. ✅ **`/fry-sight-words/`** — Fry words 1–300, organized by sets of 100

All sight words pages have:
- Grade-nav strip between tool and "Sight Word Tools" grid (links all 7 pages)
- Practice Mode (one-word-at-a-time drill)
- Audio pronunciation (Web Speech API)
- Saved words with localStorage
- Print view (colorful flashcard grid)
- Copy All button

### ⬜ Week 3 — Cool words / weird words / aesthetic words

The "interesting English words" cluster. Lower intent but high social-share volume.

1. **`/cool-words/`** — list-style page with 200+ interesting English words, each with definition, pronunciation, and short usage note. Filterable by category (sci-fi sounding, melodic, dark/edgy, vintage, etc.)
2. **`/aesthetic-words/`** — similar but slanted toward Instagram/Tumblr aesthetic culture (words like "petrichor", "sonder", "vellichor")
3. **`/beautiful-english-words/`** — overlap with aesthetic, slanted toward melodic/poetic
4. **`/unique-words-with-meaning/`** — overlap, slanted toward "untranslatable" words with deep meanings
5. **`/big-words-to-sound-smart/`** — different angle, more practical (replace "use" with "utilize", "show" with "demonstrate", etc.) — this is a high-CTR keyword

You already have `/random-weird-words/`. Cross-link these all together.

### ⬜ Week 4 — Gen Z slang + ESL + writing tools

1. **`/gen-z-slang/`** — definitions of "rizz", "skibidi", "delulu", "no cap", etc. This page needs ongoing updates (slang changes constantly) — set a reminder to refresh quarterly. Massive traffic potential but volatility too.

2. **`/gen-z-words-list/`** — alternative URL targeting the same intent

3. **`/esl-vocabulary/`** — practical English vocabulary for ESL learners. Sort by CEFR level (A1, A2, B1, B2, C1, C2) — 100-300 words per level. ESL bloggers and teachers link generously to good ESL resources.

4. **`/words-to-replace-said/`** — list of 100+ alternatives for "said" in dialogue writing. Popular with creative writing students and teachers.

5. **`/transition-words/`** — list of transition words for essays, organized by function (addition, contrast, causation, sequence, etc.). Popular with K-12 and college students.

6. **`/positive-words/`** — list of 200+ positive English words. Popular with copywriters, social media, mental health content.

---

## Future features & improvements

Ideas for improving existing Stage 3 pages after they are indexed and getting traffic. Grouped by cluster.

### Sight words pages (all 7)

**High value — build when pages hit 500+ visits/month:**

- **Spelling test mode** — hear the word, type it. Currently audio is listen-only; adding a text input + correct/incorrect feedback turns it into a full spelling drill. Technically: add `<input type="text">` in Practice Mode, compare against current word, show green/red feedback. No new data needed.

- **Progress tracker** — remember which words a child has "mastered" (seen 3× without saving as a trouble word). Store as a per-grade JSON blob in `localStorage`. Show a "Mastery" bar: "32/52 Kindergarten words mastered". Reset button. This is the single highest-engagement feature for the parent/teacher audience.

- **Print layouts for kids** — the current print view is a plain colored-grid browser stylesheet. Parents searching for sight words are overwhelmingly intending to print something for offline use with their child. This is the highest-leverage improvement for the sight words cluster because a great printout gets shared, pinned on classroom walls, photographed and posted to Facebook parenting groups, and linked from teacher blogs — all without any outreach. See full design spec below.

- **Word sentences mode** — in Practice Mode, show the word in a simple sentence instead of (or in addition to) isolated display. For kindergarten: "She **went** to the park." Requires adding `example_sentence` field to `sight-words-data.json` for each word.

- **Weekly challenge mode** — "This week's 10 words" based on the child's grade, randomized fresh each Monday, stored in `localStorage`. Creates a habit loop for return visits.

---

#### Print design spec for sight words (kid-friendly printouts)

The audience is parents printing at home on a standard inkjet, and teachers printing on a classroom laser printer. Both groups have zero tolerance for a printout that wastes paper, uses too much ink, or doesn't look intentional. The print layouts below are all pure CSS — no server, no PDF library needed.

**How to implement:** Add a `<select id="print-layout">` dropdown next to the existing Print button with the layout options below. When the user clicks Print, set a `data-print-layout` attribute on `<body>`, then use `@media print` CSS to switch layouts. No JS needed for the actual printing — just toggling a body attribute.

```html
<!-- Add next to existing Print button -->
<select id="print-layout" class="act-btn" style="padding:6px 10px;">
  <option value="flashcards">Flashcards (cut-out)</option>
  <option value="list">Word list (fridge)</option>
  <option value="bingo">Bingo card</option>
  <option value="trace">Handwriting practice</option>
  <option value="checklist">Progress checklist</option>
</select>
<button class="act-btn" id="sw-print-btn">Print</button>
```

---

**Layout 1: Flashcard sheet** (most requested by parents and teachers)

8 cards per page (2×4 grid), landscape or portrait. Each card: word in large bold type (36–48pt), grade badge in corner (e.g. "Dolch K"), dashed cut border. On the back side (second page, same 2×4 grid), blank boxes — parent writes a drawing or definition. No background colors — saves ink.

```css
@media print {
  body[data-print-layout="flashcards"] .sw-list {
    display: grid !important;
    grid-template-columns: repeat(2, 1fr);
    gap: 0;
    page-break-inside: avoid;
  }
  body[data-print-layout="flashcards"] .word-item {
    height: 130px;
    border: 2px dashed #aaa !important;
    border-radius: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    gap: 6px;
    break-inside: avoid;
  }
  body[data-print-layout="flashcards"] .word-text {
    font-size: 36pt !important;
    font-weight: 700;
  }
  body[data-print-layout="flashcards"] .word-badge {
    font-size: 9pt;
    border: 1px solid #ccc;
    padding: 2px 6px;
    border-radius: 4px;
  }
  /* Cut instructions at top */
  body[data-print-layout="flashcards"]::before {
    content: "✂ Cut along dashed lines. Fold in half for double-sided flashcards.";
    display: block;
    font-size: 9pt;
    color: #777;
    margin-bottom: 8px;
  }
}
```

---

**Layout 2: Word list / fridge sheet**

Single-column list, large font, designed to stick on the fridge or a child's bedroom door. Each word on its own line with a small checkbox on the left (child checks off words they can read). Good for a "10 words this week" takeaway.

```css
@media print {
  body[data-print-layout="list"] .sw-list {
    display: block !important;
    columns: 2;
    column-gap: 40px;
  }
  body[data-print-layout="list"] .word-item {
    display: flex;
    align-items: center;
    gap: 10px;
    border-bottom: 1px solid #eee !important;
    padding: 8px 0 !important;
    break-inside: avoid;
  }
  /* Checkbox circle */
  body[data-print-layout="list"] .word-item::before {
    content: "";
    width: 18px;
    height: 18px;
    border: 2px solid #999;
    border-radius: 50%;
    flex-shrink: 0;
    display: block;
  }
  body[data-print-layout="list"] .word-text {
    font-size: 20pt !important;
  }
}
```

---

**Layout 3: Bingo card**

Randomly arrange 24 of the current words into a 5×5 bingo grid (center = FREE space). Parent calls words aloud, child marks them. Generate a different random card each time Print is clicked (JS randomizes before print, no state needed after).

This is the highest-share print format — teachers photograph their class playing bingo and post to teacher Facebook groups and Pinterest. A single viral bingo card image has driven hundreds of backlinks for other ed sites.

Implementation: on print-button click with bingo layout selected, run a Fisher-Yates shuffle of the current word list, take 24, render into a hidden `<table class="bingo-card">` (not inside `.sw-list`), then `window.print()`. The bingo table uses `display:none` normally and `display:table` in `@media print`.

```css
@media print {
  body[data-print-layout="bingo"] .sw-list { display: none !important; }
  body[data-print-layout="bingo"] .bingo-card {
    display: table !important;
    width: 100%;
    border-collapse: collapse;
    table-layout: fixed;
  }
  body[data-print-layout="bingo"] .bingo-card td {
    border: 2px solid #333;
    text-align: center;
    vertical-align: middle;
    height: 80px;
    font-size: 18pt;
    font-weight: 700;
  }
  body[data-print-layout="bingo"] .bingo-free {
    background: #f0f0f0;
    font-size: 12pt;
    font-weight: 700;
    color: #555;
  }
  /* Column headers B-I-N-G-O */
  body[data-print-layout="bingo"] .bingo-header td {
    background: #3C3489;
    color: white;
    font-size: 24pt;
    font-weight: 900;
    height: 60px;
  }
}
```

---

**Layout 4: Handwriting practice sheet**

Each word displayed at the top of a small box, then 3–4 ruled lines below it for the child to practice writing the word. Compact: 6 words per row, 3 rows per page = 18 words per sheet. Very popular with K-2 teachers — "trace and write" is a core classroom activity.

```css
@media print {
  body[data-print-layout="trace"] .sw-list {
    display: grid !important;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
  }
  body[data-print-layout="trace"] .word-item {
    border: 1px solid #ccc !important;
    border-radius: 6px;
    padding: 8px !important;
    display: flex;
    flex-direction: column;
    gap: 4px;
    break-inside: avoid;
    min-height: 120px;
  }
  body[data-print-layout="trace"] .word-text {
    font-size: 18pt !important;
    font-weight: 700;
    border-bottom: 1px solid #ddd;
    padding-bottom: 4px;
    margin-bottom: 4px;
  }
  /* Practice lines */
  body[data-print-layout="trace"] .word-item::after {
    content: "";
    flex: 1;
    background-image: repeating-linear-gradient(
      to bottom,
      transparent,
      transparent 22px,
      #ccc 22px,
      #ccc 23px
    );
    display: block;
  }
}
```

---

**Layout 5: Progress checklist**

All words in the selected group (not just the current randomly-generated set), sorted alphabetically. Two columns. Each word has three empty star/circle checkboxes beside it — representing 3 sessions of correct recognition before it's "mastered." Simple, printer-friendly, designed to live on the fridge for a week.

```css
@media print {
  /* Render full word list (all in group, not just current) via a hidden #full-list element */
  body[data-print-layout="checklist"] .sw-list { display: none !important; }
  body[data-print-layout="checklist"] #print-checklist {
    display: grid !important;
    grid-template-columns: 1fr 1fr;
    column-gap: 24px;
    font-size: 13pt;
  }
  body[data-print-layout="checklist"] #print-checklist li {
    display: flex;
    align-items: center;
    gap: 8px;
    border-bottom: 1px solid #eee;
    padding: 5px 0;
  }
  /* Three practice checkboxes */
  body[data-print-layout="checklist"] #print-checklist li::after {
    content: "○ ○ ○";
    font-size: 14pt;
    color: #aaa;
    margin-left: auto;
    letter-spacing: 4px;
  }
}
```

---

**General print rules for all layouts (add to existing `@media print`):**

```css
@media print {
  /* Always hide these regardless of layout */
  header, nav, .breadcrumb, .hero, .ctrl, .sw-top-bar, .saved-section,
  .practice-panel, .explainer, .faq, .who, footer, .ad, [class*="ad-"],
  .more-tools, .content-wrap, .grade-nav-bar, #print-layout,
  #sw-print-btn, #sw-gen-btn, #sw-reset-btn { display: none !important; }

  /* Print header — school-friendly branding, not a logo ad */
  .print-header {
    display: block !important;
    font-size: 10pt;
    color: #666;
    border-bottom: 1px solid #ccc;
    padding-bottom: 6px;
    margin-bottom: 12px;
  }
  .print-header strong { color: #3C3489; }

  @page {
    margin: 1.2cm;
    size: letter portrait; /* or landscape for flashcard layout */
  }
}
```

**Print header HTML** (add once to SLOT:tool, hidden normally, shown on print):
```html
<div class="print-header" style="display:none">
  <strong>Wordineer.com</strong> · Free sight word tools for parents and teachers ·
  <span id="print-label">Sight Words</span>
</div>
```

---

**Claude Code prompt — implement kid-friendly print layouts**

```
# Task: Add kid-friendly print layouts to all sight words pages

Parent and teacher users of /sight-words-kindergarten/, /sight-words-1st-grade/,
/sight-words-2nd-grade/, /sight-words-3rd-grade/, /dolch-sight-words/, /fry-sight-words/,
and /sight-words-generator/ need printout-quality output. The current print stylesheet
outputs a basic colored grid — replace it with a layout selector giving 5 options.

## Files to modify

All 7 tools-src sight words files:
- template-deploy/tools-src/sight-words-generator.html
- template-deploy/tools-src/sight-words-kindergarten.html
- template-deploy/tools-src/sight-words-1st-grade.html
- template-deploy/tools-src/sight-words-2nd-grade.html
- template-deploy/tools-src/sight-words-3rd-grade.html
- template-deploy/tools-src/dolch-sight-words.html
- template-deploy/tools-src/fry-sight-words.html

## What to build

### 1. Print layout selector

Replace the existing `<button id="sw-print-btn">Print</button>` with:

```html
<div class="print-row">
  <select id="print-layout" class="act-btn">
    <option value="flashcards">Flashcards</option>
    <option value="list">Word list</option>
    <option value="bingo">Bingo card</option>
    <option value="trace">Handwriting practice</option>
    <option value="checklist">Progress checklist</option>
  </select>
  <button class="act-btn" id="sw-print-btn">Print</button>
</div>
```

JS: on print-button click, set `document.body.dataset.printLayout = document.getElementById('print-layout').value` then `window.print()`. For the bingo layout, also call `buildBingoCard()` first (see below).

### 2. Five @media print CSS layouts

Implement all 5 layouts as described in the growth plan print spec. Key requirements:
- Flashcards: 2-column dashed-border grid, 36pt word, no fill color (ink-saving)
- Word list: 2-column checklist with circle checkboxes, 20pt word
- Bingo: 5×5 table with BINGO header row, center FREE space, 18pt words
- Handwriting practice: 3-column grid, ruled lines below each word
- Progress checklist: full-group word list (all words, not just current set), 3 circle checkboxes per word

### 3. Bingo card JS

```js
buildBingoCard: function () {
  var pool = /* all words in current filter group */;
  // shuffle pool
  for (var i = pool.length-1; i>0; i--) {
    var j = Math.floor(Math.random()*(i+1));
    var tmp = pool[i]; pool[i]=pool[j]; pool[j]=tmp;
  }
  var words = pool.slice(0, 24).map(function(w){ return w.word; });
  // build 5x5 table, insert FREE at index 12 (center)
  words.splice(12, 0, 'FREE');
  var tbl = document.getElementById('sw-bingo-card');
  if (!tbl) {
    tbl = document.createElement('table');
    tbl.id = 'sw-bingo-card';
    tbl.className = 'bingo-card';
    document.querySelector('.tool-card').appendChild(tbl);
  }
  var html = '<tr class="bingo-header"><td>B</td><td>I</td><td>N</td><td>G</td><td>O</td></tr>';
  for (var r=0; r<5; r++) {
    html += '<tr>';
    for (var c=0; c<5; c++) {
      var idx = r*5+c;
      var cls = idx===12 ? ' class="bingo-free"' : '';
      html += '<td'+cls+'>'+words[idx]+'</td>';
    }
    html += '</tr>';
  }
  tbl.innerHTML = html;
}
```

### 4. Print header

Add to SLOT:tool in each file (inside `.tool-card`, before `.tool-split`):
```html
<div class="print-header">
  <strong>Wordineer.com</strong> · Free sight word tools for parents and teachers ·
  <span id="print-label"><!-- set via JS based on grade/list --></span>
</div>
```

JS sets `document.getElementById('print-label').textContent = 'Kindergarten Sight Words'` (or appropriate label) in `init()`.

### 5. Ink-saving rule

Add to the general `@media print` block:
```css
* { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body[data-print-layout="flashcards"] * { color: #000 !important; background: #fff !important; }
body[data-print-layout="list"] * { color: #000 !important; background: #fff !important; }
body[data-print-layout="trace"] * { color: #000 !important; background: #fff !important; }
```
Flashcards, lists, and trace sheets should use zero color ink. Bingo and checklist can keep minimal color on the header.

## Testing checklist

For each layout, open browser print preview and verify:
- [ ] All navigation, hero, ads, footer hidden
- [ ] Print header visible with correct grade label
- [ ] Flashcards: 2 per row, dashed borders, no background fill
- [ ] Word list: 2 columns, circle checkboxes visible, 20pt+ font
- [ ] Bingo: 5×5 grid fills the page, FREE at center, BINGO header in brand color
- [ ] Handwriting: 3 per row, ruled lines visible below each word
- [ ] Checklist: full grade group (not just current 15), 3 circles per word

## Build and deploy

1. Edit all 7 tools-src files
2. Run `cd template-deploy && python3 build.py`
3. Copy all 7 output files to wordineer-deploy/
4. Test print preview locally
5. Commit: "feat: add kid-friendly print layouts to sight words pages (flashcards, bingo, handwriting, checklist)"
```

**Medium value — consider after Week 3-4:**

- **2nd/3rd grade pages** — currently only Dolch. Add Fry group filters on these pages so a parent can see both lists side by side.
- **Sight words for 4th/5th grade** — not a Dolch category but teachers frequently search for it. Source from Fry 301-500. Adds 2 more grade pages.
- **Pre-K page** — separate `/sight-words-pre-k/` targeting Dolch Pre-K group directly (parents of 4-5 year olds search for this).

---

### SAT vocabulary pages

**High value:**

- **Mock quiz mode** — for `/sat-vocabulary-words/`: generate 10 words, show 4 answer choices (1 correct definition + 3 distractors pulled from other words). Show score at end. This is the most-requested feature on SAT prep tools and would drive repeat visits. Technically complex but high impact.

- **Root word explorer** — click on a root badge (e.g. "Latin: `bene`") to see all other words in the data file that share that root. Currently the root filter shows words with the same root language but not the same root word. Adding a root-family grouping would be genuinely useful for systematic study.

- **Expand word count to 1,000** — `sat-vocab-data.json` currently has 432 entries. Expanding to 800–1,000 significantly improves the "SAT vocabulary words" head term ranking. The data schema already supports it — just need more entries. Batch-add 200 words at a time in separate prompts.

- **Sentence context questions** — for Practice Mode: show example sentence with the word blanked out, user picks which word fits. "The professor's ___ lecture baffled even his graduate students." (choices: perspicacious / verbose / laconic / benign). This is the actual SAT "Words in Context" format — matching it makes the page more directly useful for exam prep.

**Medium value:**

- **Study schedule generator** — user inputs their SAT date, tool generates a week-by-week plan (how many words per day, which difficulty tier to focus on each week). Stores in `localStorage`. Links back to tool for each day's session.
- **Download as CSV/Anki deck** — power users (tutors especially) want to import word lists into their own apps. Add a Download button that exports the current filtered list as `word,definition,example` CSV.

---

### Cool/aesthetic/beautiful words (Week 3 — not built yet)

**Build these features in from the start:**

- **Category filter** — these pages live or die by filterable categories. For cool words: Sci-fi/space, Nature, Ancient/archaic, Melodic, Dark/gothic, Funny. Don't build without categories.
- **Social share per word** — "Share this word" button that copies `"petrichor: the smell of rain on dry earth — wordineer.com/aesthetic-words/"` to clipboard, or opens a Twitter/X pre-filled tweet. These pages get shared widely if you make it easy.
- **Word of the day integration** — cross-link cool/aesthetic words into `/word-of-the-day/`. If WOTD picks from this data, it creates a return-visit reason.
- **Embed widget** — a 400×200 iframe embed for bloggers and teachers to display a random aesthetic/cool word on their site. Backlink magnet.

---

### Gen Z slang (Week 4 — not built yet)

**Build these features in from the start:**

- **"Old vs. current" freshness signal** — show when each term was added/updated. Gen Z slang has a half-life. Showing dates ("added Jan 2025") signals to Google and users that the content is maintained.
- **Trend badge** — 🔥 Trending / ✅ Still used / 📦 Retired. Manual curation but extremely useful for users. Refreshed quarterly.
- **Submit a term form** — simple form (word + definition + example) that goes to your email. Creates community engagement and surfaces new slang you haven't heard yet.
- **Quarterly refresh reminder** — add a calendar reminder to review and update this page every 3 months (Jan, Apr, Jul, Oct). Gen Z slang decays fast.

---

## Claude Code prompt — Week 3: Build the cool words cluster

```
# Task: Build /cool-words/, /aesthetic-words/, /beautiful-english-words/ — Pattern B list pages

You are building three list/reference pages for the "interesting English words" cluster. These are Pattern B pages (list-first, less tool-heavy) that target high-volume social-discovery queries.

## Architecture

All three pages share a new data file: `wordineer-deploy/data/interesting-words-data.json`

Each entry:
{
  "word": "petrichor",
  "pronunciation": "PET-ri-kor",
  "type": "noun",
  "definition": "The pleasant, earthy smell produced when rain falls on dry ground.",
  "note": "Coined in 1964 by Australian scientists from Greek 'petra' (stone) + 'ichor' (the fluid in the veins of the gods).",
  "categories": ["aesthetic", "nature", "beautiful"],
  "origin": "Greek"
}

Categories: `cool`, `aesthetic`, `beautiful`, `unique`, `weird`, `funny`, `dark`, `nature`, `science`, `vintage`
Target: 300 words minimum, each word can appear in multiple category arrays.

## Pages to build

### 1. /cool-words/
- H1: "Cool Words" 
- Target: 30,000–60,000/mo, KD 45–55
- Filter by category, origin; search bar
- Static HTML word list (for SEO) + JS filtering on top
- CONFIG more_tools_key: "vocabulary_tools"

### 2. /aesthetic-words/
- H1: "Aesthetic Words"
- Target: 8,000–15,000/mo, KD 35–45
- Same tool, pre-filtered to `categories` includes "aesthetic"
- Different intro/explainer angle: Instagram aesthetic culture, mood words, poetic words

### 3. /beautiful-english-words/
- H1: "Beautiful English Words"  
- Target: 15,000–30,000/mo, KD 45–55
- Pre-filtered to `categories` includes "beautiful"
- Explainer: what makes a word sound beautiful (phonaesthetics, resonance, meaning)

## Tool pattern (Pattern B)

No "Generate" button — the full list is displayed by default, JS filtering on top:
- Search bar (instant filter on word/definition)
- Category pills (multi-select, default all)
- Origin filter (All / Greek / Latin / French / Anglo-Saxon / etc.)
- Count display: "Showing 287 words"
- Copy Word button per word
- Social share button per word (copies "word: definition — wordineer.com/url" to clipboard)
- Print view (compact list, no sidebar)

Static HTML fallback: render all words server-side in a `<dl>` list so Google sees them without JS.

## Requirements

Each page must have:
- 300-word intro unique to the page angle
- 1,500+ word explainer with multiple H2s
- 6 FAQ questions
- 4 "who uses this" cards
- Internal links to: /dolch-sight-words/, /sat-vocabulary-words/, /word-of-the-day/, /random-weird-words/, sibling cluster pages
- FAQPage + WebApplication + BreadcrumbList schema
- Canonical, OG, Twitter Card meta

Build /cool-words/ first. Once that is working, /aesthetic-words/ and /beautiful-english-words/ can reuse the same template with minimal changes (different H1, intro, pre-filter value, and explainer content).

Do not deploy. Deliver: tools-src files, data JSON, and a summary of word count and any gaps.
```

---

## Claude Code prompt — Week 4: Build the Gen Z slang + ESL + writing tools

```
# Task: Build /gen-z-slang/, /esl-vocabulary/, /words-to-replace-said/, /transition-words/

Four pages. Build in this order: gen-z-slang first (highest traffic ceiling), then esl-vocabulary, then writing tools.

## 1. /gen-z-slang/

Data file: `wordineer-deploy/data/gen-z-slang-data.json`
Entry format:
{
  "term": "rizz",
  "definition": "Natural charm and charisma, especially the ability to attract romantic interest effortlessly.",
  "example": "He walked in and the whole room noticed — that guy has serious rizz.",
  "status": "current",
  "added": "2024-01",
  "categories": ["social", "appearance"]
}

Status: "trending" | "current" | "established" | "fading" | "retired"

Include 100+ terms. Key ones to include: rizz, slay, no cap, fr fr, bussin, lowkey, highkey, hits different, understood the assignment, main character energy, delulu, era (as in "I'm in my healing era"), situationship, rent free, vibe check, it's giving, NPC, snatched, ate and left no crumbs, based, mid, sus, ratio, touch grass, go off, understood the assignment, unalive (content warning, define carefully), W/L (win/loss), deadass, cap/no cap.

Page requirements:
- Trend status badge on each term (🔥 Trending / ✅ Current / 📦 Fading)
- Filter by status and category
- "Last updated" date prominently displayed
- H1: "Gen Z Slang — Complete Dictionary with Definitions and Examples"
- Explainer covers: origin of Gen Z slang, how it spreads (TikTok), why it changes so fast, how older generations use it wrong, a brief history of youth slang

## 2. /esl-vocabulary/

Data file: `wordineer-deploy/data/esl-vocab-data.json`
Entry format:
{
  "word": "apologize",
  "cefr": "B1",
  "definition": "To say sorry for something you did wrong.",
  "example": "I apologize for being late to the meeting.",
  "topic": "social",
  "pos": "verb"
}

CEFR levels: A1, A2, B1, B2 (focus on A1–B2 for this page; C1–C2 is too academic for the tool audience)
Include 400+ words across all levels.
Filter by CEFR level, topic category (greetings/social, work, shopping, travel, time/dates, emotions, etc.)

Page requirements:
- CEFR level explainer (what each level means, how long to reach it)
- Internal links to SAT vocabulary (for advanced learners)
- "Who uses this" card for: international students, immigrants/newcomers, language teachers, business English learners

## 3. /words-to-replace-said/

Data file: inline in the HTML (only ~120 words, no need for JSON)
Structure: words grouped by tone/intensity — neutral (replied, responded, stated), positive (exclaimed, cheered, enthused), questioning (asked, wondered, inquired), forceful (declared, insisted, demanded), quiet (whispered, murmured, breathed), etc.

Page: Pattern B list page. Static HTML table or `<dl>`. Filter by tone. Print-friendly.
Audience: K-12 students, creative writers, English teachers (huge link bait for teacher blogs)

## 4. /transition-words/

Data file: inline in HTML (~80 transition words/phrases)
Structure: grouped by function — Addition (also, furthermore, moreover), Contrast (however, nevertheless, on the other hand), Causation (therefore, consequently, as a result), Sequence (first, then, finally, subsequently), Emphasis (indeed, in fact, above all), Example (for instance, such as, namely), Conclusion (in conclusion, to summarize, overall)

Page: Pattern B. Static table. Filter by function. Extremely popular with students writing essays — high share/bookmark rate.

## Requirements for all four pages

- FAQPage + WebApplication + BreadcrumbList schema
- Canonical, OG, Twitter Card
- 300-word unique intro per page
- 1,200+ word explainer per page
- 6 FAQ questions per page
- Internal links to sibling vocabulary pages
- more_tools_key: "vocabulary_tools"

Do not deploy. Deliver all tools-src files, data JSONs, and a word-count summary.
```

---

## Template approach

These pages split into two patterns:

### Pattern A: Tool pages (like SAT vocab, sight words generator)
Use the same template family as your existing spelling bee pages — they're already excellent. Clone the 5th-grade spelling bee page and modify:
- Source data file (sight-words-data.json instead of spelling-bee-5th-data.json)
- Filters and audio/practice mode reused as-is
- All the great explainer + FAQ + use-cases content patterns reused
- New H1, intro, and topic-specific content

### Pattern B: List/reference pages (like cool words, aesthetic words, transition words)
Different pattern — less of a "tool", more of a "resource". Structure:
- H1 + intro
- A filter/search bar above a categorized list
- The actual list rendered server-side as HTML (long, scannable, copy-friendly)
- Each word/phrase as a `<dl>` term-definition pair OR a card
- Print/save buttons
- Related lists linked at bottom

Pattern B pages are easier to build but need a lot more written content. Each word needs a real definition and a usage note that isn't copied from a dictionary (Google detects dictionary-scraped content).

---

## What each page must have (consistent with Stages 1-2)

1. Self-referencing canonical
2. Unique H1 matching target query
3. Unique 300-500 word intro
4. Static content rendered server-side (the words/list visible in raw HTML)
5. Unique FAQ block (4-6 questions) with FAQ schema
6. Internal links to 4-6 sibling vocabulary pages
7. Self-contained explainer (500-800 words for high-volume head terms like SAT vocab)
8. Breadcrumb schema
9. Open Graph + Twitter Card meta

**Additional for this cluster:** consider adding `Course` or `EducationalAlignment` schema where appropriate. SAT prep and grade-specific content can target rich result categories.

---

## Sourcing the vocabulary data

This is the hardest part of Stage 3. You need:

| Data | Source | Quality work needed |
|---|---|---|
| SAT words ✅ | Public list available on College Board (historical), Magoosh, etc. The actual "list" no longer officially exists — compile from contemporary SAT prep books and your own discretion | High — every word needs a real definition, example sentence, etymology, difficulty rating |
| Sight words ✅ | Dolch (public domain) and Fry (public domain) lists are widely available and not copyrightable. Use them. | Low — well-defined sources |
| Cool/weird/aesthetic words | Original curation from your existing word database + research. Reddit r/etymology, r/words, r/etymologymaps for inspiration | High — each needs definition + usage note + why it's interesting |
| Gen Z slang | Original research from social media, Urban Dictionary (use as reference only, don't copy), TikTok | High and ongoing — quarterly refresh required |
| ESL vocabulary by CEFR | English Profile (free CEFR-tagged word lists from Cambridge) | Medium — re-write definitions in plain English |

**Critical:** Definitions must be written in your own words. Don't paste Merriam-Webster or Oxford definitions — that's both a copyright issue and a duplicate-content issue. Write definitions in plain, simple English at the appropriate reading level.

---

## Claude Code prompt — build the SAT Vocabulary Words tool (COMPLETED ✅)

This prompt was executed in full on 2026-06-29. Delivered:
- `/sat-vocabulary-words/` — 432-word interactive tool
- `/sat-words-list/` — list-view variant
- `/hardest-sat-words/` — hard-tier filtered page
- `sat-vocab-data.json` — 432 entries with `{w, pos, d, ex, syl, root, root_note, diff}`

<details>
<summary>Original build prompt (archived)</summary>

```
# Task: Build /sat-vocabulary-words.html — modeled on the 5th-grade spelling bee page

You are building a comprehensive SAT vocabulary tool that should match the depth of /spelling-bee-words-5th-grade/. This is a Tier 1 page expected to drive significant traffic over time.

## Step 1: Read these first

1. https://wordineer.com/spelling-bee-words-5th-grade/ — fetch. This is your template for depth and quality. The new page should match its structure and explainer depth.
2. /random-word-generator.html (in project) — for CONFIG/SLOT/init patterns.
3. /global.css, /head.html, /nav.html, /footer.html.

## Step 2: CONFIG

<!-- CONFIG
{
  "url": "/sat-vocabulary-words.html",
  "output": "sat-vocabulary-words.html"
}
-->

## Step 3: Meta block

- <title>: SAT Vocabulary Words — 300+ With Definitions, Audio, Practice Mode | Wordineer
- <meta name="description">: 300+ curated SAT vocabulary words with definitions, audio pronunciation, example sentences, and root-word filtering. Practice mode, no login required.
- <link rel="canonical" href="https://wordineer.com/sat-vocabulary-words/">
- Open Graph, BreadcrumbList, FAQPage, and SoftwareApplication schema as in /spelling-bee-words-5th-grade/

## Step 4: Page structure

Mirror the 5th-grade spelling bee page exactly:

1. Breadcrumb: Wordineer › Word Tools › SAT Vocabulary
2. Eyebrow line: "300+ Words · Audio · Practice Mode · Free"
3. H1: SAT Vocabulary Words
4. Subtitle paragraph (1-2 sentences)
5. The tool (controls + results)
6. "More vocabulary tools" cross-link grid (link to spelling bee, sight words, ESL vocab, etc.)
7. Long explainer (2,000+ words, multiple H2s)
8. FAQ
9. Who-uses-it
10. Footer

## Step 5: The tool

Controls panel:
- Number of words: 1-50
- Difficulty: All / Easy (commonly seen) / Medium / Hard
- Root: All / Latin / Greek / French / Anglo-Saxon / Other
- Word type: All / Nouns / Verbs / Adjectives / Adverbs
- Show definition: toggle
- Show example sentence: toggle
- Generate button + space-to-regenerate hint

Results panel:
- Each word: word, part of speech, definition, example sentence (SAT-style context), root badge, difficulty badge
- Audio speaker icon for each word (uses browser TTS via existing tool-engine pattern)
- Heart icon to save
- Practice Mode button (collapses list, shows one at a time, user inputs/recalls definition)
- Copy all / Print list

## Step 6: Data file

Create /sat-vocab-data.json with 300+ curated SAT-level words. Each entry:

{
  "word": "perspicacious",
  "pos": "adjective",
  "definition": "having a ready insight into things; shrewd.",
  "example": "Her perspicacious analysis of the legal brief impressed the senior partners.",
  "syllables": "per-spi-CA-cious",
  "root": "Latin",
  "root_note": "from perspicere (to look through, see clearly)",
  "difficulty": "hard"
}

Curate from established SAT word lists but rewrite every definition in your own clear, plain language — do not copy dictionary definitions verbatim. Each example sentence must be original. Cover a balance of difficulty tiers (~100 easy, 100 medium, 100 hard) and root languages.

This is the highest-effort part of this task. If 300 words is too many in one pass, generate 100 to start and Claude Code can flag that more are needed. Do not generate fewer than 100.

## Step 7: Explainer content (1,500-2,500 words)

H2s (mirror the 5th-grade spelling bee depth):

**H2: What are SAT vocabulary words?**
~250 words. Explain the modern SAT (no dedicated vocab section since 2016, but "Words in Context" questions on the Reading section still test sophisticated vocabulary). Mention that vocabulary helps with both Reading comprehension and the Writing section.

**H2: Why root words matter on the SAT**
~300 words. Latin and Greek roots account for the majority of academic English vocabulary. Decoding strategies. Specific roots that appear repeatedly (-ben, mal-, -loqu-, -dict-, gen-, etc.). How to use the Root filter in this tool to study systematically.

**H2: How this tool works**
~200 words. Numbered list mirroring the spelling bee page's "How to use this tool" — set count, set difficulty, set root, generate, save trouble words, run practice mode, repeat.

**H2: A 6-week SAT vocabulary study schedule**
~400 words. Concrete week-by-week plan. Week 1: easy + medium, build daily habit. Week 2: focus on Latin roots only. Week 3: Greek roots. Week 4: French/other. Week 5: hard difficulty drill. Week 6: saved-words review. Mention spaced repetition principles.

**H2: How SAT vocabulary is actually tested**
~300 words. The "Words in Context" question format with a real example structure. Why understanding nuance and connotation matters more than just knowing the dictionary meaning.

**H2: Sample words by root group**
~200 words. List 5-8 example words for each of the major root languages with their family relationships. Shows readers how learning one root unlocks many words.

## Step 8: FAQ (6-8 questions)

Cover: Is this updated for the latest SAT? How many words should I study? Easy vs hard — where do I start? How do I use Practice Mode? Can I hear the words? What about the digital SAT? How is this different from Quizlet/Magoosh?

## Step 9: Who-uses-it (4 cards)

- High school students preparing for the SAT
- Tutors building practice lists
- Parents helping with prep at home
- ESL students preparing for the SAT (note: separate ESL Vocabulary tool exists for general English learning)

## Step 10: Internal linking (in prose)

Link in explainer body:
- /spelling-bee-words-7th-grade/ (for younger advanced students)
- /random-adjective-generator/, /random-verb-generator/ (for usage practice)
- /esl-vocabulary/ (when discussing ESL learners)
- /word-of-the-day/ (daily habit)
- /word-tools/ (hub)

## Step 11: Deliverables

1. /sat-vocabulary-words.html
2. /sat-words-list.html (list view; H1/intro covers both "sat words list" and "sat words with definitions"; no separate /sat-words-with-definitions/ page)
3. /sat-vocab-data.json (with at least 100 words, ideally 300)
4. Any additions to tool-engine.js or new vocab-engine.js
4. CSS additions (commented)
5. Update /word-tools/ hub: mark SAT Vocabulary as live, link the card
6. Add to sitemap.xml
7. Summary including: word count in JSON, any sections that need more content, any deviations from spec

Do not deploy.
```

</details>

---

## Success metrics for Stage 3

- [x] **10+ pages live in the vocabulary cluster** — 10 live as of 2026-06-29 (3 SAT + 7 sight words)
- [ ] All pages indexed within 2 weeks — *check Google Search Console by 2026-07-13*
- [ ] First backlink from an education site within 60 days — *check by 2026-08-28*
- [ ] At least 1 page in top 20 for its target query within 90 days — *check by 2026-09-27*
- [ ] Sight words pages collectively driving 1,000+ visits/month within 6 months — *check by 2026-12-29*

---

## Strategic notes on this cluster

1. **Vocabulary content has the longest payback curve on the site.** Google rewards comprehensive, authoritative content here. A SAT page that's 80% as good as the top ranker won't break into the top 10 — but if it's 120% as good (more words, better UX, audio, practice mode), it eventually wins. Be patient.

2. **The education niche is link-rich.** A great sight-words page gets linked from teacher blogs, homeschool resource lists, and PTA pages without you doing outreach. A great party-games page does not. This is why building this cluster well is the foundation for organic backlink growth.

3. **The Gen Z slang page will fluctuate dramatically.** Search demand for specific slang terms rises and falls in weeks, not months. Build the page, but don't be alarmed when traffic for specific terms tanks — that's the nature of slang. The page itself stays valuable as a frequently-updated reference.

4. **Don't try to compete head-on with Magoosh, Khan Academy, or Quizlet for SAT prep.** Their authority is too high. Win on tool quality and specific long-tail queries: "SAT words with Latin roots," "hardest SAT words," "sample SAT vocabulary questions," etc.

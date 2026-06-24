# Words That Start With — Landing Page Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a `/words-that-start-with/` hub page with A–Z letter cards (each linking to `/words-that-start-with/[letter]/`), add a cross-link paragraph in `word-tools.html`, register the page in `tools.json`, and wire up clean-URL redirects.

**Architecture:** New `type: content` source file assembled by the existing `build.py` pipeline. The A–Z letter cards reuse the site's `.tool-item` / `.tools-grid` pattern. Individual letter pages (`/words-that-start-with/a/` etc.) are out of scope — cards will link to them as stubs.

**Tech Stack:** Static HTML, existing build.py pipeline, Cloudflare Pages `_redirects`

---

## File Map

| Action | Path |
|---|---|
| Create | `template-deploy/tools-src/words-that-start-with.html` |
| Modify | `template-deploy/tools.json` |
| Modify | `template-deploy/tools-src/word-tools.html` |
| Modify | `wordineer-deploy/_redirects` |
| Build output (copy after build) | `wordineer-deploy/words-that-start-with.html` |
| Also rebuild/copy (word-tools modified) | `wordineer-deploy/word-tools.html` |

---

## Task 1: Create `words-that-start-with.html` source file

**Files:**
- Create: `template-deploy/tools-src/words-that-start-with.html`

### Color palette for letter cards (cycling A→Z, index mod 5)

| Index mod 5 | bg | stroke |
|---|---|---|
| 0 | `#EEEDFE` | `#534AB7` |
| 1 | `#EAF0F6` | `#2F4F6F` |
| 2 | `#E1F5EE` | `#1D9E75` |
| 3 | `#FEF3E8` | `#C7435B` |
| 4 | `#EEF6E8` | `#2F6B1F` |

- [ ] **Step 1: Create the file with the full source content**

Create `template-deploy/tools-src/words-that-start-with.html` with this exact content:

```html
<!-- CONFIG
{
  "type": "content",
  "url": "/words-that-start-with/",
  "output": "words-that-start-with.html"
}
-->

<!-- SLOT:meta -->
<title>Words That Start With Every Letter | A to Z Word Lists | Wordineer</title>
<meta name="description" content="Browse words that start with every letter of the alphabet. Pick any letter from A to Z to get a full list of English words — useful for word games, Wordle, vocabulary building, and more.">
<link rel="canonical" href="https://wordineer.com/words-that-start-with/">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Wordineer">
<meta property="og:title" content="Words That Start With Every Letter | A to Z Word Lists | Wordineer">
<meta property="og:description" content="Browse words that start with every letter of the alphabet. Pick any letter A–Z to get a full filterable word list.">
<meta property="og:url" content="https://wordineer.com/words-that-start-with/">
<meta property="og:image" content="https://wordineer.com/og-image.png">
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "CollectionPage",
  "name": "Words That Start With Every Letter",
  "description": "Browse English words organized by starting letter, from A to Z.",
  "url": "https://wordineer.com/words-that-start-with/"
}
</script>
<!-- /SLOT:meta -->

<!-- SLOT:style -->
<style>
.name-intro {
  font-size: 15px;
  line-height: 1.7;
  color: var(--text-2);
  margin: 0 0 20px;
}
.name-section {
  margin-top: 26px;
}
.name-section:first-of-type {
  margin-top: 0;
}
.name-section .section-title {
  margin-bottom: 4px;
}
.name-section .section-sub {
  margin-bottom: 14px;
}
.name-section .tools-grid {
  margin-bottom: 0;
}
.hub-prose {
  margin-top: 48px;
}
.hub-prose h2 {
  font-family: 'DM Serif Display', serif;
  font-size: 20px;
  font-weight: 400;
  margin: 0 0 10px;
  color: var(--text-1);
}
.hub-prose p {
  font-size: 15px;
  line-height: 1.75;
  color: var(--text-2);
  margin: 0 0 16px;
}
.faq-section {
  margin-top: 48px;
}
.faq-section > h2 {
  font-size: 20px;
  font-weight: 700;
  margin: 0 0 16px;
  color: var(--text-1);
}
.faq-item {
  border-bottom: 1px solid var(--border, #e5e5e5);
}
.faq-item summary {
  font-size: 15px;
  font-weight: 600;
  padding: 14px 0;
  cursor: pointer;
  list-style: none;
  color: var(--text-1);
}
.faq-item summary::-webkit-details-marker { display: none; }
.faq-item p {
  font-size: 14px;
  line-height: 1.7;
  color: var(--text-2);
  margin: 0 0 14px;
}
</style>
<!-- /SLOT:style -->

<!-- SLOT:hero -->
<div class="page-hero">
  <h1>Words That Start With…</h1>
  <p>Pick any letter to browse a full list of English words that begin with it. Every list is filterable by word type and difficulty — useful for word games, Wordle strategy, vocabulary study, and creative writing.</p>
</div>
<!-- /SLOT:hero -->

<!-- SLOT:content -->
<div class="content-wrap">
  <div class="section">
    <p class="name-intro">Choose a letter below. Each page opens a filterable word list you can search, sort, and copy — no sign-up required.</p>

    <div class="name-section">
      <h2 class="section-title">Browse by letter</h2>
      <p class="section-sub">26 letters. Thousands of words. Pick where to start.</p>
      <div class="tools-grid">

        <a class="tool-item" href="/words-that-start-with/a/">
          <div class="tool-icon" style="background:#EEEDFE"><svg viewBox="0 0 13 13" fill="none"><text x="6.5" y="9.5" text-anchor="middle" font-size="9" font-weight="700" font-family="sans-serif" fill="#534AB7">A</text></svg></div>
          <div class="tool-name">Words starting with A</div>
          <div class="tool-desc">Abundant, ambitious, and adventurous words.</div>
        </a>

        <a class="tool-item" href="/words-that-start-with/b/">
          <div class="tool-icon" style="background:#EAF0F6"><svg viewBox="0 0 13 13" fill="none"><text x="6.5" y="9.5" text-anchor="middle" font-size="9" font-weight="700" font-family="sans-serif" fill="#2F4F6F">B</text></svg></div>
          <div class="tool-name">Words starting with B</div>
          <div class="tool-desc">Bold, bright, and beautiful vocabulary.</div>
        </a>

        <a class="tool-item" href="/words-that-start-with/c/">
          <div class="tool-icon" style="background:#E1F5EE"><svg viewBox="0 0 13 13" fill="none"><text x="6.5" y="9.5" text-anchor="middle" font-size="9" font-weight="700" font-family="sans-serif" fill="#1D9E75">C</text></svg></div>
          <div class="tool-name">Words starting with C</div>
          <div class="tool-desc">One of the richest letters in English.</div>
        </a>

        <a class="tool-item" href="/words-that-start-with/d/">
          <div class="tool-icon" style="background:#FEF3E8"><svg viewBox="0 0 13 13" fill="none"><text x="6.5" y="9.5" text-anchor="middle" font-size="9" font-weight="700" font-family="sans-serif" fill="#C7435B">D</text></svg></div>
          <div class="tool-name">Words starting with D</div>
          <div class="tool-desc">Dynamic, detailed, and descriptive terms.</div>
        </a>

        <a class="tool-item" href="/words-that-start-with/e/">
          <div class="tool-icon" style="background:#EEF6E8"><svg viewBox="0 0 13 13" fill="none"><text x="6.5" y="9.5" text-anchor="middle" font-size="9" font-weight="700" font-family="sans-serif" fill="#2F6B1F">E</text></svg></div>
          <div class="tool-name">Words starting with E</div>
          <div class="tool-desc">Among the most common starting letters.</div>
        </a>

        <a class="tool-item" href="/words-that-start-with/f/">
          <div class="tool-icon" style="background:#EEEDFE"><svg viewBox="0 0 13 13" fill="none"><text x="6.5" y="9.5" text-anchor="middle" font-size="9" font-weight="700" font-family="sans-serif" fill="#534AB7">F</text></svg></div>
          <div class="tool-name">Words starting with F</div>
          <div class="tool-desc">Familiar, forceful, and fun vocabulary.</div>
        </a>

        <a class="tool-item" href="/words-that-start-with/g/">
          <div class="tool-icon" style="background:#EAF0F6"><svg viewBox="0 0 13 13" fill="none"><text x="6.5" y="9.5" text-anchor="middle" font-size="9" font-weight="700" font-family="sans-serif" fill="#2F4F6F">G</text></svg></div>
          <div class="tool-name">Words starting with G</div>
          <div class="tool-desc">Great for Wordle and word games.</div>
        </a>

        <a class="tool-item" href="/words-that-start-with/h/">
          <div class="tool-icon" style="background:#E1F5EE"><svg viewBox="0 0 13 13" fill="none"><text x="6.5" y="9.5" text-anchor="middle" font-size="9" font-weight="700" font-family="sans-serif" fill="#1D9E75">H</text></svg></div>
          <div class="tool-name">Words starting with H</div>
          <div class="tool-desc">Hundreds of high-frequency words.</div>
        </a>

        <a class="tool-item" href="/words-that-start-with/i/">
          <div class="tool-icon" style="background:#FEF3E8"><svg viewBox="0 0 13 13" fill="none"><text x="6.5" y="9.5" text-anchor="middle" font-size="9" font-weight="700" font-family="sans-serif" fill="#C7435B">I</text></svg></div>
          <div class="tool-name">Words starting with I</div>
          <div class="tool-desc">Intriguing, imaginative, and impactful terms.</div>
        </a>

        <a class="tool-item" href="/words-that-start-with/j/">
          <div class="tool-icon" style="background:#EEF6E8"><svg viewBox="0 0 13 13" fill="none"><text x="6.5" y="9.5" text-anchor="middle" font-size="9" font-weight="700" font-family="sans-serif" fill="#2F6B1F">J</text></svg></div>
          <div class="tool-name">Words starting with J</div>
          <div class="tool-desc">Joyful, jazzy, and just plain useful.</div>
        </a>

        <a class="tool-item" href="/words-that-start-with/k/">
          <div class="tool-icon" style="background:#EEEDFE"><svg viewBox="0 0 13 13" fill="none"><text x="6.5" y="9.5" text-anchor="middle" font-size="9" font-weight="700" font-family="sans-serif" fill="#534AB7">K</text></svg></div>
          <div class="tool-name">Words starting with K</div>
          <div class="tool-desc">Keen words, rare and common alike.</div>
        </a>

        <a class="tool-item" href="/words-that-start-with/l/">
          <div class="tool-icon" style="background:#EAF0F6"><svg viewBox="0 0 13 13" fill="none"><text x="6.5" y="9.5" text-anchor="middle" font-size="9" font-weight="700" font-family="sans-serif" fill="#2F4F6F">L</text></svg></div>
          <div class="tool-name">Words starting with L</div>
          <div class="tool-desc">Lively, lyrical, and lucid vocabulary.</div>
        </a>

        <a class="tool-item" href="/words-that-start-with/m/">
          <div class="tool-icon" style="background:#E1F5EE"><svg viewBox="0 0 13 13" fill="none"><text x="6.5" y="9.5" text-anchor="middle" font-size="9" font-weight="700" font-family="sans-serif" fill="#1D9E75">M</text></svg></div>
          <div class="tool-name">Words starting with M</div>
          <div class="tool-desc">Meaningful, melodic, and memorable words.</div>
        </a>

        <a class="tool-item" href="/words-that-start-with/n/">
          <div class="tool-icon" style="background:#FEF3E8"><svg viewBox="0 0 13 13" fill="none"><text x="6.5" y="9.5" text-anchor="middle" font-size="9" font-weight="700" font-family="sans-serif" fill="#C7435B">N</text></svg></div>
          <div class="tool-name">Words starting with N</div>
          <div class="tool-desc">Notable words across all difficulty levels.</div>
        </a>

        <a class="tool-item" href="/words-that-start-with/o/">
          <div class="tool-icon" style="background:#EEF6E8"><svg viewBox="0 0 13 13" fill="none"><text x="6.5" y="9.5" text-anchor="middle" font-size="9" font-weight="700" font-family="sans-serif" fill="#2F6B1F">O</text></svg></div>
          <div class="tool-name">Words starting with O</div>
          <div class="tool-desc">Original, open, and often overlooked words.</div>
        </a>

        <a class="tool-item" href="/words-that-start-with/p/">
          <div class="tool-icon" style="background:#EEEDFE"><svg viewBox="0 0 13 13" fill="none"><text x="6.5" y="9.5" text-anchor="middle" font-size="9" font-weight="700" font-family="sans-serif" fill="#534AB7">P</text></svg></div>
          <div class="tool-name">Words starting with P</div>
          <div class="tool-desc">Plenty of words — P is prolific.</div>
        </a>

        <a class="tool-item" href="/words-that-start-with/q/">
          <div class="tool-icon" style="background:#EAF0F6"><svg viewBox="0 0 13 13" fill="none"><text x="6.5" y="9.5" text-anchor="middle" font-size="9" font-weight="700" font-family="sans-serif" fill="#2F4F6F">Q</text></svg></div>
          <div class="tool-name">Words starting with Q</div>
          <div class="tool-desc">Quirky and rare — great for Wordle.</div>
        </a>

        <a class="tool-item" href="/words-that-start-with/r/">
          <div class="tool-icon" style="background:#E1F5EE"><svg viewBox="0 0 13 13" fill="none"><text x="6.5" y="9.5" text-anchor="middle" font-size="9" font-weight="700" font-family="sans-serif" fill="#1D9E75">R</text></svg></div>
          <div class="tool-name">Words starting with R</div>
          <div class="tool-desc">Rich, robust, and reliable vocabulary.</div>
        </a>

        <a class="tool-item" href="/words-that-start-with/s/">
          <div class="tool-icon" style="background:#FEF3E8"><svg viewBox="0 0 13 13" fill="none"><text x="6.5" y="9.5" text-anchor="middle" font-size="9" font-weight="700" font-family="sans-serif" fill="#C7435B">S</text></svg></div>
          <div class="tool-name">Words starting with S</div>
          <div class="tool-desc">The largest letter category in English.</div>
        </a>

        <a class="tool-item" href="/words-that-start-with/t/">
          <div class="tool-icon" style="background:#EEF6E8"><svg viewBox="0 0 13 13" fill="none"><text x="6.5" y="9.5" text-anchor="middle" font-size="9" font-weight="700" font-family="sans-serif" fill="#2F6B1F">T</text></svg></div>
          <div class="tool-name">Words starting with T</div>
          <div class="tool-desc">Timeless, tricky, and tactical words.</div>
        </a>

        <a class="tool-item" href="/words-that-start-with/u/">
          <div class="tool-icon" style="background:#EEEDFE"><svg viewBox="0 0 13 13" fill="none"><text x="6.5" y="9.5" text-anchor="middle" font-size="9" font-weight="700" font-family="sans-serif" fill="#534AB7">U</text></svg></div>
          <div class="tool-name">Words starting with U</div>
          <div class="tool-desc">Unusual and underused — good Wordle bets.</div>
        </a>

        <a class="tool-item" href="/words-that-start-with/v/">
          <div class="tool-icon" style="background:#EAF0F6"><svg viewBox="0 0 13 13" fill="none"><text x="6.5" y="9.5" text-anchor="middle" font-size="9" font-weight="700" font-family="sans-serif" fill="#2F4F6F">V</text></svg></div>
          <div class="tool-name">Words starting with V</div>
          <div class="tool-desc">Vivid, versatile, and vibrant vocabulary.</div>
        </a>

        <a class="tool-item" href="/words-that-start-with/w/">
          <div class="tool-icon" style="background:#E1F5EE"><svg viewBox="0 0 13 13" fill="none"><text x="6.5" y="9.5" text-anchor="middle" font-size="9" font-weight="700" font-family="sans-serif" fill="#1D9E75">W</text></svg></div>
          <div class="tool-name">Words starting with W</div>
          <div class="tool-desc">Widely used across all writing styles.</div>
        </a>

        <a class="tool-item" href="/words-that-start-with/x/">
          <div class="tool-icon" style="background:#FEF3E8"><svg viewBox="0 0 13 13" fill="none"><text x="6.5" y="9.5" text-anchor="middle" font-size="9" font-weight="700" font-family="sans-serif" fill="#C7435B">X</text></svg></div>
          <div class="tool-name">Words starting with X</div>
          <div class="tool-desc">Rare but striking — xeric, xenial, and more.</div>
        </a>

        <a class="tool-item" href="/words-that-start-with/y/">
          <div class="tool-icon" style="background:#EEF6E8"><svg viewBox="0 0 13 13" fill="none"><text x="6.5" y="9.5" text-anchor="middle" font-size="9" font-weight="700" font-family="sans-serif" fill="#2F6B1F">Y</text></svg></div>
          <div class="tool-name">Words starting with Y</div>
          <div class="tool-desc">Yearn, yield, yonder, and beyond.</div>
        </a>

        <a class="tool-item" href="/words-that-start-with/z/">
          <div class="tool-icon" style="background:#EEEDFE"><svg viewBox="0 0 13 13" fill="none"><text x="6.5" y="9.5" text-anchor="middle" font-size="9" font-weight="700" font-family="sans-serif" fill="#534AB7">Z</text></svg></div>
          <div class="tool-name">Words starting with Z</div>
          <div class="tool-desc">The rarest letter — zeal, zenith, and more.</div>
        </a>

      </div>
    </div>

    <div class="hub-prose">
      <h2>Why browse words by starting letter?</h2>
      <p>Filtering words by their first letter is one of the fastest ways to narrow a search when you already know something about what you're looking for. In word games like Wordle, Scrabble, or Scattergories, constraints often come in the form of a starting letter — knowing which words fit within that constraint is a practical skill. These lists also help writers find alternatives when a synonym search comes up short, and help students build vocabulary in a structured way.</p>
      <p>The letter S alone accounts for more English words than any other — well over a quarter of the dictionary depending on the source. Meanwhile, Q, X, and Z are the rarest starting letters, which is exactly why knowing the short lists for those letters can give you an edge in competitive word games.</p>
    </div>

    <div class="hub-prose">
      <h2>How these lists work</h2>
      <p>Each letter page draws from Wordineer's curated word dataset — the same one used by the <a href="/">random word generator</a>. Words are tagged by type (noun, verb, adjective, adverb) and difficulty (easy, medium, hard), so you can filter down to exactly the kind of word you need. All lists work instantly in the browser with no sign-up or download required.</p>
    </div>

    <div class="hub-prose">
      <h2>Useful for Wordle and other word games</h2>
      <p>One of the most common reasons people look up words by starting letter is Wordle strategy. When you've confirmed a starting letter but haven't cracked the full answer, browsing that letter's word list — especially filtered to five-letter words — can surface candidates you might not have thought of. Letters like Q, X, and Z are especially useful to study in advance because the valid word list for those letters is short enough to memorize.</p>
    </div>

    <div class="faq-section">
      <h2>Frequently asked questions</h2>

      <details class="faq-item">
        <summary>Which letter has the most words in English?</summary>
        <p>S has more words than any other starting letter in standard English dictionaries — estimates put it at around 15–20% of all entries. C, P, and T also have very large word counts. At the other end, X, Z, and Q have the fewest words starting with them, which is why those letters carry high point values in Scrabble.</p>
      </details>

      <details class="faq-item">
        <summary>Are these word lists useful for Wordle?</summary>
        <p>Yes. Once Wordle reveals a green tile for the first letter, you can jump to that letter's page and filter to five-letter words. For tricky letters like Q, U, X, or Z, the lists are short enough that scanning them quickly narrows your guesses significantly. The difficulty filter (easy / medium / hard) also helps — Wordle answers tend to be common words, so filtering to "easy" vocabulary is a good starting point.</p>
      </details>

      <details class="faq-item">
        <summary>What word types are included?</summary>
        <p>Each list includes nouns, verbs, adjectives, and adverbs. You can filter by word type on each letter's page. All words come from Wordineer's curated dataset — the same source used by the random word generator — so every entry includes a short definition and difficulty rating.</p>
      </details>

      <details class="faq-item">
        <summary>Can I use these lists for classroom vocabulary work?</summary>
        <p>Yes. Teachers often assign letter-based vocabulary exercises — "find five adjectives that start with B" — and these lists make it quick to check or generate examples. The difficulty filter lets you target age-appropriate vocabulary: easy words for younger students, hard words for advanced learners or SAT/ACT prep.</p>
      </details>

      <details class="faq-item">
        <summary>What are some good words starting with Q that don't need a U?</summary>
        <p>English has a small set of Q-without-U words, most borrowed from Arabic, Hebrew, or other languages: qoph (a Hebrew letter), qi (a variant of chi), qat (a plant), qigong (a wellness practice), and a handful of others. These are particularly useful in Scrabble where Q tiles are hard to play if there's no U available.</p>
      </details>
    </div>

  </div>
</div>
<!-- /SLOT:content -->
```

- [ ] **Step 2: Verify file exists**

```bash
ls -lh template-deploy/tools-src/words-that-start-with.html
```

Expected: file listed with non-zero size.

- [ ] **Step 3: Commit**

```bash
git add template-deploy/tools-src/words-that-start-with.html
git commit -m "feat: add words-that-start-with landing page source"
```

---

## Task 2: Update `tools.json`

**Files:**
- Modify: `template-deploy/tools.json`

Four sections need updating: `mega`, `more_word_tools`, `other_tools`, `footer_cols`.

- [ ] **Step 1: Add to `mega` — Writing & Vocabulary tools array**

In `tools.json`, find the `mega` array entry where `"cat": "Writing &amp; Vocabulary"`. Its `tools` array currently ends with `{ "href": "/word-counter/", ... }`. Append one entry:

```json
{ "href": "/words-that-start-with/", "text": "Words by Letter" }
```

- [ ] **Step 2: Add to `more_word_tools` array**

The `more_word_tools` array is a flat list of tool cards. Add this entry after the last existing card (before the closing `]`):

```json
{
  "href": "/words-that-start-with/",
  "name": "Words by letter",
  "desc": "Browse A–Z word lists by starting letter",
  "icon_bg": "#EEEDFE",
  "icon_path": "<text x=\"2\" y=\"9\" font-size=\"6\" font-weight=\"700\" font-family=\"sans-serif\" fill=\"#534AB7\">A</text><text x=\"7\" y=\"9\" font-size=\"6\" font-weight=\"700\" font-family=\"sans-serif\" fill=\"#534AB7\">Z</text>"
}
```

- [ ] **Step 3: Add to `other_tools` — Writing & Vocabulary links array**

In the `other_tools` array, find the entry where `"cat": "Writing &amp; Vocabulary"`. Its `links` array currently ends with `{ "href": "/word-counter/", ... }`. Append:

```json
{ "href": "/words-that-start-with/", "text": "Words by Letter" }
```

- [ ] **Step 4: Add to `footer_cols` — Writing & Vocabulary links array**

In the `footer_cols` array, find the entry where `"title": "Writing &amp; Vocabulary"`. Its `links` array currently ends with `{ "href": "/word-counter/", ... }`. Append:

```json
{ "href": "/words-that-start-with/", "text": "Words by Letter" }
```

- [ ] **Step 5: Validate JSON**

```bash
python3 -c "import json; json.load(open('template-deploy/tools.json')); print('OK')"
```

Expected output: `OK`

- [ ] **Step 6: Commit**

```bash
git add template-deploy/tools.json
git commit -m "feat: add words-that-start-with to navigation and tools registry"
```

---

## Task 3: Add hub-prose link block to `word-tools.html`

**Files:**
- Modify: `template-deploy/tools-src/word-tools.html` (around line 347 — after "Letters and characters" section, before existing `hub-prose` blocks)

- [ ] **Step 1: Insert hub-prose block**

In `template-deploy/tools-src/word-tools.html`, find the first `<div class="hub-prose">` block (line ~347). Insert the following **immediately before** it:

```html
    <div class="hub-prose">
      <h2>Looking for words by starting letter?</h2>
      <p>If you need words that begin with a specific letter — for Wordle, Scrabble, a vocabulary exercise, or a writing prompt — the <a href="/words-that-start-with/">words by letter hub</a> has a full A–Z index. Each letter links to a filterable list you can sort by word type and difficulty.</p>
    </div>

```

- [ ] **Step 2: Commit**

```bash
git add template-deploy/tools-src/word-tools.html
git commit -m "feat: add words-by-letter cross-link to word-tools hub"
```

---

## Task 4: Add `_redirects` rules

**Files:**
- Modify: `wordineer-deploy/_redirects`

Two lines needed per the site's established pattern: a 301 from `.html` to trailing-slash, and a 200 rewrite from trailing-slash to `.html`.

- [ ] **Step 1: Add redirect rules**

In `wordineer-deploy/_redirects`, find the "Clean URLs" section (where other `.html → /trailing-slash/` redirects live). Add these two lines together with the existing entries:

```
/words-that-start-with.html    /words-that-start-with/    301
```

Then in the "Pretty URL fallbacks" section (200 rewrites), add:

```
/words-that-start-with/    /words-that-start-with.html    200
```

- [ ] **Step 2: Commit**

```bash
git add wordineer-deploy/_redirects
git commit -m "feat: add clean URL redirects for words-that-start-with"
```

---

## Task 5: Build, copy output, and verify locally

**Files:**
- Run: `template-deploy/build.py`
- Copy output to: `wordineer-deploy/`

- [ ] **Step 1: Run the build**

```bash
cd template-deploy && python3 build.py
```

Expected: no errors, `output/words-that-start-with.html` and `output/word-tools.html` both present.

- [ ] **Step 2: Verify output files exist**

```bash
ls template-deploy/output/words-that-start-with.html template-deploy/output/word-tools.html
```

Expected: both files listed.

- [ ] **Step 3: Copy output to deploy folder**

```bash
cp template-deploy/output/words-that-start-with.html wordineer-deploy/
cp template-deploy/output/word-tools.html wordineer-deploy/
```

- [ ] **Step 4: Spot-check the built HTML**

```bash
grep -c 'words-that-start-with' wordineer-deploy/words-that-start-with.html
grep 'words-that-start-with' wordineer-deploy/word-tools.html
```

Expected: first command returns a count > 0; second command prints the anchor tag with the link.

- [ ] **Step 5: Start local server and verify in browser**

```bash
cd wordineer-deploy && python3 -m http.server 8080
```

Open `http://localhost:8080/words-that-start-with.html` and confirm:
- All 26 letter cards are visible
- Letter icons render (colored squares with letter text)
- Clicking a card navigates to `/words-that-start-with/[letter]/` (404 expected — pages not built yet)
- Open `http://localhost:8080/word-tools.html` and confirm the "Looking for words by starting letter?" prose block appears with a working link

- [ ] **Step 6: Commit built files**

```bash
git add wordineer-deploy/words-that-start-with.html wordineer-deploy/word-tools.html
git commit -m "build: generate words-that-start-with and updated word-tools pages"
```

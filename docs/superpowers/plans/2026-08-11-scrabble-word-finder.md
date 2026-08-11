# Scrabble Word Finder Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a Scrabble Word Finder at `/scrabble-word-finder/` — finds all valid words formable from input tiles, sorted by Scrabble point value, with a sortable-table results UI distinct from the existing Word Unscramble tool.

**Architecture:** Single `tools-src/scrabble-word-finder.html` file following the CONFIG + SLOT pattern. All word-matching logic is client-side JS. Data merges `dictionary.json` (primary, has definitions) + `words_expanded.json` (supplementary) at page idle — no new data files needed. Scrabble scores computed from a TILE map in JS.

**Tech Stack:** Vanilla HTML/CSS/JS. Static site built by `template-deploy/build.py`. Hosted on Cloudflare Pages.

---

## File Map

| Action | Path | Purpose |
|--------|------|---------|
| Create | `template-deploy/tools-src/scrabble-word-finder.html` | Source file — all slots |
| Modify | `template-deploy/tools.json` | Register in `more_word_tools` and `footer_cols` |
| Modify | `wordineer-deploy/_redirects` | Clean URL rewrites |
| Generate | `wordineer-deploy/scrabble-word-finder.html` | Build output (via build.py) |

---

## Task 1: CONFIG + meta + style slots

**Files:**
- Create: `template-deploy/tools-src/scrabble-word-finder.html`

- [ ] **Step 1: Create the file with CONFIG, meta, and style**

```html
<!-- CONFIG
{ "url": "/scrabble-word-finder/", "output": "scrabble-word-finder.html", "type": "tool" }
-->

<!-- SLOT:meta -->
<title>Scrabble Word Finder — Find Every Word from Your Letters | Wordineer</title>
<meta name="description" content="Enter your Scrabble tiles and instantly find every valid word, sorted by point value. Supports blank tiles (?), filters by length and score. Free anagram solver.">
<link rel="canonical" href="https://wordineer.com/scrabble-word-finder/">
<meta property="og:type"        content="website">
<meta property="og:site_name"   content="Wordineer">
<meta property="og:title"       content="Scrabble Word Finder — Find Every Word from Your Letters | Wordineer">
<meta property="og:description" content="Enter your Scrabble tiles and instantly find every valid word, sorted by point value. Supports blank tiles (?), filters by length and score.">
<meta property="og:url"         content="https://wordineer.com/scrabble-word-finder/">
<meta property="og:image"       content="https://wordineer.com/og-image.png">
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "WebApplication",
  "name": "Scrabble Word Finder",
  "url": "https://wordineer.com/scrabble-word-finder/",
  "description": "Find every valid word from your Scrabble tiles, sorted by point value. Supports blank tile wildcards and filters.",
  "applicationCategory": "UtilitiesApplication",
  "operatingSystem": "Any",
  "breadcrumb": {
    "@type": "BreadcrumbList",
    "itemListElement": [
      { "@type": "ListItem", "position": 1, "name": "Home",       "item": "https://wordineer.com/" },
      { "@type": "ListItem", "position": 2, "name": "Word Tools", "item": "https://wordineer.com/word-tools/" },
      { "@type": "ListItem", "position": 3, "name": "Scrabble Word Finder", "item": "https://wordineer.com/scrabble-word-finder/" }
    ]
  }
}
</script>
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "How do I find Scrabble words from my letters?",
      "acceptedAnswer": { "@type": "Answer", "text": "Type your Scrabble tiles into the input box and click Find Words (or press Enter). The tool searches through tens of thousands of valid English words and returns every word that can be formed from your letters, sorted by Scrabble point value highest first." }
    },
    {
      "@type": "Question",
      "name": "What does the ? wildcard do?",
      "acceptedAnswer": { "@type": "Answer", "text": "A ? acts as a blank tile — it can stand in for any letter. For example, entering 'aeirnt?' will find all words formable from those six letters plus one blank tile. Each ? counts as one character toward the 15-letter limit." }
    },
    {
      "@type": "Question",
      "name": "Which dictionary does this Scrabble word finder use?",
      "acceptedAnswer": { "@type": "Answer", "text": "The word finder uses a broad English dictionary covering tens of thousands of valid words. The NWL, SOWPODS, and WWF labels let you see the naming conventions for each game, but all three draw from the same underlying word set." }
    },
    {
      "@type": "Question",
      "name": "How are Scrabble points calculated?",
      "acceptedAnswer": { "@type": "Answer", "text": "Each letter has a fixed point value: A, E, I, O, U, L, N, S, T, R = 1 point; D, G = 2; B, C, M, P = 3; F, H, V, W, Y = 4; K = 5; J, X = 8; Q, Z = 10. Blank tiles (?) score 0. The tool adds up face values — it does not account for board multipliers." }
    },
    {
      "@type": "Question",
      "name": "What is the difference between this and the Word Unscramble tool?",
      "acceptedAnswer": { "@type": "Answer", "text": "Both tools find words from a set of letters. The Scrabble Word Finder sorts results by point value and displays them in a table with scores highlighted — making it faster to find the highest-scoring play. Word Unscramble groups results by word length, which is more useful for crosswords where length is the priority." }
    }
  ]
}
</script>
<!-- /SLOT:meta -->

<!-- SLOT:style -->
<style>
.swf-wrap{max-width:960px;margin:32px auto 0;padding:0 16px 48px}
.swf-input-row{display:flex;gap:8px;margin-bottom:12px}
.swf-input{flex:1;min-width:0;padding:13px 16px;font-size:1.05rem;border:2px solid #d1d5db;border-radius:8px;font-family:inherit;outline:none;transition:border-color .15s}
.swf-input:focus{border-color:var(--brand,#4f46e5)}
.swf-find-btn{padding:13px 22px;background:var(--brand,#4f46e5);color:#fff;border:none;border-radius:8px;font-size:1rem;font-weight:600;cursor:pointer;white-space:nowrap;transition:background .15s;font-family:inherit}
.swf-find-btn:hover{background:var(--brand-dark,#4338ca)}
.swf-clear-btn{padding:13px 14px;background:#f3f4f6;border:2px solid #d1d5db;border-radius:8px;font-size:1rem;cursor:pointer;color:#6b7280;transition:background .15s;font-family:inherit}
.swf-clear-btn:hover{background:#e5e7eb}
.swf-filters{display:flex;flex-wrap:wrap;gap:10px;margin-bottom:16px;align-items:flex-end}
.swf-filter-group{display:flex;flex-direction:column;gap:3px}
.swf-filter-label{font-size:0.72rem;font-weight:600;color:#6b7280;text-transform:uppercase;letter-spacing:.04em}
.swf-filter-select,.swf-filter-input{padding:7px 10px;border:1.5px solid #d1d5db;border-radius:6px;font-size:0.9rem;font-family:inherit;background:#fff;color:#111;outline:none}
.swf-filter-select:focus,.swf-filter-input:focus{border-color:var(--brand,#4f46e5)}
.swf-filter-input{width:90px}
.swf-dict-toggle{display:flex;border:1.5px solid #d1d5db;border-radius:6px;overflow:hidden}
.swf-dict-btn{padding:7px 12px;font-size:0.85rem;font-family:inherit;border:none;background:#fff;cursor:pointer;color:#374151;transition:background .12s,color .12s}
.swf-dict-btn.active{background:var(--brand,#4f46e5);color:#fff}
.swf-status{color:#6b7280;font-size:0.9rem;margin-bottom:8px;min-height:20px}
.swf-results-header{display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:8px;margin-bottom:10px}
.swf-count{font-size:0.9rem;color:#6b7280}
.swf-sort-bar{display:flex;gap:6px;align-items:center}
.swf-sort-label{font-size:0.8rem;color:#6b7280}
.swf-sort-btn{padding:5px 12px;border:1.5px solid #d1d5db;border-radius:20px;font-size:0.82rem;background:#fff;cursor:pointer;font-family:inherit;color:#374151;transition:all .12s}
.swf-sort-btn.active{border-color:var(--brand,#4f46e5);background:var(--brand,#4f46e5);color:#fff}
.swf-copy-all-btn{padding:5px 14px;border:1.5px solid #d1d5db;border-radius:20px;font-size:0.82rem;background:#fff;cursor:pointer;font-family:inherit;color:#374151;transition:background .12s}
.swf-copy-all-btn:hover{background:#f3f4f6}
.swf-table-wrap{overflow-x:auto}
.swf-table{width:100%;border-collapse:collapse;font-size:0.95rem}
.swf-table th{text-align:left;padding:9px 12px;font-size:0.78rem;font-weight:700;color:#6b7280;text-transform:uppercase;letter-spacing:.05em;border-bottom:2px solid #e5e7eb;white-space:nowrap}
.swf-table td{padding:9px 12px;border-bottom:1px solid #f3f4f6;vertical-align:middle}
.swf-table tr:last-child td{border-bottom:none}
.swf-table tbody tr:hover td{background:#f9fafb}
.swf-word-cell{font-weight:600;font-size:1rem;color:#111;letter-spacing:.02em;position:relative;cursor:default}
.swf-pts-badge{display:inline-block;background:#f0fdf4;color:#15803d;font-weight:700;font-size:0.85rem;padding:2px 8px;border-radius:12px}
.swf-def-text{color:#6b7280;font-size:0.88rem;max-width:300px}
.swf-row-copy{padding:4px 10px;border:1.5px solid #e5e7eb;border-radius:5px;font-size:0.78rem;background:#fff;cursor:pointer;color:#374151;font-family:inherit;transition:background .1s;white-space:nowrap}
.swf-row-copy:hover{background:#f3f4f6}
.swf-tooltip{position:absolute;left:0;top:calc(100% + 4px);z-index:10;background:#1f2937;color:#fff;font-size:0.82rem;padding:6px 10px;border-radius:6px;white-space:normal;max-width:220px;pointer-events:none;display:none;font-weight:400;line-height:1.4}
.swf-word-cell:hover .swf-tooltip{display:block}
.swf-empty{text-align:center;padding:40px 20px;color:#9ca3af;font-size:0.95rem}
.swf-expand-row{display:none}
.swf-expand-row.open{display:table-row}
.swf-expand-def{padding:2px 12px 10px;color:#6b7280;font-size:0.88rem;font-style:italic}
@media(max-width:640px){
  .swf-table .swf-def-cell,.swf-table .swf-def-hdr{display:none}
  .swf-word-cell{cursor:pointer}
  .swf-filter-input{width:74px}
  .swf-input-row{flex-wrap:wrap}
  .swf-find-btn{flex:1}
}
</style>
<!-- /SLOT:style -->
```

- [ ] **Step 2: Verify the file exists**

```bash
ls template-deploy/tools-src/scrabble-word-finder.html
```

Expected: file listed with no error.

- [ ] **Step 3: Commit**

```bash
git add template-deploy/tools-src/scrabble-word-finder.html
git commit -m "feat: scaffold scrabble-word-finder tool-src with meta and style"
```

---

## Task 2: hero + tool slots

**Files:**
- Modify: `template-deploy/tools-src/scrabble-word-finder.html`

- [ ] **Step 1: Append hero slot after the closing `<!-- /SLOT:style -->`**

```html
<!-- SLOT:hero -->
<div class="hero">
  <div class="hero-inner">
    <h1 class="hero-title">Scrabble Word Finder</h1>
    <p class="hero-sub">Enter your tiles and instantly find every valid word, sorted by Scrabble point value. Use <strong>?</strong> for blank tiles.</p>
  </div>
</div>
<!-- /SLOT:hero -->
```

- [ ] **Step 2: Append tool slot after `<!-- /SLOT:hero -->`**

```html
<!-- SLOT:tool -->
<div class="swf-wrap">
  <div class="swf-input-row">
    <input id="swf-input" class="swf-input" type="text"
      placeholder="Enter letters (e.g. aeirnt?)" maxlength="15"
      autocomplete="off" autocorrect="off" autocapitalize="none" spellcheck="false"
      aria-label="Enter Scrabble tiles">
    <button id="swf-find-btn" class="swf-find-btn">Find Words</button>
    <button id="swf-clear-btn" class="swf-clear-btn" title="Clear" aria-label="Clear input">✕</button>
  </div>

  <div class="swf-filters">
    <div class="swf-filter-group">
      <span class="swf-filter-label">Length</span>
      <select id="swf-len" class="swf-filter-select" aria-label="Word length">
        <option value="">Any</option>
        <option value="2-3">2–3</option>
        <option value="4-5">4–5</option>
        <option value="6-7">6–7</option>
        <option value="8+">8+</option>
      </select>
    </div>
    <div class="swf-filter-group">
      <span class="swf-filter-label">Min pts</span>
      <select id="swf-minpts" class="swf-filter-select" aria-label="Minimum points">
        <option value="0">Any</option>
        <option value="5">5+</option>
        <option value="10">10+</option>
        <option value="15">15+</option>
      </select>
    </div>
    <div class="swf-filter-group">
      <span class="swf-filter-label">Starts with</span>
      <input id="swf-starts" class="swf-filter-input" type="text" maxlength="3"
        placeholder="e.g. re" autocomplete="off" autocorrect="off" autocapitalize="none"
        spellcheck="false" aria-label="Starts with">
    </div>
    <div class="swf-filter-group">
      <span class="swf-filter-label">Ends with</span>
      <input id="swf-ends" class="swf-filter-input" type="text" maxlength="3"
        placeholder="e.g. ing" autocomplete="off" autocorrect="off" autocapitalize="none"
        spellcheck="false" aria-label="Ends with">
    </div>
    <div class="swf-filter-group">
      <span class="swf-filter-label">Contains</span>
      <input id="swf-contains" class="swf-filter-input" type="text" maxlength="3"
        placeholder="e.g. qu" autocomplete="off" autocorrect="off" autocapitalize="none"
        spellcheck="false" aria-label="Must contain">
    </div>
    <div class="swf-filter-group">
      <span class="swf-filter-label">Dictionary</span>
      <div class="swf-dict-toggle" role="group" aria-label="Dictionary">
        <button class="swf-dict-btn active" data-dict="nwl">NWL</button>
        <button class="swf-dict-btn" data-dict="sowpods">SOWPODS</button>
        <button class="swf-dict-btn" data-dict="wwf">WWF</button>
      </div>
    </div>
  </div>

  <div id="swf-status" class="swf-status"></div>

  <div id="swf-results-header" class="swf-results-header" style="display:none">
    <span id="swf-count" class="swf-count"></span>
    <div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap">
      <div class="swf-sort-bar">
        <span class="swf-sort-label">Sort:</span>
        <button class="swf-sort-btn active" data-sort="pts">Points ↓</button>
        <button class="swf-sort-btn" data-sort="len">Length ↓</button>
        <button class="swf-sort-btn" data-sort="az">A–Z</button>
      </div>
      <button id="swf-copy-all" class="swf-copy-all-btn">Copy all</button>
    </div>
  </div>

  <div class="swf-table-wrap">
    <table id="swf-table" class="swf-table" style="display:none">
      <thead>
        <tr>
          <th>Word</th>
          <th>Len</th>
          <th>Pts</th>
          <th class="swf-def-hdr">Definition</th>
          <th></th>
        </tr>
      </thead>
      <tbody id="swf-tbody"></tbody>
    </table>
  </div>

  <div id="swf-empty" class="swf-empty" style="display:none">
    No words found — try removing a filter or adding a wildcard (?).
  </div>
</div>
<!-- /SLOT:tool -->
```

- [ ] **Step 3: Commit**

```bash
git add template-deploy/tools-src/scrabble-word-finder.html
git commit -m "feat: add hero and tool input/table HTML to scrabble-word-finder"
```

---

## Task 3: ad_b, explainer, faq, who slots

**Files:**
- Modify: `template-deploy/tools-src/scrabble-word-finder.html`

- [ ] **Step 1: Append ad_b slot after `<!-- /SLOT:tool -->`**

```html
<!-- SLOT:ad_b -->
<div class="content-wrap" style="margin-top:32px">
  <div class="ad-rect">
    <span class="ad-tag">Advertisement · 336×280</span>
    <div class="ad-rect-img"><svg viewBox="0 0 36 36" fill="none"><path d="M18 4C10.3 4 4 10.3 4 18s6.3 14 14 14 14-6.3 14-14S25.7 4 18 4z" fill="white" opacity=".2"/><path d="M12 18c0-3.3 2.7-6 6-6s6 2.7 6 6-2.7 6-6 6" stroke="white" stroke-width="2" stroke-linecap="round"/><circle cx="18" cy="18" r="2.5" fill="white"/></svg></div>
    <div class="ad-rect-content">
      <div class="ad-rect-title">Grammarly — write with confidence</div>
      <div class="ad-rect-body">Grammar, tone &amp; clarity. Used by 30 million people. Works in Google Docs, Gmail, Word and more.</div>
      <a href="https://grammarly.com" target="_blank" rel="noopener" class="aff-cta-btn">Try Grammarly free <svg viewBox="0 0 11 11" fill="none"><path d="M2 5.5h7M6 3l2.5 2.5L6 8" stroke="white" stroke-width="1.3" stroke-linecap="round"/></svg></a>
    </div>
  </div>
</div>
<!-- /SLOT:ad_b -->
```

- [ ] **Step 2: Append explainer slot after `<!-- /SLOT:ad_b -->`**

```html
<!-- SLOT:explainer -->
<div class="explainer">
  <div class="explainer-inner">
    <h2>How to use the Scrabble Word Finder</h2>
    <p>Type your rack letters into the input box — up to 15 at once — and press Enter or click <strong>Find Words</strong>. The tool searches through tens of thousands of English words and returns every word that can be formed from your letters, sorted from highest to lowest Scrabble point value so the best play is always at the top.</p>
    <p>Add <strong>?</strong> for a blank tile. A blank can substitute any letter, so entering <em>aeirnt?</em> will surface words that need one extra letter beyond what you have. Use <strong>Starts with</strong> and <strong>Ends with</strong> to fit a word into a specific board position — essential when you need to connect to an existing letter on the board.</p>

    <div class="aff-writing">
      <div class="aff-sponsored">✦ Sponsored <span class="ad-pill">Ad</span></div>
      <div class="aff-writing-body">Once you have your words, Grammarly makes sure your writing is clear, mistake-free, and compelling — right inside Google Docs, Word, or your browser.</div>
      <a href="https://grammarly.com" target="_blank" rel="noopener" class="aff-cta-btn">Write better with Grammarly — free to start <svg viewBox="0 0 11 11" fill="none"><path d="M2 5.5h7M6 3l2.5 2.5L6 8" stroke="white" stroke-width="1.3" stroke-linecap="round"/></svg></a>
    </div>

    <h3>Sorting and filtering results</h3>
    <p>Results default to <strong>Points ↓</strong> — highest scoring first. Switch to <strong>Length ↓</strong> to prioritise longer words, or <strong>A–Z</strong> for alphabetical. Use <strong>Min pts</strong> to hide low-value words and focus on plays worth 10 or 15+ points. The <strong>Length</strong> filter narrows results to a specific range — useful when a board slot can only fit a 4- or 5-letter word.</p>

    <h3>Scrabble tile point values</h3>
    <p>A, E, I, O, U, L, N, S, T, R = 1 pt · D, G = 2 · B, C, M, P = 3 · F, H, V, W, Y = 4 · K = 5 · J, X = 8 · Q, Z = 10. Blank tiles (?) = 0. Scores shown are face-value totals — board multipliers (double/triple squares) are not included.</p>

    <h3>NWL, SOWPODS, and WWF</h3>
    <p><strong>NWL</strong> (North American Word List) is used in North American tournament Scrabble. <strong>SOWPODS</strong> is the international Scrabble dictionary — it includes more words than NWL. <strong>WWF</strong> (Words With Friends) uses its own word set with some differences from both. The toggle on this tool is a labelling aid — all three draw from the same underlying Wordineer word set, which overlaps heavily with all three game dictionaries.</p>

    <h3>Difference between this tool and Word Unscramble</h3>
    <p>The <a href="/word-unscramble/">Word Unscramble</a> tool groups results by word length — best for crosswords and puzzles where fitting a specific slot matters. The Scrabble Word Finder sorts by point value first — best when you want to maximise your score. Use whichever matches your goal.</p>
  </div>
</div>
<!-- /SLOT:explainer -->
```

- [ ] **Step 3: Append faq slot after `<!-- /SLOT:explainer -->`**

```html
<!-- SLOT:faq -->
<div class="faq">
  <h2 class="faq-title">Frequently asked questions</h2>
  <div class="faq-item open">
    <div class="faq-q"><span class="faq-q-text">How do I find Scrabble words from my letters?</span><svg class="faq-chevron" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div>
    <div class="faq-a"><p>Type your Scrabble tiles into the input box and click Find Words (or press Enter). The tool returns every word that can be formed from your letters, sorted by Scrabble point value. Use <strong>?</strong> for each blank tile you have.</p></div>
  </div>
  <div class="faq-item">
    <div class="faq-q"><span class="faq-q-text">What does the ? wildcard do?</span><svg class="faq-chevron" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div>
    <div class="faq-a"><p>A <strong>?</strong> acts as a blank tile — it can stand in for any letter. Enter up to two wildcards. For example, <em>aeirnt?</em> finds all words formable from those six letters plus one blank. Each ? counts toward the 15-letter limit and scores 0 points.</p></div>
  </div>
  <div class="faq-item">
    <div class="faq-q"><span class="faq-q-text">Which dictionary does this Scrabble word finder use?</span><svg class="faq-chevron" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div>
    <div class="faq-a"><p>The tool uses Wordineer's English word set — tens of thousands of valid words covering the most common entries in NWL, SOWPODS, and WWF. The dictionary toggle is a labelling aid; all three options use the same underlying word list.</p></div>
  </div>
  <div class="faq-item">
    <div class="faq-q"><span class="faq-q-text">How are Scrabble points calculated?</span><svg class="faq-chevron" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div>
    <div class="faq-a"><p>Face values per letter: A E I O U L N S T R = 1 · D G = 2 · B C M P = 3 · F H V W Y = 4 · K = 5 · J X = 8 · Q Z = 10. Blank (?) = 0. The totals shown are raw face-value sums — board multipliers are not counted.</p></div>
  </div>
  <div class="faq-item">
    <div class="faq-q"><span class="faq-q-text">What is the difference between this and the Word Unscramble tool?</span><svg class="faq-chevron" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div>
    <div class="faq-a"><p>Both find valid words from a set of letters. The Scrabble Word Finder sorts by point value first and shows results in a table with scores highlighted — ideal when maximising your score matters. Word Unscramble groups by word length — better for crosswords where fitting a slot length is the priority.</p></div>
  </div>
</div>
<!-- /SLOT:faq -->
```

- [ ] **Step 4: Append who slot after `<!-- /SLOT:faq -->`**

```html
<!-- SLOT:who -->
<div>
  <h2 class="section-title" style="margin-bottom:14px">Who uses Wordineer</h2>
  <div class="uc-grid">
    <div class="uc"><div class="uc-title">Scrabble players</div><div class="uc-body">Find the highest-scoring play from your rack. Filter by length and starting letter to fit the board position you need.</div></div>
    <div class="uc"><div class="uc-title">Words With Friends players</div><div class="uc-body">Enter your rack and find every valid word sorted by point value — same tile logic, works for WWF scoring.</div></div>
    <div class="uc"><div class="uc-title">Crossword solvers</div><div class="uc-body">Know the length and a few anchor letters? Use Starts with, Ends with, and Must contain to narrow down what fits.</div></div>
    <div class="uc"><div class="uc-title">Word game enthusiasts</div><div class="uc-body">Works for Boggle, Wordle, Quordle, and any letter-tile game — find every word hiding in a set of letters instantly.</div></div>
  </div>
</div>
<!-- /SLOT:who -->
```

- [ ] **Step 5: Commit**

```bash
git add template-deploy/tools-src/scrabble-word-finder.html
git commit -m "feat: add content slots to scrabble-word-finder (ad, explainer, faq, who)"
```

---

## Task 4: init slot (JS engine)

**Files:**
- Modify: `template-deploy/tools-src/scrabble-word-finder.html`

- [ ] **Step 1: Append init slot after `<!-- /SLOT:who -->`**

The entire SWF engine goes here. Note: `words_expanded.json` entries have the word in `e.w` with a capital first letter (e.g. `"Aback"`) — `parseEntry` lowercases all words.

```html
<!-- SLOT:init -->
<script>
const SWF = (() => {
  const TILE = {a:1,b:3,c:3,d:2,e:1,f:4,g:2,h:4,i:1,j:8,k:5,l:1,m:3,n:1,o:1,p:3,q:10,r:1,s:1,t:1,u:1,v:4,w:4,x:8,y:4,z:10};

  let DICT = [];
  let dictLoaded = false;
  let dictLoadPromise = null;
  let currentSort = 'pts';
  let lastResults = [];

  function tileScore(word) {
    return word.split('').reduce((s, c) => s + (TILE[c] || 0), 0);
  }

  function esc(s) {
    return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
  }

  function parseEntry(e) {
    if (typeof e === 'string') return { w: e.toLowerCase(), d: '' };
    if (Array.isArray(e))     return { w: (e[0] || '').toLowerCase(), d: '' };
    return {
      w: (e.w || e.word || '').toLowerCase(),
      d: e.d || e.def || e.definition || ''
    };
  }

  function loadDict() {
    if (dictLoadPromise) return dictLoadPromise;
    dictLoadPromise = (async () => {
      const seen = new Set();
      async function ingest(url) {
        try {
          const r = await fetch(url);
          if (!r.ok) return;
          const raw = await r.json();
          const arr = Array.isArray(raw) ? raw : Object.values(raw);
          arr.forEach(e => {
            const { w, d } = parseEntry(e);
            if (w && w.length >= 2 && /^[a-z]+$/.test(w) && !seen.has(w)) {
              seen.add(w);
              DICT.push({ w, d });
            }
          });
        } catch {}
      }
      await ingest('/data/dictionary.json');
      await ingest('/data/words_expanded.json');
      dictLoaded = true;
    })();
    return dictLoadPromise;
  }

  function scheduleDictLoad(delay) {
    setTimeout(function() {
      if ('requestIdleCallback' in window) {
        requestIdleCallback(loadDict);
      } else {
        loadDict();
      }
    }, delay);
  }

  function canFormWord(word, inputCounts, wildcards) {
    var needed = {};
    for (var i = 0; i < word.length; i++) {
      var ch = word[i];
      needed[ch] = (needed[ch] || 0) + 1;
    }
    var wildcardsNeeded = 0;
    for (var letter in needed) {
      var have = inputCounts[letter] || 0;
      if (have < needed[letter]) wildcardsNeeded += needed[letter] - have;
    }
    return wildcardsNeeded <= wildcards;
  }

  function parseInput(raw) {
    var clean = raw.toLowerCase().replace(/[^a-z?]/g, '');
    var counts = {};
    var wildcards = 0;
    for (var i = 0; i < clean.length; i++) {
      var ch = clean[i];
      if (ch === '?') wildcards++;
      else counts[ch] = (counts[ch] || 0) + 1;
    }
    return { counts: counts, wildcards: wildcards };
  }

  function applyFilters(results) {
    var lenVal    = document.getElementById('swf-len').value;
    var minPts    = parseInt(document.getElementById('swf-minpts').value, 10) || 0;
    var starts    = document.getElementById('swf-starts').value.toLowerCase().trim();
    var ends      = document.getElementById('swf-ends').value.toLowerCase().trim();
    var contains  = document.getElementById('swf-contains').value.toLowerCase().trim();

    return results.filter(function(r) {
      var w = r.w;
      var len = w.length;
      if (lenVal === '2-3' && (len < 2 || len > 3)) return false;
      if (lenVal === '4-5' && (len < 4 || len > 5)) return false;
      if (lenVal === '6-7' && (len < 6 || len > 7)) return false;
      if (lenVal === '8+'  && len < 8)               return false;
      if (r.pts < minPts)                             return false;
      if (starts   && w.indexOf(starts) !== 0)        return false;
      if (ends     && w.slice(-ends.length) !== ends) return false;
      if (contains && w.indexOf(contains) === -1)     return false;
      return true;
    });
  }

  function sortResults(results) {
    var sorted = results.slice();
    if (currentSort === 'pts') {
      sorted.sort(function(a, b) { return b.pts - a.pts || a.w.localeCompare(b.w); });
    } else if (currentSort === 'len') {
      sorted.sort(function(a, b) { return b.w.length - a.w.length || b.pts - a.pts; });
    } else {
      sorted.sort(function(a, b) { return a.w.localeCompare(b.w); });
    }
    return sorted;
  }

  function copyText(text) {
    if (navigator.clipboard) {
      navigator.clipboard.writeText(text).catch(function() {});
    } else {
      var ta = document.createElement('textarea');
      ta.value = text;
      ta.style.cssText = 'position:fixed;opacity:0;top:0;left:0';
      document.body.appendChild(ta);
      ta.select();
      try { document.execCommand('copy'); } catch(e) {}
      document.body.removeChild(ta);
    }
  }

  function renderTable(results) {
    var tbody  = document.getElementById('swf-tbody');
    var table  = document.getElementById('swf-table');
    var empty  = document.getElementById('swf-empty');
    var header = document.getElementById('swf-results-header');
    var count  = document.getElementById('swf-count');

    if (!results.length) {
      table.style.display  = 'none';
      empty.style.display  = 'block';
      header.style.display = 'none';
      return;
    }

    empty.style.display  = 'none';
    table.style.display  = 'table';
    header.style.display = 'flex';
    count.textContent    = 'Found ' + results.length + ' word' + (results.length === 1 ? '' : 's');

    var rows = results.map(function(r) {
      var word    = esc(r.w);
      var def     = esc(r.d);
      var tooltip = def ? '<span class="swf-tooltip">' + def + '</span>' : '';
      return '<tr>' +
        '<td class="swf-word-cell">' + word + tooltip + '</td>' +
        '<td>' + r.w.length + '</td>' +
        '<td><span class="swf-pts-badge">' + r.pts + '</span></td>' +
        '<td class="swf-def-cell swf-def-text">' + def + '</td>' +
        '<td><button class="swf-row-copy" data-word="' + word + '">Copy</button></td>' +
        '</tr>' +
        '<tr class="swf-expand-row">' +
        '<td colspan="5" class="swf-expand-def">' + def + '</td>' +
        '</tr>';
    }).join('');

    tbody.innerHTML = rows;

    tbody.querySelectorAll('.swf-row-copy').forEach(function(btn) {
      btn.addEventListener('click', function() {
        copyText(btn.dataset.word);
        var orig = btn.textContent;
        btn.textContent = 'Copied!';
        setTimeout(function() { btn.textContent = orig; }, 1200);
      });
    });

    tbody.querySelectorAll('.swf-word-cell').forEach(function(cell) {
      cell.addEventListener('click', function() {
        var expandRow = cell.closest('tr').nextElementSibling;
        if (expandRow && expandRow.classList.contains('swf-expand-row')) {
          expandRow.classList.toggle('open');
        }
      });
    });
  }

  function doFind(raw) {
    var parsed    = parseInput(raw);
    var matched   = DICT
      .filter(function(e) { return canFormWord(e.w, parsed.counts, parsed.wildcards); })
      .map(function(e)    { return { w: e.w, d: e.d, pts: tileScore(e.w) }; });
    lastResults = matched;
    renderTable(sortResults(applyFilters(matched)));
  }

  function find() {
    var raw    = document.getElementById('swf-input').value.trim();
    var status = document.getElementById('swf-status');
    if (!raw) return;

    if (!dictLoaded) {
      status.textContent = 'Loading dictionary…';
      loadDict().then(function() {
        status.textContent = '';
        doFind(raw);
      });
      return;
    }
    status.textContent = '';
    doFind(raw);
  }

  function rerender() {
    if (!lastResults.length) return;
    renderTable(sortResults(applyFilters(lastResults)));
  }

  function init() {
    var input      = document.getElementById('swf-input');
    var findBtn    = document.getElementById('swf-find-btn');
    var clearBtn   = document.getElementById('swf-clear-btn');
    var copyAllBtn = document.getElementById('swf-copy-all');

    input.addEventListener('keydown', function(e) { if (e.key === 'Enter') find(); });
    findBtn.addEventListener('click', find);

    clearBtn.addEventListener('click', function() {
      input.value = '';
      document.getElementById('swf-tbody').innerHTML         = '';
      document.getElementById('swf-table').style.display    = 'none';
      document.getElementById('swf-empty').style.display    = 'none';
      document.getElementById('swf-results-header').style.display = 'none';
      document.getElementById('swf-status').textContent     = '';
      document.getElementById('swf-count').textContent      = '';
      lastResults = [];
    });

    document.querySelectorAll('.swf-sort-btn').forEach(function(btn) {
      btn.addEventListener('click', function() {
        document.querySelectorAll('.swf-sort-btn').forEach(function(b) { b.classList.remove('active'); });
        btn.classList.add('active');
        currentSort = btn.dataset.sort;
        rerender();
      });
    });

    document.querySelectorAll('.swf-dict-btn').forEach(function(btn) {
      btn.addEventListener('click', function() {
        document.querySelectorAll('.swf-dict-btn').forEach(function(b) { b.classList.remove('active'); });
        btn.classList.add('active');
      });
    });

    ['swf-len','swf-minpts'].forEach(function(id) {
      document.getElementById(id).addEventListener('change', rerender);
    });
    ['swf-starts','swf-ends','swf-contains'].forEach(function(id) {
      document.getElementById(id).addEventListener('input', rerender);
    });

    if (copyAllBtn) {
      copyAllBtn.addEventListener('click', function() {
        if (!lastResults.length) return;
        var text = sortResults(applyFilters(lastResults)).map(function(r) { return r.w; }).join('\n');
        copyText(text);
        var orig = copyAllBtn.textContent;
        copyAllBtn.textContent = 'Copied!';
        setTimeout(function() { copyAllBtn.textContent = orig; }, 1200);
      });
    }

    document.querySelectorAll('.faq-q').forEach(function(q) {
      q.addEventListener('click', function() { q.closest('.faq-item').classList.toggle('open'); });
    });

    input.addEventListener('focus', function() {
      if (!dictLoadPromise) loadDict();
    }, { once: true });

    if (document.readyState === 'complete') {
      scheduleDictLoad(2000);
    } else {
      window.addEventListener('load', function() { scheduleDictLoad(2000); }, { once: true });
    }
  }

  return { init: init };
})();

SWF.init();
</script>
<!-- /SLOT:init -->
```

- [ ] **Step 2: Verify the file has all 9 slots** (CONFIG + meta, style, hero, tool, ad_b, explainer, faq, who, init)

```bash
grep -c 'SLOT:' template-deploy/tools-src/scrabble-word-finder.html
```

Expected output: `18` (9 opening + 9 closing slot tags).

- [ ] **Step 3: Commit**

```bash
git add template-deploy/tools-src/scrabble-word-finder.html
git commit -m "feat: add JS engine to scrabble-word-finder init slot"
```

---

## Task 5: Register in tools.json and _redirects

**Files:**
- Modify: `template-deploy/tools.json`
- Modify: `wordineer-deploy/_redirects`

### tools.json

- [ ] **Step 1: Add to `more_word_tools`**

Open `template-deploy/tools.json`. Find the `"more_word_tools"` array. Add this entry after the `"Rhyming Dictionary"` entry (keep alphabetical/logical grouping with word-game tools):

```json
"Scrabble Word Finder",
```

- [ ] **Step 2: Add to `footer_cols`**

Find the footer column that contains word tools (the column containing entries like `"Word Unscramble"`, `"Word Scramble"`, `"Rhyming Dictionary"`). Add:

```json
{ "href": "/scrabble-word-finder/", "text": "Scrabble Word Finder" }
```

Add it only if that column has fewer than 4 tool links. If the column is already at 4 links, skip this step (hub page "View all" handles discovery).

### _redirects

- [ ] **Step 3: Add clean URL rules to `wordineer-deploy/_redirects`**

Add these two lines at the end of the file (before any trailing comments):

```
/scrabble-word-finder.html    /scrabble-word-finder/    301
/scrabble-word-finder/        /scrabble-word-finder.html    200
```

- [ ] **Step 4: Commit**

```bash
git add template-deploy/tools.json wordineer-deploy/_redirects
git commit -m "feat: register scrabble-word-finder in tools.json and _redirects"
```

---

## Task 6: Build, copy, and smoke test

**Files:**
- Generate: `wordineer-deploy/scrabble-word-finder.html`

- [ ] **Step 1: Run the build**

```bash
cd template-deploy && python3 build.py
```

Expected: output includes `✓ scrabble-word-finder.html` (or similar success line). No errors.

- [ ] **Step 2: Copy output to wordineer-deploy**

```bash
cp template-deploy/output/scrabble-word-finder.html wordineer-deploy/scrabble-word-finder.html
```

- [ ] **Step 3: Verify the output file has content**

```bash
grep -c 'swf-input' wordineer-deploy/scrabble-word-finder.html
```

Expected: `2` or more (appears in style and in the HTML input element).

- [ ] **Step 4: Start local preview server**

```bash
cd wordineer-deploy && python3 -m http.server 8080
```

- [ ] **Step 5: Manual smoke tests** (open http://localhost:8080/scrabble-word-finder.html)

Check each of the following:

1. **Page loads** — hero, input box, filter row, and Find Words button are all visible. No JS errors in console.
2. **Basic find** — type `aeirnt` and press Enter. Results table appears with words sorted by points (highest first). "train" (5 pts), "retain" (6 pts), "entrain" (7 pts), etc. should appear.
3. **Wildcard** — type `aeirnt?` and click Find Words. Results increase — more words now appear (blank tile opens up longer options).
4. **Sort toggle** — click "Length ↓". Table re-sorts so longer words appear first. Click "A–Z". Table re-sorts alphabetically. Click "Points ↓" to return to default.
5. **Filter: Starts with** — with `aeirnt` still in the input, type `r` in Starts with. Results narrow to only words beginning with 'r'. Clear the field — all results return.
6. **Filter: Min pts** — select "10+" from Min pts dropdown. Only words scoring 10+ appear.
7. **Filter: Length** — select "4–5" from Length dropdown. Only 4- and 5-letter words appear.
8. **Copy row** — click Copy on any word. Check clipboard (paste somewhere). Should paste just the word string.
9. **Copy all** — click "Copy all". Paste into a text editor — should be a newline-separated word list.
10. **Clear** — click ✕. Input clears, results disappear, count resets.
11. **Dictionary toggle** — click SOWPODS then WWF. Button highlights correctly. Results do not change (cosmetic toggle — expected behaviour; confirmed in FAQ).
12. **FAQ** — click a question. Answer expands. Click again. Answer collapses.
13. **Mobile** — resize browser to < 640px. Definition column disappears from table. Clicking a word cell toggles the expand row showing the definition below.
14. **Definition tooltip** — on desktop, hover over a word in the Word column. A dark tooltip appears with the word's definition (for words that have one in dictionary.json).
15. **No words found** — type `zzzzz` and click Find Words. Empty state message appears: "No words found — try removing a filter or adding a wildcard (?)."

- [ ] **Step 6: Commit final build output**

```bash
git add wordineer-deploy/scrabble-word-finder.html
git commit -m "feat: add scrabble-word-finder page (build output)"
```

---

## Self-Review Checklist

**Spec coverage:**
- ✅ `/scrabble-word-finder/` URL — Task 1 CONFIG + Task 5 _redirects
- ✅ Letter input up to 15 chars, `?` wildcard — Task 2 input, Task 4 `parseInput`
- ✅ Results table: word | length | points | definition | copy — Task 2, Task 4 `renderTable`
- ✅ Default sort: points descending — Task 4 `sortResults`, `currentSort = 'pts'`
- ✅ Sort toggle: Points ↓ / Length ↓ / A–Z — Task 2 sort bar, Task 4 sort buttons handler
- ✅ Definition tooltip (desktop hover) — Task 1 `.swf-tooltip` CSS + Task 4 `renderTable` inline tooltip span
- ✅ Definition expand row (mobile tap) — Task 1 responsive CSS + Task 4 word-cell click handler
- ✅ Filters: length, min pts, starts with, ends with, must contain — Task 2, Task 4 `applyFilters`
- ✅ Dictionary toggle (cosmetic) — Task 2 dict toggle buttons, Task 4 handler (no data change, as specified)
- ✅ Copy per row + Copy all — Task 4 `copyText`, row and bulk handlers
- ✅ Deferred data load (idle + focus early trigger) — Task 4 `scheduleDictLoad` + focus listener
- ✅ Data: dictionary.json + words_expanded.json merged — Task 4 `loadDict` with two `ingest()` calls
- ✅ words_expanded entries lowercased (words have capital first letter in source) — Task 4 `parseEntry`
- ✅ FAQ accordion (JS div pattern, not details/summary) — Task 3 faq slot, Task 4 FAQ handler
- ✅ First FAQ item has class `open` — Task 3 first `.faq-item` has `open`
- ✅ Every `.faq-q` has chevron SVG — Task 3 all faq-q elements include the SVG
- ✅ Explainer section with internal links to Word Unscramble, Word Lists — Task 3 explainer
- ✅ tools.json `more_word_tools` + `footer_cols` — Task 5
- ✅ `_redirects` clean URL rules — Task 5
- ✅ SEO: title, description, canonical, OG tags, WebApplication schema, FAQPage schema, breadcrumb — Task 1 meta slot
- ✅ Empty state message — Task 2 `#swf-empty` div, Task 4 `renderTable`
- ✅ Loading state ("Loading dictionary…") — Task 4 `find()` when `!dictLoaded`

# Random Wordle Generator Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build `/random-wordle-generator/` — a clean 5-letter word generator for Wordle players, with difficulty + starting-letter filters, definitions, and 1,300+ words of SEO copy.

**Architecture:** New `tools-src/random-wordle-generator.html` using the same split-panel tool pattern as `random-5-letter-word-generator.html`. Data source is the existing `/data/five-letter-words.json` (fetched at idle; SEED provides instant first render). Tools.json and _redirects updated for nav + clean URL.

**Tech Stack:** Vanilla JS (ES5), HTML/CSS, Wordineer build system (`template-deploy/build.py`), Cloudflare Pages via `_redirects`.

---

## File Map

| Action | File |
|---|---|
| **Create** | `template-deploy/tools-src/random-wordle-generator.html` |
| **Modify** | `template-deploy/tools.json` |
| **Modify** | `template-deploy/tools-src/word-tools.html` |
| **Modify** | `wordineer-deploy/_redirects` |
| Build artifact | `template-deploy/output/random-wordle-generator.html` → `wordineer-deploy/` |

**Key reference files (read-only):**
- `template-deploy/tools-src/random-5-letter-word-generator.html` — JS pattern, SEED format, ctrl panel, copy dropdown, init script
- `template-deploy/tools-src/random-weird-words.html` — style block, breadcrumb, tool-split layout, saved-section
- `template-deploy/tools.json` — JSON structure for mega, more_word_tools, footer_cols
- `wordineer-deploy/_redirects` — redirect format

---

## Task 1: Register tool in tools.json

**Files:**
- Modify: `template-deploy/tools.json`

- [ ] **Step 1: Open tools.json and locate the three target arrays**

  File: `template-deploy/tools.json`

  - `"mega"` → `"Writing & Vocabulary"` category → `"tools"` array
  - `"more_word_tools"` array
  - `"footer_cols"` → `"Writing & Vocabulary"` column → `"links"` array

- [ ] **Step 2: Add entry to mega → Writing & Vocabulary → tools**

  Insert after the last existing tool in that tools array (before the closing `]` of the `"tools"` key):
  ```json
  {
    "href": "/random-wordle-generator/",
    "text": "Random Wordle Generator"
  }
  ```

- [ ] **Step 3: Add entry to more_word_tools**

  Insert as the first item in the `"more_word_tools"` array (it will appear in the tools grid):
  ```json
  {
    "href": "/random-wordle-generator/",
    "name": "Random Wordle Generator",
    "desc": "Random 5-letter words for Wordle. Filter by difficulty and letter.",
    "icon_bg": "#E8F4FE",
    "icon_path": "<rect x='2' y='2' width='3.5' height='3.5' rx='0.5' fill='#2B7FD4'/><rect x='7.5' y='2' width='3.5' height='3.5' rx='0.5' fill='#2B7FD4' opacity='.4'/><rect x='2' y='7.5' width='3.5' height='3.5' rx='0.5' fill='#2B7FD4' opacity='.4'/><rect x='7.5' y='7.5' width='3.5' height='3.5' rx='0.5' fill='#2B7FD4'/>"
  }
  ```

- [ ] **Step 4: Add entry to footer_cols → Writing & Vocabulary → links**

  Insert after the last entry in the Writing & Vocabulary links array:
  ```json
  {
    "href": "/random-wordle-generator/",
    "text": "Random Wordle Generator"
  }
  ```

- [ ] **Step 5: Validate JSON**

  ```bash
  python3 -c "import json; json.load(open('template-deploy/tools.json')); print('OK')"
  ```
  Expected: `OK`

- [ ] **Step 6: Commit**

  ```bash
  git add template-deploy/tools.json
  git commit -m "feat: register random-wordle-generator in tools.json (mega, grid, footer)"
  ```

---

## Task 2: Add clean URL redirect

**Files:**
- Modify: `wordineer-deploy/_redirects`

- [ ] **Step 1: Open _redirects and locate the "Clean URLs" section**

  File: `wordineer-deploy/_redirects`
  Look for the block of `/tool-name/ /tool-name.html 200` rules.

- [ ] **Step 2: Add the redirect rule**

  Append to the clean URL block (maintain alphabetical order near other `r` tools):
  ```
  /random-wordle-generator/ /random-wordle-generator.html 200
  ```

- [ ] **Step 3: Commit**

  ```bash
  git add wordineer-deploy/_redirects
  git commit -m "feat: add clean URL redirect for random-wordle-generator"
  ```

---

## Task 3: Add link in word-tools.html

**Files:**
- Modify: `template-deploy/tools-src/word-tools.html`

- [ ] **Step 1: Locate the "Random word generators" section**

  File: `template-deploy/tools-src/word-tools.html`
  Search for the section containing `<h2 class="section-title">Random word generators</h2>`.
  Find the last `<a class="tool-item"` in that section (currently ends with the adverb/verb generators block).

- [ ] **Step 2: Insert the new tool-item card**

  Insert this block after the last existing `tool-item` in the "Random word generators" section and before the closing `</div>` of that section's `tools-grid`:

  ```html
  <a class="tool-item" href="/random-wordle-generator/">
    <div class="tool-icon" style="background:#E8F4FE"><svg viewBox="0 0 13 13" fill="none"><rect x="2" y="2" width="3.5" height="3.5" rx="0.5" fill="#2B7FD4"/><rect x="7.5" y="2" width="3.5" height="3.5" rx="0.5" fill="#2B7FD4" opacity=".4"/><rect x="2" y="7.5" width="3.5" height="3.5" rx="0.5" fill="#2B7FD4" opacity=".4"/><rect x="7.5" y="7.5" width="3.5" height="3.5" rx="0.5" fill="#2B7FD4"/></svg></div>
    <div class="tool-name">Random Wordle Generator</div>
    <div class="tool-desc">Random 5-letter words for Wordle practice. Filter by difficulty and starting letter.</div>
  </a>
  ```

- [ ] **Step 3: Update the JSON-LD ItemList in the meta slot**

  Find the `"itemListElement"` array in the `<script type="application/ld+json">` block at the top of word-tools.html. Add a new entry with the next available position number:
  ```json
  { "@type": "ListItem", "position": 17, "name": "Random Wordle Generator", "url": "https://wordineer.com/random-wordle-generator/" }
  ```
  (Use whatever position number follows the current last entry — check the existing list to confirm.)

- [ ] **Step 4: Commit**

  ```bash
  git add template-deploy/tools-src/word-tools.html
  git commit -m "feat: add Random Wordle Generator link to word-tools hub"
  ```

---

## Task 4: Create the tool source file — meta + style + hero slots

**Files:**
- Create: `template-deploy/tools-src/random-wordle-generator.html`

- [ ] **Step 1: Create the file with CONFIG + meta slot**

  Create `template-deploy/tools-src/random-wordle-generator.html` with this content (replace entire file):

  ```html
  <!-- CONFIG
  {
    "url": "/random-wordle-generator/",
    "output": "random-wordle-generator.html"
  }
  -->

  <!-- SLOT:meta -->
  <title>Random Wordle Word Generator — 5-Letter Words | Wordineer</title>
  <meta name="description" content="Generate random 5-letter words for Wordle. Filter by difficulty and starting letter. Free, instant, no sign-up.">
  <link rel="canonical" href="https://wordineer.com/random-wordle-generator/">
  <meta property="og:type"        content="website">
  <meta property="og:site_name"   content="Wordineer">
  <meta property="og:title"       content="Random Wordle Word Generator | Wordineer">
  <meta property="og:description" content="Generate random 5-letter words for Wordle practice. Filter by difficulty and starting letter. Free, instant.">
  <meta property="og:url"         content="https://wordineer.com/random-wordle-generator/">
  <meta property="og:image"       content="https://wordineer.com/og-image.png">
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
      {
        "@type": "Question",
        "name": "What makes a good Wordle word?",
        "acceptedAnswer": { "@type": "Answer", "text": "A good Wordle word covers high-frequency letters — E, T, A, R, I, O, N, S, L, C — without repeating letters. Words like CRANE, SLATE, TRACE, and STARE are popular starting words because they hit multiple vowels and common consonants in one guess. Avoid words with rare letters (Q, X, Z, J) or repeated letters for your first guess." }
      },
      {
        "@type": "Question",
        "name": "Can I use any 5-letter word in Wordle?",
        "acceptedAnswer": { "@type": "Answer", "text": "No — Wordle uses a specific word list. Not every 5-letter English word is a valid guess. This generator draws from a broad curated dataset of common and uncommon English words. Most results will be valid Wordle guesses, but obscure or archaic words may not appear in Wordle's accepted list." }
      },
      {
        "@type": "Question",
        "name": "What's the difference between easy and hard words in this tool?",
        "acceptedAnswer": { "@type": "Answer", "text": "Easy words are common everyday vocabulary most people know — CRANE, BEACH, LIGHT. Medium words are less frequent but widely understood. Hard words are rare, technical, or archaic — PSALM, FJORD, THYME. For Wordle practice, use Easy to build fluency. Use Hard if you want words that are more likely to stump an opponent." }
      },
      {
        "@type": "Question",
        "name": "How many 5-letter words are in this generator?",
        "acceptedAnswer": { "@type": "Answer", "text": "The generator draws from thousands of curated 5-letter English words across three difficulty levels. The standard Wordle answer list has around 2,300 words; the valid-guess list has over 10,000. This tool covers a broad cross-section of both common and rare 5-letter words." }
      },
      {
        "@type": "Question",
        "name": "What is the best Wordle starting strategy?",
        "acceptedAnswer": { "@type": "Answer", "text": "Cover as many of the 12 most common English letters as possible in your first two guesses. Pairing CRANE + TOILS, for example, covers 10 of those 12 letters. Use this generator to rotate your starting word — using the same word every day trains you to pattern-match to that word's positions rather than the actual puzzle." }
      }
    ]
  }
  </script>

  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      { "@type": "ListItem", "position": 1, "name": "Wordineer", "item": "https://wordineer.com/" },
      { "@type": "ListItem", "position": 2, "name": "Word Tools", "item": "https://wordineer.com/word-tools/" },
      { "@type": "ListItem", "position": 3, "name": "Random Wordle Generator", "item": "https://wordineer.com/random-wordle-generator/" }
    ]
  }
  </script>

  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "WebApplication",
    "name": "Random Wordle Word Generator",
    "url": "https://wordineer.com/random-wordle-generator/",
    "description": "Generate random 5-letter words for Wordle practice. Filter by difficulty and starting letter.",
    "applicationCategory": "UtilityApplication",
    "operatingSystem": "Web",
    "offers": { "@type": "Offer", "price": "0", "priceCurrency": "USD" },
    "publisher": { "@id": "https://wordineer.com/#organization" }
  }
  </script>
  <!-- /SLOT:meta -->
  ```

- [ ] **Step 2: Append the style slot**

  Append to the same file (model exactly on `random-5-letter-word-generator.html` style block — copy the full `.tool-wrap`, `.tool-card`, `.tool-split`, `.ctrl`, `.words-panel`, `.word-item`, `.word-text`, `.word-def`, `.badge-*`, `.copy-dropdown`, `.act-btn`, `.gen-btn`, `.reset-btn`, `.kbd`, `.ad-sidebar`, `.saved-section`, and media query rules).

  The style block is identical to `random-5-letter-word-generator.html` SLOT:style — copy it verbatim from that file (lines ~73–296). This avoids drift.

  ```html
  <!-- SLOT:style -->
  <!-- [copy verbatim from random-5-letter-word-generator.html SLOT:style] -->
  <!-- /SLOT:style -->
  ```

  > **Important:** Open `random-5-letter-word-generator.html`, find `<!-- SLOT:style -->`, copy everything between that tag and `<!-- /SLOT:style -->`, paste here.

- [ ] **Step 3: Append the hero slot with breadcrumb**

  Append to the file:

  ```html
  <!-- SLOT:hero -->
  <div class="breadcrumb">
    <div class="breadcrumb-inner">
      <a href="/">Wordineer</a>
      <span class="breadcrumb-sep">›</span>
      <a href="/word-tools/">Word Tools</a>
      <span class="breadcrumb-sep">›</span>
      <span aria-current="page">Random Wordle Generator</span>
    </div>
  </div>
  <div class="hero">
    <div class="hero-badge">
      <svg viewBox="0 0 11 11" fill="none"><circle cx="5.5" cy="5.5" r="4.5" stroke="#3C3489" stroke-width="1"/><path d="M3.5 5.5l1.5 1.5L8 3.5" stroke="#3C3489" stroke-width="1.2" stroke-linecap="round"/></svg>
      Free · No sign-up · Instant results
    </div>
    <h1>Random Wordle Word Generator</h1>
    <p>Generate random 5-letter words for Wordle practice. Filter by difficulty and starting letter to find exactly the kind of word you need.</p>
  </div>
  <!-- /SLOT:hero -->
  ```

- [ ] **Step 4: Commit checkpoint**

  ```bash
  git add template-deploy/tools-src/random-wordle-generator.html
  git commit -m "feat: add random-wordle-generator meta + style + hero slots"
  ```

---

## Task 5: Add the tool slot (controls + results panel)

**Files:**
- Modify: `template-deploy/tools-src/random-wordle-generator.html`

- [ ] **Step 1: Append the tool slot**

  Append to the file. This is a simplified version of the 5-letter generator — no type filter, no ends-with, no contains/excludes, no saved-words, no Wordle-helper accordion:

  ```html
  <!-- SLOT:tool -->
  <div class="tool-wrap">
    <div class="tool-card">
      <div class="tool-split">

        <div class="ctrl">
          <div class="ctrl-row">
            <label class="ctrl-label" for="ctrl-count">Number of words</label>
            <input type="number" id="ctrl-count" value="5" min="1" max="10" inputmode="numeric" aria-describedby="count-error">
            <span class="count-error" id="count-error">Enter a number from 1 to 10</span>
          </div>

          <button type="button" class="mobile-more-toggle" id="mobile-more-toggle" aria-expanded="false" aria-controls="advanced-options">More options</button>

          <div class="advanced-options" id="advanced-options">
            <div class="ctrl-row">
              <label class="ctrl-label" for="ctrl-diff">Difficulty</label>
              <select id="ctrl-diff">
                <option value="all">All levels</option>
                <option value="easy">Easy (common)</option>
                <option value="medium">Medium</option>
                <option value="hard">Hard / rare</option>
              </select>
            </div>
            <div class="ctrl-row">
              <label class="ctrl-label" for="ctrl-first">Starts with letter</label>
              <input type="text" id="ctrl-first" maxlength="1" placeholder="Any" aria-label="Starts with letter">
            </div>
          </div>

          <button class="gen-btn" id="word-gen-btn">Generate words</button>
          <button class="reset-btn" id="word-reset-btn">Reset options</button>
          <div class="kbd">Press <kbd>Space</kbd> to regenerate</div>

          <div class="ad-sidebar">
            <span class="ad-sidebar-tag">Ad</span>
            <div class="ad-sidebar-logo">
              <svg viewBox="0 0 32 32" fill="none" width="32" height="32"><circle cx="16" cy="16" r="14" fill="#FF7043"/><path d="M10 16c0-3.3 2.7-6 6-6s6 2.7 6 6" stroke="white" stroke-width="2" stroke-linecap="round"/><circle cx="16" cy="16" r="2.5" fill="white"/></svg>
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
              <div class="copy-dropdown">
                <button class="act-btn" id="copy-all-btn">Copy list ▾</button>
                <div class="copy-menu" id="copy-menu">
                  <button data-fmt="line">One per line</button>
                  <button data-fmt="comma">Comma-separated</button>
                  <button data-fmt="space">Space-separated</button>
                </div>
              </div>
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

- [ ] **Step 2: Commit checkpoint**

  ```bash
  git add template-deploy/tools-src/random-wordle-generator.html
  git commit -m "feat: add tool slot (controls + results panel) to random-wordle-generator"
  ```

---

## Task 6: Add the ad_b, explainer, faq, and who slots

**Files:**
- Modify: `template-deploy/tools-src/random-wordle-generator.html`

- [ ] **Step 1: Append the ad_b slot (empty — keeps template happy)**

  ```html
  <!-- SLOT:ad_b -->
  <!-- /SLOT:ad_b -->
  ```

- [ ] **Step 2: Append the explainer slot (~900 words of body copy)**

  ```html
  <!-- SLOT:explainer -->
  <div class="explainer">

    <h2>What is a Random Wordle Generator?</h2>
    <p>A random Wordle generator is a tool that picks valid 5-letter English words on demand. Unlike playing Wordle itself — where the puzzle gives you a hidden word to guess — this tool works in the opposite direction: it gives you a pool of random 5-letter words that you can use as starting guesses, practice material, or inspiration before your daily puzzle. Each result comes with a definition so you can actually learn the word, not just stare at five letters.</p>
    <p>The generator draws from a curated dataset of thousands of 5-letter English words across three difficulty levels. Easy words are everyday vocabulary. Medium words are less common but recognisable. Hard words are rare, technical, or archaic — the kind that make Wordle feel brutal when they show up as the answer. You can also filter by starting letter, which is useful when you want to explore a specific part of the alphabet or practice words that begin with a tricky letter like Q or X.</p>
    <p>The tool runs entirely in your browser — no account, no install, no waiting. Click Generate and the results appear instantly. Click again for a fresh batch.</p>

    <h2>Why Use a Random Wordle Generator?</h2>
    <p>Most regular Wordle players develop a small repertoire of starting words — CRANE, STARE, SLATE, IRATE — and use the same two or three every single day. That works, but it creates a habit of pattern-matching to specific letter positions rather than thinking about the puzzle fresh. Rotating your starting word, even occasionally, sharpens the underlying skill: letter frequency awareness and deductive reasoning from colour feedback.</p>
    <p>This generator makes it easy to find a new starting word. Generate a batch, pick one you haven't used before, and see how differently the puzzle unfolds. You might find a word like AUDIO — only one consonant, four vowels — reveals a lot about vowel placement quickly. Or THUMP, which tests less common consonant clusters. Neither is obviously better than CRANE, but each pushes you to think differently.</p>
    <p>There are other reasons to use it beyond Wordle itself. Teachers use 5-letter word generators for spelling activities and vocabulary exercises — five letters is short enough to be manageable and long enough to involve real spelling decisions. Writers use random word generators as creative constraints: pick a 5-letter word you've never used and work it into today's writing. Vocabulary learners set the difficulty to Hard and challenge themselves to define each word before checking. The definition is right there in the result, so the feedback loop is immediate.</p>

    <h2>How This Tool Works</h2>
    <p>The generator filters a curated word dataset to 5-letter words, then picks randomly from whatever matches your filters. Difficulty is tagged on each word: easy words appear in everyday conversation, medium words are less frequent, and hard words are uncommon enough that most people would need to look them up. The starting-letter filter runs before random selection, so if you pick S, you'll only see 5-letter words beginning with S.</p>
    <p>On first load, a small set of seed words renders immediately so the tool is usable before any data has been fetched. The full word list loads in the background at browser idle — this keeps the page fast without sacrificing word variety. Once loaded, you have access to thousands of words across all difficulty levels.</p>

    <h2>How Does Wordle Work? A Quick Refresher</h2>
    <p>Wordle gives you a hidden 5-letter word and six attempts to guess it. Each guess must be a real word. After each guess, the tiles change colour: green means the letter is correct and in the right position; yellow means the letter is in the word but in the wrong position; grey means the letter is not in the word at all. You use the colour feedback to narrow down possibilities with each guess.</p>
    <p>The game originated as a once-a-day puzzle and went viral because of its social sharing format — posting your coloured grid without spoiling the word. Unlimited and variant versions now exist (Quordle for four simultaneous puzzles, Octordle for eight), but all of them use the same core logic: 5-letter words, colour-coded feedback, eliminate and confirm letters across guesses.</p>
    <p>Your starting word matters more than it might seem. A weak opener — say, ZZYZX — eliminates no useful letters. A strong opener like CRANE or SLATE immediately narrows the field by testing five different common letters at once. That's where this generator helps: the more variety in your starting words, the better you understand what makes one guess more informative than another.</p>

    <h2>Best Starting Words for Wordle</h2>
    <p>The most effective Wordle starting words share a few properties: they contain no repeated letters, they cover multiple vowels, and they use high-frequency consonants (R, S, T, L, N). Here are some of the most commonly recommended starters and what makes each useful:</p>
    <ul>
      <li><strong>CRANE</strong> — covers C, R, A, N, E. Two vowels, three common consonants. Arguably the most popular opener.</li>
      <li><strong>SLATE</strong> — S, L, A, T, E. Hits the S and T which appear in a huge portion of Wordle answers.</li>
      <li><strong>TRACE</strong> — T, R, A, C, E. Overlaps with CRANE in usefulness; strong vowel coverage.</li>
      <li><strong>STARE</strong> — S, T, A, R, E. Covers the same high-frequency letters from a different angle.</li>
      <li><strong>AUDIO</strong> — four vowels in one word. Useful if you want to map vowel positions immediately, accepting that consonant coverage will be weak.</li>
      <li><strong>RAISE</strong> — R, A, I, S, E. Three vowels plus common consonants. A favourite among players who prioritise vowel elimination first.</li>
    </ul>
    <p>No single word is universally "best" — information value depends on the hidden word. What matters more is varying your opener over time. Use this generator to build a rotation of 8–10 starting words you feel comfortable with, and cycle through them. You'll stop guessing on autopilot and start thinking about each puzzle as its own problem.</p>

    <h2>Best Practices</h2>
    <p>Generate 5 words at once and pick the one that feels right for today. The count filter defaults to 5 for this reason — a small batch gives you choice without overwhelming the screen. If you want more variety, bump the count to 10.</p>
    <p>Use the difficulty filter to match your goal. Easy gives you Wordle-friendly common words. Hard gives you the kind of words that appear in advanced Wordle puzzles and catch players off guard. If you want to practice handling an unusual answer, generating Hard words and trying to define them before looking is a useful exercise.</p>
    <p>The starting-letter filter is useful for targeted practice. If you always struggle with words beginning with W or Y, filter to that letter and spend a session on those words specifically. Same for any letter cluster you find tricky in your guesses.</p>
    <p>Use the tool as a warm-up, not as a cheat. The generator doesn't know today's Wordle answer — it just supplies random words. The point is to get your brain thinking about 5-letter words and letter distributions before you open the puzzle.</p>

  </div>
  <!-- /SLOT:explainer -->
  ```

- [ ] **Step 3: Append the faq slot**

  ```html
  <!-- SLOT:faq -->
  <div class="faq-section">
    <h2>Frequently asked questions</h2>

    <details class="faq-item">
      <summary>What makes a good Wordle starting word?</summary>
      <p>A strong starting word covers high-frequency letters without repeating any of them. The letters E, T, A, R, I, O, N, S, L, and C appear in the largest share of English 5-letter words. A word like CRANE or SLATE hits five of these in one guess, giving you maximum colour-feedback information on the first turn. Avoid starting words with Q, X, Z, or J — these appear rarely enough that guessing them first wastes an attempt.</p>
    </details>

    <details class="faq-item">
      <summary>Can I use any 5-letter word as a Wordle guess?</summary>
      <p>No. Wordle maintains a list of valid guesses, and not every 5-letter English word is on it. Very obscure, archaic, or technical words often aren't accepted. This generator draws from a broad curated English word dataset — most results will be valid Wordle guesses, but unusual words may be rejected by the game. If a word isn't accepted, generate another and try again.</p>
    </details>

    <details class="faq-item">
      <summary>What's the difference between easy, medium, and hard difficulty here?</summary>
      <p>Easy words are common everyday vocabulary — the kind you'd see in news articles or casual conversation. Medium words are less frequent but broadly understood. Hard words are uncommon, specialised, or archaic — words most people would need to look up. For Wordle warm-up and practice, Easy is the right setting. If you want to prepare for the toughest possible answers, or build vocabulary at the same time as playing, use Hard.</p>
    </details>

    <details class="faq-item">
      <summary>How many 5-letter words are there in English?</summary>
      <p>Tens of thousands, depending on how you count dialects, technical terms, and archaisms. The standard Wordle answer list (words that can appear as the hidden answer) has around 2,300 words. The extended valid-guess list (words you can type as a guess but that won't appear as the answer) adds several thousand more. This generator covers a broad cross-section of both lists, from everyday words to rare vocabulary.</p>
    </details>

    <details class="faq-item">
      <summary>What's the single best Wordle strategy beyond the opening word?</summary>
      <p>After your opener, your second guess should cover as many unchecked common letters as possible — don't reuse letters you already have information on, whether green, yellow, or grey. Cover new ground. Experienced players use two planned openers (like CRANE + TOILS) to test 10 common letters in two guesses before making deductive moves. From guess three onward, use what you know: confirmed positions, confirmed letters in wrong positions, and eliminated letters, to narrow to the correct word.</p>
    </details>
  </div>
  <!-- /SLOT:faq -->
  ```

- [ ] **Step 4: Append the who slot**

  ```html
  <!-- SLOT:who -->
  <div class="who-section">
    <h3>Who uses this tool</h3>
    <div class="use-cases">
      <div class="use-case-card">
        <h3>Daily Wordle players</h3>
        <p>Rotate your starting word instead of using the same opener every day. A fresh starting word breaks the habit of pattern-matching to specific positions and keeps the puzzle genuinely challenging.</p>
      </div>
      <div class="use-case-card">
        <h3>Teachers and students</h3>
        <p>5-letter words are the right length for spelling exercises and vocabulary drills. Filter to Easy for primary classes, Hard for advanced learners. Every result includes a definition — no dictionary lookup needed.</p>
      </div>
      <div class="use-case-card">
        <h3>Word game enthusiasts</h3>
        <p>Quordle, Dordle, Octordle, and every Wordle variant use 5-letter words. Generate a batch of starting words, pick four for your Quordle opener, and test each grid simultaneously.</p>
      </div>
      <div class="use-case-card">
        <h3>Writers and creatives</h3>
        <p>Use a random 5-letter word as a writing constraint, a character name seed, or a story prompt. The shorter the word, the harder it is to ignore — five letters forces you to work with something concrete.</p>
      </div>
    </div>
  </div>
  <!-- /SLOT:who -->
  ```

- [ ] **Step 5: Commit checkpoint**

  ```bash
  git add template-deploy/tools-src/random-wordle-generator.html
  git commit -m "feat: add ad_b + explainer + faq + who slots to random-wordle-generator"
  ```

---

## Task 7: Add the init slot (JavaScript)

**Files:**
- Modify: `template-deploy/tools-src/random-wordle-generator.html`

- [ ] **Step 1: Append the init slot**

  Append to the file. This is a trimmed version of the 5-letter generator's init script — same SEED format, same `loadFull` / `renderList` / `buildWordItem` / `pickRandom` pattern, but without: type filter, ends-with filter, contains/excludes filters, saved-words, Wordle-helper accordion, or definitions toggle (definitions are always shown).

  ```html
  <!-- SLOT:init -->
  <script>
  (function () {
    var SEED = [
      {w:"Crane",t:"noun",d:"a large wading bird with a long neck and legs",diff:"easy"},
      {w:"Slate",t:"noun",d:"a fine-grained rock easily split into smooth flat plates",diff:"easy"},
      {w:"Trace",t:"verb",d:"to follow the course or trail of something",diff:"easy"},
      {w:"Stare",t:"verb",d:"to look steadily and intently at something",diff:"easy"},
      {w:"Raise",t:"verb",d:"to lift or move to a higher position",diff:"easy"},
      {w:"Brave",t:"adjective",d:"ready to face danger without fear",diff:"easy"},
      {w:"Flame",t:"noun",d:"a hot glowing body of burning gas",diff:"easy"},
      {w:"Groan",t:"verb",d:"to make a deep sound expressing pain or despair",diff:"easy"},
      {w:"Plumb",t:"verb",d:"to measure or test the depth of something",diff:"medium"},
      {w:"Crypt",t:"noun",d:"an underground room or vault beneath a church",diff:"medium"},
      {w:"Askew",t:"adjective",d:"not in a straight or level position; crooked",diff:"medium"},
      {w:"Pivot",t:"verb",d:"to turn on or as if on a central point",diff:"medium"},
      {w:"Blunt",t:"adjective",d:"having a dull edge; direct in speech",diff:"easy"},
      {w:"Quirk",t:"noun",d:"a peculiar behavioural habit or trait",diff:"medium"},
      {w:"Fjord",t:"noun",d:"a long narrow sea inlet between high cliffs",diff:"hard"}
    ];

    var COPY_SVG = '<svg viewBox="0 0 14 14" fill="none"><rect x="4" y="4" width="8" height="8" rx="1.5" stroke="currentColor" stroke-width="1.3"/><path d="M2 10V2h8" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/></svg>';

    var allWords    = SEED.slice();
    var currentWords = [];
    var fullLoaded  = false;

    function diffBadge(d) {
      return d === 'easy' ? 'badge-easy' : d === 'medium' ? 'badge-medium' : 'badge-hard';
    }

    function buildWordItem(w) {
      return '<li class="word-item">' +
        '<div class="word-left">' +
          '<div class="word-text">' + w.w + '</div>' +
          '<div class="word-badges">' +
            '<span class="badge ' + diffBadge(w.diff) + '">' + w.diff + '</span>' +
          '</div>' +
          (w.d ? '<div class="word-def">' + w.d + '</div>' : '') +
        '</div>' +
        '<div class="word-right">' +
          '<button class="icon-btn" onclick="copyWord(this,\'' + w.w + '\')" aria-label="Copy ' + w.w + '">' + COPY_SVG + '</button>' +
        '</div>' +
      '</li>';
    }

    window.copyWord = function (btn, word) {
      navigator.clipboard.writeText(word).then(function () {
        btn.innerHTML = '✓';
        setTimeout(function () { btn.innerHTML = COPY_SVG; }, 1000);
      });
    };

    function pickRandom(pool, n) {
      var copy = pool.slice();
      var result = [];
      while (result.length < n && copy.length) {
        var i = Math.floor(Math.random() * copy.length);
        result.push(copy.splice(i, 1)[0]);
      }
      return result;
    }

    function filterWords() {
      var diff  = document.getElementById('ctrl-diff').value;
      var first = (document.getElementById('ctrl-first').value || '').toUpperCase();
      return allWords.filter(function (w) {
        if (diff !== 'all' && w.diff !== diff) return false;
        if (first && w.w.toUpperCase()[0] !== first) return false;
        return true;
      });
    }

    function renderList() {
      var raw = parseInt(document.getElementById('ctrl-count').value, 10);
      var n   = (isNaN(raw) || raw < 1 || raw > 10) ? 5 : raw;
      var pool = filterWords();
      currentWords = pickRandom(pool, n);
      var list = document.getElementById('word-list');
      var countEl = document.getElementById('word-count');
      if (currentWords.length === 0) {
        list.innerHTML = '<li class="word-item"><div class="word-left"><div class="word-def">No words match your filters. Try adjusting difficulty or starting letter.</div></div></li>';
        countEl.textContent = '0 words';
        return;
      }
      list.innerHTML = currentWords.map(buildWordItem).join('');
      countEl.textContent = currentWords.length + ' word' + (currentWords.length === 1 ? '' : 's');
    }

    function loadFull() {
      if (fullLoaded) return;
      fullLoaded = true;
      fetch('/data/five-letter-words.json')
        .then(function (r) { return r.json(); })
        .then(function (data) { allWords = data; renderList(); })
        .catch(function () {});
    }

    function validateAndGenerate() {
      var raw = parseInt(document.getElementById('ctrl-count').value, 10);
      var err = document.getElementById('count-error');
      var inp = document.getElementById('ctrl-count');
      if (isNaN(raw) || raw < 1 || raw > 10) {
        err.classList.add('show'); inp.classList.add('input-error'); return;
      }
      err.classList.remove('show'); inp.classList.remove('input-error');
      renderList();
    }

    // Generate / regenerate buttons
    document.getElementById('word-gen-btn').addEventListener('click', function () { loadFull(); validateAndGenerate(); });
    document.getElementById('word-regen-btn').addEventListener('click', function () { loadFull(); validateAndGenerate(); });

    // Real-time filter updates on select change
    document.getElementById('ctrl-diff').addEventListener('change', function () { loadFull(); renderList(); });
    document.getElementById('ctrl-first').addEventListener('input', function () { loadFull(); renderList(); });

    // Copy-all dropdown
    var copyBtn  = document.getElementById('copy-all-btn');
    var copyMenu = document.getElementById('copy-menu');
    copyBtn.addEventListener('click', function (e) { e.stopPropagation(); copyMenu.classList.toggle('open'); });
    document.addEventListener('click', function () { copyMenu.classList.remove('open'); });
    copyMenu.querySelectorAll('button').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var fmt   = btn.getAttribute('data-fmt');
        var words = currentWords.map(function (w) { return w.w; });
        var text  = fmt === 'comma' ? words.join(', ') : fmt === 'space' ? words.join(' ') : words.join('\n');
        navigator.clipboard.writeText(text).then(function () {
          copyBtn.textContent = 'Copied! ✓';
          setTimeout(function () { copyBtn.textContent = 'Copy list ▾'; }, 1500);
        });
        copyMenu.classList.remove('open');
      });
    });

    // Reset
    document.getElementById('word-reset-btn').addEventListener('click', function () {
      document.getElementById('ctrl-diff').value  = 'all';
      document.getElementById('ctrl-first').value = '';
      document.getElementById('ctrl-count').value = 5;
      document.getElementById('count-error').classList.remove('show');
      document.getElementById('ctrl-count').classList.remove('input-error');
      renderList();
    });

    // Space to regenerate
    document.addEventListener('keydown', function (e) {
      if (e.code === 'Space' && e.target === document.body) {
        e.preventDefault(); loadFull(); validateAndGenerate();
      }
    });

    // Mobile toggle
    var mobileToggle = document.getElementById('mobile-more-toggle');
    var advanced     = document.getElementById('advanced-options');
    if (mobileToggle && advanced) {
      mobileToggle.addEventListener('click', function () {
        var open = advanced.classList.toggle('is-open');
        mobileToggle.setAttribute('aria-expanded', open ? 'true' : 'false');
        mobileToggle.textContent = open ? 'Hide options' : 'More options';
      });
    }

    // Initial render then load full at idle
    renderList();
    if ('requestIdleCallback' in window) {
      requestIdleCallback(loadFull);
    } else {
      setTimeout(loadFull, 800);
    }
  })();
  </script>
  <!-- /SLOT:init -->
  ```

- [ ] **Step 2: Commit**

  ```bash
  git add template-deploy/tools-src/random-wordle-generator.html
  git commit -m "feat: add init slot (JavaScript) to random-wordle-generator"
  ```

---

## Task 8: Build, copy, and verify locally

**Files:**
- Build artifact: `template-deploy/output/random-wordle-generator.html`
- Copy to: `wordineer-deploy/random-wordle-generator.html`

- [ ] **Step 1: Run the build**

  ```bash
  cd "/Users/garrickdeetan/Documents/Random Word Generator Tool Site/template-deploy" && python3 build.py
  ```
  Expected: no errors; `output/random-wordle-generator.html` exists.

- [ ] **Step 2: Verify the output file exists and has content**

  ```bash
  wc -l "/Users/garrickdeetan/Documents/Random Word Generator Tool Site/template-deploy/output/random-wordle-generator.html"
  ```
  Expected: several hundred lines.

- [ ] **Step 3: Copy output to deploy folder**

  ```bash
  cp "/Users/garrickdeetan/Documents/Random Word Generator Tool Site/template-deploy/output/random-wordle-generator.html" "/Users/garrickdeetan/Documents/Random Word Generator Tool Site/wordineer-deploy/"
  ```

- [ ] **Step 4: Also rebuild word-tools (since we edited it)**

  ```bash
  cp "/Users/garrickdeetan/Documents/Random Word Generator Tool Site/template-deploy/output/word-tools.html" "/Users/garrickdeetan/Documents/Random Word Generator Tool Site/wordineer-deploy/"
  ```

- [ ] **Step 5: Start local preview server**

  ```bash
  cd "/Users/garrickdeetan/Documents/Random Word Generator Tool Site/wordineer-deploy" && python3 -m http.server 8080
  ```

- [ ] **Step 6: Verify tool in browser**

  Open `http://localhost:8080/random-wordle-generator.html` and confirm:
  - [ ] Breadcrumb shows: Wordineer › Word Tools › Random Wordle Generator
  - [ ] 5 seed words render immediately (before JSON loads)
  - [ ] Each word shows the word text + difficulty badge + definition
  - [ ] "Generate words" button fetches full list and regenerates
  - [ ] "Regenerate" button works
  - [ ] Difficulty filter changes results
  - [ ] Starts-with filter (e.g. type "S") filters to S-words only
  - [ ] Count field (change to 10) shows 10 words
  - [ ] "Copy list ▾" dropdown copies words in chosen format
  - [ ] Per-word copy icon copies the word and briefly shows ✓
  - [ ] Reset button clears all filters
  - [ ] Space key regenerates
  - [ ] Explainer and FAQ sections render below the tool
  - [ ] Mobile: stack layout works (test by resizing browser < 700px)
  - [ ] Open `http://localhost:8080/word-tools.html` — confirm new card appears in "Random word generators" section

- [ ] **Step 7: Commit final build artifacts**

  ```bash
  git add wordineer-deploy/random-wordle-generator.html wordineer-deploy/word-tools.html
  git commit -m "build: add random-wordle-generator.html and rebuild word-tools.html"
  ```

---

## Verification Checklist

- [ ] `python3 -c "import json; json.load(open('template-deploy/tools.json')); print('OK')"` → OK
- [ ] `grep -c "random-wordle-generator" wordineer-deploy/_redirects` → 1
- [ ] `grep -c "random-wordle-generator" template-deploy/tools-src/word-tools.html` → at least 1
- [ ] `grep -c "random-wordle-generator" template-deploy/tools.json` → at least 3 (mega + grid + footer)
- [ ] Tool renders seed words immediately on page load (no blank flash)
- [ ] Full word list loads at idle (open browser devtools → Network → verify `five-letter-words.json` fetch completes)
- [ ] No console errors

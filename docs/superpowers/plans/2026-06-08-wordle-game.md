# Wordle Game Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a playable Wordle game at `/wordle-game/` connected to the existing word generator via a Play icon on each result, discoverable from the Word Tools landing page.

**Architecture:** New `wordle-game.html` tool-src page with self-contained IIFE game logic; `random-wordle-generator.html` gets a Play icon + CSS tooltip per word; `word-tools.html` gets one new entry in the existing Word games section. Game reuses `/data/wordle-words.json`. No new data files, no new dependencies.

**Tech Stack:** Vanilla HTML/CSS/JS, same IIFE pattern as all other tool pages. Python build.py assembles tool-src → output. Cloudflare Pages deploys output.

---

## File Map

| Action | File |
|--------|------|
| Modify | `template-deploy/tools-src/random-wordle-generator.html` |
| Create | `template-deploy/tools-src/wordle-game.html` |
| Modify | `template-deploy/tools-src/word-tools.html` |
| Modify | `wordineer-deploy/_redirects` |
| Modify | `wordineer-deploy/sitemap.xml` |
| Build  | `cd template-deploy && python3 build.py` |
| Copy   | `cp template-deploy/output/*.html wordineer-deploy/` |

---

## Task 1: Add Play icon to random-wordle-generator.html

**Files:**
- Modify: `template-deploy/tools-src/random-wordle-generator.html`

- [ ] **Step 1: Add tooltip CSS to SLOT:style**

  In `<!-- SLOT:style -->`, add after the `.az-link:hover` rule (around line 181) before the `@media` block:

  ```css
  /* Play icon tooltip */
  .play-icon-wrap { position: relative; display: inline-flex; }
  .play-icon-wrap .play-tip {
    display: none; position: absolute; bottom: calc(100% + 6px); left: 50%;
    transform: translateX(-50%); white-space: nowrap; background: var(--text);
    color: var(--bg); font-size: 11px; font-weight: 500; padding: 4px 8px;
    border-radius: 5px; pointer-events: none; z-index: 10;
  }
  .play-icon-wrap:hover .play-tip { display: block; }
  ```

- [ ] **Step 2: Add PLAY_SVG constant in SLOT:init**

  In `<!-- SLOT:init -->`, after the `HEART_SVG_FILLED` line, add:

  ```javascript
  var PLAY_SVG = '<svg viewBox="0 0 14 14" fill="none"><polygon points="3.5,2 3.5,12 12,7" fill="currentColor"/></svg>';
  ```

- [ ] **Step 3: Add playWordle global function in SLOT:init**

  After the `window.copyWord` function block, add:

  ```javascript
  window.playWordle = function (word) {
    location.href = '/wordle-game/#' + btoa(word.toUpperCase());
  };
  ```

- [ ] **Step 4: Add play button to buildWordItem**

  In the `buildWordItem` function, find this line inside `word-right`:
  ```javascript
  '<button class="icon-btn" onclick="copyWord(this,\'' + w.w + '\')" aria-label="Copy ' + w.w + '">' + COPY_SVG + '</button>' +
  ```
  After that line (before the closing `</div>` of `word-right`), add:
  ```javascript
  '<div class="play-icon-wrap">' +
    '<button class="icon-btn" onclick="playWordle(\'' + w.w + '\')" aria-label="Play Wordle with ' + w.w + '">' + PLAY_SVG + '</button>' +
    '<span class="play-tip">Play Wordle with ' + w.w.toUpperCase() + '</span>' +
  '</div>' +
  ```

- [ ] **Step 5: Build and copy**

  ```bash
  cd template-deploy && python3 build.py
  cp template-deploy/output/random-wordle-generator.html wordineer-deploy/
  ```
  Expected: `Build complete` with no errors.

- [ ] **Step 6: Verify in browser**

  ```bash
  cd wordineer-deploy && python3 -m http.server 8080
  ```
  Open `http://localhost:8080/random-wordle-generator.html`. Hover over the ▶ icon on any word — tooltip "Play Wordle with CRANE" appears. Click it — navigates to `/wordle-game/#Q1JBTkU=` (404 expected until Task 3 is deployed).

- [ ] **Step 7: Commit**

  ```bash
  git add template-deploy/tools-src/random-wordle-generator.html wordineer-deploy/random-wordle-generator.html
  git commit -m "feat: add Play Wordle icon with tooltip to word generator results"
  ```

---

## Task 2: Create wordle-game.html — CONFIG, meta, style, hero, tool HTML

**Files:**
- Create: `template-deploy/tools-src/wordle-game.html`

- [ ] **Step 1: Create the file with CONFIG + meta slot**

  Create `template-deploy/tools-src/wordle-game.html` with this exact content (through the end of `<!-- /SLOT:meta -->`):

  ```html
  <!-- CONFIG
  {
    "url": "/wordle-game/",
    "output": "wordle-game.html",
    "type": "tool"
  }
  -->

  <!-- SLOT:meta -->
  <title>Play Wordle Free — Unlimited Wordle Game | Wordineer</title>
  <meta name="description" content="Play unlimited Wordle rounds for free. Guess any random 5-letter word in 6 tries, or challenge a friend with a custom word. No sign-up needed.">
  <link rel="canonical" href="https://wordineer.com/wordle-game/">
  <meta property="og:type"        content="website">
  <meta property="og:site_name"   content="Wordineer">
  <meta property="og:title"       content="Play Wordle Free — Unlimited Wordle Game | Wordineer">
  <meta property="og:description" content="Play unlimited Wordle rounds for free. Guess any random 5-letter word in 6 tries, or challenge a friend.">
  <meta property="og:url"         content="https://wordineer.com/wordle-game/">
  <meta property="og:image"       content="https://wordineer.com/og-image.png">
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "WebApplication",
    "name": "Play Wordle",
    "url": "https://wordineer.com/wordle-game/",
    "description": "Free unlimited Wordle game. Guess a random 5-letter word in 6 tries, or challenge a friend with a custom word.",
    "applicationCategory": "GameApplication",
    "operatingSystem": "Web",
    "offers": { "@type": "Offer", "price": "0", "priceCurrency": "USD" },
    "publisher": { "@id": "https://wordineer.com/#organization" }
  }
  </script>
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
      {
        "@type": "Question",
        "name": "What do the colors mean in Wordle?",
        "acceptedAnswer": { "@type": "Answer", "text": "Green means the letter is correct and in the right position. Yellow means the letter is in the word but in the wrong position. Grey means the letter is not in the word at all. Use the color feedback from each guess to narrow down the answer." }
      },
      {
        "@type": "Question",
        "name": "How do I challenge a friend to a Wordle game?",
        "acceptedAnswer": { "@type": "Answer", "text": "Click the Share button during or after your game. It copies a link to your clipboard that contains the same secret word, encoded in the URL. Send that link to a friend — they'll play the same word without knowing what it is in advance." }
      },
      {
        "@type": "Question",
        "name": "Can I play unlimited Wordle games?",
        "acceptedAnswer": { "@type": "Answer", "text": "Yes. Click Play again after any game to start a fresh round with a new random word. You can also change the difficulty to Easy, Medium, or Hard to adjust how common the target words are." }
      },
      {
        "@type": "Question",
        "name": "What is the best strategy for Wordle?",
        "acceptedAnswer": { "@type": "Answer", "text": "Start with a word that covers multiple common letters — CRANE, SLATE, or RAISE are popular openers. For your second guess, use letters not yet tested. From guess three onward, use the color feedback: lock in green positions, try yellows in new spots, avoid greys entirely." }
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
      { "@type": "ListItem", "position": 3, "name": "Play Wordle", "item": "https://wordineer.com/wordle-game/" }
    ]
  }
  </script>
  <!-- /SLOT:meta -->
  ```

- [ ] **Step 2: Add style slot**

  Append to the file:

  ```html
  <!-- SLOT:style -->
  <style>
  .wg-card { max-width: 500px; margin: 0 auto; padding: 16px 16px 0; }

  /* Header */
  .wg-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 14px; gap: 8px; flex-wrap: wrap; }
  .wg-title  { font-size: 20px; font-weight: 700; color: var(--text); letter-spacing: .06em; text-transform: uppercase; }
  .wg-header-right { display: flex; align-items: center; gap: 8px; }
  .wg-diff-select  { padding: 6px 10px; font-size: 13px; font-family: inherit; border: 1px solid var(--border); border-radius: 7px; background: var(--bg); color: var(--text); outline: none; cursor: pointer; appearance: none; -webkit-appearance: none; }
  .wg-diff-select:focus { border-color: var(--brand); }

  /* Challenge banner */
  .wg-challenge-banner { display: none; background: #F4F3FF; border: 1px solid #C5C0F0; border-radius: 8px; padding: 8px 12px; font-size: 13px; color: var(--brand); margin-bottom: 12px; text-align: center; font-weight: 500; }
  .wg-challenge-banner.show { display: block; }

  /* Toast */
  .wg-toast { position: fixed; top: 72px; left: 50%; transform: translateX(-50%); background: var(--text); color: var(--bg); padding: 8px 16px; border-radius: 6px; font-size: 14px; font-weight: 600; opacity: 0; pointer-events: none; z-index: 200; transition: opacity .15s; white-space: nowrap; }
  .wg-toast.show { opacity: 1; }

  /* Grid */
  .wg-grid { display: flex; flex-direction: column; align-items: center; gap: 5px; margin-bottom: 16px; }
  .wg-row  { display: flex; gap: 5px; }
  .wg-tile { width: 58px; height: 58px; display: flex; align-items: center; justify-content: center; font-size: 28px; font-weight: 700; border: 2px solid var(--border); border-radius: 3px; color: var(--text); text-transform: uppercase; user-select: none; -webkit-user-select: none; }
  .wg-tile.filled  { border-color: #999; }
  .wg-tile.correct { background: #538D4E; border-color: #538D4E; color: white; }
  .wg-tile.present { background: #B59F3B; border-color: #B59F3B; color: white; }
  .wg-tile.absent  { background: #787C7E; border-color: #787C7E; color: white; }
  .wg-tile.flip    { animation: wg-flip .5s ease forwards; }
  .wg-tile.pop     { animation: wg-pop .08s ease; }
  .wg-tile.bounce  { animation: wg-bounce .5s ease; }
  .wg-row.shake    { animation: wg-shake .5s ease; }

  @keyframes wg-flip {
    0%   { transform: rotateX(0deg); }
    45%  { transform: rotateX(90deg); }
    55%  { transform: rotateX(90deg); }
    100% { transform: rotateX(0deg); }
  }
  @keyframes wg-pop {
    0%   { transform: scale(1); }
    50%  { transform: scale(1.12); }
    100% { transform: scale(1); }
  }
  @keyframes wg-shake {
    0%, 100% { transform: translateX(0); }
    16%  { transform: translateX(-5px); }
    33%  { transform: translateX(5px); }
    50%  { transform: translateX(-5px); }
    66%  { transform: translateX(5px); }
    83%  { transform: translateX(-3px); }
  }
  @keyframes wg-bounce {
    0%, 100% { transform: translateY(0); }
    40%  { transform: translateY(-14px); }
    60%  { transform: translateY(-7px); }
  }

  /* Result */
  .wg-result { display: none; text-align: center; padding: 10px 0 14px; }
  .wg-result.show { display: block; }
  .wg-result-msg  { font-size: 20px; font-weight: 700; color: var(--text); margin-bottom: 10px; }
  .wg-result-actions { display: flex; gap: 8px; justify-content: center; flex-wrap: wrap; align-items: center; }

  /* Keyboard */
  .wg-keyboard { display: flex; flex-direction: column; align-items: center; gap: 6px; padding: 0 0 24px; }
  .wg-kb-row   { display: flex; gap: 5px; }
  .wg-kb-key   { height: 58px; min-width: 43px; padding: 0 4px; display: flex; align-items: center; justify-content: center; font-size: 13px; font-weight: 700; font-family: inherit; border: none; border-radius: 4px; background: #D3D6DA; color: #1A1A1B; cursor: pointer; user-select: none; -webkit-user-select: none; transition: background .1s, color .1s; -webkit-tap-highlight-color: transparent; }
  .wg-kb-key.wide    { min-width: 65px; font-size: 12px; }
  .wg-kb-key:active  { opacity: .85; }
  .wg-kb-key.correct { background: #538D4E; color: white; }
  .wg-kb-key.present { background: #B59F3B; color: white; }
  .wg-kb-key.absent  { background: #787C7E; color: white; }

  @media(max-width:500px) {
    .wg-tile { width: 50px; height: 50px; font-size: 24px; }
    .wg-kb-key { height: 50px; min-width: 32px; font-size: 12px; }
    .wg-kb-key.wide { min-width: 50px; font-size: 11px; }
  }
  @media(max-width:380px) {
    .wg-tile { width: 44px; height: 44px; font-size: 20px; }
    .wg-kb-key { height: 46px; min-width: 28px; font-size: 11px; }
    .wg-kb-key.wide { min-width: 44px; }
  }
  </style>
  <!-- /SLOT:style -->
  ```

- [ ] **Step 3: Add hero slot**

  Append to the file:

  ```html
  <!-- SLOT:hero -->
  <div class="breadcrumb">
    <div class="breadcrumb-inner">
      <a href="/">Wordineer</a>
      <span class="breadcrumb-sep">›</span>
      <a href="/word-tools/">Word Tools</a>
      <span class="breadcrumb-sep">›</span>
      <span aria-current="page">Play Wordle</span>
    </div>
  </div>
  <div class="hero">
    <div class="hero-badge">
      <svg viewBox="0 0 11 11" fill="none"><circle cx="5.5" cy="5.5" r="4.5" stroke="#3C3489" stroke-width="1"/><path d="M3.5 5.5l1.5 1.5L8 3.5" stroke="#3C3489" stroke-width="1.2" stroke-linecap="round"/></svg>
      Free · No sign-up · Unlimited rounds
    </div>
    <h1>Play Wordle</h1>
    <p>Guess the 5-letter word in 6 tries. Green = right letter, right place. Yellow = right letter, wrong place. Challenge a friend by sharing your puzzle link.</p>
  </div>
  <!-- /SLOT:hero -->
  ```

- [ ] **Step 4: Add tool slot (game HTML structure)**

  Append to the file:

  ```html
  <!-- SLOT:tool -->
  <div class="tool-wrap">
    <div class="wg-card">

      <div class="wg-header">
        <span class="wg-title">Wordle</span>
        <div class="wg-header-right">
          <div id="wg-diff-wrap">
            <select id="wg-diff" class="wg-diff-select" aria-label="Word difficulty">
              <option value="all">Any difficulty</option>
              <option value="easy">Easy</option>
              <option value="medium">Medium</option>
              <option value="hard">Hard</option>
            </select>
          </div>
          <button id="wg-share-btn" class="act-btn">Share</button>
        </div>
      </div>

      <div id="wg-challenge-banner" class="wg-challenge-banner">
        Someone challenged you — guess the 5-letter word!
      </div>

      <div id="wg-toast" class="wg-toast" aria-live="assertive" aria-atomic="true"></div>

      <div id="wg-grid" class="wg-grid"></div>

      <div id="wg-result" class="wg-result" aria-live="polite">
        <div id="wg-result-msg" class="wg-result-msg"></div>
        <div class="wg-result-actions">
          <button id="wg-play-again" class="gen-btn" style="width:auto;padding:9px 22px">Play again</button>
          <button id="wg-share-result" class="act-btn">Share puzzle</button>
        </div>
      </div>

      <div id="wg-keyboard" class="wg-keyboard"></div>

    </div>
  </div>
  <!-- /SLOT:tool -->
  ```

- [ ] **Step 5: Add empty ad_b slot**

  Append to the file:

  ```html
  <!-- SLOT:ad_b -->
  <!-- /SLOT:ad_b -->
  ```

---

## Task 3: Add game JavaScript to wordle-game.html (init slot)

**Files:**
- Modify: `template-deploy/tools-src/wordle-game.html`

- [ ] **Step 1: Append explainer, faq, who, and init slots**

  Append to `wordle-game.html`:

  ```html
  <!-- SLOT:explainer -->
  <div class="explainer">

    <h2>How to Play Wordle</h2>
    <p>Each game gives you a hidden 5-letter word and six attempts to guess it. Type a 5-letter word and press Enter. The tiles change colour after each guess: <strong>green</strong> means the letter is correct and in the right position; <strong>yellow</strong> means the letter is in the word but in the wrong position; <strong>grey</strong> means the letter is not in the word at all. Use the feedback to narrow down your next guess.</p>
    <p>Every guess must be a real English word — the keyboard stays greyed out until you've typed five letters, and invalid words are rejected with a shake. The on-screen keyboard tracks which letters you've eliminated, confirmed, or misplaced, so you can see your information at a glance without scrolling back through your guesses.</p>

    <h2>Challenge Mode</h2>
    <p>The Share button generates a link that contains your current secret word encoded in the URL. Send that link to anyone — they'll land on the same puzzle and play it cold, without knowing the answer. You can share mid-game or after finishing. Because the word is hidden in the URL hash (the part after #), it's never sent to the server and can't be read at a glance in most URL bars.</p>
    <p>You can also use the <a href="/random-wordle-generator/">random Wordle word generator</a> to find a good secret word, then click the Play icon on any result to start a game with that word. Copy the URL from the Share button and send it to your target.</p>

    <h2>Difficulty Levels</h2>
    <p>The difficulty dropdown controls how common the randomly selected word is. Easy words are everyday vocabulary — the kind most people know immediately. Medium words are less frequent but broadly understood. Hard words are uncommon, technical, or archaic — the type that occasionally appear in the official Wordle answer list and leave experienced players stumped. Changing the difficulty immediately resets the board with a new word at that level.</p>

  </div>
  <!-- /SLOT:explainer -->

  <!-- SLOT:faq -->
  <div class="faq">
    <h2 class="faq-title">Frequently asked questions</h2>

    <div class="faq-item open">
      <div class="faq-q"><span class="faq-q-text">What do the tile colors mean?</span><svg class="faq-chevron" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div>
      <div class="faq-a">Green means the letter is in the correct position. Yellow means the letter is in the word but in a different position. Grey means the letter does not appear in the word at all. The same logic applies to the on-screen keyboard — each key shows the best result it has earned across all your guesses.</div>
    </div>

    <div class="faq-item">
      <div class="faq-q"><span class="faq-q-text">How do I challenge a friend?</span><svg class="faq-chevron" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div>
      <div class="faq-a">Click the Share button at any point during or after your game. It copies a URL to your clipboard that encodes the secret word in the link. Send that URL to a friend — they'll play the same word without knowing the answer. The word is hidden in the URL hash so it's not visible at a glance. You can also create a challenge from the random Wordle word generator by clicking the Play icon on any word, then using the Share button on the game page.</div>
    </div>

    <div class="faq-item">
      <div class="faq-q"><span class="faq-q-text">Can I play unlimited games?</span><svg class="faq-chevron" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div>
      <div class="faq-a">Yes. Click Play again after any game to start a fresh round with a new random word. There's no limit to how many games you can play. Use the difficulty selector to cycle through easy, medium, and hard words as you improve.</div>
    </div>

    <div class="faq-item">
      <div class="faq-q"><span class="faq-q-text">What's the best Wordle opening word?</span><svg class="faq-chevron" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div>
      <div class="faq-a">The most effective openers use common letters with no repeats: CRANE, SLATE, RAISE, and STARE are popular choices because they each hit multiple high-frequency letters — E, R, A, T, S, N — in one guess. The key insight is coverage: a word that tests five different common letters gives you more colour feedback than one with repeated letters or rare letters like Q, X, or Z.</div>
    </div>

    <div class="faq-item">
      <div class="faq-q"><span class="faq-q-text">Does this use the official Wordle word list?</span><svg class="faq-chevron" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div>
      <div class="faq-a">This game uses Wordineer's curated 5-letter word dataset, which covers a broad cross-section of common and uncommon English words across three difficulty levels. It is not the official New York Times Wordle list, so some words may differ. The gameplay rules — 6 guesses, colour feedback, valid-word-only guesses — are identical to the original.</div>
    </div>
  </div>
  <!-- /SLOT:faq -->

  <!-- SLOT:who -->
  <div>
    <h2 class="section-title" style="margin-bottom:14px">Who uses this</h2>
    <div class="uc-grid">
      <div class="uc"><div class="uc-title">Daily Wordle players</div><div class="uc-body">Warm up before your daily puzzle, or keep playing after it's done. Unlimited rounds, no waiting for tomorrow's word.</div></div>
      <div class="uc"><div class="uc-title">Friends and families</div><div class="uc-body">Use challenge mode to send a custom puzzle. Pick a tricky word, share the link, and see who cracks it fastest.</div></div>
      <div class="uc"><div class="uc-title">Teachers</div><div class="uc-body">Run a vocabulary Wordle round in class — set the word to a term from the lesson, share the link, and play as a group activity.</div></div>
      <div class="uc"><div class="uc-title">Word game enthusiasts</div><div class="uc-body">Practice the underlying skills — letter frequency reasoning, deduction from colour feedback — that carry over to Quordle, Dordle, and other Wordle variants.</div></div>
    </div>
  </div>
  <!-- /SLOT:who -->

  <!-- SLOT:init -->
  <script>
  (function () {
    var ROWS = 6;
    var COLS = 5;

    // ---- State ----
    var secretWord      = '';
    var guesses         = [];
    var currentGuess    = [];
    var gameOver        = false;
    var allWords        = [];
    var wordsLoaded     = false;
    var keyStates       = {};
    var isChallengeMode = false;

    // ---- DOM ----
    var tileEls = [];   // tileEls[row][col] = element
    var keyEls  = {};   // letter -> button element

    // ---- Seed (instant first render before fetch) ----
    var SEED = [
      {w:"Crane",diff:"easy"},{w:"Slate",diff:"easy"},{w:"Trace",diff:"easy"},
      {w:"Stare",diff:"easy"},{w:"Raise",diff:"easy"},{w:"Brave",diff:"easy"},
      {w:"Flame",diff:"easy"},{w:"Groan",diff:"easy"},{w:"Plumb",diff:"medium"},
      {w:"Crypt",diff:"medium"},{w:"Askew",diff:"medium"},{w:"Pivot",diff:"medium"},
      {w:"Blunt",diff:"easy"},{w:"Quirk",diff:"medium"},{w:"Fjord",diff:"hard"}
    ];

    // ---- Build grid ----
    function buildGrid() {
      var grid = document.getElementById('wg-grid');
      for (var r = 0; r < ROWS; r++) {
        var rowEl = document.createElement('div');
        rowEl.className = 'wg-row';
        rowEl.id = 'wg-row-' + r;
        tileEls[r] = [];
        for (var c = 0; c < COLS; c++) {
          var tile = document.createElement('div');
          tile.className = 'wg-tile';
          rowEl.appendChild(tile);
          tileEls[r][c] = tile;
        }
        grid.appendChild(rowEl);
      }
    }

    // ---- Build keyboard ----
    var KB_LAYOUT = [
      ['Q','W','E','R','T','Y','U','I','O','P'],
      ['A','S','D','F','G','H','J','K','L'],
      ['Enter','Z','X','C','V','B','N','M','⌫']
    ];

    function buildKeyboard() {
      var kb = document.getElementById('wg-keyboard');
      KB_LAYOUT.forEach(function (row) {
        var rowEl = document.createElement('div');
        rowEl.className = 'wg-kb-row';
        row.forEach(function (key) {
          var btn = document.createElement('button');
          btn.className = 'wg-kb-key' + (key.length > 1 ? ' wide' : '');
          btn.textContent = key;
          btn.setAttribute('type', 'button');
          btn.addEventListener('click', function () { handleKey(key); });
          rowEl.appendChild(btn);
          if (key.length === 1) keyEls[key] = btn;
        });
        kb.appendChild(rowEl);
      });
    }

    // ---- Input ----
    function handleKey(key) {
      if (gameOver) return;
      if (key === 'Enter') {
        submitGuess();
      } else if (key === '⌫' || key === 'Backspace') {
        deleteLetter();
      } else if (/^[A-Za-z]$/.test(key)) {
        addLetter(key.toUpperCase());
      }
    }

    function addLetter(letter) {
      if (currentGuess.length >= COLS) return;
      var col = currentGuess.length;
      var row = guesses.length;
      currentGuess.push(letter);
      var tile = tileEls[row][col];
      tile.textContent = letter;
      tile.classList.remove('pop');
      void tile.offsetWidth;
      tile.classList.add('filled', 'pop');
    }

    function deleteLetter() {
      if (!currentGuess.length) return;
      currentGuess.pop();
      var col = currentGuess.length;
      var row = guesses.length;
      tileEls[row][col].textContent = '';
      tileEls[row][col].classList.remove('filled');
    }

    // ---- Validation ----
    function isValidWord(word) {
      return allWords.some(function (w) { return w.w.toUpperCase() === word; });
    }

    // ---- Submit ----
    function submitGuess() {
      if (currentGuess.length < COLS) {
        shakeRow(guesses.length);
        showToast('Not enough letters');
        return;
      }
      var word = currentGuess.join('');
      if (!isValidWord(word)) {
        shakeRow(guesses.length);
        showToast('Not in word list');
        return;
      }
      var result  = getResult(word, secretWord);
      var rowIdx  = guesses.length;
      currentGuess = [];
      revealRow(rowIdx, word, result, function () {
        guesses.push({ word: word, result: result });
        updateKeyboard(word, result);
        if (result.every(function (r) { return r === 'correct'; })) {
          gameOver = true;
          bounceRow(rowIdx);
          setTimeout(function () { showResult(true); }, 500);
        } else if (guesses.length >= ROWS) {
          gameOver = true;
          setTimeout(function () { showResult(false); }, 300);
        }
      });
    }

    // ---- Color algorithm ----
    function getResult(guess, secret) {
      var result     = ['absent','absent','absent','absent','absent'];
      var secretLeft = secret.split('');
      var guessLeft  = guess.split('');
      // Green pass: exact position matches
      for (var i = 0; i < COLS; i++) {
        if (guessLeft[i] === secretLeft[i]) {
          result[i]     = 'correct';
          secretLeft[i] = null;
          guessLeft[i]  = null;
        }
      }
      // Yellow pass: letter in word but wrong position
      for (var i = 0; i < COLS; i++) {
        if (guessLeft[i] === null) continue;
        var idx = secretLeft.indexOf(guessLeft[i]);
        if (idx !== -1) {
          result[i]       = 'present';
          secretLeft[idx] = null;
        }
      }
      return result;
    }

    // ---- Animations ----
    function revealRow(rowIdx, word, result, cb) {
      var STAGGER  = 80;
      var DURATION = 500;
      for (var c = 0; c < COLS; c++) {
        (function (col, state) {
          setTimeout(function () {
            var tile = tileEls[rowIdx][col];
            tile.classList.add('flip');
            setTimeout(function () {
              tile.classList.remove('filled', 'flip');
              tile.classList.add(state);
            }, DURATION / 2);
          }, col * STAGGER);
        })(c, result[c]);
      }
      setTimeout(cb, COLS * STAGGER + DURATION);
    }

    function shakeRow(rowIdx) {
      var row = document.getElementById('wg-row-' + rowIdx);
      row.classList.remove('shake');
      void row.offsetWidth;
      row.classList.add('shake');
      row.addEventListener('animationend', function () {
        row.classList.remove('shake');
      }, { once: true });
    }

    function bounceRow(rowIdx) {
      tileEls[rowIdx].forEach(function (tile, i) {
        setTimeout(function () {
          tile.classList.add('bounce');
          tile.addEventListener('animationend', function () {
            tile.classList.remove('bounce');
          }, { once: true });
        }, i * 100);
      });
    }

    // ---- Keyboard state ----
    var STATE_RANK = { correct: 3, present: 2, absent: 1 };
    function updateKeyboard(word, result) {
      for (var i = 0; i < COLS; i++) {
        var letter = word[i];
        var state  = result[i];
        if (!keyStates[letter] || STATE_RANK[state] > STATE_RANK[keyStates[letter]]) {
          keyStates[letter] = state;
          if (keyEls[letter]) {
            keyEls[letter].className = 'wg-kb-key ' + state;
          }
        }
      }
    }

    // ---- Toast ----
    var toastTimer;
    function showToast(msg) {
      var el = document.getElementById('wg-toast');
      if (!el) return;
      el.textContent = msg;
      el.classList.remove('show');
      void el.offsetWidth;
      el.classList.add('show');
      clearTimeout(toastTimer);
      toastTimer = setTimeout(function () { el.classList.remove('show'); }, 1500);
    }

    // ---- Result banner ----
    var WIN_MSGS = ['Genius!', 'Magnificent!', 'Impressive!', 'Splendid!', 'Great!', 'Phew!'];
    function showResult(win) {
      var banner = document.getElementById('wg-result');
      var msg    = document.getElementById('wg-result-msg');
      if (!banner || !msg) return;
      msg.textContent = win
        ? WIN_MSGS[Math.min(guesses.length - 1, 5)]
        : 'The word was ' + secretWord + '.';
      banner.classList.add('show');
    }

    // ---- Reset ----
    function resetGame(word) {
      secretWord    = word.toUpperCase();
      guesses       = [];
      currentGuess  = [];
      gameOver      = false;
      keyStates     = {};
      isChallengeMode = false;
      tileEls.forEach(function (row) {
        row.forEach(function (tile) {
          tile.textContent = '';
          tile.className   = 'wg-tile';
        });
      });
      Object.keys(keyEls).forEach(function (letter) {
        keyEls[letter].className = 'wg-kb-key';
      });
      var banner    = document.getElementById('wg-result');
      var challenge = document.getElementById('wg-challenge-banner');
      var diffWrap  = document.getElementById('wg-diff-wrap');
      if (banner)    banner.classList.remove('show');
      if (challenge) challenge.classList.remove('show');
      if (diffWrap)  diffWrap.style.display = '';
      history.replaceState(null, '', '/wordle-game/');
    }

    // ---- Word pool ----
    function getDiff() {
      var s = document.getElementById('wg-diff');
      return s ? s.value : 'all';
    }

    function pickRandom() {
      var diff = getDiff();
      var pool = allWords.filter(function (w) {
        return diff === 'all' || w.diff === diff;
      });
      if (!pool.length) pool = allWords;
      return pool[Math.floor(Math.random() * pool.length)].w.toUpperCase();
    }

    // ---- Load words ----
    function loadWords(cb) {
      if (wordsLoaded) { cb(); return; }
      fetch('/data/wordle-words.json')
        .then(function (r) { return r.json(); })
        .then(function (data) {
          allWords    = data.filter(function (w) { return w.w.length === 5; });
          wordsLoaded = true;
          cb();
        })
        .catch(function () {
          allWords    = SEED;
          wordsLoaded = true;
          cb();
        });
    }

    // ---- URL hash / mode ----
    function resolveSecret(cb) {
      var hash = location.hash.slice(1);
      if (hash) {
        try {
          var decoded = atob(hash).toUpperCase().replace(/\s/g, '');
          if (/^[A-Z]{5}$/.test(decoded)) {
            loadWords(function () {
              var valid = allWords.some(function (w) { return w.w.toUpperCase() === decoded; });
              if (valid) {
                isChallengeMode = true;
                document.getElementById('wg-challenge-banner').classList.add('show');
                var dw = document.getElementById('wg-diff-wrap');
                if (dw) dw.style.display = 'none';
                cb(decoded);
              } else {
                cb(pickRandom());
              }
            });
            return;
          }
        } catch (e) {}
      }
      loadWords(function () { cb(pickRandom()); });
    }

    // ---- Share ----
    function doShare() {
      var url = location.origin + '/wordle-game/#' + btoa(secretWord);
      navigator.clipboard.writeText(url).then(function () {
        [document.getElementById('wg-share-btn'), document.getElementById('wg-share-result')]
          .forEach(function (btn) {
            if (!btn) return;
            var orig = btn.textContent;
            btn.textContent = 'Copied! ✓';
            setTimeout(function () { btn.textContent = orig; }, 1500);
          });
      });
    }

    // ---- Physical keyboard ----
    document.addEventListener('keydown', function (e) {
      if (e.ctrlKey || e.metaKey || e.altKey) return;
      if (e.target.tagName === 'SELECT' || e.target.tagName === 'INPUT') return;
      handleKey(e.key === 'Backspace' ? '⌫' : e.key);
    });

    // ---- Wire up buttons ----
    var shareBtn = document.getElementById('wg-share-btn');
    if (shareBtn) shareBtn.addEventListener('click', doShare);

    var playAgainBtn = document.getElementById('wg-play-again');
    if (playAgainBtn) {
      playAgainBtn.addEventListener('click', function () {
        loadWords(function () { resetGame(pickRandom()); });
      });
    }

    var shareResultBtn = document.getElementById('wg-share-result');
    if (shareResultBtn) shareResultBtn.addEventListener('click', doShare);

    var diffSel = document.getElementById('wg-diff');
    if (diffSel) {
      diffSel.addEventListener('change', function () {
        loadWords(function () { resetGame(pickRandom()); });
      });
    }

    // ---- Start ----
    buildGrid();
    buildKeyboard();
    resolveSecret(function (word) {
      secretWord = word;
    });

  })();
  </script>
  <!-- /SLOT:init -->
  ```

- [ ] **Step 2: Build and copy**

  ```bash
  cd template-deploy && python3 build.py
  cp template-deploy/output/wordle-game.html wordineer-deploy/
  ```
  Expected: `Build complete` with no errors.

- [ ] **Step 3: Verify game works in browser**

  Open `http://localhost:8080/wordle-game.html` (or restart the server if stopped).

  Check all of the following:
  - Grid renders 6 rows × 5 tiles
  - Keyboard renders with QWERTY layout + Enter / ⌫
  - Typing letters fills the current row tiles with pop animation
  - Backspace removes the last letter
  - Enter with fewer than 5 letters: row shakes, toast "Not enough letters"
  - Enter with a valid 5-letter word: tiles flip and colour up (green/yellow/grey)
  - Keyboard keys update to matching colours after submission
  - Win: win message appears after all-green row, bounce animation plays
  - Lose: after 6 wrong guesses, "The word was [WORD]." appears
  - Share button: copies a URL containing a base64 hash to clipboard
  - Paste that URL in a new tab — challenge banner shows, difficulty selector hidden, same word played

- [ ] **Step 4: Commit**

  ```bash
  git add template-deploy/tools-src/wordle-game.html wordineer-deploy/wordle-game.html
  git commit -m "feat: add Play Wordle game page with challenge links and difficulty selector"
  ```

---

## Task 4: Add Play Wordle to word-tools.html Word games section

**Files:**
- Modify: `template-deploy/tools-src/word-tools.html`

- [ ] **Step 1: Add Play Wordle as first item in the Word games tools-grid**

  In `word-tools.html`, find the Word games section (search for `<h2 class="section-title">Word games</h2>`). Inside the `<div class="tools-grid">` that follows, add this as the **first** item (before the Pictionary Word Generator entry):

  ```html
  <a class="tool-item" href="/wordle-game/">
    <div class="tool-icon" style="background:#E8F4FE"><svg viewBox="0 0 13 13" fill="none"><rect x="1.5" y="1.5" width="4" height="4" rx=".5" fill="#2B7FD4"/><rect x="7" y="1.5" width="4.5" height="4.5" rx=".5" fill="#2B7FD4" opacity=".35"/><rect x="1.5" y="7" width="4.5" height="4.5" rx=".5" fill="#2B7FD4" opacity=".35"/><rect x="7" y="7" width="4.5" height="4.5" rx=".5" fill="#2B7FD4"/></svg></div>
    <div class="tool-name">Play Wordle</div>
    <div class="tool-desc">Guess a random 5-letter word in 6 tries — or challenge a friend with your own word.</div>
  </a>
  ```

- [ ] **Step 2: Build and copy**

  ```bash
  cd template-deploy && python3 build.py
  cp template-deploy/output/word-tools.html wordineer-deploy/
  ```
  Expected: `Build complete` with no errors.

- [ ] **Step 3: Verify in browser**

  Open `http://localhost:8080/word-tools.html`. Scroll to the Word games section. Confirm "Play Wordle" card appears first, with the blue grid icon. Click it — navigates to `/wordle-game.html`.

- [ ] **Step 4: Commit**

  ```bash
  git add template-deploy/tools-src/word-tools.html wordineer-deploy/word-tools.html
  git commit -m "feat: add Play Wordle to Word games section on word-tools landing page"
  ```

---

## Task 5: Add _redirects rule and sitemap entry

**Files:**
- Modify: `wordineer-deploy/_redirects`
- Modify: `wordineer-deploy/sitemap.xml`

- [ ] **Step 1: Add clean URL redirect to _redirects**

  Open `wordineer-deploy/_redirects`. Add this line in the appropriate place (alongside other `/tool-name/` → `/tool-name.html` rules):

  ```
  /wordle-game/    /wordle-game.html    200
  ```

- [ ] **Step 2: Add sitemap entry**

  Open `wordineer-deploy/sitemap.xml`. Add an entry for the new page alongside similar tool entries:

  ```xml
  <url>
    <loc>https://wordineer.com/wordle-game/</loc>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>
  ```

- [ ] **Step 3: Verify redirect locally**

  Cloudflare-style rewrites don't apply during `python3 -m http.server`, so this step is a logic check only. Confirm `/wordle-game/` is in `_redirects` and the target `/wordle-game.html` exists in `wordineer-deploy/`.

  ```bash
  grep "wordle-game" wordineer-deploy/_redirects
  ls wordineer-deploy/wordle-game.html
  ```
  Expected:
  ```
  /wordle-game/    /wordle-game.html    200
  wordineer-deploy/wordle-game.html
  ```

- [ ] **Step 4: Commit**

  ```bash
  git add wordineer-deploy/_redirects wordineer-deploy/sitemap.xml
  git commit -m "feat: add /wordle-game/ clean URL redirect and sitemap entry"
  ```

---

## Task 6: Final verification and deploy

- [ ] **Step 1: Full local smoke test**

  ```bash
  cd wordineer-deploy && python3 -m http.server 8080
  ```

  Visit each URL and confirm:
  - `http://localhost:8080/random-wordle-generator.html` — Play icon shows on each word with tooltip on hover; clicking navigates to `/wordle-game/#<base64>`
  - `http://localhost:8080/wordle-game.html` — game loads, plays correctly, share copies URL
  - `http://localhost:8080/wordle-game.html#Q1JBTkU=` (base64 of "CRANE") — challenge banner appears, difficulty hidden, CRANE is secret word
  - `http://localhost:8080/word-tools.html` — Play Wordle card visible in Word games section

- [ ] **Step 2: Push to deploy**

  ```bash
  git push
  ```
  Cloudflare Pages auto-deploys in ~20 seconds.

- [ ] **Step 3: Verify on live site**

  - `https://wordineer.com/wordle-game/` loads (clean URL via redirect)
  - `https://wordineer.com/random-wordle-generator/` shows Play icons with tooltips
  - Click Play on any word → game opens with that word pre-loaded (challenge banner visible, difficulty hidden)
  - Share button → paste URL in new tab → same word plays
  - `https://wordineer.com/word-tools/` → Play Wordle card visible in Word games section

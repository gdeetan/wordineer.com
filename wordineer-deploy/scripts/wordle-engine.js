// WORDLE_HELPER — Wordle solver engine
const WORDLE_HELPER = (() => {
  let _guesses       = [];
  let _common        = [];
  let _openers       = [];
  let _loadPromise   = null;
  let _openersPromise = null;

  // Independent state per tab; switching tabs never bleeds state between them
  const STATE = {
    solve: {
      rows: [],      // [{word, pattern}]
      candidates: [],
    },
    practice: {
      secret: null,
      rows: [],      // [{word, pattern}]
      guessCount: 0,
      gameOver: false,
    },
  };

  let _cfg = {};

  // ── Core algorithm ────────────────────────────────────────────────────────

  /**
   * Two-pass duplicate-safe pattern computation.
   * Returns number[5]: 2=correct (green), 1=present (yellow), 0=absent (grey)
   *
   * Test cases:
   *   computePattern("speed","spree") → [2,2,1,2,0]
   *     pass1: s=s✓ p=p✓ e≠r e=e✓ d≠e → greens at 0,1,3; tLeft=[null,null,r,null,null] after pass1 wait—
   *     actually tLeft after pass1: pos0→null, pos1→null, pos3→null; remaining tLeft=[_,_,'r',_,'e']
   *     pass2: pos2 guess='e' → find 'e' in tLeft → pos4 → yellow; pos4 guess='d' → not in tLeft → grey
   *     result=[2,2,1,2,0] ✓
   *
   *   computePattern("aabbb","xaaxx") → [1,2,0,0,0]
   *     target=xaaxx: pos1 a=a green; tLeft=[x,null,a,x,x]
   *     pass2: pos0 'a'→find in tLeft→pos2→yellow; pos2,3,4 'b'→not in tLeft→grey
   *
   *   computePattern("abbey","kebab") → [1,1,2,1,0]
   *     target=kebab: pos2 b=b green; tLeft=[k,e,null,a,b]
   *     pass2: pos0 'a'→pos3→yellow; pos1 'b'→pos4→yellow; pos3 'e'→pos1→yellow; pos4 'y'→grey
   *
   *   computePattern("crane","crane") → [2,2,2,2,2]
   */
  function computePattern(guess, target) {
    const result = [0, 0, 0, 0, 0];
    const tLeft  = target.split('');
    const gLeft  = guess.split('');

    // Pass 1: exact position matches (green)
    for (let i = 0; i < 5; i++) {
      if (gLeft[i] === tLeft[i]) {
        result[i] = 2;
        tLeft[i]  = null;
        gLeft[i]  = null;
      }
    }

    // Pass 2: present but wrong position (yellow)
    for (let i = 0; i < 5; i++) {
      if (gLeft[i] === null) continue;
      const j = tLeft.indexOf(gLeft[i]);
      if (j !== -1) {
        result[i] = 1;
        tLeft[j]  = null;
      }
    }

    return result;
  }

  /**
   * Filter candidate pool to words consistent with every recorded guess+pattern.
   * history: Array<{word: string, pattern: number[5]}>
   */
  function filterCandidates(pool, history) {
    return pool.filter(candidate =>
      history.every(({ word, pattern }) => {
        const p = computePattern(word, candidate);
        return p.every((v, i) => v === pattern[i]);
      })
    );
  }

  /**
   * Rank candidate guesses by Shannon entropy against the remaining answer pool.
   *
   * When the remaining pool is large (> PROBE_THRESHOLD), probe words drawn from
   * the broader common-word pool can be more informative than any remaining candidate,
   * because they may partition the pool into more even buckets even though they can't
   * themselves be the answer. Below the threshold, the probe advantage shrinks and the
   * cheaper within-pool ranking is fast enough per keystroke.
   * PROBE_THRESHOLD=150 was chosen so that worst-case JS work (~1000 probes × 150 targets
   * = 150k pattern calls) is imperceptible in the browser; above it the gain is largest.
   *
   * Returns [{word, score, isCandidate}] sorted descending by score.
   */
  function rankCandidates(remainingPool, fullDict) {
    if (!remainingPool.length) return [];
    if (remainingPool.length === 1) return [{ word: remainingPool[0], score: Infinity, isCandidate: true }];

    const PROBE_THRESHOLD = 150;
    const guessSet = (fullDict && fullDict.length && remainingPool.length > PROBE_THRESHOLD)
      ? fullDict
      : remainingPool;

    const remainingSet = new Set(remainingPool);

    return guessSet.map(guess => {
      const buckets = {};
      for (const target of remainingPool) {
        const key = computePattern(guess, target).join('');
        buckets[key] = (buckets[key] || 0) + 1;
      }
      let score = 0;
      const n = remainingPool.length;
      for (const count of Object.values(buckets)) {
        const p = count / n;
        score -= p * Math.log2(p);
      }
      return { word: guess, score, isCandidate: remainingSet.has(guess) };
    }).sort((a, b) => b.score - a.score);
  }

  /** Pick a random word from the common (plausible answer) pool. */
  function pickRandomSecret() {
    return _common[Math.floor(Math.random() * _common.length)];
  }

  // ── Data loading ──────────────────────────────────────────────────────────

  function loadData() {
    if (_loadPromise) return _loadPromise;
    _loadPromise = Promise.all([
      fetch('/data/wordle-guesses.json').then(r => r.json()),
      fetch('/data/wordle-common.json').then(r => r.json()),
    ]).then(([g, c]) => {
      _guesses = g;
      _common  = c;
    });
    return _loadPromise;
  }

  function loadOpeners() {
    if (_openersPromise) return _openersPromise;
    _openersPromise = fetch('/data/wordle-openers.json')
      .then(r => r.json())
      .then(data => { _openers = data; })
      .catch(() => { /* fall back to starters from cfg */ });
    return _openersPromise;
  }

  // ── DOM helpers ───────────────────────────────────────────────────────────

  function $(id) { return document.getElementById(id); }

  function showError(id, msg) {
    const el = $(id);
    if (el) el.textContent = msg;
  }

  function clearError(id) { showError(id, ''); }

  // ── Solve tab ─────────────────────────────────────────────────────────────

  function buildChips() {
    const container = $(_cfg.chipsId);
    if (!container) return;
    container.innerHTML = '';
    const source = _openers.length ? _openers : (_cfg.starters || []).map(w => ({ word: w, note: '' }));
    source.forEach(({ word, note }) => {
      const btn = document.createElement('button');
      btn.className = 'wh-chip';
      btn.textContent = word.toUpperCase();
      if (note) btn.title = note;
      btn.addEventListener('click', () => prefillFirstRow(word.toLowerCase()));
      container.appendChild(btn);
    });
  }

  function prefillFirstRow(word) {
    const rows = $(_cfg.solveRowsId);
    if (!rows) return;
    let inputs = rows.querySelectorAll('.wh-guess-input');
    // Use first empty row or add a new one
    let target = null;
    for (const inp of inputs) {
      if (!inp.value) { target = inp; break; }
    }
    if (!target) {
      if (inputs.length < 6) {
        addGuessRow();
        inputs = rows.querySelectorAll('.wh-guess-input');
        target = inputs[inputs.length - 1];
      } else {
        return;
      }
    }
    target.value = word.toUpperCase();
    syncTiles(target.closest('.wh-guess-row'), word);
  }

  function addGuessRow() {
    const container = $(_cfg.solveRowsId);
    if (!container) return;
    const existingRows = container.querySelectorAll('.wh-guess-row');
    if (existingRows.length >= 6) return;

    const row = document.createElement('div');
    row.className = 'wh-guess-row';
    row.style.cssText = 'display:flex;align-items:center;gap:8px;margin-bottom:10px';

    const input = document.createElement('input');
    input.type = 'text';
    input.className = 'wh-guess-input';
    input.maxLength = 5;
    input.placeholder = 'CRANE';
    input.autocomplete = 'off';
    input.autocorrect = 'off';
    input.spellcheck = false;
    input.style.cssText = 'width:110px;padding:8px 10px;font:600 16px/1 inherit;text-transform:uppercase;border:1px solid var(--border);border-radius:var(--radius);letter-spacing:.08em;outline:none;font-family:inherit';
    input.addEventListener('input', () => {
      input.value = input.value.toUpperCase().replace(/[^A-Z]/g, '').slice(0, 5);
      syncTiles(row, input.value.toLowerCase());
      input.classList.remove('error');
      clearError(_cfg.solveErrorId);
    });

    const tileRow = document.createElement('div');
    tileRow.className = 'wh-tile-row';
    tileRow.style.cssText = 'display:flex;gap:5px';

    for (let i = 0; i < 5; i++) {
      const tile = document.createElement('div');
      tile.className = 'wh-tile';
      tile.dataset.pos = i;
      tile.dataset.state = '-1';
      tile.addEventListener('click', () => cycleTile(tile));
      tileRow.appendChild(tile);
    }

    row.appendChild(input);
    row.appendChild(tileRow);
    container.appendChild(row);

    // Hide add button when 6 rows reached
    if (container.querySelectorAll('.wh-guess-row').length >= 6) {
      const addBtn = $(_cfg.addGuessBtnId);
      if (addBtn) addBtn.style.display = 'none';
    }
  }

  const TILE_CYCLE = { '-1': '0', '0': '2', '2': '1', '1': '0' };
  const TILE_CYCLE_LABELS = { '-1': '', '0': 'absent', '2': 'correct', '1': 'present' };

  function cycleTile(tile) {
    if (tile.dataset.state === '-1') return; // no letter yet
    tile.dataset.state = TILE_CYCLE[tile.dataset.state] || '0';
  }

  function syncTiles(row, word) {
    const tiles = row.querySelectorAll('.wh-tile');
    tiles.forEach((tile, i) => {
      const ch = word[i] || '';
      tile.textContent = ch.toUpperCase();
      if (!ch) {
        tile.dataset.state = '-1';
      } else if (tile.dataset.state === '-1') {
        tile.dataset.state = '0'; // default to absent when letter first typed
      }
    });
  }

  function validateAndCollectRows() {
    const container = $(_cfg.solveRowsId);
    if (!container) return null;
    const rows = container.querySelectorAll('.wh-guess-row');
    if (!rows.length) {
      showError(_cfg.solveErrorId, 'Add at least one guess first.');
      return null;
    }

    const history = [];
    for (const row of rows) {
      const input = row.querySelector('.wh-guess-input');
      const word = (input?.value || '').toLowerCase().trim();
      if (!word) continue; // skip empty rows

      if (!/^[a-z]{5}$/.test(word)) {
        input.classList.add('error');
        showError(_cfg.solveErrorId, `"${word.toUpperCase()}" must be exactly 5 letters.`);
        return null;
      }

      const tiles = row.querySelectorAll('.wh-tile');
      const pattern = [];
      let hasUnset = false;
      tiles.forEach(tile => {
        const s = parseInt(tile.dataset.state, 10);
        if (s === -1) hasUnset = true;
        pattern.push(s === -1 ? 0 : s);
      });

      if (hasUnset) {
        showError(_cfg.solveErrorId, `Set the tile colours for "${word.toUpperCase()}" before analysing.`);
        return null;
      }

      history.push({ word, pattern });
    }

    if (!history.length) {
      showError(_cfg.solveErrorId, 'Enter at least one guess to analyse.');
      return null;
    }

    return history;
  }

  function runAnalyse() {
    clearError(_cfg.solveErrorId);
    loadData().then(() => {
      const history = validateAndCollectRows();
      if (!history) return;

      const remaining = filterCandidates(_common, history);
      const ranked    = rankCandidates(remaining, _guesses);

      STATE.solve.candidates = remaining;

      // Show results section
      const resultsEl = $(_cfg.resultsId);
      if (resultsEl) resultsEl.style.display = '';

      // Best card
      if (remaining.length === 0) {
        const bw = $(_cfg.bestWordId);
        const bb = $(_cfg.bestBitsId);
        if (bw) bw.textContent = '—';
        if (bb) bb.textContent = 'No candidates match. Check your clue colours.';
        updateCandidateList([], ranked);
        return;
      }

      if (remaining.length === 1) {
        const bw = $(_cfg.bestWordId);
        const bb = $(_cfg.bestBitsId);
        if (bw) bw.textContent = remaining[0].toUpperCase();
        if (bb) bb.textContent = 'Only one word left!';
        updateCandidateList(remaining, ranked);
        return;
      }

      const best = ranked[0];
      const bw = $(_cfg.bestWordId);
      const bb = $(_cfg.bestBitsId);
      if (bw) bw.textContent = best.word.toUpperCase();
      if (bb) {
        const probeNote = best.isCandidate === false ? ' · probe word (not a possible answer)' : '';
        bb.textContent = `${best.score.toFixed(2)} bits of information · narrows the field most${probeNote}`;
      }

      updateCandidateList(remaining, ranked);
    }).catch(err => {
      showError(_cfg.solveErrorId, 'Could not load word data. Please refresh and try again.');
    });
  }

  function updateCandidateList(remaining, ranked) {
    const countEl = $(_cfg.candsCountId);
    const gridEl  = $(_cfg.candsGridId);
    const bodyEl  = $(_cfg.candsBodyId);
    const hdrEl   = $(_cfg.candsHdrId);

    if (countEl) countEl.textContent = `Possible answers: ${remaining.length}`;

    if (gridEl) {
      gridEl.innerHTML = '';
      ranked.forEach((item, idx) => {
        const span = document.createElement('span');
        span.className = 'wh-cand-word' + (idx < 10 ? ' top' : '');
        span.textContent = item.word.toUpperCase();
        gridEl.appendChild(span);
      });
    }

    // Auto-expand when small enough to scan
    const threshold = _cfg.collapseThreshold || 30;
    const shouldOpen = remaining.length <= threshold;
    if (bodyEl) bodyEl.classList.toggle('open', shouldOpen);
    if (hdrEl)  hdrEl.setAttribute('aria-expanded', shouldOpen ? 'true' : 'false');
  }

  function resetSolve() {
    const container = $(_cfg.solveRowsId);
    if (container) container.innerHTML = '';
    const resultsEl = $(_cfg.resultsId);
    if (resultsEl) resultsEl.style.display = 'none';
    const addBtn = $(_cfg.addGuessBtnId);
    if (addBtn) addBtn.style.display = '';
    clearError(_cfg.solveErrorId);
    STATE.solve.rows = [];
    STATE.solve.candidates = [];
    addGuessRow(); // start with one empty row
  }

  // ── Candidate list collapsible ────────────────────────────────────────────

  function initCandsToggle() {
    const hdr  = $(_cfg.candsHdrId);
    const body = $(_cfg.candsBodyId);
    if (!hdr || !body) return;
    hdr.addEventListener('click', () => {
      const open = body.classList.toggle('open');
      hdr.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  // ── Practice tab ──────────────────────────────────────────────────────────

  function buildPracticeGrid() {
    const grid = $(_cfg.pracGridId);
    if (!grid) return;
    grid.innerHTML = '';
    for (let r = 0; r < 6; r++) {
      const rowEl = document.createElement('div');
      rowEl.className = 'wh-grid-row';
      rowEl.id = `wh-prac-row-${r}`;
      for (let c = 0; c < 5; c++) {
        const tile = document.createElement('div');
        tile.className = 'wh-grid-tile';
        tile.id = `wh-prac-tile-${r}-${c}`;
        rowEl.appendChild(tile);
      }
      grid.appendChild(rowEl);
    }
  }

  function startPracticeGame() {
    STATE.practice.secret     = pickRandomSecret();
    STATE.practice.rows       = [];
    STATE.practice.guessCount = 0;
    STATE.practice.gameOver   = false;

    buildPracticeGrid();

    const suggestEl = $(_cfg.pracSuggestId);
    if (suggestEl) suggestEl.style.display = 'none';
    const resultEl = $(_cfg.pracResultId);
    if (resultEl) resultEl.style.display = 'none';
    const inputRow = $(_cfg.pracInputRowId);
    if (inputRow) inputRow.style.display = '';
    const input = $(_cfg.pracInputId);
    if (input) { input.value = ''; input.focus(); }
    clearError(_cfg.pracErrorId);
  }

  function submitPracticeGuess() {
    if (STATE.practice.gameOver) return;

    const input  = $(_cfg.pracInputId);
    const word   = (input?.value || '').toLowerCase().trim();
    clearError(_cfg.pracErrorId);

    if (!/^[a-z]{5}$/.test(word)) {
      showError(_cfg.pracErrorId, 'Enter exactly 5 letters.');
      return;
    }

    const pattern = computePattern(word, STATE.practice.secret);
    const rowIdx  = STATE.practice.guessCount;

    // Colour tiles
    for (let c = 0; c < 5; c++) {
      const tile = $(`wh-prac-tile-${rowIdx}-${c}`);
      if (tile) {
        tile.textContent    = word[c].toUpperCase();
        tile.dataset.state  = pattern[c];
        tile.classList.add('filled');
      }
    }

    STATE.practice.rows.push({ word, pattern });
    STATE.practice.guessCount++;
    if (input) input.value = '';

    const won = pattern.every(v => v === 2);

    if (won) {
      STATE.practice.gameOver = true;
      const inputRow = $(_cfg.pracInputRowId);
      if (inputRow) inputRow.style.display = 'none';
      const suggestEl = $(_cfg.pracSuggestId);
      if (suggestEl) suggestEl.style.display = 'none';
      showPracticeResult(`Solved in ${STATE.practice.guessCount} ${STATE.practice.guessCount === 1 ? 'guess' : 'guesses'}!`);
      return;
    }

    if (STATE.practice.guessCount >= 6) {
      STATE.practice.gameOver = true;
      const inputRow = $(_cfg.pracInputRowId);
      if (inputRow) inputRow.style.display = 'none';
      const suggestEl = $(_cfg.pracSuggestId);
      if (suggestEl) suggestEl.style.display = 'none';
      showPracticeResult(`The word was ${STATE.practice.secret.toUpperCase()}. Better luck next time!`);
      return;
    }

    // Update hint — same rankCandidates as solve tab
    const remaining = filterCandidates(_common, STATE.practice.rows);
    const ranked    = rankCandidates(remaining, _guesses);
    if (ranked.length) {
      const suggestEl = $(_cfg.pracSuggestId);
      const bestEl    = $(_cfg.pracBestId);
      const bitsEl    = $(_cfg.pracBitsId);
      if (suggestEl) suggestEl.style.display = '';
      if (bestEl)    bestEl.textContent = ranked[0].word.toUpperCase();
      if (bitsEl && remaining.length > 1) {
        const probeNote = ranked[0].isCandidate === false ? ' · probe word' : '';
        bitsEl.textContent = `${ranked[0].score.toFixed(2)} bits · ${remaining.length} words remain${probeNote}`;
      } else if (bitsEl) {
        bitsEl.textContent = '';
      }
    }
  }

  function showPracticeResult(msg) {
    const resultEl  = $(_cfg.pracResultId);
    const resultMsg = $(_cfg.pracResultMsgId);
    if (resultMsg) resultMsg.textContent = msg;
    if (resultEl)  resultEl.style.display = '';
  }

  // ── Tab switching ─────────────────────────────────────────────────────────

  function switchTab(to) {
    const tabs   = ['solve', 'practice'];
    const tabIds = { solve: _cfg.tabSolveId, practice: _cfg.tabPracticeId };
    const panIds = { solve: _cfg.panelSolveId, practice: _cfg.panelPracticeId };

    tabs.forEach(t => {
      const tab = $(tabIds[t]);
      const pan = $(panIds[t]);
      const active = t === to;
      if (tab) { tab.classList.toggle('active', active); tab.setAttribute('aria-selected', active); }
      if (pan) pan.classList.toggle('active', active);
    });

    if (to === 'practice' && !STATE.practice.secret) {
      loadData().then(() => startPracticeGame());
    }
  }

  // ── Public init ───────────────────────────────────────────────────────────

  function init(cfg) {
    _cfg = cfg || {};

    // Build chips from hardcoded starters immediately, then replace with openers once loaded
    buildChips();
    loadOpeners().then(buildChips);
    addGuessRow();

    // Solve tab wiring
    const addBtn     = $(_cfg.addGuessBtnId);
    const analyseBtn = $(_cfg.analyseBtnId);
    const resetBtn   = $(_cfg.solveResetId);

    if (addBtn)     addBtn.addEventListener('click', addGuessRow);
    if (analyseBtn) analyseBtn.addEventListener('click', runAnalyse);
    if (resetBtn)   resetBtn.addEventListener('click', resetSolve);

    initCandsToggle();

    // Practice tab wiring
    const pracSubmit = $(_cfg.pracSubmitId);
    const pracNew    = $(_cfg.pracNewId);
    const pracInput  = $(_cfg.pracInputId);

    if (pracSubmit) pracSubmit.addEventListener('click', submitPracticeGuess);
    if (pracNew)    pracNew.addEventListener('click', () => loadData().then(() => startPracticeGame()));
    if (pracInput) {
      pracInput.addEventListener('keydown', e => {
        if (e.key === 'Enter') submitPracticeGuess();
      });
      pracInput.addEventListener('input', () => {
        pracInput.value = pracInput.value.toUpperCase().replace(/[^A-Z]/g, '').slice(0, 5);
        clearError(_cfg.pracErrorId);
      });
    }

    // Tab switching
    const tabSolve    = $(_cfg.tabSolveId);
    const tabPractice = $(_cfg.tabPracticeId);
    if (tabSolve)    tabSolve.addEventListener('click',    () => switchTab('solve'));
    if (tabPractice) tabPractice.addEventListener('click', () => switchTab('practice'));
  }

  return { init, computePattern, filterCandidates, rankCandidates, pickRandomSecret };
})();

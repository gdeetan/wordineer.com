# B-Words Show More Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the A-page `Show more words` batch-render behavior to the B-words page.

**Architecture:** Copy the existing A-page page-local batching pattern into the B template instead of introducing shared abstractions. The B page keeps its existing filtering and copy/export behavior while rendering only a visible slice of the filtered results.

**Tech Stack:** Static HTML, CSS, vanilla JavaScript

---

### Task 1: Add B-page show-more markup and styles

**Files:**
- Modify: `template-deploy/tools-src/5-letter-words-starting-with-b.html`

- [ ] **Step 1: Add the `lp-more-wrap` block below the grid**

Run: `python3 - <<'PY'
from pathlib import Path
text = Path('template-deploy/tools-src/5-letter-words-starting-with-b.html').read_text()
assert 'id="lp-more-btn"' not in text
print('OK')
PY`

Expected: `OK`

- [ ] **Step 2: Add the `lp-more-wrap` style**

Run: `python3 - <<'PY'
from pathlib import Path
text = Path('template-deploy/tools-src/5-letter-words-starting-with-b.html').read_text()
assert '.lp-more-wrap' not in text
print('OK')
PY`

Expected: `OK`

### Task 2: Add the B-page batch rendering logic

**Files:**
- Modify: `template-deploy/tools-src/5-letter-words-starting-with-b.html`

- [ ] **Step 1: Add batch state and DOM references**

Run: `python3 - <<'PY'
from pathlib import Path
text = Path('template-deploy/tools-src/5-letter-words-starting-with-b.html').read_text()
assert 'var BATCH_SIZE = 50;' not in text
assert 'visibleCount' not in text
print('OK')
PY`

Expected: `OK`

- [ ] **Step 2: Add applyFilters/reset/renderCount/renderMoreButton helpers and slice-based rendering**

Run: `python3 - <<'PY'
from pathlib import Path
text = Path('template-deploy/tools-src/5-letter-words-starting-with-b.html').read_text()
assert 'filtered.slice(0, Math.min(visibleCount, filtered.length))' not in text
print('OK')
PY`

Expected: `OK`

- [ ] **Step 3: Add filter reset handlers and `Show more` click handler**

Run: `python3 - <<'PY'
from pathlib import Path
text = Path('template-deploy/tools-src/5-letter-words-starting-with-b.html').read_text()
assert "moreBtn.addEventListener('click'" not in text
print('OK')
PY`

Expected: `OK`

### Task 3: Rebuild and verify the B page

**Files:**
- Modify: `template-deploy/output/5-letter-words-starting-with-b.html` via build
- Modify: `wordineer-deploy/5-letter-words-starting-with-b.html`

- [ ] **Step 1: Rebuild template output**

Run: `python3 build.py`

Workdir: `template-deploy`

Expected: build completes and includes `5-letter-words-starting-with-b.html`

- [ ] **Step 2: Sync the built B page to the deploy folder**

Run: `cp 'template-deploy/output/5-letter-words-starting-with-b.html' 'wordineer-deploy/5-letter-words-starting-with-b.html'`

Expected: command exits successfully

- [ ] **Step 3: Verify built and deployed B pages contain the show-more logic**

Run: `python3 - <<'PY'
from pathlib import Path
for p in [
    'template-deploy/tools-src/5-letter-words-starting-with-b.html',
    'template-deploy/output/5-letter-words-starting-with-b.html',
    'wordineer-deploy/5-letter-words-starting-with-b.html',
]:
    text = Path(p).read_text()
    assert 'id="lp-more-btn"' in text
    assert 'var BATCH_SIZE = 50;' in text
    assert 'Show more words' in text
    assert "fetch('/data/five-letter-words-b.json')" in text
print('OK')
PY`

Expected: `OK`

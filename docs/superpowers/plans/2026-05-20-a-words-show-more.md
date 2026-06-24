# A-Words Show More Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add progressive disclosure to the A-words page so it initially renders a small batch of matching cards and reveals more with a `Show more words` button.

**Architecture:** Keep the existing client-side filtering and JSON loading model intact, but introduce page-local render state for visible batch size. The grid continues to render from `filtered`, while the count label and button state are derived from `visibleCount` versus the full filtered result length.

**Tech Stack:** Static HTML, CSS, vanilla JavaScript

---

### Task 1: Add the show-more markup and styles

**Files:**
- Modify: `template-deploy/tools-src/5-letter-words-starting-with-a.html`
- Test: manual browser verification on the generated page

- [ ] **Step 1: Add the footer control markup below the grid**

```html
<div class="lp-more-wrap" id="lp-more-wrap" hidden>
  <button class="lp-btn" id="lp-more-btn" type="button">Show more words</button>
</div>
```

- [ ] **Step 2: Add minimal styles for the footer control**

```css
.lp-more-wrap {
  display: flex;
  justify-content: center;
  margin-top: 18px;
}
```

- [ ] **Step 3: Verify the file still has a valid structure**

Run: `python3 - <<'PY'
from pathlib import Path
text = Path('template-deploy/tools-src/5-letter-words-starting-with-a.html').read_text()
assert 'id="lp-more-btn"' in text
assert '.lp-more-wrap' in text
print('OK')
PY`

Expected: `OK`

### Task 2: Add visible-count render state and partial rendering

**Files:**
- Modify: `template-deploy/tools-src/5-letter-words-starting-with-a.html`
- Test: manual browser verification on the generated page

- [ ] **Step 1: Add the new render-state constants and DOM references**

```js
  var BATCH_SIZE = 50;
  var allWords = SEED.slice();
  var filtered = allWords.slice();
  var visibleCount = BATCH_SIZE;
  var fullLoaded = false;
```

```js
  var moreWrap = document.getElementById('lp-more-wrap');
  var moreBtn = document.getElementById('lp-more-btn');
```

- [ ] **Step 2: Update the count helper to show visible versus total**

```js
  function renderCount(total) {
    var shown = Math.min(visibleCount, total);
    count.textContent = 'Showing ' + shown + ' of ' + total + ' words';
  }
```

- [ ] **Step 3: Render only the visible slice of filtered results**

```js
    var visibleWords = filtered.slice(0, Math.min(visibleCount, filtered.length));
    list.innerHTML = visibleWords.map(function (item) {
```

- [ ] **Step 4: Toggle the button based on remaining hidden results**

```js
  function renderMoreButton(total) {
    var hasMore = total > visibleCount;
    moreWrap.hidden = !hasMore;
  }
```

- [ ] **Step 5: Re-run the template sanity check**

Run: `python3 - <<'PY'
from pathlib import Path
text = Path('template-deploy/tools-src/5-letter-words-starting-with-a.html').read_text()
assert 'BATCH_SIZE = 50' in text
assert "Showing ' + shown + ' of ' + total + ' words" in text
assert 'filtered.slice(0, Math.min(visibleCount, filtered.length))' in text
print('OK')
PY`

Expected: `OK`

### Task 3: Reset on filter changes and append more results on click

**Files:**
- Modify: `template-deploy/tools-src/5-letter-words-starting-with-a.html`
- Test: manual browser verification on the generated page

- [ ] **Step 1: Reset visible count when filters change**

```js
  function applyFilters() {
    var typeVal = typeFilter.value;
    var diffVal = diffFilter.value;
    filtered = allWords.filter(function (item) {
      var typeOk = typeVal === 'all' || item.t === typeVal;
      var diffOk = diffVal === 'all' || item.diff === diffVal;
      return typeOk && diffOk;
    });
  }

  function resetVisibleCount() {
    visibleCount = BATCH_SIZE;
  }
```

```js
  typeFilter.addEventListener('change', function () {
    resetVisibleCount();
    render();
  });

  diffFilter.addEventListener('change', function () {
    resetVisibleCount();
    render();
  });
```

- [ ] **Step 2: Add the show-more click handler**

```js
  moreBtn.addEventListener('click', function () {
    visibleCount = Math.min(visibleCount + BATCH_SIZE, filtered.length);
    render();
  });
```

- [ ] **Step 3: Make render handle empty and small result sets cleanly**

```js
    if (!filtered.length) {
      list.innerHTML = '';
      loading.hidden = true;
      empty.hidden = false;
      count.textContent = 'Showing 0 of 0 words';
      moreWrap.hidden = true;
      return;
    }
```

- [ ] **Step 4: Verify the interactive hooks exist**

Run: `python3 - <<'PY'
from pathlib import Path
text = Path('template-deploy/tools-src/5-letter-words-starting-with-a.html').read_text()
assert "typeFilter.addEventListener('change'" in text
assert "diffFilter.addEventListener('change'" in text
assert "moreBtn.addEventListener('click'" in text
print('OK')
PY`

Expected: `OK`

### Task 4: Verify behavior locally

**Files:**
- Modify: none
- Test: `template-deploy/tools-src/5-letter-words-starting-with-a.html`

- [ ] **Step 1: Run static checks against the edited source**

Run: `python3 - <<'PY'
from pathlib import Path
import re
text = Path('template-deploy/tools-src/5-letter-words-starting-with-a.html').read_text()
assert text.count('lp-more-btn') >= 1
assert text.count('Show more words') >= 1
assert 'Showing 0 of 0 words' in text
assert 'visibleCount = Math.min(visibleCount + BATCH_SIZE, filtered.length);' in text
print('OK')
PY`

Expected: `OK`

- [ ] **Step 2: Summarize manual verification requirements**

Run: `printf '%s\n' \
'1. Start local server from wordineer-deploy' \
'2. Open /5-letter-words-starting-with-a/' \
'3. Confirm button hidden with current 101-word dataset if results <= visible count after filters, or visible when dataset later grows past 50' \
'4. Confirm count label shows visible/total format' \
'5. Confirm changing filters resets the visible batch' \
'6. Confirm copy/export still uses all filtered words'`

Expected: six-line checklist output

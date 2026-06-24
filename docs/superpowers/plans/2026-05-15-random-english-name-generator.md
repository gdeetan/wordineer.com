# Random English Name Generator Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a dedicated England-focused name generator page with a first-name default, a dedicated English-name dataset, automatic filter-driven regeneration, and SEO copy that supports the `1100+` search intent.

**Architecture:** Three layers: a dedicated `english-names.json` dataset, a page-specific HTML source built with the existing Wordineer generator pattern, and updated site wiring so the page appears in related tool menus and builds into the deployed site. Keep the page England-specific rather than duplicating the broader British generator.

**Tech Stack:** Static HTML/CSS/JS, `template-deploy/build.py`, existing Wordineer generator runtime, Node.js tests, JSON data files.

---

## File Map

| Action | Path |
|---|---|
| Create | `wordineer-deploy/data/english-names.json` |
| Create | `template-deploy/tools-src/random-english-name-generator.html` |
| Modify | `template-deploy/tools.json` |
| Modify | `wordineer-deploy/name-generators.html` |
| Create | `tests/english-names-data.test.js` |
| Create | `tests/english-generator-page.test.js` |
| Create / sync generated output | `wordineer-deploy/random-english-name-generator.html` |

---

## Task 1: Build the English Names Dataset

**Files:**
- Create: `wordineer-deploy/data/english-names.json`
- Create: `tests/english-names-data.test.js`

- [ ] **Step 1: Write the failing data test first**

Create `tests/english-names-data.test.js` with checks that lock the scope:

```js
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

test('english names dataset has the expected shape', () => {
  const file = path.join(__dirname, '..', 'wordineer-deploy', 'data', 'english-names.json');
  assert.ok(fs.existsSync(file), 'english-names.json should exist');

  const data = JSON.parse(fs.readFileSync(file, 'utf8'));
  assert.ok(Array.isArray(data.first), 'first should be an array');
  assert.ok(Array.isArray(data.middle), 'middle should be an array');
  assert.ok(Array.isArray(data.last), 'last should be an array');

  const total = data.first.length + data.middle.length + data.last.length;
  assert.ok(total >= 1100, `expected at least 1100 entries, got ${total}`);
  assert.ok(data.first.length >= 900, `expected at least 900 first names, got ${data.first.length}`);

  const firstSelected = data.first.filter((row) => Array.isArray(row) && row[1] === 'f');
  assert.ok(firstSelected.length > 0, 'dataset should include female first names');
});
```

- [ ] **Step 2: Run the test and confirm it fails**

Run:

```bash
node --test tests/english-names-data.test.js
```

Expected: fail because `english-names.json` does not exist yet.

- [ ] **Step 3: Create the dataset**

Build `wordineer-deploy/data/english-names.json` with a compact array schema:

```json
{
  "first": [
    ["James", "m", ["classic", "common"], ["timeless", "modern"], ["english"], "Classic English first name"],
    ["Hazel", "f", ["classic", "vintage"], ["timeless"], ["english"], "Soft vintage English first name"]
  ],
  "middle": [
    ["Rose", "f", ["classic"], ["timeless"], ["english"], "Traditional middle name"]
  ],
  "last": [
    ["Smith", ["common", "occupational"], ["english"], "Common English surname"]
  ]
}
```

Keep the actual file focused on:
- 900 first names
- enough middle-name support to make the total inventory honestly exceed 1100
- a smaller surname pool for full-name generation
- short notes only

- [ ] **Step 4: Re-run the dataset test**

Run:

```bash
node --test tests/english-names-data.test.js
```

Expected: pass.

---

## Task 2: Create the Page Source and Final HTML

**Files:**
- Create: `template-deploy/tools-src/random-english-name-generator.html`
- Create / sync generated output: `wordineer-deploy/random-english-name-generator.html`

- [ ] **Step 1: Write the failing page test first**

Create `tests/english-generator-page.test.js` with checks for SEO, defaults, filters, and explainer copy:

```js
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

test('english generator page has the required controls and defaults', () => {
  const source = path.join(__dirname, '..', 'template-deploy', 'tools-src', 'random-english-name-generator.html');
  assert.ok(fs.existsSync(source), 'random-english-name-generator.html source should exist');

  const html = fs.readFileSync(source, 'utf8');
  assert.match(html, /1100\+ Random English Names/i, 'title/H1 should use the 1100+ framing');
  assert.match(html, /id="eng-type"/, 'name type control should exist');
  assert.match(html, /<option value="first" selected>First name<\/option>|<option selected value="first">First name<\/option>/, 'first name should be the default');
  assert.match(html, /id="eng-mobile-toggle"/, 'mobile more-options toggle should exist');
  assert.match(html, /What is a random English name generator\?/i, 'explainer section should exist');
  assert.match(html, /How it works/i, 'how-it-works section should exist');
  assert.match(html, /random-english-name-generator\//, 'canonical URL should point to the new page');
});
```

- [ ] **Step 2: Run the test and confirm it fails**

Run:

```bash
node --test tests/english-generator-page.test.js
```

Expected: fail because the page source does not exist yet.

- [ ] **Step 3: Create the tool source**

Write `template-deploy/tools-src/random-english-name-generator.html` by copying the existing name-generator layout and adapting it for England-specific data:
- title and H1 should use `1100+ Random English Names`
- hero copy should say first names are the default
- count input should appear first
- `More options` toggle should hide the advanced controls on mobile
- `Name type` should default to `First name`
- filters should include `Gender`, `Style`, `Era`, `Starts with`, and `Show meanings`
- the result cards should auto-refresh when any filter changes
- use the dedicated `/data/english-names.json` file

The page should follow the same interaction model as the other generator pages:
- copy one
- copy all
- save favorites
- reset filters
- regenerate on control changes

- [ ] **Step 4: Sync or generate the deploy HTML**

After the source is done, run the site build so the generated output matches the source:

```bash
cd template-deploy
python3 build.py
```

Then copy the generated `template-deploy/output/random-english-name-generator.html` into `wordineer-deploy/random-english-name-generator.html` if the build step does not already update the deploy tree.

Expected: the built page contains the new SEO copy, the default `First name` selection, and the dedicated English dataset path.

- [ ] **Step 5: Re-run the page test**

Run:

```bash
node --test tests/english-generator-page.test.js
```

Expected: pass.

---

## Task 3: Wire the Tool Into Site Navigation

**Files:**
- Modify: `template-deploy/tools.json`
- Modify: `wordineer-deploy/name-generators.html`

- [ ] **Step 1: Add the English page to the tool lists**

Update the `name_generator_tools` section in `template-deploy/tools.json` so the new page appears with the rest of the name generator cards.

Use a description that keeps the scope clear:
- `England-focused first names, surnames, and full names.`

Also add it to any page lists where the current name generators are surfaced together, so the page is discoverable from the site’s existing navigation.

- [ ] **Step 2: Regenerate the site output**

Run:

```bash
cd template-deploy
python3 build.py
```

Expected: the navigation and related tool blocks include the English page.

- [ ] **Step 3: Verify the built navigation page**

Check `wordineer-deploy/name-generators.html` after the build:
- new English page link appears
- existing British and American pages remain untouched
- no broken links are introduced

---

## Task 4: Validate the Whole Feature

**Files:**
- Modify only if verification finds a defect

- [ ] **Step 1: Run all new tests**

Run:

```bash
node --test tests/english-names-data.test.js tests/english-generator-page.test.js
```

Expected: both tests pass.

- [ ] **Step 2: Validate the JSON syntax**

Run:

```bash
python3 -m json.tool wordineer-deploy/data/english-names.json > /dev/null
```

Expected: no output and exit code 0.

- [ ] **Step 3: Sanity-check the deployed page**

Open the generated page through the local HTTP server and verify:
- default `First name` selection
- mobile `More options` toggle
- filter changes automatically refresh the list
- copy/save actions work
- explainer text reads naturally and mentions English vs British names

- [ ] **Step 4: Commit**

```bash
git add template-deploy/tools-src/random-english-name-generator.html
git add template-deploy/tools.json
git add wordineer-deploy/data/english-names.json
git add wordineer-deploy/random-english-name-generator.html
git add wordineer-deploy/name-generators.html
git add tests/english-names-data.test.js
git add tests/english-generator-page.test.js
git commit -m "Add random English name generator"
```

---

## Self-Review Checklist

- The page is England-focused, not a duplicate of the British tool.
- `First name` is the default selection.
- The title and H1 support the `1100+` CTR angle honestly.
- The dataset contains at least 900 first names and at least 1100 total names.
- Mobile advanced filters are hidden behind `More options`.
- Filter changes trigger automatic regeneration.
- The site navigation includes the new page.
- Tests cover both dataset shape and page controls.

# Random British Name Generator Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a dedicated Random British Name Generator page with a dedicated `british-names.json` dataset of about 2500 tagged entries, short result notes, British-specific filters, and the high-CTR `2500+ UK Names` positioning.

**Architecture:** Follow the existing Wordineer static-generator pattern: source HTML in `template-deploy/tools-src/`, shared metadata in `template-deploy/tools.json`, generated output in `wordineer-deploy/`, and JSON data in `wordineer-deploy/data/`. Keep British-specific generation logic inside the British tool page, matching the American/Filipino pages' inline JavaScript pattern and reusing existing CSS classes and interactions.

**Tech Stack:** Plain HTML, CSS classes already in `styles/global.css`, vanilla JavaScript, JSON data loaded with `fetch('/data/british-names.json')`, Python static build script, Node.js built-in `assert`/`fs` for validation tests, manual HTTP-server testing.

---

## File Structure

- Create: `wordineer-deploy/data/british-names.json`
  - Dedicated British names dataset.
  - Contains about 2500 total tagged entries across `first`, `middle`, `last`, and `doubleLastParts`.
  - Uses compact arrays matching the approved design.

- Create: `tests/british-names-data.test.js`
  - Validates the JSON schema, total entry count, required filter coverage, and note length.
  - Runs with plain `node`, no package manager.

- Create: `tests/british-generator-page.test.js`
  - Static HTML checks for the source page and generated page.
  - Verifies title/meta text, filter controls, `More options`, result note markup, and `british-names.json` fetch reference.

- Create: `template-deploy/tools-src/random-british-name-generator.html`
  - Source page with config comment, metadata, hero, tool controls, explainer copy, FAQ, and inline British generator JavaScript.

- Modify: `template-deploy/tools.json`
  - Add or update homepage/tools metadata for Random British Name.
  - Ensure More Tools grid can include Random British Name.
  - Add planned Random Russian Name and Random Indian Name entries if the grid source requires explicit entries.

- Modify: `template-deploy/template/more-tools.html`
  - Change name-generator page subtitle from `Every word generator you need, all free` to `Every name generator you need, all free` if this shared fragment is used for the new page.

- Generated: `template-deploy/output/random-british-name-generator.html`
  - Created by `cd template-deploy && python3 build.py`.

- Generated: `wordineer-deploy/random-british-name-generator.html`
  - Production-ready static page. If `build.py` already writes directly to deploy, verify that output; if it only writes to `template-deploy/output/`, copy the reviewed generated file into `wordineer-deploy/`.

---

### Task 1: Add JSON Data Validation Test

**Files:**
- Create: `tests/british-names-data.test.js`
- Later validated file: `wordineer-deploy/data/british-names.json`

- [ ] **Step 1: Create the failing test**

Create `tests/british-names-data.test.js` with this content:

```javascript
const assert = require('assert');
const fs = require('fs');
const path = require('path');

const file = path.join(__dirname, '..', 'wordineer-deploy', 'data', 'british-names.json');
assert.ok(fs.existsSync(file), 'british-names.json should exist');

const data = JSON.parse(fs.readFileSync(file, 'utf8'));

const requiredTopKeys = ['first', 'middle', 'last', 'doubleLastParts'];
for (const key of requiredTopKeys) {
  assert.ok(Array.isArray(data[key]), `${key} should be an array`);
  assert.ok(data[key].length > 0, `${key} should not be empty`);
}

const totalEntries = data.first.length + data.middle.length + data.last.length + data.doubleLastParts.length;
assert.ok(totalEntries >= 2500, `expected at least 2500 entries, got ${totalEntries}`);
assert.ok(totalEntries <= 3200, `expected manageable dataset, got ${totalEntries}`);

const genders = new Set();
const styles = new Set();
const eras = new Set();
const regions = new Set();
const surnameTypes = new Set();

function assertShortNote(note, label) {
  assert.strictEqual(typeof note, 'string', `${label} note should be a string`);
  assert.ok(note.length > 0, `${label} note should not be empty`);
  assert.ok(note.length <= 90, `${label} note should stay short`);
}

for (const item of data.first) {
  assert.ok(Array.isArray(item), 'first item should be an array');
  assert.strictEqual(item.length, 6, `first item should have 6 fields: ${JSON.stringify(item)}`);
  const [name, gender, itemStyles, itemEras, itemRegions, note] = item;
  assert.strictEqual(typeof name, 'string', 'first name should be a string');
  assert.ok(/^[A-Z][A-Za-z' -]+$/.test(name), `first name should be title case: ${name}`);
  assert.ok(['m', 'f', 'u'].includes(gender), `invalid first gender: ${gender}`);
  assert.ok(Array.isArray(itemStyles) && itemStyles.length > 0, `${name} should have styles`);
  assert.ok(Array.isArray(itemEras) && itemEras.length > 0, `${name} should have eras`);
  assert.ok(Array.isArray(itemRegions) && itemRegions.length > 0, `${name} should have regions`);
  assertShortNote(note, name);
  genders.add(gender);
  itemStyles.forEach((value) => styles.add(value));
  itemEras.forEach((value) => eras.add(value));
  itemRegions.forEach((value) => regions.add(value));
}

for (const item of data.middle) {
  assert.ok(Array.isArray(item), 'middle item should be an array');
  assert.strictEqual(item.length, 6, `middle item should have 6 fields: ${JSON.stringify(item)}`);
  const [name, gender, itemStyles, itemEras, itemRegions, note] = item;
  assert.strictEqual(typeof name, 'string', 'middle name should be a string');
  assert.ok(['m', 'f', 'u'].includes(gender), `invalid middle gender: ${gender}`);
  assert.ok(Array.isArray(itemStyles) && itemStyles.length > 0, `${name} should have styles`);
  assert.ok(Array.isArray(itemEras) && itemEras.length > 0, `${name} should have eras`);
  assert.ok(Array.isArray(itemRegions) && itemRegions.length > 0, `${name} should have regions`);
  assertShortNote(note, name);
}

for (const item of data.last) {
  assert.ok(Array.isArray(item), 'last item should be an array');
  assert.strictEqual(item.length, 5, `last item should have 5 fields: ${JSON.stringify(item)}`);
  const [name, itemStyles, itemRegions, itemTypes, note] = item;
  assert.strictEqual(typeof name, 'string', 'last name should be a string');
  assert.ok(/^[A-Z][A-Za-z' -]+$/.test(name), `last name should be title case: ${name}`);
  assert.ok(Array.isArray(itemStyles) && itemStyles.length > 0, `${name} should have styles`);
  assert.ok(Array.isArray(itemRegions) && itemRegions.length > 0, `${name} should have regions`);
  assert.ok(Array.isArray(itemTypes) && itemTypes.length > 0, `${name} should have surname types`);
  assertShortNote(note, name);
  itemStyles.forEach((value) => styles.add(value));
  itemRegions.forEach((value) => regions.add(value));
  itemTypes.forEach((value) => surnameTypes.add(value));
}

for (const item of data.doubleLastParts) {
  assert.ok(Array.isArray(item), 'doubleLastParts item should be an array');
  assert.strictEqual(item.length, 4, `doubleLastParts item should have 4 fields: ${JSON.stringify(item)}`);
  const [name, itemStyles, itemRegions, note] = item;
  assert.strictEqual(typeof name, 'string', 'double-barrel part should be a string');
  assert.ok(Array.isArray(itemStyles) && itemStyles.length > 0, `${name} should have styles`);
  assert.ok(Array.isArray(itemRegions) && itemRegions.length > 0, `${name} should have regions`);
  assertShortNote(note, name);
}

for (const value of ['m', 'f', 'u']) assert.ok(genders.has(value), `missing gender ${value}`);
for (const value of ['common', 'classic', 'modern', 'old-fashioned', 'aristocratic', 'literary', 'unisex']) {
  assert.ok(styles.has(value), `missing style ${value}`);
}
for (const value of ['modern', '1990s-2000s', 'mid-century', 'victorian-edwardian', 'timeless']) {
  assert.ok(eras.has(value), `missing era ${value}`);
}
for (const value of ['english', 'scottish', 'welsh', 'northern-irish']) {
  assert.ok(regions.has(value), `missing region ${value}`);
}
for (const value of ['common-uk', 'occupational', 'place-based', 'patronymic', 'aristocratic', 'double-barrelled']) {
  assert.ok(surnameTypes.has(value), `missing surname type ${value}`);
}

console.log(`british-names.json ok: ${totalEntries} entries`);
```

- [ ] **Step 2: Run the test to verify it fails**

Run:

```bash
node tests/british-names-data.test.js
```

Expected:

```text
AssertionError [ERR_ASSERTION]: british-names.json should exist
```

- [ ] **Step 3: Commit the failing test**

```bash
git add tests/british-names-data.test.js
git commit -m "Add British names data validation"
```

---

### Task 2: Add `british-names.json`

**Files:**
- Create: `wordineer-deploy/data/british-names.json`

- [ ] **Step 1: Create the data file**

Create `wordineer-deploy/data/british-names.json` with this top-level shape:

```json
{
  "first": [],
  "middle": [],
  "last": [],
  "doubleLastParts": []
}
```

Populate the arrays with about 2500 total entries:

- `first`: at least 1000 entries.
- `middle`: at least 300 entries.
- `last`: at least 1000 entries.
- `doubleLastParts`: at least 200 entries.

Each `first` entry must use:

```json
["Eleanor", "f", ["classic", "literary"], ["victorian-edwardian", "timeless"], ["english"], "Classic English first name"]
```

Each `middle` entry must use:

```json
["Rose", "f", ["classic"], ["timeless"], ["english"], "Traditional British middle name"]
```

Each `last` entry must use:

```json
["Whitmore", ["classic", "aristocratic"], ["english"], ["place-based"], "English place-style surname"]
```

Each `doubleLastParts` entry must use:

```json
["Montgomery", ["aristocratic", "classic"], ["scottish", "english"], "Classic double-barrel surname part"]
```

Use only these enum values:

```javascript
const allowedGenders = ['m', 'f', 'u'];
const allowedStyles = ['common', 'classic', 'modern', 'old-fashioned', 'aristocratic', 'literary', 'unisex'];
const allowedEras = ['modern', '1990s-2000s', 'mid-century', 'victorian-edwardian', 'timeless'];
const allowedRegions = ['english', 'scottish', 'welsh', 'northern-irish'];
const allowedSurnameTypes = ['common-uk', 'occupational', 'place-based', 'patronymic', 'aristocratic', 'double-barrelled'];
```

Data quality rules:
- Names should be plausible British/UK names, not fantasy names.
- Use region tags as influence tags.
- Do not include addresses, phone numbers, NINO, birthdays, passwords, or fake identity data.
- Keep notes under 90 characters.
- Avoid duplicates inside the same array.
- It is fine for a first name to also appear in `middle`.

- [ ] **Step 2: Run JSON validation**

Run:

```bash
python3 -m json.tool wordineer-deploy/data/british-names.json >/dev/null
```

Expected: no output and exit code `0`.

- [ ] **Step 3: Run data test**

Run:

```bash
node tests/british-names-data.test.js
```

Expected:

```text
british-names.json ok: 2500 entries
```

The exact number may be higher than 2500, but it must be between 2500 and 3200.

- [ ] **Step 4: Check file size**

Run:

```bash
python3 - <<'PY'
from pathlib import Path
p = Path('wordineer-deploy/data/british-names.json')
print(round(p.stat().st_size / 1024, 1), 'KB')
PY
```

Expected: under `1000 KB`.

- [ ] **Step 5: Commit the dataset**

```bash
git add wordineer-deploy/data/british-names.json tests/british-names-data.test.js
git commit -m "Add British names dataset"
```

---

### Task 3: Add Static Page Validation Test

**Files:**
- Create: `tests/british-generator-page.test.js`
- Later validated files:
  - `template-deploy/tools-src/random-british-name-generator.html`
  - `wordineer-deploy/random-british-name-generator.html`

- [ ] **Step 1: Create the failing test**

Create `tests/british-generator-page.test.js` with this content:

```javascript
const assert = require('assert');
const fs = require('fs');
const path = require('path');

const root = path.join(__dirname, '..');
const sourcePath = path.join(root, 'template-deploy', 'tools-src', 'random-british-name-generator.html');
const deployPath = path.join(root, 'wordineer-deploy', 'random-british-name-generator.html');

assert.ok(fs.existsSync(sourcePath), 'source British page should exist');

const source = fs.readFileSync(sourcePath, 'utf8');

function mustInclude(haystack, needle, label) {
  assert.ok(haystack.includes(needle), `${label} should include ${needle}`);
}

mustInclude(source, 'CONFIG { "url": "/random-british-name-generator/"', 'source config');
mustInclude(source, '<title>Random British Name Generator - 2500+ UK Names', 'source title');
mustInclude(source, '2500+ UK-style', 'source hero copy');
mustInclude(source, 'fetch(\\'/data/british-names.json\\'', 'source data fetch');
mustInclude(source, 'id="bng-count"', 'source count control');
mustInclude(source, 'id="bng-mobile-toggle"', 'source mobile toggle');
mustInclude(source, 'id="bng-advanced"', 'source advanced panel');
mustInclude(source, 'id="bng-gender"', 'source gender filter');
mustInclude(source, 'id="bng-type"', 'source name type filter');
mustInclude(source, 'id="bng-style"', 'source style filter');
mustInclude(source, 'id="bng-region"', 'source region filter');
mustInclude(source, 'id="bng-era"', 'source era filter');
mustInclude(source, 'id="bng-surname-type"', 'source surname filter');
mustInclude(source, 'id="bng-letter"', 'source starts-with filter');
mustInclude(source, 'Double-barrelled full name', 'source double-barrel option');
mustInclude(source, 'What is a random British name generator?', 'source explainer');
mustInclude(source, 'Why use country-specific name generators?', 'source country explainer');
mustInclude(source, 'Every name generator you need, all free', 'source more tools subtitle');
mustInclude(source, 'Random Russian Name', 'source Russian cluster link text');
mustInclude(source, 'Random Indian Name', 'source Indian cluster link text');

const filterIds = ['bng-gender', 'bng-type', 'bng-style', 'bng-region', 'bng-era', 'bng-surname-type', 'bng-letter'];
for (const id of filterIds) {
  const changeBinding = `document.getElementById('${id}')?.addEventListener('change'`;
  mustInclude(source, changeBinding, `${id} auto-regenerate binding`);
}

if (fs.existsSync(deployPath)) {
  const deploy = fs.readFileSync(deployPath, 'utf8');
  mustInclude(deploy, 'Random British Name Generator - 2500+ UK Names', 'deploy title');
  mustInclude(deploy, '/data/british-names.json', 'deploy data fetch');
}

console.log('British generator page static checks ok');
```

- [ ] **Step 2: Run the test to verify it fails**

Run:

```bash
node tests/british-generator-page.test.js
```

Expected:

```text
AssertionError [ERR_ASSERTION]: source British page should exist
```

- [ ] **Step 3: Commit the failing test**

```bash
git add tests/british-generator-page.test.js
git commit -m "Add British generator page validation"
```

---

### Task 4: Create British Generator Source Page

**Files:**
- Create: `template-deploy/tools-src/random-british-name-generator.html`
- Test: `tests/british-generator-page.test.js`

- [ ] **Step 1: Create the source page**

Use `template-deploy/tools-src/random-american-name-generator.html` as the structural reference. Create `template-deploy/tools-src/random-british-name-generator.html` with:

- Config comment:

```html
<!-- CONFIG { "url": "/random-british-name-generator/", "output": "random-british-name-generator.html", "type": "tool" } -->
```

- Title:

```html
<title>Random British Name Generator - 2500+ UK Names | Wordineer</title>
```

- Canonical:

```html
<link rel="canonical" href="https://wordineer.com/random-british-name-generator/">
```

- Meta description:

```html
<meta name="description" content="Generate random British names from 2500+ UK name options. Filter by gender, style, era, region influence, surname type, and name format. Free, fast, no sign-up.">
```

- H1:

```html
<h1>Random British Name Generator</h1>
```

- Hero paragraph:

```html
<p>Generate random British names from 2500+ UK-style first names, surnames, middle names, and double-barrelled combinations. Filter by gender, name type, style, era, region influence, surname type, and starting letter.</p>
```

- Control IDs:

```html
id="bng-count"
id="bng-mobile-toggle"
id="bng-advanced"
id="bng-gender"
id="bng-type"
id="bng-style"
id="bng-region"
id="bng-era"
id="bng-surname-type"
id="bng-letter"
id="bng-gen-btn"
id="bng-reset-btn"
id="bng-results"
id="bng-saved-tags"
id="bng-copy-saved-btn"
```

- Name type options:

```html
<option value="full">Full name</option>
<option value="first">First name</option>
<option value="last">Last name</option>
<option value="middle-full">First + middle + last</option>
<option value="double-full">Double-barrelled full name</option>
```

- Region options:

```html
<option value="any">Any influence</option>
<option value="english">English</option>
<option value="scottish">Scottish</option>
<option value="welsh">Welsh</option>
<option value="northern-irish">Northern Irish</option>
```

- Surname type options:

```html
<option value="any">Any surname</option>
<option value="common-uk">Common UK</option>
<option value="occupational">Occupational</option>
<option value="place-based">Place-based</option>
<option value="patronymic">Patronymic</option>
<option value="aristocratic">Aristocratic</option>
<option value="double-barrelled">Double-barrelled</option>
```

- Explainer sections:

```html
<h2>What is a random British name generator?</h2>
<p>A random British name generator creates first names, last names, and full names inspired by naming patterns from the United Kingdom. Instead of using one generic random name generator for every culture, this tool focuses on British-style names, including common UK surnames, classic given names, modern names, regional influences, and double-barrelled surnames.</p>

<h2>How it works</h2>
<p>Choose how many names you want, then adjust the filters. You can generate male, female, or neutral names, switch between first names and full names, choose a style or era, and narrow the region influence or surname type. When you change a filter, the list updates automatically so you can compare name ideas quickly.</p>

<h2>Why use country-specific name generators?</h2>
<p>Names are shaped by culture, language, history, and local naming habits. A random Filipino name generator, random Japanese name generator, and random British name generator should not all use the same filter structure because each country has different naming patterns. Country-specific tools give better results because the filters, name data, and combinations are built around the culture where each name fits.</p>
```

- British inline JavaScript must:
  - Fetch `/data/british-names.json`.
  - Map compact arrays into objects.
  - Validate count from 1 to 50.
  - Generate all five name types.
  - Build a short note from the selected first/last/middle entries.
  - Bind `change` listeners for every filter.
  - Bind the `More options` mobile toggle.
  - Reset controls to defaults.

**Architecture note:** Follow the `random-american-name-generator.html` pattern exactly. Use `WORDINEER.init({ mode: 'custom', ... })` — do NOT invent a custom `bngBind`/`bngGenerate` pattern. The WORDINEER engine calls your `generateFn` and `renderItem` callbacks. Load data with a deferred fetch that calls `bngApplyData(raw)` and then fires the generate button.

Required inline JS structure (adapt from the American generator, replacing `ang` → `bng`):

```javascript
// 1. Label maps
const BNG_LABELS = { gender: {...}, style: {...}, region: {...}, surnameType: {...} };

// 2. Fallback data (12 first, 4 middle, 6 last, 4 doubleLastParts embedded inline)
const FALLBACK_BRITISH_NAMES = { first: [...], middle: [...], last: [...], doubleLastParts: [...] };

// 3. Map compact arrays → objects
function bngMapData(raw) { /* index 4 = regions, index 5 = note for first/middle */ }

// 4. Active data object starts from fallback
const bngActiveData = bngMapData(FALLBACK_BRITISH_NAMES);
let bngDataLoaded = false;
let bngDataPromise = null;
let bngRenderedFallback = false;

// 5. Apply full data when loaded
function bngApplyData(raw) { /* update bngActiveData in-place, set bngDataLoaded = true */ }

// 6. Deferred fetch
function bngLoadData() { /* fetch('/data/british-names.json', ...) then bngApplyData */ }

// 7. Filter helpers
function bngFilterFirstLike(rows, gender, era, style, region, letter) {}
function bngFilterLast(rows, region, surnameType) {}
function bngFilterDoubleParts(rows, region) {}

// 8. generateFn — returns array of { display, note, chips }
// Handles types: 'full', 'first', 'last', 'middle-full', 'double-full'
function bngGenerateFn(data) {}

// 9. renderItem — returns HTML string for one result card
function bngRenderItem(item) {}

// 10. Wire up via WORDINEER.init
WORDINEER.init({
  mode: 'custom',
  data: bngActiveData,
  renderItem: bngRenderItem,
  generateFn: bngGenerateFn,
  listId: 'bng-list',
  countDisplayId: 'bng-count-display',
  generateBtnId: 'bng-gen-btn',
  copyAllBtnId: 'bng-copy-all-btn',
  savedKey: 'wnr_saved_british_names',
  savedListId: 'bng-saved-tags'
});

// 11. Event listeners: count input, all 7 filter selects, reset button, copy-saved, mobile toggle
// 12. bindWordineerMenu() — copy verbatim from American generator
```

See `template-deploy/tools-src/random-american-name-generator.html` lines 312–691 for the complete working reference. All `ang` → `bng`, and add `regions`/`surnameType` filter fields that the American page doesn't have.

- [ ] **Step 2: Run page static test**

Run:

```bash
node tests/british-generator-page.test.js
```

Expected:

```text
British generator page static checks ok
```

- [ ] **Step 3: Commit the source page**

```bash
git add template-deploy/tools-src/random-british-name-generator.html tests/british-generator-page.test.js
git commit -m "Add British name generator page source"
```

---

### Task 5: Update Tool Metadata and More Tools Text

**Files:**
- Modify: `template-deploy/tools.json`
- Modify: `template-deploy/template/more-tools.html`
- Test: `tests/british-generator-page.test.js`

- [ ] **Step 1: Verify tools.json already has British entries**

`tools.json` already has two British entries added in a previous commit (lines ~193 and ~411). Confirm they exist:

```bash
grep -c "random-british-name-generator" template-deploy/tools.json
```

Expected: `2`. If the count is `0`, add entries matching the Japanese/American pattern. If `2`, no changes needed — skip to Step 2.

- [ ] **Step 2: Update More Tools subtitle**

In `template-deploy/template/more-tools.html`, change:

```html
<p class="section-sub">Every word generator you need, all free</p>
```

to:

```html
<p class="section-sub">Every name generator you need, all free</p>
```

For pages where a broader word-tools subtitle is still needed, make the British page source include its own More Tools section rather than changing all tools globally. Prefer the smaller scoped change if changing the shared fragment would make non-name tools read incorrectly.

- [ ] **Step 3: Run JSON validation**

Run:

```bash
python3 -m json.tool template-deploy/tools.json >/dev/null
```

Expected: no output and exit code `0`.

- [ ] **Step 4: Run static page test**

Run:

```bash
node tests/british-generator-page.test.js
```

Expected:

```text
British generator page static checks ok
```

- [ ] **Step 5: Commit metadata changes**

```bash
git add template-deploy/tools.json template-deploy/template/more-tools.html tests/british-generator-page.test.js
git commit -m "Update name generator tool links"
```

---

### Task 5b: Add Clean-URL Redirect Rules

**Files:**
- Modify: `wordineer-deploy/_redirects`

- [ ] **Step 1: Add two lines to `_redirects`**

Open `wordineer-deploy/_redirects`. Add one line to the 301-redirect block and one to the 200-rewrite block, matching the Japanese pattern directly above:

301 block — add after the Japanese line:
```
/random-british-name-generator.html    /random-british-name-generator/    301
```

200 rewrite block — add after the Japanese line:
```
/random-british-name-generator/    /random-british-name-generator.html    200
```

- [ ] **Step 2: Verify syntax**

```bash
grep british /Users/garrickdeetan/Documents/Random\ Word\ Generator\ Tool\ Site/wordineer-deploy/_redirects
```

Expected: two matching lines — one with `301`, one with `200`.

- [ ] **Step 3: Commit**

```bash
git add wordineer-deploy/_redirects
git commit -m "Add clean-URL redirect for British name generator"
```

---

### Task 6: Build and Deploy Static Output

**Files:**
- Generated: `template-deploy/output/random-british-name-generator.html`
- Create or update: `wordineer-deploy/random-british-name-generator.html`

- [ ] **Step 1: Run template build**

Run:

```bash
cd template-deploy
python3 build.py
```

Expected: build completes without traceback.

- [ ] **Step 2: Verify generated source output exists**

Run:

```bash
test -f template-deploy/output/random-british-name-generator.html && echo "template output exists"
```

Expected:

```text
template output exists
```

- [ ] **Step 3: Ensure deploy page exists**

If `wordineer-deploy/random-british-name-generator.html` was not created by the build, copy the reviewed generated output into deploy:

```bash
cp template-deploy/output/random-british-name-generator.html wordineer-deploy/random-british-name-generator.html
```

- [ ] **Step 4: Run static page test against deploy output**

Run:

```bash
node tests/british-generator-page.test.js
```

Expected:

```text
British generator page static checks ok
```

- [ ] **Step 5: Commit built output**

```bash
git add template-deploy/output/random-british-name-generator.html wordineer-deploy/random-british-name-generator.html
git commit -m "Build British name generator page"
```

---

### Task 7: Manual HTTP Verification

**Files:**
- Verify: `wordineer-deploy/random-british-name-generator.html`
- Verify: `wordineer-deploy/data/british-names.json`

- [ ] **Step 1: Start local server**

Run:

```bash
cd wordineer-deploy
python3 -m http.server 8080
```

Expected:

```text
Serving HTTP on :: port 8080
```

If port `8080` is busy, use:

```bash
cd wordineer-deploy
python3 -m http.server 8081
```

- [ ] **Step 2: Open manual test URL**

Open:

```text
http://localhost:8080/random-british-name-generator/
```

If using port `8081`, open:

```text
http://localhost:8081/random-british-name-generator/
```

- [ ] **Step 3: Verify desktop behavior**

Check:
- Page title/intro uses `2500+ UK Names` or `2500+ UK-style`.
- Results appear on load.
- Each result shows a name and a short note.
- `Gender` change from male to female automatically regenerates female names.
- `Region influence` changes notes or name pools.
- `Double-barrelled full name` generates hyphenated surnames.
- `Surname type: Double-barrelled` generates hyphenated surnames.
- Copy one result works.
- Save one result works.
- Copy saved names works.
- Browser console has no errors.

- [ ] **Step 4: Verify mobile behavior**

Use browser responsive mode or a narrow viewport.

Check:
- `Number of names` appears before advanced filters.
- `More options` opens below the count field.
- The button changes to `Hide options` when open.
- Filter changes still auto-regenerate.
- Text does not overlap or overflow.

- [ ] **Step 5: Stop server**

Stop the server with `Ctrl-C`.

- [ ] **Step 6: Commit any manual fixes**

If manual verification required changes:

```bash
git add template-deploy/tools-src/random-british-name-generator.html template-deploy/output/random-british-name-generator.html wordineer-deploy/random-british-name-generator.html wordineer-deploy/data/british-names.json tests/british-names-data.test.js tests/british-generator-page.test.js
git commit -m "Fix British name generator verification issues"
```

---

### Task 8: Final Verification

**Files:**
- Verify all created/modified files.

- [ ] **Step 1: Run all validation commands**

Run:

```bash
python3 -m json.tool wordineer-deploy/data/british-names.json >/dev/null
python3 -m json.tool template-deploy/tools.json >/dev/null
node tests/british-names-data.test.js
node tests/british-generator-page.test.js
```

Expected:

```text
british-names.json ok: 2500 entries
British generator page static checks ok
```

The entry count may be higher than 2500 but must stay between 2500 and 3200.

- [ ] **Step 2: Check git diff**

Run:

```bash
git diff --stat
git status --short
```

Expected:
- Only British generator files, tests, metadata, and generated output are changed by this implementation.
- Existing unrelated dirty-worktree files remain untouched.

- [ ] **Step 3: Final commit if needed**

If any uncommitted implementation changes remain:

```bash
git add docs/superpowers/plans/2026-05-08-random-british-name-generator.md tests/british-names-data.test.js tests/british-generator-page.test.js wordineer-deploy/data/british-names.json template-deploy/tools-src/random-british-name-generator.html template-deploy/tools.json template-deploy/template/more-tools.html template-deploy/output/random-british-name-generator.html wordineer-deploy/random-british-name-generator.html
git commit -m "Add random British name generator"
```

---

## Self-Review Notes

Spec coverage:
- Dedicated page: Task 4 and Task 6.
- Dedicated JSON file: Task 2.
- Around 2500 names and high-CTR title: Task 1, Task 2, Task 4.
- English, Scottish, Welsh, Northern Irish region influence: Task 1, Task 2, Task 4.
- Short notes under results: Task 2 and Task 4.
- Same mobile `More options` pattern: Task 4 and Task 7.
- Auto-regenerate on filter changes: Task 3, Task 4, Task 7.
- More Tools subtitle and name-generator list: Task 5.
- Manual HTTP testing: Task 7.

Placeholder scan:
- No placeholder markers or unspecified future work.
- Large data creation is constrained by exact schema, counts, enums, quality rules, and validation tests rather than inline listing 2500 entries in the plan.

Type consistency:
- Data arrays match the spec:
  - `first`: `[name, gender, styles, eras, regions, note]`
  - `middle`: `[name, gender, styles, eras, regions, note]`
  - `last`: `[name, styles, regions, types, note]`
  - `doubleLastParts`: `[name, styles, regions, note]`
- Page IDs use the `bng-` prefix consistently.
- Filter values match the validation test enums.

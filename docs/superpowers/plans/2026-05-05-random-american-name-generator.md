# Random American Name Generator - Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a dedicated `/random-american-name-generator/` tool page with its own American names JSON dataset, realistic first/middle/last name generation, gender/type/era/style/surname/letter filters, copy/save features, SEO copy, and internal links from the random name generator cluster.

**Architecture:** New `american-names.json` data file independent of `words.json`; new `tools-src/random-american-name-generator.html` following the current random name generator and random Filipino name generator UX; template build generates the deploy HTML; `tools.json`, `_redirects`, and related name-generator content link the new page.

**Tech Stack:** Static HTML/CSS/JS, existing Wordineer custom generator pattern, static JSON fetched from `/data/american-names.json`, Python build system (`template-deploy/build.py`), Cloudflare Pages.

---

## Files

| Action | Path |
|---|---|
| Create | `wordineer-deploy/data/american-names.json` |
| Create | `template-deploy/tools-src/random-american-name-generator.html` |
| Modify | `template-deploy/tools.json` |
| Modify | `template-deploy/tools-src/random-name-generator.html` |
| Modify | `template-deploy/tools-src/random-filipino-name-generator.html` |
| Modify | `wordineer-deploy/_redirects` |
| Generated | `wordineer-deploy/random-american-name-generator.html` |

---

## Task 1: Create `wordineer-deploy/data/american-names.json`

**Files:**
- Create: `wordineer-deploy/data/american-names.json`

- [ ] **Step 1: Create the JSON data file**

Create `wordineer-deploy/data/american-names.json` with this schema:

```json
{
  "first": [
    ["James", "m", ["classic", "common"], ["all", "1950s", "1970s", "1980s", "1990s", "2000s", "modern"], "classic American male first name"]
  ],
  "middle": [
    ["Lee", "u", ["classic", "southern"], ["all"], "common American middle name"]
  ],
  "last": [
    ["Smith", ["common-us", "english"], "common American surname"]
  ]
}
```

Required fields:
- `first`: array of `[name, gender, styles, eras, note]`
- `middle`: array of `[name, gender, styles, eras, note]`
- `last`: array of `[name, styles, note]`

Allowed `gender` values:
- `m`
- `f`
- `u`

Allowed first/middle `styles`:
- `common`
- `classic`
- `modern`
- `old-fashioned`
- `southern`
- `unisex`

Allowed last-name `styles`:
- `common-us`
- `english`
- `hispanic`
- `irish-scottish`
- `german`
- `italian`
- `french`
- `multicultural`

Allowed `eras`:
- `all`
- `early-1900s`
- `1950s`
- `1970s`
- `1980s`
- `1990s`
- `2000s`
- `modern`

MVP data minimum:
- `first`: at least 300 entries.
- `middle`: at least 100 entries.
- `last`: at least 250 entries.
- Every first/middle entry has at least one style and one era.
- Every last entry has at least one style.
- Notes stay under 80 characters.
- Names use plain ASCII unless a specific name convention needs punctuation, such as `O'Brien`.

Starter first-name coverage:
- Male common/classic: James, John, Robert, Michael, William, David, Richard, Joseph, Thomas, Charles, Christopher, Daniel, Matthew, Anthony, Mark, Donald, Steven, Paul, Andrew, Joshua, Kenneth, Kevin, Brian, George, Edward.
- Female common/classic: Mary, Patricia, Jennifer, Linda, Elizabeth, Barbara, Susan, Jessica, Sarah, Karen, Nancy, Lisa, Betty, Margaret, Sandra, Ashley, Kimberly, Emily, Donna, Michelle, Carol, Amanda, Melissa, Deborah, Stephanie.
- Modern male: Liam, Noah, Oliver, Theodore, Henry, Mateo, Elijah, Lucas, Levi, Sebastian, Jack, Ezra, Asher, Leo, Hudson, Luca, Grayson, Wyatt, Maverick, Carter.
- Modern female: Olivia, Emma, Amelia, Charlotte, Mia, Sophia, Isabella, Evelyn, Ava, Sofia, Luna, Harper, Camila, Eleanor, Violet, Aurora, Hazel, Chloe, Nova, Riley.
- Unisex: Taylor, Jordan, Morgan, Casey, Riley, Avery, Quinn, Parker, Rowan, Cameron, Reese, Skyler, Dakota, Hayden, Emerson, Finley, Blake, Sage, River, Logan.
- Old-fashioned: Walter, Harold, Clarence, Eugene, Arthur, Albert, Howard, Leonard, Dorothy, Helen, Ruth, Mildred, Florence, Ethel, Pearl, Clara, Edith, Mabel, Beatrice, Thelma.
- Southern style: Beau, Rhett, Waylon, Wyatt, Cash, Boone, Colton, Dallas, Sawyer, Walker, Jolene, Savannah, Scarlett, Magnolia, Daisy, Georgia, June, Belle, Dixie, Cheyenne.

Starter middle-name coverage:
- Neutral/classic: Lee, Lynn, Ray, Jean, Francis, Blair, Morgan, Taylor, Jordan, Quinn.
- Female/classic: Anne, Marie, Rose, Grace, Jane, Mae, Elizabeth, Claire, Louise, Ruth.
- Male/classic: James, John, William, Joseph, Thomas, Edward, Michael, David, Allen, Wayne.
- Southern/old-fashioned: Jo, Sue, Pearl, Belle, Mae, Lou, Ray, Earl, Dean, Clyde.

Starter surname coverage:
- Common US/English: Smith, Johnson, Williams, Brown, Jones, Miller, Davis, Wilson, Anderson, Thomas, Taylor, Moore, Martin, Jackson, Thompson, White, Harris, Clark, Lewis, Robinson.
- Hispanic: Garcia, Rodriguez, Martinez, Hernandez, Lopez, Gonzalez, Perez, Sanchez, Ramirez, Torres, Flores, Rivera, Gomez, Diaz, Cruz, Morales, Ortiz, Gutierrez, Chavez, Ramos.
- Irish/Scottish: Murphy, Kelly, Sullivan, Campbell, Stewart, Murray, McDonald, Kennedy, Ryan, O'Brien, Walsh, Ferguson, Hamilton, Robertson, Wallace, Graham, Johnston, Burns, Morrison, Boyd.
- German: Miller, Meyer, Schmidt, Schneider, Fischer, Weber, Wagner, Keller, Hoffman, Zimmerman, Hartman, Klein, Wolf, Becker, Schwarz, Bauer, Frank, Peters, Arnold, Kramer.
- Italian: Russo, Romano, Marino, Ferrari, Esposito, Ricci, Lombardi, Greco, Bruno, Gallo, Conti, DeLuca, Rizzo, Costa, Moretti, Bellini, Vitale, Leone, Caruso, Bianchi.
- French: Martin, Bernard, Dubois, Laurent, Moreau, Fournier, Girard, Lambert, Fontaine, Rousseau, Vincent, Marchand, Dupont, LeBlanc, Boucher, Gauthier, Chevalier, Roy, Perrault, Arnaud.
- Multicultural/common US: Nguyen, Kim, Patel, Singh, Khan, Ali, Chen, Wang, Lee, Park, Young, Allen, King, Wright, Scott, Green, Baker, Adams, Nelson, Carter.

- [ ] **Step 2: Validate JSON**

Run:

```bash
python3 -m json.tool wordineer-deploy/data/american-names.json >/dev/null
```

Expected:
- Command exits successfully.
- No JSON parse errors.

- [ ] **Step 3: Check minimum counts and schema consistency**

Run:

```bash
node -e "const fs=require('fs'); const d=JSON.parse(fs.readFileSync('wordineer-deploy/data/american-names.json','utf8')); const allowedG=new Set(['m','f','u']); const allowedFirstStyles=new Set(['common','classic','modern','old-fashioned','southern','unisex']); const allowedLastStyles=new Set(['common-us','english','hispanic','irish-scottish','german','italian','french','multicultural']); const allowedEras=new Set(['all','early-1900s','1950s','1970s','1980s','1990s','2000s','modern']); const bad=[]; for(const [i,row] of d.first.entries()){ if(row.length!==5) bad.push('first '+i+' length'); if(!allowedG.has(row[1])) bad.push('first '+i+' gender'); if(!Array.isArray(row[2])||!row[2].every(x=>allowedFirstStyles.has(x))) bad.push('first '+i+' styles'); if(!Array.isArray(row[3])||!row[3].every(x=>allowedEras.has(x))) bad.push('first '+i+' eras'); if(typeof row[4]!=='string'||row[4].length>80) bad.push('first '+i+' note'); } for(const [i,row] of d.middle.entries()){ if(row.length!==5) bad.push('middle '+i+' length'); if(!allowedG.has(row[1])) bad.push('middle '+i+' gender'); if(!Array.isArray(row[2])||!row[2].every(x=>allowedFirstStyles.has(x))) bad.push('middle '+i+' styles'); if(!Array.isArray(row[3])||!row[3].every(x=>allowedEras.has(x))) bad.push('middle '+i+' eras'); if(typeof row[4]!=='string'||row[4].length>80) bad.push('middle '+i+' note'); } for(const [i,row] of d.last.entries()){ if(row.length!==3) bad.push('last '+i+' length'); if(!Array.isArray(row[1])||!row[1].every(x=>allowedLastStyles.has(x))) bad.push('last '+i+' styles'); if(typeof row[2]!=='string'||row[2].length>80) bad.push('last '+i+' note'); } if(d.first.length<300) bad.push('first count '+d.first.length); if(d.middle.length<100) bad.push('middle count '+d.middle.length); if(d.last.length<250) bad.push('last count '+d.last.length); if(bad.length){ console.error(bad.join('\\n')); process.exit(1); } console.log({first:d.first.length,middle:d.middle.length,last:d.last.length});"
```

Expected:
- Prints counts.
- Exits successfully.

---

## Task 2: Update `template-deploy/tools.json`

**Files:**
- Modify: `template-deploy/tools.json`

- [ ] **Step 1: Add the new tool to the name tools cluster**

Find the existing name generator entries. Add:

```json
{ "href": "/random-american-name-generator/", "text": "American name" }
```

Placement:
- Near the existing `Random name` and `Filipino name` entries.
- Keep existing JSON formatting style.

- [ ] **Step 2: Validate JSON**

Run:

```bash
python3 -m json.tool template-deploy/tools.json >/dev/null
```

Expected:
- Command exits successfully.
- No JSON parse errors.

- [ ] **Step 3: Confirm entry exists exactly once**

Run:

```bash
node -e "const fs=require('fs'); const s=fs.readFileSync('template-deploy/tools.json','utf8'); const n=(s.match(/random-american-name-generator/g)||[]).length; console.log(n); if(n!==1) process.exit(1);"
```

Expected:
- Prints `1`.

---

## Task 3: Create `template-deploy/tools-src/random-american-name-generator.html`

**Files:**
- Create: `template-deploy/tools-src/random-american-name-generator.html`

- [ ] **Step 1: Use the existing tool-source structure**

Create the page with:

```html
<!-- CONFIG { "url": "/random-american-name-generator/", "output": "random-american-name-generator.html", "type": "tool" } -->
```

Required slots:
- `<!-- SLOT:meta -->`
- `<!-- SLOT:main -->`

Use the current `random-filipino-name-generator.html` and `random-name-generator.html` source structure for:
- header/nav/footer integration.
- generator card structure.
- count input pattern.
- mobile options toggle.
- results list.
- saved tags.
- toast element.
- copy/save button behavior.

- [ ] **Step 2: Add SEO metadata**

Use:

```html
<title>Random American Name Generator - Realistic US Names | Wordineer</title>
<meta name="description" content="Generate random American names instantly. Create realistic first names, last names, full names, and middle-name combinations by gender, era, style, and starting letter. Free, no sign-up.">
<link rel="canonical" href="https://wordineer.com/random-american-name-generator/">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Wordineer">
<meta property="og:title" content="Random American Name Generator | Wordineer">
<meta property="og:description" content="Create realistic American names for characters, stories, games, baby name ideas, pen names, and writing prompts. Filter by gender, era, style, and name type.">
<meta property="og:url" content="https://wordineer.com/random-american-name-generator/">
<meta property="og:image" content="https://wordineer.com/og-image.png">
```

Add FAQPage JSON-LD for these six questions:
- `Are these real people?`
- `Can I use these names in a story or game?`
- `What makes a name American?`
- `Can I generate old-fashioned American names?`
- `How is this different from the random name generator?`
- `Does this tool generate fake identities?`

- [ ] **Step 3: Add generator controls**

Use these IDs:
- Count input: `ang-count`
- Count error: `ang-count-error`
- Mobile toggle: `ang-mobile-toggle`
- Advanced panel: `ang-advanced`
- Gender select: `ang-gender`
- Type select: `ang-type`
- Era select: `ang-era`
- Style select: `ang-style`
- Last background select: `ang-last-style`
- Letter select: `ang-letter`
- Generate button: `ang-gen-btn`
- Reset button: `ang-reset-btn`
- Count display: `ang-count-display`
- Copy all button: `ang-copy-all-btn`
- Result list: `ang-list`
- Copy saved button: `ang-copy-saved-btn`
- Saved tags: `ang-saved-tags`

Control values:

Gender:
```html
<option value="any">Any</option>
<option value="f">Female</option>
<option value="m">Male</option>
<option value="u">Neutral</option>
```

Name type:
```html
<option value="full">Full name</option>
<option value="first">First name</option>
<option value="last">Last name</option>
<option value="middle-full">First + middle + last</option>
```

Era:
```html
<option value="any">Any era</option>
<option value="modern">Modern</option>
<option value="2000s">2000s</option>
<option value="1990s">1990s</option>
<option value="1980s">1980s</option>
<option value="1970s">1970s</option>
<option value="1950s">1950s</option>
<option value="early-1900s">Early 1900s</option>
```

Style:
```html
<option value="any">Any style</option>
<option value="common">Common</option>
<option value="classic">Classic</option>
<option value="modern">Modern</option>
<option value="old-fashioned">Old-fashioned</option>
<option value="southern">Southern</option>
<option value="unisex">Unisex</option>
```

Last name background:
```html
<option value="any">Any background</option>
<option value="common-us">Common US</option>
<option value="english">English / European</option>
<option value="hispanic">Hispanic American</option>
<option value="irish-scottish">Irish / Scottish</option>
<option value="german">German</option>
<option value="italian">Italian</option>
<option value="french">French</option>
<option value="multicultural">Multicultural</option>
```

Starts with:
- `any`
- `a` through `z`

- [ ] **Step 4: Add page-specific JavaScript**

Use an IIFE in the tool source, following the current custom generator pattern. It must:
- Fetch `/data/american-names.json`.
- Fall back to local fallback data if fetch fails.
- Generate initial results on page load.
- Support count 1-50.
- Support gender, name type, era, style, last background, and first-letter filters.
- Support copy one, save one, copy all, copy saved, reset.
- Update `ang-count-display`.
- Keep mobile advanced toggle behavior.

Required fallback data:

```js
const FALLBACK_AMERICAN_NAMES = {
  first: [
    ["James","m",["classic","common"],["all","1950s","1970s","1980s","1990s","2000s","modern"],"classic American male first name"],
    ["Olivia","f",["modern","common"],["2000s","modern"],"popular modern American female name"],
    ["Taylor","u",["modern","unisex"],["1980s","1990s","2000s","modern"],"common unisex first name"],
    ["John","m",["classic","common"],["all","1950s","1970s","1980s"],"familiar American male first name"],
    ["Mary","f",["classic","common"],["all","early-1900s","1950s"],"classic American female first name"],
    ["Avery","u",["modern","unisex"],["2000s","modern"],"modern unisex first name"]
  ],
  middle: [
    ["Lee","u",["classic","southern"],["all"],"common American middle name"],
    ["Anne","f",["classic"],["all"],"traditional female middle name"],
    ["James","m",["classic"],["all"],"traditional male middle name"],
    ["Grace","f",["classic","modern"],["all","modern"],"common female middle name"]
  ],
  last: [
    ["Smith",["common-us","english"],"common American surname"],
    ["Johnson",["common-us","english"],"common American surname"],
    ["Garcia",["common-us","hispanic"],"common Hispanic American surname"],
    ["Murphy",["irish-scottish"],"Irish-origin surname common in the US"],
    ["Miller",["common-us","german","english"],"common American surname"],
    ["Nguyen",["multicultural"],"common Vietnamese American surname"]
  ]
};
```

Required generation helper behavior:

```js
function filterFirstLike(rows, gender, era, style, letter) {
  let out = rows.slice();
  if (gender !== 'any') out = out.filter(row => row[1] === gender);
  if (era !== 'any') out = out.filter(row => row[3].includes(era) || row[3].includes('all'));
  if (style !== 'any') out = out.filter(row => row[2].includes(style));
  if (letter !== 'any') out = out.filter(row => row[0].toLowerCase().startsWith(letter));
  return out;
}

function filterLast(rows, lastStyle) {
  if (lastStyle === 'any') return rows.slice();
  return rows.filter(row => row[1].includes(lastStyle));
}
```

Fallback broadening rules:
- If first-name filtering returns zero, retry without style.
- If still zero, retry without era.
- If still zero, retry with gender only.
- If still zero, use all first names.
- If middle-name filtering returns zero, retry with gender only, then all middle names.
- If surname filtering returns zero, use all surnames.

Generated result object:

```js
{
  name: "Ava Grace Miller",
  note: "Modern American full name",
  chips: ["female", "modern", "common US surname"]
}
```

Result card requirements:
- Main name in a readable heading/span.
- Note under the name.
- Chips below note.
- Copy/save icon buttons consistent with existing site style.

- [ ] **Step 5: Add SEO body sections**

Add these sections after the tool:
- `What is a random American name generator?`
- `How it works`
- `American name styles`
- `Ways to use the tool`
- `Related name generators`
- `Frequently asked questions`

Use this copy exactly unless it needs minor grammar adjustment to fit existing page tone:

```html
<h2>What is a random American name generator?</h2>
<p>A random American name generator creates name combinations that sound natural in the United States. Instead of building names from random letters, it uses familiar American first names, middle names, and surnames to produce believable results for characters, writing prompts, role-playing games, and brainstorming.</p>
<p>This page is more focused than a broad random name generator. It is designed for names that feel American in spelling, rhythm, and surname pairing, while still reflecting the mix of naming influences used across the United States.</p>

<h2>How it works</h2>
<p>Choose how many names you want, select a gender or neutral mix, pick a name type, and optionally filter by era, style, surname background, or first letter. The tool combines first names, middle names, and surnames from American name lists to create realistic results.</p>
<p>You can copy a single name, copy the full list, or save favorites while you compare options.</p>

<h2>American name styles</h2>
<p>American names come from many sources, including English, Spanish, Irish, German, Italian, French, Biblical, modern, and pop culture naming patterns. That mix is why names like James Miller, Sophia Garcia, Madison Brooks, and Elijah Johnson can all feel American in different ways.</p>

<h2>Ways to use the tool</h2>
<p>Use the generator for fictional characters, tabletop game NPCs, baby name brainstorming, pen names, online aliases, classroom writing prompts, design mockups, and sample content.</p>

<h2>Related name generators</h2>
<p>Need a different style of name? Try the <a href="/random-name-generator.html">random name generator</a> for mixed origins, the <a href="/random-filipino-name-generator/">random Filipino name generator</a> for Filipino names, or the random British name generator when that page is available.</p>
```

FAQ answer copy:

```html
<p>No. The tool creates fictional combinations from name lists. A generated name may coincidentally match a real person, but the results are not identity records.</p>
<p>Yes. These names are useful for fictional characters, RPG NPCs, screenplays, short stories, writing exercises, and other creative projects.</p>
<p>American names often combine first names used in the United States with common surnames from many cultural backgrounds. The result can include English, Spanish, Irish, German, Italian, French, Biblical, modern, and pop culture influences.</p>
<p>Yes. Use the era and style filters to generate classic, vintage, or early twentieth-century name combinations.</p>
<p>The random name generator covers many origins and name styles. This page focuses on names that feel natural in an American context.</p>
<p>No. It only generates names. It does not create addresses, SSNs, phone numbers, passwords, credit card numbers, or other identity details.</p>
```

---

## Task 4: Update `template-deploy/tools-src/random-name-generator.html`

**Files:**
- Modify: `template-deploy/tools-src/random-name-generator.html`

- [ ] **Step 1: Add internal link to the American page**

Find the existing "More name generators" or related-name section. Add a link/card for:

```html
<a href="/random-american-name-generator/">Random American Name Generator</a>
```

Use nearby text:

```html
Generate realistic American first names, surnames, and full names by gender, era, style, and starting letter.
```

- [ ] **Step 2: Keep cluster links natural**

The pillar page should include:
- one exact-match phrase: `random American name generator`
- one natural descriptive phrase: `realistic American names`

Do not add repeated exact-match anchors in multiple nearby paragraphs.

---

## Task 5: Update `template-deploy/tools-src/random-filipino-name-generator.html`

**Files:**
- Modify: `template-deploy/tools-src/random-filipino-name-generator.html`

- [ ] **Step 1: Add related link to the American page**

Find the related name generators section. Add:

```html
<a href="/random-american-name-generator/">Random American Name Generator</a>
```

Use nearby text:

```html
Create realistic American names with gender, era, style, and surname filters.
```

- [ ] **Step 2: Keep existing Filipino copy focused**

Do not rewrite the Filipino tool's main SEO sections. Only add the related link/card where similar related tools already appear.

---

## Task 6: Add Redirect Rule

**Files:**
- Modify: `wordineer-deploy/_redirects`

- [ ] **Step 1: Add HTML-to-directory redirect**

Add this rule:

```text
/random-american-name-generator.html  /random-american-name-generator/  301
```

Placement:
- Near other generator redirects.
- Do not remove existing redirects.

- [ ] **Step 2: Confirm rule exists exactly once**

Run:

```bash
node -e "const fs=require('fs'); const s=fs.readFileSync('wordineer-deploy/_redirects','utf8'); const n=(s.match(/random-american-name-generator/g)||[]).length; console.log(n); if(n!==2) process.exit(1);"
```

Expected:
- Prints `2`, because the slug appears in source and destination.

---

## Task 7: Build Template Output

**Files:**
- Generated: `wordineer-deploy/random-american-name-generator.html`
- Generated or modified by build as applicable from `template-deploy`

- [ ] **Step 1: Run template build**

Run:

```bash
cd template-deploy
python3 build.py
```

Expected:
- Build completes successfully.
- `wordineer-deploy/random-american-name-generator.html` exists.

- [ ] **Step 2: Confirm generated deploy page**

Run:

```bash
node -e "const fs=require('fs'); const p='wordineer-deploy/random-american-name-generator.html'; const s=fs.readFileSync(p,'utf8'); const required=['Random American Name Generator','ang-count','ang-gender','ang-type','ang-era','ang-style','ang-last-style','ang-letter','/data/american-names.json']; const missing=required.filter(x=>!s.includes(x)); if(missing.length){ console.error('Missing: '+missing.join(', ')); process.exit(1); } console.log('ok');"
```

Expected:
- Prints `ok`.

---

## Task 8: Verify Locally

**Files:**
- Test: local static site served from `wordineer-deploy`

- [ ] **Step 1: Validate JSON files**

Run:

```bash
python3 -m json.tool wordineer-deploy/data/american-names.json >/dev/null
python3 -m json.tool template-deploy/tools.json >/dev/null
```

Expected:
- Both commands exit successfully.

- [ ] **Step 2: Start local server**

Run:

```bash
cd wordineer-deploy
python3 -m http.server 8080
```

Expected:
- Server starts at `http://localhost:8080`.

- [ ] **Step 3: Manual browser checks**

Open:

```text
http://localhost:8080/random-american-name-generator/
```

Verify:
- Page loads.
- No browser console errors.
- JSON request to `/data/american-names.json` returns 200.
- Initial names generate on page load.
- Generate button creates new results.
- Reset restores defaults.
- Count `0` clamps or errors correctly.
- Count `51` clamps or errors correctly.
- Gender `Female` returns only female/valid compatible first names.
- Gender `Male` returns only male/valid compatible first names.
- Gender `Neutral` returns neutral first names.
- Name type `First name` shows first names only.
- Name type `Last name` shows surnames only.
- Name type `Full name` shows first + last.
- Name type `First + middle + last` shows three-part names.
- Era filter changes first-name pool.
- Style filter changes first-name pool.
- Last name background changes surname pool.
- Starts-with filter affects first names.
- Copy one works.
- Save one works.
- Copy all works.
- Copy saved works.
- Mobile "More options" toggle opens/closes advanced controls.
- Result cards do not overflow on mobile.

- [ ] **Step 4: Inspect generated links**

Run:

```bash
node -e "const fs=require('fs'); const pages=['wordineer-deploy/random-american-name-generator.html','wordineer-deploy/random-name-generator.html','wordineer-deploy/random-filipino-name-generator.html']; for(const p of pages){ const s=fs.readFileSync(p,'utf8'); console.log(p, s.includes('/random-american-name-generator/') ? 'has american link' : 'missing american link'); }"
```

Expected:
- American page exists.
- Random name generator page has American link.
- Filipino page has American link.

---

## Task 9: Final Review

**Files:**
- Review all changed files.

- [ ] **Step 1: Check git diff summary**

Run:

```bash
git diff --stat
```

Expected changed files:
- `docs/superpowers/specs/2026-05-05-random-american-name-generator-design.md`
- `docs/superpowers/plans/2026-05-05-random-american-name-generator.md`
- `wordineer-deploy/data/american-names.json`
- `template-deploy/tools-src/random-american-name-generator.html`
- `template-deploy/tools.json`
- `template-deploy/tools-src/random-name-generator.html`
- `template-deploy/tools-src/random-filipino-name-generator.html`
- `wordineer-deploy/_redirects`
- `wordineer-deploy/random-american-name-generator.html`

- [ ] **Step 2: Review generated page for accidental fake identity language**

Run:

```bash
node -e "const fs=require('fs'); const s=fs.readFileSync('wordineer-deploy/random-american-name-generator.html','utf8').toLowerCase(); const banned=['ssn','social security','credit card','password','phone number','fake identity']; const hits=banned.filter(x=>s.includes(x)); console.log(hits); if(hits.some(x=>x!=='fake identity')) process.exit(1);"
```

Expected:
- No hits except possibly `fake identity` in FAQ text explaining what the tool does not do.

- [ ] **Step 3: Self-review against design spec**

Confirm every spec requirement is covered:
- Dedicated JSON file.
- Count 1-50.
- Gender filter with `Any`, `Female`, `Male`, `Neutral`.
- Name type filter with all four output types.
- Era filter.
- Style filter.
- Last name background filter.
- Starts-with filter.
- Result notes and chips.
- Copy/save actions.
- Mobile more-options toggle.
- SEO sections.
- FAQ.
- Internal links.
- Redirect.
- Local verification.

---

## Summary of Commits

Use short imperative commit messages if committing:

```bash
git add docs/superpowers/specs/2026-05-05-random-american-name-generator-design.md docs/superpowers/plans/2026-05-05-random-american-name-generator.md
git commit -m "Plan random American name generator"

git add wordineer-deploy/data/american-names.json template-deploy/tools-src/random-american-name-generator.html template-deploy/tools.json template-deploy/tools-src/random-name-generator.html template-deploy/tools-src/random-filipino-name-generator.html wordineer-deploy/_redirects wordineer-deploy/random-american-name-generator.html
git commit -m "Add random American name generator"
```

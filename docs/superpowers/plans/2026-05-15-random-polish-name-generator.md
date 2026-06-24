# Random Polish Name Generator Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a fully functional Polish name generator tool matching the design spec, integrated into the Wordineer site with data, UI, filters, and SEO.

**Architecture:** Three main components:
1. **Data layer** (`polish-names.json`): 600 given names + 400 surnames with meanings and pronunciation
2. **Template layer** (`random-polish-name-generator.html`): HTML template with CONFIG, SLOT structure, reusing existing tool-engine.js
3. **Navigation layer** (`tools.json` + `_redirects`): Wire up the tool into menus and clean URLs

**Tech Stack:** Static HTML/CSS/JS (no framework), tool-engine.js IIFE, Cloudflare Pages, Python build script.

---

## File Structure

**Create:**
- `wordineer-deploy/data/polish-names.json` — 1000+ Polish names dataset
- `template-deploy/tools-src/random-polish-name-generator.html` — Template file with CONFIG/SLOT structure

**Modify:**
- `template-deploy/tools.json` — Add Polish generator to mega menu, name_generator_tools grid, footer
- `wordineer-deploy/_redirects` — Add clean URL rewrite for `/random-polish-name-generator/`
- `template-deploy/output/` — Rebuilt by build.py (intermediate, not committed)

**No changes needed:**
- `tool-engine.js` — Reuse existing tool engine (already supports multi-era, gender, first-letter filters)
- `global.css` — Reuse existing styles

---

## Tasks

### Task 1: Create Polish Names Data File

**Files:**
- Create: `wordineer-deploy/data/polish-names.json`

- [ ] **Step 1: Research and gather 600 Polish given names (300M/300F)**

Gather names from reliable sources (Polish census data, literature, baby name databases). Ensure even split:
- 300 male names with eras (traditional, modern, or both)
- 300 female names with eras (traditional, modern, or both)
- Each name includes meaning (60 chars max) and pronunciation (phonetic English)

Example sources to check: Polish naming traditions, family trees, historical records.

Names should span both eras:
- **Traditional (18th–20th century):** Henryk, Stanisław, Zofia, Ewa, Krystyna, Bogdan, Jerzy, Janusz
- **Modern (1970s–present):** Jakub, Marta, Filip, Emma, Agnieszka, Paweł, Katarzyna, Michał

- [ ] **Step 2: Research and gather 400 Polish surnames**

Gather surnames from reliable sources (census data, name databases). Ensure variety:
- Include common endings: -ski, -ak, -czyk, -wicz, -owski, -ak, -uk
- Each surname includes meaning (60 chars max) and pronunciation

Example surnames: Kowalski (smith), Nowak (new), Lewandowski (left-side), Szymczyk, Gąsiorowski, Pietrzak, Müller, Krakowski (from Kraków).

- [ ] **Step 3: Format data into JSON structure**

Create `wordineer-deploy/data/polish-names.json` with the structure below:

```json
{
  "given": [
    {
      "name": "Jakub",
      "gender": "m",
      "era": ["modern"],
      "meaning": "supplanter; one who holds the heel",
      "pronunciation": "YAH-koop"
    },
    {
      "name": "Henryk",
      "gender": "m",
      "era": ["traditional"],
      "meaning": "estate ruler; home leader",
      "pronunciation": "HEN-rik"
    },
    {
      "name": "Zofia",
      "gender": "f",
      "era": ["traditional", "modern"],
      "meaning": "wisdom",
      "pronunciation": "ZOH-fee-ah"
    },
    {
      "name": "Marta",
      "gender": "f",
      "era": ["modern"],
      "meaning": "of Mars; the star",
      "pronunciation": "MAHR-tah"
    }
  ],
  "surnames": [
    {
      "name": "Kowalski",
      "meaning": "smith; one who works with metal",
      "pronunciation": "koh-VAL-skee"
    },
    {
      "name": "Nowak",
      "meaning": "new; recent arrival",
      "pronunciation": "NOH-vahk"
    }
  ]
}
```

Ensure:
- At least 300 male given names with valid eras
- At least 300 female given names with valid eras
- At least 400 surnames
- All pronunciations use hyphens for syllables (e.g., "YAH-koop", "koh-VAL-skee")
- Meanings are concise (under 60 chars)

- [ ] **Step 4: Validate JSON syntax**

Run: `python3 -m json.tool wordineer-deploy/data/polish-names.json > /dev/null && echo "Valid JSON"`

Expected: "Valid JSON"

- [ ] **Step 5: Spot-check data quality**

Manually verify:
- Sample 10 male names have valid eras
- Sample 10 female names have valid eras
- Sample 10 surnames have meanings and pronunciations
- No duplicate names
- All pronunciation strings are phonetic (no IPA symbols)

- [ ] **Step 6: Commit**

```bash
git add wordineer-deploy/data/polish-names.json
git commit -m "data: add 1000+ Polish names with meanings and pronunciation"
```

---

### Task 2: Create Polish Name Generator HTML Template

**Files:**
- Create: `template-deploy/tools-src/random-polish-name-generator.html`
- Reference: `template-deploy/tools-src/random-danish-name-generator.html` (pattern)

- [ ] **Step 1: Copy and adapt the Danish generator template**

Start with `template-deploy/tools-src/random-danish-name-generator.html` as a base. Replace:
- CONFIG: Update URL, output filename, and metadata
- SLOT:meta: Update title, description, canonical URL, og:* tags
- SLOT:hero: Update h1 text and subheading
- SLOT:tool: Adapt the tool UI (filters will be similar)
- SLOT:explainer: Write Polish-specific "How it works" text
- SLOT:faq: Write Polish-specific FAQ questions and answers
- SLOT:who: Update "Who uses this" section (writers, game makers, baby name seekers)

Use exact file path: `template-deploy/tools-src/random-polish-name-generator.html`

- [ ] **Step 2: Write CONFIG block**

```html
<!-- CONFIG
{
  "url": "/random-polish-name-generator/",
  "output": "random-polish-name-generator.html",
  "type": "tool",
  "more_tools_key": "name_generator_tools",
  "more_tools_subtitle": "Every name generator you need, all free"
}
-->
```

- [ ] **Step 3: Write SLOT:meta (SEO)**

```html
<!-- SLOT:meta -->
<title>1000+ Random Polish Names Generator | Wordineer</title>
<meta name="description" content="Generate authentic Polish names — Traditional classics (Henryk, Zofia) or Modern favorites (Jakub, Marta). Filter by gender, era, and first letter. Includes meanings and pronunciation. Free, no sign-up.">
<link rel="canonical" href="https://wordineer.com/random-polish-name-generator/">
<meta property="og:type"        content="website">
<meta property="og:site_name"   content="Wordineer">
<meta property="og:title"       content="1000+ Random Polish Names Generator | Wordineer">
<meta property="og:description" content="Generate authentic Polish names — Traditional classics (Henryk, Zofia) or Modern favorites (Jakub, Marta). Filter by gender, era, and first letter.">
<meta property="og:url"         content="https://wordineer.com/random-polish-name-generator/">
<meta property="og:image"       content="https://wordineer.com/og-image.png">
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "What is a random Polish name generator?",
      "acceptedAnswer": { "@type": "Answer", "text": "A tool that generates real Polish given names, surnames, or full names from a curated dataset of 1000+ authentic names. Each name includes its meaning and English-friendly pronunciation guide." }
    },
    {
      "@type": "Question",
      "name": "What's the difference between Traditional and Modern Polish names?",
      "acceptedAnswer": { "@type": "Answer", "text": "Traditional names (Henryk, Stanisław, Zofia) were most popular in the 18th–20th centuries and carry a sense of Polish history and literary tradition. Modern names (Jakub, Marta, Filip) have risen in popularity since the 1970s and reflect contemporary Polish usage. Choose Traditional for historical fiction; Modern for contemporary stories." }
    },
    {
      "@type": "Question",
      "name": "Why do Polish surnames end in -ski?",
      "acceptedAnswer": { "@type": "Answer", "text": "The -ski suffix is one of the most common Polish surname endings and originally meant 'of/from' — for example, Kowalski meant 'of the smith' (kowal = smith). Other common endings are -ak, -czyk, and -wicz. These endings reflect the name's origin: occupation, place, or patronymic tradition." }
    },
    {
      "@type": "Question",
      "name": "Can I use these names in my book?",
      "acceptedAnswer": { "@type": "Answer", "text": "Yes. All names here are real names from Polish traditions and culture. Names themselves are not copyrightable, so you can use them freely in fiction, screenplays, games, and other creative projects." }
    }
  ]
}
</script>
<!-- /SLOT:meta -->
```

- [ ] **Step 4: Write SLOT:style (CSS)**

Reuse the style block from Danish generator:

```html
<!-- SLOT:style -->
<style>
.tool-wrap  { max-width:960px; margin:0 auto; padding:24px 24px 0; }
.tool-card  { border:1px solid var(--border); border-radius:var(--radius-lg); overflow:hidden; background:var(--bg); box-shadow:var(--shadow); }
.tool-split { display:flex; }

.ctrl       { width:220px; flex-shrink:0; border-right:1px solid var(--border-2); padding:18px; overflow-y:auto; }
.ctrl-row   { margin-bottom:18px; }
.ctrl-label { display:block; font-size:12px; font-weight:600; color:var(--text-2); text-transform:uppercase; letter-spacing:.05em; margin-bottom:8px; }
.ctrl-label + input,
.ctrl-label + select { width:100%; padding:8px 10px; border:1px solid var(--border); border-radius:6px; font-family:inherit; font-size:13px; color:var(--text-1); background:var(--bg-2); }
.ctrl-label + input:focus,
.ctrl-label + select:focus { outline:none; border-color:var(--brand); }

.toggle     { position:relative; width:32px; height:18px; flex-shrink:0; }
.toggle input { opacity:0; width:0; height:0; }
.toggle-sl  { position:absolute; cursor:pointer; inset:0; background:var(--border); border-radius:9px; transition:.2s; }
.toggle input:checked + .toggle-sl { background:var(--brand); }
.toggle-sl::before { content:''; position:absolute; width:14px; height:14px; left:2px; top:2px; background:white; border-radius:50%; transition:.2s; }
.toggle input:checked + .toggle-sl::before { transform:translateX(14px); }

.gen-btn    { width:100%; padding:10px 14px; background:var(--brand); color:white; border:none; border-radius:8px; font-size:14px; font-weight:600; font-family:inherit; cursor:pointer; transition:background .15s,transform .1s; letter-spacing:-.01em; }
.gen-btn:hover { background:var(--brand-dark); }
.gen-btn:active { transform:scale(.98); }

.reset-btn  { display:block; width:100%; text-align:center; font-size:11px; color:var(--text-3); margin-top:8px; cursor:pointer; text-decoration:underline; text-underline-offset:2px; border:none; background:none; font-family:inherit; }

.ng-mobile-toggle { display:none; width:100%; margin:-2px 0 14px; padding:9px 12px; border:1px solid var(--border); border-radius:8px; background:var(--bg); color:var(--brand); font-size:13px; font-weight:600; font-family:inherit; cursor:pointer; }

.ng-advanced { display:block; }

.result-area { flex:1; min-width:0; padding:18px; overflow-y:auto; }
.result-count { font-size:13px; color:var(--text-3); margin-bottom:12px; }
.result-list { list-style:none; padding:0; margin:0; }
.result-item { padding:14px 0; border-bottom:1px solid var(--border-2); animation:fadeIn .2s ease; }
@keyframes fadeIn { from{opacity:0;transform:translateY(4px)} to{opacity:1;transform:none} }
.result-item:last-child { border-bottom:none; }
.name-text  { font-size:18px; font-weight:600; color:var(--text-1); margin-bottom:6px; }
.name-meta  { font-size:13px; color:var(--text-3); line-height:1.5; }
.name-meta.hidden { display:none; }

@media (max-width: 760px) {
  .hero--tool .hero-copy p { display:none; }
  .tool-wrap { padding:16px 14px 0; }
  .tool-split { display:block; }
  .ctrl { width:100%; border-right:none; border-bottom:1px solid var(--border-2); padding:14px; }
  .ng-mobile-toggle { display:block; }
  .ng-advanced { display:none; }
  .ng-advanced.is-open { display:block; }
  .reset-btn { display:none; }
  .result-area { padding:14px; }
  .result-item { padding:12px 0; }
  .name-text { font-size:16px; }
}
</style>
<!-- /SLOT:style -->
```

- [ ] **Step 5: Write SLOT:hero (Above-the-fold content)**

```html
<!-- SLOT:hero -->
<section class="hero hero--tool">
  <div class="hero-inner">
    <div class="hero-copy">
      <span class="hero-badge">Free &middot; No sign-up &middot; Instant</span>
      <h1>Random Polish Name Generator</h1>
      <p>Generate authentic Polish names — Traditional classics (Henryk, Zofia) or Modern favorites (Jakub, Marta). Filter by gender, era, and first letter. Includes meanings and pronunciation.</p>
    </div>
  </div>
</section>
<!-- /SLOT:hero -->
```

- [ ] **Step 6: Write SLOT:tool (Interactive UI)**

```html
<!-- SLOT:tool -->
<main class="tool-wrap">
  <section class="tool-card" aria-label="Random Polish name generator">
    <div class="tool-split">
      <div class="ctrl">
        <div class="ctrl-row">
          <label class="ctrl-label" for="png-type">Name type</label>
          <select id="png-type">
            <option value="given">First name</option>
            <option value="full">Full name</option>
            <option value="surname">Surname</option>
          </select>
        </div>

        <div class="ctrl-row">
          <label class="ctrl-label" for="png-gender">Gender</label>
          <select id="png-gender">
            <option value="any">Any</option>
            <option value="m">Male</option>
            <option value="f">Female</option>
          </select>
        </div>

        <div class="ctrl-row">
          <label class="ctrl-label" for="png-era">Era</label>
          <select id="png-era">
            <option value="all">All eras</option>
            <option value="traditional">Traditional</option>
            <option value="modern">Modern</option>
          </select>
        </div>

        <div class="ctrl-row">
          <label class="ctrl-label" for="png-letter">First letter</label>
          <select id="png-letter">
            <option value="">All letters</option>
            <option value="A">A</option>
            <option value="B">B</option>
            <option value="C">C</option>
            <!-- ... continue through Z ... -->
            <option value="Z">Z</option>
          </select>
        </div>

        <div class="ctrl-row">
          <label class="ctrl-label" for="png-count">Number of names</label>
          <input type="number" id="png-count" value="10" min="1" max="50" inputmode="numeric">
        </div>

        <div class="ctrl-row" style="display:flex; align-items:center; gap:10px;">
          <label class="ctrl-label" for="png-toggle" style="margin-bottom:0;">Show meanings</label>
          <label class="toggle">
            <input type="checkbox" id="png-toggle" checked>
            <span class="toggle-sl"></span>
          </label>
        </div>

        <button class="gen-btn" id="png-gen">Generate</button>
        <button class="reset-btn" id="png-reset">Reset filters</button>

        <button class="ng-mobile-toggle" id="png-toggle-adv">More options</button>
      </div>

      <div class="result-area">
        <div class="result-count" id="png-count-display">0 names</div>
        <ul class="result-list" id="png-results"></ul>
      </div>
    </div>
  </section>
</main>

<script type="application/json" id="png-data">
{
  "dataFile": "/data/polish-names.json",
  "dataKey": "PNG",
  "type": "given",
  "gender": "any",
  "era": "all",
  "letter": "",
  "count": 10,
  "showMeta": true
}
</script>

<script id="png-init">
(function() {
  const CONFIG = {
    typeSelect: "png-type",
    genderSelect: "png-gender",
    eraSelect: "png-era",
    letterSelect: "png-letter",
    countInput: "png-count",
    toggleInput: "png-toggle",
    genBtn: "png-gen",
    resetBtn: "png-reset",
    mobileToggleBtn: "png-toggle-adv",
    resultsList: "png-results",
    resultCount: "png-count-display",
    dataScript: "png-data",
    dataFile: "/data/polish-names.json",
    dataKey: "PNG"
  };

  let data = null;

  async function loadData() {
    if (!data) {
      const response = await fetch(CONFIG.dataFile);
      data = await response.json();
      window.TOOL_CACHE = window.TOOL_CACHE || {};
      window.TOOL_CACHE[CONFIG.dataKey] = data;
    }
    return data;
  }

  function filterNames() {
    const type = document.getElementById(CONFIG.typeSelect).value;
    const gender = document.getElementById(CONFIG.genderSelect).value;
    const era = document.getElementById(CONFIG.eraSelect).value;
    const letter = document.getElementById(CONFIG.letterSelect).value;
    const count = parseInt(document.getElementById(CONFIG.countInput).value, 10) || 10;
    const showMeta = document.getElementById(CONFIG.toggleInput).checked;

    if (!data) return [];

    let pool = [];

    if (type === "given" || type === "full") {
      const given = data.given.filter(n => {
        if (gender !== "any" && n.gender !== gender) return false;
        if (era !== "all" && !n.era.includes(era)) return false;
        if (letter && !n.name.toUpperCase().startsWith(letter)) return false;
        return true;
      });
      pool = given;
    } else if (type === "surname") {
      pool = data.surnames.filter(s => {
        if (letter && !s.name.toUpperCase().startsWith(letter)) return false;
        return true;
      });
    }

    // Shuffle and pick count
    const shuffled = pool.sort(() => Math.random() - 0.5);
    const results = shuffled.slice(0, Math.min(count, shuffled.length));

    // Build display
    const resultsList = document.getElementById(CONFIG.resultsList);
    resultsList.innerHTML = "";

    results.forEach(item => {
      const li = document.createElement("li");
      li.className = "result-item";

      let nameDisplay = item.name;
      let metaDisplay = "";

      if (type === "full") {
        const surname = data.surnames[Math.floor(Math.random() * data.surnames.length)];
        nameDisplay = `${item.name} ${surname.name}`;
        if (showMeta) {
          metaDisplay = `<div class="name-meta">${item.meaning} | ${item.pronunciation}<br>${surname.meaning} | ${surname.pronunciation}</div>`;
        }
      } else if (type === "given") {
        if (showMeta) {
          metaDisplay = `<div class="name-meta">${item.meaning}<br>${item.pronunciation}</div>`;
        }
      } else if (type === "surname") {
        if (showMeta) {
          metaDisplay = `<div class="name-meta">${item.meaning}<br>${item.pronunciation}</div>`;
        }
      }

      li.innerHTML = `<div class="name-text">${nameDisplay}</div>${metaDisplay}`;
      resultsList.appendChild(li);
    });

    // Update count
    document.getElementById(CONFIG.resultCount).textContent = `${results.length} name${results.length !== 1 ? "s" : ""}`;
  }

  function attachListeners() {
    const inputs = [
      CONFIG.typeSelect,
      CONFIG.genderSelect,
      CONFIG.eraSelect,
      CONFIG.letterSelect,
      CONFIG.countInput,
      CONFIG.toggleInput
    ];

    inputs.forEach(id => {
      const el = document.getElementById(id);
      if (el) {
        el.addEventListener("change", filterNames);
        el.addEventListener("input", filterNames);
      }
    });

    const genBtn = document.getElementById(CONFIG.genBtn);
    if (genBtn) {
      genBtn.addEventListener("click", filterNames);
    }

    const resetBtn = document.getElementById(CONFIG.resetBtn);
    if (resetBtn) {
      resetBtn.addEventListener("click", () => {
        document.getElementById(CONFIG.typeSelect).value = "given";
        document.getElementById(CONFIG.genderSelect).value = "any";
        document.getElementById(CONFIG.eraSelect).value = "all";
        document.getElementById(CONFIG.letterSelect).value = "";
        document.getElementById(CONFIG.countInput).value = "10";
        document.getElementById(CONFIG.toggleInput).checked = true;
        filterNames();
      });
    }

    const mobileToggle = document.getElementById(CONFIG.mobileToggleBtn);
    if (mobileToggle) {
      const ngAdvanced = document.querySelector(".ng-advanced");
      mobileToggle.addEventListener("click", () => {
        ngAdvanced.classList.toggle("is-open");
        mobileToggle.textContent = ngAdvanced.classList.contains("is-open") ? "Fewer options" : "More options";
      });
    }
  }

  window.addEventListener("load", async () => {
    await loadData();
    attachListeners();
    filterNames();
  });
})();
</script>
<!-- /SLOT:tool -->
```

- [ ] **Step 7: Write SLOT:explainer (How it works)**

```html
<!-- SLOT:explainer -->
<section class="content">
  <h2>How it works</h2>
  <p>This generator creates authentic Polish names for writers, game makers, character developers, and parents seeking baby names. It draws from 1000+ real Polish given names and surnames, each with meaning and pronunciation.</p>
  <p><strong>Choose your era:</strong> Traditional names (Henryk, Stanisław, Zofia) carry the weight of Polish history and literary tradition — best for historical fiction or characters with deep roots. Modern names (Jakub, Marta, Filip) reflect contemporary Polish usage since the 1970s.</p>
  <p><strong>Start with first names:</strong> Most users scan first-name ideas quickly before committing to a full character name. The default "First name" mode shows you clean, fast options. Switch to "Full name" for complete names with both given and surname.</p>
  <p><strong>Meanings and pronunciation:</strong> Each name includes its cultural meaning (from etymology, saints, places) and a phonetic pronunciation guide so you can use the name confidently even if you don't speak Polish.</p>
</section>

<section class="content">
  <h2>Who uses this?</h2>
  <p>Writers building Polish characters for novels, short stories, or screenplays. Game designers and worldbuilders creating characters and NPCs. Parents seeking authentic Polish baby names. Students researching Polish naming traditions and language.</p>
</section>
<!-- /SLOT:explainer -->
```

- [ ] **Step 8: Write SLOT:faq (FAQ section)**

```html
<!-- SLOT:faq -->
<section class="content">
  <h2>Frequently asked questions</h2>

  <details>
    <summary>What is a random Polish name generator?</summary>
    <p>A tool that generates real Polish given names, surnames, or full names from a curated dataset of 1000+ authentic names. Each name includes its meaning and English-friendly pronunciation guide, making it easy to use Polish names confidently in your writing or creative projects.</p>
  </details>

  <details>
    <summary>What's the difference between Traditional and Modern Polish names?</summary>
    <p>Traditional names (Henryk, Stanisław, Zofia) were most popular in the 18th–20th centuries and carry a sense of Polish history and literary tradition — perfect for historical fiction or characters with deep cultural roots. Modern names (Jakub, Marta, Filip) have risen in popularity since the 1970s and reflect contemporary Polish usage. Choose Traditional for period pieces; Modern for contemporary stories.</p>
  </details>

  <details>
    <summary>Why do Polish surnames end in -ski?</summary>
    <p>The -ski suffix is one of the most common Polish surname endings and originally meant "of/from" — for example, Kowalski meant "of the smith" (kowal = smith). Other common endings are -ak, -czyk, and -wicz. These endings reflect the name's origin: occupation, place of residence, or patronymic tradition. Understanding these patterns helps you recognize and create authentic-sounding Polish names.</p>
  </details>

  <details>
    <summary>Can I use these names in my book?</summary>
    <p>Yes. All names here are real names from Polish traditions and culture. Names themselves are not copyrightable, so you can use them freely in fiction, screenplays, games, and other creative projects. The meanings and pronunciations are cultural glosses meant to help you understand and use the names authentically.</p>
  </details>

</section>
<!-- /SLOT:faq -->
```

- [ ] **Step 9: Verify file structure**

Check that the template has all required SLOT blocks:
- `<!-- SLOT:meta -->` ✓
- `<!-- SLOT:style -->` ✓
- `<!-- SLOT:hero -->` ✓
- `<!-- SLOT:tool -->` ✓
- `<!-- SLOT:explainer -->` ✓
- `<!-- SLOT:faq -->` ✓

- [ ] **Step 10: Commit**

```bash
git add template-deploy/tools-src/random-polish-name-generator.html
git commit -m "feat: create Polish name generator template"
```

---

### Task 3: Update tools.json Navigation

**Files:**
- Modify: `template-deploy/tools.json`

- [ ] **Step 1: Open tools.json and locate sections**

Sections to update:
1. `mega` → "Name generators" category
2. `more_word_tools` (specifically the `name_generator_tools` grid)
3. `footer_cols` → appropriate footer column

- [ ] **Step 2: Add to `mega` → "Name generators"**

Find the section:
```json
{
  "cat": "Name generators",
  "tools": [
    ...
  ]
}
```

Add this entry (maintain alphabetical or consistent order):

```json
{
  "href": "/random-polish-name-generator/",
  "text": "Polish name generator"
}
```

Example position (alphabetically): after "Pet Name Generator", before "Random Name Generator".

- [ ] **Step 3: Add to `more_word_tools.name_generator_tools`**

Find the array under `"more_word_tools"`:
```json
"more_word_tools": {
  "name_generator_tools": [
    ...
  ]
}
```

Add this entry:

```json
{
  "href": "/random-polish-name-generator/",
  "text": "Polish name generator"
}
```

- [ ] **Step 4: Add to footer**

Find `footer_cols` and locate the "Name Generators" column:
```json
{
  "col": "Name Generators",
  "links": [
    ...
  ]
}
```

Add this entry:

```json
{
  "href": "/random-polish-name-generator/",
  "text": "Polish names"
}
```

- [ ] **Step 5: Validate JSON syntax**

Run: `python3 -m json.tool template-deploy/tools.json > /dev/null && echo "Valid JSON"`

Expected: "Valid JSON"

- [ ] **Step 6: Commit**

```bash
git add template-deploy/tools.json
git commit -m "feat: add Polish name generator to navigation"
```

---

### Task 4: Add Clean URL Redirect

**Files:**
- Modify: `wordineer-deploy/_redirects`

- [ ] **Step 1: Open _redirects file**

Check current format (Cloudflare Pages _redirects syntax).

- [ ] **Step 2: Add Polish generator redirect**

Add this line to the file (exact format from existing entries):

```
/random-polish-name-generator/  /random-polish-name-generator.html  200
```

Maintain consistent formatting with existing redirects.

- [ ] **Step 3: Verify no duplicate rules**

Check that there's no existing `/random-polish-name-generator/` rule that would conflict.

- [ ] **Step 4: Commit**

```bash
git add wordineer-deploy/_redirects
git commit -m "feat: add clean URL redirect for Polish name generator"
```

---

### Task 5: Build and Deploy

**Files:**
- Run: `cd template-deploy && python3 build.py`
- Copy: `template-deploy/output/random-polish-name-generator.html` → `wordineer-deploy/`

- [ ] **Step 1: Run build script**

```bash
cd /Users/garrickdeetan/Documents/Random\ Word\ Generator\ Tool\ Site/template-deploy
python3 build.py
```

Expected: Script completes without errors. New file created at `template-deploy/output/random-polish-name-generator.html`.

- [ ] **Step 2: Copy output file**

```bash
cp template-deploy/output/random-polish-name-generator.html wordineer-deploy/
```

Verify: `ls -lh wordineer-deploy/random-polish-name-generator.html` (file exists, size > 0)

- [ ] **Step 3: Start local server**

```bash
cd wordineer-deploy
python3 -m http.server 8080
```

Expected: "Serving HTTP on 0.0.0.0 port 8080..."

- [ ] **Step 4: Test in browser**

Open browser to: `http://localhost:8080/random-polish-name-generator/`

Verify:
- Page loads without 404
- Title shown in browser tab: "1000+ Random Polish Names Generator | Wordineer"
- Hero section displays with h1 "Random Polish Name Generator"
- Filter controls visible: Name type, Gender, Era, First letter, Count
- "Generate" button is clickable
- Toggle "Show meanings" works (checked by default)
- Generated names appear in results area
- Meanings and pronunciation display when toggle is ON
- Meanings and pronunciation hidden when toggle is OFF
- Changing filters auto-updates results

- [ ] **Step 5: Test mobile view**

In browser DevTools (F12), activate mobile view (iPhone 12 dimensions):

Verify:
- "More options" button visible at top
- Advanced filters hidden by default
- Tapping "More options" expands filters
- Layout is single-column, readable
- Text size and buttons are touch-friendly
- All filters still work in mobile view

- [ ] **Step 6: Verify pronunciation format**

In results, check that pronunciations display correctly:
- Example: "Jakub (YAH-koop)" or similar format
- No garbled text or encoding issues
- Hyphens appear between syllables

- [ ] **Step 7: Test clean URL redirect**

In browser, try the clean URL: `http://localhost:8080/random-polish-name-generator/`

Expected: Page loads successfully (redirect works, even though server is local).

- [ ] **Step 8: Stop local server**

In terminal: `Ctrl+C`

- [ ] **Step 9: Commit**

```bash
git add wordineer-deploy/random-polish-name-generator.html
git commit -m "build: generate Polish name generator HTML"
```

---

### Task 6: Verify Integration and Final Testing

**Files:**
- Verify: `template-deploy/tools.json` entries
- Verify: Navigation appears in generated pages
- Verify: No regressions in other tools

- [ ] **Step 1: Rebuild all pages**

```bash
cd template-deploy
python3 build.py
```

Expected: All pages rebuild successfully, no errors.

- [ ] **Step 2: Check that other generators still build**

Spot-check a few generated pages:

```bash
ls -lh template-deploy/output/ | grep -E "random-[a-z]+-generator"
```

Expected: Random Danish, Italian, Greek, name generator, etc. all present with recent timestamps.

- [ ] **Step 3: Start server and verify navigation**

```bash
cd wordineer-deploy
python3 -m http.server 8080
```

Open: `http://localhost:8080/random-name-generator/`

Verify:
- Polish generator appears in mega menu under "Name generators"
- Polish generator appears in "More tools" grid
- All other name generators still visible
- Clicking Polish generator link works

Navigate to `http://localhost:8080/`

Verify:
- Footer shows Polish generator link in "Name Generators" column
- All other footer links intact

- [ ] **Step 4: Test cross-tool compatibility**

Visit several other generators (Danish, Greek, Italian, Random Name):

Verify:
- No visual regressions
- Other tools' filters still work
- No console errors in DevTools
- Styles are consistent

- [ ] **Step 5: Lighthouse PageSpeed check (local)**

Run a local Lighthouse audit on Polish generator:

In browser DevTools (F12) → Lighthouse:
- Run audit for mobile
- Run audit for desktop

Expected:
- Performance: > 85
- Accessibility: > 90
- Best Practices: > 85
- SEO: > 90

If any scores are below threshold, check:
- Data file load time
- No blocking scripts
- Image optimization
- Mobile viewport config

- [ ] **Step 6: Stop server**

```bash
Ctrl+C
```

- [ ] **Step 7: Final commit summary**

Verify git log shows all commits:

```bash
git log --oneline -7
```

Expected output:
```
abc1234 build: generate Polish name generator HTML
def5678 feat: add clean URL redirect for Polish name generator
ghi9012 feat: add Polish name generator to navigation
jkl3456 feat: create Polish name generator template
mno7890 data: add 1000+ Polish names with meanings and pronunciation
```

- [ ] **Step 8: Commit (if any final tweaks made)**

```bash
git status
# If clean: all changes committed ✓
# If dirty: commit final changes
```

---

## Summary

After completing all tasks, you will have:

✓ **Data:** 1000+ authentic Polish names with meanings and pronunciation  
✓ **Template:** Full-featured HTML template with all required slots  
✓ **Navigation:** Polish generator integrated into menus and footer  
✓ **URL:** Clean URL redirect configured  
✓ **Build:** Pages generated and tested locally  
✓ **Verification:** All filters work, mobile responsive, no regressions  

The Polish name generator is ready for deployment to Cloudflare Pages.

---

## Verification Checklist (Manual QA)

Before claiming "done":

- [ ] Page loads instantly at `/random-polish-name-generator/`
- [ ] All filters (gender, era, type, letter, count) work and trigger auto-generation
- [ ] Toggle for meanings/pronunciation works on both ON and OFF states
- [ ] First name is the default in "Name type" filter
- [ ] Results display names with correct formatting (e.g., "Jakub (YAH-koop)")
- [ ] Mobile view: "More options" toggle collapses/expands correctly
- [ ] Mobile touch targets are all > 48px (accessible)
- [ ] Title and meta description display correctly
- [ ] FAQ section loads and expand/collapse works
- [ ] Polish generator appears in mega menu, tools grid, and footer
- [ ] Other generators (Danish, Italian, Greek, etc.) still work
- [ ] No console errors in browser DevTools
- [ ] Lighthouse scores remain strong (Performance > 85, SEO > 90)
- [ ] Clean URL redirect works (`/random-polish-name-generator/`)

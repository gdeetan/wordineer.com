# Sight Words Generator Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build `/sight-words-generator/` — an interactive Dolch + Fry sight words generator with audio, practice mode, and grade filtering, targeted at parents and K-3 teachers.

**Architecture:** Static HTML/JS page using the existing `type: tool` CONFIG+SLOT template. Word data lives in `wordineer-deploy/data/sight-words-data.json`. JavaScript IIFE in the `init` slot handles all interactivity: filtering, rendering, TTS audio, localStorage saves, and practice mode. Modeled directly on `sat-vocabulary-words.html`.

**Tech Stack:** Vanilla JS (ES5 IIFE pattern), HTML5, CSS, browser SpeechSynthesis API, localStorage. Python 3 for data generation script. Build system: `template-deploy/build.py`.

---

## File Map

| Action | File | Purpose |
|---|---|---|
| CREATE | `template-deploy/tools-src/sight-words-generator.html` | Page source (CONFIG + SLOTs) |
| CREATE | `wordineer-deploy/data/sight-words-data.json` | ~615-word dataset |
| CREATE | `template-deploy/generate_sight_words_data.py` | One-time data generation script |
| MODIFY | `template-deploy/tools.json` | Add tool to mega-menu + grids + footer |
| MODIFY | `wordineer-deploy/_redirects` | Clean URL redirect |
| GENERATED | `template-deploy/output/sight-words-generator.html` | Build output (auto-generated) |
| COPY-TO | `wordineer-deploy/sight-words-generator.html` | Deployed page |

---

## Task 1: Generate sight-words-data.json

**Files:**
- Create: `template-deploy/generate_sight_words_data.py`
- Create: `wordineer-deploy/data/sight-words-data.json`

- [ ] **Step 1: Create the data generation script**

Create `template-deploy/generate_sight_words_data.py`:

```python
#!/usr/bin/env python3
"""
Generate wordineer-deploy/data/sight-words-data.json
Combines Dolch (315 words) and Fry top 300 (3 groups of 100).
Words on both lists get list="both" with both group fields populated.
Run from repo root: python3 template-deploy/generate_sight_words_data.py
"""
import json, os

DOLCH = {
    "pre-k": [
        "a","and","away","big","blue","can","come","down","find","for",
        "funny","go","help","here","I","in","is","it","jump","little",
        "look","make","me","my","not","one","play","red","run","said",
        "see","the","three","to","two","up","we","where","yellow","you"
    ],
    "kindergarten": [
        "all","am","are","at","ate","be","black","brown","but","came",
        "did","do","eat","four","get","good","have","he","into","like",
        "must","new","no","now","on","our","out","please","pretty","ran",
        "ride","saw","say","she","so","soon","that","there","they","this",
        "too","under","want","was","well","went","what","white","who","will",
        "with","yes"
    ],
    "1st": [
        "after","again","an","any","as","ask","by","could","every","fly",
        "from","give","going","had","has","her","him","his","how","just",
        "know","let","live","may","of","old","once","open","over","put",
        "round","some","stop","take","thank","them","then","think","walk","were",
        "when"
    ],
    "2nd": [
        "always","around","because","been","before","best","both","buy","call","cold",
        "does","don't","fast","first","five","found","gave","goes","green","its",
        "made","many","off","or","pull","read","right","sing","sit","sleep",
        "tell","their","these","those","upon","us","use","very","wash","which",
        "why","wish","work","would","write","your"
    ],
    "3rd": [
        "about","better","bring","carry","clean","cut","done","draw","drink","eight",
        "fall","far","full","got","grow","hold","hot","hurt","if","keep",
        "kind","laugh","light","long","much","myself","never","only","own","pick",
        "seven","shall","show","six","small","start","ten","today","together","try",
        "warm"
    ],
    "nouns": [
        "apple","baby","back","ball","bear","bed","bell","bird","birthday","boat",
        "box","boy","bread","brother","cake","car","cat","chair","chicken","children",
        "Christmas","coat","corn","cow","day","dog","doll","door","duck","egg",
        "eye","farm","farmer","father","feet","fire","fish","floor","flower","fly",
        "foot","game","garden","girl","goodbye","grass","ground","hand","head","hill",
        "home","horse","house","kitty","leg","letter","man","men","milk","money",
        "morning","mother","name","nest","night","paper","party","picture","pig","rain",
        "ring","robin","school","seed","sheep","shoe","sister","snow","song","squirrel",
        "stick","street","sun","table","thing","time","top","toy","tree","watch",
        "water","wind","window","wood"
    ]
}

FRY = {
    "1-100": [
        "a","about","all","am","an","and","are","as","at","be",
        "been","but","by","called","can","come","could","day","did","do",
        "down","each","find","first","for","from","get","go","had","has",
        "have","he","her","him","his","how","I","if","in","into",
        "is","it","its","like","long","look","made","make","many","may",
        "more","my","no","not","now","number","of","on","one","or",
        "other","out","part","people","said","see","she","so","some","than",
        "that","the","their","them","then","there","these","they","this","time",
        "to","two","up","use","was","water","way","we","were","what",
        "when","which","who","will","with","words","would","write","you","your"
    ],
    "101-200": [
        "after","again","air","also","America","animal","another","answer","any","around",
        "ask","away","back","because","before","big","boy","came","change","different",
        "does","end","even","follow","form","found","give","good","great","hand",
        "help","here","home","house","just","kind","know","land","large","learn",
        "letter","line","little","live","man","me","means","men","most","mother",
        "move","much","must","name","need","new","off","old","only","our",
        "over","page","picture","place","play","point","put","read","right","same",
        "say","sentence","set","should","show","small","sound","spell","still","study",
        "such","take","tell","things","think","three","through","too","try","turn",
        "us","very","want","well","went","where","why","work","world","years"
    ],
    "201-300": [
        "below","between","book","both","car","carry","children","city","close","country",
        "don't","earth","enough","ever","every","example","eye","face","family","far",
        "feet","food","four","gave","going","group","grow","hard","head","high",
        "idea","important","Indian","keep","last","late","left","life","light","might",
        "mile","miss","mountain","near","never","next","night","often","once","open",
        "own","plant","real","river","run","saw","second","seem","side","something",
        "sometimes","song","soon","start","state","stop","story","talk","those","thought",
        "together","took","tree","under","until","upon","walk","watch","while","white",
        "without","young","above","across","along","began","being","beside","black","built",
        "during","early","five","girl","hands","hear","letter","list","map","road"
    ]
}

# Build word → dolch_group lookup
dolch_lookup = {}
for grp, words in DOLCH.items():
    for w in words:
        dolch_lookup[w.lower()] = grp

# Build word → fry_group + fry_rank lookup
fry_lookup = {}
fry_rank_counter = 0
for grp, words in FRY.items():
    for i, w in enumerate(words):
        key = w.lower()
        if grp == "1-100":
            rank = i + 1
        elif grp == "101-200":
            rank = i + 101
        else:
            rank = i + 201
        fry_lookup[key] = {"fry_group": grp, "fry_rank": rank}

# Merge
seen = {}
entries = []

def add(word, dolch_group, fry_group, fry_rank):
    key = word.lower()
    if key in seen:
        e = seen[key]
        if dolch_group and not e.get("dolch_group"):
            e["dolch_group"] = dolch_group
            e["list"] = "both"
        if fry_group and not e.get("fry_group"):
            e["fry_group"]  = fry_group
            e["fry_rank"]   = fry_rank
            e["list"] = "both"
        return
    e = {
        "word":        word,
        "list":        "both" if (dolch_group and fry_group) else ("dolch" if dolch_group else "fry"),
        "dolch_group": dolch_group,
        "fry_group":   fry_group,
        "fry_rank":    fry_rank
    }
    seen[key] = e
    entries.append(e)

# Add all Dolch words first
for grp, words in DOLCH.items():
    for w in words:
        key = w.lower()
        fd = fry_lookup.get(key, {})
        add(w, grp, fd.get("fry_group"), fd.get("fry_rank"))

# Add Fry words not yet in the list
for grp, words in FRY.items():
    for w in words:
        key = w.lower()
        fd = fry_lookup[key]
        if key not in seen:
            add(w, dolch_lookup.get(key), fd["fry_group"], fd["fry_rank"])
        else:
            # already added via Dolch — update fry fields if missing
            e = seen[key]
            if not e.get("fry_group"):
                e["fry_group"] = fd["fry_group"]
                e["fry_rank"]  = fd["fry_rank"]
                e["list"] = "both" if e.get("dolch_group") else "fry"

out_path = os.path.join(os.path.dirname(__file__), "../wordineer-deploy/data/sight-words-data.json")
with open(out_path, "w") as f:
    json.dump(entries, f, indent=2)

print(f"Generated {len(entries)} entries → {out_path}")
dolch_count = sum(1 for e in entries if e["list"] in ("dolch","both"))
fry_count   = sum(1 for e in entries if e["list"] in ("fry","both"))
both_count  = sum(1 for e in entries if e["list"] == "both")
print(f"  Dolch words (incl. both): {dolch_count}")
print(f"  Fry words (incl. both):   {fry_count}")
print(f"  On both lists:             {both_count}")
```

- [ ] **Step 2: Run the script**

```bash
cd "/Users/garrickdeetan/Documents/Random Word Generator Tool Site"
python3 template-deploy/generate_sight_words_data.py
```

Expected output (approximate):
```
Generated 580 entries → .../wordineer-deploy/data/sight-words-data.json
  Dolch words (incl. both): 315
  Fry words (incl. both):   300
  On both lists:             ~100
```

- [ ] **Step 3: Verify JSON is valid and spot-check key entries**

```bash
python3 -c "
import json
data = json.load(open('wordineer-deploy/data/sight-words-data.json'))
print('Total entries:', len(data))
# spot-check: 'the' should be list=both, dolch pre-k, fry rank 1
the = next(e for e in data if e['word']=='the')
print('the:', the)
# spot-check: 'called' should be fry-only, 1-100
called = next((e for e in data if e['word']=='called'), None)
print('called:', called)
"
```

Expected:
```
Total entries: 580   (approximately)
the: {'word': 'the', 'list': 'both', 'dolch_group': 'pre-k', 'fry_group': '1-100', 'fry_rank': ...}
called: {'word': 'called', 'list': 'fry', 'dolch_group': None, 'fry_group': '1-100', 'fry_rank': ...}
```

- [ ] **Step 4: Commit**

```bash
git add template-deploy/generate_sight_words_data.py wordineer-deploy/data/sight-words-data.json
git commit -m "feat: add sight-words-data.json (Dolch + Fry top 300)"
```

---

## Task 2: Create the page — meta + style + hero slots

**Files:**
- Create: `template-deploy/tools-src/sight-words-generator.html`

- [ ] **Step 1: Create the file with CONFIG, meta, style, and hero slots**

Create `template-deploy/tools-src/sight-words-generator.html`:

```html
<!-- CONFIG
{
  "type": "tool",
  "url": "/sight-words-generator.html",
  "output": "sight-words-generator.html"
}
-->

<!-- SLOT:meta -->
<title>Sight Words Generator — Dolch &amp; Fry Lists with Audio &amp; Practice Mode | Wordineer</title>
<meta name="description" content="Free sight words generator with Dolch and Fry lists. Filter by grade level, hear every word read aloud, and drill with Practice Mode. No login required.">
<meta property="og:title" content="Sight Words Generator — Dolch &amp; Fry Lists with Audio &amp; Practice Mode | Wordineer">
<meta property="og:description" content="Free sight words generator with Dolch and Fry lists. Filter by grade level, hear every word read aloud, and drill with Practice Mode. No login required.">
<meta property="og:url" content="https://wordineer.com/sight-words-generator/">
<meta property="og:type" content="website">
<link rel="canonical" href="https://wordineer.com/sight-words-generator/">
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "WebApplication",
  "name": "Sight Words Generator",
  "url": "https://wordineer.com/sight-words-generator/",
  "description": "Generate Dolch and Fry sight word lists with audio pronunciation and Practice Mode. Filter by grade level. Free, no login required.",
  "applicationCategory": "EducationApplication",
  "operatingSystem": "Any",
  "offers": { "@type": "Offer", "price": "0" }
}
</script>
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    { "@type": "ListItem", "position": 1, "name": "Wordineer", "item": "https://wordineer.com/" },
    { "@type": "ListItem", "position": 2, "name": "Word Tools", "item": "https://wordineer.com/word-tools/" },
    { "@type": "ListItem", "position": 3, "name": "Sight Words Generator", "item": "https://wordineer.com/sight-words-generator/" }
  ]
}
</script>
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "What is the difference between Dolch and Fry sight words?",
      "acceptedAnswer": { "@type": "Answer", "text": "The Dolch list (315 words) was developed in the 1930s–40s and is organized by grade level from Pre-K through 3rd grade. The Fry list (1,000 words) was developed in the 1950s and updated in 1980; it orders words purely by frequency. Dolch is the standard for K-3 classrooms; Fry is useful for tracking progress through Grade 9." }
    },
    {
      "@type": "Question",
      "name": "How many sight words should a kindergartner know?",
      "acceptedAnswer": { "@type": "Answer", "text": "By the end of kindergarten, most children should know all 40 Dolch Pre-K words and be working through the 52 Kindergarten words — roughly 60 to 70 Dolch words total. Development varies, so treat these as guidelines rather than hard benchmarks." }
    },
    {
      "@type": "Question",
      "name": "What order should I teach sight words?",
      "acceptedAnswer": { "@type": "Answer", "text": "Start with the Dolch Pre-K list (40 words) since these are the most frequent in early children's books. Once those are solid, move to the Kindergarten list, then 1st grade. For Fry, start with the first 100 words — they cover roughly 50% of everything written in English." }
    },
    {
      "@type": "Question",
      "name": "How long does it take to learn all the Dolch words?",
      "acceptedAnswer": { "@type": "Answer", "text": "With consistent daily practice of 5–10 minutes, most children can learn all 220 Dolch service words between ages 4 and 9 (Pre-K through 3rd grade). The key is frequency and repetition — short daily sessions beat occasional long study sessions." }
    },
    {
      "@type": "Question",
      "name": "Can I print the sight word list?",
      "acceptedAnswer": { "@type": "Answer", "text": "Yes. Click the Print button in the results bar and your browser's print dialog will open. The controls, navigation, and ads are hidden automatically so only the word list prints." }
    },
    {
      "@type": "Question",
      "name": "Is this sight words generator free?",
      "acceptedAnswer": { "@type": "Answer", "text": "Yes, completely free. No account, no signup, no download required. Generate as many lists as you want directly in your browser." }
    }
  ]
}
</script>
<!-- /SLOT:meta -->

<!-- SLOT:style -->
<style>
/* ── Tool layout (inherits from SAT vocab base) ── */
.tool-wrap  { padding:20px 24px 0; }
.tool-card  { background:var(--bg-2); border:1px solid var(--border); border-radius:14px; overflow:hidden; }
.tool-split { display:flex; min-height:480px; }

/* ── Controls ── */
.ctrl { width:220px; min-width:180px; padding:20px 18px; border-right:1px solid var(--border-2); display:flex; flex-direction:column; gap:14px; }
.ctrl-label { font-size:11px; font-weight:600; text-transform:uppercase; letter-spacing:.05em; color:var(--text-3); display:block; margin-bottom:4px; }
.ctrl-row   { display:flex; flex-direction:column; }
.ctrl select, .ctrl input[type="number"] {
  width:100%; padding:8px 10px; border:1px solid var(--border); border-radius:8px;
  background:var(--bg); color:var(--text); font-size:13px; font-family:inherit;
  appearance:none; -webkit-appearance:none;
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3E%3Cpath d='M4 6l4 4 4-4' stroke='%23888' stroke-width='1.5' fill='none' stroke-linecap='round'/%3E%3C/svg%3E");
  background-repeat:no-repeat; background-position:right 8px center; background-size:16px;
}
.ctrl input[type="number"] { background-image:none; }
.ctrl input[type="checkbox"] { width:auto; }
.toggle-row { display:flex; align-items:center; gap:8px; font-size:13px; color:var(--text-2); }
.gen-btn  { padding:10px 16px; background:var(--brand); color:#fff; border:none; border-radius:9px; font-size:14px; font-weight:600; font-family:inherit; cursor:pointer; transition:background .15s; }
.gen-btn:hover { background:var(--brand-dark); }
.reset-btn { padding:7px 12px; background:var(--bg-3,#f3f4f6); color:var(--text-2); border:1px solid var(--border); border-radius:8px; font-size:12px; font-family:inherit; cursor:pointer; }
.kbd  { font-size:11px; color:var(--text-3); margin-top:2px; }
.kbd kbd { background:var(--bg-3,#eee); border:1px solid var(--border); border-radius:4px; padding:1px 5px; font-family:inherit; }
.mobile-more-toggle { display:none; width:100%; padding:8px; font-size:12px; background:none; border:1px solid var(--border); border-radius:8px; cursor:pointer; color:var(--text-2); font-family:inherit; margin-bottom:4px; }

/* ── Results ── */
.results-col { flex:1; display:flex; flex-direction:column; }
.sw-top-bar  { display:flex; align-items:center; gap:8px; padding:12px 16px; border-bottom:1px solid var(--border-2); flex-wrap:wrap; }
.sw-count    { font-size:12px; color:var(--text-3); font-weight:600; margin-right:auto; }
.act-btn     { padding:6px 14px; background:var(--bg-3,#f3f4f6); border:1px solid var(--border); border-radius:8px; font-size:12px; font-family:inherit; cursor:pointer; color:var(--text-2); transition:background .15s; }
.act-btn:hover { background:var(--bg-2); }
.act-btn.primary { background:var(--brand); color:#fff; border-color:var(--brand); }
.act-btn.primary:hover { background:var(--brand-dark); }

.sw-list     { list-style:none; margin:0; padding:0; overflow-y:auto; flex:1; }
.sw-list .sw-empty { padding:40px 20px; color:var(--text-3); font-size:13px; text-align:center; }
.word-item   { display:flex; align-items:center; padding:11px 16px; border-bottom:1px solid var(--border-2); gap:10px; }
.word-item:last-child { border-bottom:none; }
.word-left   { display:flex; align-items:center; gap:10px; flex:1; min-width:0; }
.word-text   { font-size:1.15rem; font-weight:600; color:var(--text); }
.word-badge  { font-size:10px; font-weight:600; padding:2px 7px; border-radius:99px; white-space:nowrap; flex-shrink:0; }
.badge-dolch { background:#ede9fe; color:#5b21b6; }
.badge-fry   { background:#ccfbf1; color:#0f766e; }
.badge-both  { background:#fef3c7; color:#92400e; }
.word-right  { display:flex; gap:6px; align-items:center; flex-shrink:0; }
.icon-btn    { background:none; border:none; cursor:pointer; padding:5px; border-radius:7px; color:var(--text-3); font-size:16px; line-height:1; transition:background .12s,color .12s; }
.icon-btn:hover { background:var(--bg-3,#f3f4f6); color:var(--text); }
.icon-btn.saved { color:#e11d48; }

/* ── Saved words section ── */
.saved-section { border-top:1px solid var(--border); padding:14px 16px; }
.saved-section.hidden { display:none; }
.saved-title  { font-size:12px; font-weight:600; color:var(--text-3); text-transform:uppercase; letter-spacing:.05em; margin-bottom:10px; display:flex; align-items:center; gap:8px; }
.saved-chips  { display:flex; flex-wrap:wrap; gap:6px; margin-bottom:10px; }
.saved-chip   { background:var(--bg-3,#f3f4f6); border:1px solid var(--border); border-radius:99px; padding:3px 10px; font-size:12px; display:flex; align-items:center; gap:4px; }
.saved-chip button { background:none; border:none; cursor:pointer; color:var(--text-3); font-size:14px; line-height:1; padding:0; }
.saved-actions { display:flex; gap:6px; }

/* ── Practice Mode ── */
.practice-panel { display:none; flex-direction:column; height:100%; }
.practice-header { display:flex; align-items:center; justify-content:space-between; padding:12px 16px; border-bottom:1px solid var(--border-2); }
.practice-progress { font-size:12px; color:var(--text-3); font-weight:600; }
.practice-word-area { flex:1; display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center; gap:16px; padding:30px 20px; }
.practice-word-display { font-size:52px; font-weight:700; color:var(--text); letter-spacing:-.03em; line-height:1.1; }
.practice-badge { font-size:12px; padding:3px 10px; border-radius:99px; }
.practice-actions { display:flex; gap:8px; }
.practice-nav { display:flex; gap:10px; justify-content:center; padding:16px; border-top:1px solid var(--border-2); margin-top:auto; }

/* ── Explainer ── */
.explainer ul, .explainer ol { padding-left:1.5em; }

/* ── Responsive ── */
@media (max-width:640px) {
  .tool-wrap { padding:14px 16px 0; }
  .tool-split { flex-direction:column; }
  .ctrl { width:100%; border-right:none; border-bottom:1px solid var(--border-2); }
  .results-col { min-height:300px; }
  .mobile-more-toggle { display:block; }
  .advanced-options { display:none; }
  .advanced-options.is-open { display:block; }
  .gen-btn { margin-top:0; }
  .reset-btn, .kbd { display:none; }
  .practice-word-display { font-size:38px; }
}

@media print {
  header,nav,.breadcrumb,.hero,.ctrl,.sw-top-bar,.saved-section,.practice-panel,
  .explainer,.faq,.who,footer,.ad,[class*="ad-"],.more-tools,.content-wrap { display:none !important; }
  .word-item { border-top:none; border-bottom:1px solid #e5e7eb; padding:8px 0; break-inside:avoid; }
  .word-text { font-size:1.1rem; }
  .word-right { display:none !important; }
  @page { margin:1.5cm; }
}
</style>
<!-- /SLOT:style -->

<!-- SLOT:hero -->
<div class="breadcrumb">
  <div class="breadcrumb-inner">
    <a href="/">Wordineer</a>
    <span class="breadcrumb-sep">›</span>
    <a href="/word-tools/">Word Tools</a>
    <span class="breadcrumb-sep">›</span>
    <span aria-current="page">Sight Words Generator</span>
  </div>
</div>
<div class="hero">
  <div class="hero-badge">Dolch + Fry · Audio · Practice Mode · Free</div>
  <h1>Sight Words Generator</h1>
  <p>Generate sight word lists from the Dolch and Fry collections. Filter by grade level, hear every word read aloud, and drill with Practice Mode — no account, no download, no cost.</p>
</div>
<!-- /SLOT:hero -->
```

- [ ] **Step 2: Verify CONFIG is valid JSON**

```bash
python3 -c "
import re, json
src = open('template-deploy/tools-src/sight-words-generator.html').read()
m = re.search(r'<!-- CONFIG\s*(.*?)\s*-->', src, re.DOTALL)
print(json.loads(m.group(1)))
"
```

Expected: `{'type': 'tool', 'url': '/sight-words-generator.html', 'output': 'sight-words-generator.html'}`

---

## Task 3: Add tool slot (controls + results HTML)

**Files:**
- Modify: `template-deploy/tools-src/sight-words-generator.html` (append)

- [ ] **Step 1: Append the tool slot**

Append to `template-deploy/tools-src/sight-words-generator.html`:

```html
<!-- SLOT:tool -->
<div class="tool-wrap">
  <div class="tool-card">
    <div class="tool-split">

      <!-- Controls -->
      <div class="ctrl">
        <div class="ctrl-row">
          <label class="ctrl-label" for="ctrl-list">Word List</label>
          <select id="ctrl-list">
            <option value="all">All Lists</option>
            <option value="dolch">Dolch</option>
            <option value="fry">Fry</option>
          </select>
        </div>

        <div class="ctrl-row">
          <label class="ctrl-label" for="ctrl-group">Grade / Group</label>
          <select id="ctrl-group">
            <option value="all">All Grades &amp; Groups</option>
            <option value="pre-k">Dolch Pre-K</option>
            <option value="kindergarten">Dolch Kindergarten</option>
            <option value="1st">Dolch 1st Grade</option>
            <option value="2nd">Dolch 2nd Grade</option>
            <option value="3rd">Dolch 3rd Grade</option>
            <option value="nouns">Dolch Nouns</option>
            <option value="1-100">Fry Words 1–100</option>
            <option value="101-200">Fry Words 101–200</option>
            <option value="201-300">Fry Words 201–300</option>
          </select>
        </div>

        <button class="mobile-more-toggle" id="mobile-more-toggle" aria-expanded="false">More Options</button>

        <div class="advanced-options" id="advanced-options">
          <div class="ctrl-row">
            <label class="ctrl-label" for="ctrl-count">Number of words</label>
            <input type="number" id="ctrl-count" value="15" min="5" max="50">
          </div>

          <div class="ctrl-row">
            <div class="toggle-row">
              <input type="checkbox" id="ctrl-badge" checked>
              <label for="ctrl-badge">Show list label</label>
            </div>
          </div>
        </div>

        <button class="gen-btn" id="sw-gen-btn">Generate</button>
        <button class="reset-btn" id="sw-reset-btn">Reset</button>
        <div class="kbd">Press <kbd>Space</kbd> to regenerate</div>
      </div>

      <!-- Results -->
      <div class="results-col">
        <!-- Normal list view -->
        <div id="sw-list-view">
          <div class="sw-top-bar">
            <span class="sw-count" id="sw-count">15 words</span>
            <button class="act-btn primary" id="sw-practice-btn">Practice Mode</button>
            <button class="act-btn" id="sw-copy-all">Copy All</button>
            <button class="act-btn" id="sw-print-btn">Print</button>
          </div>
          <ul class="sw-list" id="sw-list" aria-live="polite"></ul>
        </div>

        <!-- Practice Mode -->
        <div class="practice-panel" id="sw-practice-panel" style="display:none;">
          <div class="practice-header">
            <button class="act-btn" id="sw-exit-practice">← Exit Practice</button>
            <span class="practice-progress" id="practice-progress">1 of 15</span>
          </div>
          <div class="practice-word-area">
            <div class="practice-word-display" id="practice-word-display"></div>
            <div class="practice-badge word-badge" id="practice-badge" style="display:none;"></div>
            <div class="practice-actions">
              <button class="act-btn" id="practice-hear">Hear Word</button>
            </div>
          </div>
          <div class="practice-nav">
            <button class="act-btn" id="practice-prev">← Prev</button>
            <button class="act-btn" id="practice-next">Next →</button>
          </div>
        </div>
      </div>

    </div>

    <!-- Saved words section -->
    <div class="saved-section hidden" id="saved-section">
      <div class="saved-title">
        Saved words <span id="saved-count">(0)</span>
      </div>
      <div class="saved-chips" id="saved-chips"></div>
      <div class="saved-actions">
        <button class="act-btn" id="sw-copy-saved">Copy Saved</button>
        <button class="act-btn" id="sw-clear-saved">Clear All</button>
      </div>
    </div>
  </div>
</div>
<!-- /SLOT:tool -->

<!-- SLOT:ad_b -->
<!-- /SLOT:ad_b -->
```

---

## Task 4: Add init slot (JavaScript)

**Files:**
- Modify: `template-deploy/tools-src/sight-words-generator.html` (append)

- [ ] **Step 1: Append the init slot**

Append to `template-deploy/tools-src/sight-words-generator.html`:

```html
<!-- SLOT:init -->
<script>
(function () {
  function he(s) { return String(s == null ? '' : s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;'); }

  var DOLCH_GROUPS = ['pre-k','kindergarten','1st','2nd','3rd','nouns'];
  var FRY_GROUPS   = ['1-100','101-200','201-300'];

  var GROUP_OPTS = {
    all: [
      {v:'all',   l:'All Grades &amp; Groups'},
      {v:'pre-k', l:'Dolch Pre-K'},
      {v:'kindergarten',l:'Dolch Kindergarten'},
      {v:'1st',   l:'Dolch 1st Grade'},
      {v:'2nd',   l:'Dolch 2nd Grade'},
      {v:'3rd',   l:'Dolch 3rd Grade'},
      {v:'nouns', l:'Dolch Nouns'},
      {v:'1-100', l:'Fry Words 1–100'},
      {v:'101-200',l:'Fry Words 101–200'},
      {v:'201-300',l:'Fry Words 201–300'}
    ],
    dolch: [
      {v:'all',   l:'All Grades'},
      {v:'pre-k', l:'Pre-K'},
      {v:'kindergarten',l:'Kindergarten'},
      {v:'1st',   l:'1st Grade'},
      {v:'2nd',   l:'2nd Grade'},
      {v:'3rd',   l:'3rd Grade'},
      {v:'nouns', l:'Nouns'}
    ],
    fry: [
      {v:'all',    l:'All Groups'},
      {v:'1-100',  l:'Words 1–100'},
      {v:'101-200',l:'Words 101–200'},
      {v:'201-300',l:'Words 201–300'}
    ]
  };

  var BADGE_LABEL = {
    'pre-k':       'Dolch Pre-K',
    'kindergarten':'Dolch Kindergarten',
    '1st':         'Dolch 1st Grade',
    '2nd':         'Dolch 2nd Grade',
    '3rd':         'Dolch 3rd Grade',
    'nouns':       'Dolch Nouns',
    '1-100':       'Fry 1–100',
    '101-200':     'Fry 101–200',
    '201-300':     'Fry 201–300'
  };

  var SW = {
    data:          null,
    saved:         JSON.parse(localStorage.getItem('sw-saved') || '[]'),
    practiceWords: [],
    practiceIdx:   0,

    load: function () {
      var self = this;
      if (self.data) return Promise.resolve(self.data);
      return fetch('/data/sight-words-data.json')
        .then(function (r) { return r.json(); })
        .then(function (d) { self.data = Array.isArray(d) ? d : (d.words || d.data || []); return self.data; });
    },

    rebuildGroupSelect: function () {
      var list = document.getElementById('ctrl-list').value;
      var opts = GROUP_OPTS[list] || GROUP_OPTS.all;
      var sel  = document.getElementById('ctrl-group');
      var prev = sel.value;
      sel.innerHTML = opts.map(function (o) {
        return '<option value="' + o.v + '">' + o.l + '</option>';
      }).join('');
      var still = opts.some(function (o) { return o.v === prev; });
      if (still) sel.value = prev; else sel.value = 'all';
    },

    badgeFor: function (word, listFilter) {
      var showBadge = document.getElementById('ctrl-badge').checked;
      if (!showBadge) return '';
      var label = '', cls = '';
      if (word.list === 'both') {
        // Show Dolch badge unless user is looking at Fry only
        if (listFilter === 'fry') {
          label = BADGE_LABEL[word.fry_group] || 'Fry';
          cls   = 'badge-fry';
        } else {
          label = BADGE_LABEL[word.dolch_group] || 'Dolch';
          cls   = 'badge-dolch';
        }
      } else if (word.list === 'dolch') {
        label = BADGE_LABEL[word.dolch_group] || 'Dolch';
        cls   = 'badge-dolch';
      } else {
        label = BADGE_LABEL[word.fry_group] || 'Fry';
        cls   = 'badge-fry';
      }
      return '<span class="word-badge ' + cls + '">' + he(label) + '</span>';
    },

    filter: function (words) {
      var list  = document.getElementById('ctrl-list').value;
      var group = document.getElementById('ctrl-group').value;
      var count = Math.min(50, Math.max(5, parseInt(document.getElementById('ctrl-count').value, 10) || 15));
      var result = words.slice();

      if (list === 'dolch') {
        result = result.filter(function (w) { return w.list === 'dolch' || w.list === 'both'; });
      } else if (list === 'fry') {
        result = result.filter(function (w) { return w.list === 'fry' || w.list === 'both'; });
      }

      if (group !== 'all') {
        var isDolch = DOLCH_GROUPS.indexOf(group) !== -1;
        var isFry   = FRY_GROUPS.indexOf(group)   !== -1;
        result = result.filter(function (w) {
          if (isDolch) return w.dolch_group === group;
          if (isFry)   return w.fry_group   === group;
          return true;
        });
      }

      // Fisher-Yates shuffle
      for (var i = result.length - 1; i > 0; i--) {
        var j = Math.floor(Math.random() * (i + 1));
        var tmp = result[i]; result[i] = result[j]; result[j] = tmp;
      }
      return result.slice(0, count);
    },

    generate: function () {
      var self = this;
      var list  = document.getElementById('sw-list');
      var listFilter = document.getElementById('ctrl-list').value;
      self.load()
        .then(function (words) {
          var filtered = self.filter(words);
          self.render(filtered, listFilter);
        })
        .catch(function () {
          list.innerHTML = '<li class="sw-empty">Could not load word list. Please refresh and try again.</li>';
        });
    },

    render: function (words, listFilter) {
      var list    = document.getElementById('sw-list');
      var countEl = document.getElementById('sw-count');
      var saved   = this.saved;

      if (!words.length) {
        list.innerHTML = '<li class="sw-empty">No words match your filters. Try a different grade or list.</li>';
        countEl.textContent = '0 words';
        return;
      }

      countEl.textContent = words.length + ' word' + (words.length !== 1 ? 's' : '');
      var self = this;
      list.innerHTML = words.map(function (w) {
        var isSaved  = saved.indexOf(w.word) !== -1;
        var badge    = self.badgeFor(w, listFilter);
        return [
          '<li class="word-item" data-word="' + he(w.word) + '">',
          '  <div class="word-left">',
          '    <span class="word-text">' + he(w.word) + '</span>',
          badge,
          '  </div>',
          '  <div class="word-right">',
          '    <button class="icon-btn speak-btn" aria-label="Hear ' + he(w.word) + '">',
          '      <svg viewBox="0 0 20 20" width="18" height="18" fill="none"><path d="M3 7.5h3l4-3v11l-4-3H3V7.5z" stroke="currentColor" stroke-width="1.4"/><path d="M14 6.5c1.5 1 2.5 2.2 2.5 3.5s-1 2.5-2.5 3.5" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/></svg>',
          '    </button>',
          '    <button class="icon-btn save-btn' + (isSaved ? ' saved' : '') + '" aria-label="Save ' + he(w.word) + '" data-word="' + he(w.word) + '">',
          '      <svg viewBox="0 0 20 20" width="18" height="18" fill="' + (isSaved ? '#e11d48' : 'none') + '"><path d="M10 16.5s-7-4.5-7-9a4 4 0 0 1 7-2.65A4 4 0 0 1 17 7.5c0 4.5-7 9-7 9z" stroke="' + (isSaved ? '#e11d48' : 'currentColor') + '" stroke-width="1.4"/></svg>',
          '    </button>',
          '  </div>',
          '</li>'
        ].join('\n');
      }).join('\n');

      // Bind speak/save buttons
      [].slice.call(list.querySelectorAll('.speak-btn')).forEach(function (btn) {
        btn.addEventListener('click', function () {
          self.speak(this.closest('.word-item').dataset.word);
        });
      });
      [].slice.call(list.querySelectorAll('.save-btn')).forEach(function (btn) {
        btn.addEventListener('click', function () {
          self.toggleSave(this.dataset.word, this);
        });
      });
    },

    speak: function (word) {
      if (!window.speechSynthesis) return;
      window.speechSynthesis.cancel();
      var u = new SpeechSynthesisUtterance(word);
      u.lang = 'en-US';
      u.rate = 0.85;
      window.speechSynthesis.speak(u);
    },

    toggleSave: function (word, btn) {
      var idx = this.saved.indexOf(word);
      if (idx !== -1) {
        this.saved.splice(idx, 1);
        if (btn) {
          btn.classList.remove('saved');
          btn.innerHTML = '<svg viewBox="0 0 20 20" width="18" height="18" fill="none"><path d="M10 16.5s-7-4.5-7-9a4 4 0 0 1 7-2.65A4 4 0 0 1 17 7.5c0 4.5-7 9-7 9z" stroke="currentColor" stroke-width="1.4"/></svg>';
        }
      } else {
        this.saved.push(word);
        if (btn) {
          btn.classList.add('saved');
          btn.innerHTML = '<svg viewBox="0 0 20 20" width="18" height="18" fill="#e11d48"><path d="M10 16.5s-7-4.5-7-9a4 4 0 0 1 7-2.65A4 4 0 0 1 17 7.5c0 4.5-7 9-7 9z" stroke="#e11d48" stroke-width="1.4"/></svg>';
        }
      }
      localStorage.setItem('sw-saved', JSON.stringify(this.saved));
      this.renderSaved();
    },

    renderSaved: function () {
      var section = document.getElementById('saved-section');
      var chips   = document.getElementById('saved-chips');
      var countEl = document.getElementById('saved-count');
      var self    = this;
      if (!this.saved.length) {
        section.classList.add('hidden');
        return;
      }
      section.classList.remove('hidden');
      countEl.textContent = '(' + this.saved.length + ')';
      chips.innerHTML = this.saved.map(function (w) {
        return '<span class="saved-chip">' + he(w) + '<button aria-label="Remove ' + he(w) + '" data-word="' + he(w) + '">×</button></span>';
      }).join('');
      [].slice.call(chips.querySelectorAll('button')).forEach(function (btn) {
        btn.addEventListener('click', function () { self.toggleSave(this.dataset.word, null); });
      });
    },

    copyAll: function () {
      var items = [].slice.call(document.querySelectorAll('.word-item'));
      var text  = items.map(function (li) { return li.dataset.word; }).join('\n');
      if (navigator.clipboard) { navigator.clipboard.writeText(text); }
      else { var ta = document.createElement('textarea'); ta.value = text; document.body.appendChild(ta); ta.select(); document.execCommand('copy'); document.body.removeChild(ta); }
    },

    copySaved: function () {
      var text = this.saved.join('\n');
      if (navigator.clipboard) { navigator.clipboard.writeText(text); }
      else { var ta = document.createElement('textarea'); ta.value = text; document.body.appendChild(ta); ta.select(); document.execCommand('copy'); document.body.removeChild(ta); }
    },

    enterPractice: function () {
      var items = [].slice.call(document.querySelectorAll('.word-item'));
      this.practiceWords = items.map(function (li) { return li.dataset.word; });
      if (!this.practiceWords.length) return;
      this.practiceIdx = 0;
      document.getElementById('sw-list-view').style.display    = 'none';
      document.getElementById('sw-practice-panel').style.display = 'flex';
      this.renderPractice();
    },

    exitPractice: function () {
      document.getElementById('sw-practice-panel').style.display = 'none';
      document.getElementById('sw-list-view').style.display      = '';
    },

    renderPractice: function () {
      var w = this.practiceWords[this.practiceIdx];
      document.getElementById('practice-word-display').textContent = w || '';
      document.getElementById('practice-progress').textContent =
        (this.practiceIdx + 1) + ' of ' + this.practiceWords.length;
    },

    reset: function () {
      document.getElementById('ctrl-list').value  = 'all';
      document.getElementById('ctrl-count').value = '15';
      document.getElementById('ctrl-badge').checked = true;
      this.rebuildGroupSelect();
      this.generate();
    },

    init: function () {
      var self = this;
      self.renderSaved();
      self.generate();

      document.getElementById('sw-gen-btn').addEventListener('click',      function () { self.generate(); });
      document.getElementById('sw-reset-btn').addEventListener('click',    function () { self.reset(); });
      document.getElementById('sw-copy-all').addEventListener('click',     function () { self.copyAll(); });
      document.getElementById('sw-print-btn').addEventListener('click',    function () { window.print(); });
      document.getElementById('sw-copy-saved').addEventListener('click',   function () { self.copySaved(); });
      document.getElementById('sw-clear-saved').addEventListener('click',  function () { self.saved = []; localStorage.removeItem('sw-saved'); self.renderSaved(); });
      document.getElementById('sw-practice-btn').addEventListener('click', function () { self.enterPractice(); });
      document.getElementById('sw-exit-practice').addEventListener('click',function () { self.exitPractice(); });
      document.getElementById('practice-hear').addEventListener('click',   function () { self.speak(self.practiceWords[self.practiceIdx]); });
      document.getElementById('practice-prev').addEventListener('click',   function () { if (self.practiceIdx > 0) { self.practiceIdx--; self.renderPractice(); } });
      document.getElementById('practice-next').addEventListener('click',   function () { if (self.practiceIdx < self.practiceWords.length - 1) { self.practiceIdx++; self.renderPractice(); } });

      // Rebuild group dropdown when list changes
      document.getElementById('ctrl-list').addEventListener('change', function () {
        self.rebuildGroupSelect();
        self.generate();
      });
      document.getElementById('ctrl-group').addEventListener('change', function () { self.generate(); });
      document.getElementById('ctrl-badge').addEventListener('change', function () { self.generate(); });

      // Space to regenerate
      document.addEventListener('keydown', function (e) {
        if (e.code !== 'Space') return;
        var tag = document.activeElement && document.activeElement.tagName;
        if (tag === 'INPUT' || tag === 'SELECT' || tag === 'BUTTON' || tag === 'TEXTAREA') return;
        e.preventDefault();
        self.generate();
      });

      // Mobile more-options toggle
      var moreToggle  = document.getElementById('mobile-more-toggle');
      var advancedOpts = document.getElementById('advanced-options');
      if (moreToggle && advancedOpts) {
        moreToggle.addEventListener('click', function () {
          var isOpen = advancedOpts.classList.toggle('is-open');
          moreToggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
          moreToggle.textContent = isOpen ? 'Hide Options' : 'More Options';
        });
      }

      /* ── FAQ accordion ── */
      document.querySelectorAll('.faq-item').forEach(function (item) {
        var q = item.querySelector('.faq-q');
        if (!q) return;
        q.addEventListener('click', function () { item.classList.toggle('open'); });
      });
    }
  };

  SW.init();
}());
</script>
<!-- /SLOT:init -->
```

---

## Task 5: Add explainer, FAQ, and who slots

**Files:**
- Modify: `template-deploy/tools-src/sight-words-generator.html` (append after ad_b slot)

- [ ] **Step 1: Append explainer, faq, and who slots**

Insert between `<!-- SLOT:ad_b --><!-- /SLOT:ad_b -->` and `<!-- SLOT:init -->` (or append before init slot):

```html
<!-- SLOT:explainer -->
<section class="explainer">

<h2>What are sight words?</h2>
<p>If you've ever watched a beginning reader sound out "the" letter by letter — "tuh... huh... eh... the!" — you already know why sight words matter. "The" doesn't follow standard phonics rules. Neither do "said," "of," "have," or "come." These words just have to be memorized.</p>
<p>Sight words are high-frequency words that appear constantly in written English but often can't be decoded by sounding out. They're sometimes called "heart words" (you learn them by heart) or "high-frequency words." Whatever you call them, the research is consistent: recognizing these words on sight — instantly, without sounding out — is one of the strongest predictors of reading fluency in young children.</p>
<p>Here's the math that makes them worth the effort. The 100 most common English words make up roughly 50% of everything written. The top 300 cover about 65%. When a child can read those words automatically, their brain can spend its limited working memory on comprehension — following the story, understanding the meaning, asking questions about the text — rather than decoding. That mental bandwidth is the difference between a child who reads and a child who actually enjoys reading.</p>
<p>Most reading curricula in the United States organize sight words into one of two main lists: the Dolch list, which covers Pre-K through 3rd grade, or the Fry list, which extends through Grade 9. Both are public domain, freely available, and widely taught. This generator gives you access to both in a single tool.</p>

<h2>Dolch vs. Fry — what's the difference?</h2>
<p>Dr. Edward William Dolch was a professor of education at the University of Illinois who spent years studying the books children were actually reading in the 1930s and '40s. He identified 220 words — "service words," he called them — that appeared over and over in children's literature, plus 95 common nouns. The result is a list of 315 words organized into six grade bands from Pre-K through 3rd grade. The Dolch list has been the standard for early childhood reading instruction ever since, and if your child's teacher sends home a weekly word list, there's a good chance it's drawn from Dolch.</p>
<p>Dr. Edward Fry took a different approach when he published his word list in the 1950s (and updated it in 1980). Instead of studying children's books specifically, he analyzed a much broader range of text, including materials used in Grades 3 through 9. His list runs to 1,000 words, ordered purely by frequency — the most common word in the English language first, the 1,000th-most-common word last. The Fry list is typically broken into groups of 100.</p>
<p>So which list should you use? For Pre-K through 2nd grade students just beginning to read, Dolch is typically the classroom standard — the grade bands map directly to where your child should be each year. The Fry list is a better framework for 3rd grade and beyond, or if you want a frequency-based approach that continues into middle school. The first 100 Fry words cover roughly 50% of all written text on their own, so mastering that group is an enormous milestone at any age.</p>
<p>Both lists are fully represented in this generator. If you're not sure which to use, start with Dolch — it's where most American teachers start, and the grade-level structure makes it easier to set goals and track progress.</p>

<h2>How to use this generator</h2>
<p>The tool takes about ten seconds to set up. Here's the flow:</p>
<ol>
  <li><strong>Choose a list.</strong> Select Dolch, Fry, or both. If your child's school uses a specific list, match it — consistency with the classroom matters for reinforcement.</li>
  <li><strong>Pick a grade or group.</strong> For Dolch, this maps directly to classroom grade levels (Pre-K through 3rd grade, plus Nouns). For Fry, select a frequency band (1–100, 101–200, 201–300).</li>
  <li><strong>Set a word count.</strong> For a five-minute session, 10–12 words is plenty. For a longer review, try 20–25. The default is 15.</li>
  <li><strong>Click Generate</strong> — or press <kbd>Space</kbd> at any time — to get a fresh random selection from your chosen grade and list.</li>
  <li><strong>Hear words aloud.</strong> Click the speaker icon on any word to hear it read at a clear, natural pace using your browser's built-in voice engine. No plugin required.</li>
  <li><strong>Save tricky words.</strong> Click the heart on any word your child struggles with. Saved words persist between sessions — close the browser and they'll still be there next time.</li>
  <li><strong>Run Practice Mode.</strong> Click Practice Mode to work through the current list one word at a time — just the word, centered on a clean screen, with no other distractions. Hit Hear Word to reinforce the pronunciation, and Prev/Next to move through the set.</li>
</ol>

<h2>Five ways to practice sight words at home</h2>
<p>The research on sight word instruction is pretty consistent: short, frequent sessions beat long occasional ones by a wide margin. Five to ten minutes a day, four or five days a week, will outperform an hour-long Saturday session every single time. Here are five techniques that actually work — one for each day of the week if you want to mix things up.</p>
<p><strong>Flash card drill.</strong> Classic for a reason. Generate a list, read through it together, and flip to Practice Mode for the ones your child hesitates on. Keep the stack small — ten to fifteen words — and retire a word once they can read it instantly three times in a row. The brain needs distributed repetition over days, not mass exposure in one sitting, to move a word into permanent memory.</p>
<p><strong>Find it in a book.</strong> During bedtime reading, pick two or three target words before you start: "tonight we're looking for 'said' and 'because'." Every time you hit one in the text, your child reads it aloud. By the end of the chapter they've encountered the word in real context a dozen times without any drilling. This technique is especially good because it shows children that sight words aren't arbitrary — they genuinely appear everywhere.</p>
<p><strong>Sentence building.</strong> Say a target word and ask your child to use it in a made-up sentence. This sounds simple, but it forces them to think about what the word means in context, not just what the letters look like. A child who can use "because" correctly in a sentence has a deeper relationship with that word than one who can simply read it off a flash card.</p>
<p><strong>Rainbow writing.</strong> Write the word in pencil on a piece of paper. Then trace over it five times in different colored markers — while saying the letters aloud each time. The combination of muscle memory, auditory repetition, and visual attention is surprisingly effective, especially for kinesthetic learners in kindergarten and first grade. It also buys you about four minutes of quiet.</p>
<p><strong>Practice Mode with the lights low.</strong> Not in any curriculum guide, but: put the laptop on the kitchen table, dim the room a bit, and run Practice Mode. The word on a clean screen becomes the whole focus for a minute and a half. This works especially well for kids who get distracted by the controls, the badge colors, and everything else competing for their attention in a fully lit room.</p>

<h2>When should my child know these words?</h2>
<p>These are guidelines, not hard benchmarks — reading development varies widely, and being a few months behind a typical milestone isn't cause for concern. That said, here's what most K-3 teachers aim for:</p>
<p><strong>Pre-K:</strong> Recognize 10–20 of the 40 Dolch Pre-K words by the end of the year. Words like "the," "I," "can," "go," and "a" are the most important. If your child can read those five without hesitating, you're off to a strong start.</p>
<p><strong>Kindergarten:</strong> All 40 Dolch Pre-K words solidly mastered, plus an introduction to the 52 Kindergarten words. A target of 60–70 total Dolch words by the end of kindergarten is realistic for most children.</p>
<p><strong>1st Grade:</strong> The full Pre-K and Kindergarten lists, plus the 41 First Grade words — roughly 133 Dolch words by year's end. Most 1st grade reading programs assign five to ten sight words per week drawn from this pool.</p>
<p><strong>2nd Grade:</strong> Through the Dolch Second Grade list — about 179 total words. By this point, words that were drilled in 1st grade should be genuinely automatic, not just recognizable with a second's thought.</p>
<p><strong>3rd Grade:</strong> The full 220 Dolch service words, with active work on the Nouns list. A 3rd grader who knows all 220 Dolch words can read about 75% of the words in a typical elementary school book without decoding. That's when reading stops feeling like work and starts feeling like reading.</p>

<h2>More tools for early readers on Wordineer</h2>
<p>Once your child has sight words down, the natural next challenge is spelling. The <a href="/spelling-bee-words-2nd-grade/">2nd Grade Spelling Bee Words</a> and <a href="/spelling-bee-words-3rd-grade/">3rd Grade Spelling Bee Words</a> tools use the same Practice Mode pattern as this generator and are a natural bridge from sight word recognition to competition-level spelling. For older students ready to work on academic vocabulary, the <a href="/sat-vocabulary-words/">SAT Vocabulary Words</a> tool covers 400+ college-level words with etymology, example sentences, and difficulty filtering. Browse the full <a href="/word-tools/">Word Tools hub</a> for the complete collection.</p>

</section>
<!-- /SLOT:explainer -->

<!-- SLOT:faq -->
<div class="faq">
  <h2 class="faq-title">Frequently asked questions</h2>

  <div class="faq-item open">
    <div class="faq-q"><span class="faq-q-text">What is the difference between Dolch and Fry sight words?</span><svg class="faq-chevron" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div>
    <div class="faq-a">The Dolch list (315 words) was developed in the 1930s–40s and is organized by grade level from Pre-K through 3rd grade — it's the standard in most American K-3 classrooms. The Fry list (1,000 words) was developed in the 1950s and updated in 1980; it orders words purely by frequency and extends through Grade 9. Both lists are public domain. For young readers (Pre-K through 2nd grade), Dolch is usually the right starting point because the grade bands map directly to classroom expectations.</div>
  </div>

  <div class="faq-item">
    <div class="faq-q"><span class="faq-q-text">How many sight words should a kindergartner know?</span><svg class="faq-chevron" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div>
    <div class="faq-a">By the end of kindergarten, most children should know all 40 Dolch Pre-K words and be working through the 52 Kindergarten-level words — roughly 60 to 70 Dolch words total. Development varies, so treat these as guidelines rather than hard benchmarks. If your child's teacher has specific expectations, those take precedence over any general milestone.</div>
  </div>

  <div class="faq-item">
    <div class="faq-q"><span class="faq-q-text">What order should I teach sight words?</span><svg class="faq-chevron" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div>
    <div class="faq-a">Start with the Dolch Pre-K list (40 words), since these are the most common in early children's books — "the," "and," "I," "a," "to," and so on. Once those are solid, move to the Kindergarten list, then 1st grade. For Fry, start with the first 100 words — they cover roughly 50% of everything written in English, so mastering them first gives the biggest return. Follow your child's classroom sequence when possible; consistency between home and school reinforces retention.</div>
  </div>

  <div class="faq-item">
    <div class="faq-q"><span class="faq-q-text">How long does it take to learn all the Dolch words?</span><svg class="faq-chevron" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div>
    <div class="faq-a">With consistent daily practice of 5–10 minutes, most children learn all 220 Dolch service words across Pre-K through 3rd grade — roughly ages 4 to 9. The key is frequency, not duration. Short daily sessions (even five minutes) dramatically outperform longer occasional ones, because memory consolidation happens between sessions, not during them.</div>
  </div>

  <div class="faq-item">
    <div class="faq-q"><span class="faq-q-text">Can I print the sight word list?</span><svg class="faq-chevron" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div>
    <div class="faq-a">Yes. Click the Print button in the results bar and your browser's print dialog will open. The controls, navigation, and other page elements are hidden automatically so only the word list prints — clean and ready to use as a take-home sheet or reference card.</div>
  </div>

  <div class="faq-item">
    <div class="faq-q"><span class="faq-q-text">Is this sight words generator free?</span><svg class="faq-chevron" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div>
    <div class="faq-a">Yes, completely free. No account, no signup, no download, no timer. Generate as many lists as you want, save words to your browser's local storage, and run Practice Mode as many times as you need — all at no cost.</div>
  </div>
</div>
<!-- /SLOT:faq -->

<!-- SLOT:who -->
<div class="who">
  <h2>Who uses this tool?</h2>
  <div class="uc-grid">
    <div class="uc"><div class="uc-title">Parents of Early Readers</div><div class="uc-body">Teaching a Pre-K through 2nd grader at home and want a quick way to generate fresh practice lists without printing PDFs. Use Practice Mode during evening sessions — ten minutes a night, five nights a week, is enough to move through an entire grade level in a month.</div></div>
    <div class="uc"><div class="uc-title">Kindergarten &amp; 1st Grade Teachers</div><div class="uc-body">Build grade-specific word lists in seconds for morning warm-ups, partner reading drills, or take-home sheets. Filter to your current unit's grade level and print the list directly from the browser — no worksheet software required.</div></div>
    <div class="uc"><div class="uc-title">Reading Tutors &amp; Interventionists</div><div class="uc-body">Quickly generate targeted lists for struggling readers at any grade level. The Dolch grade filters let you pinpoint exactly which word bank to work from, and Practice Mode gives you a clean one-word-at-a-time drill you can run live during a session without any setup.</div></div>
    <div class="uc"><div class="uc-title">Homeschool Educators</div><div class="uc-body">Build a structured sight word curriculum aligned to Dolch grade groupings without buying a packaged program. Work through the lists in order, save words that need more repetition, and use the Fry filter when your student is ready to go beyond the standard K-3 scope.</div></div>
  </div>
</div>
<!-- /SLOT:who -->
```

---

## Task 6: Update tools.json

**Files:**
- Modify: `template-deploy/tools.json`

- [ ] **Step 1: Open tools.json and locate the three insertion points**

The file has three sections that need updating:
1. `mega` array — the `"Writing & Vocabulary"` category tools list
2. `more_word_tools` array
3. `footer_cols` array — the `"Writing & Vocabulary"` column links

- [ ] **Step 2: Add sight words entry to mega Writing & Vocabulary tools**

In `template-deploy/tools.json`, find the `mega` array entry with `"cat": "Writing &amp; Vocabulary"`. Add to its `tools` array:

```json
{ "href": "/sight-words-generator/", "text": "Sight Words Generator" }
```

- [ ] **Step 3: Add sight words entry to more_word_tools**

Find the `more_word_tools` array and add:

```json
{ "href": "/sight-words-generator/", "text": "Sight Words Generator" }
```

- [ ] **Step 4: Add sight words entry to footer_cols Writing & Vocabulary**

Find the `footer_cols` entry with `"title": "Writing &amp; Vocabulary"` and add to its `links` array:

```json
{ "href": "/sight-words-generator/", "text": "Sight Words Generator" }
```

- [ ] **Step 5: Validate tools.json is still valid JSON**

```bash
python3 -c "import json; json.load(open('template-deploy/tools.json')); print('tools.json valid')"
```

Expected: `tools.json valid`

---

## Task 7: Update _redirects

**Files:**
- Modify: `wordineer-deploy/_redirects`

- [ ] **Step 1: Add clean URL redirect**

Open `wordineer-deploy/_redirects` and add:

```
/sight-words-generator   /sight-words-generator/   301
```

Place it with the other tool redirects (grouped alphabetically or near the bottom of the tool section).

---

## Task 8: Build, copy, and verify locally

**Files:**
- Generated: `template-deploy/output/sight-words-generator.html`
- Copy-to: `wordineer-deploy/sight-words-generator.html`

- [ ] **Step 1: Run the build**

```bash
cd "/Users/garrickdeetan/Documents/Random Word Generator Tool Site/template-deploy" && python3 build.py
```

Expected: build completes with no errors. Look for `sight-words-generator.html` in the output.

- [ ] **Step 2: Verify the output file exists and has expected slots**

```bash
python3 -c "
import re
src = open('output/sight-words-generator.html').read()
checks = ['Sight Words Generator', 'ctrl-list', 'ctrl-group', 'sw-gen-btn', 'sw-practice-panel', 'SW.init', 'sight-words-data.json', 'What are sight words', 'faq-item', 'uc-grid']
for c in checks:
    found = c in src
    print(('OK' if found else 'MISSING'), c)
"
```

Expected: all lines print `OK`.

- [ ] **Step 3: Copy to deploy folder**

```bash
cp "/Users/garrickdeetan/Documents/Random Word Generator Tool Site/template-deploy/output/sight-words-generator.html" "/Users/garrickdeetan/Documents/Random Word Generator Tool Site/wordineer-deploy/sight-words-generator.html"
```

- [ ] **Step 4: Start local server and verify in browser**

```bash
cd "/Users/garrickdeetan/Documents/Random Word Generator Tool Site/wordineer-deploy" && python3 -m http.server 8080
```

Open `http://localhost:8080/sight-words-generator.html` and verify:
- [ ] Page loads without console errors
- [ ] Generate button produces a word list
- [ ] List selector (Dolch/Fry/All) works — grade dropdown rebuilds correctly
- [ ] Grade filter narrows the word list
- [ ] Space bar regenerates
- [ ] Speaker icon plays audio
- [ ] Heart saves a word; saved section appears below the tool card
- [ ] Practice Mode shows words one at a time, Prev/Next work, Exit returns to list
- [ ] Print removes controls and leaves only word list
- [ ] FAQ accordions expand/collapse

- [ ] **Step 5: Commit all changes**

```bash
cd "/Users/garrickdeetan/Documents/Random Word Generator Tool Site"
git add \
  template-deploy/tools-src/sight-words-generator.html \
  template-deploy/tools.json \
  wordineer-deploy/data/sight-words-data.json \
  wordineer-deploy/sight-words-generator.html \
  wordineer-deploy/_redirects
git commit -m "feat: add Sight Words Generator (/sight-words-generator/) with Dolch + Fry, audio, practice mode"
```

---

## Self-Review Checklist

**Spec coverage:**
- [x] Data file (Dolch 315 + Fry 300, deduplicated, both-list tagging) → Task 1
- [x] Controls: list / grade / count / badge toggle → Task 3
- [x] Dynamic group dropdown rebuild on list change → Task 4 (`rebuildGroupSelect`)
- [x] Results: word text + badge + speaker + heart → Task 3 + 4
- [x] Saved words section with localStorage → Task 4 (`toggleSave`, `renderSaved`)
- [x] Practice Mode (no reveal step — recognition only) → Task 3 + 4
- [x] TTS audio at 0.85× rate → Task 4 (`speak`)
- [x] Copy all + print → Task 4
- [x] 1,500+ word explainer copy (5 H2 sections) → Task 5
- [x] FAQ (6 questions) with FAQPage schema → Task 2 + 5
- [x] Who-uses-it (4 cards) → Task 5
- [x] BreadcrumbList + WebApplication schema → Task 2
- [x] Internal links in explainer → Task 5
- [x] tools.json updates (mega + more_word_tools + footer_cols) → Task 6
- [x] _redirects clean URL → Task 7
- [x] Build + verify steps → Task 8

**Type consistency:** `SW` object methods referenced consistently throughout — `SW.init()`, `self.generate()`, `self.render()`, `self.speak()`, `self.toggleSave()`, `self.renderSaved()`, `self.enterPractice()`, `self.exitPractice()`, `self.renderPractice()`. All match definitions.

**No placeholders:** All steps contain complete code. No TBDs.

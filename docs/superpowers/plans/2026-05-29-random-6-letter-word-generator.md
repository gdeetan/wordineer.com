# Random 6 Letter Word Generator — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a fully functional Random 6 Letter Word Generator page at `/random-6-letter-word-generator/` matching the Wordineer 3/4/5-letter tool pattern, with Crossword & Game Helper mode and Scrabble score display.

**Architecture:** Static HTML page assembled by `build.py` from a tool-src template. A self-contained IIFE init script handles all interactivity client-side. A new `six-letter-words.json` dataset powers the tool, extracted from existing word data and supplemented as needed.

**Tech Stack:** Python 3 (data extraction + build), Vanilla JS ES5 (tool logic), HTML/CSS (no framework), Cloudflare Pages (hosting).

---

## File Map

| Action | Path |
|--------|------|
| CREATE | `wordineer-deploy/data/six-letter-words.json` |
| CREATE | `wordineer-deploy/data/extract_six_letter_words.py` *(one-time script, keep for re-runs)* |
| CREATE | `template-deploy/tools-src/random-6-letter-word-generator.html` |
| MODIFY | `template-deploy/tools.json` |
| MODIFY | `wordineer-deploy/_redirects` |
| GENERATED | `template-deploy/output/random-6-letter-word-generator.html` *(by build.py)* |
| COPY → | `wordineer-deploy/random-6-letter-word-generator.html` |

**Reference files (read-only):**
- `template-deploy/tools-src/random-5-letter-word-generator.html` — base template to copy
- `wordineer-deploy/data/words.json` — primary word source
- `wordineer-deploy/data/words_expanded.json` — extended word source

---

## Task 1: Extract six-letter-words.json from existing data

**Files:**
- Create: `wordineer-deploy/data/extract_six_letter_words.py`
- Create: `wordineer-deploy/data/six-letter-words.json`

- [ ] **Step 1: Write the extraction script**

Create `wordineer-deploy/data/extract_six_letter_words.py`:

```python
#!/usr/bin/env python3
"""Extract all 6-letter words from existing Wordineer word datasets."""
import json, os, re

BASE = os.path.dirname(__file__)
SOURCES = ['words.json', 'words_expanded.json']
OUT = os.path.join(BASE, 'six-letter-words.json')

seen = set()
results = []

for src in SOURCES:
    path = os.path.join(BASE, src)
    if not os.path.exists(path):
        print(f'  skipping {src} (not found)')
        continue
    with open(path) as f:
        data = json.load(f)
    # Handle both array and dict formats
    if isinstance(data, dict):
        items = list(data.values())
    else:
        items = data
    for item in items:
        w = item.get('w', '')
        # Only pure alpha, exactly 6 letters
        if len(w) != 6 or not re.match(r'^[A-Za-z]+$', w):
            continue
        key = w.lower()
        if key in seen:
            continue
        seen.add(key)
        results.append({
            'w': w[0].upper() + w[1:].lower(),
            't': item.get('t', 'noun'),
            'd': (item.get('d') or '')[:100],
            'diff': item.get('diff', 'medium')
        })

# Sort alphabetically
results.sort(key=lambda x: x['w'].lower())

with open(OUT, 'w') as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print(f'Done. Wrote {len(results)} words to six-letter-words.json')

# Print distribution
easy   = sum(1 for r in results if r['diff'] == 'easy')
medium = sum(1 for r in results if r['diff'] == 'medium')
hard   = sum(1 for r in results if r['diff'] == 'hard')
print(f'  easy:{easy}  medium:{medium}  hard:{hard}')
```

- [ ] **Step 2: Run the extraction script**

```bash
cd wordineer-deploy/data && python3 extract_six_letter_words.py
```

Expected output (approximate):
```
Done. Wrote XXXX words to six-letter-words.json
  easy:XXX  medium:XXX  hard:XXX
```

- [ ] **Step 3: Verify output quality**

```bash
cd wordineer-deploy/data && python3 -c "
import json
data = json.load(open('six-letter-words.json'))
print('Total words:', len(data))
print('First 5:', [d['w'] for d in data[:5]])
print('Sample hard:', next((d for d in data if d['diff']=='hard'), None))
# Check all are exactly 6 letters
bad = [d['w'] for d in data if len(d['w']) != 6]
print('Bad length count:', len(bad))
if bad: print('Examples:', bad[:5])
"
```

Expected: Total ≥ 500, zero bad-length words, sample entries look reasonable.

> **If total < 500:** The existing datasets don't have enough 6-letter coverage. In this case, supplement by running the tool in a browser against a word list API, or manually add entries following the schema until the total reaches at least 500 before proceeding. The tool is functional at 500+ words; 2,000+ is ideal.

- [ ] **Step 4: Commit the data file**

```bash
git add wordineer-deploy/data/six-letter-words.json wordineer-deploy/data/extract_six_letter_words.py
git commit -m "feat: add six-letter-words.json dataset"
```

---

## Task 2: Create the tool source HTML file

**Files:**
- Create: `template-deploy/tools-src/random-6-letter-word-generator.html`

This file is built by copying `random-5-letter-word-generator.html` as the base and applying all changes below. Work through each slot in order.

- [ ] **Step 1: Copy the 5-letter tool as starting base**

```bash
cp template-deploy/tools-src/random-5-letter-word-generator.html \
   template-deploy/tools-src/random-6-letter-word-generator.html
```

- [ ] **Step 2: Update the CONFIG block**

Replace the CONFIG block at the very top of the file:

*Old:*
```
<!-- CONFIG
{
  "url": "/random-5-letter-word-generator/",
  "output": "random-5-letter-word-generator.html"
}
-->
```

*New:*
```
<!-- CONFIG
{
  "url": "/random-6-letter-word-generator/",
  "output": "random-6-letter-word-generator.html"
}
-->
```

- [ ] **Step 3: Replace the SLOT:meta block**

Replace the entire `<!-- SLOT:meta -->` … `<!-- /SLOT:meta -->` block with:

```html
<!-- SLOT:meta -->
<title>Random 6 Letter Word Generator — Free, Instant | Wordineer</title>
<meta name="description" content="Generate random 6-letter words instantly. Filter by difficulty, word type, and letter patterns. Includes Crossword &amp; Game Helper mode with Scrabble score display. Free, no sign-up.">
<link rel="canonical" href="https://wordineer.com/random-6-letter-word-generator/">
<meta property="og:type"        content="website">
<meta property="og:site_name"   content="Wordineer">
<meta property="og:title"       content="Random 6 Letter Word Generator | Wordineer">
<meta property="og:description" content="Generate random 6-letter words with filters for difficulty, type, and letter patterns. Crossword &amp; Game Helper and Scrabble score display included.">
<meta property="og:url"         content="https://wordineer.com/random-6-letter-word-generator/">
<meta property="og:image"       content="https://wordineer.com/og-image.png">
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "What is a 6 letter word generator?",
      "acceptedAnswer": { "@type": "Answer", "text": "A 6 letter word generator randomly selects English words that are exactly six characters long from a curated dataset. You can filter by word type, difficulty level, and letter patterns. This tool also includes a Crossword & Game Helper mode and displays Scrabble point values for every word." }
    },
    {
      "@type": "Question",
      "name": "How many 6-letter words are in English?",
      "acceptedAnswer": { "@type": "Answer", "text": "Estimates vary by dictionary, but most sources put the total between 17,000 and 22,000 six-letter words in common use. This tool's curated dataset covers the most useful ones, tagged by type, difficulty, and definition." }
    },
    {
      "@type": "Question",
      "name": "How does Crossword & Game Helper mode work?",
      "acceptedAnswer": { "@type": "Answer", "text": "Open the Crossword & Game Helper section. Enter a letter in Contains to show only words with that letter. Enter a letter in Does NOT Contain to exclude words with that letter. Combine with Starts With and Ends With filters to pin down a crossword slot or narrow Wordle 6 candidates." }
    },
    {
      "@type": "Question",
      "name": "What does the difficulty rating mean?",
      "acceptedAnswer": { "@type": "Answer", "text": "Easy words are common everyday vocabulary. Medium words are less frequent but widely understood. Hard words are uncommon, specialised, or archaic — useful for advanced vocabulary study or competitive Scrabble." }
    },
    {
      "@type": "Question",
      "name": "Is this tool free?",
      "acceptedAnswer": { "@type": "Answer", "text": "Yes — completely free, no account required, no limits." }
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
    { "@type": "ListItem", "position": 3, "name": "6 Letter Word Generator", "item": "https://wordineer.com/random-6-letter-word-generator/" }
  ]
}
</script>
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "WebApplication",
  "name": "Random 6-Letter Word Generator",
  "url": "https://wordineer.com/random-6-letter-word-generator/",
  "description": "Generate random 6-letter words instantly. Filter by difficulty, word type, and letter patterns. Includes Crossword & Game Helper mode and Scrabble score display. Free, no sign-up.",
  "applicationCategory": "UtilityApplication",
  "operatingSystem": "Web",
  "offers": { "@type": "Offer", "price": "0", "priceCurrency": "USD" },
  "publisher": { "@id": "https://wordineer.com/#organization" }
}
</script>
<!-- /SLOT:meta -->
```

- [ ] **Step 4: Add Scrabble score badge CSS to SLOT:style**

Inside the `<!-- SLOT:style -->` block, add this rule after `.badge-hard { ... }`:

```css
.badge-score { background:#FFF8E1; color:#795548; }
```

- [ ] **Step 5: Replace the SLOT:hero block**

```html
<!-- SLOT:hero -->
<div class="breadcrumb">
  <div class="breadcrumb-inner">
    <a href="/">Wordineer</a>
    <span class="breadcrumb-sep">›</span>
    <a href="/word-tools/">Word Tools</a>
    <span class="breadcrumb-sep">›</span>
    <span aria-current="page">6 Letter Word Generator</span>
  </div>
</div>
<div class="hero">
  <div class="hero-badge">
    <svg viewBox="0 0 11 11" fill="none"><circle cx="5.5" cy="5.5" r="4.5" stroke="#3C3489" stroke-width="1"/><path d="M3.5 5.5l1.5 1.5L8 3.5" stroke="#3C3489" stroke-width="1.2" stroke-linecap="round"/></svg>
    Free · No sign-up · Instant results
  </div>
  <h1>Random 6 Letter Word Generator</h1>
  <p>Generate random 6-letter words in one click. Filter by difficulty, word type, or letter pattern — or use Crossword &amp; Game Helper mode to narrow candidates by known and eliminated letters. Every word shows its Scrabble point value.</p>
</div>
<!-- /SLOT:hero -->
```

- [ ] **Step 6: Update the SLOT:tool — sidebar controls**

In the `<!-- SLOT:tool -->` section, make three changes:

**6a. Rename the Wordle Helper toggle button label** (in the sidebar `<button class="wordle-toggle" ...>`):

*Old:*
```html
<button type="button" class="wordle-toggle" id="wordle-toggle" aria-expanded="false">
  <span>▼ Wordle Helper</span>
  <span style="font-size:10px;font-weight:400;opacity:.7">optional</span>
</button>
<div class="wordle-helper" id="wordle-helper">
  <div class="ctrl-row">
    <label class="ctrl-label" for="ctrl-contains">Contains letter</label>
    <input type="text" id="ctrl-contains" maxlength="1" placeholder="e.g. R" style="text-transform:uppercase;text-align:center;">
  </div>
  <div class="ctrl-row">
    <label class="ctrl-label" for="ctrl-excludes">Does NOT contain</label>
    <input type="text" id="ctrl-excludes" maxlength="1" placeholder="e.g. S" style="text-transform:uppercase;text-align:center;">
  </div>
</div>
```

*New:*
```html
<button type="button" class="wordle-toggle" id="wordle-toggle" aria-expanded="false">
  <span>▼ Crossword &amp; Game Helper</span>
  <span style="font-size:10px;font-weight:400;opacity:.7">optional</span>
</button>
<div class="wordle-helper" id="wordle-helper">
  <div class="ctrl-row">
    <label class="ctrl-label" for="ctrl-contains">Contains letter</label>
    <input type="text" id="ctrl-contains" maxlength="1" placeholder="e.g. R" style="text-transform:uppercase;text-align:center;">
  </div>
  <div class="ctrl-row">
    <label class="ctrl-label" for="ctrl-excludes">Does NOT contain</label>
    <input type="text" id="ctrl-excludes" maxlength="1" placeholder="e.g. S" style="text-transform:uppercase;text-align:center;">
  </div>
</div>
```

**6b. Add sort select to the words-top actions bar** (in `.words-actions`, before the Regenerate button):

*Old:*
```html
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
```

*New:*
```html
<div class="words-actions">
  <select class="act-btn" id="ctrl-sort" aria-label="Sort results" style="cursor:pointer;padding-right:6px;">
    <option value="none">Default</option>
    <option value="az">A → Z</option>
    <option value="za">Z → A</option>
    <option value="score">Score ↓</option>
  </select>
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
```

**6c. Update A-Z browse section** at the bottom of the tool slot:

*Old:*
```html
<div class="az-section">
  <h2>Browse 5-letter words by first letter</h2>
  <p>Looking for all 5-letter words starting with a specific letter? Each page below shows a complete filterable list with definitions and difficulty ratings.</p>
  <div class="az-links">
    <a class="az-link" href="/5-letter-words-starting-with-a/">A</a>
    ... (all 26)
  </div>
</div>
```

*New:*
```html
<div class="az-section">
  <h2>Browse 6-letter words by first letter</h2>
  <p>Looking for all 6-letter words starting with a specific letter? Each page below shows a complete filterable list with definitions and difficulty ratings.</p>
  <div class="az-links">
    <a class="az-link" href="/6-letter-words-starting-with-a/">A</a>
    <a class="az-link" href="/6-letter-words-starting-with-b/">B</a>
    <a class="az-link" href="/6-letter-words-starting-with-c/">C</a>
    <a class="az-link" href="/6-letter-words-starting-with-d/">D</a>
    <a class="az-link" href="/6-letter-words-starting-with-e/">E</a>
    <a class="az-link" href="/6-letter-words-starting-with-f/">F</a>
    <a class="az-link" href="/6-letter-words-starting-with-g/">G</a>
    <a class="az-link" href="/6-letter-words-starting-with-h/">H</a>
    <a class="az-link" href="/6-letter-words-starting-with-i/">I</a>
    <a class="az-link" href="/6-letter-words-starting-with-j/">J</a>
    <a class="az-link" href="/6-letter-words-starting-with-k/">K</a>
    <a class="az-link" href="/6-letter-words-starting-with-l/">L</a>
    <a class="az-link" href="/6-letter-words-starting-with-m/">M</a>
    <a class="az-link" href="/6-letter-words-starting-with-n/">N</a>
    <a class="az-link" href="/6-letter-words-starting-with-o/">O</a>
    <a class="az-link" href="/6-letter-words-starting-with-p/">P</a>
    <a class="az-link" href="/6-letter-words-starting-with-q/">Q</a>
    <a class="az-link" href="/6-letter-words-starting-with-r/">R</a>
    <a class="az-link" href="/6-letter-words-starting-with-s/">S</a>
    <a class="az-link" href="/6-letter-words-starting-with-t/">T</a>
    <a class="az-link" href="/6-letter-words-starting-with-u/">U</a>
    <a class="az-link" href="/6-letter-words-starting-with-v/">V</a>
    <a class="az-link" href="/6-letter-words-starting-with-w/">W</a>
    <a class="az-link" href="/6-letter-words-starting-with-x/">X</a>
    <a class="az-link" href="/6-letter-words-starting-with-y/">Y</a>
    <a class="az-link" href="/6-letter-words-starting-with-z/">Z</a>
  </div>
</div>
```

- [ ] **Step 7: Replace the SLOT:explainer block**

Replace the entire `<!-- SLOT:explainer -->` … `<!-- /SLOT:explainer -->` block with:

```html
<!-- SLOT:explainer -->
<div class="explainer">

  <h2>What is a 6 letter word generator?</h2>
  <p>A 6 letter word generator randomly selects English words that are exactly six characters long from a curated dataset. Unlike a dictionary search — where you need to know what you're looking for — a generator surfaces words you might not have thought of, filtered to whatever constraints you set. This one lets you narrow results by word type (noun, verb, adjective, adverb), difficulty level (easy, medium, hard), and letter patterns. Every result shows a Scrabble point value and an optional definition, so the tool is useful whether you're hunting for a high-scoring play or building vocabulary from scratch.</p>
  <p>Six-letter words occupy a particularly useful position in English vocabulary. They're long enough to carry specific, concrete meaning — long enough, in fact, that they dominate crossword grids and fuel Scrabble endgames. Short enough to be memorable and speakable. They represent the point where words graduate from conversational basics into richer, more expressive territory.</p>

  <h2>Why use a 6 letter word generator?</h2>

  <h3>Word games and Scrabble</h3>
  <p>Six-letter words are where Scrabble strategy starts to get serious. A well-placed six-letter word across a triple-word square can score 30–45 points. Even better: a six-letter word on your rack means you're one tile away from a seven-letter bingo — playing all seven tiles earns an automatic 50-point bonus. The difficulty filter lets you drill uncommon high-value words (Hard) or build pattern recognition for common plays (Easy). Use Sort by Score to surface the highest-point options from any generated batch instantly.</p>

  <h3>Crossword solving</h3>
  <p>Six-letter slots are among the most common lengths in standard American crossword grids. When you have a few confirmed letters but can't crack the answer, the Crossword & Game Helper lets you combine Starts With, Ends With, and Contains filters to narrow the field to a handful of candidates. It's faster and more targeted than scanning a dictionary page — and the definitions mean you can confirm the right answer on the spot.</p>

  <h3>Creative writing and naming</h3>
  <p>Six letters is a naming sweet spot. Long enough to feel like a real, meaningful word — short enough to be a clean domain name, product name, or character name. Writers use random word generators to break creative blocks: generate ten words, pick the one that sparks something, and build from there. The word type filter lets you focus on nouns for naming exercises or adjectives for writing prompts. Six-letter words also have natural rhythm — try using them as first lines in freewriting sessions.</p>

  <h3>Vocabulary building</h3>
  <p>Mid-length words are the easiest to retain. The brain can process them as single units rather than letter-by-letter decoding, which means they stick faster than long technical terms. Set difficulty to Hard, enable definitions, and generate 15–20 words you don't know. Spend 30 seconds on each one. Come back tomorrow and generate the same settings — the overlap will test what you've actually retained. Adding two or three words a week compounds over a year into a meaningfully stronger vocabulary.</p>

  <h3>Teaching and classroom use</h3>
  <p>Six-letter words sit comfortably at the upper-elementary and middle-school vocabulary level. Filter by Easy nouns for a third-grade spelling list, or push to Hard adjectives for an advanced class. The definitions toggle means you can use the output directly in a worksheet without looking up each word separately. Copy the list in one-per-line format and paste it straight into your document in one click.</p>

  <h2>How it works</h2>
  <p>The generator pulls from a curated dataset of 6-letter English words, each tagged with its word type, difficulty level, and definition. When you click Generate, it randomly selects words matching your active filters and displays results instantly — including the Scrabble point value for each word, calculated from standard tile values.</p>
  <p>On first load, a built-in seed of common words renders immediately with no wait. The full dataset loads in the background at browser idle time. All filters and sorting apply client-side with no server round-trips — change any setting and the list refreshes without clicking Generate again.</p>

  <h2>Tips for getting the most out of this tool</h2>

  <h3>For crossword players</h3>
  <p>Combine Starts With and Contains to pin down a specific slot. For example: a six-letter word starting with B that contains the letter Z — set Starts With to B, open Game Helper, set Contains to Z, and generate. You'll get a short list of candidates to check against your clue.</p>

  <h3>For Scrabble players</h3>
  <p>Use Sort by Score to immediately see which words from your filtered results have the highest Scrabble value. Filter by Hard and Noun to drill uncommon high-value plays that opponents are unlikely to block. Six-letter words ending in common suffixes (-TION, -NESS, -MENT) are often easier to form from a mixed rack.</p>

  <h3>For writers</h3>
  <p>Set type to Adjective and difficulty to Easy for punchy, clean descriptors that don't slow a reader down. Set type to Noun and difficulty to Medium for grounded, specific nouns that make sentences concrete. Generate 5–10 words and write one sentence using each — the constraint forces creative decisions you'd otherwise skip.</p>

  <h3>For teachers</h3>
  <p>Set count to 10, difficulty to Easy, and type to Noun for a manageable weekly spelling list. Use Medium for vocabulary enrichment exercises, Hard for gifted programmes. Enable definitions, generate, and copy directly — no extra reference lookup needed.</p>

</div>
<!-- /SLOT:explainer -->
```

- [ ] **Step 8: Replace the SLOT:faq block**

```html
<!-- SLOT:faq -->
<div class="faq">
  <h2 class="faq-title">Frequently asked questions</h2>

  <div class="faq-item open">
    <div class="faq-q"><span class="faq-q-text">What is a 6 letter word generator?</span><svg class="faq-chevron" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div>
    <div class="faq-a">A 6 letter word generator randomly selects English words that are exactly six characters long. You can filter by word type, difficulty, and letter patterns. Every result shows a Scrabble point value and an optional definition. This tool also includes a Crossword &amp; Game Helper mode for narrowing candidates by confirmed and eliminated letters.</div>
  </div>

  <div class="faq-item">
    <div class="faq-q"><span class="faq-q-text">How many 6-letter words are in English?</span><svg class="faq-chevron" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div>
    <div class="faq-a">Estimates vary depending on the dictionary, but most sources put it between 17,000 and 22,000 six-letter words in common use. This tool's curated dataset covers the most useful ones tagged with type, difficulty, and definition — with more being added over time.</div>
  </div>

  <div class="faq-item">
    <div class="faq-q"><span class="faq-q-text">How does Crossword &amp; Game Helper mode work?</span><svg class="faq-chevron" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div>
    <div class="faq-a">Open the Crossword &amp; Game Helper section in the filters. Enter a letter in Contains to show only words with that letter. Enter a letter in Does NOT Contain to exclude words with that letter. Combine with Starts With and Ends With to pin down a crossword slot or narrow Wordle 6 candidates after gathering information from earlier guesses.</div>
  </div>

  <div class="faq-item">
    <div class="faq-q"><span class="faq-q-text">What does the difficulty rating mean?</span><svg class="faq-chevron" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div>
    <div class="faq-a">Easy words are common everyday vocabulary. Medium words are less frequent but widely understood. Hard words are uncommon, specialised, or archaic — useful for advanced vocabulary study or competitive Scrabble prep.</div>
  </div>

  <div class="faq-item">
    <div class="faq-q"><span class="faq-q-text">Can I use this for Scrabble or crosswords?</span><svg class="faq-chevron" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div>
    <div class="faq-a">Yes. Every word displays its Scrabble point total — use Sort by Score to surface the highest-value plays. For crosswords, combine Starts With, Ends With, and Contains filters in Game Helper mode to narrow a specific slot to a short candidate list.</div>
  </div>

  <div class="faq-item">
    <div class="faq-q"><span class="faq-q-text">Is this tool free?</span><svg class="faq-chevron" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div>
    <div class="faq-a">Completely free, forever. No account required, no limits, no paywalls.</div>
  </div>

  <div class="faq-item">
    <div class="faq-q"><span class="faq-q-text">How do I copy the word list?</span><svg class="faq-chevron" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div>
    <div class="faq-a">Click the Copy List button above the results and choose your format — one per line for documents, comma-separated for spreadsheets, or space-separated for other tools. To copy a single word, click the copy icon on its card.</div>
  </div>
</div>
<!-- /SLOT:faq -->
```

- [ ] **Step 9: Replace the SLOT:who block**

```html
<!-- SLOT:who -->
<div>
  <h2 class="section-title" style="margin-bottom:14px">Who uses this tool</h2>
  <div class="uc-grid">
    <div class="uc"><div class="uc-title">Word game players</div><div class="uc-body">Sort by Scrabble Score to find the highest-value plays instantly. Use Game Helper mode to crack crossword slots and Wordle 6 guesses.</div></div>
    <div class="uc"><div class="uc-title">Writers &amp; creatives</div><div class="uc-body">Generate naming options for brands, products, or characters. Six letters hit the sweet spot between meaningful and memorable.</div></div>
    <div class="uc"><div class="uc-title">Students &amp; learners</div><div class="uc-body">Filter by difficulty to target the right vocabulary level. Definitions are built in, so you can study meaning and usage without opening a second tab.</div></div>
    <div class="uc"><div class="uc-title">Teachers &amp; educators</div><div class="uc-body">Generate a spelling or vocabulary list in seconds. Filter by word type and difficulty, then copy in one click for immediate use in worksheets or tests.</div></div>
  </div>
</div>
<!-- /SLOT:who -->
```

- [ ] **Step 10: Replace the SLOT:init block with the full updated JS**

Replace the entire `<!-- SLOT:init -->` … `<!-- /SLOT:init -->` block with:

```html
<!-- SLOT:init -->
<script>
(function () {
  var SEED = [
    {w:"Banter",t:"noun",d:"the playful and friendly exchange of teasing remarks",diff:"easy"},
    {w:"Breeze",t:"noun",d:"a gentle wind",diff:"easy"},
    {w:"Bridge",t:"noun",d:"a structure carrying a road over a river or gap",diff:"easy"},
    {w:"Butter",t:"noun",d:"a pale yellow fatty substance made from cream",diff:"easy"},
    {w:"Castle",t:"noun",d:"a large medieval fortified building",diff:"easy"},
    {w:"Coffee",t:"noun",d:"a drink made from roasted ground coffee beans",diff:"easy"},
    {w:"Dancer",t:"noun",d:"a person who dances",diff:"easy"},
    {w:"Dollar",t:"noun",d:"the basic monetary unit of the US and other countries",diff:"easy"},
    {w:"Finger",t:"noun",d:"each of the four digits of the hand",diff:"easy"},
    {w:"Flower",t:"noun",d:"the seed-bearing part of a plant",diff:"easy"},
    {w:"Forest",t:"noun",d:"a large area covered chiefly with trees",diff:"easy"},
    {w:"Friend",t:"noun",d:"a person you know well and regard with affection",diff:"easy"},
    {w:"Garden",t:"noun",d:"a piece of ground for growing flowers, vegetables, or fruit",diff:"easy"},
    {w:"Gentle",t:"adjective",d:"mild in temperament or behaviour; kind",diff:"easy"},
    {w:"Honest",t:"adjective",d:"free of deceit; truthful and sincere",diff:"easy"},
    {w:"Mirror",t:"noun",d:"a reflective surface, typically glass coated with metal",diff:"easy"},
    {w:"Mother",t:"noun",d:"a female parent",diff:"easy"},
    {w:"Muscle",t:"noun",d:"a band of tissue whose contraction produces movement",diff:"easy"},
    {w:"Planet",t:"noun",d:"a celestial body orbiting a star",diff:"easy"},
    {w:"Purple",t:"adjective",d:"of a colour intermediate between red and blue",diff:"easy"},
    {w:"Rather",t:"adverb",d:"used to indicate preference or a higher degree",diff:"easy"},
    {w:"Silver",t:"noun",d:"a precious shiny white metal",diff:"easy"},
    {w:"Simple",t:"adjective",d:"easily understood or done; not complex",diff:"easy"},
    {w:"Summer",t:"noun",d:"the warmest season of the year",diff:"easy"},
    {w:"Winter",t:"noun",d:"the coldest season of the year",diff:"easy"},
    {w:"Bright",t:"adjective",d:"giving out or reflecting a lot of light",diff:"easy"},
    {w:"Change",t:"verb",d:"to make or become different",diff:"easy"},
    {w:"Choice",t:"noun",d:"an act of selecting between two or more possibilities",diff:"easy"},
    {w:"Corner",t:"noun",d:"a place where two sides or edges meet",diff:"easy"},
    {w:"Danger",t:"noun",d:"the possibility of suffering harm or injury",diff:"easy"},
    {w:"Admire",t:"verb",d:"to regard with respect or warm approval",diff:"medium"},
    {w:"Afford",t:"verb",d:"to have enough money to pay for something",diff:"medium"},
    {w:"Cipher",t:"noun",d:"a secret or disguised way of writing; a code",diff:"medium"},
    {w:"Cobalt",t:"noun",d:"a hard silvery-white magnetic metal element",diff:"medium"},
    {w:"Famine",t:"noun",d:"extreme scarcity of food across a region",diff:"medium"},
    {w:"Gallop",t:"verb",d:"to run at the fastest speed",diff:"medium"},
    {w:"Gravel",t:"noun",d:"a loose aggregation of small water-worn stones",diff:"medium"},
    {w:"Hamlet",t:"noun",d:"a small settlement smaller than a village",diff:"medium"},
    {w:"Ignite",t:"verb",d:"to catch fire or set on fire",diff:"medium"},
    {w:"Jargon",t:"noun",d:"special words used by a particular group",diff:"medium"},
    {w:"Luster",t:"noun",d:"a gentle sheen or soft glow",diff:"medium"},
    {w:"Mortal",t:"adjective",d:"subject to death; causing death",diff:"medium"},
    {w:"Mystic",t:"adjective",d:"relating to mysticism or the spiritual",diff:"medium"},
    {w:"Nimble",t:"adjective",d:"quick and light in movement",diff:"medium"},
    {w:"Astute",t:"adjective",d:"having an ability to accurately assess situations",diff:"medium"},
    {w:"Rustic",t:"adjective",d:"relating to the countryside; simple and unsophisticated",diff:"medium"},
    {w:"Shrill",t:"adjective",d:"high-pitched and piercing in sound",diff:"medium"},
    {w:"Tangle",t:"verb",d:"to twist together into a confused mass",diff:"medium"},
    {w:"Wander",t:"verb",d:"to walk or move in a leisurely way",diff:"medium"},
    {w:"Zephyr",t:"noun",d:"a soft, gentle breeze",diff:"hard"},
    {w:"Quartz",t:"noun",d:"a hard mineral consisting of silicon and oxygen",diff:"hard"},
    {w:"Loquat",t:"noun",d:"a small yellow egg-shaped fruit from East Asia",diff:"hard"},
    {w:"Myriad",t:"adjective",d:"countless or very great in number",diff:"hard"},
    {w:"Limpid",t:"adjective",d:"clear and transparent; easily understood",diff:"hard"}
  ];

  var SCRABBLE = {A:1,E:1,I:1,O:1,U:1,L:1,N:1,S:1,T:1,R:1,D:2,G:2,B:3,C:3,M:3,P:3,F:4,H:4,V:4,W:4,Y:4,K:5,J:8,X:8,Q:10,Z:10};
  function scoreWord(w) {
    return w.toUpperCase().split('').reduce(function(sum, c) { return sum + (SCRABBLE[c] || 0); }, 0);
  }

  var allWords = SEED.slice();
  var currentWords = [];
  var savedWords = [];
  var fullLoaded = false;
  var showDefs = true;

  function diffBadge(d) {
    return d === 'easy' ? 'badge-easy' : d === 'medium' ? 'badge-medium' : 'badge-hard';
  }

  var HEART_SVG = '<svg viewBox="0 0 14 14" fill="none"><path d="M7 12s-5-3.5-5-7a3 3 0 016 0 3 3 0 016 0c0 3.5-5 7-5 7z" stroke="currentColor" stroke-width="1.3"/></svg>';
  var COPY_SVG  = '<svg viewBox="0 0 14 14" fill="none"><rect x="4" y="4" width="8" height="8" rx="1.5" stroke="currentColor" stroke-width="1.3"/><path d="M2 10V2h8" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/></svg>';

  function getFiltered() {
    var type     = document.getElementById('ctrl-type').value;
    var diff     = document.getElementById('ctrl-diff').value;
    var first    = (document.getElementById('ctrl-first').value || '').toUpperCase();
    var last     = (document.getElementById('ctrl-last').value  || '').toUpperCase();
    var contains = (document.getElementById('ctrl-contains').value || '').toUpperCase();
    var excludes = (document.getElementById('ctrl-excludes').value || '').toUpperCase();

    return allWords.filter(function (w) {
      var wu = w.w.toUpperCase();
      if (type !== 'all' && w.t !== type) return false;
      if (diff !== 'all' && w.diff !== diff) return false;
      if (first && wu[0] !== first) return false;
      if (last  && wu[wu.length - 1] !== last) return false;
      if (contains && wu.indexOf(contains) === -1) return false;
      if (excludes && wu.indexOf(excludes) !== -1) return false;
      return true;
    });
  }

  function pickRandom(pool, n) {
    var copy = pool.slice();
    var result = [];
    while (result.length < n && copy.length) {
      var i = Math.floor(Math.random() * copy.length);
      result.push(copy.splice(i, 1)[0]);
    }
    return result;
  }

  function sortWords(words) {
    var sort = document.getElementById('ctrl-sort').value;
    if (sort === 'az') return words.slice().sort(function(a,b){ return a.w.localeCompare(b.w); });
    if (sort === 'za') return words.slice().sort(function(a,b){ return b.w.localeCompare(a.w); });
    if (sort === 'score') return words.slice().sort(function(a,b){ return scoreWord(b.w) - scoreWord(a.w); });
    return words;
  }

  function renderList() {
    var n = parseInt(document.getElementById('ctrl-count').value, 10);
    if (isNaN(n) || n < 1 || n > 50) return;

    var pool = getFiltered();
    var total = pool.length;
    currentWords = sortWords(pickRandom(pool, n));
    showDefs = document.getElementById('ctrl-defs').checked;

    document.getElementById('word-count').textContent =
      'Showing ' + currentWords.length + ' of ' + total + ' matching words';

    var list = document.getElementById('word-list');
    if (currentWords.length === 0) {
      list.innerHTML = '<li style="padding:20px 0;color:var(--text-3);font-size:13px">No words match your filters. Try broadening the selection.</li>';
      return;
    }

    list.innerHTML = currentWords.map(function (w) {
      var isSaved = savedWords.indexOf(w.w) !== -1;
      var pts = scoreWord(w.w);
      return '<li class="word-item">' +
        '<div class="word-left">' +
          '<div class="word-text">' + w.w + '</div>' +
          '<div class="word-badges">' +
            '<span class="badge badge-type">' + w.t + '</span>' +
            '<span class="badge ' + diffBadge(w.diff) + '">' + w.diff + '</span>' +
            '<span class="badge badge-score">' + pts + ' pts</span>' +
          '</div>' +
          (showDefs && w.d ? '<div class="word-def">' + w.d + '</div>' : '') +
        '</div>' +
        '<div class="word-right">' +
          '<button class="icon-btn' + (isSaved ? ' saved' : '') + '" data-word="' + w.w + '" aria-label="Save ' + w.w + '" onclick="toggleSave(this)">' + HEART_SVG + '</button>' +
          '<button class="icon-btn" aria-label="Copy ' + w.w + '" onclick="copyWord(this,\'' + w.w + '\')">' + COPY_SVG + '</button>' +
        '</div>' +
      '</li>';
    }).join('');
  }

  window.toggleSave = function (btn) {
    var word = btn.getAttribute('data-word');
    var idx = savedWords.indexOf(word);
    if (idx === -1) { savedWords.push(word); btn.classList.add('saved'); }
    else { savedWords.splice(idx, 1); btn.classList.remove('saved'); }
    renderSaved();
  };

  window.copyWord = function (btn, word) {
    navigator.clipboard.writeText(word).then(function () {
      btn.innerHTML = '✓';
      setTimeout(function () { btn.innerHTML = COPY_SVG; }, 1000);
    });
  };

  function renderSaved() {
    var container = document.getElementById('saved-tags');
    var countEl   = document.getElementById('saved-count');
    countEl.textContent = '(' + savedWords.length + ')';
    if (savedWords.length === 0) {
      container.innerHTML = '<span class="saved-empty">Click the heart on any word to save it here</span>';
      return;
    }
    container.innerHTML = savedWords.map(function (w) {
      return '<span class="saved-tag">' + w +
        '<span class="saved-tag-remove" onclick="removeSaved(\'' + w + '\')" aria-label="Remove ' + w + '">×</span>' +
      '</span>';
    }).join('');
  }

  window.removeSaved = function (word) {
    savedWords = savedWords.filter(function (w) { return w !== word; });
    document.querySelectorAll('[data-word="' + word + '"]').forEach(function (b) { b.classList.remove('saved'); });
    renderSaved();
  };

  function validateAndGenerate() {
    var raw = parseInt(document.getElementById('ctrl-count').value, 10);
    var err = document.getElementById('count-error');
    var inp = document.getElementById('ctrl-count');
    if (isNaN(raw) || raw < 1 || raw > 50) {
      err.classList.add('show'); inp.classList.add('input-error'); return;
    }
    err.classList.remove('show'); inp.classList.remove('input-error');
    renderList();
  }

  function loadFull() {
    if (fullLoaded) return;
    fullLoaded = true;
    fetch('/data/six-letter-words.json')
      .then(function (r) { return r.json(); })
      .then(function (data) { allWords = data; renderList(); })
      .catch(function () {});
  }

  // Generate / regen buttons
  document.getElementById('word-gen-btn').addEventListener('click', function () { loadFull(); validateAndGenerate(); });
  document.getElementById('word-regen-btn').addEventListener('click', function () { loadFull(); validateAndGenerate(); });

  // Real-time filter updates
  ['ctrl-type','ctrl-diff','ctrl-first','ctrl-last','ctrl-contains','ctrl-excludes','ctrl-defs','ctrl-sort'].forEach(function (id) {
    var el = document.getElementById(id);
    if (!el) return;
    el.addEventListener('change', function () { loadFull(); validateAndGenerate(); });
    el.addEventListener('input',  function () { loadFull(); validateAndGenerate(); });
  });

  document.getElementById('ctrl-count').addEventListener('input',  validateAndGenerate);
  document.getElementById('ctrl-count').addEventListener('change', validateAndGenerate);

  // Game Helper toggle
  document.getElementById('wordle-toggle').addEventListener('click', function () {
    var helper = document.getElementById('wordle-helper');
    var btn    = document.getElementById('wordle-toggle');
    var open   = helper.classList.toggle('open');
    btn.classList.toggle('active', open);
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
  });

  // Copy All dropdown
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

  // Copy saved
  document.getElementById('saved-copy-btn').addEventListener('click', function () {
    if (!savedWords.length) return;
    navigator.clipboard.writeText(savedWords.join('\n'));
  });

  // Reset
  document.getElementById('word-reset-btn').addEventListener('click', function () {
    ['ctrl-type','ctrl-diff','ctrl-first','ctrl-last','ctrl-contains','ctrl-excludes'].forEach(function (id) {
      var el = document.getElementById(id);
      if (el) el.value = el.tagName === 'SELECT' ? el.options[0].value : '';
    });
    document.getElementById('ctrl-count').value = 20;
    document.getElementById('ctrl-defs').checked = true;
    document.getElementById('ctrl-sort').value = 'none';
    document.getElementById('wordle-helper').classList.remove('open');
    document.getElementById('wordle-toggle').classList.remove('active');
    validateAndGenerate();
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

  // FAQ accordion
  document.querySelectorAll('.faq-item').forEach(function (item) {
    var q = item.querySelector('.faq-q');
    if (q) q.addEventListener('click', function () { item.classList.toggle('open'); });
  });

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

- [ ] **Step 11: Commit the new tool source file**

```bash
git add template-deploy/tools-src/random-6-letter-word-generator.html
git commit -m "feat: add random-6-letter-word-generator tool source"
```

---

## Task 3: Update tools.json

**Files:**
- Modify: `template-deploy/tools.json`

- [ ] **Step 1: Add to mega nav — Writing & Vocabulary tools array**

In `template-deploy/tools.json`, find the `"mega"` array → first object with `"cat": "Writing &amp; Vocabulary"` → its `"tools"` array. Add after the 3-letter entry:

```json
{ "href": "/random-6-letter-word-generator/", "text": "6 Letter Word Generator" }
```

So the tools array becomes:
```json
"tools": [
  { "href": "/", "text": "Random Word Generator" },
  { "href": "/random-sentence-generator/", "text": "Random Sentence Generator" },
  { "href": "/random-4-letter-word-generator/", "text": "4 Letter Word Generator" },
  { "href": "/random-3-letter-word-generator/", "text": "3 Letter Word Generator" },
  { "href": "/random-6-letter-word-generator/", "text": "6 Letter Word Generator" },
  { "href": "/random-paragraph-generator/", "text": "Random Paragraph Generator", "status": "planned" },
  { "href": "/word-counter/", "text": "Word Counter", "status": "planned" }
]
```

- [ ] **Step 2: Add to more_word_tools array**

In the `"more_word_tools"` flat array, add after the 4-letter entry (after `{ "href": "/random-4-letter-word-generator/", ... }`):

```json
{
  "href": "/random-6-letter-word-generator/",
  "name": "6 Letter Word Generator",
  "desc": "Random 6-letter words with Scrabble scores and crossword helper.",
  "icon_bg": "#EEEDFE",
  "icon_path": "<path d=\"M2 4h9M2 7h7M2 10h5\" stroke=\"#534AB7\" stroke-width=\"1.3\" stroke-linecap=\"round\"/>"
}
```

- [ ] **Step 3: Add to other_tools — Writing & Vocabulary links array**

In the `"other_tools"` array → first object with `"cat": "Writing &amp; Vocabulary"` → its `"links"` array. Add after the 3-letter entry:

```json
{ "href": "/random-6-letter-word-generator/", "text": "6 Letter Word Generator" }
```

- [ ] **Step 4: Add to footer_cols — Writing & Vocabulary links array**

In the `"footer_cols"` array → first object with `"title": "Writing &amp; Vocabulary"` → its `"links"` array. Add after the 3-letter entry:

```json
{ "href": "/random-6-letter-word-generator/", "text": "6 Letter Word Generator" }
```

- [ ] **Step 2: Commit tools.json**

```bash
git add template-deploy/tools.json
git commit -m "feat: add 6-letter word generator to tools.json nav/footer"
```

---

## Task 4: Add clean URL redirect

**Files:**
- Modify: `wordineer-deploy/_redirects`

- [ ] **Step 1: Add the redirect line**

Open `wordineer-deploy/_redirects` and add this line alongside the existing letter-length redirects:

```
/random-6-letter-word-generator   /random-6-letter-word-generator/   301
```

- [ ] **Step 2: Commit**

```bash
git add wordineer-deploy/_redirects
git commit -m "feat: add redirect for random-6-letter-word-generator clean URL"
```

---

## Task 5: Build, copy, preview, and verify

**Files:**
- Generate: `template-deploy/output/random-6-letter-word-generator.html`
- Copy to: `wordineer-deploy/random-6-letter-word-generator.html`

- [ ] **Step 1: Run the build**

```bash
cd template-deploy && python3 build.py
```

Expected: No errors. `output/random-6-letter-word-generator.html` created.

If build errors: check that all SLOT names and CONFIG JSON in the new tool-src file are valid (no unclosed tags, valid JSON in CONFIG block).

- [ ] **Step 2: Copy output to deploy folder**

```bash
cp template-deploy/output/random-6-letter-word-generator.html wordineer-deploy/
```

- [ ] **Step 3: Start local preview server**

```bash
cd wordineer-deploy && python3 -m http.server 8080
```

Open `http://localhost:8080/random-6-letter-word-generator.html` in a browser.

- [ ] **Step 4: Verify seed load**

On page load (before any click), confirm:
- Words appear immediately (seed words)
- Each word shows: word text, type badge, difficulty badge, **score badge** (e.g. "8 pts")
- Definitions visible (definitions toggle is on by default)

- [ ] **Step 5: Verify full dataset load**

Click Generate. Confirm word count in header increases (e.g. "Showing 20 of 847 matching words" rather than the seed count).

- [ ] **Step 6: Verify all filters**

Test each filter:
- Word type: set to Nouns only → all results should show noun badge
- Difficulty: set to Easy → all results should show easy badge
- Starts with: enter "B" → all results start with B
- Ends with: enter "E" → all results end with E

- [ ] **Step 7: Verify Game Helper**

Open the Crossword & Game Helper section:
- Enter "R" in Contains → all results contain the letter R
- Enter "S" in Does NOT contain → no results contain S
- Combine both → results contain R but not S

- [ ] **Step 8: Verify Scrabble sort**

Change sort dropdown to "Score ↓":
- Results re-order from highest pts to lowest
- Spot check: QUARTZ should score 24 pts (Q=10, U=1, A=1, R=1, T=1, Z=10)

- [ ] **Step 9: Verify copy formats**

Click Copy list → One per line: paste into a text editor and confirm words are newline-separated.
Click Copy list → Comma-separated: paste and confirm comma-separated.

- [ ] **Step 10: Verify save and bulk copy**

Click the heart on 3 words. Confirm they appear in the Saved Words section below. Click Copy saved → paste and confirm all 3 words appear.

- [ ] **Step 11: Verify Space key shortcut**

Click on empty page area (not an input). Press Space. Confirm results refresh.

- [ ] **Step 12: Verify mobile layout**

Resize browser to < 700px width. Confirm:
- Controls stack above results
- "More options" toggle appears and hides/shows advanced filters
- A-Z links are visible and clickable

- [ ] **Step 13: Verify nav/footer**

Check that the 6-letter word generator link appears in the site navigation mega-menu and footer (injected from tools.json).

- [ ] **Step 14: Commit final output**

```bash
git add wordineer-deploy/random-6-letter-word-generator.html
git commit -m "build: generate and add random-6-letter-word-generator output page"
```

---

## Verification Checklist (summary)

- [ ] Seed words appear on page load with no fetch delay
- [ ] Full dataset loads async (word count increases after generate)
- [ ] Type, difficulty, starts-with, ends-with filters all work
- [ ] Game Helper contains/excludes filters work correctly
- [ ] Scrabble score badge shows on every word
- [ ] Sort by Score orders results high → low (QUARTZ = 24 pts)
- [ ] Copy list formats: line/comma/space all correct
- [ ] Save words: add, remove, bulk copy works
- [ ] Space key regenerates
- [ ] Mobile: "More options" toggle works
- [ ] Nav mega-menu and footer show 6-letter generator link
- [ ] Clean URL redirect works: `/random-6-letter-word-generator` → `/random-6-letter-word-generator/`
- [ ] No autofocus on load (PageSpeed compliance)

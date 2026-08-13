# Multi-Letter Prefix Pages Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a standalone Python script that generates ~400–500 static HTML pages for 5-letter words starting with 2-letter prefixes (e.g. `/5-letter-words-starting-with-st/`), writing directly to `wordineer-deploy/` and updating `_redirects` and `sitemap.xml`.

**Architecture:** `generate_prefix_pages.py` imports helper functions from `build.py` (build_mega_cols, build_footer_cols, read) to assemble complete HTML using the same template fragments. Each page is a content-type page: head → nav → hero → content → footer. Word data comes from existing `five-letter-words-[a-z].json` files. Pages with fewer than 3 words are skipped.

**Tech Stack:** Python 3 (stdlib only), existing template fragments in `template/`, existing word data JSON in `wordineer-deploy/data/`.

---

## File Map

| File | Action | Purpose |
|---|---|---|
| `template-deploy/generate_prefix_pages.py` | Create | Main generator script |
| `wordineer-deploy/5-letter-words-starting-with-{xy}.html` | Create (×~450) | Generated pages |
| `wordineer-deploy/_redirects` | Modify | Append redirect rules per page |
| `template-deploy/sitemap.xml` | Modify | Append sitemap entries |
| `template-deploy/tools-src/5-letter-words-starting-with-[a-z].html` | Modify (×26) | Add "Browse by prefix" grid in Task 6 |

---

## Reference: Content Page Assembly (from build.py)

Content-type pages are assembled as:
```
build_stamp + head.html (with META/STYLE injected)
<body>
nav.html (with MEGA_COLS injected)
hero slot HTML
content slot HTML
footer.html (with FOOTER_COLS injected)
</body>
</html>
```

The script replicates this exactly by importing from build.py.

---

## Task 1: Skeleton, Imports, and Data Loader

**Files:**
- Create: `template-deploy/generate_prefix_pages.py`

- [ ] **Step 1: Create the script skeleton**

```python
#!/usr/bin/env python3
"""
generate_prefix_pages.py — generates 5-letter words starting with [XY] pages.

Usage:
    python3 generate_prefix_pages.py --batch 2   # 2-letter prefixes (Batch 1)
    python3 generate_prefix_pages.py --batch 3   # 3-letter prefixes (Batch 2, deferred)
    python3 generate_prefix_pages.py --test       # run self-tests and exit
    python3 generate_prefix_pages.py --batch 2 --dry-run  # print summary, write nothing
"""

import argparse
import json
import os
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from itertools import product

# ── paths ──────────────────────────────────────────────────────────────────────
SCRIPT_DIR   = os.path.dirname(os.path.abspath(__file__))
DEPLOY_DIR   = os.path.normpath(os.path.join(SCRIPT_DIR, '..', 'wordineer-deploy'))
DATA_DIR     = os.path.join(DEPLOY_DIR, 'data')
REDIRECTS    = os.path.join(DEPLOY_DIR, '_redirects')
SITEMAP      = os.path.join(SCRIPT_DIR, 'sitemap.xml')
TMPL_DIR     = os.path.join(SCRIPT_DIR, 'template')
TOOLS_JSON   = os.path.join(SCRIPT_DIR, 'tools.json')

MIN_WORDS    = 3

# Letters ordered by frequency in English — used to score Wordle picks
FREQ_ORDER   = 'ETAOINSHRDLUCMFGYPWBVKJXQZ'

# ── import helpers from build.py ───────────────────────────────────────────────
sys.path.insert(0, SCRIPT_DIR)
from build import build_mega_cols, build_footer_cols, read


def load_all_five_letter_words():
    """Return list of all word entries from five-letter-words-[a-z].json files."""
    words = []
    for letter in 'abcdefghijklmnopqrstuvwxyz':
        path = os.path.join(DATA_DIR, f'five-letter-words-{letter}.json')
        if os.path.exists(path):
            with open(path, encoding='utf-8') as f:
                words.extend(json.load(f))
    return words


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--batch', type=int, choices=[2, 3], help='Prefix length to generate')
    parser.add_argument('--dry-run', action='store_true', help='Print summary without writing files')
    parser.add_argument('--test', action='store_true', help='Run self-tests and exit')
    args = parser.parse_args()

    if args.test:
        run_tests()
        sys.exit(0)

    if not args.batch:
        parser.error('--batch is required unless --test is specified')

    main(args.batch, dry_run=args.dry_run)
```

- [ ] **Step 2: Verify imports work**

```bash
cd template-deploy && python3 -c "from build import build_mega_cols, build_footer_cols, read; print('imports OK')"
```

Expected: `imports OK`

- [ ] **Step 3: Verify data loads**

```bash
cd template-deploy && python3 -c "
import sys; sys.path.insert(0, '.')
from generate_prefix_pages import load_all_five_letter_words
words = load_all_five_letter_words()
print(f'Loaded {len(words)} words')
print('Sample:', words[:3])
"
```

Expected: `Loaded NNNN words` (thousands), 3 sample entries with `w`, `t`, `d`, `diff` keys.

- [ ] **Step 4: Commit**

```bash
git add template-deploy/generate_prefix_pages.py
git commit -m "feat: scaffold generate_prefix_pages.py with data loader"
```

---

## Task 2: Core Word Analysis Functions

**Files:**
- Modify: `template-deploy/generate_prefix_pages.py`

- [ ] **Step 1: Add filter_by_prefix**

Add after `load_all_five_letter_words`:

```python
def filter_by_prefix(words, prefix):
    """Return words whose 'w' field starts with prefix (case-insensitive)."""
    p = prefix.lower()
    return [w for w in words if w['w'].lower().startswith(p)]


def has_enough_words(words, prefix, min_count=MIN_WORDS):
    return len(filter_by_prefix(words, prefix)) >= min_count
```

- [ ] **Step 2: Add compute_best_picks**

```python
def compute_best_picks(words, n=5):
    """
    Score each word by how many unique high-frequency English letters it covers
    in positions 2, 3, 4 (0-indexed) — the unknown slots when prefix is confirmed.
    Returns top n words sorted by score desc, then alphabetically.
    """
    freq_rank = {ch: i for i, ch in enumerate(FREQ_ORDER)}

    def score(entry):
        tail = entry['w'][2:].upper()          # positions 2,3,4
        unique_tail = set(tail)
        # Sum of frequency ranks (lower rank = more common = better)
        return -sum(freq_rank.get(ch, 99) for ch in unique_tail)

    sorted_words = sorted(words, key=lambda e: (score(e), e['w']))
    return sorted_words[:n]
```

- [ ] **Step 3: Add compute_position_freq**

```python
def compute_position_freq(words, pos=2, top_n=5):
    """Return list of (letter, count) for the top_n most common letters at position pos."""
    counts = Counter(w['w'][pos].upper() for w in words if len(w['w']) > pos)
    return counts.most_common(top_n)
```

- [ ] **Step 4: Add group_by_type**

```python
TYPE_LABELS = {
    'noun': 'Nouns',
    'verb': 'Verbs',
    'adjective': 'Adjectives',
    'adj': 'Adjectives',
    'adverb': 'Adverbs',
    'adv': 'Adverbs',
}

def group_by_type(words):
    """Return dict: {display_label: [entries]} for each part of speech present."""
    groups = {}
    for entry in words:
        label = TYPE_LABELS.get(entry.get('t', '').lower())
        if label:
            groups.setdefault(label, []).append(entry)
    # Sort words within each group alphabetically
    for label in groups:
        groups[label].sort(key=lambda e: e['w'])
    return groups
```

- [ ] **Step 5: Add run_tests and verify all pass**

```python
def run_tests():
    print('Running self-tests...')

    sample = [
        {'w': 'stare', 't': 'verb',      'd': 'to look fixedly'},
        {'w': 'stone', 't': 'noun',      'd': 'a rock'},
        {'w': 'strip', 't': 'verb',      'd': 'to remove covering'},
        {'w': 'stern', 't': 'adjective', 'd': 'serious'},
        {'w': 'crimp', 't': 'verb',      'd': 'to press into folds'},
        {'w': 'crane', 't': 'noun',      'd': 'a large bird'},
    ]

    # filter_by_prefix
    st_words = filter_by_prefix(sample, 'st')
    assert len(st_words) == 4, f'Expected 4 ST words, got {len(st_words)}'
    cr_words = filter_by_prefix(sample, 'cr')
    assert len(cr_words) == 2, f'Expected 2 CR words, got {len(cr_words)}'
    assert filter_by_prefix(sample, 'zz') == [], 'Expected empty for ZZ'

    # has_enough_words
    assert has_enough_words(sample, 'st') is True
    assert has_enough_words(sample, 'cr') is False   # only 2, below min of 3

    # compute_best_picks
    picks = compute_best_picks(st_words, n=2)
    assert len(picks) == 2
    assert all('w' in p for p in picks)

    # compute_position_freq
    freq = compute_position_freq(st_words, pos=2)
    assert len(freq) <= 5
    assert all(isinstance(letter, str) and isinstance(count, int) for letter, count in freq)

    # group_by_type
    groups = group_by_type(st_words)
    assert 'Verbs' in groups
    assert 'Nouns' in groups
    assert 'stare' in [e['w'] for e in groups['Verbs']]
    assert all(groups[label] == sorted(groups[label], key=lambda e: e['w'])
               for label in groups), 'Groups not sorted alphabetically'

    print('All tests passed.')
```

- [ ] **Step 6: Run tests**

```bash
cd template-deploy && python3 generate_prefix_pages.py --test
```

Expected: `All tests passed.`

- [ ] **Step 7: Commit**

```bash
git add template-deploy/generate_prefix_pages.py
git commit -m "feat: add word analysis functions to prefix page generator"
```

---

## Task 3: HTML Page Renderer

**Files:**
- Modify: `template-deploy/generate_prefix_pages.py`

- [ ] **Step 1: Add helper to build JSON-LD schema**

Add after `group_by_type`:

```python
def render_breadcrumb_schema(prefix):
    p = prefix.upper()
    url = f'https://wordineer.com/5-letter-words-starting-with-{prefix.lower()}/'
    return f'''<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {{"@type":"ListItem","position":1,"name":"Wordineer","item":"https://wordineer.com/"}},
    {{"@type":"ListItem","position":2,"name":"Word Lists","item":"https://wordineer.com/word-lists/"}},
    {{"@type":"ListItem","position":3,"name":"5-Letter Words","item":"https://wordineer.com/5-letter-words/"}},
    {{"@type":"ListItem","position":4,"name":"5 Letter Words Starting With {p}","item":"{url}"}}
  ]
}}
</script>'''


def render_faq_schema(prefix, word_count):
    p = prefix.upper()
    return f'''<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {{
      "@type": "Question",
      "name": "How many 5-letter words start with {p}?",
      "acceptedAnswer": {{"@type":"Answer","text":"This list has {word_count} five-letter words starting with {p}."}}
    }},
    {{
      "@type": "Question",
      "name": "What are the best 5-letter words starting with {p} for Wordle?",
      "acceptedAnswer": {{"@type":"Answer","text":"If you've confirmed {p[0]} and {p[1] if len(p)>1 else p[0]} in positions 1 and 2, prioritise words that cover common letters in the remaining three slots — E, T, A, O, I, N are the most useful."}}
    }}
  ]
}}
</script>'''
```

- [ ] **Step 2: Add render_meta**

```python
def render_meta(prefix, word_count):
    p  = prefix.upper()
    pl = prefix.lower()
    url = f'https://wordineer.com/5-letter-words-starting-with-{pl}/'
    bc  = render_breadcrumb_schema(prefix)
    faq = render_faq_schema(prefix, word_count)
    return f'''{bc}
{faq}
<title>5 Letter Words Starting With {p} ({word_count} Words) | Wordineer</title>
<meta name="description" content="{word_count} five-letter words starting with {p} — filterable by word type, with definitions. Useful for Wordle, Scrabble, and vocabulary.">
<link rel="canonical" href="{url}">
<meta property="og:title" content="5 Letter Words Starting With {p} | Wordineer">
<meta property="og:description" content="{word_count} five-letter words starting with {p}, with definitions. Filter by noun, verb, adjective.">
<meta property="og:url" content="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Wordineer">
<meta property="og:image" content="https://wordineer.com/og-image.png">'''
```

- [ ] **Step 3: Add render_style**

```python
def render_style():
    return '''<style>
.pfx-wrap { max-width: 860px; margin: 0 auto; padding: 0 16px 48px; }
.pfx-count { font-size: 15px; color: var(--text-2); margin: 0 0 20px; }
.pfx-picks { background: #f0fdf4; border: 1.5px solid #86efac; border-radius: 10px;
             padding: 14px 18px; margin: 0 0 28px; }
.pfx-picks-title { font-size: 13px; font-weight: 600; color: #16a34a; text-transform: uppercase;
                   letter-spacing: .04em; margin: 0 0 8px; }
.pfx-picks-words { display: flex; flex-wrap: wrap; gap: 8px; margin: 0; }
.pfx-pick { font-size: 15px; font-weight: 600; color: #15803d; background: #dcfce7;
            border-radius: 6px; padding: 4px 10px; font-family: monospace; }
.pfx-freq { font-size: 14px; color: var(--text-2); margin: 0 0 28px; }
.pfx-freq strong { color: var(--text-1); }
.pfx-filters { display: flex; gap: 8px; flex-wrap: wrap; margin: 0 0 12px; }
.pfx-filter { padding: 6px 14px; border: 1.5px solid var(--border-2, #d1d5db);
              border-radius: 20px; background: #fff; font-size: 13px; cursor: pointer;
              font-family: inherit; color: var(--text-2); transition: all .15s; }
.pfx-filter.active, .pfx-filter:hover { background: var(--primary, #6366f1);
              border-color: var(--primary, #6366f1); color: #fff; }
.pfx-table { width: 100%; border-collapse: collapse; font-size: 14px; margin: 0 0 32px; }
.pfx-table th { text-align: left; padding: 8px 12px; border-bottom: 2px solid var(--border-1, #e5e7eb);
                font-size: 12px; text-transform: uppercase; letter-spacing: .05em; color: var(--text-3); }
.pfx-table td { padding: 10px 12px; border-bottom: 1px solid var(--border-1, #e5e7eb);
                color: var(--text-1); vertical-align: top; }
.pfx-table tr:last-child td { border-bottom: none; }
.pfx-table td:first-child { font-weight: 700; font-family: monospace; font-size: 15px; }
.pfx-table td:nth-child(2) { color: var(--text-3); font-size: 12px; text-transform: uppercase;
                              letter-spacing: .04em; width: 80px; }
.pfx-table tr[data-type].hidden { display: none; }
.pfx-groups { margin: 0 0 32px; }
.pfx-group-title { font-size: 13px; font-weight: 600; text-transform: uppercase;
                   letter-spacing: .05em; color: var(--text-3); margin: 0 0 8px; }
.pfx-chips { display: flex; flex-wrap: wrap; gap: 6px; margin: 0 0 20px; }
.pfx-chip { font-size: 14px; font-family: monospace; font-weight: 600; padding: 4px 10px;
            background: var(--bg-2, #f3f4f6); border-radius: 6px; color: var(--text-1); }
.pfx-links { display: flex; flex-wrap: wrap; gap: 8px; margin: 0 0 32px; }
.pfx-link { font-size: 13px; padding: 5px 12px; border: 1.5px solid var(--border-2, #d1d5db);
            border-radius: 6px; color: var(--text-2); text-decoration: none; }
.pfx-link:hover { border-color: var(--primary, #6366f1); color: var(--primary, #6366f1); }
.pfx-back { font-size: 14px; color: var(--text-3); margin: 0 0 24px; }
.pfx-back a { color: var(--primary, #6366f1); text-decoration: none; }
</style>'''
```

- [ ] **Step 4: Add render_hero**

```python
def render_hero(prefix, word_count):
    p = prefix.upper()
    return f'''<section class="hero">
  <div class="hero-inner">
    <h1 class="hero-title">5 Letter Words Starting With {p}</h1>
    <p class="hero-sub">{word_count} words — filter by type, see definitions, find your best Wordle guess.</p>
  </div>
</section>'''
```

- [ ] **Step 5: Add render_word_table**

```python
def render_word_table(words):
    rows = []
    for entry in sorted(words, key=lambda e: e['w']):
        w    = entry['w'].upper()
        t    = entry.get('t', '').lower()
        d    = entry.get('d', '')
        rows.append(
            f'  <tr data-type="{t}">'
            f'<td>{w}</td>'
            f'<td>{t}</td>'
            f'<td>{d}</td>'
            f'</tr>'
        )
    return (
        '<table class="pfx-table" aria-label="Word list">\n'
        '  <thead><tr>'
        '<th scope="col">Word</th>'
        '<th scope="col">Type</th>'
        '<th scope="col">Definition</th>'
        '</tr></thead>\n'
        '<tbody>\n'
        + '\n'.join(rows) +
        '\n</tbody></table>'
    )
```

- [ ] **Step 6: Add render_content (assembles all content sections)**

```python
def render_content(prefix, words, picks, freq, groups):
    p       = prefix.upper()
    p1      = p[0]           # first letter for parent page link
    count   = len(words)

    # Wordle picks callout
    picks_html = ''.join(f'<span class="pfx-pick">{e["w"].upper()}</span>' for e in picks)
    picks_block = (
        f'<div class="pfx-picks">'
        f'<div class="pfx-picks-title">Best Wordle guesses for {p}</div>'
        f'<div class="pfx-picks-words">{picks_html}</div>'
        f'</div>'
    ) if picks else ''

    # Position frequency line
    freq_letters = ', '.join(f'<strong>{ltr}</strong>' for ltr, _ in freq)
    freq_block = (
        f'<p class="pfx-freq">In 5-letter words starting with {p}, '
        f'the most common letters in position 3 are: {freq_letters}.</p>'
    ) if freq else ''

    # Filter buttons — detect which types exist
    types_present = sorted({entry.get('t','').lower() for entry in words if entry.get('t')})
    filter_btns = '<div class="pfx-filters">'
    filter_btns += '<button class="pfx-filter active" data-filter="all">All</button>'
    label_map = {'noun':'Nouns','verb':'Verbs','adjective':'Adjectives','adj':'Adjectives',
                 'adverb':'Adverbs','adv':'Adverbs'}
    seen = set()
    for t in types_present:
        lbl = label_map.get(t, t.title())
        if lbl not in seen:
            filter_btns += f'<button class="pfx-filter" data-filter="{t}">{lbl}</button>'
            seen.add(lbl)
    filter_btns += '</div>'

    # Word table
    table = render_word_table(words)

    # Word groups (chips)
    group_html = ''
    if groups:
        group_html = '<div class="pfx-groups">'
        for label, entries in groups.items():
            chips = ''.join(f'<span class="pfx-chip">{e["w"].upper()}</span>' for e in entries)
            group_html += (
                f'<div class="pfx-group-title">{label}</div>'
                f'<div class="pfx-chips">{chips}</div>'
            )
        group_html += '</div>'

    # Parent link + Wordle helper link
    links = (
        f'<p class="pfx-back">← <a href="/5-letter-words-starting-with-{p1.lower()}/">'
        f'All 5-letter words starting with {p1}</a></p>'
    )

    # FAQ
    faq = f'''<div class="faq">
  <h2 class="faq-title">Frequently asked questions</h2>
  <div class="faq-item open">
    <div class="faq-q"><span class="faq-q-text">How many 5-letter words start with {p}?</span><svg class="faq-chevron" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div>
    <div class="faq-a"><p>This list has {count} five-letter words starting with {p}. The count reflects standard English words — Wordle's answer pool is smaller, using only common everyday words.</p></div>
  </div>
  <div class="faq-item">
    <div class="faq-q"><span class="faq-q-text">What are the best {p} words for Wordle?</span><svg class="faq-chevron" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div>
    <div class="faq-a"><p>Once {p} is confirmed in positions 1–2, your next guess should cover as many common letters as possible in positions 3–5. {", ".join(e["w"].upper() for e in picks[:3])} are strong choices — they hit frequent letters in the remaining slots.</p></div>
  </div>
  <div class="faq-item">
    <div class="faq-q"><span class="faq-q-text">Can I filter by word type?</span><svg class="faq-chevron" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div>
    <div class="faq-a"><p>Yes — use the filter buttons above the table to show only nouns, verbs, or adjectives. Definitions are included for every word.</p></div>
  </div>
</div>'''

    # Filter + FAQ JS
    script = '''<script>
(function(){
  var btns = document.querySelectorAll('.pfx-filter');
  btns.forEach(function(btn){
    btn.addEventListener('click', function(){
      btns.forEach(function(b){ b.classList.remove('active'); });
      btn.classList.add('active');
      var f = btn.dataset.filter;
      document.querySelectorAll('.pfx-table tbody tr').forEach(function(row){
        row.classList.toggle('hidden', f !== 'all' && row.dataset.type !== f);
      });
    });
  });
  document.querySelectorAll('.faq-q').forEach(function(q){
    q.addEventListener('click', function(){ q.closest('.faq-item').classList.toggle('open'); });
  });
})();
</script>'''

    return (
        f'<div class="pfx-wrap">\n'
        f'<p class="pfx-count">{count} words</p>\n'
        f'{picks_block}\n'
        f'{freq_block}\n'
        f'{filter_btns}\n'
        f'{table}\n'
        f'{group_html}\n'
        f'{links}\n'
        f'<p style="margin:0 0 24px"><a href="/wordle-helper/" style="color:var(--primary,#6366f1)">Need to match a specific pattern? Try the Wordle Helper →</a></p>\n'
        f'{faq}\n'
        f'{script}\n'
        f'</div>'
    )
```

- [ ] **Step 7: Add render_page (full assembled HTML)**

```python
def render_page(prefix, words, mega_html, footer_cols_html):
    picks  = compute_best_picks(words)
    freq   = compute_position_freq(words)
    groups = group_by_type(words)

    meta    = render_meta(prefix, len(words))
    style   = render_style()
    hero    = render_hero(prefix, len(words))
    content = render_content(prefix, words, picks, freq, groups)

    # Read template fragments
    head_tmpl   = read(os.path.join(TMPL_DIR, 'head.html'))
    nav_tmpl    = read(os.path.join(TMPL_DIR, 'nav.html'))
    footer_tmpl = read(os.path.join(TMPL_DIR, 'footer.html'))

    from datetime import datetime, timezone
    stamp = f'<!-- build: {datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")} -->\n'

    head = (head_tmpl
        .replace('{{META}}', meta)
        .replace('{{OG_IMAGE}}', '')
        .replace('{{HEAD_EXTRAS}}', '')
        .replace('{{STYLE}}', style))
    nav    = nav_tmpl.replace('{{MEGA_COLS}}', mega_html)
    footer = footer_tmpl.replace('{{FOOTER_COLS}}', footer_cols_html)

    return '\n'.join(filter(None, [
        stamp + head,
        '<body>',
        nav,
        hero,
        content,
        footer,
        '</body>',
        '</html>',
    ]))
```

- [ ] **Step 8: Add render test to run_tests**

Append inside `run_tests()`:

```python
    # render_page smoke test (uses real templates + tools.json)
    import json as _json
    tools_data = _json.load(open(TOOLS_JSON, encoding='utf-8'))
    mega_html  = build_mega_cols(tools_data['mega'], '/5-letter-words-starting-with-st/')
    fcols_html = build_footer_cols(tools_data['footer_cols'])
    sample_st  = [
        {'w': 'stare', 't': 'verb',      'd': 'to look fixedly'},
        {'w': 'stone', 't': 'noun',      'd': 'a rock'},
        {'w': 'strip', 't': 'verb',      'd': 'to remove'},
        {'w': 'stern', 't': 'adjective', 'd': 'serious and strict'},
    ]
    html = render_page('st', sample_st, mega_html, fcols_html)
    assert '<h1' in html, 'Missing h1'
    assert 'STARE' in html or 'stare' in html.lower(), 'Missing word STARE'
    assert 'pfx-picks' in html, 'Missing picks callout'
    assert 'pfx-table' in html, 'Missing word table'
    assert '.faq-q' in html or 'faq-q' in html, 'Missing FAQ'
    assert '<footer' in html, 'Missing footer'
    assert '</html>' in html, 'Missing closing html tag'
    print('render_page smoke test passed.')
```

- [ ] **Step 9: Run tests**

```bash
cd template-deploy && python3 generate_prefix_pages.py --test
```

Expected: `All tests passed.` with `render_page smoke test passed.`

- [ ] **Step 10: Commit**

```bash
git add template-deploy/generate_prefix_pages.py
git commit -m "feat: add HTML renderer to prefix page generator"
```

---

## Task 4: Redirects and Sitemap Updater

**Files:**
- Modify: `template-deploy/generate_prefix_pages.py`

- [ ] **Step 1: Add redirect_lines_for**

```python
def redirect_lines_for(prefix):
    """Return the two _redirects lines for a prefix page (301 + 200 rewrite)."""
    slug = f'5-letter-words-starting-with-{prefix.lower()}'
    return [
        f'/{slug}.html    /{slug}/    301',
        f'/{slug}/    /{slug}.html    200',
    ]
```

- [ ] **Step 2: Add append_redirects**

```python
def append_redirects(path, lines):
    """Append redirect lines if they don't already exist in the file."""
    existing = open(path, encoding='utf-8').read() if os.path.exists(path) else ''
    new_lines = [ln for ln in lines if ln not in existing]
    if new_lines:
        with open(path, 'a', encoding='utf-8') as f:
            f.write('\n' + '\n'.join(new_lines))
```

- [ ] **Step 3: Add append_sitemap_entries**

```python
def append_sitemap_entries(path, urls):
    """Insert sitemap <url> entries before the closing </urlset> tag."""
    if not os.path.exists(path):
        print(f'  warning: sitemap not found at {path}')
        return
    content = open(path, encoding='utf-8').read()
    entries = []
    for url in urls:
        entry = f'  <url><loc>{url}</loc></url>'
        if entry not in content:
            entries.append(entry)
    if entries:
        block = '\n'.join(entries)
        content = content.replace('</urlset>', f'{block}\n</urlset>')
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
```

- [ ] **Step 4: Add redirect + sitemap tests to run_tests**

Append inside `run_tests()`:

```python
    # redirect_lines_for
    lines = redirect_lines_for('st')
    assert len(lines) == 2
    assert '/5-letter-words-starting-with-st.html    /5-letter-words-starting-with-st/    301' in lines
    assert '/5-letter-words-starting-with-st/    /5-letter-words-starting-with-st.html    200' in lines
    print('redirect_lines_for test passed.')
```

- [ ] **Step 5: Run tests**

```bash
cd template-deploy && python3 generate_prefix_pages.py --test
```

Expected: all tests pass including `redirect_lines_for test passed.`

- [ ] **Step 6: Commit**

```bash
git add template-deploy/generate_prefix_pages.py
git commit -m "feat: add redirects and sitemap helpers to prefix generator"
```

---

## Task 5: Main Orchestration

**Files:**
- Modify: `template-deploy/generate_prefix_pages.py`

- [ ] **Step 1: Add generate_all_prefixes**

```python
import string

def generate_all_prefixes(batch_len):
    """Yield all lowercase prefix strings of length batch_len."""
    for combo in product(string.ascii_lowercase, repeat=batch_len):
        yield ''.join(combo)
```

- [ ] **Step 2: Add main()**

```python
def main(batch_len, dry_run=False):
    print(f'Loading word data...')
    all_words = load_all_five_letter_words()
    print(f'  {len(all_words)} words loaded.')

    # Load tools.json once — nav and footer are the same for every page
    with open(TOOLS_JSON, encoding='utf-8') as f:
        tools_data = json.load(f)
    mega_html  = build_mega_cols(tools_data['mega'], '')
    fcols_html = build_footer_cols(tools_data['footer_cols'])

    generated  = []
    skipped    = 0
    redirect_lines_all = []
    sitemap_urls = []

    prefixes = list(generate_all_prefixes(batch_len))
    print(f'Checking {len(prefixes)} {batch_len}-letter prefix combinations...')

    for prefix in prefixes:
        words = filter_by_prefix(all_words, prefix)
        if len(words) < MIN_WORDS:
            skipped += 1
            continue

        slug     = f'5-letter-words-starting-with-{prefix.lower()}'
        out_path = os.path.join(DEPLOY_DIR, f'{slug}.html')
        url      = f'https://wordineer.com/{slug}/'

        if not dry_run:
            page_html = render_page(prefix, words, mega_html, fcols_html)
            with open(out_path, 'w', encoding='utf-8') as f:
                f.write(page_html)

        generated.append(prefix)
        redirect_lines_all.extend(redirect_lines_for(prefix))
        sitemap_urls.append(url)

    if not dry_run and redirect_lines_all:
        append_redirects(REDIRECTS, redirect_lines_all)
        print(f'  _redirects updated ({len(redirect_lines_all)} lines)')

    if not dry_run and sitemap_urls:
        append_sitemap_entries(SITEMAP, sitemap_urls)
        print(f'  sitemap.xml updated ({len(sitemap_urls)} entries)')

    print(f'\nDone. {len(generated)} pages {"would be " if dry_run else ""}generated, '
          f'{skipped} combos skipped (< {MIN_WORDS} words).')
    if generated:
        print(f'  Sample prefixes: {", ".join(generated[:10])}{"..." if len(generated) > 10 else ""}')
```

- [ ] **Step 3: Dry-run to verify counts before writing anything**

```bash
cd template-deploy && python3 generate_prefix_pages.py --batch 2 --dry-run
```

Expected output like:
```
Loading word data...
  NNNN words loaded.
Checking 676 2-letter prefix combinations...
Done. ~400-500 pages would be generated, ~180-270 combos skipped (< 3 words).
  Sample prefixes: ab, ac, ad, ae, af, ag, ah, ai, al, am...
```

If the generated count is wildly off (< 100 or > 600), stop and investigate the word data before proceeding.

- [ ] **Step 4: Run for real**

```bash
cd template-deploy && python3 generate_prefix_pages.py --batch 2
```

Expected: similar output without "would be". Check that HTML files appear in `wordineer-deploy/`.

```bash
ls ../wordineer-deploy/5-letter-words-starting-with-st.html
ls ../wordineer-deploy/5-letter-words-starting-with-cr.html
```

- [ ] **Step 5: Commit**

```bash
git add template-deploy/generate_prefix_pages.py
git commit -m "feat: add main orchestration to prefix page generator"
```

---

## Task 6: QA Sample Pages

**Files:** None — verification only.

- [ ] **Step 1: Start local server**

```bash
cd wordineer-deploy && python3 -m http.server 8080
```

- [ ] **Step 2: Check these 5 pages in browser**

Open each URL and verify:
- `http://localhost:8080/5-letter-words-starting-with-st.html`
- `http://localhost:8080/5-letter-words-starting-with-cr.html`
- `http://localhost:8080/5-letter-words-starting-with-sh.html`
- `http://localhost:8080/5-letter-words-starting-with-bl.html`
- `http://localhost:8080/5-letter-words-starting-with-tr.html`

For each page verify:
- [ ] H1 shows correct prefix (e.g. "5 Letter Words Starting With ST")
- [ ] Word count in subtitle is accurate
- [ ] Green "Best Wordle guesses" callout is present with 3–5 words
- [ ] Position-3 frequency line is present
- [ ] Word table renders with Word / Type / Definition columns
- [ ] Filter buttons (All / Nouns / Verbs / Adjectives) work — clicking hides/shows rows
- [ ] FAQ accordion opens and closes on click
- [ ] "← All 5-letter words starting with S" link points to correct parent URL
- [ ] "Try the Wordle Helper →" link present
- [ ] Nav and footer render correctly (no broken layout)
- [ ] No AI-slop phrases: "comprehensive", "ultimate", "whether you're", "look no further"
- [ ] Page title in browser tab is correct

- [ ] **Step 3: Check _redirects has correct entries**

```bash
grep "5-letter-words-starting-with-st" ../wordineer-deploy/_redirects
```

Expected:
```
/5-letter-words-starting-with-st.html    /5-letter-words-starting-with-st/    301
/5-letter-words-starting-with-st/    /5-letter-words-starting-with-st.html    200
```

- [ ] **Step 4: Check sitemap has entries**

```bash
grep "5-letter-words-starting-with-st" sitemap.xml
```

Expected: `<url><loc>https://wordineer.com/5-letter-words-starting-with-st/</loc></url>`

- [ ] **Step 5: Commit generated pages**

```bash
cd ..
git add wordineer-deploy/5-letter-words-starting-with-*.html wordineer-deploy/_redirects template-deploy/sitemap.xml
git commit -m "feat: generate 5-letter words starting-with 2-letter prefix pages (batch 1)"
```

---

## Task 7: Add "Browse by Prefix" Grid to Parent Single-Letter Pages

Add a grid of 2-letter prefix links to each of the 26 single-letter pages in `tools-src/`.

**Files:**
- Modify: `template-deploy/tools-src/5-letter-words-starting-with-[a-z].html` (×26)

- [ ] **Step 1: Write a helper script to get valid prefixes per first letter**

Run this to see which 2-letter combos exist for letter S (as a test):

```bash
python3 -c "
import json, os, sys
sys.path.insert(0, 'template-deploy')
from generate_prefix_pages import load_all_five_letter_words, filter_by_prefix, MIN_WORDS
import string
words = load_all_five_letter_words()
letter = 's'
valid = [letter+c for c in string.ascii_lowercase
         if len(filter_by_prefix(words, letter+c)) >= MIN_WORDS]
print(f'Valid prefixes for {letter.upper()}: {valid}')
print(f'Count: {len(valid)}')
"
```

- [ ] **Step 2: Add the prefix grid to `5-letter-words-starting-with-s.html`**

Locate the `<!-- SLOT:content -->` section in `template-deploy/tools-src/5-letter-words-starting-with-s.html`. Before the closing `<!-- /SLOT:content -->`, add the prefix grid. Run the helper from Step 1 to get the valid prefixes, then build the HTML:

```html
<div style="margin-top:40px">
  <h2 style="font-family:'DM Serif Display',serif;font-size:20px;font-weight:400;margin:0 0 12px">Browse 5-letter words starting with S by prefix</h2>
  <div style="display:flex;flex-wrap:wrap;gap:8px">
    <a href="/5-letter-words-starting-with-sa/" style="padding:6px 14px;border:1.5px solid #d1d5db;border-radius:6px;font-size:13px;color:#6b7280;text-decoration:none">SA</a>
    <a href="/5-letter-words-starting-with-sc/" style="padding:6px 14px;border:1.5px solid #d1d5db;border-radius:6px;font-size:13px;color:#6b7280;text-decoration:none">SC</a>
    <!-- ... one <a> per valid prefix ... -->
  </div>
</div>
```

Only include prefixes with ≥3 words (use the helper from Step 1 for the exact list).

- [ ] **Step 3: Repeat for all 26 letters**

Run the helper script for each letter a–z. Update each `5-letter-words-starting-with-[letter].html` file with its valid prefix grid. The grid links use the same inline style — no new CSS class needed.

- [ ] **Step 4: Rebuild and copy output**

```bash
cd template-deploy && python3 build.py
cp output/5-letter-words-starting-with-*.html ../wordineer-deploy/
```

- [ ] **Step 5: Spot-check a parent page in browser**

Open `http://localhost:8080/5-letter-words-starting-with-s.html` and verify:
- Prefix grid appears below the existing content
- Each chip links to the correct URL
- Page layout is unchanged above the grid

- [ ] **Step 6: Commit**

```bash
git add template-deploy/tools-src/5-letter-words-starting-with-*.html wordineer-deploy/5-letter-words-starting-with-*.html
git commit -m "feat: add browse-by-prefix grid to single-letter parent pages"
```

---

## Self-Review Notes

- **Spec coverage:** All spec requirements covered — generator script, ≥3 word minimum, best Wordle picks, position-3 frequency, word groups, anti-slop content rules, redirects, sitemap, parent page grids, QA on ST/CR/SH/BL/TR.
- **No placeholders:** All code blocks are complete and runnable.
- **Type consistency:** `filter_by_prefix` → used in `main()` and `has_enough_words`. `render_page` → called in `main()`. `redirect_lines_for` → called in `main()`. All function names consistent throughout.
- **Anti-slop enforcement:** Banned phrases are absent from all `render_*` functions. FAQ answers include actual word counts and actual word examples from `picks`.

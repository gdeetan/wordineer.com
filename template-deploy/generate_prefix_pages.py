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
import html
import json
import os
import re
import string
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
        if not os.path.exists(path):
            continue
        try:
            with open(path, encoding='utf-8') as f:
                words.extend(json.load(f))
        except json.JSONDecodeError as e:
            print(f'  warning: could not parse {path}: {e}', file=sys.stderr)
    if not words:
        print(f'  warning: no five-letter word data found in {DATA_DIR}', file=sys.stderr)
    return words


def filter_by_prefix(words, prefix):
    """Return words whose 'w' field starts with prefix (case-insensitive)."""
    p = prefix.lower()
    return [w for w in words if w['w'].lower().startswith(p)]


def has_enough_words(words, prefix, min_count=MIN_WORDS):
    return len(filter_by_prefix(words, prefix)) >= min_count


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
        # Lower rank index = more common letter. Sum of ranks = lower is better.
        return sum(freq_rank.get(ch, len(FREQ_ORDER)) for ch in unique_tail)

    sorted_words = sorted(words, key=lambda e: (score(e), e['w']))
    return sorted_words[:n]


def compute_position_freq(words, pos=2, top_n=5):
    """Return list of (letter, count) for the top_n most common letters at position pos."""
    counts = Counter(w['w'][pos].upper() for w in words if len(w['w']) > pos)
    return counts.most_common(top_n)


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
    for label in groups:
        groups[label].sort(key=lambda e: e['w'])
    return groups


def render_breadcrumb_schema(prefix):
    p   = prefix.upper()
    pl  = prefix.lower()
    url = f'https://wordineer.com/5-letter-words-starting-with-{pl}/'
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


def render_faq_schema(prefix, word_count, picks):
    p    = prefix.upper()
    pl   = prefix.lower()
    p1   = p[0]
    p2   = p[1] if len(p) > 1 else p[0]
    top3 = ', '.join(e['w'].upper() for e in picks[:3]) if picks else 'common words'
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
      "acceptedAnswer": {{"@type":"Answer","text":"With {p1} and {p2} confirmed in positions 1 and 2, try {top3} — they cover common letters in the remaining slots."}}
    }}
  ]
}}
</script>'''


def render_meta(prefix, word_count, picks):
    p   = prefix.upper()
    pl  = prefix.lower()
    url = f'https://wordineer.com/5-letter-words-starting-with-{pl}/'
    bc  = render_breadcrumb_schema(prefix)
    faq = render_faq_schema(prefix, word_count, picks)
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


def render_style():
    return '''<style>
.pfx-wrap { max-width: 860px; margin: 0 auto; padding: 32px 16px 48px; }
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
.pfx-back { font-size: 14px; color: var(--text-3); margin: 0 0 24px; }
.pfx-back a { color: var(--primary, #6366f1); text-decoration: none; }
</style>'''


def render_breadcrumb(prefix):
    p  = prefix.upper()
    p1 = prefix[0].lower()
    return (
        '<div class="breadcrumb">\n'
        '  <div class="breadcrumb-inner">\n'
        '    <a href="/">Wordineer</a>\n'
        '    <span class="breadcrumb-sep">›</span>\n'
        '    <a href="/word-lists/">Word Lists</a>\n'
        '    <span class="breadcrumb-sep">›</span>\n'
        f'    <a href="/5-letter-words-starting-with-{p1}/">5-Letter Words Starting With {p[0]}</a>\n'
        '    <span class="breadcrumb-sep">›</span>\n'
        f'    <span aria-current="page">Starting With {p}</span>\n'
        '  </div>\n'
        '</div>'
    )


def render_hero(prefix, word_count):
    p = prefix.upper()
    return f'''<section class="hero">
  <div class="hero-inner">
    <h1 class="hero-title">5 Letter Words Starting With {p}</h1>
    <p class="hero-sub">{word_count} words — filter by type, see definitions, find your best Wordle guess.</p>
  </div>
</section>'''


def render_word_table(words):
    rows = []
    for entry in sorted(words, key=lambda e: e['w']):
        w = html.escape(entry['w'].upper())
        t = entry.get('t', '').lower()
        d = html.escape(entry.get('d', ''))
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


def render_content(prefix, words, picks, freq, groups):
    p     = prefix.upper()
    p1    = p[0]
    count = len(words)

    # Wordle picks callout
    picks_html  = ''.join(f'<span class="pfx-pick">{e["w"].upper()}</span>' for e in picks)
    picks_block = (
        f'<div class="pfx-picks">'
        f'<div class="pfx-picks-title">Best Wordle guesses for {p}</div>'
        f'<div class="pfx-picks-words">{picks_html}</div>'
        f'</div>'
    ) if picks else ''

    # Position frequency line
    freq_letters = ', '.join(f'<strong>{ltr}</strong>' for ltr, _ in freq)
    freq_block   = (
        f'<p class="pfx-freq">In 5-letter words starting with {p}, '
        f'the most common letters in position 3 are: {freq_letters}.</p>'
    ) if freq else ''

    # Filter buttons
    types_present = sorted({entry.get('t', '').lower() for entry in words if entry.get('t')})
    filter_btns   = '<div class="pfx-filters">'
    filter_btns  += '<button class="pfx-filter active" data-filter="all">All</button>'
    label_map = {'noun': 'Nouns', 'verb': 'Verbs', 'adjective': 'Adjectives',
                 'adj': 'Adjectives', 'adverb': 'Adverbs', 'adv': 'Adverbs'}
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
            chips      = ''.join(f'<span class="pfx-chip">{e["w"].upper()}</span>' for e in entries)
            group_html += (
                f'<div class="pfx-group-title">{label}</div>'
                f'<div class="pfx-chips">{chips}</div>'
            )
        group_html += '</div>'

    # Parent link
    back_link = (
        f'<p class="pfx-back">← <a href="/5-letter-words-starting-with-{p1.lower()}/">'
        f'All 5-letter words starting with {p1}</a></p>'
    )

    # Wordle helper link
    wordle_link = (
        '<p style="margin:0 0 24px">'
        '<a href="/wordle-helper/" style="color:var(--primary,#6366f1)">'
        'Need to match a specific pattern? Try the Wordle Helper →</a></p>'
    )

    # FAQ (uses actual picks data, no filler)
    top3_words = ', '.join(e['w'].upper() for e in picks[:3]) if picks else 'common words'
    faq = f'''<div class="faq">
  <h2 class="faq-title">Frequently asked questions</h2>
  <div class="faq-item open">
    <div class="faq-q"><span class="faq-q-text">How many 5-letter words start with {p}?</span><svg class="faq-chevron" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div>
    <div class="faq-a"><p>This list has {count} five-letter words starting with {p}. Wordle's answer pool is smaller — it uses only common everyday words.</p></div>
  </div>
  <div class="faq-item">
    <div class="faq-q"><span class="faq-q-text">What are the best {p} words for Wordle?</span><svg class="faq-chevron" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div>
    <div class="faq-a"><p>With {p} confirmed in positions 1–2, try {top3_words} — they cover common letters in positions 3–5.</p></div>
  </div>
  <div class="faq-item">
    <div class="faq-q"><span class="faq-q-text">Can I filter by word type?</span><svg class="faq-chevron" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div>
    <div class="faq-a"><p>Yes — use the filter buttons above the table to show only nouns, verbs, or adjectives. Every word has a definition.</p></div>
  </div>
</div>'''

    # Filter + FAQ JS (inline — content pages don't have an init slot)
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
        '<div class="pfx-wrap">\n'
        f'{picks_block}\n'
        f'{freq_block}\n'
        f'{filter_btns}\n'
        f'{table}\n'
        f'{group_html}\n'
        f'{back_link}\n'
        f'{wordle_link}\n'
        f'{faq}\n'
        f'{script}\n'
        '</div>'
    )


def render_page(prefix, words, mega_html, footer_cols_html):
    picks  = compute_best_picks(words)
    freq   = compute_position_freq(words)
    groups = group_by_type(words)

    meta    = render_meta(prefix, len(words), picks)
    style   = render_style()
    hero    = render_hero(prefix, len(words))
    content = render_content(prefix, words, picks, freq, groups)

    head_tmpl   = read(os.path.join(TMPL_DIR, 'head.html'))
    nav_tmpl    = read(os.path.join(TMPL_DIR, 'nav.html'))
    footer_tmpl = read(os.path.join(TMPL_DIR, 'footer.html'))

    stamp = f'<!-- build: {datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")} -->\n'

    head   = (head_tmpl
        .replace('{{META}}', meta)
        .replace('{{OG_IMAGE}}', '')
        .replace('{{HEAD_EXTRAS}}', '')
        .replace('{{STYLE}}', style))
    nav    = nav_tmpl.replace('{{MEGA_COLS}}', mega_html)
    footer = footer_tmpl.replace('{{FOOTER_COLS}}', footer_cols_html)

    breadcrumb = render_breadcrumb(prefix)

    return '\n'.join(filter(None, [
        stamp + head,
        '<body>',
        nav,
        breadcrumb,
        hero,
        content,
        footer,
        '</body>',
        '</html>',
    ]))


def redirect_lines_for(prefix):
    """Return the two _redirects lines for a prefix page (301 + 200 rewrite)."""
    slug = f'5-letter-words-starting-with-{prefix.lower()}'
    return [
        f'/{slug}.html    /{slug}/    301',
        f'/{slug}/    /{slug}.html    200',
    ]


def append_redirects(path, lines):
    """Append redirect lines that don't already exist in the file."""
    existing = open(path, encoding='utf-8').read() if os.path.exists(path) else ''
    new_lines = [ln for ln in lines if ln not in existing]
    if new_lines:
        with open(path, 'a', encoding='utf-8') as f:
            f.write('\n' + '\n'.join(new_lines))


def append_sitemap_entries(path, urls):
    """Insert sitemap <url> entries before the closing </urlset> tag."""
    if not os.path.exists(path):
        print(f'  warning: sitemap not found at {path}', file=sys.stderr)
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


def generate_all_prefixes(batch_len):
    """Yield all lowercase prefix strings of length batch_len."""
    for combo in product(string.ascii_lowercase, repeat=batch_len):
        yield ''.join(combo)


def main(batch_len, dry_run=False):
    print(f'Loading word data...')
    all_words = load_all_five_letter_words()
    print(f'  {len(all_words)} words loaded.')

    with open(TOOLS_JSON, encoding='utf-8') as f:
        tools_data = json.load(f)
    mega_html  = build_mega_cols(tools_data['mega'], '')
    fcols_html = build_footer_cols(tools_data['footer_cols'])

    generated          = []
    skipped            = 0
    redirect_lines_all = []
    sitemap_urls       = []

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
            output_path = os.path.join(SCRIPT_DIR, 'output', f'{slug}.html')
            if os.path.isdir(os.path.join(SCRIPT_DIR, 'output')):
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(page_html)

        generated.append(prefix)
        redirect_lines_all.extend(redirect_lines_for(prefix))
        sitemap_urls.append(url)

    if not dry_run and redirect_lines_all:
        append_redirects(REDIRECTS, redirect_lines_all)
        print(f'  _redirects updated ({len(redirect_lines_all)} lines added)')

    if not dry_run and sitemap_urls:
        append_sitemap_entries(SITEMAP, sitemap_urls)
        print(f'  sitemap.xml updated ({len(sitemap_urls)} entries added)')

    print(f'\nDone. {len(generated)} pages {"would be " if dry_run else ""}generated, '
          f'{skipped} combos skipped (< {MIN_WORDS} words).')
    if generated:
        sample = generated[:10]
        print(f'  Sample prefixes: {", ".join(sample)}{"..." if len(generated) > 10 else ""}')


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
    print('filter_by_prefix: OK')

    # has_enough_words
    assert has_enough_words(sample, 'st') is True
    assert has_enough_words(sample, 'cr') is False   # only 2, below min of 3
    print('has_enough_words: OK')

    # compute_best_picks
    picks = compute_best_picks(st_words, n=2)
    assert len(picks) == 2
    assert all('w' in p for p in picks)
    print('compute_best_picks: OK')

    # compute_position_freq
    freq = compute_position_freq(st_words, pos=2)
    assert len(freq) <= 5
    assert all(isinstance(letter, str) and isinstance(count, int) for letter, count in freq)
    print('compute_position_freq: OK')

    # group_by_type
    groups = group_by_type(st_words)
    assert 'Verbs' in groups
    assert 'Nouns' in groups
    assert 'stare' in [e['w'] for e in groups['Verbs']]
    assert all(groups[label] == sorted(groups[label], key=lambda e: e['w'])
               for label in groups), 'Groups not sorted alphabetically'
    print('group_by_type: OK')

    # edge cases
    assert filter_by_prefix([], 'st') == [], 'Empty list should return empty'
    assert compute_best_picks([], n=5) == [], 'Empty list should return empty picks'
    assert compute_position_freq([], pos=2) == [], 'Empty list should return empty freq'
    assert group_by_type([]) == {}, 'Empty list should return empty groups'
    print('edge cases: OK')

    # render_page smoke test (uses real templates + tools.json)
    with open(TOOLS_JSON, encoding='utf-8') as _f:
        _tools = json.load(_f)
    _mega   = build_mega_cols(_tools['mega'], '/5-letter-words-starting-with-st/')
    _fcols  = build_footer_cols(_tools['footer_cols'])
    _sample = [
        {'w': 'stare', 't': 'verb',      'd': 'to look fixedly'},
        {'w': 'stone', 't': 'noun',      'd': 'a rock'},
        {'w': 'strip', 't': 'verb',      'd': 'to remove'},
        {'w': 'stern', 't': 'adjective', 'd': 'serious and strict'},
    ]
    _html = render_page('st', _sample, _mega, _fcols)
    assert '<h1' in _html,             'Missing h1'
    assert 'STARE' in _html,           'Missing word STARE'
    assert 'pfx-picks' in _html,       'Missing picks callout'
    assert 'pfx-table' in _html,       'Missing word table'
    assert 'faq-q' in _html,          'Missing FAQ'
    assert '<footer' in _html,         'Missing footer'
    assert '</html>' in _html,         'Missing closing html tag'
    assert 'comprehensive' not in _html.lower(), 'Banned phrase found: comprehensive'
    assert "you've come to the right place" not in _html.lower(), 'Banned phrase found'
    print('render_page smoke test: OK')

    # redirect_lines_for
    _lines = redirect_lines_for('st')
    assert len(_lines) == 2, 'Expected 2 redirect lines'
    assert '/5-letter-words-starting-with-st.html    /5-letter-words-starting-with-st/    301' in _lines
    assert '/5-letter-words-starting-with-st/    /5-letter-words-starting-with-st.html    200' in _lines
    print('redirect_lines_for: OK')

    print('All tests passed.')


if __name__ == '__main__':
    if not os.path.isdir(DEPLOY_DIR):
        sys.exit(f'Error: wordineer-deploy/ not found at {DEPLOY_DIR}')

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

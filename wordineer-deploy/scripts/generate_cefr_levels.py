#!/usr/bin/env python3
"""
generate_cefr_levels.py — build 6 static ESL CEFR level pages (A1..C2) plus
per-level CSV downloads. Mirrors the letter-hub generator pattern.

Reads:
  template-deploy/data-src/esl/levels.json      (per-level word data)
  template-deploy/data-src/esl/review.csv       (approved def/example)
  template-deploy/data-src/esl/cefr-meta.json   (byline / license / versions)
  template-deploy/data-src/esl/chips.json       (POS chip constants)
  template-deploy/tools.json                    (mega + footer nav)

Writes:
  wordineer-deploy/esl-vocabulary-cefr-{a1..c2}.html
  wordineer-deploy/downloads/esl-cefr-{a1..c2}.csv
  wordineer-deploy/_redirects   (appends 6*2 rules if missing)
  template-deploy/sitemap.xml   (appends 6 URLs if missing)
  template-deploy/output/*.html (mirror copy)

Usage:
  python3 template-deploy/scripts/generate_cefr_levels.py
  python3 template-deploy/scripts/generate_cefr_levels.py --dry-run
"""

from __future__ import annotations

import argparse
import csv
import html
import json
import os
import sys
from datetime import datetime, timezone

# ── paths ──────────────────────────────────────────────────────────────────────
SCRIPT_DIR   = os.path.dirname(os.path.abspath(__file__))
TDEPLOY_DIR  = os.path.normpath(os.path.join(SCRIPT_DIR, '..'))
ROOT         = os.path.normpath(os.path.join(TDEPLOY_DIR, '..'))
DEPLOY_DIR   = os.path.join(ROOT, 'wordineer-deploy')
DATA_SRC     = os.path.join(TDEPLOY_DIR, 'data-src', 'esl')
TMPL_DIR     = os.path.join(TDEPLOY_DIR, 'template')
TOOLS_JSON   = os.path.join(TDEPLOY_DIR, 'tools.json')
OUTPUT_MIRROR = os.path.join(TDEPLOY_DIR, 'output')
REDIRECTS    = os.path.join(DEPLOY_DIR, '_redirects')
SITEMAP      = os.path.join(TDEPLOY_DIR, 'sitemap.xml')
DOWNLOADS_DIR = os.path.join(DEPLOY_DIR, 'downloads')

LEVELS = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2']
HIGH_FREQ_TOP_N = 12  # per level: default view = the N highest-Zipf words.
CANONICAL_BASE = 'https://wordineer.com'
HUB_URL = f'{CANONICAL_BASE}/esl-vocabulary-cefr/'

# ── import helpers from build.py ───────────────────────────────────────────────
sys.path.insert(0, TDEPLOY_DIR)
from build import build_mega_cols, build_footer_cols, read  # noqa: E402


# ── load data ──────────────────────────────────────────────────────────────────
def load_all():
    with open(os.path.join(DATA_SRC, 'levels.json'), encoding='utf-8') as f:
        levels_doc = json.load(f)
    with open(os.path.join(DATA_SRC, 'cefr-meta.json'), encoding='utf-8') as f:
        meta = json.load(f)
    with open(os.path.join(DATA_SRC, 'chips.json'), encoding='utf-8') as f:
        chips = json.load(f)
    review = {}
    with open(os.path.join(DATA_SRC, 'review.csv'), encoding='utf-8', newline='') as f:
        for row in csv.DictReader(f):
            key = (row['level'], row['word'].strip().lower())
            review[key] = row
    return levels_doc, meta, chips, review


# ── chip validator ─────────────────────────────────────────────────────────────
def validate_chips(chips, levels_doc):
    """Fail the build if any POS in the data isn't covered by a chip's `match`."""
    covered = set()
    for chip in chips['pos_chips']:
        for m in (chip.get('match') or []):
            covered.add(m.lower())
    unknown = set()
    for lvl in LEVELS:
        for e in levels_doc['levels'][lvl]['all']:
            pos = (e.get('pos') or '').strip().lower()
            if pos and pos not in covered:
                unknown.add(pos)
    if unknown:
        sys.exit(
            f'CHIP VALIDATOR FAILED: POS values in levels.json not covered by chips.json: '
            f'{sorted(unknown)}. Add them to chips.json or fix the data.'
        )
    # Validate labels are non-empty strings
    for chip in chips['pos_chips']:
        if not chip.get('label') or not chip.get('slug'):
            sys.exit(f'CHIP VALIDATOR FAILED: chip is missing label or slug: {chip}')


# ── render helpers ─────────────────────────────────────────────────────────────
def e(s):
    return html.escape(s or '', quote=True)


def slug_word(w):
    return ''.join(c if c.isalnum() else '-' for c in w.lower()).strip('-')


def pos_slug_for(pos, chips):
    p = (pos or '').strip().lower()
    for chip in chips['pos_chips']:
        for m in (chip.get('match') or []):
            if m.lower() == p:
                return chip['slug']
    return ''


def prev_next(level):
    i = LEVELS.index(level)
    prev = LEVELS[i - 1] if i > 0 else None
    nxt = LEVELS[i + 1] if i < len(LEVELS) - 1 else None
    return prev, nxt


def level_url(level):
    return f'{CANONICAL_BASE}/esl-vocabulary-cefr/{level.lower()}/'


def render_breadcrumb_schema(level):
    url = level_url(level)
    return f'''<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {{"@type":"ListItem","position":1,"name":"Wordineer","item":"https://wordineer.com/"}},
    {{"@type":"ListItem","position":2,"name":"Word Tools","item":"https://wordineer.com/word-tools/"}},
    {{"@type":"ListItem","position":3,"name":"ESL Vocabulary (CEFR)","item":"{HUB_URL}"}},
    {{"@type":"ListItem","position":4,"name":"{level}","item":"{url}"}}
  ]
}}
</script>'''


def render_learning_resource_schema(level, meta, word_count):
    url = level_url(level)
    lic = meta['license']['url']
    return f'''<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "LearningResource",
  "name": "{level} English Vocabulary List (CEFR)",
  "url": "{url}",
  "educationalLevel": "CEFR {level}",
  "learningResourceType": "vocabulary list",
  "inLanguage": "en",
  "isAccessibleForFree": true,
  "license": "{lic}",
  "author": {{"@type": "Person", "name": "{e(meta['author']['name'])}", "url": "{meta['author']['url']}"}},
  "publisher": {{"@type": "Organization", "name": "Wordineer", "url": "https://wordineer.com/"}},
  "about": "English as a Second Language vocabulary at CEFR level {level}",
  "numberOfItems": {word_count}
}}
</script>'''


def render_meta(level, word_count, meta):
    url = level_url(level)
    title = f'{level} English Vocabulary List (CEFR) — {word_count} Words | Wordineer'
    desc = (f'The {level} CEFR English vocabulary list: {word_count} words with '
            f'part of speech, IPA pronunciation, definitions, and example sentences. '
            f'Free CSV download.')
    bc = render_breadcrumb_schema(level)
    lr = render_learning_resource_schema(level, meta, word_count)
    return f'''{bc}
{lr}
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Wordineer">
<meta property="og:image" content="https://wordineer.com/og-image.png">'''


def render_style():
    return '''<style>
.esl-wrap { max-width: 920px; margin: 0 auto; padding: 28px 16px 48px; }
.esl-crumbs { font-size: 13px; color: var(--text-3, #6b7280); margin: 0 0 12px; }
.esl-crumbs a { color: inherit; text-decoration: none; }
.esl-crumbs a:hover { text-decoration: underline; }
.esl-intro { font-size: 16px; color: var(--text-2, #4b5563); margin: 0 0 24px; line-height: 1.55; }
.esl-chips { display: flex; gap: 8px; flex-wrap: wrap; margin: 0 0 20px; }
.esl-chip { padding: 6px 14px; border: 1.5px solid var(--border-2, #d1d5db); border-radius: 20px;
            background: #fff; font-size: 13px; cursor: pointer; font-family: inherit;
            color: var(--text-2, #4b5563); transition: all .15s; }
.esl-chip.active, .esl-chip:hover { background: var(--primary, #6366f1);
            border-color: var(--primary, #6366f1); color: #fff; }
.esl-cards { display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
             gap: 14px; margin: 0 0 36px; }
.esl-card { border: 1px solid var(--border-1, #e5e7eb); border-radius: 10px;
            padding: 16px; background: #fff; scroll-margin-top: 90px; }
.esl-card-head { display: flex; align-items: baseline; justify-content: space-between; gap: 8px; }
.esl-card-word { font-family: 'DM Serif Display', Georgia, serif; font-size: 22px; margin: 0; color: var(--text-1, #111827); }
.esl-badge { font-size: 11px; font-weight: 700; letter-spacing: .05em; padding: 3px 8px;
             border-radius: 999px; background: var(--primary-tint, #eef2ff); color: var(--primary, #6366f1); }
.esl-card-line { font-size: 13px; color: var(--text-3, #6b7280); margin: 4px 0 0; }
.esl-ipa { font-family: 'DM Sans', system-ui, sans-serif; }
.esl-card-def { font-size: 14px; color: var(--text-1, #111827); margin: 12px 0 8px; line-height: 1.5; }
.esl-card-ex { font-size: 13px; color: var(--text-2, #4b5563); margin: 0; font-style: italic; }
.esl-jump { display: flex; gap: 4px; flex-wrap: wrap; margin: 0 0 12px; font-size: 13px; }
.esl-jump a { padding: 2px 8px; border-radius: 4px; background: var(--surface-1, #f3f4f6);
             color: var(--text-2, #4b5563); text-decoration: none; }
.esl-jump a:hover { background: var(--primary, #6366f1); color: #fff; }
.esl-table { width: 100%; border-collapse: collapse; font-size: 14px; margin: 0 0 28px; }
.esl-table th { text-align: left; padding: 8px 12px; border-bottom: 2px solid var(--border-1, #e5e7eb);
                font-size: 12px; text-transform: uppercase; letter-spacing: .05em; color: var(--text-3, #6b7280); }
.esl-table td { padding: 10px 12px; border-bottom: 1px solid var(--border-1, #e5e7eb);
                color: var(--text-1, #111827); vertical-align: top; }
.esl-table a { color: var(--primary, #6366f1); text-decoration: none; }
.esl-table a:hover { text-decoration: underline; }
.esl-az-head { font-family: 'DM Serif Display', Georgia, serif; font-size: 24px; margin: 8px 0 12px; padding-top: 8px;
               border-top: 1px solid var(--border-1, #e5e7eb); }
.esl-downloads { border: 1px solid var(--border-1, #e5e7eb); border-radius: 10px; padding: 14px 18px;
                 margin: 0 0 28px; background: var(--surface-1, #f9fafb); }
.esl-downloads h3 { margin: 0 0 6px; font-size: 14px; text-transform: uppercase; letter-spacing: .04em; color: var(--text-3, #6b7280); }
.esl-downloads a { color: var(--primary, #6366f1); font-weight: 600; text-decoration: none; margin-right: 16px; }
.esl-trust { border: 1px solid var(--border-1, #e5e7eb); border-radius: 10px; padding: 14px 18px;
             margin: 32px 0 0; background: #fff; font-size: 13px; color: var(--text-2, #4b5563); }
.esl-trust p { margin: 0 0 6px; }
.esl-trust a { color: var(--primary, #6366f1); text-decoration: none; }
.esl-navpn { display: flex; justify-content: space-between; margin: 24px 0 0; font-size: 14px; }
.esl-navpn a { color: var(--primary, #6366f1); text-decoration: none; font-weight: 600; }
.esl-tools-link { margin: 12px 0 0; font-size: 14px; }
@media print {
  nav.nav, .mega, .esl-crumbs, .esl-chips, .esl-downloads, .esl-navpn, .esl-tools-link,
  .esl-trust, footer, .breadcrumb, .more-tools, .ad, .ad-b, .esl-jump { display: none !important; }
  .esl-wrap { max-width: 100%; padding: 0 12px; }
  body { font-size: 11px; color: #000; background: #fff; }
  h1 { font-size: 20px; margin: 0 0 6px; }
  .esl-intro { font-size: 12px; margin: 0 0 12px; }
  .esl-cards { display: grid; grid-template-columns: repeat(2, 1fr); gap: 8px; }
  .esl-card { border: 1px solid #ccc; border-radius: 0; padding: 8px 10px; break-inside: avoid; }
  .esl-card-word { font-size: 14px; }
  .esl-card-def, .esl-card-ex { font-size: 11px; }
  .esl-table { font-size: 11px; }
  .esl-table th, .esl-table td { padding: 4px 6px; }
  .esl-az-head { font-size: 14px; margin: 6px 0 4px; padding-top: 4px; }
  .esl-badge { color: #000; background: transparent; border: 1px solid #000; padding: 1px 4px; }
  a { color: #000; text-decoration: none; }
}
</style>'''


def render_breadcrumb_html(level):
    return f'''<div class="esl-wrap"><nav aria-label="Breadcrumb" class="esl-crumbs">
<a href="/">Wordineer</a> › <a href="/word-tools/">Word Tools</a> › <a href="/esl-vocabulary-cefr/">ESL Vocabulary (CEFR)</a> › {level}
</nav></div>'''


def render_hero(level, all_count, approved_count, meta):
    hub = HUB_URL + '#methodology'
    return f'''<div class="esl-wrap"><header>
<h1>{level} English Vocabulary List (CEFR)</h1>
<p class="esl-intro">This is the {level} vocabulary list from Wordineer’s CEFR ESL dataset ({all_count} words at this level). Each word has part of speech, American English IPA, a plain-language definition, and an example sentence — see the <a href="{hub}">source and methodology</a>.</p>
</header></div>'''


def render_chips(chips):
    default_slug = 'high-freq' if any(c['slug'] == 'high-freq' for c in chips['pos_chips']) else 'all'
    parts = ['<div class="esl-wrap"><div class="esl-chips" role="tablist" aria-label="Filter cards">']
    for c in chips['pos_chips']:
        active = c['slug'] == default_slug
        cls = 'esl-chip active' if active else 'esl-chip'
        parts.append(
            f'<button type="button" class="{cls}" data-pos="{e(c["slug"])}" '
            f'role="tab" aria-selected="{"true" if active else "false"}">{e(c["label"])}</button>'
        )
    parts.append('</div></div>')
    return ''.join(parts)


def render_cards(level, cards_data, chips, high_freq_words):
    if not cards_data:
        return ('<div class="esl-wrap"><p class="esl-intro" style="color:var(--text-3,#6b7280)">'
                'No approved cards yet at this level. See the full table below.</p></div>')
    out = ['<div class="esl-wrap"><section aria-label="Featured cards"><div class="esl-cards" id="esl-cards">']
    for card in cards_data:
        pos = card.get('pos') or ''
        pslug = pos_slug_for(pos, chips)
        ipa = card.get('ipa') or ''
        definition = card.get('_def_approved') or ''
        example = card.get('_ex_approved') or ''
        word = card['word']
        wid = f'word-{slug_word(word)}'
        hf_attr = ' data-highfreq="1"' if word.lower() in high_freq_words else ''
        out.append(
            f'<article class="esl-card" id="{wid}" data-pos="{e(pslug)}"{hf_attr}>'
            f'<div class="esl-card-head"><h3 class="esl-card-word">{e(word)}</h3>'
            f'<span class="esl-badge">{e(card["level"])}</span></div>'
            f'<p class="esl-card-line">{e(pos)}{" · " if pos and ipa else ""}'
            f'<span class="esl-ipa">{e(ipa)}</span></p>'
            f'<p class="esl-card-def">{e(definition)}</p>'
            f'<p class="esl-card-ex">“{e(example)}”</p>'
            f'</article>'
        )
    out.append('</div></section></div>')
    return ''.join(out)


def render_full_table(level, all_data, approved_words, chips, high_freq_words):
    """Alphabetical table with A-Z jump links; approved words link to their card anchor."""
    by_letter = {}
    for row in all_data:
        first = row['word'][0].lower()
        by_letter.setdefault(first, []).append(row)
    letters = sorted(by_letter.keys())

    jump = ''.join(f'<a href="#letter-{ltr}">{ltr.upper()}</a>' for ltr in letters)
    out = [
        '<div class="esl-wrap"><section aria-label="Full word list">',
        f'<h2 style="font-family:\'DM Serif Display\',Georgia,serif;font-size:26px;margin:24px 0 12px">All {level} words ({len(all_data)})</h2>',
        f'<div class="esl-jump">{jump}</div>',
    ]
    for ltr in letters:
        rows = sorted(by_letter[ltr], key=lambda r: r['word'].lower())
        out.append(f'<h3 class="esl-az-head" id="letter-{ltr}">{ltr.upper()}</h3>')
        out.append('<table class="esl-table"><thead><tr><th>Word</th><th>Part of speech</th></tr></thead><tbody>')
        for r in rows:
            word = r['word']
            pos = r.get('pos') or ''
            pslug = pos_slug_for(pos, chips)
            hf_attr = ' data-highfreq="1"' if word.lower() in high_freq_words else ''
            if word.lower() in approved_words:
                anchor = f'#word-{slug_word(word)}'
                cell = f'<a href="{anchor}">{e(word)}</a>'
            else:
                cell = e(word)
            out.append(f'<tr data-pos="{e(pslug)}"{hf_attr}><td>{cell}</td><td>{e(pos)}</td></tr>')
        out.append('</tbody></table>')
    out.append('</section></div>')
    return ''.join(out)


def render_downloads(level):
    lvl = level.lower()
    return f'''<div class="esl-wrap"><div class="esl-downloads">
<h3>Downloads</h3>
<a href="/downloads/esl-cefr-{lvl}.csv" download>CSV (imports into Anki, Quizlet)</a>
</div></div>'''


def render_prev_next_and_related(level):
    prev, nxt = prev_next(level)
    left = f'<a href="/esl-vocabulary-cefr/{prev.lower()}/">← {prev}</a>' if prev else '<span></span>'
    right = f'<a href="/esl-vocabulary-cefr/{nxt.lower()}/">{nxt} →</a>' if nxt else '<span></span>'
    return f'''<div class="esl-wrap">
<nav class="esl-navpn" aria-label="Level navigation">{left}{right}</nav>
<p class="esl-tools-link">Not sure of your level? Try the <a href="/cefr-level-checker/">CEFR level checker</a>.</p>
</div>'''


def render_trust_kit(meta):
    au = meta['author']
    lic = meta['license']
    versions = meta.get('sources', [])
    ver_line = ', '.join(s['name'] for s in versions) if versions else ''
    return f'''<div class="esl-wrap"><div class="esl-trust">
<p><strong>Built and maintained by <a href="{au['url']}">{e(au['name'])}</a>.</strong>
Last verified: {e(meta['last_verified'])} · Dataset v{e(meta['dataset_version'])} · Sources: {e(ver_line)}.</p>
<p>Cite: {e(meta['citation']['short'])} License: <a href="{lic['url']}">{e(lic['name'])}</a>.</p>
</div></div>'''


def render_faq(level, all_count, approved_count):
    return f'''<div class="esl-wrap"><section aria-labelledby="faq-h" style="margin-top:32px">
<h2 id="faq-h" style="font-family:'DM Serif Display',Georgia,serif;font-size:24px;margin:0 0 12px">Frequently asked</h2>
<div class="faq">
<div class="faq-item open"><div class="faq-q"><span class="faq-q-text">How many words are on the {level} list?</span><svg class="faq-chevron" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div><div class="faq-a"><p>{all_count} at this level. {approved_count} have a written definition and example sentence.</p></div></div>
<div class="faq-item"><div class="faq-q"><span class="faq-q-text">Can I import the CSV into Anki or Quizlet?</span><svg class="faq-chevron" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div><div class="faq-a"><p>Yes. Both accept comma-separated files with a header row. Columns are word, pos, level, ipa, definition, example.</p></div></div>
<div class="faq-item"><div class="faq-q"><span class="faq-q-text">Where do the pronunciations come from?</span><svg class="faq-chevron" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div><div class="faq-a"><p>American English IPA, transcribed from the CMU Pronouncing Dictionary. Stress marks: ˈ primary, ˌ secondary.</p></div></div>
</div></section></div>'''


def render_filter_script():
    # No fetch(). No DOM building. Pre-rendered rows filtered by data-pos / data-highfreq.
    return '''<script>
(function(){
  var scope = document;
  var chips = scope.querySelectorAll('.esl-chip');
  function matches(el, filter){
    if (filter === 'all') return true;
    if (filter === 'high-freq') return el.getAttribute('data-highfreq') === '1';
    return el.getAttribute('data-pos') === filter;
  }
  function apply(filter){
    chips.forEach(function(c){
      var on = c.getAttribute('data-pos') === filter;
      c.classList.toggle('active', on);
      c.setAttribute('aria-selected', on ? 'true' : 'false');
    });
    var cards = scope.querySelectorAll('.esl-card');
    var rows  = scope.querySelectorAll('.esl-table tbody tr');
    function show(el, ok){ el.style.display = ok ? '' : 'none'; }
    cards.forEach(function(el){ show(el, matches(el, filter)); });
    rows.forEach(function(el){ show(el, matches(el, filter)); });
  }
  chips.forEach(function(c){
    c.addEventListener('click', function(){ apply(c.getAttribute('data-pos') || 'all'); });
  });
  // Apply the default filter on load so cards render in the initial state (high-freq).
  var initial = document.querySelector('.esl-chip.active');
  apply(initial ? (initial.getAttribute('data-pos') || 'all') : 'all');
})();
</script>'''


def render_page(level, levels_doc, meta, chips, review, mega_html, footer_cols_html):
    lvl = levels_doc['levels'][level]
    all_data = list(lvl['all'])

    # Merge approved def/example onto each row (used by cards).
    for row in all_data:
        key = (level, row['word'].strip().lower())
        rv = review.get(key)
        if rv and rv['status'] == 'approved':
            row['_def_approved'] = rv['definition']
            row['_ex_approved'] = rv['example']
            row['_approved'] = True
        else:
            row['_def_approved'] = ''
            row['_ex_approved'] = ''
            row['_approved'] = False

    approved_words = {r['word'].lower() for r in all_data if r['_approved']}
    # Cards use levels.json 'cards' set, filtered to approved rows only.
    approved_lookup = {r['word'].lower(): r for r in all_data if r['_approved']}
    cards_data = []
    for c in lvl['cards']:
        m = approved_lookup.get(c['word'].lower())
        if m:
            cards_data.append(m)

    # Top-N by Zipf frequency — powers the default "High frequency" filter.
    by_zipf = sorted(all_data, key=lambda r: r.get('zipf', 0), reverse=True)
    high_freq_words = {r['word'].lower() for r in by_zipf[:HIGH_FREQ_TOP_N]}

    head_tmpl   = read(os.path.join(TMPL_DIR, 'head.html'))
    nav_tmpl    = read(os.path.join(TMPL_DIR, 'nav.html'))
    footer_tmpl = read(os.path.join(TMPL_DIR, 'footer.html'))

    meta_html  = render_meta(level, len(all_data), meta)
    style_html = render_style()
    stamp = f'<!-- build: {datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")} -->\n'

    head = (head_tmpl
            .replace('{{META}}', meta_html)
            .replace('{{OG_IMAGE}}', '')
            .replace('{{HEAD_EXTRAS}}', '')
            .replace('{{STYLE}}', style_html))
    nav = nav_tmpl.replace('{{MEGA_COLS}}', mega_html)
    footer = footer_tmpl.replace('{{FOOTER_COLS}}', footer_cols_html)

    body_parts = [
        render_breadcrumb_html(level),
        render_hero(level, len(all_data), len(approved_words), meta),
        render_chips(chips),
        render_cards(level, cards_data, chips, high_freq_words),
        render_downloads(level),
        render_full_table(level, all_data, approved_words, chips, high_freq_words),
        render_prev_next_and_related(level),
        render_faq(level, len(all_data), len(approved_words)),
        render_trust_kit(meta),
        render_filter_script(),
    ]

    return '\n'.join([
        stamp + head,
        '<body>',
        nav,
        *body_parts,
        footer,
        '</body>',
        '</html>',
    ])


def write_pdf(level, levels_doc, review, meta):
    """Two-column A4 PDF per level: cards then full alphabetical list.

    Uses ReportLab (pure-Python, no system deps). Written for correctness
    over polish — layout is intentionally minimal.
    """
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import cm
        from reportlab.lib.enums import TA_LEFT
        from reportlab.platypus import (BaseDocTemplate, Frame, PageTemplate,
                                         Paragraph, Spacer, PageBreak)
    except ImportError:
        return None

    os.makedirs(DOWNLOADS_DIR, exist_ok=True)
    path = os.path.join(DOWNLOADS_DIR, f'esl-cefr-{level.lower()}.pdf')

    lvl = levels_doc['levels'][level]
    all_data = list(lvl['all'])
    approved = {}
    for row in all_data:
        rv = review.get((level, row['word'].strip().lower()))
        if rv and rv['status'] == 'approved':
            approved[row['word'].lower()] = rv

    cards = [c for c in lvl['cards'] if c['word'].lower() in approved]

    page_w, page_h = A4
    margin = 1.5 * cm
    gutter = 0.6 * cm
    col_w = (page_w - 2 * margin - gutter) / 2
    top = page_h - margin
    bottom = margin + 0.9 * cm  # room for footer
    col_h = top - bottom
    left_frame = Frame(margin, bottom, col_w, col_h, id='col1', showBoundary=0,
                       leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    right_frame = Frame(margin + col_w + gutter, bottom, col_w, col_h, id='col2', showBoundary=0,
                        leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)

    def _footer(canvas, doc):
        canvas.saveState()
        canvas.setFont('Helvetica', 8)
        canvas.setFillGray(0.35)
        canvas.drawString(margin, margin * 0.4,
            f"Wordineer CEFR ESL Vocabulary — {level} · v{meta['dataset_version']} · "
            f"{meta['citation']['short']}")
        canvas.drawRightString(page_w - margin, margin * 0.4, f"Page {doc.page}")
        canvas.restoreState()

    doc = BaseDocTemplate(path, pagesize=A4,
                          leftMargin=margin, rightMargin=margin,
                          topMargin=margin, bottomMargin=margin,
                          title=f"{level} CEFR Vocabulary — Wordineer",
                          author=meta['author']['name'])
    doc.addPageTemplates([PageTemplate(id='two-col', frames=[left_frame, right_frame],
                                       onPage=_footer)])

    styles = getSampleStyleSheet()
    h1 = ParagraphStyle('h1', parent=styles['Heading1'], fontSize=18, spaceAfter=4, textColor='#111827')
    h2 = ParagraphStyle('h2', parent=styles['Heading2'], fontSize=13, spaceAfter=4, textColor='#111827')
    subtitle = ParagraphStyle('sub', parent=styles['BodyText'], fontSize=9, textColor='#6b7280', spaceAfter=10)
    card_word = ParagraphStyle('card_word', parent=styles['BodyText'], fontSize=11, spaceAfter=0, leading=13,
                               textColor='#111827', fontName='Helvetica-Bold')
    card_meta = ParagraphStyle('card_meta', parent=styles['BodyText'], fontSize=8, textColor='#6b7280', spaceAfter=2, leading=10)
    card_def = ParagraphStyle('card_def', parent=styles['BodyText'], fontSize=9, spaceAfter=2, leading=11)
    card_ex = ParagraphStyle('card_ex', parent=styles['BodyText'], fontSize=8, textColor='#4b5563', spaceAfter=8, leading=10, fontName='Helvetica-Oblique')
    list_row = ParagraphStyle('row', parent=styles['BodyText'], fontSize=9, leading=11, spaceAfter=0)

    story = []
    story.append(Paragraph(f"{level} English Vocabulary List (CEFR)", h1))
    story.append(Paragraph(
        f"{len(all_data)} words at CEFR {level}. Definitions and examples: Wordineer. "
        f"IPA: CMU Pronouncing Dictionary. Frequency: wordfreq (Zipf, en). "
        f"Source: <a href='https://wordineer.com/esl-vocabulary-cefr/{level.lower()}/'>wordineer.com/esl-vocabulary-cefr/{level.lower()}/</a>. "
        f"License: CC BY 4.0.", subtitle))

    if cards:
        story.append(Paragraph("Featured cards", h2))
        for c in cards:
            approved_row = approved[c['word'].lower()]
            story.append(Paragraph(f"{c['word']} <font size=8 color='#6b7280'>· {c.get('pos','')} · {c.get('ipa','')}</font>", card_word))
            story.append(Paragraph(approved_row['definition'], card_def))
            story.append(Paragraph(f"“{approved_row['example']}”", card_ex))

    story.append(Paragraph(f"All {level} words", h2))
    for row in sorted(all_data, key=lambda r: r['word'].lower()):
        story.append(Paragraph(f"<b>{row['word']}</b> <font size=8 color='#6b7280'>{row.get('pos','')}</font> "
                               f"<font size=8 color='#6b7280'>{row.get('ipa','')}</font>", list_row))

    doc.build(story)
    return path


def write_csv(level, levels_doc, review):
    """CSV per level: word, pos, level, ipa, definition, example (blank if not approved)."""
    os.makedirs(DOWNLOADS_DIR, exist_ok=True)
    lvl = levels_doc['levels'][level]
    path = os.path.join(DOWNLOADS_DIR, f'esl-cefr-{level.lower()}.csv')
    with open(path, 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
        w.writerow(['word', 'pos', 'level', 'ipa', 'definition', 'example'])
        for row in sorted(lvl['all'], key=lambda r: r['word'].lower()):
            key = (level, row['word'].strip().lower())
            rv = review.get(key)
            approved = rv and rv['status'] == 'approved'
            definition = rv['definition'] if approved else ''
            example = rv['example'] if approved else ''
            w.writerow([row['word'], row.get('pos', ''), row['level'], row.get('ipa', ''), definition, example])
    return path


def redirect_lines_for(level):
    slug = f'esl-vocabulary-cefr-{level.lower()}'
    pretty = f'/esl-vocabulary-cefr/{level.lower()}/'
    pretty_noslash = f'/esl-vocabulary-cefr/{level.lower()}'
    return [
        f'/{slug}.html    {pretty}    301',
        f'{pretty}    /{slug}.html    200',
        f'{pretty_noslash}    /{slug}.html    200',
    ]


def append_redirects(path, lines):
    existing = open(path, encoding='utf-8').read() if os.path.exists(path) else ''
    new_lines = [ln for ln in lines if ln not in existing]
    if new_lines:
        with open(path, 'a', encoding='utf-8') as f:
            f.write('\n' + '\n'.join(new_lines) + '\n')
    return len(new_lines)


def append_sitemap_entries(path, urls):
    if not os.path.exists(path):
        return 0
    content = open(path, encoding='utf-8').read()
    entries = []
    for url in urls:
        entry = f'  <url><loc>{url}</loc></url>'
        if entry not in content:
            entries.append(entry)
    if entries:
        content = content.replace('</urlset>', '\n'.join(entries) + '\n</urlset>')
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
    return len(entries)


def main(dry_run=False):
    levels_doc, meta, chips, review = load_all()
    validate_chips(chips, levels_doc)
    print('Chip validator: PASS')

    with open(TOOLS_JSON, encoding='utf-8') as f:
        tools_data = json.load(f)
    mega_html  = build_mega_cols(tools_data['mega'], '')
    fcols_html = build_footer_cols(tools_data['footer_cols'])

    redirect_lines_all = []
    sitemap_urls = []
    written = []
    csv_paths = []

    os.makedirs(OUTPUT_MIRROR, exist_ok=True)

    for level in LEVELS:
        page = render_page(level, levels_doc, meta, chips, review, mega_html, fcols_html)
        slug = f'esl-vocabulary-cefr-{level.lower()}'
        out_deploy = os.path.join(DEPLOY_DIR, f'{slug}.html')
        out_mirror = os.path.join(OUTPUT_MIRROR, f'{slug}.html')
        csv_path = None
        if not dry_run:
            with open(out_deploy, 'w', encoding='utf-8') as f:
                f.write(page)
            with open(out_mirror, 'w', encoding='utf-8') as f:
                f.write(page)
            csv_path = write_csv(level, levels_doc, review)
            pdf_path = write_pdf(level, levels_doc, review, meta)
        written.append((level, out_deploy, len(page)))
        csv_paths.append(csv_path)
        redirect_lines_all.extend(redirect_lines_for(level))
        sitemap_urls.append(level_url(level))

    added_r = append_redirects(REDIRECTS, redirect_lines_all) if not dry_run else 0
    added_s = append_sitemap_entries(SITEMAP, sitemap_urls) if not dry_run else 0

    print('\nGenerated pages:')
    for lvl, path, size in written:
        rel = os.path.relpath(path, ROOT)
        flag = '  ⚠ >400KB' if size > 400 * 1024 else ''
        print(f'  {lvl}: {rel}  ({size:,} bytes){flag}')
    print(f'\n_redirects: {added_r} new lines added')
    print(f'sitemap.xml: {added_s} new entries added')
    print(f'CSVs written: {sum(1 for p in csv_paths if p)}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    main(dry_run=args.dry_run)

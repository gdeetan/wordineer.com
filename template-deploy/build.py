#!/usr/bin/env python3
"""
Wordineer build script
----------------------
Reads tools.json + tools-src/*.html → writes finished pages to output/

Run: python3 build.py
"""

import html
import json
import os
import re
import shutil
import unicodedata
from datetime import datetime, timezone

ROOT      = os.path.dirname(os.path.abspath(__file__))
TMPL_DIR  = os.path.join(ROOT, 'template')
SRC_DIR   = os.path.join(ROOT, 'tools-src')
OUT_DIR   = os.path.join(ROOT, 'output')
DATA_FILE = os.path.join(ROOT, 'tools.json')
DEPLOY_DATA_DIR = os.path.join(ROOT, '..', 'wordineer-deploy', 'data')


# ── helpers ──────────────────────────────────────────────────────────────────

def read(path):
    with open(path, encoding='utf-8') as f:
        return f.read()

def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def copy_embed_pages():
    """Copy output/embed/ tree into wordineer-deploy/embed/."""
    embed_out = os.path.join(OUT_DIR, 'embed')
    if not os.path.isdir(embed_out):
        print('  no embed pages to copy')
        return
    deploy_dir = os.path.join(ROOT, '..', 'wordineer-deploy')
    if not os.path.isdir(deploy_dir):
        print('  warning → wordineer-deploy/ not found, skipping embed copy')
        return
    embed_deploy = os.path.join(deploy_dir, 'embed')
    if os.path.exists(embed_deploy):
        shutil.rmtree(embed_deploy)
    shutil.copytree(embed_out, embed_deploy)
    slugs = os.listdir(embed_out)
    print(f'  copied → embed/{" embed/".join(slugs)} into wordineer-deploy/embed/')


def build_embed_page(src_path, cfg, slots, slug):
    """Generate a minimal iframe-embeddable page for a tool."""
    # Extract <title> text from meta slot
    title_match = re.search(r'<title>(.*?)</title>', slots['meta'], re.DOTALL)
    title_text = title_match.group(1).strip() if title_match else 'Wordineer Tool'

    # Extract CSS version from head.html
    head_src = read(os.path.join(TMPL_DIR, 'head.html'))
    css_link_match = re.search(r'href="(/styles/global\.css[^"]*)"', head_src)
    css_href = css_link_match.group(1) if css_link_match else '/styles/global.css'

    # Extract tool-engine.js version from footer.html
    footer_src = read(os.path.join(TMPL_DIR, 'footer.html'))
    engine_match = re.search(r'src="(/scripts/tool-engine\.js[^"]*)"', footer_src)
    engine_src = engine_match.group(1) if engine_match else '/scripts/tool-engine.js'

    embed_style = (
        '<style>\n'
        'body { margin: 0; padding: 8px; box-sizing: border-box; }\n'
        '.embed-attrib { text-align: center; font-size: 0.75rem; color: #888; margin: 8px 0 4px; }\n'
        + (slots['style'] + '\n' if slots['style'] else '') +
        '</style>'
    )

    attribution = (
        '<p class="embed-attrib">\n'
        '  Powered by <a href="https://wordineer.com/?utm_source=embed&utm_medium=iframe"\n'
        '  target="_blank" rel="noopener">Wordineer</a>\n'
        '</p>'
    )

    auto_height = (
        '<script>\n'
        '(function () {\n'
        '  function send() {\n'
        '    parent.postMessage({ wordineerHeight: document.body.scrollHeight }, \'*\');\n'
        '  }\n'
        '  window.addEventListener(\'load\', send);\n'
        '  new ResizeObserver(send).observe(document.body);\n'
        '})();\n'
        '</script>'
    )

    # Strip affiliate blocks and ad sidebars from embed pages
    tool_html = slots['tool']

    def strip_div_by_class(html, class_name):
        """Remove divs with a specific class name using balanced depth tracking."""
        # Find opening <div class="...{class_name}...">
        match = re.search(rf'<div[^>]*class="[^"]*{re.escape(class_name)}[^"]*"[^>]*>', html)
        if not match:
            return html
        start = match.start()
        depth = 1
        pos = match.end()
        while depth > 0 and pos < len(html):
            close = html.find('</div>', pos)
            if close == -1:
                break
            open_next = html.find('<div', pos)
            if open_next != -1 and open_next < close:
                depth += 1
                pos = open_next + 4
            else:
                depth -= 1
                if depth == 0:
                    return html[:start] + html[close+6:]
                pos = close + 6
        return html

    tool_html = strip_div_by_class(tool_html, 'aff-nudge')
    tool_html = strip_div_by_class(tool_html, 'ad-sidebar')

    build_stamp = f'<!-- build: {datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")} -->\n'

    page = '\n'.join([
        build_stamp + '<!DOCTYPE html>',
        '<html lang="en">',
        '<head>',
        '<meta charset="UTF-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
        f'<title>{title_text}</title>',
        f'<link rel="stylesheet" href="{css_href}">',
        embed_style,
        '</head>',
        '<body>',
        tool_html,
        attribution,
        f'<script src="{engine_src}"></script>',
        auto_height,
        slots['init'],
        '</body>',
        '</html>',
    ])

    out_path = os.path.join(OUT_DIR, 'embed', slug, 'index.html')
    write(out_path, page)
    print(f'  built → embed/{slug}/index.html  [embed]')


def inject_page_data(cfg):
    """Read JSON specified in cfg['inject_data'] and return an inline <script> tag."""
    fname = cfg.get('inject_data')
    if not fname:
        return ''
    src_path = os.path.join(DEPLOY_DATA_DIR, fname)
    if not os.path.isfile(src_path):
        print(f'  warning → inject_data file not found: {src_path}')
        return ''
    with open(src_path, encoding='utf-8') as f:
        data = json.load(f)
    compact = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
    return f'<script>window._PAGE_DATA={compact};</script>'


def _esc(s):
    return html.escape(str(s)) if s is not None else ''


def canonical_path(path):
    """Return Wordineer's extensionless canonical path."""
    if not path or path == '/':
        return '/'
    if '?' in path or '#' in path:
        return path
    if re.search(r'\.[a-z0-9]{2,5}$', path, re.I):
        return path
    return '/' + path.strip('/')


def canonical_abs_url(url):
    if url == 'https://wordineer.com/':
        return url
    if url.startswith('https://wordineer.com/'):
        path = url.replace('https://wordineer.com', '', 1)
        return 'https://wordineer.com' + canonical_path(path)
    return url


def canonical_href(href):
    if href.startswith('/'):
        return canonical_path(href)
    if href.startswith('https://wordineer.com/'):
        return canonical_abs_url(href)
    return href


def normalize_internal_urls(page_html):
    """Strip internal trailing slashes from generated links and URL metadata."""
    def attr_fix(m):
        return f'{m.group(1)}="{canonical_href(m.group(2))}"'

    page_html = re.sub(
        r'\b(href|content|url|item|@id)="(https://wordineer\.com/[^"]+|/[^"]+)"',
        attr_fix,
        page_html,
    )

    def json_string_fix(m):
        return f'{m.group(1)}{canonical_abs_url(m.group(2))}"'

    page_html = re.sub(
        r'("(?:url|item|@id)"\s*:\s*")'
        r'(https://wordineer\.com/[^"]+)"',
        json_string_fix,
        page_html,
    )
    return page_html


def _render_five_letter_rows(data):
    parts = []
    for r in data:
        w = _esc(r.get('w', ''))
        vowels = _esc((r.get('vowels') or '').upper()) or '—'
        vc = r.get('vowel_count', '')
        uniq = r.get('unique_letters', False)
        bits = r.get('bits')
        bits_str = f'{bits:.2f}' if bits is not None else '—'
        uniq_html = '<span class="badge-unique">✓</span>' if uniq else ''
        parts.append(
            f'<tr>'
            f'<td><strong>{w.upper()}</strong></td>'
            f'<td><span class="vowel-chip">{vowels}</span></td>'
            f'<td>{vc}</td>'
            f'<td>{uniq_html}</td>'
            f'<td>{bits_str}</td>'
            f'</tr>'
        )
    return ''.join(parts)


_ETYM_ESSAY_OVERLAP = frozenset({
    'admiral', 'alcohol', 'algebra', 'assassin', 'atlas', 'awful', 'bedlam',
    'berserk', 'bonfire', 'boycott', 'bungalow', 'calculate', 'candidate',
    'carnival', 'cereal', 'chaos', 'chocolate', 'clue', 'coffee', 'companion',
    'cotton', 'curfew', 'disaster', 'dunce', 'glamour', 'gymnasium', 'hazard',
    'jungle', 'ketchup', 'magazine', 'marathon', 'mattress', 'meander',
    'mentor', 'money', 'mortgage', 'muscle', 'narcissism', 'nice', 'nightmare',
    'panic', 'paradise', 'quarantine', 'rival', 'robot', 'salary', 'sandwich',
    'school', 'shampoo', 'silhouette', 'silly', 'slogan', 'tantalize',
    'tragedy', 'travel', 'treacle', 'tycoon', 'villain', 'window', 'zero',
})


def _etym_slug(word):
    s = unicodedata.normalize('NFKD', word or '')
    s = ''.join(c for c in s if not unicodedata.combining(c))
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')


def _render_etymology_cards(data):
    parts = []
    for r in data:
        w = r.get('w', '')
        slug = _etym_slug(w)
        display_word = _esc(w[0].upper() + w[1:] if w else '')
        origin = _esc(r.get('origin') or r.get('category') or '')
        category = r.get('category') or 'Other'
        cat_cls = 'origin-' + category.replace(' ', '-')
        first_use = _esc(r.get('first_use', ''))
        root = _esc(r.get('root', ''))
        history = _esc(r.get('history', ''))
        search_blob = _esc(' '.join(filter(None, [
            w, r.get('origin', ''), category, r.get('root', ''),
            r.get('history', ''), ' '.join(r.get('modern_relatives') or []),
        ])).lower())
        relatives = r.get('modern_relatives', [])
        relatives_html = ''
        if relatives:
            chips = ''.join(f'<span class="rel-chip">{_esc(rw)}</span>' for rw in relatives)
            relatives_html = (
                f'<div class="etym-relatives-label">Modern relatives</div>'
                f'<div class="etym-relatives">{chips}</div>'
            )
        essay_html = ''
        if (w or '').lower() in _ETYM_ESSAY_OVERLAP:
            essay_html = (
                f'<p class="etym-essay-link"><a href="/word-etymology/#{slug}">'
                f'Longer story on the etymology essay</a></p>'
            )
        parts.append(
            f'<div class="etym-card" id="{_esc(slug)}" data-word="{_esc(w)}" '
            f'data-category="{_esc(category)}" data-search="{search_blob}">'
            f'<div class="etym-header">'
            f'<span class="etym-word">{display_word}</span>'
            f'<span class="etym-badge {cat_cls}">{origin}</span>'
            f'<span class="etym-date">{first_use}</span>'
            f'</div>'
            f'<div class="etym-root">Root: <strong>{root}</strong></div>'
            f'<div class="etym-history">{history}</div>'
            f'{relatives_html}'
            f'{essay_html}'
            f'</div>'
        )
    return ''.join(parts)


_SPEAK_SVG = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" width="16" height="16">'
    '<path d="M9.547 3.062A.75.75 0 0110 3.75v12.5a.75.75 0 01-1.21.59l-3.63-2.895H3.5A1.5 1.5 0 012 12.444'
    'V7.556A1.5 1.5 0 013.5 6.056h1.66l3.63-2.895a.75.75 0 01.757-.099zM13.78 6.22a.75.75 0 011.06 0A6.75 6.75'
    ' 0 0116.5 10a6.75 6.75 0 01-1.66 4.5.75.75 0 01-1.14-.976A5.25 5.25 0 0015 10a5.25 5.25 0 00-1.3-3.524'
    '.75.75 0 010-1.256z"/></svg>'
)


def _render_esl_cards(data):
    parts = []
    for r in data:
        w = r.get('w', '')
        cefr = _esc(r.get('cefr', ''))
        pos = _esc(r.get('pos', ''))
        ipa = _esc(r.get('ipa', ''))
        definition = _esc(r.get('def', ''))
        example = _esc(r.get('example', ''))
        w_attr = html.escape(w, quote=True)
        w_disp = _esc(w)
        parts.append(
            f'<div class="esl-card">'
            f'<span class="cefr-badge cefr-{cefr}">{cefr}</span>'
            f'<div class="eword">{w_disp}'
            f'<button class="speak-btn" data-word="{w_attr}" onclick="speakWord(event,this.dataset.word)"'
            f' title="Hear pronunciation" aria-label="Speak word">{_SPEAK_SVG}</button>'
            f'</div>'
            f'<div class="ipa">{ipa}</div>'
            f'<span class="pos">{pos}</span>'
            f'<div class="def">{definition}</div>'
            f'<div class="example">{example}</div>'
            f'</div>'
        )
    return ''.join(parts)


def inject_ssr_html(cfg, slots):
    """Render dataset as static HTML into pages that contain the <!-- SSR_ROWS --> placeholder."""
    url = cfg.get('url', '')
    fname = cfg.get('inject_data')
    if not fname:
        return slots

    all_slot_text = ''.join(slots.values())
    if '<!-- SSR_ROWS -->' not in all_slot_text:
        return slots

    src_path = os.path.join(DEPLOY_DATA_DIR, fname)
    if not os.path.isfile(src_path):
        return slots

    with open(src_path, encoding='utf-8') as f:
        data = json.load(f)

    if url == '/common-5-letter-words/':
        rendered = _render_five_letter_rows(data)
        slot_name = 'tool'
    elif url == '/etymology-100-common-words/':
        rendered = _render_etymology_cards(data)
        slot_name = 'content'
    elif url == '/esl-vocabulary-cefr/':
        rendered = _render_esl_cards(data)
        slot_name = 'tool'
    else:
        return slots

    slots[slot_name] = slots[slot_name].replace('<!-- SSR_ROWS -->', rendered)
    print(f'  ssr → {len(data)} items baked into {url}')
    return slots


def copy_data_assets():
    """Mirror deploy JSON assets into output/ so template previews can fetch /data/*.json."""
    if not os.path.isdir(DEPLOY_DATA_DIR):
        print('  warning → deploy data directory not found, skipping JSON asset copy')
        return
    out_data_dir = os.path.join(OUT_DIR, 'data')
    os.makedirs(out_data_dir, exist_ok=True)
    copied = 0
    for fname in sorted(os.listdir(DEPLOY_DATA_DIR)):
        if not (fname.endswith('.json') or fname == 'etymology-100.csv'):
            continue
        shutil.copy2(os.path.join(DEPLOY_DATA_DIR, fname), os.path.join(out_data_dir, fname))
        copied += 1
    print(f'  copied → {copied} data file(s) into output/data/')

def copy_script_assets():
    """Mirror page-local JS assets into output/scripts/ for preview builds."""
    scripts_dir = os.path.join(ROOT, 'scripts')
    if not os.path.isdir(scripts_dir):
        print('  warning → template scripts directory not found, skipping script asset copy')
        return
    out_scripts_dir = os.path.join(OUT_DIR, 'scripts')
    os.makedirs(out_scripts_dir, exist_ok=True)
    copied = 0
    for fname in sorted(os.listdir(scripts_dir)):
        if not fname.endswith('.js'):
            continue
        shutil.copy2(os.path.join(scripts_dir, fname), os.path.join(out_scripts_dir, fname))
        copied += 1
    print(f'  copied → {copied} JS script file(s) into output/scripts/')

def copy_redirects():
    """Copy _redirects into output/ so deploy only needs to copy output/."""
    src = os.path.join(ROOT, '_redirects')
    if not os.path.isfile(src):
        print('  warning → template-deploy/_redirects not found, skipping')
        return
    shutil.copy2(src, os.path.join(OUT_DIR, '_redirects'))
    print('  copied → _redirects into output/')


def copy_static_pages():
    """Copy standalone static pages (404.html, etc.) into output/ and wordineer-deploy/."""
    deploy_dir = os.path.join(ROOT, '..', 'wordineer-deploy')
    static_files = ['404.html']
    for fname in static_files:
        src = os.path.join(ROOT, fname)
        if not os.path.isfile(src):
            print(f'  warning → template-deploy/{fname} not found, skipping')
            continue
        shutil.copy2(src, os.path.join(OUT_DIR, fname))
        if os.path.isdir(deploy_dir):
            shutil.copy2(src, os.path.join(deploy_dir, fname))
        print(f'  copied → {fname} into output/ + wordineer-deploy/')


def build_sitemap(data):
    """Generate sitemap.xml from tools.json live entries and write to output/ and wordineer-deploy/."""
    today = datetime.now(timezone.utc).strftime('%Y-%m-%d')

    seen = set()
    entries = []

    def add(href, priority, changefreq):
        href = canonical_path(href)
        if not href or href in seen:
            return
        seen.add(href)
        loc = 'https://wordineer.com/' if href == '/' else 'https://wordineer.com' + href
        entries.append((loc, priority, changefreq))

    add('/', 1.0, 'weekly')

    for cat in data.get('mega', []):
        add(cat.get('view_all_href', ''), 0.8, 'weekly')
        for tool in cat.get('tools', []):
            if tool.get('status') in ('planned', 'standby', 'coming_soon'):
                continue
            add(tool.get('href', ''), 0.7, 'weekly')

    for tool in data.get('more_word_tools', []):
        if tool.get('status') in ('planned', 'standby', 'coming_soon'):
            continue
        add(tool.get('href', ''), 0.7, 'weekly')

    for tool in data.get('more_name_tools', []):
        if tool.get('status') in ('planned', 'standby', 'coming_soon'):
            continue
        add(tool.get('href', ''), 0.7, 'weekly')

    for tool in data.get('other_tools', []):
        if tool.get('status') in ('planned', 'standby', 'coming_soon'):
            continue
        add(tool.get('href', ''), 0.6, 'monthly')

    for col in data.get('footer_cols', []):
        for tool in col.get('links', []):
            if tool.get('status') in ('planned', 'standby', 'coming_soon'):
                continue
            add(tool.get('href', ''), 0.5, 'monthly')

    for tool in data.get('vocabulary_tools', []):
        if tool.get('status') in ('planned', 'standby', 'coming_soon'):
            continue
        add(tool.get('href', ''), 0.7, 'weekly')

    for tool in data.get('spelling_bee_tools', []):
        if tool.get('status') in ('planned', 'standby', 'coming_soon'):
            continue
        add(tool.get('href', ''), 0.7, 'weekly')

    for tool in data.get('sight_words_tools', []):
        if tool.get('status') in ('planned', 'standby', 'coming_soon'):
            continue
        add(tool.get('href', ''), 0.7, 'weekly')

    for tool in data.get('words_ending_pages', []):
        if tool.get('status') in ('planned', 'standby', 'coming_soon'):
            continue
        add(tool.get('href', ''), 0.6, 'monthly')

    # Merge in generator-produced pages (e.g. from generate_prefix_pages.py).
    # These live only on disk in wordineer-deploy/ and aren't in tools.json.
    # Without this, every build.py run would strip them from the sitemap.
    deploy_dir = os.path.join(ROOT, '..', 'wordineer-deploy')
    if os.path.isdir(deploy_dir):
        gen_pat = re.compile(r'^(\d+-letter-words-starting-with-[a-z]+)\.html$')
        generator_added = 0
        for fname in sorted(os.listdir(deploy_dir)):
            m = gen_pat.match(fname)
            if not m:
                continue
            href = '/' + m.group(1)
            before = len(seen)
            add(href, 0.5, 'monthly')
            if len(seen) > before:
                generator_added += 1
    else:
        generator_added = 0

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for loc, priority, changefreq in entries:
        lines += [
            '  <url>',
            f'    <loc>{loc}</loc>',
            f'    <lastmod>{today}</lastmod>',
            f'    <changefreq>{changefreq}</changefreq>',
            f'    <priority>{priority:.1f}</priority>',
            '  </url>',
        ]
    lines.append('</urlset>')
    xml = '\n'.join(lines)

    out_path = os.path.join(OUT_DIR, 'sitemap.xml')
    write(out_path, xml)

    # Also refresh template-deploy/sitemap.xml so the generator's next run
    # sees the current full set (it merges with this file).
    tpl_path = os.path.join(ROOT, 'sitemap.xml')
    write(tpl_path, xml)

    suffix = f' (+{generator_added} generator-added)' if generator_added else ''
    deploy_path = os.path.join(ROOT, '..', 'wordineer-deploy', 'sitemap.xml')
    if os.path.isdir(os.path.dirname(deploy_path)):
        write(deploy_path, xml)
        print(f'  sitemap.xml → {len(entries)} URLs{suffix} (output/ + wordineer-deploy/ + template-deploy/)')
    else:
        print(f'  sitemap.xml → {len(entries)} URLs{suffix} (output/ + template-deploy/)')

def slot(src, name):
    """Pull the content between <!-- SLOT:name --> and <!-- /SLOT:name -->."""
    m = re.search(
        r'<!-- SLOT:' + re.escape(name) + r' -->(.*?)<!-- /SLOT:' + re.escape(name) + r' -->',
        src, re.DOTALL
    )
    return m.group(1).strip() if m else ''

def config(src):
    """Pull the JSON block from <!-- CONFIG ... --> at the top of a tool-src file."""
    m = re.search(r'<!-- CONFIG\s*(.*?)\s*-->', src, re.DOTALL)
    return json.loads(m.group(1)) if m else {}

def strip_inline_nav_init(init_html):
    """Remove page-local hamburger wiring. Shared runtime owns nav behavior now."""
    if not init_html:
        return ''
    return re.sub(
        r'\n?\(function bindWordineerMenu\(\)\{[\s\S]*?\}\)\(\);\s*',
        '\n',
        init_html,
        count=1,
    )


def format_name_generator_label(raw_label):
    if not raw_label:
        return ''
    if raw_label.lower() == 'random name':
        return 'Random Name Generator'
    if 'generator' in raw_label.lower():
        return raw_label
    return raw_label + ' Generator'


def is_name_generator_page(active_url):
    return (
        active_url == '/random-name-generator/'
        or bool(re.fullmatch(r'/random(?:-[a-z0-9]+)+-name-generator/', active_url))
    )


def label_from_name_generator_url(active_url):
    slug = active_url.strip('/')
    if not slug.endswith('-name-generator'):
        return ''
    if slug == 'random-name-generator':
        return 'Random Name Generator'
    middle = slug[len('random-'):-len('-name-generator')]
    words = [part.capitalize() for part in middle.split('-') if part]
    return 'Random ' + ' '.join(words) + ' Name Generator'


def find_name_generator_label(data, active_url):
    for tool in data.get('name_generator_tools', []):
        if tool.get('href') == active_url:
            return format_name_generator_label(tool.get('name', ''))

    return label_from_name_generator_url(active_url)


def build_software_application_schema(cfg, slots):
    """Auto-generate SoftwareApplication schema for tool pages."""
    if '"SoftwareApplication"' in slots.get('meta', ''):
        return ''  # page already has it (e.g. wordle-helper)

    active_url = cfg.get('url', '')
    if not active_url:
        return ''

    title_match = re.search(r'<title>(.*?)</title>', slots.get('meta', ''), re.DOTALL)
    if not title_match:
        return ''
    name = re.sub(r'\s*[|—–-]\s*Wordineer.*$', '', title_match.group(1).strip())

    desc_match = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', slots.get('meta', ''))
    description = desc_match.group(1) if desc_match else ''

    url_lower = active_url.lower()
    game_keywords = ('wordle', 'game', 'dice', 'coin', 'wheel', 'trivia',
                     'charade', 'truth-or-dare', 'never-have-i', 'dad-joke',
                     'rock-paper', 'scattergories', 'catchphrase', 'pictionary',
                     'magic-8')
    category = 'GameApplication' if any(k in url_lower for k in game_keywords) else 'UtilityApplication'

    schema = {
        "@context": "https://schema.org",
        "@type": "SoftwareApplication",
        "name": name,
        "url": f'https://wordineer.com{active_url}',
        "applicationCategory": category,
        "operatingSystem": "Web",
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
        "publisher": {"@id": "https://wordineer.com/#organization"},
    }
    if description:
        schema["description"] = description

    return (
        '<script type="application/ld+json">\n'
        + json.dumps(schema, ensure_ascii=False, indent=2)
        + '\n</script>'
    )


def build_breadcrumb(active_url, data, cfg):
    # Breadcrumbs are now handled per-page in tools-src (hero slot + meta slot schema)
    return '', ''
    if not is_name_generator_page(active_url):
        return '', ''

    current_label = find_name_generator_label(data, active_url)
    if not current_label:
        return '', ''

    current_label_html = html.escape(current_label)
    breadcrumb_html = '\n'.join([
        '<nav class="breadcrumb" aria-label="Breadcrumb">',
        '  <div class="breadcrumb-inner">',
        '    <a href="/">Home</a>',
        '    <span class="breadcrumb-sep" aria-hidden="true">›</span>',
        '    <a href="/name-generators/">Name Generators</a>',
        '    <span class="breadcrumb-sep" aria-hidden="true">›</span>',
        f'    <span aria-current="page">{current_label_html}</span>',
        '  </div>',
        '</nav>',
    ])

    breadcrumb_schema = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": 1,
                "name": "Home",
                "item": "https://wordineer.com/",
            },
            {
                "@type": "ListItem",
                "position": 2,
                "name": "Name Generators",
                "item": "https://wordineer.com/name-generators/",
            },
            {
                "@type": "ListItem",
                "position": 3,
                "name": current_label,
                "item": f'https://wordineer.com{active_url}',
            },
        ],
    }
    breadcrumb_schema_html = (
        '<script type="application/ld+json">\n'
        + json.dumps(breadcrumb_schema, ensure_ascii=False, indent=2)
        + '\n</script>'
    )
    return breadcrumb_html, breadcrumb_schema_html


# ── HTML generators (driven entirely by tools.json) ──────────────────────────

def build_mega_cols(mega, active_url):
    cols = []
    for cat in mega:
        links = []
        for t in cat['tools']:
            cls = 'mega-link active' if t['href'] == active_url else 'mega-link'
            links.append(f'      <a class="{cls}" href="{t["href"]}">{t["text"]}</a>')
        if cat.get('view_all_href'):
            links.append(f'      <a class="mega-link mega-link--view-all" href="{cat["view_all_href"]}">View all →</a>')
        cols.append(
            '    <div class="mega-col">\n'
            f'      <div class="mega-cat">{cat["cat"]}</div>\n'
            + '\n'.join(links) + '\n'
            '    </div>'
        )
    return '\n'.join(cols)


def build_tools_grid(more_word_tools, active_url):
    # Show up to 6 word tools, always excluding the current page.
    # If a "More Name Gen Tools" card exists, pin it as the last visible card.
    items = [t for t in more_word_tools if t['href'] != active_url]
    more_name_card = next((t for t in items if t.get('name') == 'More Name Gen Tools'), None)
    if more_name_card:
        lead_items = [t for t in items if t is not more_name_card][:5]
        items = lead_items + [more_name_card]
    else:
        items = items[:6]
    rows = []
    for t in items:
        badge = ' <span class="new-badge">new</span>' if t.get('new') else ''
        rows.append(
            f'      <a class="tool-item" href="{t["href"]}">'
            f'<div class="tool-icon" style="background:{t["icon_bg"]}">'
            f'<svg viewBox="0 0 13 13" fill="none">{t["icon_path"]}</svg></div>'
            f'<div class="tool-name">{t["name"]}{badge}</div>'
            f'<div class="tool-desc">{t["desc"]}</div></a>'
        )
    return '\n'.join(rows)


def build_other_grid(other_tools):
    cols = []
    for cat in other_tools:
        links = ''.join(
            f'<a class="other-link" href="{l["href"]}">{l["text"]}</a>'
            for l in cat['links']
        )
        if cat.get('view_all_href'):
            links += f'<a class="other-link other-link--view-all" href="{cat["view_all_href"]}">View all →</a>'
        cols.append(
            '      <div class="other-cat">'
            f'<div class="other-cat-title">'
            f'<svg viewBox="0 0 13 13" fill="none">{cat["icon_path"]}</svg>'
            f'{cat["cat"]}</div>'
            f'{links}</div>'
        )
    return '\n'.join(cols)


def build_footer_cols(footer_cols):
    cols = []
    for col in footer_cols:
        links_html = ''
        for l in col['links']:
            links_html += f'<a class="footer-link" href="{l["href"]}">{l["text"]}</a>'
        if col.get('view_all_href'):
            links_html += f'<a class="footer-link footer-link--view-all" href="{col["view_all_href"]}">View all →</a>'
        cols.append(
            f'      <div><div class="footer-col-title">{col["title"]}</div>'
            f'{links_html}</div>'
        )
    return '\n'.join(cols)


def build_related_html(url, data):
    related = data.get('page_meta', {}).get(url, {}).get('related', [])
    if not related:
        return ''
    links = '\n'.join(
        f'    <a class="related-link" href="{r["href"]}">{r["text"]}</a>'
        for r in related
    )
    return (
        '\n<div class="related-tools">'
        '\n  <h3 class="related-title">Related tools &amp; guides</h3>'
        '\n  <div class="related-links">\n'
        + links +
        '\n  </div>'
        '\n</div>\n'
    )


def build_og_image_tag(url, data, meta_slot):
    if 'og:image' in meta_slot:
        return ''  # page already declares its own og:image
    og = data.get('page_meta', {}).get(url, {}).get('ogImage') or '/og-default.jpg'
    return f'<meta property="og:image" content="https://wordineer.com{og}">'


def build_twitter_tags(meta_slot):
    if 'name="twitter:card"' in meta_slot or "name='twitter:card'" in meta_slot:
        return ''

    def content_for(pattern):
        m = re.search(pattern, meta_slot, re.DOTALL)
        return m.group(1).strip() if m else ''

    title = content_for(r'<meta\s+property="og:title"\s+content="([^"]*)"')
    if not title:
        title = content_for(r'<title>(.*?)</title>')
    title = re.sub(r'\s*\|\s*Wordineer\s*$', '', title)
    desc = content_for(r'<meta\s+property="og:description"\s+content="([^"]*)"')
    if not desc:
        desc = content_for(r'<meta\s+name="description"\s+content="([^"]*)"')

    tags = ['<meta name="twitter:card" content="summary_large_image">']
    if title:
        tags.append(f'<meta name="twitter:title" content="{html.escape(title, quote=True)}">')
    if desc:
        tags.append(f'<meta name="twitter:description" content="{html.escape(desc, quote=True)}">')
    return '\n'.join(tags)


# ── page builder ─────────────────────────────────────────────────────────────

def normalize_canonical(page_html):
    """Strip trailing slashes from canonical hrefs. Cloudflare Pages serves pages at
    non-trailing-slash URLs (200); trailing-slash variants 308-redirect to them.
    Exception: homepage https://wordineer.com/ keeps its slash."""
    def fix(m):
        href = m.group(1)
        stripped = href.rstrip('/')
        # stripped would be bare origin (e.g. "https://wordineer.com") for homepage — skip
        if href.endswith('/') and '/' in stripped.split('://', 1)[-1]:
            href = stripped
        return f'<link rel="canonical" href="{href}">'
    return re.sub(r'<link rel="canonical" href="([^"]+)">', fix, page_html)


def build_page(src_path, data):
    src = read(src_path)
    cfg = config(src)

    page_type   = cfg.get('type', 'tool')   # 'tool' or 'content'
    active_url  = cfg.get('url', '').rstrip('/') or '/'
    output_file = cfg.get('output', os.path.basename(src_path))

    # Extract slots (missing slots return empty string — safe for both page types)
    slots = {name: slot(src, name)
             for name in ('meta', 'style', 'hero', 'tool', 'ad_b',
                          'explainer', 'faq', 'who', 'init', 'content')}
    slots['init'] = strip_inline_nav_init(slots['init'])
    slots = inject_ssr_html(cfg, slots)

    # Build shared nav/footer blocks from tools.json
    mega_html        = build_mega_cols(data['mega'], active_url)
    footer_cols_html = build_footer_cols(data['footer_cols'])
    breadcrumb_html, breadcrumb_schema_html = build_breadcrumb(active_url, data, cfg)

    # Related tools and og:image from page_meta
    related_html  = build_related_html(active_url, data)
    og_image_tag  = build_og_image_tag(active_url, data, slots['meta'])
    twitter_tags  = build_twitter_tags(slots['meta'])
    build_stamp   = f'<!-- build: {datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")} -->\n'
    page_data_tag = inject_page_data(cfg)

    # Load shared template fragments
    head   = read(os.path.join(TMPL_DIR, 'head.html'))
    nav    = read(os.path.join(TMPL_DIR, 'nav.html'))
    footer = read(os.path.join(TMPL_DIR, 'footer.html'))

    # Inject slots into shared templates
    sw_schema_html = build_software_application_schema(cfg, slots) if page_type == 'tool' else ''
    extras = '\n'.join(filter(None, [breadcrumb_schema_html, sw_schema_html]))

    head   = (head
        .replace('{{META}}', slots['meta'])
        .replace('{{OG_IMAGE}}', '\n'.join(filter(None, [og_image_tag, twitter_tags])))
        .replace('{{HEAD_EXTRAS}}', extras)
        .replace('{{STYLE}}', slots['style']))
    nav    = nav.replace('{{MEGA_COLS}}', mega_html)
    footer = footer.replace('{{FOOTER_COLS}}', footer_cols_html)

    if page_type == 'standalone':
        # Verbatim page — only the CONFIG comment is stripped and nav/footer placeholders injected.
        # Everything else (head, scripts) is kept exactly as written in tools-src.
        page = re.sub(r'<!-- CONFIG.*?-->\n?', '', src, flags=re.DOTALL)
        page = page.replace('{{MEGA_COLS}}', mega_html)
        page = page.replace('{{FOOTER_COLS}}', footer_cols_html)
        page = build_stamp + page

    elif page_type == 'content':
        # Simple layout: head → nav → hero → (data injection) → content → related → footer
        wrapped_related = f'<div class="content-wrap">{related_html}</div>' if related_html.strip() else ''
        page = '\n'.join(filter(None, [
            build_stamp + head,
            '<body>',
            nav,
            slots['hero'],
            page_data_tag,
            slots['content'],
            wrapped_related,
            footer,
            '</body>',
            '</html>',
        ]))

    else:
        # Full tool layout: head → nav → hero → tool → ads → grids → footer → init
        more_tools = read(os.path.join(TMPL_DIR, 'more-tools.html'))
        tools_key = cfg.get('more_tools_key', 'more_word_tools')
        tools_grid_html = build_tools_grid(data[tools_key], active_url)
        other_grid_html = build_other_grid(data['other_tools'])
        more_tools = (more_tools
            .replace('{{MORE_TOOLS_TITLE}}', cfg.get('more_tools_title', 'More word tools'))
            .replace('{{MORE_TOOLS_SUBTITLE}}', cfg.get('more_tools_subtitle', 'Every word generator you need, all free'))
            .replace('{{TOOLS_GRID}}', tools_grid_html)
            .replace('{{OTHER_GRID}}', other_grid_html)
            .replace('{{EXPLAINER}}',  slots['explainer'])
            .replace('{{FAQ}}',        slots['faq'])
            .replace('{{WHO}}',        slots['who'])
            .replace('{{RELATED_TOOLS}}', related_html))

        page = '\n'.join(filter(None, [
            build_stamp + head,
            '<body>',
            nav,
            breadcrumb_html,
            slots['hero'],
            slots['tool'],
            slots['ad_b'],
            more_tools,
            footer,
            page_data_tag,
            slots['init'],
            '</body>',
            '</html>',
        ]))

    page = normalize_internal_urls(normalize_canonical(page))
    out_path = os.path.join(OUT_DIR, output_file)
    write(out_path, page)
    print(f'  built → {output_file}  [{page_type}]')

    # Also generate embed page if flagged (standalone pages have no slots, skip)
    if cfg.get('embed') and page_type != 'standalone':
        embed_slug = cfg.get('embed_slug') or output_file.replace('.html', '')
        build_embed_page(src_path, cfg, slots, embed_slug)


# ── pre-build validation ──────────────────────────────────────────────────────

def validate_configs(src_files):
    """Fail fast if two source files would write to the same output filename."""
    seen = {}  # output_file -> src_path
    errors = []
    for src_path in src_files:
        src = read(src_path)
        cfg = config(src)
        output_file = cfg.get('output', os.path.basename(src_path))
        if output_file in seen:
            errors.append(
                f'  DUPLICATE OUTPUT: "{output_file}" claimed by both '
                f'{os.path.basename(seen[output_file])} and {os.path.basename(src_path)}'
            )
        else:
            seen[output_file] = src_path
    if errors:
        print('BUILD ABORTED — duplicate output filenames detected:')
        for e in errors:
            print(e)
        raise SystemExit(1)


# ── main ─────────────────────────────────────────────────────────────────────

def main():
    # Deploy: copy from template-deploy/output/ (include subfolders such as
    # output/random-words-starting-with/), never from tools-src/.
    data = json.loads(read(DATA_FILE))
    # Clean stale HTML files from a previous build before writing fresh output.
    # Preserve externally-generated pages (e.g. from generate_prefix_pages.py) —
    # they have no tools-src source, so this loop would otherwise wipe them.
    _gen_pat = re.compile(r'^\d+-letter-words-starting-with-[a-z]+\.html$')
    if os.path.isdir(OUT_DIR):
        for f in os.listdir(OUT_DIR):
            if f.endswith('.html') and not _gen_pat.match(f):
                os.remove(os.path.join(OUT_DIR, f))
    os.makedirs(OUT_DIR, exist_ok=True)

    src_files = sorted(
        os.path.join(SRC_DIR, f)
        for f in os.listdir(SRC_DIR) if f.endswith('.html')
    )
    if not src_files:
        print('No tool source files found in tools-src/')
        return

    # Skip draft files, files with no CONFIG block, and externally-generated pages
    def _cfg(p): return config(read(p))
    src_files = [p for p in src_files
                 if _cfg(p)  # has a CONFIG block
                 and not _cfg(p).get('draft')
                 and _cfg(p).get('type') != 'generated']

    validate_configs(src_files)

    print(f'Building {len(src_files)} page(s)...')
    for src_path in src_files:
        build_page(src_path, data)
    copy_data_assets()
    copy_script_assets()
    copy_redirects()
    copy_static_pages()
    copy_embed_pages()
    build_sitemap(data)

    print(f'\nDone! Output is in:  {OUT_DIR}/')
    print('Deploy: copy from template-deploy/output/ (include subfolders e.g. random-words-starting-with/)')
    print('  cp output/*.html output/_redirects ../wordineer-deploy/')
    print('  cp -R output/random-words-starting-with ../wordineer-deploy/')

if __name__ == '__main__':
    main()

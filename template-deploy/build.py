#!/usr/bin/env python3
"""
Wordineer build script
----------------------
Reads tools.json + tools-src/*.html → writes finished pages to output/

Run: python3 build.py
"""

import os, re, json, shutil

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

def copy_data_assets():
    """Mirror deploy JSON assets into output/ so template previews can fetch /data/*.json."""
    if not os.path.isdir(DEPLOY_DATA_DIR):
        print('  warning → deploy data directory not found, skipping JSON asset copy')
        return
    out_data_dir = os.path.join(OUT_DIR, 'data')
    os.makedirs(out_data_dir, exist_ok=True)
    copied = 0
    for fname in sorted(os.listdir(DEPLOY_DATA_DIR)):
        if not fname.endswith('.json'):
            continue
        shutil.copy2(os.path.join(DEPLOY_DATA_DIR, fname), os.path.join(out_data_dir, fname))
        copied += 1
    print(f'  copied → {copied} JSON data file(s) into output/data/')

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


# ── HTML generators (driven entirely by tools.json) ──────────────────────────

def build_mega_cols(mega, active_url):
    cols = []
    for cat in mega:
        links = []
        for t in cat['tools']:
            cls = 'mega-link active' if t['href'] == active_url else 'mega-link'
            links.append(f'      <a class="{cls}" href="{t["href"]}">{t["text"]}</a>')
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
        links = ''.join(
            f'<a class="footer-link" href="{l["href"]}">{l["text"]}</a>'
            for l in col['links']
        )
        cols.append(
            f'      <div><div class="footer-col-title">{col["title"]}</div>'
            f'{links}</div>'
        )
    return '\n'.join(cols)


# ── page builder ─────────────────────────────────────────────────────────────

def build_page(src_path, data):
    src = read(src_path)
    cfg = config(src)

    page_type   = cfg.get('type', 'tool')   # 'tool' or 'content'
    active_url  = cfg.get('url', '')
    output_file = cfg.get('output', os.path.basename(src_path))

    # Extract slots (missing slots return empty string — safe for both page types)
    slots = {name: slot(src, name)
             for name in ('meta', 'style', 'hero', 'tool', 'ad_b',
                          'explainer', 'faq', 'who', 'init', 'content')}
    slots['init'] = strip_inline_nav_init(slots['init'])

    # Build shared nav/footer blocks from tools.json
    mega_html        = build_mega_cols(data['mega'], active_url)
    footer_cols_html = build_footer_cols(data['footer_cols'])

    # Load shared template fragments
    head   = read(os.path.join(TMPL_DIR, 'head.html'))
    nav    = read(os.path.join(TMPL_DIR, 'nav.html'))
    footer = read(os.path.join(TMPL_DIR, 'footer.html'))

    # Inject slots into shared templates
    head   = head.replace('{{META}}', slots['meta']).replace('{{STYLE}}', slots['style'])
    nav    = nav.replace('{{MEGA_COLS}}', mega_html)
    footer = footer.replace('{{FOOTER_COLS}}', footer_cols_html)

    if page_type == 'content':
        # Simple layout: head → nav → hero → content → footer
        page = '\n'.join([
            head,
            '<body>',
            nav,
            slots['hero'],
            slots['content'],
            footer,
            '</body>',
            '</html>',
        ])

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
            .replace('{{WHO}}',        slots['who']))

        page = '\n'.join([
            head,
            '<body>',
            nav,
            slots['hero'],
            slots['tool'],
            slots['ad_b'],
            more_tools,
            footer,
            slots['init'],
            '</body>',
            '</html>',
        ])

    out_path = os.path.join(OUT_DIR, output_file)
    write(out_path, page)
    print(f'  built → {output_file}  [{page_type}]')


# ── main ─────────────────────────────────────────────────────────────────────

def main():
    data = json.loads(read(DATA_FILE))
    os.makedirs(OUT_DIR, exist_ok=True)

    src_files = sorted(f for f in os.listdir(SRC_DIR) if f.endswith('.html'))
    if not src_files:
        print('No tool source files found in tools-src/')
        return

    print(f'Building {len(src_files)} page(s)...')
    for fname in src_files:
        build_page(os.path.join(SRC_DIR, fname), data)
    copy_data_assets()

    print(f'\nDone! Output is in:  {OUT_DIR}/')
    print('Copy the contents of output/ to wordineer-deploy/ when ready to deploy.')

if __name__ == '__main__':
    main()

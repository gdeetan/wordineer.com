# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

# Project: Wordineer Tool Site

Wordineer is a static HTML/CSS/JS site (no framework) hosted on Cloudflare Pages at wordineer.com. It provides SEO-focused generator tools (words, names, numbers). Performance and simplicity are the top priorities — do not introduce frameworks or replace working systems.

**Before every change:** state how you will verify it works, then verify before calling it done.

---

# Architecture

## Folder layout

```
template-deploy/          ← build system (edit here)
  tools-src/              ← source HTML files with CONFIG + SLOT syntax
  template/               ← shared fragments (head.html, nav.html, footer.html, more-tools.html)
  tools.json              ← central registry: mega-menu, tools grids, footer links
  build.py                ← assembles tools-src/ → output/
  output/                 ← generated pages (intermediate, not committed)

wordineer-deploy/         ← production files (deployed to Cloudflare Pages)
  scripts/tool-engine.js  ← main tool engine (WORDINEER IIFE); tool-engine.min.js is the minified copy
  styles/global.css        ← shared styles
  data/                   ← JSON datasets
  _headers                ← Cloudflare cache rules (scripts/styles: 1yr immutable; data: 7d)
  _redirects              ← canonical URL redirects (www→non-www, .html→trailing-slash)

template-deploy-backup/   ← archived snapshot, do not edit
```

**Never edit `wordineer-deploy/` directly.** It is build output. Always edit `template-deploy/tools-src/` and rebuild.

---

## Build & deploy

```bash
# 1. Build
cd template-deploy && python3 build.py

# 2. Copy output to deploy folder
cp template-deploy/output/*.html wordineer-deploy/

# 3. Preview locally (fetch() requires a server — file:// won't work)
cd wordineer-deploy && python3 -m http.server 8080

# 4. Push → Cloudflare Pages auto-deploys in ~20 seconds
```

---

## tool-src page structure

Each file in `tools-src/` starts with a `<!-- CONFIG ... -->` block (JSON), followed by named `<!-- SLOT:name --> ... <!-- /SLOT:name -->` blocks:

```html
<!-- CONFIG
{ "url": "/tool-name.html", "output": "tool-name.html", "type": "tool" }
-->
```

`type` is `"tool"` (full layout with nav/grids/ads/footer) or `"content"` (simple layout: no tool/ads/grids).

**Slots for `type: tool`:**

| Slot | Purpose |
|------|---------|
| `meta` | `<title>`, `<meta>`, canonical, JSON-LD schema |
| `style` | page-scoped `<style>` block |
| `hero` | above-the-fold heading/intro |
| `tool` | interactive tool UI |
| `ad_b` | ad placement below tool |
| `explainer` | how-it-works section |
| `faq` | FAQ accordion |
| `who` | "who uses this" section |
| `init` | inline `<script>` at bottom of `<body>` |

**Slots for `type: content`:** `meta`, `style`, `hero`, `content`

Navigation, mega-menu, tools grids, and footer are injected automatically from `tools.json` — never hardcode them in tool-src files.

---

## Adding a new tool

1. Create `template-deploy/tools-src/[tool-name].html` following an existing tool-src as a pattern.
2. Add the tool to all four sections of `tools.json` where relevant: `mega`, `more_word_tools`, `other_tools`, `footer_cols`.
3. If the tool needs a clean URL (`/tool-name/` instead of `/tool-name.html`), add rewrite rules to `wordineer-deploy/_redirects`.
4. Build and copy output, then preview locally before deploying.

---

## Data files (`wordineer-deploy/data/`)

- `words.json` — primary word dataset; also embedded as SEED in `tool-engine.js` for instant first render
- `words_expanded.json` — extended word set
- `dictionary.json` — definitions lookup
- `names.json` — name generator dataset
- `sentences.json` — sentence generator dataset

**words.json entry schema:**
```json
{ "w": "Luminary", "t": "noun", "d": "a person who inspires others", "diff": "medium", "borrowed": false }
```
- `t`: `"noun"` | `"adjective"` | `"verb"` | `"adverb"`
- `diff`: `"easy"` | `"medium"` | `"hard"`
- `d`: keep under ~100 chars for clean display

---

## PageSpeed rules

- Keep above-the-fold tool UI working immediately — no fetch() at initial render.
- Load `words.json`, `names.json`, `dictionary.json` after page load / browser idle / first user action.
- Trigger deferred loads early on: Generate button, filter changes, Enter, Space.
- No load-time autofocus/select — causes forced reflow in Lighthouse.
- Ads, analytics, and consent scripts must be deferred.
- **Bump `?v=N` query string** whenever changing `tool-engine.js` or `global.css` (scripts/styles are cached for 1 year immutable via `_headers`).
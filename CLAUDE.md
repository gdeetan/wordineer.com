# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

# Project: Wordineer Tool Site

Wordineer is a static HTML/CSS/JS site (no framework) hosted on Cloudflare Pages at wordineer.com. It provides SEO-focused generator tools (words, names, numbers). Performance and simplicity are the top priorities — do not introduce frameworks or replace working systems.

**Before every change:** state how you will verify it works, then verify before calling it done.

**Do not touch working features when creating or updating pages.** When adding a new page or modifying an existing one, only add/change what the task requires. Do not "improve," refactor, or rewrite functionality that already works — especially interactive components like the FAQ accordion, mobile menu, saved-items panel, copy-all button, keyboard shortcuts, or the tool-engine init flow. If a working feature is accidentally broken (e.g., the FAQ toggle JS is removed from the `init` slot, or the required HTML structure is changed), it wastes a full debug + fix + rebuild + redeploy cycle. When in doubt, copy the exact pattern from an existing working page (see the FAQ pattern below for one example) and leave the rest alone.

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
  api.html                  ← NOT an active page; ignore it
```

**Never edit `wordineer-deploy/` directly.** It is build output. Always edit `template-deploy/tools-src/` and rebuild.

**Every change to page content or structure must start in `template-deploy/`.** After any edit to `tools-src/`, `tools.json`, or template fragments, run `build.py` and copy output to `wordineer-deploy/`. Never skip this step — edits made only in `wordineer-deploy/` will be overwritten on the next build and are not tracked as source.

---

## Build & deploy

**Always upload / copy from `template-deploy/output/`.** That folder is the built site. Do not upload pages out of `tools-src/` (source slots) or try to dump the entire `wordineer-deploy/` HTML tree through GitHub’s web UI — GitHub truncates a single folder at 1,000 files. Subfolders under `output/` (for example `template-deploy/output/random-words-starting-with/`) stay well under that cap and are the right path to commit and push.

```bash
# 1. Build
cd template-deploy && python3 build.py

# 2. Copy from template-deploy/output/ (never from tools-src/)
cp template-deploy/output/*.html wordineer-deploy/
cp template-deploy/output/_redirects wordineer-deploy/
# include output subfolders (letter hubs, etc.)
cp -R template-deploy/output/random-words-starting-with wordineer-deploy/

# 3. Preview locally (fetch() requires a server — file:// won't work)
cd wordineer-deploy && python3 -m http.server 8080

# 4. Commit the files you copied from output/, then push
#    git add template-deploy/output/random-words-starting-with wordineer-deploy/random-words-starting-with
#    git commit && git push
#    Cloudflare Pages auto-deploys in ~20 seconds
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

## FAQ pattern — REQUIRED

Every tool page must use the **JS-driven div pattern** for the `faq` slot. **Never use native `<details>/<summary>`** — the global CSS rule `.faq-a{display:none}` conflicts with it and breaks all FAQ accordions.

```html
<!-- SLOT:faq -->
<div class="faq">
  <h2 class="faq-title">Frequently asked questions</h2>
  <div class="faq-item open">
    <div class="faq-q"><span class="faq-q-text">Question?</span><svg class="faq-chevron" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div>
    <div class="faq-a"><p>Answer.</p></div>
  </div>
  <div class="faq-item">
    <div class="faq-q"><span class="faq-q-text">Question 2?</span><svg class="faq-chevron" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div>
    <div class="faq-a"><p>Answer 2.</p></div>
  </div>
</div>
<!-- /SLOT:faq -->
```

**Do NOT add local FAQ toggle JS to the `init` slot.** `tool-engine.js` already binds `.faq-q` clicks via `initFaq()` (auto-runs on DOMContentLoaded and inside `WORDINEER.init`). Adding a second binder in the page causes double-binding — the click toggles `.open` twice per click, net-zero change, and the accordion silently stops working. If you copy from an old file that has this line, delete it.

Rules: first item gets class `open`; every `.faq-q` needs the chevron SVG; answers wrap in `<p>` inside `.faq-a`.

---

## Adding a new tool

1. Create `template-deploy/tools-src/[tool-name].html` following an existing tool-src as a pattern.
2. Add the tool to all four sections of `tools.json` where relevant: `mega`, `more_word_tools`, `other_tools`, `footer_cols`.
3. If the tool needs a clean URL (`/tool-name/` instead of `/tool-name.html`), add rewrite rules to `wordineer-deploy/_redirects`.
4. Build and copy output, then preview locally before deploying.

## Mega-menu, footer, and other_tools column limits

Each category column in the hamburger mega-menu (`mega`), the footer (`footer_cols`), and the body "Other tools" grid (`other_tools`) must have **at most 4 tool links + one "View all" link**. Do not add a fifth tool link — keep only the most representative tools for the category and rely on the hub page (via "View all") for the full list. Apply this rule whenever adding tools to `tools.json`.

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

---

## Writing style — avoid AI slop

Based on Pew Research (Aug 2026) on how AI detectors and readers spot AI-written text. Apply to page copy, FAQs, explainers, meta descriptions, and anchor text.

Source: [Pew Research — How Much of the Internet Is Written With AI?](https://www.pewresearch.org/data-labs/2026/08/20/how-much-of-the-internet-is-written-with-ai/)

**Cut these 4 tells:**
1. **Em dashes (—)** — use commas, periods, or parentheses instead.
2. **Oxford commas** — vary list punctuation; don't default to them.
3. **AI vocabulary** — do not use: *additionally, align with, boasts, bolstered, crucial, delve, emphasizing, enduring, enhance, essential, fostering, garner, highlight, interplay, intricate, key, landscape, meticulous, perfectly, pivotal, showcase, significant, tapestry, testament, underscore, valuable, vibrant.*
4. **Negative parallelism** — kill "not just X, it's Y" and "not merely A but B" constructions.

**Write human:**
- Concrete over abstract (name the thing, number, or person — no "landscapes" or "tapestries").
- Uneven rhythm. Short sentences. Then longer, messier ones. Break parallelism on purpose.
- Plain verbs: *use* not *utilize*, *help* not *enhance*, *show* not *showcase*.
- No throat-clearing intros ("In today's fast-paced world…"). No restated summary conclusions.
- Anchor text: name the concrete destination in plain, specific words — the exact tool or page — not generic "learn more" phrasing.
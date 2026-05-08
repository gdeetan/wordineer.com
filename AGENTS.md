# Repository Guidelines

## Project Structure & Module Organization

This repository is a static Wordineer site. The production-ready site lives in `wordineer-deploy/`, with top-level HTML pages, `styles/global.css`, `scripts/tool-engine.js`, `data/*.json`, `fonts/`, `robots.txt`, `sitemap.xml`, `_headers`, and `_redirects`. Page templates and generated outputs live in `template-deploy/`: edit shared fragments in `template-deploy/template/`, source page bodies in `template-deploy/tools-src/`, and tool metadata in `template-deploy/tools.json`. `template-deploy-backup/` is archival; do not use it as the primary edit target unless intentionally restoring old content. Keep screenshots and research artifacts outside deploy folders unless they are meant to ship.

## Build, Test, and Development Commands

There is no package manager setup for this repo. Use the static server commands below from the directory being tested:

```bash
cd wordineer-deploy
python3 -m http.server 8080
```

Open `http://localhost:8080`. Do not test by opening HTML files directly; `fetch('/data/words.json')` requires an HTTP server. To regenerate template output, run:

```bash
cd template-deploy
python3 build.py
```

Then review the generated files before copying or deploying.

## Coding Style & Naming Conventions

Use plain HTML, CSS, JavaScript, and JSON. Keep indentation at 2 spaces in HTML/CSS/JS and preserve existing formatting in large generated pages. Name tool pages with lowercase hyphenated slugs, such as `random-name-generator.html`. Keep shared behavior in `scripts/tool-engine.js`; avoid duplicating generator logic inline across pages. Data files should remain valid JSON with stable keys expected by the scripts.

## Testing Guidelines

No automated test framework is configured. Manually test changed pages through the local HTTP server. Verify generator buttons, data loading, navigation links, responsive layout, and console errors. For data edits, validate JSON before committing:

```bash
python3 -m json.tool wordineer-deploy/data/words.json >/dev/null
```

## Commit & Pull Request Guidelines

Git history is not available in this checkout, so use short imperative commit messages, for example `Add pictionary word generator` or `Fix word data loading`. Pull requests should describe the changed pages or data files, list manual test URLs, and include screenshots for visible UI changes. Link related issues when available.

## Deployment & Configuration Notes

The site is suitable for Cloudflare Pages with no build command and `/` as the output directory when deploying `wordineer-deploy/`. Preserve `_headers`, `_redirects`, `robots.txt`, and `sitemap.xml` when preparing releases. Avoid committing `.DS_Store` files or temporary generated backups.

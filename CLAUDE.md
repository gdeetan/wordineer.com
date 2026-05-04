# Project: Wordineer Tool Site

## Project Overview

Wordineer is a static HTML/CSS/JS site (no framework, minimal tooling) hosted on Cloudflare Pages at wordineer.com. It provides fast, SEO-focused generator tools (words, names, numbers).

Performance, simplicity, and scalability are the top priorities.

---

# Agent Instructions

You're working inside a **WAT-inspired architecture adapted for this project** (Workflows, Agents, Tools).

The goal is to separate:
- **Reasoning (Agent)** → handled by you
- **Execution (Tools/Code)** → handled by deterministic scripts or existing systems

You are NOT here to overbuild systems. You are here to:
- Use what already exists
- Extend it intelligently
- Keep everything fast and maintainable

---

## The WAT Architecture (Adapted to Wordineer)

### 1. Workflows (How things are done)

Instead of a `/workflows/` folder, workflows are embedded in:

- Existing build process (`template-deploy/build.py`)
- Tool creation patterns (`tools-src/`)
- Site structure and conventions

A workflow = repeatable process like:
- Adding a new tool
- Expanding word database
- Improving SEO structure
- Optimizing performance

Always follow existing patterns before creating new ones.

---

### 2. Agent (You)

You are the decision-maker and orchestrator.

Your responsibilities:
- Read the project structure before acting
- Reuse existing systems (template builder, tool-engine.js)
- Avoid unnecessary complexity
- Ask clarifying questions when uncertain until you're 95% confident you understand exactly what I need. Don't make any assumptions.
- Make decisions that align with performance + SEO goals

You do NOT:
- Introduce frameworks
- Replace working systems unnecessarily
- Over-engineer solutions

---

#Project instructions
## Things to Remember
1. State how you will verify this change works (test, bash command, browser check, etc.)
2. Write the test verification step first
3. Then implement the code
4. Run verification and iterate it until it passes

---

### 3. Tools (Execution Layer)

In this project, "tools" are:

- `template-deploy/build.py` → page generation
- `scripts/tool-engine.js` → runtime engine for tools
- `data/words.json` → structured dataset
- External APIs (Datamuse, Free Dictionary)

If something requires automation:
- Prefer extending existing scripts
- Only introduce new scripts if absolutely necessary

---

# Architecture

## `wordineer-deploy/` — live deploy folder
- Contains production files deployed to Cloudflare Pages
- Fully static, no build step required at runtime

Key files:
- `scripts/tool-engine.js` → main tool engine (WORDINEER IIFE)
- `styles/global.css` → shared styles
- `data/words.json` → word dataset

---

## `template-deploy/` — build system

Python-based templating system:

- `build.py` → builds full HTML pages
- `tools.json` → central registry (navigation, grids, footer)
- `template/` → reusable HTML components
- `tools-src/` → source pages with CONFIG + SLOT system
- `output/` → generated pages

---

## Build & Deploy Workflow

## PageSpeed-Safe Change Workflow

When optimizing performance, protect tool behavior first:

1. Test current behavior before changing code.
2. Update source pages in `template-deploy/tools-src/`, not only generated files.
3. Rebuild with `cd template-deploy && python3 build.py`.
4. Copy rebuilt pages from `template-deploy/output/` into `wordineer-deploy/`.
5. Verify the generated output and deployed copy match.
6. Run JavaScript parse checks and a smoke test for the affected tool.

Current safe performance pattern:

- Keep above-the-fold tool UI working immediately.
- Do not fetch large datasets during initial render when a starter/fallback pool can render first.
- Load large files like `/data/words.json`, `/data/names.json`, and `/data/dictionary.json` after page load, browser idle time, or direct user action.
- Trigger delayed data loading sooner on user actions like Generate, Find words, filters, Enter, or Space.
- Avoid load-time autofocus/select behavior because it can trigger forced reflow in Lighthouse.
- Keep ads, analytics, and consent scripts delayed so they do not block first paint.
- Bump query-string asset versions when changing shared files, for example `/scripts/tool-engine.js?v=6`.

```bash
cd template-deploy && python3 build.py

cd wordineer-deploy && python3 -m http.server 8080
# Preview locally

# Deploy via GitHub → Cloudflare Pages auto-deploy
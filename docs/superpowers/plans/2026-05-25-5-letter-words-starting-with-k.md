# 5 Letter Words Starting With K Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a new `5-letter-words-starting-with-k` source page and matching dataset that follows the existing letter-page series while expanding the list to 120 curated K words with definitions.

**Architecture:** Reuse the established `5-letter-words-starting-with-*` template structure from the adjacent pages, swap in K-specific metadata and prose, and provide a dedicated `five-letter-words-k.json` payload for the page's lazy-load path. Keep the filter UI, card rendering, breadcrumb, FAQ, and A-Z navigation unchanged so the new page plugs into the existing series without JS changes.

**Tech Stack:** Static HTML, inline CSS/JS, JSON data, Python build script

---

### Task 1: Add the K page source

**Files:**
- Create: `template-deploy/tools-src/5-letter-words-starting-with-k.html`

- [ ] **Step 1: Base the new source page on an existing letter page**

Use `template-deploy/tools-src/5-letter-words-starting-with-j.html` as the structural model because it already targets a higher-count letter page in the same series.

- [ ] **Step 2: Replace letter-specific metadata and prose**

Update the title, description, schema, breadcrumb, hero, A-Z active state, prose sections, and FAQ answers so they consistently describe K words and the final curated count of 120.

- [ ] **Step 3: Replace the inline seed data and JSON fetch path**

Embed the K seed list in the inline `SEED` array and update the lazy-load fetch target to `/data/five-letter-words-k.json`.

### Task 2: Add the K dataset

**Files:**
- Create: `wordineer-deploy/data/five-letter-words-k.json`

- [ ] **Step 1: Build the 120-entry dataset**

Store each entry with the existing object shape:

```json
{"w":"Koala","t":"noun","d":"an Australian tree-dwelling marsupial that feeds mainly on eucalyptus leaves","diff":"easy"}
```

- [ ] **Step 2: Keep definitions and tags consistent**

Use concise definitions, one of the existing type labels (`noun`, `verb`, `adjective`, `adverb`), and difficulty labels (`easy`, `medium`, `hard`) that match the existing series.

### Task 3: Build and verify

**Files:**
- Verify: `template-deploy/build.py`

- [ ] **Step 1: Run the template build**

Run: `cd template-deploy && python3 build.py`

Expected: build completes successfully and generates the new K page output.

- [ ] **Step 2: Validate the new JSON payload**

Run: `python3 -m json.tool wordineer-deploy/data/five-letter-words-k.json >/dev/null`

Expected: command exits `0` with no output.

- [ ] **Step 3: Spot-check the generated page content**

Confirm the generated page contains the `Starting With K` breadcrumb, `5 Letter Words Starting With K` heading, and references the K dataset path.

# 5 Letter Words Starting With M Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a new `5-letter-words-starting-with-m` source page and matching dataset that follows the existing letter-page series with 120-130 curated M words and definitions.

**Architecture:** Reuse the established `5-letter-words-starting-with-*` page structure, swap in M-specific metadata and prose, and provide a dedicated `five-letter-words-m.json` dataset for the page's lazy-load path. Keep the shared filter UI, breadcrumb, FAQ, card rendering, and A-Z navigation unchanged so the new page fits the existing series cleanly.

**Tech Stack:** Static HTML, inline CSS/JS, JSON data, Python build script

---

### Task 1: Add the M page source

**Files:**
- Create: `template-deploy/tools-src/5-letter-words-starting-with-m.html`

- [ ] **Step 1: Base the source file on an existing completed letter page**

Use `template-deploy/tools-src/5-letter-words-starting-with-l.html` as the structural model because it already matches the current series pattern and 120+ word target.

- [ ] **Step 2: Replace the letter-specific metadata and body copy**

Update the title, meta description, schema, breadcrumb, hero copy, A-Z active state, prose sections, and FAQ answers so they consistently describe M words and the final curated count.

- [ ] **Step 3: Replace the inline seed list and fetch path**

Embed an M seed array in the inline script and update the lazy-load fetch target to `/data/five-letter-words-m.json`.

### Task 2: Add the M dataset

**Files:**
- Create: `wordineer-deploy/data/five-letter-words-m.json`

- [ ] **Step 1: Build the curated data file**

Store each entry with the existing object shape:

```json
{"w":"Magic","t":"noun","d":"the power of apparently influencing events by mysterious forces","diff":"easy"}
```

- [ ] **Step 2: Keep tags and definitions consistent**

Use concise dictionary-style definitions, one of the current type labels (`noun`, `verb`, `adjective`, `adverb`), and the current difficulty labels (`easy`, `medium`, `hard`).

### Task 3: Build and verify

**Files:**
- Verify: `template-deploy/build.py`

- [ ] **Step 1: Run the template build**

Run: `cd template-deploy && python3 build.py`

Expected: the build succeeds and generates `5-letter-words-starting-with-m.html`.

- [ ] **Step 2: Validate the new JSON payload**

Run: `python3 -m json.tool wordineer-deploy/data/five-letter-words-m.json >/dev/null`

Expected: command exits `0` with no output.

- [ ] **Step 3: Spot-check the generated output**

Confirm the generated page contains the `Starting With M` breadcrumb, the `5 Letter Words Starting With M` heading, and the `/data/five-letter-words-m.json` fetch path.

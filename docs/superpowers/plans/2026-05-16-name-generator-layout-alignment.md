# Name Generator Layout Alignment Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Align all name-generator templates to the shared filter/results/saved layout pattern and add a `Regenerate` button beside `Copy all`.

**Architecture:** Apply one structural normalization pass across all `template-deploy/tools-src/*name-generator.html` files. Update only shared layout markup and CSS, leaving each page's result rendering and dataset-specific controls intact.

**Tech Stack:** Static HTML, inline CSS, inline JavaScript, Node.js for verification

---

### Task 1: Inventory target templates

**Files:**
- Modify: `template-deploy/tools-src/*name-generator.html`
- Test: `template-deploy/tools-src/*name-generator.html`

- [ ] **Step 1: Enumerate the target files**

Run: `rg --files template-deploy/tools-src | rg 'name-generator\\.html$'`
Expected: A list of all name-generator templates, including `random-name-generator.html`.

- [ ] **Step 2: Check current structure markers**

Run: `node` script to report whether each file has a regenerate button and whether `saved-section` sits after `tool-split`.
Expected: A per-file summary showing which templates need structural normalization.

### Task 2: Normalize shared structure

**Files:**
- Modify: `template-deploy/tools-src/*name-generator.html`

- [ ] **Step 1: Move saved sections below the split container where needed**

Implementation:
- Ensure `saved-section` is a sibling after `tool-split`, not nested inside the left controls or right results panel.

- [ ] **Step 2: Add regenerate buttons where missing**

Implementation:
- Insert `<button type="button" class="act-btn" id="<prefix>-regen-btn" onclick="document.getElementById('<prefix>-gen-btn')?.click()">Regenerate</button>` beside `Copy all`.

- [ ] **Step 3: Normalize shared layout selectors**

Implementation:
- Standardize structural CSS for `.ctrl`, `.words-panel`, `.words-top`, `.words-actions`, `.word-list`, and `.saved-section`.
- Preserve page-specific selectors outside those structural rules.

### Task 3: Verify the template set

**Files:**
- Test: `template-deploy/tools-src/*name-generator.html`

- [ ] **Step 1: Run structural verification**

Run: `node` script that checks each target template for the regenerate button, bottom saved section, and normalized shared selectors.
Expected: All target templates report success.

- [ ] **Step 2: Spot-check representative files**

Run: inspect `random-name-generator.html`, `random-danish-name-generator.html`, and `random-chinese-name-generator.html`.
Expected: Shared structure is aligned while page-specific name-result styling remains intact.

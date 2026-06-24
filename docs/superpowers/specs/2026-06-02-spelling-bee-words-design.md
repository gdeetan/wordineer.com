# Spelling Bee Words Generator — Design Spec

**Date:** 2026-06-02  
**Status:** Approved  
**URL:** `/spelling-bee-words/`  
**Output:** `spelling-bee-words.html`

---

## Context

No fast, filterable spelling bee word generator exists in the market. Competitors are either static lists (SpellingWordsWell, LitSpelling) or heavy platforms requiring login and audio (SpellQuiz). Wordineer's static-site generator pattern — instant results, filter controls, save/copy, print — is a natural fit and can outdo all of them on UX while staying framework-free.

Primary audiences: students preparing for school/regional bees, teachers and coaches building custom practice lists.

---

## Data

### New file: `wordineer-deploy/data/spelling-bee-words.json`

Array of ~1,000 word objects:

```json
{ "w": "entrepreneur", "grade": "adult", "diff": "hard",
  "origin": "French", "syl": 5, "pos": "noun",
  "d": "a person who organizes and operates a business" }
```

**Field values:**

- `grade`: `"k-2"` | `"3-4"` | `"5-6"` | `"7-8"` | `"9-12"` | `"adult"`
- `diff`: `"easy"` | `"medium"` | `"hard"` | `"expert"`
- `origin`: `"Latin"` | `"Greek"` | `"French"` | `"Germanic"` | `"Anglo-Saxon"` | `"Spanish"` | `"Other"`
- `syl`: integer (1–7)
- `pos`: `"noun"` | `"verb"` | `"adjective"` | `"adverb"`
- `d`: definition string, max ~100 chars

**Word distribution target (~1,000 total):**

| Grade | Easy | Medium | Hard | Expert | Total |
|-------|------|--------|------|--------|-------|
| k-2   | 40   | 30     | 20   | —      | ~90   |
| 3-4   | 40   | 40     | 30   | 10     | ~120  |
| 5-6   | 30   | 40     | 40   | 20     | ~130  |
| 7-8   | 20   | 40     | 50   | 30     | ~140  |
| 9-12  | 10   | 30     | 60   | 60     | ~160  |
| adult | —    | 20     | 80   | 80     | ~180  |
| **Total** | | | | | **~820–1,000** |

Words should span a range of origins (Latin, Greek, French prominent in higher grades; Anglo-Saxon/Germanic dominant in lower grades).

---

## Tool Page

### CONFIG block

```html
<!-- CONFIG
{ "url": "/spelling-bee-words/", "output": "spelling-bee-words.html", "type": "tool" }
-->
```

### Breadcrumbs (in SLOT:hero)

```html
<div class="breadcrumb">
  <div class="breadcrumb-inner">
    <a href="/">Wordineer</a>
    <span class="breadcrumb-sep">›</span>
    <a href="/word-tools/">Word Tools</a>
    <span class="breadcrumb-sep">›</span>
    <span aria-current="page">Spelling Bee Words</span>
  </div>
</div>
```

### Tool UI (SLOT:tool)

**Left panel — controls:**

| Control | Type | Values |
|---------|------|--------|
| Grade Level | Segmented buttons | K-2, 3-4, 5-6, 7-8, 9-12, Adult, All |
| Difficulty | Segmented buttons | Easy, Medium, Hard, Expert, All |
| Word Origin | Select/dropdown | All, Latin, Greek, French, Germanic, Anglo-Saxon, Spanish, Other |
| Count | Number input | 10–50, default 20 |
| Show Definitions | Toggle checkbox | On by default |
| Generate | Button | Primary CTA |

**Right panel — results:**

Each word card:
```
entrepreneur                [French]  5 syl  noun
a person who organizes and operates a business
                                          [♥]  [⎘]
```

- Origin badge colored by language family (subtle pill/chip)
- Syllable count always visible
- Definition shown/hidden via toggle (controls all cards)
- Heart = save to localStorage; clipboard icon = copy single word

**Top action bar (above word list):**
- "20 words" count label
- Copy All button
- **Print List** button → `window.print()` with print-specific CSS that hides everything except word number, word, syllable count, and definition

**Saved words section** (below tool card, same pattern as other tools):
- "Saved words (N)" label
- Saved tags with × to remove
- Copy Saved button

### Print CSS

```css
@media print {
  /* hide nav, controls, ads, footer, saved section */
  /* show only .print-list: numbered word, syllables, definition */
  /* clean serif font, black on white */
}
```

The print output format per word:
```
1. entrepreneur (5 syl) — French — noun
   a person who organizes and operates a business
```

---

## Explainer Copy (SLOT:explainer)

Target: ~1,100 words across 8 sections. Tone: clear, practical, no fluff.

### Section outline

**1. What Is a Spelling Bee? (~100 words)**
Brief history — Scripps National Spelling Bee, school-to-national pipeline. Why spelling bees matter for vocabulary and language development.

**2. What Is This Tool? (~150 words)**
A free generator that pulls from a curated bank of 1,000+ authentic spelling bee words. Filter by grade level, difficulty, and word origin. Generate a fresh random list every time. Save words you want to revisit. Print a clean list for classroom use.

**3. Why Use Wordineer's Spelling Bee Words Generator? (~150 words)**
- Instant randomized lists — not the same static page every time
- Etymology badges show word origins (Latin, Greek, French, etc.) — learn the pattern, not just the word
- Syllable counts on every word to aid pronunciation practice
- Print any list in one click — no copy-pasting into Word
- Save words to a personal session list
- No login, no paywall, works on any device

**4. How It Works — Step by Step (~100 words)**
1. Choose a grade level (or "All")
2. Set a difficulty tier
3. Optionally filter by word origin
4. Choose how many words (10–50)
5. Click Generate
6. Save words you want to study; print the full list for offline practice

**5. Grade-Level Breakdown (~200 words)**
Brief description of each tier and what competition level it maps to:
- K-2: foundational sight words and short phonetic patterns (school bee)
- 3-4: 2–3 syllable words, common prefixes/suffixes (school/district)
- 5-6: Latin and Greek roots start appearing (district bee)
- 7-8: borrowed words, irregular spellings, double consonants (regional)
- 9-12: advanced etymology, rare patterns (state/national)
- Adult: championship-level vocabulary (adult bees, Scripps alumni)

**6. Understanding Word Origins (~150 words)**
Why etymology matters for spelling: Latin patterns (-tion, -ance, -ent), Greek patterns (ph=f, ch=k, silent p), French patterns (-eur, -ette, -esque), Germanic patterns (double consonants, -ght). Learning the origin family lets you decode dozens of words from one rule.

**7. Best Practices for Spelling Bee Preparation (~150 words)**
- Practice saying the word aloud before spelling it
- Ask for the definition and part of speech (rules in competition)
- Learn origin patterns, not individual spellings
- Drill easy words first to build confidence
- Practice under mild time pressure (10 seconds per word)
- Review saved words daily in the week before competition
- Mix grade levels: master your grade, preview the next

**8. Tips for Teachers & Coaches (~100 words)**
- Use grade filter to build level-appropriate lists for your class
- Print 2–3 difficulty tiers separately for multi-round elimination format
- Filter by origin to build themed practice rounds (e.g., "French words day")
- Generate a new list each session — prevents memorization of a single list
- Use the "Expert" tier to challenge advanced students without jumping grades

---

## FAQ (SLOT:faq) — 7 questions

1. What grade levels does this tool cover?
2. How many spelling bee words are in the database?
3. Can I print the word list for my classroom?
4. What does word origin mean, and why does it matter?
5. How do I save words for focused practice?
6. What is the difference between difficulty levels?
7. Are these official Scripps National Spelling Bee words?

---

## Who Uses This Tool (SLOT:who)

- **Students** preparing for school, district, and regional spelling bees
- **Parents** running practice sessions at home
- **Teachers** building custom classroom bee word lists
- **Homeschool educators** covering spelling bee prep without a pre-made curriculum
- **Adults** practicing for adult spelling bee events

---

## tools.json entries

### mega menu — "Writing & Vocabulary" category
```json
{ "href": "/spelling-bee-words/", "text": "Spelling Bee Words" }
```

### more_word_tools grid
```json
{
  "href": "/spelling-bee-words/",
  "name": "Spelling Bee Words",
  "desc": "Filter 1,000+ spelling bee words by grade, difficulty, and word origin. Save and print custom lists.",
  "icon_bg": "#EEF4FE",
  "icon_path": "<path d=\"M12 3l2.5 7.5H22l-6.5 4.5 2.5 7.5L12 18l-6 4.5 2.5-7.5L3 10.5h7.5z\" stroke=\"#3B6FD4\" stroke-width=\"1.3\" stroke-linecap=\"round\" stroke-linejoin=\"round\" fill=\"none\"/>"
}
```

### footer_cols — "Word Tools" column
```json
{ "href": "/spelling-bee-words/", "text": "Spelling Bee Words" }
```

---

## _redirects entry

```
/spelling-bee-words   /spelling-bee-words/   301
```

---

## Verification Plan

1. `cd template-deploy && python3 build.py` — no errors
2. `cp template-deploy/output/spelling-bee-words.html wordineer-deploy/`
3. `cd wordineer-deploy && python3 -m http.server 8080`
4. Open `http://localhost:8080/spelling-bee-words.html`

**Checklist:**
- [ ] Grade filter changes word list correctly
- [ ] Difficulty filter works independently and combined with grade
- [ ] Origin filter narrows results correctly
- [ ] "Show Definitions" toggle shows/hides definitions on all cards
- [ ] Save (♥) adds word to saved section; × removes it
- [ ] Copy All copies full word list to clipboard
- [ ] Copy Saved copies saved words only
- [ ] Print button opens browser print dialog with clean layout (no nav/controls visible)
- [ ] Breadcrumbs render: Wordineer › Word Tools › Spelling Bee Words
- [ ] Generating 0 results (e.g., K-2 + Expert) shows a friendly "No words match" message
- [ ] Page passes Lighthouse performance ≥ 90 (data loads deferred)
- [ ] tools.json entries appear in mega menu, more_word_tools grid, footer

---

## Files to create / modify

| File | Action |
|------|--------|
| `wordineer-deploy/data/spelling-bee-words.json` | Create — ~1,000 word dataset |
| `template-deploy/tools-src/spelling-bee-words.html` | Create — full tool-src page |
| `template-deploy/tools.json` | Modify — add to mega, more_word_tools, footer_cols |
| `wordineer-deploy/_redirects` | Modify — add clean URL redirect |
| `template-deploy/output/spelling-bee-words.html` | Generated by build.py |
| `wordineer-deploy/spelling-bee-words.html` | Copied from output/ |

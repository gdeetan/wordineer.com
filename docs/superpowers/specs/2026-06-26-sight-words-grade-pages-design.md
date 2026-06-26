# Spec: Sight Words Grade Pages

**Date:** 2026-06-26  
**Status:** Approved  

---

## Goal

Build four grade-specific sight words pages that rank individually for high-volume teacher/parent searches ("kindergarten sight words", "1st grade sight words", etc.) while reusing the existing sight-words-generator engine. Each page beats competitors (static PDFs, no audio, no interactivity) with audio, practice mode, save, copy, print, and a full word list in the explainer.

---

## Pages

| URL | File output | Dolch group | Word count |
|---|---|---|---|
| `/sight-words-kindergarten/` | `sight-words-kindergarten.html` | `kindergarten` | 52 words |
| `/sight-words-1st-grade/` | `sight-words-1st-grade.html` | `1st` | 41 words |
| `/sight-words-2nd-grade/` | `sight-words-2nd-grade.html` | `2nd` | 46 words |
| `/sight-words-3rd-grade/` | `sight-words-3rd-grade.html` | `3rd` | 41 words |

---

## Architecture

**Pattern:** Thin wrapper — each page is a standalone `tools-src/` file with its own CONFIG, slots, and init script. The page loads the same `sight-words-data.json` and reuses the same JS engine as `sight-words-generator.html`, but the init script pre-sets the grade filter on page load.

No new JS engine needed. No grade-specific data files. The existing `dolch_group` field in `sight-words-data.json` handles all filtering.

### Pre-filter behavior
- On init: set `#ctrl-list` to `dolch`, set `#ctrl-group` to the page's grade (e.g. `kindergarten`), trigger generate
- Filters remain editable — no hard lock
- User can explore other grades from the same page

---

## CONFIG (per page)

```json
{
  "url": "/sight-words-kindergarten/",
  "output": "sight-words-kindergarten.html",
  "type": "tool",
  "more_tools_key": "sight_words_tools",
  "more_tools_title": "More sight words tools",
  "more_tools_subtitle": "Grade-by-grade Dolch and Fry practice"
}
```

---

## Slot: meta

Each page gets its own `<title>`, `<meta name="description">`, canonical URL, and three JSON-LD blocks:

1. `WebApplication` schema (same as sight-words-generator, url/name adjusted per page)
2. `BreadcrumbList` — 4 levels (see below)
3. `FAQPage` — 6 questions per page (grade-specific, see FAQ section)

### Canonical URLs
- `https://wordineer.com/sight-words-kindergarten/`
- `https://wordineer.com/sight-words-1st-grade/`
- `https://wordineer.com/sight-words-2nd-grade/`
- `https://wordineer.com/sight-words-3rd-grade/`

---

## Slot: hero

### Breadcrumb (4 levels)
```
Wordineer › Word Tools › Sight Words Generator › [Grade]
```
- Wordineer → `/`
- Word Tools → `/word-tools/`
- Sight Words Generator → `/sight-words-generator/`
- [Grade] → current page (aria-current="page")

### Hero badge
`"[N] Words · Audio · Practice Mode · Free"`  
e.g. `"52 Words · Audio · Practice Mode · Free"` for kindergarten

### H1 examples
- Kindergarten: `Kindergarten Sight Words`
- 1st Grade: `First Grade Sight Words`
- 2nd Grade: `Second Grade Sight Words`
- 3rd Grade: `Third Grade Sight Words`

### Subtitle (1-2 sentences, grade-specific)
Example for kindergarten:  
"The complete Dolch Kindergarten list — 52 words every beginning reader should recognize on sight. Filter, generate, hear each word aloud, and drill with Practice Mode. No login, no download."

---

## Slot: tool

Identical structure to `sight-words-generator.html`. No changes to the tool UI itself — the init script handles pre-selection.

---

## Cross-grade nav strip

Inserted immediately after the tool card, before the explainer. A compact row of links to all grade pages and the master generator. Example:

```
Also: Pre-K · [Kindergarten] · 1st Grade · 2nd Grade · 3rd Grade · All Grades →
```

Current page shown as plain text (not a link). Styled as a simple pill-link row. Helps users navigate without returning to the hub, and creates internal linking across the cluster.

---

## Slot: explainer (1,000+ words per page)

### Section 1: Complete word list for this grade
Hardcoded HTML — a grid of all words for the grade (e.g., all 52 kindergarten Dolch words), displayed as scannable chips/badges. This makes the page useful without JS and signals to search engines that the page is the authoritative resource for this grade's list.

Label: `"All [N] Dolch [Grade] Sight Words"` as an H2.

### Section 2: What these words are and why they matter at this grade
~200 words. Grade-specific. For kindergarten: transition from letter recognition to word recognition, pre-reading to early reading. For 3rd grade: consolidating fluency before chapter books, bridge to independent reading.

### Section 3: How many words kids should know by end of this grade
~150 words. Concrete benchmarks with context — not just a number, but what it means developmentally. Dolch grade bands as cumulative (e.g., a 1st grader should know Pre-K + Kindergarten + 1st Grade = ~133 words). Framed for parents: what's normal, when to be concerned, how to tell progress is happening.

### Section 4: Teaching strategies specific to this grade
~300 words. Grade-calibrated advice:
- **Kindergarten:** Flash card cadence, two-at-a-time introduction, multi-sensory (say it, write it, trace it), keeping sessions under 10 minutes
- **1st grade:** Speed drills, reading in context (not just isolated), partner reading, word walls
- **2nd grade:** Automaticity focus — if they're still sounding out, reteach; sentence-level context; self-correction habits
- **3rd grade:** Words in writing, not just reading; transfer to chapter books; catching gaps in prior grade lists

### Section 5: A 4-week practice schedule
~250 words. Concrete weekly plan. Week 1: introduce half the list. Week 2: drill the full list, identify trouble words. Week 3: practice trouble words 3× daily. Week 4: review + test readiness. Woven into normal daily routine — breakfast, car ride, bedtime.

### Section 6: How to use this tool with your child
~150 words. Step-by-step: set filters, generate, hear words, save hard ones, run Practice Mode. Practical, parent-friendly tone.

---

## Slot: faq (6 questions per page)

### Kindergarten FAQ
1. How many sight words should a kindergartner know by the end of the year?
2. What's the difference between Dolch and Fry for kindergarten?
3. My child is in kindergarten but already knows all 52 words. What's next?
4. How long should daily sight word practice be for a 5-year-old?
5. Is it okay if my kindergartner reads sight words slowly? Does it need to be instant?
6. Can I use this tool for pre-K as well?

### 1st Grade FAQ
1. How many total sight words should a 1st grader know?
2. What if my 1st grader is still struggling with kindergarten words?
3. How are 1st grade sight words different from kindergarten words?
4. Should I focus on Dolch or Fry in 1st grade?
5. How do I make sight word practice less boring for a 6-year-old?
6. My child's teacher uses a different list — is that a problem?

### 2nd Grade FAQ
1. How many sight words should a 2nd grader know by end of year?
2. At what point should sight words be automatic vs. sounded out?
3. What if my 2nd grader has gaps in the kindergarten and 1st grade lists?
4. How do sight words connect to spelling in 2nd grade?
5. My child reads sight words in isolation but forgets them in a book. Why?
6. Is Dolch or Fry more relevant in 2nd grade?

### 3rd Grade FAQ
1. Do 3rd graders still need to practice sight words?
2. How many Dolch words should a 3rd grader know total (cumulative)?
3. What comes after the Dolch 3rd grade list?
4. My 3rd grader reads fine but struggles to write sight words correctly. Is that normal?
5. How do sight words relate to reading fluency in 3rd grade?
6. Should I move my 3rd grader to the Fry list?

---

## Slot: who (4 cards per page, grade-adjusted)

### Kindergarten
- Parents of 5-year-olds starting school
- Kindergarten teachers running morning word drills
- Pre-K teachers preparing advanced students
- Homeschool parents following a K curriculum

### 1st Grade
- Parents supporting early readers at home
- 1st grade teachers building word walls
- Reading tutors working with struggling readers
- After-school program instructors

### 2nd Grade
- Parents helping children bridge to chapter books
- 2nd grade teachers tracking fluency progress
- Reading interventionists catching gaps early
- Homeschool educators following grade benchmarks

### 3rd Grade
- Parents of kids preparing for independent reading
- 3rd grade teachers consolidating word banks
- Reading specialists working on automaticity
- Tutors identifying gaps from earlier grade lists

---

## Slot: init

Per-page init script sets the grade filter before first render:

```javascript
// Kindergarten example
document.addEventListener('DOMContentLoaded', function () {
  var listEl  = document.getElementById('ctrl-list');
  var groupEl = document.getElementById('ctrl-group');
  if (listEl)  listEl.value  = 'dolch';
  if (groupEl) { SW.rebuildGroupSelect(); groupEl.value = 'kindergarten'; }
  document.getElementById('sw-gen-btn').click();
});
```

Each page sets the appropriate `groupEl.value` for its grade.

---

## word-tools.html changes

Add a sub-section below the existing Sight Words Generator card in the Vocabulary & Learning section. Four new live `<a class="tool-item">` cards, one per grade page. Use the same icon color/style as the existing sight words card (purple/pink, `background:#FEE9F9` or match exactly).

Remove any "Coming soon" badge if the cards exist already as placeholders.

---

## tools.json changes

Add all 4 grade page URLs to:
1. `mega` array — under the sight words / vocabulary category
2. `footer_cols` — under vocabulary/learning column

Format:
```json
{ "href": "/sight-words-kindergarten/", "text": "Kindergarten Sight Words" }
```

---

## _redirects

Add clean URL rewrites for each page (if not already handled by Cloudflare Pages):
```
/sight-words-kindergarten   /sight-words-kindergarten/   301
/sight-words-1st-grade      /sight-words-1st-grade/      301
/sight-words-2nd-grade      /sight-words-2nd-grade/      301
/sight-words-3rd-grade      /sight-words-3rd-grade/      301
```

---

## Content tone guidelines

- Direct and helpful — parent talking to parent, teacher talking to teacher
- No filler phrases ("In today's world...", "It is important to note...")
- Specific numbers, concrete actions, honest benchmarks
- Short paragraphs (2-4 sentences max)
- No AI tells: no "delve into", no "tapestry of", no "it's worth noting"

---

## Deliverables

1. `template-deploy/tools-src/sight-words-kindergarten.html`
2. `template-deploy/tools-src/sight-words-1st-grade.html`
3. `template-deploy/tools-src/sight-words-2nd-grade.html`
4. `template-deploy/tools-src/sight-words-3rd-grade.html`
5. Updated `template-deploy/tools-src/word-tools.html` — 4 new grade page cards
6. Updated `template-deploy/tools.json` — mega menu + footer entries
7. Build all pages → copy output to `wordineer-deploy/`
8. Add `_redirects` entries for clean URLs
9. Do NOT deploy to Cloudflare — push to git only

---

## Success criteria

- Each page ranks independently for "[grade] sight words" within 60 days
- Tool pre-loads filtered to correct grade on arrival
- Complete word list visible in explainer without JS
- Cross-grade nav strip links all 4 pages + master generator
- word-tools hub shows all 4 grade pages as live links
- 1,000+ words of content per page

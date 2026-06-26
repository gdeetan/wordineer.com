# Sight Words Grade Pages Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build four grade-specific Dolch sight words pages (Kindergarten, 1st, 2nd, 3rd Grade) that each rank independently, pre-filter the existing sight-words-generator engine to their grade, and include 1,000+ words of original content per page.

**Architecture:** Each page is a standalone `tools-src/` HTML file using the CONFIG/SLOT build system. The JS engine from `sight-words-generator.html` is copied verbatim into each page's `SLOT:init`; the DOMContentLoaded handler is modified to set grade defaults before calling `SW.generate()`. No new JS files — all data comes from the existing `wordineer-deploy/data/sight-words-data.json` which already has `dolch_group` tags.

**Tech Stack:** Static HTML, vanilla JS (existing SW engine), Python build.py, sight-words-data.json (423 words with dolch_group/fry_group fields)

---

## Files

**Create:**
- `template-deploy/tools-src/sight-words-kindergarten.html`
- `template-deploy/tools-src/sight-words-1st-grade.html`
- `template-deploy/tools-src/sight-words-2nd-grade.html`
- `template-deploy/tools-src/sight-words-3rd-grade.html`

**Modify:**
- `template-deploy/tools.json` — add sight_words_tools more-tools block; add grade pages to mega + footer
- `template-deploy/tools-src/word-tools.html` — add 4 grade page cards to Vocabulary section
- `wordineer-deploy/_redirects` — add clean URL rewrites for all 4 pages

**Build output (after running build.py + copy):**
- `wordineer-deploy/sight-words-kindergarten.html`
- `wordineer-deploy/sight-words-1st-grade.html`
- `wordineer-deploy/sight-words-2nd-grade.html`
- `wordineer-deploy/sight-words-3rd-grade.html`

---

## Task 1: Update tools.json and word-tools.html

**Files:**
- Modify: `template-deploy/tools.json`
- Modify: `template-deploy/tools-src/word-tools.html`

- [ ] **Step 1: Add sight_words_tools block to tools.json**

Open `template-deploy/tools.json`. Find the `"more_tools"` top-level key (same level as `"mega"`, `"footer_cols"`, etc.). Add the following entry to the `more_tools` object:

```json
"sight_words_tools": {
  "title": "More sight words tools",
  "subtitle": "Grade-by-grade Dolch and Fry practice",
  "tools": [
    { "href": "/sight-words-generator/", "text": "Sight Words Generator", "desc": "All grades, Dolch + Fry, audio, Practice Mode." },
    { "href": "/sight-words-kindergarten/", "text": "Kindergarten Sight Words", "desc": "All 52 Dolch Kindergarten words." },
    { "href": "/sight-words-1st-grade/", "text": "First Grade Sight Words", "desc": "All 41 Dolch 1st Grade words." },
    { "href": "/sight-words-2nd-grade/", "text": "Second Grade Sight Words", "desc": "All 46 Dolch 2nd Grade words." },
    { "href": "/sight-words-3rd-grade/", "text": "Third Grade Sight Words", "desc": "All 41 Dolch 3rd Grade words." }
  ]
}
```

- [ ] **Step 2: Add grade pages to mega menu**

In `tools.json`, find the `"mega"` array. Find the category object that contains `"/sight-words-generator/"`. Add the 4 grade pages after the generator entry:

```json
{ "href": "/sight-words-kindergarten/", "text": "Kindergarten Sight Words" },
{ "href": "/sight-words-1st-grade/", "text": "First Grade Sight Words" },
{ "href": "/sight-words-2nd-grade/", "text": "Second Grade Sight Words" },
{ "href": "/sight-words-3rd-grade/", "text": "Third Grade Sight Words" }
```

- [ ] **Step 3: Add grade pages to footer_cols**

In `tools.json`, find `"footer_cols"`. In the column that contains `"/sight-words-generator/"`, add the 4 grade page entries after it following the same `{"href": "...", "text": "..."}` format.

- [ ] **Step 4: Add grade page cards to word-tools.html**

Open `template-deploy/tools-src/word-tools.html`. Find the existing Sight Words Generator card:

```html
<a class="tool-item" href="/sight-words-generator/">
  <div class="tool-icon" style="background:#FEE9F9">...</div>
  <div class="tool-name">Sight Words Generator</div>
  <div class="tool-desc">Dolch and Fry sight words with audio, grade filters, and Practice Mode.</div>
</a>
```

Add the following 4 cards immediately after it (copy the icon SVG from the sight-words-generator card):

```html
<a class="tool-item" href="/sight-words-kindergarten/">
  <div class="tool-icon" style="background:#FEE9F9"><svg viewBox="0 0 13 13" fill="none"><path d="M2 10V4.5C2 3.4 2.9 2.5 4 2.5h5c1.1 0 2 .9 2 2V10" stroke="#B0279A" stroke-width=".9" stroke-linecap="round"/><path d="M4 6.5h5M4 8.5h3" stroke="#B0279A" stroke-width=".75" stroke-linecap="round"/><path d="M5.5 2.5v2" stroke="#B0279A" stroke-width=".75" stroke-linecap="round"/></svg></div>
  <div class="tool-name">Kindergarten Sight Words</div>
  <div class="tool-desc">All 52 Dolch Kindergarten words with audio and Practice Mode.</div>
</a>

<a class="tool-item" href="/sight-words-1st-grade/">
  <div class="tool-icon" style="background:#FEE9F9"><svg viewBox="0 0 13 13" fill="none"><path d="M2 10V4.5C2 3.4 2.9 2.5 4 2.5h5c1.1 0 2 .9 2 2V10" stroke="#B0279A" stroke-width=".9" stroke-linecap="round"/><path d="M4 6.5h5M4 8.5h3" stroke="#B0279A" stroke-width=".75" stroke-linecap="round"/><path d="M5.5 2.5v2" stroke="#B0279A" stroke-width=".75" stroke-linecap="round"/></svg></div>
  <div class="tool-name">First Grade Sight Words</div>
  <div class="tool-desc">All 41 Dolch 1st Grade words with audio and Practice Mode.</div>
</a>

<a class="tool-item" href="/sight-words-2nd-grade/">
  <div class="tool-icon" style="background:#FEE9F9"><svg viewBox="0 0 13 13" fill="none"><path d="M2 10V4.5C2 3.4 2.9 2.5 4 2.5h5c1.1 0 2 .9 2 2V10" stroke="#B0279A" stroke-width=".9" stroke-linecap="round"/><path d="M4 6.5h5M4 8.5h3" stroke="#B0279A" stroke-width=".75" stroke-linecap="round"/><path d="M5.5 2.5v2" stroke="#B0279A" stroke-width=".75" stroke-linecap="round"/></svg></div>
  <div class="tool-name">Second Grade Sight Words</div>
  <div class="tool-desc">All 46 Dolch 2nd Grade words with audio and Practice Mode.</div>
</a>

<a class="tool-item" href="/sight-words-3rd-grade/">
  <div class="tool-icon" style="background:#FEE9F9"><svg viewBox="0 0 13 13" fill="none"><path d="M2 10V4.5C2 3.4 2.9 2.5 4 2.5h5c1.1 0 2 .9 2 2V10" stroke="#B0279A" stroke-width=".9" stroke-linecap="round"/><path d="M4 6.5h5M4 8.5h3" stroke="#B0279A" stroke-width=".75" stroke-linecap="round"/><path d="M5.5 2.5v2" stroke="#B0279A" stroke-width=".75" stroke-linecap="round"/></svg></div>
  <div class="tool-name">Third Grade Sight Words</div>
  <div class="tool-desc">All 41 Dolch 3rd Grade words with audio and Practice Mode.</div>
</a>
```

- [ ] **Step 5: Commit**

```bash
git add template-deploy/tools.json template-deploy/tools-src/word-tools.html
git commit -m "feat: add sight words grade pages to tools.json and word-tools hub"
```

---

## Task 2: Create sight-words-kindergarten.html

**Files:**
- Create: `template-deploy/tools-src/sight-words-kindergarten.html`

- [ ] **Step 1: Create the file with CONFIG and meta slot**

```html
<!-- CONFIG
{
  "url": "/sight-words-kindergarten/",
  "output": "sight-words-kindergarten.html",
  "type": "tool",
  "more_tools_key": "sight_words_tools",
  "more_tools_title": "More sight words tools",
  "more_tools_subtitle": "Grade-by-grade Dolch and Fry practice"
}
-->

<!-- SLOT:meta -->
<title>Kindergarten Sight Words — Dolch List with Audio &amp; Practice Mode | Wordineer</title>
<meta name="description" content="All 52 Dolch Kindergarten sight words with audio pronunciation and Practice Mode. Generate, drill, and save trouble words — built for parents and teachers. Free, no login.">
<meta property="og:title" content="Kindergarten Sight Words — Dolch List with Audio &amp; Practice Mode | Wordineer">
<meta property="og:description" content="All 52 Dolch Kindergarten sight words with audio pronunciation and Practice Mode. Free, no login required.">
<meta property="og:url" content="https://wordineer.com/sight-words-kindergarten/">
<meta property="og:type" content="website">
<link rel="canonical" href="https://wordineer.com/sight-words-kindergarten/">
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "WebApplication",
  "name": "Kindergarten Sight Words",
  "url": "https://wordineer.com/sight-words-kindergarten/",
  "description": "Practice all 52 Dolch Kindergarten sight words with audio pronunciation and Practice Mode. Free, no login required.",
  "applicationCategory": "EducationApplication",
  "operatingSystem": "Any",
  "offers": { "@type": "Offer", "price": "0" }
}
</script>
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    { "@type": "ListItem", "position": 1, "name": "Wordineer", "item": "https://wordineer.com/" },
    { "@type": "ListItem", "position": 2, "name": "Word Tools", "item": "https://wordineer.com/word-tools/" },
    { "@type": "ListItem", "position": 3, "name": "Sight Words Generator", "item": "https://wordineer.com/sight-words-generator/" },
    { "@type": "ListItem", "position": 4, "name": "Kindergarten", "item": "https://wordineer.com/sight-words-kindergarten/" }
  ]
}
</script>
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "How many sight words should a kindergartner know by the end of the year?",
      "acceptedAnswer": { "@type": "Answer", "text": "By June of kindergarten, most children should recognize all 92 Dolch Pre-K and Kindergarten words — that's the 40 Pre-K words plus the 52 Kindergarten words. The goal is automatic recognition under two seconds per word, not just correctness after a long pause." }
    },
    {
      "@type": "Question",
      "name": "What is the difference between Dolch and Fry sight words for kindergarten?",
      "acceptedAnswer": { "@type": "Answer", "text": "The Dolch list organizes 315 words into grade bands from Pre-K through 3rd grade — ideal for tracking classroom progress year by year. The Fry list orders 1,000 words by frequency without grade bands. For kindergartners, Dolch is the standard most American teachers use, so matching the classroom list is the best starting point." }
    },
    {
      "@type": "Question",
      "name": "My kindergartner already knows all 52 words. What comes next?",
      "acceptedAnswer": { "@type": "Answer", "text": "Move to the Dolch 1st Grade list. Change the grade filter in this generator to '1st Grade' or visit the First Grade Sight Words page. Some parents also start the Fry 1–100 list in parallel once their child has solid kindergarten coverage." }
    },
    {
      "@type": "Question",
      "name": "How long should daily sight word practice be for a 5-year-old?",
      "acceptedAnswer": { "@type": "Answer", "text": "Five to ten minutes maximum. Short, consistent sessions work better than long infrequent ones. Morning before school or right after dinner when attention is fresh tends to outperform bedtime practice for most kids this age." }
    },
    {
      "@type": "Question",
      "name": "Does sight word recognition need to be instant?",
      "acceptedAnswer": { "@type": "Answer", "text": "Eventually, yes. The goal is recognition in under one to two seconds — that's what 'automatic' means. In the early weeks, a 3-second pause is fine. By the end of kindergarten, the aim is instant recall. Practice Mode in this tool helps build that speed over time." }
    },
    {
      "@type": "Question",
      "name": "Can I use this tool for Pre-K words too?",
      "acceptedAnswer": { "@type": "Answer", "text": "Yes. Change the Grade group filter to 'Dolch Pre-K' to get the 40 Pre-K words. This page defaults to kindergarten, but all Dolch grade groups are available in the filter." }
    }
  ]
}
</script>
<!-- /SLOT:meta -->
```

- [ ] **Step 2: Add style slot**

```html
<!-- SLOT:style -->
<style>
.word-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin: 16px 0 28px;
}
.word-chip {
  background: var(--surface-2, #f0f0f8);
  border: 1px solid var(--border, #e5e5ea);
  border-radius: 6px;
  padding: 5px 12px;
  font-size: 14px;
  font-weight: 600;
  color: var(--text-1);
  letter-spacing: .01em;
}
.grade-nav {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  align-items: center;
  margin: 0 0 36px;
  font-size: 13px;
}
.grade-nav-label {
  color: var(--text-3, #aaa);
  margin-right: 2px;
}
.grade-nav a {
  padding: 4px 12px;
  border-radius: 20px;
  text-decoration: none;
  background: var(--surface-2, #f0f0f8);
  color: var(--text-2);
  border: 1px solid var(--border, #e5e5ea);
  transition: background .15s;
}
.grade-nav a:hover { background: var(--surface-3, #e8e8f0); }
.grade-nav-current {
  padding: 4px 12px;
  border-radius: 20px;
  background: #3C3489;
  color: #fff;
  font-weight: 600;
  font-size: 13px;
}
.explainer h2 {
  font-family: 'DM Serif Display', serif;
  font-size: 22px;
  font-weight: 400;
  margin: 36px 0 10px;
  color: var(--text);
}
.explainer p, .explainer li {
  font-size: 15px;
  line-height: 1.75;
  color: var(--text-2);
  margin: 0 0 14px;
}
.explainer ul, .explainer ol {
  padding-left: 20px;
  margin: 0 0 16px;
}
.explainer li { margin: 0 0 8px; }
.explainer strong { color: var(--text-1); }
@media (max-width: 600px) {
  .results-col { min-height: 300px; }
  .mobile-more-toggle { display: block; }
  .advanced-options { display: none; }
  .advanced-options.is-open { display: block; }
  .gen-btn { margin-top: 0; }
  .reset-btn, .kbd { display: none; }
  .practice-word-display { font-size: 36px; }
}
@media print {
  header, nav, .breadcrumb, .hero, .ctrl, .sw-top-bar, .saved-section, .practice-panel, .explainer, .faq, .who, footer, .ad, [class*="ad-"], .more-tools, .grade-nav { display: none !important; }
  .word-item { border-top: none; border-bottom: 1px solid #e5e7eb; padding: 8px 0; break-inside: avoid; }
  .word-text { font-size: 1.1rem; }
  @page { margin: 1.5cm; }
}
</style>
<!-- /SLOT:style -->
```

- [ ] **Step 3: Add hero slot**

```html
<!-- SLOT:hero -->
<div class="breadcrumb">
  <div class="breadcrumb-inner">
    <a href="/">Wordineer</a>
    <span class="breadcrumb-sep">›</span>
    <a href="/word-tools/">Word Tools</a>
    <span class="breadcrumb-sep">›</span>
    <a href="/sight-words-generator/">Sight Words Generator</a>
    <span class="breadcrumb-sep">›</span>
    <span aria-current="page">Kindergarten</span>
  </div>
</div>
<div class="hero">
  <div class="hero-badge">52 Words · Audio · Practice Mode · Free</div>
  <h1>Kindergarten Sight Words</h1>
  <p>The complete Dolch Kindergarten list — 52 words every beginning reader should recognize on sight by end of the school year. Hear each word aloud, save the ones your child misses, and drill with Practice Mode. No account needed.</p>
</div>
<!-- /SLOT:hero -->
```

- [ ] **Step 4: Add tool slot**

Copy the entire `<!-- SLOT:tool --> ... <!-- /SLOT:tool -->` block from `template-deploy/tools-src/sight-words-generator.html` verbatim. The JS will set the defaults — no changes needed to the HTML selects.

- [ ] **Step 5: Add explainer slot**

```html
<!-- SLOT:explainer -->
<div class="explainer">

  <div class="grade-nav">
    <span class="grade-nav-label">Grade:</span>
    <a href="/sight-words-generator/">All Grades</a>
    <span class="grade-nav-current">Kindergarten</span>
    <a href="/sight-words-1st-grade/">1st Grade</a>
    <a href="/sight-words-2nd-grade/">2nd Grade</a>
    <a href="/sight-words-3rd-grade/">3rd Grade</a>
  </div>

  <h2>All 52 Dolch Kindergarten Sight Words</h2>
  <div class="word-chips">
    <span class="word-chip">all</span><span class="word-chip">am</span><span class="word-chip">are</span><span class="word-chip">at</span><span class="word-chip">ate</span><span class="word-chip">be</span><span class="word-chip">black</span><span class="word-chip">brown</span><span class="word-chip">but</span><span class="word-chip">came</span><span class="word-chip">did</span><span class="word-chip">do</span><span class="word-chip">eat</span><span class="word-chip">four</span><span class="word-chip">get</span><span class="word-chip">good</span><span class="word-chip">have</span><span class="word-chip">he</span><span class="word-chip">into</span><span class="word-chip">like</span><span class="word-chip">must</span><span class="word-chip">new</span><span class="word-chip">no</span><span class="word-chip">now</span><span class="word-chip">on</span><span class="word-chip">our</span><span class="word-chip">out</span><span class="word-chip">please</span><span class="word-chip">pretty</span><span class="word-chip">ran</span><span class="word-chip">ride</span><span class="word-chip">saw</span><span class="word-chip">say</span><span class="word-chip">she</span><span class="word-chip">so</span><span class="word-chip">soon</span><span class="word-chip">that</span><span class="word-chip">there</span><span class="word-chip">they</span><span class="word-chip">this</span><span class="word-chip">too</span><span class="word-chip">under</span><span class="word-chip">want</span><span class="word-chip">was</span><span class="word-chip">well</span><span class="word-chip">went</span><span class="word-chip">what</span><span class="word-chip">white</span><span class="word-chip">who</span><span class="word-chip">will</span><span class="word-chip">with</span><span class="word-chip">yes</span>
  </div>

  <h2>What these words are — and why these 52 matter</h2>
  <p>The Dolch Kindergarten list has 52 words — not chosen at random, but identified by Dr. Edward Dolch after analyzing hundreds of children's books in the 1930s. His finding was simple: certain words appeared in nearly every page a child would ever read, regardless of topic or grade level. "She," "have," "went," "what," "they" — these words are in almost every sentence. If a child has to sound them out every time, reading slows to a crawl and comprehension suffers. Knowing them automatically frees up mental energy for the harder, less predictable words.</p>
  <p>Combined with the 40 Pre-K words most children start on in preschool, there are 92 total Dolch words to cover by the end of kindergarten. That sounds like a lot. In practice, most kids who get daily exposure to books and five to ten minutes of deliberate practice per week move through the list steadily over the school year.</p>
  <p>"Sight words" is a slightly misleading name — it implies you just show a child the word and they learn it. Recognition comes from repeated exposure across multiple contexts: seeing the word in books, writing it by hand, hearing it read aloud, and recalling it independently under mild pressure. The generator handles the audio and randomization; the writing-it-down part is worth doing separately with paper and pencil.</p>

  <h2>How many words should a kindergartner know by the end of the year?</h2>
  <p>The standard benchmark is all 92 Dolch Pre-K and Kindergarten words by June — the 40 Pre-K words plus all 52 on this page. But "know" has a threshold: the goal isn't just correctness after a long pause. It's recognition in under two seconds. A child who reads "they" correctly after five seconds of thought hasn't mastered it yet. Automatic recognition means they see the word and say it the way you'd read your own name — without any visible effort.</p>
  <p>If your child is a few words behind the benchmark in March, that's completely normal. Development isn't a straight line. What matters more is steady progress month to month. If they've stalled entirely or regressed, that's worth raising with their teacher. If they're at 70 words in March and clearly moving forward, they're fine.</p>
  <p>Practice Mode in this tool is specifically designed to build speed, not just accuracy. It shows one word at a time and requires an active response before moving on — that's closer to actual reading than looking at a flashcard stack in order.</p>

  <h2>Teaching kindergarten sight words: what actually works</h2>
  <p>Two new words at a time. That's the rule most kindergarten teachers use, and it works at home too. Don't introduce ten words in one session hoping some will stick. Pick two, work on them across three or four sessions, then add two more. This feels slow. The retention rate is higher, and the total time to get through all 52 words is shorter this way than throwing them all at once.</p>
  <p>A four-step routine that takes about eight minutes:</p>
  <ol>
    <li><strong>Say it.</strong> Show the word, say it clearly, have your child repeat it.</li>
    <li><strong>Spell it.</strong> Go through each letter together out loud.</li>
    <li><strong>Write it.</strong> Your child writes the word on paper or a whiteboard — not a tablet. Handwriting activates memory differently than tracing on a screen or typing.</li>
    <li><strong>Find it.</strong> Look together in a book you're already reading and point to the word in real text. Finding it in context is more powerful than seeing it in isolation.</li>
  </ol>
  <p>Repeat across multiple evenings before moving to new words. Use this generator to vary practice — a random selection from the kindergarten list keeps sessions from feeling mechanical and trains recognition that's independent of order.</p>
  <p>Keep sessions short. Five to ten minutes is the right range for a five-year-old. If your child is clearly distracted or getting frustrated, stop. Forcing practice when attention is gone builds resistance, not reading ability.</p>
  <p>A few words that consistently trip kindergartners up:</p>
  <ul>
    <li><strong>"was" and "saw"</strong> — same letters, different order. Kids mix these up constantly. Practice them as a deliberate pair.</li>
    <li><strong>"they"</strong> — kids sometimes read it as "the" because the first three letters match. Make them look at the full word before responding.</li>
    <li><strong>"pretty"</strong> — the irregular vowel sound confuses kids who try to sound it out. Worth extra repetitions.</li>
    <li><strong>"want"</strong> — the "a" sounds like "o" in speech. Unusual for a word at this level.</li>
    <li><strong>"please"</strong> — the silent letter pattern trips kids up. Slow it down and say each letter clearly.</li>
  </ul>
  <p>Save trouble words using the heart icon and return to them first in each session until they're solid.</p>

  <h2>A 4-week practice schedule</h2>
  <p>This is a loose structure, not a rigid program. Adjust based on your child's pace.</p>
  <p><strong>Week 1:</strong> Introduce words 1–26. Two new words per day using the four-step routine above. Spend at least two sessions on each pair before moving on. By the end of the week you should have introduced roughly half the list — don't expect mastery yet, just exposure and initial recognition.</p>
  <p><strong>Week 2:</strong> Introduce words 27–52 while reviewing week 1 words at the start of each session. Start using the generator for random mixes — recognizing words out of the order you taught them is an important skill that pure flashcard routines often miss.</p>
  <p><strong>Week 3:</strong> Identify trouble words using the save feature and target those specifically. Run Practice Mode every day this week. The goal is getting response time under two seconds for every word on the list.</p>
  <p><strong>Week 4:</strong> Speed and transfer. Take a familiar book and page through it, pointing to kindergarten sight words as you go. Count how many your child gets right on first glance. Read two pages together and notice how often these 52 words appear — seeing them in real sentences is motivating and shows kids that what they've been drilling actually matters in books.</p>

  <h2>How to use this tool with your child</h2>
  <p>The generator is already filtered to the Dolch Kindergarten list. Hit Generate (or press Space) to get a random selection of words. Click the speaker icon on any word to hear it read aloud — useful for checking pronunciation or running a listening-only session where your child hears the word before seeing it. Click the heart on any word your child misses to save it; saved words stay between sessions. When you're ready to drill, hit Practice Mode — the list collapses to one word at a time, which more closely simulates actual reading than scanning a full list.</p>

</div>
<!-- /SLOT:explainer -->
```

- [ ] **Step 6: Add faq slot**

```html
<!-- SLOT:faq -->
<div class="faq">
  <h2 class="faq-title">Frequently asked questions</h2>

  <div class="faq-item open">
    <button class="faq-q"><span class="faq-q-text">How many sight words should a kindergartner know by end of year?</span><svg class="faq-chevron" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></button>
    <div class="faq-a">By June, most kindergartners should recognize all 92 Dolch Pre-K and Kindergarten words — the 40 Pre-K words plus all 52 on this page. That's the standard classroom benchmark. A child who knows 80 of the 92 and is clearly progressing is in good shape; benchmarks are guidelines, not hard cutoffs.</div>
  </div>

  <div class="faq-item">
    <button class="faq-q"><span class="faq-q-text">What's the difference between Dolch and Fry for kindergarten?</span><svg class="faq-chevron" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></button>
    <div class="faq-a">Dolch organizes words by grade level from Pre-K through 3rd grade — it maps directly to classroom progression. Fry orders 1,000 words by frequency without grade bands. For kindergartners, Dolch is what most American teachers use. If your child's school uses a specific list, match it. If they don't specify, start with Dolch.</div>
  </div>

  <div class="faq-item">
    <button class="faq-q"><span class="faq-q-text">My child already knows all 52 words. What comes next?</span><svg class="faq-chevron" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></button>
    <div class="faq-a">Move to the <a href="/sight-words-1st-grade/">Dolch 1st Grade list</a> — 41 more words. You can also change the grade filter in this generator to "1st Grade." Some parents start the Fry 1–100 list in parallel once their child has solid kindergarten coverage, since the Fry list continues past where Dolch stops.</div>
  </div>

  <div class="faq-item">
    <button class="faq-q"><span class="faq-q-text">How long should daily practice be for a 5-year-old?</span><svg class="faq-chevron" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></button>
    <div class="faq-a">Five to ten minutes is the right range. Shorter is better than longer at this age — attention drops fast. Consistent daily practice of 5 minutes beats an irregular 30-minute session once a week. Morning before school or after dinner tends to work better than bedtime for most kids.</div>
  </div>

  <div class="faq-item">
    <button class="faq-q"><span class="faq-q-text">Does recognition need to be instant?</span><svg class="faq-chevron" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></button>
    <div class="faq-a">Eventually, yes. "Automatic" means under one to two seconds. In the early weeks, a 3-second pause is fine — the word is still being learned. By the end of kindergarten, instant recognition is the goal. A child who pauses on "they" or "what" in May still needs more practice on those specific words.</div>
  </div>

  <div class="faq-item">
    <button class="faq-q"><span class="faq-q-text">Can I use this for Pre-K words too?</span><svg class="faq-chevron" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></button>
    <div class="faq-a">Yes. Change the Grade filter to "Dolch Pre-K" to see the 40 Pre-K words. This page defaults to the kindergarten group, but all Dolch grades are available in the filter. The <a href="/sight-words-generator/">master Sight Words Generator</a> also lets you mix all grades at once.</div>
  </div>
</div>
<!-- /SLOT:faq -->
```

- [ ] **Step 7: Add who slot**

```html
<!-- SLOT:who -->
<div class="who">
  <h2>Who uses this tool?</h2>
  <div class="uc-grid">
    <div class="uc"><div class="uc-title">Parents of Kindergartners</div><div class="uc-body">Working through the reading list the teacher sent home and want something more engaging than the same flashcard stack every night. Generate a random 10-word set, run Practice Mode during breakfast, and save the words your child misses for next session.</div></div>
    <div class="uc"><div class="uc-title">Kindergarten Teachers</div><div class="uc-body">Build grade-filtered word lists for morning warm-ups, partner reading drills, or take-home practice sheets. Print directly from the browser — no worksheet software or account required.</div></div>
    <div class="uc"><div class="uc-title">Pre-K Teachers Prepping Advanced Students</div><div class="uc-body">When a Pre-K student has mastered the 40 Pre-K words and is ready for more, the kindergarten list is the natural next step. Filter to kindergarten and introduce 2–3 words at a time at the end of the year.</div></div>
    <div class="uc"><div class="uc-title">Homeschool Parents</div><div class="uc-body">Following the Dolch sequence as the backbone of an early reading curriculum without buying a packaged program. Work through the grade bands in order, use the save feature to track trouble words, and run Practice Mode as a daily five-minute drill.</div></div>
  </div>
</div>
<!-- /SLOT:who -->
```

- [ ] **Step 8: Add init slot**

Copy the entire `<!-- SLOT:init --> ... <!-- /SLOT:init -->` block from `template-deploy/tools-src/sight-words-generator.html` verbatim, **with one change only**: find the section at the bottom of the IIFE where `SW.generate()` is called on page load, and replace it with:

```javascript
SW.load().then(function () {
  document.getElementById('ctrl-list').value = 'dolch';
  SW.rebuildGroupSelect();
  document.getElementById('ctrl-group').value = 'kindergarten';
  SW.generate();
});
```

The rest of the IIFE (SW object definition, event listeners, GROUP_OPTS, BADGE_LABEL, etc.) is identical to sight-words-generator.

- [ ] **Step 9: Commit**

```bash
git add template-deploy/tools-src/sight-words-kindergarten.html
git commit -m "feat: add sight-words-kindergarten page"
```

---

## Task 3: Create sight-words-1st-grade.html

**Files:**
- Create: `template-deploy/tools-src/sight-words-1st-grade.html`

- [ ] **Step 1: Copy kindergarten file as base**

```bash
cp "template-deploy/tools-src/sight-words-kindergarten.html" "template-deploy/tools-src/sight-words-1st-grade.html"
```

- [ ] **Step 2: Replace CONFIG**

```html
<!-- CONFIG
{
  "url": "/sight-words-1st-grade/",
  "output": "sight-words-1st-grade.html",
  "type": "tool",
  "more_tools_key": "sight_words_tools",
  "more_tools_title": "More sight words tools",
  "more_tools_subtitle": "Grade-by-grade Dolch and Fry practice"
}
-->
```

- [ ] **Step 3: Replace SLOT:meta**

```html
<!-- SLOT:meta -->
<title>First Grade Sight Words — Dolch List with Audio &amp; Practice Mode | Wordineer</title>
<meta name="description" content="All 41 Dolch First Grade sight words with audio pronunciation and Practice Mode. Generate, drill, and save trouble words — built for parents and 1st grade teachers. Free, no login.">
<meta property="og:title" content="First Grade Sight Words — Dolch List with Audio &amp; Practice Mode | Wordineer">
<meta property="og:description" content="All 41 Dolch First Grade sight words with audio pronunciation and Practice Mode. Free, no login required.">
<meta property="og:url" content="https://wordineer.com/sight-words-1st-grade/">
<meta property="og:type" content="website">
<link rel="canonical" href="https://wordineer.com/sight-words-1st-grade/">
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "WebApplication",
  "name": "First Grade Sight Words",
  "url": "https://wordineer.com/sight-words-1st-grade/",
  "description": "Practice all 41 Dolch First Grade sight words with audio pronunciation and Practice Mode. Free, no login required.",
  "applicationCategory": "EducationApplication",
  "operatingSystem": "Any",
  "offers": { "@type": "Offer", "price": "0" }
}
</script>
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    { "@type": "ListItem", "position": 1, "name": "Wordineer", "item": "https://wordineer.com/" },
    { "@type": "ListItem", "position": 2, "name": "Word Tools", "item": "https://wordineer.com/word-tools/" },
    { "@type": "ListItem", "position": 3, "name": "Sight Words Generator", "item": "https://wordineer.com/sight-words-generator/" },
    { "@type": "ListItem", "position": 4, "name": "First Grade", "item": "https://wordineer.com/sight-words-1st-grade/" }
  ]
}
</script>
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "How many total sight words should a 1st grader know?",
      "acceptedAnswer": { "@type": "Answer", "text": "By the end of 1st grade, children should know all Dolch words from Pre-K through 1st Grade — that's 40 Pre-K words, 52 Kindergarten words, and 41 First Grade words, totaling 133 words. All of them should be automatic: recognized in under two seconds without sounding out." }
    },
    {
      "@type": "Question",
      "name": "What if my 1st grader still struggles with kindergarten words?",
      "acceptedAnswer": { "@type": "Answer", "text": "Go back and fill those gaps first. Change the grade filter to 'Dolch Kindergarten' and identify which words are still causing hesitation. Catching gaps in 1st grade is much easier than fixing them in 3rd. Most 1st graders can cover both kindergarten gaps and new 1st grade words within the same school year." }
    },
    {
      "@type": "Question",
      "name": "How are 1st grade sight words different from kindergarten words?",
      "acceptedAnswer": { "@type": "Answer", "text": "First grade words include more pronouns, verb forms, and relational words — 'her,' 'him,' 'his,' 'them,' 'their,' 'when,' 'how,' 'why.' They also include irregular verbs like 'could,' 'had,' 'were,' and 'knew' that can't be sounded out phonetically. The focus shifts from simple recognition to recognizing words at reading speed." }
    },
    {
      "@type": "Question",
      "name": "Should I focus on Dolch or Fry in 1st grade?",
      "acceptedAnswer": { "@type": "Answer", "text": "Dolch, unless your child's school specifies otherwise. The Dolch grade bands map directly to classroom benchmarks through 3rd grade. The Fry list is a better fit from 3rd grade onward, or when you want to extend beyond what Dolch covers. Both lists are available in this generator's filter." }
    },
    {
      "@type": "Question",
      "name": "How do I make sight word practice less boring for a 6-year-old?",
      "acceptedAnswer": { "@type": "Answer", "text": "Change the format regularly. One session use the generator for random lists; another session write words in shaving cream or sand; another session use Practice Mode as a game where they race to answer before you do. Vary the medium and the format. Short sessions — 5 to 8 minutes — also keep engagement higher than longer ones." }
    },
    {
      "@type": "Question",
      "name": "My child's teacher uses a different word list. Is that a problem?",
      "acceptedAnswer": { "@type": "Answer", "text": "No. Most school lists overlap heavily with Dolch anyway. Practice with the school's list first; use this generator to supplement with any Dolch words the school list doesn't cover. Both are aiming at the same goal: high-frequency words your child can read automatically." }
    }
  ]
}
</script>
<!-- /SLOT:meta -->
```

- [ ] **Step 4: Replace SLOT:hero**

```html
<!-- SLOT:hero -->
<div class="breadcrumb">
  <div class="breadcrumb-inner">
    <a href="/">Wordineer</a>
    <span class="breadcrumb-sep">›</span>
    <a href="/word-tools/">Word Tools</a>
    <span class="breadcrumb-sep">›</span>
    <a href="/sight-words-generator/">Sight Words Generator</a>
    <span class="breadcrumb-sep">›</span>
    <span aria-current="page">1st Grade</span>
  </div>
</div>
<div class="hero">
  <div class="hero-badge">41 Words · Audio · Practice Mode · Free</div>
  <h1>First Grade Sight Words</h1>
  <p>The complete Dolch 1st Grade list — 41 words that push early readers from letter-by-letter decoding to real reading fluency. Hear each word aloud, save the hard ones, and drill with Practice Mode. No account needed.</p>
</div>
<!-- /SLOT:hero -->
```

- [ ] **Step 5: Replace SLOT:explainer**

```html
<!-- SLOT:explainer -->
<div class="explainer">

  <div class="grade-nav">
    <span class="grade-nav-label">Grade:</span>
    <a href="/sight-words-generator/">All Grades</a>
    <a href="/sight-words-kindergarten/">Kindergarten</a>
    <span class="grade-nav-current">1st Grade</span>
    <a href="/sight-words-2nd-grade/">2nd Grade</a>
    <a href="/sight-words-3rd-grade/">3rd Grade</a>
  </div>

  <h2>All 41 Dolch First Grade Sight Words</h2>
  <div class="word-chips">
    <span class="word-chip">after</span><span class="word-chip">again</span><span class="word-chip">an</span><span class="word-chip">any</span><span class="word-chip">as</span><span class="word-chip">ask</span><span class="word-chip">by</span><span class="word-chip">could</span><span class="word-chip">every</span><span class="word-chip">fly</span><span class="word-chip">from</span><span class="word-chip">give</span><span class="word-chip">going</span><span class="word-chip">had</span><span class="word-chip">has</span><span class="word-chip">her</span><span class="word-chip">him</span><span class="word-chip">his</span><span class="word-chip">how</span><span class="word-chip">just</span><span class="word-chip">know</span><span class="word-chip">let</span><span class="word-chip">live</span><span class="word-chip">may</span><span class="word-chip">of</span><span class="word-chip">old</span><span class="word-chip">once</span><span class="word-chip">open</span><span class="word-chip">over</span><span class="word-chip">put</span><span class="word-chip">round</span><span class="word-chip">some</span><span class="word-chip">stop</span><span class="word-chip">take</span><span class="word-chip">thank</span><span class="word-chip">them</span><span class="word-chip">then</span><span class="word-chip">think</span><span class="word-chip">walk</span><span class="word-chip">were</span><span class="word-chip">when</span>
  </div>

  <h2>What makes 1st grade sight words different</h2>
  <p>The Dolch Kindergarten list is mostly short, simple words — "be," "do," "go," "no," "he," "she." The 1st grade list steps up. You get irregular verb forms ("could," "had," "were," "went"), pronouns ("him," "her," "his," "them"), and relational words that can't be pictured or sounded out ("just," "once," "some," "every"). These are the words that hold sentences together, and they don't behave phonetically — "could" doesn't sound like it looks, and "of" sounds nothing like it's spelled.</p>
  <p>By the end of 1st grade, the cumulative total is 133 Dolch words: the 40 from Pre-K, the 52 from Kindergarten, and these 41. That's the benchmark. At that count, a child should be able to get through most early reader books — the kind with 1–3 sentences per page — without stopping to decode familiar words. The sight words become invisible infrastructure that lets reading happen.</p>

  <h2>How many sight words should a 1st grader know?</h2>
  <p>All 133 Dolch words through 1st Grade, by June. That's the full cumulative count — Pre-K through 1st. Not just the 41 new ones: the earlier words need to be solid too, because 1st grade reading piles all of them together on every page.</p>
  <p>The test isn't just "can they read this word" — it's "can they read this word in under two seconds, in a sentence, without breaking the flow." A child who hesitates on "was" or "they" in the middle of a sentence is still working on automaticity, even if they get it right. Use Practice Mode with a light time pressure to build speed, not just accuracy.</p>
  <p>If you notice gaps in kindergarten words during 1st grade practice, address those first. Catching them early in 1st grade is straightforward. Waiting until 3rd grade to fix a gap from kindergarten is harder and slower.</p>

  <h2>Teaching 1st grade sight words: strategies that work</h2>
  <p>By 1st grade, the introduction technique from kindergarten (say it, spell it, write it, find it) still works. But the emphasis shifts. Speed becomes more important. Recognition in isolation isn't the finish line — recognition at reading pace in continuous text is.</p>
  <p>A few adjustments that help at this level:</p>
  <ul>
    <li><strong>Speed drills.</strong> Run Practice Mode and have your child try to answer before you do. Or time them: how many words in 60 seconds? A little friendly pressure builds the automaticity that isolated practice doesn't.</li>
    <li><strong>Reading in context.</strong> Don't only practice with the generator. Read books together and point out 1st grade sight words when they appear. "There's 'could' — you know that one." Connecting practice to real reading reinforces why it matters.</li>
    <li><strong>Watch the confusable pairs.</strong> "Them" and "then," "his" and "him" and "her," "had" and "has" — kids mix these up in 1st grade. Practice them in pairs deliberately, not just individually.</li>
    <li><strong>Self-correction.</strong> If your child reads a word wrong in a book, pause and ask "does that sound right?" before correcting them. Building the habit of checking themselves is a reading skill on its own.</li>
  </ul>
  <p>If a child is still struggling with kindergarten words in the fall of 1st grade, don't push new 1st grade words yet. Use this generator filtered to "Dolch Kindergarten" and address those gaps over a few weeks. The 1st grade words aren't going anywhere.</p>

  <h2>A 4-week plan for 1st graders</h2>
  <p><strong>Week 1:</strong> Diagnostic. Run through all 133 cumulative Dolch words (use the "All Grades" filter in the generator, then narrow to each group one at a time). Save any word that causes hesitation, regardless of grade. You now have a targeted list.</p>
  <p><strong>Week 2:</strong> Work through the targeted words from Week 1. Two to four words per day. Continue reading out loud together every evening, and pause on targeted words when they appear in text.</p>
  <p><strong>Week 3:</strong> Introduce any new 1st Grade words not yet covered. Run Practice Mode daily. This week the goal is response time — under two seconds per word.</p>
  <p><strong>Week 4:</strong> Full list drills with the generator on random shuffle. Pick up a new early reader book and track how smoothly your child reads through it. Sight word automaticity should be making the reading noticeably easier than it was four weeks ago.</p>

  <h2>How to use this tool</h2>
  <p>The generator is pre-set to Dolch 1st Grade. Hit Generate (or Space) for a fresh set. Change the grade filter anytime — switching to Kindergarten or Pre-K to check earlier words works the same way. Click the speaker icon to hear any word. Save trouble words with the heart. Practice Mode shows one word at a time for drilling. Everything saves between sessions so you don't lose your saved word list when you close the browser.</p>

</div>
<!-- /SLOT:explainer -->
```

- [ ] **Step 6: Replace SLOT:faq**

```html
<!-- SLOT:faq -->
<div class="faq">
  <h2 class="faq-title">Frequently asked questions</h2>

  <div class="faq-item open">
    <button class="faq-q"><span class="faq-q-text">How many total sight words should a 1st grader know?</span><svg class="faq-chevron" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></button>
    <div class="faq-a">By end of 1st grade: all 133 Dolch words from Pre-K through 1st Grade. That's 40 Pre-K + 52 Kindergarten + 41 First Grade words. All of them should be automatic — recognized in under two seconds without sounding out.</div>
  </div>

  <div class="faq-item">
    <button class="faq-q"><span class="faq-q-text">What if my 1st grader still struggles with kindergarten words?</span><svg class="faq-chevron" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></button>
    <div class="faq-a">Go back and fill those gaps first. Change the grade filter to "Dolch Kindergarten" and identify which words still cause hesitation. Catching gaps in 1st grade is much easier than fixing them later. Most 1st graders can cover kindergarten gaps and new 1st grade words within the same school year.</div>
  </div>

  <div class="faq-item">
    <button class="faq-q"><span class="faq-q-text">How are 1st grade words different from kindergarten words?</span><svg class="faq-chevron" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></button>
    <div class="faq-a">First grade words include more pronouns (her, him, his, them), irregular verb forms (could, had, were), and relational words (just, once, every, some) that can't be decoded phonetically. They're harder to picture and harder to sound out, which is why explicit practice matters more at this level than it did in kindergarten.</div>
  </div>

  <div class="faq-item">
    <button class="faq-q"><span class="faq-q-text">Should I focus on Dolch or Fry in 1st grade?</span><svg class="faq-chevron" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></button>
    <div class="faq-a">Dolch, unless your child's teacher specifies otherwise. The Dolch grade bands align with classroom benchmarks through 3rd grade. The Fry list is a better framework from 3rd grade onward, when kids are ready to extend beyond the Dolch service words.</div>
  </div>

  <div class="faq-item">
    <button class="faq-q"><span class="faq-q-text">How do I make practice less boring for a 6-year-old?</span><svg class="faq-chevron" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></button>
    <div class="faq-a">Change the format. One session use the generator for random lists, another session write words in shaving cream, another session race against each other in Practice Mode. Rotate the medium every few days and keep sessions under 8 minutes. Novelty and brevity beat length and repetition for this age group.</div>
  </div>

  <div class="faq-item">
    <button class="faq-q"><span class="faq-q-text">My child's teacher uses a different list. Is that a problem?</span><svg class="faq-chevron" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></button>
    <div class="faq-a">No. Most school lists overlap heavily with Dolch. Practice the school list first; use this generator to fill in any Dolch words the school list doesn't cover. Both are targeting the same goal: high-frequency words your child reads automatically.</div>
  </div>
</div>
<!-- /SLOT:faq -->
```

- [ ] **Step 7: Replace SLOT:who**

```html
<!-- SLOT:who -->
<div class="who">
  <h2>Who uses this tool?</h2>
  <div class="uc-grid">
    <div class="uc"><div class="uc-title">Parents of 1st Graders</div><div class="uc-body">Supporting an early reader at home and want a fast way to generate targeted practice lists. Filter to the 1st grade group, generate 12 words, run Practice Mode before bedtime — ten minutes, done.</div></div>
    <div class="uc"><div class="uc-title">1st Grade Teachers</div><div class="uc-body">Build word wall rotations, morning warm-up lists, or take-home practice sheets in seconds. Filter to the current unit's grade group and print directly from the browser — no worksheet software required.</div></div>
    <div class="uc"><div class="uc-title">Reading Tutors</div><div class="uc-body">Quickly run a diagnostic across Dolch grade groups to find gaps. Save the trouble words, then drill them specifically with Practice Mode during the session — no setup, no prep time.</div></div>
    <div class="uc"><div class="uc-title">Homeschool Educators</div><div class="uc-body">Following the Dolch sequence as the backbone of a 1st grade reading curriculum. Work through the grade bands in order, use saved words to track trouble spots, and run the generator daily for variety.</div></div>
  </div>
</div>
<!-- /SLOT:who -->
```

- [ ] **Step 8: Update init slot grade default**

In the SLOT:init (copied from kindergarten), change the grade default line:

```javascript
document.getElementById('ctrl-group').value = '1st';
```

- [ ] **Step 9: Commit**

```bash
git add template-deploy/tools-src/sight-words-1st-grade.html
git commit -m "feat: add sight-words-1st-grade page"
```

---

## Task 4: Create sight-words-2nd-grade.html

**Files:**
- Create: `template-deploy/tools-src/sight-words-2nd-grade.html`

- [ ] **Step 1: Copy and update CONFIG**

```bash
cp "template-deploy/tools-src/sight-words-kindergarten.html" "template-deploy/tools-src/sight-words-2nd-grade.html"
```

Replace CONFIG:
```html
<!-- CONFIG
{
  "url": "/sight-words-2nd-grade/",
  "output": "sight-words-2nd-grade.html",
  "type": "tool",
  "more_tools_key": "sight_words_tools",
  "more_tools_title": "More sight words tools",
  "more_tools_subtitle": "Grade-by-grade Dolch and Fry practice"
}
-->
```

- [ ] **Step 2: Replace SLOT:meta**

```html
<!-- SLOT:meta -->
<title>Second Grade Sight Words — Dolch List with Audio &amp; Practice Mode | Wordineer</title>
<meta name="description" content="All 46 Dolch Second Grade sight words with audio pronunciation and Practice Mode. Generate, drill, and save trouble words — built for parents and 2nd grade teachers. Free, no login.">
<meta property="og:title" content="Second Grade Sight Words — Dolch List with Audio &amp; Practice Mode | Wordineer">
<meta property="og:description" content="All 46 Dolch Second Grade sight words with audio and Practice Mode. Free, no login required.">
<meta property="og:url" content="https://wordineer.com/sight-words-2nd-grade/">
<meta property="og:type" content="website">
<link rel="canonical" href="https://wordineer.com/sight-words-2nd-grade/">
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "WebApplication",
  "name": "Second Grade Sight Words",
  "url": "https://wordineer.com/sight-words-2nd-grade/",
  "description": "Practice all 46 Dolch Second Grade sight words with audio pronunciation and Practice Mode. Free, no login required.",
  "applicationCategory": "EducationApplication",
  "operatingSystem": "Any",
  "offers": { "@type": "Offer", "price": "0" }
}
</script>
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    { "@type": "ListItem", "position": 1, "name": "Wordineer", "item": "https://wordineer.com/" },
    { "@type": "ListItem", "position": 2, "name": "Word Tools", "item": "https://wordineer.com/word-tools/" },
    { "@type": "ListItem", "position": 3, "name": "Sight Words Generator", "item": "https://wordineer.com/sight-words-generator/" },
    { "@type": "ListItem", "position": 4, "name": "Second Grade", "item": "https://wordineer.com/sight-words-2nd-grade/" }
  ]
}
</script>
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "How many sight words should a 2nd grader know by end of year?",
      "acceptedAnswer": { "@type": "Answer", "text": "By June of 2nd grade, children should know all 179 Dolch words from Pre-K through 2nd Grade — cumulative. That's 40 Pre-K, 52 Kindergarten, 41 First Grade, and 46 Second Grade words. All should be truly automatic: under two seconds, no sounding out." }
    },
    {
      "@type": "Question",
      "name": "At what point should sight words be automatic vs. sounded out?",
      "acceptedAnswer": { "@type": "Answer", "text": "Sight words should never be sounded out — that's the whole point. If your child is still sounding out 'because' or 'always' in 2nd grade, those words need more drill time. The goal is immediate visual recognition, not phonetic decoding. Use Practice Mode to measure speed and identify words that aren't automatic yet." }
    },
    {
      "@type": "Question",
      "name": "What if my 2nd grader has gaps in the kindergarten or 1st grade lists?",
      "acceptedAnswer": { "@type": "Answer", "text": "Address them directly. Change the grade filter to Kindergarten or 1st Grade and run through those words. Save any that cause hesitation and drill them for one to two weeks before returning to the 2nd grade list. Gaps compound — a shaky 'were' or 'could' will slow reading in 2nd grade just as much as an unknown 2nd grade word." }
    },
    {
      "@type": "Question",
      "name": "How do sight words connect to spelling in 2nd grade?",
      "acceptedAnswer": { "@type": "Answer", "text": "They're related but different skills. A child can read 'because' automatically but still misspell it in writing — the visual recognition path and the spelling retrieval path are separate. By 2nd grade, it's worth practicing both: reading with this tool and writing the words by hand separately. If your child misspells common sight words in their written work, that's a gap worth addressing." }
    },
    {
      "@type": "Question",
      "name": "My child reads sight words in isolation but forgets them in a book. Why?",
      "acceptedAnswer": { "@type": "Answer", "text": "Because reading in context requires splitting attention across meaning, syntax, and decoding simultaneously. A word that's automatic in isolation may slow a child down in text if they haven't built that automaticity under load. Reading books aloud together and pointing to sight words in context helps bridge this gap. The word needs to be automatic in both settings." }
    },
    {
      "@type": "Question",
      "name": "Is Dolch or Fry more relevant in 2nd grade?",
      "acceptedAnswer": { "@type": "Answer", "text": "Dolch is still the right framework through 2nd grade — the grade bands map directly to classroom expectations. After your child completes the 2nd grade Dolch list, the Fry list (available in the filter on this generator) is a natural next step toward 3rd grade and beyond." }
    }
  ]
}
</script>
<!-- /SLOT:meta -->
```

- [ ] **Step 3: Replace SLOT:hero**

```html
<!-- SLOT:hero -->
<div class="breadcrumb">
  <div class="breadcrumb-inner">
    <a href="/">Wordineer</a>
    <span class="breadcrumb-sep">›</span>
    <a href="/word-tools/">Word Tools</a>
    <span class="breadcrumb-sep">›</span>
    <a href="/sight-words-generator/">Sight Words Generator</a>
    <span class="breadcrumb-sep">›</span>
    <span aria-current="page">2nd Grade</span>
  </div>
</div>
<div class="hero">
  <div class="hero-badge">46 Words · Audio · Practice Mode · Free</div>
  <h1>Second Grade Sight Words</h1>
  <p>The complete Dolch 2nd Grade list — 46 words that bridge early readers to independent reading. These are longer, more abstract words where automaticity matters more than ever. Audio, Practice Mode, save feature — no account required.</p>
</div>
<!-- /SLOT:hero -->
```

- [ ] **Step 4: Replace SLOT:explainer**

```html
<!-- SLOT:explainer -->
<div class="explainer">

  <div class="grade-nav">
    <span class="grade-nav-label">Grade:</span>
    <a href="/sight-words-generator/">All Grades</a>
    <a href="/sight-words-kindergarten/">Kindergarten</a>
    <a href="/sight-words-1st-grade/">1st Grade</a>
    <span class="grade-nav-current">2nd Grade</span>
    <a href="/sight-words-3rd-grade/">3rd Grade</a>
  </div>

  <h2>All 46 Dolch Second Grade Sight Words</h2>
  <div class="word-chips">
    <span class="word-chip">always</span><span class="word-chip">around</span><span class="word-chip">because</span><span class="word-chip">been</span><span class="word-chip">before</span><span class="word-chip">best</span><span class="word-chip">both</span><span class="word-chip">buy</span><span class="word-chip">call</span><span class="word-chip">cold</span><span class="word-chip">does</span><span class="word-chip">don't</span><span class="word-chip">fast</span><span class="word-chip">first</span><span class="word-chip">five</span><span class="word-chip">found</span><span class="word-chip">gave</span><span class="word-chip">goes</span><span class="word-chip">green</span><span class="word-chip">its</span><span class="word-chip">made</span><span class="word-chip">many</span><span class="word-chip">off</span><span class="word-chip">or</span><span class="word-chip">pull</span><span class="word-chip">read</span><span class="word-chip">right</span><span class="word-chip">sing</span><span class="word-chip">sit</span><span class="word-chip">sleep</span><span class="word-chip">tell</span><span class="word-chip">their</span><span class="word-chip">these</span><span class="word-chip">those</span><span class="word-chip">upon</span><span class="word-chip">us</span><span class="word-chip">use</span><span class="word-chip">very</span><span class="word-chip">wash</span><span class="word-chip">which</span><span class="word-chip">why</span><span class="word-chip">wish</span><span class="word-chip">work</span><span class="word-chip">would</span><span class="word-chip">write</span><span class="word-chip">your</span>
  </div>

  <h2>Second grade sight words: what changes at this level</h2>
  <p>The 46 Dolch Second Grade words are noticeably longer and more abstract than what came before. "Because," "always," "would," "which," "their," "those" — these aren't words you can picture or demonstrate with an action. They're the connective tissue of written language, the words that hold clauses and ideas together.</p>
  <p>By the end of 2nd grade, the cumulative total is 179 Dolch words: Pre-K through 2nd Grade. At this point, a child should be reading early chapter books — things like <em>Magic Tree House</em> or early <em>Junie B. Jones</em> — with these words serving as reliable anchors in every sentence. When sight words are truly automatic, reading becomes less like decoding and more like understanding.</p>
  <p>The challenge at this level isn't recognition — most 2nd graders can read "because" and "always" correctly. The challenge is automaticity: recognition without any visible effort, in the middle of a sentence, while tracking meaning. A child who slows down slightly on "would" in every sentence is not yet automatic on that word, even if they always get it right.</p>

  <h2>How many sight words should a 2nd grader know?</h2>
  <p>All 179 cumulative Dolch words by June — Pre-K through 2nd Grade. More importantly, all 179 should be automatic. Not "mostly right" or "gets it with a pause" — truly instant recognition.</p>
  <p>To test this at home: open a book your child knows and page through it quickly, pointing to sight words one at a time. Any word that produces a half-second hesitation is still in progress. Save those in the generator and work on them specifically. The list of hesitations will be shorter than you think — usually a handful of words, not the whole list.</p>
  <p>If you notice gaps from earlier grade lists (kindergarten or 1st grade words that still cause hesitation), don't ignore them to push forward. Use the grade filter to go back and drill those words for a week or two. Cumulative gaps get harder to close as the reading demands increase.</p>

  <h2>Teaching 2nd grade sight words: the automaticity goal</h2>
  <p>By 2nd grade, the introduction technique matters less than the drilling technique. Your child probably already knows what "because" means. The job now is making that recognition instantaneous and effortless — under load, in text, without breaking the reading flow.</p>
  <p>What works at this level:</p>
  <ul>
    <li><strong>Timed sessions.</strong> How many words in 30 seconds? The time pressure simulates the reading experience better than leisurely flashcard review. Practice Mode is good for this — keep a count and try to beat it next session.</li>
    <li><strong>Reading passages, not just word lists.</strong> Give your child a paragraph to read aloud. Track which words cause any hesitation. That list — not the full Dolch list — is what to drill this week.</li>
    <li><strong>"Don't" needs special attention.</strong> Contractions with apostrophes look different to young readers. "Don't" is on the 2nd grade list. Treat it explicitly as a unit, not as "do" + "not."</li>
    <li><strong>"Its" vs. "it's."</strong> "Its" is on the Dolch list; the possessive-vs-contraction distinction is confusing. For sight word purposes, just drill "its" as a unit. Grammar distinctions can wait.</li>
    <li><strong>Check writing, not just reading.</strong> By 2nd grade, sight words should be showing up in your child's writing too. If they write "becuse" or "ther" (for "their"), the reading recognition and the spelling are not yet fully connected. Practice both.</li>
  </ul>

  <h2>A 4-week schedule for 2nd graders</h2>
  <p><strong>Week 1:</strong> Full diagnostic. Run through all Dolch groups one at a time — not just 2nd grade, but Pre-K, Kindergarten, and 1st too. Save every word that produces any hesitation. This is your work list for the month.</p>
  <p><strong>Week 2:</strong> Drill the saved words across all grades. Two sessions per day, 5–8 minutes each. One session with the generator (random list), one with Practice Mode for speed.</p>
  <p><strong>Week 3:</strong> Add new 2nd grade words not yet introduced. Continue drilling trouble words from Week 1. By end of week, your child should have been exposed to all 46 words at least several times each.</p>
  <p><strong>Week 4:</strong> Reading in context. Pick up a chapter book your child is currently reading and track sight words on a few pages. The measure of success isn't how they do in Practice Mode — it's how smoothly they read continuous text. Fluent reading that doesn't slow on sight words is the real benchmark.</p>

  <h2>How to use this generator</h2>
  <p>The tool is pre-set to Dolch 2nd Grade. Generate a random set with the button or Space bar. Change the grade filter anytime to review earlier grades — the Dolch Kindergarten and 1st Grade groups are worth revisiting regularly. Click the speaker icon to hear words aloud. Save trouble words with the heart. Run Practice Mode for speed drills. Saved words persist between sessions in browser local storage.</p>

</div>
<!-- /SLOT:explainer -->
```

- [ ] **Step 5: Replace SLOT:faq**

```html
<!-- SLOT:faq -->
<div class="faq">
  <h2 class="faq-title">Frequently asked questions</h2>

  <div class="faq-item open">
    <button class="faq-q"><span class="faq-q-text">How many sight words should a 2nd grader know by end of year?</span><svg class="faq-chevron" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></button>
    <div class="faq-a">By June, all 179 Dolch words from Pre-K through 2nd Grade — cumulative. That's 40 + 52 + 41 + 46. All should be automatic: under two seconds, no sounding out, no hesitation.</div>
  </div>

  <div class="faq-item">
    <button class="faq-q"><span class="faq-q-text">Should sight words be automatic or is sounding out okay?</span><svg class="faq-chevron" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></button>
    <div class="faq-a">Automatic. Sounding out sight words defeats the purpose — these are words specifically chosen because phonics doesn't work reliably on them. If your child is sounding out "because" or "always" in 2nd grade, those words need more direct drill. Use Practice Mode to build speed.</div>
  </div>

  <div class="faq-item">
    <button class="faq-q"><span class="faq-q-text">What if my 2nd grader has gaps in earlier lists?</span><svg class="faq-chevron" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></button>
    <div class="faq-a">Address them first. Change the grade filter to Kindergarten or 1st Grade and run a quick diagnostic. Save anything that causes hesitation and drill those for a week or two before returning to 2nd grade words. Gaps from earlier grades slow reading just as much as unknown 2nd grade words.</div>
  </div>

  <div class="faq-item">
    <button class="faq-q"><span class="faq-q-text">How do sight words connect to spelling in 2nd grade?</span><svg class="faq-chevron" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></button>
    <div class="faq-a">They're related but separate. A child can read "because" automatically but still misspell it in writing — the recognition path and the spelling path are different. By 2nd grade, it's worth practicing both: use this tool for reading recognition, and have your child write sight words by hand separately. Misspelled sight words in written work are a gap worth fixing.</div>
  </div>

  <div class="faq-item">
    <button class="faq-q"><span class="faq-q-text">My child reads sight words correctly but forgets them mid-sentence. Why?</span><svg class="faq-chevron" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></button>
    <div class="faq-a">Because reading in context splits attention across meaning, syntax, and word recognition simultaneously. A word that's automatic in isolation may slow things down in a sentence if it hasn't been fully automated under that cognitive load. Reading books aloud together and pausing on sight words in context helps close this gap.</div>
  </div>

  <div class="faq-item">
    <button class="faq-q"><span class="faq-q-text">Is Dolch or Fry more relevant in 2nd grade?</span><svg class="faq-chevron" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></button>
    <div class="faq-a">Dolch is still the right framework through 2nd grade. Once your child completes the 2nd grade Dolch list, the Fry list is a natural extension — change the List filter in this generator to "Fry" to access Fry words by frequency band.</div>
  </div>
</div>
<!-- /SLOT:faq -->
```

- [ ] **Step 6: Replace SLOT:who**

```html
<!-- SLOT:who -->
<div class="who">
  <h2>Who uses this tool?</h2>
  <div class="uc-grid">
    <div class="uc"><div class="uc-title">Parents of 2nd Graders</div><div class="uc-body">Supporting a reader making the jump to chapter books. Generate a 12-word set from the 2nd grade group, run Practice Mode twice, and check which words still cause a pause. Those are the only ones that need more work.</div></div>
    <div class="uc"><div class="uc-title">2nd Grade Teachers</div><div class="uc-body">Track progress across the full cumulative Dolch list and identify which grade-level gaps remain by mid-year. Generate targeted lists for small-group intervention or take-home sheets — print directly from the browser.</div></div>
    <div class="uc"><div class="uc-title">Reading Interventionists</div><div class="uc-body">Run a fast diagnostic across multiple Dolch groups in one session. Save all hesitation words to a running list, then use Practice Mode for targeted drill. The grade filter makes it easy to pinpoint exactly where gaps sit.</div></div>
    <div class="uc"><div class="uc-title">Homeschool Educators</div><div class="uc-body">Building fluency before introducing longer chapter books. The 2nd grade Dolch words are the last group before the vocabulary load increases significantly — getting these automatic now makes a measurable difference in reading pace.</div></div>
  </div>
</div>
<!-- /SLOT:who -->
```

- [ ] **Step 7: Update init grade default**

In SLOT:init, change:
```javascript
document.getElementById('ctrl-group').value = '2nd';
```

- [ ] **Step 8: Commit**

```bash
git add template-deploy/tools-src/sight-words-2nd-grade.html
git commit -m "feat: add sight-words-2nd-grade page"
```

---

## Task 5: Create sight-words-3rd-grade.html

**Files:**
- Create: `template-deploy/tools-src/sight-words-3rd-grade.html`

- [ ] **Step 1: Copy and update CONFIG**

```bash
cp "template-deploy/tools-src/sight-words-kindergarten.html" "template-deploy/tools-src/sight-words-3rd-grade.html"
```

Replace CONFIG:
```html
<!-- CONFIG
{
  "url": "/sight-words-3rd-grade/",
  "output": "sight-words-3rd-grade.html",
  "type": "tool",
  "more_tools_key": "sight_words_tools",
  "more_tools_title": "More sight words tools",
  "more_tools_subtitle": "Grade-by-grade Dolch and Fry practice"
}
-->
```

- [ ] **Step 2: Replace SLOT:meta**

```html
<!-- SLOT:meta -->
<title>Third Grade Sight Words — Dolch List with Audio &amp; Practice Mode | Wordineer</title>
<meta name="description" content="All 41 Dolch Third Grade sight words with audio pronunciation and Practice Mode. The final Dolch grade band — drill, save, and print. Free, no login.">
<meta property="og:title" content="Third Grade Sight Words — Dolch List with Audio &amp; Practice Mode | Wordineer">
<meta property="og:description" content="All 41 Dolch Third Grade sight words with audio and Practice Mode. Free, no login required.">
<meta property="og:url" content="https://wordineer.com/sight-words-3rd-grade/">
<meta property="og:type" content="website">
<link rel="canonical" href="https://wordineer.com/sight-words-3rd-grade/">
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "WebApplication",
  "name": "Third Grade Sight Words",
  "url": "https://wordineer.com/sight-words-3rd-grade/",
  "description": "Practice all 41 Dolch Third Grade sight words with audio pronunciation and Practice Mode. Free, no login required.",
  "applicationCategory": "EducationApplication",
  "operatingSystem": "Any",
  "offers": { "@type": "Offer", "price": "0" }
}
</script>
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    { "@type": "ListItem", "position": 1, "name": "Wordineer", "item": "https://wordineer.com/" },
    { "@type": "ListItem", "position": 2, "name": "Word Tools", "item": "https://wordineer.com/word-tools/" },
    { "@type": "ListItem", "position": 3, "name": "Sight Words Generator", "item": "https://wordineer.com/sight-words-generator/" },
    { "@type": "ListItem", "position": 4, "name": "Third Grade", "item": "https://wordineer.com/sight-words-3rd-grade/" }
  ]
}
</script>
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Do 3rd graders still need to practice sight words?",
      "acceptedAnswer": { "@type": "Answer", "text": "Yes — the 3rd grade Dolch list is the final grade band, and some of these words have irregular pronunciations that trip kids up ('laugh,' 'eight,' 'shall'). Beyond the 3rd grade list, it's worth checking for gaps in earlier lists that may have been glossed over in previous years." }
    },
    {
      "@type": "Question",
      "name": "How many Dolch words should a 3rd grader know total?",
      "acceptedAnswer": { "@type": "Answer", "text": "By end of 3rd grade, all 220 Dolch service words — the complete Pre-K through 3rd Grade set. That covers the 40 Pre-K, 52 Kindergarten, 41 First Grade, 46 Second Grade, and 41 Third Grade words. After this, most programs shift to Fry words for continued vocabulary development." }
    },
    {
      "@type": "Question",
      "name": "What comes after the Dolch 3rd grade list?",
      "acceptedAnswer": { "@type": "Answer", "text": "The Fry list. Change the List filter in this generator to 'Fry' and start with the 1–100 group. The Fry list continues to 1,000 words and covers the academic vocabulary that Dolch doesn't. The first 300 Fry words overlap significantly with Dolch, so the transition is gradual." }
    },
    {
      "@type": "Question",
      "name": "My 3rd grader reads fine but misspells sight words. Is that normal?",
      "acceptedAnswer": { "@type": "Answer", "text": "Yes, it's common. Reading recognition and spelling are separate skills. A child can read 'laugh' instantly but spell it 'laf' in writing. By 3rd grade, spelling sight words correctly in writing is a reasonable goal — practice both reading with this tool and writing words by hand separately." }
    },
    {
      "@type": "Question",
      "name": "How do sight words relate to reading fluency in 3rd grade?",
      "acceptedAnswer": { "@type": "Answer", "text": "3rd grade is when fluent reading — reading in phrases rather than word by word — typically develops. Sight word automaticity is a prerequisite. If a child is still decoding or hesitating on words like 'thought,' 'because,' or 'could,' it interrupts the phrasing that makes fluent reading possible." }
    },
    {
      "@type": "Question",
      "name": "Should I move my 3rd grader to the Fry list?",
      "acceptedAnswer": { "@type": "Answer", "text": "Once they have all 220 Dolch service words solid, yes. Use the grade filter on this generator to run a quick diagnostic across all Dolch groups first. Any hesitations are worth addressing before moving on. If everything looks automatic, switch the List filter to Fry and start with the 1–100 group." }
    }
  ]
}
</script>
<!-- /SLOT:meta -->
```

- [ ] **Step 3: Replace SLOT:hero**

```html
<!-- SLOT:hero -->
<div class="breadcrumb">
  <div class="breadcrumb-inner">
    <a href="/">Wordineer</a>
    <span class="breadcrumb-sep">›</span>
    <a href="/word-tools/">Word Tools</a>
    <span class="breadcrumb-sep">›</span>
    <a href="/sight-words-generator/">Sight Words Generator</a>
    <span class="breadcrumb-sep">›</span>
    <span aria-current="page">3rd Grade</span>
  </div>
</div>
<div class="hero">
  <div class="hero-badge">41 Words · Audio · Practice Mode · Free</div>
  <h1>Third Grade Sight Words</h1>
  <p>The final Dolch grade band — 41 words that complete the 220-word service vocabulary every fluent reader should have automatic. Drill with audio and Practice Mode, check for gaps in earlier grades, and build toward independent reading. No account needed.</p>
</div>
<!-- /SLOT:hero -->
```

- [ ] **Step 4: Replace SLOT:explainer**

```html
<!-- SLOT:explainer -->
<div class="explainer">

  <div class="grade-nav">
    <span class="grade-nav-label">Grade:</span>
    <a href="/sight-words-generator/">All Grades</a>
    <a href="/sight-words-kindergarten/">Kindergarten</a>
    <a href="/sight-words-1st-grade/">1st Grade</a>
    <a href="/sight-words-2nd-grade/">2nd Grade</a>
    <span class="grade-nav-current">3rd Grade</span>
  </div>

  <h2>All 41 Dolch Third Grade Sight Words</h2>
  <div class="word-chips">
    <span class="word-chip">about</span><span class="word-chip">better</span><span class="word-chip">bring</span><span class="word-chip">carry</span><span class="word-chip">clean</span><span class="word-chip">cut</span><span class="word-chip">done</span><span class="word-chip">draw</span><span class="word-chip">drink</span><span class="word-chip">eight</span><span class="word-chip">fall</span><span class="word-chip">far</span><span class="word-chip">full</span><span class="word-chip">got</span><span class="word-chip">grow</span><span class="word-chip">hold</span><span class="word-chip">hot</span><span class="word-chip">hurt</span><span class="word-chip">if</span><span class="word-chip">keep</span><span class="word-chip">kind</span><span class="word-chip">laugh</span><span class="word-chip">light</span><span class="word-chip">long</span><span class="word-chip">much</span><span class="word-chip">myself</span><span class="word-chip">never</span><span class="word-chip">only</span><span class="word-chip">own</span><span class="word-chip">pick</span><span class="word-chip">seven</span><span class="word-chip">shall</span><span class="word-chip">show</span><span class="word-chip">six</span><span class="word-chip">small</span><span class="word-chip">start</span><span class="word-chip">ten</span><span class="word-chip">today</span><span class="word-chip">together</span><span class="word-chip">try</span><span class="word-chip">warm</span>
  </div>

  <h2>Third grade sight words: the final Dolch group</h2>
  <p>The Dolch 3rd Grade list is the last grade band in the Dolch system. After these 41 words, most reading programs shift to the Fry list or to subject-area vocabulary. Completing all 220 Dolch service words means a child has automatic recognition of the most common words in the English language — the words that make up the backbone of nearly everything they'll read through elementary school and beyond.</p>
  <p>Some of these words have irregular pronunciations that trip kids up even in 3rd grade: "laugh" sounds nothing like it looks; "eight" has a silent combination that defies phonics rules; "shall" is uncommon enough in spoken language that many kids haven't heard it often. These aren't words to gloss over because they seem basic — a 3rd grader who hesitates on "laugh" mid-sentence is still not automatic on that word.</p>
  <p>Third grade is also the year when most kids hit a critical inflection point in reading. They start reading in phrases rather than word by word, and comprehension deepens as a result. Sight word automaticity is a prerequisite for that shift — if any of the 220 Dolch words are still causing hesitation, they act as speed bumps in every page of text.</p>

  <h2>How many sight words should a 3rd grader know?</h2>
  <p>By June of 3rd grade: all 220 Dolch service words — the complete cumulative set from Pre-K through 3rd Grade. These 41 words plus all 179 from earlier grades. Every one of them should be automatic: under two seconds, no sounding out, no visible effort in continuous text.</p>
  <p>Before drilling 3rd grade words, it's worth running a diagnostic across all earlier Dolch groups. Use the grade filter in this generator to check Pre-K, Kindergarten, 1st, and 2nd grade words one group at a time. Save any word that produces hesitation, regardless of the grade it came from. A gap in the kindergarten list is just as worth fixing in 3rd grade as a gap in the 3rd grade list.</p>
  <p>After the 220 Dolch words are solid, the Fry list is the natural next step. The first 300 Fry words overlap heavily with Dolch, but Fry continues to 1,000 words and covers more academic vocabulary. Change the List filter in this generator to "Fry" to begin that progression.</p>

  <h2>Teaching 3rd grade sight words</h2>
  <p>By 3rd grade, the methods matter less than the consistency. Kids this age can practice more independently — Practice Mode works well as a self-directed drill. The main shifts at this level:</p>
  <ul>
    <li><strong>Transfer to writing.</strong> Can they spell these words correctly in their own writing? By 3rd grade, that's a fair expectation. If a child writes "laff" for "laugh" or "togeather" for "together," the word isn't fully integrated. Practice spelling them by hand, not just reading recognition.</li>
    <li><strong>Reading in longer text.</strong> By 3rd grade, kids should be reading chapter books. The test is in that context: do sight words flow by invisibly, or do they slow the reading? A child who reads fluently in a chapter book has these words automatic. One who still sounds out "because" or "together" doesn't, regardless of how they perform on isolated drills.</li>
    <li><strong>Watch for cumulative gaps.</strong> Run a full Dolch diagnostic periodically — all five grade groups. Gaps from kindergarten or 1st grade can still be present in 3rd grade, especially for kids who moved schools or had inconsistent instruction. They're worth finding and fixing.</li>
    <li><strong>Irregular pronunciations explicitly.</strong> "Laugh," "eight," "shall," "light" — go over these deliberately, because phonics won't get a child there. Name the irregularity: "this one breaks the rules — 'laugh' sounds like 'laff.'" Naming it makes it easier to remember.</li>
  </ul>

  <h2>A 4-week plan for 3rd graders</h2>
  <p><strong>Week 1:</strong> Full Dolch diagnostic. All 220 words, all five grade groups, one at a time. Save every hesitation. The work list you build here is more valuable than the 3rd grade list alone.</p>
  <p><strong>Week 2:</strong> Drill all saved words with a mix of generator sessions and Practice Mode. Include words from all grades — don't only work on 3rd grade words if earlier ones came up in the diagnostic.</p>
  <p><strong>Week 3:</strong> Reading in context. Pick a chapter book your child is currently in and track fluency. Are sight words stopping them? Which ones? Add those to the saved list if they aren't already there.</p>
  <p><strong>Week 4:</strong> Final speed run. Go through all 220 Dolch words in the generator on random shuffle across all grades. Any remaining hesitations become the targeted list for the next month. Begin introducing Fry words 1–100 for any student who's fully solid on all Dolch groups.</p>

  <h2>How to use this generator</h2>
  <p>This tool is pre-set to Dolch 3rd Grade. Change the grade filter anytime — checking earlier Dolch groups is worth doing regularly at this level. Generate a random set and hear words aloud with the speaker icon. Save trouble words with the heart; they persist between sessions. Practice Mode is useful for independent drilling once your child is comfortable running it themselves. Print any list directly from the browser for a take-home sheet or classroom reference.</p>

</div>
<!-- /SLOT:explainer -->
```

- [ ] **Step 5: Replace SLOT:faq**

```html
<!-- SLOT:faq -->
<div class="faq">
  <h2 class="faq-title">Frequently asked questions</h2>

  <div class="faq-item open">
    <button class="faq-q"><span class="faq-q-text">Do 3rd graders still need to practice sight words?</span><svg class="faq-chevron" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></button>
    <div class="faq-a">Yes — the 3rd grade Dolch list has 41 words including some with irregular pronunciations ("laugh," "eight," "shall") that trip kids up even at this level. It's also worth checking for gaps in earlier lists. A full Dolch diagnostic at the start of 3rd grade often reveals a handful of words from kindergarten or 1st grade that were never fully automated.</div>
  </div>

  <div class="faq-item">
    <button class="faq-q"><span class="faq-q-text">How many Dolch words should a 3rd grader know total?</span><svg class="faq-chevron" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></button>
    <div class="faq-a">All 220 Dolch service words — the complete Pre-K through 3rd Grade set. That's 40 + 52 + 41 + 46 + 41. After 3rd grade, most programs shift to the Fry list for continued vocabulary development.</div>
  </div>

  <div class="faq-item">
    <button class="faq-q"><span class="faq-q-text">What comes after the Dolch 3rd grade list?</span><svg class="faq-chevron" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></button>
    <div class="faq-a">The Fry list. Change the List filter in this generator to "Fry" and start with the 1–100 group. The first 300 Fry words overlap significantly with Dolch, so the transition is gradual. Fry continues to 1,000 words and covers academic vocabulary useful through 9th grade.</div>
  </div>

  <div class="faq-item">
    <button class="faq-q"><span class="faq-q-text">My 3rd grader reads fine but misspells sight words. Is that normal?</span><svg class="faq-chevron" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></button>
    <div class="faq-a">Yes, it's common. Reading recognition and spelling are separate skills. By 3rd grade, spelling sight words correctly in writing is a reasonable expectation — practice both reading with this tool and writing words by hand separately. If "laugh" is spelled "laf" or "together" is spelled "togeather," those words need spelling-specific practice, not just reading drill.</div>
  </div>

  <div class="faq-item">
    <button class="faq-q"><span class="faq-q-text">How do sight words connect to reading fluency in 3rd grade?</span><svg class="faq-chevron" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></button>
    <div class="faq-a">Third grade is when phrase-level reading typically develops — when kids stop reading word by word and start reading in chunks. Sight word automaticity is a prerequisite for that shift. Any word that still causes hesitation acts as a speed bump in every sentence it appears in, preventing the fluent phrasing that makes comprehension easier.</div>
  </div>

  <div class="faq-item">
    <button class="faq-q"><span class="faq-q-text">Should I move my 3rd grader to the Fry list?</span><svg class="faq-chevron" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></button>
    <div class="faq-a">Once all 220 Dolch words are solid, yes. Run a quick diagnostic across all five Dolch grade groups first — any hesitation is worth addressing before moving on. When everything looks automatic, switch the List filter to "Fry" and start with 1–100.</div>
  </div>
</div>
<!-- /SLOT:faq -->
```

- [ ] **Step 6: Replace SLOT:who**

```html
<!-- SLOT:who -->
<div class="who">
  <h2>Who uses this tool?</h2>
  <div class="uc-grid">
    <div class="uc"><div class="uc-title">Parents of 3rd Graders</div><div class="uc-body">Supporting a child making the transition to independent reading and chapter books. Run a full Dolch diagnostic at the start of the year, drill any gaps, and use Practice Mode as a quick daily check-in — five minutes, consistent.</div></div>
    <div class="uc"><div class="uc-title">3rd Grade Teachers</div><div class="uc-body">Run grade-group diagnostics to identify which Dolch words still need work across the class. Generate targeted practice lists for small groups and print take-home sheets directly from the browser — no separate software required.</div></div>
    <div class="uc"><div class="uc-title">Reading Specialists</div><div class="uc-body">The grade filter makes it easy to identify exactly where gaps sit across the full Dolch sequence. Save all hesitation words from a diagnostic session and use Practice Mode for targeted intervention — all without any setup or account.</div></div>
    <div class="uc"><div class="uc-title">Homeschool Educators</div><div class="uc-body">Completing the Dolch sequence and preparing for the Fry word progression. The generator handles both Dolch and Fry lists in one tool — finish the 3rd grade band, then switch the List filter to Fry to continue building vocabulary beyond the basic service words.</div></div>
  </div>
</div>
<!-- /SLOT:who -->
```

- [ ] **Step 7: Update init grade default**

In SLOT:init, change:
```javascript
document.getElementById('ctrl-group').value = '3rd';
```

- [ ] **Step 8: Commit**

```bash
git add template-deploy/tools-src/sight-words-3rd-grade.html
git commit -m "feat: add sight-words-3rd-grade page"
```

---

## Task 6: Build, copy output, add redirects, preview

**Files:**
- Run: `template-deploy/build.py`
- Copy: built HTML files → `wordineer-deploy/`
- Modify: `wordineer-deploy/_redirects`

- [ ] **Step 1: Build all pages**

```bash
cd "/Users/garrickdeetan/Documents/Random Word Generator Tool Site/template-deploy"
python3 build.py
```

Expected: no errors. Output files created in `template-deploy/output/`:
- `sight-words-kindergarten.html`
- `sight-words-1st-grade.html`
- `sight-words-2nd-grade.html`
- `sight-words-3rd-grade.html`
- `word-tools.html` (rebuilt with new cards)

Also rebuilt: any page that uses shared templates (nav, footer) — check that existing pages still look correct.

- [ ] **Step 2: Copy output to wordineer-deploy**

```bash
cp template-deploy/output/sight-words-kindergarten.html wordineer-deploy/
cp template-deploy/output/sight-words-1st-grade.html wordineer-deploy/
cp template-deploy/output/sight-words-2nd-grade.html wordineer-deploy/
cp template-deploy/output/sight-words-3rd-grade.html wordineer-deploy/
cp template-deploy/output/word-tools.html wordineer-deploy/
```

- [ ] **Step 3: Add _redirects entries**

Open `wordineer-deploy/_redirects`. Follow the existing pattern for clean URL rewrites. Add:

```
/sight-words-kindergarten /sight-words-kindergarten/ 301
/sight-words-kindergarten.html /sight-words-kindergarten/ 301
/sight-words-1st-grade /sight-words-1st-grade/ 301
/sight-words-1st-grade.html /sight-words-1st-grade/ 301
/sight-words-2nd-grade /sight-words-2nd-grade/ 301
/sight-words-2nd-grade.html /sight-words-2nd-grade/ 301
/sight-words-3rd-grade /sight-words-3rd-grade/ 301
/sight-words-3rd-grade.html /sight-words-3rd-grade/ 301
```

Also add the Cloudflare Pages rewrite rule so the HTML file serves at the clean URL:
```
/sight-words-kindergarten/* /sight-words-kindergarten.html 200
/sight-words-1st-grade/* /sight-words-1st-grade.html 200
/sight-words-2nd-grade/* /sight-words-2nd-grade.html 200
/sight-words-3rd-grade/* /sight-words-3rd-grade.html 200
```

Check the existing _redirects file for the exact format used for sight-words-generator and match it exactly.

- [ ] **Step 4: Local preview**

```bash
cd wordineer-deploy && python3 -m http.server 8080
```

Open in browser:
- `http://localhost:8080/sight-words-kindergarten.html` — verify: breadcrumb shows 4 levels, tool pre-loaded on Dolch Kindergarten, word list visible in explainer, grade nav strip links all pages
- `http://localhost:8080/sight-words-1st-grade.html` — verify: pre-loaded on 1st Grade
- `http://localhost:8080/sight-words-2nd-grade.html` — verify: pre-loaded on 2nd Grade
- `http://localhost:8080/sight-words-3rd-grade.html` — verify: pre-loaded on 3rd Grade
- `http://localhost:8080/word-tools.html` — verify: 4 new grade page cards visible in Vocabulary section

For each grade page, verify:
- [ ] Tool generates words from the correct Dolch grade on load
- [ ] Grade nav strip highlights the current page
- [ ] Cross-grade links in the nav strip all resolve
- [ ] Word chip grid shows correct words for the grade
- [ ] Audio works (speaker icon)
- [ ] Practice Mode works
- [ ] FAQ accordion opens/closes
- [ ] Print styles hide non-word-list content

- [ ] **Step 5: Final commit**

```bash
git add wordineer-deploy/sight-words-kindergarten.html \
        wordineer-deploy/sight-words-1st-grade.html \
        wordineer-deploy/sight-words-2nd-grade.html \
        wordineer-deploy/sight-words-3rd-grade.html \
        wordineer-deploy/word-tools.html \
        wordineer-deploy/_redirects
git commit -m "build: add sight words grade pages — kindergarten, 1st, 2nd, 3rd grade"
```

---

## Self-Review

**Spec coverage check:**
- ✅ 4 grade pages (Kindergarten, 1st, 2nd, 3rd) — Tasks 2–5
- ✅ Pre-filtered tool per grade — each init slot sets list+grade before generate()
- ✅ 1,000+ word copy per page — each explainer has 6 H2 sections totaling 1,000+ words
- ✅ Complete static word list in explainer (hardcoded word-chips grid) — each page
- ✅ Breadcrumb 4 levels — Wordineer › Word Tools › Sight Words Generator › [Grade]
- ✅ Cross-grade nav strip — grade-nav div at top of each explainer
- ✅ word-tools.html updated with 4 grade cards + icons — Task 1
- ✅ tools.json updated (mega, footer, more_tools) — Task 1
- ✅ _redirects entries — Task 6
- ✅ FAQ 6 questions per page — each with grade-specific content
- ✅ Who 4 cards per page — each grade-adjusted
- ✅ Build + preview verification — Task 6

**No placeholders found.** All word lists are fully hardcoded. All content sections are written out. All code blocks are complete.

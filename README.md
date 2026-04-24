# Wordineer — Complete Deployment & Expansion Guide

---

## PART 1 — File structure

```
wordineer/
├── index.html                        ← homepage (random word generator)
├── random-sentence-generator.html    ← second tool (ready to customise)
├── [tool-name].html                  ← copy BaseLayout.html for each new tool
│
├── styles/
│   └── global.css                    ← ALL shared styles — edit once, applies everywhere
│
├── scripts/
│   └── tool-engine.js                ← THE FIX: loads words.json, powers all word tools
│
├── data/
│   └── words.json                    ← 289 curated words with defs, types, difficulty
│
└── src/
    └── layouts/
        └── BaseLayout.html           ← master template — copy for every new tool
```

### Why words weren't generating in the template (root cause + fix)
The old BaseLayout had an empty `<script>` slot with a comment saying
"add your JS here" — but no WORDS array and no generate() function.

**The fix:** `tool-engine.js` is now a shared file that:
1. Fetches `data/words.json` once on page load
2. Exposes `WORDINEER.render()`, `WORDINEER.reset()`, etc.
3. Every page just calls `WORDINEER.init({...})` with its element IDs

**Words now load from `data/words.json`** — a single file you add to,
never scattered across multiple HTML files.

---

## PART 2 — Deployment options (fastest to most scalable)

### Option A — Cloudflare Pages (RECOMMENDED — free, fastest globally)

Best for: pure HTML/CSS/JS sites with no server needed.

**Step 1 — Register domain**
→ Go to namecheap.com
→ Search for wordineer.com, buy it (~$12/year)
→ At checkout, set nameservers to Cloudflare (do this after step 2)

**Step 2 — Set up Cloudflare**
→ Go to cloudflare.com → Create free account
→ Add Site → enter your domain → select Free plan
→ Cloudflare scans DNS, then gives you 2 nameservers (e.g. ns1.cloudflare.com)
→ Go back to Namecheap → Manage Domain → Nameservers → Custom → paste both
→ Wait 5–30 min for propagation

**Step 3 — Create GitHub repository**
→ Go to github.com → New repository → name it "wordineer"
→ Keep it Public (required for Cloudflare Pages free tier)

**Step 4 — Push your files to GitHub**
```bash
# In your project folder:
git init
git add .
git commit -m "Initial Wordineer build"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/wordineer.git
git push -u origin main
```

**Step 5 — Connect to Cloudflare Pages**
→ Cloudflare dashboard → Pages → Create a project → Connect to Git
→ Select your wordineer repo
→ Build settings:
   - Framework preset: None
   - Build command: (leave blank)
   - Build output directory: / (root)
→ Click Save and Deploy
→ Cloudflare builds and deploys in ~30 seconds

**Step 6 — Add your custom domain**
→ Cloudflare Pages → your project → Custom domains → Add custom domain
→ Enter: wordineer.com
→ Also add: www.wordineer.com
→ Cloudflare automatically creates DNS records and provisions SSL
→ Your site is live at https://wordineer.com with HTTPS ✓

**Step 7 — Every future update**
```bash
git add .
git commit -m "Add dice-roller page"
git push
# Cloudflare auto-deploys in ~20 seconds. Done.
```

---

### Option B — Netlify (alternative, equally free)

→ netlify.com → New site from Git → select your GitHub repo
→ Build command: (blank) | Publish directory: /
→ Add custom domain in Site settings → Domain management
→ Add Namecheap DNS records Netlify provides
→ Free SSL auto-provisioned

Use Netlify if: you want drag-and-drop uploads without Git.
You can literally drag your folder into netlify.com/drop and it's live in 10 seconds.

---

### Option C — Vercel (best if you later move to Next.js)

→ vercel.com → Import Git Repository → select wordineer
→ Framework: Other | Root: /
→ Deploy
→ Add domain in Settings → Domains

Use Vercel if: you plan to upgrade to Next.js/React later.
The same repo works on both — no migration needed.

---

## PART 3 — Cloudflare Pages folder structure (what to upload)

When deploying, Cloudflare serves everything from your repo root.
Your file paths must match your URLs exactly:

| File in repo          | URL it serves                        |
|-----------------------|--------------------------------------|
| index.html            | wordineer.com/                       |
| random-word-generator.html | wordineer.com/random-word-generator |
| styles/global.css     | wordineer.com/styles/global.css      |
| scripts/tool-engine.js| wordineer.com/scripts/tool-engine.js |
| data/words.json       | wordineer.com/data/words.json        |

IMPORTANT: The `fetch('/data/words.json')` in tool-engine.js uses an
absolute path from root. This works perfectly on Cloudflare Pages.
It will NOT work if you just open the HTML file directly from your Desktop
(file:// protocol blocks fetch). Always test via a local server:

```bash
# Option 1 — Python (built in on Mac/Linux)
python3 -m http.server 8080
# then open http://localhost:8080

# Option 2 — Node (if installed)
npx serve .
# then open http://localhost:3000
```

---

## PART 4 — Adding more words to words.json

Open `data/words.json` and add entries in this format:

```json
{
  "w": "Luminary",
  "t": "noun",
  "d": "a person who inspires or influences others in a particular sphere",
  "diff": "medium",
  "borrowed": false
}
```

Fields:
- `w`        — the word (capitalised)
- `t`        — part of speech: "noun", "adjective", "verb", "adverb"
- `d`        — definition (keep under 100 chars for clean display)
- `diff`     — "easy", "medium", or "hard"
- `borrowed` — true if borrowed from another language (German, French, etc.)

Free word sources:
- WordNet (Princeton): wordnet.princeton.edu — public domain, 155,000 words
- Datamuse API: api.datamuse.com — free, no key, returns words + definitions
- Free Dictionary API: api.dictionaryapi.dev — free, no key, full definitions

To bulk-add words, create a script that calls the Free Dictionary API:
```js
// fetch-words.js — run with: node fetch-words.js
const words = ['ephemeral','tenacious','serendipity']; // your word list
for (const w of words) {
  const res = await fetch(`https://api.dictionaryapi.dev/api/v2/entries/en/${w}`);
  const data = await res.json();
  const def = data[0]?.meanings[0]?.definitions[0]?.definition;
  const pos = data[0]?.meanings[0]?.partOfSpeech;
  console.log(JSON.stringify({ w: w[0].toUpperCase()+w.slice(1), t: pos, d: def, diff:'medium', borrowed:false }));
}
```

---

## PART 5 — Creating a new tool page (step by step)

### Step 1 — Copy the template
```bash
cp src/layouts/BaseLayout.html [tool-name].html
# Example: cp src/layouts/BaseLayout.html dice-roller.html
```

### Step 2 — Update the 9 marked slots (search for ① ② ③ etc.)

| Slot | What to change | Example |
|------|---------------|---------|
| ① | `<title>` | `Dice Roller — Free Online Dice \| Wordineer` |
| ② | `<meta description>` | `Roll any dice online free — 4, 6, 8, 10, 12, 20 sided.` |
| ③ | canonical URL | `https://wordineer.com/dice-roller` |
| ④ | og:title + og:url | Match ① and ③ |
| ④ | FAQ JSON-LD | Update 3 questions relevant to this tool |
| ⑤ | `<h1>` | `Dice roller` |
| ⑤ | Hero subtitle | `Roll any dice type instantly — 4, 6, 8, 10, 12, or 20 sided.` |
| ⑥ | Active mega-link | Add `class="active"` to the right nav link |
| ⑦ | Tool slot | Replace placeholder `<div>` with your tool's HTML |
| ⑧ | Explanation text | 300+ words unique to this tool |
| ⑨ | FAQ items | 5–7 questions unique to this tool |

### Step 3 — For WORD tools: the WORDINEER.init() call at the bottom
is already there — just make sure your HTML element IDs match:
```html
<ul id="word-list"></ul>      <!-- listId -->
<input id="ctrl-count">       <!-- countId -->
<span id="word-count">        <!-- countDisplayId -->
<select id="ctrl-type">       <!-- typeId -->
<select id="ctrl-diff">       <!-- diffId -->
<input id="ctrl-first">       <!-- firstId -->
<input id="ctrl-last">        <!-- lastId -->
<input type="checkbox" id="ctrl-defs"> <!-- defsId -->
```

### Step 4 — For NON-WORD tools (dice roller, coin flip, etc.)
Remove the word generator HTML and the WORDINEER.init() call.
Write your own simple JS directly in a `<script>` tag at the bottom.
The nav, footer, ad zones, and affiliate blocks are already there.

### Step 5 — Add to the nav mega menu
Open `src/layouts/BaseLayout.html` → find the mega menu → add a link.
Then update this same nav in ALL existing .html files.
(This is why Astro is worth upgrading to at 10+ pages — see Part 6.)

### Step 6 — Add to the footer
Same as Step 5 — update BaseLayout.html and copy to all pages.

### Step 7 — Deploy
```bash
git add [tool-name].html
git commit -m "Add dice-roller tool"
git push
# Live on Cloudflare Pages in ~20 seconds
```

---

## PART 6 — Replacing mock ads with real AdSense tags

When approved by Google AdSense, replace each ad zone's inner content:

**Zone A (sidebar 160×300):**
Find: `<!-- AD ZONE A — sidebar -->` → replace the inner `<div class="ad-sidebar">` content with:
```html
<ins class="adsbygoogle"
     style="display:inline-block;width:160px;height:300px"
     data-ad-client="ca-pub-XXXXXXXXXXXX"
     data-ad-slot="XXXXXXXXXX"></ins>
<script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
```

**Zone B (leaderboard 728×90):**
Find: `<!-- AD ZONE B -->` → replace `<div class="ad-leaderboard-inner">` content:
```html
<ins class="adsbygoogle"
     style="display:inline-block;width:728px;height:90px"
     data-ad-client="ca-pub-XXXXXXXXXXXX"
     data-ad-slot="XXXXXXXXXX"></ins>
<script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
```

**Zone C (rectangle 336×280):**
Find: `<!-- AD ZONE C -->` → replace `<div class="ad-rect">` content.

Add the AdSense `<script>` tag once in `<head>` of BaseLayout.html:
```html
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-XXXX" crossorigin="anonymous"></script>
```

---

## PART 7 — Replacing Grammarly placeholders with real affiliate links

1. Apply at grammarly.com/affiliates (via Impact platform)
2. Get your unique URL: `https://grammarly.go2cloud.org/aff_c?offer_id=X&aff_id=Y`
3. In VS Code: Edit → Find in Files → search `https://grammarly.com`
4. Replace all with your affiliate URL + tracking params:
   `https://grammarly.go2cloud.org/aff_c?offer_id=X&aff_id=Y&utm_source=wordineer`
5. Save all files → `git add . && git commit -m "Add Grammarly affiliate links" && git push`

---

## PART 8 — Upgrade path: when to move to Astro (10+ pages)

At 10+ pages, maintaining copy-pasted nav/footer becomes painful.
Astro gives you shared components with zero JS overhead.

```bash
npm create astro@latest wordineer
# choose: "Empty" template, TypeScript: No

# Move files:
cp global.css src/styles/
cp tool-engine.js public/scripts/
cp words.json public/data/

# Create BaseLayout.astro — imports once, used by all pages
# Each tool becomes src/pages/dice-roller.astro
# Nav and Footer become src/components/Nav.astro, Footer.astro
```

Astro outputs pure static HTML — same Cloudflare Pages deployment,
same performance. Zero behaviour change for users, huge maintainability win for you.

---

## Quick reference: deployment checklist

- [ ] Domain registered (Namecheap ~$12/year)
- [ ] Cloudflare account created, nameservers updated
- [ ] GitHub repo created, files pushed
- [ ] Cloudflare Pages project connected to GitHub repo
- [ ] Custom domain added in Cloudflare Pages
- [ ] SSL active (auto — confirm green padlock)
- [ ] Test: open wordineer.com → words generate ✓
- [ ] Test: open wordineer.com/random-sentence-generator.html → loads ✓
- [ ] Submit to Google Search Console (search.google.com/search-console)
- [ ] Submit sitemap: create sitemap.xml listing all .html pages
- [ ] Apply for Grammarly affiliate (grammarly.com/affiliates)
- [ ] Apply for Google AdSense once 10K+ sessions/month

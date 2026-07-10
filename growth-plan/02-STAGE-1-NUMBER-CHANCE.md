# Stage 1 — Number & Chance cluster

**Goal:** Build every tool in the `/number-chance/` category. Fix the broken URLs, then launch all 30+ tools across three waves.

**Why this stage first:**
- The hub page (`/number-chance/`) already exists and is linked from the nav — Google has already crawled the "Coming soon" cards and found dead links
- `/coin-flip/`, `/random-number-generator/`, and `/dice-roller/` are **BROKEN** right now (serve homepage content with wrong canonical) — every day these are unfixed is ranking equity being wasted
- Coin flip, dice roller, and random number generators are among the **lowest-competition utility keywords** on the web relative to their search volume — incumbents like random.org and flip-a-coin.com win on backlinks, not content quality
- Programmatic structure: the number range tools (1–10, 1–100, 1–1000, etc.) share a single template, so you build once and generate ~14 pages
- No data files needed — all tools are pure JS, no fetch(), no load delay

**Realistic outcome at maturity:** 15,000–30,000 visits/month across this cluster.

**Estimated build effort:** 30–50 hours across 5–6 weeks.

---

## Build status — as of 2026-07-10

### Wave 1 — 8/8 complete ✅

| Tool | URL | Status |
|---|---|---|
| Coin Flip | `/coin-flip/` | ✅ Merged to main |
| Random Number Generator | `/random-number-generator/` | ✅ Merged to main |
| Random Number 1–100 | `/random-number-1-100/` | ✅ Merged to main |
| Dice Roller | `/dice-roller/` | ✅ Merged to main |
| Random Number 1–10 | `/random-number-1-10/` | ✅ Merged to main |
| Flip a Coin 10 Times | `/flip-a-coin-10-times/` | ✅ Merged to main |
| Flip a Coin 100 Times | `/flip-a-coin-100-times/` | ✅ Merged to main |
| Wheel of Names | `/wheel-of-names/` | ✅ Merged to main |

### Wave 2 — 10/15 complete

| Tool | URL | Status |
|---|---|---|
| Random Number 1–20 | `/random-number-1-20/` | ✅ Merged to main |
| Random Number 1–50 | `/random-number-1-50/` | ✅ Merged to main |
| Random Number 1–6 | `/random-number-1-6/` | ✅ Merged to main |
| Random Number 1–1000 | `/random-number-1-1000/` | ✅ Merged to main |
| Random Number 1–4 | `/random-number-1-4/` | ✅ Merged to main |
| Random Number 1–8 | `/random-number-1-8/` | ✅ Merged to main |
| Random Number 1–3 | `/random-number-1-3/` | ✅ Merged to main |
| Random Number 1–25 | `/random-number-1-25/` | ✅ Merged to main |
| Random Number 1–30 | `/random-number-1-30/` | ✅ Merged to main |
| Pick a Number 1–20 | `/pick-a-number-1-20/` | ✅ Merged to main |
| Random Number 1–200 | `/random-number-1-200/` | ⬜ Not built |
| Flip a Coin 5 Times | `/flip-a-coin-5-times/` | ⬜ Not built |
| Flip a Coin 1000 Times | `/flip-a-coin-1000-times/` | ⬜ Not built |
| Flip 2 Coins | `/flip-2-coins/` | ⬜ Not built |
| Flip 3 Coins | `/flip-3-coins/` | ⬜ Not built |

### Wave 3 — 0/9 complete

| Tool | URL | Status |
|---|---|---|
| Magic 8 Ball | `/magic-8-ball/` | ⬜ Not built |
| Rock Paper Scissors | `/rock-paper-scissors/` | ⬜ Not built |
| Powerball Number Generator | `/powerball-number-generator/` | ⬜ Not built |
| Random Even Number Generator | `/random-even-number-generator/` | ⬜ Not built |
| Random Odd Number Generator | `/random-odd-number-generator/` | ⬜ Not built |
| Weighted Random Number Generator | `/weighted-random-number-generator/` | ⬜ Not built |
| Random Number Wheel 1–10 | `/random-number-wheel-1-10/` | ⬜ Not built |
| Lottery Number Generator | `/lottery-number-generator/` | ⬜ Not built |
| Raffle Number Generator | `/raffle-number-generator/` | ⬜ Not built |

### Next session
5 Wave 2 tools remaining: random-number-1-200, flip-a-coin-5-times, flip-a-coin-1000-times, flip-2-coins, flip-3-coins. Then all 9 Wave 3 specialty tools.

---

## Keyword landscape

### Tier 1 — Highest-volume, build in Wave 1

| Keyword | Est. Volume | Est. KD | Target URL |
|---|---|---|---|
| flip a coin | 500,000–1M | 55–65 | `/coin-flip/` |
| random number generator | 200,000–500,000 | 50–60 | `/random-number-generator/` |
| random number generator 1-100 | 50,000–100,000 | 35–45 | `/random-number-1-100/` |
| dice roller | 100,000–200,000 | 40–50 | `/dice-roller/` |
| wheel of names | 200,000–500,000 | 55–65 | `/wheel-of-names/` |
| random number generator 1-10 | 30,000–60,000 | 25–35 | `/random-number-1-10/` |
| flip a coin 10 times | 30,000–60,000 | 20–30 | `/flip-a-coin-10-times/` |
| flip a coin 100 times | 15,000–30,000 | 15–25 | `/flip-a-coin-100-times/` |

### Tier 2 — Number range variants (Wave 2)

| Keyword | Est. Volume | Est. KD | Target URL |
|---|---|---|---|
| random number 1-20 | 20,000–40,000 | 20–30 | `/random-number-1-20/` |
| random number 1-50 | 15,000–30,000 | 20–30 | `/random-number-1-50/` |
| random number 1-6 | 15,000–30,000 | 20–30 | `/random-number-1-6/` |
| random number 1-1000 | 5,000–10,000 | 15–25 | `/random-number-1-1000/` |
| random number 1-4 | 5,000–10,000 | 10–20 | `/random-number-1-4/` |
| random number 1-8 | 3,000–6,000 | 10–20 | `/random-number-1-8/` |
| random number 1-3 | 3,000–6,000 | 10–20 | `/random-number-1-3/` |
| random number 1-25 | 2,000–4,000 | 10–20 | `/random-number-1-25/` |
| random number 1-30 | 2,000–4,000 | 10–20 | `/random-number-1-30/` |
| random number 1-200 | 1,500–3,000 | 10–20 | `/random-number-1-200/` |
| pick a number 1-20 | 4,000–8,000 | 15–25 | `/pick-a-number-1-20/` |
| flip a coin 5 times | 8,000–15,000 | 10–20 | `/flip-a-coin-5-times/` |
| flip 2 coins | 3,000–6,000 | 10–20 | `/flip-2-coins/` |
| flip 3 coins | 2,000–4,000 | 10–20 | `/flip-3-coins/` |
| flip a coin 1000 times | 4,000–8,000 | 10–20 | `/flip-a-coin-1000-times/` |

### Tier 3 — Specialty tools (Wave 3)

| Keyword | Est. Volume | Est. KD | Target URL |
|---|---|---|---|
| powerball number generator | 30,000–60,000 | 30–40 | `/powerball-number-generator/` |
| magic 8 ball | 50,000–100,000 | 45–55 | `/magic-8-ball/` |
| rock paper scissors | 30,000–60,000 | 40–50 | `/rock-paper-scissors/` |
| random even number generator | 3,000–6,000 | 10–20 | `/random-even-number-generator/` |
| random odd number generator | 2,000–4,000 | 10–20 | `/random-odd-number-generator/` |
| weighted random number generator | 2,000–4,000 | 15–25 | `/weighted-random-number-generator/` |
| random number wheel | 5,000–10,000 | 20–30 | `/random-number-wheel-1-10/` |
| lottery number generator | 8,000–15,000 | 25–35 | `/lottery-number-generator/` |
| raffle number generator | 4,000–8,000 | 15–25 | `/raffle-number-generator/` |

---

## Build order

### Wave 1 — High-traffic anchors (Weeks 1–2)

Build these 8 tools first. They carry the highest individual search volume and include the 3 currently broken URLs that need immediate repair.

---

#### 1. Coin Flip — `/coin-flip/`

**Priority: CRITICAL — currently broken**

**Target keywords:** "flip a coin" (500K–1M/mo, KD 55–65), "coin flip" (200K+/mo)

**Why the difficulty is irrelevant:** You're not trying to rank #1 on "flip a coin" against flip-a-coin.com immediately. You're fixing a broken canonical that's hurting your domain and capturing the long-tail click-throughs from your hub page. Every coin flip variant page you build later links here.

**Features to build:**
- Large animated coin (CSS flip animation — heads shows H, tails shows T with distinct styling)
- Single large FLIP button — center of screen, keyboard trigger (Space/Enter)
- Result displayed prominently: "Heads" or "Tails" in big text
- Session counter: "Heads: 4 | Tails: 3 | Total: 7" — resets on page reload
- Copy result button (copies "Heads" to clipboard)
- Result history: last 10 flips shown as small H/T chips below counter
- "Flip Again" secondary CTA after result appears

**Features to skip:** Sound effects, animation customization, persistent history (localStorage), sharing. Add in v2 based on engagement.

**Tool source file:** `template-deploy/tools-src/coin-flip.html`

**Server-render requirement:** Show "Click to flip" as the initial state in static HTML — no placeholder.

---

#### 2. Random Number Generator 1–100 — `/random-number-1-100/`

**Target keywords:** "random number generator 1 to 100" (50K–100K/mo, KD 35–45), "random number between 1 and 100"

**Features to build:**
- Giant number display (the result, center of screen — 72–96px font)
- GENERATE button — keyboard trigger (Space/Enter)
- Min/max labels shown ("Between 1 and 100") as static context
- Copy button next to result
- History strip: last 10 results shown as small chips, newest left
- Re-generate clears previous result briefly before showing new one (visual beat)

**Features to skip:** Export, multiple-at-once generation, sorting. Keep it one number, one click.

**Server-render requirement:** Static HTML shows a sample number (e.g., "42") as default result with a note it refreshes on generate.

**Template note:** This page IS the canonical template for all Wave 2 number range variants. Build it well once.

---

#### 3. Random Number Generator (custom) — `/random-number-generator/`

**Priority: CRITICAL — currently broken**

**Target keywords:** "random number generator" (200K–500K/mo, KD 50–60)

**Features to build:**
- Min/max input fields (default: 1 and 100)
- GENERATE button — large, keyboard trigger
- Giant result number display
- Copy button
- History strip: last 10 results
- Quick-range pills below inputs: "1–10", "1–100", "1–1000" — clicking fills min/max instantly
- Mobile: inputs side by side with large tap targets

**Differentiation vs. incumbents:** The quick-range pills make this more frictionless than most competitors who require typing both numbers from scratch.

---

#### 4. Dice Roller — `/dice-roller/`

**Priority: CRITICAL — currently broken**

**Target keywords:** "dice roller" (100K–200K/mo, KD 40–50), "roll a dice online", "virtual dice"

**Features to build:**
- Die type selector: D4, D6, D8, D10, D12, D20 — toggle buttons, D6 selected by default
- Optional: quantity selector (1–4 dice) — add/remove dice chips
- ROLL button — large, keyboard trigger (Space/Enter/R)
- Result displayed per die + sum total if multiple
- Visual die face for D6 (dot pattern SVG) — D4/D8/D10/D12/D20 show number only (not pips)
- Roll history: last 10 results (showing die type + result)
- "Roll again" secondary CTA

**Classroom note:** Teachers use dice rollers for math probability lessons. The D6 with dot faces is critical for this use case — it's recognizable at a glance on a projector.

**Features to skip:** 3D animation, sound, RPG modifier math (AC, to-hit), custom die sizes. All v2.

---

#### 5. Wheel of Names — `/wheel-of-names/`

**Target keywords:** "wheel of names" (200K–500K/mo, KD 55–65), "name picker wheel", "classroom name spinner"

**Note on difficulty:** wheelofnames.com dominates this term and is a mature, full-featured product. Wordineer's path isn't outranking it on the head term — it's capturing classroom-adjacent traffic from your spelling bee and sight words audience who already know your site, plus long-tail variants like "random name picker for classroom."

**Features to build:**
- Canvas-based spinning wheel (using browser Canvas API)
- Names textarea: paste or type names one per line
- SPIN button — triggers easing animation (3–5 second spin, decelerates realistically)
- Winner modal/overlay shown after spin stops with winner's name
- "Remove winner and spin again" option
- Segment count auto-adjusts to name count (up to 20 names practical)
- Color segments auto-assigned from a palette

**Features to skip:** Weighted segments, saving lists to URL, multiple wheels, audio. These are v2+ features that wheelofnames.com has — match them only after the basic tool is live.

**Implementation note:** Canvas spinner is the most complex build in Wave 1. Plan 6–8 hours for this alone. Alternatively, build a simpler "list randomizer" that picks a name without the visual spin, then add the canvas wheel in v1.1.

---

#### 6. Random Number Generator 1–10 — `/random-number-1-10/`

**Target keywords:** "random number 1 to 10" (30K–60K/mo, KD 25–35), "number between 1 and 10"

**Teacher use case:** Primary school "I'm thinking of a number between 1 and 10" — the most common classroom number game. Position copy in hero to call this out.

**Features:** Identical to the 1–100 template. Just change the range. Build from the 1–100 tool-src by cloning CONFIG and adjusting `min`, `max`, hero text, meta, and internal links.

---

#### 7. Flip a Coin 10 Times — `/flip-a-coin-10-times/`

**Target keywords:** "flip a coin 10 times" (30K–60K/mo, KD 20–30)

**Why it ranks:** This is a long-tail term with much lower KD than "flip a coin" — and people searching it have a specific intent (probability demo, decision run, teacher activity).

**Features to build:**
- "Flip All 10" button — auto-runs 10 flips in sequence with brief visual delay between each
- Results grid: 10 coin icons showing H or T per flip
- Running tally shown updating in real time as flips animate
- Final summary: "Heads: 7 | Tails: 3 | 70% heads this run"
- "Flip Again" button resets and re-runs all 10
- Copy result button (copies "10 flips: HHTHTHHTHH — 6 heads, 4 tails")

**Key insight from research:** flip-a-coin.com built dedicated pages for each multi-flip variant. That's exactly what this template approach replicates — same tool, different counts, different URLs.

---

#### 8. Flip a Coin 100 Times — `/flip-a-coin-100-times/`

**Target keywords:** "flip a coin 100 times" (15K–30K/mo, KD 15–25)

**Primary use case:** Statistics and probability education — demonstrate the law of large numbers.

**Features to build:**
- "Run 100 Flips" button — instant result (no animation needed at this volume, just calculate)
- Result grid of 100 coins shown as small H/T chips in a 10×10 grid
- Distribution bar chart: visual split of heads vs. tails
- Stats summary: "Heads: 52 | Tails: 48 | 52% heads"
- "Run Again" button
- Copy stats button

**Copy note:** Hero text for this page should lean into the stats/education angle: "See how close to 50/50 you actually get."

---

### Wave 2 — Number range variants (Weeks 3–4)

These 11 pages are **programmatic variants** of the 1–100 tool built in Wave 1. Build one canonical template, then clone for each range.

**Template approach:** Each tool-src file has identical structure — only these values vary:
- CONFIG: `url`, `output`
- Meta: `<title>`, `<meta name="description">`, canonical URL
- Hero: H1, intro paragraph
- JS: `const MIN = 1; const MAX = N;`
- Quick-range pills: updated to neighboring ranges
- Internal links: "Try also" section linking to adjacent tools

**Build checklist per variant:**
- [ ] Clone `/random-number-1-100/` tool-src
- [ ] Update CONFIG, meta, canonical
- [ ] Update hero H1 + intro (unique — not duplicate content)
- [ ] Update JS MIN/MAX constants
- [ ] Update quick-range pills to show related ranges
- [ ] Add to tools.json (update hub page card from "Coming soon" to live link)
- [ ] Add _redirects entry if needed

**Pages to build (in order of volume):**

| Page | URL | MIN | MAX | Notes |
|---|---|---|---|---|
| Random Number 1–20 | `/random-number-1-20/` | 1 | 20 | D&D ability check range, classroom range |
| Random Number 1–50 | `/random-number-1-50/` | 1 | 50 | Raffle range, bracket draws |
| Random Number 1–6 | `/random-number-1-6/` | 1 | 6 | Virtual D6 — show dot-face SVG same as dice roller |
| Pick a Number 1–20 | `/pick-a-number-1-20/` | 1 | 20 | "I'm thinking of" guessing game framing |
| Flip a Coin 5 Times | `/flip-a-coin-5-times/` | — | — | Clone coin flip multi-flip template |
| Flip a Coin 1000 Times | `/flip-a-coin-1000-times/` | — | — | Show histogram, no animation |
| Flip 2 Coins | `/flip-2-coins/` | — | — | Show both results simultaneously |
| Flip 3 Coins | `/flip-3-coins/` | — | — | Show 3 results simultaneously |
| Random Number 1–1000 | `/random-number-1-1000/` | 1 | 1000 | Large giveaways |
| Random Number 1–4 | `/random-number-1-4/` | 1 | 4 | Tie-breaker, turn order |
| Random Number 1–8 | `/random-number-1-8/` | 1 | 8 | D8 equivalent |
| Random Number 1–3 | `/random-number-1-3/` | 1 | 3 | Three-way decision |
| Random Number 1–25 | `/random-number-1-25/` | 1 | 25 | 25-entry draws |
| Random Number 1–30 | `/random-number-1-30/` | 1 | 30 | Classroom of 30 students |
| Random Number 1–200 | `/random-number-1-200/` | 1 | 200 | Double-hundred range |

---

### Wave 3 — Specialty tools (Weeks 5–6)

These tools each require unique implementations — no shared template. Prioritize by volume.

---

#### Magic 8 Ball — `/magic-8-ball/`

**Target keywords:** "magic 8 ball" (50K–100K/mo, KD 45–55), "magic 8 ball online"

**Features:**
- Large 8-ball icon (SVG — dark circle with "8" visible)
- Tap/click to "shake" — CSS shake animation, then triangle window reveals answer
- 20 classic responses (10 positive, 5 neutral, 5 negative) — exact Magic 8-Ball text
- Answer displayed in the triangle window area
- "Ask Again" / "Shake Again" button
- No text input needed (user asks question in their head — classic mechanic)

---

#### Rock Paper Scissors — `/rock-paper-scissors/`

**Target keywords:** "rock paper scissors" (30K–60K/mo, KD 40–50)

**Features:**
- 3 choice buttons: Rock, Paper, Scissors (with icon SVGs)
- Computer picks simultaneously (shown after user clicks)
- Result: "You win!", "Computer wins!", "It's a tie!" with reasoning ("Paper covers rock")
- Session score counter: Player X – Computer Y
- "Play Again" resets round (keeps score)

---

#### Powerball Number Generator — `/powerball-number-generator/`

**Target keywords:** "powerball number generator" (30K–60K/mo, KD 30–40), "powerball random numbers"

**Features:**
- GENERATE button — picks 5 numbers from 1–69 + 1 Powerball from 1–26 (no repeats in main 5)
- Results displayed as lottery-style balls: 5 white balls + 1 red Powerball
- "Generate New Set" button
- Copy button (copies as "5, 18, 23, 41, 66 — PB: 14")
- Brief explainer: "This selects numbers using the official Powerball format. It does not improve your odds."

---

#### Random Even Number Generator — `/random-even-number-generator/`

**Target keywords:** "random even number generator" (3K–6K/mo, KD 10–20)

**Features:**
- Default range: 2–100 (even numbers only)
- Optional: set custom min/max (tool enforces even output)
- Standard number display + generate + copy + history
- Server-render: show an even number as example

---

#### Random Odd Number Generator — `/random-odd-number-generator/`

**Target keywords:** "random odd number generator" (2K–4K/mo, KD 10–20)

**Features:** Mirror of even number generator with odd output.

---

#### Weighted Random Number Generator — `/weighted-random-number-generator/`

**Target keywords:** "weighted random number generator" (2K–4K/mo, KD 15–25)

**Features:**
- Add options (label + weight) via a list input — up to 10 options
- Visual weight bar per option (shows relative probability)
- PICK button — draws from weighted pool
- Result shown with probability context: "Red (40% weight)"
- "Add Option" / "Clear All" controls
- Primary use case: game design, probability demos, unequal group selections

---

#### Random Number Wheel 1–10 — `/random-number-wheel-1-10/`

**Target keywords:** "random number wheel 1-10" (3K–6K/mo, KD 15–25), "number spinner 1-10"

**Note:** This is a classroom-specific tool — number wheels for math warm-ups. Primary audience: elementary school teachers.

**Features:**
- Pre-filled canvas wheel with 10 segments (1–10)
- SPIN button — same spinner mechanic as Wheel of Names
- Result shown after spin
- Designed for projector use: large, high-contrast

**Second variant:** `/random-number-wheel-1-50/` — same tool, 50 segments.

---

#### Lottery Number Generator — `/lottery-number-generator/`

**Target keywords:** "lottery number generator" (8K–15K/mo, KD 25–35)

**Features:**
- Default format: 6 numbers from 1–49 (common international format)
- "Generate Lucky Numbers" button
- Lottery-ball style result display
- Copy button
- Brief explainer on randomness and odds

---

#### Raffle Number Generator — `/raffle-number-generator/`

**Target keywords:** "raffle number generator" (4K–8K/mo, KD 15–25)

**Features:**
- Input: ticket pool size (e.g., "200 tickets sold")
- DRAW button: picks 1 number from 1–N
- Result displayed prominently
- "Draw Another Winner" button (draws again from full pool, or optionally excludes previous winner)

---

## Template approach summary

| Tool category | Template file | Pages generated |
|---|---|---|
| Coin flip (single) | `coin-flip.html` | 1 |
| Coin flip (multi) | `flip-a-coin-N-times.html` | 4 (5, 10, 100, 1000 times) |
| Multi-coin simultaneous | `flip-N-coins.html` | 2 (2, 3 coins) |
| Number generator (custom) | `random-number-generator.html` | 1 |
| Number generator (range) | `random-number-1-100.html` (canonical) | 12 variants |
| Dice roller | `dice-roller.html` | 1 |
| Wheel of Names | `wheel-of-names.html` | 1 |
| Number wheel | `random-number-wheel.html` | 2 (1–10, 1–50) |
| Magic 8 Ball | `magic-8-ball.html` | 1 |
| Rock Paper Scissors | `rock-paper-scissors.html` | 1 |
| Powerball | `powerball-number-generator.html` | 1 |
| Even/Odd generators | `random-even-number-generator.html` | 2 |
| Weighted generator | `weighted-random-number-generator.html` | 1 |
| Lottery | `lottery-number-generator.html` | 1 |
| Raffle | `raffle-number-generator.html` | 1 |

**Total pages: 32**

---

## Competitive feature decisions

Based on research of flip-a-coin.com, wheelofnames.com, random.org, and random-number-generator.com:

### Include in every tool (table stakes)
- One-click generate with keyboard trigger (Space or Enter)
- Copy result button
- Session history (minimum: last 10 results as chips)
- Mobile-first layout (large tap targets, no hover-only interactions)
- Instant results — no loading state needed (all JS, no fetch)

### Wordineer's differentiation angle
- **Speed moat**: Static HTML served from Cloudflare edge — no JS bundle, no hydration wait. Faster than every React-based competitor.
- **Teacher-first framing**: Hero copy on coin flip, dice, number wheel, and 1–10 generator should reference classroom use. "No install, no student accounts, runs on any school device" is a real value prop that competitors underuse.
- **Hub cross-linking**: Every tool links back to `/number-chance/` and shows 3–4 related tools. This builds the cluster's topical authority faster than isolated pages.

### Skip for v1 (add based on engagement data)
- Cryptographic randomness (`crypto.getRandomValues()`) — Math.random() is sufficient for all these use cases; adding crypto RNG adds complexity without user-visible benefit
- OBS/streaming integration — relevant for Wheel of Names eventually but not launch
- Gamification (streaks, points, betting) — only if engagement metrics show users returning repeatedly
- Sound effects — adds complexity and accessibility concerns
- localStorage persistence — adds complexity; ship without, add if users request it

---

## Linkable resource strategy — features that earn backlinks

The ROAST audit identified the absence of linkable assets as the ceiling on domain authority. Tools that get linked aren't just functional — they do something memorable that makes a blogger, teacher, or developer say "I need to send people here."

### What makes a tool linkable

1. **Does something no one else does** — one feature that's genuinely novel in the category earns more links than ten table-stakes features
2. **Produces sharable output** — if the result can be sent to someone, it will be
3. **Has educational depth that can be cited** — a stats panel, probability explainer, or simulation that shows real math gives teachers and bloggers a reason to reference the page
4. **Serves a niche perfectly** — the tool that is THE best option for D&D coin flips, or THE best classroom number picker, earns repeat links from that community
5. **Embeds or prints cleanly** — teachers link to tools they can put on a smartboard or print as a worksheet

### Innovative feature ideas by tool (not yet seen in the wild at scale)

**Coin Flip:**
- **"Decision mode"** — user types two options ("Pizza / Tacos"), coin decides between them and shows the chosen option as the result (not just heads/tails). No competitor offers this on the coin flip page itself. Teachers and journalists would link to it.
- **Convergence visualizer** — run flips continuously and watch a live chart converge toward 50/50 in real time. Shows the Law of Large Numbers visually. Education bloggers and stats teachers will cite and link this.
- **"Best of N" mode** — flip until one side wins 3 (or 5, or 7) times — like a sports series tiebreaker. No one has built this. Sports sites would link to it.
- **Shareable result URL** — after a flip, URL updates to `?result=heads&seed=8274`. Anyone can verify the result wasn't manipulated. Useful for online game tiebreakers; people share these links.

**Random Number Generator:**
- **"No-repeat pool mode"** — generate N unique numbers from a range with no duplicates, then mark pool as exhausted. Teachers use this to call on each student exactly once. No mainstream tool presents this as a one-click mode.
- **"Blind pick for two players"** — both players type a guess, reveal simultaneously. Higher/lower wins. Zero-dependency game built into the page. Shareable.
- **Distribution panel** — after 10+ generates, show a mini histogram of your session's results. Instant proof the generator isn't biased. Educators and skeptics will share tools that show this.
- **"Exclude numbers" field** — skip specific numbers in the range (e.g., exclude 13 for superstitious office raffles). Niche but memorable; people mention it in blog posts.

**Dice Roller:**
- **Dice expression parser** — type `2d6+3` or `1d20 advantage` and the tool evaluates it. D&D and tabletop RPG communities link to tools that speak their notation natively. Reddit posts alone could drive thousands of visits.
- **Custom die faces** — define any values on any die (e.g., D6 with faces: 1,1,2,3,5,8 — the "Fibonacci die" used in Agile poker). No competitor does this without an account. Dev and design blogs would link it.
- **Roll log export** — copy your full session roll history as text for D&D session notes. Players would bookmark and share this.
- **Advantage/Disadvantage mode** — roll 2d20, highlight the higher (Advantage) or lower (Disadvantage) automatically. Single most-requested D&D digital tool; currently requires a separate page on most sites.

**Wheel of Names:**
- **"Round robin mode"** — spin once, winner is removed, spin again until all names have been picked once. Generates a complete random order. Classroom teachers and event organizers need this every week. wheelofnames.com buries this feature; make it a first-class mode.
- **Import CSV / paste list** — paste a comma-separated list or one name per line from Google Sheets. Teachers use Google Sheets for rosters; this bridges the gap instantly.
- **Shareable wheel URL** — names encoded in URL params so teachers can bookmark and reopen the same class list. One of the top-requested features that wheelofnames.com handles poorly (requires account).
- **Printable spinner PDF** — generate a printable blank spinner students can cut out and use physically. No digital tool offers this. Elementary school teachers would link from Pinterest and TPT.

**Flip a Coin Multiple Times:**
- **Streak tracker** — shows longest current heads/tails streak and all-time longest streak in the session. Gamblers' fallacy explainer tied to it ("A streak of 7 heads doesn't change the next flip"). Stats and psychology educators would cite this.
- **"First to N heads wins" mode** — two players, flip until one side hits N. Gamified tiebreaker used in board games. Shareable result.
- **Export as table** — copy the full flip sequence as a table (flip #, result, running %). Statistics teachers use this for homework exercises and will link to a tool that produces clean exportable data.

**Powerball Generator:**
- **"Office pool generator"** — one click generates N unique sets of picks (e.g., 10 sets for 10 coworkers), formatted as a printable ticket sheet. HR people organizing office pools would share this link every week the jackpot is big.
- **Historical frequency context** — show which numbers have come up most often in real Powerball history (link to public draw data). Makes the page a reference, not just a tool.

### Implementing linkable features — instructions for Claude Code

When building each tool, include this directive in every prompt:

> Before writing any code, search the web for the top 5 competitors for this tool. For each one, list what features they have and — more importantly — what features they're missing. Then implement the standard table-stakes features first, and add **at least two features from the innovative ideas list above** (or propose new ones) that no current competitor has. The goal is to build the tool that educators, bloggers, and community sites would link to as the definitive version of this tool. Document which novel features you added and why they're link-worthy.

---

## Bug fixes required (do before Wave 1 launches)

1. **Fix `/coin-flip/` canonical** — currently serving homepage content
2. **Fix `/random-number-generator/` canonical** — currently serving homepage content
3. **Fix `/dice-roller/` canonical** — currently serving homepage content
4. **Verify `/number-chance/` hub** — check the hub page itself renders with correct canonical and all hub card links resolve (not 404)
5. **Add _redirects entries** — ensure `/coin-flip` (no trailing slash) redirects to `/coin-flip/`

These are Stage 0 work but they block the value of Wave 1 traffic. Fix them on the same PR as the first tool launch.

---

## Internal linking plan

Every tool page must include:
- Breadcrumb: Wordineer → Number & Chance Tools → [Tool Name]
- "More number & chance tools" section linking to 3–5 sibling tools (inject from tools.json grid)
- Canonical back-link to `/number-chance/` hub in the breadcrumb

The hub page (`number-chance.html`) must update each "Coming soon" card to a live link as each tool ships. Update hub + tools.json in the same PR as each tool.

---

## Success metrics (Stage 1 is "done" when)

- All 32 tool pages are live at their canonical URLs with no broken redirects
- The 3 previously broken URLs (`/coin-flip/`, `/random-number-generator/`, `/dice-roller/`) return 200 with correct canonicals
- All hub "Coming soon" badges are replaced with live links
- Search Console shows the new pages indexed within 2 weeks of launch
- **Traffic milestone at 90 days:** 2,000+ organic visits/month to the `/number-chance/` cluster
- **Traffic milestone at 180 days:** 8,000–15,000 organic visits/month to the cluster

---

## Claude Code prompts (paste to start each tool)

Each prompt includes a research step. Before writing any code, Claude should search the web for the top competitors for that tool, identify feature gaps, and implement at least two novel features from the linkable resource list above that no current competitor offers. The goal is best-in-class — not just functional.

---

### Coin Flip
```
Build the coin flip tool at template-deploy/tools-src/coin-flip.html.
Follow the CONFIG + SLOT structure from an existing tool-src file.
CONFIG: { "type": "tool", "url": "/coin-flip/", "output": "coin-flip.html" }

FIRST: Search the web for "flip a coin online" and "coin flip tool". List the top 5 results, what features each has, and what they're missing. Then implement the features below PLUS at least two features from this list that no competitor currently has:
- Decision mode: user types two options, coin picks one (shows the chosen option as the result, not just heads/tails)
- Convergence visualizer: live chart showing heads% and tails% converging toward 50/50 as flips accumulate
- "Best of N" mode: flip until one side wins 3 (or 5 or 7) times — series tiebreaker format
- Shareable result URL: after flip, URL updates with ?result=heads so the result can be shared/verified

Base tool UI (required):
- Animated coin SVG (CSS flip animation — no library)
- Large FLIP button (keyboard: Space/Enter triggers it)
- Result: "Heads" or "Tails" in large text, color-coded
- Session counter: Heads: N | Tails: N
- History strip: last 10 H/T chips
- Copy result button

No localStorage. No sound. No external dependencies. Pure HTML/CSS/JS in the init slot.
Document which novel features you added and why they make this the most linkable coin flip tool on the web.
State how you'll verify it works before calling it done.
```

---

### Random Number Generator 1–100
```
Build the random number 1–100 generator at template-deploy/tools-src/random-number-1-100.html.
CONFIG: { "type": "tool", "url": "/random-number-1-100/", "output": "random-number-1-100.html" }

FIRST: Search the web for "random number generator 1 to 100". List the top 5 results, what features each has, and what gaps exist. Then implement the features below PLUS at least two novel features from this list that no competitor currently has:
- No-repeat pool mode: generate numbers from the range without duplicates until the pool is exhausted, then reset — teachers use this to call on every student exactly once
- Distribution panel: after 10+ generates, show a mini histogram of your session results (proves fairness, educators and skeptics will share it)
- Exclude numbers field: enter numbers to skip in the range (e.g., skip 13) — niche but memorable
- Blind pick for two players: both type a guess, reveal simultaneously, higher wins — zero-dependency game built into the page

Base tool UI (required):
- Giant number display (result, 72px+ font)
- GENERATE button (Space/Enter trigger)
- Quick-range pills: 1–10, 1–50, 1–100, 1–1000 (linking to the relevant range pages)
- Copy button
- History strip: last 10 results as chips, newest left

Server-render: static HTML includes "42" as example result.
This is the canonical template all range variants will clone — build it exceptionally well.
Document which novel features you added and why they make this more linkable than random.org or random-number-generator.com.
State how you'll verify it works before calling it done.
```

---

### Dice Roller
```
Build the dice roller at template-deploy/tools-src/dice-roller.html.
CONFIG: { "type": "tool", "url": "/dice-roller/", "output": "dice-roller.html" }

FIRST: Search the web for "dice roller online" and "virtual dice D&D". List the top 5 results, what features each has, and what the tabletop RPG community is still missing. Then implement the features below PLUS at least two novel features from this list that no competitor currently has:
- Dice expression parser: type "2d6+3" or "1d20 advantage" and evaluate it — D&D communities link to tools that speak their notation natively
- Advantage/Disadvantage mode: roll 2d20 automatically, highlight the higher (Adv) or lower (Dis) die — most-requested D&D digital feature
- Custom die faces: user defines values on any die (e.g., faces: 1,1,2,3,5,8 for Fibonacci/Agile poker die) — dev and design blogs would link to this
- Roll log export: copy full session history as text for D&D session notes — players would bookmark and share this

Base tool UI (required):
- Die type selector: D4, D6, D8, D10, D12, D20 (toggle buttons, D6 default)
- Quantity: 1–4 dice (+ / - buttons)
- ROLL button (Space/Enter/R trigger)
- D6 face: SVG dot pattern (1–6 pips)
- Other dice: show number in die outline SVG
- Result: each die value + sum total
- History: last 10 rolls (die type + result)

No 3D animation. No sound required for v1.
Document which novel features you added and why the tabletop RPG community will share this over competitors.
State how you'll verify it works before calling it done.
```

---

### Wheel of Names
```
Build the Wheel of Names tool at template-deploy/tools-src/wheel-of-names.html.
CONFIG: { "type": "tool", "url": "/wheel-of-names/", "output": "wheel-of-names.html" }

FIRST: Search the web for "wheel of names" and "classroom name spinner". List the top 5 results (especially wheelofnames.com), what features they have, and what teachers and event organizers are still asking for. Then implement the features below PLUS at least two novel features from this list that no competitor currently handles well:
- Round robin mode: spin once → winner is removed → spin again until all names drawn → produces a complete random order. Teachers need this weekly for presentations. wheelofnames.com buries this; make it a first-class mode with a clear toggle.
- Shareable wheel URL: encode names in URL params (?names=Alice,Bob,Carol) so teachers can bookmark and reopen the same class list without an account. Top complaint about every competitor.
- Import from paste: paste a comma-separated list or one name per line from Google Sheets/Excel. Teachers live in spreadsheets; this removes the biggest friction point.
- Printable spinner: generate a print-friendly blank spinner students can cut out and use physically — elementary teachers would share this on Pinterest and Teachers Pay Teachers.

Base tool UI (required):
- Canvas-based spinning wheel (browser Canvas API, no library)
- Names textarea: paste or type names one per line
- SPIN button — easing animation (3–5 second spin, decelerates realistically)
- Winner overlay/modal shown after spin with winner's name
- "Remove winner and spin again" option
- Color segments auto-assigned from palette, adjusts to name count

Document which novel features you added and why classroom teachers and event organizers will link to this over wheelofnames.com.
State how you'll verify it works before calling it done.
```

---

### Flip a Coin 10 Times
```
Build the 10-flip coin tool at template-deploy/tools-src/flip-a-coin-10-times.html.
CONFIG: { "type": "tool", "url": "/flip-a-coin-10-times/", "output": "flip-a-coin-10-times.html" }

FIRST: Search the web for "flip a coin 10 times". List the top 5 results and identify what's missing — especially features that stats teachers or people testing probability would want. Then implement the features below PLUS at least two novel features from this list:
- Streak tracker: show longest current heads streak and tails streak, with a one-line Gamblers' Fallacy callout ("A 7-flip streak doesn't change the next flip"). Statistics and psychology educators cite tools that teach this.
- "First to N heads wins" mode: flip until one side reaches N — sports series/tiebreaker format. Shareable result ("Heads wins the series 3–1 after 6 flips").
- Export as table: copy the full 10-flip sequence as a markdown/plain-text table (Flip #, Result, Running H%, Running T%) for statistics homework use.

Base tool UI (required):
- "Flip All 10" button — runs 10 flips in sequence with brief visual delay
- Results grid: 10 coin icons showing H or T
- Running tally updating in real time
- Final summary: "Heads: 7 | Tails: 3 | 70% heads"
- "Flip Again" resets and re-runs
- Copy result button

This page is the template for the 5x, 100x, and 1000x variants — make the structure clean and parameterized.
Document which novel features make this the tool that stats teachers link to.
State how you'll verify it works before calling it done.
```

---

### Flip a Coin 100 Times
```
Build the 100-flip coin tool at template-deploy/tools-src/flip-a-coin-100-times.html.
CONFIG: { "type": "tool", "url": "/flip-a-coin-100-times/", "output": "flip-a-coin-100-times.html" }

FIRST: Search the web for "flip a coin 100 times" and "law of large numbers simulator". List the top 5 results and what they offer. The primary use case here is statistics and probability education. Implement the features below PLUS at least one feature that makes this the most cited statistics demonstration tool for this topic:
- Live convergence line chart: as each of the 100 flips is added, draw a line showing heads% approaching 50%. This is the Law of Large Numbers made visual — stats teachers will link to it in their course materials.
- "Run again and compare" overlay: run a second simulation and overlay its convergence line in a different color on the same chart. Shows that variance between runs shrinks as N grows.
- Streak analysis: after the run, report the longest heads and tails streaks and contextualize ("In 100 flips, a streak of 7 or more is expected about 80% of the time").

Base tool UI (required):
- "Run 100 Flips" button — instant calculation (no per-flip animation at this volume)
- Result grid of 100 coins as small H/T chips in a 10×10 grid
- Distribution bar chart (visual heads vs. tails split)
- Stats summary: "Heads: 52 | Tails: 48 | 52% heads"
- "Run Again" button
- Copy stats button

Hero copy angle: "See how close to 50/50 you actually get." — lean into the stats/education framing.
Document which features make this the tool stats teachers cite in their lessons.
State how you'll verify it works before calling it done.
```

---

### Number Generator (Custom Range)
```
Build the custom range number generator at template-deploy/tools-src/random-number-generator.html.
CONFIG: { "type": "tool", "url": "/random-number-generator/", "output": "random-number-generator.html" }

NOTE: This URL is currently BROKEN (serving homepage with wrong canonical). This is a critical fix — treat the canonical and meta setup carefully.

FIRST: Search the web for "random number generator" (head term). List the top 5 results, what features they have, and where they fall short. This is the highest-competition page in the cluster — implement the base features plus at least two novel features that help it stand out:
- No-repeat pool mode (same as 1–100 page): generate from a custom range without duplicates until pool exhausted — ideal for teachers
- Distribution panel: histogram after 10+ results showing frequency per number (proves fairness; shareable proof)
- "Generate a list" mode: choose N numbers at once — get 5, 10, or 20 random numbers from the range in one click, formatted as a copyable list
- Quick-range pills: 1–10, 1–50, 1–100, 1–1000 that fill the min/max instantly, plus links to the dedicated pages

Base tool UI (required):
- Min/max input fields (default: 1 and 100)
- GENERATE button (Space/Enter trigger)
- Giant result display
- Copy button
- History strip: last 10 results

Document which novel features you added and why this outranks random.org's number generator.
State how you'll verify it works before calling it done.
```

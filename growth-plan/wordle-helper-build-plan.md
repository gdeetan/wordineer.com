# Wordle Helper — Planning Brief & Build Prompts

## 1. Strategic summary

**Target page:** `/wordle-helper.html`
**Cluster:** Word Games (sits alongside Pictionary generator, Scattergories, Scrabble word finder)
**Primary intent served:** tool intent — "wordle solver," "wordle helper," "wordle answer finder"
**Secondary intent absorbed:** "best wordle starting words" gets answered *inside* the tool (interactive starting-word picker) instead of as a competing standalone page, so it reinforces this page's topical authority rather than splitting it.

**The wedge:** every competitor tool filters a word list. None of the free ones actually rank "what should I guess next" by real information value. We build the entropy engine NYT paywalled, ship it free, and say so.

---

## 2. Competitive audit (scanned live, June 2026)

| Site | What it does | Gap |
|---|---|---|
| TryHardGuides Wordle Solver | 3-box green/yellow/gray filter, "common letters" counter | No ranking logic — just a filtered list |
| WordFinder (yourdictionary) | Same 3-box pattern, scrabble-tool styling reused | Generic, ad-heavy, no differentiation |
| word.tips | Filter + static "best starting words" article bolted on | Two disconnected experiences, not one tool |
| CapitalizeMyTitle | Basic filter form | Thin, no unique data |
| wordlesolver.pro | Frequency-sorted results, stats dashboard, multi-length solver | Closest competitor — frequency sort is a real feature, but still no entropy-based recommendation |
| wordlesolver.app | Cites WordleBot/MIT/entropy research in prose | Talks about the math, doesn't run it |
| PerThirtySix | Click-to-filter visualization, color-coded by frequency | Best UX of the bunch, but it's a static archive explorer, not a live turn-by-turn coach |
| NYT WordleBot | The real thing — entropy-based "skill/luck" scoring per guess | Paywalled behind NYT subscription |

**Conclusion:** the open competitive set tops out at "filter + sort by frequency." Nobody free is doing live expected-information-gain ranking. That's our build.

---

## 3. The differentiation, concretely

1. **Entropy-ranked "best next guess"** — after each guess, the tool doesn't just list what still fits; it computes which remaining word would, on average, eliminate the most possibilities, and shows it first with a plain-English reason ("narrows the field the most").
2. **Tile-grid input**, not three text boxes — five letter cells per row, click a tile to cycle gray → yellow → green, type to fill letters. Matches how people already think about Wordle and is faster on mobile than three separate fields.
3. **Built-in starting-word picker** — a curated, entropy-ranked opener list lives inside Step 1 of the tool itself (click a word to drop it straight into row one), not a separate blog post. This is what absorbs "best wordle starting words" search intent.
4. **Honest dictionary framing** — copy explicitly says we don't pretend to know NYT's current answer pool; we work from the full accepted-word dictionary and rank by real-world frequency. Differentiates from competitors still citing a static 2,309-word list as gospel.
5. **No ads inside the tool card itself** — ad placements stay in the existing strip/rect slots around the tool, consistent with current pages. Clean tool UX → better dwell time → better long-run rankings.
6. **Clear "not affiliated with NYT" disclaimer** — standard across this niche, keeps us on safe ground re: Wordle's trademark.
7. **Practice Mode** — a self-contained playable round where the site itself picks the secret word and auto-scores your guesses, so a first-time visitor understands and trusts the tool in under a minute without needing an external Wordle game open at all. This is also the cleanest possible live demo of the recommendation engine, since the answer is genuinely known to the tool. It directly solves a problem every competitor tool just assumes away: a cold visitor has no idea they're expected to already be mid-game elsewhere.

---

## 4. Page architecture (matches existing SLOT system)

- **SLOT:meta** — Title: `Wordle Helper — Free Solver & Best Starting Words | Wordineer`. Meta description leads with the free/no-paywall angle. JSON-LD: `FAQPage` + `WebApplication` (applicationCategory: GameApplication).
- **SLOT:hero** — H1 "Wordle Helper," subhead emphasizing "the free alternative to WordleBot," with a persistent "How it works" 3-step strip directly beneath it.
- **SLOT:tool** — two-tab toggle: "Solve My Game" (6-row × 5-tile grid, live candidate count, "Best next guess" panel, starting-word picker) for people playing a real Wordle elsewhere, and "Practice Mode" (same grid, auto-scored against a tool-picked secret word) so first-time visitors can use and trust the tool with nothing else open. Both tabs share the same scoring and ranking logic.
- **SLOT:explainer** — How to use it; how the entropy ranking works (plain English, no jargon dump); why we don't rely on the old 2,309 list; who uses it (streak-savers, teachers, Quordle/Dordle players).
- **SLOT:faq** — Includes "best wordle starting words," "is using a solver cheating," "does this work for Dordle/Quordle/Octordle," "how does the recommendation work," matched 1:1 to the FAQPage schema.
- **SLOT:who** — reuse the existing 4-card pattern (streak-savers / teachers using it for vocab / casual players / data-curious players).
- **SLOT:init** — calls the new engine's `init()`.

---

## 5. Data architecture

**New files, built from your existing pipeline (not copied from any single competitor's compiled list):**

- `data/wordle-guesses.json` — full list of valid 5-letter English words usable as a guess (~10–13k words). Build by filtering your existing WordNet/NLTK source down to 5-letter entries, the same pipeline already used for `words.json`.
- `data/wordle-openers.json` — precomputed top ~40 starting words with entropy scores and a one-line "why," generated offline (Python script, see Session 2) using `wordfreq` for frequency weighting — same library already used for difficulty scoring elsewhere in the project.

This keeps the dataset originally yours rather than a redistributed third-party file, and reuses tooling you already have installed.

---

## 6. Build sequencing

**Session 1 — Core tool, basic ranking, full page/SEO shell.** Self-information ranking computed live in-browser against the remaining candidate pool only (cheap — pool shrinks fast after guess 1). Ships a fully working, correct, good-enough solver.

**Session 2 — True entropy upgrade + offline precompute.** Adds the Python script that computes entropy against the *entire* guess dictionary (not just remaining candidates) for genuinely optimal recommendations, generates `wordle-openers.json`, and wires the live engine to use full-dictionary entropy for early turns where it matters most.

Splitting this way avoids context overload in one session and means you have a shippable v1 after Session 1 even if Session 2 slips.

---

## 7. Claude Code Prompt — Session 1 (paste-ready)

```
CONTEXT
I'm adding a new tool to Wordineer (wordineer.com), a static site built via
build.py + tools.json + tools-src/*.html using a SLOT-based template system
(SLOT:meta, SLOT:style, SLOT:hero, SLOT:tool, SLOT:explainer, SLOT:faq,
SLOT:who, SLOT:init). Read tools-src/random-word-generator.html and
tools-src/random-sentence-generator.html first as exact structural models —
match their CONFIG block format, slot markup conventions, CSS class naming,
and JS init pattern precisely. Also read tool-engine.js, global.css, nav.html,
footer.html, head.html and more-tools.html before writing anything, so the
new tool matches existing UX and visual identity exactly (CSS variables only,
no new color literals, DM Sans / DM Serif Display typography, sticky nav,
mega menu, toast pattern, FAQ accordion, ad-strip placements).

GOAL — Session 1 of 2
Build a new tool page: "Wordle Helper" at tools-src/wordle-helper.html,
output /wordle-helper.html. This is a Wordle solver/helper that goes beyond
competitors' simple green/yellow/gray filter tools by recommending the
single best next guess, not just a filtered list. Session 1 covers the full
page, a tile-grid input UI, correct clue-matching logic, a "best next
guess" ranking computed against the remaining candidate pool (self-
information scoring), AND two usage modes (see SLOT:tool): "Solve My Game"
for people bringing clues from an external Wordle they're already playing,
and "Practice Mode," a self-contained playable round where the tool picks
its own secret word so first-time visitors can understand and trust the
tool without needing anything open elsewhere. This second mode matters —
without it, a cold visitor has no way to know they're expected to already
be mid-game somewhere else, which is a real confusion every competitor tool
just ignores. Session 2 (separate, later) will upgrade the ranking to
full-dictionary entropy and add a precomputed starting-word list — don't
build that part now, but leave a clean integration point (see "Future hook"
below).

DATA TO BUILD FIRST
Create data/wordle-guesses.json: an array of valid 5-letter English words
usable as Wordle guesses. Derive this from the project's existing word
sourcing approach (WordNet/NLTK, same as words.json) — filter to exactly
5 letters, alphabetic only, common dictionary words. Aim for a
comprehensive list (several thousand entries) rather than a small curated
set, since the tool needs to recognize any word a real player might type.
Store as a flat JSON array of lowercase strings, e.g. ["about","abuse",...].
Do not copy this from any single external site's compiled list — generate
it from the project's own dictionary sources.

Also create data/wordle-common.json: a subset of the above, filtered to
words above a frequency threshold (use wordfreq if available in the
project's tooling, otherwise a reasonable heuristic), representing
"plausible answer" words as opposed to obscure valid guesses. This powers
which words get suggested vs. which are merely accepted as valid input.

PAGE CONTENT (tools-src/wordle-helper.html)

SLOT:meta
- Title: "Wordle Helper — Free Solver & Best Starting Words | Wordineer"
- Meta description leading with "free, no sign-up, no paywall" — this is
  the differentiator vs. NYT's paywalled WordleBot.
- Canonical: https://wordineer.com/wordle-helper.html
- OG tags matching the pattern in random-word-generator.html
- JSON-LD: combine an FAQPage schema (questions matching SLOT:faq exactly)
  with a WebApplication schema (applicationCategory: "GameApplication",
  offers: free).

SLOT:style
- Tile grid: 6 rows x 5 cells, each cell a square button-like div, large
  letter display, three visual states (default/empty, "present" / yellow-
  equivalent, "correct" / green-equivalent, "absent" / gray-equivalent).
  IMPORTANT: do not literally copy NYT Wordle's exact tile colors. Use the
  project's own palette for these three states — green family (--green,
  --green-light, --green-dark) for "correct," amber family (--amber,
  --amber-light) for "present," and a neutral (--bg-3 / --text-3 / --border)
  treatment for "absent." This keeps the UI on-brand and avoids mimicking
  Wordle's specific visual trade dress.
- Style the "best next guess" recommendation panel as a highlighted card
  (similar visual weight to the existing aff-writing / saved-strip
  components) so it draws the eye as the primary output of the tool.
- Starting-word picker: a simple chip/pill list of words, clickable, same
  pattern as existing tag-style UI elements in the codebase if one exists,
  otherwise a clean new minimal chip component using existing CSS vars.
- Mobile: tile grid must scale down gracefully; follow the same
  mobile-more-toggle collapse pattern used in random-word-generator.html
  for any secondary controls (e.g. "show full candidate list" toggle).

SLOT:hero
- H1: "Wordle Helper"
- Subhead emphasizing: free, no sign-up, recommends your best next guess
  (not just a filtered list), no paywall.

SLOT:tool
- IMPORTANT, READ FIRST: this is the section that solves "how does a
  first-time visitor know what word they're even trying to find" — a
  question every competitor tool quietly ignores. Before any tile grid,
  render a persistent "How it works" strip (3 short numbered steps, small
  icons, always visible, not collapsed or buried below the fold):
    1. Pick a starting word (or type your own)
    2. Play it in your Wordle game and note the colors you get back
    3. Enter those colors here for your best next guess
  Next to this strip, a small quiet outbound link: "Don't have a Wordle
  open? Play today's puzzle on NYT ↗" (target="_blank" rel="noopener
  nofollow", styled as a secondary link, not a CTA — the goal is to be
  genuinely useful to a confused visitor, not to look like we're sending
  business away reluctantly).

- Directly below that strip, a two-tab toggle:

  TAB A — "Solve My Game" (default/active tab)
  For visitors already playing a real Wordle elsewhere (NYT, a clone, on
  paper with friends) who are bringing their own clues here.
    - Step 1 state (no guesses yet): show the starting-word picker — a
      hardcoded list of ~15-20 well-known strong openers (e.g. SLATE,
      CRANE, TRACE, ADIEU, RAISE — publicly known strategy words, framed
      as "popular high-coverage openers" since this is a Session 1
      placeholder; Session 2 replaces it with the precomputed
      entropy-ranked list). Clicking a word fills it into guess row 1,
      but the user can also just type their own first guess directly.
    - 6 rows x 5 tiles. A one-line caption above row 1 makes the
      expectation explicit: "Enter the colors Wordle gave you for this
      guess." User types a letter into the active tile; clicking a
      filled tile cycles its clue state through absent -> present ->
      correct -> absent. An explicit "Submit guess" button per row (or
      auto-advance on 5th letter + Enter) locks that row's letters+states
      into guess history and advances to the next row.
    - Reject invalid guesses (5 letters not found in wordle-guesses.json)
      with an inline error matching the existing count-error /
      input-error visual pattern from random-word-generator.html.
    - Live "Possible answers remaining: N" counter, updating after each
      guess.
    - "Best next guess" panel: top-ranked recommended word plus a
      one-line plain-English reason (e.g. "Tests 5 new letters not yet
      tried" or "Narrows the remaining field the most"). Below it, a
      collapsible "Show all N possibilities" list (collapsed by default
      if N is large, matching the mobile-more-toggle collapse pattern).
    - "Start over" button resets all rows and the picker state.

  TAB B — "Practice Mode" (new — this is what actually fixes the "how do
  I know the word" problem rather than just explaining around it)
  A fully self-contained playable round: the tool itself picks a secret
  word at random from wordle-common.json and auto-scores every guess —
  no external game needed at all. This exists so a first-time visitor can
  understand and trust the tool in under a minute on this page alone, and
  it doubles as the cleanest live demo of the recommendation engine,
  since the answer is genuinely known to the tool and the "best next
  guess" panel can be shown working correctly in real time.
    - "New practice word" button picks a fresh secret word and resets
      the grid.
    - Same 6x5 grid and typing UX as Tab A, but the user only types
      letters — clue colors are computed automatically against the
      secret word using the same pattern function as Tab A (do not
      duplicate the logic; both tabs must call the same function).
    - Same "Best next guess" panel, available as an optional hint —
      label it clearly as a hint, not forced.
    - On a correct guess: a clean "Solved in N guesses!" message + "New
      practice word" button. After 6 incorrect guesses: reveal the
      secret word and offer "Try again."
    - Copy here must never imply this is "today's Wordle" or "today's
      answer" — call it "Practice Mode" / "a random word to try the tool
      on." Conflating it with the real daily puzzle would undermine the
      honesty angle in SLOT:explainer.

- A small "Not affiliated with the New York Times" disclaimer near the
  tool footer, visible regardless of which tab is active.

CORE LOGIC (new file: scripts/wordle-engine.js, separate namespace
WORDLE_HELPER, following the IIFE + exposed-methods pattern used in
tool-engine.js — do not modify tool-engine.js itself)

1. Pattern function — given a guess and a target word, return a 5-element
   array where 2=correct (green), 1=present-wrong-position (yellow),
   0=absent (gray). MUST handle duplicate letters correctly using the
   standard two-pass algorithm:
   - Pass 1: mark exact position matches as correct (2), and mark those
     target letter positions as "used."
   - Pass 2: for remaining guess letters (not yet marked correct), check
     if that letter exists in an unused target position; if so mark
     present (1) and consume that target position; otherwise mark absent
     (0).
   This is the single most common bug in clone Wordle solvers — get this
   exactly right and write a few inline test cases as comments showing
   correct handling of a guess with a repeated letter against a target
   with only one occurrence of that letter.

2. Candidate filtering — given the full guess history (list of
   {word, pattern}), filter the candidate pool (start from
   wordle-common.json, fall back to wordle-guesses.json if needed) to only
   words where computing the pattern function against every past guess in
   the history reproduces that guess's recorded pattern exactly.

3. Ranking (Session 1 version — self-information against remaining pool
   only): for each remaining candidate word as a hypothetical next guess,
   compute the distribution of patterns it would produce across all OTHER
   remaining candidates (treating each as a possible true answer), then
   score it by Shannon entropy: sum over each resulting pattern group of
   -(group_size/total) * log2(group_size/total). Rank candidates
   descending by this score and surface the top one as "Best next guess,"
   with the rest available in the expandable full list. This is a
   reasonable approximation since it only tests words from the remaining
   pool itself (not the full outside dictionary) — note in a code comment
   that Session 2 will extend this to test arbitrary words from the full
   guess dictionary as well, which sometimes yields better "probe" words
   not in the remaining pool.

4. FUTURE HOOK: structure the ranking function as
   rankCandidates(remainingPool, fullGuessDictionary) so that Session 2
   can swap in full-dictionary entropy scoring without restructuring the
   calling code. For now fullGuessDictionary can be ignored/unused inside
   the function body, but keep the parameter in the signature.

5. Performance: candidate pools after guess 1 are typically small (well
   under 1000 words), so an O(n^2) entropy pass in plain JS is fine. Only
   guard against pathological cases (e.g. if remaining pool is empty due
   to a contradictory input) with a friendly inline message rather than
   letting the UI break.

6. Practice Mode logic — pickRandomSecret() selects a word from
   wordle-common.json. On each Practice Mode guess submission, call the
   SAME pattern function from point 1 (secret word as the "target,"
   typed word as the "guess") to compute tile colors automatically — do
   not write a second scoring implementation. Track guess count for the
   "Solved in N guesses!" message and cap at 6 rows like Tab A. The
   "Best next guess" panel in Practice Mode calls the same
   rankCandidates() used in Tab A, filtered by Practice Mode's own guess
   history — both tabs share the ranking and pattern functions; only the
   source of clue colors differs (user-set in Tab A, computer-set in Tab
   B). Switching tabs should not carry guess history between them — each
   tab keeps its own independent state.

SLOT:explainer
- "How to use the Wordle Helper" — short numbered steps.
- "How the recommendation works" — plain-English paragraph on the entropy
  concept, no equations: frame it as "we test every remaining word against
  every other remaining word and find the one most likely to narrow things
  down fastest, the same idea NYT's WordleBot uses internally."
- "Why we don't rely on the old 2,309-word answer list" — short paragraph,
  honest framing: NYT no longer restricts answers to the original public
  list, so any solver pretending to know the answer pool is just guessing;
  this tool ranks by real-world word frequency instead.
- "Who uses this" subsection feeding into SLOT:who.

SLOT:faq (write matching FAQPage JSON-LD exactly)
- "How do I know what word I'm trying to guess?" — direct answer: if
  you're playing the real Wordle (NYT or elsewhere), play your guess
  there first, then enter the colors it gives you under "Solve My Game."
  If you just want to try the tool without an active game, switch to
  "Practice Mode" and it'll pick a word for you automatically.
- "What are the best Wordle starting words?" — answer references the
  in-tool picker, gives 2-3 named examples with one-line reasons.
- "Is using a Wordle solver cheating?" — even-handed, non-judgmental
  framing (learning tool / streak-saver framing, respect the player's
  choice).
- "Does this work for Dordle, Quordle, or Octordle?" — honest answer for
  Session 1: not yet, single-board only (avoid overpromising).
- "How is this different from other Wordle solvers?" — directly state the
  best-next-guess ranking differentiator vs. plain filter tools.
- "Is this affiliated with the New York Times?" — clear no, independent
  tool.

SLOT:who — 4 cards: streak-savers, teachers (vocabulary angle, ties to
existing word-tools cross-links), casual players, data-curious players who
like seeing the reasoning.

SLOT:init — wire up WORDLE_HELPER.init() with whatever element IDs the
markup above needs (grid container, candidate-count display, recommendation
panel, starting-word picker container, reset button). Also call the
existing initFaq/initMega equivalents if those live in a shared place
rather than tool-engine.js — check how random-sentence-generator.html
wires this up if it differs from random-word-generator.html.

INTEGRATION
- Add an entry to tools.json for this tool (match existing tool entry
  shape — check an existing entry for the exact fields used, e.g. name,
  url, icon, description, category).
- Add a card to more-tools.html's tools grid (or the relevant category
  grid) linking to /wordle-helper.html.
- Add the new wordle-engine.js script tag to wordle-helper.html's own
  output (do not add it globally to footer.html, since other tools don't
  need this engine).

ACCEPTANCE CRITERIA
- Page builds via build.py without errors and matches the visual language
  of existing tool pages (nav, footer, ad slots, typography, spacing).
- A first-time visitor with no Wordle game open anywhere can still
  understand and use the page within seconds, via the "How it works"
  strip and/or Practice Mode — this is the main thing to manually verify.
- Tab switching works cleanly and keeps each tab's guess history fully
  independent (no bleed-through between Solve My Game and Practice Mode).
- Practice Mode's auto-scoring and Tab A's manual scoring visibly use the
  identical pattern function (verify by checking the code, not just the
  UI) — no duplicated/divergent scoring logic.
- Tile grid is usable via both click-to-cycle and keyboard typing.
- Duplicate-letter clue logic is verifiably correct (include the test
  cases mentioned above).
- Invalid words are rejected with a clear inline error, not a silent
  failure.
- "Best next guess" updates correctly after every submitted row in both
  tabs and matches a manual sanity check (e.g. after a guess with no
  greens or yellows, the candidate pool should shrink to exclude every
  letter in that guess).
- Mobile layout doesn't break the tile grid, tab toggle, or controls.
- FAQ content in the visible page matches the FAQPage JSON-LD exactly.
- No literal Wordle/NYT tile colors used — confirm the three clue states
  use the project's existing CSS variables, not new hardcoded hex values.
```

---

## 8. Claude Code Prompt — Session 2 (paste-ready, run after Session 1 ships)

```
CONTEXT
Wordle Helper (tools-src/wordle-helper.html, scripts/wordle-engine.js) is
live from Session 1. It currently ranks the "best next guess" using
self-information computed only against the remaining candidate pool. This
session upgrades that to true entropy scoring against the full guess
dictionary, and adds a precomputed, entropy-ranked starting-word list to
replace the Session 1 placeholder picker.

GOAL
1. Write a standalone Python script (scripts/compute_wordle_openers.py,
   not shipped to the browser, run once locally) that:
   - Loads data/wordle-guesses.json (full valid-guess dictionary) and
     data/wordle-common.json (frequency-filtered plausible-answer pool).
   - For a sample of candidate opening words (the full guess dictionary if
     performance allows, otherwise a few thousand of the most common
     5-letter words as a reasonable approximation), computes the Shannon
     entropy of the pattern distribution that word produces across the
     wordle-common.json answer pool — same pattern function logic as the
     JS version in wordle-engine.js, reimplemented in Python (or shared
     via a small JSON-defined test fixture to confirm both implementations
     agree on the same sample cases).
   - Outputs the top 40 words by entropy to data/wordle-openers.json as
     [{ "word": "...", "bits": 0.00, "note": "..." }, ...], where "note" is
     a short auto-generated or manually-curated one-line reason (e.g.
     "covers 5 high-frequency letters with no repeats").
   - Print progress/timing to stdout since this may take a while over a
     large dictionary; this script is a one-time/occasional offline build
     step, not part of the live site build.

2. Update wordle-helper.html's Step 1 starting-word picker to load
   data/wordle-openers.json instead of the Session 1 hardcoded list,
   rendering word + note for each entry.

3. Upgrade rankCandidates() in wordle-engine.js to optionally test
   candidate guesses drawn from the broader wordle-common.json pool (not
   only the currently-remaining candidates) when the remaining pool is
   still large (say, above ~150 words) — this is when "probe" words that
   aren't themselves possible answers can still be the most informative
   guess, which is the gap between Session 1's approximation and true
   entropy play. Once the remaining pool drops below that threshold, fall
   back to the cheaper Session 1 approach (ranking only within the
   remaining pool) to keep things fast on every keystroke.

4. Add a code comment explaining the performance tradeoff and the
   threshold chosen, so this is tunable later without re-deriving the
   reasoning.

ACCEPTANCE CRITERIA
- data/wordle-openers.json exists with 40 ranked entries and is loaded
  correctly by the picker UI.
- The upgraded ranking visibly recommends different (better) words than
  Session 1's approximation in at least one manual test case with a large
  remaining pool (e.g. right after a first guess with very few hits).
- Performance: ranking recalculation after any guess still completes
  fast enough to feel instant in the browser (no visible UI freeze) on a
  typical remaining-pool size.
- No regression to Session 1's correctness (duplicate-letter logic,
  invalid-word rejection, mobile layout) — re-verify the Session 1
  acceptance criteria still pass.
```

---

## 9. Internal linking strategy

Using a hub-and-spoke / content-cluster model — each major topic gets a hub page, every spoke links up to its hub and sideways to its siblings, and the homepage feeds the hubs.

### Current page inventory, clustered

**Writing & Vocabulary cluster**
- Random Word Generator — `/` (also the de facto homepage, highest authority on the site)
- Random Sentence Generator — `/random-sentence-generator.html`
- Word Scrambler — `/word-scrambler.html`
- Word Tools hub — planned, not yet live

**Word Games cluster** (where Wordle Helper lives)
- Wordle Helper — `/wordle-helper.html` (this build)
- Pictionary Word Generator — `/pictionary-word-generator.html` — **referenced by name in random-word-generator.html's existing explainer copy, but not in your current project file set. Confirm this page is actually live before treating it as a real link target — if it isn't built yet, that existing link is a dead end right now and worth fixing either way.**
- Scattergories Generator — planned, not yet live
- Scrabble Word Finder — planned, not yet live
- Word Games hub — planned (the "Word Games" mega-nav column needs a "view all" target)

**Names cluster**
- Random Name Generator — built
- Name Generators hub — `/name-generators/` — built

Numbers & Chance and Account & Security clusters aren't built yet, so no linking work there yet — same pattern below applies once they exist.

### Recommended link additions

| From | To | Anchor text | Why |
|---|---|---|---|
| Wordle Helper (explainer or FAQ) | Scrabble Word Finder | "our Scrabble word finder" | same cluster, same stuck-mid-game use case — only add once that page is live |
| Wordle Helper (explainer or FAQ) | Pictionary Word Generator | "Pictionary word generator" | same cluster cross-sell — only add once confirmed live |
| Random Word Generator's "For games and Pictionary" section | Wordle Helper | "free Wordle Helper" | sends authority from your highest-traffic page straight to the new tool on day one |
| Random Word Generator's "Game nights" who-uses-it card | Wordle Helper | contextual mention alongside existing Pictionary/charades reference | reinforces the Word Games cluster from the home page |
| Pictionary / Scattergories / Scrabble (once built) | Wordle Helper | "Wordle Helper" | reciprocal — every cluster sibling should link back |
| Word Games hub (once built) | every Word Games tool | tool name | hub → spoke, the hub's core job |
| Every Word Games tool | Word Games hub | "← All word games" or similar | spoke → hub, keeps tools from sitting 2+ clicks deep |
| Mega nav, Word Games column | Wordle Helper | "Wordle Helper" | present on every page — your single highest-value internal link slot |
| Footer, Word Games column (once the 5-column restructure ships) | Wordle Helper | "Wordle Helper" | sitewide evergreen safety net |
| more-tools.html grid | Wordle Helper | "Wordle Helper" card | guaranteed day-one discoverability before nav/footer catch up |

### Orphan-prevention checklist for launch day

Before the five-column nav/footer restructure ships, Wordle Helper's only guaranteed paths to an already-crawled, authoritative page are:
1. A `tools.json` entry (feeds `more-tools.html`'s grid).
2. At least one contextual link from the home page itself (highest priority — this is the one link that matters most if everything else is mid-rollout).

Don't wait on the nav restructure to do #2 — add it the same day the tool ships.

### Anchor text rule
Never "click here" / "learn more." Always the tool's actual name or a close natural variant ("Wordle Helper," "free Wordle solver," "Scrabble word finder").

### Cluster rule going forward
Once Pictionary, Scattergories, and Scrabble Word Finder all exist, every Word Games page should link to at least 2 of its 3 siblings plus the hub — this is the same content-cluster pattern, just repeated as the cluster fills in. Don't link to a sibling tool before it's actually live; a forward reference to an unbuilt page is a dead link, not a head start.

---

## 10. Claude Code Prompt — Internal Linking Pass (paste-ready, run after Wordle Helper ships)

```
CONTEXT
Wordle Helper is live (or about to ship) at /wordle-helper.html. This pass
is purely about interlinking it with the rest of the site and auditing the
existing Word Games / Writing & Vocabulary clusters for gaps. Do not change
any tool functionality in this pass.

GOAL
1. Audit every internal <a href="/..."> across tools-src/*.html. For each
   link, confirm the target actually exists as a built, output page
   (check via the CONFIG output mapping at the top of each source file,
   not just guessing from the filename). Specifically check whether
   random-word-generator.html's existing references to
   /pictionary-word-generator.html point to a real, live page. Report any
   internal links that currently point to pages that don't exist.

2. Add these contextual links, but ONLY to pages confirmed live in step 1:
   - In wordle-helper.html's SLOT:explainer or SLOT:faq, one sentence
     linking to /scrabble-word-finder.html ("our Scrabble word finder")
     and one to /pictionary-word-generator.html ("Pictionary word
     generator") — skip either with a code comment noting "add once this
     page ships" if it isn't live yet.
   - In random-word-generator.html's existing "For games and Pictionary"
     explainer paragraph, add one sentence pointing to /wordle-helper.html
     ("Stuck on today's Wordle? Try our free Wordle Helper.").
   - In random-word-generator.html's SLOT:who "Game nights" card, mention
     Wordle Helper alongside the existing Pictionary/charades reference.

3. Confirm Wordle Helper's tools.json entry renders correctly in
   more-tools.html's grid (skip if the Session 1 prompt already handled
   this — just verify).

4. Check how nav.html's {{MEGA_COLS}} and footer.html's {{FOOTER_COLS}}
   are generated (likely from tools.json or a separate config — find the
   actual source). If Wordle Helper needs to be added there manually, add
   it under the Word Games column if that column already exists in the
   current build; if the five-column nav/footer restructure hasn't shipped
   yet, leave a clear comment flagging this as a follow-up rather than
   forcing it into the current column structure.

5. Use descriptive anchor text everywhere added — never "click here" or
   "learn more." Use the tool's actual name or a close natural variant.

ACCEPTANCE CRITERIA
- No internal link, new or pre-existing, points to a page that doesn't
  actually exist (report and either fix or flag every one found).
- Wordle Helper has at least one inbound link from the home page, on top
  of its tools.json / more-tools.html listing.
- Every added link uses descriptive, tool-specific anchor text.
- No existing page's content flow or layout is disrupted — these are
  single added sentences/links, not section rewrites.
```


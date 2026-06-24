# Spelling Bee Words for Elementary — Design Spec
_Date: 2026-06-04_

## Context

Wordineer already has a general spelling bee words generator (`/spelling-bee-words/`) covering K–Adult, and individual grade pages for Kindergarten, 2nd–7th grade. The placeholder link "Spelling Bee Words (Elementary)" in `/word-tools/` is live in the nav but has no page behind it.

This spec defines a purpose-built K–5 tool targeting **parents** running practice sessions at home and **elementary teachers** running classroom bees. It needs to be structurally and functionally differentiated from the main `/spelling-bee-words/` tool — not just a filtered copy of it.

## URL & Files

| Item | Value |
|---|---|
| URL | `/spelling-bee-words-elementary/` |
| Source file | `template-deploy/tools-src/spelling-bee-words-elementary.html` |
| Output file | `template-deploy/output/spelling-bee-words-elementary.html` |
| Deploy file | `wordineer-deploy/spelling-bee-words-elementary.html` |
| Data file | `wordineer-deploy/data/spelling-bee-words-elementary.json` (new) |
| Config type | `tool`, `more_tools_key: "spelling_bee_tools"` |

## Data File: `spelling-bee-words-elementary.json`

### Schema
Every entry: `{ "w", "grade", "diff", "origin", "syl", "pos", "d" }`
- `grade`: `"kindergarten"` | `"1st"` | `"2nd"` | `"3rd"` | `"4th"` | `"5th"`
- `diff`: `"easy"` | `"medium"` | `"hard"` (no `"expert"` — not applicable K-5)
- `syl`: integer syllable count
- `origin`: `"Anglo-Saxon"` | `"Germanic"` | `"Latin"` | `"Greek"` | `"French"` | `"Spanish"` | `"Other"`

### Build process (Python script)
1. Load `spelling-bee-words-kindergarten.json` → add `grade: "kindergarten"`, normalize `syl` to int, add `origin: "Anglo-Saxon"` where missing, strip `cat` and `ex` fields
2. Load `spelling-bee-2nd-grade.json` → remap `grade: "k-2"` → `"2nd"`; `syl` already int
3. Load `spelling-bee-3rd-grade.json` → add `grade: "3rd"`, normalize dotted `syl` string to int
4. Load `spelling-bee-4th-grade.json` → add `grade: "4th"`, normalize dotted `syl` string to int
5. Load `spelling-bee-5th-grade.json` → add `grade: "5th"`, normalize dotted `syl` string to int
6. Author ~120 1st-grade words fresh with full schema (`grade: "1st"`) — 1-3 syllable words, mix of Easy/Medium, Anglo-Saxon and Germanic origins dominate, matching typical 1st-grade classroom bee vocabulary
7. Merge all → write `spelling-bee-words-elementary.json`
Expected total: ~1,300+ words

## Tool Controls (differentiated from main tool)

| Control | Main tool | Elementary |
|---|---|---|
| Count | 1–50, default 20 | 1–50, default **15** |
| Grade | K-2, 3-4, 5-6, 7-8, 9-12, Adult | All Elementary / Kindergarten / 1st / 2nd / 3rd / 4th / 5th |
| Difficulty | Easy/Medium/Hard/**Expert** | Easy/Medium/Hard (no Expert) |
| Word origin | All origins | All origins (same) |
| Definitions toggle | Yes | Yes |
| Practice Mode | **No** | **Yes** |

## Practice Mode

Copied and adapted from `spelling-bee-words-2nd-grade.html`.
- "Practice Mode" button in results top bar
- Words shown one at a time — word is hidden, parent reads it aloud
- Controls: Reveal / Next / Exit Practice
- Keeps same generated list; no re-fetch

## Actions Bar
- Copy all · Print list · Practice Mode toggle
- Heart icon per word → saves to session (localStorage)
- Saved words tray below list with Copy saved button

## Breadcrumbs

```
Wordineer › Word Tools › Spelling Bee Words › Spelling Bee Words for Elementary
```
4-level: adds parent link to `/spelling-bee-words/` above the current page.

## `_redirects` entries to add

```
/spelling-bee-words-elementary.html    /spelling-bee-words-elementary/    301
/spelling-bee-words-elementary/        /spelling-bee-words-elementary.html   200
/spelling-bee-words-elementary         /spelling-bee-words-elementary/    301
```

## `tools.json` update

Add entry to `spelling_bee_tools` array (insert after the main spelling-bee-words entry):
```json
{
  "href": "/spelling-bee-words-elementary/",
  "name": "Spelling Bee Words (Elementary)",
  "desc": "K–5 spelling bee words with Practice Mode for parent-led home sessions. Filter by individual grade and difficulty.",
  "icon_bg": "#FEF9EC",
  "icon_path": "<path d=\"M2 4h9M2 7h11M2 10h7\" stroke=\"#C07B00\" stroke-width=\"1.3\" stroke-linecap=\"round\"/>"
}
```

## word-tools.html

The `<a class="tool-item" href="/spelling-bee-words-elementary/">` placeholder already exists with the correct `href` — no code change needed. It becomes live the moment the page is deployed to Cloudflare Pages.

## Hero

```
Badge:  K–5 · Practice Mode · Parent-Ready
H1:     Spelling Bee Words for Elementary Students
P:      Filter 1,000+ elementary spelling bee words by grade (K–5),
        difficulty, and word origin. Use Practice Mode to run parent-led
        sessions at home — no login, no account, free.
```

## Meta

```
Title:       Spelling Bee Words for Elementary Students (K–5) | Wordineer
Description: 1,000+ K–5 spelling bee words filtered by grade, difficulty,
             and word origin. Practice Mode for parent-led home sessions.
             Free, printable, no login.
Canonical:   https://wordineer.com/spelling-bee-words-elementary/
```

## Page Copy (1,000+ words) — Explainer Sections

### What Are Spelling Bee Words for Elementary?
Spelling bee words for elementary school span kindergarten through 5th grade — the range where most students have their first competition experience. At the K-2 level, these are short, phonetically regular words drawn from everyday reading vocabulary: one and two syllable words that follow predictable sound-letter patterns. By 3rd and 4th grade, the word list expands into multi-syllable words, common prefixes and suffixes, and the first wave of Latin borrowings. 5th grade marks the start of genuine competition vocabulary — words with irregular patterns, double consonants, and silent letters that require deliberate study rather than sounding out.

The Wordineer Elementary Spelling Bee Generator gives you instant access to 1,000+ words across all five elementary grade levels with definitions, syllable counts, and word origin labels on every entry. It is designed for parents running home practice sessions and teachers organizing classroom spelling bees — not for students drilling on their own. The tool generates a fresh random selection every time you click Generate so that practice never turns into memorizing the same sequence.

### Why Use This Tool for Elementary Spelling Bee Practice?
Most spelling bee word resources are static: the same list every visit, no filtering, no way to target your child's specific grade. This generator is different in four ways that matter for elementary preparation:

**Individual grade targeting.** The grade filter shows Kindergarten, 1st, 2nd, 3rd, 4th, and 5th as separate options — not grouped bands. A parent preparing a 2nd grader doesn't want to sort through 5th-grade vocabulary, and a teacher coaching 4th graders doesn't need kindergarten words in the mix. Select the exact grade and the generator pulls only words at that level.

**Practice Mode for parent-led sessions.** This is the feature that separates this tool from every static word list on the web. Click "Practice Mode" and the list switches to a one-word-at-a-time view. The word is hidden. You — the parent or coach — read the word aloud. Your child spells it. You click Reveal to show the correct spelling and confirm. Click Next to move on. It runs exactly like a real spelling bee round, without you having to hold a printed sheet and cover words with your thumb.

**Difficulty tiers that match real school bees.** The Easy tier covers the words that make up the bulk of a K-5 classroom bee — familiar vocabulary your child likely encounters in daily reading. Medium reflects the words that appear in competitive school-level rounds where students have been preparing for weeks. Hard covers the stretch words that district bee qualifiers practice: less common vocabulary, trickier patterns, and words that require knowing a root or rule to spell correctly.

**Free and printable.** There is no account, no paywall, and no limit on how many times you generate. Click Print List for a clean, numbered word list suitable for handing out in class or reading from during a practice session.

### How to Use This Tool
1. **Select a grade.** Choose your child's current grade from the Grade dropdown. If you want to preview next year's level or build stretch vocabulary, select one grade higher.
2. **Set a difficulty.** Start with Easy for the first session of a new grade level. Move to Medium once your child is reliably spelling Easy words correctly. Save Hard for the final week before a competition.
3. **Choose a count.** 15 words is the default — a good session length for most elementary students. Younger children (K-2) often do better with 10. Competitive 5th graders can handle 25-30 per session.
4. **Click Generate.** A random selection meeting your filters appears instantly.
5. **Use Practice Mode.** Click the Practice Mode button in the results panel to run a live round. Words are shown one at a time. Read the word, let your child spell it, then click Reveal and Next.
6. **Save words you want to review again.** Click the heart icon on any word to add it to your session saved list. At the end of a session, use Copy Saved to take those words into your notes app or a study list.
7. **Print for classroom use.** Teachers: generate a list, then click Print List. It produces a clean numbered page ready to read aloud during a class bee.

### What Elementary Spelling Bee Words Actually Look Like by Grade

**Kindergarten** words are short and phonetic: one syllable, common consonant-vowel patterns, and vocabulary from everyday life. These are the words a child who reads at grade level sees constantly in early readers. Examples: *cat, run, jump, blue, look, help, play*.

**1st grade** words extend the same phonetic patterns into slightly longer territory — two syllables start appearing, along with common blends (bl-, cr-, st-) and digraphs (ch, sh, th). The words are still highly regular. Examples: *happy, green, seven, pretty, garden, bring*.

**2nd grade** introduces words where spelling requires more than just sounding out. Common silent letters, vowel combinations (-oa-, -ea-, -ou-), and longer two-syllable words that require attention to middle syllables. Examples: *captain, perfect, between, special, toward*.

**3rd grade** is where preparation starts to matter. Words from this level regularly appear in competitive school bees. Latin prefixes and suffixes begin showing up — *un-, re-, -tion, -ful*. Double consonants and less predictable vowel patterns increase. Examples: *enormous, adventure, distance, famous, machine*.

**4th grade** marks the shift to deliberate vocabulary study. Many words at this level have Latin roots and need to be learned as units rather than decoded. Silent letters become common. Examples: *necessary, ancient, comfortable, separate, because, receive*.

**5th grade** introduces the vocabulary that serious elementary competitors study. Words with Greek and Latin roots, irregular patterns that only make sense knowing the word's origin, and multi-syllable words requiring careful syllable-by-syllable spelling. Examples: *pneumonia, exaggerate, silhouette, accomplish, dictionary*.

### How to Manage Elementary Spelling Bee Preparation

**Start 3–4 weeks before the competition.** One session per day, 15 minutes maximum for younger students, up to 20 minutes for 4th and 5th graders. Consistency matters far more than session length.

**Follow an Easy → Medium → Hard sequence.** Spend the first week on Easy words to build fluency and confidence. Move to Medium in week two. Introduce Hard words in week three. In the final week, mixed review across all difficulty levels.

**Rotate words — never repeat the same list twice.** The generator produces a fresh random selection every time you click Generate. Use this. A child who has seen the same 20 words 10 times in the same order is not learning to spell — they're learning a sequence. Rotating words forces genuine retention.

**Practice saying the word, not just writing it.** Spelling bees are oral. Make every practice round verbal: you say the word, your child spells it aloud, letter by letter, then says the word again. This matches what they will do on stage and builds the muscle memory for competition conditions.

**Use saved words as a missed-word list.** When your child misses a word in Practice Mode, heart-save it immediately. At the end of the session, copy the saved list and add it to a running review document. These are the words to start the next session with before generating new ones.

**Don't add more words in the final 48 hours.** New vocabulary introduced too close to competition day is more likely to cause confusion than help. Stick to review of words already practiced.

### Best Practices for Teachers Running Classroom Spelling Bees

Running a classroom bee with this tool takes about 5 minutes of prep:

**Generate separately by difficulty.** Pull an Easy list, print it, then pull a Medium list and print it separately. Use Easy words for early rounds and Medium for the final rounds. This creates a natural difficulty curve without manual curation.

**Randomize within rounds.** Generate a new list for each new practice session so no student gets an unfair advantage from having seen a particular sequence before.

**Use the origin filter for vocabulary lessons.** Filter to "Latin" or "Anglo-Saxon" for a session focused on root patterns rather than random vocabulary. This works especially well for 4th and 5th grade classes studying word roots as part of their ELA curriculum.

**Print the list in advance.** The Print List button produces a clean, numbered list without any UI chrome. Read from it during practice and hand out copies so students can review words after the session.

### More Ways to Practice at Home

Once your child has drilled their word list here, a few other tools on Wordineer can keep practice interesting without the pressure of timed rounds. The [Word Scramble](/word-scramble/) tool presents a jumbled word to unscramble — great for training letter-pattern recognition at a lower stakes level. [Word Unscramble](/word-unscramble/) lets you type in any scrambled word and find the answer, which works well for reviewing tricky spellings from missed-word lists. For older elementary students building vocabulary beyond the competition list, the [Random Word Generator](/random-word-generator/) pulls from a broad word set with definitions included.

---

## FAQ (7 questions)

1. **What words are in elementary school spelling bees?** — K-2: phonetic 1-2 syllable words. 3-4: multi-syllable, first Latin borrowings. 5th: competition-level words with root patterns.
2. **How is this different from the main Spelling Bee Words tool?** — Main tool covers K-12 and adult with grouped grade bands and no Practice Mode. This tool covers K-5 with individual grade labels and Practice Mode built for parent-led sessions.
3. **How do I run a practice session using Practice Mode?** — Generate a list, click Practice Mode, read each hidden word aloud, child spells it, click Reveal to confirm, Next to continue.
4. **How many words should my child practice per day?** — 10-15 for K-2, 15-20 for grades 3-5. Short daily sessions beat long infrequent ones.
5. **What is the difference between Easy, Medium, and Hard for elementary?** — Easy: school bee, familiar vocabulary. Medium: competitive classroom rounds. Hard: district bee stretch words.
6. **Can I print the word list for a classroom?** — Yes. Click Print List after generating. Clean numbered printout, no UI chrome.
7. **Do I need an account?** — No. Free, no login, no limit on generates.

---

## Who Section

Lead with Parents, then Teachers, then Homeschool, then Students, then Spelling Bee Coaches.

---

## Verification Checklist

- [ ] Build script runs without error; `spelling-bee-words-elementary.json` contains ~1,300+ entries with correct schema
- [ ] Page builds via `python3 build.py` with no errors
- [ ] Page loads at `localhost:8080/spelling-bee-words-elementary.html`
- [ ] Grade filter shows: All Elementary, Kindergarten, 1st, 2nd, 3rd, 4th, 5th
- [ ] Difficulty filter shows: All levels, Easy, Medium, Hard (no Expert)
- [ ] Practice Mode button activates one-at-a-time view; Reveal/Next work correctly
- [ ] Save/heart icon adds word to saved tray; persists on regenerate
- [ ] Print List opens clean print dialog
- [ ] Breadcrumbs render: Wordineer › Word Tools › Spelling Bee Words › Spelling Bee Words for Elementary
- [ ] `_redirects` clean URL rewrite works on local server
- [ ] word-tools.html link `/spelling-bee-words-elementary/` resolves correctly

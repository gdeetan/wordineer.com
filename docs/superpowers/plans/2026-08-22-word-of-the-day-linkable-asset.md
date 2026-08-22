# Word of the Day Linkable Asset Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn `/word-of-the-day/` into a citable 2026 useful-word calendar on one URL, with a server-rendered 365-row table, CSV download, print stylesheet, and copy-this-week.

**Architecture:** `wotd-2026.json` is the source of truth. `build.py` inlines it as `window._PAGE_DATA` and bakes today’s card plus the year table into HTML. Page JS maps the visitor’s local date onto the 2026 calendar. No new routes.

**Tech Stack:** Static HTML/CSS/JS, Python 3 `build.py`, JSON + CSV in `wordineer-deploy/data/`.

**Spec:** `docs/superpowers/specs/2026-08-22-word-of-the-day-linkable-asset-design.md`

---

## File map

| File | Role |
|---|---|
| `wordineer-deploy/data/validate_wotd_2026.py` | Schema/invariant checker (exit 0/1) |
| `wordineer-deploy/data/build_wotd_2026.py` | Builds JSON+CSV from SAT + words.json + 12 seed words |
| `wordineer-deploy/data/wotd-2026.json` | 365 dated entries |
| `wordineer-deploy/data/wotd-2026.csv` | Same data, schema-order header |
| `template-deploy/build.py` | SSR today card + year table; copy CSV into output/data |
| `template-deploy/tools-src/word-of-the-day.html` | Page source: meta, CSS, year list UI, JS |
| `wordineer-deploy/word-of-the-day.html` | Built copy (after `build.py`) |

Do not edit `wordineer-deploy/word-of-the-day.html` by hand. Do not add dated URLs. Do not change `tool-engine.js`.

---

### Task 1: Dataset validator

**Files:**
- Create: `wordineer-deploy/data/validate_wotd_2026.py`

- [ ] **Step 1: Write the validator**

```python
#!/usr/bin/env python3
"""Validate wotd-2026.json against the Phase 1 spec. Exit 1 on failure."""
import json
import os
import sys
from collections import Counter
from datetime import date, timedelta

ROOT = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(ROOT, 'wotd-2026.json')
KEYS = [
    'date', 'word', 'pos', 'pronunciation', 'difficulty', 'definition',
    'explanation', 'example', 'memory', 'quiz', 'answer', 'prompt',
]
POS = {'noun', 'adjective', 'verb', 'adverb'}
DIFF = {'easy', 'medium', 'hard'}


def fail(msg):
    print('FAIL:', msg)
    sys.exit(1)


def main():
    if not os.path.isfile(PATH):
        fail(f'missing {PATH}')
    with open(PATH, encoding='utf-8') as f:
        data = json.load(f)
    if not isinstance(data, list):
        fail('root must be a list')
    if len(data) != 365:
        fail(f'expected 365 entries, got {len(data)}')

    expected_dates = []
    d = date(2026, 1, 1)
    while d.year == 2026:
        expected_dates.append(d.isoformat())
        d += timedelta(days=1)
    if len(expected_dates) != 365:
        fail('internal: 2026 date count')

    dates, words = [], []
    diffs = Counter()
    for i, row in enumerate(data):
        if not isinstance(row, dict):
            fail(f'row {i} is not an object')
        for k in KEYS:
            val = row.get(k)
            if not isinstance(val, str) or not val.strip():
                fail(f'row {i} missing/empty {k}')
            if '<' in val or '>' in val:
                fail(f'row {i} field {k} contains HTML')
        if row['pos'] not in POS:
            fail(f"row {i} bad pos {row['pos']!r}")
        if row['difficulty'] not in DIFF:
            fail(f"row {i} bad difficulty {row['difficulty']!r}")
        if len(row['definition']) > 120:
            fail(f"row {i} definition too long ({len(row['definition'])})")
        dates.append(row['date'])
        words.append(row['word'].strip().lower())
        diffs[row['difficulty']] += 1

    if sorted(dates) != expected_dates:
        fail('dates must be unique and cover 2026-01-01 .. 2026-12-31')
    if len(set(words)) != 365:
        fail('words must be unique (case-insensitive)')

    easy_pct = 100.0 * diffs['easy'] / 365
    med_pct = 100.0 * diffs['medium'] / 365
    hard_pct = 100.0 * diffs['hard'] / 365
    if abs(easy_pct - 30) > 5 or abs(med_pct - 50) > 5 or abs(hard_pct - 20) > 5:
        fail(f'difficulty mix off: easy={easy_pct:.1f}% medium={med_pct:.1f}% hard={hard_pct:.1f}%')

    print(
        f'OK 365 entries; difficulty easy={diffs["easy"]} '
        f'medium={diffs["medium"]} hard={diffs["hard"]}'
    )


if __name__ == '__main__':
    main()
```

- [ ] **Step 2: Run it against a missing file**

```bash
python3 wordineer-deploy/data/validate_wotd_2026.py
```

Expected: `FAIL: missing .../wotd-2026.json` and exit 1.

- [ ] **Step 3: Commit**

```bash
git add wordineer-deploy/data/validate_wotd_2026.py
git commit -m "test: add wotd-2026 dataset validator"
```

---

### Task 2: Generate `wotd-2026.json` and CSV

**Files:**
- Create: `wordineer-deploy/data/build_wotd_2026.py`
- Create: `wordineer-deploy/data/wotd-2026.json`
- Create: `wordineer-deploy/data/wotd-2026.csv`

The JSON is the source of truth. The script writes both files. Do not hand-edit the CSV.

- [ ] **Step 1: Write the builder**

```python
#!/usr/bin/env python3
"""Build the 2026 Word of the Day calendar from seed + SAT + words.json."""
import csv
import json
import os
import re
from collections import defaultdict
from datetime import date, timedelta

ROOT = os.path.dirname(os.path.abspath(__file__))
KEYS = [
    'date', 'word', 'pos', 'pronunciation', 'difficulty', 'definition',
    'explanation', 'example', 'memory', 'quiz', 'answer', 'prompt',
]
POS = {'noun', 'adjective', 'verb', 'adverb'}
PATTERN = ['easy', 'medium', 'medium', 'hard', 'medium', 'easy', 'medium']
BLOCKLIST = {
    'fopdoodle', 'gardyloo', 'snollygoster', 'mamihlapinatapai',
    'kalsarikanni', 'kalsarikänni', 'ninnyhammer', 'smellfungus',
    'quomodocunquize', 'hornswoggle', 'absquatulate', 'blatteroon',
    'callipygian', 'callipygous', 'limeade', 'elbow',
}
FUNCTION_WORDS = {
    'about', 'above', 'after', 'again', 'ahead', 'almost', 'alone', 'along',
    'already', 'also', 'always', 'among', 'another', 'around', 'because',
    'before', 'behind', 'below', 'between', 'beyond', 'during', 'every',
    'other', 'through', 'under', 'until', 'without', 'would', 'could',
    'should', 'their', 'there', 'these', 'those', 'where', 'which', 'while',
    'whose', 'being', 'having', 'doing', 'using',
}

SEED = [
    {'word': 'lucid', 'pos': 'adjective', 'pronunciation': 'LOO-sid', 'difficulty': 'medium', 'definition': 'clear and easy to understand', 'explanation': 'A lucid idea, sentence, or explanation is clear enough that people can follow it without confusion.', 'example': 'Her lucid summary helped the whole class understand the difficult chapter.', 'memory': 'Think of a clear light switching on: lucid writing lights up the meaning.', 'quiz': 'Which sentence uses lucid correctly?', 'answer': 'Correct use: The teacher gave a lucid explanation of the problem.', 'prompt': 'Give students 60 seconds to rewrite a confusing sentence from today\'s lesson so it is lucid.'},
    {'word': 'resilient', 'pos': 'adjective', 'pronunciation': 'ri-ZIL-yuhnt', 'difficulty': 'medium', 'definition': 'able to recover after difficulty or change', 'explanation': 'A resilient person, plan, or material can handle pressure and keep going.', 'example': 'The resilient team adjusted quickly after the first idea failed.', 'memory': 'Resilient sounds like returning to shape after being bent.', 'quiz': 'If someone stays calm and recovers after a setback, what are they?', 'answer': 'They are resilient.', 'prompt': 'Ask students to describe a time they were resilient in one sentence.'},
    {'word': 'nuance', 'pos': 'noun', 'pronunciation': 'NOO-ahns', 'difficulty': 'hard', 'definition': 'a small but important difference in meaning, feeling, or expression', 'explanation': 'Nuance helps you notice the fine details that make two similar ideas not exactly the same.', 'example': 'The actor captured every nuance of the character\'s nervous smile.', 'memory': 'Nuance is the tiny shade of meaning between almost-matching ideas.', 'quiz': 'What does nuance add to an idea?', 'answer': 'It adds a small, subtle difference in meaning or feeling.', 'prompt': 'Have students compare two similar words and name one nuance that separates them.'},
    {'word': 'pragmatic', 'pos': 'adjective', 'pronunciation': 'prag-MAT-ik', 'difficulty': 'hard', 'definition': 'focused on practical results rather than theory', 'explanation': 'A pragmatic choice may not be perfect, but it works in real life.', 'example': 'They made a pragmatic decision to fix the old laptop instead of buying a new one.', 'memory': 'Pragmatic people ask, "What will actually work?"', 'quiz': 'Is a pragmatic solution more practical or more imaginary?', 'answer': 'More practical.', 'prompt': 'Give students a messy classroom problem and ask for one pragmatic fix in a sentence.'},
    {'word': 'vivid', 'pos': 'adjective', 'pronunciation': 'VIV-id', 'difficulty': 'easy', 'definition': 'bright, clear, or full of life', 'explanation': 'Vivid words, colors, or memories feel strong and easy to picture.', 'example': 'The poem used vivid details that made the street feel alive.', 'memory': 'Vivid writing makes a picture feel visible.', 'quiz': 'What kind of details help readers picture a scene?', 'answer': 'Vivid details.', 'prompt': 'Ask students to add two vivid details to a dull sentence on the board.'},
    {'word': 'meticulous', 'pos': 'adjective', 'pronunciation': 'muh-TIK-yuh-luhs', 'difficulty': 'hard', 'definition': 'very careful and attentive to detail', 'explanation': 'Meticulous work is done with patience, precision, and close attention.', 'example': 'The editor made meticulous notes on every paragraph.', 'memory': 'Meticulous means tiny details matter.', 'quiz': 'Would a meticulous person rush through a task?', 'answer': 'No. A meticulous person works carefully.', 'prompt': 'Have students spend 60 seconds making one sentence more meticulous by adding a precise detail.'},
    {'word': 'cordial', 'pos': 'adjective', 'pronunciation': 'KOR-juhl', 'difficulty': 'medium', 'definition': 'warm, friendly, and polite', 'explanation': 'A cordial greeting is friendly without being overly familiar.', 'example': 'The two neighbors exchanged a cordial hello each morning.', 'memory': 'Cordial sounds connected to the heart: friendly and warm.', 'quiz': 'What is a cordial greeting like?', 'answer': 'It is warm, friendly, and polite.', 'prompt': 'Ask students to write a cordial two-sentence email to a classmate.'},
    {'word': 'tenacious', 'pos': 'adjective', 'pronunciation': 'tuh-NAY-shuhs', 'difficulty': 'hard', 'definition': 'not giving up easily', 'explanation': 'A tenacious person keeps holding on to a goal, even when it is difficult.', 'example': 'Her tenacious research finally uncovered the missing records.', 'memory': 'Tenacious means you hold tight to the task.', 'quiz': 'What word describes someone who keeps trying?', 'answer': 'Tenacious.', 'prompt': 'Students write one sentence about a tenacious person from history or sports.'},
    {'word': 'concise', 'pos': 'adjective', 'pronunciation': 'kuhn-SYSE', 'difficulty': 'medium', 'definition': 'using few words while still being clear', 'explanation': 'Concise writing removes extra words but keeps the meaning.', 'example': 'The instructions were concise, so everyone knew what to do.', 'memory': 'Concise means clear and compact.', 'quiz': 'Is concise writing long-winded or brief?', 'answer': 'Brief.', 'prompt': 'Give students a wordy sentence and 60 seconds to make it concise.'},
    {'word': 'curious', 'pos': 'adjective', 'pronunciation': 'KYUR-ee-uhs', 'difficulty': 'easy', 'definition': 'wanting to know or learn more', 'explanation': 'A curious mind asks questions and looks for patterns.', 'example': 'The curious student stayed after class to ask how the machine worked.', 'memory': 'Curious starts with a question.', 'quiz': 'What does a curious person like to do?', 'answer': 'Ask questions and learn more.', 'prompt': 'Ask each student to write one curious question about today\'s topic.'},
    {'word': 'eloquent', 'pos': 'adjective', 'pronunciation': 'EL-uh-kwuhnt', 'difficulty': 'hard', 'definition': 'expressing ideas clearly and beautifully', 'explanation': 'An eloquent speaker or writer uses language in a graceful, effective way.', 'example': 'Her eloquent speech made the audience feel hopeful.', 'memory': 'Eloquent expression sounds elegant and clear.', 'quiz': 'What does an eloquent speaker do well?', 'answer': 'Express ideas clearly and beautifully.', 'prompt': 'Students rewrite a flat opinion so it sounds more eloquent, without adding fluff.'},
    {'word': 'adapt', 'pos': 'verb', 'pronunciation': 'uh-DAPT', 'difficulty': 'easy', 'definition': 'to change so something works in a new situation', 'explanation': 'When you adapt, you adjust your behavior, plan, or tool to fit new conditions.', 'example': 'We had to adapt the lesson for a younger class.', 'memory': 'Adapt means adjust.', 'quiz': 'If plans change and you adjust, what do you do?', 'answer': 'You adapt.', 'prompt': 'Ask students how they would adapt a playground game for a rainy day.'},
]


def load_json(name):
    with open(os.path.join(ROOT, name), encoding='utf-8') as f:
        return json.load(f)


def ok_word(word):
    w = (word or '').strip()
    if not re.fullmatch(r'[A-Za-z]{4,12}', w):
        return False
    low = w.lower()
    if low in BLOCKLIST or low in FUNCTION_WORDS:
        return False
    return True


def lemma_key(word):
    low = word.strip().lower()
    for suf in ('tion', 'sion', 'ness', 'ment', 'able', 'ible', 'ous', 'ive', 'ing', 'ed', 'ly', 'es', 's'):
        if len(low) > len(suf) + 3 and low.endswith(suf):
            return low[:-len(suf)]
    return low


def pron_from_syl(syl, word):
    if not syl:
        return word.upper()
    parts = [p for p in re.split(r'[·.\-]+', syl) if p]
    if not parts:
        return word.upper()
    parts = [p.lower() for p in parts]
    parts[-1] = parts[-1].upper()
    return '-'.join(parts)


def fill_fields(word, pos, pronunciation, difficulty, definition, example, memory):
    word = word.strip()
    pos = pos.strip().lower()
    definition = definition.strip().rstrip('.')
    if definition[0].isupper() and not definition.startswith(word.capitalize()):
        definition = definition[0].lower() + definition[1:]
    if len(definition) > 100:
        definition = definition[:97].rsplit(' ', 1)[0] + '…'
    explanation = (
        f'{word.capitalize()} is a {pos} meaning {definition}. '
        f'Use it when that meaning is exactly what you need in writing or speech.'
    )
    if not example:
        example = f'She chose the word "{word}" because she meant {definition}.'
    if not memory:
        memory = f'Remember {word}: it means {definition}.'
    quiz = f'What does "{word}" mean?'
    answer = definition[0].upper() + definition[1:] + '.'
    prompt = (
        f'Give students 60 seconds to use "{word}" in an original sentence '
        f'that shows it means "{definition}".'
    )
    return {
        'word': word.lower() if word.islower() or word.istitle() else word,
        'pos': pos,
        'pronunciation': pronunciation,
        'difficulty': difficulty,
        'definition': definition,
        'explanation': explanation,
        'example': example,
        'memory': memory,
        'quiz': quiz,
        'answer': answer,
        'prompt': prompt,
    }


def display_word(word):
    return word[:1].upper() + word[1:] if word else word


def collect_candidates():
    used_words = set()
    used_lemmas = set()
    buckets = defaultdict(list)

    def take(entry):
        w = entry['word']
        key = w.strip().lower()
        lemma = lemma_key(w)
        if key in used_words or lemma in used_lemmas:
            return
        used_words.add(key)
        used_lemmas.add(lemma)
        entry = dict(entry)
        entry['word'] = display_word(w)
        buckets[entry['difficulty']].append(entry)

    for row in SEED:
        take(dict(row))

    sat = load_json('sat-vocab-data.json')
    sat_sorted = sorted(sat, key=lambda r: {'easy': 0, 'medium': 1, 'hard': 2}.get(r.get('diff'), 9))
    for r in sat_sorted:
        w = r.get('w') or ''
        pos = (r.get('pos') or '').lower()
        diff = r.get('diff') or 'medium'
        if not ok_word(w) or pos not in POS or diff not in {'easy', 'medium', 'hard'}:
            continue
        take(fill_fields(
            w, pos, pron_from_syl(r.get('syl'), w), diff,
            r.get('d') or '', r.get('ex') or '', r.get('root_note') or '',
        ))

    words = load_json('words.json')
    for row in words:
        w, pos, definition, diff = row[0], row[1], row[2], row[3]
        if not ok_word(w) or pos not in POS or diff not in {'easy', 'medium', 'hard'}:
            continue
        if not definition or len(definition) < 12:
            continue
        take(fill_fields(w, pos, w.upper(), diff, definition, '', ''))

    return buckets


def assign_dates(buckets):
    dates = []
    d = date(2026, 1, 1)
    while d.year == 2026:
        dates.append(d.isoformat())
        d += timedelta(days=1)

    pointers = {k: 0 for k in ('easy', 'medium', 'hard')}
    out = []
    for i, dt in enumerate(dates):
        want = PATTERN[i % len(PATTERN)]
        chosen = None
        for candidate in (want, 'medium', 'easy', 'hard'):
            idx = pointers[candidate]
            if idx < len(buckets[candidate]):
                chosen = dict(buckets[candidate][idx])
                pointers[candidate] = idx + 1
                break
        if chosen is None:
            raise SystemExit('Not enough candidate words to fill 365 days')
        chosen['date'] = dt
        out.append({k: chosen[k] for k in KEYS})
    return out


def write_csv(rows, path):
    with open(path, 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=KEYS, extrasaction='ignore')
        w.writeheader()
        w.writerows(rows)


def main():
    buckets = collect_candidates()
    rows = assign_dates(buckets)
    json_path = os.path.join(ROOT, 'wotd-2026.json')
    csv_path = os.path.join(ROOT, 'wotd-2026.csv')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)
        f.write('\n')
    write_csv(rows, csv_path)
    print(f'wrote {len(rows)} rows -> {json_path} and {csv_path}')


if __name__ == '__main__':
    main()
```

- [ ] **Step 2: Run the builder**

```bash
python3 wordineer-deploy/data/build_wotd_2026.py
```

Expected: `wrote 365 rows -> .../wotd-2026.json and .../wotd-2026.csv`

- [ ] **Step 3: Run the validator**

```bash
python3 wordineer-deploy/data/validate_wotd_2026.py
```

Expected: `OK 365 entries; difficulty easy=… medium=… hard=…` and exit 0.

If mix is off, change `PATTERN` or skip extra SAT `hard` rows before `words.json` fill, then rerun builder + validator. Do not edit JSON by hand unless one word is obviously junk.

- [ ] **Step 4: Confirm CSV header**

```bash
head -n 1 wordineer-deploy/data/wotd-2026.csv
```

Expected:

```
date,word,pos,pronunciation,difficulty,definition,explanation,example,memory,quiz,answer,prompt
```

- [ ] **Step 5: Commit**

```bash
git add wordineer-deploy/data/build_wotd_2026.py wordineer-deploy/data/wotd-2026.json wordineer-deploy/data/wotd-2026.csv
git commit -m "data: add 2026 word-of-the-day calendar JSON and CSV"
```

---

### Task 3: Bake WOTD HTML in `build.py`

**Files:**
- Modify: `template-deploy/build.py` (`copy_data_assets`, `inject_ssr_html`, add render helpers)

- [ ] **Step 1: Copy all CSV data files, not only etymology-100.csv**

In `copy_data_assets()`, replace:

```python
        if not (fname.endswith('.json') or fname == 'etymology-100.csv'):
            continue
```

with:

```python
        if not (fname.endswith('.json') or fname.endswith('.csv')):
            continue
```

- [ ] **Step 2: Add WOTD render helpers above `inject_ssr_html`**

```python
_WOTD_MONTHS = (
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December',
)

_WOTD_LISTEN_SVG = (
    '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none">'
    '<path d="M11 5 6 9H3v6h3l5 4V5Z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>'
    '<path d="M15.5 8.5a5 5 0 0 1 0 7M18.5 5.5a9 9 0 0 1 0 13" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>'
    '</svg>'
)


def map_wotd_date(d):
    month, day = d.month, d.day
    if month == 2 and day == 29:
        day = 28
    return f'2026-{month:02d}-{day:02d}'


def _wotd_by_date(data):
    return {row.get('date'): row for row in data if isinstance(row, dict) and row.get('date')}


def _wotd_entry_for_build(data):
    by_date = _wotd_by_date(data)
    key = map_wotd_date(datetime.now(timezone.utc).date())
    if key in by_date:
        return by_date[key]
    for row in reversed(data):
        if row.get('date') and row['date'] <= key:
            return row
    return data[0] if data else None


def _render_wotd_today(entry):
    if not entry:
        return ''
    word = _esc(entry.get('word', ''))
    pos = _esc(entry.get('pos', ''))
    pron = _esc(entry.get('pronunciation', ''))
    diff = _esc(entry.get('difficulty', ''))
    definition = _esc(entry.get('definition', ''))
    explanation = _esc(entry.get('explanation', ''))
    example = _esc(entry.get('example', ''))
    memory = _esc(entry.get('memory', ''))
    quiz = _esc(entry.get('quiz', ''))
    answer = _esc(entry.get('answer', ''))
    return (
        f'<div class="wotd-date" id="wotd-date">{_esc(entry.get("date", ""))}</div>'
        f'<div class="wotd-word-row"><div>'
        f'<div class="wotd-word-wrap">'
        f'<div class="wotd-word" id="wotd-word">{word}</div>'
        f'<button class="wotd-listen" id="wotd-listen" type="button" aria-label="Listen to pronunciation" title="Listen to pronunciation">{_WOTD_LISTEN_SVG}</button>'
        f'</div>'
        f'<div class="wotd-meta" id="wotd-meta">'
        f'<span class="wotd-pill">{pos}</span>'
        f'<span class="wotd-pill soft">{pron}</span>'
        f'<span class="wotd-pill soft">{diff}</span>'
        f'</div></div>'
        f'<button class="gen-btn" id="wotd-surprise" type="button" style="width:auto;white-space:nowrap">Surprise me</button>'
        f'</div>'
        f'<div class="wotd-def" id="wotd-definition">{definition}</div>'
        f'<div class="wotd-section"><div class="wotd-section-title">Plain English</div>'
        f'<div class="wotd-body" id="wotd-explanation">{explanation}</div></div>'
        f'<div class="wotd-section"><div class="wotd-section-title">Example</div>'
        f'<div class="wotd-example" id="wotd-example">{example}</div></div>'
        f'<div class="wotd-section"><div class="wotd-section-title">Memory hook</div>'
        f'<div class="wotd-body" id="wotd-memory">{memory}</div></div>'
        f'<div class="wotd-practice">'
        f'<button class="act-btn" id="wotd-practice-copy" type="button">Copy practice prompt</button>'
        f'<button class="act-btn" id="wotd-quiz-reveal" type="button">Reveal quiz answer</button>'
        f'</div>'
        f'<div class="wotd-quiz"><div class="wotd-quiz-q" id="wotd-quiz-q">{quiz}</div>'
        f'<div class="wotd-quiz-a" id="wotd-quiz-a">{answer}</div></div>'
    )


def _render_wotd_rows(data):
    parts = []
    current_month = None
    for row in data:
        dt = row.get('date') or ''
        month = dt[5:7] if len(dt) >= 7 else ''
        if month and month != current_month:
            current_month = month
            try:
                month_name = _WOTD_MONTHS[int(month) - 1]
            except (ValueError, IndexError):
                month_name = month
            parts.append(
                f'<tr class="wotd-month-row" id="wotd-month-{_esc(month)}">'
                f'<th colspan="5">{_esc(month_name)}</th></tr>'
            )
        parts.append(
            f'<tr>'
            f'<td>{_esc(dt)}</td>'
            f'<td><strong>{_esc(row.get("word", ""))}</strong></td>'
            f'<td>{_esc(row.get("pos", ""))}</td>'
            f'<td>{_esc(row.get("definition", ""))}</td>'
            f'<td>{_esc(row.get("prompt", ""))}</td>'
            f'</tr>'
        )
    return ''.join(parts)
```

- [ ] **Step 3: Teach `inject_ssr_html` to fill WOTD placeholders**

Replace the body of `inject_ssr_html` so missing `SSR_ROWS` does not skip a page that still has `SSR_TODAY`, and add the WOTD branch:

```python
def inject_ssr_html(cfg, slots):
    """Render dataset as static HTML into pages that contain SSR placeholders."""
    url = cfg.get('url', '')
    fname = cfg.get('inject_data')
    if not fname:
        return slots

    all_slot_text = ''.join(slots.values())
    if '<!-- SSR_ROWS -->' not in all_slot_text and '<!-- SSR_TODAY -->' not in all_slot_text:
        return slots

    src_path = os.path.join(DEPLOY_DATA_DIR, fname)
    if not os.path.isfile(src_path):
        print(f'  warning → inject_data file not found: {src_path}')
        return slots

    with open(src_path, encoding='utf-8') as f:
        data = json.load(f)

    slot_name = None
    if url == '/common-5-letter-words/':
        rendered = _render_five_letter_rows(data)
        slot_name = 'tool'
        slots[slot_name] = slots[slot_name].replace('<!-- SSR_ROWS -->', rendered)
    elif url == '/etymology-100-common-words/':
        rendered = _render_etymology_cards(data)
        slot_name = 'content'
        slots[slot_name] = slots[slot_name].replace('<!-- SSR_ROWS -->', rendered)
    elif url == '/esl-vocabulary-cefr/':
        rendered = _render_esl_cards(data)
        slot_name = 'tool'
        slots[slot_name] = slots[slot_name].replace('<!-- SSR_ROWS -->', rendered)
    elif url == '/word-of-the-day/':
        slot_name = 'tool'
        today = _render_wotd_today(_wotd_entry_for_build(data))
        rows = _render_wotd_rows(data)
        slots[slot_name] = slots[slot_name].replace('<!-- SSR_TODAY -->', today)
        slots[slot_name] = slots[slot_name].replace('<!-- SSR_ROWS -->', rows)
    else:
        return slots

    print(f'  ssr → {len(data)} items baked into {url}')
    return slots
```

- [ ] **Step 4: Commit**

```bash
git add template-deploy/build.py
git commit -m "feat: SSR word-of-the-day card and 2026 year table"
```

---

### Task 4: Page chrome — CONFIG, meta, CSS, year list markup

**Files:**
- Modify: `template-deploy/tools-src/word-of-the-day.html`

Keep existing card IDs, saved-words, previous-7, and help sidebar. Do not use `<details>`/`<summary>`.

- [ ] **Step 1: Add `inject_data` to CONFIG**

Replace the CONFIG line with:

```html
<!-- CONFIG { "url": "/word-of-the-day/", "output": "word-of-the-day.html", "inject_data": "wotd-2026.json" } -->
```

- [ ] **Step 2: Replace the `meta` slot**

Use this full slot (FAQ schema must match visible FAQ questions in Task 6):

```html
<!-- SLOT:meta -->
<title>Word of the Day 2026 — Free Daily Vocabulary List (CSV) | Wordineer</title>
<meta name="description" content="A useful English word every day, plus the full 2026 calendar to download as CSV or print for class. Definition, example, memory hook, and a 5-minute classroom prompt.">
<link rel="canonical" href="https://wordineer.com/word-of-the-day/">
<meta property="og:type"        content="website">
<meta property="og:site_name"   content="Wordineer">
<meta property="og:title"       content="Word of the Day 2026 | Wordineer">
<meta property="og:description" content="One useful word a day — and the full 2026 list, free to download or print.">
<meta property="og:url"         content="https://wordineer.com/word-of-the-day">
<meta property="og:image"       content="https://wordineer.com/og-image.png">
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Dataset",
  "name": "Wordineer 2026 Word of the Day",
  "description": "365 useful English words for writing and conversation, one per calendar day in 2026, with definitions and classroom prompts.",
  "url": "https://wordineer.com/word-of-the-day",
  "creator": { "@type": "Organization", "name": "Wordineer" },
  "distribution": {
    "@type": "DataDownload",
    "encodingFormat": "text/csv",
    "contentUrl": "https://wordineer.com/data/wotd-2026.csv"
  }
}
</script>
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "What's the fastest way to actually remember a new word?",
      "acceptedAnswer": { "@type": "Answer", "text": "Write one sentence using the word before you leave the page. Producing a word in context is far more effective for retention than reading its definition passively. The memory hook on each word gives you an association to anchor the meaning — read it, then write your sentence. That 90-second routine is worth more than reviewing 20 words at once." }
    },
    {
      "@type": "Question",
      "name": "What if today's word is too easy or too hard?",
      "acceptedAnswer": { "@type": "Answer", "text": "Hit Surprise me to get a different word from the vocabulary set without changing the official daily word. Press it as many times as you like to find a word at the right difficulty. The daily word stays the same for everyone on that calendar date." }
    },
    {
      "@type": "Question",
      "name": "Do my saved words persist if I close the browser?",
      "acceptedAnswer": { "@type": "Answer", "text": "Yes — saved words are stored in your browser's local storage, so they stay between visits on the same device and browser. They won't sync across devices. Use Copy saved to paste your list into a notes app before clearing your browser data." }
    },
    {
      "@type": "Question",
      "name": "Does the word of the day change every day?",
      "acceptedAnswer": { "@type": "Answer", "text": "Yes. Each calendar date in 2026 has an official word on the published list below. Everyone with the same local date sees the same word. The Previous words panel shows the last 7 days if you missed one." }
    },
    {
      "@type": "Question",
      "name": "Can I download the full year list?",
      "acceptedAnswer": { "@type": "Answer", "text": "Yes. Use Download CSV for the full 2026 calendar, including definition, example, memory hook, quiz, and classroom prompt for every day. You can also copy the current Monday–Sunday week as a tab-separated list." }
    },
    {
      "@type": "Question",
      "name": "Can I print this for class?",
      "acceptedAnswer": { "@type": "Answer", "text": "Yes. Click Print / Save as PDF. The print view keeps the year table and a Wordineer credit line, and hides navigation, ads, and the quiz chrome. Use your browser's Save as PDF if you need a file." }
    },
    {
      "@type": "Question",
      "name": "Are these the same words Dictionary.com uses?",
      "acceptedAnswer": { "@type": "Answer", "text": "No. This list is curated for words people actually write and say, and the whole 2026 calendar is published up front so teachers can plan. Dictionary.com's word of the day is a separate editorial feed." }
    },
    {
      "@type": "Question",
      "name": "How do I use the Word of the Day as a classroom activity?",
      "acceptedAnswer": { "@type": "Answer", "text": "Project the page, show the word and memory hook, and ask students to guess the definition before scrolling down. Then reveal the definition and example and give everyone 60 seconds to write one original sentence. The whole warm-up takes 4–5 minutes. Each row also has a ready classroom prompt." }
    },
    {
      "@type": "Question",
      "name": "Where do the words come from?",
      "acceptedAnswer": { "@type": "Answer", "text": "The daily words are curated for learning value — chosen to be useful in writing and conversation. Each entry includes a pronunciation guide, plain-English explanation, real-world example sentence, memory hook, a short quiz, and a classroom prompt." }
    }
  ]
}
</script>
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "WebApplication",
  "name": "Wordineer Word of the Day",
  "url": "https://wordineer.com/word-of-the-day",
  "applicationCategory": "EducationalApplication",
  "operatingSystem": "Any",
  "description": "A free daily vocabulary builder with a 2026 word-of-the-day calendar, CSV download, and classroom prompts.",
  "offers": {
    "@type": "Offer",
    "price": "0",
    "priceCurrency": "USD"
  }
}
</script>
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    { "@type": "ListItem", "position": 1, "name": "Wordineer", "item": "https://wordineer.com/" },
    { "@type": "ListItem", "position": 2, "name": "Word Tools", "item": "https://wordineer.com/word-tools/" },
    { "@type": "ListItem", "position": 3, "name": "Word of the Day", "item": "https://wordineer.com/word-of-the-day/" }
  ]
}
</script>
<!-- /SLOT:meta -->
```

- [ ] **Step 3: Append year-list and print CSS before `</style>`**

```css
.wotd-year { margin-top: 28px; }
.wotd-year-head h2 { font-size: 22px; margin: 0 0 8px; letter-spacing: -.02em; }
.wotd-year-head p { font-size: 14px; line-height: 1.55; color: var(--text-2); margin: 0 0 14px; }
.wotd-year-actions { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 12px; }
.wotd-year-actions a.act-btn { text-decoration: none; display: inline-flex; align-items: center; }
.wotd-month-jumps { display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 12px; }
.wotd-month-jumps a { font-size: 12px; padding: 5px 9px; border: 1px solid var(--border); border-radius: 6px; color: var(--text-2); text-decoration: none; background: var(--bg); }
.wotd-month-jumps a:hover { background: var(--bg-2); color: var(--text); }
.wotd-table-wrap { overflow-x: auto; border: 1px solid var(--border); border-radius: var(--radius-lg); background: var(--bg); }
.wotd-year-table { width: 100%; border-collapse: collapse; min-width: 640px; }
.wotd-year-table th, .wotd-year-table td { text-align: left; padding: 8px 10px; border-bottom: 1px solid var(--border-2); font-size: 13px; vertical-align: top; }
.wotd-year-table thead th { font-size: 10px; text-transform: uppercase; letter-spacing: .06em; color: var(--text-3); background: var(--bg-2); }
.wotd-month-row th { background: var(--bg-2); font-size: 13px; color: var(--text); letter-spacing: 0; text-transform: none; }
.wotd-print-banner { display: none; }
@media (max-width: 700px) {
  .wotd-year { margin-top: 18px; }
}
@media print {
  nav, .hamburger, #mega, .ad-rect, .ad-slot, .faq, .uc-grid, .more-tools,
  footer, .wotd-help-panel, .wotd-side, .wotd-practice, .wotd-quiz,
  #wotd-surprise, .words-actions, .hero-badge, .breadcrumb { display: none !important; }
  .wotd-print-banner { display: block; margin: 0 0 16px; }
  .wotd-print-banner h1 { font-size: 18pt; margin: 0 0 4pt; }
  .wotd-print-banner p { font-size: 10pt; color: #444; margin: 0; }
  .tool-wrap { max-width: none; padding: 0; }
  .tool-card { border: 0; box-shadow: none; }
  .wotd-year-actions, .wotd-month-jumps { display: none !important; }
  .wotd-table-wrap { overflow: visible; border: 0; }
  .wotd-year-table { min-width: 0; }
  .wotd-month-row { break-before: page; }
  .wotd-month-row:first-child { break-before: auto; }
}
```

- [ ] **Step 4: Update hero intro**

Replace the hero `<p>` with:

```html
  <p>Learn one useful word every day — then download the full 2026 list as CSV or print it for class.</p>
```

- [ ] **Step 5: Replace `#wotd-main` inner HTML with the today placeholder, and add the year list after `</div>` of `.tool-card` but still inside `.tool-wrap`**

`#wotd-main` becomes:

```html
        <div class="wotd-main" id="wotd-main">
          <!-- SSR_TODAY -->
        </div>
```

Immediately after the tool-card closing `</div>` (the one that wraps `.tool-split`), still inside `.tool-wrap`, insert:

```html
  <div class="wotd-print-banner">
    <h1>Wordineer 2026 Word of the Day</h1>
    <p>https://wordineer.com/word-of-the-day</p>
  </div>
  <div class="wotd-year" id="wotd-year">
    <div class="wotd-year-head">
      <h2>2026 word of the day list</h2>
      <p>The official calendar — 365 useful writing words, free to download and print. Chosen for words people actually write and say, not obscure trivia.</p>
      <div class="wotd-year-actions">
        <a class="act-btn" href="/data/wotd-2026.csv" download>Download CSV</a>
        <button class="act-btn" id="wotd-print" type="button">Print / Save as PDF</button>
        <button class="act-btn" id="wotd-copy-week" type="button">Copy this week</button>
      </div>
      <nav class="wotd-month-jumps" aria-label="Jump to month">
        <a href="#wotd-month-01">Jan</a>
        <a href="#wotd-month-02">Feb</a>
        <a href="#wotd-month-03">Mar</a>
        <a href="#wotd-month-04">Apr</a>
        <a href="#wotd-month-05">May</a>
        <a href="#wotd-month-06">Jun</a>
        <a href="#wotd-month-07">Jul</a>
        <a href="#wotd-month-08">Aug</a>
        <a href="#wotd-month-09">Sep</a>
        <a href="#wotd-month-10">Oct</a>
        <a href="#wotd-month-11">Nov</a>
        <a href="#wotd-month-12">Dec</a>
      </nav>
    </div>
    <div class="wotd-table-wrap">
      <table class="wotd-year-table">
        <thead>
          <tr>
            <th>Date</th>
            <th>Word</th>
            <th>Part of speech</th>
            <th>Definition</th>
            <th>Classroom prompt</th>
          </tr>
        </thead>
        <tbody>
          <!-- SSR_ROWS -->
        </tbody>
      </table>
    </div>
  </div>
```

- [ ] **Step 6: Commit**

```bash
git add template-deploy/tools-src/word-of-the-day.html
git commit -m "feat: add 2026 year list chrome to word-of-the-day"
```

---

### Task 5: Runtime JS — date map, previous 7, surprise, copy week, print

**Files:**
- Modify: `template-deploy/tools-src/word-of-the-day.html` (`SLOT:init`)

Replace the `WORDINEER_WOTD` IIFE. Keep `bindWordineerMenu` unchanged after it.

- [ ] **Step 1: Replace `const WORDINEER_WOTD = (() => { ... })(); WORDINEER_WOTD.init();` with:**

```js
const WORDINEER_WOTD = (() => {
  const curated = [
    { word:'lucid', pos:'adjective', pronunciation:'LOO-sid', difficulty:'medium', definition:'clear and easy to understand', explanation:'A lucid idea, sentence, or explanation is clear enough that people can follow it without confusion.', example:'Her lucid summary helped the whole class understand the difficult chapter.', memory:'Think of a clear light switching on: lucid writing lights up the meaning.', quiz:'Which sentence uses lucid correctly?', answer:'Correct use: The teacher gave a lucid explanation of the problem.', prompt:'Give students 60 seconds to rewrite a confusing sentence from today\'s lesson so it is lucid.' },
    { word:'resilient', pos:'adjective', pronunciation:'ri-ZIL-yuhnt', difficulty:'medium', definition:'able to recover after difficulty or change', explanation:'A resilient person, plan, or material can handle pressure and keep going.', example:'The resilient team adjusted quickly after the first idea failed.', memory:'Resilient sounds like returning to shape after being bent.', quiz:'If someone stays calm and recovers after a setback, what are they?', answer:'They are resilient.', prompt:'Ask students to describe a time they were resilient in one sentence.' },
    { word:'nuance', pos:'noun', pronunciation:'NOO-ahns', difficulty:'hard', definition:'a small but important difference in meaning, feeling, or expression', explanation:'Nuance helps you notice the fine details that make two similar ideas not exactly the same.', example:'The actor captured every nuance of the character\'s nervous smile.', memory:'Nuance is the tiny shade of meaning between almost-matching ideas.', quiz:'What does nuance add to an idea?', answer:'It adds a small, subtle difference in meaning or feeling.', prompt:'Have students compare two similar words and name one nuance that separates them.' },
    { word:'pragmatic', pos:'adjective', pronunciation:'prag-MAT-ik', difficulty:'hard', definition:'focused on practical results rather than theory', explanation:'A pragmatic choice may not be perfect, but it works in real life.', example:'They made a pragmatic decision to fix the old laptop instead of buying a new one.', memory:'Pragmatic people ask, "What will actually work?"', quiz:'Is a pragmatic solution more practical or more imaginary?', answer:'More practical.', prompt:'Give students a messy classroom problem and ask for one pragmatic fix in a sentence.' },
    { word:'vivid', pos:'adjective', pronunciation:'VIV-id', difficulty:'easy', definition:'bright, clear, or full of life', explanation:'Vivid words, colors, or memories feel strong and easy to picture.', example:'The poem used vivid details that made the street feel alive.', memory:'Vivid writing makes a picture feel visible.', quiz:'What kind of details help readers picture a scene?', answer:'Vivid details.', prompt:'Ask students to add two vivid details to a dull sentence on the board.' },
    { word:'meticulous', pos:'adjective', pronunciation:'muh-TIK-yuh-luhs', difficulty:'hard', definition:'very careful and attentive to detail', explanation:'Meticulous work is done with patience, precision, and close attention.', example:'The editor made meticulous notes on every paragraph.', memory:'Meticulous means tiny details matter.', quiz:'Would a meticulous person rush through a task?', answer:'No. A meticulous person works carefully.', prompt:'Have students spend 60 seconds making one sentence more meticulous by adding a precise detail.' },
    { word:'cordial', pos:'adjective', pronunciation:'KOR-juhl', difficulty:'medium', definition:'warm, friendly, and polite', explanation:'A cordial greeting is friendly without being overly familiar.', example:'The two neighbors exchanged a cordial hello each morning.', memory:'Cordial sounds connected to the heart: friendly and warm.', quiz:'What is a cordial greeting like?', answer:'It is warm, friendly, and polite.', prompt:'Ask students to write a cordial two-sentence email to a classmate.' },
    { word:'tenacious', pos:'adjective', pronunciation:'tuh-NAY-shuhs', difficulty:'hard', definition:'not giving up easily', explanation:'A tenacious person keeps holding on to a goal, even when it is difficult.', example:'Her tenacious research finally uncovered the missing records.', memory:'Tenacious means you hold tight to the task.', quiz:'What word describes someone who keeps trying?', answer:'Tenacious.', prompt:'Students write one sentence about a tenacious person from history or sports.' },
    { word:'concise', pos:'adjective', pronunciation:'kuhn-SYSE', difficulty:'medium', definition:'using few words while still being clear', explanation:'Concise writing removes extra words but keeps the meaning.', example:'The instructions were concise, so everyone knew what to do.', memory:'Concise means clear and compact.', quiz:'Is concise writing long-winded or brief?', answer:'Brief.', prompt:'Give students a wordy sentence and 60 seconds to make it concise.' },
    { word:'curious', pos:'adjective', pronunciation:'KYUR-ee-uhs', difficulty:'easy', definition:'wanting to know or learn more', explanation:'A curious mind asks questions and looks for patterns.', example:'The curious student stayed after class to ask how the machine worked.', memory:'Curious starts with a question.', quiz:'What does a curious person like to do?', answer:'Ask questions and learn more.', prompt:'Ask each student to write one curious question about today\'s topic.' },
    { word:'eloquent', pos:'adjective', pronunciation:'EL-uh-kwuhnt', difficulty:'hard', definition:'expressing ideas clearly and beautifully', explanation:'An eloquent speaker or writer uses language in a graceful, effective way.', example:'Her eloquent speech made the audience feel hopeful.', memory:'Eloquent expression sounds elegant and clear.', quiz:'What does an eloquent speaker do well?', answer:'Express ideas clearly and beautifully.', prompt:'Students rewrite a flat opinion so it sounds more eloquent, without adding fluff.' },
    { word:'adapt', pos:'verb', pronunciation:'uh-DAPT', difficulty:'easy', definition:'to change so something works in a new situation', explanation:'When you adapt, you adjust your behavior, plan, or tool to fit new conditions.', example:'We had to adapt the lesson for a younger class.', memory:'Adapt means adjust.', quiz:'If plans change and you adjust, what do you do?', answer:'You adapt.', prompt:'Ask students how they would adapt a playground game for a rainy day.' }
  ];

  let calendar = [];
  let byDate = {};
  let fallbackWords = [];
  let current = null;
  let officialToday = null;
  let saved = [];
  let speechVoice = null;

  function pad(n) { return String(n).padStart(2, '0'); }

  function mapWotdDate(d) {
    let m = d.getMonth() + 1;
    let day = d.getDate();
    if (m === 2 && day === 29) day = 28;
    return '2026-' + pad(m) + '-' + pad(day);
  }

  function loadCalendar() {
    const raw = window._PAGE_DATA;
    if (!Array.isArray(raw) || !raw.length) return;
    calendar = raw.filter(row => row && row.date && row.word);
    byDate = {};
    calendar.forEach(row => { byDate[row.date] = row; });
  }

  function entryForDate(d) {
    const key = mapWotdDate(d);
    if (byDate[key]) return byDate[key];
    const cur = new Date(d.getFullYear(), d.getMonth(), d.getDate());
    for (let i = 0; i < 366; i++) {
      cur.setDate(cur.getDate() - 1);
      const k = mapWotdDate(cur);
      if (byDate[k]) return byDate[k];
    }
    return null;
  }

  function dayNumber(date) {
    const start = new Date(Date.UTC(2026, 0, 1));
    const utc = Date.UTC(date.getFullYear(), date.getMonth(), date.getDate());
    return Math.floor((utc - start.getTime()) / 86400000);
  }

  function curatedForDate(date) {
    const n = dayNumber(date);
    return curated[((n % curated.length) + curated.length) % curated.length];
  }

  function officialEntry(date) {
    return entryForDate(date) || curatedForDate(date);
  }

  function esc(s) {
    return String(s || '').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
  }

  function speechSupported() {
    return 'speechSynthesis' in window && 'SpeechSynthesisUtterance' in window;
  }

  function chooseSpeechVoice() {
    if (!speechSupported()) return null;
    const voices = window.speechSynthesis.getVoices();
    speechVoice =
      voices.find(voice => /^en(-|_)/i.test(voice.lang) && voice.localService) ||
      voices.find(voice => /^en(-|_)/i.test(voice.lang)) ||
      null;
    return speechVoice;
  }

  function setupSpeech() {
    const btn = document.getElementById('wotd-listen');
    if (!btn) return;
    if (!speechSupported()) {
      btn.hidden = true;
      return;
    }
    chooseSpeechVoice();
    if ('onvoiceschanged' in window.speechSynthesis) {
      window.speechSynthesis.onvoiceschanged = chooseSpeechVoice;
    }
  }

  function speakCurrentWord() {
    if (!current) return;
    if (!speechSupported()) {
      showToast('Audio not supported');
      return;
    }
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(current.word);
    utterance.lang = 'en-US';
    utterance.rate = 0.86;
    utterance.voice = speechVoice || chooseSpeechVoice();
    window.speechSynthesis.speak(utterance);
  }

  function dateLabel(date) {
    return date.toLocaleDateString(undefined, { weekday:'long', month:'long', day:'numeric', year:'numeric' });
  }

  function smallDate(date) {
    return date.toLocaleDateString(undefined, { month:'short', day:'numeric' });
  }

  function showToast(msg) {
    const t = document.getElementById('toast');
    if (!t) return;
    t.textContent = msg;
    t.classList.add('show');
    setTimeout(() => t.classList.remove('show'), 1800);
  }

  function copyText(text) {
    if (navigator.clipboard) navigator.clipboard.writeText(text);
    showToast('Copied!');
  }

  function render(entry, label, dateForLabel) {
    current = entry;
    const status = document.getElementById('wotd-status');
    const dateEl = document.getElementById('wotd-date');
    const wordEl = document.getElementById('wotd-word');
    if (!wordEl) return;
    if (status) status.textContent = label || "Today's word";
    if (dateEl) dateEl.textContent = label === 'Practice word' ? 'Extra practice' : dateLabel(dateForLabel || new Date());
    wordEl.textContent = entry.word;
    document.getElementById('wotd-meta').innerHTML =
      '<span class="wotd-pill">' + esc(entry.pos) + '</span>' +
      '<span class="wotd-pill soft">' + esc(entry.pronunciation || 'pronunciation varies') + '</span>' +
      '<span class="wotd-pill soft">' + esc(entry.difficulty) + '</span>';
    document.getElementById('wotd-definition').textContent = entry.definition;
    document.getElementById('wotd-explanation').textContent = entry.explanation || ('Use ' + entry.word + ' when you mean: ' + entry.definition + '.');
    document.getElementById('wotd-example').textContent = entry.example || ('Try using "' + entry.word + '" in one clear sentence today.');
    document.getElementById('wotd-memory').textContent = entry.memory || ('Memory hook: connect "' + entry.word + '" with the idea "' + entry.definition + '".');
    document.getElementById('wotd-quiz-q').textContent = entry.quiz || ('Write one sentence using "' + entry.word + '" correctly.');
    const ans = document.getElementById('wotd-quiz-a');
    ans.textContent = entry.answer || ('A good answer should show the meaning: ' + entry.definition + '.');
    ans.classList.remove('show');
  }

  function loadSaved() {
    try { saved = JSON.parse(localStorage.getItem('wordineer_wotd_saved') || '[]'); }
    catch (e) { saved = []; }
    renderSaved();
  }

  function saveSaved() {
    localStorage.setItem('wordineer_wotd_saved', JSON.stringify(saved));
    renderSaved();
  }

  function renderSaved() {
    const wrap = document.getElementById('wotd-saved-tags');
    const count = document.getElementById('wotd-saved-count');
    if (count) count.textContent = '(' + saved.length + ')';
    if (!wrap) return;
    if (!saved.length) {
      wrap.innerHTML = '<span class="saved-empty">Save words you want to practice later</span>';
      return;
    }
    wrap.innerHTML = saved.map(item =>
      '<span class="saved-tag">' + esc(item.word) + '<span class="saved-tag-remove" data-word="' + esc(item.word) + '">x</span></span>'
    ).join('');
    wrap.querySelectorAll('.saved-tag-remove').forEach(btn => {
      btn.addEventListener('click', () => {
        saved = saved.filter(item => item.word !== btn.dataset.word);
        saveSaved();
      });
    });
  }

  function saveCurrent() {
    if (!current) return;
    if (!saved.some(item => item.word === current.word)) {
      saved.push({ word: current.word, definition: current.definition });
      saveSaved();
    }
    showToast('Saved!');
  }

  function practiceEntryFromFallback(row) {
    return {
      word: row[0],
      pos: row[1] || 'word',
      pronunciation: '',
      difficulty: row[3] || 'medium',
      definition: row[2] || 'definition unavailable',
      explanation: 'This practice word comes from Wordineer\'s vocabulary dataset. Read the definition, then try using it in your own sentence.',
      example: 'Try writing one sentence that uses "' + row[0] + '" clearly.',
      memory: 'Connect the word to its meaning: ' + (row[2] || 'definition unavailable') + '.',
      quiz: 'What does "' + row[0] + '" mean?',
      answer: row[2] || 'Review the definition, then try again.'
    };
  }

  function surprise() {
    const todayWord = (officialToday && officialToday.word || '').toLowerCase();
    const calPool = calendar.filter(row => (row.word || '').toLowerCase() !== todayWord);
    const extra = fallbackWords.map(practiceEntryFromFallback);
    const pool = calPool.concat(extra);
    if (!pool.length) {
      render(curated[Math.floor(Math.random() * curated.length)], 'Practice word');
      return;
    }
    render(pool[Math.floor(Math.random() * pool.length)], 'Practice word');
  }

  function renderPrevious() {
    const wrap = document.getElementById('wotd-previous');
    if (!wrap) return;
    const today = new Date();
    const rows = [];
    for (let i = 1; i <= 7; i++) {
      const d = new Date(today);
      d.setDate(today.getDate() - i);
      const entry = officialEntry(d);
      rows.push('<button class="wotd-prev-btn" type="button" data-offset="' + i + '"><span class="wotd-prev-date">' + esc(smallDate(d)) + '</span><span class="wotd-prev-word">' + esc(entry.word) + '</span></button>');
    }
    wrap.innerHTML = rows.join('');
    wrap.querySelectorAll('.wotd-prev-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const d = new Date();
        d.setDate(d.getDate() - parseInt(btn.dataset.offset, 10));
        render(officialEntry(d), smallDate(d) + ' word', d);
      });
    });
  }

  function mondayOfWeek(d) {
    const x = new Date(d.getFullYear(), d.getMonth(), d.getDate());
    const dow = x.getDay();
    const offset = dow === 0 ? -6 : 1 - dow;
    x.setDate(x.getDate() + offset);
    return x;
  }

  function copyThisWeek() {
    const start = mondayOfWeek(new Date());
    const lines = ['date\tword\tpos\tdefinition\tprompt'];
    for (let i = 0; i < 7; i++) {
      const d = new Date(start);
      d.setDate(start.getDate() + i);
      const entry = entryForDate(d);
      if (!entry) continue;
      lines.push([entry.date, entry.word, entry.pos, entry.definition, entry.prompt].join('\t'));
    }
    if (lines.length === 1) return;
    if (navigator.clipboard) navigator.clipboard.writeText(lines.join('\n'));
    showToast("Copied this week's words.");
  }

  async function loadFallbackWords() {
    try {
      const res = await fetch('/data/words.json');
      const rows = await res.json();
      fallbackWords = rows.filter(row => row && row[0] && row[2] && row[0].length > 3 && row[0].length < 14).slice(0, 800);
    } catch (e) {
      fallbackWords = [];
    }
  }

  function bind() {
    document.getElementById('wotd-copy-word')?.addEventListener('click', () => current && copyText(current.word));
    document.getElementById('wotd-copy-example')?.addEventListener('click', () => current && copyText(current.example));
    document.getElementById('wotd-save-word')?.addEventListener('click', saveCurrent);
    document.getElementById('wotd-listen')?.addEventListener('click', speakCurrentWord);
    document.getElementById('wotd-surprise')?.addEventListener('click', surprise);
    document.getElementById('wotd-practice-copy')?.addEventListener('click', () => current && copyText('Write one original sentence using "' + current.word + '" to mean: ' + current.definition));
    document.getElementById('wotd-quiz-reveal')?.addEventListener('click', () => document.getElementById('wotd-quiz-a')?.classList.add('show'));
    document.getElementById('wotd-copy-saved')?.addEventListener('click', () => {
      if (!saved.length) return;
      copyText(saved.map(item => item.word + ' - ' + item.definition).join('\n'));
    });
    document.getElementById('wotd-print')?.addEventListener('click', () => window.print());
    document.getElementById('wotd-copy-week')?.addEventListener('click', copyThisWeek);

    document.querySelectorAll('.faq-q').forEach(q => {
      q.addEventListener('click', () => q.closest('.faq-item').classList.toggle('open'));
    });
  }

  async function init() {
    loadCalendar();
    bind();
    setupSpeech();
    loadSaved();
    const today = new Date();
    officialToday = officialEntry(today);
    render(officialToday, "Today's word", today);
    renderPrevious();
    await loadFallbackWords();
  }

  return { init };
})();

WORDINEER_WOTD.init();
```

Note: `#wotd-listen` and `#wotd-surprise` are inside `<!-- SSR_TODAY -->`, so they exist only after build. Local unbuilt source will not have those nodes until `build.py` runs. Always test the built output.

- [ ] **Step 2: Commit**

```bash
git add template-deploy/tools-src/word-of-the-day.html
git commit -m "feat: hydrate word-of-the-day from the 2026 calendar"
```

---

### Task 6: Explainer, FAQ, internal links

**Files:**
- Modify: `template-deploy/tools-src/word-of-the-day.html`

- [ ] **Step 1: Add a short paragraph to the explainer (after the first `<h2>` block) and four internal links**

Append this as a new section inside `SLOT:explainer` before the classroom heading:

```html
  <h2>The 2026 list, published in full</h2>
  <p>Most word-of-the-day pages hide tomorrow. This page publishes the whole year: 365 useful words with definitions and classroom prompts. Download the <a href="/data/wotd-2026.csv">CSV</a>, print the table, or copy this week for a lesson plan. For more vocabulary practice try the <a href="/word-tools">word tools hub</a>, the <a href="/">random word generator</a>, <a href="/sat-vocabulary-words">SAT vocabulary words</a>, and <a href="/esl-vocabulary-cefr">ESL vocabulary by CEFR level</a>.</p>
```

Use the same href form as other tool-src pages (build.py canonicalizes).

- [ ] **Step 2: Replace `SLOT:faq` so answers are wrapped in `<p>` and the three new questions exist**

Questions, in order, must match the FAQ schema from Task 4:

1. What's the fastest way to actually remember a new word?
2. What if today's word is too easy or too hard?
3. Do my saved words persist if I close the browser?
4. Does the word of the day change every day?
5. Can I download the full year list?
6. Can I print this for class?
7. Are these the same words Dictionary.com uses?
8. How do I use the Word of the Day as a classroom activity?
9. Where do the words come from?

First item has class `open`. Every `.faq-q` includes the chevron SVG:

```html
<svg class="faq-chevron" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
```

Each `.faq-a` wraps its answer in `<p>`. Reuse the answer text from the FAQ schema in Task 4.

- [ ] **Step 3: Commit**

```bash
git add template-deploy/tools-src/word-of-the-day.html
git commit -m "content: year-list explainer and FAQ on word-of-the-day"
```

---

### Task 7: Build, copy, verify

**Files:**
- Modify: `wordineer-deploy/word-of-the-day.html` (via copy of build output only)

- [ ] **Step 1: Build**

```bash
cd template-deploy && python3 build.py
```

Expected in the log: `ssr → 365 items baked into /word-of-the-day/` and a data copy that includes `wotd-2026.csv`.

- [ ] **Step 2: Confirm placeholders are gone in output**

```bash
python3 - <<'PY'
from pathlib import Path
html = Path('template-deploy/output/word-of-the-day.html').read_text()
assert '<!-- SSR_ROWS -->' not in html
assert '<!-- SSR_TODAY -->' not in html
assert 'wotd-month-01' in html
assert 'Download CSV' in html
assert '/data/wotd-2026.csv' in html
print('output HTML ok', html.count('<tr>'), 'table rows-ish')
PY
```

Expected: `output HTML ok` and a row count well above 365 (month header rows included).

- [ ] **Step 3: Copy to deploy**

```bash
cp template-deploy/output/word-of-the-day.html wordineer-deploy/word-of-the-day.html
```

`wotd-2026.json` and `wotd-2026.csv` already live in `wordineer-deploy/data/`. Do not copy the whole `output/data/` tree over other datasets.

- [ ] **Step 4: Serve and smoke-check**

```bash
cd wordineer-deploy && python3 -m http.server 8080
```

Open `http://localhost:8080/word-of-the-day.html`.

| Check | Expected |
|---|---|
| View source | Real words in the year table; no `SSR_ROWS` |
| Today’s card | Matches local date mapped to 2026; not stuck on Ephemeral |
| Previous 7 | Prior mapped words; clicking one updates the card only |
| Surprise me | Changes the card, not the table |
| Download CSV | `/data/wotd-2026.csv` with header + 365 rows |
| Copy this week | Toast “Copied this week's words.”; clipboard is TSV Mon–Sun |
| Print preview | Table + credit; nav/ads/FAQ hidden |
| FAQ | Accordion toggles; first item open |
| Mobile 360px | Card usable; table scrolls; month jumps wrap |
| Console | No errors |

- [ ] **Step 5: Commit built pages** (both paths are tracked in git)

```bash
git add template-deploy/output/word-of-the-day.html wordineer-deploy/word-of-the-day.html
git commit -m "chore: ship built word-of-the-day year list page"
```

---

### Task 8: Mark the spec approved

**Files:**
- Modify: `docs/superpowers/specs/2026-08-22-word-of-the-day-linkable-asset-design.md`

- [ ] **Step 1: Change status**

Replace `**Status:** Draft pending user review` with `**Status:** Approved`.

- [ ] **Step 2: Commit**

```bash
git add docs/superpowers/specs/2026-08-22-word-of-the-day-linkable-asset-design.md
git commit -m "docs: mark word-of-the-day linkable-asset spec approved"
```

---

## Spec coverage

| Spec requirement | Task |
|---|---|
| 365 JSON + CSV, unique dates/words, difficulty mix | 1–2 |
| Useful register, 12 seed words kept | 2 |
| `inject_data`, SSR today + year table | 3–4 |
| Copy CSV into output/data | 3 |
| Toolbar: CSV, print, copy week, month jumps | 4 |
| Table columns Date/Word/POS/Definition/Prompt | 3–4 |
| Local date map onto 2026; Feb 29 → 28 | 3, 5 |
| 12-word fallback if `_PAGE_DATA` missing | 5 |
| Surprise me from 365 + words.json, not official date | 5 |
| Previous 7 as buttons | 5 |
| Print CSS, no PDF library | 4–5 |
| Dataset + FAQ JSON-LD | 4, 6 |
| FAQ accordion + `<p>` answers + new questions | 6 |
| Four internal links | 6 |
| No dated URLs / embed / email / RSS | all (omitted) |
| Build, copy, manual verify | 7 |

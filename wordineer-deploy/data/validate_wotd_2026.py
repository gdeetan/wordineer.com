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

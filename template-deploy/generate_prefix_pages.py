#!/usr/bin/env python3
"""
generate_prefix_pages.py — generates 5-letter words starting with [XY] pages.

Usage:
    python3 generate_prefix_pages.py --batch 2   # 2-letter prefixes (Batch 1)
    python3 generate_prefix_pages.py --batch 3   # 3-letter prefixes (Batch 2, deferred)
    python3 generate_prefix_pages.py --test       # run self-tests and exit
    python3 generate_prefix_pages.py --batch 2 --dry-run  # print summary, write nothing
"""

import argparse
import json
import os
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from itertools import product

# ── paths ──────────────────────────────────────────────────────────────────────
SCRIPT_DIR   = os.path.dirname(os.path.abspath(__file__))
DEPLOY_DIR   = os.path.normpath(os.path.join(SCRIPT_DIR, '..', 'wordineer-deploy'))
DATA_DIR     = os.path.join(DEPLOY_DIR, 'data')
REDIRECTS    = os.path.join(DEPLOY_DIR, '_redirects')
SITEMAP      = os.path.join(SCRIPT_DIR, 'sitemap.xml')
TMPL_DIR     = os.path.join(SCRIPT_DIR, 'template')
TOOLS_JSON   = os.path.join(SCRIPT_DIR, 'tools.json')

MIN_WORDS    = 3

# Letters ordered by frequency in English — used to score Wordle picks
FREQ_ORDER   = 'ETAOINSHRDLUCMFGYPWBVKJXQZ'

# ── import helpers from build.py ───────────────────────────────────────────────
sys.path.insert(0, SCRIPT_DIR)
from build import build_mega_cols, build_footer_cols, read


def load_all_five_letter_words():
    """Return list of all word entries from five-letter-words-[a-z].json files."""
    words = []
    for letter in 'abcdefghijklmnopqrstuvwxyz':
        path = os.path.join(DATA_DIR, f'five-letter-words-{letter}.json')
        if not os.path.exists(path):
            continue
        try:
            with open(path, encoding='utf-8') as f:
                words.extend(json.load(f))
        except json.JSONDecodeError as e:
            print(f'  warning: could not parse {path}: {e}', file=sys.stderr)
    if not words:
        print(f'  warning: no five-letter word data found in {DATA_DIR}', file=sys.stderr)
    return words


def filter_by_prefix(words, prefix):
    """Return words whose 'w' field starts with prefix (case-insensitive)."""
    p = prefix.lower()
    return [w for w in words if w['w'].lower().startswith(p)]


def has_enough_words(words, prefix, min_count=MIN_WORDS):
    return len(filter_by_prefix(words, prefix)) >= min_count


def compute_best_picks(words, n=5):
    """
    Score each word by how many unique high-frequency English letters it covers
    in positions 2, 3, 4 (0-indexed) — the unknown slots when prefix is confirmed.
    Returns top n words sorted by score desc, then alphabetically.
    """
    freq_rank = {ch: i for i, ch in enumerate(FREQ_ORDER)}

    def score(entry):
        tail = entry['w'][2:].upper()          # positions 2,3,4
        unique_tail = set(tail)
        # Lower rank index = more common letter. Sum of ranks = lower is better.
        return sum(freq_rank.get(ch, len(FREQ_ORDER)) for ch in unique_tail)

    sorted_words = sorted(words, key=lambda e: (score(e), e['w']))
    return sorted_words[:n]


def compute_position_freq(words, pos=2, top_n=5):
    """Return list of (letter, count) for the top_n most common letters at position pos."""
    counts = Counter(w['w'][pos].upper() for w in words if len(w['w']) > pos)
    return counts.most_common(top_n)


TYPE_LABELS = {
    'noun': 'Nouns',
    'verb': 'Verbs',
    'adjective': 'Adjectives',
    'adj': 'Adjectives',
    'adverb': 'Adverbs',
    'adv': 'Adverbs',
}


def group_by_type(words):
    """Return dict: {display_label: [entries]} for each part of speech present."""
    groups = {}
    for entry in words:
        label = TYPE_LABELS.get(entry.get('t', '').lower())
        if label:
            groups.setdefault(label, []).append(entry)
    for label in groups:
        groups[label].sort(key=lambda e: e['w'])
    return groups


def run_tests():
    print('Running self-tests...')

    sample = [
        {'w': 'stare', 't': 'verb',      'd': 'to look fixedly'},
        {'w': 'stone', 't': 'noun',      'd': 'a rock'},
        {'w': 'strip', 't': 'verb',      'd': 'to remove covering'},
        {'w': 'stern', 't': 'adjective', 'd': 'serious'},
        {'w': 'crimp', 't': 'verb',      'd': 'to press into folds'},
        {'w': 'crane', 't': 'noun',      'd': 'a large bird'},
    ]

    # filter_by_prefix
    st_words = filter_by_prefix(sample, 'st')
    assert len(st_words) == 4, f'Expected 4 ST words, got {len(st_words)}'
    cr_words = filter_by_prefix(sample, 'cr')
    assert len(cr_words) == 2, f'Expected 2 CR words, got {len(cr_words)}'
    assert filter_by_prefix(sample, 'zz') == [], 'Expected empty for ZZ'
    print('filter_by_prefix: OK')

    # has_enough_words
    assert has_enough_words(sample, 'st') is True
    assert has_enough_words(sample, 'cr') is False   # only 2, below min of 3
    print('has_enough_words: OK')

    # compute_best_picks
    picks = compute_best_picks(st_words, n=2)
    assert len(picks) == 2
    assert all('w' in p for p in picks)
    print('compute_best_picks: OK')

    # compute_position_freq
    freq = compute_position_freq(st_words, pos=2)
    assert len(freq) <= 5
    assert all(isinstance(letter, str) and isinstance(count, int) for letter, count in freq)
    print('compute_position_freq: OK')

    # group_by_type
    groups = group_by_type(st_words)
    assert 'Verbs' in groups
    assert 'Nouns' in groups
    assert 'stare' in [e['w'] for e in groups['Verbs']]
    assert all(groups[label] == sorted(groups[label], key=lambda e: e['w'])
               for label in groups), 'Groups not sorted alphabetically'
    print('group_by_type: OK')

    # edge cases
    assert filter_by_prefix([], 'st') == [], 'Empty list should return empty'
    assert compute_best_picks([], n=5) == [], 'Empty list should return empty picks'
    assert compute_position_freq([], pos=2) == [], 'Empty list should return empty freq'
    assert group_by_type([]) == {}, 'Empty list should return empty groups'
    print('edge cases: OK')

    print('All tests passed.')


if __name__ == '__main__':
    if not os.path.isdir(DEPLOY_DIR):
        sys.exit(f'Error: wordineer-deploy/ not found at {DEPLOY_DIR}')

    parser = argparse.ArgumentParser()
    parser.add_argument('--batch', type=int, choices=[2, 3], help='Prefix length to generate')
    parser.add_argument('--dry-run', action='store_true', help='Print summary without writing files')
    parser.add_argument('--test', action='store_true', help='Run self-tests and exit')
    args = parser.parse_args()

    if args.test:
        run_tests()
        sys.exit(0)

    if not args.batch:
        parser.error('--batch is required unless --test is specified')

    main(args.batch, dry_run=args.dry_run)

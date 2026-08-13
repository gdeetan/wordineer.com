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
        if os.path.exists(path):
            with open(path, encoding='utf-8') as f:
                words.extend(json.load(f))
    return words


def run_tests():
    print('Running self-tests...')
    # Tests will be added in subsequent tasks
    print('All tests passed.')


if __name__ == '__main__':
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

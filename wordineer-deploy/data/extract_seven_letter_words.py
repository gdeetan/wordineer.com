#!/usr/bin/env python3
"""Extract all 7-letter words from existing Wordineer word datasets."""
import json, os, re

BASE = os.path.dirname(os.path.abspath(__file__))
SOURCES = ['words.json', 'words_expanded.json']
OUT = os.path.join(BASE, 'seven-letter-words.json')

seen = set()
results = []

for src in SOURCES:
    path = os.path.join(BASE, src)
    if not os.path.exists(path):
        print(f'  skipping {src} (not found)')
        continue
    with open(path) as f:
        data = json.load(f)
    if isinstance(data, dict):
        items = list(data.values())
    else:
        items = data
    for item in items:
        if isinstance(item, list):
            item = {'w': item[0], 't': item[1] if len(item) > 1 else 'noun',
                    'd': item[2] if len(item) > 2 else '', 'diff': item[3] if len(item) > 3 else 'medium'}
        w = item.get('w', '')
        if len(w) != 7 or not re.match(r'^[A-Za-z]+$', w):
            continue
        key = w.lower()
        if key in seen:
            continue
        seen.add(key)
        results.append({
            'w': w[0].upper() + w[1:].lower(),
            't': item.get('t', 'noun'),
            'd': (item.get('d') or '')[:100],
            'diff': item.get('diff', 'medium')
        })

results.sort(key=lambda x: x['w'].lower())

with open(OUT, 'w') as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print(f'Done. Wrote {len(results)} words to seven-letter-words.json')

easy   = sum(1 for r in results if r['diff'] == 'easy')
medium = sum(1 for r in results if r['diff'] == 'medium')
hard   = sum(1 for r in results if r['diff'] == 'hard')
print(f'  easy:{easy}  medium:{medium}  hard:{hard}')

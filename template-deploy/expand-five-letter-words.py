import json

VOWELS = set('aeiou')

def analyze(word):
    w = word.lower()
    vow = ''.join(c for c in w if c in VOWELS)
    return {
        "w": word.lower(),
        "vowel_count": len(vow),
        "vowels": vow if vow else "",
        "unique_letters": len(set(w)) == 5,
        "bits": None
    }

with open('../wordineer-deploy/data/five-letter-words-analyzed.json') as f:
    analyzed = json.load(f)

with open('../wordineer-deploy/data/five-letter-words.json') as f:
    raw = json.load(f)

# Pool is list of objects with "w" key
pool_words = [e['w'].lower() for e in raw if len(e.get('w', '')) == 5 and e['w'].isalpha()]

existing = {e['w'].lower() for e in analyzed}

# Preserve existing entries; add new ones not already in analyzed
new_entries = [analyze(w) for w in pool_words if w not in existing]

# Sort existing: ranked (bits not None) first descending, then unranked
ranked = [e for e in analyzed if e.get('bits') is not None]
ranked.sort(key=lambda e: e['bits'], reverse=True)
unranked_existing = [e for e in analyzed if e.get('bits') is None]

combined = ranked + unranked_existing + new_entries

# Take top 1000 (or however many available)
result = combined[:1000]

with open('../wordineer-deploy/data/five-letter-words-analyzed.json', 'w') as f:
    json.dump(result, f, separators=(',', ':'))

print(f"Done: {len(result)} words written ({len(new_entries)} new entries added)")

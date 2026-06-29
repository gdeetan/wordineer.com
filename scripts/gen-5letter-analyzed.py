import json, re
from pathlib import Path

DATA = Path("wordineer-deploy/data")

with open(DATA / "wordle-common.json") as f:
    common = json.load(f)  # list of lowercase 5-letter strings

with open(DATA / "wordle-openers.json") as f:
    openers_raw = json.load(f)

# Handle both array of objects and other formats
if isinstance(openers_raw, list) and len(openers_raw) > 0 and isinstance(openers_raw[0], dict):
    bits_map = {o["word"].lower(): o["bits"] for o in openers_raw}
else:
    bits_map = {}

VOWELS = set("aeiou")

def analyze(word):
    w = word.lower()
    vowels_in_word = sorted(set(c for c in w if c in VOWELS))
    return {
        "w": w,
        "vowel_count": len(vowels_in_word),
        "vowels": "".join(vowels_in_word),
        "unique_letters": len(set(w)) == 5,
        "bits": bits_map.get(w),
    }

results = [analyze(w) for w in common if isinstance(w, str) and len(w) == 5]
results.sort(key=lambda x: (-(x["bits"] or 0), x["w"]))

with open(DATA / "five-letter-words-analyzed.json", "w") as f:
    json.dump(results, f, separators=(",", ":"))

print(f"Written {len(results)} words")

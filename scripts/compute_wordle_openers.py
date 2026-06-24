#!/usr/bin/env python3
"""
Compute the top 40 entropy-ranked Wordle opening words.

Run once offline (not part of the site build):
    python3 scripts/compute_wordle_openers.py

Reads:
  wordineer-deploy/data/wordle-guesses.json  — full valid-guess dictionary
  wordineer-deploy/data/wordle-common.json   — plausible-answer pool

Outputs:
  wordineer-deploy/data/wordle-openers.json  — top-40 openers by Shannon entropy
"""
import json
import math
import time
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).parent.parent / "wordineer-deploy" / "data"

def load(name):
    with open(ROOT / name) as f:
        return json.load(f)

# Two-pass duplicate-safe pattern: mirrors computePattern() in wordle-engine.js exactly.
# Returns a tuple of 5 ints: 2=green, 1=yellow, 0=grey.
def compute_pattern(guess, target):
    result = [0, 0, 0, 0, 0]
    t_left = list(target)
    g_left = list(guess)

    # Pass 1: exact matches (green)
    for i in range(5):
        if g_left[i] == t_left[i]:
            result[i] = 2
            t_left[i] = None
            g_left[i] = None

    # Pass 2: present but wrong position (yellow)
    for i in range(5):
        if g_left[i] is None:
            continue
        try:
            j = t_left.index(g_left[i])
            result[i] = 1
            t_left[j] = None
        except ValueError:
            pass

    return tuple(result)

def entropy(guess, common):
    buckets = Counter(compute_pattern(guess, t) for t in common)
    n = len(common)
    return -sum((c / n) * math.log2(c / n) for c in buckets.values())

# Frequency-ordered high-value letters for note generation
FREQ_ORDER = "ETAOINSHRDLCUMWFGYPBVKJXQZ"

def make_note(word):
    uniq = list(dict.fromkeys(word))  # preserve order, deduplicate
    count = len(uniq)
    # Top-3 letters by FREQ_ORDER that appear in the word
    top = [c for c in FREQ_ORDER if c in word][:3]
    covers = ", ".join(top) if top else ""
    if count == 5:
        return f"covers {covers} — 5 distinct letters"
    else:
        return f"covers {covers} — {count} distinct letters"

def main():
    guesses = [w.upper() for w in load("wordle-guesses.json")]
    common  = [w.upper() for w in load("wordle-common.json")]

    print(f"Scoring {len(guesses)} guess words against {len(common)} answer pool words…")
    t0 = time.time()

    results = []
    for i, word in enumerate(guesses):
        if i % 100 == 0 and i > 0:
            elapsed = time.time() - t0
            eta = elapsed / i * (len(guesses) - i)
            print(f"  {i}/{len(guesses)} — {elapsed:.1f}s elapsed, ~{eta:.0f}s remaining")
        bits = entropy(word, common)
        results.append((word, bits))

    results.sort(key=lambda x: -x[1])
    top40 = results[:40]

    elapsed = time.time() - t0
    print(f"\nDone in {elapsed:.1f}s. Top 10:")
    for rank, (word, bits) in enumerate(top40[:10], 1):
        print(f"  {rank:2}. {word}  {bits:.4f} bits")

    out = [
        {"word": word, "bits": round(bits, 2), "note": make_note(word)}
        for word, bits in top40
    ]

    out_path = ROOT / "wordle-openers.json"
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nWrote {len(out)} entries → {out_path}")

if __name__ == "__main__":
    main()

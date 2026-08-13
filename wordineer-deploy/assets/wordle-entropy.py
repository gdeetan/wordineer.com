"""
wordle_entropy.py — Entropy ranking of all valid Wordle starting words.

Ports the exact algorithm from wordineer-deploy/scripts/wordle-engine.js:
  - Equal probability per remaining candidate (no frequency weighting)
  - Shannon entropy: H = -sum(p * log2(p)) over pattern buckets
  - Two-pass duplicate-safe pattern computation (green first, then yellow)
  - PROBE_THRESHOLD = 150: when pool > 150, guess from full dict; else from pool

Data:
  wordle-common.json  → answer pool (642 words)
  wordle-guesses.json → full guess dict (715 words)

Outputs:
  output/starting-words-full.csv      (word, entropy_bits, expected_remaining, rank)
  output/starting-words-top100.json   (top 100 for site consumption)
"""

import json
import csv
import math
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
DATA_DIR  = REPO_ROOT / "wordineer-deploy" / "data"
OUT_DIR   = Path(__file__).parent / "output"
OUT_DIR.mkdir(exist_ok=True)

PROBE_THRESHOLD = 150  # must match JS constant


def compute_pattern(guess: str, target: str) -> tuple:
    """Two-pass duplicate-safe pattern computation. Returns 5-tuple of 0/1/2."""
    result = [0, 0, 0, 0, 0]
    t_left = list(target)
    g_left = list(guess)

    # Pass 1: exact matches (green = 2)
    for i in range(5):
        if g_left[i] == t_left[i]:
            result[i] = 2
            t_left[i] = None
            g_left[i] = None

    # Pass 2: present but wrong position (yellow = 1)
    for i in range(5):
        if g_left[i] is None:
            continue
        if g_left[i] in t_left:
            result[i] = 1
            t_left[t_left.index(g_left[i])] = None

    return tuple(result)


def rank_candidates(remaining_pool: list, full_dict: list) -> list:
    """
    Rank guesses by Shannon entropy against remaining_pool.
    Returns list of dicts sorted descending by score.
    Mirrors rankCandidates() in wordle-engine.js exactly.
    """
    if not remaining_pool:
        return []
    if len(remaining_pool) == 1:
        return [{"word": remaining_pool[0], "score": float("inf"), "is_candidate": True}]

    guess_set = full_dict if (full_dict and len(remaining_pool) > PROBE_THRESHOLD) else remaining_pool
    remaining_set = set(remaining_pool)
    n = len(remaining_pool)

    results = []
    for guess in guess_set:
        buckets: dict = {}
        for target in remaining_pool:
            key = compute_pattern(guess, target)
            buckets[key] = buckets.get(key, 0) + 1
        score = 0.0
        for count in buckets.values():
            p = count / n
            score -= p * math.log2(p)
        # expected remaining = sum(count * count/n) = sum(count^2) / n
        expected_remaining = sum(c * c for c in buckets.values()) / n
        results.append({
            "word": guess,
            "score": score,
            "expected_remaining": expected_remaining,
            "is_candidate": guess in remaining_set,
        })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results


def main():
    print("Loading word data...")
    common  = json.loads((DATA_DIR / "wordle-common.json").read_text())
    guesses = json.loads((DATA_DIR / "wordle-guesses.json").read_text())
    print(f"  Answer pool: {len(common)} words")
    print(f"  Guess dict:  {len(guesses)} words")

    # For starting word ranking, remaining pool = full answer pool
    print(f"\nRanking {len(guesses)} starting words by entropy against {len(common)}-word answer pool...")
    print("(This may take a minute — ~715 × 642 = 459k pattern calls)")
    ranked = rank_candidates(common, guesses)
    print(f"Done. Top 5:")
    for i, r in enumerate(ranked[:5], 1):
        print(f"  #{i:3d}  {r['word'].upper()}  {r['score']:.4f} bits  "
              f"(expected remaining: {r['expected_remaining']:.1f})")

    # Sanity checks
    print("\nSanity checks:")
    words_to_check = ["slate", "crane", "raise", "roate", "fuzzy", "mamma"]
    word_ranks = {r["word"]: i + 1 for i, r in enumerate(ranked)}
    for w in words_to_check:
        rank = word_ranks.get(w, "NOT FOUND")
        flag = " ⚠️  BAD" if w in ("fuzzy", "mamma") and isinstance(rank, int) and rank <= 20 else ""
        print(f"  {w.upper()}: rank #{rank}{flag}")

    # Check top-20 doesn't include known weak words
    top20 = {r["word"] for r in ranked[:20]}
    bad = top20 & {"fuzzy", "mamma"}
    if bad:
        print(f"\n⚠️  WARNING: Known-weak words in top 20: {bad}")
        print("   Stop and debug before publishing — something is wrong.")
        return

    # Write CSV
    csv_path = OUT_DIR / "starting-words-full.csv"
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["rank", "word", "entropy_bits", "expected_remaining"])
        writer.writeheader()
        for i, r in enumerate(ranked, 1):
            writer.writerow({
                "rank": i,
                "word": r["word"].upper(),
                "entropy_bits": round(r["score"], 4),
                "expected_remaining": round(r["expected_remaining"], 2),
            })
    print(f"\nWrote {csv_path}")

    # Write top-100 JSON
    top100 = [
        {
            "rank": i + 1,
            "word": r["word"].upper(),
            "entropy_bits": round(r["score"], 4),
            "expected_remaining": round(r["expected_remaining"], 2),
        }
        for i, r in enumerate(ranked[:100])
    ]
    json_path = OUT_DIR / "starting-words-top100.json"
    json_path.write_text(json.dumps(top100, indent=2))
    print(f"Wrote {json_path}")

    return ranked


if __name__ == "__main__":
    main()

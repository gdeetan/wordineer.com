"""
wordle_benchmark.py — 10,000-game solver benchmark simulation.

Simulates the Wordineer Wordle solver playing 10,000 games:
  - Fixed opener = best word from wordle_entropy.py ranking
  - Each subsequent guess = highest-entropy recommendation
  - Secret words drawn from wordle-common.json (uniform random, seed=42)
  - Also benchmarks SLATE, CRANE, RAISE for comparison table

Same algorithm as wordle_entropy.py (exact port of wordle-engine.js).

Outputs:
  output/benchmark.json — per-opener stats: mean, median, solve-rate, distribution
"""

import json
import math
import random
import statistics
from pathlib import Path

REPO_ROOT   = Path(__file__).parent.parent
DATA_DIR    = REPO_ROOT / "wordineer-deploy" / "data"
OUT_DIR     = Path(__file__).parent / "output"
OUT_DIR.mkdir(exist_ok=True)

PROBE_THRESHOLD = 150
SEED            = 42
N_GAMES         = 10_000


# ── Algorithm (identical to wordle_entropy.py) ──────────────────────────────

def compute_pattern(guess: str, target: str) -> tuple:
    result = [0, 0, 0, 0, 0]
    t_left = list(target)
    g_left = list(guess)
    for i in range(5):
        if g_left[i] == t_left[i]:
            result[i] = 2
            t_left[i] = None
            g_left[i] = None
    for i in range(5):
        if g_left[i] is None:
            continue
        if g_left[i] in t_left:
            result[i] = 1
            t_left[t_left.index(g_left[i])] = None
    return tuple(result)


def filter_candidates(pool: list, history: list) -> list:
    def consistent(candidate):
        for word, pattern in history:
            if compute_pattern(word, candidate) != pattern:
                return False
        return True
    return [w for w in pool if consistent(w)]


def best_guess(remaining: list, full_dict: list) -> str:
    if len(remaining) == 1:
        return remaining[0]
    guess_set = full_dict if (full_dict and len(remaining) > PROBE_THRESHOLD) else remaining
    remaining_set = set(remaining)
    n = len(remaining)
    best_word  = None
    best_score = -1.0
    for guess in guess_set:
        buckets: dict = {}
        for target in remaining:
            key = compute_pattern(guess, target)
            buckets[key] = buckets.get(key, 0) + 1
        score = 0.0
        for count in buckets.values():
            p = count / n
            score -= p * math.log2(p)
        # Prefer candidates over non-candidates on tie (mirrors JS sort stability)
        is_cand = guess in remaining_set
        if score > best_score or (score == best_score and is_cand and best_word not in remaining_set):
            best_score = score
            best_word  = guess
    return best_word


def simulate_game(secret: str, opener: str, common: list, guesses: list) -> int:
    """Returns number of guesses to solve, or 7 if failed (> 6 guesses)."""
    history  = []
    remaining = list(common)
    for attempt in range(1, 8):
        if attempt == 1:
            guess = opener
        else:
            guess = best_guess(remaining, guesses)
            if guess is None:
                return 7  # no candidates left — shouldn't happen

        pattern = compute_pattern(guess, secret)
        history.append((guess, pattern))

        if pattern == (2, 2, 2, 2, 2):
            return attempt

        remaining = filter_candidates(remaining, history)
        if not remaining:
            return 7

    return 7


def run_benchmark(opener: str, secrets: list, common: list, guesses: list) -> dict:
    print(f"  Simulating {N_GAMES} games with opener {opener.upper()}...")
    counts = []
    distribution = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, "fail": 0}
    for i, secret in enumerate(secrets):
        n = simulate_game(secret, opener, common, guesses)
        counts.append(n)
        if n <= 6:
            distribution[n] += 1
        else:
            distribution["fail"] += 1
        if (i + 1) % 1000 == 0:
            print(f"    {i + 1}/{N_GAMES} games done...")

    solve_rate = sum(1 for c in counts if c <= 6) / len(counts)
    return {
        "opener":        opener.upper(),
        "n_games":       N_GAMES,
        "seed":          SEED,
        "mean_guesses":  round(statistics.mean(counts), 3),
        "median_guesses": statistics.median(counts),
        "solve_rate_6":  round(solve_rate, 4),
        "distribution":  distribution,
    }


def main():
    print("Loading word data...")
    common  = json.loads((DATA_DIR / "wordle-common.json").read_text())
    guesses = json.loads((DATA_DIR / "wordle-guesses.json").read_text())
    print(f"  Answer pool: {len(common)}, Guess dict: {len(guesses)}")

    # Load top-ranked opener from entropy output
    top100_path = OUT_DIR / "starting-words-top100.json"
    if not top100_path.exists():
        print("\nERROR: Run wordle_entropy.py first to generate starting-words-top100.json")
        return

    top100  = json.loads(top100_path.read_text())
    top_word = top100[0]["word"].lower()
    print(f"\nTop-ranked opener: {top_word.upper()} ({top100[0]['entropy_bits']} bits)")

    # Fixed secret sequence (reproducible)
    rng = random.Random(SEED)
    secrets = [rng.choice(common) for _ in range(N_GAMES)]

    openers_to_test = [top_word, "slate", "crane", "raise"]
    # Deduplicate while preserving order
    seen = set()
    openers_to_test = [o for o in openers_to_test if not (o in seen or seen.add(o))]

    results = {}
    for opener in openers_to_test:
        stats = run_benchmark(opener, secrets, common, guesses)
        results[opener.upper()] = stats
        sr = stats["solve_rate_6"] * 100
        print(f"  → solve rate: {sr:.1f}%, mean: {stats['mean_guesses']:.3f} guesses")

    # Write output
    out_path = OUT_DIR / "benchmark.json"
    out_path.write_text(json.dumps(results, indent=2))
    print(f"\nWrote {out_path}")

    # Plain-English findings summary (suitable to quote on site)
    top_stats = results[top_word.upper()]
    sr = top_stats["solve_rate_6"] * 100
    mean = top_stats["mean_guesses"]
    print("\n" + "=" * 60)
    print("FINDINGS SUMMARY (review before publishing)")
    print("=" * 60)
    print(f"Best opener:    {top_word.upper()} ({top100[0]['entropy_bits']} bits)")
    print(f"Solve rate:     {sr:.1f}% within 6 guesses")
    print(f"Mean guesses:   {mean:.2f}")
    print(f"Seed:           {SEED}")
    print(f"Games:          {N_GAMES:,}")
    print()
    print('Quote-ready stat:')
    print(f'  "Playing the recommended guess every turn solves {sr:.1f}% of games in')
    print(f'   6 or fewer, averaging {mean:.2f} guesses ({N_GAMES:,} simulated games, seed {SEED})."')
    print()
    print("Comparison table:")
    for name, s in results.items():
        print(f"  {name:8s}: {s['solve_rate_6']*100:.1f}% solve, {s['mean_guesses']:.3f} mean")

    return results


if __name__ == "__main__":
    main()

# Methodology: Wordineer Wordle Entropy Analysis

**Published:** July 2026  
**Seed:** 42  
**Reproducible:** Yes — see reproduction instructions below.

---

## Candidate pool

We used Wordineer's own word lists, the same data the live Wordle Helper tool uses:

- **Answer pool** (`wordle-common.json`): 642 plausible Wordle answers — common English 5-letter words.
- **Guess dictionary** (`wordle-guesses.json`): 715 valid 5-letter words accepted as guesses.

**Important limitation:** These lists are curated by Wordineer and do not claim to be the exact NYT Wordle answer or guess lists. The NYT list is not published and changes over time. Rankings may differ from analyses that use other word lists.

---

## Entropy formula

For each candidate starting word *g*, we compute the Shannon information gain against the full answer pool:

```
H(g) = -Σ  p_i · log₂(p_i)
```

where *p_i = |bucket_i| / |pool|* and each bucket groups all answers that produce the same colour pattern when *g* is guessed.

- Higher entropy = the guess partitions the remaining answers into more evenly sized groups = more information gained = better starting word.
- Units: bits of information.
- No frequency weighting is applied — each remaining answer is treated as equally likely, matching the live tool's behaviour.

---

## Pattern computation

The colour pattern for a guess/target pair is computed with a two-pass duplicate-safe algorithm:

1. **Pass 1 (green):** Mark exact position matches. Remove matched letters from both guess and target.
2. **Pass 2 (yellow):** For each remaining guess letter, check if it appears in the remaining target letters. If yes, mark yellow and consume that target letter to prevent double-counting.

This correctly handles duplicate letters (e.g. ABBEY vs KEBAB).

---

## Probe word threshold

When the remaining answer pool exceeds 150 words, the scorer tests every word in the guess dictionary (715 words) — not just the remaining pool — because a non-answer word can sometimes partition the pool more evenly. Below 150 words the advantage is negligible and only the remaining pool is scored.

This matches `PROBE_THRESHOLD = 150` in `wordle-engine.js`.

---

## Benchmark simulation

- **Games:** 10,000
- **Secret words:** drawn uniformly at random from the 642-word answer pool using Python's `random.Random(42)` — fixed seed, fully reproducible.
- **Strategy:** Play the opener, then always play the highest-entropy recommendation at each subsequent step (same algorithm as the live tool).
- **Openers compared:** TRACE (our top-ranked word), SLATE, CRANE, RAISE.
- **Failure criterion:** More than 6 guesses counts as a failed game.

---

## Results summary

| Opener | Entropy (bits) | Solve rate | Mean guesses |
|--------|---------------|------------|--------------|
| TRACE  | 5.9894        | 100.0%     | 3.02         |
| SLATE  | 5.9492        | 100.0%     | 3.02         |
| CRANE  | 5.5951        | 100.0%     | 3.03         |
| RAISE  | n/a*          | 100.0%     | 3.09         |

\* RAISE is not in the Wordineer guess dictionary, so it has no entropy ranking. It was included as a comparison opener because it is widely discussed.

The 100% solve rate is achievable because the 642-word answer pool is small relative to the solver's ability to partition it; with the full NYT list (~2,300+ answers) failure rates would be higher.

---

## Limitations

- **Not the NYT list.** Published rankings reflect Wordineer's word lists, not the actual NYT puzzle sequence.
- **Equal-probability assumption.** The solver treats all remaining answers as equally likely. A Bayesian solver that weights by real-world word frequency might behave differently.
- **Small answer pool.** 642 answers is small; the 100% solve rate would not hold on larger corpora.
- **Static word lists.** The NYT occasionally adds or removes words. Our lists are a snapshot as of July 2026.

---

## Reproduction

```bash
git clone <this repo>
cd research
pip install matplotlib
python3 wordle_entropy.py     # generates starting-words-full.csv + starting-words-top100.json
python3 wordle_benchmark.py   # requires starting-words-top100.json; generates benchmark.json
python3 wordle_charts.py      # requires both JSON outputs; generates PNG charts
```

All outputs are deterministic for a given version of the word lists and seed 42.

---

## License

- **Data** (CSV, JSON outputs): CC BY 4.0 — free to use with attribution to Wordineer (wordineer.com).
- **Code** (Python scripts): MIT.

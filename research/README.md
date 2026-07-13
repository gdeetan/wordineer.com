# Wordineer Wordle Entropy Analysis

Original Shannon entropy rankings for Wordle starting words, with a reproducible 10,000-game benchmark simulation. Data lives at **[wordineer.com/best-wordle-starting-words/](https://wordineer.com/best-wordle-starting-words/)**.

## What's in this dataset

| File | Description |
|------|-------------|
| `output/starting-words-full.csv` | All 715 valid starting words ranked by Shannon entropy (rank, word, entropy_bits, expected_remaining) |
| `output/starting-words-top100.json` | Top 100 words — same fields, JSON format for web consumption |
| `output/benchmark.json` | 10,000-game simulation results for TRACE, SLATE, CRANE, RAISE |
| `output/top-20-openers.png` | Horizontal bar chart of top 20 openers by entropy (1200×675) |
| `output/guess-distribution.png` | Guess distribution comparison across 4 openers (1200×675) |
| `output/og-wordle-helper.png` | OG card for wordineer.com/wordle-helper/ (1200×630) |
| `output/methodology.md` | Full methodology: candidate pool, formula, simulation setup, limitations |

## Key findings

| Opener | Entropy (bits) | Solve rate | Mean guesses |
|--------|---------------|------------|--------------|
| **TRACE** | 5.9894 | 100% | 3.02 |
| SLATE | 5.9492 | 100% | 3.02 |
| CRANE | 5.5951 | 100% | 3.03 |
| RAISE | n/a* | 100% | 3.09 |

\* RAISE is not in the Wordineer guess dictionary. Included as a comparison opener because it's widely discussed.

10,000 games · Python seed 42 · answer pool: 642 words · guess dict: 715 words.

## Algorithm

Pure Shannon entropy, equal probability per remaining candidate — no frequency weighting:

```
H(guess) = -Σ p_i · log₂(p_i)
```

where each bucket groups answers that produce the same color pattern. Two-pass duplicate-safe pattern computation (green first, then yellow). Probe word threshold: when the remaining pool exceeds 150 words, all 715 guess-dict words are scored; otherwise only the remaining pool.

This matches the live tool at wordineer.com/wordle-helper/ exactly.

## Reproduce

```bash
git clone <this-repo>
cd research

pip install matplotlib

# 1. Rank all starting words (~5 seconds)
python3 wordle_entropy.py

# 2. Run 10,000-game benchmark (~10 minutes)
python3 wordle_benchmark.py

# 3. Generate charts
python3 wordle_charts.py
```

All outputs are deterministic for a given word list and seed 42.

Data files used: `../wordineer-deploy/data/wordle-common.json` (answer pool) and `../wordineer-deploy/data/wordle-guesses.json` (guess dict). If you cloned only this research folder, copy those two files into a `data/` subdirectory and update the paths in `wordle_entropy.py`.

## License

- **Data** (`output/*.csv`, `output/*.json`): [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) — free to use with attribution to Wordineer (wordineer.com)
- **Code** (`*.py`): MIT

## Citation

```
Wordineer (2026). Best Wordle Starting Words — Ranked by Information Theory.
wordineer.com/best-wordle-starting-words/
```

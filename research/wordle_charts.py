"""
wordle_charts.py — Generate chart assets for the Wordle Helper research page.

Outputs:
  output/top-20-openers.png     (1200×675, horizontal bar chart)
  output/guess-distribution.png (1200×675, grouped bar chart)
  output/og-wordle-helper.png   (1200×630, OG card)
"""

import json
import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch

OUT_DIR  = Path(__file__).parent / "output"

# Site colors from global.css custom properties
BRAND      = "#4A3FD4"
BRAND_DARK = "#3C3489"
GREEN      = "#1D9E75"
GREEN_LT   = "#E1F5EE"
AMBER      = "#BA7517"
BLUE       = "#185FA5"
TEXT       = "#1a1a18"
TEXT_2     = "#5a5a56"
TEXT_3     = "#9a9a94"
BG         = "#ffffff"
BG_2       = "#f7f7f4"
BG_3       = "#f0f0ec"


def load_top100():
    return json.loads((OUT_DIR / "starting-words-top100.json").read_text())


def load_benchmark():
    return json.loads((OUT_DIR / "benchmark.json").read_text())


def chart_top20():
    top100 = load_top100()
    top20  = top100[:20]
    words  = [r["word"] for r in top20]
    bits   = [r["entropy_bits"] for r in top20]

    fig, ax = plt.subplots(figsize=(12, 6.75), facecolor=BG)
    ax.set_facecolor(BG)

    colors = [BRAND if i == 0 else (GREEN if r["entropy_bits"] >= top20[4]["entropy_bits"] else TEXT_3)
              for i, r in enumerate(top20)]
    bars = ax.barh(range(20, 0, -1), bits, color=colors, height=0.7, zorder=3)

    ax.set_xlim(min(bits) - 0.05, max(bits) + 0.12)
    ax.set_yticks(range(20, 0, -1))
    ax.set_yticklabels(words, fontsize=12, fontweight="600", color=TEXT)
    ax.tick_params(left=False, bottom=False)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_color(BG_3)
    ax.set_xlabel("Shannon entropy (bits of information)", fontsize=11, color=TEXT_2, labelpad=10)
    ax.xaxis.label.set_color(TEXT_2)
    ax.tick_params(axis="x", colors=TEXT_3, labelsize=10)
    ax.grid(axis="x", color=BG_3, linewidth=1, zorder=0)

    for bar, b in zip(bars, reversed(bits)):
        ax.text(b + 0.005, bar.get_y() + bar.get_height() / 2,
                f"{b:.3f}", va="center", fontsize=9, color=TEXT_2)

    ax.set_title("Best Wordle Starting Words by Shannon Entropy",
                 fontsize=15, fontweight="700", color=TEXT, pad=16, loc="left")
    ax.text(0.01, 0.02, "wordineer.com", transform=ax.transAxes,
            fontsize=9, color=TEXT_3, ha="left", va="bottom")

    fig.tight_layout(pad=1.5)
    out = OUT_DIR / "top-20-openers.png"
    fig.savefig(out, dpi=100, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print(f"Wrote {out}")


def chart_guess_distribution():
    data = load_benchmark()
    openers = list(data.keys())
    guess_counts = list(range(1, 7))
    bar_colors   = [BRAND, GREEN, AMBER, BLUE]
    x = range(len(guess_counts))
    width = 0.2

    fig, ax = plt.subplots(figsize=(12, 6.75), facecolor=BG)
    ax.set_facecolor(BG)

    for oi, (opener, color) in enumerate(zip(openers, bar_colors)):
        dist = data[opener]["distribution"]
        counts = [dist.get(g, 0) for g in guess_counts]
        offset = (oi - len(openers) / 2 + 0.5) * width
        bars = ax.bar([xi + offset for xi in x], counts, width=width * 0.85,
                      color=color, label=opener, zorder=3, alpha=0.9)

    ax.set_xticks(list(x))
    ax.set_xticklabels([f"{g}" for g in guess_counts], fontsize=11, color=TEXT)
    ax.set_xlabel("Number of guesses to solve", fontsize=11, color=TEXT_2, labelpad=10)
    ax.set_ylabel("Games (out of 10,000)", fontsize=11, color=TEXT_2, labelpad=10)
    ax.tick_params(left=False, bottom=False)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_color(BG_3)
    ax.tick_params(axis="y", colors=TEXT_3, labelsize=10)
    ax.tick_params(axis="x", colors=TEXT_2, labelsize=11)
    ax.grid(axis="y", color=BG_3, linewidth=1, zorder=0)

    legend = ax.legend(fontsize=10, framealpha=0.9, edgecolor=BG_3,
                       facecolor=BG, labelcolor=TEXT_2)

    ax.set_title("Guess Distribution by Opening Word (10,000 simulated games, seed 42)",
                 fontsize=13, fontweight="700", color=TEXT, pad=16, loc="left")
    ax.text(0.99, 0.02, "wordineer.com", transform=ax.transAxes,
            fontsize=9, color=TEXT_3, ha="right", va="bottom")

    fig.tight_layout(pad=1.5)
    out = OUT_DIR / "guess-distribution.png"
    fig.savefig(out, dpi=100, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print(f"Wrote {out}")


def og_card():
    data    = load_benchmark()
    top100  = load_top100()
    top_word = top100[0]["word"]
    sr       = data[top_word]["solve_rate_6"] * 100
    mean     = data[top_word]["mean_guesses"]

    fig, ax = plt.subplots(figsize=(12, 6.3), facecolor=BG)
    ax.set_facecolor(BG)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6.3)
    ax.axis("off")

    # Left color bar
    bar = FancyBboxPatch((0, 0), 0.35, 6.3, boxstyle="square,pad=0", facecolor=BRAND)
    ax.add_patch(bar)

    # Site name
    ax.text(0.6, 5.6, "WORDINEER.COM", fontsize=11, fontweight="700",
            color=BRAND, va="top", ha="left")

    # Wordle tile motif (5 tiles)
    tile_colors = [GREEN, AMBER, GREEN, AMBER, GREEN]
    tile_labels = list(top_word.upper())
    for ti, (ch, tc) in enumerate(zip(tile_labels, tile_colors)):
        rect = FancyBboxPatch((0.6 + ti * 0.75, 4.45), 0.65, 0.7,
                              boxstyle="round,pad=0.05", facecolor=tc, edgecolor="white", linewidth=2)
        ax.add_patch(rect)
        ax.text(0.6 + ti * 0.75 + 0.325, 4.8, ch, fontsize=17, fontweight="700",
                color="white", va="center", ha="center")

    # Headline
    ax.text(0.6, 4.1, "Best Wordle Starting Words",
            fontsize=22, fontweight="700", color=TEXT, va="top", ha="left")
    ax.text(0.6, 3.35, "Ranked by Information Theory",
            fontsize=16, color=TEXT_2, va="top", ha="left")

    # Stat box
    stat_box = FancyBboxPatch((0.6, 1.5), 5.2, 1.4,
                              boxstyle="round,pad=0.1", facecolor=GREEN_LT, edgecolor=GREEN, linewidth=1.5)
    ax.add_patch(stat_box)
    ax.text(1.2, 2.3, f"{sr:.0f}%", fontsize=36, fontweight="700",
            color=GREEN, va="center", ha="left")
    ax.text(2.6, 2.55, "solve rate within 6 guesses", fontsize=11, color=TEXT_2,
            va="center", ha="left")
    ax.text(2.6, 2.1, f"avg {mean:.2f} guesses · 10,000 simulated games", fontsize=10,
            color=TEXT_3, va="center", ha="left")

    ax.text(0.6, 1.1, f"Top opener: {top_word.upper()}  ·  seed 42  ·  reproducible methodology",
            fontsize=10, color=TEXT_3, va="top", ha="left")

    fig.tight_layout(pad=0)
    out = OUT_DIR / "og-wordle-helper.png"
    fig.savefig(out, dpi=100, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print(f"Wrote {out}")


if __name__ == "__main__":
    chart_top20()
    chart_guess_distribution()
    og_card()
    print("All charts generated.")

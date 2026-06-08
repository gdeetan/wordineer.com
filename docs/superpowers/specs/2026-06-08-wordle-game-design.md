# Wordle Game — Design Spec
**Date:** 2026-06-08  
**Status:** Approved

---

## Overview

Add a playable Wordle game to Wordineer at `/wordle-game/`. The game connects to the existing random Wordle word generator via a "Play" icon on each word. Users can also reach the game directly for solo play. Challenge links (shareable URLs with a base64-encoded secret word) let users send a custom puzzle to a friend.

---

## Architecture

### Files changed / created

| File | Action |
|---|---|
| `template-deploy/tools-src/wordle-game.html` | **New** — full game page |
| `template-deploy/tools-src/random-wordle-generator.html` | **Edit** — add Play icon + tooltip to each word item |
| `template-deploy/tools.json` | **Edit** — add game to word-tools landing page under "Word games" section only |
| `wordineer-deploy/_redirects` | **Edit** — add `/wordle-game/` clean URL rewrite |
| `wordineer-deploy/sitemap.xml` | **Edit** — add `/wordle-game/` entry |

**No new data files.** Game reuses `/data/wordle-words.json` (already used by the generator).  
**No new dependencies.** Pure HTML/CSS/JS, same IIFE script pattern as all other tool pages.

---

## Generator Page Changes (`random-wordle-generator.html`)

### Play icon button

- Add a play icon button (`▶`) to the `word-right` div of each word item, after the existing copy button
- Styled as `.icon-btn` — same size and style as heart and copy buttons
- On click: encodes the word with `btoa()` and navigates to `/wordle-game/#<base64>`
- On hover: CSS tooltip appears above the button reading **"Play Wordle with [WORD]"**
- `aria-label`: `"Play Wordle with [WORD]"`
- On mobile (no hover): icon only, no tooltip — tap navigates directly

### Tooltip implementation

CSS-only tooltip via `::before` / `::after` pseudo-elements on the button. No JS needed. Tooltip appears on `:hover` and `:focus-visible`.

---

## Game Page (`/wordle-game/`)

### URL scheme

| Mode | URL | Behavior |
|---|---|---|
| Challenge | `/wordle-game/#Q1JBTkU=` | Decode hash → use as secret word |
| Solo | `/wordle-game/` | Pick random word from dataset at selected difficulty |

**Hash decoding:** `atob(location.hash.slice(1))` → uppercase → validate as real 5-letter word in dataset. If invalid/absent → fall back to random word silently.

**Hash is never sent to the server** — Cloudflare Pages never sees the secret word.

### Page layout (top to bottom)

```
HEADER
  Title: "Play Wordle"
  [Difficulty: Easy▾]  (solo mode only — hidden in challenge mode)
  [Share link]  (copies current URL with encoded word to clipboard)
  Challenge banner: "Someone challenged you — guess the 5-letter word!" (challenge mode only)

GRID
  6 rows × 5 tiles
  Active row accepts keyboard + on-screen keyboard input
  Submitted rows show green/yellow/grey
  Unplayed rows: empty outlined tiles

KEYBOARD
  Row 1: Q W E R T Y U I O P
  Row 2: A S D F G H J K L
  Row 3: [Enter] Z X C V B N M [⌫]
  Keys color up as letters are used (grey/yellow/green)

WIN/LOSE BANNER (shown after game ends, above keyboard)
  Win:  "Got it in 3! 🎉"
  Lose: "The word was CRANE."
  Buttons: [Play again]  [Share this puzzle]
```

### Difficulty selector (solo mode)

Dropdown in the header: **Any / Easy / Medium / Hard**. Changing difficulty + clicking "New word" (or "Play again" after a game) resets the board with a fresh word at that difficulty. Hidden when playing a challenge link.

### Share button behavior

- **Challenge mode:** copies current URL (already contains the hash)
- **Solo mode:** encodes the current secret word into a hash, copies that URL — so you can share the exact puzzle you just played
- Button label: "Share" → "Copied! ✓" for 1.5s after click

---

## Game Logic

### Guess validation

1. Must be exactly 5 letters
2. Must exist in `wordle-words.json`
3. If invalid: row shakes (CSS animation), no submission, input stays

### Color feedback algorithm

Applied per row after submission, left to right:

1. **Green** — letter matches secret word at this exact position
2. **Yellow** — letter is in the secret word but at a different position (only if not already consumed by a green match)
3. **Grey** — letter is not in the secret word (or all instances already accounted for)

Duplicate letter rule: if the secret has one `E` and the guess has two `E`s, at most one gets green or yellow — the other goes grey.

### Keyboard state

Each key tracks its **best** color earned across all submitted rows. Green never downgrades to yellow. Updated after each row submission.

### Win condition

All 5 tiles in a submitted row are green → game over, win banner shown.

### Lose condition

6 rows submitted without a win → game over, secret word revealed in lose banner.

### Tile flip animation

CSS `transform: rotateX(90deg)` flip, staggered left-to-right at ~80ms per tile, triggered on row submission. Color applied at the midpoint of the flip (when tile is edge-on).

---

## Nav / Tools.json Integration

- **Word Tools landing page (`/word-tools/`):** Add game card under the existing "Word games" section only
- **Mega-menu:** not added
- **Footer:** not added
- **More-tools grids on other pages:** not added

Card copy:
- **Title:** Play Wordle
- **Description:** Guess a random 5-letter word in 6 tries — or challenge a friend with your own word.

---

## Redirects & Sitemap

**`_redirects`:**
```
/wordle-game/   /wordle-game.html   200
```

**`sitemap.xml`:** Add entry for `https://wordineer.com/wordle-game/` with standard priority.

---

## SEO

- `<title>`: "Play Wordle Free — Unlimited Wordle Game | Wordineer"
- Meta description: "Play unlimited Wordle rounds for free. Guess any random 5-letter word in 6 tries, or challenge a friend with a custom word. No sign-up needed."
- JSON-LD: `WebApplication` schema, same pattern as other tool pages
- Breadcrumb: Wordineer → Word Tools → Play Wordle

---

## Build & Deploy Steps

1. Edit `tools-src/random-wordle-generator.html` — add play icon + tooltip
2. Create `tools-src/wordle-game.html`
3. Edit `tools.json` — add to word-tools "Word games" section
4. Run `cd template-deploy && python3 build.py`
5. Copy output: `cp template-deploy/output/*.html wordineer-deploy/`
6. Edit `wordineer-deploy/_redirects`
7. Edit `wordineer-deploy/sitemap.xml`
8. Preview locally: `cd wordineer-deploy && python3 -m http.server 8080`
9. Verify: generator Play button → game, solo play, share link, challenge link
10. Push → Cloudflare deploys

# Free Password Generator — Design Spec

**Date:** 2026-06-12
**URL:** `/password-generator/`
**Output file:** `password-generator.html`
**Type:** `tool` (full layout with nav/grids/ads/footer)

---

## Context

Adding a new "Free Password Generator" tool. It is already stubbed as "Coming soon" in `account-tools.html` (lines 160–164) and registered with `"status": "planned"` in `tools.json`. This spec covers the tool UI, copy, breadcrumbs, sitemap, and redirects needed to ship it.

---

## Feature Set

| Feature | Notes |
|---|---|
| Length slider (8–64) | Default: 16 |
| Uppercase toggle | Default: on |
| Lowercase toggle | Default: on |
| Numbers toggle | Default: on |
| Symbols toggle (`!@#$%^&*`) | Default: on |
| Exclude ambiguous chars (0, O, l, 1, I) | Default: off |
| Copy to clipboard | With toast feedback |
| Regenerate button | + Enter/Space keyboard shortcut |
| Password strength meter | Color bar + label + crack-time estimate |
| Password history | Last 5 passwords, each copyable |
| Privacy badge | "Generated in your browser — never transmitted" |

**Skipped:** memorable/pronounceable (separate planned tool), bulk generation, app integration, download-as-file.

**Randomness source:** `window.crypto.getRandomValues()` — not `Math.random()`.

---

## UI Layout & Style

Split-panel layout. **Style must match `random-word-generator.html` exactly** — reuse its CSS class names and values, do not invent divergent styles:

- `.tool-wrap` → `max-width:960px; margin:0 auto; padding:24px 24px 0`
- `.ctrl` → `width:220px; flex-shrink:0; padding:18px; border-right:1px solid var(--border-2); background:var(--bg-2)`
- `.ctrl-label` → `font-size:10px; font-weight:600; text-transform:uppercase; letter-spacing:.06em`
- `.gen-btn` → same brand-color button style
- `.toggle` / `.toggle-sl` → same pill toggle pattern
- `.word-text` equivalent for password display → `font-size:20px; font-weight:500; letter-spacing:-.02em` (but `font-family:monospace` for password output)
- `.act-btn` → same for Copy / Regenerate buttons
- `.kbd` / `kbd` → same keyboard shortcut hint style

```
┌─────────────────────────────────────────────────────────────┐
│  CTRL PANEL (220px)        │  OUTPUT PANEL                  │
│                            │                                 │
│  Length  [──●───────] 16   │  ┌─────────────────────────┐   │
│                            │  │  Kx9#mQ2!vR@nZpL         │   │
│  [✓] Uppercase             │  │  (monospace, 20px)       │   │
│  [✓] Lowercase             │  └─────────────────────────┘   │
│  [✓] Numbers               │                                 │
│  [✓] Symbols               │  Strength: ████████░░  Strong  │
│  [ ] No ambiguous          │  Est. crack time: centuries     │
│                            │                                 │
│  [Generate Password]       │  [⧉ Copy]  [↻ Regenerate]     │
│                            │                                 │
│  Enter or Space to refresh │  ─ History ─────────────────   │
│                            │  Tz7$kPm1   [copy]             │
│                            │  #vQ9xWn2   [copy]             │
└─────────────────────────────────────────────────────────────┘
```

**Strength scoring (no library):**
- +1 for length ≥ 12 / ≥ 16 / ≥ 20
- +1 each for uppercase, lowercase, numbers, symbols present
- −1 if only one character class
- 0–1 = Weak, 2 = Fair, 3 = Good, 4 = Strong, 5+ = Very Strong
- Crack-time labels: seconds → minutes → hours-days → years → centuries → millions of years

---

## Breadcrumbs

Two-level (Wordineer › Account Tools › Free Password Generator):

```html
<div class="breadcrumb">
  <div class="breadcrumb-inner">
    <a href="/">Wordineer</a>
    <span class="breadcrumb-sep">›</span>
    <a href="/account-tools/">Account Tools</a>
    <span class="breadcrumb-sep">›</span>
    <span aria-current="page">Free Password Generator</span>
  </div>
</div>
```

JSON-LD BreadcrumbList has 3 items: Wordineer → Account Tools → Free Password Generator.

---

## Copy Outline (1,050+ words)

**Page title:** `Free Password Generator — Strong, Secure Passwords | Wordineer`

**H1:** `Free Password Generator`

**Hero subhead:** `Generate a strong, random password in one click. Set your rules, copy, done.`

**Explainer sections:**
1. What Is a Free Password Generator? (~150 words)
2. Why Use a Strong Password Generator Free of Charge? (~200 words) — covers human bias, credential stuffing
3. How It Works (~100 words) — explains `crypto.getRandomValues()`, rejection sampling
4. **Cloud-Based vs. Browser-Based Password Generators (~250 words)** — pros/cons table or structured comparison:
   - *Cloud-based tools (LastPass, Bitwarden generator, Norton, etc.)*: Pros — synced history, accessible anywhere, account integration; Cons — password passes through or is logged on a server, requires trust in the provider, account needed, potential for data breach at provider
   - *Browser-based tools (this tool)*: Pros — password never leaves your device, no account, no server, no breach risk at the provider level, works offline; Cons — no synced history, nothing auto-fills, you still need to store the password yourself
   - Conclusion: for generating a password to paste into a manager, browser-based is strictly safer; the right tool depends on how you store credentials afterward
5. How to Manage Passwords (~200 words) — password manager, 2FA, no reuse, HaveIBeenPwned
6. Best Practices for Strong Passwords (~150 words) — length first, all char classes, no personal info

**Keywords integrated:** `free password creator`, `strong password generator free`, `secure password generator free`, `free password maker`

**FAQ (8 questions):**
1. Is this password generator really free?
2. Are the passwords generated here secure?
3. Does this tool store my passwords?
4. How long should my password be?
5. Should I include symbols?
6. What does "exclude ambiguous characters" mean?
7. Can I use one password for multiple accounts?
8. What's the difference between a password and a passphrase? (links to `/passphrase-generator/`)

**Who section:** 5 bullet personas (new account setup, breach response, IT pros, students, password manager migration)

---

## Files to Create / Modify

| Action | File | Detail |
|---|---|---|
| Create | `template-deploy/tools-src/password-generator.html` | Full tool-src with all slots |
| Modify | `template-deploy/tools-src/account-tools.html` | Lines 160–164: div→`<a href="/password-generator/">`, remove soon-badge |
| Modify | `template-deploy/tools.json` | Remove `"status": "planned"` from mega + footer_cols |
| Modify | `template-deploy/sitemap.xml` | Add active entry (priority 0.9, changefreq weekly) |
| Modify | `wordineer-deploy/_redirects` | Add `/password-generator.html → /password-generator/ 301` |

---

## Verification Checklist

- [ ] `/password-generator/` loads; password generates on page load
- [ ] All 5 toggles update password in real time
- [ ] Length slider updates password in real time
- [ ] Enter/Space regenerates
- [ ] Copy toast appears and works
- [ ] Strength bar + crack-time update with settings changes
- [ ] History shows last 5; each row's copy button works
- [ ] Breadcrumbs render; both links navigate correctly
- [ ] account-tools.html: card is now an `<a>` tag, no "Coming soon" badge
- [ ] `/password-generator.html` 301 redirects to `/password-generator/`

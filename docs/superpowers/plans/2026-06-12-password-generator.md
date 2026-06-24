# Free Password Generator Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and ship the `/password-generator/` tool on Wordineer — a fully client-side password generator with strength metering, copy history, and 1,050+ words of SEO copy.

**Architecture:** Single `template-deploy/tools-src/password-generator.html` assembled by `build.py` using CONFIG+SLOT syntax. All password generation runs via `crypto.getRandomValues()` in the browser — zero network requests, no backend. UI follows the split-panel pattern of `random-word-generator.html` exactly (same CSS class names, same font sizes, same 960px/220px dimensions).

**Tech Stack:** Vanilla HTML/CSS/JS · Python `build.py` assembler · Cloudflare Pages static hosting

---

## File Map

| Action | File |
|---|---|
| **Create** | `template-deploy/tools-src/password-generator.html` |
| **Modify** | `template-deploy/tools-src/account-tools.html` (line 160) |
| **Modify** | `template-deploy/tools.json` (2 entries) |
| **Modify** | `template-deploy/sitemap.xml` |
| **Modify** | `wordineer-deploy/_redirects` |
| **Build output** | `template-deploy/output/password-generator.html` → `wordineer-deploy/password-generator.html` |

---

## Task 1 — Create tool-src scaffold (CONFIG + meta + style + hero)

**Files:**
- Create: `template-deploy/tools-src/password-generator.html`

- [ ] **Step 1: Create the file with CONFIG, meta, style, and hero slots**

```html
<!-- CONFIG
{
  "url": "/password-generator/",
  "output": "password-generator.html",
  "type": "tool",
  "more_tools_key": "more_word_tools",
  "more_tools_subtitle": "More free word and generator tools"
}
-->

<!-- SLOT:meta -->
<title>Free Password Generator — Strong, Secure Passwords | Wordineer</title>
<meta name="description" content="Create strong, random passwords instantly with this free password generator. Set length, character types, and complexity — everything runs in your browser with no sign-up required.">
<link rel="canonical" href="https://wordineer.com/password-generator/">
<meta property="og:type"        content="website">
<meta property="og:site_name"   content="Wordineer">
<meta property="og:title"       content="Free Password Generator | Wordineer">
<meta property="og:description" content="Generate a strong, random password in one click. Set length, character types, and complexity. Runs in your browser — nothing is transmitted to any server.">
<meta property="og:url"         content="https://wordineer.com/password-generator/">
<meta property="og:image"       content="https://wordineer.com/og-image.png">
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Is this password generator really free?",
      "acceptedAnswer": { "@type": "Answer", "text": "Yes. There is no cost, no account, no sign-up, and no premium tier. This is a free password creator in the strictest sense — open the page, generate passwords, close the page. Nothing is gated." }
    },
    {
      "@type": "Question",
      "name": "Are the passwords generated here secure?",
      "acceptedAnswer": { "@type": "Answer", "text": "Yes. The tool uses crypto.getRandomValues(), the browser's cryptographically secure random number generator. This is the same API used for TLS session keys in HTTPS. It is not predictable, even if an attacker knows exactly when you generated your password." }
    },
    {
      "@type": "Question",
      "name": "Does this tool store my passwords?",
      "acceptedAnswer": { "@type": "Answer", "text": "No. Nothing is transmitted to any server. The password history shown on the page lives only in memory — it disappears when you close or reload the tab. There is no database, no log file, and no analytics tracking the passwords generated here." }
    },
    {
      "@type": "Question",
      "name": "How long should my password be?",
      "acceptedAnswer": { "@type": "Answer", "text": "For most accounts, 16 characters is a strong baseline. For critical accounts — your email, banking, and especially your password manager master password — use 20 characters or more. Length has the largest single impact on crack time." }
    },
    {
      "@type": "Question",
      "name": "Should I include symbols?",
      "acceptedAnswer": { "@type": "Answer", "text": "Yes, if the site allows them. Symbols expand the character pool from about 62 characters (letters plus numbers) to about 95, which dramatically increases the number of possible combinations. Some systems restrict which symbols are allowed — if a site rejects your generated password, turn off symbols or regenerate." }
    },
    {
      "@type": "Question",
      "name": "What does 'exclude ambiguous characters' mean?",
      "acceptedAnswer": { "@type": "Answer", "text": "Characters like 0 (zero), O (capital O), l (lowercase L), 1 (one), and I (capital i) look nearly identical in many fonts. Excluding them makes it easier to manually type a password when copy-paste is not an option — for example, entering a Wi-Fi password on a TV." }
    },
    {
      "@type": "Question",
      "name": "Can I use one password for multiple accounts?",
      "acceptedAnswer": { "@type": "Answer", "text": "No. Password reuse is one of the most common causes of account takeover. When a site is breached and your credentials are leaked, attackers immediately try them on other major sites (called credential stuffing). Using a unique password on every account limits any breach to the single compromised site." }
    },
    {
      "@type": "Question",
      "name": "What is the difference between a password and a passphrase?",
      "acceptedAnswer": { "@type": "Answer", "text": "A traditional password is a random mix of characters. A passphrase is a sequence of random words. Passphrases are easier to remember but typically need to be longer to achieve the same entropy. For accounts where you need to type the credential manually, a passphrase generator may be more practical." }
    }
  ]
}
</script>
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "WebApplication",
  "name": "Free Password Generator",
  "url": "https://wordineer.com/password-generator/",
  "description": "Generate strong, random passwords instantly. Set length, character types, and complexity. Runs entirely in your browser — no sign-up required.",
  "applicationCategory": "SecurityApplication",
  "operatingSystem": "Web",
  "offers": { "@type": "Offer", "price": "0", "priceCurrency": "USD" },
  "publisher": { "@id": "https://wordineer.com/#organization" }
}
</script>
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    { "@type": "ListItem", "position": 1, "name": "Wordineer", "item": "https://wordineer.com/" },
    { "@type": "ListItem", "position": 2, "name": "Account Tools", "item": "https://wordineer.com/account-tools/" },
    { "@type": "ListItem", "position": 3, "name": "Free Password Generator", "item": "https://wordineer.com/password-generator/" }
  ]
}
</script>
<!-- /SLOT:meta -->

<!-- SLOT:style -->
<style>
/* ── Layout — matches random-word-generator exactly ── */
.tool-wrap  { max-width:960px; margin:0 auto; padding:24px 24px 0; }
.tool-card  { border:1px solid var(--border); border-radius:var(--radius-lg); overflow:hidden; background:var(--bg); box-shadow:var(--shadow); }
.tool-split { display:flex; }

/* Controls panel */
.ctrl       { width:220px; flex-shrink:0; padding:18px; border-right:1px solid var(--border-2); background:var(--bg-2); }
.ctrl-row   { margin-bottom:14px; }
.ctrl-label { font-size:10px; font-weight:600; color:var(--text-3); text-transform:uppercase; letter-spacing:.06em; display:block; margin-bottom:5px; }
.def-row    { display:flex; align-items:center; gap:8px; margin-bottom:10px; }
.def-lbl    { font-size:12px; color:var(--text-2); cursor:pointer; line-height:1.4; }
.toggle     { position:relative; width:32px; height:18px; flex-shrink:0; }
.toggle input { opacity:0; width:0; height:0; }
.toggle-sl  { position:absolute; cursor:pointer; inset:0; background:var(--border); border-radius:9px; transition:.2s; }
.toggle input:checked + .toggle-sl { background:var(--brand); }
.toggle-sl::before { content:''; position:absolute; width:14px; height:14px; left:2px; top:2px; background:white; border-radius:50%; transition:.2s; }
.toggle input:checked + .toggle-sl::before { transform:translateX(14px); }
.gen-btn    { width:100%; padding:10px 14px; background:var(--brand); color:white; border:none; border-radius:8px; font-size:14px; font-weight:600; font-family:inherit; cursor:pointer; transition:background .15s,transform .1s; letter-spacing:-.01em; }
.gen-btn:hover { background:var(--brand-dark); }
.gen-btn:active { transform:scale(.98); }
.kbd        { text-align:center; font-size:10px; color:var(--text-3); margin-top:6px; }
.kbd kbd    { background:var(--bg-3); border:1px solid var(--border); border-radius:3px; padding:1px 5px; font-size:10px; font-family:inherit; }

/* Length slider */
.range-row  { display:flex; align-items:center; gap:8px; }
.range-row input[type="range"] { flex:1; accent-color:var(--brand); cursor:pointer; }
.range-val  { font-size:13px; font-weight:700; color:var(--text); min-width:22px; text-align:right; }

/* Output panel */
.words-panel { flex:1; display:flex; flex-direction:column; overflow:hidden; min-height:360px; }
.words-top   { display:flex; align-items:center; justify-content:space-between; padding:10px 16px; border-bottom:1px solid var(--border-2); }
.words-count { font-size:12px; color:var(--text-3); font-weight:600; }
.act-btn     { font-size:12px; padding:5px 11px; border:1px solid var(--border); border-radius:6px; background:var(--bg); color:var(--text-2); cursor:pointer; font-family:inherit; transition:background .12s; }
.act-btn:hover { background:var(--bg-2); }
.word-list   { flex:1; overflow-y:auto; list-style:none; padding:0 16px; margin:0; }
.word-item   { display:flex; align-items:center; justify-content:space-between; padding:9px 0; border-bottom:1px solid var(--border-2); gap:10px; animation:fadeIn .2s ease; }
.word-item:last-child { border-bottom:none; }
@keyframes fadeIn { from{opacity:0;transform:translateY(4px)} to{opacity:1;transform:none} }

/* Password-specific additions */
.pw-output-wrap { padding:20px 18px 16px; border-bottom:1px solid var(--border-2); }
.pw-output      { font-size:20px; font-weight:500; letter-spacing:-.02em; color:var(--text); font-family:monospace; word-break:break-all; min-height:28px; line-height:1.35; }
.pw-strength    { padding:10px 16px 12px; border-bottom:1px solid var(--border-2); }
.pw-str-track   { height:4px; background:var(--border-2); border-radius:2px; margin-bottom:6px; overflow:hidden; }
.pw-str-fill    { height:100%; border-radius:2px; transition:width .3s,background .3s; width:0; background:var(--border-2); }
.pw-str-info    { display:flex; align-items:center; gap:8px; flex-wrap:wrap; }
.pw-str-label   { font-size:12px; font-weight:700; color:var(--text); }
.pw-crack-time  { font-size:11px; color:var(--text-3); }
.pw-actions     { display:flex; gap:8px; padding:10px 16px; border-bottom:1px solid var(--border-2); }
.pw-privacy     { display:flex; align-items:center; gap:5px; padding:7px 16px; font-size:11px; color:var(--text-3); border-bottom:1px solid var(--border-2); background:var(--bg-2); }
.pw-privacy svg { flex-shrink:0; }
.pw-hist-text   { font-family:monospace; font-size:13px; font-weight:500; letter-spacing:-.01em; color:var(--text); flex:1; min-width:0; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }
.pw-toast       { position:fixed; bottom:24px; left:50%; transform:translateX(-50%) translateY(10px); background:#1a1a1a; color:white; font-size:13px; font-weight:600; padding:10px 18px; border-radius:8px; opacity:0; transition:opacity .2s,transform .2s; pointer-events:none; z-index:999; }
.pw-toast.show  { opacity:1; transform:translateX(-50%) translateY(0); }
</style>
<!-- /SLOT:style -->

<!-- SLOT:hero -->
<div class="breadcrumb">
  <div class="breadcrumb-inner">
    <a href="/">Wordineer</a>
    <span class="breadcrumb-sep">›</span>
    <a href="/account-tools/">Account Tools</a>
    <span class="breadcrumb-sep">›</span>
    <span aria-current="page">Free Password Generator</span>
  </div>
</div>
<div class="hero">
  <div class="hero-badge">
    <svg viewBox="0 0 11 11" fill="none"><circle cx="5.5" cy="5.5" r="4.5" stroke="#3C3489" stroke-width="1"/><path d="M3.5 5.5l1.5 1.5L8 3.5" stroke="#3C3489" stroke-width="1.2" stroke-linecap="round"/></svg>
    Free · No sign-up · Instant
  </div>
  <h1>Free Password Generator</h1>
  <p>Generate a strong, random password in one click. Set your length and character rules — everything runs in your browser and is never transmitted anywhere.</p>
</div>
<!-- /SLOT:hero -->
```

- [ ] **Step 2: Verify the file exists**

```bash
ls -lh /path/to/template-deploy/tools-src/password-generator.html
```
Expected: file present, non-zero size.

---

## Task 2 — Add tool slot (UI HTML)

**Files:**
- Modify: `template-deploy/tools-src/password-generator.html` (append after hero slot)

- [ ] **Step 1: Append the tool slot to the file**

```html
<!-- SLOT:tool -->
<div class="tool-wrap">
  <div class="tool-card">
    <div class="tool-split">

      <!-- Left: Controls -->
      <div class="ctrl">
        <div class="ctrl-row">
          <span class="ctrl-label">Length: <span id="pw-length-val" style="text-transform:none;letter-spacing:0;color:var(--text)">16</span></span>
          <div class="range-row">
            <input type="range" id="pw-length" min="8" max="64" value="16" aria-label="Password length">
          </div>
        </div>

        <div class="def-row">
          <label class="toggle"><input type="checkbox" id="pw-upper" checked><span class="toggle-sl"></span></label>
          <label class="def-lbl" for="pw-upper">Uppercase (A–Z)</label>
        </div>
        <div class="def-row">
          <label class="toggle"><input type="checkbox" id="pw-lower" checked><span class="toggle-sl"></span></label>
          <label class="def-lbl" for="pw-lower">Lowercase (a–z)</label>
        </div>
        <div class="def-row">
          <label class="toggle"><input type="checkbox" id="pw-nums" checked><span class="toggle-sl"></span></label>
          <label class="def-lbl" for="pw-nums">Numbers (0–9)</label>
        </div>
        <div class="def-row">
          <label class="toggle"><input type="checkbox" id="pw-syms" checked><span class="toggle-sl"></span></label>
          <label class="def-lbl" for="pw-syms">Symbols (!@#$…)</label>
        </div>
        <div class="def-row" style="margin-bottom:20px">
          <label class="toggle"><input type="checkbox" id="pw-noambig"><span class="toggle-sl"></span></label>
          <label class="def-lbl" for="pw-noambig">Exclude ambiguous (0, O, l, 1, I)</label>
        </div>

        <button class="gen-btn" id="pw-gen-btn">Generate Password</button>
        <p class="kbd">Press <kbd>Enter</kbd> or <kbd>Space</kbd> to refresh</p>
      </div>

      <!-- Right: Output -->
      <div class="words-panel">
        <div class="pw-output-wrap">
          <div class="pw-output" id="pw-output" aria-live="polite" aria-label="Generated password"></div>
        </div>

        <div class="pw-strength">
          <div class="pw-str-track">
            <div class="pw-str-fill" id="pw-str-fill"></div>
          </div>
          <div class="pw-str-info">
            <span class="pw-str-label" id="pw-str-label">—</span>
            <span class="pw-crack-time" id="pw-crack-time"></span>
          </div>
        </div>

        <div class="pw-actions">
          <button class="act-btn" id="pw-copy-btn">⧉ Copy</button>
          <button class="act-btn" id="pw-regen-btn">↻ Regenerate</button>
        </div>

        <div class="pw-privacy">
          <svg viewBox="0 0 13 13" fill="none" width="12" height="12"><path d="M6.5 1.5L2 3.5v3c0 2.5 1.9 4.8 4.5 5.5C9.1 11.3 11 9 11 6.5v-3L6.5 1.5z" stroke="currentColor" stroke-width="1.1" stroke-linejoin="round"/></svg>
          Generated in your browser — never transmitted to any server
        </div>

        <div class="words-top">
          <span class="words-count">Recent passwords</span>
        </div>
        <ul class="word-list" id="pw-hist-list"></ul>
      </div>

    </div>
  </div>
</div>
<div class="pw-toast" id="pw-toast">Copied!</div>
<!-- /SLOT:tool -->

<!-- SLOT:ad_b --><!-- /SLOT:ad_b -->
```

---

## Task 3 — Add init slot (JavaScript)

**Files:**
- Modify: `template-deploy/tools-src/password-generator.html` (append after ad_b slot)

- [ ] **Step 1: Append the init slot**

```html
<!-- SLOT:init -->
<script>
(function () {
  var UC   = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
  var LC   = 'abcdefghijklmnopqrstuvwxyz';
  var NU   = '0123456789';
  var SY   = '!@#$%^&*()-_=+[]{}|;:,.<>?';
  var AMBIG = /[0Ol1I]/g;

  function buildPool(u, l, n, s, noA) {
    var p = (u ? UC : '') + (l ? LC : '') + (n ? NU : '') + (s ? SY : '');
    return noA ? p.replace(AMBIG, '') : p;
  }

  function generate(len, pool) {
    if (!pool) return '';
    var result = '';
    while (result.length < len) {
      var buf = new Uint8Array(Math.ceil((len - result.length) * 2));
      crypto.getRandomValues(buf);
      var cap = Math.floor(256 / pool.length) * pool.length;
      for (var i = 0; i < buf.length && result.length < len; i++) {
        if (buf[i] < cap) result += pool[buf[i] % pool.length];
      }
    }
    return result;
  }

  var LABELS  = ['Weak', 'Weak', 'Fair', 'Good', 'Strong', 'Very Strong'];
  var COLORS  = ['#E24B4A', '#E24B4A', '#F59E0B', '#10B981', '#3C3489', '#1a1080'];
  var CRACKS  = ['< 1 second', '< 1 minute', 'Hours to days', 'Years', 'Centuries', 'Millions of years'];
  var WIDTHS  = ['10%', '20%', '40%', '60%', '80%', '100%'];

  function scorePassword(pw) {
    var s = 0;
    if (pw.length >= 12) s++;
    if (pw.length >= 16) s++;
    if (pw.length >= 20) s++;
    if (/[A-Z]/.test(pw)) s++;
    if (/[a-z]/.test(pw)) s++;
    if (/[0-9]/.test(pw)) s++;
    if (/[^A-Za-z0-9]/.test(pw)) s++;
    var classes = [/[A-Z]/.test(pw), /[a-z]/.test(pw), /[0-9]/.test(pw), /[^A-Za-z0-9]/.test(pw)].filter(Boolean).length;
    if (classes <= 1) s -= 2;
    return Math.max(0, Math.min(5, s));
  }

  var history = [];

  function escH(s) {
    return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  function renderHistory() {
    var list = document.getElementById('pw-hist-list');
    list.innerHTML = '';
    history.forEach(function (p) {
      var li = document.createElement('li');
      li.className = 'word-item';
      li.innerHTML = '<span class="pw-hist-text">' + escH(p) + '</span>'
        + '<button class="act-btn" style="flex-shrink:0" data-pw="' + escH(p) + '">Copy</button>';
      list.appendChild(li);
    });
  }

  function fallbackCopy(text) {
    var ta = document.createElement('textarea');
    ta.value = text;
    ta.style.cssText = 'position:fixed;opacity:0;pointer-events:none';
    document.body.appendChild(ta);
    ta.focus();
    ta.select();
    try { document.execCommand('copy'); } catch (e) {}
    document.body.removeChild(ta);
  }

  function copyText(text) {
    var toast = document.getElementById('pw-toast');
    function showToast() {
      toast.classList.add('show');
      setTimeout(function () { toast.classList.remove('show'); }, 1800);
    }
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(showToast).catch(function () {
        fallbackCopy(text);
        showToast();
      });
    } else {
      fallbackCopy(text);
      showToast();
    }
  }

  function render() {
    var len   = parseInt(document.getElementById('pw-length').value, 10);
    var upper = document.getElementById('pw-upper').checked;
    var lower = document.getElementById('pw-lower').checked;
    var nums  = document.getElementById('pw-nums').checked;
    var syms  = document.getElementById('pw-syms').checked;
    var noAmb = document.getElementById('pw-noambig').checked;
    var pool  = buildPool(upper, lower, nums, syms, noAmb);
    var pw    = pool ? generate(len, pool) : '';

    var out = document.getElementById('pw-output');
    out.textContent = pw || '— enable at least one option —';

    if (pw) {
      var sc = scorePassword(pw);
      var fill = document.getElementById('pw-str-fill');
      fill.style.width      = WIDTHS[sc];
      fill.style.background = COLORS[sc];
      document.getElementById('pw-str-label').textContent  = LABELS[sc];
      document.getElementById('pw-crack-time').textContent = 'Est. crack time: ' + CRACKS[sc];
      history.unshift(pw);
      if (history.length > 5) history.pop();
      renderHistory();
    }
  }

  document.addEventListener('DOMContentLoaded', function () {
    var slider = document.getElementById('pw-length');
    var valEl  = document.getElementById('pw-length-val');

    slider.addEventListener('input', function () {
      valEl.textContent = slider.value;
      render();
    });

    ['pw-upper', 'pw-lower', 'pw-nums', 'pw-syms', 'pw-noambig'].forEach(function (id) {
      document.getElementById(id).addEventListener('change', render);
    });

    document.getElementById('pw-gen-btn').addEventListener('click', render);
    document.getElementById('pw-regen-btn').addEventListener('click', render);

    document.getElementById('pw-copy-btn').addEventListener('click', function () {
      var pw = document.getElementById('pw-output').textContent;
      if (pw && pw.indexOf('—') === -1) copyText(pw);
    });

    document.getElementById('pw-hist-list').addEventListener('click', function (e) {
      var btn = e.target.closest('[data-pw]');
      if (btn) copyText(btn.dataset.pw);
    });

    document.addEventListener('keydown', function (e) {
      if (e.target !== document.body) return;
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); render(); }
    });

    render();
  });
}());
</script>
<!-- /SLOT:init -->
```

---

## Task 4 — Add explainer, faq, and who slots (copy)

**Files:**
- Modify: `template-deploy/tools-src/password-generator.html` (append after init slot)

- [ ] **Step 1: Append explainer, faq, and who slots**

```html
<!-- SLOT:explainer -->
<div>
  <h2>What is a Free Password Generator?</h2>
  <p>A free password generator is a tool that creates random, complex passwords based on rules you set — length, character types, and special requirements. Instead of trying to invent a password yourself (and falling back on patterns attackers already know), a generator uses cryptographically secure randomness to produce something genuinely unpredictable.</p>
  <p>This tool works entirely inside your browser. Nothing you generate is sent to a server, stored in a database, or logged anywhere. You're using a free password creator that gives you full control without any account, subscription, or software install.</p>

  <h2>Why Use a Strong Password Generator Free of Charge?</h2>
  <p>Most people pick passwords that feel random but aren't. Birthdays, pet names, keyboard walks like <code>qwerty123</code>, and substitutions like <code>p@ssw0rd</code> are the first things brute-force attacks try. A dictionary of the most common password patterns can crack the majority of human-chosen passwords in under an hour.</p>
  <p>A strong password generator free of cost removes the human bias entirely. The generator doesn't know your name, your interests, or your keyboard habits — it only knows entropy. A 16-character password using uppercase, lowercase, numbers, and symbols has roughly 95<sup>16</sup> possible combinations. At a trillion guesses per second, that takes over 3 billion years to exhaust.</p>
  <p>The other reason to use a generator is reuse. People who create their own passwords tend to reuse them or make slight variations (<code>password1</code>, <code>password2</code>). When one site gets breached, attackers run "credential stuffing" attacks against every other site using the same email. A fresh random password on every account makes each breach a contained problem, not a domino effect.</p>

  <h2>Cloud-Based vs. Browser-Based Password Generators</h2>
  <p>Not all free password makers work the same way. The most important distinction is where the generation happens.</p>
  <p><strong>Cloud-based tools</strong> (password manager generators, web services that process your request on a server) have real advantages: your history is synced across devices, the tool can integrate with auto-fill, and the result can go straight into your vault. The trade-off is trust. Your password either passes through a server or is generated there — you're relying on that company's security, their logging practices, and their continued operation. A breach at the provider, a rogue employee, or a compromised API could expose passwords generated there. Most reputable services are trustworthy, but the attack surface exists.</p>
  <p><strong>Browser-based tools like this one</strong> generate everything locally on your device. The code runs in your browser tab, your password never leaves your machine, and there is no provider to breach. The trade-off is that you must manually copy the result into your password manager — there is no sync, no auto-fill, and the history resets when you close the tab.</p>
  <p>For most use cases, the right workflow is: use this secure password generator free tool to generate a strong credential, then paste it into your password manager. You get the security of local generation and the convenience of manager-based storage. Neither tool alone is the complete solution.</p>

  <h2>How It Works</h2>
  <p>This tool uses the Web Cryptography API — specifically <code>window.crypto.getRandomValues()</code> — which is the same cryptographically secure random number source used by your browser for HTTPS connections. It is not <code>Math.random()</code>, which is predictable and unsuitable for security purposes.</p>
  <p>When you click Generate (or press Enter), the tool builds a character pool from your selected options, pulls random bytes from <code>crypto.getRandomValues()</code>, and maps each byte to a character using rejection sampling to eliminate modulo bias. The generation happens in under a millisecond, entirely on your device.</p>

  <h2>How to Manage Passwords</h2>
  <p>Generating a strong password is only half the job. Storing and using it securely matters just as much.</p>
  <p><strong>Use a password manager.</strong> Apps like Bitwarden (free, open-source), 1Password, or the built-in browser password manager let you store a unique, random password for every account without remembering any of them. You remember one strong master password; everything else is generated and filled automatically.</p>
  <p><strong>Enable two-factor authentication (2FA) on critical accounts.</strong> A strong password plus a second factor means an attacker needs both your password and physical access to your second device. For email, banking, and your password manager, 2FA is non-negotiable.</p>
  <p><strong>Never reuse passwords.</strong> If one site gets breached, change it immediately on every site that shares it. HaveIBeenPwned.com lets you check if your email appears in known breach datasets.</p>
  <p><strong>Change passwords when there is a reason.</strong> Contrary to older guidance, changing passwords on a schedule without cause reduces security — people make predictable increments. Change them when a site reports a breach, you suspect unauthorized access, or you're ending a shared login.</p>

  <h2>Best Practices for Strong Passwords</h2>
  <p><strong>Length matters most.</strong> Every additional character multiplies the search space exponentially. A 12-character password is not twice as hard to crack as a 6-character one — it is millions of times harder. Aim for 16 characters or more for sensitive accounts.</p>
  <p><strong>Use all character classes.</strong> Uppercase, lowercase, numbers, and symbols each expand the character pool. A password drawn from 95 possible characters per position is far harder to crack than one drawn from 26.</p>
  <p><strong>Avoid personal information.</strong> Names, birthdays, addresses, and pet names are in publicly available databases attackers use for targeted attacks. Use a free password maker for every new account — the five seconds it takes to generate and save is worth it.</p>
  <p><strong>Beware of security questions.</strong> Many sites offer password recovery via questions like "What was your childhood nickname?" Treat these as passwords — give them random, false answers stored in your password manager.</p>
</div>
<!-- /SLOT:explainer -->

<!-- SLOT:faq -->
<div class="faq">
  <h2 class="faq-title">Frequently asked questions</h2>
  <div class="faq-item open">
    <div class="faq-q"><span class="faq-q-text">Is this password generator really free?</span><svg class="faq-chevron" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div>
    <div class="faq-a">Yes. There is no cost, no account, no sign-up, and no premium tier. This is a free password creator in the strictest sense — open the page, generate passwords, close the page. Nothing is gated.</div>
  </div>
  <div class="faq-item">
    <div class="faq-q"><span class="faq-q-text">Are the passwords generated here secure?</span><svg class="faq-chevron" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div>
    <div class="faq-a">Yes. The tool uses <code>crypto.getRandomValues()</code>, the browser's cryptographically secure random number generator. This is the same API used for TLS session keys in HTTPS. It is not predictable, even if an attacker knows exactly when you generated your password.</div>
  </div>
  <div class="faq-item">
    <div class="faq-q"><span class="faq-q-text">Does this tool store my passwords?</span><svg class="faq-chevron" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div>
    <div class="faq-a">No. Nothing is transmitted to any server. The password history shown on the page lives only in memory — it disappears when you close or reload the tab. There is no database, no log file, and no analytics tracking the passwords generated here.</div>
  </div>
  <div class="faq-item">
    <div class="faq-q"><span class="faq-q-text">How long should my password be?</span><svg class="faq-chevron" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div>
    <div class="faq-a">For most accounts, 16 characters is a strong baseline. For critical accounts — your email, banking, and especially your password manager master password — use 20 characters or more. Length has the largest single impact on crack time.</div>
  </div>
  <div class="faq-item">
    <div class="faq-q"><span class="faq-q-text">Should I include symbols?</span><svg class="faq-chevron" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div>
    <div class="faq-a">Yes, if the site allows them. Symbols expand the character pool from about 62 characters (letters plus numbers) to about 95, which dramatically increases the number of possible combinations. Some systems restrict which symbols are allowed — if a site rejects your generated password, turn off symbols or regenerate.</div>
  </div>
  <div class="faq-item">
    <div class="faq-q"><span class="faq-q-text">What does "exclude ambiguous characters" mean?</span><svg class="faq-chevron" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div>
    <div class="faq-a">Characters like <code>0</code> (zero), <code>O</code> (capital O), <code>l</code> (lowercase L), <code>1</code> (one), and <code>I</code> (capital i) look nearly identical in many fonts. Excluding them makes it easier to manually type a password when copy-paste is not an option — for example, entering a Wi-Fi password on a TV.</div>
  </div>
  <div class="faq-item">
    <div class="faq-q"><span class="faq-q-text">Can I use one password for multiple accounts?</span><svg class="faq-chevron" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div>
    <div class="faq-a">No. Password reuse is one of the most common causes of account takeover. When a site is breached and your credentials are leaked, attackers immediately try them on other major sites — a technique called credential stuffing. Using a unique password on every account limits any breach to the single compromised site.</div>
  </div>
  <div class="faq-item">
    <div class="faq-q"><span class="faq-q-text">What is the difference between a password and a passphrase?</span><svg class="faq-chevron" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div>
    <div class="faq-a">A traditional password is a random mix of characters. A passphrase is a sequence of random words (like <code>correct horse battery staple</code>). Passphrases are easier to remember but typically need to be longer to achieve the same entropy. For accounts where you need to type the credential manually, try our <a href="/passphrase-generator/">Passphrase Generator</a> instead.</div>
  </div>
</div>
<!-- /SLOT:faq -->

<!-- SLOT:who -->
<div>
  <h2 class="section-title" style="margin-bottom:14px">Who uses a free password generator?</h2>
  <div class="uc-grid">
    <div class="uc"><div class="uc-title">New account setup</div><div class="uc-body">People setting up new accounts who want a strong credential without spending time thinking one up</div></div>
    <div class="uc"><div class="uc-title">Breach response</div><div class="uc-body">Anyone who just heard their favourite site got breached and needs fresh, unique passwords fast across multiple accounts</div></div>
    <div class="uc"><div class="uc-title">IT professionals</div><div class="uc-body">Generating credentials for shared systems, service accounts, and temporary access that need to be strong and non-guessable</div></div>
    <div class="uc"><div class="uc-title">Students</div><div class="uc-body">People who've been told to "use a strong password" with no further guidance and need a quick, trustworthy tool</div></div>
    <div class="uc"><div class="uc-title">Password manager migration</div><div class="uc-body">Anyone switching to a password manager who is re-securing old accounts with fresh, randomly generated credentials</div></div>
  </div>
</div>
<!-- /SLOT:who -->
```

---

## Task 5 — Update supporting files

**Files:**
- Modify: `template-deploy/tools-src/account-tools.html`
- Modify: `template-deploy/tools.json`
- Modify: `template-deploy/sitemap.xml`
- Modify: `wordineer-deploy/_redirects`

### 5a — Activate the account-tools.html placeholder

- [ ] **Step 1: In `account-tools.html`, replace the Coming Soon div (lines ~160–164) with an active link**

Find this block:
```html
        <div class="tool-item tool-item--soon">
          <div class="tool-icon" style="background:#EEEDFE"><svg viewBox="0 0 13 13" fill="none"><path d="M4.5 6.5V5a2 2 0 0 1 4 0v1.5" stroke="#5B46D4" stroke-width="1.1" stroke-linecap="round"/><rect x="3" y="6.5" width="7" height="4.5" rx="1" stroke="#5B46D4" stroke-width="1.1"/><circle cx="6.5" cy="8.8" r=".8" fill="#5B46D4"/></svg></div>
          <div class="tool-name">Password Generator <span class="soon-badge">Coming soon</span></div>
          <div class="tool-desc">One click, one strong password. Set your length and character rules.</div>
        </div>
```

Replace with:
```html
        <a class="tool-item" href="/password-generator/">
          <div class="tool-icon" style="background:#EEEDFE"><svg viewBox="0 0 13 13" fill="none"><path d="M4.5 6.5V5a2 2 0 0 1 4 0v1.5" stroke="#5B46D4" stroke-width="1.1" stroke-linecap="round"/><rect x="3" y="6.5" width="7" height="4.5" rx="1" stroke="#5B46D4" stroke-width="1.1"/><circle cx="6.5" cy="8.8" r=".8" fill="#5B46D4"/></svg></div>
          <div class="tool-name">Password Generator</div>
          <div class="tool-desc">One click, one strong password. Set your length and character rules.</div>
        </a>
```

### 5b — Remove `"status": "planned"` from tools.json

- [ ] **Step 1: In `tools.json`, find the two password-generator entries and remove `"status": "planned"` from each**

In the `mega` section, find:
```json
        {
          "href": "/password-generator/",
          "text": "Password Generator",
          "status": "planned"
        },
```
Change to:
```json
        {
          "href": "/password-generator/",
          "text": "Password Generator"
        },
```

In the `footer_cols` section, find the same pattern and make the same change.

### 5c — Add sitemap entry

- [ ] **Step 1: In `sitemap.xml`, add the new entry after the passphrase-generator entry (or any other account-tools entry)**

```xml
  <!-- ✅ ACTIVE — Account Tool / Free Password Generator -->
  <url>
    <loc>https://wordineer.com/password-generator</loc>
    <priority>0.9</priority>
    <changefreq>weekly</changefreq>
  </url>
```

### 5d — Add _redirects entry

- [ ] **Step 1: In `wordineer-deploy/_redirects`, add the clean URL redirect at the end of the "Clean URLs" section**

```
/password-generator.html    /password-generator/    301
```

---

## Task 6 — Build, copy output, and verify

**Files:**
- Run: `template-deploy/build.py`
- Copy: `template-deploy/output/password-generator.html` → `wordineer-deploy/`

- [ ] **Step 1: Build**

```bash
cd "template-deploy" && python3 build.py
```
Expected: no errors, `output/password-generator.html` created.

- [ ] **Step 2: Copy output to deploy folder**

```bash
cp template-deploy/output/password-generator.html wordineer-deploy/password-generator.html
cp template-deploy/output/account-tools.html wordineer-deploy/account-tools.html
```

- [ ] **Step 3: Start local server**

```bash
cd wordineer-deploy && python3 -m http.server 8080
```

- [ ] **Step 4: Verify the tool (open http://localhost:8080/password-generator.html)**

Check each item:
- [ ] Page loads; a password is visible on page load (no click required)
- [ ] All 5 controls update the password in real time (slider + 4 toggles + no-ambiguous)
- [ ] Setting all 4 char-type toggles OFF shows the "— enable at least one option —" message
- [ ] Re-enabling a toggle immediately generates a password again
- [ ] Strength bar and crack-time update with every change
- [ ] Strong config (16 chars, all on) shows "Strong" or "Very Strong"
- [ ] Weak config (8 chars, numbers only) shows "Weak"
- [ ] Copy button fires the "Copied!" toast
- [ ] Regenerate button generates a new password
- [ ] History list shows up to 5 prior passwords; each Copy button works
- [ ] Press Enter and Space on the page body each regenerate the password
- [ ] Breadcrumbs render: `Wordineer › Account Tools › Free Password Generator`
- [ ] "Wordineer" link goes to `/`, "Account Tools" link goes to `/account-tools/`

- [ ] **Step 5: Verify account-tools page (http://localhost:8080/account-tools.html)**

- [ ] Password Generator card is now a clickable `<a>` link to `/password-generator/`
- [ ] "Coming soon" badge is gone

- [ ] **Step 6: Commit all changes**

```bash
git add template-deploy/tools-src/password-generator.html \
        template-deploy/tools-src/account-tools.html \
        template-deploy/tools.json \
        template-deploy/sitemap.xml \
        wordineer-deploy/_redirects \
        wordineer-deploy/password-generator.html \
        wordineer-deploy/account-tools.html
git commit -m "feat: add Free Password Generator tool at /password-generator/"
```

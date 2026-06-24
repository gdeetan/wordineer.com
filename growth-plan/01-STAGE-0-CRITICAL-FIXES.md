# Stage 0 — Critical fixes (THIS WEEK)

These need to happen before anything else. Without them, every other stage under-performs because broken pages drag the whole site down, exposed keys are a security risk, and Google can't properly crawl what you do have.

**Estimated time:** 4–8 hours total.

---

## Fix 1: Stop /number-chance/ category from serving homepage content

**Problem (re-stated):** `/coin-flip/`, `/random-number-generator/`, `/dice-roller/` (and likely every other number-chance URL) currently return the homepage HTML with `<link rel="canonical" href="https://wordineer.com/">`. This tells Google these URLs are duplicates of the homepage.

**Two options — pick one:**

### Option A (recommended): Build the pages properly (Stage 1)

Stage 1 of this plan covers building the whole /number-chance/ cluster. If you start it this week, you can fix the broken URLs and unlock a high-value cluster at the same time. **Recommended path.**

### Option B (temporary): Remove broken URLs from nav and homepage

If you can't start Stage 1 immediately, remove these from your nav and homepage:
- Number Generator
- Flip a Coin
- Dice Roller

And drop their card mentions on the /number-chance/ hub (currently showing as live links that go to homepage content). Leave the hub itself intact but make every card a "Coming soon" placeholder until built.

This is a stop-gap. The right answer is Option A.

---

## Fix 2: Rotate exposed API keys

In your `random-word-generator.html` (and possibly other tool pages that import the same JS init), API keys for Wordnik and Merriam-Webster are visible in client-side source.

**Steps:**

1. **Today:** Log into Wordnik and Merriam-Webster developer dashboards, regenerate keys (this invalidates the old ones).
2. **Today:** Create a Cloudflare Worker (call it `dictionary-proxy`) that:
   - Receives a request from your site with the word to look up
   - Calls Wordnik/Merriam with the secret keys stored as Worker secrets
   - Returns the response
3. **This week:** Update `tool-engine.js` to call your worker endpoint instead of the third-party APIs directly. Remove `apiKeys` from the WORDINEER.init() call. Remove the `apiKeys` parameter from the `<!-- SLOT:init -->` block in every tool page.
4. **This week:** Add a CORS allow-list on the worker so only `wordineer.com` (and your dev environment) can call it.

If you've been running with these keys exposed for a while, also check your dictionary API quotas for unusual usage. If you see suspicious traffic, your keys were being used by someone else.

**Note:** This is not just security hygiene. The Wordnik and Merriam dashboards can suspend your account if exposed keys are reported, and at scale your free-tier quotas could be exhausted by random scrapers.

---

## Fix 3: Google Search Console health check

Open Search Console for wordineer.com. Walk through these checks:

1. **Coverage / Pages report.** Look at "Why pages aren't indexed."
   - If you see many "Duplicate without user-selected canonical" — that's the broken /number-chance/ family. Fixing them (Fix 1) will fix this.
   - If you see "Crawled – currently not indexed" on the spelling bee or letter pages — that's a quality signal Google is throwing back at you. Note which pages and we'll address them in Stage 5.
   - If you see "Discovered – not indexed" — Google found the URL but didn't bother crawling. Often a crawl budget issue on a large site, or a quality signal on small ones.

2. **Performance report.** Check which queries are currently delivering impressions/clicks. This is your starting ranking distribution — note your top 20 queries, you'll want to defend and improve these first.

3. **Sitemaps.** Confirm `sitemap.xml` is submitted. If not, generate one from `tools.json` listing every actual live URL (no "Coming soon" placeholders). Resubmit after Stage 1.

4. **Mobile usability.** Confirm no mobile errors.

5. **Core Web Vitals.** Check the CWV report. Anything in "Poor" or "Needs improvement" on mobile should be fixed before Stage 2.

**Time:** 30 minutes. Do this before any new builds.

---

## Fix 4: Sitemap audit and rebuild

The site has 50+ live pages but I don't know if your sitemap reflects them all. Without a complete sitemap, Google relies entirely on link discovery.

**Steps:**

1. Open `https://wordineer.com/sitemap.xml` in a browser. If it doesn't exist or 404s, that's the first fix.
2. Count entries. Compare to your actual live page count.
3. If missing pages, regenerate from `tools.json`. Your build script should output `sitemap.xml` listing every URL with `<lastmod>` set to the last build date.
4. Submit (or resubmit) via Search Console.

**Bonus:** Add `<lastmod>` updates whenever a page changes. This signals freshness to Google.

---

## Fix 5: Robots.txt sanity check

Open `https://wordineer.com/robots.txt`. Confirm:
- It allows crawling (no `Disallow: /` for `User-agent: *`)
- It references the sitemap: `Sitemap: https://wordineer.com/sitemap.xml`
- It doesn't block any tool directories

If the file doesn't exist or is wrong, fix it. Default for a tool site:

```
User-agent: *
Allow: /
Disallow: /admin/
Disallow: /api/

Sitemap: https://wordineer.com/sitemap.xml
```

---

## Fix 6: Canonical audit (sample 10 pages)

In a browser, view-source on these and confirm each has a self-referencing canonical pointing to its own URL (not the homepage):

- /spelling-bee-words-5th-grade/
- /random-noun-generator/
- /random-5-letter-word-generator/
- /pictionary-word-generator/
- /word-of-the-day/
- /passphrase-generator/
- /random-words-starting-with/a/
- /random-quote-generator/
- /word-tools/
- /name-generators/

If any of these have `<link rel="canonical" href="https://wordineer.com/">` (the homepage), they're broken in the same way as the number-chance category. Fix the template that produced them.

---

## Verification — when Stage 0 is "done"

You can move to Stage 1 once:

- [ ] /number-chance/ URLs either work as proper pages OR are removed from nav/homepage
- [ ] Wordnik and Merriam-Webster keys rotated, behind a Cloudflare Worker, removed from client JS
- [ ] Search Console connected, sitemap submitted, coverage report reviewed
- [ ] sitemap.xml exists and includes every live page (no placeholders)
- [ ] robots.txt allows crawling and references sitemap
- [ ] Sampled 10 pages have self-referencing canonicals

Set a calendar reminder for 7 days from completing this. Re-check Search Console then — many indexing issues take 3–7 days to clear after fixes.

---

## What Stage 0 unlocks

Stage 0 is unglamorous but essential. Skipping it means:
- The broken number-chance category continues to confuse Google about your homepage's topic
- Exposed API keys could cost you money or get accounts suspended
- You can't measure whether new builds are working without Search Console
- Sitemap gaps mean Google may never find some of your best content

After Stage 0, the site is in a state where new builds compound rather than fight uphill.

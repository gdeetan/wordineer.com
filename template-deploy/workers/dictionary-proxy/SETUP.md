# Dictionary Proxy Worker — Setup

This Cloudflare Worker proxies Wordnik and Merriam-Webster API calls so keys never appear in client HTML.

## Prerequisites

- Cloudflare account (free tier is fine)
- Node.js 18+

## Step 1 — Rotate your API keys

Do this FIRST, before anything else. The old keys are now exposed in git history.

1. **Wordnik:** Log in at https://developer.wordnik.com → My Account → regenerate API key
2. **Merriam-Webster:** Log in at https://dictionaryapi.com → My Keys → delete the old key, create a new one (select "Collegiate Dictionary")

## Step 2 — Install Wrangler

```bash
npm install -g wrangler
wrangler login   # opens browser to authorize your Cloudflare account
```

## Step 3 — Deploy the Worker

```bash
cd template-deploy/workers/dictionary-proxy
wrangler deploy
```

Wrangler will print the Worker URL, e.g.:
`https://dictionary-proxy.YOUR-ACCOUNT.workers.dev`

## Step 4 — Set secrets

```bash
wrangler secret put WORDNIK_KEY
# paste your new Wordnik key when prompted

wrangler secret put MERRIAM_KEY
# paste your new Merriam-Webster key when prompted
```

## Step 5 — Wire up the site

In each of these tools-src files, uncomment and update the `dictionaryProxyUrl` line:

- `template-deploy/tools-src/random-word-generator.html`
- `template-deploy/tools-src/random-verb-generator.html`
- `template-deploy/tools-src/random-adjective-generator.html`
- `template-deploy/tools-src/random-adverb-generator.html`
- `template-deploy/tools-src/random-noun-generator.html`

Change:
```js
  // dictionaryProxyUrl: 'https://dictionary-proxy.YOUR-ACCOUNT.workers.dev',
```
To:
```js
  dictionaryProxyUrl: 'https://dictionary-proxy.YOUR-ACCOUNT.workers.dev',
```
(Replace `YOUR-ACCOUNT` with your actual Cloudflare subdomain.)

Then rebuild and redeploy:
```bash
cd template-deploy && python3 build.py
cp output/index.html output/random-*-generator.html ../wordineer-deploy/
git add -A && git commit -m "feat: wire dictionary proxy"
git push
```

## Step 6 — Verify

Open https://wordineer.com and generate some words. Check browser DevTools → Network tab — you should see requests going to `dictionary-proxy.YOUR-ACCOUNT.workers.dev`, not to `api.wordnik.com` or `dictionaryapi.com` directly.

## Notes

- The Worker enforces CORS to `wordineer.com` only. Scrapers using the Worker URL directly will get blocked.
- Wordnik/Merriam free tiers have daily limits. The Worker adds no overhead — it's a pure proxy.
- If the Worker is down, the site degrades gracefully: tools still work with their seed words, just without live dictionary lookups.

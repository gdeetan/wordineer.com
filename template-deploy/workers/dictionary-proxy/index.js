const ALLOWED_ORIGINS = ['https://wordineer.com', 'https://www.wordineer.com'];

export default {
  async fetch(request, env) {
    const origin = request.headers.get('Origin') || '';
    const corsHeaders = {
      'Access-Control-Allow-Origin': ALLOWED_ORIGINS.includes(origin) ? origin : ALLOWED_ORIGINS[0],
      'Access-Control-Allow-Methods': 'GET, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
      'Vary': 'Origin',
    };

    if (request.method === 'OPTIONS') {
      return new Response(null, { status: 204, headers: corsHeaders });
    }

    const url = new URL(request.url);
    const service = url.searchParams.get('service');
    const action  = url.searchParams.get('action');
    const word    = url.searchParams.get('word') || '';
    const pos     = url.searchParams.get('includePartOfSpeech') || '';

    try {
      if (service === 'wordnik' && action === 'randomWords') {
        const posParam = pos ? `&includePartOfSpeech=${encodeURIComponent(pos)}` : '';
        const apiUrl = `https://api.wordnik.com/v4/words.json/randomWords?hasDictionaryDef=true${posParam}&minCorpusCount=5000&limit=20&api_key=${env.WORDNIK_KEY}`;
        const res  = await fetch(apiUrl, { signal: AbortSignal.timeout(5000) });
        const data = await res.json();
        return Response.json(data, { headers: corsHeaders });
      }

      if (service === 'wordnik' && action === 'define' && word) {
        const apiUrl = `https://api.wordnik.com/v4/word.json/${encodeURIComponent(word)}/definitions?limit=3&sourceDictionaries=all&useCanonical=false&api_key=${env.WORDNIK_KEY}`;
        const res  = await fetch(apiUrl, { signal: AbortSignal.timeout(4000) });
        const data = await res.json();
        const entry = data?.[0];
        if (!entry?.text) return Response.json(null, { headers: corsHeaders });
        return Response.json(
          { def: entry.text.replace(/<[^>]+>/g, '').slice(0, 100), pos: entry.partOfSpeech || null },
          { headers: corsHeaders }
        );
      }

      if (service === 'merriam' && action === 'define' && word) {
        const apiUrl = `https://www.dictionaryapi.com/api/v3/references/collegiate/json/${encodeURIComponent(word)}?key=${env.MERRIAM_KEY}`;
        const res  = await fetch(apiUrl, { signal: AbortSignal.timeout(4000) });
        const data = await res.json();
        const entry = data?.[0];
        if (!entry || typeof entry !== 'object' || !entry.shortdef?.length) return Response.json(null, { headers: corsHeaders });
        return Response.json(
          { def: entry.shortdef[0].slice(0, 100), pos: entry.fl || null },
          { headers: corsHeaders }
        );
      }

      return new Response('Bad request', { status: 400, headers: corsHeaders });
    } catch {
      return new Response('Internal error', { status: 500, headers: corsHeaders });
    }
  },
};

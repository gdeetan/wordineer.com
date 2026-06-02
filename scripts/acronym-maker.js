(function(root, factory) {
  if (typeof module === 'object' && module.exports) {
    module.exports = factory();
  } else {
    root.WordineerAcronymMaker = factory();
  }
})(typeof globalThis !== 'undefined' ? globalThis : this, function() {
  const MAX_TARGET_LENGTH = 8;
  const MIN_TARGET_LENGTH = 2;
  const DEFAULT_LIMIT = 10;

  const VOWELS = new Set(['A', 'E', 'I', 'O', 'U', 'Y']);

  const KEYWORD_TAGS = {
    brand: ['brand', 'branding', 'identity', 'positioning', 'marketing', 'launch', 'campaign', 'audience', 'message'],
    growth: ['growth', 'scale', 'expansion', 'revenue', 'momentum', 'business', 'sales'],
    team: ['team', 'staff', 'people', 'culture', 'leadership', 'collaboration', 'workplace'],
    product: ['product', 'service', 'platform', 'tool', 'solution', 'offering'],
    tech: ['tech', 'software', 'digital', 'app', 'data', 'system', 'engineering', 'code', 'automation'],
    community: ['community', 'club', 'volunteer', 'local', 'school', 'members'],
    nonprofit: ['nonprofit', 'mission', 'charity', 'impact', 'donor', 'outreach'],
    environment: ['green', 'sustainable', 'sustainability', 'climate', 'clean', 'recycling', 'environment'],
    health: ['health', 'wellness', 'medical', 'care', 'mental', 'fitness'],
    education: ['education', 'learning', 'student', 'teaching', 'training', 'classroom'],
    finance: ['finance', 'budget', 'investment', 'capital', 'accounting'],
    security: ['security', 'privacy', 'risk', 'safety', 'protection', 'compliance'],
    operations: ['operations', 'workflow', 'process', 'delivery', 'logistics', 'efficiency']
  };

  const WORD_BANK = {
    A: ['Adaptive', 'Aligned', 'Active', 'Agile', 'Authentic', 'Advanced', 'Accessible', 'Accelerated', 'Audience', 'Action'],
    B: ['Bold', 'Brand', 'Bridge', 'Better', 'Business', 'Bright', 'Balanced', 'Build', 'Benefit', 'Blueprint'],
    C: ['Clear', 'Creative', 'Connected', 'Community', 'Care', 'Catalyst', 'Core', 'Collective', 'Craft', 'Code'],
    D: ['Driven', 'Digital', 'Dynamic', 'Direct', 'Design', 'Delivery', 'Development', 'Discovery', 'Data', 'Dependable'],
    E: ['Effective', 'Elevated', 'Essential', 'Engine', 'Enterprise', 'Empower', 'Eco', 'Enable', 'Exchange', 'Everyday'],
    F: ['Focused', 'Future', 'Friendly', 'Forward', 'Flexible', 'Flourish', 'Foundry', 'Framework', 'Fund', 'Force'],
    G: ['Growth', 'Guided', 'Green', 'Global', 'Genuine', 'Grounded', 'Group', 'Generate', 'Goal', 'Gather'],
    H: ['Human', 'Helpful', 'Healthy', 'Horizon', 'Hub', 'Harmony', 'Hands-on', 'High-Impact', 'Holistic', 'Hope'],
    I: ['Impact', 'Insight', 'Inclusive', 'Innovation', 'Intelligent', 'Integrated', 'Initiative', 'Improve', 'Inspire', 'Integrity'],
    J: ['Joint', 'Journey', 'Joyful', 'Just', 'Jumpstart', 'Junction', 'Junior', 'Justice', 'Jewel', 'Jolt'],
    K: ['Key', 'Knowledge', 'Kind', 'Kinetic', 'Keep', 'Kernel', 'Kinship', 'Kickstart', 'Keystone', 'Knack'],
    L: ['Leading', 'Local', 'Launch', 'Learning', 'Lift', 'Link', 'Logic', 'Lasting', 'Lively', 'Lab'],
    M: ['Modern', 'Mission', 'Momentum', 'Market', 'Meaningful', 'Maker', 'Movement', 'Method', 'Member', 'Managed'],
    N: ['Next', 'Network', 'Natural', 'New', 'Nimble', 'North', 'Nurture', 'Navigate', 'Noticeable', 'Nexus'],
    O: ['Opportunity', 'Open', 'Outreach', 'Operational', 'Original', 'Orbit', 'Organized', 'Onward', 'Outcome', 'Optimize'],
    P: ['Professional', 'Purpose', 'Product', 'Project', 'Positive', 'Powered', 'People', 'Practical', 'Progress', 'Path'],
    Q: ['Quality', 'Quick', 'Quest', 'Quiet', 'Quantum', 'Qualified', 'Quorum', 'Quotable', 'Query', 'Quill'],
    R: ['Reach', 'Results', 'Reliable', 'Responsive', 'Resource', 'Ready', 'Renew', 'Rise', 'Roadmap', 'Rooted'],
    S: ['Strategic', 'Smart', 'Shared', 'Sustainable', 'Support', 'Studio', 'Scale', 'Signal', 'Service', 'Spark'],
    T: ['Team', 'Trusted', 'Technical', 'Targeted', 'Together', 'Transform', 'Tool', 'Thrive', 'Track', 'Tactic'],
    U: ['Unified', 'Useful', 'Urban', 'Upgrade', 'Uplift', 'Understand', 'Utility', 'Unite', 'Unique', 'User'],
    V: ['Vision', 'Value', 'Vital', 'Venture', 'Voice', 'Visible', 'Verified', 'Velocity', 'Volunteer', 'Versatile'],
    W: ['Works', 'Workshop', 'World', 'Wise', 'Workflow', 'Way', 'Wave', 'Wellness', 'Win', 'Wing'],
    X: ['Xchange', 'Xcelerate', 'Xpert', 'Xplore', 'Xact', 'Xpand', 'Xenial', 'X-factor', 'Xperience', 'Xylem'],
    Y: ['Yield', 'Youth', 'Your', 'Year-round', 'Yes', 'Yardstick', 'Yonder', 'Yoke', 'Yarn', 'Yielding'],
    Z: ['Zenith', 'Zone', 'Zero-Waste', 'Zoom', 'Zest', 'Zonal', 'Zip', 'Zing', 'Zeal', 'Zestful']
  };

  const WORD_TAGS = {
    Adaptive: ['tech', 'operations', 'product'],
    Aligned: ['team', 'brand', 'operations'],
    Active: ['health', 'community'],
    Agile: ['tech', 'operations', 'product'],
    Authentic: ['brand', 'community'],
    Advanced: ['tech', 'product'],
    Accessible: ['community', 'education', 'health'],
    Accelerated: ['growth', 'operations'],
    Audience: ['brand', 'marketing'],
    Action: ['community', 'nonprofit', 'operations'],
    Bold: ['brand', 'growth'],
    Brand: ['brand'],
    Bridge: ['community', 'team', 'nonprofit'],
    Better: ['product', 'health', 'education'],
    Business: ['growth', 'finance'],
    Bright: ['education', 'brand'],
    Balanced: ['health', 'team'],
    Build: ['product', 'community', 'tech'],
    Benefit: ['nonprofit', 'community', 'health'],
    Blueprint: ['operations', 'tech'],
    Clear: ['brand', 'product'],
    Creative: ['brand', 'community'],
    Connected: ['community', 'team', 'tech'],
    Community: ['community', 'nonprofit'],
    Care: ['health', 'community'],
    Catalyst: ['growth', 'nonprofit', 'product'],
    Core: ['brand', 'operations'],
    Collective: ['team', 'community'],
    Craft: ['brand', 'product'],
    Code: ['tech'],
    Driven: ['growth', 'operations'],
    Digital: ['tech', 'product', 'brand'],
    Dynamic: ['brand', 'growth'],
    Direct: ['operations', 'brand'],
    Design: ['brand', 'product', 'tech'],
    Delivery: ['operations', 'product'],
    Development: ['growth', 'product', 'community'],
    Discovery: ['product', 'brand', 'education'],
    Data: ['tech', 'finance'],
    Dependable: ['security', 'operations'],
    Effective: ['operations', 'product'],
    Elevated: ['brand', 'growth'],
    Essential: ['health', 'product'],
    Engine: ['tech', 'growth'],
    Enterprise: ['growth', 'finance'],
    Empower: ['nonprofit', 'education', 'team'],
    Eco: ['environment'],
    Enable: ['tech', 'operations', 'education'],
    Exchange: ['community', 'finance', 'education'],
    Everyday: ['product', 'community'],
    Focused: ['operations', 'team', 'product'],
    Future: ['brand', 'growth', 'environment'],
    Friendly: ['community', 'brand'],
    Forward: ['growth', 'brand'],
    Flexible: ['operations', 'product', 'team'],
    Flourish: ['growth', 'community'],
    Foundry: ['tech', 'product'],
    Framework: ['tech', 'operations'],
    Fund: ['finance', 'nonprofit'],
    Force: ['team', 'growth'],
    Growth: ['growth'],
    Guided: ['education', 'community'],
    Green: ['environment'],
    Global: ['growth', 'community'],
    Genuine: ['brand', 'community'],
    Grounded: ['brand', 'team'],
    Group: ['team', 'community'],
    Generate: ['growth', 'tech'],
    Goal: ['operations', 'team'],
    Gather: ['community', 'team'],
    Human: ['health', 'community', 'brand'],
    Helpful: ['community', 'health', 'education'],
    Healthy: ['health'],
    Horizon: ['growth', 'brand'],
    Hub: ['tech', 'community'],
    Harmony: ['team', 'health', 'community'],
    'Hands-on': ['education', 'community'],
    'High-Impact': ['nonprofit', 'growth'],
    Holistic: ['health', 'education'],
    Hope: ['nonprofit', 'community'],
    Impact: ['nonprofit', 'growth', 'community'],
    Insight: ['tech', 'brand', 'finance'],
    Inclusive: ['community', 'education', 'team'],
    Innovation: ['tech', 'product', 'growth'],
    Intelligent: ['tech', 'product'],
    Integrated: ['tech', 'operations'],
    Initiative: ['nonprofit', 'community'],
    Improve: ['health', 'operations', 'education'],
    Inspire: ['brand', 'education', 'community'],
    Integrity: ['brand', 'security', 'team'],
    Joint: ['team', 'community'],
    Journey: ['brand', 'education'],
    Joyful: ['community', 'brand'],
    Just: ['nonprofit', 'community'],
    Jumpstart: ['growth', 'education'],
    Junction: ['community', 'tech'],
    Junior: ['education'],
    Justice: ['nonprofit', 'community'],
    Jewel: ['brand'],
    Jolt: ['growth', 'brand'],
    Key: ['product', 'operations'],
    Knowledge: ['education', 'tech'],
    Kind: ['community', 'health'],
    Kinetic: ['growth', 'brand'],
    Keep: ['security', 'operations'],
    Kernel: ['tech', 'product'],
    Kinship: ['team', 'community'],
    Kickstart: ['growth', 'education'],
    Keystone: ['brand', 'operations'],
    Knack: ['brand', 'education'],
    Leading: ['growth', 'brand'],
    Local: ['community', 'nonprofit'],
    Launch: ['growth', 'product', 'brand'],
    Learning: ['education'],
    Lift: ['community', 'growth', 'health'],
    Link: ['tech', 'community', 'team'],
    Logic: ['tech', 'finance'],
    Lasting: ['brand', 'environment'],
    Lively: ['brand', 'community'],
    Lab: ['tech', 'education', 'product'],
    Modern: ['brand', 'product'],
    Mission: ['nonprofit', 'brand'],
    Momentum: ['growth', 'team'],
    Market: ['brand', 'growth'],
    Meaningful: ['brand', 'community'],
    Maker: ['product', 'brand'],
    Movement: ['community', 'nonprofit'],
    Method: ['operations', 'education'],
    Member: ['community', 'team'],
    Managed: ['operations', 'security'],
    Next: ['growth', 'product'],
    Network: ['community', 'tech'],
    Natural: ['environment', 'health'],
    New: ['brand', 'growth'],
    Nimble: ['tech', 'operations'],
    North: ['brand'],
    Nurture: ['health', 'community', 'education'],
    Navigate: ['tech', 'operations'],
    Noticeable: ['brand'],
    Nexus: ['tech', 'community'],
    Opportunity: ['growth', 'community'],
    Open: ['community', 'tech', 'education'],
    Outreach: ['nonprofit', 'community'],
    Operational: ['operations'],
    Original: ['brand', 'product'],
    Orbit: ['brand', 'tech'],
    Organized: ['operations', 'team'],
    Onward: ['growth', 'community'],
    Outcome: ['operations', 'health'],
    Optimize: ['tech', 'operations'],
    Professional: ['brand', 'team'],
    Purpose: ['nonprofit', 'brand', 'community'],
    Product: ['product'],
    Project: ['operations', 'team'],
    Positive: ['community', 'health'],
    Powered: ['tech', 'growth'],
    People: ['team', 'community'],
    Practical: ['operations', 'education'],
    Progress: ['growth', 'community'],
    Path: ['education', 'brand'],
    Quality: ['brand', 'product', 'operations'],
    Quick: ['operations', 'tech'],
    Quest: ['brand', 'education'],
    Quiet: ['health', 'security'],
    Quantum: ['tech'],
    Qualified: ['education', 'team'],
    Quorum: ['team', 'community'],
    Quotable: ['brand'],
    Query: ['tech'],
    Quill: ['brand', 'education'],
    Reach: ['growth', 'nonprofit', 'community'],
    Results: ['operations', 'growth'],
    Reliable: ['security', 'operations', 'product'],
    Responsive: ['product', 'community'],
    Resource: ['education', 'community', 'finance'],
    Ready: ['operations', 'team'],
    Renew: ['environment', 'health'],
    Rise: ['growth', 'community'],
    Roadmap: ['operations', 'product'],
    Rooted: ['brand', 'community'],
    Strategic: ['brand', 'growth', 'operations'],
    Smart: ['tech', 'product'],
    Shared: ['team', 'community'],
    Sustainable: ['environment', 'growth'],
    Support: ['community', 'health', 'team'],
    Studio: ['brand', 'product'],
    Scale: ['growth', 'tech'],
    Signal: ['brand', 'tech'],
    Service: ['community', 'operations'],
    Spark: ['brand', 'growth'],
    Team: ['team'],
    Trusted: ['brand', 'security', 'health'],
    Technical: ['tech'],
    Targeted: ['brand', 'growth'],
    Together: ['community', 'team'],
    Transform: ['growth', 'nonprofit', 'health'],
    Tool: ['product', 'tech'],
    Thrive: ['health', 'growth', 'community'],
    Track: ['operations', 'tech'],
    Tactic: ['brand', 'operations'],
    Unified: ['team', 'community', 'tech'],
    Useful: ['product', 'education'],
    Urban: ['community', 'environment'],
    Upgrade: ['tech', 'growth'],
    Uplift: ['community', 'nonprofit', 'brand'],
    Understand: ['education', 'community'],
    Utility: ['product', 'tech', 'operations'],
    Unite: ['team', 'community'],
    Unique: ['brand', 'product'],
    User: ['product', 'tech'],
    Vision: ['brand', 'growth'],
    Value: ['finance', 'brand', 'product'],
    Vital: ['health', 'operations'],
    Venture: ['growth', 'brand'],
    Voice: ['brand', 'community'],
    Visible: ['brand', 'marketing'],
    Verified: ['security', 'finance'],
    Velocity: ['growth', 'tech'],
    Volunteer: ['community', 'nonprofit'],
    Versatile: ['product', 'operations'],
    Works: ['operations', 'product'],
    Workshop: ['education', 'community'],
    World: ['community', 'brand'],
    Wise: ['education', 'finance'],
    Workflow: ['operations', 'tech'],
    Way: ['brand', 'community'],
    Wave: ['brand', 'environment'],
    Wellness: ['health'],
    Win: ['growth', 'team'],
    Wing: ['brand', 'community'],
    Xchange: ['finance', 'community', 'tech'],
    Xcelerate: ['growth', 'tech'],
    Xpert: ['tech', 'education'],
    Xplore: ['education', 'brand'],
    Xact: ['operations', 'finance'],
    Xpand: ['growth'],
    Xenial: ['community'],
    'X-factor': ['brand'],
    Xperience: ['product', 'brand'],
    Xylem: ['environment'],
    Yield: ['finance', 'growth', 'environment'],
    Youth: ['community', 'education'],
    Your: ['brand'],
    'Year-round': ['operations'],
    Yes: ['brand', 'community'],
    Yardstick: ['operations'],
    Yonder: ['brand'],
    Yoke: ['team'],
    Yarn: ['brand'],
    Yielding: ['environment'],
    Zenith: ['growth', 'brand'],
    Zone: ['product', 'operations'],
    'Zero-Waste': ['environment'],
    Zoom: ['growth', 'tech'],
    Zest: ['brand', 'community'],
    Zonal: ['operations'],
    Zip: ['tech', 'growth'],
    Zing: ['brand'],
    Zeal: ['community', 'growth'],
    Zestful: ['brand', 'community']
  };

  const STYLE_BONUSES = {
    professional: ['Strategic', 'Clear', 'Professional', 'Trusted', 'Reliable', 'Operational', 'Quality', 'Results', 'Roadmap'],
    creative: ['Creative', 'Spark', 'Original', 'Journey', 'Studio', 'Bright', 'Zest', 'Orbit'],
    technical: ['Technical', 'Integrated', 'Framework', 'Data', 'Engine', 'Optimize', 'Utility', 'Xact'],
    friendly: ['Friendly', 'Community', 'Helpful', 'Together', 'Human', 'Wellness', 'Joyful', 'Uplift']
  };

  function normalizeAcronymTarget(input) {
    return String(input || '')
      .toUpperCase()
      .replace(/[^A-Z]/g, '')
      .slice(0, MAX_TARGET_LENGTH);
  }

  function tokenizeKeywords(input) {
    return String(input || '')
      .toLowerCase()
      .replace(/[^a-z0-9\s-]/g, ' ')
      .split(/\s+/)
      .filter(Boolean);
  }

  function detectTags(tokens) {
    const found = new Set();
    Object.keys(KEYWORD_TAGS).forEach(function(tag) {
      if (KEYWORD_TAGS[tag].some(function(keyword) { return tokens.includes(keyword); })) {
        found.add(tag);
      }
    });
    return found;
  }

  function createRng(seed) {
    let value = Math.abs(Number.isFinite(seed) ? seed : Date.now()) || 1;
    return function() {
      value |= 0;
      value = value + 0x6D2B79F5 | 0;
      let t = Math.imul(value ^ value >>> 15, 1 | value);
      t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t;
      return ((t ^ t >>> 14) >>> 0) / 4294967296;
    };
  }

  function scoreWord(word, style, tagSet, tokenSet, letterIndex) {
    const tags = WORD_TAGS[word] || [];
    let score = 1;

    tags.forEach(function(tag) {
      if (tagSet.has(tag)) score += 5;
    });

    if ((STYLE_BONUSES[style] || []).includes(word)) score += 4;

    if (tokenSet.has(word.toLowerCase())) score += 4;
    if (letterIndex === 0 && ['Brand', 'Growth', 'Mission', 'Vision', 'Clear', 'Trusted'].includes(word)) score += 2;
    if (letterIndex === 0 && ['Your', 'Yes'].includes(word)) score -= 2;
    if (word.length <= 3) score -= 1;

    return score;
  }

  function getWordOptions(letter, style, tagSet, tokenSet, rng, usedWords, letterIndex) {
    const base = (WORD_BANK[letter] || []).slice();
    const scored = base
      .filter(function(word) { return !usedWords.has(word); })
      .map(function(word) {
        const rawScore = scoreWord(word, style, tagSet, tokenSet, letterIndex);
        return {
          word: word,
          score: rawScore + rng()
        };
      })
      .sort(function(a, b) { return b.score - a.score; });

    return scored.map(function(entry) { return entry.word; });
  }

  function isPronounceableTarget(target) {
    const letters = target.split('');
    const vowelCount = letters.filter(function(letter) { return VOWELS.has(letter); }).length;
    if (vowelCount >= 1) return true;
    return /[LRMN]/.test(target);
  }

  function buildBadges(target, phraseWords, style, matchedTags) {
    const badges = [];
    if (isPronounceableTarget(target)) badges.push('Pronounceable');
    if (matchedTags >= 2) badges.push('Clear');
    if (phraseWords.every(function(word) { return word.length >= 4 && word.length <= 12; })) badges.push('Brandable');

    if (style === 'professional' || style === 'technical') badges.push('Formal');
    if (style === 'friendly') badges.push('Friendly');
    if (style === 'creative') badges.push('Creative');

    if (!badges.length) badges.push('Usable');
    return badges;
  }

  function buildWhyLine(style, matchedTags, hasPronounceableTarget) {
    const parts = [];
    if (matchedTags >= 2) parts.push('built around your topic keywords');
    else if (matchedTags === 1) parts.push('keeps one clear topical cue');
    else parts.push('stays broad enough to reuse across contexts');

    if (style === 'professional') parts.push('leans formal and presentation-ready');
    if (style === 'creative') parts.push('leans more imaginative than corporate');
    if (style === 'technical') parts.push('uses product and systems language');
    if (style === 'friendly') parts.push('sounds approachable and people-first');
    if (hasPronounceableTarget) parts.push('keeps the acronym easy to say');

    return parts.join('; ') + '.';
  }

  function scorePhrase(words, style, tagSet, tokenSet, target) {
    let total = 0;
    let matchedTags = 0;

    words.forEach(function(word, index) {
      const tags = WORD_TAGS[word] || [];
      const wordScore = scoreWord(word, style, tagSet, tokenSet, index);
      total += wordScore;
      if (tags.some(function(tag) { return tagSet.has(tag); })) matchedTags += 1;
    });

    if (isPronounceableTarget(target)) total += 3;
    if (words.length <= 5) total += 2;

    return { total: total, matchedTags: matchedTags };
  }

  function generateAcronymResults(options) {
    const target = normalizeAcronymTarget(options && options.target);
    if (target.length < MIN_TARGET_LENGTH) return [];

    const style = ['professional', 'creative', 'technical', 'friendly'].includes(options && options.style)
      ? options.style
      : 'professional';
    const limit = Math.max(1, Math.min(12, parseInt(options && options.limit, 10) || DEFAULT_LIMIT));
    const tokens = tokenizeKeywords(options && options.keywords);
    const tokenSet = new Set(tokens);
    const tagSet = detectTags(tokens);
    const rng = createRng(options && options.seed);
    const seen = new Set();
    const results = [];

    for (let attempt = 0; attempt < limit * 12 && results.length < limit; attempt += 1) {
      const words = [];
      const usedWords = new Set();

      for (let index = 0; index < target.length; index += 1) {
        const letter = target[index];
        const optionsForLetter = getWordOptions(letter, style, tagSet, tokenSet, rng, usedWords, index);
        if (!optionsForLetter.length) break;

        const pickIndex = Math.min(optionsForLetter.length - 1, Math.floor(rng() * Math.min(5, optionsForLetter.length)) + (attempt % 2));
        const picked = optionsForLetter[pickIndex] || optionsForLetter[0];
        words.push(picked);
        usedWords.add(picked);
      }

      if (words.length !== target.length) continue;

      const phrase = words.join(' ');
      if (seen.has(phrase)) continue;
      seen.add(phrase);

      const scored = scorePhrase(words, style, tagSet, tokenSet, target);
      const badges = buildBadges(target, words, style, scored.matchedTags);

      results.push({
        acronym: target,
        phrase: phrase,
        score: scored.total,
        badges: badges,
        why: buildWhyLine(style, scored.matchedTags, isPronounceableTarget(target))
      });
    }

    return results.sort(function(a, b) { return b.score - a.score; }).slice(0, limit);
  }

  function copyText(text) {
    if (typeof navigator !== 'undefined' && navigator.clipboard && navigator.clipboard.writeText) {
      return navigator.clipboard.writeText(text);
    }
    return Promise.reject(new Error('Clipboard unavailable'));
  }

  function initAcronymMakerPage() {
    if (typeof document === 'undefined') return;

    const targetInput = document.getElementById('am-target');
    const keywordsInput = document.getElementById('am-keywords');
    const styleSelect = document.getElementById('am-style');
    const generateButton = document.getElementById('am-generate');
    const regenerateButton = document.getElementById('am-regenerate');
    const copyAllButton = document.getElementById('am-copy-all');
    const resultList = document.getElementById('am-results');
    const status = document.getElementById('am-status');
    const error = document.getElementById('am-error');
    const exampleButtons = Array.from(document.querySelectorAll('[data-am-example]'));

    if (!targetInput || !keywordsInput || !styleSelect || !generateButton || !resultList) return;

    let generationCount = 0;
    let lastResults = [];

    function setStatus(message) {
      if (status) status.textContent = message;
    }

    function setError(message) {
      if (!error) return;
      error.textContent = message || '';
      error.style.display = message ? 'block' : 'none';
    }

    function renderResults(results) {
      resultList.innerHTML = '';

      if (!results.length) {
        setStatus('No results yet. Enter 2 to 8 letters and generate ideas.');
        return;
      }

      const fragment = document.createDocumentFragment();

      results.forEach(function(result) {
        const item = document.createElement('article');
        item.className = 'am-result';

        const top = document.createElement('div');
        top.className = 'am-result-top';

        const titleWrap = document.createElement('div');
        titleWrap.className = 'am-result-head';

        const acronym = document.createElement('div');
        acronym.className = 'am-result-acronym';
        acronym.textContent = result.acronym;

        const phrase = document.createElement('div');
        phrase.className = 'am-result-phrase';
        phrase.textContent = result.phrase;

        const badgeRow = document.createElement('div');
        badgeRow.className = 'am-badges';
        result.badges.forEach(function(badge) {
          const chip = document.createElement('span');
          chip.className = 'am-badge';
          chip.textContent = badge;
          badgeRow.appendChild(chip);
        });

        titleWrap.appendChild(acronym);
        titleWrap.appendChild(phrase);
        titleWrap.appendChild(badgeRow);

        const copyButton = document.createElement('button');
        copyButton.type = 'button';
        copyButton.className = 'am-copy';
        copyButton.textContent = 'Copy';
        copyButton.addEventListener('click', function() {
          copyText(result.phrase).then(function() {
            copyButton.textContent = 'Copied';
            window.setTimeout(function() {
              copyButton.textContent = 'Copy';
            }, 1200);
          }).catch(function() {
            copyButton.textContent = 'Unavailable';
          });
        });

        top.appendChild(titleWrap);
        top.appendChild(copyButton);

        const why = document.createElement('p');
        why.className = 'am-why';
        why.textContent = result.why;

        item.appendChild(top);
        item.appendChild(why);
        fragment.appendChild(item);
      });

      resultList.appendChild(fragment);
      setStatus(results.length + ' acronym ideas generated.');
    }

    function runGeneration(useFreshSeed) {
      const target = normalizeAcronymTarget(targetInput.value);
      if (target.length < MIN_TARGET_LENGTH) {
        setError('Enter 2 to 8 letters using A-Z only.');
        resultList.innerHTML = '';
        setStatus('Need a short acronym target before results can be generated.');
        return;
      }

      setError('');
      targetInput.value = target;
      generationCount += 1;

      lastResults = generateAcronymResults({
        target: target,
        keywords: keywordsInput.value,
        style: styleSelect.value,
        limit: 10,
        seed: useFreshSeed ? Date.now() + generationCount : generationCount
      });

      renderResults(lastResults);
    }

    generateButton.addEventListener('click', function() {
      runGeneration(false);
    });

    if (regenerateButton) {
      regenerateButton.addEventListener('click', function() {
        runGeneration(true);
      });
    }

    if (copyAllButton) {
      copyAllButton.addEventListener('click', function() {
        if (!lastResults.length) return;
        const combined = lastResults.map(function(result) { return result.acronym + ': ' + result.phrase; }).join('\n');
        copyText(combined).then(function() {
          copyAllButton.textContent = 'Copied all';
          window.setTimeout(function() {
            copyAllButton.textContent = 'Copy all';
          }, 1200);
        }).catch(function() {
          copyAllButton.textContent = 'Unavailable';
        });
      });
    }

    targetInput.addEventListener('input', function() {
      const normalized = normalizeAcronymTarget(targetInput.value);
      if (targetInput.value !== normalized) targetInput.value = normalized;
    });

    targetInput.addEventListener('keydown', function(event) {
      if (event.key === 'Enter') {
        event.preventDefault();
        runGeneration(false);
      }
    });

    exampleButtons.forEach(function(button) {
      button.addEventListener('click', function() {
        targetInput.value = button.getAttribute('data-target') || '';
        keywordsInput.value = button.getAttribute('data-keywords') || '';
        styleSelect.value = button.getAttribute('data-style') || 'professional';
        runGeneration(false);
      });
    });

    runGeneration(false);
  }

  return {
    generateAcronymResults: generateAcronymResults,
    initAcronymMakerPage: initAcronymMakerPage,
    normalizeAcronymTarget: normalizeAcronymTarget
  };
});

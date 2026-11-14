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
    A: ['Adaptive', 'Aligned', 'Active', 'Agile', 'Authentic', 'Advanced', 'Accessible', 'Accelerated', 'Audience', 'Action', 'Allied', 'Ambient', 'Anchor', 'Applied', 'Artisan', 'Ascent', 'Assist', 'Atlas', 'Aware', 'Axiom', 'Access', 'Admirable', 'Amplified', 'Approachable', 'Ample'],
    B: ['Bold', 'Brand', 'Bridge', 'Better', 'Business', 'Bright', 'Balanced', 'Build', 'Benefit', 'Blueprint', 'Beacon', 'Backbone', 'Boost', 'Bespoke', 'Boundary', 'Boundless', 'Breakthrough', 'Buzz', 'Breeze', 'Base', 'Bloom', 'Branch', 'Beyond', 'Buildup', 'Blend'],
    C: ['Clear', 'Creative', 'Connected', 'Community', 'Care', 'Catalyst', 'Core', 'Collective', 'Craft', 'Code', 'Clever', 'Confident', 'Capable', 'Candid', 'Classic', 'Compound', 'Common', 'Compass', 'Content', 'Current', 'Cycle', 'Collaborative', 'Crisp', 'Centered', 'Charter'],
    D: ['Driven', 'Digital', 'Dynamic', 'Direct', 'Design', 'Delivery', 'Development', 'Discovery', 'Data', 'Dependable', 'Daily', 'Decisive', 'Dedicated', 'Diverse', 'Durable', 'Deep', 'Deliberate', 'Diamond', 'Distinct', 'Daring', 'Dialog', 'Drive', 'Dream', 'Dawn', 'Daybreak'],
    E: ['Effective', 'Elevated', 'Essential', 'Engine', 'Enterprise', 'Empower', 'Eco', 'Enable', 'Exchange', 'Everyday', 'Equitable', 'Earnest', 'Earth', 'Easy', 'Edge', 'Education', 'Element', 'Elite', 'Energy', 'Engage', 'Equal', 'Evolve', 'Expand', 'Explore', 'Expert'],
    F: ['Focused', 'Future', 'Friendly', 'Forward', 'Flexible', 'Flourish', 'Foundry', 'Framework', 'Fund', 'Force', 'Fast', 'Fearless', 'Fine', 'Finish', 'First', 'Fit', 'Flow', 'Fluent', 'Fresh', 'Full', 'Function', 'Fabric', 'Fair', 'Faithful', 'Family'],
    G: ['Growth', 'Guided', 'Green', 'Global', 'Genuine', 'Grounded', 'Group', 'Generate', 'Goal', 'Gather', 'Gentle', 'Gift', 'Giving', 'Glad', 'Glow', 'Good', 'Grace', 'Grand', 'Grateful', 'Great', 'Grit', 'Guard', 'Guide', 'Gear', 'Golden'],
    H: ['Human', 'Helpful', 'Healthy', 'Horizon', 'Hub', 'Harmony', 'Hands-on', 'High-Impact', 'Holistic', 'Hope', 'Habit', 'Handshake', 'Happy', 'Hardy', 'Harvest', 'Heart', 'Hearth', 'Heritage', 'Highland', 'Highlight', 'Home', 'Honest', 'Honor', 'Humble', 'Harmony'],
    I: ['Impact', 'Insight', 'Inclusive', 'Innovation', 'Intelligent', 'Integrated', 'Initiative', 'Improve', 'Inspire', 'Integrity', 'Ideal', 'Idea', 'Imagine', 'Immediate', 'Impression', 'Independent', 'Index', 'Industry', 'Infinite', 'Informed', 'Ingenious', 'Inside', 'Instant', 'Intent', 'Invest'],
    J: ['Joint', 'Journey', 'Joyful', 'Just', 'Jumpstart', 'Junction', 'Junior', 'Justice', 'Jewel', 'Jolt', 'Jovial', 'Judgment', 'Jet', 'Jigsaw', 'Jive', 'Jogger', 'Jot', 'Jubilant', 'Juice', 'Jury', 'Justified', 'Juxtapose', 'Jazz', 'Jet-set', 'Jamboree'],
    K: ['Key', 'Knowledge', 'Kind', 'Kinetic', 'Keep', 'Kernel', 'Kinship', 'Kickstart', 'Keystone', 'Knack', 'Kaleidoscope', 'Karma', 'Keen', 'Keeper', 'Kindred', 'Kinetic', 'Kismet', 'Kit', 'Knight', 'Knitted', 'Knowing', 'Known', 'King', 'Kingdom', 'Krypton'],
    L: ['Leading', 'Local', 'Launch', 'Learning', 'Lift', 'Link', 'Logic', 'Lasting', 'Lively', 'Lab', 'Ladder', 'Lamp', 'Lane', 'Large', 'Latitude', 'Lean', 'Legacy', 'Legend', 'Lens', 'Level', 'Liberal', 'Light', 'Linear', 'Living', 'Loft'],
    M: ['Modern', 'Mission', 'Momentum', 'Market', 'Meaningful', 'Maker', 'Movement', 'Method', 'Member', 'Managed', 'Main', 'Major', 'Mantle', 'Map', 'Mark', 'Mature', 'Mentor', 'Merit', 'Mesh', 'Methodical', 'Milestone', 'Mindful', 'Model', 'Motion', 'Mutual'],
    N: ['Next', 'Network', 'Natural', 'New', 'Nimble', 'North', 'Nurture', 'Navigate', 'Noticeable', 'Nexus', 'Namesake', 'Native', 'Needed', 'Neighbor', 'Nest', 'Niche', 'Noble', 'Nod', 'Norm', 'Notable', 'Notice', 'Novel', 'Nova', 'Nugget', 'Number'],
    O: ['Opportunity', 'Open', 'Outreach', 'Operational', 'Original', 'Orbit', 'Organized', 'Onward', 'Outcome', 'Optimize', 'Objective', 'Observant', 'Offer', 'Office', 'Omega', 'One', 'Order', 'Organic', 'Origin', 'Outlook', 'Outlet', 'Output', 'Outside', 'Overall', 'Owner'],
    P: ['Professional', 'Purpose', 'Product', 'Project', 'Positive', 'Powered', 'People', 'Practical', 'Progress', 'Path', 'Pace', 'Pack', 'Partner', 'Pathway', 'Patient', 'Peak', 'Peer', 'Pilot', 'Pioneer', 'Pledge', 'Plus', 'Point', 'Portal', 'Pride', 'Proven'],
    Q: ['Quality', 'Quick', 'Quest', 'Quiet', 'Quantum', 'Qualified', 'Quorum', 'Quotable', 'Query', 'Quill', 'Quaint', 'Quantify', 'Quartz', 'Queen', 'Quench', 'Quintet', 'Quirky', 'Quiver', 'Quota', 'Quintessential', 'Quilt', 'Quip', 'Quorum', 'Quasar', 'Quintuple'],
    R: ['Reach', 'Results', 'Reliable', 'Responsive', 'Resource', 'Ready', 'Renew', 'Rise', 'Roadmap', 'Rooted', 'Radiant', 'Rally', 'Rare', 'Raw', 'Real', 'Reason', 'Rebuild', 'Recognize', 'Record', 'Refined', 'Relay', 'Reliable', 'Remote', 'Reset', 'Rhythm'],
    S: ['Strategic', 'Smart', 'Shared', 'Sustainable', 'Support', 'Studio', 'Scale', 'Signal', 'Service', 'Spark', 'Safe', 'Sage', 'Sanctuary', 'Sapient', 'Savvy', 'Seasoned', 'Seed', 'Sense', 'Serious', 'Shape', 'Shift', 'Shine', 'Simple', 'Skilled', 'Social'],
    T: ['Team', 'Trusted', 'Technical', 'Targeted', 'Together', 'Transform', 'Tool', 'Thrive', 'Track', 'Tactic', 'Talent', 'Tandem', 'Teach', 'Tenor', 'Tested', 'Textile', 'Theory', 'Thoughtful', 'Thread', 'Tier', 'Tight', 'Timeless', 'Timely', 'Tone', 'Top'],
    U: ['Unified', 'Useful', 'Urban', 'Upgrade', 'Uplift', 'Understand', 'Utility', 'Unite', 'Unique', 'User', 'Ultra', 'Umbrella', 'Unbiased', 'Underline', 'Underpin', 'Undo', 'Universal', 'Unknown', 'Unlimited', 'Unlock', 'Upbeat', 'Upfront', 'Upkeep', 'Upright', 'Upward'],
    V: ['Vision', 'Value', 'Vital', 'Venture', 'Voice', 'Visible', 'Verified', 'Velocity', 'Volunteer', 'Versatile', 'Valid', 'Vanguard', 'Vast', 'Veteran', 'Viable', 'Vibrance', 'Victory', 'Vigor', 'Vigilant', 'Village', 'Virtual', 'Virtue', 'Vista', 'Visit', 'Vivid'],
    W: ['Works', 'Workshop', 'World', 'Wise', 'Workflow', 'Way', 'Wave', 'Wellness', 'Win', 'Wing', 'Walk', 'Warmth', 'Watch', 'Water', 'Welcome', 'Whole', 'Wide', 'Wider', 'Wild', 'Willing', 'Window', 'Winning', 'Wisdom', 'Witness', 'Wonder'],
    X: ['Xchange', 'Xcelerate', 'Xpert', 'Xplore', 'Xact', 'Xpand', 'Xenial', 'X-factor', 'Xperience', 'Xylem', 'Xtra', 'Xtreme', 'Xcept', 'Xcess', 'Xtend', 'Xplain', 'Xpert', 'Xpress', 'Xchange', 'Xplicit', 'Xport', 'Xample', 'Xcellent', 'Xpand', 'Xcite'],
    Y: ['Yield', 'Youth', 'Your', 'Year-round', 'Yes', 'Yardstick', 'Yonder', 'Yoke', 'Yarn', 'Yielding', 'Yearly', 'Yen', 'Young', 'Yarnspin', 'Yeti', 'Yacht', 'Yielded', 'Yummy', 'Yacht', 'Yeast', 'Yield-plus', 'Yardage', 'Yeoman', 'Yearn', 'Year-one'],
    Z: ['Zenith', 'Zone', 'Zero-Waste', 'Zoom', 'Zest', 'Zonal', 'Zip', 'Zing', 'Zeal', 'Zestful', 'Zephyr', 'Zebra', 'Zeroed', 'Zing-up', 'Zippy', 'Zodiac', 'Zoned', 'Zoomed', 'Zygote', 'Zinger', 'Zing', 'Zoomer', 'Zone-one', 'Zealous', 'Zero-day']
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

  const STOP_WORDS = new Set([
    'a','an','the','and','or','but','so','of','for','to','with','in','on','at','by','is','are','be','am',
    'our','your','my','their','his','her','its','we','us','they','them','i','me','you',
    'that','this','these','those','will','can','may','might','should','would','could',
    'from','as','into','onto','out','up','down','over','under','about','across',
    'it','if','not','no','yes','very','just','also','than','then','there','here'
  ]);

  const CATEGORY_OPTIONS = ['brand','growth','team','product','tech','community','nonprofit','environment','health','education','finance','security','operations'];

  function normalizeAcronymTarget(input) {
    return String(input || '')
      .toUpperCase()
      .replace(/[^A-Z]/g, '')
      .slice(0, MAX_TARGET_LENGTH);
  }

  function normalizeCategory(input) {
    const value = String(input || '').toLowerCase().trim();
    return CATEGORY_OPTIONS.indexOf(value) !== -1 ? value : '';
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
    const category = normalizeCategory(options && options.category);
    if (category) tagSet.add(category);
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

  function titleCaseWord(word) {
    if (!word) return '';
    return word.charAt(0).toUpperCase() + word.slice(1).toLowerCase();
  }

  function extractSignificantWords(phrase) {
    const raw = tokenizeKeywords(phrase);
    const significant = raw.filter(function(t) { return t.length > 1 && !STOP_WORDS.has(t) && /[a-z]/.test(t); });
    return significant.length ? significant : raw.filter(function(t) { return /[a-z]/.test(t); });
  }

  function shuffleArray(array, rng) {
    const copy = array.slice();
    for (let i = copy.length - 1; i > 0; i -= 1) {
      const j = Math.floor(rng() * (i + 1));
      const tmp = copy[i];
      copy[i] = copy[j];
      copy[j] = tmp;
    }
    return copy;
  }

  function scoreReverseAcronym(letters) {
    const vowels = letters.split('').filter(function(l) { return VOWELS.has(l); }).length;
    const unique = new Set(letters.split('')).size;
    let score = unique;
    if (vowels >= 1) score += 3;
    if (vowels >= 2) score += 1;
    if (letters.length >= 3 && letters.length <= 5) score += 2;
    if (/^[AEIOUY]/.test(letters)) score -= 1;
    return score;
  }

  function buildReverseBadges(letters, chosenWords, inOrder) {
    const badges = [];
    if (isPronounceableTarget(letters)) badges.push('Pronounceable');
    if (new Set(letters.split('')).size === letters.length) badges.push('No repeats');
    if (inOrder) badges.push('Reads in order');
    if (chosenWords.every(function(w) { return w.length >= 3 && w.length <= 10; })) badges.push('Memorable');
    return badges;
  }

  function generateReverseAcronyms(options) {
    const phrase = String(options && options.phrase || '');
    const requestedLength = parseInt(options && options.length, 10);
    const length = Math.max(MIN_TARGET_LENGTH, Math.min(MAX_TARGET_LENGTH, Number.isFinite(requestedLength) ? requestedLength : 4));
    const limit = Math.max(1, Math.min(12, parseInt(options && options.limit, 10) || DEFAULT_LIMIT));
    const words = extractSignificantWords(phrase);
    if (words.length < length) return [];

    const rng = createRng(options && options.seed);
    const results = [];
    const seen = new Set();
    const pronounceableOnly = !!(options && options.pronounceableOnly);

    function pushCandidate(indices, inOrder) {
      const sorted = inOrder ? indices.slice().sort(function(a, b) { return a - b; }) : indices;
      const chosen = sorted.map(function(i) { return words[i]; });
      const letters = chosen.map(function(w) { return w.charAt(0).toUpperCase(); }).join('');
      if (pronounceableOnly && !isPronounceableTarget(letters)) return;
      const key = letters + '|' + chosen.join(' ');
      if (seen.has(key)) return;
      seen.add(key);
      results.push({
        acronym: letters,
        phrase: chosen.map(titleCaseWord).join(' '),
        score: scoreReverseAcronym(letters) + (inOrder ? 1 : 0),
        badges: buildReverseBadges(letters, chosen, inOrder),
        why: inOrder
          ? 'First letters of your words, kept in the order you wrote them.'
          : 'First letters of your words, reordered for a smoother acronym.'
      });
    }

    const inOrderCount = Math.min(limit, Math.max(3, words.length - length + 1));
    for (let start = 0; start < inOrderCount && results.length < limit; start += 1) {
      if (start + length > words.length) break;
      const indices = [];
      for (let k = 0; k < length; k += 1) indices.push(start + k);
      pushCandidate(indices, true);
    }

    const totalPicks = Math.max(limit * 6, 24);
    for (let attempt = 0; attempt < totalPicks && results.length < limit * 2; attempt += 1) {
      const shuffled = shuffleArray(words.map(function(_, i) { return i; }), rng);
      const indices = shuffled.slice(0, length);
      pushCandidate(indices, false);
    }

    return results
      .sort(function(a, b) { return b.score - a.score; })
      .slice(0, limit);
  }

  function copyText(text) {
    if (typeof navigator !== 'undefined' && navigator.clipboard && navigator.clipboard.writeText) {
      return navigator.clipboard.writeText(text);
    }
    return Promise.reject(new Error('Clipboard unavailable'));
  }

  function bindFaqAccordion(root) {
    const scope = root || (typeof document !== 'undefined' ? document : null);
    if (!scope || typeof scope.querySelectorAll !== 'function') return;

    const items = Array.from(scope.querySelectorAll('.faq-item'));
    const questions = Array.from(scope.querySelectorAll('.faq-q'));

    questions.forEach(function(question) {
      if (typeof question.addEventListener !== 'function') return;
      question.addEventListener('click', function() {
        const item = typeof question.closest === 'function' ? question.closest('.faq-item') : null;
        if (!item || !item.classList) return;

        const isOpen = typeof item.classList.contains === 'function' && item.classList.contains('open');
        items.forEach(function(other) {
          if (other !== item && other.classList && typeof other.classList.remove === 'function') {
            other.classList.remove('open');
          }
        });

        if (isOpen) {
          if (typeof item.classList.remove === 'function') item.classList.remove('open');
        } else if (typeof item.classList.add === 'function') {
          item.classList.add('open');
        }
      });
    });
  }

  function initAcronymMakerPage() {
    if (typeof document === 'undefined') return;

    const targetInput = document.getElementById('am-target');
    const keywordsInput = document.getElementById('am-keywords');
    const styleSelect = document.getElementById('am-style');
    const categorySelect = document.getElementById('am-category');
    const phraseInput = document.getElementById('am-phrase');
    const lengthSelect = document.getElementById('am-length');
    const generateButton = document.getElementById('am-generate');
    const regenerateButton = document.getElementById('am-regenerate');
    const regeneratePanelButton = document.getElementById('am-regenerate-panel');
    const copyAllButton = document.getElementById('am-copy-all');
    const resultList = document.getElementById('am-results');
    const status = document.getElementById('am-status');
    const error = document.getElementById('am-error');
    const exampleButtons = Array.from(document.querySelectorAll('[data-am-example]'));
    const tabButtons = Array.from(document.querySelectorAll('[data-am-tab]'));
    const modePanels = Array.from(document.querySelectorAll('[data-am-mode]'));
    const pronounceableCheck = document.getElementById('am-pronounceable');
    const savedPanel = document.getElementById('am-saved');
    const savedList = document.getElementById('am-saved-list');
    const savedClear = document.getElementById('am-saved-clear');

    if (!targetInput || !keywordsInput || !styleSelect || !generateButton || !resultList) return;

    const SAVED_KEY = 'wnr_am_saved_v1';
    let generationCount = 0;
    let lastResults = [];
    let currentMode = 'forward';

    function loadSaved() {
      try {
        const raw = localStorage.getItem(SAVED_KEY);
        const parsed = raw ? JSON.parse(raw) : [];
        return Array.isArray(parsed) ? parsed : [];
      } catch (e) { return []; }
    }
    function persistSaved(list) {
      try { localStorage.setItem(SAVED_KEY, JSON.stringify(list)); } catch (e) {}
    }
    let savedItems = loadSaved();

    function savedKey(item) { return (item.mode || 'forward') + '|' + item.acronym + '|' + item.phrase; }
    function isSaved(item) {
      const k = savedKey(item);
      return savedItems.some(function(s) { return savedKey(s) === k; });
    }
    function renderSaved() {
      if (!savedPanel || !savedList) return;
      if (!savedItems.length) { savedPanel.hidden = true; savedList.innerHTML = ''; return; }
      savedPanel.hidden = false;
      savedList.innerHTML = '';
      savedItems.forEach(function(item, idx) {
        const chip = document.createElement('span');
        chip.className = 'am-saved-chip';
        chip.title = item.phrase;
        chip.innerHTML = '<span class="am-saved-chip-letters"></span><span class="am-saved-chip-phrase"></span><button type="button" class="am-saved-chip-remove" aria-label="Remove">×</button>';
        chip.querySelector('.am-saved-chip-letters').textContent = item.acronym;
        chip.querySelector('.am-saved-chip-phrase').textContent = item.phrase.length > 32 ? item.phrase.slice(0, 30) + '…' : item.phrase;
        chip.addEventListener('click', function(ev) {
          if (ev.target.classList.contains('am-saved-chip-remove')) return;
          copyText(item.acronym + ': ' + item.phrase).catch(function(){});
        });
        chip.querySelector('.am-saved-chip-remove').addEventListener('click', function(ev) {
          ev.stopPropagation();
          savedItems.splice(idx, 1);
          persistSaved(savedItems);
          renderSaved();
          refreshStars();
        });
        savedList.appendChild(chip);
      });
    }
    function refreshStars() {
      Array.from(resultList.querySelectorAll('[data-am-row]')).forEach(function(row) {
        const idx = parseInt(row.getAttribute('data-am-row'), 10);
        const result = lastResults[idx];
        if (!result) return;
        const star = row.querySelector('.am-star');
        if (!star) return;
        star.classList.toggle('is-saved', isSaved({ mode: result.mode, acronym: result.acronym, phrase: result.phrase }));
      });
    }

    function updateUrlParams() {
      if (typeof history === 'undefined' || !history.replaceState) return;
      const params = new URLSearchParams();
      params.set('mode', currentMode);
      params.set('style', styleSelect.value);
      if (categorySelect && categorySelect.value) params.set('cat', categorySelect.value);
      if (currentMode === 'reverse') {
        if (phraseInput && phraseInput.value) params.set('phrase', phraseInput.value);
        if (lengthSelect) params.set('len', lengthSelect.value);
        if (pronounceableCheck) params.set('pron', pronounceableCheck.checked ? '1' : '0');
      } else {
        if (targetInput.value) params.set('letters', targetInput.value);
        if (keywordsInput.value) params.set('notes', keywordsInput.value);
      }
      try { history.replaceState({}, '', location.pathname + '?' + params.toString()); } catch (e) {}
    }
    function readUrlParams() {
      if (typeof URLSearchParams === 'undefined') return;
      const params = new URLSearchParams(location.search || '');
      if (params.get('mode') === 'reverse') currentMode = 'reverse';
      if (params.get('style') && styleSelect) styleSelect.value = params.get('style');
      if (params.get('cat') && categorySelect) categorySelect.value = params.get('cat');
      if (params.get('letters')) targetInput.value = params.get('letters');
      if (params.get('notes')) keywordsInput.value = params.get('notes');
      if (params.get('phrase') && phraseInput) phraseInput.value = params.get('phrase');
      if (params.get('len') && lengthSelect) lengthSelect.value = params.get('len');
      if (params.get('pron') != null && pronounceableCheck) pronounceableCheck.checked = params.get('pron') === '1';
    }

    function setMode(mode) {
      currentMode = mode === 'reverse' ? 'reverse' : 'forward';
      tabButtons.forEach(function(btn) {
        const isActive = btn.getAttribute('data-am-tab') === currentMode;
        btn.classList.toggle('is-active', isActive);
        btn.setAttribute('aria-selected', isActive ? 'true' : 'false');
      });
      modePanels.forEach(function(panel) {
        panel.hidden = panel.getAttribute('data-am-mode') !== currentMode;
      });
    }

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
        setStatus('No ideas yet. Enter 2 to 8 letters.');
        const empty = document.createElement('li');
        empty.className = 'am-empty';
        empty.textContent = 'No ideas yet. Enter 2 to 8 letters.';
        resultList.appendChild(empty);
        return;
      }

      const fragment = document.createDocumentFragment();

      results.forEach(function(result, rowIndex) {
        const item = document.createElement('li');
        item.className = 'word-item';
        item.setAttribute('data-am-row', String(rowIndex));

        const left = document.createElement('div');
        left.className = 'word-left';

        const acronym = document.createElement('div');
        acronym.className = 'word-pos';
        acronym.textContent = result.acronym;

        const phrase = document.createElement('div');
        phrase.className = 'word-text';
        phrase.textContent = result.phrase;

        const badgeRow = document.createElement('div');
        badgeRow.className = 'am-badges';
        result.badges.forEach(function(badge) {
          const chip = document.createElement('span');
          chip.className = 'am-badge';
          chip.textContent = badge;
          badgeRow.appendChild(chip);
        });

        const why = document.createElement('div');
        why.className = 'word-def';
        why.textContent = result.why;

        left.appendChild(acronym);
        left.appendChild(phrase);
        left.appendChild(badgeRow);
        left.appendChild(why);

        const right = document.createElement('div');
        right.className = 'word-right';

        const starButton = document.createElement('button');
        starButton.type = 'button';
        starButton.className = 'am-star';
        starButton.title = 'Save';
        starButton.setAttribute('aria-label', 'Save');
        starButton.innerHTML = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2.5l2.9 6.3 6.6.8-4.8 4.5 1.3 6.5L12 17.3l-6 3.3 1.3-6.5L2.5 9.6l6.6-.8L12 2.5z"/></svg>';
        if (isSaved({ mode: result.mode, acronym: result.acronym, phrase: result.phrase })) {
          starButton.classList.add('is-saved');
        }
        starButton.addEventListener('click', function() {
          const payload = { mode: result.mode, acronym: result.acronym, phrase: result.phrase };
          const k = savedKey(payload);
          const existingIdx = savedItems.findIndex(function(s) { return savedKey(s) === k; });
          if (existingIdx >= 0) {
            savedItems.splice(existingIdx, 1);
            starButton.classList.remove('is-saved');
          } else {
            savedItems.push(payload);
            starButton.classList.add('is-saved');
          }
          persistSaved(savedItems);
          renderSaved();
        });

        const rerollButton = document.createElement('button');
        rerollButton.type = 'button';
        rerollButton.className = 'am-reroll';
        rerollButton.title = 'Regenerate this row';
        rerollButton.setAttribute('aria-label', 'Regenerate this row');
        rerollButton.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 12a9 9 0 0 1 15.5-6.3L21 8"/><path d="M21 3v5h-5"/><path d="M21 12a9 9 0 0 1-15.5 6.3L3 16"/><path d="M3 21v-5h5"/></svg>';
        rerollButton.addEventListener('click', function() { rerollRow(rowIndex); });

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

        right.appendChild(starButton);
        right.appendChild(rerollButton);
        right.appendChild(copyButton);
        item.appendChild(left);
        item.appendChild(right);
        fragment.appendChild(item);
      });

      resultList.appendChild(fragment);
      setStatus(results.length + ' ideas generated.');
    }

    function runGeneration(useFreshSeed) {
      generationCount += 1;
      const seed = useFreshSeed ? Date.now() + generationCount : generationCount;
      const categoryValue = categorySelect ? categorySelect.value : '';

      if (currentMode === 'reverse') {
        const phraseValue = phraseInput ? phraseInput.value : '';
        if (!phraseValue || phraseValue.trim().length < 2) {
          setError('Describe your topic in a few words.');
          resultList.innerHTML = '';
          setStatus('Enter a short topic to extract an acronym.');
          updateUrlParams();
          return;
        }
        const requestedLength = lengthSelect ? parseInt(lengthSelect.value, 10) : 4;
        setError('');
        lastResults = generateReverseAcronyms({
          phrase: phraseValue + ' ' + (categoryValue || ''),
          length: requestedLength,
          limit: 10,
          pronounceableOnly: pronounceableCheck ? pronounceableCheck.checked : false,
          seed: seed
        }).map(function(r) { r.mode = 'reverse'; return r; });
        if (!lastResults.length) {
          setError('Add a few more descriptive words so we can pick ' + (requestedLength) + ' letters.');
        }
        renderResults(lastResults);
        updateUrlParams();
        return;
      }

      const target = normalizeAcronymTarget(targetInput.value);
      if (target.length < MIN_TARGET_LENGTH) {
        setError('Enter 2 to 8 letters only.');
        resultList.innerHTML = '';
        setStatus('Enter 2 to 8 letters.');
        updateUrlParams();
        return;
      }

      setError('');
      targetInput.value = target;

      lastResults = generateAcronymResults({
        target: target,
        keywords: keywordsInput.value,
        style: styleSelect.value,
        category: categoryValue,
        limit: 10,
        seed: seed
      }).map(function(r) { r.mode = 'forward'; return r; });

      renderResults(lastResults);
      updateUrlParams();
    }

    function rerollRow(rowIndex) {
      if (rowIndex < 0 || rowIndex >= lastResults.length) return;
      const categoryValue = categorySelect ? categorySelect.value : '';
      const existingKeys = new Set(lastResults.map(function(r, i) { return i === rowIndex ? null : r.acronym + '|' + r.phrase; }));
      let replacement = null;
      for (let attempt = 0; attempt < 20 && !replacement; attempt += 1) {
        const batchSeed = Date.now() + attempt * 7919 + rowIndex;
        let batch;
        if (currentMode === 'reverse') {
          batch = generateReverseAcronyms({
            phrase: (phraseInput ? phraseInput.value : '') + ' ' + (categoryValue || ''),
            length: lengthSelect ? parseInt(lengthSelect.value, 10) : 4,
            limit: 10,
            pronounceableOnly: pronounceableCheck ? pronounceableCheck.checked : false,
            seed: batchSeed
          });
        } else {
          batch = generateAcronymResults({
            target: normalizeAcronymTarget(targetInput.value),
            keywords: keywordsInput.value,
            style: styleSelect.value,
            category: categoryValue,
            limit: 10,
            seed: batchSeed
          });
        }
        for (let i = 0; i < batch.length; i += 1) {
          const key = batch[i].acronym + '|' + batch[i].phrase;
          if (!existingKeys.has(key)) { replacement = batch[i]; break; }
        }
      }
      if (!replacement) return;
      replacement.mode = currentMode;
      lastResults[rowIndex] = replacement;
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

    if (regeneratePanelButton) {
      regeneratePanelButton.addEventListener('click', function() {
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

    tabButtons.forEach(function(btn) {
      btn.addEventListener('click', function() {
        const mode = btn.getAttribute('data-am-tab');
        setMode(mode);
        setError('');
      });
    });

    if (phraseInput) {
      phraseInput.addEventListener('keydown', function(event) {
        if (event.key === 'Enter' && (event.metaKey || event.ctrlKey)) {
          event.preventDefault();
          runGeneration(false);
        }
      });
    }
    if (lengthSelect) {
      lengthSelect.addEventListener('change', function() { runGeneration(false); });
    }
    if (categorySelect) {
      categorySelect.addEventListener('change', function() { runGeneration(false); });
    }
    if (pronounceableCheck) {
      pronounceableCheck.addEventListener('change', function() { runGeneration(false); });
    }
    if (styleSelect) {
      styleSelect.addEventListener('change', function() { runGeneration(false); });
    }
    if (savedClear) {
      savedClear.addEventListener('click', function() {
        savedItems = [];
        persistSaved(savedItems);
        renderSaved();
        refreshStars();
      });
    }

    readUrlParams();
    setMode(currentMode);
    renderSaved();
    runGeneration(false);
  }

  return {
    bindFaqAccordion: bindFaqAccordion,
    generateAcronymResults: generateAcronymResults,
    generateReverseAcronyms: generateReverseAcronyms,
    initAcronymMakerPage: initAcronymMakerPage,
    normalizeAcronymTarget: normalizeAcronymTarget
  };
});

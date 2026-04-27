const WORDINEER = (() => {
const SEED = [
{w:"Brave",    t:"adjective",d:"ready to face danger without fear",                       diff:"easy",  borrowed:false},
{w:"Calm",     t:"adjective",d:"not showing nervousness or strong emotion",               diff:"easy",  borrowed:false},
{w:"Dream",    t:"noun",     d:"a series of images occurring during sleep",               diff:"easy",  borrowed:false},
{w:"Eager",    t:"adjective",d:"wanting to do something very much",                       diff:"easy",  borrowed:false},
{w:"Flame",    t:"noun",     d:"a hot glowing body of ignited gas",                       diff:"easy",  borrowed:false},
{w:"Gentle",   t:"adjective",d:"mild in temperament; kind and tender",                    diff:"easy",  borrowed:false},
{w:"Happy",    t:"adjective",d:"feeling or showing pleasure or contentment",               diff:"easy",  borrowed:false},
{w:"Inspire",  t:"verb",     d:"fill someone with the urge to do something creative",     diff:"medium",borrowed:false},
{w:"Journey",  t:"noun",     d:"an act of travelling from one place to another",          diff:"medium",borrowed:false},
{w:"Keen",     t:"adjective",d:"having or showing eagerness or enthusiasm",               diff:"medium",borrowed:false},
{w:"Labyrinth",t:"noun",     d:"a complicated irregular network of passages",             diff:"hard",  borrowed:false},
{w:"Melancholy",t:"noun",    d:"a deep pensive sadness with no obvious cause",            diff:"hard",  borrowed:false},
{w:"Noble",    t:"adjective",d:"having fine personal qualities or high morals",           diff:"medium",borrowed:false},
{w:"Ocean",    t:"noun",     d:"a very large expanse of sea",                             diff:"easy",  borrowed:false},
{w:"Persist",  t:"verb",     d:"continue firmly in an opinion or course of action",      diff:"medium",borrowed:false},
{w:"Resilient",t:"adjective",d:"able to recover quickly from difficulties",               diff:"medium",borrowed:false},
{w:"Serendipity",t:"noun",   d:"finding something good without looking for it",           diff:"hard",  borrowed:false},
{w:"Tenacious",t:"adjective",d:"tending to keep a firm hold; persistent",                diff:"hard",  borrowed:false},
{w:"Unique",   t:"adjective",d:"being the only one of its kind",                         diff:"medium",borrowed:false},
{w:"Vivid",    t:"adjective",d:"producing powerful feelings or clear images",             diff:"easy",  borrowed:false},
{w:"Wander",   t:"verb",     d:"walk or move in a leisurely or aimless way",              diff:"easy",  borrowed:false},
{w:"Zealous",  t:"adjective",d:"having or showing great energy in pursuit of a cause",   diff:"hard",  borrowed:false},
{w:"Wanderlust",t:"noun",    d:"a strong desire to travel and explore the world",         diff:"medium",borrowed:true},
{w:"Schadenfreude",t:"noun", d:"pleasure derived from another person's misfortune",       diff:"hard",  borrowed:true},
];
let WORDS      = [...SEED];
let saved      = [];
let current    = [];
let config     = {};
let defsShown  = true;
let fullLoaded = false;
let API_KEYS   = { wordnik: '', merriam: '' };
const SC_WORDS_KEY = 'wnr_words_v3';
function scGet(key) {
try { return JSON.parse(sessionStorage.getItem(key)); } catch { return null; }
}
function scSet(key, val) {
try { sessionStorage.setItem(key, JSON.stringify(val)); } catch {}
}
async function loadWords() {
const cached = scGet(SC_WORDS_KEY);
if (Array.isArray(cached) && cached.length > 100) {
WORDS = cached;
fullLoaded = true;
return;
}
try {
const res = await fetch('/data/words.json');
if (!res.ok) throw new Error(res.status);
const raw = await res.json();
const data = raw.map(e => ({ w: e[0], t: e[1], d: e[2], diff: e[3], borrowed: e[4] }));
WORDS = data;
fullLoaded = true;
scSet(SC_WORDS_KEY, data);
} catch {
}
}
const DM_SEEDS = [
'adventure','beauty','courage','dream','earth','forest','grace','hope',
'journey','knowledge','light','mind','nature','ocean','peace','quest',
'river','spirit','truth','vision','wisdom','wonder','youth','time','life',
'shadow','storm','fire','water','silence','freedom','growth','change',
'memory','power','glory','faith','chaos','order','mystery','legend',
];
const POS_MAP = { noun:'n', adjective:'adj', verb:'v', adverb:'adv' };
async function fetchDatamuse(type) {
const seed  = DM_SEEDS[Math.floor(Math.random() * DM_SEEDS.length)];
const posQ  = (type !== 'all' && POS_MAP[type]) ? `&pos=${POS_MAP[type]}` : '';
const cKey  = `wnr_dm_${seed}_${type}`;
const hit   = scGet(cKey);
if (hit) return hit;
try {
const res  = await fetch(`https://api.datamuse.com/words?ml=${seed}${posQ}&max=25`, { signal: AbortSignal.timeout(4000) });
if (!res.ok) return [];
const data = await res.json();
const words = data.map(d => d.word).filter(w => w && /^[a-z]{3,}$/.test(w));
scSet(cKey, words);
return words;
} catch { return []; }
}
async function fetchDefinition(word) {
const cKey = `wnr_def_${word.toLowerCase()}`;
const hit  = scGet(cKey);
if (hit) return hit;
// 1. Free Dictionary API
try {
  const res = await fetch(`https://api.dictionaryapi.dev/api/v2/entries/en/${encodeURIComponent(word)}`, { signal: AbortSignal.timeout(4000) });
  if (res.ok) {
    const data    = await res.json();
    const meaning = data[0]?.meanings?.[0];
    const def     = meaning?.definitions?.[0]?.definition;
    const pos     = meaning?.partOfSpeech;
    if (def) {
      const result = { def: def.slice(0, 100), pos };
      scSet(cKey, result);
      return result;
    }
  }
} catch {}
// 2. Merriam-Webster fallback
const mw = await fetchMerriamDef(word);
if (mw) { scSet(cKey, mw); return mw; }
// 3. Wordnik fallback
const wn = await fetchWordnikDef(word);
if (wn) { scSet(cKey, wn); return wn; }
scSet(cKey, null);
return null;
}
async function fetchWordnikWords(type) {
if (!API_KEYS.wordnik) return [];
const posParam = (type !== 'all' && type !== 'extended' && type !== 'nonenglish' && POS_MAP[type])
  ? `&includePartOfSpeech=${type}` : '';
const cKey = `wnr_wn_${type}`;
const hit  = scGet(cKey);
if (hit) return hit;
try {
  const res = await fetch(
    `https://api.wordnik.com/v4/words.json/randomWords?hasDictionaryDef=true${posParam}&minCorpusCount=5000&limit=20&api_key=${API_KEYS.wordnik}`,
    { signal: AbortSignal.timeout(5000) }
  );
  if (!res.ok) return [];
  const data  = await res.json();
  const words = data.map(d => d.word).filter(w => w && /^[a-z]{3,}$/.test(w));
  scSet(cKey, words);
  return words;
} catch { return []; }
}
async function fetchWordnikDef(word) {
if (!API_KEYS.wordnik) return null;
try {
  const res = await fetch(
    `https://api.wordnik.com/v4/word.json/${encodeURIComponent(word)}/definitions?limit=3&sourceDictionaries=all&useCanonical=false&api_key=${API_KEYS.wordnik}`,
    { signal: AbortSignal.timeout(4000) }
  );
  if (!res.ok) return null;
  const data = await res.json();
  const entry = data?.[0];
  if (!entry?.text) return null;
  return { def: entry.text.replace(/<[^>]+>/g, '').slice(0, 100), pos: entry.partOfSpeech || null };
} catch { return null; }
}
async function fetchMerriamDef(word) {
if (!API_KEYS.merriam) return null;
try {
  const res = await fetch(
    `https://www.dictionaryapi.com/api/v3/references/collegiate/json/${encodeURIComponent(word)}?key=${API_KEYS.merriam}`,
    { signal: AbortSignal.timeout(4000) }
  );
  if (!res.ok) return null;
  const data = await res.json();
  const entry = data?.[0];
  if (!entry || typeof entry !== 'object' || !entry.shortdef?.length) return null;
  return { def: entry.shortdef[0].slice(0, 100), pos: entry.fl || null };
} catch { return null; }
}
async function augmentLive(type) {
const [dmWords, wnWords] = await Promise.all([
  fetchDatamuse(type),
  fetchWordnikWords(type),
]);
const combined = [...new Set([...dmWords, ...wnWords])];
if (!combined.length) return;
const existing = new Set(WORDS.map(w => w.w.toLowerCase()));
const novel    = combined.filter(w => !existing.has(w));
if (!novel.length) return;
const cap = Math.min(novel.length, 12);
for (let i = 0; i < cap; i += 3) {
const batch   = novel.slice(i, i + 3);
const results = await Promise.all(batch.map(fetchDefinition));
batch.forEach((word, j) => {
const info = results[j];
if (!info) return;
const inferredPos = (type !== 'all' && type !== 'extended' && type !== 'nonenglish')
? type : (info.pos || 'noun');
WORDS.push({
w:        word.charAt(0).toUpperCase() + word.slice(1),
t:        info.pos || inferredPos,
d:        info.def,
diff:     'medium',
borrowed: false,
_live:    true,
});
});
}
}
const MAX_WORDS = 50;
function setCountError(show) {
const err = document.getElementById('count-error');
const inp = document.getElementById(config.countId);
if (err) err.classList.toggle('show', show);
if (inp) inp.classList.toggle('input-error', show);
}
function pick() {
const count = parseInt(document.getElementById(config.countId)?.value) || 10;
const type   = document.getElementById(config.typeId)?.value   || 'all';
const diff   = document.getElementById(config.diffId)?.value   || 'all';
const first  = (document.getElementById(config.firstId)?.value || '').toUpperCase().trim();
const last   = (document.getElementById(config.lastId)?.value  || '').toUpperCase().trim();
let pool = WORDS.filter(w => {
if (type === 'noun'      && w.t !== 'noun')      return false;
if (type === 'adjective' && w.t !== 'adjective') return false;
if (type === 'verb'      && w.t !== 'verb')      return false;
if (type === 'adverb'    && w.t !== 'adverb')    return false;
if (type === 'extended'  && w.diff !== 'hard')   return false;
if (type === 'nonenglish'&& !w.borrowed)         return false;
if (diff !== 'all'       && w.diff !== diff)     return false;
if (first && !w.w.toUpperCase().startsWith(first)) return false;
if (last  && !w.w.toUpperCase().endsWith(last))    return false;
return true;
});
if (!pool.length) pool = WORDS;
const shuffled = [...pool].sort(() => Math.random() - 0.5);
return shuffled.slice(0, Math.min(count, shuffled.length, MAX_WORDS));
}
function render() {
const rawCount = parseInt(document.getElementById(config.countId)?.value, 10);
if (isNaN(rawCount) || rawCount < 1 || rawCount > MAX_WORDS) {
setCountError(true);
return;
}
setCountError(false);
current   = pick();
defsShown = document.getElementById(config.defsId)?.checked !== false;
const list = document.getElementById(config.listId);
if (!list) return;
list.innerHTML = '';
current.forEach((wd, i) => {
const li = document.createElement('li');
li.className = 'word-item';
const isSaved      = saved.some(s => s.w === wd.w);
const showGrammarly = i < 3 && defsShown;
const safeD = wd.d.replace(/'/g, "\\'");
li.innerHTML = `
<div class="word-left">
<div class="word-text">${wd.w}</div>
<div class="word-pos">${wd.t}</div>
${defsShown ? `<div class="word-def">${wd.d}</div>` : ''}
${showGrammarly
? `<div class="word-grammarly"><a href="https://grammarly.com" target="_blank" rel="noopener">Use in a sentence with Grammarly →</a></div>`
: ''}
</div>
<div class="word-right">
<button class="icon-btn" title="Copy" onclick="WORDINEER.copyWord('${wd.w}', this)">
<svg viewBox="0 0 14 14" fill="none">
<rect x="1" y="4" width="9" height="9.5" rx="1.5" stroke="currentColor" stroke-width="1.1"/>
<path d="M4.5 4V2.5A1.5 1.5 0 016 1h5.5A1.5 1.5 0 0113 2.5v7a1.5 1.5 0 01-1.5 1.5H10" stroke="currentColor" stroke-width="1.1"/>
</svg>
</button>
<button class="icon-btn${isSaved ? ' saved' : ''}" title="Save" onclick="WORDINEER.toggleSave('${wd.w}','${wd.t}','${safeD}',this)">
<svg viewBox="0 0 16 16" fill="none">
<path d="M8 13.5S2 9.5 2 5.5A3 3 0 018 4a3 3 0 016 1.5c0 4-6 8-6 8z"
stroke="currentColor" stroke-width="1.3"
fill="${isSaved ? '#E24B4A' : 'none'}"
stroke-linecap="round"/>
</svg>
</button>
</div>`;
list.appendChild(li);
});
const wc = document.getElementById(config.countDisplayId);
if (wc) wc.textContent = current.length + ' word' + (current.length !== 1 ? 's' : '') + ' generated';
}
function toggleSave(word, type, def, btn) {
const idx = saved.findIndex(s => s.w === word);
if (idx >= 0) {
saved.splice(idx, 1);
btn.classList.remove('saved');
btn.querySelector('path').setAttribute('fill', 'none');
} else {
saved.push({ w: word, t: type, d: def });
btn.classList.add('saved');
btn.querySelector('path').setAttribute('fill', '#E24B4A');
}
renderSaved();
}
function renderSaved() {
const el    = document.getElementById('saved-tags');
const cnt   = document.getElementById('saved-count');
const nudge = document.getElementById('aff-nudge');
if (!el) return;
if (cnt) cnt.textContent = '(' + saved.length + ')';
if (!saved.length) {
el.innerHTML = '<span class="saved-empty">Click the heart on any word to save it here</span>';
if (nudge) nudge.classList.remove('show');
return;
}
if (nudge) nudge.classList.add('show');
el.innerHTML = saved.map(s =>
`<span class="saved-tag">${s.w} <span class="saved-tag-remove" onclick="WORDINEER.removeSaved('${s.w}')">×</span></span>`
).join('');
}
function removeSaved(word) {
saved = saved.filter(s => s.w !== word);
renderSaved();
document.querySelectorAll('.icon-btn.saved').forEach(btn => {
const wt = btn.closest('.word-item')?.querySelector('.word-text')?.textContent;
if (wt === word) {
btn.classList.remove('saved');
btn.querySelector('path')?.setAttribute('fill', 'none');
}
});
}
function copyWord(word, btn) {
navigator.clipboard?.writeText(word);
const orig = btn.innerHTML;
btn.innerHTML = `<svg viewBox="0 0 14 14" fill="none"><path d="M2 7l3.5 3.5 6.5-6.5" stroke="#1D9E75" stroke-width="1.3" stroke-linecap="round"/></svg>`;
setTimeout(() => { btn.innerHTML = orig; }, 900);
showToast('Copied: ' + word);
}
function copyAll() {
const words = current.map(w => w.w).join('\n');
navigator.clipboard?.writeText(words);
showToast('All words copied!');
}
function copySaved() {
if (!saved.length) return;
navigator.clipboard?.writeText(saved.map(s => s.w).join(', '));
showToast('Saved words copied!');
}
function showToast(msg) {
const t = document.getElementById('toast');
if (!t) return;
t.textContent = msg;
t.classList.add('show');
setTimeout(() => t.classList.remove('show'), 2000);
}
function reset() {
const ids = [config.countId, config.typeId, config.diffId, config.firstId, config.lastId];
const defaults = ['10', 'all', 'all', '', ''];
ids.forEach((id, i) => {
const el = document.getElementById(id);
if (el) el.value = defaults[i];
});
const defs = document.getElementById(config.defsId);
if (defs) defs.checked = true;
render();
}
function initFaq() {
document.querySelectorAll('.faq-q').forEach(q => {
q.addEventListener('click', () => q.closest('.faq-item').classList.toggle('open'));
});
}
function initMega() {
document.addEventListener('click', e => {
const mega = document.getElementById('mega');
const hbg  = document.querySelector('.hamburger');
if (!mega || !hbg) return;
if (mega.classList.contains('open') && !mega.contains(e.target) && !hbg.contains(e.target)) {
mega.classList.remove('open');
}
});
}
function initSpacebar() {
document.addEventListener('keydown', e => {
if (e.code === 'Space' && !['INPUT','SELECT','TEXTAREA','BUTTON'].includes(e.target.tagName)) {
e.preventDefault();
generate();
}
});
}
function initDefToggle() {
const el = document.getElementById(config.defsId);
if (el) el.addEventListener('change', render);
}
const _render = render;
function generate() {
_render();
const type = document.getElementById(config.typeId)?.value || 'all';
augmentLive(type).catch(() => {});
}
function init(cfg) {
config = {
listId:         cfg.listId         || 'word-list',
countId:        cfg.countId        || 'ctrl-count',
countDisplayId: cfg.countDisplayId || 'word-count',
typeId:         cfg.typeId         || 'ctrl-type',
diffId:         cfg.diffId         || 'ctrl-diff',
firstId:        cfg.firstId        || 'ctrl-first',
lastId:         cfg.lastId         || 'ctrl-last',
defsId:         cfg.defsId         || 'ctrl-defs',
};
if (cfg.apiKeys) {
  API_KEYS.wordnik  = cfg.apiKeys.wordnik  || '';
  API_KEYS.merriam  = cfg.apiKeys.merriam  || '';
}
render();
loadWords().then(() => {
if (current.every(w => SEED.some(s => s.w === w.w))) {
render();
}
}).catch(() => {});
augmentLive('all').catch(() => {});
initFaq();
initMega();
initSpacebar();
initDefToggle();
const countEl = document.getElementById(config.countId);
if (countEl) {
countEl.addEventListener('input', function() {
const v = parseInt(this.value);
if (v >= 1 && v <= MAX_WORDS) setCountError(false);
});
}
}
return { init, render, generate, reset, copyWord, copyAll, copySaved, toggleSave, removeSaved, showToast };
})();
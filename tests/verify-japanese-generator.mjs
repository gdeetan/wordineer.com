import fs from 'node:fs';

const requiredFiles = [
  'wordineer-deploy/data/japanese-names.json',
  'template-deploy/tools-src/random-japanese-name-generator.html',
  'wordineer-deploy/random-japanese-name-generator.html'
];

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

for (const file of requiredFiles) {
  assert(fs.existsSync(file), `Missing required file: ${file}`);
}

const data = JSON.parse(fs.readFileSync('wordineer-deploy/data/japanese-names.json', 'utf8'));
assert(Array.isArray(data.given), 'Data must include given array');
assert(Array.isArray(data.surnames), 'Data must include surnames array');
assert(data.given.length >= 100, 'Need at least 100 Japanese given names');
assert(data.surnames.length >= 100, 'Need at least 100 Japanese surnames');

const genders = new Set(data.given.map((name) => name[3]));
assert(genders.has('m'), 'Need male given names');
assert(genders.has('f'), 'Need female given names');
assert(genders.has('u'), 'Need unisex given names');

for (const name of data.given.slice(0, 20)) {
  assert(name.length >= 7, 'Given names must use compact 7-field schema');
  assert(Array.isArray(name[2]), 'Given name kanji variants must be an array');
  assert(Array.isArray(name[4]), 'Given name styles must be an array');
  assert(Array.isArray(name[5]), 'Given name themes must be an array');
}

for (const name of data.surnames.slice(0, 20)) {
  assert(name.length >= 6, 'Surnames must use compact 6-field schema');
  assert(Array.isArray(name[3]), 'Surname styles must be an array');
  assert(Array.isArray(name[4]), 'Surname themes must be an array');
}

const page = fs.readFileSync('template-deploy/tools-src/random-japanese-name-generator.html', 'utf8');
for (const id of [
  'jp-count',
  'jp-type',
  'jp-gender',
  'jp-style',
  'jp-theme',
  'jp-letter',
  'jp-order',
  'jp-script',
  'jp-mobile-toggle'
]) {
  assert(page.includes(`id="${id}"`), `Missing control id ${id}`);
}

assert(page.includes("fetch('/data/japanese-names.json'"), 'Page must fetch Japanese names JSON');
assert(page.includes('jpRegenerateFromFilters'), 'Page must include live filter regeneration');
assert(page.includes("addEventListener('change', jpRegenerateFromFilters)"), 'Select filters must regenerate on change');
assert(page.includes("addEventListener('input',  jpRegenerateFromFilters)") || page.includes("addEventListener('input', jpRegenerateFromFilters)"), 'Filters must regenerate on input');
assert(page.includes('Random Japanese Name Generator - Real Names &amp; Meanings'), 'Page must include high-CTR title');
assert(page.includes('What Is a Random Japanese Name Generator?'), 'Page must include What Is section');
assert(page.includes('How It Works'), 'Page must include How It Works section');
assert(page.includes('<!-- SLOT:explainer -->'), 'Source page must use explainer slot for below-tools content');
assert(page.includes('<!-- SLOT:faq -->'), 'Source page must include FAQ slot');
assert(page.includes('<!-- SLOT:who -->'), 'Source page must include Who slot');
assert(page.includes('Who uses Wordineer'), 'Page must include Who uses Wordineer section');
assert(page.includes('Frequently asked questions'), 'Page must include FAQ heading');
assert(page.includes('random Filipino name generator'), 'Page must include Filipino cluster keyword');
assert(page.includes('random British name generator'), 'Page must include British cluster keyword');
assert(page.includes('<!-- SLOT:tool -->'), 'Source page must use tool slot');
assert(page.includes('<!-- SLOT:init -->'), 'Source page must use init slot');
assert(page.includes('bindWordineerMenu'), 'Page must bind hamburger menu');
assert(page.includes('.hero--tool .hero-copy p'), 'Page must include mobile rule for hero support copy');
assert(page.includes('#jp-advanced .ctrl-row'), 'Page must include mobile filter grouping rule');

const toolsJson = fs.readFileSync('template-deploy/tools.json', 'utf8');
assert(toolsJson.includes('/random-japanese-name-generator/'), 'tools.json must link Japanese generator');
for (const href of [
  '/random-name-generator/',
  '/random-american-name-generator/',
  '/random-filipino-name-generator/',
  '/random-japanese-name-generator/',
  '/random-british-name-generator/'
]) {
  assert(toolsJson.includes(href), `tools.json must include ${href}`);
}

const builtPage = fs.readFileSync('wordineer-deploy/random-japanese-name-generator.html', 'utf8');
assert(builtPage.includes('id="jp-count"'), 'Built page must include tool controls');
assert(builtPage.includes('id="jp-list"'), 'Built page must include result list');
assert(builtPage.includes("fetch('/data/japanese-names.json'"), 'Built page must include init script');
assert(builtPage.includes('What Is a Random Japanese Name Generator?'), 'Built page must include explainer below tools');
assert(builtPage.includes('Frequently asked questions'), 'Built page must include FAQ');
assert(builtPage.includes('Who uses Wordineer'), 'Built page must include Who section');
assert(builtPage.includes('bindWordineerMenu'), 'Built page must include hamburger binding');

console.log('Japanese generator verification passed');

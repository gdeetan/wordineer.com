import fs from 'node:fs';

const requiredFiles = [
  'wordineer-deploy/data/scottish-names.json',
  'template-deploy/tools-src/random-scottish-name-generator.html',
  'wordineer-deploy/random-scottish-name-generator.html'
];

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

for (const file of requiredFiles) {
  assert(fs.existsSync(file), `Missing required file: ${file}`);
}

const data = JSON.parse(fs.readFileSync('wordineer-deploy/data/scottish-names.json', 'utf8'));
assert(Array.isArray(data.given), 'Data must include given array');
assert(Array.isArray(data.surnames), 'Data must include surnames array');

const page = fs.readFileSync('template-deploy/tools-src/random-scottish-name-generator.html', 'utf8');
for (const id of [
  'sng-count',
  'sng-type',
  'sng-gender',
  'sng-style',
  'sng-theme',
  'sng-letter',
  'sng-popularity',
  'sng-mobile-toggle'
]) {
  assert(page.includes(`id="${id}"`), `Missing control id ${id}`);
}

assert(page.includes("fetch('/data/scottish-names.json'"), 'Page must fetch Scottish names JSON');
assert(page.includes('sngRegenerateFromFilters'), 'Page must include live filter regeneration');
assert(page.includes('What Is a Random Scottish Name Generator?'), 'Page must include What Is section');
assert(page.includes('How It Works'), 'Page must include How It Works section');
assert(page.includes('Who uses Wordineer'), 'Page must include Who section');

const builtPage = fs.readFileSync('wordineer-deploy/random-scottish-name-generator.html', 'utf8');
assert(builtPage.includes('id="sng-count"'), 'Built page must include tool controls');
assert(builtPage.includes('id="sng-list"'), 'Built page must include result list');
assert(builtPage.includes('What Is a Random Scottish Name Generator?'), 'Built page must include explainer below tools');

console.log('Scottish generator verification passed');

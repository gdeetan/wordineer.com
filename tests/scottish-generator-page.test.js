const assert = require('assert');
const fs = require('fs');
const path = require('path');

const root = path.join(__dirname, '..');
const sourcePath = path.join(root, 'template-deploy', 'tools-src', 'random-scottish-name-generator.html');
const deployPath = path.join(root, 'wordineer-deploy', 'random-scottish-name-generator.html');

assert.ok(fs.existsSync(sourcePath), 'source Scottish page should exist');

const source = fs.readFileSync(sourcePath, 'utf8');

function mustInclude(haystack, needle, label) {
  assert.ok(haystack.includes(needle), `${label} should include: ${needle}`);
}

mustInclude(source, 'CONFIG { "url": "/random-scottish-name-generator/"', 'source config');
mustInclude(source, '1,000+ Random Scottish Names - Free Random Scottish Name Generator', 'source title');
mustInclude(source, '/data/scottish-names.json', 'source data fetch path');

for (const id of [
  'sng-count',
  'sng-mobile-toggle',
  'sng-advanced',
  'sng-type',
  'sng-gender',
  'sng-style',
  'sng-theme',
  'sng-letter',
  'sng-popularity',
  'sng-defs',
  'sng-gen-btn',
  'sng-reset-btn',
  'sng-list',
  'sng-saved-tags'
]) {
  mustInclude(source, `id="${id}"`, `${id} control`);
}

mustInclude(source, '<option value="given">Given name only</option>', 'default given-name option');
mustInclude(source, 'What Is a Random Scottish Name Generator?', 'explainer heading');
mustInclude(source, 'How It Works', 'how it works heading');
mustInclude(source, 'Scottish Names: Modern, Gaelic, and Anglicized Forms', 'style explainer');
mustInclude(source, 'class="explainer"', 'explainer wrapper');
mustInclude(source, 'faq-item', 'faq accordion layout');
mustInclude(source, 'uc-grid', 'who uses grid layout');
mustInclude(source, 'Who uses Wordineer', 'who uses heading');
mustInclude(source, '"@type": "FAQPage"', 'FAQ schema');
mustInclude(source, "savedKey: 'wnr_saved_scottish_names'", 'saved key');
mustInclude(source, 'WORDINEER.init(', 'WORDINEER init call');

const filterIds = ['sng-type', 'sng-gender', 'sng-style', 'sng-theme', 'sng-letter', 'sng-popularity'];
for (const id of filterIds) {
  mustInclude(source, `'${id}'`, `${id} referenced in source`);
}

if (fs.existsSync(deployPath)) {
  const deploy = fs.readFileSync(deployPath, 'utf8');
  mustInclude(deploy, '1,000+ Random Scottish Names - Free Random Scottish Name Generator', 'deploy title');
  mustInclude(deploy, '/data/scottish-names.json', 'deploy data fetch path');
  mustInclude(deploy, 'id="sng-count"', 'deploy count control');
  mustInclude(deploy, 'What Is a Random Scottish Name Generator?', 'deploy explainer');
  mustInclude(deploy, 'faq-item', 'deploy faq accordion layout');
  mustInclude(deploy, 'Who uses Wordineer', 'deploy who uses section');
  mustInclude(deploy, 'WORDINEER.init(', 'deploy WORDINEER init');
}

console.log('Scottish generator page static checks ok');

const assert = require('assert');
const fs = require('fs');
const path = require('path');

const file = path.join(__dirname, '..', 'wordineer-deploy', 'data', 'scottish-names.json');
assert.ok(fs.existsSync(file), 'scottish-names.json should exist');

const data = JSON.parse(fs.readFileSync(file, 'utf8'));

assert.ok(Array.isArray(data.given), 'given should be an array');
assert.ok(Array.isArray(data.surnames), 'surnames should be an array');
assert.ok(data.given.length >= 300, `expected at least 300 given names, got ${data.given.length}`);
assert.ok(data.surnames.length >= 200, `expected at least 200 surnames, got ${data.surnames.length}`);

const givenGenders = new Set();
const styleValues = new Set();
const themeValues = new Set();
const popularityValues = new Set();
const originLabelValues = new Set();

for (const item of data.given) {
  assert.strictEqual(typeof item.name, 'string', 'given name must be a string');
  assert.ok(/^\p{Lu}[\p{L}' -]+$/u.test(item.name), `given name should be title case: ${item.name}`);
  assert.ok(['m', 'f', 'u'].includes(item.gender), `invalid gender: ${item.gender}`);
  assert.ok(Array.isArray(item.styles) && item.styles.length > 0, `${item.name} must have styles`);
  assert.ok(Array.isArray(item.themes), `${item.name} must have themes array`);
  assert.strictEqual(typeof item.meaning, 'string', `${item.name} meaning must be a string`);
  assert.ok(item.meaning.length > 0, `${item.name} meaning must not be empty`);
  assert.ok(['common', 'familiar', 'rare'].includes(item.popularity), `invalid popularity: ${item.popularity}`);
  assert.ok(['Gaelic', 'Scots', 'Anglicized', 'Scottish'].includes(item.originLabel), `invalid originLabel: ${item.originLabel}`);
  givenGenders.add(item.gender);
  item.styles.forEach((value) => styleValues.add(value));
  item.themes.forEach((value) => themeValues.add(value));
  popularityValues.add(item.popularity);
  originLabelValues.add(item.originLabel);
}

for (const item of data.surnames) {
  assert.strictEqual(typeof item.name, 'string', 'surname must be a string');
  assert.ok(/^\p{Lu}[\p{L}' -]+$/u.test(item.name), `surname should be title case: ${item.name}`);
  assert.ok(Array.isArray(item.styles) && item.styles.length > 0, `${item.name} must have styles`);
  assert.ok(Array.isArray(item.themes), `${item.name} must have themes array`);
  assert.strictEqual(typeof item.meaning, 'string', `${item.name} meaning must be a string`);
  assert.ok(item.meaning.length > 0, `${item.name} meaning must not be empty`);
  assert.ok(['common', 'familiar', 'rare'].includes(item.popularity), `invalid surname popularity: ${item.popularity}`);
  assert.ok(['Gaelic', 'Scots', 'Anglicized', 'Scottish'].includes(item.originLabel), `invalid surname originLabel: ${item.originLabel}`);
  item.styles.forEach((value) => styleValues.add(value));
  item.themes.forEach((value) => themeValues.add(value));
  popularityValues.add(item.popularity);
  originLabelValues.add(item.originLabel);
}

for (const value of ['m', 'f', 'u']) assert.ok(givenGenders.has(value), `missing gender ${value}`);
for (const value of ['modern', 'traditional-gaelic', 'anglicized', 'classic']) assert.ok(styleValues.has(value), `missing style ${value}`);
for (const value of ['nature', 'strength', 'sea', 'light', 'warrior', 'saintly', 'noble', 'joy']) assert.ok(themeValues.has(value), `missing theme ${value}`);
for (const value of ['common', 'familiar', 'rare']) assert.ok(popularityValues.has(value), `missing popularity ${value}`);
for (const value of ['Gaelic', 'Scots', 'Anglicized', 'Scottish']) assert.ok(originLabelValues.has(value), `missing originLabel ${value}`);

console.log(`scottish-names.json ok: ${data.given.length} given, ${data.surnames.length} surnames`);

const fs = require('fs');
const path = require('path');

function assert(condition, message) {
  if (!condition) {
    throw new Error(message);
  }
}

const root = path.resolve(__dirname, '..');
const pagePath = path.join(root, 'random-german-name-generator.html');
const dataPath = path.join(root, 'data', 'german-names.json');

assert(fs.existsSync(pagePath), 'Missing page: random-german-name-generator.html');
assert(fs.existsSync(dataPath), 'Missing dataset: data/german-names.json');

const html = fs.readFileSync(pagePath, 'utf8');
const data = JSON.parse(fs.readFileSync(dataPath, 'utf8'));

assert(/<h1>1000\+ Random German Names<\/h1>/.test(html), 'Expected German page hero title');
assert(/<select id="de-type">/.test(html), 'Expected name type filter');
assert(/<option value="given" selected>Given name only<\/option>/.test(html), 'Expected given name default');
assert(/<select id="de-surname-category">/.test(html), 'Expected surname category filter');
assert(/What is random German name generator\?/.test(html), 'Expected explainer heading');
assert(/fetch\('\/data\/german-names\.json'/.test(html), 'Expected dedicated German JSON fetch');
assert(/deSyncSurnameCategory\(\)/.test(html), 'Expected surname category sync logic');
assert(/document\.getElementById\('de-mobile-toggle'\)/.test(html), 'Expected mobile options toggle');

assert(Array.isArray(data.given), 'Expected given array');
assert(Array.isArray(data.surnames), 'Expected surnames array');
assert(data.given.length >= 700, 'Expected at least 700 given names');
assert(data.surnames.length >= 250, 'Expected at least 250 surnames');
assert(data.given.length + data.surnames.length >= 1000, 'Expected at least 1000 total names');
assert(data.given.length + data.surnames.length <= 1300, 'Expected no more than 1300 total names');

const sampleGiven = data.given[0];
const sampleSurname = data.surnames[0];
assert(Array.isArray(sampleGiven) && sampleGiven.length >= 5, 'Expected compact given-name tuple format');
assert(Array.isArray(sampleSurname) && sampleSurname.length >= 5, 'Expected compact surname tuple format');

const givenStyles = new Set();
const givenRegions = new Set();
const surnameCategories = new Set();
data.given.forEach(function(entry) {
  assert(typeof entry[0] === 'string' && entry[0], 'Given name missing string name');
  assert(entry[1] === 'm' || entry[1] === 'f', 'Given name gender must be m or f');
  assert(Array.isArray(entry[2]) && entry[2].length, 'Given name missing styles');
  assert(Array.isArray(entry[3]) && entry[3].length, 'Given name missing regions');
  assert(typeof entry[4] === 'string' && entry[4], 'Given name missing meaning');
  entry[2].forEach(function(tag) { givenStyles.add(tag); });
  entry[3].forEach(function(tag) { givenRegions.add(tag); });
});
data.surnames.forEach(function(entry) {
  assert(typeof entry[0] === 'string' && entry[0], 'Surname missing string name');
  assert(Array.isArray(entry[1]) && entry[1].length, 'Surname missing categories');
  assert(Array.isArray(entry[2]) && entry[2].length, 'Surname missing styles');
  assert(Array.isArray(entry[3]) && entry[3].length, 'Surname missing regions');
  assert(typeof entry[4] === 'string' && entry[4], 'Surname missing meaning');
  entry[1].forEach(function(tag) { surnameCategories.add(tag); });
});

['traditional', 'classic', 'modern', 'strong', 'soft', 'elegant'].forEach(function(tag) {
  assert(givenStyles.has(tag), 'Missing style tag in given names: ' + tag);
});
['general', 'bavarian-southern', 'northern', 'austrian-influenced', 'swiss-influenced'].forEach(function(tag) {
  assert(givenRegions.has(tag), 'Missing region tag in given names: ' + tag);
});
['occupational', 'topographic', 'patronymic', 'descriptive'].forEach(function(tag) {
  assert(surnameCategories.has(tag), 'Missing surname category: ' + tag);
});

console.log('German name generator contract checks passed.');

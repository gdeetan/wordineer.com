const fs = require('fs');
const path = require('path');

function assert(condition, message) {
  if (!condition) {
    throw new Error(message);
  }
}

const root = path.resolve(__dirname, '..');
const pagePath = path.join(root, 'random-turkish-name-generator.html');
const dataPath = path.join(root, 'data', 'turkish-names.json');

assert(fs.existsSync(pagePath), 'Missing page: random-turkish-name-generator.html');
assert(fs.existsSync(dataPath), 'Missing dataset: data/turkish-names.json');

const html = fs.readFileSync(pagePath, 'utf8');
const data = JSON.parse(fs.readFileSync(dataPath, 'utf8'));

assert(/<h1>1000\+ Random Turkish Names<\/h1>/.test(html), 'Expected Turkish page hero title');
assert(/<select id="tr-type">/.test(html), 'Expected Turkish name type filter');
assert(/<option value="given" selected>Given name<\/option>/.test(html), 'Expected given-name default');
assert(/<select id="tr-theme">/.test(html), 'Expected meaning theme filter');
assert(/<select id="tr-length">/.test(html), 'Expected length filter');
assert(/What is a random Turkish name generator\?/.test(html), 'Expected explainer heading');
assert(/fetch\('\/data\/turkish-names\.json'/.test(html), 'Expected dedicated Turkish JSON fetch');
assert(/document\.getElementById\('tr-mobile-toggle'\)/.test(html), 'Expected mobile options toggle');

assert(Array.isArray(data.givenNames), 'Expected givenNames array');
assert(Array.isArray(data.surnames), 'Expected surnames array');
assert(data.givenNames.length >= 780, 'Expected at least 780 given names');
assert(data.givenNames.length <= 840, 'Expected no more than 840 given names');
assert(data.surnames.length >= 430, 'Expected at least 430 surnames');
assert(data.surnames.length <= 470, 'Expected no more than 470 surnames');
assert(data.givenNames.length + data.surnames.length >= 1230, 'Expected at least 1230 total names');

const sampleGiven = data.givenNames[0];
const sampleSurname = data.surnames[0];
assert(typeof sampleGiven.latin === 'string' && sampleGiven.latin, 'Given name missing latin value');
assert(sampleGiven.gender === 'm' || sampleGiven.gender === 'f' || sampleGiven.gender === 'u', 'Given name gender must be m, f, or u');
assert(Array.isArray(sampleGiven.themes) && sampleGiven.themes.length, 'Given name missing themes');
assert(typeof sampleGiven.meaning === 'string' && sampleGiven.meaning, 'Given name missing meaning');
assert(sampleGiven.length === 'short' || sampleGiven.length === 'medium' || sampleGiven.length === 'long', 'Given name missing valid length');

assert(typeof sampleSurname.latin === 'string' && sampleSurname.latin, 'Surname missing latin value');
assert(typeof sampleSurname.note === 'string' && sampleSurname.note, 'Surname missing note');
assert(sampleSurname.length === 'short' || sampleSurname.length === 'medium' || sampleSurname.length === 'long', 'Surname missing valid length');

const genders = new Set();
const themes = new Set();
data.givenNames.forEach(function(entry) {
  genders.add(entry.gender);
  entry.themes.forEach(function(tag) { themes.add(tag); });
});
['m', 'f', 'u'].forEach(function(tag) {
  assert(genders.has(tag), 'Missing given-name gender bucket: ' + tag);
});
['nature', 'strength', 'beauty', 'virtue', 'light', 'sky-sea', 'royalty', 'faith'].forEach(function(tag) {
  assert(themes.has(tag), 'Missing meaning theme: ' + tag);
});

console.log('Turkish name generator contract checks passed.');

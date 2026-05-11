import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const testDir = path.dirname(fileURLToPath(import.meta.url));
const repoRoot = path.resolve(testDir, '..');

const paths = {
  data: path.join(repoRoot, 'wordineer-deploy', 'data', 'scottish-names.json'),
  source: path.join(repoRoot, 'template-deploy', 'tools-src', 'random-scottish-name-generator.html'),
  built: path.join(repoRoot, 'wordineer-deploy', 'random-scottish-name-generator.html')
};

function assertFileExists(filePath, label) {
  assert.ok(fs.existsSync(filePath), `${label} should exist: ${path.relative(repoRoot, filePath)}`);
}

function readRequiredFile(filePath, label) {
  assertFileExists(filePath, label);
  return fs.readFileSync(filePath, 'utf8');
}

function mustInclude(html, needle, label) {
  assert.ok(html.includes(needle), `${label} should include: ${needle}`);
}

for (const [label, filePath] of Object.entries(paths)) {
  assertFileExists(filePath, label);
}

// Dedicated page/data tests cover detailed Scottish content and schema.
// This verifier stays at the integration level: required artifacts exist,
// data loads from the dedicated JSON, and core UI wiring survives build output.
const data = JSON.parse(readRequiredFile(paths.data, 'data'));
assert.ok(Array.isArray(data.given), 'data should expose a given array');
assert.ok(Array.isArray(data.surnames), 'data should expose a surnames array');

const source = readRequiredFile(paths.source, 'source page');
const built = readRequiredFile(paths.built, 'built page');

for (const [label, html] of [
  ['source page', source],
  ['built page', built]
]) {
  mustInclude(html, '/data/scottish-names.json', `${label} data wiring`);
  mustInclude(html, 'WORDINEER.init(', `${label} init wiring`);
  mustInclude(html, "savedKey: 'wnr_saved_scottish_names'", `${label} saved-key wiring`);

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
    mustInclude(html, `id="${id}"`, `${label} ${id}`);
  }
}

mustInclude(source, 'sngRegenerateFromFilters', 'source live filter regeneration hook');
mustInclude(source, "addEventListener('change', sngRegenerateFromFilters)", 'source change-event wiring');
assert.ok(
  source.includes("addEventListener('input', sngRegenerateFromFilters)") ||
    source.includes("addEventListener('input',  sngRegenerateFromFilters)"),
  'source input-event wiring should regenerate results'
);
mustInclude(source, 'What Is a Random Scottish Name Generator?', 'source explainer heading');
mustInclude(built, 'What Is a Random Scottish Name Generator?', 'built explainer heading');

console.log('Scottish generator integration verification passed');

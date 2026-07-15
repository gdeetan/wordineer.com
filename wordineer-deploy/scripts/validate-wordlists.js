#!/usr/bin/env node
'use strict';

const fs   = require('fs');
const path = require('path');

const DATA_DIR = path.join(__dirname, '..', '..', 'wordineer-deploy', 'data');

// Pages whose data is a cats-array-per-entry word card format.
// cats: null means "no category filter chips — skip coverage check"
const WORD_FILES = {
  'cool-words.json': {
    cats: ['cool','aesthetic','beautiful','unique','funny','dark','nature','science','vintage']
  },
  'aesthetic-words.json': {
    cats: ['cool','aesthetic','beautiful','unique','dark','nature','science','vintage']
  },
  'beautiful-english-words.json': {
    cats: null  // origin select only — no category chips
  },
  'unique-words-with-meaning.json': {
    cats: ['cool','aesthetic','beautiful','unique','funny','dark','nature','science','vintage']
  }
};

// Pages whose data is flat { w, <filterField> } entries
const CHIP_FILES = {
  'words-to-replace-said.json': {
    filterField: 'tone',
    filters: ['neutral','quiet','loud','questioning','positive','negative','conversational','authoritative']
  },
  'transition-words.json': {
    filterField: 'func',
    filters: ['addition','contrast','cause','sequence','emphasis','example','conclusion']
  }
};

const MIN_COVERAGE = 8;
let errors = 0;
let warnings = 0;

function fail(msg) { console.error('FAIL:', msg); errors++; }
function warn(msg)  { console.warn('WARN:', msg); warnings++; }

function loadJSON(filename) {
  const p = path.join(DATA_DIR, filename);
  try {
    return JSON.parse(fs.readFileSync(p, 'utf8'));
  } catch (e) {
    fail(`Cannot read ${filename}: ${e.message}`);
    return null;
  }
}

// ── Word-card files ──────────────────────────────────────────────────────────

for (const [filename, config] of Object.entries(WORD_FILES)) {
  const data = loadJSON(filename);
  if (!data) continue;

  if (!Array.isArray(data) || !data.length) {
    fail(`${filename}: must be a non-empty array`);
    continue;
  }

  // Required fields
  data.forEach((e, i) => {
    if (!e.w) fail(`${filename}[${i}]: missing 'w'`);
    if (!e.d) fail(`${filename}[${i}]: missing 'd'`);
    if (!Array.isArray(e.cats) || !e.cats.length) fail(`${filename}[${i}] (${e.w}): 'cats' must be a non-empty array`);
  });

  // No duplicate words
  const seen = new Set();
  data.forEach(e => {
    if (seen.has(e.w)) warn(`${filename}: duplicate word '${e.w}'`);
    seen.add(e.w);
  });

  if (config.cats) {
    const catSet = new Set(config.cats);

    // Coverage ≥ MIN_COVERAGE per filter value
    for (const cat of config.cats) {
      const count = data.filter(e => Array.isArray(e.cats) && e.cats.includes(cat)).length;
      if (count < MIN_COVERAGE) fail(`${filename}: '${cat}' has ${count} entries (need ≥${MIN_COVERAGE})`);
    }

    // Orphan tags in data not in FILTERS
    data.forEach((e, i) => {
      if (!Array.isArray(e.cats)) return;
      e.cats.forEach(tag => {
        if (!catSet.has(tag)) warn(`${filename}[${i}] (${e.w}): orphan tag '${tag}' not in FILTERS`);
      });
    });
  }

  console.log(`OK  ${filename} (${data.length} entries)`);
}

// ── Chip files ───────────────────────────────────────────────────────────────

for (const [filename, config] of Object.entries(CHIP_FILES)) {
  const data = loadJSON(filename);
  if (!data) continue;

  if (!Array.isArray(data) || !data.length) {
    fail(`${filename}: must be a non-empty array`);
    continue;
  }

  // Required fields
  data.forEach((e, i) => {
    if (!e.w) fail(`${filename}[${i}]: missing 'w'`);
    if (!e[config.filterField]) fail(`${filename}[${i}] (${e.w}): missing '${config.filterField}'`);
  });

  // Coverage ≥ MIN_COVERAGE per filter value
  const filterSet = new Set(config.filters);
  for (const val of config.filters) {
    const count = data.filter(e => e[config.filterField] === val).length;
    if (count < MIN_COVERAGE) fail(`${filename}: '${val}' has ${count} entries (need ≥${MIN_COVERAGE})`);
  }

  // Orphan filter values
  data.forEach((e, i) => {
    const v = e[config.filterField];
    if (!filterSet.has(v)) warn(`${filename}[${i}] (${e.w}): orphan value '${v}' not in FILTERS`);
  });

  // No duplicate (word, filterValue) pairs — same word can appear in multiple groups
  const seen = new Set();
  data.forEach(e => {
    const key = e.w + '|' + e[config.filterField];
    if (seen.has(key)) warn(`${filename}: duplicate '${e.w}' in group '${e[config.filterField]}'`);
    seen.add(key);
  });

  console.log(`OK  ${filename} (${data.length} entries)`);
}

console.log(`\nvalidate-wordlists: ${errors} error(s), ${warnings} warning(s)`);
process.exit(errors > 0 ? 1 : 0);

#!/usr/bin/env node
// scripts/validate-data.js
// Run: node scripts/validate-data.js
// Validates that every declared filter/tag value in party-game data files
// has at least MIN_COUNT matching entries.

const fs = require('fs');
const path = require('path');

const DATA_DIR = path.join(__dirname, '../wordineer-deploy/data');
const MIN_COUNT = 5;
let errors = 0;

function check(label, items, getTag, tagValues) {
  for (const tag of tagValues) {
    const matches = items.filter(i => getTag(i) === tag);
    if (matches.length < MIN_COUNT) {
      console.error(`FAIL ${label}: tag "${tag}" has only ${matches.length} entries (min ${MIN_COUNT})`);
      errors++;
    } else {
      console.log(`  OK ${label}[${tag}]: ${matches.length} entries`);
    }
  }
}

function load(filename) {
  const fp = path.join(DATA_DIR, filename);
  if (!fs.existsSync(fp)) {
    console.error(`FAIL: ${fp} does not exist`);
    errors++;
    return null;
  }
  try {
    return JSON.parse(fs.readFileSync(fp, 'utf8'));
  } catch (e) {
    console.error(`FAIL: ${fp} has invalid JSON: ${e.message}`);
    errors++;
    return null;
  }
}

// --- scattergories.json ---
console.log('\n=== scattergories.json ===');
const sc = load('scattergories.json');
if (sc) {
  if (!Array.isArray(sc.lists) || sc.lists.length < 12) {
    console.error(`FAIL scattergories: need 12 lists, found ${sc.lists?.length ?? 0}`);
    errors++;
  } else {
    console.log(`  OK lists: ${sc.lists.length} (each has ${sc.lists.map(l=>l.length).join(',')} categories)`);
  }
  const badLists = sc.lists.filter(l => !Array.isArray(l));
  if (badLists.length > 0) {
    console.error(`FAIL scattergories: ${badLists.length} list(s) are not arrays`);
    errors++;
  }
  const themes = ['classic','kids','adults','holiday','food','pop-culture','hard'];
  for (const t of themes) {
    const cats = (sc.pool || {})[t] || [];
    if (cats.length < 10) {
      console.error(`FAIL scattergories pool[${t}]: only ${cats.length} categories (need 10+)`);
      errors++;
    } else {
      console.log(`  OK pool[${t}]: ${cats.length} categories`);
    }
  }
}

// --- catchphrase.json ---
console.log('\n=== catchphrase.json ===');
const cp = load('catchphrase.json');
if (cp) {
  const badEntries = cp.filter(item => !item.category || !item.difficulty);
  if (badEntries.length > 0) {
    console.error(`FAIL catchphrase: ${badEntries.length} entries missing category or difficulty`);
    errors++;
  }
  const categories = ['everyday','actions','places','people','food','entertainment','idioms','hard'];
  const difficulties = ['easy','medium','hard'];
  check('catchphrase category', cp, i => i.category, categories);
  check('catchphrase difficulty', cp, i => i.difficulty, difficulties);
  console.log(`  Total entries: ${cp.length}`);
  if (cp.length < 400) {
    console.error(`FAIL catchphrase: only ${cp.length} entries (need 400+)`);
    errors++;
  }
}

// --- couples-truth-or-dare.json ---
console.log('\n=== couples-truth-or-dare.json ===');
const ctd = load('couples-truth-or-dare.json');
if (ctd) {
  const intensities = ['sweet','fun','romantic','spicy'];
  for (const intensity of intensities) {
    const group = (ctd[intensity] || {});
    const truths = Array.isArray(group.truth) ? group.truth : [];
    const dares = Array.isArray(group.dare) ? group.dare : [];
    if (truths.length < MIN_COUNT) {
      console.error(`FAIL couples[${intensity}].truth: only ${truths.length} (need ${MIN_COUNT}+)`);
      errors++;
    } else {
      console.log(`  OK couples[${intensity}].truth: ${truths.length}`);
    }
    if (dares.length < MIN_COUNT) {
      console.error(`FAIL couples[${intensity}].dare: only ${dares.length} (need ${MIN_COUNT}+)`);
      errors++;
    } else {
      console.log(`  OK couples[${intensity}].dare: ${dares.length}`);
    }
  }
}

// --- writing-prompts.json ---
console.log('\n=== writing-prompts.json ===');
const wp = load('writing-prompts.json');
if (wp) {
  const types = ['story-starter','journal','dialogue','first-line','what-if','poetry'];
  const genres = ['general','fantasy','scifi','romance','mystery','horror','literary'];
  const audiences = ['adults','teens','kids'];
  const lengths = ['quick','deep'];
  check('wp type', wp, i => i.type, types);
  check('wp genre', wp, i => i.genre, genres);
  check('wp audience', wp, i => i.audience, audiences);
  check('wp length', wp, i => i.length, lengths);
  console.log(`  Total prompts: ${wp.length}`);
  if (wp.length < 300) {
    console.error(`FAIL writing-prompts: only ${wp.length} entries (need 300+)`);
    errors++;
  }
}

// --- plot-generator.json ---
console.log('\n=== plot-generator.json ===');
const pg = load('plot-generator.json');
if (pg) {
  const genres = ['fantasy','scifi','mystery','romance','thriller','literary','comedy'];
  const components = ['protagonists','settings','conflicts','complications','twists','themes'];
  for (const comp of components) {
    const items = pg[comp] || [];
    if (items.length < 10) {
      console.error(`FAIL plot[${comp}]: only ${items.length} entries (need 10+)`);
      errors++;
    } else {
      console.log(`  OK plot[${comp}]: ${items.length} entries`);
    }
    // Check genre tags
    check(`plot[${comp}] genre`, items, i => i.genre, genres);
  }
  // Validate template assembly: try 10 random assemblies
  const templates = pg.templates || [];
  if (templates.length < 4) {
    console.error(`FAIL plot templates: only ${templates.length} (need 4+)`);
    errors++;
  } else {
    console.log(`  OK templates: ${templates.length}`);
    // Print 3 sample assemblies for human review
    console.log('\n  --- Sample plot assemblies ---');
    for (let i = 0; i < 3; i++) {
      const pick = arr => arr[Math.floor(Math.random() * arr.length)];
      const t = templates[Math.floor(Math.random() * templates.length)];
      const result = t
        .replace('{protagonist}', pick(pg.protagonists || []).text || '?')
        .replace('{setting}', pick(pg.settings || []).text || '?')
        .replace('{conflict}', pick(pg.conflicts || []).text || '?')
        .replace('{complication}', pick(pg.complications || []).text || '?')
        .replace('{twist}', pick(pg.twists || []).text || '?');
      console.log(`  ${i + 1}. ${result}\n`);
    }
  }
}

console.log(`\n${errors === 0 ? '✓ All checks passed' : `✗ ${errors} error(s) found`}`);
process.exit(errors > 0 ? 1 : 0);

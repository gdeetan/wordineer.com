import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const DATA_PATH = path.join(ROOT, 'wordineer-deploy', 'data', 'korean-names.json');
const TARGET_GIVEN = 1400;

const leadChunks = [
  { r: 'min', h: '민', g: ['m', 'u'], s: ['modern', 'strong', 'kdrama'], t: ['wisdom', 'strength'], m: 'clever' },
  { r: 'seo', h: '서', g: ['f', 'u'], s: ['modern', 'elegant', 'kdrama'], t: ['wisdom', 'beauty'], m: 'auspicious' },
  { r: 'ji', h: '지', g: ['u'], s: ['modern', 'classic', 'kdrama'], t: ['wisdom', 'virtue'], m: 'wise' },
  { r: 'hye', h: '혜', g: ['f', 'u'], s: ['classic', 'soft'], t: ['wisdom', 'beauty'], m: 'bright' },
  { r: 'hyun', h: '현', g: ['m', 'u'], s: ['classic', 'strong'], t: ['virtue', 'strength'], m: 'virtuous' },
  { r: 'tae', h: '태', g: ['m', 'u'], s: ['modern', 'strong'], t: ['light', 'strength'], m: 'great' },
  { r: 'do', h: '도', g: ['m', 'u'], s: ['modern', 'gentle'], t: ['virtue', 'peace'], m: 'path' },
  { r: 'jun', h: '준', g: ['m', 'u'], s: ['modern', 'classic', 'kdrama'], t: ['wisdom', 'strength'], m: 'talented' },
  { r: 'jae', h: '재', g: ['m', 'u'], s: ['modern', 'strong'], t: ['wisdom', 'strength'], m: 'talent' },
  { r: 'woo', h: '우', g: ['m', 'u'], s: ['modern', 'classic'], t: ['peace', 'virtue'], m: 'friend' },
  { r: 'yoon', h: '윤', g: ['u'], s: ['classic', 'modern'], t: ['virtue', 'leadership'], m: 'govern' },
  { r: 'ye', h: '예', g: ['f', 'u'], s: ['modern', 'elegant', 'kdrama'], t: ['wisdom', 'beauty'], m: 'artful' },
  { r: 'yeo', h: '여', g: ['f', 'u'], s: ['classic', 'soft'], t: ['beauty', 'peace'], m: 'beautiful' },
  { r: 'na', h: '나', g: ['f', 'u'], s: ['traditional', 'soft'], t: ['beauty', 'peace'], m: 'gentle' },
  { r: 'hae', h: '해', g: ['u'], s: ['modern', 'soft', 'kdrama'], t: ['light', 'nature'], m: 'sun' },
  { r: 'bo', h: '보', g: ['f', 'u'], s: ['modern', 'elegant'], t: ['beauty', 'virtue'], m: 'treasure' },
  { r: 'chae', h: '채', g: ['f', 'u'], s: ['modern', 'elegant', 'kdrama'], t: ['flower', 'beauty'], m: 'color' },
  { r: 'rin', h: '린', g: ['f', 'u'], s: ['modern', 'elegant'], t: ['light', 'beauty'], m: 'refined' },
  { r: 'mi', h: '미', g: ['f', 'u'], s: ['classic', 'soft'], t: ['beauty', 'peace'], m: 'beauty' },
  { r: 'so', h: '소', g: ['f', 'u'], s: ['modern', 'soft'], t: ['peace', 'beauty'], m: 'bright' },
  { r: 'seung', h: '승', g: ['m', 'u'], s: ['classic', 'strong'], t: ['strength', 'virtue'], m: 'victory' },
  { r: 'sang', h: '상', g: ['m', 'u'], s: ['classic', 'strong'], t: ['strength', 'virtue'], m: 'high' },
  { r: 'dong', h: '동', g: ['m', 'u'], s: ['classic', 'strong'], t: ['nature', 'virtue'], m: 'east' },
  { r: 'dae', h: '대', g: ['m', 'u'], s: ['classic', 'strong'], t: ['strength', 'virtue'], m: 'great' },
  { r: 'kyung', h: '경', g: ['u'], s: ['classic'], t: ['wisdom', 'virtue'], m: 'respect' },
  { r: 'a', h: '아', g: ['f', 'u'], s: ['modern', 'soft'], t: ['beauty', 'peace'], m: 'grace' },
  { r: 'ri', h: '리', g: ['f', 'u'], s: ['modern', 'soft'], t: ['beauty', 'peace'], m: 'beauty' },
  { r: 'sun', h: '선', g: ['u'], s: ['classic'], t: ['virtue', 'peace'], m: 'good' },
  { r: 'jin', h: '진', g: ['u'], s: ['classic', 'modern'], t: ['wisdom', 'virtue'], m: 'precious' },
  { r: 'eun', h: '은', g: ['u'], s: ['classic', 'soft'], t: ['peace', 'virtue'], m: 'kindness' },
  { r: 'ga', h: '가', g: ['f', 'u'], s: ['modern', 'soft'], t: ['beauty', 'peace'], m: 'beautiful' },
  { r: 'ra', h: '라', g: ['f', 'u'], s: ['modern', 'soft'], t: ['beauty', 'peace'], m: 'graceful' },
  { r: 'hyo', h: '효', g: ['f', 'u'], s: ['classic', 'soft'], t: ['virtue', 'beauty'], m: 'filial' },
  { r: 'seol', h: '설', g: ['f', 'u'], s: ['traditional', 'soft'], t: ['winter', 'beauty'], m: 'snow' },
  { r: 'yul', h: '율', g: ['u'], s: ['modern', 'classic'], t: ['time', 'virtue'], m: 'rhythm' },
  { r: 'si', h: '시', g: ['u'], s: ['classic'], t: ['wisdom', 'virtue'], m: 'poem' },
  { r: 'gyu', h: '규', g: ['m', 'u'], s: ['classic'], t: ['wisdom', 'virtue'], m: 'standard' },
  { r: 'chan', h: '찬', g: ['m', 'u'], s: ['modern', 'classic', 'kdrama'], t: ['strength', 'virtue'], m: 'praise' },
  { r: 'sung', h: '성', g: ['m', 'u'], s: ['classic', 'strong'], t: ['strength', 'virtue'], m: 'achievement' },
  { r: 'young', h: '영', g: ['u'], s: ['modern', 'classic'], t: ['light', 'wisdom'], m: 'bright' }
];

const tailChunks = [
  { r: 'ho', h: '호', g: ['m', 'u'], s: ['modern', 'strong'], t: ['strength', 'wisdom'], m: 'great' },
  { r: 'jun', h: '준', g: ['m', 'u'], s: ['modern', 'classic', 'kdrama'], t: ['wisdom', 'strength'], m: 'talented' },
  { r: 'woo', h: '우', g: ['m', 'u'], s: ['modern', 'classic'], t: ['peace', 'virtue'], m: 'friend' },
  { r: 'min', h: '민', g: ['m', 'u'], s: ['modern', 'strong', 'kdrama'], t: ['wisdom', 'strength'], m: 'clever' },
  { r: 'hyun', h: '현', g: ['m', 'u'], s: ['classic', 'strong'], t: ['virtue', 'strength'], m: 'virtuous' },
  { r: 'bin', h: '빈', g: ['m', 'u'], s: ['modern', 'elegant'], t: ['beauty', 'virtue'], m: 'refined' },
  { r: 'seok', h: '석', g: ['m', 'u'], s: ['classic'], t: ['strength', 'virtue'], m: 'stone' },
  { r: 'jin', h: '진', g: ['u'], s: ['classic', 'modern'], t: ['wisdom', 'virtue'], m: 'precious' },
  { r: 'young', h: '영', g: ['u'], s: ['modern', 'classic'], t: ['light', 'wisdom'], m: 'bright' },
  { r: 'yoon', h: '윤', g: ['u'], s: ['classic', 'modern'], t: ['virtue', 'leadership'], m: 'govern' },
  { r: 'yul', h: '율', g: ['u'], s: ['modern', 'classic'], t: ['time', 'virtue'], m: 'rhythm' },
  { r: 'yeon', h: '연', g: ['f', 'u'], s: ['modern', 'elegant', 'kdrama'], t: ['beauty', 'virtue'], m: 'graceful' },
  { r: 'eun', h: '은', g: ['u'], s: ['classic', 'soft'], t: ['peace', 'virtue'], m: 'kindness' },
  { r: 'ah', h: '아', g: ['f', 'u'], s: ['modern', 'soft'], t: ['beauty', 'peace'], m: 'grace' },
  { r: 'na', h: '나', g: ['f', 'u'], s: ['traditional', 'soft'], t: ['beauty', 'peace'], m: 'gentle' },
  { r: 'ri', h: '리', g: ['f', 'u'], s: ['modern', 'soft'], t: ['beauty', 'peace'], m: 'beauty' },
  { r: 'ra', h: '라', g: ['f', 'u'], s: ['modern', 'soft'], t: ['beauty', 'peace'], m: 'graceful' },
  { r: 'mi', h: '미', g: ['f', 'u'], s: ['classic', 'soft'], t: ['beauty', 'peace'], m: 'beauty' },
  { r: 'kyung', h: '경', g: ['u'], s: ['classic'], t: ['wisdom', 'virtue'], m: 'respect' },
  { r: 'kyu', h: '규', g: ['m', 'u'], s: ['classic'], t: ['wisdom', 'virtue'], m: 'standard' },
  { r: 'sung', h: '성', g: ['m', 'u'], s: ['classic', 'strong'], t: ['strength', 'virtue'], m: 'achievement' },
  { r: 'han', h: '한', g: ['u'], s: ['classic'], t: ['greatness', 'unity'], m: 'one' },
  { r: 'sol', h: '솔', g: ['u'], s: ['traditional', 'soft'], t: ['nature', 'beauty'], m: 'pine' },
  { r: 'hwa', h: '화', g: ['f', 'u'], s: ['traditional', 'elegant'], t: ['flower', 'beauty'], m: 'flower' },
  { r: 'hye', h: '혜', g: ['f', 'u'], s: ['classic', 'soft'], t: ['wisdom', 'beauty'], m: 'bright' },
  { r: 'dam', h: '담', g: ['u'], s: ['modern', 'soft'], t: ['peace', 'virtue'], m: 'calm' },
  { r: 'seo', h: '서', g: ['f', 'u'], s: ['modern', 'elegant', 'kdrama'], t: ['wisdom', 'beauty'], m: 'auspicious' },
  { r: 'so', h: '소', g: ['f', 'u'], s: ['modern', 'soft'], t: ['peace', 'beauty'], m: 'bright' },
  { r: 'ji', h: '지', g: ['u'], s: ['modern', 'classic', 'kdrama'], t: ['wisdom', 'virtue'], m: 'wise' },
  { r: 'ae', h: '애', g: ['f', 'u'], s: ['modern', 'soft'], t: ['beauty', 'peace'], m: 'love' },
  { r: 'chan', h: '찬', g: ['m', 'u'], s: ['modern', 'classic', 'kdrama'], t: ['strength', 'virtue'], m: 'praise' },
  { r: 'beom', h: '범', g: ['m', 'u'], s: ['classic', 'strong'], t: ['strength', 'nature'], m: 'tiger' },
  { r: 'hwan', h: '환', g: ['m', 'u'], s: ['classic', 'strong'], t: ['light', 'strength'], m: 'brilliant' },
  { r: 'geun', h: '근', g: ['m', 'u'], s: ['classic'], t: ['virtue', 'strength'], m: 'root' },
  { r: 'gyeom', h: '겸', g: ['u'], s: ['classic'], t: ['virtue', 'wisdom'], m: 'modesty' },
  { r: 'ro', h: '로', g: ['u'], s: ['modern', 'classic'], t: ['path', 'wisdom'], m: 'road' },
  { r: 'hae', h: '해', g: ['u'], s: ['modern', 'soft', 'kdrama'], t: ['light', 'nature'], m: 'sun' },
  { r: 'da', h: '다', g: ['u'], s: ['modern', 'soft'], t: ['peace', 'virtue'], m: 'all' },
  { r: 'won', h: '원', g: ['u'], s: ['modern', 'classic'], t: ['virtue', 'origin'], m: 'origin' },
  { r: 'si', h: '시', g: ['u'], s: ['classic'], t: ['wisdom', 'virtue'], m: 'poem' }
];

function uniq(arr) {
  return [...new Set(arr)];
}

function intersect(a, b) {
  const setB = new Set(b);
  return a.filter((x) => setB.has(x));
}

function makeName(prefix, suffix) {
  const roman = (prefix.r + suffix.r).replace(/(^|[-'\s])([a-z])/g, (_, p1, p2) => p1 + p2.toUpperCase());
  const display = roman.charAt(0).toUpperCase() + roman.slice(1);
  const hangul = prefix.h + suffix.h;
  const genderHit = intersect(prefix.g, suffix.g);
  const gender = genderHit.includes('m') && !genderHit.includes('f') ? 'm'
    : genderHit.includes('f') && !genderHit.includes('m') ? 'f'
      : genderHit.includes('m') && genderHit.includes('f') ? 'u'
        : 'u';
  const styles = uniq([...prefix.s, ...suffix.s]);
  const themes = uniq([...prefix.t, ...suffix.t]);
  if ((styles.includes('modern') && styles.includes('elegant')) || styles.includes('kdrama')) {
    if (!styles.includes('kdrama')) styles.push('kdrama');
  }
  return [
    display,
    hangul,
    gender,
    styles,
    themes,
    `${prefix.m} and ${suffix.m}`
  ];
}

function main() {
  const raw = JSON.parse(fs.readFileSync(DATA_PATH, 'utf8'));
  const existing = Array.isArray(raw.given) ? raw.given.slice() : [];
  const seen = new Set(existing.map((x) => `${x[0].toLowerCase()}|${x[1]}`));

  const generated = [];
  for (const prefix of leadChunks) {
    for (const suffix of tailChunks) {
      if (generated.length + existing.length >= TARGET_GIVEN) break;
      if (prefix.r === suffix.r) continue;
      const entry = makeName(prefix, suffix);
      const key = `${entry[0].toLowerCase()}|${entry[1]}`;
      if (seen.has(key)) continue;
      seen.add(key);
      generated.push(entry);
    }
    if (generated.length + existing.length >= TARGET_GIVEN) break;
  }

  if (existing.length + generated.length < TARGET_GIVEN) {
    throw new Error(`Unable to reach ${TARGET_GIVEN} given names; got ${existing.length + generated.length}`);
  }

  raw.given = existing.concat(generated.slice(0, TARGET_GIVEN - existing.length));
  fs.writeFileSync(DATA_PATH, JSON.stringify(raw, null, 2) + '\n');
  console.log(`Wrote ${raw.given.length} Korean given names to ${DATA_PATH}`);
}

main();

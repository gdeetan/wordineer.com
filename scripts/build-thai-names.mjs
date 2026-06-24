import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const DATA_PATH = path.join(ROOT, 'wordineer-deploy', 'data', 'thai-names.json');
const TARGETS = {
  given: 700,
  surnames: 200,
  nicknames: 100,
};

const givenLead = [
  { r: 'Than', h: 'ธน', g: ['m', 'u'], s: ['common', 'modern'], t: ['fortune'], m: 'wealth' },
  { r: 'Kitti', h: 'กิตติ', g: ['m'], s: ['traditional', 'common'], t: ['strength', 'virtue'], m: 'honor' },
  { r: 'Naphat', h: 'นภัส', g: ['m', 'f', 'u'], s: ['modern'], t: ['beauty', 'nature'], m: 'radiant sky' },
  { r: 'Phat', h: 'ภัทร', g: ['m', 'f', 'u'], s: ['common', 'modern'], t: ['fortune', 'virtue'], m: 'auspicious' },
  { r: 'Siri', h: 'สิริ', g: ['f', 'u'], s: ['common', 'elegant'], t: ['fortune', 'beauty'], m: 'glory' },
  { r: 'Wara', h: 'วรา', g: ['f', 'u'], s: ['modern', 'elegant'], t: ['beauty', 'virtue'], m: 'excellent' },
  { r: 'Chai', h: 'ชัย', g: ['m'], s: ['common', 'strong'], t: ['strength'], m: 'victory' },
  { r: 'Anan', h: 'อนันต์', g: ['m', 'u'], s: ['traditional'], t: ['virtue'], m: 'endless' },
  { r: 'Arun', h: 'อรุณ', g: ['m'], s: ['traditional'], t: ['nature'], m: 'dawn' },
  { r: 'Dara', h: 'ดารา', g: ['f'], s: ['common', 'soft'], t: ['beauty'], m: 'star' },
  { r: 'Kanya', h: 'กัญญา', g: ['f'], s: ['common', 'soft'], t: ['beauty'], m: 'maiden' },
  { r: 'Chon', h: 'ชล', g: ['f', 'u'], s: ['common', 'soft'], t: ['nature'], m: 'water' },
  { r: 'Rawi', h: 'รวิ', g: ['m', 'u'], s: ['modern'], t: ['nature', 'light'], m: 'sun' },
  { r: 'Manat', h: 'มนัส', g: ['u'], s: ['traditional'], t: ['virtue'], m: 'mind' },
  { r: 'Supha', h: 'สุภ', g: ['u'], s: ['common', 'modern'], t: ['virtue', 'fortune'], m: 'excellent' },
  { r: 'Phim', h: 'พิมพ์', g: ['f'], s: ['modern', 'soft'], t: ['beauty'], m: 'pattern' },
  { r: 'Bunya', h: 'บุญญา', g: ['f', 'u'], s: ['traditional'], t: ['fortune', 'virtue'], m: 'merit' },
  { r: 'Athi', h: 'อธิ', g: ['m'], s: ['modern', 'strong'], t: ['strength'], m: 'leader' },
  { r: 'Phu', h: 'ภู', g: ['m', 'u'], s: ['traditional', 'modern'], t: ['nature', 'strength'], m: 'earth' },
  { r: 'Udom', h: 'อุดม', g: ['u'], s: ['traditional'], t: ['fortune'], m: 'abundance' },
  { r: 'Kriang', h: 'เกรียง', g: ['m', 'u'], s: ['traditional'], t: ['strength'], m: 'fame' },
  { r: 'Rung', h: 'รุ่ง', g: ['f', 'u'], s: ['modern', 'soft'], t: ['light', 'nature'], m: 'bright' },
  { r: 'Chaya', h: 'ชยา', g: ['f', 'u'], s: ['modern'], t: ['strength', 'beauty'], m: 'victory' },
  { r: 'Nari', h: 'นริ', g: ['f', 'u'], s: ['modern'], t: ['beauty', 'virtue'], m: 'noble' },
  { r: 'Mali', h: 'มาลี', g: ['f'], s: ['traditional', 'soft'], t: ['nature', 'beauty'], m: 'flower' },
  { r: 'Thida', h: 'ธิดา', g: ['f'], s: ['traditional'], t: ['beauty'], m: 'daughter' },
  { r: 'Watana', h: 'วัฒนา', g: ['u'], s: ['modern'], t: ['fortune'], m: 'progress' },
  { r: 'Yot', h: 'ยศ', g: ['m'], s: ['traditional', 'strong'], t: ['strength'], m: 'rank' },
  { r: 'Chira', h: 'จิรา', g: ['f', 'u'], s: ['modern'], t: ['beauty', 'virtue'], m: 'lasting' },
  { r: 'Suphat', h: 'สุภัทร', g: ['m', 'u'], s: ['common', 'modern'], t: ['virtue', 'fortune'], m: 'excellent' },
  { r: 'Narin', h: 'นรินทร์', g: ['m', 'u'], s: ['traditional'], t: ['virtue', 'strength'], m: 'noble ruler' },
  { r: 'Aphich', h: 'อภิช', g: ['m', 'u'], s: ['modern'], t: ['virtue'], m: 'superior' },
  { r: 'Sathi', h: 'สถิ', g: ['u'], s: ['traditional'], t: ['virtue'], m: 'stable' },
  { r: 'Ratt', h: 'รัต', g: ['f', 'u'], s: ['modern', 'soft'], t: ['beauty'], m: 'jewel' },
  { r: 'Piya', h: 'ปิยะ', g: ['m', 'f', 'u'], s: ['common', 'soft'], t: ['beauty', 'virtue'], m: 'beloved' },
  { r: 'Kamon', h: 'กมล', g: ['u'], s: ['traditional', 'soft'], t: ['virtue'], m: 'heart' },
  { r: 'Suk', h: 'สุข', g: ['u'], s: ['traditional', 'common'], t: ['fortune'], m: 'happiness' },
  { r: 'Phrom', h: 'พรหม', g: ['m', 'u'], s: ['traditional'], t: ['virtue', 'fortune'], m: 'divine' },
  { r: 'Sak', h: 'ศัก', g: ['m'], s: ['common', 'strong'], t: ['strength'], m: 'power' },
];

const givenTail = [
  { r: 'korn', h: 'กรณ์', g: ['m', 'u'], s: ['traditional', 'strong'], t: ['strength'], m: 'action' },
  { r: 'chai', h: 'ชัย', g: ['m'], s: ['common', 'strong'], t: ['strength'], m: 'victory' },
  { r: 'wat', h: 'วัฒน์', g: ['m', 'u'], s: ['modern'], t: ['fortune'], m: 'growth' },
  { r: 'wut', h: 'วุฒิ', g: ['m'], s: ['traditional', 'strong'], t: ['wisdom'], m: 'wisdom' },
  { r: 'phat', h: 'ภัทร', g: ['m', 'f', 'u'], s: ['common', 'modern'], t: ['fortune', 'virtue'], m: 'auspicious' },
  { r: 'porn', h: 'พร', g: ['f', 'u'], s: ['traditional', 'soft'], t: ['fortune', 'virtue'], m: 'blessing' },
  { r: 'thida', h: 'ธิดา', g: ['f'], s: ['traditional'], t: ['beauty'], m: 'daughter' },
  { r: 'nuch', h: 'นุช', g: ['f'], s: ['soft', 'common'], t: ['beauty'], m: 'beloved woman' },
  { r: 'rat', h: 'รัตน์', g: ['f', 'u'], s: ['modern', 'soft'], t: ['beauty', 'fortune'], m: 'jewel' },
  { r: 'sorn', h: 'สรณ์', g: ['u'], s: ['traditional'], t: ['virtue'], m: 'refuge' },
  { r: 'yot', h: 'ยศ', g: ['m'], s: ['traditional', 'strong'], t: ['strength'], m: 'rank' },
  { r: 'phop', h: 'ภพ', g: ['m', 'u'], s: ['traditional'], t: ['virtue', 'strength'], m: 'world' },
  { r: 'sak', h: 'ศักดิ์', g: ['m'], s: ['common', 'strong'], t: ['strength'], m: 'power' },
  { r: 'sri', h: 'ศรี', g: ['f', 'u'], s: ['common', 'elegant'], t: ['beauty', 'virtue'], m: 'glory' },
  { r: 'nara', h: 'นรา', g: ['u'], s: ['modern'], t: ['virtue'], m: 'person' },
  { r: 'da', h: 'ดา', g: ['f'], s: ['soft', 'common'], t: ['beauty'], m: 'graceful' },
  { r: 'mai', h: 'ใหม่', g: ['u'], s: ['modern'], t: ['fortune'], m: 'new' },
  { r: 'phon', h: 'พล', g: ['m'], s: ['common', 'strong'], t: ['strength'], m: 'strength' },
  { r: 'wadee', h: 'วดี', g: ['f'], s: ['traditional', 'soft'], t: ['beauty'], m: 'beautiful' },
  { r: 'napa', h: 'นภา', g: ['f', 'u'], s: ['modern', 'soft'], t: ['nature', 'beauty'], m: 'sky' },
  { r: 'rak', h: 'รัก', g: ['u'], s: ['soft', 'modern'], t: ['beauty'], m: 'love' },
  { r: 'phana', h: 'พนา', g: ['u'], s: ['traditional'], t: ['nature'], m: 'forest' },
  { r: 'chana', h: 'ชนะ', g: ['m'], s: ['strong', 'modern'], t: ['strength'], m: 'victory' },
  { r: 'phan', h: 'พัน', g: ['u'], s: ['traditional'], t: ['virtue'], m: 'lineage' },
  { r: 'chaiyot', h: 'ไชยยศ', g: ['m'], s: ['strong', 'traditional'], t: ['strength'], m: 'victorious rank' },
  { r: 'prasit', h: 'ประสิทธิ์', g: ['m', 'u'], s: ['traditional'], t: ['virtue'], m: 'accomplishment' },
  { r: 'pong', h: 'พงศ์', g: ['m'], s: ['traditional', 'common'], t: ['strength', 'virtue'], m: 'lineage' },
  { r: 'ruang', h: 'เรือง', g: ['u'], s: ['modern'], t: ['fortune'], m: 'shine' },
  { r: 'sakdi', h: 'ศักดิ์', g: ['m'], s: ['strong', 'common'], t: ['strength'], m: 'power' },
  { r: 'thong', h: 'ทอง', g: ['u'], s: ['common'], t: ['fortune'], m: 'gold' },
  { r: 'kham', h: 'คำ', g: ['u'], s: ['common'], t: ['fortune', 'beauty'], m: 'word; gold' },
  { r: 'sakul', h: 'สกุล', g: ['u'], s: ['traditional'], t: ['virtue'], m: 'family' },
  { r: 'yuen', h: 'ยืน', g: ['u'], s: ['traditional'], t: ['virtue'], m: 'enduring' },
  { r: 'dee', h: 'ดี', g: ['u'], s: ['common', 'soft'], t: ['virtue'], m: 'good' },
  { r: 'phijit', h: 'พิชิต', g: ['m'], s: ['strong', 'modern'], t: ['strength'], m: 'conquer' },
  { r: 'amnuay', h: 'อำนวย', g: ['u'], s: ['modern'], t: ['fortune'], m: 'support' },
  { r: 'chok', h: 'โชค', g: ['u'], s: ['common'], t: ['fortune'], m: 'luck' },
  { r: 'setth', h: 'เศรษฐ', g: ['u'], s: ['traditional'], t: ['fortune'], m: 'wealth' },
  { r: 'rung', h: 'รุ่ง', g: ['f', 'u'], s: ['soft', 'modern'], t: ['nature', 'light'], m: 'bright' },
];

const surnameLead = [
  { r: 'Charoen', h: 'เจริญ', s: ['common', 'traditional'], l: 'shorter', m: 'prosperity' },
  { r: 'Than', h: 'ธน', s: ['modern'], l: 'shorter', m: 'wealth' },
  { r: 'Rattan', h: 'รัตน', s: ['common', 'traditional'], l: 'distinctive', m: 'jewel' },
  { r: 'Wong', h: 'วงศ์', s: ['common', 'traditional'], l: 'shorter', m: 'lineage' },
  { r: 'Suwan', h: 'สุวรรณ', s: ['common', 'traditional'], l: 'distinctive', m: 'gold' },
  { r: 'Mongkol', h: 'มงคล', s: ['common', 'traditional'], l: 'shorter', m: 'auspicious' },
  { r: 'Udom', h: 'อุดม', s: ['traditional'], l: 'shorter', m: 'abundance' },
  { r: 'Kasem', h: 'เกษม', s: ['traditional'], l: 'shorter', m: 'joy' },
  { r: 'Saeng', h: 'แสง', s: ['common'], l: 'shorter', m: 'light' },
  { r: 'Boon', h: 'บุญ', s: ['common', 'traditional'], l: 'shorter', m: 'merit' },
  { r: 'Siri', h: 'สิริ', s: ['modern', 'elegant'], l: 'shorter', m: 'glory' },
  { r: 'Kiat', h: 'เกียรติ', s: ['common', 'traditional'], l: 'shorter', m: 'honor' },
  { r: 'Phong', h: 'พงศ์', s: ['traditional'], l: 'shorter', m: 'lineage' },
  { r: 'Sawat', h: 'สวัสดิ์', s: ['common'], l: 'shorter', m: 'blessing' },
  { r: 'Rueang', h: 'เรือง', s: ['modern'], l: 'shorter', m: 'shine' },
  { r: 'Phatthana', h: 'วัฒนา', s: ['modern'], l: 'distinctive', m: 'development' },
  { r: 'Opas', h: 'โอภาส', s: ['modern'], l: 'shorter', m: 'brightness' },
  { r: 'Suriya', h: 'สุริยะ', s: ['traditional'], l: 'distinctive', m: 'sun' },
  { r: 'Chok', h: 'โชค', s: ['common'], l: 'shorter', m: 'luck' },
  { r: 'Narin', h: 'นรินทร์', s: ['traditional'], l: 'distinctive', m: 'noble ruler' },
  { r: 'Phrom', h: 'พรหม', s: ['traditional'], l: 'distinctive', m: 'divine' },
  { r: 'Chai', h: 'ชัย', s: ['common', 'traditional'], l: 'shorter', m: 'victory' },
  { r: 'Det', h: 'เดช', s: ['strong'], l: 'shorter', m: 'power' },
  { r: 'Sakul', h: 'สกุล', s: ['traditional'], l: 'shorter', m: 'family' },
  { r: 'In', h: 'อินทร์', s: ['distinctive', 'strong'], l: 'distinctive', m: 'royal' },
  { r: 'Kham', h: 'คำ', s: ['common'], l: 'shorter', m: 'gold' },
  { r: 'Phan', h: 'พัน', s: ['traditional'], l: 'shorter', m: 'lineage' },
];

const surnameTail = [
  { r: 'chai', h: 'ชัย', s: ['common', 'traditional'], l: 'shorter', m: 'victory' },
  { r: 'wong', h: 'วงศ์', s: ['common', 'traditional'], l: 'shorter', m: 'lineage' },
  { r: 'karn', h: 'กาญจน์', s: ['traditional'], l: 'distinctive', m: 'gold' },
  { r: 'sak', h: 'ศักดิ์', s: ['strong'], l: 'shorter', m: 'power' },
  { r: 'thong', h: 'ทอง', s: ['common'], l: 'shorter', m: 'gold' },
  { r: 'kun', h: 'กุล', s: ['common', 'traditional'], l: 'shorter', m: 'family' },
  { r: 'phon', h: 'ผล', s: ['common'], l: 'shorter', m: 'result' },
  { r: 'phat', h: 'ภัทร', s: ['modern'], l: 'shorter', m: 'auspicious' },
  { r: 'sen', h: 'เสนี', s: ['traditional', 'strong'], l: 'distinctive', m: 'army' },
  { r: 'sri', h: 'ศรี', s: ['common', 'elegant'], l: 'shorter', m: 'glory' },
  { r: 'amnuay', h: 'อำนวย', s: ['modern'], l: 'distinctive', m: 'support' },
  { r: 'sap', h: 'ทรัพย์', s: ['common'], l: 'shorter', m: 'wealth' },
  { r: 'ruang', h: 'เรือง', s: ['modern'], l: 'shorter', m: 'shine' },
  { r: 'phan', h: 'พันธ์', s: ['traditional'], l: 'shorter', m: 'lineage' },
  { r: 'det', h: 'เดช', s: ['strong'], l: 'shorter', m: 'power' },
  { r: 'phrom', h: 'พรหม', s: ['traditional'], l: 'distinctive', m: 'divine' },
  { r: 'chaiyot', h: 'ไชยยศ', s: ['strong', 'traditional'], l: 'distinctive', m: 'victorious rank' },
  { r: 'wattan', h: 'วัฒน์', s: ['modern'], l: 'shorter', m: 'development' },
  { r: 'suwan', h: 'สุวรรณ', s: ['common', 'traditional'], l: 'distinctive', m: 'gold' },
  { r: 'kasem', h: 'เกษม', s: ['traditional'], l: 'shorter', m: 'joy' },
];

const nicknameLead = [
  { r: 'Aom', h: 'ออม', g: ['f'], s: ['cute', 'soft', 'common'], t: ['beauty'], m: 'gentle sound' },
  { r: 'Bow', h: 'โบว์', g: ['f'], s: ['cute', 'modern'], t: ['beauty'], m: 'ribbon-like sound' },
  { r: 'Bua', h: 'บัว', g: ['f'], s: ['soft', 'common'], t: ['nature', 'beauty'], m: 'lotus' },
  { r: 'Fah', h: 'ฟ้า', g: ['f', 'u'], s: ['common', 'soft'], t: ['nature', 'beauty'], m: 'sky' },
  { r: 'Gift', h: 'กิ๊ฟ', g: ['f'], s: ['modern', 'cute'], t: ['fortune'], m: 'gift' },
  { r: 'Ice', h: 'ไอซ์', g: ['u'], s: ['modern', 'cute'], t: ['beauty'], m: 'cool sound' },
  { r: 'Kae', h: 'แก้ม', g: ['f'], s: ['cute', 'soft'], t: ['beauty'], m: 'cheek' },
  { r: 'Kao', h: 'เก้า', g: ['u'], s: ['common', 'cute'], t: ['fortune'], m: 'nine' },
  { r: 'Keng', h: 'เก่ง', g: ['m'], s: ['common', 'strong'], t: ['strength'], m: 'skillful' },
  { r: 'Kwan', h: 'ขวัญ', g: ['f', 'u'], s: ['common', 'soft'], t: ['virtue', 'beauty'], m: 'spirit' },
  { r: 'Mint', h: 'มิ้นต์', g: ['f'], s: ['modern', 'cute'], t: ['beauty'], m: 'fresh' },
  { r: 'Mook', h: 'มุก', g: ['f'], s: ['common', 'soft'], t: ['beauty', 'fortune'], m: 'pearl' },
  { r: 'Noon', h: 'นุ่น', g: ['f'], s: ['common', 'soft'], t: ['beauty'], m: 'warm sound' },
  { r: 'Nok', h: 'นก', g: ['f'], s: ['common', 'traditional'], t: ['nature'], m: 'bird' },
  { r: 'Nut', h: 'นัท', g: ['u'], s: ['common', 'modern'], t: ['fortune'], m: 'short modern sound' },
  { r: 'Oi', h: 'ออย', g: ['f'], s: ['modern', 'cute'], t: ['beauty'], m: 'playful sound' },
  { r: 'Pang', h: 'แป้ง', g: ['f'], s: ['cute', 'common'], t: ['beauty'], m: 'powder' },
  { r: 'Pae', h: 'เป้', g: ['m'], s: ['common', 'cute'], t: ['strength'], m: 'target' },
  { r: 'Pim', h: 'พิม', g: ['f'], s: ['common', 'soft'], t: ['beauty'], m: 'pattern' },
  { r: 'Ploy', h: 'พลอย', g: ['f'], s: ['common', 'cute'], t: ['beauty', 'fortune'], m: 'gemstone' },
  { r: 'Pun', h: 'ปัน', g: ['u'], s: ['modern', 'cute'], t: ['fortune'], m: 'share' },
  { r: 'Sai', h: 'ทราย', g: ['f'], s: ['common', 'soft'], t: ['nature'], m: 'sand' },
  { r: 'Sky', h: 'สกาย', g: ['u'], s: ['modern', 'cute'], t: ['nature'], m: 'sky' },
  { r: 'Ton', h: 'ต้น', g: ['m'], s: ['common', 'traditional'], t: ['nature', 'strength'], m: 'tree' },
  { r: 'Wan', h: 'หวาน', g: ['f'], s: ['cute', 'soft'], t: ['beauty'], m: 'sweet' },
  { r: 'Yui', h: 'ยุ้ย', g: ['f'], s: ['cute', 'modern'], t: ['beauty'], m: 'playful sound' },
  { r: 'Bam', h: 'แบม', g: ['f'], s: ['modern', 'cute'], t: ['beauty'], m: 'bright sound' },
  { r: 'Benz', h: 'เบนซ์', g: ['m'], s: ['modern', 'cute'], t: ['strength'], m: 'stylish' },
  { r: 'Boom', h: 'บูม', g: ['m'], s: ['modern', 'cute'], t: ['strength'], m: 'loud energy' },
  { r: 'Bie', h: 'บี้', g: ['m'], s: ['cute', 'modern'], t: ['strength'], m: 'small energetic sound' },
  { r: 'Toey', h: 'เตย', g: ['f'], s: ['common', 'soft'], t: ['nature'], m: 'pandan leaf' },
];

const nicknameTail = [
  { r: 'jai', h: 'ใจ', g: ['u'], s: ['soft', 'common'], t: ['virtue', 'beauty'], m: 'heart' },
  { r: 'rak', h: 'รัก', g: ['u'], s: ['soft'], t: ['beauty'], m: 'love' },
  { r: 'wan', h: 'หวาน', g: ['f', 'u'], s: ['cute', 'soft'], t: ['beauty'], m: 'sweet' },
  { r: 'noi', h: 'น้อย', g: ['f'], s: ['cute'], t: ['beauty'], m: 'small' },
  { r: 'dee', h: 'ดี', g: ['u'], s: ['common', 'soft'], t: ['virtue'], m: 'good' },
  { r: 'lek', h: 'เล็ก', g: ['u'], s: ['common'], t: ['virtue'], m: 'small' },
  { r: 'mook', h: 'มุก', g: ['f'], s: ['cute', 'soft'], t: ['beauty'], m: 'pearl' },
  { r: 'bun', h: 'บุญ', g: ['u'], s: ['common'], t: ['fortune', 'virtue'], m: 'merit' },
  { r: 'yim', h: 'ยิ้ม', g: ['u'], s: ['cute', 'soft'], t: ['beauty'], m: 'smile' },
  { r: 'ka', h: 'กา', g: ['f', 'u'], s: ['cute'], t: ['beauty'], m: 'bright sound' },
];

const romanizationOverrides = new Map([
  ['Methawee-wong', 'Methaweewong'],
]);

function uniq(arr) {
  return [...new Set(arr.filter(Boolean))];
}

function normalizeRomanized(value) {
  return romanizationOverrides.get(value) || value;
}

function titleCase(value) {
  const normalized = String(value || '').trim();
  if (!normalized) return '';
  return normalized.charAt(0).toUpperCase() + normalized.slice(1);
}

function romanize(a, b) {
  return titleCase(`${a}${b}`);
}

function pickGender(a, b) {
  const genders = uniq([...(a || []), ...(b || [])]);
  if (genders.includes('m') && !genders.includes('f')) return 'm';
  if (genders.includes('f') && !genders.includes('m')) return 'f';
  return 'u';
}

function pickLength(romanized) {
  return romanized.length > 11 ? 'distinctive' : 'shorter';
}

function makeCompound(a, b) {
  const romanized = romanize(a.r, b.r);
  const gender = pickGender(a.g, b.g);
  const styles = uniq([...(a.s || []), ...(b.s || [])]);
  const themes = uniq([...(a.t || []), ...(b.t || [])]);
  return {
    thai: `${a.h}${b.h}`,
    romanized,
    gender,
    styles,
    themes,
    meaning: `${a.m}; ${b.m}`,
  };
}

function buildPool(prefixes, suffixes, mapEntry) {
  const out = [];
  for (const a of prefixes) {
    for (const b of suffixes) {
      out.push(mapEntry(a, b));
    }
  }
  return out;
}

function growArray(existing, target, candidates, makeKey, transform) {
  const result = existing.slice();
  const seen = new Set(result.map(makeKey));
  for (const candidate of candidates) {
    if (result.length >= target) break;
    const entry = transform(candidate);
    const key = makeKey(entry);
    if (seen.has(key)) continue;
    seen.add(key);
    result.push(entry);
  }
  if (result.length < target) {
    throw new Error(`Unable to reach target ${target}; only got ${result.length}`);
  }
  return result.slice(0, target);
}

function maybeCleanStyles(styles) {
  return uniq(styles).filter(Boolean);
}

function buildSurnameEntry(a, b) {
  const romanized = normalizeRomanized(romanize(a.r, b.r));
  return [
    `${a.h}${b.h}`,
    romanized,
    maybeCleanStyles([...(a.s || []), ...(b.s || [])]),
    pickLength(romanized),
    `${a.m}; ${b.m}`,
  ];
}

function buildNicknameEntry(a, b) {
  const compound = makeCompound(a, b);
  return [
    compound.thai,
    compound.romanized,
    compound.gender,
    maybeCleanStyles(compound.styles),
    uniq(compound.themes),
    compound.meaning,
  ];
}

function buildGivenEntry(a, b) {
  const compound = makeCompound(a, b);
  return [
    compound.thai,
    compound.romanized,
    compound.gender,
    maybeCleanStyles(compound.styles),
    uniq(compound.themes),
    compound.meaning,
  ];
}

function dedupeByRomanized(entries) {
  const seen = new Set();
  return entries.filter((entry) => {
    const key = String(entry[1] || '').toLowerCase();
    if (seen.has(key)) return false;
    seen.add(key);
    return true;
  });
}

function normalizeExistingEntries(entries) {
  return entries.map((entry) => {
    if (!Array.isArray(entry) || entry.length < 2) return entry;
    const normalized = normalizeRomanized(entry[1]);
    if (normalized === entry[1]) return entry;
    return [entry[0], normalized, ...entry.slice(2)];
  });
}

function main() {
  const raw = JSON.parse(fs.readFileSync(DATA_PATH, 'utf8'));
  const givenExisting = dedupeByRomanized(normalizeExistingEntries(Array.isArray(raw.given) ? raw.given.slice() : []));
  const surnameExisting = dedupeByRomanized(normalizeExistingEntries(Array.isArray(raw.surnames) ? raw.surnames.slice() : []));
  const nicknameExisting = dedupeByRomanized(normalizeExistingEntries(Array.isArray(raw.nicknames) ? raw.nicknames.slice() : []));

  const givenCandidates = buildPool(givenLead, givenTail, buildGivenEntry);
  const surnameCandidates = buildPool(surnameLead, surnameTail, buildSurnameEntry);
  const nicknameCandidates = buildPool(nicknameLead, nicknameTail, buildNicknameEntry);

  const byRomanized = (entry) => String(entry[1] || '').toLowerCase();

  raw.given = growArray(givenExisting, TARGETS.given, givenCandidates, byRomanized, (entry) => entry);
  raw.surnames = growArray(surnameExisting, TARGETS.surnames, surnameCandidates, byRomanized, (entry) => entry);
  raw.nicknames = growArray(nicknameExisting, TARGETS.nicknames, nicknameCandidates, byRomanized, (entry) => entry);
  raw.source = 'Curated Thai name dataset for Wordineer, expanded with compositional Thai name roots';
  raw.notes = 'Thai names are shown in romanized form by default, with Thai script available as an alternate display. Meaning notes are short helper summaries, not full linguistic or legal naming guidance.';

  fs.writeFileSync(DATA_PATH, `${JSON.stringify(raw, null, 2)}\n`);
  console.log(`Wrote ${raw.given.length + raw.surnames.length + raw.nicknames.length} Thai names to ${DATA_PATH}`);
}

main();

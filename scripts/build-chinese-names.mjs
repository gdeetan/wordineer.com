import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const DATA_PATH = path.join(ROOT, 'wordineer-deploy', 'data', 'chinese-names.json');
const TARGET_GIVEN = 1200;

const maleLeads = [
  { p: 'Hao', h: '浩', s: ['modern', 'strong'], t: ['strength', 'light'], m: 'vast' },
  { p: 'Jun', h: '俊', s: ['common', 'elegant'], t: ['wisdom', 'beauty'], m: 'talented' },
  { p: 'Wei', h: '伟', s: ['common', 'strong'], t: ['strength', 'prosperity'], m: 'great' },
  { p: 'Zhi', h: '志', s: ['traditional', 'strong'], t: ['virtue', 'wisdom'], m: 'ambition' },
  { p: 'Ming', h: '明', s: ['common', 'elegant'], t: ['light', 'wisdom'], m: 'bright' },
  { p: 'Tian', h: '天', s: ['traditional', 'elegant'], t: ['light', 'nature'], m: 'heaven' },
  { p: 'Guang', h: '光', s: ['traditional', 'elegant'], t: ['light', 'virtue'], m: 'radiance' },
  { p: 'Jian', h: '建', s: ['modern', 'strong'], t: ['strength', 'prosperity'], m: 'build' },
  { p: 'Yong', h: '永', s: ['traditional', 'gentle'], t: ['peace', 'virtue'], m: 'eternal' },
  { p: 'Peng', h: '鹏', s: ['wuxia', 'strong'], t: ['strength', 'prosperity'], m: 'great roc' },
  { p: 'Wen', h: '文', s: ['traditional', 'elegant'], t: ['wisdom', 'virtue'], m: 'culture' },
  { p: 'Bo', h: '博', s: ['modern', 'elegant'], t: ['wisdom', 'prosperity'], m: 'broad' },
  { p: 'Lei', h: '雷', s: ['strong', 'wuxia'], t: ['nature', 'strength'], m: 'thunder' },
  { p: 'Cheng', h: '承', s: ['traditional', 'gentle'], t: ['virtue', 'prosperity'], m: 'carry forward' },
  { p: 'Rui', h: '睿', s: ['modern', 'elegant'], t: ['wisdom', 'light'], m: 'wise' },
  { p: 'Han', h: '翰', s: ['traditional', 'elegant'], t: ['wisdom', 'virtue'], m: 'scholarly writing' },
  { p: 'Guo', h: '国', s: ['traditional', 'strong'], t: ['virtue', 'prosperity'], m: 'nation' },
  { p: 'Qi', h: '启', s: ['modern', 'gentle'], t: ['wisdom', 'light'], m: 'open and awaken' },
  { p: 'Sheng', h: '盛', s: ['traditional', 'strong'], t: ['prosperity', 'strength'], m: 'flourishing' },
  { p: 'Yu', h: '宇', s: ['modern', 'elegant'], t: ['light', 'prosperity'], m: 'universe' }
];

const maleTails = [
  { p: 'Ran', h: '然', s: ['gentle', 'elegant'], t: ['virtue', 'peace'], m: 'natural calm' },
  { p: 'Chen', h: '辰', s: ['modern', 'elegant'], t: ['light', 'prosperity'], m: 'morning star' },
  { p: 'Xuan', h: '轩', s: ['modern', 'elegant'], t: ['prosperity', 'light'], m: 'lofty' },
  { p: 'Jie', h: '杰', s: ['common', 'strong'], t: ['wisdom', 'strength'], m: 'heroic excellence' },
  { p: 'Ze', h: '泽', s: ['modern', 'gentle'], t: ['virtue', 'water'], m: 'grace' },
  { p: 'Guo', h: '国', s: ['traditional', 'strong'], t: ['strength', 'prosperity'], m: 'nation' },
  { p: 'Hong', h: '宏', s: ['traditional', 'strong'], t: ['prosperity', 'strength'], m: 'grandness' },
  { p: 'Yao', h: '耀', s: ['elegant', 'strong'], t: ['light', 'prosperity'], m: 'glory' },
  { p: 'Yuan', h: '远', s: ['wuxia', 'gentle'], t: ['virtue', 'wisdom'], m: 'far-reaching' },
  { p: 'Yu', h: '宇', s: ['modern', 'elegant'], t: ['light', 'nature'], m: 'the cosmos' },
  { p: 'Wei', h: '伟', s: ['common', 'strong'], t: ['strength', 'prosperity'], m: 'greatness' },
  { p: 'Hao', h: '豪', s: ['modern', 'strong'], t: ['strength', 'prosperity'], m: 'heroic greatness' },
  { p: 'Qiang', h: '强', s: ['traditional', 'strong'], t: ['strength', 'peace'], m: 'strength' },
  { p: 'Long', h: '龙', s: ['wuxia', 'strong'], t: ['strength', 'prosperity'], m: 'dragon' },
  { p: 'Hai', h: '海', s: ['elegant', 'gentle'], t: ['nature', 'prosperity'], m: 'sea' },
  { p: 'Liang', h: '良', s: ['traditional', 'gentle'], t: ['virtue', 'prosperity'], m: 'goodness' },
  { p: 'Dong', h: '东', s: ['common', 'modern'], t: ['light', 'nature'], m: 'east' },
  { p: 'Ming', h: '明', s: ['traditional', 'elegant'], t: ['light', 'wisdom'], m: 'brightness' },
  { p: 'An', h: '安', s: ['gentle', 'traditional'], t: ['peace', 'virtue'], m: 'peace' },
  { p: 'Han', h: '翰', s: ['elegant', 'traditional'], t: ['wisdom', 'virtue'], m: 'scholarly grace' }
];

const femaleLeads = [
  { p: 'Mei', h: '美', s: ['common', 'elegant'], t: ['beauty', 'prosperity'], m: 'beautiful' },
  { p: 'Xin', h: '心', s: ['common', 'gentle'], t: ['peace', 'beauty'], m: 'heart' },
  { p: 'Yu', h: '雨', s: ['modern', 'gentle'], t: ['nature', 'beauty'], m: 'rain' },
  { p: 'Jing', h: '静', s: ['common', 'gentle'], t: ['peace', 'virtue'], m: 'calm' },
  { p: 'Li', h: '丽', s: ['traditional', 'elegant'], t: ['beauty', 'prosperity'], m: 'lovely' },
  { p: 'Ruo', h: '若', s: ['modern', 'elegant'], t: ['light', 'beauty'], m: 'like' },
  { p: 'Yan', h: '燕', s: ['traditional', 'gentle'], t: ['nature', 'beauty'], m: 'swallow bird' },
  { p: 'Xiao', h: '晓', s: ['traditional', 'gentle'], t: ['light', 'nature'], m: 'dawn' },
  { p: 'Lan', h: '兰', s: ['traditional', 'elegant'], t: ['nature', 'virtue'], m: 'orchid' },
  { p: 'Qian', h: '倩', s: ['modern', 'gentle'], t: ['beauty', 'virtue'], m: 'graceful' },
  { p: 'Ying', h: '映', s: ['elegant', 'wuxia'], t: ['light', 'nature'], m: 'reflected glow' },
  { p: 'Shu', h: '淑', s: ['traditional', 'elegant'], t: ['virtue', 'beauty'], m: 'graceful goodness' },
  { p: 'Xiu', h: '秀', s: ['traditional', 'gentle'], t: ['beauty', 'nature'], m: 'elegant' },
  { p: 'Hui', h: '慧', s: ['common', 'gentle'], t: ['wisdom', 'virtue'], m: 'wisdom' },
  { p: 'Qing', h: '清', s: ['elegant', 'gentle'], t: ['light', 'virtue'], m: 'clear' },
  { p: 'Meng', h: '梦', s: ['modern', 'elegant'], t: ['beauty', 'light'], m: 'dream' },
  { p: 'Jia', h: '佳', s: ['modern', 'elegant'], t: ['beauty', 'prosperity'], m: 'excellent' },
  { p: 'Ling', h: '凌', s: ['wuxia', 'strong'], t: ['strength', 'light'], m: 'rise above' },
  { p: 'Rong', h: '荣', s: ['traditional', 'strong'], t: ['prosperity', 'beauty'], m: 'glory' },
  { p: 'Ning', h: '宁', s: ['modern', 'gentle'], t: ['peace', 'virtue'], m: 'tranquil' }
];

const femaleTails = [
  { p: 'Lin', h: '琳', s: ['common', 'elegant'], t: ['beauty', 'prosperity'], m: 'jade chime' },
  { p: 'Yi', h: '怡', s: ['gentle', 'common'], t: ['peace', 'virtue'], m: 'harmony' },
  { p: 'Tong', h: '桐', s: ['modern', 'gentle'], t: ['nature', 'beauty'], m: 'parasol tree' },
  { p: 'Hua', h: '华', s: ['traditional', 'elegant'], t: ['beauty', 'prosperity'], m: 'splendor' },
  { p: 'Xi', h: '曦', s: ['modern', 'elegant'], t: ['light', 'beauty'], m: 'dawn glow' },
  { p: 'Ling', h: '玲', s: ['traditional', 'gentle'], t: ['beauty', 'virtue'], m: 'tinkling jade' },
  { p: 'Yue', h: '月', s: ['gentle', 'elegant'], t: ['nature', 'light'], m: 'moon' },
  { p: 'Mei', h: '梅', s: ['traditional', 'gentle'], t: ['nature', 'light'], m: 'plum blossom' },
  { p: 'Xin', h: '心', s: ['elegant', 'gentle'], t: ['virtue', 'beauty'], m: 'heart' },
  { p: 'Ru', h: '如', s: ['modern', 'gentle'], t: ['beauty', 'virtue'], m: 'as if graceful' },
  { p: 'Yue', h: '月', s: ['wuxia', 'elegant'], t: ['light', 'nature'], m: 'moonlight' },
  { p: 'Ying', h: '英', s: ['traditional', 'elegant'], t: ['virtue', 'beauty'], m: 'excellence' },
  { p: 'Lan', h: '兰', s: ['traditional', 'gentle'], t: ['beauty', 'nature'], m: 'orchid' },
  { p: 'Yao', h: '瑶', s: ['modern', 'elegant'], t: ['beauty', 'prosperity'], m: 'precious jade' },
  { p: 'Lian', h: '莲', s: ['elegant', 'wuxia'], t: ['nature', 'beauty'], m: 'lotus' },
  { p: 'Zhen', h: '珍', s: ['common', 'gentle'], t: ['beauty', 'prosperity'], m: 'precious treasure' },
  { p: 'Yun', h: '云', s: ['modern', 'elegant'], t: ['nature', 'light'], m: 'cloud' },
  { p: 'Qing', h: '清', s: ['gentle', 'elegant'], t: ['peace', 'virtue'], m: 'clarity' },
  { p: 'Xue', h: '雪', s: ['elegant', 'gentle'], t: ['nature', 'light'], m: 'snow' },
  { p: 'Xin', h: '馨', s: ['modern', 'gentle'], t: ['peace', 'virtue'], m: 'fragrance' }
];

const unisexLeads = [
  { p: 'An', h: '安', s: ['common', 'gentle'], t: ['peace', 'virtue'], m: 'peace' },
  { p: 'Chen', h: '晨', s: ['common', 'modern'], t: ['light', 'nature'], m: 'morning' },
  { p: 'Guang', h: '光', s: ['traditional', 'elegant'], t: ['light', 'virtue'], m: 'light' },
  { p: 'He', h: '和', s: ['traditional', 'gentle'], t: ['peace', 'virtue'], m: 'harmony' },
  { p: 'Jing', h: '静', s: ['common', 'gentle'], t: ['peace', 'virtue'], m: 'stillness' },
  { p: 'Lan', h: '岚', s: ['elegant', 'gentle'], t: ['nature', 'light'], m: 'mountain mist' },
  { p: 'Lin', h: '霖', s: ['modern', 'gentle'], t: ['nature', 'prosperity'], m: 'timely rain' },
  { p: 'Ming', h: '明', s: ['common', 'modern'], t: ['light', 'wisdom'], m: 'brightness' },
  { p: 'Ning', h: '宁', s: ['common', 'gentle'], t: ['peace', 'virtue'], m: 'tranquility' },
  { p: 'Qing', h: '清', s: ['common', 'elegant'], t: ['light', 'virtue'], m: 'clarity' },
  { p: 'Rui', h: '睿', s: ['modern', 'elegant'], t: ['wisdom', 'light'], m: 'insight' },
  { p: 'Tian', h: '天', s: ['traditional', 'elegant'], t: ['light', 'nature'], m: 'sky' },
  { p: 'Xin', h: '欣', s: ['common', 'modern'], t: ['peace', 'prosperity'], m: 'joyful flourishing' },
  { p: 'Yun', h: '云', s: ['elegant', 'gentle'], t: ['nature', 'light'], m: 'cloud' },
  { p: 'Zi', h: '子', s: ['traditional', 'elegant'], t: ['wisdom', 'virtue'], m: 'scholarly child' }
];

const unisexTails = [
  { p: 'An', h: '安', s: ['gentle', 'traditional'], t: ['peace', 'virtue'], m: 'peace' },
  { p: 'Ming', h: '明', s: ['modern', 'elegant'], t: ['light', 'wisdom'], m: 'brightness' },
  { p: 'He', h: '和', s: ['gentle', 'traditional'], t: ['peace', 'virtue'], m: 'harmony' },
  { p: 'Lan', h: '岚', s: ['elegant', 'gentle'], t: ['nature', 'light'], m: 'mist' },
  { p: 'Xi', h: '熙', s: ['modern', 'elegant'], t: ['light', 'prosperity'], m: 'radiant joy' },
  { p: 'Yue', h: '悦', s: ['common', 'modern'], t: ['peace', 'prosperity'], m: 'delight' },
  { p: 'Yun', h: '云', s: ['elegant', 'gentle'], t: ['nature', 'light'], m: 'cloud' },
  { p: 'Zhen', h: '真', s: ['traditional', 'gentle'], t: ['virtue', 'wisdom'], m: 'truth' },
  { p: 'Zhi', h: '知', s: ['traditional', 'elegant'], t: ['wisdom', 'virtue'], m: 'knowledge' },
  { p: 'Jia', h: '佳', s: ['common', 'elegant'], t: ['beauty', 'prosperity'], m: 'excellence' },
  { p: 'Yu', h: '宇', s: ['modern', 'elegant'], t: ['light', 'prosperity'], m: 'universe' },
  { p: 'Yao', h: '瑶', s: ['elegant', 'gentle'], t: ['beauty', 'prosperity'], m: 'precious jade' },
  { p: 'Ling', h: '灵', s: ['common', 'wuxia'], t: ['wisdom', 'light'], m: 'spirit' },
  { p: 'Feng', h: '风', s: ['wuxia', 'strong'], t: ['nature', 'strength'], m: 'wind' },
  { p: 'Chen', h: '晨', s: ['common', 'modern'], t: ['light', 'nature'], m: 'morning' },
  { p: 'Qing', h: '清', s: ['common', 'elegant'], t: ['light', 'virtue'], m: 'purity' },
  { p: 'Rui', h: '睿', s: ['modern', 'elegant'], t: ['wisdom', 'light'], m: 'wisdom' },
  { p: 'Tian', h: '天', s: ['traditional', 'elegant'], t: ['light', 'nature'], m: 'heaven' },
  { p: 'Xin', h: '欣', s: ['common', 'modern'], t: ['peace', 'prosperity'], m: 'joy' },
  { p: 'Ning', h: '宁', s: ['gentle', 'traditional'], t: ['peace', 'virtue'], m: 'calm' }
];

function uniq(values) {
  return [...new Set(values)];
}

function buildSet(leads, tails, gender, target, seen) {
  const out = [];
  for (const lead of leads) {
    for (const tail of tails) {
      if (out.length >= target) return out;
      const pinyin = lead.p + tail.p;
      const hanzi = lead.h + tail.h;
      const key = `${pinyin.toLowerCase()}|${hanzi}`;
      if (seen.has(key)) continue;
      seen.add(key);
      out.push([
        pinyin,
        hanzi,
        gender,
        uniq([...lead.s, ...tail.s]),
        uniq([...lead.t, ...tail.t]),
        `${lead.m}; ${tail.m}`
      ]);
    }
  }
  return out;
}

function main() {
  const raw = JSON.parse(fs.readFileSync(DATA_PATH, 'utf8'));
  const existing = Array.isArray(raw.given) ? raw.given.slice() : [];
  const seen = new Set(existing.map((entry) => `${String(entry[0]).toLowerCase()}|${entry[1]}`));

  const maleTarget = 400;
  const femaleTarget = 400;
  const unisexTarget = 280;

  const generatedMale = buildSet(maleLeads, maleTails, 'm', maleTarget, seen);
  const generatedFemale = buildSet(femaleLeads, femaleTails, 'f', femaleTarget, seen);
  const generatedUnisex = buildSet(unisexLeads, unisexTails, 'u', unisexTarget, seen);

  const combined = existing
    .concat(generatedMale)
    .concat(generatedFemale)
    .concat(generatedUnisex)
    .slice(0, TARGET_GIVEN);

  if (combined.length < 1000) {
    throw new Error(`Chinese dataset too small after generation: ${combined.length}`);
  }

  raw.source = 'Curated and expanded Chinese name dataset for Wordineer';
  raw.notes = 'Mandarin-mainland focused dataset for writers and creators. It combines a curated seed list with larger generated pools built from common Chinese name elements. Pinyin is shown in simple Latin spelling for English readers. Meanings are concise helper notes, not full etymology entries. Chinese full names are shown in family-name-first order by default.';
  raw.given = combined;

  fs.writeFileSync(DATA_PATH, JSON.stringify(raw, null, 2) + '\n', 'utf8');
  console.log(`Wrote ${raw.given.length} Chinese given names to ${DATA_PATH}`);
}

main();

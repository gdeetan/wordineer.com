import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const NAMES_PATH = path.join(ROOT, 'wordineer-deploy', 'data', 'names.json');
const OUT_PATH = path.join(ROOT, 'wordineer-deploy', 'data', 'indian-names.json');

const TARGETS = {
  givenNames: 800,
  surnames: 300,
};

const GIVEN_SPLIT = { male: 34, female: 34, unisex: 12 };
const STYLE_POOL = [
  ['traditional', 'mythological'],
  ['traditional', 'religious'],
  ['modern', 'urban'],
  ['traditional', 'urban'],
  ['modern', 'religious'],
];

const REGION_SPECS = [
  {
    slug: 'hindi-hindustani',
    label: 'Hindi / Hindustani',
    malePrefixes: ['Aar', 'Dev', 'Har', 'Ish', 'Nikh', 'Pran', 'Rudr', 'Shaur'],
    maleSuffixes: ['av', 'esh', 'it', 'ayan', 'ansh', 'raj'],
    femalePrefixes: ['An', 'Div', 'Ish', 'Kav', 'Nav', 'Priy', 'Tan', 'Yash'],
    femaleSuffixes: ['aya', 'ika', 'isha', 'ita', 'ya', 'shree'],
    unisexPrefixes: ['Adi', 'Kir', 'Man', 'Nav', 'Sai', 'Ved'],
    unisexSuffixes: ['an', 'deep', 'it', 'ra', 'ya'],
    surnames: [
      'Agarwal', 'Ahuja', 'Anand', 'Arora', 'Bajpai', 'Bansal', 'Bhardwaj', 'Chauhan', 'Dubey', 'Dwivedi',
      'Jain', 'Kapoor', 'Khanna', 'Malhotra', 'Mehra', 'Mishra', 'Nagpal', 'Pandey', 'Pathak', 'Saxena',
      'Sethi', 'Sharma', 'Shukla', 'Srivastava', 'Tandon', 'Tiwari', 'Tripathi', 'Verma', 'Kaushal', 'Bhatnagar'
    ],
  },
  {
    slug: 'punjabi',
    label: 'Punjabi',
    malePrefixes: ['Amar', 'Bal', 'Charan', 'Gur', 'Har', 'Jas', 'Nav', 'Sat'],
    maleSuffixes: ['deep', 'inder', 'jeet', 'pal', 'preet', 'veer'],
    femalePrefixes: ['Aman', 'Gur', 'Har', 'Jas', 'Man', 'Nav', 'Sim', 'Sukh'],
    femaleSuffixes: ['deep', 'jyot', 'kaur', 'leen', 'noor', 'preet'],
    unisexPrefixes: ['Akal', 'Dil', 'Ek', 'Gur', 'Mehar', 'Sim'],
    unisexSuffixes: ['deep', 'jeet', 'noor', 'preet', 'veer'],
    surnames: [
      'Aulakh', 'Batra', 'Bedi', 'Boparai', 'Brar', 'Chahal', 'Chawla', 'Dhillon', 'Gill', 'Grewal',
      'Heer', 'Johal', 'Juneja', 'Kang', 'Khurana', 'Kohli', 'Maan', 'Nanda', 'Pannu', 'Randhawa',
      'Saini', 'Sandhu', 'Sekhon', 'Sidhu', 'Sodhi', 'Suri', 'Toor', 'Uppal', 'Virk', 'Walia'
    ],
  },
  {
    slug: 'gujarati',
    label: 'Gujarati',
    malePrefixes: ['Bhav', 'Darsh', 'Har', 'Meet', 'Nir', 'Parth', 'Vraj', 'Yug'],
    maleSuffixes: ['deep', 'esh', 'il', 'it', 'raj', 'vik'],
    femalePrefixes: ['Aashi', 'Bhumi', 'Dev', 'Het', 'Jin', 'Krish', 'Nidh', 'Riddh'],
    femaleSuffixes: ['a', 'al', 'i', 'ika', 'ya', 'vi'],
    unisexPrefixes: ['Aum', 'Dar', 'Het', 'Jiv', 'Nav', 'Rit'],
    unisexSuffixes: ['a', 'an', 'deep', 'il', 'ya'],
    surnames: [
      'Acharya', 'Barot', 'Bhatt', 'Buch', 'Contractor', 'Dave', 'Desai', 'Gajjar', 'Gandhi', 'Kothari',
      'Majmudar', 'Mehta', 'Mistry', 'Modi', 'Panchal', 'Pandya', 'Parekh', 'Parikh', 'Patel', 'Raval',
      'Shah', 'Vakil', 'Solanki', 'Soni', 'Thakkar', 'Trivedi', 'Vora', 'Vyas', 'Zaveri', 'Jhaveri'
    ],
  },
  {
    slug: 'marathi',
    label: 'Marathi',
    malePrefixes: ['Adi', 'Om', 'Prath', 'Roh', 'Shiv', 'Swar', 'Tan', 'Ved'],
    maleSuffixes: ['aj', 'esh', 'it', 'raj', 'roop', 'vik'],
    femalePrefixes: ['Aar', 'Bhav', 'Gaur', 'Mrun', 'Praj', 'Rev', 'Sai', 'Tanv'],
    femaleSuffixes: ['ali', 'ika', 'ita', 'mayi', 'shree', 'ya'],
    unisexPrefixes: ['Ari', 'Jay', 'Nitya', 'Ritu', 'Samar', 'Tej'],
    unisexSuffixes: ['a', 'an', 'deep', 'it', 'ya'],
    surnames: [
      'Agashe', 'Apte', 'Bapat', 'Bhonsle', 'Chavan', 'Damle', 'Deshmukh', 'Gokhale', 'Inamdar', 'Jadhav',
      'Kadam', 'Kale', 'Karmarkar', 'Kulkarni', 'Mahajan', 'Mane', 'More', 'Patil', 'Pawar', 'Phadke',
      'Ranade', 'Salunkhe', 'Sathe', 'Shinde', 'Soman', 'Thackeray', 'Vaidya', 'Wagh', 'Pansare', 'Ghate'
    ],
  },
  {
    slug: 'bengali',
    label: 'Bengali',
    malePrefixes: ['Anir', 'Arn', 'Deb', 'Nil', 'Prad', 'Rit', 'Souv', 'Subh'],
    maleSuffixes: ['an', 'deep', 'esh', 'jit', 'moy', 'roop'],
    femalePrefixes: ['Apar', 'Deba', 'Ishi', 'Mou', 'Rim', 'Shre', 'Suchi', 'Tuli'],
    femaleSuffixes: ['ita', 'lata', 'mita', 'moyee', 'rika', 'shree'],
    unisexPrefixes: ['Anu', 'Joy', 'Neel', 'Ritu', 'Shubho', 'Tanu'],
    unisexSuffixes: ['a', 'an', 'deep', 'ita', 'ya'],
    surnames: [
      'Banerjee', 'Basu', 'Bhaduri', 'Bhattacharya', 'Bhowmick', 'Biswas', 'Bose', 'Chakrabarti', 'Chatterjee', 'Chowdhury',
      'Das', 'Datta', 'Dey', 'Dhar', 'Ghosh', 'Lahiri', 'Majumdar', 'Mitra', 'Mukherjee', 'Nandi',
      'Pal', 'Paul', 'Ray', 'Roy', 'Saha', 'Sanyal', 'Sarkar', 'Sen', 'Sengupta', 'Sinha'
    ],
  },
  {
    slug: 'tamil',
    label: 'Tamil',
    malePrefixes: ['Arul', 'Bala', 'Karth', 'Muthu', 'Prabu', 'Senth', 'Surya', 'Thiru'],
    maleSuffixes: ['kumar', 'mani', 'nathan', 'raj', 'vel', 'moorthy'],
    femalePrefixes: ['Anu', 'Kala', 'Madhu', 'Nila', 'Priya', 'Selvi', 'Tamizh', 'Vani'],
    femaleSuffixes: ['kani', 'latha', 'mozhi', 'priya', 'selvi', 'valli'],
    unisexPrefixes: ['Aru', 'Ini', 'Kala', 'Muthu', 'Nila', 'Thendral'],
    unisexSuffixes: ['mani', 'mozhi', 'nila', 'oli', 'selvam'],
    surnames: [
      'Arumugam', 'Balasubramanian', 'Chandrasekaran', 'Elangovan', 'Ganesan', 'Jagannathan', 'Kannan', 'Krishnan', 'Kumaravel', 'Lakshmanan',
      'Manivannan', 'Murugan', 'Narayanan', 'Natarajan', 'Palanisamy', 'Parthasarathy', 'Rajagopal', 'Rajendran', 'Ramasamy', 'Ranganathan',
      'Selvaraj', 'Shanmugam', 'Srinivasan', 'Subramanian', 'Sundararajan', 'Swaminathan', 'Thiagarajan', 'Venkataraman', 'Velmurugan', 'Viswanathan'
    ],
  },
  {
    slug: 'telugu',
    label: 'Telugu',
    malePrefixes: ['Chandra', 'Hari', 'Naga', 'Rama', 'Sai', 'Sri', 'Teja', 'Venkata'],
    maleSuffixes: ['babu', 'krishna', 'nath', 'prasad', 'ram', 'teja'],
    femalePrefixes: ['Anu', 'Bhanu', 'Divya', 'Keerthi', 'Lakshmi', 'Sree', 'Swarna', 'Vani'],
    femaleSuffixes: ['latha', 'lekha', 'mala', 'priya', 'sree', 'valli'],
    unisexPrefixes: ['Bhav', 'Chinni', 'Keer', 'Nitya', 'Satya', 'Sree'],
    unisexSuffixes: ['a', 'deep', 'ram', 'sree', 'ya'],
    surnames: [
      'Alluri', 'Bandi', 'Chaganti', 'Chalasani', 'Chintala', 'Chowdary', 'Gadde', 'Katuri', 'Kilaru', 'Kommineni',
      'Koppula', 'Maddineni', 'Malladi', 'Mallela', 'Mandava', 'Nanduri', 'Pidaparti', 'Potluri', 'Pusapati', 'Rachakonda',
      'Reddy', 'Saripalli', 'Singamsetty', 'Sriram', 'Talluri', 'Thota', 'Uppalapati', 'Varma', 'Velagapudi', 'Yarlagadda'
    ],
  },
  {
    slug: 'kannada',
    label: 'Kannada',
    malePrefixes: ['Anand', 'Gur', 'Kiran', 'Nanda', 'Puneeth', 'Raghav', 'Shiv', 'Vijay'],
    maleSuffixes: ['aditya', 'endra', 'esha', 'kumar', 'raj', 'teja'],
    femalePrefixes: ['Anu', 'Deepa', 'Kavya', 'Megha', 'Pooja', 'Rashmi', 'Sowmya', 'Veena'],
    femaleSuffixes: ['lekha', 'latha', 'mala', 'priya', 'shree', 'vani'],
    unisexPrefixes: ['Chiru', 'Gauri', 'Nava', 'Prakr', 'Siri', 'Tej'],
    unisexSuffixes: ['a', 'deep', 'esha', 'it', 'ya'],
    surnames: [
      'Adiga', 'Bhandary', 'Deshpande', 'Ganiga', 'Gowda', 'Hebbar', 'Hegde', 'Huilgol', 'Jois', 'Kamath',
      'Hugar', 'Kunder', 'Madappa', 'Murthy', 'Naik', 'Nayak', 'Pai', 'Ponnappa', 'Poojary', 'Prabhu',
      'Rao', 'Shastry', 'Shenoy', 'Shetty', 'Somayaji', 'Udupa', 'Upadhya', 'Venkatesh', 'Beligere', 'Hosamani'
    ],
  },
  {
    slug: 'malayalam',
    label: 'Malayalam',
    malePrefixes: ['Arun', 'Hari', 'Jith', 'Manu', 'Nandu', 'Rohit', 'Sree', 'Vinu'],
    maleSuffixes: ['das', 'dev', 'kumar', 'krishnan', 'lal', 'raj'],
    femalePrefixes: ['Anu', 'Arya', 'Divya', 'Lekha', 'Meera', 'Nila', 'Sreya', 'Vidhya'],
    femaleSuffixes: ['ja', 'lekha', 'lakshmi', 'mani', 'mol', 'priya'],
    unisexPrefixes: ['Aisw', 'Biju', 'Gopi', 'Nithya', 'Rithu', 'Vaiga'],
    unisexSuffixes: ['a', 'deep', 'mol', 'ra', 'ya'],
    surnames: [
      'Antony', 'Chacko', 'Cherian', 'Daniel', 'Eapen', 'George', 'Isaac', 'Joseph', 'Kallarakal', 'Koshy',
      'Kurian', 'Kurup', 'Maliekal', 'Marar', 'Mathew', 'Menon', 'Nair', 'Nambiar', 'Namboodiri', 'Nedumparambil',
      'Ninan', 'Oommen', 'Panicker', 'Philip', 'Pillai', 'Tharakan', 'Thomas', 'Unnithan', 'Varghese', 'Warrier'
    ],
  },
  {
    slug: 'sanskrit-pan-indian',
    label: 'Sanskrit-derived / pan-Indian',
    malePrefixes: ['Adi', 'Agni', 'Bharg', 'Chandra', 'Ish', 'Rudra', 'Surya', 'Ved'],
    maleSuffixes: ['ansh', 'dev', 'mitra', 'nath', 'raj', 'tej'],
    femalePrefixes: ['Aditi', 'Arya', 'Bhavya', 'Gauri', 'Isha', 'Jyoti', 'Sharada', 'Ved'],
    femaleSuffixes: ['lakshmi', 'mala', 'priya', 'rekha', 'shree', 'vani'],
    unisexPrefixes: ['Aksha', 'Divya', 'Jaya', 'Kiran', 'Nitya', 'Satya'],
    unisexSuffixes: ['anshi', 'deep', 'jyot', 'mani', 'mitra'],
    surnames: [
      'Agnihotri', 'Bhargava', 'Chaturvedi', 'Dikshit', 'Dvivedi', 'Garg', 'Gaur', 'Gautam', 'Jamadagni', 'Kaul',
      'Kaushik', 'Lahoti', 'Mishrikotkar', 'Ojha', 'Parashar', 'Pandit', 'Pathania', 'Shastri', 'Somani', 'Tarkas',
      'Upadhyay', 'Vaid', 'Vats', 'Vashishtha', 'Vidyarthi', 'Vyom', 'Yajnik', 'Brahme', 'Agastya', 'Aatreya'
    ],
  },
];

function titleCase(value) {
  const normalized = String(value || '').trim();
  return normalized ? normalized.charAt(0).toUpperCase() + normalized.slice(1) : '';
}

function composeName(prefix, suffix) {
  let merged = prefix + suffix;
  if (prefix && suffix && prefix.slice(-1).toLowerCase() === suffix.charAt(0).toLowerCase()) {
    merged = prefix + suffix.slice(1);
  }
  return titleCase(merged.replace(/\s+/g, ''));
}

function makeChunks(list, styleSets, notes) {
  return list.map((text, index) => ({
    text,
    styles: styleSets[index % styleSets.length],
    note: notes[index % notes.length],
  }));
}

function makeGivenEntries(spec, genderKey, target, seen) {
  const prefixKey = `${genderKey}Prefixes`;
  const suffixKey = `${genderKey}Suffixes`;
  const prefixes = makeChunks(
    spec[prefixKey],
    genderKey === 'male'
      ? [STYLE_POOL[0], STYLE_POOL[1], STYLE_POOL[2]]
      : genderKey === 'female'
        ? [STYLE_POOL[1], STYLE_POOL[2], STYLE_POOL[3]]
        : [STYLE_POOL[2], STYLE_POOL[3], STYLE_POOL[4]],
    genderKey === 'male'
      ? ['strength', 'devotion', 'clarity', 'courage']
      : genderKey === 'female'
        ? ['beauty', 'grace', 'wisdom', 'joy']
        : ['light', 'balance', 'peace', 'creativity']
  );
  const suffixes = makeChunks(
    spec[suffixKey],
    genderKey === 'male'
      ? [STYLE_POOL[0], STYLE_POOL[2], STYLE_POOL[4]]
      : genderKey === 'female'
        ? [STYLE_POOL[1], STYLE_POOL[2], STYLE_POOL[3]]
        : [STYLE_POOL[2], STYLE_POOL[3], STYLE_POOL[4]],
    genderKey === 'male'
      ? ['power', 'warmth', 'protection', 'honor']
      : genderKey === 'female'
        ? ['radiance', 'kindness', 'devotion', 'beauty']
        : ['friendship', 'calm', 'brightness', 'flow']
  );

  const gender = genderKey === 'male' ? 'm' : genderKey === 'female' ? 'f' : 'u';
  const out = [];

  for (const prefix of prefixes) {
    for (const suffix of suffixes) {
      if (out.length >= target) return out;
      if (spec.slug === 'hindi-hindustani' && genderKey === 'male' && prefix.text === 'Aar') continue;
      if (spec.slug === 'hindi-hindustani' && genderKey === 'male' && suffix.text === 'av' && prefix.text !== 'Pran') continue;
      if (spec.slug === 'marathi' && genderKey === 'male' && suffix.text === 'aj') continue;
      const name = composeName(prefix.text, suffix.text);
      const key = name.toLowerCase();
      if (seen.has(key)) continue;
      seen.add(key);
      out.push({
        name,
        gender,
        regions: [spec.slug],
        styles: [...new Set([...prefix.styles, ...suffix.styles])],
        meaning: `${spec.label} given name with ${prefix.note} and ${suffix.note} associations.`,
      });
    }
  }

  return out;
}

function mapGenericIndianSeeds() {
  const raw = JSON.parse(fs.readFileSync(NAMES_PATH, 'utf8'));
  const rows = Array.isArray(raw.first) ? raw.first.filter((item) => item[2] === 'Indian') : [];
  const styleMap = {
    classic: ['traditional', 'religious'],
    timeless: ['traditional', 'urban'],
    modern: ['modern', 'urban'],
  };
  return rows.map((item) => ({
    name: item[0],
    gender: item[1],
    regions: ['sanskrit-pan-indian'],
    styles: styleMap[item[3]] || ['traditional'],
    meaning: item[4],
  }));
}

function growGivenNames() {
  const result = [];
  const seen = new Set();

  for (const seed of mapGenericIndianSeeds()) {
    const key = seed.name.toLowerCase();
    if (seen.has(key)) continue;
    seen.add(key);
    result.push(seed);
  }

  for (const spec of REGION_SPECS) {
    result.push(...makeGivenEntries(spec, 'male', GIVEN_SPLIT.male, seen));
    result.push(...makeGivenEntries(spec, 'female', GIVEN_SPLIT.female, seen));
    result.push(...makeGivenEntries(spec, 'unisex', GIVEN_SPLIT.unisex, seen));
  }

  if (result.length < TARGETS.givenNames) {
    throw new Error(`Unable to reach ${TARGETS.givenNames} given names; got ${result.length}`);
  }

  return result.slice(0, TARGETS.givenNames);
}

function surnameStylesFor(index) {
  return STYLE_POOL[index % STYLE_POOL.length];
}

function growSurnames() {
  const result = [];
  const seen = new Set();

  for (const spec of REGION_SPECS) {
    spec.surnames.forEach((name, index) => {
      const key = name.toLowerCase();
      if (seen.has(key)) return;
      seen.add(key);
      result.push({
        name,
        regions: [spec.slug],
        styles: surnameStylesFor(index),
        meaning: `${spec.label} surname used in family and community naming traditions.`,
      });
    });
  }

  if (result.length < TARGETS.surnames) {
    throw new Error(`Unable to reach ${TARGETS.surnames} surnames; got ${result.length}`);
  }

  return result.slice(0, TARGETS.surnames);
}

function main() {
  const data = {
    source: 'Generated from curated Indian naming roots and vetted repo seed names for Wordineer.',
    givenNames: growGivenNames(),
    surnames: growSurnames(),
  };

  fs.writeFileSync(OUT_PATH, JSON.stringify(data, null, 2) + '\n');
  console.log(`Wrote ${data.givenNames.length} given names and ${data.surnames.length} surnames to ${OUT_PATH}`);
}

main();

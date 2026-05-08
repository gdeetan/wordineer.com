# Random Filipino Name Generator — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a dedicated `/random-filipino-name-generator/` tool page with its own JSON dataset, SEO copy, style-based filtering (Traditional / Spanish-colonial / Modern / Nickname), count 1–50 with validation, save/copy features, and internal linking from the random name generator page.

**Architecture:** New `philippine-names.json` data file (independent of `names.json`); new `tools-src/random-filipino-name-generator.html` following the exact pattern of `random-name-generator.html` with style-based filters instead of origin/era; tools.json updated to register the tool in all four sections; random-name-generator.html explainer updated with a related-tools section.

**Tech Stack:** Vanilla HTML/CSS/JS, WORDINEER engine (IIFE, `mode: 'custom'`), static JSON dataset, Python build system (`build.py`), Cloudflare Pages.

---

## Files

| Action | Path |
|---|---|
| Create | `wordineer-deploy/data/philippine-names.json` |
| Create | `template-deploy/tools-src/random-filipino-name-generator.html` |
| Modify | `template-deploy/tools.json` |
| Modify | `template-deploy/tools-src/random-name-generator.html` |
| Modify | `wordineer-deploy/_redirects` |
| Generated | `wordineer-deploy/random-filipino-name-generator.html` (via build) |

---

## Task 1: Create `wordineer-deploy/data/philippine-names.json`

**Files:**
- Create: `wordineer-deploy/data/philippine-names.json`

- [ ] **Step 1: Create the JSON data file**

Create `wordineer-deploy/data/philippine-names.json` with the following content. Schema: first names `[name, gender, style, meaning]`; last names `[name, style, meaning]`. Gender: `"m"` | `"f"` | `"u"`. Style: `"traditional"` | `"spanish"` | `"modern"` | `"nickname"`.

```json
{
  "first": [
    ["Ligaya","f","traditional","happiness; joy"],
    ["Dalisay","f","traditional","pure; clean"],
    ["Luningning","f","traditional","brilliance; radiance"],
    ["Liwanag","f","traditional","light; brightness"],
    ["Marilag","f","traditional","beautiful; magnificent"],
    ["Mutya","f","traditional","precious gem; muse"],
    ["Tala","f","traditional","bright star"],
    ["Malaya","f","traditional","free; liberated"],
    ["Biyaya","f","traditional","blessing; grace"],
    ["Maningning","f","traditional","bright; luminous"],
    ["Lakambini","f","traditional","princess; noble lady"],
    ["Paraluman","f","traditional","guiding star; muse"],
    ["Mayumi","f","traditional","gentle; graceful"],
    ["Diwata","f","traditional","fairy; nature spirit"],
    ["Sampaguita","f","traditional","jasmine; national flower of the Philippines"],
    ["Bituin","f","traditional","star"],
    ["Luwalhati","f","traditional","glory; splendor"],
    ["Dangal","f","traditional","honor; dignity"],
    ["Tahimik","f","traditional","peaceful; quiet"],
    ["Perlas","f","traditional","pearl"],
    ["Bulalacao","f","traditional","firefly"],
    ["Bulaklak","f","traditional","flower"],
    ["Ganda","f","traditional","beauty"],
    ["Umalagad","f","traditional","guardian; protector"],
    ["Pag-asa","f","traditional","hope"],
    ["Bayani","m","traditional","hero; patriot"],
    ["Lakan","m","traditional","lord; noble title"],
    ["Datu","m","traditional","chief; leader"],
    ["Lawin","m","traditional","hawk; falcon"],
    ["Bagwis","m","traditional","feather; wing"],
    ["Matapang","m","traditional","brave; courageous"],
    ["Magiting","m","traditional","valiant; heroic"],
    ["Kidlat","m","traditional","lightning"],
    ["Alon","m","traditional","wave"],
    ["Ulap","m","traditional","cloud"],
    ["Agos","m","traditional","flow; current"],
    ["Habagat","m","traditional","southwest monsoon wind"],
    ["Sandiwa","m","traditional","united spirit; one soul"],
    ["Lakandula","m","traditional","prince of the lake; noble warrior"],
    ["Tagumpay","m","traditional","success; triumph"],
    ["Timawa","m","traditional","free man; freeman"],
    ["Maginoo","m","traditional","noble; gentleman"],
    ["Tapang","m","traditional","courage; bravery"],
    ["Talino","m","traditional","intelligence; brilliance"],
    ["Dunong","m","traditional","wisdom; knowledge"],
    ["Diwa","u","traditional","spirit; soul; essence"],
    ["Luntian","u","traditional","green; nature; life"],
    ["Mahal","u","traditional","love; beloved; dear"],
    ["Buhay","u","traditional","life; alive"],
    ["Lakas","u","traditional","strength; power"],
    ["Maria","f","spanish","beloved; wished-for child"],
    ["Ana","f","spanish","grace; favor"],
    ["Rosa","f","spanish","rose"],
    ["Carmen","f","spanish","garden; vineyard"],
    ["Paz","f","spanish","peace"],
    ["Consuelo","f","spanish","consolation; comfort"],
    ["Remedios","f","spanish","remedy; cure"],
    ["Dolores","f","spanish","sorrows; pains"],
    ["Concepcion","f","spanish","conception; beginning"],
    ["Asuncion","f","spanish","assumption; ascent to heaven"],
    ["Felicidad","f","spanish","happiness; felicity"],
    ["Esperanza","f","spanish","hope; expectation"],
    ["Rosario","f","spanish","rosary; garland of roses"],
    ["Pilar","f","spanish","pillar; column"],
    ["Teresa","f","spanish","harvester; to reap"],
    ["Cristina","f","spanish","follower of Christ"],
    ["Luisa","f","spanish","renowned warrior"],
    ["Elena","f","spanish","bright; shining light"],
    ["Isabel","f","spanish","pledged to God"],
    ["Lourdes","f","spanish","from Lourdes; miraculous"],
    ["Milagros","f","spanish","miracles; wonders"],
    ["Natividad","f","spanish","nativity; birth of Christ"],
    ["Trinidad","f","spanish","holy trinity"],
    ["Corazon","f","spanish","heart"],
    ["Gloria","f","spanish","glory"],
    ["Herminia","f","spanish","soldier; warrior"],
    ["Imelda","f","spanish","powerful fighter"],
    ["Florencia","f","spanish","blooming; prosperous"],
    ["Purificacion","f","spanish","purification; cleansing"],
    ["Perpetua","f","spanish","everlasting; eternal"],
    ["Jose","m","spanish","God will increase"],
    ["Juan","m","spanish","God is gracious"],
    ["Pedro","m","spanish","rock; stone"],
    ["Manuel","m","spanish","God is with us"],
    ["Francisco","m","spanish","free man; from France"],
    ["Antonio","m","spanish","priceless; praiseworthy"],
    ["Carlos","m","spanish","free man; strong"],
    ["Fernando","m","spanish","bold journey; adventurous"],
    ["Ramon","m","spanish","wise protector"],
    ["Eduardo","m","spanish","wealthy guardian"],
    ["Alfredo","m","spanish","elf counsel; wise counselor"],
    ["Roberto","m","spanish","bright fame"],
    ["Ricardo","m","spanish","powerful ruler"],
    ["Ernesto","m","spanish","earnest; sincere"],
    ["Arturo","m","spanish","bear; noble warrior"],
    ["Alberto","m","spanish","noble and bright"],
    ["Bernardo","m","spanish","brave as a bear"],
    ["Cesar","m","spanish","head of hair; emperor"],
    ["Domingo","m","spanish","of the Lord; born on Sunday"],
    ["Felipe","m","spanish","lover of horses"],
    ["Guillermo","m","spanish","resolute protector"],
    ["Lorenzo","m","spanish","crowned with laurel"],
    ["Miguel","m","spanish","who is like God"],
    ["Pablo","m","spanish","small; humble"],
    ["Salvador","m","spanish","savior; rescuer"],
    ["Angel","f","modern","divine messenger"],
    ["Jasmine","f","modern","jasmine flower; gift from God"],
    ["Nicole","f","modern","victory of the people"],
    ["Christine","f","modern","follower of Christ"],
    ["Patricia","f","modern","noble; patrician"],
    ["Jessica","f","modern","God beholds; wealthy"],
    ["Jennifer","f","modern","fair one; white wave"],
    ["Ashley","f","modern","ash tree meadow"],
    ["Stephanie","f","modern","crown; garland"],
    ["Crystal","f","modern","clear; sparkling"],
    ["Sheila","f","modern","blind; heavenly"],
    ["Rowena","f","modern","fame and joy"],
    ["Lovely","f","modern","beautiful; lovable"],
    ["Precious","f","modern","of great value; beloved"],
    ["Princess","f","modern","royal daughter"],
    ["Faith","f","modern","trust; belief"],
    ["Grace","f","modern","grace; favor"],
    ["Hope","f","modern","optimism; expectation"],
    ["Joy","f","modern","happiness; delight"],
    ["Cherry","f","modern","cherry; beloved"],
    ["Daisy","f","modern","day's eye; cheerful flower"],
    ["Honey","f","modern","sweet; beloved"],
    ["Heaven","f","modern","paradise; divine"],
    ["Queenie","f","modern","queen; ruler"],
    ["Rhea","f","modern","flowing stream; earth"],
    ["John","m","modern","God is gracious"],
    ["Mark","m","modern","warlike; of Mars"],
    ["Michael","m","modern","who is like God"],
    ["Kevin","m","modern","handsome; kind"],
    ["Bryan","m","modern","strong; virtuous"],
    ["Ryan","m","modern","little king"],
    ["Jason","m","modern","healer; the Lord is salvation"],
    ["Justin","m","modern","righteous; just"],
    ["Christian","m","modern","follower of Christ"],
    ["Kenneth","m","modern","born of fire; handsome"],
    ["Renz","m","modern","ruler of the home"],
    ["Lance","m","modern","land; territory"],
    ["Lloyd","m","modern","gray; sacred"],
    ["Kent","m","modern","border land; bright white"],
    ["Neil","m","modern","champion; cloud"],
    ["Ian","m","modern","God is gracious"],
    ["Eric","m","modern","eternal ruler; ever powerful"],
    ["Glenn","m","modern","valley; glen"],
    ["Jerome","m","modern","sacred name; holy"],
    ["Prince","m","modern","royal son; first"],
    ["Duke","m","modern","leader; nobleman"],
    ["Carlo","m","modern","free man; strong"],
    ["Paolo","m","modern","small; humble"],
    ["Marco","m","modern","warlike; defender"],
    ["Dennis","m","modern","follower of Dionysus; festive"],
    ["Alex","u","modern","defender of the people"],
    ["Jamie","u","modern","supplanter; one who follows"],
    ["Sam","u","modern","God has heard"],
    ["Chris","u","modern","follower of Christ"],
    ["Jordan","u","modern","to flow down; descend"],
    ["Nene","f","nickname","baby girl; term of endearment"],
    ["Inday","f","nickname","young girl; term of endearment (Visayan)"],
    ["Baby","f","nickname","youngest child; beloved"],
    ["Beng","f","nickname","short form of Benigna or Belen"],
    ["Bing","f","nickname","short form of Albina or Robina"],
    ["Che","f","nickname","short form of names ending in -che"],
    ["Leng","f","nickname","short form of names with this ending"],
    ["Meng","f","nickname","short form of names with this ending"],
    ["Neng","f","nickname","young girl; little one"],
    ["Pet","f","nickname","short form of Petra or Petronilla"],
    ["Reng","f","nickname","short form of names with this ending"],
    ["Tess","f","nickname","short form of Teresa; harvester"],
    ["Tessie","f","nickname","beloved short form of Teresa"],
    ["Tina","f","nickname","short form of Cristina or Martina"],
    ["Weng","f","nickname","short form of names with this ending"],
    ["Yen","f","nickname","short form of names containing yen"],
    ["Yeng","f","nickname","short form of names with this ending"],
    ["Ging","f","nickname","short form of names containing ging"],
    ["Totoy","m","nickname","little boy; term for a young boy"],
    ["Dodong","m","nickname","little boy; eldest son (Visayan)"],
    ["Nonong","m","nickname","beloved grandson; little one"],
    ["Nonoy","m","nickname","baby boy; youngest son"],
    ["Boy","m","nickname","son; young man"],
    ["Bong","m","nickname","short form of names containing bong"],
    ["Dong","m","nickname","short form of names ending in -dong"],
    ["Jun","m","nickname","Junior; young one"],
    ["Jojo","m","nickname","short form of double-J names"],
    ["Nono","m","nickname","short form of Honorio or Nonong"],
    ["Enteng","m","nickname","short form of Ernesto or Esteban"],
    ["Joric","m","nickname","short form of George or Jorick"],
    ["Kokoy","m","nickname","baby boy; playful affectionate term"],
    ["Peping","m","nickname","short form of Jose or Pepe"],
    ["Pitoy","m","nickname","short form of names ending in -pito"],
    ["Tinoy","m","nickname","short form of names ending in -tino"],
    ["Tonyo","m","nickname","short form of Antonio"],
    ["Nong","u","nickname","respectful term; short for Manong"],
    ["Oca","u","nickname","short form of names ending in -oca"],
    ["Bogs","u","nickname","short form of names containing bogs"],
    ["Nicky","u","nickname","short form of Nicholas or Nicole"],
    ["Ricky","u","nickname","short form of Ricardo or Erica"]
  ],
  "last": [
    ["Santos","spanish","saints"],
    ["Reyes","spanish","kings"],
    ["Cruz","spanish","cross"],
    ["Garcia","spanish","young; uncertain origin"],
    ["Gonzales","spanish","battle; war"],
    ["Fernandez","spanish","brave journey"],
    ["Ramos","spanish","branches; palm branches"],
    ["Mendoza","spanish","cold mountain; place name"],
    ["Torres","spanish","towers; watchtower"],
    ["Flores","spanish","flowers"],
    ["Aquino","spanish","from Aquino; eagle"],
    ["Villanueva","spanish","new town; village"],
    ["Castillo","spanish","castle"],
    ["Rivera","spanish","riverbank; shore"],
    ["Perez","spanish","son of Pedro; rock"],
    ["Diaz","spanish","son of Diego; supplanter"],
    ["Bautista","spanish","one who baptizes"],
    ["Morales","spanish","mulberry trees"],
    ["Soriano","spanish","from Soria; place name"],
    ["Espiritu","spanish","spirit; Holy Spirit"],
    ["Miranda","spanish","worthy of admiration; wonderful"],
    ["Aguilar","spanish","eagle's nest"],
    ["Valenzuela","spanish","little brave one"],
    ["Gutierrez","spanish","son of Gutierre; war army"],
    ["Herrera","spanish","iron smith; blacksmith"],
    ["Molina","spanish","mill; from the mill"],
    ["Navarro","spanish","plains; from Navarre"],
    ["Ortega","spanish","nettle plant; place name"],
    ["Padilla","spanish","small frying pan"],
    ["Pascual","spanish","born at Easter"],
    ["Salazar","spanish","old hall; ancient manor"],
    ["Velasco","spanish","crow; raven"],
    ["Villa","spanish","town; small settlement"],
    ["Villafuerte","spanish","strong town; fortified village"],
    ["Arroyo","spanish","stream; small river"],
    ["Romero","spanish","rosemary; pilgrim to Rome"],
    ["Delgado","spanish","thin; slender"],
    ["Campos","spanish","fields; plains"],
    ["Lara","spanish","from Lara; famous"],
    ["Medina","spanish","city; town"],
    ["Valencia","spanish","from Valencia; brave"],
    ["Vargas","spanish","lowlands; marshland"],
    ["Zamora","spanish","wild olive trees"],
    ["Alcantara","spanish","the bridge"],
    ["De Leon","spanish","from Leon; lion"],
    ["Del Rosario","spanish","of the rosary"],
    ["Evangelista","spanish","evangelist; bearer of good news"],
    ["Guerrero","spanish","warrior; soldier"],
    ["Ibarra","spanish","near the river; meadow"],
    ["Luna","spanish","moon"],
    ["Manalo","spanish","God is with us"],
    ["Martinez","spanish","son of Martin; warlike"],
    ["Mojica","spanish","from Mojica; place name"],
    ["Montano","spanish","mountain; highland"],
    ["Moreno","spanish","dark; brown-skinned"],
    ["Ocampo","spanish","of the field"],
    ["Palma","spanish","palm tree; triumph"],
    ["Ponce","spanish","fifth; pontoon bridge"],
    ["Robles","spanish","oak trees; strong as oak"],
    ["Magsaysay","traditional","to say; to tell; eloquent"],
    ["Diokno","traditional","honor and principle"],
    ["Katigbak","traditional","from katigbak; a type of plant"],
    ["Maliwat","traditional","brave; courageous; fearless"],
    ["Panahon","traditional","weather; time; season"],
    ["Balingit","traditional","graceful; fluid movement"],
    ["Sicat","traditional","lightning; swift; quick"],
    ["Manalang","traditional","one who prays; devout"],
    ["Magpantay","traditional","to balance; to equalize"],
    ["Magbuhos","traditional","to pour; to dedicate oneself"],
    ["Magdangal","traditional","to bring honor; to dignify"],
    ["Magtibay","traditional","to strengthen; to reinforce"],
    ["Magalang","traditional","polite; respectful; courteous"],
    ["Tinio","traditional","a type of hardwood tree"],
    ["Sumulong","traditional","to advance; to move forward"],
    ["Crisostomo","traditional","golden-mouthed; eloquent speaker"],
    ["Lukban","traditional","pomelo fruit"],
    ["Manglapus","traditional","wing of a bird; soaring"],
    ["Maranan","traditional","junction; crossroads"],
    ["Masangkay","traditional","tall; lofty; towering"],
    ["Panganiban","traditional","one who faces danger"],
    ["Manalansan","traditional","to pray earnestly; deeply devout"],
    ["Ilustre","traditional","illustrious; distinguished"],
    ["Buenaventura","traditional","good fortune; happy journey"],
    ["Lacson","traditional","quick; sharp"],
    ["Lumbera","traditional","torch bearer; one who brings light"],
    ["Yabut","traditional","from yabut; a type of crab"],
    ["Pangilinan","traditional","one who fasts; devout"],
    ["Pimentel","traditional","one who deals in spice"],
    ["Macaraeg","traditional","one who smooths the way"],
    ["Tagamolila","traditional","violet flower; gentle spirit"]
  ]
}
```

- [ ] **Step 2: Validate JSON**

```bash
python3 -c "import json; data=json.load(open('wordineer-deploy/data/philippine-names.json')); print(f'first: {len(data[\"first\"])}, last: {len(data[\"last\"])}')"
```

Expected output: `first: 190, last: 91` (approximate — exact count depends on above data).

- [ ] **Step 3: Check file size**

```bash
ls -lh wordineer-deploy/data/philippine-names.json
```

Expected: under 60KB.

- [ ] **Step 4: Commit**

```bash
git add wordineer-deploy/data/philippine-names.json
git commit -m "feat: add philippine-names.json dataset for Filipino name generator"
```

---

## Task 2: Update `template-deploy/tools.json`

**Files:**
- Modify: `template-deploy/tools.json`

- [ ] **Step 1: Add to `mega` — Name generators section**

In the `mega` array, find the object with `"cat": "Name generators"` and add to its `tools` array:

```json
{ "href": "/random-filipino-name-generator/", "text": "Filipino names" }
```

The Name generators section becomes:
```json
{
  "cat": "Name generators",
  "tools": [
    { "href": "/index.html",                             "text": "Random word generator" },
    { "href": "/random-name-generator/",                 "text": "Random name" },
    { "href": "/random-filipino-name-generator/",        "text": "Filipino names" },
    { "href": "/username-generator/",                    "text": "Username generator" },
    { "href": "/fantasy-name-generator/",                "text": "Fantasy name gen" },
    { "href": "/baby-name-finder/",                      "text": "Baby name finder" },
    { "href": "/pet-name-generator/",                    "text": "Pet name gen" }
  ]
}
```

- [ ] **Step 2: Add to `more_word_tools`**

Append this entry to the `more_word_tools` array (after the `random-name-generator` entry):

```json
{
  "href": "/random-filipino-name-generator/",
  "name": "Random Filipino name",
  "desc": "Filipino names with meanings — traditional, Spanish-colonial, modern, and nickname styles.",
  "icon_bg": "#F5E6E6",
  "icon_path": "<circle cx=\"6.5\" cy=\"4\" r=\"2.2\" stroke=\"#C0392B\" stroke-width=\"1.1\"/><path d=\"M1.5 11.5c0-2.8 2.2-5 5-5s5 2.2 5 5\" stroke=\"#C0392B\" stroke-width=\"1.1\" stroke-linecap=\"round\"/>",
  "new": true
}
```

- [ ] **Step 3: Add to `other_tools` — Name generators section**

Find the `other_tools` object with `"cat": "Name generators"` and add to its `links` array:

```json
{ "href": "/random-filipino-name-generator/", "text": "Random Filipino name generator" }
```

- [ ] **Step 4: Add to `footer_cols` — Name generators section**

Find the `footer_cols` object with `"title": "Name generators"` and add to its `links` array:

```json
{ "href": "/random-filipino-name-generator/", "text": "Filipino name gen" }
```

- [ ] **Step 5: Validate JSON**

```bash
python3 -c "import json; json.load(open('template-deploy/tools.json')); print('tools.json valid')"
```

Expected: `tools.json valid`

- [ ] **Step 6: Commit**

```bash
git add template-deploy/tools.json
git commit -m "feat: register random-filipino-name-generator in tools.json"
```

---

## Task 3: Create `template-deploy/tools-src/random-filipino-name-generator.html`

**Files:**
- Create: `template-deploy/tools-src/random-filipino-name-generator.html`

- [ ] **Step 1: Create the full tool-src file**

Create `template-deploy/tools-src/random-filipino-name-generator.html` with the following complete content:

```html
<!-- CONFIG { "url": "/random-filipino-name-generator/", "output": "random-filipino-name-generator.html", "type": "tool" } -->

<!-- SLOT:meta -->
<title>Random Filipino Name Generator — 280+ Names with Meanings | Wordineer</title>
<meta name="description" content="Generate random Filipino names instantly — traditional Tagalog, Spanish-colonial, modern, and nickname styles. Meanings shown under every result. Filter by gender and style. Free, no sign-up.">
<link rel="canonical" href="https://wordineer.com/random-filipino-name-generator/">
<meta property="og:type"        content="website">
<meta property="og:site_name"   content="Wordineer">
<meta property="og:title"       content="Random Filipino Name Generator | Wordineer">
<meta property="og:description" content="Generate Filipino names with meanings — traditional, Spanish-colonial, modern, and nickname styles. Filter by gender and style. Free, no sign-up.">
<meta property="og:url"         content="https://wordineer.com/random-filipino-name-generator/">
<meta property="og:image"       content="https://wordineer.com/og-image.png">
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "What are the most common Filipino surnames?",
      "acceptedAnswer": { "@type": "Answer", "text": "The most common Filipino surnames are Santos, Reyes, Cruz, Garcia, and Gonzales. Most are Spanish in origin, introduced during the colonial period. In 1849, a Spanish colonial decree (Claveria) required Filipino families to adopt Spanish surnames from a government catalogue, which is why the most common last names in the Philippines today are Spanish words meaning saints, kings, cross, and similar Catholic concepts." }
    },
    {
      "@type": "Question",
      "name": "What is the difference between traditional and Spanish-colonial Filipino names?",
      "acceptedAnswer": { "@type": "Answer", "text": "Traditional Filipino names come from pre-colonial Tagalog and other indigenous languages. Examples include Ligaya (happiness), Bayani (hero), and Dalisay (pure). Spanish-colonial names arrived with over three centuries of Spanish rule and Catholic influence. Examples include Jose, Maria, Santos, and Cruz. Today, both coexist — a person named Bayani Santos has a traditional first name and a Spanish-colonial surname, a combination that is entirely common." }
    },
    {
      "@type": "Question",
      "name": "Are Filipino names gender-specific?",
      "acceptedAnswer": { "@type": "Answer", "text": "Most Filipino names are gender-specific, but there are exceptions. Traditional names like Diwa (spirit), Lakas (strength), and Mahal (love) are used for both boys and girls. Modern Western names like Alex, Sam, and Jordan are also used as unisex. In the Filipino nickname tradition, some terms like Nong (short for Manong) can apply across genders in informal usage." }
    },
    {
      "@type": "Question",
      "name": "How do Filipino nicknames work?",
      "acceptedAnswer": { "@type": "Answer", "text": "Filipino nicknames are an integral part of the culture. Common patterns include reduplication (Jojo, Nono, Boboy), diminutive suffixes (-oy for boys as in Totoy and Dodong, -eng/-eng for girls as in Neng and Leng), and shortened forms of formal names (Tess from Teresa, Tonyo from Antonio, Jun from Junior). Many Filipinos are known almost exclusively by their nickname rather than their given name." }
    },
    {
      "@type": "Question",
      "name": "Can I use these names for fiction?",
      "acceptedAnswer": { "@type": "Answer", "text": "Yes — all names generated here are real Filipino names drawn from authentic cultural sources. You can use them freely for fiction, screenplays, game characters, or any creative project. For writers, the style filter is especially useful: pick Traditional for historical or rural Philippine settings, Spanish-colonial for upper-class or older-generation characters, Modern for contemporary urban characters, and Nickname for casual or close-community portrayals. Names are not copyrightable." }
    }
  ]
}
</script>
<!-- /SLOT:meta -->

<!-- SLOT:style -->
<style>
.tool-wrap  { max-width:960px; margin:0 auto; padding:24px 24px 0; }
.tool-card  { border:1px solid var(--border); border-radius:var(--radius-lg); overflow:hidden; background:var(--bg); box-shadow:var(--shadow); }
.tool-split { display:flex; }

.ctrl       { width:220px; flex-shrink:0; padding:18px; border-right:1px solid var(--border-2); background:var(--bg-2); }
.ctrl-row   { margin-bottom:14px; }
.ctrl-label { font-size:10px; font-weight:600; color:var(--text-3); text-transform:uppercase; letter-spacing:.06em; display:block; margin-bottom:5px; }
.ctrl-row input, .ctrl-row select { width:100%; padding:7px 10px; font-size:13px; font-family:inherit; border:1px solid var(--border); border-radius:7px; background:var(--bg); color:var(--text); appearance:none; outline:none; transition:border-color .15s; }
.ctrl-row input:focus, .ctrl-row select:focus { border-color:var(--brand); }
.gen-btn    { width:100%; padding:10px 14px; background:var(--brand); color:white; border:none; border-radius:8px; font-size:14px; font-weight:600; font-family:inherit; cursor:pointer; transition:background .15s,transform .1s; letter-spacing:-.01em; }
.gen-btn:hover { background:var(--brand-dark); }
.gen-btn:active { transform:scale(.98); }
.reset-btn  { display:block; width:100%; text-align:center; font-size:11px; color:var(--text-3); margin-top:8px; cursor:pointer; text-decoration:underline; text-underline-offset:2px; border:none; background:none; font-family:inherit; }
.kbd        { text-align:center; font-size:10px; color:var(--text-3); margin-top:6px; }
.kbd kbd    { background:var(--bg-3); border:1px solid var(--border); border-radius:3px; padding:1px 5px; font-size:10px; font-family:inherit; }

.words-panel { flex:1; display:flex; flex-direction:column; overflow:hidden; }
.words-top  { display:flex; align-items:center; justify-content:space-between; padding:12px 16px; border-bottom:1px solid var(--border-2); }
.words-count { font-size:12px; color:var(--text-3); }
.words-actions { display:flex; gap:6px; }
.act-btn    { font-size:12px; padding:5px 11px; border:1px solid var(--border); border-radius:6px; background:var(--bg); color:var(--text-2); cursor:pointer; font-family:inherit; transition:background .12s; }
.act-btn:hover { background:var(--bg-2); }
.word-list  { flex:1; overflow-y:auto; list-style:none; padding:0 16px; margin:0; }
.word-item  { display:flex; align-items:flex-start; justify-content:space-between; padding:12px 0; border-bottom:1px solid var(--border-2); gap:10px; animation:fadeIn .2s ease; }
@keyframes fadeIn { from{opacity:0;transform:translateY(4px)} to{opacity:1;transform:none} }
.word-item:last-child { border-bottom:none; }
.word-left  { flex:1; }
.word-right { display:flex; align-items:flex-start; gap:4px; padding-top:2px; flex-shrink:0; }
.icon-btn   { width:28px; height:28px; display:flex; align-items:center; justify-content:center; background:transparent; border:none; cursor:pointer; border-radius:5px; color:var(--text-3); transition:background .12s,color .12s; }
.icon-btn:hover { background:var(--bg-2); color:var(--text); }
.icon-btn svg { width:14px; height:14px; }
.icon-btn.saved { color:#E24B4A; }

.saved-section { padding:12px 16px; border-top:1px solid var(--border-2); }
.saved-top  { display:flex; align-items:center; justify-content:space-between; margin-bottom:7px; }
.saved-label { font-size:10px; font-weight:600; color:var(--text-3); text-transform:uppercase; letter-spacing:.06em; }
.saved-copy { font-size:11px; color:var(--brand); cursor:pointer; text-decoration:underline; text-underline-offset:2px; border:none; background:none; font-family:inherit; }
.saved-tags { display:flex; gap:5px; flex-wrap:wrap; min-height:22px; }
.saved-tag  { font-size:11px; padding:3px 10px; background:var(--brand-light); color:var(--brand-dark); border-radius:20px; display:flex; align-items:center; gap:4px; }
.saved-tag-remove { cursor:pointer; opacity:.6; font-size:13px; line-height:1; }
.saved-tag-remove:hover { opacity:1; }
.saved-empty { font-size:12px; color:var(--text-3); font-style:italic; }

/* Filipino name specific */
.word-text  { font-size:17px; font-weight:600; color:var(--text); line-height:1.25; }
.pf-badge   { display:inline-block; font-size:10px; font-weight:600; text-transform:uppercase; letter-spacing:.05em; padding:2px 8px; border-radius:10px; margin-top:4px; }
.pf-badge--traditional { background:#E8F4E8; color:#2D6B2D; }
.pf-badge--spanish     { background:#FDF3E3; color:#8B4513; }
.pf-badge--modern      { background:#E8F0FE; color:#1A56DB; }
.pf-badge--nickname    { background:#FEE8F0; color:#C41E6A; }
.ng-meaning { font-size:12px; color:var(--text-3); margin-top:3px; font-style:italic; }

.ng-mobile-toggle { display:none; width:100%; margin:-2px 0 14px; padding:9px 12px; border:1px solid var(--border); border-radius:8px; background:var(--bg); color:var(--brand); font-size:13px; font-weight:600; font-family:inherit; cursor:pointer; }
.ng-advanced { display:block; }

@media(max-width:700px){
  .tool-wrap { padding:14px 16px 0; }
  .tool-split { flex-direction:column; }
  .ctrl { width:100%; border-right:none; border-bottom:1px solid var(--border-2); }
  .reset-btn, .kbd { display:none; }
  .word-list { max-height:440px; overflow-y:auto; }
  .ng-mobile-toggle { display:block; }
  .ng-advanced { display:none; }
  .ng-advanced.is-open { display:block; }
  .hero { padding:12px 16px 12px; }
  .hero-badge { margin-bottom:6px; }
  .hero h1 { font-size:24px; }
}
</style>
<!-- /SLOT:style -->

<!-- SLOT:hero -->
<div class="hero">
  <div class="hero-badge">
    <svg viewBox="0 0 11 11" fill="none"><circle cx="5.5" cy="5.5" r="4.5" stroke="#3C3489" stroke-width="1"/><path d="M3.5 5.5l1.5 1.5L8 3.5" stroke="#3C3489" stroke-width="1.2" stroke-linecap="round"/></svg>
    Free · No sign-up · Instant
  </div>
  <h1>Random Filipino name generator</h1>
  <p>Generate male, female, and unisex Filipino names with meanings — traditional Tagalog, Spanish-colonial, modern, and nickname styles. One click, no sign-up.</p>
</div>
<!-- /SLOT:hero -->

<!-- SLOT:tool -->
<div class="tool-wrap">
  <div class="tool-card">
    <div class="tool-split">

      <!-- LEFT: controls -->
      <div class="ctrl">
        <div class="ctrl-row">
          <label class="ctrl-label" for="pf-count">Number of names</label>
          <input type="number" id="pf-count" value="5" min="1" max="50" inputmode="numeric">
          <span class="pf-count-error" id="pf-count-error" style="display:none;font-size:11px;color:#E24B4A;margin-top:4px;">Enter a number from 1 to 50</span>
        </div>

        <button type="button" class="ng-mobile-toggle" id="pf-mobile-toggle" aria-expanded="false" aria-controls="pf-advanced">More options</button>

        <div class="ng-advanced" id="pf-advanced">
          <div class="ctrl-row">
            <label class="ctrl-label" for="pf-gender">Gender</label>
            <select id="pf-gender">
              <option value="any">Any</option>
              <option value="m">Male</option>
              <option value="f">Female</option>
            </select>
          </div>
          <div class="ctrl-row">
            <label class="ctrl-label" for="pf-style">Style</label>
            <select id="pf-style">
              <option value="any">Any</option>
              <option value="traditional">Traditional Tagalog</option>
              <option value="spanish">Spanish-colonial</option>
              <option value="modern">Modern / Western</option>
              <option value="nickname">Nickname form</option>
            </select>
          </div>
          <div class="ctrl-row">
            <label class="ctrl-label" for="pf-type">Name type</label>
            <select id="pf-type">
              <option value="first">First name only</option>
              <option value="full">Full name</option>
              <option value="last">Last name only</option>
            </select>
          </div>
          <div class="ctrl-row">
            <label class="ctrl-label" for="pf-letter">First letter</label>
            <select id="pf-letter">
              <option value="">Any letter</option>
              <option>A</option><option>B</option><option>C</option><option>D</option>
              <option>E</option><option>F</option><option>G</option><option>H</option>
              <option>I</option><option>J</option><option>K</option><option>L</option>
              <option>M</option><option>N</option><option>O</option><option>P</option>
              <option>Q</option><option>R</option><option>S</option><option>T</option>
              <option>U</option><option>V</option><option>W</option><option>X</option>
              <option>Y</option><option>Z</option>
            </select>
          </div>
        </div>

        <button class="gen-btn" id="pf-gen-btn">Generate names</button>
        <button class="reset-btn" id="pf-reset-btn">Reset options</button>
        <div class="kbd">Press <kbd>Space</kbd> to regenerate</div>

        <div class="ad-sidebar">
          <span class="ad-sidebar-tag">Ad</span>
          <div class="ad-sidebar-logo">
            <svg viewBox="0 0 32 32" fill="none" width="32" height="32"><circle cx="16" cy="16" r="14" fill="#15a249"/><path d="M10 16c0-3.3 2.7-6 6-6s6 2.7 6 6-2.7 6-6 6" stroke="white" stroke-width="2" stroke-linecap="round"/><circle cx="16" cy="16" r="2.5" fill="white"/></svg>
            <span class="ad-sidebar-brand">Grammarly</span>
          </div>
          <div class="ad-sidebar-headline">Write with confidence</div>
          <div class="ad-sidebar-body">Fix grammar, improve clarity, and choose the right words — everywhere you write.</div>
          <a href="https://grammarly.com" target="_blank" rel="noopener" class="ad-sidebar-cta">Try free →</a>
          <div class="ad-sidebar-sub">Free plan · No credit card</div>
        </div>
      </div>

      <!-- RIGHT: name results -->
      <div class="words-panel">
        <div class="words-top">
          <span class="words-count" id="pf-count-display">Generating…</span>
          <div class="words-actions">
            <button class="act-btn" id="pf-copy-all-btn">Copy all</button>
          </div>
        </div>
        <ul class="word-list" id="pf-list"></ul>
      </div>

    </div>

    <!-- Saved names -->
    <div class="saved-section">
      <div class="saved-top">
        <span class="saved-label">Saved names</span>
        <button class="saved-copy" id="pf-copy-saved-btn">Copy saved</button>
      </div>
      <div class="saved-tags" id="pf-saved-tags">
        <span class="saved-empty">Click the heart on any name to save it here</span>
      </div>
    </div>

  </div>
</div>
<!-- /SLOT:tool -->

<!-- SLOT:ad_b -->
<div class="ad-leaderboard">
  <div class="ad-leaderboard-inner">
    <span class="ad-tag">Advertisement · 728×90</span>
    <div class="ad-mock-content">
      <div class="ad-title">Grammarly — write with confidence. Grammar, tone &amp; clarity.</div>
      <div class="ad-sub">Used by 30 million people. Works in Google Docs, Gmail, Word and more.</div>
      <a href="https://grammarly.com" target="_blank" rel="noopener" class="ad-mock-cta">Try Grammarly free</a>
    </div>
  </div>
</div>
<!-- /SLOT:ad_b -->

<!-- SLOT:explainer -->
<div class="explainer">
  <h2>What is a random Filipino name generator?</h2>
  <p>A random Filipino name generator picks authentic Filipino names from a curated dataset and delivers them instantly — with meanings shown under every result. This tool lets you filter by gender and style (Traditional Tagalog, Spanish-colonial, Modern/Western, or Nickname form), so you can get exactly the kind of Filipino name your project needs. Every result card shows the name, its style as a badge, and a short meaning drawn from the name's cultural and linguistic roots. No loading, no account required.</p>

  <h2>How Filipino names work</h2>
  <p>Filipino naming is shaped by three major influences. Pre-colonial names — like Ligaya (happiness), Bayani (hero), and Dalisay (pure) — come from Tagalog and other indigenous languages, often carrying meanings tied to nature, virtues, and emotions. Spanish colonization introduced Catholic saint names and Spanish words that became standard surnames: Santos (saints), Reyes (kings), Cruz (cross). A government decree in 1849 required Filipino families to adopt surnames from a Spanish catalogue, which is why most Filipino family names today are Spanish. In the 20th century, American influence brought a wave of English and Western names that remain common today — Faith, Angel, John, and Kevin are as Filipino as Jose and Maria. Across all these layers, Filipinos also maintain a vibrant nickname culture: almost every person has a short, playful "palayaw" used by family and close friends.</p>

  <h2>Types of Filipino names</h2>
  <p><strong>Traditional Tagalog</strong> names come from pre-colonial indigenous roots. They often describe virtues, nature, light, or strength — Ligaya (joy), Tala (star), Lawin (hawk), Kidlat (lightning). These names carry deep cultural resonance and are popular for literary characters and historical settings.</p>
  <p><strong>Spanish-colonial</strong> names arrived with over three centuries of Catholic influence. First names like Jose, Maria, Carmen, and Isabel — and surnames like Santos, Cruz, and Reyes — belong to this category. They remain the most statistically common Filipino names today.</p>
  <p><strong>Modern / Western</strong> names reflect American cultural influence after 1898. Names like Angel, Faith, Christian, and Carlo are fully naturalized into Filipino culture and are especially common among younger generations.</p>
  <p><strong>Nickname forms</strong> are the affectionate diminutives that Filipinos use every day. Totoy, Dodong, Nene, and Inday are not secondary names — for many Filipinos, the nickname is how everyone knows them. Reduplication (Jojo, Nono) and suffix patterns (-ong, -oy, -eng) are hallmarks of this style.</p>

  <h2>For writers and worldbuilders</h2>
  <p>The Style filter is the most useful tool for fiction writers and game designers. Use Traditional for historical Philippine settings or rural communities. Use Spanish-colonial for upper-class families, older-generation characters, or settings in the 19th century. Use Modern for contemporary urban characters. Use Nickname for close-knit community scenes or casual dialogue — a character who goes by Dodong or Nene immediately signals warmth and familiarity. The Full Name type pairs a first name and last name from your selected style, giving you authentic-feeling combinations like Bayani Magsaysay or Maria Santos.</p>

  <h2>Want names from other countries?</h2>
  <p>For random names from 30+ world origins — American, English, Japanese, Arabic, and more — try the <a href="/random-name-generator/">random name generator</a>. It covers over 500 names with the same meanings-inline format.</p>
</div>
<!-- /SLOT:explainer -->

<!-- SLOT:faq -->
<div class="faq">
  <h2 class="faq-title">Frequently asked questions</h2>
  <div class="faq-item open">
    <div class="faq-q"><span class="faq-q-text">What are the most common Filipino surnames?</span><svg class="faq-chevron" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div>
    <div class="faq-a">The most common Filipino surnames are Santos, Reyes, Cruz, Garcia, and Gonzales — all Spanish in origin. They became standard surnames after an 1849 Spanish colonial decree (the Claveria decree) required Filipino families to adopt surnames from a government-issued catalogue of Spanish words. This is why Filipino family names today overwhelmingly reference Catholic concepts (Santos = saints, Cruz = cross, Espiritu = spirit) or Spanish vocabulary (Flores = flowers, Torres = towers, Ramos = branches).</div>
  </div>
  <div class="faq-item">
    <div class="faq-q"><span class="faq-q-text">What is the difference between traditional and Spanish-colonial Filipino names?</span><svg class="faq-chevron" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div>
    <div class="faq-a">Traditional names come from pre-colonial Tagalog and indigenous Philippine languages — Ligaya (happiness), Bayani (hero), Dalisay (pure). They predate Spanish arrival and are often connected to nature, virtues, and emotions. Spanish-colonial names arrived with over 300 years of Spanish rule and Catholic church influence — Jose, Maria, Santos, Cruz. Today both coexist naturally: a person named Bayani Santos has a traditional first name and a Spanish-colonial surname, a combination that is entirely common across the Philippines.</div>
  </div>
  <div class="faq-item">
    <div class="faq-q"><span class="faq-q-text">Are Filipino names gender-specific?</span><svg class="faq-chevron" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div>
    <div class="faq-a">Most Filipino names are gender-specific, but the traditional pool includes genuine unisex names. Diwa (spirit), Lakas (strength), and Mahal (love) are used across genders. Modern Western imports like Alex, Sam, and Jordan are also unisex. Spanish-colonial names are generally strongly gendered (Jose/Maria, Pedro/Rosa). In the nickname tradition, some terms like Nong (short for Manong or Manang) adapt informally across genders in everyday speech.</div>
  </div>
  <div class="faq-item">
    <div class="faq-q"><span class="faq-q-text">How do Filipino nicknames work?</span><svg class="faq-chevron" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div>
    <div class="faq-a">Filipino nicknames (palayaw) follow recognisable patterns. Reduplication doubles a syllable or short name: Jojo, Nono, Boboy. Diminutive suffixes mark gender: -oy and -ong for boys (Totoy, Dodong, Nonong), -eng and -it for girls (Neng, Leng, Nit). Many nicknames are shortened forms of formal names — Tess from Teresa, Tonyo from Antonio, Jun from Junior. Filipinos often go through life almost exclusively by their nickname; a person's legal name may be Ricardo but everyone from family to coworkers calls him Ricky or Ric.</div>
  </div>
  <div class="faq-item">
    <div class="faq-q"><span class="faq-q-text">Can I use these names for fiction?</span><svg class="faq-chevron" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div>
    <div class="faq-a">Yes — all names here are real Filipino names drawn from authentic cultural sources. Names are not copyrightable. For fiction, the Style filter is your main tool: Traditional for historical or rural Philippine settings, Spanish-colonial for upper-class or older-generation characters, Modern for contemporary urban characters, Nickname for close-knit or informal community scenes. The Full Name type gives you authentic first + last combinations. Save your favourites with the heart icon and copy them all in one click.</div>
  </div>
</div>
<!-- /SLOT:faq -->

<!-- SLOT:who -->
<div>
  <h2 class="section-title" style="margin-bottom:14px">Who uses this tool</h2>
  <div class="uc-grid">
    <div class="uc"><div class="uc-title">Writers &amp; screenwriters</div><div class="uc-body">Find authentic Filipino character names for fiction, scripts, and games. Filter by style to match your story's setting and era</div></div>
    <div class="uc"><div class="uc-title">Genealogists</div><div class="uc-body">Research Filipino naming conventions and understand the cultural roots behind surnames and given names in your family history</div></div>
    <div class="uc"><div class="uc-title">Expecting parents</div><div class="uc-body">Explore Filipino names with meanings. Save your favourites and share your shortlist — traditional, modern, or something in between</div></div>
    <div class="uc"><div class="uc-title">Game designers</div><div class="uc-body">Build believable Filipino characters for games and tabletop RPGs. The style filter makes it easy to match naming conventions to your setting</div></div>
  </div>
</div>
<!-- /SLOT:who -->

<!-- SLOT:init -->
<script>
const PF_STYLE_LABELS = {
  traditional: 'Traditional',
  spanish:     'Spanish-colonial',
  modern:      'Modern',
  nickname:    'Nickname'
};

const PF_SEED = {
  first: [
    ["Ligaya","f","traditional","happiness; joy"],
    ["Bayani","m","traditional","hero; patriot"],
    ["Dalisay","f","traditional","pure; clean"],
    ["Diwa","u","traditional","spirit; soul; essence"],
    ["Jose","m","spanish","God will increase"],
    ["Maria","f","spanish","beloved; wished-for child"],
    ["Santos","m","spanish","saints"],
    ["Angel","f","modern","divine messenger"],
    ["John","m","modern","God is gracious"],
    ["Faith","f","modern","trust; belief"],
    ["Nene","f","nickname","baby girl; term of endearment"],
    ["Totoy","m","nickname","little boy; term for a young boy"]
  ],
  last: [
    ["Santos","spanish","saints"],
    ["Reyes","spanish","kings"],
    ["Cruz","spanish","cross"],
    ["Flores","spanish","flowers"],
    ["Magsaysay","traditional","to say; to tell; eloquent"],
    ["Balingit","traditional","graceful; fluid movement"]
  ]
};

function pfMapData(raw) {
  return {
    first: (raw.first || []).map(function(n) { return { n: n[0], g: n[1], s: n[2], m: n[3] }; }),
    last:  (raw.last  || []).map(function(n) { return { n: n[0], s: n[1], m: n[2] }; })
  };
}

const pfActiveData = pfMapData(PF_SEED);
let pfDataIsFull = false;
let pfDataPromise = null;
let pfDataScheduled = false;
let pfDataTimer = null;
let pfRenderedFallback = false;

async function pfLoadFullData() {
  if (pfDataPromise) return pfDataPromise;
  pfDataPromise = (async function() {
    try {
      const res = await fetch('/data/philippine-names.json', { cache: 'force-cache' });
      if (!res.ok) throw new Error(res.status);
      const raw = await res.json();
      if (!Array.isArray(raw.first) || !Array.isArray(raw.last)) throw new Error('Invalid data');
      const data = pfMapData(raw);
      pfActiveData.first = data.first;
      pfActiveData.last  = data.last;
      pfDataIsFull = true;
      if (pfRenderedFallback) document.getElementById('pf-gen-btn')?.click();
    } catch (err) {
      if (!pfDataIsFull) WORDINEER.showToast('Using starter names while the full list loads.');
      pfDataPromise = null;
      pfDataScheduled = false;
    }
  })();
  return pfDataPromise;
}

function pfScheduleData(delay) {
  const wait = delay || 0;
  if (pfDataIsFull) return;
  if (pfDataScheduled) {
    if (wait > 0 || !pfDataTimer) return;
    clearTimeout(pfDataTimer);
  }
  pfDataScheduled = true;
  pfDataTimer = setTimeout(function() {
    pfDataTimer = null;
    const run = function() { pfLoadFullData().catch(function() {}); };
    if ('requestIdleCallback' in window) {
      window.requestIdleCallback(run, { timeout: 5000 });
    } else {
      run();
    }
  }, wait);
}

function pfScheduleDataAfterLoad() {
  const schedule = function() { pfScheduleData(2500); };
  if (document.readyState === 'complete') {
    schedule();
  } else {
    window.addEventListener('load', schedule, { once: true });
  }
}

function pfShuffle(arr) {
  const a = [...arr];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

function pfGenerateFn(data) {
  pfRenderedFallback = !pfDataIsFull;
  const raw = parseInt(document.getElementById('pf-count')?.value);
  if (isNaN(raw) || raw < 1 || raw > 50) return [];
  const count  = raw;
  const gender = document.getElementById('pf-gender')?.value || 'any';
  const style  = document.getElementById('pf-style')?.value  || 'any';
  const type   = document.getElementById('pf-type')?.value   || 'first';
  const letter = document.getElementById('pf-letter')?.value || '';

  let firstPool = data.first.filter(function(n) {
    if (gender !== 'any' && n.g !== gender && n.g !== 'u') return false;
    if (style  !== 'any' && n.s !== style) return false;
    if (letter && !n.n.toUpperCase().startsWith(letter)) return false;
    return true;
  });

  let lastPool = data.last.filter(function(n) {
    if (style !== 'any' && n.s !== style) return false;
    if (type === 'last' && letter && !n.n.toUpperCase().startsWith(letter)) return false;
    return true;
  });

  const sf = pfShuffle(firstPool);
  const sl = pfShuffle(lastPool);
  const results = [];
  const seen = new Set();
  let fi = 0, li = 0;

  while (results.length < count) {
    if (type === 'first' && fi >= sf.length) break;
    if (type === 'last'  && li >= sl.length) break;
    if (type === 'full'  && (fi >= sf.length || li >= sl.length)) break;

    const fn = sf[fi];
    const ln = sl[li];
    let display, meaning, nameStyle;

    if (type === 'first') {
      display = fn.n; meaning = fn.m; nameStyle = fn.s;
      fi++;
    } else if (type === 'last') {
      display = ln.n; meaning = ln.m; nameStyle = ln.s;
      li++;
    } else {
      display = fn.n + ' ' + ln.n; meaning = fn.m; nameStyle = fn.s;
      fi++; li++;
    }

    if (!seen.has(display)) {
      seen.add(display);
      results.push({ display: display, meaning: meaning, style: nameStyle });
    }
  }
  return results;
}

function pfRenderItem(item) {
  let savedArr = [];
  try { savedArr = JSON.parse(localStorage.getItem('wnr_saved_filipino_names') || '[]'); } catch {}
  const isSaved    = savedArr.includes(item.display);
  const styleLabel = PF_STYLE_LABELS[item.style] || item.style;
  const safeAttr   = item.display.replace(/"/g, '&quot;');
  const safeClick  = item.display.replace(/\\/g, '\\\\').replace(/'/g, "\\'");
  return '<li class="word-item">'
    + '<div class="word-left">'
    +   '<div class="word-text">' + item.display + '</div>'
    +   '<span class="pf-badge pf-badge--' + item.style + '">' + styleLabel + '</span>'
    +   '<div class="ng-meaning">' + item.meaning + '</div>'
    + '</div>'
    + '<div class="word-right">'
    +   '<button class="icon-btn" title="Copy" onclick="pfCopyName(\'' + safeClick + '\',this)">'
    +     '<svg viewBox="0 0 14 14" fill="none"><rect x="1" y="4" width="9" height="9.5" rx="1.5" stroke="currentColor" stroke-width="1.1"/><path d="M4.5 4V2.5A1.5 1.5 0 016 1h5.5A1.5 1.5 0 0113 2.5v7a1.5 1.5 0 01-1.5 1.5H10" stroke="currentColor" stroke-width="1.1"/></svg>'
    +   '</button>'
    +   '<button class="icon-btn' + (isSaved ? ' saved' : '') + '" title="' + (isSaved ? 'Unsave' : 'Save') + '" data-action="save" data-name="' + safeAttr + '">'
    +     '<svg viewBox="0 0 16 16" fill="none"><path d="M8 13.5S2 9.5 2 5.5A3 3 0 018 4a3 3 0 016 1.5c0 4-6 8-6 8z" stroke="currentColor" stroke-width="1.3" fill="' + (isSaved ? '#E24B4A' : 'none') + '" stroke-linecap="round"/></svg>'
    +   '</button>'
    + '</div>'
    + '</li>';
}

window.pfCopyName = function(name, btn) {
  navigator.clipboard?.writeText(name);
  const orig = btn.innerHTML;
  btn.innerHTML = '<svg viewBox="0 0 14 14" fill="none"><path d="M2 7l3.5 3.5 6.5-6.5" stroke="#1D9E75" stroke-width="1.3" stroke-linecap="round"/></svg>';
  setTimeout(function() { btn.innerHTML = orig; }, 900);
  WORDINEER.showToast('Copied: ' + name);
};

(function() {
  WORDINEER.init({
    mode:           'custom',
    data:           pfActiveData,
    renderItem:     pfRenderItem,
    generateFn:     pfGenerateFn,
    listId:         'pf-list',
    countDisplayId: 'pf-count-display',
    generateBtnId:  'pf-gen-btn',
    copyAllBtnId:   'pf-copy-all-btn',
    savedKey:       'wnr_saved_filipino_names',
    savedListId:    'pf-saved-tags'
  });

  pfScheduleDataAfterLoad();

  // Count validation
  const pfCountInput = document.getElementById('pf-count');
  const pfCountError = document.getElementById('pf-count-error');
  function pfValidateCount() {
    const v = parseInt(pfCountInput.value);
    const invalid = isNaN(v) || v < 1 || v > 50;
    pfCountError.style.display = invalid ? 'block' : 'none';
    pfCountInput.style.borderColor = invalid ? '#E24B4A' : '';
    return !invalid;
  }
  function pfRegenerateFromFilters() {
    if (!pfValidateCount()) return;
    if (!pfDataIsFull) {
      pfLoadFullData()
        .then(function() { document.getElementById('pf-gen-btn')?.click(); })
        .catch(function() { document.getElementById('pf-gen-btn')?.click(); });
      return;
    }
    document.getElementById('pf-gen-btn')?.click();
  }
  pfCountInput?.addEventListener('input', pfValidateCount);
  pfCountInput?.addEventListener('change', pfRegenerateFromFilters);

  ['pf-gender','pf-style','pf-type','pf-letter'].forEach(function(id) {
    const el = document.getElementById(id);
    if (!el) return;
    el.addEventListener('change', pfRegenerateFromFilters);
    el.addEventListener('input',  pfRegenerateFromFilters);
  });

  document.getElementById('pf-gen-btn')?.addEventListener('click', function() {
    pfScheduleData(0);
  });

  document.addEventListener('keydown', function(e) {
    if ((e.code === 'Space' || e.code === 'Enter') && !['INPUT','SELECT','TEXTAREA','BUTTON'].includes(e.target.tagName)) {
      pfScheduleData(0);
    }
  }, true);

  document.getElementById('pf-reset-btn')?.addEventListener('click', function() {
    pfScheduleData(0);
    document.getElementById('pf-count').value  = '5';
    pfValidateCount();
    document.getElementById('pf-gender').value = 'any';
    document.getElementById('pf-style').value  = 'any';
    document.getElementById('pf-type').value   = 'first';
    document.getElementById('pf-letter').value = '';
    document.getElementById('pf-gen-btn').click();
  });

  document.getElementById('pf-copy-saved-btn')?.addEventListener('click', function() {
    const tags = document.querySelectorAll('#pf-saved-tags .saved-tag');
    if (!tags.length) return;
    const names = Array.from(tags).map(function(t) { return t.textContent.replace('×','').trim(); }).filter(Boolean);
    navigator.clipboard?.writeText(names.join('\n'));
    WORDINEER.showToast('Saved names copied!');
  });

  const toggle   = document.getElementById('pf-mobile-toggle');
  const advanced = document.getElementById('pf-advanced');
  if (toggle && advanced) {
    toggle.addEventListener('click', function() {
      const isOpen = advanced.classList.toggle('is-open');
      toggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
      toggle.textContent = isOpen ? 'Hide options' : 'More options';
    });
  }
})();

(function bindWordineerMenu(){
  const mega = document.getElementById("mega");
  const hbg = document.querySelector(".hamburger");
  if (!mega || !hbg) return;
  hbg.onclick = null;
  hbg.removeAttribute("onclick");
  hbg.setAttribute("role","button");
  hbg.setAttribute("tabindex","0");
  hbg.setAttribute("aria-controls","mega");
  hbg.setAttribute("aria-expanded",mega.classList.contains("open")?"true":"false");
  function setMenu(open){ mega.classList.toggle("open",open); hbg.setAttribute("aria-expanded",open?"true":"false"); }
  function toggleMenu(e){ e.preventDefault(); e.stopPropagation(); setMenu(!mega.classList.contains("open")); }
  hbg.addEventListener("click",toggleMenu);
  hbg.addEventListener("keydown",function(e){ if(e.key==="Enter"||e.key===" ") toggleMenu(e); });
  document.addEventListener("click",function(e){ if(mega.classList.contains("open")&&!mega.contains(e.target)&&!hbg.contains(e.target)) setMenu(false); });
})();
</script>
<!-- /SLOT:init -->
```

- [ ] **Step 2: Build and verify output is generated**

```bash
cd template-deploy && python3 build.py
```

Expected: build completes with no errors and `output/random-filipino-name-generator.html` exists.

```bash
ls -lh template-deploy/output/random-filipino-name-generator.html
```

Expected: file exists, size > 20KB.

- [ ] **Step 3: Commit**

```bash
git add template-deploy/tools-src/random-filipino-name-generator.html
git commit -m "feat: add random-filipino-name-generator tool-src page"
```

---

## Task 4: Update `template-deploy/tools-src/random-name-generator.html` — Add related tools section

**Files:**
- Modify: `template-deploy/tools-src/random-name-generator.html`

- [ ] **Step 1: Add "More name generators" section to the explainer slot**

In `template-deploy/tools-src/random-name-generator.html`, find the end of the `<!-- SLOT:explainer -->` block. It currently ends with the teachers paragraph and `</div>`. Add the following section immediately before the closing `</div>`:

```html

  <h2>More name generators</h2>
  <p>Looking for names from a specific country or culture? Explore the name generator cluster:</p>
  <ul>
    <li><a href="/random-filipino-name-generator/">Random Filipino name generator</a> — traditional, Spanish-colonial, modern, and nickname styles with meanings</li>
    <li><a href="/random-american-name-generator/">Random American name generator</a> — first and last names across American naming traditions</li>
    <li><a href="/random-word-generator/">Random word generator</a> — for vocabulary building, games, and creative prompts</li>
  </ul>
```

The closing `</div>` of the explainer slot should remain as-is after this addition.

- [ ] **Step 2: Rebuild to confirm no build errors**

```bash
cd template-deploy && python3 build.py
```

Expected: build completes with no errors.

- [ ] **Step 3: Commit**

```bash
git add template-deploy/tools-src/random-name-generator.html
git commit -m "feat: add name generator cluster links to random-name-generator explainer"
```

---

## Task 5: Add redirect rule to `wordineer-deploy/_redirects`

**Files:**
- Modify: `wordineer-deploy/_redirects`

- [ ] **Step 1: Add the clean URL redirect**

In `wordineer-deploy/_redirects`, add these two lines in the "Clean URLs" section (after the existing `.html` to trailing-slash rules):

```
/random-filipino-name-generator.html  /random-filipino-name-generator/  301
/random-filipino-name-generator/      /random-filipino-name-generator.html  200
```

The first line redirects direct `.html` URL accesses to the clean URL. The second serves the actual HTML file at the clean URL (rewrite, not redirect).

- [ ] **Step 2: Commit**

```bash
git add wordineer-deploy/_redirects
git commit -m "feat: add clean URL redirect for random-filipino-name-generator"
```

---

## Task 6: Build, copy output, preview, and verify

**Files:**
- Generated: `wordineer-deploy/random-filipino-name-generator.html`

- [ ] **Step 1: Full build**

```bash
cd template-deploy && python3 build.py
```

Expected: no errors, `output/random-filipino-name-generator.html` and updated `output/random-name-generator.html` present.

- [ ] **Step 2: Copy output to deploy folder**

```bash
cp template-deploy/output/*.html wordineer-deploy/
```

- [ ] **Step 3: Start local server**

```bash
cd wordineer-deploy && python3 -m http.server 8080
```

- [ ] **Step 4: Verify Filipino generator — default state**

Open `http://localhost:8080/random-filipino-name-generator.html`

Check:
- Page loads with no console errors
- 5 names generate immediately from seed data (no blank list)
- Each result shows: name, style badge (coloured correctly), meaning in italics

- [ ] **Step 5: Verify Filipino generator — filters**

Test each filter combination:
1. Gender = Male → all results should be male or unisex names
2. Gender = Female → all results should be female or unisex names
3. Style = Traditional Tagalog → badge on each result reads "Traditional" (green badge)
4. Style = Spanish-colonial → badge reads "Spanish-colonial" (brown/tan badge)
5. Style = Modern / Western → badge reads "Modern" (blue badge)
6. Style = Nickname form → badge reads "Nickname" (pink badge)
7. Name type = Full name → results show "FirstName LastName" format
8. Name type = Last name only → results are surnames only
9. Starting letter = M → all names begin with M

- [ ] **Step 6: Verify count validation**

1. Set count to `0` → red border on input, error text "Enter a number from 1 to 50" appears, no names generate
2. Set count to `51` → same error behaviour
3. Set count to `50` → 50 names generate (may hit pool limit — that's acceptable, tool shows as many as available)
4. Set count back to `5` → error clears, names generate normally

- [ ] **Step 7: Verify save and copy**

1. Click heart icon on a name → name appears as pink tag in "Saved names" section
2. Click heart again → name removed from saved section
3. Click "Copy all" → toast "Copied X names" appears
4. Click "Copy saved" → toast "Saved names copied!" appears

- [ ] **Step 8: Verify mobile More options toggle**

Resize browser to mobile width (≤700px) or use DevTools device mode:
- "More options" button is visible
- Clicking it reveals the Gender, Style, Name type, Starting letter controls
- Button text changes to "Hide options"
- Clicking again collapses the panel

- [ ] **Step 9: Verify random-name-generator internal links**

Open `http://localhost:8080/random-name-generator.html`

Scroll to the explainer section. Verify:
- "More name generators" heading is present
- Link to `/random-filipino-name-generator/` is present and correct
- Link to `/random-american-name-generator/` is present (stub — 404 is acceptable at this stage)
- Link to `/random-word-generator/` is present

- [ ] **Step 10: Verify tools.json injected sections**

On `http://localhost:8080/random-filipino-name-generator.html`:
- Mega nav → "Name generators" section includes "Filipino names" link
- More tools grid below the tool includes the "Random Filipino name" card with red icon

On `http://localhost:8080/random-name-generator.html`:
- More tools grid includes the "Random Filipino name" card

- [ ] **Step 11: Final commit**

```bash
git add wordineer-deploy/random-filipino-name-generator.html wordineer-deploy/random-name-generator.html
git commit -m "feat: deploy random-filipino-name-generator and updated random-name-generator"
```

---

## Summary of all commits

1. `feat: add philippine-names.json dataset for Filipino name generator`
2. `feat: register random-filipino-name-generator in tools.json`
3. `feat: add random-filipino-name-generator tool-src page`
4. `feat: add name generator cluster links to random-name-generator explainer`
5. `feat: add clean URL redirect for random-filipino-name-generator`
6. `feat: deploy random-filipino-name-generator and updated random-name-generator`

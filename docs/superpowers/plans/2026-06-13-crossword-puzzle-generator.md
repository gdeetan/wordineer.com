# Crossword Puzzle Generator Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a full Crossword Puzzle Generator at `/crossword-puzzle-generator/` — auto-generate from curated word list, custom word/clue input, print output, interactive browser solve mode, and shareable URL hash — all client-side.

**Architecture:** Vanilla JS/HTML/CSS via the existing tools-src build system. A greedy grid layout algorithm places words on a coordinate grid, rendered as an HTML table. Puzzle state serializes to base64 URL hash for sharing. Data loaded via `fetch()` on first generate.

**Tech Stack:** Vanilla JS (ES5-compatible, no libraries), HTML table for grid, `window.print()` + `@media print` CSS, `btoa/atob` for URL encoding.

---

## File Map

| Action | Path | Purpose |
|--------|------|---------|
| Create | `wordineer-deploy/data/crossword-words.json` | ~400 curated words, 3 tiers × 8 categories |
| Create | `template-deploy/tools-src/crossword-puzzle-generator.html` | Full tool source (all slots) |
| Modify | `template-deploy/tools-src/word-tools.html` | Activate crossword placeholder link |
| Modify | `template-deploy/tools.json` | Add to mega + more_word_tools + footer_cols |
| Modify | `wordineer-deploy/_redirects` | Clean URL rules |
| Modify | `wordineer-deploy/sitemap.xml` | Add URL entry |

---

### Task 1: Create crossword-words.json

**Files:**
- Create: `wordineer-deploy/data/crossword-words.json`

- [ ] **Step 1: Write the data file**

```json
{
  "easy": {
    "animals": [
      {"w":"CAT","c":"A pet that meows and purrs"},
      {"w":"DOG","c":"A loyal pet that barks"},
      {"w":"COW","c":"A farm animal that gives milk"},
      {"w":"HEN","c":"A female chicken"},
      {"w":"PIG","c":"A farm animal that rolls in mud"},
      {"w":"ANT","c":"A small insect that lives in colonies"},
      {"w":"BEE","c":"An insect that makes honey"},
      {"w":"OWL","c":"A nocturnal bird known for wisdom"},
      {"w":"FOX","c":"A clever orange wild animal"},
      {"w":"APE","c":"A primate closely related to humans"},
      {"w":"FROG","c":"An amphibian that croaks and leaps"},
      {"w":"DUCK","c":"A bird that swims and quacks"},
      {"w":"BEAR","c":"A large furry animal that hibernates"},
      {"w":"DEER","c":"A graceful forest animal with antlers"},
      {"w":"HAWK","c":"A bird of prey with sharp talons"},
      {"w":"LAMB","c":"A young sheep"},
      {"w":"MOLE","c":"A small burrowing mammal"},
      {"w":"TOAD","c":"A warty amphibian similar to a frog"}
    ],
    "science": [
      {"w":"SUN","c":"The star at the center of our solar system"},
      {"w":"MOON","c":"Earth's natural satellite"},
      {"w":"STAR","c":"A ball of burning gas in space"},
      {"w":"RAIN","c":"Water that falls from clouds"},
      {"w":"SNOW","c":"Frozen precipitation that forms flakes"},
      {"w":"WIND","c":"Moving air that can power turbines"},
      {"w":"ROCK","c":"A solid piece of mineral matter"},
      {"w":"ATOM","c":"The smallest unit of a chemical element"},
      {"w":"SEED","c":"The start of a new plant"},
      {"w":"ROOT","c":"The part of a plant that absorbs water underground"},
      {"w":"HEAT","c":"A form of energy transferred by temperature"},
      {"w":"SOIL","c":"The layer of earth where plants grow"},
      {"w":"WAVE","c":"A moving ridge of water or energy"},
      {"w":"TIDE","c":"The rise and fall of the ocean"},
      {"w":"MIST","c":"Thin cloud at ground level"},
      {"w":"CELL","c":"The basic unit of all living things"}
    ],
    "geography": [
      {"w":"HILL","c":"A raised area of land smaller than a mountain"},
      {"w":"LAKE","c":"A body of water surrounded by land"},
      {"w":"CAVE","c":"A hollow space in rock or underground"},
      {"w":"CAPE","c":"A point of land jutting into the sea"},
      {"w":"ISLE","c":"A small island"},
      {"w":"GULF","c":"A large area of sea partly enclosed by land"},
      {"w":"DUNE","c":"A mound of sand shaped by the wind"},
      {"w":"MOOR","c":"An open, boggy upland area"},
      {"w":"VALE","c":"A broad river valley"},
      {"w":"PORT","c":"A place where ships dock"},
      {"w":"PLAIN","c":"A large flat area of land"},
      {"w":"RIVER","c":"A flowing body of fresh water"},
      {"w":"CLIFF","c":"A steep rock face by the sea"},
      {"w":"MARSH","c":"A low waterlogged area of land"},
      {"w":"FJORD","c":"A long narrow inlet between cliffs"}
    ],
    "food": [
      {"w":"MILK","c":"A white drink produced by cows"},
      {"w":"BREAD","c":"A staple food made by baking dough"},
      {"w":"APPLE","c":"A round red or green fruit"},
      {"w":"GRAPE","c":"A small fruit that grows in clusters"},
      {"w":"HONEY","c":"A sweet sticky substance made by bees"},
      {"w":"LEMON","c":"A sour yellow citrus fruit"},
      {"w":"ONION","c":"A pungent vegetable that can make you cry"},
      {"w":"RICE","c":"A staple grain eaten by billions"},
      {"w":"CORN","c":"A yellow grain also called maize"},
      {"w":"PEAR","c":"A sweet fruit narrow at the top"},
      {"w":"PLUM","c":"A small purple stone fruit"},
      {"w":"OATS","c":"A grain often eaten as porridge"},
      {"w":"MINT","c":"An herb used to flavor food and drinks"},
      {"w":"KALE","c":"A dark leafy green vegetable"},
      {"w":"BEET","c":"A root vegetable with deep red juice"},
      {"w":"LIME","c":"A small green citrus fruit"}
    ],
    "sports": [
      {"w":"RUN","c":"To move quickly on foot"},
      {"w":"SWIM","c":"To move through water using the body"},
      {"w":"JUMP","c":"To push off the ground into the air"},
      {"w":"GOLF","c":"A sport played with clubs and a small ball"},
      {"w":"YOGA","c":"An exercise practice with poses and breathing"},
      {"w":"DIVE","c":"To leap headfirst into water"},
      {"w":"RACE","c":"A competition to see who is fastest"},
      {"w":"TEAM","c":"A group of players on the same side"},
      {"w":"GOAL","c":"The target in many sports"},
      {"w":"BALL","c":"A round object used in many games"},
      {"w":"PASS","c":"To throw or send the ball to a teammate"},
      {"w":"BASE","c":"A marker in baseball that runners must touch"},
      {"w":"LANE","c":"A marked section of a track or pool"},
      {"w":"GAME","c":"A competitive activity with rules"},
      {"w":"KICK","c":"To strike something with the foot"}
    ],
    "school": [
      {"w":"PEN","c":"A writing tool that uses ink"},
      {"w":"BOOK","c":"A collection of written pages bound together"},
      {"w":"DESK","c":"A flat surface for writing and studying"},
      {"w":"NOTE","c":"A short written message or reminder"},
      {"w":"POEM","c":"A piece of writing with rhythm"},
      {"w":"MATH","c":"The study of numbers and shapes"},
      {"w":"TEST","c":"An assessment of knowledge"},
      {"w":"QUIZ","c":"A short test of knowledge"},
      {"w":"NOUN","c":"A word that names a person, place, or thing"},
      {"w":"VERB","c":"A word that expresses action or being"},
      {"w":"SORT","c":"To arrange items into groups"},
      {"w":"READ","c":"To understand written words"},
      {"w":"DRAW","c":"To make a picture with a pencil or pen"},
      {"w":"EXAM","c":"A formal test of academic knowledge"},
      {"w":"RULE","c":"A principle or regulation to be followed"}
    ],
    "nature": [
      {"w":"OAK","c":"A common hardwood tree that produces acorns"},
      {"w":"FLY","c":"A two-winged insect"},
      {"w":"WEB","c":"A silky trap spun by a spider"},
      {"w":"BUD","c":"A new growth on a plant before it opens"},
      {"w":"DEW","c":"Water droplets that form on surfaces overnight"},
      {"w":"LOG","c":"A section of a tree trunk"},
      {"w":"LEAF","c":"The flat green part of a plant"},
      {"w":"BARK","c":"The outer covering of a tree"},
      {"w":"NEST","c":"A structure built by birds to hold eggs"},
      {"w":"FERN","c":"A flowerless plant with feathery fronds"},
      {"w":"MOSS","c":"A soft green plant that grows on rocks"},
      {"w":"VINE","c":"A climbing or trailing plant"},
      {"w":"POND","c":"A small body of still water"},
      {"w":"TWIG","c":"A small slender branch"},
      {"w":"CLAM","c":"A shellfish that filters water"}
    ],
    "technology": [
      {"w":"CODE","c":"Instructions written for a computer"},
      {"w":"FILE","c":"A collection of data stored on a computer"},
      {"w":"LINK","c":"A connection between web pages"},
      {"w":"CHAT","c":"Text-based communication online"},
      {"w":"BYTE","c":"A unit of digital information"},
      {"w":"DATA","c":"Information processed by a computer"},
      {"w":"CHIP","c":"A tiny electronic circuit in a device"},
      {"w":"SCAN","c":"To digitize a document using a device"},
      {"w":"TEXT","c":"Written characters sent digitally"},
      {"w":"DISK","c":"A flat circular storage medium"},
      {"w":"ICON","c":"A small picture representing a program"},
      {"w":"PORT","c":"A connection point on a computer"},
      {"w":"GRID","c":"A network of lines forming squares"},
      {"w":"WIFI","c":"Wireless internet connection technology"},
      {"w":"FEED","c":"A stream of updated content online"}
    ]
  },
  "medium": {
    "animals": [
      {"w":"HORSE","c":"A large domesticated animal used for riding"},
      {"w":"EAGLE","c":"A large bird of prey with excellent eyesight"},
      {"w":"SHARK","c":"A powerful ocean predator with sharp teeth"},
      {"w":"TIGER","c":"A large striped wild cat of Asia"},
      {"w":"ZEBRA","c":"An African animal with black and white stripes"},
      {"w":"CAMEL","c":"A desert animal with a humped back"},
      {"w":"PANDA","c":"A black and white bear from China"},
      {"w":"KOALA","c":"An Australian marsupial that eats eucalyptus"},
      {"w":"RABBIT","c":"A small furry mammal with long ears"},
      {"w":"PARROT","c":"A colorful bird that can mimic speech"},
      {"w":"PYTHON","c":"A large constrictor snake"},
      {"w":"JAGUAR","c":"A spotted big cat of South America"},
      {"w":"FALCON","c":"A fast bird of prey used in hunting"},
      {"w":"SALMON","c":"A fish that swims upstream to spawn"},
      {"w":"WALRUS","c":"A large marine mammal with long tusks"},
      {"w":"COYOTE","c":"A wild dog of North America"}
    ],
    "science": [
      {"w":"PLANT","c":"A living organism that uses photosynthesis"},
      {"w":"CLOUD","c":"A mass of water droplets in the sky"},
      {"w":"MAGNET","c":"An object that attracts iron and steel"},
      {"w":"FOSSIL","c":"Remains of an ancient organism in rock"},
      {"w":"COMET","c":"A ball of ice and rock orbiting the sun"},
      {"w":"ORBIT","c":"The path of one object around another"},
      {"w":"PRISM","c":"A glass shape that splits light into colors"},
      {"w":"VIRUS","c":"A tiny agent that causes disease"},
      {"w":"SPORE","c":"A reproductive cell from plants and fungi"},
      {"w":"PETAL","c":"A colorful leaf-like part of a flower"},
      {"w":"NERVE","c":"A fiber that transmits signals in the body"},
      {"w":"OZONE","c":"A gas in the atmosphere that blocks UV rays"},
      {"w":"RADAR","c":"A system that detects objects using radio waves"},
      {"w":"CLONE","c":"An exact genetic copy of an organism"},
      {"w":"PULSE","c":"The rhythmic beat of the heart"}
    ],
    "geography": [
      {"w":"JUNGLE","c":"A dense tropical forest"},
      {"w":"ARCTIC","c":"The cold region around the North Pole"},
      {"w":"CANYON","c":"A deep gorge cut by a river"},
      {"w":"DESERT","c":"A dry region with little rainfall"},
      {"w":"VALLEY","c":"Low land between hills or mountains"},
      {"w":"TUNDRA","c":"A treeless Arctic landscape with frozen soil"},
      {"w":"HARBOR","c":"A sheltered area of water near land"},
      {"w":"SUMMIT","c":"The highest point of a mountain"},
      {"w":"RAPIDS","c":"A section of river where water flows fast"},
      {"w":"LAGOON","c":"A shallow body of water separated from the sea"},
      {"w":"STEPPE","c":"A flat treeless grassland in Eurasia"},
      {"w":"DELTA","c":"A landform at the mouth of a river"},
      {"w":"CRATER","c":"A bowl-shaped depression in the ground"},
      {"w":"TRENCH","c":"A long narrow valley on the ocean floor"},
      {"w":"PLAINS","c":"A large flat grassy region"}
    ],
    "food": [
      {"w":"MANGO","c":"A sweet tropical fruit with yellow flesh"},
      {"w":"OLIVE","c":"A small oily fruit used to make oil"},
      {"w":"PASTA","c":"An Italian food made from wheat dough"},
      {"w":"GINGER","c":"A spicy root used in cooking and medicine"},
      {"w":"CASHEW","c":"A curved tropical nut"},
      {"w":"MUFFIN","c":"A small round baked good for breakfast"},
      {"w":"FENNEL","c":"An anise-flavored herb used in cooking"},
      {"w":"WALNUT","c":"A wrinkled nut with a hard brown shell"},
      {"w":"ALMOND","c":"A nutritious nut used in many dishes"},
      {"w":"SHERBET","c":"A frozen dessert made with fruit juice"},
      {"w":"WAFFLE","c":"A crisp batter cake cooked in a patterned iron"},
      {"w":"CLOVES","c":"Dried flower buds used as a spice"},
      {"w":"SALAMI","c":"A cured sausage from Italy"},
      {"w":"LENTIL","c":"A small flat edible legume"},
      {"w":"CARAMEL","c":"A sweet sticky confection from heated sugar"}
    ],
    "sports": [
      {"w":"RUGBY","c":"A contact sport played with an oval ball"},
      {"w":"TENNIS","c":"A racket sport played on a court"},
      {"w":"HOCKEY","c":"A game played with sticks and a puck"},
      {"w":"BOXING","c":"A combat sport using fists"},
      {"w":"SPRINT","c":"A short race run at full speed"},
      {"w":"HURDLE","c":"A barrier to jump over in a race"},
      {"w":"RODEO","c":"A competition of cowboy skills"},
      {"w":"ARCHER","c":"Someone who shoots arrows at a target"},
      {"w":"COACH","c":"A person who trains athletes"},
      {"w":"TROPHY","c":"A prize awarded for winning"},
      {"w":"LEAGUE","c":"A group of teams that compete together"},
      {"w":"FINALS","c":"The last round of a competition"},
      {"w":"PODIUM","c":"A raised platform for award ceremonies"},
      {"w":"FENCER","c":"An athlete who competes with a sword"},
      {"w":"JOCKEY","c":"A person who rides horses in races"}
    ],
    "school": [
      {"w":"ESSAY","c":"A short piece of writing on a topic"},
      {"w":"DRAFT","c":"An early version of a piece of writing"},
      {"w":"ATLAS","c":"A collection of maps in book form"},
      {"w":"RULER","c":"A straight tool used to measure length"},
      {"w":"PENCIL","c":"A writing tool with a graphite core"},
      {"w":"THESIS","c":"The main argument of an essay"},
      {"w":"DEBATE","c":"A formal discussion of opposing views"},
      {"w":"FIGURE","c":"A diagram or statistical number in a text"},
      {"w":"SYNTAX","c":"The rules governing sentence structure"},
      {"w":"CLAUSE","c":"A group of words with a subject and verb"},
      {"w":"SYMBOL","c":"A mark or character representing something"},
      {"w":"CHORUS","c":"A repeated section of a poem or song"},
      {"w":"MARGIN","c":"The blank space around text on a page"},
      {"w":"CIPHER","c":"A coded system of writing"},
      {"w":"PERIOD","c":"A punctuation mark ending a sentence"}
    ],
    "nature": [
      {"w":"FOREST","c":"A large area covered with trees"},
      {"w":"POLLEN","c":"A powder produced by flowers for reproduction"},
      {"w":"BURROW","c":"A tunnel dug by an animal to live in"},
      {"w":"CANOPY","c":"The top layer of leaves in a forest"},
      {"w":"GLACIER","c":"A slow-moving mass of ice"},
      {"w":"HABITAT","c":"The natural environment of an animal"},
      {"w":"CURRENT","c":"A steady flow of water or air"},
      {"w":"MINERAL","c":"A naturally occurring solid substance"},
      {"w":"BEDROCK","c":"The solid rock beneath soil"},
      {"w":"ESTUARY","c":"Where a river meets the sea"},
      {"w":"BRAMBLE","c":"A thorny shrub that bears blackberries"},
      {"w":"WETLAND","c":"Land saturated with water"},
      {"w":"EROSION","c":"The wearing away of land by water or wind"},
      {"w":"THICKET","c":"A dense growth of shrubs and small trees"},
      {"w":"THUNDER","c":"The loud sound that follows lightning"}
    ],
    "technology": [
      {"w":"SERVER","c":"A computer that provides data to others"},
      {"w":"ROUTER","c":"A device that directs internet traffic"},
      {"w":"CURSOR","c":"A moveable pointer on a computer screen"},
      {"w":"BACKUP","c":"A copy of data kept in case of loss"},
      {"w":"SENSOR","c":"A device that detects environmental changes"},
      {"w":"PIXEL","c":"The smallest unit of a digital image"},
      {"w":"REBOOT","c":"To restart a computer system"},
      {"w":"FILTER","c":"A tool that separates or selects data"},
      {"w":"PLUGIN","c":"Software that adds features to an application"},
      {"w":"UPLOAD","c":"To transfer data from a device to the internet"},
      {"w":"DOMAIN","c":"The address of a website"},
      {"w":"COOKIE","c":"A small piece of data stored by a browser"},
      {"w":"STREAM","c":"To watch or listen to media online"},
      {"w":"PROMPT","c":"A cue shown to a user to enter information"},
      {"w":"SEARCH","c":"To look for information online"}
    ]
  },
  "hard": {
    "animals": [
      {"w":"CHEETAH","c":"The fastest land animal on Earth"},
      {"w":"PLATYPUS","c":"A mammal that lays eggs and has a duck bill"},
      {"w":"NARWHAL","c":"An Arctic whale with a long spiral tusk"},
      {"w":"MONGOOSE","c":"A small predator known for fighting cobras"},
      {"w":"MANATEE","c":"A large slow-moving marine mammal"},
      {"w":"MANDRILL","c":"A large colorful primate of central Africa"},
      {"w":"PORCUPINE","c":"A rodent covered in sharp quills"},
      {"w":"SCORPION","c":"An arachnid with a venomous tail stinger"},
      {"w":"ARMADILLO","c":"A mammal with a bony protective shell"},
      {"w":"PELICAN","c":"A large water bird with a pouched bill"},
      {"w":"FLAMINGO","c":"A pink wading bird that stands on one leg"},
      {"w":"WOLVERINE","c":"A fierce mammal from northern forests"},
      {"w":"CHAMELEON","c":"A lizard that can change its skin color"},
      {"w":"ALBATROSS","c":"A large seabird with the longest wingspan"},
      {"w":"TAPIR","c":"A large pig-like mammal of South America"}
    ],
    "science": [
      {"w":"MOLECULE","c":"Two or more atoms bonded together"},
      {"w":"ELECTRON","c":"A negatively charged particle orbiting the nucleus"},
      {"w":"TELESCOPE","c":"An instrument for viewing distant objects in space"},
      {"w":"ECOSYSTEM","c":"A community of organisms and their environment"},
      {"w":"ISOTOPE","c":"Atoms of same element with different neutrons"},
      {"w":"AMPLITUDE","c":"The maximum displacement of a wave"},
      {"w":"COMBUSTION","c":"A rapid reaction that produces heat and light"},
      {"w":"REFRACTION","c":"The bending of light between materials"},
      {"w":"SYMBIOSIS","c":"A close relationship between two different species"},
      {"w":"SEDIMENT","c":"Material deposited by water, wind, or ice"},
      {"w":"PHOTON","c":"The smallest unit of light energy"},
      {"w":"ENTROPY","c":"A measure of disorder in a system"},
      {"w":"MUTATION","c":"A permanent change in the genetic code"},
      {"w":"GERMINATION","c":"The process by which a seed sprouts"},
      {"w":"CHRYSALIS","c":"The protective case of a developing butterfly"}
    ],
    "geography": [
      {"w":"HIMALAYAS","c":"The world's highest mountain range in Asia"},
      {"w":"PENINSULA","c":"A strip of land almost surrounded by water"},
      {"w":"TRIBUTARY","c":"A river that flows into a larger river"},
      {"w":"LONGITUDE","c":"Distance east or west measured in degrees"},
      {"w":"LATITUDE","c":"Distance north or south of the equator"},
      {"w":"PATAGONIA","c":"A region at the southern tip of South America"},
      {"w":"ARCHIPELAGO","c":"A group of islands"},
      {"w":"TEMPERATE","c":"A climate with moderate temperatures"},
      {"w":"MANGROVE","c":"A coastal tree with roots in salty water"},
      {"w":"PERMAFROST","c":"Permanently frozen ground in cold regions"},
      {"w":"FLOODPLAIN","c":"Flat land near a river that floods regularly"},
      {"w":"DECIDUOUS","c":"Trees that shed their leaves in autumn"},
      {"w":"BIOSPHERE","c":"The regions of Earth where living things exist"},
      {"w":"EQUATOR","c":"The imaginary line circling the middle of Earth"},
      {"w":"MERIDIAN","c":"A line of longitude on the Earth's surface"}
    ],
    "food": [
      {"w":"ARTICHOKE","c":"A vegetable with tough outer leaves and edible heart"},
      {"w":"POMEGRANATE","c":"A fruit filled with ruby-red seeds"},
      {"w":"ASPARAGUS","c":"A green vegetable that grows as stalks"},
      {"w":"CRANBERRY","c":"A small tart red berry used in sauces"},
      {"w":"SOURDOUGH","c":"Bread made with fermented dough"},
      {"w":"CARDAMOM","c":"A fragrant spice used in chai and baking"},
      {"w":"TURMERIC","c":"A bright yellow spice from the ginger family"},
      {"w":"JALAPEÑO","c":"A medium-hot green chili pepper"},
      {"w":"MOZZARELLA","c":"A soft Italian cheese used on pizza"},
      {"w":"TAMARIND","c":"A sour tropical fruit used in cooking"},
      {"w":"BASMATI","c":"A long-grain aromatic rice from South Asia"},
      {"w":"SAFFRON","c":"The world's most expensive spice from crocus flowers"},
      {"w":"EDAMAME","c":"Young soybeans eaten as a snack"},
      {"w":"PROSCIUTTO","c":"A thin-sliced Italian dry-cured ham"},
      {"w":"KOMBUCHA","c":"A fermented tea drink with probiotics"}
    ],
    "sports": [
      {"w":"TRIATHLON","c":"A race combining swimming, cycling, and running"},
      {"w":"DECATHLON","c":"A ten-event athletic competition"},
      {"w":"GYMNASTICS","c":"A sport involving acrobatic feats and balance"},
      {"w":"LACROSSE","c":"A game played with a long stick and mesh pocket"},
      {"w":"PENTATHLON","c":"A five-event Olympic athletic competition"},
      {"w":"SLALOM","c":"A skiing race through a series of gates"},
      {"w":"EQUESTRIAN","c":"Relating to horse riding as a sport"},
      {"w":"VELODROME","c":"An arena designed for track cycling"},
      {"w":"SQUASH","c":"A racket sport played in an enclosed court"},
      {"w":"BIATHLON","c":"A winter sport combining skiing and rifle shooting"},
      {"w":"LUGE","c":"A one-person sled sport on an icy track"},
      {"w":"DRESSAGE","c":"A competition testing horse obedience and movement"},
      {"w":"BOBSLED","c":"A steered sled raced on an icy track"},
      {"w":"STEEPLECHASE","c":"A long-distance race with water jumps and hurdles"},
      {"w":"MARATHON","c":"A long-distance foot race of 26.2 miles"}
    ],
    "school": [
      {"w":"BIBLIOGRAPHY","c":"A list of sources used in writing"},
      {"w":"ALGORITHM","c":"A step-by-step procedure for solving a problem"},
      {"w":"HYPOTHESIS","c":"A testable prediction in a scientific experiment"},
      {"w":"PROTAGONIST","c":"The main character in a story"},
      {"w":"METAPHOR","c":"A figure of speech comparing two unlike things directly"},
      {"w":"DENOMINATOR","c":"The bottom number of a fraction"},
      {"w":"CURRICULUM","c":"The subjects taught in a school"},
      {"w":"SYNTHESIS","c":"Combining elements to form a new whole"},
      {"w":"NARRATIVE","c":"A spoken or written account of events"},
      {"w":"INFERENCE","c":"A conclusion reached by reasoning from evidence"},
      {"w":"PARABOLA","c":"A curved line shaped like an arc"},
      {"w":"PERIMETER","c":"The distance around the outside of a shape"},
      {"w":"QUADRANT","c":"One of four sections divided by axes"},
      {"w":"PARLIAMENT","c":"A legislative assembly that makes laws"},
      {"w":"SUBORDINATE","c":"A clause that cannot stand alone as a sentence"}
    ],
    "nature": [
      {"w":"POLLINATION","c":"The transfer of pollen to fertilize plants"},
      {"w":"HIBERNATION","c":"A state of deep sleep during winter"},
      {"w":"CAMOUFLAGE","c":"Coloring that helps an animal blend in"},
      {"w":"PREDATOR","c":"An animal that hunts other animals for food"},
      {"w":"MIGRATION","c":"The seasonal movement of animals to new areas"},
      {"w":"DECOMPOSER","c":"An organism that breaks down dead matter"},
      {"w":"WATERSHED","c":"Land area draining into a river system"},
      {"w":"SUCCESSION","c":"The gradual change in an ecosystem over time"},
      {"w":"SOLSTICE","c":"When the sun is furthest from the equator"},
      {"w":"FLUORESCENCE","c":"Emission of light absorbed and re-emitted"},
      {"w":"THERMOCLINE","c":"A layer in water where temperature changes rapidly"},
      {"w":"TRANSPIRATION","c":"The process by which plants release water vapor"},
      {"w":"BIODIVERSITY","c":"The variety of life in a given area"},
      {"w":"GERMINATION","c":"The sprouting of a seed into a new plant"},
      {"w":"CARNIVORE","c":"An animal that eats only meat"}
    ],
    "technology": [
      {"w":"BANDWIDTH","c":"The rate at which data is transmitted"},
      {"w":"ENCRYPTION","c":"The process of encoding data for security"},
      {"w":"BLOCKCHAIN","c":"A decentralized digital ledger of transactions"},
      {"w":"HYPERLINK","c":"A clickable reference in a webpage"},
      {"w":"COMPILER","c":"Software that converts code into machine language"},
      {"w":"DATABASE","c":"An organized collection of structured information"},
      {"w":"INTERFACE","c":"A point where two systems or users interact"},
      {"w":"RECURSION","c":"A function that calls itself to solve a problem"},
      {"w":"PROTOTYPE","c":"An early sample or model of a product"},
      {"w":"PARAMETER","c":"A variable used in a programming function"},
      {"w":"FIRMWARE","c":"Software embedded in a hardware device"},
      {"w":"RENDERING","c":"The process of generating an image from data"},
      {"w":"MIDDLEWARE","c":"Software connecting different applications"},
      {"w":"CONTAINER","c":"An isolated environment for running software"},
      {"w":"VIRTUALIZE","c":"To create a simulated version of a resource"}
    ]
  }
}
```

- [ ] **Step 2: Verify the file is valid JSON**

```bash
python3 -c "import json; d=json.load(open('wordineer-deploy/data/crossword-words.json')); print('OK — easy cats:', list(d['easy'].keys()), 'total easy:', sum(len(v) for v in d['easy'].values()))"
```

Expected output: `OK — easy cats: ['animals', 'science', 'geography', 'food', 'sports', 'school', 'nature', 'technology'] total easy: 128` (or similar count ≥ 120)

- [ ] **Step 3: Commit**

```bash
git add wordineer-deploy/data/crossword-words.json
git commit -m "feat: add crossword-words.json dataset (400 words, 3 tiers × 8 categories)"
```

---

### Task 2: Create tool HTML — CONFIG, meta, style, hero slots

**Files:**
- Create: `template-deploy/tools-src/crossword-puzzle-generator.html`

- [ ] **Step 1: Write CONFIG + meta slot**

Create the file with this content as the opening:

```html
<!-- CONFIG
{
  "url": "/crossword-puzzle-generator/",
  "output": "crossword-puzzle-generator.html",
  "type": "tool",
  "more_tools_key": "more_word_tools",
  "more_tools_title": "More word tools",
  "more_tools_subtitle": "Word generators, games, and puzzle tools — all free"
}
-->

<!-- SLOT:meta -->
<title>Crossword Puzzle Generator — Free, Printable & Shareable | Wordineer</title>
<meta name="description" content="Free crossword puzzle generator. Enter your own words and clues or auto-generate from 400+ curated words. Print blank puzzles, share a link, or solve in your browser — no sign-up needed.">
<link rel="canonical" href="https://wordineer.com/crossword-puzzle-generator/">
<meta property="og:type"        content="website">
<meta property="og:site_name"   content="Wordineer">
<meta property="og:title"       content="Free Crossword Puzzle Generator | Wordineer">
<meta property="og:description" content="Make a custom crossword in seconds. Add your own words and clues, or pick a topic and let the generator do the work. Print, solve, and share — all client-side.">
<meta property="og:url"         content="https://wordineer.com/crossword-puzzle-generator/">
<meta property="og:image"       content="https://wordineer.com/og-image.png">
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "How many words can I add to a crossword?",
      "acceptedAnswer": { "@type": "Answer", "text": "You can add up to 30 custom words. The layout algorithm tries to connect as many as possible through shared letters. Words that can't be linked to the rest of the grid are skipped — aim for 10–20 words for the best density." }
    },
    {
      "@type": "Question",
      "name": "Can I print a blank version for students?",
      "acceptedAnswer": { "@type": "Answer", "text": "Yes. Click Print Blank to open the print dialog with letters hidden — students see only the empty grid and clue numbers. Click Print with Answers to print the filled-in solution." }
    },
    {
      "@type": "Question",
      "name": "How do I share my puzzle?",
      "acceptedAnswer": { "@type": "Answer", "text": "Click Share to copy a link to your clipboard. The puzzle is encoded in the URL — no account needed, no server storage. Anyone with the link can open and solve the puzzle." }
    }
  ]
}
</script>
<!-- /SLOT:meta -->
```

- [ ] **Step 2: Add style slot**

Append to the file:

```html
<!-- SLOT:style -->
<style>
/* ── Tabs ──────────────────────────────────── */
.cw-tabs{display:flex;gap:8px;margin-bottom:16px}
.cw-tab{padding:8px 20px;border:1.5px solid #D1D9E0;border-radius:20px;background:#fff;cursor:pointer;font-size:.875rem;color:#555;transition:background .15s,color .15s,border-color .15s;line-height:1.4}
.cw-tab.active{background:#3C3489;color:#fff;border-color:#3C3489}
.cw-tab:hover:not(.active){border-color:#3C3489;color:#3C3489}

/* ── Controls ──────────────────────────────── */
.cw-controls{display:flex;gap:16px;flex-wrap:wrap;margin-bottom:16px;align-items:flex-end}
.cw-ctrl{display:flex;flex-direction:column;gap:5px}
.cw-ctrl label{font-size:.75rem;font-weight:700;color:#888;text-transform:uppercase;letter-spacing:.05em}
.cw-select{padding:8px 32px 8px 12px;border:1.5px solid #D1D9E0;border-radius:8px;font-size:.9rem;background:#fff url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='10' height='6'%3E%3Cpath d='M0 0l5 6 5-6z' fill='%23888'/%3E%3C/svg%3E") no-repeat right 10px center;-webkit-appearance:none;appearance:none;cursor:pointer}

/* ── Textarea ──────────────────────────────── */
.cw-textarea{width:100%;padding:12px;border:1.5px solid #D1D9E0;border-radius:8px;font-family:ui-monospace,monospace;font-size:.875rem;resize:vertical;box-sizing:border-box;min-height:160px;line-height:1.6}
.cw-textarea:focus{outline:none;border-color:#3C3489}
.cw-error{color:#E24B4A;font-size:.85rem;margin-top:6px}

/* ── Generate button (reuse site pattern) ─── */
.cw-panel .gen-btn{margin-top:12px}

/* ── Output area ───────────────────────────── */
.cw-output{display:flex;gap:28px;margin-top:24px;flex-wrap:wrap;align-items:flex-start}
.cw-grid-wrap{flex:0 0 auto;overflow-x:auto;max-width:100%}
.cw-table{border-collapse:collapse;table-layout:fixed}
.cw-table td{width:32px;height:32px;padding:0;box-sizing:border-box}
.cw-black{background:#222}
.cw-cell{border:1.5px solid #aaa;background:#fff;position:relative;vertical-align:middle;text-align:center;cursor:default}
.cw-num{position:absolute;top:1px;left:2px;font-size:9px;line-height:1;color:#333;pointer-events:none;user-select:none}
.cw-letter{font-size:.95rem;font-weight:700;color:#1a1a2e;display:block;line-height:32px;user-select:none}

/* ── Solve mode ────────────────────────────── */
.cw-input{width:100%;height:100%;border:none;background:transparent;text-align:center;font-size:.95rem;font-weight:700;text-transform:uppercase;padding:0;cursor:text;outline:none;color:#1a1a2e;caret-color:#3C3489;position:absolute;top:0;left:0}
.cw-cell{overflow:hidden}
.cw-cell.cw-correct{background:#D1FAE5}
.cw-cell.cw-wrong{background:#FEE2E2}
.cw-cell.cw-selected{background:#EEF0FB}

/* ── Clues ─────────────────────────────────── */
.cw-clues-wrap{flex:1;min-width:200px;max-width:380px}
.cw-clues-section{margin-bottom:20px}
.cw-clues-title{font-size:.8rem;font-weight:700;text-transform:uppercase;letter-spacing:.08em;color:#888;margin:0 0 8px}
.cw-clue-list{padding:0;margin:0;list-style:none}
.cw-clue-list li{font-size:.875rem;color:#444;line-height:1.5;margin-bottom:5px;display:flex;gap:6px}
.cw-clue-list li b{flex:0 0 auto;min-width:24px;color:#3C3489}

/* ── Actions ───────────────────────────────── */
.cw-actions{display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin-top:16px;padding-top:16px;border-top:1px solid #EEF0F3}
.cw-word-count{font-size:.8rem;color:#888;margin-right:auto}
.cw-btn{padding:8px 14px;border:1.5px solid #D1D9E0;border-radius:8px;background:#fff;cursor:pointer;font-size:.8rem;color:#444;transition:all .15s;white-space:nowrap}
.cw-btn:hover{border-color:#3C3489;color:#3C3489}
.cw-btn:disabled{opacity:.4;cursor:not-allowed;pointer-events:none}
.cw-btn--primary{background:#3C3489;color:#fff;border-color:#3C3489}
.cw-btn--primary:hover{background:#2a246b;border-color:#2a246b}

/* ── Empty state ───────────────────────────── */
.cw-empty{color:#bbb;font-size:.9rem;padding:32px 0;text-align:center}

/* ── Toast ─────────────────────────────────── */
.cw-toast{position:fixed;bottom:24px;left:50%;transform:translateX(-50%) translateY(10px);background:#1a1a2e;color:#fff;padding:10px 20px;border-radius:10px;font-size:.875rem;opacity:0;pointer-events:none;transition:opacity .2s,transform .2s;z-index:999;white-space:nowrap}
.cw-toast.show{opacity:1;transform:translateX(-50%) translateY(0)}

/* ── Print ─────────────────────────────────── */
@media print{
  nav,.breadcrumb,.cw-tabs,.cw-panel,.gen-btn,.cw-actions,.cw-toast,
  footer,.ad,[class*="ad-"],[class*="more-tools"]{display:none!important}
  .cw-output{display:flex!important}
  .cw-clue-list li{break-inside:avoid}
}
</style>
<!-- /SLOT:style -->
```

- [ ] **Step 3: Add hero slot**

Append to the file:

```html
<!-- SLOT:hero -->
<div class="breadcrumb">
  <div class="breadcrumb-inner">
    <a href="/">Wordineer</a>
    <span class="breadcrumb-sep">›</span>
    <a href="/word-tools/">Word Tools</a>
    <span class="breadcrumb-sep">›</span>
    <span aria-current="page">Crossword Puzzle Generator</span>
  </div>
</div>
<div class="hero">
  <div class="hero-badge">
    <svg viewBox="0 0 11 11" fill="none"><rect x="1" y="1" width="3.5" height="3.5" rx=".6" stroke="#3C3489" stroke-width="1"/><rect x="6.5" y="1" width="3.5" height="3.5" rx=".6" stroke="#3C3489" stroke-width="1"/><rect x="1" y="6.5" width="3.5" height="3.5" rx=".6" stroke="#3C3489" stroke-width="1"/><rect x="6.5" y="6.5" width="3.5" height="3.5" rx=".6" stroke="#3C3489" stroke-width="1"/></svg>
    Free · No sign-up · Print or solve in browser
  </div>
  <h1>Crossword Puzzle Generator</h1>
  <p>Make a custom crossword in seconds — enter your own words and clues, or auto-generate from 400+ curated words by topic and difficulty. Print blank for students or share a link anyone can solve.</p>
</div>
<!-- /SLOT:hero -->
```

- [ ] **Step 4: Verify file exists and has correct CONFIG**

```bash
head -10 template-deploy/tools-src/crossword-puzzle-generator.html
```

Expected: shows `<!-- CONFIG` block with `"url": "/crossword-puzzle-generator/"`.

- [ ] **Step 5: Commit**

```bash
git add template-deploy/tools-src/crossword-puzzle-generator.html
git commit -m "feat: add crossword tool HTML shell (CONFIG, meta, style, hero)"
```

---

### Task 3: Add tool slot HTML (UI panels + grid container)

**Files:**
- Modify: `template-deploy/tools-src/crossword-puzzle-generator.html` (append)

- [ ] **Step 1: Append tool slot**

```html
<!-- SLOT:tool -->
<div class="tool-wrap">

  <!-- Tab buttons -->
  <div class="cw-tabs">
    <button id="cw-tab-auto" class="cw-tab active" type="button">Auto-Generate</button>
    <button id="cw-tab-custom" class="cw-tab" type="button">Custom Puzzle</button>
  </div>

  <!-- Auto-generate panel -->
  <div id="cw-auto-panel" class="cw-panel">
    <div class="cw-controls">
      <div class="cw-ctrl">
        <label for="cw-difficulty">Difficulty</label>
        <select id="cw-difficulty" class="cw-select">
          <option value="easy">Easy</option>
          <option value="medium" selected>Medium</option>
          <option value="hard">Hard</option>
        </select>
      </div>
      <div class="cw-ctrl">
        <label for="cw-category">Category</label>
        <select id="cw-category" class="cw-select">
          <option value="all">All Categories</option>
          <option value="animals">Animals</option>
          <option value="science">Science</option>
          <option value="geography">Geography</option>
          <option value="food">Food</option>
          <option value="sports">Sports</option>
          <option value="school">School</option>
          <option value="nature">Nature</option>
          <option value="technology">Technology</option>
        </select>
      </div>
    </div>
    <button id="cw-generate-btn" class="gen-btn" type="button">Generate Crossword</button>
  </div>

  <!-- Custom puzzle panel -->
  <div id="cw-custom-panel" class="cw-panel" style="display:none">
    <label class="cw-ctrl" for="cw-custom-input" style="display:block;margin-bottom:8px">
      Enter one word and clue per line: <code>WORD, Your clue here</code>
    </label>
    <textarea id="cw-custom-input" class="cw-textarea"
      placeholder="OCEAN, The largest body of water&#10;TIDE, The rise and fall of the sea&#10;WAVE, A moving ridge of water&#10;CORAL, A reef-building marine organism&#10;SHARK, An apex ocean predator"></textarea>
    <div id="cw-custom-error" class="cw-error" style="display:none" role="alert"></div>
    <button id="cw-generate-custom-btn" class="gen-btn" type="button">Generate Crossword</button>
  </div>

  <!-- Grid output -->
  <div class="cw-output" id="cw-output">
    <div class="cw-grid-wrap" id="cw-grid">
      <div class="cw-empty">Choose a difficulty and category, then click Generate Crossword.</div>
    </div>
    <div class="cw-clues-wrap" id="cw-clues-wrap" style="display:none">
      <div class="cw-clues-section">
        <h3 class="cw-clues-title">Across</h3>
        <ol id="cw-across" class="cw-clue-list"></ol>
      </div>
      <div class="cw-clues-section">
        <h3 class="cw-clues-title">Down</h3>
        <ol id="cw-down" class="cw-clue-list"></ol>
      </div>
    </div>
  </div>

  <!-- Action buttons (hidden until first generate) -->
  <div id="cw-actions" class="cw-actions" style="display:none">
    <span id="cw-word-count" class="cw-word-count"></span>
    <button id="cw-print-blank-btn" class="cw-btn" type="button">Print Blank</button>
    <button id="cw-print-ans-btn" class="cw-btn" type="button">Print Answers</button>
    <button id="cw-solve-btn" class="cw-btn cw-btn--primary" type="button">Solve in Browser</button>
    <button id="cw-check-btn" class="cw-btn cw-btn--primary" type="button" style="display:none">Check Answers</button>
    <button id="cw-reveal-btn" class="cw-btn" type="button" style="display:none">Reveal All</button>
    <button id="cw-exit-solve-btn" class="cw-btn" type="button" style="display:none">Exit Solve</button>
    <button id="cw-share-btn" class="cw-btn" type="button">Share Link</button>
  </div>

  <div id="cw-toast" class="cw-toast" role="status" aria-live="polite"></div>
</div>
<!-- /SLOT:tool -->
```

- [ ] **Step 2: Commit**

```bash
git add template-deploy/tools-src/crossword-puzzle-generator.html
git commit -m "feat: add crossword tool slot HTML (input panels, grid container, action buttons)"
```

---

### Task 4: Add grid algorithm JS (init slot, part 1)

**Files:**
- Modify: `template-deploy/tools-src/crossword-puzzle-generator.html` (append)

- [ ] **Step 1: Append init slot opening + algorithm functions**

```html
<!-- SLOT:init -->
<script>
(function () {
'use strict';

var DATA_URL = '/data/crossword-words.json';
var cwData = null;
var currentResult = null;
var solveMode = false;
var currentTab = 'auto';

/* ── Grid Layout Algorithm ──────────────────────────────────────── */

function placeWord(grid, word, x, y, dir) {
  var dx = dir === 'across' ? 1 : 0, dy = dir === 'down' ? 1 : 0;
  for (var i = 0; i < word.length; i++) {
    grid[(x + i * dx) + ',' + (y + i * dy)] = word[i];
  }
}

function canPlace(grid, word, x, y, dir) {
  var dx = dir === 'across' ? 1 : 0, dy = dir === 'down' ? 1 : 0;
  var px = dir === 'across' ? 0 : 1, py = dir === 'across' ? 1 : 0;

  // Cell immediately before and after the word must be empty
  if (grid[(x - dx) + ',' + (y - dy)]) return false;
  if (grid[(x + word.length * dx) + ',' + (y + word.length * dy)]) return false;

  var intersections = 0;
  for (var i = 0; i < word.length; i++) {
    var cx = x + i * dx, cy = y + i * dy;
    var key = cx + ',' + cy;
    if (grid[key]) {
      if (grid[key] !== word[i]) return false; // letter conflict
      intersections++;
    } else {
      // Empty cell: perpendicular neighbors must be empty (no parallel touching words)
      if (grid[(cx - px) + ',' + (cy - py)]) return false;
      if (grid[(cx + px) + ',' + (cy + py)]) return false;
    }
  }
  return intersections > 0; // must connect to existing grid
}

function scorePlacement(grid, word, x, y, dir) {
  var dx = dir === 'across' ? 1 : 0, dy = dir === 'down' ? 1 : 0;
  var intersections = 0;
  for (var i = 0; i < word.length; i++) {
    if (grid[(x + i * dx) + ',' + (y + i * dy)]) intersections++;
  }
  // More intersections = better; penalize distance from origin
  return intersections * 20 - Math.abs(x) - Math.abs(y);
}

function findBestPlacement(grid, word) {
  var best = null, bestScore = -Infinity;
  var keys = Object.keys(grid);
  for (var ki = 0; ki < keys.length; ki++) {
    var parts = keys[ki].split(',');
    var gx = parseInt(parts[0]), gy = parseInt(parts[1]);
    var letter = grid[keys[ki]];
    for (var li = 0; li < word.length; li++) {
      if (word[li] !== letter) continue;
      // Try across (intersect vertically placed letter)
      var ax = gx - li, ay = gy;
      if (canPlace(grid, word, ax, ay, 'across')) {
        var s = scorePlacement(grid, word, ax, ay, 'across');
        if (s > bestScore) { bestScore = s; best = {x: ax, y: ay, dir: 'across'}; }
      }
      // Try down (intersect horizontally placed letter)
      var dx2 = gx, dy2 = gy - li;
      if (canPlace(grid, word, dx2, dy2, 'down')) {
        var s2 = scorePlacement(grid, word, dx2, dy2, 'down');
        if (s2 > bestScore) { bestScore = s2; best = {x: dx2, y: dy2, dir: 'down'}; }
      }
    }
  }
  return best;
}

function normalize(result) {
  var minX = Infinity, minY = Infinity;
  Object.keys(result.grid).forEach(function(k) {
    var p = k.split(',');
    minX = Math.min(minX, parseInt(p[0]));
    minY = Math.min(minY, parseInt(p[1]));
  });
  var newGrid = {};
  Object.keys(result.grid).forEach(function(k) {
    var p = k.split(','); newGrid[(parseInt(p[0])-minX)+','+(parseInt(p[1])-minY)] = result.grid[k];
  });
  return {
    placed: result.placed.map(function(p) {
      return {word:p.word, clue:p.clue, x:p.x-minX, y:p.y-minY, dir:p.dir};
    }),
    grid: newGrid
  };
}

function renumber(result) {
  var maxX = 0, maxY = 0;
  Object.keys(result.grid).forEach(function(k) {
    var p = k.split(',');
    maxX = Math.max(maxX, parseInt(p[0]));
    maxY = Math.max(maxY, parseInt(p[1]));
  });
  var cellNum = {}, n = 1;
  for (var row = 0; row <= maxY; row++) {
    for (var col = 0; col <= maxX; col++) {
      var k = col + ',' + row;
      if (!result.grid[k]) continue;
      var sa = !result.grid[(col-1)+','+row] && result.grid[(col+1)+','+row];
      var sd = !result.grid[col+','+(row-1)] && result.grid[col+','+(row+1)];
      if (sa || sd) cellNum[k] = n++;
    }
  }
  return {
    placed: result.placed.map(function(p) {
      return {word:p.word, clue:p.clue, x:p.x, y:p.y, dir:p.dir, num:cellNum[p.x+','+p.y]};
    }),
    grid: result.grid, cellNum: cellNum, maxX: maxX, maxY: maxY
  };
}

function buildCrossword(entries) {
  var words = entries.filter(function(e) { return e.w && e.w.length >= 2; })
    .slice().sort(function(a, b) { return b.w.length - a.w.length; });
  if (!words.length) return null;
  var grid = {}, placed = [];
  // Place first word horizontally at origin
  placeWord(grid, words[0].w, 0, 0, 'across');
  placed.push({word:words[0].w, clue:words[0].c, x:0, y:0, dir:'across'});
  for (var wi = 1; wi < words.length; wi++) {
    var bp = findBestPlacement(grid, words[wi].w);
    if (bp) {
      placeWord(grid, words[wi].w, bp.x, bp.y, bp.dir);
      placed.push({word:words[wi].w, clue:words[wi].c, x:bp.x, y:bp.y, dir:bp.dir});
    }
  }
  if (placed.length < 2) return null;
  return renumber(normalize({placed:placed, grid:grid}));
}
```

- [ ] **Step 2: Commit (algorithm complete, rest of init follows in Task 5)**

```bash
git add template-deploy/tools-src/crossword-puzzle-generator.html
git commit -m "feat: add crossword grid layout algorithm (buildCrossword, canPlace, renumber)"
```

---

### Task 5: Add renderer + auto/custom generate JS (init slot, part 2)

**Files:**
- Modify: `template-deploy/tools-src/crossword-puzzle-generator.html` (append to existing `<script>` block — add before the closing `</script>`)

- [ ] **Step 1: Add renderer + generate functions (inside the existing `<script>` block, after `buildCrossword`)**

```javascript
/* ── Renderer ────────────────────────────────────────────────────── */

function esc(s) {
  return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}

function renderGrid(result) {
  var gridEl = document.getElementById('cw-grid');
  var cluesWrap = document.getElementById('cw-clues-wrap');
  var actionsEl = document.getElementById('cw-actions');

  if (!result || !result.placed.length) {
    gridEl.innerHTML = '<div class="cw-empty">Could not place any words. Try fewer words or check for repeated letters.</div>';
    cluesWrap.style.display = 'none';
    actionsEl.style.display = 'none';
    return;
  }

  // Build table
  var rows = [];
  for (var row = 0; row <= result.maxY; row++) {
    var cells = [];
    for (var col = 0; col <= result.maxX; col++) {
      var key = col + ',' + row;
      var letter = result.grid[key];
      if (letter) {
        var numSpan = result.cellNum[key] ? '<span class="cw-num">'+result.cellNum[key]+'</span>' : '';
        cells.push('<td class="cw-cell" data-key="'+key+'" data-letter="'+letter+'">'
          +numSpan+'<span class="cw-letter">'+letter+'</span></td>');
      } else {
        cells.push('<td class="cw-black"></td>');
      }
    }
    rows.push('<tr>'+cells.join('')+'</tr>');
  }
  gridEl.innerHTML = '<table class="cw-table">'+rows.join('')+'</table>';

  // Clue lists
  var across = result.placed.filter(function(p){return p.dir==='across';}).sort(function(a,b){return a.num-b.num;});
  var down   = result.placed.filter(function(p){return p.dir==='down';}).sort(function(a,b){return a.num-b.num;});
  document.getElementById('cw-across').innerHTML = across.map(function(p){
    return '<li><b>'+p.num+'.</b> '+esc(p.clue)+'</li>';
  }).join('');
  document.getElementById('cw-down').innerHTML = down.map(function(p){
    return '<li><b>'+p.num+'.</b> '+esc(p.clue)+'</li>';
  }).join('');

  cluesWrap.style.display = '';
  actionsEl.style.display = '';
  document.getElementById('cw-word-count').textContent = result.placed.length + ' words placed';
}

/* ── Auto-generate ───────────────────────────────────────────────── */

function autoGenerate() {
  if (!cwData) { fetchData(autoGenerate); return; }
  var difficulty = document.getElementById('cw-difficulty').value;
  var category   = document.getElementById('cw-category').value;
  var pool = [];
  if (category === 'all') {
    Object.keys(cwData[difficulty]).forEach(function(cat){ pool = pool.concat(cwData[difficulty][cat]); });
  } else {
    pool = (cwData[difficulty][category] || []).slice();
  }
  shuffle(pool);
  currentResult = buildCrossword(pool.slice(0, 20));
  renderGrid(currentResult);
  exitSolveMode(false);
}

function fetchData(cb) {
  var btn = document.getElementById('cw-generate-btn');
  btn.disabled = true; btn.textContent = 'Loading…';
  fetch(DATA_URL).then(function(r){ return r.json(); }).then(function(data){
    cwData = data;
    btn.disabled = false; btn.textContent = 'Generate Crossword';
    cb();
  }).catch(function(){
    btn.disabled = false; btn.textContent = 'Generate Crossword';
    showToast('Failed to load word data. Please try again.');
  });
}

function shuffle(arr) {
  for (var i = arr.length - 1; i > 0; i--) {
    var j = Math.floor(Math.random() * (i + 1));
    var t = arr[i]; arr[i] = arr[j]; arr[j] = t;
  }
}

/* ── Custom generate ─────────────────────────────────────────────── */

function customGenerate() {
  var val = document.getElementById('cw-custom-input').value.trim();
  var errEl = document.getElementById('cw-custom-error');
  errEl.style.display = 'none';
  if (!val) { showToast('Enter at least one word and clue.'); return; }

  var entries = [], errors = [];
  val.split('\n').forEach(function(line, i) {
    line = line.trim(); if (!line) return;
    var comma = line.indexOf(',');
    if (comma === -1) { errors.push('Line '+(i+1)+': missing comma between word and clue.'); return; }
    var word = line.slice(0, comma).trim().toUpperCase().replace(/[^A-Z]/g,'');
    var clue = line.slice(comma + 1).trim();
    if (word.length < 2) { errors.push('Line '+(i+1)+': word must be at least 2 letters.'); return; }
    if (!clue) { errors.push('Line '+(i+1)+': clue is empty.'); return; }
    entries.push({w: word, c: clue});
  });

  if (errors.length) { errEl.textContent = errors[0]; errEl.style.display = ''; return; }
  if (!entries.length) { showToast('No valid entries found.'); return; }

  currentResult = buildCrossword(entries);
  renderGrid(currentResult);
  exitSolveMode(false);
}
```

- [ ] **Step 2: Commit**

```bash
git add template-deploy/tools-src/crossword-puzzle-generator.html
git commit -m "feat: add crossword renderer, auto-generate, and custom-generate functions"
```

---

### Task 6: Add print, solve mode, share, toast, init JS (init slot, part 3)

**Files:**
- Modify: `template-deploy/tools-src/crossword-puzzle-generator.html` (continue in `<script>` block)

- [ ] **Step 1: Add remaining JS functions**

```javascript
/* ── Print ───────────────────────────────────────────────────────── */

function printBlank() {
  document.querySelectorAll('.cw-letter').forEach(function(el){ el.style.visibility='hidden'; });
  window.print();
  document.querySelectorAll('.cw-letter').forEach(function(el){ el.style.visibility=''; });
}

function printAnswers() { window.print(); }

/* ── Solve mode ──────────────────────────────────────────────────── */

function enterSolveMode() {
  if (!currentResult) return;
  solveMode = true;

  // Replace each cell's static letter span with an input
  document.querySelectorAll('.cw-cell').forEach(function(td) {
    var numEl = td.querySelector('.cw-num');
    var numHtml = numEl ? numEl.outerHTML : '';
    var letter = td.dataset.letter;
    td.innerHTML = numHtml + '<input class="cw-input" maxlength="1" data-letter="'+letter
      +'" autocomplete="off" autocorrect="off" autocapitalize="characters" spellcheck="false">';
  });

  // Keyboard navigation
  document.querySelectorAll('.cw-input').forEach(function(inp) {
    inp.addEventListener('keydown', function(e) {
      var td = inp.closest('td');
      var p = td.dataset.key.split(',');
      var col = parseInt(p[0]), row = parseInt(p[1]);
      if (e.key === 'ArrowRight') { e.preventDefault(); focusCell(col+1, row); }
      else if (e.key === 'ArrowLeft')  { e.preventDefault(); focusCell(col-1, row); }
      else if (e.key === 'ArrowDown')  { e.preventDefault(); focusCell(col, row+1); }
      else if (e.key === 'ArrowUp')    { e.preventDefault(); focusCell(col, row-1); }
      else if (e.key === 'Backspace' && !inp.value) {
        e.preventDefault(); focusCell(col-1, row) || focusCell(col, row-1);
      }
    });
    inp.addEventListener('input', function() {
      inp.value = inp.value.toUpperCase().replace(/[^A-Z]/g,'').slice(-1);
      if (inp.value) {
        var td = inp.closest('td');
        var p = td.dataset.key.split(',');
        var col = parseInt(p[0]), row = parseInt(p[1]);
        if (!focusCell(col+1, row)) focusCell(col, row+1);
      }
    });
  });

  // Toggle button visibility
  document.getElementById('cw-solve-btn').style.display = 'none';
  document.getElementById('cw-check-btn').style.display = '';
  document.getElementById('cw-reveal-btn').style.display = '';
  document.getElementById('cw-exit-solve-btn').style.display = '';
  document.getElementById('cw-print-blank-btn').disabled = true;
  document.getElementById('cw-print-ans-btn').disabled = true;
}

function focusCell(col, row) {
  var td = document.querySelector('td[data-key="'+col+','+row+'"]');
  if (!td) return false;
  var inp = td.querySelector('.cw-input');
  if (!inp) return false;
  inp.focus(); return true;
}

function checkAnswers() {
  var allCorrect = true;
  document.querySelectorAll('.cw-input').forEach(function(inp) {
    var td = inp.closest('td');
    td.classList.remove('cw-correct','cw-wrong');
    if (!inp.value) { allCorrect = false; return; }
    if (inp.value === inp.dataset.letter) { td.classList.add('cw-correct'); }
    else { td.classList.add('cw-wrong'); allCorrect = false; }
  });
  if (allCorrect) showToast('Puzzle complete!');
}

function revealAll() {
  document.querySelectorAll('.cw-input').forEach(function(inp) {
    inp.value = inp.dataset.letter;
    var td = inp.closest('td');
    td.classList.remove('cw-wrong'); td.classList.add('cw-correct');
  });
  showToast('Answers revealed.');
}

function exitSolveMode(rerender) {
  solveMode = false;
  if (rerender !== false && currentResult) renderGrid(currentResult);
  document.getElementById('cw-solve-btn').style.display = '';
  document.getElementById('cw-check-btn').style.display = 'none';
  document.getElementById('cw-reveal-btn').style.display = 'none';
  document.getElementById('cw-exit-solve-btn').style.display = 'none';
  document.getElementById('cw-print-blank-btn').disabled = false;
  document.getElementById('cw-print-ans-btn').disabled = false;
}

/* ── Share via URL hash ──────────────────────────────────────────── */

function sharePuzzle() {
  if (!currentResult) return;
  var compact = {p: currentResult.placed.map(function(p) {
    return [p.word, p.clue, p.x, p.y, p.dir==='across'?0:1, p.num];
  })};
  var encoded = btoa(unescape(encodeURIComponent(JSON.stringify(compact))));
  var url = location.origin + location.pathname + '#puzzle=' + encoded;
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(url).then(function(){ showToast('Link copied!'); }).catch(function(){ fallbackCopy(url); });
  } else { fallbackCopy(url); }
}

function fallbackCopy(url) {
  var ta = document.createElement('textarea');
  ta.value = url; ta.style.cssText = 'position:fixed;top:-9999px';
  document.body.appendChild(ta); ta.select();
  try { document.execCommand('copy'); showToast('Link copied!'); } catch(e) { showToast('Copy the URL from the address bar.'); }
  document.body.removeChild(ta);
}

function loadFromHash() {
  var m = location.hash.match(/[#&]puzzle=([^&]*)/);
  if (!m) return;
  try {
    var compact = JSON.parse(decodeURIComponent(escape(atob(m[1]))));
    var placed = compact.p.map(function(a){ return {word:a[0],clue:a[1],x:a[2],y:a[3],dir:a[4]===0?'across':'down',num:a[5]}; });
    var grid={}, cellNum={}, maxX=0, maxY=0;
    placed.forEach(function(p){
      cellNum[p.x+','+p.y]=p.num;
      var dx=p.dir==='across'?1:0, dy=p.dir==='down'?1:0;
      for(var i=0;i<p.word.length;i++){
        var key=(p.x+i*dx)+','+(p.y+i*dy);
        grid[key]=p.word[i];
        maxX=Math.max(maxX,p.x+i*dx); maxY=Math.max(maxY,p.y+i*dy);
      }
    });
    currentResult={placed:placed,grid:grid,cellNum:cellNum,maxX:maxX,maxY:maxY};
    renderGrid(currentResult);
    showToast('Puzzle loaded from link!');
  } catch(e) { /* invalid hash — ignore */ }
}

/* ── Toast ───────────────────────────────────────────────────────── */

function showToast(msg) {
  var t = document.getElementById('cw-toast');
  t.textContent = msg; t.classList.add('show');
  setTimeout(function(){ t.classList.remove('show'); }, 2200);
}

/* ── Tab switching ───────────────────────────────────────────────── */

function switchTab(tab) {
  var isAuto = tab === 'auto';
  document.getElementById('cw-auto-panel').style.display   = isAuto ? '' : 'none';
  document.getElementById('cw-custom-panel').style.display = isAuto ? 'none' : '';
  document.getElementById('cw-tab-auto').classList.toggle('active', isAuto);
  document.getElementById('cw-tab-custom').classList.toggle('active', !isAuto);
  currentTab = tab;
}

/* ── Bootstrap ───────────────────────────────────────────────────── */

document.addEventListener('DOMContentLoaded', function() {
  document.getElementById('cw-tab-auto').addEventListener('click', function(){ switchTab('auto'); });
  document.getElementById('cw-tab-custom').addEventListener('click', function(){ switchTab('custom'); });
  document.getElementById('cw-generate-btn').addEventListener('click', autoGenerate);
  document.getElementById('cw-generate-custom-btn').addEventListener('click', customGenerate);
  document.getElementById('cw-print-blank-btn').addEventListener('click', printBlank);
  document.getElementById('cw-print-ans-btn').addEventListener('click', printAnswers);
  document.getElementById('cw-solve-btn').addEventListener('click', enterSolveMode);
  document.getElementById('cw-check-btn').addEventListener('click', checkAnswers);
  document.getElementById('cw-reveal-btn').addEventListener('click', revealAll);
  document.getElementById('cw-exit-solve-btn').addEventListener('click', function(){ exitSolveMode(true); });
  document.getElementById('cw-share-btn').addEventListener('click', sharePuzzle);

  document.addEventListener('keydown', function(e) {
    if (document.activeElement !== document.body) return;
    if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); document.getElementById('cw-generate-btn').click(); }
  });

  loadFromHash();
});

}());
</script>
<!-- /SLOT:init -->
```

- [ ] **Step 2: Commit**

```bash
git add template-deploy/tools-src/crossword-puzzle-generator.html
git commit -m "feat: add solve mode, print, share URL, and DOMContentLoaded bootstrap"
```

---

### Task 7: Add explainer, FAQ, and who slots (copy)

**Files:**
- Modify: `template-deploy/tools-src/crossword-puzzle-generator.html` (append)

- [ ] **Step 1: Append explainer slot**

```html
<!-- SLOT:explainer -->
<div class="explainer">

<h2>What Is a Crossword Puzzle Generator?</h2>
<p>A crossword puzzle generator is a tool that arranges a set of words into an interlocking grid, where each word crosses at least one other through a shared letter. The result is a solvable puzzle: a blank grid with numbered clues that players use to fill in the correct words. Traditionally, making a crossword by hand takes hours — you'd need graph paper, careful planning, and a lot of erasing. A generator does all of that layout work instantly, leaving you free to focus on the vocabulary and clues that matter.</p>
<p>This tool is built for two different users: teachers and curriculum designers who want to build custom vocabulary puzzles with their own word lists, and casual players who want a fresh crossword on a specific topic without typing anything at all. Both modes produce the same output: a printable grid, a numbered clue list, and — if you want — a shareable link that anyone can open and solve in their browser.</p>

<h2>Why Use a Crossword Puzzle Generator?</h2>
<p>Crossword puzzles are one of the most effective vocabulary reinforcement tools available. Research in language acquisition consistently shows that encountering a word in a retrieval context — where you have to produce it from memory rather than simply recognize it — strengthens long-term retention far better than flashcard-style review. A crossword forces exactly that: given a definition, produce the word. Given the first letter, complete the spelling. The grid structure also makes spelling errors immediately visible, which gives students feedback they can act on.</p>
<p>Beyond the classroom, crosswords work for any group that learns together: family game nights, office trivia sessions, pub quizzes, escape room warm-ups. Making a custom crossword with your own topic used to require specialized software. Now it takes thirty seconds. Type your words and clues, click Generate, and you have a puzzle ready to print or share.</p>

<h2>How It Works</h2>
<p>The generator runs entirely in your browser — no data is sent to any server. When you click Generate, the layout algorithm sorts your words by length (longest first), places the longest word horizontally at the center of the grid, then scans each subsequent word for letters it shares with already-placed words. Every shared letter is a candidate intersection. The algorithm scores each candidate position by how many letters it connects and how compact the resulting grid is, then places the word at the best-scoring spot. Words that share no letters with the rest of the grid are skipped.</p>
<p>The auto-generate mode draws from a curated set of 400+ words organized by difficulty (Easy, Medium, Hard) and category (Animals, Science, Geography, Food, Sports, School, Nature, Technology). It picks up to 20 words, shuffles them, runs the same algorithm, and renders the result. Custom mode parses your textarea line by line — one <code>WORD, Clue text</code> pair per line — strips non-letter characters from the word, and feeds the entries into the same layout engine.</p>

<h2>Best Practices for Better Crosswords</h2>
<p><strong>Word length matters.</strong> Words between 4 and 10 letters work best. Very short words (2–3 letters) are hard to clue interestingly and rarely intersect cleanly. Very long words (12+ letters) can push the grid into an awkward shape. A mix of medium-length words — say, five 5-letter words, five 7-letter words, and a few 9-letter words — tends to produce a dense, satisfying grid.</p>
<p><strong>Write clues that match your audience.</strong> For younger students or beginners, use direct definitions: <code>OCEAN, The largest body of water on Earth</code>. For more advanced players, indirect clues work better: <code>OCEAN, Titanic's final resting place</code>. Avoid clues that are too similar to each other — if two clues both say "A type of tree," students will guess randomly rather than think.</p>
<p><strong>Aim for 10–20 words.</strong> Fewer than 8 words and the grid feels sparse; words won't intersect much. More than 25 words and some will inevitably fail to connect. The sweet spot is 12–18 words for a classroom-sized puzzle.</p>
<p><strong>Vary word length deliberately.</strong> If all your words are the same length, the algorithm has fewer intersection options, and words are more likely to get dropped. Include a few short words to create more shared-letter opportunities for longer ones.</p>

</div>
<!-- /SLOT:explainer -->
```

- [ ] **Step 2: Append FAQ slot**

```html
<!-- SLOT:faq -->
<div class="faq-wrap">
  <div class="faq-title">Frequently Asked Questions</div>

  <div class="faq-item open">
    <button class="faq-q" aria-expanded="true">
      <span class="faq-q-text">How many words can I add to a crossword?</span>
      <svg class="faq-chevron" viewBox="0 0 10 6" fill="none"><path d="M1 1l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
    </button>
    <div class="faq-a">
      <p>You can enter up to 30 words in custom mode. The algorithm tries to connect as many as possible through shared letters — in practice, 10 to 20 words is the sweet spot for a dense, well-connected grid. Words that share no letters with the rest of the puzzle are automatically skipped rather than placed as isolated islands.</p>
    </div>
  </div>

  <div class="faq-item">
    <button class="faq-q" aria-expanded="false">
      <span class="faq-q-text">What happens if some of my words don't fit?</span>
      <svg class="faq-chevron" viewBox="0 0 10 6" fill="none"><path d="M1 1l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
    </button>
    <div class="faq-a">
      <p>Words that can't be connected to the existing grid are silently skipped. The word count shown below the grid tells you exactly how many words were placed. If fewer words appear than you entered, try adding more words that share common letters — E, A, R, S, and T are the most intersection-friendly letters in English.</p>
    </div>
  </div>

  <div class="faq-item">
    <button class="faq-q" aria-expanded="false">
      <span class="faq-q-text">What's the difference between Easy, Medium, and Hard?</span>
      <svg class="faq-chevron" viewBox="0 0 10 6" fill="none"><path d="M1 1l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
    </button>
    <div class="faq-a">
      <p>The difficulty setting controls which curated word list is used in auto-generate mode. Easy words are short and common — 3 to 6 letters, everyday vocabulary. Medium words are 5 to 8 letters with slightly more specialized definitions. Hard words are 7 to 12 letters with technical, academic, or advanced vocabulary. The difficulty setting has no effect in custom mode — there, the words you enter determine the challenge level.</p>
    </div>
  </div>

  <div class="faq-item">
    <button class="faq-q" aria-expanded="false">
      <span class="faq-q-text">How do I share my puzzle with students or friends?</span>
      <svg class="faq-chevron" viewBox="0 0 10 6" fill="none"><path d="M1 1l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
    </button>
    <div class="faq-a">
      <p>Click <strong>Share Link</strong> after generating a puzzle. The tool encodes the entire puzzle — words, clues, and grid layout — into the URL itself. No account needed and nothing is stored on any server. Anyone who opens the link will see your exact puzzle and can solve it in their browser using the Solve in Browser mode.</p>
    </div>
  </div>

  <div class="faq-item">
    <button class="faq-q" aria-expanded="false">
      <span class="faq-q-text">Can I print a blank version without the answers showing?</span>
      <svg class="faq-chevron" viewBox="0 0 10 6" fill="none"><path d="M1 1l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
    </button>
    <div class="faq-a">
      <p>Yes. Click <strong>Print Blank</strong> to open the print dialog with all letters hidden — students see only the empty grid and numbered clue list, which is what they need to solve it on paper. Click <strong>Print Answers</strong> to print the filled-in solution grid, which you can keep as a teacher's answer key.</p>
    </div>
  </div>

  <div class="faq-item">
    <button class="faq-q" aria-expanded="false">
      <span class="faq-q-text">Does my puzzle get saved anywhere?</span>
      <svg class="faq-chevron" viewBox="0 0 10 6" fill="none"><path d="M1 1l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
    </button>
    <div class="faq-a">
      <p>No. The generator runs entirely in your browser. Nothing is transmitted to any server, and no puzzle data is stored in a database. The only persistence available is the Share Link, which encodes the puzzle into the URL — the puzzle lives in the link, not on our servers. If you close the tab without sharing or printing, the puzzle is gone.</p>
    </div>
  </div>

  <div class="faq-item">
    <button class="faq-q" aria-expanded="false">
      <span class="faq-q-text">Can I use proper nouns or multi-word phrases?</span>
      <svg class="faq-chevron" viewBox="0 0 10 6" fill="none"><path d="M1 1l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
    </button>
    <div class="faq-a">
      <p>Proper nouns work fine — <code>PARIS, Capital of France</code> is a valid entry. Multi-word phrases are not supported in the grid itself, since each grid word must be a single unbroken string of letters. If you want to include a phrase like "WHITE HOUSE," you'll need to enter it as <code>WHITEHOUSE</code> or pick one of the words, like <code>OVAL, The shape of the President's office</code>. Non-letter characters in the word field (spaces, hyphens) are automatically stripped.</p>
    </div>
  </div>

  <div class="faq-item">
    <button class="faq-q" aria-expanded="false">
      <span class="faq-q-text">What's the ideal grid size for a classroom puzzle?</span>
      <svg class="faq-chevron" viewBox="0 0 10 6" fill="none"><path d="M1 1l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
    </button>
    <div class="faq-a">
      <p>The grid resizes automatically based on the words you provide — there's no manual size control. For a 20-to-30-minute classroom activity, 12 to 15 words typically produces a grid that fills a single sheet of paper when printed, has enough white space to write comfortably, and takes students the right amount of time to complete. Fewer words make a quicker warm-up; more words make a longer independent activity.</p>
    </div>
  </div>

</div>
<!-- /SLOT:faq -->
```

- [ ] **Step 3: Append who slot**

```html
<!-- SLOT:who -->
<div class="uc-grid">
  <div class="uc">
    <div class="uc-title">Teachers</div>
    <div class="uc-body">Build vocabulary review puzzles, test-prep activities, and end-of-unit assessments using your exact word list. Print blank copies for the class and keep the answer version for yourself.</div>
  </div>
  <div class="uc">
    <div class="uc-title">Students</div>
    <div class="uc-body">Challenge yourself with a custom topic crossword or make one for a friend. Share the link so they can solve it in their browser without printing anything.</div>
  </div>
  <div class="uc">
    <div class="uc-title">Parents &amp; Homeschoolers</div>
    <div class="uc-body">Supplement any lesson with a printable crossword in seconds. Pick a topic from the curated library or type in your own words to match exactly what you're teaching this week.</div>
  </div>
  <div class="uc">
    <div class="uc-title">Game Night Hosts</div>
    <div class="uc-body">Create a custom crossword around a shared interest — a TV show, a decade, a city — and share the link before the event so everyone can compete. No printing required.</div>
  </div>
</div>
<!-- /SLOT:who -->
```

- [ ] **Step 4: Commit**

```bash
git add template-deploy/tools-src/crossword-puzzle-generator.html
git commit -m "feat: add explainer, FAQ, and who-uses copy to crossword tool"
```

---

### Task 8: Integration — word-tools, tools.json, _redirects, sitemap

**Files:**
- Modify: `template-deploy/tools-src/word-tools.html`
- Modify: `template-deploy/tools.json`
- Modify: `wordineer-deploy/_redirects`
- Modify: `wordineer-deploy/sitemap.xml`

- [ ] **Step 1: Activate placeholder in word-tools.html**

In `template-deploy/tools-src/word-tools.html`, find lines 360–364:

```html
        <div class="tool-item tool-item--soon">
          <div class="tool-icon" style="background:#EAF0F6"><svg viewBox="0 0 13 13" fill="none"><rect x="2" y="2" width="3" height="3" rx=".35" stroke="#2F4F6F" stroke-width=".85"/><rect x="5" y="5" width="3" height="3" rx=".35" stroke="#2F4F6F" stroke-width=".85"/><rect x="8" y="2" width="3" height="3" rx=".35" stroke="#2F4F6F" stroke-width=".85"/><rect x="2" y="8" width="3" height="3" rx=".35" stroke="#2F4F6F" stroke-width=".85"/><rect x="8" y="8" width="3" height="3" rx=".35" stroke="#2F4F6F" stroke-width=".85"/><path d="M5 3.5h3M3.5 5v3M9.5 5v3M5 9.5h3" stroke="#2F4F6F" stroke-width=".75" stroke-linecap="round"/></svg></div>
          <div class="tool-name">Crossword Puzzle Generator <span class="soon-badge">Coming soon</span></div>
          <div class="tool-desc">Crossword-style prompts and puzzle ideas for solo play or classrooms.</div>
        </div>
```

Replace with:

```html
        <a href="/crossword-puzzle-generator/" class="tool-item">
          <div class="tool-icon" style="background:#EAF0F6"><svg viewBox="0 0 13 13" fill="none"><rect x="2" y="2" width="3" height="3" rx=".35" stroke="#2F4F6F" stroke-width=".85"/><rect x="5" y="5" width="3" height="3" rx=".35" stroke="#2F4F6F" stroke-width=".85"/><rect x="8" y="2" width="3" height="3" rx=".35" stroke="#2F4F6F" stroke-width=".85"/><rect x="2" y="8" width="3" height="3" rx=".35" stroke="#2F4F6F" stroke-width=".85"/><rect x="8" y="8" width="3" height="3" rx=".35" stroke="#2F4F6F" stroke-width=".85"/><path d="M5 3.5h3M3.5 5v3M9.5 5v3M5 9.5h3" stroke="#2F4F6F" stroke-width=".75" stroke-linecap="round"/></svg></div>
          <div class="tool-name">Crossword Puzzle Generator</div>
          <div class="tool-desc">Make a printable crossword with your own words and clues, or auto-generate by topic.</div>
        </a>
```

- [ ] **Step 2: Add to tools.json mega menu**

In `template-deploy/tools.json`, find the `"Games & fun"` mega category (around line 129). Add the crossword entry to its `tools` array:

```json
        {
          "href": "/crossword-puzzle-generator/",
          "text": "Crossword Puzzle Generator"
        },
```

Add it after the existing `"/pictionary-phrase-generator/"` entry.

- [ ] **Step 3: Add to tools.json more_word_tools**

Find the `more_word_tools` array entry for charades (around line 379). Add after it:

```json
    {
      "href": "/crossword-puzzle-generator/",
      "name": "Crossword Puzzle Generator",
      "desc": "Make a printable crossword with your words and clues, or auto-generate by topic and difficulty",
      "icon_bg": "#EAF0F6",
      "icon_path": "<rect x=\"2\" y=\"2\" width=\"3\" height=\"3\" rx=\".35\" stroke=\"#2F4F6F\" stroke-width=\".85\"/><rect x=\"5\" y=\"5\" width=\"3\" height=\"3\" rx=\".35\" stroke=\"#2F4F6F\" stroke-width=\".85\"/><rect x=\"8\" y=\"2\" width=\"3\" height=\"3\" rx=\".35\" stroke=\"#2F4F6F\" stroke-width=\".85\"/><rect x=\"2\" y=\"8\" width=\"3\" height=\"3\" rx=\".35\" stroke=\"#2F4F6F\" stroke-width=\".85\"/><rect x=\"8\" y=\"8\" width=\"3\" height=\"3\" rx=\".35\" stroke=\"#2F4F6F\" stroke-width=\".85\"/><path d=\"M5 3.5h3M3.5 5v3M9.5 5v3M5 9.5h3\" stroke=\"#2F4F6F\" stroke-width=\".75\" stroke-linecap=\"round\"/>"
    },
```

- [ ] **Step 4: Add to tools.json footer_cols**

Find the footer_cols section. Add to the word tools column alongside charades/pictionary:

```json
      {"href": "/crossword-puzzle-generator/", "text": "Crossword Puzzle Generator"},
```

- [ ] **Step 5: Add _redirects rules**

Append to `wordineer-deploy/_redirects`:

```
/crossword-puzzle-generator.html    /crossword-puzzle-generator/    301
/crossword-puzzle-generator/        /crossword-puzzle-generator.html    200
```

- [ ] **Step 6: Add sitemap entry**

In `wordineer-deploy/sitemap.xml`, find the closing `</urlset>` tag and insert before it:

```xml
  <url>
    <loc>https://wordineer.com/crossword-puzzle-generator/</loc>
    <lastmod>2026-06-13</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.9</priority>
  </url>
```

- [ ] **Step 7: Commit all integration changes**

```bash
git add template-deploy/tools-src/word-tools.html template-deploy/tools.json wordineer-deploy/_redirects wordineer-deploy/sitemap.xml
git commit -m "feat: integrate crossword into word-tools, mega menu, footer, _redirects, sitemap"
```

---

### Task 9: Build, copy output, and verify locally

**Files:**
- Build output: `wordineer-deploy/crossword-puzzle-generator.html`
- Build output: `wordineer-deploy/word-tools.html`

- [ ] **Step 1: Run build**

```bash
cd template-deploy && python3 build.py
```

Expected: no errors, output mentions `crossword-puzzle-generator.html` and `word-tools.html` generated.

- [ ] **Step 2: Copy output files**

```bash
cp template-deploy/output/crossword-puzzle-generator.html wordineer-deploy/crossword-puzzle-generator.html
cp template-deploy/output/word-tools.html wordineer-deploy/word-tools.html
```

- [ ] **Step 3: Start local server**

```bash
cd wordineer-deploy && python3 -m http.server 8080
```

Open `http://localhost:8080/crossword-puzzle-generator.html` in browser.

- [ ] **Step 4: Verify auto-generate mode**

1. Select Medium / Animals, click Generate Crossword
2. Grid renders with black and white cells
3. Clue numbers in grid match numbered Across/Down lists
4. Word count shows a number ≥ 5
5. Action buttons appear: Print Blank, Print Answers, Solve in Browser, Share Link

- [ ] **Step 5: Verify custom mode**

1. Click Custom Puzzle tab
2. Paste this into the textarea:
   ```
   OCEAN, The largest body of water
   TIDE, The rise and fall of the sea
   WAVE, A moving ridge of water
   CORAL, A reef-building organism
   SHARK, An apex ocean predator
   FISH, A cold-blooded aquatic animal
   REEF, An underwater ridge of rock or coral
   SALT, A mineral found in seawater
   ```
3. Click Generate Crossword — grid should render with 5–8 words placed

- [ ] **Step 6: Verify solve mode**

1. After generating any puzzle, click Solve in Browser
2. Grid cells become text inputs
3. Click a cell and type a letter — it should appear uppercase
4. Press arrow keys — focus moves to adjacent cells
5. Click Check Answers — empty cells stay neutral, correct cells go green, wrong cells go red
6. Click Reveal All — all cells fill with correct letters and go green

- [ ] **Step 7: Verify share and hash restore**

1. Generate a puzzle, click Share Link — toast says "Link copied!"
2. Open a new browser tab, paste the copied URL, press Enter
3. Puzzle restores automatically — same words, same grid layout

- [ ] **Step 8: Verify print blank**

1. Generate a puzzle
2. Click Print Blank — browser print dialog opens, grid shows empty cells with clue numbers

- [ ] **Step 9: Verify word-tools integration**

Open `http://localhost:8080/word-tools.html` — Crossword Puzzle Generator appears as an active link (not grayed out, no "Coming soon" badge). Clicking it navigates to the crossword page.

- [ ] **Step 10: Verify breadcrumb**

On the crossword page, breadcrumb shows: `Wordineer › Word Tools › Crossword Puzzle Generator`. First two items are clickable links.

- [ ] **Step 11: Commit final output**

```bash
git add wordineer-deploy/crossword-puzzle-generator.html wordineer-deploy/word-tools.html
git commit -m "feat: add built crossword puzzle generator to deploy folder"
```

---

## Verification Checklist (post-deploy)

- [ ] Auto-generate: grid renders for all 3 difficulties × 8 categories + "All"
- [ ] Custom mode: 8-word custom puzzle places ≥ 5 words
- [ ] Clue numbers in grid match across/down lists
- [ ] Print Blank: letters hidden in print preview
- [ ] Print Answers: letters visible in print preview
- [ ] Solve mode: inputs editable, arrow keys work, check/reveal work
- [ ] Share: URL hash round-trips correctly (generate → share → paste → restore)
- [ ] Breadcrumb: 3-level, both ancestor links active
- [ ] word-tools page: link active, no "Coming soon" badge
- [ ] `/crossword-puzzle-generator/` clean URL resolves via _redirects
- [ ] sitemap.xml: entry present at priority 0.9
- [ ] PageSpeed: no autofocus on load, data fetch deferred to first Generate click

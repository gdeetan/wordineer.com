# Random Italian Name Generator — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a fully-featured `/random-italian-name-generator/` tool page with dedicated JSON data, filters for gender/style/region/letter, copy/save per name, and all standard Wordineer page sections.

**Architecture:** Dedicated `italian-names.json` with compact `{n,g,s,r,d}` schema. Tool-src HTML follows the Scottish name generator pattern with prefix `ing_`. Build system assembles final page via `build.py`.

**Tech Stack:** Vanilla JS, static HTML/CSS, Cloudflare Pages, Python build script, Node.js tests.

---

## File map

| Action | Path |
|---|---|
| Create | `wordineer-deploy/data/italian-names.json` |
| Create | `template-deploy/tools-src/random-italian-name-generator.html` |
| Modify | `template-deploy/tools.json` |
| Modify | `wordineer-deploy/_redirects` |
| Modify | `wordineer-deploy/sitemap.xml` |
| Create | `tests/italian-names-data.test.js` |
| Create | `tests/italian-generator-page.test.js` |
| Create (generated) | `wordineer-deploy/random-italian-name-generator.html` |

---

## Task 1: Create italian-names.json

**Files:**
- Create: `wordineer-deploy/data/italian-names.json`

Schema per given name: `{ "n": string, "g": "m"|"f"|"u", "s": "classic"|"modern"|"religious"|"regional", "r": "north"|"central"|"south"|"sicily"|"any", "d": string }`

Schema per surname: `{ "n": string, "s": "classic"|"modern"|"religious"|"regional", "r": "north"|"central"|"south"|"sicily"|"any", "d": string }` (surnames have no `g` field)

- [ ] **Step 1: Create the data file**

Create `wordineer-deploy/data/italian-names.json` with the following content:

```json
{
  "given": [
    { "n": "Marco", "g": "m", "s": "classic", "r": "any", "d": "warlike; defender" },
    { "n": "Giovanni", "g": "m", "s": "classic", "r": "any", "d": "God is gracious" },
    { "n": "Luigi", "g": "m", "s": "classic", "r": "any", "d": "famous warrior" },
    { "n": "Antonio", "g": "m", "s": "classic", "r": "any", "d": "priceless; praiseworthy" },
    { "n": "Francesco", "g": "m", "s": "classic", "r": "any", "d": "free one; from France" },
    { "n": "Carlo", "g": "m", "s": "classic", "r": "any", "d": "free man; strong" },
    { "n": "Alberto", "g": "m", "s": "classic", "r": "any", "d": "noble and bright" },
    { "n": "Alessandro", "g": "m", "s": "classic", "r": "any", "d": "defender of men" },
    { "n": "Andrea", "g": "m", "s": "classic", "r": "any", "d": "manly; brave" },
    { "n": "Angelo", "g": "m", "s": "classic", "r": "any", "d": "messenger; angel" },
    { "n": "Bruno", "g": "m", "s": "classic", "r": "any", "d": "brown; dark one" },
    { "n": "Claudio", "g": "m", "s": "classic", "r": "any", "d": "lame; from the Roman Claudius clan" },
    { "n": "Daniele", "g": "m", "s": "classic", "r": "any", "d": "God is my judge" },
    { "n": "Domenico", "g": "m", "s": "classic", "r": "any", "d": "belonging to the Lord" },
    { "n": "Edoardo", "g": "m", "s": "classic", "r": "any", "d": "wealthy guardian" },
    { "n": "Emilio", "g": "m", "s": "classic", "r": "any", "d": "rival; eager" },
    { "n": "Enrico", "g": "m", "s": "classic", "r": "any", "d": "ruler of the home" },
    { "n": "Fabio", "g": "m", "s": "classic", "r": "any", "d": "bean grower; from the Fabian clan" },
    { "n": "Federico", "g": "m", "s": "classic", "r": "any", "d": "peaceful ruler" },
    { "n": "Filippo", "g": "m", "s": "classic", "r": "any", "d": "lover of horses" },
    { "n": "Flavio", "g": "m", "s": "classic", "r": "any", "d": "golden-haired; blond" },
    { "n": "Giorgio", "g": "m", "s": "classic", "r": "any", "d": "farmer; earthworker" },
    { "n": "Giacomo", "g": "m", "s": "classic", "r": "any", "d": "supplanter; held by the heel" },
    { "n": "Gianluca", "g": "m", "s": "classic", "r": "any", "d": "God is gracious; light" },
    { "n": "Gino", "g": "m", "s": "classic", "r": "any", "d": "short form of names ending in -gino" },
    { "n": "Guido", "g": "m", "s": "classic", "r": "any", "d": "guide; forest" },
    { "n": "Leo", "g": "m", "s": "classic", "r": "any", "d": "lion" },
    { "n": "Luciano", "g": "m", "s": "classic", "r": "any", "d": "light; illuminated" },
    { "n": "Mauro", "g": "m", "s": "classic", "r": "any", "d": "dark; Moorish" },
    { "n": "Mario", "g": "m", "s": "classic", "r": "any", "d": "of Mars; warlike" },
    { "n": "Massimo", "g": "m", "s": "classic", "r": "any", "d": "greatest" },
    { "n": "Michele", "g": "m", "s": "classic", "r": "any", "d": "who is like God?" },
    { "n": "Ottavio", "g": "m", "s": "classic", "r": "any", "d": "eighth" },
    { "n": "Paolo", "g": "m", "s": "classic", "r": "any", "d": "small; humble" },
    { "n": "Piero", "g": "m", "s": "classic", "r": "any", "d": "rock; stone" },
    { "n": "Pietro", "g": "m", "s": "classic", "r": "any", "d": "rock; stone" },
    { "n": "Raffaele", "g": "m", "s": "classic", "r": "any", "d": "God has healed" },
    { "n": "Riccardo", "g": "m", "s": "classic", "r": "any", "d": "powerful ruler" },
    { "n": "Roberto", "g": "m", "s": "classic", "r": "any", "d": "bright fame" },
    { "n": "Romeo", "g": "m", "s": "classic", "r": "any", "d": "pilgrim to Rome" },
    { "n": "Sergio", "g": "m", "s": "classic", "r": "any", "d": "from the Roman Sergius clan" },
    { "n": "Silvio", "g": "m", "s": "classic", "r": "north", "d": "of the forest; woodland" },
    { "n": "Stefano", "g": "m", "s": "classic", "r": "any", "d": "crown; wreath" },
    { "n": "Tommaso", "g": "m", "s": "classic", "r": "any", "d": "twin" },
    { "n": "Ugo", "g": "m", "s": "classic", "r": "north", "d": "mind; spirit" },
    { "n": "Umberto", "g": "m", "s": "classic", "r": "any", "d": "bright warrior; bear cub" },
    { "n": "Vincenzo", "g": "m", "s": "classic", "r": "any", "d": "conquering; victorious" },
    { "n": "Vittorio", "g": "m", "s": "classic", "r": "any", "d": "victorious" },
    { "n": "Cesare", "g": "m", "s": "classic", "r": "central", "d": "hairy; Roman imperial title" },
    { "n": "Dante", "g": "m", "s": "classic", "r": "central", "d": "enduring; steadfast" },
    { "n": "Aldo", "g": "m", "s": "classic", "r": "north", "d": "old; noble" },
    { "n": "Renzo", "g": "m", "s": "classic", "r": "north", "d": "short form of Lorenzo; laurel" },
    { "n": "Franco", "g": "m", "s": "classic", "r": "any", "d": "free; Frankish" },
    { "n": "Dario", "g": "m", "s": "classic", "r": "any", "d": "he who holds firm the good" },
    { "n": "Renato", "g": "m", "s": "classic", "r": "any", "d": "reborn; new life" },
    { "n": "Giulio", "g": "m", "s": "classic", "r": "central", "d": "youthful; from the Julian clan" },
    { "n": "Aurelio", "g": "m", "s": "classic", "r": "any", "d": "golden" },
    { "n": "Maurizio", "g": "m", "s": "classic", "r": "any", "d": "dark; Moorish" },
    { "n": "Corrado", "g": "m", "s": "classic", "r": "north", "d": "bold counsel" },
    { "n": "Ernesto", "g": "m", "s": "classic", "r": "any", "d": "serious; earnest" },
    { "n": "Ettore", "g": "m", "s": "classic", "r": "any", "d": "holding fast; defender" },
    { "n": "Marcello", "g": "m", "s": "classic", "r": "any", "d": "little warrior; of Mars" },
    { "n": "Ruggero", "g": "m", "s": "classic", "r": "north", "d": "famous spear; renowned" },
    { "n": "Valerio", "g": "m", "s": "classic", "r": "central", "d": "strong; healthy" },
    { "n": "Vito", "g": "m", "s": "classic", "r": "south", "d": "life; lively" },
    { "n": "Luca", "g": "m", "s": "modern", "r": "any", "d": "bringer of light" },
    { "n": "Matteo", "g": "m", "s": "modern", "r": "any", "d": "gift of God" },
    { "n": "Lorenzo", "g": "m", "s": "modern", "r": "any", "d": "from Laurentum; laurel" },
    { "n": "Davide", "g": "m", "s": "modern", "r": "any", "d": "beloved" },
    { "n": "Mattia", "g": "m", "s": "modern", "r": "any", "d": "gift of God" },
    { "n": "Samuele", "g": "m", "s": "modern", "r": "any", "d": "heard by God" },
    { "n": "Simone", "g": "m", "s": "modern", "r": "any", "d": "he has heard" },
    { "n": "Alessio", "g": "m", "s": "modern", "r": "any", "d": "defender" },
    { "n": "Gabriele", "g": "m", "s": "modern", "r": "any", "d": "God is my strength" },
    { "n": "Leonardo", "g": "m", "s": "modern", "r": "any", "d": "bold lion" },
    { "n": "Niccolò", "g": "m", "s": "modern", "r": "north", "d": "victory of the people" },
    { "n": "Diego", "g": "m", "s": "modern", "r": "any", "d": "supplanter; teaching" },
    { "n": "Emanuele", "g": "m", "s": "modern", "r": "any", "d": "God is with us" },
    { "n": "Riccardo", "g": "m", "s": "modern", "r": "any", "d": "powerful ruler" },
    { "n": "Giuseppe", "g": "m", "s": "religious", "r": "any", "d": "God will add; Italian form of Joseph" },
    { "n": "Benedetto", "g": "m", "s": "religious", "r": "any", "d": "blessed" },
    { "n": "Bartolomeo", "g": "m", "s": "religious", "r": "any", "d": "son of Talmai; son of the furrows" },
    { "n": "Celestino", "g": "m", "s": "religious", "r": "any", "d": "heavenly" },
    { "n": "Costantino", "g": "m", "s": "religious", "r": "any", "d": "steadfast; constant" },
    { "n": "Damiano", "g": "m", "s": "religious", "r": "south", "d": "to tame; patron saint of physicians" },
    { "n": "Donato", "g": "m", "s": "religious", "r": "central", "d": "given by God" },
    { "n": "Ignazio", "g": "m", "s": "religious", "r": "any", "d": "fire; ardent" },
    { "n": "Innocenzo", "g": "m", "s": "religious", "r": "any", "d": "innocent" },
    { "n": "Isidoro", "g": "m", "s": "religious", "r": "south", "d": "gift of Isis; gifted" },
    { "n": "Martino", "g": "m", "s": "religious", "r": "any", "d": "of Mars; warlike" },
    { "n": "Natale", "g": "m", "s": "religious", "r": "south", "d": "born at Christmas; nativity" },
    { "n": "Onofrio", "g": "m", "s": "religious", "r": "south", "d": "devoted to the good; Egyptian saint" },
    { "n": "Pacifico", "g": "m", "s": "religious", "r": "any", "d": "peaceful" },
    { "n": "Pasquale", "g": "m", "s": "religious", "r": "south", "d": "of Easter; paschal" },
    { "n": "Rocco", "g": "m", "s": "religious", "r": "south", "d": "rest; patron of the sick" },
    { "n": "Sebastiano", "g": "m", "s": "religious", "r": "south", "d": "venerable; from Sebaste" },
    { "n": "Agostino", "g": "m", "s": "religious", "r": "central", "d": "great; venerated" },
    { "n": "Ambrogio", "g": "m", "s": "religious", "r": "north", "d": "immortal; divine" },
    { "n": "Cristoforo", "g": "m", "s": "religious", "r": "any", "d": "bearer of Christ" },
    { "n": "Floriano", "g": "m", "s": "religious", "r": "central", "d": "flourishing; in bloom" },
    { "n": "Girolamo", "g": "m", "s": "religious", "r": "any", "d": "sacred name; holy name" },
    { "n": "Gregorio", "g": "m", "s": "religious", "r": "any", "d": "watchful; alert" },
    { "n": "Lazzaro", "g": "m", "s": "religious", "r": "south", "d": "God has helped" },
    { "n": "Nazzareno", "g": "m", "s": "religious", "r": "central", "d": "from Nazareth; the Nazarene" },
    { "n": "Pancrazio", "g": "m", "s": "religious", "r": "south", "d": "all-powerful" },
    { "n": "Gennaro", "g": "m", "s": "regional", "r": "south", "d": "patron saint of Naples; January" },
    { "n": "Ciro", "g": "m", "s": "regional", "r": "south", "d": "sun; throne; Persian royal name" },
    { "n": "Carmine", "g": "m", "s": "regional", "r": "south", "d": "garden; song; from Carmel" },
    { "n": "Salvatore", "g": "m", "s": "regional", "r": "south", "d": "savior; redeemer" },
    { "n": "Alfonso", "g": "m", "s": "regional", "r": "south", "d": "noble and ready; eager for battle" },
    { "n": "Gaetano", "g": "m", "s": "regional", "r": "south", "d": "from Gaeta; the ancient city" },
    { "n": "Calogero", "g": "m", "s": "regional", "r": "sicily", "d": "beautiful elder; good old age" },
    { "n": "Antonino", "g": "m", "s": "regional", "r": "sicily", "d": "priceless; Sicilian form of Antonio" },
    { "n": "Carmelo", "g": "m", "s": "regional", "r": "sicily", "d": "garden; vineyard of God" },
    { "n": "Nino", "g": "m", "s": "regional", "r": "south", "d": "short form of Giovanni and other names" },
    { "n": "Beppe", "g": "m", "s": "regional", "r": "any", "d": "familiar form of Giuseppe" },
    { "n": "Pino", "g": "m", "s": "regional", "r": "any", "d": "familiar form of Giuseppe or Filippo" },
    { "n": "Sandro", "g": "m", "s": "regional", "r": "central", "d": "short form of Alessandro" },
    { "n": "Nando", "g": "m", "s": "regional", "r": "any", "d": "short form of Ferdinando" },
    { "n": "Checco", "g": "m", "s": "regional", "r": "central", "d": "Tuscan familiar form of Francesco" },
    { "n": "Gigi", "g": "m", "s": "regional", "r": "any", "d": "familiar form of Luigi" },
    { "n": "Turi", "g": "m", "s": "regional", "r": "sicily", "d": "Sicilian familiar form of Salvatore" },
    { "n": "Rino", "g": "m", "s": "regional", "r": "north", "d": "short form of names ending in -rino" },
    { "n": "Maria", "g": "f", "s": "classic", "r": "any", "d": "beloved; sea of bitterness; wished-for child" },
    { "n": "Anna", "g": "f", "s": "classic", "r": "any", "d": "grace; favor" },
    { "n": "Rosa", "g": "f", "s": "classic", "r": "any", "d": "rose; beautiful flower" },
    { "n": "Elena", "g": "f", "s": "classic", "r": "any", "d": "bright; shining light" },
    { "n": "Laura", "g": "f", "s": "classic", "r": "any", "d": "laurel; honor" },
    { "n": "Chiara", "g": "f", "s": "classic", "r": "any", "d": "clear; bright; famous" },
    { "n": "Sara", "g": "f", "s": "classic", "r": "any", "d": "princess; noblewoman" },
    { "n": "Paola", "g": "f", "s": "classic", "r": "any", "d": "small; humble" },
    { "n": "Luisa", "g": "f", "s": "classic", "r": "any", "d": "famous warrior; renowned in battle" },
    { "n": "Francesca", "g": "f", "s": "classic", "r": "any", "d": "free one; from France" },
    { "n": "Giovanna", "g": "f", "s": "classic", "r": "any", "d": "God is gracious" },
    { "n": "Isabella", "g": "f", "s": "classic", "r": "any", "d": "pledged to God; devoted" },
    { "n": "Lucia", "g": "f", "s": "classic", "r": "any", "d": "light; illumination" },
    { "n": "Beatrice", "g": "f", "s": "classic", "r": "central", "d": "she who brings happiness; blessed" },
    { "n": "Carla", "g": "f", "s": "classic", "r": "any", "d": "free woman; strong" },
    { "n": "Daniela", "g": "f", "s": "classic", "r": "any", "d": "God is my judge" },
    { "n": "Donatella", "g": "f", "s": "classic", "r": "central", "d": "little gift; given by God" },
    { "n": "Elisa", "g": "f", "s": "classic", "r": "any", "d": "pledged to God; my God is an oath" },
    { "n": "Emma", "g": "f", "s": "classic", "r": "any", "d": "whole; universal" },
    { "n": "Federica", "g": "f", "s": "classic", "r": "any", "d": "peaceful ruler" },
    { "n": "Gabriella", "g": "f", "s": "classic", "r": "any", "d": "God is my strength" },
    { "n": "Gemma", "g": "f", "s": "classic", "r": "central", "d": "precious stone; gem" },
    { "n": "Ginevra", "g": "f", "s": "classic", "r": "north", "d": "fair one; white wave" },
    { "n": "Gloria", "g": "f", "s": "classic", "r": "any", "d": "glory; splendor" },
    { "n": "Grazia", "g": "f", "s": "classic", "r": "any", "d": "grace; blessing" },
    { "n": "Ilaria", "g": "f", "s": "classic", "r": "any", "d": "cheerful; joyful" },
    { "n": "Irene", "g": "f", "s": "classic", "r": "any", "d": "peace" },
    { "n": "Letizia", "g": "f", "s": "classic", "r": "any", "d": "joy; gladness" },
    { "n": "Livia", "g": "f", "s": "classic", "r": "central", "d": "blue; envious; from the Livius clan" },
    { "n": "Lorenza", "g": "f", "s": "classic", "r": "any", "d": "from Laurentum; laurel" },
    { "n": "Maddalena", "g": "f", "s": "classic", "r": "any", "d": "from Magdala; tower" },
    { "n": "Mara", "g": "f", "s": "classic", "r": "any", "d": "bitter; strength" },
    { "n": "Margherita", "g": "f", "s": "classic", "r": "any", "d": "pearl; daisy" },
    { "n": "Marta", "g": "f", "s": "classic", "r": "any", "d": "lady; mistress" },
    { "n": "Monica", "g": "f", "s": "classic", "r": "any", "d": "advisor; alone" },
    { "n": "Nicoletta", "g": "f", "s": "classic", "r": "any", "d": "victory of the people" },
    { "n": "Olimpia", "g": "f", "s": "classic", "r": "any", "d": "of Olympus; heavenly" },
    { "n": "Ornella", "g": "f", "s": "classic", "r": "any", "d": "flowering ash tree" },
    { "n": "Patrizia", "g": "f", "s": "classic", "r": "any", "d": "noble; patrician" },
    { "n": "Roberta", "g": "f", "s": "classic", "r": "any", "d": "bright fame" },
    { "n": "Rossana", "g": "f", "s": "classic", "r": "any", "d": "red-haired; dawn" },
    { "n": "Sabrina", "g": "f", "s": "classic", "r": "any", "d": "from the river Severn; legendary princess" },
    { "n": "Silvia", "g": "f", "s": "classic", "r": "any", "d": "of the forest; woodland spirit" },
    { "n": "Simona", "g": "f", "s": "classic", "r": "any", "d": "she who has heard" },
    { "n": "Stella", "g": "f", "s": "classic", "r": "any", "d": "star" },
    { "n": "Valentina", "g": "f", "s": "classic", "r": "any", "d": "strong; healthy; brave" },
    { "n": "Veronica", "g": "f", "s": "classic", "r": "any", "d": "true image; she who brings victory" },
    { "n": "Viviana", "g": "f", "s": "classic", "r": "any", "d": "lively; full of life" },
    { "n": "Angela", "g": "f", "s": "classic", "r": "any", "d": "angel; messenger" },
    { "n": "Alessandra", "g": "f", "s": "classic", "r": "any", "d": "defender of men" },
    { "n": "Barbara", "g": "f", "s": "classic", "r": "any", "d": "foreign woman; stranger" },
    { "n": "Caterina", "g": "f", "s": "classic", "r": "any", "d": "pure; unsullied" },
    { "n": "Cristina", "g": "f", "s": "classic", "r": "any", "d": "follower of Christ; anointed" },
    { "n": "Diana", "g": "f", "s": "classic", "r": "central", "d": "divine; Roman goddess of the hunt" },
    { "n": "Eleonora", "g": "f", "s": "classic", "r": "any", "d": "bright; shining light" },
    { "n": "Giuliana", "g": "f", "s": "classic", "r": "any", "d": "youthful; from the Julian clan" },
    { "n": "Marina", "g": "f", "s": "classic", "r": "any", "d": "of the sea; sea-born" },
    { "n": "Teresa", "g": "f", "s": "classic", "r": "any", "d": "harvester; summer" },
    { "n": "Claudia", "g": "f", "s": "classic", "r": "any", "d": "lame; from the Roman Claudius clan" },
    { "n": "Franca", "g": "f", "s": "classic", "r": "north", "d": "free; Frankish" },
    { "n": "Mirella", "g": "f", "s": "classic", "r": "any", "d": "wonderful; admirable" },
    { "n": "Norma", "g": "f", "s": "classic", "r": "any", "d": "rule; pattern; northern woman" },
    { "n": "Adele", "g": "f", "s": "classic", "r": "north", "d": "noble; nobility" },
    { "n": "Adriana", "g": "f", "s": "classic", "r": "any", "d": "from Hadria; dark one" },
    { "n": "Alberta", "g": "f", "s": "classic", "r": "north", "d": "noble and bright" },
    { "n": "Amalia", "g": "f", "s": "classic", "r": "any", "d": "work; industrious" },
    { "n": "Bianca", "g": "f", "s": "classic", "r": "any", "d": "white; pure" },
    { "n": "Bruna", "g": "f", "s": "classic", "r": "any", "d": "dark-haired; brown" },
    { "n": "Carolina", "g": "f", "s": "classic", "r": "any", "d": "free woman; song of joy" },
    { "n": "Costanza", "g": "f", "s": "classic", "r": "any", "d": "steadfast; constant" },
    { "n": "Delia", "g": "f", "s": "classic", "r": "any", "d": "from Delos; visible; clear" },
    { "n": "Elettra", "g": "f", "s": "classic", "r": "any", "d": "amber; shining; glittering" },
    { "n": "Emilia", "g": "f", "s": "classic", "r": "north", "d": "rival; eager; from Aemilia" },
    { "n": "Eugenia", "g": "f", "s": "classic", "r": "any", "d": "well-born; noble" },
    { "n": "Eva", "g": "f", "s": "classic", "r": "any", "d": "life; living" },
    { "n": "Fabiola", "g": "f", "s": "classic", "r": "any", "d": "bean grower; from the Fabian clan" },
    { "n": "Fiorella", "g": "f", "s": "classic", "r": "south", "d": "little flower; blossom" },
    { "n": "Flaminia", "g": "f", "s": "classic", "r": "central", "d": "of the Flaminian road; Roman" },
    { "n": "Flora", "g": "f", "s": "classic", "r": "any", "d": "flower; goddess of spring" },
    { "n": "Gianna", "g": "f", "s": "classic", "r": "any", "d": "God is gracious" },
    { "n": "Giuditta", "g": "f", "s": "classic", "r": "any", "d": "woman of Judea; praised" },
    { "n": "Giulietta", "g": "f", "s": "classic", "r": "any", "d": "youthful; romantic; from Verona" },
    { "n": "Ida", "g": "f", "s": "classic", "r": "any", "d": "industrious; hardworking" },
    { "n": "Iolanda", "g": "f", "s": "classic", "r": "any", "d": "violet flower" },
    { "n": "Lara", "g": "f", "s": "classic", "r": "any", "d": "famous; shining; protection" },
    { "n": "Liliana", "g": "f", "s": "classic", "r": "any", "d": "lily; pure" },
    { "n": "Lina", "g": "f", "s": "classic", "r": "any", "d": "short form of names ending in -lina" },
    { "n": "Linda", "g": "f", "s": "classic", "r": "any", "d": "beautiful; pretty" },
    { "n": "Sofia", "g": "f", "s": "modern", "r": "any", "d": "wisdom" },
    { "n": "Giulia", "g": "f", "s": "modern", "r": "any", "d": "youthful; from the Julian clan" },
    { "n": "Alessia", "g": "f", "s": "modern", "r": "any", "d": "defender" },
    { "n": "Aurora", "g": "f", "s": "modern", "r": "any", "d": "dawn; goddess of the dawn" },
    { "n": "Camilla", "g": "f", "s": "modern", "r": "any", "d": "helper at religious rites; noble" },
    { "n": "Gaia", "g": "f", "s": "modern", "r": "any", "d": "earth; goddess of the earth" },
    { "n": "Giorgia", "g": "f", "s": "modern", "r": "any", "d": "farmer; earthworker" },
    { "n": "Greta", "g": "f", "s": "modern", "r": "north", "d": "pearl; northern form of Margherita" },
    { "n": "Vittoria", "g": "f", "s": "modern", "r": "any", "d": "victory" },
    { "n": "Serena", "g": "f", "s": "modern", "r": "any", "d": "tranquil; serene; clear sky" },
    { "n": "Erica", "g": "f", "s": "modern", "r": "any", "d": "heather; eternal ruler" },
    { "n": "Martina", "g": "f", "s": "modern", "r": "any", "d": "of Mars; warlike; strong" },
    { "n": "Alice", "g": "f", "s": "modern", "r": "any", "d": "noble; nobility" },
    { "n": "Noemi", "g": "f", "s": "modern", "r": "any", "d": "pleasantness; my delight" },
    { "n": "Rebecca", "g": "f", "s": "modern", "r": "any", "d": "to bind; captivating" },
    { "n": "Melissa", "g": "f", "s": "modern", "r": "any", "d": "honeybee; sweet" },
    { "n": "Arianna", "g": "f", "s": "modern", "r": "any", "d": "most holy; very pure" },
    { "n": "Sveva", "g": "f", "s": "modern", "r": "north", "d": "Swabian; from the Germanic tribe" },
    { "n": "Luna", "g": "f", "s": "modern", "r": "any", "d": "moon; goddess of the moon" },
    { "n": "Giada", "g": "f", "s": "modern", "r": "any", "d": "jade; green precious stone" },
    { "n": "Assunta", "g": "f", "s": "religious", "r": "south", "d": "assumption; taken up to heaven" },
    { "n": "Concetta", "g": "f", "s": "religious", "r": "south", "d": "immaculate conception; pure" },
    { "n": "Immacolata", "g": "f", "s": "religious", "r": "south", "d": "immaculate; spotless" },
    { "n": "Nunzia", "g": "f", "s": "religious", "r": "south", "d": "short form of Annunziata; announcement" },
    { "n": "Rosaria", "g": "f", "s": "religious", "r": "south", "d": "of the rosary; devotion to Mary" },
    { "n": "Serafina", "g": "f", "s": "religious", "r": "any", "d": "fiery; burning; angelic being" },
    { "n": "Agnese", "g": "f", "s": "religious", "r": "any", "d": "pure; chaste; lamb of God" },
    { "n": "Benedetta", "g": "f", "s": "religious", "r": "any", "d": "blessed" },
    { "n": "Celestina", "g": "f", "s": "religious", "r": "any", "d": "heavenly; of the sky" },
    { "n": "Faustina", "g": "f", "s": "religious", "r": "central", "d": "fortunate; blessed" },
    { "n": "Felicita", "g": "f", "s": "religious", "r": "any", "d": "happiness; good fortune" },
    { "n": "Giuseppa", "g": "f", "s": "religious", "r": "south", "d": "God will add; feminine of Giuseppe" },
    { "n": "Natalia", "g": "f", "s": "religious", "r": "any", "d": "born at Christmas; nativity" },
    { "n": "Teodora", "g": "f", "s": "religious", "r": "any", "d": "gift of God" },
    { "n": "Annunziata", "g": "f", "s": "religious", "r": "south", "d": "the announcement; annunciation" },
    { "n": "Elisabetta", "g": "f", "s": "religious", "r": "any", "d": "pledged to God; my God is an oath" },
    { "n": "Carmela", "g": "f", "s": "regional", "r": "south", "d": "garden; vineyard of God" },
    { "n": "Filomena", "g": "f", "s": "regional", "r": "south", "d": "friend of strength; beloved" },
    { "n": "Graziella", "g": "f", "s": "regional", "r": "south", "d": "graceful; little grace" },
    { "n": "Mariella", "g": "f", "s": "regional", "r": "south", "d": "little Maria; beloved" },
    { "n": "Rossella", "g": "f", "s": "regional", "r": "south", "d": "red-haired; little red one" },
    { "n": "Teresina", "g": "f", "s": "regional", "r": "south", "d": "little Teresa; harvester" },
    { "n": "Peppina", "g": "f", "s": "regional", "r": "south", "d": "familiar form of Giuseppa" },
    { "n": "Agata", "g": "f", "s": "regional", "r": "sicily", "d": "good; virtuous; patron saint of Sicily" },
    { "n": "Rosalia", "g": "f", "s": "regional", "r": "sicily", "d": "rose; patroness of Palermo" },
    { "n": "Gaetana", "g": "f", "s": "regional", "r": "south", "d": "from Gaeta; feminine of Gaetano" },
    { "n": "Calogera", "g": "f", "s": "regional", "r": "sicily", "d": "beautiful elder; feminine of Calogero" },
    { "n": "Fiore", "g": "u", "s": "regional", "r": "south", "d": "flower; blossom" }
  ],
  "surnames": [
    { "n": "Ferrari", "s": "classic", "r": "north", "d": "blacksmith; ironworker" },
    { "n": "Colombo", "s": "classic", "r": "north", "d": "dove; Columbus" },
    { "n": "Ricci", "s": "classic", "r": "north", "d": "curly-haired" },
    { "n": "Ferretti", "s": "classic", "r": "north", "d": "little ironworker; ferryman" },
    { "n": "Brambilla", "s": "classic", "r": "north", "d": "from Brembilla; bramble place" },
    { "n": "Cattaneo", "s": "classic", "r": "north", "d": "captain; chief" },
    { "n": "Galli", "s": "classic", "r": "north", "d": "Gaul; rooster" },
    { "n": "Villa", "s": "classic", "r": "north", "d": "country house; estate" },
    { "n": "Fontana", "s": "classic", "r": "north", "d": "fountain; spring" },
    { "n": "Martini", "s": "classic", "r": "north", "d": "of Mars; son of Martino" },
    { "n": "Moretti", "s": "classic", "r": "north", "d": "dark-skinned; little Moor" },
    { "n": "Pellegrini", "s": "classic", "r": "north", "d": "pilgrim; traveler" },
    { "n": "Carbone", "s": "classic", "r": "north", "d": "coal; charcoal" },
    { "n": "Conti", "s": "classic", "r": "north", "d": "counts; noble title" },
    { "n": "Gatti", "s": "classic", "r": "north", "d": "cats; agile one" },
    { "n": "Lombardi", "s": "classic", "r": "north", "d": "from Lombardy; long-bearded" },
    { "n": "Monti", "s": "classic", "r": "north", "d": "mountains; from the hills" },
    { "n": "Neri", "s": "classic", "r": "north", "d": "black-haired; dark one" },
    { "n": "Riva", "s": "classic", "r": "north", "d": "riverbank; shore" },
    { "n": "Sartori", "s": "classic", "r": "north", "d": "tailor" },
    { "n": "Trevisan", "s": "classic", "r": "north", "d": "from Treviso" },
    { "n": "Verdi", "s": "classic", "r": "north", "d": "green; lush" },
    { "n": "Zanetti", "s": "classic", "r": "north", "d": "little Giovanni; son of Zane" },
    { "n": "Milani", "s": "classic", "r": "north", "d": "from Milan; Milanese" },
    { "n": "Visconti", "s": "classic", "r": "north", "d": "viscount; noble title" },
    { "n": "Paganini", "s": "classic", "r": "north", "d": "little pagan; villager" },
    { "n": "Rossi", "s": "classic", "r": "central", "d": "red-haired; rosy complexion" },
    { "n": "Bianchi", "s": "classic", "r": "central", "d": "white; fair-skinned" },
    { "n": "De Luca", "s": "classic", "r": "central", "d": "of Luca; son of Luca" },
    { "n": "Mancini", "s": "classic", "r": "central", "d": "left-handed" },
    { "n": "Rinaldi", "s": "classic", "r": "central", "d": "wise ruler; son of Rinaldo" },
    { "n": "Mazza", "s": "classic", "r": "central", "d": "club; mace; a strong person" },
    { "n": "Testa", "s": "classic", "r": "central", "d": "head; intelligent person" },
    { "n": "Serra", "s": "classic", "r": "central", "d": "ridge; saw-toothed mountain" },
    { "n": "Gallo", "s": "classic", "r": "central", "d": "rooster; Gaul" },
    { "n": "Romano", "s": "classic", "r": "central", "d": "Roman; from Rome" },
    { "n": "Longo", "s": "classic", "r": "central", "d": "tall; long" },
    { "n": "Costa", "s": "classic", "r": "central", "d": "coast; hillside" },
    { "n": "Marini", "s": "classic", "r": "central", "d": "of the sea; marine" },
    { "n": "Vitali", "s": "classic", "r": "central", "d": "vital; full of life" },
    { "n": "De Angelis", "s": "classic", "r": "central", "d": "of the angels" },
    { "n": "Gentile", "s": "classic", "r": "central", "d": "gentle; noble; kind" },
    { "n": "Grassi", "s": "classic", "r": "central", "d": "fat; stout; well-fed" },
    { "n": "Guerra", "s": "classic", "r": "central", "d": "war; warrior" },
    { "n": "Leone", "s": "classic", "r": "central", "d": "lion; brave" },
    { "n": "Pagano", "s": "classic", "r": "central", "d": "pagan; villager; from the country" },
    { "n": "Parisi", "s": "classic", "r": "central", "d": "from Paris; Parisian" },
    { "n": "Pieri", "s": "classic", "r": "central", "d": "son of Piero; stone" },
    { "n": "Toscano", "s": "classic", "r": "central", "d": "Tuscan; from Tuscany" },
    { "n": "Innocenti", "s": "classic", "r": "central", "d": "innocent; blameless" },
    { "n": "Morandi", "s": "classic", "r": "central", "d": "of Morando; dark one" },
    { "n": "Venturi", "s": "classic", "r": "central", "d": "from Ventura; fortunate" },
    { "n": "Russo", "s": "classic", "r": "south", "d": "red-haired; common in southern Italy" },
    { "n": "Esposito", "s": "classic", "r": "south", "d": "exposed; foundling child; most common Neapolitan name" },
    { "n": "Amato", "s": "classic", "r": "south", "d": "beloved; loved" },
    { "n": "Bruno", "s": "classic", "r": "south", "d": "brown; dark-complexioned" },
    { "n": "Rizzo", "s": "classic", "r": "south", "d": "curly-haired" },
    { "n": "Marino", "s": "classic", "r": "south", "d": "of the sea; mariner" },
    { "n": "Ferraro", "s": "classic", "r": "south", "d": "blacksmith; ironworker" },
    { "n": "Giordano", "s": "classic", "r": "south", "d": "from the Jordan river" },
    { "n": "Fusco", "s": "classic", "r": "south", "d": "dark; dusky" },
    { "n": "Capone", "s": "classic", "r": "south", "d": "big head; capon" },
    { "n": "Caruso", "s": "classic", "r": "south", "d": "close-cropped hair; shaved head" },
    { "n": "D'Angelo", "s": "classic", "r": "south", "d": "of the angel; son of Angelo" },
    { "n": "Di Maio", "s": "classic", "r": "south", "d": "of May; born in May" },
    { "n": "Greco", "s": "classic", "r": "south", "d": "Greek; of Greek origin" },
    { "n": "Napolitano", "s": "classic", "r": "south", "d": "Neapolitan; from Naples" },
    { "n": "Orlando", "s": "classic", "r": "south", "d": "famous throughout the land" },
    { "n": "Palumbo", "s": "classic", "r": "south", "d": "dove; pigeon" },
    { "n": "Petrone", "s": "classic", "r": "south", "d": "big rock; strong as stone" },
    { "n": "Sorrentino", "s": "classic", "r": "south", "d": "from Sorrento; the ancient promontory" },
    { "n": "Vitiello", "s": "classic", "r": "south", "d": "little calf; young one" },
    { "n": "Borrelli", "s": "classic", "r": "south", "d": "from a wooded area; forest dweller" },
    { "n": "Coppola", "s": "classic", "r": "south", "d": "cap maker; hat maker" },
    { "n": "Cuomo", "s": "classic", "r": "south", "d": "from Cuomo; hill" },
    { "n": "De Simone", "s": "classic", "r": "south", "d": "son of Simone; God has heard" },
    { "n": "Iacono", "s": "classic", "r": "south", "d": "deacon; son of Giacomo" },
    { "n": "Iannone", "s": "classic", "r": "south", "d": "from Giovanni; God is gracious" },
    { "n": "Lettieri", "s": "classic", "r": "south", "d": "reader; learned man" },
    { "n": "Ruggiero", "s": "classic", "r": "south", "d": "famous spear; son of Ruggero" },
    { "n": "Sacco", "s": "classic", "r": "south", "d": "sack; bag; sackcloth" },
    { "n": "Lombardo", "s": "classic", "r": "sicily", "d": "Lombard; from Lombardy" },
    { "n": "Messina", "s": "classic", "r": "sicily", "d": "from Messina; the city of straits" },
    { "n": "Battaglia", "s": "classic", "r": "sicily", "d": "battle; fighter" },
    { "n": "Castiglione", "s": "classic", "r": "sicily", "d": "little castle; fortified place" },
    { "n": "Arena", "s": "classic", "r": "sicily", "d": "sand; arena; open space" },
    { "n": "Barone", "s": "classic", "r": "sicily", "d": "baron; noble title" },
    { "n": "Bonafede", "s": "classic", "r": "sicily", "d": "good faith; sincere" },
    { "n": "Cammarata", "s": "classic", "r": "sicily", "d": "from Cammarata; vaulted chamber" },
    { "n": "Catalano", "s": "classic", "r": "sicily", "d": "Catalan; from Catalonia" },
    { "n": "Chiofalo", "s": "classic", "r": "sicily", "d": "from the Sicilian dialect; bald one" },
    { "n": "Collura", "s": "classic", "r": "sicily", "d": "collar maker; from collura" },
    { "n": "Cusumano", "s": "classic", "r": "sicily", "d": "from the Arabic Qusuman; elegant" },
    { "n": "Di Bella", "s": "classic", "r": "sicily", "d": "of beauty; beautiful family" },
    { "n": "Ferreri", "s": "classic", "r": "sicily", "d": "Sicilian ironworker; blacksmith" },
    { "n": "Finocchiaro", "s": "classic", "r": "sicily", "d": "fennel grower; from finocchio" },
    { "n": "La Rosa", "s": "classic", "r": "sicily", "d": "the rose; fragrant beauty" },
    { "n": "Licata", "s": "classic", "r": "sicily", "d": "from Licata; the ancient port city" },
    { "n": "Lo Presti", "s": "classic", "r": "sicily", "d": "the priest; son of the priest" },
    { "n": "Lupo", "s": "classic", "r": "sicily", "d": "wolf; fierce one" },
    { "n": "Mancuso", "s": "classic", "r": "sicily", "d": "left-handed; Sicilian form of Mancini" },
    { "n": "Platania", "s": "classic", "r": "sicily", "d": "from Platania; place of plane trees" },
    { "n": "Ragusa", "s": "classic", "r": "sicily", "d": "from Ragusa; the Sicilian city" },
    { "n": "Salamone", "s": "classic", "r": "sicily", "d": "Solomon; man of peace" },
    { "n": "Salvo", "s": "classic", "r": "sicily", "d": "safe; saved; Sicilian short form" },
    { "n": "Sciortino", "s": "classic", "r": "sicily", "d": "from the Arabic Sciortino; guardian" },
    { "n": "Trovato", "s": "classic", "r": "sicily", "d": "found; foundling child" },
    { "n": "Vitale", "s": "classic", "r": "sicily", "d": "vital; life-giving" }
  ]
}
```

- [ ] **Step 2: Verify the file is valid JSON**

```bash
node -e "const d=require('./wordineer-deploy/data/italian-names.json'); console.log('given:', d.given.length, 'surnames:', d.surnames.length)"
```

Expected output: `given: 201 surnames: 115` (counts will match the file above)

- [ ] **Step 3: Commit**

```bash
git add wordineer-deploy/data/italian-names.json
git commit -m "feat: add italian-names.json dataset (201 given, 115 surnames)"
```

---

## Task 2: Write tests for the data file

**Files:**
- Create: `tests/italian-names-data.test.js`

- [ ] **Step 1: Create the test file**

```javascript
const assert = require('assert');
const fs = require('fs');
const path = require('path');

const file = path.join(__dirname, '..', 'wordineer-deploy', 'data', 'italian-names.json');
assert.ok(fs.existsSync(file), 'italian-names.json should exist');

const data = JSON.parse(fs.readFileSync(file, 'utf8'));

assert.ok(Array.isArray(data.given), 'given should be an array');
assert.ok(Array.isArray(data.surnames), 'surnames should be an array');
assert.ok(data.given.length >= 150, `expected at least 150 given names, got ${data.given.length}`);
assert.ok(data.surnames.length >= 100, `expected at least 100 surnames, got ${data.surnames.length}`);

const VALID_GENDERS = new Set(['m', 'f', 'u']);
const VALID_STYLES = new Set(['classic', 'modern', 'religious', 'regional']);
const VALID_REGIONS = new Set(['north', 'central', 'south', 'sicily', 'any']);

const foundGenders = new Set();
const foundStyles = new Set();
const foundRegions = new Set();

for (const item of data.given) {
  assert.ok(item && typeof item === 'object', 'given entry must be an object');
  assert.strictEqual(typeof item.n, 'string', `given name must be string: ${JSON.stringify(item)}`);
  assert.ok(/^\p{Lu}[\p{L}' -]+$/u.test(item.n), `given name must be title case: ${item.n}`);
  assert.ok(VALID_GENDERS.has(item.g), `invalid gender "${item.g}" for: ${item.n}`);
  assert.ok(VALID_STYLES.has(item.s), `invalid style "${item.s}" for: ${item.n}`);
  assert.ok(VALID_REGIONS.has(item.r), `invalid region "${item.r}" for: ${item.n}`);
  assert.strictEqual(typeof item.d, 'string', `meaning must be string for: ${item.n}`);
  assert.ok(item.d.length > 0, `meaning must not be empty for: ${item.n}`);
  assert.ok(item.d.length <= 120, `meaning too long (${item.d.length} chars) for: ${item.n}`);
  foundGenders.add(item.g);
  foundStyles.add(item.s);
  foundRegions.add(item.r);
}

for (const item of data.surnames) {
  assert.ok(item && typeof item === 'object', 'surname entry must be an object');
  assert.strictEqual(typeof item.n, 'string', `surname must be string: ${JSON.stringify(item)}`);
  assert.ok(/^\p{Lu}[\p{L}' -]+$/u.test(item.n), `surname must be title case: ${item.n}`);
  assert.ok(VALID_STYLES.has(item.s), `invalid style "${item.s}" for surname: ${item.n}`);
  assert.ok(VALID_REGIONS.has(item.r), `invalid region "${item.r}" for surname: ${item.n}`);
  assert.strictEqual(typeof item.d, 'string', `surname meaning must be string for: ${item.n}`);
  assert.ok(item.d.length > 0, `surname meaning must not be empty for: ${item.n}`);
  assert.ok(item.d.length <= 120, `surname meaning too long for: ${item.n}`);
  foundStyles.add(item.s);
  foundRegions.add(item.r);
}

for (const g of ['m', 'f']) {
  assert.ok(foundGenders.has(g), `missing gender ${g} in given names`);
}
for (const s of ['classic', 'modern', 'religious', 'regional']) {
  assert.ok(foundStyles.has(s), `missing style ${s}`);
}
for (const r of ['north', 'central', 'south', 'sicily']) {
  assert.ok(foundRegions.has(r), `missing region ${r}`);
}

console.log(`italian-names.json ok: ${data.given.length} given, ${data.surnames.length} surnames`);
```

- [ ] **Step 2: Run the test**

```bash
node tests/italian-names-data.test.js
```

Expected: `italian-names.json ok: 201 given, 115 surnames`

- [ ] **Step 3: Commit**

```bash
git add tests/italian-names-data.test.js
git commit -m "test: add italian-names.json data validation test"
```

---

## Task 3: Create the tool-src HTML

**Files:**
- Create: `template-deploy/tools-src/random-italian-name-generator.html`

- [ ] **Step 1: Create the file**

```html
<!-- CONFIG { "url": "/random-italian-name-generator/",
  "output": "random-italian-name-generator.html",
  "type": "tool",
  "more_tools_key": "name_generator_tools",
  "more_tools_subtitle": "Every name generator you need, all free"
} -->

<!-- SLOT:meta -->
<title>800+ Random Italian Name Generator - Free Italian Names | Wordineer</title>
<meta name="description" content="Generate random Italian names for characters, stories, games, and ancestry research. Filter by gender, style, region, and starting letter. Free and fast.">
<link rel="canonical" href="https://wordineer.com/random-italian-name-generator/">
<meta property="og:type"        content="website">
<meta property="og:site_name"   content="Wordineer">
<meta property="og:title"       content="800+ Random Italian Names | Wordineer">
<meta property="og:description" content="Generate Italian given names and surnames filtered by gender, style (classic, modern, religious, regional), and region (north, central, south, Sicily).">
<meta property="og:url"         content="https://wordineer.com/random-italian-name-generator/">
<meta property="og:image"       content="https://wordineer.com/og-image.png">
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "What are common Italian last names?",
      "acceptedAnswer": { "@type": "Answer", "text": "The most common Italian surnames include Rossi, Ferrari, Russo, Esposito, Bianchi, Romano, Colombo, Ricci, Marino, and Greco. Rossi (red-haired) and Russo (its southern equivalent) are the most frequent surnames in Italy, similar to Smith in English." }
    },
    {
      "@type": "Question",
      "name": "How are Italian names structured?",
      "acceptedAnswer": { "@type": "Answer", "text": "Italian names follow the Western order: given name first, then surname. Most Italians use one given name and one surname, though middle names are common. Surnames are typically inherited from the father. Since 2022 Italian law allows children to take both parents' surnames." }
    },
    {
      "@type": "Question",
      "name": "What do Italian names mean?",
      "acceptedAnswer": { "@type": "Answer", "text": "Italian names draw heavily from Latin and Ancient Roman roots, Biblical names, saint names, and nature. Names like Marco (warlike), Lucia (light), and Fiore (flower) reflect this heritage. Surnames often describe occupations (Ferrari = blacksmith), physical traits (Ricci = curly-haired), or places of origin (Toscano = from Tuscany)." }
    },
    {
      "@type": "Question",
      "name": "Are Italian names gendered?",
      "acceptedAnswer": { "@type": "Answer", "text": "Yes. Italian names are strongly gendered. Male names commonly end in -o (Marco, Carlo, Bruno) while female names end in -a (Maria, Rosa, Giulia). There are exceptions — Andrea is male in Italian — but gender assignment is clear for the vast majority of names." }
    },
    {
      "@type": "Question",
      "name": "What is the difference between northern and southern Italian names?",
      "acceptedAnswer": { "@type": "Answer", "text": "Northern Italian names often reflect Germanic, French, and Celtic influences (Aldo, Ugo, Franca, Adele). Southern names, especially from Naples and Sicily, show stronger Spanish, Norman, and Greek influences (Gennaro, Carmela, Calogero, Assunta). Regional names are distinct enough that they can hint at a character's hometown or ancestry." }
    },
    {
      "@type": "Question",
      "name": "Can I use these Italian names for a story or character?",
      "acceptedAnswer": { "@type": "Answer", "text": "Yes. The generated names are drawn from real Italian given names and surnames and can be used freely in fiction, games, screenplays, and creative projects. The meaning notes are short creative hints, not a formal naming authority." }
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
.ctrl       { width:300px; padding:18px; border-right:1px solid var(--border-2); background:var(--bg-2); flex-shrink:0; }
.ctrl-row   { margin-bottom:14px; }
.ctrl-label { font-size:10px; font-weight:600; color:var(--text-3); text-transform:uppercase; letter-spacing:.06em; display:block; margin-bottom:5px; }
.ctrl-row input, .ctrl-row select { width:100%; padding:7px 10px; font-size:13px; font-family:inherit; border:1px solid var(--border); border-radius:7px; background:var(--bg); color:var(--text); appearance:none; outline:none; transition:border-color .15s; }
.ctrl-row input:focus, .ctrl-row select:focus { border-color:var(--brand); }
.def-row    { display:flex; align-items:center; gap:8px; margin-bottom:14px; }
.def-row label { font-size:12px; color:var(--text-2); cursor:pointer; }
.toggle     { position:relative; width:32px; height:18px; flex-shrink:0; }
.toggle input { opacity:0; width:0; height:0; }
.toggle-sl  { position:absolute; cursor:pointer; inset:0; background:var(--border); border-radius:9px; transition:.2s; }
.toggle input:checked + .toggle-sl { background:var(--brand); }
.toggle-sl::before { content:''; position:absolute; width:14px; height:14px; left:2px; top:2px; background:white; border-radius:50%; transition:.2s; }
.toggle input:checked + .toggle-sl::before { transform:translateX(14px); }
.gen-btn    { width:100%; padding:10px 14px; background:var(--brand); color:white; border:none; border-radius:8px; font-size:14px; font-weight:600; font-family:inherit; cursor:pointer; transition:background .15s,transform .1s; letter-spacing:-.01em; }
.gen-btn:hover { background:var(--brand-dark); }
.gen-btn:active { transform:scale(.98); }
.reset-btn  { display:block; width:100%; text-align:center; font-size:11px; color:var(--text-3); margin-top:8px; cursor:pointer; text-decoration:underline; text-underline-offset:2px; border:none; background:none; font-family:inherit; }
.ng-mobile-toggle { display:none; width:100%; margin:-2px 0 14px; padding:9px 12px; border:1px solid var(--border); border-radius:8px; background:var(--bg); color:var(--brand); font-size:13px; font-weight:600; font-family:inherit; cursor:pointer; }
.ng-advanced { display:block; }
.result-area { flex:1; min-width:0; padding:18px; }
.result-top { display:flex; align-items:center; justify-content:space-between; gap:12px; margin-bottom:12px; }
.result-count { font-size:13px; color:var(--text-3); }
.actions { display:flex; gap:8px; flex-wrap:wrap; }
.btn-small { padding:8px 11px; border:1px solid var(--border); border-radius:8px; background:var(--bg); color:var(--text); font-size:13px; cursor:pointer; }
.word-list { list-style:none; padding:0; margin:0; display:grid; gap:10px; }
.word-item { display:flex; align-items:flex-start; justify-content:space-between; gap:12px; padding:14px; border:1px solid var(--border); border-radius:8px; background:var(--bg); }
.word-left { min-width:0; }
.word-text { font-size:22px; line-height:1.2; font-weight:750; color:var(--text); margin-bottom:6px; }
.ng-meaning { font-size:13px; color:var(--text-2); line-height:1.45; margin-top:6px; }
.ing-badges { display:flex; flex-wrap:wrap; gap:5px; }
.ing-badge { display:inline-flex; align-items:center; padding:3px 7px; border-radius:999px; background:#EEF6E8; color:#2F6B1F; font-size:11px; font-weight:700; text-transform:capitalize; }
.ing-badge--region { background:#FEF3E2; color:#8B5A0A; }
.word-right { display:flex; gap:6px; flex-shrink:0; }
.icon-btn { width:34px; height:34px; display:inline-flex; align-items:center; justify-content:center; border:none; border-radius:8px; background:var(--bg); color:var(--text-2); cursor:pointer; }
.icon-btn svg { width:16px; height:16px; }
.icon-btn.saved { color:#E24B4A; background:#FFF5F5; }
.saved-panel { margin-top:18px; padding:14px; border:1px solid var(--border); border-radius:8px; background:var(--bg-2); }
.saved-title { font-size:13px; font-weight:700; color:var(--text); margin-bottom:10px; }
.saved-tags { display:flex; flex-wrap:wrap; gap:7px; }
.saved-tags span { display:inline-flex; align-items:center; gap:6px; padding:6px 8px; border:1px solid var(--border); border-radius:999px; background:var(--bg); font-size:12px; }
.saved-tags button { border:0; background:transparent; color:var(--text-3); cursor:pointer; padding:0; }
.content-section { max-width:900px; margin:34px auto 0; padding:0 24px; }
.content-section h2 { margin:0 0 10px; font-size:26px; line-height:1.2; }
.content-section p { color:var(--text-2); line-height:1.7; }
.content-section a { color:var(--brand); text-decoration:underline; text-underline-offset:3px; }
.content-grid { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:18px; margin-top:18px; }
.content-box { border:1px solid var(--border); border-radius:8px; padding:16px; background:var(--bg); }
.content-box h3 { margin:0 0 8px; font-size:17px; }

@media (max-width: 760px) {
  .hero--tool .hero-copy p { display:none; }
  .tool-wrap { padding:16px 14px 0; }
  .tool-split { display:block; }
  .ctrl { width:100%; border-right:none; border-bottom:1px solid var(--border-2); }
  .ng-mobile-toggle { display:block; margin:10px 0 14px; }
  .ng-advanced { display:none; }
  .ng-advanced.is-open { display:block; }
  .result-top { align-items:flex-start; flex-direction:column; }
  .word-item { align-items:flex-start; }
  .word-text { font-size:20px; }
  .content-grid { grid-template-columns:1fr; }
}
</style>
<!-- /SLOT:style -->

<!-- SLOT:hero -->
<section class="hero hero--tool">
  <div class="hero-inner">
    <div class="hero-copy">
      <span class="hero-badge">Free &middot; No sign-up &middot; Instant</span>
      <h1>Random Italian Name Generator</h1>
      <p>Generate authentic Italian names filtered by gender, style, and region. Classic, modern, religious, and dialectal forms.</p>
    </div>
  </div>
</section>
<!-- /SLOT:hero -->

<!-- SLOT:tool -->
<main class="tool-wrap">
  <section class="tool-card" aria-label="Random Italian name generator">
    <div class="tool-split">
      <div class="ctrl">
        <div class="ctrl-row">
          <label class="ctrl-label" for="ing-count">Number of names</label>
          <input type="number" id="ing-count" value="5" min="1" max="50" inputmode="numeric">
        </div>

        <div class="ctrl-row">
          <label class="ctrl-label" for="ing-gender">Gender</label>
          <select id="ing-gender">
            <option value="any">Any</option>
            <option value="m">Male</option>
            <option value="f">Female</option>
          </select>
        </div>

        <div class="ctrl-row">
          <label class="ctrl-label" for="ing-type">Name type</label>
          <select id="ing-type">
            <option value="given">Given name only</option>
            <option value="full">Full name</option>
            <option value="surname">Surname only</option>
          </select>
        </div>

        <button type="button" class="ng-mobile-toggle" id="ing-mobile-toggle" aria-expanded="false" aria-controls="ing-advanced">More options</button>

        <div class="ng-advanced" id="ing-advanced">
          <div class="ctrl-row">
            <label class="ctrl-label" for="ing-style">Style</label>
            <select id="ing-style">
              <option value="any">Any style</option>
              <option value="classic">Classic &amp; Traditional</option>
              <option value="modern">Modern</option>
              <option value="religious">Religious &amp; Saint</option>
              <option value="regional">Regional &amp; Dialectal</option>
            </select>
          </div>

          <div class="ctrl-row">
            <label class="ctrl-label" for="ing-region">Region</label>
            <select id="ing-region">
              <option value="any">Any region</option>
              <option value="north">Northern Italy</option>
              <option value="central">Central Italy</option>
              <option value="south">Southern Italy</option>
              <option value="sicily">Sicily</option>
            </select>
          </div>

          <div class="ctrl-row">
            <label class="ctrl-label" for="ing-letter">Starts with</label>
            <select id="ing-letter">
              <option value="any">Any letter</option>
              <option value="a">A</option><option value="b">B</option><option value="c">C</option><option value="d">D</option>
              <option value="e">E</option><option value="f">F</option><option value="g">G</option><option value="h">H</option>
              <option value="i">I</option><option value="j">J</option><option value="k">K</option><option value="l">L</option>
              <option value="m">M</option><option value="n">N</option><option value="o">O</option><option value="p">P</option>
              <option value="q">Q</option><option value="r">R</option><option value="s">S</option><option value="t">T</option>
              <option value="u">U</option><option value="v">V</option><option value="w">W</option><option value="x">X</option>
              <option value="y">Y</option><option value="z">Z</option>
            </select>
          </div>

          <div class="def-row">
            <label class="toggle" aria-label="Show meanings"><input type="checkbox" id="ing-defs" checked><span class="toggle-sl"></span></label>
            <label for="ing-defs">Show meanings</label>
          </div>
        </div>

        <button class="gen-btn" id="ing-gen-btn">Generate names</button>
        <button class="reset-btn" id="ing-reset-btn">Reset options</button>
        <div class="kbd">Press <kbd>Space</kbd> to regenerate</div>
      </div>

      <div class="result-area">
        <div class="result-top">
          <span class="result-count" id="ing-count-display">Generating...</span>
          <div class="actions">
            <button class="btn-small" id="ing-copy-all-btn">Copy all</button>
          </div>
        </div>
        <ul class="word-list" id="ing-list"></ul>

        <div class="saved-panel">
          <div class="saved-title">Saved names</div>
          <div class="saved-top" style="display:flex;align-items:center;justify-content:space-between;gap:8px;margin-bottom:10px;">
            <span class="saved-label">Tap the heart on a name to save it here</span>
            <button class="saved-copy" id="ing-copy-saved-btn">Copy saved</button>
          </div>
          <div class="saved-tags" id="ing-saved-tags">
            <span class="saved-empty">Click the heart on any name to save it here</span>
          </div>
        </div>
      </div>
    </div>
  </section>
</main>
<!-- /SLOT:tool -->

<!-- SLOT:explainer -->
<div class="explainer">
  <h2>What Is a Random Italian Name Generator?</h2>
  <p>A random Italian name generator creates Italian given names, surnames, or full name combinations from a curated dataset of real Italian names. It is useful for writers building characters set in Italy, game designers populating Italian-themed worlds, ancestry researchers looking up naming patterns, and language learners exploring the culture behind Italian words.</p>

  <h2>How It Works</h2>
  <p>Choose how many names you want, then narrow results with gender, name type, style, region, or starting letter. Results update automatically whenever you change a filter. On mobile, tap <strong>More options</strong> to reveal the style, region, and letter controls. The tool loads a dedicated Italian name dataset covering classic and traditional forms, modern given names, religious and saint names, and regional and dialectal forms from all parts of Italy.</p>

  <h2>Italian Names: Style and Regional Variety</h2>
  <p>Italian naming has distinct regional flavors. Northern names like Aldo, Ugo, and Franca reflect Germanic and French influence from centuries of trade and migration. Central Italian names from Tuscany and Rome, such as Beatrice, Cesare, and Dante, carry the weight of the Renaissance and classical antiquity. Southern names from Naples, Calabria, and Puglia — Gennaro, Carmela, Ciro — show Spanish, Norman, and Greek heritage. Sicilian names like Calogero and Rosalia are recognizable to anyone familiar with the island's distinct identity.</p>

  <h2>More Random Name Generators</h2>
  <p>Need names from another culture? Try the <a href="/random-name-generator/">random name generator</a> for broad options across 30+ origins, or use focused tools like the <a href="/random-spanish-name-generator/">random Spanish name generator</a>, <a href="/random-french-name-generator/">random French name generator</a>, and <a href="/random-greek-name-generator/">random Greek name generator</a>.</p>
</div>
<!-- /SLOT:explainer -->

<!-- SLOT:faq -->
<div class="faq">
  <h2 class="faq-title">Frequently asked questions</h2>
  <div class="faq-item open">
    <div class="faq-q"><span class="faq-q-text">What are common Italian last names?</span><svg class="faq-chevron" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div>
    <div class="faq-a">The most common Italian surnames include Rossi, Ferrari, Russo, Esposito, Bianchi, Romano, Colombo, Ricci, Marino, and Greco. Rossi (red-haired) tops the list in northern and central Italy, while Russo, its southern equivalent, dominates in the south. Many Italian surnames derive from occupations, physical traits, or places of origin.</div>
  </div>
  <div class="faq-item">
    <div class="faq-q"><span class="faq-q-text">How are Italian names structured?</span><svg class="faq-chevron" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div>
    <div class="faq-a">Italian names follow the Western order: given name first, then surname. Most Italians use one given name and one surname. Since 2022, Italian law allows children to take both parents' surnames, so double-barrelled surnames are increasingly common in new generations.</div>
  </div>
  <div class="faq-item">
    <div class="faq-q"><span class="faq-q-text">What do Italian names mean?</span><svg class="faq-chevron" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div>
    <div class="faq-a">Italian names draw heavily from Latin and Roman roots, the Bible, and saint names. Marco means warlike, Lucia means light, and Fiore means flower. Surnames often describe occupations (Ferrari = blacksmith), physical traits (Ricci = curly-haired), or places (Toscano = from Tuscany). The meaning notes on each generated name give a short summary.</div>
  </div>
  <div class="faq-item">
    <div class="faq-q"><span class="faq-q-text">Are Italian names gendered?</span><svg class="faq-chevron" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div>
    <div class="faq-a">Yes. Italian names are strongly gendered. Male names commonly end in -o (Marco, Carlo, Bruno) and female names in -a (Maria, Rosa, Giulia). One notable exception is Andrea, which is male in Italian despite being female in many other languages. The gender filter on this tool reflects standard Italian usage.</div>
  </div>
  <div class="faq-item">
    <div class="faq-q"><span class="faq-q-text">What is the difference between northern and southern Italian names?</span><svg class="faq-chevron" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div>
    <div class="faq-a">Northern Italian names reflect Germanic, French, and Celtic influences — Aldo, Ugo, Franca, Adele. Southern names, especially from Naples and Sicily, carry Spanish, Norman, and Greek heritage — Gennaro, Carmela, Calogero, Assunta. Regional names can hint clearly at a character's hometown or ancestry, which is useful for writers building geographically grounded stories.</div>
  </div>
  <div class="faq-item">
    <div class="faq-q"><span class="faq-q-text">Is this Italian name generator free?</span><svg class="faq-chevron" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div>
    <div class="faq-a">Yes. It is completely free to use, with no account, no sign-up, and no limit on how many names you generate. The Italian name data loads from a static file so the page stays fast.</div>
  </div>
</div>
<!-- /SLOT:faq -->

<!-- SLOT:who -->
<div>
  <h2 class="section-title" style="margin-bottom:14px">Who uses Wordineer</h2>
  <div class="uc-grid">
    <div class="uc"><div class="uc-title">Writers &amp; Storytellers</div><div class="uc-body">Find Italian character names with meanings and regional context that fit a story's setting and tone.</div></div>
    <div class="uc"><div class="uc-title">Game Designers</div><div class="uc-body">Generate NPC names, faction rosters, and character shortlists for Italian-themed games and visual novels.</div></div>
    <div class="uc"><div class="uc-title">Ancestry Researchers</div><div class="uc-body">Explore Italian surname origins, regional patterns, and the meaning behind family names before deeper research.</div></div>
    <div class="uc"><div class="uc-title">Language Learners</div><div class="uc-body">Browse authentic Italian names to practice recognition of gendered endings, regional patterns, and cultural context.</div></div>
  </div>
</div>
<!-- /SLOT:who -->

<!-- SLOT:init -->
<script src="/scripts/tool-engine.js"></script>
<script>
const ING_STYLE_LABELS = {
  classic: 'Classic',
  modern: 'Modern',
  religious: 'Religious',
  regional: 'Regional'
};
const ING_REGION_LABELS = {
  north: 'Northern Italy',
  central: 'Central Italy',
  south: 'Southern Italy',
  sicily: 'Sicily'
};
let ingData = { given: [], surnames: [] };
let ingReady = false;
let ingCurrentItems = [];

function ingEsc(s) {
  return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}

function ingShuffle(arr) {
  const a = arr.slice();
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

function ingCount() {
  const v = parseInt(document.getElementById('ing-count')?.value, 10);
  if (isNaN(v)) return 5;
  return Math.max(1, Math.min(50, v));
}

function ingDefsVisible() {
  return document.getElementById('ing-defs')?.checked !== false;
}

function ingNormalizeGiven(entry) {
  if (!entry || typeof entry !== 'object') return null;
  const n = String(entry.n || '').trim();
  if (!n) return null;
  return [n, String(entry.g || 'u'), String(entry.s || 'classic'), String(entry.r || 'any'), String(entry.d || '')];
}

function ingNormalizeSurname(entry) {
  if (!entry || typeof entry !== 'object') return null;
  const n = String(entry.n || '').trim();
  if (!n) return null;
  return [n, String(entry.s || 'classic'), String(entry.r || 'any'), String(entry.d || '')];
}

function ingNoResultsItem() {
  return {
    display: 'No matching Italian names found',
    meaning: 'Try a broader style, region, gender, or starting letter.',
    style: '',
    region: '',
    noResult: true
  };
}

function ingCurrentFilterValues() {
  return {
    type:   document.getElementById('ing-type')?.value   || 'given',
    gender: document.getElementById('ing-gender')?.value || 'any',
    style:  document.getElementById('ing-style')?.value  || 'any',
    region: document.getElementById('ing-region')?.value || 'any',
    letter: document.getElementById('ing-letter')?.value || 'any'
  };
}

function ingGenerateFn(data) {
  if (!ingReady || !data.given.length || !data.surnames.length) {
    return [{ display: 'Loading Italian names...', meaning: 'Please wait while the name data loads.', style: 'classic', region: '' }];
  }

  const filters = ingCurrentFilterValues();
  const limit = ingCount();
  const letter = filters.letter === 'any' ? '' : filters.letter.toUpperCase();

  const givenPool = data.given.filter(function(n) {
    if (filters.gender !== 'any' && n[1] !== filters.gender && n[1] !== 'u') return false;
    if (filters.style !== 'any' && n[2] !== filters.style) return false;
    if (filters.region !== 'any' && n[3] !== 'any' && n[3] !== filters.region) return false;
    if (letter && !n[0].toUpperCase().startsWith(letter)) return false;
    return true;
  });

  const surnamePool = data.surnames.filter(function(n) {
    if (filters.style !== 'any' && n[1] !== filters.style) return false;
    if (filters.region !== 'any' && n[2] !== 'any' && n[2] !== filters.region) return false;
    if (letter && filters.type === 'surname' && !n[0].toUpperCase().startsWith(letter)) return false;
    return true;
  });

  if (filters.type === 'given' && !givenPool.length) return [ingNoResultsItem()];
  if (filters.type === 'surname' && !surnamePool.length) return [ingNoResultsItem()];
  if (filters.type === 'full' && (!givenPool.length || !surnamePool.length)) return [ingNoResultsItem()];

  const sg = ingShuffle(givenPool);
  const ss = ingShuffle(surnamePool);
  const results = [];
  const seen = new Set();
  let gi = 0;
  let si = 0;
  let guard = 0;

  while (results.length < limit && guard < limit * 40) {
    guard++;

    if (filters.type === 'given') {
      const given = sg[gi++ % sg.length];
      if (!given) break;
      if (seen.has(given[0])) continue;
      seen.add(given[0]);
      results.push({ display: given[0], meaning: given[4], style: given[2], region: given[3] === 'any' ? '' : given[3], kind: 'given' });
      continue;
    }

    if (filters.type === 'surname') {
      const surname = ss[si++ % ss.length];
      if (!surname) break;
      if (seen.has(surname[0])) continue;
      seen.add(surname[0]);
      results.push({ display: surname[0], meaning: surname[3], style: surname[1], region: surname[2] === 'any' ? '' : surname[2], kind: 'surname' });
      continue;
    }

    const given = sg[gi++ % sg.length];
    const surname = ss[si++ % ss.length];
    if (!given || !surname) break;
    if (letter && !given[0].toUpperCase().startsWith(letter)) continue;
    const display = given[0] + ' ' + surname[0];
    if (seen.has(display)) continue;
    seen.add(display);
    const meaningParts = [given[4], surname[3]].filter(Boolean);
    results.push({
      display,
      meaning: meaningParts.join('; '),
      style: given[2],
      region: surname[2] === 'any' ? (given[3] === 'any' ? '' : given[3]) : surname[2],
      kind: 'full'
    });
  }

  ingCurrentItems = results.slice();
  return results.length ? results : [ingNoResultsItem()];
}

function ingRenderItem(item) {
  if (item.noResult) {
    return '<li class="word-item ing-no-results">'
      + '<div class="word-left">'
      +   '<div class="word-text">' + ingEsc(item.display) + '</div>'
      +   '<div class="ng-meaning">' + ingEsc(item.meaning) + '</div>'
      + '</div>'
      + '</li>';
  }

  let savedArr = [];
  try { savedArr = JSON.parse(localStorage.getItem('wnr_saved_it_names') || '[]'); } catch {}
  const isSaved = savedArr.includes(item.display);
  const safeAttr = item.display.replace(/"/g, '&quot;');
  const safeClick = item.display.replace(/\\/g, '\\\\').replace(/'/g, "\\'");
  const styleBadge = item.style ? '<span class="ing-badge">' + ingEsc(ING_STYLE_LABELS[item.style] || item.style) + '</span>' : '';
  const regionBadge = item.region ? '<span class="ing-badge ing-badge--region">' + ingEsc(ING_REGION_LABELS[item.region] || item.region) + '</span>' : '';
  const meaningLine = ingDefsVisible() && item.meaning ? '<div class="ng-meaning">' + ingEsc(item.meaning) + '</div>' : '';

  return '<li class="word-item">'
    + '<div class="word-left">'
    +   '<div class="word-text">' + ingEsc(item.display) + '</div>'
    +   '<div class="ing-badges">' + styleBadge + regionBadge + '</div>'
    +   meaningLine
    + '</div>'
    + '<div class="word-right">'
    +   '<button class="icon-btn" title="Copy" onclick="ingCopyName(\'' + safeClick + '\',this)">'
    +     '<svg viewBox="0 0 14 14" fill="none"><rect x="1" y="4" width="9" height="9.5" rx="1.5" stroke="currentColor" stroke-width="1.1"/><path d="M4.5 4V2.5A1.5 1.5 0 016 1h5.5A1.5 1.5 0 0113 2.5v7a1.5 1.5 0 01-1.5 1.5H10" stroke="currentColor" stroke-width="1.1"/></svg>'
    +   '</button>'
    +   '<button class="icon-btn' + (isSaved ? ' saved' : '') + '" title="' + (isSaved ? 'Unsave' : 'Save') + '" data-action="save" data-name="' + safeAttr + '">'
    +     '<svg viewBox="0 0 16 16" fill="none"><path d="M8 13.5S2 9.5 2 5.5A3 3 0 018 4a3 3 0 016 1.5c0 4-6 8-6 8z" stroke="currentColor" stroke-width="1.3" fill="' + (isSaved ? '#E24B4A' : 'none') + '"/></svg>'
    +   '</button>'
    + '</div>'
    + '</li>';
}

function ingRenderCurrentItems() {
  const list = document.getElementById('ing-list');
  if (!list || !ingCurrentItems.length) return;
  list.innerHTML = '';
  ingCurrentItems.forEach(function(item) {
    const wrapper = document.createElement('div');
    wrapper.innerHTML = ingRenderItem(item);
    list.appendChild(wrapper.firstElementChild || wrapper);
  });
}

function ingCopyName(name, btn) {
  navigator.clipboard.writeText(name).then(function() {
    const old = btn.innerHTML;
    btn.textContent = '✓';
    setTimeout(function(){ btn.innerHTML = old; }, 900);
  });
}

function ingSyncNoResultCount() {
  setTimeout(function() {
    const list = document.getElementById('ing-list');
    const display = document.getElementById('ing-count-display');
    if (list?.querySelector('.ing-no-results') && display) display.textContent = '0 results found';
  }, 0);
}

function ingRegenerateFromFilters() {
  document.getElementById('ing-gen-btn')?.click();
  ingSyncNoResultCount();
}

window.ingCopyName = ingCopyName;

fetch('/data/italian-names.json', { cache: 'force-cache' })
  .then(function(res) {
    if (!res.ok) throw new Error('Italian name data failed to load');
    return res.json();
  })
  .then(function(data) {
    ingData = {
      given:    Array.isArray(data?.given)    ? data.given.map(ingNormalizeGiven).filter(Boolean)       : [],
      surnames: Array.isArray(data?.surnames) ? data.surnames.map(ingNormalizeSurname).filter(Boolean)  : []
    };
    ingReady = true;
    WORDINEER.init({
      mode:           'custom',
      data:           ingData,
      renderItem:     ingRenderItem,
      generateFn:     ingGenerateFn,
      listId:         'ing-list',
      countDisplayId: 'ing-count-display',
      generateBtnId:  'ing-gen-btn',
      copyAllBtnId:   'ing-copy-all-btn',
      savedKey:       'wnr_saved_it_names',
      savedListId:    'ing-saved-tags'
    });
    ingRegenerateFromFilters();
  })
  .catch(function() {
    const display = document.getElementById('ing-count-display');
    if (display) display.textContent = 'Name data could not load. Please refresh and try again.';
  });

const ingCountInput = document.getElementById('ing-count');
ingCountInput?.addEventListener('input', ingRegenerateFromFilters);
ingCountInput?.addEventListener('change', ingRegenerateFromFilters);
document.getElementById('ing-gen-btn')?.addEventListener('click', ingSyncNoResultCount);
document.getElementById('ing-defs')?.addEventListener('change', ingRenderCurrentItems);
['ing-type','ing-gender','ing-style','ing-region','ing-letter'].forEach(function(id) {
  const el = document.getElementById(id);
  if (!el) return;
  el.addEventListener('change', ingRegenerateFromFilters);
  el.addEventListener('input',  ingRegenerateFromFilters);
});
document.getElementById('ing-reset-btn')?.addEventListener('click', function() {
  document.getElementById('ing-count').value = '5';
  document.getElementById('ing-type').value = 'given';
  document.getElementById('ing-gender').value = 'any';
  document.getElementById('ing-style').value = 'any';
  document.getElementById('ing-region').value = 'any';
  document.getElementById('ing-letter').value = 'any';
  document.getElementById('ing-defs').checked = true;
  ingRegenerateFromFilters();
});
document.getElementById('ing-mobile-toggle')?.addEventListener('click', function() {
  const advanced = document.getElementById('ing-advanced');
  const isOpen = advanced?.classList.toggle('is-open');
  this.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
  this.textContent = isOpen ? 'Hide options' : 'More options';
});

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

- [ ] **Step 2: Commit**

```bash
git add template-deploy/tools-src/random-italian-name-generator.html
git commit -m "feat: add random-italian-name-generator tool-src"
```

---

## Task 4: Write tests for the page

**Files:**
- Create: `tests/italian-generator-page.test.js`

- [ ] **Step 1: Create the test file**

```javascript
const assert = require('assert');
const fs = require('fs');
const path = require('path');

const root = path.join(__dirname, '..');
const sourcePath = path.join(root, 'template-deploy', 'tools-src', 'random-italian-name-generator.html');
const deployPath = path.join(root, 'wordineer-deploy', 'random-italian-name-generator.html');

assert.ok(fs.existsSync(sourcePath), 'source Italian page should exist');

const source = fs.readFileSync(sourcePath, 'utf8');

function mustInclude(haystack, needle, label) {
  assert.ok(haystack.includes(needle), `${label} should include: ${needle}`);
}

mustInclude(source, 'CONFIG { "url": "/random-italian-name-generator/"', 'source config');
mustInclude(source, '800+ Random Italian Name Generator', 'source title');
mustInclude(source, '/data/italian-names.json', 'source data fetch path');

for (const id of [
  'ing-count',
  'ing-mobile-toggle',
  'ing-advanced',
  'ing-type',
  'ing-gender',
  'ing-style',
  'ing-region',
  'ing-letter',
  'ing-defs',
  'ing-gen-btn',
  'ing-reset-btn',
  'ing-list',
  'ing-saved-tags'
]) {
  mustInclude(source, `id="${id}"`, `${id} control`);
}

mustInclude(source, '<option value="given">Given name only</option>', 'default given-name option');
mustInclude(source, 'value="5"', 'default count is 5');
mustInclude(source, 'What Is a Random Italian Name Generator?', 'explainer heading');
mustInclude(source, 'How It Works', 'how it works heading');
mustInclude(source, 'Italian Names: Style and Regional Variety', 'style explainer heading');
mustInclude(source, 'class="explainer"', 'explainer wrapper');
mustInclude(source, 'faq-item', 'faq accordion layout');
mustInclude(source, 'uc-grid', 'who uses grid layout');
mustInclude(source, 'Who uses Wordineer', 'who uses heading');
mustInclude(source, '"@type": "FAQPage"', 'FAQ schema');
mustInclude(source, "savedKey:       'wnr_saved_it_names'", 'saved key');
mustInclude(source, 'WORDINEER.init(', 'WORDINEER init call');

const filterIds = ['ing-type', 'ing-gender', 'ing-style', 'ing-region', 'ing-letter'];
for (const id of filterIds) {
  mustInclude(source, `'${id}'`, `${id} referenced in source`);
}

mustInclude(source, "value=\"regional\">Regional &amp; Dialectal", 'regional style option');
mustInclude(source, "value=\"sicily\">Sicily", 'sicily region option');
mustInclude(source, "value=\"religious\">Religious &amp; Saint", 'religious style option');

if (fs.existsSync(deployPath)) {
  const deploy = fs.readFileSync(deployPath, 'utf8');
  mustInclude(deploy, '800+ Random Italian Name Generator', 'deploy title');
  mustInclude(deploy, '/data/italian-names.json', 'deploy data fetch path');
  mustInclude(deploy, 'id="ing-count"', 'deploy count control');
  mustInclude(deploy, 'What Is a Random Italian Name Generator?', 'deploy explainer');
  mustInclude(deploy, 'faq-item', 'deploy faq accordion layout');
  mustInclude(deploy, 'Who uses Wordineer', 'deploy who uses section');
  mustInclude(deploy, 'WORDINEER.init(', 'deploy WORDINEER init');
}

console.log('Italian generator page static checks ok');
```

- [ ] **Step 2: Run the test (source checks only — deploy file not built yet)**

```bash
node tests/italian-generator-page.test.js
```

Expected: `Italian generator page static checks ok`

- [ ] **Step 3: Commit**

```bash
git add tests/italian-generator-page.test.js
git commit -m "test: add Italian generator page static checks"
```

---

## Task 5: Update tools.json

**Files:**
- Modify: `template-deploy/tools.json`

- [ ] **Step 1: Add to mega Name generators section**

In `template-deploy/tools.json`, find the `"cat": "Name generators"` block inside `"mega"`. It currently ends before `"href": "/name-generators/"`. Insert the Italian entry before that final "More Name Gen Tools" link:

```json
{
  "href": "/random-italian-name-generator/",
  "text": "Italian Name Generator"
},
```

- [ ] **Step 2: Add to more_word_tools array**

In the `"more_word_tools"` array, insert after the Norwegian Name entry (or before the "More Name Gen Tools" entries):

```json
{
  "href": "/random-italian-name-generator/",
  "name": "Random Italian Name",
  "desc": "Italian names by gender, region, and style.",
  "icon_bg": "#FEF3E2",
  "icon_path": "<rect x=\"2\" y=\"3\" width=\"9\" height=\"7\" rx=\"1.2\" fill=\"#FFFAF4\" stroke=\"#8B5A0A\" stroke-width=\".9\"/><path d=\"M2.8 4.1h7.4M2.8 6.5h7.4M2.8 8.9h7.4\" stroke=\"#8B5A0A\" stroke-width=\".85\" stroke-linecap=\"round\"/><path d=\"M4.2 3.4v6.2\" stroke=\"#2F7A2F\" stroke-width=\".75\" stroke-linecap=\"round\"/><path d=\"M8.8 3.4v6.2\" stroke=\"#C53A3A\" stroke-width=\".75\" stroke-linecap=\"round\"/>",
  "new": true
},
```

- [ ] **Step 3: Add to other_tools and footer_cols**

Find the name generators category in `"other_tools"` and add:

```json
{ "href": "/random-italian-name-generator/", "text": "Italian Name Generator" }
```

Find the name generators column in `"footer_cols"` and add:

```json
{ "href": "/random-italian-name-generator/", "text": "Italian Name Generator" }
```

- [ ] **Step 4: Commit**

```bash
git add template-deploy/tools.json
git commit -m "feat: add Italian name generator to tools.json nav"
```

---

## Task 6: Update _redirects and sitemap.xml

**Files:**
- Modify: `wordineer-deploy/_redirects`
- Modify: `wordineer-deploy/sitemap.xml`

- [ ] **Step 1: Add redirect rule**

In `wordineer-deploy/_redirects`, add the canonical redirect for the clean URL. Follow the existing pattern (e.g. the Scottish entry). Add:

```
/random-italian-name-generator/ /random-italian-name-generator.html 200
```

- [ ] **Step 2: Add sitemap entry**

In `wordineer-deploy/sitemap.xml`, add a new `<url>` entry following the existing pattern:

```xml
<url>
  <loc>https://wordineer.com/random-italian-name-generator/</loc>
  <changefreq>monthly</changefreq>
  <priority>0.7</priority>
</url>
```

- [ ] **Step 3: Commit**

```bash
git add wordineer-deploy/_redirects wordineer-deploy/sitemap.xml
git commit -m "feat: add Italian name generator URL redirect and sitemap entry"
```

---

## Task 7: Build, copy, and verify

**Files:**
- Generated: `wordineer-deploy/random-italian-name-generator.html`

- [ ] **Step 1: Build**

```bash
cd template-deploy && python3 build.py
```

Expected: no errors; `output/random-italian-name-generator.html` should appear in the output listing.

- [ ] **Step 2: Copy to deploy folder**

```bash
cp template-deploy/output/random-italian-name-generator.html wordineer-deploy/
```

- [ ] **Step 3: Run all tests**

```bash
node tests/italian-names-data.test.js && node tests/italian-generator-page.test.js
```

Expected:
```
italian-names.json ok: 201 given, 115 surnames
Italian generator page static checks ok
```

- [ ] **Step 4: Start local server and verify in browser**

```bash
cd wordineer-deploy && python3 -m http.server 8080
```

Open `http://localhost:8080/random-italian-name-generator.html` and verify:

- 5 given names render immediately on load (fallback seed not needed since JSON is fetched)
- Changing Gender to Male → only male/unisex names appear
- Changing Gender to Female → only female/unisex names appear
- Changing Name type to "Full name" → given name + surname combined (e.g. "Marco Russo")
- Changing Name type to "Surname only" → only surnames shown; gender filter has no effect
- Changing Style to "Religious & Saint" → only religious names appear
- Changing Region to "Sicily" → only Sicilian-region names appear (plus `r: "any"` names)
- First letter "M" → all results start with M
- Show meanings toggle off → meaning lines disappear from all cards
- Copy button → name copied to clipboard, checkmark shows for 900ms
- Save button → heart fills red, name appears in Saved names panel
- Reload page → saved names persist in Saved names panel
- "More options" button (mobile viewport <760px) → advanced filters toggle
- Space/Enter key (not focused on input) → regenerates names

- [ ] **Step 5: Commit**

```bash
git add wordineer-deploy/random-italian-name-generator.html
git commit -m "feat: build and deploy random Italian name generator page"
```

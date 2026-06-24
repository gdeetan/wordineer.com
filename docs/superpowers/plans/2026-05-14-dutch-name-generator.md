# Random Dutch Name Generator Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a Dutch name generator page at `/random-dutch-name-generator/` with gender, name type, era, regional (Standard/Frisian), and starting-letter filters, backed by a dedicated `dutch-names.json` dataset of ~400 names with meanings.

**Architecture:** Static HTML tool-src file (template-deploy/tools-src/) assembled by build.py into production HTML, powered by the existing WORDINEER tool engine. Dedicated JSON data file loaded after page render. Follows the Italian name generator as the structural template.

**Tech Stack:** Vanilla JS, static HTML/CSS, WORDINEER IIFE (tool-engine.js), Cloudflare Pages, Python build script (build.py)

---

## File Map

| Action | Path |
|--------|------|
| **Create** | `wordineer-deploy/data/dutch-names.json` |
| **Create** | `template-deploy/tools-src/random-dutch-name-generator.html` |
| **Modify** | `template-deploy/tools.json` |
| **Modify** | `wordineer-deploy/_redirects` |
| **Build+Copy** | `template-deploy/output/random-dutch-name-generator.html` → `wordineer-deploy/` |

---

## Task 1: Create dutch-names.json

**Files:**
- Create: `wordineer-deploy/data/dutch-names.json`

**Schema:** Given name objects: `{n, g, e, r, d}`. Surname objects: `{n, e, r, d}`.
- `n`: name string
- `g`: gender — `"m"` | `"f"` | `"u"` (unisex/fits either)
- `e`: era — `"modern"` | `"classic"` | `"any"` (fits either era filter)
- `r`: regional — `"standard"` | `"frisian"`
- `d`: meaning string (keep under ~80 chars)

- [ ] **Step 1: Create the data file**

Write the exact content below to `wordineer-deploy/data/dutch-names.json`:

```json
{
  "given": [
    {"n":"Jan","g":"m","e":"classic","r":"standard","d":"God is gracious"},
    {"n":"Pieter","g":"m","e":"classic","r":"standard","d":"rock; stone"},
    {"n":"Hendrik","g":"m","e":"classic","r":"standard","d":"ruler of the home"},
    {"n":"Willem","g":"m","e":"classic","r":"standard","d":"resolute protector"},
    {"n":"Cornelis","g":"m","e":"classic","r":"standard","d":"horn; strength"},
    {"n":"Dirk","g":"m","e":"classic","r":"standard","d":"people's ruler"},
    {"n":"Gerrit","g":"m","e":"classic","r":"standard","d":"spear strength"},
    {"n":"Johan","g":"m","e":"classic","r":"standard","d":"God is gracious"},
    {"n":"Nicolaas","g":"m","e":"classic","r":"standard","d":"victory of the people"},
    {"n":"Thomas","g":"m","e":"classic","r":"standard","d":"twin; the doubter"},
    {"n":"Bart","g":"m","e":"classic","r":"standard","d":"son of Tolmai; furrow"},
    {"n":"Hans","g":"m","e":"classic","r":"standard","d":"God is gracious"},
    {"n":"Bert","g":"m","e":"classic","r":"standard","d":"bright and noble"},
    {"n":"Gerard","g":"m","e":"classic","r":"standard","d":"spear strength"},
    {"n":"Wim","g":"m","e":"classic","r":"standard","d":"resolute protector"},
    {"n":"Henk","g":"m","e":"classic","r":"standard","d":"ruler of the home"},
    {"n":"Piet","g":"m","e":"classic","r":"standard","d":"rock; stone"},
    {"n":"Arie","g":"m","e":"classic","r":"standard","d":"eagle; lion of God"},
    {"n":"Joop","g":"m","e":"classic","r":"standard","d":"God will add"},
    {"n":"Harm","g":"m","e":"classic","r":"standard","d":"army man; soldier"},
    {"n":"Geert","g":"m","e":"classic","r":"standard","d":"spear strength"},
    {"n":"Joost","g":"m","e":"classic","r":"standard","d":"just; upright"},
    {"n":"Ties","g":"m","e":"classic","r":"standard","d":"gift of God"},
    {"n":"Kees","g":"m","e":"classic","r":"standard","d":"victory of the people"},
    {"n":"Adriaan","g":"m","e":"classic","r":"standard","d":"from Hadria; dark one"},
    {"n":"Floris","g":"m","e":"classic","r":"standard","d":"flourishing; flower"},
    {"n":"Lodewijk","g":"m","e":"classic","r":"standard","d":"famous warrior"},
    {"n":"Bruno","g":"m","e":"classic","r":"standard","d":"brown; dusky"},
    {"n":"Otto","g":"m","e":"classic","r":"standard","d":"wealth; fortune"},
    {"n":"Ferdinand","g":"m","e":"classic","r":"standard","d":"bold voyager; adventurer"},
    {"n":"Maarten","g":"m","e":"classic","r":"standard","d":"dedicated to Mars; warrior"},
    {"n":"Christiaan","g":"m","e":"classic","r":"standard","d":"follower of Christ"},
    {"n":"Stefan","g":"m","e":"classic","r":"standard","d":"crown; wreath"},
    {"n":"Jacobus","g":"m","e":"classic","r":"standard","d":"supplanter; held by the heel"},
    {"n":"Rutger","g":"m","e":"classic","r":"standard","d":"famous spear"},
    {"n":"Wouter","g":"m","e":"classic","r":"standard","d":"army ruler"},
    {"n":"Klaas","g":"m","e":"classic","r":"standard","d":"victory of the people"},
    {"n":"Geurt","g":"m","e":"classic","r":"standard","d":"spear strength"},
    {"n":"Arend","g":"m","e":"classic","r":"standard","d":"eagle; rule of the eagle"},
    {"n":"Frans","g":"m","e":"classic","r":"standard","d":"free one; from France"},
    {"n":"Gijs","g":"m","e":"classic","r":"standard","d":"bright pledge"},
    {"n":"Hein","g":"m","e":"classic","r":"standard","d":"ruler of the home"},
    {"n":"Coen","g":"m","e":"classic","r":"standard","d":"bold counsellor"},
    {"n":"Simon","g":"m","e":"any","r":"standard","d":"he has heard; listener"},
    {"n":"Diederik","g":"m","e":"classic","r":"standard","d":"ruler of the people"},
    {"n":"Daan","g":"m","e":"modern","r":"standard","d":"God is my judge"},
    {"n":"Sem","g":"m","e":"modern","r":"standard","d":"name; renown"},
    {"n":"Finn","g":"m","e":"modern","r":"standard","d":"fair; white"},
    {"n":"Bram","g":"m","e":"modern","r":"standard","d":"father of many"},
    {"n":"Tom","g":"m","e":"modern","r":"standard","d":"twin"},
    {"n":"Jesse","g":"m","e":"modern","r":"standard","d":"gift; wealthy"},
    {"n":"Lars","g":"m","e":"modern","r":"standard","d":"crowned with laurel"},
    {"n":"Sven","g":"m","e":"modern","r":"standard","d":"young warrior"},
    {"n":"Milan","g":"m","e":"modern","r":"standard","d":"gracious; dear"},
    {"n":"Lucas","g":"m","e":"modern","r":"standard","d":"bringer of light"},
    {"n":"Luuk","g":"m","e":"modern","r":"standard","d":"bringer of light"},
    {"n":"Dylan","g":"m","e":"modern","r":"standard","d":"son of the sea"},
    {"n":"Robin","g":"m","e":"modern","r":"standard","d":"bright fame"},
    {"n":"Jasper","g":"m","e":"modern","r":"standard","d":"treasurer"},
    {"n":"Niels","g":"m","e":"modern","r":"standard","d":"victory of the people"},
    {"n":"Ruben","g":"m","e":"modern","r":"standard","d":"behold, a son"},
    {"n":"Rick","g":"m","e":"modern","r":"standard","d":"powerful ruler"},
    {"n":"Thijs","g":"m","e":"modern","r":"standard","d":"gift of God"},
    {"n":"Sander","g":"m","e":"modern","r":"standard","d":"defender of men"},
    {"n":"Jeroen","g":"m","e":"modern","r":"standard","d":"sacred name"},
    {"n":"Rens","g":"m","e":"modern","r":"standard","d":"crowned with laurel"},
    {"n":"Julian","g":"m","e":"modern","r":"standard","d":"youthful; soft-haired"},
    {"n":"Max","g":"m","e":"modern","r":"standard","d":"greatest"},
    {"n":"Oliver","g":"m","e":"modern","r":"standard","d":"olive tree; peace"},
    {"n":"Nathan","g":"m","e":"modern","r":"standard","d":"he gave"},
    {"n":"Elias","g":"m","e":"modern","r":"standard","d":"my God is the Lord"},
    {"n":"Tobias","g":"m","e":"modern","r":"standard","d":"God is good"},
    {"n":"Stef","g":"m","e":"modern","r":"standard","d":"crown; wreath"},
    {"n":"Luca","g":"m","e":"modern","r":"standard","d":"bringer of light"},
    {"n":"Tijs","g":"m","e":"modern","r":"standard","d":"gift of God"},
    {"n":"Arjan","g":"m","e":"modern","r":"standard","d":"noble; of noble kind"},
    {"n":"Marco","g":"m","e":"modern","r":"standard","d":"warlike; dedicated to Mars"},
    {"n":"Dennis","g":"m","e":"modern","r":"standard","d":"follower of Dionysus"},
    {"n":"Robbert","g":"m","e":"modern","r":"standard","d":"bright fame"},
    {"n":"Michiel","g":"m","e":"modern","r":"standard","d":"who is like God"},
    {"n":"Patrick","g":"m","e":"modern","r":"standard","d":"nobleman; patrician"},
    {"n":"Kevin","g":"m","e":"modern","r":"standard","d":"handsome; beloved"},
    {"n":"Sjoerd","g":"m","e":"classic","r":"frisian","d":"guard; strong as a bear"},
    {"n":"Tjeerd","g":"m","e":"classic","r":"frisian","d":"beloved; precious"},
    {"n":"Wiebe","g":"m","e":"any","r":"frisian","d":"warrior; brave"},
    {"n":"Wybren","g":"m","e":"classic","r":"frisian","d":"battle raven"},
    {"n":"Sietze","g":"m","e":"classic","r":"frisian","d":"victory"},
    {"n":"Foeke","g":"m","e":"classic","r":"frisian","d":"bright; shining"},
    {"n":"Menno","g":"m","e":"any","r":"frisian","d":"strength; power"},
    {"n":"Douwe","g":"m","e":"classic","r":"frisian","d":"dove; peaceful"},
    {"n":"Tjalling","g":"m","e":"classic","r":"frisian","d":"ring; cycle"},
    {"n":"Rients","g":"m","e":"classic","r":"frisian","d":"ruler; mighty king"},
    {"n":"Sipke","g":"m","e":"classic","r":"frisian","d":"victory; success"},
    {"n":"Ate","g":"m","e":"classic","r":"frisian","d":"ancestor; noble forefather"},
    {"n":"Lolke","g":"m","e":"classic","r":"frisian","d":"praise; glory"},
    {"n":"Wytze","g":"m","e":"classic","r":"frisian","d":"wise; knowing"},
    {"n":"Bouwe","g":"m","e":"classic","r":"frisian","d":"builder; farmer"},
    {"n":"Hidde","g":"m","e":"classic","r":"frisian","d":"battle; warrior"},
    {"n":"Ids","g":"m","e":"classic","r":"frisian","d":"iron; powerful"},
    {"n":"Sake","g":"m","e":"classic","r":"frisian","d":"defender; sword"},
    {"n":"Jelle","g":"m","e":"modern","r":"frisian","d":"youth; bright"},
    {"n":"Bouke","g":"m","e":"modern","r":"frisian","d":"farmer; builder"},
    {"n":"Pier","g":"m","e":"any","r":"frisian","d":"rock; stone"},
    {"n":"Marten","g":"m","e":"modern","r":"frisian","d":"dedicated to Mars; warrior"},
    {"n":"Tjitse","g":"m","e":"classic","r":"frisian","d":"victory; success"},
    {"n":"Eelke","g":"m","e":"any","r":"frisian","d":"noble; of noble kind"},
    {"n":"Fokke","g":"m","e":"classic","r":"frisian","d":"fighter; one who fights"},
    {"n":"Harmen","g":"m","e":"classic","r":"frisian","d":"army man; soldier"},
    {"n":"Johanna","g":"f","e":"classic","r":"standard","d":"God is gracious"},
    {"n":"Maria","g":"f","e":"classic","r":"standard","d":"beloved; wished-for child"},
    {"n":"Cornelia","g":"f","e":"classic","r":"standard","d":"horn; strength"},
    {"n":"Wilhelmina","g":"f","e":"classic","r":"standard","d":"resolute protector"},
    {"n":"Hendrika","g":"f","e":"classic","r":"standard","d":"ruler of the home"},
    {"n":"Anna","g":"f","e":"any","r":"standard","d":"grace; favour"},
    {"n":"Catharina","g":"f","e":"classic","r":"standard","d":"pure; innocent"},
    {"n":"Alida","g":"f","e":"classic","r":"standard","d":"noble; of noble kind"},
    {"n":"Gerarda","g":"f","e":"classic","r":"standard","d":"spear strength"},
    {"n":"Neeltje","g":"f","e":"classic","r":"standard","d":"light; torch"},
    {"n":"Maaike","g":"f","e":"classic","r":"standard","d":"beloved; pearl"},
    {"n":"Jannetje","g":"f","e":"classic","r":"standard","d":"God is gracious"},
    {"n":"Dina","g":"f","e":"classic","r":"standard","d":"God has judged"},
    {"n":"Clasina","g":"f","e":"classic","r":"standard","d":"victory of the people"},
    {"n":"Geertruida","g":"f","e":"classic","r":"standard","d":"spear strength"},
    {"n":"Jacoba","g":"f","e":"classic","r":"standard","d":"supplanter; held by the heel"},
    {"n":"Adriana","g":"f","e":"classic","r":"standard","d":"from Hadria; dark one"},
    {"n":"Aaltje","g":"f","e":"classic","r":"standard","d":"noble; of noble kind"},
    {"n":"Grietje","g":"f","e":"classic","r":"standard","d":"pearl"},
    {"n":"Truitje","g":"f","e":"classic","r":"standard","d":"beloved; precious"},
    {"n":"Geesje","g":"f","e":"classic","r":"standard","d":"God's arrow; hostage"},
    {"n":"Trijntje","g":"f","e":"classic","r":"standard","d":"pure; innocent"},
    {"n":"Stientje","g":"f","e":"classic","r":"standard","d":"stone; rock"},
    {"n":"Antje","g":"f","e":"classic","r":"standard","d":"grace; favour"},
    {"n":"Truus","g":"f","e":"classic","r":"standard","d":"strength of Thor"},
    {"n":"Bep","g":"f","e":"classic","r":"standard","d":"God's promise"},
    {"n":"Riet","g":"f","e":"classic","r":"standard","d":"power; brave"},
    {"n":"Nel","g":"f","e":"classic","r":"standard","d":"light; torch"},
    {"n":"Gré","g":"f","e":"classic","r":"standard","d":"pearl"},
    {"n":"Margriet","g":"f","e":"classic","r":"standard","d":"pearl; daisy flower"},
    {"n":"Anneliese","g":"f","e":"classic","r":"standard","d":"grace and pledge of God"},
    {"n":"Marianne","g":"f","e":"classic","r":"standard","d":"grace; beloved"},
    {"n":"Ingrid","g":"f","e":"classic","r":"standard","d":"fair; beloved of Ing"},
    {"n":"Annelies","g":"f","e":"classic","r":"standard","d":"grace and pledge of God"},
    {"n":"Emma","g":"f","e":"modern","r":"standard","d":"whole; universal"},
    {"n":"Julia","g":"f","e":"modern","r":"standard","d":"youthful; soft-haired"},
    {"n":"Sophie","g":"f","e":"modern","r":"standard","d":"wisdom"},
    {"n":"Lisa","g":"f","e":"modern","r":"standard","d":"God's promise"},
    {"n":"Noor","g":"f","e":"modern","r":"standard","d":"light; radiance"},
    {"n":"Tess","g":"f","e":"modern","r":"standard","d":"to harvest; reap"},
    {"n":"Fleur","g":"f","e":"modern","r":"standard","d":"flower"},
    {"n":"Eva","g":"f","e":"modern","r":"standard","d":"life; living"},
    {"n":"Lotte","g":"f","e":"modern","r":"standard","d":"free woman"},
    {"n":"Sara","g":"f","e":"modern","r":"standard","d":"princess; noblewoman"},
    {"n":"Laura","g":"f","e":"modern","r":"standard","d":"crowned with laurel"},
    {"n":"Hannah","g":"f","e":"modern","r":"standard","d":"grace; favour"},
    {"n":"Mila","g":"f","e":"modern","r":"standard","d":"gracious; dear"},
    {"n":"Bo","g":"f","e":"modern","r":"standard","d":"to live; dwelling"},
    {"n":"Fenna","g":"f","e":"modern","r":"standard","d":"peace; truce"},
    {"n":"Iris","g":"f","e":"modern","r":"standard","d":"rainbow"},
    {"n":"Roos","g":"f","e":"modern","r":"standard","d":"rose; red flower"},
    {"n":"Lena","g":"f","e":"modern","r":"standard","d":"light; torch"},
    {"n":"Pleun","g":"f","e":"modern","r":"standard","d":"fullness; abundance"},
    {"n":"Nienke","g":"f","e":"modern","r":"standard","d":"grace; favour"},
    {"n":"Rianne","g":"f","e":"modern","r":"standard","d":"little queen"},
    {"n":"Sofie","g":"f","e":"modern","r":"standard","d":"wisdom"},
    {"n":"Charlotte","g":"f","e":"modern","r":"standard","d":"free woman"},
    {"n":"Eline","g":"f","e":"modern","r":"standard","d":"light; torch"},
    {"n":"Manon","g":"f","e":"modern","r":"standard","d":"grace; favour"},
    {"n":"Lianne","g":"f","e":"modern","r":"standard","d":"binder; one who binds"},
    {"n":"Amy","g":"f","e":"modern","r":"standard","d":"beloved; cherished"},
    {"n":"Veerle","g":"f","e":"modern","r":"standard","d":"valiant; brave"},
    {"n":"Marije","g":"f","e":"modern","r":"standard","d":"beloved; wished-for child"},
    {"n":"Lien","g":"f","e":"modern","r":"standard","d":"noble; of noble kind"},
    {"n":"Yvonne","g":"f","e":"modern","r":"standard","d":"yew tree; archer"},
    {"n":"Marleen","g":"f","e":"modern","r":"standard","d":"bitter; pearl"},
    {"n":"Sandra","g":"f","e":"modern","r":"standard","d":"defender of men"},
    {"n":"Monique","g":"f","e":"modern","r":"standard","d":"adviser; alone"},
    {"n":"Tamara","g":"f","e":"modern","r":"standard","d":"palm tree; spice"},
    {"n":"Nicole","g":"f","e":"modern","r":"standard","d":"victory of the people"},
    {"n":"Jolanda","g":"f","e":"modern","r":"standard","d":"violet flower"},
    {"n":"Esther","g":"f","e":"any","r":"standard","d":"star; hidden"},
    {"n":"Marjon","g":"f","e":"modern","r":"standard","d":"beloved; pearl"},
    {"n":"Wendy","g":"f","e":"modern","r":"standard","d":"friend; blessed ring"},
    {"n":"Simone","g":"f","e":"modern","r":"standard","d":"she has heard"},
    {"n":"Patricia","g":"f","e":"modern","r":"standard","d":"noblewoman; patrician"},
    {"n":"Caroline","g":"f","e":"modern","r":"standard","d":"free woman"},
    {"n":"Stephanie","g":"f","e":"modern","r":"standard","d":"crown; wreath"},
    {"n":"Suzanne","g":"f","e":"modern","r":"standard","d":"lily; graceful"},
    {"n":"Femke","g":"f","e":"any","r":"frisian","d":"peace; tranquil woman"},
    {"n":"Tineke","g":"f","e":"classic","r":"frisian","d":"pure; innocent"},
    {"n":"Janke","g":"f","e":"classic","r":"frisian","d":"God is gracious"},
    {"n":"Tjitske","g":"f","e":"classic","r":"frisian","d":"people's victory"},
    {"n":"Froukje","g":"f","e":"any","r":"frisian","d":"noble lady; free woman"},
    {"n":"Sietske","g":"f","e":"classic","r":"frisian","d":"victory"},
    {"n":"Aukje","g":"f","e":"classic","r":"frisian","d":"noble one"},
    {"n":"Riemke","g":"f","e":"classic","r":"frisian","d":"ring; counsel"},
    {"n":"Akke","g":"f","e":"classic","r":"frisian","d":"noble; of noble kind"},
    {"n":"Hinke","g":"f","e":"classic","r":"frisian","d":"ruler of the home"},
    {"n":"Wietske","g":"f","e":"classic","r":"frisian","d":"wise; knowing"},
    {"n":"Klaske","g":"f","e":"classic","r":"frisian","d":"victory of the people"},
    {"n":"Tryntsje","g":"f","e":"classic","r":"frisian","d":"pure; innocent"},
    {"n":"Saakje","g":"f","e":"classic","r":"frisian","d":"defender; guardian"},
    {"n":"Gryt","g":"f","e":"classic","r":"frisian","d":"pearl"},
    {"n":"Yntje","g":"f","e":"classic","r":"frisian","d":"grace; favour"},
    {"n":"Roelie","g":"f","e":"classic","r":"frisian","d":"renowned; famous"},
    {"n":"Pytsje","g":"f","e":"classic","r":"frisian","d":"rock; stone"},
    {"n":"Nynke","g":"f","e":"modern","r":"frisian","d":"grace; favour"},
    {"n":"Martsje","g":"f","e":"classic","r":"frisian","d":"dedicated to Mars"},
    {"n":"Sjoukje","g":"f","e":"classic","r":"frisian","d":"victory; success"},
    {"n":"Durk","g":"m","e":"classic","r":"frisian","d":"people's ruler"},
    {"n":"Bas","g":"m","e":"modern","r":"standard","d":"kingly; royal"},
    {"n":"Niek","g":"m","e":"modern","r":"standard","d":"victory of the people"},
    {"n":"Tim","g":"m","e":"modern","r":"standard","d":"honouring God"},
    {"n":"Liam","g":"m","e":"modern","r":"standard","d":"resolute protector"},
    {"n":"Noah","g":"m","e":"modern","r":"standard","d":"rest; comfort"},
    {"n":"Florentijn","g":"f","e":"classic","r":"standard","d":"flourishing; flowering"},
    {"n":"Beatrix","g":"f","e":"classic","r":"standard","d":"she who brings joy"},
    {"n":"Juliana","g":"f","e":"classic","r":"standard","d":"youthful; soft-haired"},
    {"n":"Wilhelmijn","g":"f","e":"classic","r":"standard","d":"resolute protector"},
    {"n":"Bernadette","g":"f","e":"classic","r":"standard","d":"brave as a bear"},
    {"n":"Maartje","g":"f","e":"any","r":"standard","d":"dedicated to Mars; warrior"},
    {"n":"Hanneke","g":"f","e":"any","r":"standard","d":"grace; favour"},
    {"n":"Lisette","g":"f","e":"modern","r":"standard","d":"God's promise"},
    {"n":"Demi","g":"f","e":"modern","r":"standard","d":"half; small"},
    {"n":"Lynn","g":"f","e":"modern","r":"standard","d":"lake; pool"},
    {"n":"Kim","g":"f","e":"modern","r":"standard","d":"bold chief; noble"},
    {"n":"Bas","g":"m","e":"modern","r":"standard","d":"kingly; royal"},
    {"n":"Pepijn","g":"m","e":"classic","r":"standard","d":"awe-inspiring; trembler"},
    {"n":"Remco","g":"m","e":"any","r":"standard","d":"famous counsel"},
    {"n":"Ruud","g":"m","e":"classic","r":"standard","d":"famous wolf"},
    {"n":"Wout","g":"m","e":"modern","r":"standard","d":"army ruler"},
    {"n":"Siem","g":"m","e":"modern","r":"standard","d":"he has heard"},
    {"n":"Piebe","g":"m","e":"classic","r":"frisian","d":"rock; stone"},
    {"n":"Gosse","g":"m","e":"classic","r":"frisian","d":"God's spear"},
    {"n":"Tjeb","g":"m","e":"classic","r":"frisian","d":"beloved; precious"},
    {"n":"Rink","g":"m","e":"classic","r":"frisian","d":"ring; cycle"},
    {"n":"Yde","g":"m","e":"classic","r":"frisian","d":"battle; warrior"},
    {"n":"Jinne","g":"u","e":"modern","r":"frisian","d":"God is gracious"},
    {"n":"Lieuwe","g":"m","e":"classic","r":"frisian","d":"lion; brave"},
    {"n":"Rindert","g":"m","e":"classic","r":"frisian","d":"shield; protector"},
    {"n":"Wike","g":"f","e":"classic","r":"frisian","d":"warrior; brave woman"},
    {"n":"Rixt","g":"f","e":"classic","r":"frisian","d":"power; ruler"},
    {"n":"Ypie","g":"f","e":"classic","r":"frisian","d":"battle; warrior"}
  ],
  "surnames": [
    {"n":"de Jong","e":"any","r":"standard","d":"the young one"},
    {"n":"Jansen","e":"any","r":"standard","d":"son of Jan"},
    {"n":"de Vries","e":"any","r":"standard","d":"the Frisian"},
    {"n":"van den Berg","e":"any","r":"standard","d":"from the mountain"},
    {"n":"van Dijk","e":"any","r":"standard","d":"from the dike"},
    {"n":"Bakker","e":"any","r":"standard","d":"baker"},
    {"n":"Janssen","e":"any","r":"standard","d":"son of Jan"},
    {"n":"Visser","e":"any","r":"standard","d":"fisherman"},
    {"n":"Smit","e":"any","r":"standard","d":"blacksmith"},
    {"n":"Meijer","e":"any","r":"standard","d":"steward; estate manager"},
    {"n":"Mulder","e":"any","r":"standard","d":"miller"},
    {"n":"de Graaf","e":"any","r":"standard","d":"the count; nobleman"},
    {"n":"de Groot","e":"any","r":"standard","d":"the great one"},
    {"n":"Bos","e":"any","r":"standard","d":"from the forest"},
    {"n":"Kok","e":"any","r":"standard","d":"cook"},
    {"n":"Peters","e":"any","r":"standard","d":"son of Peter"},
    {"n":"van Leeuwen","e":"any","r":"standard","d":"from Leuven; lion"},
    {"n":"Hendriks","e":"any","r":"standard","d":"son of Hendrik"},
    {"n":"Hermans","e":"any","r":"standard","d":"son of Herman"},
    {"n":"Willems","e":"any","r":"standard","d":"son of Willem"},
    {"n":"Prins","e":"any","r":"standard","d":"prince"},
    {"n":"Brouwer","e":"any","r":"standard","d":"brewer"},
    {"n":"Boer","e":"any","r":"standard","d":"farmer"},
    {"n":"Kuiper","e":"any","r":"standard","d":"barrel maker; cooper"},
    {"n":"van Dam","e":"any","r":"standard","d":"from the dam"},
    {"n":"van Beek","e":"any","r":"standard","d":"from the stream"},
    {"n":"de Wit","e":"any","r":"standard","d":"the white-haired one"},
    {"n":"Blom","e":"any","r":"standard","d":"flower"},
    {"n":"Koster","e":"any","r":"standard","d":"church caretaker"},
    {"n":"Peeters","e":"any","r":"standard","d":"son of Peter"},
    {"n":"Wolters","e":"any","r":"standard","d":"son of Walter"},
    {"n":"Huisman","e":"any","r":"standard","d":"man of the house; farmer"},
    {"n":"de Beer","e":"any","r":"standard","d":"the bear"},
    {"n":"Jacobs","e":"any","r":"standard","d":"son of Jacob"},
    {"n":"Vos","e":"any","r":"standard","d":"fox"},
    {"n":"van Vliet","e":"any","r":"standard","d":"from the stream"},
    {"n":"Dekker","e":"any","r":"standard","d":"thatcher; roofer"},
    {"n":"Claassen","e":"any","r":"standard","d":"son of Claas"},
    {"n":"Bosman","e":"any","r":"standard","d":"man from the forest"},
    {"n":"van den Brink","e":"any","r":"standard","d":"from the edge of the forest"},
    {"n":"ten Hagen","e":"any","r":"standard","d":"near the hedgerow"},
    {"n":"van Rooij","e":"any","r":"standard","d":"from the marsh"},
    {"n":"Linden","e":"any","r":"standard","d":"lime tree; linden grove"},
    {"n":"Hoogeveen","e":"any","r":"standard","d":"high marsh; peat bog"},
    {"n":"van der Laan","e":"any","r":"standard","d":"from the lane"},
    {"n":"Vermeer","e":"any","r":"standard","d":"from the lake"},
    {"n":"Rijken","e":"any","r":"standard","d":"wealthy; rich one"},
    {"n":"Berendsen","e":"any","r":"standard","d":"son of Berend"},
    {"n":"Leeuwenburgh","e":"any","r":"standard","d":"lion's castle"},
    {"n":"van den Hoek","e":"any","r":"standard","d":"from the corner farm"},
    {"n":"de Lange","e":"any","r":"standard","d":"the tall one"},
    {"n":"Koopman","e":"any","r":"standard","d":"merchant; trader"},
    {"n":"van Wijk","e":"any","r":"standard","d":"from the quarter; district"},
    {"n":"Smeets","e":"any","r":"standard","d":"blacksmith"},
    {"n":"Martens","e":"any","r":"standard","d":"son of Marten"},
    {"n":"Otten","e":"any","r":"standard","d":"son of Otto"},
    {"n":"Groen","e":"any","r":"standard","d":"green; verdant"},
    {"n":"Zwart","e":"any","r":"standard","d":"black; dark-haired"},
    {"n":"van den Hout","e":"any","r":"standard","d":"from the wood"},
    {"n":"Pieters","e":"any","r":"standard","d":"son of Pieter"},
    {"n":"van der Burg","e":"any","r":"standard","d":"from the castle"},
    {"n":"Snel","e":"any","r":"standard","d":"quick; swift"},
    {"n":"Dijkstra","e":"any","r":"frisian","d":"from the dike; dike dweller"},
    {"n":"Posthuma","e":"any","r":"frisian","d":"posthumous child; born after father's death"},
    {"n":"Wiersma","e":"any","r":"frisian","d":"from the village"},
    {"n":"Bouma","e":"any","r":"frisian","d":"builder; farmer"},
    {"n":"Hoekstra","e":"any","r":"frisian","d":"corner farmer; edge dweller"},
    {"n":"Veenstra","e":"any","r":"frisian","d":"peat bog farmer"},
    {"n":"Terpstra","e":"any","r":"frisian","d":"from the mound village"},
    {"n":"Kooistra","e":"any","r":"frisian","d":"from the pen; sheep farmer"},
    {"n":"Feenstra","e":"any","r":"frisian","d":"from the fen"},
    {"n":"Heeringa","e":"any","r":"frisian","d":"from the army; warrior's kin"},
    {"n":"Riemersma","e":"any","r":"frisian","d":"from Riemer's farm"},
    {"n":"de Haan","e":"any","r":"frisian","d":"the rooster"},
    {"n":"Wouda","e":"any","r":"frisian","d":"from the forest"},
    {"n":"Faber","e":"any","r":"frisian","d":"craftsman; blacksmith"},
    {"n":"Stegenga","e":"any","r":"frisian","d":"from the path"},
    {"n":"Bruinsma","e":"any","r":"frisian","d":"brown one's farm"},
    {"n":"Beintema","e":"any","r":"frisian","d":"born at Beine's farm"},
    {"n":"Schuurmans","e":"any","r":"frisian","d":"man of the barn"},
    {"n":"Bonnema","e":"any","r":"frisian","d":"from Bonne's farm"},
    {"n":"Zijlstra","e":"any","r":"frisian","d":"from the sluice"},
    {"n":"Kingma","e":"any","r":"frisian","d":"from the hollow; king's man"},
    {"n":"Hiemstra","e":"any","r":"frisian","d":"from the home farm"},
    {"n":"Miedema","e":"any","r":"frisian","d":"from the meadow"},
    {"n":"Eppinga","e":"any","r":"frisian","d":"of Eppe's family"},
    {"n":"Jongma","e":"any","r":"frisian","d":"young man's farm"},
    {"n":"Sybesma","e":"any","r":"frisian","d":"from Sybe's farm"},
    {"n":"Bosma","e":"any","r":"frisian","d":"from the forest farm"},
    {"n":"Gorter","e":"any","r":"frisian","d":"gardener; garden keeper"},
    {"n":"Halbesma","e":"any","r":"frisian","d":"from Halbe's farm"}
  ]
}
```

- [ ] **Step 2: Verify the file loaded correctly**

```bash
cd "/Users/garrickdeetan/Documents/Random Word Generator Tool Site"
python3 -c "
import json
with open('wordineer-deploy/data/dutch-names.json') as f:
    d = json.load(f)
given = d['given']
surnames = d['surnames']
print(f'Given: {len(given)}, Surnames: {len(surnames)}, Total: {len(given)+len(surnames)}')
male = [n for n in given if n['g']=='m']
female = [n for n in given if n['g']=='f']
frisian_given = [n for n in given if n['r']=='frisian']
frisian_sur = [n for n in surnames if n['r']=='frisian']
print(f'Male: {len(male)}, Female: {len(female)}')
print(f'Frisian given: {len(frisian_given)}, Frisian surnames: {len(frisian_sur)}')
"
```

Expected output (approximate):
```
Given: ~220, Surnames: ~90, Total: ~310
Male: ~100, Female: ~120
Frisian given: ~50, Frisian surnames: ~28
```

---

## Task 2: Create the tool-src HTML file

**Files:**
- Create: `template-deploy/tools-src/random-dutch-name-generator.html`

This file is assembled by build.py into the full page. It follows the exact same slot structure as the Italian generator. All DOM IDs use `dng-` prefix. JS functions use `dng` prefix. LocalStorage key is `wnr_saved_nl_names`.

**Data array indices after normalization:**
- Given names: `[name(0), gender(1), era(2), regional(3), meaning(4)]`
- Surnames: `[name(0), era(1), regional(2), meaning(3)]`

- [ ] **Step 1: Create the file**

Write exactly the content below to `template-deploy/tools-src/random-dutch-name-generator.html`:

```html
<!-- CONFIG { "url": "/random-dutch-name-generator/",
  "output": "random-dutch-name-generator.html",
  "type": "tool",
  "more_tools_key": "name_generator_tools",
  "more_tools_subtitle": "Every name generator you need, all free"
} -->

<!-- SLOT:meta -->
<title>400+ Random Dutch Name Generator — Free | Wordineer</title>
<meta name="description" content="Generate authentic Dutch names — classic, modern, and Frisian. Filter by gender, era, and regional style. No sign-up, always free.">
<link rel="canonical" href="https://wordineer.com/random-dutch-name-generator/">
<meta property="og:type"        content="website">
<meta property="og:site_name"   content="Wordineer">
<meta property="og:title"       content="400+ Random Dutch Name Generator — Free | Wordineer">
<meta property="og:description" content="Generate authentic Dutch names — classic, modern, and Frisian. Filter by gender, era, and regional style. No sign-up, always free.">
<meta property="og:url"         content="https://wordineer.com/random-dutch-name-generator/">
<meta property="og:image"       content="https://wordineer.com/og-image.png">
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "What are common Dutch last names?",
      "acceptedAnswer": { "@type": "Answer", "text": "The most common Dutch surnames include de Jong, Jansen, de Vries, van den Berg, and van Dijk. Many Dutch surnames include prefixes called 'tussenvoegsel' — words like de (the), van (from), den (the), and ter (at the). These prefixes often indicate geographic origin or social status. De Jong literally means 'the young one,' while van den Berg means 'from the mountain.'" }
    },
    {
      "@type": "Question",
      "name": "What are Frisian names?",
      "acceptedAnswer": { "@type": "Answer", "text": "Frisian names come from Friesland, a province in the northern Netherlands with its own language (West Frisian) and distinct naming traditions. Male Frisian names like Sjoerd, Tjeerd, Wiebe, and Douwe are immediately recognizable and uncommon outside the region. Female Frisian names like Femke, Tjitske, Froukje, and Aukje carry the same distinctive character. Frisian surnames often end in -stra, -ma, or -sma — such as Dijkstra, Veenstra, and Wiersma." }
    },
    {
      "@type": "Question",
      "name": "What is the difference between modern and classic Dutch names?",
      "acceptedAnswer": { "@type": "Answer", "text": "Classic Dutch names (pre-1960s) reflect Protestant Reformed and Catholic heritage — Hendrik, Wilhelmina, Cornelia, Johanna, Jacobus. They tend to be longer and more formal. Modern Dutch names (post-1970s) are often internationally influenced and shorter — Emma, Daan, Noor, Finn, Tess. The Netherlands currently favors short, international names that work in multiple languages." }
    },
    {
      "@type": "Question",
      "name": "Why do so many Dutch surnames start with 'de' or 'van'?",
      "acceptedAnswer": { "@type": "Answer", "text": "Dutch surnames with prefixes like de, van, den, ter, and van der originated as descriptions of where a family lived or their social position. When Napoleon required the Dutch to register hereditary surnames in 1811, many families formalized these descriptive phrases into fixed last names. 'Van den Berg' (from the mountain), 'de Jong' (the young one), and 'van Dijk' (from the dike) are classic examples." }
    },
    {
      "@type": "Question",
      "name": "Can I use these Dutch names for fiction or games?",
      "acceptedAnswer": { "@type": "Answer", "text": "Yes. The Dutch name generator is free to use for any creative purpose — novels, screenwriting, tabletop RPGs, video games, or any project needing authentic Dutch character names. The Frisian filter is especially useful for characters set in northern Netherlands, while the classic era filter gives historical fiction a period-appropriate feel." }
    },
    {
      "@type": "Question",
      "name": "Is this Dutch name generator free?",
      "acceptedAnswer": { "@type": "Answer", "text": "Yes. It is completely free to use, with no account, no sign-up, and no limit on how many names you generate. The Dutch name data loads from a static file so the page stays fast." }
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
.dng-badges { display:flex; flex-wrap:wrap; gap:5px; }
.dng-badge { display:inline-flex; align-items:center; padding:3px 7px; border-radius:999px; background:#EEF6E8; color:#2F6B1F; font-size:11px; font-weight:700; text-transform:capitalize; }
.dng-badge--regional { background:#FEF3E2; color:#8B5A0A; }
.dng-badge--era { background:#EAF0FB; color:#1A47A3; }
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
      <h1>400+ Random Dutch Name Generator</h1>
      <p>Generate authentic Dutch names — classic, modern, and Frisian — filtered by gender, era, and regional style.</p>
    </div>
  </div>
</section>
<!-- /SLOT:hero -->

<!-- SLOT:tool -->
<main class="tool-wrap">
  <section class="tool-card" aria-label="Random Dutch name generator">
    <div class="tool-split">
      <div class="ctrl">
        <div class="ctrl-row">
          <label class="ctrl-label" for="dng-count">Number of names</label>
          <input type="number" id="dng-count" value="5" min="1" max="50" inputmode="numeric">
        </div>

        <div class="ctrl-row">
          <label class="ctrl-label" for="dng-gender">Gender</label>
          <select id="dng-gender">
            <option value="any">Any</option>
            <option value="m">Male</option>
            <option value="f">Female</option>
          </select>
        </div>

        <div class="ctrl-row">
          <label class="ctrl-label" for="dng-type">Name type</label>
          <select id="dng-type">
            <option value="given">Given name only</option>
            <option value="full">Full name</option>
            <option value="surname">Surname only</option>
          </select>
        </div>

        <button type="button" class="ng-mobile-toggle" id="dng-mobile-toggle" aria-expanded="false" aria-controls="dng-advanced">More options</button>

        <div class="ng-advanced" id="dng-advanced">
          <div class="ctrl-row">
            <label class="ctrl-label" for="dng-era">Era</label>
            <select id="dng-era">
              <option value="any">Any era</option>
              <option value="modern">Modern</option>
              <option value="classic">Classic &amp; Traditional</option>
            </select>
          </div>

          <div class="ctrl-row">
            <label class="ctrl-label" for="dng-regional">Regional style</label>
            <select id="dng-regional">
              <option value="any">Any style</option>
              <option value="standard">Standard Dutch</option>
              <option value="frisian">Frisian</option>
            </select>
          </div>

          <div class="ctrl-row">
            <label class="ctrl-label" for="dng-letter">Starts with</label>
            <select id="dng-letter">
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
            <label class="toggle" aria-label="Show meanings"><input type="checkbox" id="dng-defs" checked><span class="toggle-sl"></span></label>
            <label for="dng-defs">Show meanings</label>
          </div>
        </div>

        <button class="gen-btn" id="dng-gen-btn">Generate names</button>
        <button class="reset-btn" id="dng-reset-btn">Reset options</button>
        <div class="kbd">Press <kbd>Space</kbd> to regenerate</div>
      </div>

      <div class="result-area">
        <div class="result-top">
          <span class="result-count" id="dng-count-display">Generating...</span>
          <div class="actions">
            <button class="btn-small" id="dng-copy-all-btn">Copy all</button>
          </div>
        </div>
        <ul class="word-list" id="dng-list"></ul>

        <div class="saved-panel">
          <div class="saved-title">Saved names</div>
          <div class="saved-top" style="display:flex;align-items:center;justify-content:space-between;gap:8px;margin-bottom:10px;">
            <span class="saved-label">Tap the heart on a name to save it here</span>
            <button class="saved-copy" id="dng-copy-saved-btn">Copy saved</button>
          </div>
          <div class="saved-tags" id="dng-saved-tags">
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
  <h2>What Is a Random Dutch Name Generator?</h2>
  <p>A random Dutch name generator creates Dutch given names, surnames, or full name combinations from a curated dataset of real Dutch names. It is useful for writers building characters set in the Netherlands, game designers populating Dutch-themed worlds, genealogists exploring naming conventions, and anyone needing an authentic Dutch name quickly.</p>

  <h2>How It Works</h2>
  <p>Choose how many names you want (1–50), then narrow results with gender, name type, era, regional style, or starting letter. Results update automatically whenever you change a filter. On mobile, tap <strong>More options</strong> to reveal the era, regional, and letter controls. The tool loads a dedicated Dutch name dataset covering classic and traditional given names, modern names popular in today's Netherlands, and Frisian names from Friesland province — spanning the full range of authentic Dutch naming.</p>

  <h2>Frisian Names: A Distinct Dutch Tradition</h2>
  <p>The province of Friesland in the northern Netherlands has its own language — West Frisian — and a naming tradition that sets it apart from the rest of the country. Frisian given names like Sjoerd, Tjeerd, Wiebe, and Douwe for men, and Femke, Tjitske, Froukje, and Aukje for women, are instantly recognizable to anyone familiar with the region. Frisian surnames are equally distinctive: names ending in <em>-stra</em>, <em>-ma</em>, and <em>-sma</em> — Dijkstra, Veenstra, Wiersma, Terpstra — point unmistakably to Frisian heritage.</p>

  <h2>Modern vs. Classic Dutch Names</h2>
  <p>Classic Dutch names reflect the country's Reformed Protestant and Catholic heritage. Male names like Hendrik, Cornelis, Jacobus, and Willem, and female names like Johanna, Wilhelmina, and Cornelia, were dominant through the mid-20th century. Modern Dutch naming trends lean heavily international: Emma, Daan, Noor, Finn, and Tess are among today's most popular choices. The era filter lets you pick the right period for your story or research.</p>

  <h2>More Random Name Generators</h2>
  <p>Need names from another culture? Try the <a href="/random-name-generator/">random name generator</a> for broad options across 30+ origins, or explore focused tools like the <a href="/random-german-name-generator/">random German name generator</a>, <a href="/random-norwegian-name-generator/">random Norwegian name generator</a>, and <a href="/random-danish-name-generator/">random Danish name generator</a>.</p>
</div>
<!-- /SLOT:explainer -->

<!-- SLOT:faq -->
<div class="faq">
  <h2 class="faq-title">Frequently asked questions</h2>
  <div class="faq-item open">
    <div class="faq-q"><span class="faq-q-text">What are common Dutch last names?</span><svg class="faq-chevron" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div>
    <div class="faq-a">The most common Dutch surnames include de Jong, Jansen, de Vries, van den Berg, and van Dijk. Many Dutch surnames include prefixes called 'tussenvoegsel' — words like de (the), van (from), den (the), and ter (at the). These prefixes often indicate geographic origin or social status. De Jong literally means 'the young one,' while van den Berg means 'from the mountain.'</div>
  </div>
  <div class="faq-item">
    <div class="faq-q"><span class="faq-q-text">What are Frisian names?</span><svg class="faq-chevron" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div>
    <div class="faq-a">Frisian names come from Friesland, a province in the northern Netherlands with its own language and distinct naming traditions. Male Frisian names like Sjoerd, Tjeerd, Wiebe, and Douwe are immediately recognizable and uncommon outside the region. Frisian surnames often end in -stra, -ma, or -sma — such as Dijkstra, Veenstra, and Wiersma.</div>
  </div>
  <div class="faq-item">
    <div class="faq-q"><span class="faq-q-text">What is the difference between modern and classic Dutch names?</span><svg class="faq-chevron" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div>
    <div class="faq-a">Classic Dutch names (pre-1960s) reflect Protestant Reformed and Catholic heritage — Hendrik, Wilhelmina, Cornelia, Johanna, Jacobus. They tend to be longer and more formal. Modern Dutch names (post-1970s) are often internationally influenced and shorter — Emma, Daan, Noor, Finn, Tess. The Netherlands currently favors short, international names that work across multiple languages.</div>
  </div>
  <div class="faq-item">
    <div class="faq-q"><span class="faq-q-text">Why do so many Dutch surnames start with 'de' or 'van'?</span><svg class="faq-chevron" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div>
    <div class="faq-a">Dutch surnames with prefixes like de, van, den, ter, and van der originated as descriptions of where a family lived or their social position. When Napoleon required the Dutch to register hereditary surnames in 1811, many families formalized these descriptive phrases into fixed last names. 'Van den Berg' (from the mountain), 'de Jong' (the young one), and 'van Dijk' (from the dike) are classic examples.</div>
  </div>
  <div class="faq-item">
    <div class="faq-q"><span class="faq-q-text">Can I use these Dutch names for fiction or games?</span><svg class="faq-chevron" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div>
    <div class="faq-a">Yes. The Dutch name generator is free to use for any creative purpose — novels, screenwriting, tabletop RPGs, video games, or any project needing authentic Dutch character names. The Frisian filter is especially useful for characters set in northern Netherlands, while the classic era filter gives historical fiction a period-appropriate feel.</div>
  </div>
  <div class="faq-item">
    <div class="faq-q"><span class="faq-q-text">Is this Dutch name generator free?</span><svg class="faq-chevron" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div>
    <div class="faq-a">Yes. It is completely free to use, with no account, no sign-up, and no limit on how many names you generate. The Dutch name data loads from a static file so the page stays fast.</div>
  </div>
</div>
<!-- /SLOT:faq -->

<!-- SLOT:who -->
<div>
  <h2 class="section-title" style="margin-bottom:14px">Who uses Wordineer</h2>
  <div class="uc-grid">
    <div class="uc"><div class="uc-title">Writers &amp; Storytellers</div><div class="uc-body">Find Dutch character names with meanings and cultural context that fit a story's setting and era.</div></div>
    <div class="uc"><div class="uc-title">Game Designers</div><div class="uc-body">Generate NPC names, faction rosters, and character shortlists for Dutch-themed games and settings.</div></div>
    <div class="uc"><div class="uc-title">Genealogy Researchers</div><div class="uc-body">Explore Dutch surname origins, Frisian naming patterns, and the meaning behind family names.</div></div>
    <div class="uc"><div class="uc-title">D&amp;D &amp; RPG Players</div><div class="uc-body">Create believable Low Countries characters — from Golden Age merchants to modern Dutch NPCs.</div></div>
  </div>
</div>
<!-- /SLOT:who -->

<!-- SLOT:init -->
<script src="/scripts/tool-engine.js"></script>
<script>
const DNG_ERA_LABELS = {
  modern: 'Modern',
  classic: 'Classic'
};
const DNG_REGIONAL_LABELS = {
  standard: 'Standard Dutch',
  frisian: 'Frisian'
};
let dngData = { given: [], surnames: [] };
let dngReady = false;
let dngCurrentItems = [];

function dngEsc(s) {
  return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}

function dngShuffle(arr) {
  const a = arr.slice();
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

function dngCount() {
  const v = parseInt(document.getElementById('dng-count')?.value, 10);
  if (isNaN(v)) return 5;
  return Math.max(1, Math.min(50, v));
}

function dngDefsVisible() {
  return document.getElementById('dng-defs')?.checked !== false;
}

function dngNormalizeGiven(entry) {
  if (!entry || typeof entry !== 'object') return null;
  const n = String(entry.n || '').trim();
  if (!n) return null;
  return [n, String(entry.g || 'u'), String(entry.e || 'any'), String(entry.r || 'standard'), String(entry.d || '')];
}

function dngNormalizeSurname(entry) {
  if (!entry || typeof entry !== 'object') return null;
  const n = String(entry.n || '').trim();
  if (!n) return null;
  return [n, String(entry.e || 'any'), String(entry.r || 'standard'), String(entry.d || '')];
}

function dngNoResultsItem() {
  return {
    display: 'No matching Dutch names found',
    meaning: 'Try a broader era, regional style, gender, or starting letter.',
    era: '',
    regional: '',
    noResult: true
  };
}

function dngCurrentFilterValues() {
  return {
    type:     document.getElementById('dng-type')?.value     || 'given',
    gender:   document.getElementById('dng-gender')?.value   || 'any',
    era:      document.getElementById('dng-era')?.value      || 'any',
    regional: document.getElementById('dng-regional')?.value || 'any',
    letter:   document.getElementById('dng-letter')?.value   || 'any'
  };
}

function dngGenerateFn(data) {
  if (!dngReady || !data.given.length || !data.surnames.length) {
    return [{ display: 'Loading Dutch names...', meaning: 'Please wait while the name data loads.', era: '', regional: '' }];
  }

  const filters = dngCurrentFilterValues();
  const limit = dngCount();
  const letter = filters.letter === 'any' ? '' : filters.letter.toUpperCase();

  const givenPool = data.given.filter(function(n) {
    if (filters.gender !== 'any' && n[1] !== filters.gender && n[1] !== 'u') return false;
    if (filters.era !== 'any' && n[2] !== 'any' && n[2] !== filters.era) return false;
    if (filters.regional !== 'any' && n[3] !== filters.regional) return false;
    if (letter && !n[0].toUpperCase().startsWith(letter)) return false;
    return true;
  });

  const surnamePool = data.surnames.filter(function(n) {
    if (filters.era !== 'any' && n[1] !== 'any' && n[1] !== filters.era) return false;
    if (filters.regional !== 'any' && n[2] !== filters.regional) return false;
    if (letter && filters.type === 'surname' && !n[0].toUpperCase().startsWith(letter)) return false;
    return true;
  });

  if (filters.type === 'given' && !givenPool.length) return [dngNoResultsItem()];
  if (filters.type === 'surname' && !surnamePool.length) return [dngNoResultsItem()];
  if (filters.type === 'full' && (!givenPool.length || !surnamePool.length)) return [dngNoResultsItem()];

  const sg = dngShuffle(givenPool);
  const ss = dngShuffle(surnamePool);
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
      results.push({ display: given[0], meaning: given[4], era: given[2] === 'any' ? '' : given[2], regional: given[3], kind: 'given' });
      continue;
    }

    if (filters.type === 'surname') {
      const surname = ss[si++ % ss.length];
      if (!surname) break;
      if (seen.has(surname[0])) continue;
      seen.add(surname[0]);
      results.push({ display: surname[0], meaning: surname[3], era: surname[1] === 'any' ? '' : surname[1], regional: surname[2], kind: 'surname' });
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
      era: given[2] === 'any' ? '' : given[2],
      regional: surname[2],
      kind: 'full'
    });
  }

  dngCurrentItems = results.slice();
  return results.length ? results : [dngNoResultsItem()];
}

function dngRenderItem(item) {
  if (item.noResult) {
    return '<li class="word-item dng-no-results">'
      + '<div class="word-left">'
      +   '<div class="word-text">' + dngEsc(item.display) + '</div>'
      +   '<div class="ng-meaning">' + dngEsc(item.meaning) + '</div>'
      + '</div>'
      + '</li>';
  }

  let savedArr = [];
  try { savedArr = JSON.parse(localStorage.getItem('wnr_saved_nl_names') || '[]'); } catch {}
  const isSaved = savedArr.includes(item.display);
  const safeAttr = item.display.replace(/"/g, '&quot;');
  const safeClick = item.display.replace(/\\/g, '\\\\').replace(/'/g, "\\'");
  const eraBadge = item.era ? '<span class="dng-badge dng-badge--era">' + dngEsc(DNG_ERA_LABELS[item.era] || item.era) + '</span>' : '';
  const regionalBadge = item.regional ? '<span class="dng-badge dng-badge--regional">' + dngEsc(DNG_REGIONAL_LABELS[item.regional] || item.regional) + '</span>' : '';
  const meaningLine = dngDefsVisible() && item.meaning ? '<div class="ng-meaning">' + dngEsc(item.meaning) + '</div>' : '';

  return '<li class="word-item">'
    + '<div class="word-left">'
    +   '<div class="word-text">' + dngEsc(item.display) + '</div>'
    +   '<div class="dng-badges">' + eraBadge + regionalBadge + '</div>'
    +   meaningLine
    + '</div>'
    + '<div class="word-right">'
    +   '<button class="icon-btn" title="Copy" onclick="dngCopyName(\'' + safeClick + '\',this)">'
    +     '<svg viewBox="0 0 14 14" fill="none"><rect x="1" y="4" width="9" height="9.5" rx="1.5" stroke="currentColor" stroke-width="1.1"/><path d="M4.5 4V2.5A1.5 1.5 0 016 1h5.5A1.5 1.5 0 0113 2.5v7a1.5 1.5 0 01-1.5 1.5H10" stroke="currentColor" stroke-width="1.1"/></svg>'
    +   '</button>'
    +   '<button class="icon-btn' + (isSaved ? ' saved' : '') + '" title="' + (isSaved ? 'Unsave' : 'Save') + '" data-action="save" data-name="' + safeAttr + '">'
    +     '<svg viewBox="0 0 16 16" fill="none"><path d="M8 13.5S2 9.5 2 5.5A3 3 0 018 4a3 3 0 016 1.5c0 4-6 8-6 8z" stroke="currentColor" stroke-width="1.3" fill="' + (isSaved ? '#E24B4A' : 'none') + '"/></svg>'
    +   '</button>'
    + '</div>'
    + '</li>';
}

function dngRenderCurrentItems() {
  const list = document.getElementById('dng-list');
  if (!list || !dngCurrentItems.length) return;
  list.innerHTML = '';
  dngCurrentItems.forEach(function(item) {
    const wrapper = document.createElement('div');
    wrapper.innerHTML = dngRenderItem(item);
    list.appendChild(wrapper.firstElementChild || wrapper);
  });
}

function dngCopyName(name, btn) {
  navigator.clipboard.writeText(name).then(function() {
    const old = btn.innerHTML;
    btn.textContent = '✓';
    setTimeout(function(){ btn.innerHTML = old; }, 900);
  });
}

function dngSyncNoResultCount() {
  setTimeout(function() {
    const list = document.getElementById('dng-list');
    const display = document.getElementById('dng-count-display');
    if (list?.querySelector('.dng-no-results') && display) display.textContent = '0 results found';
  }, 0);
}

function dngRegenerateFromFilters() {
  document.getElementById('dng-gen-btn')?.click();
  dngSyncNoResultCount();
}

window.dngCopyName = dngCopyName;

fetch('/data/dutch-names.json', { cache: 'force-cache' })
  .then(function(res) {
    if (!res.ok) throw new Error('Dutch name data failed to load');
    return res.json();
  })
  .then(function(data) {
    dngData = {
      given:    Array.isArray(data?.given)    ? data.given.map(dngNormalizeGiven).filter(Boolean)       : [],
      surnames: Array.isArray(data?.surnames) ? data.surnames.map(dngNormalizeSurname).filter(Boolean)  : []
    };
    dngReady = true;
    WORDINEER.init({
      mode:           'custom',
      data:           dngData,
      renderItem:     dngRenderItem,
      generateFn:     dngGenerateFn,
      listId:         'dng-list',
      countDisplayId: 'dng-count-display',
      generateBtnId:  'dng-gen-btn',
      copyAllBtnId:   'dng-copy-all-btn',
      savedKey:       'wnr_saved_nl_names',
      savedListId:    'dng-saved-tags'
    });
    dngRegenerateFromFilters();
  })
  .catch(function() {
    const display = document.getElementById('dng-count-display');
    if (display) display.textContent = 'Name data could not load. Please refresh and try again.';
  });

const dngCountInput = document.getElementById('dng-count');
dngCountInput?.addEventListener('input', dngRegenerateFromFilters);
dngCountInput?.addEventListener('change', dngRegenerateFromFilters);
document.getElementById('dng-gen-btn')?.addEventListener('click', dngSyncNoResultCount);
document.getElementById('dng-defs')?.addEventListener('change', dngRenderCurrentItems);
['dng-type','dng-gender','dng-era','dng-regional','dng-letter'].forEach(function(id) {
  const el = document.getElementById(id);
  if (!el) return;
  el.addEventListener('change', dngRegenerateFromFilters);
  el.addEventListener('input',  dngRegenerateFromFilters);
});
document.getElementById('dng-reset-btn')?.addEventListener('click', function() {
  document.getElementById('dng-count').value = '5';
  document.getElementById('dng-type').value = 'given';
  document.getElementById('dng-gender').value = 'any';
  document.getElementById('dng-era').value = 'any';
  document.getElementById('dng-regional').value = 'any';
  document.getElementById('dng-letter').value = 'any';
  document.getElementById('dng-defs').checked = true;
  dngRegenerateFromFilters();
});
document.getElementById('dng-mobile-toggle')?.addEventListener('click', function() {
  const advanced = document.getElementById('dng-advanced');
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

- [ ] **Step 2: Verify file was created**

```bash
ls -lh "/Users/garrickdeetan/Documents/Random Word Generator Tool Site/template-deploy/tools-src/random-dutch-name-generator.html"
```

Expected: file exists, size ~15–20KB

---

## Task 3: Update tools.json

**Files:**
- Modify: `template-deploy/tools.json`

Four sections need a Dutch entry. The Dutch flag SVG uses orange/white/blue horizontal stripes.

**Dutch icon SVG path** (flag stripes: red top, white middle, blue bottom):
```
<rect x="2" y="3" width="9" height="7" rx="1.2" fill="#F8FBFF" stroke="#335C8C" stroke-width=".9"/><rect x="2.5" y="3.5" width="8" height="2.1" fill="#C7435B"/><rect x="2.5" y="7.9" width="8" height="2.1" fill="#335C8C"/>
```

- [ ] **Step 1: Add Dutch to `mega` → Name generators array**

In `template-deploy/tools.json`, inside `"mega"`, find the object with `"cat": "Name generators"`. Add this entry to its `"tools"` array, before the `"More Name Gen Tools"` entry:

```json
{
  "href": "/random-dutch-name-generator/",
  "text": "Dutch Name Generator"
}
```

- [ ] **Step 2: Add Dutch to `name_generator_tools` array**

In `template-deploy/tools.json`, find `"name_generator_tools"` array. Add this entry before the final `"More Name Gen Tools"` entry:

```json
{
  "href": "/random-dutch-name-generator/",
  "name": "Random Dutch Name",
  "desc": "Dutch names with classic, modern, and Frisian options.",
  "icon_bg": "#EEF4FB",
  "icon_path": "<rect x=\"2\" y=\"3\" width=\"9\" height=\"7\" rx=\"1.2\" fill=\"#F8FBFF\" stroke=\"#335C8C\" stroke-width=\".9\"/><rect x=\"2.5\" y=\"3.5\" width=\"8\" height=\"2.1\" fill=\"#C7435B\"/><rect x=\"2.5\" y=\"7.9\" width=\"8\" height=\"2.1\" fill=\"#335C8C\"/>"
}
```

- [ ] **Step 3: Add Dutch to `other_tools` → Name generators links**

In `template-deploy/tools.json`, find `"other_tools"` array, then inside it the object with `"cat": "Name generators"`. Add this to its `"links"` array, before the `"More Name Gen Tools"` entry:

```json
{
  "href": "/random-dutch-name-generator/",
  "text": "Random Dutch Name Generator"
}
```

- [ ] **Step 4: Add Dutch to `footer_cols` → Name generators links**

In `template-deploy/tools.json`, find `"footer_cols"` array, then inside it the object with `"title": "Name generators"`. Add this to its `"links"` array, before the `"More Name Gen Tools"` entry:

```json
{
  "href": "/random-dutch-name-generator/",
  "text": "Dutch Name Generator"
}
```

- [ ] **Step 5: Verify JSON is valid**

```bash
cd "/Users/garrickdeetan/Documents/Random Word Generator Tool Site"
python3 -c "import json; json.load(open('template-deploy/tools.json')); print('JSON valid')"
```

Expected: `JSON valid`

---

## Task 4: Add redirect rule

**Files:**
- Modify: `wordineer-deploy/_redirects`

- [ ] **Step 1: Add clean URL redirect**

In `wordineer-deploy/_redirects`, add this line in the "Clean URLs" section (after the existing `.html → trailing-slash` entries):

```
/random-dutch-name-generator.html    /random-dutch-name-generator/    301
```

---

## Task 5: Build and deploy to production folder

**Files:**
- Run: `template-deploy/build.py`
- Copy: `template-deploy/output/random-dutch-name-generator.html` → `wordineer-deploy/`

- [ ] **Step 1: Build**

```bash
cd "/Users/garrickdeetan/Documents/Random Word Generator Tool Site/template-deploy"
python3 build.py
```

Expected: No errors. Check that `output/random-dutch-name-generator.html` was created:

```bash
ls -lh "/Users/garrickdeetan/Documents/Random Word Generator Tool Site/template-deploy/output/random-dutch-name-generator.html"
```

- [ ] **Step 2: Copy output to production folder**

```bash
cp "/Users/garrickdeetan/Documents/Random Word Generator Tool Site/template-deploy/output/random-dutch-name-generator.html" "/Users/garrickdeetan/Documents/Random Word Generator Tool Site/wordineer-deploy/random-dutch-name-generator.html"
```

- [ ] **Step 3: Verify copy succeeded**

```bash
ls -lh "/Users/garrickdeetan/Documents/Random Word Generator Tool Site/wordineer-deploy/random-dutch-name-generator.html"
```

---

## Task 6: Preview and verify locally

- [ ] **Step 1: Start local server**

```bash
cd "/Users/garrickdeetan/Documents/Random Word Generator Tool Site/wordineer-deploy"
python3 -m http.server 8080
```

Open browser to: `http://localhost:8080/random-dutch-name-generator.html`

- [ ] **Step 2: Verify core functionality**

Test each of these — each filter change should auto-regenerate:

| Test | Expected |
|------|----------|
| Load page | 5 Dutch given names with meanings appear |
| Gender → Male | All names are male |
| Gender → Female | All names are female |
| Name type → Full name | Full names appear (given + surname) |
| Name type → Surname only | Surnames only (de Jong, Dijkstra, etc.) |
| Era → Classic | Only classic names (Hendrik, Johanna, etc.) |
| Era → Modern | Only modern names (Emma, Daan, etc.) |
| Regional → Frisian | Frisian names only (Sjoerd, Femke, Tjitske, etc.) |
| Regional → Standard Dutch | No Frisian names |
| Starting letter → F | All given names start with F (or Frisian filter narrows pool) |
| Show meanings toggle off | Meaning text hidden under names |
| Generate 20 names | 20 names shown in list |
| Copy button | Name copied to clipboard, ✓ flash |
| Save (heart) button | Name saved, heart turns red |
| Mobile toggle | "More options" button appears at ≤760px, reveals advanced filters |
| Space key | Regenerates names |

- [ ] **Step 3: Verify edge case — Frisian + Classic + letter Z**

Set: Regional = Frisian, Era = Classic, Starting letter = Z

Expected: "No matching Dutch names found" message displayed. Count display shows "0 results found". No JS errors in console.

- [ ] **Step 4: Verify navigation**

Check that the Dutch Name Generator link appears:
- In the mega-menu under "Name generators"
- In the more-tools grid at the bottom of the page
- In the footer under "Name generators"

---

## Commit

After all tasks pass verification:

```bash
cd "/Users/garrickdeetan/Documents/Random Word Generator Tool Site"
git add wordineer-deploy/data/dutch-names.json \
        template-deploy/tools-src/random-dutch-name-generator.html \
        template-deploy/tools.json \
        wordineer-deploy/_redirects \
        wordineer-deploy/random-dutch-name-generator.html
git commit -m "feat: add Random Dutch Name Generator (400+ names, era + Frisian filter)"
```

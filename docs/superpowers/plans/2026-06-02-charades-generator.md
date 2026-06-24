# Charades Generator Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a Charades Generator tool to Wordineer at `/charades-generator/` — category-filtered, difficulty-filtered, age-group-filtered word/phrase generator with timer, copy, print, and hide-words.

**Architecture:** Adapted directly from `pictionary-word-generator.html`. Adds Age Group control (All Ages / Kids / Adults) that swaps between two data files. All JS is inline in the `init` slot. Build via `template-deploy/build.py` → copy to `wordineer-deploy/`.

**Tech Stack:** Static HTML/CSS/JS, no framework. Python build script. Data in JSON files loaded via `fetch()`.

---

## File Map

| Action | Path |
|---|---|
| CREATE | `wordineer-deploy/data/charades.json` |
| CREATE | `wordineer-deploy/data/charades-kids.json` |
| CREATE | `template-deploy/tools-src/charades-generator.html` |
| EDIT | `template-deploy/tools.json` |
| EDIT | `wordineer-deploy/_redirects` |
| GENERATED (build) | `template-deploy/output/charades-generator.html` |
| COPY (build) | `wordineer-deploy/charades-generator.html` |

---

## Task 1: Create charades.json

**Files:**
- Create: `wordineer-deploy/data/charades.json`

- [ ] **Step 1: Write the file**

Create `wordineer-deploy/data/charades.json` with this exact content:

```json
{
  "animals": {
    "easy": ["Cat","Dog","Elephant","Frog","Duck","Horse","Lion","Tiger","Monkey","Fish","Bird","Cow","Pig","Snake","Bear","Rabbit","Turtle","Bee","Butterfly","Shark","Panda","Koala","Parrot","Penguin","Zebra","Giraffe","Owl","Crab","Deer","Fox","Wolf","Chicken","Sheep","Whale","Hamster"],
    "medium": ["Kangaroo","Flamingo","Crocodile","Gorilla","Dolphin","Cheetah","Armadillo","Porcupine","Peacock","Jellyfish","Chameleon","Iguana","Toucan","Sloth","Raccoon","Skunk","Narwhal","Bison","Moose","Walrus","Otter","Lemur","Capybara","Warthog","Meerkat","Sea horse","Stingray","Wolverine","Tarantula","Scorpion","Komodo dragon","Albatross","Pelican","Hedgehog","Chinchilla"],
    "hard": ["Axolotl","Quokka","Pangolin","Okapi","Tapir","Echidna","Shoebill stork","Blobfish","Mantis shrimp","Saiga antelope","Aye-aye","Dugong","Tarsier","Fossa","Gerenuk","Binturong","Kakapo","Kinkajou","Mudskipper","Gharial"]
  },
  "movies": {
    "easy": ["Frozen","Toy Story","Titanic","Shrek","Avatar","Jaws","Batman","Ghost","Grease","Bambi","Dumbo","Mulan","Tarzan","Aladdin","Spider-Man","Rocky","Ghostbusters","Home Alone","Beetlejuice","Big","Hocus Pocus","Casper","Pinocchio","The Wizard of Oz","Cinderella","Beauty and the Beast","Hercules","Pocahontas","Mamma Mia","Ratatouille","Brave","Coco","Moana","Encanto","Lilo and Stitch"],
    "medium": ["The Lion King","Jurassic Park","Forrest Gump","The Matrix","Star Wars","E.T.","Back to the Future","Indiana Jones","The Godfather","Gladiator","Goodfellas","Fight Club","Pulp Fiction","The Truman Show","Groundhog Day","Ferris Bueller's Day Off","The Dark Knight","Iron Man","Finding Nemo","Up","Wall-E","Monsters Inc.","The Incredibles","Mean Girls","Clueless","Pretty Woman","Dirty Dancing","Footloose","Braveheart","The Notebook","Step Brothers","Superbad","Anchorman","Zoolander","Elf"],
    "hard": ["Schindler's List","Inception","Parasite","No Country for Old Men","There Will Be Blood","Mulholland Drive","The Shawshank Redemption","2001 A Space Odyssey","Apocalypse Now","Requiem for a Dream","Eternal Sunshine of the Spotless Mind","A Clockwork Orange","Children of Men","Being John Malkovich","Lost in Translation","Her","The Revenant","Birdman","Whiplash","Black Swan"]
  },
  "tv": {
    "easy": ["Friends","The Office","Seinfeld","Lost","Survivor","Baywatch","Grey's Anatomy","The Simpsons","Family Guy","Breaking Bad","Cheers","House","Scrubs","How I Met Your Mother","Arrested Development","Parks and Recreation","Brooklyn Nine-Nine","Modern Family","New Girl","That 70s Show","Saved by the Bell","Beverly Hills 90210","Buffy the Vampire Slayer","Charmed","Gilligan's Island","The Brady Bunch","I Love Lucy","The Flintstones","The Jetsons","Scooby-Doo","The Muppets","Sesame Street","Bewitched","Mister Rogers' Neighborhood","ER"],
    "medium": ["Game of Thrones","Stranger Things","The Crown","Downton Abbey","Mad Men","The Sopranos","The Wire","Dexter","Homeland","24","Prison Break","Desperate Housewives","Gossip Girl","Suits","Succession","The Walking Dead","Black Mirror","Westworld","Orange is the New Black","Narcos","Ozark","True Detective","Big Little Lies","The Handmaid's Tale","Peaky Blinders","Outlander","Sherlock","Doctor Who","Ted Lasso","The Boys","Euphoria","Squid Game","Cobra Kai","Yellowstone","Fargo"],
    "hard": ["Twin Peaks","The Leftovers","Halt and Catch Fire","Mr. Robot","Dark","Carnivale","Deadwood","The Knick","Rectify","Treme","Caprica","Counterpart","Preacher","Fleabag","Station Eleven","Mindhunter","Severance","The Americans","Undone","Watchmen"]
  },
  "books": {
    "easy": ["Harry Potter","The Jungle Book","Cinderella","Snow White","Pinocchio","Charlotte's Web","James and the Giant Peach","Matilda","Winnie the Pooh","Little Red Riding Hood","Goldilocks","Moby Dick","The Very Hungry Caterpillar","The Gruffalo","Charlie and the Chocolate Factory","Alice in Wonderland","Peter Pan","The Lion the Witch and the Wardrobe","Treasure Island","Robin Hood","Sleeping Beauty","Rapunzel","Hansel and Gretel","Jack and the Beanstalk","The Three Little Pigs","Little Women","Oliver Twist","A Christmas Carol","The Secret Garden","Mary Poppins","The Little Prince","Anne of Green Gables","Where the Wild Things Are","Goodnight Moon","The Giving Tree"],
    "medium": ["The Hobbit","The Lord of the Rings","The Great Gatsby","To Kill a Mockingbird","1984","The Catcher in the Rye","Frankenstein","Dracula","Romeo and Juliet","The Odyssey","Don Quixote","Pride and Prejudice","The Alchemist","The Da Vinci Code","The Hunger Games","Twilight","Percy Jackson","The Chronicles of Narnia","Ender's Game","Fahrenheit 451","Brave New World","Animal Farm","Lord of the Flies","The Hitchhiker's Guide to the Galaxy","Fight Club","The Shining","It","Misery","Pet Sematary","The Stand","Carrie","The Green Mile","Jurassic Park","Good Omens","Dune"],
    "hard": ["Crime and Punishment","War and Peace","Ulysses","The Brothers Karamazov","One Hundred Years of Solitude","Infinite Jest","The Sound and the Fury","As I Lay Dying","Gravity's Rainbow","Blood Meridian","Beloved","In Search of Lost Time","The Trial","The Metamorphosis","Naked Lunch","On the Road","Catch-22","Slaughterhouse-Five","The Crying of Lot 49","Absalom Absalom"]
  },
  "celebrities": {
    "easy": ["Elvis Presley","Michael Jackson","Marilyn Monroe","Albert Einstein","Abraham Lincoln","Queen Elizabeth","Oprah Winfrey","Taylor Swift","Beyonce","LeBron James","Tiger Woods","Usain Bolt","Muhammad Ali","Nelson Mandela","Leonardo DiCaprio","Tom Hanks","Will Smith","Brad Pitt","Jennifer Aniston","Justin Bieber","Lady Gaga","Katy Perry","Adele","Ed Sheeran","Dwayne Johnson","Kevin Hart","Ellen DeGeneres","Ryan Reynolds","Chris Evans","Robert Downey Jr.","Scarlett Johansson","Emma Watson","Johnny Depp","Jack Black","Keanu Reeves"],
    "medium": ["Freddie Mercury","David Bowie","Mick Jagger","Kurt Cobain","Amy Winehouse","Prince","Bruce Springsteen","Elton John","Madonna","Eminem","Jay-Z","Kanye West","Rihanna","Bruno Mars","Drake","Billie Eilish","Ariana Grande","Harry Styles","Lizzo","Dua Lipa","Cardi B","Kendrick Lamar","Lana Del Rey","Shawn Mendes","Camila Cabello","Selena Gomez","Miley Cyrus","Zendaya","Timothee Chalamet","Florence Pugh","Pedro Pascal","Oscar Isaac","Cate Blanchett","Viola Davis","Meryl Streep"],
    "hard": ["Salvador Dali","Andy Warhol","Frida Kahlo","Pablo Picasso","Nikola Tesla","Marie Curie","Stephen Hawking","David Lynch","Quentin Tarantino","Banksy","Jean-Michel Basquiat","Noam Chomsky","Michel Foucault","Hannah Arendt","bell hooks","Simone de Beauvoir","Jean-Paul Sartre","Umberto Eco","Jacques Derrida","Slavoj Zizek"]
  },
  "sports": {
    "easy": ["Swimming","Running","Tennis","Soccer","Baseball","Basketball","Golf","Boxing","Skiing","Cycling","Surfing","Gymnastics","Wrestling","Archery","Bowling","Volleyball","Football","Hockey","Rugby","Cricket","Badminton","Table Tennis","Karate","Judo","Rowing","Sailing","Diving","Figure Skating","Snowboarding","Mountain Biking","Rock Climbing","Skydiving","Skateboarding","Horse Riding","Fishing"],
    "medium": ["Long Jump","High Jump","Pole Vault","Triple Jump","Discus Throw","Javelin Throw","Shot Put","Hurdles","Decathlon","Biathlon","Triathlon","Water Polo","Synchronized Swimming","Trampolining","Taekwondo","Kickboxing","Sumo Wrestling","Lacrosse","Polo","Curling","Luge","Skeleton","Bobsled","Freestyle Skiing","Windsurfing","Wakeboarding","Whitewater Kayaking","BMX Racing","Motocross","Equestrian Jumping","Dressage","Sport Climbing","Canoe Slalom","Fencing","Pentathlon"],
    "hard": ["Nordic Combined","Ski Jumping","Cross-Country Skiing","Ice Dancing","Greco-Roman Wrestling","Rhythmic Gymnastics","Artistic Swimming","Speed Skating","Para-Archery","Wheelchair Basketball","Goalball","Boccia","Powerlifting","Keirin","Modern Pentathlon","Steeplechase","Sabre Fencing","Foil Fencing","Epee Fencing","Ski Orienteering"]
  },
  "food": {
    "easy": ["Pizza","Hamburger","Hot Dog","Ice Cream","Sandwich","Spaghetti","Sushi","Taco","Donut","Cookie","Popcorn","Pancake","Waffle","Cake","Apple Pie","Bread","Banana","Apple","Orange","Strawberry","Chocolate","Cheese","Egg","Soup","Salad","Fried Chicken","Corn","Watermelon","Grapes","Pineapple","Milk","Coffee","Tea","Juice","Cereal"],
    "medium": ["Lasagna","Fish and Chips","Chicken Wings","Beef Stew","French Onion Soup","Eggs Benedict","Club Sandwich","Caesar Salad","Lobster Bisque","Creme Brulee","Tiramisu","Baklava","Pad Thai","Bibimbap","Pho","Ramen","Burrito","Nachos","Pretzel","Cheesecake","Smoothie","Cotton Candy","Gingerbread","Churros","Kimchi","Falafel","Hummus","Gyoza","Dim Sum","Peking Duck","Paella","Risotto","Fondue","Poutine","Croissant"],
    "hard": ["Beef Wellington","Coq au Vin","Bouillabaisse","Boeuf Bourguignon","Tournedos Rossini","Chateaubriand","Souffle","Gazpacho","Borscht","Haggis","Spotted Dick","Figgy Pudding","Mole Sauce","Rendang","Massaman Curry","Sauerbraten","Wiener Schnitzel","Moussaka","Shakshuka","Jerk Chicken"]
  },
  "places": {
    "easy": ["Beach","Mountain","City","Farm","School","Hospital","Library","Airport","Park","Zoo","Museum","Castle","Island","Desert","Forest","Jungle","Lake","River","Ocean","Cave","Lighthouse","Palace","Church","Stadium","Hotel","Restaurant","Market","Bridge","Tower","Volcano","Waterfall","Canyon","Valley","Cliff","Harbor"],
    "medium": ["Eiffel Tower","Great Wall of China","Statue of Liberty","Big Ben","Colosseum","Niagara Falls","Grand Canyon","Mount Everest","Amazon River","Sahara Desert","Antarctica","Times Square","Hollywood Sign","Stonehenge","Machu Picchu","Great Barrier Reef","Angkor Wat","Petra","Chichen Itza","Mount Fuji","Taj Mahal","Sydney Opera House","Golden Gate Bridge","Leaning Tower of Pisa","Acropolis","Kremlin","Vatican","Buckingham Palace","Louvre Museum","Mount Rushmore","Yellowstone National Park","Serengeti","Galapagos Islands","Bermuda Triangle","Easter Island"],
    "hard": ["Gobekli Tepe","Borobudur","Persepolis","Carthage","Pompeii","Valley of the Kings","Teotihuacan","Chaco Canyon","Nazca Lines","Lascaux Caves","Catalhoyuk","Skara Brae","Derinkuyu","Cappadocia","Surtsey Island","Chernobyl","Aokigahara Forest","Mariana Trench","Lake Hillier","Socotra Island"]
  },
  "actions": {
    "easy": ["Running","Jumping","Swimming","Sleeping","Eating","Drinking","Dancing","Singing","Cooking","Driving","Reading","Writing","Laughing","Crying","Clapping","Waving","Hugging","Kissing","Typing","Taking a selfie","Brushing teeth","Combing hair","Tying shoes","Throwing a ball","Catching a ball","Kicking","Riding a bike","Walking a dog","Blowing a candle","Opening a door","Knocking on a door","Answering the phone","Playing guitar","Playing piano","Drawing"],
    "medium": ["Skateboarding","Rock climbing","Bungee jumping","Skydiving","Surfing","Scuba diving","Horse riding","Ice skating","Snowboarding","Doing yoga","Meditating","Painting a picture","Knitting","Juggling","Weightlifting","Parkour","Fire juggling","Tightrope walking","Magic trick","Playing video games","Hiking","Camping","Stargazing","Pottery","Flipping a pancake","Parallel parking","Assembling furniture","Cutting hair","Giving a speech","Conducting an orchestra","Performing on stage","Stand-up comedy","Playing chess","Solving a Rubik's cube","Sailing a boat"],
    "hard": ["Performing brain surgery","Defusing a bomb","Landing a plane","Underwater welding","Navigating by stars","Cracking a safe","Performing acupuncture","Competitive eating","Sword swallowing","Fire eating","Ventriloquism","Base jumping","Cave diving","Free solo climbing","Speed chess","Wing walking","Blindfolded Rubik's cube","Escapology","Slacklining","Tightrope walking over canyon"]
  },
  "objects": {
    "easy": ["Chair","Table","Lamp","Phone","Umbrella","Backpack","Bicycle","Ladder","Mirror","Scissors","Clock","Toothbrush","Pillow","Blanket","Shoe","Hat","Glasses","Pencil","Spoon","Fork","Knife","Plate","Bowl","Cup","Bag","Key","Sofa","Bed","Camera","Watch","Book","Guitar","Drum","Balloon","Kite"],
    "medium": ["Grandfather Clock","Rocking Chair","Ironing Board","Lawn Mower","Vacuum Cleaner","Washing Machine","Sewing Machine","Microscope","Telescope","Compass","Abacus","Accordion","Periscope","Jackhammer","Typewriter","Phonograph","Cassette Tape","VHS Tape","Fax Machine","Lava Lamp","Snow Globe","Music Box","Kaleidoscope","Metronome","Sundial","Boomerang","Catapult","Trebuchet","Weather Vane","Theremin","Spirograph","Defibrillator","Stethoscope","Fire Extinguisher","Diving Helmet"],
    "hard": ["Astrolabe","Sextant","Theodolite","Pantograph","Chronometer","Spectrometer","Oscilloscope","Geiger Counter","Seismograph","Autoclave","Centrifuge","Electroscope","Galvanometer","Interferometer","Manometer","Nephelometer","Plethysmograph","Orrery","Astrolabe","Turbidimeter"]
  },
  "funny": {
    "easy": ["Tripping over","Sneezing","Hiccupping","Stubbing a toe","Slipping on banana peel","Snoring","Brain freeze","Belly flop","Yawning","Being tickled","Running in a dream","Chasing a chicken","Bad hair day","Spilling coffee","Walking into glass door","Missing a high five","Talking in sleep","Burping","Wearing pants backwards","Waving at wrong person","Getting hiccups","Air drumming","Invisible wall","Funny walk","Slow-motion run","Dramatic entrance","Accidental wink","Pretending to be on phone","Speed-reading","Running like Phoebe","Robot walk","Moonwalk","Dabbing","Floss dance","The worm"],
    "medium": ["Air guitar","Dad joke","Selfie stick","Flash mob","Chicken dance","Piggyback ride","Photobomb","Ordering wrong food","Calling teacher mom","Wrong number","Accidentally liking old photo","Autocorrect fail","Sitting in wet seat","Getting head stuck","Locked out of house","Explaining a joke","Running wrong direction","Narrating own life","Dramatic exit","Impersonating a celebrity","Invisible horse","Zombie walk","Gangnam style","Electric slide","Dramatic reading","The sprinkler","Mannequin challenge","Sock puppet show","Mime in a box","Pretending to swim on floor","Riding imaginary horse","Conducting invisible orchestra","Celebrating alone","Over-rehearsed handshake","Invisible car driving"],
    "hard": ["Planking","Rickroll","NPC behavior","Main character energy","Going viral","Speed running","Touch grass","Being a pick-me","Performative crying","Cringe compilation","Unboxing video","Mukbang","Getting ratio'd","Reacting to reaction video","Gaslighting","Gatekeeping","Girlbossing","Doomscrolling","Ghosting someone","Humble bragging"]
  },
  "christmas": {
    "easy": ["Santa Claus","Rudolph","Snowman","Christmas Tree","Reindeer","Elf","Present","Stocking","Mistletoe","Candy Cane","Gingerbread Man","Snowflake","Christmas Lights","Angel","Bell","Wreath","Nutcracker","Tinsel","Ornament","Star","Sleigh","Chimney","Fireplace","Turkey","Christmas Ham","Hot Cocoa","Cookies for Santa","Christmas Card","Advent Calendar","Carol Singing","Gift Wrapping","Christmas Jumper","Boxing Day","Eggnog","Christmas Dinner"],
    "medium": ["Nativity Scene","Christmas Carols","Figgy Pudding","Yule Log","Christmas Cracker","Midnight Mass","Wassailing","Poinsettia","Fruitcake","White Christmas","Carolers","Toys for Tots","Secret Santa","Ugly Sweater Contest","Christmas Pageant","The Night Before Christmas","The Grinch","Home Alone","A Christmas Carol","It's a Wonderful Life","Elf on the Shelf","Polar Express","Christmas Pudding","Mulled Wine","Mince Pies","Boxing Day Sales","New Year's Countdown","Christmas Eve","Holiday Office Party","Christmas Village","Santa's Workshop","North Pole","Christmas Star","Epiphany","Advent Wreath"],
    "hard": ["Krampus","Zwarte Piet","Sinterklaas","Befana","Pere Noel","Yule Lads","Odin's Wild Hunt","Epiphany","St. Nicholas Day","Feast of the Seven Fishes","Las Posadas","Misa de Gallo","Julnissen","Christkind","Weihnachtsmann","Joulupukki","Ded Moroz","Snegurochka","Nisse","La Befana"]
  }
}
```

- [ ] **Step 2: Verify file is valid JSON**

Run: `python3 -c "import json; d=json.load(open('wordineer-deploy/data/charades.json')); print('Categories:', list(d.keys())); print('Total entries:', sum(len(v) for cat in d.values() for v in cat.values()))"`

Expected output:
```
Categories: ['animals', 'movies', 'tv', 'books', 'celebrities', 'sports', 'food', 'places', 'actions', 'objects', 'funny', 'christmas']
Total entries: 1080
```

- [ ] **Step 3: Commit**

```bash
git add wordineer-deploy/data/charades.json
git commit -m "feat: add charades.json word/phrase dataset (1080 entries, 12 categories)"
```

---

## Task 2: Create charades-kids.json

**Files:**
- Create: `wordineer-deploy/data/charades-kids.json`

- [ ] **Step 1: Write the file**

Create `wordineer-deploy/data/charades-kids.json` with this exact content (kid-safe subset, no celebrities, no hard-to-explain entries):

```json
{
  "animals": {
    "easy": ["Cat","Dog","Elephant","Frog","Duck","Horse","Lion","Tiger","Monkey","Fish","Bird","Cow","Pig","Snake","Bear","Rabbit","Turtle","Bee","Butterfly","Shark","Panda","Koala","Parrot","Penguin","Zebra","Giraffe","Owl","Crab","Deer","Fox","Wolf","Chicken","Sheep","Whale","Hamster"],
    "medium": ["Kangaroo","Flamingo","Crocodile","Gorilla","Dolphin","Peacock","Porcupine","Jellyfish","Sloth","Raccoon","Skunk","Narwhal","Bison","Moose","Walrus","Otter","Lemur","Capybara","Meerkat","Sea horse"],
    "hard": ["Axolotl","Quokka","Pangolin","Okapi","Tapir","Echidna","Shoebill stork","Platypus","Narwhal","Blobfish"]
  },
  "movies": {
    "easy": ["Frozen","Toy Story","Shrek","Avatar","Batman","Bambi","Dumbo","Mulan","Tarzan","Aladdin","Spider-Man","Ghostbusters","Home Alone","Hocus Pocus","Casper","Pinocchio","The Wizard of Oz","Cinderella","Beauty and the Beast","Hercules","Pocahontas","Ratatouille","Brave","Coco","Moana","Encanto","Lilo and Stitch","The Little Mermaid","Paddington","Minions"],
    "medium": ["The Lion King","Jurassic Park","E.T.","Back to the Future","Indiana Jones","Finding Nemo","Up","Wall-E","Monsters Inc.","The Incredibles","Zoolander","Elf","Star Wars","Grease","Rocky"],
    "hard": []
  },
  "tv": {
    "easy": ["Friends","The Office","The Simpsons","Family Guy","Scooby-Doo","The Flintstones","The Jetsons","The Muppets","Sesame Street","Mister Rogers' Neighborhood","SpongeBob SquarePants","Dora the Explorer","Bluey","Peppa Pig","Paw Patrol","Winnie the Pooh","Tom and Jerry","Looney Tunes","The Teletubbies","Barney"],
    "medium": ["Stranger Things","Doctor Who","Sherlock","Brooklyn Nine-Nine","Parks and Recreation","Modern Family","New Girl","Arrested Development","Cobra Kai","Ted Lasso"],
    "hard": []
  },
  "books": {
    "easy": ["Harry Potter","The Jungle Book","Cinderella","Snow White","Pinocchio","Charlotte's Web","James and the Giant Peach","Matilda","Winnie the Pooh","Little Red Riding Hood","Goldilocks","The Very Hungry Caterpillar","The Gruffalo","Charlie and the Chocolate Factory","Alice in Wonderland","Peter Pan","The Lion the Witch and the Wardrobe","Treasure Island","Robin Hood","Sleeping Beauty","Rapunzel","Hansel and Gretel","Jack and the Beanstalk","The Three Little Pigs","Little Women","Oliver Twist","A Christmas Carol","The Secret Garden","Mary Poppins","The Little Prince","Anne of Green Gables","Where the Wild Things Are","Goodnight Moon","The Giving Tree","Paddington Bear"],
    "medium": ["The Hobbit","Percy Jackson","The Chronicles of Narnia","Ender's Game","The Hunger Games","The Da Vinci Code","Treasure Island","Robinson Crusoe","Swiss Family Robinson","20 000 Leagues Under the Sea"],
    "hard": []
  },
  "sports": {
    "easy": ["Swimming","Running","Tennis","Soccer","Baseball","Basketball","Golf","Boxing","Skiing","Cycling","Surfing","Gymnastics","Wrestling","Archery","Bowling","Volleyball","Football","Hockey","Rugby","Badminton","Table Tennis","Karate","Judo","Rowing","Diving","Figure Skating","Snowboarding","Skateboarding","Horse Riding","Fishing"],
    "medium": ["Long Jump","High Jump","Pole Vault","Discus Throw","Javelin Throw","Hurdles","Biathlon","Triathlon","Water Polo","Trampolining","Taekwondo","Lacrosse","Curling","Luge","Bobsled","Freestyle Skiing","BMX Racing","Rock Climbing","Canoe Slalom","Fencing"],
    "hard": []
  },
  "food": {
    "easy": ["Pizza","Hamburger","Hot Dog","Ice Cream","Sandwich","Spaghetti","Sushi","Taco","Donut","Cookie","Popcorn","Pancake","Waffle","Cake","Apple Pie","Bread","Banana","Apple","Orange","Strawberry","Chocolate","Cheese","Egg","Soup","Salad","Fried Chicken","Corn","Watermelon","Grapes","Pineapple","Milk","Coffee","Juice","Cereal","Peanut Butter"],
    "medium": ["Fish and Chips","Chicken Wings","Caesar Salad","Nachos","Pretzel","Cheesecake","Smoothie","Cotton Candy","Gingerbread","Churros","Dim Sum","Ramen","Burrito","Gyoza","Lasagna"],
    "hard": []
  },
  "places": {
    "easy": ["Beach","Mountain","City","Farm","School","Hospital","Library","Airport","Park","Zoo","Museum","Castle","Island","Desert","Forest","Jungle","Lake","River","Ocean","Cave","Lighthouse","Palace","Church","Stadium","Hotel","Restaurant","Market","Bridge","Tower","Volcano","Waterfall","Canyon","Valley","Harbor","Treehouse"],
    "medium": ["Eiffel Tower","Great Wall of China","Statue of Liberty","Big Ben","Colosseum","Niagara Falls","Grand Canyon","Mount Everest","Amazon River","Sahara Desert","Antarctica","Times Square","Stonehenge","Machu Picchu","Mount Fuji","Taj Mahal","Sydney Opera House","Golden Gate Bridge","Leaning Tower of Pisa","Acropolis"],
    "hard": []
  },
  "actions": {
    "easy": ["Running","Jumping","Swimming","Sleeping","Eating","Drinking","Dancing","Singing","Cooking","Driving","Reading","Writing","Laughing","Crying","Clapping","Waving","Hugging","Typing","Taking a selfie","Brushing teeth","Combing hair","Tying shoes","Throwing a ball","Catching a ball","Riding a bike","Walking a dog","Blowing a candle","Playing guitar","Playing piano","Drawing","Painting","Skipping","Hopping","Spinning","Cartwheeling"],
    "medium": ["Skateboarding","Rock climbing","Surfing","Ice skating","Snowboarding","Doing yoga","Juggling","Magic trick","Playing video games","Hiking","Camping","Pottery","Flipping a pancake","Giving a speech","Solving a puzzle","Baking cookies","Building a sandcastle","Flying a kite","Blowing bubbles","Playing catch"],
    "hard": []
  },
  "objects": {
    "easy": ["Chair","Table","Lamp","Phone","Umbrella","Backpack","Bicycle","Ladder","Mirror","Scissors","Clock","Toothbrush","Pillow","Blanket","Shoe","Hat","Glasses","Pencil","Spoon","Fork","Knife","Plate","Bowl","Cup","Bag","Key","Sofa","Bed","Camera","Watch","Guitar","Drum","Balloon","Kite","Book"],
    "medium": ["Grandfather Clock","Rocking Chair","Vacuum Cleaner","Washing Machine","Microscope","Telescope","Compass","Accordion","Kaleidoscope","Boomerang","Snow Globe","Music Box","Metronome","Sundial","Theremin","Diving Helmet","Periscope","Weather Vane","Lava Lamp","Spirograph"],
    "hard": []
  },
  "funny": {
    "easy": ["Tripping over","Sneezing","Hiccupping","Stubbing a toe","Slipping on banana peel","Snoring","Brain freeze","Belly flop","Yawning","Being tickled","Running in a dream","Chasing a chicken","Bad hair day","Walking into glass door","Missing a high five","Burping","Wearing pants backwards","Waving at wrong person","Air drumming","Funny walk","Slow-motion run","Dramatic entrance","Robot walk","Moonwalk","Dabbing"],
    "medium": ["Air guitar","Flash mob","Chicken dance","Piggyback ride","Photobomb","Calling teacher mom","Autocorrect fail","Explaining a joke","Running wrong direction","Dramatic exit","Invisible horse","Zombie walk","Gangnam style","Electric slide","Mime in a box","Pretending to swim on floor","Riding imaginary horse","Invisible car driving","Conducting invisible orchestra","Celebrating alone"],
    "hard": []
  },
  "christmas": {
    "easy": ["Santa Claus","Rudolph","Snowman","Christmas Tree","Reindeer","Elf","Present","Stocking","Mistletoe","Candy Cane","Gingerbread Man","Snowflake","Christmas Lights","Angel","Bell","Wreath","Nutcracker","Tinsel","Ornament","Star","Sleigh","Chimney","Fireplace","Christmas Ham","Hot Cocoa","Cookies for Santa","Christmas Card","Advent Calendar","Carol Singing","Gift Wrapping","Christmas Jumper","Boxing Day","Eggnog","Christmas Dinner","Reindeer Games"],
    "medium": ["Nativity Scene","Christmas Carols","Figgy Pudding","Yule Log","Christmas Cracker","Wassailing","The Night Before Christmas","The Grinch","Home Alone","A Christmas Carol","It's a Wonderful Life","Elf on the Shelf","Polar Express","Christmas Pudding","Mulled Wine","Secret Santa","Ugly Sweater Contest","Santa's Workshop","North Pole","Christmas Star"],
    "hard": []
  }
}
```

- [ ] **Step 2: Verify**

Run: `python3 -c "import json; d=json.load(open('wordineer-deploy/data/charades-kids.json')); print('Categories:', list(d.keys())); print('Total entries:', sum(len(v) for cat in d.values() for v in cat.values()))"`

Expected output:
```
Categories: ['animals', 'movies', 'tv', 'books', 'celebrities', 'sports', 'food', 'places', 'actions', 'objects', 'funny', 'christmas']
Total entries: ~430
```

Note: celebrities category is absent from kids.json (intentional — omitted for age appropriateness). The normalized words from missing categories return empty arrays, which the filter handles gracefully.

- [ ] **Step 3: Commit**

```bash
git add wordineer-deploy/data/charades-kids.json
git commit -m "feat: add charades-kids.json curated kid-safe dataset"
```

---

## Task 3: Create charades-generator.html

**Files:**
- Create: `template-deploy/tools-src/charades-generator.html`

This is the longest task. The file is adapted from `pictionary-word-generator.html` with these changes:
- Age Group seg control (All Ages / Kids / Adults)
- 12 category options in dropdown
- Dual data loading: `charades.json` + `charades-kids.json`
- `CAT_LABELS` map for display
- `filtered()` respects `state.ageGroup`
- Updated copy throughout (charades rules, not drawing rules)
- Category badge shows label like "Movies", "TV Shows"

- [ ] **Step 1: Write the file**

Create `template-deploy/tools-src/charades-generator.html` with this content:

```html
<!-- CONFIG { "url": "/charades-generator/", "output": "charades-generator.html" } -->

<!-- SLOT:meta -->
<title>Charades Generator — Free Random Words & Phrases | Wordineer</title>
<meta name="description" content="Generate random charades words and phrases for parties, classrooms, and family game nights. Filter by category, difficulty, and age group. Free, no sign-up, instant results.">
<link rel="canonical" href="https://wordineer.com/charades-generator/">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Wordineer">
<meta property="og:title" content="Charades Generator — Free Random Words & Phrases | Wordineer">
<meta property="og:description" content="Generate random charades words and phrases — filter by category, difficulty, and age group. Free, no sign-up, instant.">
<meta property="og:url" content="https://wordineer.com/charades-generator/">
<meta property="og:image" content="https://wordineer.com/og-image.png">
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "What is a Charades Generator?",
      "acceptedAnswer": { "@type": "Answer", "text": "A charades generator picks random words and phrases for the acting and guessing game charades. Choose a category, difficulty, and age group, then use the results for parties, classrooms, or family game nights." }
    },
    {
      "@type": "Question",
      "name": "How many words should I generate per round?",
      "acceptedAnswer": { "@type": "Answer", "text": "For a standard round, generate 5 to 10 words. This gives players enough variety while keeping rounds short. Adjust the count down for beginners and up for experienced groups." }
    },
    {
      "@type": "Question",
      "name": "Can I use this charades generator for kids?",
      "acceptedAnswer": { "@type": "Answer", "text": "Yes. Set Age Group to Kids and the generator switches to a curated dataset of age-appropriate words and phrases. You can also set Difficulty to Easy for the simplest possible words." }
    }
  ]
}
</script>
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "WebApplication",
  "name": "Charades Generator",
  "url": "https://wordineer.com/charades-generator/",
  "description": "Generate random charades words and phrases for parties, classrooms, and family game nights. Filter by category, difficulty, and age group.",
  "applicationCategory": "GameApplication",
  "operatingSystem": "Web",
  "offers": { "@type": "Offer", "price": "0", "priceCurrency": "USD" },
  "publisher": { "@id": "https://wordineer.com/#organization" }
}
</script>
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    { "@type": "ListItem", "position": 1, "name": "Wordineer", "item": "https://wordineer.com/" },
    { "@type": "ListItem", "position": 2, "name": "Word Tools", "item": "https://wordineer.com/word-tools/" },
    { "@type": "ListItem", "position": 3, "name": "Charades Generator", "item": "https://wordineer.com/charades-generator/" }
  ]
}
</script>
<!-- /SLOT:meta -->

<!-- SLOT:style -->
<style>
.tool-wrap{max-width:960px;margin:0 auto;padding:24px 24px 0}
.pic-card{border:1px solid var(--border);border-radius:8px;background:var(--bg);box-shadow:var(--shadow);overflow:hidden}
.pic-layout{display:grid;grid-template-columns:300px 1fr;min-height:520px}
.pic-controls{background:var(--bg-2);border-right:1px solid var(--border-2);padding:16px}
.pic-main{display:flex;flex-direction:column;min-width:0}
.control-group{margin-bottom:16px}
.control-label{display:block;font-size:10px;font-weight:700;color:var(--text-3);text-transform:uppercase;letter-spacing:.06em;margin-bottom:7px}
.seg{display:grid;grid-template-columns:repeat(4,1fr);gap:6px}
.seg.three{grid-template-columns:repeat(3,1fr)}
.seg button,.pic-select,.count-input{border:1px solid var(--border);background:var(--bg);color:var(--text-2);border-radius:6px;font:inherit;font-size:12px;font-weight:600;padding:8px 6px;transition:border-color .15s,background .15s,color .15s}
.seg button{cursor:pointer}
.seg button.active{background:var(--brand);border-color:var(--brand);color:white}
.count-input{width:100%;font-size:13px;padding:7px 10px;color:var(--text)}
.mobile-more-btn{display:none;width:100%;margin-top:8px}
.options-panel{display:block}
.pic-select{width:100%;appearance:none}
.primary-btn{width:100%;border:0;border-radius:6px;background:var(--brand);color:white;font-size:14px;font-weight:700;padding:12px 14px;cursor:pointer}
.secondary-actions{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:8px}
.small-btn{border:1px solid var(--border);background:var(--bg);color:var(--text-2);border-radius:6px;font-size:12px;font-weight:600;padding:9px 8px;cursor:pointer}
.small-btn:hover,.seg button:hover{border-color:var(--brand)}
.timer-box{border:1px solid var(--border);background:var(--bg);border-radius:8px;padding:12px;margin-top:10px}
.timer-time{font-size:34px;line-height:1;font-weight:700;color:var(--text);margin-bottom:10px;font-variant-numeric:tabular-nums}
.timer-actions{display:grid;grid-template-columns:1fr 1fr;gap:8px}
.rules-mini{font-size:12px;line-height:1.55;color:var(--text-2);background:#fffaf0;border:1px solid #f1ddaf;border-radius:8px;padding:12px;margin-top:24px}
.pic-top{display:flex;align-items:center;justify-content:space-between;gap:12px;padding:16px;border-bottom:1px solid var(--border-2)}
.pic-status{font-size:12px;color:var(--text-3)}
.word-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px;padding:16px;list-style:none;margin:0;flex:1}
.word-card{border:1px solid var(--border);border-radius:8px;padding:14px;background:var(--bg);display:flex;align-items:flex-start;justify-content:space-between;gap:10px;min-height:74px}
.word-card.hidden .word-text,.word-card.hidden .word-meta{filter:blur(7px);user-select:none}
.word-text{font-size:20px;font-weight:700;color:var(--text);line-height:1.2;margin-bottom:5px}
.word-meta{font-size:11px;color:var(--text-3);text-transform:uppercase;letter-spacing:.05em}
.word-cat-badge{display:inline-block;font-size:10px;font-weight:700;background:var(--brand-light,#EEEDFE);color:var(--brand-dark,#3C3489);border-radius:4px;padding:2px 6px;margin-bottom:4px;text-transform:uppercase;letter-spacing:.04em}
.save-btn{width:30px;height:30px;border:1px solid var(--border);border-radius:6px;background:var(--bg);color:var(--text-3);cursor:pointer;flex:0 0 auto}
.save-btn.saved{background:#fff1f1;color:#d93838;border-color:#f0b8b8}
.saved-panel{border-top:1px solid var(--border-2);padding:12px 16px;background:var(--bg-2)}
.saved-top{display:flex;align-items:center;justify-content:space-between;margin-bottom:8px}
.saved-label{font-size:10px;font-weight:700;color:var(--text-3);text-transform:uppercase;letter-spacing:.06em}
.saved-list{display:flex;flex-wrap:wrap;gap:6px;min-height:24px}
.saved-pill{font-size:12px;padding:4px 10px;background:var(--brand-light);color:var(--brand-dark);border-radius:999px;display:flex;align-items:center;gap:6px}
.saved-pill button{border:0;background:transparent;color:inherit;cursor:pointer;padding:0;font-size:14px;line-height:1}
.empty-text{font-size:12px;color:var(--text-3);font-style:italic}
.toast{position:fixed;left:50%;bottom:20px;transform:translateX(-50%);background:var(--text);color:white;padding:8px 12px;border-radius:6px;font-size:12px;opacity:0;pointer-events:none;transition:opacity .18s;z-index:9999}
.toast.show{opacity:1}
.explainer ol{margin:0 0 10px;padding-left:20px;font-size:14px;color:var(--text-2);line-height:1.7}
.explainer li{padding-left:2px;margin-bottom:4px}
.idea-tags{display:flex;flex-wrap:wrap;gap:8px;margin-top:10px}
.idea-tags span{font-size:12px;background:var(--bg-2);border:1px solid var(--border);border-radius:999px;padding:5px 10px;color:var(--text-2)}
@media(max-width:700px){
  .tool-wrap{padding:14px 16px 0}
  .pic-layout{grid-template-columns:1fr}
  .pic-controls{border-right:0;border-bottom:1px solid var(--border-2)}
  .word-grid{grid-template-columns:1fr}
  .mobile-more-btn{display:block}
  .options-panel{display:none;margin-top:12px}
  .options-panel.open{display:block;margin-bottom:12px}
  .timer-time{font-size:22px;margin-bottom:6px}
  .timer-box{padding:8px}
}
@media print{
  .nav,.mega,.hero,.pic-controls,.pic-top,.saved-panel,.ad-leaderboard,.content-wrap,.footer{display:none!important}
  .tool-wrap{max-width:none;padding:0}
  .pic-card{border:0;box-shadow:none}
  .pic-layout{display:block}
  .word-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:12px;padding:0}
  .word-card{min-height:110px;break-inside:avoid;border:1px solid #111}
}
</style>
<!-- /SLOT:style -->

<!-- SLOT:hero -->
<div class="breadcrumb">
  <div class="breadcrumb-inner">
    <a href="/">Wordineer</a>
    <span class="breadcrumb-sep">›</span>
    <a href="/word-tools/">Word Tools</a>
    <span class="breadcrumb-sep">›</span>
    <span aria-current="page">Charades Generator</span>
  </div>
</div>
<div class="hero">
  <div class="hero-badge">
    <svg viewBox="0 0 11 11" fill="none"><circle cx="5.5" cy="5.5" r="4.5" stroke="#3C3489" stroke-width="1"/><path d="M3.5 5.5l1.5 1.5L8 3.5" stroke="#3C3489" stroke-width="1.2" stroke-linecap="round"/></svg>
    Free · No sign-up · Instant results
  </div>
  <h1>Charades Generator</h1>
  <p>Generate random charades words and phrases in one click — filter by category, difficulty, and age group for the perfect round every time.</p>
</div>
<!-- /SLOT:hero -->

<!-- SLOT:tool -->
<div class="tool-wrap" aria-label="Charades word generator">
  <div class="pic-card">
    <div class="pic-layout">
      <aside class="pic-controls">
        <div class="control-group">
          <label class="control-label" for="count-input">Number of words</label>
          <input class="count-input" id="count-input" type="number" min="1" max="50" step="1" value="5" inputmode="numeric">
          <span id="pic-count-error" style="display:none;font-size:11px;color:#E24B4A;margin-top:4px;">Enter a number from 1 to 50</span>
          <button class="small-btn mobile-more-btn" type="button" id="more-options-btn" aria-expanded="false" aria-controls="more-options-panel">More options</button>
        </div>
        <div class="options-panel" id="more-options-panel">
          <div class="control-group">
            <span class="control-label">Age Group</span>
            <div class="seg three" data-control="ageGroup">
              <button type="button" class="active" data-value="all">All Ages</button>
              <button type="button" data-value="kids">Kids</button>
              <button type="button" data-value="adults">Adults</button>
            </div>
          </div>
          <div class="control-group">
            <span class="control-label">Difficulty</span>
            <div class="seg three" data-control="difficulty">
              <button type="button" class="active" data-value="easy">Easy</button>
              <button type="button" data-value="medium">Medium</button>
              <button type="button" data-value="hard">Hard</button>
            </div>
          </div>
          <div class="control-group">
            <label class="control-label" for="pic-category">Category</label>
            <select id="pic-category" class="pic-select">
              <option value="all">All categories</option>
              <option value="animals">Animals</option>
              <option value="movies">Movies</option>
              <option value="tv">TV Shows</option>
              <option value="books">Books</option>
              <option value="celebrities">Celebrities</option>
              <option value="sports">Sports</option>
              <option value="food">Food</option>
              <option value="places">Places</option>
              <option value="actions">Actions</option>
              <option value="objects">Objects</option>
              <option value="funny">Funny</option>
              <option value="christmas">Christmas</option>
            </select>
          </div>
          <div class="timer-box">
            <span class="control-label">Round timer</span>
            <div class="seg three" data-control="timer">
              <button type="button" data-value="30">30s</button>
              <button type="button" class="active" data-value="60">60s</button>
              <button type="button" data-value="90">90s</button>
            </div>
            <div class="timer-time" id="timer-display">1:00</div>
            <div class="timer-actions">
              <button class="small-btn" type="button" id="timer-toggle">Start</button>
              <button class="small-btn" type="button" id="timer-reset">Reset</button>
            </div>
          </div>
        </div>
        <button class="primary-btn" type="button" id="generate-btn">Generate Charades Words</button>
        <div class="secondary-actions">
          <button class="small-btn" type="button" id="copy-btn">Copy list</button>
          <button class="small-btn" type="button" id="print-btn">Print cards</button>
          <button class="small-btn" type="button" id="hide-btn">Hide words</button>
          <button class="small-btn" type="button" id="clear-btn">Clear saved</button>
        </div>
        <div class="rules-mini">Act out the word silently — no speaking, mouthing, or pointing at objects. Your team wins a point when they guess correctly before the timer runs out.</div>
      </aside>
      <section class="pic-main">
        <div class="pic-top">
          <div>
            <strong>Words for this round</strong>
            <div class="pic-status" id="status">5 easy words generated</div>
          </div>
          <button class="small-btn" type="button" id="reset-session-btn">Reset repeats</button>
        </div>
        <ul class="word-grid" id="word-grid"></ul>
        <div class="saved-panel">
          <div class="saved-top">
            <span class="saved-label">Saved words <span id="saved-count">(0)</span></span>
            <button class="small-btn" type="button" id="copy-saved-btn">Copy saved</button>
          </div>
          <div class="saved-list" id="saved-list"><span class="empty-text">Save words here before you generate the next round.</span></div>
        </div>
      </section>
    </div>
  </div>
</div>
<!-- /SLOT:tool -->

<!-- SLOT:ad_b -->
<div class="ad-leaderboard">
  <div class="ad-leaderboard-inner">
    <span class="ad-tag">Advertisement · 728×90</span>
    <div class="ad-mock-content">
      <div class="ad-title">Grammarly - write with confidence. Grammar, tone &amp; clarity.</div>
      <div class="ad-sub">Used by 30 million people. Works in Google Docs, Gmail, Word and more.</div>
      <a href="https://grammarly.com" target="_blank" rel="noopener" class="ad-mock-cta">Try Grammarly free</a>
    </div>
  </div>
</div>
<!-- /SLOT:ad_b -->

<!-- SLOT:explainer -->
<div class="explainer">
  <h2>What is a Charades Generator?</h2>
  <p>A charades generator solves the blank-mind problem that kills every game night: someone says "let's play charades" and nobody can think of a single word worth acting out. Instead of scribbling on paper slips, scrolling through group chats, or recycling the same five words from last time, you get a fresh set of words and phrases in one click — filtered to exactly the group you're playing with.</p>
  <p>This tool covers 12 categories spanning classic charades staples (Animals, Actions, Objects, Places, Food) and the entertainment categories charades is famous for (Movies, TV Shows, Books, Celebrities). Each category has three difficulty tiers and an age group filter so you can go from a kindergarten classroom to an adult game night without switching tools.</p>

  <h2>How It Works</h2>
  <ol>
    <li>Choose an <strong>Age Group</strong> — All Ages uses the full word set, Kids switches to a curated family-safe dataset, Adults unlocks the full range including harder pop culture references.</li>
    <li>Pick a <strong>Category</strong> or leave it on All categories for a mixed surprise round.</li>
    <li>Set the <strong>Difficulty</strong> — Easy words are immediately recognisable, Medium require a bit more creativity, Hard will test even experienced players.</li>
    <li>Click <strong>Generate Charades Words</strong>. The tool avoids repeats within your session so you won't see the same word twice until you reset.</li>
    <li>Use <strong>Hide Words</strong> so the actor can reveal each card themselves without the group seeing it first. Start the timer and go.</li>
  </ol>

  <h2>Charades Best Practices</h2>
  <p>The biggest mistake beginners make is trying to be too literal. Here's what separates good charades players from great ones:</p>
  <ul>
    <li><strong>Use standard signals</strong> — Hold up the number of fingers for word count. Tap your wrist for "hurry up." Cup your ear for "sounds like." Touch your nose when someone's close.</li>
    <li><strong>Start with the structure</strong> — If it's a movie title, hold up an imaginary camera. For a book, open your hands flat. For a TV show, draw a rectangle in the air. This tells guessers what kind of thing they're looking for.</li>
    <li><strong>Warm up with Easy rounds</strong> — Especially if you're playing with mixed ages or first-timers. Confidence early makes hard rounds more fun later.</li>
    <li><strong>Keep rounds to 60–90 seconds</strong> — Shorter rounds create urgency and energy. Use the built-in timer to keep things moving.</li>
    <li><strong>Act confidently</strong> — Even if you're unsure, committing to the performance is half the battle. Hesitant gestures are harder to guess than bold, committed ones.</li>
    <li><strong>Mix categories on All</strong> — Random surprises (an animal followed by a movie title followed by a food) keep guessers on their toes and make longer games more interesting.</li>
  </ul>

  <h2>How to Manage Your Game</h2>
  <p>For parties and classrooms, the workflow is: generate before the game starts, save your favourites, then hide. Use <strong>Hide Words</strong> mode to blur the cards — the actor taps a card to reveal only their word, keeping the rest hidden from the group. The <strong>Saved</strong> tray lets you build a custom list across multiple generate sessions, which is useful for pre-curating a round with a specific theme. <strong>Print Cards</strong> gives you a physical set you can cut up and use without any screen in the room — great for outdoor games or when you don't want phones at the table.</p>

  <div class="idea-tags">
    <span>Kangaroo</span><span>The Lion King</span><span>Skydiving</span><span>Eiffel Tower</span><span>Taylor Swift</span><span>Slipping on banana peel</span>
  </div>
</div>
<!-- /SLOT:explainer -->

<!-- SLOT:faq -->
<div class="faq">
  <h2 class="faq-title">Charades Generator FAQs</h2>
  <div class="faq-item open">
    <div class="faq-q"><span class="faq-q-text">How many words should I generate per round?</span><svg class="faq-chevron" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div>
    <div class="faq-a">Five to ten words is the sweet spot for most groups. Five keeps rounds fast-paced; ten works well when you want a longer session or have a big group taking turns. Beginners and young kids do best with three to five Easy words.</div>
  </div>
  <div class="faq-item">
    <div class="faq-q"><span class="faq-q-text">What's the difference between Easy, Medium, and Hard?</span><svg class="faq-chevron" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div>
    <div class="faq-a">Easy words are immediately recognisable single words anyone can act out — Cat, Pizza, Running. Medium includes more complex single words and short phrases that require some creative acting — Jurassic Park, Rock Climbing, Dad Joke. Hard includes obscure references, abstract concepts, and long phrases that challenge even experienced players — Inception, Axolotl, Performing Brain Surgery.</div>
  </div>
  <div class="faq-item">
    <div class="faq-q"><span class="faq-q-text">Can I use this for kids?</span><svg class="faq-chevron" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div>
    <div class="faq-a">Yes. Set Age Group to Kids and the generator switches to a curated dataset of age-appropriate words. The Kids set covers animals, classic movies, children's books, sports, food, objects, and actions — all screened to be suitable for younger players. Celebrities are excluded from the Kids set.</div>
  </div>
  <div class="faq-item">
    <div class="faq-q"><span class="faq-q-text">What categories are included?</span><svg class="faq-chevron" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div>
    <div class="faq-a">Twelve categories: Animals, Movies, TV Shows, Books, Celebrities, Sports, Food, Places, Actions, Objects, Funny, and Christmas. The Celebrities and Funny categories are most appropriate for adults; all other categories work for all ages when set to Easy or Medium.</div>
  </div>
  <div class="faq-item">
    <div class="faq-q"><span class="faq-q-text">How do I use the timer?</span><svg class="faq-chevron" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div>
    <div class="faq-a">Choose 30, 60, or 90 seconds from the timer options, then click Start when the actor is ready. The timer counts down and shows a toast notification when time is up. Click Reset to return to the full duration between rounds.</div>
  </div>
  <div class="faq-item">
    <div class="faq-q"><span class="faq-q-text">Can I print the word cards?</span><svg class="faq-chevron" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div>
    <div class="faq-a">Yes. Click Print Cards to open the browser print dialog. The controls, navigation, and ads are hidden in print view so you get a clean two-column card layout. Cut the cards out for a fully offline game.</div>
  </div>
  <div class="faq-item">
    <div class="faq-q"><span class="faq-q-text">What are the standard charades hand signals?</span><svg class="faq-chevron" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div>
    <div class="faq-a">Hold up fingers for the number of words. Pinch two fingers together to signal a small word (a, the, of). Cup your ear for "sounds like." Tap your wrist for "hurry up." Touch your nose when a guess is correct. Open hands flat for a book title; hold up an imaginary camera for a movie; draw a rectangle in the air for a TV show.</div>
  </div>
  <div class="faq-item">
    <div class="faq-q"><span class="faq-q-text">How is this different from Pictionary?</span><svg class="faq-chevron" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div>
    <div class="faq-a">Pictionary requires players to draw the word; charades requires players to act it out silently with gestures and body language. Charades words tend to be longer phrases (movie titles, actions, celebrities) while Pictionary words are typically drawable objects and scenes. Wordineer has a separate <a href="/pictionary-word-generator/">Pictionary Word Generator</a> optimised for drawing-friendly words.</div>
  </div>
</div>
<!-- /SLOT:faq -->

<!-- SLOT:who -->
<div class="section">
  <h2 class="section-title" style="margin-bottom:14px">Who Uses the Charades Generator?</h2>
  <div class="uc-grid">
    <div class="uc"><div class="uc-title">Family game nights</div><div class="uc-body">Use the Age Group filter to mix adult and kids words across rounds. The timer keeps everyone engaged and the category badges make it easy to call out themes in advance.</div></div>
    <div class="uc"><div class="uc-title">Party hosts</div><div class="uc-body">Generate a pre-made list, save your favourites, and print cards before guests arrive. No scrambling for paper slips or repeating the same tired words.</div></div>
    <div class="uc"><div class="uc-title">Teachers &amp; classrooms</div><div class="uc-body">Set Age Group to Kids, pick a category that matches the lesson (Animals, Actions, Books), and run a quick vocabulary warmup or indoor activity without any setup.</div></div>
    <div class="uc"><div class="uc-title">Team-building &amp; icebreakers</div><div class="uc-body">Charades works on Zoom as well as in person. Use Medium difficulty with Movies or Celebrities for a fast-paced, universally accessible icebreaker that gets laughs without awkward silence.</div></div>
  </div>
</div>
<!-- /SLOT:who -->

<!-- SLOT:init -->
<div class="toast" id="toast" role="status" aria-live="polite"></div>
<script>
(function(){
  const CAT_LABELS={animals:'Animals',movies:'Movies',tv:'TV Shows',books:'Books',celebrities:'Celebrities',sports:'Sports',food:'Food',places:'Places',actions:'Actions',objects:'Objects',funny:'Funny',christmas:'Christmas'};
  const SEED=[
    {w:'Cat',c:['animals'],d:'easy'},{w:'Dog',c:['animals'],d:'easy'},{w:'Elephant',c:['animals'],d:'easy'},{w:'Penguin',c:['animals'],d:'easy'},{w:'Shark',c:['animals'],d:'easy'},
    {w:'Frozen',c:['movies'],d:'easy'},{w:'Toy Story',c:['movies'],d:'easy'},{w:'Shrek',c:['movies'],d:'easy'},{w:'Bambi',c:['movies'],d:'easy'},{w:'Moana',c:['movies'],d:'easy'},
    {w:'Friends',c:['tv'],d:'easy'},{w:'The Office',c:['tv'],d:'easy'},{w:'Seinfeld',c:['tv'],d:'easy'},{w:'The Simpsons',c:['tv'],d:'easy'},{w:'Scooby-Doo',c:['tv'],d:'easy'},
    {w:'Harry Potter',c:['books'],d:'easy'},{w:'Alice in Wonderland',c:['books'],d:'easy'},{w:'Matilda',c:['books'],d:'easy'},{w:'Peter Pan',c:['books'],d:'easy'},{w:'Cinderella',c:['books'],d:'easy'},
    {w:'Taylor Swift',c:['celebrities'],d:'easy'},{w:'Beyonce',c:['celebrities'],d:'easy'},{w:'Tom Hanks',c:['celebrities'],d:'easy'},{w:'Oprah Winfrey',c:['celebrities'],d:'easy'},{w:'LeBron James',c:['celebrities'],d:'easy'},
    {w:'Swimming',c:['sports'],d:'easy'},{w:'Soccer',c:['sports'],d:'easy'},{w:'Golf',c:['sports'],d:'easy'},{w:'Basketball',c:['sports'],d:'easy'},{w:'Skiing',c:['sports'],d:'easy'},
    {w:'Pizza',c:['food'],d:'easy'},{w:'Ice Cream',c:['food'],d:'easy'},{w:'Sushi',c:['food'],d:'easy'},{w:'Pancake',c:['food'],d:'easy'},{w:'Donut',c:['food'],d:'easy'},
    {w:'Beach',c:['places'],d:'easy'},{w:'Zoo',c:['places'],d:'easy'},{w:'Castle',c:['places'],d:'easy'},{w:'Museum',c:['places'],d:'easy'},{w:'Airport',c:['places'],d:'easy'},
    {w:'Running',c:['actions'],d:'easy'},{w:'Jumping',c:['actions'],d:'easy'},{w:'Dancing',c:['actions'],d:'easy'},{w:'Sleeping',c:['actions'],d:'easy'},{w:'Singing',c:['actions'],d:'easy'},
    {w:'Chair',c:['objects'],d:'easy'},{w:'Umbrella',c:['objects'],d:'easy'},{w:'Scissors',c:['objects'],d:'easy'},{w:'Clock',c:['objects'],d:'easy'},{w:'Camera',c:['objects'],d:'easy'},
    {w:'Sneezing',c:['funny'],d:'easy'},{w:'Belly flop',c:['funny'],d:'easy'},{w:'Hiccupping',c:['funny'],d:'easy'},{w:'Brain freeze',c:['funny'],d:'easy'},{w:'Slipping on banana peel',c:['funny'],d:'easy'},
    {w:'Santa Claus',c:['christmas'],d:'easy'},{w:'Snowman',c:['christmas'],d:'easy'},{w:'Rudolph',c:['christmas'],d:'easy'},{w:'Candy Cane',c:['christmas'],d:'easy'},{w:'Christmas Tree',c:['christmas'],d:'easy'}
  ];
  const SEED_COPY=[...SEED];
  let words=[...SEED],kidsWords=[],charFullLoaded=false,charLoadPromise=null,kidsFullLoaded=false,kidsLoadPromise=null;
  function charNormalizeWords(raw){
    if(Array.isArray(raw))return raw.map(([w,c,d])=>({w,c,d}));
    const out=[];
    Object.entries(raw||{}).forEach(([cat,levels])=>{
      Object.entries(levels||{}).forEach(([diff,items])=>{
        (items||[]).forEach(item=>{
          if(typeof item==='string')out.push({w:item,c:[cat],d:diff});
          else if(item&&item.w)out.push({w:item.w,c:item.c||[cat],d:item.d||diff});
        });
      });
    });
    return out;
  }
  function charLoadFullWords(){
    if(charFullLoaded||charLoadPromise)return;
    charLoadPromise=fetch('/data/charades.json').then(r=>{if(!r.ok)throw new Error(r.status);return r.json()}).then(raw=>{words=charNormalizeWords(raw);charFullLoaded=true}).catch(()=>{charLoadPromise=null});
  }
  function charLoadKidsWords(){
    if(kidsFullLoaded||kidsLoadPromise)return;
    kidsLoadPromise=fetch('/data/charades-kids.json').then(r=>{if(!r.ok)throw new Error(r.status);return r.json()}).then(raw=>{kidsWords=charNormalizeWords(raw);kidsFullLoaded=true;if(state.ageGroup==='kids')generate();}).catch(()=>{kidsLoadPromise=null});
  }
  function charScheduleLoad(){if(charFullLoaded)return;if('requestIdleCallback' in window)requestIdleCallback(charLoadFullWords,{timeout:4000});else setTimeout(charLoadFullWords,200)}
  window.addEventListener('load',charScheduleLoad,{once:true});
  const state={count:5,difficulty:'easy',category:'all',ageGroup:'all',timer:60,current:[],saved:[],seen:new Set(),hidden:false,remaining:60,running:false,interval:null};
  const $=id=>document.getElementById(id),grid=$('word-grid'),status=$('status'),savedList=$('saved-list'),savedCount=$('saved-count'),toast=$('toast');
  const picCountInput=$('count-input'),picCountError=$('pic-count-error');
  function showToast(text){toast.textContent=text;toast.classList.add('show');setTimeout(()=>toast.classList.remove('show'),1600)}
  function setSeg(control,value){document.querySelectorAll(`[data-control="${control}"] button`).forEach(btn=>btn.classList.toggle('active',btn.dataset.value===String(value)));if(control==='count')picCountInput.value=value}
  function picValidateCount(){const v=parseInt(picCountInput.value);const invalid=isNaN(v)||v<1||v>50;picCountError.style.display=invalid?'block':'none';picCountInput.style.borderColor=invalid?'#E24B4A':'';return !invalid}
  function setCount(value){const next=Math.max(1,Math.min(50,Number(value)||1));state.count=next;picCountInput.style.borderColor='';picCountError.style.display='none';setSeg('count',next)}
  function activePool(){if(state.ageGroup==='kids')return kidsFullLoaded?kidsWords:SEED_COPY;return words;}
  function filtered(){const pool=activePool();if(state.category==='all')return pool.filter(item=>item.d===state.difficulty);return pool.filter(item=>item.d===state.difficulty&&item.c.includes(state.category))}
  function generate(){let pool=filtered().filter(item=>!state.seen.has(item.w));if(!pool.length&&state.seen.size){state.seen.clear();pool=filtered()}if(!pool.length){state.current=[];renderWords();return}const chosen=[];while(chosen.length<state.count&&pool.length){const idx=Math.floor(Math.random()*pool.length);const item=pool.splice(idx,1)[0];chosen.push(item);state.seen.add(item.w)}state.current=chosen;renderWords()}
  function renderWords(){if(!state.current.length){grid.innerHTML='<li style="grid-column:1/-1;padding:24px;text-align:center;color:var(--text-3)">No words found — try a different filter or click Generate</li>';const catLabel=state.category==='all'?'all categories':(CAT_LABELS[state.category]||state.category);status.textContent=`No ${state.difficulty} ${catLabel} words found`;return}grid.innerHTML=state.current.map(item=>{const saved=state.saved.includes(item.w);const catLabel=CAT_LABELS[item.c[0]]||item.c[0];return `<li class="word-card${state.hidden?' hidden':''}"><div><div class="word-cat-badge">${catLabel}</div><div class="word-text">${item.w}</div><div class="word-meta">${item.d}</div></div><button class="save-btn${saved?' saved':''}" type="button" data-save="${item.w}" aria-label="Save ${item.w}">♥</button></li>`}).join('');const catLabel=state.category==='all'?'all categories':(CAT_LABELS[state.category]||state.category);status.textContent=`${state.current.length} ${state.difficulty} ${catLabel} word${state.current.length!==1?'s':''} generated`}
  function renderSaved(){savedCount.textContent=`(${state.saved.length})`;savedList.innerHTML=state.saved.length?state.saved.map(word=>`<span class="saved-pill">${word}<button type="button" data-remove="${word}" aria-label="Remove ${word}">×</button></span>`).join(''):'<span class="empty-text">Save words here before you generate the next round.</span>'}
  function copyText(text,emptyMessage){if(!text){showToast(emptyMessage);return}if(navigator.clipboard)navigator.clipboard.writeText(text).then(()=>showToast('Copied'));else showToast('Copy not available')}
  function setTimer(seconds){state.timer=seconds;state.remaining=seconds;updateTimer()}
  function updateTimer(){const min=Math.floor(state.remaining/60),sec=String(state.remaining%60).padStart(2,'0');$('timer-display').textContent=`${min}:${sec}`}
  function stopTimer(){clearInterval(state.interval);state.interval=null;state.running=false;$('timer-toggle').textContent='Start'}
  function startTimer(){if(state.running){stopTimer();return}state.running=true;$('timer-toggle').textContent='Pause';state.interval=setInterval(()=>{state.remaining-=1;updateTimer();if(state.remaining<=0){stopTimer();showToast('Time is up')}},1000)}
  document.addEventListener('click',e=>{
    const segBtn=e.target.closest('[data-control] button');
    if(segBtn){const control=segBtn.closest('[data-control]').dataset.control,value=segBtn.dataset.value;if(control==='count')setCount(value);if(control==='difficulty'){state.difficulty=value;state.seen.clear();}if(control==='ageGroup'){state.ageGroup=value;state.seen.clear();if(value==='kids')charLoadKidsWords();else charLoadFullWords();setSeg(control,value);generate();return}if(control==='timer')setTimer(Number(value));if(control!=='count')setSeg(control,value);if(control!=='timer')generate();return}
    const save=e.target.closest('[data-save]');if(save){const word=save.dataset.save;if(state.saved.includes(word))state.saved=state.saved.filter(item=>item!==word);else state.saved.push(word);renderSaved();renderWords();return}
    const remove=e.target.closest('[data-remove]');if(remove){state.saved=state.saved.filter(item=>item!==remove.dataset.remove);renderSaved();renderWords();return}
    const faq=e.target.closest('.faq-q');if(faq)faq.closest('.faq-item').classList.toggle('open');
  });
  picCountInput.addEventListener('input',e=>{const v=parseInt(e.target.value);const invalid=isNaN(v)||v<1||v>50;picCountError.style.display=invalid?'block':'none';picCountInput.style.borderColor=invalid?'#E24B4A':'';if(!invalid){state.count=v;generate()}});
  picCountInput.addEventListener('change',()=>picValidateCount());
  $('more-options-btn').addEventListener('click',e=>{const panel=$('more-options-panel');const open=panel.classList.toggle('open');e.target.setAttribute('aria-expanded',open?'true':'false');e.target.textContent=open?'Fewer options':'More options'});
  $('pic-category').addEventListener('change',e=>{state.category=e.target.value;state.seen.clear();generate()});
  $('generate-btn').addEventListener('click',()=>{if(state.ageGroup==='kids')charLoadKidsWords();else charLoadFullWords();generate()});
  $('copy-btn').addEventListener('click',()=>copyText(state.current.map(item=>item.w).join(', '),'No words to copy'));
  $('copy-saved-btn').addEventListener('click',()=>copyText(state.saved.join(', '),'No saved words'));
  $('print-btn').addEventListener('click',()=>window.print());
  $('clear-btn').addEventListener('click',()=>{state.saved=[];renderSaved();renderWords();showToast('Saved words cleared')});
  $('hide-btn').addEventListener('click',e=>{state.hidden=!state.hidden;e.target.textContent=state.hidden?'Reveal words':'Hide words';renderWords()});
  $('reset-session-btn').addEventListener('click',()=>{state.seen.clear();showToast('Repeat history reset')});
  $('timer-toggle').addEventListener('click',startTimer);
  $('timer-reset').addEventListener('click',()=>{stopTimer();state.remaining=state.timer;updateTimer()});
  generate();renderSaved();updateTimer();
})();

(function bindWordineerMenu(){
  const mega=document.getElementById("mega");
  const hbg=document.querySelector(".hamburger");
  if(!mega||!hbg)return;
  hbg.onclick=null;
  hbg.removeAttribute("onclick");
  hbg.setAttribute("role","button");
  hbg.setAttribute("tabindex","0");
  hbg.setAttribute("aria-controls","mega");
  hbg.setAttribute("aria-expanded",mega.classList.contains("open")?"true":"false");
  function setMenu(open){mega.classList.toggle("open",open);hbg.setAttribute("aria-expanded",open?"true":"false")}
  function toggleMenu(e){e.preventDefault();e.stopPropagation();setMenu(!mega.classList.contains("open"))}
  hbg.addEventListener("click",toggleMenu);
  hbg.addEventListener("keydown",e=>{if(e.key==="Enter"||e.key===" ")toggleMenu(e)});
  document.addEventListener("click",e=>{if(mega.classList.contains("open")&&!mega.contains(e.target)&&!hbg.contains(e.target))setMenu(false)});
})();
</script>
<!-- /SLOT:init -->
```

- [ ] **Step 2: Verify the file exists and CONFIG is valid**

Run: `python3 -c "
import re, json, sys
src = open('template-deploy/tools-src/charades-generator.html').read()
m = re.search(r'<!-- CONFIG\s*(\{.*?\})\s*-->', src, re.DOTALL)
if not m: sys.exit('No CONFIG found')
cfg = json.loads(m.group(1))
print('url:', cfg['url'])
print('output:', cfg['output'])
assert cfg['url'] == '/charades-generator/', 'wrong url'
assert cfg['output'] == 'charades-generator.html', 'wrong output'
print('CONFIG valid')
"`

Expected:
```
url: /charades-generator/
output: charades-generator.html
CONFIG valid
```

- [ ] **Step 3: Commit**

```bash
git add template-deploy/tools-src/charades-generator.html
git commit -m "feat: add charades-generator.html tool source"
```

---

## Task 4: Update tools.json

**Files:**
- Modify: `template-deploy/tools.json`

Three additions needed. The file is at `template-deploy/tools.json`.

- [ ] **Step 1: Add to mega "Games & fun" (line ~61)**

Find this exact block (around line 55–63):
```json
    {
      "cat": "Games &amp; fun",
      "view_all_href": "/number-chance/",
      "tools": [
        { "href": "/random-number-generator/", "text": "Number Generator" },
        { "href": "/coin-flip/", "text": "Flip a Coin" },
        { "href": "/pictionary-phrase-generator/", "text": "Pictionary Phrase Generator" },
        { "href": "/dice-roller/", "text": "Dice Roller" }
      ]
    }
```

Replace it with:
```json
    {
      "cat": "Games &amp; fun",
      "view_all_href": "/number-chance/",
      "tools": [
        { "href": "/random-number-generator/", "text": "Number Generator" },
        { "href": "/coin-flip/", "text": "Flip a Coin" },
        { "href": "/charades-generator/", "text": "Charades Generator" },
        { "href": "/pictionary-phrase-generator/", "text": "Pictionary Phrase Generator" },
        { "href": "/dice-roller/", "text": "Dice Roller" }
      ]
    }
```

- [ ] **Step 2: Add to more_word_tools grid (after the pictionary-word-generator entry ~line 142)**

Find this exact block:
```json
        {
          "href": "/pictionary-word-generator/",
          "name": "Pictionary Word Generator",
          "desc": "Random drawing words for Pictionary rounds.",
          "icon_bg": "#EEF6E8",
      "icon_path": "<path d=\"M2 2.5h9v6H6.5L3.5 11V8.5H2z\" stroke=\"#2F6B1F\" stroke-width=\"1.1\" stroke-linejoin=\"round\"/><path d=\"M8.5 4l.4.8.9.1-.7.6.2.9-.8-.4-.8.4.2-.9-.7-.6.9-.1z\" fill=\"#2F6B1F\"/>"
    },
```

Add immediately after it:
```json
    {
      "href": "/charades-generator/",
      "name": "Charades Generator",
      "desc": "Random charades words and phrases — filter by category, difficulty, and age group.",
      "icon_bg": "#FEF3EE",
      "icon_path": "<circle cx=\"7\" cy=\"5\" r=\"2.5\" stroke=\"#C05621\" stroke-width=\"1.1\"/><path d=\"M3 11c0-2.2 1.8-4 4-4s4 1.8 4 4\" stroke=\"#C05621\" stroke-width=\"1.1\" stroke-linecap=\"round\"/>"
    },
```

- [ ] **Step 3: Add to footer_cols "Games & fun" (around line 423–431)**

Find this exact block:
```json
    {
      "title": "Games &amp; fun",
      "view_all_href": "/number-chance/",
      "links": [
        { "href": "/random-number-generator/", "text": "Number Generator" },
        { "href": "/coin-flip/", "text": "Flip a Coin" },
        { "href": "/pictionary-phrase-generator/", "text": "Pictionary Phrase Generator" },
        { "href": "/dice-roller/", "text": "Dice Roller" }
      ]
    }
```

Replace with:
```json
    {
      "title": "Games &amp; fun",
      "view_all_href": "/number-chance/",
      "links": [
        { "href": "/random-number-generator/", "text": "Number Generator" },
        { "href": "/coin-flip/", "text": "Flip a Coin" },
        { "href": "/charades-generator/", "text": "Charades Generator" },
        { "href": "/pictionary-phrase-generator/", "text": "Pictionary Phrase Generator" },
        { "href": "/dice-roller/", "text": "Dice Roller" }
      ]
    }
```

- [ ] **Step 4: Also add to other_tools "Games & fun" (around line 358–366)**

Find this exact block:
```json
    {
      "cat": "Games &amp; fun",
      "view_all_href": "/number-chance/",
      "icon_path": "<rect x=\"1\" y=\"1\" width=\"4.5\" height=\"4.5\" rx=\"1\" stroke=\"currentColor\" stroke-width=\"1\"/><rect x=\"7.5\" y=\"1\" width=\"4.5\" height=\"4.5\" rx=\"1\" stroke=\"currentColor\" stroke-width=\"1\"/><rect x=\"1\" y=\"7.5\" width=\"4.5\" height=\"4.5\" rx=\"1\" stroke=\"currentColor\" stroke-width=\"1\"/><rect x=\"7.5\" y=\"7.5\" width=\"4.5\" height=\"4.5\" rx=\"1\" stroke=\"currentColor\" stroke-width=\"1\"/>",
      "links": [
        { "href": "/random-number-generator/", "text": "Number Generator" },
        { "href": "/coin-flip/", "text": "Flip a Coin" },
        { "href": "/pictionary-phrase-generator/", "text": "Pictionary Phrase Generator" },
        { "href": "/dice-roller/", "text": "Dice Roller" }
      ]
    }
```

Replace with:
```json
    {
      "cat": "Games &amp; fun",
      "view_all_href": "/number-chance/",
      "icon_path": "<rect x=\"1\" y=\"1\" width=\"4.5\" height=\"4.5\" rx=\"1\" stroke=\"currentColor\" stroke-width=\"1\"/><rect x=\"7.5\" y=\"1\" width=\"4.5\" height=\"4.5\" rx=\"1\" stroke=\"currentColor\" stroke-width=\"1\"/><rect x=\"1\" y=\"7.5\" width=\"4.5\" height=\"4.5\" rx=\"1\" stroke=\"currentColor\" stroke-width=\"1\"/><rect x=\"7.5\" y=\"7.5\" width=\"4.5\" height=\"4.5\" rx=\"1\" stroke=\"currentColor\" stroke-width=\"1\"/>",
      "links": [
        { "href": "/random-number-generator/", "text": "Number Generator" },
        { "href": "/coin-flip/", "text": "Flip a Coin" },
        { "href": "/charades-generator/", "text": "Charades Generator" },
        { "href": "/pictionary-phrase-generator/", "text": "Pictionary Phrase Generator" },
        { "href": "/dice-roller/", "text": "Dice Roller" }
      ]
    }
```

- [ ] **Step 5: Verify tools.json is valid JSON**

Run: `python3 -c "import json; json.load(open('template-deploy/tools.json')); print('tools.json valid')"`

Expected: `tools.json valid`

- [ ] **Step 6: Commit**

```bash
git add template-deploy/tools.json
git commit -m "feat: add charades-generator to tools.json registry (mega, more_word_tools, other_tools, footer)"
```

---

## Task 5: Update _redirects

**Files:**
- Modify: `wordineer-deploy/_redirects`

- [ ] **Step 1: Add redirect**

Append to the end of `wordineer-deploy/_redirects`:
```
/charades-generator.html    /charades-generator/    301
/charades-generator/    /charades-generator.html    200
```

- [ ] **Step 2: Commit**

```bash
git add wordineer-deploy/_redirects
git commit -m "feat: add /charades-generator/ clean URL redirect"
```

---

## Task 6: Build, Copy, and Verify

**Files:**
- Run build: `template-deploy/build.py`
- Copy: `template-deploy/output/charades-generator.html` → `wordineer-deploy/charades-generator.html`

- [ ] **Step 1: Run the build**

```bash
cd template-deploy && python3 build.py
```

Expected: no errors. Output includes `charades-generator.html`.

Verify:
```bash
ls template-deploy/output/charades-generator.html
```

- [ ] **Step 2: Copy to deploy folder**

```bash
cp template-deploy/output/charades-generator.html wordineer-deploy/charades-generator.html
```

- [ ] **Step 3: Copy rebuilt pages that reference tools.json (nav/footer changed)**

Since tools.json changed, all pages with the mega-menu and footer need rebuilding too:

```bash
cp template-deploy/output/*.html wordineer-deploy/
```

- [ ] **Step 4: Start local preview server**

```bash
cd wordineer-deploy && python3 -m http.server 8080
```

- [ ] **Step 5: Verify in browser**

Visit `http://localhost:8080/charades-generator.html` and check:

1. Breadcrumb shows: Wordineer › Word Tools › Charades Generator
2. On load, 5 Easy words appear immediately (SEED)
3. Each word card has a colored category badge (e.g. "ANIMALS", "MOVIES")
4. Age Group seg: All Ages / Kids / Adults all clickable and toggle active state
5. Switching to Kids re-generates with kid-friendly words
6. Difficulty buttons Easy / Medium / Hard work
7. Category dropdown includes all 12 categories; selecting one filters results
8. Timer: selecting 30s/60s/90s updates display; Start counts down; Reset returns to full
9. Copy list puts comma-separated words in clipboard (check with paste)
10. Hide Words blurs all word text; clicking again reveals
11. Save button on a card adds to the Saved tray
12. Print Cards opens print dialog with clean card layout (no nav/controls)
13. Mega-menu includes "Charades Generator" under Games & fun
14. Footer includes "Charades Generator" under Games & fun

- [ ] **Step 6: Commit**

```bash
git add wordineer-deploy/charades-generator.html wordineer-deploy/*.html
git commit -m "build: generate and deploy charades-generator with updated nav/footer"
```

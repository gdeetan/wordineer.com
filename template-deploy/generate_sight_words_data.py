#!/usr/bin/env python3
"""
Generate wordineer-deploy/data/sight-words-data.json
Combines Dolch (315 words) and Fry top 300 (3 groups of 100).
Words on both lists get list="both" with both group fields populated.
Run from repo root: python3 template-deploy/generate_sight_words_data.py
"""
import json, os

DOLCH = {
    "pre-k": [
        "a","and","away","big","blue","can","come","down","find","for",
        "funny","go","help","here","I","in","is","it","jump","little",
        "look","make","me","my","not","one","play","red","run","said",
        "see","the","three","to","two","up","we","where","yellow","you"
    ],
    "kindergarten": [
        "all","am","are","at","ate","be","black","brown","but","came",
        "did","do","eat","four","get","good","have","he","into","like",
        "must","new","no","now","on","our","out","please","pretty","ran",
        "ride","saw","say","she","so","soon","that","there","they","this",
        "too","under","want","was","well","went","what","white","who","will",
        "with","yes"
    ],
    "1st": [
        "after","again","an","any","as","ask","by","could","every","fly",
        "from","give","going","had","has","her","him","his","how","just",
        "know","let","live","may","of","old","once","open","over","put",
        "round","some","stop","take","thank","them","then","think","walk","were",
        "when"
    ],
    "2nd": [
        "always","around","because","been","before","best","both","buy","call","cold",
        "does","don't","fast","first","five","found","gave","goes","green","its",
        "made","many","off","or","pull","read","right","sing","sit","sleep",
        "tell","their","these","those","upon","us","use","very","wash","which",
        "why","wish","work","would","write","your"
    ],
    "3rd": [
        "about","better","bring","carry","clean","cut","done","draw","drink","eight",
        "fall","far","full","got","grow","hold","hot","hurt","if","keep",
        "kind","laugh","light","long","much","myself","never","only","own","pick",
        "seven","shall","show","six","small","start","ten","today","together","try",
        "warm"
    ],
    "nouns": [
        "apple","baby","back","ball","bear","bed","bell","bird","birthday","boat",
        "box","boy","bread","brother","cake","car","cat","chair","chicken","children",
        "Christmas","coat","corn","cow","day","dog","doll","door","duck","egg",
        "eye","farm","farmer","father","feet","fire","fish","floor","flower","fly",
        "foot","game","garden","girl","goodbye","grass","ground","hand","head","hill",
        "home","horse","house","kitty","leg","letter","man","men","milk","money",
        "morning","mother","name","nest","night","paper","party","picture","pig","rain",
        "ring","robin","school","seed","sheep","shoe","sister","snow","song","squirrel",
        "stick","street","sun","table","thing","time","top","toy","tree","watch",
        "water","wind","window","wood"
    ]
}

FRY = {
    "1-100": [
        "a","about","all","am","an","and","are","as","at","be",
        "been","but","by","called","can","come","could","day","did","do",
        "down","each","find","first","for","from","get","go","had","has",
        "have","he","her","him","his","how","I","if","in","into",
        "is","it","its","like","long","look","made","make","many","may",
        "more","my","no","not","now","number","of","on","one","or",
        "other","out","part","people","said","see","she","so","some","than",
        "that","the","their","them","then","there","these","they","this","time",
        "to","two","up","use","was","water","way","we","were","what",
        "when","which","who","will","with","words","would","write","you","your"
    ],
    "101-200": [
        "after","again","air","also","America","animal","another","answer","any","around",
        "ask","away","back","because","before","big","boy","came","change","different",
        "does","end","even","follow","form","found","give","good","great","hand",
        "help","here","home","house","just","kind","know","land","large","learn",
        "letter","line","little","live","man","me","means","men","most","mother",
        "move","much","must","name","need","new","off","old","only","our",
        "over","page","picture","place","play","point","put","read","right","same",
        "say","sentence","set","should","show","small","sound","spell","still","study",
        "such","take","tell","things","think","three","through","too","try","turn",
        "us","very","want","well","went","where","why","work","world","years"
    ],
    "201-300": [
        "below","between","book","both","car","carry","children","city","close","country",
        "don't","earth","enough","ever","every","example","eye","face","family","far",
        "feet","food","four","gave","going","group","grow","hard","head","high",
        "idea","important","Indian","keep","last","late","left","life","light","might",
        "mile","miss","mountain","near","never","next","night","often","once","open",
        "own","plant","real","river","run","saw","second","seem","side","something",
        "sometimes","song","soon","start","state","stop","story","talk","those","thought",
        "together","took","tree","under","until","upon","walk","watch","while","white",
        "without","young","above","across","along","began","being","beside","black","built",
        "during","early","five","girl","hands","hear","list","map","road","school"
    ]
}

# Build word → dolch_group lookup
dolch_lookup = {}
for grp, words in DOLCH.items():
    for w in words:
        dolch_lookup[w.lower()] = grp

# Build word → fry_group + fry_rank lookup
fry_lookup = {}
for grp, words in FRY.items():
    for i, w in enumerate(words):
        key = w.lower()
        if grp == "1-100":
            rank = i + 1
        elif grp == "101-200":
            rank = i + 101
        else:
            rank = i + 201
        fry_lookup[key] = {"fry_group": grp, "fry_rank": rank}

# Merge
seen = {}
entries = []

def add(word, dolch_group, fry_group, fry_rank):
    key = word.lower()
    e = {
        "word":        word,
        "list":        "both" if (dolch_group and fry_group) else ("dolch" if dolch_group else "fry"),
        "dolch_group": dolch_group,
        "fry_group":   fry_group,
        "fry_rank":    fry_rank
    }
    seen[key] = e
    entries.append(e)

# Add all Dolch words first
for grp, words in DOLCH.items():
    for w in words:
        key = w.lower()
        fd = fry_lookup.get(key, {})
        add(w, grp, fd.get("fry_group"), fd.get("fry_rank"))

# Add Fry words not yet in the list
for grp, words in FRY.items():
    for w in words:
        key = w.lower()
        fd = fry_lookup[key]
        if key not in seen:
            add(w, dolch_lookup.get(key), fd["fry_group"], fd["fry_rank"])
        else:
            e = seen[key]
            if not e.get("fry_group"):
                e["fry_group"] = fd["fry_group"]
                e["fry_rank"]  = fd["fry_rank"]
                e["list"] = "both" if e.get("dolch_group") else "fry"

# Sanity-check source list sizes
dolch_total = sum(len(v) for v in DOLCH.values())
fry_total   = sum(len(v) for v in FRY.values())
assert fry_total == 300, f"Expected 300 Fry words, got {fry_total}"
print(f"Source counts — Dolch: {dolch_total}, Fry: {fry_total}")

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../wordineer-deploy/data/sight-words-data.json")
with open(out_path, "w") as f:
    json.dump(entries, f, indent=2)

print(f"Generated {len(entries)} entries → {out_path}")
dolch_count = sum(1 for e in entries if e["list"] in ("dolch","both"))
fry_count   = sum(1 for e in entries if e["list"] in ("fry","both"))
both_count  = sum(1 for e in entries if e["list"] == "both")
print(f"  Dolch words (incl. both): {dolch_count}")
print(f"  Fry words (incl. both):   {fry_count}")
print(f"  On both lists:             {both_count}")

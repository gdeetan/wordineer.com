#!/usr/bin/env python3
"""
Expands words.json from ~2,082 to ~10,000 entries using NLTK WordNet + wordfreq.
Outputs words_expanded.json and expansion_report.txt.
"""

import json
import re
import sys
import subprocess
from pathlib import Path
from collections import defaultdict
from typing import Optional, List, Dict

# ---------------------------------------------------------------------------
# Dependency bootstrap
# ---------------------------------------------------------------------------

def pip_install(pkg):
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", pkg])

try:
    import nltk
except ImportError:
    pip_install("nltk")
    import nltk

try:
    from wordfreq import zipf_frequency
except ImportError:
    pip_install("wordfreq")
    from wordfreq import zipf_frequency

# Download required NLTK data silently
for resource in ["wordnet", "omw-1.4"]:
    try:
        nltk.data.find(f"corpora/{resource}")
    except LookupError:
        nltk.download(resource, quiet=True)

from nltk.corpus import wordnet as wn

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

BASE_DIR = Path(__file__).parent
INPUT_FILE  = BASE_DIR / "words.json"
OUTPUT_FILE = BASE_DIR / "words_expanded.json"
REPORT_FILE = BASE_DIR / "expansion_report.txt"

TARGET_TOTAL = 10_000

# POS targets (new words to add per type)
TYPE_TARGETS = {
    "noun":      4500,
    "adjective": 2200,
    "verb":      2100,
    "adverb":    1200,
}

DIFF_TARGETS = {"easy": 2500, "medium": 4000, "hard": 3500}

# wordfreq Zipf thresholds  (higher = more frequent)
# Zipf ≥ 5.0 → top ~2 000 words  → easy
# Zipf 3.5–4.99 → ~next 6 000 → medium
# Zipf < 3.5 → rare → hard
EASY_THRESHOLD   = 5.0
MEDIUM_THRESHOLD = 3.5

# Known loanword set (curated — expand as needed)
LOANWORDS: set[str] = {
    # German
    "angst","doppelganger","ersatz","fahrenheit","gestalt","hamburger","kindergarten",
    "kitsch","leitmotif","poltergeist","pretzel","rucksack","schadenfreude","spiel",
    "uber","wanderlust","weltanschauung","wiener","zeitgeist","blitz","bratwurst",
    "delicatessen","dachshund","diktat","flak","frank","gemutlich","kaput","noodle",
    "poodle","pumpernickel","quartz","sauerkraut","schnapps","seltzer","strafe",
    "waltz","wunderkind","zinnia","zither",
    # French
    "ennui","genre","ballet","bouquet","buffet","bureau","cabaret","cafe","camouflage",
    "carton","chauffeur","chic","cliche","clique","colonel","coquette","corsage",
    "coupon","critique","croissant","cuisine","debut","decor","detour","dossier",
    "elite","encore","entrepreneur","envelope","etiquette","facade","fiancee","flair",
    "fondue","garage","gazette","gourmet","hotel","intrigue","jargon","liaison",
    "limousine","mauve","menu","milieu","naive","niche","nuance","passe","plateau",
    "prestige","rapport","regime","renaissance","repertoire","restaurant","rouge",
    "silhouette","souvenir","suite","tableau","terrain","unique","vague","vignette",
    "voila","voyage","carte blanche","deja vu","bon vivant","raison detre",
    "laissez faire","avant garde","joie de vivre","faux pas","coup de grace",
    "force majeure","fait accompli","beau monde","bonhomie","potpourri","revue",
    "sabotage","salon","soiree","triage","velour","brunette","chaise","champagne",
    "charade","chardonnay","chateau","chauvinism","creme","depot","echelon",
    "entourage","espionage","finesse","flaneur","foyer","fracas","fuselage",
    "impasse","macabre","mademoiselle","manoeuvre","moustache","palette","parole",
    "pastiche","petite","plaque","premiere","prose","protege","rendezvous",
    "risque","rogue","rouge","roulette","sachet","sauté","sorbet","suede","touche",
    # Spanish/Portuguese
    "alligator","armadillo","avocado","barbeque","bonanza","cargo","cigar","cocoa",
    "condor","desperado","embargo","fiesta","flamingo","guerrilla","hammock",
    "hurricane","junta","llama","macho","mosquito","mustang","patio","plaza",
    "poncho","potato","ranch","salsa","siesta","sombrero","stampede","tango",
    "tomato","tornado","vanilla","vigilante","yucca","aficionado","bonito",
    "bravado","cabana","cafeteria","cannibal","canyon","caramel","casino",
    "coyote","enchilada","hacienda","indigo","lasso","machete","mango","oregano",
    "papaya","paprika","pimento","pueblo","tobacco",
    # Italian
    "alarm","alert","ballot","broccoli","bronze","cameo","casino","cello","cupola",
    "fresco","ghetto","gondola","grotto","influenza","lava","macaroni","maestro",
    "malaria","manifesto","miniature","motto","opera","panorama","piano","piazza",
    "pizza","portfolio","quartet","replica","scenario","soprano","stanza","studio",
    "tempo","torso","umbrella","vendetta","villa","violin","volcano","zucchini",
    "allegro","alto","arcade","aria","balcony","bandit","bravura","cadenza",
    "cantata","cappella","casino","concerto","diva","duo","espresso","falsetto",
    "finale","forte","graffiti","imbroglio","impresario","lagoon","lotto","mafia",
    "mafioso","mezzo","motto","paparazzi","paparazzo","parmesan","pasta","piazza",
    "piccolo","pronto","regatta","sepia","soprano","stucco","terra cotta","tirade",
    "torso","virtuoso",
    # Japanese
    "anime","bonsai","emoji","geisha","haiku","honcho","judo","karaoke","karate",
    "kimono","manga","ninja","origami","ramen","sake","samurai","sushi","tofu",
    "tsunami","tycoon","zen","futon","geisha","hibachi","ikebana","kamikaze",
    "katana","koi","kudos","ninjutsu","rickshaw","shogun","sumo","tempura",
    "teriyaki","typhoon","umami","wasabi","yakuza",
    # Arabic
    "alcohol","algebra","algorithm","almanac","amalgam","assassin","azure","candy",
    "cipher","coffee","cotton","elixir","ghoul","hazard","jar","lemon","magazine",
    "mattress","monsoon","nadir","orange","safari","sequin","sherbet","sirup",
    "sofa","spinach","sugar","syrup","tambourine","tarragon","zenith","zero",
    "admiral","alchemy","alkali","arabesque","arsenal","artichoke","azure",
    "bedouin","calibre","caraway","carmine","checkmate","cipher","crimson",
    "drugstore","gauze","giraffe","henna","lacquer","lute","marzipan","massage",
    "ottoman","racket","realgar","saffron","salve","talc","tariff","vizier",
    # Other
    "avatar","bungalow","jungle","loot","pundit","shampoo","thug","yoga",  # Hindi/Sanskrit
    "amok","batik","bamboo","ketchup","sarong","gecko",  # Malay
    "ski","fjord","troll","slalom","lemming",  # Norse/Norwegian
    "ombudsman","smorgasbord","tungsten",  # Swedish
    "sauna","tundra",  # Finnish
    "intelligentsia","sputnik","mammoth","vodka","taiga",  # Russian
    "chutzpah","maven","mensch","schlep","schmooze","shtick","glitch","klutz",  # Yiddish
    "taboo","tattoo","ukulele",  # Polynesian/Hawaiian
    "igloo","kayak","parka",  # Inuit
    "chocolate","cacao","chilli","tomato",  # Nahuatl
    "banana","yam",  # West African
    "boomerang","kangaroo","wombat",  # Australian Aboriginal
}

# Vulgar/offensive blocklist (lowercase)
BLOCKLIST: set[str] = {
    "bastard","bitch","cock","cunt","damn","dick","fuck","nigger","pussy",
    "shit","slut","whore","ass","arse","prick","twat","wanker","bollocks",
    "motherfucker","asshole","arsehole","faggot","retard","crap",
}

# Very obscure scientific/Latin jargon patterns to skip
JARGON_PATTERNS = re.compile(
    r"^[A-Z][a-z]+ [a-z]+$"   # Binomial nomenclature
)

WN_POS_MAP = {
    wn.NOUN: "noun",
    wn.VERB: "verb",
    wn.ADJ:  "adjective",
    wn.ADV:  "adverb",
}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def title_case(word: str) -> str:
    return " ".join(part.capitalize() for part in word.split())


def assign_difficulty(word: str) -> str:
    freq = zipf_frequency(word.lower(), "en")
    if freq >= EASY_THRESHOLD:
        return "easy"
    elif freq >= MEDIUM_THRESHOLD:
        return "medium"
    else:
        return "hard"


def is_borrowed(word: str) -> bool:
    return word.lower() in LOANWORDS


def clean_definition(raw: str, word: str) -> Optional[str]:
    """Clean a WordNet definition; return None if it should be skipped."""
    d = raw.strip()

    # Remove trailing period
    if d.endswith("."):
        d = d[:-1]

    # Lowercase first letter
    d = d[:1].lower() + d[1:] if d else d

    # Strip leading articles
    d = re.sub(r"^(a|an|the) ", "", d)

    # Remove parenthetical examples like "(often used in combination)"
    d = re.sub(r"\(.*?\)", "", d).strip()
    d = re.sub(r"\s{2,}", " ", d)

    # Skip empty
    if not d:
        return None

    # Truncate if too long (> 20 words)
    words_in_def = d.split()
    if len(words_in_def) > 20:
        d = " ".join(words_in_def[:18]).rstrip(",;:")

    # Remove trailing period again after truncation
    if d.endswith("."):
        d = d[:-1]

    return d


def is_valid_word(lemma_name: str) -> bool:
    """Return True if the lemma string is a usable single English word."""
    # No underscores (multi-word in WordNet)
    if "_" in lemma_name:
        return False
    # No hyphens
    if "-" in lemma_name:
        return False
    # Must be alphabetic only
    if not lemma_name.isalpha():
        return False
    # Min length
    if len(lemma_name) < 2:
        return False
    # Blocklist
    if lemma_name.lower() in BLOCKLIST:
        return False
    # Looks like a proper noun (starts uppercase in WordNet)
    if lemma_name[0].isupper():
        return False
    # Binomial / scientific jargon
    if JARGON_PATTERNS.match(lemma_name):
        return False
    return True


def get_best_definition(synsets, word: str) -> Optional[str]:
    """Pick the best definition from a list of synsets for the given word."""
    for ss in synsets:
        raw = ss.definition()
        cleaned = clean_definition(raw, word)
        if cleaned and word.lower() not in cleaned.lower():
            return cleaned
    # Fallback: allow definitions that contain the word
    for ss in synsets:
        raw = ss.definition()
        cleaned = clean_definition(raw, word)
        if cleaned:
            return cleaned
    return None


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    report_lines: List[str] = []
    flagged: List[Dict] = []

    # 1. Load existing words
    with open(INPUT_FILE, encoding="utf-8") as f:
        existing: list[dict] = json.load(f)

    existing_words_lower: set[str] = {e["w"].lower() for e in existing}
    print(f"Loaded {len(existing)} existing words.")
    report_lines.append(f"Existing words loaded: {len(existing)}")

    # Count current distribution
    current_by_type: dict[str, int] = defaultdict(int)
    for e in existing:
        current_by_type[e["t"]] += 1

    report_lines.append("Current type distribution:")
    for t, c in sorted(current_by_type.items()):
        report_lines.append(f"  {t}: {c}")

    # 2. Calculate how many of each type we still need
    need_by_type: Dict[str, int] = {}
    for t, target in TYPE_TARGETS.items():
        need_by_type[t] = max(0, target - current_by_type.get(t, 0))

    print("Need to add:")
    for t, n in need_by_type.items():
        print(f"  {t}: {n}")

    # 3. Iterate WordNet and collect candidates
    new_entries: list[dict] = []
    seen_lower: set[str] = set(existing_words_lower)  # mutable copy for dedup

    added_by_type: dict[str, int] = defaultdict(int)

    # We iterate all synsets grouped by POS
    wn_pos_list = [
        (wn.NOUN, "noun"),
        (wn.ADJ,  "adjective"),
        (wn.VERB, "verb"),
        (wn.ADV,  "adverb"),
    ]

    for wn_pos, pos_label in wn_pos_list:
        still_needed = need_by_type[pos_label]
        if still_needed <= 0:
            continue

        print(f"Collecting {pos_label}s from WordNet (need {still_needed})...")

        synsets_for_pos = list(wn.all_synsets(wn_pos))

        # Build word → synset list map
        word_to_synsets: dict[str, list] = defaultdict(list)
        for ss in synsets_for_pos:
            for lemma in ss.lemmas():
                lname = lemma.name()
                if is_valid_word(lname):
                    word_to_synsets[lname].append(ss)

        # Sort by frequency (most common first) for better quality
        sorted_words = sorted(
            word_to_synsets.keys(),
            key=lambda w: zipf_frequency(w, "en"),
            reverse=True,
        )

        for w in sorted_words:
            if added_by_type[pos_label] >= still_needed:
                break

            if w.lower() in seen_lower:
                continue

            definition = get_best_definition(word_to_synsets[w], w)
            if not definition:
                continue

            # Check if definition contains the word (flag for review)
            contains_self = w.lower() in definition.lower()

            diff = assign_difficulty(w)
            borrowed = is_borrowed(w)

            entry = {
                "w": title_case(w),
                "t": pos_label,
                "d": definition,
                "diff": diff,
                "borrowed": borrowed,
            }

            new_entries.append(entry)
            seen_lower.add(w.lower())
            added_by_type[pos_label] += 1

            if contains_self:
                flagged.append({"word": title_case(w), "reason": "definition contains the word itself", "definition": definition})

        print(f"  Added {added_by_type[pos_label]} {pos_label}s")

    # 4. Merge and sort
    all_entries = existing + new_entries
    all_entries.sort(key=lambda e: e["w"].lower())

    print(f"\nTotal words after expansion: {len(all_entries)}")

    # 5. Validate
    print("Running validation...")
    valid_types  = {"noun", "verb", "adjective", "adverb"}
    valid_diffs  = {"easy", "medium", "hard"}
    errors: list[str] = []

    for i, entry in enumerate(all_entries):
        w = entry.get("w", "")
        t = entry.get("t", "")
        d = entry.get("d", "")
        diff = entry.get("diff", "")
        borrowed = entry.get("borrowed")

        if not all(k in entry for k in ("w","t","d","diff","borrowed")):
            errors.append(f"[{i}] {w}: missing field(s)")
        if t not in valid_types:
            errors.append(f"[{i}] {w}: invalid type '{t}'")
        if diff not in valid_diffs:
            errors.append(f"[{i}] {w}: invalid diff '{diff}'")
        if not w or w[0] != w[0].upper():
            errors.append(f"[{i}] {w}: not Title Case")
        if not d:
            errors.append(f"[{i}] {w}: empty definition")
        if d.endswith("."):
            errors.append(f"[{i}] {w}: definition ends with period")
        if borrowed is None:
            errors.append(f"[{i}] {w}: 'borrowed' field is null")

    if errors:
        print(f"Validation errors: {len(errors)}")
        for e in errors[:20]:
            print(f"  {e}")
    else:
        print("Validation passed — no errors.")

    # 6. Write output
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_entries, f, ensure_ascii=False, indent=2)
    print(f"Written: {OUTPUT_FILE}")

    # 7. Build report
    final_by_type:  dict[str, int] = defaultdict(int)
    final_by_diff:  dict[str, int] = defaultdict(int)
    final_borrowed  = 0

    for e in all_entries:
        final_by_type[e["t"]] += 1
        final_by_diff[e["diff"]] += 1
        if e.get("borrowed"):
            final_borrowed += 1

    report_lines += [
        "",
        "=" * 50,
        f"FINAL WORD COUNT: {len(all_entries)}",
        "=" * 50,
        "",
        "By part of speech:",
        *[f"  {t}: {final_by_type[t]} (target {TYPE_TARGETS.get(t, '?')})" for t in ["noun","adjective","verb","adverb"]],
        "",
        "By difficulty:",
        *[f"  {d}: {final_by_diff[d]} (target {DIFF_TARGETS.get(d, '?')})" for d in ["easy","medium","hard"]],
        "",
        f"Borrowed/loanwords: {final_borrowed} (target 500)",
        "",
        f"New words added: {len(new_entries)}",
        "",
    ]

    if errors:
        report_lines += ["VALIDATION ERRORS:", *errors[:100], ""]

    if flagged:
        report_lines += [
            f"FLAGGED FOR REVIEW ({len(flagged)} entries — definition contains the word):",
            *[f"  {f['word']}: {f['definition']}" for f in flagged[:100]],
        ]

    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))
    print(f"Report written: {REPORT_FILE}")


if __name__ == "__main__":
    main()

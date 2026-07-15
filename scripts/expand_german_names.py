#!/usr/bin/env python3
import json
import re
import urllib.request
from collections import OrderedDict
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_PATH = ROOT / "data" / "german-names.json"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; WordineerDatasetBuilder/1.0; +https://wordineer.com)"
}

GIVEN_SOURCES = [
    ("https://www.behindthename.com/names/usage/german", {"general"}),
    ("https://www.behindthename.com/names/usage/german-austrian", {"austrian-influenced", "general"}),
    ("https://www.behindthename.com/names/usage/german-swiss", {"swiss-influenced", "general"}),
    ("https://www.behindthename.com/names/usage/low-german", {"northern", "general"}),
    ("https://www.behindthename.com/names/usage/upper-german", {"bavarian-southern", "general"})
]

SURNAME_SOURCES = [
    ("https://surnames.behindthename.com/names/usage/german", {"general"}),
    ("https://surnames.behindthename.com/names/usage/upper-german", {"bavarian-southern", "general"}),
    ("https://surnames.behindthename.com/names/usage/german-swiss", {"swiss-influenced", "general"})
]

BLOCK_RE = re.compile(r'<div class="browsename">(.*?)</div>', re.S)
TAG_RE = re.compile(r"<[^>]+>")
NAME_RE = re.compile(r'<span class="listname"><a [^>]*>(.*?)</a></span>', re.S)
GENDER_RE = re.compile(r'<span class="listgender">.*?<span class="(masc|fem|unisex)"', re.S)
USAGE_RE = re.compile(r'<span class="listusage">(.*?)</span>', re.S)
MNG_RE = re.compile(r'<span class="mng">(.*?)</span>', re.S)

GERMAN_SEED = {
    "Ada", "Adele", "Amalia", "Anna", "Anneliese", "Anton", "Benedikt", "Bernhard", "Bruno",
    "Clara", "Conrad", "Dieter", "Elias", "Elise", "Emil", "Emilia", "Emma", "Erich", "Eva",
    "Felix", "Florian", "Franz", "Franziska", "Frieda", "Friedrich", "Georg", "Gerhard", "Greta",
    "Hannah", "Hans", "Heidi", "Heinrich", "Helene", "Ida", "Ingrid", "Jakob", "Jannik",
    "Johann", "Johanna", "Johannes", "Jonas", "Josef", "Josefine", "Karl", "Kilian", "Klara",
    "Klaus", "Konrad", "Lara", "Lea", "Lena", "Leon", "Leonie", "Leopold", "Liesel", "Lina",
    "Linus", "Lotta", "Luisa", "Lukas", "Magdalena", "Magnus", "Marlene", "Mathilda", "Matthias",
    "Maximilian", "Mia", "Moritz", "Nele", "Nina", "Niklas", "Oskar", "Otto", "Paul", "Paula",
    "Romy", "Sabine", "Sebastian", "Sophie", "Stefan", "Thea", "Theo", "Theresa", "Thomas",
    "Tobias", "Valentin", "Viktoria", "Walter", "Wilhelm", "Wilhelmine", "Elsa"
}

STRONG_CLUSTERS = ("hard", "helm", "wolf", "ward", "bert", "brand", "fried", "ger", "karl", "konr", "wil", "wald", "sieg")
SOFT_ENDINGS = ("a", "ia", "ie", "ina", "ine", "ella", "ette", "lina", "ora", "e")
ELEGANT_ENDINGS = ("ine", "ina", "ette", "elle", "old", "bert", "fried", "mund", "wald", "liese")


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=20) as res:
        return res.read().decode("utf-8", "ignore")


def strip_tags(value: str) -> str:
    text = TAG_RE.sub("", value)
    return re.sub(r"\s+", " ", unescape(text)).strip()


def normalize_name(value: str) -> str:
    value = strip_tags(value)
    return re.sub(r"\s+\d+$", "", value).strip()


def clean_sentence(text: str, limit: int = 110) -> str:
    text = strip_tags(text)
    text = re.sub(r'\s+', ' ', text).strip()
    if not text:
        return ""
    if len(text) > limit:
        clipped = text[:limit].rsplit(" ", 1)[0].rstrip(",;:")
        return clipped + "..."
    return text


def first_sentence(text: str, limit: int = 110) -> str:
    text = strip_tags(text)
    parts = re.split(r'(?<=[.!?])\s+', text)
    return clean_sentence(parts[0], limit=limit)


def body_after_break(block: str) -> str:
    parts = re.split(r'<br\s*/?>', block, maxsplit=1, flags=re.I)
    return parts[1] if len(parts) > 1 else block


def extract_note(block: str, limit: int = 108) -> str:
    meanings = [strip_tags(x).strip('" ') for x in MNG_RE.findall(block)]
    if meanings:
        joined = "; ".join(dict.fromkeys([m for m in meanings if m]))
        return clean_sentence(joined, limit=limit)
    body = body_after_break(block)
    return clean_sentence(first_sentence(body, limit=limit), limit=limit)


def scrape_blocks(base_url: str):
    page = 1
    while True:
        url = base_url if page == 1 else f"{base_url}/{page}"
        html = fetch(url)
        blocks = BLOCK_RE.findall(html)
        if not blocks:
            break
        for block in blocks:
            yield block
        page += 1


def classify_name_shape(name: str):
    lower = name.lower()
    tone = []
    if any(cluster in lower for cluster in STRONG_CLUSTERS) or sum(ch in "kbdgtrw" for ch in lower) >= max(2, len(lower) // 3):
        tone.append("strong")
    if lower.endswith(SOFT_ENDINGS):
        tone.append("soft")
    if lower.endswith(ELEGANT_ENDINGS) or len(name) >= 8:
        tone.append("elegant")
    if not tone:
        tone.append("soft" if lower.endswith(("n", "s", "l")) else "strong")
    deduped = []
    for item in tone:
        if item not in deduped:
            deduped.append(item)
    return deduped[:2]


def classify_given_styles(name: str, usage_text: str, note: str):
    styles = []
    lower_note = note.lower()
    lower_usage = usage_text.lower()
    lower_name = name.lower()

    if name in GERMAN_SEED:
        if name in {"Emma", "Mia", "Lena", "Leon", "Noah", "Elias", "Theo", "Mila"}:
            styles.append("modern")
        else:
            styles.append("classic")
    elif "rare" in lower_usage or "old german" in lower_note or "medieval" in lower_note or "saint" in lower_note:
        styles.extend(["traditional", "classic"])
    elif any(term in lower_note for term in ("short form", "diminutive", "variant", "combination")):
        styles.append("modern")
    else:
        styles.append("classic")

    if "traditional" not in styles and any(term in lower_note for term in ("derived from the old german", "old high german", "frankish")):
        styles.append("traditional")

    for tone in classify_name_shape(name):
        if tone not in styles:
            styles.append(tone)

    if "modern" not in styles and len(lower_name) <= 4 and "traditional" not in styles:
        styles.append("modern")

    out = []
    for item in styles:
        if item not in out:
            out.append(item)
    return out[:3]


def classify_surname_category(note: str):
    lower = note.lower()
    if any(term in lower for term in ("occupational name", "occupation", "maker", "herder", "judge", "scribe", "carpenter", "baker", "smith", "weaver", "wagon", "miller", "cook", "tailor", "shepherd", "fisher", "innkeeper")):
        return "occupational"
    if any(term in lower for term in ("patronymic", "derived from the given name", "from the given name", "means \"son of", "son of", "family of")):
        return "patronymic"
    if any(term in lower for term in ("topographic", "lived near", "from the name of", "from a place name", "from german", "denotes somebody from", "denoted somebody from", "dwelled near", "mountain", "hill", "field", "forest", "brook", "valley", "street", "corner", "farmstead", "river", "marsh")):
        return "topographic"
    return "descriptive"


def classify_surname_styles(name: str, category: str):
    styles = []
    if category == "occupational":
        styles.extend(["traditional", "strong"])
    elif category == "topographic":
        styles.extend(["classic", "elegant"])
    elif category == "patronymic":
        styles.extend(["classic", "soft"])
    else:
        styles.extend(["classic", "strong"])

    lower = name.lower()
    if lower.endswith(("mann", "hardt", "berg", "wald", "stein")) and "strong" not in styles:
        styles.append("strong")
    if lower.endswith(("er", "ner", "ler")) and "traditional" not in styles:
        styles.append("traditional")
    if lower.endswith(("lein", "li", "el", "e")) and "soft" not in styles:
        styles.append("soft")

    out = []
    for item in styles:
        if item not in out:
            out.append(item)
    return out[:3]


def merge_regions(existing, incoming):
    order = ["general", "bavarian-southern", "northern", "austrian-influenced", "swiss-influenced"]
    values = set(existing) | set(incoming)
    return [item for item in order if item in values]


def scrape_given():
    given = OrderedDict()
    for base_url, regions in GIVEN_SOURCES:
        for block in scrape_blocks(base_url):
            name_match = NAME_RE.search(block)
            gender_match = GENDER_RE.search(block)
            usage_match = USAGE_RE.search(block)
            if not name_match or not gender_match:
                continue
            gender = {"masc": "m", "fem": "f", "unisex": "u"}[gender_match.group(1)]
            if gender == "u":
                continue
            name = normalize_name(name_match.group(1))
            usage_text = strip_tags(usage_match.group(1) if usage_match else "")
            note = extract_note(block, limit=104)
            if not note:
                continue
            styles = classify_given_styles(name, usage_text, note)
            key = (name, gender)
            if key not in given:
                given[key] = {
                    "name": name,
                    "gender": gender,
                    "styles": styles,
                    "regions": list(regions),
                    "meaning": note
                }
            else:
                given[key]["regions"] = merge_regions(given[key]["regions"], regions)
                for style in styles:
                    if style not in given[key]["styles"]:
                        given[key]["styles"].append(style)
                if len(given[key]["meaning"]) > len(note):
                    given[key]["meaning"] = note
    return list(given.values())


def scrape_surnames():
    surnames = OrderedDict()
    for base_url, regions in SURNAME_SOURCES:
        for block in scrape_blocks(base_url):
            name_match = NAME_RE.search(block)
            if not name_match:
                continue
            name = normalize_name(name_match.group(1))
            note = extract_note(block, limit=108)
            if not note:
                continue
            category = classify_surname_category(note)
            styles = classify_surname_styles(name, category)
            key = name
            if key not in surnames:
                surnames[key] = {
                    "name": name,
                    "categories": [category],
                    "styles": styles,
                    "regions": list(regions),
                    "meaning": note
                }
            else:
                surnames[key]["regions"] = merge_regions(surnames[key]["regions"], regions)
                if category not in surnames[key]["categories"]:
                    surnames[key]["categories"].append(category)
                for style in styles:
                    if style not in surnames[key]["styles"]:
                        surnames[key]["styles"].append(style)
                if len(surnames[key]["meaning"]) > len(note):
                    surnames[key]["meaning"] = note
    return list(surnames.values())


def score_given(entry):
    score = 0
    if "general" in entry["regions"]:
        score += 6
    if "classic" in entry["styles"]:
        score += 3
    if "modern" in entry["styles"]:
        score += 2
    if entry["name"] in GERMAN_SEED:
        score += 8
    if "traditional" in entry["styles"]:
        score += 2
    score -= max(0, len(entry["meaning"]) - 60) * 0.03
    return (-score, entry["name"])


def score_surname(entry):
    score = 0
    if "general" in entry["regions"]:
        score += 6
    if "occupational" in entry["categories"]:
        score += 3
    if "topographic" in entry["categories"]:
        score += 2
    score -= max(0, len(entry["meaning"]) - 60) * 0.03
    return (-score, entry["name"])


def trim_and_balance(given, surnames):
    given_sorted = sorted(given, key=score_given)
    surnames_sorted = sorted(surnames, key=score_surname)

    # Keep the dataset within the requested 1000-1300 range while preserving a large, balanced given-name pool.
    target_given = min(900, len(given_sorted))
    target_surnames = min(320, len(surnames_sorted))
    total = target_given + target_surnames
    if total > 1300:
        overflow = total - 1300
        target_given -= min(overflow, max(0, target_given - 750))
        overflow = target_given + target_surnames - 1300
        if overflow > 0:
            target_surnames -= overflow

    selected_given = given_sorted[:target_given]
    selected_surnames = surnames_sorted[:target_surnames]

    given_output = [
        [entry["name"], entry["gender"], entry["styles"][:3], entry["regions"][:3], entry["meaning"]]
        for entry in selected_given
    ]
    surname_output = [
        [entry["name"], entry["categories"][:2], entry["styles"][:3], entry["regions"][:3], entry["meaning"]]
        for entry in selected_surnames
    ]
    return given_output, surname_output


def main():
    given = scrape_given()
    surnames = scrape_surnames()
    given_output, surname_output = trim_and_balance(given, surnames)
    payload = {"given": given_output, "surnames": surname_output}
    OUT_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {len(given_output)} given names and {len(surname_output)} surnames to {OUT_PATH}")


if __name__ == "__main__":
    main()

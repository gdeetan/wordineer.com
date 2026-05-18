#!/usr/bin/env python3
"""Generate the Turkish names dataset used by the Random Turkish Name Generator.

Sources:
- Wiktionary category members and extracts for Turkish male/female/unisex given names
- Wiktionary category members and extracts for Turkish surnames
- Forebears Turkey surname rankings for high-frequency surname coverage
"""

from __future__ import annotations

import html
import json
import random
import re
import sys
import time
import unicodedata
import urllib.parse
import urllib.request
from urllib.error import HTTPError
from pathlib import Path


ROOT = Path(__file__).resolve().parent
OUT_PATH = ROOT / "turkish-names.json"

RNG = random.Random(17)
USER_AGENT = "Mozilla/5.0 (Wordineer dataset builder)"

GIVEN_TARGETS = {"m": 370, "f": 370, "u": 60}
SURNAME_TARGET = 450

THEME_KEYWORDS = {
    "nature": [
        "water", "sea", "river", "rain", "wind", "flower", "rose", "tree", "leaf",
        "mountain", "earth", "cloud", "sky", "moon", "sun", "star", "forest", "spring",
        "falcon", "hawk", "lion", "wolf", "bird", "deer", "storm", "dawn", "dew",
    ],
    "strength": [
        "brave", "strong", "power", "warrior", "hero", "iron", "steel", "sword",
        "battle", "falcon", "wolf", "lion", "thunder", "unyielding", "firm", "hardy",
        "courage", "resolute", "victory",
    ],
    "beauty": [
        "beautiful", "beauty", "lovely", "grace", "delicate", "gentle", "charming",
        "elegant", "pretty", "fragrance", "melody", "song", "pearl", "blossom",
    ],
    "virtue": [
        "honest", "just", "pure", "kind", "good", "wise", "calm", "patient", "truth",
        "noble", "generous", "clean", "clear", "dignified", "modest", "humble",
    ],
    "light": [
        "light", "bright", "radiant", "shining", "glow", "luminous", "torch",
        "illumin", "sun", "dawn",
    ],
    "sky-sea": [
        "moon", "star", "sky", "sea", "ocean", "water", "wind", "cloud", "rain", "storm",
    ],
    "royalty": [
        "queen", "king", "prince", "princess", "ruler", "leader", "lord", "crown",
        "emperor", "sultan", "royal",
    ],
    "faith": [
        "god", "allah", "faith", "holy", "saint", "blessed", "religion", "spirit",
        "prayer", "worship", "sacred", "servant",
    ],
}
THEME_FALLBACKS = ["virtue", "nature", "beauty", "strength", "light", "faith", "royalty", "sky-sea"]


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    delay = 1.5
    for attempt in range(6):
        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                return response.read().decode("utf-8", "ignore")
        except HTTPError as exc:
            if exc.code != 429 or attempt == 5:
                raise
            time.sleep(delay)
            delay *= 1.8
    raise RuntimeError(f"Failed to fetch: {url}")


def normalize_spaces(value: str) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def strip_accents(value: str) -> str:
    return "".join(
        ch for ch in unicodedata.normalize("NFKD", value)
        if not unicodedata.combining(ch)
    )


def ascii_variant(name: str) -> str:
    mapped = (
        name.replace("ı", "i")
        .replace("İ", "I")
        .replace("ş", "s")
        .replace("Ş", "S")
        .replace("ğ", "g")
        .replace("Ğ", "G")
        .replace("ç", "c")
        .replace("Ç", "C")
        .replace("ö", "o")
        .replace("Ö", "O")
        .replace("ü", "u")
        .replace("Ü", "U")
    )
    return strip_accents(mapped)


def classify_length(name: str) -> str:
    letters = len(re.sub(r"[^A-Za-zÇĞİIÖŞÜçğıöşü]", "", name))
    if letters <= 5:
        return "short"
    if letters <= 8:
        return "medium"
    return "long"


def clean_title(title: str) -> str:
    title = urllib.parse.unquote(title)
    title = html.unescape(title)
    return normalize_spaces(title.replace("_", " "))


def clean_extract(text: str) -> str:
    text = html.unescape(text or "")
    text = normalize_spaces(text)
    text = re.sub(r"\[[^\]]+\]", "", text)
    text = re.sub(r"\s+\.", ".", text)
    return text


def strip_tags(text: str) -> str:
    return normalize_spaces(html.unescape(re.sub(r"<[^>]+>", "", text or "")))


def summary_to_meaning(name: str, summary: str, gender_label: str) -> str:
    summary = clean_extract(summary)
    if not summary:
        return f"Turkish {gender_label} given name used in modern Turkey."
    summary = summary.split("\n", 1)[0]
    summary = re.sub(rf"^{re.escape(name)}\s+is\s+", "", summary, flags=re.I)
    summary = re.sub(rf"^{re.escape(name)}\s+", "", summary, flags=re.I)
    summary = re.sub(r"^a Turkish (male|female|unisex) given name\b[, ]*", "", summary, flags=re.I)
    summary = re.sub(r"^Turkish (male|female|unisex) given name\b[, ]*", "", summary, flags=re.I)
    summary = re.sub(r"^A Turkish surname\b[, ]*", "", summary, flags=re.I)
    summary = summary.strip(" .;:")
    if not summary:
        return f"Turkish {gender_label} given name used in modern Turkey."
    if len(summary) > 110:
        summary = summary[:107].rstrip(" ,;:") + "..."
    return summary[0].upper() + summary[1:] if summary else summary


def theme_for_text(name: str, text: str) -> list[str]:
    hay = f"{name} {text}".lower()
    themes = []
    for theme, keywords in THEME_KEYWORDS.items():
        if any(word in hay for word in keywords):
            themes.append(theme)
    if not themes:
        themes = [THEME_FALLBACKS[sum(ord(ch) for ch in ascii_variant(name)) % len(THEME_FALLBACKS)]]
    elif len(themes) > 2:
        themes = themes[:2]
    return themes


def wiktionary_category_titles(category: str) -> list[str]:
    titles: list[str] = []
    cont = None
    while True:
        params = {
            "action": "query",
            "list": "categorymembers",
            "cmtitle": category,
            "cmlimit": "500",
            "cmtype": "page",
            "format": "json",
        }
        if cont:
            params["cmcontinue"] = cont
        url = "https://en.wiktionary.org/w/api.php?" + urllib.parse.urlencode(params)
        payload = json.loads(fetch(url))
        for member in payload.get("query", {}).get("categorymembers", []):
            titles.append(clean_title(member.get("title", "")))
        cont = payload.get("continue", {}).get("cmcontinue")
        if not cont:
            break
    return titles


def wiktionary_extracts(titles: list[str]) -> dict[str, str]:
    out: dict[str, str] = {}
    for idx in range(0, len(titles), 25):
        chunk = titles[idx: idx + 25]
        params = {
            "action": "query",
            "prop": "extracts",
            "exintro": "1",
            "explaintext": "1",
            "redirects": "1",
            "titles": "|".join(chunk),
            "format": "json",
        }
        url = "https://en.wiktionary.org/w/api.php?" + urllib.parse.urlencode(params)
        payload = json.loads(fetch(url))
        pages = payload.get("query", {}).get("pages", {})
        for page in pages.values():
            title = clean_title(page.get("title", ""))
            extract = clean_extract(page.get("extract", ""))
            if title:
                out[title] = extract
        time.sleep(0.35)
    return out


def parse_forebears_surnames(limit: int) -> list[str]:
    html_text = fetch("https://forebears.io/turkey/surnames")
    matches = re.findall(r'<td class="sur"><a href="surnames/[^"]+">(.+?)</a></td>', html_text)
    names = []
    seen = set()
    for raw in matches:
        name = clean_title(raw)
        name = name.replace("&#x131;", "ı")
        name = name.replace("&#x15F;", "ş").replace("&#x11F;", "ğ").replace("&#xE7;", "ç")
        name = name.replace("&#xF6;", "ö").replace("&#xFC;", "ü").replace("&#xD6;", "Ö")
        name = name.replace("&#xDC;", "Ü").replace("&#xC7;", "Ç").replace("&#x15E;", "Ş")
        name = name.replace("&#x130;", "İ")
        name = html.unescape(name)
        if not name or name in seen:
            continue
        seen.add(name)
        names.append(name)
        if len(names) >= limit:
            break
    return names


def parse_behindthename_turkish() -> dict[str, str]:
    out: dict[str, str] = {}
    for page in ("", "/2", "/3"):
        html_text = fetch("https://www.behindthename.com/names/usage/turkish" + page)
        entries = re.findall(
            r'<div class="browsename">.*?<a href="/name/[^"]+" class="nll">(.+?)</a>.*?<br>(.*?)</div>',
            html_text,
            flags=re.S,
        )
        for raw_name, raw_desc in entries:
            name = strip_tags(raw_name)
            name = re.sub(r"\s+\d+$", "", name).strip()
            desc = strip_tags(raw_desc).strip(" .;:")
            if not name or not desc:
                continue
            if len(desc) > 110:
                desc = desc[:107].rstrip(" ,;:") + "..."
            out[ascii_variant(name).lower()] = desc[0].upper() + desc[1:] if desc else desc
    return out


def pick_titles(source_titles: list[str], target: int) -> list[str]:
    titles = []
    seen_ascii = set()
    pool = source_titles[:]
    RNG.shuffle(pool)
    for title in pool:
        base = ascii_variant(title).lower()
        if base in seen_ascii:
            continue
        seen_ascii.add(base)
        titles.append(title)
        if len(titles) >= target:
            break
    return sorted(titles, key=lambda value: (ascii_variant(value).lower(), value))


def build_given_names() -> list[dict]:
    btn_map = parse_behindthename_turkish()
    male_titles = pick_titles(wiktionary_category_titles("Category:Turkish_male_given_names"), GIVEN_TARGETS["m"])
    female_titles = pick_titles(wiktionary_category_titles("Category:Turkish_female_given_names"), GIVEN_TARGETS["f"])
    unisex_titles = pick_titles(wiktionary_category_titles("Category:Turkish_unisex_given_names"), GIVEN_TARGETS["u"])

    rows = []
    for gender, titles in (("m", male_titles), ("f", female_titles), ("u", unisex_titles)):
        gender_label = {"m": "male", "f": "female", "u": "unisex"}[gender]
        for title in titles:
            meaning = btn_map.get(ascii_variant(title).lower()) or f"Turkish {gender_label} given name used in modern Turkey."
            rows.append({
                "latin": title,
                "ascii": ascii_variant(title),
                "gender": gender,
                "themes": theme_for_text(title, meaning),
                "meaning": meaning,
                "length": classify_length(title),
            })
    rows.sort(key=lambda entry: (entry["gender"], ascii_variant(entry["latin"]).lower(), entry["latin"]))
    return rows


def build_surnames() -> list[dict]:
    forebears = parse_forebears_surnames(1000)
    wiki_titles = wiktionary_category_titles("Category:Turkish_surnames")
    wiki_extract_map = wiktionary_extracts(wiki_titles)
    wiki_lookup = {ascii_variant(title).lower(): title for title in wiki_titles}

    rows = []
    seen = set()
    for name in forebears:
        key = ascii_variant(name).lower()
        if key in seen:
            continue
        seen.add(key)
        wiki_title = wiki_lookup.get(key)
        extract = wiki_extract_map.get(wiki_title, "") if wiki_title else ""
        if extract:
            note = summary_to_meaning(name, extract, "family")
        elif len(rows) < 100:
            note = "High-frequency Turkish surname recorded in Turkey."
        else:
            note = "Common Turkish surname used in modern Turkey."
        rows.append({
            "latin": name,
            "ascii": ascii_variant(name),
            "note": note,
            "length": classify_length(name),
        })
        if len(rows) >= SURNAME_TARGET:
            break
    rows.sort(key=lambda entry: (ascii_variant(entry["latin"]).lower(), entry["latin"]))
    return rows


def main() -> int:
    given_names = build_given_names()
    surnames = build_surnames()
    payload = {
        "source": {
            "givenNames": [
                "https://en.wiktionary.org/wiki/Category:Turkish_male_given_names",
                "https://en.wiktionary.org/wiki/Category:Turkish_female_given_names",
                "https://en.wiktionary.org/wiki/Category:Turkish_unisex_given_names",
            ],
            "surnames": [
                "https://forebears.io/turkey/surnames",
                "https://en.wiktionary.org/wiki/Category:Turkish_surnames",
            ],
        },
        "givenNames": given_names,
        "surnames": surnames,
    }
    OUT_PATH.write_text(json.dumps(payload, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"Wrote {len(given_names)} given names and {len(surnames)} surnames to {OUT_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

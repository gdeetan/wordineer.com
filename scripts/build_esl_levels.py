#!/usr/bin/env python3
"""Build per-level ESL word data + review CSV from the CEFR lexicon.

Reads the current 62-word lexicon, standardizes IPA to one GenAm convention
(no syllable dots, ər for unstressed r-schwa, ɜr for stressed), attaches a
wordfreq Zipf score per headword, and emits:

  template-deploy/data-src/esl/levels.json    per-level {cards, all}
  template-deploy/data-src/esl/review.csv     draft rows for editorial review
  template-deploy/data-src/esl/build_report.txt

No page changes. No writes outside template-deploy/data-src/esl/.
"""

from __future__ import annotations

import csv
import json
import os
import random
import re
import sys
from collections import defaultdict
from datetime import datetime, timezone

try:
    from wordfreq import zipf_frequency
except ImportError:
    sys.exit("Missing dependency: pip install wordfreq")

try:
    from importlib.metadata import version as _pkg_version
    WF_VER = _pkg_version("wordfreq")
except Exception:
    WF_VER = "unknown"

try:
    import nltk
    from nltk.corpus import cmudict
except ImportError:
    sys.exit("Missing dependency: pip install nltk")

# Ensure the CMU corpus is available.
try:
    _ = cmudict.dict()
except LookupError:
    nltk.download("cmudict", quiet=True)

CMU = cmudict.dict()

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
LEXICON_PATH = os.path.join(ROOT, "wordineer-deploy", "data", "esl-cefr-vocabulary.json")
OUT_DIR = os.path.join(ROOT, "template-deploy", "data-src", "esl")
LEVELS_PATH = os.path.join(OUT_DIR, "levels.json")
REVIEW_PATH = os.path.join(OUT_DIR, "review.csv")
REPORT_PATH = os.path.join(OUT_DIR, "build_report.txt")

CARDS_CAP = 50
IPA_CONVENTION = "genam-ər-no-dots"

# ---------------------------------------------------------------------------
# ARPAbet → GenAm IPA
# ---------------------------------------------------------------------------

ARPABET = {
    "AA": "ɑ", "AE": "æ", "AO": "ɔ", "AW": "aʊ", "AY": "aɪ",
    "EH": "ɛ", "EY": "eɪ", "IH": "ɪ", "IY": "i", "OW": "oʊ",
    "OY": "ɔɪ", "UH": "ʊ", "UW": "u",
    "B": "b", "CH": "tʃ", "D": "d", "DH": "ð", "F": "f", "G": "ɡ",
    "HH": "h", "JH": "dʒ", "K": "k", "L": "l", "M": "m", "N": "n",
    "NG": "ŋ", "P": "p", "R": "r", "S": "s", "SH": "ʃ", "T": "t",
    "TH": "θ", "V": "v", "W": "w", "Y": "j", "Z": "z", "ZH": "ʒ",
}
VOWELS = {"AA","AE","AH","AO","AW","AY","EH","ER","EY","IH","IY","OW","OY","UH","UW"}

LEGAL_2ONSET = {
    ("P","R"),("B","R"),("T","R"),("D","R"),("K","R"),("G","R"),("F","R"),("TH","R"),("SH","R"),
    ("P","L"),("B","L"),("K","L"),("G","L"),("F","L"),("S","L"),
    ("S","M"),("S","N"),("S","P"),("S","T"),("S","K"),("S","W"),("T","W"),("K","W"),("D","W"),("G","W"),
    ("P","Y"),("B","Y"),("K","Y"),("G","Y"),("F","Y"),("M","Y"),("N","Y"),("HH","Y"),("V","Y"),
}
LEGAL_3ONSET = {
    ("S","P","R"),("S","T","R"),("S","K","R"),("S","P","L"),("S","K","W"),
    ("S","P","Y"),("S","T","Y"),("S","K","Y"),
}


def _split_phone(p):
    """Return (bare_phone, stress) where stress is '', '0', '1', or '2'."""
    m = re.match(r"^([A-Z]+)([012])?$", p)
    if not m:
        return p, ""
    return m.group(1), m.group(2) or ""


def _phone_to_ipa(bare, stress):
    if bare == "AH":
        return "ʌ" if stress in ("1", "2") else "ə"
    if bare == "ER":
        return "ɜr" if stress in ("1", "2") else "ər"
    return ARPABET.get(bare, bare)


def _onset_len(cluster):
    """Number of consonants (ARPAbet) at the tail of `cluster` that form a legal onset."""
    k = len(cluster)
    if k == 0:
        return 0
    if k == 1:
        return 1
    if k >= 3 and tuple(cluster[-3:]) in LEGAL_3ONSET:
        return 3
    if tuple(cluster[-2:]) in LEGAL_2ONSET:
        return 2
    return 1


def arpabet_to_ipa(phones):
    """Convert a list of ARPAbet phones to slashed IPA in the chosen convention."""
    bare = []
    stress = []
    for p in phones:
        b, s = _split_phone(p)
        bare.append(b)
        stress.append(s)

    vowel_positions = [i for i, b in enumerate(bare) if b in VOWELS]
    syllable_start = [0] * len(vowel_positions)
    for si, vpos in enumerate(vowel_positions):
        if si == 0:
            syllable_start[si] = 0
        else:
            prev_vpos = vowel_positions[si - 1]
            between = bare[prev_vpos + 1: vpos]
            onset = _onset_len(between)
            syllable_start[si] = vpos - onset

    # stress mark per syllable
    marks = []
    for si, vpos in enumerate(vowel_positions):
        s = stress[vpos]
        if s == "1":
            marks.append("ˈ")
        elif s == "2":
            marks.append("ˌ")
        else:
            marks.append("")

    # If word has any stress-1 syllable, that gets ˈ; if only stress-0/2 (rare),
    # promote first stress-2 to ˈ so every word has a primary mark.
    if not any(m == "ˈ" for m in marks):
        for i, m in enumerate(marks):
            if m == "ˌ":
                marks[i] = "ˈ"
                break
        else:
            if marks:
                marks[0] = "ˈ"

    out = []
    for i, b in enumerate(bare):
        # emit stress mark for the syllable that starts at position i
        for si, start in enumerate(syllable_start):
            if start == i and marks[si]:
                out.append(marks[si])
        out.append(_phone_to_ipa(b, stress[i]))
    return "/" + "".join(out) + "/"


def lookup_ipa(word):
    """Return (ipa, missing, multi) for a single word."""
    key = word.lower()
    entries = CMU.get(key)
    if not entries:
        return "", True, False
    phones = entries[0]
    return arpabet_to_ipa(phones), False, len(entries) > 1


# ---------------------------------------------------------------------------
# Exclusions for the rich-card set
# ---------------------------------------------------------------------------

FUNCTION_WORDS = {
    # articles
    "a", "an", "the",
    # pronouns
    "i", "you", "he", "she", "it", "we", "they",
    "me", "him", "her", "us", "them",
    "my", "your", "his", "its", "our", "their",
    "this", "that", "these", "those",
    # auxiliaries / modals
    "be", "am", "is", "are", "was", "were", "been", "being",
    "do", "does", "did", "have", "has", "had",
    "will", "would", "shall", "should", "can", "could", "may", "might", "must",
    # prepositions
    "in", "on", "at", "to", "from", "of", "for", "with", "by",
    "about", "into", "through", "during", "before", "after",
    "above", "below", "between", "among", "over", "under",
    # conjunctions
    "and", "or", "but", "so", "yet", "because", "if", "when", "while", "although",
}


def _is_proper(word_display, pos):
    if pos and pos.lower().strip() in ("proper noun", "propernoun", "proper_noun"):
        return True
    return False


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    with open(LEXICON_PATH, encoding="utf-8") as f:
        lex = json.load(f)

    exclusions = []       # for report: (word, reason)
    multi_pron = []       # words with >1 CMU pronunciation
    ipa_missing_list = [] # words missing from CMU

    entries = []
    for row in lex:
        word_display = row["w"]
        pos = row.get("pos", "")
        level = row["cefr"]
        wlow = word_display.strip().lower()
        zipf = zipf_frequency(wlow, "en")
        ipa, missing, multi = lookup_ipa(wlow)
        if missing:
            ipa_missing_list.append(word_display)
        if multi:
            multi_pron.append(word_display)

        excl_reason = None
        if wlow in FUNCTION_WORDS:
            excl_reason = "function_word"
        elif _is_proper(word_display, pos):
            excl_reason = "proper_noun"
        if excl_reason:
            exclusions.append((word_display, excl_reason))

        entries.append({
            "word": word_display,
            "pos": pos,
            "level": level,
            "zipf": round(zipf, 3),
            "ipa": ipa,
            "ipa_missing": missing,
            "eligible_for_cards": excl_reason is None,
            "_def": row.get("def", ""),
            "_example": row.get("example", ""),
        })

    # Per-level split
    by_level = defaultdict(list)
    for e in entries:
        by_level[e["level"]].append(e)

    levels_out = {}
    for level in sorted(by_level.keys()):
        rows = by_level[level]
        eligible = [e for e in rows if e["eligible_for_cards"]]
        eligible.sort(key=lambda e: (-e["zipf"], e["word"].lower()))
        cards_n = min(CARDS_CAP, len(eligible))
        cards = eligible[:cards_n]
        all_rows = sorted(rows, key=lambda e: e["word"].lower())

        def _slim(e):
            return {
                "word": e["word"],
                "pos": e["pos"],
                "level": e["level"],
                "zipf": e["zipf"],
                "ipa": e["ipa"],
                "ipa_missing": e["ipa_missing"],
            }

        levels_out[level] = {
            "cards": [_slim(e) for e in cards],
            "all": [_slim(e) for e in all_rows],
        }

    meta = {
        "wordfreq_version": WF_VER,
        "ipa_convention": IPA_CONVENTION,
        "cards_cap": CARDS_CAP,
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "source_lexicon": os.path.relpath(LEXICON_PATH, ROOT),
    }

    with open(LEVELS_PATH, "w", encoding="utf-8") as f:
        json.dump({"meta": meta, "levels": levels_out}, f, ensure_ascii=False, indent=2)
        f.write("\n")

    # review.csv — preserve status/notes/definition/example on re-run so hand edits stick
    existing = {}
    if os.path.exists(REVIEW_PATH):
        with open(REVIEW_PATH, encoding="utf-8", newline="") as f:
            r = csv.DictReader(f)
            for row in r:
                key = (row["level"], row["word"].strip().lower())
                existing[key] = row
    with open(REVIEW_PATH, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
        w.writerow(["level", "word", "pos", "ipa", "definition", "example", "status", "notes"])
        for e in sorted(entries, key=lambda x: (x["level"], x["word"].lower())):
            key = (e["level"], e["word"].strip().lower())
            prior = existing.get(key)
            status = prior["status"] if prior else "draft"
            definition = prior["definition"] if prior and prior["definition"] else e["_def"]
            example = prior["example"] if prior and prior["example"] else e["_example"]
            notes = prior["notes"] if prior else ("ipa_missing" if e["ipa_missing"] else "")
            # Refresh notes flag if IPA missing status changed
            if e["ipa_missing"] and "ipa_missing" not in notes:
                notes = (notes + ";ipa_missing").strip(";")
            w.writerow([e["level"], e["word"], e["pos"], e["ipa"], definition, example, status, notes])

    # Report
    report_lines = []
    R = report_lines.append
    R(f"build_esl_levels.py report — {meta['generated_at']}")
    R(f"wordfreq version: {WF_VER}")
    R(f"IPA convention: {IPA_CONVENTION}")
    R(f"Cards cap per level: {CARDS_CAP}")
    R("")
    R("Per-level counts (all / eligible / cards):")
    for level in sorted(levels_out.keys()):
        rows = by_level[level]
        eligible = [e for e in rows if e["eligible_for_cards"]]
        R(f"  {level}: all={len(rows)}  eligible={len(eligible)}  cards={len(levels_out[level]['cards'])}")
    R("")
    R(f"ipa_missing: {len(ipa_missing_list)}")
    for w_ in ipa_missing_list:
        R(f"  - {w_}")
    R("")
    R(f"Excluded from cards ({len(exclusions)}):")
    for w_, why in exclusions:
        R(f"  - {w_} ({why})")
    R("")
    R(f"Multiple CMU pronunciations (first taken): {len(multi_pron)}")
    for w_ in multi_pron:
        R(f"  - {w_}")
    R("")
    R("15 random IPA spot checks (seed=0):")
    rng = random.Random(0)
    sample = rng.sample(entries, min(15, len(entries)))
    for e in sample:
        R(f"  {e['word']} → {e['ipa'] or '(missing)'}")
    R("")
    R("Words dropped or retagged from the 62: 0 (decision d keeps all)")
    R("")

    # Acceptance tests
    R("=" * 40)
    R("ACCEPTANCE TESTS")
    R("=" * 40)

    # 1. Level parity
    src_levels = {row["w"].strip().lower(): row["cefr"] for row in lex}
    parity_fail = []
    for level, bucket in levels_out.items():
        for e in bucket["all"]:
            if src_levels.get(e["word"].strip().lower()) != e["level"]:
                parity_fail.append(e["word"])
    R(f"[{'PASS' if not parity_fail else 'FAIL'}] Level parity ({len(parity_fail)} mismatches)")

    # 2. No syllable dots / no ɚ in levels.json
    with open(LEVELS_PATH, encoding="utf-8") as f:
        levels_text = f.read()
    ipa_strings = re.findall(r'"ipa":\s*"([^"]*)"', levels_text)
    dot_fail = [s for s in ipa_strings if "." in s]
    schwa_r_fail = [s for s in ipa_strings if "ɚ" in s]
    R(f"[{'PASS' if not dot_fail else 'FAIL'}] No syllable dots in IPA ({len(dot_fail)})")
    R(f"[{'PASS' if not schwa_r_fail else 'FAIL'}] No ɚ in IPA (single r convention) ({len(schwa_r_fail)})")

    # 3. Anchor words
    anchors = {"water": "/ˈwɔtər/", "work": "/ˈwɜrk/", "hello": "/həˈloʊ/"}
    actual = {}
    for bucket in levels_out.values():
        for e in bucket["all"]:
            k = e["word"].strip().lower()
            if k in anchors:
                actual[k] = e["ipa"]
    anchor_pass = True
    for k, expected in anchors.items():
        got = actual.get(k, "(not present)")
        ok = got == expected
        anchor_pass = anchor_pass and ok
        R(f"  {'✓' if ok else '✗'} {k}: expected {expected}, got {got}")
    R(f"[{'PASS' if anchor_pass else 'FAIL'}] Anchor words")

    # 4. Review row count
    with open(REVIEW_PATH, encoding="utf-8") as f:
        n_lines = sum(1 for _ in f)
    n_data = n_lines - 1
    R(f"[{'PASS' if n_data == len(lex) else 'FAIL'}] review.csv row count: {n_data} data + 1 header (expected {len(lex)} data)")

    # 5. Meta present
    ok_meta = bool(meta["wordfreq_version"]) and meta["wordfreq_version"] != "unknown"
    R(f"[{'PASS' if ok_meta else 'WARN'}] meta.wordfreq_version = {meta['wordfreq_version']!r}")

    text = "\n".join(report_lines)
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write(text + "\n")
    print(text)


if __name__ == "__main__":
    main()

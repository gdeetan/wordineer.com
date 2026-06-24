# B-Words Dataset Expansion Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Expand the B-only five-letter dataset while maximizing entries that have real definitions.

**Architecture:** Build a local generation script that derives B-word candidates from `dictionary.json`, preserves local metadata where present, enriches unmatched words via an external dictionary API, and falls back only when external lookup fails. Then rebuild and verify the B page against the new dataset.

**Tech Stack:** Python 3, JSON, static HTML build pipeline, external HTTP API

---

### Task 1: Measure local metadata coverage and candidate breadth

**Files:**
- Modify: none
- Test: local Python inspection commands

- [ ] **Step 1: Count current local structured B-word coverage**

Run: `python3 - <<'PY'
from pathlib import Path
import json, re
pat = re.compile(r'^[A-Za-z]{5}$')
seen = {}
for path in [
    'wordineer-deploy/data/five-letter-words-b.json',
    'wordineer-deploy/data/five-letter-words.json',
    'wordineer-deploy/data/words_expanded.json',
]:
    data = json.loads(Path(path).read_text())
    for item in data:
        rec = item if isinstance(item, dict) else {'w': item[0], 't': item[1], 'd': item[2], 'diff': item[3]}
        w = rec.get('w')
        if not w or not pat.fullmatch(w) or not w.lower().startswith('b'):
            continue
        if all(rec.get(k) for k in ('w', 't', 'd', 'diff')):
            seen.setdefault(w.lower(), rec)
print('structured_b', len(seen))
PY`

Expected: numeric count around the known local structured ceiling

- [ ] **Step 2: Count broad B candidates from the dictionary**

Run: `python3 - <<'PY'
from pathlib import Path
import json, re
pat = re.compile(r'^[A-Za-z]{5}$')
data = json.loads(Path('wordineer-deploy/data/dictionary.json').read_text())
words = sorted({w.lower() for w in data if isinstance(w, str) and pat.fullmatch(w) and w.lower().startswith('b')})
print('dictionary_b', len(words))
print('sample_start', words[:10])
print('sample_end', words[-10:])
PY`

Expected: numeric count around the known dictionary pool

### Task 2: Create the external-enrichment generation script

**Files:**
- Create: `template-deploy/generate_five_letter_words_b.py`
- Test: local script execution and syntax check

- [ ] **Step 1: Add the generator script**

```python
from pathlib import Path
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "wordineer-deploy" / "data"
PATTERN = re.compile(r"^[A-Za-z]{5}$")
API_BASE = "https://api.dictionaryapi.dev/api/v2/entries/en/"
VALID_TYPES = {"noun", "verb", "adjective", "adverb"}


def load_json(path: Path):
    return json.loads(path.read_text())


def is_valid_b_word(word: str) -> bool:
    return isinstance(word, str) and bool(PATTERN.fullmatch(word)) and word.lower().startswith("b")


def normalize_word(word: str) -> str:
    return word.lower()


def title_word(word: str) -> str:
    return word[:1].upper() + word[1:].lower()


def coerce_record(item):
    if isinstance(item, dict):
        return {
            "w": item.get("w"),
            "t": item.get("t"),
            "d": item.get("d"),
            "diff": item.get("diff"),
        }
    if isinstance(item, list) and len(item) >= 4:
        return {"w": item[0], "t": item[1], "d": item[2], "diff": item[3]}
    return None


def collect_structured_records():
    records = {}
    for name in ["five-letter-words-b.json", "five-letter-words.json", "words_expanded.json"]:
        for item in load_json(DATA / name):
            rec = coerce_record(item)
            if not rec or not all(rec.values()):
                continue
            if not is_valid_b_word(rec["w"]):
                continue
            key = normalize_word(rec["w"])
            if key in records:
                continue
            records[key] = {
                "w": title_word(rec["w"]),
                "t": rec["t"],
                "d": rec["d"],
                "diff": rec["diff"],
            }
    return records


def collect_dictionary_candidates():
    words = load_json(DATA / "dictionary.json")
    return sorted({normalize_word(w) for w in words if is_valid_b_word(w)})


def fetch_external_record(word: str):
    url = API_BASE + urllib.parse.quote(word)
    req = urllib.request.Request(url, headers={"User-Agent": "WordineerDataBuilder/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError:
        return None
    except urllib.error.URLError:
        return None

    for entry in payload:
        meanings = entry.get("meanings") or []
        for meaning in meanings:
            part = (meaning.get("partOfSpeech") or "").strip().lower()
            defs = meaning.get("definitions") or []
            if part not in VALID_TYPES:
                continue
            for d in defs:
                text = (d.get("definition") or "").strip()
                if text:
                    return {
                        "w": title_word(word),
                        "t": part,
                        "d": text,
                        "diff": "hard",
                    }
    return None


def main():
    structured = collect_structured_records()
    candidates = collect_dictionary_candidates()
    final = []
    external_hits = 0
    fallback_hits = 0

    for word in candidates:
        if word in structured:
            final.append(structured[word])
            continue
        external = fetch_external_record(word)
        if external:
            external_hits += 1
            final.append(external)
        else:
            fallback_hits += 1
            final.append({
                "w": title_word(word),
                "t": "noun",
                "d": "definition unavailable",
                "diff": "hard",
            })
        time.sleep(0.05)

    output = DATA / "five-letter-words-b.json"
    output.write_text(json.dumps(final, indent=2) + "\n")
    print(f"structured_b_records={len(structured)}")
    print(f"dictionary_b_candidates={len(candidates)}")
    print(f"external_hits={external_hits}")
    print(f"fallback_hits={fallback_hits}")
    print(f"written_records={len(final)}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Syntax-check the script**

Run: `PYTHONPYCACHEPREFIX='/private/tmp/pycache-codex' python3 -m py_compile template-deploy/generate_five_letter_words_b.py && echo OK`

Expected: `OK`

### Task 3: Run external enrichment and generate the dataset

**Files:**
- Modify: `wordineer-deploy/data/five-letter-words-b.json`
- Test: local generator execution

- [ ] **Step 1: Run the B-word generator**

Run: `python3 template-deploy/generate_five_letter_words_b.py`

Expected: prints `structured_b_records=...`, `dictionary_b_candidates=...`, `external_hits=...`, `fallback_hits=...`, and `written_records=...`

- [ ] **Step 2: Stop and request escalation only if the generator fails on network access**

Run: no additional command unless the prior step fails due to sandboxed network restrictions

Expected: if sandbox blocks HTTP, rerun with escalation request rather than guessing

### Task 4: Validate the resulting dataset

**Files:**
- Modify: none
- Test: local validation commands

- [ ] **Step 1: Validate JSON shape, duplicates, and required fields**

Run: `python3 - <<'PY'
from pathlib import Path
import json, re
data = json.loads(Path('wordineer-deploy/data/five-letter-words-b.json').read_text())
assert isinstance(data, list)
assert data
pat = re.compile(r'^[A-Za-z]{5}$')
seen = set()
fallback = 0
for item in data:
    assert set(item.keys()) == {'w', 't', 'd', 'diff'}
    assert all(item[k] for k in ('w', 't', 'd', 'diff'))
    assert pat.fullmatch(item['w'])
    assert item['w'].lower().startswith('b')
    key = item['w'].lower()
    assert key not in seen
    seen.add(key)
    if item['d'] == 'definition unavailable':
        fallback += 1
print('count', len(data))
print('fallback_records', fallback)
print('first', data[0])
print('last', data[-1])
PY`

Expected: prints count, fallback count, and sample records without assertion failures

- [ ] **Step 2: Validate the JSON file using the standard tool**

Run: `python3 -m json.tool wordineer-deploy/data/five-letter-words-b.json >/dev/null && echo OK`

Expected: `OK`

### Task 5: Rebuild and verify B page compatibility

**Files:**
- Modify: `template-deploy/output/5-letter-words-starting-with-b.html` via build
- Modify: `wordineer-deploy/5-letter-words-starting-with-b.html` if deployment sync is needed
- Test: build and inspection commands

- [ ] **Step 1: Rebuild template output**

Run: `python3 build.py`

Workdir: `template-deploy`

Expected: build completes successfully and includes `5-letter-words-starting-with-b.html`

- [ ] **Step 2: Sync the built B page to the deploy folder**

Run: `cp 'template-deploy/output/5-letter-words-starting-with-b.html' 'wordineer-deploy/5-letter-words-starting-with-b.html'`

Expected: command exits successfully

- [ ] **Step 3: Verify the page still references the B dataset and current interaction pattern**

Run: `python3 - <<'PY'
from pathlib import Path
import json
page = Path('template-deploy/output/5-letter-words-starting-with-b.html').read_text()
deployed = Path('wordineer-deploy/5-letter-words-starting-with-b.html').read_text()
data = json.loads(Path('wordineer-deploy/data/five-letter-words-b.json').read_text())
assert "fetch('/data/five-letter-words-b.json')" in page
assert "fetch('/data/five-letter-words-b.json')" in deployed
print('dataset_count', len(data))
PY`

Expected: prints `dataset_count ...` without assertion failures

# C-Words Dataset Expansion Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Expand the C-only five-letter dataset beyond 500 entries while preserving the existing schema.

**Architecture:** Build a local generation script that derives C-word candidates from `dictionary.json`, preserves local metadata where present, and applies approved fallback metadata to unmatched words. Then rebuild and verify the C page against the new dataset.

**Tech Stack:** Python 3, JSON, static HTML build pipeline

---

### Task 1: Measure local metadata coverage and candidate breadth

**Files:**
- Modify: none
- Test: local Python inspection commands

- [ ] **Step 1: Count current local structured C-word coverage**

Run: `python3 - <<'PY'
from pathlib import Path
import json, re
pat = re.compile(r'^[A-Za-z]{5}$')
seen = {}
for path in [
    'wordineer-deploy/data/five-letter-words-c.json',
    'wordineer-deploy/data/five-letter-words.json',
    'wordineer-deploy/data/words_expanded.json',
]:
    data = json.loads(Path(path).read_text())
    for item in data:
        rec = item if isinstance(item, dict) else {'w': item[0], 't': item[1], 'd': item[2], 'diff': item[3]}
        w = rec.get('w')
        if not w or not pat.fullmatch(w) or not w.lower().startswith('c'):
            continue
        if all(rec.get(k) for k in ('w', 't', 'd', 'diff')):
            seen.setdefault(w.lower(), rec)
print('structured_c', len(seen))
PY`

Expected: numeric count around the known local structured ceiling

- [ ] **Step 2: Count broad C candidates from the dictionary**

Run: `python3 - <<'PY'
from pathlib import Path
import json, re
pat = re.compile(r'^[A-Za-z]{5}$')
data = json.loads(Path('wordineer-deploy/data/dictionary.json').read_text())
words = sorted({w.lower() for w in data if isinstance(w, str) and pat.fullmatch(w) and w.lower().startswith('c')})
print('dictionary_c', len(words))
print('sample_start', words[:10])
print('sample_end', words[-10:])
PY`

Expected: numeric count around the known dictionary pool

### Task 2: Create the C-dataset generation script

**Files:**
- Create: `template-deploy/generate_five_letter_words_c.py`
- Test: local script execution and syntax check

- [ ] **Step 1: Add the generator script**

```python
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "wordineer-deploy" / "data"
PATTERN = re.compile(r"^[A-Za-z]{5}$")


def load_json(path: Path):
    return json.loads(path.read_text())


def is_valid_c_word(word: str) -> bool:
    return isinstance(word, str) and bool(PATTERN.fullmatch(word)) and word.lower().startswith("c")


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
    for name in ["five-letter-words-c.json", "five-letter-words.json", "words_expanded.json"]:
        for item in load_json(DATA / name):
            rec = coerce_record(item)
            if not rec or not all(rec.values()):
                continue
            if not is_valid_c_word(rec["w"]):
                continue
            if rec["d"] == "definition unavailable":
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
    return sorted({normalize_word(w) for w in words if is_valid_c_word(w)})


def main():
    structured = collect_structured_records()
    candidates = collect_dictionary_candidates()
    final = []
    fallback_hits = 0
    for word in candidates:
        if word in structured:
            final.append(structured[word])
        else:
            fallback_hits += 1
            final.append({
                "w": title_word(word),
                "t": "noun",
                "d": "definition unavailable",
                "diff": "hard",
            })
    output = DATA / "five-letter-words-c.json"
    output.write_text(json.dumps(final, indent=2) + "\n")
    print(f"structured_c_records={len(structured)}")
    print(f"dictionary_c_candidates={len(candidates)}")
    print(f"fallback_hits={fallback_hits}")
    print(f"written_records={len(final)}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Syntax-check the script**

Run: `PYTHONPYCACHEPREFIX='/private/tmp/pycache-codex' python3 -m py_compile template-deploy/generate_five_letter_words_c.py && echo OK`

Expected: `OK`

### Task 3: Generate and validate the dataset

**Files:**
- Modify: `wordineer-deploy/data/five-letter-words-c.json`

- [ ] **Step 1: Run the C-word generator**

Run: `python3 template-deploy/generate_five_letter_words_c.py`

Expected: prints `structured_c_records=...`, `dictionary_c_candidates=...`, `fallback_hits=...`, and `written_records=...`

- [ ] **Step 2: Validate JSON shape, duplicates, and required fields**

Run: `python3 - <<'PY'
from pathlib import Path
import json, re
data = json.loads(Path('wordineer-deploy/data/five-letter-words-c.json').read_text())
assert isinstance(data, list)
assert data
pat = re.compile(r'^[A-Za-z]{5}$')
seen = set()
fallback = 0
for item in data:
    assert set(item.keys()) == {'w', 't', 'd', 'diff'}
    assert all(item[k] for k in ('w', 't', 'd', 'diff'))
    assert pat.fullmatch(item['w'])
    assert item['w'].lower().startswith('c')
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

- [ ] **Step 3: Validate the JSON file using the standard tool**

Run: `python3 -m json.tool wordineer-deploy/data/five-letter-words-c.json >/dev/null && echo OK`

Expected: `OK`

### Task 4: Rebuild and verify C page compatibility

**Files:**
- Modify: `template-deploy/output/5-letter-words-starting-with-c.html` via build
- Modify: `wordineer-deploy/5-letter-words-starting-with-c.html`

- [ ] **Step 1: Rebuild template output**

Run: `python3 build.py`

Workdir: `template-deploy`

Expected: build completes and includes `5-letter-words-starting-with-c.html`

- [ ] **Step 2: Sync the built C page to the deploy folder**

Run: `cp 'template-deploy/output/5-letter-words-starting-with-c.html' 'wordineer-deploy/5-letter-words-starting-with-c.html'`

Expected: command exits successfully

- [ ] **Step 3: Verify the page still references the C dataset**

Run: `python3 - <<'PY'
from pathlib import Path
import json
page = Path('template-deploy/output/5-letter-words-starting-with-c.html').read_text()
deployed = Path('wordineer-deploy/5-letter-words-starting-with-c.html').read_text()
data = json.loads(Path('wordineer-deploy/data/five-letter-words-c.json').read_text())
assert "fetch('/data/five-letter-words-c.json')" in page
assert "fetch('/data/five-letter-words-c.json')" in deployed
print('dataset_count', len(data))
PY`

Expected: prints `dataset_count ...` without assertion failures

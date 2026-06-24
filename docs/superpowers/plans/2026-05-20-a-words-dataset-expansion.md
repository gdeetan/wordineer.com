# A-Words Dataset Expansion Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Expand the A-only five-letter dataset from local repo sources while preserving the existing page-facing schema.

**Architecture:** Build a local data-generation script that derives five-letter A-word candidates from `dictionary.json`, resolves metadata from higher-quality structured sources, applies approved fallback metadata to unmatched candidates, and writes the result back to `wordineer-deploy/data/five-letter-words-a.json`. Then rebuild and verify the A page against the updated dataset.

**Tech Stack:** Python 3, JSON, static HTML build pipeline

---

### Task 1: Measure the real candidate pool before editing data

**Files:**
- Modify: none
- Test: local Python inspection commands

- [ ] **Step 1: Count strict A-only matches available from structured local metadata**

Run: `python3 - <<'PY'
from pathlib import Path
import json, re

def load(path):
    return json.loads(Path(path).read_text())

def norm(word):
    return word.lower()

pat = re.compile(r'^[A-Za-z]{5}$')
seen = {}
for path in [
    'wordineer-deploy/data/five-letter-words-a.json',
    'wordineer-deploy/data/five-letter-words.json',
    'wordineer-deploy/data/words_expanded.json',
]:
    data = load(path)
    for item in data:
        w = item['w'] if isinstance(item, dict) else item[0]
        if not pat.fullmatch(w):
            continue
        if not w.lower().startswith('a'):
            continue
        if isinstance(item, dict):
            rec = {'w': item.get('w'), 't': item.get('t'), 'd': item.get('d'), 'diff': item.get('diff')}
        else:
            rec = {'w': item[0], 't': item[1], 'd': item[2], 'diff': item[3]}
        if all(rec.values()):
            seen.setdefault(norm(w), rec)
print(len(seen))
PY`

Expected: numeric count showing the real local structured ceiling

- [ ] **Step 2: Count broad candidate A-words from the dictionary source**

Run: `python3 - <<'PY'
from pathlib import Path
import json, re
data = json.loads(Path('wordineer-deploy/data/dictionary.json').read_text())
pat = re.compile(r'^[A-Za-z]{5}$')
words = sorted({w.lower() for w in data if isinstance(w, str) and pat.fullmatch(w) and w.lower().startswith('a')})
print(len(words))
print(words[:10])
print(words[-10:])
PY`

Expected: numeric count greater than the strict structured ceiling

### Task 2: Create the A-dataset generation script

**Files:**
- Create: `template-deploy/generate_five_letter_words_a.py`
- Test: local script execution

- [ ] **Step 1: Add the generation script**

```python
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "wordineer-deploy" / "data"
PATTERN = re.compile(r"^[A-Za-z]{5}$")


def load_json(path: Path):
    return json.loads(path.read_text())


def is_valid_a_word(word: str) -> bool:
    return isinstance(word, str) and bool(PATTERN.fullmatch(word)) and word.lower().startswith("a")


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
    for name in ["five-letter-words-a.json", "five-letter-words.json", "words_expanded.json"]:
        for item in load_json(DATA / name):
            rec = coerce_record(item)
            if not rec or not all(rec.values()):
                continue
            if not is_valid_a_word(rec["w"]):
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
    return sorted({normalize_word(w) for w in words if is_valid_a_word(w)})


def main():
    structured = collect_structured_records()
    candidates = collect_dictionary_candidates()
    final = []
    for word in candidates:
        if word in structured:
            final.append(structured[word])
        else:
            final.append({
                "w": title_word(word),
                "t": "noun",
                "d": "definition unavailable",
                "diff": "hard",
            })
    output = DATA / "five-letter-words-a.json"
    output.write_text(json.dumps(final, indent=2) + "\n")
    print(f"structured_a_records={len(structured)}")
    print(f"dictionary_a_candidates={len(candidates)}")
    print(f"written_records={len(final)}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Run the generation script**

Run: `python3 template-deploy/generate_five_letter_words_a.py`

Expected: prints `structured_a_records=...`, `dictionary_a_candidates=...`, and `written_records=...`

### Task 3: Validate the resulting dataset and report the final count

**Files:**
- Modify: `wordineer-deploy/data/five-letter-words-a.json`
- Test: local Python verification commands

- [ ] **Step 1: Validate JSON shape, duplicates, and required fields**

Run: `python3 - <<'PY'
from pathlib import Path
import json, re
data = json.loads(Path('wordineer-deploy/data/five-letter-words-a.json').read_text())
assert isinstance(data, list)
assert data
pat = re.compile(r'^[A-Za-z]{5}$')
seen = set()
for item in data:
    assert set(item.keys()) == {'w', 't', 'd', 'diff'}
    assert all(item[k] for k in ('w', 't', 'd', 'diff'))
    assert pat.fullmatch(item['w'])
    assert item['w'].lower().startswith('a')
    key = item['w'].lower()
    assert key not in seen
    seen.add(key)
print('count', len(data))
print('first', data[0])
print('last', data[-1])
PY`

Expected: prints a count and sample records without assertion failures

- [ ] **Step 2: Validate the JSON file using the standard tool**

Run: `python3 -m json.tool wordineer-deploy/data/five-letter-words-a.json >/dev/null && echo OK`

Expected: `OK`

### Task 4: Rebuild and verify page compatibility

**Files:**
- Modify: `template-deploy/output/5-letter-words-starting-with-a.html` via build
- Modify: `wordineer-deploy/5-letter-words-starting-with-a.html` if deployment copy is needed
- Test: local build and source inspection

- [ ] **Step 1: Rebuild template output**

Run: `python3 build.py`

Workdir: `template-deploy`

Expected: build completes successfully and includes `5-letter-words-starting-with-a.html`

- [ ] **Step 2: Verify the A page and dataset still align**

Run: `python3 - <<'PY'
from pathlib import Path
import json
page = Path('template-deploy/output/5-letter-words-starting-with-a.html').read_text()
data = json.loads(Path('wordineer-deploy/data/five-letter-words-a.json').read_text())
assert "fetch('/data/five-letter-words-a.json')" in page
assert 'id="lp-more-btn"' in page
print('dataset_count', len(data))
PY`

Expected: prints `dataset_count ...` without assertion failures

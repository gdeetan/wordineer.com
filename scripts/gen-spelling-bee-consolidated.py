#!/usr/bin/env python3
"""
Generate spelling-bee-consolidated.json: merge grade-specific files into 500 hardest words.
"""
import json
import glob
import os

def normalize_grade(grade_str):
    """Convert grade string to normalized form (k, 1st, 2nd, ..., 7th)."""
    if not grade_str:
        return None
    grade_str = str(grade_str).lower().strip()

    # Handle ranges like "k-2", "3-4"
    if '-' in grade_str:
        parts = grade_str.split('-')
        grade_str = parts[0]  # Take the lower bound

    # Handle "kindergarten"
    if 'kindergarten' in grade_str or grade_str == 'k':
        return 'k'

    # Handle numeric grades with suffixes
    for suffix in ['st', 'nd', 'rd', 'th']:
        if grade_str.endswith(suffix):
            num = grade_str[:-len(suffix)]
            return f"{num}{suffix}"

    # Handle plain numbers
    if grade_str.isdigit():
        num = int(grade_str)
        if num == 1:
            return '1st'
        elif num == 2:
            return '2nd'
        elif num == 3:
            return '3rd'
        else:
            return f'{num}th'

    return grade_str


def extract_grade_from_filename(filename):
    """Extract grade from filename like 'spelling-bee-2nd-grade.json'."""
    basename = os.path.basename(filename)
    # Remove prefix and suffix
    if basename.startswith('spelling-bee-'):
        middle = basename[len('spelling-bee'):-len('.json')]  # e.g., "-2nd-grade"
        # Extract the grade part
        parts = middle.strip('-').split('-')
        if parts:
            grade_str = parts[0]  # e.g., "2nd"
            return normalize_grade(grade_str)
    return None


def difficulty_rank(diff):
    """Return sort rank for difficulty (hard > medium > easy)."""
    ranking = {'hard': 0, 'medium': 1, 'easy': 2}
    return ranking.get(str(diff).lower(), 3)


def grade_sort_key(grade):
    """Return numeric sort key for grade (k < 1st < 2nd < ... < 7th)."""
    if not grade:
        return 999
    grade_str = str(grade).lower()
    if grade_str == 'k':
        return 0
    for i in range(1, 8):
        if str(i) in grade_str:
            return i
    return 999


# Load all grade-specific files
data = []
loaded_files = []

for filepath in sorted(glob.glob('/Users/garrickdeetan/Documents/Random Word Generator Tool Site/wordineer-deploy/data/spelling-bee-*.json')):
    # Skip consolidated, elementary, words.json, and kindergarten generic files
    basename = os.path.basename(filepath)
    if 'consolidated' in basename or 'elementary' in basename or basename == 'spelling-bee-words.json' or basename == 'spelling-bee-words-kindergarten.json':
        continue

    with open(filepath, 'r') as f:
        entries = json.load(f)

    if not isinstance(entries, list):
        continue

    # Infer grade from filename if not present in entry
    file_grade = extract_grade_from_filename(filepath)

    for entry in entries:
        if not isinstance(entry, dict):
            continue

        word = entry.get('w', '').strip()
        if not word:
            continue

        # Normalize word to capitalized form
        word = word.capitalize()

        # Extract or infer grade
        grade = entry.get('grade')
        if not grade:
            grade = file_grade
        grade = normalize_grade(grade)

        # Extract difficulty
        diff = entry.get('diff', 'easy')
        diff = str(diff).lower()
        if diff not in ['easy', 'medium', 'hard']:
            diff = 'easy'

        data.append({
            'w': word,
            'grade': grade,
            'diff': diff,
        })

    loaded_files.append(basename)

print(f"Loaded {len(loaded_files)} files: {', '.join(loaded_files)}")
print(f"Total entries before dedup: {len(data)}")

# Deduplicate by word, preferring harder difficulty
seen = {}
for entry in data:
    word = entry['w'].lower()
    if word not in seen:
        seen[word] = entry
    else:
        # Prefer harder difficulty, or alphabetically if same difficulty
        old = seen[word]
        if difficulty_rank(entry['diff']) < difficulty_rank(old['diff']):
            seen[word] = entry
        elif difficulty_rank(entry['diff']) == difficulty_rank(old['diff']):
            # If same difficulty, prefer lower grade
            if entry.get('grade') and old.get('grade'):
                if grade_sort_key(entry['grade']) < grade_sort_key(old['grade']):
                    seen[word] = entry

consolidated = list(seen.values())
print(f"After dedup: {len(consolidated)} unique words")

# Sort by: grade (k < 1st < ... < 7th), then difficulty (hard > medium > easy), then alphabetically
consolidated.sort(key=lambda x: (
    grade_sort_key(x.get('grade')),
    difficulty_rank(x.get('diff', 'easy')),
    x['w'].lower()
))

# Cap at 500, preferring hard/medium
# Strategy: take all hard, then all medium, then easy until 500
hard_words = [e for e in consolidated if e['diff'] == 'hard']
medium_words = [e for e in consolidated if e['diff'] == 'medium']
easy_words = [e for e in consolidated if e['diff'] == 'easy']

consolidated = hard_words + medium_words + easy_words
if len(consolidated) > 500:
    consolidated = consolidated[:500]

print(f"Final consolidated: {len(consolidated)} words")

# Verify distribution
grades_count = {}
diffs_count = {}
for entry in consolidated:
    g = entry.get('grade', '?')
    d = entry.get('diff', '?')
    grades_count[g] = grades_count.get(g, 0) + 1
    diffs_count[d] = diffs_count.get(d, 0) + 1

print(f"By grade: {sorted(grades_count.items())}")
print(f"By difficulty: {sorted(diffs_count.items())}")

# Write output
output_path = '/Users/garrickdeetan/Documents/Random Word Generator Tool Site/wordineer-deploy/data/spelling-bee-consolidated.json'
with open(output_path, 'w') as f:
    json.dump(consolidated, f, indent=2)

print(f"\nWrote {len(consolidated)} entries to {output_path}")
print(f"Sample entries:")
for entry in consolidated[:3]:
    print(f"  {entry}")

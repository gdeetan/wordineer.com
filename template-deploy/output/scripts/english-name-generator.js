(function(root, factory) {
  const api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  root.ENGLISH_NAME_GENERATOR = api;
})(typeof globalThis !== 'undefined' ? globalThis : this, function() {
  const ERA_PRIORITY = {
    any: { modern: 50, timeless: 44, 'mid-century': 36, vintage: 28, 'victorian-edwardian': 18 },
    modern: { modern: 60, timeless: 42, 'mid-century': 34, vintage: 16, 'victorian-edwardian': 8 },
    vintage: { vintage: 60, 'victorian-edwardian': 48, timeless: 30, 'mid-century': 22, modern: 10 },
    victorian: { 'victorian-edwardian': 64, vintage: 46, timeless: 26, 'mid-century': 16, modern: 6 },
    edwardian: { 'victorian-edwardian': 64, vintage: 46, timeless: 26, 'mid-century': 16, modern: 6 },
    'mid-century': { 'mid-century': 64, modern: 44, timeless: 30, vintage: 16, 'victorian-edwardian': 8 },
    timeless: { timeless: 64, modern: 38, 'mid-century': 22, vintage: 14, 'victorian-edwardian': 8 }
  };

  const STYLE_PRIORITY = {
    any: { common: 70, modern: 48, timeless: 42, classic: 28, 'old-fashioned': 20, elegant: 16, literary: 14, biblical: 12 },
    common: { common: 72, modern: 46, timeless: 38, classic: 24, 'old-fashioned': 14 },
    modern: { modern: 72, common: 42, timeless: 34, classic: 18 },
    classic: { classic: 72, timeless: 46, common: 28, 'old-fashioned': 20 },
    timeless: { timeless: 72, common: 44, modern: 30, classic: 18 },
    'old-fashioned': { 'old-fashioned': 72, classic: 46, timeless: 30, common: 20 },
    literary: { literary: 72, elegant: 36, classic: 30, timeless: 22 },
    biblical: { biblical: 72, classic: 30, timeless: 22, common: 12 },
    elegant: { elegant: 72, timeless: 34, classic: 28, literary: 20 }
  };

  const STYLE_FAMILIES = {
    timeless: ['timeless', 'classic', 'old-fashioned', 'common', 'aristocratic'],
    biblical: ['biblical', 'classic', 'old-fashioned', 'common'],
    elegant: ['elegant', 'aristocratic', 'literary', 'classic', 'timeless']
  };

  const VINTAGE_STYLE_PRIORITY = {
    'old-fashioned': 90,
    classic: 82,
    elegant: 64,
    literary: 58,
    biblical: 42,
    timeless: 26,
    common: 18,
    modern: 8
  };

  const VINTAGE_ERA_PRIORITY = {
    'victorian-edwardian': 96,
    vintage: 88,
    timeless: 34,
    'mid-century': 20,
    modern: 8
  };

  const VICTORIAN_STYLE_PRIORITY = {
    'old-fashioned': 96,
    classic: 82,
    elegant: 54,
    literary: 44,
    biblical: 34,
    timeless: 24,
    common: 18,
    modern: 6
  };

  const EDWARDIAN_STYLE_PRIORITY = {
    classic: 90,
    timeless: 72,
    elegant: 60,
    'old-fashioned': 42,
    literary: 34,
    common: 26,
    biblical: 18,
    modern: 10
  };

  const VICTORIAN_SURNAME_PRIORITY = {
    aristocratic: 84,
    occupational: 72,
    patronymic: 60,
    'place-based': 52,
    common: 28,
    'double-barrelled': 18
  };

  const EDWARDIAN_SURNAME_PRIORITY = {
    common: 76,
    occupational: 62,
    'place-based': 54,
    patronymic: 42,
    aristocratic: 24,
    'double-barrelled': 18
  };

  const POPULAR_FIRST_BOOSTS = {
    olivia: 42, emma: 41, ava: 40, lily: 39, sophie: 38, mia: 37, amelia: 36, isla: 35, charlotte: 34, alice: 33,
    grace: 32, ella: 31, freya: 30, ruby: 29, evie: 28, florence: 27, hannah: 26, isabelle: 25, lucy: 24, harper: 23,
    james: 42, george: 41, william: 40, oliver: 39, noah: 38, jack: 37, henry: 36, thomas: 35, charlie: 34, leo: 33,
    harry: 32, arthur: 31, ethan: 30, max: 29, samuel: 28, benjamin: 27, edward: 26, charles: 25, frederick: 24, alfred: 23
  };

  const POPULAR_LAST_BOOSTS = {
    smith: 42, jones: 41, williams: 40, brown: 39, taylor: 38, davies: 37, evans: 36, wilson: 35, thomas: 34, roberts: 33,
    johnson: 32, wright: 31, walker: 30, white: 29, hall: 28, harris: 27, clark: 26, lewis: 25, king: 24, green: 23,
    baker: 22, adams: 21, hill: 20, wood: 19, moore: 18, ward: 17, cooper: 16, parker: 15, collins: 14, edwards: 13
  };

  function normalizeEnglishName(value) {
    return String(value || '')
      .normalize('NFD')
      .replace(/[\u0300-\u036f]/g, '')
      .trim()
      .toLowerCase();
  }

  function normalizeEnglishTag(tag) {
    const value = normalizeEnglishName(tag);
    if (value === 'common-uk') return 'common';
    return value;
  }

  function rowName(row) {
    return String(row && (row.n != null ? row.n : row[0]) || '').trim();
  }

  function rowGender(row) {
    return String(row && (row.g != null ? row.g : row[1]) || '');
  }

  function rowStyles(row) {
    const styles = row && (row.styles != null ? row.styles : row[2]);
    return Array.isArray(styles) ? styles.map(normalizeEnglishTag).filter(Boolean) : [];
  }

  function rowEras(row) {
    const eras = row && (row.eras != null ? row.eras : row[3]);
    return Array.isArray(eras) ? eras.map(normalizeEnglishTag).filter(Boolean) : [];
  }

  function rowTypes(row) {
    const types = row && (row.types != null ? row.types : row[3]);
    return Array.isArray(types) ? types.map(normalizeEnglishTag).filter(Boolean) : [];
  }

  function matchesTag(tags, wanted) {
    const value = normalizeEnglishTag(wanted);
    if (!value || value === 'any') return true;
    return Array.isArray(tags) && tags.includes(value);
  }

  function matchesStyle(tags, style) {
    const value = normalizeEnglishTag(style);
    if (!value || value === 'any') return true;
    const family = STYLE_FAMILIES[value];
    if (family) {
      return Array.isArray(tags) && tags.some(function(tag) {
        return family.includes(tag);
      });
    }
    return matchesTag(tags, value);
  }

  function matchesEra(tags, era) {
    const value = normalizeEnglishTag(era);
    if (!value || value === 'any') return true;
    if (value === 'victorian' || value === 'edwardian') return matchesTag(tags, 'victorian-edwardian');
    if (value === 'vintage') return Array.isArray(tags) && (tags.includes('victorian-edwardian') || tags.includes('mid-century') || tags.includes('timeless'));
    return matchesTag(tags, value);
  }

  function bestPriority(tags, table) {
    let score = 0;
    (tags || []).forEach(function(tag) {
      const value = table[tag] || 0;
      if (value > score) score = value;
    });
    return score;
  }

  function scoreEnglishRow(row, opts) {
    const options = opts || {};
    const kind = options.kind === 'last' ? 'last' : 'first';
    const name = normalizeEnglishName(rowName(row));
    const styles = rowStyles(row);
    const eras = rowEras(row);
    const types = rowTypes(row);
    const eraKey = normalizeEnglishTag(options.era);

    let score = 0;
    if (kind === 'last') {
      const selectedLastStyle = normalizeEnglishTag(options.lastStyle);
      if (selectedLastStyle && selectedLastStyle !== 'any') {
        score += bestPriority(types, STYLE_PRIORITY[selectedLastStyle] || STYLE_PRIORITY.any);
      }
      if (eraKey === 'vintage' || eraKey === 'victorian') {
        score += bestPriority(types, VICTORIAN_SURNAME_PRIORITY);
      } else if (eraKey === 'edwardian') {
        score += bestPriority(types, EDWARDIAN_SURNAME_PRIORITY);
      } else {
        score += bestPriority(types, { common: 42, occupational: 24, 'place-based': 20, patronymic: 18, aristocratic: 12, 'double-barrelled': 6 });
      }
    } else if (eraKey === 'vintage') {
      score += bestPriority(styles, VINTAGE_STYLE_PRIORITY);
      score += bestPriority(eras, VINTAGE_ERA_PRIORITY);
    } else if (eraKey === 'victorian') {
      score += bestPriority(styles, VICTORIAN_STYLE_PRIORITY);
      score += bestPriority(eras, { 'victorian-edwardian': 96, vintage: 86, timeless: 26, 'mid-century': 12, modern: 4 });
    } else if (eraKey === 'edwardian') {
      score += bestPriority(styles, EDWARDIAN_STYLE_PRIORITY);
      score += bestPriority(eras, { 'victorian-edwardian': 96, vintage: 78, timeless: 34, 'mid-century': 16, modern: 8 });
    } else {
      score += bestPriority(styles, STYLE_PRIORITY[normalizeEnglishTag(options.style)] || STYLE_PRIORITY.any);
      score += bestPriority(eras, ERA_PRIORITY[eraKey] || ERA_PRIORITY.any);
    }

    if (kind === 'last') {
      score += POPULAR_LAST_BOOSTS[name] || 0;
    } else {
      score += bestPriority(styles, { common: 42, modern: 28, timeless: 24, classic: 12, 'old-fashioned': 8, literary: 6, biblical: 6, elegant: 6 });
      score += POPULAR_FIRST_BOOSTS[name] || 0;
    }

    return score;
  }

  function filterEnglishRows(rows, opts) {
    const options = opts || {};
    const kind = options.kind === 'last' ? 'last' : 'first';
    const gender = normalizeEnglishTag(options.gender);
    const era = normalizeEnglishTag(options.era);
    const style = normalizeEnglishTag(options.style);
    const lastStyle = normalizeEnglishTag(options.lastStyle);
    const letter = normalizeEnglishTag(options.letter);

    return (Array.isArray(rows) ? rows : []).filter(function(row) {
      if (kind !== 'last' && gender && gender !== 'any' && rowGender(row) !== gender) return false;

      const name = rowName(row);
      if (letter && letter !== 'any' && !normalizeEnglishName(name).startsWith(letter)) return false;

      if (kind === 'last') {
        const types = rowTypes(row);
        if (lastStyle && lastStyle !== 'any' && !matchesTag(types, lastStyle)) return false;
      } else {
        const styles = rowStyles(row);
        const eras = rowEras(row);
        if (!matchesStyle(styles, style)) return false;
        if (!matchesEra(eras, era)) {
          return false;
        }
      }

      return true;
    });
  }

  function rankEnglishRows(rows, opts) {
    const filtered = filterEnglishRows(rows, opts);
    const scored = new Map();

    filtered.forEach(function(row) {
      const name = rowName(row);
      const key = normalizeEnglishName(name);
      if (!key) return;
      const score = scoreEnglishRow(row, opts);
      const existing = scored.get(key);
      if (!existing || score > existing.score || (score === existing.score && name.localeCompare(existing.name) < 0)) {
        scored.set(key, { row: row, score: score, name: name });
      }
    });

    return Array.from(scored.values())
      .sort(function(a, b) {
        if (b.score !== a.score) return b.score - a.score;
        return a.name.localeCompare(b.name);
      })
      .map(function(entry) { return entry.row; });
  }

  return {
    normalizeEnglishName: normalizeEnglishName,
    normalizeEnglishTag: normalizeEnglishTag,
    rowName: rowName,
    rowGender: rowGender,
    rowStyles: rowStyles,
    rowEras: rowEras,
    rowTypes: rowTypes,
    matchesTag: matchesTag,
    matchesStyle: matchesStyle,
    matchesEra: matchesEra,
    filterEnglishRows: filterEnglishRows,
    scoreEnglishRow: scoreEnglishRow,
    rankEnglishRows: rankEnglishRows
  };
});

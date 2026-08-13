(function(root, factory) {
  const api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  root.SPANISH_NAME_GENERATOR = api;
  root.initSpanishNameGenerator = api.initSpanishNameGenerator;
})(typeof globalThis !== 'undefined' ? globalThis : this, function() {
  const LABELS = {
    gender: { f: 'female', m: 'male' },
    style: {
      classic: 'classic',
      modern: 'modern',
      traditional: 'traditional',
      'saint-inspired': 'saint-inspired',
      'nature-inspired': 'nature-inspired'
    }
  };

  function getWordineerApi() {
    if (typeof globalThis !== 'undefined' && globalThis.WORDINEER) return globalThis.WORDINEER;
    if (typeof window !== 'undefined' && window.WORDINEER) return window.WORDINEER;
    return null;
  }

  const FALLBACK_SPANISH_NAMES = {
    first: [
      ['Lucia', 'f', ['classic', 'modern'], 'light'],
      ['Sofia', 'f', ['classic', 'modern'], 'wisdom'],
      ['Carmen', 'f', ['traditional', 'saint-inspired'], 'garden; song'],
      ['Maria', 'f', ['traditional', 'saint-inspired'], 'beloved; wished-for child'],
      ['Pilar', 'f', ['traditional', 'saint-inspired'], 'pillar'],
      ['Rocio', 'f', ['traditional', 'nature-inspired'], 'dew'],
      ['Alba', 'f', ['modern', 'nature-inspired'], 'dawn'],
      ['Clara', 'f', ['classic'], 'bright; clear'],
      ['Elena', 'f', ['classic'], 'shining light'],
      ['Angela', 'f', ['classic', 'saint-inspired'], 'messenger'],
      ['Alejandro', 'm', ['classic', 'modern'], 'defender of humankind'],
      ['Diego', 'm', ['classic', 'modern'], 'supplanter'],
      ['Javier', 'm', ['traditional', 'saint-inspired'], 'new house'],
      ['Santiago', 'm', ['traditional', 'saint-inspired'], 'Saint James'],
      ['Mateo', 'm', ['modern', 'saint-inspired'], 'gift of God'],
      ['Hugo', 'm', ['modern'], 'mind; intellect'],
      ['Alvaro', 'm', ['classic'], 'guardian; cautious'],
      ['Pablo', 'm', ['classic', 'traditional'], 'small; humble'],
      ['Rafael', 'm', ['traditional', 'saint-inspired'], 'God has healed'],
      ['Martin', 'm', ['classic', 'modern'], 'of Mars; warlike']
    ],
    compoundFirst: [
      ['Maria Jose', 'f', ['traditional', 'saint-inspired'], 'Mary + Joseph'],
      ['Maria del Carmen', 'f', ['traditional', 'saint-inspired'], 'Mary of Carmel'],
      ['Ana Maria', 'f', ['traditional', 'saint-inspired'], 'grace + Mary'],
      ['Maria Pilar', 'f', ['traditional', 'saint-inspired'], 'Mary + pillar'],
      ['Jose Luis', 'm', ['traditional', 'saint-inspired'], 'Joseph + Louis'],
      ['Jose Antonio', 'm', ['traditional', 'saint-inspired'], 'Joseph + Anthony'],
      ['Juan Carlos', 'm', ['traditional'], 'John + Charles'],
      ['Luis Miguel', 'm', ['traditional', 'saint-inspired'], 'Louis + Michael']
    ],
    last: [
      ['Garcia', 'common', 'young; uncertain origin'],
      ['Lopez', 'common', 'son of Lope'],
      ['Martinez', 'common', 'son of Martin'],
      ['Sanchez', 'common', 'son of Sancho'],
      ['Rodriguez', 'common', 'son of Rodrigo'],
      ['Fernandez', 'common', 'son of Fernando'],
      ['Gomez', 'common', 'son of Gome'],
      ['Ruiz', 'common', 'son of Ruy'],
      ['Navarro', 'regional', 'from Navarre'],
      ['Ortega', 'regional', 'nettle plant; place name'],
      ['Romero', 'traditional', 'pilgrim to Rome; rosemary'],
      ['Molina', 'occupational', 'from the mill'],
      ['Pastor', 'occupational', 'shepherd'],
      ['Delgado', 'descriptive', 'slender'],
      ['Serrano', 'regional', 'from the mountains'],
      ['Campos', 'regional', 'fields'],
      ['Cabrera', 'regional', 'goat place'],
      ['Torres', 'common', 'towers'],
      ['Castro', 'regional', 'fortress'],
      ['Leon', 'regional', 'lion']
    ],
    secondLast: [
      ['Jimenez', 'common', 'son of Jimeno'],
      ['Morales', 'regional', 'mulberry trees'],
      ['Iglesias', 'regional', 'churches'],
      ['Herrera', 'occupational', 'iron smith'],
      ['Prieto', 'descriptive', 'dark-haired'],
      ['Gallardo', 'descriptive', 'brave; noble'],
      ['Aguilar', 'regional', 'eagle place'],
      ['Santana', 'traditional', 'Saint Anne'],
      ['Lozano', 'descriptive', 'elegant; lively'],
      ['Valero', 'descriptive', 'brave'],
      ['Calvo', 'descriptive', 'bald'],
      ['Crespo', 'descriptive', 'curly-haired'],
      ['Rojas', 'descriptive', 'red-colored'],
      ['Benitez', 'common', 'son of Benito'],
      ['Dominguez', 'common', 'son of Domingo'],
      ['Marin', 'occupational', 'of the sea'],
      ['Soler', 'regional', 'sunny place'],
      ['Ferrer', 'occupational', 'blacksmith'],
      ['Cortes', 'regional', 'courts; enclosures'],
      ['Bravo', 'descriptive', 'bold; brave']
    ]
  };

  function normalizeInitial(value) {
    return String(value || '')
      .normalize('NFD')
      .replace(/[\u0300-\u036f]/g, '')
      .trim()
      .charAt(0)
      .toLowerCase();
  }

  function mapSpanishNameData(raw) {
    return {
      first: (raw.first || []).map(function(row) {
        return {
          n: row[0],
          g: row[1],
          styles: row[2] || [],
          meaning: row[3] || ''
        };
      }),
      compoundFirst: (raw.compoundFirst || []).map(function(row) {
        return {
          n: row[0],
          g: row[1],
          styles: row[2] || [],
          meaning: row[3] || ''
        };
      }),
      last: (raw.last || []).map(function(row) {
        return {
          n: row[0],
          tag: row[1] || '',
          meaning: row[2] || ''
        };
      }),
      secondLast: (raw.secondLast || []).map(function(row) {
        return {
          n: row[0],
          tag: row[1] || '',
          meaning: row[2] || ''
        };
      })
    };
  }

  function shuffle(items) {
    const out = items.slice();
    for (let i = out.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      const tmp = out[i];
      out[i] = out[j];
      out[j] = tmp;
    }
    return out;
  }

  function cyclePick(items, index) {
    return items[index % items.length];
  }

  function filterPersonal(rows, opts) {
    return rows.filter(function(row) {
      if (opts.gender !== 'any' && row.g !== opts.gender) return false;
      if (opts.style !== 'any' && !row.styles.includes(opts.style)) return false;
      if (opts.letter !== 'any' && normalizeInitial(row.n) !== opts.letter) return false;
      return true;
    });
  }

  function filterSurnames(rows, opts) {
    return rows.filter(function(row) {
      if (opts.letter !== 'any' && normalizeInitial(row.n) !== opts.letter) return false;
      return true;
    });
  }

  function uniqueByDisplay(items) {
    const seen = new Set();
    return items.filter(function(item) {
      if (seen.has(item.display)) return false;
      seen.add(item.display);
      return true;
    });
  }

  function generateSpanishNames(data, options) {
    const count = Number.parseInt(options.count, 10);
    if (!Number.isInteger(count) || count < 1 || count > 50) return [];

      const opts = {
        gender: options.gender || 'any',
        type: options.type || 'first',
        style: options.style || 'any',
        surnameStructure: options.surnameStructure || 'any',
        letter: options.letter || 'any'
      };

    const oneSurnameMode = opts.type === 'full' && opts.surnameStructure === 'one';
    const twoSurnameMode = opts.type === 'two-surname-full' || (opts.type === 'full' && opts.surnameStructure === 'two');

    const firstPool = shuffle(filterPersonal(data.first || [], opts));
    const compoundPool = shuffle(filterPersonal(data.compoundFirst || [], opts));
    const lastLetter = opts.type === 'last' ? opts.letter : 'any';
    const lastPool = shuffle(filterSurnames(data.last || [], { letter: lastLetter }));
    const secondLastPool = shuffle(filterSurnames(data.secondLast || [], { letter: 'any' }));

    if (opts.type === 'first' && !firstPool.length) return [];
    if (opts.type === 'compound-first' && !compoundPool.length) return [];
    if (opts.type === 'last' && !lastPool.length) return [];
    if ((opts.type === 'full' || opts.type === 'two-surname-full') && (!firstPool.length || !lastPool.length)) return [];
    if (twoSurnameMode && !secondLastPool.length) return [];

    const results = [];
    let index = 0;
    let guard = 0;

    while (results.length < count && guard < count * 20) {
      guard += 1;

      if (opts.type === 'first') {
        const first = cyclePick(firstPool, index++);
        results.push({
          display: first.n,
          meaning: first.meaning,
          note: 'Spanish given name',
          chips: [LABELS.gender[first.g] || first.g, LABELS.style[first.styles[0]] || first.styles[0] || 'Spanish']
        });
        continue;
      }

      if (opts.type === 'compound-first') {
        const compound = cyclePick(compoundPool, index++);
        results.push({
          display: compound.n,
          meaning: compound.meaning,
          note: 'Curated compound Spanish given name',
          chips: [LABELS.gender[compound.g] || compound.g, LABELS.style[compound.styles[0]] || compound.styles[0] || 'compound']
        });
        continue;
      }

      if (opts.type === 'last') {
        const last = cyclePick(lastPool, index++);
        results.push({
          display: last.n,
          meaning: last.meaning,
          note: 'Spanish surname',
          chips: ['surname', last.tag || 'Spanish']
        });
        continue;
      }

      const first = cyclePick(firstPool, index);
      const last = cyclePick(lastPool, index + 3);
      const secondLast = secondLastPool.length ? cyclePick(secondLastPool, index + 7) : null;
      const shouldUseTwo = twoSurnameMode || (!oneSurnameMode && opts.type === 'full' && opts.surnameStructure === 'any' && index % 2 === 1);
      index += 1;

      if (shouldUseTwo && secondLast) {
        results.push({
          display: first.n + ' ' + last.n + ' ' + secondLast.n,
          meaning: first.meaning + ' · ' + last.meaning + ' · ' + secondLast.meaning,
          note: 'Spanish full name with two surnames',
          chips: [LABELS.gender[first.g] || first.g, LABELS.style[first.styles[0]] || first.styles[0] || 'Spanish', 'two surnames']
        });
      } else {
        results.push({
          display: first.n + ' ' + last.n,
          meaning: first.meaning + ' · ' + last.meaning,
          note: 'Spanish full name',
          chips: [LABELS.gender[first.g] || first.g, LABELS.style[first.styles[0]] || first.styles[0] || 'Spanish', 'one surname']
        });
      }
    }

    return uniqueByDisplay(results).slice(0, count);
  }

  function initSpanishNameGenerator() {
    if (typeof document === 'undefined') return;
    const list = document.getElementById('sng-list');
    if (!list || list.dataset.bound === '1') return;
    list.dataset.bound = '1';

    const countInput = document.getElementById('sng-count');
    const countError = document.getElementById('sng-count-error');
    const countDisplay = document.getElementById('sng-count-display');
    const genderSelect = document.getElementById('sng-gender');
    const typeSelect = document.getElementById('sng-type');
    const styleSelect = document.getElementById('sng-style');
    const surnameStructureSelect = document.getElementById('sng-surname-structure');
    const letterSelect = document.getElementById('sng-letter');
    const defsToggle = document.getElementById('sng-defs');
    const generateBtn = document.getElementById('sng-gen-btn');
    const resetBtn = document.getElementById('sng-reset-btn');
    const copyAllBtn = document.getElementById('sng-copy-all-btn');
    const copySavedBtn = document.getElementById('sng-copy-saved-btn');
    const savedList = document.getElementById('sng-saved-tags');
    const mobileToggle = document.getElementById('sng-mobile-toggle');
    const advancedPanel = document.getElementById('sng-advanced');
    const savedKey = 'wnr_saved_spanish_names';

    const activeData = mapSpanishNameData(FALLBACK_SPANISH_NAMES);
    let currentItems = [];
    let savedNames = [];
    let loadAttempted = false;

    function loadSaved() {
      try {
        savedNames = JSON.parse(localStorage.getItem(savedKey) || '[]');
        if (!Array.isArray(savedNames)) savedNames = [];
      } catch {
        savedNames = [];
      }
    }

    function persistSaved() {
      localStorage.setItem(savedKey, JSON.stringify(savedNames));
    }

    function isSaved(name) {
      return savedNames.includes(name);
    }

    function escapeHtml(value) {
      return String(value)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;');
    }

    function renderSaved() {
      if (!savedList) return;
      if (!savedNames.length) {
        savedList.innerHTML = '<span class="saved-empty">Click the heart on any name to save it here</span>';
        return;
      }
      savedList.innerHTML = savedNames.map(function(name) {
        return '<span class="saved-tag">' + escapeHtml(name) + ' <span class="saved-tag-remove" data-action="remove-saved" data-name="' + escapeHtml(name) + '">×</span></span>';
      }).join('');
    }

    function renderItems(items) {
      if (countDisplay) countDisplay.textContent = items.length + ' result' + (items.length === 1 ? '' : 's') + ' generated';
      if (!items.length) {
        list.innerHTML = '<li class="word-item sng-no-results"><div class="word-left"><div class="word-text">No names match these filters</div><div class="sng-meaning">Try a broader style, a different letter, or reset the filters.</div></div></li>';
        return;
      }
      const showDefs = defsToggle ? defsToggle.checked : true;
      list.innerHTML = items.map(function(item) {
        const chips = (item.chips || []).filter(Boolean).slice(0, 3).map(function(chip, index) {
          const kind = index === 0 ? 'gender' : (index === 1 ? 'style' : 'type');
          return '<span class="sng-chip sng-chip--' + kind + '">' + escapeHtml(chip) + '</span>';
        }).join('');
        return ''
          + '<li class="word-item" data-name="' + escapeHtml(item.display) + '">'
          +   '<div class="word-left">'
          +     '<div class="word-text">' + escapeHtml(item.display) + '</div>'
          +     (showDefs ? '<div class="sng-meaning">' + escapeHtml(item.meaning) + '</div>' : '')
          +     '<div class="sng-note">' + escapeHtml(item.note) + '</div>'
          +     '<div class="sng-chips">' + chips + '</div>'
          +   '</div>'
          +   '<div class="word-right">'
          +     '<button class="icon-btn" type="button" title="Copy" data-action="copy" data-name="' + escapeHtml(item.display) + '">'
          +       '<svg viewBox="0 0 14 14" fill="none"><rect x="1" y="4" width="9" height="9.5" rx="1.5" stroke="currentColor" stroke-width="1.1"/><path d="M4.5 4V2.5A1.5 1.5 0 016 1h5.5A1.5 1.5 0 0113 2.5v7a1.5 1.5 0 01-1.5 1.5H10" stroke="currentColor" stroke-width="1.1"/></svg>'
          +     '</button>'
          +     '<button class="icon-btn' + (isSaved(item.display) ? ' saved' : '') + '" type="button" title="' + (isSaved(item.display) ? 'Unsave' : 'Save') + '" data-action="save" data-name="' + escapeHtml(item.display) + '">'
          +       '<svg viewBox="0 0 16 16" fill="none"><path d="M8 13.5S2 9.5 2 5.5A3 3 0 018 4a3 3 0 016 1.5c0 4-6 8-6 8z" stroke="currentColor" stroke-width="1.3" fill="' + (isSaved(item.display) ? '#E24B4A' : 'none') + '" stroke-linecap="round"/></svg>'
          +     '</button>'
          +   '</div>'
          + '</li>';
      }).join('');
    }

    function validateCount() {
      const count = Number.parseInt(countInput && countInput.value, 10);
      const valid = Number.isInteger(count) && count >= 1 && count <= 50;
      if (countError) countError.style.display = valid ? 'none' : 'block';
      return valid;
    }

    function syncControls() {
      const type = typeSelect ? typeSelect.value : 'full';
      if (genderSelect) genderSelect.disabled = type === 'last';
      if (surnameStructureSelect) {
        const shouldDisable = type === 'last' || type === 'compound-first' || type === 'two-surname-full';
        surnameStructureSelect.disabled = shouldDisable;
        if (type === 'two-surname-full') surnameStructureSelect.value = 'two';
        if (type === 'compound-first' || type === 'last') surnameStructureSelect.value = 'any';
      }
    }

    function getOptions() {
      return {
        count: countInput ? countInput.value : '10',
        gender: genderSelect ? genderSelect.value : 'any',
        type: typeSelect ? typeSelect.value : 'first',
        style: styleSelect ? styleSelect.value : 'any',
        surnameStructure: surnameStructureSelect ? surnameStructureSelect.value : 'any',
        letter: letterSelect ? letterSelect.value : 'any'
      };
    }

    function generateAndRender() {
      syncControls();
      if (!validateCount()) {
        currentItems = [];
        renderItems(currentItems);
        return;
      }
      currentItems = generateSpanishNames(activeData, getOptions());
      renderItems(currentItems);
    }

    function copyText(text, message) {
      navigator.clipboard && navigator.clipboard.writeText(text);
      const api = getWordineerApi();
      if (api && typeof api.showToast === 'function') {
        api.showToast(message);
      }
    }

    function loadData() {
      if (loadAttempted) return;
      loadAttempted = true;
      fetch('/data/spanish-names.json', { cache: 'force-cache' })
        .then(function(response) {
          if (!response.ok) throw new Error(String(response.status));
          return response.json();
        })
        .then(function(raw) {
          const mapped = mapSpanishNameData(raw);
          activeData.first = mapped.first;
          activeData.compoundFirst = mapped.compoundFirst;
          activeData.last = mapped.last;
          activeData.secondLast = mapped.secondLast;
          generateAndRender();
        })
        .catch(function() {
          const api = getWordineerApi();
          if (api && typeof api.showToast === 'function') {
            api.showToast('Using starter Spanish names while the full list loads.');
          }
        });
    }

    loadSaved();
    renderSaved();
    generateAndRender();
    loadData();

    list.addEventListener('click', function(event) {
      const button = event.target.closest('[data-action]');
      if (!button) return;
      const action = button.getAttribute('data-action');
      const name = button.getAttribute('data-name');
      if (!name) return;

      if (action === 'copy') {
        copyText(name, 'Copied: ' + name);
        return;
      }

      if (action === 'save') {
        if (isSaved(name)) {
          savedNames = savedNames.filter(function(savedName) { return savedName !== name; });
        } else {
          savedNames.push(name);
        }
        persistSaved();
        renderSaved();
        renderItems(currentItems);
      }
    });

    if (savedList) {
      savedList.addEventListener('click', function(event) {
        const button = event.target.closest('[data-action="remove-saved"]');
        if (!button) return;
        const name = button.getAttribute('data-name');
        if (!name) return;
        savedNames = savedNames.filter(function(savedName) { return savedName !== name; });
        persistSaved();
        renderSaved();
        renderItems(currentItems);
      });
    }

    if (countInput) {
      countInput.addEventListener('input', function() {
        validateCount();
        generateAndRender();
      });
    }

    [genderSelect, typeSelect, styleSelect, surnameStructureSelect, letterSelect].forEach(function(control) {
      if (!control) return;
      control.addEventListener('change', generateAndRender);
    });

    if (defsToggle) defsToggle.addEventListener('change', function() { renderItems(currentItems); });
    if (generateBtn) generateBtn.addEventListener('click', generateAndRender);
    if (resetBtn) {
      resetBtn.addEventListener('click', function() {
        if (countInput) countInput.value = '10';
        if (genderSelect) genderSelect.value = 'any';
        if (typeSelect) typeSelect.value = 'first';
        if (styleSelect) styleSelect.value = 'any';
        if (surnameStructureSelect) surnameStructureSelect.value = 'any';
        if (letterSelect) letterSelect.value = 'any';
        if (defsToggle) defsToggle.checked = true;
        generateAndRender();
      });
    }
    if (copyAllBtn) {
      copyAllBtn.addEventListener('click', function() {
        const text = currentItems.map(function(item) { return item.display; }).join('\n');
        if (!text) return;
        copyText(text, 'All names copied!');
      });
    }
    if (copySavedBtn) {
      copySavedBtn.addEventListener('click', function() {
        if (!savedNames.length) return;
        copyText(savedNames.join(', '), 'Saved names copied!');
      });
    }
    if (mobileToggle && advancedPanel) {
      mobileToggle.addEventListener('click', function() {
        const isOpen = advancedPanel.classList.toggle('is-open');
        mobileToggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
        mobileToggle.textContent = isOpen ? 'Hide options' : 'More options';
      });
    }

    document.addEventListener('keydown', function(event) {
      if (event.code === 'Space' && !['INPUT', 'SELECT', 'TEXTAREA', 'BUTTON'].includes(event.target.tagName)) {
        event.preventDefault();
        generateAndRender();
      }
    });
  }

  return {
    FALLBACK_SPANISH_NAMES: FALLBACK_SPANISH_NAMES,
    normalizeInitial: normalizeInitial,
    mapSpanishNameData: mapSpanishNameData,
    generateSpanishNames: generateSpanishNames,
    initSpanishNameGenerator: initSpanishNameGenerator
  };
});

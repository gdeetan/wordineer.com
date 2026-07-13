// BW — Best Wordle Starting Words interactive table
const BW = (() => {
  let _data = [];
  let _sortCol = 'rank';
  let _sortAsc  = true;
  let _query    = '';

  const $ = id => document.getElementById(id);

  function loadAndRender() {
    fetch('/data/starting-words-top100.json')
      .then(r => r.json())
      .then(data => {
        _data = data;
        render();
        wireSort();
        wireSearch();
      })
      .catch(() => {
        const tb = $('bw-tbody');
        if (tb) tb.innerHTML = '<tr><td colspan="4" style="text-align:center;color:var(--text-3);padding:20px">Could not load data. Please refresh.</td></tr>';
      });
  }

  function filtered() {
    if (!_query) return _data;
    const q = _query.toLowerCase();
    return _data.filter(r => r.word.toLowerCase().includes(q));
  }

  function sorted(rows) {
    return [...rows].sort((a, b) => {
      const av = a[_sortCol], bv = b[_sortCol];
      const cmp = typeof av === 'string' ? av.localeCompare(bv) : av - bv;
      return _sortAsc ? cmp : -cmp;
    });
  }

  function render() {
    const tb = $('bw-tbody');
    if (!tb) return;
    const rows = sorted(filtered());
    if (!rows.length) {
      tb.innerHTML = '<tr><td colspan="4" style="text-align:center;color:var(--text-3);padding:16px">No words match your search.</td></tr>';
      updateCount(0);
      return;
    }
    tb.innerHTML = rows.map(r => `
      <tr class="${r.rank <= 3 ? 'bw-top' : ''}">
        <td class="bw-rank">${r.rank}</td>
        <td class="bw-word">${r.word}</td>
        <td class="bw-bits">${r.entropy_bits.toFixed(4)}</td>
        <td class="bw-rem">${r.expected_remaining.toFixed(1)}</td>
      </tr>`).join('');
    updateCount(rows.length);
  }

  function updateCount(n) {
    const el = $('bw-count');
    if (el) el.textContent = n === _data.length ? `Showing all ${n} words` : `Showing ${n} of ${_data.length} words`;
  }

  function wireSort() {
    document.querySelectorAll('[data-bw-sort]').forEach(th => {
      th.style.cursor = 'pointer';
      th.addEventListener('click', () => {
        const col = th.dataset.bwSort;
        if (_sortCol === col) {
          _sortAsc = !_sortAsc;
        } else {
          _sortCol = col;
          _sortAsc = col === 'rank';
        }
        document.querySelectorAll('[data-bw-sort]').forEach(h => h.removeAttribute('aria-sort'));
        th.setAttribute('aria-sort', _sortAsc ? 'ascending' : 'descending');
        render();
      });
    });
  }

  function wireSearch() {
    const inp = $('bw-search');
    if (!inp) return;
    inp.addEventListener('input', () => {
      _query = inp.value.trim();
      render();
    });
  }

  return { init: loadAndRender };
})();

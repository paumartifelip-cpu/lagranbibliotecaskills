(function () {
  'use strict';
  var ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="9" y="9" width="12" height="12" rx="2" fill="none"/><path d="M5 15V5a2 2 0 0 1 2-2h10" fill="none"/></svg>';
  var CHECK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12l5 5L20 7" fill="none"/></svg>';
  var page = document.body.getAttribute('data-page');

  /* ---------- copiar ---------- */
  function setIdle(btn) { btn.classList.remove('ok'); btn.innerHTML = ICON + '<span>' + (btn.getAttribute('data-label') || 'Copiar') + '</span>'; }
  function setOk(btn, msg) { btn.classList.add('ok'); btn.innerHTML = CHECK + '<span>' + msg + '</span>'; setTimeout(function () { setIdle(btn); }, 2000); }
  function fallbackCopy(text, btn) {
    var ok = false;
    try {
      var ta = document.createElement('textarea');
      ta.value = text; ta.setAttribute('readonly', ''); ta.style.cssText = 'position:fixed;top:0;opacity:0';
      document.body.appendChild(ta); ta.select(); ok = document.execCommand('copy'); document.body.removeChild(ta);
    } catch (e) {}
    setOk(btn, ok ? 'Copiado' : 'No se pudo copiar');
  }
  function copyText(text, btn) {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(function () { setOk(btn, 'Copiado'); }, function () { fallbackCopy(text, btn); });
    } else fallbackCopy(text, btn);
  }
  // botones estáticos (paso a paso)
  document.querySelectorAll('.prompt > .copy').forEach(function (btn) {
    setIdle(btn);
    btn.addEventListener('click', function () {
      copyText(btn.parentElement.querySelector('pre').textContent.replace(/^\n+|\n+$/g, ''), btn);
    });
  });

  var S = window.SKILLS || [], C = window.CATS || [];
  if (!S.length) return;
  var CAT = {}; C.forEach(function (c) { CAT[c[0]] = c; });
  var GOAL = { G: ['💰 Ganar más', 'g'], T: ['⏱ Automatizar', 't'], L: ['🕊 Libertad', 'l'] };
  var FUNC = { V: 'Vender y captar', C: 'Atender y comunicar', M: 'Redes y marketing', A: 'Cobros y números', O: 'Organización', E: 'Equipo', F: 'Enseñar y documentar' };
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function norm(s) { return s.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, ''); }
  S.forEach(function (s) { s.push(norm(s[1] + ' ' + s[2] + ' ' + CAT[s[6]][1])); }); // s[7] = texto de búsqueda

  /* ---------- selección guardada ---------- */
  var KEY = 'miSeleccionSkills';
  var pack = [];
  try { pack = JSON.parse(localStorage.getItem(KEY) || '[]'); } catch (e) { pack = []; }
  function savePack() { try { localStorage.setItem(KEY, JSON.stringify(pack)); } catch (e) {} renderBar(); }
  function toggle(id) { var i = pack.indexOf(id); if (i < 0) pack.push(id); else pack.splice(i, 1); savePack(); }
  var bar = document.getElementById('packbar');
  function renderBar() {
    document.querySelectorAll('.star').forEach(function (b) {
      var on = pack.indexOf(+b.getAttribute('data-id')) >= 0; b.classList.toggle('on', on);
      b.textContent = on ? '★' : '☆'; b.setAttribute('aria-pressed', on);
    });
    if (!bar) return;
    if (!pack.length) { bar.hidden = true; return; }
    bar.hidden = false;
    bar.innerHTML = '⭐<b>' + pack.length + '</b> guardadas <button type="button" data-a="list">Copiar lista</button><button type="button" data-a="texts">Copiar los textos</button><button type="button" class="x" data-a="clear">Vaciar</button>';
  }
  if (bar) bar.addEventListener('click', function (e) {
    var a = e.target.getAttribute && e.target.getAttribute('data-a'); if (!a) return;
    if (a === 'clear') { if (confirm('¿Vaciar tu selección?')) { pack = []; savePack(); } return; }
    var items = pack.map(function (id) { return S[id]; });
    var text = a === 'list'
      ? items.map(function (s, i) { return (i + 1) + '. ' + s[1] + ' (' + CAT[s[6]][1] + '): ' + s[2]; }).join('\n')
      : items.map(function (s) { return s[3]; }).join('\n\n---\n\n');
    var old = e.target.textContent;
    copyText(text, e.target); setTimeout(function () { e.target.textContent = old; }, 2100);
  });

  /* ---------- tarjeta de skill ---------- */
  function card(s, extra) {
    var g = GOAL[s[4]];
    return '<article class="sk" data-id="' + s[0] + '"><div class="sk-top"><div class="sk-h"><b>' + esc(s[1]) + '</b><span>' + esc(s[2]) + '</span></div>' +
      '<button type="button" class="star" data-id="' + s[0] + '" aria-label="Guardar skill" title="Guardar en mi selección">☆</button></div>' +
      '<div class="tags"><span class="tag">' + esc(CAT[s[6]][1]) + '</span><span class="tag ' + g[1] + '">' + g[0] + '</span><span class="tag">' + FUNC[s[5]] + '</span></div>' +
      (extra || '') +
      '<div class="sk-act"><button type="button" class="copy" data-id="' + s[0] + '"></button><button type="button" class="ghost" data-view="' + s[0] + '">Ver texto</button></div>' +
      '<div class="view" hidden></div></article>';
  }
  function bindCards(root) {
    root.querySelectorAll('.copy[data-id]').forEach(function (b) { if (!b.innerHTML) setIdle(b); });
  }
  function delegate(root) {
    root.addEventListener('click', function (e) {
      var t = e.target.closest('button'); if (!t) return;
      if (t.classList.contains('star')) { toggle(+t.getAttribute('data-id')); return; }
      if (t.classList.contains('copy') && t.hasAttribute('data-id')) { copyText(S[+t.getAttribute('data-id')][3], t); return; }
      if (t.hasAttribute('data-view')) {
        var art = t.closest('.sk'), v = art.querySelector('.view');
        if (v.hidden) { v.innerHTML = '<pre>' + esc(S[+t.getAttribute('data-view')][3]) + '</pre>'; v.hidden = false; t.textContent = 'Ocultar texto'; }
        else { v.hidden = true; t.textContent = 'Ver texto'; }
      }
    });
  }

  /* ---------- BIBLIOTECA ---------- */
  if (page === 'skills') {
    var st = { kind: 'prof', cat: '', goal: '', func: '', q: '', shown: 40 };
    var $ = function (id) { return document.getElementById(id); };
    var list = $('list'), more = $('more'), picker = $('picker'), status = $('status'), crumb = $('crumb'), sugg = $('sugg');
    var total = { prof: 0, tarea: 0 };
    C.forEach(function (c) { total[c[2]] += c[3]; });
    $('n-prof').textContent = C.filter(function (c) { return c[2] === 'prof'; }).length;
    $('n-tarea').textContent = C.filter(function (c) { return c[2] === 'tarea'; }).length;

    function chip(label, val, on, count, attr) { return '<button type="button" class="chip' + (on ? ' on' : '') + '" ' + (attr || 'data-v') + '="' + val + '">' + esc(label) + (count != null ? '<small>' + count + '</small>' : '') + '</button>'; }
    function matches(s) {
      if (st.goal && s[4] !== st.goal) return false;
      if (st.func && s[5] !== st.func) return false;
      if (st.cat && s[6] !== st.cat) return false;
      if (st.q) { var ws = norm(st.q).split(/\s+/); for (var i = 0; i < ws.length; i++) if (s[7].indexOf(ws[i]) < 0) return false; }
      return true;
    }
    function renderFilters() {
      $('f-goal').innerHTML = chip('Todos', '', !st.goal) + Object.keys(GOAL).map(function (k) { return chip(GOAL[k][0], k, st.goal === k); }).join('');
      $('f-func').innerHTML = chip('Todas', '', !st.func) + Object.keys(FUNC).map(function (k) { return chip(FUNC[k], k, st.func === k); }).join('');
      document.querySelectorAll('.tab').forEach(function (t) { t.classList.toggle('on', t.getAttribute('data-kind') === st.kind); });
    }
    function renderPicker() {
      if (st.cat || st.q) { picker.innerHTML = ''; return; }
      var byCat = function (c) { return chip(c[1], c[0], false, c[3], 'data-cat'); };
      if (st.kind === 'prof') {
        picker.innerHTML = '<div class="sectors">' + (window.SECTORS || []).map(function (sec) {
          var cs = C.filter(function (c) { return c[2] === 'prof' && c[4] === sec; }).sort(function (a, b) { return a[1].localeCompare(b[1], 'es'); });
          return cs.length ? '<div class="sector"><h3>' + esc(sec) + '</h3><div class="chips">' + cs.map(byCat).join('') + '</div></div>' : '';
        }).join('') + '</div>';
      } else {
        picker.innerHTML = '<div class="chips">' + C.filter(function (c) { return c[2] === 'tarea'; }).sort(function (a, b) { return a[1].localeCompare(b[1], 'es'); }).map(byCat).join('') + '</div>';
      }
    }
    function renderSugg() {
      if (!st.q || st.cat) { sugg.hidden = true; return; }
      var t = norm(st.q), hits = C.filter(function (c) { return norm(c[1]).indexOf(t) >= 0; }).slice(0, 12);
      if (!hits.length) { sugg.hidden = true; return; }
      sugg.hidden = false;
      sugg.innerHTML = '<h3>¿Buscas una de estas?</h3><div class="chips">' + hits.map(function (c) { return chip(c[1], c[0], false, c[3], 'data-cat'); }).join('') + '</div>';
    }
    function render() {
      renderFilters(); renderPicker(); renderSugg();
      if (st.cat) { crumb.hidden = false; crumb.innerHTML = '<h2>' + esc(CAT[st.cat][1]) + '</h2><button type="button" data-clear="1">← Todas las categorías</button>'; }
      else crumb.hidden = true;
      if (!st.cat && !st.q && !st.goal && !st.func) {
        status.textContent = 'Elige ' + (st.kind === 'prof' ? 'tu profesión' : 'una tarea') + ', o usa el buscador y los filtros. Hay ' + total.prof + ' skills por profesión y ' + total.tarea + ' por tarea.';
        list.innerHTML = ''; more.hidden = true; return;
      }
      var res = S.filter(function (s) { return (st.cat || st.q || CAT[s[6]][2] === st.kind) && matches(s); });
      status.textContent = res.length + (res.length === 1 ? ' skill' : ' skills') + (st.cat ? '' : st.q ? ' para «' + st.q + '»' : '');
      var vis = res.slice(0, st.shown), html = '';
      if (st.cat && !st.goal) { // agrupado por objetivo
        ['G', 'T', 'L'].forEach(function (g) {
          var part = vis.filter(function (s) { return s[4] === g; }); if (!part.length) return;
          html += '<h3 class="gh">' + GOAL[g][0] + '<small>' + part.length + '</small></h3>' + part.map(function (s) { return card(s); }).join('');
        });
      } else html = vis.map(function (s) { return card(s); }).join('');
      list.innerHTML = html || '<p class="empty" style="display:block">No hay skills con ese filtro. Prueba otra palabra o quita algún filtro.</p>';
      more.hidden = res.length <= st.shown;
      more.textContent = 'Mostrar más (' + (res.length - st.shown) + ' restantes)';
      bindCards(list); renderBar();
    }
    function reset() { st.shown = 40; render(); }
    function pick(id) { st.cat = id; if (id) st.kind = CAT[id][2]; st.q = ''; $('q').value = ''; reset(); window.scrollTo({ top: document.querySelector('.tabs').offsetTop + 120, behavior: 'smooth' }); }
    document.querySelector('.filters').addEventListener('click', function (e) {
      var b = e.target.closest('.chip'); if (!b) return;
      var grp = b.parentElement.id === 'f-goal' ? 'goal' : 'func'; st[grp] = b.getAttribute('data-v'); reset();
    });
    [picker, sugg].forEach(function (el) { el.addEventListener('click', function (e) { var b = e.target.closest('[data-cat]'); if (b) pick(b.getAttribute('data-cat')); }); });
    crumb.addEventListener('click', function (e) { if (e.target.hasAttribute('data-clear')) { st.cat = ''; reset(); } });
    document.querySelector('.tabs').addEventListener('click', function (e) { var b = e.target.closest('.tab'); if (!b) return; st.kind = b.getAttribute('data-kind'); st.cat = ''; reset(); });
    $('q').addEventListener('input', function () { st.q = this.value.trim(); if (st.q) st.cat = ''; reset(); });
    more.addEventListener('click', function () { st.shown += 40; render(); });
    delegate(list);
    var h = location.hash.match(/cat=([\w]+)/);
    if (h && CAT[h[1]]) { st.cat = h[1]; st.kind = CAT[h[1]][2]; }
    render();
  }

  /* ---------- CUESTIONARIO ---------- */
  if (page === 'quiz') {
    var form = document.getElementById('quiz'), res = document.getElementById('quiz-res');
    delegate(res);
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var prof = document.getElementById('q-prof').value;
      var goal = form.querySelector('input[name=g]:checked').value;
      var funcs = Array.prototype.map.call(form.querySelectorAll('input[name=f]:checked'), function (i) { return i.value; });
      var n = +form.querySelector('input[name=n]:checked').value;
      if (!prof) { alert('Elige primero a qué te dedicas.'); document.getElementById('q-prof').focus(); return; }
      var scored = S.map(function (s) {
        var sc = 0, c = CAT[s[6]];
        if (prof !== 'otra' && s[6] === prof) sc += 10;
        else if (c[2] === 'prof') sc -= 6; // otra profesión: solo si encaja muy bien
        if (s[4] === goal) sc += 4;
        if (funcs.indexOf(s[5]) >= 0) sc += 3;
        if (c[2] === 'tarea') sc += (prof === 'otra' ? 3 : 1);
        if (s[6] === 'tlib' && goal === 'L') sc += 3;
        return { s: s, sc: sc, o: s[0] };
      }).sort(function (a, b) { return b.sc - a.sc || a.o - b.o; });
      var out = [], per = {};
      scored.forEach(function (x) {
        if (out.length >= n) return;
        var k = x.s[6]; per[k] = per[k] || 0;
        if (prof === 'otra' && per[k] >= 3) return;
        per[k]++; out.push(x.s);
      });
      var pname = prof === 'otra' ? 'tu perfil' : CAT[prof][1];
      res.hidden = false;
      res.innerHTML = '<div class="res-head"><p class="block-eyebrow">Tus resultados</p><h2 class="block-title">Tus ' + out.length + ' skills para empezar</h2>' +
        '<p class="block-lead">Para <b>' + esc(pname) + '</b> · objetivo: ' + GOAL[goal][0] + (funcs.length ? ' · te quita tiempo: ' + funcs.map(function (f) { return FUNC[f].toLowerCase(); }).join(', ') : '') + '</p></div>' +
        '<p class="res-note"><b>Cómo seguir:</b> empieza por la primera. Pulsa <b>Copiar</b>, pégala en ChatGPT o Codex y contesta sus preguntas. Después prueba y corrige tu skill con el <a href="paso-a-paso.html">paso a paso</a>. Con ⭐ guardas las que quieras revisar luego.</p>' +
        '<div class="list">' + out.map(function (s, i) { return card(s, '<div class="tags"><span class="tag" style="background:#F2E3C4">Recomendada nº ' + (i + 1) + '</span></div>'); }).join('') + '</div>' +
        '<div class="cta-row"><a class="btn dark" href="skills.html' + (prof !== 'otra' ? '#cat=' + prof : '') + '">Ver todas las skills de ' + (prof === 'otra' ? 'la biblioteca' : esc(pname)) + ' →</a></div>';
      bindCards(res); renderBar();
      res.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
  }
  renderBar();
})();

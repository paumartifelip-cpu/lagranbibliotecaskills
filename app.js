
(function () {
  var ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="9" y="9" width="12" height="12" rx="2" fill="none"/><path d="M5 15V5a2 2 0 0 1 2-2h10" fill="none"/></svg>';
  var CHECK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12l5 5L20 7" fill="none"/></svg>';
  function setIdle(btn) { btn.classList.remove('ok'); btn.innerHTML = ICON + '<span>Copiar</span>'; }
  function setOk(btn, msg) { btn.classList.add('ok'); btn.innerHTML = CHECK + '<span>' + msg + '</span>'; setTimeout(function () { setIdle(btn); }, 2200); }
  function selectText(el) {
    try { var r = document.createRange(); r.selectNodeContents(el); var s = window.getSelection(); s.removeAllRanges(); s.addRange(r); } catch (e) {}
  }
  function fallbackCopy(text, pre, btn) {
    var ok = false;
    try {
      var ta = document.createElement('textarea');
      ta.value = text; ta.setAttribute('readonly', ''); ta.style.position = 'fixed'; ta.style.top = '0'; ta.style.opacity = '0';
      document.body.appendChild(ta); ta.select(); ok = document.execCommand('copy'); document.body.removeChild(ta);
    } catch (e) { ok = false; }
    if (ok) { setOk(btn, 'Copiado'); }
    else { selectText(pre); setOk(btn, 'Seleccionado: pulsa copiar'); }
  }
  document.querySelectorAll('.copy').forEach(function (btn) {
    setIdle(btn);
    btn.addEventListener('click', function () {
      var pre = btn.parentElement.querySelector('pre');
      var text = pre.textContent.replace(/^\n+|\n+$/g, '');
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(function () { setOk(btn, 'Copiado'); }, function () { fallbackCopy(text, pre, btn); });
      } else { fallbackCopy(text, pre, btn); }
    });
  });
})();

(function () {
  var q = document.getElementById('q'); if (!q) return;
  var areas = document.querySelectorAll('.area'), empty = document.getElementById('empty');
  function norm(s) { return s.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, ''); }
  q.addEventListener('input', function () {
    var t = norm(q.value.trim()), any = false;
    areas.forEach(function (a) {
      var n = 0;
      a.querySelectorAll('.sk').forEach(function (li) {
        var ok = !t || norm(li.textContent).indexOf(t) >= 0; li.hidden = !ok; if (ok) n++;
      });
      a.hidden = n === 0; if (n) any = true;
      if (t && n) a.open = true;
    });
    empty.style.display = any ? 'none' : 'block';
  });
})();

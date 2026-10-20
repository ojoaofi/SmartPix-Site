/* Projetos: filters + detail view.
   Desktop: the detail grows out of the card that opened it and returns into it.
   Phone: a bottom sheet that tracks the finger 1:1 and dismisses with momentum (Apple drawer spring: damping 0.8, response 0.3). */
(function () {
  'use strict';
  var D = document, SP = window.SP, grid = D.getElementById('pgrid'), dlg = D.getElementById('pd');
  if (!grid || !SP) return;
  var chips = [].slice.call(D.querySelectorAll('[data-filter]')), cards = [].slice.call(grid.querySelectorAll('.card'));
  function plural(n) { return n + (n === 1 ? ' tipo de projeto' : ' tipos de projeto'); }
  chips.forEach(function (c) {
    c.addEventListener('click', function () {
      var f = c.getAttribute('data-filter');
      chips.forEach(function (x) { x.setAttribute('aria-pressed', x === c); });
      cards.forEach(function (k) { k.hidden = f !== 'todos' && (k.getAttribute('data-cat') || '').indexOf(f) < 0; });
      D.getElementById('pcount').textContent = plural(cards.filter(function (k) { return !k.hidden; }).length);
      SP.track('project_filter', { filter: f });
    });
  });
  if (!dlg || !dlg.showModal) return;

  var mq = matchMedia('(max-width: 734px)'), opener = null, sp = new SP.Spring({ from: 0, to: 0, damping: 1, response: 0.38 }), anim = null, closing = false;
  function sheet() { return mq.matches; }
  /* p: 0 = gone, 1 = presented. The scrim follows the same value so material and dimming move together. */
  function paint(p) {
    dlg.style.setProperty('--bd', Math.max(0, Math.min(1, p)).toFixed(3));
    if (sheet()) { dlg.style.opacity = 1; dlg.style.transform = 'translateY(' + ((1 - p) * dlg.offsetHeight).toFixed(1) + 'px)'; return; }
    dlg.style.opacity = Math.max(0, Math.min(1, p * 1.4)).toFixed(3);
    dlg.style.transform = 'translate(' + (dlg._dx * (1 - p)).toFixed(1) + 'px,' + (dlg._dy * (1 - p)).toFixed(1) + 'px) scale(' + (0.86 + 0.14 * p).toFixed(4) + ')';
  }
  function origin() { var r = opener.closest('.card').getBoundingClientRect(), cx = r.left + r.width / 2 - innerWidth / 2, cy = r.top + r.height / 2 - innerHeight / 2; dlg._dx = cx * 0.5; dlg._dy = cy * 0.5; }
  function animate(to, cfg, v, done) {
    if (anim) anim.stop(); sp.to = to; sp.config(cfg[0], cfg[1]); if (v != null) sp.v = v;
    if (SP.reduce) { sp.x = to; sp.v = 0; paint(to); if (done) done(); return; }
    var fin = false, f = function () { if (fin) return; fin = true; if (done) done(); };
    anim = SP.run(sp, function (p) { paint(p); if (to === 0 && p < 0.02) { anim.stop(); f(); } }, f, 0.005);
  }
  function open(card) {
    opener = card.querySelector('.card-open') || card; closing = false;
    var box = dlg.querySelector('.pd-content'); box.innerHTML = card.querySelector('.card-detail').innerHTML;
    var h = box.querySelector('h2'); if (h) h.id = 'pd-title';
    dlg.showModal(); dlg.scrollTop = 0; origin(); sp.x = 0; sp.v = 0; paint(0);
    animate(1, [1, sheet() ? 0.42 : 0.38]);
    SP.track('project_open', { project: card.getAttribute('data-id') });
  }
  function close(v) {
    if (!dlg.open || closing) return; closing = true; origin();
    animate(0, sheet() ? [1, 0.32] : [1, 0.38], v, function () { dlg.close(); });
    setTimeout(function () { if (dlg.open && closing) dlg.close(); }, 900);
  }
  cards.forEach(function (c) { c.addEventListener('click', function () { open(c); }); });
  dlg.addEventListener('click', function (e) { if (e.target === dlg && !sheetDrag.moved || e.target.closest('[data-close]')) close(); });
  dlg.addEventListener('cancel', function (e) { e.preventDefault(); close(); });
  dlg.addEventListener('close', function () { closing = false; if (opener) opener.focus(); });

  /* ---- sheet drag-to-dismiss (phone) ---- */
  var sheetDrag = { on: false, decided: false, moved: false, y0: 0, p0: 1, tr: null };
  dlg.addEventListener('pointerdown', function (e) {
    if (!sheet() || closing || e.target.closest('a,button') || e.target === dlg) return;
    sheetDrag.on = true; sheetDrag.decided = false; sheetDrag.moved = false; sheetDrag.y0 = e.clientY; sheetDrag.tr = new SP.Tracker();
  });
  dlg.addEventListener('pointermove', function (e) {
    var s = sheetDrag; if (!s.on) return;
    var dy = e.clientY - s.y0, h = dlg.offsetHeight || 1;
    if (!s.decided) {
      if (Math.abs(dy) < 10) return; s.decided = true;
      /* only take over a downward pull that starts at the top of the sheet; otherwise let it scroll */
      if (dy < 0 || dlg.scrollTop > 0) { s.on = false; return; }
      s.moved = true; if (anim) anim.stop(); s.p0 = sp.x; s.y0 = e.clientY; dy = 0;
      try { dlg.setPointerCapture(e.pointerId); } catch (_) {}
    }
    var p = s.p0 - dy / h; if (p > 1) p = 1 + SP.rubberband(p - 1, 1, 0.3); /* resist pulling up past the top */
    sp.x = p; s.tr.add(p, e.timeStamp); paint(p);
  });
  function release() {
    var s = sheetDrag; if (!s.on) return; s.on = false; if (!s.moved) return;
    var v = s.tr.v(), end = sp.x + SP.project(v, 0.99);
    if (end < 0.6) { closing = false; close(v); } else { animate(1, [0.8, 0.3], v); } /* momentum decides, not position alone */
    setTimeout(function () { s.moved = false; }, 0);
  }
  dlg.addEventListener('dragstart', function (e) { e.preventDefault(); });
  dlg.addEventListener('pointerup', release); dlg.addEventListener('pointercancel', release);

  if (location.hash) { var pre = D.getElementById(location.hash.slice(1)); if (pre && cards.indexOf(pre) > -1) setTimeout(function () { pre.scrollIntoView({ block: 'center' }); }, 50); }
})();

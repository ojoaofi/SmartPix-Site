/* Projetos: filters + a detail sheet that grows out of the card that opened it and returns to it. */
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
  var opener = null, sp = new SP.Spring({ from: 0, to: 0, damping: 1, response: 0.38 }), anim = null;
  function paint(p) { dlg.style.opacity = Math.min(1, p * 1.4).toFixed(3); dlg.style.transform = 'translate(' + (dlg._dx * (1 - p)).toFixed(1) + 'px,' + (dlg._dy * (1 - p)).toFixed(1) + 'px) scale(' + (0.86 + 0.14 * p).toFixed(4) + ')'; }
  function origin() { var r = opener.closest('.card').getBoundingClientRect(), cx = r.left + r.width / 2 - innerWidth / 2, cy = r.top + r.height / 2 - innerHeight / 2; dlg._dx = cx * 0.5; dlg._dy = cy * 0.5; }
  function open(card) {
    opener = card.querySelector('.card-open') || card; var box = dlg.querySelector('.pd-content'); box.innerHTML = card.querySelector('.card-detail').innerHTML; var h = box.querySelector('h2'); if (h) h.id = 'pd-title';
    dlg.showModal(); origin(); sp.to = 1;
    if (SP.reduce) { sp.x = 1; paint(1); } else { sp.x = 0; paint(0); if (anim) anim.stop(); anim = SP.run(sp, paint); }
    SP.track('project_open', { project: card.getAttribute('data-id') });
  }
  function close() {
    if (!dlg.open) return; origin(); sp.to = 0;
    if (SP.reduce) { dlg.close(); return; }
    if (anim) anim.stop(); var done = false, fin = function () { if (done) return; done = true; if (anim) anim.stop(); dlg.close(); };
    anim = SP.run(sp, function (p) { paint(p); if (p < 0.04) fin(); }, fin, 0.01); setTimeout(fin, 700);
  }
  cards.forEach(function (c) { c.addEventListener('click', function () { open(c); }); });
  if (location.hash) { var pre = D.getElementById(location.hash.slice(1)); if (pre && cards.indexOf(pre) > -1) setTimeout(function () { pre.scrollIntoView({ block: 'center' }); }, 50); }
  dlg.addEventListener('click', function (e) { if (e.target === dlg || e.target.closest('[data-close]')) close(); });
  dlg.addEventListener('cancel', function (e) { e.preventDefault(); close(); });
  dlg.addEventListener('close', function () { if (opener) opener.focus(); });
})();

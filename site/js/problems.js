/* Problemas → soluções: tabs + before/after comparison.
   The divider tracks the finger 1:1, then carries its release velocity into a spring (drawer feel: damping 0.8, response 0.3).
   Choosing a problem plays a short reveal that hints the direction of the gesture. */
(function () {
  'use strict';
  var D = document, SP = window.SP, root = D.getElementById('px');
  if (!root || !SP) return;
  var tabs = [].slice.call(root.querySelectorAll('[role=tab]')), panels = [].slice.call(root.querySelectorAll('[role=tabpanel]'));

  function setup(panel) {
    var ba = panel.querySelector('.ba'); if (!ba || ba._sp) return ba && ba._sp;
    var handle = ba.querySelector('.handle'), x = new SP.Spring({ from: 50, to: 50, damping: 0.8, response: 0.3 }), anim = null, drag = false, tr = null, used = false;
    function paint(v) { var c = Math.max(0, Math.min(100, v)), r = Math.round(c); ba.style.setProperty('--x', c.toFixed(2) + '%'); if (+handle.getAttribute('aria-valuenow') !== r) { handle.setAttribute('aria-valuenow', r); handle.setAttribute('aria-valuetext', r + '% antes, ' + (100 - r) + '% depois'); } }
    function to(t, cfg) { x.to = t; if (cfg) x.config(cfg[0], cfg[1]); if (SP.reduce) { x.x = t; x.v = 0; paint(t); return; } if (!anim || !anim.alive) anim = SP.run(x, paint, null, 0.02); }
    function pct(e) { var b = ba.getBoundingClientRect(); return (e.clientX - b.left) / b.width * 100; }
    var off = 0, chase = false;
    ba.addEventListener('pointerdown', function (e) {
      drag = true; tr = new SP.Tracker();
      var p = pct(e), cur = x.x, hw = 1.375 * 16 / ba.getBoundingClientRect().width * 100;
      if (Math.abs(p - cur) <= hw) { /* grabbed the divider: keep the grab offset, track 1:1 */ if (anim) anim.stop(); x.v = 0; off = cur - p; chase = false; }
      else { /* tapped elsewhere: the divider travels to the finger on a spring, then follows */ off = 0; chase = true; to(p, [1, 0.28]); }
      tr.add(cur, e.timeStamp);
      try { ba.setPointerCapture(e.pointerId); } catch (_) {}
      if (!used) { used = true; SP.track('problem_compare', { problem: panel.id }); }
    });
    ba.addEventListener('pointermove', function (e) {
      if (!drag) return; var p = pct(e) + off, over = p < 0 ? p : p > 100 ? p - 100 : 0, t = over ? (p < 0 ? SP.rubberband(over, 100) : 100 + SP.rubberband(over, 100)) : p;
      if (chase && Math.abs(t - x.x) > 1.5 && anim && anim.alive) { x.to = t; tr.add(x.x, e.timeStamp); return; }
      chase = false; if (anim) anim.stop(); x.x = t; x.to = t; tr.add(t, e.timeStamp); paint(t);
    });
    function up() {
      if (!drag) return; drag = false;
      if (chase) { chase = false; return; } /* a tap: let the spring finish at the tapped point */
      var v = tr.v(), end = x.x + SP.project(v, 0.99), target = end < 10 ? 0 : end > 90 ? 100 : Math.max(0, Math.min(100, end));
      x.v = v; to(target, [0.8, 0.3]);
    }
    ba.addEventListener('pointerup', up); ba.addEventListener('pointercancel', up);
    handle.addEventListener('keydown', function (e) {
      var k = e.key, step = e.shiftKey ? 20 : 5, t = x.to;
      if (k === 'ArrowLeft' || k === 'ArrowDown') t -= step; else if (k === 'ArrowRight' || k === 'ArrowUp') t += step; else if (k === 'PageDown') t -= 20; else if (k === 'PageUp') t += 20; else if (k === 'Home') t = 0; else if (k === 'End') t = 100; else return;
      e.preventDefault(); to(Math.max(0, Math.min(100, t)), [1, 0.3]);
    });
    ba._sp = { reveal: function () { if (SP.reduce) { paint(50); x.x = x.to = 50; return; } x.x = 86; x.v = 0; paint(86); to(50, [1, 0.7]); } };
    return ba._sp;
  }

  function select(i, focus) {
    tabs.forEach(function (t, j) { var on = j === i; t.setAttribute('aria-selected', on); t.tabIndex = on ? 0 : -1; panels[j].hidden = !on; });
    if (focus) tabs[i].focus();
    var s = setup(panels[i]); if (s) s.reveal();
    SP.track('problem_view', { problem: panels[i].id });
  }
  tabs.forEach(function (t, i) {
    t.addEventListener('click', function () { select(i); });
    t.addEventListener('keydown', function (e) {
      var n = tabs.length, j = i;
      if (e.key === 'ArrowDown' || e.key === 'ArrowRight') j = (i + 1) % n; else if (e.key === 'ArrowUp' || e.key === 'ArrowLeft') j = (i - 1 + n) % n; else if (e.key === 'Home') j = 0; else if (e.key === 'End') j = n - 1; else return;
      e.preventDefault(); select(j, true);
    });
  });
  setup(panels[0]);
  /* first reveal when the section scrolls in */
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { var s = setup(panels.filter(function (p) { return !p.hidden; })[0]); if (s) s.reveal(); io.disconnect(); } }); }, { threshold: 0.45 });
    io.observe(root);
  }
})();

/* Smart Pix — shared behaviour: springs, nav, analytics, WhatsApp, entry motion. */
(function () {
  'use strict';
  var W = window, D = document;
  var reduce = W.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  var WA = '5511910101324';

  /* ---------- Springs (Apple model: damping ratio + response). Interruptible: retarget keeps x and v. ---------- */
  function Spring(o) { this.x = o.from || 0; this.v = o.velocity || 0; this.to = o.to == null ? this.x : o.to; this.config(o.damping == null ? 1 : o.damping, o.response || 0.4); }
  Spring.prototype.config = function (damping, response) { this.k = Math.pow(2 * Math.PI / response, 2); this.c = 4 * Math.PI * damping / response; return this; };
  Spring.prototype.step = function (dt) {
    var h = 1 / 240, n = Math.max(1, Math.round(dt / h)); h = dt / n;
    for (var i = 0; i < n; i++) { var a = -this.k * (this.x - this.to) - this.c * this.v; this.v += a * h; this.x += this.v * h; }
    return this.x;
  };
  Spring.prototype.settled = function (eps) { eps = eps || 0.001; return Math.abs(this.x - this.to) < eps && Math.abs(this.v) < eps * 10; };
  function run(spring, onUpdate, onDone, eps) {
    var last = 0, raf = 0, alive = true;
    function f(t) { if (!alive) return; var dt = last ? Math.min(0.05, (t - last) / 1000) : 1 / 60; last = t; onUpdate(spring.step(dt)); if (spring.settled(eps)) { spring.x = spring.to; spring.v = 0; onUpdate(spring.x); alive = false; if (onDone) onDone(); return; } raf = requestAnimationFrame(f); }
    raf = requestAnimationFrame(f);
    return { stop: function () { alive = false; cancelAnimationFrame(raf); }, get alive() { return alive; } };
  }
  /* Apple's momentum projection (Designing Fluid Interfaces) */
  function project(v, rate) { rate = rate || 0.998; return (v / 1000) * rate / (1 - rate); }
  function rubberband(over, dim, c) { c = c || 0.55; return (over * dim * c) / (dim + c * Math.abs(over)); }
  /* velocity tracker from the last pointer samples */
  function Tracker() { this.s = []; }
  Tracker.prototype.add = function (x, t) { this.s.push([x, t]); if (this.s.length > 6) this.s.shift(); };
  Tracker.prototype.v = function () { var s = this.s; if (s.length < 2) return 0; var a = s[0], b = s[s.length - 1], dt = (b[1] - a[1]) / 1000; return dt > 0 ? (b[0] - a[0]) / dt : 0; };

  /* ---------- Analytics (GA4 / Tag Manager ready) ---------- */
  W.dataLayer = W.dataLayer || [];
  var attr = {};
  try {
    var q = new URLSearchParams(location.search);
    ['utm_source', 'utm_medium', 'utm_campaign'].forEach(function (k) { if (q.get(k)) attr[k] = q.get(k); });
    if (Object.keys(attr).length) sessionStorage.setItem('sp_attr', JSON.stringify(attr)); else attr = JSON.parse(sessionStorage.getItem('sp_attr') || '{}');
  } catch (e) { attr = {}; }
  function track(ev, p) { try { W.dataLayer.push(Object.assign({ event: ev, page: location.pathname.split('/').pop() || 'index' }, attr, p || {})); } catch (e) {} }
  function waLink(text) { return 'https://wa.me/' + WA + '?text=' + encodeURIComponent(text); }

  /* one polite live region for short confirmations (copy, steppers) */
  var live = D.createElement('p'); live.className = 'sr'; live.setAttribute('aria-live', 'polite'); D.body.appendChild(live);
  function say(t) { live.textContent = ''; setTimeout(function () { live.textContent = t; }, 60); }
  W.SP = { Spring: Spring, run: run, project: project, rubberband: rubberband, Tracker: Tracker, track: track, waLink: waLink, reduce: reduce, attr: attr, WA: WA, say: say };
  try { var mq = matchMedia('(prefers-reduced-motion: reduce)'); mq.addEventListener('change', function () { reduce = W.SP.reduce = mq.matches; }); } catch (e) {}

  D.addEventListener('click', function (e) {
    var el = e.target.closest('[data-cta]'); if (el) track('cta_click', { cta: el.getAttribute('data-cta') });
    var wa = e.target.closest('a[href*="wa.me/"]'); if (wa) track('whatsapp_click', { cta: wa.getAttribute('data-cta') || 'link' });
  });

  /* ---------- Nav: scroll-edge effect only once content passes under it ---------- */
  var nav = D.querySelector('.nav');
  function edge() { if (nav) nav.style.setProperty('--edge', scrollY > 8 ? 1 : 0); }
  addEventListener('scroll', edge, { passive: true }); edge();

  /* ---------- Menu sheet: scales out of its trigger, closes back into it ---------- */
  var btn = D.getElementById('menuBtn'), sheet = D.getElementById('sheet'), scrim = D.getElementById('scrim');
  if (btn && sheet) {
    var sp = new Spring({ from: 0, to: 0, damping: 1, response: 0.32 }), anim = null, open = false;
    function paint(p) { sheet.style.transform = 'scale(' + (0.6 + 0.4 * p).toFixed(4) + ')'; sheet.style.opacity = Math.max(0, Math.min(1, p)).toFixed(3); }
    function setOpen(v) {
      open = v; btn.setAttribute('aria-expanded', v); scrim.classList.toggle('open', v);
      if (v) { sheet.classList.add('vis'); sheet.removeAttribute('inert'); }
      [D.querySelector('main'), D.querySelector('.foot'), D.getElementById('dock'), D.querySelector('.nav-links'), D.querySelector('.brand'), D.querySelector('.nav-wa'), D.querySelector('.nav-cta')].forEach(function (el) { if (el) el.inert = v; });
      sp.to = v ? 1 : 0;
      if (reduce) { sp.x = sp.to; paint(sp.x); if (!v) { sheet.classList.remove('vis'); sheet.setAttribute('inert', ''); } }
      else { if (anim) anim.stop(); anim = run(sp, paint, function () { if (!open) { sheet.classList.remove('vis'); sheet.setAttribute('inert', ''); } }); }
      if (v) setTimeout(function () { var f = sheet.querySelector('a,button'); if (f) f.focus(); }, 30); else btn.focus();
      track('menu', { open: v });
    }
    sheet.setAttribute('inert', '');
    btn.addEventListener('click', function () { setOpen(!open); });
    scrim.addEventListener('click', function () { setOpen(false); });
    sheet.addEventListener('click', function (e) { if (e.target.closest('a') || e.target.closest('[data-close]')) setOpen(false); });
    D.addEventListener('keydown', function (e) {
      if (!open) return;
      if (e.key === 'Escape') { setOpen(false); return; }
      if (e.key === 'Tab') { /* keep focus inside the sheet and its trigger */
        var f = [btn].concat([].slice.call(sheet.querySelectorAll('a,button'))), i = f.indexOf(D.activeElement);
        if (e.shiftKey && i <= 0) { e.preventDefault(); f[f.length - 1].focus(); } else if (!e.shiftKey && i === f.length - 1) { e.preventDefault(); f[0].focus(); }
      }
    });
  }

  /* ---------- Entry motion ---------- */
  if ('IntersectionObserver' in W) {
    if (!reduce) {
      var io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.remove('below'); io.unobserve(e.target); } }); }, { rootMargin: '0px 0px -8% 0px' });
      D.querySelectorAll('.rise').forEach(function (el) { if (el.getBoundingClientRect().top > innerHeight) { el.classList.add('below'); io.observe(el); } });
    }
    var seen = {};
    D.querySelectorAll('section[id]').forEach(function (s) {
      new IntersectionObserver(function (es, o) { es.forEach(function (e) { if (e.isIntersecting && !seen[s.id]) { seen[s.id] = 1; track('section_view', { section: s.id }); o.disconnect(); } }); }, { threshold: 0.3 }).observe(s);
    });
    /* steps fill their rule as they arrive */
    var stepIO = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('on'); stepIO.unobserve(e.target); } }); }, { threshold: 0.6 });
    D.querySelectorAll('.steps li').forEach(function (li, i) { li.style.transitionDelay = (i * 0.12) + 's'; stepIO.observe(li); });
  }

  /* ---------- Manifesto: words light up with reading progress ---------- */
  var mf = D.querySelector('.manifesto .big');
  if (mf) {
    var words = mf.textContent.trim().split(/\s+/), hl = (mf.getAttribute('data-hl') || '').split('|');
    mf.innerHTML = words.map(function (w) { return '<span class="w' + (hl.indexOf(w.replace(/[.,:]/g, '')) > -1 ? ' hl' : '') + '">' + w + '</span>'; }).join(' ');
    var ws = mf.querySelectorAll('.w');
    function mfScroll() { var b = mf.getBoundingClientRect(), p = (innerHeight * 0.95 - b.top) / (b.height + innerHeight * 0.2); var n = Math.round(Math.max(0, Math.min(1, p)) * ws.length); for (var i = 0; i < ws.length; i++) ws[i].classList.toggle('on', i < n); }
    if (!reduce) { addEventListener('scroll', function () { requestAnimationFrame(mfScroll); }, { passive: true }); mfScroll(); }
  }

  /* ---------- Rails ---------- */
  D.querySelectorAll('[data-rail]').forEach(function (wrap) {
    var rail = wrap.querySelector('.rail'); if (!rail) return;
    wrap.querySelectorAll('[data-dir]').forEach(function (b) {
      b.addEventListener('click', function () { var c = rail.querySelector('.card'); var w = c ? c.getBoundingClientRect().width + 20 : 320; rail.scrollBy({ left: +b.getAttribute('data-dir') * w, behavior: reduce ? 'auto' : 'smooth' }); track('rail_nav'); });
    });
  });

  /* ---------- FAQ, copy ---------- */
  D.querySelectorAll('.faq details').forEach(function (d) { d.addEventListener('toggle', function () { if (d.open) track('faq_open', { q: d.querySelector('summary').textContent.trim() }); }); });
  D.querySelectorAll('[data-copy]').forEach(function (b) {
    var label = b.textContent;
    b.addEventListener('click', function () {
      var t = b.getAttribute('data-copy'), done = function () { b.textContent = 'Copiado'; say('Copiado: ' + t); setTimeout(function () { b.textContent = label; }, 1600); };
      try { navigator.clipboard.writeText(t).then(done, function () {}); } catch (e) {}
      track('copy', { what: t });
    });
  });

  /* ---------- Generic WhatsApp links with context ---------- */
  D.querySelectorAll('[data-wa]').forEach(function (a) { a.href = waLink(a.getAttribute('data-wa')); a.target = '_blank'; a.rel = 'noopener'; });

  /* ---------- Mobile dock hides over the quote form and footer ---------- */
  var dock = D.getElementById('dock');
  if (dock && 'IntersectionObserver' in W) {
    var hideFor = D.querySelectorAll('[data-hide-dock], .foot, #resumo'), vis = new Set();
    var dio = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) vis.add(e.target); else vis.delete(e.target); }); dock.classList.toggle('hide', vis.size > 0); dock.inert = vis.size > 0; }, { threshold: 0.05 });
    hideFor.forEach(function (el) { dio.observe(el); });
  }
})();

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
    function f(t) { if (!alive) return; var dt = last ? Math.min(0.1, (t - last) / 1000) : 1 / 60; last = t; onUpdate(spring.step(dt)); if (spring.settled(eps)) { spring.x = spring.to; spring.v = 0; onUpdate(spring.x); alive = false; if (onDone) onDone(); return; } raf = requestAnimationFrame(f); }
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
  /* run fn right after the next layout (a ResizeObserver's first report), so reading geometry at start forces no reflow */
  function afterLayout(fn) { if (!W.ResizeObserver) return requestAnimationFrame(fn); var ro = new ResizeObserver(function () { ro.disconnect(); fn(); }); ro.observe(D.documentElement); }

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
  /* The bar adapts to what scrolls under it: light material over light sections, dark over dark (as on apple.com). */
  function bgLum(el) {
    for (; el && el !== D.documentElement; el = el.parentElement) {
      var c = getComputedStyle(el).backgroundColor, m = c.match(/[\d.]+/g);
      if (m && (m.length < 4 || +m[3] > 0.5)) return (0.2126 * m[0] + 0.7152 * m[1] + 0.0722 * m[2]) / 255;
    }
    var b = getComputedStyle(D.body).backgroundColor.match(/[\d.]+/g); return b ? (0.2126 * b[0] + 0.7152 * b[1] + 0.0722 * b[2]) / 255 : 1;
  }
  /* Band edges are measured in page coordinates only after layout (first layout, load, resize, body height change);
     scrolling then just compares numbers. Sticky and fixed bands (and a dialog, fixed once open) move with the scroll, so they are read live. */
  var bands = [].slice.call(D.querySelectorAll('main > *, main section, .tiles, .tile, .foot')), marks = null, navB = 0, lastEl, lastLight = null, lastEdge = null, edgeRaf = 0;
  function measure() {
    if (!nav) return;
    var sy = scrollY; navB = nav.getBoundingClientRect().bottom;
    marks = bands.map(function (b) {
      var live = b.tagName === 'DIALOG' || /sticky|fixed/.test(getComputedStyle(b).position), r = live ? null : b.getBoundingClientRect();
      return { el: b, live: live, top: r ? r.top + sy : 0, bottom: r ? r.bottom + sy : 0 };
    });
    lastEl = undefined; edge();
  }
  function box(m, sy) { if (!m.live) return [m.top - sy, m.bottom - sy]; var r = m.el.getBoundingClientRect(); return [r.top, r.bottom]; }
  function edge() {
    edgeRaf = 0; if (!marks) return;
    var sy = scrollY, e = sy > 8 ? 1 : 0, y = navB - 4, bx = marks.map(function (m) { return box(m, sy); }), el = null, i;
    /* the block currently under the bar: the deepest band whose box spans the bar's lower edge, else the next one below */
    for (i = 0; i < bx.length; i++) if (bx[i][0] <= y && bx[i][1] > y) el = marks[i].el;
    if (!el) for (i = 0; i < bx.length; i++) if (bx[i][0] > y) { el = marks[i].el; break; }
    if (e !== lastEdge) { lastEdge = e; nav.style.setProperty('--edge', e); }
    if (el === lastEl) return; lastEl = el;
    var light = el ? bgLum(el) > 0.6 : false;
    if (light !== lastLight) { lastLight = light; nav.classList.toggle('light', light); }
  }
  addEventListener('scroll', function () { if (!edgeRaf) edgeRaf = requestAnimationFrame(edge); }, { passive: true });
  addEventListener('resize', measure); addEventListener('load', measure);
  /* the first report arrives right after the first layout, so nothing is measured before the page is laid out */
  if (W.ResizeObserver) new ResizeObserver(function () { measure(); }).observe(D.body); else requestAnimationFrame(measure);
  /* backgrounds can change with these preferences */
  ['(prefers-contrast: more)', '(forced-colors: active)'].forEach(function (q) { try { matchMedia(q).addEventListener('change', measure); } catch (e) {} });

  /* ---------- Menu sheet: scales out of its trigger, closes back into it ---------- */
  var btn = D.getElementById('menuBtn'), sheet = D.getElementById('sheet'), scrim = D.getElementById('scrim');
  if (btn && sheet) {
    var sp = new Spring({ from: 0, to: 0, damping: 1, response: 0.32 }), anim = null, open = false;
    function paint(p) { /* the menu unfolds down out of the bar and folds back into it */ sheet.style.transform = 'translateY(' + (-14 * (1 - p)).toFixed(2) + 'px)'; sheet.style.opacity = Math.max(0, Math.min(1, p)).toFixed(3); }
    function setOpen(v) {
      open = v; btn.setAttribute('aria-expanded', v); scrim.classList.toggle('open', v); D.documentElement.style.overflow = v ? 'hidden' : ''; btn.setAttribute('aria-label', v ? 'Fechar menu' : 'Abrir menu'); if (nav) nav.classList.toggle('menu-open', v);
      if (v) { sheet.classList.add('vis'); sheet.removeAttribute('inert'); }
      [D.querySelector('main'), D.querySelector('.foot'), D.querySelector('.nav-links'), D.querySelector('.brand'), D.querySelector('.nav-wa'), D.querySelector('.nav-cta')].forEach(function (el) { if (el) el.inert = v; });
      sp.to = v ? 1 : 0;
      if (reduce) { sp.x = sp.to; paint(sp.x); if (!v) { sheet.classList.remove('vis'); sheet.setAttribute('inert', ''); } }
      else { if (anim) anim.stop(); anim = run(sp, paint, function () { if (!open) { sheet.classList.remove('vis'); sheet.setAttribute('inert', ''); } }); }
      if (v) setTimeout(function () { var f = sheet.querySelector('a,button'); if (f) f.focus(); }, 30); else btn.focus();
      track('menu', { open: v });
    }
    sheet.setAttribute('inert', '');
    /* the window grew past the phone layout (rotation, resize): the trigger is gone, so the open sheet would trap the page */
    addEventListener('resize', function () { if (open && !btn.getClientRects().length) setOpen(false); });
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
      /* the first report (after layout, no forced reflow) says where each block starts: only blocks below the fold wait; they enter as soon as they show */
      var io = new IntersectionObserver(function (es) {
        var vh = innerHeight;
        es.forEach(function (e) {
          var el = e.target;
          if (!el._rise) { el._rise = 1; if (e.boundingClientRect.top > vh) el.classList.add('below'); else io.unobserve(el); }
          else if (e.isIntersecting) { el.classList.remove('below'); io.unobserve(el); }
        });
      }, { rootMargin: '0px 0px -2% 0px' });
      D.querySelectorAll('.rise').forEach(function (el) { io.observe(el); });
    }
    var seen = {};
    D.querySelectorAll('section[id]').forEach(function (s) {
      new IntersectionObserver(function (es, o) { es.forEach(function (e) { if (e.isIntersecting && !seen[s.id]) { seen[s.id] = 1; track('section_view', { section: s.id }); o.disconnect(); } }); }, { threshold: 0.3 }).observe(s);
    });
    /* steps fill their rule as they arrive */
    var stepIO = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('on'); stepIO.unobserve(e.target); } }); }, { threshold: 0.6 });
    D.querySelectorAll('.steps li').forEach(function (li, i) { li.style.transitionDelay = (i * 0.12) + 's'; stepIO.observe(li); });
  }

  /* ---------- Rails: touch uses native scrolling; mouse gets 1:1 drag, momentum projected to the nearest card, spring settle ---------- */
  D.querySelectorAll('[data-rail]').forEach(function (wrap) {
    var rail = wrap.querySelector('.rail'); if (!rail) return;
    var cards = [].slice.call(rail.children), sp = new Spring({ damping: 1, response: 0.45 }), anim = null, band = new Spring({ damping: 1, response: 0.4 }), bandAnim = null;
    function stops() { var pad = parseFloat(getComputedStyle(rail).paddingLeft) || 0, /* scroll-padding mirrors the padding; its computed value can stay unresolved */ max = rail.scrollWidth - rail.clientWidth; return cards.map(function (c) { return Math.max(0, Math.min(max, c.offsetLeft - pad)); }).concat([max]); }
    function nearest(x) { return stops().reduce(function (b, s) { return Math.abs(s - x) < Math.abs(b - x) ? s : b; }, 0); }
    function snapOff() { rail.style.scrollSnapType = 'none'; }
    function snapOn() { rail.style.scrollSnapType = ''; }
    function glide(target, v) {
      if (anim) anim.stop(); snapOff(); sp.x = rail.scrollLeft; sp.v = v || 0; sp.to = target;
      if (reduce) { rail.scrollLeft = target; snapOn(); return; }
      anim = run(sp, function (x) { rail.scrollLeft = x; }, snapOn, 0.5);
    }
    function setBand(px) { rail.style.transform = px ? 'translateX(' + px.toFixed(1) + 'px)' : ''; }
    wrap.querySelectorAll('[data-dir]').forEach(function (b) {
      b.addEventListener('click', function () {
        var d = +b.getAttribute('data-dir'), cur = anim && anim.alive ? sp.to : rail.scrollLeft, st = stops(), i = 0;
        st.forEach(function (s, j) { if (Math.abs(s - cur) < Math.abs(st[i] - cur)) i = j; });
        glide(st[Math.max(0, Math.min(st.length - 1, i + d))]); track('rail_nav');
      });
    });
    var down = false, dragging = false, sx = 0, start = 0, tr = null, moved = false;
    rail.addEventListener('pointerdown', function (e) {
      if (e.pointerType !== 'mouse' || e.button !== 0) return;
      down = true; dragging = false; moved = false; sx = e.clientX; if (anim) anim.stop(); start = rail.scrollLeft; tr = new Tracker(); tr.add(-start, e.timeStamp);
    });
    rail.addEventListener('pointermove', function (e) {
      if (!down) return; var dx = e.clientX - sx;
      if (!dragging) { if (Math.abs(dx) < 10) return; dragging = true; moved = true; snapOff(); rail.classList.add('grabbing'); try { rail.setPointerCapture(e.pointerId); } catch (_) {} }
      var want = start - dx, max = rail.scrollWidth - rail.clientWidth, over = want < 0 ? want : want > max ? want - max : 0;
      rail.scrollLeft = Math.max(0, Math.min(max, want)); setBand(over ? -rubberband(over, rail.clientWidth) : 0);
      tr.add(-want, e.timeStamp);
    });
    function up() {
      if (!down) return; down = false; if (!dragging) return; dragging = false; rail.classList.remove('grabbing');
      var v = -tr.v(), target = nearest(rail.scrollLeft + project(v, 0.995));
      var off = parseFloat((rail.style.transform.match(/-?[\d.]+/) || [0])[0]);
      if (off) { band.x = off; band.to = 0; band.v = 0; if (bandAnim) bandAnim.stop(); bandAnim = run(band, function (x) { setBand(x); }, function () { setBand(0); }); }
      glide(target, v);
    }
    rail.addEventListener('pointerup', up); rail.addEventListener('pointercancel', up);
    rail.addEventListener('click', function (e) { if (moved) { e.preventDefault(); e.stopPropagation(); moved = false; } }, true);
    rail.addEventListener('dragstart', function (e) { e.preventDefault(); });
    rail.addEventListener('wheel', function () { if (anim) { anim.stop(); snapOn(); } }, { passive: true });
    /* arrows dim at the ends, like Apple's galleries */
    var prev = wrap.querySelector('[data-dir="-1"]'), next = wrap.querySelector('[data-dir="1"]');
    function ends() { var max = rail.scrollWidth - rail.clientWidth; if (prev) prev.disabled = rail.scrollLeft <= 2; if (next) next.disabled = rail.scrollLeft >= max - 2; }
    rail.addEventListener('scroll', function () { requestAnimationFrame(ends); }, { passive: true }); addEventListener('resize', ends); afterLayout(ends);
  });

  /* ---------- Horizontal sub-navigation: fade only the edge that has more content ---------- */
  D.querySelectorAll('.subnav ul').forEach(function (u) {
    var w = u;
    function f() { w.classList.toggle('fade-l', u.scrollLeft > 4); w.classList.toggle('fade-r', u.scrollLeft < u.scrollWidth - u.clientWidth - 4); }
    u.addEventListener('scroll', f, { passive: true }); addEventListener('resize', f); afterLayout(f);
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
})();

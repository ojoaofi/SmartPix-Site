/* Estúdio 3D — the visitor types their brand and sees a full stand printed with it.
   Rotation: 1:1 drag, momentum projected to the nearest view, spring with velocity hand-off (Apple: rotation damping 0.8, response 0.4).
   Renders on demand only (no idle loop). */
(function () {
  'use strict';
  var D = document, SP = window.SP, root = D.getElementById('studio');
  if (!root || !SP) return;
  var input = D.getElementById('brandName'), quote = D.getElementById('studioQuote'), out = D.getElementById('studioOut');
  var swatches = [].slice.call(root.querySelectorAll('.swatch')), views = [].slice.call(root.querySelectorAll('[data-view]'));
  var state = { name: '', color: '#bde000' }, live = D.getElementById('studioLive'), liveT = 0, firstSync = true;
  try { var saved = JSON.parse(sessionStorage.getItem('sp_studio') || 'null'); if (saved) state = saved; } catch (e) {}
  if (state.name) input.value = state.name;

  function brand() { return (state.name || '').trim() || 'SUA MARCA'; }
  function syncUI() {
    swatches.forEach(function (s) { var on = s.getAttribute('data-c') === state.color; s.setAttribute('aria-checked', on); s.tabIndex = on ? 0 : -1; });
    var b = brand(), cname = (swatches.filter(function (s) { return s.getAttribute('data-c') === state.color; })[0] || {}).title || '';
    out.innerHTML = 'Estande <b>' + esc(b) + '</b>: lona 5 × 3 m sem emenda, Smart Floor, balcão, totem e letra-caixa.';
    if (firstSync) { firstSync = false; } else { clearTimeout(liveT); liveT = setTimeout(function () { var t = 'Estande atualizado: ' + b + ', cor ' + cname.toLowerCase() + '.'; if (live && live.textContent !== t) live.textContent = t; }, 800); }
    var p = new URLSearchParams({ origem: 'estudio-3d', produto: 'Estande completo', marca: b, cor: cname });
    quote.href = 'orcamento.html?' + p.toString();
    try { sessionStorage.setItem('sp_studio', JSON.stringify(state)); } catch (e) {}
  }
  function esc(t) { return String(t).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }

  /* ---------- colour helpers ---------- */
  function hex2rgb(h) { h = h.replace('#', ''); return [parseInt(h.substr(0, 2), 16), parseInt(h.substr(2, 2), 16), parseInt(h.substr(4, 2), 16)]; }
  function rgb(a) { return 'rgb(' + a.map(function (v) { return Math.round(Math.max(0, Math.min(255, v))); }).join(',') + ')'; }
  function mix(h, t, k) { var a = hex2rgb(h), b = t === 'w' ? [255, 255, 255] : [0, 0, 0]; return rgb(a.map(function (v, i) { return v + (b[i] - v) * k; })); }
  function lum(h) { var a = hex2rgb(h).map(function (v) { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); }); return 0.2126 * a[0] + 0.7152 * a[1] + 0.0722 * a[2]; }
  function ink(h) { return lum(h) > 0.4 ? '#0b0b0b' : '#ffffff'; }

  /* ---------- printed artwork (canvas) ---------- */
  function fit(g, text, maxW, maxH, weight) {
    var s = maxH; g.font = weight + ' ' + s + 'px Poppins, Arial, sans-serif';
    var w = g.measureText(text).width; if (w > maxW) { s = s * maxW / w; g.font = weight + ' ' + s + 'px Poppins, Arial, sans-serif'; }
    return s;
  }
  function shapes(g, W, H, c, seed) {
    g.fillStyle = mix(c, 'k', 0.28); g.beginPath(); g.moveTo(W * (0.55 + seed * 0.05), 0); g.lineTo(W, 0); g.lineTo(W, H); g.lineTo(W * (0.25 + seed * 0.05), H); g.closePath(); g.fill();
    g.fillStyle = mix(c, 'w', 0.18); g.beginPath(); g.moveTo(W * 0.78, 0); g.lineTo(W * 0.9, 0); g.lineTo(W * 0.62, H); g.lineTo(W * 0.5, H); g.closePath(); g.fill();
  }
  function art(kind, name, c) {
    var cv = D.createElement('canvas'), g = cv.getContext('2d'), W, H, t = ink(c);
    if (kind === 'lona') { W = 2048; H = 1229; cv.width = W; cv.height = H; g.fillStyle = c; g.fillRect(0, 0, W, H); shapes(g, W, H, c, 0);
      g.fillStyle = t; g.textBaseline = 'middle'; var s = fit(g, name, W * 0.62, 300, 700); g.fillText(name, W * 0.08, H * 0.5);
      g.font = '400 ' + Math.round(s * 0.18) + 'px Poppins, Arial, sans-serif'; g.globalAlpha = 0.8; g.fillText('impresso em tamanho real', W * 0.083, H * 0.5 + s * 0.62); g.globalAlpha = 1; }
    else if (kind === 'side') { W = 820; H = 1024; cv.width = W; cv.height = H; g.fillStyle = mix(c, 'k', 0.55); g.fillRect(0, 0, W, H);
      for (var i = 0; i < 7; i++) { g.fillStyle = i % 2 ? c : mix(c, 'w', 0.2); g.globalAlpha = 0.9; g.beginPath(); var x = -200 + i * 170; g.moveTo(x, H); g.lineTo(x + 90, H); g.lineTo(x + 500, 0); g.lineTo(x + 410, 0); g.fill(); }
      g.globalAlpha = 1; g.save(); g.translate(W * 0.5, H * 0.52); g.rotate(-Math.PI / 2); g.fillStyle = '#fff'; g.textAlign = 'center'; g.textBaseline = 'middle'; fit(g, name, H * 0.8, 150, 700); g.fillText(name, 0, 0); g.restore(); }
    else if (kind === 'floor') { W = 2048; H = 1100; cv.width = W; cv.height = H; g.fillStyle = '#121212'; g.fillRect(0, 0, W, H);
      g.fillStyle = c; for (var k = 0; k < 5; k++) { g.globalAlpha = 0.85 - k * 0.14; g.fillRect(0, H * 0.18 + k * 120, W, 54); }
      g.globalAlpha = 1; g.fillStyle = mix(c, 'w', 0.1); g.textAlign = 'center'; g.textBaseline = 'middle'; fit(g, name, W * 0.5, 170, 700); g.fillText(name, W * 0.5, H * 0.82); }
    else if (kind === 'counter') { W = 1024; H = 672; cv.width = W; cv.height = H; g.fillStyle = c; g.fillRect(0, 0, W, H); shapes(g, W, H, c, 1);
      g.fillStyle = t; g.textAlign = 'center'; g.textBaseline = 'middle'; fit(g, name, W * 0.8, 180, 700); g.fillText(name, W * 0.5, H * 0.5); }
    else if (kind === 'totem') { W = 320; H = 1066; cv.width = W; cv.height = H; g.fillStyle = '#0b0b0b'; g.fillRect(0, 0, W, H); g.fillStyle = c; g.fillRect(0, H * 0.62, W, H * 0.38);
      g.save(); g.translate(W * 0.5, H * 0.3); g.rotate(-Math.PI / 2); g.fillStyle = '#fff'; g.textAlign = 'center'; g.textBaseline = 'middle'; fit(g, name, H * 0.52, 120, 700); g.fillText(name, 0, 0); g.restore(); }
    else if (kind === 'letters') { W = 2048; H = 256; cv.width = W; cv.height = H; g.fillStyle = '#fff'; g.textAlign = 'center'; g.textBaseline = 'middle'; fit(g, name.toUpperCase(), W * 0.96, 210, 700); g.fillText(name.toUpperCase(), W / 2, H * 0.54); }
    return cv;
  }

  syncUI();
  input.addEventListener('input', function () { state.name = input.value.slice(0, 22); syncUI(); schedule(); if (!typed) { typed = true; SP.track('studio_brand_typed'); } });
  var typed = false;
  function pick(s) { state.color = s.getAttribute('data-c'); syncUI(); schedule(); SP.track('studio_color', { color: s.title }); }
  swatches.forEach(function (s, i) {
    s.addEventListener('click', function () { pick(s); });
    s.addEventListener('keydown', function (e) { /* radio group: arrows move and select */
      var d = (e.key === 'ArrowRight' || e.key === 'ArrowDown') ? 1 : (e.key === 'ArrowLeft' || e.key === 'ArrowUp') ? -1 : 0; if (!d) return;
      e.preventDefault(); var n = swatches[(i + d + swatches.length) % swatches.length]; pick(n); n.focus();
    });
  });
  quote.addEventListener('click', function () { SP.track('studio_quote', { brand_typed: !!state.name }); });

  /* ---------- WebGL ---------- */
  var hasGL = (function () { try { var c = D.createElement('canvas'); return !!(window.WebGLRenderingContext && (c.getContext('webgl') || c.getContext('experimental-webgl'))); } catch (e) { return false; } })();
  var schedule = function () {};
  if (!hasGL || (navigator.connection && navigator.connection.saveData)) return;
  function load() {
    var s = D.createElement('script'); s.src = 'https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js'; s.crossOrigin = 'anonymous';
    s.onload = function () { try { init(); } catch (e) { console.warn('studio', e); } };
    D.head.appendChild(s);
  }
  if (D.readyState === 'complete') setTimeout(load, 30); else addEventListener('load', function () { setTimeout(load, 30); });

  function init() {
    var T = THREE, stage = root.querySelector('.studio-stage'), cv = D.getElementById('studioCanvas');
    stage.tabIndex = 0; stage.setAttribute('aria-label', 'Visualizador 3D do estande. Use as setas para girar ou os botões de vista.');
    function C(h) { return new T.Color(h).convertSRGBToLinear(); }
    var R = new T.WebGLRenderer({ canvas: cv, antialias: true, alpha: true, powerPreference: 'high-performance' });
    R.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2)); R.outputEncoding = T.sRGBEncoding; R.toneMapping = T.NoToneMapping; R.setClearColor(0, 0);
    var S = new T.Scene(), cam = new T.PerspectiveCamera(32, 2, 0.1, 80);
    S.fog = new T.Fog(0x000000, 18, 40);
    S.add(new T.HemisphereLight(0xffffff, 0x101010, 0.55));
    var key = new T.DirectionalLight(0xffffff, 0.75); key.position.set(-4, 7, 8); S.add(key);
    var fill = new T.DirectionalLight(0xffffff, 0.3); fill.position.set(5, 3, 4); S.add(fill);
    var glow = new T.PointLight(C('#bde000'), 0.0, 9, 2); glow.position.set(0, 2.6, 1.2); S.add(glow);

    function texOf(canvas) { var t = new T.CanvasTexture(canvas); t.encoding = T.sRGBEncoding; t.anisotropy = Math.min(8, R.capabilities.getMaxAnisotropy()); return t; }
    function printMat(t) { return new T.MeshStandardMaterial({ map: t, emissive: 0xffffff, emissiveMap: t, emissiveIntensity: 0.38, roughness: 0.62, metalness: 0 }); }
    var dark = new T.MeshStandardMaterial({ color: C('#151515'), roughness: 0.7 }), white = new T.MeshStandardMaterial({ color: C('#f2f2f2'), roughness: 0.5 });

    /* ground and contact shadow */
    var ground = new T.Mesh(new T.PlaneGeometry(60, 60), new T.MeshBasicMaterial({ color: 0x000000 })); ground.rotation.x = -Math.PI / 2; ground.position.y = -0.002; S.add(ground);
    var sc = D.createElement('canvas'); sc.width = sc.height = 256; var sg = sc.getContext('2d'), gr = sg.createRadialGradient(128, 128, 10, 128, 128, 128); gr.addColorStop(0, 'rgba(0,0,0,.75)'); gr.addColorStop(1, 'rgba(0,0,0,0)'); sg.fillStyle = gr; sg.fillRect(0, 0, 256, 256);
    var shadow = new T.Mesh(new T.PlaneGeometry(8.5, 5.5), new T.MeshBasicMaterial({ map: new T.CanvasTexture(sc), transparent: true, depthWrite: false })); shadow.rotation.x = -Math.PI / 2; shadow.position.y = 0.001; S.add(shadow);

    var parts = {};
    /* Smart Floor 5.6 × 3 m */
    var floorT = texOf(art('floor', brand(), state.color));
    parts.floor = new T.Mesh(new T.BoxGeometry(5.6, 0.04, 3), [dark, dark, printMat(floorT), dark, dark, dark]); parts.floor.position.set(0, 0.02, 0); S.add(parts.floor);
    /* Lona 5 × 3 m, seamless */
    var lonaT = texOf(art('lona', brand(), state.color));
    parts.lona = new T.Mesh(new T.BoxGeometry(5, 3, 0.08), [dark, dark, dark, dark, printMat(lonaT), dark]); parts.lona.position.set(0.3, 1.54, -1.46); S.add(parts.lona);
    /* side wall 2.4 × 3 m */
    var sideT = texOf(art('side', brand(), state.color));
    parts.side = new T.Mesh(new T.BoxGeometry(0.08, 3, 2.4), [printMat(sideT), dark, dark, dark, dark, dark]); parts.side.position.set(-2.24, 1.54, -0.26); S.add(parts.side);
    /* fascia with letra-caixa */
    var fascia = new T.Mesh(new T.BoxGeometry(5.1, 0.5, 0.3), new T.MeshStandardMaterial({ color: C('#0d0d0d'), roughness: 0.4, metalness: 0.2 })); fascia.position.set(0.3, 3.29, -1.32); S.add(fascia);
    var letT = new T.CanvasTexture(art('letters', brand(), state.color));
    var letters = new T.Group(); letters.position.set(0.3, 3.29, -1.16);
    var layerMats = [];
    for (var i = 0; i < 9; i++) {
      var front = i === 8, m = front ? new T.MeshStandardMaterial({ map: letT, transparent: true, alphaTest: 0.5, color: C(state.color), emissive: C(state.color), emissiveIntensity: 0.55, roughness: 0.3 })
        : new T.MeshBasicMaterial({ map: letT, transparent: true, alphaTest: 0.5, color: new T.Color(0x000000).lerp(C(state.color), 0.22 + i * 0.02) });
      layerMats.push(m); var pl = new T.Mesh(new T.PlaneGeometry(4.8, 0.6), m); pl.position.z = i * 0.012; letters.add(pl);
    }
    parts.letra = letters; S.add(letters);
    /* counter 1.6 × 1.05 × 0.6 */
    var counterT = texOf(art('counter', brand(), state.color));
    parts.balcao = new T.Group();
    var body = new T.Mesh(new T.BoxGeometry(1.6, 1.0, 0.6), [white, white, white, white, printMat(counterT), white]); body.position.y = 0.54; parts.balcao.add(body);
    var top = new T.Mesh(new T.BoxGeometry(1.7, 0.05, 0.7), new T.MeshStandardMaterial({ color: C('#1a1a1a'), roughness: 0.35, metalness: 0.3 })); top.position.y = 1.065; parts.balcao.add(top);
    parts.balcao.position.set(1.15, 0.04, 0.55); S.add(parts.balcao);
    /* totem 0.6 × 2 m */
    var totemT = texOf(art('totem', brand(), state.color));
    parts.totem = new T.Mesh(new T.BoxGeometry(0.6, 2, 0.06), [dark, dark, dark, dark, printMat(totemT), dark]); parts.totem.position.set(-1.35, 1.04, 0.95); parts.totem.rotation.y = 0.35; S.add(parts.totem);

    function repaint() {
      var b = brand(), c = state.color;
      [[floorT, 'floor'], [lonaT, 'lona'], [sideT, 'side'], [counterT, 'counter'], [totemT, 'totem']].forEach(function (p) { p[0].image = art(p[1], b, c); p[0].needsUpdate = true; });
      letT.image = art('letters', b, c); letT.needsUpdate = true;
      layerMats.forEach(function (m, i) { if (i === 8) { m.color = C(c); m.emissive = C(c); } else m.color = new T.Color(0x000000).lerp(C(c), 0.22 + i * 0.02); });
      glow.color = C(c); render();
    }
    var tmr = 0; schedule = function () { clearTimeout(tmr); tmr = setTimeout(repaint, 90); };
    if (D.fonts && D.fonts.load) D.fonts.load('700 100px Poppins').then(repaint, function () {});

    /* ---------- camera: yaw on a spring ---------- */
    var STOPS = [-50, -25, 0, 25, 50], LIMIT = 62;
    var yaw = new SP.Spring({ from: SP.reduce ? 25 : 44, to: 25, damping: 1, response: 0.9 }), anim = null;
    var dist = 10;
    function size() { var w = stage.clientWidth, h = stage.clientHeight; if (!w || !h) return; R.setSize(w, h, false); cam.aspect = w / h; dist = Math.max(11, 13 / cam.aspect); cam.updateProjectionMatrix(); render(); }
    var labels = [].slice.call(root.querySelectorAll('.studio-labels span')), anchors = { lona: [-1.3, 2.6, -1.4], piso: [0.6, 0.06, 1.2], balcao: [1.15, 1.25, 0.55], totem: [-1.35, 2.15, 0.95], letra: [2.2, 3.6, -1.2] }, v3 = new T.Vector3();
    function render() {
      var a = yaw.x * Math.PI / 180;
      cam.position.set(Math.sin(a) * dist + 0.2, 3.1, Math.cos(a) * dist); cam.lookAt(0.15, 1.3, -0.3);
      R.render(S, cam);
      var w = stage.clientWidth, h = stage.clientHeight;
      labels.forEach(function (l) { var p = anchors[l.getAttribute('data-part')]; v3.set(p[0], p[1], p[2]).project(cam); l.style.transform = 'translate(' + ((v3.x + 1) / 2 * w).toFixed(1) + 'px,' + ((1 - v3.y) / 2 * h).toFixed(1) + 'px) translate(-50%,-50%)'; });
    }
    function go(target, opts) {
      yaw.to = target; if (opts) yaw.config(opts.damping, opts.response);
      if (SP.reduce) { yaw.x = target; yaw.v = 0; render(); return; }
      if (!anim || !anim.alive) anim = SP.run(yaw, render, null, 0.01);
    }
    function nearest(x) { return STOPS.reduce(function (b, s) { return Math.abs(s - x) < Math.abs(b - x) ? s : b; }, STOPS[0]); }
    function markView(t) { views.forEach(function (b) { b.setAttribute('aria-pressed', +b.getAttribute('data-view') === t); }); }

    /* drag: 1:1, rubber-band past the limit, momentum projected to the nearest stop */
    var dragging = false, sx = 0, sy = 0, startYaw = 0, tracker = new SP.Tracker(), decided = false, horizontal = false, DEG_PER_PX = 0.18;
    stage.addEventListener('pointerdown', function (e) {
      dragging = true; decided = false; horizontal = false; sx = e.clientX; sy = e.clientY;
      if (anim) anim.stop(); startYaw = yaw.x; yaw.v = 0; tracker = new SP.Tracker(); tracker.add(yaw.x, e.timeStamp);
    });
    stage.addEventListener('pointermove', function (e) {
      if (!dragging) return;
      var dx = e.clientX - sx, dy = e.clientY - sy;
      if (!decided) { if (Math.abs(dx) < 10 && Math.abs(dy) < 10) return; decided = true; horizontal = Math.abs(dx) > Math.abs(dy); if (!horizontal) { dragging = false; return; } try { stage.setPointerCapture(e.pointerId); } catch (_) {} root.classList.add('drag'); SP.track('studio_rotate'); }
      var raw = startYaw - dx * DEG_PER_PX, over = Math.abs(raw) - LIMIT;
      yaw.x = over > 0 ? Math.sign(raw) * (LIMIT + SP.rubberband(over, 90)) : raw;
      tracker.add(yaw.x, e.timeStamp); render();
    });
    function release() {
      if (!dragging) return; dragging = false; root.classList.remove('drag');
      if (!horizontal) return;
      var v = tracker.v(), target = nearest(Math.max(-LIMIT, Math.min(LIMIT, yaw.x + SP.project(v, 0.995))));
      yaw.v = v; markView(target); go(target, { damping: 0.8, response: 0.4 });
    }
    stage.addEventListener('pointerup', release); stage.addEventListener('pointercancel', release);
    views.forEach(function (b) { b.addEventListener('click', function () { var t = +b.getAttribute('data-view'); markView(t); go(t, { damping: 1, response: 0.5 }); SP.track('studio_view', { view: t }); }); });
    stage.addEventListener('keydown', function (e) {
      if (e.key !== 'ArrowLeft' && e.key !== 'ArrowRight') return; e.preventDefault();
      var i = STOPS.indexOf(nearest(yaw.to)) + (e.key === 'ArrowRight' ? -1 : 1); i = Math.max(0, Math.min(STOPS.length - 1, i)); markView(STOPS[i]); go(STOPS[i], { damping: 1, response: 0.45 });
    });

    size(); addEventListener('resize', size);
    if (window.ResizeObserver) new ResizeObserver(size).observe(stage);
    root.classList.add('gl'); if (matchMedia('(min-width: 700px)').matches) root.classList.add('labels');
    markView(25); go(25);
  }
})();
